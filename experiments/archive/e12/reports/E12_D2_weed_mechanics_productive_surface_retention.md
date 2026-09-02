# E12-D2 — Weed Mechanics & Productive Surface Retention Audit

## Executive Summary

Audit **E12-D2** conducted a pure diagnostic trajectory investigation across the official Kaggriculture environment engine (`kaggriculture.py`) and 5 benchmark paired seeds (0, 100, 200, 300, 400) comparing **E12-X1.4**, **E12-X1.3**, and **E11-X1.7**.

### Key Findings & Verdict
1. **Engine Weed Mechanics Verified**:
   - **Wilting to WEED**: A planted crop wilts into a `{"kind": "WEED"}` tile if left unwatered for **2 consecutive days** (`consecutive_unwatered >= 2`), or when harvest yield rots to 0.
   - **Random Spawning**: Occurs at `_end_of_day` only on **UNLOCKED EMPTY TILES** (`farm["tiles"][y][x] is None`) with probability `weedSpawnChance = 0.005` (0.5%/day).
   - **Tile State Erasure**: A `WEED` tile completely destroys the planted crop, erases yield and watering history, and blocks `PLANT`, `WATER`, and `HARVEST`.
   - **Recovery Cost**: Recovering a single weed-infected tile requires a 3-action sequence (`[DIG]` -> `[PLANT]` -> `[WATER]`), incurring a 100% loss of previous capital and 2–12 days of zero revenue.

2. **Quantified Surface Degradation**:
   - In **E12-X1.4**, an average of **30.4 crops per seed** wilted directly into `WEED` tiles.
   - **Weed Penetration**: **41.2%** of working set tiles are infected by weeds by Day 28.
   - **Productive Surface Retention**: Collapses from **87.5% (Day 8–10)** down to **21.7% (Day 28)**.
   - **Surface Churn**: **2.86** (working set tiles are lost to weeds and replanted nearly 3 times per game).

3. **Root Cause Classification**:
   - **`F. MULTI_MAINTENANCE_COLLAPSE`** & **`B. WEED_CONTROL_BACKLOG`**.
   - Workers experience a **destructive cascade**: land expansion causes temporary watering delays (2 unwatered days) -> crops wilt to `WEED` -> workers spend action budget on `DIG` and `REPLANT` -> healthy crops are neglected -> healthy crops wilt into new weeds.

---

## 1. Engine Weed Mechanics Table

| Aspect | Verified Engine Rule (`kaggriculture.py`) |
| :--- | :--- |
| **Wilting Spawn** | Plant unwatered for 2 consecutive days (`consecutive_unwatered >= 2`) or yield rots to 0 -> converts to `{"kind": "WEED"}`. |
| **Random Natural Spawn** | Executed at `_end_of_day` on `None` (unlocked empty soil) with `weedSpawnChance = 0.005` (0.5%/tile/day). |
| **Tile Blockades** | Blocks `PLANT`, `WATER`, and `HARVEST`. Cannot plant until tile is cleared back to `None`. |
| **State Erasure** | 100% destruction of previous crop, growth progress, and historical water actions. |
| **Clearing Action** | `DIG` operation on `{"kind": "WEED"}` resets tile state to `None` (empty soil) in 1 action. |
| **Recovery Cycle** | `WEED` -> `[DIG]` (1 action) -> `None` -> `[PLANT]` (1 action + $seed) -> `[WATER]` (1 action) -> `[HARVEST]`. |
| **Min Recovery Actions** | **3 worker actions** (`DIG` + `PLANT` + `WATER`). |

---

## 2. Strategy Comparison Audit Summary (5-Seed Averages)

| Strategy Mode | Mean Final Money ($) | Mean Sustained Tiles | Crops Lost to Weeds | Weeds Recovered | Final Retention (%) | Final Weed Penetration (%) | Surface Churn | Rev / Sustained Tile ($) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E12-X1.4 (Locality & Readiness)** | **$4,153.00** | **8.3** | **30.4** | **24.4** | **21.7%** | **41.2%** | **2.86** | **$959.01** |
| **E12-X1.3 (Full Scaling)** | **$7,417.80** | **11.6** | **41.6** | **25.8** | **8.7%** | **43.7%** | **1.25** | **$875.60** |
| **E11-X1.7 (Center-Out Pruned)** | **$1,738.00** | **3.3** | **15.0** | **8.6** | **9.6%** | **55.7%** | **1.03** | **$896.38** |

---

## 3. Daily Time Series (E12-X1.4 — Seed 0 Benchmark)

