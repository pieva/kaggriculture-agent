# E12-X1.15-COPILOT - Implementation Hypothesis

Candidate: `E12_X115_COPILOT_INDEPENDENT`

## Evidence used

1. OBSERVED: X1.12 reproduces `$42,491` on seed `0` and `$48,313` on `421521921` in its verified harness.
2. OBSERVED: strong replay trajectories span Q0-only, Q0+Q1 and Q0+Q1+Q2; Q2 is a high-ceiling branch, not a universal target.
3. OBSERVED: competitive peak workforce varies, so a copied hand count is not a policy invariant.
4. OBSERVED: compact one-quadrant play can beat a larger but poorly monetized footprint.
5. OBSERVED: livestock products, fertilizer, crops and Wheat are jointly sold by strong trajectories.
6. OBSERVED: X1.14 reduces weeds while reducing final money on required seeds.
7. OBSERVED: X1.12's midgame gap is low crop surface relative to its animal and logistics workload.
8. OBSERVED: a failed Q2 bolt-on did not activate Q2 because capital and recovery were consumed after Q1.
9. OBSERVED: a prior independent 3Q candidate improved aggregate development and holdout means, but its results are not treated as specifications.

## Bottleneck diagnosis

INFERRED: the controlling X1.12 bottleneck is not a single livestock or land constant. It is the interaction of calendar hires, delayed productive footprint, animal-care logistics and expansion cash. The current worker dispatcher can spend many turns servicing animals and shed movement before adding enough crop throughput. A candidate that only increases Hands or only lowers weeds is contradicted by X1.14.

## Policy architecture

X1.15 uses a separate decision method and reuses only general state/action helpers from the shared agent. It has three operational phases:

- Foundation: preserve a productive crop/pasture core, hire only to a modest observed workload envelope, and buy a small early animal seed rather than committing to a fixed herd.
- Capacity release: permit Q1 and then Q2 only when the current surface has active crop/pasture work, cash remains above an operating reserve, and the new quadrant can be built immediately. The gate is deliberately state-based rather than a fixed day target.
- Harvest conversion: sell non-feed outputs promptly, keep Wheat for animal demand, stop planting near the horizon, and retain workers when they can still convert ready crop/animal output.

The implementation will test a conservative Q2 branch against the X1.12 baseline. It will not force Q2, 12 Hands, 75 tiles or a fixed livestock mix.

## Opening

INFERRED: use the existing diversified seed opening because it is reproducible in the local implementation and preserves cash for capacity. Buy one Cow only after pasture exists and the first crop core is active. This intentionally tests whether earlier livestock cash flow helps without assuming livestock-first is mandatory.

## Workforce logic

INFERRED: desired hands are derived from active crops, animals and unfinished pasture work, capped by a conservative six-hand operating envelope in Q0/Q1 and a larger envelope only after Q2. Hire at the day boundary only when cash reserve and remaining horizon support it. The causal test is whether this reduces idle/pass and improves final money, not whether peak Hands increases.

## Livestock logic

INFERRED: grow Cow and Sheep exposure gradually, with Wheat/feed reserve and pasture availability gates. Do not use fixed final targets. Pause animal purchases when active crop work is below a minimum or when the expansion reserve would be consumed.

## Q1/Q2 logic

INFERRED: Q1 can be purchased when cash is at least the land cost plus reserve, active crop/pasture work is already present, and the current worker envelope is not saturated. Q2 is optional and requires Q1, a larger crop footprint, controlled weeds/unwatered work, and enough cash for immediate activation. These are economic proxies, not causal proof.

## Monetization and logistics

INFERRED: sell Milk, Wool, Fertilizer and harvest crops whenever in the shed; sell only Wheat above a feed reserve. Preserve the existing nearest-target reservation behavior for movement, feed, care, harvest and placement so this experiment isolates capital and workload decisions rather than copying another agent's routing.

## Endgame

INFERRED: no new planting after the late horizon threshold; continue harvest, animal care and liquidation while output exists. Avoid a universal worker shutdown because replay endgames vary.

## Why it could beat X1.12

The candidate changes the interaction between capital release and workload without changing the baseline mode. It may activate more surface before the delayed X1.12 Q1 gate, while preventing the premature low-cash expansion failure observed in the corpus. The direct test is matched-harness final money on four development seeds.

## Risks and falsifiers

- The current shared file contains pre-existing X1.15 Codex/Antigravity modes. They were not used as design sources; the candidate must use its own method and name.
- Reusing X1.12 routing may leave the true throughput bottleneck unchanged.
- Early expansion can recreate the `$6,825` failure if reserve accounting is wrong.
- A six-hand cap may underfund the three-quadrant branch.
- Seed-specific market dynamics may make one expansion rule look robust.
- The candidate is not eligible for holdout or upload unless development gains are robust, tests pass and standalone equivalence is independently verified.

## Causal-to-test questions

- Does state-gated early capacity release improve final money without a systematic low-cash collapse?
- Does retaining a feed reserve preserve livestock monetization while freeing capital for crops and land?
- Does a larger worker envelope after Q2 convert more surface into cash, or merely add movement cost?
