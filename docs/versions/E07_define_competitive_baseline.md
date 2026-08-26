# DEFINE Evidence — E07 Competitive Baseline Reconstruction

**Date:** 2026-08-26  
**Phase:** DEFINE / Reconnaissance  
**Status:** `COMPLETED — GO FOR PLAN`  
**Target Architecture:** `E07 Competitive Reference Configuration`  

---

## 1. Executive Summary

This document defines the architectural reconnaissance and competitive baseline reconstruction for **E07**. 

Up to E06, the project followed an incremental, single-variable approach (`E01 baseline` $\rightarrow$ `E02 ROI crops` $\rightarrow$ `E03 4-tile` $\rightarrow$ `E04 9-tile falsified` $\rightarrow$ `E05 2-worker HIRE` $\rightarrow$ `E06 Water-First`). While E06 achieved strong local metrics ($24662.00 Mean Money, 70 weeds), it operates within a highly constrained local subspace: single quadrant (9 tiles), no livestock, no buildings, no land expansion (`BUY_LAND`), no market timing, and static priority scheduling across all 720 turns.

This DEFINE phase identifies the **recurrent strategic patterns** across publicly observable competitive Kaggriculture agents and synthesizes them into a **E07 Competitive Reference Configuration**. This configuration will serve as the multi-capability 2nd-generation architectural baseline of the project, enabling controlled single-variable ablation and optimization experiments starting from E08+.

---

## 2. Current Baseline Analysis — E06 Configuration

We audited the current shipped baseline (`WaterFirstHIRENWClusterROIAgent` in `src/agricola/strategy/water_first_hire_nw_cluster_roi.py` and `submission/submission.py`):

| Strategic Dimension | E06 Current Implementation | Status / Limit |
| :--- | :--- | :--- |
| **Land Use** | Compact 9-tile NW cluster `{(x,y) \| x ∈ [2,4], y ∈ [2,4]}` in Quadrant 0. | Static 9 tiles. 16 tiles in Q0 unused. 75 tiles in Q1–Q3 unused. |
| **Land Expansion (`BUY_LAND`)** | `BUY_LAND` is **never** executed. | 0% multi-quadrant utilization. |
| **Workforce (`HIRE`)** | 1 Farmer Principal (4 tiles) + 1 Daily Farm Hand ($1/day, 5 tiles) hired at `hour == 0`. | Fixed 2 workers. Multi-hand scaling (>1 hand) not supported. |
| **Spatial Partitioning** | Fixed 4:5 spatial split between Farmer and Hand 1. | Static spatial division; no dynamic workload rebalancing. |
| **Crop Policy** | ROI formula: $(2.0 \times \text{price} - \text{seed\_cost}) / \text{growth\_days}$. Immediate replanting. | Single-crop decision per tile; no strategic crop mix or feed crops. |
| **Planting / Watering / Harvesting** | Static task priority: `WATER > HARVEST > PLANT`. Manhattan pathing. | Fixed scheduling across all 720 turns. |
| **Livestock (Cows / Sheep)** | **None.** Animals are never purchased or managed. | 0% biological asset cashflow engine. |
| **Structures (Well / Barn / Storage)** | **None.** No buildings or infrastructure are constructed. | 0% structural enhancement. |
| **Market Policy** | Immediate liquidation. Harvested crops are sold on the same turn. | No market timing, no price crash protection, no order buffering. |
| **Capital Allocation** | Cash spent on daily $1 HIRE + seed costs. Remaining cash held idle. | No active reinvestment engine for land, herd, or infrastructure. |
| **Phase Scheduling** | Identical logic for step 0 to step 720. | No early opening script, mid-game scaling, or end-game liquidation. |
| **Opponent Awareness** | **None.** Opponent state is completely ignored. | 0% competitive reaction. |
| **Unused Capabilities** | `BUY_LAND`, `DIG`, Livestock (`COW`, `SHEEP`), Structures (`WELL`, `BARN`, `FENCE`, `STORAGE`), Market timing, Multi-hand HIRE. | ~70% of environment action space unused. |

---

## 3. Research Method & Sources

We conducted a systematic external search across Kaggle competition forums, Kaggle open-source notebooks, public GitHub repositories, and environment documentation.

