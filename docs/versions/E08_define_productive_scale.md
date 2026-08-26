# E08 — DEFINE Productive Scale Optimization

**Phase:** `E08-01 — DEFINE Productive Scale Optimization`  
**Date:** 2026-08-26  
**Status:** `COMPLETED`  
**Decision:** **`GO FOR PLAN`**  
**Target Submission:** Kaggle E08 Submission (Evening 2026-08-26)  

---

## Executive Summary

The E07 local performance verification (`E07-08`) classified the architecture as **`ARCHITECTURALLY VALID, ECONOMICALLY WEAK`**.
While all 15 architectural capabilities (Land expansion, Workforce HIRE, Livestock cycle, Market brokerage, Liquidation) passed 100%, E07 produced a mean local final money of **$15,364.57 ± $3,144.39**, representing a **-38.98% regression vs E06 ($25,180.30)** and **-28.49% vs E05 ($21,485.87)**.

On Kaggle, after ~5 hours of match settling:
- **E05:** `429.5`
- **E06:** `375.7`
- **E07:** `339.5` (approx. -9.6% vs E06 and -21.0% vs E05; initial score 600.0 is non-significant).

A primary structural flaw identified in E07 was the **under-utilization of purchased land**: E07 bought Quadrant 1 ($1,000 cash investment, unlocking 50 total tiles) but maintained a target of only **24 productive crop tiles** (9 in Q0, 15 in Q1), leaving **26 tiles (52.0% of owned land) completely idle**.

**Primary Experimental Question for E08:**
> *Can we substantially scale the productive land surface of owned territory (from 24 to 40 tiles) without degrading operational efficiency or overwhelming worker capacity?*

---

## 1. Evidence from E07

Local diagnostic runs (30 paired controlled episodes) and functional audit logs for E07 provide the following baseline metrics:

### Real Utilization Matrix — E07 Baseline

| Metric | E07 Baseline Value | Rationale / Detail |
| :--- | ---: | :--- |
| **owned tiles after expansion** | **50** | Q0 (25 tiles) + Q1 (25 tiles) after $1,000 `BUY_LAND` |
| **target productive tiles** | **24** | 9 Q0 crop + 15 Q1 crop tiles |
| **actually worked unique tiles** | **24** | 100% of target productive tiles were worked |
| **planted unique tiles** | **24** | 24 unique tiles planted across season |
| **harvested unique tiles** | **24** | 24 unique tiles produced harvested crops |
| **productive utilization / owned land** | **48.0%** | 24 productive tiles / 50 owned tiles |
| **idle / unutilized owned land** | **52.0%** | 26 tiles unused (pastures/well take 6, leaving 20 empty tiles) |
| **Q0 crop utilization** | **36.0%** | 9 crop tiles / 25 Q0 tiles (6 tiles wheat, 3 flex) |
| **Q1 crop utilization** | **60.0%** | 15 crop tiles / 25 Q1 tiles (12 melon, 3 carrot) |
| **worker productive %** | **30.8%** | ~754 worker-turns spent on plant/water/harvest/feed |
| **worker movement %** | **54.2%** | ~1327 worker-turns spent traveling across 50 tiles |
| **worker idle %** | **15.0%** | ~367 worker-turns unassigned / idle |
| **worker-days** | **~102** | 1 Farmer + up to 3 Hands (2448 total worker-turns/ep) |

### Key Diagnostic Takeaway
E07 spent **$1,000 cash** to expand land from 25 to 50 tiles, yet only 48.0% of total owned land generated crops. Furthermore, **15.0% of worker turns were completely idle**, demonstrating that the 4-worker labor force was under-allocated relative to its capacity.

---

## 2. Kaggle E07 Status

After ~5 hours of rating convergence on Kaggle:
- **E05 (`v0.5-e05-hire-multiworker`):** **429.5**
- **E06 (`v0.6-e06-water-first`):** **375.7**
- **E07 (`HybridLivestockClusterROIAgent`):** **339.5**

### Comparative Analysis
- E07 vs E06: **-36.2 pts (-9.6%)**
- E07 vs E05: **-90.0 pts (-21.0%)**

