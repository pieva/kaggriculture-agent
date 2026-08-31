# KAGGRICULTURE C2 — CODEX FORENSIC AG vs V7 SERVICEABILITY AND ROUTING

## Mandato
Eseguire una forensic comparison mirata, senza modificare codice o policy, per spiegare:
1. perché Codex V7 ha 4 fughe animali per episodio mentre AG Q0 3+3 produce circa 93 MILK / 74 WOOL;
2. perché Codex V7 richiede 3,192 MOVE per productive action nonostante ruoli persistenti, zone locali e commitment atomico.

Obiettivo: identificare pochi meccanismi concreti e verificabili che permettano di preservare il successo crop di Codex e recuperare la serviceability livestock di AG. Non proporre un redesign generale.

## Vincoli
TASK_TYPE: READ_ONLY_FORENSIC_ANALYSIS
IMPLEMENTATION: NOT AUTHORIZED
MODEL_SPEC: DO NOT MODIFY
FOUNDATION: DO NOT MODIFY
DLC: DO NOT MODIFY
TOURNAMENT: NOT AUTHORIZED
KAGGLE: NOT AUTHORIZED
COMMIT: NOT AUTHORIZED
PUSH: NOT AUTHORIZED

Non eseguire tuning. Ammessi lettura codice/report, trace analysis, diagnostica breve indispensabile e replay locali deterministici degli episodi già eseguiti solo per estrarre trace mancanti.

## Fonti
Codex V7:
- results/model_spec_c2/codex/CODEX_COMPACT_Q0_ROUTINE_BUILD_REPORT.md
- results/model_spec_c2/codex/CODEX_COMPACT_Q0_ROUTINE_RESULTS.csv
- controller/config/telemetry effettivi V7.

Metriche canoniche:
FINAL_MONEY_MEAN 39265.67
MELON 95.00
STRAWBERRY 40.17
MILK 28.17
WOOL 14.67
ANIMAL_ESCAPES 24 total = 4/run
MOVE_PER_PRODUCTIVE_ACTION 3.1923
PRODUCTIVE_UTILIZATION 67.43%
ON_TIME_CROP_SERVICE_RATIO 79.49%
RETARGET_PER_WORKER_DAY 0.04769
PASS 871.5/run
ROLE_CHANGES 0
DUPLICATE_ASSIGNMENTS 0

Antigravity Q0 3+3:
- recuperare evidenze canoniche da results/model_spec_c2/antigravity/
- verificare sui file: FINAL_MONEY_MEAN ~37997.67, MILK ~93, WOOL ~74, TOTAL_CROP_UNITS ~24.7.
- recuperare controller/config AG della replica se disponibile.

## Analisi obbligatorie

### 1. Animal Escape Timeline
Per ciascuna delle 24 fughe V7 ricostruire:
episode/seed/seat; species; animal id/tile; activation day; first unfed boundary; second unfed/escape boundary; assigned worker; worker positions; committed target; pending livestock/crop/logistics tasks; slack; interrupt; FEED request/effect; causa concreta del mancato FEED.

Primary cause taxonomy:
NO_FEED_AVAILABLE
FEED_NOT_STAGED
WORKER_TOO_FAR
ROUTE_ORDER_ERROR
TASK_COMMITMENT_BLOCKED
INTERRUPT_TOO_LATE
CAPACITY_ADMISSION_ERROR
INVENTORY_HANDLING_DELAY
TARGET_RESERVATION_ERROR
LEGALITY_STATE_ERROR
OTHER

Produrre conteggi per causa.

### 2. Livestock Cadence AG vs Codex
Confrontare FEED requests/effects/on-time, CARE requests/effects/on-time, MILK/WOOL collection, mean/median/max MOVE per livestock service, due-to-effect delay, pending livestock tasks a EOD.
Non fermarsi a “Codex misses FEED”: spiegare perché.

### 3. Worker Geometry
Per worker livestock Codex misurare distance/day, distance per FEED/CARE/COLLECT, shed returns, cross-cluster trips, backtracking, empty repositioning. Confrontare AG quando possibile. Cercare pattern pasture→shed→pasture e simili.

### 4. MOVE Decomposition by Role
Ruoli:
CROP_ZONE_0
CROP_ZONE_1
CROP_ZONE_2
LIVESTOCK_COW
LIVESTOCK_SHEEP
FERTILIZER_LOGISTICS
FLOAT_RESERVE

Per ruolo: MOVE, productive actions, MOVE/productive, PASS, target count, mean target distance, cross-zone assists.
Identificare PRIMARY_MOVE_SOURCE dei 2196.83 MOVE/run.

### 5. Route Optimality
Su campione rappresentativo calcolare:
ROUTE_STRETCH = actual MOVE / minimum feasible MOVE
per crop, livestock, fertilizer/logistics, float. Non serve TSP globale.

