# E14 Codex Test And Build Report

Date: 2026-08-29

## Build Output

- Builder: `scripts/build_submission_codex.py`
- Output: `submission_codex.py`
- Output location: repository root
- Candidate mode: `E12_X115_CODEX_INDEPENDENT`
- Candidate variant: `X115D`
- Build result: PASS

## Isolation Checks

- `submission_codex.py` exists at the repository root: PASS
- Output filename is exactly `submission_codex.py`: PASS
- Bundle entrypoint uses Codex mode and variant D: PASS
- Bundle contains no `antigravity` or `copilot` text markers after Codex build filtering: PASS
- Codex MODEL_SPEC lives under `docs/model_specs/codex/`: PASS

## Behavioral Equivalence

- `tests/test_submission_codex_isolation.py`: PASS
- Required seed equivalence for Codex source vs `submission_codex.py`: PASS on seeds `0` and `421521921`

## Available Submission Tests

- `tests/test_submission_behavioral_equivalence.py`: PASS
- `tests/test_submission.py`: PASS
- Combined available submission suite: `4 passed`

## Smoke Run

- `kaggriculture` 24-step smoke run against `submission_codex.py`: PASS
- Final smoke status: `DONE`
- Final smoke reward: `$928`

The smoke command printed unrelated OpenSpiel warnings for unavailable poker games during import, but the Kaggriculture run completed.

## Syntax

- `py_compile` for `scripts/build_submission_codex.py`: PASS
- `py_compile` for `tests/test_submission_codex_isolation.py`: PASS
- `py_compile` for `submission_codex.py`: PASS

## Whitespace

- E14/Codex-created files checked for trailing whitespace: PASS
- Global `git diff --check`: FAIL outside the E14/Codex-created files

Global failures are in already-dirty or generic files such as:

- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`
- `docs/PROJECT_STATE.md`
- `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`

They were not corrected in this pass to avoid collateral edits.

## Warnings

- Pytest emitted a non-blocking cache warning: access denied creating `.pytest_cache` entries.

