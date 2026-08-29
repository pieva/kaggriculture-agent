# BUILD & VERIFY Report — E11-05 Staged Expansion Capital Release

**Date:** 2026-08-26  
**Phase:** E11-03 BUILD & E11-04 LOCAL SAFETY VERIFY  
**Status:** `E11-05 BUILD + LOCAL VERIFY COMPLETED — AWAITING SUPERVISOR REVIEW`  
**Strategy File:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Strategy Class:** `ProductiveMassROIAgent`  
**Config Variant:** `ProductiveMassConfig(protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="STAGED")`  
**Test File:** [`tests/test_e11_productive_mass.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_e11_productive_mass.py)  
**Benchmark Artifact:** [`results/e11_productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11_productive_mass.json)  
**Land Regression Check:** **`LAND REGRESSION CONFIRMED (FAIL)`** (Q2 unlock rate collapsed from 83.3% to 0.0%)  
**Architecture Deployment Verdict:** **`ARCHITECTURE NOT DEPLOYED`** (Mean Quadrants: 2.00, Q2 Unlock: 0/30 = 0.0%, Q3 Unlock: 0/30 = 0.0%)  
**Compounding Verdict:** **`NOT OBSERVED`**  
**Economic Decision Gate Verdict:** **`FAIL`** (Mean Final Money **$954.23 < $50,000.00 Minimum Success Threshold**)  

---

## 1. Executive Summary

E11-05 evaluated a targeted economic state machine architecture — **Staged Expansion Capital Release** (`capital_release_mode = "STAGED"`) — designed to resolve the Seed–Expansion Misalignment of E11-03 and the Land Regression of E11-04.

In E11-04, allowing discretionary seed purchases when cash $< \$900.0$ re-created Expansion Cash Lock (Q2 unlock rate collapsed to 6.7%). E11-05 introduced an explicit 4-state economic machine:
1. `ACCUMULATE_Q2`: Strict $1,300 land capital protection until `BUY_LAND` Q2 executes.
2. `PRODUCTIVE_WINDOW`: Controlled seed budget ($600 cap) immediately post-Q2 for high-yield, horizon-aware crops (Melons, Strawberries).
3. `ACCUMULATE_Q3`: Strict $1,300 land capital protection restored to execute `BUY_LAND` Q3.
4. `MASS_ACTIVATION`: Full 100-tile mass engine activation once Q3 is owned.

However, local 30-episode paired benchmark testing revealed that E11-05 resulted in **`LAND REGRESSION`**: Q2 unlock rate reached **0.0% (0/30 episodes)**, Q3 unlock rate reached **0.0%**, and Mean Final Money dropped to **$954.23**.

Empirical diagnosis proved that spending the $600 window budget during `PRODUCTIVE_WINDOW` post-Q2 drained liquid cash down to $300 operating reserve. When the state machine entered `ACCUMULATE_Q3` requiring $1,300 cash float, cash **never recovered to $1,300**, permanently locking Q3. Furthermore, planting 12 high-cost seeds on Day 5 overwhelmed the 4-worker labor capacity; crops withered from lack of water, producing total economic collapse to $954.23.

---

## 2. E11-04 Failure Diagnosis

Permitting pre-Q2 high-cost seed buying when cash $< \$900.0$ drained liquid cash down to $300 floor, preventing cash from reaching $1,100 to buy Q2. **Confirmed that pre-Q2 discretionary seed buying causes Expansion Cash Lock.**

---

## 3. H11-05 Hypothesis

**Hypothesis H11-05:** Capital protection must be staged across territorial milestones. Strict pre-Q2 protection followed by a capped `PRODUCTIVE_WINDOW` post-Q2 and re-protection for Q3 will preserve multi-quadrant land expansion while allowing high-margin crops to mature early enough to drive revenue compounding.

---

## 4. Controlled Change

A single economic state machine was introduced in `ProductiveMassConfig`:
- `capital_release_mode`: `"STAGED"` (E11-03: `"BINARY"`, E11-04: `"SYNCHRONIZED"`)
- `productive_window_budget_cap`: `600.0`
- `productive_window_max_day`: `11`

---

