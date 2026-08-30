# POST-E15 — ANTIGRAVITY MODEL_SPEC REVISION (Candidate)

**Modeler:** `ANTIGRAVITY`  
**Date:** 2026-08-29  
**Basis:** E15 frozen MODEL_SPEC (`MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md`), E15 primary evidence, POST-E15 capability check  
**Status:** `CANDIDATE_REVISION` — not frozen, not the next-round MODEL_SPEC  
**Provenance Discipline:** [E15-FROZEN], [E15-PRI], [CAP-CHECK], [MY-INF]

> Victory ≠ Model Validity.  
> Defeat ≠ Model Falsification.

---

## A. Baseline Reconstruction

### A.1 E15 Frozen MODEL_SPEC Principles

**[E15-FROZEN]** The Antigravity MODEL_SPEC E14.6 was organized around these core pillars:

1. **Three-Quadrant Territory (Q0→Q1→Q2, 75 tiles):** Capital-protected sequential expansion.
2. **Staggered Workforce Ramp:** Scaling to 12 active hands via multi-hour hiring.
3. **Internal Feed Autarky:** Clustered crop rotation prioritizing internal wheat feed.
4. **On-Demand Pasture Architecture:** Pastures constructed strictly when animals are owned.
5. **High-Velocity Cash Crop & Byproduct Monetization:** Daily watering + shed liquidation.

The spec ranked `irrigation_dispatch_priority` as Rank #1 (Critical/High) and `feed_autarky_pipeline` as Rank #2 (Critical/High). It declared a target of 18 animals (14 Cow, 4 Sheep) and 12 hands, operating over 3 quadrants.

### A.2 E15 Observed Behavior

**[E15-PRI]** The Antigravity submission produced a highly reproducible behavioral fingerprint across two matches (M1 vs Codex, M3 vs Copilot):

| Metric | M1 | M3 |
|---|---:|---:|
| WATER | 34 | 30 |
| HARVEST | 414 | 374 |
| FEED | 309 | 315 |
| MOVE | 5,019 | 5,047 |
| max hands | 12 | 12 |
| max pasture | 18 | 18 |
| max animals | 18 | 18 |
| max active crops | 8 | 9 |
| FINAL_MONEY | $8,672 | $9,371 |

### A.3 Model → Policy → Implementation Divergence

**[E15-PRI + CAP-CHECK]**

The central finding is a **severe MODEL-to-POLICY/IMPLEMENTATION fracture**:

| MODEL_SPEC Declaration | Realized Behavior | Status |
|---|---|---|
| `irrigation_dispatch_priority` = Rank #1 Critical | 34/30 WATER in 720 steps | **STRONGLY_WEAKENED** |
| Cash-crop rotation (Strawberry/Melon) | Zero Strawberry/Melon SELL orders | **STRONGLY_WEAKENED** |
| Feed autarky = Rank #2 Critical | Massive BUY_PRODUCT Wheat (1,007 M1; 904 M3) | **STRONGLY_WEAKENED** |
| Capital-protected expansion | Cash drops to $81 (M1 Day19), $73 (M3 Day18) | **STRONGLY_WEAKENED** |
| Target 55 active crops | Max 8–9 active crops | **STRONGLY_WEAKENED** |
| On-demand pasture (=animals) | 18 pasture / 18 animals → crowds out crop surface | **PARTIALLY_REALIZED but counterproductive** |
| Endgame wheat liquidation | Present but insufficient to overcome structural deficit | **WEAKLY_REALIZED** |

### A.4 Layer Summary

| Layer | Verdict | Rationale |
|---|---|---|
| **MODEL_VALIDITY** | `PARTIALLY_SUPPORTED` | Core concepts (watering priority, maintained surface, monetization) are directionally correct — the *winners* do what the MODEL_SPEC *says* Antigravity should do. |
| **POLICY_REALIZATION** | `STRONGLY_WEAKENED` | The submission systematically violates its own spec's priorities. |
| **IMPLEMENTATION_FIDELITY** | `STRONGLY_WEAKENED` | HARVEST/PLANT ratio of 4.45/3.74 signals dispatch pathology; 5,000+ MOVE signals routing inefficiency. |

> **[MY-INF]** The E15 Antigravity MODEL_SPEC is not falsified at the concept level. It is untested by its own implementation. The revision must therefore focus on (1) correcting the concepts that E15 *does* weaken, and (2) acknowledging which concepts remain UNRESOLVED because the implementation prevented meaningful evaluation.

---

## B. Concept-by-Concept Revision

### B.1 Terrain & Productive Surface

```text
concept_id: land_surface_total
feature_status: FEATURE
e15_relationship: non_monotonic — 3Q (75 tiles) lost to 2Q (50 tiles) in both Antigravity matches; however, 3Q has never been tested with adequate watering/dispatch. Land is a necessary but not sufficient enabler.
current_initial_bound: 2Q (50 tiles) is sufficient for competitive outcomes. 3Q (75 tiles) is UNRESOLVED as net-positive or net-negative when execution quality is controlled.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: Test 2Q and 3Q with matched watering/dispatch quality.
confounders: Confounded with dispatch/watering quality, cash pressure, and livestock scale. Antigravity's 3Q failure cannot be attributed to Q-count alone.
validation_requirement: A 3Q agent with WATER ≥ 400 and active_crops ≥ 25 must be observed to determine whether 3Q is viable.
falsification_condition: If a 3Q agent with strong execution produces FINAL_MONEY ≥ $25k, land_surface_total remains a useful enabler. If 3Q consistently underperforms 2Q with matched parameters, it should be demoted.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC assumed 3Q was Critical/High. E15 evidence shows 3Q was associated with failure, but causality is confounded. Demoted from unquestioned pillar to testable hypothesis.
```

