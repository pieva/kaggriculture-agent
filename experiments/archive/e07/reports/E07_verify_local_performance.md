# E07-08 — VERIFY Local Performance Report

**Phase:** `E07-08 — VERIFY Local Performance`  
**Date:** 2026-08-26  
**Status:** `COMPLETED`  
**VERIFY Decision:** **`ARCHITECTURALLY VALID, ECONOMICALLY WEAK`**

---

## 1. Benchmark Objective

The objective of `E07-08` is to empirically benchmark the new competitive baseline reference **E07** (`HybridLivestockClusterROIAgent`) against the shipped baseline **E06** (`WaterFirstHIRENWClusterROIAgent`) and historical baseline **E05** (`HIRENWClusterROIAgent`) across 30 paired controlled local episodes to answer:

> Does the new E07 architecture produce a real local performance improvement over previous baselines, and which economic components explain its performance?

---

## 2. Frozen E07 Configuration

Before starting the benchmark, the E07 configuration was frozen without any post-observation parameter tuning:

| Parameter | Value | Description |
| :--- | ---: | :--- |
| `target_quadrants` | `2` | Q0 (25 tiles) + Q1 (25 tiles) = 50 tiles total |
| `productive_tiles` | `24` | 9 Q0 crop + 15 Q1 crop tiles |
| `wheat_tiles` | `6` | Dedicated feed crop tiles in Q0 |
| `melon_tiles` | `12` | Dedicated cash crop tiles in Q1 |
| `carrot_tiles` | `6` | Dedicated flex liquidity tiles |
| `target_workers` | `4` | 1 Farmer Principal + up to 3 Farm Hands |
| `target_cows` | `4` | Cow target ($400 cost, Milk $160) |
| `target_sheep` | `2` | Sheep target ($500 cost, Wool $200) |
| `expansion timing` | `Day 12` | Target day for `BUY_LAND` Q1 expansion |
| `cash reserve` | `$300.00` | Minimum liquid bank float |
| `livestock cutoffs` | Cow D20, Sheep D18 | Acquisition day cutoffs |
| `crop cutoffs` | Melon D18, All crops D26 | Planting day cutoffs |
| `liquidation timing` | Day 27+ | Inventory flush phase start day |
| `market policy` | Order cap 10/turn, shed cap 100 | Market broker rules |

---

## 3. Benchmark Protocol

- **Total Episodes per Agent:** 30 episodes (720 steps each).
- **Opponents:** 10 × `pass`, 10 × `random`, 10 × `starter`.
- **Positioning:** 5 episodes as Player 0, 5 episodes as Player 1 per opponent.
- **Random Seeds:** Identical seeds (`seed = episode_idx * 100`) across all agents for exact paired-sample comparisons.

---

## 4. Comparability Check

- **Runner Compatibility:** All three agents (E05, E06, E07) were executed through the exact same evaluation runner (`src/agricola/evaluation/runner.py`) using `reward = farm["money"]`.
- **Agent Entrypoints:** A wrapper helper `agent_decide` dispatched `.decide(state)` for E07 and `.act(state)` for E05/E06, ensuring 100% execution fidelity.
- **Wheat Stock Verification:** Environment inspection confirmed that `WHEAT` seed (`private["seeds"]["WHEAT"]`) and `WHEAT` product (`private["shed"]["WHEAT"]`) are separate inventory stocks. Seeds are used strictly for `PLANT`, whereas harvested/bought product is used for `FEED` or `SELL`. The product conservation equation was strictly enforced.

---

## 5. Overall Results (30 Episodes per Agent)

| Agent | Completion | DQ | W / D / L | Win Rate | Mean Final Money | SD (`ddof=1`) | Median | Min | Max |
| :--- | ---: | ---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **E05** | 100.0% | 0 | 30 / 0 / 0 | 100.0% | **$21,485.87** | ± $217.21 | $21,442.00 | $21,242.00 | $22,568.00 |
| **E06** | 100.0% | 0 | 30 / 0 / 0 | 100.0% | **`$25,180.30`** | **± $1,751.93** | **`$25,847.00`** | $22,192.00 | $28,040.00 |
| **E07** | 100.0% | 0 | 30 / 0 / 0 | 100.0% | **$15,364.57** | ± $3,144.39 | $15,990.50 | $7,253.00 | $18,423.00 |

---

## 6. Opponent Breakdown

| Agent | Opponent | N | Mean Final Money | SD (`ddof=1`) | Median | W / D / L |
| :--- | :--- | ---: | ---: | ---: | ---: | :---: |
| **E05** | `pass` | 10 | $21,554.60 | ± $356.07 | $21,442.00 | 10 / 0 / 0 |
| **E05** | `random` | 10 | $21,447.00 | ± $106.59 | $21,442.00 | 10 / 0 / 0 |
| **E05** | `starter` | 10 | $21,456.00 | ± $77.20 | $21,442.00 | 10 / 0 / 0 |
| **E06** | `pass` | 10 | $24,593.30 | ± $2,144.96 | $25,847.00 | 10 / 0 / 0 |
| **E06** | `random` | 10 | $26,127.30 | ± $687.32 | $25,847.00 | 10 / 0 / 0 |
| **E06** | `starter` | 10 | $24,820.30 | ± $1,814.73 | $25,847.00 | 10 / 0 / 0 |
| **E07** | `pass` | 10 | $14,749.10 | ± $3,708.58 | $15,430.50 | 10 / 0 / 0 |
| **E07** | `random` | 10 | $15,275.20 | ± $3,096.08 | $15,360.50 | 10 / 0 / 0 |
| **E07** | `starter` | 10 | $16,069.40 | ± $2,745.50 | $16,932.50 | 10 / 0 / 0 |

