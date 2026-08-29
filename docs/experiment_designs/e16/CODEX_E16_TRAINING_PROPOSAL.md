# CODEX Independent E16 Training Design Proposal

- **MODELER_ID:** `CODEX`
- **Status:** `INDEPENDENT PROPOSAL - NOT FROZEN`
- **Evidence role:** `TRAINING / INITIAL BOUNDING + INTERACTION DISCRIMINATION`
- **Canonical input:** `docs/model_specs/post_e15/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md`
- **Independence:** no E16 proposal from another modeler was read.

E16 is training evidence. Its results may revise features, relationships, and initial bounds, but may not later be presented as independent validation or test evidence. Numerical settings below are experimental probes and controls, never optima.

## A. DESIGN SUMMARY

```text
design_id: E16-CODEX-S12-STAGED-PREFERRED
training_goal: discriminate irrigation-service x crop-working-set and livestock x pasture x crop-opportunity interactions while separating assigned policy, realized behavior, and executed effects.
design_type: blocked staged response-surface subset; 7-cell Stage A followed conditionally by 5-cell Stage B.
total_cells: 12 planned maximum (7 Stage A + 5 Stage B); 7 if the preregistered Stage B gate is not met.
seeds_per_cell: 3 shared training seeds, with 2 seat-swapped episodes per seed.
total_episodes: 72 planned maximum (42 Stage A + 30 Stage B); 42 if Stage B is blocked.
staged: YES
```

### Evidence reconstruction

Primary E15 evidence contains only three pairwise episodes, one seed per pairing. The observed low-outcome bundle has `quadrants_owned = 3`, 8-9 maximum active crops, 18 pasture, 18 animals, 12 hands, and a replay-derived mean EOD watered-crop fraction of 0.082-0.144. The four other policy-match observations have `quadrants_owned = 2`, 25-37 maximum active crops, 5-9 pasture, 4-7 animals, 9-10 hands, and a replay-derived fraction of 0.711-0.752. The region between those bundles is sparse and fully confounded. M2 additionally shows that 37 crops and more WATER requests do not monotonically dominate 28 crops.

These are PRIMARY E15 observations or explicitly labelled replay-derived proxies. They initialize the E16 search region; they do not define optima or validated thresholds. Requested actions and market orders in E15 are not treated as executed effects or transactions.

### Controlled baseline and treatment onset

All cells must use one common E16 treatment implementation and configuration schema. The implementation hash must be identical across cells; a machine-checked allowlist may differ only in the manipulated fields declared below. No current submission is modified by this proposal.

The common opening is identical and treatment-inert across cells until `T0`, defined as the first state after verified execution of the acquisition that yields `quadrants_owned = 2`. Before `T0`, the common opening caps the crop working set at 10 with the fixed allocator, emits no pasture or animal acquisition, and uses the same pre-treatment workforce schedule. This ensures that the low crop cell never requires destructive shrinking and that every livestock cell begins from the same zero-herd/zero-pasture state. From `T0` onward:

- `quadrants_owned` is capped at `2`; no third-quadrant order is permitted;
- treatment parameters become active;
- the same deterministic tile ordering, crop allocator, routing module, hire/renewal module, cash rule, feed rule, and endgame module are used in every cell;
- if the common opening never reaches `T0`, the episode is retained as an opening/policy-realization failure and is not replaced by another seed.

Because the opening is identical within each seed/opponent/seat block, treatment effects begin from the same realized state if implementation fidelity holds. `quadrants_owned = 2` is a controlled operating baseline, not an optimum or frozen land threshold.

## B. HYPOTHESES

```text
hypothesis_id: H-A1_SERVICE_FLOOR
concepts: watering_dispatch_priority, watering_execution_rate, watering_continuity, crop_surface_maintained
relationship: raising assigned watering priority should increase executed service and maintained surface until service capacity saturates; final_money need not be monotonic above the operational floor.
current_evidence: E15 separates a replay proxy of 0.082-0.144 from 0.711-0.752, but observes almost nothing between them and does not isolate watering from crop scale or dispatch.
uncertainty_to_resolve: whether a transition exists inside the candidate 0.20-0.70 policy-intent range and whether it changes with crop working-set size.
falsification_condition: at fixed crop target, priority assignment changes realized service but does not improve maintained surface, action completion, or final_money consistently; if assignment does not change realized service, POLICY_REALIZATION or IMPLEMENTATION_FIDELITY is falsified instead of the feature relation.
```

