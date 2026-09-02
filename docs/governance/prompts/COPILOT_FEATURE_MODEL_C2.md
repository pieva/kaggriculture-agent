# Copilot — FEATURE MODEL C2

## Obiettivo

Costruire il candidato **Feature Model C2** della Model Foundation Kaggriculture.

Questo passaggio è classificato dalla Foundation Reconciliation R1 come:

```text
FEATURE_MODEL_C1: REVISE_MAJOR
```

Non è quindi un semplice aggiornamento editoriale. Occorre trasformare il Feature Model in un **contratto informativo comune, consumer-neutral e verificabile**, coerente con:

```text
ONTOLOGY C2
    ↓
STATE MACHINE C2
    ↓
FEATURE MODEL C2
    ↓
MODEL_SPEC individuali
```

Non modificare ancora i MODEL_SPEC individuali, il runtime o la policy. Non eseguire training, benchmark o nuovi episodi.

---

# 1. Fonti obbligatorie

Leggere integralmente:

```text
docs/foundation/ontology/ONTOLOGY_C2.md
docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C1.md

docs/governance/foundation/copilot/COPILOT_FOUNDATION_REVIEW_R1.md
docs/governance/foundation/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md
docs/governance/foundation/reconciliation/CODEX_FOUNDATION_RECONCILIATION_R1.md
```

Consultare inoltre, quando necessario:

```text
docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY.md
docs/model/model_specs/codex/MODEL_SPEC_CODEX.md
docs/model/model_specs/copilot/MODEL_SPEC_COPILOT.md

docs/model/model_specs/antigravity/ANTIGRAVITY_MODEL_SPEC_REVISION.md
docs/model/model_specs/codex/CODEX_MODEL_SPEC_REVISION.md
docs/model/model_specs/copilot/COPILOT_MODEL_SPEC_REVISION.md
docs/model_specs/history/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md
```

I MODEL_SPEC servono **solo come consumer evidence** per identificare problemi di mapping. Non devono determinare la struttura semantica del Feature Model comune.

La Foundation Reconciliation R1 è l'arbitrato normativo.

---

# 2. Output

NON sovrascrivere C1.

Creare:

```text
docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
```

con stato:

```text
CANDIDATE C2
NOT FROZEN
CONSUMER-NEUTRAL
UPSTREAM:
  - ONTOLOGY_C2 CANDIDATE
  - STATE_MACHINE_C2 CANDIDATE
DERIVED FROM FOUNDATION RECONCILIATION R1
```

Preservare C1 per confronto.

---

# 3. Principio architetturale fondamentale

Il Feature Model C2 deve descrivere:

> quali informazioni esistono, sono osservabili o derivabili al decision time, con quale provenienza, clock, phase, formula e grado di evidenza.

NON deve descrivere:

> quale specifico MODEL_SPEC le usa.

Quindi il catalogo comune deve essere **consumer-neutral**.

Architettura:

```text
ENGINE
  ↓
ONTOLOGY
  ↓
STATE MACHINE
  ↓
FEATURE MODEL
  ↓
┌──────────────────────────────────────┐
│ consumer matrices versionate        │
│  AG MODEL_SPEC                       │
│  Codex MODEL_SPEC                    │
│  Copilot MODEL_SPEC                  │
└──────────────────────────────────────┘
  ↓
POLICY / RUNTIME
```

---

# 4. BLOCKER — rimuovere `current_MODEL_SPEC_usage`

La reconciliation ha accolto il finding Copilot P0-01.

Il Feature Model comune non deve avere una colonna semanticamente autorevole:

```text
current_MODEL_SPEC_usage
```

perché non esiste un singolo consumer corrente universale.

## 4.1 Storico

Preservare l'informazione storica C1 se utile, ma rinominarla/archiviarla esplicitamente come riferimento al consumer effettivo, per esempio:

```text
codex_e15_frozen_usage
```

oppure spostarla in una sezione/matrice storica separata.

Non presentarla come proprietà intrinseca della feature.

## 4.2 C2

Nel catalogo C2 non introdurre colonne consumer-specifiche AG/Codex/Copilot.

I mapping consumer saranno esterni e versionati.

---

# 5. Information classes

Preservare e verificare la distinzione almeno tra:

```text
ENGINE_STATE
RAW_OBSERVABLE
DERIVED_FEATURE
POLICY_CONTEXT
TELEMETRY_ONLY
OUTCOME_LABEL
```

Verificare che ogni feature appartenga alla classe corretta.

Non confondere:

```text
ENGINE_OBSERVABLE
```

con:

```text
TELEMETRY_OBSERVED
```

Una feature può essere computabile online dall'engine state ma non essere stata correttamente persistita nel replay R1.

