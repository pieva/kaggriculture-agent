# Cross-Competitor Analysis

## Comparative Table

| Episode | Seed | Competitor | Our score | Competitor score | Gap | Ratio | Q1 day | Q2 | Peak hands | Peak productive | Weed tile-days | Final livestock | Main sells |
|---|---:|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| `101294736` | `421521921` | truebelief | `$6,825` | `$86,297` | `$79,472` | `12.644` | 11 | no | 12 | 50 | 10 | `9 Cow / 5 Sheep` | Wheat, Fertilizer, Milk, Melon, Wool |
| `101705751` | `1056561958` | Dr. Mikholae Hutchinson | `$38,815` | `$90,137` | `$51,322` | `2.322` | 14 | no | 10 | 46 | 11 | `7 Cow / 4 Sheep / 2 Goose` | Fertilizer, Milk, Strawberry, Wheat, Egg |
| `101717011` | `1273000467` | Alexander Sokolov | `$24,314` | `$50,420` | `$26,106` | `2.074` | n/a | no | 8 | 15 | 145 | `4 Cow / 2 Sheep` | Wheat, Milk, Fertilizer, Carrot, Wool |

## Shared Patterns

- Q2 is absent across all benchmark competitors; high scores and a direct win over us are possible without a third quadrant.
- Productive capacity must be matched to maintainable workload. Elite Q0+Q1 runs peak at `50` and `46` productive tiles; the compact one-quadrant win peaks at only `15` productive tiles but monetizes densely.
- Workforce should be workload-derived rather than copied: peak hands are `12`, `10` and `8`.
- Revenue is diversified across crop products, animal products and Fertilizer.
- Livestock is part of the engine, but it is balanced with crop maintenance and logistics throughput.
- Land expansion is not an invariant. The third replay beats our two-quadrant run using only `NW`.

## Variable Patterns

- Q1 usage differs: truebelief reaches Q1 on Day 11, Dr. Mikholae Hutchinson on Day 14, Alexander Sokolov never buys Q1.
- Livestock mix differs: high-density compact Cow+Sheep vs larger Cow+Sheep vs Cow+Sheep+Goose.
- Crop/sell mix differs materially: truebelief sells more Wheat/Melon/Wool; Hutchinson sells more Fertilizer/Strawberry/Egg.
- Peak hands range from `8` to `12` and cannot be treated as a copied constant.
- Weed tolerance differs: elite >86k replays stay near zero, while the compact one-quadrant win tolerates `145` weed tile-days but still out-earns our `$24,314`.

## Specific Patterns

- truebelief-specific: larger Cow/Sheep final inventory and heavier Wheat/Melon/Wool sales.
- Hutchinson-specific: Goose/Egg channel and very high Fertilizer monetization.
- Sokolov-specific: one-quadrant density, very high Wheat sales (`756`), moderate livestock (`4 Cow / 2 Sheep`) and a score that doubles our two-quadrant result on the same seed.
- Our `101294736` side-specific failure: buys Q2 on Day 8 with only `$295`, `8` crop tiles and `6` hands, then finishes at `$6,825`.
- Our `101705751` side-specific failure: stays Q0+Q1 with livestock but accumulates `158` weed tile-days, indicating throughput/backlog breakdown rather than a pure land-expansion issue.
- Our `101717011` side-specific failure: buys Q1 on Day 12 and reaches more peak productive area (`32`) than Sokolov (`15`), but converts it poorly and ends at `$24,314`.

## Evidence State

Q2: `CONSISTENT REJECTION` as a near-term required target in this batch. All three competitors avoid Q2; two exceed `$86k`, and one beats us with a single quadrant.

Q1: `MIXED EVIDENCE` as a required target. Q1 supports elite scores in two replays, but `101717011` proves compact one-quadrant play can beat our current two-quadrant policy.

Livestock: `INFERRED` as capacity/ROI-gated engine. Suppression is rejected by X1.13 verification; fixed counts are rejected by cross-replay variation.

Workforce: `INFERRED` as workload-derived throughput. Fixed schedules are weaker than a capacity model tied to crop, livestock, logistics and backlog.

Capital deployment: `INFERRED`. The model needs deployable capital, not raw cash, to decide HIRE, livestock, Q1 and conditional Q2. The new replay strengthens this: spending on Q1 can lose to denser single-quadrant compounding.
