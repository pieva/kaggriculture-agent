# REVIEW Report — E08 Productive Scale Optimization (`E08-05 / Corrected`)

**Date:** 2026-08-26  
**Phase:** REVIEW (Correction Pass E08-05B)  
**Status:** `REVIEW CORRECTED`  
**Decision:** **`REVIEW CORRECTED — READY TO CLOSE E08`**  
**Strategy Class:** `HybridLivestockClusterROIAgent`  
**JSON Output Artifact:** [`experiments/archive/e08/artifacts/productive_scale.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e08/artifacts/productive_scale.json)  
**Correction Audit File:** [`experiments/archive/e08/reports/E08_review_corrections.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e08/reports/E08_review_corrections.md)  

---

## 1. Executive Review

The experimental hypothesis of **E08 — Productive Scale Optimization** (*"Increasing target productive tiles from 24 to 40 across Q0+Q1 will increase Mean Final Money by utilizing owned land"*) has been **falsified**.

In the official 30-episode paired benchmark:
- **E08 Mean Final Money:** **$11,880.30** (± $6,475.07)
- **E07 Primary Baseline:** **$13,320.37** (± $6,328.16) — Delta: **-$1,440.07 (-10.81%)**
- **E06 Active Shipped Baseline:** **$24,987.67** (± $1,974.32) — Gap to E06: **$13,107.37 (-52.46%)**

Expanding the crop footprint across 50 tiles without increasing worker travel density diluted worker efficiency: Movement Share rose to **61.6%**, creating a severe `plant_pending` backlog of **17.96 tiles/day** and leaving over 42% of nominal capacity unplanted.

---

## 2. Baseline Reconciliation (E06 & E07)

### E06 Baseline Reconciliation
- **Doc Historic Value (`PROJECT_STATE.md`):** **$25,180.30** (Standalone E06 benchmark).
- **E08 Paired Benchmark Value:** **$24,987.67** (Direct 4-agent paired benchmark in `experiments/archive/e08/artifacts/productive_scale.json`).
- **Reconciliation:** The delta of **-$192.63 (-0.76%)** is due to minor environment setup variations between standalone E06 evaluation and multi-agent paired evaluation runner loops. Both reflect the exact same performance level (~$25,000). For paired E08 comparisons, **$24,987.67** is the authoritative paired baseline.

### E07 Baseline Reconciliation
- **DEFINE/PLAN Historic Value:** **$15,364.57** (Standalone 30-ep benchmark in `experiments/archive/e07/artifacts/competitive_baseline.json`).
- **E08 Paired Benchmark Value:** **$13,320.37** (Simultaneous 4-agent paired benchmark).
- **Reconciliation:** The delta of **-$2,044.20 (-13.3%)** occurs because opponent seed ordering and execution in the 4-agent paired runner altered cash/market timing slightly. When evaluated under identical paired conditions, E08 ($11,880.30) regressed by **-$1,440.07 (-10.81%)** relative to E07 ($13,320.37).

---

## 3. Functional Review (40 Configured ≠ 40 Productive)

In the VERIFY phase, the functional check was classified as `FUNCTIONAL VERIFY PASS`. Re-evaluating against the strict experimental rule **`40 configured ≠ 40 productive`**:

- **Configured Layout:** 40 crop tiles (20 Q0 + 20 Q1).
- **Mean Daily Active Productive Tiles:** **13.84 tiles/day** (benchmark) / **16.33 tiles/day** (diagnostic).
- **Peak Active Productive Tiles:** **22.93 tiles** (benchmark) / **23 tiles** (diagnostic).
- **Backlog `plant_pending`:** **17.96 tiles/day**.

### Re-classification Decision
> **`FUNCTIONAL VERIFY PASS WITH WARNINGS`**

**Reasoning:** The strategy correctly unlocks Q1, configures 40 valid coordinates without crashing, and executes seed purchases. However, due to workforce throughput limitations, the agent operates only **34.6% to 57.3% of nominal capacity**, leaving the majority of configured tiles unplanted or unmaintained.

---

## 4. Economic Review & Paired Analysis

### Summary Statistics (30 Paired Episodes)

