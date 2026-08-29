# External Validation Report — E09-01 Livestock Subsystem Ablation

**Date:** 2026-08-26  
**Phase:** E09-06 External Validation  
**Status:** **`E09-06 EXTERNAL VALIDATION — SUBMISSION READY`**  
**Kaggle Upload Status:** **`SUBMISSION READY — MANUAL UPLOAD REQUIRED`**  
**Submission Package Path:** [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py) (Size: 42,032 bytes)  
**Recommended Kaggle Description:** `E09-01 Livestock Ablation — 40t Livestock OFF`  
**Strategy Class:** `LivestockAblationROIAgent` ([`src/agricola/strategy/livestock_ablation_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/livestock_ablation_roi.py))  

---

## 1. Executive Summary

The **External Validation** phase for **E09-01 — Livestock Subsystem Ablation** has been prepared. 

Following the supervisor directive, the exact strategy variant `LivestockAblationROIAgent` (40 tiles, Livestock OFF, Water-First priority) evaluated during the local 30-episode VERIFY benchmark was frozen and bundled into a standalone Kaggle submission file at [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py). No strategy logic or parameter tuning was altered.

---

## 2. Frozen Candidate Identity

| Dimension | E09-01 Frozen Submission Specification |
| :--- | :--- |
| **Strategy Class** | `LivestockAblationROIAgent` |
| **Productive Crop Footprint** | **40 tiles** (20 Q0 + 20 Q1) |
| **Livestock Subsystem** | **OFF** (0 animal purchases, 0 pastures, 0 placement, 0 feed, 0 Milk/Wool sales) |
| **Workforce & Hiring** | **4 workers** (1 Farmer Principal + 3 Farm Hands hired at Day 1, 6, 12) |
| **Land Expansion** | **Day 12 `BUY_LAND` Q1** ($1,000) |
| **Task Priority Scheme** | **`WATER > HARVEST > PLANT`** (Water-First scheduling) |
| **Cross-Boundary Water Assist** | **Enabled** |
| **Crop Allocation Ratios** | **22 Melon, 12 Carrot, 6 Wheat** |
| **Seed Buying Cash Reserve** | **$300.0 Liquid Cash Floor** |
| **Local Performance Baseline** | **Mean Final Money: $22,899.20 \| Median Final Money: $27,672.00 \| Win Rate: 100.0%** |
| **Primary Causal Baseline** | **E08 paired ($11,468.53) — Mean Delta: +$11,430.67 (+99.67%), 86.7% paired win rate** |

---

## 3. Entrypoint & Packaging Verification

- **Entrypoint File:** [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py) updated to instantiate `LivestockAblationROIAgent` from `agricola.strategy.livestock_ablation_roi`.
- **Bundling Script:** [`scripts/build_submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/build_submission.py) executed cleanly to bundle `GameState`, `ActionBuilder`, `CompetitiveConfig`, `TelemetryLogger`, and `LivestockAblationROIAgent` into a self-contained single-file bundle.
- **Bundle File:** [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py) (42,032 bytes).
- **Test Suite Results:** **46/46 unit & integration tests passed (100%)** in 2.88s (`pytest tests/`), including `test_submission.py` standalone execution in `kaggle_environments` engine.

---

## 4. Manual Upload Instructions for Supervisor

1. **File to Upload:** [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py)
2. **Kaggle Competition:** Kaggriculture
3. **Submission Description:** `E09-01 Livestock Ablation — 40t Livestock OFF`
4. **Post-Upload Action:** Provide Kaggle submission confirmation / score / ranking to update external validation documentation.

---

<!-- END OF DOCUMENT -->
