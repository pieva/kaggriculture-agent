# E12-X1.15 Codex Independent Build Hypothesis

Date: 2026-08-28

## Evidence Used

1. `OBSERVED`: `101462495`, `101761797` and `101891362` contain strong Q2/3Q play with high-side scores from `$96,069` to `$133,035`.
2. `OBSERVED`: Q2 high-side runs reach peak productive surface `75` and peak hands `12`.
3. `OBSERVED`: Q2 timing in the new replay set is Day 9-11, not a universal fixed date.
4. `OBSERVED`: Q1-only elite runs still reach `$86,297` and `$90,137`, so Q2 is not mandatory.
5. `OBSERVED`: Sokolov `101717011` wins with Q0 only, peak productive `15`, and peak hands `8`, so land/surface are means, not objectives.
6. `OBSERVED`: all strong competitors monetize livestock products and Fertilizer; X1.13/X1.14 livestock suppression regressed badly.
7. `OBSERVED`: fixed livestock mixes are invalid: observed finals include `9 Cow / 5 Sheep`, `7 Cow / 4 Sheep / 2 Goose`, `4 Cow / 2 Sheep`, `6 Cow / 9 Sheep`, `14 Cow / 2 Sheep`, and `12 Cow`.
8. `OBSERVED`: X1.14 reduced weed tile-days but reduced money on required seeds, so clean field alone is not an economic target.
9. `INFERRED`: high Q2 scores require expansion activation plus enough logistics and livestock revenue, not land purchase by itself.
10. `CAUSAL_REQUIRED`: whether X1.12 can support Q2 without recreating premature expansion failures must be verified by counterfactual runs.

## Chosen Architecture

Mode: `E12_X115_CODEX_INDEPENDENT`.

The initial candidate is a Q2-capable, livestock-preserving branch derived from X1.12 infrastructure:

- keep X1.12 opening and early livestock because it already beats X1.11 locally;
- add Q2 as a conditional high-ceiling branch rather than a fixed target;
- expand the crop working set into Q2 only after Q2 is owned;
- raise crop targets only when land exists, avoiding a seed/cash drain before activation;
- preserve Cow/Sheep monetization instead of repeating X1.14 crop-clean variants that suppressed revenue;
- keep workforce capped at 12 but schedule it from land/horizon rather than pure weed cleanup.

## Why This Could Beat X1.12

X1.12 peaks around two-quadrant production and remains far below Q2 replay ceilings. The six-replay review shows that strong Q2 play can produce a much larger monetizable surface without abandoning livestock products. A gated Q2 branch is the smallest structural change that tests the new evidence while avoiding a rewrite.

## Main Overfitting Risks

- Buying Q2 too early can repeat the old `101294736` failure pattern.
- More crop surface can lower economic density if workers spend too much time moving.
- A 12-hand cap can overspend on seeds where compact Q0/Q1 play is better.
- Q2 replay success may be agent-quality evidence rather than land evidence.
- Without a price ledger, Wheat buy/sell changes remain risky.

## Initial Verification Plan

Development seeds:

- `0`
- `421521921`
- `1056561958`
- `1273000467`

Holdout seeds after freeze only:

- `2026082801`
- `2026082802`
- `2026082803`
- `2026082804`

Adopt only if the development set shows meaningful aggregate improvement over X1.12 without catastrophic regression, then confirm on holdout before building a standalone candidate.
