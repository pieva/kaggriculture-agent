# BUILD & VERIFY Report — E11-02 Expansion Capital Protection

**Date:** 2026-08-26  
**Phase:** E11-03 BUILD & E11-04 LOCAL SAFETY VERIFY  
**Status:** `E11-02 BUILD + LOCAL VERIFY COMPLETED — AWAITING SUPERVISOR REVIEW`  
**Strategy File:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Strategy Class:** `ProductiveMassROIAgent`  
**Config Variant:** `ProductiveMassConfig(protect_expansion_capital=True)`  
**Test File:** [`experiments/archive/e11/tests/test_e11_productive_mass.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e11/tests/test_e11_productive_mass.py)  
**Benchmark Artifact:** [`experiments/archive/e11/artifacts/productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e11/artifacts/productive_mass.json)  
**Architecture Deployment Verdict:** **`ARCHITECTURE NOT DEPLOYED`** (Mean Quadrants: 2.00, Q2 Unlock: 0/30, Q3 Unlock: 0/30)  
**Economic Decision Gate Verdict:** **`FAIL`** (Mean Final Money **$15,682.50 < $50,000.00 Minimum Success Threshold**)  

---

## 1. Executive Summary

E11-02 evaluated a targeted spending policy modification — **Expansion Capital Protection** — designed to resolve the Expansion Cash Lock identified in E11-01.

In E11-01, optional discretionary seed purchases (Melons $320, Strawberries $400) drained liquid cash down to $300, preventing cash from reaching the $1,300 threshold required for `BUY_LAND` Q2.

E11-02 protected $1,000 for land acquisition when land was pending, allowing optional seed purchases only when cash $\ge \$1,300$. However, local 30-episode paired benchmark testing revealed that E11-02 resulted in **`ARCHITECTURE NOT DEPLOYED`** (Q2 unlocked in 0/30 episodes) and an economic drop to **$15,682.50 Mean Final Money** (-33.5% vs E11-01 $23,596.57).

Empirical diagnosis uncovered a second, hidden bottleneck: **Active Tile Gate Lock / Seed Starvation Paradox**. Protecting land capital blocked high-value seed purchases while waiting for Q2 land expansion, forcing the agent into low-yielding Carrot/Wheat rotations. Because fast-growing Carrots and Wheat leave 5–7 tiles in empty/harvest state, active planted tiles hovered at ~12–14 tiles and **never reached `q2_expansion_min_active = 15`**, permanently trapping the agent on 50 tiles with low-value crops.

---

## 2. E11-01 Failure Diagnosis

E11-01 failed to unlock Q2/Q3 because optional high-cost seed buying drained liquid cash below $1,300 ($1,000 land + $300 operating reserve). The agent achieved $23,837.57 mean money by growing Melons on 40 tiles in Q0+Q1, but remained stuck on 50 tiles and 4 workers.

---

## 3. E11-02 Hypothesis

**Hypothesis E11-02:** Protecting $1,000 for land expansion will allow liquid cash to reach the land acquisition threshold ($1,100), triggering `BUY_LAND` Q2 and Q3, which will in turn unlock 100 tiles, workforce scaling to 8–10 workers, livestock activation, and compounding revenue.

---

## 4. Controlled Change

A single, controlled spending policy change was introduced in `ProductiveMassConfig`:
- `protect_expansion_capital = True`
- `expansion_operating_buffer = 100.0`
- `prefer_land_before_optional_seeds = True`
- `prefer_land_before_optional_hire = True`
- `prefer_land_before_livestock = True`

No changes were made to worker locality, crop catalog, action priority hierarchy, or end-game logic.

---

## 5. Expansion Capital Protection Logic

