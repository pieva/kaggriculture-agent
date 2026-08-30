# POST-TOURNAMENT FAILURE REVIEW -- COPILOT C2

## Scope and evidence boundary

This is a forensic review only. No candidate, Foundation, MODEL_SPEC, test, configuration,
or tournament artifact was changed, and no tournament was rerun.

Evidence examined:

- Foundation C2: `docs/model/ontology/ONTOLOGY_C2.md`,
  `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`, and
  `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`;
- candidate MODEL_SPEC:
  `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md`;
- candidate implementation:
  `src/agricola/strategy/copilot/c2_policy.py`,
  `src/agricola/strategy/copilot/agent_c2.py`, and
  `src/agricola/strategy/copilot/c2_config.py`;
- build evidence and candidate tests:
  `results/model_spec_c2/copilot/BUILD_VERIFICATION.md` and
  `tests/test_copilot_c2.py`;
- frozen protocol, runner, summaries, and the six preserved Copilot replays in
  `results/model_spec_c2/tournament/`.

The review also replay-inspected every Copilot P1 observation/action pair. In all six
episodes `observation.player == 1`; the farmer on `observation.farms[1]` remained
at `(4,4)` for all 720 steps, and that tile was `None` for all 720 observations.

## 1. Observed failure

The tournament result is unambiguous:

| Metric | Copilot C2 |
|---|---:|
| Episodes | 6 |
| Final money | $3,000 in every episode |
| Mean active surface | 0 |
| PLANT | 0 |
| MOVE | 0 |
| Market orders | 0 |
| Mean WATER / HARVEST / DIG dispatches | 119.2 / 136.2 / 586.2 |

The candidate completed all 720 steps with `DONE`; this is execution completion, not
productive-policy completion. It never acquired seed, never accessed an arable target,
never planted, never created a crop, and never generated revenue. Therefore the
finding is:

```text
PRODUCTIVE AGRICULTURAL LOOP NOT REALIZED
```

## 2. Reconstructed chain

| Level | Required / specified | Implemented or verified | Missing / failure effect |
|---|---|---|---|
| Foundation C2 | Describes engine phases, market settlement, local tile actions, worker movement, seed-constrained PLANT, and lifecycle transitions. It explicitly separates `action_eligible_now` from `serviceable_before_deadline`. | The common contract was available; it does not prescribe a strategy. | No Foundation defect caused the failure. It supplied the mechanics needed to build a bootstrap loop, but did not itself require one. |
| MODEL_SPEC Copilot C2 | Prevention of premature HARVEST and loss of an already-existing working set. It specifies local WATER, strict HARVEST, DIG of `LOST_WEED` / `RETIREMENT_DUE`, and PLANT only if seed exists. | The implementation largely realizes those local predicates. | It declares market invariant/non-priority and calls movement only a local worker policy. It contains no seed bootstrap, market order, spatial target, routing, acquisition, sale, revenue, or reinvestment contract. |
| Build | Implement the candidate-specific policy and callable entrypoint. | Local classifier and dispatch code were implemented. `market` is hardcoded to `[]`; no MOVE-producing path exists. Both entrypoints call the policy with `player_index=0`. | The P1 candidate reads opponent state. The executable is not a complete agricultural policy. |
| Build verification | Candidate tests, smoke execution, diff check, known limitations, then readiness declaration. | `BUILD_VERIFICATION.md` records target pytest PASS, diff check PASS, and smoke PASS. | The smoke did not require a real initialized economy to progress; it did not test P1 indexing, market bootstrap, movement, valid state effects, or a completed loop. |
| Test suite | Preserve C2 harvest/lifecycle semantics and entrypoint shape. | Tests cover synthetic readiness/classification and asserted action lists; the entrypoint test only checks dictionary/list types. | No test runs 720 real steps and asserts an agricultural state transition or economic outcome. |
| `TOURNAMENT_READY` | The master prompt requires invocability, no premature-HARVEST regression, lifecycle semantics, passing tests, and no known blocker. | Those syntactic/local requirements were treated as satisfied. | Readiness conditions did not require initialization, ownership-index correctness, movement, seed acquisition, PLANT success, surface creation, or revenue. |
| Real runtime | P1 must decide against its own observation and bootstrap from $3,000, zero seed, and spawn `(4,4)`. | The policy dispatches action labels derived from `farms[0]`, while its actual P1 farm is `farms[1]`. | Actions are applied to a stationary empty own tile, making them no-ops; independently, zero market orders makes first PLANT impossible. |