```text
concept_id: land_purchase_timing
feature_status: FEATURE
e15_relationship: conditional — early land purchase is not sufficient without activation capacity.
current_initial_bound: Q1 purchase observed between Day 9 (Antigravity) and Day 11 (Codex/Copilot). Earlier is not demonstrably better.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: Test Q1 at Day 9 vs Day 11 with cash-gating conditions.
confounders: Co-varies with cash buffer and workforce readiness.
validation_requirement: Observe FINAL_MONEY sensitivity to Q1 timing with other parameters controlled.
falsification_condition: If Day 11 Q1 consistently matches or beats Day 9 Q1, early purchase adds no value.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC used dynamic triggers (Day 5+ at $1k); Q2 trigger (Day 8+ at $2k) resulted in premature expansion. Timing gates need to be more conservative.
```

```text
concept_id: activated_land_surface
feature_status: FEATURE
e15_relationship: positive — higher activation ratio (active crops / owned surface) is associated with better outcomes.
current_initial_bound: Winners showed ≥ 50% activation; Antigravity showed < 15% activation (8-9 crops on 75 tiles).
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Not directly controllable; depends on watering, dispatch, and crop management.
confounders: Activation is a consequence of multiple upstream features, not independently tunable.
validation_requirement: Track daily activation ratio as a diagnostic metric.
falsification_condition: If high activation with poor monetization produces low FINAL_MONEY, activation alone is insufficient.
change_from_e15_spec: UNCHANGED
change_rationale: E15 MODEL_SPEC correctly identified activation ≠ ownership. E15 evidence strongly supports this distinction.
```

```text
concept_id: crop_surface_maintained
feature_status: FEATURE
e15_relationship: thresholded — below ~10 active crops, strong failure signal. Above ~25, non-monotonic (37 lost to 28 in M2).
current_initial_bound: failure_region ≤ 9; competitive_region [25, 37]; E15 does not resolve optimum within competitive region.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: 15, 20, 25, 30, 35
confounders: Crop surface co-varies with watering, workforce, and monetization quality.
validation_requirement: Multi-seed test of crop surface with matched watering.
falsification_condition: If 15 active crops with strong monetization matches 30 crops, then surface above minimum is not a driver.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC targeted 55 active crops. E15 evidence shows 28 is sufficient to win and 37 did not beat 28. Target drastically revised downward.
```

```text
concept_id: pasture_surface_maintained
feature_status: FEATURE
e15_relationship: conditional — must be proportionate to actual herd size. Excessive pasture crowds out arable surface.
current_initial_bound: Copilot competitive at 5 pasture; Antigravity failed at 18 pasture. Codex intermediate at 9.
parameter_or_hyperparameter: PARAMETER (directly linked to livestock_headcount)
next_training_values: 4, 5, 7, 9
confounders: Inseparable from livestock_headcount and crop surface tradeoff.
validation_requirement: Test pasture at matched livestock levels to isolate spatial tradeoff.
falsification_condition: If pasture = 9 with 7 animals and strong crop management outperforms pasture = 5 with 4 animals, then compact pasture is not inherently superior.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC used on-demand 1:1 pasture:animal gating. The principle is sound, but the target of 18 animals means 18 pastures, which is excessive. Revise target animal count downward.
```

```text
concept_id: maintained_productive_surface
feature_status: FEATURE
e15_relationship: positive — maintained (not merely owned) surface discriminates all three matches.
current_initial_bound: not_established as a numeric target. Qualitative: maintained crop surface >> nominal capacity as predictor.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Track daily maintained surface (watered fraction, active crops, functional pasture).
confounders: Composite of watering, dispatch, crop management.
validation_requirement: Daily telemetry of maintained vs total surface.
falsification_condition: If high maintained surface with poor monetization fails, maintenance is necessary but not sufficient.
change_from_e15_spec: UNCHANGED
change_rationale: Correctly formulated in E15 spec; strongly supported by E15 evidence.
```

```text
concept_id: monetized_productive_output
feature_status: FEATURE
e15_relationship: positive — FINAL_MONEY correlates with monetized output across all matches.
current_initial_bound: not_established as absolute value. Copilot achieved $37.8k from compact working set; Codex $27.5k from larger set.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Requires executed transaction ledger to decompose.
confounders: Outcome metric, not independently tunable.
validation_requirement: Executed revenue ledger by product category.
falsification_condition: Not applicable — this is the target, not a causal feature.
change_from_e15_spec: UNCHANGED
change_rationale: Correctly formulated.
```

```text
concept_id: land_activation_payback
feature_status: FEATURE
e15_relationship: negative (in Antigravity context) — Q2 expansion consumed capital without producing proportional return.
current_initial_bound: not_established. Antigravity's Q2 payback was negative. Copilot/Codex Q1 payback appears positive.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Track capital invested in land expansion vs incremental revenue attributable to new surface.
confounders: Payback depends entirely on activation quality, not on land per se.
validation_requirement: Measure revenue before/after Q1/Q2 expansion with matched other variables.
falsification_condition: If Q2 with strong execution shows positive payback, the concept is validated but the E15 MODEL_SPEC's gating was too permissive.
change_from_e15_spec: REVISED
change_rationale: E15 spec expected Q2 payback to be positive. E15 evidence shows it was negative due to implementation failure. Revise the gating conditions, not the concept.
```

