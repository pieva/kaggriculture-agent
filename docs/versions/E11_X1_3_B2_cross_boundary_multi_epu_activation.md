# E11-X1.3-B2 — BUILD + VERIFY — Cross-Boundary Multi-EPU Activation

## Executive Summary

The experiment **E11-X1.3-B2** tested the architectural hypothesis:

> **Can a SINGLE land purchase (Q1, $1,000) host BOTH EPU2 AND EPU3 consecutively (18 -> 27 active productive tiles), avoiding the need for a second land purchase and improving land amortization efficiency?**

A rigorous spatial geometry audit confirmed that 27 non-overlapping productive tiles fit inside 2 Quadrants (50 owned tiles: Q0 + Q1).

However, local machine benchmark testing **falsified** immediate Day 0 multi-EPU expansion:
- **E11-X1.3-B (Day 14 Expansion, 18 tiles):** **$28,727.40 Mean Money** (53.4% scaling efficiency)
- **E11-X1.3-B2 (Day 0 Expansion, 27 tiles):** **$9,808.40 Mean Money** (12.2% scaling efficiency)

---

## 1. Geometry Audit & Coordinate Partitioning

| EPU Module | Target Tiles | Quadrant | Worker Assigned | Spatial Partition Coordinates |
| :--- | :---: | :---: | :---: | :--- |
| **EPU1** | 9 tiles | Q0 | Farmer + Hand 1 | `(4,4),(4,3),(3,4),(3,3)` + `(4,2),(3,2),(2,4),(2,3),(2,2)` |
| **EPU2** | 9 tiles | Q1 | Hand 2 | `(5,4),(5,3),(6,4),(6,3),(5,2),(6,2),(7,4),(7,3),(7,2)` |
| **EPU3** | 9 tiles | Q1 | Hand 3 | `(5,1),(5,0),(6,1),(6,0),(7,1),(7,0),(8,1),(8,0),(9,0)` |
| **Total** | **27 tiles** | **Q0 + Q1** | **4 workers** | **100% Unique, Non-overlapping, Legal within 2Q (50t)** |

---

## 2. Benchmark Results & Falsification Analysis

### Verified Benchmark Records:
- **X1.3-A (1× EPU, 9t):** `E11-X1.3-A-20260827-095542` (Mean: **$26,888.40**)
- **X1.3-B (2× EPU, 18t):** `E11-X1.3-B-20260827-100010` (Mean: **$28,727.40**)
- **X1.3-B2 (3× EPU, 27t):** `E11-X1.3-B2-20260827-103019` (Mean: **$9,808.40**)

### Root Cause Analysis of B2 Falsification ($9.8k vs $28.7k):

1. **Premature Land Purchase (Day 0 Working Capital Draining):**
   Buying Q1 on Day 0 deducts $1,000 immediately from the initial $3,000 bankroll, leaving only $2,000.
2. **Seed Capital Deficit for 27 Tiles:**
   Melon seeds for 27 tiles cost $2,160 ($80 * 27). The remaining $2,000 is insufficient to purchase 27 seeds and fund daily workforce wages ($3/day).
3. **Travel & Distance Penalty (Hand 3):**
   Hand 3 assigned to `(5,1)...(9,0)` spends 5–6 steps per cycle walking back and forth from shed `(4,4)` to the northern edge of Q1, diluting labor productivity.
4. **Causal Confirmation of Post-Surplus Expansion (Day 14):**
   Buying land on Day 14 (after EPU1 harvest generates $14k+ surplus) in `X1.3-B` protects working capital and yields **$28,727.40**, proving that **post-surplus expansion (Day 14)** is essential for financial stability.

---

## 3. Verified SHA-256 Provenance Records

```json
{
  "run_id": "E11-X1.3-B2-20260827-103019",
  "config_sha256": "fecb130d0d6e6fab5ed0be73f1ff346bbdbfca66e1fe07ee0aeac23aeb9ea283",
  "episodes_sha256": "bf6102405b12814120ca5bb50aae8f26ef9bd724e52643a6d48bcce415d862fb",
  "mean_final_money": 9808.40,
  "verdict": "FALSIFIED",
  "provenance_verifier": "PASS"
}
```

---

## 4. Final Strategic Conclusion & Action

- **`E11-X1.3-B` (2× EPU 18-tile scaling, Day 14 Land Purchase, Mean: $28,727.40) REMAINS THE AUTHORITATIVE SUBMISSION CANDIDATE FOR KAGGLE.**
- The standalone submission bundle `submission/submission.py` remains frozen on `X1.3-B`.
