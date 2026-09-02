# E14 Codex Structure Audit And Migration Plan

Date: 2026-08-29

## Initial Repository State

- Branch: `main`
- HEAD: `4445aa0 Close E08 productive scale experiment`
- Working tree: dirty before E14 work
- Initial snapshots:
  - `experiments/archive/e14/artifacts/codex/git_status_initial.txt`
  - `experiments/archive/e14/artifacts/codex/git_branch_initial.txt`
  - `experiments/archive/e14/artifacts/codex/git_head_initial.txt`
  - `experiments/archive/e14/artifacts/codex/git_diff_stat_initial.txt`

No reset, clean, stash or revert was performed.

## Codex-Owned Current Assets

- `results/e12/x115_codex/`
- `results/e13/episode_101971376/codex/`
- `scripts/benchmark_e12_x1_15_codex.py`
- `src/agricola/strategy/productive_mass_roi.py` mode `E12_X115_CODEX_INDEPENDENT`

## Shared Infrastructure Allowed

- `src/agricola/core/state.py`
- `src/agricola/core/actions.py`
- `src/agricola/strategy/hybrid_livestock_cluster_roi.py` for shared config/telemetry definitions used by the bundler
- Kaggle `kaggriculture` environment
- Raw replay JSON and replay parser outputs used as evidence

## Contamination Risks Found

- `docs/model_specs/history/MODEL_SPEC_PRE_C2.md` exists as a shared/historical spec path.
- Generic `scripts/build_submission.py` writes `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`, which is not Codex-specific.
- Multiple agent/experiment modes coexist in `src/agricola/strategy/productive_mass_roi.py`.
- Agent-specific prompts and outputs coexist in shared `docs/prompts`, `scripts`, `submission` and `results` namespaces.

These risks are structural. E14 reduces them by adding Codex-specific spec and build paths without editing other-agent files.

## Migration Plan

1. Create `docs/model_specs/codex/` as the Codex-specific current spec home.
2. Add an independent `MODEL_SPEC.md` based only on Codex evidence and replay artifacts.
3. Add a ranked parameter impact table with impact and confidence separated.
4. Add a taxonomy changelog that records added, reformulated, split, deprecated and removed concepts.
5. Add `scripts/build_submission_codex.py` with fixed output `submission_codex.py`.
6. Add isolation tests that confirm the Codex bundle is buildable and contains no other-agent markers.
7. Build `submission_codex.py`, run available relevant tests, run whitespace checks and record final status.

