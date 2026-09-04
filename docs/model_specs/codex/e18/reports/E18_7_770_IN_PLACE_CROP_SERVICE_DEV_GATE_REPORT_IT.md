# E18.7 — gate 7-7-0 in-place crop service

## Verdetto

Gate A causale: `FAIL`. Gate B di
convergenza Top-3: `FAIL`. Entrambi gli
agenti usano la stessa topologia `7-7-0`; l'unica mutazione è PASS → HARVEST o
WATER immediato sulla cella corrente.

## Risultati

| KPI | E18.7 service | E18.6 controllo | Delta |
|---|---:|---:|---:|
| Money | 63714.79 | 63714.79 | +0.00% |
| Comandi unità | 7519.00 | 7519.00 | +0.00% |
| Move | 3607.14 | 3607.14 | +0.00% |
| PASS | 844.93 | 846.93 | -0.24% |
| Produttive normalizzate | 3066.93 | 3064.93 | +0.07% |
| Move/prod. normalizzato | 1.1761 | 1.1769 | -0.07% |
| Crop service | 1576.93 | 1574.93 | +0.13% |
| Harvest riusciti | 233.43 | 233.43 | +0.00% |
| Unità raccolte | 560.14 | 560.14 | +0.00% |
| Late unwatered/crop | 0.4783 | 0.4783 | +0.00% |

Topologia/fill candidata: `14/14`; controllo:
`14/14`. Record: `1-1`.
Perdite verificate: `14` contro
`14`. Delta money matched medio
`+0.00%`, peggiore
`-1.27%`.

## Gate A causale

```json
{
  "crop_service_at_least_5pct_higher": false,
  "exact_filled_770_candidate_all_matches": true,
  "exact_filled_770_control_all_matches": true,
  "harvest_events_at_least_5pct_higher": false,
  "harvested_units_at_least_5pct_higher": false,
  "late_unwatered_at_least_5pct_better": false,
  "livestock_losses_not_above_control": true,
  "money_not_below_control_minus_5pct": true,
  "move_not_above_control_plus_1pct": true,
  "non_service_dimensions_frozen": true,
  "normalized_productive_at_least_3pct_higher": false,
  "normalized_ratio_at_least_3pct_better": false,
  "pass_at_least_5pct_lower": false,
  "treatment_activated_all_matches": true,
  "worst_matched_money_delta_at_least_minus_10pct": true,
  "zero_cross_quadrant_routes": true,
  "zero_errors_and_fallbacks": true,
  "zero_non_pass_overrides": true,
  "zero_q2_pastures_candidate": true,
  "zero_service_distance": true,
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

Due soli WATER aggiuntivi non spiegano il gap Top-3. Il PASS replacement
in-place è meccanicamente sicuro, ma non è una leva sufficiente.
