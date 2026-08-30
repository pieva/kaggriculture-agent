# PROJECT_STATE â€” Kaggriculture

## Stato corrente

```text
PROJECT: Kaggriculture
PHASE: C2 â€” Foundation Revision / Engine Contract
STATUS_DATE: 2026-08-31

ENGINE_CONTRACT_AUDIT_COMPLETE: YES
INDEPENDENT_REVIEWS_COMPLETE: YES
AGG_01_STATUS: RESOLVED
ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED: YES
ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE: YES

ONTOLOGY_REVISION_STARTED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Contesto

Il round C2 ha mostrato che la Foundation precedente descriveva correttamente diversi meccanismi generali, ma conteneva anche assunzioni errate o insufficientemente verificate sull'engine Kaggriculture.

La revisione Ã¨ stata quindi riportata a monte, separando:

1. **Engine / Domain Contract** â€” fatti normativi dell'ambiente;
2. **Ontology** â€” concetti di dominio;
3. **Environment State Machine** â€” stati e transizioni dell'engine;
4. **Feature Model** â€” osservabili, derivati e policy context;
5. **Decision Lifecycle / Controller Contract** â€” ciclo deliberativo dell'agente;
6. **MODEL_SPEC** â€” strategie specifiche;
7. **BUILD / VERIFY / TOURNAMENT / Kaggle** â€” fasi downstream.

La sequenza approvata Ã¨:

```text
ENGINE CONTRACT / PERIOD LEDGER AUDIT
-> ONTOLOGY
-> ENVIRONMENT STATE MACHINE
-> FEATURE MODEL
-> DECISION LIFECYCLE CONTRACT
-> VERTICAL CROSS-REVIEW
-> FOUNDATION FREEZE
-> THREE INDEPENDENT MODEL_SPEC REVISIONS
```

## 2. Evidenza che ha motivato la revisione period-centric

La precedente iterazione competitiva C2 ha prodotto:

```text
Codex V4 Mean Final Money:     31,579.50
Antigravity Mean Final Money:  27,565.17
Copilot Mean Final Money:       7,823.67
```

La successiva analisi dei replay dei player ad alto punteggio ha mostrato che:

- LuCcc raggiunge **56,772** usando un solo quadrante;
- Gordeev, Dipin e ÐŸÐµÑ‚Ð°Ñ€ raggiungono circa **88kâ€“95k** con configurazioni diverse;
- la sola espansione territoriale non Ã¨ quindi condizione necessaria per superare 50k;
- emerge una forte struttura temporale nei cicli biologici e di servizio.

Principio architetturale emerso:

```text
BIOLOGICAL PERIOD
-> FUTURE SERVICE DEMAND
-> CAPACITY FEASIBILITY
-> COMMITMENT
-> EXECUTION
-> TRANSITION VERIFICATION
```

Principio controller:

```text
REACT sceglie e rialloca la capacitÃ  produttiva nei punti di decisione.
PLAN governa deterministicamente il ciclo dopo il commitment.
VERIFY controlla l'esecuzione e le transizioni.
REVIEW precede il successivo punto di decisione.
```

Questo ciclo non deve essere confuso con l'Environment State Machine.

## 3. Feedback Foundation indipendenti

Tre review indipendenti hanno convergito sulla direzione period-centric.

### Antigravity

Verdetto:

```text
ACCEPT_WITH_METHODOLOGICAL_REFINEMENT
```

Conferma:

- biological periods come concetto centrale;
- temporal serviceability;
- separazione Domain State Machine / Agent Deliberation;
- REACT ai decision point e PLAN dopo il commitment;
- Foundation neutrale rispetto a mix, workforce ed expansion.

### Copilot

Verdetto:

```text
PROCEED WITH FOUNDATION REVISION, BUT DO NOT FREEZE PERIODIC CANONICALS YET
```

Conferma:

- period-centric Foundation;
- separazione engine facts / policy;
- serviceability per finestra;
- necessitÃ  di verificare direttamente i periodi engine;
- nessun freeze dei valori numerici senza source evidence.

### Codex

Verdetto:

```text
PARTIALLY_SUPPORTED
PROCEED_ONLY_AFTER_MANDATORY_CHANGES
```

Correzioni decisive:

- specie avicola canonica: `GOOSE`, non `CHICKEN`;
- `FEED` non Ã¨ il gate del base animal output;
- periodi canonici espressi in giorni e parametrizzati con `turnsPerDay`;
- separazione formale tra `Environment State Machine` e `Decision Lifecycle`;
- serviceability distinta in:
  - `ACTION_ELIGIBLE_NOW`;
  - `RESERVED_SERVICEABLE_BEFORE_DEADLINE`;
  - `REALIZED_SERVICEABLE_IN_WINDOW`.

Da questo feedback Ã¨ nato il gate obbligatorio:

```text
ENGINE PERIOD LEDGER / CONTRACT AUDIT
prima della revisione Ontology.
```

## 4. Codex Engine Contract / Period Ledger Audit

Documento:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

Engine verificato:

```text
PACKAGE: kaggle-environments
PACKAGE_VERSION: 1.32.7
ENVIRONMENT_VERSION: 0.1.0
turnsPerDay: configurable, default 24
episodeSteps: default 720
```

Fingerprint canonico finale:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

### Clock contract verificato

```text
step == day * turnsPerDay + hour
EOD_STEP(d) = (d + 1) * turnsPerDay - 1
STATE_t -> ACTION_t -> STATE_t+1
```

Le periodicitÃ  biologiche non devono essere hardcoded in step assoluti.

### Species inventory verificato

Crops:

```text
WHEAT
CARROT
TOMATO
STRAWBERRY
MELON
```

Animals:

```text
GOOSE
COW
SHEEP
```

`CHICKEN`:

```text
NOT_SUPPORTED
```

Products:

```text
EGG
MILK
WOOL
FERTILIZER
```

### Crop ledger verificato

- `WHEAT`: first yield day 2, max yield day 4, non-ongoing.
- `CARROT`: first yield day 2, max yield day 3, non-ongoing.
- `TOMATO`: first event day 8, interval 1 day, ongoing.
- `STRAWBERRY`: first event day 10, interval 2 days, ongoing.
- `MELON`: first yield day 10, max yield day 12, non-ongoing.

Le finestre di harvesting policy non devono essere confuse con i periodi engine.

### Animal ledger verificato

```text
GOOSE: first output d0+4, interval 1 day
COW:   first output d0+8, interval 2 days
SHEEP: first output d0+6, interval 3 days
```

Semantica chiave:

- base output = `1` nel scheduled production event se l'animale non Ã¨ fuggito;
- `FEED` non abilita il base output;
- `FEED` previene l'escape e abilita il consumo del `pending_care_bonus`;
- `CARE` contribuisce al bonus futuro solo insieme a `FEED`;
- secondo giorno consecutivo non alimentato -> escape prima della produzione.

### Fertilizer verificato

```text
BASE_INCREMENT_TOTAL = 1
FERTILIZED_INCREMENT_TOTAL = 2
FERTILIZER_UPLIFT = +1
```

`FERTILIZE`:

- non accelera il biological clock;
- vale per `current_day .. current_day+2` inclusi;
- modifica l'incremento di yield, non l'etÃ  o il calendario.

### Inventory overflow verificato

`DROP` manuale:

```text
puÃ² perdere l'overflow se lo shed Ã¨ pieno
```

EOD auto-drop:

```text
puÃ² perdere l'overflow
```

`PLACE` nello shed:

```text
deposita quanto entra e conserva il residuo nel worker inventory
```

## 5. Discrepancy Foundation da correggere

Il Codex audit ha individuato almeno queste discrepancy da correggere prima del freeze Foundation:

```text
CLK-01
ANI-01
ANI-02
FER-01
FER-02
INV-01
INV-02
SVC-01
CAP-01
OBS-01
HAR-01
SPC-01
PER-01
```

I P0 sostanziali confermati sono:

```text
CLK-01
ANI-01
FER-01
INV-01
```

Significato:

- clock/periodicitÃ ;
- FEED/base animal production;
- fertilizer uplift;
- inventory overflow.

## 6. Independent Engine Contract Reviews

### Antigravity review

Documento:

```text
results/model_spec_c2/foundation_revision/
ANTIGRAVITY_C2_ENGINE_CONTRACT_REVIEW.md
```

Esito:

```text
ENGINE_IDENTITY_MATCH: YES
NEW_P0_FOUND: 0
NEW_P1_FOUND: 0
UNRESOLVED_BLOCKERS: 0
ENGINE_CONTRACT_READY_TO_FREEZE: YES
ONTOLOGY_REVISION_SAFE_AFTER_RECONCILIATION: YES
```

La review conferma tutta la semantica critica dell'audit.

### Copilot review

Documento:

```text
results/model_spec_c2/foundation_revision/
COPILOT_C2_ENGINE_CONTRACT_INDEPENDENT_REVIEW.md
```

Esito semantico:

```text
ACCEPT_WITH_CORRECTIONS
```

Copilot conferma:

- clock;
- species inventory;
- animal base production;
- FEED/CARE;
- fertilizer;
- inventory overflow;
- periodi config-relative;
- serviceability tripartita.

Unico rilievo:

```text
AGG-01
SEVERITY: P3
TYPE: provenance / fingerprint reproducibility
```

Nessuna nuova contradiction semantica.

## 7. AGG-01 correction e re-verification

Codex ha prodotto:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md
```