```text
hypothesis_id: H-A2_SERVICE_X_SURFACE
concepts: watering_dispatch_priority, watering_execution_rate, crop_surface_maintained, worker_capacity_available, action_dispatch_failure
relationship: the marginal value of a larger crop working set is conditional on sufficient service; a large set under low service should create more unmet needs and failures than the same set under high service.
current_evidence: 8-9 crops/low service and 25-37 crops/high service occur as bundles; M2 rejects a simple more-crops-is-better relation above the observed floor.
uncertainty_to_resolve: whether service and crop target have a non-zero interaction, and where failure, transition, and competitive working regions begin within the E15 gap.
falsification_condition: the paired difference-in-differences is near zero across seeds for maintained surface, action failures, and final_money, or a larger crop set performs equivalently under LOW and HIGH service while the assigned priorities are faithfully realized.
```

```text
hypothesis_id: H-B1_HERD_SCALE
concepts: livestock_headcount, livestock_product_flow, livestock service burden, crop_surface_maintained, operating_cash_buffer
relationship: herd scale is non_monotonic and conditional; beyond supported capacity, acquisition, feed, and service burden should displace crop care or cash conversion.
current_evidence: 4-7 animals occur in the E15 competitive bundle and 17-18 in the replicated failure bundle, with 8-16 sparsely observed and all components confounded.
uncertainty_to_resolve: whether the 4 -> 10 -> 17 sequence at fixed pasture 18 exposes a transition attributable to herd burden rather than pasture footprint.
falsification_condition: at fixed pasture 18, increasing herd from 4 to 10 to 17 produces no consistent deterioration in crop service, cash shortfall, action failure, product net flow, or final_money, or produces a consistent improvement after executed costs are included.
```

```text
hypothesis_id: H-B2_PASTURE_OPPORTUNITY_COST
concepts: pasture_surface_maintained, pasture_arable_surface_tradeoff, livestock_headcount, crop_surface_maintained
relationship: pasture beyond the minimum support allocation imposes an arable opportunity cost whose magnitude depends on herd scale.
current_evidence: E15 observes pasture maxima 5, 9, and 18 only inside different policy bundles; it cannot separate pasture from animal count.
uncertainty_to_resolve: whether changing from minimum-support pasture to 18 pasture at fixed herd 4 and herd 10 reduces maintained crop output or net cash, and whether that effect interacts with herd.
falsification_condition: excess pasture has no consistent effect at either fixed herd level, or its lost crop surface is fully offset by executed livestock value without additional cash or dispatch failure.
```

## C. FACTORS AND CONTROLS

The operational `watering_dispatch_priority` levels are policy-intent parameters. At each day, WATER is top-ranked until the policy has observed successful service for the declared fraction of unique daily watering needs; the common queue then resumes. Failed/no-op WATER does not count toward the quota. The realized execution rate remains a derived metric and is not assumed equal to the assignment.

Crop composition is controlled by a deterministic largest-remainder allocator with target shares 40% Wheat, 40% Strawberry, and 20% Melon. Thus targets 10, 17, and 25 map respectively to `4/4/2`, `7/7/3`, and `10/10/5`. The mix is a control, not a crop-margin conclusion.

