# PLAN Evidence — E07 Configurable Competitive Baseline (`E07-03`)

**Date:** 2026-08-26  
**Phase:** PLAN  
**Status:** `PLAN COMPLETED`  
**Decision:** `GO FOR BUILD WITH OPEN PARAMETERS`  
**Target Class:** `HybridLivestockClusterROIAgent`  

---

## 1. Objective

To design a modular, highly configurable 2nd-generation baseline agent architecture—`HybridLivestockClusterROIAgent`—capable of operating across all core competitive dimensions of Kaggriculture:

- Multi-quadrant land expansion (`BUY_LAND`);
- Multi-worker scaling & burst-hiring (`HIRE`);
- Integrated livestock engine (Cows/Sheep) & Wheat feed loop;
- Strategic multi-crop role allocation (Feed, Cash, Flex);
- Capital allocation & reinvestment engine;
- Premium-First market order brokerage;
- 4-Phase lifecycle management (Opening $\rightarrow$ Scale $\rightarrow$ Produce $\rightarrow$ Liquidate);
- End-game asset liquidation.

E07 represents an intentional **architectural baseline step-change**. Every quantitative parameter is explicitly exposed via a centralized configuration model (`CompetitiveConfig`) as **`OPEN / TUNABLE`**, establishing a clean foundation for controlled single-variable ablation and optimization experiments in E08+.

---

## 2. Inputs from DEFINE (`E07-01`) and VERIFY (`E07-02`)

- **E07-01 DEFINE:** Identified that E06 ($24,662 Mean Money) reached a ceiling within a single 9-tile quadrant. Public competitive analysis established that top agents operate a compounding multi-capability economy (Livestock + Wheat feed + Multi-hand labor + Land expansion + Market brokerage + Phase liquidation).
- **E07-02 VERIFY:** Verified official environment mechanics (`kaggriculture.py`). Ground-truth rules established: Quadrant expansion ($1k/$2k/$4k), Cow cost $400 (Milk $160), Sheep cost $500 (Wool $200), Wheat feed requirement (1 Wheat/day), 10 orders/turn cap, 100 shed cap, 720 turns. Demonstrated mathematical sustainability: 6 Wheat tiles provide a guaranteed +3 Wheat/day feed surplus for 6 animals, and 4 workers provide a +26.5 turn/day labor buffer across 50 owned tiles. Projected economic model: $35,000 – $45,000 terminal bank capital.

---

## 3. Architectural Principles

1. **Strict Separation of Architecture vs Parameters:** Architectural capabilities (Phase management, Capital allocation, Feed balancing, Market queue) are hard infrastructure. Quantitative values (tile counts, herd size, day thresholds, cash buffers) are encapsulated in `CompetitiveConfig` as tunable parameters.
2. **Zero-Regression of Historical Baseline (E06):** E06 (`WaterFirstHIRENWClusterROIAgent`) remains 100% intact, reproducible, and tested. E07 is built in new modular strategy files under `src/agricola/strategy/hybrid_livestock_cluster_roi.py`.
3. **Comprehensive Instrumentation:** Every sub-system emits diagnostic telemetry during simulation runs to enable deep-dive root-cause analysis during VERIFY/REVIEW.

---

## 4. Proposed Agent Architecture (`HybridLivestockClusterROIAgent`)

The E07 agent is structured as a decoupled object-oriented system:

```text
                                 [ GameState Observation ]
                                             │
                                             ▼
                                  [ CompetitiveConfig ]
                                             │
                                             ▼
                                     [ Phase Manager ]
                                             │
                       ┌─────────────────────┼─────────────────────┐
                       ▼                     ▼                     ▼
             [ Capital Allocator ]    [ Land Manager ]    [ Workforce Manager ]
                       │                     │                     │
                       ├─────────────────────┼─────────────────────┤
                       ▼                     ▼                     ▼
              [ Livestock Manager ]   [ Crop Manager ]     [ Task Dispatcher ]
                       │                     │                     │
                       └─────────────────────┼─────────────────────┘
                                             ▼
                                    [ Feed Manager ]
                                             │
                                             ▼
                                    [ Market Broker ]
                                             │
                                             ▼
                                   [ End-Game Manager ]
                                             │
                                             ▼
                                    [ ActionBuilder ]
```

---

## 5. Configuration Model (`CompetitiveConfig`)

All strategic parameters are encapsulated in a single dataclass:

```python
from dataclass import dataclass
from typing import Dict, List, Tuple

@dataclass
class CompetitiveConfig:
    # --- Land & Expansion ---
    target_quadrants: int = 2               # Number of 5x5 quadrants (Q0=25, Q1=50)
    expansion_day: int = 12                 # Target day for 1st BUY_LAND (Q1, max Day 12)
    
    # --- Crop Role Allocations (out of 24 active crop tiles) ---
    wheat_tiles: int = 6                    # Dedicated FEED crop tiles
    melon_tiles: int = 12                   # Dedicated CASH crop tiles
    carrot_tiles: int = 6                    # Dedicated FLEX liquidity crop tiles
    
    # --- Livestock Engine ---
    target_cows: int = 4                    # Target Cow count ($400 cost, Milk product)
    target_sheep: int = 2                   # Target Sheep count ($500 cost, Wool product)
    feed_safety_buffer: int = 3             # Minimum extra Wheat units in shed
    stop_sheep_buy_day: int = 18            # Day cutoff for Sheep acquisition (needs 7.5d payoff)
    stop_cow_buy_day: int = 20              # Day cutoff for Cow acquisition (needs 5d payoff)
    
    # --- Workforce Scaling ---
    target_workers: int = 4                 # Farmer Principal + 3 Farm Hands
    hire_days: List[int] = (1, 6, 12)       # Days to execute burst-hire at hour == 0
    minimum_cash_after_hire: float = 300.0  # Cash float remaining after HIRE
    
    # --- Capital & Cash Reserve ---
    cash_reserve: float = 300.0             # Minimum liquid cash float
    
    # --- Phase & End-Game Amortization Cutoffs ---
    stop_melon_day: int = 18                # Day cutoff for Melon planting (12d growth cycle)
    stop_all_planting_day: int = 26         # Day cutoff for all crop planting
    liquidation_start_day: int = 27         # Day to commence 100% shed inventory flush
```

---

## 6. Phase Manager

Manages strategic state transitions across 4 operational phases:

- **`OPENING` (Days 1–5 / Turns 0–120):** Setup initial infrastructure. Buy 2 Cows + 2 Sheep, plant 6 Wheat + 8 Melons, hire Hand 1 on Day 1 turn 0. Maintain cash reserve float.
- **`SCALE` (Days 6–15 / Turns 121–360):** Reinvest daily animal cashflow ($293/day). Scale herd to 4 Cows + 2 Sheep. Hire Hand 2 on Day 6 turn 0. Execute `BUY_LAND` (Q1) on Day 12 turn 0. Hire Hand 3 on Day 12 turn 0.
- **`PRODUCE` (Days 16–25 / Turns 361–600):** Maximize 50-tile output. Maintain Wheat feed cycle, harvest Melons on rotation, execute daily Milk/Wool market sales. Enforce Cow buy cutoff (Day 20) and Sheep buy cutoff (Day 18).
- **`LIQUIDATE` (Days 26–30 / Turns 601–720):** 
  - Day 18: Cease Melon planting (Melon requires 12 days to mature; planting after Day 18 cannot harvest before Day 30).
  - Day 26: Cease all crop planting.
  - Days 27–30: Liquidate 100% shed inventory (Milk, Wool, Melons, Carrots, Wheat) via continuous market `SELL` orders to convert 100% of stored products into liquid bank cash. (Note: Animals, land, and structures cannot be sold in Kaggriculture and must be fully amortized through product sales prior to Day 30).

---

## 7. Capital Allocator

Centralized reinvestment broker that governs cash expenditure according to strict priority order while enforcing `cash_reserve`:

$$\text{Available Reinvestment Cash} = \max(0.0, \text{Current Money} - \text{cash\_reserve})$$

### Reinvestment Priority Hierarchy
1. **Daily Seeds & Feed Buffer:** Buy required seeds for active crop tiles.
2. **Workforce HIRE:** Execute scheduled HIRE on `hire_days` at `hour == 0` if `Available Cash >= hire_cost + minimum_cash_after_hire`.
3. **Livestock Acquisition:** Purchase Cows/Sheep if `Available Cash >= animal_cost` AND feed loop is balanced (`feed_supply >= feed_demand`).
4. **Land Expansion (`BUY_LAND`):** Purchase Quadrant 1 on `expansion_day` if `Available Cash >= $1000`.

---

## 8. Land Manager

Distinguishes and tracks 6 functional tile categories across owned territory:

```python
owned_tiles: Set[Tuple[int, int]]          # All unlocked tiles (Q0 = 25, Q1 = 50)
productive_tiles: Set[Tuple[int, int]]     # Active non-empty, non-locked tiles
crop_tiles: Set[Tuple[int, int]]           # Tiles assigned to Wheat, Melon, Carrot
livestock_tiles: Set[Tuple[int, int]]      # Tiles assigned to Pasture/Coop (Cows/Sheep)
infrastructure_tiles: Set[Tuple[int, int]] # Water access / central transit hub tiles
reserved_tiles: Set[Tuple[int, int]]       # Flex unallocated tiles in Q1 (18 tiles)
```

- **Expansion Trigger:** When `Phase == SCALE` and `Day == expansion_day` and `Money - 1000 >= cash_reserve`, append `["BUY_LAND"]` to market order queue. Quadrant 1 (NE 5x5) is unlocked.

---

## 9. Workforce Manager

Coordinates 1 Farmer Principal and up to 3 Daily Farm Hands:

- **Burst-Hiring Rule:** `HIRE` orders are issued strictly on `hour == 0` of designated `hire_days` `(1, 6, 12)`.
- **Worker Allocation:**
  - *Farmer Principal:* Manages Quadrant 0 core crops and market interactions.
  - *Farm Hand 1:* Dedicated Livestock & Feed Worker (pastures, animal feeding, Wheat plot watering).
  - *Farm Hand 2:* Dedicated Cash Crop Worker (Melon plot watering & harvesting in Q0).
  - *Farm Hand 3:* Dedicated Q1 Expansion Worker (Q1 crop watering & harvesting).

---

## 10. Crop Manager

Manages multi-crop role assignment across 24 active crop tiles:

- **`FEED` Role (6 Wheat Tiles):** Dedicated to producing Wheat for livestock consumption.
- **`CASH` Role (12 Melon Tiles):** Dedicated to 12-day high-payout Melon harvest rotations ($250 base price).
- **`FLEX` Role (6 Carrot Tiles):** Dedicated to 3-day fast-cycle Carrots ($35 base price) to maintain liquid cash flow between Melon harvests.

---

## 11. Livestock & Feed Manager

- **Livestock Engine:** Manages 4 Cows (`PASTURE`, $400 cost, $160 Milk every 2 days) and 2 Sheep (`PASTURE`, $500 cost, $200 Wool every 3 days).
- **Feed Balance Guard:**
  $$\text{Expected Feed Supply} = \text{Wheat Shed Inventory} + (\text{Wheat Crop Tiles} \times 6)$$
  $$\text{Expected Feed Demand} = \text{Animal Count} \times \text{Remaining Season Days}$$
  $$\text{Condition: } \text{Expected Feed Supply} \ge \text{Expected Feed Demand} + \text{feed\_safety\_buffer}$$
- If `Expected Feed Supply < Demand`, Capital Allocator halts animal purchases and Crop Manager temporarily converts Flex tiles to Wheat.

---

## 12. Task Dispatcher

Coordinates daily worker actions avoiding collisions, idleness, or starvation:

### Operational Priority Hierarchy
$$\text{WATER (Starvation Risk)} > \text{FEED\_ANIMALS} > \text{HARVEST (Mature Crops)} > \text{PLANT (Empty Tiles)}$$

Within the same priority level, workers select the target tile using **nearest Manhattan distance**. Task reservation prevents multiple workers from navigating to the same tile.

---

## 13. Market Broker

Centralizes all market transactions adhering to environment limits:

- **Order Limit:** Max **10 orders per turn** (strictly enforced).
- **Shed Limit:** Max **100 stored items** (monitored to prevent overflow loss).
- **Premium-First Priority Queue:**
  1. Priority 1: High-value animal products (`MILK`, `WOOL`).
  2. Priority 2: High-ROI mature crops (`MELON`).
  3. Priority 3: Flex crops (`CARROT`).
  4. Priority 4: Excess Wheat (only if shed count > feed safety buffer + 10).

---

## 14. End-Game Manager

Applies horizon-aware cutoffs and inventory liquidation as step 720 approaches:

- **Day 18 (`hour == 0`):** Cease Melon planting (Melon requires 12 days to grow; planting after Day 18 will not mature before step 720 and represents 100% wasted capital).
- **Day 18 / Day 20 (`hour == 0`):** Cease Sheep purchases on Day 18 and Cow purchases on Day 20 (livestock cannot be sold back to market; late purchases cannot amortize their $400/$500 cost before step 720).
- **Day 26 (`hour == 0`):** Cease all crop planting.
- **Days 27–30 (Turns 648–720):** Issue continuous `SELL` orders for 100% of stored Milk, Wool, Melons, Carrots, and Wheat in shed to guarantee $0 unsold inventory remaining at step 720. (Note: Unsold shed inventory, growing/mature field crops, livestock, land, and structures produce $0 terminal reward unless converted to liquid cash).

