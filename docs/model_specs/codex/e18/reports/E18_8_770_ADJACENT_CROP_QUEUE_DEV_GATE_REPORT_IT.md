# E18.8 — gate 7-7-0 adjacent crop queue

## Verdetto

Gate A causale: `FAIL`. Gate B di
convergenza Top-3: `FAIL`. La topologia è
`7-7-0` per entrambi; l'unica mutazione è PASS → missione crop adiacente nello
stesso quadrante.

## Risultati

| KPI | E18.8 queue | E18.6 controllo | Delta |
|---|---:|---:|---:|
| Money | 58920.50 | 69931.71 | -15.75% |
| Move | 3691.86 | 3601.79 | +2.50% |
| PASS | 705.50 | 852.64 | -17.26% |
| Produttive normalizzate | 3121.64 | 3064.57 | +1.86% |
| Move/prod. normalizzato | 1.1827 | 1.1753 | +0.63% |
| Crop service | 1589.93 | 1574.64 | +0.97% |
| Harvest riusciti | 158.64 | 233.14 | -31.95% |
| Unità raccolte | 400.86 | 559.64 | -28.37% |
| Late unwatered/crop | 0.4393 | 0.4783 | -8.15% |

Missioni totali sui 14 match: `1372` assegnate,
`240` completate, `1132` cancellate. Topologia
candidata: `14/14`; controllo:
`14/14`. Record:
`0-14`. Delta money matched medio
`-15.59%`, peggiore
`-24.12%`.

## Gate A causale

```json
{
  "assignment_distance_at_most_one": true,
  "crop_service_at_least_5pct_higher": false,
  "exact_filled_770_candidate_all_matches": true,
  "exact_filled_770_control_all_matches": true,
  "harvest_events_at_least_5pct_higher": false,
  "harvested_units_at_least_5pct_higher": false,
  "late_unwatered_at_least_5pct_better": true,
  "livestock_losses_not_above_control": true,
  "money_not_below_control_minus_5pct": false,
  "move_not_above_control_plus_3pct": true,
  "non_queue_dimensions_frozen": true,
  "normalized_productive_at_least_3pct_higher": false,
  "normalized_ratio_not_worse": false,
  "pass_at_least_5pct_lower": true,
  "treatment_activated_all_matches": true,
  "worst_matched_money_delta_at_least_minus_10pct": false,
  "zero_cross_quadrant_routes": true,
  "zero_errors_and_fallbacks": true,
  "zero_non_pass_overrides": true,
  "zero_q2_pastures_candidate": true,
  "zero_topology_breaches": true
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

Holdout, final e upload Kaggle non sono autorizzati da questo gate.

## Interpretazione causale

La riduzione dei PASS è ingannevole se ottenuta spostando worker fuori dalle
missioni implicite del provider. L'alto tasso di cancellazione della queue
spiega il crollo di harvest e money: questa architettura è respinta.
