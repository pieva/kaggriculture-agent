# E18.27 — confronto interno D10-D15

Confronti matched sul parent E18.26; seed e seat identici contro lo stesso avversario. Nessun holdout o upload.

| Avversario | Seed | Seat | E18.26 | E18.27 | Delta |
|---|---:|---:|---:|---:|---:|
| E18.16 | 180903001 | 0 | 54761.0 | 74287.0 | +19526.0 |
| E18.16 | 180903001 | 1 | 53968.0 | 74287.0 | +20319.0 |
| E18.25 | 180903001 | 0 | 63172.0 | 76408.0 | +13236.0 |
| E18.25 | 180903001 | 1 | 63020.0 | 73597.0 | +10577.0 |

## Gate aggregati

```json
{
  "prefix_d1_d9_identical": true,
  "zero_errors": true,
  "zero_escapes": true,
  "feed_d11_d15_complete": true,
  "resources_cap_14": true,
  "hands_cap_12": true,
  "topology_770_d15_d30": true,
  "mix_9_5_d15_d30": true,
  "crops_d15_38_23": true,
  "melon_sold_by_d12": true,
  "matched_parent_positive": true,
  "incumbent_margin_nonnegative": false
}
```

## Gate planner legacy

```json
{
  "exact_770_layout": true,
  "exact_9_cow_5_sheep": true,
  "all_composition_checkpoints": true,
  "zero_shadow_crop_starvation": true,
  "zero_shadow_animal_escape": true,
  "zero_shadow_illegal_actions": true,
  "all_daily_routes_feasible": true,
  "real_hire_timing_and_peak_12_hands": true,
  "daily_reserve_target_met": true,
  "terminal_residual_crops_at_most_2": true,
  "peak_62_crops_by_d13": false,
  "shadow_crop_output_at_least_jesse_reference_885": false,
  "trajectory_within_720_steps": true
}
```

Dataset: `E18_27_D10_D15_SMOKE_V3.json`.
