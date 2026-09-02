# E17 Top-3 replay analysis — Copilot

## Corpus verification

All and only the nine preregistered replays were parsed. Each is valid JSON, has a distinct `info.EpisodeId`, schema/version `1`/`0.1.0`, module `1.32.7`, 720 steps, and terminal `DONE/DONE`. Agent/player mapping and terminal rewards reconcile with `data/replays/MANIFEST.md`.

## Quantitative benchmark

| Agent | Episodes | Mean score | Median score | Mean final cash | Mean peak hands |
|---|---:|---:|---:|---:|---:|
| tetsuya | 4 | 96,568.00 | 95,127.00 | $96,568.00 | 12.00 |
| OceanMix | 4 | 82,535.25 | 82,271.00 | $82,535.25 | 12.00 |
| Crop Dusta | 5 | 91,361.20 | 87,152.00 | $91,361.20 | 12.00 |

## Episode cards and temporal quadrant table

`Q1/Q2` are reported as the observed unlock order after NW: NE is Q1 and SW is Q2 whenever those are the first and second expansions. SE was not required by the observed 3Q runs. `unplanted` is final empty plus WEED tiles; animal-dedicated tiles are PASTURE plus COOP, not inferred animal occupancy.

### 104527555 — tetsuya (player 0)

OBSERVED: score `81,050`, final cash `$81,050`, peak/terminal hands `12/11`, movement requests `3415`, status `DONE`. Q1 NE `{'step': 169, 'day': 7}`, Q2 SW `{'step': 241, 'day': 10}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 17 | 7 | 0 | 7 | WHEAT:1 |
| NE | 25 | 20 | 2 | 0 | 2 | CARROT:1, WHEAT:2 |
| SW | 25 | 19 | 5 | 1 | 6 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=1, BUILD_PASTURE=14, BUY_ANIMAL=9, BUY_LAND=2, BUY_PRODUCT=300, BUY_SEED=38, CARE=311, COLLECT_FERTILIZER=341, DIG=33, DROP=206, EAST=871, FEED=324, FERTILIZE=55, HARVEST=434, HIRE=310, NORTH=816, PASS=1251, PICKUP=134, PLACE=15, PLANT=242, SELL=473, SOUTH=641, WATER=962, WEST=1087.

### 104541810 — tetsuya (player 0)

OBSERVED: score `109,204`, final cash `$109,204`, peak/terminal hands `12/11`, movement requests `3344`, status `DONE`. Q1 NE `{'step': 169, 'day': 7}`, Q2 SW `{'step': 241, 'day': 10}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 15 | 7 | 0 | 7 | WHEAT:3 |
| NE | 25 | 15 | 2 | 1 | 3 | WHEAT:7 |
| SW | 25 | 19 | 5 | 0 | 5 | WHEAT:1 |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=1, BUILD_PASTURE=14, BUY_ANIMAL=9, BUY_LAND=2, BUY_PRODUCT=257, BUY_SEED=29, CARE=311, COLLECT_FERTILIZER=343, DIG=40, DROP=219, EAST=862, FEED=320, FERTILIZE=81, HARVEST=433, HIRE=310, NORTH=824, PASS=1335, PICKUP=149, PLACE=15, PLANT=215, SELL=441, SOUTH=581, WATER=913, WEST=1077.

### 104543983 — Crop Dusta (player 0)

