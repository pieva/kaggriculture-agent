# Next Model Delta

Competitive Benchmark Batch #1 is analysis-only. No strategy or submission change is included in this document.

## Scope

Target the next code delta at structural behavior observed across both strong replay competitors, not at copied constants.

## 1. Workload-Derived Workforce Throughput

Evidence:

- truebelief (`101294736`) reaches `$86,297` with peak `12` hands, peak `50` productive tiles and `10` weed tile-days.
- Dr. Mikholae Hutchinson (`101705751`) reaches `$90,137` with peak `10` hands, peak `46` productive tiles and `11` weed tile-days.
- Our side in `101705751` peaks at `9` hands and `30` productive tiles, but accumulates `158` weed tile-days and finishes at `$38,815`.
- Alexander Sokolov (`101717011`) beats our `$24,314` with `$50,420` on one quadrant, peak `8` hands and only `15` peak productive tiles, showing that workforce must fit monetizable workload rather than maximize area.

Model delta:

- Replace calendar-shaped HIRE target with `desired_hands = f(active_crop_tiles, pasture/coop tasks, carry/logistics queue, weeds, unwatered crop count, harvest-ready count, travel distance, remaining horizon)`.
- Introduce a workload envelope for Q0+Q1: hire aggressively while marginal hand payback fits horizon and backlog is above target.

Expected effect:

- More stable crop surface after Q1.
- Lower weed and unwatered backlog.
- Higher simultaneous crop/livestock/logistics throughput.

VERIFY metrics:

- final_money on seed `0` and `421521921`;
- mean/peak crop tiles;
- productive tiles Day 12-25;
- weed tile-days;
- unwatered crop tile-days;
- productive actions per day;
- movement/productive ratio;
- idle/pass actions while backlog exists.

Counterfactuals:

- workload HIRE with conservative, medium and aggressive marginal payback thresholds;
- cap peak hands at `8`, `10`, `12`, and uncapped-by-calendar but ROI-gated;
- compare against X1.12 and X1.13 rejected variants.

Overfitting risk:

- Copying peak `8`, `10` or `12` hands directly may overspend or underserve depending on land, travel/backlog and horizon.

## 2. Deployable Capital And Land Discipline

Evidence:

- Both strong competitors buy Q1 but do not buy Q2.
- Q1 timing differs: Day 11 for truebelief, Day 14 for Dr. Mikholae Hutchinson.
- The strong paths end at `$86,297` and `$90,137` while maintaining Q0+Q1 productive capacity; Q2 is not required in this batch.
- Alexander Sokolov beats our current two-quadrant policy `$50,420` to `$24,314` while staying in `NW`, proving Q1 is not automatically positive EV.

Model delta:

- Add `deployable_capital = cash - working_capital_reserve - committed_feed_seed_logistics_cost`.
- Gate Q1/Q2, HIRE and livestock buys against deployable capital, activation cost, current quadrant monetization and remaining payback horizon.
- Keep Q2 as a conditional expansion option only after Q0+Q1 backlog is controlled and expected payback exceeds land plus activation cost.
- Permit compact Q0-only continuation when expected Q1 activation cost exceeds marginal revenue before endgame.

Expected effect:

- Avoid early land expansion that leaves insufficient operating capital.
- Avoid Q1 expansion that increases surface area but lowers monetization density.
- Convert idle cash into capacity when backlog and horizon justify it.
- Prevent Q2 from becoming a fixed target.

VERIFY metrics:

- cash available vs deployable capital by day;
- Q1/Q2 buy day and post-buy cash;
- Q0-only vs Q1 marginal revenue after the would-be expansion day;
- crop and pasture activation time after expansion;
- productive tile ramp after Q1;
- final_money and endgame liquidation.

Counterfactuals:

- Q1 gate by deployable capital only;
- Q1 gate by deployable capital plus backlog envelope;
- Q0-only continuation vs Q1 expansion on seed `1273000467`;
- Q2 disabled baseline vs conditional Q2 payback gate.

Overfitting risk:

- Over-reserving cash can recreate X1.12 underdeployment; under-reserving can repeat failed expansion/crop degradation. A Q1 bias can also lose to compact Q0 monetization.

## 3. Balanced Livestock Product Engine

Evidence:

- truebelief sells `WHEAT:268`, `FERTILIZER:138`, `MILK:134`, `MELON:108`, `WOOL:70` and ends with `9 Cow / 5 Sheep`.
- Dr. Mikholae Hutchinson sells `FERTILIZER:208`, `MILK:161`, `STRAWBERRY:132`, `WHEAT:109`, `EGG:71` and ends with `7 Cow / 4 Sheep / 2 Goose`.
- Alexander Sokolov sells `WHEAT:756`, `MILK:129`, `FERTILIZER:69`, `CARROT:59`, `WOOL:52` and ends with `4 Cow / 2 Sheep` on one quadrant.
- X1.13 livestock suppression improved some crop-health metrics but collapsed score, proving livestock should be gated, not removed.

Model delta:

- Replace fixed livestock targets with marginal animal slots scored by expected Milk/Wool/Egg/Fertilizer value, feed cost, care/feed/harvest workload, product pickup/sell bandwidth and remaining horizon.
- Keep crop SLA as a hard operational guard: livestock growth pauses when crop backlog exceeds threshold.

Expected effect:

- Preserve high-value animal products without starving crop maintenance.
- Make Cow/Sheep/Goose mix seed/market/horizon aware.
- Improve product collection and selling throughput.

VERIFY metrics:

- animal count by type and day;
- Milk/Wool/Egg/Fertilizer units sold;
- feed misses and care misses;
- animal yield left uncollected;
- crop backlog during livestock ramp;
- final_money.

Counterfactuals:

- Cow+Sheep only vs Cow+Sheep+Goose candidate;
- livestock max by workload envelope;
- product pickup priority before vs after crop recovery tasks.

Overfitting risk:

- Hardcoding `9 Cow / 5 Sheep` or adding Goose unconditionally may overfit these two replays and collapse on seeds where feed/logistics are weaker.

## Adoption Gate

A future build may adopt a delta only if it improves X1.12 on both required seeds and does not regress the benchmark diagnostics:

- seed `0` final_money above `$42,491`;
- seed `421521921` final_money above `$48,313`;
- weed tile-days materially below failing replay patterns;
- productive surface maintained after Q1;
- source/submission behavioral equivalence passes before Kaggle preparation.
