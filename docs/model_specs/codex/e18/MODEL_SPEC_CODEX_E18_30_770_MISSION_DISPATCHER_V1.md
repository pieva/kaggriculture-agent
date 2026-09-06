# E18.30 V1 — 770, motore di assegnazione per missioni

Stato: **CROP_POOL V2 — DEVELOPMENT_ECONOMIC_AND_SAFETY_PASS / STANDALONE_PASS**, 2026-09-06.
Parent economico immutabile: E18.28 C (56036993). E18.29 B3 è un controllo
secondario, non un rilascio promosso. Topologia 770, 14 pascoli, cap 14 animali,
massimo 12 manovali. Cambia assegnazione, non mix/specie/apertura/topologia.

## Problema e obiettivo

Nelle 17 sconfitte esterne E18.28: 746,3 PASS D15-D30, 83,5% code esaurite.
I lavoratori non condividono il backlog. Nei casi 105864674 e 105874761,
assunzioni fallite lasciano lavoro produttivo su worker inesistenti; il mercato
non riprova dopo H2. Ridurre i PASS è una diagnostica, non la funzione obiettivo:
si cerca maggiore cassa finale con servizio e sicurezza preservati, non più MOVE.
Fonte: `reports/E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md`.

## Contratto del nuovo motore

- Missione identificata semanticamente per giorno, tile, servizio/ciclo; deduplica
  prima dell'assegnazione. Non trasferire a un altro worker una coda di MOVE
  assoluta: ricostruire la rotta dalla posizione effettiva.
- Pool globale con stati READY, ASSIGNED, DONE, CANCELLED, EXPIRED; il ledger
  registra anche attesa prerequisiti e motivazione di mancata assegnazione.
- Snapshot di lavoratori reali all'inizio del batch; identità persistenti
  fornite dall'adattatore, non indici presunti attraverso licenziamenti/assunzioni.
- Prima riconciliare conferme osservate, assegnatari scomparsi, missioni non
  più valide e deadline. Solo dopo assegnare il lavoro ancora ammissibile.
- DONE soltanto da conferma osservata. Emissione comando e fine coda non sono
  esecuzione. Dopo blocco o perdita prerequisito rilasciare i claim; missioni
  con inventario in-flight richiedono recovery esplicita dell'adattatore.
- Il nucleo riceve offerte di rotta completa già verificate: costi di avvicinamento,
  servizio, ritorno/DROP, disponibilità scorte/shed e deadline finale. Non usare
  Manhattan come prova di fattibilità in presenza di gate, ostacoli o merci.
- Prenotazioni esclusive e quantitative condivise nel batch; nessun doppio
  servizio tile/ciclo, doppio uso di inventario o capacità shed.
- Ordine iniziale deterministico: missioni di safety, deadline, valore netto
  stimato per slot totale, località e ID come tie-break. Il ranking non è una
  promessa di ottimo globale. Mantenere missioni avviate per evitare thrashing.
- PASS con causale diagnostica solo quando nessuna missione ammessa. Distinguere
  attesa biologica legittima, cassa/scorte, capacità, deadline e pool realmente vuoto.

## Tranche e ablation

0. Nucleo puro del ledger/assegnatore con test: hiring non confermato, lavoro
   orfano, prerequisiti mancanti, deduplica, deadline, claims e acknowledgement.
   Nessuna connessione al runtime pubblicato, nessuna promessa economica.
1. Adattatore state-aware e route admission sulle missioni già nel piano E18.28:
   redistribuzione senza modificare obiettivi economici; dry-run/OFF parity.
2. Payroll e HIRE con riserva di liquidità, retry dopo incassi osservati, nuova
   ammissione lavoro con capacità realmente acquisita. Ablation separata.
3. Generatore di missioni redditizie per pool scarico: CARE/HARVEST/fertilizzante
   e rotazioni solo con ciclo completo economicamente fattibile; ablation separata.

## Gate preregistrati

Gate 0: unit test contratti, ordine deterministico, zero doppie prenotazioni,
zero assegnazioni a worker assenti; OFF action parity col parent.
Gate 1: smoke seed 180903001, entrambi i seat, contro E18.16 ed E18.2.
Gate 2: sette seed development 180903001–180903007 × due seat contro E18.16,
parent matched; E18.29 B3 confronto secondario. Non consumare holdout in debug.
Safety: zero fughe, zero morti crop per promozione (il difetto ereditato resta
visibile), servizio FEED/WATER senza nuove deadline mancate, cap invariati.
Economia: delta medio positivo, almeno 12/14 delta non negativi e worst non
peggiore di -1% rispetto al parent; da giudicare insieme al gap vs controlli,
non sufficiente per chiamare la candidata incumbent. Soglie fissate prima dei run.
Efficienza: riportare PASS/slot, MOVE/productive e cassa netta per missione;
non promuovere una sola riduzione PASS. Report standard V3 D1-D30, sempre due curve.
Poi standalone parity e validazione esterna del migliore sviluppo eleggibile.

