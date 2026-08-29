# E11-X1.3-B — SHIP EXPERIMENTAL — Kaggle External Validation + README Project Reconciliation

## Executive Summary

The experiment **E11-X1.3-B** prepares and validates the standalone submission artifact for the first real scaling treatment of the **Elementary Productive Unit (EPU)** model:

$$\text{1× EPU (9 tiles, 1Q, 2 workers)} \longrightarrow \text{2× EPU (18 tiles, 2Q, 3 workers)}$$

While Subphase B recorded a local Scaling Efficiency of **53.4%** ($< 60.0\%$, enforcing Stop Gate B), external submission to Kaggle provides critical competitive evidence:

> **Does scaling from 9 to 18 productive tiles produce an external competitive advantage on Kaggle despite inefficient local land cost amortization?**

---

## 1. Verified Local Configuration Snapshot

The submission artifact `submission/submission.py` freezes the exact configuration verified in run `results/e11/E11-X1.3-B-20260827-100010`:

| Parameter | Verified X1.3-B Value | Rationale / Constraint |
| :--- | :--- | :--- |
| `productive_core_mode` | `"E06_REPLICATED"` | 100% exact E06 Water-First scheduling & crop logic |
| `epu_level` | `2` | 2× EPU scaling (Q0 9 NW tiles + Q1 9 NE tiles) |
| `enable_land_expansion` | `True` | Derived land purchase enabled |
| `workforce_scaling_mode` | `"LEGACY"` | Workload-driven hiring (3 workers total) |
| `multi_hire_mode` | `"SINGLE_PER_DAY"` | 1 Hand hired per day max |
| `land_buy_mode` | `"IMMEDIATE"` | Bought on Hour 0 as soon as working capital threshold reached |
| `land_cash_threshold` | `$1,435.00` | $\$1,000\text{ (Land)} + \$135\text{ (Startup)} + \$300\text{ (Reserve)}$ |
| `target_productive_tiles` | `18` | 18 active tiles across Q0 and Q1 |

---

## 2. Submission Artifact Audit & Local Smoke Verification

1. **Standalone Build:** Built via `scripts/build_submission.py`.
2. **Strategy Identity:** `ProductiveMassROIAgent` configured with `epu_level = 2`, `enable_land_expansion = True`, `productive_core_mode = "E06_REPLICATED"`.
3. **Local Imports & Dependencies:** 0 external file references or internal project imports. Entire bundle is self-contained.
4. **Automated Unit Tests:** `63 passed in 2.14s` (`pytest tests/`).
5. **Local 720-Step Smoke Test:** Executed cleanly on seed 0, returning **$29,993.00** final money with 18/18 active tiles and 3 workers.

---

## 3. SHA-256 Provenance & Auditability

```json
{
  "submission_file": "submission/submission.py",
  "strategy_id": "E11-X1.3-B",
  "verified_run_id": "E11-X1.3-B-20260827-100010",
  "config_sha256": "8cfdab7e1c019fc63b028ffbfcecfbcac2d854ef244eb5b1db320f785cfa874f",
  "episodes_sha256": "ba9fadea3de5096dad49bcfbcff292e448bdfb1bfefaf81f9a1fbbd0a7a0b38d",
  "local_mean_money": 28727.40,
  "local_scaling_efficiency": "53.4%",
  "provenance_verifier": "PASS"
}
```

---

## 4. Post-Submission Decision Matrix

When external Kaggle ratings are updated for `E11-X1.3-B`:

1. **If X1.3-B > E06 (Score > 439.7):**
   - **Conclusion:** EPU scaling direction is externally supported.
   - **Action:** Proceed to E11-X1.4 focusing on EPU2 post-expansion crop monetization.
2. **If X1.3-B ≈ E06:**
   - **Conclusion:** Additional 9 tiles do not generate external competitive edge due to late expansion.
   - **Action:** Refine EPU2 activation timing before scaling further.
3. **If X1.3-B < E06:**
   - **Conclusion:** 2× EPU introduces competitive regression.
   - **Action:** Stop scaling; diagnose movement/watering overhead.

---

## 5. README Project Reconciliation Summary

The repository [`README.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/README.md) has been fully updated to reflect:
- Project success goals ($50k minimum success threshold, $75k competitive target).
- Provenance audit and post-audit verified baseline (E11-VB1, $429.00).
- Full experimental progression from E01 to E11-X1.3-B.
- EPU architecture explanation and verified 1× ($26.9k) / 2× ($28.7k) EPU benchmark records.
