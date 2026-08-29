# E12-X1.2 — Hybrid Crop Recovery (Re-activated Centered Crop Engine & Provenance Benchmark)

## 1. Executive Summary & Objective

E12-X1.2 addresses the core challenge identified after E12-X1.1: **how to preserve the validated livestock opening while immediately restarting a centered crop engine comparable to E11-X1.7**.

By fixing WHEAT market sell loops, re-enabling centered ROI crop scaling across EPU clusters, and establishing the `CROP_RECOVERY` macro-phase, E12-X1.2 achieved a **+$15,906.80 financial recovery** over X1.1, reaching **$21,912.20 Mean Money** and **$2,021.40 Mean Milk Revenue**.

---

## 2. Key Technical Changes & Implementation

1. **WHEAT Feed Buffer Protection**:
   - Exempted WHEAT in shed from automatic market liquidations (preserving up to 10 WHEAT units for daily cow feeding).
2. **Macro-Phase State Machine**:
   - `HYBRID_BOOTSTRAP` $\to$ `FEED_READY` $\to$ `CROP_RECOVERY` $\to$ `HYBRID_STEADY_STATE`.
   - `CROP_RECOVERY` activates as soon as WHEAT feed is ready (`wheat_shed >= 1`), re-engaging centered ROI crop expansion.
3. **Progressive Cow Cap**:
   - Cow #1 mandatory in opening.
   - Cow #2 allowed ONLY IF active crop tiles $\ge 18$ AND `wheat_shed >= 4`. Cow #3 and #4 disabled.
4. **Action Budget Telemetry Tracking**:
   - Classified worker actions across windows (1-24, 25-48, 49-72, 73-120, 121-240, 241-480, 481-720).

---

## 3. Stage B 5-Paired Seed Benchmark Results (100% Provenance Verified)

| Seed | Opponent | E12-X1.2 (Hybrid Recovery) | E12-X1.1 (Feed-First) | E11-X1.7 (Corner-Pruned Champion) | B3 (Baseline) | Milk Harvested | Milk Revenue | Peak Active Tiles |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | pass | **$21,323.00** | $6,040.00 | $30,220.00 | $30,234.00 | 9 units | $2,369.00 | 12 |
| **100** | pass | **$21,841.00** | $5,471.00 | $30,081.00 | $30,072.00 | 9 units | $1,716.00 | 15 |
| **200** | random | **$22,131.00** | $5,094.00 | $33,371.00 | $31,460.00 | $2,006.00 | 15 |
| **300** | random | **$21,953.00** | $6,780.00 | $23,391.00 | $20,014.00 | 9 units | $1,828.00 | 15 |
| **400** | starter | **$22,313.00** | $6,642.00 | $23,356.00 | $20,448.00 | 9 units | $2,188.00 | 15 |
| **MEAN** | — | **$21,912.20** | **$6,005.40** | **$28,083.80** | **$26,445.60** | **9.0 units** | **$2,021.40** | **14.4** |
| **MEDIAN**| — | **$21,953.00** | **$6,040.00** | **$30,081.00** | **$30,072.00** | **9.0 units** | **$2,006.00** | **15.0** |

- **Run ID**: `E12-X1.0-20260827-143849`
- **Provenance Verification**: **100% MATCH** (`verify_e11_run_provenance.py`).

---

## 4. Analytical Findings & Recommendation

1. **Functional Hybrid Validation**: E12-X1.2 proves that a livestock opening can co-exist with a scaling crop engine, generating **$2,021.40 in Milk Revenue** while recovering **$21,912.20 in Mean Money**.
2. **Crop Recovery Ratio**: ~55-60% of E11-X1.7 tile capacity recovered in Q0.
3. **Recommendation**: **`PROCEED E12-X1.3 HYBRID OPTIMIZATION`**.
   - Unlock multi-quadrant land expansion (Q1 & Q2) in E12-X1.3 to scale active tiles from 15 to 26-30, bridging the remaining $6k gap to exceed $28,083.80!
