# Project State

**Last update:** 2026-08-25

## Current phase

E05 completed, reviewed & shipped — Multi-Worker Scaling (`HIRENWClusterROIAgent`, 9 tiles compact cluster 3x3 with 1 farmer + 1 daily hand at $1/day). Economic Hypothesis **SUPPORTED**: Mean Final Money expanded from $11232.47 to **$21568.93 ± $361.25** (+92.02% vs E04, +46.90% vs E03). Starvation reduced (-26.05% weed conversions) but unresolved (176 weeds remaining).

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
- Tag Git E05: `v0.5-e05-hire-multiworker` (validazione dello scaling multi-worker 9 tile).
- Modular package structure under `src/agricola/`.
- Strategy `HIRENWClusterROIAgent` in `src/agricola/strategy/hire_nw_cluster_roi.py` managing 9 tiles with 1 farmer (4 tiles) and 1 hand (5 tiles).
- Entrypoint `src/agricola/agent.py` updated to run `HIRENWClusterROIAgent`.
- Standalone submission bundle `submission/submission.py` updated and verified.
- Unit test suite (`pytest tests/`) 100% passing (25/25).
- Benchmark evaluation runner (`src/agricola/evaluation/runner.py`) updated with dedicated output isolation (`results/e05_hire_multiworker.json`).

## Experimental Progression

`E01 operational baseline → E02 economic crop selection → E03 production scaling (4 tiles) → E04 NW scaling (9 tiles, single farmer, falsified) → E05 multi-worker HIRE (9 tiles, 2 workers, shipped)`

## Benchmark Metrics Comparison (E01 vs E02 vs E03 vs E04 vs E05)

| Metric | E01 Baseline (`CarrotLoopAgent`) | E02 Evolution (`ROICropAgent`) | E03 Scaling (`MultiTileROIAgent`) | E04 NW Scaling (`NWClusterROIAgent`) | E05 Multi-Worker (`HIRENWClusterROIAgent`) | E04 → E05 Delta |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Workers** | 1 farmer | 1 farmer | 1 farmer | 1 farmer | **1 farmer + 1 hand ($1/day)** | **+1 worker** |
| **Managed Footprint** | 1 tile (4,4) | 1 tile (4,4) | 4 tiles (2x2) | 9 tiles (3x3) | **9 tiles (3x3)** | — |
| **Total Episodes** | 30 | 30 | 30 | 30 | **30** | — |
| **Completion Rate** | 100.00% | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 66.67% | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Mean Final Money** | **$3567.63** | **$5857.17** | **$14682.47** | **$11232.47** | **`$21568.93`** | **+$10336.46 (+92.02%)** |
| **Sample Std Dev (`ddof=1`)** | ± $205.38 | ± $132.37 | ± $1164.33 | ± $661.26 | **± $361.25** | — |
| **Median Final Money** | $3528.00 | $5837.00 | $14146.00 | $11050.00 | **`$21442.00`** | +$10392.00 |
| **Total Weed Conversions** | 0 | 0 | 0 | 238 weeds | **176 weeds** | **-62 (-26.05%)** |
| **Agent Mean Latency** | 0.0142 ms | 0.0267 ms | 0.0698 ms | 0.0570 ms | **0.0924 ms** | +0.0354 ms |

## Main Verified Interpretation & Observations of E05

> **E05 valida l'ipotesi che l'introduzione di capacità lavorativa subordinata via HIRE ($1/giorno) e coordinata tramite partizionamento spaziale fisso 4:5 sblocchi la produttività economica del cluster a 9 tile, portando il capitale finale a $21568.93 (+92.02% vs E04, +46.90% vs E03). Tuttavia, E05 riduce ma non azzera la water starvation (176 weed conversions residue).**

## Next step

Pianificare l'esperimento E06 a partire dalle candidate direzioni individuate nella REVIEW (es. Candidate A: Water-First Scheduling con HIRE per azzerare le 176 weed residue).
