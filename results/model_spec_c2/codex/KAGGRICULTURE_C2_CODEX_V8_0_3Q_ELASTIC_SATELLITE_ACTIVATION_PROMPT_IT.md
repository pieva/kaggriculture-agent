# KAGGRICULTURE C2 — CODEX V8.0 3Q ELASTIC SATELLITE

## Mandato

Costruire, verificare e documentare una nuova candidata Codex a tre quadranti, derivata dalla V7.3 Dual-Q1 Cadence. Q0 e Q1 devono conservare geometria, ruoli, priorità e cadenza già validati; Q2 deve essere attivato come satellite produttivo elastico soltanto quando capitale, orizzonte biologico e capacità operativa ne dimostrano la sostenibilità.

Target centrale:

```text
FINAL_MONEY_MEAN >= 90000
```

La candidata deve rimanere isolata dalla submission canonica fino al superamento di tutti i gate. Solo dopo il superamento è autorizzata la generazione di `submission/submission_codex.py` e la rimozione delle altre varianti `submission_codex*.py` presenti esclusivamente nella cartella `submission`.

## Autorizzazioni

```text
TASK_TYPE: IMPLEMENTATION_LOCAL_VALIDATION_AND_SUBMISSION_BUILD
IMPLEMENTATION_AUTHORIZED: YES
LOCAL_REPLAY_AUTHORIZED: YES
BOUNDED_CAUSAL_ITERATION_AUTHORIZED: YES
DOCUMENTATION_AUTHORIZED: YES
CANONICAL_SUBMISSION_REPLACEMENT_AUTHORIZED_AFTER_GATES: YES
REMOVE_OTHER_CODEX_SUBMISSIONS_AFTER_GATES: YES
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
FOUNDATION_MODIFICATION_AUTHORIZED: NO
ENGINE_MODIFICATION_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_EXECUTION_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

## Baseline obbligatoria

Usare come baseline comportamentale congelata:

- controller: `src/agricola/strategy/codex_dual_q1_cadence.py`;
- config: `configs/model_spec_c2/CODEX_C2_DUAL_Q1_CADENCE_CONFIG.json`;
- risultati: `results/model_spec_c2/codex/CODEX_V7_3_Q1_CADENCE_RESULTS.json`;
- report: `results/model_spec_c2/codex/CODEX_V7_3_Q1_CADENCE_FINAL_REPORT_IT.md`.

Metriche V7.3:

```text
FINAL_MONEY_MEAN: 78036.17
FINAL_MONEY_MEDIAN: 77481.00
FINAL_MONEY_MIN: 71771.00
FINAL_MONEY_MAX: 88397.00
Q0_CROP_UNITS_MEAN: 137.17
Q1_CROP_UNITS_MEAN: 85.83
TOTAL_CROP_UNITS_MEAN: 223.00
MILK_MEAN: 146.17
WOOL_MEAN: 109.17
ANIMAL_ESCAPES_TOTAL: 0
MOVE_PER_PRODUCTIVE_ACTION: 3.0163
Q1_ACTIVATION_DAY_MEAN: 8.00
Q1_FULL_MODULE_DAY_MEAN: 11.00
Q1_FIRST_OUTPUT_DAY_MEAN: 13.00
```

## Vincolo economico determinante

La capacità non deve essere dimensionata per analogia nominale. Con 12 hands la spesa giornaliera è 376; la tredicesima hand aggiunge 233 al giorno e la quattordicesima aggiunge altri 377. Sei ulteriori hands porterebbero il costo giornaliero totale a 6.764, rendendo una copia completa di Q0/Q1 economicamente non recuperabile.

Q2 deve quindi usare:

```text
2 HANDS AGGIUNTIVE AL MASSIMO
1 OWNER LIVESTOCK/FEED Q2
1 OWNER CROP/SERVICE Q2
ASSISTENZA DEL FARMER E DEI LOGISTICS Q0/Q1 SOLO DOPO LE URGENZE LOCALI
```

## Architettura V8.0

### Q0 e Q1 — nucleo congelato

Non modificare il comportamento V7.3 dei due moduli esistenti:

- 18 crop, 3 cow, 3 sheep e 6 pasture per quadrante;
- W0 relief/logistics globale;
- W1–W6 owner Q0;
- W7–W12 owner Q1;
- FEED ownership invariata;
- W12 può assistere Q1 soltanto su ANIMAL_COLLECTION e CARE, come in V7.3;
- nessuna sottrazione ordinaria di capacità a Q0/Q1.

### Q2 — satellite SW elastico

Q2 usa il quadrante SW, costo terra 2.000. Il footprint iniziale deve essere compatto e dimensionato su capacità realmente osservabile:

- massimo 12 asset produttivi nel core iniziale;
- ciclo 1 diagnostico: 12 MELON crop-only;
- ciclo 2 ammesso dopo il fallimento economico del ciclo 1: 6 COW + 6 SHEEP;
- W13 owner FEED/livestock Q2;
- W14 owner crop/service Q2;
- nessuna espansione automatica a 18 crop senza un nuovo gate positivo;
- mix produttivo scelto con attenzione alla saturazione osservata;
- preferire la diversificazione soltanto se supportata da replay causali e non a costo di una regressione del nucleo.

L’implementazione può ridurre footprint o livestock target se il ledger dimostra che la versione completa non è ripagabile o non è serviceable.

Il ciclo 1 crop-only è stato respinto: 31 MELON Q2 hanno portato il prezzo terminale del prodotto a 10 e ridotto il denaro finale del replay diagnostico da 88.397 a 83.046. Il ciclo 2 con dodici asset livestock e una hand aggiuntiva è stato respinto dal ledger prima dell'acquisto: il netto proiettato era 7.524–9.142, sotto il floor 12.000. Il ciclo 3 mantiene 6 COW + 6 SHEEP ma elimina il costo marginale. Dopo il primo replay W6/W12, la verifica conclusiva di capacità suddivide Q2 in quattro sottocluster da tre animali assegnati a W0, W6, W9 e W12; gli owner FEED Q0/Q1 restano invariati e CARE/COLLECTION Q2 restano subordinati alle urgenze del nucleo.

La verifica di capacità successiva usa la proprietà engine esplicita `consecutive_unfed`: Q2 viene alimentato quando il contatore osservato è 1, quindi a cadenza massima sicura alternata; Q0/Q1 conservano FEED giornaliero. Questo libera fasi Q2 per CARE e COLLECTION senza ammettere fughe.

## Gate di attivazione Q2

Finestra obiettivo: D10–D12. Dopo D12 non acquistare Q2.

```text
OWNED_QUADRANTS = 2
Q1_FULL_MODULE = YES
Q0_Q1_ANIMAL_ESCAPES = 0
Q0_Q1_HARD_TASKS_SERVICEABLE = YES
CASH_PLUS_SELLABLE_INVENTORY >= 5500
OPERATING_BUFFER_AFTER_LAND > 0
REMAINING_HORIZON >= 18 DAYS
PROJECTED_Q2_NET_CONTRIBUTION >= 12000
PROJECTED_Q2_INCREMENTAL_LABOR_COST <= 9000
```

Registrare nel ledger ogni decisione di ammissione con giorno, cassa, inventario vendibile, costo terra, salario marginale proiettato, primo output, contributo netto stimato ed esito.

La soglia di liquidità è calibrata sul replay diagnostico completo: al D12 i sei episodi canonici mostrano disponibilità tra 5.722 e 6.519, mentre il payback Q2 proiettato resta superiore a 22.000. Il buffer 5.500 ammette il satellite senza rimuovere i gate di orizzonte, payback o serviceability.

## Serviceability Q2

1. W13 deve poter chiudere il set FEED Q2 con pickup batch e commitment composto serviceable.
2. W14 deve chiudere WATER/PLANT/HARVEST hard del core crop entro la capacità giornaliera.
3. CARE e ANIMAL_COLLECTION non possono precedere FEED dovuto.
4. W0, W6 e W12 possono assistere Q2 solo dopo la chiusura delle rispettive urgenze Q0/Q1.
5. Vietare target duplicati, cross-quadrant assist ordinario e movimenti verso interazioni illegalmente non serviceable.
6. In caso di roster incompleto, degradare il footprint Q2; non sottrarre owner a Q0/Q1.
7. Il controller deve restare fail-closed: zero errori tecnici e zero fallback.

## Gate di accettazione

### Gate tecnico ed economico minimo

```text
TECHNICAL_PASS: YES
ERRORS: 0
FALLBACKS: 0
ANIMAL_ESCAPES_TOTAL: 0
FINAL_MONEY_MEAN >= 88000
FINAL_MONEY_MIN >= 78000
Q2_NET_CONTRIBUTION > 0
Q0_CROP_REGRESSION <= 3%
Q1_CROP_REGRESSION <= 3%
MOVE_PER_PRODUCTIVE_ACTION <= 3.50
```

### Target centrale obbligatorio per la submission

```text
FINAL_MONEY_MEAN >= 90000
FINAL_MONEY_MIN >= 82000
Q2_NET_CONTRIBUTION >= 12000
Q0_CROP_REGRESSION <= 3%
Q1_CROP_REGRESSION <= 3%
ANIMAL_ESCAPES_TOTAL = 0
MOVE_PER_PRODUCTIVE_ACTION <= 3.30
TECHNICAL_PASS: YES
```

Se il target centrale non è raggiunto, non sostituire la submission canonica e non eliminare alcun file.

## Protocollo di verifica

Usare senza selezione post-hoc:

```text
SEEDS: 26090101, 26090102, 26090103
SEATS: 0, 1
OPPONENT: INERT_PASS_POLICY
EPISODE_STEPS: 720
TURNS_PER_DAY: 24
EPISODES: 6
```

Confrontare ogni episodio con la corrispondente V7.3. Conservare tutti i run, inclusi gli outlier. Sono ammessi al massimo tre cicli causali. Ogni ciclo deve cambiare un solo meccanismo dichiarato e misurare almeno:

- denaro finale e delta appaiato V7.3;
- costo terra, animali, seed, feed e salari marginali Q2;
- giorno di attivazione, giorno di completamento e primo output Q2;
- produzione e ricavi separati Q0/Q1/Q2;
- FEED/CARE/COLLECT e crop hard per quadrante;
- fughe, deadline miss, MOVE, PASS e productive actions;
- realized price per prodotto e segnali di cannibalizzazione.

## Artefatti richiesti

- `src/agricola/strategy/codex_3q_elastic.py`;
- `configs/model_spec_c2/CODEX_C2_3Q_ELASTIC_CONFIG.json`;
- `tests/test_codex_3q_elastic.py`;
- `scripts/benchmark_codex_3q_elastic.py`;
- `results/model_spec_c2/codex/CODEX_V8_0_3Q_RESULTS.csv`;
- `results/model_spec_c2/codex/CODEX_V8_0_3Q_RESULTS.json`;
- `results/model_spec_c2/codex/CODEX_V8_0_3Q_FINAL_REPORT_IT.md`;
- builder e verifier standalone dedicati;
- `submission/submission_codex.py`, solo dopo il superamento del target centrale.

## Consolidamento submission

Dopo il superamento dei gate:

1. costruire la V8.0 standalone in `submission/submission_codex.py`;
2. verificare import isolato senza package `src` e parità esatta delle 719 decisioni sui sei replay canonici;
3. elencare e validare i path assoluti di `submission/submission_codex*.py`;
4. eliminare esclusivamente le altre varianti Codex nella cartella `submission`;
5. non modificare né eliminare submission Antigravity o file non Codex;
6. verificare che il solo file corrispondente al pattern sia `submission_codex.py`.

## Blocco finale obbligatorio

```text
CANDIDATE_VERSION: <value>
Q0_Q1_CORE_PRESERVED: YES | PARTIAL | NO
Q2_ACTIVATION_DAY_MEAN: <value>
Q2_FULL_MODULE_DAY_MEAN: <value>
Q2_FIRST_OUTPUT_DAY_MEAN: <value>
FINAL_MONEY_MEAN: <value>
FINAL_MONEY_MEDIAN: <value>
FINAL_MONEY_MIN: <value>
FINAL_MONEY_MAX: <value>
DELTA_VS_V7_3: <value>
Q2_NET_CONTRIBUTION: <value>
Q0_CROP_UNITS_MEAN: <value>
Q1_CROP_UNITS_MEAN: <value>
Q2_CROP_UNITS_MEAN: <value>
ANIMAL_ESCAPES_TOTAL: <value>
MOVE_PER_PRODUCTIVE_ACTION: <value>
OBJECTIVE_88000_REACHED: YES | NO
OBJECTIVE_90000_REACHED: YES | NO
TECHNICAL_PASS: YES | NO
SUBMISSION_PARITY: YES | NO
ONLY_CANONICAL_CODEX_SUBMISSION_REMAINS: YES | NO
PRIMARY_REMAINING_BOTTLENECK: <value or NONE>
NEXT_STEP: FREEZE_V8_0 | ONE_MORE_CAUSAL_ITERATION | REJECT_3Q
TOURNAMENT_AUTHORIZED: NO
KAGGLE_EXECUTION_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

## STOP

Dopo report, build e verifica della submission fermarsi. Non eseguire torneo o upload Kaggle, non creare commit e non eseguire push.
