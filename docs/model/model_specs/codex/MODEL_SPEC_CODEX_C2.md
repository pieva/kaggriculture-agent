# MODEL_SPEC Codex C2 — Compact Q0 Routine V7

```text
MODEL_SPEC_ID: CODEX-C2-COMPACT-Q0-ROUTINE-V7
AGENT_ID: CODEX_C2
FOUNDATION_CHECKPOINT: f391ee2
SCOPE: AGENT_SPECIFIC_POLICY
LAND: Q0_ONLY
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Objective

The immediate objective is `FINAL_MONEY > 56772`. The controller pursues
monetized output from a compact, serviceable farm. It does not optimize owned
land, raw entity count, speculative trading, or formal plan complexity. The
project target remains 80,000, but this candidate is a Q0 causal test.

## 2. Production Architecture

The footprint is frozen:

```text
Q0:
  18 crop tiles: 9 MELON, 8 STRAWBERRY, 1 WHEAT
  6 PASTURE: 3 COW, 3 SHEEP
  central shed access
WORKFORCE:
  7 total = farmer + 6 hands
GOOSE:
  0
```

All productive positions are inside the NW 5×5 quadrant. The controller never
emits `BUY_LAND`. A nineteenth crop tile is outside the candidate definition.

## 3. Worker Roles

| Worker | Role | Primary responsibility |
|---:|---|---|
| 0 | `FLOAT_RESERVE` | hard interrupts, bootstrap help, temporary overload |
| 1 | `CROP_ZONE_0` | six-tile local crop route |
| 2 | `CROP_ZONE_1` | six-tile local crop route |
| 3 | `CROP_ZONE_2` | six-tile local crop route |
| 4 | `LIVESTOCK_COW` | three COW pasture positions |
| 5 | `LIVESTOCK_SHEEP` | three SHEEP pasture positions |
| 6 | `FERTILIZER_LOGISTICS` | shed, animal/feed staging, fertilizer, unblock |

Roles persist across turns and days. They are re-evaluated after workforce or
asset change and at EOD. An ordinary FEED, CARE, fertilizer, inventory, or
market opportunity does not borrow a crop worker.

The float worker has work but no wandering permission: every non-PASS action is
bound to an explicit target. A crop worker may cross its zone only when its own
zone has no due task and another zone exposes a hard interrupt.

## 4. Zones and Recurrent Routes

The eighteen crop positions are partitioned into three stable zones of six.
Within each zone, task selection uses priority class, economic value at risk,
deadline slack, Manhattan distance, and stable route index.

The worker keeps its target while moving. Completion or observable invalidation
opens the next local choice. A shared reservation set prevents two workers from
claiming the same farm entity in one turn.

Livestock positions are two three-tile clusters: the first cluster is COW and
the second is SHEEP. Animal type is part of the position contract.

## 5. Planning Horizons

```text
STRATEGIC_HORIZON: episode end for payback and terminal cutoffs
SOFT_FORECAST: current state to first monetizable output
HARD_SCHEDULE: current day and next biological service boundary
LOCAL_ROUTE: one committed target plus its path/interaction
```

No 17-day hard calendar exists. No fixed 20% route reserve or 15% exception
reserve exists.

Global replan is triggered only by EOD, workforce change, crop/pasture/animal
asset change, structural invalidation, or an infeasible hard-deadline set.
Local replan is triggered only by target completion, target invalidation,
worker unavailability, or hard interrupt.

## 6. Atomic Target Commitment

A commitment contains worker id, role, target position, intended interaction,
assigned step, zone, and optional hard-interrupt reason.

The target is stable while movement is in progress. A small distance, price, or
priority improvement does not replace it. A hard task may interrupt a lower
risk valid target; this increments `RETARGET_COUNT` and
`INTERRUPTS_BY_REASON`.

Every interaction request is checked against the next observation. A request is
not counted as output merely because it was emitted.

## 7. Interrupt Rules

Hard interrupt reason codes:

```text
ANIMAL_ESCAPE_PREVENTION
CROP_WATER_LOSS
HARVEST_TERMINAL_RISK
BLOCKING_INVENTORY_LOSS
WORKER_OR_TARGET_LEGALITY_INVALIDATION
REPEATED_ELIGIBLE_NOOP
```

CARE, fertilizer, market price, ordinary inventory clearing, and a newly ready
low-risk crop are scheduled but non-interrupting.

Lexicographic task order:

1. irreversible loss before next feasible service;
2. economic value at risk;
3. deadline proximity / remaining slack;
4. route-local completion cost.

## 8. Capacity Admission

For each relevant window `w`:

```text
AVAILABLE(w) = active worker action slots
REQUIRED(w) = hard service + route MOVE + PICKUP/PLACE
              + inventory handling + candidate actions
