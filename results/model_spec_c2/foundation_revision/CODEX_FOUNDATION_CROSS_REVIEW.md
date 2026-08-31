# KAGGRICULTURE C2 — Codex Foundation Cross-Review

Reviewer: Codex  
Review type: independent Foundation cross-review  
Review date: 2026-08-31  
Scope: ontology, state machine, feature model, frozen engine contract, Decision Lifecycle boundary, documentation alignment  
Independence note: the Antigravity and Copilot Foundation cross-review reports were not consulted.  

## 1. Executive Verdict

The three Foundation documents express a recognisable and largely compatible architecture, but they do **not** yet form an implementation-safe common Foundation. The review finds six blocking engine-contract contradictions: a nonexistent worker carrying capacity, observation paths that do not exist in the runtime state, hard-coded land and capacity constants, an incomplete ongoing-fertilizer predicate, a fictitious structure build cost, and an incorrect pending-animal-care transition.

The intended separation between policy-neutral environment semantics and agent-specific strategy is also incomplete. Several useful concepts belong in the shared layer, but working-set selection, livestock-capacity policy, retirement rules, cash/feed buffers, deployable-capital windows, and endgame shutdown or liquidation logic must remain agent-specific. The proposed Decision Lifecycle is suitable as a shared Foundation layer only after its lifecycle states, invalidation semantics, evidence timing, and boundary with `MODEL_SPEC` are made explicit.

Accordingly, this review returns **FAIL_WITH_BLOCKERS**. Foundation correction should precede Decision Lifecycle drafting. No Foundation, README, Decision Lifecycle, Model Spec, code, build, tournament, or Kaggle modification is authorized by this report.

### Required-question answers

| # | Required question | Answer |
|---:|---|---|
| 1 | Are ontology, state machine, and feature model mutually coherent? | **No.** Their central objects are recognisable across layers, but lifecycle taxonomies, fertilizer behavior, animal-care transitions, terminal timing, observability, and several feature paths are inconsistent. |
| 2 | Are there contradictions with the frozen engine contract? | **Yes.** Six are blocking and are recorded as P0 findings. |
| 3 | Is there policy leakage into the common Foundation? | **Yes.** Working-set, capacity, retirement, buffers, deployable-capital, and endgame concepts embed strategic choices. |
| 4 | Is the design free of future leakage? | **Not yet demonstrated.** No explicit future-state input is specified, but execution outcomes are sometimes labelled online-observable and request, eligibility, execution, and post-transition evidence are not contractually separated. |
| 5 | Are indispensable common features missing? | **Yes.** A canonical request/execution ledger, configuration identity, robust state paths, batch-aware eligibility, state-conservation quantities, and explicit lifecycle invalidation evidence are missing or incomplete. |
| 6 | Do any current features belong in `MODEL_SPEC` instead? | **Yes.** `POL-WS-*`, `POL-CAP-*`, `POL-RET-*`, strategy-specific buffers/windows, and value-laden productive/retirement classifications belong in agent-specific specifications or optional agent telemetry. |
| 7 | Is telemetry sufficient for performance decomposition? | **No.** It is broad but cannot yet support exact accounting or robust causal diagnosis. |
| 8 | Is provenance sufficient for fair comparison? | **No.** It needs an unambiguous episode identity scheme and a canonical environment-configuration identity/snapshot, in addition to the existing run, seed, model, player, opponent, and environment fingerprint fields. |
| 9 | Should the Decision Lifecycle be a shared Foundation layer? | **Yes, with refinements.** Its generic lifecycle and evidence contract are common; strategy selection and thresholds are not. |
| 10 | Should `MODEL_SPEC` remain agent-specific? | **Yes.** It is the correct home for goals, heuristics, planning horizons, thresholds, action prioritisation, and adaptation policy. |
| 11 | Is the proposed Decision Lifecycle / `MODEL_SPEC` boundary correct? | **Partially.** The architectural direction is correct, but several strategy-specific concepts still cross into the Foundation and generic invalidation/repair semantics are missing. |
| 12 | Is the proposed state sequence adequate? | **Not yet.** It needs explicit infeasible, cancel, invalidate, repair/replan, supersede, and terminal/closed paths; `REACT` and `VERIFY` also require clearer event semantics. |
| 13 | Does the Foundation support strategic divergence among agents? | **Only after correction.** The intended environment model is neutral, but present policy leakage can bias all agents toward one style. |
| 14 | Are README or project-documentation changes needed? | **Yes, later.** They should describe the layered architecture and terminology after the Foundation and Decision Lifecycle contracts stabilize. README modification is not authorized here. |
| 15 | Are there blockers before Decision Lifecycle drafting? | **Yes.** The six P0 engine contradictions and the boundary/lifecycle P1 findings should be resolved first. |

## 2. Documents Reviewed

### Foundation documents

