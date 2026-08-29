# CODEX Candidate MODEL_SPEC Revision after E15

- **MODELER_ID:** `CODEX`
- **Status:** candidate revision; non frozen
- **Scope:** post-E15 feature, relationship and initial-bound revision only
- **Date:** 2026-08-29

This document does not replace the frozen E15 MODEL_SPEC, does not define an E16 design, and does not contain policy or implementation changes. All numerical values below are observed regions or candidates for future training, never optima.

## 1. Provenance and epistemic boundaries

1. **METHODOLOGICAL FRAME:** `README.md`. The object of study is the explicit model; policy realization and implementation fidelity are separate layers. Evidence used for training or bounding cannot later serve as independent validation.
2. **E15 FROZEN MODEL DECLARATION:** `results/e15/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md`. Its central thesis is a capital-to-cash chain: capital -> productive asset -> activation -> maintenance -> harvest/collection -> sale -> reinvestable cash.
3. **PRIMARY E15 EVIDENCE:** the frozen manifest plus `summary.json`, `telemetry.json`, and `raw_replay.json` for M1, M2, and M3. The replay prevails over later summaries where they disagree.
4. **POST-E15 SELF CAPABILITY CHECK:** `results/post_e15/capability_check/CODEX_CAPABILITY_CHECK.md`.
5. **YOUR INFERENCE:** every classification, candidate bound, interaction, and training priority in this revision unless explicitly labelled as an observed value.

No post-E15 output from another modeler was consulted.

## 2. Baseline reconstruction

### 2.1 Frozen ex-ante model

The frozen CODEX declaration ranked monetized throughput per action, deployable-capital timing, revenue breadth/conversion, land activation payback, livestock product flow, maintained crop surface, and logistics completion above raw asset counts. It already deprecated fixed herd constants, field cleanliness as an autonomous objective, and an unconditional quadrant target. It treated E15 as feature discrimination and initial bounding, not optimization.

The principal ex-ante hypotheses were:

- owned land has value only when activated and paid back;
- worker count matters through completed, monetized capacity rather than by itself;
- maintained and harvested surface matters more than planted or owned surface;
- livestock is an economic product engine only when pasture, feed, workforce, collection, sale, and cash conversion remain aligned;
- inventory is not revenue until sold, and sale proceeds matter through reinvestment timing;
- movement is a cost only after necessary transit is separated from avoidable overhead;
- local/Kaggle fidelity and endgame liquidation are distinct diagnostic subsystems.

### 2.2 Primary E15 reconstruction

E15 was a three-match frozen pairwise round robin, 720 steps per match, with a different seed for each pairing.

| Match | Seed | Outcome | WATER requests | Max active-crop proxy | Max pasture / animals | Max hands | Min observed cash |
|---|---:|---|---|---|---|---|---|
| M1 | 1113294977 | Antigravity 8,672; **Codex 20,461** | 34; 439 | 8; 28 | 18/18; 9/7 | 12; 10 | 25; 220 |
| M2 | 3033283457 | Codex 27,510; **Copilot 37,752** | 475; 446 | 37; 28 | 9/7; 5/4 | 10; 10 | 331; 87 |
| M3 | 3122977751 | **Copilot 26,629**; Antigravity 9,371 | 439; 30 | 25; 9 | 5/4; 18/18 | 9; 12 | 105; 19 |

**YOUR INFERENCE from primary replay:** the mean end-of-day fraction of active crops with `watered_today=true`, over productive days 0-27, is 0.082 and 0.144 for the two Antigravity runs, 0.711 and 0.733 for Codex, and 0.752 and 0.739 for Copilot. This is a declared proxy, not a canonical E15 metric. The HARVEST/PLANT request ratio is 3.74-4.45 in the two low-outcome runs and 0.72-0.98 in the other four observations.

The requested BUY_PRODUCT quantities are 904-1,889 and requested SELL quantities are 1,095-2,033 across the six policy-match observations. Those are requests, not executed transaction quantities. They cannot establish expenditure, revenue, churn, or conversion rates.

For CODEX specifically, both replays realize 2 quadrants, 9 pasture, 7 animals, and 10 hands. The crop proxy rises from 28 in M1 to 37 in M2 and WATER requests rise from 439 to 475, while M2 still loses to a 28-crop, 5-pasture, 4-animal, 10-hand policy. Therefore the low-service failure regime is discriminated, but values above that regime are not monotonically ordered by raw surface, WATER count, or raw productive-action share.

### 2.3 Layer diagnosis

**MODEL_VALIDITY: PARTIALLY_SUPPORTED.** The capital-to-cash chain remains coherent and E15 supports keeping irrigation service, maintained crop surface, dispatch effectiveness, pasture/crop allocation, herd scale, cash protection, and capacity alignment in the feature space. E15 does not isolate their causal effects, identify optima, or validate the model. Raw land, workforce, herd, crop, WATER, and action-share magnitudes are not monotonic predictors within the observed above-floor regime.

**POLICY_REALIZATION: PARTIALLY_SUPPORTED.** CODEX realizes a crop-heavy, consistently watered 2Q working set and a moderate herd. It does not demonstrate the promised marginal-payback logic for expansion, hire, livestock, or market conversion. In M2, the larger crop working set and higher raw productive-action share do not convert into the best terminal cash.

**IMPLEMENTATION_FIDELITY: PARTIALLY_SUPPORTED.** The frozen code completes both 720-step matches and produces a stable behavioral fingerprint. However, X1.15 variant D delegates workforce choice to a calendar schedule while fewer than 3 quadrants are owned; actual peak hands remain 10 despite a technical cap of 12. Its Q2 purchase branch is never realized. Its local `realized_revenue` counters are incremented when SELL orders are emitted using the current displayed price, before execution is verified. These implementation choices do not faithfully measure executed monetization or fully realize elastic, payback-based co-scaling.

### 2.4 Proposition disposition

**Supported as training hypotheses:** a severe irrigation/maintenance shortfall is associated with the replicated low-output signature; maintained crop surface and livestock/pasture scale interact; raw movement and repeated action requests require effectiveness qualification; cash protection and conversion timing remain economically relevant.

**Weakened:** more owned land, more workforce, more animals, more maintained crops, more WATER, or a larger raw productive-action share are individually better. E15 supports conditional and potentially thresholded/non-monotonic relationships instead.

**Falsified in their narrow formulation:** `requested transaction quantity = executed quantity/value`; CODEX's pre-execution revenue counter as proof of realized revenue; raw productive-action share as a monotonic sufficient ranking metric.

**Unresolved:** executed market economics, crop and livestock margins, marginal hire/land payback, feed dependency, movement necessity, state-capacity formula, independent seed generalization, and local/Kaggle fidelity.

### 2.5 Correction to the self capability check

The self capability check classified `productive_action_share` as `NOT_FEATURE`. That conclusion is too strong. M2 shows that the current gross share is not a monotonic sufficient predictor, but it does not show that action composition/effectiveness has no explanatory value. This revision corrects the concept to `UNRESOLVED`, retains it as a derived diagnostic, and requires a shared taxonomy plus executed action effects. This is a **YOUR INFERENCE correcting POST-E15 SELF CAPABILITY CHECK from PRIMARY E15 EVIDENCE**.

## 3. Concept-by-concept revision

### A. Land and productive surface

```text
concept_id: land_surface_total
feature_status: UNRESOLVED
e15_relationship: conditional and non_monotonic; 2Q co-occurs with higher outcomes and 3Q with the replicated failure bundle, but land is not isolated.
current_initial_bound: not_established; observed values are 2Q in four higher-outcome observations and 3Q in two low-outcome observations, with the 2Q-3Q transition fully confounded.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: compare 2Q and 3Q only after activation, workload, herd, and post-purchase cash are controlled.
confounders: purchase timing, activated surface, crop/pasture split, workforce, herd, cash, seed, and implementation.
validation_requirement: after training, replicate the selected land rule on unseen seeds and opponents with the same activation accounting.
falsification_condition: controlled 3Q activation consistently outperforms or underperforms 2Q independently of the bundled factors.
change_from_e15_spec: REVISED
change_rationale: the frozen spec used land conditionally; E15 strengthens the warning against treating quadrant count as a direct feature but cannot resolve its sign.
```

```text
concept_id: land_purchase_timing
feature_status: FEATURE
e15_relationship: conditional interaction with deployable capital and activation readiness.
current_initial_bound: not_established; the second quadrant is first observed at day 11 hour 1 for Codex/Copilot, while Antigravity reaches two quadrants at day 9 and three at day 18-19.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: readiness gates at no prior monetization, partial prior-surface monetization, and full measured activation/payback readiness.
confounders: different land counts, cash costs, crop horizon, workforce, and policy bundles.
validation_requirement: validate the trained gate on unseen seeds using executed cash-flow and purchase-to-activation telemetry.
falsification_condition: purchase timing has no repeatable effect after land count and activation are controlled.
change_from_e15_spec: UNCHANGED
change_rationale: timing remains a primary lever, but E15 supplies no optimal day or causal threshold.
```

```text
concept_id: activated_land_surface
feature_status: FEATURE
e15_relationship: positive only through maintained and monetized use; conditional on service capacity.
current_initial_bound: not_established; active-crop and pasture snapshots are partial proxies, not a complete activation definition.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure 25%, 50%, and 75% of owned surface simultaneously active and serviced, preserving crop/pasture breakdown.
confounders: mere planting, weeds, watering, pasture without animals, horizon, and sale lag.
validation_requirement: confirm the preregistered activation formula predicts future monetized output on independent episodes.
falsification_condition: activation measured without target leakage adds no predictive information beyond owned surface.
change_from_e15_spec: UNCHANGED
change_rationale: the owned-versus-activated distinction remains central and is not contradicted by E15.
```

