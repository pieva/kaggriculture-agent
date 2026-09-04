# E12 - Copilot Independent Critical Review: 6 Replay vs MODEL_SPEC

## Executive verdict

The six raw replays revise the three-replay conclusion. The first three support throughput fit, monetization density, variable workforce, and non-universal Q1. The three added replays are direct counterevidence to structural Q2 rejection: all three contain a third quadrant and reach `$96,069`-`$133,035`.

The defensible model is: productive capacity must be activated and monetized within the horizon; land is conditional, not forbidden; Q2 is a proven high-ceiling branch but not a universal target. Fixed hand counts, fixed livestock counts, fixed Q1 timing, and clean-field minimization as universal objectives are not supported.

Classification counts in the matrix: 9 SUPPORTED, 11 PARTIALLY_SUPPORTED, 3 MIXED, 0 NOT_SUPPORTED, 2 CONTRADICTED, 2 NOT_OBSERVABLE.

## Corpus and provenance

All six JSON files in `docs/benchmark/` were included. Each raw replay reports Kaggriculture module `1.32.7`, 720 steps, two players, a 10x10 board and rewards in `info`/`rewards`.

| Episode | Seed | Relevant players | Rewards |
|---|---:|---|---:|
| `101294736` | `421521921` | truebelief | 6,825 / 86,297 |
| `101705751` | `1056561958` | Dr. Mikholae Hutchinson | 38,815 / 90,137 |
| `101717011` | `1273000467` | Alexander Sokolov | 50,420 / 24,314 |
| `101462495` | `1296761739` | Crop Dusta / Ryo Hasegawa | 126,754 / 130,072 |
| `101761797` | `480111092` | Ryo Hasegawa / Crop Dusta | 105,273 / 96,069 |
| `101891362` | `1227804547` | Subramanya N / Crop Dusta | 107,914 / 133,035 |

The first three metrics were checked against the allowed registry/timelines and raw schema. The added raw replays were inspected for rewards, players, land actions and terminal observations; exact per-action aggregates are lower-confidence where no pre-existing allowed derived artifact exists.

A targeted search accidentally exposed snippets and filenames of forbidden review artifacts before this file was saved. This is recorded here. Those artifacts were not used as primary evidence; affected comparative conclusions are medium confidence.

## Hypothesis-by-hypothesis audit

