# Kaggriculture Feature Model C2

```text
CANDIDATE C2
NOT FROZEN
CONSUMER-NEUTRAL
UPSTREAM:
  - ONTOLOGY_C2 CANDIDATE
  - STATE_MACHINE_C2 CANDIDATE
DERIVED FROM FOUNDATION RECONCILIATION R1
REMEDIATION R2: CODEX FEATURE MODEL C2 REVIEW R1
```

## 1. Scope and remediation status

This file is a remediation pass against the Codex review of the C2 candidate. It addresses only the issues mandated by the review and does not add a new model layer, new policy, new runtime behavior, or any consumer-specific matrix.

The scope is restricted to:

- P0-01, P0-02, P1-01, P1-02, P1-03, P1-04, P2-01, P2-02
- preserving NOTE-01 and NOTE-02

The resulting artifact is still a candidate and not frozen:

```text
FEATURE MODEL C2 STATUS: CANDIDATE / NOT FROZEN
```

## 2. P0-01 resolution: a real canonical catalog

The feature model contains a real catalog keyed by the canonical C1 IDs. The C2 candidate preserves the admissible canonical IDs validated in C1 and keeps the rejected deterministic RNG concept outside the admissible feature count. No silent 59 -> 74 expansion is accepted. The catalog is the common information contract and not a per-consumer usage map.

ANTIGRAVITY_FOUNDATION_REVIEW_R1: READ

### 2.1 Real total and class counts

```text
Real feature catalog total = 58
ENGINE_STATE: 14
RAW_OBSERVABLE: 5
DERIVED_FEATURE: 33
POLICY_CONTEXT: 2
TELEMETRY_ONLY: 3
OUTCOME_LABEL: 1
```

This total is the result of the admissible canonical catalog after excluding the rejected deterministic future-RNG record `REJ-01`, which remains only in the rejected ledger. Pure event and provenance fields are not counted as feature objects in this common model.

### 2.2 Canonical catalog

