# Implementation Plan — E03: Multi-Tile Scaling

## 1. Verified Initial State

- **Repository**: `C:\Users\pietr\Projects\kaggriculture-agent`
- **Branch**: `main` (up-to-date with `origin/main`)
- **Git Working Tree**: Clean (untracked prompt/screenshot files only, no modified tracked files).
- **Consolidated Commit**: `107e82b — Finalize E02 documentation`
- **Available Tags**: `v0.1-e01-baseline`, `v0.2-e02-roicrop`
- **E01 Baseline Performance**: Mean Final Money `$3567.63 ± $205.38`, Overall Win Rate `66.67%`, Win Rate vs `starter` `0%`.
- **E02 Baseline Performance**: Mean Final Money `$5857.17 ± $132.37`, Overall Win Rate `100.0%`, Win Rate vs `starter` `100.0%`.
- **External Kaggle Skill Rating**:
  - E01 `CarrotLoopAgent`: `255.2` (observed up to `328.4`)
  - E02 `ROICropAgent`: `290.8` (observed initial rating `600.0`, stabilized at `290.8`)

---

## 2. Experimental Principle & Strategic Isolation

E03 strictly adheres to the core methodology: **one main strategic variable per experiment**.

- **Main Strategic Variable**: `single-tile production → multi-tile production` (expanding cultivation footprint from 1 tile `(4,4)` to 4 adjacent tiles `{(4,4), (4,3), (3,4), (3,3)}`).
- **Enabling Operational Mechanisms** (required infrastructure, NOT independent economic strategies):
  - Action movement format correction (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
  - Manhattan distance routing.
  - Spatial task target selection within priority sets.
  - Multi-tile state tracking across 4 tiles.
  - Seed purchasing matched strictly to the number of empty managed tiles.

---

## 3. Empirical Environment Evidence & Analysis

From systematic empirical probing of the `kaggriculture` environment via test scripts, we established:

1. **Grid Structure & Size**:
   - Full Board: `10 x 10` grid (100 total tiles).
   - Partitioned into 4 quadrants of `5 x 5` tiles: NW `(0..4, 0..4)`, NE `(5..9, 0..4)`, SW `(0..4, 5..9)`, SE `(5..9, 5..9)`.
   - **Initial Unlocked Area**: Top-Left quadrant (NW), i.e., 25 unlocked tiles at coordinates `(x, y)` where `x ∈ [0, 4]` and `y ∈ [0, 4]`.
   - Remaining 75 tiles are marked `"LOCKED"`. Unlocking additional quadrants requires the `BUY_LAND` market order at a cost of **$1000** per quadrant.

2. **Farmer Initial Position**:
   - `[4, 4]` (bottom-right tile of the NW unlocked quadrant).

3. **Movement Commands & Mechanics**:
   - Movement is commanded in the `farmer` action as `["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]` directly.
   - **Enabling Fix**: `ActionBuilder.move("N")` currently outputs `["MOVE", "N"]`, which the environment ignores (treated as PASS). In E03, `ActionBuilder` must output `[direction]` directly (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
   - Temporal Cost: Movement takes **1 turn (1 hour)** per tile step.
   - Economic Cost: **$0** (free).
   - Distance Metric: Manhattan distance $|x_2 - x_1| + |y_2 - y_1|$ turns.

4. **Market Action Rules**:
   - Market orders can be issued in the same turn as the farmer's action and do not require forfeiting the farmer's action on that turn.

5. **Tile State Observability**:
   - `observation["farms"][player_id]["tiles"]` provides full 2D grid visibility every turn:
     - `"LOCKED"`: Locked quadrant tile.
     - `None`: Unlocked empty tile.
     - `dict`: Planted tile containing `kind: "PLANT"`, `crop: str`, `planted_day: int`, `watered_today: bool`, `stage: int`, etc.
   - All 25 unlocked tiles can be inspected simultaneously in 0 ms.

---

## 4. Analysis of E02 Single-Tile Assumptions

`ROICropAgent` in E02 relies on four hardcoded single-tile assumptions:

1. **Fixed Tile Location**: Interacts only with `state.current_tile()` assuming the farmer never leaves `(4, 4)`.
2. **Single-Seed Inventory Buffer**: Purchases at most 1 seed (`target_seeds_owned == 0`), which stalls multi-tile planting.
3. **No Navigation System**: Has no pathfinding, target selection, or direction routing logic.
4. **No Multi-Tile Prioritization**: Lacks a task queue to arbitrate between harvesting, planting, and watering across multiple tile locations.

---

## 5. Evaluation of Multi-Tile Alternatives

We evaluated 4 options for E03 multi-tile scaling:

| Strategy Option | Tiles Count | Movement Overhead | Capital Cost | Complexity | Experimental Confounding Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A: 2 Tiles** | 2 tiles `{(4,4), (4,3)}` | 1 step between tiles | $160 (2 Melon seeds) | Minimal | Low, but underutilizes turn capacity |
| **Option B: Compact 2x2 Cluster (Selected)** | 4 tiles `{(4,4), (4,3), (3,4), (3,3)}` | Max 2 steps between any 2 tiles | $320 (4 Melon seeds) | Low-Medium | **Very Low**: Clean attribution to production scaling |
| **Option C: Liquidity-Based Progressive Scaling** | Dynamic (1 to 25) | Variable (1 to 8 steps) | Variable ($80 to $2000) | High | **High**: Introduces new economic policy & threshold logic |
| **Option D: Full Unlocked Quadrant** | 25 tiles | High (up to 8 steps traversal) | $2000 (25 Melon seeds) | Very High | **High**: Risk of water starvation & turn starvation |

### Rationale for Selected Solution (Option B)

A **compact 2x2 cluster of 4 tiles** centered at the farmer's starting position `(4,4)` — specifically `{(4,4), (4,3), (3,4), (3,3)}`:
- All 4 tiles are unlocked from turn 0 (no `BUY_LAND` required, eliminating economic confounding).
- Farmer starts at `(4,4)`, directly inside the cluster.
- Distance between any two tiles in the cluster is at most 2 steps.
- Turn budget efficiency: In a 12-day Melon growth cycle (288 turns), watering 4 tiles takes 4 turns/day * 12 days = 48 watering turns + ~12 movement turns = 60 turns total (only **20.8%** of available turns).
- Capital efficiency: $320 for 4 Melon seeds out of $3000 starting capital.
- Direct experimental control: Isolates **Multi-Tile Production Scaling** as the single independent variable.

---

## 6. Definitive Experimental Hypothesis

> Holding E02's economic strategy constant, expanding cultivation from one tile to a compact four-tile 2×2 cluster using spatial task prioritization will increase productive throughput and produce a measurable improvement in Mean Final Money without introducing operational instability or unacceptable decision latency.

---

## 7. Experimental Variables & Preservation of E02 Constraints

- **Independent Variable**: Cultivation footprint (1 tile `(4,4)` in E02 → 4 adjacent tiles `{(4,4), (4,3), (3,4), (3,3)}` in E03) with supporting multi-tile spatial task prioritization.
- **Strictly Preserved E02 Constraints**:
  - ROI calculation formula: `NetProfitPerDay = (SellPrice * 2.0 - SeedPrice) / Days`.
  - Crop selection function (`select_best_crop`).
  - Selling policy: Immediate sale of all shed inventory.
  - Market timing: None (sell immediately).
  - End-of-season cutoff: None.
  - Land purchase (`BUY_LAND`): Disabled / unused.
  - Benchmark configuration: 30 episodes total (10 vs `pass`, 10 vs `random`, 10 vs `starter`), 720 steps/episode.

---

## 8. Definitive Target Selection & Operational Strategy

On every turn, `MultiTileROIAgent` executes the following sequence:

### 1. Market Orders (Issued alongside farmer action)
- Sell any crops present in shed.
- Count empty tiles $E$ in the managed cluster `{(4,4), (4,3), (3,4), (3,3)}`. If owned seeds $S < E$, buy $\min(E - S, \lfloor \text{money} / \text{seed\_cost} \rfloor)$ seeds of the highest ROI crop.

### 2. Strict Spatial Priority Hierarchy for Target Selection
The target tile $T$ is selected using a strict, unambiguous priority hierarchy:

1. **Construct `HARVEST_SET`**: managed tiles containing mature crops (`age >= max_yield_day`).
   - If `HARVEST_SET` is not empty, select target $T \in \text{HARVEST\_SET}$ minimizing Manhattan distance $|x_T - x_{\text{farmer}}| + |y_T - y_{\text{farmer}}|$. Tie-breaking: sorted by coordinate `(y, x)`.
2. **Else, construct `PLANT_SET`**: empty managed tiles (`tile is None`), evaluated **only if seeds are owned**.
   - If `PLANT_SET` is not empty, select target $T \in \text{PLANT\_SET}$ minimizing Manhattan distance. Tie-breaking: sorted by coordinate `(y, x)`.
3. **Else, construct `WATER_SET`**: planted managed tiles requiring water today (`not watered_today`).
   - If `WATER_SET` is not empty, select target $T \in \text{WATER\_SET}$ minimizing Manhattan distance. Tie-breaking: sorted by coordinate `(y, x)`.

### 3. Action Execution
- If $T$ matches current farmer position: execute the tile action (`HARVEST`, `PLANT`, or `WATER`).
- Else: execute 1 step move towards $T$ (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
- If all sets are empty: execute `PASS`.

---

## 9. Proposed Code Changes

### Components & Files

#### `src/agricola/core/actions.py` [MODIFY]
- Fix `ActionBuilder.move(direction)` to output `[direction]` directly (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`) instead of `["MOVE", direction]`.

#### `src/agricola/strategy/multi_tile_roi.py` [NEW]
- Implement `MultiTileROIAgent` with 4-tile cluster management, strict priority task queue, Manhattan movement routing, and E02 ROI crop selection.

#### `src/agricola/agent.py` [MODIFY]
- Update default exported agent instance to `MultiTileROIAgent`.

#### `tests/test_actions.py` [NEW]
- Add unit tests verifying `ActionBuilder` outputs exact movement formats expected by Kaggriculture (`["NORTH"]`, etc.).

#### `tests/test_multi_tile.py` [NEW]
- Add unit tests verifying target selection hierarchy, seed buying for 4 tiles, movement step calculation, and single-turn task execution.

#### `scripts/build_submission.py` [MODIFY]
- Update script to package `MultiTileROIAgent` into `submission/submission.py`.

#### `submission/submission.py` [REGENERATE]
- Rebuild standalone submission file and verify with tests.

---

## 10. Verification & Benchmark Plan (VERIFY)

### Automated Tests
- `pytest tests/test_actions.py`
- `pytest tests/test_multi_tile.py`
- `pytest tests/test_submission.py`

### Benchmark Metric Verification (Local Evaluation)
Run full benchmark via `scripts/run_eval.py`:
- **Command**: `python scripts/run_eval.py --opponents pass,random,starter --episodes 10 --steps 720 --output results/e03_multi_tile.json`
- **Episodes**: 30 total (10 vs `pass`, 10 vs `random`, 10 vs `starter`).

---

## 11. Definitive Success Criteria for E03

1. **Benchmark Completion & Validity**:
   - Completion Rate = `100.0%`
   - Disqualification Rate = `0.0%`
   - Overall Win Rate = `100.0%`
   - Win Rate vs `starter` = `100.0%`

2. **Primary Performance Criterion**:
   - **`Mean Final Money E03 > Mean Final Money E02 ($5857.17)`**
   - Mandatory Recorded Metrics:
     - Absolute difference: `Mean Final Money E03 - $5857.17`
     - Percentage difference: `((Mean Final Money E03 - $5857.17) / $5857.17) * 100`
     - Sample standard deviation (`ddof=1`)
     - Median Final Money
   - *Exploratory Benchmark Target*: `$10,000.00` (informational target for exploration, not a validation requirement).

3. **Operational Stability & Latency**:
   - Agent Mean Turn Latency: `< 0.1 ms/turn`.
   - Code test suite passes cleanly with 0 failures.