```text
concept_id: pasture_arable_surface_tradeoff
feature_status: FEATURE
e15_relationship: conditional — 18 pasture on 75 tiles (24% of surface) leaves insufficient crop surface. 5 pasture on 50 tiles (10%) is competitive.
current_initial_bound: pasture / total_tiles ≤ ~15% appears safe. 24% was associated with failure.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: Test pasture fractions at 8%, 12%, 18% of total surface.
confounders: Entangled with livestock_headcount and total land.
validation_requirement: Isolate pasture fraction from livestock revenue contribution.
falsification_condition: If pasture = 18% with strong crop management and smaller herd succeeds, the tradeoff is less binding.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC acknowledged the tradeoff but the 18-animal target forced 18 pastures. Revise animal target downward to reduce tradeoff pressure.
```

### B.2 Workforce, Dispatch & Logistics

```text
concept_id: workforce_headcount
feature_status: FEATURE
e15_relationship: non_monotonic — 12 hands lost to 9-10 hands. More workers are not better when dispatch is poor.
current_initial_bound: competitive_region [9, 12]. Failure observed at 12 with poor dispatch. Success at 9-10 with good dispatch.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: 8, 9, 10, 12
confounders: Workforce interacts with dispatch quality, quadrant count, and routing efficiency.
validation_requirement: Test workforce at matched dispatch quality.
falsification_condition: If 12 hands with strong dispatch outperforms 9, then workforce_headcount matters above threshold.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC targeted 12 hands as a key architectural element. E15 evidence shows 9-10 is competitive and 12 may cause movement overhead. Revise default target downward.
```

```text
concept_id: worker_capacity_available
feature_status: FEATURE
e15_relationship: positive — more capacity is useful only if converted to productive output.
current_initial_bound: not_established independently.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Not directly controllable; derived from workforce_headcount.
confounders: Capacity is a necessary but not sufficient condition.
validation_requirement: Track worker utilization rate.
falsification_condition: If low capacity (8 hands) with perfect utilization outperforms high capacity (12 hands) with poor utilization, capacity is secondary to utilization.
change_from_e15_spec: UNCHANGED
change_rationale: Correctly formulated but emphasis must shift from capacity to utilization.
```

```text
concept_id: hire_order_scheduling
feature_status: FEATURE
e15_relationship: unresolved — E15 does not discriminate scheduling strategies directly. All agents successfully hired workers.
current_initial_bound: not_established.
parameter_or_hyperparameter: PARAMETER
next_training_values: No change proposed; staggered hiring remains sound.
confounders: None directly observed.
validation_requirement: None specific.
falsification_condition: If single-turn hiring reliably produces the same headcount, staggering is unnecessary complexity.
change_from_e15_spec: UNCHANGED
change_rationale: Staggered hiring across H0+H1 remains theoretically sound and was not the source of E15 failure.
```

```text
concept_id: productive_action_share
feature_status: FEATURE
e15_relationship: thresholded — raw productive action share is NOT a strong discriminant (Codex had higher share than Copilot in M2 and lost). Quality of action matters more than share.
current_initial_bound: not_established as useful threshold.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Not directly controllable.
confounders: Productive_action_share conflates efficient and inefficient productive actions (e.g., failed HARVEST counts as productive).
validation_requirement: Decompose into successful vs failed actions.
falsification_condition: Already partially weakened by M2.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC targeted >42% productive share. E15 evidence shows this is insufficient as a driver — action monetization quality matters more than share.
```

```text
concept_id: movement_overhead
feature_status: UNRESOLVED
e15_relationship: conditional — absolute MOVE is higher in Antigravity (5,000+) but MOVE-share (~71%) is similar across all agents.
current_initial_bound: not_established.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Not directly controllable; depends on layout and routing.
confounders: Absolute MOVE is confounded with quadrant count and dispatch patterns.
validation_requirement: Separate necessary movement from overhead movement.
falsification_condition: If a 3Q agent achieves < 4,000 MOVE, excessive movement is a routing issue, not a Q-count issue.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC attributed 63% movement overhead to worker locality. E15 tournament shows ~71% MOVE-share across all agents, suggesting movement is inherent, not pathological per se. The issue is absolute volume tied to spatial expansion.
```

```text
concept_id: action_dispatch_failure
feature_status: FEATURE
e15_relationship: negative — HARVEST/PLANT ratio > 3 is a replicated signature of dispatch pathology in Antigravity. Winners show ~1.0 ratio.
current_initial_bound: failure_region: ratio > 3.0. competitive_region: ratio [0.7, 1.1].
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: Requires action success/failure logging.
confounders: High ratio may reflect crop death from insufficient watering rather than pure dispatch failure.
validation_requirement: Per-action success/failure data.
falsification_condition: If ratio > 3 is confirmed to be "successful harvests from different tiles in sequence," the dispatch failure interpretation is falsified.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC identified dispatch loop traps as a known risk. E15 evidence confirms this at a much larger scale than anticipated — the entire submission exhibits this pattern systematically.
```

```text
concept_id: worker_action_monetization_rate
feature_status: FEATURE
e15_relationship: positive — higher $/action proxy is consistently associated with winning.
current_initial_bound: Copilot ~$7.1/action; Codex ~$5.2/action; Antigravity ~$1.3/action (estimated).
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Requires executed transaction ledger for decomposition.
confounders: Composite outcome, not independently tunable.
validation_requirement: Revenue per action category.
falsification_condition: If an agent with low $/action wins through terminal asset liquidation, flow monetization is not sufficient.
change_from_e15_spec: UNCHANGED
change_rationale: Correctly identified in E15 spec. E15 evidence strongly supports it.
```