OBSERVED: score `83,634`, final cash `$83,634`, peak/terminal hands `12/12`, movement requests `3958`, status `DONE`. Q1 NE `{'step': 155, 'day': 6}`, Q2 SW `{'step': 218, 'day': 9}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 17 | 8 | 0 | 8 | — |
| NE | 25 | 19 | 2 | 4 | 6 | — |
| SW | 25 | 19 | 4 | 0 | 4 | CARROT:1, STRAWBERRY:1 |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=4, BUILD_PASTURE=14, BUY_ANIMAL=19, BUY_LAND=2, BUY_PRODUCT=200, BUY_SEED=106, CARE=303, COLLECT_FERTILIZER=360, DIG=44, DROP=32, EAST=795, FEED=320, FERTILIZE=155, HARVEST=428, HIRE=294, NORTH=1150, PASS=236, PICKUP=237, PLACE=88, PLANT=204, SELL=337, SOUTH=898, WATER=1030, WEST=1115.

### 104543983 — tetsuya (player 1)

OBSERVED: score `76,264`, final cash `$76,264`, peak/terminal hands `12/11`, movement requests `3399`, status `DONE`. Q1 NE `{'step': 169, 'day': 7}`, Q2 SW `{'step': 241, 'day': 10}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 18 | 7 | 0 | 7 | — |
| NE | 25 | 23 | 1 | 1 | 2 | — |
| SW | 25 | 19 | 2 | 4 | 6 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=5, BUILD_PASTURE=10, BUY_ANIMAL=9, BUY_LAND=2, BUY_PRODUCT=300, BUY_SEED=34, CARE=309, COLLECT_FERTILIZER=333, DIG=34, DROP=199, EAST=826, FEED=318, FERTILIZE=103, HARVEST=471, HIRE=309, NORTH=835, PASS=1272, PICKUP=151, PLACE=15, PLANT=204, SELL=473, SOUTH=646, WATER=890, WEST=1092.

### 104547425 — OceanMix (player 0)

OBSERVED: score `114,361`, final cash `$114,361`, peak/terminal hands `12/11`, movement requests `3207`, status `DONE`. Q1 NE `{'step': 151, 'day': 6}`, Q2 SW `{'step': 266, 'day': 11}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 15 | 10 | 0 | 10 | — |
| NE | 25 | 18 | 7 | 0 | 7 | — |
| SW | 25 | 25 | 0 | 0 | 0 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=1, BUILD_PASTURE=17, BUY_ANIMAL=13, BUY_LAND=2, BUY_PRODUCT=72, BUY_SEED=52, CARE=372, COLLECT_FERTILIZER=378, DIG=37, DROP=18, EAST=695, FEED=364, FERTILIZE=75, HARVEST=467, HIRE=287, NORTH=991, PASS=697, PICKUP=155, PLACE=110, PLANT=249, SELL=262, SOUTH=550, WATER=1102, WEST=971.

### 104547425 — Crop Dusta (player 1)

OBSERVED: score `106,328`, final cash `$106,328`, peak/terminal hands `12/12`, movement requests `4001`, status `DONE`. Q1 NE `{'step': 122, 'day': 5}`, Q2 SW `{'step': 199, 'day': 8}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 14 | 9 | 0 | 9 | WHEAT:2 |
| NE | 25 | 19 | 6 | 0 | 6 | — |
| SW | 25 | 20 | 5 | 0 | 5 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_PASTURE=20, BUY_ANIMAL=20, BUY_LAND=2, BUY_PRODUCT=179, BUY_SEED=92, CARE=340, COLLECT_FERTILIZER=392, DIG=40, DROP=29, EAST=846, FEED=361, FERTILIZE=168, HARVEST=396, HIRE=304, NORTH=1174, PASS=307, PICKUP=255, PLACE=108, PLANT=188, SELL=296, SOUTH=853, WATER=1025, WEST=1128.

### 104564762 — Crop Dusta (player 1)

OBSERVED: score `87,152`, final cash `$87,152`, peak/terminal hands `12/12`, movement requests `4147`, status `DONE`. Q1 NE `{'step': 122, 'day': 5}`, Q2 SW `{'step': 201, 'day': 8}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 16 | 5 | 0 | 5 | WHEAT:4 |
| NE | 25 | 15 | 5 | 0 | 5 | TOMATO:5 |
| SW | 25 | 18 | 0 | 5 | 5 | TOMATO:2 |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=5, BUILD_PASTURE=10, BUY_ANIMAL=15, BUY_LAND=2, BUY_PRODUCT=214, BUY_SEED=90, CARE=276, COLLECT_FERTILIZER=324, DIG=39, DROP=32, EAST=810, FEED=286, FERTILIZE=158, HARVEST=436, HIRE=304, NORTH=1287, PASS=311, PICKUP=211, PLACE=71, PLANT=199, SELL=324, SOUTH=929, WATER=1121, WEST=1121.

### 104577270 — OceanMix (player 1)

OBSERVED: score `86,580`, final cash `$86,580`, peak/terminal hands `12/11`, movement requests `3148`, status `DONE`. Q1 NE `{'step': 151, 'day': 6}`, Q2 SW `{'step': 266, 'day': 11}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 16 | 7 | 2 | 9 | — |
| NE | 25 | 18 | 7 | 0 | 7 | — |
| SW | 25 | 25 | 0 | 0 | 0 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=3, BUILD_PASTURE=17, BUY_ANIMAL=10, BUY_LAND=2, BUY_PRODUCT=70, BUY_SEED=45, CARE=333, COLLECT_FERTILIZER=332, DIG=43, DROP=19, EAST=709, FEED=326, FERTILIZE=62, HARVEST=467, HIRE=290, NORTH=961, PASS=918, PICKUP=131, PLACE=121, PLANT=243, SELL=292, SOUTH=548, WATER=1142, WEST=930.