The productive loop was lost first at **resource acquisition**, **target selection/routing**,
and **correct player-state binding**, before the otherwise sensible local lifecycle rules
could ever apply.

## 3. MODEL_SPEC review

### What it actually contracts

The MODEL_SPEC gives precise rules for:

- strict `HARVEST` readiness (`PLANT`, positive yield, and crop age);
- WATER of a locally occupied unwatered `PLANT`;
- DIG of local `LOST_WEED` or `RETIREMENT_DUE`;
- PLANT on an empty local tile *only when seeds are already available*;
- conservative fallback to `PASS` where seed, cash, or diagnostic data are insufficient.

It explicitly says market transactions remain invariant and are not prioritized. Its
movement section says only: act on the tile where the worker already is; otherwise
`PASS`, and expressly avoids routing. The stated metrics include market activity,
movement share, active surface, and final money, but their presence in a metric list is
not an executable requirement or acceptance threshold.

### Required-loop coverage classification

| Loop element | MODEL_SPEC status | Runtime realization status |
|---|---|---|
| Initial capital | Observed, not operationalized | IMPLEMENTED BUT NOT CONSUMED for decisions |
| Resource / seed acquisition | NOT SPECIFIED | NOT IMPLEMENTED |
| Market ordering | NOT SPECIFIED as an active policy; explicitly invariant | NOT IMPLEMENTED (`market: []`) |
| Productive tile target | NOT SPECIFIED | NOT IMPLEMENTED |
| Movement / tile access | NOT SPECIFIED as routing; only local action described | NOT IMPLEMENTED |
| DIG | SPECIFIED | IMPLEMENTED INCORRECTLY in P1 because target state is read from player 0 |
| PLANT | SPECIFIED BUT CONDITIONAL on already-owned seed | IMPLEMENTED BUT UNREACHABLE from the real initial state |
| WATER | SPECIFIED | IMPLEMENTED BUT UNREACHABLE on Copilot's own farm; P1 dispatch is also based on player 0 |
| HARVEST | SPECIFIED | Local predicate is implemented; P1 dispatch is based on player 0 and cannot harvest a self-created crop |
| Inventory / sale | NOT SPECIFIED | NOT IMPLEMENTED |
| Revenue / reinvestment | NOT SPECIFIED | NOT IMPLEMENTED |

### Classification

The failure is **E: a combination**, with primary specification and policy-realization
defects and a decisive build defect:

1. **MODEL_SPEC defect:** it never contracts the initial economic/productive loop.
   “PLANT if seeds exist” is not seed procurement. “Use the local worker” is not
   routing to a productive tile.
2. **BUILD defect:** `agent_c2.py` invokes
   `decide_actions(obs, player_index=0)` unconditionally. In a P1 observation this
   binds decisions to the opponent. The duplicate callable in `c2_policy.py` has the
   same hardcoded value.
3. **Incomplete policy realization:** the candidate intentionally omits market,
   movement, targets, selling, and reinvestment.
4. **VERIFY defect:** local dispatch and interface tests were accepted as evidence of
   functional policy, without validating effects in the initialized environment.

## 4. End-to-end productive loop

The required chain and actual breaks are:

```text
CAPITAL ($3,000)
  -> RESOURCE ACQUISITION              BREAK: NOT SPECIFIED / NOT IMPLEMENTED
  -> MOVEMENT / TILE ACCESS            BREAK: NOT SPECIFIED / NOT IMPLEMENTED
  -> DIG                               unreachable as productive preparation
  -> PLANT                             unreachable: seed inventory begins at zero
  -> WATER / MAINTENANCE               unreachable: no own crop exists
  -> MATURE CROP                       unreachable
  -> HARVEST                           unreachable as a successful own harvest
  -> INVENTORY / MARKET                BREAK: NOT SPECIFIED / NOT IMPLEMENTED
  -> REVENUE / REINVESTMENT            BREAK: NOT SPECIFIED / NOT IMPLEMENTED
```