Per ogni feature mantenere/definire esplicitamente:

```text
online_available
decision_time_available
future_leakage
```

---

# 6. Clock e phase contract

Allinearsi a State Machine C2.

Per ogni RAW/DERIVED feature temporale rilevante indicare:

- clock autorevole;
- sampling phase;
- eventuale derivazione diagnostica;
- se il valore è disponibile prima della decisione.

Distinguere:

```text
engine_step
```

da:

```text
canonical_step = day * turnsPerDay + hour
```

`engine_step` è autorevole per le regole engine che lo consumano.

`canonical_step` è una ricostruzione diagnostica e non deve essere presentata come sostituto universale di `engine_step`.

Correggere CRP-13..15 e qualsiasi altra feature temporale se C1 assume implicitamente equivalenza fra i due clock.

---

# 7. Lifecycle classifier totale

Questo è un requisito di freeze esplicito della reconciliation.

I valori canonici candidati sono:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

Il Feature Model C2 deve definire un **classifier totale eseguibile**, includendo:

- input necessari;
- predicati;
- ordine di precedenza;
- fallback;
- comportamento su tile `None`;
- comportamento su `LOCKED`;
- comportamento su `WEED`;
- comportamento su `PLANT`;
- working-set scope/policy-context;
- ongoing vs non-ongoing;
- maturity;
- produzione futura prevista;
- condizioni di `RETIREMENT_DUE`.

La classificazione deve essere deterministica dati gli input disponibili.

Aggiungere pseudocodice o decision table sufficientemente precisa da poter essere implementata senza interpretazione.

## 7.1 Boundary tests

Definire casi di test almeno per:

- `LOCKED`;
- tile fuori working set;
- `None` dentro working set;
- PLANT immatura con `yield_units > 0`;
- PLANT matura con `yield_units > 0`;
- ongoing appena raccolta;
- ongoing dopo ultima produzione utile;
- WEED;
- eventuali input mancanti/non validi.

Non inventare uno stato nuovo per coprire errori di telemetria. Gestire gli input invalidi separatamente dal dominio.

---

# 8. HARVEST readiness

Formalizzare come derived feature decision-time:

```text
harvest_ready =
    tile.kind == "PLANT"
    AND tile.yield_units > 0
    AND day - tile.planted_day >= CROPS[tile.crop].first_yield_day
```

Esplicitare:

```text
yield_units > 0
!=
harvest_ready
```

Documentare:

- source fields;
- crop rule dependency;
- sampling phase;
- online availability;
- leakage;
- boundary conditions.

Questo è un finding critico: R1 aveva 5.804 tentativi HARVEST prematuri.

---

# 9. Crop decay risk window

Preservare la struttura multi-causa già corretta in C1:

```text
crop_decay_risk_window:
  care_due
  water_loss_at_eod_if_unserved
  action_phases_until_eod_refresh
  lifespan_decay_started
  next_lifespan_decay_phase
  lifespan_loss_phase_if_no_action
  empty_random_weed_eligible
```

Verificare ogni componente contro clock/phase C2.

Non introdurre:

```text
time_to_random_weed
```

o qualunque countdown deterministico verso un evento RNG.

Il random spawn su EMPTY deve essere rappresentato come:

```text
eligibility / hazard
```

non come deadline nota.

---

# 10. Need / eligibility / serviceability

Formalizzare la separazione introdotta dalla reconciliation:

```text
tile_need
action_eligible_now
serviceable_before_deadline
```

## 10.1 `tile_need`

Rappresenta una necessità meccanica/biologica della tile indipendente dall'attore.

## 10.2 `action_eligible_now`

Deve includere i requisiti engine/actor necessari perché una specifica azione possa essere eseguita **ora**, per esempio:

- actor position/reach;
- tile/action preconditions;
- inventory/resources se richiesti;
- action phase.

Definire il contratto solo fino a dove supportato.

## 10.3 `serviceable_before_deadline`

ATTENZIONE: nella State Machine C2 il report ha usato la parola "garantita". Non adottare questa formulazione.

Definire invece come concetto computabile/stimabile di:

> possibilità, date le informazioni e i vincoli noti, che un attore possa raggiungere la tile e completare l'azione prima della deadline.

Mantenerlo:

```text
PARTIALLY_KNOWN
```

finché non sono contrattualizzati completamente:

- routing;
- actor scheduling;
- action phase;
- inventory;
- policy memory;
- contention;
- deadline;
- reachability.

Non trasformarlo in una garanzia.

---

# 11. Aggregate contracts

Questo è un blocker C2.

Ogni aggregate/metric che possa essere consumato da un MODEL_SPEC o usato come policy gate deve avere un contratto canonico.

