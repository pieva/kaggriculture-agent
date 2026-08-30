# Copilot Independent Parametric Strategy Model (E14)

## 1. Scope and isolation boundary

This specification defines the Copilot workstream only. It is intentionally separate from the Antigravity and Codex archives and is anchored to the existing Copilot implementation path that uses the shared Kaggriculture environment and the common `ProductiveMassROIAgent` engine, but with a Copilot-specific policy envelope and a dedicated bundle.

### Shared infrastructure intentionally retained
- `src/agricola/core/state.py`
- `src/agricola/core/actions.py`
- generic evaluation and harness code
- deterministic simulator primitives
- common benchmark JSON and replay corpus under `results/`

### Contaminations or accidental dependencies removed from Copilot scope
- No direct reuse of Antigravity-specific package path (`src/agricola/strategy/antigravity/`)
- No direct reuse of the Codex-specific configuration or build logic
- No use of the shared historical `docs/MODEL_SPEC.md` as the active Copilot source of truth
- No agent-specific overwrite of the other candidates' results or submissions

### Repository hygiene for this phase
- Maintain a Copilot-specific model file at `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT.md`
- Preserve `docs/MODEL_SPEC.md` as a historical artifact only
- Build the final candidate as `submission_copilot.py`

---

## 2. Copilot architecture

### 2.1 Architectural principle
Copilot follows the repository principle of shared infrastructure, isolated intelligence.

The active Copilot model is a low-capacity, state-gated throughput policy built around the existing E12 X1.15 Copilot mode already present in the shared `ProductiveMassROIAgent` engine:

- `productive_core_mode = "E12_X115_COPILOT_INDEPENDENT"`
- state-based animal capacity gating
- conservative early herd expansion
- continued use of the shared economic primitive but with a dedicated Copilot wrapper and dedicated build artifact

### 2.2 Active Copilot policy envelope
The model does not claim that “capacity first” or “Q2 always” are universal truths. Instead, Copilot treats the alignment between working set, cash, pasture capacity, and active crops as the primary driver. The current policy is deliberately conservative and evidence-tethered:

- early game: low herd counts until active crops and cash are established
- when owned quadrants are below two and operating capital is weak, animal expansion stays tightly gated
- once the active crop base and pasture support are in place, the model expands to moderate herd targets
- the active risk is not raw hand count, but throughput-to-capital coherence

---

## 3. Taxonomy changelog

This taxonomy is intentionally open and evidence-based. The following operations were accepted or explicit guardrails for Copilot.

| Parameter / Influence | Operation | Copilot state | Evidence basis |
|---|---|---|---|
| `state_based_capacity_gate` | ADD | Live gate on day, owned quadrants, crop count, and cash | `ProductiveMassROIAgent` Copilot mode uses a conditional animal-capacity envelope |
| `target_cows` | REFORMULATE | Conservative dynamic target, not fixed universal value | Local X1.15 evidence and benchmark replay review show fixed herd sizes are contradicted |
| `target_sheep` | REFORMULATE | Conditional on pasture and active crop readiness | Herd mixes vary across evidence corpus; fixed 7/4 is not stable |
| `throughput_vs_capacity` | ADD | Throughput must match working set and quadrants | Replay review emphasizes physical capacity differs from economic utilization |
| `low_capacity_opening` | RETAIN | Low early herd and crop reliance before cash lock-in | Copilot mode intentionally avoids early over-commitment |
| `fixed_q2_priority` | REMOVE | Q2 is never treated as mandatory in Copilot active policy | Relay benchmark evidence rejects universal Q2-first doctrine |
| `fixed_workforce_count` | REMOVE | Copilot does not hardcode a universal hand total | Evidence matrix contradicts fixed worker counts |

---

## 4. Ranking by expected economic impact

The list below is ordered by economic impact, not by confidence. A parameter can be highly impactful while still being weakly evidenced.

