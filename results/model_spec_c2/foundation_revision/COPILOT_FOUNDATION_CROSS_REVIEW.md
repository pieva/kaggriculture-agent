# COPILOT - FOUNDATION CROSS-REVIEW

```text
AGENT_ID: COPILOT
DOCUMENT_TYPE: INDEPENDENT_FOUNDATION_CROSS_REVIEW
PHASE: REVIEW
DATE: 2026-08-31
SCOPE: READ / AUDIT / CROSS-REVIEW / ARCHITECTURE REVIEW / REPORT
SOURCE_ARTIFACTS_MODIFIED: NO
```

## 1. Executive Verdict

The Foundation is strongly aligned with the frozen Engine Contract and is deliberately strategy-neutral. Its feature, telemetry, and provenance coverage is sufficient for heterogeneous controllers and later review.

Two corrections are required before the Foundation can be called internally coherent: the three documents do not share one canonical tile-lifecycle vocabulary, and the candidate Decision Lifecycle sequence does not state a governed invalidation path. Neither issue contradicts the engine. The first must be reconciled in the Foundation documents; the second must be resolved when drafting the shared Decision Lifecycle Contract.

```text
REVIEW_VERDICT: ACCEPT_WITH_CORRECTIONS
ENGINE_CONTRACT_CONTRADICTIONS: NONE
FOUNDATION_BLOCKER: P1-01
```

## 2. Documents Reviewed

- `docs/model/ontology/ONTOLOGY_C2.md`
- `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`
- `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`
- `results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md` (frozen normative source)
- `results/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md` (frozen audit baseline)
- `results/model_spec_c2/foundation_revision/KAGGRICULTURE_COMMON_FOUNDATION_CROSS_REVIEW_PROMPT.md`

## 3. Ontology <-> State Machine Review

Clock, EOD ordering, species inventory, crop/animal lifecycles, fertilizer, inventory loss, market execution, worker lifecycle, and the action/request/execution distinction agree with the frozen contract. In particular, the State Machine correctly preserves the non-native status of derived labels and the non-causal nature of `RETIREMENT_DUE`.

The alignment fails at the shared tile-lifecycle taxonomy. The Ontology presents six online-derivable canonical categories including `EMPTY_ASSIGNED` and `RETIREMENT_DUE`; the State Machine repeats that taxonomy while describing `RETIREMENT_DUE` as a policy classification rather than an environment state. This cannot simultaneously be a total policy-neutral, online-derived environment classifier and a policy classification.

## 4. State Machine <-> Feature Model Review

The Feature Model correctly materializes current-state and historical deterministic derivations: clock, legal harvest readiness, crop care risk, fertilizer window/uplift, animal feed/care/escape semantics, inventory overflow exposure, action eligibility, and multidimensional capacity are separated as required.

`ACTION_ELIGIBLE_NOW` is correctly modeled as a current guard and not as a request, execution result, or future transition. The serviceability tripartition is also preserved: eligibility is derived, reservation is policy context, and realization is post-hoc.

However, the Feature Model's environment classifier exposes five labels with `EMPTY_AVAILABLE` and moves retirement to policy-only `POL-RET`. This disagrees with the six-label contract used by the Ontology and State Machine. The published mapping matrix still claims coverage of `tile_lifecycle_state`, so the discrepancy is not visible to a downstream consumer.

## 5. Ontology <-> Feature Model Review

The epistemic classes are generally well separated. Online environment facts and exact derivations are distinct from policy context and post-hoc telemetry; the catalog preserves no-future-leakage for terminal outcome, realized serviceability, routing diagnostics, and economic lock-in.

The catalog's `source_concept_id` field is not consistently a semantic mapping. For example, current buy prices are mapped to `dynamic_market_price_elasticity`, seed purchase prices to `planting_action_flow`, and fixed animal purchase prices to `livestock_headcount`. The feature values remain useful and do not create policy leakage, but these mappings weaken the claimed Ontology-to-Feature traceability.

## 6. Engine Contract Alignment

Alignment with the frozen contract is confirmed:

- parametric clock invariant and EOD trigger;
- five crop and three animal species, with `CHICKEN = NOT_SUPPORTED`;
- scheduled base animal output independent of same-day `FEED`, subject to survival;
- deferred care-bonus consumption and accumulation order;
- fertilizer total increment of 2 and net uplift of +1 within `day .. day+2`;
- conservative `PLACE` versus destructive `DROP` and EOD auto-drop overflow;
- daily farm-hand lifetime and allowed worker multi-occupancy.

The independently reverified aggregate fingerprint is `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d`. No engine-contract contradiction was found.

## 7. Policy-Neutrality and No-Future-Leakage

