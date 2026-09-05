# MODEL SPEC — Codex E18.19 7-7-0 retrying trajectory V1

## Stato

`GENERATED__E18_18_DELTA_PASS__E18_16_SMOKE_FAIL__NO_UPLOAD`.

E18.19 è la prima esecuzione state-acknowledged del piano E18.18. Congela il
piano hash
`844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1`,
la topologia `7-7-0`, i 14 pascoli, il mix `9 COW + 5 SHEEP`, i checkpoint
crop e la policy di mercato. Cambia una sola famiglia causale: la gestione di
un task quando lo stato osservato diverge dallo stato nominale.

La build è completa come candidata development, ma non è una policy di
submission: fallisce ancora il primo smoke contro E18.16. Gate 1 completo,
holdout, final-confirmation e upload Kaggle non sono autorizzati.

## Problema corretto

L'executor E18.18 leggeva la cella `(giorno, turno, worker)` e trasformava in
`PASS` un comando non più applicabile. Al turno successivo passava comunque
alla cella seguente. Un'unica weed poteva quindi cancellare `PLANT`, spostare
la posizione effettiva rispetto al percorso e propagare la divergenza a
`WATER`, `HARVEST`, `PLACE` e `FEED`.

E18.19 conserva invece una coda ordinata per ogni coppia
`(giorno, worker)`. Un task resta in testa finché viene:

- eseguito sullo stato corretto;
- preceduto da un'azione di ripristino;
- riconosciuto come stale e saltato;
- abbandonato dopo un retry limitato, per non bloccare il resto della giornata.

I `PASS` pianificati vengono rispettati quando sono futuri e assorbiti come
slack quando la coda è in ritardo.

## Regole di esecuzione

### Posizione e tile

- se la posizione non coincide con il target, viene emesso un solo MOVE
  deterministico verso il target e il task non avanza;
- una weed davanti a `PLANT` o `BUILD_PASTURE` produce `DIG`, poi retry;
- `PLACE` su tile vuota produce prima `BUILD_PASTURE`;
- MOVE già soddisfatti e azioni optional diventate stale vengono consumati
  senza emettere un comando illegale.

### Logistica e continuità

- `PICKUP` usa la quantità realmente disponibile;
- se il prelievo è parziale, la quantità residua resta in coda;
- il procurement ha al massimo un turno di attesa; se non riesce, la coda
  degrada e prosegue;
- `PLANT`, `BUILD_PASTURE` e `PLACE` hanno lo stesso retry limitato dopo il
  tentativo di ripristino;
- un `FEED` senza Wheat già trasportato viene saltato: restare fermi sul
  pascolo non può rendere raggiungibile il Wheat presente nello shed e
  cancellerebbe tutti i servizi successivi;
- `WATER`, `HARVEST`, `FERTILIZE`, `DIG`, `CARE`,
  `COLLECT_FERTILIZER` e `DROP` non più applicabili vengono saltati.

Il mercato conta soltanto le richieste non ancora consumate dalla coda. I
`DROP` previsti nello stesso batch sono valorizzati soltanto quando l'executor
li emette realmente.

## Invarianti e criteri

- `7-7-0` esatto a D30;
- 14 pascoli pieni, cap COW/SHEEP 14;
- `9 COW + 5 SHEEP` a D30;
- zero errori controller;
- nessun task critico può bloccare indefinitamente una route;
- E18.18 è il controllo causale del layer di esecuzione;
- E18.16 resta l'incumbent economico e deve essere eguagliato prima del Gate 1
  completo.

## Evidenza development

### Delta diretto contro E18.18

Sul seed `180903001`, entrambi i seat e con il medesimo piano:

| Seat E18.19 | E18.19 | E18.18 | Margine |
|---:|---:|---:|---:|
| 0 | 92.554 | 54.654 | +37.900 |
| 1 | 94.168 | 55.213 | +38.955 |

Mediana E18.19 `93.361`, mediana E18.18 `54.933,5`: `+38.427,5`, pari a
`+69,95%`. E18.19 chiude `7-7-0` e `9 COW + 5 SHEEP` in entrambi i seat;
E18.18 resta rispettivamente a `3+1` e `2+2` animali nel confronto diretto.
Zero errori per entrambi.

Questo PASS identifica l'effetto positivo del retry, ma non misura la
competitività assoluta.

### Smoke contro l'incumbent E18.16

Sul medesimo seed e nei due seat:

| Seat E18.19 | E18.19 | E18.16 | Margine |
|---:|---:|---:|---:|
| 0 | 51.853 | 79.440 | -27.587 |
| 1 | 51.181 | 77.867 | -26.686 |

Mediana E18.19 `51.517`, mediana E18.16 `78.653,5`, delta `-27.136,5`
(`-34,50%`). Gli invarianti strutturali ora passano: entrambe le esecuzioni
E18.19 terminano `7-7-0`, `9 COW + 5 SHEEP`, crop terminali zero, shed vuoto,
due weed residue e zero errori. Restano 19 FEED e 11 PLANT saltati per seat;
soltanto quattro righe per esecuzione restano fuori dalla finestra giornaliera.

Il fallimento economico, non più strutturale, blocca il Gate 1 completo.

## Diagnosi e prossima ablation

Il delta rispetto a E18.18 dimostra che la traiettoria nominale è
recuperabile. Il confronto con E18.16 mostra però sensibilità alla contesa di
mercato: contro l'executor E18.18 E18.19 monetizza circa 93k, contro E18.16
circa 52k. La prossima versione deve isolare una sola famiglia causale:
procurement e liquidazione market-aware sotto contesa, mantenendo congelati
layout, crop plan, animali e route.

Prima di cambiare il mercato vanno derivati dal replay matched almeno:

- valore e quantità SELL per prodotto e fase;
- prezzo medio realizzato e opportunity loss rispetto al prezzo giornaliero;
- quantità BUY non soddisfatte e relativo impatto su 19 FEED/11 PLANT;
- capitale impegnato in animali, semi, land e hire per giorno;
- output prodotto ma non monetizzato o monetizzato in batch congestionati.

Solo un'ablation con miglioramento seat-balanced contro E18.16 può autorizzare
i sette seed del Gate 1. Nessun upload esterno è previsto per E18.19 V1.

### Esito del successore E18.20 — 2026-09-05

Il netting degli ordini Wheat nello stesso batch supera il delta diretto
contro E18.19 in entrambi i seat (`+267` sulla mediana), ma migliora di soli 5
punti il money nello smoke contro E18.16 e lascia un gap del `34,49%`.
E18.20 è documentata in
`MODEL_SPEC_CODEX_E18_20_770_WHEAT_MARKET_NETTING_V1.md`; non è promossa e non
autorizza il Gate 1 completo o una submission.

## Artefatti

- config: `configs/CODEX_E18_19_770_RETRYING_TRAJECTORY_V1.json`;
- executor: `tools/e18_19_retrying_trajectory_controller.py`;
- test: `tests/test_codex_e18_19_retrying_trajectory_controller.py`;
- smoke incumbent:
  `artifacts/derived/E18_19_770_RETRYING_TRAJECTORY_GATE_1_SMOKE_V1.json`;
- delta E18.18:
  `artifacts/derived/E18_19_770_RETRYING_TRAJECTORY_INTERNAL_DELTA_V1.json`;
- report smoke:
  `reports/E18_19_770_RETRYING_TRAJECTORY_GATE_1_SMOKE_REPORT_IT.md`;
- report delta:
  `reports/E18_19_770_RETRYING_TRAJECTORY_INTERNAL_DELTA_REPORT_IT.md`.
