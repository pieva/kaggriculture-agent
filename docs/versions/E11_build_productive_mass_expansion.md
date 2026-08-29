# BUILD & VERIFY Report — E11-01 Productive Mass Expansion

**Date:** 2026-08-26  
**Phase:** E11-03 BUILD & E11-04 LOCAL SAFETY VERIFY  
**Status:** `E11-01 BUILD + LOCAL VERIFY COMPLETED — AWAITING SUPERVISOR REVIEW`  
**Strategy File Created:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Strategy Class:** `ProductiveMassROIAgent`  
**Config Class:** `ProductiveMassConfig`  
**Test File Created:** [`tests/test_e11_productive_mass.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_e11_productive_mass.py)  
**Benchmark Artifact:** [`results/e11_productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11_productive_mass.json)  
**Decision Gate Verdict:** **`FAIL`** (Mean Final Money **$23,837.57 < $50,000.00 Minimum Success Threshold**)  

---

## 1. Summary of Modifications to the PLAN

Before code implementation, `docs/versions/E11_plan_productive_mass_expansion.md` was formally updated:
1. **Initial Hypotheses Clarification:** All starting parameters (expansion days, active tile thresholds, hiring ratios, operating reserve, reinvestment threshold, Wheat/Cow/Sheep target counts, end-game cutoffs) were explicitly designated as **E11-01 Initial Hypotheses**, requiring empirical validation.
2. **Action Priority Hierarchy Refinement:** Updated to a 5-Tier Action Dispatch Hierarchy where strategic reinvestment (`BUY_LAND`, `HIRE`, animal buys) operates in Tier 3, ensuring time-critical crop watering and harvesting in Tier 1 are never interrupted.

---

## 2. Environment Mechanics Verification

All environment parameters were verified directly against `kaggle_environments` `kaggriculture` specification:
- **Board Grid:** 10x10 grid (100 tiles total) split into four 5x5 quadrants (Q0, Q1, Q2, Q3).
- **Starting Money:** $3,000.0 (or $1,000.0 local default).
- **`BUY_LAND` Cost:** $1,000.0 per quadrant.
- **`HIRE` Fibonacci Cost Curve:** $1, $1, $2, $3, $5, $8, $13, $21, $34, $55 for daily hires (`farmHandCostMult = 1`).
- **Crop Catalog (`CROPS`):**
  - `WHEAT`: Seed $10, Growth 4d, Yield 6 units, Price $25 -> Revenue $150 (Net $140/4d).
  - `CARROT`: Seed $20, Growth 3d, Yield 4 units, Price $35 -> Revenue $140 (Net $120/3d).
  - `TOMATO`: Seed $50, Growth 8d, Yield 5 units, Price $50 -> Revenue $250 (Net $200/8d).
  - `STRAWBERRY`: Seed $100, Growth 10d, Yield 4 units, Price $100 -> Revenue $400 (Net $300/10d).
  - `MELON`: Seed $80, Growth 12d, Yield 1 unit, Price $250 -> Revenue $250 (Net $170/12d).
- **Livestock Engine:** Cows ($400, 5 pasture tiles, Milk $160) & Sheep ($500, 4 pasture tiles, Wool $200), each consuming 1 Wheat/day.
- **Shed & Market Limits:** Shed capacity = 100 items; max 10 market orders per turn.

---

## 3. Implemented Architecture & Configuration (`ProductiveMassROIAgent`)

The complete multi-capability architecture was implemented in `src/agricola/strategy/productive_mass_roi.py`:

```text
                                PRODUCTIVE MASS ARCHITECTURE
┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐
│ Quadrant Locality Dispatcher │ 3-Tier Dynamic Crop Portfolio│ Scaled Market Brokerage      │
│ • Q0: Farmer + Hand 1        │ • Liquidity: CARROT (3d)     │ • Max 10 orders/turn         │
│ • Q1: Hand 2 + Hand 3        │ • Growth: TOMATO/STRAW/MELON │ • Shed 100 capacity tracking │
│ • Q2: Hand 4 + Hand 5        │ • Feed: WHEAT (4d)           │ • Milk ($160) & Wool ($200)  │
│ • Q3: Hand 6 + Hand 7+       │                              │   daily market sales         │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
```

### Initial Configuration Parameters (`ProductiveMassConfig`):
- `target_quadrants`: 4 (100 tiles total)
- `max_workers`: 10 (1 Farmer + up to 9 Hands)
- `operating_reserve`: $300.0 inviolable liquid cash floor
- `target_tiles_per_worker`: 7.0 active tiles per worker
- `livestock_enabled`: True (Target 6 Cows, 4 Sheep, Wheat feed buffer = 4)
- `reinvestment_threshold`: $1,500.0

---

## 4. Test Suite Execution (`tests/test_e11_productive_mass.py`)

5 unit & integration tests were created and passed cleanly:
1. `test_e11_initialization_config`: PASSED (100 tiles model, 4 quadrants defined).
2. `test_e11_dynamic_land_expansion_triggers`: PASSED (Q1 buy execution verified).
3. `test_e11_workforce_scaling_triggers`: PASSED (HIRE trigger on active tile ratio verified).
4. `test_e11_crop_portfolio_selection`: PASSED (3-tier crop selection & cutoff enforcement verified).
5. `test_e11_locality_dispatcher`: PASSED (Quadrant locality preference & spillover assist verified).

