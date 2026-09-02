# Kaggle Overnight Validation Report — E10-01 Q1 Expansion Capital Protection

**Date:** 2026-08-26  
**Phase:** E10-06 Kaggle Overnight Validation  
**Status:** **`E10-01 SUBMISSION READY — MANUAL UPLOAD REQUIRED`**  
**Submission Package Path:** [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py) (Size: 44,521 bytes)  
**Recommended Kaggle Description:** `E10-01 Q1 Capital Protection — 40t Livestock OFF`  
**Strategy Class:** `Q1CapitalProtectedROIAgent` ([`src/agricola/strategy/q1_capital_protected_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/q1_capital_protected_roi.py))  

---

## 1. Executive Summary

The **E10-01 Q1 Expansion Capital Protection** strategy variant has been fully defined, planned, built, frozen, and packaged for overnight validation on Kaggle.

Local safety verification on 30 paired episodes confirms that protecting the `$1,000.0` capital floor for `BUY_LAND` Q1 prior to Day 12 **completely eliminates all catastrophic financial collapses below $10,000** observed in E09-01 (0 episodes < $10k in E10 vs 6 in E09), increases mean final money from **$21,706.53 to $23,515.87 (+ $1,809.33)**, and drastically reduces standard deviation from **$9,168.20 down to $2,789.27 (-70%)**.

---

## 2. Frozen Candidate Identity

| Dimension | E10-01 Submission Specification |
| :--- | :--- |
| **Strategy Class** | `Q1CapitalProtectedROIAgent` |
| **Footprint** | **40 tiles** (20 Q0 + 20 Q1) |
| **Livestock Subsystem** | **OFF** (0 animal purchases, 0 pastures, 0 placement, 0 feed, 0 Milk/Wool sales) |
| **Workforce & Hiring** | **4 workers** (1 Farmer + 3 Hands hired at Day 1, 6, 12) |
| **Land Expansion Target** | **Day 12 `BUY_LAND` Q1** ($1,000.0) |
| **Experimental Variable** | **Q1 Expansion Capital Protection** (Enforces $1,000 reserve floor on Days 8–11 until Q1 is owned) |
| **Task Priority Scheme** | **`WATER > HARVEST > PLANT`** (Water-First scheduling) |
| **Cross-Boundary Water Assist** | **Enabled** |
| **Crop Allocation Ratios** | **22 Melon, 12 Carrot, 6 Wheat** |
| **Local Performance Baseline** | **Mean Final Money: $23,515.87 \| Median: $23,845.00 \| Min: $10,915.00 \| SD: $2,789.27** |
| **Primary Causal Baseline** | **E09-01 paired ($21,706.53) — Mean Delta: +$1,809.33 (+8.3%)** |

---

## 3. Local Safety Verification Results (30 Paired Episodes)

The 30-episode paired safety benchmark compared E10-01 against E09-01, E08, E07, E06, and E05 under identical seeds (0, 100, ..., 900) across 10 x `pass`, 10 x `random`, and 10 x `starter` opponents:

| Metric | E05 (9t) | E06 (9t WF) | E07 (24t) | E08 (40t Live ON) | E09-01 (40t Live OFF) | **E10-01 (40t Protection)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mean Final Money** | $21,530.07 | $25,172.80 | $11,233.00 | $11,359.00 | $21,706.53 | **`$23,515.87`** |
| **Median Final Money** | $21,442.00 | $25,847.00 | $9,612.50 | $9,559.50 | $27,672.00 | **`$23,845.00`** |
| **Sample SD** | ± $288.94 | ± $1,748.17 | ± $5,207.94 | ± $5,923.27 | ± $9,168.20 | **`± $2,789.27` (-70%)** |
| **Min Final Money** | $21,282.00 | $22,192.00 | $89.00 | $89.00 | $124.00 | **`$10,915.00` (+$10,791)** |
| **Max Final Money** | $22,568.00 | $28,040.00 | $22,276.00 | $22,276.00 | $28,885.00 | **`$27,644.00`** |
| **Episodes < $10k** | 0 | 0 | 17 | 17 | 6 | **`0` (100% eliminated)** |
| **Episodes < $20k** | 0 | 0 | 29 | 28 | 9 | **`2` (77% reduction)** |
| **Coeff. of Variation** | 0.013 | 0.069 | 0.464 | 0.521 | 0.422 | **`0.119` (-72%)** |
| **Win Rate vs Standard** | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | **`100.0%`** |

### Key Empirical Observations:
1. **Catastrophic Tail Elimination:** All 6 episodes that collapsed below $10,000 in E09-01 (dropping as low as $124.00) were completely eliminated in E10-01. The minimum money in E10-01 rose to **$10,915.00**.
2. **Mean Financial Output Increased:** Mean final money increased from **$21,706.53 to $23,515.87 (+ $1,809.33 / episode)**.
3. **Drastic Variance Reduction:** Standard deviation dropped from **$9,168.20 down to $2,789.27 (-69.6%)**, confirming high consistency.
4. **Safety Gates Passed:** All 5 safety gates for Kaggle submission satisfied.

---

## 4. Entrypoint & Packaging Verification

- **Entrypoint File:** [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py) updated to instantiate `Q1CapitalProtectedROIAgent`.
- **Bundling Script:** [`scripts/build_submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/build_submission.py) executed cleanly to bundle `Q1CapitalProtectedROIAgent` into a self-contained single-file bundle.
- **Bundle File:** [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py) (44,521 bytes).
- **Test Suite Results:** **50/50 unit & integration tests passed (100%)** in 2.03s (`pytest tests/`), including `test_submission.py` standalone execution in `kaggle_environments` engine.

---

## 5. Manual Upload Instructions for Supervisor

1. **File to Upload:** [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py)
2. **Kaggle Competition:** Kaggriculture
3. **Recommended Submission Description:** `E10-01 Q1 Capital Protection — 40t Livestock OFF`
4. **Post-Upload Directive:** Keep strategy frozen overnight to collect clean competitive evidence on Kaggle.

---

<!-- END OF FILE -->