### 104578185 — tetsuya (player 0)

OBSERVED: score `119,754`, final cash `$119,754`, peak/terminal hands `12/11`, movement requests `3351`, status `DONE`. Q1 NE `{'step': 169, 'day': 7}`, Q2 SW `{'step': 241, 'day': 10}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 18 | 7 | 0 | 7 | — |
| NE | 25 | 19 | 2 | 0 | 2 | CARROT:2, WHEAT:2 |
| SW | 25 | 19 | 5 | 1 | 6 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=1, BUILD_PASTURE=14, BUY_ANIMAL=9, BUY_LAND=2, BUY_PRODUCT=181, BUY_SEED=32, CARE=300, COLLECT_FERTILIZER=330, DIG=42, DROP=192, EAST=848, FEED=312, FERTILIZE=125, HARVEST=437, HIRE=314, NORTH=824, PASS=1412, PICKUP=161, PLACE=15, PLANT=217, SELL=339, SOUTH=598, WATER=919, WEST=1081.

### 104578185 — Crop Dusta (player 1)

OBSERVED: score `114,881`, final cash `$114,881`, peak/terminal hands `12/12`, movement requests `4204`, status `DONE`. Q1 NE `{'step': 155, 'day': 6}`, Q2 SW `{'step': 212, 'day': 8}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 16 | 8 | 0 | 8 | TOMATO:1 |
| NE | 25 | 15 | 9 | 0 | 9 | STRAWBERRY:1 |
| SW | 25 | 23 | 0 | 0 | 0 | TOMATO:2 |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_PASTURE=17, BUY_ANIMAL=17, BUY_LAND=2, BUY_PRODUCT=226, BUY_SEED=67, CARE=288, COLLECT_FERTILIZER=357, DIG=51, DROP=34, EAST=843, FEED=305, FERTILIZE=111, HARVEST=390, HIRE=295, NORTH=1251, PASS=203, PICKUP=221, PLACE=80, PLANT=143, SELL=328, SOUTH=930, WATER=1030, WEST=1180.

### 104586335 — Crop Dusta (player 0)

OBSERVED: score `64,811`, final cash `$64,811`, peak/terminal hands `12/12`, movement requests `4040`, status `DONE`. Q1 NE `{'step': 122, 'day': 5}`, Q2 SW `{'step': 203, 'day': 8}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 18 | 5 | 2 | 7 | — |
| NE | 25 | 21 | 1 | 3 | 4 | — |
| SW | 25 | 21 | 0 | 3 | 3 | CARROT:1 |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=8, BUILD_PASTURE=6, BUY_ANIMAL=14, BUY_LAND=2, BUY_PRODUCT=178, BUY_SEED=129, CARE=255, COLLECT_FERTILIZER=310, DIG=40, DROP=27, EAST=779, FEED=271, FERTILIZE=154, HARVEST=482, HIRE=304, NORTH=1190, PASS=379, PICKUP=193, PLACE=42, PLANT=258, SELL=264, SOUTH=939, WATER=1164, WEST=1132.

### 104586335 — OceanMix (player 1)

OBSERVED: score `51,238`, final cash `$51,238`, peak/terminal hands `12/10`, movement requests `2974`, status `DONE`. Q1 NE `{'step': 151, 'day': 6}`, Q2 SW `{'step': 266, 'day': 11}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 19 | 6 | 0 | 6 | — |
| NE | 25 | 18 | 7 | 0 | 7 | — |
| SW | 25 | 25 | 0 | 0 | 0 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=1, BUILD_PASTURE=14, BUY_ANIMAL=9, BUY_LAND=2, BUY_PRODUCT=67, BUY_SEED=49, CARE=279, COLLECT_FERTILIZER=318, DIG=42, DROP=15, EAST=648, FEED=269, FERTILIZE=70, HARVEST=458, HIRE=274, NORTH=898, PASS=862, PICKUP=119, PLACE=116, PLANT=255, SELL=245, SOUTH=544, WATER=1155, WEST=884.

