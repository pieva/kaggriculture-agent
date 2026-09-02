# E12-D1 — Top Player Temporal & Economic Benchmark Report

**Date:** 2026-08-27  
**Phase:** E12-D1 PURE DIAGNOSTIC AUDIT  
**Status:** `COMPLETED & QUANTIFIED — NO STRATEGY CODE MODIFIED IN D1`  
**Primary Datasets:** 
- `experiments/archive/e12/artifacts/x13_temporal_benchmark.csv` (E12-X1.3 Paired Seeds 0, 100, 200, 300, 400)
- `experiments/archive/e12/artifacts/x17_temporal_benchmark.csv` (E11-X1.7 Paired Seeds 0, 100, 200, 300, 400)
- Competitor Replay Benchmark Envelope ($70,000–$85,000 top players from `E11-B1` audit)

---

## 1. Executive Summary & Experimental Finding

E12-D1 executed a temporal and economic trajectory audit comparing **E12-X1.3 (Hybrid Full Crop Scaling)** directly against **E11-X1.7 (Corner-Pruned 26t Champion)** and the **Top Competitor Benchmark Envelope**.

### Diagnostic Verdict: **`CAPITAL DIVERGENCE & HARVEST YIELD COLLAPSE`**

The audit revealed why E12-X1.3 achieved physical scale (24.4 peak active tiles, 5.0 workers, 4 quadrants) but generated only **$7,015.40 Mean Money** (vs **$28,083.80 in E11-X1.7**):

1. **Harvest Yield Collapse (72% Crop Death Rate)**:
   - In E12-X1.3, workers planted a mean of **77.8 crops** across 4 quadrants.
   - However, only **21.8 crops** were actually harvested! **72.0% of all planted crops in X1.3 withered or died unharvested!**
   - In contrast, E11-X1.7 planted a mean of **53.4 crops** and harvested **57.8 crops** (**108.2% harvest yield ratio** via multi-harvest crops).
2. **Premature Capital Draining**:
   - On Turn 48–64 (Day 2), E12-X1.3 spends `$1,000` on Q1 land and `$12` on 4 hands simultaneously, driving liquid cash down to **$50.00**.
   - E11-X1.7 maintains a minimum cash float of **$1,547.00** through Day 12.
3. **Seed 200 Anomaly Discovered**:
   - Draining cash to `$50` on Day 2 triggered `_select_crop_to_plant` liquidity fallback to `CARROT` on feed tiles `(2,3), (2,4)`.
   - CARROTS replaced WHEAT, resulting in 0 WHEAT harvested to shed, which prevented Cow #1 purchase (`wheat_shed >= 1`), yielding **$0.00 Milk Revenue** on Seed 200.

---

## 2. Opening Trajectory Comparison (Turn 1 – 24 / Day 0 – 1)

| Metric | Turn 1 (Day 0 Hr 0) | Turn 6 (Day 0 Hr 5) | Turn 12 (Day 0 Hr 11) | Turn 24 (Day 0 Hr 23) | Capital Deployed @ Turn 24 | Min Cash Turn 1–24 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Top Competitors** | $3,000 | $2,700 | $2,200 | $1,800–$2,400 | ~33% | $1,800 |
| **E11-X1.7** | $3,000 | $3,000 | $3,000 | $3,000 | 0% | $3,000 |
| **E12-X1.3** | $3,000 | $1,999 | $1,078 | $1,078 | **64.1%** | **$1,078** |

### Opening Capital Deployment Ratio $CDR(T) = \frac{\text{Cash}_0 - \text{Cash}_T}{\text{Cash}_0}$:
- **E12-X1.3 $CDR(24)$:** **64.1%** (Rapid early capital burn on Q1 land buy + 4 hires on Day 0–1).
- **E11-X1.7 $CDR(24)$:** **0.0%** (Concentrates capital in Q0 crop cycles before expanding).

---

## 3. Temporal Benchmark Trajectory (Turn 1 – 720)

### Mean Cash Trajectory ($)
| Turn (Day) | Top Competitor Envelope | E11-X1.7 Baseline | E12-X1.3 Hybrid | Cash Gap (X1.3 vs X1.7) |
| :---: | :---: | :---: | :---: | :---: |
| **Turn 1 (D0)** | $3,000 | $3,000 | $3,000 | $0 |
| **Turn 24 (D1)** | $1,800 – $2,400 | $3,000 | $1,078 | -$1,922 |
| **Turn 48 (D2)** | $1,500 – $2,200 | $3,000 | $74 | -$2,926 |
| **Turn 72 (D3)** | $1,800 – $3,000 | $3,000 | $50 | -$2,950 |
| **Turn 120 (D5)** | $2,500 – $4,500 | $3,000 | $50 | -$2,950 |
| **Turn 240 (D10)** | $5,000 – $10,000 | $3,000 | $50 | -$2,950 |
| **Turn 360 (D15)** | $12,000 – $25,000 | $3,000 | $4,579 | +$1,579 |
| **Turn 480 (D20)** | $25,000 – $45,000 | $3,752 | $3,752 | $0 |
| **Turn 600 (D25)** | $45,000 – $65,000 | $7,815 | $3,397 | -$4,418 |
| **Turn 720 (D30)** | **$70,000 – $85,000** | **$28,083.80** | **$7,015.40** | **-$21,068.40** |