| feature_id | name | information_class | type | ontology_mapping | state_machine_mapping | source_variables | derivation_or_formula | formula_version | granularity | authoritative_clock | sampling_phase | online_available | decision_time_available | future_leakage | evidence_status | validity_limits | CONTRACT_SCHEMA_COMPLETE | FEATURE_FORMULA_COMPLETE | freeze_ready |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TMP-01 | step current | ENGINE_STATE | RAW | NONE_DIRECT | STEP_OPEN | observation.step | identity | v1 | episode-step | engine_step | current step | YES | YES | NO | ENGINE_VERIFIED | N/A | YES | YES | YES |
| TMP-02 | day current | ENGINE_STATE | RAW | crop_horizon_alignment | global clock | observation.day | identity | v1 | day | day | current day | YES | YES | NO | ENGINE_VERIFIED | N/A | YES | YES | YES |
| TMP-03 | hour current | ENGINE_STATE | RAW | crop_decay_risk_window | phase within day | observation.hour | identity | v1 | action phase | hour | current phase | YES | YES | NO | ENGINE_VERIFIED | N/A | YES | YES | YES |
| TMP-04 | canonical_step | DERIVED_FEATURE | DERIVED | NONE_DIRECT | diagnostic reconstruction | day,hour,turnsPerDay | day*turnsPerDay+hour | v1 | action phase | canonical_step | post-sample diagnostics | YES | YES | NO | DERIVED | diagnostic only | YES | YES | NO |
| TMP-05 | action_phases_until_eod_refresh | DERIVED_FEATURE | TIMING_CONSTRAINT | crop_decay_risk_window | pre-EOD action window | hour,turnsPerDay | turnsPerDay-hour inclusive | v1 | tile-day/action phase | hour | pre-refresh | YES | YES | NO | DERIVED | requires known turnsPerDay | YES | YES | NO |
| FRM-01 | farm_money_current | ENGINE_STATE | RAW | operating_cash_buffer | farm state | farm.money | identity | v1 | player-step | engine_step | pre-action | YES | YES | NO | ENGINE_VERIFIED | not equal to buffer | YES | YES | YES |
| FRM-02 | tile_grid_raw | RAW_OBSERVABLE | RAW | activated_land_surface, field_cleanliness_state | all tile states | farm.tiles | identity | v1 | player-board-step | engine_step | current board snapshot | YES | YES | NO | ENGINE_VERIFIED | snapshot scope only | YES | YES | YES |
| FRM-03 | working_set_member | POLICY_CONTEXT | POLICY_ASSIGNMENT_CONTEXT | crop_surface_maintained | working-set membership | policy assignment | membership in working map | v1 | tile | N/A | decision context | YES | YES | NO | DERIVED | policy-only | YES | YES | YES |
| FRM-04 | land_surface_total | DERIVED_FEATURE | AGGREGATE | land_surface_total | unlocked vs LOCKED | unlocked_quadrants or tile grid | count of owned or unlocked land | v1 | player-step | engine_step | current board | YES | YES | NO | ENGINE_VERIFIED | scope must be declared | YES | YES | YES |
| FRM-05 | activated_land_surface | DERIVED_FEATURE | AGGREGATE | activated_land_surface | productive / structure tiles | tile grid + activation rule | count of active productive area | v1 | player-step/window | engine_step | pre-action | YES | YES | NO | PARTIALLY_KNOWN | board and ownership scope required | NO | NO | NO |
| CRP-01 | tile_kind | ENGINE_STATE | CATEGORICAL | field_cleanliness_state | None, LOCKED, PLANT, WEED | tile.kind | normalize native tile value | v1 | tile-step | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | invalid values outside domain | YES | YES | YES |
| CRP-02 | crop_id_and_rules | ENGINE_STATE | CATEGORICAL | crop_care_action_flow | ongoing / non-ongoing schedule | tile.crop + CROPS rules | lookup rule table | v1 | tile-cycle | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | requires valid crop metadata | YES | YES | YES |
| CRP-03 | planted_day | ENGINE_STATE | RAW | crop_horizon_alignment | plant origin clock | tile.planted_day | identity | v1 | tile-cycle | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | only for PLANT | YES | YES | YES |
| CRP-04 | crop_age_days | DERIVED_FEATURE | DERIVED | crop_horizon_alignment | growth / maturity | day, planted_day | day-planted_day | v1 | tile-step | day | pre-action | YES | YES | NO | DERIVED | requires valid day and planted_day | YES | YES | YES |
| CRP-05 | yield_units | ENGINE_STATE | RAW | crop_harvest_action_flow | yield held by tile | tile.yield_units | identity | v1 | tile-step | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | not equivalent to harvest readiness | YES | YES | YES |
| CRP-06 | watered_today | ENGINE_STATE | PREDICATE | watering_execution_rate | daily watering flag | tile.watered_today | identity | v1 | tile-day/step | day | pre-refresh and decision phase | YES | YES | NO | ENGINE_VERIFIED | reset daily by EOD | YES | YES | YES |
| CRP-07 | consecutive_unwatered | ENGINE_STATE | RAW | crop_decay_risk_window | EOD care counter | tile.consecutive_unwatered | identity | v1 | tile-day | day | EOD refresh | YES | YES | NO | ENGINE_VERIFIED | requires valid day semantics | YES | YES | YES |
| CRP-08 | max_lifespan_step | ENGINE_STATE | RAW | crop_decay_risk_window | onset decay | tile.max_lifespan_step | identity | v1 | tile-cycle | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | not enough alone for RETIREMENT_DUE | YES | YES | YES |
| CRP-09 | tile_lifecycle_state | DERIVED_FEATURE | CATEGORICAL | crop_care_action_flow, crop_harvest_action_flow, crop_decay_risk_window | OUT_OF_SCOPE, EMPTY_ASSIGNED, GROWING, HARVEST_READY, RETIREMENT_DUE, LOST_WEED | tile, day, hour, working set, crop rules | precedence-based classifier | v2 | tile-step | engine_step | current state | YES | YES | NO | DERIVED | invalid inputs outside lifecycle are diagnostic errors | YES | YES | YES |
| CRP-10 | harvest_ready | DERIVED_FEATURE | PREDICATE | crop_harvest_action_flow | GROWING to HARVEST_READY | tile.kind, tile.yield_units, tile.planted_day, day, crop rule | tile.kind == PLANT and yield_units > 0 and age >= first_yield_day | v2 | tile-step | day | action decision | YES | YES | NO | ENGINE_VERIFIED + DERIVED | not identical to yield_units > 0 | YES | YES | YES |
| CRP-11 | care_due | DERIVED_FEATURE | PREDICATE | crop_care_completion_rate | orthogonal care state | tile.kind, tile.watered_today | PLANT and not watered today | v1 | tile-step | day|hour | pre-action and pre-refresh | YES | YES | NO | DERIVED | requires valid crop and current day | YES | YES | YES |
| CRP-12 | water_loss_at_eod_if_unserved | DERIVED_FEATURE | PREDICATE | crop_decay_risk_window | deterministic EOD loss boundary | care_due, consecutive_unwatered | care_due and counter+1 >= 2 | v1 | tile-action phase | day | EOD refresh | YES | YES | NO | DERIVED | uses day-based EOD semantics | YES | YES | YES |
| CRP-13 | lifespan_decay_started | DERIVED_FEATURE | PREDICATE | crop_decay_risk_window | decay phase | max_lifespan_step, engine_step | step >= max_lifespan_step and ongoing state active | v1 | tile-step | engine_step | pre-action and decay phase | YES | YES | NO | DERIVED | not by itself RETIREMENT_DUE | YES | YES | YES |
| CRP-14 | next_lifespan_decay_phase | DERIVED_FEATURE | TIMING_CONSTRAINT | crop_decay_risk_window | next even-offset decay | max_lifespan_step, engine_step, turnsPerDay | next deterministic decay boundary | v1 | tile-action phase | engine_step | pre-action and decay phase | YES | YES | NO | DERIVED | requires engine phase contract | YES | YES | YES |
| CRP-15 | lifespan_loss_phase_if_no_action | DERIVED_FEATURE | TIMING_CONSTRAINT | crop_decay_risk_window | deterministic no-action loss | max_lifespan_step, yield_units, action history | next decay step causing yield loss if no action | v1 | tile-cycle | engine_step | pre-action | YES | YES | NO | DERIVED | no final incoming outcome | YES | YES | YES |
| CRP-16 | empty_random_weed_eligible | DERIVED_FEATURE | PREDICATE | crop_decay_risk_window, field_cleanliness_state | EMPTY_ASSIGNED to LOST_WEED exposure | tile, working set, EOD phase | empty tile eligible for weed-hazard draw | v1 | tile-EOD | day|hour | EOD exposure check | YES | YES | NO | DERIVED | stochastic spawn not deterministic | YES | YES | YES |
| CRP-17 | crop_decay_risk_window | DERIVED_FEATURE | TIMING_CONSTRAINT | crop_decay_risk_window | structured multi-cause risk window | CRP-11, CRP-12, CRP-13, CRP-14, CRP-15, CRP-16 | multi-cause constraint object | v1 | tile-action phase | engine_step + day|hour | current decision window | YES | YES | NO | DERIVED | no scalar score | YES | YES | YES |
| CRP-18 | active_crop_surface | DERIVED_FEATURE | AGGREGATE | crop_surface_maintained | count PLANT | tile grid, tile.kind | count(tile.kind == PLANT) | v1 | player-step | engine_step | current snapshot | YES | YES | NO | DERIVED | board scope and ownership scope required | NO | YES | NO |
| CRP-19 | crop_surface_maintained | DERIVED_FEATURE | AGGREGATE | crop_surface_maintained | maintained lifecycle states | tile grid, tile lifecycle, maintenance rule | count of tiles in valid maintained set | v1 | player-day/window | engine_step | pre-refresh or decision phase | YES | YES | NO | PARTIALLY_KNOWN | active != maintained; formula incomplete unless scope is defined | NO | NO | NO |
| CRP-20 | watering_execution_rate | DERIVED_FEATURE | AGGREGATE | watering_execution_rate | executed WATER over need | watering requests, execution events, care need | executed_water / eligible_water_need | v1 | player-day/window | engine_step | action or current window | YES | YES | NO | PARTIALLY_KNOWN | denominator must be canonical | NO | NO | NO |
| CRP-21 | watering_continuity | DERIVED_FEATURE | AGGREGATE | watering_continuity | service persistence | daily watering records | consecutive or sustained service ratio | v1 | player-window | day | time-window based | YES | YES | NO | PARTIALLY_KNOWN | denominators and schedule lag not formalized | NO | NO | NO |
| CRP-22 | crop_care_completion_rate | DERIVED_FEATURE | AGGREGATE | crop_care_completion_rate | completion of explicit needs | care events, care demand, tile states | completed care / declared care needs | v1 | player-day/window | day | current decision window | YES | YES | NO | PARTIALLY_KNOWN | denominator ambiguous | NO | NO | NO |
| CRP-23 | crop_harvest_action_flow | DERIVED_FEATURE | AGGREGATE | crop_harvest_action_flow | readiness-to-collection flow | harvest requests, execution outcomes, yield | readiness events -> executed harvest breakdown | v1 | player-window | engine_step | action and follow-through | YES | YES | NO | PARTIALLY_KNOWN | request vs executed must be separated | NO | NO | NO |
| CRP-24 | field_cleanliness_state | DERIVED_FEATURE | AGGREGATE | field_cleanliness_state | distribution of WEED | tile grid, tile.kind | map of clean vs weed-impacted tiles | v1 | board-step | engine_step | board snapshot | YES | YES | NO | PARTIALLY_KNOWN | weed mapping requires scope | NO | NO | NO |
| CRP-25 | weed_backlog_cost | DERIVED_FEATURE | AGGREGATE | weed_backlog_cost | recovery burden | weed positions, action history, schedule | backlog cost proxy not canonical | v1 | player-window | engine_step | current window | YES | YES | NO | PARTIALLY_KNOWN | no stable formula | NO | NO | NO |
| WRK-01 | unit_positions | RAW_OBSERVABLE | RAW | movement_overhead | worker positions | farmer, hands, tile positions | identity | v1 | unit-step | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | reachability and occupancy separate | YES | YES | YES |
| WRK-02 | workforce_headcount | DERIVED_FEATURE | AGGREGATE | workforce_headcount | available workers | farmer, hands | 1 + len(hands) where applicable | v1 | player-step/day | engine_step | pre-action | YES | YES | NO | DERIVED | not equal to service capacity | YES | YES | YES |
| WRK-03 | worker_capacity_available | DERIVED_FEATURE | AGGREGATE | worker_capacity_available | action slots available | active units, time windows, action rules | theoretical capacity with explicit denominator | v1 | player-step/window | engine_step | pre-action | YES | YES | NO | PARTIALLY_KNOWN | missing canonical denominator | NO | NO | NO |
| WRK-04 | movement_overhead | DERIVED_FEATURE | AGGREGATE | movement_overhead | MOVE consumption | action history, unit positions | movement count or distance cost | v1 | player-window | engine_step | current window | YES | YES | NO | PARTIALLY_KNOWN | routing and contention not yet canonical | NO | NO | NO |
| WRK-05 | action_dispatch_failure | DERIVED_FEATURE | AGGREGATE | action_dispatch_failure | no-effect or rejected action | requested, executed, state delta | classify request and execution mismatch | v1 | action/window | engine_step | post-action | YES | YES | NO | PARTIALLY_KNOWN | requires event provenance | NO | NO | NO |
| WRK-06 | productive_action_share | DERIVED_FEATURE | AGGREGATE | productive_action_share | useful action composition | classified action history | useful actions / declared denominator | v1 | player-window | engine_step | current window | YES | YES | NO | PARTIALLY_KNOWN | denominator not canonical | NO | NO | NO |
| LIV-01 | livestock_headcount | DERIVED_FEATURE | AGGREGATE | livestock_headcount | occupied animal structures | tile grid, animal id | count per species | v1 | player-step | engine_step | current board | YES | YES | NO | PARTIALLY_KNOWN | species scope required | NO | NO | NO |
| LIV-02 | animal_service_state | DERIVED_FEATURE | CATEGORICAL | feed_availability, livestock_product_flow | fed / cared / unfed / yield flags | animal tile fields | tuple-like service state | v1 | animal-step | day|hour | current animal state | YES | YES | NO | PARTIALLY_KNOWN | requires explicit feed and care conjunction | NO | NO | NO |
| LIV-03 | feed_availability | DERIVED_FEATURE | AGGREGATE | feed_availability | available WHEAT feed | shed, inventory, production | available feed by compartment | v1 | player-step | engine_step | current state | YES | YES | NO | PARTIALLY_KNOWN | inventory provenance and EOD semantics required | NO | NO | NO |
| LIV-04 | pasture_surface_maintained | DERIVED_FEATURE | AGGREGATE | pasture_surface_maintained | functional pasture | tile grid, occupancy/service rule | maintained pasture count | v1 | player-day/window | engine_step | decision phase | YES | YES | NO | PARTIALLY_KNOWN | definition incomplete | NO | NO | NO |
| LIV-05 | livestock_product_flow | DERIVED_FEATURE | AGGREGATE | livestock_product_flow | production-collection-sale | animal yield, harvest, inventory, sell | stage-wise product flow | v1 | player-window | day | current period | YES | YES | NO | PARTIALLY_KNOWN | product and price provenance not canonical | NO | NO | NO |
| INV-01 | seed_inventory | ENGINE_STATE | RAW | planting_action_flow | PLANT resource | private.seeds | identity by crop | v1 | player-step | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | inventory is crop-specific | YES | YES | YES |
| INV-02 | shed_inventory | ENGINE_STATE | RAW | shed_inventory_integrity, inventory_to_cash_conversion | persistent storage | private.shed | identity by item | v1 | player-step | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | real provenance across EOD transfer | YES | YES | YES |
| INV-03 | worker_inventory | ENGINE_STATE | RAW | contract_inventory_loss | transient carried items | private.inventories | identity by unit and item | v1 | unit-step | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | not equal to return obligation | YES | YES | YES |
| INV-04 | inventory_to_cash_conversion | DERIVED_FEATURE | AGGREGATE | inventory_to_cash_conversion | collected / stored / sold chain | inventory deltas, sell executions, cash deltas | converted quantity / value over window | v1 | player-window | engine_step | post-action or current window | YES | YES | NO | PARTIALLY_KNOWN | conversion and liquidated value semantics ambiguous | NO | NO | NO |
| MKT-01 | market_state_current | RAW_OBSERVABLE | RAW | dynamic_market_price_elasticity | shared prices and inventory | observation market | identity | v1 | product-step | engine_step | current market state | YES | YES | NO | ENGINE_VERIFIED | requires current quote semantics | YES | YES | YES |
| MKT-02 | market_transaction_value | TELEMETRY_ONLY | AGGREGATE | market_transaction_value | executed BUY / SELL value | realized quantity, realized price | sum executed_quantity * realized_price | v1 | order/transaction | engine_step | post-action | NO | NO | YES | TELEMETRY_ONLY | not pre-action input | YES | YES | NO |
| MKT-03 | operating_cash_buffer | POLICY_CONTEXT | DERIVED | operating_cash_buffer | cash relative to declared obligations | current money + obligations model | money minus obligations | v1 | player-step/window | engine_step | decision phase | YES | YES | NO | PARTIALLY_KNOWN | obligations and threshold not canonical | NO | NO | NO |
| MKT-04 | market_order_batch_limit | RAW_OBSERVABLE | TIMING_CONSTRAINT | market_order_batch_limit | market phase capacity | configuration max orders and remaining slots | structural limit and remaining slots | v1 | player-step | engine_step | current market phase | YES | YES | NO | ENGINE_VERIFIED | requires market config validity | YES | YES | YES |
| GLB-01 | opponent_public_farm_state | RAW_OBSERVABLE | RAW | NONE_DIRECT | other public farm | farms[opponent] | identity | v1 | opponent-board-step | engine_step | current state | YES | YES | NO | ENGINE_VERIFIED | limited to public fields | YES | YES | YES |
| GLB-02 | action_execution_result | TELEMETRY_ONLY | CATEGORICAL | action_dispatch_failure | requested / accepted / executed / no-op | wrapper event before and after | post-action attribution | v1 | action event | engine_step | post-action | NO | NO | YES | TELEMETRY_ONLY | not a decision-time input | YES | YES | NO |
| GLB-03 | transition_reason | TELEMETRY_ONLY | CATEGORICAL | observability support | action / EOD / decay / RNG reason | instrumented transition log | post-transition attribution | v1 | transition event | engine_step | post-transition | NO | NO | YES | TELEMETRY_ONLY | not a policy input | YES | YES | NO |
| LBL-01 | final_money_outcome | OUTCOME_LABEL | AGGREGATE | final_money_outcome | terminal reward | terminal money reward | identity at terminal state | v1 | episode/player | terminal state | terminal | NO | NO | YES | OUTCOME_LABEL | terminal only | YES | YES | NO |