- `docs/model/ontology/ONTOLOGY_C2.md` — SHA-256 `54f023da5ced12ea014725aff03724dc1747f264a775f17927199e861c2e40a9`.
- `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md` — SHA-256 `0e8cffa16899c3ad8cfd65ce32ea85227a01d1afdaac34da453d4840b7e52527`.
- `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md` — SHA-256 `9510360c37862a87231db1809fb5f6071452a18d65821af06927284e7382a53d`.

### Engine-contract evidence

- `results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md` — frozen reconciliation, SHA-256 `47dbdf9e0a9100483654951f8cdc61fc80e6225481b776818622ef0c15d1f1d5`.
- `results/model_spec_c2/foundation_revision_feedback/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md` — independent contract audit, SHA-256 `1c3ffc2dc5039caee0d5c9b5100775278d2b8cb7c062aa9b3952337d6d289c8e`.
- Engine aggregate fingerprint — `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d`.
- Frozen runtime implementation in the installed `kaggriculture.py`, used read-only to verify disputed predicates, mutation order, and state paths.

### Explicit exclusions

- Other agents' Foundation cross-review reports were not read.
- No benchmark, tournament, Kaggle run, source modification, cleanup, or Decision Lifecycle draft was performed.

## 3. Ontology ↔ State Machine

The documents share the main domain nouns—farm, tile, crop, worker, livestock, inventory, market, weather, fertilizer, actions, periods, and episode—but the mapping is not fully reciprocal.

| Concern | Ontology | State machine | Assessment |
|---|---|---|---|
| State boundary | Distinguishes observable concepts and derived flows | Gives a transition sequence | Directionally aligned, but the state machine describes end-of-day as if it followed `STATE(t+1)` instead of being part of the transition that produces it. |
| Farm lifecycle | Six-category lifecycle including `EMPTY_ASSIGNED`, `OUT_OF_SCOPE`, and `RETIREMENT_DUE` | Claims six states, but treats retirement as a policy view and broadens out-of-scope semantics | Inconsistent taxonomy and ownership. |
| Fertilizer | Represents availability, application, and effect | Specifies one-turn and ongoing effects | Ongoing effect omits the required same-transition watering condition. |
| Livestock care | Defines pending care and consumption at production | Describes feed/care/production transitions | Both imply persistence when not fed, contradicting the runtime reset on any scheduled production event. |
| Terminal state | Episode lifecycle concept | Explicit terminal predicate | Both use an oversimplified `episodeSteps` equality/next-step formulation rather than the frozen runtime boundary. |
| Action/result semantics | Some action flows are labelled online-observable while containing execution | Transition table separates guards/effects only partially | Request, eligibility, execution, no-op, and post-transition evidence need a shared vocabulary. |

The most consequential issue is epistemic: an action request is observable at decision time; execution success, fill, mutation, and reward are post-transition evidence. The ontology currently collapses portions of those phases into “online-observable” flows. A common lifecycle cannot safely use those concepts until the timing distinction is normative.

## 4. State Machine ↔ Feature Model

The feature model covers most state-machine entities, but several features cannot be computed from the runtime state as named, and some formulas encode a different transition model.

| State-machine concept | Feature-model mapping | Assessment |
|---|---|---|
| Worker inventory | `WRK-01`–`WRK-06`, `ELG-03/09/10/17` | Incorrectly adds a worker carrying-capacity constraint absent from the engine. |
| Tile lifecycle | `FRM-*`, environmental classifier, `POL-RET-*` | Class count and semantics differ; assigned-empty and retirement handling are not consistently represented. |
| Crop/fertilizer | `CRP-*`, `FRT-*`, `POST-10`–`POST-12` | Broad coverage, but ongoing fertilizer effect is wrong and fertilizer generation is not conserved under Boolean saturation. |
| Livestock | `LIV-*`, `POST-13`–`POST-18` | Several raw paths are fictitious; pending-care reset semantics are wrong. |
| Market | `MKT-*`, `POST-19`–`POST-24` | Uses nonexistent buy/sell price maps instead of the runtime `prices` table and does not fully encode inventory-sensitive quote timing. |
| Action eligibility | `ELG-*` | Per-action guards are useful, but batch ordering and aggregate same-crop demand are not represented. |
| Transition telemetry | `POST-*` | Broad diagnostic intent, but there is no canonical requested/eligible/executed/no-op event ledger with reasons. |
| Terminal condition | episode/time features | Inherits the state machine's incorrect terminal formulation. |

The feature model should be viewed as a contract for computations, not a catalogue of desirable labels. Every raw path must either exist in the observation or be explicitly marked as a deterministic derivation with inputs and timing. That standard is not met by the current livestock, market, worker, and configuration features.

## 5. Ontology ↔ Feature Model

Coverage is extensive but not cleanly typed.