```text
concept_id: crop_surface_maintained
feature_status: FEATURE
e15_relationship: positive below a service floor, then conditional and potentially non_monotonic.
current_initial_bound: observed low-outcome max active-crop proxy 8-9 and higher-outcome region 25-37; 10-24 is unobserved and active crops are not yet the formal maintained-surface metric.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: crop working-set caps 9, 13, 17, 21, and 25 with fixed irrigation service and herd bundle.
confounders: watering, crop mix, horizon, routing, pasture footprint, harvest, and sell-through.
validation_requirement: validate the trained region on unseen seeds using daily serviced surface and executed monetization.
falsification_condition: a 9-crop serviced set matches 25 crops consistently, or 25 crops fail to improve maintained/monetized flow over 9.
change_from_e15_spec: UNCHANGED
change_rationale: E15 directly strengthens the feature but only supplies a wide initial gap, not a threshold.
```

```text
concept_id: pasture_surface_maintained
feature_status: FEATURE
e15_relationship: conditional; useful only relative to supported livestock and the arable opportunity cost.
current_initial_bound: observed pasture maxima are 5, 9, and 18; 18 belongs to the replicated low-output bundle, while 5-9 belongs to higher-output bundles.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: 5, 9, 13, and 18 maintained pasture at fixed herd and owned land.
confounders: herd size, empty pasture, feed, workforce, arable surface, and product monetization.
validation_requirement: validate pasture contribution on independent episodes with pasture occupancy and livestock margin telemetry.
falsification_condition: maintained pasture adds no information once animal count and arable opportunity cost are known.
change_from_e15_spec: REVISED
change_rationale: E15 makes the pasture component independently measurable enough to elevate it from an implicit subsystem term.
```

```text
concept_id: maintained_productive_surface
feature_status: FEATURE
e15_relationship: conditional interaction; crop and pasture components must not be collapsed without value and service weights.
current_initial_bound: not_established; observed bundles range from 8-9 crops plus 18 pasture to 25-37 crops plus 5-9 pasture.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: preregister component-wise crop/pasture serviced areas and compare unweighted versus monetization-weighted aggregates.
confounders: aggregation weights, empty pasture, crop health, horizon, and target leakage from revenue.
validation_requirement: validate any aggregate formula out of sample while retaining its component breakdown.
falsification_condition: the aggregate is less stable or less informative than its separate crop and pasture components.
change_from_e15_spec: UNCHANGED
change_rationale: the concept remains useful only with the canonical breakdown and an explicit formula.
```

```text
concept_id: monetized_productive_output
feature_status: FEATURE
e15_relationship: positive by definition as a throughput mediator, with magnitude and source unresolved.
current_initial_bound: not_established; E15 records final cash and requests but lacks an executed product-to-sale ledger.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure executed value per product, per productive tile, and per day rather than impose target values.
confounders: starting cash, asset purchases, wages, market prices, unsold inventory, and shared-market effects.
validation_requirement: validate the metric's link to future cash on independent runs without using final money in its construction.
falsification_condition: executed productive output does not mediate the relationship between maintained surface and cash.
change_from_e15_spec: UNCHANGED
change_rationale: E15 cannot quantify it, but the production-to-cash distinction remains structurally necessary.
```

```text
concept_id: land_activation_payback
feature_status: FEATURE
e15_relationship: conditional and potentially thresholded by remaining horizon.
current_initial_bound: not_established; no purchase-cost-to-attributed-cash-return series exists in E15.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure payback lag and return at 25%, 50%, and 100% recovery of acquisition plus activation cost.
confounders: pre-existing production, shared workers, asset residual value, price changes, and attribution method.
validation_requirement: validate a preregistered attribution rule on held-out episodes after the gate is trained.
falsification_condition: attributed land payback does not distinguish beneficial from harmful expansion out of sample.
change_from_e15_spec: UNCHANGED
change_rationale: the frozen hypothesis survives, but E15 supplies no direct payback observation.
```

```text
concept_id: pasture_arable_surface_tradeoff
feature_status: FEATURE
e15_relationship: interaction; negative when pasture exceeds supported livestock value, otherwise unresolved.
current_initial_bound: observed compact region 5-9 pasture with 25-37 crops and failure bundle 18 pasture with 8-9 crops; 9-18 is unobserved.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: pasture 5, 9, 13, and 18 at fixed land, herd, workforce, and crop service.
confounders: herd, empty pasture, feed, crop type, land total, and product margins.
validation_requirement: confirm the selected split on unseen seeds using executed revenue and opportunity-cost accounting.
falsification_condition: changing pasture at fixed herd and capacity does not change maintained crop output or livestock return.
change_from_e15_spec: REVISED
change_rationale: E15 strengthens the tradeoff from an implicit mapping to an explicit candidate interaction.
```

### B. Workforce, dispatch, and logistics

```text
concept_id: workforce_headcount
feature_status: UNRESOLVED
e15_relationship: conditional and non_monotonic; headcount is not throughput.
current_initial_bound: observed 9-10 hands in higher-output bundles and 12 in the low-output bundle; M2 has 10 for both policies and different outcomes.
parameter_or_hyperparameter: PARAMETER
next_training_values: 9, 10, 11, and 12 hands at fixed working set, routing, and contract schedule.
confounders: workload, movement, wages, contract timing, order slots, and action effectiveness.
validation_requirement: validate the selected headcount on unseen seeds using executed useful work and net marginal cash.
falsification_condition: headcount alone produces a repeatable effect once workload and routing are controlled.
change_from_e15_spec: REVISED
change_rationale: the frozen model already rejected raw count as value; E15 leaves the controllable count unresolved rather than positively ranked.
```

```text
concept_id: worker_capacity_available
feature_status: FEATURE
e15_relationship: positive up to workload saturation, conditional on routing and valid dispatch.
current_initial_bound: not_established; E15 observes hand counts but not theoretical versus actually usable action capacity.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure 60%, 80%, and 95% useful-capacity utilization at a fixed worker count.
confounders: Farmer inclusion, contract expiry, travel, inventory handling, and invalid actions.
validation_requirement: validate the capacity definition and its marginal value on independent runs.
falsification_condition: declared available capacity does not predict completed useful actions better than headcount.
change_from_e15_spec: UNCHANGED
change_rationale: the canonical separation between headcount and capacity remains essential.
```

```text
concept_id: hire_order_scheduling
feature_status: FEATURE
e15_relationship: conditional interaction with workload onset, contract expiry, cash, and order slots.
current_initial_bound: not_established; HIRE request counts are 232 for Codex/Copilot and 284-286 for Antigravity, but renewals and executed hires are not separated.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: early calendar hiring, just-in-time hiring, and backlog-triggered hiring with identical maximum headcount.
confounders: contract length, failed orders, daily batch limits, wage timing, and inherited calendar logic.
validation_requirement: validate the trained schedule independently with executed hire and contract-state telemetry.
falsification_condition: schedule has no effect at fixed headcount, contract coverage, and cash.
change_from_e15_spec: REVISED
change_rationale: CODEX implementation exposes calendar dependence, so scheduling needs explicit treatment rather than remaining incidental.
```

```text
concept_id: marginal_hire_payback
feature_status: FEATURE
e15_relationship: expected positive only while marginal completed value exceeds hire and coordination cost.
current_initial_bound: not_established; E15 lacks counterfactual attribution for the tenth through twelfth hand.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure incremental net cash and useful completions for +1 and +2 hands around 9-10.
confounders: simultaneous workload scaling, route assignment, wages, expiry, and seed.
validation_requirement: validate the learned stopping rule on held-out episodes with the same attribution formula.
falsification_condition: marginal payback estimates do not generalize or reverse under unchanged workload.
change_from_e15_spec: UNCHANGED
change_rationale: the concept remains the correct economic interpretation of hiring, though E15 does not estimate it.
```

```text
concept_id: productive_action_share
feature_status: UNRESOLVED
e15_relationship: unresolved; the current gross proxy is non_monotonic and composition-sensitive.
current_initial_bound: not_established; in M2 CODEX has about 18.35% versus Copilot 17.24% under the current gross taxonomy and lower final money.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: compare gross share with executed-useful share and value-weighted share under a shared action taxonomy.
confounders: action mix, necessary movement, retries, action failure, product value, and denominator choice.
validation_requirement: preregister the taxonomy and validate predictive value on independent episodes after any threshold is trained.
falsification_condition: no preregistered share variant adds out-of-sample information beyond component action flows.
change_from_e15_spec: REVISED
change_rationale: corrects the self capability check; M2 rejects a monotonic sufficient proxy, not the entire concept.
```

```text
concept_id: movement_overhead
feature_status: FEATURE
e15_relationship: negative only for movement not required to complete productive or logistical loops.
current_initial_bound: raw MOVE requests are 5,019-5,047 in the low-output runs and 3,761-3,768 in the other runs; necessary and avoidable movement are not separated.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure overhead after classifying each move by subsequent completed task within fixed 1-, 2-, and 4-step windows.
confounders: farm size, worker count, path length, transport, and task location.
validation_requirement: validate the attribution window and overhead relationship on unseen trajectories.
falsification_condition: classified avoidable movement has no repeatable cost once topology and workload are controlled.
change_from_e15_spec: UNCHANGED
change_rationale: E15 supports continued attention to logistics but not the equation MOVE equals waste.
```

```text
concept_id: necessary_transit_fraction
feature_status: FEATURE
e15_relationship: qualifies movement_overhead; expected positive association with route completion, sign versus money conditional.
current_initial_bound: not_established; positions and MOVE requests are observable, but no attribution rule is present.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: classify transit using 1-, 2-, and 4-step completion windows and report sensitivity.
confounders: multi-step paths, rerouting, inventory transport, competing targets, and simultaneous task changes.
validation_requirement: validate the classification against manually audited held-out route samples and independent episodes.
falsification_condition: the classification cannot reliably distinguish functional paths from loops.
change_from_e15_spec: ADDED
change_rationale: the frozen spec omitted this concept, but E15 makes it necessary to interpret its own movement thesis correctly.
```

