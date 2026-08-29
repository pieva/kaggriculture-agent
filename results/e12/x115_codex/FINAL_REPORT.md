# E12-X1.15 Codex Independent Competitive Build Final Report

Date: 2026-08-28

## Verdict

`X1.15 CODEX NO ROBUST IMPROVEMENT: DO NOT UPLOAD`

No standalone candidate was created because no X1.15 variant passed the local development gate. Holdout was not run because the candidate was not frozen.

## Candidate Name

`E12_X115_CODEX_INDEPENDENT`

## Architecture Summary

Codex tested a Q2-capable branch derived from X1.12:

- preserve X1.12 opening and early livestock structure;
- add Q2 as a conditional high-ceiling expansion branch;
- expand crop working set into Q2 after ownership;
- permit up to 12 hands;
- preserve Cow/Sheep monetization;
- avoid treating weeds, surface, hands or animal count as standalone objectives.

## Evidence -> Hypothesis -> Delta

| Evidence | Hypothesis | Code delta |
|---|---|---|
| Q2 replay files show strong 3Q scores up to `$133,035` | Q2 is a high-ceiling conditional branch | Added `E12_X115_CODEX_INDEPENDENT` mode and Q2 gate |
| X1.14 reduced weeds but lowered money | Do not optimize crop cleanliness alone | Preserved livestock branch and avoided livestock suppression as primary policy |
| Fixed livestock targets vary across competitors | Herd should be branch-specific and bounded | Tested `10 Cow / 5 Sheep`, `9 Cow / 4 Sheep`, `12 Cow / 3 Sheep` caps as variant envelopes |
| Q2 replay winners use peak productive `75` and peak hands `12` | Q2 needs surface plus capacity | Added Q2 crop positions and 12-hand cap |
| Sokolov wins with Q0 only | Land is not automatically good | Q2 remained gated, not unconditional |

## Development Results

Seeds:

- `0`
- `421521921`
- `1056561958`
- `1273000467`

| Variant | Mean | Median | Min | Max | Verdict |
|---|---:|---:|---:|---:|---|
| `X112` | `$42,780` | `$42,756` | `$37,294` | `$48,313` | baseline |
| `X115B` | `$18,754` | `$18,412` | `$17,683` | `$20,508` | rejected |
| `X115C` | `$20,836` | `$15,898` | `$10,957` | `$40,591` | rejected |
| `X115D` | `$26,461` | `$28,366` | `$20,269` | `$28,841` | rejected |

Best X1.15 variant by mean: `X115D`, still `-38.15%` versus X1.12 mean.

Full artifacts:

- `results/e12/x115_codex/development_results.json`
- `results/e12/x115_codex/development_results.csv`
- `results/e12/x115_codex/development_results.md`

## Q1/Q2 Behavior

All X1.15 variants still bought Q1 on Day 12 and never bought Q2 on the development seeds.

The early-land variant did not actually shift Q1 earlier because the X1.12-preserved opening did not have sufficient cash before Day 12. After Q1, livestock/seeds/crop recovery consumed the deployable capital before Q2 could pass the gate.

## Workforce Behavior

- X1.12: peak hands `9`, mean about `6.5`.
- X115B/C/D: peak hands `10`, mean from `5.03` to `7.10`.

More hands did not improve money, consistent with X1.14 counterevidence.

## Livestock Behavior

- X1.12 preserved `7 Cow / 4 Sheep`.
- X115B/C usually collapsed to `7 Cow / 0 Sheep`.
- X115D preserved some sheep, ending around `7 Cow / 3 Sheep`, but still lost too much money.

The failure supports the existing conclusion: livestock revenue must be preserved, and partial sheep loss is economically costly.

## Monetization Behavior

X1.15 variants reduced Wheat volume relative to X1.12, but also sharply reduced Milk/Wool/Fertilizer and premium crop monetization. The result was cleaner-looking but economically weaker.

## Failure Modes

1. Q2 evidence was not operationalized because the preserved X1.12 opening did not generate early deployable cash.
2. Higher surface and lower weeds did not compensate for lost livestock/product revenue.
3. The X1.12 routing/logistics engine did not become a top-style 3Q engine just by adding Q2 targets.
4. Variants that protected expansion or crop surface delayed or suppressed Sheep, repeating the X1.14 pattern.
5. Q2 likely requires a different opening, not a late bolt-on to X1.12.

## Holdout

Not run. The holdout protocol is reserved for a frozen candidate. No X1.15 variant passed the development gate.

## Standalone

Not created. `submission/submission_x115_codex.py` was not generated.

## Equivalence And Tests

- X1.12 source/submission equivalence: PASS via `scripts/verify_x112_submission_candidate.py`.
- Regression tests: `12 passed`, one non-blocking `.pytest_cache` warning.
- Syntax check: `py_compile` passed for `src/agricola/strategy/productive_mass_roi.py` and `scripts/benchmark_e12_x1_15_codex.py`.

## Files Created Or Modified

Created:

- `results/e12/x115_codex/IMPLEMENTATION_HYPOTHESIS.md`
- `results/e12/x115_codex/FINAL_REPORT.md`
- `results/e12/x115_codex/development_results.json`
- `results/e12/x115_codex/development_results.csv`
- `results/e12/x115_codex/development_results.md`
- `scripts/benchmark_e12_x1_15_codex.py`

Modified:

- `src/agricola/strategy/productive_mass_roi.py`

Not modified:

- `docs/MODEL_SPEC.md`
- `submission/submission.py`
- raw replay JSON files
- dependency/environment files

## Next Technical Lesson

The next serious Q2 attempt should not graft Q2 onto X1.12 after its Day-12 Q1 path. It needs a new opening that accumulates early deployable capital before Q1/Q2 while preserving livestock monetization, or a compact branch that explicitly chooses not to expand.