- Most ontology entities have feature families, which is a strong base for a common environment model.
- The ontology's six farm lifecycle categories do not map one-to-one to the feature model's five environmental categories plus policy overlays.
- Ontology flows that combine intent and outcome do not have corresponding timestamped event records in the feature model.
- Several policy concepts are promoted to canonical ontology or feature concepts without being necessary properties of the environment.
- The feature model introduces implementation-looking raw fields that the ontology does not justify and the runtime does not provide.
- The ontology distinguishes provenance classes, but the feature model does not consistently distinguish direct observation, deterministic derivation, policy output, and post-transition telemetry at field level.

The reciprocal mapping should be tightened around four types: raw observation, deterministic environment derivation, agent-policy value, and post-transition evidence. A concept may appear in more than one phase only through separately named fields with explicit timestamps.

## 6. Engine Contract Alignment

Engine alignment fails. The critical mismatches are summarized below; their full dispositions are in Section 14.

1. Worker inventory is unbounded by `ANIMALS.max_held`; that field limits output held on an animal tile. The worker-capacity features and eligibility guards therefore reject valid actions.
2. Runtime tiles use flat fields such as `animal`, `fertilizer_available`, and `yield_units`; the feature model's nested `structure.*` observation paths do not exist.
3. Runtime market state exposes `inventory` and `prices`; there are no `buy_prices` or `sell_prices` maps.
4. Quadrant area derives from `boardSize`; the default 10×10 board yields 25 tiles per quadrant, not 16. Shed and market-order limits are configuration values, not universal constants.
5. Ongoing fertilizer produces a +2 crop increment only when the tile is watered in that transition and fertilizer has not expired.
6. Coop and pasture construction has no cash cost or cash guard in the frozen engine.
7. Pending animal care is cleared on every scheduled production event, including surviving unfed production events; it is not retained until a fed production event.
8. Terminal timing is framework-specific in the frozen implementation and is not represented by the documents' simple equality predicate.

Other contract-sensitive details that the eventual corrected Foundation must preserve include atomic same-crop planting validation, serialization effects across worker actions, inventory-sensitive market quote timing, private-shed delivery for animal purchases, and the distinction between animal output capacity and other inventories.

## 7. Policy-Neutrality and No-Future-Leakage

### Policy neutrality

The common Foundation may define what exists, what is observable, what actions mean, how transitions occur, and how evidence is recorded. It should not prescribe which fields an agent works, how many animals it should own, when it should retire assets, how much cash or feed it should reserve, or when it should shut down economic activity.

The following concepts currently cross that boundary:

- ontology concepts such as `feed_security_buffer`, `operating_cash_buffer`, `deployable_capital_window`, and endgame shutdown/liquidation;
- `POL-WS-*` working-set selection;
- `POL-CAP-*` livestock-capacity policy;
- `POL-RET-*` retirement rules;
- `POST-42` or similar classifications that decide which actions are “productive” rather than merely reporting action type and effect.

`POL-RES-*`-style generic commitment or reservation representation can remain shared if it records an agent's declared decision without imposing its value, horizon, or trigger.

### No-future-leakage

The feature model correctly states a general online/offline separation, and this review found no feature that explicitly requests a future observation. Nevertheless, the guarantee is incomplete because:

- action flows marked online-observable sometimes include execution or transaction outcomes;
- no canonical timestamped separation exists between requested, eligible-at-snapshot, submitted, executed, no-op, and observed-post-transition;
- some post-transition features lack a precise source-state and target-state definition;
- causal labels such as “economic lock-in” cannot be inferred from a single factual trace without a counterfactual or an explicitly weaker diagnostic definition.

The Foundation therefore cannot yet claim a proven no-future-leakage contract. The correct result is **PARTIAL**, not a finding that future leakage has already occurred.

## 8. Performance Decomposition

The telemetry catalogue covers many important dimensions: production, revenue, costs, crop care, livestock care, occupancy, action counts, timing, and market behavior. That breadth is useful, but sufficiency requires exact accounting identities and reproducible event evidence.

Current blockers to sufficient decomposition are:

- `POST-08` attributes a structure construction cost that does not exist;
- the wheat equation uses production generation where a true conservation identity must account for on-tile `yield_units`, worker inventory, shed inventory, feed consumption, sales, and boundary deltas;
- fertilizer “generated units” ignores Boolean saturation: setting an already-available fertilizer flag does not generate another storable unit;
- action telemetry does not normatively record every request, snapshot eligibility, engine execution/no-op result, reason, worker, action index, and transition;
- some efficiency metrics have incompatible definitions across ontology and feature model;
- “economic lock-in” is counterfactual, while the available data is observational;
- shared action costs and capital absorption lack explicit attribution rules;
- unsuccessful and invalidated actions are essential to diagnosing performance but are not first-class events.

A corrected decomposition should separate:

1. direct accounting identities, which must reconcile exactly;
2. descriptive diagnostics, which summarize observed behavior;
3. causal or counterfactual analyses, which require an explicit identification method and must not be presented as direct telemetry.

