# E11-X1.3-B3: Fixed 3×3 EPU Strip Scaling & Kaggle Submission

## Executive Summary

Experiment **E11-X1.3-B3** implemented the supervisor-mandated fixed $3 \times 3$ EPU strip layout:
- **EPU1**: `[(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]` (Q0)
- **EPU2**: `[(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)]` (Q0+Q1)
- **EPU3**: `[(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)]` (Q1)

This configuration features:
1. **Zero Geometry Search Overhead**: Eliminates combinatorial search in favor of a clean, regular $3 \times 3$ horizontal strip.
2. **Post-Surplus Realized Revenue Land Gate**: Requires `cumulative_realized_revenue > 0.0` (EPU1 must harvest and sell crops at market) before `BUY_LAND` can trigger. This prevents pre-surplus bankroll depletion on Day 1.
3. **1-Land Purchase (50 tiles total)**: Unlocks Q1, making all 27 productive tiles available across the 3 contiguous $3 \times 3$ blocks.

---

## Benchmark Results Comparison

| Metric | X1.3-A (1× EPU) | X1.3-B (2× EPU) | Old B2 (Day 0) | B2R (Spatially Equiv) | E11-X1.3-B3 (Fixed 3×3 Strip) |
|---|---|---|---|---|---|
| **Mean Final Money** | $26,888.40 | **$28,727.40** | $9,808.40 | $26,435.40 | **$26,445.60** |
| **Median Money** | $26,888.40 | $28,727.40 | $9,808.40 | $26,581.00 | **$30,072.00** |
| **Peak Episode Money** | $26,888.40 | $28,727.40 | $11,500.00 | $27,649.00 | **$31,460.00** (Seed 200) |
| **Land Buy Day** | N/A | Day 14 | Day 0 | Day 1 | **Day 13 (Post-Surplus)** |
| **Realized Revenue Gate** | N/A | N/A | No | No | **YES (`realized_revenue > 0`)** |
| **Peak Active Workforce** | 2 | 3 | 4 | 4 | **4 Workers** |
| **Peak Active Tiles** | 9 | 18 | 27 | 16 | **27 Tiles** |
| **Provenance Status** | PASS | PASS | PASS | PASS | **PASS (100% Match)** |

---

## Standalone Submission Artifact Verification

- **Submission Bundle Path**: [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py)
- **Generator**: `scripts/build_submission.py`
- **Standalone Verification Test (`pytest tests/test_submission.py`)**: **PASS**
- **Standalone Smoke Run (`scratch/smoke_submission_b3.py`)**: **PASS ($23,416.00 on 720-step evaluation)**
- **Code Audit**: 100% self-contained, 0 unbundled external references.

---

## Kaggle Submission Metadata

- **Submission Name**: `E11-X1.3-B3 Fixed 3x3 3xEPU`
- **Target File**: `submission/submission.py`
- **Status**: **READY FOR KAGGLE UPLOAD**
