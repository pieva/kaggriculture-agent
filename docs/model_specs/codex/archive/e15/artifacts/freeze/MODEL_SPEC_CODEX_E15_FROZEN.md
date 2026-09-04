# Codex Independent MODEL_SPEC

Date: 2026-08-29

## Scope

This is the current Codex-owned strategy specification for Kaggriculture E14.
It does not replace or edit other agents' model specs. Historical shared
`docs/model_specs/history/MODEL_SPEC_PRE_C2.md` remains an archive and is not the current Codex source of
truth.

This directory contains Codex-owned strategy intelligence for Kaggriculture.
New Codex work should use this file as the current Codex-specific source of
truth.

## Current Candidate

- Candidate mode: `E12_X115_CODEX_INDEPENDENT`
- Builder: `scripts/build_submission_codex.py`
- Submission artifact: `submission/submission_codex.py`
- Status: buildable Codex candidate, not upload-approved
- Best tested variant: `X115D`
- Local verdict from E12-X1.15: no robust improvement; do not upload without a new economic redesign

The current candidate is deliberately buildable for isolation and forensic
comparison. It is not claimed to be competitive enough for Kaggle upload.

## Primary Evidence

1. `experiments/archive/e12/artifacts/x115_codex/FINAL_REPORT.md`
   - X1.12 mean: `$42,780`
   - Best X1.15 Codex mean: `$26,461`
   - Best X1.15 variant: `X115D`
   - Q1 stayed on Day 12 and Q2 never fired on development seeds
2. `experiments/archive/e13/artifacts/episode_101971376/codex/summary.json`
   - Pietro reward: `$7,123`
   - Harith reward: `$133,049`
   - First material divergence: Day 12
   - Harith sell value: `$171,870`; Pietro sell value: `$83,418`
   - Harith productive action share: `42.56%`; Pietro: `27.39%`
3. `experiments/archive/e13/artifacts/episode_101971376/codex/FORENSIC_REPLAY_ANALYSIS.md`
   - Capacity compounds early; late game amplifies rather than creates the gap
   - Land works only when activated and monetized
   - Livestock, crop and fertilizer revenue are entangled and must be measured together
4. `experiments/archive/e13/artifacts/episode_101971376/codex/EVIDENCE_MATRIX.csv`
   - "More hands", "more land", "more livestock" are only partially supported alone
   - "Economic similarity" between weak and strong trajectories is contradicted

## Economic Thesis

The winning architecture is not "more of one thing". It is a higher conversion
rate from capital and worker time into sold output.

The model must optimize this chain:

capital -> asset purchase -> activated surface/livestock -> maintained output
-> harvest/collection -> market sell -> reinvestable cash

Any parameter that improves only an intermediate metric must be treated as
suspect until it improves final money or a direct leading revenue proxy.

## Complete Parameter / Influence Ranking

| Rank | Factor | Expected Impact | Confidence | Status | Primary Evidence | Codex Action |
|---:|---|---|---|---|---|---|
| 1 | Monetized throughput per worker action | Very High | High | Keep/Reformulate | E13 Harith productive share 42.56% vs Pietro 27.39%; sell value 171870 vs 83418 | Optimize actions only through converted revenue, not raw activity |
| 2 | Deployable capital timing before expansion | Very High | Medium | Add | X1.15 graft never bought Q2; Q1 stayed Day 12; high-side replays show earlier compounding | Measure spendable cash windows separately from end-of-day money |
| 3 | Market revenue breadth and conversion | Very High | High | Keep/Reformulate | E13 Harith sells Wheat Strawberry Fertilizer Milk Wool Melon; Pietro overconcentrated in Wheat/Milk/Wool | Rank asset loops by sold value and lag, not inventory held |
| 4 | Land activation payback | High | Medium | Split | E13 Q2 matters only with productive/logistics action; X1.15 Q2 gate never fired | Separate land purchase from planted/pasture productive activation |
| 5 | Livestock product engine | High | High | Keep/Reformulate | E13 Harith monetized Milk/Wool/Fertilizer strongly; X1.15 sheep suppression lost money | Preserve animal products unless counterfactual proves stronger alternative |
| 6 | Crop surface actually maintained and harvested | High | High | Keep | E13 crop care 1333 vs 259; X1.14 weed cleanup alone regressed | Tie crop allocation to care/harvest/sell capacity |
| 7 | Movement and logistics efficiency | High | Medium | Add | E13 Pietro movement 4936 vs Harith 3464 with lower revenue | Score routes by product completion per movement |
| 8 | Wheat as operating commodity | High | Medium | Reformulate | E13 Harith bought/sold Wheat at lower churn than Pietro; X1.12 sells high Wheat volume | Treat Wheat as feed/liquidity buffer with churn penalty |
| 9 | Elastic hire as capacity purchase | Medium-High | Medium | Reformulate | E13 Pietro 12 hands still lost; Harith 7 hands won; X1.15 more hands did not help | Hire only when expected marginal workload pays back |
| 10 | Endgame liquidation and production shutdown | Medium | Medium | Keep/Split | E13 Day 30 cash-out gap; X1.12 inventory flush matters | Separate stop-plant, sell-through, and animal-product finalization |
| 11 | Fixed herd size constants | Medium | High | Deprecate | Observed strong runs vary herd shape; X1.15 fixed variants fragile | Use caps and marginal ROI envelopes instead of fixed counts |
| 12 | Weed cleanliness as objective | Medium | High | Deprecate | X1.14 reduced weed tile-days but lost money | Use weeds as backlog cost, not target variable |
| 13 | Quadrant count target | Medium | Medium | Reformulate | Q0-only and Q1-only elite runs exist; Q2 high ceiling exists | Branch by payback and liquidity, not required land count |
| 14 | Local-vs-Kaggle fidelity metrics | High | Medium | Add | E13 blind replay exposed local weakness not visible from required seeds | Track divergence day, sell ledger, action mix and asset lag against replays |