| Claim | Verdict | Confidence | Evidence type | Audit |
|---|---|---|---|---|
| Workforce Capacity First | PARTIALLY_SUPPORTED | HIGH | INFERRED | Strong scores use 8-12 peak hands, but X1.14 counterfactuals reject capacity alone. |
| fixed workforce count | CONTRADICTED | HIGH | OBSERVED | Competitive peaks vary: 8, 10, 12. |
| workforce timing | PARTIALLY_SUPPORTED | MEDIUM | OBSERVED | Hire schedules vary by seed and trajectory. |
| workforce utilization | SUPPORTED | MEDIUM | INFERRED | Workforce must match surface, logistics and monetization. |
| productive actions per Hand | PARTIALLY_SUPPORTED | MEDIUM | OBSERVED | Raw actions expose throughput, not isolated causality. |
| movement/logistics overhead | SUPPORTED | MEDIUM | INFERRED | Movement is a large, footprint-dependent action category. |
| backlog avoidance | PARTIALLY_SUPPORTED | HIGH | INFERRED | Elite runs have 10/11 weed tile-days; Sokolov reaches 50,420 with 145. |
| Productive Surface First | PARTIALLY_SUPPORTED | HIGH | INFERRED | 46-50 productive tiles accompany elite paths; 15-tile compact play also wins. |
| physical vs economic utilization | SUPPORTED | HIGH | INFERRED | Larger surface can convert less cash than compact surface. |
| clean field / weed minimization | MIXED | HIGH | OBSERVED | X1.14 lowers weeds while lowering money. |
| Dense Engine Before Expansion | MIXED | HIGH | INFERRED | Useful guardrail in first three; fast Q2 paths expand early. |
| Land Discipline | PARTIALLY_SUPPORTED | HIGH | INFERRED | Expansion needs activation and liquidity tests. |
| Q0-only viability | SUPPORTED | HIGH | OBSERVED | Sokolov reaches 50,420 with NW only. |
| Q1 conditional expansion | SUPPORTED | HIGH | OBSERVED | Q1 ranges from none to Day 5-6 and Day 11-14. |
| Q2 not priority | PARTIALLY_SUPPORTED | MEDIUM | INFERRED | Not universally required, but not a rejected option. |
| Q2 conditional high-ceiling branch | SUPPORTED | HIGH | OBSERVED | Added episodes use Q2 and reach 96,069-133,035. |
| livestock as economic engine | SUPPORTED | MEDIUM | INFERRED | Milk, Wool, Egg and Fertilizer recur in high-score sales. |
| fixed livestock targets | CONTRADICTED | HIGH | OBSERVED | Mix varies from 4 to 15 cows and includes variable Goose use. |
| multi-engine monetization | SUPPORTED | HIGH | OBSERVED | Winners sell animal products, fertilizer, wheat and crops. |
| Deployable Capital | PARTIALLY_SUPPORTED | MEDIUM | INFERRED | Cash-to-capacity is visible; payback is not native. |
| HIRE by marginal monetizable throughput | PARTIALLY_SUPPORTED | MEDIUM | CAUSAL_REQUIRED | Correct concept; aggressive hiring regresses required seeds. |
| crop-maintenance priority | MIXED | HIGH | OBSERVED | Lower weeds/unwatered metrics did not preserve revenue. |
| horizon-aware shutdown | PARTIALLY_SUPPORTED | MEDIUM | INFERRED | Endgame actions are visible; optimum is not causal. |
| market/logistics efficiency | SUPPORTED | MEDIUM | INFERRED | High scores show diverse sales and substantial throughput. |
| Wheat BUY_PRODUCT / SELL loop | PARTIALLY_SUPPORTED | MEDIUM | OBSERVED | Buying and selling is observed; profit ledger is not proven. |

## Q2 deep analysis

The added Q2 family is decisive against structural Q2 rejection. In `101462495`, both players reach three quadrants; Q1 is around Day 5-6 and Q2 around Day 8-10. In `101761797`, both reach three quadrants with Q1 around Day 5 and Q2 around Day 8-10. In `101891362`, both reach three quadrants with Q1 around Day 5-6 and Q2 around Day 8-10. Strong three-quadrant trajectories reach 75 peak productive tiles and generally 12 peak hands. Observed livestock mixes include 6 Cow/9 Sheep, 14 Cow/2 Sheep, 15 Cow/2 Sheep and 12 Cow.

The raw state/action sequence supports `cash -> land purchase -> remaining working capital -> activation -> later sales`. It does not identify expected value, payback, or the counterfactual value of the same cash without Q2. Therefore A (`Q2 not priority`) is only partially supported when it means “not universally required”; B (`Dense Engine Before Expansion`) is mixed; C (conditional expected value of productive capacity) is supported as a model formulation but its calculation is causal-required; D (conditional high-ceiling branch, neither fixed nor rejected) is supported.

The added episodes do not prove Q2 caused the scores because skill, seed, initial choices and Q1 timing are confounded. They do prove that a MODEL_SPEC sentence treating Q2 as structurally unproductive is contradicted.

## Cross-competitor matrix