```text
concept_id: watering_execution_rate
feature_status: FEATURE
e15_relationship: thresholded — below ~30-34 total WATER, catastrophic failure. Above ~440, competitive but not monotonically better (Codex 475 lost to Copilot 446 in M2).
current_initial_bound: minimum_viable > 34 (failure bound). Competitive at ~440-475. No observations in [35, 438].
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: 100, 200, 300, 400, 450
confounders: Watering co-varies with crop surface, dispatch quality, and workforce allocation.
validation_requirement: Multi-value test to locate the elbow in the response curve.
falsification_condition: If WATER ~200 produces competitive results, the minimum threshold is much lower than 440.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC declared watering as Rank #1 Critical/High and targeted >1,000 WATER. The submission realized 30-34. The priority was correct but the implementation failed completely. The revised spec must ENFORCE this priority, not merely declare it. The >1,000 target from replay benchmarks may not apply to the current environment version.
```

```text
concept_id: watering_continuity
feature_status: FEATURE
e15_relationship: thresholded — Antigravity watered in only ~5 days out of 30. Winners watered continuously.
current_initial_bound: failure_region: watering in < 10 days. success_region: watering in > 25 days.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: Enforce daily watering as a constraint, not a target.
confounders: Continuity is a consequence of dispatch priority.
validation_requirement: Track days with WATER > 0.
falsification_condition: If intermittent but intense watering (e.g., every other day, high volume) matches continuous, then continuity is less important than volume.
change_from_e15_spec: UNCHANGED
change_rationale: Correctly identified. The failure is implementation, not model.
```

### B.3 Crop Production

```text
concept_id: crop_revenue_mix
feature_status: FEATURE
e15_relationship: positive — presence of cash-crop SELL orders (Strawberry/Melon) is associated with winning. Antigravity had zero cash-crop sales.
current_initial_bound: at_least_some cash-crop sales appear necessary. Observed: winners sell 30-58 units of Strawberry/Melon.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: Test crop mixes with 0%, 30%, 60% cash-crop allocation.
confounders: Cash-crop sales presuppose adequate watering and crop management.
validation_requirement: Revenue decomposition by product type.
falsification_condition: If a wheat-only agent with strong monetization achieves competitive FINAL_MONEY, cash-crop presence is not necessary.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC declared cash-crop rotation as Rank #5 High/High. The submission failed to produce any cash-crop sales. The model concept is supported by E15 evidence (winners do sell cash crops), but the implementation must actually execute this.
```

```text
concept_id: crop_horizon_alignment
feature_status: FEATURE
e15_relationship: unresolved — E15 does not provide sufficient granularity to assess planting/harvesting timing.
current_initial_bound: not_established from E15.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: No change from E15 spec (stop planting Melon/Strawberry by Day 26).
confounders: None directly observed.
validation_requirement: Track un-harvested mature crops at game end.
falsification_condition: If planting cash crops until Day 28 with fast harvest still captures revenue, Day 26 cutoff is too conservative.
change_from_e15_spec: UNCHANGED
change_rationale: Reasonable principle, not directly tested in E15.
```

### B.4 Feed, Wheat & Livestock

```text
concept_id: feed_market_dependency
feature_status: UNRESOLVED
e15_relationship: unresolved — Copilot uses MORE BUY_PRODUCT Wheat (1,828/1,889) than anyone and wins. Market dependency is not inherently negative.
current_initial_bound: not_established. E15 evidence contradicts the "autarky is critical" thesis.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: Requires executed transaction ledger to assess net cost of market wheat.
confounders: Wheat BUY_PRODUCT may serve as a cash-flow management tool (buy/resell) rather than feed expenditure.
validation_requirement: Decompose wheat purchases into feed-consumed vs resold.
falsification_condition: If high market wheat dependency with positive net wheat P/L is observed, then dependency is not a cost center.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC declared feed autarky as Rank #2 Critical/High. E15 evidence shows the tournament winner uses the most market wheat. This does not prove autarky is wrong (Copilot may use wheat differently), but it fundamentally weakens the "dependency = catastrophic drain" thesis as stated. Deprioritize autarky-as-absolute; reframe as "feed cost management."
```

```text
concept_id: livestock_headcount
feature_status: FEATURE
e15_relationship: non_monotonic — 18 animals associated with failure; 4 associated with winning; 7 intermediate.
current_initial_bound: failure_region ≥ 17. competitive_region [4, 7]. Interval [8, 16] unobserved.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: 0, 4, 7, 10, 14
confounders: Confounded with pasture allocation, cash pressure, feed cost, and workforce allocation.
validation_requirement: Multi-value test with matched watering and crop surface.
falsification_condition: If 10 animals with adequate support produces competitive results, the E15 4-animal observation is not a ceiling.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC targeted 14 Cow + 4 Sheep = 18. E15 evidence shows 18 is in the failure region. Drastically revised downward to [4, 7] initial search range.
```

```text
concept_id: species_margin_differential
feature_status: UNRESOLVED
e15_relationship: unresolved — no clean Cow vs Sheep comparison in E15. Copilot used only Cow; Antigravity used 13 Cow + 4 Sheep.
current_initial_bound: not_established.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: Requires controlled Cow-only vs mixed herd experiment.
confounders: Species mix is confounded with total herd size and other strategy differences.
validation_requirement: Factorial test of species mix × herd size.
falsification_condition: If Wool ($200) consistently generates more margin per feed unit than Milk ($160), sheep scaling is justified.
change_from_e15_spec: DEPRIORITIZED
change_rationale: E15 MODEL_SPEC prioritized sheep scaling (Rank #7 High/Medium). E15 evidence provides no support for this — the winner uses zero sheep. Deprioritize until controlled evidence is available.
```