The frozen protocol specifies zero initial seed and the replay confirms it. Since the
only PLANT branch is `tile is None and crop_name is not None`, and `_select_crop`
returns `None` with zero seeds, the candidate returns `PASS` on an empty correctly-read
spawn tile. Since the entrypoint always returns an empty market list, no future state can
make `crop_name` non-`None`. Thus, even if the P1 index defect were removed, the
agricultural loop is economically impossible by construction from the standard initial
state.

## 5. Movement analysis

The MODEL_SPEC does not define a destination, target-selection policy, path planner,
or condition that emits a cardinal movement action. `c2_policy.py` contains no action
path returning `NORTH`, `SOUTH`, `EAST`, or `WEST`; its only farmer returns are
`DIG`, `HARVEST`, `WATER`, `PLANT`, and `PASS`. Configuration field
`active_working_set_radius` is not consumed by the policy.

The Foundation makes movement available and states that the main farmer is reset to the
shed spawn at each EOD, so movement is necessary to work non-spawn tiles. There are no
candidate spatial targets and no reachable condition that can produce MOVE. The replay
result--the real P1 farmer at `(4,4)` for all 720 steps--is therefore the deterministic
consequence of absent movement dispatch, not merely a telemetry anomaly.

The P1 hardcoded-index defect compounds it: when the opponent has crops, the policy
selects WATER/HARVEST/DIG from opponent tile state, but those commands execute on
Copilot's own still-empty `(4,4)`. In R3 this explains the apparently active action
profile despite zero self surface. In R2 with a passive opponent, it mostly emits PASS.

## 6. Market and bootstrap analysis

No initial seed order is specified or implemented. The agent returns:

```python
{"farmer": farmer, "hands": hands, "market": []}
```

on every call. No `BUY_SEED`, `BUY_LAND`, `HIRE`, or `SELL` branch exists. The common
`ActionBuilder` supports these orders, so this is a candidate omission rather than an
engine limitation.

The first observation has zero owned seeds. Consequently:

```text
zero seeds + no BUY_SEED branch
-> `_select_crop` returns None forever
-> PLANT branch is unreachable
-> no crop output or sale can ever exist
```

This bootstrap failure is deterministic at step 0 for every tournament seed. It alone
makes PLANT and the economic loop impossible; routing and player-index errors are
additional independent blockers.

## 7. Action-loop and telemetry analysis

The runner's action telemetry counts the opcode returned by the agent. It does not
classify whether the engine accepted the opcode or whether a tile/inventory/money state
transition followed it. It separately samples active `PLANT` tiles, which correctly
reported zero, but that signal was not made a pre-tournament acceptance gate.

The tests repeat the same mistake at a smaller scale:

- recovery tests assert `["DIG"]`, not that `WEED -> EMPTY_ASSIGNED` occurred in the
  engine;
- WATER testing asserts `["WATER"]`, not `watered_today` or later crop survival;
- no test asserts a successful PLANT, crop existence, maturity, successful HARVEST,
  inventory receipt, or sale;
- the callable test accepts any list-valued `market`, including the permanently empty
  list.

Accordingly, `ACTION GENERATED` was permitted to stand in for `POLICY WORKING`.
The runtime proves that interpretation false: action labels were emitted while the
actual farm remained empty and cash unchanged.

## 8. VERIFY escape review

The reported `168 passed` and `3/3 TOURNAMENT_READY` establish repository/test health
under their chosen assertions, not agricultural realization. Candidate verification
records only target pytest, `git diff --check`, and a smoke execution; its known
limitations explicitly leave market non-priority.

| Required semantic assertion | Present before tournament? |
|---|---|
| 720-step completion | Yes, indirectly through smoke/completion expectations |
| MOVEMENT OBSERVED | No |
| Valid productive-tile access | No |
| SEED ACQUIRED | No |
| DIG SUCCESSFUL (`WEED -> EMPTY`) | No |
| PLANT SUCCESSFUL | No |
| CROP EXISTS / active surface > 0 | No |
| WATER SUCCESSFUL / crop survives EOD | No |
| MATURE CROP EXISTS | No |
| HARVEST SUCCESSFUL / inventory changes | No |
| Revenue generated | No |
| P1 own-state binding | No |
| Full economic loop | No |

