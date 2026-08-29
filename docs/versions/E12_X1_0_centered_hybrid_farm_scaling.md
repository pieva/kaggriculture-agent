# E12-X1.0 — Centered Hybrid Farm Scaling (Cow-First + Progressive 2×2 Core)

## Executive Summary

Experiment **E12-X1.0** evaluated Hypothesis **H12**: constructing a cow-first hybrid farm with a reserved 2×2 livestock core `[(3,3), (3,4), (4,3), (4,4)]` adjacent to the origin `(4,4)` and scaling crop production around the core.

---

## 5-Way Paired Benchmark Results

| Seed | Opponent | B3 ($27\text{t}$) | X1.6 ($32\text{t}$) | **E11-X1.7 (Corner-Pruned 26t)** | **E12-X1.0 (Cow-First Hybrid)** | **Winner** |
|---|---|---|---|---|---|---|
| **0** | `pass` | **$30,234.00** | $29,297.00 | $30,220.00 | $110.00 | **B3** |
| **100** | `pass` | $30,072.00 | $29,095.00 | **$30,081.00** | $11,118.00 | **X1.7** |
| **200** | `random` | $31,460.00 | **$34,634.00** | $33,371.00 | $4,056.00 | **X1.6** |
| **300** | `random` | $20,014.00 | $22,318.00 | **$23,391.00** | $4,636.00 | **X1.7** |
| **400** | `starter` | $20,448.00 | $22,197.00 | **$23,356.00** | $11,218.00 | **X1.7** |

---

## Operational & Statistical Comparison

| Metric | B3 ($3 \times 9 = 27\text{t}$) | X1.6 ($2 \times 16 = 32\text{t}$) | **E11-X1.7 (Corner-Pruned 26t)** | **E12-X1.0 (Cow-First Hybrid)** | **Best Candidate** |
|---|---|---|---|---|---|
| **Mean Final Money** | $26,445.60 | $27,508.20 | **$28,083.80** | $6,227.60 | **E11-X1.7 (CHAMPION)** |
| **Median Final Money** | $30,072.00 | $29,095.00 | **$30,081.00** | $4,636.00 | **E11-X1.7 (CHAMPION)** |
| **Standard Deviation** | $5,687.21 | $5,078.68 | **$4,064.03** | $4,917.43 | E11-X1.7 |
| **Minimum Money (Floor)** | $20,014.00 | $22,197.00 | **$23,356.00** | $110.00 | E11-X1.7 |
| **Maximum Money (Ceiling)** | $31,460.00 | **$34,634.00** | $33,371.00 | $11,218.00 | X1.6 |
| **Active Pastures** | 0 | 0 | 0 | **4 Pastures** | E12-X1.0 |
| **Active Cows Placed** | 0 | 0 | 0 | **4 Active Cows** | E12-X1.0 |
| **Milk Harvested** | 0 | 0 | 0 | **0 Units** | Feed Loop Bottleneck |
| **Provenance Verdict** | **`PASS`** | **`PASS`** | **`PASS`** | **`PASS (100% Match)`** | SHA-256 verified |

---

## Key Diagnostics & Next Steps

1. **Structural Success**: 2×2 livestock core reservation and progressive pasture construction worked 100% properly (4 pastures built, 4 cows placed).
2. **Bottleneck Identified**: WHEAT crops were planted, but WHEAT was not harvested into shed in time for workers to perform `PICKUP WHEAT` $\to$ `FEED`, resulting in 0 MILK yield.
3. **Current Active Candidate**: **`E11-X1.7 Corner-Pruned Center-Out 26t`** remains the **CHAMPION SUBMISSION CANDIDATE** ($28,083.80 Mean, $30,081.00 Median) and is loaded in `submission/submission.py`.
