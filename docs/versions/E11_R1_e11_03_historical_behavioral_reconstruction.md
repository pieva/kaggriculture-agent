# BUILD & VERIFY Report — E11-R1 E11-03 Historical Behavioral Reconstruction

**Date:** 2026-08-27  
**Phase:** E11-R1 HISTORICAL BEHAVIORAL RECONSTRUCTION  
**Status:** `E11-R0 PARTIALLY COMPLETED — configuration isolation restored, historical behavioral reproducibility NOT restored`  
**E11-03 Classification:** **`NOT REPRODUCED`**  
**E11-06 Status:** **`RESULT INVALID FOR CAUSAL INTERPRETATION`**  
**Strategy File:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Benchmark Script:** [`scripts/benchmark_e11_performance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/benchmark_e11_performance.py)  
**Audit Artifact:** [`results/e11_productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11_productive_mass.json)  

---

## 1. Executive Summary

Following the completion of **E11-R0 Baseline Reproducibility Audit**, which successfully restored configuration isolation across all E11 variants, **E11-R1** was launched to investigate why isolated E11-03 execution ($892.63–$7,167.80 Mean Money, 2Q / 50 tiles) failed to reproduce the historical architectural fingerprint documented in `docs/versions/E11_03_expansion_gate_unlock.md` (3Q unlock ~83.3%, 4Q unlock ~60.0%, 100 tiles reached, 54 peak active tiles, 6 peak workers).

Through step-by-step causal chain analysis, Git log auditing, single-seed step tracing, and telemetry artifact inspection, E11-R1 identified the fundamental root cause: **Expansion Capital Protection Deadlock & Synthetic Timing Discrepancy**. 

Under live simulation mechanics with `protect_expansion_capital = True`, liquid cash post-Q1 acquisition drops to ~$899. Optional high-yield seed buys (Melon $320, Strawberry $400, Tomato $200) are blocked below $1,300 optional reserve, while essential seed buys (Carrot $120, Wheat $60) keep liquid cash oscillating in the $500–$850 range. As a result, liquid cash **never reaches the $1,100 threshold required for BUY_LAND Q2**, permanently locking the agent on 2 Quadrants (50 tiles).

Per the mandatory guidelines, **E11-03 is formally classified as `NOT REPRODUCED`**, and **E11-06 remains `RESULT INVALID FOR CAUSAL INTERPRETATION`**. Execution is halted at the **STOP GATE** (Case B).

---

## 2. R0 Correction & Status Adjustment

| Audit Phase | Previous Status | Corrected Official Status | Rationale |
| :--- | :--- | :--- | :--- |
| **E11-R0** | `AUDIT COMPLETED` | **`E11-R0 PARTIALLY COMPLETED — configuration isolation restored, historical behavioral reproducibility NOT restored`** | Configuration isolation was restored, but E11-03 failed the historical architectural acceptance criterion (3Q 83.3%, 4Q 60.0%). |
| **E11-03** | `REPRODUCED & RESTORED` | **`NOT REPRODUCED`** | Live simulation remains at 2Q (50 tiles) and 0.0% land expansion. |
| **E11-06** | `RESULT INVALID` | **`RESULT INVALID FOR CAUSAL INTERPRETATION`** | Remains invalid pending valid historical baseline reproduction. |

---

## 3. Historical E11-03 Specification

The parameter tuple for E11-03 documented in `docs/versions/E11_03_expansion_gate_unlock.md`:

| Parameter | Historical Documented Value | Current Isolated Value | Source File |
| :--- | :---: | :---: | :--- |
| `protect_expansion_capital` | `True` | `True` | [`docs/versions/E11_03_expansion_gate_unlock.md:75`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L75) |
| `expansion_gate_mode` | `"MIN_OPERATIONAL"` | `"MIN_OPERATIONAL"` | [`docs/versions/E11_03_expansion_gate_unlock.md:71`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L71) |
| `capital_release_mode` | `"BINARY"` | `"BINARY"` | [`docs/versions/E11_03_expansion_gate_unlock.md:8`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L8) |
| `workforce_scaling_mode` | `"LEGACY"` | `"LEGACY"` | `ProductiveMassConfig` default |
| `operating_reserve` | `$300.0` | `$300.0` | [`docs/versions/E11_03_expansion_gate_unlock.md:82`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L82) |
| `expansion_operating_buffer` | `$100.0` | `$100.0` | [`docs/versions/E11_03_expansion_gate_unlock.md:82`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L82) |
| `q1_expansion_min_q0_active` | 6 tiles | 6 tiles | [`docs/versions/E11_03_expansion_gate_unlock.md:72`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L72) |
| `q2_expansion_min_active` | 8 tiles | 8 tiles | [`docs/versions/E11_03_expansion_gate_unlock.md:73`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L73) |
| `q3_expansion_min_active` | 12 tiles | 12 tiles | [`docs/versions/E11_03_expansion_gate_unlock.md:74`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_03_expansion_gate_unlock.md#L74) |
| `prefer_land_before_optional_hire` | `False` | `False` | `ProductiveMassConfig` default |
| `target_tiles_per_worker` | 7.0 | 7.0 | `ProductiveMassConfig` default |

---

## 4. Historical Fingerprint

| Metric | Documented E11-03 Target | Isolated Reconstructed E11-03 | Delta / Status |
| :--- | :---: | :---: | :--- |
| **3Q / 75 tiles Unlock Rate** | **`~83.3% (25/30)`** | **`0.0% (0/30)`** | **`-83.3% (NOT REPRODUCED)`** |
| **3Q Mean Unlock Day** | **`Day 5.4`** | N/A (Never Unlocked) | N/A |
| **4Q / 100 tiles Unlock Rate** | **`~60.0% (18/30)`** | **`0.0% (0/30)`** | **`-60.0% (NOT REPRODUCED)`** |
| **4Q Mean Unlock Day** | **`Day 11.2`** | N/A (Never Unlocked) | N/A |
| **Peak Owned Land** | **`100 tiles (4 Quadrants)`** | **`50 tiles (2 Quadrants)`** | **`-50 tiles`** |
| **Peak Active Productive Tiles** | **`~54 tiles`** | **`17 tiles`** | **`-37 tiles`** |
| **Peak Workforce** | **`~6 workers`** | **`2 workers`** | **`-4 workers`** |
| **Mean Final Money** | **`$7,193.77`** | **`$892.63 – $7,167.80`** | **`-$6,301.14`** |

---

## 5. Git Historical Audit

The Git audit executed:
```powershell
git log --oneline --all -- src/agricola/strategy/productive_mass_roi.py
git log --oneline --all -- scripts/benchmark_e11_performance.py
```
- **Git Evidence Availability:** **UNAVAILABLE** (Git commits stopped at commit `4445aa0 Close E08 productive scale experiment`). All E09, E10, and E11 development occurred within the workspace directory.
- **Primary Source of Truth:** `docs/versions/E11_03_expansion_gate_unlock.md` and `results/e11_productive_mass.json`.

---

## 6. Semantic Code & Logic Audit

| Function / Component | Historical Semantics | Current Semantics | Changed? | Causal Impact |
| :--- | :--- | :--- | :---: | :--- |
| **`_record_diagnostics`** | Counts `PLANT` tiles in owned quadrants | Counts `PLANT` tiles in owned quadrants | No | Identical tile counting semantics |
| **`_process_market_decisions`** | Checks `cash >= 1100.0` and `active_tiles >= 8` | Checks `cash >= 1100.0` and `active_tiles >= 8` | No | Identical readiness check logic |
| **`_buy_seeds_if_needed`** | Discretionary seeds blocked when `cash < 1300` | Discretionary seeds blocked when `cash < 1300` | No | Blocks high-yield seeds post-Q1 |
| **`_dispatch_worker_actions`** | Water-First priority (`WATER > HARVEST > PLANT`) | Water-First priority (`WATER > HARVEST > PLANT`) | No | Identical 5-tier action dispatch |

---

## 7. First Behavioral Divergence & Root Cause Analysis

### First Behavioral Divergence
```text
Day 5 (Hour 0):
  Expected (Documented E11-03): BUY_LAND Q2 executes (Cash >= $1,100, Active Tiles >= 8).
  Current Isolated Execution: BUY_LAND Q2 DOES NOT EXECUTE (Cash = $515.0 < $1,100.0).
```

### Empirical Root Cause
1. **Capital Drainage via Essential Seeds & Wages:** Post-Q1 acquisition on Day 1 (cost $1,000), liquid cash drops to $899. On Days 1–4, repeated essential seed purchases (Carrot $120, Wheat $60) and worker hiring drain cash down to $515–$816.
2. **Expansion Protection Lockout:** Discretionary high-yield seeds (Melon $320, Strawberry $400) require $1,300 cash float and remain permanently blocked.
3. **Productive Tile Depletion:** On Day 10–11, when harvested crop revenue brings cash above $1,100, the harvested tiles leave only 4 active plants on the farm (`active_tiles = 4 < 8 q2_gate`), permanently blocking `BUY_LAND` Q2 for the remainder of the episode.

---

## 8. Progressive Reproduction Test Results

- **Stage A (Single Episode, Seed 0):** Money = $439.00 – $13,152.00, Quadrants = 2, Peak Workers = 2, Peak Active = 14–17 (**Q2 NOT UNLOCKED**).
- **Stage B (Mini-Batch, 5 Seeds):** Mean Money = $12,585.60, 3Q Unlock Rate = 0.0%, 4Q Unlock Rate = 0.0% (**Q2 NOT UNLOCKED**).
- **Stage C (10 Seeds):** 3Q Unlock Rate = 0.0%, 4Q Unlock Rate = 0.0% (**Q2 NOT UNLOCKED**).
- **Stage D (Full 30-Episode Benchmark):** Mean Money = $895.23 – $7,167.80, 3Q Unlock Rate = **0.0%**, 4Q Unlock Rate = **0.0%**.

---

## 9. Final Reproduction Verdict & Recommendations

### Final Verdict: **`NOT REPRODUCED`**

E11-03 failed to reproduce its documented architectural fingerprint (0.0% 3Q unlock vs ~83.3% target; 0.0% 4Q unlock vs ~60.0% target).

### Impact on E11-06 & E11-07
- **E11-06 Status:** **`RESULT INVALID FOR CAUSAL INTERPRETATION`** (retains invalidation status).
- **E11-07 Status:** **`DO NOT DESIGN / DO NOT IMPLEMENT`** (blocked by Stop Gate Case B).

### Next Step Recommendation
**STOP GATE CASE B ENFORCED:** Stop all execution. Report divergence findings to Supervisor for architectural alignment before proceeding.

---

<!-- END OF FILE -->