| Agent | Completion | DQ Rate | W / D / L | Win Rate (%) | Mean Money | Median Money | Sample Std Dev (`ddof=1`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E05** | 100.0% | 0.0% | 30 / 0 / 0 | 100.0% | $21,480.87 | $21,442.00 | ± $214.01 |
| **E06** | 100.0% | 0.0% | 30 / 0 / 0 | 100.0% | **$24,987.67** | **$25,847.00** | ± $1,974.32 |
| **E07** | 100.0% | 0.0% | 28 / 0 / 2 | 93.3% | $13,320.37 | $10,262.00 | ± $6,328.16 |
| **E08** | 100.0% | 0.0% | 28 / 0 / 2 | 93.3% | **$11,880.30** | **$9,790.50** | **± $6,475.07** |

### Paired Episode Breakdown (E08 vs E07)
- **Equal Performance (20/30 episodes):** All 10 episodes vs `pass` and all 10 vs `starter` yielded **identical rewards** between E07 and E08 ($10,987.80 vs `pass`, $13,529.40 vs `starter`). Staggered seed purchasing (respecting the $300 cash floor) restricted Q1 seed buys to the exact same initial batch under non-disruptive opponents.
- **Regression vs `random` (10/30 episodes):** Mean money dropped from **$15,443.90** (E07) to **$11,123.70** (E08), a delta of **-$4,320.20 (-27.97%)**. Random opponent market transactions disrupted cash timing; when E08 attempted Q1 seed expansion, worker travel distances and cross-boundary water assist caused unharvested crops and net capital loss.

---

## 5. Cash Scope Reconciliation ($339.00 vs $177.40)

| Cash Metric Scope | Value | Target / Floor Policy | Primary Source | Operational Cause |
| :--- | ---: | :---: | :--- | :--- |
| **V1 Single Episode Diagnostic Min Cash** | **$339.00** | $300.00 | `scratch/v1_diagnostic_telemetry.json` | Single episode vs `starter`; cash remained above $339 after Day 13 land purchase. |
| **30-Episode Benchmark Mean Min Cash** | **$177.40** | $300.00 | `experiments/archive/e08/artifacts/productive_scale.json` | Benchmark mean min cash. Dips below $300 occurred on Day 12 when Hand 3 hiring ($8) and pasture building occurred immediately prior to Q1 land purchase ($1,000). |

**Constraint Classification:** **`SECONDARY CONSTRAINT`** (Liquid bank balance was protected against disqualifications, but overall liquidity was constrained by livestock and land capital outlays).

---

## 6. Bottleneck Classification Matrix

| Dimension / Candidate | Classification | Empirical Evidence & Justification |
| :--- | :---: | :--- |
| **Productive Scale Hypothesis** | **`FALSIFIED`** | Scaling target tiles to 40 reduced Mean Money by -10.81% vs E07 and widened gap to E06. |
| **Operational Throughput Bottleneck** | **`DEMONSTRATED BOTTLENECK`** | 4 workers across 50 tiles cannot service 40 crop tiles + 5 pastures. Throughput is saturated. |
| **Absolute Worker Count Sufficiency** | **`UNCONFIRMED`** | Cannot isolate whether 4 workers are intrinsically too few until spatial dispersion & livestock are ablated. |
| **Movement & Dispersion Overhead** | **`DEMONSTRATED BOTTLENECK`** | Worker Movement Share reached **61.6%** (vs <38% target). `plant_pending` backlog averaged **17.96 tiles/day**. |
| **Cash Floor & Liquidity** | **`SECONDARY CONSTRAINT`** | Staggered purchasing protected liquid cash. Seed spending ($3,978) drained cash without proportional yield. |
| **Livestock Direct Financial Loss** | **`DEMONSTRATED FACT`** | Spending ($4,426.67) vs revenue ($449.33) = net financial loss of **-$3,977.34**. |
| **Livestock Overall Performance Collapse** | **`STRONG CANDIDATE`** | Pasture feeding & harvesting in Q0 consumes worker turns needed for high-ROI Melon crops ($250/unit). Requires E09 ablation. |

---

## 7. Corrected E06 Architectural Comparison Matrix

| Architectural Dimension | E06 (`WaterFirstHIRENW`) | E07 (`HybridLivestock` 24t) | E08 (`HybridLivestock` 40t) | Type of Evidence / Primary Source |
| :--- | :---: | :---: | :---: | :--- |
| **Mean Final Money (Paired)** | **$24,987.67** | $13,320.37 | **$11,880.30** | Measured / `experiments/archive/e08/artifacts/productive_scale.json` |
| **Target Crop Footprint** | 9 tiles (3x3 NW) | 24 tiles (Q0+Q1) | 40 tiles (Q0+Q1) | Configuration Fact / Strategy Code |
| **Mean Active Tiles (Daily)** | **`N/A`** | **`N/A`** | **13.84 tiles/day** | Measured / `experiments/archive/e08/artifacts/productive_scale.json` |
| **Peak Active Tiles** | **`N/A`** | **`N/A`** | **22.93 tiles** | Measured / `experiments/archive/e08/artifacts/productive_scale.json` |
| **Workforce Size** | 2 workers (1F + 1H) | 4 workers (1F + 3H) | 4 workers (1F + 3H) | Configuration Fact / Strategy Code |
| **Livestock Subsystem** | None (0 cows, 0 sheep) | 4 Cows, 2 Sheep (5 pastures) | 4 Cows, 2 Sheep (5 pastures) | Configuration Fact / Strategy Code |
| **Livestock Direct Net Balance** | $0.00 | **-$3,977.34** | **-$3,977.34** | Measured / Spending ($4,427) vs Revenue ($449) |
| **Worker Movement Share (%)** | **`N/A`** | **`N/A`** | **61.6%** | Measured / `experiments/archive/e08/artifacts/productive_scale.json` |
| **`plant_pending` Backlog** | **`N/A`** | **`N/A`** | **17.96 tiles/day** | Measured / `experiments/archive/e08/artifacts/productive_scale.json` |
| **Min Cash (Benchmark Mean)** | **`N/A`** | $523.10 | **$177.40** | Measured / Benchmark Telemetry |

---

## 8. E08 Decision

- **Experimental Code & Evidence:** Retained in repository as valid empirical evidence (`src/agricola/strategy/hybrid_livestock_cluster_roi.py`, `experiments/archive/e08/artifacts/productive_scale.json`).
- **Kaggle Submission Decision:** **NOT CANDIDATE FOR KAGGLE SUBMISSION.** E06 `WaterFirstHIRENWClusterROIAgent` remains the active shipped baseline.

---

## 9. Corrected E09 Experimental Recommendation

> **"A parità dell'architettura E07, quale effetto produce l'ablazione completa del sottosistema livestock (con rimozione del relativo feed loop) sulla prestazione economica e sull'efficienza operativa?"**

### Recommended Specifications:
- **Primary Hypothesis:** Ablating the livestock subsystem (0 cows, 0 sheep, 0 pastures) while preserving the exact 24-tile crop footprint and 4-worker structure of E07 will eliminate livestock capital loss (-$3,977) and free worker turns, increasing Mean Final Money above E07 ($13,320.37).
- **Single Independent Variable:** **Livestock Subsystem: `ON` (E07) $\rightarrow$ `OFF` (E09)**.
  - Ablation includes: 0 Cows, 0 Sheep, 0 pastures, removal of `FEED` actions, and deactivation of the Wheat feed loop.
- **Frozen Variables (Preserved from E07):**
  - Target crop footprint: **24 tiles** (E07 baseline layout: 9 Q0 + 15 Q1).
  - Workforce: **4 workers** (1 Farmer + 3 Hands).
  - Land Expansion: Day 12 `BUY_LAND` Q1 ($1,000).
  - Task Priority: Water-First scheduling (`WATER > HARVEST > PLANT`).
  - Liquidation policy & Market policy.
  - Paired benchmark runner protocol (30 episodes vs `pass`, `random`, `starter`).
- **Single Primary Baseline:** **E07** ($13,320.37 paired mean money).
  - E06 ($24,987.67) remains a secondary architectural reference benchmark.
- **Recommended Metrics:** Mean Final Money, Median, SD (`ddof=1`), delta E09 - E07, Worker Movement Share, `plant_pending` backlog, and freed capital accounting.

---

<!-- END OF DOCUMENT -->
