# C2 â€” CODEX ENGINE CONTRACT / PERIOD LEDGER AUDIT

```text
AGENT: CODEX
PHASE: DEFINE / FOUNDATION AUDIT
TASK_ID: C2-ENGINE-CONTRACT-PERIOD-LEDGER-AUDIT
SCOPE: ENGINE SEMANTICS ONLY
FOUNDATION_MODIFICATION_AUTHORIZED: NO
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Obiettivo

Produrre una ricostruzione **canonica, verificabile e source-grounded** della semantica temporale e biologica dell'engine Kaggriculture usato localmente per C2.

L'audit deve stabilire i fatti di dominio che la futura Foundation potrÃ  assumere come comuni, prima di qualsiasi revisione di:

- Ontology;
- Environment State Machine;
- Feature Model;
- Decision Lifecycle;
- MODEL_SPEC.

Il compito NON Ã¨ proporre una strategia competitiva.

Il compito NON Ã¨ ottimizzare il comportamento dell'agente.

Il compito NON Ã¨ riscrivere la Foundation.

Il compito Ã¨:

```text
ENGINE SOURCE
-> VERIFIED DOMAIN FACTS
-> PERIOD LEDGER
-> BOUNDARY EXAMPLES
-> PROVENANCE / VERSION
-> DISCREPANCIES WITH CURRENT FOUNDATION
```

---

# 2. Contesto metodologico da preservare

I tre feedback indipendenti hanno convergito sulla necessitÃ  di separare:

```text
DOMAIN / ENGINE SEMANTICS
POLICY-CONTEXT FEATURES
CONTROLLER / DELIBERATION
```

La revisione futura userÃ  indicativamente:

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

Questo audit Ã¨ il prerequisito del primo passo successivo.

---

# 3. Vincolo fondamentale

Ogni affermazione classificata come `ENGINE_VERIFIED` deve essere supportata direttamente da:

- source code dell'engine;
- metadata canonici runtime;
- costanti/configurazioni;
- test engine;
- o transizioni deterministiche riproducibili.

I replay esterni possono essere usati solo come:

```text
EMPIRICAL_VALIDATION
```

non come fonte primaria dei fatti canonici.

Non promuovere a fatto engine:

- osservazioni di replay;
- euristiche dei MODEL_SPEC;
- soglie economiche;
- pattern dei top player;
- interpretazioni strategiche.

---

# 4. Versione e provenance

Identificare in apertura:

```text
ENGINE_PACKAGE:
ENGINE_VERSION:
ENGINE_SOURCE_ROOT:
GIT_COMMIT_OR_HASH:
RELEVANT_CONFIG:
turnsPerDay:
EPISODE_LENGTH:
DATE_OF_AUDIT:
```

Se l'engine non Ã¨ direttamente versionato con hash univoco, costruire un fingerprint riproducibile dei file sorgente rilevanti.

Elencare tutti i file engine consultati.

Ogni fatto congelabile deve essere riconducibile almeno a:

```text
source_file
symbol / class / function / constant
line or code region if practical
```

---

# 5. Audit del clock

Verificare formalmente:

- unitÃ  canonica del tempo;
- `turn`;
- `step`;
- `day`;
- relazione `step <-> day`;
- `turnsPerDay`;
- configurabilitÃ  di `turnsPerDay`;
- EOD boundary;
- ordine delle risoluzioni dentro il turno;
- reset di flag daily;
- differenza tra action-time e transition-time;
- semantica:

```text
STATE_t
-> ACTION_t
-> STATE_t+1
```

Verificare se questa Ã¨ la corretta convenzione per misurare un effetto.

Produrre almeno 3 boundary examples completi:

```text
example A: action just before EOD
example B: action at first turn of new day
example C: plant/place and first biological event
```

---

# 6. Species inventory â€” fonte engine

Ricostruire l'inventario effettivo delle specie supportate dall'engine.

## Crops

Verificare almeno:

```text
WHEAT
CARROT
MELON
TOMATO
STRAWBERRY
```

e qualsiasi altra specie crop realmente engine-supported.

## Livestock

Verificare almeno:

```text
GOOSE
COW
SHEEP
```

e qualsiasi altra specie animale realmente engine-supported.

### Blocco specifico

Verificare esplicitamente:

```text
CHICKEN
```

e classificare:

```text
NOT_SUPPORTED
ALIAS
LEGACY_NAME
RUNTIME_VARIANT
OTHER
```

Non assumere `CHICKEN` senza prova.

---

# 7. Period ledger per ogni crop

Per ogni specie crop produrre una riga/tabella contenente, se applicabile:

```text
entity
structure / terrain requirement
seed cost
plant legality
origin_day semantics
first_yield_day
max_yield_day
production_interval
max_productions
ongoing / non_ongoing
water requirement
consecutive_unwatered rule
weed / decay rule
harvest legality
harvest window
yield progression
fertilizer interaction
max_lifespan formula
daily reset interaction
inventory / product generated
sellable output
source provenance
confidence
```

Distinguere sempre:

```text
ENGINE_HARD_RULE
POLICY_CHOICE
DERIVED_FORMULA
```

Esempio di distinzione da verificare:

```text
HARVEST legal from age X
!=
HARVEST economically optimal at age Y
```

Non trasformare una scelta di max-yield in una legge del dominio.

---

# 8. Period ledger per ogni animal

Per ogni specie animale produrre:

```text
entity
required structure
purchase cost
max held
placement legality
origin_day semantics
first_yield_day
production_interval
max_productions if any
base production
bonus production
FEED requirement
CARE effect
consecutive_unfed rule
escape rule
fertilizer generation
daily reset
product generated
collection semantics
inventory interaction
sellable output
source provenance
confidence
```

---

# 9. Blocco P0 â€” Animal production vs FEED

Questo punto Ã¨ un blocker esplicito.

La Foundation corrente e l'ispezione engine preliminare risultano potenzialmente discordanti.

Verificare direttamente nel source:

```text
QUESTION:
Does an animal produce base output on a production day if fed_today == FALSE,
provided it has not escaped?
```

Separare:

```text
BASE_OUTPUT
FEED_BONUS
CARE_BONUS
ESCAPE_RISK
PRODUCTION_ELIGIBILITY
```

Produrre esempi di transizione minimi per almeno:

```text
COW
SHEEP
GOOSE
```

con casi:

```text
fed + cared
fed + not cared
not fed + cared
not fed + not cared
```

quando legalmente osservabili.

Se la Foundation corrente Ã¨ errata, riportare:

```text
FOUNDATION_DISCREPANCY: YES
SEVERITY: P0
AFFECTED_SEMANTICS:
PROPOSED_CORRECTION:
```

Non modificare ancora i file Foundation.

---

# 10. Blocco P0 â€” Fertilizer

Verificare esattamente:

- origine;
- quali entitÃ  lo producono;
- condizione di produzione;
- durata;
- effetto;
- momento di applicazione;
- interazione con crop age;
- interazione con WATER;
- interazione con yield;
- interazione con first/max yield;
- eventuale stacking;
- expiry;
- reset.

Produrre un esempio minimo step/day-based.

Non usare formule dedotte dai replay se non confermate dal source.

---

# 11. Service needs

Per ogni specie distinguere:

```text
ENGINE_HARD_NEED
POLICY_OUTPUT_NEED
OPTIONAL_BONUS_SERVICE
```

Esempi da verificare:

```text
WATER needed to avoid engine loss
vs
WATER at a cadence chosen to maximize yield

