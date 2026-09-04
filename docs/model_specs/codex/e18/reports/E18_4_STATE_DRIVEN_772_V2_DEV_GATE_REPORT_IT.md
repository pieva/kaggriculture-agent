# E18.4 V2 — locality/task-aging development gate

## Decisione

**Gate A: FAIL**. Gate B:
NON ESEGUITO.
La candidata resta development-only; nessun upload Kaggle è autorizzato.

## Risultati principali

| KPI medio | V2 | E18.2 |
|---|---:|---:|
| Money | 47247.57 | 77644.29 |
| Move | 4477.43 | 3591.57 |
| Productive | 2217.43 | 2802.50 |
| Move/productive | 2.0192 | 1.2816 |
| Harvested units | 472.57 | 601.29 |
| Crop tile-days D21-D30 | 452.43 | 472.71 |
| Weed tile-days D21-D30 | 36.36 | 15.00 |

## Gate falliti

- `move_actions_lte_e18_2`
- `productive_actions_gte_95pct_e18_2`
- `move_per_productive_lte_1_28`
- `harvested_units_gte_95pct_e18_2`
- `late_weed_tile_days_lte_110pct_e18_2`

## Integrità

- match development: 14;
- holdout/final consumati: no/no;
- topologia 7-7-2 esatta: 14/14;
- fill 16/16: 14/14;
- errori/fallback/perdite: 0/0/0.
