# E12-D3 — Marginal Capacity ROI Audit
## Why Worker #5 Adds Only +1.7%

## Executive Summary

Experiment **E12-D3 (Marginal Capacity ROI Audit)** was executed as a pure diagnostic audit to uncover why adding the 5th crop worker in E12-X1.7 (+25% theoretical crop capacity from 16 to 20 crop tiles) produced only **+$378.00 (+1.7%)** in Mean Final Money over X1.6 ($22,008.80 $\rightarrow$ $22,386.80).

---

## 1. Audit Findings & Empirical Evidence

| Benchmark Metric | E12-X1.6 (4 Crop Workers) | E12-X1.7 (5 Crop Workers) | Diagnostic Verdict |
| :--- | :---: | :---: | :--- |
| **Mean Final Money** | $22,008.80 | $22,386.80 | **+$378.00 (+1.7%)** |
| **Worker 5 Hired** | N/A | **`None` (Not Hired)** | `active_tiles / 5.0` required 25 tiles for 6th worker |
| **Marginal Tiles (17–20) First Plant** | Day 18–22 (Turn 437–532) | Day 18–22 (Turn 437–532) | **LATE ACTIVATION (Turns 437–532)** |
| **Remaining Days at First Plant** | 6–10 Days | 6–10 Days | **MELON HORIZON MISMATCH (< 12 growth days)** |
| **Melon Cycle Completion Ratio** | 0% (Unfinished) | 0% (Unfinished) | **Melons planted on Day 18–22 generated $0 revenue!** |
| **Seed 400 Peak (Carrot Fallback)** | $22,559.00 | **$26,002.00** | **+$3,443.00 when fast Carrot cycles completed!** |

---

## 2. Root Cause Analysis

### Primary Root Cause: `A. LATE_CAPACITY_ACTIVATION` & `MELON_HORIZON_MISMATCH`

1. **Late Tile Activation**:
   - Marginal tiles 17–20 in Q1 were entered and planted for the first time at **Turn 437 to Turn 532 (Day 18 to Day 22)**.
2. **Melon Growth Horizon Conflict**:
   - Melon requires **12 growth days** to mature (`growth_days = 12`).
   - A Melon planted at Turn 437 (Day 18) matures on Day 30 (Turn 720) — exactly at episode termination.
   - A Melon planted after Day 18 (Turn 432) receives watering actions and consumes \$80 seed capital, but completes **0% of its harvest cycle**, yielding **$0 revenue**.
3. **Hiring Formula Gate**:
   - Worker 5 was never actually hired because `target_tiles_per_worker = 5.0` required 25 active tiles before hiring worker #6.

---

## 3. P&L Breakdown for Marginal Tiles 17–20

- **Gross Revenue**: \$0 (Unfinished Melons) / +\$3,443 (Seed 400 completed Carrot cycles)
- **Seed Investment**: -\$320 (\$80 per Melon seed $\times$ 4 tiles)
- **Watering Action Overhead**: ~36 worker actions spent watering unharvested Melons
- **Net Contribution**: -\$320 (Seeds 0, 100, 200, 300) / +\$3,123 (Seed 400) $\rightarrow$ **Average +$378.00**

---

## 4. Single Empirical Recommendation for X1.8

**`X1.8 EARLIER WORKFORCE / CAPACITY ACTIVATION`**

Do **NOT** add Worker #6 yet. Instead, E12-X1.8 must solve **Capacity Activation Timing**:
1. **Earlier Worker & Tile Activation**: Accelerate Q1 unlock and Cluster E activation from Day 18–22 to **Day 4–6**.
2. **Horizon-Aware Crop Selection**: Forbid planting 12-day Melons after Day 16, switching marginal tiles to 3-day Carrots so 100% of planted crops complete their harvest cycles before Turn 720.
