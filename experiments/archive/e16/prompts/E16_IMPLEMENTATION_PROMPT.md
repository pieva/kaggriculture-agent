# E16 --- IMPLEMENTATION PROMPT

**Stato:** `CANONICAL IMPLEMENTATION PROMPT`\
**Fase:** `E16 — TRAINING / IMPLEMENT`\
**Artefatto frozen di riferimento:**
`experiments/archive/e16/design/E16_TRAINING_DESIGN_FROZEN.md`

## Obiettivo

Implementa integralmente E16 secondo il disegno sperimentale frozen.

Non ridisegnare l'esperimento. Non modificare i fattori, i valori, i
seed, le celle, l'opponent, la regola di avanzamento, la telemetria
richiesta o il ruolo epistemico di E16.

E16 è **TRAINING**.

L'implementazione deve consentire di:

1.  eseguire l'instrumentation gate E0;
2.  eseguire Stage A;
3.  calcolare in modo deterministico il gate `C*`;
4.  eseguire Stage B solo se autorizzato dal gate;
5.  produrre risultati, telemetry e audit trail riproducibili;
6.  impedire deviazioni post hoc dal protocollo frozen.

------------------------------------------------------------------------

# 1. LETTURA OBBLIGATORIA

Prima di modificare codice o file, leggi integralmente:

1.  `README.md`;
2.  `docs/model_specs/post_e15/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md`;
3.  `experiments/archive/e16/design/E16_TRAINING_DESIGN_FROZEN.md`;
4.  la documentazione E15 necessaria a verificare gli artifact frozen;
5.  l'attuale struttura di runner, evaluation, telemetry, test e
    submission del repository.

Individua e verifica in particolare:

``` text
experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py
sha256 = 604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Non procedere se artifact e hash non corrispondono.

------------------------------------------------------------------------

# 2. REGOLE DI GOVERNANCE

Sono frozen e non modificabili:

``` text
quadrants_owned = 2

Stage A cells = 7
Stage B cells = 5

seed_1 = 1802163452
seed_2 = 1678077158

seat swap = mandatory

opponent =
experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py

opponent sha256 =
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Non:

-   cambiare seed;
-   aggiungere seed;
-   eliminare celle;
-   aggiungere celle;
-   cambiare opponent;
-   cambiare advancement rule;
-   usare `final_money` nel gate Stage B;
-   trasformare controlli in fattori;
-   cambiare valori perché un run "sembra migliore";
-   fare early stopping su performance;
-   produrre submission Kaggle;
-   modificare artifact E15 frozen;
-   aggiornare il MODEL_SPEC sulla base di smoke test;
-   chiamare E16 VALIDATION o TEST.

Se una specifica frozen non è implementabile senza alterarne il
significato, **STOP** e segnala il blocker. Non reinterpretarla
autonomamente.

------------------------------------------------------------------------

# 3. IMPLEMENTAZIONE COMUNE

Deve esistere una sola implementation E16 condivisa da tutte le celle.

La treatment build deve avere un hash unico.

Tra celle possono cambiare esclusivamente i parametri presenti nella
allowlist MANIPULATED.

La configurazione deve essere machine-readable e validabile.

Crea, se coerente con l'architettura corrente del repository, una
struttura equivalente a:

``` text
src/
  ... implementation E16 comune ...

scripts/
  run_e16_training.py
  validate_e16_instrumentation.py
  analyze_e16_stage_a.py
  analyze_e16_stage_b.py

configs/
  e16/
    E16_FROZEN_CONFIG.json

results/
  e16/
    instrumentation/
    stage_a/
    stage_b/
    analysis/
    manifests/

tests/
  test_e16_*.py
```

Adatta i percorsi allo stile reale del repository. Non introdurre una
nuova architettura se esistono già convenzioni equivalenti.

------------------------------------------------------------------------

# 4. CONFIGURAZIONE FROZEN

La configurazione deve rappresentare in modo esplicito almeno:

``` text
design_id
evidence_role
opponent_path
opponent_sha256
treatment_build_sha256
engine_version

quadrants_owned
workforce_headcount
livestock_species
crop_mix
feed_coverage_rule
operating_cash_rule
routing_module
hire_and_renewal_schedule
land_acquisition_timing
endgame_module

seed_list
seat_protocol

stage_a_cells
stage_b_cells

stage_b_gate
telemetry_schema_version
```

La config deve essere immutabile durante un run.

Il runner deve fallire in modo esplicito se:

-   hash opponent errato;
-   hash treatment inatteso;
-   cell id sconosciuto;
-   parametro non allowlisted cambia tra celle;
-   seed non previsto;
-   seat non previsto;
-   `quadrants_owned != 2`;
-   Stage B viene richiesto senza gate positivo.

------------------------------------------------------------------------

# 5. T0 E COMMON OPENING

Implementa:

``` text
T0 =
primo stato successivo all'esecuzione verificata
dell'acquisizione che porta quadrants_owned = 2
```

Prima di `T0`:

``` text
crop working set cap = 10
pasture acquisition = forbidden
livestock acquisition = forbidden
workforce schedule = common
routing = common
cash rule = common
land acquisition = common
```

Dopo `T0`:

``` text
quadrants_owned hard cap = 2
third quadrant order = forbidden
cell treatment parameters = active
all non-manipulated modules = identical
```

Se `T0` non viene raggiunto:

``` text
opening_failure = TRUE
policy_realization_failure = TRUE
episode retained
NO replacement seed
NO silent rerun
```

------------------------------------------------------------------------

# 6. STAGE A

Implementa esattamente le celle:

  Cell     watering_dispatch_priority   crop_working_set_target
  ------ ---------------------------- -------------------------
  A01                      LOW = 0.20                        10
  A02                     HIGH = 0.70                        10
  A03                      LOW = 0.20                        25
  A04                     HIGH = 0.70                        25
  A05                      MID = 0.45                        17
  A06                      MID = 0.45                        25
  A07                     HIGH = 0.70                        17

Controls Stage A:

``` text
quadrants_owned = 2
livestock_headcount_target = 4
pasture_allocation_target = 5
workforce_headcount = 10
species = Cow
crop mix = 40% Wheat / 40% Strawberry / 20% Melon
opponent = Copilot E15 frozen
```

### watering_dispatch_priority

È un PARAMETER di policy.

Non deve essere implementato come sinonimo di `watering_execution_rate`.

La policy deve esprimere l'intenzione di servizio dichiarata dalla
cella; la realizzazione viene misurata separatamente.

------------------------------------------------------------------------

# 7. STAGE A RUN MATRIX

Per ogni cella:

``` text
seed = 1802163452
  treatment P0 / opponent P1
  opponent P0 / treatment P1

seed = 1678077158
  treatment P0 / opponent P1
  opponent P0 / treatment P1
```

Totale:

``` text
7 × 2 × 2 = 28 episodes
```

Nessun run viene sostituito per gameplay failure o disqualification.

------------------------------------------------------------------------

# 8. GATE C\*

Dopo il completamento di tutte le 28 execution Stage A, calcola solo
sulle celle:

``` text
A02 -> crop target 10 / HIGH watering
A07 -> crop target 17 / HIGH watering
A04 -> crop target 25 / HIGH watering
```

Per ciascuna calcola:

``` text
completion_rate
median post-ramp watering_execution_rate
median watering_continuity
median crop_target_attainment
```

Steady window:

``` text
third full day after T0
through start of common endgame shutdown
```

Una cella è `CAPACITY_ELIGIBLE` se:

``` text
completion_rate >= 0.80
median watering_execution_rate >= 0.60
median watering_continuity >= 0.75
median crop_target_attainment >= 0.80
```

Poi:

``` text
C* = largest crop target among CAPACITY_ELIGIBLE cells
```

`final_money` deve essere tecnicamente impossibile da usare nel calcolo
del gate.

Se nessuna cella è eleggibile:

``` text
STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR
```

e il runner deve impedire l'esecuzione Stage B.

Produci un artifact machine-readable del gate con:

``` text
eligible_cells
metrics_by_cell
selected_C_star
gate_status
input_result_hashes
analysis_code_hash
timestamp
```

------------------------------------------------------------------------

# 9. STAGE B

Stage B viene abilitato solo da un gate positivo.

Controls:

``` text
watering_dispatch_priority = HIGH 0.70
crop_working_set_target = C*
quadrants_owned = 2
workforce_headcount = 10
species = Cow
```

Celle:

  Cell     herd target   pasture target
  ------ ------------- ----------------
  B01                4                5
  B02                4               18
  B03               10               11
  B04               10               18
  B05               17               18

Run matrix identica:

``` text
5 cells × 2 seeds × 2 seats = 20 episodes
```

Totale massimo E16:

``` text
28 + 20 = 48 episodes
```

------------------------------------------------------------------------

# 10. INSTRUMENTATION GATE E0

Prima dei run TRAINING esegui smoke test non analitici.

Devono verificare almeno:

``` text
event ledger present
requested != executed distinction
accepted / partial / executed / failed / no-op states
realized_price reconciliation
realized_value reconciliation
cash before/after reconciliation
inventory flow reconciliation
failure reason coverage
treatment build hash
opponent hash
configuration hash
quadrants_owned numeric semantics
T0 detection
seat detection
seed detection
cell config allowlist
```

Smoke run:

-   non conta come TRAINING;
-   non entra nei risultati Stage A/B;
-   non aggiorna bound;
-   non aggiorna MODEL_SPEC.

Se E0 fallisce, **non eseguire E16**.

------------------------------------------------------------------------

# 11. EVENT LEDGER

Ogni event record deve contenere almeno:

``` text
design_id
stage
cell_id
episode_id
seed
treatment_seat
player
step
day
hour
actor_or_order_id
actor_or_order_type
target_tile_or_commodity

requested_payload
executed_payload
success
failure_or_noop_reason

requested_quantity
executed_quantity

displayed_price_at_request
realized_price
realized_value

cash_flow_category
cash_before
cash_after

relevant_state_before
relevant_state_after
provenance

treatment_build_sha256
opponent_sha256
engine_version
configuration_sha256

quadrants_owned
```

Distingui almeno:

``` text
requested
accepted
partially_executed
executed
failed
no_op
```

Non inferire execution dalla sola presenza di una request.

------------------------------------------------------------------------

# 12. STATE TELEMETRY

Registra almeno:

``` text
assigned_crop_target
achieved_crop_surface

assigned_watering_priority
watering_need_denominator
successful_watering_effects

assigned_herd_target
achieved_herd

assigned_pasture_target
achieved_pasture

workforce_state
worker_capacity

pasture_occupancy
feed_demand
feed_coverage

purchase_to_activation_lag

necessary_transit
avoidable_transit

terminal_inventory_by_product
unsold_inventory_quantity
unsold_inventory_value_estimate
```

`unsold_inventory_value_estimate`:

-   deve avere metodo esplicito;
-   deve avere provenance;
-   non è `realized_value`;
-   non può essere sommato al cash realizzato salvo esplicita semantica
    dell'environment.

------------------------------------------------------------------------

# 13. DERIVED METRICS

Implementa:

``` text
watering_execution_rate =
unique successful crop-day WATER effects
/
unique crop-day watering needs
```

``` text
watering_continuity =
productive days with watering_execution_rate >= 0.50
/
productive days
```

``` text
crop_target_attainment =
daily active crop surface
/
assigned crop target
```

``` text
pasture_occupancy =
occupied pasture
/
constructed pasture
```

``` text
action_failure_rate =
failed_or_noop actor actions
/
requested actor actions
```

Riporta separatamente:

``` text
active_crop_surface
serviced_crop_surface
surviving_crop_surface
harvest_ready_surface
crop_losses

realized_cash_flow_by_category

livestock_acquisition_cost
feed_cost
livestock_service_cost
livestock_product_realized_value

product_generated
product_collected
product_stored
product_sold

terminal_unsold_inventory

worker_capacity
worker_utilization

necessary_transit
avoidable_transit
```

Non costruire un composite score con `final_money`.

------------------------------------------------------------------------

# 14. ANALYSIS IMPLEMENTATION

Implementa un'analisi riproducibile che produca raw episode data e
paired contrasts.

## Stage A

``` text
A02 - A01
A04 - A03

(A04 - A03) - (A02 - A01)

A03 -> A06 -> A04

A02 -> A07 -> A04

A05 vs corner interpolation
```

## Stage B

``` text
B02 - B01
B04 - B03

(B04 - B03) - (B02 - B01)

B02 -> B04 -> B05
```

Per ogni contrasto mostra:

``` text
raw values by seed
raw values by seat
paired differences
sign consistency
median
range
```

Mean/std possono essere supplementari.

Non usare asymptotic p-values come prova di validation.

Con 2 seed, una direzione incoerente tra seed deve rimanere
`UNRESOLVED`.

------------------------------------------------------------------------

# 15. FAILURE POLICY

Gameplay failure/disqualification:

``` text
retain as outcome
NO automatic rerun
NO replacement seed
```

Infrastructure failure verificato:

``` text
rerun allowed only with exact same:
cell
seed
seat
treatment hash
opponent hash
engine hash
configuration
```

Conserva entrambi i tentativi nell'audit trail.

Nessuna outlier deletion.

Nessuna winsorization.

Nessuna seed exclusion post hoc.

------------------------------------------------------------------------