```text
concept_id: fertilizer_byproduct_flow
feature_status: UNRESOLVED
e15_relationship: weakened — Antigravity collected Fertilizer (15 units); Codex collected 0-1; Copilot collected 0-2. The winner does not use Fertilizer.
current_initial_bound: not_established as a competitive advantage.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: None — deprioritize.
confounders: Fertilizer collection competes for worker turns.
validation_requirement: Observe marginal revenue from Fertilizer vs opportunity cost.
falsification_condition: If Fertilizer collection with high worker efficiency produces net-positive returns, it can be reinstated.
change_from_e15_spec: DEPRIORITIZED
change_rationale: E15 MODEL_SPEC ranked Fertilizer monetization as Rank #8 High/High based on replay benchmarks. E15 tournament evidence shows winners ignore Fertilizer. The replay benchmarks may be from a different environment version or opponent landscape.
```

```text
concept_id: wheat_operating_flow
feature_status: UNRESOLVED
e15_relationship: unresolved — both winners show intense wheat buy/sell flow, but profitability cannot be determined without executed transaction ledger.
current_initial_bound: not_established.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: Requires transaction ledger.
confounders: Wheat flow may be profitable arbitrage, neutral cash management, or a cost center.
validation_requirement: Executed transaction price and quantity data.
falsification_condition: If wheat churn is confirmed to have positive P/L, it becomes a strategic feature.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC treated wheat as primarily a feed resource (autarky pipeline). E15 evidence shows winners treat wheat as a major trading commodity. The model must accommodate wheat-as-operating-flow, not only wheat-as-feed.
```

### B.5 Capital, Market & Reinvestment

```text
concept_id: operating_cash_buffer
feature_status: FEATURE
e15_relationship: non_monotonic — too little cash causes operational stalls, but higher early cash is NOT monotonically better (Copilot operated with lower cash than Codex in M2 Days 4-9 and won).
current_initial_bound: failure_region: cash approaching $0 during mid-game expansion. Success does not require the highest buffer.
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: Test minimum buffer thresholds ($100, $300, $500) as gating conditions for expansion.
confounders: Cash depletion co-occurs with investment decisions.
validation_requirement: Compare conservative (high buffer) vs aggressive (low buffer) strategies with matched other parameters.
falsification_condition: If aggressive investment to near-zero cash with strong execution produces high FINAL_MONEY, high buffer is not needed.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC used $1k-$2k as expansion gates. E15 evidence shows these gates may have been both too permissive (allowing Q2 expansion without readiness) and too rigid (a lower buffer may be adequate with better execution). Reframe as dynamic condition, not fixed threshold.
```

```text
concept_id: deployable_capital_window
feature_status: FEATURE
e15_relationship: positive — timing of capital deployment relative to operational readiness is associated with outcome.
current_initial_bound: not_established numerically. Qualitative: deploy capital only when operational capacity can absorb it.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Track capital deployment timing vs activation lag.
confounders: Capital deployment co-occurs with multiple decisions.
validation_requirement: Measure time-to-activation after each major investment.
falsification_condition: If immediate capital deployment with fast activation succeeds, timing is less important than activation speed.
change_from_e15_spec: UNCHANGED
change_rationale: Correctly formulated; strongly supported by E15 evidence.
```

```text
concept_id: inventory_to_cash_conversion
feature_status: FEATURE
e15_relationship: positive — higher SELL order volume associated with higher FINAL_MONEY.
current_initial_bound: Antigravity 198 SELL orders; Copilot 298-302. These are REQUESTED orders.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Requires executed transaction ledger.
confounders: More SELL orders may reflect more production or more churn.
validation_requirement: Executed SELL quantities and revenues.
falsification_condition: If an agent with fewer but higher-value SELL orders matches Copilot, volume is less important than value.
change_from_e15_spec: UNCHANGED
change_rationale: Correctly formulated.
```

```text
concept_id: state_capacity_alignment
feature_status: FEATURE
e15_relationship: positive — the most consistently discriminating concept across all three E15 matches. Compact, well-aligned working sets outperform large, poorly-aligned ones.
current_initial_bound: not_established as a numeric metric. Qualitative: active_crops / (pasture + hands + animals) appears predictive.
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: Define and track an alignment metric. Cannot be directly tuned — emerges from component decisions.
confounders: Composite concept; discriminative power may be because it captures joint effects.
validation_requirement: Formalize the alignment metric and track across experiments.
falsification_condition: If a deliberately mis-aligned agent (large capacity, low activation) compensates through a different mechanism, alignment is not necessary.
change_from_e15_spec: REVISED
change_rationale: E15 MODEL_SPEC treated this as PARTIAL, using modular gating rules. E15 evidence shows it is the strongest discriminant in the tournament. Promote to a primary organizing principle.
```

### B.6 Endgame & Diagnostics

```text
concept_id: endgame_inventory_liquidation
feature_status: FEATURE
e15_relationship: unresolved — both winners and losers reach zero crops at end. Causal contribution to FINAL_MONEY not isolable.
current_initial_bound: not_established independently.
parameter_or_hyperparameter: PARAMETER
next_training_values: No change — retain Day 28+ liquidation.
confounders: Endgame effect is small relative to accumulated advantage.
validation_requirement: Track revenue from liquidation specifically.
falsification_condition: If agents without liquidation achieve similar FINAL_MONEY, the effect is negligible.
change_from_e15_spec: UNCHANGED
change_rationale: Sound principle, minor contributor.
```

```text
concept_id: field_cleanliness_state
feature_status: NOT_FEATURE (as competitive driver)
e15_relationship: negative — cleaner fields are NOT associated with winning. Codex won M1 with 22 weeds; Antigravity lost with 5 weeds.
current_initial_bound: not applicable — cleanliness does not predict outcome.
parameter_or_hyperparameter: NOT_YET_TUNABLE
next_training_values: None.
confounders: Clean fields may simply reflect unused land.
validation_requirement: None.
falsification_condition: If a dedicated weed-clearing agent outperforms, reassess.
change_from_e15_spec: UNCHANGED
change_rationale: E15 MODEL_SPEC already deprecated field cleanliness. E15 evidence confirms this.
```