```text
concept_id: routing_completion_efficiency
feature_status: FEATURE
e15_relationship: positive and conditional on reachable valid targets.
current_initial_bound: not_established; raw action counts and positions permit future derivation but no completion-linked route metric exists.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure completed task loops per move and completion within 1, 2, and 4 steps after target acquisition.
confounders: target churn, task invalidation, worker inventory, land topology, and action ordering.
validation_requirement: validate a preregistered route-completion definition on unseen episodes.
falsification_condition: route completion adds no predictive value beyond movement count and workload.
change_from_e15_spec: UNCHANGED
change_rationale: the concept remains central but requires an executable metric.
```

```text
concept_id: action_dispatch_failure
feature_status: FEATURE
e15_relationship: negative and plausibly thresholded; current evidence is a retry/failure proxy.
current_initial_bound: observed HARVEST/PLANT request ratio 3.74-4.45 in low outcomes and 0.72-0.98 elsewhere; 0.98-3.74 is unobserved and not a proven failure threshold.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: induce proxy ratios near 1.0, 1.7, 2.5, and 3.7 while recording exact action effects.
confounders: repeatable yields, inventory capacity, distance, concurrent actors, and valid but zero-yield requests.
validation_requirement: validate the action-effect taxonomy and learned failure region on unseen episodes.
falsification_condition: an action-effect ledger shows high ratios are mostly useful or reducing them does not release capacity.
change_from_e15_spec: REVISED
change_rationale: E15 elevates dispatch failure from a partial symptom to a first-class measurement need.
```

```text
concept_id: worker_action_monetization_rate
feature_status: FEATURE
e15_relationship: positive in economic interpretation, with macro and net forms potentially non_monotonic under differing product mixes.
current_initial_bound: not_established; final money per requested action is not realized revenue per executed useful action.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: record macro realized revenue/all actions and net realized revenue/executed useful non-move actions by product.
confounders: starting assets, purchase costs, terminal inventory, price, and attribution lag.
validation_requirement: validate both preregistered forms on held-out episodes without final-outcome leakage.
falsification_condition: neither form predicts or mediates cash conversion better than raw component flows.
change_from_e15_spec: UNCHANGED
change_rationale: the top frozen factor survives conceptually, but E15 did not observe its required numerator or denominator.
```

### C. Crop production and care

```text
concept_id: crop_care_action_flow
feature_status: FEATURE
e15_relationship: positive only when requested care is executed and completes crop needs.
current_initial_bound: not_established; E15 separates requested PLANT, WATER, and HARVEST counts but not successful care flow.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure requested, executed, successful, and redundant care flows per active-crop-day.
confounders: working-set size, decay rules, retries, crop type, and action ordering.
validation_requirement: validate the care-flow formula on independent episodes with action-effect telemetry.
falsification_condition: completed care flow does not explain maintained surface after active-crop exposure is controlled.
change_from_e15_spec: REVISED
change_rationale: E15 supports making the formerly broader mapping explicit and execution-aware.
```

```text
concept_id: planting_action_flow
feature_status: FEATURE
e15_relationship: conditional; planting creates workload and potential output but is not production by itself.
current_initial_bound: requested PLANT counts are 93-126 and do not rank final outcomes monotonically.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure executed planting per open serviced slot and completion-to-harvest conversion.
confounders: seed availability, crop mix, horizon, maintenance capacity, and replant cycles.
validation_requirement: validate trained planting intensity on unseen seeds using eventual harvest and sale attribution.
falsification_condition: planting flow adds no information beyond active surface and crop mix.
change_from_e15_spec: REVISED
change_rationale: the partial horizon proxy becomes an explicit flow with no assumed positive monotonicity.
```

```text
concept_id: watering_execution_rate
feature_status: FEATURE
e15_relationship: positive below a service floor, then conditional and not ordered by raw volume.
current_initial_bound: observed mean daily serviced proxy 0.082-0.144 in the replicated low-output bundle and 0.711-0.752 elsewhere; 0.144-0.711 is unobserved.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: mean daily serviced fractions 0.15, 0.30, 0.45, 0.60, and 0.72 at fixed crop exposure.
confounders: active-crop denominator, continuity, crop type, distance, workforce, and failed WATER actions.
validation_requirement: validate the trained service region on held-out seeds with executed WATER and daily need denominators.
falsification_condition: low service produces equivalent maintained surface and money under controlled workload, or high service does not improve them.
change_from_e15_spec: REVISED
change_rationale: E15 elevates watering from a broad maintenance component to a discriminating first-class feature.
```

```text
concept_id: watering_continuity
feature_status: FEATURE
e15_relationship: positive and plausibly thresholded across productive days.
current_initial_bound: serviced fraction at least 0.5 occurs on 2 of 24 productive days for Antigravity and 23-24 of 28 for Codex/Copilot; the middle region is unobserved.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: 25%, 50%, 75%, and 90% of productive days meeting a 0.5 serviced-fraction criterion.
confounders: crop replacement, harvest before snapshot, endgame, and denominator changes.
validation_requirement: validate continuity effects on unseen episodes with per-crop longitudinal service histories.
falsification_condition: breaking continuity at fixed total WATER does not reduce persistence, harvest, or cash.
change_from_e15_spec: REVISED
change_rationale: E15 turns an implicit maintenance property into an explicit candidate timing feature.
```

```text
concept_id: crop_harvest_action_flow
feature_status: FEATURE
e15_relationship: positive only for successful yield collection; repeated requests may indicate dispatch failure.
current_initial_bound: requested HARVEST counts are 91-414 and HARVEST/PLANT ratios separate 0.72-0.98 from 3.74-4.45, but successful harvest quantities are unavailable.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure successful harvests, yielded units, zero-effect requests, and lag from readiness to collection.
confounders: repeatable harvest rules, crop readiness, inventory capacity, and concurrent actions.
validation_requirement: validate the flow-to-revenue link independently with product-level transaction execution.
falsification_condition: successful harvest flow does not predict inventory growth or monetized crop output.
change_from_e15_spec: REVISED
change_rationale: E15 requires separating productive harvest flow from retry volume.
```

```text
concept_id: crop_care_completion_rate
feature_status: FEATURE
e15_relationship: positive, thresholded, and conditional on crop-specific needs.
current_initial_bound: not_established; the EOD watering proxy covers one care dimension and active crops do not supply a complete need denominator.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: 25%, 50%, 75%, and 90% of preregistered daily crop-care needs completed.
confounders: care taxonomy, differing crop needs, harvest timing, weeds, and concurrent replacement.
validation_requirement: validate the formula and trained region on independent longitudinal crop histories.
falsification_condition: completion rate fails to predict crop persistence, yield, or monetized output.
change_from_e15_spec: REVISED
change_rationale: the former broad proxy is retained but must gain an explicit denominator.
```

```text
concept_id: crop_decay_risk_window
feature_status: UNRESOLVED
e15_relationship: plausible thresholded timing constraint; relevant engine rule and exposure are not established by E15.
current_initial_bound: not_established; `consecutive_unwatered` is observable but no verified loss threshold or causal episode set is reconstructed.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: first verify the engine rule, then measure 0, 1, 2, and 3 consecutive unserviced days if those values are valid.
confounders: crop species, harvest/replant, fertilizer, weed state, and snapshot timing.
validation_requirement: validate any risk window against independent loss events after engine verification.
falsification_condition: engine inspection or replay transitions show no such decay mechanism in the modeled regime.
change_from_e15_spec: ADDED
change_rationale: the frozen CODEX spec omitted it; E15 exposes continuity as important but does not authorize a threshold.
```

```text
concept_id: crop_horizon_alignment
feature_status: FEATURE
e15_relationship: interaction between remaining time, crop cycle, maintenance, harvest, and sell-through.
current_initial_bound: not_established; no crop-cycle-to-sale lag is attributed in E15.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: initiation only when remaining horizon is 1.0, 1.5, or 2.0 measured crop-to-cash cycles.
confounders: crop type, maintenance delay, inventory lag, price, and endgame liquidation.
validation_requirement: validate the trained cutoff on unseen episodes and independently held-out crop cycles.
falsification_condition: horizon-aware initiation does not improve completed monetized cycles at fixed crop mix.
change_from_e15_spec: UNCHANGED
change_rationale: the frozen hypothesis remains sound but wholly unbounded by E15.
```

```text
concept_id: crop_revenue_mix
feature_status: UNRESOLVED
e15_relationship: conditional and potentially non_monotonic across price, cycle time, and service cost.
current_initial_bound: not_established; E15 has crop states, prices, and SELL requests but no executed revenue breakdown.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure executed crop revenue shares by Wheat, Carrot, Tomato, Strawberry, and Melon before proposing mix bounds.
confounders: requested versus executed sales, crop quantities, initial inventory, market elasticity, and cycle completion.
validation_requirement: validate any trained revenue mix on unseen seeds with executed quantity and price.
falsification_condition: crop revenue composition has no stable relation to net cash after production cost and horizon are controlled.
change_from_e15_spec: REVISED
change_rationale: the frozen model used revenue breadth, but E15 cannot observe realized crop mix reliably.
```

### D. Feed, Wheat, and livestock

```text
concept_id: feed_availability
feature_status: FEATURE
e15_relationship: positive up to sufficiency, then inventory holding cost may dominate.
current_initial_bound: not_established; shed and worker Wheat states are observable, but feed demand coverage is not summarized.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure 1, 2, and 3 expected feed-days of coverage with shed, worker, and near-term crop sources separated.
confounders: herd/species, future Wheat harvest, market purchases, worker inventory, and timing.
validation_requirement: validate the coverage formula on unseen feeding episodes and loss outcomes.
falsification_condition: feed coverage does not predict successful livestock care or product flow.
change_from_e15_spec: UNCHANGED
change_rationale: availability remains a real constraint, distinct from self-sufficiency.
```

```text
concept_id: feed_security_buffer
feature_status: FEATURE
e15_relationship: thresholded and conditional on expected demand and replenishment lag.
current_initial_bound: not_established; the frozen implementation uses internal reserves, but E15 provides no executed demand-to-buffer comparison.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: 1, 3, and 5 feed-days above expected demand at fixed herd.
confounders: feed availability definition, purchase lead time, Wheat crop timing, and cash opportunity cost.
validation_requirement: validate the selected buffer on unseen demand and price sequences.
falsification_condition: buffer changes neither missed feeding nor net cash under controlled herd demand.
change_from_e15_spec: REVISED
change_rationale: E15 does not identify a reserve, but future training needs an explicit demand-relative hyperparameter.
```