### 2.3 Migration C1 -> C2

The migration is exhaustive for the 59 canonical C1 IDs. No new feature IDs are introduced in C2 beyond the canonical IDs. This is a clarification and cleanup, not an expansion.

| feature_id | C1 name/class | C2 name/class | change_type | reason | compatibility | replacement_or_split |
|---|---|---|---|---|---|---|
| TMP-01 | step current / RAW_OBSERVABLE | step current / ENGINE_STATE | CLARIFIED | explicit engine contract | compatible | N/A |
| TMP-02 | day current / RAW_OBSERVABLE | day current / ENGINE_STATE | CLARIFIED | clock semantics clarified | compatible | N/A |
| TMP-03 | hour current / RAW_OBSERVABLE | hour current / ENGINE_STATE | CLARIFIED | phase semantics clarified | compatible | N/A |
| TMP-04 | canonical_step / DERIVED_FEATURE | canonical_step / DERIVED_FEATURE | CLARIFIED | preserved as diagnostic only | compatible | N/A |
| TMP-05 | action_phases_until_eod_refresh / DERIVED_FEATURE | action_phases_until_eod_refresh / DERIVED_FEATURE | CLARIFIED | phase and clock precision fixed | compatible | N/A |
| FRM-01 | farm_money_current / RAW_OBSERVABLE | farm_money_current / ENGINE_STATE | RECLASSIFIED | current money is not equal to cash buffer | compatible | N/A |
| FRM-02 | tile_grid_raw / RAW_OBSERVABLE | tile_grid_raw / RAW_OBSERVABLE | UNCHANGED | retained | compatible | N/A |
| FRM-03 | working_set_member / POLICY_CONTEXT | working_set_member / POLICY_CONTEXT | UNCHANGED | retained | compatible | N/A |
| FRM-04 | land_surface_total / DERIVED_FEATURE | land_surface_total / DERIVED_FEATURE | UNCHANGED | retained | compatible | N/A |
| FRM-05 | activated_land_surface / DERIVED_FEATURE | activated_land_surface / DERIVED_FEATURE | CLARIFIED | scope and board ownership clarified | compatible | N/A |
| CRP-01 | tile_kind / RAW_OBSERVABLE | tile_kind / ENGINE_STATE | RECLASSIFIED | engine-native state semantics | compatible | N/A |
| CRP-02 | crop_id_and_rules / RAW_OBSERVABLE | crop_id_and_rules / ENGINE_STATE | RECLASSIFIED | recipe metadata is engine-relevant state | compatible | N/A |
| CRP-03 | planted_day / RAW_OBSERVABLE | planted_day / ENGINE_STATE | RECLASSIFIED | clock-source contract clarified | compatible | N/A |
| CRP-04 | crop_age_days / DERIVED_FEATURE | crop_age_days / DERIVED_FEATURE | UNCHANGED | retained | compatible | N/A |
| CRP-05 | yield_units / RAW_OBSERVABLE | yield_units / ENGINE_STATE | RECLASSIFIED | engine state and not policy abstraction | compatible | N/A |
| CRP-06 | watered_today / RAW_OBSERVABLE | watered_today / ENGINE_STATE | RECLASSIFIED | daily care flag is engine state | compatible | N/A |
| CRP-07 | consecutive_unwatered / RAW_OBSERVABLE | consecutive_unwatered / ENGINE_STATE | RECLASSIFIED | EOD care counter remains engine state | compatible | N/A |
| CRP-08 | max_lifespan_step / RAW_OBSERVABLE | max_lifespan_step / ENGINE_STATE | RECLASSIFIED | engine state not derived | compatible | N/A |
| CRP-09 | tile_lifecycle_state / DERIVED_FEATURE | tile_lifecycle_state / DERIVED_FEATURE | FORMULA_VERSIONED | total classifier and precedence formalized | compatible | N/A |
| CRP-10 | harvest_ready / DERIVED_FEATURE | harvest_ready / DERIVED_FEATURE | FORMULA_VERSIONED | formula explicitly fixed with crop rule maturity gate | compatible | N/A |
| CRP-11 | care_due / DERIVED_FEATURE | care_due / DERIVED_FEATURE | FORMULA_VERSIONED | clarified as orthogonal to lifecycle | compatible | N/A |
| CRP-12 | water_loss_at_eod_if_unserved / DERIVED_FEATURE | water_loss_at_eod_if_unserved / DERIVED_FEATURE | UNCHANGED | retained | compatible | N/A |
| CRP-13 | lifespan_decay_started / DERIVED_FEATURE | lifespan_decay_started / DERIVED_FEATURE | CLARIFIED | not equivalent to RETIREMENT_DUE | compatible | N/A |
| CRP-14 | next_lifespan_decay_phase / DERIVED_FEATURE | next_lifespan_decay_phase / DERIVED_FEATURE | CLARIFIED | clock source corrected | compatible | N/A |
| CRP-15 | lifespan_loss_phase_if_no_action / DERIVED_FEATURE | lifespan_loss_phase_if_no_action / DERIVED_FEATURE | CLARIFIED | corrected phase and no-action semantics | compatible | N/A |
| CRP-16 | empty_random_weed_eligible / DERIVED_FEATURE | empty_random_weed_eligible / DERIVED_FEATURE | CLARIFIED | hazard semantics preserved | compatible | N/A |
| CRP-17 | crop_decay_risk_window / DERIVED_FEATURE | crop_decay_risk_window / DERIVED_FEATURE | CLARIFIED | kept as structured risk object | compatible | N/A |
| CRP-18 | active_crop_surface / DERIVED_FEATURE | active_crop_surface / DERIVED_FEATURE | FORMULA_VERSIONED | base formula count(tile.kind == PLANT) preserved | compatible | N/A |
| CRP-19 | crop_surface_maintained / DERIVED_FEATURE | crop_surface_maintained / DERIVED_FEATURE | FORMULA_VERSIONED | maintained != active; formula remains incomplete | partial | N/A |
| CRP-20 | watering_execution_rate / DERIVED_FEATURE | watering_execution_rate / DERIVED_FEATURE | CLARIFIED | denominator and phase clarified | partial | N/A |
| CRP-21 | watering_continuity / DERIVED_FEATURE | watering_continuity / DERIVED_FEATURE | CLARIFIED | denominator and schedule clarified | partial | N/A |
| CRP-22 | crop_care_completion_rate / DERIVED_FEATURE | crop_care_completion_rate / DERIVED_FEATURE | CLARIFIED | denominator still incomplete | partial | N/A |
| CRP-23 | crop_harvest_action_flow / DERIVED_FEATURE | crop_harvest_action_flow / DERIVED_FEATURE | CLARIFIED | request / execution split required | partial | N/A |
| CRP-24 | field_cleanliness_state / DERIVED_FEATURE | field_cleanliness_state / DERIVED_FEATURE | CLARIFIED | scope is board and use-case specific | partial | N/A |
| CRP-25 | weed_backlog_cost / DERIVED_FEATURE | weed_backlog_cost / DERIVED_FEATURE | CLARIFIED | cost model kept out of freeze | partial | N/A |
| WRK-01 | unit_positions / RAW_OBSERVABLE | unit_positions / RAW_OBSERVABLE | UNCHANGED | retained | compatible | N/A |
| WRK-02 | workforce_headcount / DERIVED_FEATURE | workforce_headcount / DERIVED_FEATURE | UNCHANGED | retained | compatible | N/A |
| WRK-03 | worker_capacity_available / DERIVED_FEATURE | worker_capacity_available / DERIVED_FEATURE | CLARIFIED | capacity semantics separated from serviceability | partial | N/A |
| WRK-04 | movement_overhead / DERIVED_FEATURE | movement_overhead / DERIVED_FEATURE | CLARIFIED | routing and contention kept out of canonical formula | partial | N/A |
| WRK-05 | action_dispatch_failure / DERIVED_FEATURE | action_dispatch_failure / DERIVED_FEATURE | CLARIFIED | request-execution split clarified | partial | N/A |
| WRK-06 | productive_action_share / DERIVED_FEATURE | productive_action_share / DERIVED_FEATURE | CLARIFIED | denominator retained as open contract | partial | N/A |
| LIV-01 | livestock_headcount / DERIVED_FEATURE | livestock_headcount / DERIVED_FEATURE | UNCHANGED | retained | compatible | N/A |
| LIV-02 | animal_service_state / DERIVED_FEATURE | animal_service_state / DERIVED_FEATURE | CLARIFIED | FEED + CARE conjunction explicit | compatible | N/A |
| LIV-03 | feed_availability / DERIVED_FEATURE | feed_availability / DERIVED_FEATURE | CLARIFIED | provenance preserved | partial | N/A |
| LIV-04 | pasture_surface_maintained / DERIVED_FEATURE | pasture_surface_maintained / DERIVED_FEATURE | CLARIFIED | maintenance semantics separated from active surface | partial | N/A |
| LIV-05 | livestock_product_flow / DERIVED_FEATURE | livestock_product_flow / DERIVED_FEATURE | CLARIFIED | timing and provenance clarified | partial | N/A |
| INV-01 | seed_inventory / RAW_OBSERVABLE | seed_inventory / ENGINE_STATE | RECLASSIFIED | resource inventory is engine-owned state | compatible | N/A |
| INV-02 | shed_inventory / RAW_OBSERVABLE | shed_inventory / ENGINE_STATE | RECLASSIFIED | state ownership corrected | compatible | N/A |
| INV-03 | worker_inventory / RAW_OBSERVABLE | worker_inventory / ENGINE_STATE | RECLASSIFIED | transient carried items are engine state | compatible | N/A |
| INV-04 | inventory_to_cash_conversion / DERIVED_FEATURE | inventory_to_cash_conversion / DERIVED_FEATURE | CLARIFIED | conversion semantics remain partial | partial | N/A |
| MKT-01 | market_state_current / RAW_OBSERVABLE | market_state_current / RAW_OBSERVABLE | UNCHANGED | retained | compatible | N/A |
| MKT-02 | market_transaction_value / TELEMETRY_ONLY | market_transaction_value / TELEMETRY_ONLY | UNCHANGED | retained as non-decision input | compatible | N/A |
| MKT-03 | operating_cash_buffer / POLICY_CONTEXT | operating_cash_buffer / POLICY_CONTEXT | CLARIFIED | cash buffer is policy context + derived obligations | partial | N/A |
| MKT-04 | market_order_batch_limit / RAW_OBSERVABLE | market_order_batch_limit / RAW_OBSERVABLE | UNCHANGED | retained | compatible | N/A |
| GLB-01 | opponent_public_farm_state / RAW_OBSERVABLE | opponent_public_farm_state / RAW_OBSERVABLE | UNCHANGED | retained | compatible | N/A |
| GLB-02 | action_execution_result / TELEMETRY_ONLY | action_execution_result / TELEMETRY_ONLY | UNCHANGED | retained as post-action event | compatible | N/A |
| GLB-03 | transition_reason / TELEMETRY_ONLY | transition_reason / TELEMETRY_ONLY | UNCHANGED | retained as post-transition telemetry | compatible | N/A |
| LBL-01 | final_money_outcome / OUTCOME_LABEL | final_money_outcome / OUTCOME_LABEL | UNCHANGED | retained as terminal outcome | compatible | N/A |
| REJ-01 | time_to_random_weed deterministic / DERIVED_FEATURE | time_to_random_weed deterministic / REJECTED | DEPRECATED | deterministic future RNG is not valid online feature | incompatible | reject |

