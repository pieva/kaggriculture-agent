# E13 Forensic Replay Analysis - Episode 101971376

## Scope and integrity
Independent reconstruction from `data/replays/json/101971376.json`; no other E13 analysis was read. Raw replay was not modified. Metrics are snapshot/action-derived; HIRE and BUY_LAND prices are not explicit in the action payload.

## Verified identity
- Episode: `101971376`; seed: `1630102796`; steps: `720`; module: `1.32.7`
- Player 0: Pietro Valocchi, final reward/money `$7123`
- Player 1: Harith Al-Ani, final reward/money `$133049`
- Final gap: `$125926`; ratio: `18.68x`

## First material divergence
Definition: first end-of-day where Harith's cash lead is at least `$1,000` or productive-tile lead is at least 5, with the lead subsequently persisting. This is a screening threshold, not a causal counterfactual.
- Day `1`: cash `$232` vs `$348` (gap `$116`); productive tiles `8` vs `21` (gap `13`).
- Immediately observed state: Q `NW` vs `NW`; hands `5` vs `8`; crops `4` vs `17`; pasture `4` vs `4`; weeds `0` vs `0`.
- Boundary actions at turn `23`: Pietro `HARVEST, HARVEST, HARVEST, HARVEST, SOUTH, WEST`; Harith `PASS, PASS, PASS, PASS, PASS, PASS, PASS, PASS, PASS, BUY_PRODUCT`. The observations at this boundary are post-transition; the prior turn's action is the direct event boundary.

## Revenue and action accounting
- Crop SELL value: Pietro `$38100`; Harith `$89446`.
- Milk/wool/egg SELL value: Pietro `$43933`; Harith `$65441`.
- Fertilizer SELL value: Pietro `$1385`; Harith `$16983`.
- Total explicitly priced SELL value: Pietro `$83418`; Harith `$171870`.

Action totals:
- Pietro: WEST=1723, EAST=1290, NORTH=1170, SOUTH=753, HARVEST=398, PICKUP=377, FEED=327, HIRE=292, CARE=291, PLACE=253, BUY_PRODUCT=216, PASS=205, SELL=202, DIG=91, PLANT=89, WATER=79, BUY_SEED=25, BUILD_PASTURE=18, COLLECT_FERTILIZER=16, BUY_ANIMAL=12, BUY_LAND=2
- Harith: WEST=1186, WATER=1145, NORTH=1011, EAST=769, PASS=634, SOUTH=498, SELL=383, CARE=354, COLLECT_FERTILIZER=338, FEED=333, HARVEST=314, HIRE=291, PICKUP=278, BUY_PRODUCT=169, PLANT=140, FERTILIZE=92, BUY_SEED=74, DIG=48, DROP=37, PLACE=33, BUY_ANIMAL=20, BUILD_PASTURE=17, BUY_LAND=2

## Daily timeline
The CSV contains one row per player per day, including cash, cash delta, cumulative revenue/spending, cash-relevant inventory snapshot, land, hands, surface, livestock, and crop mix. `money` is observed at hour 23.

## Gap decomposition (maximum five causes)
### Cause 1 - Capacity creation and surface
**Status:** `OBSERVED`
**Evidence:** Harith reaches more productive tiles earlier/later as shown by the daily timeline; this creates more opportunities for care, harvest and collection.
**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment -> compounded capacity.
**Confidence:** MEDIUM
**Alternative explanation:** price timing, hidden simulator rules, or action ordering may contribute; no exact causal dollar split is claimed.

### Cause 2 - Livestock product engine
**Status:** `OBSERVED`
**Evidence:** Priced livestock-product SELL value is `$65441` vs `$43933`; milk/wool/fertilizer actions and sales are separately ledgered.
**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment -> compounded capacity.
**Confidence:** HIGH
**Alternative explanation:** price timing, hidden simulator rules, or action ordering may contribute; no exact causal dollar split is claimed.

### Cause 3 - Crop mix and monetization
**Status:** `OBSERVED`
**Evidence:** Priced crop SELL value is `$89446` vs `$38100`; WHEAT/MELON/STRAWBERRY sales and market prices are in the ledger.
**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment -> compounded capacity.
**Confidence:** HIGH
**Alternative explanation:** price timing, hidden simulator rules, or action ordering may contribute; no exact causal dollar split is claimed.

### Cause 4 - Workforce and action throughput
**Status:** `INFERRED`
**Evidence:** Final hands are `7` vs `12`; total action mix is in `ACTION_LEDGER.csv`. Capacity only becomes money through completed care/logistics/sales.
**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment -> compounded capacity.
**Confidence:** MEDIUM
**Alternative explanation:** price timing, hidden simulator rules, or action ordering may contribute; no exact causal dollar split is claimed.

### Cause 5 - Compounded reinvestment timing
**Status:** `INFERRED`
**Evidence:** Cash differences permit different subsequent BUY/HIRE/LAND actions; the replay observes the sequence but cannot isolate a counterfactual contribution without rerunning the environment.
**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment -> compounded capacity.
**Confidence:** MEDIUM
**Alternative explanation:** price timing, hidden simulator rules, or action ordering may contribute; no exact causal dollar split is claimed.

## Simple-hypothesis tests
See `EVIDENCE_MATRIX.csv` for all nine classifications and counterevidence.

- `Q2 alone explains win`: **NOT_SUPPORTED** - Q2 timing is observed but must be read with throughput/revenue
- `More Hands alone explains win`: **PARTIALLY_SUPPORTED** - Final hands 7 vs 12; action counts differ materially
- `More livestock alone explains win`: **PARTIALLY_SUPPORTED** - Final cows/sheep 8/7 vs 13/4; product revenue is measurable
- `Cleaner field explains win`: **PARTIALLY_SUPPORTED** - Final weeds 6 vs 3; clean capacity is not revenue by itself
- `More surface explains win`: **PARTIALLY_SUPPORTED** - Final productive tiles 22 vs 18
- `Mostly crop revenue`: **MIXED** - Crop sales value 89446 vs 38100
- `Mostly livestock-product revenue`: **SUPPORTED** - Milk/wool/egg sales value 65441 vs 43933; fertilizer is separate at 16983 vs 1385
- `Gap starts mainly late game`: **CONTRADICTED** - First material divergence is day 1, not late game
- `Architectures economically similar`: **CONTRADICTED** - Final cash, action mix, surface and revenue composition diverge

## Local-Kaggle fidelity metrics for future work
Use per-day money deltas, explicit BUY/SELL value, market-price paths, land timing, hands/action counts, productive tile counts, crop/livestock output and end-of-day inventory snapshots. The contextual seed-0 local/Kaggle figures were not used causally here.

## Observability limits
Exact HIRE and BUY_LAND unit prices, worker idle time, intent, and counterfactual causal dollar attribution are not directly identifiable from this raw replay alone. Private inventory snapshots are player-perspective observations and some production quantities can only be inferred from action/state transitions.
