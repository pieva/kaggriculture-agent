# E08 — PLAN Productive Scale Optimization

**Phase:** `E08-02 — PLAN Productive Scale Optimization`  
**Date:** 2026-08-26  
**Status:** `PLAN COMPLETED`  
**Decision:** **`GO FOR BUILD`**  
**Target Class:** `HybridLivestockClusterROIAgent` (with E08 40-Tile Scale & Spatial Worker Partitioning)  

---

## Executive Summary

This plan formalizes the technical implementation details for **E08 Productive Scale Optimization**.
The primary objective of E08 is to scale the target productive crop surface from **24 to 40 tiles** (+66.7%) on owned territory (Q0 + Q1 = 50 tiles), raising land utilization from **48.0% to 80.0%**, while freezing workforce size (4 workers: 1 Farmer + 3 Hands) and livestock/expansion parameters.

To prevent the increased surface area from causing high movement overhead, E08 introduces a **Spatial Worker Partitioning Scheme** in `TaskDispatcher`, dividing the 4 workers between Q0 and Q1.

---

## 1. Experimental Delta: E07 $\rightarrow$ E08

| Feature / Parameter | E07 Baseline | E08 Implementation | Rationale |
| :--- | :--- | :--- | :--- |
| **Target Productive Tiles** | `24` (9 Q0 + 15 Q1) | **`40` (20 Q0 + 20 Q1)** | Eliminates 16 idle owned tiles (+66.7% productive surface) |
| **Land Utilization** | `48.0%` (24/50) | **`80.0%` (40/50)** | Monetizes $1,000 Q1 land investment |
| **Crop Role Allocation** | 6 Wheat, 12 Melon, 6 Carrot | **6 Wheat, 22 Melon, 12 Carrot** | Establishes +10 Melon cash tiles, +6 Carrot flex tiles |
| **Worker Partitioning** | Global unconstrained travel | **Spatial Partitioning (Q0 vs Q1)** | Farmer+Hand1 in Q0; Hand2+Hand3 in Q1 (movement <38%) |
| **Q1 Seed Purchasing** | Instant full-plot purchase | **Staggered Reinvestment** | Prevents cash float depletion (<$300) on Day 12 |
| **Workforce Target** | 4 (1 Farmer + 3 Hands) | **4 (1 Farmer + 3 Hands)** | **FROZEN** (96 turns/day, 54.2% productive load E07 estimate) |
| **Livestock Target** | 4 Cows, 2 Sheep | **4 Cows, 2 Sheep** | **FROZEN** (6 dedicated Wheat tiles feed loop) |
| **Expansion Timing** | Day 12 (Q1 $1,000) | **Day 12 (Q1 $1,000)** | **FROZEN** (Melon cashflow reinvestment) |
| **Task Priority** | Water-First | **Water-First** | **FROZEN** (`WATER > FEED > HARVEST > PLANT`) |

---

## 2. Spatial Grid Layout & Crop Allocation (40 Productive Tiles)

The requirement for E08 is **40 productive tiles (80% utilization of 50 owned tiles)**. The initial layout partitioning across Quadrant 0 (NW) and Quadrant 1 (NE) is structured as follows:

### Quadrant 0 (25 Tiles: $(x,y)$ where $x \in [0,4], y \in [0,4]$)
- **Infrastructure & Livestock (5 tiles):**
  - Pastures: $(0,0), (0,1), (1,0), (1,1), (0,2)$ (housing Cows & Sheep)
- **Active Crop Tiles in Q0 (20 tiles):**
  - **6 Wheat Tiles (Feed):** $(1,2), (1,3), (1,4), (2,0), (2,1), (2,2)$
  - **8 Melon Tiles (Cash):** $(2,3), (2,4), (3,0), (3,1), (3,2), (3,3), (3,4), (4,0)$
  - **6 Carrot Tiles (Flex):** $(4,1), (4,2), (4,3), (4,4), (0,3), (0,4)$

### Quadrant 1 (25 Tiles: $(x,y)$ where $x \in [5,9], y \in [0,4]$)
- **Active Crop Tiles in Q1 (20 tiles):**
  - **14 Melon Tiles (Cash):** $(5,0), (5,1), (5,2), (5,3), (5,4), (6,0), (6,1), (6,2), (6,3), (6,4), (7,0), (7,1), (7,2), (7,3)$
  - **6 Carrot Tiles (Flex):** $(7,4), (8,0), (8,1), (8,2), (8,3), (8,4)$
- **Flex Buffer Tiles in Q1 (5 tiles):**
  - $(9,0), (9,1), (9,2), (9,3), (9,4)$ (reserved for pathing/future buffer)

---

## 3. Spatial Worker Partitioning Scheme

To optimize worker transit across the expanded 40-tile footprint, `TaskDispatcher` will enforce spatial worker partitioning (with target movement share <38%):

```text
                     QUADRANT 0 (NW)                       QUADRANT 1 (NE)
                y ∈ [0, 4] (25 tiles)                 y ∈ [5, 9] (25 tiles)
           ┌─────────────────────────────┐       ┌─────────────────────────────┐
           │ Worker 0 (Farmer Principal) │       │ Worker 2 (Farm Hand 2)      │
           │ Worker 1 (Farm Hand 1)      │       │ Worker 3 (Farm Hand 3)      │
           │                             │       │                             │
           │ Focus:                      │       │ Focus:                      │
           │ • Q0 Crop Watering/Harvest  │       │ • Q1 Melon/Carrot Planting  │
           │ • Wheat Feed Loop           │       │ • Q1 Crop Watering          │
           │ • Animal Feeding & Pastures │       │ • Q1 Crop Harvesting        │
           │ • Shed Pickup/Deposit       │       │                             │
           └──────────────┬──────────────┘       └──────────────┬──────────────┘
                          │                                     │
                          └───────────── PENDING ───────────────┘
                                     WATER ASSIST
```