Root cause:

- serializzazione del manifest originariamente underspecified;
- root, path normalization, sort case-sensitive, BOM e trailing newline non esplicitati.

Procedura canonica finale:

```text
PATH_SEPARATOR: /
SORT: Unicode case-sensitive ascending
FILE_READ_MODE: binary
HASH_HEX: lowercase
RECORD: path + HTAB + sha256
TEXT_ENCODING: UTF-8
BOM: NO
RECORD_SEPARATOR: LF
TRAILING_NEWLINE: NO
PAYLOAD_LENGTH: 702 bytes
```

Codex ha riprodotto il vecchio hash:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

senza modificare contenuti semantici.

Copilot ha quindi eseguito una re-verification mirata:

```text
results/model_spec_c2/foundation_revision/
COPILOT_C2_AGG_01_REVERIFICATION.md
```

Esito:

```text
CANONICAL_COMMAND_EXECUTED: YES
INDIVIDUAL_FILE_HASHES_MATCH: YES
CANONICAL_PAYLOAD_MATCH: YES
PAYLOAD_LENGTH_702: YES
AGGREGATE_MATCH: YES

AGG_01_STATUS: RESOLVED
ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED: YES
ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE: YES
```

## 8. Stato decisionale corrente

La fase di audit/review dell'Engine Contract Ã¨ conclusa.

