# Project State

**Last update:** 2026-08-19

## Current phase

E01 completed & consolidated — Baseline implemented, verified on Kaggle, and benchmarked (`v0.1-e01-baseline`).

## Objective

Develop and evaluate a competitive agent for the Kaggle Kaggriculture
competition using Google Antigravity as the coding agent.

The project is also an empirical test of the supervised development method:

DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP

## Repository state

- Tag Git: `v0.1-e01-baseline` (main aligned with origin/main).
- Modular package structure created under `src/agricola/`.
- `README.md` updated with installation instructions, Kaggle score, tag reference, and E02 entrypoint.
- Virtual environment `.venv` with Python 3.12 and `kaggle-environments` configured.
- State wrapper (`GameState`) and action builder (`ActionBuilder`) implemented.
- Baseline agent `CarrotLoopAgent` implemented.
- Top-level Kaggle entrypoint (`src/agricola/agent.py`) ready.
- Bundler script (`scripts/build_submission.py`) producing standalone `submission/submission.py`.
- Submission verified on Kaggle platform: Status **`Complete`**, Initial Score **`600.0`**.
- Observable execution trace verified and documented in `docs/versions/E01_verify_antigravity.md`.
- Benchmark evaluation runner (`scripts/run_eval.py`) with exact per-turn agent latency tracking.
- Test suite (`tests/`) distinguishing Unit Tests and Integration Smoke Tests passing 100% (5/5).

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

## Benchmark Metrics (E01 Baseline - 30 Episodes x 720 Steps)

- **Completion Rate**: 100.00% (30/30 episodes completed to turn 720)
- **Disqualification Rate**: 0.00% (0 invalid episode terminations)
- **Overall Win/Draw Rate**: 66.67% Win / 33.33% Draw / 0% Loss (20W / 0L / 10D)
- **Win Rate vs `pass`**: 100.00% (Mean Money: $3594.30)
- **Win Rate vs `random`**: 100.00% (Mean Money: $3610.50)
- **Draw Rate vs `starter`**: 100.00% Draw / 0% Loss (Mean Money: $3531.60)
- **Agent Mean Turn Latency**: 0.0142 ms/turn
- **Simulation Mean Step Duration**: 3.69 ms/step

## Next step

E02 — Dynamic Crop Selection & ROI Scaling (ROICropAgent): Implementation Plan completato e sottoposto a REVIEW; in attesa di approvazione umana prima della fase BUILD.