**Full Workspace Suite:** `pytest tests/` passed **55/55 tests (100%)** in 2.26s.

---

## 5. Local Safety Verification Benchmark Results (30 Paired Episodes)

The 30-episode paired benchmark evaluated E11-01 against E10-01, E09-01, E08, E06, and E05 on identical seeds (`0, 100, ..., 900`) across 10 x `pass`, 10 x `random`, and 10 x `starter` opponents:

| Metric | E05 (9t) | E06 (9t WF) | E08 (40t Live ON) | E09-01 (40t Live OFF) | E10-01 (40t Protection) | **E11-01 (100t Mass)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mean Final Money** | $21,518.97 | $24,879.03 | $11,502.93 | $21,000.93 | $23,405.57 | **`$23,837.57`** |
| **Median Final Money** | $21,442.00 | $25,847.00 | $9,602.50 | $27,332.00 | $23,854.50 | **`$24,165.50`** |
| **Sample Std Dev (`ddof=1`)** | ± $293.74 | ± $1,828.31 | ± $6,058.30 | ± $9,119.36 | ± $2,823.36 | **`± $1,781.29` (-37%)** |
| **Min Final Money** | $21,242.00 | $22,192.00 | $89.00 | $124.00 | $10,915.00 | **`$18,221.00` (+$7,306)** |
| **Max Final Money** | $22,585.00 | $27,873.00 | $22,276.00 | $28,004.00 | $26,331.00 | **`$25,059.00`** |
| **Episodes < $10k** | 0 | 0 | 16 | 7 | 0 | **`0`** |
| **Episodes < $20k** | 0 | 0 | 27 | 11 | 2 | **`3`** |
| **Episodes < $50k** | 30 | 30 | 30 | 30 | 30 | **`30`** |
| **Paired Wins vs E10-01** | - | - | - | - | Ref | **`22 / 30 (73.3%)`** |

---

## 6. Decision Gate Verdict

### Official Verdict: **`FAIL`**
- **Condition:** Mean Final Money **$23,837.57 < $50,000.00 Minimum Success Threshold**.
- **Paired Delta vs E10-01:** **+$432.00 (+1.85%)**. E11-01 beat E10-01 head-to-head in **22 out of 30 paired episodes (73.3%)**, and drastically reduced variance (SD dropped to ± $1,781.29, min money rose to $18,221.00), but failed to achieve the $50,000+ scale jump.

---

## 7. Trajectory & Checkpoint Comparison

| Checkpoint | Metric | E10-01 Baseline | E11-01 Treatment | Observed Growth Trajectory |
| :--- | :--- | :---: | :---: | :--- |
| **Day 7 (25%)** | Money | ~$1,000 | ~$944 | Q1 unlocked Day 4–6 |
| **Day 15 (50%)** | Money | ~$4,000 | ~$14,695 | High Melon revenue accumulated |
| **Day 22 (75%)** | Money | ~$12,000 | ~$19,052 | Production plateaued on Q0+Q1 |
| **Day 30 (100%)** | Final Money | **$23,405.57** | **$23,837.57** | **Linear production, missing exponential compounding** |

---

## 8. Dominant Bottleneck Diagnosis

Telemetry audit revealed the exact technical root cause of why E11-01 stopped scaling:

1. **Expansion Cash Lock (Primary Bottleneck):**
   - In E11-01, Q2 expansion required `cash >= $1,000.0 + $300.0 reserve` ($1,300) AND `active_tiles >= 20`.
   - On Days 6–12, seed purchasing spent cash on high-value seeds (Melon $320, Strawberry $400, Tomato $200), keeping liquid cash in the $400–$950 range.
   - Consequently, liquid cash **never reached $1,300 on Days 6–18**, causing `BUY_LAND` Q2 and Q3 to **NEVER EXECUTE**.
2. **Workforce Scaling Lock:**
   - Because Q2/Q3 were never unlocked (`owned_quadrants` stayed at 2), workforce scaling stopped at 4 workers.
3. **Livestock Lock:**
   - Livestock acquisition required `owned_quadrants >= 3`. Because Q2 was never unlocked, **0 Cows and 0 Sheep were ever purchased**.
4. **Summary:**
   - E11-01 successfully validated the underlying architecture (22/30 head-to-head wins vs E10, SD ± $1,781), but operated on only 2 quadrants (50 tiles, 4 workers) because the Q2 land expansion condition was blocked by pre-expansion seed spending.

---

## 9. Failure Mode Classification

- **Primary Failure Mode:** **Expansion Cash Lock / Liquidity Bottleneck** (Safeguard in E11-01 prevented Q2 land purchase because seed purchases drained cash below the $1,300 threshold).
- **Attribution:** The architectural foundation (Locality Dispatcher, 5-tier priority, multi-crop portfolio) is valid, but land acquisition parameters need liquidity timing protection identical to E10.

---

## 10. Proposed Next Step (E11-02 Optimization Direction)

Instead of abandoning the 100-tile architecture, **E11-02** will resolve the **Expansion Cash Lock**:
1. Protect $1,000 capital for Q2/Q3 land expansion prior to land purchase (preventing discretionary seed buys from draining cash below $1,000).
2. Allow `BUY_LAND` Q2 and Q3 to execute as soon as cash $\ge \$1,000.0$ (releasing redundant post-land reserve requirement).
3. Unlock full 4-quadrant land expansion, workforce scaling to 8–10 workers, and livestock integration.

---

<!-- END OF FILE -->