| Rank | Name | Type | Status | Expected impact | Confidence | Evidence status | Mechanism | Validity |
|---:|---|---|---|---|---|---|---|---|
| 1 | `throughput_to_cash_conversion` | interaction | retained | Critical | Medium | SUPPORTED | Revenue quality depends on how quickly active crops and product sales convert into reinvestable cash | REPLAY_SUPPORTED |
| 2 | `working_set_capacity_gate` | policy | added | Critical | Medium | SUPPORTED | Cash, active crops, pasture, and owned quadrants must be synchronized before herd growth | REPLAY_SUPPORTED |
| 3 | `crop_activation_and_monetization` | policy | retained | Critical | Medium | SUPPORTED | Productive tile activation and product sales drive compounding | REPLAY_SUPPORTED |
| 4 | `land_unlock_condition` | policy | reformulated | High | Medium | SUPPORTED | Land expansion is a rewarded branch only when the operating set can support it | REPLAY_SUPPORTED |
| 5 | `pasture_to_livestock_alignment` | interaction | retained | High | Medium | SUPPORTED | Animals need pasture and feed support to convert to revenue rather than drain resources | REPLAY_SUPPORTED |
| 6 | `wheat_feed_security` | constraint | retained | High | Medium | SUPPORTED | Feed bottlenecks can erase throughput gains and cause expensive market purchase dependence | REPLAY_SUPPORTED |
| 7 | `cash_buffer_before_expansion` | constraint | retained | High | Medium | WEAKLY_SUPPORTED | Expansion without liquidity can stall the working set and reduce throughput | LOCAL_ONLY |
| 8 | `milestone_day_gating` | policy | reformulated | Medium | Medium | WEAKLY_SUPPORTED | Day triggers alone are insufficient; state-based conditions matter more | LOCAL_ONLY |
| 9 | `herd_target_sensitivity` | parameter | reformulated | Medium | Low | WEAKLY_SUPPORTED | Optimal cow/sheep mix is seed- and timing-dependent, not fixed | LOCAL_KAGGLE_CONFLICT |
| 10 | `inventory_liquidation_and_shed_flush` | policy | retained | Medium | Medium | SUPPORTED | Bare inventory can erode end-game cash if not monetized or flushed correctly | REPLAY_SUPPORTED |
| 11 | `field_cleanliness_priority` | policy | deprecated | Low | Medium | CONTRADICTED | Over-prioritizing weed cleanup is not a universal profit driver | REPLAY_SUPPORTED |
| 12 | `fixed_hire_count` | parameter | removed | Low | High | FALSIFIED | Hand totals are not universal; they are condition-specific | REPLAY_SUPPORTED |

---

## 5. Evidence backfill

### 5.1 Primary evidence corpus
- `results/benchmark/COPILOT_MODEL_SPEC_CRITICAL_REVIEW_6REPLAY.md`
- `results/benchmark/COPILOT_MODEL_SPEC_EVIDENCE_MATRIX_6REPLAY.csv`
- `results/e12/x115_copilot/FINAL_REPORT.md`
- `scripts/benchmark_e12_x1_15_copilot.py`
- `tests/test_e12_x1_15_copilot.py`

### 5.2 Confirming evidence
- The six-replay review rejects fixed workforce and fixed herd target assumptions.
- Elite high-score replays show Q2 is a real, high-ceiling branch but not a universal target.
- Existing Copilot X1.15 benchmark confirms the mode is state-based and does not mutate shared config.
- The local test ensures the Copilot dispatch stays stable without altering the base config.

---

## 9. Canonical Ontology Mapping (E14.6)

This section maps all 64 canonical concepts from `docs/model/ontology/ONTOLOGY.md` to the Copilot model. The mapping preserves Copilot's independent judgment on ranking, importance, and implementation while enabling semantic interoperability for E15.