```text
concept_id: feed_market_dependency
feature_status: UNRESOLVED
e15_relationship: unresolved and possibly non_monotonic; market supply can protect production or destroy margin.
current_initial_bound: not_established; winners request more BUY_PRODUCT Wheat in all three matches, but execution, consumption, resale, and net cost are unknown.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: executed external-feed shares 0.25, 0.50, and 0.75 at fixed herd and Wheat production.
confounders: Wheat resale, failed purchases, price, feed consumption, crop opportunity cost, and shared market.
validation_requirement: validate the trained dependency region on unseen price/seed episodes using executed flows.
falsification_condition: executed dependency has no stable effect, or its sign reverses after use and resale are accounted for.
change_from_e15_spec: REVISED
change_rationale: E15 request counts invalidate a simple negative interpretation and leave the economic relationship unresolved.
```

```text
concept_id: feed_market_expenditure
feature_status: UNRESOLVED
e15_relationship: negative as a cost, but potentially beneficial through avoided livestock interruption.
current_initial_bound: not_established; requested BUY_PRODUCT quantity cannot establish executed expenditure.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: record executed Wheat quantity times realized price, rejection, and downstream feed use per order.
confounders: non-feed product purchases, resale, price elasticity, and alternative Wheat production cost.
validation_requirement: validate expenditure-to-margin effects independently after a sourcing rule is trained.
falsification_condition: executed feed expenditure cannot be separated from other Wheat roles or does not affect net livestock margin.
change_from_e15_spec: REVISED
change_rationale: the partial frozen concept now requires a transaction ledger before it can be tuned.
```

```text
concept_id: wheat_operating_flow
feature_status: FEATURE
e15_relationship: interaction among seed, crop, feed, inventory, buy, sell, and cash roles.
current_initial_bound: not_established; requested BUY_PRODUCT Wheat quantities span 904-1,889 and higher request volume co-occurs with each match winner, without execution proof.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure role-tagged Wheat units and cash by source, destination, and holding interval.
confounders: transaction execution, resale, feed use, seed inventory, future harvest, and market price.
validation_requirement: validate any learned operating mix on unseen episodes with a conserved unit-flow ledger.
falsification_condition: role-tagged Wheat flow adds no information beyond total Wheat inventory.
change_from_e15_spec: UNCHANGED
change_rationale: E15 reinforces the need for a multi-role flow rather than a buy-volume judgment.
```

```text
concept_id: market_churn_cost
feature_status: UNRESOLVED
e15_relationship: plausibly negative when buy/sell cycles lose value, but not observable from requests.
current_initial_bound: not_established; no executed lot matching or realized price pair exists.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: match executed buy/sell lots over 1-, 3-, and 7-day windows and measure net value loss plus displaced productive use.
confounders: fungible Wheat sources, feed consumption, dynamic prices, and inventory carry.
validation_requirement: validate the lot-attribution method and learned churn sensitivity on independent episodes.
falsification_condition: matched cycles do not destroy value after productive use and price movement are included.
change_from_e15_spec: REVISED
change_rationale: E15 cannot support the frozen warning without executed transaction provenance.
```

```text
concept_id: livestock_headcount
feature_status: FEATURE
e15_relationship: conditional, non_monotonic, and interacting with pasture, feed, workforce, and cash.
current_initial_bound: observed higher-outcome region 4-7 animals and replicated low-output region 17-18; 7-17 is unobserved and no optimum is implied.
parameter_or_hyperparameter: PARAMETER
next_training_values: 4, 7, 10, 13, and 17 animals with species breakdown and fixed capacity bundle.
confounders: species, pasture, feed, workforce, product sales, capital cost, and crop opportunity cost.
validation_requirement: validate the trained herd region on unseen seeds with net product margin and service telemetry.
falsification_condition: 13-17 animals equal or exceed 4-7 under controlled supporting capacity, or herd count adds no information.
change_from_e15_spec: REVISED
change_rationale: fixed constants remain deprecated, but count stays a tunable conditional feature rather than a direct value proxy.
```

```text
concept_id: livestock_capacity
feature_status: FEATURE
e15_relationship: conditional upper bound created jointly by pasture, feed, workforce, and horizon.
current_initial_bound: not_established; 18 animals with 18 pasture fail as a bundle, while 4-7 with 5-9 pasture succeed, without capacity utilization data.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: define capacity from minimum of pasture, feed-day, care-action, and collection/sale capacities, then test 50%, 75%, and 100% utilization.
confounders: formula weights, species, product cycles, empty pasture, and transaction lag.
validation_requirement: validate the formula and utilization region on independent episodes.
falsification_condition: the composite capacity does not predict missed care or livestock product flow better than headcount.
change_from_e15_spec: REVISED
change_rationale: E15 makes capacity alignment explicit but does not quantify it.
```

```text
concept_id: pasture_capacity_alignment
feature_status: FEATURE
e15_relationship: interaction; both excess pasture and livestock crowding can reduce economic throughput.
current_initial_bound: observed pairs are approximately 5/4, 9/7, and 18/18 pasture/animal maxima; economic utilization is not established.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: pasture-to-animal ratios around observed 1.0, 1.25, and 1.5 plus an excess-pasture sentinel.
confounders: species requirements, empty pasture timing, care capacity, land opportunity cost, and herd growth.
validation_requirement: validate the selected alignment region on unseen episodes with occupancy and margin accounting.
falsification_condition: alignment ratios do not predict service or margin once separate pasture and herd values are included.
change_from_e15_spec: REVISED
change_rationale: the E15 bundles justify explicit interaction measurement, not a canonical ratio.
```

```text
concept_id: livestock_product_flow
feature_status: FEATURE
e15_relationship: positive only when care, collection, storage, sale, and realized value all complete.
current_initial_bound: not_established; CARE/FEED/HARVEST requests and inventories are observable, but the end-to-end executed product flow is absent.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure units produced, collected, stored, sold, and monetized by Milk and Wool cycle.
confounders: herd size, species, feed, worker inventory, contract loss, and market execution.
validation_requirement: validate the flow-to-net-cash relationship on independent episodes.
falsification_condition: completed livestock flow does not improve cash after all subsystem costs are attributed.
change_from_e15_spec: UNCHANGED
change_rationale: the economic engine remains in the feature space, but raw animal and action counts cannot confirm it.
```

```text
concept_id: species_margin_differential
feature_status: UNRESOLVED
e15_relationship: unresolved; possible conditional differences in capital, feed, care, cycle time, and price.
current_initial_bound: not_established; E15 does not isolate Cow versus Sheep executed costs and returns.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: measure net margin and payback separately for Cow and Sheep at matched capacity utilization.
confounders: mixed herds, different acquisition timing, pasture, feed, byproducts, and market prices.
validation_requirement: validate any learned differential on held-out species cohorts and episodes.
falsification_condition: no stable margin difference remains after full cost and timing attribution.
change_from_e15_spec: REVISED
change_rationale: the frozen partial distinction has no primary E15 margin evidence.
```

```text
concept_id: fertilizer_byproduct_flow
feature_status: UNRESOLVED
e15_relationship: positive only if generated, collected, retained, sold, and worth more than its capacity cost.
current_initial_bound: requested COLLECT_FERTILIZER is 15 in both low-output Antigravity runs and 0-2 elsewhere; executed units and revenue are unknown.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure generated, collected, stored, lost, and executed-sold Fertilizer units per animal-day.
confounders: herd size, collection opportunity cost, worker inventory, contract loss, and price.
validation_requirement: validate byproduct margin on independent episodes with full unit provenance.
falsification_condition: Fertilizer flow contributes no positive net value after collection and sale costs.
change_from_e15_spec: REVISED
change_rationale: E15 weakens the frozen assumption that collection requests demonstrate monetized byproduct value.
```

### E. Capital, market, conversion, and reinvestment

```text
concept_id: market_transaction_value
feature_status: UNRESOLVED
e15_relationship: primitive for expenditure and revenue; sign depends on BUY versus SELL and downstream use.
current_initial_bound: not_established; requested quantity and displayed pre-action price are observable, but executed quantity, realized price, and rejection are not.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: record each order with requested and executed quantity, observed/reconstructed/base-price source, realized unit price, value, and rejection reason.
confounders: order batching, simultaneous orders, price movement, market inventory, and partial fills.
validation_requirement: validate transaction-value reconstruction against an independent engine ledger before using it in held-out evaluation.
falsification_condition: reconstructed values fail to reconcile cash and inventory changes at transaction level.
change_from_e15_spec: ADDED
change_rationale: the frozen spec omitted the primitive, while E15 shows it is required to test its revenue and expenditure claims.
```

```text
concept_id: operating_cash_buffer
feature_status: FEATURE
e15_relationship: thresholded, conditional, and non_monotonic because excess idle cash can displace productive investment.
current_initial_bound: observed minima 19-25 in the replicated low-output bundle and 87-331 elsewhere; M2 winner reaches 87 versus CODEX 331, so higher is not always better and 25-87 is unresolved.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: policy floors 25, 50, 87, and 150 with identical obligations and investment options.
confounders: intentional investment, wage/feed liabilities, revenue timing, prices, and opponent effects.
validation_requirement: validate the trained floor on unseen seeds with obligation-specific shortfall and opportunity-cost accounting.
falsification_condition: low floors do not increase failures or high floors do not sacrifice profitable deployment under controlled obligations.
change_from_e15_spec: REVISED
change_rationale: E15 supplies an initial gap but rejects a simple more-cash-is-better interpretation.
```

