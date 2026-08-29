# E11-X1.4 — EPU Densification Before Replication (2×3×5 vs B3 3×3×3)

## Executive Summary

Experiment **E11-X1.4** evaluated whether densifying 2 EPUs to $3 \times 5$ (15 tiles each = 30 tiles total) before activating EPU3 outperforms replicating 3 EPUs at $3 \times 3$ (27 tiles total, B3).

- **Hypothesis A (B3)**: 3 EPUs $\times$ 9 tiles = 27 tiles (4 workers, 1 land purchase).
- **Hypothesis B (X1.4)**: 2 EPUs $\times$ 15 tiles = 30 tiles (3 workers, 1 land purchase).

---

## Head-to-Head Paired Benchmark Results

| Seed | Opponent | B3 Money ($3 \times 9$) | X1.4 Money ($2 \times 15$) | Paired Delta | Head-to-Head Winner |
|---|---|---|---|---|---|
| **0** | `pass` | **$30,234.00** | $22,555.00 | -$7,679.00 | **B3** |
| **100** | `pass` | **$30,072.00** | $28,235.00 | -$1,837.00 | **B3** |
| **200** | `random` | **$31,460.00** | $28,274.00 | -$3,186.00 | **B3** |
| **300** | `random` | $20,014.00 | **$28,474.00** | +$8,460.00 | **X1.4** |
| **400** | `starter` | $20,448.00 | **$28,508.00** | +$8,060.00 | **X1.4** |

---

## Metric Comparison Matrix

| Metric | B3 ($3 \times 9$) | X1.4 ($2 \times 15$) | Comparison |
|---|---|---|---|
| **Mean Money** | $26,445.60 | **$27,209.20** | +$763.60 |
| **Median Money** | **$30,072.00** | $28,274.00 | -$1,798.00 (B3 higher median) |
| **Std Dev** | $5,687.21 | **$2,604.28** | X1.4 has 54% lower variance |
| **Min Money** | $20,014.00 | **$22,555.00** | X1.4 higher downside floor |
| **Max Money (Peak Ceiling)** | **$31,460.00** | $28,508.00 | B3 higher peak revenue |
| **Head-to-Head Wins** | **3 / 5 (60%)** | 2 / 5 (40%) | B3 wins majority of seeds |
| **Target Productive Tiles** | 27 | 30 | X1.4 +3 tiles |
| **Peak Active Workforce** | 4 | 3 | X1.4 saves 1 Hand contract |
| **Provenance Status** | PASS | PASS | Both 100% verified |

---

## Tonight Night-Run Recommendation

- **RECOMMENDATION**: **B3 (`E11-X1.3-B3 Fixed 3x3 3xEPU`)**
- **Rationale**: B3 wins 60% of seeds head-to-head, achieves a higher median ($30,072 vs $28,274) and peak ceiling ($31,460 vs $28,508), and has already been verified 100% semantically equivalent in standalone submission form.
