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


## 2026-09-07 — richiesta esplicita di report storico V4C/Top770

Riutilizzati i corpus congelati Top770-001 e Top770-002 solo per il report
storico descrittivo V4C, richiesto dal proprietario. Nessuna nuova release
valutata, nessun nuovo episodio acquisito, nessun ripristino dello stato
holdout. Avversario V4C INERT_PASS e topologia 7-7-5 dichiarati nel report.


## 2026-09-07 — nuova 770 assistita D1–D30 contro i Top già utilizzati

Riuso esplicitamente richiesto dal proprietario degli stessi cinque replay
Top770-001 e quattro Top770-002 selezionati nel report V4C. Nessun nuovo
episodio esterno acquisito; nessun ripristino dello stato holdout. Nuova 770
assistita V1 congelata misurata localmente per D1–D30 contro V4D, 7 semi di
sviluppo e entrambe le posizioni. Il report separa le curve storiche esterne
dal confronto diretto locale, senza dedurre un ranking dai ricavi fra corpus.
Report in `docs/model_specs/codex/e19/reports/assisted_770_top770_d30_20260907/`.


## 2026-09-07 — formato completo richiesto per la nuova 770

Il proprietario ha indicato E18_27_TOP770_D01_D30_COMPLETE_KPI.html come
riferimento di presentazione. Rigenerati i report nel formato V4.1, 22 pannelli,
un confronto separato per Top770-001 e Top770-002. Stessi corpus esposti,
nessun nuovo episodio pubblico. Riprodotti i medesimi 14 run locali per
completare i KPI operativi H24, verificando la parità dei risultati precedenti.


## 2026-09-08 — ciclo V48 e analisi per fasi

V48 congelata e pubblicata prima del confronto. Esclusi tutti gli autori
consumati/esposti elencati sopra, comprese le righe dello screening precedente.
I seguenti autori sono ora ESPOSTI per il ciclo V48; non sono holdout per release future.
La selezione segue l'ordine osservato durante lo screening, con classifica variabile.

| Autore | Submission | Corpus congelato | Stato |
|---|---:|---|---|
| SpaTaro | 56089825 | 106824217, 106817281, 106815633 | ESPOSTO; screening o analisi esplorativa |
| Otter Vibe | 56097405 | 106831672, 106830724, 106829767 | ESPOSTO; screening o analisi esplorativa |
| binghua | 56092906 | 106828029, 106821108, 106818377 | ESPOSTO; screening o analisi esplorativa |
| Matthew Huang | 56096542 | 106829776, 106828804, 106824954, 106823287, 106818211 | ESPOSTO; screening o analisi esplorativa |
| Ad Space Available | 56058327 | 106829767, 106827849, 106825938 | ESPOSTO; screening o analisi esplorativa |
| Tarang222 | 56091994 | 106829955, 106829522, 106825688 | ESPOSTO; screening o analisi esplorativa |
| THUNDER THUNDER | 56089409 | 106833660, 106824849, 106819193 | ESPOSTO; screening o analisi esplorativa |
| carbonapi | 56092842 | 106828023, 106820397, 106820129 | ESPOSTO; screening o analisi esplorativa |
| Suliman Tadros | 56082927 | 106831569, 106829740, 106824940 | ESPOSTO; screening o analisi esplorativa |
| kwa | 56071845 | 106833694, 106825206, 106824970 | ESPOSTO; screening o analisi esplorativa |
| JustinLee | 56065461 | 106833569, 106833660, 106830724 | ESPOSTO; screening o analisi esplorativa |
| Subin An | 56098520 | 106835267, 106834322, 106833359, 106832424, 106831443 | Top770-003; 4/5 finali 770, 16/16 checkpoint per ciascuno dei quattro; CONSUMATO nel ciclo diagnostico V48 |

Il quinto replay di Top770-003 (106835267, 10-7-0) è conservato ed è incluso nel
report del corpus completo. Matthew: 3/5 finali 770, non qualificato dal criterio storico.
Suliman: 10-7-0 in 3/3, alternativa esplorativa, non prova di superiorità.

Su richiesta successiva del proprietario aggiunta analisi D15, moda D15-D25,
sblocco/utilizzo Q2 e D30. Questo criterio aggiunto non è retroattivamente
preregistrato e non sostituisce silenziosamente il criterio finale originario.
Un solo nuovo autore Top770 qualificato, non dodici nuovi Top770.
Gli avversari incidentali nei replay sono stati visibili nello screening:
la loro presenza non qualifica nuovi alias né va trattata come cecità completa.

Report: docs/model_specs/codex/e19/reports/new_top_v48_20260908/REPORT_NUOVI_TOP_V48_IT.html
Quattro report da 22 KPI: Top770-003 filtrato n4, corpus completo n5, Matthew n5,
Suliman n3. Confronto V48 locale n6, non appaiato a questi replay esterni.
Nessuna nuova policy, nessuna 662, nessuna ulteriore submission.


## Esposizione avversari V48 — coorte 38 del 2026-09-08

38 replay contro altri giocatori (30 nuovi), cutoff 106869264. Gli avversari elencati sono osservati e analizzati: non sono una nuova coorte Top770 qualificata e non vanno riutilizzati come holdout indipendente.

Aditya Kapadia; Aditya Mishra; Attension_Seeker; Bibek; Dandan Li; DataLover; DeokJin; Hafida Belayd; Jia Chen; Kaggler Albafica; Kanny912; Kenny; LittleScottyy; MD.Firoj Khondokar; MOHSIN525; Nguyễn Nhật Thanh; Nikola010; PRITIKA SA; Peter Thompson; Rheal Thomas; SanggeunParrk; Sarah Ng; Shane Thivaharraja; Sidharth Hulyalkar; Singaraj B; Terrance Luangrath; Tita Kongolo; Udbhaw Anand; Udit Jain #2; Yihan Guo; eternitywinner; huanghaoyu7280; lava; my; ricardo; typeIIIfairy; コーラ.

Report: `docs/model_specs/codex/e19/reports/v48_external_pass_update_20260908/REPORT_V48_REPLAY_PASS_IT.html`.
