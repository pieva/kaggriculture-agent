# PLAN Report — E11 3× Productive Mass Expansion

**Date:** 2026-08-26  
**Phase:** E11-02 PLAN  
**Status:** `PLANNED — AWAITING BUILD APPROVAL`  
**Primary Current Baseline:** E10-01 (`Q1CapitalProtectedROIAgent`, 40 tiles, 4 workers, Livestock OFF) — Mean Money: **$23,515.87**, SD: **$2,789.27**  
**Strategy File to Create:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Strategy Class:** `ProductiveMassROIAgent`  
**Architectural Core:** **"Mass first, efficiency second" — Full 100-Tile, 8–12 Worker, Multi-Crop & Livestock Scaling**  

---

## 1. Executive Summary

E11 marks a fundamental architectural paradigm shift for the Kaggriculture agent.

Prior iterations (E01–E10) focused on micro-optimizing scheduling and capital protection within narrow, fixed footprints (9 to 40 tiles, 2 to 4 workers, single land expansion). While E10-01 achieved zero catastrophic crashes and a low standard deviation ($2,789.27), its final economic output ($23,515.87) remains trapped at a local ceiling because ~60% of potential map resources and ~65% of labor capacity are left untouched.

The **E11-B0 Top Player Benchmark** confirmed a structural **~3.0× Productive Mass Gap** ($70,000–$75,000 top player mean vs $23,515.87 baseline). E11 is engineered from the ground up to close this gap by building a multi-quadrant, high-density workforce, multi-crop, and livestock production engine designed to achieve the **Competitive Target of $75,000 Mean Final Money**, using **$50,000 exclusively as the minimum success threshold**.

---

## 2. Corrected E11 Success Criteria & Classification Matrix

E11 does not intentionally target half the gap. The architecture is designed to target full competitive parity with top participants ($75,000).

```text
                                  E11 EVALUATION MATRIX
┌───────────────────────┬──────────────────────────────────┬────────────────────────────────────────────────┐
│   Mean Final Money    │        Evaluation Verdict        │            Strategic Interpretation            │
├───────────────────────┼──────────────────────────────────┼────────────────────────────────────────────────┤
│       < $50,000       │               FAIL               │ Mass expansion failed to generate scale.       │
│  $50,000 – <$60,000   │         MINIMUM SUCCESS          │ Minimum floor reached; strong residual gap.    │
│  $60,000 – <$70,000   │           COMPETITIVE            │ Competitive architecture; needs fine tuning.   │
│  $70,000 – <$75,000   │        NEAR TOP BENCHMARK        │ Parity nearly achieved with top benchmark.     │
│       ≥ $75,000       │         TARGET ACHIEVED          │ Full competitive parity with top benchmark.    │
│       > $75,000       │        BENCHMARK EXCEEDED        │ Exceeds top benchmark performance.             │
└───────────────────────┴──────────────────────────────────┴────────────────────────────────────────────────┘
```

- **Primary Baseline (E10-01):** Mean Final Money = **$23,515.87**
- **Minimum Success Threshold:** **Mean Final Money $\ge \$50,000.00$** (`+112.6%` vs E10-01)
- **Competitive Target:** **Mean Final Money $\ge \$75,000.00$** (`+218.9%` vs E10-01)

---

## 3. Architectural Objective: "Mass First, Efficiency Second"

Instead of tweaking parameters on 40 tiles, E11 builds a compounding **Growth Feedback Loop**:

$$\text{Production} \longrightarrow \text{Market Revenue} \longrightarrow \text{Available Capital} \longrightarrow \text{\{Land, Workforce, Seeds, Herd\}} \longrightarrow \text{Scaled Capacity} \longrightarrow \text{Higher Production}$$

```text
E10-01 Baseline Architecture                    E11 Productive Mass Architecture
┌───────────────────────────────┐               ┌─────────────────────────────────────────────────┐
│ 50 Tiles (Q0 + Q1)            │               │ 100 Tiles (Q0 + Q1 + Q2 + Q3)                   │
│ 40 Productive Crop Tiles      │  ──────────>  │ 75–90 Active Productive Tiles                   │
│ 4 Workers (1 Farmer + 3 Hands)│               │ 8–12 Workers (1 Farmer + 7–11 Hands)            │
│ 0 Animals (Livestock OFF)     │               │ Scaled Livestock (6–10 Cows, 4–6 Sheep)         │
│ Passive Cash Accumulation     │               │ Aggressive Reinvestment Engine                  │
└───────────────────────────────┘               └─────────────────────────────────────────────────┘
```