# 16. TEST OBBLIGATORI

Aggiungi test automatici almeno per:

1.  opponent path/hash;
2.  cell count = 7 + 5;
3.  exact Stage A values;
4.  exact Stage B values;
5.  exact seeds;
6.  seat swap completeness;
7.  `quadrants_owned == 2`;
8.  third-quadrant acquisition forbidden;
9.  Stage B blocked without valid gate;
10. `final_money` absent from gate logic;
11. manipulated-field allowlist;
12. identical control config across cells;
13. event ledger schema;
14. requested/executed distinction;
15. derived metrics;
16. T0 detection;
17. no replacement seed;
18. hash/config fail-closed behavior;
19. total episode count = 28 or 48 as appropriate;
20. deterministic/reproducible gate result.

Esegui l'intera test suite esistente, non solo i nuovi test.

------------------------------------------------------------------------

# 17. OUTPUT ARTIFACTS

Produci almeno:

``` text
experiments/archive/e16/artifacts/manifests/E16_IMPLEMENTATION_MANIFEST.json
experiments/archive/e16/artifacts/instrumentation/E16_E0_REPORT.md
experiments/archive/e16/artifacts/stage_a/E16_STAGE_A_RUN_MANIFEST.json
experiments/archive/e16/artifacts/analysis/E16_STAGE_A_ANALYSIS.md
experiments/archive/e16/artifacts/analysis/E16_STAGE_B_GATE.json
```

Se Stage B autorizzato:

``` text
results/e16/stage_b/E16_STAGE_B_RUN_MANIFEST.json
results/e16/analysis/E16_STAGE_B_ANALYSIS.md
experiments/archive/e16/artifacts/analysis/E16_TRAINING_REPORT.md
```

Se Stage B bloccato:

``` text
experiments/archive/e16/artifacts/analysis/E16_TRAINING_REPORT.md
```

deve dichiarare:

``` text
STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR
```

e spiegare quale requisito non è stato soddisfatto.

------------------------------------------------------------------------

# 18. IMPLEMENTATION MANIFEST

Il manifest deve includere:

``` text
design_id
evidence_role = TRAINING

git_commit
git_dirty_state

treatment_build_path
treatment_build_sha256

opponent_path
opponent_sha256

engine_version
environment_version

config_path
config_sha256

telemetry_schema_version

seed_list
seat_protocol

stage_a_cell_ids
stage_b_cell_ids

instrumentation_gate_status

stage_a_status
stage_b_gate_status
stage_b_status
```

------------------------------------------------------------------------

# 19. STOP CONDITIONS

Interrompi e segnala BLOCKER se:

-   opponent hash non corrisponde;
-   frozen design manca o è incoerente;
-   environment non consente di distinguere request da execution e non
    esiste un modo affidabile per strumentarlo;
-   non puoi implementare `quadrants_owned = 2` hard cap;
-   il runner non può garantire cell/seed/seat/config identity;
-   Stage B gate non può essere calcolato senza deviazioni dal frozen
    design;
-   una modifica necessaria richiederebbe cambiare MODEL_SPEC o design
    frozen.

Non aggirare un blocker con una modifica implicita.

------------------------------------------------------------------------

# 20. WORKFLOW OPERATIVO

Procedi in questo ordine:

``` text
1. INSPECT
2. PLAN
3. IMPLEMENT
4. TEST
5. BUILD/FREEZE TREATMENT ARTIFACT
6. RUN E0 INSTRUMENTATION GATE
7. STOP AND REPORT E0 RESULT
```

**Non eseguire ancora i 28 episodi Stage A nello stesso passaggio, salvo
istruzione esplicita successiva.**

Il primo obiettivo è consegnare un'implementazione E16 pronta e
verificata, con E0 superato.

------------------------------------------------------------------------

# 21. REPORT FINALE DI QUESTO PASSAGGIO

Concludi con:

``` text
IMPLEMENTATION_STATUS: READY | BLOCKED
TESTS: <passed>/<total>
TREATMENT_BUILD_SHA256: ...
OPPONENT_SHA256_VERIFIED: YES | NO
CONFIG_SHA256: ...
E0_STATUS: PASS | FAIL | NOT_RUN
STAGE_A_READY: YES | NO
BLOCKERS: NONE | ...
FILES_CHANGED:
  ...
```

Se `E0_STATUS != PASS`, allora:

``` text
STAGE_A_READY = NO
```

Non avviare Stage A.

Il compito termina quando l'implementazione è pronta e l'instrumentation
gate E0 è stato verificato.