The master build prompt allowed a deterministic short sanity check and required tests
for mechanisms “if pertinent”; it did not make successful initialization and loop
realization mandatory. Its `TOURNAMENT_READY` conditions require an invocable candidate
and semantic-regression avoidance, but not any minimum productive outcome. This is the
process escape that allowed a prevention-only fragment to be certified as tournament
ready.

## 9. Root cause analysis

```text
OBSERVED FAILURE
    Full completion but $3,000 terminal cash, zero seed/market/PLANT/MOVE,
    and zero active productive surface.

IMMEDIATE CAUSE
    On P1, the entrypoint hardcodes player_index=0 and bases local actions on
    the opponent while they are applied to Copilot's own stationary empty tile.

CONTRIBUTING CAUSES
    No market/seed bootstrap, no spatial target/routing/MOVE dispatch, and no
    selling or reinvestment policy. Independently, these make the loop impossible
    even with the player-index defect fixed.

PROCESS ESCAPE
    BUILD/VERIFY tested classifier correctness, dispatch labels, output shape, and
    completion, but not real-environment state transitions or a productive loop.

ROOT CAUSE
    Copilot C2 was specified and accepted as a local failure-prevention patch for an
    assumed existing working set, not as an end-to-end agricultural policy from the
    tournament's actual initialized state.
```

**Policy defect:** no bootstrap economy, routing, productive target set, market
orders, or economic closure.

**Specification defect:** those requirements were not contractual; the policy could
truthfully preserve an existing crop but not create one.

**Verification defect:** readiness was inferred from local action generation and
non-regression rather than observable effects. The P1 ownership/index contract was
also never tested.

## 10. Escape analysis

The simplest pre-tournament falsifying test would have been:

> Instantiate Copilot C2 against the real initial P1 observation, advance one full
> 720-step episode, and assert both `BUY_SEED >= 1` and `active_crop_surface > 0`
> (or, more minimally, assert `BUY_SEED >= 1` in the first actionable step).

It fails deterministically because the market list is always empty. A companion
two-seat test would have immediately exposed the hardcoded P1 index:

> For an observation whose `player == 1`, mutate only `farms[1]`; assert that the
> decision changes, while mutating `farms[0]` alone does not change the own-farm
> decision.

Other gates that would have intercepted the candidate:

1. static candidate completeness gate: require at least one market-order and one
   movement dispatch path when initial seeds are zero and work lies off spawn;
2. initialized-runtime smoke gate: assert seed acquisition, MOVE, and successful
   `PLANT` transitions;
3. lifecycle realization gate: require a self-created crop to survive WATER and reach
   maturity before HARVEST;
4. economic closure gate: require inventory and positive sale/revenue transition;
5. P0/P1 symmetry gate: run the same deterministic smoke as both players and compare
   own-farm state transitions;
6. readiness gate: reject completion with zero active surface or zero productive
   transitions.

## 11. Latent failures after bootstrap repair

| Risk | Classification | Evidence |
|---|---|---|
| P1 opponent-state decision binding | CONFIRMED | All tournament Copilot observations have `player == 1`, while both candidate entrypoints hardcode index 0. |
| Bootstrap impossibility with zero seeds | CONFIRMED | Initial replay inventories are zero; agent market is permanently `[]`; PLANT requires a positive seed count. |
| No spatial realization | CONFIRMED | No candidate MOVE return path, target enumeration, or routing logic exists. |
| Action effects can remain no-ops | CONFIRMED | Replay shows zero own `PLANT`/surface and unchanged cash despite many action labels. |
| Worker capacity/serviceability failure | HIGH RISK | No `HIRE`, worker routing, or serviceability budget exists; Foundation resets hands daily. |
| Incorrect retirement classification for zero-yield non-ongoing plants | HIGH RISK | `classify_tile_lifecycle` marks any zero-yield `PLANT` without `max_lifespan_step` as `RETIREMENT_DUE`; this needs a real-engine transition test after valid harvest. |
| No inventory-to-sale closure | HIGH RISK | The agent has no sell policy, so a repaired planting/harvest path would still lack revenue. |
| Atomic multi-PLANT seed overcommit | POSSIBLE | Foundation warns PLANT is atomically blocked per crop when same-step demand exceeds owned seed; no allocation logic is implemented. |
| Water behavior on an actual managed multi-tile surface | POSSIBLE | Only local tile checks exist; no route/deadline scheduling has been tested. |
| Strict HARVEST predicate itself accepts immature crops | NO EVIDENCE | Unit tests exercise age/yield rejection and acceptance; the predicate matches Foundation C2 for the tested crop rules. |