Until then, the answer to performance-decomposition sufficiency is **NO**.

## 9. Provenance

The proposed provenance already includes many necessary comparison keys: `episode_id`, `run_id`, seed, agent/model identity, player/opponent, environment fingerprint, horizon, and observed steps. It is not yet sufficient for fair comparison because the identity and scope of `episode_id` are unspecified and the complete runtime configuration is not canonically identified.

At minimum, every episode-level record and every event row should be joinable through:

- a globally unambiguous or run-scoped `(run_id, episode_id)` key with documented reset/progression semantics;
- seed and player/seat identity;
- agent/model/spec version identity;
- opponent identity and version;
- engine/environment fingerprint;
- canonical configuration hash or immutable configuration ID, with the normalized configuration snapshot retained;
- feature-schema and telemetry-schema version;
- transition identifiers sufficient to order all events deterministically.

The engine fingerprint must not be treated as a substitute for configuration. `boardSize`, `turnsPerDay`, `shedCapacity`, `maxMarketOrdersPerTurn`, `episodeSteps`, and other configuration values can change behavior without changing code.

## 10. Decision Lifecycle Architecture

The Decision Lifecycle should become a shared Foundation layer because every agent needs a common language for decision intent, feasibility, commitment, execution evidence, invalidation, and adaptation. A suitable policy-neutral lifecycle can standardize records and state transitions without choosing a strategy.

The proposed sequence is directionally sound but incomplete. Its common semantics should include at least:

- `decision_id`, plan/version identity, parent/superseded decision, owner, creation transition, and evidence snapshot;
- a proposed state and a feasibility result with reasons;
- an explicit infeasible/rejected path;
- a commitment object with scope, start, expected completion, invariants, and declared invalidators;
- requested action events separated from execution events;
- verify events tied to the resulting state transition;
- repair-within-commitment, cancel, invalidate, supersede, reopen/replan, completed, and terminal/closed paths;
- an evidence-timing rule defining what may be used at each lifecycle step.

`REACT` is better modelled as event intake and transition logic than as a single mandatory phase occurring only after verification. `VERIFY` is a recurrent evidence activity: it occurs after actions, at relevant state changes, and at terminal closure. A named `PLAN_FEASIBLE` state can be retained if it represents a completed feasibility gate rather than an agent's particular planning algorithm.

Commitment prevents oscillation only if its identity and invalidation contract are explicit. The shared layer should specify how an agent records a commitment and why it was retained, repaired, or invalidated; it must not prescribe commitment duration, risk tolerance, target crop mix, thresholds, or priority rules.

## 11. Decision Lifecycle / MODEL_SPEC Boundary

| Shared Foundation / Decision Lifecycle | Agent-specific `MODEL_SPEC` |
|---|---|
| Environment ontology and state-transition semantics | Objectives and utility formulation |
| Observation timing and provenance | Planning horizon and search method |
| Action request/execution event schema | Action selection and prioritisation |
| Generic feasibility result and reason codes | Strategy-specific feasibility margins |
| Generic commitment, reservation, invalidation, repair, supersession, and closure records | Commitment duration, scope choice, and invalidation thresholds |
| Configuration and engine identity | Cash, feed, inventory, and risk buffers |
| Exact accounting identities | Crop mix, field working set, herd sizing, and routing |
| Policy-neutral diagnostic primitives | Retirement, liquidation, shutdown, and endgame policy |
| Lifecycle conformance checks | Adaptation and opponent-response policy |

The proposed boundary is therefore only partially correct. Generic lifecycle governance belongs in the shared layer. Any default that changes what an agent prefers, reserves, plants, owns, retires, or considers “productive” belongs in the agent specification. Optional agent-declared fields may use a shared envelope, but their values and rules remain agent-owned.

## 12. Freedom for Agent-Specific Strategies

After the boundary corrections above, the Foundation can support materially different agents: conservative or aggressive capital deployment, crops or livestock, stable commitments or rapid replanning, market-oriented or self-sufficient play, compact or broad field use, and different reactions to weather and opponents.

To preserve this freedom, conformance must test only environment truth, timing, lifecycle record integrity, and telemetry integrity. It must not score compliance with a preferred working set, herd limit, reserve size, retirement trigger, planning horizon, or action priority. Shared telemetry may report those choices; it may not standardize them as the correct policy.

The current drafts do not fully meet this criterion because policy-labelled fields are embedded in the common feature model and strategy-specific buffers and endgame concepts are canonized in the ontology. This is correctable without abandoning the overall architecture.

## 13. Documentation Alignment Feedback

Project documentation will need an architectural update after the blockers are resolved and the shared Decision Lifecycle contract is approved. The update should explain, without prescribing agent strategy:

1. the layered architecture: engine contract → ontology/state machine/feature model → shared Decision Lifecycle → agent-specific `MODEL_SPEC` → implementation/evaluation;
2. that C2 means Cycle 2 and does not identify a particular agent strategy;
3. the difference between raw observation, deterministic derivation, agent-policy output, action request, engine execution, and post-transition evidence;
4. the provenance keys required for comparable episodes;
5. which artifacts are shared and which may diverge by agent;
6. that performance diagnostics are not automatically causal attribution;
7. the authoritative version/fingerprint references for each contract layer.

No README wording or patch is supplied because this review does not authorize README modification. Documentation should not be updated to describe an unstable lifecycle before the Foundation corrections and lifecycle contract are accepted.

## 14. Findings

### CR-FND-P0-01 — Nonexistent worker carrying capacity

- **Severity:** P0
- **Classification:** Foundation defect
- **Layer:** Feature model / engine contract
- **Source document:** `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** `WRK-06`, `ELG-03`, `ELG-09`, `ELG-10`, `ELG-17`, capacity section
- **Finding:** The feature model treats `maxHeld` as worker inventory capacity and conditions pickup, harvest, collect, and purchase eligibility on worker free space. The frozen engine has no worker inventory capacity. `ANIMALS.max_held` limits output held on an animal tile.
- **Evidence:** Runtime inventory addition has no worker-capacity guard; pickup, harvest, and collect do not test worker space. Animal refresh alone applies species `max_held` to tile output.
- **Impact:** Valid actions can be classified as ineligible, available capacity can be understated, and agents built against the common contract can systematically suppress legal collection and purchase behavior.
- **Recommended disposition:** Remove worker-capacity semantics and all dependent eligibility predicates. Rename and remap `max_held` exclusively as per-animal-tile output capacity.

### CR-FND-P0-02 — Observation paths do not exist in runtime state

- **Severity:** P0
- **Classification:** Foundation defect
- **Layer:** Feature model / observation schema
- **Source document:** `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** `LIV-01`, `LIV-10`, `LIV-11`, `MKT-02`, `MKT-03`, worker raw fields
- **Finding:** The feature model specifies nested fields such as `structure.animal.species`, `structure.fertilizer_available`, `structure.output_available`, `market.buy_prices`, and `market.sell_prices` that are absent from the runtime state.
- **Evidence:** Runtime tiles expose flat `animal`, `fertilizer_available`, and `yield_units` fields. Market state exposes `inventory` and `prices`. Worker identity/type/activity are list/index/config-derived values unless explicitly materialized by an adapter.
- **Impact:** The common feature contract cannot be implemented literally and independent agents may invent incompatible adapters.
- **Recommended disposition:** Replace every raw path with the actual state path or mark the field as a deterministic derivation with exact inputs, timing, type, and adapter version.

### CR-FND-P0-03 — Hard-coded land and capacity constants contradict configuration

- **Severity:** P0
- **Classification:** Foundation defect
- **Layer:** Feature model / engine contract
- **Source document:** `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** `FRM-03`, `INV-03`, market-limit formula
- **Finding:** The model assumes 16 tiles per quadrant and universal shed/order limits of 100 and 10. These are not general engine invariants.
- **Evidence:** Quadrants are computed from `boardSize // 2`; on the default 10×10 board each quadrant has 25 tiles. Shed capacity and per-turn market-order limits are configuration values.
- **Impact:** Farm area, utilization, free capacity, action eligibility, and normalized performance metrics are wrong under the frozen default and non-default configurations.
- **Recommended disposition:** Derive all areas and limits from canonical configuration fields; prohibit undocumented numeric defaults in environment features.

### CR-FND-P0-04 — Ongoing fertilizer effect omits same-transition watering

- **Severity:** P0
- **Classification:** Foundation defect
- **Layer:** State machine / feature model
- **Source document:** `KAGGRICULTURE_STATE_MACHINE_C2.md`; `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** end-of-day crop update; `FRT-04`
- **Finding:** Both documents imply that unexpired ongoing fertilizer alone yields the +2 crop increment. The engine also requires the tile to have been watered in the current transition.
- **Evidence:** Runtime crop growth applies ongoing fertilizer only when `was_watered` is true and the fertilizer expiry condition holds.
- **Impact:** Growth forecasts, fertilizer attribution, action eligibility, and performance decomposition overstate crop progress on unwatered tiles.
- **Recommended disposition:** Make the effect predicate conjunctive: watered in the relevant transition and ongoing fertilizer active at the engine-defined boundary; document one-turn versus ongoing application separately.

### CR-FND-P0-05 — Structure construction is assigned a fictitious cash cost

- **Severity:** P0
- **Classification:** Foundation defect
- **Layer:** State machine / feature model / accounting
- **Source document:** `KAGGRICULTURE_STATE_MACHINE_C2.md`; `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** `BUILD_COOP`, `BUILD_PASTURE`, `POST-08`
- **Finding:** The state machine requires cash greater than or equal to a structure cost, and telemetry records structure build cost. The frozen engine builds on a valid empty tile without a cash guard or cash deduction.
- **Evidence:** Runtime build handlers test tile eligibility and install the structure; they contain no price lookup or cash mutation.
- **Impact:** Legal builds can be rejected, cash planning is distorted, and profit decomposition records nonexistent expenditure.
- **Recommended disposition:** Remove the cash predicate and structure-cost metric for this engine contract. If a later engine adds a cost, introduce it through a versioned contract change.

