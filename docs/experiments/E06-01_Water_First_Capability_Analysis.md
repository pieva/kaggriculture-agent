# E06-01 — Capability & Scheduling Analysis: Water-First Priority (`WATER > HARVEST > PLANT`)

**Date:** 2026-08-25  
**Author:** Google Antigravity  
**Phase:** DEFINE  
**Target File:** `docs/experiments/E06-01_Water_First_Capability_Analysis.md`  
**Status:** Complete — Recommendation: **`GO`**

---

## 1. Experimental Question

Does the residual operational starvation issue observed in E05 depend, at least in part, on `WATER` being executed after `HARVEST` and `PLANT`? 

Specifically, can a **Water-First** policy (`WATER > HARVEST > PLANT`) eliminate or significantly reduce starvation, end-of-day unwatered tiles, and weed conversions without introducing an economic regression that makes the overall strategy worse than E05?

---

## 2. E05 Baseline

In E05 (`HIRENWClusterROIAgent`), we scaled the productive footprint to 9 tiles in a 3×3 NW cluster `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` using 1 Farmer Principal (4 tiles) and 1 daily Farm Hand ($1/day, 5 tiles).

### Local Benchmark Performance (30 Episodes, 720 steps each)
- **Strategy Class:** `HIRENWClusterROIAgent`
- **Managed Footprint:** 9 tiles (3×3 NW cluster)
- **Workers:** 1 Farmer Principal + 1 daily Farm Hand ($1/day HIRE at `hour == 0`)
- **Spatial Partitioning:** Fixed 4:5 (Farmer: 4 tiles, Hand 1: 5 tiles)
- **Task Priority Policy:** `HARVEST > PLANT > WATER`
- **Completion Rate:** `100.00%`
- **Disqualification Rate:** `0.00%`
- **Overall Win Rate:** `100.00%` (30W / 0L / 0D vs `pass`, `random`, `starter`)
- **Mean Final Money:** **`$21568.93 ± $361.25`**
- **Median Final Money:** **`$21442.00`**
- **Total Weed Conversions:** **`176`** (5.87 weeds/episode)
- **Mean Unwatered End-of-Day Ratio:** **`3.33%`**
- **Agent Mean Turn Latency:** `0.0924 ms/turn`

### Kaggle External Validation Status
- **Kaggle Submission:** `submission/submission.py` (`HIRENWClusterROIAgent`)
- **Observed & Stabilized Kaggle Skill Rating:** **`439.7`** (External Validation Passed, `+161.4` points / `+57.99%` vs E03 rating of `278.3`).

### E05 Review Finding
While E05 achieved outstanding economic expansion (`+$10336.46` / `+92.02%` vs E04), the REVIEW phase classified the operational status as **`STARVATION REDUCED BUT UNRESOLVED`**. Weed conversions fell from 238 to 176 (`-26.05%`), but crop mortality events persisted due to priority conflicts on Hand 1's 5-tile partition during peak harvest days.

---

## 3. Current Scheduling Logic (`HARVEST > PLANT > WATER`)

The E05 worker decision engine is implemented in `src/agricola/strategy/hire_nw_cluster_roi.py` within `_compute_worker_action()`:

```python
if harvest_candidate_tiles:
    target_pos = select_nearest(harvest_candidate_tiles)
    task = "HARVEST"
elif empty_tiles and target_seeds_owned > 0:
    target_pos = select_nearest(empty_tiles)
    task = "PLANT"
elif water_candidate_tiles:
    target_pos = select_nearest(water_candidate_tiles)
    task = "WATER"
```

### Operational Execution Cycle per Worker
1. **Harvest Check:** Worker checks assigned tiles for mature crops (`age >= max_yield_day`). If found, targets the nearest harvestable tile.
2. **Plant Check:** If no harvests are ready, worker checks assigned tiles for empty unplanted tiles. If seeds are available in inventory/virtual allocation, targets nearest empty tile.
3. **Water Check:** Only if no mature crops exist AND no empty tiles can be planted does the worker check for unwatered growing plants (`watered_today == False`).

---

## 4. Environment Mechanics Relevant to WATER

In the Kaggriculture environment:
1. **Daily Water Reset:** At `hour == 0` of every day, the `watered_today` boolean flag on all planted tiles resets to `False`.
2. **Water Requirement for Growth:** Planted crops require 1 watering action per day (`WATER` action while standing on tile) to progress towards `max_yield_day`.
3. **Starvation Penalty & Weed Conversion:** If a plant goes unwatered during a day (reaching `hour == 23` with `watered_today == False`), its growth stalls. Consecutive unwatered days trigger plant death, transforming the tile into a `WEED`.
4. **Impact of `WEED` Tiles:**
   - A `WEED` tile produces **$0 revenue**.
   - A `WEED` tile **permanently blocks planting** until cleared by a `DIG` action.
   - In E05, `DIG` is disabled, meaning any tile converted to `WEED` is permanently lost for the remainder of the 30-day episode.