## Taxonomy Changes

### Added

- `monetized_throughput_per_worker_action`: primary scoring lens for action policies.
- `deployable_capital_window`: cash available for irreversible purchases after reserved operating needs.
- `land_activation_payback`: payback model for land after purchase, planting, pasture build, harvest/collection and sell-through.
- `route_completion_efficiency`: completed output loops per movement/logistics action.
- `local_kaggle_replay_fidelity`: replay-derived checks for divergence day, market ledger, productive share and asset lag.

### Reformulated

- `hands_target` becomes `elastic_hire_capacity`: HIRE is valid only when marginal workload and horizon justify it.
- `wheat_target` becomes `wheat_operating_commodity`: Wheat is feed, liquidity and market throughput, with churn risk.
- `crop_mix_counts` becomes `horizon_aware_crop_allocation`: crop choice depends on remaining days, care capacity, inventory and sell lag.
- `livestock_targets` becomes `livestock_product_engine`: herd shape is a bounded revenue loop, not a fixed replay copy.
- `quadrant_target` becomes `expansion_payback_branch`: land is optional unless activation and liquidity make it profitable.

### Split

- `Q2_enabled` is split into `Q2_purchase_gate`, `Q2_activation_gate`, `Q2_worker_capacity_gate` and `Q2_sellthrough_gate`.
- `productive_surface` is split into crop surface, pasture surface, maintained surface, harvest-ready surface and monetized surface.
- `endgame` is split into stop-plant, inventory flush, animal-product collection and final sell cadence.

### Deprecated

- Fixed numbers copied from replay trajectories as constants.
- Weed minimization as a standalone objective.
- Peak hands as a standalone objective.
- Raw land ownership as a standalone objective.
- Inventory accumulation without a sell-through plan.

### Removed From Current Codex Reasoning

- Shared `docs/model_specs/history/MODEL_SPEC_PRE_C2.md` as current source of truth. It remains historical only.
- Generic `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py` as Codex candidate artifact. Codex now builds `submission/submission_codex.py`.

## Confirming Evidence

- Harith beats Pietro with fewer final hands but far higher productive share and sell value.
- X1.15 proves that adding Q2 eligibility and more hands to X1.12 does not create a high-ceiling engine.
- X1.14 shows that cleaner fields without revenue conversion are not enough.
- X1.15 sheep collapse correlates with worse monetized product diversity.
- E13 material divergence starts Day 12, so the key difference is compounding structure, not final-day sell timing alone.

## Falsifying Evidence And Warnings

- Q2 is not mandatory: strong compact and Q1-only trajectories exist in the evidence corpus.
- Livestock count is not a magic constant: herd composition varies across strong runs.
- Peak hands can be actively harmful if hires increase movement, idle time, or unmonetized inventory.
- Wheat volume can be profit or churn; it must be evaluated through feed use, sell timing and inventory left behind.
- A buildable candidate is not automatically an upload candidate.

## Open Ablation Hypotheses