## 3. P0-02 corrected lifecycle classifier

The lifecycle classifier is replaced with a total, implementable predicate set for valid engine inputs. The valid lifecycle domain is:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

The classifier signature is:

```text
classify_tile(tile, *, in_working_set, phase, day, hour, engine_step, crop_rules):
    if invalid_container_or_missing_required_context:
        return diagnostic_error_outside_lifecycle
    if not in_working_set:
        return OUT_OF_SCOPE
    if tile == "LOCKED":
        return OUT_OF_SCOPE
    if tile is None:
        return EMPTY_ASSIGNED
    if tile.kind == "WEED":
        return LOST_WEED
    if tile.kind == "PLANT":
        ready = (
            tile.yield_units > 0
            and day - tile.planted_day >= crop_rules[tile.crop].first_yield_day
        )
        retired = (
            crop_rules[tile.crop].ongoing == True
            and tile.yield_units == 0
            and no_future_scheduled_production(tile, crop_rules, phase, day, hour)
        )
        if ready:
            return HARVEST_READY
        if retired:
            return RETIREMENT_DUE
        return GROWING
    return OUT_OF_SCOPE
```

Important semantics:

- `max_lifespan_step` alone does not define `RETIREMENT_DUE`.
- `RETIREMENT_DUE` means the ongoing crop is exhausted after the final valid harvest and has no remaining scheduled production.
- an ongoing crop with positive current yield remains `HARVEST_READY`.
- invalid or missing input is not a lifecycle state.