### 104586487 — OceanMix (player 0)

OBSERVED: score `77,962`, final cash `$77,962`, peak/terminal hands `12/10`, movement requests `2974`, status `DONE`. Q1 NE `{'step': 151, 'day': 6}`, Q2 SW `{'step': 266, 'day': 11}`, Q3 SE `None`. UNKNOWN: animal escapes (the replay exposes no event/state field).

| Quadrant | Unlocked tiles | Unplanted final | Pasture | Coop | Animal-dedicated | Crops final |
|---|---:|---:|---:|---:|---:|---|
| NW | 25 | 19 | 6 | 0 | 6 | — |
| NE | 25 | 18 | 7 | 0 | 7 | — |
| SW | 25 | 25 | 0 | 0 | 0 | — |
| SE | 0 | 0 | 0 | 0 | 0 | — |

DERIVED requested actions: BUILD_COOP=1, BUILD_PASTURE=14, BUY_ANIMAL=9, BUY_LAND=2, BUY_PRODUCT=67, BUY_SEED=49, CARE=279, COLLECT_FERTILIZER=318, DIG=42, DROP=15, EAST=648, FEED=269, FERTILIZE=70, HARVEST=458, HIRE=274, NORTH=898, PASS=862, PICKUP=119, PLACE=116, PLANT=255, SELL=245, SOUTH=544, WATER=1155, WEST=884.

## Cross-agent findings

OBSERVED: all Top-3 agents reach a 3-quadrant footprint in the sampled corpus; terminal cash and score vary materially across opponent/seed. OBSERVED: no tetsuya–OceanMix head-to-head occurs, so this corpus cannot establish their causal ordering. INFERRED: earlier expansion combined with serviceable density, rather than terminal cash alone, is a high-value factor for a controlled follow-up.

## Gap versus Copilot V2 derivative baseline

OBSERVED: Copilot V2 is an open-loop, Codex-derived 3Q action table with no executed ledger and no independently attributable Q ownership. GAP (HIGH, implementation/telemetry): it cannot measure the per-day observed milestones above while running; add only an offline requested/executed ledger in a future independently authored experiment. GAP (MEDIUM, policy): the replay Top-3 agents show varied Q1/Q2 timing across seeds/opponents, whereas V2 has fixed timing. Missing information: action execution outcome and opponent intent prevent causal attribution.

## Prioritized E17 hypothesis

**E17-H1 — milestone-gated expansion telemetry (HIGH information value).** Mechanism: distinguish whether Q1/Q2 timing and workforce peaks correlate with final score after controlling by fixed seed/seat. Change one factor only: add an offline requested/executed milestone ledger to a new independent baseline; do not change routing. Baseline/control: identical independently authored policy without the ledger. Use at least 6 preregistered seeds with balanced seats. Primary metric: score; diagnostics: final cash, Q unlock step, peak hands, active crop/pasture/coop tiles, weeds, and execution ratios. Promote only if parity is byte/behavioral for actions and the ledger is complete; rollback if instrumentation changes actions or omits required fields. Risk: low policy risk, medium engineering cost. This report does not implement it.

## Limits

UNKNOWN: requested actions are not execution outcomes; pasture/coop tiles do not expose animal occupancy/species by coordinate; replay evidence is observational and must not be used online. No other-agent MODEL_SPEC, E17 output, or routine was used by this Copilot analysis.