1. A capital-first opening that delays discretionary buys until Q1/Q2 activation may beat X1.12.
2. A compact Q0/Q1 branch with stricter route completion may beat Q2 on some seeds.
3. Sheep preservation likely matters more than X1.15 allowed, but the correct cap is seed/horizon dependent.
4. Q2 requires a new opening, not a late graft onto Day-12 Q1.
5. Endgame sell-through should be validated as a separate subsystem from production growth.

## Canonical Ontology Mapping

This mapping adopts the common ontology vocabulary without changing Codex ranking,
confidence, expected impact, causal interpretation or policy. `USED` means the
concept is explicitly used by the Codex MODEL_SPEC; `PARTIAL` means Codex models
only part of the canonical phenomenon or uses a broader local proxy; `NOT_USED`
means the concept remains available in the ontology but is not an independent
Codex modeling factor.

| concept_id | usage | mapping | local_term | model_assessment | evidence/confidence reference |
|---|---|---|---|---|---|
| `land_surface_total` | USED | PARTIAL | quadrant count target / expansion payback branch | Codex treats land count as meaningful only through payback, not as a target by itself. | Ranking #13; Taxonomy Reformulated; Falsifying Evidence |
| `land_purchase_timing` | USED | FULL | deployable capital timing before expansion | Timing of land purchase is a primary economic lever in the Codex thesis. | Ranking #2; Primary Evidence; Open Ablation #1 |
| `activated_land_surface` | USED | FULL | Q2 activation gate / land activation payback | Codex separates purchased land from land that becomes economically active. | Ranking #4; Taxonomy Split |
| `crop_surface_maintained` | USED | FULL | crop surface actually maintained and harvested | Maintained crop surface is treated as a high-impact production condition. | Ranking #6; Taxonomy Split |
| `pasture_surface_maintained` | PARTIAL | PARTIAL | pasture component of productive surface | Codex covers pasture through livestock engine and surface split, but does not rank pasture maintenance as a standalone factor. | Ranking #5; Taxonomy Split |
| `maintained_productive_surface` | USED | FULL | productive surface retained until monetization | Codex distinguishes maintained surface from merely owned or planted surface. | Ranking #6; Taxonomy Split |
| `monetized_productive_output` | USED | FULL | market revenue breadth and conversion | Codex evaluates production by cash conversion, not by raw production alone. | Ranking #3; Confirming Evidence |
| `land_activation_payback` | USED | FULL | land activation payback | Canonical concept directly matches the Codex ranked factor. | Ranking #4; Taxonomy Added |
| `pasture_arable_surface_tradeoff` | PARTIAL | PARTIAL | crop/pasture split in productive surface | Codex recognizes crop versus pasture allocation, but has no independent tradeoff score. | Ranking #5 and #6; Taxonomy Split |
| `workforce_headcount` | USED | PARTIAL | elastic hire as capacity purchase | Headcount matters in Codex only through capacity and marginal payback. | Ranking #9; Taxonomy Reformulated |
| `worker_capacity_available` | USED | FULL | worker capacity gate / elastic hire capacity | Codex models worker capacity as a gate on surface activation and throughput. | Ranking #7 and #9; Taxonomy Split |
| `hire_order_scheduling` | PARTIAL | PARTIAL | elastic hire timing | Codex includes hire elasticity, but not a separate order-slot scheduling model. | Ranking #9; Open Ablation #3 |
| `marginal_hire_payback` | USED | FULL | elastic hire as capacity purchase | Codex explicitly frames hiring as marginal capacity purchase. | Ranking #9; Falsifying Evidence |
| `productive_action_share` | USED | FULL | productive share / route completion | Productive share is a diagnostic for the X1.15 failure and competitor gap. | Primary Evidence; Confirming Evidence |
| `movement_overhead` | USED | FULL | movement and logistics efficiency | Movement cost is a ranked cause of lost throughput. | Ranking #7; Primary Evidence |
| `necessary_transit_fraction` | NOT_USED | ABSENT | none | Codex does not currently separate necessary from avoidable transit. | Ontology verification warning; no Codex ranking entry |
| `routing_completion_efficiency` | USED | FULL | route completion efficiency | Codex treats route completion as a logistics/throughput condition. | Ranking #7; Taxonomy Added |
| `action_dispatch_failure` | PARTIAL | PARTIAL | local-vs-Kaggle fidelity / route failure symptoms | Codex observes failure symptoms but does not isolate dispatch failure as a distinct model factor. | Ranking #14; Primary Evidence |
| `worker_action_monetization_rate` | USED | FULL | monetized throughput per worker action | Canonical concept directly matches the top Codex ranked factor. | Ranking #1; Taxonomy Added |
| `crop_care_action_flow` | PARTIAL | BROADER | crop surface maintained and harvested | Codex covers crop care as part of maintained surface, not as a separate action flow. | Ranking #6 |
| `planting_action_flow` | PARTIAL | BROADER | horizon-aware crop allocation | Planting is modeled through crop allocation and horizon, not as its own flow. | Ranking #6; Taxonomy Reformulated |
| `watering_execution_rate` | PARTIAL | BROADER | crop surface actually maintained | Watering contributes to maintained surface but is not independently ranked. | Ranking #6 |
| `watering_continuity` | PARTIAL | BROADER | crop surface actually maintained | Continuity is implicit in maintenance and harvest readiness. | Ranking #6; Taxonomy Split |
| `crop_harvest_action_flow` | PARTIAL | BROADER | harvest/logistics/selling throughput | Harvesting is included in throughput but not isolated from logistics and selling. | Ranking #1, #6 and #7 |
| `crop_care_completion_rate` | PARTIAL | BROADER | maintained crop surface | Completion rate is approximated by retained/harvested crop surface. | Ranking #6 |
| `crop_decay_risk_window` | NOT_USED | ABSENT | none | Codex warns about maintained surface but has no distinct decay-window model. | No Codex ranking entry |
| `crop_horizon_alignment` | USED | FULL | horizon-aware crop allocation | Canonical concept directly matches the Codex crop allocation reformulation. | Taxonomy Reformulated; Open Ablation #5 |
| `crop_revenue_mix` | USED | FULL | crop allocation / market revenue breadth | Codex includes crop mix as part of revenue breadth and conversion. | Ranking #3 and #6 |
| `feed_availability` | USED | FULL | wheat as operating commodity / feed use | Feed availability is central to the livestock and wheat interpretation. | Ranking #8; Confirming Evidence |
| `feed_security_buffer` | PARTIAL | PARTIAL | wheat operating commodity | Codex covers wheat as operating stock but does not specify a separate buffer target. | Ranking #8; Falsifying Evidence |
| `feed_market_dependency` | USED | PARTIAL | wheat volume can be profit or churn | Codex recognizes feed market dependence through buy/sell/feed interpretation. | Ranking #8; Falsifying Evidence |
| `feed_market_expenditure` | PARTIAL | PARTIAL | wheat operating commodity / market churn | Feed buying cost is acknowledged, but not ranked as an isolated cost factor. | Ranking #8; Falsifying Evidence |
| `wheat_operating_flow` | USED | FULL | wheat as operating commodity | Canonical concept directly matches the Codex wheat reformulation. | Ranking #8; Taxonomy Reformulated |
| `market_churn_cost` | PARTIAL | PARTIAL | wheat volume can be profit or churn | Codex flags churn risk but does not assign a separate cost metric. | Ranking #8; Falsifying Evidence |
| `livestock_headcount` | USED | PARTIAL | fixed herd size constants / livestock product engine | Codex uses herd counts as evidence, while deprecating fixed constants as policy. | Ranking #5 and #11 |
| `livestock_capacity` | PARTIAL | PARTIAL | livestock product engine | Capacity is included through product flow and pasture constraints, but not separated. | Ranking #5 |
| `pasture_capacity_alignment` | PARTIAL | PARTIAL | livestock product engine / pasture surface | Codex covers pasture alignment indirectly through livestock and productive surface. | Ranking #5; Taxonomy Split |
| `livestock_product_flow` | USED | FULL | Milk + Wool + Fertilizer monetization | Livestock product flow is a high-impact Codex economic engine. | Ranking #5; Confirming Evidence |
| `species_margin_differential` | PARTIAL | PARTIAL | Cow + Sheep product engine | Codex distinguishes cattle and sheep evidence but has no independent species-margin model. | Ranking #5; Confirming Evidence |
| `fertilizer_byproduct_flow` | USED | FULL | fertilizer monetization | Fertilizer is explicitly part of the livestock product monetization thesis. | Ranking #5; Confirming Evidence |
| `market_transaction_value` | NOT_USED | ABSENT | none | Codex does not currently model per-transaction value or price provenance as a standalone factor. | Ontology concept; no Codex ranking entry |
| `operating_cash_buffer` | USED | PARTIAL | capital protection / deployable capital window | Codex treats cash buffer as part of deployable capital timing rather than an independent target. | Ranking #2; Open Ablation #1 |
| `deployable_capital_window` | USED | FULL | deployable capital timing before expansion | Canonical concept directly matches a very-high-impact Codex factor. | Ranking #2; Taxonomy Added |
| `asset_liquidity_lag` | PARTIAL | PARTIAL | endgame liquidation / inventory flush | Codex recognizes liquidity lag mainly in endgame and sell-through context. | Ranking #10; Taxonomy Split |
| `inventory_to_cash_conversion` | USED | FULL | market revenue breadth and conversion | Inventory-to-cash conversion is a primary Codex revenue criterion. | Ranking #3 and #10 |
| `market_sellthrough_lag` | USED | PARTIAL | selling throughput / final sell cadence | Codex models sell-through in throughput and endgame, not as a separate lag metric. | Ranking #7 and #10 |
| `unsold_inventory_value` | PARTIAL | PARTIAL | inventory flush / final sell cadence | Unsold inventory is a warning signal within endgame liquidation. | Ranking #10; Falsifying Evidence |
| `reinvestment_cash_flow` | USED | PARTIAL | deployable capital window | Reinvestment flow is implicit in capital timing before expansion. | Ranking #2 |
| `product_mix_revenue` | USED | FULL | market revenue breadth and conversion | Codex evaluates breadth of monetized products as a core economic lever. | Ranking #3 and #5 |
| `price_realization_variance` | NOT_USED | ABSENT | none | Codex does not independently model market price variance. | No Codex ranking entry |
| `dynamic_market_price_elasticity` | NOT_USED | ABSENT | none | Codex does not currently include dynamic market price elasticity as a factor or policy. | Ontology concept; no Codex ranking entry |
| `shed_inventory_integrity` | PARTIAL | PARTIAL | inventory flush / local-vs-Kaggle fidelity | Codex cares about retained inventory only through conversion and fidelity symptoms. | Ranking #10 and #14 |
| `contract_inventory_loss` | NOT_USED | ABSENT | none | Codex does not use contract inventory loss as an explanatory factor. | Ontology concept; no Codex ranking entry |
| `endgame_shutdown_timing` | USED | FULL | endgame production shutdown | Codex explicitly splits stop-plant timing from liquidation cadence. | Ranking #10; Taxonomy Split |
| `endgame_inventory_liquidation` | USED | FULL | inventory flush / final sell cadence | Codex treats final liquidation as a separate subsystem to validate. | Ranking #10; Open Ablation #5 |
| `field_cleanliness_state` | USED | PARTIAL | weed cleanliness as objective | Codex uses cleanliness as a state but deprecates it as a standalone objective. | Ranking #12; Taxonomy Deprecated |
| `weed_backlog_cost` | USED | PARTIAL | weed cleanliness as objective | Codex recognizes weed backlog cost only when tied to productive surface loss. | Ranking #12; Falsifying Evidence |
| `market_order_batch_limit` | NOT_USED | ABSENT | none | Codex does not model order batching limits as a standalone engine constraint. | Ontology concept; no Codex ranking entry |
| `action_order_slot_pressure` | PARTIAL | PARTIAL | peak hands can be harmful | Codex captures slot pressure indirectly through hire harm and throughput loss. | Ranking #9; Falsifying Evidence |
| `state_capacity_alignment` | USED | PARTIAL | worker-land co-scaling / capacity gates | Codex aligns state and capacity through expansion and worker gates, not a single metric. | Ranking #4, #7 and #9 |
| `local_kaggle_fidelity_gap` | USED | FULL | local-vs-Kaggle fidelity metrics | Canonical concept directly matches the Codex diagnostic factor. | Ranking #14; Taxonomy Added |
| `operational_divergence_onset` | USED | PARTIAL | material divergence timing | Codex uses divergence timing diagnostically, not as a ranked economic factor. | Primary Evidence; Ranking #14 |
| `economic_lock_in_onset` | USED | FULL | economic lock-in / failed recovery point | Codex uses lock-in timing to interpret unrecoverable economic gaps. | Primary Evidence; Falsifying Evidence |
| `final_money_outcome` | USED | FULL | final money benchmark outcome | Final money is the main benchmark outcome for candidate validity. | Primary Evidence; Current Candidate |
## Isolation and Validity Rules

- Codex model intelligence lives in `docs/model_specs/codex/MODEL_SPEC.md`.
- Codex build output is exactly `submission/submission_codex.py`.
- Codex may share parser, state, action and Kaggle environment infrastructure.
- Codex must not depend on other-agent strategy directories, benchmark scripts or submission artifacts.
- Other-agent files may be listed as repository contamination risks but not used as model evidence.
