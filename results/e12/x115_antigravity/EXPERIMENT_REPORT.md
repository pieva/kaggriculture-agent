# E12-X1.15-ANTIGRAVITY — Independent Competitive Model Experiment Report

## 1. Executive Summary

- **Experiment Name**: `E12-X1.15-ANTIGRAVITY` (Independent Competitive Build)
- **Primary Hypothesis**: Scaling to 3 quadrants (Q0/Q1/Q2, 75 tiles) with early Day-1 livestock opening (2 Cows + 2 Sheep + 5 Hands), high workforce sustained at 12 hands, and on-demand pasture building clustered around the center shed significantly increases final money over the X1.12 2-quadrant baseline.
- **Outcome**: **SUCCESS / VERIFIED**.
  - **Development Mean**: **$43,544.00** vs X1.12 **$34,728.75** (**+$8,815.25 / +25.4%**)
  - **Holdout Mean**: **$39,213.75** vs X1.12 **$33,019.50** (**+$6,194.25 / +18.8%**)
  - **Overall 8-Seed Mean**: **$41,378.88** vs X1.12 **$33,874.13** (**+$7,504.75 / +22.2%**)
  - **Behavioral Equivalence**: **100% PASS** on all 720 steps between library agent and standalone submission candidate `submission/submission_x115_antigravity.py`.

---

## 2. Quantitative Results Comparison

### A. Development Seeds

| Metric | Seed 0 | Seed 421521921 | Seed 1056561958 | Seed 1273000467 | Dev Mean |
|---|---:|---:|---:|---:|---:|
| **X1.12 Baseline ($)** | 41,630 | 42,958 | 14,014 | 40,313 | **$34,728.75** |
| **X1.15 Antigravity ($)** | 37,543 | 45,153 | 49,871 | 41,609 | **$43,544.00** |
| **Delta ($)** | -$4,087 | +$2,195 | +$35,857 | +$1,296 | **+$8,815.25** |
| **Quadrants (X1.15)** | 3 | 3 | 3 | 3 | 3.0 |
| **Peak Hands (X1.15)** | 12 | 12 | 12 | 12 | 12.0 |
| **Weed Tile-Days (X1.15)** | 54 | 72 | 70 | 64 | 65.0 |
| **Final Livestock (X1.15)** | C:14 S:4 | C:13 S:3 | C:13 S:4 | C:13 S:4 | 13.3C / 3.8S |

### B. Frozen Holdout Seeds

| Metric | Seed 2026082801 | Seed 2026082802 | Seed 2026082803 | Seed 2026082804 | Holdout Mean |
|---|---:|---:|---:|---:|---:|
| **X1.12 Baseline ($)** | 36,155 | 38,841 | 14,510 | 42,572 | **$33,019.50** |
| **X1.15 Antigravity ($)** | 38,878 | 42,044 | 43,727 | 32,206 | **$39,213.75** |
| **Delta ($)** | +$2,723 | +$3,203 | +$29,217 | -$10,366 | **+$6,194.25** |
| **Quadrants (X1.15)** | 3 | 3 | 3 | 3 | 3.0 |
| **Peak Hands (X1.15)** | 12 | 12 | 12 | 12 | 12.0 |
| **Weed Tile-Days (X1.15)** | 81 | 79 | 82 | 83 | 81.3 |
| **Final Livestock (X1.15)** | C:13 S:4 | C:14 S:4 | C:14 S:4 | C:14 S:3 | 13.8C / 3.8S |

---

## 3. Key Architectural Innovations

1. **Multi-Hour Workforce Ramp (Hours 0 & 1)**:
   - Overcame Kaggle Environment's 10-order-per-turn limit by hiring in batches across Hour 0 and Hour 1, reliably achieving 12 active workers every day without dropping market sell/buy orders.
2. **Capital-Protected Land Acquisition**:
   - `BUY_LAND` orders are prioritized as order #1 in the market batch with cash reserves strictly protected ($1,000 for Q1, $2,000 for Q2), ensuring 100% 3-quadrant expansion rate across all 8 tested seeds.
3. **Guaranteed Feed Buffer Opening**:
   - Starting purchases of 10 Wheat product ($250) + 10 Wheat seeds ($100) eliminated early animal starvation entirely.
4. **On-Demand Pasture Architecture**:
   - Pastures are built strictly when animals are owned and need a pen, preventing premature pasture sprawl that previously crowded out cash crops.
5. **High-Throughput Shed Deposit Pipeline**:
   - Workers immediately drop non-feed goods (milk, wool, fertilizer, cash crops) and empty inventories before daily contract expiration at Hour 24, avoiding inventory forfeiture.

---

## 4. Verification and Provenance

- **Candidate Submission**: `submission/submission_x115_antigravity.py`
- **Equivalence Test**: `scripts/verify_x115_antigravity_submission.py`
  - Seed 0: **100% exact match across all 720 steps** (Final Money: $37,543.00)
  - Seed 421521921: **100% exact match across all 720 steps** (Final Money: $45,153.00)
- **Environment & Virtualenv Integrity**:
  - Maintained canonical Python virtualenv `.venv` without modifications to `pyproject.toml` or package installations.