Non restano:

```text
NEW_SEMANTIC_P0: 0
UNRESOLVED_PROVENANCE_BLOCKERS: 0
```

Il contratto engine Ã¨ quindi pronto per:

```text
FINAL ENGINE CONTRACT RECONCILIATION
-> ENGINE CONTRACT FREEZE
-> ONTOLOGY REVISION
```

Non Ã¨ ancora autorizzato:

```text
MODEL_SPEC REVISION
BUILD
TOURNAMENT
KAGGLE
```

## 9. Principi da preservare nella Foundation revision

1. **Engine facts prima della policy.**
2. **Periodi in giorni / formule config-relative**, non costanti assolute in step.
3. Separare:
   - biological event;
   - legal action window;
   - policy scheduling choice.
4. Separare:
   - action requested;
   - action executed;
   - state transition observed.
5. Serviceability tripartita:
   - `ACTION_ELIGIBLE_NOW`;
   - `RESERVED_SERVICEABLE_BEFORE_DEADLINE`;
   - `REALIZED_SERVICEABLE_IN_WINDOW`.
6. `CAPACITY_RESERVATION`, `COMMITMENT`, `DECISION_POINT`, `REACTIVE_OVERRIDE` appartengono al controller/policy context salvo prova che siano domain concepts autonomi.
7. La Foundation non prescrive:
   - crop/livestock mix;
   - workforce count;
   - quadrant strategy;
   - expansion schedule;
   - routing/scheduling algorithm;
   - exploration policy.
8. `DEFINE -> PLAN -> BUILD -> VERIFY -> REVIEW -> SHIP` resta metodologia di progetto; non deve diventare Environment State Machine.
9. Per il controller usare invece una lifecycle separata, orientativamente:
   ```text
   DECISION_OPEN
   -> DEFINED
   -> PLAN_FEASIBLE
   -> COMMITTED_EXECUTING
   -> REVIEW_READY
   -> DECISION_OPEN
   ```
10. `VERIFY` Ã¨ continuo/ortogonale durante l'esecuzione.

## 10. Performance target prossimo round

Target di progetto, non proprietÃ  Foundation:

```text
FAILURE_GATE: Mean Final Money < 50,000
MATERIAL_IMPROVEMENT: 50,000 <= Mean Final Money < 80,000
TARGET: Mean Final Money >= 80,000
```

Questi valori dovranno essere valutati con:

- holdout seeds;
- opponents;
- seats;
- stessa configurazione baseline/candidate;
- dispersione;
- separazione technical failures / economic score.

## 11. Prossima azione

Alla ripresa:

```text
1. produrre Final Engine Contract Reconciliation;
2. congelare Engine Contract;
3. correggere Ontology C2 usando il contratto congelato;
4. correggere Environment State Machine;
5. aggiornare Feature Model;
6. definire Decision Lifecycle Contract;
7. vertical cross-review;
8. Foundation freeze;
9. solo dopo: tre MODEL_SPEC indipendenti.
```

---

```text
C2_ENGINE_CONTRACT_REVIEW_PHASE_COMPLETE: YES
ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE: YES
AGG_01_STATUS: RESOLVED
ENGINE_FINGERPRINT_CANONICAL:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

NEXT_PHASE:
FINAL ENGINE CONTRACT RECONCILIATION + FREEZE

MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
