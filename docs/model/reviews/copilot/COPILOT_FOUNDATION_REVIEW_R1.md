# KAGGRICULTURE — FOUNDATION REVIEW R1 — COPILOT

**Reviewer:** Copilot independent review
**Date:** 2026-08-30
**Scope:** operational consistency, observability, and decision-time
translatability of the C1 foundation. This is not a policy optimization or a
proposal for a new treatment.
**Independence boundary:** no Antigravity review was read. The review used
only the State Machine C1, Feature Model C1, canonical ontology, Copilot
MODEL_SPEC, post-E15 consolidation, and the Copilot execution path needed to
test claims of consumption.

## 1. Verdict

```text
VERDICT: DO_NOT_FREEZE_FOUNDATION_C1
BLOCKERS: 3 P0
MATERIAL_FINDINGS: 6 P1
```

The C1 documents correctly separate many important categories (engine state,
policy context, telemetry-only labels, and outcomes), reject deterministic
prediction of random WEED spawn, and preserve `crop_decay_risk_window` as a
structured constraint. They are not yet a single executable foundation:

1. `current_MODEL_SPEC_usage` is explicitly keyed to the frozen **Codex**
   model while the requested current model and executable path are Copilot.
   Its `USED`/`PARTIALLY_USED` values cannot support a Copilot
   implementation-consistency decision.
2. several derived states and aggregates deliberately have no canonical
   formula, but are still marked `USED`, `FULL`, or decision-time available
   in the Copilot MODEL_SPEC;
3. the Copilot MODEL_SPEC claims broad feature consumption that the wrapper
   neither receives nor computes, and the delegated runtime uses fixed
   thresholds and a second policy layer whose conditions are not specified in
   the MODEL_SPEC.

No finding recommends a threshold, ranking, or policy change. The required
resolution is to make definitions, inputs, state ownership, and measurement
contracts unambiguous before freezing.

## 2. Review method and acceptance criteria

For every candidate feature or transition, this review asks:

1. Is its precondition necessary and sufficient, including phase and actor?
2. Can it be computed from an observation and persisted policy memory before
   the action is emitted?
3. Does its definition name a canonical scope, time window, denominator, and
   state precedence where applicable?
4. Is an asserted MODEL_SPEC consumer demonstrably supplied with the feature
   or with every primitive needed to compute it?
5. Can telemetry distinguish request, execution, state effect, and the
   relevant pre/post phase without reconstructing them from outcome?

`P0` blocks a freeze because two conforming implementations can make a
different decision or because the model-to-feature contract cannot be
verified. `P1` is material and must be resolved or explicitly scoped out
before a future implementation relies on it. `P2` is a non-blocking
clarification.

## 3. P0 findings

### P0-01 — `current_MODEL_SPEC_usage` has the wrong authoritative consumer

**Evidence.** The Feature Model declares that `current_MODEL_SPEC_usage`
references the frozen Codex E15 MODEL_SPEC, not the Copilot MODEL_SPEC
(Feature Model §1). Its gap section consequently makes claims about “the
MODEL_SPEC frozen” and the Codex consumer. In contrast, the Copilot
MODEL_SPEC maps its own 64 concepts and claims 50 `USED` concepts
(Copilot MODEL_SPEC §9).

**Why this blocks.** A row such as `CRP-19` can be `USED` in the C1 table only
with respect to a consumer which the document says is Codex, while a Copilot
reader can reasonably read it as a claim about the Copilot model. The two
models do not have the same mappings. This makes the requested check
“declared feature versus what the MODEL_SPEC consumes” non-deterministic.

**Required resolution.** Rename the existing column to
`codex_e15_frozen_usage`, retain its historical values, and add a separately
versioned `copilot_model_spec_usage` column or consumer matrix. Every
consumer matrix must name the exact MODEL_SPEC path and revision. Do not
infer Copilot usage from a concept being present in the ontology.

### P0-02 — The Copilot MODEL_SPEC overstates executable feature consumption

