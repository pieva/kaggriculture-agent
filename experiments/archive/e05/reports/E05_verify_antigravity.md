# VERIFY Evidence — E05 HIRE Multi-Worker Scaling (`HIRENWClusterROIAgent`)

**Date:** 2026-08-25  
**Strategy:** `HIRENWClusterROIAgent`  
**Phase:** VERIFY  
**Readiness Decision:** `READY FOR REVIEW`  
**Preliminary Classification:** `Strong Success Candidate`  

---

## 1. Executive Summary & Verification Overview

In **E05 (`HIRENWClusterROIAgent`)**, we evaluated the primary experimental variable selected in E05-01: introducing additional worker capacity via **1 daily farm hand (`HIRE` at $1/day)** with fixed spatial partitioning (4:5) on the 9-tile NW footprint `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`.

All control parameters from E03/E04 (ROI crop selection formula `yield=2.0`, task priority `HARVEST > PLANT > WATER`, immediate liquidation, no `BUY_LAND`, no `DIG`, no horizon logic) were strictly held constant.

---

## 2. Pre-Benchmark Integrity Checks

1. **Unit Test Suite (`pytest tests/`):** `25 passed in 1.88s` (100% passing).
2. **Standalone Submission Build:** `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py` generated and validated via `test_submission.py` (PASSED).
3. **Artifact Isolation Verification:** Confirmed `experiments/archive/e01/artifacts/baseline.json`, `experiments/archive/e02/artifacts/roi_crop.json`, and `experiments/archive/e03/artifacts/multi_tile.json` remain untouched. Benchmark output saved exclusively to `experiments/archive/e05/artifacts/hire_multiworker.json`.

---

## 3. Benchmark Results (30 Episodes × 720 Steps)

The full 30-episode benchmark was executed against `pass` (10 ep), `random` (10 ep), and `starter` (10 ep):

### 3.1 Overall Benchmark Performance

| Metric | Value |
| :--- | :--- |
| **Total Episodes** | **30** |
| **Completion Rate** | **100.00%** (30/30) |
| **Disqualification Rate** | **0.00%** (0/30) |
| **Overall Win Rate** | **100.00%** (30W / 0L / 0D) |
| **Mean Final Money** | **`$21568.93 ± $361.25`** |
| **Median Final Money** | **`$21442.00`** |
| **Min / Max Final Money** | `$21282.00` / `$22867.00` |
| **Agent Mean Turn Latency** | **`0.0924 ms/turn`** |
| **Sim Mean Step Time** | `4.70 ms/step` |

---

### 3.2 Opponent Breakdown

| Opponent | Episodes | Wins / Losses / Ties | Win Rate | Mean Final Money | Std Dev (`ddof=1`) | Median Final Money |
| :--- | :---: | :---: | :---: | ---: | ---: | ---: |
| **`pass`** | 10 | 10W / 0L / 0D | 100.00% | **$21554.60** | ± $377.29 | $21442.00 |
| **`random`** | 10 | 10W / 0L / 0D | 100.00% | **$21696.20** | ± $445.67 | $21442.00 |
| **`starter`** | 10 | 10W / 0L / 0D | 100.00% | **$21456.00** | ± $276.54 | $21442.00 |

---

### 3.3 Comparative Table Across Iterations (E01–E05)

| Iteration | Strategy | Workers | Managed Footprint | Mean Final Money | Std Dev | Median Final Money | Total Weed Conversions | Mean Unwatered End-of-Day % | Win Rate vs `starter` |
| :--- | :--- | :---: | :---: | ---: | ---: | ---: | :---: | :---: | :---: |
| **E01** | `CarrotLoopAgent` | 1 farmer | 1 tile (4,4) | $3567.63 | ± $205.38 | $3528.00 | 0 | 0.00% | 0.00% (draws) |
| **E02** | `ROICropAgent` | 1 farmer | 1 tile (4,4) | $5857.17 | ± $132.37 | $5837.00 | 0 | 0.00% | 100.00% |
| **E03** | `MultiTileROIAgent` | 1 farmer | 4 tiles (2×2) | $14682.47 | ± $1164.33 | $14146.00 | 0 | 0.00% | 100.00% |
| **E04** | `NWClusterROIAgent` | 1 farmer | 9 tiles (3×3) | $11232.47 | ± $661.26 | $11050.00 | 238 (7.93/ep) | 3.33% | 100.00% |
| **E05** | `HIRENWClusterROIAgent` | **1 farmer + 1 hand ($1/day)** | **9 tiles (3×3)** | **`$21568.93`** | **± $361.25** | **`$21442.00`** | **176 (5.87/ep)** | **3.33%** | **100.00%** |

