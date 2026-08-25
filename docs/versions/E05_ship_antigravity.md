# SHIP Evidence — E05 HIRE Multi-Worker Scaling (`HIRENWClusterROIAgent`)

**Date:** 2026-08-25  
**Strategy:** `HIRENWClusterROIAgent`  
**Phase:** SHIP  
**Status:** Shipped (`v0.5-e05-hire-multiworker`)  
**SHIP Decision:** `SHIP PASSED`  
**Overall Experiment Evaluation:** `STRONG SUCCESS`  
**Economic Hypothesis:** `SUPPORTED`  
**Starvation Operational Status:** `REDUCED BUT UNRESOLVED`  

---

## 1. Executive Summary & Experimental Consolidation

In **E05 (`HIRENWClusterROIAgent`)**, we successfully validated and consolidated the primary experimental variable: introducing additional worker capacity via **1 daily farm hand (`HIRE` at $1/day)** with fixed spatial partitioning (4:5) on the 9-tile NW footprint `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`.

- **Control (E04):** `NWClusterROIAgent` on 9 tiles (1 farmer) — Mean Final Money: `$11232.47 ± $661.26`.
- **Superior Historical Reference (E03):** `MultiTileROIAgent` on 4 tiles — Mean Final Money: `$14682.47 ± $1164.33`.
- **E05 Verified Performance:** Mean Final Money **`$21568.93 ± $361.25`** (`+$10336.46` / `+92.02%` vs E04, `+$6886.46` / `+46.90%` vs E03).
- **Economic Hypothesis Decision:** **`SUPPORTED`**
- **Worker Capacity Bottleneck Evaluation:** **`STRONGLY SUPPORTED`**
- **Operational Failure Mode Status:** **`STARVATION REDUCED BUT UNRESOLVED`** (Weed conversions decreased from 238 to 176, a `-26.05%` reduction).

---

## 2. Consolidated E05 Configuration

- **Strategy Class:** `HIRENWClusterROIAgent` in [`src/agricola/strategy/hire_nw_cluster_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/hire_nw_cluster_roi.py)
- **Managed Footprint:** 9 tiles `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` in NW quadrant.
- **Workers & Daily HIRE Lifecycle:**
  - 1 Farmer Principal (permanent).
  - 1 Daily Farm Hand hired on `hour == 0` when `len(hands) == 0` and `hires_today == 0` ($1/day cost, total $30/episode).
- **Fixed Spatial Partitioning (4:5):**
  - Farmer Principal (4 tiles): `{(4,4), (4,3), (3,4), (3,3)}`
  - Farm Hand 1 (5 tiles): `{(4,2), (3,2), (2,4), (2,3), (2,2)}`
- **Control Parameters Preserved:** ROI crop selection formula E03 (`yield=2.0`), task priority `HARVEST > PLANT > WATER`, immediate liquidation, no `BUY_LAND`, no `DIG`, no horizon logic.

---

## 3. Benchmark Metrics Summary (30 Episodes)

| Metric | E03 Reference (4 tiles) | E04 Control (9 tiles, 1 farmer) | **E05 Shipped (`HIRENWClusterROIAgent`)** | E04 → E05 Delta |
| :--- | :---: | :---: | :---: | :---: |
| **Workers** | 1 farmer | 1 farmer | **1 farmer + 1 hand ($1/day)** | **+1 worker** |
| **Footprint** | 4 tiles (2×2) | 9 tiles (3×3) | **9 tiles (3×3)** | — |
| **Total Episodes** | 30 | 30 | **30** | — |
| **Completion Rate** | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Mean Final Money** | **$14682.47 ± $1164.33** | **$11232.47 ± $661.26** | **`$21568.93 ± $361.25`** | **+$10336.46 (+92.02%)** |
| **Median Final Money** | $14146.00 | $11050.00 | **`$21442.00`** | +$10392.00 |
| **Total Weed Conversions** | 0 | 238 (7.93/ep) | **176 (5.87/ep)** | **-62 (-26.05%)** |
| **Mean Unwatered End-of-Day %** | 0.00% | 3.33% | **3.33%** | 0.00% |
| **Agent Mean Turn Latency** | 0.0698 ms | 0.0570 ms | **0.0924 ms** | +0.0354 ms |

### Opponent Breakdown (E05)
- `pass`: **$21554.60 ± $377.29** (10/10 W)
- `random`: **$21696.20 ± $445.67** (10/10 W)
- `starter`: **$21456.00 ± $276.54** (10/10 W)

---

## 4. Final Scientific Interpretation

1. **Economic Hypothesis (`SUPPORTED`):** Adding worker capacity via `HIRE` ($1/day) with fixed 4:5 spatial partitioning resolved the 9-tile economic scaling failure of E04, producing a **+92.02%** gain over E04 and **+46.90%** over E03.
2. **Worker Capacity Bottleneck (`STRONGLY SUPPORTED`):** Single-farmer physical capacity was a critical bottleneck suppressing 9-tile productivity in E04.
3. **Starvation Failure Mode (`STARVATION REDUCED BUT UNRESOLVED`):** Weed conversions dropped by **-26.05%** (238 $\rightarrow$ 176), but crop mortality events persist because Hand 1 on 5 tiles faces priority conflicts (`HARVEST > PLANT > WATER`) during peak harvest days.
4. **Coexistence Insight:** Outstanding economic success (`+$10.3k`) coexists with an unresolved operational failure mode (176 weeds). The economic gain from harvested crops far exceeds the loss from unwatered tiles, but resolving the remaining 176 weeds provides a clear focus for E06.

---

## 5. Artifact Verification & Historical Isolation

- **E05 Dedicated Artifact:** `results/e05_hire_multiworker.json`
- **Historical Artifacts Preserved:** `results/e01_baseline.json`, `results/e02_roi_crop.json`, and `results/e03_multi_tile.json` are unmodified.
- **Operational Infrastructure Correction:** Updated `scripts/run_eval.py` default output path to `results/latest_eval.json` to prevent future accidental overwrites of historical baseline files.

---

## 6. Candidate Directions for E06 (No Selection)

1. **Candidate A — Water-First Scheduling with HIRE (Recommended by REVIEW):** Modify task priority to `WATER > HARVEST > PLANT` or introduce dynamic water prioritization to eliminate the 176 residual weed conversions.
2. **Candidate B — DIG / Weed Recovery with HIRE:** Introduce action `DIG` to clear weeds.
3. **Candidate C — Dynamic Worker Partitioning:** Rebalance tile allocation dynamically between workers.
4. **Candidate D — Multi-Hand Scaling (2+ HIRE):** Test a 2nd farm hand ($2/giorno).
5. **Candidate E — Further Spatial Scaling:** Expand beyond 9 tiles to new land quadrants.

---

## 7. Version Control & Consolidation Metadata

- **Commit Message:** `Finalize E05 HIRE multi-worker scaling experiment`
- **Branch:** `main` (pushed to `origin/main`)
- **Annotated Tag:** `v0.5-e05-hire-multiworker`
- **Tag Message:** `E05 HIRE Multi-Worker Scaling validated and shipped`
- **Test Suite Status:** `25 passed` (100% passing)
- **Standalone Submission:** `submission/submission.py` validated and passing.
- **SHIP Status:** `SHIP PASSED`
