# Project State

**Last update:** 2026-08-24

## Current phase

E03 completed & consolidated — Multi-Tile Scaling (`MultiTileROIAgent`) implemented, benchmarked, verified, reviewed, shipped to Kaggle (Status `Complete`, initial observed rating `600.0`). Ready for version tag `v0.3-e03-multitile`.

## Objective

Develop and evaluate a competitive agent for the Kaggle Kaggriculture
competition using Google Antigravity as the coding agent.

The project is an empirical test of the supervised development method:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

## Repository state

- Tag Git Baseline: `v0.1-e01-baseline` (main aligned with origin/main).
- Tag Git E02: `v0.2-e02-roicrop`.
- Tag Git E03: ready for `v0.3-e03-multitile`.
- Modular package structure under `src/agricola/`.
- `README.md` updated with E01 baseline, E02 dynamic crop selection, E03 multi-tile scaling, iteration table, and documentation links.
- Strategy `MultiTileROIAgent` implemented in `src/agricola/strategy/multi_tile_roi.py` managing a 2x2 compact grid cluster `{(4,4), (4,3), (3,4), (3,3)}`.
- Entrypoint `src/agricola/agent.py` updated to run `MultiTileROIAgent`.
- Standalone submission bundle `submission/submission.py` updated, verified, and uploaded to Kaggle (Status `Complete`).
- Unit test suite (`tests/test_actions.py`, `tests/test_multi_tile.py`, `tests/test_roi_crop.py`, `tests/test_baseline.py`, `tests/test_submission.py`) 100% passing (14/14).
- Benchmark evaluation runner (`scripts/run_eval.py`) with per-turn agent latency tracking.
- Evidence files generated and consolidated under `docs/versions/`:
  - `docs/versions/E03_build_antigravity.md`
  - `docs/versions/E03_verify_antigravity.md`
  - `docs/versions/E03_review_antigravity.md`
  - `docs/versions/E03_ship_antigravity.md`

## Experimental Progression

`E01 operational baseline → E02 economic crop selection → E03 production scaling`

## Benchmark Metrics Comparison (E01 vs E02 vs E03)

| Metric | E01 Baseline (`CarrotLoopAgent`) | E02 Evolution (`ROICropAgent`) | E03 Scaling (`MultiTileROIAgent`) | E02 → E03 Delta |
| :--- | :---: | :---: | :---: | :---: |
| **Managed Footprint** | Single tile `(4,4)` | Single tile `(4,4)` | **2x2 Cluster (4 tiles)** | **1 → 4 tiles** |
| **Total Episodes** | 30 | 30 | 30 | — |
| **Completion Rate** | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 66.67% (20W / 0L / 10D) | 100.00% (30W / 0L / 0D) | **100.00% (30W / 0L / 0D)** | 0.00% |
| **Win Rate vs `pass`** | 100.00% ($3594.30) | 100.00% ($5908.50) | **100.00% ($15257.00)** | +$9348.50 |
| **Win Rate vs `random`** | 100.00% ($3577.00) | 100.00% ($5829.00) | **100.00% ($14284.10)** | +$8455.10 |
| **Win Rate vs `starter`** | 0.00% Draw ($3531.60) | 100.00% Win ($5834.00) | **100.00% Win ($14506.30)** | +$8672.30 |
| **Mean Final Money** | **$3567.63** | **$5857.17** | **$14682.47** | **+$8825.30 (+150.68%)** |
| **Sample Std Dev (`ddof=1`)** | ± $205.38 | ± $132.37 | **± $1164.33** | — |
| **Median Final Money** | $3528.00 | $5837.00 | **$14146.00** | **+$8309.00** |
| **Agent Mean Turn Latency** | 0.0142 ms/turn | 0.0267 ms/turn | **0.0698 ms/turn** | +0.0431 ms/turn |
| **Kaggle Platform Status** | Validated (`600.0`) | Complete (`600.0` → `285.1`) | **Complete (`600.0` initial)** | In observation |

> *Note: Local benchmark metrics and Kaggle Skill Rating measure different aspects of the agent and must not be compared directly.*

## Main Verified Interpretation & Observations of E03

> **E03 supporta l'ipotesi che il Multi-Tile Production Scaling incrementi significativamente il throughput e il capitale finale maturato (+150.68%) a parità di logica economica.**

Key verified findings:
1. Managing 4 adjacent tiles `{(4,4), (4,3), (3,4), (3,3)}` scales production output linearly, generating up to +$14,000+ per episode.
2. The directional movement action bug fix (`["NORTH"]`, `["SOUTH"]`, etc.) enabled valid farmer navigation across the grid.
3. The strict spatial priority hierarchy (`HARVEST > PLANT > WATER`) ensures 0 watering starvation and 0 deadlock.
4. Higher variance ($\pm \$1164.33$) reflects right-skewed revenue jumps when partial harvest cycles complete right near step 720.

## Next step

Creazione del commit e del tag Git `v0.3-e03-multitile`. Osservare l'evoluzione del Kaggle Skill Rating per definire la successiva iterazione sperimentale E04.
