# Registro Top770 — utilizzo singolo per ciclo

Decisione del proprietario, 2026-09-06. Registro comune, non specifica strategica
di un agente. Identità pubbliche conservate qui per evitare duplicati; nei
grafici usare alias Top770 numerati e non cambiare silenziosamente identità.

## Regola anti-riutilizzo

Un benchmark è un autore/strategia con submission e corpus congelati. Dopo
l'apertura dei dettagli è **esposto**, non holdout. Può alimentare il suo
unico ciclo diagnostico; alla chiusura non va riutilizzato per confrontare
nuove release, nemmeno cambiandone alias o scaricando altri episodi dello
stesso autore. Conservarne le ipotesi generali e la provenienza storica.
Una nuova submission dello stesso autore non azzera automaticamente l'esposizione.

La rotazione riduce il riutilizzo, ma non elimina da sola l'overfitting:
sviluppo sui controlli interni, verifica pubblica su avversari diversi e
separazione dei dati di selezione, diagnosi e validazione rimangono necessari.
Non scegliere il riferimento in base a un risultato favorevole alla candidata.

| Alias / identità | Stato | Evidenza / utilizzo |
|---|---|---|
| Top770-001 — Jesse Bullard | CONSUMATO; escluso da nuove release | Corpus storico 105405557, 105384058, 105398563, 105391568, 105565293; submission storica 55994794. Report E18.31 V4 solo chiusura documentale, non nuova validazione |
| Crop Dusta | GIÀ ESPOSTO; non candidato vergine | Analisi strategiche e topology-matched E18.6 precedenti; non assumere 770 stabile nelle nuove versioni |
| Giulio Ravasio | GIÀ ESPOSTO; non candidato vergine | Benchmark Top3 precedenti; escluso dal prossimo confronto indipendente |
| 3정훈 e sbol ball | GIÀ ESPOSTI; non candidati vergini | Analisi `E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_IT.md` |
| Top770-002 — Marlubie | CONSUMATO; unico ciclo diagnostico E18.31 del 2026-09-06 concluso | Submission 56044235; cinque replay congelati, quattro 770. Conservare le ipotesi generali; non riutilizzare per valutare release successive |

## Screening corrente — 2026-09-06

Classifica letta durante la sessione, non congelata artificialmente: i ranghi
cambiano mentre arrivano gli scontri. Presi i leader non già utilizzati, in
ordine osservato al momento della selezione; nessun filtro economico. Con due
non-770 nei primi tre casi è impossibile raggiungere 4/5, quindi screening
interrotto a tre. I casi seguenti sono **screening già esposti**, non riserve
di benchmark vergini. Conteggi non sommabili: uno stesso episodio può comparire
nella cronologia di entrambi gli avversari.

| Autore | Submission selezionata | Finali 770 / esaminati | Esito |
|---|---:|---:|---|
| keiz | 56036783 | 0/3 | Escluso |
| Mengfei Li | 56047440 | 0/3 | Escluso; anche riduzioni dei pascoli in chiusura |
| Syed Asad Ali | 56041453 | 1/3 | Escluso |
| Aastik Rajan15 | 56044391 | 3/5 | Escluso; alterna 770 e 10-7-0 |
| Lyesterday | 56040121 | 3/5 | Escluso; alterna 770 e 10-7-0 |
| CemBas | 56027043 | 3/5 | Escluso; alterna 770 e 10-7-0 |
| Dresden | 56044774 | 3/5 | Escluso; alterna 770 e 10-7-0 |
| Andrey Tikhomirov | 55995741 | 0/3 | Escluso |
| mikelou1 | 56045229 | 1/3 | Escluso |
| Agent 0 | 56046775 | 0/3 | Escluso |
| JianYuan Deng | 56042415 | 1/3 | Escluso |
| Milan Leonard | 56044802 | 0/3 | Escluso |
| Atakan Aldemir | 56013009 | 1/3 | Escluso |
| Marlubie / Top770-002 | 56044235 | 4/5 | Primo candidato che supera il criterio |

Top770-002 era tredicesimo / score 2760,1 nello snapshot precedente
all'apertura della sua cronologia. I cinque replay consecutivi selezionati:

| Episodio | Seat Top | Topologia finale | Checkpoint 770 D15–D30 | Uso |
|---|---:|---|---:|---|
| 106077622 | 0 | 7-7-0 | 16/16 | Report |
| 106076806 | 0 | 7-7-0 | 16/16 | Report |
| 106073019 | 1 | 7-7-0 | 16/16 | Report |
| 106068545 | 1 | 10-7-0 | 0/16 | Conservato, escluso dalle curve 770 |
| 106064835 | 1 | 7-7-0 | 16/16 | Report |

Il riferimento usa anche tre oche: 770 descrive i pascoli, non uguaglianza
del mix biologico. La stabilità è preliminare e condizionata al campione,
non garanzia universale né prova di superiorità causale.

Prossimi nomi non ancora aperti in questo ciclo: Zhongyi Dai, JamesJJJJJ,
c0nrad. Sono **candidati da verificare**, non Top770 già qualificati. Non aprire
i loro dettagli in anticipo: preservare un prossimo ciclo realmente nuovo.

Provenienza completa e corpus agente:
`docs/model_specs/codex/e18/artifacts/derived/E18_31_EXTERNAL_*SCREEN*.json`,
`E18_31_EXTERNAL_TOP002_FULL_20260906.json` e
`E18_31_PUBLIC_REPLAY_RECOVERY_CATALOG_20260906.json` nella stessa directory.

## Criterio di selezione preregistrato prima del nuovo corpus

Esaminare i nuovi leader in ordine di classifica, escludendo autori già
utilizzati in analisi approfondite. Screening iniziale: tre replay recenti
competitivi, esclusi self-play ed errori; se compatibili, estendere a cinque.
Per dichiarare stabilità preliminare: almeno quattro dei cinque finali con
tre quadranti attivi e pascoli 7-7-0; su tali replay almeno l'80% dei checkpoint
D15–D30 deve mantenere 7-7-0. Conservare anche i casi non conformi, senza
nasconderli nel denominatore. Preferire l'orientamento Q0=7/Q1=7/Q2=0/Q3=0.

Non usare cassa, PASS o somiglianza delle traiettorie alla candidata per
scegliere il vincitore dello screening. Cinque replay non provano una policy
fissa universale: documentare variabilità, eventuali quadranti aggiuntivi e
variazioni di mix. L'organico del benchmark è misurato, non imposto a 12.

La nostra release resta quella già verificata: 770 e massimo 12 manovali.
Le ipotesi estratte devono riguardare prerequisiti, capacità, valore economico
e scadenze, non quote/date copiate dal benchmark; devono essere valide anche
quando in futuro cambierà l'architettura.
