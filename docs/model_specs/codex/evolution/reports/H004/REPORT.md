# H004: stimare la priorita concorrente dalla storia osservabile

84situazioni,42partite,7seed diagnostici gia esposti. Ogni previsione usa solo cinque transizioni H1 precedenti (D15-D19), osservazioni proprie/pubbliche e ordini propri. Le predizioni vengono scritte e hashate prima di leggere etichette D20 e payoff H003. Nessuna nuova policy o submission.

Testimonianze identificate: 64/420; errori retrospettivi: 0. Forecast non astenuti: 18/84; errori: 0. Riordini H003 selezionati: 0; negativi: 0.

## Copertura del modello inverso

| Esito | Testimonianze |
|---|---:|
| ambiguous | 14 |
| floor_unidentifiable | 10 |
| identified | 64 |
| negative_competing_supply | 86 |
| no_own_strawberry | 138 |
| unsupported_own_orders | 108 |

## Decisione H004 sulla transizione D20 H1

| Modello | Forecast non astenuti | Errori forecast | Riordini | Negativi | Delta cassa totale |
|---|---:|---:|---:|---:|---:|
| E18 | 18/28 | 0 | 0 | 0 | +0 |
| E19 | 0/28 | 0 | 0 | 0 | +0 |
| E20.1 | 0/28 | 0 | 0 | 0 | +0 |

Nessuna promozione. Una testimonianza storica esatta non garantisce che l avversario mantenga lo stesso ordine il giorno successivo. I payoff riusano soltanto le transizioni H003 coincidenti per hash; non sono nuove partite o risultati terminali. Le astensioni valgono nessun cambiamento, non successi. Il modello inverso ipotizza una vendita per prodotto e non identifica in generale acquisti/rivendite compensati o vendite spezzate; i casi incompatibili vengono esclusi.

[Protocollo](../../H004_PROTOCOL.md) - [Predizioni congelate](PREDICTIONS.json) - [Errori ed esiti completi](RESULT.json).

**Esito: non utile operativamente in questa versione.** Le18previsioni coperte riguardano soltanto E18, senza selezionare riordini; copertura utile E19/E20.1 zero. Zero errori su questi casi selezionati non equivale a prevedibilita generale. I ruoli sono diagnostici, non repliche indipendenti.

Il prossimo passo tecnico e modellare acquisti/vendite misti nella stessa transazione, conservando l astensione quando mancano dati. Il residuo negativo di offerta puo anche dipendere dal floor, non prova da solo un acquisto concorrente. Non si abbassano le soglie dopo gli esiti. [Verifica su storia troncata e input immutabili](CHECKS.json).
