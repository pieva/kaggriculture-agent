# X1.13 Implementation Delta

## Mode

`E12_DYNAMIC_ALLOCATION_X113`

## X1.12 Rules Kept

- Day-1 diversified seed opening: Wheat + Melon + Strawberry.
- Q1 remains economically delayed rather than immediate.
- Milk, Wool, Fertilizer, crop products and excess Wheat are monetized through shed sale.
- Worker dispatcher still uses exclusive reservations to reduce same-turn collisions.
- Feed, care, animal harvest, crop harvest, water, dig, plant and shed logistics remain explicit tasks.
- X1.12 mode `E12_TRUEBELIEF_ENGINE_X112` remains unchanged and callable.

## X1.12 Rules Removed Or De-Hardcoded

- `7 Cow / 4 Sheep` is not treated as a target for X1.13.
- `Q0+Q1 only` is not treated as a permanent strategic constraint.
- Fixed day/workforce trajectory from X1.12 is replaced by workload-based HIRE in X1.13 variants C/D/E.

## New Metrics Introduced

The benchmark reconstructs per-day and episode telemetry from environment steps and actions:

- active crop tiles, pasture tiles, productive tiles;
- weeds, harvested-empty slots, unwatered crop tiles;
- productive utilization for Q0/Q1/Q2;
- pending DIG, PLANT, WATER, crop HARVEST, FEED, CARE, livestock HARVEST, COLLECT_FERTILIZER and logistics tasks;
- farmer/hands availability, productive actions, movement actions and idle/PASS;
- crop/livestock/logistics workload and backlog per worker;
- seed/livestock/product/HIRE/land spend;
- crop, Milk, Wool and Fertilizer revenue;
- final inventory, final money and livestock;
- Q2 purchase day, first productive day, time-to-activation and observed payback proxy.

## Trigger Deltas

- Livestock gate: buy the next animal only if crop backlog is inside worker capacity, feed coverage is sufficient, remaining horizon is adequate and expected marginal production can exceed acquisition plus operating drag.
- HIRE gate: hire from backlog per worker and horizon/cash reserve instead of fixed observed truebelief hand counts.
- Q2 gate: buy Q2 only if Q0+Q1 utilization is high, degradation/backlog is low, cash covers land plus working capital, remaining horizon can repay activation time, and workforce can operate the added surface.
- Assignment fix: in variant E, worker task ordering is crop-SLA first under degradation, then livestock/logistics, then normal X1.12 flow.

## Counterfactual Set

- A: X1.12 baseline unchanged.
- B: X1.13 livestock dynamic gate, Q2 disabled.
- C: B plus workload-based HIRE.
- D: C plus dynamic Q2 gate.
- E: D plus crop-SLA-first assignment when backlog degrades.
