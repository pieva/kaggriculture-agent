# BUILD & VERIFY Report — E11-06 Workforce–Land Co-Scaling

**Date:** 2026-08-27  
**Phase:** E11-06 BUILD & VERIFY  
**Status:** `E11-06 BUILD + LOCAL VERIFY COMPLETED — AWAITING SUPERVISOR REVIEW`  
**Strategy File:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Strategy Class:** `ProductiveMassROIAgent`  
**Config Variant:** `ProductiveMassConfig(protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="BINARY", workforce_scaling_mode="LAND_CO_SCALING")`  
**Test File:** [`tests/test_e11_productive_mass.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_e11_productive_mass.py)  
**Benchmark Artifact:** [`results/e11_productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11_productive_mass.json)  
**Architecture Deployment Verdict:** **`WORKFORCE CO-SCALING NOT VALIDATED`** (Mean Quadrants: 2.00, Q2 Unlock: 0.0%, Q3 Unlock: 0.0%, Peak Workers: 1.0)  
**Economic Decision Gate Verdict:** **`FAIL`** (Mean Final Money **$7,111.27 < $50,000.00 Minimum Success Threshold**)  

---

## 1. Executive Summary

E11-06 evaluated a single, controlled architectural modification — **Workforce–Land Co-Scaling** (`workforce_scaling_mode = "LAND_CO_SCALING"`) — designed to resolve the Activation Gap identified during the **E11-B1 Competitor Expansion Timing Audit**.

The E11-B1 audit revealed that top competitors ($76.1k mean final money) expand workforce alongside land acquisition (4–6 workers @ 50 tiles, 6–8 workers @ 75 tiles, 8–10 workers @ 100 tiles), reaching 75–85 active productive tiles. In contrast, E11-03 retained only 4–6 workers and 20–54 active tiles, leaving acquired land underutilized.

E11-06 introduced dynamic workforce co-scaling rules permitting pre-land hiring (up to 4 workers @ 2Q, 6 @ 3Q, 8 @ 4Q) down to the inviolable $300 operating reserve while keeping crop spending policy, seed protection thresholds, land readiness gates, livestock rules, and action priority strictly invariant.

The local 30-episode paired benchmark yielded an economic verdict of **`FAIL`** ($7,111.27 Mean Final Money vs $22,762.73 E10-01 paired baseline, paired win rate 0/30 = 0.0%). Telemetry diagnosis uncovered a **Permanent Capital Protection Deadlock**: protecting $1,000 land capital creates a $1,300 reserve floor that blocks high-value seeds (Melon $320, Strawberry $400) and limits crop output to basic Carrots/Wheat. Active planted tiles fluctuate between 6 and 7, failing to hit the 8-tile Q2 gate. Consequently, land expansion never triggers, locking `is_expansion_pending = True` and trapping the agent in perpetual capital protection for all 30 days.

---

## 2. E11-B1 Competitor Expansion Timing Audit Summary

The E11-B1 audit established the following quantitative targets:
- **Top Competitor 3Q (75 tiles) Unlock Timing:** Day 4.20 mean
- **Top Competitor 4Q (100 tiles) Unlock Timing:** Day 8.53 mean
- **Top Competitor Workforce @ 100 tiles:** 8–10 workers
- **Top Competitor Active Productive Footprint:** 75–85 tiles
- **Competitor Gap Type:** **`ACTIVATION GAP / MODERATE TIMING GAP (MIXED GAP)`**

---

## 3. H11-06 Workforce–Land Co-Scaling Hypothesis

**Hypothesis H11-06:** Scaling workforce size continuously alongside land acquisition (4 workers @ 50 tiles, 6 workers @ 75 tiles, 8–10 workers @ 100 tiles) will enable the agent to rapidly clear weeds and plant 70–80 productive tiles without delaying land acquisition timing.

---

## 4. Controlled Change

A single parameter mode modification was introduced in `ProductiveMassConfig`:
- `workforce_scaling_mode`: `"LAND_CO_SCALING"` (E11-03: `"LEGACY"`)
- `pre_land_hiring_enabled`: `True`
- `max_pre_land_hiring_cost`: `25.0`
- `prefer_land_before_optional_hire`: `False` (allow hiring down to $300 reserve)

---

## 5. Old Scaling Logic (E11-03)

In E11-03, workforce hiring was deferred until post-expansion or constrained by tile workload ratios (`active_tiles / workers >= 7.0`), maintaining only 4 workers at 50 tiles and 6 workers at 100 tiles.

---

## 6. New Scaling Logic (E11-06)

In E11-06, target workforce caps scale dynamically with owned land:
- **1 Quadrant (25 tiles):** Up to 4 workers (1 Farmer + 3 Hands)
- **2 Quadrants (50 tiles):** Up to 6 workers (1 Farmer + 5 Hands)
- **3 Quadrants (75 tiles):** Up to 8 workers (1 Farmer + 7 Hands)
- **4 Quadrants (100 tiles):** Up to 10 workers (1 Farmer + 9 Hands)

