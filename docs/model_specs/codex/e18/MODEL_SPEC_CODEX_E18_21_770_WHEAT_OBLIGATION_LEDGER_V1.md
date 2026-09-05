# MODEL SPEC — Codex E18.21 7-7-0 Wheat obligation ledger V1

## Stato

`GENERATED__PARENT_DELTA_PASS__INCUMBENT_GATE_FAIL__NO_UPLOAD`.

E18.21 eredita integralmente piano, route, retry executor e netting Wheat di
E18.20. L'unica modifica attiva è un ledger per worker dei `PICKUP WHEAT`
emessi nello step corrente: queste unità restano riservate fino all'esecuzione
del batch e non possono essere incluse simultaneamente in `SELL WHEAT`.

Il trattamento supera il delta diretto contro E18.20 in entrambi i seat, ma il
vantaggio assoluto contro E18.16 è marginale. Gate 1 completo, holdout,
final-confirmation e upload Kaggle restano non autorizzati.

## Causa isolata

E18.19/E18.20 avanzano il cursore della route non appena emettono il comando
worker. La costruzione degli ordini di mercato avviene subito dopo, nello
stesso step. Un `PICKUP WHEAT` appena emesso non compare quindi più tra i
fabbisogni pendenti, anche se il motore non lo ha ancora eseguito: il Wheat può
apparire libero ed essere venduto nello stesso batch.

E18.21 intercetta il comando emesso, registra `(giorno, turno, worker, unità)`
e riduce soltanto l'eventuale vendita Wheat dello stesso step. Non aggiunge
acquisti, non modifica le missioni e non conserva scorte oltre lo step.

## Trattamento selezionato

Variante `INFLIGHT_ONLY`, attiva da D11:

1. registrare ogni `PICKUP WHEAT` emesso, separatamente per worker;
2. sommare le unità in-flight del batch;
3. sottrarle da `SELL WHEAT`, entro la quantità vendibile;
4. lasciare invariati tutti gli altri ordini e il netting E18.20;
5. non trasferire la riserva al turno successivo.

Nel test seat-balanced il ledger osserva 277 unità in-flight per episodio,
interviene in 15 turni e protegge complessivamente 115 unità di vendita.

## Ablation respinte

Il controller diagnostico implementa anche un ledger source-tagged per Wheat
acquistato a D+2, ma il flag è disattivato nella versione selezionata.

| Variante | Mediana vs E18.20 | Mediana vs E18.16 | FEED skip vs E18.16 |
|---|---:|---:|---:|
| `INFLIGHT_ONLY` | 75.203,5 | 51.534,5 | 19 |
| `CONTRACTS_ONLY` | 75.518,5 | 51.314,0 | 12 |
| `INFLIGHT_AND_CONTRACTS` | 75.515,5 | 51.292,0 | 12 |

I contratti D+2 aiutano nel confronto simmetrico con E18.20 e riducono i FEED
saltati, ma perdono rispettivamente 220,5 e 242,5 punti rispetto alla variante
in-flight quando l'avversario è E18.16. Il costo di capitale supera quindi il
beneficio biologico su questo smoke; entrambe le varianti restano respinte.

## Invarianti

- piano E18.18 hash
  `844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1`;
- topologia `7-7-0` e 14 pascoli pieni;
- `9 COW + 5 SHEEP`, cap risorse 14;
- 12 hands al picco;
- nessuna mutazione a route, crop, animali o lifecycle;
- zero overlap Wheat nello stesso batch da D11;
- zero errori controller.

## Evidenza pre-gate

### Delta causale contro E18.20

Seed `180903001`, entrambi i seat:

| Seat E18.21 | E18.21 | E18.20 | Margine |
|---:|---:|---:|---:|
| 0 | 75.282 | 74.911 | +371 |
| 1 | 75.125 | 75.066 | +59 |

Mediana E18.21 `75.203,5`, mediana E18.20 `74.988,5`, delta `+215`
(`+0,29%`). Struttura e composizione finali sono esatte; errori zero.

### Confronto con l'incumbent E18.16

| Seat E18.21 | E18.21 | E18.16 | Margine |
|---:|---:|---:|---:|
| 0 | 51.868 | 79.438 | -27.570 |
| 1 | 51.201 | 77.851 | -26.650 |

Mediana E18.21 `51.534,5` contro `78.644,5`, delta `-27.110`
(`-34,47%`). Rispetto allo smoke E18.20 contro lo stesso incumbent, il money
del candidato cresce soltanto di 12,5 punti. Le richieste Wheat scendono da
`SELL 2.377 / BUY 2.211` a `SELL 1.798 / BUY 1.646`, ma i FEED saltati restano
19: il gate incumbent è `FAIL`.

## Verdetto e prossima leva

Il guard in-flight è causalmente corretto, limitato e non regressivo: resta
parte della linea di sviluppo. Non basta però a colmare il gap e E18.21 non
sostituisce E18.16 come migliore sviluppo.

Il churn residuo deriva soprattutto dall'acquisto anticipato D+2 che viene poi
rilasciato dal criterio di vendita D+1. Poiché proteggere quella scorta è troppo
costoso, la prossima ablation deve fare l'opposto: non comprare il fabbisogno
Wheat attribuibile soltanto a D+2 e mantenere procurement just-in-time fino a
D+1. Il guard dei pickup in-flight resta congelato.

Aggiornamento E18.22: il procurement JIT D+1 passa il delta diretto di
`+2.120` mediani e migliora di 507 punti il candidato contro E18.16. Le
richieste Wheat diventano comparabili all'incumbent, ma il gap resta `-33,70%`;
la prossima diagnosi si sposta sui PLANT/HARVEST saltati.

## Artefatti

- config: `configs/CODEX_E18_21_770_WHEAT_OBLIGATION_LEDGER_V1.json`;
- controller: `tools/e18_21_wheat_obligation_ledger_controller.py`;
- test: `tests/test_codex_e18_21_wheat_obligation_ledger_controller.py`;
- runner: `tools/run_e18_21_770_wheat_obligation_ledger_gate.py`;
- risultati:
  `artifacts/derived/E18_21_770_WHEAT_OBLIGATION_LEDGER_PRE_GATE_V1.json`;
- report:
  `reports/E18_21_770_WHEAT_OBLIGATION_LEDGER_PRE_GATE_REPORT_IT.md`.
