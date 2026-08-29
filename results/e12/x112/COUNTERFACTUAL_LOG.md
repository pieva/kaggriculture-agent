# X1.12 Truebelief Economic Engine Reconstruction - Counterfactual Log

Primary evidence:
- Raw replay: `results/e12/x111/101294736.json`
- Raw SHA-256: `6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695`
- Parsed benchmark: `results/e12/x111/truebelief_benchmark.json`
- Timeline: `results/e12/x111/x111_truebelief_comparison_timeline.csv`
- Summary: `results/e12/x111/TRUEBELIEF_BENCHMARK.md`

Gate:
- Required: `final_money >= 80000` on seeds `0` and `421521921`, Q0+Q1 only.
- Status: not passed.
- Submission was not rebuilt.

Best X1.12 local checkpoint so far:

| Config | Seed 0 | Seed 421521921 | Peak Productive | Final Livestock |
| --- | ---: | ---: | ---: | --- |
| 7 Cow / 4 Sheep | 42,491 | 48,313 | 35 | 7 Cow / 4 Sheep |

Measured deltas and counterfactuals:

| Change | Seed 0 | Seed 421521921 | Outcome |
| --- | ---: | ---: | --- |
| Crop-only X1.12, dynamic pasture exclusion | 34,711 | 30,542 | Positive vs no-engine baseline, below X1.12 livestock |
| 4 Cow / 2 Sheep | 39,342 | 40,844 | Positive livestock contribution, lower than 7/4 |
| 6 Cow / 2 Sheep | 35,766 | 43,205 | Unstable; Wool/Fertilizer under-realized |
| 7 Cow / 4 Sheep | 42,491 | 48,313 | Best checkpoint |
| 9 Cow / 5 Sheep | 37,767 | 44,447 | Too much livestock drag |
| Hardcoded truebelief Day-1 schedule | 30,176 | 34,044 | Negative despite matching Day-1 21 crop / 4 pasture |
| Predicted post-sell cash for same-day Q1 | 17,770 | 27,326 | Negative; Q1/cows too early collapse surface |
| Pre-seed Q1 before livestock | 42,391 | 48,213 | Neutral/slightly negative |
| Multi-hour HIRE plus surface-first animal harvest/care | 23,607 | 24,991 | Negative; hire cost and routing overhead dominate |
| Pasture conversion to force 11 structures | 39,995 | 41,475 | Negative; lost crop throughput exceeds livestock gain |
| Replay Day 11-15 action slice | 30,140 | 28,237 | Negative; replay actions do not transfer to divergent local state |

Current diagnosis:
- The truebelief reference reaches Day 14-20 at roughly `39 crop + 11 pasture + 11 animals`.
- The best local X1.12 reaches 7 Cow / 4 Sheep, but only about `21 crop + 9 pasture` in the same midgame window.
- The missing gap is not a single buy target. It is worker assignment/routing throughput after Q1: planting and watering Q1 are starved by movement, feed/care, pickup/place, and market-order timing.
- `FERTILIZE` is not part of the observed truebelief action set; truebelief monetizes Fertilizer through collection and sale.
- The local player-1 replay context is not a valid benchmark substitute: running X1.12 as player 1 against replay player-0 actions collapses to near-zero cash, so it was discarded.

No files intentionally updated:
- `PROJECT_STATE`
- `NEW_SESSION`
- `EXPERIMENT_LOG`
- submission bundle