| concept_id | usage | mapping | local_term | model_assessment | evidence/confidence reference |
|---|---|---|---|---|---|
| `land_surface_total` | USED | FULL | `territory_scale_3q` (historical) / `land_unlock_condition` (current) | Copilot tracks owned land quadrants as a state variable, not as a policy trigger. Ownership is independent from activation or monetization. | Section 2.1; Section 4, rank 4 |
| `land_purchase_timing` | PARTIAL | PARTIAL | `milestone_day_gating` | Copilot originally used day thresholds but now employs state-based gating. Timing emerges from state alignment, not from fixed calendar. | Section 4, rank 4; Section 6 reformulations |
| `activated_land_surface` | USED | FULL | (none; integrated into `land_unlock_condition`) | Activation is the conversion of owned land into productive use. Copilot distinguishes this from mere ownership. | Section 2.1; Section 4, rank 4 |
| `crop_surface_maintained` | USED | FULL | `crop_activation_and_monetization` | Copilot actively maintains productive crop surface as a state-based commitment, not a fixed target. The surface is part of the working set. | Section 4, rank 3 |
| `pasture_surface_maintained` | USED | FULL | `pasture_to_livestock_alignment` | Copilot maintains pasture in proportion to herd size and feed requirements. Pasture is functional support, not speculative excess. | Section 4, rank 5 |
| `maintained_productive_surface` | USED | FULL | (aggregate metric) | Copilot tracks total maintained surface as a diagnostic; it is computed from crop + pasture components. | Section 4, rank 3 |
| `monetized_productive_output` | USED | FULL | `throughput_to_cash_conversion` | Copilot prioritizes output that is actually sold or convertible to cash, not merely produced. This is a critical ranking factor. | Section 4, rank 1; Section 5.1 |
| `land_activation_payback` | PARTIAL | PARTIAL | (none explicitly; emerges from `land_unlock_condition` logic) | Copilot considers payback implicitly through state-based expansion gating. Expansion occurs only when operating capital and crop base support it. | Section 2.2; Section 4, rank 4 |
| `pasture_arable_surface_tradeoff` | USED | FULL | `pasture_to_livestock_alignment` | Copilot recognizes the finite-surface competition between pasture and crops. Pasture is demand-driven, not maximized speculatively. | Section 2.2; Section 4, rank 5 |
| `workforce_headcount` | USED | FULL | `fixed_hire_count` (removed from active policy) | Copilot no longer assumes a universal hand count. Workforce headcount is variable and depends on throughput demand and cash availability. | Section 3, parameter rank N/A; Section 5.4 |
| `worker_capacity_available` | USED | FULL | (none; integrated into state-based capacity calculation) | Copilot tracks the theoretical available labor hours and matches it against working-set capacity requirements. | Section 4, rank 2 |
| `hire_order_scheduling` | PARTIAL | PARTIAL | (none; handled implicitly in dispatch) | Copilot does not explicitly model order-slot timing within turns, but respects the market-order limit as a constraint. | Section 4, rank 2; constraint implicit |
| `marginal_hire_payback` | NOT_USED | ABSENT | (none) | Copilot does not currently formalize marginal payback of additional workers. It uses threshold-based state gating instead. | Section 3, parameter rank N/A |
| `productive_action_share` | USED | FULL | (efficiency denominator) | Copilot prioritizes the fraction of worker actions that contribute to revenue or production, not idle/redundant movement. | Section 4, rank 1, 2, 3 |
| `movement_overhead` | USED | PARTIAL | (inherent in efficiency framing) | Copilot recognizes movement as a cost but does not isolate or optimize movement separately. Movement is captured in throughput-to-cash efficiency. | Section 4, rank 1, 2 |
| `necessary_transit_fraction` | NOT_USED | ABSENT | (none) | Copilot does not separate necessary transit from redundant movement. It treats movement holistically within throughput efficiency. | (none) |
| `routing_completion_efficiency` | USED | FULL | `throughput_to_cash_conversion` | Copilot implicitly measures how effectively routing completes productive loops, not just the number of actions. | Section 4, rank 1 |
| `action_dispatch_failure` | USED | PARTIAL | (none; handled implicitly) | Copilot avoids explicit loop traps through state-based conditional dispatch. Failures are monitored but not isolated as distinct concepts. | Section 2.1 |
| `worker_action_monetization_rate` | USED | FULL | `throughput_to_cash_conversion` (rank 1) | Copilot tracks ricavi realizzati / azioni worker as the primary efficiency metric. Uses both macro (all actions) and netta (productive + logistics only) forms. | Section 4, rank 1 |
| `crop_care_action_flow` | USED | FULL | `crop_activation_and_monetization` | Copilot maintains a composite crop-care flow that includes PLANT, WATER, and HARVEST actions coordinated to maintain productive surface. | Section 4, rank 3 |
| `planting_action_flow` | USED | PARTIAL | (part of `crop_activation_and_monetization`) | Copilot counts PLANT actions as part of crop activation but does not isolate them as a separate strategic lever. | Section 4, rank 3 |
| `watering_execution_rate` | USED | FULL | (critical component of `crop_activation_and_monetization`) | Copilot recognizes WATER as a critical bottleneck. Continuous watering is necessary for crop progression and ties directly to monetization. | Section 4, rank 3; Section 5.1 |
| `watering_continuity` | USED | FULL | (implicit in maintenance requirement) | Copilot requires regular watering as part of maintained_productive_surface logic. Interruption causes decay. | Section 4, rank 3 |
| `crop_harvest_action_flow` | USED | PARTIAL | (part of `crop_activation_and_monetization`) | Copilot counts HARVEST as a conversion step but does not isolate harvesting strategy as a distinct lever; it follows from maintained surfaces. | Section 4, rank 3 |
| `crop_care_completion_rate` | USED | PARTIAL | (care_completion measured implicitly) | Copilot tracks whether crop care is completed on maintained surfaces but does not report it as a formal KPI. | Section 4, rank 3 |
| `crop_decay_risk_window` | USED | PARTIAL | (implicit in maintenance timing) | Copilot understands that unwatered crops decay, creating a care-continuity requirement. The window is implicit in the state-based care logic. | Section 4, rank 3 |
| `crop_horizon_alignment` | USED | PARTIAL | `milestone_day_gating` (deprecated but illustrative) | Copilot is aware that planting must complete before days 26–27 for end-of-episode harvest. State-based decisions now subsume day thresholds. | Section 4, rank 3 |
| `crop_revenue_mix` | USED | PARTIAL | `crop_activation_and_monetization` | Copilot generates revenue from crops but does not explicitly optimize product mix. Mix emerges from working-set capacity and rotational discipline. | Section 4, rank 3 |
| `feed_availability` | USED | FULL | `wheat_feed_security` (rank 6) | Copilot maintains awareness of feed stock as a constraint on livestock. Shortage forces market purchases or herd reduction. | Section 4, rank 6 |
| `feed_security_buffer` | USED | FULL | `wheat_feed_security` | Copilot sustains a buffer of internal feed to avoid market dependency and maintain herd continuity. | Section 4, rank 6 |
| `feed_market_dependency` | USED | FULL | `wheat_feed_security` (negative pole) | Copilot tracks reliance on market wheat as a cost drain. High dependency increases cash pressure and reduces reinvestment capacity. | Section 4, rank 6 |
| `feed_market_expenditure` | USED | FULL | (cost component of `wheat_feed_security` / `cash_buffer_before_expansion`) | Copilot monitors market feed purchases as a key drain on deployable capital. | Section 4, rank 7 |
| `wheat_operating_flow` | USED | FULL | `wheat_feed_security` | Copilot treats wheat as a multi-role commodity: seed, internal feed, market commodity. Autarky vs. market is a policy choice, not an ontological truth. | Section 4, rank 6 |
| `market_churn_cost` | NOT_USED | ABSENT | (none) | Copilot does not explicitly track buy/sell cycles of the same commodity as a distinct cost category. Churn is implicit in market dynamics. | (none) |
| `livestock_headcount` | USED | FULL | `target_cows` / `target_sheep` (now dynamic) | Copilot maintains variable herd counts gated by pasture and feed availability, not fixed targets. | Section 3, parameter rank 9 (herd_target_sensitivity) |
| `livestock_capacity` | USED | FULL | `pasture_to_livestock_alignment` | Copilot limits herd size to what pasture and feed can sustain. Capacity is a function of available pasture, feed buffer, and workforce. | Section 4, rank 5 |
| `pasture_capacity_alignment` | USED | FULL | `pasture_to_livestock_alignment` | Pasture size and allocation are aligned to herd capacity, not maximized speculatively. Copilot gates herd expansion on pasture readiness. | Section 4, rank 5 |
| `livestock_product_flow` | USED | PARTIAL | `pasture_to_livestock_alignment` (economic component) | Copilot tracks livestock output (Milk, Wool) as revenue but treats it as secondary to crop-driven throughput. | Section 4, rank 5 |
| `species_margin_differential` | USED | PARTIAL | `herd_target_sensitivity` | Copilot is aware that species differ in feed/output ratio but does not isolate species-specific optimization as a primary lever. | Section 3, parameter rank 9 |
| `fertilizer_byproduct_flow` | USED | PARTIAL | (minor revenue stream within `throughput_to_cash_conversion`) | Copilot generates fertilizer as a byproduct of livestock but does not prioritize fertilizer monetization. | Section 4, rank 1 |
| `market_transaction_value` | USED | FULL | (price component in all market transactions) | Copilot reconstructs transaction prices from action ledgers when available; uses base prices when ledgers are not available. | Section 5.1–5.2 |
| `operating_cash_buffer` | USED | FULL | `cash_buffer_before_expansion` (rank 7) | Copilot maintains a cash reserve to protect operating continuity (wages, seeds). Buffer size is not canonically fixed. | Section 4, rank 7 |
| `deployable_capital_window` | USED | FULL | `cash_buffer_before_expansion` (timing component) | Copilot expands only when cash exceeds operating buffer. The window opens dynamically based on cash state. | Section 4, rank 7 |
| `asset_liquidity_lag` | PARTIAL | PARTIAL | (implicit in expansion timing logic) | Copilot is aware that capital deployed in land/animals does not immediately return cash, influencing expansion timing. | Section 4, rank 4 |
| `inventory_to_cash_conversion` | USED | FULL | `inventory_liquidation_and_shed_flush` (rank 10) | Copilot ensures inventory reaches the shed for sale, with explicit end-game liquidation logic. | Section 4, rank 10 |
| `market_sellthrough_lag` | USED | PARTIAL | (implicit in inventory-to-cash timing) | Copilot recognizes delay between harvest/collection and sale but does not explicitly model price decay. | Section 4, rank 10 |
| `unsold_inventory_value` | NOT_USED | ABSENT | (none; terminal inventory is treated as sunk loss) | Copilot does not retain end-game inventory intentionally and does not value unsold assets. | (none) |
| `reinvestment_cash_flow` | USED | FULL | (implicit in expansion logic) | Copilot reinvests realized cash into land, animals, and workforce according to state-based availability. | Section 4, ranks 1–7 |
| `product_mix_revenue` | USED | PARTIAL | `crop_activation_and_monetization` (revenue component) | Copilot generates revenue from multiple products (crop, livestock, fertilizer) but does not explicitly optimize product mix. | Section 4, rank 3 |
| `price_realization_variance` | PARTIAL | PARTIAL | (prices observed in action ledgers vary from base) | Copilot notes that market prices fluctuate but does not explicitly model price elasticity as a decision variable. | Section 5.3 (mixed evidence) |
| `dynamic_market_price_elasticity` | NOT_USED | ABSENT | (price fluctuation noted but not leveraged) | Copilot does not exploit dynamic pricing strategically. Price changes are treated as constraints, not as optimization opportunities. | (none) |
| `shed_inventory_integrity` | USED | FULL | (implicit in deposit/return logic) | Copilot ensures inventory safely reaches and persists in the shed, avoiding loss due to worker-contract expiration. | Section 4, rank 10 |
| `contract_inventory_loss` | USED | FULL | (implicit in end-of-hour worker reset) | Copilot avoids inventory loss by depositing goods to the shed before hourly contract resets. | Section 4, rank 10; evidence ENGINE_RULE_SUPPORTED |
| `endgame_shutdown_timing` | USED | PARTIAL | `inventory_liquidation_and_shed_flush` (timing component) | Copilot stops new planting and focuses on harvest/collection in the final days but does not use a fixed day threshold. | Section 4, rank 10 |
| `endgame_inventory_liquidation` | USED | FULL | `inventory_liquidation_and_shed_flush` (rank 10) | Copilot aggressively liquidates remaining inventory in the final episode steps to maximize terminal cash. | Section 4, rank 10 |
| `field_cleanliness_state` | USED | PARTIAL | `field_cleanliness_priority` (deprecated) | Copilot acknowledges weeds but deprioritizes weed cleanup; cleanliness is not a primary profit driver. | Section 3, rank 11 (deprecated); Section 5.3 |
| `weed_backlog_cost` | NOT_USED | ABSENT | (not quantified in Copilot model) | Copilot does not formally calculate opportunity cost of weed cleanup and treats it as acceptable overhead. | (none) |
| `market_order_batch_limit` | PARTIAL | PARTIAL | (constraint known; not explicitly leveraged) | Copilot is aware of the 10-order-per-turn market limit and respects it implicitly in dispatch design. | Section 2.1; evidence ENGINE_RULE_SUPPORTED |
| `action_order_slot_pressure` | NOT_USED | ABSENT | (none) | Copilot does not quantify slot pressure as a distinct diagnostic. The constraint is absorbed into dispatch design. | (none) |
| `state_capacity_alignment` | USED | FULL | `working_set_capacity_gate` (rank 2) | Copilot's core logic is state-based capacity alignment: cash, crops, pasture, and ownership must be synchronized before growth. | Section 2.2; Section 4, rank 2 |
| `local_kaggle_fidelity_gap` | PARTIAL | PARTIAL | `local_kaggle_fidelity_gap` (Section 5.3) | Copilot acknowledges the gap between local and Kaggle performance. X1.15 local benchmark is used but Kaggle validity remains unproven. | Section 5.3–5.4 (Validity discipline) |
| `operational_divergence_onset` | USED | PARTIAL | (implicit in Day-1 decision quality assessment) | Copilot recognizes that early operational choices (e.g., crop care, herd gating) diverge strategies by Day 1. | Section 5.1 (implicit) |
| `economic_lock_in_onset` | USED | PARTIAL | (implicit in compounding logic) | Copilot understands that divergence hardens into economic lock-in around Day 12 when capital gaps become irreversible. | Section 5.1 (implicit) |
| `final_money_outcome` | USED | FULL | (ultimate performance metric) | Copilot is optimized to maximize `final_money_outcome` at Step 720. This is the terminal objective. | Section 1; Section 4, all ranks |

