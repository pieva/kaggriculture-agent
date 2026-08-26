# VERIFY Report — E08 Performance Verification (`E08-04 / V2`)

**Date:** 2026-08-26  
**Phase:** VERIFY (Phase V2 — Performance Verification)  
**Status:** `VERIFY COMPLETED`  
**Decision:** **`VERIFY FAIL — SUPERVISION REQUIRED`**  
**Strategy Class:** `HybridLivestockClusterROIAgent`  
**JSON Output Artifact:** [`results/e08_productive_scale.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e08_productive_scale.json)  

---

## 1. Benchmark Protocol & Setup (V2.1)

The local performance benchmark was executed using the official paired 30-episode protocol:

- **Episodes:** 30 paired episodes per agent (10 vs `pass`, 10 vs `random`, 10 vs `starter`).
- **Positioning:** 15 episodes as Player 0 (P0), 15 episodes as Player 1 (P1).
- **Random Seeds:** Identical paired seeds (`seed = episode_idx * 100`) for all agents.
- **Agents Benchmarked:**
  1. `E05`: `HIRENWClusterROIAgent` (E05 Shipped 9-tile multi-worker baseline)
  2. `E06`: `WaterFirstHIRENWClusterROIAgent` (E06 Shipped active baseline)
  3. `E07`: `HybridLivestockClusterROIAgent (24 tiles)` (E07 Primary Baseline)
  4. `E08`: `HybridLivestockClusterROIAgent (40 tiles)` (E08 Productive Scale Optimization candidate)

---

## 2. Aggregate Performance Results (V2.2)

| Agent | Completion Rate | Disqualification | Win / Draw / Loss | Win Rate (%) | Mean Final Money | Median Final Money | Std Dev (`ddof=1`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E05** | 100.0% | 0.0% | 30 / 0 / 0 | 100.0% | $21,480.87 | $21,442.00 | ± $214.01 |
| **E06** | 100.0% | 0.0% | 30 / 0 / 0 | 100.0% | **$24,987.67** | **$25,847.00** | ± $1,974.32 |
| **E07** | 100.0% | 0.0% | 28 / 0 / 2 | 93.3% | $13,320.37 | $10,262.00 | ± $6,328.16 |
| **E08** | 100.0% | 0.0% | 28 / 0 / 2 | 93.3% | **$11,880.30** | **$9,790.50** | **± $6,475.07** |

---

## 3. Comparative Deltas & Gap Analysis (V2.2)

### E08 vs E07 (Primary Baseline Comparison)
- **Mean Money Delta:** **-$1,440.07 (-10.81%)** ($11,880.30 vs $13,320.37)
- **Median Money Delta:** **-$471.50 (-4.59%)** ($9,790.50 vs $10,262.00)
- **Paired Win Rate:** **4 / 30 episodes better (13.3%)**, 20 equal (66.7%), 6 worse (20.0%).

### E08 vs E06 (Secondary Gap Recovery Reference)
- **Mean Money Delta:** **-$13,107.37 (-52.46%)** vs E06 ($24,987.67)
- **Remaining Gap to E06:** **$13,107.37**
- **Gap Recovered vs E07:** **-12.34%** (Scaling to 40 tiles expanded the economic performance gap rather than closing it).

---

## 4. Opponent Breakdown (V2.3)

| Opponent | E08 Mean Money | E07 Mean Money | Absolute Delta | Pct Delta (%) | E08 Win Rate (%) | E07 Win Rate (%) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **`pass`** | $10,987.80 | $10,987.80 | $0.00 | 0.00% | 90.0% | 90.0% |
| **`random`** | $11,123.70 | $15,443.90 | -$4,320.20 | -27.97% | 100.0% | 100.0% |
| **`starter`** | $13,529.40 | $13,529.40 | $0.00 | 0.00% | 90.0% | 90.0% |

The performance regression occurred specifically during dynamic opponent interactions (`random`), where worker travel distance and seed cost cash drains degraded overall liquidity management.

---

## 5. Operational Bottleneck & Telemetry Diagnostic (V3)

```text
40 Configured Tiles -> 22.93 Peak Active -> 13.84 Mean Daily -> $11,880.30 Final Money
```

Analysis of E08 telemetry metrics reveals the core root causes of the economic failure:

1. **Under-utilization of Configured Capacity:**
   - While 40 tiles were configured, the mean daily productive tiles reached only **13.84 tiles/day** (peak 22.93 tiles). Over **50% of nominal capacity was left unplanted**.
2. **Severe Movement Overhead & Spatial Bottleneck:**
   - Worker Movement Share reached **61.6%** (1,234 movement steps out of 2,002 total steps), failing the diagnostic target of `<38%`. Workers spend over 60% of their turns traveling across the 50-tile grid.
3. **Severe Planting Backlog (`plant_pending`):**
   - `mean_plant_pending` backlog averaged **17.96 tiles/day**. Workers are consumed by watering and travelling, creating a massive queue of unplanted crop tiles.
4. **Capital Drain from Sementi:**
   - Seed spending reached **$3,978.00**, but generated only **$12,000.00** in Melon revenue due to unharvested or delayed crop cycles.
   - Cash minimum dropped to **$177.40**, restricting timely worker hiring or expansion flexibility.

---

## 6. Outlier & Stability Analysis (V2.4)

- **Disqualifications:** 0/30 (0.0%).
- **Completion:** 30/30 (100.0%).
- **Low-reward Outliers:** Seed 600 vs `pass` ($132.00 in E07 & E08) and Seed 600 vs `random` ($197.00 in E08) due to early-game crop loss or market timing lock.

---

## 7. VERIFY Decision

> **`VERIFY FAIL — SUPERVISION REQUIRED`**

The experimental hypothesis of E08 (*"Increasing target productive scale from 24 to 40 tiles will increase Mean Final Money"*) has been **falsified**. Scaling tile footprint without increasing workforce density or optimizing tile locality degraded economic performance by **-10.81%** vs E07 and widened the gap to E06.

---

<!-- END OF DOCUMENT -->