SLACK(w) = AVAILABLE(w) - REQUIRED(w)
```

A post-bootstrap animal is admitted only when all hard deadlines remain
feasible, minimum slack is non-negative, two FEED rounds are on hand or
affordable, cash covers animal/feed/floor, inventory has a legal path, first
output precedes payback cutoff, and forecast required actions do not exceed
observed capacity.

Observed capacity becomes available after three complete days and is the
minimum successful non-PASS action count among those days, including observed
productive, MOVE, and handling actions. Before three days, no growth beyond the
preregistered 2+2 bootstrap is admitted.

## 9. Crop Cohorts

MELON uses nine fixed positions in three spatial cohorts of three, with initial
offsets `0 / 1 / 2` days. It is the high-value batch crop.

STRAWBERRY uses eight fixed positions in two cohorts of four, with offsets
`0 / 2` days. Recurrent harvest windows at biological ages 10/12/14/16 are
protected; harvest does not imply retirement.

WHEAT uses one fixed position for the feed buffer. Its preferred harvest target
is age 4/full economic yield when serviceable. No MELON/STRAWBERRY position is
converted into additional WHEAT.

Replant occurs only after observed harvest/clearance effect and while the new
crop can reach first monetizable output before the terminal margin.

## 10. Livestock Activation

```text
BOOTSTRAP day 0–1:
  2 COW + 2 SHEEP
STAGED day ~7:
  +1 COW if capacity admission passes
STAGED day ~8:
  +1 SHEEP if capacity admission passes
```

The controller does not force 3+3 after rejection. Each decision records
`animal_activation_day`, `activation_admitted`, `activation_rejected`,
`rejection_reason`, and the capacity snapshot.

FEED and CARE are local daily tasks. COW collection follows observed yield with
an expected 48-step period after first output; SHEEP follows 72 steps.
Collection is not gated on `fed_today` because base production is scheduled by
the engine.

## 11. Fertilizer Closed Loop

```text
PASTURE
-> COLLECT_FERTILIZER
-> FERTILIZER_LOGISTICS/FLOAT inventory
-> eligible high-value crop
-> FERTILIZE only when watered_today is observed
```

Target order is MELON, early-cycle STRAWBERRY, then WHEAT only when feed is
critical. Fertilizer is never applied on an unwatered tile under a promise that
WATER may happen later.

## 12. Market Policy

Market priority is `LOW_PRIORITY`. Orders do not retarget workers.

- Sell MILK, WOOL, MELON and STRAWBERRY in daily batches.
- Sell fertilizer after the direct carried-fertilizer application path.
- Keep `2 × active_or_staged_animals` WHEAT units.
- Buy WHEAT product only to close the feed deficit.
- Buy crop seed for fixed eligible positions only.
- Do not buy for resale, trade short-term price oscillations, or buy land.

The opening is serialized under the ten-order engine limit: six hires, 2 COW,
2 SHEEP, feed and the first MELON cohort are spread across the first available
turns without violating the cash floor.

## 13. Verification and Minimal Lifecycle

The runtime retains only decision identity, local PLAN, target commitment,
post-state VERIFY, invalidation, hard-interrupt reason code, simple evidence
counters, and terminal closure. It does not implement DEFINE, SHIP, or
supersession as runtime phases and does not depend on a separate operational
planning layer.

Post-state verification covers movement, planting, watering, harvest, digging,
pasture construction, feeding, care, fertilizer collection/application,
pickup/place, hires, purchases, and sales. Repeated legal no-op outcomes
invalidate local commitments. Manual `DROP` is forbidden.

## 14. Instrumentation

Required output:

```text
FINAL_MONEY
crop_revenue
livestock_revenue
market_trading_contribution
MILK_units / WOOL_units
MELON_units / STRAWBERRY_units
WHEAT_consumed / WHEAT_sold
fertilizer_collected / fertilizer_applied
productive_actions / MOVE_actions / PASS_actions
MOVE_PER_PRODUCTIVE_ACTION
PRODUCTIVE_UTILIZATION
ON_TIME_CROP_SERVICE_RATIO
HARD_DEADLINE_MISSES
ANIMAL_ESCAPE
RETARGET_COUNT / TARGET_DWELL_TIME
DUPLICATE_ASSIGNMENTS / INTERRUPTS_BY_REASON
ROLE_CHANGES / CROSS_ZONE_ASSISTS
```

Leading indicators:

1. `ON_TIME_CROP_SERVICE_RATIO`;
2. `HARD_DEADLINE_MISSES`;
3. `HIGH_VALUE_CROP_UNITS_VS_COHORT_PLAN`;
4. `MOVE_PER_PRODUCTIVE_ACTION`;
5. `RETARGET_COUNT_PER_WORKER_DAY`.

## 15. Review Criteria

```text
BUILD_READY_FOR_REVIEW if:
  technical verification PASS
  AND mean FINAL_MONEY >= 56773
  AND ANIMAL_ESCAPE total = 0
  AND livestock output materially preserved
  AND crop serviceability materially improved

STRONG_SUCCESS: mean FINAL_MONEY >= 60000
PROJECT_SUCCESS: mean FINAL_MONEY >= 80000
```

If the gate fails, the report selects one primary bottleneck from the authorized
taxonomy and does not tune on preregistered seeds.