**Evidence.** The Copilot MODEL_SPEC marks, among others,
`worker_action_monetization_rate`, `market_transaction_value`,
`inventory_to_cash_conversion`, `maintained_productive_surface`, and
`operating_cash_buffer` as `USED/FULL` (Copilot MODEL_SPEC §9). The Feature
Model instead marks realized transaction value as telemetry-only and
unavailable before execution (`MKT-02`), and marks maintained surfaces and
cash buffer conditional because their formulas depend on an incomplete
maintenance or obligation model (`CRP-19`, `MKT-03`).

The runtime wrapper only passes `enable_land_expansion`, herd targets,
`max_workers`, and `stop_hire_day` to `ProductiveMassConfig`; its
`CopilotConfig` opening budget, cash floor, active-crop floor, and pasture
floor are not forwarded. The active Copilot routine calculates a small
capacity envelope, then delegates to the X112 routine. That routine uses
additional fixed day, cash, crop, pasture, and inventory rules. It receives
no action-execution result, transition reason, or realized transaction
record.

**Why this blocks.** “Used” currently conflates:

- policy-time primitive consumption;
- an implicit heuristic;
- telemetry measured after execution; and
- a diagnostic asserted by the MODEL_SPEC but not supplied to the runtime.

Two implementers can therefore both claim conformity while one computes a
formal buffer/maintained surface and another only uses raw money/plant count.
They will be different policies.

**Required resolution.** For every `USED` Copilot mapping, identify one of:

```text
POLICY_INPUT | RUNTIME_DERIVED | POST_ACTION_TELEMETRY | OUTCOME_ONLY
```

For `POLICY_INPUT` and `RUNTIME_DERIVED`, list source fields, policy-owned
memory, formula, phase, and the consuming function. Downgrade mappings that
are only telemetry or an unimplemented diagnostic; alternatively add the
missing implementation and corresponding pre-action inputs. The feature
table must never describe `MKT-02`, `GLB-02`, `GLB-03`, or `LBL-01` as a
pre-action policy input.

### P0-03 — Derived surface/capacity concepts are used before their formulas exist

**Evidence.** The ontology requires an operational maintenance formula for
`crop_surface_maintained` and a crop/pasture breakdown for
`maintained_productive_surface`. It requires explicit submetrics, weights,
and formula for `state_capacity_alignment`. The Feature Model itself records
no canonical formula for `activated_land_surface`,
`crop_surface_maintained`, `pasture_surface_maintained`,
`crop_care_completion_rate`, `productive_action_share`, and
`operating_cash_buffer`; it marks several of them `CONDITIONAL` or
`PARTIALLY_KNOWN`. The post-E15 consolidation also says not to freeze a
`state_capacity_alignment` formula.

The Copilot MODEL_SPEC nonetheless declares the maintained-surface and
state-capacity concepts `USED/FULL`, describes an “efficiency denominator,”
and says its core policy is state-based capacity alignment, without a
computable formula.

**Why this blocks.** The same raw board can produce different maintained
surface, available capacity, and expansion decisions depending on whether
GROWING-but-due-for-water, RETIREMENT_DUE, empty assigned tiles, pasture with
an unfed animal, or inventory held by a worker count. This is not merely a
metric-reporting gap: the MODEL_SPEC says those concepts gate policy.

**Required resolution.** Before any mapping is `FULL` or used for a gate,
publish a component schema with:

- included/excluded lifecycle states and species;
- board scope and ownership scope;
- pre-action versus post-refresh sampling point;
- numerator, denominator, zero-denominator convention, and window;
- whether a component is raw, engine-derived, policy memory, or telemetry;
- a versioned formula and examples for boundary states.

Until then, map these concepts `PARTIAL` or `NOT_USED` and restrict policy
claims to the raw predicates it actually uses.

## 4. P1 findings

### P1-01 — `tile_lifecycle_state` lacks an executable precedence function

The State Machine calls the lifecycle states canonical and the Feature Model
says precedence is declared, but neither provides an ordered classifier.
`OUT_OF_SCOPE` overlaps `LOST_WEED` for a WEED outside the working set; a
structure is both a non-crop tile and potentially out of scope; and the
definition of `RETIREMENT_DUE` (“no further production prevista” and
“lifespan impostato”) does not state the exact crop-rule fields, boundary
tick, or precedence versus `HARVEST_READY`. A classifier must specify input
domain, order, and fallback. For example, it must state whether working-set
membership is tested before tile kind, and exactly when an ongoing final
harvest becomes retirement due.