---

## 4. Environment Mechanics Relevant to Scaling

To design an unconstrained scaling policy, we leverage the exact parameters of the `kaggriculture` environment:

1. **Land Grid & Expansion:** 100 tiles total across 4 Quadrants (Q0: (0,0)-(4,4); Q1: (5,0)-(9,4); Q2: (0,5)-(4,9); Q3: (5,5)-(9,9)). `BUY_LAND` costs **$1,000.0** per quadrant.
2. **Workforce Cost Curve (`HIRE`):** First hire cost = $1, 2nd = $1, 3rd = $2, 4th = $3, 5th = $5, 6th = $8, 7th = $13, 8th = $21, 9th = $34, 10th = $55. Hiring 8 hands ($1+1+2+3+5+8+13+21 = \$54$ cumulative) is cheap relative to revenue generation.
3. **Crop Parameters (`CROPS`):**
   - `WHEAT`: Seed $10, Growth 4 days, Yield 6 units, Price $25 -> Revenue $150 (Net $140 / 4d = $35/day). Also serves as feed for Cow/Sheep.
   - `CARROT`: Seed $20, Growth 3 days, Yield 4 units, Price $35 -> Revenue $140 (Net $120 / 3d = $40/day). High liquidity crop.
   - `TOMATO`: Seed $50, Growth 8 days, Yield 5 units, Price $50 -> Revenue $250 (Net $200 / 8d = $25/day). Mid-game growth crop.
   - `STRAWBERRY`: Seed $100, Growth 10 days, Yield 4 units, Price $100 -> Revenue $400 (Net $300 / 10d = $30/day). High-yield crop.
   - `MELON`: Seed $80, Growth 12 days, Yield 1 unit, Price $250 -> Revenue $250 (Net $170 / 12d = $14.17/day). High single-unit cash dump.
4. **Livestock Engine Parameters:**
   - `COW`: Cost $400. Requires 5 pasture tiles. Consumes 1 Wheat/day. Produces Milk ($160 value) daily after maturity.
   - `SHEEP`: Cost $500. Requires 4 pasture tiles. Consumes 1 Wheat/day. Produces Wool ($200 value) daily after maturity.
5. **Market Limits:** Shed capacity = 100 items. Market order cap = 10 orders/turn. Market prices experience decay if over-supplied; premium-first queue protects margins.

---

## 5. Subsystem Design & Strategy

### 5.1 Land Expansion Strategy (4 Quadrants / 100 Tiles)

Rather than hard-coding expansion days (`if day == 12`), E11 implements **Dynamic Economic Expansion Triggers**:

- **Initial State:** Q0 (25 tiles) owned.
- **Q1 Expansion Trigger:** Execute `BUY_LAND` Q1 when:
  - Active planted tiles in Q0 $\ge 15$, AND
  - Liquid cash $\ge \$1,000.0 + \text{Operating Reserve } (\$200.0)$. (Typically achieved Day 4–6).
- **Q2 Expansion Trigger:** Execute `BUY_LAND` Q2 when:
  - Total active planted tiles in Q0+Q1 $\ge 30$, AND
  - Workforce $\ge 4$ workers, AND
  - Liquid cash $\ge \$1,000.0 + \text{Operating Reserve } (\$300.0)$. (Typically achieved Day 8–10).
- **Q3 Expansion Trigger:** Execute `BUY_LAND` Q3 when:
  - Total active planted tiles in Q0+Q1+Q2 $\ge 50$, AND
  - Workforce $\ge 6$ workers, AND
  - Liquid cash $\ge \$1,000.0 + \text{Operating Reserve } (\$400.0)$. (Typically achieved Day 12–14).

---

### 5.2 Workforce Scaling Strategy (8–12 Workers)

Workforce scaling is tied dynamically to active tile count and land expansion:

- **Target Ratio:** 1 worker for every 8–10 active productive tiles.
- **Hiring Triggers:** Execute `HIRE` at `hour == 0` when:
  - `(Total Active Tiles / Current Workers) > 8.0`, AND
  - `state.hires_today < max_hires_per_day`, AND
  - `cash - hire_cost >= operating_reserve`.
- **Workforce Growth Schedule:**
  - Day 1: Hire Hand 1 (2 workers total)
  - Day 3: Hire Hand 2 (3 workers total)
  - Day 5: Hire Hand 3 (4 workers total)
  - Day 7–8: Hire Hand 4 & Hand 5 (6 workers total)
  - Day 10–12: Hire Hand 6 & Hand 7 (8 workers total)
  - Day 13–15: Hire Hand 8 & Hand 9 (10 workers total)

---

### 5.3 Worker Locality & Quadrant Assignment

To solve the **travel time bottleneck** across 100 tiles, workers are assigned using a **Quadrant Locality Dispatcher**:

```text
           QUADRANT LOCALITY ASSIGNMENT (10x10 GRID)
 ┌─────────────────────────────┬─────────────────────────────┐
 │ Quadrant 0 (0,0) - (4,4)    │ Quadrant 1 (5,0) - (9,4)    │
 │ Assigned: Farmer + Hand 1   │ Assigned: Hand 2 + Hand 3   │
 ├─────────────────────────────┼─────────────────────────────┤
 │ Quadrant 2 (0,5) - (4,9)    │ Quadrant 3 (5,5) - (9,9)    │
 │ Assigned: Hand 4 + Hand 5   │ Assigned: Hand 6 + Hand 7+  │
 └─────────────────────────────┴─────────────────────────────┘
```

- **Local Scope Priority:** Each worker primarily services crop tiles within their designated quadrant boundaries.
- **Dynamic Spillover Assist:** A worker only crosses quadrant boundaries if their primary quadrant has zero pending `WATER` or `HARVEST` tasks and an adjacent quadrant has an urgent unwatered crop backlog.

---

### 5.4 Crop Portfolio Strategy

E11 replaces static 3-crop allocation with a **3-Tier Dynamic Crop Portfolio**:

1. **Liquidity Tier (`CARROT`):** 3-day growth cycle. Fast cash generation during Days 1–10 to finance HIRE and BUY_LAND.
2. **Growth & Revenue Tier (`TOMATO` / `MELON` / `STRAWBERRY`):**
   - `TOMATO` (8-day growth): Planted heavily on Days 4–15 for high mid-game liquidity.
   - `MELON` (12-day growth): Planted on Days 1–18 for massive end-game cash dumps.
   - `STRAWBERRY` (10-day growth): Planted on Days 5–18 as high-margin cash generator.
3. **Strategic Feed Tier (`WHEAT`):** 4-day growth cycle. 12–16 tiles dedicated to Wheat to supply Cow/Sheep feed loop + excess sold for steady market cash.

---

### 5.5 Livestock & Processing Engine Integration

Unlike E08 (where livestock failed due to lack of labor), E11 integrates livestock with dedicated labor:

- **Acquisition Triggers:** Buy Cows/Sheep when:
  - Quadrant 2 or 3 is unlocked (providing spatial room for pastures), AND
  - Wheat feed buffer $\ge \text{Herd Size} + 4$ units in shed/crop, AND
  - Liquid cash $\ge \text{Animal Cost} + \$300.0$.
- **Target Herd Size:** 6 Cows ($2,400) + 4 Sheep ($2,000).
- **Pasture Placement:** Pastures located in dedicated 5x5 blocks in Quadrants 2 and 3.
- **Product Sales Loop:** Farmer/Hands automatically harvest Milk ($160/unit) and Wool ($200/unit) daily and execute high-frequency sales via `MarketBroker`.

---

### 5.6 Capital Reinvestment Model

E11 partitions capital into 3 dynamic pools:

1. **Operating Reserve ($R_{op}$):** $200.0 (Days 1–5), $300.0 (Days 6–15), $400.0 (Days 16+). Minimum float never touched by optional seed/animal buys.
2. **Expansion & Investment Pool ($P_{exp}$):** $\max(0, \text{Cash} - R_{op})$. Priority order: `BUY_LAND` > `HIRE` > `LIVESTOCK` > `HIGH-ROI SEEDS`.
3. **Idle Cash Sinking Guard:** If liquid cash exceeds $1,500.0 before Day 20, the agent triggers immediate reinvestment into new tile planting, seed packs, or animal purchases.

---

### 5.7 Economic Phase Model (5 Lifecycle Phases)

```text
 ┌───────────────┐     ┌───────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌────────────────┐
 │ Phase A       │     │ Phase B           │     │ Phase C         │     │ Phase D         │     │ Phase E        │
 │ Bootstrap     │ ──> │ First Expansion   │ ──> │ Mass Scaling    │ ──> │ Full Mass Engine│ ──> │ Liquidation    │
 │ (Days 1–5)    │     │ (Days 6–10)       │     │ (Days 11–18)    │     │ (Days 19–26)    │     │ (Days 27–30)   │
 └───────────────┘     └───────────────────┘     └─────────────────┘     └─────────────────┘     └────────────────┘
```

- **Phase A (Bootstrap, Days 1–5):** Q0 active, 3 workers hired, Carrot/Wheat planting for immediate liquidity.
- **Phase B (First Expansion, Days 6–10):** `BUY_LAND` Q1 & Q2 executed. Workforce scaled to 6 workers. Tomato & Melon planting initiated.
- **Phase C (Mass Scaling, Days 11–18):** `BUY_LAND` Q3 executed. Workforce scaled to 8–10 workers. Livestock herd acquired (Cows + Sheep). Wheat feed loop active.
- **Phase D (Full Mass Engine, Days 19–26):** 75–90 active tiles across all 4 quadrants. Daily Milk/Wool/Crop harvesting and market sales.
- **Phase E (Liquidation, Days 27–30):** Planting cutoffs active. 100% shed inventory flush. No further capital expenditure.

---

### 5.8 5-Tier Action Priority Hierarchy

To manage 8–12 workers across 100 tiles without task collisions, starvation, or strategic interruption of urgent tasks:

```text
                           5-TIER ACTION DISPATCH HIERARCHY
┌───────────────────────────────────────┬────────────────────────────────────────────────────────┐
│ Tier 1 — Urgent Productive Actions    │ • Urgent Watering (prevents weed conversion)            │
│                                       │ • Time-critical Mature Crop Harvesting                 │
│                                       │ • Animal Feeding & Care                                │
│                                       │ • Time-critical Product Collection (Milk/Wool)         │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ Tier 2 — Productive Continuity        │ • Crop Planting & Replanting on empty tiles            │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ Tier 3 — Strategic Reinvestment       │ • Strategic Market Actions at hour == 0:               │
│                                       │   - BUY_LAND (when economic & labor ready)             │
│                                       │   - HIRE (when active tile backlog ready)              │
│                                       │   - Livestock Animal Buys (when feed ready)            │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ Tier 4 — Capacity Preparation         │ • Tile Weed DIG Remediation                            │
│                                       │ • Quadrant Locality-Guided Movement                    │
├───────────────────────────────────────┼────────────────────────────────────────────────────────┤
│ Tier 5 — PASS                         │ • Idle Fallback (no profitable action available)       │
└───────────────────────────────────────┴────────────────────────────────────────────────────────┘
```


---

## 6. Failure Modes & Safeguards

| Failure Mode | Root Cause | Safeguard / Indicator | Diagnostic Metric |
| :--- | :--- | :--- | :--- |
| **Overexpansion** | Buying Q2/Q3 without workers to tend tiles. | Block `BUY_LAND` unless `workers >= 2 * owned_quadrants`. | `unwatered_tiles_count > 5` |
| **Overhiring** | Hiring hands when cash is low or tiles are few. | Block `HIRE` if `cash - hire_cost < R_op` or `active_tiles/worker < 6`. | `idle_worker_turns > 20%` |
| **Liquidity Collapse** | Spending all cash on land/animals, leaving $0 for seeds. | Enforce inviolable $300 Operating Reserve $R_{op}$. | `min_cash_balance < $200` |
| **Premature Livestock** | Buying Cows/Sheep before Wheat feed buffer is ready. | Require Wheat shed count $\ge \text{Herd Size} + 4$ before animal purchase. | `starved_animals_count > 0` |
| **Travel Dilution** | Workers running across 10x10 map. | Enforce Quadrant Locality Dispatcher. | `movement_share > 50%` |
| **Idle Capital** | Holding > $2,000 cash doing nothing in mid-game. | Trigger automatic seed/worker/land expansion when cash > $1,500 on Days 1–20. | `idle_cash_over_1500_days` |
| **End-Game Overinvestment** | Buying Melons/Cows on Day 25 that won't yield before Day 30. | Enforce rigid horizon cutoffs (Melon Day 18, Animals Day 20, All Plant Day 26). | `unharvested_crop_units` |