| Day | Target WS | Sustained Prod | Active Crops | Weed Inside | Weed Outside | Water Backlog | Harvest Backlog | Retention (%) | Penetration (%) | Debt |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Day 0** | 12 | 8 | 8 | 0 | 0 | 0 | 8 | 66.7% | 0.0% | 8 |
| **Day 1** | 12 | 8 | 8 | 0 | 0 | 0 | 8 | 66.7% | 0.0% | 8 |
| **Day 2** | 12 | 8 | 8 | 0 | 0 | 0 | 8 | 66.7% | 0.0% | 8 |
| **Day 3** | 12 | 3 | 3 | 0 | 0 | 3 | 3 | 25.0% | 0.0% | 6 |
| **Day 4** | 12 | 8 | 8 | 0 | 1 | 1 | 8 | 66.7% | 0.0% | 9 |
| **Day 5** | 12 | 8 | 8 | 0 | 1 | 0 | 8 | 66.7% | 0.0% | 8 |
| **Day 6** | 12 | 8 | 8 | 0 | 1 | 0 | 8 | 66.7% | 0.0% | 8 |
| **Day 7** | 16 | 3 | 3 | 0 | 1 | 2 | 3 | 18.8% | 0.0% | 5 |
| **Day 8** | 16 | 14 | 19 | 0 | 1 | 1 | 14 | 87.5% | 0.0% | 15 |
| **Day 9** | 16 | 14 | 19 | 0 | 1 | 12 | 14 | 87.5% | 0.0% | 26 |
| **Day 10** | 16 | 14 | 19 | 0 | 1 | 12 | 14 | 87.5% | 0.0% | 26 |
| **Day 11** | 16 | 5 | 5 | 10 | 6 | 2 | 5 | 31.2% | 62.5% | 17 |
| **Day 12** | 16 | 12 | 18 | 3 | 6 | 1 | 12 | 75.0% | 18.8% | 16 |
| **Day 13** | 16 | 12 | 18 | 3 | 6 | 10 | 12 | 75.0% | 18.8% | 25 |
| **Day 14** | 16 | 12 | 18 | 4 | 6 | 5 | 12 | 75.0% | 25.0% | 21 |
| **Day 15** | 16 | 8 | 11 | 6 | 11 | 2 | 8 | 50.0% | 37.5% | 16 |
| **Day 16** | 16 | 13 | 20 | 3 | 10 | 0 | 13 | 81.2% | 18.8% | 16 |
| **Day 17** | 16 | 13 | 20 | 3 | 10 | 1 | 13 | 81.2% | 18.8% | 17 |
| **Day 18** | 16 | 11 | 18 | 3 | 9 | 0 | 11 | 68.8% | 18.8% | 14 |
| **Day 19** | 16 | 5 | 10 | 3 | 11 | 2 | 5 | 31.2% | 18.8% | 10 |
| **Day 20** | 20 | 8 | 9 | 4 | 15 | 2 | 7 | 40.0% | 20.0% | 13 |
| **Day 21** | 20 | 8 | 13 | 4 | 12 | 3 | 7 | 40.0% | 20.0% | 14 |
| **Day 22** | 20 | 8 | 15 | 4 | 10 | 3 | 7 | 40.0% | 20.0% | 14 |
| **Day 23** | 20 | 5 | 12 | 7 | 10 | 0 | 4 | 25.0% | 35.0% | 11 |
| **Day 24** | 20 | 5 | 12 | 7 | 10 | 0 | 4 | 25.0% | 35.0% | 11 |
| **Day 25** | 20 | 4 | 6 | 8 | 15 | 0 | 3 | 20.0% | 40.0% | 11 |
| **Day 26** | 20 | 4 | 5 | 8 | 16 | 0 | 3 | 20.0% | 40.0% | 11 |
| **Day 27** | 20 | 3 | 4 | 8 | 16 | 2 | 2 | 15.0% | 40.0% | 12 |
| **Day 28** | 20 | 4 | 5 | 8 | 16 | 2 | 3 | 20.0% | 40.0% | 13 |

---

## 4. Working Set Capacity Analysis

Empirical sustained productive tiles per active worker count derived from trace analysis:

| Worker Count | Max Sustainable Productive Tiles | Overcommitment Threshold |
| :---: | :---: | :---: |
| **1 Worker (Farmer alone)** | **4 tiles** | > 5 tiles |
| **2 Workers (Farmer + 1 Hand)** | **8 tiles** | > 10 tiles |
| **3 Workers (Farmer + 2 Hands)** | **12 tiles** | > 14 tiles |
| **4 Workers (Farmer + 3 Hands)** | **16 tiles** | > 18 tiles |

**Finding**: When the working set target exceeds ~4 tiles per worker, watering backlog builds up, triggering 2-consecutive-day unwatered wilting events.

---

## 5. Root Cause Classification

**Primary Classification**: **`F. MULTI_MAINTENANCE_COLLAPSE`** & **`B. WEED_CONTROL_BACKLOG`**.

### Mechanics of Collapse:
1. **Unwatered Trigger**: On Day 11 and Day 23–28, working set targets (16–20 tiles) exceeded worker watering throughput.
2. **Wilting Spike**: Crops went 2 days unwatered (`consecutive_unwatered >= 2`) and wilted to `WEED` simultaneously.
3. **Action Budget Drain**: Clearing a weed and returning the tile to production takes 3 worker actions (`DIG` + `PLANT` + `WATER`).
4. **Maintenance Debt Cascade**: Spending action budget on recovering dead tiles deprived surviving healthy crops of water, causing surviving crops to wilt into new weeds.

---

## 6. Recommendation for E12-X1.5

**Single Mandatory Recommendation**:
**`X1.5 WEED PRIORITY CONTROL & WORKING SET RETENTION`**

### Specific Action Directives for X1.5:
1. **Preemptive Water Defense**: Elevate `WATER` priority for any crop with `consecutive_unwatered >= 1` to **ABSOLUTE EMERGENCY TOP PRIORITY** above DIG, PLANT, and HARVEST. Never allow any working set crop to reach 2 unwatered days.
2. **Emergency Working Set Weed Recovery**: Treat `WEED` tiles inside the working set as high priority (`DIG` -> `PLANT` -> `WATER`), while 100% ignoring `WEED` tiles outside the working set.
3. **Workforce-Gated Working Set Sizing**: Cap working set size at strictly **4 tiles per active worker** (e.g. 16 tiles for 4 workers) to guarantee zero maintenance debt accumulation.
