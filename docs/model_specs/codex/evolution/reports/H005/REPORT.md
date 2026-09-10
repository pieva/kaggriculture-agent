# H005: stimare la priorita concorrente dalla storia osservabile

84situazioni,42partite,7seed diagnostici gia esposti. Ogni previsione usa solo cinque transizioni H1 precedenti (D15-D19), osservazioni proprie/pubbliche e ordini propri. Le predizioni vengono scritte e hashate prima di leggere etichette D20 e payoff H003. Nessuna nuova policy o submission.

Testimonianze identificate: 83/420; errori retrospettivi: 0. Forecast non astenuti: 31/84; errori: 0. Riordini H003 selezionati: 0; negativi: 0.

## Copertura del modello inverso

| Esito | Testimonianze |
|---|---:|
| ambiguous | 27 |
| floor_unidentifiable | 26 |
| identified | 83 |
| inconsistent_competing_supply | 116 |
| no_own_strawberry | 168 |

## Decisione H005 sulla transizione D20 H1

| Modello | Forecast non astenuti | Errori forecast | Riordini | Negativi | Delta cassa totale |
|---|---:|---:|---:|---:|---:|
| E18 | 24/28 | 0 | 0 | 0 | +0 |
| E19 | 7/28 | 0 | 0 | 0 | +0 |
| E20.1 | 0/28 | 0 | 0 | 0 | +0 |

Nessuna promozione. Una testimonianza storica esatta non garantisce che l avversario mantenga lo stesso ordine il giorno successivo. I payoff riusano soltanto le transizioni H003 coincidenti per hash; non sono nuove partite o risultati terminali. Le astensioni valgono nessun cambiamento, non successi. Il modello inverso supporta acquisti di prodotti/semi e ipotizza una richiesta per prodotto; non identifica in generale acquisti/rivendite compensati o vendite spezzate; i casi incompatibili vengono esclusi.

[Protocollo](../../H005_PROTOCOL.md) - [Predizioni congelate](PREDICTIONS.json) - [Errori ed esiti completi](RESULT.json).

## Interpretazione finale H005

Rispetto a H004, le ricostruzioni storiche identificate aumentano da 64 a 83 su 420 e le previsioni da 18 a 31 su 84. Tutte le 31 previsioni sono `not_first`: 24 per E18, 7 per E19, nessuna per E20.1. Nessuna attiva il riordino H003. Decisione: **NOT_OPERATIONALLY_USEFUL**, non adottato. Zero errori nei casi coperti non dimostra generalizzazione: il campione contiene sette seed diagnostici gia esposti, con ruoli accoppiati.

I 24 test sintetici sul motore coprono vendite e acquisti propri e concorrenti, acquisti di semi e assunzioni: tutti conservano la posizione vera. Il controllo temporale riproduce 420 testimonianze e 84 previsioni rimuovendo D20 e seguito, oscurando anche la fattoria pubblica avversaria; input e hash delle predizioni restano invariati.

La diagnosi successiva, separata dalle predizioni congelate, localizza i 116 residui incompatibili su MILK (75) e WOOL (41). In 50 casi il prezzo iniziale e gia 1; negli altri 66 parte sopra il minimo. Il motore non incrementa lo stock pubblico per le vendite quotate a 1: il residuo negativo non prova acquisti avversari. La diagnosi localizza il limite, senza ricostruire ancora tutte le transazioni dei 66 casi restanti.

Prossimo esperimento da preregistrare: trattare come ricavo certo le vendite dei prodotti non acquistabili gia al minimo, mantenendo non identificato il volume concorrente. Per i prodotti che raggiungono il minimo durante il batch serve invece una ricostruzione compatibile con la saturazione dello stock. Non modificare retroattivamente H005 e non abbassare la soglia delle due testimonianze concordi. I seed riservati 180911301-307 restano inutilizzati.

[Controlli temporali](CHECKS.json) · [Test sul motore](SYNTHETIC_CHECKS.json) · [Diagnosi delle astensioni](ABSTENTION_DIAGNOSIS.json).
