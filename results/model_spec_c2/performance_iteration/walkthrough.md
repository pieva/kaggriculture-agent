# C2 Performance Tournament — Walkthrough & Final Results

## Executive Summary

The **C2 Common Performance Tournament** has been orchestrated and audited across all three frozen candidates:
1. **Antigravity C2** (Performance Iteration)
2. **Codex C2 V4** (Performance Iteration)
3. **Copilot C2** (Performance Iteration)

In accordance with the experimental amendment, evaluation was conducted on **3 brand new, independent, frozen seeds** (`1838889274`, `1619968655`, `710418712`).
Across 9 matches (18 player-episodes, 6,480 total steps), completion was 100% with **zero unhandled exceptions or fallbacks**.

The **C2 Performance Objective (> $23,000 Mean Final Money)** was achieved with exceptional margins by **Codex C2 V4** ($31,579.50) and **Antigravity C2** ($27,565.17).

---

## 1. Economic Tournament Ranking

| Rank | Candidate | Record | Mean Final Money | Median Final Money | Std (`ddof=1`) | Min Final Money | Max Final Money | Delta vs Prior C2 ($) | Delta vs Prior C2 (%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Codex C2 V4** | **6W - 0L - 0T** | **$31,579.50** | **$31,130.50** | $3,705.61 | $27,724.00 | $37,165.00 | **+$16,423.50** | **+108.36%** |
| **2** | **Antigravity C2** | **3W - 3L - 0T** | **$27,565.17** | **$27,726.00** | $3,092.40 | $23,545.00 | $30,563.00 | **+$10,894.17** | **+65.35%** |
| **3** | **Copilot C2** | **0W - 6L - 0T** | **$7,823.67** | **$7,742.00** | $287.78 | $7,582.00 | $8.369.00 | **+$3,669.67** | **+88.34%** |

---

## 2. Match Details

### Round 1: Antigravity C2 (P0) vs Codex C2 V4 (P1)
- **Seed 1838889274:** Antigravity P0: **$25,425.00** | Codex P1: **$29,866.00** $\implies$ **Codex C2 V4**
- **Seed 1619968655:** Antigravity P0: **$23,545.00** | Codex P1: **$27,724.00** $\implies$ **Codex C2 V4**
- **Seed 710418712:** Antigravity P0: **$25,494.00** | Codex P1: **$28,110.00** $\implies$ **Codex C2 V4**

### Round 2: Antigravity C2 (P0) vs Copilot C2 (P1)
- **Seed 1838889274:** Antigravity P0: **$29,958.00** | Copilot P1: **$7,621.00** $\implies$ **Antigravity C2**
- **Seed 1619968655:** Antigravity P0: **$30,406.00** | Copilot P1: **$7,741.00** $\implies$ **Antigravity C2**
- **Seed 710418712:** Antigravity P0: **$30,563.00** | Copilot P1: **$8,369.00** $\implies$ **Antigravity C2**

### Round 3: Codex C2 V4 (P0) vs Copilot C2 (P1)
- **Seed 1838889274:** Codex P0: **$37,165.00** | Copilot P1: **$7,743.00** $\implies$ **Codex C2 V4**
- **Seed 1619968655:** Codex P0: **$34,217.00** | Copilot P1: **$7,582.00** $\implies$ **Codex C2 V4**
- **Seed 710418712:** Codex P0: **$32,395.00** | Copilot P1: **$7,886.00** $\implies$ **Codex C2 V4**

---

## 3. Productive Telemetry

| Candidate | Mean Active Surface | Max Active Surface | Mean First Rev Step | Mean WATER | Mean HARVEST | Mean PLANT | Mean DIG | Mean Market Orders |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Codex C2 V4** | 13.66 | 22 | 106.0 | 408.3 | 81.7 | 72.8 | 27.0 | 455.7 |
| **Antigravity C2** | 18.24 | 24 | 265.0 | 578.0 | 81.0 | 70.0 | 23.0 | 287.0 |
| **Copilot C2** | 22.58 | 25 | 73.0 | 887.0 | 350.0 | 353.0 | 3.0 | 463.0 |

---

## 4. Frozen Tournament Artifacts

- [C2_PERFORMANCE_TOURNAMENT_PROTOCOL.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/performance_tournament/C2_PERFORMANCE_TOURNAMENT_PROTOCOL.md)
- [C2_PERFORMANCE_TOURNAMENT_SUMMARY.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/performance_tournament/C2_PERFORMANCE_TOURNAMENT_SUMMARY.md)
- [aggregated_results.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/performance_tournament/aggregated_results.json)
- [aggregated_results.csv](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/performance_tournament/aggregated_results.csv)
- Raw logs: `results/model_spec_c2/performance_tournament/raw/` (9 match folders)
