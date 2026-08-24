# E03 BUILD Review — Multi-Tile Scaling

## Summary of Changes

The **BUILD** phase for **E03 — Multi-Tile Scaling** has been completed strictly following the approved implementation plan (`docs/plans/E03_Multi_Tile_Scaling.md`).

The single main strategic variable introduced is:

**`single-tile production → multi-tile production`**

The agent footprint expanded from a single tile `(4, 4)` to a compact 2x2 cluster of 4 adjacent tiles: `{(4,4), (4,3), (3,4), (3,3)}`.

---

## Files Created & Modified

### Created Files
- [`src/agricola/strategy/multi_tile_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/multi_tile_roi.py): Implementation of `MultiTileROIAgent` managing the 2x2 cluster using spatial target prioritization and E02 ROI crop selection.
- [`tests/test_actions.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_actions.py): Unit tests for `ActionBuilder` movement action formatting (`["NORTH"]`, etc.).
- [`tests/test_multi_tile.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_multi_tile.py): Unit tests for `MultiTileROIAgent` spatial target prioritization, Manhattan distance routing, tie-breaking, and seed purchasing.
- [`docs/versions/E03_build_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E03_build_antigravity.md): BUILD phase review documentation.

### Modified Files
- [`src/agricola/core/actions.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/core/actions.py): Infrastructure bug fix for movement action formatting.
- [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py): Updated default exported agent instance to `MultiTileROIAgent`.
- [`scripts/build_submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/build_submission.py): Updated bundling script to package `MultiTileROIAgent`.

---

## Infrastructure Movement Bug Fix

- **Problem Identified**: `ActionBuilder.move(direction)` previously constructed `["MOVE", direction]`, which was ignored by Kaggriculture's environment parser (acting as a PASS).
- **Fix Implemented**: Updated `ActionBuilder.move(direction)` to output direct movement action strings (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
- **Classification**: Necessary infrastructure bug fix enabling movement across multiple tiles, not an independent economic strategy.

---

## Implemented Behavior (`MultiTileROIAgent`)

1. **Managed Grid Footprint**:
   - Fixed 2x2 cluster: `{(4,4), (4,3), (3,4), (3,3)}`.
   - All 4 tiles are unlocked from step 0 (no land purchases).

2. **Market Phase**:
   - Sells all harvested crops in shed immediately.
   - Computes highest ROI crop using E02 formula: `NetProfitPerDay = (SellPrice * 2.0 - SeedPrice) / Days`.
   - Counts empty managed tiles $E$. If owned seeds $S < E$, purchases $\min(E - S, \lfloor \text{money} / \text{seed\_cost} \rfloor)$ seeds of the highest ROI crop. Market orders are issued alongside farmer actions on the same turn.

3. **Strict Spatial Priority Hierarchy**:
   - `HARVEST_SET`: Managed tiles with mature crops (`age >= max_yield_day`).
   - `PLANT_SET`: Empty managed tiles (`tile is None`), evaluated if seeds owned.
   - `WATER_SET`: Planted managed tiles requiring water today (`not watered_today`).
   - Spatial Selection: Minimizes Manhattan distance $|x_T - x_{\text{farmer}}| + |y_T - y_{\text{farmer}}|$ **within the highest active priority class**. Tie-breaking: sorted by coordinate `(y, x)`.

4. **Action Execution**:
   - If farmer position == $T$: executes tile action (`HARVEST`, `PLANT`, `WATER`).
   - Else: executes 1 step move towards $T$ (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
   - If no candidate tiles exist across all sets: executes `PASS`.

---

## Preserved E02 Constraints & Strategy

- Economic crop selection logic (`select_best_crop`).
- ROI formula with `Yield = 2.0`.
- Immediate selling of harvested products.
- No market timing or price holding.
- No end-of-season cutoff logic.
- No `BUY_LAND` purchases.

---

## Test Execution & Verification

Ran test suite via `pytest`:
```bash
.\.venv\Scripts\pytest
```

### Test Results
```text
collected 14 items

tests\test_actions.py ..                                                 [ 14%]
tests\test_baseline.py ....                                              [ 42%]
tests\test_multi_tile.py .....                                           [ 78%]
tests\test_roi_crop.py ..                                                [ 92%]
tests\test_submission.py .                                               [100%]

============================= 14 passed in 6.64s ==============================
```

- Total Tests: 14
- Passed: 14
- Failed: 0
- Status: **PASSED (100% clean test run)**

---

## Plan Deviations

None. All implementation components were executed exactly according to the approved plan `docs/plans/E03_Multi_Tile_Scaling.md`.
