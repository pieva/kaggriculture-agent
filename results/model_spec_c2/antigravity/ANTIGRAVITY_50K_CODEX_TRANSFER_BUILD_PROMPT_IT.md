# KAGGRICULTURE C2 — ANTIGRAVITY 50K CODEX TRANSFER BUILD

## Mandato

Costruire e verificare localmente una nuova candidata **Antigravity C2** capace di superare una media di **50.000 Final Money**, trasferendo in modo selettivo le lezioni dimostrate dal passaggio Codex V7 → V7.1.

Non copiare integralmente il controller Codex e non indebolire i meccanismi nei quali Antigravity è già superiore. Lo scopo è combinare:

- la continuità livestock e la disciplina dei ruoli già dimostrate da Antigravity;
- la serviceability preventiva, la chiusura delle catene di inventario e la produttività crop dimostrate da Codex V7.1.

Il lavoro termina quando il gate economico e i gate tecnici definiti in questo prompt sono raggiunti e documentati, oppure quando le evidenze dimostrano con precisione perché non siano raggiungibili senza riaprire l'architettura.

## Autorizzazioni e limiti

```text
TASK_TYPE: IMPLEMENTATION_AND_LOCAL_VALIDATION
IMPLEMENTATION_AUTHORIZED: YES
LOCAL_DETERMINISTIC_REPLAY_AUTHORIZED: YES
BOUNDED_MECHANISTIC_ITERATION_AUTHORIZED: YES
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
FOUNDATION_MODIFICATION_AUTHORIZED: NO
DLC_MODIFICATION_AUTHORIZED: NO
ENGINE_MODIFICATION_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_UPLOAD_OR_RUN_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

Sono ammessi al massimo **tre cicli di correzione causale** dopo la prima implementazione. Non sono ammessi branch condizionali per seed, seat o episodio, ricerca casuale di parametri, selezione post-hoc dei soli run favorevoli o modifica dei prezzi/motore.

## 1. Fonti obbligatorie

### Evidenze Codex

Leggere prima di modificare codice:

- `results/model_spec_c2/codex/CODEX_V7_AG_SERVICEABILITY_FORENSIC.md`
- `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_FINAL_REPORT_IT.md`
- `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_RESULTS.csv`
- `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_RESULTS.json`
- `src/agricola/strategy/codex_compact_q0.py`
- commit di riferimento Codex: `beefae1`

### Evidenze Antigravity

- `results/model_spec_c2/antigravity/README.md`
- `results/model_spec_c2/antigravity/current/BUILD_VERIFICATION.md`
- `results/model_spec_c2/antigravity/experiments/Q0_3X3/LUCCC_EXACT_Q0_3COW_3SHEEP_REPLICATION.md`
- `results/model_spec_c2/antigravity/experiments/Q0_3X3/LUCCC_EXACT_Q0_3COW_3SHEEP_RESULTS.csv`
- `results/model_spec_c2/antigravity/experiments/ROUTINE_PLANNING/Q0_3X3_ROUTINE_WORKER_PLANNING_TEST.md`
- `results/model_spec_c2/antigravity/experiments/ROUTINE_PLANNING/Q0_3X3_ROUTINE_WORKER_PLANNING_RESULTS.csv`
- `results/model_spec_c2/antigravity/evidence/Q0_3X3_FORENSIC_GAP_ANALYSIS.md`
- `results/model_spec_c2/antigravity/evidence/LUCCC_PRODUCTION_AUDIT.md`
- controller, configurazione, test e build script Antigravity effettivamente presenti nel repository.

Non assumere che i moduli storici usati dagli esperimenti siano ancora disponibili. Identificare prima il controller Antigravity realmente eseguibile e separare con chiarezza:

1. baseline corrente pure horticulture;
2. evidenza storica Q0 3+3;
3. nuova candidata 50K.

## 2. Quadro comparativo canonico

### Antigravity corrente — pure horticulture 2Q

```text
FINAL_MONEY_MEAN: 43837.33
FINAL_MONEY_MIN_ON_REPORTED_SEEDS: 41548.00
FINAL_MONEY_MAX_ON_REPORTED_SEEDS: 45266.00
CROP_TILES: 40
WORKERS: 10
ANIMALS: 0
PERFORMANCE_GATE_50000: FAIL
```

Questa baseline è tecnicamente solida e non deve essere sovrascritta fino a quando la nuova candidata non supera tutti i gate.

### Antigravity Q0 3+3 Control

```text
FINAL_MONEY_MEAN: 37997.67
TOTAL_CROP_UNITS: 24.70
MILK_CANONICAL_EVIDENCE: 93
WOOL_CANONICAL_EVIDENCE: 74
ANIMAL_ESCAPES: 0
MOVE_PER_PRODUCTIVE_ACTION: 4.82
```

### Antigravity Q0 3+3 Routine Planner

```text
FINAL_MONEY_MEAN: 39695.33
TOTAL_CROP_UNITS: 85.33
MELON: 62.00
STRAWBERRY: 14.33
MILK: 88.00
WOOL: 70.00
ANIMAL_ESCAPES: 0
FEED_COMPLIANCE: 100%
MOVE_PER_PRODUCTIVE_ACTION: 3.31
TARGET_SWITCHES_UNJUSTIFIED: 0
CROSS_ZONE_WANDERING: 0
```

Nota obbligatoria: alcuni documenti AG contengono una discrepanza tra unità livestock narrative e unità canoniche 93/74. Verificare i CSV e la telemetria effettiva della nuova candidata; non risolvere la discrepanza per assunzione.

### Codex V7 — baseline prima della correzione

```text
FINAL_MONEY_MEAN: 39265.67
TOTAL_CROP_UNITS: 135.17
MILK: 28.17
WOOL: 14.67
ANIMAL_ESCAPES: 24 TOTAL / 4 PER RUN
MOVE_PER_PRODUCTIVE_ACTION: 3.1923
```

### Codex V7.1 — dopo la correzione

```text
FINAL_MONEY_MEAN: 61118.83
FINAL_MONEY_MEDIAN: 61299.50
FINAL_MONEY_MIN: 57859.00
FINAL_MONEY_MAX: 64752.00
ALL_EPISODES_ABOVE_50000: YES
TOTAL_CROP_UNITS: 139.83
MELON: 103.00
STRAWBERRY: 36.83
MILK: 90.00
WOOL: 60.00
ANIMAL_ESCAPES: 0
PRODUCTIVE_ACTIONS: 858.00
MOVE_PER_PRODUCTIVE_ACTION: 3.0321
CROP_REVENUE: 30561.17
LIVESTOCK_REVENUE: 35288.00
```

Codex V7.1 migliora Final Money di **21.853,17 / 55,65%** rispetto a V7, elimina tutte le fughe e preserva la produzione crop.

## 3. Cosa ha fatto Codex per superare 50K

### 3.1 Forensic prima dell'implementazione

Codex ha ricostruito tutte le 24 fughe e ha dimostrato che:

- i quattro animali bootstrap fuggivano tutti a D5/S120;
- il deposito conteneva ancora 8 WHEAT;
- il problema non era stockout o distanza;
- W4/W5, proprietari livestock previsti, non esistevano nel giorno decisivo;
- FLOAT/CROP potevano inseguire un target FEED senza trasportare WHEAT;
- la legalità veniva controllata soltanto all'arrivo sul pascolo.

La causa primaria era `FEED_NOT_STAGED`; la causa secondaria era `LEGALITY_STATE_ERROR`.

### 3.2 SERVICEABLE_BOOTSTRAP_BINDING

Codex ha mantenuto i proprietari livestock ordinari quando presenti, ma ha introdotto ownership di emergenza quando il roster giornaliero era incompleto:

- farmer/FLOAT per il cluster COW;
- primo hand disponibile per il cluster SHEEP;
- farmer per entrambi i cluster quando era l'unico worker.

Il binding è limitato alla chiusura del servizio animale e non altera permanentemente i ruoli crop.

### 3.3 INVENTORY_AWARE_FEED_DISPATCH

Un worker non può più impegnarsi verso FEED se non trasporta WHEAT. In assenza di scorta personale il commitment diventa una catena esplicita:

```text
SHED → PICKUP WHEAT → PASTURE → FEED
```

La capacità viene verificata prima del movimento, evitando target remoti formalmente urgenti ma materialmente illegali.

### 3.4 FEED_FIRST_CLUSTER_BATCHING

Il worker preleva in una volta il WHEAT necessario al proprio cluster, alimenta tutti gli animali dovuti e solo dopo passa a CARE, raccolta prodotto, fertilizzante o ritorno al deposito.

Con roster completo, la raccolta ordinaria del fertilizzante viene affidata al ruolo logistico dedicato, riducendo l'abbandono dei cluster livestock.

### 3.5 Preservazione crop e verifica

Codex non ha modificato footprint, mix, coorti o zone colturali. Ha aggiunto test mirati, rigenerato la submission standalone, eseguito la suite completa e confrontato sei replay preregistrati sugli stessi seed/seat della baseline.

Il risultato non deriva quindi dal trasferimento indiscriminato di capacità crop verso il bestiame.

## 4. Diagnosi di trasferimento per Antigravity

Antigravity non presenta lo stesso difetto primario di Codex V7:

- la variante Routine conserva zero fughe;
- FEED compliance è già 100%;
- MILK 88 e WOOL 70 sono superiori a Codex V7.1 nel WOOL e comparabili nel MILK;
- i ruoli livestock AG occupano indici anticipati W1/W2 e sono meno esposti alla scomparsa dei temporary hands rispetto ai W4/W5 della vecchia V7.

Non sacrificare questi vantaggi. Il principale gap AG è altrove:

1. **Crop throughput insufficiente:** 85,33 unità Routine contro 139,83 Codex V7.1.
2. **Fragole sottoservite:** 14,33 contro 36,83.
3. **Fertilizzante non pienamente convertito in resa:** le evidenze AG mostrano surplus venduto o raccolto senza applicazione ottimale.
4. **Baseline eseguibile disallineata:** il controller corrente è pure horticulture 2Q, mentre il miglior meccanismo livestock è conservato soprattutto in evidenze/esperimenti storici.
5. **Architettura e metriche talvolta incoerenti nei report:** verificare l'effettivo conteggio delle 18 tile; 9 MELON + 8 STRAWBERRY + 1 WHEAT è un insieme coerente di 18 tile.

Per AG, il trasferimento opportuno non è “più feed”. È una **integrazione ad alta densità Q0** che preservi la sua continuità livestock e porti la serviceability crop al livello Codex.

## 5. Architettura candidata raccomandata

Usare come ipotesi primaria, da verificare e non da assumere automaticamente:

```text
TERRITORY: Q0 / NW ONLY
LAND_COST: 0
PRODUCTIVE_POSITIONS: 24
CROP_TILES: 18
PASTURES: 6
COW_TARGET: 3
SHEEP_TARGET: 3
WORKERS_TOTAL: 7
CROP_MIX: 9 MELON / 8 STRAWBERRY / 1 WHEAT
```

Ruoli raccomandati, preservando il Routine Planner AG:

| Worker | Ruolo | Responsabilità |
|---|---|---|
| W0 | RELIEF_LOGISTICS | shed, staging, assistenza hard realmente eseguibile |
| W1 | LIVESTOCK_COW | feed-first COW, care, milk collection |
| W2 | LIVESTOCK_SHEEP | feed-first SHEEP, care, wool collection |
| W3 | CROP_ZONE_0 | sei tile contigue, priorità WATER/HARVEST |
| W4 | CROP_ZONE_1 | sei tile contigue, priorità WATER/HARVEST |
| W5 | CROP_ZONE_2 | sei tile contigue, priorità WATER/HARVEST |
| W6 | FERTILIZER_LOGISTICS | raccolta concime e applicazione sulle crop irrigate |

Se il roster è incompleto, definire fallback deterministici che garantiscano sia il feed sia le deadline WATER, senza cambiare permanentemente ruolo.

## 6. Azioni di sviluppo richieste

### Azione 1 — Reconciliation e baseline eseguibile

Prima di implementare:

1. individuare quale controller Antigravity è oggi realmente importabile;
2. riprodurre la baseline corrente 43.837,33 sui seed canonici AG;
3. verificare se il Routine Planner storico può essere ricostruito da codice ancora presente senza inventare comportamento mancante;
4. se il codice storico non esiste, creare una candidata sperimentale isolata e non sovrascrivere il controller corrente;
5. produrre una tabella source-of-truth con configurazione, file, versione e metriche.

### Azione 2 — Portare la chiusura serviceability Codex senza degradare AG

Implementare o verificare esplicitamente:

- proprietario attivo per ogni cluster animale;
- fallback owner quando W1/W2 non sono presenti;
- FEED assegnabile solo con WHEAT trasportato o con commitment composto di pickup;
- prelievo batch sufficiente per tutti gli animali dovuti nel cluster;
- chiusura completa del due-feed-set prima di CARE/collection/fertilizer;
- nessun worker crop/FLOAT inviato verso FEED privo di scorta;
- nessuna vendita WHEAT che riduca la riserva sotto due round completi del bestiame attivo/staged.

Questi sono invarianti di sicurezza. Non devono essere il principale consumatore del budget di ottimizzazione, perché AG è già forte nel livestock.

### Azione 3 — Recuperare il gap crop

Applicare una routine crop deterministica:

1. tre zone contigue da sei tile;
2. ownership persistente e target reservation atomica;
3. ordine di servizio per perdita economica e deadline reale:
   - WATER che evita la perdita a EOD;
   - HARVEST a rischio terminale o yield cap;
   - WATER di completamento resa;
   - HARVEST maturo;
   - PLANT di coorte;
4. cross-zone assist solo quando la zona originaria non ha task pendenti;
5. niente rescan opportunistico che interrompa un target valido;
6. cohort planning che mantenga la semina serviceable prima dell'orizzonte finale;
7. nessun HARVEST prematuro.

Target intermedi:

```text
TOTAL_CROP_UNITS >= 110
STRAWBERRY_UNITS >= 28
MELON_UNITS >= 75
ON_TIME_CROP_SERVICE_RATIO >= 0.82
```

Questi valori sono inferiori al risultato Codex V7.1 e quindi plausibili, ma sufficientemente superiori alla Routine AG da colmare gran parte del gap economico.

### Azione 4 — Chiudere il ciclo fertilizzante

Il fertilizzante deve essere trattato come input produttivo prima che come merce da vendere:

- W6 raccoglie il fertilizzante senza sottrarre W1/W2 al feed;
- applicare solo a MELON/STRAWBERRY già irrigate e legalmente fertilizzabili;
- priorità MELON, poi STRAWBERRY in base al prossimo output monetizzabile;
- scaricare/vendere soltanto surplus non applicabile entro la finestra utile;
- misurare raccolto, applicato, venduto e incremento di yield attribuibile.

Gate:

```text
FERTILIZER_APPLIED >= 28 PER RUN
FERTILIZER_APPLICATION_NOOPS: 0
```

### Azione 5 — Cashflow e attivazione livestock

Non copiare automaticamente il giorno di attivazione Codex. Preservare il bootstrap AG provato, ma verificarne la serviceability:

- 2 COW + 2 SHEEP bootstrap solo se il feed owner è disponibile;
- espansione a 3+3 appena cash, WHEAT reserve e capacità osservata lo permettono;
- evitare Q1 e relativo costo terra nella candidata primaria;
- proteggere salari, seed delle coorti e almeno due round feed;
- vendere MILK/WOOL/crop con regola osservabile e senza bloccare lo shed;
- valutare market timing soltanto dopo aver superato i gate di produzione; nessun arbitraggio è necessario per dimostrare 50K.

### Azione 6 — Ridurre MOVE improduttivi

Misurare per ruolo:

- MOVE;
- azioni produttive;
- MOVE/produttiva;
- PASS con task globale disponibile;
- commitment abbandonati;
- ritorni shed;
- distanza per FEED/CARE/COLLECT/WATER/HARVEST;
- cross-zone assist.

Il pathfinding locale non basta. Ridurre sequenze macro come pasture→shed→pasture e zone→shed→stessa zona tramite batching e inventory staging.

Gate:

```text
MOVE_PER_PRODUCTIVE_ACTION <= 3.20
UNJUSTIFIED_TARGET_SWITCHES: 0
DUPLICATE_ASSIGNMENTS: 0
```

## 7. Piano sperimentale obbligatorio

### Fase A — Regressione Antigravity

Usare i seed canonici AG:

```text
1838889274
1619968655
710418712
```

Riprodurre la baseline eseguibile e verificare che il nuovo harness non alteri il comportamento osservato.

### Fase B — Valutazione candidata

Usare prima di osservare i risultati economici:

```text
SEEDS: 26090101, 26090102, 26090103
SEATS: 0, 1
OPPONENT: INERT_PASS_POLICY
EPISODE_STEPS: 720
TURNS_PER_DAY: 24
EPISODES: 6
```

Questa è la suite di confronto diretto usata per Codex V7/V7.1. Tutti i sei episodi devono essere conservati; non eliminare outlier.

### Fase C — Conferma sui seed AG

Dopo il superamento della Fase B, eseguire la nuova candidata sui tre seed canonici AG, preferibilmente su entrambi i seat. Riportare separatamente i due protocolli; non fondere le medie.

## 8. Gate di accettazione

### Gate obbligatori

```text
TECHNICAL_PASS: YES
UNHANDLED_ERRORS: 0
FALLBACKS: 0
INVALID_ACTIONS: 0
PLAYER_0_AND_PLAYER_1_SUPPORTED: YES
FINAL_MONEY_MEAN_PHASE_B >= 50000
FINAL_MONEY_MIN_PHASE_B >= 45000
ANIMAL_ESCAPES_TOTAL: 0
MILK_MEAN >= 85
WOOL_MEAN >= 65
TOTAL_CROP_UNITS_MEAN >= 110
MOVE_PER_PRODUCTIVE_ACTION <= 3.20
```

### Stretch target, non obbligatorio

```text
FINAL_MONEY_MEAN: 58000-62000
FINAL_MONEY_MIN: >=50000
MILK: 88-93
WOOL: 70-74
TOTAL_CROP_UNITS: 130-140
```

Il target minimo è raggiunto soltanto se la media dei sei episodi della Fase B supera 50.000. Un singolo run sopra soglia non è sufficiente.

## 9. Test richiesti

Aggiungere test specifici per:

1. binding di un feed owner per ogni cluster attivo;
2. impossibilità di routing FEED senza WHEAT o pickup composto;
3. batch pickup dimensionato sul due-feed-set;
4. precedenza FEED su unload/fertilizer secondari;
5. conservazione dell'ownership crop;
6. cross-zone assist soltanto con zona originaria libera;
7. fertilizzazione soltanto same-day-watered e legalmente eleggibile;
8. protezione della riserva WHEAT;
9. player-index independence;
10. equivalenza source/submission, se viene generata una standalone locale;
11. determinismo a parità di seed/seat;
12. zero regressioni nella suite completa del repository.

## 10. Regole di iterazione

Se il primo ciclo non raggiunge 50K:

1. decomporre il gap in crop revenue, livestock revenue, costi, MOVE e PASS;
2. identificare un solo meccanismo causale dominante;
3. applicare una modifica circoscritta;
4. rieseguire l'intera Fase B;
5. confrontare tutti i sei episodi con il ciclo precedente.

Ordine di priorità delle eventuali correzioni:

1. deadline WATER/HARVEST perse;
2. fertilizer non applicato;
3. inventario o shed blocking;
4. commitment abbandonati e ritorni shed;
5. market realization.

Non cambiare simultaneamente footprint, mix, numero lavoratori, livestock e market timing: renderebbe il risultato non attribuibile.

## 11. Artefatti finali

Produrre almeno:

- controller/config candidata in un percorso Antigravity chiaramente versionato;
- test dedicati;
- harness o aggiornamento controllato del benchmark;
- `results/model_spec_c2/antigravity/ANTIGRAVITY_50K_RESULTS.csv`;
- `results/model_spec_c2/antigravity/ANTIGRAVITY_50K_RESULTS.json`;
- `results/model_spec_c2/antigravity/ANTIGRAVITY_50K_FINAL_REPORT_IT.md`.

La baseline corrente e i suoi artefatti canonici devono rimanere disponibili e non essere sovrascritti.

## 12. Struttura del report finale

1. Esito esecutivo
2. Baseline e source-of-truth
3. Confronto Codex V7, Codex V7.1 e Antigravity
4. Architettura candidata
5. Meccanismi trasferiti da Codex
6. Meccanismi AG preservati
7. Modifiche implementate
8. Serviceability livestock
9. Serviceability crop
10. Fertilizer closed loop
11. MOVE e PASS decomposition
12. Risultati per seed e seat
13. Confronto economico
14. Test e riproducibilità
15. Rischi e limiti
16. Verdetto finale

Chiudere con il seguente blocco:

```text
AGENT_ID: ANTIGRAVITY
CANDIDATE_VERSION: <value>
EXECUTABLE_BASELINE_REPRODUCED: YES | NO
PHASE_B_EPISODES: 6
FINAL_MONEY_MEAN: <value>
FINAL_MONEY_MEDIAN: <value>
FINAL_MONEY_MIN: <value>
FINAL_MONEY_MAX: <value>
ALL_PHASE_B_RUNS_RETAINED: YES
ANIMAL_ESCAPES_TOTAL: <value>
MILK_MEAN: <value>
WOOL_MEAN: <value>
MELON_MEAN: <value>
STRAWBERRY_MEAN: <value>
TOTAL_CROP_UNITS_MEAN: <value>
FERTILIZER_COLLECTED_MEAN: <value>
FERTILIZER_APPLIED_MEAN: <value>
MOVE_PER_PRODUCTIVE_ACTION: <value>
PRIMARY_REMAINING_BOTTLENECK: <value or NONE>
CODEX_MECHANISMS_IMPORTED: <value>
AG_MECHANISMS_PRESERVED: <value>
OBJECTIVE_50000_REACHED: YES | NO
TECHNICAL_PASS: YES | NO
NEXT_STEP: FREEZE_CANDIDATE | ONE_MORE_CAUSAL_ITERATION | ARCHITECTURE_REOPEN_REQUIRED
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

## STOP

Quando il gate viene raggiunto e il report è completo, fermarsi. Non avviare torneo, non effettuare upload o run Kaggle, non creare commit e non eseguire push. Qualunque operazione successiva richiede una nuova autorizzazione esplicita.
