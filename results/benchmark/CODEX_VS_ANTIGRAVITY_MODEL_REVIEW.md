# Codex vs Antigravity MODEL_SPEC Review

Date: 2026-08-28

## Executive Comparison

The main divergence is evidence scope.

Antigravity reviewed three replay files: `101294736`, `101705751`, `101717011`. Codex reviewed all six raw JSON files currently present in `docs/benchmark/`: those three plus `101462495`, `101761797`, `101891362`.

That difference changes the land/Q2 conclusion. Antigravity was right to say the original 3-replay batch did not support Q2. Codex finds that the current 6-replay folder contains three strong Q2 examples, including scores from `$96,069` to `$133,035`, Q2 on Day 9-11, peak productive surface `75`, and peak hands `12`.

Therefore, the recommended human resolution is not "Antigravity wrong"; it is:

> Antigravity's Q2 conclusion was valid for its evidence set, but is now stale under the expanded benchmark folder.

## Same Classification

| Claim | Antigravity verdict | Codex verdict | Resolution |
|---|---|---|---|
| Fixed hand count / more hands mechanically means more money | Not supported / mixed | Not supported / mixed | Agree. Workforce must be value/capacity based. |
| Fixed `7 Cow / 4 Sheep` target | Supported as invalid target | Supported as invalid target | Agree. Keep as `OBSERVED_REFERENCE`, not target. |
| Livestock as economic engine | Supported | Supported | Agree strongly. |
| Multi-engine monetization | Supported | Supported | Agree strongly. |
| Deployable Capital direct observability | Not observable / inferred | Not observable / inferred | Agree. Useful model variable, not replay fact. |
| Wheat loop economic damage | Partially supported | Mixed / partially supported | Broad agreement: volume anomaly is observed; P/L needs ledger. |
| Horizon-aware shutdown as universal rule | Mixed | Partially supported / low confidence | Agree that universal wording is too strong. |

## Different Classification

| Claim | Antigravity verdict | Codex verdict | Raw evidence | Recommended human resolution |
|---|---|---|---|---|
| Q2 conditional only / not priority | Supported within 3-replay batch; "absence in batch" | Mixed; Q2 is high-ceiling conditional | `101462495`, `101761797`, `101891362` all include 3Q high-score play, Q2 Day 9-11, peak productive `75` | Update MODEL_SPEC to say Q2 is not universally required but is a proven high-ceiling branch. |
| Q0+Q1 sufficient envelope | Supported for 3-replay batch | Mixed under 6 replays | Q1-only scores `$86,297`, `$90,137`; Q2 scores `$96,069`, `$105,273`, `$126,754`, `$130,072`, `$133,035` across high sides | Keep Q0/Q1 as valid envelope, remove any ceiling implication. |
| Dense Engine Before Expansion | Supported by Antigravity's three files | Partially supported | Sokolov supports compact density; Q2 winners expand and monetize early | Reframe as "monetizable density during expansion", not strict before/after ordering. |
| Backlog avoidance | Mixed in Antigravity | Supported for elite-scale, but not causal alone | Q1/Q2 elite high sides show weed tile-days `10`, `11`, `5`, `1`, `24`, `26`; Sokolov `145` is lower ceiling | State as operating constraint for scale, not standalone objective. |
| Productive Surface First | Partially supported | Mixed | Q2 high sides peak `75`; Sokolov peaks `15` and beats us | Split into two archetypes: compact monetization and large-scale throughput. |
| Crop SLA Before Expansion | Not supported / contradicted by X1.14 | Partially supported / causal required | X1.14 crop priority regressed; Q2 winners still keep low weeds while scaling | Do not remove; recast as "SLA must not suppress product engines." |

## Causal Interpretation Differences

Antigravity is generally more skeptical of turning replay correlations into policy claims. Codex agrees with that caution, but the expanded Q2 evidence makes some positive claims stronger:

- Q2 has observed successful executions, not merely theoretical potential.
- High productive surface can be monetized if paired with workforce and logistics.
- Low weeds remain associated with elite-scale runs, even though X1.14 proves weed reduction alone is insufficient.

Codex is more assertive only where the three new raw replays add direct evidence.

## Evidence Used By One Agent But Not The Other

Antigravity used:

- 3 raw replay JSON files.
- X1.13/X1.14 counterfactual summaries.
- Detailed extracted timelines for workforce, money, wheat loop and endgame.

Codex used:

- all 6 raw replay JSON files in `docs/benchmark/`;
- the same permitted MODEL_SPEC and benchmark documents;
- X1.14 counterfactual table;
- parsed aggregate metrics from `scripts/benchmark_batch_registry.py` without rewriting strategy/submission.

Codex did not independently reconstruct full per-transaction price ledgers.

## Possible Parsing Issues

- In Q2 files there is no Pietro side. The existing parser labels the first non-Pietro side as "our" and the other as "competitor"; this naming is not meaningful for `101462495`, `101761797`, `101891362`. Codex therefore treats both sides as competitive evidence and uses the high-scoring side for summary.
- Weed tile-days and unwatered tile-days can be measurement-sensitive. Antigravity found surprising unwatered counts; Codex did not re-audit that metric deeply.
- `BUY_PRODUCT` versus `BUY_SEED` naming may be flattened by parser logic; Wheat loop claims need a dedicated ledger before economic conclusions.
- Final livestock can differ from animal buys; attrition or intermediate loss should be audited before inferring target herds.

## Possible Over-Generalizations

Antigravity over-generalization risk:

- Treating 3-replay Q2 absence as broad Q2 rejection.
- Treating Q0/Q1 sufficiency as near-ceiling evidence.

Codex over-generalization risk:

- Treating Q2 high scores as transferable to X1.12 before testing activation/logistics.
- Overweighting high-score Q2 replays without separating agent strength from land policy.
- Assuming low weeds are required for all winning strategies despite Sokolov.

## More Prudence / More Assertion

Antigravity is more prudent on:

- causality;
- deployable capital;
- wheat P/L;
- endgame shutdown;
- decision intent.

Codex is more assertive on:

- Q2 being a proven high-ceiling branch;
- Q0+Q1 no longer being a strong envelope under current evidence;
- the need to split compact-density and 3Q-throughput archetypes.

## Divergences Requiring Human Control

| Divergence | Why human review matters | Suggested decision |
|---|---|---|
| Whether to patch MODEL_SPEC immediately for Q2 | It changes next BUILD direction materially. | Patch wording before next BUILD; do not implement yet. |
| Whether Q2 files should be folded into canonical registry | Current `BENCHMARK_REGISTRY.md` covers only 3 replay rows. | Rebuild/update registry in a separate analysis task if approved. |
| Whether Crop Dusta/Ryo/Subramanya are the correct competitor labels for high sides | Parser names "our" by Pietro presence; Q2 files need neutral labels. | Use neutral `player_0/player_1` plus team names in future registry. |
| Whether Wheat loop is wasteful | Requires price/inventory ledger, not aggregate counts. | Build ledger parser before model patch that changes Wheat. |
| Whether X1.14 falsifies workforce capacity or only a bad implementation | Important for next BUILD. | Treat X1.14 as falsifying aggressive workforce as tested, not the capacity concept. |

## Divergences Requiring More Replay Or Counterfactual

- Q2 transferability to X1.12 on seeds `0`, `421521921`, `1273000467`.
- Q0-only compact branch reproducibility beyond `101717011`.
- Goose/Egg marginal value versus Cow/Sheep only.
- Worker action value by product channel.
- Crop SLA threshold that protects scale without suppressing livestock/product revenue.

## Recommended Unified Patch Direction

1. Keep Antigravity's caution about causality.
2. Add Codex's expanded Q2 evidence.
3. Replace "Q2 not priority" with "Q2 conditional high-ceiling branch observed; not universally required."
4. Replace "Cross-Competitor Invariants" with "Cross-Competitor Patterns".
5. Split land strategies into at least three observed archetypes:
   - compact Q0 monetization;
   - Q0+Q1 elite livestock/crop engine;
   - Q0+Q1+Q2 high-surface throughput engine.
6. Keep X1.14 as counterevidence against simple workforce/crop-priority tuning.
7. Require ledger telemetry before changing Wheat market behavior.

## Bottom Line

Antigravity's review is the better causal-skeptic document for the original 3-replay batch. Codex's review is more current for the actual folder contents because it includes the three Q2 replay files. The combined conclusion is stronger than either alone:

> The MODEL_SPEC should remain strict about evidence versus causality, but it must be updated so Q2 is no longer framed as absent/rejected. Q2 is a conditional expansion path with direct high-score evidence, and the next model work should test whether X1.12 can activate that branch without repeating earlier premature-expansion failures.