**Resolution:** add pseudocode or a decision table with mutually exclusive
predicates and test vectors covering every engine tile value inside and
outside the working set.

### P1-02 — Temporal semantics mix engine `step` and diagnostic `canonical_step`

The State Machine says `canonical_step = day * turnsPerDay + hour` is a
diagnostic workaround and must not replace engine `step`. Yet `CRP-13..15`
derive lifespan timing from `canonical_step`, while transition timing is
described as engine decay. The document does not state whether decay cadence
is keyed to engine `step`, day/hour, or both, nor how a policy should behave
when the two disagree.

**Resolution:** name the authoritative clock for each engine transition and
each derived deadline. If `canonical_step` exists only for replay repair,
mark it telemetry/reconstruction-only in lifespan timing and require online
policy computation from the authoritative live field.

### P1-03 — Necessary transition conditions omit actor reachability and action phase

Tables describe `PLANT`, `WATER`, `HARVEST`, `DIG`, `FEED`, and `CARE` mostly
with tile/resource predicates. An emitted action additionally requires a
specific actor, co-location or movement path, inventory compartment,
reservation/collision rules, action ordering, and remaining action phases.
The State Machine deliberately labels several of these workforce conditions
`PARTIALLY_KNOWN`, but the feature model calls deadlines decision-time
available without expressing serviceability.

**Resolution:** distinguish:

```text
tile_need | action_eligible_now | serviceable_before_deadline
```

Only the first is established for all listed tile rules. Keep the latter two
`PARTIALLY_KNOWN` until actor, inventory, collision, and phase requirements
are enumerated.

### P1-04 — Aggregate flow metrics have non-canonical denominators and ownership

The C1 catalog correctly warns that denominators must be declared, but its
definitions remain open for watering execution/continuity, crop-care
completion, worker capacity, productive action share, weed backlog cost,
livestock flow, conversion, and cash buffer. The ontology independently
requires explicit denominators for worker capacity, productive share, and
crop-care completion. This permits incompatible treatment of requests,
successful actions, repeated attempts, late service, worker inventory,
ongoing turnover, and zero-demand periods.

**Resolution:** each aggregate must have an `aggregate_contract` containing
scope, interval closure, numerator event predicate, denominator event
predicate, deduplication key, handling of zero denominator, and whether
failed/no-op actions are included. Metrics without this contract remain
diagnostic concepts, not comparable features or MODEL_SPEC inputs.

### P1-05 — Market and inventory features conflate displayed state, requests, executions, and estimates

The Feature Model correctly separates current market state from realized
value, but the Copilot MODEL_SPEC says it reconstructs transaction prices
from ledgers “when available” and otherwise uses base prices. Those two
values are not interchangeable: one is post-execution telemetry and the
other is an estimate. Likewise, the State Machine only partially knows
batching, per-unit quotes, and failure cases. A cash delta cannot uniquely
attribute a market transaction when multiple orders are processed.

**Resolution:** preserve four fields for every order:

```text
displayed_quote_pre_request
requested_quantity
executed_quantity
realized_price_and_cash_delta
```

Require explicit provenance for estimates, prohibit estimated value from
being reported as realized, and make policy use of post-action fields
impossible in the same decision phase.

### P1-06 — The current Copilot model description hides fixed thresholds and delegated rules

The MODEL_SPEC describes dynamic, state-based targets and removes fixed
workforce/herd assumptions. The actual Copilot routine uses explicit
day/cash/crop/pasture branches with targets `(1,0)`, `(2,0)`, `(4,1)`,
`(6,3)`, and `(7,4)`, then delegates to X112, which adds independent
day-based land, herd, reserve, seed, feed, and hiring rules. This can still
be a state-gated policy, but it is not implementable from the MODEL_SPEC:
the table omits the predicates, threshold inclusivity, day indexing
convention, conflict order, and the delegated rule set.