| variable | role | type | candidate_values_or_control | rationale |
|---|---|---|---|---|
| `watering_dispatch_priority` | MANIPULATED | PARAMETER | `LOW=0.20`, `MID=0.45`, `HIGH=0.70` daily successful-service intent | Samples low, middle, and high intent inside the broad E15 gap without treating any value as a threshold. |
| `crop_working_set_target` | MANIPULATED | PARAMETER | Stage A: `10`, `17`, `25`; Stage B: preregistered `C*` selected from Stage A diagnostics | Samples just above the E15 failure proxy, an unobserved middle, and the lower competitive observation. |
| `livestock_headcount_target` | MANIPULATED | PARAMETER | Stage A control `4`; Stage B `4`, `10`, `17` | Low observed region, unobserved middle, and failure-scale anchor; none is an optimum. |
| `pasture_allocation_target` | MANIPULATED | PARAMETER | Stage A control `5`; Stage B `5`, `11`, `18` according to cell | Separates minimum support from excess footprint with feasible animal/pasture combinations. |
| `quadrants_owned` | CONTROL | PARAMETER | common opening to `2`, then hard cap `2` | Canonical E16 controlled baseline; land effect is not inferred. |
| `workforce_headcount` | CONTROL | PARAMETER | concurrent hands target `10` from `T0` through the common shutdown window | Holds raw workforce constant so service burden is expressed through useful capacity and failures. Ten is a control, not an optimum. |
| hire/renewal schedule | CONTROL | HYPERPARAMETER | one identical schedule and contract-renewal rule, frozen before runs | Prevents workforce timing from becoming a hidden treatment. |
| livestock species | CONTROL | PARAMETER | Cow only in all treatment cells | Removes unresolved species-margin variation; E16 cannot infer Cow superiority. |
| crop mix and tile order | CONTROL | HYPERPARAMETER | fixed 40/40/20 allocator and deterministic non-pasture tile order | Prevents detailed crop mix and topology from expanding the DOE. |
| feed coverage rule | CONTROL | HYPERPARAMETER | target 3 expected feed-days; same production/purchase rule in every cell | Holds sourcing logic constant in demand-relative terms; 3 days is an experimental control, not a trained bound. |
| operating cash rule | CONTROL | HYPERPARAMETER | projected cash after discretionary orders must remain at least 300 | Common confounder control, not a recommendation or cash optimum. |
| routing module | CONTROL | HYPERPARAMETER | one frozen actor-to-task and movement policy | Routing is observed diagnostically but receives no dedicated cells. |
| land acquisition timing | CONTROL | HYPERPARAMETER | identical common opening; treatments activate only at verified `T0` | Makes land timing pre-treatment and paired across cells. |
| endgame module | CONTROL | HYPERPARAMETER | one frozen shutdown/liquidation policy | Prevents horizon behavior from confounding treatment comparisons. |
| opponent | CONTROL | HYPERPARAMETER | frozen Copilot E15 submission, SHA256 `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb` | A single competitive opponent removes opponent variation within E16; conclusions remain opponent-conditional. |
| `watering_execution_rate` | DERIVED_METRIC | DERIVED_METRIC | successful unique crop-day WATER effects / unique crop-day watering needs | Measures policy realization; not directly manipulated. |
| `watering_continuity` | DERIVED_METRIC | DERIVED_METRIC | productive days with service rate >=0.50 / productive days | Temporal diagnostic; 0.50 is a reporting cut, not an optimum. |
| daily serviced/maintained crop surface | DERIVED_METRIC | DERIVED_METRIC | active, required, serviced, surviving, harvest-ready, and lost tile counts reported separately | Avoids equating planted or active surface with maintained output. |
| pasture occupancy and feed coverage | DERIVED_METRIC | DERIVED_METRIC | animals/pasture and accessible feed/expected demand, with sources separated | Measures realization and livestock capacity without a composite score. |
| `action_dispatch_failure` | OBSERVABILITY | OBSERVABILITY_REQUIREMENT | exact requested/executed/no-op/reason records | Required to distinguish insufficient model capacity from invalid execution. |
| market/cash/product flow | OBSERVABILITY | OBSERVABILITY_REQUIREMENT | executed quantities, prices, values, categorized cash flow, inventory provenance | Prevents requests from being interpreted as economic execution. |
| `state_capacity_alignment` components | OBSERVABILITY | NOT_YET_TUNABLE | record components only; no weights or composite formula | E16 may inform later formalization but cannot freeze a target-derived metric. |
| `productive_action_share` | DERIVED_METRIC | DERIVED_METRIC | record execution-aware/value-aware variants; no cells allocated | Consolidated priority is LOW and the raw aggregate is composition-sensitive. |
| `final_money` | DERIVED_METRIC | DERIVED_METRIC / PRIMARY_TARGET | terminal environment money | Primary target, never a causal feature or component of another metric. |

The common cash, feed, workforce, routing, species, and endgame settings are controls selected for identifiability. E16 cannot claim they are optimal or validated. If the treatment implementation cannot keep them identical, the exact divergence is logged as a predicted confounder and analyzed under POLICY_REALIZATION.

## D. EXPERIMENT CELLS

### Stage A - irrigation x crop working set

```text
cell_id: A01_LOW_WATER_LOW_CROP
factor_values: watering_dispatch_priority=LOW(0.20); crop_working_set_target=10; livestock_headcount_target=4; pasture_allocation_target=5
comparison_role: low-low corner and candidate failure anchor.
epistemic_question: can a small crop set remain maintained under low assigned service, or does the irrigation floor dominate even at low workload?
why_required: removing it eliminates the low-crop baseline needed for the watering main effect and the interaction contrast.
```

```text
cell_id: A02_HIGH_WATER_LOW_CROP
factor_values: watering_dispatch_priority=HIGH(0.70); crop_working_set_target=10; livestock_headcount_target=4; pasture_allocation_target=5
comparison_role: high-low corner; compare with A01 and with larger crop targets under HIGH.
epistemic_question: what is the watering effect at low crop load, and is crop target 10 capacity-feasible under high service?
why_required: removing it prevents separation of watering from crop-load effects at the low surface corner.
```