### 9.1 Mapping Summary

**Total canonical concepts:** 64  
**Copilot USED:** 50  
**Copilot PARTIAL:** 7  
**Copilot NOT_USED:** 7  

**Mapping Classification:**
- FULL: 33
- PARTIAL: 24
- ABSENT: 7
- BROADER: 0
- NARROWER: 0
- CONFLICT: 0

### 9.2 Key mapping observations

1. **Throughput-to-cash centrality:** Copilot's model is centered on `worker_action_monetization_rate` (`throughput_to_cash_conversion`) as the primary efficiency metric, enabling both macro and netta forms.

2. **State-based expansion:** Copilot uses `state_capacity_alignment` (`working_set_capacity_gate`) as the core policy envelope, replacing day-based thresholds with conditional gating on cash, crops, and pasture.

3. **Conservative livestock:** Copilot treats `livestock_capacity` (`pasture_to_livestock_alignment`) as demand-driven, not as a universal maximization target. Herd targets are dynamic.

4. **Crop prioritization:** `crop_activation_and_monetization` and `watering_execution_rate` are ranked as critical factors. Copilot does not compromise crop care for other goals.

5. **Feed as constraint:** `wheat_feed_security` is high-impact (rank 6) but not the primary lever. Feed is a constraint to be satisfied, not an optimization axis.