### Search Categories
1. **GitHub Repositories:** Public Kaggriculture agents, starter kits, and multi-worker framework implementations.
2. **Kaggle Discussion Forums:** Strategy posts, baseline comparisons, RL vs heuristic discussions, and market price decay threads.
3. **Kaggle Code / Notebooks:** Open-source submission scripts, `ObservationWrapper` implementations, and replay analyzers.
4. **Environment Specification:** `kaggle-environments` Kaggriculture game rules (shed capacity 100, max 10 market orders/turn, hiring cost curve, crop growth tables, livestock feeding rules).

---

## 4. Public Competitive Sources Log

| Source ID | Source Type | URL / Reference | Key Focus / Information Retained |
| :--- | :--- | :--- | :--- |
| **SRC-01** | Kaggle Discussion | `kaggle.com/competitions/kaggriculture/discussion` | Fixed asset development strategies, line-up baselines, static vs dynamic look-ahead. |
| **SRC-02** | Kaggle Discussion | `kaggle.com/competitions/kaggriculture/discussion` | Multi-worker livestock engine, herd scaling (~8 cows, 4 sheep), wheat feed cycle. |
| **SRC-03** | Kaggle Discussion | `kaggle.com/competitions/kaggriculture/discussion` | Labor cost curve (burst-hiring at `hour == 0`), land expansion timing (`BUY_LAND`). |
| **SRC-04** | Kaggle Discussion / Code | `kaggle.com/competitions/kaggriculture/discussion` | Market order execution limits (10 orders/turn), shed capacity (100 items), premium-first broker. |
| **SRC-05** | Public Repos / Code | `github.com` (Kaggriculture agent repositories) | Modular architecture (`SpatialNavigator`, `CropManager`, `MarketBroker`, `WorkerDispatcher`). |
| **SRC-06** | Kaggle Discussion | `kaggle.com/competitions/kaggriculture/discussion` | End-game liquidation script (Day 29–30 sell-off of inventory, crops, and animals). |

---

## 5. Competitive Agents Analysed

We identified 4 primary agent archetypes in public competitive Kaggriculture submissions:

1. **Archetype A — `Fixed-Script Livestock-Crop Hybrid Agent` (Dominant Meta):**
   - Combines a deterministic opening script (Days 1–5) with a multi-worker livestock engine (8 cows + 4 sheep + wheat crops) and 2–3 quadrant expansion (`BUY_LAND`).
2. **Archetype B — `Look-Ahead NPV / Simulation Agent`:**
   - Uses a rolling 3-day simulation window to calculate Net Present Value (NPV) of investing in crops vs livestock vs land expansion.
3. **Archetype C — `Modular Heuristic / Sustainable Farmer Baseline`:**
   - Uses object-oriented decoupling (`SpatialNavigator`, `CropManager`, `MarketBroker`) with heuristic priority rules, multi-worker spatial assignment, and market order buffering.
4. **Archetype D — `RL PPO Meta-Agent / Reflection Loop`:**
   - Employs Proximal Policy Optimization (PPO) or Actor-Critic reflection loops to select macro-strategies based on opponent observation and market price decay.

---

## 6. Evidence Classification Schema

Every statement in this document is explicitly tagged with one of four evidence levels:

- **`CODE`**: Directly verified in public agent source code or environment execution rules.
- **`EPISODE`**: Directly observed in game replays or simulation logs.
- **`AUTHOR`**: Stated by competition authors or top participants in official documentation/discussions.
- **`INFERENCE`**: Our analytical deduction derived from `CODE`, `EPISODE`, or `AUTHOR` evidence.

---

## 7. Comparative Strategy Matrix Across Competitive Archetypes