FEED needed to avoid escape
vs
FEED needed for production bonus

CARE needed for bonus
vs
CARE required for legal survival
```

L'audit deve impedire che una preferenza economica venga codificata come legge dell'engine.

---

# 12. Service windows e deadlines

Per ogni servizio determinare se l'engine definisce:

```text
exact_due_step
open_window
close_window
hard_deadline
soft_deadline
daily_reset_boundary
```

Se la nozione di `SERVICE_WINDOW` Ã¨ una derivazione della policy e non una primitive engine, dichiararlo.

Classificare ogni window:

```text
ENGINE_DEFINED
DERIVED_FROM_ENGINE
POLICY_DECLARED
```

---

# 13. Capacity semantics

Non progettare ancora il planner.

Auditare soltanto quali vincoli engine sono realmente rilevanti per la futura capacitÃ :

- worker contracts;
- worker actions / day;
- movement semantics;
- task ordering;
- structures;
- shed / handling;
- inventory;
- feed availability;
- seed availability;
- fertilizer;
- market-order mechanics;
- spatial constraints;
- simultaneous or serialized actions;
- legality dependencies.

Non dichiarare:

```text
required_slots <= available_slots
```

come garanzia sufficiente.

Indicare quali dimensioni rendono la capacity multidimensionale.

---

# 14. Tre livelli di serviceability

Verificare se la futura Foundation puÃ² distinguere coerentemente:

```text
ACTION_ELIGIBLE_NOW
RESERVED_SERVICEABLE_BEFORE_DEADLINE
REALIZED_SERVICEABLE_IN_WINDOW
```

Per ognuno specificare:

```text
SOURCE:
OBSERVABILITY:
DETERMINISTIC / PARTIALLY_KNOWN / POST_HOC:
DEPENDENCIES:
```

Non trasformare `RESERVED_SERVICEABLE` in fatto engine se dipende da un planner.

---

# 15. Discrepancy audit della Foundation C2 corrente

Confrontare i risultati con:

```text
docs/model/ontology/ONTOLOGY_C2.md
docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
```

Classificare ogni divergenza:

```text
P0_ENGINE_CONTRADICTION
P1_SEMANTIC_AMBIGUITY
P2_MISSING_DOMAIN_FACT
P3_NAMING_OR_MODELING_ISSUE
```

Per ogni discrepancy:

```text
ID
CURRENT_FOUNDATION_CLAIM
ENGINE_EVIDENCE
WHY_IT_MATTERS
AFFECTED_LAYER
RECOMMENDED_CHANGE
```

Non applicare ancora la modifica.

---

# 16. Period ledger canonico

Produrre una tabella finale versionata.

Schema minimo:

```text
ENTITY
ENTITY_TYPE
BIOLOGICAL_EVENT
PERIOD_DAYS
PERIOD_FORMULA
FIRST_EVENT_DAY
WINDOW_OPEN
WINDOW_CLOSE
HARD_DEADLINE
DAILY_RESET_DEPENDENCY
ONGOING
MAX_PRODUCTIONS
ENGINE_SOURCE
ENGINE_HASH
STATUS
```

Dove gli step derivano da:

```text
period_steps = period_days * turnsPerDay
```

quando questa formula Ã¨ realmente corretta.

Non congelare direttamente 24/48/72/96 come costanti universali.

---

# 17. Replay reconciliation

Solo dopo aver costruito il ledger engine-grounded, confrontarlo con i quattro replay:

```text
103484828.json â€” LuCcc
103473619.json â€” Gordeev
103462357.json â€” Dipin
103464592.json â€” Petar
```

Per ogni pattern periodico rilevante classificare:

```text
ENGINE_CONFIRMED
ENGINE_COMPATIBLE_POLICY_PATTERN
POLICY_SPECIFIC
UNEXPLAINED
REPLAY_MEASUREMENT_ARTIFACT
```

Lo scopo non Ã¨ reinterpretare la strategia dei player, ma verificare che il ledger spieghi correttamente le periodicitÃ  osservate.

---

# 18. No future leakage / provenance

Verificare la futura separazione tra:

```text
PRE_ACTION_ENGINE_STATE
DERIVED_PRE_ACTION_FEATURE
POLICY_CONTEXT
POST_ACTION_TRANSITION_EVIDENCE
POST_WINDOW_METRIC
```

In particolare:

```text
completion_evidence
forecast_error
realized_serviceability
```

non devono diventare input anticipati dell'evento che devono misurare.

Segnalare qualsiasi rischio di future leakage presente nella Foundation corrente o proposto.

---

# 19. Output richiesto

Creare:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

Il report deve contenere almeno:

1. Executive verdict.
2. Engine identity / version / hash.
3. Source inventory.
4. Clock contract.
5. Action-transition semantics.
6. Canonical species inventory.
7. Crop period ledger.
8. Animal period ledger.
9. Animal production vs FEED P0 audit.
10. Fertilizer audit.
11. Service-need taxonomy.
12. Window/deadline taxonomy.
13. Capacity-relevant engine constraints.
14. Three-way serviceability analysis.
15. Current Foundation discrepancy matrix.
16. Canonical period ledger.
17. Replay reconciliation.
18. Provenance / no-future-leakage findings.
19. Required corrections before Ontology revision.
20. Final authorization verdict.

---

# 20. Final verdict schema

Chiudere il report con:

```text
ENGINE_CONTRACT_AUDIT_COMPLETE: YES/NO
ENGINE_IDENTITY_FROZEN: YES/NO
CLOCK_CONTRACT_VERIFIED: YES/NO
SPECIES_INVENTORY_VERIFIED: YES/NO
GOOSE_CHICKEN_RESOLVED: YES/NO
ANIMAL_FEED_PRODUCTION_SEMANTICS_RESOLVED: YES/NO
FERTILIZER_SEMANTICS_RESOLVED: YES/NO
PERIOD_LEDGER_READY_FOR_REVIEW: YES/NO
FOUNDATION_DISCREPANCIES_IDENTIFIED: YES/NO
ONTOLOGY_REVISION_SAFE_TO_START: YES/NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Se anche un solo blocker P0 resta irrisolto:

```text
ONTOLOGY_REVISION_SAFE_TO_START: NO
```

---

# 21. Vincoli finali

- Non modificare il codice.
- Non modificare la Foundation.
- Non modificare i MODEL_SPEC.
- Non fare tuning.
- Non fare tournament.
- Non fare Kaggle.
- Non usare score come prova di semantica engine.
- Non trasformare policy choices in engine facts.
- Non introdurre nuovi termini ontologici nel repository durante questo audit.
- Non leggere feedback successivi di Antigravity/Copilot se non esplicitamente autorizzato.
- Dove il source non consente una conclusione, usare `UNRESOLVED`, non inferire.

```text
NEXT_PHASE_IF_PASS:
INDEPENDENT REVIEW OF ENGINE CONTRACT BY ANTIGRAVITY + COPILOT
```