```text
cell_id: A03_LOW_WATER_HIGH_CROP
factor_values: watering_dispatch_priority=LOW(0.20); crop_working_set_target=25; livestock_headcount_target=4; pasture_allocation_target=5
comparison_role: low-high stress corner.
epistemic_question: does a competitive-observed crop scale collapse when service intent is low?
why_required: removing it eliminates the cell most capable of falsifying the service x surface interaction.
```

```text
cell_id: A04_HIGH_WATER_HIGH_CROP
factor_values: watering_dispatch_priority=HIGH(0.70); crop_working_set_target=25; livestock_headcount_target=4; pasture_allocation_target=5
comparison_role: high-high corner and upper crop candidate for Stage B anchoring.
epistemic_question: can the larger crop working set be serviced and maintained under high priority without excessive dispatch or cash cost?
why_required: removing it eliminates the competitive corner and the complete 2x2 interaction estimate.
```

```text
cell_id: A05_MID_WATER_MID_CROP
factor_values: watering_dispatch_priority=MID(0.45); crop_working_set_target=17; livestock_headcount_target=4; pasture_allocation_target=5
comparison_role: joint center point.
epistemic_question: is the unobserved middle a transition regime, and is there curvature not explained by the four corners?
why_required: removing it forces a linear corner-only interpretation and leaves the joint middle entirely unsampled.
```

```text
cell_id: A06_MID_WATER_HIGH_CROP
factor_values: watering_dispatch_priority=MID(0.45); crop_working_set_target=25; livestock_headcount_target=4; pasture_allocation_target=5
comparison_role: watering-axis bridge at high crop load.
epistemic_question: where does service transition between LOW and HIGH when crop demand is high?
why_required: removing it leaves only two service levels at the workload where the irrigation boundary matters most.
```

```text
cell_id: A07_HIGH_WATER_MID_CROP
factor_values: watering_dispatch_priority=HIGH(0.70); crop_working_set_target=17; livestock_headcount_target=4; pasture_allocation_target=5
comparison_role: crop-axis bridge at high service and middle candidate for Stage B anchoring.
epistemic_question: where does useful crop scale transition between 10 and 25 when service intent is high?
why_required: removing it prevents initial crop bounding under a capacity-feasible service regime.
```

### Stage B - livestock x pasture x crop opportunity cost

`C*` is determined only by the preregistered Stage A advancement rule in Section E. All Stage B cells use `watering_dispatch_priority=HIGH(0.70)`, `crop_working_set_target=C*`, Cow-only species, and the same demand-relative feed rule.

```text
cell_id: B01_HERD4_PASTURE5
factor_values: livestock_headcount_target=4; pasture_allocation_target=5; watering_dispatch_priority=HIGH(0.70); crop_working_set_target=C*
comparison_role: compact livestock baseline and minimum-support pasture at low herd.
epistemic_question: what crop, service, and economic state is achieved by the low compact bundle under the Stage A operational anchor?
why_required: removing it eliminates the baseline for the low-herd pasture contrast and the minimum-support bundle response.
```

```text
cell_id: B02_HERD4_PASTURE18
factor_values: livestock_headcount_target=4; pasture_allocation_target=18; watering_dispatch_priority=HIGH(0.70); crop_working_set_target=C*
comparison_role: pasture-only excess sentinel at fixed low herd.
epistemic_question: what is the arable and routing cost of 13 additional pasture without additional livestock?
why_required: removing it makes pasture footprint inseparable from herd scale and removes the cleanest opportunity-cost contrast.
```

```text
cell_id: B03_HERD10_PASTURE11
factor_values: livestock_headcount_target=10; pasture_allocation_target=11; watering_dispatch_priority=HIGH(0.70); crop_working_set_target=C*
comparison_role: unobserved middle herd with minimum-support pasture.
epistemic_question: does a middle herd remain serviceable when pasture grows only enough to support it?
why_required: removing it leaves the 4-17 herd interval unbounded and prevents a pasture-effect contrast at middle herd.
```

```text
cell_id: B04_HERD10_PASTURE18
factor_values: livestock_headcount_target=10; pasture_allocation_target=18; watering_dispatch_priority=HIGH(0.70); crop_working_set_target=C*
comparison_role: middle herd with excess pasture; bridge between B02, B03, and B05.
epistemic_question: does excess pasture change the middle-herd result, and how does herd 10 compare with herd 4 at fixed pasture 18?
why_required: removing it destroys both the second fixed-herd pasture contrast and the lower segment of the fixed-pasture herd curve.
```

