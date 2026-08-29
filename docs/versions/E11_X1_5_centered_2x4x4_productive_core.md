# E11-X1.5 — Centered 2×4×4 Productive Core

## Executive Summary

Experiment **E11-X1.5** evaluated Hypothesis **H11-X1.5**: two centered, compact $4 \times 4$ EPUs (16 tiles each = 32 tiles total) located immediately around the center/shed boundary between Q0 and Q1.

- **Hypothesis A (B3)**: 3 EPUs $\times$ 9 tiles = 27 tiles (4 workers, 1 land purchase).
- **Hypothesis B (X1.4)**: 2 EPUs $\times$ 15 tiles = 30 tiles (3 workers, 1 land purchase).
- **Hypothesis C (X1.5)**: 2 EPUs $\times$ 16 tiles = 32 tiles (3 workers, 1 land purchase).

---

## 3-Way Paired Benchmark Results

| Seed | Opponent | B3 ($3 \times 9 = 27\text{t}$) | X1.4 ($2 \times 15 = 30\text{t}$) | X1.5 ($2 \times 16 = 32\text{t}$) | Winner |
|---|---|---|---|---|---|
| **0** | `pass` | **$30,234.00** | $22,555.00 | $24,223.00 | **B3** |
| **100** | `pass` | **$30,072.00** | $28,235.00 | $24,154.00 | **B3** |
| **200** | `random` | **$31,460.00** | $28,274.00 | $24,097.00 | **B3** |
| **300** | `random` | $20,014.00 | **$28,474.00** | $24,070.00 | **X1.4** |
| **400** | `starter` | $20,448.00 | $28,508.00 | **$28,601.00** | **X1.5** |

---

## Operational Comparison Matrix

| Metric | B3 ($3 \times 9$) | X1.4 ($2 \times 15$) | X1.5 ($2 \times 16$) | Verdict |
|---|---|---|---|---|
| **Target Tiles** | 27 | 30 | 32 | X1.5 target |
| **Peak Active Tiles** | 27 | **30** | 26 | X1.4 achieved |
| **Mean Final Money** | $26,445.60 | **$27,209.20** | $25,029.00 | X1.4 +$763.60 |
| **Median Final Money** | **$30,072.00** | $28,274.00 | $24,154.00 | B3 highest median |
| **Std Dev** | $5,687.21 | $2,604.28 | **$2,001.35** | X1.5 lowest variance |
| **Min Money** | $20,014.00 | $22,555.00 | **$24,070.00** | X1.5 highest floor |
| **Max Money** | **$31,460.00** | $28,508.00 | $28,601.00 | B3 highest peak |
| **Wins vs B3** | N/A | 2 / 5 (40%) | 2 / 5 (40%) | B3 wins 60% |
| **Wins vs X1.4** | 3 / 5 (60%) | N/A | 1 / 5 (20%) | X1.4 wins 80% vs X1.5 |

---

## Verdict & Recommendation

- **Verdict**: **`X1.5 NOT BETTER`**. EPU2 expansion in Q1 was delayed by seed capital overhead on EPU1's 16 tiles, capping active tiles at 26.
- **TONIGHT RECOMMENDATION**: **`B3 (E11-X1.3-B3 Fixed 3x3 3xEPU)`**. Highest median ($30,072.00), highest peak ceiling ($31,460.00), and 100% verified standalone submission artifact ready.