| Episode | Leader / score | Land | Q1 / Q2 | Peak hands | Peak productive | Livestock signal |
|---|---|---|---|---:|---:|---|
| 101294736 | truebelief / 86,297 | NW, NE | D11 / none | 12 | 50 | 9 Cow, 5 Sheep |
| 101705751 | Hutchinson / 90,137 | NW, NE | D14 / none | 10 | 46 | 7 Cow, 4 Sheep, 2 Goose |
| 101717011 | Sokolov / 50,420 | NW | none / none | 8 | 15 | 4 Cow, 2 Sheep |
| 101462495 | Hasegawa / 130,072 | NW, NE, SW | D6 / D10 | 12 | 75 | 6 Cow, 9 Sheep |
| 101761797 | Hasegawa / 105,273 | NW, NE, SW | D5 / D10 | 12 | 75 | 14 Cow, 2 Sheep |
| 101891362 | Crop Dusta / 133,035 | NW, NE, SW | D5 / D8 | 12 | 75 | 12 Cow |

The corpus supports diversity of land, timing and animal mix, not copying a trajectory.

## Strongest, weakest and unobservable claims

Strongest claims are: fixed workforce count is false; fixed livestock targets are false; physical and economic utilization differ; multi-engine selling is repeatedly observed; Q2 is a real high-ceiling branch.

Weakest claims are: Q2 is universally low priority; Dense Engine Before Expansion as a fixed ordering; clean field as an objective; more Hands implies more money; fixed 7 Cow/4 Sheep.

Counterexamples include Sokolov’s one-quadrant win, X1.14 weed reduction with lower money, the added three-quadrant >$100k paths, and livestock mixes from 4 to 15 cows. Raw files do not directly observe causal payback, marginal animal ROI, economic value of a hand, semantic backlog, or Wheat ledger profit. These require BUILD/counterfactual experiments.

## X1.14 causal counterevidence

Baseline X1.12 is 42,491 / 48,313 on seeds 0 / 421521921. Aggressive workforce B is 39,301 / 36,238 despite 21 weed tile-days; crop-priority C is 31,585 / 35,537 despite 6 weed tile-days; livestock brake D is 31,744 / 35,654. On seed 1273000467, B reaches 54,228 versus X1.12 43,021. Workforce and clean-field interventions are therefore seed- and monetization-dependent. The correct patch is an economic throughput gate, not “hire more” or “remove weeds.”

## Recommended MODEL_SPEC patch plan (not applied)

| Action | Proposed change |
|---|---|
| KEEP | Evidence-vs-rule discipline; throughput, monetization and horizon awareness; Q0-only viability. |
| DOWNGRADE | Q2 not priority, Dense Engine Before Expansion, clean-field minimization, fixed endgame timing. |
| REFRAME | Workforce Capacity First as workload/marginal-throughput fit; Productive Surface First as maintained monetizable capacity; Land Discipline as deployable-capital gate. |
| REMOVE | Universal fixed workforce/livestock counts; structural Q2 rejection. |
| NEEDS_MORE_EVIDENCE | Exact Q2 payback, causal Q2 lift, Wheat trading profit, animal marginal ROI, optimal shutdown. |

## What should not change

Do not hardcode added replay values, make Q2 mandatory, suppress livestock, equate low weeds with profit, or treat peak hands/productive tiles as universal targets. Do not modify strategy or submission based on this review alone.

## Open questions and confidence limitations

The key missing experiment is a paired Q2/no-Q2 control with identical seed, policy and pre-purchase state. Future BUILD work should record activation latency, post-purchase cash, productive tile ramp, task backlog, product sales and liquidation. Confidence is reduced by accidental exposure of forbidden snippets before this file was saved, replay confounding, and lack of causal economic fields in raw observations.

## Environment integrity statement

No environment command, dependency operation, benchmark execution, upload, strategy edit, submission edit, MODEL_SPEC edit, raw JSON edit, branch operation, commit or push was performed. The canonical `.venv` was not changed. The only intended new files are this review and the evidence matrix; pre-existing untracked tests were left untouched.

COPILOT 6-REPLAY MODEL_SPEC CRITICAL REVIEW: COMPLETE

CANONICAL .VENV: UNTOUCHED

STRATEGY CODE: NOT MODIFIED

MODEL_SPEC: NOT MODIFIED - PATCH PLAN ONLY