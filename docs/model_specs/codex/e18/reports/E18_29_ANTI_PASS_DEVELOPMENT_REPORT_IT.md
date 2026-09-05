# E18.29 B3 — anti-PASS con protezione del servizio

2026-09-05. Parent E18.28 C pubblicata (56036993), topologia 770 invariata.
Development: sette seed × due seat contro E18.16; non sono 14 seed indipendenti.
Controllo aggiuntivo E18.2/V4D su un seed × due seat. Nessun holdout o upload.

## Intervento

Missioni aggiuntive solo quando il worker ha terminato tutti i task produttivi del giorno e ha inventario vuoto: raccolta fertilizzante disponibile, consegna allo shed, rientro alla posizione iniziale. Prenotazione tile e budget completo entro H23; nessun nuovo acquisto, hire, semina o cambio calendario. Il mercato parent può vendere il surplus o usarlo al posto degli acquisti previsti.

OFF riproduce tutti i 719 batch del parent in entrambi i seat. A isola D7-D12; B estende D7-D30. Lo smoke iniziale è conservato; prima dell'estensione si è aggiunta una guardia prudenziale per gli inventari degli altri worker presso lo shed e l'audit delle consegne effettive.

B migliorava tutti i 14 profili (+5.577,43 medi), ma è stata fermata: il fertilizzante aggiuntivo rende eseguibili boost prima saltati, riducendo il margine della coda. Nel caso diagnosticato PLANT Wheat slittava a D21 H24, senza WATER, causando morte al refresh. Il tentativo B2 di saltare FERTILIZE è risultato inerte: il worker interessato non aveva tale task. La traccia completa rivela invece due MOVE aggiuntivi per lo spawn differente di M11, con mangime già disponibile. B3 confronta le due assegnazioni delle code dei due ultimi hands appena assunti e le scambia solo se questo permette a entrambe di rispettare la scadenza. Nessuna regola condizionata a seed o coordinate. L'audit delle morti per sete viene eseguito in ogni match B3.

## KPI medi development

| KPI | E18.28 C | E18.29 B3 | Delta |
|---|---:|---:|---:|
| Cassa finale | 74,491.57 | 80,212.57 | +5,721.00 |
| PASS | 1,568.07 | 1,148.07 | -420.00 |
| MOVE | 3,053.00 | 3,299.86 | +246.86 |
| Fertilizzante raccolto | 106.57 | 170.86 | +64.29 |
| Fertilizzante consegnato | 106.57 | 170.86 | +64.29 |
| Fertilizzante venduto | 74.57 | 111.29 | +36.71 |
| Fertilizzante acquistato | 0.00 | 0.00 | +0.00 |
| Fertilizzante utilizzato | 32.00 | 59.57 | +27.57 |
| Costo manodopera | 6,858.00 | 6,858.00 | +0.00 |
| FEED eseguiti | 325.14 | 325.14 | +0.00 |
| WATER eseguiti | 1,156.86 | 1,156.86 | +0.00 |

## Esiti matched

| Seed | Seat | Parent | B3 | Delta | Sicurezza |
|---|---:|---:|---:|---:|---|
| 180903001 | 0 | 77,898 | 85,359 | +7,461 | PASS |
| 180903001 | 1 | 77,898 | 85,359 | +7,461 | PASS |
| 180903002 | 0 | 69,773 | 75,764 | +5,991 | PASS |
| 180903002 | 1 | 69,773 | 75,764 | +5,991 | PASS |
| 180903003 | 0 | 61,940 | 68,175 | +6,235 | PASS |
| 180903003 | 1 | 61,940 | 68,175 | +6,235 | PASS |
| 180903004 | 0 | 59,438 | 62,635 | +3,197 | PASS |
| 180903004 | 1 | 51,338 | 54,600 | +3,262 | PASS |
| 180903005 | 0 | 93,875 | 99,665 | +5,790 | PASS |
| 180903005 | 1 | 93,250 | 99,157 | +5,907 | FAIL |
| 180903006 | 0 | 96,030 | 99,673 | +3,643 | PASS |
| 180903006 | 1 | 96,030 | 99,673 | +3,643 | PASS |
| 180903007 | 0 | 71,963 | 79,296 | +7,333 | PASS |
| 180903007 | 1 | 61,736 | 69,681 | +7,945 | PASS |

## Attribuzione economica

I flussi sono rieseguiti nel motore esatto e riconciliati con la cassa finale in tutti i 719 batch di entrambi i giocatori. La differenza comprende gli effetti endogeni su disponibilità e prezzi; non attribuire tutto l'aumento al prezzo iniziale del fertilizzante.

| Voce | Delta medio |
|---|---:|
| purchase_cash:BUY_PRODUCT:WHEAT | -650.36 |
| sales_cash:FERTILIZER | +1,696.07 |
| sales_cash:MILK | +20.43 |
| sales_cash:STRAWBERRY | +2,957.93 |
| sales_cash:WHEAT | +396.21 |

## Andamento temporale

| Giorni | PASS parent | PASS B3 | MOVE parent | MOVE B3 |
|---|---:|---:|---:|---:|
| D1–D6 | 270.57 | 270.57 | 243.00 | 243.00 |
| D7–D12 | 528.86 | 496.29 | 481.00 | 503.57 |
| D13–D15 | 48.21 | 48.21 | 271.00 | 271.00 |
| D16–D24 | 517.93 | 222.50 | 1,170.00 | 1,340.29 |
| D25–D30 | 202.50 | 110.50 | 888.00 | 942.00 |

## Controllo E18.2/V4D

| Seat | Parent | B3 | Delta | Sicurezza |
|---|---:|---:|---:|---|
| 0 | 60,612 | 67,745 | +7,133 | PASS |
| 1 | 60,612 | 67,745 | +7,133 | PASS |

## Verdetto e limiti

Gate economico: PASS; gate completo di sicurezza: FAIL. Delta medio +5,721.00; peggiore +3,197. Nessuna promozione automatica a incumbent.

Verifica crop nel caso seed 180903005 seat 1: parent [{'service_day': 12, 'position': [4, 8], 'crop': 'STRAWBERRY'}]; B3 [{'service_day': 12, 'position': [4, 8], 'crop': 'STRAWBERRY'}]. La riesecuzione parent ha gli stessi 719 batch del parent congelato. Il criterio preregistrato di zero morti per sete rimane assoluto: un eventuale difetto ereditato non viene nascosto né trasformato retroattivamente in un PASS del gate.

Prima del rilascio va risolta la missione PLANT→WATER di D12 già difettosa nel parent: prenotare e confermare l'irrigazione iniziale insieme alla semina. Questo primo intervento non risolve il sottoutilizzo iniziale né ripristina le giornate CARE escluse dal piano. Successivamente, in ablation separate: accorpare le raccolte compatibili in giri multi-tile e valutare CARE soltanto dove il bonus sarà prodotto, raccolto e venduto entro D30. I MOVE aumentano per la logistica aggiuntiva; il beneficio va giudicato sulla cassa netta, non su PASS=0.

Artefatti, strumenti e test sono sotto docs/model_specs/codex/e18. NEW_SESSION/PROJECT_STATE, pulizia cache e Git restano distinti e differiti al workflow di verifica dell'upload E18.28. Nessuna nuova submission in questo sviluppo.

B3−B medio: +143.57; scambi di code ai nuovi hands: 1.00 per partita. Vittorie dirette su E18.16: parent 1/14, B3 4/14. Il miglioramento matched non equivale a dominare il campione interno.