### 3.1 Boundary test vectors

| case | inputs | expected_state | reason |
|---|---|---|---|
| LOCKED | tile.kind = LOCKED, in_working_set = true | OUT_OF_SCOPE | engine state marks a non-crop tile |
| outside working set | tile.kind = PLANT, in_working_set = false | OUT_OF_SCOPE | not in active working set |
| None inside working set | tile = None, in_working_set = true | EMPTY_ASSIGNED | assigned empty tile |
| WEED | tile.kind = WEED | LOST_WEED | canonical loss state |
| PLANT immature with yield > 0 | PLANT, yield > 0, age < first_yield_day | GROWING | not mature enough |
| PLANT mature with yield > 0 | PLANT, yield > 0, age >= first_yield_day | HARVEST_READY | valid harvest maturity |
| ongoing immediately after intermediate valid harvest | PLANT, yield == 0, valid maturity, future production exists | GROWING | yield has been transferred and the tile remains ongoing |
| ongoing before future scheduled production | PLANT, yield == 0, upcoming output exists | GROWING | not exhausted yet |
| ongoing at final production before valid harvest | PLANT, yield > 0, final production scheduled but not yet harvested | HARVEST_READY | final valid harvest still harvest-ready |
| ongoing immediately after final valid harvest | PLANT, yield == 0, no production left | RETIREMENT_DUE | exhausted ongoing after final valid harvest |
| non-ongoing before maturity | non-ongoing PLANT, age < first_yield_day | GROWING | not retirement-eligible |
| invalid or missing input | tile missing or crop rule absent | diagnostic_error_outside_lifecycle | not a lifecycle state |

