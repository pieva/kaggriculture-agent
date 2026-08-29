# Copilot vs Codex vs Antigravity: MODEL_SPEC Review

## Scope and process

Copilot first saved `COPILOT_MODEL_SPEC_CRITICAL_REVIEW_6REPLAY.md` and its matrix, then read the existing Codex and Antigravity artifacts. A targeted search had accidentally exposed snippets of those artifacts before the Copilot file was saved; this limitation is recorded in the Copilot review. No strategy, submission, MODEL_SPEC, raw JSON or environment file was changed.

## Overall convergence

All three reviews agree that fixed workforce counts and fixed livestock targets are not portable rules, that livestock products and multi-engine monetization matter, and that replay correlation is not causal proof of payback, HIRE value or Wheat profit. All agree that the original three-replay Q2 conclusion cannot be applied unchanged to the current six-file corpus.

## Major divergences

| Claim | Copilot | Codex | Antigravity/Gemini | Raw evidence | Divergence cause | Recommended human resolution |
|---|---|---|---|---|---|---|
| Q2 not priority | PARTIALLY_SUPPORTED: not universal, not rejected | MIXED: conditional high-ceiling | CONTRADICTED / “mandatory for >100k” | First three competitors avoid Q2; three added episodes use Q2 and score 96,069-133,035 | Interpretive; Antigravity overstates necessity from selected top tier | Reframe as observed high-ceiling branch, not universal requirement. |
| Q2 causal value | Causal-required | Causal caution | Strong positive architectural conclusion | Q2 timing, cash and later score are observed, matched no-Q2 control is absent | Causal confidence | Keep Q2 testable and conditional; do not claim Q2 caused score. |
| Dense Engine Before Expansion | MIXED | PARTIALLY_SUPPORTED | PARTIALLY_SUPPORTED, but fast expansion favored | Sokolov is compact Q0; Q2 paths expand Day 5-10 and reach 75 productive tiles | Interpretation of “before” | Replace strict ordering with monetizable density during expansion. |
| Workforce Capacity First | PARTIALLY_SUPPORTED | MIXED | PARTIALLY_SUPPORTED, high workforce emphasized | Winning peaks 8/10/12; X1.14 aggressive variant regresses required seeds | Interpretation and causal caution | Define capacity as workload and monetizable throughput fit, not more hands. |
| Fixed workforce schedule | CONTRADICTED | NOT_SUPPORTED | PARTIALLY_SUPPORTED heuristic | Peaks and timing vary; no single count explains score | Different threshold for “schedule useful” vs “universal” | Remove universal target; retain schedules only as candidate heuristics. |
| Productive surface | PARTIALLY_SUPPORTED | MIXED | SUPPORTED as 75-tile elite trait | 15-tile Sokolov wins mid-tier; Q2 elites reach 75 | Tier framing | Separate compact-density and large-scale-throughput archetypes. |
| Backlog / weeds | PARTIALLY_SUPPORTED | SUPPORTED | MIXED / secondary constraint | Elite runs low weeds; Sokolov tolerates 145; X1.14 clean variants lose money | Correlation versus objective | Keep backlog as operating constraint; reject weed minimization as standalone goal. |
| Crop SLA before expansion | Not separately classified | PARTIALLY_SUPPORTED | NOT_SUPPORTED | Expansion can coexist with low but nonzero weeds; X1.14 priority can regress | Wording ambiguity and metric choice | Require serviceability, not zero-weeds blocking. |
| Livestock as economic engine | SUPPORTED | SUPPORTED | SUPPORTED, primary engine | Repeated Milk/Wool/Egg/Fertilizer sales and varied herds | Confidence only | Keep engine claim, retain causal/seed caveat on marginal mix. |
| Day-1 livestock opening | Not elevated to a universal claim | Not elevated to a universal claim | SUPPORTED / “universal top-tier” | Several added trajectories and Sokolov buy animals early | Sample generalization; exact player/action parsing | Record as observed elite pattern, not fixed rule, until broader corpus. |
| Deployable Capital | PARTIALLY_SUPPORTED | NOT_OBSERVABLE | NOT_OBSERVABLE | Cash and land actions are raw; reserves/payback are not | Classification boundary between concept and measurement | Keep as inferred design variable, not observed metric; require ledger. |
| Wheat loop | PARTIALLY_SUPPORTED | MIXED | PARTIALLY_SUPPORTED / complex | Buy and sell volumes are observed; net volumes differ | Parsing/ledger availability | Do not call waste or profit without prices, inventory and timing ledger. |
| Horizon-aware shutdown | PARTIALLY_SUPPORTED | PARTIALLY_SUPPORTED low confidence | PARTIALLY_SUPPORTED, late hands retained | Different competitors stop planting or retain hands late | Endgame interpretation | Audit last 2-3 days before adopting a rule. |

## Corpus and parsing differences

Antigravity's main Q2 claim is based on the added six-replay corpus, but its language changes from “all six top-player runs” to “all >$100k runs” and then to “mandatory for >$100k.” Those are different claims: the corpus shows association in this sample, not necessity. Codex is more conservative and Copilot keeps the causal distinction explicit.

The old three-replay registry uses Pietro-specific `our` versus `competitor` labels. The added episodes contain no Pietro side, so those labels must not be used to infer policy quality. The raw evidence should use player/team names and both trajectories. Weed and productive metrics are parser-derived; Wheat BUY_PRODUCT/SELL and endgame intent require a transaction ledger.

## Differences caused by evidence scope

Antigravity's earlier conclusions were shaped by the first three replay files and correctly described Q2 absence in that subset. Codex and the current Copilot review include `101462495`, `101761797` and `101891362`, which contain Q2 and three-quadrant high scores. This is a corpus difference, not simply an agent error. Any three-replay statement must be labeled subset-local.

## Differences caused by interpretation

The same evidence supports “Q2 has a successful high-ceiling observation” but does not support “Q2 is required,” “Q2 caused the score,” “Day 1 livestock is universal,” or “75 tiles are necessary.” Copilot therefore uses SUPPORTED for the branch and PARTIALLY_SUPPORTED/MIXED for stronger causal or universal formulations.

## Unified human resolution

1. Keep evidence-versus-causality discipline from all three reviews.
2. Replace structural Q2 rejection with: “Q2 is a conditional high-ceiling branch observed in the expanded corpus; it is not universally required.”
3. Split the observed architectures into compact Q0, Q0+Q1, and Q0+Q1+Q2 throughput branches.
4. Treat workforce, land, livestock and crop maintenance as coupled throughput decisions.
5. Keep fixed counts, zero-weed objectives, Wheat waste claims and optimal shutdown out of the model until counterfactual or ledger evidence exists.
6. Do not copy Day 5-6 Q1, Day 8-10 Q2, 12 hands, 75 tiles or any specific herd as hard parameters.

## Unresolved questions

- Does Q2 improve X1.12 under matched seeds and pre-purchase state?
- Does the compact Q0 branch generalize beyond seed `1273000467`?
- What are the marginal values of Cow, Sheep and Goose per worker-action?
- Is Wheat trading profitable after complete price/inventory reconstruction?
- Should hands remain through the final hours when harvest, care and selling queues exist?

## Final comparison verdict

Codex provides the most balanced six-replay scope. Antigravity contributes useful detailed Q2 and endgame observations but overstates several universal conclusions. Copilot agrees with Codex on the evidence update while preserving Antigravity's causal caution and explicitly recording the blind-review contamination. No automatic winner is selected; the proposed human resolution is the conservative synthesis above.