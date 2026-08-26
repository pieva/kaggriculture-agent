# Project State

**Last update:** 2026-08-26

## Current phase

E08 — Productive Scale Optimization: **E08 COMPLETED & CLOSED** (`E08 FALSIFIED — SHIPPED BASELINE E06 REMAINS ACTIVE`). Documenti di riferimento: [`docs/versions/E08_review_productive_scale.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E08_review_productive_scale.md), [`docs/versions/E08_review_corrections.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E08_review_corrections.md) e [`docs/versions/E08_ship_productive_scale.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E08_ship_productive_scale.md). Baseline Shipped corrente: E06 `WaterFirstHIRENWClusterROIAgent` (`v0.6-e06-water-first`).

## Objective

Develop and evaluate a competitive agent for the Kaggle Kaggriculture
competition using Google Antigravity as the coding agent.

The project is an empirical test of the supervised development method:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

## Repository state

- Tag Git Baseline: `v0.1-e01-baseline`.
- Tag Git E02: `v0.2-e02-roicrop`.
- Tag Git E03: `v0.3-e03-multitile`.
- Tag Git E04: `v0.4-e04-nw-scaling` (falsificazione dell'ipotesi 4→9 single farmer).
- Tag Git E05: `v0.5-e05-hire-multiworker` (validazione dello scaling multi-worker 9 tile, Kaggle Score: 439.7).
- Tag Git E06: `v0.6-e06-water-first` (validazione Water-First scheduling 9 tile, **Mean Money: $25180.30**, shipped baseline attiva).
- E07 Strategy Class: `HybridLivestockClusterROIAgent` in [`src/agricola/strategy/hybrid_livestock_cluster_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/hybrid_livestock_cluster_roi.py) (**ARCHITECTURALLY VALID, ECONOMICALLY WEAK**, Kaggle Score: 339.5).
- E08 Closure Report: [`docs/versions/E08_ship_productive_scale.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E08_ship_productive_scale.md) (**FALSIFIED HYPOTHESIS**, Mean Money: **$11,880.30**, -10.8% vs E07).
- Entrypoint `src/agricola/agent.py` running E06 `WaterFirstHIRENWClusterROIAgent` (E06 shipped baseline attiva).
- Unit test suite (`pytest tests/`) 100% passing (**42/42**).

## Experimental Progression

`E01 operational baseline → E02 economic crop selection → E03 production scaling (4 tiles) → E04 NW scaling (9 tiles, single farmer, falsified) → E05 multi-worker HIRE (9 tiles, 2 workers, shipped) → E06 Water-First Scheduling (shipped) → E07 Competitive Baseline Reconstruction → E08 Productive Scale Optimization (FALSIFIED, CLOSED) → E09 Livestock Subsystem Ablation (NEXT)`

## Benchmark Metrics Comparison (E01 vs E02 vs E03 vs E04 vs E05 vs E06 vs E07 vs E08)

| Metric | E01 Baseline | E02 Evolution | E03 Scaling | E04 NW Scaling | E05 Multi-Worker | E06 Water-First | E07 Competitive | E08 Productive Scale |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Strategy** | `CarrotLoopAgent` | `ROICropAgent` | `MultiTileROIAgent` | `NWClusterROIAgent` | `HIRENWClusterROIAgent` | `WaterFirstHIRENWClusterROIAgent` | `HybridLivestockClusterROIAgent` | `HybridLivestockClusterROIAgent` |
| **Task Priority** | Statica | Statica | `HARVEST > PLANT > WATER` | `HARVEST > PLANT > WATER` | `HARVEST > PLANT > WATER` | **`WATER > HARVEST > PLANT`** | `WATER > FEED > HARVEST > PLANT` | `WATER > FEED > HARVEST > PLANT` |
| **Workers** | 1 farmer | 1 farmer | 1 farmer | 1 farmer | 1 farmer + 1 hand | **1 farmer + 1 hand** | 1 farmer + 3 hands | 1 farmer + 3 hands |
| **Footprint** | 1 tile (4,4) | 1 tile (4,4) | 4 tiles (2x2) | 9 tiles (3x3) | 9 tiles (3x3) | **9 tiles (3x3)** | 50 tiles (24 productive) | 50 tiles (40 productive) |
| **Total Episodes** | 30 | 30 | 30 | 30 | 30 | **30** | 30 | 30 |
| **Completion Rate** | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | **100.00%** | 100.00% | 100.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | **0.00%** | 0.00% | 0.00% |
| **Overall Win Rate** | 66.67% | 100.00% | 100.00% | 100.00% | 100.00% | **100.00%** | 93.33% | 93.33% |
| **Mean Final Money** | **$3567.63** | **$5857.17** | **$14682.47** | **$11232.47** | **$21568.93** | **`$24662.00`** | **$13320.37** | **$11880.30** |
| **Sample Std Dev (`ddof=1`)** | ± $205.38 | ± $132.37 | ± $1164.33 | ± $661.26 | ± $361.25 | **± $1932.04** | ± $6328.16 | ± $6475.07 |
| **Median Final Money** | $3528.00 | $5837.00 | $14146.00 | $11050.00 | $21442.00 | **`$25847.00`** | $10262.00 | $9790.50 |
| **Kaggle Score** | 600.0 | 285.1 | 278.3 | N/A | **429.5** | 375.7 | 339.5 | N/A |

## Next step

Esperimento E08 formalmente chiuso (falsificato). La shipped baseline attiva rimane E06. Iniziare la fase **E09-01 DEFINE — Livestock Subsystem Ablation**: formulazione dell'esperimento di ablazione controllata Livestock `ON` (E07) $\rightarrow$ `OFF` (E09).