Per ciascun aggregate rilevante definire almeno:

```text
feature_id
scope
sampling_phase
window
numerator
denominator
zero_denominator_convention
dedup_key
source_class
formula_version
boundary_examples
online_available
decision_time_available
future_leakage
evidence_status
```

Applicare in particolare a concetti come:

```text
active_crop_surface
crop_surface_maintained
watering_execution
continuity
care_completion
harvest_action_flow
cleanliness
weed_backlog_cost
workforce_capacity
movement_overhead
dispatch_failure
productive_action_share
state_capacity_alignment
operating_cash_buffer
```

se restano nel catalogo.

## 11.1 Regola epistemica

Se una formula non è sufficientemente supportata:

- NON inventarla;
- NON promuovere la feature a pienamente definita;
- marcarla `PARTIALLY_KNOWN`, `CONDITIONAL`, `NOT_FROZEN` o equivalente;
- dichiarare esattamente cosa manca.

In particolare:

```text
state_capacity_alignment
```

non può essere congelata senza formula canonica.

---

# 12. Active surface vs maintained surface

Preservare la distinzione:

```text
active_crop_surface
!=
crop_surface_maintained
```

Una tile attiva non è automaticamente mantenuta correttamente.

Definire o qualificare con precisione il contratto di `crop_surface_maintained`.

Non dedurre mantenimento dalla sola presenza di `PLANT`.

---

# 13. Care completion denominator

C1 riconosce che il denominatore è incompleto.

In C2:

- definire il denominatore se l'evidenza upstream lo consente;
- altrimenti mantenere esplicitamente il contratto incompleto;
- non produrre una percentuale apparentemente precisa con popolazione target ambigua.

La stessa regola vale per qualsiasi ratio.

---

# 14. Workforce features

Rivedere:

```text
worker_positions
worker_headcount
workforce_capacity
movement_overhead
dispatch_failure
productive_action_share
```

alla luce di:

```text
worker_multi_occupancy = ENGINE_VERIFIED
```

La co-location non implica:

- collision penalty;
- capacità produttiva doppia automatica;
- serviceability;
- assenza di contention logica.

Separare chiaramente engine state, derived metrics e policy interpretation.

---

# 15. Inventory provenance

Preservare separatamente almeno:

```text
worker inventory
shed inventory
seed inventory
shed capacity
automatic EOD transfer
shed overflow loss
```

Eliminare ogni derivazione basata sul falso assunto:

```text
worker must return before contract expiry
```

Se esiste una feature di inventory-loss risk, deve essere ricondotta al rischio reale di:

```text
shed_overflow_eod_loss
```

e definita con provenance/phase appropriati.

---

# 16. Market provenance

Non aggregare in una singola feature ambigua:

```text
market state
transaction request
executed transaction
realized value
```

Distinguere almeno concettualmente:

```text
displayed_quote
requested_quantity
executed_quantity
realized_price
cash_delta
estimate
```

Ogni campo deve avere provenance.

Le quantità realizzate post-action non possono essere presentate come pre-action policy input dello stesso step.

---

# 17. Telemetry-only e outcome-only

Verificare esplicitamente almeno:

```text
MKT-02 transaction value
GLB-02 action execution result
GLB-03 transition reason
LBL-01 final money
```

Se sono disponibili solo dopo l'azione/episodio, classificarle correttamente:

```text
POST_ACTION_TELEMETRY
OUTCOME_ONLY
```

a livello di consumer taxonomy successiva.

Nel Feature Model comune restano rispettivamente:

```text
TELEMETRY_ONLY
OUTCOME_LABEL
```

e non devono essere considerate decision-time input.

---

# 18. Livestock / fertilizer

Integrare solo ciò che Ontology C2 e State Machine C2 hanno promosso a ENGINE_VERIFIED:

- fertilizer window `day..day+2`;
- bonus crop esatto;
- CARE → `pending_care_bonus`;
- consumo/effetto su production day con condizioni engine supportate;
- worker multi-occupancy.

Non inventare feature economiche o di ROI.

Se una feature livestock resta incompleta, conservarla `PARTIALLY_KNOWN`.

---

# 19. Feature IDs e stabilità

Preservare gli ID C1 quando la semantica resta la stessa.

Se una feature cambia semanticamente in modo materiale:

- documentare la variazione;
- decidere se mantenere l'ID con nuova `formula_version` o introdurre un nuovo ID;
- evitare silent semantic drift.

Aggiungere una sezione:

```text
## Migrazione Feature Model C1 -> C2
```

con almeno:

```text
feature_id
C1 status
C2 status
change type
reason
compatibility
```

Tipi:

```text
UNCHANGED
CLARIFIED
FORMULA_VERSIONED
RECLASSIFIED
DEPRECATED
ADDED
SPLIT
```

---

# 20. Consumer matrix — definire il contratto, non compilarla ancora

Il Feature Model C2 deve specificare la struttura che una futura consumer matrix dovrà avere.

Schema minimo consigliato:

```text
consumer_id
model_spec_path
model_spec_revision
runtime_path
runtime_revision_or_commit
feature_id
consumer_role
formula_version
sampling_phase
consuming_function
evidence
status
```

con:

```text
consumer_role =
  POLICY_INPUT
  | RUNTIME_DERIVED
  | POST_ACTION_TELEMETRY
  | OUTCOME_ONLY
```

Ma NON compilare ancora le tre matrici definitive.

Non modificare i MODEL_SPEC.

---

# 21. Event schema downstream

Recepire come requisito downstream, senza implementare un sistema telemetry nuovo, lo schema minimo emerso dalla review Copilot:

```text
episode_id
player_id
engine_step
day
hour
phase
observation_sequence
actor_id_or_order_id
action_sequence
state_before
requested_payload
eligibility_predicates
executed_payload
execution_status
failure_reason
state_after_action
state_after_market
state_after_refresh
transition_id
transition_reason
source_engine_or_policy_version
tile_id
tile_lifecycle_before
tile_lifecycle_after
inventory_compartment_before_after
market_quote_before
requested_quantity
executed_quantity
realized_price
cash_delta
```

Aggiungere anche il requisito di versionamento per:

```text
policy memory
aggregate contract
event IDs / dedup
```

Questo è un contratto informativo downstream, non una feature online automaticamente disponibile.

---

# 22. Punti da mantenere fuori dal freeze se non supportati

Non chiudere artificialmente:

- market elasticity;
- livestock economics;
- opponent strategy;
- multiplayer fairness;
- routing optimality;
- policy thresholds;
- learned weights;
- economic optima;
- counterfactual metrics;
- non-R1 generalization;
- remote Kaggle fidelity non verificata.

Classificarli coerentemente come `PARTIALLY_KNOWN` o `NOT_ANALYZED`.

---

# 23. Verifica di coerenza verticale

Prima di chiudere, verificare:

```text
ONTOLOGY_C2 concept
    ↓
STATE_MACHINE_C2 transition/state
    ↓
FEATURE_MODEL_C2 observable/derived representation
```

Non è richiesta una biiezione.

`NONE_DIRECT` è legittimo quando un concetto ontologico non richiede una feature dedicata.

Segnalare:

- concetti upstream senza rappresentazione necessaria;
- feature senza upstream semantic basis;
- duplicazioni;
- overaggregation;
- feature candidate non supportate.

---

# 24. Verifiche

Eseguire almeno:

```powershell
git diff --check
.\.venv\Scripts\pytest.exe
```

Se `ruff` fa parte dei check correnti, eseguirlo.

Non eseguire episodi, benchmark o training.

Mostrare:

```powershell
git status --short
git diff -- docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
```

Non fare commit.

---

# 25. Stop condition

Dopo aver creato e verificato:

```text
docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
```

FERMARSI.

Non modificare:

```text
MODEL_SPEC_ANTIGRAVITY.md
MODEL_SPEC_CODEX.md
MODEL_SPEC_COPILOT.md
```

Non creare ancora consumer matrices definitive.

Non modificare runtime/policy.

---

# Output finale richiesto

Restituire in italiano:

1. path e stato del Feature Model C2;
2. numero totale di feature per information class;
3. modifiche C1 -> C2;
4. trattamento di `current_MODEL_SPEC_usage`;
5. lifecycle classifier e boundary cases;
6. clock/phase contract;
7. harvest readiness;
8. crop decay risk window;
9. need / eligibility / serviceability;
10. aggregate contracts completi e ancora incompleti;
11. workforce/inventory/market provenance;
12. telemetry/outcome classification;
13. schema della futura consumer matrix;
14. event-schema downstream;
15. punti `PARTIALLY_KNOWN` / `NOT_ANALYZED`;
16. verifica di coerenza verticale;
17. risultato `git diff --check`;
18. risultato test/lint;
19. `git status --short`;
20. eventuali blocker residui per il freeze.

Chiudere con:

```text
ONTOLOGY C2: CANDIDATE / NOT FROZEN
STATE MACHINE C2: CANDIDATE / NOT FROZEN
FEATURE MODEL C2: CANDIDATE CREATED / NOT FROZEN
MODEL_SPEC C2: NOT STARTED
CONSUMER MATRICES: NOT STARTED
FOUNDATION C2: NOT FROZEN
```

STOP.
