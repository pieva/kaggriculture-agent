# E18.10 — gate 7-7-0 WATER-before-DIG

## Verdetto

Gate A causale: `FAIL`. Gate B Top-3:
`FAIL`. Controllo E18.9; unica mutazione:
DIG protetto → WATER in-place se il crop vivo è unwatered.

## Risultati

| KPI | E18.10 WATER | E18.9 controllo | Delta |
|---|---:|---:|---:|
| Money | 64827.50 | 64519.79 | +0.48% |
| Move | 3612.29 | 3608.43 | +0.11% |
| PASS | 839.71 | 849.14 | -1.11% |
| WATER | 928.00 | 908.86 | +2.11% |
| DIG | 47.00 | 53.07 | -11.44% |
| Crop service | 1576.14 | 1568.57 | +0.48% |
| Late crop tile-days | 508.64 | 482.50 | +5.42% |
| Late unwatered/crop | 0.4579 | 0.4807 | -4.73% |
| Harvest riusciti | 247.07 | 238.36 | +3.66% |
| Unità raccolte | 585.93 | 575.21 | +1.86% |

Opportunità DIG→WATER sui 14 match: `1036`. Topologia candidata:
`0/14`; controllo:
`14/14`. Record:
`8-6`. Delta money matched medio
`-0.08%`, peggiore
`-3.07%`.

## Gate A causale

```json
{
  "crop_service_at_least_1pct_higher": false,
  "dig_not_higher": true,
  "exact_filled_770_candidate_all_matches": false,
  "exact_filled_770_control_all_matches": true,
  "harvest_events_at_least_1pct_higher": true,
  "harvested_units_at_least_1pct_higher": true,
  "late_crop_tile_days_not_lower": true,
  "late_unwatered_at_least_2pct_better": true,
  "livestock_losses_not_above_control": false,
  "money_not_below_control_minus_2pct": true,
  "move_not_above_control_plus_1pct": true,
  "non_water_dimensions_frozen": true,
  "pass_at_least_1pct_lower": true,
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

## Invalidazione safety

La V1 non rappresenta correttamente l'ipotesi preregistrata: il task WATER
poteva sovrascrivere un comando provider non-PASS sullo shed access `(4,5)`.
Il fill finale `13/14` e tre perdite verificate per match rendono il risultato
`INVALID/REJECTED`. I delta crop non sono utilizzabili per una promozione.
