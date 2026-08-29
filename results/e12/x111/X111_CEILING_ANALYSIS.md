# E12-X1.11 Ceiling Analysis

Status: NOT SUCCESSFUL

Run: `E12-X1.11-20260828-102541`

## Hard Gates

| Gate | Result |
| --- | --- |
| Seed 0 `final_money >= 80000` | FAIL: `29858.00` |
| Seed 421521921 `final_money >= 80000` | FAIL: `24827.00` |
| Q0+Q1 only, `owned_quadrants == 2` | PASS |
| Q2 disabled | PASS |
| Source/submission equivalence | PASS via `tests/test_submission_behavioral_equivalence.py` |

## Best Results

| Seed | Final Money | Gap to 80000 | Owned Quadrants | Peak Active Tiles | Peak Workforce |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | `29858.00` | `50142.00` | 2 | 26 | 4 |
| 421521921 | `24827.00` | `55173.00` | 2 | 27 | 4 |

Mean final money: `27342.50`.

## Iteration History

| Iteration | Seed 0 | Seed 421521921 | Finding |
| --- | ---: | ---: | --- |
| Pre-existing X1.11 draft | `661.00` | `895.00` | Pasture-first dispatcher collapsed crop production; milk pipeline yielded `0.00`. |
| Dense Q0+Q1 EPU attempt | `22364.00` | `23414.00` | More tiles caused high travel and lower harvest count than the verified E06 core. |
| Verified E06/EPU core routed as X1.11 | `29858.00` | `24827.00` | Best reproducible Q0+Q1 result in this workspace. |

## Revenue and Cost Decomposition

Seed 0:

- Crop revenue: `40932.00`
- Milk revenue: `0.00`
- Seed spend: `5300.00`
- Land spend: `1000.00`
- Workforce spend: `62.00`
- Livestock spend: `0.00`

Seed 421521921:

- Crop revenue: `29137.00`
- Milk revenue: `0.00`
- Seed spend: `4140.00`
- Land spend: `1000.00`
- Workforce spend: `62.00`
- Livestock spend: `0.00`

## Contribution Analysis

The DEFINE contribution ladder projected approximately:

- Net livestock engine: `+14000`
- Crop rotation engine: `+48000`
- Retail wheat savings: `+8000`

Measured local evidence does not support those magnitudes:

- The pre-existing X1.11 livestock draft bought cows and built pastures but produced `0.00` milk revenue.
- Existing X1.3 4-quadrant livestock controls only produced about `2542-2970` milk revenue on the same two seeds.
- X1.9/X1.7 Q0+Q1 controls produced about `26194-30220` final money without milk contribution.
- The best verified Q0+Q1 crop engine remains around `24827-29858`, not near `80000`.

Retail wheat elimination is real but not large enough: the failed draft spent only `100.00` on retail wheat per seed, so removing it cannot close a `50k+` gap.

## Structural Ceiling Evidence

Under the current Q0+Q1 action economy, verified crop throughput peaks around 26-27 productive tiles with 4 effective workers. Attempts to expand the managed surface to more tiles reduced final money because movement and maintenance displaced harvest turnover.

The remaining gap is not a marginal routing issue:

- Seed 0 needs `+50142.00`.
- Seed 421521921 needs `+55173.00`.
- The largest measured livestock upside in nearby working agents is roughly `3k`, not `14k`.
- The dense tile attempt lost `5k-7k` versus the verified E06/EPU core.

## Architectural Assumption That Must Change

The current X1.11 assumption that Q0+Q1 alone can reach `80000` with repaired livestock, feed sizing, and local crop allocation is not supported by local evidence.

To plausibly pursue `80000`, one of these constraints likely has to change:

- Allow Q2/Q3 expansion again with a materially better workforce/market engine.
- Discover a new high-throughput worker architecture that activates 40+ Q0+Q1 tiles without harvest delay.
- Find an environment mechanic not currently exploited by the repo's crop/livestock agents, such as a materially different market-price or inventory timing strategy.

Do not label E12-X1.11 as successful unless both required seeds reach `80000` and source/submission equivalence remains true.