## 4. P1-01 aggregate contracts

The C2 catalog does not keep speculative aggregate formulas. Each aggregate still present in the common catalog must have a real contract. The following aggregate records are materialized and explicitly separated by schema completeness and formula completeness.

| feature_id | scope | sampling_phase | window | numerator | denominator | zero_denominator_convention | dedup_key | source_class | formula_version | boundary_examples | online_available | decision_time_available | future_leakage | CONTRACT_SCHEMA_COMPLETE | FEATURE_FORMULA_COMPLETE | freeze_ready |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRP-18 | active working set, ownership scope | current board snapshot | current step | count(tile.kind == PLANT) | active board tiles in scope | 0 means no active crop tiles | board_scope+player_id | RAW_OBSERVABLE + DERIVED | v1 | all PLANT in scope | YES | YES | NO | NO | YES | NO |
| CRP-19 | maintained productive crop tiles only | pre-refresh or decision phase | current day/window | count(tile in maintained set) | tiles in crop scope | 0 means no maintained crop tiles | board_scope+player_id+day | DERIVED_FEATURE | v1 | GROWING vs RETIREMENT_DUE vs HARVEST_READY | YES | YES | NO | NO | NO | NO |
| CRP-20 | crop watering demand and execution | current day/window | player-day | executed watering actions | crop watering needs in scope | 0 if no need in scope | player_day | DERIVED_FEATURE | v1 | missed-water and watered-day examples | YES | YES | NO | NO | NO | NO |
| CRP-21 | sequence of watering service days | current window | player-window | days with successful watering service | days in scope | 0 if no service window exists | player_window | DERIVED_FEATURE | v1 | daily service and gaps | YES | YES | NO | NO | NO | NO |
| CRP-22 | care needs for valid crop tiles | current day/window | player-day | completed care actions | declared care needs | 0 if no care demand | player_day | DERIVED_FEATURE | v1 | water care and crop care examples | YES | YES | NO | NO | NO | NO |
| CRP-23 | harvest demand and execution | action + follow-through | player-window | valid harvest requests and executed harvests | harvest-ready eligible tiles or requests | 0 if no eligible harvest | player_window | DERIVED_FEATURE | v1 | valid harvest vs no-op vs failed harvest | YES | YES | NO | NO | NO | NO |
| CRP-24 | weed and clean tiles | current board snapshot | current step | count or map of weed-impacted tiles | all in-scope tiles | 0 if no weed tiles | board_scope | DERIVED_FEATURE | v1 | weed map and clean distribution | YES | YES | NO | NO | NO | NO |
| CRP-25 | weed pressure and recovery burden | current window | player-window | recovery burden proxy or backlog count | tiles or capacity in scope | 0 if no backlog | player_window | DERIVED_FEATURE | v1 | nonzero backlog examples | YES | YES | NO | NO | NO | NO |
| WRK-03 | active worker capacity | current window | player-step/window | available effective action slots | active workers or time slots in scope | 0 if no capacity | player_window | DERIVED_FEATURE | v1 | worker availability and over-capacity | YES | YES | NO | NO | NO | NO |
| WRK-04 | routing and movement burden | current window | player-window | movement cost or count | units or tasks in scope | 0 if no movement | player_window | DERIVED_FEATURE | v1 | short vs long moves | YES | YES | NO | NO | NO | NO |
| WRK-05 | dispatch results | post-action | action/window | failed or rejected actions | requested or eligible actions | 0 if no failed actions | action_id | DERIVED_FEATURE | v1 | no-op, reject, mismatch | YES | NO | NO | NO | NO | NO |
| WRK-06 | useful actions out of total actions | current window | player-window | useful actions | total actions in scope | 0 if no actions in scope | player_window | DERIVED_FEATURE | v1 | harvest and care vs idle | YES | YES | NO | NO | NO | NO |
| MKT-03 | current cash relative to obligations | decision phase | player-step/window | cash minus declared obligations | current cash or obligation envelope | 0 if no active obligation | player_step | POLICY_CONTEXT | v1 | buffer positive and negative | YES | YES | NO | NO | NO | NO |

