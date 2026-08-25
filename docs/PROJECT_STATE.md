# Project State

**Last update:** 2026-08-25

## Current phase

E04 completed & reviewed — Initial NW Scaling (`NWClusterROIAgent`, 9 tiles compact cluster 3x3) implemented, benchmarked, verified, and reviewed. Hypothesis **falsified**: Mean Final Money decreased from $14682.47 to $11232.47 (-23.49%) due to 1-farmer physical capacity limits and severe water starvation (238 weed conversions).

## Objective

Develop and evaluate a competitive agent for the Kaggle Kaggriculture
competition using Google Antigravity as the coding agent.

The project is an empirical test of the supervised development method:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

## Repository state

- Tag Git Baseline: `v0.1-e01-baseline` (main aligned with origin/main).
- Tag Git E02: `v0.2-e02-roicrop`.
- Tag Git E03: `v0.3-e03-multitile`.
- Modular package structure under `src/agricola/`.
- Strategy `NWClusterROIAgent` implemented in `src/agricola/strategy/nw_cluster_roi.py` managing a 3x3 compact grid cluster `{(x,y) | x in [2..4], y in [2..4]}`.
- Entrypoint `src/agricola/agent.py` updated to run `NWClusterROIAgent`.
- Standalone submission bundle `submission/submission.py` updated and verified.
- Unit test suite (`tests/test_actions.py`, `tests/test_multi_tile.py`, `tests/test_nw_cluster.py`, `tests/test_roi_crop.py`, `tests/test_baseline.py`, `tests/test_submission.py`) 100% passing (19/19).
- Benchmark evaluation runner (`src/agricola/evaluation/runner.py`) updated with water starvation proxy tracking.

## Experimental Progression

`E01 operational baseline → E02 economic crop selection → E03 production scaling (4 tiles) → E04 NW scaling (9 tiles, falsified)`

## Benchmark Metrics Comparison (E01 vs E02 vs E03 vs E04)

| Metric | E01 Baseline (`CarrotLoopAgent`) | E02 Evolution (`ROICropAgent`) | E03 Scaling (`MultiTileROIAgent`) | E04 NW Scaling (`NWClusterROIAgent`) | E03 → E04 Delta |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Managed Footprint** | Single tile `(4,4)` | Single tile `(4,4)` | 2x2 Cluster (4 tiles) | **3x3 Cluster (9 tiles)** | **4 → 9 tiles** |
| **Total Episodes** | 30 | 30 | 30 | **30** | — |
| **Completion Rate** | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 66.67% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Mean Final Money** | **$3567.63** | **$5857.17** | **$14682.47** | **$11232.47** | **-$3450.00 (-23.49%)** |
| **Sample Std Dev (`ddof=1`)** | ± $205.38 | ± $132.37 | ± $1164.33 | **± $661.26** | — |
| **Median Final Money** | $3528.00 | $5837.00 | $14146.00 | **$11050.00** | -$3096.00 |
| **Total Weed Conversions** | 0 | 0 | 0 | **238 weeds** | **+238 weeds** |
| **Agent Mean Latency** | 0.0142 ms/turn | 0.0267 ms/turn | 0.0698 ms/turn | **0.0570 ms/turn** | -0.0128 ms/turn |

## Main Verified Interpretation & Observations of E04

> **E04 falsifica l'ipotesi che un singolo farmer possa gestire 9 tile mantenendo una produttività agricola superiore. Il limite fisico di lavorazione del singolo farmer è compreso tra 4 e 6 tile. Scalare a 9 tile senza lavoratori aggiuntivi (`HIRE`) o bonifica erbacce (`DIG`) provoca la morte per disidratazione di 6-9 tile per episodio (238 erbacce totali), degradando il capitale finale (-23.49%).**

## Next step

Pianificare l'esperimento E05 per superare il collo di bottiglia lavorativo emerso in E04 mediante l'introduzione della forza lavoro subordinata (`HIRE`) o della bonifica/routing ottimizzato.