```text
cell_id: B05_HERD17_PASTURE18
factor_values: livestock_headcount_target=17; pasture_allocation_target=18; watering_dispatch_priority=HIGH(0.70); crop_working_set_target=C*
comparison_role: E15 failure-scale anchor at fixed pasture 18.
epistemic_question: does the high herd reproduce capacity/cash failure after irrigation, crop target, land, workforce, species, routing, and pasture are controlled?
why_required: removing it prevents direct probing of the observed failure-scale region and the 10-to-17 herd transition.
```

All five livestock/pasture combinations are structurally feasible: pasture count is never below animal target. Differences between target and achieved state remain evidence about policy realization, not grounds for silently relabelling a cell.

## E. STAGE / ADVANCEMENT RULES

### E0 - instrumentation gate

Before training episodes, run non-analytic smoke executions to verify that the ledger reconciles action application, cash, market transactions, and inventory conservation. Smoke outcomes are not retained as training evidence and do not count in the 72-episode budget. Any unreconciled transaction/value, missing failure reason, or configuration-hash mismatch blocks E16. The same smoke configuration is rerun after a telemetry fix; no model conclusion may be drawn from it.

### E1 - Stage A

Execute all seven Stage A cells over all preregistered seed/seat blocks. No cell is stopped early for poor `final_money`.

### E2 - deterministic selection of `C*`

Only HIGH-priority cells A02 (`10`), A07 (`17`), and A04 (`25`) are eligible. For each cell, compute over all planned episodes:

- completion rate;
- median post-ramp daily `watering_execution_rate`;
- median `watering_continuity`;
- median crop-target attainment, defined as daily active crop surface / assigned target over the steady window from the third full day after `T0` through the common endgame shutdown.

A cell is `CAPACITY_ELIGIBLE` if:

```text
completion_rate >= 0.80
median watering_execution_rate >= 0.60
median watering_continuity >= 0.75
median crop_target_attainment >= 0.80
```

These are advancement criteria, not learned feature thresholds or optima. They may not be reported as validated bounds.

Set `C*` to the largest crop target among `CAPACITY_ELIGIBLE` cells. `final_money` and opponent money are forbidden inputs to this rule. If no cell is eligible, do not execute Stage B; report `STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR`. Do not substitute a different watering level, seed, crop target, or post-hoc gate.

### E3 - Stage B

If and only if `C*` exists, execute all five Stage B cells over the same seed/seat blocks. No Stage B cell is selected, removed, or stopped based on interim outcome.

## F. SEED / OPPONENT PROTOCOL

### Training seeds

Use three new common seeds, distinct from E15. They are the unsigned big-endian first 32 bits of SHA256 over the stated ASCII labels:

| Label | First 32 SHA256 bits | Seed |
|---|---|---:|
| `E16-CODEX-TRAINING-SEED-1` | `6b6ad4fc` | 1802163452 |
| `E16-CODEX-TRAINING-SEED-2` | `64056ce6` | 1678077158 |
| `E16-CODEX-TRAINING-SEED-3` | `37bcf795` | 935131029 |

Every cell uses all three seeds. Seed selection is never changed after observing outcomes.

### Opponent and seats

The opponent is the immutable E15 frozen Copilot submission at `results/e15/freeze/submission_copilot_E15_FROZEN.py`, SHA256 `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb`.

For each cell and seed, execute two episodes:

1. treatment policy as player 0, opponent as player 1;
2. opponent as player 0, treatment policy as player 1.

The unit of blocking is `(seed, treatment_seat)`. Treatment contrasts are computed within the same block. The fixed opponent controls opponent variance rather than estimating it; therefore all E16 conclusions are conditional on this opponent and may not be generalized to other opponents.

### Run order

Stage A precedes Stage B. Within each stage and `(seed, seat)` block, sort cells ascending by the hexadecimal SHA256 of:

```text
E16-CODEX-S12-STAGED-PREFERRED|stage|seed|seat|cell_id
```

This produces a deterministic pseudo-randomized order without post-hoc rearrangement. Execution workers may run blocks in parallel, but each result retains start time, worker identity, engine version, and all hashes.

### Failures and reruns

- Gameplay completion failures and disqualifications remain outcomes and are never replaced.
- A proven infrastructure failure may be rerun only with the identical cell, seed, seat, opponent hash, treatment hash, engine hash, and configuration; both attempts remain in the audit trail and only the preregistered valid-attempt rule is analyzed.
- No replacement seed is permitted.

Paired blocking separates assigned-treatment contrasts from seed and seat variation. It does not estimate generalization; that requires later independent validation with unused seeds and opponents.

