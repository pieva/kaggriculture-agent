# SHIP Evidence — E06 Water-First Scheduling (`WaterFirstHIRENWClusterROIAgent`)

**Date:** 2026-08-25  
**Strategy Class:** `WaterFirstHIRENWClusterROIAgent`  
**Phase:** SHIP  
**Status:** Shipped (`v0.6-e06-water-first`)  
**SHIP Decision:** `SHIP PASSED`  
**Overall Experiment Evaluation:** `STRONG SUCCESS`  
**Hypothesis Verdict:** `SUPPORTED`  

---

## 1. Executive Summary & Experimental Consolidation

In **E06 (`WaterFirstHIRENWClusterROIAgent`)**, we successfully validated and consolidated the primary experimental variable: modifying worker spatial task priority from `HARVEST > PLANT > WATER` to **`WATER > HARVEST > PLANT`** on the 9-tile NW footprint `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` with 1 Farmer Principal and 1 Daily Farm Hand ($1/day).

- **E05 Baseline (Shipped):** Mean Final Money `$21568.93 ± $361.25`, Weed Conversions = `176`.
- **E06 Shipped Performance:** Mean Final Money **`$24662.00 ± $1932.04`** (`+$3093.07` / `+14.34%` vs E05).
- **Median Final Money:** **`$25847.00`** (`+$4405.00` / `+20.54%` vs E05).
- **Total Weed Conversions:** **`70`** (down from 176, a **`-60.23%`** reduction).
- **Paired Money Win Rate:** **`29 / 30` episodes (`96.7%`)**.
- **Paired Weed Win Rate:** **`30 / 30` episodes (`100.0%`)**.
- **Experimental Integrity:** `PASSED`
- **Hypothesis Verdict:** `SUPPORTED`
- **SHIP Decision:** **`SHIP PASSED`**

---

## 2. Shipped Strategy Configuration

