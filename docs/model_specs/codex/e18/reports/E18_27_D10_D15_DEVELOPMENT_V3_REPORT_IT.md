# E18.27 — confronto interno D10-D15

Confronti matched sul parent E18.26; seed e seat identici contro lo stesso avversario. Nessun holdout o upload.

| Avversario | Seed | Seat | E18.26 | E18.27 | Delta |
|---|---:|---:|---:|---:|---:|
| E18.16 | 180903001 | 0 | 54761.0 | 74287.0 | +19526.0 |
| E18.16 | 180903001 | 1 | 53968.0 | 74287.0 | +20319.0 |
| E18.16 | 180903002 | 0 | 47423.0 | 66154.0 | +18731.0 |
| E18.16 | 180903002 | 1 | 47239.0 | 66154.0 | +18915.0 |
| E18.16 | 180903003 | 0 | 53205.0 | 52684.0 | -521.0 |
| E18.16 | 180903003 | 1 | 53205.0 | 52684.0 | -521.0 |
| E18.16 | 180903004 | 0 | 62931.0 | 48427.0 | -14504.0 |
| E18.16 | 180903004 | 1 | 63061.0 | 41141.0 | -21920.0 |
| E18.16 | 180903005 | 0 | 83276.0 | 90769.0 | +7493.0 |
| E18.16 | 180903005 | 1 | 83276.0 | 90146.0 | +6870.0 |
| E18.16 | 180903006 | 0 | 72665.0 | 92680.0 | +20015.0 |
| E18.16 | 180903006 | 1 | 72665.0 | 92680.0 | +20015.0 |
| E18.16 | 180903007 | 0 | 52856.0 | 67924.0 | +15068.0 |
| E18.16 | 180903007 | 1 | 52974.0 | 58167.0 | +5193.0 |

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
  "mix_9_5_d15_d30": false,
  "crops_d15_38_23": false,
  "melon_sold_by_d12": true,
  "matched_parent_positive": false,
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

Dataset: `E18_27_D10_D15_DEVELOPMENT_V3.json`.