## G. TELEMETRY REQUIREMENTS

### Required event ledger

Each event record must contain at least:

```text
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
```

The ledger must distinguish `requested`, `accepted`, `partially_executed`, `executed`, `failed`, and `no_op`. Required failure reasons include at minimum invalid target, no need, no yield, insufficient cash, insufficient inventory, storage full, actor unavailable, contract expired, order-limit rejection, duplicate reservation, and unknown engine rejection.

### Required state series

- explicit `quadrants_owned: int`, separate from environmental identifiers `Q0/Q1/Q2/...`;
- assigned and achieved crop, pasture, herd, hands, feed coverage, and WATER quota states;
- daily active crop surface, watering-need denominator, unique successfully serviced crop surface, care backlog, crop losses, harvest-ready surface, and harvested units;
- pasture target, constructed pasture, occupied pasture, animal counts by species, care/feed needs and completions, product units generated/collected/stored/sold;
- Wheat by role and provenance: seed, crop output, feed, shed, worker inventory, executed buy, executed sell, and loss;
- worker capacity, task target, route start/end, necessary transit, avoidable transit, completed loop, action failures, and contract expiry/inventory transfer;
- land order/application step, `T0`, and purchase-to-activation lag even though land is controlled;
- categorized cash flows for land, hires/contracts, seeds, animals, pasture/structures, feed/product buys, executed sales, and other engine charges;
- terminal inventory quantity by product and provenance;
- `unsold_inventory_value_estimate` only with explicit price method and provenance; it is never `realized_value`.

### Preregistered diagnostic metrics

No metric below incorporates `final_money` as an input.

```text
watering_execution_rate = unique successful crop-day WATER effects / unique crop-day watering needs
watering_continuity = productive days with watering_execution_rate >= 0.50 / productive days
crop_target_attainment = daily active crop surface / assigned crop target
maintained_crop_surface = daily serviced and surviving crop tiles, reported alongside active and harvest-ready counts
action_failure_rate = failed or no-op executed attempts / requested actor actions
pasture_occupancy = occupied pasture / constructed pasture
feed_coverage_days = accessible feed units / expected next-day feed demand
external_feed_dependency = executed market-bought feed used / total feed used
necessary_transit_fraction = MOVE steps linked to a completed productive/logistic target / all MOVE steps
realized_product_margin = executed product sale value - attributed executed acquisition/feed/structure/contract costs
terminal_unsold_quantity = sum of unsold product units, with product breakdown retained
```

`maintained_crop_surface`, movement attribution, and cost attribution must be preregistered in the eventual frozen protocol before runs. `state_capacity_alignment` remains component-only and `NOT_YET_TUNABLE`; E16 does not construct a weighted composite.

## H. ANALYSIS PLAN

### Analysis populations and layer separation

1. **Assigned-cell / intention-to-treat population:** all valid infrastructure episodes, including policy failures and gameplay disqualifications. This is primary for MODEL_VALIDITY under the specified policy realization.
2. **Realization diagnostics:** assigned versus achieved watering service, crop surface, herd, pasture, workforce, and cash state. These diagnose POLICY_REALIZATION and are not substituted for randomized assignments in primary contrasts.
3. **Implementation audit:** configuration/hash allowlist, event reconciliation, action application, completion, and unknown failure reasons diagnose IMPLEMENTATION_FIDELITY.

If assignment does not move its realized mechanism, E16 may reject the implementation or policy realization but cannot claim the underlying model relation was falsified.

### Primary comparisons - Stage A

For every `(seed, seat)` block compute paired differences for `final_money`, completion, maintained crop surface, watering service/continuity, action failures, realized cash flow, and terminal unsold inventory.

- WATER effect at low crop: `A02 - A01`.
- WATER effect at high crop: `A04 - A03`.
- Primary interaction: `(A04 - A03) - (A02 - A01)`.
- Watering transition at crop 25: ordered A03 -> A06 -> A04.
- Crop transition under HIGH: ordered A02 -> A07 -> A04.
- Joint-middle curvature: A05 versus bilinear interpolation of the four corner cells, with the exact 10/17/25 coordinate weights stated in the analysis output.

The interaction is supported only if assigned priority is realized and the difference-in-differences has a consistent mechanism-aligned direction in at least four of six seed/seat blocks. With only three seeds, report all six paired values, median, range, and sign count; do not claim statistical validation or rely on asymptotic p-values.

### Primary comparisons - Stage B