*Note on initial score 600.0:* Initial ratings start at 600.0 before matchmaking; thus 600.0 is an unrated artifact and not a performance indicator.

### Root Cause on Kaggle
1. **Unproductive Fixed Asset Drag:** E07 spent $1,000 upfront on Q1 land expansion and $573 on livestock, but only farmed 24 tiles total.
2. **Wheat ROI Drag:** Dedicating 6 of 9 Q0 tiles to Wheat ($25 gross price) to sustain livestock created a net negative direct payback (-$124 direct return on livestock), forfeiting high-margin Melon/Carrot crop cycles.
3. **High Movement Burden:** Navigating 50 tiles for only 24 productive tiles resulted in a 54.2% movement ratio and 7.73 weeds/episode.

---

## 3. Competitive Replay Evidence

Analysis of top-performing Kaggle adversary replays reveals clear structural patterns in land utilization:

### Competitor Classification by Productive Scale

| Class | Productive Utilization | Characteristics | Final Money Range |
| :--- | :--- | :--- | :--- |
| **LOW** | **18.0% – 30.0%** | Single quadrant (Q0 only), 9–12 productive tiles, 1 worker, no land purchase. Conservative baselines. | $10,000 – $15,000 |
| **MEDIUM** | **40.0% – 50.0%** (E07) | Buys Q1 (50 tiles), targets ~20–25 productive tiles, 3–4 workers, leaves 25+ tiles idle. Mixed livestock. | $15,000 – $25,000 |
| **HIGH** | **70.0% – 90.0%** (Top Competitors) | Buys Q1 (and Q2/Q3 for 50–75+ tiles), transforms **35–48+ tiles** into active productive crops/pastures, 3–4 workers, optimized spatial clusters. | **$35,000 – $50,000+** |

### Key Reconnaissance Findings
1. **Land Expansion Coupling:** Strong agents who buy land **do not leave 50%+ of it idle**. Land expansion is strictly coupled with immediate surface crop scaling (35–45+ crop tiles).
2. **Workforce Alignment:** Top agents run **3 to 4 workers** (1 Farmer + 2–3 Hands), identical to E07's workforce size. Their higher score comes from **higher productive turn allocation** (~55–65% productive, ~30–35% movement, <5% idle), not from larger workforce size.

---

## 4. Productive-Land Gap

Comparing E07 against high-performing competitive benchmarks reveals a stark **Productive-Land Gap**:

```text
E07 Owned Land:                   [██████████████████████████████████████████████████] 50 tiles
E07 Active Productive Tiles:      [████████████████████████] 24 tiles (48% land utilization)
High-Utilization Target (S2):    [████████████████████████████████████████] 40 tiles (80% land utilization)
Competitor Full Potential:        [████████████████████████████████████████████████] 48 tiles (96% land utilization)
```

E07 leaves **26 owned tiles uncultivated**. Buying Q1 for $1,000 cash without farming its tiles is economically equivalent to destroying $1,000 in liquid capital.

---

## 5. Workforce Bottleneck Analysis

We investigated whether the 24-tile limit in E07 resulted from:
- **A. Conservative configuration**
- **B. Insufficient workforce**
- **C. Pathing inefficiency**
- **D. Task priority**
- **E. Combination**

### Quantitative Labor Capacity Analysis (E07 Baseline)
- **Daily Worker Capacity:** 4 workers × 24 turns = **96 worker-turns / day** (2,448 worker-turns per 30-day episode).
- **Productive Actions per Worker-Day:** $\frac{754 \text{ productive turns}}{102 \text{ worker-days}} = \mathbf{7.39 \text{ actions / worker-day}}$.
- **Movement Actions per Worker-Day:** $\frac{1327 \text{ movement turns}}{102 \text{ worker-days}} = \mathbf{13.01 \text{ actions / worker-day}}$.
- **Productive Tiles per Worker:** $\frac{24 \text{ tiles}}{3.4 \text{ avg workers}} = \mathbf{7.06 \text{ tiles / worker}}$.
- **Harvests per Worker-Day:** $\frac{98 \text{ harvests}}{102 \text{ worker-days}} = \mathbf{0.96 \text{ harvests / worker-day}}$.

### Bottleneck Diagnosis
The primary bottleneck is **A. Conservative configuration** combined with **C. Pathing inefficiency**.