```text
concept_id: local_kaggle_fidelity_gap
feature_status: UNRESOLVED
e15_relationship: unresolved — E15 was run locally only. No local-vs-Kaggle comparison available.
current_initial_bound: not_established.
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: Requires Kaggle submission and comparison.
confounders: N/A.
validation_requirement: Submit and compare.
falsification_condition: If local and Kaggle scores converge, the gap is resolved.
change_from_e15_spec: UNCHANGED
change_rationale: Separate workstream (Problem B) correctly identified.
```

---

## C. Feature Interaction Map

```text
interaction_id: WATERING_DISPATCH_LIVESTOCK_CASH
features: watering_execution_rate, action_dispatch_failure, livestock_headcount, operating_cash_buffer, crop_surface_maintained
reason: These features form a tightly coupled system. Large livestock → high FEED/CARE demand → fewer worker-turns for WATER → low crop surface → low revenue → cash pressure → premature expansion. This is the primary failure mode observed in Antigravity E15.
current_evidence: [E15-PRI] Replicated in M1 and M3 — Antigravity shows this exact cascade.
confounding_risk: HIGH — cannot separate individual feature contributions without controlled experiments.
training_implication: The first training experiment must fix livestock at a low level (e.g., 4) and test watering independently. Only after watering threshold is established should livestock be varied.
```

```text
interaction_id: WORKING_SET_COMPACTNESS
features: crop_surface_maintained, pasture_arable_surface_tradeoff, workforce_headcount, state_capacity_alignment
reason: Copilot's compact working set (25-28 crops, 5 pasture, 4 animals, 9 hands) outperforms larger configurations. The interaction suggests that LESS can be MORE when components are well-aligned.
current_evidence: [E15-PRI] M2 — Copilot 28 crops beats Codex 37 crops. M3 — Copilot 25 crops beats Antigravity 9 crops. But Antigravity's 9 crops fails for many reasons beyond size.
confounding_risk: MEDIUM — cannot determine whether compactness itself is the cause or whether it merely enables better maintenance.
training_implication: Test a "compact well-maintained" vs "large well-maintained" working set to separate size from quality.
```

```text
interaction_id: MARKET_WHEAT_FLOW_ECONOMICS
features: wheat_operating_flow, feed_market_dependency, market_churn_cost, inventory_to_cash_conversion
reason: Winners show intense wheat buy/sell activity (~1,800 units) alongside high SELL order volume. Without an executed transaction ledger, we cannot determine whether this flow is net profitable, neutral (cash-flow management), or a cost.
current_evidence: [E15-PRI] Copilot: 1,828-1,889 BUY_PRODUCT Wheat; 1,767-1,831 SELL Wheat (requested). [CAP-CHECK] These are request counts, not executed.
confounding_risk: HIGH — the entire wheat-flow hypothesis is confounded by lack of price/execution data.
training_implication: BLOCK — do not adjust wheat strategy until executed transaction ledger is available.
```

```text
interaction_id: CASH_DEPLOYMENT_TIMING
features: deployable_capital_window, land_activation_payback, operating_cash_buffer, asset_liquidity_lag
reason: Antigravity deployed capital into Q2 expansion, workforce, and livestock before the existing capacity could monetize. The cash trajectory shows spikes to near-zero coinciding with expansion events.
current_evidence: [E15-PRI] M1 Day 19: cash hits $81 after Q2 + herd expansion. M3 Day 18: cash hits $73 at same expansion point.
confounding_risk: MEDIUM — cannot separate "deployed too early" from "deployed into wrong things."
training_implication: Tighten expansion gating: require demonstrated activation of existing capacity before deploying capital into new capacity.
```

---

## D. Observability Requirements

| Observability | Currently Available? | Necessity | Rationale |
|---|---|---|---|
| Requested vs executed market orders | **NO** — only requests logged | **CRITICAL** | Cannot assess market strategy, wheat P/L, or revenue decomposition. |
| Executed transaction price & quantity | **NO** | **CRITICAL** | Cannot determine revenue per product, margins, or churn cost. |
| Action success/failure reason | **NO** — only action counts | **HIGH** | Cannot decompose HARVEST/PLANT ratio into failed vs successful. |
| Daily maintained/serviced crop surface | **NO** — only max observed | **HIGH** | Cannot track activation trajectory. |
| Daily watered crop fraction | **NO** | **HIGH** | Cannot characterize watering adequacy. |
| Cash-flow breakdown (revenue by source, expenditure by category) | **NO** | **HIGH** | Cannot assess which revenue streams drive FINAL_MONEY. |
| Movement: necessary transit vs overhead | **NO** — only total MOVE | **MEDIUM** | Cannot separate useful movement from waste. |
| Purchase-to-activation lag | **NO** | **MEDIUM** | Cannot measure how quickly investments produce returns. |
| Worker utilization rate | **NO** | **MEDIUM** | Cannot assess workforce efficiency. |

> [!IMPORTANT]
> The **executed transaction ledger** is the single most critical new observability for the next round. Without it, all market-related features (wheat_operating_flow, feed_market_dependency, market_churn_cost, crop_revenue_mix profitability) remain UNRESOLVED.

---

## E. Candidate Training Priorities

