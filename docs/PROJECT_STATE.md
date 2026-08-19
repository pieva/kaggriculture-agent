# Project State

**Last update:** 2026-08-19

## Current phase

E02 completed & reviewed — Dynamic Crop Selection & ROI Scaling (`ROICropAgent`) implemented, verified, reviewed, and documentally consolidated. Awaiting human approval for SHIP (Kaggle submission & version tagging).

## Objective

Develop and evaluate a competitive agent for the Kaggle Kaggriculture
competition using Google Antigravity as the coding agent.

The project is also an empirical test of the supervised development method:

DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP

## Repository state

- Tag Git Baseline: `v0.1-e01-baseline` (main aligned with origin/main).
- Modular package structure under `src/agricola/`.
- `README.md` updated with E01 baseline, Kaggle score 600.0, and E02 entrypoint.
- Virtual environment `.venv` with Python 3.12 and `kaggle-environments`.
- Strategy `ROICropAgent` implemented in `src/agricola/strategy/roi_crop.py`.
- Entrypoint `src/agricola/agent.py` updated to run `ROICropAgent`.
- Standalone submission bundle `submission/submission.py` updated and verified.
- Unit tests (`tests/test_roi_crop.py`) added; full test suite 100% passing (7/7).
- Benchmark evaluation runner (`scripts/run_eval.py`) with per-turn agent latency tracking.
- Evidence files generated and consolidated under `docs/versions/`:
  - `docs/versions/E02_build_antigravity.md`
  - `docs/versions/E02_verify_review_antigravity.md`
  - `docs/versions/E02_simulation_analysis.md`

## Verified E01 Baseline Operational Cycle

`BUY_SEED → PLANT → WATER → PASS → HARVEST → PLANT → SELL`

Key observations from E01 VERIFY trace:
1. Farmer remains immobile on initial tile `(4, 4)`.
2. Uses exclusively `CARROT` crop.
3. Next cycle's seed is pre-purchased as a buffer (`seeds == 0` triggers `BUY_SEED`).
4. `farmer` and `market` actions operate as independent channels in the same turn.
5. Watering increases crop yield (`yield_units = 2`).
6. Harvested crops are sold immediately upon availability in `shed`.
7. Seed cost and crop selling price are distinct economic variables: seed cost is defined statically by the crop configuration, while selling price is exposed dynamically by the market.
8. Rich `GameState` fields (grid map, opponent state, other crops, dynamic market prices) remain unexploited.

## Benchmark Metrics Comparison (E01 Baseline vs E02 ROICropAgent)

| Metric | E01 Baseline (`CarrotLoopAgent`) | E02 Evolution (`ROICropAgent`) | Change / Delta |
| :--- | :---: | :---: | :---: |
| **Total Episodes** | 30 | 30 | — |
| **Completion Rate** | 100.00% | 100.00% | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% |
| **Overall Win Rate** | 66.67% (20W / 0L / 10D) | **100.00%** (30W / 0L / 0D) | **+33.33%** |
| **Win Rate vs `pass`** | 100.00% ($3594.30) | 100.00% ($5908.50) | +$2314.20 |
| **Win Rate vs `random`** | 100.00% ($3577.00) | 100.00% ($5829.00) | +$2252.00 |
| **Win Rate vs `starter`** | 0.00% Draw (10D / $3531.60) | **100.00% Win** (10W / $5834.00) | **0% → 100% Win** |
| **Mean Final Money** | **$3567.63** | **$5857.17** | **+$2289.53 (+64.18%)** |
| **Sample Std Dev (`ddof=1`)** | **± $205.38** | **± $132.37** | — |
| **Population Std Dev (`ddof=0`)**| ± $201.93 | ± $130.14 | — |
| **Median Final Money** | $3528.00 | $5837.00 | +$2309.00 |
| **Agent Mean Turn Latency** | 0.0142 ms/turn | 0.0267 ms/turn | +0.0125 ms/turn |
| **Simulation Step Time** | 3.69 ms/step | 3.45 ms/step | -0.24 ms/step |

## Main Verified Interpretation of E02

> **E02 migliora principalmente perché la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.**

Key verified findings:
1. `MELON` is Rank 1 under both the implemented `Yield=2` model and the environment's `max_yield = 6` watered yield.
2. Completed sales cycles in the 720-step simulation are 100% `MELON`, generating over +$1600 gross revenue per harvest on tile `(4, 4)` vs +$140 for `CARROT`.
3. Late in the season (Day 21), l'agente selects `STRAWBERRY` as its ROI rises above `MELON`.
4. E02 limits identified: End-of-Season Horizon (unharvested late crops), Single-Tile Limitation `(4, 4)`, Immediate Selling (no market sell timing), and Yield Model Simplification (`Yield=2`).

## Next step

E02 — SHIP: submission Kaggle reale, verifica del risultato esterno e successivo tag di versione (`v0.2-e02-roicrop`).
