# Verification Evidence — E04 Initial NW Scaling (`NWClusterROIAgent`)

**Date:** 2026-08-25  
**Strategy:** `NWClusterROIAgent`  
**Phase:** VERIFY  

---

## 1. Executive Summary & Verification Overview

In **E04 (`NWClusterROIAgent`)**, we tested the primary experimental variable selected in E04-02: scaling the managed tile footprint from 4 tiles (2×2 cluster) to **9 tiles (3×3 compact cluster)** `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` in the initial unlocked NW quadrant, operated by a single farmer without `BUY_LAND` and without `HIRE`.

We also integrated water starvation proxy metrics into the evaluation runner (`runner.py`) to empirically measure whether a single farmer using the E03 policy can maintain 9 tiles without crop mortality.

---

## 2. Changes Made

### Strategy Implementation
- **`src/agricola/strategy/nw_cluster_roi.py`** [NEW]: Created `NWClusterROIAgent` managing a 3×3 compact grid of 9 adjacent tiles: `((4,4), (4,3), (4,2), (3,4), (3,3), (3,2), (2,4), (2,3), (2,2))`. Preserved E03 ROI crop selection formula and immediate liquidation logic.
- **`src/agricola/agent.py`** [MODIFY]: Updated submission entrypoint to instantiate `NWClusterROIAgent`.
- **`scripts/build_submission.py`** [MODIFY]: Updated standalone submission builder to bundle `NWClusterROIAgent`.

### Testing & Evaluation Infrastructure
- **`tests/test_nw_cluster.py`** [NEW]: Added 5 unit tests verifying 9-tile cluster tile count, seed purchasing (up to 9 seeds), priority hierarchy (`HARVEST > PLANT > WATER`), Manhattan routing, and PASS behavior.
- **`src/agricola/evaluation/runner.py`** [MODIFY]: Added water starvation proxy tracking (`_compute_starvation_metrics`):
  - **Severe Starvation Proxy:** `weed_count` (tiles converted to `{"kind": "WEED"}` due to $\ge 2$ consecutive unwatered days).
  - **Early-Warning Starvation Proxy:** `unwatered_end_of_day_ratio_pct` (% of days ending at `hour == 23` with unwatered active plants).

---

## 3. Verification Results

### 3.1 Unit Test Suite
Ran pytest across all 6 test modules:
```bash
.venv/Scripts/python.exe -m pytest tests/
```
**Result:** `19 passed in 2.06s` (100% passing).

### 3.2 Standalone Submission Build
Generated standalone submission bundle:
```bash
.venv/Scripts/python.exe scripts/build_submission.py
```
**Result:** Standalone submission generated and validated (`test_submission.py` PASSED).

### 3.3 Local Benchmark Comparison (30 Episodes)

Ran 30-episode benchmark evaluation (`scripts/run_eval.py`) against `pass`, `random`, `starter`:

| Metric | E02 (`ROICropAgent`) | E03 Control (`MultiTileROIAgent`) | E04 Target (Plan) | **E04 Actual (`NWClusterROIAgent`)** | E03 → E04 Delta |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Footprint** | 1 tile `(4,4)` | 4 tiles (2×2) | 9 tiles (3×3) | **9 tiles (3×3)** | **4 → 9 tiles** |
| **Total Episodes** | 30 | 30 | 30 | **30** | — |
| **Completion Rate** | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Mean Final Money** | **$5857.17** | **$14682.47** | **$\ge \$22,000.00$** | **$11232.47 ± $661.26** | **-$3450.00 (-23.49%)** |
| **Median Final Money** | $5837.00 | $14146.00 | — | **$11050.00** | -$3096.00 |
| **Total Weed Conversions** | 0 | 0 | 0 (target) | **238 weeds (7.93/ep)** | **+238 weeds** |
| **Unwatered End-of-Day %** | 0.00% | 0.00% | 0.00% (target) | **3.33%** | +3.33% |
| **Agent Mean Latency** | 0.0267 ms | 0.0698 ms | $< 1.0$ ms | **0.0570 ms** | -0.0128 ms |

---

## 4. Rigorous Empirical Analysis & Nuance Clarifications

### 4.1 Weed Conversions Metric Formulation
- **Metric Observation:** Total 238 weed conversions across 30 episodes, corresponding to an average of **7.93 weed conversions per episode**.
- **Data Limitation Clarification:** The observed metric records the total number of tile conversion events to `{"kind": "WEED"}`. With the existing logged data, we measure 7.93 weed conversion events per episode. Because `NWClusterROIAgent` does not execute `DIG` to clear weeds, a tile converted to `WEED` remains occupied for the rest of the game, reducing the active planting capacity.

### 4.2 Single Farmer Policy Scope & Capacity Bottleneck
- **Supported Conclusion:** The E03 policy (`HARVEST > PLANT > WATER` priority with Manhattan routing and immediate seed purchasing), extended directly from 4 to 9 tiles without other modifications and keeping a single farmer, is **not operationally sustainable**.
- **Scope Limit (NOT a Universal Law):** This result demonstrates a **capacity and scheduling bottleneck** for the specific E03 policy on a 9-tile cluster. It does **not** prove that *any* single-farmer strategy beyond 4 tiles is universally impossible (e.g. an agent with water-first scheduling or an intermediate footprint like 6 tiles could exhibit different operational dynamics).

### 4.3 Theoretical Estimate Methodological Review
- **Static Estimate in Plan:** The plan estimated 9 `WATER` actions + ~8–10 Manhattan movement steps = 17–19 turns/day, below the 24 turns/day budget.
- **Methodological Finding:** A static count of `WATER + movement` is insufficient to predict operational sustainability because it ignores:
  1. `HARVEST` action turns;
  2. `PLANT` action turns;
  3. Routing travel between heterogeneous task targets;
  4. Temporal distribution of tasks within the day;
  5. Operational priority conflicts where high-priority `HARVEST` or `PLANT` tasks displace time-critical `WATER` tasks.