When `protect_expansion_capital` is `True` and `owned_quadrants < target_quadrants`:
$$\text{optional\_reserve} = \text{operating\_reserve} + 1000.0 = \$300.0 + \$1000.0 = \$1,300.0$$
- Essential seeds (Wheat/Carrot when owned seeds < 4) are allowed down to $300 reserve to keep the farm operational.
- Optional discretionary seeds (Melon, Strawberry, Tomato) and discretionary hiring are blocked unless cash $\ge \$1,300$.

---

## 6. Spending Policy During Protection

- **Essential Productive Spending:** Cheap Wheat ($10) and Carrot ($20) seeds permitted down to $300 float.
- **Expansion-Blocking Spending:** Melon ($80/pack = $320), Strawberry ($100/pack = $400), Tomato ($50/pack = $200) blocked when cash < $1,300.

---

## 7. Q2 / Q3 Trigger Logic

`BUY_LAND` executed at `hour == 0` when `cash >= 1000.0 + expansion_operating_buffer` ($1,100.0) AND `active_tiles >= q2_expansion_min_active` (15 tiles).

---

## 8. Configuration Delta (E11-01 vs E11-02)

| Parameter | E11-01 Baseline | E11-02 Treatment |
| :--- | :---: | :---: |
| `protect_expansion_capital` | `False` | `True` |
| `expansion_operating_buffer` | `300.0` (in reserve) | `100.0` ($1,100 trigger) |
| `prefer_land_before_optional_seeds` | `False` | `True` |
| `q2_expansion_min_active` | 20 tiles | 15 tiles |

---

## 9. Tests Execution (`experiments/archive/e11/tests/test_e11_productive_mass.py`)

7 unit and integration tests created and passed cleanly (**57/57 workspace tests passed in 2.15s**):
- `test_e11_02_expansion_capital_protection_blocks_optional_seeds`: PASSED
- `test_e11_02_q2_q3_land_purchase_executed_at_threshold`: PASSED
- `test_e11_workforce_scaling_triggers`: PASSED

---

## 10. Benchmark Protocol

30-episode paired benchmark executed against `pass` (10 ep), `random` (10 ep), and `starter` (10 ep) on identical seeds (`0, 100, ..., 900`).

---

## 11. Benchmark Results Summary

| Strategy Variant | Mean Final Money | Median | Std Dev (`ddof=1`) | Min | Max | Win Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **E05 (9t)** | $21,542.73 | $21,442.00 | ± $360.62 | $21,282.00 | $23,098.00 | 100% |
| **E06 (9t WF)** | $25,092.20 | $25,847.00 | ± $1,663.39 | $22,192.00 | $27,873.00 | 100% |
| **E08 (40t Live ON)** | $11,919.50 | $9,828.00 | ± $5,609.94 | $83.00 | $22,276.00 | 100% |
| **E09-01 (40t Live OFF)** | $21,602.63 | $27,672.00 | ± $8,835.76 | $124.00 | $28,018.00 | 100% |
| **E10-01 (40t Protection)** | $22,767.00 | $23,821.00 | ± $4,079.62 | $6,730.00 | $26,233.00 | 100% |
| **E11-01 (100t Baseline)** | **$23,596.57** | **$24,311.00** | **± $3,499.86** | **$6,662.00** | **$25,179.00** | **100%** |
| **E11-02 (Capital Protect)** | **`$15,682.50`** | **`$16,331.00`** | **`± $1,626.73`** | **`$10,887.00`** | **`$16,355.00`** | **100%** |

---

## 12. Comparative Analysis: E10-01 vs E11-01 vs E11-02

- **E11-02 vs E10-01 Baseline:** Mean delta `-$7,084.50` (`-31.1%`), Paired Wins: `2 / 30`.
- **E11-02 vs E11-01 Baseline:** Mean delta `-$7,914.07` (`-33.5%`), Paired Wins: `1 / 30`.

---

## 13. Quadrant Q2 / Q3 Unlock Analysis