```text
concept_id: deployable_capital_window
feature_status: FEATURE
e15_relationship: conditional timing state after measured obligations and before horizon closes.
current_initial_bound: not_established; total cash is observable, but obligations and attributed future receipts are not separated.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure deployable cash above 1.0, 1.5, and 2.0 expected obligation cycles rather than fixed currency alone.
confounders: obligation formula, uncertain receipts, market prices, contract timing, and asset liquidity.
validation_requirement: validate a preregistered obligations formula and deployment rule on independent episodes.
falsification_condition: the window does not improve investment payback discrimination beyond raw cash.
change_from_e15_spec: UNCHANGED
change_rationale: the concept remains central, but no E15 total-cash trajectory alone can establish it.
```

```text
concept_id: asset_liquidity_lag
feature_status: UNRESOLVED
e15_relationship: expected negative when capital returns after relevant obligations or episode end.
current_initial_bound: not_established; E15 lacks asset-attributed purchase-to-cash events.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: measure lag in hours/days and fractions of remaining horizon for land, crop, and livestock assets separately.
confounders: shared production, residual inventory value, price, reinvestment, and attribution rules.
validation_requirement: validate asset attribution and learned lag sensitivity on independent episodes.
falsification_condition: attributed lag has no stable relationship to realized net return.
change_from_e15_spec: REVISED
change_rationale: the frozen partial endgame proxy is insufficient for a general liquidity claim.
```

```text
concept_id: inventory_to_cash_conversion
feature_status: UNRESOLVED
e15_relationship: positive when executed at acceptable value and before cash is needed.
current_initial_bound: requested SELL counts are 198 in both low-output runs and 212-302 elsewhere, but order count/quantity does not establish execution or revenue.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: measure executed sold units/value divided by sellable units/value over 1-, 3-, and 7-day windows.
confounders: requested versus executed sales, order size, price, initial inventory, terminal inventory, and product mix.
validation_requirement: validate the trained conversion window on held-out episodes with transaction-level reconciliation.
falsification_condition: executed conversion does not predict reinvestable cash or terminal inventory after price is controlled.
change_from_e15_spec: REVISED
change_rationale: E15 cannot confirm a frozen primary factor without executed sales.
```

```text
concept_id: market_sellthrough_lag
feature_status: UNRESOLVED
e15_relationship: negative when sale delay blocks reinvestment or terminal liquidation; potentially positive if waiting improves price.
current_initial_bound: not_established; inventory availability and SELL requests are observable, but accepted-sale timestamps are not.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: measure 0-, 1-, 3-, and 7-day availability-to-executed-sale lags by product.
confounders: price movement, order rejection, deliberate holding, market batch limits, and inventory source.
validation_requirement: validate the lag-return tradeoff on independent price paths after training.
falsification_condition: lag has no stable effect on reinvestment or realized value when price is controlled.
change_from_e15_spec: REVISED
change_rationale: the frozen cadence proxy needs direct accepted-sale timing.
```

```text
concept_id: unsold_inventory_value
feature_status: UNRESOLVED
e15_relationship: conditional; terminal inventory is an opportunity cost unless residual value is credited by the environment.
current_initial_bound: not_established; terminal quantities and displayed prices can support labelled estimates, not realized value.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: report quantity plus valuation at observed terminal price, conservative reference price, and zero-liquidation value.
confounders: residual scoring rules, future sale feasibility, price elasticity, and product provenance.
validation_requirement: validate valuation conventions against independent executed liquidation episodes and engine scoring.
falsification_condition: estimated unsold value does not reconcile with any realizable or scored terminal value.
change_from_e15_spec: REVISED
change_rationale: E15 supports quantity observation but not the frozen warning's monetary magnitude.
```

```text
concept_id: reinvestment_cash_flow
feature_status: UNRESOLVED
e15_relationship: positive when executed sale proceeds become deployable before profitable opportunities close.
current_initial_bound: not_established; E15 has total cash trajectories but no source/use cash-flow attribution.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: tag executed sale proceeds and their next use within 1, 3, and 7 days.
confounders: mixed cash pool, other revenues/costs, simultaneous purchases, and counterfactual attribution.
validation_requirement: validate the attribution rule and trained reuse window on independent episodes.
falsification_condition: tagged proceeds do not affect later productive investment or net return.
change_from_e15_spec: REVISED
change_rationale: the frozen model's capital loop remains plausible, but E15 cannot trace it.
```

```text
concept_id: product_mix_revenue
feature_status: UNRESOLVED
e15_relationship: conditional and potentially diversification-shaped rather than monotonic in breadth.
current_initial_bound: not_established; E15 lacks executed revenue by crop, livestock product, and byproduct.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: measure executed revenue and net margin shares by crop, Milk, Wool, and Fertilizer before setting candidates.
confounders: production cost, cycle time, price, initial inventory, and requested versus executed sales.
validation_requirement: validate any selected mix on independent market/seed episodes with net, not gross, attribution.
falsification_condition: mix adds no out-of-sample information after total executed revenue and capacity costs are included.
change_from_e15_spec: REVISED
change_rationale: E15 does not observe the frozen revenue-breadth claim at transaction level.
```

```text
concept_id: price_realization_variance
feature_status: UNRESOLVED
e15_relationship: potentially negative versus a preregistered reference, with sign dependent on timing strategy.
current_initial_bound: not_established; displayed market prices exist, but realized executed prices do not.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: compare executed price with order-time, daily median, and fixed base-price references, each explicitly labelled.
confounders: partial fill, order delay, volume, shared market, and chosen reference.
validation_requirement: validate the reference and variance-return relation on independent market paths.
falsification_condition: no reference yields a stable, reconcilable realization metric.
change_from_e15_spec: ADDED
change_rationale: E15 market ambiguity makes this omitted concept necessary for future economic interpretation.
```

```text
concept_id: dynamic_market_price_elasticity
feature_status: UNRESOLVED
e15_relationship: plausible interaction between executed volume, market state, and realized price.
current_initial_bound: not_established; E15 contains displayed price/inventory snapshots and requests but no causal fill/price response.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: first verify engine response, then measure price change per executed unit in low, medium, and high volume bands.
confounders: opponent orders, time trend, inventory restoration, rejected orders, and simultaneous commodities.
validation_requirement: validate any elasticity estimate on independent price paths and order sequences.
falsification_condition: engine verification shows prices are exogenous to executed volume in this regime.
change_from_e15_spec: ADDED
change_rationale: the frozen spec omitted elasticity; E15 cannot resolve it but cannot safely ignore it when interpreting requested volume.
```

### F. Endgame and inventory integrity

```text
concept_id: shed_inventory_integrity
feature_status: UNRESOLVED
e15_relationship: enabling constraint for storage, sale, and endgame value.
current_initial_bound: not_established; shed snapshots are observable, but each unexplained delta cannot be attributed to sale, use, transfer, or loss.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: reconcile every shed delta with executed transfer, consumption, production, sale, and loss events.
confounders: concurrent worker actions, market execution, feed use, contract expiry, and snapshot timing.
validation_requirement: validate conservation on independent episodes before using shed persistence as a feature.
falsification_condition: reconciled events show no unexplained integrity loss in the modeled regime.
change_from_e15_spec: REVISED
change_rationale: the frozen partial fidelity proxy becomes an explicit conservation requirement.
```

```text
concept_id: contract_inventory_loss
feature_status: UNRESOLVED
e15_relationship: negative constraint when expiring worker inventory is not transferred; ontology reports engine-rule support, E15 incidence is unmeasured.
current_initial_bound: not_established; worker inventories and hands are observable, but expiry-linked loss events are not labelled.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: record inventory immediately before and after each contract expiry with transfer/loss reason.
confounders: manual deposit, consumption, rehire identity, simultaneous sale, and worker indexing.
validation_requirement: independently verify loss conservation and economic impact after any handling rule is trained.
falsification_condition: engine/replay reconciliation shows inventory persists or is automatically transferred at expiry.
change_from_e15_spec: ADDED
change_rationale: the frozen CODEX model omitted an engine-supported risk relevant to inventory-to-cash conversion.
```

```text
concept_id: endgame_shutdown_timing
feature_status: FEATURE
e15_relationship: interaction with remaining crop/product-to-cash horizon.
current_initial_bound: not_established; no attributed initiation-to-cash cycles support a specific cutoff.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: stop new cycles at 0.5, 1.0, and 1.5 measured product-to-cash cycles remaining.
confounders: crop/product type, existing backlog, liquidation capacity, price, and contract expiry.
validation_requirement: validate the trained cutoff on unseen episodes with terminal cash and unsold inventory both reported.
falsification_condition: shutdown timing does not affect completed cycles, terminal inventory, or cash under controlled mix.
change_from_e15_spec: UNCHANGED
change_rationale: the frozen subsystem remains valid in form, but E15 provides no day optimum.
```

```text
concept_id: endgame_inventory_liquidation
feature_status: FEATURE
e15_relationship: positive when executed before episode end without excessive price impact or order pressure.
current_initial_bound: not_established; SELL requests and terminal inventories do not prove accepted liquidation.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: candidate sell cadences of 1, 4, and 8 orders per decision, subject to verified market limits and identical available quantity.
confounders: batch limit, quantity per order, price elasticity, rejected orders, and product mix.
validation_requirement: validate the trained cadence on unseen market paths using executed sellthrough and terminal inventory.
falsification_condition: cadence changes neither executed liquidation nor realized terminal value.
change_from_e15_spec: UNCHANGED
change_rationale: E15 leaves the frozen liquidation hypothesis plausible but entirely execution-dependent.
```

### G. Field condition and recovery

```text
concept_id: field_cleanliness_state
feature_status: NOT_FEATURE
e15_relationship: not a standalone economic driver in the modeled regime; remains a conditioning state for productive-surface recovery.
current_initial_bound: no autonomous bound; cleanliness must be reported separately on productive and fallow tiles.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: no autonomous target values; observe it only as a covariate for backlog, activation, and routing tests.
confounders: productive versus unused tiles, crop opportunity cost, expansion, and routing.
validation_requirement: independently confirm that autonomous cleanup adds no value after productive backlog is controlled.
falsification_condition: controlled cleanup of otherwise equivalent productive surfaces produces a repeatable net-cash gain not captured by weed backlog cost.
change_from_e15_spec: DEPRIORITIZED
change_rationale: retains the frozen deprecation and removes cleanliness itself from the next training feature space, without ignoring weeds on productive land.
```