- Pasture opportunity cost at herd 4: `B02 - B01`.
- Pasture opportunity cost at herd 10: `B04 - B03`.
- Pasture x herd interaction: `(B04 - B03) - (B02 - B01)`, where the pasture treatment is `EXCESS_18` versus `MINIMUM_SUPPORT`.
- Herd response at fixed pasture 18: ordered B02 -> B04 -> B05 (4 -> 10 -> 17 animals).
- Supported-bundle response: ordered B01 -> B03 -> B05, interpreted as total scale package rather than an isolated herd effect because pasture also changes.

Executed livestock product value must be reported with acquisition, feed, pasture, contract, and terminal inventory components. BUY/SELL requests alone cannot support an economic conclusion.

### Secondary comparisons

- Assigned-versus-achieved treatment gaps by cell and block.
- Action failure reason, route completion, necessary transit, feed dependency, cash shortfall, product-to-sale lag, and terminal inventory decomposition.
- Opponent `final_money` and match money delta as competitive-context diagnostics, never substitutes for treatment policy `final_money`.
- Execution-aware and value-aware `productive_action_share` only as LOW-priority diagnostics; no threshold or cell selection uses them.

### Failure, outlier, and missing-data rules

- Disqualification/completion failure is reported as an outcome; do not drop it from rates or primary qualitative ordering.
- Do not trim, winsorize, or remove a seed because its economic result is extreme.
- Report raw episode values, block-paired differences, median, range, and sign consistency. Mean/standard deviation may be supplementary.
- Missing telemetry does not authorize imputation of execution, price, value, or success. A missing mandatory ledger field fails the instrumentation gate or marks the affected episode non-interpretable for that metric.
- A confirmed infrastructure rerun follows Section F; no other reruns are allowed.

### Permitted conclusions

- classify candidate failure, transition, and competitive working regions inside the sampled controls;
- retain, revise, deprioritize, or mark unresolved the two interaction hypotheses;
- narrow future TRAINING values for assigned parameters;
- diagnose model validity separately from policy realization and implementation fidelity;
- report opponent-conditional training effects and confounders.

### Forbidden conclusions

- any optimum, globally best policy, validation, generalization, or Kaggle claim;
- reuse of E16 seeds/opponent outcomes as later independent validation or test;
- causal interpretation of realized post-treatment metrics without the assigned-cell contrasts;
- inference about `quadrants_owned = 3`, detailed crop mix, cash-floor optimum, workforce optimum, species margin, routing optimum, or endgame optimum;
- equation of requested actions/orders with execution or realized value;
- use of `final_money` inside a composite feature or Stage B advancement rule;
- opponent-general conclusions from the single fixed opponent.

## I. INFORMATION-GAIN AUDIT

```text
cell_id: A01_LOW_WATER_LOW_CROP
information_gained: low-crop watering baseline and evidence on whether even a small working set crosses the service failure region.
what_is_lost_if_removed: A02-A01 main effect and the complete corner interaction.
```

```text
cell_id: A02_HIGH_WATER_LOW_CROP
information_gained: high-service response at crop 10 and the lowest candidate Stage B capacity anchor.
what_is_lost_if_removed: watering effect at low crop and crop-scale curve under HIGH.
```

```text
cell_id: A03_LOW_WATER_HIGH_CROP
information_gained: high-load stress response under low service.
what_is_lost_if_removed: the strongest falsification cell for the service x surface interaction.
```

```text
cell_id: A04_HIGH_WATER_HIGH_CROP
information_gained: high-high competitive corner and largest candidate Stage B anchor.
what_is_lost_if_removed: full interaction, high-crop watering effect, and capacity test at crop 25.
```

```text
cell_id: A05_MID_WATER_MID_CROP
information_gained: direct observation of the joint unobserved middle and curvature residual.
what_is_lost_if_removed: ability to detect a diagonal transition not represented by single-axis bridges.
```

```text
cell_id: A06_MID_WATER_HIGH_CROP
information_gained: middle watering point at the crop load where service is most stressed.
what_is_lost_if_removed: localization of the service transition at crop 25.
```

```text
cell_id: A07_HIGH_WATER_MID_CROP
information_gained: middle crop point under high service and an intermediate Stage B anchor candidate.
what_is_lost_if_removed: localization of crop capacity between 10 and 25 under adequate intent.
```

```text
cell_id: B01_HERD4_PASTURE5
information_gained: compact livestock baseline under the selected crop-service anchor.
what_is_lost_if_removed: both the low-herd pasture contrast and a supported-bundle baseline.
```

```text
cell_id: B02_HERD4_PASTURE18
information_gained: direct excess-pasture opportunity cost at fixed low herd and herd-4 point at pasture 18.
what_is_lost_if_removed: pasture cannot be separated cleanly from animal scale.
```