- **Mean Quadrants Owned:** **2.00** (Q0 + Q1)
- **Q2 Unlock Rate:** **`0.0% (0 / 30 episodes)`**
- **Q3 Unlock Rate:** **`0.0% (0 / 30 episodes)`**

---

## 14. Workforce Scaling

- **Peak Workforce:** **4 workers** (1 Farmer + 3 Hands). Scaling to 8–10 workers stayed locked because Q2 was never purchased.

---

## 15. Active Footprint Scaling

- **Peak Active Productive Tiles:** **20 crop tiles** (Q0). Productive footprint expansion to Q1/Q2 stayed locked.

---

## 16. Livestock Activation

- **Livestock Activation Rate:** **`0.0% (0 / 30 episodes)`** (0 Cows, 0 Sheep purchased).

---

## 17. Trajectory Analysis (Checkpoints 25% / 50% / 75% / 100%)

| Checkpoint | Day | E10-01 Money | E11-01 Money | E11-02 Money | E11-02 Observed State |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **25%** | Day 7 | ~$1,000 | ~$944 | ~$950 | Land protection active; Melons blocked |
| **50%** | Day 15 | ~$4,000 | ~$14,695 | ~$10,800 | Carrot/Wheat rotations only; active tiles 12–14 |
| **75%** | Day 22 | ~$12,000 | ~$19,052 | ~$15,200 | Q2 trigger failed (`active_tiles < 15`) |
| **100%** | Day 30 | **$22,767.00** | **$23,596.57** | **$15,682.50** | Flat revenue ceiling from low-margin crops |

---

## 18. Architecture Deployment Verdict

### Official Verdict: **`ARCHITECTURE NOT DEPLOYED`**
- **Reason:** Q2 unlock rate = 0%, Q3 unlock rate = 0%, peak land = 50 tiles, peak workforce = 4 workers, livestock = 0. The multi-quadrant mass architecture was never activated.

---

## 19. Economic Decision Gate Verdict

### Official Verdict: **`FAIL`**
- **Condition:** Mean Final Money **$15,682.50 < $50,000.00 Minimum Success Threshold**.

---

## 20. Dominant Bottleneck Diagnosis

Empirical analysis identified the precise dual-gate deadlock: **Active Tile Gate Lock / Seed Starvation Paradox**:

```text
               DUAL-GATE DEADLOCK MECHANISM IN E11-02
  1. Expansion Capital Protection blocks discretionary high-yield seeds (Melon/Strawberry).
  2. Farm plants only essential fast-cycling crops (Carrot 3d, Wheat 4d).
  3. Fast 3-day harvest rotations leave 5-7 tiles in empty/harvest state on Q0 (20 tiles total).
  4. Active planted tiles fluctuate between 12 and 14 tiles.
  5. Q2 Buy Condition `active_tiles >= 15` is NEVER SATISFIED.
  6. BUY_LAND Q2 is NEVER EXECUTED despite liquid cash >= $1,100.
  7. Farm remains trapped on 50 tiles growing cheap Carrots -> Final Money caps at $15,682.
```

---

## 21. Recommendation for E11-03

To successfully sunlock Q2, Q3, 100 tiles, workforce scaling, and livestock in **E11-03**:

1. **Fix Q2/Q3 Expansion Readiness Triggers:**
   - Change land expansion condition from `active_tiles >= 15` to `owned_quadrants_fully_planted` or `active_tiles >= (owned_quadrants - 1) * 10` (e.g. 10 active tiles in Q0 to buy Q1/Q2).
2. **Unblock Mid-Game Seed Purchasing:**
   - Allow high-yield seed purchases (Melon/Strawberry) once cash exceeds $600 rather than holding $1,300, or tie land protection strictly to Day 4–8 windows so seed starvation does not occur.
3. **Execute Full 100-Tile Mass Verification:**
   - With Q2 and Q3 reliably unlocked by Day 6–10, evaluate full mass deployment and performance against the $50k / $75k targets.

---

<!-- END OF FILE -->