**Resolution:** either document the exact runtime decision graph as the
Copilot policy contract, including the X112 delegation, or narrow the
MODEL_SPEC to a non-executable conceptual model and stop claiming it
describes the active policy's feature consumption.

## 5. Decision-time and leakage assessment

| Category | Review result | Constraint |
|---|---|---|
| Raw board, clock, money, tile fields, current inventories, current market | Admissible in principle | Record observation phase and player/board scope. |
| Tile readiness and water-loss predicate | Admissible when crop rules and authoritative clock are available | Not a proof that a reachable actor can service it. |
| Lifecycle classification and lifespan deadline | Conditionally admissible | Requires P1-01/P1-02 classifier and clock contract. |
| Working set, reservations, target assignment | Policy memory, not engine feature | Persist ownership/version and update semantics. |
| Flow, continuity, dispatch failure, monetization | Historical derived feature | Require an online event log and declared window; never replace with terminal outcome. |
| Realized price/value, execution result, transition reason | Telemetry-only after mutation | Cannot gate the request that generated it. |
| Final money and unsold terminal valuation | Outcome/evaluation only | Must never enter pre-terminal policy input. |
| Random-WEED time to occurrence | Rejected | Future RNG is unavailable; eligibility is the only valid pre-action predicate. |

## 6. Required telemetry contract

The existing lists are substantively good but must become an event schema
with timing and identifiers. The minimum record for a future validating run
is:

```text
episode_id, player_id, engine_step, day, hour, phase, observation_sequence,
actor_id_or_order_id, action_sequence,
state_before, requested_payload, eligibility_predicates,
executed_payload, execution_status, failure_reason,
state_after_action, state_after_market, state_after_refresh,
transition_id, transition_reason, source_engine_or_policy_version,
tile_id, tile_lifecycle_before, tile_lifecycle_after,
inventory_compartment_before_after, market_quote_before,
requested_quantity, executed_quantity, realized_price, cash_delta
```

Additionally record, at every decision point, the policy-memory version and
contents required for working-set membership, reservations, and any aggregate
window. For daily aggregates, emit both constituent event IDs and the
`aggregate_contract` version. For R1 repair, retain raw `step` alongside
`day/hour`; do not overwrite either with reconstructed time.

This contract makes it possible to verify:

- that an action was eligible before it was requested;
- that it executed and changed the intended state;
- which EOD cause produced a loss;
- whether an aggregate used only past/current information;
- whether the runtime consumed the same feature values described in the
  MODEL_SPEC.

## 7. Explicitly preserved strengths and non-findings

The following parts should be retained:

1. The separation of `ENGINE_STATE`, `RAW_OBSERVABLE`, `DERIVED_FEATURE`,
   `POLICY_CONTEXT`, `TELEMETRY_ONLY`, and `OUTCOME_LABEL`.
2. The separation of online observability from replay persistence.
3. The rejection of deterministic `time_to_random_weed`.
4. The requirement that `crop_decay_risk_window` remain a structured,
   multi-cause constraint rather than a scalar score.
5. The distinction between active and maintained crop surface, current money
   and operating buffer, current market state and realized transaction value,
   and preventive versus recovery `DIG`.
6. The explicit `PARTIALLY_KNOWN`/`NOT_ANALYZED` boundaries for livestock,
   market, collisions, and non-R1 crop behavior.

## 8. Freeze exit criteria

The foundation may move from `CANDIDATE C1` only when all of the following
are present and internally consistent:

1. a versioned, named consumer matrix for each MODEL_SPEC;
2. an executable lifecycle classifier with precedence and boundary tests;
3. an authoritative clock/phase contract for every transition and deadline;
4. formula contracts for every aggregate used by a MODEL_SPEC or policy gate;
5. a Copilot runtime-to-spec trace identifying raw inputs, derived inputs,
   policy memory, telemetry, and outcomes;
6. the event schema above (or an equivalent schema) capable of validating
   each asserted execution and aggregate;
7. mapping downgrades for every concept that remains conceptual,
   telemetry-only, or formula-incomplete.

Until then, the correct status remains:

```text
CANDIDATE C1
NOT FROZEN
PENDING RESOLUTION OF P0-01, P0-02, P0-03
```