### CR-FND-P0-06 — Pending animal-care transition is incorrect

- **Severity:** P0
- **Classification:** Foundation defect
- **Layer:** Ontology / state machine / feature model
- **Source document:** `ONTOLOGY_C2.md`; `KAGGRICULTURE_STATE_MACHINE_C2.md`; `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** pending care, animal production transition, care-consumption telemetry
- **Finding:** The Foundation implies pending care is consumed only by a fed production event and otherwise remains pending. The engine clears pending care on every scheduled production event, including an unfed event where the animal survives.
- **Evidence:** Runtime animal refresh evaluates fed bonus where applicable and then resets pending bonus to zero for the production event regardless of feeding outcome.
- **Impact:** Output forecasts, care timing, value attribution, and livestock-state reconstruction can all be wrong.
- **Recommended disposition:** Specify reset and bonus application as two distinct effects: bonus application requires the engine's fed-production condition; pending care reset occurs at every scheduled production event.

### CR-FND-P1-01 — Eligibility is not batch- and serialization-aware

- **Severity:** P1
- **Classification:** Architectural defect
- **Layer:** Feature model / action contract
- **Source document:** `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** `ELG-*`, planting eligibility, “silent no-op” claim
- **Finding:** Eligibility is defined mainly per action against one snapshot. Atomic same-crop planting validates aggregate demand, and serialized worker actions can invalidate later actions within the same step. `ELG-07` does not express aggregate same-crop seed demand.
- **Evidence:** The runtime validates grouped plant requests atomically and processes other worker actions in sequence against mutated state.
- **Impact:** A feature may label an action eligible even though its submitted batch is rejected or an earlier action consumes the required resource. “Every predicate prevents a silent no-op” is therefore not true.
- **Recommended disposition:** Define snapshot eligibility, batch feasibility, pre-execution eligibility, and actual execution as separate records. Add aggregate planting predicates and action-order identifiers.

### CR-FND-P1-02 — Farm lifecycle taxonomy is not reciprocal across layers

- **Severity:** P1
- **Classification:** Architectural defect
- **Layer:** Ontology / state machine / feature model
- **Source document:** All three Foundation documents
- **Section / feature / concept:** six-category lifecycle, `EMPTY_ASSIGNED`, `OUT_OF_SCOPE`, `RETIREMENT_DUE`, environmental classifier
- **Finding:** The ontology, state machine, and feature model claim or imply exhaustive lifecycle classifications but disagree on category membership, ownership, and whether retirement is environment state or policy overlay.
- **Evidence:** The ontology includes assigned-empty and a narrow out-of-scope category; the state machine broadens out-of-scope and treats retirement as a policy view; the feature model has five environmental categories and separate working-set/retirement policy features.
- **Impact:** Coverage checks and per-state metrics cannot be compared reliably, and strategy-specific field selection is mistaken for environment truth.
- **Recommended disposition:** Define a single policy-neutral physical/environmental tile-state partition. Represent assignment, working set, commitment, and retirement as separately typed agent-declared overlays.

### CR-FND-P1-03 — Action intent and execution evidence are epistemically conflated

