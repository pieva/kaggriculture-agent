# E12-X1.9 Competitive Gap Audit vs truebelief

Seed audited locally: 421521921.

Replay observation:
- X1.9: 6,825
- truebelief: 86,297

Local reproduction:
- X1.9 local final money: 8,714
- Provenance gap: local behavior does not exactly match the Kaggle replay final money, but reproduces the same qualitative failure mode: Q0 opens well, Q1/Q2 are bought, then productive surface collapses and land remains underused.

Key local milestones:

| Day | Money | Land | Crops | Pastures | Animals | Utilization | Radius-5 util |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 2,753 | NW | 21 | 4 | 0 | 1.000 | 1.000 |
| 2 | 741 | NW+NE | 26 | 8 | 0 | 0.680 | 0.688 |
| 5 | 1,558 | NW+NE | 18 | 8 | 0 | 0.520 | 0.542 |
| 8 | 289 | NW+NE+SW | 16 | 8 | 0 | 0.320 | 0.358 |
| 10 | 604 | NW+NE+SW | 8 | 8 | 0 | 0.213 | 0.239 |
| 15 | 465 | NW+NE+SW | 8 | 8 | 0 | 0.213 | 0.239 |
| 20 | 8,066 | NW+NE+SW | 14 | 8 | 6 | 0.293 | 0.328 |
| 25 | 7,591 | NW+NE+SW | 2 | 8 | 8 | 0.133 | 0.149 |
| 30 | 8,714 | NW+NE+SW | 11 | 8 | 8 | 0.253 | 0.284 |

Primary root causes:
- Land is purchased but not activated.
- Harvested crops are often not replanted.
- Working set collapses after Q1/Q2 instead of expanding.
- Crop mix is too narrow: no Tomato or Strawberry; Wheat and Carrot dominate tile-days.
- Livestock reaches 8 cows but is late and economically weak.
- Placement misses the requested core B: 4 cows in core A, 3 in core B, 1 off-core.

Generated files:
- e12_x19_truebelief_gap_audit.json
- daily_metrics.csv
- milestones.csv
- tile_timeline.csv
- land_events.csv
- animal_events.csv