### Dispatch Rules
1. **Primary Assignment:**
   - Workers {0, 1} strictly handle target tiles in Q0 ($y \le 4$).
   - Workers {2, 3} strictly handle target tiles in Q1 ($y \ge 5$).
2. **Cross-Boundary Water Assist (Priority Override):**
   - If a worker has 0 pending tasks in their assigned quadrant AND a tile in the opposite quadrant has `needs_water == True`, the worker may cross the boundary to assist.
3. **Shed Access Exemption:**
   - All workers may travel to Shed $(4,3)$ for `PICKUP` / `SELL` orders when required.

---

## 4. Staggered Capital Allocation (Q1 Seed Purchasing)

Buying seeds for 20 Q1 tiles at once on Day 12 would require:
$$14 \text{ Melons} \times \$80 + 6 \text{ Carrots} \times \$20 = \$1,120 + \$120 = \mathbf{\$1,240}$$

To avoid dropping liquid cash below `minimum_cash_float = $300.0`:
- **Staggered Purchasing Policy:**
  - Day 12 (Post-Expansion): Plant 6 Carrots + 4 Melons (Seed cost: $120 + $320 = $440).
  - Day 13–15: As early Melon/Carrot revenues are realized, plant remaining 10 Melon tiles in batches of 3–4 tiles per day.
  - Capital Allocator condition: `Available Seed Cash = Money - 300.0`.

---

## 5. Architectural Component Modifications

### `src/agricola/strategy/hybrid_livestock_cluster_roi.py`

1. **`CompetitiveConfig` Updates:**
   ```python
   @dataclass
   class CompetitiveConfig:
       # ...
       productive_tiles: int = 40        # Scaled from 24 to 40
       melon_tiles: int = 22             # Scaled from 12 to 22
       carrot_tiles: int = 12            # Scaled from 6 to 12
       wheat_tiles: int = 6              # Frozen
       spatial_partitioning: bool = True # Enable spatial worker dispatcher
   ```

2. **`LandManager` Tile Map Update:**
   - Hardcode explicit 20 Q0 + 20 Q1 crop tile layout lists.

3. **`TaskDispatcher` Spatial Dispatch Logic:**
   - Add quadrant filtering based on worker index ($w \in \{0,1\} \rightarrow Q0, w \in \{2,3\} \rightarrow Q1$).

---

## 6. Implementation Sequence (B1–B6)

```text
B1: Configuration & Telemetry Extension
    │ • Update CompetitiveConfig with 40-tile targets (22 Melon, 12 Carrot, 6 Wheat).
    │ • Add E08 scale diagnostic flags.
    ▼
B2: 40-Tile Spatial Grid Layout Engine
    │ • Implement exact coordinate mapping for 20 Q0 crop tiles & 20 Q1 crop tiles.
    ▼
B3: Spatial Worker Partitioning in Task Dispatcher
    │ • Implement worker index quadrant scoping ({0,1} -> Q0, {2,3} -> Q1).
    │ • Implement cross-quadrant water assist override.
    ▼
B4: Staggered Capital Allocation for Q1 Seeds
    │ • Regulate Day 12–15 seed purchases to maintain $300.0 cash float.
    ▼
B5: Unit Test Suite Updates (`tests/test_hybrid_livestock_cluster.py`)
    │ • Test 40-tile layout allocation.
    │ • Test spatial partitioning dispatcher rules.
    │ • Test staggered seed capital safety.
    ▼
B6: 30-Episode Local Benchmark Verification
    │ • Execute 30-episode paired benchmark against E07 ($15,364.57) and E06 ($25,180.30).
```

---

## 7. Verification Plan

### Automated Tests (`pytest tests/`)
- Run `pytest tests/test_hybrid_livestock_cluster.py` (new and updated unit tests).
- Run full pytest suite (`pytest tests/`): all **41/41** existing tests must pass.

### Local Benchmark Protocol (30 Paired Episodes)
- **Opponents:** 10 × `pass`, 10 × `random`, 10 × `starter`.
- **Seeds:** Identical seeds (`seed = episode_idx * 100`) across E05, E06, E07, E08.
- **Metrics Measured:**
  - Mean Final Money ($)
  - SD (`ddof=1`)
  - Median Final Money ($)
  - Paired Win / Equal / Loss vs E07 and E06
  - Worked productive tiles count
  - Land utilization rate (%)
  - Worker productive turn %
  - Worker movement turn %
  - Weed conversion count

### Success Thresholds
- **Completion Rate:** 100% (0 disqualifications).
- **Productive Scale:** 40 tiles actually worked.
- **Economic Victory:** Mean Final Money E08 > E07 (**>$15,364.57**).
- **Target Gap Closure:** Recover part of gap toward E06 (**$25,180.30**).

---

## 8. PLAN Decision

> **`GO FOR BUILD`**

Proceeding to BUILD after approval will implement the B1–B5 changes in `src/agricola/strategy/hybrid_livestock_cluster_roi.py` and run the B6 benchmark verification.

---

<!-- END OF DOCUMENT -->