- **Severity:** P1
- **Classification:** Architectural defect
- **Layer:** Ontology / feature model / telemetry
- **Source document:** `ONTOLOGY_C2.md`; `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** planting/watering/harvest/feed/care/transaction flows; online/offline classes
- **Finding:** Several flows are labelled online-observable while their descriptions include execution, fill, mutation, or transaction value. The feature model does not supply a normative event contract that separates those phases.
- **Evidence:** Execution success and state effects are known only after engine transition, even when action intent and a quoted price are known before it.
- **Impact:** Online features can accidentally depend on post-transition information, undermining no-future-leakage guarantees and lifecycle verification.
- **Recommended disposition:** Introduce timestamped request, snapshot-eligibility, submission, execution/no-op, and post-state events with distinct names and allowed consumers.

### CR-FND-P1-04 — Phase and terminal semantics are inaccurate

- **Severity:** P1
- **Classification:** Foundation defect
- **Layer:** Ontology / state machine
- **Source document:** `ONTOLOGY_C2.md`; `KAGGRICULTURE_STATE_MACHINE_C2.md`
- **Section / feature / concept:** global transition sequence, terminal predicate, episode end
- **Finding:** The state diagram makes end-of-day look external to the transition that produces the next state, and both documents reduce termination to an equality or simple next-step check that does not match the frozen runtime boundary.
- **Evidence:** Runtime applies actions, updates market/town/decay, conditionally performs end-of-day, and then emits the resulting state. Its framework-facing terminal guard uses the engine's specific step offset.
- **Impact:** Event timestamps, final-period behavior, terminal features, and trace replay can be off by one or assigned to the wrong state.
- **Recommended disposition:** Define one transition index convention, place all mutations inside it in engine order, and copy the exact versioned terminal predicate from the frozen contract.

### CR-FND-P1-05 — Agent strategy leaks into the common Foundation

- **Severity:** P1
- **Classification:** Model Spec concern
- **Layer:** Ontology / feature model / Decision Lifecycle boundary
- **Source document:** `ONTOLOGY_C2.md`; `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** buffers, deployable-capital window, endgame liquidation, `POL-WS-*`, `POL-CAP-*`, `POL-RET-*`, productive-action classification
- **Finding:** The shared documents canonize strategic choices that are neither engine facts nor necessary generic lifecycle fields.
- **Evidence:** Working-set size, herd cap, retirement trigger, reserve buffers, deployable capital, and endgame shutdown can legitimately differ among agents.
- **Impact:** Independent Model Specs are biased toward one policy family and strategic divergence becomes a conformance failure.
- **Recommended disposition:** Move decision rules and values into agent-specific `MODEL_SPEC`. Retain only generic typed envelopes for optional agent declarations and neutral raw/derived environment inputs.

### CR-FND-P1-06 — Performance accounting and causal labels are insufficient

- **Severity:** P1
- **Classification:** Architectural defect
- **Layer:** Feature model / performance telemetry
- **Source document:** `KAGGRICULTURE_FEATURE_MODEL_C2.md`; `ONTOLOGY_C2.md`
- **Section / feature / concept:** `POST-08`, wheat/fertilizer equations, routing metrics, `POST-31`, action metrics
- **Finding:** Direct accounting, descriptive efficiency, and causal interpretation are mixed. Some identities omit material state, fertilizer generation ignores Boolean saturation, routing definitions differ, and “economic lock-in” requires counterfactual support.
- **Evidence:** Wheat can reside on tiles, workers, or shed and can be fed or sold; those boundary stocks and flows are not all present in the stated equation. A true lock-in claim cannot be read directly from one observed trace.
- **Impact:** Episode totals may not reconcile and diagnostic comparisons can be mistaken for causal explanations.
- **Recommended disposition:** Establish exact conservation ledgers first, define observational diagnostics separately, and require a declared counterfactual method for causal metrics.

### CR-FND-P1-07 — Provenance cannot uniquely reproduce comparison conditions

- **Severity:** P1
- **Classification:** Foundation defect
- **Layer:** Feature model / provenance
- **Source document:** `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** provenance fields
- **Finding:** Existing fields do not define episode identity scope and do not canonically identify the full engine configuration.
- **Evidence:** Behaviorally material values such as board size, period length, capacities, order limits, and episode length are configurable independently of the code fingerprint.
- **Impact:** Rows can be ambiguously joined and apparently like-for-like agent comparisons can use different environments.
- **Recommended disposition:** Define `(run_id, episode_id)` semantics, retain a normalized immutable configuration snapshot and hash/ID, version telemetry schemas, and use deterministic transition/event keys.

### CR-FND-P1-08 — Decision Lifecycle candidate lacks failure and invalidation semantics

- **Severity:** P1
- **Classification:** Architectural defect
- **Layer:** Proposed shared Decision Lifecycle
- **Source document:** Foundation revision cross-review prompt and Foundation boundary implied by the three documents
- **Section / feature / concept:** candidate lifecycle sequence; commitment; react; verify
- **Finding:** The candidate sequence lacks explicit infeasible, cancellation, invalidation, repair, supersession, replan, and closed/terminal paths. It also leaves unclear whether `REACT` is an event intake or a fixed phase and when verification evidence becomes usable.
- **Evidence:** Real engine transitions can reject, no-op, invalidate resources, or end an episode before a plan completes; a linear success path cannot represent those outcomes.
- **Impact:** Different agents will implement incompatible commitment and replanning semantics, and the shared lifecycle may either permit oscillation or encode a strategy.
- **Recommended disposition:** Resolve the P0 contract issues first, then draft a versioned lifecycle state machine with generic reason codes, evidence timing, plan versions, commitment scope, repair-versus-reopen rules, and terminal closure.

### CR-FND-P2-01 — Evidence classes and derivation labels are inconsistent

- **Severity:** P2
- **Classification:** Documentation defect
- **Layer:** Ontology / feature model
- **Source document:** `ONTOLOGY_C2.md`; `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** provenance/evidence labels; worker and state identifiers
- **Finding:** Some values are labelled engine-verified or raw even though they are derived, adapter-assigned, or policy-produced; `worker_capacity_available` is a particularly misleading engine-verified label.
- **Evidence:** Worker IDs/types/activity and several convenience booleans require deterministic derivation or adapter conventions, while worker capacity is not an engine concept at all.
- **Impact:** Consumers cannot reliably determine whether a field is observed, computed, declared by policy, or learned after transition.
- **Recommended disposition:** Apply one field-level epistemic taxonomy and require derivation formulas and source timestamps for every non-raw value.

