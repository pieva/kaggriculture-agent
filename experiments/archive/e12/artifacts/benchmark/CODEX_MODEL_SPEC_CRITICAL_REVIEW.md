# Codex Independent Critical Review: MODEL_SPEC vs Benchmark Replay JSON

Date: 2026-08-28

## Executive Verdict

`docs/model_specs/history/MODEL_SPEC_PRE_C2.md` is directionally strong on the big safety rails: fixed livestock targets are invalid, fixed hand counts are invalid, multi-engine monetization is real, and replay trajectories must not be copied as constants.

The largest issue is Q2. The earlier three-replay batch supported "Q2 not required"; the current `docs/benchmark/` folder also contains three Q2 replays with very high scores. Those raw files materially weaken any wording that treats Q2 as low-priority or mostly rejected. The better claim is:

> Q2 is not universally required, but it is a proven high-ceiling expansion when activated with enough workforce, crop surface, livestock/logistics throughput and capital discipline.

The second issue is causality. Several MODEL_SPEC claims correctly point in the right direction but should remain `INFERRED` or `CAUSAL_REQUIRED`: deployable capital, marginal HIRE, market/logistics efficiency and horizon-aware shutdown cannot be proven from replay summaries alone.

Process limitation: during file discovery I accidentally exposed lines from Antigravity's existing review via `rg`. I did not read the full Antigravity artifacts before producing this file, but this means the blind-review barrier is imperfect. The classifications below are based on the raw replay files and allowed registry/model documents.

## Evidence Base

Raw replay files inspected in `docs/benchmark/`:

| Episode | Seed | Agents | Rewards | High-scoring side | Final quadrants | Q2 day | Peak hands | Peak productive | Weed tile-days | Final livestock | Main sold products |
|---|---:|---|---:|---|---|---:|---:|---:|---:|---|---|
| `101294736` | `421521921` | Pietro Valocchi vs truebelief | `6825 / 86297` | truebelief | `NW,NE` | n/a | 12 | 50 | 10 | `9 Cow / 5 Sheep` | Wheat, Fertilizer, Milk, Melon, Wool |
| `101462495` | `1296761739` | Crop Dusta vs Ryo Hasegawa | `126754 / 130072` | Ryo Hasegawa | `NW,NE,SW` | 11 | 12 | 75 | 5 | `6 Cow / 9 Sheep` | Wheat, Fertilizer, Strawberry, Wool, Milk |
| `101705751` | `1056561958` | Pietro Valocchi vs Dr. Mikholae Hutchinson | `38815 / 90137` | Dr. Mikholae Hutchinson | `NW,NE` | n/a | 10 | 46 | 11 | `7 Cow / 4 Sheep / 2 Goose` | Fertilizer, Milk, Strawberry, Wheat, Egg |
| `101717011` | `1273000467` | Alexander Sokolov vs Pietro Valocchi | `50420 / 24314` | Alexander Sokolov | `NW` | n/a | 8 | 15 | 145 | `4 Cow / 2 Sheep` | Wheat, Milk, Fertilizer, Carrot, Wool |
| `101761797` | `480111092` | Ryo Hasegawa vs Crop Dusta | `105273 / 96069` | Ryo Hasegawa | `NW,NE,SW` | 11 | 12 | 75 | 1 | `14 Cow / 2 Sheep` | Milk, Strawberry, Fertilizer, Wheat, Melon |
| `101891362` | `1227804547` | Subramanya N vs Crop Dusta | `107914 / 133035` | Crop Dusta | `NW,NE,SW` | 9 | 12 | 75 | 24 | `12 Cow` | Wheat, Milk, Fertilizer, Strawberry, Tomato |

Allowed secondary evidence used:

- `docs/model_specs/history/MODEL_SPEC_PRE_C2.md`
- `experiments/archive/e12/artifacts/benchmark/BENCHMARK_REGISTRY.md`
- `experiments/archive/e12/artifacts/benchmark/CROSS_COMPETITOR_ANALYSIS.md`
- `experiments/archive/e12/artifacts/benchmark/NEXT_MODEL_DELTA.md`
- `experiments/archive/e12/artifacts/x114/COUNTERFACTUAL_LOG.md`

## Hypothesis-By-Hypothesis Audit