```text
concept_id: weed_backlog_cost
feature_status: FEATURE
e15_relationship: negative when weeds block productive activation or consume scarce recovery capacity; otherwise near zero.
current_initial_bound: not_established; weed snapshots are derivable, but no opportunity-cost or recovery ledger exists.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure backlog separately on productive-target and fallow tiles, plus actions and monetized cycles displaced.
confounders: land total, crop plan, route distance, spare capacity, and autonomous cleanliness policy.
validation_requirement: validate a preregistered opportunity-cost formula on unseen recovery episodes.
falsification_condition: productive-tile weed backlog has no effect on activation, service, or cash after workload is controlled.
change_from_e15_spec: UNCHANGED
change_rationale: the economic backlog, unlike cleanliness itself, remains a plausible conditional feature.
```

### H. Constraints, diagnostics, and outcome

```text
concept_id: market_order_batch_limit
feature_status: FEATURE
e15_relationship: structural constraint on order application and scheduling; ontology records engine-rule support.
current_initial_bound: engine value not re-estimated by E15; requests are observable, but accepted/applied slots and overflow handling are not labelled.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: verify the engine limit and record requested, accepted, rejected, deferred, and unused slots per decision.
confounders: order type, bundling, simultaneous player orders, and submission formatting.
validation_requirement: independently confirm the limit and its application semantics before validating any batching rule.
falsification_condition: engine inspection or reconciled execution shows no such limit or different semantics.
change_from_e15_spec: ADDED
change_rationale: the frozen CODEX model omitted an engine-supported constraint needed to interpret HIRE and liquidation requests.
```

```text
concept_id: action_order_slot_pressure
feature_status: UNRESOLVED
e15_relationship: negative when demanded valid orders exceed applicable slots, conditional on prioritization.
current_initial_bound: not_established; E15 counts emitted orders but not accepted slots, displaced orders, or their value.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure demand-to-capacity ratios 0.5, 0.8, 1.0, and 1.2 after the relevant limits are verified.
confounders: market versus worker slots, order priority, invalid orders, and batch semantics.
validation_requirement: validate the pressure metric and economic loss on independent overloaded episodes.
falsification_condition: excess requested demand causes no displacement or value loss under verified engine semantics.
change_from_e15_spec: REVISED
change_rationale: the frozen partial proxy cannot be interpreted without accepted-order observability.
```

```text
concept_id: state_capacity_alignment
feature_status: UNRESOLVED
e15_relationship: plausible high-order interaction among land, maintained crop/pasture surface, herd, workforce, feed, routing, and cash.
current_initial_bound: no scalar bound; the 2Q/25-37 crop/5-9 pasture/4-7 animal/9-10 hand bundle outperforms the 3Q/8-9 crop/18 pasture/18 animal/12 hand bundle, but components are inseparable.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: preregister component metrics and compare no composite, equal-weight composite, and bottleneck-minimum composite without final-money inputs.
confounders: all component features, arbitrary weights, target leakage, and correlated policy bundles.
validation_requirement: validate any frozen formula on independent episodes after weights and thresholds are trained.
falsification_condition: a composite adds no out-of-sample discrimination beyond separate components or changes sign across seeds.
change_from_e15_spec: REVISED
change_rationale: E15 supports the interaction hypothesis but not the frozen spec's implicit capacity gates as a valid metric.
```

```text
concept_id: local_kaggle_fidelity_gap
feature_status: UNRESOLVED
e15_relationship: diagnostic qualifier, not a local performance feature.
current_initial_bound: not_established; E15 supplies local frozen replays only and therefore no paired local/Kaggle difference.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: measure paired state-transition, action-execution, ranking, and final-money differences on identical submitted builds where feasible.
confounders: seed, opponent, engine version, hidden environment differences, and build identity.
validation_requirement: only independent Kaggle evidence can validate the estimated gap after local training.
falsification_condition: paired executions show equivalent semantics and stable performance within preregistered tolerances.
change_from_e15_spec: REVISED
change_rationale: the frozen concept remains necessary, but E15 cannot supply any value or confidence for it.
```

```text
concept_id: operational_divergence_onset
feature_status: FEATURE
e15_relationship: diagnostic timing preceding possible economic divergence; threshold and dimension specific.
current_initial_bound: not_established; replay trajectories permit derivation, but E15 did not preregister a divergence dimension or threshold.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure first persistent divergence in serviced surface, herd/pasture ratio, executed action failure, and cash using 1-, 3-, and 6-step persistence windows.
confounders: normal policy differences, transient purchases, scale normalization, and post-hoc threshold selection.
validation_requirement: preregister the dimension/threshold and validate onset stability on independent episodes.
falsification_condition: onset is unstable, purely post-hoc, or does not precede the associated subsystem difference.
change_from_e15_spec: UNCHANGED
change_rationale: the diagnostic survives but cannot be collapsed into a single post-hoc timestamp.
```

```text
concept_id: economic_lock_in_onset
feature_status: FEATURE
e15_relationship: diagnostic timing after operational divergence when an economic gap becomes persistent under a declared recovery criterion.
current_initial_bound: not_established; final gaps are observed, but recovery probability and lock-in threshold are not.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: measure persistence over 3, 6, and 12 steps after a preregistered cash/obligation deficit, with counterfactual recovery checks.
confounders: price shocks, intentional investment, opponent market effects, and hindsight from final money.
validation_requirement: validate the preregistered lock-in rule prospectively on independent episodes.
falsification_condition: purported lock-in states frequently recover or do not predict persistent economic disadvantage out of sample.
change_from_e15_spec: UNCHANGED
change_rationale: the frozen distinction from operational onset remains useful but wholly provisional.
```

```text
concept_id: final_money_outcome
feature_status: NOT_FEATURE
e15_relationship: terminal target and benchmark outcome, not a causal explanatory input.
current_initial_bound: observed E15 range 8,672-37,752 across different seed/opponent cells; it is not a feature threshold or training optimum.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: none; retain as primary outcome with net-flow, terminal inventory, and subsystem diagnostics beside it.
confounders: seed, opponent, shared market, starting state, unliquidated inventory, and all policy components.
validation_requirement: assess trained candidates on fully independent held-out episodes; E15 cannot be reused as validation.
falsification_condition: not applicable as a feature; revise outcome use if engine scoring differs from terminal money.
change_from_e15_spec: REVISED
change_rationale: preserves final money as the target while explicitly removing it from the explanatory feature space.
```

## 4. Feature interaction map

```text
interaction_id: I01_irrigation_service_x_crop_working_set
features: watering_execution_rate, watering_continuity, crop_care_completion_rate, crop_surface_maintained
reason: crop scale creates value only when daily care capacity services it continuously.
current_evidence: empirically supported as a bundled discrimination; 8-9 crops and 0.082-0.144 service proxy co-occur in two low outcomes, while 25-37 and 0.711-0.752 co-occur elsewhere; the independent effects are not isolated.
confounding_risk: workforce, dispatch, crop mix, horizon, pasture, and action execution.
training_implication: vary service fraction and working-set cap independently, include middle values, and retain per-crop longitudinal denominators.
```

```text
interaction_id: I02_crop_surface_x_pasture_x_herd
features: crop_surface_maintained, pasture_surface_maintained, livestock_headcount, pasture_arable_surface_tradeoff, livestock_capacity
reason: land and care capacity are jointly allocated between crop and livestock subsystems.
current_evidence: empirically supported only at bundle level; 18 pasture/18 animals/8-9 crops differs from 5-9 pasture/4-7 animals/25-37 crops.
confounding_risk: owned land, feed, workforce, species, market conversion, and policy implementation.
training_implication: separate herd and pasture effects at fixed land/service before estimating an interaction or capacity ratio.
```

```text
interaction_id: I03_workload_x_workforce_x_dispatch
features: workforce_headcount, worker_capacity_available, action_dispatch_failure, routing_completion_efficiency, necessary_transit_fraction
reason: additional hands monetize only if tasks exist, routes complete, and dispatches have useful effects.
current_evidence: plausible and weakly supported; 12-hand runs have about 5,000 MOVE requests and high HARVEST/PLANT ratios, while 9-10-hand runs have about 3,760 MOVE and lower ratios, but the policy bundles differ.
confounding_risk: land topology, active surface, animal workload, contract schedule, and action semantics.
training_implication: hold working set fixed while varying hands, then classify movement and action effects rather than relying on counts.
```

```text
interaction_id: I04_land_purchase_x_activation_x_cash
features: land_purchase_timing, activated_land_surface, land_activation_payback, operating_cash_buffer, deployable_capital_window
reason: expansion is beneficial only if purchased capacity activates and returns cash before obligations or horizon bind.
current_evidence: plausible, not isolated; the observed 3Q bundle has low cash minima and low crop activation, but land, herd, and policy differ simultaneously.
confounding_risk: initial crop engine, workforce, pasture, price, acquisition day, and attribution method.
training_implication: condition purchase candidates on preregistered activation readiness and record purchase-to-activation-to-payback events.
```

```text
interaction_id: I05_inventory_x_market_x_reinvestment
features: inventory_to_cash_conversion, market_transaction_value, market_sellthrough_lag, reinvestment_cash_flow, operating_cash_buffer
reason: produced inventory matters economically only through executed sale value and timely reuse of proceeds.
current_evidence: model-plausible but unobserved; SELL requests and cash trajectories co-vary grossly, yet execution and attribution are absent.
confounding_risk: order rejection, price, initial inventory, mixed cash sources, and terminal holdings.
training_implication: establish transaction and cash-flow ledgers before assigning values or tuning cadence.
```