---

## 7. E07 vs E06 Delta

$$\Delta = \text{Mean}(E07) - \text{Mean}(E06) = \$15,364.57 - \$25,180.30 = \mathbf{-\$9,815.73}$$
$$\Delta\% = \frac{-\$9,815.73}{\$25,180.30} \times 100 = \mathbf{-38.98\%}$$

- **Median Delta:** `-$9,856.50` (**`-38.13%`**)
- **Win Rate Delta:** `0.00%` (both achieve 100% win rate vs opponents).

---

## 8. E07 vs E05 Delta

$$\Delta = \text{Mean}(E07) - \text{Mean}(E05) = \$15,364.57 - \$21,485.87 = \mathbf{-\$6,121.30}$$
$$\Delta\% = \frac{-\$6,121.30}{\$21,485.87} \times 100 = \mathbf{-28.49\%}$$

- **Median Delta:** `-$5,451.50` (**`-25.42%`**)

---

## 9. Paired Analysis (30 Paired Episodes)

| Comparison | Better ($E07 > Opp$) | Equal ($E07 = Opp$) | Worse ($E07 < Opp$) | Mean Paired $\Delta$ | Median Paired $\Delta$ |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **E07 vs E06** | **0 (0.0%)** | 0 (0.0%) | **30 (100.0%)** | **-$9,815.73** | **-$9,863.50** |
| **E07 vs E05** | **0 (0.0%)** | 0 (0.0%) | **30 (100.0%)** | **-$6,121.30** | **-$5,939.00** |

> **Finding:** E06 beat E07 in **100% of paired episodes** under identical seeds and opponent actions.

---

## 10. Land Diagnostics (E07)

- **`BUY_LAND` Executed:** 30 / 30 episodes (100%).
- **Mean Expansion Timing:** Step 299.7 (Day 12.5).
- **Managed Tiles:** 50 tiles total (Q0 25 + Q1 25).
- **Productive Crop Tiles:** 24 (9 Q0 + 15 Q1).
- **Q1 Harvests:** Mean 30.67 crops.
- **Q1 Worked Steps:** Mean 563.7 steps.

---

## 11. Workforce Diagnostics (E07)

- **HIRE Attempted / Accepted:** 68.0 / 68.0 orders per episode (100% acceptance).
- **HIRE Spending:** Mean $85.00 total.
- **Peak Simultaneous Workers:** 4.0 workers (1 Farmer + 3 Hands, 100% active).
- **Worker Time Allocation:**
  - Productive step ratio: ~30.8%
  - Movement step ratio: ~54.2% (significantly higher travel distance across 50 tiles)
  - Idle step ratio: ~15.0%

---

## 12. Crop Economics (E07 Mean Values)

| Crop | Harvested Units | Sold Units | Seed Cost ($) | Gross Revenue ($) | Gross Contribution ($) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Melon** | 67.63 | 67.63 | $202.90 | $16,908.33 | +$16,705.43 |
| **Wheat** | 129.53 | 115.00 | $117.50 | $2,875.00 | +$2,757.50 |
| **Carrot** | 4.07 | 4.07 | $20.35 | $142.33 | +$121.98 |
| **Total Crops** | **201.23** | **186.70** | **$340.75** | **$19,925.66** | **+$19,584.91** |

---

## 13. Livestock Economics (E07 Mean Values)

- **Cows Purchased:** 1.27 ($506.67 cost)
- **Sheep Purchased:** 0.13 ($66.67 cost)
- **Total Livestock Purchase Cost:** **$573.34**
- **Pastures Built:** 5.8
- **Feed Actions Attempted / Successful / Wheat Consumed:** 33.3 / 33.3 / 33.3 units
- **Milk Generated / Harvested / Sold:** 3.4 / 3.4 / 2.43 units
- **Milk Revenue:** **$389.33**
- **Wool Sold / Revenue:** 0.3 units / **$60.00**
- **Total Livestock Revenue:** **$449.33**
- **Observed Direct Livestock Cash Contribution:** $$\text{Revenue } (\$449.33) - \text{Direct Cost } (\$573.34) = \mathbf{-\$124.01}$$

---

## 14. Wheat Accounting & Corrected Ledger

- **Initial Wheat Product:** 0
- **Harvested Wheat Product:** 129.53 units
- **Purchased Wheat Product:** 47.00 units
- **Total Wheat Product Sources:** **176.53 units**
- **Fed Wheat:** 33.30 units
- **Sold Wheat:** 115.00 units
- **Final Product Stock (Shed + Worker Inv):** 28.23 units
- **Total Wheat Product Uses:** **176.53 units**
- **Product Conservation Delta:** **0**

