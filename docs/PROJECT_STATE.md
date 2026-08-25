# Project State

**Last update:** 2026-08-25

## Current phase

E06 completed, reviewed & shipped — Water-First Scheduling (`WaterFirstHIRENWClusterROIAgent`, 9 tiles compact cluster 3x3 with 1 farmer + 1 daily hand at $1/day, priority `WATER > HARVEST > PLANT`). Experimental Hypothesis **SUPPORTED**: Mean Final Money expanded from $21568.93 to **`$24662.00 ± $1932.04`** (+14.34% vs E05, +119.56% vs E04, +67.97% vs E03). Median Final Money reached **`$25847.00`** (+20.54% vs E05). Weed conversions reduced by **`-60.23%`** (176 $\rightarrow$ 70 weeds).

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
- Tag Git E06: `v0.6-e06-water-first` (validazione Water-First scheduling 9 tile, **Mean Money: $24662.00**).
- Modular package structure under `src/agricola/`.
- Strategy `WaterFirstHIRENWClusterROIAgent` in `src/agricola/strategy/water_first_hire_nw_cluster_roi.py` managing 9 tiles with 1 farmer (4 tiles) and 1 hand (5 tiles).
- Entrypoint `src/agricola/agent.py` running `WaterFirstHIRENWClusterROIAgent`.
- Standalone submission bundle `submission/submission.py` updated and verified for E06.
- Unit test suite (`pytest tests/`) 100% passing (**30/30**).
- Dedicated benchmark output isolation: `results/e06_water_first.json`.
- E06 SHIP Report: [`docs/versions/E06_ship_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E06_ship_antigravity.md) (`SHIP PASSED`).

## Experimental Progression

`E01 operational baseline → E02 economic crop selection → E03 production scaling (4 tiles) → E04 NW scaling (9 tiles, single farmer, falsified) → E05 multi-worker HIRE (9 tiles, 2 workers, shipped) → E06 Water-First Scheduling (9 tiles, 2 workers, shipped)`

## Benchmark Metrics Comparison (E01 vs E02 vs E03 vs E04 vs E05 vs E06)

| Metric | E01 Baseline | E02 Evolution | E03 Scaling | E04 NW Scaling | E05 Multi-Worker | E06 Water-First | E05 → E06 Delta |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Strategy** | `CarrotLoopAgent` | `ROICropAgent` | `MultiTileROIAgent` | `NWClusterROIAgent` | `HIRENWClusterROIAgent` | `WaterFirstHIRENWClusterROIAgent` | — |
| **Task Priority** | Statica | Statica | `HARVEST > PLANT > WATER` | `HARVEST > PLANT > WATER` | `HARVEST > PLANT > WATER` | **`WATER > HARVEST > PLANT`** | **Water-First** |
| **Workers** | 1 farmer | 1 farmer | 1 farmer | 1 farmer | 1 farmer + 1 hand | **1 farmer + 1 hand** | — |
| **Footprint** | 1 tile (4,4) | 1 tile (4,4) | 4 tiles (2x2) | 9 tiles (3x3) | 9 tiles (3x3) | **9 tiles (3x3)** | — |
| **Total Episodes** | 30 | 30 | 30 | 30 | 30 | **30** | — |
| **Completion Rate** | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 66.67% | 100.00% | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Mean Final Money** | **$3567.63** | **$5857.17** | **$14682.47** | **$11232.47** | **$21568.93** | **`$24662.00`** | **+$3093.07 (+14.34%)** |
| **Sample Std Dev (`ddof=1`)** | ± $205.38 | ± $132.37 | ± $1164.33 | ± $661.26 | ± $361.25 | **± $1932.04** | — |
| **Median Final Money** | $3528.00 | $5837.00 | $14146.00 | $11050.00 | $21442.00 | **`$25847.00`** | **+$4405.00 (+20.54%)** |
| **Total Weed Conversions** | 0 | 0 | 0 | 238 weeds | 176 weeds | **`70 weeds`** | **-106 (-60.23%)** |
| **Agent Mean Latency** | 0.0142 ms | 0.0267 ms | 0.0698 ms | 0.0570 ms | 0.0924 ms | **`0.0822 ms`** | -0.0102 ms |

## Main Verified Interpretation & Observations of E06

> **E06 valida l'ipotesi che assegnare priorità a WATER rispetto ad HARVEST e PLANT (`WaterFirstHIRENWClusterROIAgent`) elimini oltre il 60% della mortalità delle colture (176 → 70 weed conversions) ed espanda il capitale finale medio a $24662.00 (+14.34% vs E05) e la mediana a $25847.00 (+20.54% vs E05), con un win rate paired del 96.7%.**

## Next step

Avviare la definizione del nuovo esperimento **E07** valutando le candidate emerse dalla REVIEW E06 (es. Candidate A: `DIG` / Weed Recovery per eliminare le 70 erbacce residue).
