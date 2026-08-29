# E14 Codex Isolation Report

Date: 2026-08-29

## Eliminated For Codex Current Workflow

- Current Codex model spec no longer points at shared `docs/MODEL_SPEC.md`.
- Codex candidate build no longer uses generic `submission/submission.py`.
- Codex build output is fixed to root-level `submission_codex.py`.
- Codex evidence backfill is stored under `results/e14/codex/`.

## Intentionally Shared Dependencies

- Core game state wrapper.
- Action builder.
- ProductiveMassROIAgent implementation file, selected by Codex mode.
- Shared telemetry/config definitions needed by the standalone bundler.
- Raw benchmark/replay data and Codex-owned parsed evidence.

## Known Remaining Coupling

- Strategy implementation still lives in the large shared `productive_mass_roi.py` file.
- The repository contains other-agent scripts and submissions in shared directories.
- Generic README and historical docs may still mention `docs/MODEL_SPEC.md` and generic submission paths.

These are not edited in this pass to avoid overwriting concurrent or historical work.