### 6. PASS Diagnosis
Classificare:
NO_LEGAL_TASK
WAITING_FOR_COMMITTED_TARGET
WAITING_FOR_BIOLOGICAL_EVENT
NO_LOCAL_TASK_BUT_GLOBAL_TASK_EXISTS
RESERVE_IDLE
INVENTORY_BLOCK
ROUTE_STATE_BUG
OTHER

Separare slack sano da capacità inutilizzata mentre esistono task utili.

### 7. Cross-Zone Assists
V7: ~51.67/run. Determinare chi assiste chi, task, distanza, deadline protetta, eventuale deadline persa nella zona originaria. Valutare FLOAT_RESERVE.

### 8. Capacity Admission
V7: 64 rejection, 14 admission, 3+3 prevalentemente day13, 24 escapes.
Per ogni animal admission confrontare predicted vs observed required actions, route MOVE e slack.
Classificare:
BAD_CAPACITY_ESTIMATE
BAD_ROUTE_ESTIMATE
UNMODELED_FEED_LOGISTICS
UNMODELED_COLLECTION
UNMODELED_INTERRUPT
OTHER

### 9. AG Mechanisms Worth Importing
Verificare, senza assumere: earlier FEED dispatch, worker positioning, pasture ordering, commitment, WHEAT staging, inventory policy, service priority, livestock interrupt, fertilizer/logistics contention.
Per ciascuno:
AG_BEHAVIOR
CODEX_BEHAVIOR
OBSERVED_EFFECT
LIKELY_CAUSALITY HIGH|MEDIUM|LOW

### 10. Crop Preservation
Preservare almeno MELON ~95 e STRAWBERRY ~40. Per ogni fix:
CROP_REGRESSION_RISK LOW|MEDIUM|HIGH.
Non spostare semplicemente capacità dalle crop al livestock.

### 11. Minimal Correction Set
Massimo 3 correzioni, specifiche e meccanicamente giustificate.
Preservare salvo prova di impossibilità:
Q0; 18 crop; 9 MELON; 8 STRAWBERRY; 1 WHEAT; 6 pasture; 3 COW; 3 SHEEP target; 7 workers.
Per fix:
MECHANISM
EXPECTED_EFFECT
METRIC_AFFECTED
CROP_REGRESSION_RISK
CONFIDENCE

### 12. Counterfactual Economics
Stimare LOW/CENTRAL/HIGH Final Money se crop V7 resta invariato e livestock recupera livello AG. Considerare replacement evitati, MILK/WOOL aggiuntivi, feed, handling, crop opportunity cost. Non sommare gross revenue ingenuamente. È diagnostica, non benchmark.

## Output
Creare SOLO:
results/model_spec_c2/codex/CODEX_V7_AG_SERVICEABILITY_FORENSIC.md

CSV opzionali solo se necessari:
CODEX_V7_ANIMAL_ESCAPE_TRACE.csv
CODEX_V7_ROLE_EFFICIENCY.csv

## Struttura report
1. Executive Finding
2. Sources and Reproducibility
3. AG vs Codex Production Contrast
4. Animal Escape Timeline
5. Escape Root Causes
6. Livestock Service Cadence
7. Worker Geometry
8. MOVE Decomposition by Role
9. PASS Decomposition
10. Cross-Zone Assist Analysis
11. Capacity Admission Accuracy
12. AG Mechanisms Worth Importing
13. Crop Preservation Constraints
14. Minimal Correction Set
15. Counterfactual Economic Range
16. Final Verdict

Chiudere con:

PRIMARY_ESCAPE_CAUSE: <value>
SECONDARY_ESCAPE_CAUSE: <value or NONE>
PRIMARY_MOVE_SOURCE: <role/mechanism>
PRIMARY_PASS_SOURCE: <role/mechanism>
CAPACITY_ADMISSION_ACCURATE: YES | PARTIAL | NO
AG_LIVESTOCK_ADVANTAGE_EXPLAINED: YES | PARTIAL | NO
CODEX_CROP_ADVANTAGE_TO_PRESERVE: YES
MINIMAL_FIX_COUNT: 1 | 2 | 3
FIX_1: <value>
FIX_2: <value or NONE>
FIX_3: <value or NONE>
EXPECTED_LIVESTOCK_RECOVERY: <value>
CROP_REGRESSION_RISK: LOW | MEDIUM | HIGH
COUNTERFACTUAL_FINAL_MONEY_LOW: <value>
COUNTERFACTUAL_FINAL_MONEY_CENTRAL: <value>
COUNTERFACTUAL_FINAL_MONEY_HIGH: <value>
NEXT_STEP: MINIMAL_V7_CORRECTION_BUILD | MORE_FORENSIC_REQUIRED | ARCHITECTURE_REOPEN_REQUIRED
IMPLEMENTATION_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO

## STOP
Dopo la forensic fermarsi. Non implementare correzioni, non modificare MODEL_SPEC, non fare tuning, tournament, Kaggle, commit o push.