With **15.0% idle time** (~367 worker-turns wasted sitting idle), the existing 4-worker labor force (1 Farmer + 3 Hands) has ample unused capacity. 
Scaling from 24 to 40 productive tiles increases daily action demands (plant, water, harvest) from ~34.5 to ~52 actions/day. Out of 96 available worker-turns/day:
- **Productive actions:** ~52 turns (54.2%)
- **Movement actions:** ~38 turns (39.6%)
- **Buffer / Idle:** ~6 turns (6.2%)

**Conclusion:** The workforce of 4 workers is **fully sufficient** to manage 40 productive tiles if spatial pathing and worker partitioning are applied. **No increase in workforce size is required for E08.**

---

## 6. Candidate Scale Scenarios

We evaluated four non-implemented candidate scenarios for E08:

### S0 — Control (E07 Baseline)
- **Productive Tiles:** 24 (9 Q0 + 15 Q1)
- **Workforce:** 4 workers (1 Farmer + 3 Hands)
- **Land Utilization:** 48.0% (24 / 50)
- **Qualitative Assessment:** High worker idle rate (15.0%), poor ROI on $1,000 Q1 land purchase.

### S1 — Moderate Scale
- **Productive Tiles:** 32 (16 Q0 + 16 Q1)
- **Workforce:** 4 workers (frozen)
- **Land Utilization:** 64.0% (32 / 50)
- **Qualitative Assessment:** Moderate action load (~42 actions/day). Easily sustained by 4 workers. Leaves 18 tiles idle, under-utilizing available labor margin.

### S2 — High Scale (RECOMMENDED FOR E08)
- **Productive Tiles:** **40** (20 Q0 + 20 Q1)
- **Workforce:** **4 workers** (frozen: 1 Farmer + 3 Hands)
- **Land Utilization:** **80.0%** (40 / 50)
- **Qualitative Assessment:**
  - **Planting load:** ~4–5 plants/day average.
  - **Watering load:** 40 waters/day max.
  - **Harvesting load:** ~6–8 harvests/day average.
  - **Movement burden:** Managed via spatial worker partitioning (Farmer + Hand 1 in Q0, Hand 2 + Hand 3 in Q1).
  - **Capital required:** ~$500 seed capital, fully funded by initial cash + early harvests.
  - **Risk:** Low-to-moderate, controlled by Water-First scheduling.

### S3 — Near-Full Q0+Q1 Scale
- **Productive Tiles:** 48–50 (near 100% of Q0+Q1)
- **Workforce:** 4–5 workers
- **Land Utilization:** 96.0% – 100.0% (48–50 / 50)
- **Qualitative Assessment:** Very high action load (~68 actions/day). Leaves minimal margin for travel delays across 50 tiles. High risk of unwatered tiles converting to weeds under adverse weather without a 5th worker.

---

## 7. Selected E08 Configuration

We select **Scenario S2 — High Scale (40 Productive Tiles)**.

### Quantitative Rationale
E07 diagnostic data proved that 4 workers had 15.0% idle time on 24 tiles. Scaling to 40 tiles consumes ~52 productive actions/day out of 96 available worker-turns/day (54.2% load), leaving 44 turns for movement and buffer. This tests high land utilization (80.0%) while remaining operationally feasible with the **frozen E07 workforce**.

### Exact Parameter Differences: E07 $\rightarrow$ E08