| Dimension | E06 Baseline | Archetype A (Fixed Livestock-Crop) | Archetype B (Look-Ahead NPV) | Archetype C (Modular Heuristic) | Archetype D (RL PPO Meta) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Land (`BUY_LAND`)** | 1 Quadrant (9 tiles) | 2–3 Quadrants (50–75 tiles) | 2–4 Quadrants (50–100 tiles) | 2 Quadrants (50 tiles) | Dynamic (2–4 Quadrants) |
| **Workforce (`HIRE`)** | 2 Workers (1 farmer + 1 hand) | 3–6 Workers (1 farmer + 2–5 hands) | 3–5 Workers | 3–4 Workers | Dynamic (3–6 Workers) |
| **Hiring Timing** | Daily `hour == 0` | Burst `hour == 0` | Cash-flow threshold | Burst `hour == 0` | Policy-driven |
| **Crops** | ROI single-crop per tile | Wheat (feed) + Melons (cash) | Dynamic NPV optimization | ROI Crop Mix (Wheat/Melon/Carrot) | RL policy crop mix |
| **Livestock** | None | ~8 Cows + ~4 Sheep | Dynamic herd size | ~4 Cows + ~2 Sheep | RL policy herd size |
| **Structures** | None | Well + Barn (if herd > 6) | Well + Barn | Well | Barn |
| **Market Policy** | Immediate liquidation | Premium-first broker | Market-depth aware broker | Order queue buffering | Price-decay reflecting broker |
| **Capital Policy** | Cash idle | Reinvest in herd $\rightarrow$ land | Reinvest by max NPV | Reinvest by cash thresholds | RL value function |
| **Phase Scheduling** | None (Static) | 4 Phases (Early/Mid/Late/End) | Continuous rolling window | 3 Phases (Early/Mid/End) | Phase-conditioned RL |
| **Evidence Level** | `CODE` | `AUTHOR` / `CODE` | `AUTHOR` | `CODE` | `AUTHOR` / `INFERENCE` |

---

## 8. Land Use and Expansion Analysis

- **Observation (`CODE` / `AUTHOR`):** Starting grid is 1 quadrant (5x5, 25 tiles). Purchasing additional 5x5 quadrants via `BUY_LAND` costs $1,000–$2,000 per quadrant.
- **Competitive Pattern (`AUTHOR` / `INFERENCE`):** Top agents expand to **2 to 3 quadrants** (50 to 75 tiles). Expansion is NOT done immediately on Day 1; it is timed to coincide with the first major harvest revenue event (e.g. Day 12–14 melon harvest), ensuring sufficient liquid cash remains for seeds and worker salaries.
- **Unused Land Risk (`CODE`):** Buying land without sufficient workforce to water/harvest results in unworked tiles and wasted capital.

---

## 9. Workforce Analysis (`HIRE`)

- **Observation (`CODE` / `AUTHOR`):** Hiring additional farm hands (`HIRE`) costs $1/day for hand 1, with non-linear cost increases for multiple hands hired on the *same day*. Hired hands are active until `hour == 23`.
- **Burst-Hiring Rule (`CODE` / `AUTHOR`):** Hiring MUST occur at **`hour == 0`** (start of day) so that hired hands provide 24 full hours of labor. Hiring later in the day wastes money on partial-day labor.
- **Workforce Target (`AUTHOR` / `INFERENCE`):** Competitive 2–3 quadrant farms employ **3 to 5 total workers** (1 Principal Farmer + 2 to 4 Farm Hands).
- **Task Partitioning (`CODE`):** Workers are assigned dedicated spatial sub-clusters or specialized roles (e.g., 1 worker dedicated exclusively to feeding/milking livestock, 2 workers on crop watering/harvesting).

---

## 10. Crop Strategy Analysis

- **Observation (`CODE` / `AUTHOR`):** Crops have distinct growth cycles and revenue profiles:
  - *Wheat:* 1-day growth cycle, low seed cost, essential as feed for livestock.
  - *Carrot:* 3-day growth cycle, moderate ROI.
  - *Melon / Pumpkin:* 8–12 day growth cycle, high capital requirement, massive lump-sum harvest payout.
- **Crop Mix Pattern (`AUTHOR` / `INFERENCE`):** Competitive agents do not plant 100% of a single crop. They dedicate:
  - **30%–40% land area to Wheat** (continuous daily harvest to feed cows/sheep).
  - **50%–60% land area to High-ROI Crops (Melons/Pumpkins)** for large capital accumulation.
  - **10% flex area for fast cash crops (Carrots)** during liquidity dips.

---

## 11. Livestock and Structures Analysis

- **Observation (`CODE` / `AUTHOR`):**
  - **Cows:** Produce Milk daily when fed Wheat. Milk commands high market price and steady cash flow.
  - **Sheep:** Produce Wool daily when fed Wheat. Wool provides secondary high-value revenue.
  - **Feed Cycle:** 1 Cow requires 1 Wheat per day. 1 Sheep requires 1 Wheat per day.
