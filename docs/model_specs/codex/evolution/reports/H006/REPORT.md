# H006: stimare la priorita concorrente dalla storia osservabile

84situazioni,42partite,7seed diagnostici gia esposti. Ogni previsione usa solo cinque transizioni H1 precedenti (D15-D19), osservazioni proprie/pubbliche e ordini propri. Le predizioni vengono scritte e hashate prima di leggere etichette D20 e payoff H003. Nessuna nuova policy o submission.

Testimonianze identificate: 116/420; errori retrospettivi: 0. Forecast non astenuti: 40/84; errori: 0. Riordini H003 selezionati: 4; negativi: 0.

## Copertura del modello inverso

| Esito | Testimonianze |
|---|---:|
| ambiguous | 39 |
| floor_unidentifiable | 27 |
| identified | 116 |
| inconsistent_competing_supply | 70 |
| no_own_strawberry | 168 |

## Decisione H006 sulla transizione D20 H1

| Modello | Forecast non astenuti | Errori forecast | Riordini | Negativi | Delta cassa totale |
|---|---:|---:|---:|---:|---:|
| E18 | 24/28 | 0 | 0 | 0 | +0 |
| E19 | 11/28 | 0 | 4 | 0 | +74 |
| E20.1 | 5/28 | 0 | 0 | 0 | +0 |

Nessuna promozione. Una testimonianza storica esatta non garantisce che l avversario mantenga lo stesso ordine il giorno successivo. I payoff riusano soltanto le transizioni H003 coincidenti per hash; non sono nuove partite o risultati terminali. Le astensioni valgono nessun cambiamento, non successi. Il modello inverso supporta acquisti di prodotti/semi e ipotizza una richiesta per prodotto; non identifica in generale acquisti/rivendite compensati o vendite spezzate; i casi incompatibili vengono esclusi.

[Protocollo](../../H006_PROTOCOL.md) - [Predizioni congelate](PREDICTIONS.json) - [Errori ed esiti completi](RESULT.json).

## Interpretazione finale H006

H006 recupera le vendite proprie di prodotti non acquistabili gia al prezzo minimo come ricavi certi, senza stimare il volume concorrente. Soglie e campione invariati rispetto a H005.

Ricostruzioni identificate: 83 -> 116/420; previsioni: 31 -> 40/84. Errori storici 0, errori forecast 0, riordini selezionati 4, riordini negativi 0, delta cassa one-step totale 74.0. Decisione: **DIAGNOSTIC_ONLY_REQUIRES_FULL_CONTINUATIONS**, non adottato.

Passati 120 casi sintetici sul motore, inclusi casi di astensione per fragole e grano al minimo. Riprodotte 420 testimonianze e 84 previsioni senza D20/seguito e senza azioni o stato privato avversari; input e predizioni invariati. Le predizioni H005 restano identiche. Nessuna nuova partita completa, nessuna modifica ai tre modelli, nessun accesso ai seed riservati.

Gli errori sono misurati solo nei casi coperti del campione diagnostico gia esposto (sette seed, ruoli accoppiati). Le astensioni non sono successi. I prodotti che raggiungono il minimo durante il batch restano un limite del modello inverso; il presente esperimento non ne ricostruisce la saturazione.

I quattro riordini selezionati riguardano esclusivamente E19 contro E18: seed 180910204 e 180910206, entrambi i ruoli. Sono due seed, non quattro repliche indipendenti. Il vantaggio immediato per ruolo e rispettivamente +17 e +20 di cassa (+32 e +37 di margine). E20.1 non riceve interventi. Il seguito concreto richiede quattro prosecuzioni modificate e quattro controlli esatti fino a D30, con memoria originale ricostruita, avversario libero di reagire e audit dei 22 KPI; questi risultati terminali non sono ancora disponibili.

[Confronto H005](COMPARISON.json) · [Controlli](CHECKS.json) · [Test sintetici](SYNTHETIC_CHECKS.json).