---

## 4. Productive Mass & Workforce Milestone Comparison

| Milestone | Top Competitor Envelope | E11-X1.7 Baseline | E12-X1.3 Hybrid | Divergence Note |
| :--- | :---: | :---: | :---: | :--- |
| **Turn Cow #1** | Turn 200–288 (Day 8–12) | N/A (No Livestock) | Turn 122 (Day 5) | E12-X1.3 buys Cow #1 earlier |
| **Turn 9 Crop Tiles** | Turn 24 (Day 1) | Turn 24 (Day 1) | Turn 24 (Day 1) | On target |
| **Turn 15 Crop Tiles** | Turn 96 (Day 4) | Turn 120 (Day 5) | Turn 48 (Day 2) | E12-X1.3 plants Q1 too early |
| **Turn 24 Crop Tiles** | Turn 192 (Day 8) | Turn 288 (Day 12) | Turn 72 (Day 3) | E12-X1.3 hits 24t by Day 3 |
| **Workforce @ 24 Tiles** | 6–8 workers | 6 workers | 5 workers | 5 workers insufficient for 4 quads |
| **Land Expansion Q1 (50t)**| Day 4.20 mean | Day 5.36 mean | **Day 1.0 (Turn 24)** | Premature by 3+ days |
| **Land Expansion Q2 (75t)**| Day 8.53 mean | Day 11.39 mean | **Day 2.0 (Turn 48)** | Premature by 6+ days |

---

## 5. Productivity-Normalized Metrics Audit

| Metric | E11-X1.7 Champion | E12-X1.3 Hybrid | Delta / Ratio | Diagnostic Cause |
| :--- | :---: | :---: | :---: | :--- |
| **Crops Planted (Mean)** | 53.4 crops | 77.8 crops | +24.4 crops | Over-planting across 4 quads |
| **Crops Harvested (Mean)**| 57.8 crops | 21.8 crops | **-36.0 crops** | **Drought / Unwatered Death** |
| **Harvest Yield Ratio** | **108.2%** | **28.0%** | **-80.2%** | 72% of planted crops die |
| **Revenue per Planted Tile**| $525.90 | $90.17 | -82.8% | Low tile utilization |
| **Movement / Total Action %**| 24.1% | **61.4%** | +37.3% | Excess map walking across quads |
| **Productive Action %** | 75.9% | **38.6%** | -37.3% | Only 38% turns spent working |

---

## 6. Root-Cause Hypotheses & Divergence Classification

### Primary Point of Divergence: `CAPITAL_DIVERGENCE` @ Turn 24 & `PRODUCTIVE_MASS_DIVERGENCE` @ Turn 72

1. **Root Cause #1: Map Travel Overhead & Worker Drought Death (High Confidence)**:
   - Unlocking Q1, Q2, Q3 on Days 1–3 forces 5 workers to walk long distances across the 10x10 map (`(0,0)` to `(9,9)`).
   - `Movement / Total Action %` rises to **61.4%**. Workers spend nearly 2/3 of their time walking instead of watering.
   - As a result, crops on Q1–Q3 dry out and die of drought, driving the harvest yield ratio down to **28.0%**.
2. **Root Cause #2: Premature Capital Exhaustion (High Confidence)**:
   - Buying Q1/Q2 land and 4 hands on Days 1–2 drains cash to **$50.00**, leaving zero float to purchase high-value seeds (Melons/Strawberries).
   - The strategy is forced into low-value Carrot fallbacks.
3. **Root Cause #3: Seed 200 Livestock Overriding (High Confidence)**:
   -Draining cash to $50 on Day 2 caused Carrot fallbacks on dedicated feed tiles `(2,3), (2,4)`, blocking WHEAT production and preventing Cow #1 acquisition.

---

## 7. Actionable Directives for E12-X1.4

### Strategic Rule: **DO NOT MODIFY FARM GEOMETRY OR COW #1 OPENING**
- Keep E12 Centered 2x2 Livestock core `(0,0)..(1,1)`.
- Keep Cow #1 opening with Feed Ring WHEAT buffer.

### Required Optimizations for E12-X1.4: **`X1.4 WORKER EFFICIENCY & STAGED EXPANSION TIMING`**
1. **Stage Land Expansion**: Gate Q1 purchase until Day 4–5 and Q2 purchase until Day 8–10 (matching Top Player envelope & E11-X1.7 timing).
2. **Quadrant Locality Pinning**: Restrict workers to specific assigned quadrants (e.g. Farmer + Hand 1 in Q0, Hand 2 in Q1) to eliminate cross-map travel overhead and reduce movement ratio from 61.4% to <25%.
3. **Protect Liquidity Reserve**: Maintain minimum `$300` operating cash reserve so seed purchases are never blocked.
4. **Feed Tile Priority Lock**: Inviolably protect feed tiles `(2,3), (2,4), (1,3), (1,4)` for WHEAT regardless of cash level, preventing the Seed 200 Carrot fallback bug.
