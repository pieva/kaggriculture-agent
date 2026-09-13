# E22 — prima evidenza: chiusura incompleta

Analisi del 13 settembre 2026 richiesta dall'utente. E22 identifica questa nuova fase di analisi; nessuna nuova policy è stata promossa o pubblicata. Campione di riferimento E20.9 / E20v44, submission 56202079.

## Fonte e verifica

[Replay pubblico Kaggle](https://www.kaggle.com/competitions/episodes/108491899/replay.json), episodio 108491899, seed 1392588142, Denis Revenko contro Pietro Valocchi (seat 1). Cassa finale 131885 contro 118902: distacco 12983. Identità, seed e risultato coincidono con lo screenshot fornito dall'utente.

Il replay scaricato è conservato in `data/replays/json/e22_closure_20260913/108491899.json`; hash e risultati riproducibili in [AUDIT.json](AUDIT.json). Lo [script diagnostico](../../tools/audit_closure.py) ricostruisce gli ultimi 11 turni con il motore locale: nel controllo, fattorie, scorte private di entrambi e mercato coincidono esattamente con tutti gli stati registrati. Non interviene alcun cambio di giornata in questo intervallo.

Ricostruita anche la memoria della policy sorgente: 719/719 gruppi di comandi dei lavoratori coincidono con il replay. In 23 turni la lista di mercato differisce; non si dichiara parità completa della policy. Le prove economiche usano gli ordini effettivamente registrati, conservandone l'ordine salvo le integrazioni esplicite.

Orari sotto riferiti all'osservazione prima dell'azione, a base uno. L'ultimo comando è D30 H23: lo stato risultante è D30 H24. Coordinate e indici dei lavoratori a base zero, con lavoratore 0 agricoltore.

## Residui confermati

| Posizione | Prodotto | Quantità |
|---|---|---:|
| Campo (3,7) | Pomodoro | 1 |
| Campo (4,8) | Pomodoro | 1 |
| Campo (2,5) | Grano maturo, seminato D28 | 2 |
| Deposito | Grano | 1 |
| Deposito | Lana | 3 |

Inventari finali dei lavoratori vuoti. Rimangono inoltre tre semi di grano e tre di carota: distinti dai prodotti liquidabili analizzati qui.

## Cause operative

**Pomodori.** Le due missioni sono in fondo alla coda dello specialista 12, dopo i servizi di oca e pecora e il deposito dei loro prodotti. Consegna a H16; a H17 arriva alle missioni e le scarta entrambe. Da (4,5), ogni missione richiede secondo il controllo corrente 3 passi di andata + 3 di ritorno + 3 di margine, contro 7 ore nel confronto interno. Non esiste una redistribuzione verso i lavoratori già liberi. I lavoratori 9 e 10 hanno invece solo PASS da H13 alla fine: mandandoli rispettivamente a (3,7) e (4,8), raccolgono a H18 e H17, consegnano a H22 e H21, e vendono entro la chiusura.

**Grano nel campo.** Il lavoratore 4 arriva sulla casella (2,5), esegue WATER a H18 e riparte a H19; non raccoglie le due unità mature. Sostituendo quell'acqua con HARVEST si mantiene il percorso successivo e si consegna al DROP di H21. È una visita del calendario che non viene convertita in raccolta finale.

**Deposito finale.** A H23 il lavoratore 5 deposita tre lana e lo specialista deposita un grano. Gli ordini sono SELL WHEAT 2 e SELL MILK 15, calcolati sulle scorte visibili prima dei DROP. Il motore esegue prima i lavoratori e poi il mercato: questi prodotti sarebbero vendibili nello stesso turno se l'ordine comprendesse le consegne. Non esiste un successivo turno d'azione H24.

La protezione di rientro in `operational_calendar_v44.py:act_worker` non copre tutti i lavoratori: quelli che seguono i comandi originali vengono serviti direttamente da `operational_calendar_base.py:__call__`. Non basta quindi correggere quella sola funzione per ottenere una garanzia globale di chiusura.

## Prove causali circoscritte

| Prova | Cassa propria | Delta sul controllo | Cassa avversaria |
|---|---:|---:|---:|
| Controllo riprodotto | 118902 | 0 | 131885 |
| Due missioni pomodoro su lavoratori liberi | 119097 | +195 | 131885 |
| Raccolta grano e vendita finale del grano disponibile | 118978 | +76 | 131885 |
| Vendita delle ultime consegne di grano e lana | 119122 | +220 | 131850 |
| Interventi combinati | 119302 | **+400** | 131885 |

La prova combinata lascia zero resa colturale e zero prodotti in deposito. Questi sono effetti economici delle sequenze provate, non valutazioni a prezzo fisso dei singoli residui. Non sono additivi: il mercato condiviso regola le unità dei due giocatori in parallelo e quantità diverse modificano anche gli incassi degli ordini contemporanei. La prova sul grano include la vendita del grano finale disponibile, quindi non è una stima isolata del valore delle sole due unità nel campo.

Le azioni avversarie restano quelle registrate; non viene simulata una sua risposta a una nuova policy. L'integrazione dell'ultimo ordine usa la quantità dopo l'esecuzione dei comandi propri come verifica ex post di fattibilità. Una policy reale dovrà prevedere le consegne dai comandi emessi e dallo stato osservato. Non si tratta di una valutazione competitiva di E22 né di una stima del massimo recuperabile.

## Ipotesi di lavoro E22

L'evidenza sostiene una chiusura coordinata fra lavoratori e mercato: assegnare la resa matura a chi può completare raccolta, trasporto e vendita; convertire visite inutili in raccolte; includere le consegne dell'ultimo turno negli ordini. Il controllo deve coprire anche i lavoratori che seguono il calendario originale.

In questo episodio il recupero dimostrato è 400 monete, circa il 3,1% del distacco iniziale: la sconfitta resta. Prima di implementare una nuova variante, estendere la diagnosi a un campione E20.9 per misurare frequenza, valore e costo opportunità della chiusura, separando questa inefficienza dalle differenze produttive e di mercato che spiegano il resto del divario.
