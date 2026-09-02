# VERIFY Report — E09-01 Local Performance Benchmark

**Date:** 2026-08-26  
**Phase:** E09-04 VERIFY  
**Status:** `VERIFY COMPLETED — EXPERIMENTAL HYPOTHESIS CONFIRMED`  
**Decision:** **`READY FOR E09-05 REVIEW`**  
**Dataset Artifact:** [`experiments/archive/e09/artifacts/livestock_ablation.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e09/artifacts/livestock_ablation.json)  
**Primary Baseline:** E08 (`HybridLivestockClusterROIAgent`, 40 tiles, Livestock ON)  
**Treatment:** E09-01 (`LivestockAblationROIAgent`, 40 tiles, Livestock OFF)  
**Secondary Historical Reference:** E07 (`HybridLivestockClusterROIAgent`, 24 tiles, Livestock ON)  

---

## 1. Executive Summary

The **VERIFY** phase for **E09-01 — Livestock Subsystem Ablation** evaluated 30 paired episodes for five agent variants (`E05`, `E06`, `E07`, `E08`, `E09_01`) across identical seeds against standard opponents (`pass`, `random`, `starter`).

The experimental hypothesis is **DECISIVELY CONFIRMED**:

> **Removing the livestock subsystem from the 40-tile E08 configuration doubles mean final money ($22,899.20 vs $11,468.53, +99.67%), increases median money to $27,672.00 (+176.9%), restores win rate to 100.0%, and beats E08 in 26 out of 30 paired episodes (86.7%).**

---

## 2. Benchmark Summary Metrics (30 Paired Episodes per Agent)

| Metric | E05 Multi-Worker | E06 Water-First (Shipped) | E07 Competitive Ref | E08 Productive Scale | E09-01 Livestock Ablation |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Strategy Class** | `HIRENWCluster` | `WaterFirstHIRENWCluster` | `HybridLivestockCluster` | `HybridLivestockCluster` | **`LivestockAblationROI`** |
| **Footprint** | 9 tiles (3x3) | 9 tiles (3x3) | 24 tiles (9 Q0 + 15 Q1) | 40 tiles (20 Q0 + 20 Q1) | **40 tiles (20 Q0 + 20 Q1)** |
| **Livestock Subsystem** | OFF | OFF | ON | ON | **OFF** |
| **Total Episodes** | 30 | 30 | 30 | 30 | **30** |
| **Completion Rate** | 100.0% | 100.0% | 100.0% | 100.0% | **100.0%** |
| **Disqualification Rate** | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| **W / D / L** | 30 / 0 / 0 | 30 / 0 / 0 | 28 / 0 / 2 | 27 / 0 / 3 | **30 / 0 / 0** |
| **Win Rate** | 100.0% | 100.0% | 93.3% | 90.0% | **100.0%** |
| **Mean Final Money** | $21,495.87 | $24,731.37 | $12,578.73 | $11,468.53 | **`$22,899.20`** |
| **Std Dev (`ddof=1`)** | ± $212.45 | ± $1,859.19 | ± $6,141.92 | ± $6,643.06 | **± $7,892.99** |
| **Median Final Money** | $21,442.00 | $25,847.00 | $10,164.00 | $9,994.00 | **`$27,672.00`** |
| **Min / Max Money** | $21,282 / $22,568 | $22,180 / $27,873 | $89 / $22,784 | $89 / $22,784 | **$5,788 / $28,408** |
| **Mean Weed Count** | 5.90 | 2.17 | 19.53 | 20.87 | **18.90** |
| **Mean Latency (ms)** | 0.098 ms | 0.096 ms | 0.346 ms | 0.338 ms | **0.187 ms** |

---

## 3. Causal Delta & Paired Comparisons

### A. Primary Causal Delta (E09-01 vs E08 Primary Baseline)
- **Mean Final Money Delta ($\Delta_{\text{causal}}$):** **`+$11,430.67` (+99.67% increase)**
- **Median Money Delta:** **`+$17,678.00` (+176.89% increase)**
- **Paired Head-to-Head (30 episodes):**
  - **E09-01 Better:** **26 / 30 episodes (86.7%)**
  - **Equal:** 0 / 30 episodes
  - **E08 Better:** 4 / 30 episodes (13.3%)
  - **Mean Paired Difference:** +$11,430.67 (SD ± $10,087.74)
  - **Median Paired Difference:** +$13,078.50

### B. Secondary Reference Delta (E09-01 vs E07 Secondary Baseline)
- **Mean Final Money Delta ($\Delta_{\text{sec}}$):** **`+$10,320.47` (+82.05% increase vs E07 $12,578.73)**
- **Median Money Delta:** **`+$17,508.00` (+172.26% increase vs E07 $10,164.00)**
- **Paired Head-to-Head (30 episodes):**
  - **E09-01 Better:** **26 / 30 episodes (86.7%)**

### C. Comparison with E06 Shipped Baseline ($24,731.37)
- **Mean Delta vs E06:** -$1,832.17 (-7.41%)
- **Median Delta vs E06:** **+$1,825.00** ($27,672.00 vs $25,847.00 — E09-01 median is **higher** than E06!)
- **Paired Head-to-Head vs E06:** E09-01 outperforms E06 in **21 out of 30 episodes (70.0%)**, though exhibiting higher variance due to 40-tile crop density.

---

## 4. Opponent Performance Breakdown

| Opponent | Metric | E05 | E06 (Shipped) | E07 | E08 | E09-01 (Treatment) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **vs `pass`** | Win Rate | 100.0% | 100.0% | 90.0% | 90.0% | **100.0%** |
| (10 eps) | Mean Money | $21,554.60 | $24,593.30 | $10,987.80 | $10,987.80 | **`$23,040.90`** |
| | Median Money | $21,442.00 | $25,847.00 | $9,790.50 | $9,790.50 | **`$27,672.00`** |
| **vs `random`** | Win Rate | 100.0% | 100.0% | 100.0% | 90.0% | **100.0%** |
| (10 eps) | Mean Money | $21,477.00 | $24,780.50 | $13,219.00 | $9,888.40 | **`$21,724.50`** |
| | Median Money | $21,442.00 | $25,847.00 | $10,492.00 | $9,948.50 | **`$27,507.00`** |
| **vs `starter`** | Win Rate | 100.0% | 100.0% | 90.0% | 90.0% | **100.0%** |
| (10 eps) | Mean Money | $21,456.00 | $24,820.30 | $13,529.40 | $13,529.40 | **`$23,932.20`** |
| | Median Money | $21,442.00 | $25,847.00 | $14,648.00 | $14,648.00 | **`$27,729.50`** |

---

## 5. Diagnostic Telemetry & Mechanism Analysis

Comparing E08 (Livestock ON) vs E09-01 (Livestock OFF):

| Diagnostic Metric | E08 Baseline (Livestock ON) | E09-01 Treatment (Livestock OFF) | Delta / Shift Mechanism |
| :--- | :---: | :---: | :--- |
| **Livestock Spending** | $900.00 / ep | **$0.00 / ep** | **+$900.00 liquid cash saved** |
| **Pastures & Feed Actions** | 5 pastures, 18 feed actions | **0 pastures, 0 feed actions** | **18 worker actions redirected to crop watering/harvesting** |
| **Wheat Economy** | 18 Wheat fed to animals | **0 Wheat fed (all sold at market)** | **+$450.00 additional market revenue from Wheat** |
| **Realized Revenue (Livestock)** | -$3,977.34 Net Loss | **$0.00 (Zero loss)** | **+$3,977.34 net profit recovery from livestock elimination** |
| **Realized Revenue (Melon)** | $12,416.67 / ep | **$24,683.33 / ep** | **+$12,266.66 (+98.8%) Melon sales revenue boost!** |
| **Seed Spending** | $2,420.00 / ep | **$4,568.00 / ep** | **+$2,148.00 reinvested into Melon & Carrot seeds** |
| **Mean Movement Share** | 61.6% movement | **60.7% movement** | Reduced worker movement friction |
| **Mean Plant Pending Backlog** | 17.96 tiles/day | **16.07 tiles/day** | -1.89 tiles/day backlog reduction |
| **Mean Daily Active Tiles** | ~13.1 tiles/day | **15.89 tiles/day** | **+2.79 active tiles/day operational scale increase** |

---

## 6. Evaluation Against Decision Criteria

The experimental decision criterion established in E09 DEFINE was:

1. **Conclusion A (Livestock is a Structural Value Sink in E08 Config):** E09-01 significantly outperforms E08 ($\Delta_{\text{causal}} > +\$1,500$, paired win rate $> 60\%$).
2. **Conclusion B (Livestock is Value-Additive):** E09-01 significantly degrades vs E08 ($\Delta_{\text{causal}} < -\$1,000$).
3. **Conclusion C (Inconclusive):** Delta is marginal ($-\$1,000 \le \Delta \le +\$1,500$).

### Decision:
**`CONCLUSION A CONFIRMED — LIVESTOCK IS A STRUCTURAL VALUE SINK IN E08 CONFIGURATION`**

- $\Delta_{\text{causal}} = +\$11,430.67$ (vastly exceeds $+\$1,500$ threshold).
- Paired Win Rate = **86.7%** (26/30 episodes, vastly exceeds $60\%$ threshold).
- Median Money = **$27,672.00** (+176.9% vs E08 $9,994.00).

---

<!-- END OF DOCUMENT -->