### CR-FND-P2-02 — Diagrams, naming, and transition coverage overclaim precision

- **Severity:** P2
- **Classification:** Documentation defect
- **Layer:** State machine / feature model
- **Source document:** `KAGGRICULTURE_STATE_MACHINE_C2.md`; `KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Section / feature / concept:** end-of-day diagram, configuration names, exhaustive transition table
- **Finding:** Some diagrams order effects differently from the runtime, configuration labels are not exact, and a table presented as exhaustive omits action families such as pickup.
- **Evidence:** Runtime animal refresh performs production/reset before setting the next fertilizer availability; the exact configuration key is `maxMarketOrdersPerTurn`; the transition coverage is not complete.
- **Impact:** These issues are unlikely to change current-state values in every case, but they impede trace debugging and encourage incompatible implementations.
- **Recommended disposition:** Make diagrams reflect mutation order, use exact versioned key names, and either complete action coverage or label tables as illustrative.

### CR-FND-P2-03 — Project documentation does not yet express the target layered architecture

- **Severity:** P2
- **Classification:** Documentation defect
- **Layer:** README / project architecture documentation
- **Source document:** project documentation as referenced by the review mandate
- **Section / feature / concept:** Foundation and Model Spec architecture
- **Finding:** The eventual five-layer structure and the shared-versus-agent-specific boundary need a stable, discoverable project-level explanation.
- **Evidence:** The current revision introduces a proposed shared Decision Lifecycle between environment Foundation and agent Model Specs, along with stricter evidence and provenance terminology.
- **Impact:** Contributors may edit the wrong artifact, treat C2 as a strategy, or confuse action requests with engine outcomes.
- **Recommended disposition:** After contract approval, update project documentation using the subjects listed in Section 13. Do not modify README during this review.

## 15. Residual Risks

Even after the listed findings are corrected, the following risks should be explicitly tested before implementation or competition use:

- engine version drift between the frozen fingerprint and the runtime used for evaluation;
- configuration drift hidden behind the same engine code fingerprint;
- adapter drift when deterministic convenience fields are materialized;
- ambiguous event ordering for multiple workers and atomic versus serialized action families;
- seat/player asymmetry and opponent identity leakage in comparative data;
- end-of-period and terminal off-by-one errors;
- telemetry that reconciles episode totals but loses intermediate no-op or invalidation evidence;
- lifecycle conformance tests that accidentally enforce one strategy;
- observational diagnostics being reported as causal effects;
- future engine variants adding costs, capacities, or state fields without a versioned Foundation migration.

The appropriate next validation after document correction is a small set of deterministic contract fixtures covering each engine predicate and transition boundary. That is a recommendation for later work, not build or evaluation authorization.

## 16. Final Gate

```text
ENGINE_CONTRACT_ALIGNMENT: FAIL
ONTOLOGY_STATE_MACHINE_ALIGNMENT: PARTIAL
STATE_MACHINE_FEATURE_MODEL_ALIGNMENT: FAIL
ONTOLOGY_FEATURE_MODEL_ALIGNMENT: PARTIAL
POLICY_NEUTRALITY: PARTIAL
NO_FUTURE_LEAKAGE: PARTIAL
ONLINE_OFFLINE_SEPARATION: PARTIAL
PERFORMANCE_DECOMPOSITION_SUFFICIENT: NO
PROVENANCE_SUFFICIENT: NO
DECISION_LIFECYCLE_AS_SHARED_FOUNDATION_LAYER: YES_WITH_REFINEMENTS
MODEL_SPEC_AS_AGENT_SPECIFIC_LAYER: YES
DECISION_LIFECYCLE_MODEL_SPEC_BOUNDARY: PARTIAL_NEEDS_REFINEMENT
FOUNDATION_SUPPORTS_STRATEGIC_DIVERGENCE: YES_AFTER_CORRECTIONS
DOCUMENTATION_ARCHITECTURE_UPDATE_REQUIRED: YES_AFTER_CONTRACT_STABILIZATION
README_MODIFICATION_AUTHORIZED: NO
FOUNDATION_REVISION_CLEANUP_AUTHORIZED: NO
P0_FINDINGS: 6
P1_FINDINGS: 8
P2_FINDINGS: 3
FOUNDATION_CROSS_REVIEW: FAIL_WITH_BLOCKERS
DECISION_LIFECYCLE_DRAFTING_RECOMMENDED: NO
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

This gate recommends correction and reconciliation only. It grants no authorization to modify any reviewed artifact or proceed to downstream execution.