| Claim | Verdict | Confidence | Evidence type | Rationale | Patch plan |
|---|---|---|---|---|---|
| Workforce Capacity First | `MIXED` | MEDIUM | `CAUSAL_REQUIRED` | Strong players commonly use high workforce, especially Q2 runs with 12 hands, but Sokolov wins with 8 and X1.14 aggressive workforce regresses required seeds. | `REFRAME` |
| Workforce size | `NOT_SUPPORTED` | HIGH | `OBSERVED` | No fixed count is stable: 8, 10 and 12 all appear in winning or elite paths. | `REMOVE` |
| Workforce timing | `PARTIALLY_SUPPORTED` | MEDIUM | `INFERRED` | Sustained workforce appears important, but timing causality needs per-day hire/payback comparison. | `REFRAME` |
| Workforce utilization | `PARTIALLY_SUPPORTED` | MEDIUM | `INFERRED` | Productive action volume correlates with top Q2 scores, but not enough to explain Sokolov or X1.14. | `REFRAME` |
| Backlog avoidance | `SUPPORTED` | HIGH | `OBSERVED` | Low weeds strongly accompany the 86k-133k replays; Sokolov is a lower-score counterexample, not a full refutation. | `KEEP` |
| Productive Surface First | `MIXED` | HIGH | `OBSERVED` | Elite scores use 46-75 peak productive tiles; Sokolov wins with only 15. | `REFRAME` |
| Dense Engine Before Expansion | `PARTIALLY_SUPPORTED` | MEDIUM | `INFERRED` | Compact density matters, but Q2 winners expand early and monetize. "Before" is too rigid. | `REFRAME` |
| Land Discipline | `SUPPORTED` | HIGH | `OBSERVED` | Bad expansion loses; disciplined Q2 wins. The claim should be about payback quality, not avoiding land. | `REFRAME` |
| Q1 conditional expansion | `SUPPORTED` | HIGH | `OBSERVED` | Q1 appears in elite Q1 and Q2 runs, but Sokolov proves it is not mandatory. | `KEEP` |
| Q2 conditional only / not priority | `MIXED` | HIGH | `OBSERVED` | New Q2 replays contradict any de-prioritization stronger than "conditional." | `DOWNGRADE` |
| Livestock as economic engine | `SUPPORTED` | HIGH | `OBSERVED` | All high-scoring competitors monetize livestock outputs and Fertilizer. | `KEEP` |
| Fixed livestock targets are invalid | `SUPPORTED` | HIGH | `OBSERVED` | Livestock mixes vary widely, including Goose and Cow-only final mixes. | `KEEP` |
| Multi-engine monetization | `SUPPORTED` | HIGH | `OBSERVED` | Every competitor sells several product families. | `KEEP` |
| Deployable Capital | `NOT_OBSERVABLE` | MEDIUM | `INFERRED` | Useful concept, but not directly measurable without reconstructing obligations and payback. | `NEEDS_MORE_EVIDENCE` |
| Horizon-aware shutdown | `PARTIALLY_SUPPORTED` | LOW | `INFERRED` | Late selling is visible, but shutdown intent and optimality require a detailed endgame action ledger. | `NEEDS_MORE_EVIDENCE` |
| HIRE by marginal monetizable throughput | `NOT_OBSERVABLE` | MEDIUM | `CAUSAL_REQUIRED` | Replays show hires, not the decision function or counterfactual marginal value. | `NEEDS_MORE_EVIDENCE` |
| Crop-maintenance priority | `PARTIALLY_SUPPORTED` | HIGH | `OBSERVED` | Low weeds matter for elite scores, but X1.14 proves clean field alone can reduce money. | `REFRAME` |
| Physical vs economic utilization | `SUPPORTED` | HIGH | `OBSERVED` | Sokolov monetizes a small footprint better than our larger one; Q2 elites show physical scale must become economic output. | `KEEP` |
| Market/logistics efficiency | `PARTIALLY_SUPPORTED` | MEDIUM | `INFERRED` | Broad sell volume implies logistics throughput; exact route and uncollected-yield losses are not measured yet. | `REFRAME` |
| Wheat BUY_PRODUCT / SELL loop | `MIXED` | HIGH | `OBSERVED` | Wheat buy/sell exists on both sides; profit/waste cannot be asserted without price and inventory ledger. | `REFRAME` |
| Day-1 diversified opening | `PARTIALLY_SUPPORTED` | MEDIUM | `OBSERVED` | Diversification is common, exact constants are not portable. | `REFRAME` |
| Q0+Q1 only as sufficient envelope | `MIXED` | HIGH | `OBSERVED` | It is sufficient for 86k/90k and Q0-only can beat us, but Q2 reaches 96k-133k. | `DOWNGRADE` |
| Crop allocation horizon-aware | `PARTIALLY_SUPPORTED` | LOW | `INFERRED` | Crop mix varies and late liquidation is plausible, but intent is not directly observable. | `NEEDS_MORE_EVIDENCE` |
| Clean field as causal objective | `MIXED` | HIGH | `CAUSAL_REQUIRED` | Elite replays are clean; X1.14 clean-field variants regress; Sokolov tolerates weeds. | `REFRAME` |

## Cross-Competitor Matrix

| Pattern | Q1 elite replays | Q0 compact replay | Q2 elite replays | Interpretation |
|---|---|---|---|---|
| Land | truebelief and Hutchinson use Q1 only | Sokolov remains Q0 only | Ryo/Crop/Subramanya class replays use Q2 | Land value is conditional; Q2 cannot be dismissed. |
| Workforce | 10-12 peak hands | 8 peak hands | 12 peak hands | Use workload/payback, not a copied count. |
| Productive surface | 46-50 peak productive | 15 peak productive | 75 peak productive | Both compact density and large-scale throughput can win. |
| Weeds | 10-11 tile-days | 145 tile-days | 1-26 tile-days on high side | Clean fields are strong for elite scale but not a standalone causal target. |
| Livestock | Cow/Sheep/Goose mix | Cow/Sheep compact mix | Cow-heavy or Sheep-heavy variants | Livestock is robust; fixed mix is false. |
| Monetization | Milk/Fertilizer/Wool/crops | Wheat/Milk/Fertilizer/crops | very broad product sales | Multi-engine monetization is the strongest invariant. |

