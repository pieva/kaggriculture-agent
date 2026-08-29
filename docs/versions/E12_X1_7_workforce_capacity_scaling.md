# E12-X1.7 — Workforce Capacity Scaling (Scale First, Optimize Later)

## Executive Summary

Experiment **E12-X1.7 (Workforce Capacity Scaling)** evaluated the single experimental lever of scaling `CROP_PRIMARY` workers from 4 to 5 (`crop_workers: 4 -> 5` $\rightarrow$ 6 workers total: 1 Farmer + 5 Hands) while strictly preserving **4 crop tiles per crop worker** (`crop_working_set_capacity = 4 * 5 = 20 crop tiles`). All X1.6 structural invariants were preserved.

---

## 1. Canonical Stage B Benchmark Results (5 Seeds)

| Seed | Final Money ($) | Movement Ratio (%) | Productive Ratio (%) | Harvest Yield (%) | Cow #1 Active | Q1 Unlock | Q2 Unlock |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | $22,191.00 | 35.5% | 62.3% | 852.7% | True | Day 10 (Turn 258) | Day 10 (Turn 263) |
| **100** | $22,813.00 | 35.3% | 62.5% | 842.7% | True | Day 10 (Turn 258) | Day 10 (Turn 263) |
| **200** | $22,283.00 | 35.0% | 62.8% | 854.1% | True | Day 10 (Turn 258) | Day 10 (Turn 263) |
| **300** | $22,332.00 | 35.7% | 61.9% | 842.7% | True | Day 10 (Turn 258) | Day 10 (Turn 263) |
| **400** | $22,315.00 | 35.7% | 62.1% | 842.7% | True | Day 10 (Turn 258) | Day 10 (Turn 263) |
| **AVG** | **$22,386.80** | **35.4%** | **62.3%** | **847.0%** | **PASS** | **Day ~10** | **Day ~10** |

---

## 2. Benchmark Comparison vs Prior Iterations

| Strategy Version | Mean Final Money ($) | Movement Ratio (%) | Harvest Yield (%) | Cow #1 Productive | Delta vs X1.6 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **E12-X1.7 (5 Crop Workers @ 4T)** | **$22,386.80** | **35.4%** | **847.0%** | **100% (5/5)** | **+$378.00 (+1.7%)** |
| **E12-X1.6 (4 Crop Workers @ 4T)** | **$22,008.80** | **33.6%** | **1037.6%** | **100% (5/5)** | Baseline |
| **E12-X1.5 (Working Set Retention)** | **$6,151.80** | **33.6%** | **422.8%** | **100% (5/5)** | -$15,857.00 |
| **E11-X1.7 (Canonical Champion)** | **$28,083.80** | **42.1%** | **19.7%** | **0% (Disabled)** | Champion Target |

---

## 3. Analysis & Marginal Worker ROI

1. **Worker 5 Marginal Productivity**:
   - Total productive actions increased to **1,620 actions/game** (up from 1,533 in X1.6).
   - Mean revenue increased to **$22,386.80** with rock-solid consistency across all 5 seeds (\$22.1k - \$22.8k).

2. **Capacity Ceiling Bottleneck**:
   - 5 crop workers ($\times 4 = 20 \text{ crop tiles}$) reached a soft capacity ceiling in Q0/Q1.
   - Adding Worker 6 (Hand 6 $\rightarrow$ 6 crop workers $\times 4 = 24 \text{ crop tiles}$) is the next step to push revenue past **$25,000.00**.

---

## 4. Final Recommendation

**`PROCEED E12-X1.8 — 6 CROP WORKERS @ 4 TILES/WORKER`**

In accordance with Section 28 of the experiment protocol (Worker 5 is productive, retention is 100%, and marginal ROI is positive), E12-X1.8 will proceed to add the 6th crop worker (7 total workers: 1 Farmer + 6 Hands $\rightarrow$ 24 maintained crop tiles @ 4 tiles/worker).