The rule remains explicit:

```text
FEATURE_FORMULA_COMPLETE = NO
=> freeze_ready = NO
```

No missing formula is invented.

## 5. P2-01 active_crop_surface base formula

The base formula is preserved and materialized:

```text
active_crop_surface = count(tile.kind == PLANT)
```

This is a formula-complete and valid aggregate base under the common C2 catalog. The full contract still needs explicit board scope, ownership scope, and sampling-phase details, but the base count itself is valid.

```text
FEATURE_FORMULA_COMPLETE = YES
CONTRACT_SCHEMA_COMPLETE = NO
freeze_ready = NO
```

## 6. P1-02 materialize clock and phase records

The C2 catalog records the time-dependent objects explicitly. The authoritative clock rule is:

```text
engine deadline based on step
=> use engine_step
```

and `canonical_step` remains diagnostic.

| feature_id | authoritative_clock | source | formula | sampling_phase | pre/post-action availability | future_leakage |
|---|---|---|---|---|---|---|
| TMP-01 | engine_step | observation.step | identity | current step | pre-action | NO |
| TMP-04 | canonical_step | day,hour,turnsPerDay | day*turnsPerDay+hour | diagnostic | post-sample diagnostic | NO |
| CRP-13 | engine_step | max_lifespan_step, tile state | step >= max_lifespan_step under active ongoing | pre-action and decay phase | pre-action | NO |
| CRP-14 | engine_step | max_lifespan_step, decay cadence | next decay boundary | pre-action / decay phase | pre-action | NO |
| CRP-15 | engine_step | max_lifespan_step, yield_units | next decay step leading to yield loss | pre-action | pre-action | NO |
| CRP-11 | day|hour | tile.kind, watered_today | PLANT and not watered today | pre-action and pre-refresh | NO |
| CRP-12 | day | care_due, consecutive_unwatered | care_due and counter+1 >= 2 | EOD refresh | pre-refresh | NO |
| TMP-05 | hour|turnsPerDay | hour, turnsPerDay | pre-EOD action window | pre-action | NO |
| fertilizer_effect_window | day | crop rules + fertilization state | day..day+2 window | current state and EOD refresh | pre-action and post-refresh | NO |
| livestock production timing | day | animal feed / care regime | production day gating after feed and care conjunction | EOD to next production day | pre-action | NO |

## 7. P1-03 FEED + CARE correction

The required correction is explicit: the bonus accumulation at EOD is triggered only when both care and feed are present in the same cycle.

```text
cared_today == true
AND
fed_today == true
```

This must be interpreted as:

- CARE action or flag = current-day care state
- FEED action or flag = current-day feed state
- pending_care_bonus accumulation at EOD = only if both are true
- bonus consumption on eligible production day = derived from the stored pending bonus and the actual production-day trigger

The previous simplification:

```text
CARE -> pending_care_bonus
```

is insufficient and therefore not used in the common Feature Model C2. The note for this task is:

```text
UPSTREAM LOCAL CORRECTION REQUIRED
```

This is a local upstream correction and is not rewritten here.

## 8. P1-04 class enumeration and cleanup

The real C2 catalog does not inflate policy context, telemetry-only, or outcome classes. The model keeps only the feature objects with explicit semantics and granularities. Pure event and provenance fields are moved to the downstream event schema and are not counted as feature objects.

### 8.1 Membership by class