| Parameter | E07 Baseline | E08 Selected (S2) | Delta / Change |
| :--- | :--- | :--- | :--- |
| **Target Productive Tiles** | `24` (9 Q0 + 15 Q1) | **`40` (20 Q0 + 20 Q1)** | **+16 tiles (+66.7%)** |
| **Land Utilization Target** | `48.0%` (24 / 50) | **`80.0%` (40 / 50)** | **+32.0 percentage points** |
| **Crop Mix Allocation** | 6 Wheat, 12 Melon, 6 Carrot | **6 Wheat, 22 Melon, 12 Carrot** | **+10 Melon, +6 Carrot** |
| **Workforce Target** | 4 (1 Farmer + 3 Hands) | **4 (1 Farmer + 3 Hands)** | **FROZEN (0 change)** |
| **Livestock Target** | 4 Cows, 2 Sheep | **4 Cows, 2 Sheep** | **FROZEN (0 change)** |
| **Land Expansion (`BUY_LAND`)** | Day 12 (Q1 $1,000) | **Day 12 (Q1 $1,000)** | **FROZEN (0 change)** |
| **Task Priority Schedule** | `WATER > FEED > HARVEST > PLANT` | **`WATER > FEED > HARVEST > PLANT`** | **FROZEN (0 change)** |
| **Market Broker Policy** | Order cap 10/turn, shed 100 | **Order cap 10/turn, shed 100** | **FROZEN (0 change)** |
| **Liquidation Timing** | Day 25 Stop Melon, Day 27+ Flush | **Day 25 Stop Melon, Day 27+ Flush** | **FROZEN (0 change)** |

---

## 8. Variables Frozen from E07

To isolate **PRODUCTIVE SCALE** as the single primary experimental variable, all other architectural components are strictly frozen:

1. **Livestock Targets & Feed Logic:** Target 4 Cows, 2 Sheep, 6 dedicated Wheat tiles.
2. **Workforce Schedule:** 1 Farmer Principal + up to 3 Farm Hands hired at `hour == 0`.
3. **Land Expansion Timing:** Day 12 Q1 purchase (`BUY_LAND`) for $1,000.
4. **Task Priority Schedule:** `WATER > FEED_ANIMALS > HARVEST > PLANT` (Water-First scheduling).
5. **Market Broker Policy:** Max 10 orders/turn, premium-first queue (Milk/Wool > Melon > Carrot > Wheat).
6. **End-Game Liquidation Timing:** Day 25 Melon plant cutoff, Day 27+ inventory flush.

---

## 9. Variable Changed in E08

The sole primary experimental variable modified in E08 is:

> **`PRODUCTIVE SCALE`**
> - Target productive crop tiles increased from **24 to 40** (+66.7%).
> - Owned land utilization increased from **48.0% to 80.0%**.
> - Additional 16 tiles allocated conservatively to cash crops (+10 Melon tiles, +6 Carrot tiles).

---

## 10. Success Criteria

Primary local benchmark evaluation: **E08 vs E07** (30 paired controlled local episodes, 720 steps each, identical random seeds `seed = episode_idx * 100`).

### Measured Metrics
- Mean Final Money
- Standard Deviation (`ddof=1`)
- Median Final Money
- Paired Win / Equal / Loss count
- Productive tiles actually worked
- Land utilization rate (%)
- Worker productive turn %
- Worker movement turn %
- Terminal unused assets

### Success Thresholds
- **Architectural Success:** Substantial increase in actually productive land surface (from 24 to 40 tiles) with **100.0% completion rate** and **0 disqualifications**.
- **Economic Success:** Mean Final Money E08 > E07 (**>$15,364.57**).
- **Secondary Target:** Recover part of the performance gap toward E06 (**$25,180.30**) and E05 (**$21,485.87**).

---

## 11. Risks

1. **Movement Overhead:** Navigating across 40 tiles in Q0+Q1 could increase travel steps if spatial partitioning is unoptimized.
   *Mitigation:* Assign Farmer + Hand 1 to Q0 tiles, Hand 2 + Hand 3 to Q1 tiles.
2. **Watering Bottleneck on Dry Days:** On dry days, 40 tiles requiring water could delay lower-priority harvesting or planting actions.
   *Mitigation:* Enforce Water-First priority so no crops decay or convert to weeds.
3. **Upfront Seed Capital Liquidity:** Planting 40 tiles requires ~$500–$700 in seed investments.
   *Mitigation:* Stagger Q1 planting over Days 12–15 as early Melon/Carrot revenues arrive.

---

## 12. PLAN Recommendation & Decision

### Decision
> **`GO FOR PLAN`**

### Recommendation
Proceed immediately to **E08 PLAN** to formalize the implementation specification of `HybridLivestockClusterROIAgent` configured for 40 productive tiles (20 Q0 + 20 Q1), with spatial worker partitioning to control movement overhead and ensure a rapid Kaggle submission this evening.

---

<!-- END OF DOCUMENT -->