I 30 replay pubblici sono corpus diagnostico, non holdout o target da ottimizzare.
Stress sintetici low-cash/hiring fallito e cambi roster devono essere generici,
non branch sui seed/ID degli episodi. Nessun nuovo upload prima dei gate.

## As-built della prima tranche

Implementato `tools/e18_30_mission_dispatcher.py`: ledger e pool condiviso,
manovali osservati, recupero orfani, deduplica, conferme, deadline e claim
quantitativi. Offerte fresche e fattibili per l'intera rotta residua, compresa
consegna, devono essere fornite dall'adattatore; non sono inferite dal nucleo.
25 test pass, incluso stress deterministico su 100 scenari sintetici.
Report: `reports/E18_30_MISSION_DISPATCHER_GATE_0_IT.md`.

La prima tranche copriva solo i contratti. L'integrazione online successiva
è descritta sotto; il report Gate 0 rimane storico, non stato corrente.

## Tranche online — 2026-09-06

Adattatore `tools/e18_30_mission_runtime.py`, runner e riepilogo matched dedicati.
Preregistrazione: `reports/E18_30_RUNTIME_PREREGISTRATION_20260906_IT.md`.
Identità giorno/slot osservato, percorsi verificati nel motore, ritorno prima
del successivo task parent, prenotazione shed e acknowledgement dopo esecuzione.
OFF delega al parent; RESCUE recupera WATER già dovuti a rischio deadline;
POOL aggiunge, separatamente, missioni complete di fertilizzante non prenotato.
Economia parent e target 770/cap 14/max 12 hands conservati; HIRE non modificato.

36 test contratti/adattatore passati. Smoke: 16 partite, seed 180903001,
entrambi i seat contro E18.16 ed E18.2/V4D. OFF: 2.876 batch identici al parent.
RESCUE invariata nello smoke senza deficit. POOL contro E18.16: 87.549 contro
77.898 parent; contro E18.2: 69.768 contro 60.612. PASS 1.076 contro 1.558,
MOVE 3.294 contro 3.053. Zero morti crop/fughe/errori/missioni incomplete nei
quattro casi POOL; nessuna vittoria contro i controlli. Non è una promozione.
Fonte: `reports/E18_30_SMOKE_SUMMARY_V1_20260906_IT.md`.

Gate V1 completato: POOL +7456,21 medio contro parent, 14/14 positivi, ma
13/14 safety: rimane la morte Strawberry anche nel parent. NON promossa.
Report `reports/E18_30_DEVELOPMENT_SUMMARY_V1_20260906_IT.md`; source V1 congelata
in `artifacts/source/E18_30_MISSION_RUNTIME_V1.py` con SHA originale verificato.

## CROP_POOL V2 — ciclo colturale completo

Aggiunge missioni per PLANT→WATER già presenti consecutivamente nel piano quando
l'ETA dell'owner reale supera la deadline. Target vuoto/WEED, DIG se necessario,
semi osservati prenotati e percorso completo comprensivo di ritorno se richiesto.
Semina confermata prima di WATER; obbligo donor e fabbisogno semi riconciliati solo
dopo conferma. Nessuna nuova coltura né eccezione per D12, tile o seed.
ETA coerente con i cursori già avanzati e il comando baseline del batch.

44 test dedicati e 371 test complessivi pass. Gate contro E18.16: 14/14 delte
positive e safety pass, cassa 81.976 contro 74.491,57 (+10,05%), worst +4.471;
PASS 1090,29 contro 1568,07 (-30,47%), D15–D30 303,57 contro 734,71 (-58,68%),
MOVE +7,83%. Vittorie 5/14 contro 1/14 parent. E18.2 smoke: +9.156 rispetto al
parent, ma ancora 0/2 vittorie. Zero crop/animal deaths, errori o missioni incomplete
in tutti i 16 casi V2; nessuna diminuzione giornaliera di WATER/FEED/CARE eseguiti.

Standalone `submission/submission_codex_e18_30_770.py`, SHA-256
`5c47e641aed7d2e619a356a187654f3fe2bfaed3e1302c5f978d2ee742ce01de`:
quattro casi, 2.876 batch identici source/bundle e 2.876 via file-loader Kaggle.
NON pubblicata, non incumbent promosso, nessun holdout consumato. Si tratta della
prima migrazione ibrida delle code legacy, non della risoluzione globale dei PASS.
HIRE/payroll e generazione CARE/HARVEST restano tranche separate.

Risultati, decomposizione economica, limiti e prossime verifiche:
`reports/E18_30_RUNTIME_V2_CONSOLIDATED_20260906_IT.md`.