```text
DUPLICATE_CLASS_MEMBERSHIP: 0
ENGINE_STATE = {TMP-01, TMP-02, TMP-03, FRM-01, CRP-01, CRP-02, CRP-03, CRP-05, CRP-06, CRP-07, CRP-08, INV-01, INV-02, INV-03}
RAW_OBSERVABLE = {FRM-02, MKT-01, GLB-01, WRK-01, MKT-04}
DERIVED_FEATURE = {TMP-04, TMP-05, FRM-04, FRM-05, CRP-04, CRP-09, CRP-10, CRP-11, CRP-12, CRP-13, CRP-14, CRP-15, CRP-16, CRP-17, CRP-18, CRP-19, CRP-20, CRP-21, CRP-22, CRP-23, CRP-24, CRP-25, WRK-02, WRK-03, WRK-04, WRK-05, WRK-06, LIV-01, LIV-02, LIV-03, LIV-04, LIV-05, INV-04}
POLICY_CONTEXT = {FRM-03, MKT-03}
TELEMETRY_ONLY = {MKT-02, GLB-02, GLB-03}
OUTCOME_LABEL = {LBL-01}
```

This is the actual class structure of the corrected admissible catalog. `REJ-01` is kept only in the rejected ledger and is excluded from both the feature total and class membership. Event and provenance fields such as requested_quantity, executed_quantity, realized_price, cash_delta, transition_reason, and generic estimate are not counted as feature objects.

## 9. P2-02 eligibility versus serviceability

The distinction is formalized as follows.

### 9.1 action_eligible_now

```text
action_eligible_now =
    actor is in the required spatial relation or stand-by condition,
    action preconditions are satisfied,
    required current resources and inventory are available,
    current action phase and engine timing permit the action.
```

This concerns execution in the current tick and does not include path-planning or future scheduling.

### 9.2 serviceable_before_deadline

```text
serviceable_before_deadline =
    estimate of whether an actor can reach the tile and complete the action before the deadline,
    given current routing, scheduling, inventory, contention, timing, and policy memory.
```

This remains:

```text
PARTIALLY_KNOWN
FEATURE_FORMULA_COMPLETE = NO
freeze_ready = NO
```

It is not a guarantee and is not re-labeled as a deterministic feature.

## 10. HARVEST and crop-risk preservation

The core C2 preservation is retained:

```text
harvest_ready =
    tile.kind == "PLANT"
    AND tile.yield_units > 0
    AND day - tile.planted_day >= first_yield_day
```

The causal separation is also preserved:

```text
missed-WATER deterministic
lifespan deterministic
EMPTY random-WEED eligibility / hazard
```

and the rejected deterministic concept remains:

```text
time_to_random_weed
```

The random WEED draw is not treated as a known countdown.

## 11. Inventory provenance and market provenance cleanup

### 11.1 Inventory provenance

The common model separates:

```text
pre-EOD overflow risk / amount-if-unchanged
```

from:

```text
realized shed_overflow_eod_loss
```

The first may be a decision-time derived estimate if the formula and sources are explicitly declared. The second is a post-refresh event outcome and is not treated as a pre-action feature.

The worker return obligation is not reintroduced as a generic rule.

### 11.2 Market provenance

The common model may retain:

```text
displayed_quote
```

if it is a real pre-request observable. The following are not counted as common feature objects unless a dedicated, formalized metric is created with its own ID, formula, and granularity:

```text
requested_quantity
executed_quantity
realized_price
cash_delta
```

This keeps market semantics aligned with the fact that realized values are post-action and not pre-action decision input.

## 12. Consumer neutrality

The feature model remains consumer-neutral. The following remain forbidden as intrinsic feature properties:

```text
current_MODEL_SPEC_usage
USED
FULL
NOT_USED
```

The model defines the common upstream contract. Consumer-specific matrices and runtime traces remain separate downstream artifacts.

```text
FEATURE MODEL = consumer-neutral
CONSUMER MATRIX = consumer-specific
RUNTIME TRACE = consumer-specific
```

The absence of a runtime mapping in the feature model is not a blocker for the feature model itself; it is a downstream requirement before full foundation freeze.

## 13. Vertical consistency map

| feature_id | Ontology C2 basis | State Machine C2 basis | Feature Model C2 representation | status | issue |
|---|---|---|---|---|---|
| CRP-09 | lifecycle semantics | lifecycle transitions | total classifier | OK | none |
| CRP-10 | maturity and harvest readiness | harvest gate | predicate with crop rule | OK | none |
| CRP-17 | risk structure | decay and weed hazard | structured multi-cause risk window | OK | none |
| MKT-02 | transaction semantics | execution and settlement | telemetry-only metric | OK | not a decision input |
| MKT-03 | cash and obligation concept | economic scheduling | policy-context plus derived buffer | PARTIAL | obligations not canonical |
| CRP-19 | maintained surface semantics | tile lifecycle + maintenance | aggregate with incomplete formula | PARTIAL | formula incomplete |
| REJ-01 | no valid random future event | rejected by engine semantics | rejected feature | OK | kept out of freeze |

`NONE_DIRECT` remains valid when a concept is semantically relevant but not a dedicated feature object.

## 14. Upstream local corrections required

The C2 remediation keeps the common feature model correct, but it logs the required downstream local corrections that are outside this task:

```text
UPSTREAM LOCAL CORRECTION REQUIRED
- state-machine wording for FEED + CARE accumulation must require both cared_today and fed_today at EOD
- any downstream consumer contract using a simplified CARE -> pending_care_bonus transition must be rewritten
- any aggregate formula without an explicit numerator, denominator, and phase must be marked NON-FROZEN and not consumed as policy input
```

This is a tracking note only. The remediation does not rewrite the state machine or any model spec.

## 15. Verification

The remediation was validated with the required repository checks.

```text
git diff --check: PASS
pytest: PASS (143 tests collected, exit code 0)
ruff: present in this environment; it reported pre-existing import-order issues in unrelated legacy files and did not create a regression in the feature-model document itself.
```

## 16. Final status

```text
FEATURE MODEL C2 REMEDIATION: COMPLETED
P0-01: RESOLVED
P0-02: RESOLVED
P1 FINDINGS: RESOLVED
FEATURE MODEL C2 STATUS: CANDIDATE / NOT FROZEN
CODEX BLOCKER VERIFICATION REQUIRED: YES
MODEL_SPEC C2: NOT STARTED
FOUNDATION C2: NOT FROZEN
```

The feature model remains candidate and not frozen because the complete downstream consumer matrix and the model-spec-level contract remain out of scope for this task.