```text
interaction_id: I06_wheat_feed_market_loop
features: wheat_operating_flow, feed_availability, feed_security_buffer, feed_market_dependency, market_churn_cost
reason: Wheat can be seed, crop output, feed, bought inventory, sold inventory, or cash source, so isolated order volume is uninterpretable.
current_evidence: plausible and specifically unresolved; every match winner requests more BUY_PRODUCT Wheat, contradicting a simple dependency-is-bad reading without proving benefit.
confounding_risk: execution, resale, herd demand, crop output, dynamic price, and shared market.
training_implication: conserve role-tagged Wheat units and vary sourcing only after feed demand and market execution are observable.
```

```text
interaction_id: I07_horizon_x_mix_x_endgame
features: crop_horizon_alignment, crop_revenue_mix, endgame_shutdown_timing, endgame_inventory_liquidation, market_sellthrough_lag
reason: late production has value only if its full care, harvest, and sale cycle fits the remaining horizon.
current_evidence: frozen-model hypothesis only; E15 lacks cycle-to-cash attribution and accepted liquidation timing.
confounding_risk: product cycle length, price, terminal inventory valuation, worker contracts, and order limits.
training_implication: express cutoffs in measured cycles remaining, not frozen days, after the ledger exists.
```

```text
interaction_id: I08_state_capacity_composite
features: state_capacity_alignment plus land, crop, pasture, livestock, workforce, feed, routing, and cash components
reason: the replicated policy fingerprints suggest bottleneck alignment may explain more than any raw magnitude.
current_evidence: plausible high-order hypothesis, not a supported metric; only two strongly separated bundles are observed.
confounding_risk: arbitrary weights, collinearity, target leakage, sparse cells, and overfitting E15.
training_implication: preregister component formulas first and compare a bottleneck composite against separate terms; do not freeze weights from E15.
```

## 5. Observability requirements

| Requirement | What E15 already makes observable | What remains required | Decision |
|---|---|---|---|
| Requested vs executed actions | Requested Farmer/hand actions, positions, tile states, and next snapshots | Per-actor applied action, effect delta, success flag, and standardized failure reason | **Required.** Some effects can be inferred, but concurrency and snapshot timing prevent complete attribution. |
| Requested vs executed market transactions | Requested order type, commodity, quantity; displayed market price/inventory; cash and private inventory snapshots | Accepted/rejected/partial status, executed quantity, realized unit price, value, and application step | **Required.** Do not use requests as trades. |
| Quantity and realized price | Requested quantities and public displayed prices are available | Executed quantity and transaction-specific realized price with provenance (`observed`, `reconstructed`, or `base_price_estimate`) | **Required.** Current displayed price is not automatically the fill price. |
| Action success/failure reason | Requested type/target and many before/after states are available | Exact reason such as invalid target, no yield, no inventory capacity, unreachable, duplicate reservation, or engine rejection | **Required.** Needed for `action_dispatch_failure`. |
| Daily maintained/serviced surface | Active crop/pasture tile states and `watered_today` support the declared EOD proxy | Daily need denominator, successful service by care type, persistence/loss, productive-versus-fallow classification, crop/pasture breakdown | **Required extension.** Active and watered surface are not wholly missing, but formal maintenance is. |
| Cash-flow breakdown | Per-step total cash trajectory is available | Executed inflows/outflows by sale, buy, hire, land, animal, wage, feed, seed, and other obligation, reconciled to total cash | **Required.** Total cash alone cannot establish payback or reinvestment. |
| Necessary movement vs overhead | Positions and requested MOVE directions are available | Target/task linkage, route start/end, completion window, transport role, and avoidable-loop label | **Required derivation plus audit.** Raw movement is already observable; necessity is not. |
| Purchase-to-activation/payback lag | Land-unlock state transitions, tile states, cash, and purchase requests are available | Verified purchase application, acquisition/activation costs, first serviced production, executed sale proceeds, and attributed recovery timestamp | **Required.** Transition time is partially derivable; payback attribution is missing. |
| Contract and shed inventory integrity | Hands, worker inventories, and shed snapshots are available | Contract identity/expiry event, transfers, consumption, production, sale, and explicit loss reason | **Required** before inventory conservation claims. |

The minimum acceptable future record is an event ledger keyed by episode, player, step, actor/order, requested payload, executed payload, effect/reason, quantity, realized price/value, cash-flow category, state before/after, and provenance. Derived formulas must be preregistered and must not include final money as an input.

## 6. Candidate training priorities

```text
priority: 1
concept_or_interaction: action and market execution observability foundation
information_gap: requested actions/orders cannot be reconciled to executed effects, quantities, prices, values, or failure reasons.
why_it_matters: almost every economic and efficiency conclusion otherwise risks measuring intent rather than environment response.
candidate_values_or_measurement: event ledger with requested/executed payload, effect, failure reason, transaction quantity/price/value, and reconciled cash/inventory delta.
expected_information_gain: very high; unlocks valid measurement of dispatch, monetization, conversion, feed cost, churn, payback, and endgame.
```

```text
priority: 2
concept_or_interaction: I01_irrigation_service_x_crop_working_set
information_gap: the transition between serviced fractions 0.144 and 0.711 and crop proxies 9 and 25 is unobserved.
why_it_matters: this is the strongest replicated E15 discrimination and may define a failure floor without implying an optimum.
candidate_values_or_measurement: serviced fractions 0.15, 0.30, 0.45, 0.60, 0.72 and crop caps 9, 13, 17, 21, 25, varied independently in the later common design.
expected_information_gain: very high; separates service threshold, surface threshold, and interaction.
```

```text
priority: 3
concept_or_interaction: I02_crop_surface_x_pasture_x_herd
information_gap: E15 observes only compact and large livestock/land bundles, with no 7-17 herd or 9-18 pasture transition.
why_it_matters: the bundle can consume land, workforce, feed, and cash while appearing productive by asset count.
candidate_values_or_measurement: herd 4, 7, 10, 13, 17 and pasture 5, 9, 13, 18, with species and net product-flow accounting.
expected_information_gain: high; separates animal scale, pasture opportunity cost, and capacity alignment.
```

```text
priority: 4
concept_or_interaction: I03_workload_x_workforce_x_dispatch
information_gap: 9-12 hands are observed, but useful capacity, necessary transit, failed dispatches, and marginal payback are not.
why_it_matters: workforce is a major recurring cost and raw headcount does not explain M2.
candidate_values_or_measurement: 9, 10, 11, 12 hands at fixed workload, with route-completion, action-effect, contract, and net marginal-cash metrics.
expected_information_gain: high; can distinguish capacity shortage from coordination and routing overhead.
```

```text
priority: 5
concept_or_interaction: I05_inventory_x_market_x_reinvestment
information_gap: no executed sellthrough, product revenue, availability-to-sale lag, or tagged reuse of proceeds.
why_it_matters: the frozen CODEX thesis ranks conversion and reinvestment near the top, but E15 cannot test them.
candidate_values_or_measurement: conversion and reinvestment measured over 1-, 3-, and 7-day windows, with terminal quantity/value and product breakdown.
expected_information_gain: high after priority 1; confirms or revises the central capital-to-cash chain.
```

```text
priority: 6
concept_or_interaction: I04_land_purchase_x_activation_x_cash
information_gap: 2Q versus 3Q is fully bundled and purchase-to-activation/payback lag is not attributed.
why_it_matters: expansion can create either productive capacity or irreversible capital/workload lock-in.
candidate_values_or_measurement: 2Q and 3Q candidates gated at no, partial, and full prior-surface readiness, with cash floor 25, 50, 87, 150 as separate candidate measurements.
expected_information_gain: medium-high; distinguishes land effect from activation and liquidity effects.
```

```text
priority: 7
concept_or_interaction: I06_wheat_feed_market_loop
information_gap: requested Wheat purchases cannot be assigned to feed, resale, seed, holding, or failed execution.
why_it_matters: every E15 winner requests more Wheat product volume, directly challenging a simplistic dependency penalty.
candidate_values_or_measurement: role-tagged unit conservation and executed external-feed shares 0.25, 0.50, 0.75 at fixed herd/feed demand.
expected_information_gain: medium-high; resolves feed security versus market churn and cash cost.
```

```text
priority: 8
concept_or_interaction: I07_horizon_x_mix_x_endgame
information_gap: no measured crop/product-to-cash cycle or executed liquidation lag supports frozen day cutoffs.
why_it_matters: late activity can inflate productive counts while leaving terminal inventory or incomplete cycles.
candidate_values_or_measurement: shutdown at 0.5, 1.0, 1.5 cycles remaining and liquidation cadence 1, 4, 8 orders only after order-limit verification.
expected_information_gain: medium; converts calendar constants into horizon-relative candidates.
```

These are ordered uncertainties and candidate measurements only. They intentionally do not specify seeds, opponents, cell counts, evaluation protocol, or a complete E16 experiment.

## 7. Changeset from frozen E15 MODEL_SPEC

