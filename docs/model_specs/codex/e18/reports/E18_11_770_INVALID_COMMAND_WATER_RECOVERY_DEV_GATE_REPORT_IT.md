# E18.11 — invalid-command WATER recovery

## Verdetto

Gate A causale: `FAIL`. Gate B Top-3:
`FAIL`. Controllo E18.10 V2; unica
mutazione: comando locale noto e infeasible → WATER in-place su crop secco.

## Risultati

| KPI | E18.11 | E18.10 V2 | Delta |
|---|---:|---:|---:|
| Money | 65220.07 | 65220.07 | +0.00% |
| Move | 3602.36 | 3602.36 | +0.00% |
| PASS | 852.00 | 849.00 | +0.35% |
| WATER | 933.93 | 924.93 | +0.97% |
| Crop service | 1581.64 | 1576.64 | +0.32% |
| Late crop tile-days | 507.50 | 507.50 | +0.00% |
| Late unwatered/crop | 0.4608 | 0.4608 | +0.00% |
| Harvest riusciti | 242.71 | 242.71 | +0.00% |
| Unità raccolte | 578.71 | 578.71 | +0.00% |

Conversioni totali: `168` (`{"FERTILIZE": 112, "HARVEST": 42, "PLANT": 14}`).
Topologia/fill candidata: `14/14`; controllo:
`14/14`. Record:
`1-1`. Delta money matched medio
`+0.00%`, peggiore
`-0.36%`.

## Gate A causale

```json
{
  "crop_service_at_least_0_5pct_higher": false,
  "dig_not_higher": true,
  "exact_filled_770_candidate_all_matches": true,
  "exact_filled_770_control_all_matches": true,
  "harvest_events_not_lower": true,
  "harvested_units_not_lower": true,
  "late_crop_tile_days_not_lower": true,
  "late_unwatered_at_least_1pct_better": false,
  "livestock_losses_not_above_control": true,
  "money_not_below_control_minus_2pct": true,
  "move_not_above_control": true,
  "non_water_dimensions_frozen": true,
  "recovery_activated_all_matches": true,
  "water_at_least_1pct_higher": false,
  "worst_matched_money_delta_at_least_minus_5pct": true,
  "zero_errors_and_fallbacks": true,
  "zero_feasible_provider_overrides": true,
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