---

## 4. Quantitative Comparative Analysis

### 4.1 Economic Comparison vs E04 Control (`$11232.47 ± $661.26`)
- **Absolute Delta vs E04:** **`+$10336.46`**
- **Percentage Delta vs E04:** **`+92.02%`**
- **Minimum Economic Success Criterion (`Mean E05 > Mean E04`):** **SATISFIED (+92.02%)**

### 4.2 Economic Comparison vs E03 Reference (`$14682.47 ± $1164.33`)
- **Absolute Delta vs E03:** **`+$6886.46`**
- **Percentage Delta vs E03:** **`+46.90%`**
- **Strong Economic Success Criterion (`Mean E05 >= Mean E03`):** **SATISFIED (+46.90%)**

---

## 5. Agricultural Starvation & Operational Diagnostics

### 5.1 Weed Conversions Comparison
- **Total Weed Conversions E05:** 176 total across 30 episodes (average **5.87 weed conversions/episode**).
- **Comparison vs E04 (238 total / 7.93 per episode):**
  - Absolute Reduction: **`-62 weed conversions`**
  - Relative Reduction: **`-26.05%`**
- **Analysis:** Introducing Hand 1 reduced crop death events by -26.05%. While Hand 1 on 5 tiles still experienced occasional unwatered tiles during heavy harvesting phases, the active farm capacity remained high enough to generate $21.5k+ revenue.

### 5.2 Mean Unwatered End-of-Day Ratio
- **E05 Value:** **`3.33%`** (1 day out of 30 per episode ending at `hour == 23` with unwatered active plants).
- **Comparison vs E04 (`3.33%`):** Identical end-of-day early warning ratio (0.00 percentage point change).

---

## 6. HIRE Operational Diagnostics & Worker Utilization

- **Total HIRE Actions Executed:** 900 total across 30 episodes (exactly **30 HIRE actions per episode**, 1 per day at `hour == 0`).
- **HIRE Cost:** $30.00 per episode ($1/day x 30 days). The final mean money of `$21568.93` is **net of all HIRE costs**.
- **Worker Utilization & Partitioning:**
  - **Farmer Principal (4 tiles):** Executed tasks strictly on `{(4,4), (4,3), (3,4), (3,3)}`.
  - **Hand 1 (5 tiles):** Active for 23 hours/day (hours 1..23), executing tasks strictly on `{(4,2), (3,2), (2,4), (2,3), (2,2)}`.
- **Latency & Performance:** Mean turn latency was **0.0924 ms/turn** (well below the 1000 ms `actTimeout` limit).

---

## 7. Anomalies & Deviations

- **Operational Infrastructure Correction:** Minor update to `scripts/run_eval.py` CLI default output path to prevent overwriting historical baseline files (documented in BUILD E05-03B).
- **No Strategy Deviations:** The agent code ran strictly as specified in PLAN/BUILD without any mid-benchmark tuning.

---

## 8. Preliminary Classification & Readiness Decision

- **Preliminary Classification:** **`Strong Success Candidate`**
  - Mean Final Money increased by **+92.02%** vs E04 (`+$10336.46`) and **+46.90%** vs E03 (`+$6886.46`).
  - Weed conversions dropped by **-26.05%**.
  - Completion Rate = `100.00%`, Disqualification Rate = `0.00%`, Win Rate = `100.00%`.
- **Readiness Decision:** **`READY FOR REVIEW`**