---

## 5. Relationship Between Watering, Starvation and Weeds

Why did 176 weed conversions occur in E05 despite having 2 active workers?

### Operational Analysis of Hand 1 (5 Tiles)
- Hand 1 is assigned 5 tiles: `{(4,2), (3,2), (2,4), (2,3), (2,2)}`.
- Each day consists of 24 hours (24 action steps per worker).
- On peak harvest days (e.g. day 3, 6, 9... when CARROT matures):
  - Hand 1 spends 5 steps traveling to mature tiles + 5 steps harvesting them = 10 steps.
  - Hand 1 spends 5 steps moving to empty tiles + 5 steps planting new seeds = 10 steps.
  - Total time spent on HARVEST and PLANT = **20 steps**.
  - Remaining time in the 24-hour day = **4 steps**.
- If Hand 1 also has 3 or 4 growing plants needing water on other tiles, traveling to those tiles (Manhattan distance) and executing `WATER` requires 6–8 steps.
- Because `HARVEST` and `PLANT` are evaluated before `WATER`, watering is deferred to the final hours of the day (hours 20–23).
- Hand 1 runs out of hours before watering all growing tiles.
- The unwatered plants reach `hour == 23` unwatered, leading to repeated starvation and `WEED` conversions.

**Key Insight:** Starvation in E05 is not primarily caused by lack of overall physical capacity, but by **temporal deferral**: `WATER` is pushed to the end of the day after harvesting and replanting, causing worker time budget depletion.

---

## 6. Candidate E06 Intervention (`WATER > HARVEST > PLANT`)

We propose to evaluate a pure scheduling priority swap in `_compute_worker_action()`:

```python
if water_candidate_tiles:
    target_pos = select_nearest(water_candidate_tiles)
    task = "WATER"
elif harvest_candidate_tiles:
    target_pos = select_nearest(harvest_candidate_tiles)
    task = "HARVEST"
elif empty_tiles and target_seeds_owned > 0:
    target_pos = select_nearest(empty_tiles)
    task = "PLANT"
```

### Is this intervention isolated and controlled?
**YES.** This modification changes a single, isolated logic block inside worker task selection. All other components of the agent architecture remain 100% untouched.

---

## 7. Controlled Variables

To ensure strict scientific control, the following variables will remain **100% frozen** relative to E05:

| Variable | E05 Value | E06 Proposed Value | Status |
| :--- | :--- | :--- | :--- |
| **Managed Footprint** | 9 tiles (3×3 NW cluster) | 9 tiles (3×3 NW cluster) | Frozen |
| **Cluster Location** | `{(x,y) \| x ∈ [2,4], y ∈ [2,4]}` | `{(x,y) \| x ∈ [2,4], y ∈ [2,4]}` | Frozen |
| **Worker Allocation** | 1 Farmer + 1 Daily Hand | 1 Farmer + 1 Daily Hand | Frozen |
| **HIRE Lifecycle & Cost** | Hour 0, $1/day cost | Hour 0, $1/day cost | Frozen |
| **Spatial Partitioning** | Fixed 4:5 (Farmer: 4, Hand: 5) | Fixed 4:5 (Farmer: 4, Hand: 5) | Frozen |
| **Crop Selection Model** | E03 ROI/day formula (`yield=2.0`) | E03 ROI/day formula (`yield=2.0`) | Frozen |
| **Liquidation Policy** | Immediate shed sale on market phase | Immediate shed sale on market phase | Frozen |
| **Movement & Pathfinding** | Nearest Manhattan distance | Nearest Manhattan distance | Frozen |
| **Episode Length** | 720 steps (30 days) | 720 steps (30 days) | Frozen |
| **Opponent Set** | `['pass', 'random', 'starter']` | `['pass', 'random', 'starter']` | Frozen |
| **Benchmark Protocol & Seeds** | 30 episodes, seeds 0–9 per opp | 30 episodes, seeds 0–9 per opp | Frozen |

---

## 8. Potential Confounders

We have identified three potential confounding mechanisms that could complicate the evaluation:

1. **Crop Rotation Delay (Cycle Starvation):** Prioritizing `WATER` over `HARVEST` means mature crops will sit unharvested on tiles while the worker waters other tiles. This delays `PLANT` of the next crop cycle. Over a 30-day episode, delaying planting by 4–8 hours per cycle may cause the agent to miss 1–2 complete harvest cycles across the 9 tiles, resulting in lower gross revenue.
2. **Seed Capital Deadlock:** Seed purchases occur during the Market Phase based on empty tile counts. If planting is delayed due to water prioritization, purchased seeds sit idle in inventory while capital is locked.
3. **Spatial Routing Inefficiency (Ping-Ponging):** Under `HARVEST > PLANT > WATER`, a worker harvests and replants a tile in a single localized visit. Under `WATER > HARVEST > PLANT`, a worker may walk to tile A to water it, walk to tile B to harvest, and walk back to tile A to plant, increasing total Manhattan travel distance per day.

