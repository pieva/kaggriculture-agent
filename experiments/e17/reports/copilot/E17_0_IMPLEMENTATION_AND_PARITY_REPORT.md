# E17.0 — Copilot native baseline, ledger e freeze report

- **Agent owner:** Copilot
- **Policy:** `COPILOT-E17.0-NATIVE-3Q-CROP-BASELINE-V1`
- **Deliverable:** `NATIVE_BASELINE_CONSTRUCTION_AND_LEDGER`
- **Opponent:** `INERT_PASS_POLICY`
- **Seed:** `26090101`, `26090102`, `26090103`
- **Seat:** `0`, `1`
- **Holdout consumato:** `false`
- **Final confirmation consumata:** `false`
- **E17.1 / ottimizzazione policy:** non implementate

## 1. Esito

```text
E17_0_COPILOT_STATUS: PASS
LEDGER_SCHEMA: E17_LEDGER_V1
LEDGER_RECORD_COVERAGE: 26163/26163 = 100%
TECHNICAL_ERRORS: 0
DERIVED_EOD_ESCAPE_COUNT: 0
THREE_QUADRANT_OPERATION: 6/6 PASS
DETERMINISTIC_REPRODUCIBILITY: 6/6 PASS
SOURCE_CONFIG_FREEZE: PASS
NO_IMPORT_OTHER_AGENT_ROUTINE: PASS
NO_COPY_OTHER_AGENT_ACTION_TABLE: PASS
NO_EXTERNAL_PLANNER_DISPATCHER_OR_SCHEDULE: PASS
ROUTINE_FINGERPRINT_DISTINCT: PASS
ACTION_PARITY_WITH_CODEX: NOT_APPLICABLE_BY_FROZEN_STRATEGY
STRATEGIC_INDEPENDENCE_LOCAL_AUDIT: PASS
LEVEL_D_INDEPENDENT_REVIEW: PENDING
```

La baseline è un controller crop-only reattivo allo stato: seleziona deterministicamente task `HARVEST → WATER → DIG → PLANT`, bilancia l'allocazione delle tile vuote fra NW/NE/SW e calcola i movimenti con una regola Manhattan propria. Non contiene una tabella di 719 azioni e non dipende da policy agent-local altrui.

## 2. Artefatti congelati

| Artefatto | SHA-256 |
|---|---|
| `src/agricola/strategy/copilot/e17_native_3q.py` | `1D0FD4268097EBC2C36B2C578AB34A8EE757A61BC3C72970604FE7007F2E4FCA` |
| `experiments/e17/configs/copilot/COPILOT_E17_0_NATIVE_3Q_V1.json` | `7691CF2010AC4BF5E6B36DB566C61B75043FF92EB5C98A6D94CC9DD6D1D9BFBE` |
| Native policy fingerprint | `315073D272A4EF38DA2E98AD1B559A2A3DC4A4C2C117CEC609DC377E324BCDAB` |
| Ledger neutrale `src/agricola/core/e17_ledger.py` | `A22C97584D4AE81A341485744C8AF0FFBBF14A9C9A8491BD3210FC768AD672C9` |
| Metriche aggregate | `38E76B74D3D4239FF5D2297FC6300926B5BCA310641ADA7B1834FB21F833648E` |
| Freeze manifest | `75C4749410407D04B228AB969EBF1ADBF7F9F3F4B35866AE263BBB3A471FB0BE` |

Le copie frozen di source e config sono byte-identiche ai rispettivi file attivi. Il manifest registra anche hash di runner, test, ledger, opponent e di tutti i 18 artefatti di run.

## 3. Matrice development

Ogni caso è stato eseguito due volte con lo stesso episode ID. Il secondo run è servito soltanto alla verifica di riproducibilità e non è stato aggiunto al denominatore sperimentale.

| Seed | Seat | Denaro finale | Batch | Record ledger | Q operati | Riproducibilità |
|---:|---:|---:|---:|---:|---|---|
| 26090101 | 0 | 9.223 | 719 | 4.361 | Q0/Q1/Q2 | PASS |
| 26090101 | 1 | 10.492 | 719 | 4.361 | Q0/Q1/Q2 | PASS |
| 26090102 | 0 | 8.760 | 719 | 4.359 | Q0/Q1/Q2 | PASS |
| 26090102 | 1 | 8.263 | 719 | 4.361 | Q0/Q1/Q2 | PASS |
| 26090103 | 0 | 8.467 | 719 | 4.360 | Q0/Q1/Q2 | PASS |
| 26090103 | 1 | 8.444 | 719 | 4.361 | Q0/Q1/Q2 | PASS |

