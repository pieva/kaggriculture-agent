# BUILD Report — E05 HIRE Multi-Worker Scaling (`HIRENWClusterROIAgent`)

**Date:** 2026-08-25  
**Strategy:** `HIRENWClusterROIAgent`  
**Phase:** BUILD (E05-03B Result Isolation Correction)  
**Status:** Completed (`READY FOR VERIFY`)  

---

## 1. Objective of BUILD

Implement `HIRENWClusterROIAgent` according to the approved implementation plan (`docs/plans/E05_HIRE_MultiWorker_Scaling.md`) to evaluate whether introducing 1 daily farm hand via `HIRE` ($1/day) with fixed spatial partitioning (4:5) on the 9-tile NW footprint eliminates the worker capacity/scheduling bottleneck of E04.

---

## 2. Experimental Scoping & Isolation

- **Control (E04):** `NWClusterROIAgent` (1 farmer, 9 tiles, no `HIRE`, `HARVEST > PLANT > WATER`).
- **Treatment (E05):** `HIRENWClusterROIAgent` (1 farmer + 1 daily farm hand, 9 tiles, fixed 4:5 spatial partitioning, `HARVEST > PLANT > WATER`).
- **Single Experimental Variable:** Additional worker capacity introduced through 1 daily `HIRE` ($1/day).
- **Strict Isolation Constraints Preserved:**
  - NO `BUY_LAND`
  - NO `DIG` (no weed recovery)
  - NO Water-First scheduling
  - NO changes to E03 ROI crop selection formula (`yield=2.0`)
  - NO horizon filtering
  - NO dynamic rebalancing of worker partitions

---

## 3. Core Implementation Details

### 3.1 GameState Extensions (`src/agricola/core/state.py`)
- Added `state.hands_positions`: returns list of `(x, y)` tuples for active farm hands.
- Added `state.hires_today`: returns `int(self.my_farm.get("hires_today", 0))`.

### 3.2 ActionBuilder Extensions (`src/agricola/core/actions.py`)
- Added `actions.hire()`: appends `["HIRE"]` to `self.market_orders`.
- Added `actions.add_hand_action(action_list)`: appends `action_list` to `self.hands_actions`.

### 3.3 Strategy Implementation (`src/agricola/strategy/hire_nw_cluster_roi.py`)
- Created `HIRENWClusterROIAgent` managing the 9-tile cluster with 1 Farmer and 1 Hand:
  - **Farmer Partition (4 tiles):** `{(4,4), (4,3), (3,4), (3,3)}`
  - **Hand 1 Partition (5 tiles):** `{(4,2), (3,2), (2,4), (2,3), (2,2)}`
- **Daily HIRE Lifecycle:**
  - Emits `["HIRE"]` on `hour == 0` if `len(hands) == 0` and `hires_today == 0` and `money >= 1.0`.
  - Hand 1 becomes active in state at `hour == 1` and receives actions via `add_hand_action(...)`.
  - Hand 1 automatically resets at end of day (`hour == 23`).
- **Shared Seed Protection:**
  - Tracks `virtual_seeds` during `act()` to prevent Farmer and Hand 1 from issuing atomic invalid `PLANT` orders if stock is limited.

---

## 4. Result Artifact Isolation Correction (E05-03B)

- **Anomaly Detected:** During initial smoke testing, executing `scripts/run_eval.py` without an explicit `--output` flag defaulted to `results/e01_baseline.json`, inadvertently overwriting the E01 baseline artifact.
- **Root Cause:** Hardcoded default parameter `default="results/e01_baseline.json"` in `scripts/run_eval.py` CLI parser.
- **Corrective Action Applied:**
  1. Restored `results/e01_baseline.json` exactly to `HEAD` via `git checkout HEAD -- results/e01_baseline.json`.
  2. Updated `scripts/run_eval.py` default output parameter to `results/latest_eval.json`.
  3. Executed 1-episode smoke evaluation with explicit dedicated output path: `results/e05_hire_multiworker.json`.
- **Verification:** Verified that `results/e01_baseline.json` and all historical result files (E01–E04) remain 100% clean and unmodified.

---

## 5. Test Results & Verification

### 5.1 Unit Test Suite (`pytest tests/`)
Created `tests/test_hire_nw_cluster.py` covering:
- Hand position parsing in `GameState`
- Action serialization for `HIRE` and `hands`
- Daily HIRE emission on `hour == 0`
- Prevention of duplicate daily `HIRE`
- Fixed spatial partitioning for Farmer and Hand 1
- Shared seed reservation logic

**Pytest Output:** `25 passed in 1.88s` (100% passing across all 7 test files).

### 5.2 Standalone Submission Bundling
Generated standalone submission bundle:
```bash
.venv/Scripts/python.exe scripts/build_submission.py
```
**Result:** Standalone submission generated at `submission/submission.py` and validated via `tests/test_submission.py` (PASSED).

### 5.3 1-Episode Technical Smoke Evaluation
Ran 1-episode smoke evaluation against `starter` to verify runtime stability and dedicated artifact writing:
```bash
.venv/Scripts/python.exe scripts/run_eval.py --opponents starter --episodes 1 --output results/e05_hire_multiworker.json
```
**Smoke Evaluation Output:**
- **Dedicated Artifact:** `results/e05_hire_multiworker.json`
- **Completion Rate:** `100.00%` (720/720 steps completed)
- **Disqualification Rate:** `0.00%`
- **Overall Win Rate:** `100.00%` (1W / 0L)
- **Mean Final Money:** `$21442.00`
- **HIRE Executions:** 30 ingaggi eseguiti (1 al giorno a `hour == 0` per 30 giorni) al costo di $30 totali.
- **Agent Mean Turn Latency:** `0.0619 ms/turn`
- **Sim Mean Step Time:** `3.79 ms/step`

---

## 6. Files Created and Modified

### Created Files:
- `src/agricola/strategy/hire_nw_cluster_roi.py`
- `tests/test_hire_nw_cluster.py`
- `results/e05_hire_multiworker.json`
- `docs/versions/E05_build_antigravity.md`

### Modified Files:
- `src/agricola/core/state.py`
- `src/agricola/core/actions.py`
- `src/agricola/agent.py`
- `scripts/build_submission.py`
- `scripts/run_eval.py`

---

## 7. Deviations from PLAN

- **Operational Infrastructure Adjustment:** Corrected `scripts/run_eval.py` CLI default output parameter from `results/e01_baseline.json` to `results/latest_eval.json` to prevent accidental overwrites of historical baseline artifacts. No strategic or experimental variable changes were made.

---

## 8. Readiness Decision for VERIFY

> **`READY FOR VERIFY`**

The implementation of `HIRENWClusterROIAgent` is complete, fully covered by unit tests, verified via standalone submission build, confirmed technically stable via 1-episode smoke evaluation, and writes to a dedicated E05 result artifact (`results/e05_hire_multiworker.json`). The codebase is ready for the 30-episode comparative benchmark evaluation in the **VERIFY** phase.