- **Strategy Class:** `WaterFirstHIRENWClusterROIAgent` in [`src/agricola/strategy/water_first_hire_nw_cluster_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/water_first_hire_nw_cluster_roi.py).
- **Managed Footprint:** 9 tiles `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` in NW quadrant.
- **Workers & HIRE Lifecycle:** 1 Farmer Principal (4 tiles) + 1 Daily Farm Hand hired on `hour == 0` ($1/day cost, 5 tiles).
- **Spatial Partitioning:** Fixed 4:5 (Farmer: `{(4,4), (4,3), (3,4), (3,3)}`; Hand 1: `{(4,2), (3,2), (2,4), (2,3), (2,2)}`).
- **Single Variable Modified:** Worker task priority `WATER > HARVEST > PLANT`.
- **Control Parameters Preserved:** E03 ROI crop selection ($2.0 \times \text{price} - \text{seed}) / \text{days}$, immediate liquidation, nearest Manhattan routing.

---

## 3. Experimental Progression

`E01 baseline → E02 ROI crop selection → E03 multi-tile scaling → E04 NW scaling (falsified) → E05 multi-worker HIRE (shipped) → E06 Water-First scheduling (shipped)`

---

## 4. Benchmark Metrics Summary (30 Episodes)

| Metric | E03 Reference (4 tiles) | E04 Control (9 tiles, 1 farmer) | E05 Shipped (9 tiles, 2 workers) | **E06 Shipped (`WaterFirstHIRENWClusterROIAgent`)** | E05 → E06 Delta |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Strategy Priority** | `HARVEST > PLANT > WATER` | `HARVEST > PLANT > WATER` | `HARVEST > PLANT > WATER` | **`WATER > HARVEST > PLANT`** | **Water-First** |
| **Workers** | 1 farmer | 1 farmer | 1 farmer + 1 hand ($1/day) | **1 farmer + 1 hand ($1/day)** | — |
| **Managed Footprint** | 4 tiles (2×2) | 9 tiles (3×3) | 9 tiles (3×3) | **9 tiles (3×3)** | — |
| **Total Episodes** | 30 | 30 | 30 | **30** | — |
| **Completion Rate** | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 100.00% | 100.00% | 100.00% | **100.00%** (30W / 0L / 0D) | 0.00% |
| **Mean Final Money** | $14682.47 ± $1164.33 | $11232.47 ± $661.26 | $21568.93 ± $361.25 | **`$24662.00 ± $1932.04`** | **+$3093.07 (+14.34%)** |
| **Median Final Money** | $14146.00 | $11050.00 | $21442.00 | **`$25847.00`** | **+$4405.00 (+20.54%)** |
| **Min Final Money** | $12430.00 | $10120.00 | $21282.00 | **`$22184.00`** | +$902.00 |
| **Max Final Money** | $16840.00 | $12450.00 | $22867.00 | **`$27873.00`** | +$5006.00 |
| **Total Weed Conversions** | 0 | 238 (7.93/ep) | 176 (5.87/ep) | **`70` (2.33/ep)** | **-106 (-60.23%)** |
| **Mean Unwatered EOD %** | 0.00% | 3.33% | 3.33% | **`8.11%`** *(Metric Caveat)* | +4.78% |
| **Agent Mean Turn Latency** | 0.0698 ms | 0.0570 ms | 0.0924 ms | **`0.0822 ms`** | -0.0102 ms |

### Opponent Breakdown (E06)
- `pass`: **$24593.30 ± $2145.00** (10/10 W) | Weeds: 22 total (2.20/ep)
- `random`: **$24572.40 ± $2122.90** (10/10 W) | Weeds: 26 total (2.60/ep)
- `starter`: **$24820.30 ± $1814.70** (10/10 W) | Weeds: 22 total (2.20/ep)

---

## 5. Paired Seed-by-Seed Evidence (30 Episodes)

$$\Delta \text{Money}_i = \text{Money}_{\text{E06}, i} - \text{Money}_{\text{E05}, i}$$
$$\Delta \text{Weeds}_i = \text{Weeds}_{\text{E06}, i} - \text{Weeds}_{\text{E05}, i}$$

- **Mean Paired Money Delta:** **`+$3093.07 ± $1942.60`**
- **Median Paired Money Delta:** **`+$4405.00`**
- **Money Win Rate:** **`29 / 30` episodes (`96.7%`)** outperforming E05.
- **Mean Paired Weed Delta:** **`-3.53 weeds/episode`**
- **Weed Win Rate:** **`30 / 30` episodes (`100.0%`)** outperforming E05.

---

## 6. Operational & Economic Verdicts

- **Operational Verdict:** **`PARTIAL SUPPORT`** (Weed conversions decreased by `-60.23%` from 176 to 70; starvation was drastically reduced, though 70 weeds remain due to peak harvest workload on Hand 1's 5-tile partition).
- **Economic Verdict:** **`ECONOMIC IMPROVEMENT`** (Mean Final Money expanded by `+$3093.07` / `+14.34%`, passing the `$21200` guardrail with a 96.7% paired win rate).
- **Reliability Verdict:** **`PASSED`** (100% completion, 0% disqualification, 100% win rate against all opponents).

---

## 7. Metric Caveat & Causal Interpretation

- **Metric Caveat:** `Mean Unwatered End-of-Day Ratio = 8.11%` is recorded as a metric caveat. It represents an intra-day sampling artifact caused by planting seeds in the afternoon after morning watering passes. Newly planted seeds sit unwatered at hour 23 but suffer 0 starvation and are watered the next morning.
- **Causal Interpretation:** Controlled single-variable design provides rigorous evidence that the Water-First policy caused the `+$3093.07` money expansion and `-106` weed reduction. Preventing 106 crop deaths preserved active tile days, allowing 2–4 extra crop harvest cycles per episode.

---

## 8. Final Hypothesis Verdict & SHIP Decision

- **Final Hypothesis Verdict:** **`SUPPORTED`**
- **SHIP Decision:** **`SHIP PASSED`**

---

## 9. Standalone Validation & Test Results

- **Standalone Submission File:** [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py) (Bundles `GameState`, `ActionBuilder`, `HIRENWClusterROIAgent`, and `WaterFirstHIRENWClusterROIAgent`).
- **Test Suite Results:** `.venv\Scripts\pytest tests/` $\rightarrow$ **`30 passed in 2.33s` (100% passing)**.

---

## 10. Final Artifacts Preserved

- Benchmark Result: `results/e06_water_first.json`
- Capability Analysis: `docs/experiments/E06-01_Water_First_Capability_Analysis.md`
- Implementation Plan: `docs/plans/E06_Water_First_Scheduling.md`
- BUILD Report: `docs/versions/E06_build_antigravity.md`
- VERIFY Report: `docs/versions/E06_verify_antigravity.md`
- REVIEW Report: `docs/versions/E06_review_antigravity.md`
- SHIP Report: `docs/versions/E06_ship_antigravity.md`

---

## 11. Git Metadata

- **Commit Message:** `Finalize E06 water-first scheduling experiment`
- **Branch:** `main` (pushed to `origin/main`)
- **Annotated Tag:** `v0.6-e06-water-first`
- **Tag Message:** `E06 Water-First Scheduling validated and shipped`

---

## 12. Prioritized Roadmap for E07

1. **Candidate A — `DIG` / Weed Recovery:** Enable `DIG` to clear the 70 residual weeds and reclaim dead tiles. (Recommended for E07 DEFINE).
2. **Candidate B — Dynamic Worker Partitioning:** Rebalance 4:5 tile split dynamically based on real-time workload.
3. **Candidate C — Dynamic Priority Scheduling:** Urgency-based task priority (`WATER_URGENT > HARVEST > PLANT > WATER_NON_URGENT`).
4. **Candidate D — Multi-Hand Scaling:** Test a 2nd daily farm hand ($2/day cost).
5. **Candidate E — Metric Redesign:** Replace `Unwatered End-of-Day Ratio` with consecutive unwatered day tracking.
