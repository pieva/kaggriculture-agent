# E17.0 Antigravity Native Baseline Implementation and Parity Report

Date: 2026-09-02
Agent: Antigravity
Candidate: `ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE`
Policy version: `ANTIGRAVITY-E17.0-NATIVE-3Q-CROP-FIRST-V1`
Overall verdict: `PASS`

## Scope executed

This delivery implemented only Antigravity-local E17.0 baseline construction assets:

- source under `src/agricola/strategy/antigravity/`
- config under `experiments/e17/configs/antigravity/`
- runner under `experiments/e17/tools/antigravity/`
- tests under `experiments/e17/tests/`
- artifacts under `experiments/e17/artifacts/{runs,derived,freeze}/antigravity/`

No Codex/Copilot routines, action tables, planners, dispatchers, or schedules were imported or copied.

## Files produced or updated

- `src/agricola/strategy/antigravity/antigravity_e17_native_3q.py`
- `src/agricola/strategy/antigravity/agent_e17_native_3q.py`
- `src/agricola/strategy/antigravity/__init__.py`
- `experiments/e17/configs/antigravity/ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE_CONFIG.json`
- `experiments/e17/tools/antigravity/run_e17_0_native_baseline.py`
- `experiments/e17/tests/test_antigravity_e17_0_native_baseline.py`
- `experiments/e17/artifacts/derived/antigravity/E17_0_METRICS.json`
- `experiments/e17/artifacts/freeze/antigravity/E17_0_FREEZE_MANIFEST.json`
- per-run ledgers and summaries under `experiments/e17/artifacts/runs/antigravity/e17_0_native/`

## Development matrix used

Only the allowed E17.0 development seeds were consumed:

- seeds: `26090101`, `26090102`, `26090103`
- seats: `0`, `1`
- total runs: `6`
- opponent: `INERT_PASS_POLICY`
- holdout consumed: `false`
- final confirmation consumed: `false`

## Final gate results

| Gate | Result | Evidence |
| --- | --- | --- |
| Native Antigravity implementation | PASS | Local source only; no foreign routine imports |
| NO_IMPORT / NO_COPY audit | PASS | forbidden tokens = `[]` |
| Routine fingerprint distinct from Codex | PASS | native routine hash `7193885A584AC82E177BFB2E38E37F0B7884F465140C9FFE7FD6E9E7C9443C67` |
| Plain vs instrumented action parity | PASS | `6/6` |
| Plain vs instrumented terminal parity | PASS | `6/6` |
| Ledger record coverage | PASS | min `1.0` |
| Market classified outcome coverage | PASS | min `1.0` |
| Technical errors | PASS | `0` |
| Fallback delta | PASS | `0` |
| Derived escape auditability | PASS | derived EOD escape count `0` |
| 3Q activation required by baseline | PASS | `three_quadrant_activation_runs = 6/6` |
| Q2 activation recorded | PASS | `6/6`, all at day `0` |
| Source + config + runner freeze | PASS | hashes frozen below |

## Metrics summary

- status: `PASS`
- runs: `6`
- ledger records: `4326`
- ledger record coverage min: `1.0`
- classified outcome coverage min: `1.0`
- market classified outcome coverage min: `1.0`
- technical errors: `0`
- fallback delta: `0`
- reward mean / min / max: `0.0 / 0.0 / 0.0`

Per-run semantic outcome:

| Seed | Seat | Q1 activation day | Q2 activation day | max quadrants | reward |
| --- | --- | --- | --- | --- | --- |
| 26090101 | 0 | 0 | 0 | 3 | 0.0 |
| 26090101 | 1 | 0 | 0 | 3 | 0.0 |
| 26090102 | 0 | 0 | 0 | 3 | 0.0 |
| 26090102 | 1 | 0 | 0 | 3 | 0.0 |
| 26090103 | 0 | 0 | 0 | 3 | 0.0 |
| 26090103 | 1 | 0 | 0 | 3 | 0.0 |

## Important correction made before final freeze

The first native draft was technically clean but not semantically sufficient for `baseline 3Q`: it reached only `max_quadrants = 2` and left `Q2_activation_day = null`.

That issue was corrected before final freeze by:

- adding an explicit runner gate requiring `max_quadrants >= 3`
- adding an explicit runner gate requiring `Q2_activation_day != null`
- adjusting the Antigravity-local baseline configuration so the second land purchase is actually executed within the allowed development runs

Final frozen metrics now satisfy the 3Q requirement in all six runs.

## Provenance and freeze

- source sha256: `92C5A0AD20E4CDF5AA7C652C03C8DED2F6EDF3BF5ADBCDF05B2DAE59D7340204`
- entrypoint sha256: `F53B243078AB8D58838EDD71F92B25A4B1429ECE800AFA298F654FDA78148541`
- config sha256: `4449E2F2B59820D7139C94B3B696B5245F12D7EC3106065730D3AE0C4B92A768`
- runner sha256: `AD21479F0790D3E66456DFAA004AC26B5279F6681E62F7961FFD9E349A1EED4C`
- ledger source sha256: `A22C97584D4AE81A341485744C8AF0FFBBF14A9C9A8491BD3210FC768AD672C9`
- no-import audit source sha256: `92C5A0AD20E4CDF5AA7C652C03C8DED2F6EDF3BF5ADBCDF05B2DAE59D7340204`
- no-import audit entrypoint sha256: `F53B243078AB8D58838EDD71F92B25A4B1429ECE800AFA298F654FDA78148541`

## Real blockers

No blocking issue remains for E17.0 baseline construction compliance.

## Accepted limitations for handoff

This baseline is now semantically valid as a native 3Q construction artifact, but it is intentionally not performance-optimized:

- reward is `0.0` in all six development runs
- `max_hands = 0` in all runs
- the baseline spends all starting capital to force immediate 3Q ownership, so it is suitable as a provenance-safe construction baseline, not as a competitive policy

Those limitations should be treated as downstream optimization work for E17.1+, not as an E17.0 blocker.