## 12. Proposed minimum acceptance gates for a future Copilot C2 build

These are proposed gates only; they are not implemented in this review.

### BUILD GATE

- Candidate resolves its own farm/private state using `observation.player` in both P0
  and P1 tests.
- Static/targeted tests demonstrate reachable branches for `BUY_SEED`, cardinal MOVE,
  valid PLANT, WATER, HARVEST, and SELL; branches must use own state.
- A zero-seed initial state produces a valid acquisition plan, not permanent PASS.
- Existing strict HARVEST and lifecycle predicate tests continue to pass.

### RUNTIME SMOKE GATE

Run the actual Kaggriculture environment from its standard initialization for a bounded
prefix, in both seats, and assert state effects:

- a market `BUY_SEED` is submitted and the owned seed balance subsequently increases;
- at least one MOVE changes the farmer coordinate and reaches a valid arable tile;
- a DIG, if issued, changes an eligible `WEED`/retired tile to empty;
- a PLANT consumes seed and produces a `PLANT` tile;
- `active_crop_surface > 0`.

### POLICY REALIZATION GATE

Run a complete 720-step real-environment episode and assert:

- completion without `INVALID`/`ERROR`;
- successful WATER changes the crop's watering state and at least one planted crop
  survives to a later day;
- at least one self-created crop reaches maturity;
- a valid HARVEST changes tile/inventory state;
- a sale causes a realized positive revenue/cash transition;
- the chain `seed acquired -> plant -> water -> mature -> harvest -> sell` occurs for
  the same candidate-owned production path.

### TOURNAMENT READINESS GATE

Across all frozen preflight seeds and both player positions:

- all runtime-smoke and realization conditions pass;
- `active_productive_surface > 0`, `PLANT > 0`, and `market activity > 0`;
- no readiness declaration is allowed solely from dispatch counts;
- telemetry records action **outcomes** (accepted/no-op/failed plus before/after state),
  not only action types;
- final money/revenue is measured and the policy completes at least one economic loop.

## COPILOT C2 FAILURE VERDICT

```text
Failure class:
    End-to-end policy realization failure; combined MODEL_SPEC, BUILD, and VERIFY escape.

Immediate cause:
    P1 entrypoint hardcodes player_index=0, deciding from the opponent farm while
    actions execute on Copilot's stationary empty own farm.

Root cause:
    The candidate was a local prevention policy for an assumed existing working set,
    not a specified or implemented bootstrap-to-revenue agricultural policy.

MODEL_SPEC defect:
    YES. No contractual seed acquisition, market ordering, spatial targets/routing,
    sale, revenue, reinvestment, or full initial-state loop.

BUILD defect:
    YES. Hardcoded P0 index in both callable paths; market is permanently empty and
    movement/target/routing are absent.

VERIFY defect:
    YES. Assertions validated action dispatch/interface/local predicates, not
    own-state binding or real state transitions and economic closure.

Process escape:
    TOURNAMENT_READY required invocability and local semantic non-regression, but no
    initialized-runtime productive-loop acceptance gate.

Productive-loop break:
    Capital -> resource acquisition -> movement/tile access; all downstream farming
    stages were unreachable. P1 state misbinding additionally made emitted actions
    no-ops on the real farm.

Latent failure risk:
    CONFIRMED bootstrap, P1-index, and routing failures; HIGH RISK worker,
    retirement-classification, and sale-closure failures after a bootstrap repair.

Minimum required remediation:
    Do not patch actions in isolation. Specify and implement a self-indexed,
    initialized-state bootstrap loop with market seed acquisition, targets/routing,
    valid lifecycle operations, sale, and reinvestment; then validate it in P0 and P1.

Required acceptance gates:
    BUILD GATE, RUNTIME SMOKE GATE, POLICY REALIZATION GATE, and TOURNAMENT READINESS
    GATE defined above, all based on observed state transitions/effects.

Confidence:
    HIGH. The conclusions are directly supported by source inspection and all six
    preserved Copilot replay observation/action traces.
```

```text
FAILURE_REVIEW_COMPLETE
REMEDIATION_NOT_STARTED
```