---

## 15. Instrumentation & Diagnostic System

`HybridLivestockClusterROIAgent` will emit a structured JSON diagnostic summary at episode completion containing:

- **Economy:** Starting Money, Final Money, Minimum Cash Float, Expenditure by Category (Seeds, HIRE, Land, Animals), Revenue by Product (Milk, Wool, Melon, Carrot, Wheat).
- **Land:** Owned Tiles, Productive Tiles, Land Utilization Ratio, Quadrant 1 Unlock Step.
- **Workforce:** Peak Worker Count, Total HIRE Orders, Worker Idle Turns, Movement Turns, Productive Action Turns.
- **Crops:** Total Planted, Total Watered, Total Harvested, Crop Mortality (Weeds), Unharvested Crops on Day 30.
- **Livestock & Feed:** Animals Acquired (Cows/Sheep), Wheat Feed Consumed, Animal Starvation Events, Milk Produced, Wool Produced.
- **Market:** Market Orders Placed, Quantities Sold per Product, Market Price Decay Deltas, Shed Overflow Discards.
- **End-Game:** Immature Crop Loss at Step 720, Liquidated Inventory Value, Final Asset Conversion Ratio.

---

## 16. Test Strategy

### A. Unit Tests (`tests/test_hybrid_livestock_cluster.py`)
1. `test_config_defaults_and_parsing`: Verify `CompetitiveConfig` initialization and parameter overrides.
2. `test_phase_manager_transitions`: Verify correct phase state shifts based on day, cash, and time.
3. `test_capital_allocator_cash_reserve`: Verify that reinvestment halts when money drops below `cash_reserve`.
4. `test_land_manager_quadrant_unlock`: Verify `BUY_LAND` order generation and 50-tile tracking.
5. `test_workforce_burst_hire_turn_zero`: Verify that `HIRE` orders are issued strictly on `hour == 0`.
6. `test_crop_role_allocation`: Verify 6 Wheat / 12 Melon / 6 Carrot tile assignment.
7. `test_feed_balance_guard`: Verify that animal purchase halts when Wheat supply is below demand buffer.
8. `test_market_broker_order_cap`: Verify that market orders never exceed 10 per turn.
9. `test_end_game_melon_cutoff`: Verify that Melon planting is blocked after Day 25.

### B. Behavioral Synthetic Tests
1. `test_cash_starvation_resilience`: Verify agent behavior when money is depleted.
2. `test_feed_deficit_recovery`: Verify that Flex tiles convert to Wheat when feed is low.
3. `test_end_game_liquidation_selloff`: Verify complete shed inventory sell-off on Days 29–30.

### C. Regression Suite
- Run full pytest suite (`pytest tests/`): All historical E01–E06 tests (**30/30**) must pass 100%.

---

## 17. Local Benchmark Strategy

- **Opponents:** `pass`, `random`, `starter` (10 episodes each, total **30 episodes**).
- **Protocol:** Identical 30-episode protocol (seeds 0, 100, ..., 900, 720 steps).
- **Primary Metrics:** Mean Final Money ($), Sample Std Dev (`ddof=1`), Median Final Money ($), Min/Max Money ($), Completion Rate (%), Disqualification Rate (%), Win Rate (%), Weed Conversions, Turn Latency (ms).
- **Paired Seed Comparison:** 30 seed-matched episode deltas against E06 baseline (`results/e06_water_first.json`).

---

## 18. Success Criteria

### A. Architectural Success Criteria (Mandatory)
1. 100% Completion Rate across 30 benchmark episodes (0 disqualifications).
2. Successful execution of `BUY_LAND` unlocking Quadrant 1 (50 tiles owned).
3. Successful burst-hiring scaling to 4 workers (1 Farmer + 3 Hands).
4. Successful operation of Livestock Engine (Cows + Sheep + Wheat feed loop).
5. 0 animal starvation events.
6. Execution of 4-phase lifecycle and Day 29–30 end-game liquidation.
7. Full diagnostic telemetry emission.

### B. Performance Success Criteria (To Be Measured)
- Mean Final Money E07 > Mean Final Money E06 ($24,662.00).
- Positive paired money delta in > 80% of matched episodes vs E06.

---

## 19. Failure Criteria

E07 BUILD/VERIFY will be flagged for diagnostic review if:
- Any episode fails to complete or suffers disqualification;
- `BUY_LAND` is purchased but Quadrant 1 tiles remain 0% utilized;
- Livestock suffers starvation due to feed loop breakdown;
- Worker idle time exceeds 30% of total worker-turns;
- Shed capacity overflow causes discarded inventory losses;
- End-game liquidation leaves > $2,000 in unliquidated shed inventory or unharvested crops on Day 30.