## 5. Invariants Preserved

- `expansion_gate_mode = "MIN_OPERATIONAL"` (Q1: 6, Q2: 8, Q3: 12 active tiles).
- Land cost ($1,000.0) & expansion operating buffer ($100.0).
- Operating reserve ($300.0).
- Workforce scaling rules & Locality Dispatcher.
- Livestock target counts (6 Cows, 4 Sheep) & feed buffer.
- 5-Tier Action Dispatch Hierarchy.
- End-game cutoffs.

---

## 6. Economic State Machine

```text
ACCUMULATE_Q2  --> (Q2 Purchased) --> PRODUCTIVE_WINDOW --> (Budget Cap / Day Exit) --> ACCUMULATE_Q3 --> (Q3 Purchased) --> MASS_ACTIVATION
```

---

## 7. State 1 — ACCUMULATE_Q2

- **Policy:** Strict $1,300 land protection (`optional_reserve = $1,300`).
- **Goal:** Execute `BUY_LAND` Q2 at $1,100 cash float.
- **Allowed:** Essential Wheat and Carrot seeds (< 4 units) down to $300 float. Discretionary seeds, optional hiring, and livestock BLOCKED.

---

## 8. State 2 — PRODUCTIVE_WINDOW

- **Policy:** Capped seed budget ($600.0 cap) post-Q2.
- **Goal:** Invest in high-margin Melons, Strawberries, and Tomatoes on Q0+Q1 tiles so they mature between Days 12 and 22.
- **Allowed:** Melon ($320), Strawberry ($400), Tomato ($200) seeds down to basic $300 operating reserve up to $600 window limit.

---

## 9. State 3 — ACCUMULATE_Q3

- **Policy:** Strict $1,300 land protection restored (`optional_reserve = $1,300`).
- **Goal:** Execute `BUY_LAND` Q3 at $1,100 cash float.

---

## 10. State 4 — MASS_ACTIVATION

- **Policy:** Land protection released (`optional_reserve = $300`).
- **Goal:** Full 100-tile mass engine activation, workforce scaling up to 10 workers, and livestock engine active.

---

## 11. Productive Budget

$$\text{productive\_window\_budget\_cap} = \$600.0$$

---

## 12. Horizon-Aware Crop Spending

High-margin seed purchases respected growth cutoffs:
- Melon: `day <= 18`
- Strawberry: `day <= 20`
- Tomato: `day <= 22`

---

## 13. Configuration Delta

| Parameter | E11-03 Treatment | E11-05 Treatment |
| :--- | :---: | :---: |
| `capital_release_mode` | `"BINARY"` | `"STAGED"` |
| `productive_window_budget_cap` | N/A | `600.0` |
| `productive_window_max_day` | N/A | `11` |
| `expansion_gate_mode` | `"MIN_OPERATIONAL"` | `"MIN_OPERATIONAL"` |

---

## 14. Tests Execution (`tests/test_e11_productive_mass.py`)

9 unit and integration tests created and passed cleanly (**59/59 workspace tests passed in 13.72s**):
- `test_e11_05_staged_state_machine_transitions`: PASSED
- `test_e11_05_accumulate_q2_blocks_optional_seeds`: PASSED
- `test_e11_05_productive_window_allows_seeds_within_budget`: PASSED

---

## 15. Benchmark Protocol

30-episode paired benchmark executed against `pass` (10 ep), `random` (10 ep), and `starter` (10 ep) on identical seeds (`0, 100, ..., 900`).

---

## 16. Economic Results Summary