6. **Inventory discipline:** Copilot emphasizes `inventory_liquidation_and_shed_flush`, treating end-game cash conversion as non-negotiable.

7. **Local-only evidence:** Copilot's confidence in several parameters (e.g., `herd_target_sensitivity`, `milestone_day_gating`) is marked as LOCAL_ONLY or LOCAL_KAGGLE_CONFLICT, not REPLAY_SUPPORTED.

### 9.3 Concepts NOT used by Copilot

The following canonical concepts are explicitly NOT_USED or ABSENT:

- `marginal_hire_payback` (threshold-based instead)
- `necessary_transit_fraction` (not isolated)
- `market_churn_cost` (not quantified)
- `unsold_inventory_value` (terminal inventory discarded)
- `weed_backlog_cost` (not formalized)
- `action_order_slot_pressure` (constraint implicit)
- `dynamic_market_price_elasticity` (prices treated as fixed constraints, not exploited)

These absences do not constitute errors; they represent Copilot's strategic choices to prioritize other factors.

### 9.4 Preservation of Copilot independence

**Ranking, impact, and confidence are unchanged:**
- Section 4, the "Ranking by expected economic impact" table, remains the canonical expression of Copilot's independent judgment.
- No policy thresholds, strategic timing, or causal interpretations have been altered.
- The ontology mapping serves only to translate Copilot's terminology into canonical concept_ids for E15 cross-model comparison.

