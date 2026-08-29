# E12-X1.15-COPILOT - Final Report

## Candidate

`E12_X115_COPILOT_INDEPENDENT`

## Architecture summary

The candidate adds one Copilot-specific mode to `ProductiveMassROIAgent`. It leaves X1.12's router and implementation unchanged, temporarily derives a livestock capacity envelope from day, owned quadrants, active crops, pasture, animal tiles and cash, delegates the action plan to X1.12 routing, and restores the original configuration after each turn. It does not copy or call the other X1.15 modes.

## Evidence -> hypothesis -> code delta

The six-replay review showed variable workforce and herd sizes, compact and large-footprint winning paths, multi-engine monetization, and Q2 as conditional. X1.14 showed that aggressive Hands or clean-field priority can lower money. The hypothesis was that reducing early livestock commitment while retaining X1.12 routing could release cash without sacrificing the economic engine. The code delta was limited to the new dispatch branch and `_decide_e12_x115_copilot_independent` in `src/agricola/strategy/productive_mass_roi.py`.

## Baseline and development results

Baseline and candidate were executed in the same `kaggle-environments` harness with the canonical `.venv` interpreter, 720 steps per episode.

| Seed | X1.12 | Copilot | Delta | Delta % |
|---:|---:|---:|---:|---:|
| 0 | 42,491 | 37,622 | -4,869 | -11.46% |
| 421521921 | 48,313 | 40,564 | -7,749 | -16.04% |
| 1056561958 | 37,294 | 23,441 | -13,853 | -37.15% |
| 1273000467 | 43,021 | 36,040 | -6,981 | -16.23% |
| **Mean** | **42,779.75** | **34,416.75** | **-8,363.00** | **-19.55%** |
| **Median** | **42,756.00** | **38,831.00** | **-3,925.00** | **-9.18%** |

All episodes ended `DONE`. The candidate regressed on every development seed, so no holdout was run and the candidate was not frozen for upload.

## Behavior

Both policies bought Q1 on Day 12 and did not buy Q2. Candidate peak hands were 9, 10, 9 and 9; mean hands were 6.57, 6.63, 6.60 and 6.57. Candidate peak crop tiles were 26, 29, 25 and 26, slightly above baseline in some seeds, but productive actions and productive-to-movement ratio were lower. Candidate final livestock was consistently `4 Cow / 0 Sheep`, while baseline was `7 Cow / 4 Sheep`. Minimum cash remained approximately 222-223 in both policies.

The measured candidate action totals were:

| Seed | Productive | Movement | Idle | Productive / movement |
|---:|---:|---:|---:|---:|
| 0 | 1,379 | 3,721 | 150 | 0.371 |
| 421521921 | 1,392 | 3,754 | 150 | 0.371 |
| 1056561958 | 1,358 | 3,765 | 150 | 0.361 |
| 1273000467 | 1,372 | 3,728 | 150 | 0.368 |

The runner did not record per-product BUY/SELL ledgers; no economic conclusion about Wheat or individual channels is claimed from this experiment.

## Failure modes

The candidate's lower animal exposure removed Sheep monetization without changing the underlying movement-heavy dispatcher. More crop tiles did not compensate for lost livestock revenue. The experiment therefore falsifies this narrow wrapper hypothesis, not the broader idea of capacity-aware livestock allocation or Q2 as a conditional branch.

## Comparison with prior declared outcomes

The permitted prior outcomes indicate that a failed X1.12 Q2 bolt-on did not activate Q2, while another independent 3Q candidate improved aggregate development and holdout means. This candidate independently confirms that a small state-based livestock wrapper is insufficient; it does not treat either prior outcome as a specification and does not inspect their code or reports.

## Holdout, standalone and gate

Holdout seeds `2026082801`-`2026082804` were not run because development performance failed the robustness gate. No standalone submission was created. Source/submission equivalence was not applicable to this non-uploadable candidate. The focused candidate tests passed: `2 passed in 0.15s`.

The benchmark emitted non-fatal OpenSpiel unknown-game warnings during environment initialization; all measured episodes completed with status `DONE`.

## Files created and modified

Created:

- `results/e12/x115_copilot/IMPLEMENTATION_HYPOTHESIS.md`
- `results/e12/x115_copilot/FINAL_REPORT.md`
- `results/e12/x115_copilot/RESULTS_TABLE.csv`
- `results/e12/x115_copilot/development_results.json`
- `results/e12/x115_copilot/git_status_short.txt`
- `scripts/benchmark_e12_x1_15_copilot.py`
- `tests/test_e12_x1_15_copilot.py`

Modified:

- `src/agricola/strategy/productive_mass_roi.py`: added only the Copilot dispatcher and mode method.

Not modified intentionally:

- `docs/MODEL_SPEC.md`
- `submission/submission.py`
- dependency files and `.venv`
- raw replay JSON
- other agents' X1.15 artifacts

## Contamination and integrity

The shared strategy file already contained other X1.15 modes before this build. They were not used as design sources or copied. No other X1.15 directories, standalone files, implementation hypotheses or reports were read. The initial PowerShell status command returned only a continuation prompt; the later status capture confirmed a pre-existing dirty tree with many unrelated files. No reset, clean, stash, checkout, branch, commit, push, upload or environment mutation was performed.

`X1.15 COPILOT NO ROBUST IMPROVEMENT: DO NOT UPLOAD`
