# MODEL SPEC — Codex E18.20 7-7-0 Wheat market netting V1

## Stato

`GENERATED__PARENT_DELTA_PASS__INCUMBENT_GATE_FAIL__NO_UPLOAD`.

E18.20 eredita integralmente executor, piano, route e composizione da E18.19.
La sola famiglia causale modificata è il mercato Wheat: dal giorno 11 una
quantità richiesta contemporaneamente con `SELL WHEAT` e
`BUY_PRODUCT WHEAT` viene compensata prima dell'invio al mercato.

Il delta diretto contro E18.19 passa in entrambi i seat. Il vantaggio è però
troppo piccolo e il gap da E18.16 resta ampio; Gate 1 completo, holdout,
final-confirmation e upload Kaggle non sono autorizzati.

## Diagnosi di partenza

Nel match E18.19 contro E18.16, seed `180903001`, seat candidato 0, E18.19
richiedeva:

- `2.942` unità in `SELL WHEAT`;
- `2.776` unità in `BUY_PRODUCT WHEAT`;
- 150 turni con entrambe le operazioni;
- 566 unità di overlap nello stesso batch.

E18.16 richiedeva soltanto 415 vendite e 469 acquisti Wheat. La differenza non
è spiegata dal fabbisogno biologico: E18.19 calcola la vendita sulla riserva
fino a D+1 e il riacquisto su un orizzonte che include D+2. Inoltre il mercato
quota buy e sell unitariamente; un round trip nello stesso batch è
economicamente nullo in isolamento, ma occupa ordini, capitale e interagisce
con gli ordini concorrenti.

## Trattamento selezionato

Da D11, dopo che E18.19 ha prodotto gli ordini nominali:

1. sommare la quantità `SELL WHEAT` del batch;
2. sommare la quantità `BUY_PRODUCT WHEAT` del batch;
3. cancellare `min(sell, buy)` da entrambe;
4. preservare ordine relativo e quantità residue di tutti gli altri ordini;
5. non modificare seed, animali, hire, land, altre vendite o azioni worker.

L'attivazione D11 lascia intatta la finanza critica di setup e lo sblocco NE
di D7. L'overlap precedente a D11 resta una unità e viene registrato, ma non è
parte del trattamento.

## Variante respinta nel pre-gate

È stata provata separatamente anche una riserva Wheat fino a D+2, allineata
all'orizzonte di acquisto. Sul primo seat contro E18.16 riduceva le richieste
da `SELL 2.942 / BUY 2.776` a circa `SELL 575 / BUY 413` e i FEED saltati da
19 a 12, ma abbassava il money da `51.853` a `51.484` circa. Il segnale mostra
che la riduzione del churn è reale, ma una riserva aggregata trattiene Wheat
senza conoscere quale worker lo trasporta e quando torna allo shed. Questa
variante non fa parte di E18.20 V1.

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

### Delta causale contro E18.19

Seed `180903001`, entrambi i seat:

| Seat E18.20 | E18.20 | E18.19 | Margine |
|---:|---:|---:|---:|
| 0 | 75.324 | 74.868 | +456 |
| 1 | 75.135 | 75.057 | +78 |

Mediana E18.20 `75.229,5`, mediana E18.19 `74.962,5`, delta `+267`. Il
candidato elimina dal periodo trattato rispettivamente 566 e 608 unità di
round trip e vince in entrambi i seat. Topologia e composizione finali sono
esatte; errori zero.

### Confronto con l'incumbent E18.16

| Seat E18.20 | E18.20 | E18.16 | Margine |
|---:|---:|---:|---:|
| 0 | 51.857 | 79.437 | -27.580 |
| 1 | 51.187 | 77.860 | -26.673 |

Mediana E18.20 `51.522`, mediana E18.16 `78.648,5`, delta `-27.126,5`
(`-34,49%`). Il netting migliora di soli 5 punti la mediana assoluta E18.19
sullo stesso smoke e di circa 10 punti il margine; non riduce materialmente il
gap.

## Verdetto e prossima versione

Il meccanismo è corretto, seat-balanced e privo di regressioni strutturali,
quindi E18.20 supera il delta causale rispetto al parent. Non supera però il
gate incumbent e non sostituisce E18.16 come miglior sviluppo.

Il churn residuo resta elevato: contro E18.16 E18.20 richiede per seat
`SELL 2.377 / BUY 2.211` Wheat. La prossima ablation non deve reintrodurre la
riserva D+2 aggregata. Deve costruire un ledger di obbligazioni Wheat che
distingua:

- Wheat nello shed realmente libero;
- Wheat acquistato e riservato a pickup futuri;
- Wheat già trasportato dal worker assegnato ai FEED;
- Wheat appena raccolto destinato alla vendita;
- quantità che torneranno allo shed a fine giornata.

Soltanto questo ledger può impedire l'alternanza cross-turn senza immobilizzare
capitale o rendere indisponibile il feed. Piano e traiettorie restano congelati.

Aggiornamento E18.21: il guard per-worker sui `PICKUP WHEAT` in-flight supera
il delta diretto (`+215` mediano), ma migliora di soli 12,5 punti lo smoke
assoluto contro E18.16. I contratti D+2 source-tagged riducono i FEED saltati
ma peggiorano il money e restano respinti. La prossima leva è procurement
just-in-time D+1, non un'ulteriore riserva.

## Artefatti

- config: `configs/CODEX_E18_20_770_WHEAT_MARKET_NETTING_V1.json`;
- controller: `tools/e18_20_wheat_market_netting_controller.py`;
- test: `tests/test_codex_e18_20_wheat_market_netting_controller.py`;
- runner: `tools/run_e18_20_770_wheat_market_netting_gate.py`;
- risultati:
  `artifacts/derived/E18_20_770_WHEAT_MARKET_NETTING_PRE_GATE_V1.json`;
- report:
  `reports/E18_20_770_WHEAT_MARKET_NETTING_PRE_GATE_REPORT_IT.md`.