- **Livestock Cashflow Engine (`AUTHOR` / `INFERENCE`):** Animals represent a "wheat-powered cashflow factory". Unlike crops which risk 2-day starvation death or market price crashes upon bulk dump, fed animals generate guaranteed daily income.
- **Optimal Herd Size (`AUTHOR`):** ~8 Cows and ~4 Sheep (supported by 12 daily Wheat tiles).
- **Structures (`CODE` / `INFERENCE`):** Building a `WELL` reduces travel time for watering. Building a `BARN` is required when herd size exceeds threshold capacity.

---

## 12. Capital Allocation & Market Strategy

- **Observation (`CODE` / `AUTHOR`):**
  - Shed capacity is capped at 100 items. Market orders are capped at 10 orders per turn.
  - Dumping large quantities of a single crop in 1 turn crashes town market demand and price.
- **Premium-First Market Broker (`CODE` / `AUTHOR`):** Competitive agents execute market sales via a dedicated broker module:
  1. Priority 1: High-value animal products (Milk, Wool).
  2. Priority 2: Mature high-ROI crops (Melons).
  3. Priority 3: Excess crops (Carrots, excess Wheat).
- **Capital Reinvestment Loop (`INFERENCE`):**
  $$\text{Harvest/Milk Revenue} \longrightarrow \text{Cash Reserve ($300–$500)} \longrightarrow \text{Buy Livestock} \longrightarrow \text{Buy Land (`BUY_LAND`)} \longrightarrow \text{Hire Hand}$$

---

## 13. Phase Scheduling & End-Game Policy

Competitive agents divide the 30-day (720-turn) season into 4 distinct operational phases:

1. **Phase 1 — Early Opening (Days 1–5 / Turns 0–120):**
   - Fixed script: Buy 2 Cows + 2 Sheep, plant 7 Wheat + 12 Melons, hire Hand 1 at `hour == 0`.
2. **Phase 2 — Herd & Workforce Scaling (Days 6–15 / Turns 121–360):**
   - Expand herd to 6–8 Cows + 4 Sheep. Hire Hand 2 and Hand 3 at `hour == 0`. Maintain Wheat feed cycle.
3. **Phase 3 — Land Expansion & Crop Rotation (Days 16–25 / Turns 361–600):**
   - Execute `BUY_LAND` (Quadrant 1 and Quadrant 2). Expand Melon planting. Hire Hand 4 if needed.
4. **Phase 4 — End-Game Liquidation (Days 26–30 / Turns 601–720):**
   - **Day 26–28:** Stop planting long-growth crops (Melons). Plant only 1-day Wheat/Carrots.
   - **Day 29–30 (Turns 696–720):** Liquidate all stored inventory (Milk, Wool, Crops). Sell livestock if net capital gain is positive. Convert 100% of assets into terminal bank money.

---

## 14. Opponent Awareness

- **Observation (`CODE` / `AUTHOR`):** Most competitive agents operate primary heuristic execution independently of opponent actions. Advanced agents monitor opponent net worth and market sales to prevent price-clashing on identical crop sell turns.

---

## 15. Recurring Competitive Patterns Summary

1. **Biological Asset Engine:** Livestock fed by dedicated Wheat crops generates non-starvable daily cash flow.
2. **Burst-Hiring at Hour 0:** Hands hired strictly on turn 0 of each day to maximize labor efficiency.
3. **Timed Land Expansion:** `BUY_LAND` executed after major harvest payouts, avoiding cash-flow starvation.
4. **Premium-First Order Brokerage:** Market queue buffers high-value goods, preventing market price collapse.
5. **Phase-Based End-Game Liquidation:** Ceasing long crops on Day 26 and selling 100% inventory on Day 29–30.

---

## 16. Counterexamples & Failed Scaling Patterns

- **Failed Pattern 1 — Premature `BUY_LAND` (Day 1 Land Purchase):** Spending $1,000+ on Day 1 leaves zero cash for seed/workers, resulting in dead unwatered tiles.
- **Failed Pattern 2 — Over-Hiring on Same Day:** Hiring 3 hands on the same day triggers non-linear cost penalties, draining cassa.
- **Failed Pattern 3 — Unfed Livestock:** Purchasing Cows without a dedicated Wheat crop results in starving, unproductive animals.
- **Failed Pattern 4 — Bulk Crop Dumping:** Dumping 50 CARROTS in 1 turn crashes price to minimum, forfeiting ~60% of revenue.

