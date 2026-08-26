# E07-09 — Kaggle External Validation Report

**Phase:** `E07-09 — Kaggle External Validation`  
**Date:** 2026-08-26  
**Status:** `PREPARED & VERIFIED (PENDING MANUAL UPLOAD)`  

---

## 1. Objective

The objective of `E07-09` is to bundle, verify, and submit the standalone **E07 baseline configuration** (`HybridLivestockClusterROIAgent`) to the Kaggle Kaggriculture competition for external validation. This submission provides an empirical comparison between local controlled benchmarks and external Kaggle leaderboard behavior.

> **Note:** E06 (`WaterFirstHIRENWClusterROIAgent`, Mean Money $25,180.30) remains the active local shipped baseline. E07 is submitted purely for external validation.

---

## 2. Source & Commit State

- **Strategy Class:** `HybridLivestockClusterROIAgent` (`src/agricola/strategy/hybrid_livestock_cluster_roi.py`)
- **Config Class:** `CompetitiveConfig`
- **Standalone Bundle File:** [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py)
- **Bundle Generator:** [`scripts/build_submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/build_submission.py)

---

## 3. Submission Audit & Cleanliness Check

- **Import Audit:** Verified zero internal package imports (`agricola.core`, `agricola.strategy`), zero hardcoded local filesystem paths, zero `src/` dependencies.
- **Dependencies Included:** All core classes (`GameState`, `ActionBuilder`, `CompetitiveConfig`, `HybridLivestockClusterROIAgent`) are 100% bundled standalone into `submission/submission.py`.
- **Diagnostic Code Audit:** No scratch scripts or telemetry file logging calls are executed at submission runtime.

---

## 4. Pre-Submission Test Suite Result (`pytest`)

Executed full unit test suite:

```powershell
============================= 41 passed in 1.85s ==============================
```

- **Result:** **41 / 41 PASSED (100%)**.
- Zero regressions on E01–E06 test suites.

---

## 5. Standalone Local 720-Step Smoke Test

Executed full episode simulation using `kaggle_environments` with `submission/submission.py` standalone bundle vs `random` opponent:

```text
============================================================
STANDALONE SUBMISSION FULL 720-STEP SMOKE TEST RESULT:
Total Steps Executed: 720/720
Player 0 Status:      DONE
Player 0 Final Money: $18,044.00
============================================================
ALL STANDALONE VERIFICATION CHECKS PASSED!
```

---

## 6. Configuration Consistency Audit (E07-08 vs Submission)

| Parameter | E07-08 Frozen Value | Submission Value | Audit Status |
| :--- | ---: | ---: | :---: |
| `target_quadrants` | `2` | `2` | **MATCH** |
| `productive_tiles` | `24` | `24` | **MATCH** |
| `wheat_tiles` | `6` | `6` | **MATCH** |
| `melon_tiles` | `12` | `12` | **MATCH** |
| `carrot_tiles` | `6` | `6` | **MATCH** |
| `target_workers` | `4` | `4` | **MATCH** |
| `target_cows` | `4` | `4` | **MATCH** |
| `target_sheep` | `2` | `2` | **MATCH** |
| `expansion timing` | `Day 12` | `Day 12` | **MATCH** |
| `cash reserve` | `$300.00` | `$300.00` | **MATCH** |
| `cow cutoff` | `D20` | `D20` | **MATCH** |
| `sheep cutoff` | `D18` | `D18` | **MATCH** |
| `melon cutoff` | `D18` | `D18` | **MATCH** |
| `all crops cutoff` | `D26` | `D26` | **MATCH** |
| `liquidation` | `D27+` | `D27+` | **MATCH** |

---

## 7. Submission Details & Upload Instructions

Automated submission via browser or CLI was bypassed in accordance with Section 10 directives (avoiding repeated browser auth loops).

### Action Required by User:
1. Navigate to the **Kaggle Kaggriculture Competition** web submission page.
2. Select and upload file: [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py).
3. Set Submission Description:
   ```text
   E07 HybridLivestockClusterROIAgent - external validation
   ```
4. Click **Submit**.

---

## 8. Leaderboard Score Tracking & 2-Hour Monitoring Protocol

| Version | Strategy | Local Mean Money | Kaggle Score ($T_0$) | Kaggle Score ($T+2\text{h}$) | Status |
| :--- | :--- | ---: | ---: | ---: | :---: |
| **E05** | `HIRENWClusterROIAgent` | $21,485.87 | 439.7 | 439.7 | Stabilized |
| **E06** | `WaterFirstHIRENWClusterROIAgent` | **$25,180.30** | — | — | Active Shipped Baseline |
| **E07** | `HybridLivestockClusterROIAgent` | $15,364.57 | *Pending* | *Pending* | **External Validation** |

> **Monitoring Protocol:** The initial Kaggle Skill Rating ($T_0$) is provisional. The final evaluation will be recorded after the standard **2-hour assestamento window ($T+2\text{h}$)**.