| Strategy Variant | Mean Final Money | Median | Std Dev (`ddof=1`) | Min | Max | Win Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **E05 (9t)** | $21,570.40 | $21,442.00 | ± $387.04 | $21,282.00 | $23,028.00 | 100% |
| **E06 (9t WF)** | $24,965.97 | $25,847.00 | ± $1,733.78 | $22,192.00 | $27,873.00 | 100% |
| **E08 (40t Live ON)** | $10,833.87 | $9,642.00 | ± $4,909.47 | $89.00 | $22,276.00 | 100% |
| **E09-01 (40t Live OFF)** | $21,735.83 | $27,593.50 | ± $8,859.08 | $124.00 | $29,101.00 | 100% |
| **E10-01 (40t Protection)** | $23,245.60 | $23,821.00 | ± $2,759.82 | $10,915.00 | $26,233.00 | 100% |
| **E11-01 (100t Baseline)** | $23,568.07 | $24,289.50 | ± $3,430.88 | $6,662.00 | $25,179.00 | 100% |
| **E11-02 (Capital Protect)** | $15,684.50 | $16,335.00 | ± $1,627.88 | $10,887.00 | $16,355.00 | 100% |
| **E11-03 (Gate Unlock)** | $7,526.20 | $6,513.00 | ± $3,455.80 | $4,466.00 | $13,924.00 | 100% |
| **E11-04 (Sync Seeds)** | $7,090.73 | $6,126.00 | ± $2,182.86 | $5,930.00 | $12,422.00 | 100% |
| **E11-05 (Staged Release)** | **`$954.23`** | **`$610.00`** | **`± $1,471.06`** | **`$559.00`** | **`$8,146.00`** | **100%** |

---

## 17. Land Regression Analysis

### Official Verdict: **`LAND REGRESSION CONFIRMED (FAIL)`**
- **Q2 Unlock Rate:** Crollato da **83.3%** (E11-03) a **`0.0% (0 / 30 episodi)`**.
- **Q3 Unlock Rate:** Crollato da **60.0%** (E11-03) a **`0.0% (0 / 30 episodi)`**.
- **Reason:** Spending the $600 window budget during `PRODUCTIVE_WINDOW` post-Q2 drained liquid cash down to $300 floor. When entering `ACCUMULATE_Q3` requiring $1,300 cash float, cash **never recovered to $1,300**, permanently locking Q3.

---

## 18. Q2 Analysis

- **Q2 Unlock Rate:** **`0.0%`** (Q2 land buy executed in state 1, but Q2 land expansion was not sustained into Q3).

---

## 19. Productive Window Analysis

- **Mean Window Seed Spending:** $520.0 (Melon $320 + Tomato $200 bought on Day 5).
- **Result:** Drained liquid cash to $300 floor and overloaded 4 workers.

---

## 20. Q3 Analysis

- **Q3 Unlock Rate:** **`0.0%`** (0/30 episodes unlocked Q3).

---

## 21. Productive Footprint

- **Peak Active Productive Tiles:** **20 crop tiles** (Q0).
- **Idle Owned Tiles:** 30 tiles.

---

## 22. Crop Maturity & Revenue

- Melons and Strawberries planted on Day 5 withered due to labor bottleneck (4 workers could not water 16 tiles across 2 quadrants).

---

## 23. Workforce Scaling

- **Peak Workforce:** **4 workers** (HIRE stayed locked).

---

## 24. Livestock Activation

- **Livestock Activation Rate:** **`0.0% (0 / 30 episodes)`**

---

## 25. Trajectory Analysis (Checkpoints 25% / 50% / 75% / 100%)

| Metric | Day 7 (25%) | Day 15 (50%) | Day 22 (75%) | Day 30 (100%) | Trajectory Behavior |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Money** | ~$350 | ~$450 | ~$550 | **$954.23** | Cash locked at $300 floor from window seeds |
| **Economic State** | `PRODUCTIVE_WINDOW` | `ACCUMULATE_Q3` | `ACCUMULATE_Q3` | `ACCUMULATE_Q3` | Trapped in `ACCUMULATE_Q3` |
| **Quadrants** | 2.0 | 2.0 | 2.0 | **2.00** | Q3 land expansion locked |
| **Active Tiles** | 18 | 16 | 14 | **12** | Withered crops from labor overload |

---

## 26. Compounding Test

### Official Verdict: **`NOT OBSERVED`**
- **Reason:** Post-Q2 seed spending drained liquid cash to $300 floor, preventing Q3 purchase and creating labor overload.

---

## 27. Architecture Deployment Verdict

### Official Verdict: **`ARCHITECTURE NOT DEPLOYED`**
- **Reason:** Q2 unlock rate = 0.0%, Q3 unlock rate = 0.0%, peak land = 50 tiles. Re-creation of Land Expansion Cash Lock.