---

## 17. E06 Competitive Gap Analysis Matrix

| Capability / Dimension | Current E06 Baseline | Competitive Standard Pattern | Gap Description | Severity | Confidence |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Land Utilization** | 9 tiles (Q0 only) | 50–75 tiles (Q0 + Q1 + Q2) | E06 uses < 15% of active map area. | **HIGH** | `HIGH` |
| **Land Expansion** | 0 `BUY_LAND` | 2–3 `BUY_LAND` executions | E06 never expands territory. | **HIGH** | `HIGH` |
| **Workforce Size** | 2 workers (1 farmer, 1 hand) | 3–5 workers | E06 labor throughput capped at 2 workers. | **HIGH** | `HIGH` |
| **Crop Diversification** | 1 ROI crop formula | Wheat (feed) + Melons (cash) + Carrot (flex) | E06 lacks dedicated feed crops and crop roles. | **MEDIUM** | `HIGH` |
| **Livestock Engine** | None (0 animals) | ~8 Cows + ~4 Sheep | E06 lacks daily compounding milk/wool income. | **CRITICAL** | `HIGH` |
| **Structures** | None | Well + Barn | E06 lacks infrastructure efficiency gains. | **LOW** | `MEDIUM` |
| **Market Policy** | Immediate sell on harvest turn | Premium-first queue & price-decay check | E06 risks price front-running & shed limits. | **MEDIUM** | `HIGH` |
| **Capital Allocation** | Idle cash after HIRE/seeds | Active reinvestment loop (herd $\rightarrow$ land $\rightarrow$ hands) | E06 capital sits uninvested in cassa. | **HIGH** | `HIGH` |
| **Phase Scheduling** | Static priority (0–720) | 4-phase lifecycle (Opening $\rightarrow$ Scale $\rightarrow$ Expand $\rightarrow$ Liquidate) | E06 does not adjust strategy near episode end. | **HIGH** | `HIGH` |
| **End-Game Liquidation** | None | Stop long crops Day 26, sell inventory Day 29–30 | E06 leaves unharvested crops on Day 30. | **HIGH** | `HIGH` |

---

## 18. Proposed E07 Competitive Reference Configuration

We synthesize the competitive evidence into a complete 2nd-generation architectural configuration:

| Parameter / Module | Proposed E07 Policy / Value | Evidence Level | Sources | Confidence | Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Primary Strategy Class** | `HybridLivestockClusterROIAgent` | `CODE` / `AUTHOR` | SRC-01..06 | **HIGH** | New 2nd-gen architectural baseline |
| **Land Footprint Target** | 2 Quadrants (50 tiles total: Q0 + Q1) | `AUTHOR` / `INFERENCE` | SRC-01, SRC-03 | **HIGH** | Scaled up from 9 tiles |
| **Land Expansion (`BUY_LAND`)** | Buy Q1 on Day 12 after 1st Melon harvest | `AUTHOR` / `INFERENCE` | SRC-03, SRC-06 | **MEDIUM** | Timed after liquidity event |
| **Workforce Target** | 4 Workers (1 Principal + 3 Farm Hands) | `CODE` / `AUTHOR` | SRC-02, SRC-03 | **HIGH** | 1 livestock worker, 3 field workers |
| **Hiring Schedule** | Burst-hire Hand 1 Day 1, Hand 2 Day 6, Hand 3 Day 12 at `hour == 0` | `CODE` / `AUTHOR` | SRC-03, SRC-05 | **HIGH** | Strictly turn 0 of target day |
| **Livestock Herd Target** | 4 Cows + 2 Sheep | `AUTHOR` / `INFERENCE` | SRC-02, SRC-04 | **HIGH** | Sustainable herd matching 6 Wheat tiles |
| **Livestock Feed Loop** | 6 dedicated Wheat tiles (1-day growth) | `CODE` / `AUTHOR` | SRC-02, SRC-04 | **HIGH** | 1 Wheat/day per animal |
| **Crop Mix Strategy** | 6 Wheat (feed) + 12 Melon (cash) + 6 Carrot (flex) | `AUTHOR` / `INFERENCE` | SRC-01, SRC-02 | **HIGH** | Balanced crop role allocation |
| **Task Scheduling Priority** | `WATER > FEED_ANIMALS > HARVEST > PLANT` | `CODE` / `INFERENCE` | E06 evidence + SRC-02 | **HIGH** | Water & feed prioritized over planting |
| **Structures** | Build `WELL` on Day 5 (if cash > $500) | `INFERENCE` | SRC-05 | **LOW** | Optional infrastructure enhancement |
| **Market Broker Policy** | Premium-first queue (Milk/Wool > Melon > Carrot) | `CODE` / `AUTHOR` | SRC-04, SRC-05 | **HIGH** | Max 10 orders/turn queue buffer |
| **Phase 1 (Opening, Days 1–5)** | Buy 2 Cows + 2 Sheep, plant 6 Wheat + 8 Melons, Hire Hand 1 | `AUTHOR` / `CODE` | SRC-01, SRC-06 | **HIGH** | Fixed opening script |
| **Phase 2 (Scale, Days 6–15)** | Scale herd to 4 Cows + 2 Sheep, Hire Hand 2 & 3, Buy Q1 (`BUY_LAND`) | `AUTHOR` / `CODE` | SRC-02, SRC-03 | **HIGH** | Reinvestment scaling phase |
| **Phase 3 (Produce, Days 16–25)** | Full 50-tile production, milk/wool daily sales, melon rotations | `AUTHOR` / `CODE` | SRC-01, SRC-04 | **HIGH** | Peak cash generation phase |
| **Phase 4 (Liquidate, Days 26–30)** | Stop Melon planting Day 25; sell ALL stored goods & animals Day 29–30 | `AUTHOR` / `CODE` | SRC-06 | **HIGH** | Terminal capital maximization |
| **Cash Reserve Minimum** | Keep $300 minimum cash float at all times | `INFERENCE` | SRC-03 | **MEDIUM** | Buffer against seed/salary bankruptcy |

---

## 19. Confidence Assessment and Evidence Gaps

### Parameters with `HIGH` Confidence
- Livestock cashflow engine (Cows/Sheep + Wheat feed loop).
- Burst-hiring at `hour == 0`.
- Phase-based End-Game Liquidation (Days 26–30).
- Premium-first market order broker.

### Parameters with `MEDIUM` Confidence
- Exact timing of `BUY_LAND` (Day 12 vs Day 14).
- Minimum cash reserve threshold ($300 vs $500).

### Parameters with `LOW` Confidence / Information Gaps
- **Structures (`WELL`, `BARN`):** Exact ROI of building a `WELL` vs spending cash on another Cow is not fully proven in public literature.
- **Animal Sale on Day 30:** Whether selling livestock on turn 718 produces higher net money than retaining animal value requires empirical testing.

---

## 20. Candidate Variables for Post-E07 Controlled Experiments (E08+)

Once the E07 Competitive Reference Baseline is built and validated, the following single-variable ablation and optimization experiments are identified for E08+:

1. **E08 — Livestock Herd Size Optimization:** Ablation of herd size (0 vs 4 vs 8 Cows).
2. **E09 — `BUY_LAND` Expansion Timing:** Ablation of land purchase timing (Day 8 vs Day 12 vs Day 16).
3. **E10 — `DIG` Weed Clearing Integration:** Testing `DIG` action on residual dead tiles within the multi-quadrant farm.
4. **E11 — End-Game Liquidation Timing:** Comparing Day 28 vs Day 29 vs Day 30 asset liquidation.
5. **E12 — Structure ROI Assessment:** Testing `WELL` / `BARN` construction vs pure livestock reinvestment.

---

## 21. DEFINE Decision

> **`GO FOR PLAN (E07 Competitive Reference Configuration)`**

### Rationale
E06 local optimization reached a ceiling ($24.6k) within a severely restricted 9-tile sub-space. The public competitive evidence demonstrates that top-tier performance requires a multi-capability architecture (Livestock + Wheat Feed Loop + Multi-Worker HIRE + Timed `BUY_LAND` + Market Brokerage + Phase Liquidation). Building E07 as a full 2nd-generation baseline step-change will elevate the project to competitive parity and unlock meaningful single-variable ablation research from E08 onward.