Aggregati economici, riportati come caratterizzazione e non come criterio di ottimizzazione:

```text
MEAN_FINAL_MONEY: 8941.5
MEDIAN_FINAL_MONEY: 8613.5
MIN_FINAL_MONEY: 8263
MAX_FINAL_MONEY: 10492
POPULATION_STDDEV: 758.2055
```

I sei duplicati hanno prodotto uguaglianza esatta di action-sequence SHA, ledger SHA, stato/risultato terminale e denaro finale.

## 4. Ledger ed escape audit

Il ledger ha registrato `26.163` comandi su `26.163` emessi. Ogni episodio contiene 719 action batch. Non si sono verificati errori della policy, errori del ledger, status invalidi o run sostituiti.

Sono presenti `1.179` record market. La classification coverage market è `10,1781%`: il valore basso è atteso perché i batch con più ordini restano prudentemente `UNKNOWN`. Non è stato imputato alcun outcome ambiguo e il frozen gate richiede copertura dei record al 100%, non classificazione artificiale al 100%.

`DERIVED_EOD_ESCAPE_COUNT=0`. Il relativo estrattore è attivo e versionato nel ledger; la baseline corrente non introduce animali, quindi il risultato attesta integrità dell'audit ma non costituisce evidenza di serviceability zootecnica.

## 5. Audit di indipendenza

L'audit AST e di provenance rileva:

- nessun import da `agricola.strategy.codex` o `agricola.strategy.antigravity`;
- nessun riferimento a `ROUTINE_ACTIONS`, `codex_v9_routine_data` o routine agent-local esterne;
- nessuna action table, planner, dispatcher o schedule importata;
- dipendenze condivise limitate a observation contract, ledger neutrale e opponent neutrale;
- fingerprint nativo `315073D2…`, distinto dal routine fingerprint Codex `C2466262…`;
- decisioni calcolate dallo stato corrente, senza branch su seed o dati futuri.

Il gate locale d'indipendenza è `PASS`. Come richiesto dal freeze comune, l'accesso al torneo di Livello D resta subordinato a review indipendente esterna; questa review non viene autocertificata dal presente report.

## 6. Verifica

```text
TARGETED_LEDGER_AND_COPILOT_TESTS: PASS
REPOSITORY_PLUS_E17_TESTS: 62/62 PASS
DEVELOPMENT_MATRIX: 3 seeds × 2 seats = 6/6 COMPLETE
FAILED_RUN_REPLACEMENT: NONE
HOLDOUT_CONSUMED: false
FINAL_CONFIRMATION_CONSUMED: false
```

Artefatti principali:

- `experiments/e17/artifacts/runs/copilot/e17_0/` — 6 ledger JSONL, 6 summary e 6 file di eventi derivati;
- `experiments/e17/artifacts/derived/copilot/E17_0_METRICS.json`;
- `experiments/e17/artifacts/freeze/copilot/E17_0_FREEZE_MANIFEST.json`;
- `experiments/e17/artifacts/freeze/copilot/COPILOT_E17_0_NATIVE_3Q_V1.py`;
- `experiments/e17/artifacts/freeze/copilot/COPILOT_E17_0_NATIVE_3Q_V1.json`.

## 7. Blocker e confini

**Blocker E17.0 Copilot reali: nessuno.**

Restano due limiti non bloccanti e dichiarati: la copertura di classificazione market è parziale per disegno conservativo, e l'indipendenza per il Livello D richiede ancora una review esterna. I risultati economici contro opponent inert non autorizzano promozione, confronto indipendente o submission.

```text
E17_1_IMPLEMENTED: NO
POLICY_OPTIMIZATION: NO
HOLDOUT_OR_FINAL_USED: NO
LEVEL_D_TOURNAMENT: NO
KAGGLE_SUBMISSION: NO
COMMIT: NO
PUSH: NO
NEXT_ALLOWED_ACTION: independent review and common E17.0 reconciliation
```