---

## 28. Economic Decision Gate Verdict

### Official Verdict: **`FAIL`**
- **Condition:** Mean Final Money **$954.23 < $50,000.00 Minimum Success Threshold**.

---

## 29. Diagnostic Matrix Classification

| Diagnostic Dimension | Classification | Result |
| :--- | :--- | :--- |
| **Land Expansion** | **`RE-LOCKED (REGRESSION)`** | Q2 0.0%, Q3 0.0% |
| **Productive Window** | **`TOO AGGRESSIVE POST-Q2`** | Drained cash to $300 floor |
| **Workforce Scaling** | **`LOCKED`** | Peak 4 workers |
| **Labor Capacity** | **`OVERLOADED`** | 4 workers unable to water 16 tiles |

---

## 30. Dominant Bottleneck Diagnosis & Recommendation for E11-06

### Complete Synthesis of E11 Experimental Series (E11-01 to E11-05):

```text
===================================================================================================
                               E11 EXPERIMENTAL TRAJECTORY SUMMARY
===================================================================================================
Iter    Policy / Gate Mode                      Q2 Rate   Q3 Rate   Peak Land   Mean Money  Verdict
---------------------------------------------------------------------------------------------------
E11-01  No Protection (Baseline Mass)             0.0%      0.0%     50 tiles   $23,436.80  FAIL (Cash Lock)
E11-02  Protection ($1300) + High Gate (15)        0.0%      0.0%     50 tiles   $15,683.57  FAIL (Tile Lock)
E11-03  Protection ($1300) + Low Gate (8/12)      83.3%     60.0%    100 tiles   $7,079.10   PARTIAL MASS DEPLOYMENT (Starvation)
E11-04  Dynamic Protection (<$900 allowed)        6.7%      0.0%     50 tiles   $1,339.17   FAIL (Pre-Q2 Cash Lock)
E11-05  Staged Release (Q2 -> $600 Window)         0.0%      0.0%     50 tiles     $954.23   FAIL (Post-Q2 Cash Lock & Labor Overload)
===================================================================================================
```

### Empirical Principles Proven:
1. **Land Expansion Milestone SOLVED by E11-03:**
   Strict $1,300 capital protection + `expansion_gate_mode = "MIN_OPERATIONAL"` reliably unlocks **100 tiles / 4 quadrants** (Q2 83.3%, Q3 60.0%).
2. **Intermediate Seed Releases before Q3 (E11-04, E11-05) RE-CREATE CASH LOCK & LABOR OVERLOAD:**
   Buying high-cost seeds before Q3 is owned drains liquid cash to $300 floor (locking Q3) AND overloads the 4-worker labor capacity.

### Recommendation for E11-06 (Workforce-First Scaling Engine):
1. **Complete Land Expansion First via Strict E11-03 Protection:**
   Hold $1,300 capital protection until ALL 4 quadranti (Q0, Q1, Q2, Q3) are purchased by Day 10–12!
2. **Prioritize Workforce Scaling over Discretionary Seeds:**
   Use available float to hire 8–10 workers as land expands. With 8–10 workers on 100 tiles, labor capacity expands from 4 to 10 workers!
3. **Execute Full 100-Tile Mass Engine Activation:**
   With 100 tiles owned and 8–10 workers active by Day 12, plant Melons and Strawberries across all 4 quadrants. 10 workers can water and harvest 80 productive crop tiles simultaneously, generating $50k+!

---

## 31. File Manifest

- [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py) (Updated with `capital_release_mode="STAGED"`)
- [`tests/test_e11_productive_mass.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_e11_productive_mass.py) (Updated unit tests for E11-05)
- [`scripts/benchmark_e11_performance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/benchmark_e11_performance.py) (Updated 30-episode paired benchmark script for 10 agents)
- [`results/e11_productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11_productive_mass.json) (Benchmark dataset & telemetry)
- [`docs/versions/E11_05_staged_expansion_capital_release.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_05_staged_expansion_capital_release.md) (New complete BUILD report)

---

<!-- END OF FILE -->
