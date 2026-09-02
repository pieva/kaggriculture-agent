# REVIEW Correction Pass — E08 Productive Scale Optimization (`E08-05B`)

**Date:** 2026-08-26  
**Phase:** REVIEW Correction Pass  
**Status:** `REVIEW CORRECTED`  
**Decision:** **`REVIEW CORRECTED — READY TO CLOSE E08`**  

---

## 1. Executive Summary of Corrections

This document records the four mandatory corrections applied during the **E08-05B REVIEW Correction Pass**:

1. **54.2% Metric Relabeling:** Removed all references conflating `54.2%` with E07 movement share. Correctly relabeled `54.2%` as the DEFINE estimated productive turn load ($\sim 52 \text{ actions} / 96 \text{ turns}$). E07 movement share set to **`N/A`** due to lack of historical step-type telemetry logging.
2. **E06 Metric Audit:** Audited all E06 claims. Replaced unmeasured E06 metrics (`Movement Share`, `Active Tiles`, `Plant Pending Backlog`) with **`N/A`** in architectural comparison tables.
3. **Cash Scope Reconciliation ($339.00 vs $177.40):** Explicitly separated single-episode V1 diagnostic cash ($339.00) from 30-episode benchmark mean minimum cash ($177.40). Clarified that the $300.0 cash reserve floor governed seed and land purchases, while the dip to $177.40 occurred due to pre-existing Day 12 hiring and pasture building logic executed prior to land expansion.
4. **Single-Variable E09 Recommendation:** Rewrote the E09 recommendation as a **pure single-variable livestock ablation experiment** (Livestock `ON` [E07] $\rightarrow$ `OFF` [E09]), freezing all other E07 architectural parameters (24 tiles, 4 workers, Q1 Day 12 land purchase).

---

## 2. Audit & Correction Matrix

| Original Finding / Text | Issue Identified | Verified Source Evidence | Correction Applied |
| :--- | :--- | :--- | :--- |
| **`E07 Movement Share = 54.2% (est)`** | Conflated DEFINE productive workload estimate with movement share | `docs/plans/E08_Productive_Scale_Optimization.md` (52 actions / 96 turns = 54.2% load) | Relabeled 54.2% strictly as productive turn load estimate. Set E07 movement share to **`N/A`**. |
| **`E06 Movement ~32%`**, **`Backlog ~0`**, **`9.0 active tiles`** | Unmeasured intuitive estimates for E06 without telemetry logs | `src/agricola/strategy/water_first_hire_nw_cluster_roi.py` (no step-type or queue logger) | Replaced unmeasured E06 metrics with **`N/A`** in comparison table. Kept 9 tiles as Configuration Fact. |
| **`Min Cash $339` vs `$177.40`** | Scope ambiguity between V1 single episode and 30-ep benchmark | `scratch/v1_diagnostic_telemetry.json` ($339.00) vs `experiments/archive/e08/artifacts/productive_scale.json` ($177.40) | Reconciled scopes explicitly in cash table. Clarified policy: cash floor protected seed/land purchases; $177.40 dip resulted from Day 12 hire/pasture execution. |
| **`Workforce Count = DEMONSTRATED BOTTLENECK`** | Conflated absolute worker count with spatial dispersion & throughput | `experiments/archive/e08/artifacts/productive_scale.json` (61.6% movement share) | Reclassified throughput as **`DEMONSTRATED BOTTLENECK`** and absolute worker count sufficiency as **`UNCONFIRMED`**. |
| **`Livestock = DEMONSTRATED COLLAPSE CAUSE`** | Asserted performance collapse causality prior to ablation testing | `experiments/archive/e08/artifacts/productive_scale.json` ($4,426.67 spending vs $449.33 revenue = -$3,977.34) | Classified direct net loss (-$3,977.34) as **`DEMONSTRATED FACT`** and overall performance collapse causality as **`STRONG CANDIDATE`**. |
| **`E09 Multi-variable Redesign`** (16 tiles, 2-3 workers, Q0 only) | Combined 4+ variable changes simultaneously, preventing causal attribution | Methodological requirement for single-variable ablation | Rewrote E09 as pure single-variable ablation: Livestock `ON` (E07) $\rightarrow$ `OFF` (E09) with 24 tiles and 4 workers frozen. |

---

## 3. Cash Scope Reconciliation

| Cash Metric Scope | Value | Target / Floor Policy | Primary Source | Operational Cause |
| :--- | ---: | :---: | :--- | :--- |
| **V1 Single Episode Diagnostic Min Cash** | **$339.00** | $300.00 | `scratch/v1_diagnostic_telemetry.json` | Controlled single episode vs `starter`; cash remained above $339 after Day 13 land purchase. |
| **30-Episode Benchmark Mean Min Cash** | **$177.40** | $300.00 | `experiments/archive/e08/artifacts/productive_scale.json` | Mean minimum cash across 30 episodes. Dips below $300 occurred on Day 12 when Hand 3 hiring ($8) and pasture building occurred immediately prior to Q1 land purchase ($1,000). |

### Cash Policy Clarification:
The `$300.0` cash reserve floor in E08 was explicitly applied as a guard condition for **staggered seed purchasing** (`cash - seed_cost >= 300.0`) and land expansion (`cash - 1000.0 >= 300.0`). Staggered seed purchasing strictly respected this floor and prevented seed buys whenever cash dropped near $300. The dip to $177.40 was caused by pre-existing E07 workforce hiring and pasture placement actions, NOT by E08 seed purchasing logic.

**Constraint Classification:** **`SECONDARY CONSTRAINT`** (Liquid bank balance was protected against disqualifications, but overall liquidity was constrained by livestock and land capital outlays).

---

## 4. Corrected Architectural Comparison Table (E06 / E07 / E08)

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

## 5. Corrected E09 Experimental Recommendation

> **"A parità dell'architettura E07, quale effetto produce l'ablazione completa del sottosistema livestock (con rimozione del relativo feed loop) sulla prestazione economica e sull'efficienza operativa?"**

### Recommended Specifications:
- **Primary Hypothesis:** Ablating the livestock subsystem (0 cows, 0 sheep, 0 pastures) while preserving the exact 24-tile crop footprint and 4-worker structure of E07 will eliminate livestock capital loss (-$3,977) and free worker turns, increasing Mean Final Money above E07 ($13,320.37).
- **Single Independent Variable:** **Livestock Subsystem: `ON` (E07) $\rightarrow$ `OFF` (E09)**.
  - Ablation includes: 0 Cows, 0 Sheep, 0 pastures, removal of `FEED` actions, and deactivation of the Wheat feed loop (Wheat planted as regular crop or ablated).
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