## Claims Currently Too Strong

- `Q2 not priority` is too strong with the new raw files. Keep only "Q2 conditional".
- `Q0+Q1 only` as a strong envelope is stale. It is one successful envelope, not the ceiling.
- `Dense Engine Before Expansion` should not imply expansion must wait for a fully mature Q0/Q1 engine; Q2 winners activate early and still compound.
- `Workforce Capacity First` should not imply more hands mechanically improves money. X1.14 falsifies that form.
- `Crop maintenance priority` should not become "minimize weeds at any economic cost."

## Claims Strongly Supported

- Fixed livestock targets are invalid.
- Fixed hand counts are invalid.
- Multi-engine monetization is real and repeated across all replay families.
- Land expansion must be disciplined by activation and monetization, not copied by day.
- Physical utilization and economic utilization are different things.

## Counterexamples

- Sokolov `101717011`: beats our two-quadrant policy with Q0 only, 8 peak hands and 15 peak productive tiles.
- Q2 replays `101462495`, `101761797`, `101891362`: contradict a Q2-avoidance reading by reaching 96k-133k with Q2 and 75 peak productive tiles.
- X1.14 variants: weed tile-days fall sharply, but final money regresses on required seeds.
- Our side in `101717011`: more peak productive tiles than Sokolov, but lower final money, showing surface alone is not enough.
- Livestock suppression in X1.13/X1.14-style tests loses too much product monetization.

## Not Observable Claims

- True deployable capital.
- Marginal monetizable throughput per hire.
- Exact market P/L of Wheat buy/sell loops.
- Uncollected livestock yield and logistics queue losses.
- Intentional horizon-aware shutdown versus incidental late behavior.

## Causal Claims Requiring Counterfactual

- Whether Q2 improves X1.12 if activated with the correct prerequisites.
- Whether lower weeds cause higher final money after controlling for livestock and product throughput.
- Whether a workload-derived HIRE function beats a calendar schedule.
- Whether Sokolov-style Q0-only compounding is seed-specific or a general branch.
- Whether Goose/Egg should enter the engine or remain competitor-specific evidence.

## Recommended MODEL_SPEC Patch Plan

| Topic | Action | Patch direction |
|---|---|---|
| Q2 | `DOWNGRADE` | Replace "not priority" with "conditional high-ceiling expansion observed in new Q2 replays; requires payback/capacity gate." |
| Q0+Q1 | `DOWNGRADE` | Treat as one sufficient envelope, not strategic boundary. |
| Workforce | `REFRAME` | Capacity first means monetizable throughput fit, not more hands. |
| Weeds | `REFRAME` | Low backlog is an operating constraint; clean field alone is not a goal. |
| Dense engine | `REFRAME` | Require monetizable density before/while expanding; do not force calendar ordering. |
| Livestock | `KEEP` | Keep fixed-target rejection and capacity/ROI framing. |
| Multi-engine | `KEEP` | Strengthen as observed invariant. |
| Deployable capital | `NEEDS_MORE_EVIDENCE` | Keep as inferred model variable and add required ledger telemetry. |
| Wheat loop | `NEEDS_MORE_EVIDENCE` | Add price/inventory ledger before calling it wasteful or profitable. |
| Endgame | `NEEDS_MORE_EVIDENCE` | Add day 26-30 action and inventory liquidation audit. |

## Claims That Should Remain Unchanged

- Competitor trajectories are evidence, not targets.
- Fixed livestock counts are invalid.
- Fixed hand counts are invalid.
- Q1 should be conditional rather than a copied date.
- Multi-engine monetization is required for elite paths.
- Raw replay JSON is primary evidence.

## Open Questions

- Is Q2 success driven by land itself, by the specific agents' stronger logistics, or by market/seed conditions?
- Can X1.12 support 3Q without recreating the old Q2 failure from `101294736`?
- Does Sokolov's Q0-only win generalize beyond seed `1273000467`?
- What is the real P/L of the Wheat buy/sell loop after price and inventory reconstruction?
- Which product channel has the highest marginal return per worker-action in days 10-25?

## Confidence Limitations

- Replay summaries expose realized behavior, not decision intent.
- The parser captures action/product counts but not full economic ledgers.
- Some "our side" episodes are not the same local candidate version, so they are weak evidence about X1.12 itself.
- New Q2 files change the benchmark distribution and make prior three-replay conclusions incomplete.
- No new benchmark or strategy test was run for this review.

## Classification Count

| Classification | Count |
|---|---:|
| `SUPPORTED` | 7 |
| `PARTIALLY_SUPPORTED` | 8 |
| `MIXED` | 6 |
| `NOT_SUPPORTED` | 1 |
| `CONTRADICTED` | 0 |
| `NOT_OBSERVABLE` | 2 |

Total claims audited: 24.