No strategy is selected by the Foundation: it does not prescribe crop/livestock mix, expansion timing, worker target, routing, cash threshold, action rank, or market policy. Explicit policy context is isolated from environment features.

No future leakage was found in the online vector. The static EOD-overflow exposure is explicitly counterfactual conditional on the current state rather than an asserted future result. The only classification ambiguity is `RETIREMENT_DUE`: its current wording crosses the boundary between an environment-derived label and a policy decision.

## 8. Performance Decomposition Review

The offline telemetry is sufficient for direct accounting and diagnostics: output, collection, sale, revenue, direct costs, capital absorption, worker action categories, movement/logistics, service actions, occupancy, losses, activation, first/last output, and Wheat feed-versus-sale flows are covered by `POST-01..43`.

The documents correctly do not infer causal or counterfactual contribution from this accounting alone. Such claims require later ablation, paired comparisons, or another experimental design.

## 9. Provenance Review

The Feature Model supplies stable/progressive `episode_id`, unique `run_id`, separate seed, agent, model-spec version, player position, opponent/configuration context, Foundation version, environment fingerprint, and active timing configuration. This meets the requested longitudinal-comparison provenance, provided the run harness enforces uniqueness rather than treating these fields as advisory labels.

## 10. Decision Lifecycle Architecture Review

`Decision Lifecycle Contract` should be a shared Foundation layer downstream from the Feature Model. It can govern decision-state transitions, evidence availability, commitment, verification, invalidation, and review without choosing strategy.

The candidate sequence is a suitable backbone, but it needs an explicit controlled invalidation transition. `VERIFY` during `COMMITTED_EXECUTING` must record evidence continuously without causing implicit replanning; only named, observable invalidation guards may exit commitment. The contract should define the destination and evidence preservation for an invalidated plan before another plan is defined.

## 11. Decision Lifecycle / MODEL_SPEC Boundary

The proposed boundary is correct:

- shared contract: lifecycle states, abstract entry/exit guards, commitment/invalidation/replanning protocol, temporal evidence availability, and request/execution/transition separation;
- agent-specific `MODEL_SPEC`: objectives, scoring, portfolio, workforce, routing, reservations, expansion, market behavior, review criteria, commitment horizon, and exploration.

The Foundation must not turn policy-context inputs such as `POL-RET`, reservations, or serviceable capacity into mandated values or decision rules.

## 12. Freedom for Agent-Specific Strategies

The common contracts provide the same environmental semantics while permitting legitimate divergence in all listed strategic dimensions. They allow different controllers to choose different crop/livestock portfolios, capital and terrain allocation, workers, routing, capacity reservations, expansion, market policy, and evaluation criteria without redefining the engine.

## 13. Documentation Alignment Feedback

After reconciliation, the designated documentation editor should:

- change the Foundation architecture from four artifacts to five shared layers, inserting `Decision Lifecycle Contract` between Feature Model and agent-specific `MODEL_SPEC`;
- state explicitly that `MODEL_SPEC` is agent-specific, while the preceding layers are common contracts;
- document the request/decision/execution/transition and online/policy-context/telemetry/outcome separations;
- find and update diagrams or prose implying a generic shared `MODEL_SPEC` or the old four-artifact flow;
- state that `C2` means Cycle 2, a revision/provenance identifier rather than an architectural layer.

No README patch or replacement text is supplied or authorized.

## 14. Findings

### P1-01

```text
ID: P1-01
SEVERITY: P1
LAYER: ONTOLOGY / ENVIRONMENT STATE MACHINE / FEATURE MODEL
SOURCE DOCUMENT: ONTOLOGY_C2.md section 3.G; KAGGRICULTURE_STATE_MACHINE_C2.md section 3.1; KAGGRICULTURE_FEATURE_MODEL_C2.md sections 5 and 20
SECTION / FEATURE / CONCEPT: tile_lifecycle_state; EMPTY_ASSIGNED versus EMPTY_AVAILABLE; RETIREMENT_DUE versus policy_retirement_due
FINDING: The three documents do not define one total, policy-neutral tile-lifecycle classifier. Ontology and State Machine declare a six-category online-derived taxonomy, while Feature Model implements five environment labels, renames the empty label, and makes retirement policy-only.
EVIDENCE: The Ontology calls tile_lifecycle_state ONLINE_DERIVABLE and includes EMPTY_ASSIGNED and RETIREMENT_DUE. The State Machine calls RETIREMENT_DUE a policy classification. The Feature Model returns EMPTY_AVAILABLE and assigns retirement solely through POL-RET, yet claims mapping coverage for tile_lifecycle_state.
IMPACT: A controller cannot depend on one stable semantic feature contract. It may incorrectly treat a policy assignment as an engine-derived state or rely on a category absent from the materialized classifier.
RECOMMENDED DISPOSITION: FOUNDATION DEFECT. Reconcile one vocabulary and classification rule. Either retain only exact environment-derived categories and make retirement explicitly policy context everywhere, or define an exact non-policy derivation with a complete formula and use it consistently. Align names and mapping matrix.
```