| Concept | E15 status/hypothesis | Revised status | Change | Evidence basis | Remaining uncertainty |
|---|---|---|---|---|---|
| `land_surface_total` | USED/PARTIAL, payback-conditional | UNRESOLVED | REVISED | 2Q/3Q primary bundles | isolated land effect |
| `land_purchase_timing` | USED/FULL | FEATURE | UNCHANGED | frozen thesis; replay unlock times | causal readiness gate |
| `activated_land_surface` | USED/FULL | FEATURE | UNCHANGED | crop/pasture snapshots | formal activation formula |
| `crop_surface_maintained` | USED/FULL | FEATURE | UNCHANGED | 8-9 vs 25-37 proxy | transition and optimum |
| `pasture_surface_maintained` | PARTIAL/PARTIAL | FEATURE | REVISED | 5/9/18 pasture bundles | independent pasture value |
| `maintained_productive_surface` | USED/FULL | FEATURE | UNCHANGED | bundle decomposition | aggregation formula |
| `monetized_productive_output` | USED/FULL | FEATURE | UNCHANGED | methodological chain | executed product value |
| `land_activation_payback` | USED/FULL | FEATURE | UNCHANGED | frozen hypothesis only | attribution and lag |
| `pasture_arable_surface_tradeoff` | PARTIAL/PARTIAL | FEATURE | REVISED | primary bundle contrast | separate main effects |
| `workforce_headcount` | USED/PARTIAL | UNRESOLVED | REVISED | 9-12 hands; M2 tie | marginal causal effect |
| `worker_capacity_available` | USED/FULL | FEATURE | UNCHANGED | canonical separation | usable-capacity formula |
| `hire_order_scheduling` | PARTIAL/PARTIAL | FEATURE | REVISED | implementation/calendar gap | executed contracts and timing |
| `marginal_hire_payback` | USED/FULL | FEATURE | UNCHANGED | frozen economic framing | counterfactual attribution |
| `productive_action_share` | USED/FULL | UNRESOLVED | REVISED | M2 non-monotonic proxy | taxonomy and execution |
| `movement_overhead` | USED/FULL | FEATURE | UNCHANGED | 3,761-5,047 MOVE requests | necessary fraction |
| `necessary_transit_fraction` | NOT_USED/ABSENT | FEATURE | ADDED | interpretive requirement | attribution window |
| `routing_completion_efficiency` | USED/FULL | FEATURE | UNCHANGED | positions/action traces | completion metric |
| `action_dispatch_failure` | PARTIAL/PARTIAL | FEATURE | REVISED | HARVEST/PLANT gap | exact action effects |
| `worker_action_monetization_rate` | USED/FULL | FEATURE | UNCHANGED | frozen top factor | realized numerator/denominator |
| `crop_care_action_flow` | PARTIAL/BROADER | FEATURE | REVISED | separated request flows | executed completion |
| `planting_action_flow` | PARTIAL/BROADER | FEATURE | REVISED | 93-126 PLANT requests | plant-to-cash conversion |
| `watering_execution_rate` | PARTIAL/BROADER | FEATURE | REVISED | 0.082-0.752 service proxy | middle region and execution |
| `watering_continuity` | PARTIAL/BROADER | FEATURE | REVISED | 2/24 vs 23-24/28 days | causal continuity effect |
| `crop_harvest_action_flow` | PARTIAL/BROADER | FEATURE | REVISED | request-ratio separation | successful yield units |
| `crop_care_completion_rate` | PARTIAL/BROADER | FEATURE | REVISED | maintenance discrimination | need denominator |
| `crop_decay_risk_window` | NOT_USED/ABSENT | UNRESOLVED | ADDED | continuity evidence; ontology | verified engine threshold |
| `crop_horizon_alignment` | USED/FULL | FEATURE | UNCHANGED | frozen hypothesis | cycle-to-cash lag |
| `crop_revenue_mix` | USED/FULL | UNRESOLVED | REVISED | missing executed revenue | product margins |
| `feed_availability` | USED/FULL | FEATURE | UNCHANGED | replay inventory states | demand coverage |
| `feed_security_buffer` | PARTIAL/PARTIAL | FEATURE | REVISED | frozen reserves; no bound | days-of-feed threshold |
| `feed_market_dependency` | USED/PARTIAL | UNRESOLVED | REVISED | winners request more Wheat | execution/use/resale |
| `feed_market_expenditure` | PARTIAL/PARTIAL | UNRESOLVED | REVISED | requests not costs | executed spend |
| `wheat_operating_flow` | USED/FULL | FEATURE | UNCHANGED | role ambiguity in E15 | conserved role flow |
| `market_churn_cost` | PARTIAL/PARTIAL | UNRESOLVED | REVISED | missing lot ledger | matched-cycle cost |
| `livestock_headcount` | USED/PARTIAL | FEATURE | REVISED | 4-7 vs 17-18 bundles | 7-17 transition/species |
| `livestock_capacity` | PARTIAL/PARTIAL | FEATURE | REVISED | bundle interaction | capacity formula |
| `pasture_capacity_alignment` | PARTIAL/PARTIAL | FEATURE | REVISED | 5/4, 9/7, 18/18 | economic ratio |
| `livestock_product_flow` | USED/FULL | FEATURE | UNCHANGED | model chain; animal states | executed product flow |
| `species_margin_differential` | PARTIAL/PARTIAL | UNRESOLVED | REVISED | no isolated margin | Cow/Sheep net return |
| `fertilizer_byproduct_flow` | USED/FULL | UNRESOLVED | REVISED | 15 requests in low runs | generated/sold units |
| `market_transaction_value` | NOT_USED/ABSENT | UNRESOLVED | ADDED | request/execution gap | fill value/provenance |
| `operating_cash_buffer` | USED/PARTIAL | FEATURE | REVISED | minima 19-331; M2 reversal | obligation-relative floor |
| `deployable_capital_window` | USED/FULL | FEATURE | UNCHANGED | frozen thesis | obligation formula |
| `asset_liquidity_lag` | PARTIAL/PARTIAL | UNRESOLVED | REVISED | missing attribution | asset-specific lag |
| `inventory_to_cash_conversion` | USED/FULL | UNRESOLVED | REVISED | SELL requests only | executed sellthrough |
| `market_sellthrough_lag` | USED/PARTIAL | UNRESOLVED | REVISED | accepted-sale time missing | price/lag tradeoff |
| `unsold_inventory_value` | PARTIAL/PARTIAL | UNRESOLVED | REVISED | quantities estimable | valuation convention |
| `reinvestment_cash_flow` | USED/PARTIAL | UNRESOLVED | REVISED | total cash only | source/use attribution |
| `product_mix_revenue` | USED/FULL | UNRESOLVED | REVISED | revenue ledger missing | net mix margins |
| `price_realization_variance` | NOT_USED/ABSENT | UNRESOLVED | ADDED | displayed versus fill gap | price reference |
| `dynamic_market_price_elasticity` | NOT_USED/ABSENT | UNRESOLVED | ADDED | volume/price ambiguity | engine response |
| `shed_inventory_integrity` | PARTIAL/PARTIAL | UNRESOLVED | REVISED | snapshot deltas | event conservation |
| `contract_inventory_loss` | NOT_USED/ABSENT | UNRESOLVED | ADDED | ontology engine support | E15 incidence |
| `endgame_shutdown_timing` | USED/FULL | FEATURE | UNCHANGED | frozen subsystem | cycle-relative cutoff |
| `endgame_inventory_liquidation` | USED/FULL | FEATURE | UNCHANGED | SELL/terminal ambiguity | executed cadence |
| `field_cleanliness_state` | USED/PARTIAL, deprecated objective | NOT_FEATURE | DEPRIORITIZED | frozen deprecation | conditional productive effect |
| `weed_backlog_cost` | USED/PARTIAL | FEATURE | UNCHANGED | productive opportunity-cost thesis | formula |
| `market_order_batch_limit` | NOT_USED/ABSENT | FEATURE | ADDED | ontology engine support | application semantics |
| `action_order_slot_pressure` | PARTIAL/PARTIAL | UNRESOLVED | REVISED | emitted orders only | accepted/displaced slots |
| `state_capacity_alignment` | USED/PARTIAL | UNRESOLVED | REVISED | separated E15 bundles | formula/weights/causality |
| `local_kaggle_fidelity_gap` | USED/FULL | UNRESOLVED | REVISED | local E15 only | paired Kaggle evidence |
| `operational_divergence_onset` | USED/PARTIAL | FEATURE | UNCHANGED | replay trajectories | preregistered threshold |
| `economic_lock_in_onset` | USED/FULL | FEATURE | UNCHANGED | terminal gaps only | recovery criterion |
| `final_money_outcome` | USED/FULL outcome | NOT_FEATURE | REVISED | methodological separation | independent validation distribution |

## 8. Epistemic audit

### RETAIN

- Retain the capital -> activation -> maintenance -> executed output -> executed sale -> reinvestable cash chain as the CODEX model's organizing hypothesis.
- Retain irrigation service, maintained crop surface, pasture/crop allocation, conditional herd scale, dispatch/routing, operating cash, horizon, and endgame as candidate features or interactions.
- Retain final money as the primary outcome, accompanied by component diagnostics and terminal inventory reporting.
- Retain the strict separations owned vs productive land, headcount vs capacity, inventory vs revenue, movement vs waste, and local result vs Kaggle validity.

### REVISE

- Revise all raw-count interpretations to conditional, thresholded, non-monotonic, or unresolved relationships.
- Revise `productive_action_share` from the self-check's unsupported `NOT_FEATURE` to `UNRESOLVED`; require execution-aware and value-aware variants.
- Revise frozen revenue, expenditure, conversion, payback, and product-flow claims to depend on an executed event ledger.
- Revise CODEX policy-realization claims: X1.15 D realized stable crop care and a moderate 2Q bundle, not fully elastic capacity/payback control.

### DEPRIORITIZE_OR_REMOVE

- Remove `field_cleanliness_state` as an autonomous training feature; retain weed effects only through productive backlog and recovery cost.
- Remove `final_money_outcome` from the explanatory feature space while retaining it as the target.
- Continue to reject fixed herd constants, fixed quadrant targets, and raw peak workforce as model propositions; they are policy settings, not canonical causal features.

### UNRESOLVED

- Independent causal effects and transition regions for land, workforce, herd, pasture, watering, crop surface, and cash buffer.
- Executed market value, sellthrough, reinvestment, product mix, Wheat use, feed expenditure, churn, and species/byproduct margins.
- Necessary transit, exact dispatch failure, worker contract loss, market order application, state-capacity formula, operational lock-in thresholds, and local/Kaggle gap.
- Generalization across common seeds/opponents and all validation claims.

### DO_NOT_FREEZE_YET

- Do not freeze any candidate numerical value, interval, threshold, interaction weight, composite formula, or feature ordering in this document.
- Do not freeze the EOD watering proxy as the canonical maintenance metric.
- Do not freeze any transaction or revenue estimate derived from requested orders or displayed pre-action prices.
- Do not freeze an E16 configuration from these priorities; they are inputs to a later common design process.
- Do not reuse E15 for validation or test. All future validation must be independent of the evidence used here for feature selection and initial bounding.

This file is a candidate MODEL_SPEC revision and remains open to common review, training evidence, and later independent validation.