```text
cell_id: B03_HERD10_PASTURE11
information_gained: middle-herd response with minimum-support pasture.
what_is_lost_if_removed: the 4-17 gap remains unsampled under compact pasture and the second pasture contrast disappears.
```

```text
cell_id: B04_HERD10_PASTURE18
information_gained: excess-pasture effect at middle herd and middle herd effect at fixed pasture 18.
what_is_lost_if_removed: both the interaction estimate and the lower segment of the fixed-pasture herd curve.
```

```text
cell_id: B05_HERD17_PASTURE18
information_gained: controlled test of the E15 failure-scale herd region.
what_is_lost_if_removed: no cell directly probes whether the high herd remains harmful after bundle confounders are controlled.
```

### Cells eliminated during design

- A full `3 x 3` irrigation/crop factorial was rejected. Cells `(LOW,17)` and `(MID,10)` do not add as much transition information as the two retained axis bridges and center.
- A full herd x pasture factorial was rejected because several low-pasture/high-herd combinations are structurally infeasible and would test placement failure rather than economic interaction.
- Dedicated workforce, crop-mix, routing, cash, endgame, species, market-mix, land, and `productive_action_share` cells were eliminated because they would dilute information gain and violate consolidated priorities.
- No `quadrants_owned = 3` cell is included; land remains a controlled unresolved region for later training.

No retained cell is redundant under the stated primary contrasts.

## J. COST

### PREFERRED

```text
total_cells: 12 planned maximum (7 Stage A + 5 Stage B)
episodes_per_cell: 6 (3 common seeds x 2 seats)
total_episodes: 72 maximum; 42 if Stage B is blocked
relative_cost_vs_E15: 24x maximum by episode count; E15 used 3 episodes
```

### MINIMAL

```text
total_cells: 12 planned maximum
episodes_per_cell: 4 (first 2 preregistered seeds x 2 seats)
total_episodes: 48 maximum; 28 if Stage B is blocked
relative_cost_vs_E15: 16x maximum by episode count
```

The MINIMAL version preserves every epistemic contrast but leaves only two independent seed blocks, making sign consistency fragile and one seed capable of dominating an initial bound. The PREFERRED version is recommended because the third seed buys more information than adding another factor level or opponent. Neither version is validation. Instrumentation smoke runs are implementation QA and excluded from training totals and model updates.

## K. DESIGN RISKS

1. **Ledger misattribution or incomplete reconciliation:** invalidates the distinction between requested and executed actions/transactions. Mitigation: blocking E0 gate and conservation checks.
2. **Assigned factors are not realized:** WATER quota, crop target, herd, or pasture may not be achieved. Mitigation: intention-to-treat primary analysis plus explicit policy-realization diagnostics; never relabel cells by achieved value.
3. **High herd is capital-constrained before service burden is expressed:** the common cash rule may turn B05 into an acquisition failure. Mitigation: retain as a valid policy-realization outcome and decompose acquisition, cash, and achieved herd; do not infer herd biology if target is not reached.
4. **Stage B anchor rule conditions on Stage A behavior:** B is conditional on an operationally feasible crop background. Mitigation: rule is preregistered, excludes `final_money`, and all A results remain reported; B claims are conditional on `C*`.
5. **Single opponent induces opponent-conditional estimates:** shared-market behavior may interact with treatments. Mitigation: freeze opponent and seats for training; prohibit generalization until independent opponent validation.
6. **Three seeds remain a small training sample:** nonlinear seed effects may be missed. Mitigation: shared blocks, seat swap, raw paired results, no asymptotic validation claims, and later unused validation seeds.
7. **Fixed workforce/crop mix/feed/cash modules can define the observed interaction:** controls improve identifiability but limit scope. Mitigation: state the conditional regime explicitly and leave those features unresolved for later rounds.

## L. RECOMMENDATION

The preferred design is the smallest proposal here that simultaneously retains a 2x2 irrigation/surface interaction, samples both transition axes and the joint middle, separates pasture cost at fixed herd twice, samples herd at fixed pasture through low/middle/high regions, and blocks invalid livestock inference when no crop-service anchor is realized.

```text
RECOMMENDED_DESIGN: E16-CODEX-S12-STAGED-PREFERRED
READY_FOR_CROSS_REVIEW: YES
BLOCKERS: NONE
```

Cross-review may change controls, cells, seeds, or opponent protocol before a common E16 freeze. It must not reinterpret this proposal as implementation, validation, an optimum claim, or authorization to read future E16 results as independent test evidence.