---

## 20. Open Parameters Table (`OPEN / TUNABLE`)

| Parameter | Initial Candidate Value | Status | Tuning Goal in E08+ |
| :--- | :---: | :---: | :--- |
| **Target Quadrants** | `2` (50 tiles) | **`OPEN`** | Test 2 vs 3 quadrants (`BUY_LAND` Q2) |
| **Active Crop Tiles** | `24` tiles | **`OPEN`** | Test 24 vs 36 active crop tiles |
| **Wheat Tiles (Feed)** | `6` tiles | **`OPEN`** | Optimize feed surplus margin |
| **Melon Tiles (Cash)** | `12` tiles | **`OPEN`** | Test Melon vs Watermelon/Pumpkin mix |
| **Carrot Tiles (Flex)** | `6` tiles | **`OPEN`** | Test Carrot vs Tomato liquidity flex |
| **Target Workers** | `4` (1 Farmer + 3 Hands) | **`OPEN`** | Test 3 vs 4 vs 5 total workers |
| **Hiring Schedule** | `(1, 6, 12)` at `hour == 0` | **`OPEN`** | Optimize burst-hire days |
| **Target Cows** | `4` cows | **`OPEN`** | Ablation in E08 (0 vs 4 vs 8 Cows) |
| **Target Sheep** | `2` sheep | **`OPEN`** | Ablation in E08 (0 vs 2 vs 4 Sheep) |
| **Expansion Day** | `Day 12` | **`OPEN`** | Ablation in E09 (Day 8 vs 12 vs 16) |
| **Cash Reserve Float** | `$300.0` | **`OPEN`** | Test $200 vs $300 vs $500 float |
| **Stop Melon Day** | `Day 25` | **`OPEN`** | Test Day 24 vs 25 vs 26 cutoff |
| **Liquidation Start Day** | `Day 29` | **`OPEN`** | Ablation in E11 (Day 28 vs 29 vs 30) |
| **Market Queue Priority** | `Milk/Wool > Melon > Carrot` | **`OPEN`** | Test price-decay dynamic sorting |

---

## 21. Implementation Sequence (B1–B10)

```text
B1: CompetitiveConfig & Diagnostic Instrumentation Infrastructure
        │
        ▼
B2: Phase Manager & Lifecycle State Engine
        │
        ▼
B3: Land Manager (50-Tile Tracking & BUY_LAND Expansion)
        │
        ▼
B4: Workforce Manager & Burst-HIRE Scheduler (4 Workers)
        │
        ▼
B5: Crop Manager & Multi-Role Allocator (Wheat/Melon/Carrot)
        │
        ▼
B6: Livestock Manager & Wheat Feed Balance Guard (Cows/Sheep)
        │
        ▼
B7: Multi-Worker Task Dispatcher (Priority & Spatial Assignment)
        │
        ▼
B8: Premium-First Market Broker & Order Queue (10 Orders/Turn)
        │
        ▼
B9: End-Game Manager & Asset Liquidation Engine (Days 26–30)
        │
        ▼
B10: Integration, Unit Test Suite (pytest), & 30-Episode Local Benchmark
```

---

## 22. Risks & Mitigations

| Risk | Potential Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Cash Starvation on Day 12** | Unable to pay worker salaries or seeds after `BUY_LAND` | `Capital Allocator` enforces `$300 cash_reserve` float before `BUY_LAND`. |
| **Livestock Starvation** | Unfed animals become unproductive | `Feed Balance Guard` halts animal acquisition if Wheat supply < demand buffer. |
| **Shed Capacity Overflow** | Crops discarded when shed reaches 100 items | `Market Broker` continuously flushes low-tier flex crops when shed > 70 items. |
| **Order Limit Dropping** | Extra orders beyond 10 silently dropped | `Market Broker` strictly caps generated orders at 10 per turn. |
| **Worker Collision** | Multiple workers attempt same tile action | `Task Dispatcher` maintains atomic tile-reservation registry. |

---

## 23. PLAN Decision

> **`GO FOR BUILD WITH OPEN PARAMETERS`**

### Rationale
The architecture for `HybridLivestockClusterROIAgent` is fully specified, modularly decoupled, mathematically grounded in official environment rules, and backed by a comprehensive B1–B10 implementation plan and unit test strategy.

Proceeding to **E07 BUILD** will construct the B1–B10 modules and execute the 30-episode local benchmark to establish the 2nd-generation baseline.