```text
priority: 1
concept_or_interaction: WATERING_DISPATCH_LIVESTOCK_CASH (interaction cluster)
information_gap: No observations between WATER = 34 and WATER = 439. No observations between livestock = 4 and livestock = 7 with matched watering.
why_it_matters: This interaction cluster explains the primary Antigravity failure mode and is the widest information gap in E15. Narrowing the watering threshold alone would collapse uncertainty on 3+ related features.
candidate_values_or_measurement: Fix livestock = 4, quadrants = 2, workforce = 9. Test WATER targets: 100, 200, 300, 400. Measure FINAL_MONEY, active_crops/day, HARVEST/PLANT ratio.
expected_information_gain: HIGH — locating the watering elbow would resolve the most important single question from E15.
```

```text
priority: 2
concept_or_interaction: livestock_headcount (direct feature)
information_gap: Only 3 values observed (4, 7, 17-18). Range [8-16] entirely unobserved.
why_it_matters: Livestock interacts with pasture, cash, feed, and workforce. Setting the right herd size determines the entire subsystem balance.
candidate_values_or_measurement: Fix watering = high (~440), quadrants = 2. Test max_animals: 0, 4, 7, 10, 14. Measure FINAL_MONEY, feed expenditure, pasture allocation, crop surface.
expected_information_gain: HIGH — would determine whether the competitive range is [4, 7] or extends higher.
```

```text
priority: 3
concept_or_interaction: crop_surface_maintained (as interaction with state_capacity_alignment)
information_gap: 37 crops lost to 28; 8-9 crops clearly failed. What is the minimum viable crop surface?
why_it_matters: Resolves whether compact working set wins because of size or because of maintenance quality.
candidate_values_or_measurement: Fix watering = high, livestock = 4. Test target max_active_crops: 15, 20, 25, 30, 35. Measure FINAL_MONEY, maintenance quality metrics.
expected_information_gain: MEDIUM — would map the crop-surface response curve and clarify M2's paradox.
```

```text
priority: 4
concept_or_interaction: executed transaction ledger (observability)
information_gap: Zero executed transaction data in E15.
why_it_matters: Blocks resolution of wheat_operating_flow, feed_market_dependency, market_churn_cost, crop_revenue_mix profitability. Without this, ~5 features remain permanently UNRESOLVED.
candidate_values_or_measurement: Add telemetry: executed_quantity, executed_price, product_type, direction (BUY/SELL) for every market order.
expected_information_gain: HIGH — unlocks analysis of all market-related features.
```

```text
priority: 5
concept_or_interaction: land_surface_total (3Q vs 2Q)
information_gap: 3Q has only been tested with the worst implementation in the tournament. It may be viable with adequate execution.
why_it_matters: If 3Q is viable, it opens a larger search space for crop surface and revenue. If it is inherently worse, the model can be simplified.
candidate_values_or_measurement: Test 2Q vs 3Q with matched watering (~440), livestock (4), and workforce (9). Measure FINAL_MONEY, crop surface, movement overhead.
expected_information_gain: MEDIUM — resolves a central architectural question for Antigravity.
```

---

## F. Changeset Relative to E15 MODEL_SPEC

| Concept | E15 Status/Hypothesis | Revised Status | Change | Evidence Basis | Remaining Uncertainty |
|---|---|---|---|---|---|
| `territory_scale_3q` | Critical/High, 3Q as pillar | FEATURE, 3Q UNRESOLVED | REVISED | 3Q lost both matches; confounded with implementation | 3Q viability with adequate execution |
| `watering_execution_rate` | Rank #1, Critical/High, >1000 target | FEATURE, thresholded, target TBD | REVISED | 34/30 WATER → catastrophic failure | Minimum threshold location [35-438] |
| `feed_autarky_pipeline` | Rank #2, Critical/High | UNRESOLVED, deprioritized | REVISED | Winner uses most market wheat | Wheat flow economics |
| `workforce_ramp_multi_hour` | Rank #4, Critical/High, 12 hands | FEATURE, target revised to [9-10] | REVISED | 12 hands lost; 9-10 competitive | 12 viable with better dispatch? |
| `cash_crop_rotation` | Rank #5, High/High | FEATURE, implementation failed | UNCHANGED (concept) | Zero cash-crop sales despite spec | Implementation must execute |
| `on_demand_pasture_gating` | Rank #6, High/High | FEATURE, target revised | REVISED | 18 pasture is excessive | Optimal pasture at lower herd |
| `herd_specialization_sheep_cow` | Rank #7, High/Medium | UNRESOLVED | DEPRIORITIZED | Winner uses zero sheep | Species margin data absent |
| `byproduct_monetization_fert` | Rank #8, High/High | UNRESOLVED | DEPRIORITIZED | Winner ignores Fertilizer | Marginal ROI unknown |
| `livestock_headcount` | 14 Cow + 4 Sheep = 18 | FEATURE, range [4, 7] | REVISED | 18 = failure region | Optimal within [4-10] |
| `productive_action_share` | Target >42% | FEATURE, weakened as driver | REVISED | Codex higher share, lost M2 | Quality > share |
| `state_capacity_alignment` | PARTIAL mapping | FEATURE, promoted to primary | REVISED | Best discriminant in E15 | Formalization needed |
| `crop_surface_maintained` | 55 active crops target | FEATURE, target [20-30] | REVISED | 28 beats 37; 8-9 fails | Response curve shape |
| `field_cleanliness_state` | Deprecated/Low | NOT_FEATURE confirmed | UNCHANGED | Winner has more weeds | — |
| `movement_overhead` | 63% as problem | UNRESOLVED | REVISED | ~71% MOVE-share for all agents | Inherent vs reducible |

---

## G. Epistemic Audit

### RETAIN

Concepts that remain in the model with the same or strengthened status:

1. **`watering_execution_rate`** — Rank #1 priority confirmed by E15 evidence. Implementation must enforce it.
2. **`state_capacity_alignment`** — Promoted from PARTIAL to primary organizing principle.
3. **`maintained_productive_surface`** — Correctly formulated; strongly supported.
4. **`deployable_capital_window`** — Correctly formulated; consistent with E15 cash trajectory evidence.
5. **`activated_land_surface`** — Correctly formulated; ownership ≠ activation remains a key separation.
6. **`inventory_to_cash_conversion`** — Directionally supported by SELL order data.
7. **`worker_action_monetization_rate`** — Consistently discriminating proxy metric.
8. **`crop_revenue_mix`** — Cash-crop presence associated with winning.
9. **`hire_order_scheduling`** — Not contradicted; retains operational value.
10. **`endgame_inventory_liquidation`** — Sound minor principle.

### REVISE

Concepts requiring significant update to initial bounds, relationship, or priority:

1. **`livestock_headcount`** — From target 18 → initial search range [4, 7].
2. **`crop_surface_maintained`** — From target 55 → initial search range [20, 30].
3. **`workforce_headcount`** — From target 12 → initial search range [9, 10].
4. **`territory_scale_3q` / `land_surface_total`** — From 3Q as pillar → 2Q as default, 3Q as hypothesis.
5. **`feed_market_dependency`** — From "catastrophic drain" → UNRESOLVED (winner uses most market wheat).
6. **`operating_cash_buffer`** — From fixed $1k-$2k gates → dynamic gating tied to activation readiness.
7. **`action_dispatch_failure`** — From known risk → confirmed primary failure mode requiring architectural fix.
8. **`productive_action_share`** — From target >42% → demoted; quality > share.
9. **`pasture_arable_surface_tradeoff`** — Target revised via lower livestock.
10. **`wheat_operating_flow`** — From feed resource → multi-role operating commodity.

### DEPRIORITIZE_OR_REMOVE

1. **`herd_specialization_sheep_cow`** — No E15 evidence for sheep advantage. DEPRIORITIZE.
2. **`byproduct_monetization_fert`** — Winners ignore Fertilizer. DEPRIORITIZE.
3. **`field_cleanliness_state`** — Confirmed NOT_FEATURE. RETAIN as deprecated.
4. **`necessary_transit_fraction`** — NOT_USED in E15 spec; no new evidence. DEPRIORITIZE.

### UNRESOLVED

1. **`wheat_operating_flow`** — Profitability unknown without transaction ledger.
2. **`market_churn_cost`** — Cannot be assessed.
3. **`species_margin_differential`** — No clean comparison.
4. **`feed_market_dependency`** — Winner uses most market wheat; direction reversed from spec hypothesis.
5. **`movement_overhead`** — ~71% MOVE-share for all agents; may be inherent.
6. **`land_surface_total` (3Q viability)** — Never tested with adequate execution.
7. **`price_realization_variance`** — No price data.
8. **`local_kaggle_fidelity_gap`** — Not tested in E15.
9. **`fertilizer_byproduct_flow`** — Marginal ROI unknown.
10. **`crop_decay_risk_window`** — Engine mechanics not verified.

### DO_NOT_FREEZE_YET

The following should not be frozen as parameters until controlled evidence is obtained:

1. **Any specific numeric target for livestock, workforce, or crop surface.** E15 provides initial bounds, not optima. The next round must narrow these ranges through controlled experiments before freezing values.
2. **Any claim about wheat flow profitability.** The executed transaction ledger is a prerequisite.
3. **Any judgment on 3Q viability.** The only 3Q test was with the worst-performing implementation.
4. **The watering threshold.** The [34, 439] interval must be narrowed before a target can be set.
5. **State-capacity alignment as a formal metric.** The concept is strongly supported but has no formalized computation. Define and validate the metric before freezing.

---

## Source Provenance

| Source | Path | Role |
|---|---|---|
| E15 Frozen MODEL_SPEC | [MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md) | E15 FROZEN MODEL DECLARATION |
| E15 Frozen Ontology | [ONTOLOGY_E15_FROZEN.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/freeze/ONTOLOGY_E15_FROZEN.md) | METHODOLOGICAL FRAME |
| E15 Tournament Synthesis | [E15_FINAL_TOURNAMENT_SYNTHESIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/E15_FINAL_TOURNAMENT_SYNTHESIS.md) | POST-E15 INTERPRETATION |
| M1 Telemetry | [telemetry.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/M1_antigravity_vs_codex/telemetry.json) | PRIMARY E15 EVIDENCE |
| M2 Telemetry | [telemetry.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/M2_codex_vs_copilot/telemetry.json) | PRIMARY E15 EVIDENCE |
| M3 Telemetry | [telemetry.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/M3_copilot_vs_antigravity/telemetry.json) | PRIMARY E15 EVIDENCE |
| M1 Forensic Analysis | [E15_M1_NEUTRAL_FORENSIC_ANALYSIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/M1_antigravity_vs_codex/E15_M1_NEUTRAL_FORENSIC_ANALYSIS.md) | PRIMARY E15 EVIDENCE |
| M2 Forensic Analysis | [E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/M2_codex_vs_copilot/E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md) | PRIMARY E15 EVIDENCE |
| M3 Forensic Analysis | [E15_M3_NEUTRAL_FORENSIC_ANALYSIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e15/M3_copilot_vs_antigravity/E15_M3_NEUTRAL_FORENSIC_ANALYSIS.md) | PRIMARY E15 EVIDENCE |
| Capability Check | [ANTIGRAVITY_CAPABILITY_CHECK.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/post_e15/capability_check/ANTIGRAVITY_CAPABILITY_CHECK.md) | POST-E15 SELF CAPABILITY CHECK |
| README.md | [README.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/README.md) | METHODOLOGICAL FRAME |
