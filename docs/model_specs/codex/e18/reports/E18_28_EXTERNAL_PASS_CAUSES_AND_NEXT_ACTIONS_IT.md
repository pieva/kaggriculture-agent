# PASS: diagnosi esterna e priorità della prossima ablation

2026-09-05. Evidenza: [campione completo e KPI](E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_IT.md),
submission [56036993](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56036993).
Analizzata E18.28 C, non la candidata interna E18.29 B3.
Tutti i 30 replay competitivi disponibili nella lista ispezionata, 17 sconfitte
e 13 vittorie contro 30 avversari distinti; escluso solo il self-test.

## Conclusione

Concentrarsi sui PASS è giustificato: il difetto non dipende dal solo Top770.
L'obiettivo, però, è recuperare valore netto negli slot inutilizzati, non
azzerare il contatore. Un MOVE inutile non costituisce un miglioramento.

Nelle sconfitte E18.28 registra 1.578,9 PASS a partita; nelle vittorie 1.566,9.
La quasi identità segnala un limite strutturale presente in entrambe, non una
spiegazione sufficiente dell'esito. La variabilità di mercato, avversario,
resa e tenuta della traiettoria determina quanto quel limite pesa sul risultato.

In D15-D30: 746,3 PASS medi nelle sconfitte contro 181,2 degli avversari,
15,92% contro 4,05% degli slot realmente disponibili. Le architetture degli
avversari non sono equivalenti: non attribuire causalmente il delta a una
singola regola, né copiare il loro mix. La nostra topologia è 770 in 30/30.

## Cause verificate e ipotesi da sottoporre a test

| Priorità | Evidenza | Causa / limite | Prossimo rimedio da verificare |
|---|---|---|---|
| 1 — capacità a fine coda | 622,8 dei 746,3 PASS D15-D30, **83,5%**, sono `QUEUE_FINISHED` | Il worker non ha più task produttivi assegnati; il parent restituisce PASS senza cercare altre missioni | Coda comune delle missioni ancora utili e riassegnazione ai worker liberi, con prenotazione esclusiva e costo completo di andata/servizio/consegna/rientro |
| 2 — calendario rigido | 123,5 PASS D15-D30, **16,5%**, sono `WAIT_SCHEDULED_TURN` | La prossima azione non è ancora autorizzata dall'orario della traiettoria | Separare vincoli reali (maturazione, disponibilità, mercato, altri worker) dal timestamp del piano; anticipare solo task i cui prerequisiti e conseguenze sono verificati |
| 3 — missioni prive di esecutore, sicurezza obbligatoria | Due sconfitte: D11 solo 7 o 3 hands contro 11 previsti; rispettivamente 9 e 23 crop morte in D12/D15 | Assunzioni non finanziate; il piano continua ad assegnare lavoro a worker assenti. Nessun ulteriore HIRE richiesto dopo H2, anche quando la cassa recupera | Riserva payroll/servizio prima della spesa discrezionale, ACK delle assunzioni e redistribuzione delle missioni orfane; retry tardivo solo se resta tempo per una missione utile |
| 4 — impiego economico degli slot | PASS locali D15-D30 coincidono con fertilizzante disponibile in 32,1 tile-giorni e CARE non eseguita in 23 tile-giorni medi per sconfitta | Opportunità non incluse nel piano; non tutte sono monetizzabili o compatibili | Valutare fertilizzante raccolto/consegnato/usato o venduto; CARE solo con successivi FEED, produzione, raccolta e vendita prima di D30 |

Le priorità indicano l'ordine diagnostico e di sviluppo, non una stima in denaro.
La sicurezza del punto 3 è un requisito di rilascio anche se l'ablation di
produttività parte dal punto 1. Le ablation vanno separate: non introdurre
insieme mercato, assunzioni, nuova coltura e nuovo calendario.

Nessun PASS D15-D30 del campione è classificato come blocco immediato di
PICKUP/PLANT/PLACE. Questo esclude tali attese come causa diretta del conteggio
tardivo; **non** esclude effetti indiretti di carenze precedenti o task saltati.

## Due sconfitte che rendono visibile il problema di adattamento