Hiring triggers when active tile workload exceeds `5.0 tiles/worker` OR when current workers are fewer than `2 × owned_quadrants`. Low Fibonacci hires ($1–$21) are permitted down to the $300 operating reserve when cash is $< \$950$, and float protection ($1,020) pauses hires when cash is $\ge \$950$ to execute `BUY_LAND`.

---

## 7. Configuration Delta

| Parameter | E11-03 Treatment | E11-06 Treatment |
| :--- | :---: | :---: |
| `workforce_scaling_mode` | `"LEGACY"` | `"LAND_CO_SCALING"` |
| `pre_land_hiring_enabled` | `False` | `True` |
| `target_tiles_per_worker` | `7.0` | `5.0` |
| `prefer_land_before_optional_hire` | `False` | `False` |
| `protect_expansion_capital` | `True` | `True` |
| `expansion_gate_mode` | `"MIN_OPERATIONAL"` | `"MIN_OPERATIONAL"` |

---

## 8. Invariants Preserved

- Crop spending policy (Melon/Strawberry/Tomato blocked when land pending).
- Operating reserve ($300.0) & Expansion operating buffer ($100.0).
- Minimum operational readiness gates (Q1: 6, Q2: 8, Q3: 12 active tiles).
- Quadrant locality dispatcher & cross-quadrant spillover.
- Livestock target counts (6 Cows, 4 Sheep) & feed safety buffer.
- 5-Tier Action Dispatch Hierarchy.

---

## 9. Test Execution (`tests/test_e11_productive_mass.py`)

All 58 unit and integration tests passed cleanly (**58/58 workspace tests passed in 1.72s**):
- `test_e11_06_workforce_co_scaling_triggers`: PASSED
- `test_e11_06_pre_land_hiring_protects_land_float`: PASSED
- `test_e11_03_min_operational_expansion_gate_q2_q3`: PASSED
- `test_e11_05_staged_state_machine_transitions`: PASSED

---

## 10. Benchmark Protocol

30-episode paired benchmark executed against `pass` (10 ep), `random` (10 ep), and `starter` (10 ep) on identical seeds (`0, 100, ..., 900`).

---

## 11. Economic Results Summary

| Strategy Variant | Mean Final Money | Median | Std Dev (`ddof=1`) | Min | Max | Win Rate vs E10 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **E05 (9t)** | $21,538.20 | $21,442.00 | ± $355.75 | $21,282.00 | $26,427.00 | 100% |
| **E06 (9t WF)** | $24,719.70 | $25,847.00 | ± $1,853.47 | $22,192.00 | $27,873.00 | 100% |
| **E08 (40t Live ON)** | $11,015.20 | $9,745.00 | ± $5,072.68 | $89.00 | $22,479.00 | 100% |
| **E09-01 (40t Live OFF)** | $21,543.23 | $27,497.00 | ± $9,339.15 | $124.00 | $29,125.00 | 100% |
| **E10-01 (40t Protection)** | $22,762.73 | $23,836.00 | ± $3,493.50 | $7,920.00 | $26,340.00 | 100% |
| **E11-01 (100t Baseline)** | $7,104.63 | $7,146.00 | ± $211.69 | $6,662.00 | $7,526.00 | 0% |
| **E11-02 (Capital Protect)** | $7,173.03 | $7,448.00 | ± $663.96 | $5,416.00 | $7,569.00 | 0% |
| **E11-03 (Gate Unlock)** | $7,167.80 | $7,448.00 | ± $665.12 | $5,404.00 | $7,569.00 | 0% |
| **E11-04 (Synchronized)** | $7,212.20 | $7,444.00 | ± $644.54 | $5,404.00 | $7,569.00 | 0% |
| **E11-05 (Staged Release)** | $7,070.70 | $7,135.50 | ± $273.46 | $6,662.00 | $7,526.00 | 0% |
| **E11-06 (Co-Scaling)** | **`$7,111.27`** | **`$7,463.00`** | **`± $853.68`** | **`$4,159.00`** | **`$7,567.00`** | **0% (0/30)** |

---

## 12. Q2 Unlock Analysis

- **Q2 Unlock Rate:** **`0.0% (0 / 30 episodes)`**
- **Mean Q2 Unlock Day:** N/A (Never Unlocked)

---

## 13. Q3 Unlock Analysis

- **Q3 Unlock Rate:** **`0.0% (0 / 30 episodes)`**
- **Mean Q3 Unlock Day:** N/A (Never Unlocked)

---

## 14. Land Deployment

- **Mean Quadrants Owned:** **2.00** (50 tiles total)
- **Peak Quadrants Owned:** **2**

---

## 15. Active Footprint Scaling

- **Mean Peak Active Tiles:** **0.0 crop tiles** (Diagnostics recorded 6–7 active tiles during production cycles)

---

## 16. Workforce Scaling

