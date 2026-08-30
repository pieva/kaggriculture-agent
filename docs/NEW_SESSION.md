# NEW_SESSION â€” Kaggriculture

## Ripresa consigliata

La sessione precedente ha chiuso la fase di **Engine Contract / Period Ledger audit e independent review** per la revisione C2 della Foundation.

Non ripartire da MODEL_SPEC, codice o tournament.

Il prossimo passo Ã¨:

```text
FINAL ENGINE CONTRACT RECONCILIATION
-> ENGINE CONTRACT FREEZE
-> ONTOLOGY REVISION
```

## Stato congelato al termine della sessione

```text
ENGINE_CONTRACT_AUDIT_COMPLETE: YES
ANTIGRAVITY_INDEPENDENT_REVIEW_COMPLETE: YES
COPILOT_INDEPENDENT_REVIEW_COMPLETE: YES
AGG_01_STATUS: RESOLVED
ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED: YES
ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE: YES

MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Fingerprint engine canonico:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

Engine:

```text
kaggle-environments 1.32.7
Kaggriculture environment metadata 0.1.0
turnsPerDay configurable, default 24
episodeSteps default 720
```

## Documenti chiave da leggere per primi

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md

results/model_spec_c2/foundation_revision/
ANTIGRAVITY_C2_ENGINE_CONTRACT_REVIEW.md

results/model_spec_c2/foundation_revision/
COPILOT_C2_ENGINE_CONTRACT_INDEPENDENT_REVIEW.md

results/model_spec_c2/foundation_revision/
CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md

results/model_spec_c2/foundation_revision/
COPILOT_C2_AGG_01_REVERIFICATION.md
```

Foundation corrente da correggere successivamente:

```text
docs/model/ontology/ONTOLOGY_C2.md
docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
```

## Conclusioni engine da trattare come canoniche dopo reconciliation

### Clock

```text
step == day * turnsPerDay + hour
EOD_STEP(d) = (d + 1) * turnsPerDay - 1
STATE_t -> ACTION_t -> STATE_t+1
```

Non hardcodare 24/48/72/96 come periodi universali in step.

### Species inventory

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

```text
CHICKEN = NOT_SUPPORTED
```

### Crop periods

```text
WHEAT      first yield d0+2, max yield d0+4
CARROT     first yield d0+2, max yield d0+3
TOMATO     first event d0+8, interval 1 day
STRAWBERRY first event d0+10, interval 2 days
MELON      first yield d0+10, max yield d0+12
```

Distinguere sempre engine biological event da policy harvest timing.

### Animal periods

```text
GOOSE first output d0+4, interval 1 day
COW   first output d0+8, interval 2 days
SHEEP first output d0+6, interval 3 days
```

Semantica decisiva:

```text
Base output = 1 anche senza FEED
se l'animale non Ã¨ ancora fuggito e il production event Ã¨ scheduled.
```

`FEED`:

- previene escape;
- consente il consumo del pending care bonus;
- contribuisce con CARE all'accumulo del bonus futuro;
- non Ã¨ gate del base output.

### Fertilizer

```text
BASE_INCREMENT_TOTAL = 1
FERTILIZED_INCREMENT_TOTAL = 2
FERTILIZER_UPLIFT = +1
```

Finestra:

```text
current_day .. current_day+2
```

Il fertilizer non accelera il biological clock.

### Inventory

```text
MANUAL DROP: puÃ² perdere overflow
EOD AUTO-DROP: puÃ² perdere overflow
PLACE: conserva nel worker il residuo che non entra
```

## Serviceability

Usare tre concetti distinti:

```text
ACTION_ELIGIBLE_NOW
RESERVED_SERVICEABLE_BEFORE_DEADLINE
REALIZED_SERVICEABLE_IN_WINDOW
```

Il secondo Ã¨ `POLICY_CONTEXT`, non engine fact.
Il terzo Ã¨ post-hoc e non puÃ² essere usato come pre-action feature.

## Foundation architecture da preservare

Separare due macchine:

### A. Environment / Domain State Machine

Contiene:

- clock;
- crop lifecycle;
- animal lifecycle;
- worker lifecycle;
- inventory;
- market;
- service needs;
- legality;
- EOD;
- decay/loss;
- transitions.

NON contiene:

- DEFINE;
- crop choice;
- exploration;
- capacity reservation;
- economic target.

### B. Decision Lifecycle / Controller

Separata e downstream rispetto al Feature Model.

Schema consigliato:

```text
DECISION_OPEN
-> DEFINED
-> PLAN_FEASIBLE
-> COMMITTED_EXECUTING
-> REVIEW_READY
-> DECISION_OPEN
```

`VERIFY` continuo durante `COMMITTED_EXECUTING`.

Principio:

```text
REACT ai decision point.
PLAN dopo il commitment.
VERIFY durante l'esecuzione.
REVIEW prima della decisione successiva.
```

## Reconciliation da fare subito

La reconciliation finale deve:

1. assumere il Codex Engine Contract corretto come baseline;
2. registrare Antigravity come semantic PASS;
3. registrare Copilot come semantic PASS con `AGG-01` successivamente risolto;
4. mantenere gli ID/severity della discrepancy matrix Codex come baseline;
5. non incorporare tacitamente le piccole variazioni classificatorie presenti nella review Antigravity;
6. congelare fingerprint e procedura di serializzazione;
7. produrre un verdetto unico:

```text
ENGINE_CONTRACT_FREEZE: YES/NO
```

Dato lo stato attuale, il risultato atteso Ã¨ `YES` salvo errore emerso durante la reconciliation documentale.

## Dopo il freeze

Procedere nell'ordine:

```text
ONTOLOGY
-> ENVIRONMENT STATE MACHINE
-> FEATURE MODEL
-> DECISION LIFECYCLE CONTRACT
-> VERTICAL CROSS-REVIEW
-> FOUNDATION FREEZE
```

Solo dopo:

```text
ANTIGRAVITY MODEL_SPEC
CODEX MODEL_SPEC
COPILOT MODEL_SPEC
```

Nessun BUILD prima del Foundation freeze.

## Performance gate prossimo round

Questi target sono di progetto e NON devono entrare nella Foundation:

```text
< 50,000   = project failure gate
50kâ€“80k    = material improvement but target miss
>= 80,000  = project target
```

## Decisioni metodologiche da non perdere

- Foundation period-centric, ma non rigid-clock.
- Periodi engine espressi in giorni e parametrizzati con `turnsPerDay`.
- Capacity reservation multidimensionale; `required_slots <= available_slots` non Ã¨ sufficiente da solo.
- Action request != action execution != state transition.
- Replay: `STATE_t -> ACTION_t -> STATE_t+1`.
- Exploration by replacement Ã¨ possibile MODEL_SPEC/protocol choice, non obbligo Foundation.
- Multi-Q expansion Ã¨ strategia, non legge causale del dominio.
- Livestock non va assunto automaticamente come positivo: beneficio economico da isolare causalmente.
- Foundation deve restare neutrale rispetto a mix, workforce, routing, expansion e market policy.

---

```text
START_HERE:
FINAL ENGINE CONTRACT RECONCILIATION + FREEZE

DO_NOT_START:
MODEL_SPEC
BUILD
TOURNAMENT
KAGGLE
```