- Replay **105864674**: D11 inizia con cassa 44. Dopo H1 rimangono 11 e sono
  assunti 7 hands. Da H3 non viene più richiesto HIRE; a H18 la cassa è 3.164,
  ma gli hands restano 7. Restano nelle code D11 14 WATER e 4 HARVEST, oltre
  alla logistica, assegnati a worker non attivati. A D12 si registrano 9 crop
  morte per sete. Finale 50.144 contro 93.378.
- Replay **105874761**: D11 inizia con cassa 4, che permette 3 hands. Nessun
  HIRE dopo H2; la cassa recupera a 272 a H18, ma gli hands restano 3. Le
  code D11 non eseguite includono 27 WATER e 12 HARVEST. A D12 muoiono 22
  crop, più una Wheat a D15: totale 23. Finale 55.091 contro 82.373.

In entrambi esistono anche PASS di worker reali con coda terminata.
Ciò prova la coesistenza di capacità inutilizzata e missioni non eseguite;
non prova che tutti i raccolti fossero salvabili con il tempo e le distanze
residue. Il recupero va dimostrato nel motore, non assunto dal conteggio.
I timestamp, cash, hands e richieste HIRE sono conservati in `failure_cases`
del dataset aggregato V2; le code integrali restano nei derivati per episodio.

## Dove cercare il rendimento economico

Nelle 17 sconfitte, con tutti i flussi riconciliati, i ricavi lordi medi da
Strawberry sono 27.841 nostri contro 42.904 avversari; Fertilizer 6.430 contro
13.887; Wool 14.507 contro 21.719. Sono divari descrittivi, **non** guadagni
recuperabili né contributi causali sommabili: mix, quantità, prezzi, costi e
topologie differiscono. Ad esempio il numero di HARVEST non misura la resa.

La linea fertilizzante già esplorata da E18.29 B3 è quindi coerente con un
segnale esterno indipendente da Top770. Non è però stata verificata su queste
partite: non trasferire automaticamente il +5.721 locale al campione pubblico.
Non occorre aprire ora un altro esperimento di espansione delle mucche.

Per ogni missione anti-PASS misurare: slot convertiti in servizio effettivo,
MOVE aggiuntivi, quantità prodotte/consegnate/vendute, costi, incasso netto e
ritardi imposti alle missioni già previste. Un CARE senza raccolta del bonus
o un raccolto senza consegna non dimostra miglioramento economico.

## Protocollo anti-overfitting

1. Congelare questo campione completo e usarlo per classificare failure mode,
   senza condizionare il comportamento a nomi, episode ID, seed o coordinate
   specifiche osservate in una singola partita.
2. Sviluppare su campioni interni congelati, seed development preregistrati ed
   entrambi i seat; confrontare parent e trattamento sotto gli stessi avversari.
3. Aggiungere test sintetici del meccanismo: hire parziale, cassa che recupera,
   worker assente, coda vuota, task anticipabile/non anticipabile, shed pieno,
   deadline FEED/WATER, chiusura H23/D30. Nessuna regola ad hoc per il replay.
4. Holdout separato, nessun rilascio con nuove morti crop/animali o violazioni
   del target 770/cap 14/max 12 hands. Verificare delta medio e worst-case.
5. La successiva submission quotidiana fornisce il nuovo controllo esterno.
   Questo campione, una volta usato per la diagnosi, non è più un holdout.

## Riproducibilità e limiti

Trenta replay, 21.570 batch con parità esatta delle decisioni del nostro
controller. Cash verificata in 29/30 episodi, incluse **tutte le 17 sconfitte**.
Un episodio vinto, 105852748, ha un disaccordo di 81 nella cassa avversaria a
step 549: conservato e escluso soltanto dai flussi. Il batch contiene un DROP
con shed quasi pieno; l'ordine delle chiavi inventario nel JSON può influire
sulla ricostruzione dell'overflow. È un'ipotesi sul parser, non un difetto
attribuito al nostro agente. Non è stata corretta occultando il disaccordo.

Sei test di integrità del dataset superati. Nessuna policy/config/piano
modificata, nessuna nuova simulazione, submission, promozione, pulizia generale
o operazione Git. I download restano nei percorsi esatti del manifest; nessuna
duplicazione dei grezzi nel repository. Il documento stabilisce ipotesi per
la prossima release, non attesta che siano già implementate.
