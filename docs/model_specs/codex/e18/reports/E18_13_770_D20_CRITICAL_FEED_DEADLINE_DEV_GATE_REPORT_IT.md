# E18.13 — D20 critical FEED deadline

## Verdetto

Gate A causale: `FAIL`. Gate B Top-3:
`FAIL`. Controllo E18.10 V2; unica
mutazione: a D20 un MOVE viene ritardato di un turno per eseguire FEED in-place
su un animale già critico, con Wheat già trasportato dal worker.

## Risultati

| KPI | E18.13 | E18.10 V2 | Delta |
|---|---:|---:|---:|
| Money | 65265.93 | 65049.64 | +0.33% |
| Loss bestiame verificati | 0 | 14 | n/a |
| FEED | 335.00 | 335.00 | +0.00% |
| Move | 3607.86 | 3603.21 | +0.13% |
| PASS | 846.43 | 848.14 | -0.20% |
| WATER | 925.93 | 924.93 | +0.11% |
| Crop service | 1577.71 | 1576.64 | +0.07% |
| Late crop tile-days | 507.64 | 507.50 | +0.03% |
| Late unwatered/crop | 0.4570 | 0.4608 | -0.82% |
| Harvest riusciti | 242.79 | 242.71 | +0.03% |
| Unità raccolte | 579.79 | 578.71 | +0.19% |

Override FEED totali: `14`. Topologia/fill candidata:
`14/14`; controllo:
`14/14`. Record:
`6-8`. Delta money matched medio
`-0.37%`, peggiore
`-2.85%`.

## Gate A causale

```json
{
  "control_loss_reproduced_each_match": true,
  "crop_service_not_lower_by_more_than_0_5pct": true,
  "exact_filled_770_candidate_all_matches": true,
  "exact_filled_770_control_all_matches": true,
  "feed_not_lower": true,
  "harvest_events_not_lower_by_more_than_0_5pct": true,
  "harvested_units_not_lower_by_more_than_0_5pct": true,
  "late_unwatered_not_worse_by_more_than_0_5pct": true,
  "money_not_below_control": true,
  "move_not_higher_by_more_than_0_5pct": true,
  "non_target_dimensions_frozen": true,
  "one_critical_feed_override_each_match": true,
  "only_one_route_delay_each_match": true,
  "water_not_lower_by_more_than_0_5pct": true,
  "worst_matched_money_delta_at_least_minus_2pct": false,
  "zero_candidate_livestock_losses": true,
  "zero_errors_and_fallbacks": true,
  "zero_infeasible_or_non_move_overrides": true,
  "zero_q2_pastures_candidate": true,
  "zero_topology_breaches": true
}
```

## Gate B Top-3

```json
{
  "crop_service_at_least_1800": false,
  "harvest_events_at_least_300": false,
  "late_crop_tile_days_at_least_500": true,
  "late_unwatered_at_most_0_42": false,
  "move_at_most_3500": false,
  "normalized_ratio_at_most_1_10": false,
  "pass_at_most_600": false
}
```

Holdout, final e upload Kaggle non sono autorizzati.
