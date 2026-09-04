# E18.9 — gate 7-7-0 live-crop rotation guard

## Verdetto

Gate A causale: `FAIL`. Gate B Top-3:
`FAIL`. L'unica mutazione è la soppressione
del DIG calendarizzato su un crop reclaimed ancora vivo; nessun worker è
reroutato.

## Risultati

| KPI | E18.9 guard | E18.6 controllo | Delta |
|---|---:|---:|---:|
| Money | 64022.86 | 63716.64 | +0.48% |
| Move | 3612.21 | 3604.50 | +0.21% |
| PASS | 844.86 | 849.79 | -0.58% |
| DIG | 53.07 | 56.14 | -5.47% |
| Crop service | 1568.93 | 1574.71 | -0.37% |
| Late crop tile-days | 482.29 | 459.64 | +4.93% |
| Late unwatered/crop | 0.4805 | 0.4785 | +0.41% |
| Harvest riusciti | 238.71 | 233.29 | +2.33% |
| Unità raccolte | 575.57 | 560.00 | +2.78% |

Opportunità DIG soppresse sui 14 match: `2982`. Topologia candidata:
`14/14`; controllo:
`14/14`. Record:
`10-4`. Delta money matched medio
`+0.49%`, peggiore
`-0.95%`.

## Gate A causale

```json
{
  "dig_at_least_10pct_lower": false,
  "exact_filled_770_candidate_all_matches": true,
  "exact_filled_770_control_all_matches": true,
  "guard_activated_all_matches": true,
  "harvest_events_at_least_5pct_higher": false,
  "harvested_units_at_least_5pct_higher": false,
  "late_crop_tile_days_at_least_5pct_higher": false,
  "late_unwatered_not_worse_than_plus_2pct": true,
  "livestock_losses_not_above_control": true,
  "money_not_below_control_minus_3pct": true,
  "move_not_above_control_plus_1pct": true,
  "non_rotation_dimensions_frozen": true,
  "pass_not_above_control_plus_1pct": true,
  "worst_matched_money_delta_at_least_minus_7_5pct": true,
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
  "late_crop_tile_days_at_least_500": false,
  "late_unwatered_at_most_0_42": false,
  "move_at_most_3500": false,
  "normalized_ratio_at_most_1_10": false,
  "pass_at_most_600": false
}
```

Holdout, final e upload Kaggle non sono autorizzati.

## Interpretazione causale

Il gate non è superato e non autorizza promozione, ma è il primo trattamento
770 con direzione economica e agronomica positiva senza churn delle
traiettorie. La prossima ablation resta locale: DIG protetto → WATER in-place
soltanto quando il crop vivo è unwatered.
