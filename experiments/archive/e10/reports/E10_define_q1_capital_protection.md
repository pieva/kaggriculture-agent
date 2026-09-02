# DEFINE Report — E10-01 Q1 Expansion Capital Protection

**Date:** 2026-08-26  
**Phase:** E10-01 DEFINE  
**Status:** `DEFINED — READY FOR PLAN`  
**Primary Causal Baseline:** E09-01 (`LivestockAblationROIAgent`, 40 tiles, Livestock OFF) — Mean: **$22,899.20**, Median: **$27,672.00**, SD: **$7,892.99**  
**Secondary References:** E06 (9 tiles, Mean $24,731.37), E07 (24 tiles, Mean $12,578.73), E08 (40 tiles, Livestock ON, Mean $11,468.53)  
**Experimental Variant:** `E10-01 Q1 Expansion Capital Protection`  
**Single Variable Change:** Dedicated capital protection floor for Day 12 Q1 land expansion (`BUY_LAND` Q1)  

---

## 1. Experimental Context & Motivation

In **E09-01**, removing the livestock subsystem doubled mean final money ($22,899.20 vs $11,468.53) and achieved a median final money of $27,672.00, outperforming E06 (9 tiles) in 70% of local paired episodes. However, E09-01 exhibited a severe negative tail in 7 out of 30 local episodes (and underperformed on Kaggle, scoring 347.0 vs E06's 375.7).

Forensic diagnosis in E09-05 REVIEW identified the primary cause of these severe drops:
> **Day 12 Q1 Land Expansion Cash Bottleneck**

In negative tail episodes (e.g. seeds 500, 700, 100, 200), optional seed purchases (Melon seeds at $320/pack or Carrot seeds at $120/pack) on Days 8–11 consumed liquid cash down to near the default `$300.0` reserve floor. Consequently, at Day 12 Hour 0, liquid cash fell short of the `$1,000.0` land expansion cost (or the `$1,000.0 + $300.0` post-purchase reserve condition). `BUY_LAND` Q1 was delayed by several days or missed entirely before the Day 18 Melon planting cutoff, leaving 14 Q1 Melon tiles unplanted and forfeiting ~$22,500 in potential revenue per episode.

---

## 2. Primary Causal Baseline & Invariants

### Primary Causal Baseline:
- **E09-01** (`LivestockAblationROIAgent`, [`src/agricola/strategy/livestock_ablation_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/livestock_ablation_roi.py))

### Frozen Strategy Invariants (Identical to E09-01):
1. **Target Productive Footprint:** 40 tiles (20 Q0 + 20 Q1).
2. **Livestock Subsystem:** **OFF** (0 animal buys, 0 pastures, 0 placement, 0 feed, 0 Milk/Wool sales).
3. **Workforce & Hiring Schedule:** 4 workers maximum (Farmer + 3 Hands hired at Day 1, Day 6, Day 12 using Fibonacci cost array `[1, 1, 2, 3, 5, 8]`).
4. **Task Priority Scheme:** `WATER > HARVEST > PLANT` (Water-First scheduling).
5. **Spatial Partitioning:** Worker 0 (Farmer) & Worker 1 (Hand 1) assigned to Q0 ($x \le 4$), Worker 2 (Hand 2) & Worker 3 (Hand 3) assigned to Q1 ($x \ge 5$) when owned.
6. **Cross-Boundary Emergency Water Assist:** Enabled.
7. **Crop Allocation:** 22 Melon tiles (8 Q0, 14 Q1), 12 Carrot tiles (6 Q0, 6 Q1), 6 Wheat tiles (6 Q0).
8. **End-Game Horizon & Liquidation:** Cutoff Day 26 for planting, Flush starting Day 27.
9. **Market Policy:** Order cap 10/turn, shed capacity 100, Premium-First queue.
10. **Target Expansion Day:** Day 12 (`expansion_day = 12`).

---

## 3. Experimental Variable: Q1 Expansion Capital Protection Policy

### Analysis of Current Code & Mechanics:
- **Cost of `BUY_LAND` Q1:** `$1,000.0`
- **Target Expansion Day:** Day 12, Hour 0 (`expansion_day = 12`)
- **Current Cash Reserve Floor:** `cash_reserve = 300.0`
- **Pre-Expansion Spending Leakage:** In E09, `_buy_seeds_if_needed` evaluates `cash - seed_cost >= 300.0`. On Days 8–11, cash between $300 and $1,300 is freely spent on Melon/Carrot seeds, causing cash at Day 12 to drop below the required land expansion threshold.

### Proposed Rule (Single Variable Delta E09 -> E10):
`Q1 Expansion Capital Protection` introduces a minimal, continuous protection rule prior to land expansion:

1. **Pre-Expansion Seed Protection Window (Days 8–11 while `owned_quadrants < 2`):**
   When `owned_quadrants < 2` and `day >= 8` (the pre-expansion accumulation window after initial Q0 planting), discretionary seed purchases in `_buy_seeds_if_needed` must enforce a protected cash reserve equal to the land cost (`$1,000.0`). Seed purchases are allowed only if `cash - seed_cost >= 1000.0`.

2. **Unblocked `BUY_LAND` Execution on Day 12:**
   On or after Day 12 (`day >= expansion_day`), if `owned_quadrants < 2`, `BUY_LAND` Q1 executes as soon as `cash >= 1000.0` (requiring no redundant post-purchase $300 reserve that would block expansion when cash is between $1,000 and $1,299).

3. **Post-Expansion Release:**
   Once `BUY_LAND` Q1 is executed (`owned_quadrants >= 2`), capital protection is released, and standard reserve rules (`cash_reserve = 300.0`) resume for all subsequent seed/market operations.

---

## 4. Hypothesis Statement

> **Protecting the $1,000.0 capital required for Q1 land expansion prior to Day 12 will ensure timely Q1 land acquisition on Day 12, enabling full 40-tile productive crop activation and eliminating the financial collapses observed in E09 without regressing peak mainstream performance.**

---

<!-- END OF FILE -->
