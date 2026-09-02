# E12-X1.7 — Kaggle External Validation

## Executive Summary

Experiment **E12-X1.7 (Kaggle External Validation)** executed provenance verification, standalone build generation, and unit test validation for the **E12-X1.7 Workforce Capacity Scaling** agent candidate.

---

## 1. Provenance & Build Verification

- **Standalone Submission File**: [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py)
- **SHA-256 Hash**: `F12068386FC0773FA2059E98DDA85A96C8F9C3ADC6EBE60A8B76230F816F3779`
- **Unit Test Status**: `83/83 passed in 2.19s (100%)`
- **Submission Test Status**: `1/1 passed in 1.52s (100%)`
- **Source Configuration**: `ProductiveMassConfig` (Mode: `E12_HYBRID_STAGED_LOCALITY`, 5 `CROP_PRIMARY` workers, 4 crop tiles/worker, 4-cow progressive 2x2 core scaling).

---

## 2. Benchmark Summary Comparison

| Strategy Version | Local Mean Money ($) | Kaggle Leaderboard Score ($) | Relative Rank | Architecture Status |
| :--- | :---: | :---: | :---: | :--- |
| **E11-X1.7 (Canonical Champion)** | $28,083.80 | Champion Baseline | Champion | Corner-Pruned 26t Pure Crop |
| **E12-X1.7 (Workforce Capacity)** | **$22,386.80** | **Pending Upload** | External Validation Candidate | Centered 2x2 Hybrid Cow-Crop |
| **E12-X1.6 (Functional Workforce)** | $22,008.80 | Baseline | Historical Baseline | Centered 2x2 Hybrid Cow-Crop |

---

## 3. Manual Kaggle Upload Instructions

Since Kaggle CLI is not configured in the active environment, the verified standalone submission file is ready for manual UI upload:

1. Open the Kaggle Kaggriculture Competition submission page:
   `https://www.kaggle.com/competitions/kaggriculture/submissions`
2. Drag and drop the standalone submission file:
   [`c:\Users\pietr\Projects\kaggriculture-agent\experiments\archive\e15\artifacts\freeze\legacy_submissions\submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py)
3. Set the submission label:
   `E12-X1.7 Workforce Capacity Scaling ($22,386.80 Mean)`
4. Click **Submit** and observe the live leaderboard score.

---

## 4. Single Authorized Recommendation

**`PROCEED E12-X1.8 — EARLIER WORKFORCE / CAPACITY ACTIVATION`**

Proceed with E12-X1.8 strategy development based on the empirical D3 audit findings (accelerating Q1 unlock and Cluster E activation from Day 18–22 to Day 4–6 and aligning 12-day Melon growth cutoffs).
