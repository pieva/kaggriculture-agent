# BUILD Report — E09-01 Livestock Subsystem Ablation

**Date:** 2026-08-26  
**Phase:** E09-01 BUILD  
**Status:** `BUILD COMPLETED`  
**Decision:** **`READY FOR E09-01 VERIFY`**  
**Strategy Class:** `LivestockAblationROIAgent` ([`src/agricola/strategy/livestock_ablation_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/livestock_ablation_roi.py))  
**Unit Tests:** [`tests/test_e09_livestock_ablation.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_e09_livestock_ablation.py) (**46/46 passed**)  
**Benchmark Runner Prepared:** [`scripts/benchmark_e09_performance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/benchmark_e09_performance.py)  

---

## 1. Summary of Build

The **BUILD** phase for **E09-01 — Livestock Subsystem Ablation** has been completed.

Following the approved single-variable ablation specification, `LivestockAblationROIAgent` was implemented as a dedicated strategy class in `src/agricola/strategy/livestock_ablation_roi.py`. It preserves the 40-tile productive crop footprint, 4-worker workforce, land expansion, Water-First priority, and spatial partitioning of E08, while completely ablating all active strategic livestock behaviors.

---

## 2. Controlled Ablation Matrix

| Livestock Subsystem Component | E08 Baseline (Livestock ON) | E09-01 Treatment (Livestock OFF) | Technical Implementation |
| :--- | :---: | :---: | :--- |
| **Animal Purchases** | ON (`BUY_ANIMAL COW/SHEEP`) | **OFF (0 Animal Purchases)** | `target_cows = 0`, `target_sheep = 0`. Market animal buying disabled. |
| **Pasture Construction** | ON (`BUILD_PASTURE` on 5 tiles) | **OFF (0 Pastures Built)** | `BUILD_PASTURE` action generation completely disabled. `pasture_tiles = []`. |
| **Animal Placement** | ON (`PLACE COW/SHEEP`) | **OFF (0 Animals Placed)** | `PLACE` action generation completely disabled. |
| **Animal Feeding** | ON (`FEED`, Wheat pickup) | **OFF (0 Feed Actions)** | `FEED` action generation disabled. `wheat_fed = 0`. |
| **Feed Safety Buffer** | ON (5 Wheat reserved) | **OFF (0 Wheat Reserved)** | `feed_safety_buffer = 0`. All Wheat available for market sale. |
| **Livestock Harvest** | ON (Milk/Wool harvesting) | **OFF (0 Livestock Harvests)** | Milk/Wool harvesting from pastures disabled. |
| **Livestock Sales** | ON (`SELL MILK`, `SELL WOOL`) | **OFF (0 Livestock Sales)** | Milk and Wool market orders disabled (0 units produced/sold). |

---

## 3. Frozen Variables Matrix

| Architectural Dimension | E08 Baseline | E09-01 Treatment | Status |
| :--- | :---: | :---: | :---: |
| **Target Productive Footprint** | 40 tiles (20 Q0 + 20 Q1) | 40 tiles (20 Q0 + 20 Q1) | **`FROZEN`** |
| **Workforce Size & Hiring** | 4 workers (Day 1, 6, 12) | 4 workers (Day 1, 6, 12) | **`FROZEN`** |
| **Land Expansion** | Day 12 `BUY_LAND` Q1 ($1,000) | Day 12 `BUY_LAND` Q1 ($1,000) | **`FROZEN`** |
| **Spatial Worker Partitioning** | Worker 0-1 (Q0), Worker 2-3 (Q1) | Worker 0-1 (Q0), Worker 2-3 (Q1) | **`FROZEN`** |
| **Task Priority Scheme** | `WATER > HARVEST > PLANT` | `WATER > HARVEST > PLANT` | **`FROZEN`** |
| **Cross-Boundary Water Assist** | Enabled | Enabled | **`FROZEN`** |
| **Crop Allocation Ratios** | Melon (22), Carrot (12), Wheat (6) | Melon (22), Carrot (12), Wheat (6) | **`FROZEN`** |
| **Seed Buying Cash Reserve** | $300.0 Liquid Cash Reserve | $300.0 Liquid Cash Reserve | **`FROZEN`** |
| **Liquidation Policy** | Day 27+ Inventory Flush | Day 27+ Inventory Flush | **`FROZEN`** |

---

## 4. Test Suite & Verification Results

1. **E09-01 Structural Unit Tests ([`tests/test_e09_livestock_ablation.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_e09_livestock_ablation.py)):**
   - `test_e09_configuration_ablation`: Verified `target_cows=0`, `target_sheep=0`, `feed_safety_buffer=0`, 40 crop tiles. (PASS).
   - `test_e09_no_livestock_actions_emitted`: Verified 0 `BUY_ANIMAL`, 0 `BUILD_PASTURE`, 0 `PLACE`, 0 `FEED`, 0 Milk/Wool sales emitted over simulation steps. (PASS).
   - `test_e09_hiring_and_expansion_preserved`: Verified `HIRE` and `BUY_LAND` Q1 issued on Day 12 Hour 0. (PASS).
   - `test_e09_water_first_priority_preserved`: Verified `WATER` executed on unwatered plant tile. (PASS).
2. **Full Regression Suite (`pytest tests/`):**
   - **46/46 unit tests passed (100%)** in 6.80s.
3. **Technical Smoke Test (`scratch/run_e09_smoke.py`):**
   - Executed single 720-step episode (seed=100 vs `starter`). Final Money = **$7,943.00**. Confirmed 0 cows, 0 sheep, 0 pastures built, 0 feed actions, 0 wheat fed, 0 Milk/Wool revenue. All smoke assertions passed.
4. **Kaggle Entrypoint Integrity:** [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py) remains 100% untouched pointing to E06 shipped baseline `WaterFirstHIRENWClusterROIAgent`.

---

## 5. Preparation for VERIFY

The paired 30-episode benchmark runner script has been created at [`scripts/benchmark_e09_performance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/benchmark_e09_performance.py).

When VERIFY is authorized, it will evaluate:
- **Primary Causal Delta:** E09-01 (40t, Livestock OFF) vs E08 (40t, Livestock ON) on identical 30 paired episodes (`seed = episode_idx * 100`).
- **Secondary Reference Delta:** E09-01 (40t, Livestock OFF) vs E07 (24t, Livestock ON).

---

<!-- END OF DOCUMENT -->