---

## 15. Capital Deployment & Investments (E07 Mean Values)

- **Starting Cash:** $3,000.00
- **Minimum Cash Float:** $218.00
- **Seed Investment:** $340.75
- **Workforce HIRE Investment:** $85.00
- **Land Expansion Investment (Q1):** $1,000.00
- **Livestock Purchase Investment:** $573.34
- **Total Direct Investments:** **$1,999.09**

---

## 16. Phase Economics

- **OPENING (Day 0–5):** Q0 crop setup, HIRE 2 workers. Cash: $3000 $\rightarrow$ $2100.
- **SCALE (Day 6–12):** BUY_LAND Q1 ($1000), HIRE 3 hands ($3/day), buy Cows ($400). Cash drops to min float $218.00.
- **PRODUCE (Day 13–26):** High travel movement across Q0/Q1/Pastures. 33.3 Wheat fed, 3.4 Milk harvested.
- **LIQUIDATION (Day 27–30):** Inventory flush successfully converts shed crops to cash, bringing final cassa to **$15,364.57**.

---

## 17. Terminal Asset Audit (Unmonetized Assets at Turn 720)

- **Unsold Inventory:** ~28 units Wheat product in shed/inv.
- **Remaining Livestock:** ~1.27 Cows + 0.13 Sheep on pastures.
- **Mature / Immature Crops Remaining:** ~4 tiles unharvested at step 720.
- **Unused Productive Capacity:** 50 tiles owned, but long worker travel distances limit turn efficiency.

---

## 18. Variability & Outliers

- **Top 3 Best Episodes:**
  1. Ep 9 vs `pass` (seed 800): **$18,423.00** (2 weeds)
  2. Ep 7 vs `starter` (seed 600): **$18,352.00** (3 weeds)
  3. Ep 2 vs `random` (seed 100): **$18,327.00** (0 weeds)
- **Top 3 Worst Episodes:**
  1. Ep 7 vs `pass` (seed 600): **$7,253.00** (6 weeds, delayed animal purchase)
  2. Ep 1 vs `random` (seed 0): **$9,458.00** (11 weeds, adverse initial weather)
  3. Ep 1 vs `pass` (seed 0): **$9,507.00** (11 weeds, adverse initial weather)

---

## 19. Performance Diagnosis: Root Causes of E07 Underperformance vs E06 (-38.98%)

1. **Opportunity Cost of Wheat Crop Allocation (Primary Cause):**
   E07 dedicated 6 out of 9 Q0 tiles to **Wheat** (gross yield $25/unit). E06 dedicated all 9 tiles to **Carrots/Melons** (gross yield $140–$250/unit). Locking 6 tiles into low-margin Wheat created a massive ~$7,000 revenue drag.
2. **Livestock Negative Net Direct Return:**
   Cows cost $400 + 5 pasture tiles + 6 feed tiles + 14-day yield cycle, producing only $389.33 Milk revenue by Day 30, failing to recoup the $573.34 purchase investment.
3. **Q1 Land Expansion Cost & Travel Distance Overhead:**
   Buying Q1 cost $1,000 cash upfront. Working Q1 tiles (0,5)–(4,9) required workers to travel long distances from shed (4,4), increasing movement steps to 54.2% and causing 7.73 weeds/episode (vs 2.1 in E06).

---

## 20. Candidate Variables E08+

| Variable | Priority | Rationale |
| :--- | :---: | :--- |
| **Wheat Allocation Reduction** | **HIGH** | Reduce Wheat tiles from 6 to 2–3 or buy feed directly from market to unlock high-ROI Melon/Carrot tiles. |
| **Livestock Purchase Timing & Size** | **HIGH** | Limit Cow purchases to max 1 early Cow or eliminate Sheep ($500 cost, $60 revenue) to avoid negative net payback. |
| **Land Expansion (BUY_LAND) Timing** | **HIGH** | Defer Q1 expansion or eliminate it if movement overhead exceeds crop margin. |
| **Task Priority (WATER > HARVEST > PLANT)** | **HIGH** | Adopt E06 Water-First priority in multi-worker routine to reduce weed conversions from 7.73 to <2. |
| **Worker Partitioning & Routing** | **MEDIUM** | Optimize worker tile assignment to minimize travel steps between shed (4,4) and Q1. |

---

## 21. VERIFY Decision

> **`ARCHITECTURALLY VALID, ECONOMICALLY WEAK`**

All 15 E07 architectural capabilities (Phase scheduling, Workforce multi-scaling, Land expansion, Livestock pipeline, Feed loop, Market brokerage, Inventory flush) are **100% verified and operational**. However, the un-tuned capital deployment ($1000 land, $573 animals, 6 low-ROI Wheat tiles) creates a **-38.98% economic regression vs E06** ($15,364.57 vs $25,180.30). E07 serves as an architecturally valid foundation for E08+ optimization.