---

## 7. Telemetry & Instrumentation Specification

`ProductiveMassROIAgent` will instrument the following diagnostic metrics:

- `checkpoints_money`: Cash at Day 7, Day 15, Day 22, Day 30.
- `quadrants_owned_history`: Days when Q1, Q2, Q3 were purchased.
- `active_productive_tiles_history`: Daily active productive tile count.
- `workforce_history`: Daily worker count.
- `livestock_counts`: Daily count of Cows and Sheep.
- `capital_allocation`: Cumulative breakdown of spending on Land, Workforce, Seeds, Livestock.
- `revenue_breakdown`: Realized revenue from Melon, Carrot, Tomato, Strawberry, Wheat, Milk, Wool.
- `movement_share`: Percentage of worker actions spent moving vs productive work.

---

## 8. Implementation & Class Architecture Plan

### 8.1 New Strategy File
- **File Path:** `src/agricola/strategy/productive_mass_roi.py`
- **Class Name:** `ProductiveMassROIAgent`

### 8.2 Decoupled Helper Modules (if needed)
- `QuadrantLocalityDispatcher`: Manages spatial bounds and worker quadrant assignments.
- `DynamicReinvestmentBroker`: Manages capital allocation, land expansion triggers, and hiring.

### 8.3 Unit & Integration Test Plan (`experiments/archive/e11/tests/test_e11_productive_mass.py`)
1. Test initialization of 100-tile layout model.
2. Test dynamic `BUY_LAND` Q1, Q2, Q3 expansion triggers.
3. Test dynamic workforce scaling (8–10 workers).
4. Test Quadrant Locality Dispatcher worker assignment.
5. Test Wheat feed balance guard and Cow/Sheep acquisition.
6. Test end-game liquidation cutoff enforcement.

---

## 9. Expected Trajectory & Verification Criteria

```text
                                EXPECTED MONEY TRAJECTORY
  $80k ─────────────────────────────────────────────────────────────────────────── Competitive Target ($75k)
  $70k ─────────────────────────────────────────────────────────────────── * * * 
  $60k ───────────────────────────────────────────────────────── * * * 
  $50k ─────────────────────────────────────────────── * * * ────────────────────── Minimum Success Threshold ($50k)
  $40k ───────────────────────────────────── * * * 
  $30k ─────────────────────────── * * * 
  $20k ───────────────── * * * ─────────────────────────────────────────────────── E10-01 Baseline ($23.5k)
  $10k ─────── * * * 
    $0 ─── * 
       Day 1    Day 7    Day 15   Day 22   Day 30
```

### BUILD & VERIFY Acceptance Criteria:
- **`FAIL`**: Mean Final Money $< \$50,000.00$
- **`MINIMUM SUCCESS`**: Mean Final Money $\ge \$50,000.00$
- **`COMPETITIVE TARGET ACHIEVED`**: Mean Final Money $\ge \$75,000.00$

---

## 10. Open Questions & Risks

1. **Kaggle Environments Memory / Latency Limit:** Running 10–12 workers generating actions per turn must remain well within the 60.0s overage time limit and $< 1.0\text{ ms/turn}$ latency. (Python dictionary lookups are fast, but pathfinding across 100 tiles must use Manhattan distance grid math).
2. **Opponent Interference:** High-tier opponents may buy land or seeds aggressively; `MarketBroker` must handle variable market price decay dynamically.

---

<!-- END OF FILE -->