### P1-02

```text
ID: P1-02
SEVERITY: P1
LAYER: DECISION LIFECYCLE ARCHITECTURE
SOURCE DOCUMENT: KAGGRICULTURE_COMMON_FOUNDATION_CROSS_REVIEW_PROMPT.md section 6.2
SECTION / FEATURE / CONCEPT: DECISION_OPEN -> DEFINED -> PLAN_FEASIBLE -> COMMITTED_EXECUTING -> REVIEW_READY
FINDING: The candidate lifecycle names invalidation and controlled replanning as responsibilities but omits an explicit invalidation transition, its guards, and its destination.
EVIDENCE: VERIFY is continuous during COMMITTED_EXECUTING, but the candidate sequence only shows normal progression through REVIEW_READY.
IMPACT: Implementations may either replan on every observation change or remain committed after an observable plan failure; both undermine the stated anti-oscillation objective.
RECOMMENDED DISPOSITION: ARCHITECTURAL DEFECT. In the future shared contract, define named invalidation guards, a single permitted exit path from COMMITTED_EXECUTING, preservation of verification evidence, and the re-entry point for a new decision. Do not encode strategy-specific guards.
```

### P2-01

```text
ID: P2-01
SEVERITY: P2
LAYER: FEATURE MODEL
SOURCE DOCUMENT: KAGGRICULTURE_FEATURE_MODEL_C2.md section 4
SECTION / FEATURE / CONCEPT: source_concept_id mappings for CRP-02/03, MKT-08/09, and related raw/configuration features
FINDING: Several source_concept_id values name a different semantic concept from the value represented by the feature.
EVIDENCE: Crop species is mapped to crop_care_action_flow; planted_day to crop_horizon_alignment; seed-price configuration to planting_action_flow; and animal-price configuration to livestock_headcount.
IMPACT: Automated traceability and later MODEL_SPEC mapping can report concept coverage that is semantically broader or different from the actual feature.
RECOMMENDED DISPOSITION: FOUNDATION DEFECT. During reconciliation, introduce precise ontology concepts or mark the technical/configuration values NONE_DIRECT where appropriate, then correct the catalog and its mapping matrix.
```

## 15. Residual Risks

- The report confirms documentation contracts, not a runtime feature-extraction implementation.
- Provenance is structurally sufficient, but uniqueness and progression must be enforced by the future execution harness.
- Direct telemetry is not causal attribution.
- P1-01 must be reconciled before a controller can treat the tile classifier as frozen.

## 16. Final Gate

```text
ENGINE_CONTRACT_ALIGNMENT: YES
ONTOLOGY_STATE_MACHINE_ALIGNMENT: NO - P1-01
STATE_MACHINE_FEATURE_MODEL_ALIGNMENT: NO - P1-01
ONTOLOGY_FEATURE_MODEL_ALIGNMENT: NO - P1-01, P2-01

POLICY_NEUTRALITY: YES, WITH P1-01 CLASSIFICATION CORRECTION REQUIRED
NO_FUTURE_LEAKAGE: YES
ONLINE_OFFLINE_SEPARATION: YES
PERFORMANCE_DECOMPOSITION_SUFFICIENT: YES
PROVENANCE_SUFFICIENT: YES

DECISION_LIFECYCLE_AS_SHARED_FOUNDATION_LAYER: YES
MODEL_SPEC_AS_AGENT_SPECIFIC_LAYER: YES
DECISION_LIFECYCLE_MODEL_SPEC_BOUNDARY: YES
FOUNDATION_SUPPORTS_STRATEGIC_DIVERGENCE: YES

DOCUMENTATION_ARCHITECTURE_UPDATE_REQUIRED: YES
README_MODIFICATION_AUTHORIZED: NO
FOUNDATION_REVISION_CLEANUP_AUTHORIZED: NO

P0_FINDINGS: 0
P1_FINDINGS: 2 (P1-01, P1-02)
P2_FINDINGS: 1 (P2-01)

FOUNDATION_CROSS_REVIEW: ACCEPT_WITH_CORRECTIONS
DECISION_LIFECYCLE_DRAFTING_RECOMMENDED: YES, AFTER RECONCILIATION OF P1-01 AND WITH P1-02 INCORPORATED

FOUNDATION_FILES_MODIFIED: NO
README_MODIFIED: NO
DECISION_LIFECYCLE_CREATED: NO
MODEL_SPEC_MODIFIED: NO
CODE_MODIFIED: NO

DECISION_LIFECYCLE_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
