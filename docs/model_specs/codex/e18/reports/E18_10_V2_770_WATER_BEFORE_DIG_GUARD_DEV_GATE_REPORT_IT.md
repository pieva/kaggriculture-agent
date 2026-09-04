# E18.10 V2 — safe PASS-only WATER-before-DIG

## Verdetto

Gate A causale: `FAIL`. Gate B Top-3:
`FAIL`. La V2 converte soltanto un PASS
finale di E18.9 in WATER in-place ed esclude lo shed access `(4,5)`.

## Risultati

| KPI | E18.10 V2 | E18.9 controllo | Delta |
|---|---:|---:|---:|
| Money | 65556.43 | 64460.21 | +1.70% |
| Move | 3601.79 | 3609.71 | -0.22% |
| PASS | 849.71 | 847.86 | +0.22% |
| WATER | 924.93 | 908.86 | +1.77% |
| DIG | 47.00 | 53.07 | -11.44% |
| Crop service | 1576.50 | 1568.57 | +0.51% |
| Late crop tile-days | 507.64 | 482.50 | +5.21% |
| Late unwatered/crop | 0.4610 | 0.4807 | -4.10% |
| Harvest riusciti | 242.57 | 238.36 | +1.77% |
| Unità raccolte | 578.57 | 575.21 | +0.58% |

PASS→WATER totali sui 14 match: `210`. Topologia/fill candidata:
`14/14`; controllo:
`14/14`. Record:
`12-2`. Delta money matched medio
`+1.46%`, peggiore
`-0.05%`.

## Gate A causale

```json
{
  "crop_service_at_least_1pct_higher": false,
  "dig_not_higher": true,
  "exact_filled_770_candidate_all_matches": true,
  "exact_filled_770_control_all_matches": true,
  "harvest_events_at_least_1pct_higher": true,
  "harvested_units_at_least_1pct_higher": false,
  "late_crop_tile_days_not_lower": true,
  "late_unwatered_at_least_2pct_better": true,
  "livestock_losses_not_above_control": true,
  "money_not_below_control_minus_2pct": true,
  "move_not_above_control_plus_1pct": true,
  "non_water_dimensions_frozen": true,
  "pass_at_least_1pct_lower": false,
  "water_at_least_1pct_higher": true,
  "water_conversion_activated_all_matches": true,
  "worst_matched_money_delta_at_least_minus_5pct": true,
  "zero_errors_and_fallbacks": true,
  "zero_provider_non_pass_overrides": true,
  "zero_q2_pastures_candidate": true,
  "zero_topology_breaches": true,
  "zero_worker_route_mutations": true
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

## Interpretazione causale

La correzione PASS-only conserva la safety e conferma la direzione WATER:
meno DIG, meno stress idrico, superficie attiva più a lungo, più harvest e
meno move. Il gate non passa perché l'intervento su quattro target ha volume
insufficiente su crop service, unità e PASS. E18.10 V2 è il nuovo best research
770, non una candidata autorizzata per holdout o upload.