**This mapping is a **semantic normalization only**, not a strategic revision of the Copilot model.**

### 5.3 Falsifying / contradictory evidence
- Fixed workforce counts are contradicted by replay matrices that show distinct productive peaks and trajectories.
- Fixed livestock targets are contradicted by varied herd mixes across sessions.
- Weed/clean-field minimization is mixed or contradicted in competitor replay analysis.
- A universal Q2-first or Q2-rejecting rule is not supported; the evidence instead supports conditionality.

### 5.4 Validity discipline
Local-only evidence is separated from replay-supported evidence. The Copilot model does not collapse the distinction between the two. When a parameter is only supported by local behavior, it remains marked as local or locally-conflicted until a replay or Kaggle proof is available.

---

## 6. Taxonomic change log (Copilot)

### Additions
- `state_based_capacity_gate`
- `throughput_to_cash_conversion`

### Reformulations
- `target_cows` from fixed herd assumption to conditional state gate
- `target_sheep` from static target to dynamic pasture-fed configuration
- `land_unlock_condition` from rigid rule to liquidity + operating-state gate

### Removes
- `fixed_hire_count`
- `fixed_q2_priority`
- `fixed_field_cleanliness_priority`

### Deprications retained for history
- historical land or workforce timing heuristics that were never uniquely supported by evidence

---

## 7. Open questions and ablation priorities

1. Is the low-capacity gate overly conservative on seeds with unusually high early cash generation?
2. Does a more explicit Q2 conditional branch materially improve reward without destabilizing working capital?
3. Are there stronger feed-security thresholds than the current state-based gating?
4. Which product mix (crop vs animal vs fertilizer) gives the best marginal throughput in the 10-20 day window?

---

## 8. Verification and build status

- Copilot package exists independently under `src/agricola/strategy/copilot/`
- Standalone build output is `submission_copilot.py`
- Local behavioral smoke test is `tests/test_e12_x1_15_copilot.py`
- The Copilot model is isolated from the Antigravity and Codex workstreams by namespace and build path

This specification is intentionally narrow, open to revision, and grounded in local plus replay evidence rather than agency convergence by copy.