---

## 9. Primary Metrics

To evaluate E06 against E05, we establish two primary metrics:

1. **Total Weed Conversions (Primary Operational Metric):**
   - Total count of tiles converting to `WEED` across 30 benchmark episodes.
   - **E05 Baseline:** `176` weeds (5.87 weeds/ep).
   - **Goal:** Statistically significant reduction towards `0`.

2. **Mean Final Money (Primary Economic Metric):**
   - Mean final accumulated money across 30 benchmark episodes.
   - **E05 Baseline:** `$21568.93 ± $361.25`.
   - **Goal:** Non-inferiority to E05 (no economic regression due to rotation delays).

---

## 10. Secondary / Diagnostic Metrics

To diagnose operational dynamics and trace potential trade-offs:

1. **Mean Unwatered End-of-Day Ratio (%):** Percentage of days with unwatered plants at `hour == 23`. (E05 Baseline: `3.33%`).
2. **Harvest Yield Count / Harvest Cycles Completed:** Total number of successful harvests completed across the episode to detect crop rotation delay.
3. **Completion Rate (%):** Percentage of episodes completed without crash/timeout. (Target: `100.00%`).
4. **Disqualification Rate (%):** Percentage of invalid episodes. (Target: `0.00%`).
5. **Agent Mean Turn Latency (ms):** Decision time per step. (Target: `< 1.0 ms`).

---

## 11. Economic Trade-off Matrix

Water-First introduces a fundamental operational vs economic trade-off:

$$\Delta \text{Profit} = \Delta \text{Revenue}_{\text{saved weeds}} - \Delta \text{Revenue}_{\text{delayed rotations}}$$

| Scenario | Operational Result (Weeds) | Economic Result (Mean Money) | Classification | Action / Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **A: Win-Win** | Weeds drop to `< 30` | Mean Money `> $21568.93` | **Strong Success** | Water-First resolves weeds AND boosts profits. |
| **B: Balanced Trade-off** | Weeds drop to `< 50` | Mean Money `[$21200.00, $21568.93]` | **Operational Success** | Weeds eliminated with non-inferior economic cost. |
| **C: Negative Trade-off** | Weeds drop to `< 50` | Mean Money `< $21200.00` | **Economic Regression** | Rotation delay costs more than weeds saved. Falsified. |
| **D: Failure** | Weeds `≥ 120` | Mean Money `< $21200.00` | **Double Failure** | Policy failed operationally and economically. |

---

## 12. Proposed Success and Falsification Criteria

### Baseline Reference Values (E05)
- Mean Final Money: `$21568.93 ± $361.25`
- Total Weed Conversions: `176`
- Mean Unwatered End-of-Day Ratio: `3.33%`

### Proposed Success Criteria (All must be satisfied for SHIP)
1. **Operational Success:** Total Weed Conversions `< 50` (a `> 70%` reduction vs E05 baseline of 176) AND Mean Unwatered End-of-Day Ratio `< 1.0%`.
2. **Economic Non-Regression:** Mean Final Money **`≥ $21200.00`** (within ~1 sample standard deviation of E05 baseline `$21568.93 ± $361.25`).
3. **Execution Safety:** Completion Rate = `100.00%`, Disqualification Rate = `0.00%`.

### Proposed Falsification Criteria (Any triggers REJECT / REVISE)
1. **Economic Falsification:** Mean Final Money **`< $21200.00`** (statistically significant economic loss caused by crop rotation delays).
2. **Operational Falsification:** Total Weed Conversions **`≥ 120`** (demonstrating that task priority order was not the main cause of starvation).

---

## 13. Identified Risks

1. **Rotation Lag Risk:** High risk that prioritizing WATER delays HARVEST and PLANT enough to lose 1 full harvest cycle per tile over 30 days.
2. **Pathing Overhead Risk:** Increased Manhattan travel between water targets and harvest targets.
3. **Market Window Risk:** Delayed harvest might cause selling at lower market price dips.

---

## 14. Recommendation: GO / REVISE / NO-GO

### Recommendation: **`GO`**

### Rationale
The proposed Water-First intervention (`WATER > HARVEST > PLANT`) is a clean, single-variable, 100% controlled experiment that directly tests the primary operational failure mode identified in E05. It has zero code dependencies, zero architectural changes, and can be evaluated cleanly using our existing, verified 30-episode benchmark suite.

### Proposed Falsifiable Hypothesis for Phase PLAN
> *"Modifying worker spatial task priority from HARVEST > PLANT > WATER to WATER > HARVEST > PLANT (`WaterFirstHIRENWClusterROIAgent`) in the 9-tile multi-worker architecture will reduce total weed conversions from 176 to < 50 (-71.6%) and mean unwatered end-of-day ratio from 3.33% to < 1.0%, while maintaining Mean Final Money >= $21200.00 (non-inferior to E05 baseline $21568.93 ± $361.25)."*