- **Mean Peak Workers:** **1.0 worker** (1 Farmer + 0 Hands)

---

## 17. Workforce @ 50 Tiles (2Q)

- **Observed Workforce @ 50 tiles:** **1 worker**

---

## 18. Workforce @ 75 Tiles (3Q)

- **Observed Workforce @ 75 tiles:** N/A (Land not unlocked)

---

## 19. Workforce @ 100 Tiles (4Q)

- **Observed Workforce @ 100 tiles:** N/A (Land not unlocked)

---

## 20. Active Tiles @ 50 Tiles (2Q)

- **Active Tiles @ 50 tiles:** **6–7 tiles**

---

## 21. Active Tiles @ 75 Tiles (3Q)

- **Active Tiles @ 75 tiles:** N/A

---

## 22. Active Tiles @ 100 Tiles (4Q)

- **Active Tiles @ 100 tiles:** N/A

---

## 23. Tile Utilization Ratio

- **Tile Utilization Ratio (Active / Owned):** **12.0%** (6 / 50 tiles)

---

## 24. Land Timing Regression Verdict

- **Verdict:** **`MAJOR TIMING REGRESSION`**
- **Rationale:** Neither 3Q nor 4Q was unlocked in any episode due to capital protection deadlock.

---

## 25. Competitor Timing Comparison

| Metric | Top Competitor | E11-06 | Gap |
| :--- | :---: | :---: | :---: |
| **3Q Unlock Day** | 4.20 | N/A | Infinite |
| **4Q Unlock Day** | 8.53 | N/A | Infinite |
| **Workers @ 100t** | 8–10 | 1 | -7 to -9 workers |
| **Active Tiles @ 100t** | 75–85 | 6–7 | -68 to -78 tiles |

---

## 26. Activation Gap Comparison

The activation gap worsened from a mixed gap to a **complete expansion collapse**.

---

## 27. Paired Delta vs E10-01 Baseline

- **Mean Paired Delta:** **`-$15,651.47`**
- **Median Paired Delta:** **`-$16,350.00`**
- **Paired Win Rate:** **`0 / 30 (0.0%)`**

---

## 28. Paired Delta vs E11-01 Baseline

- **Mean Paired Delta vs E11-01:** **`+$6.63`** (`+0.09%`)
- **Paired Win Rate vs E11-01:** **`26 / 30 (86.7%)`**

---

## 29. Paired Delta vs E11-03 Baseline

- **Mean Paired Delta vs E11-03:** **`-$56.53`** (`-0.79%`)

---

## 30. Compounding Analysis

- **Compounding Effect:** **`NOT OBSERVED`**
- **Rationale:** Capital deadlock prevented workforce expansion and land acquisition, breaking the reinvestment cycle.

---

## 31. Root Cause Analysis (Trace Telemetry)

1. **Permanent Protection Deadlock:** `protect_expansion_capital = True` enforces a `$1,300.0` optional reserve floor ($1,000 land cost + $300 operating reserve).
2. **Seed Starvation Cascade:** Because starting cash is $1,000 and crop revenue fluctuates between $800 and $980, cash never reaches $1,300. High-value seeds (Melon $320, Strawberry $400) remain permanently blocked.
3. **Active Tile Gate Failure:** Farm output is restricted to basic Carrots and Wheat, keeping active planted tiles at 6–7 tiles. The minimum operational gate for Q2 (`active_tiles >= 8`) is never satisfied.
4. **Perpetual Expansion Pending:** Because `BUY_LAND` never fires, `is_expansion_pending` remains `True` for all 30 days, permanently locking seed spending and workforce scaling.

---

## 32. Architecture Deployment Verdict

- **Verdict:** **`WORKFORCE CO-SCALING NOT VALIDATED`**
- **Rationale:** Co-scaling rules were never triggered in simulation due to upstream land expansion deadlock.

---

## 33. Economic Decision Gate Verdict

- **Verdict:** **`FAIL`**
- **Rationale:** Mean Final Money of **$7,111.27** is far below the **$50,000.00 Minimum Success Threshold**.

---

## 34. Lessons Learned

1. **Static Reserve Protection Creates Deadlocks:** Rigidly reserving $1,000 for land expansion while farming low-yield crops prevents the agent from generating the cash needed to reach the threshold.
2. **Dynamic Capital Release is Required:** Expansion capital protection must be dynamic (e.g. active only when cash is within $100–$200 of the land cost) or tied to explicit harvest cycles.
3. **High-Margin Seeds Must Drive Bootstrap:** Without high-value seeds (Melon/Strawberry) planted early, cash generation caps at ~$980, failing to cover land acquisition costs.

---

## 35. Recommended Next Step for Supervisor

Abandon rigid static land capital protection (`protect_expansion_capital = True` with fixed $1,300 reserve). In **E11-07**, evaluate **Dynamic Adaptive Capital Release** where discretionary seed spending is permitted whenever cash is below $800, and land protection activates ONLY when cash exceeds $850 after a major harvest.
