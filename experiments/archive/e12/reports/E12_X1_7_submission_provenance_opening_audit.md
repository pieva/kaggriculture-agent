# E12-X1.7 — Submission Provenance & Opening Behavior Audit

## Executive Summary

Audit **E12-X1.7 (Submission Provenance & Opening Behavior Audit)** was conducted following visual replay observation on Kaggle. The audit verified that the previously uploaded submission (`F12068386FC0773FA2059E98DDA85A96C8F9C3ADC6EBE60A8B76230F816F3779`) executed the **E11 Pure Crop Strategy** instead of **E12-X1.7 Hybrid Strategy** due to a hardcoded configuration in `scripts/build_submission.py`.

The builder script has been fixed, the standalone submission rebuilt, and **100% behavioral equivalence** across the opening 24 turns on Seed 0 verified between `src/agricola/...` and `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`.

---

## 1. Provenance Audit Findings

| Metric / Check | Initial Build (Uploaded to Kaggle) | Fixed Rebuilt Submission | Diagnostic Verdict |
| :--- | :---: | :---: | :--- |
| **SHA-256 Hash** | `F12068386FC0773FA2059E98DDA85A96C8F9C3ADC6EBE60A8B76230F816F3779` | **`22EB239B108AC045AC86548B6A9444EDEF1939072756C082C2EC8D95EF13881F`** | Hash Updated |
| **Configured Mode** | `EPU_CORNER_PRUNED_CENTER_OUT` (E11 Crop) | **`E12_HYBRID_STAGED_LOCALITY` (E12-X1.7 Hybrid)** | **Root Cause Fixed** |
| **Turn 1–24 Behavioral Match** | 0 / 24 Turns (Mismatch) | **24 / 24 Turns (100% Match)** | **PERFECT EQUIVALENCE** |
| **Pasture / Livestock Core** | None (Pure Crop) | **2x2 Central Core `[(3,3),(3,4),(4,3),(4,4)]` Active** | **Core Verified** |
| **Unit Test Suite** | 83/83 Pass | **84/84 Pass (Added `test_submission_behavioral_equivalence.py`)** | **100% Pass** |

---

## 2. Root Cause Classification

**`A. BUILD_SCRIPT_CONFIG_MISMATCH`**

Lines 30–37 of `scripts/build_submission.py` had a legacy fallback hardcoded to `productive_core_mode="EPU_CORNER_PRUNED_CENTER_OUT"`. Consequently, any call to `scripts/build_submission.py` bundled the E11 Pure Crop strategy into `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`.

- **Uploaded Kaggle Submission Verdict**: **`CURRENT KAGGLE SUBMISSION INVALID — REUPLOAD REQUIRED`**

---

## 3. Rebuild & Fix Summary

1. **`scripts/build_submission.py`**: Updated `SUBMISSION_TEMPLATE` to instantiate `ProductiveMassConfig` with exact E12-X1.7 parameters (`E12_HYBRID_STAGED_LOCALITY`, `epu_level=3`, `workforce_scaling_mode="LAND_CO_SCALING"`, `target_tiles_per_worker=5.0`, `max_workers=6`).
2. **Behavioral Trace Test**: Created [`scratch/trace_opening_equivalence.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scratch/trace_opening_equivalence.py) and confirmed **100% identical actions** across all 24 opening turns on Seed 0.
3. **Automated Unit Test**: Created [`tests/test_submission_behavioral_equivalence.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_submission_behavioral_equivalence.py) to assert opening action parity between source and standalone submission in the automated test suite.

---

## 4. Re-Upload Authorization & Standalone File Details

- **Verified File Path**: [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py)
- **New Verified SHA-256 Hash**: `22EB239B108AC045AC86548B6A9444EDEF1939072756C082C2EC8D95EF13881F`
- **Upload Label**: `E12-X1.7 Workforce Capacity Scaling`
