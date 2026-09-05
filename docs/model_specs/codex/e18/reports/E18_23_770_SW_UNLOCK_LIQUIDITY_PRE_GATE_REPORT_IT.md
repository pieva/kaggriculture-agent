# E18.23 — SW unlock liquidity pre-gate

## Verdetto

Delta causale E18.22:
`FAIL`.
Gate incumbent E18.16:
`FAIL`.

## Contro E18.22

| Seat E18.23 | E18.23 | E18.22 | Margine | SW unlock day | PLANT skip | HARVEST skip |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 76661 | 76487 | +174 | 11 | 10 | 43 |
| 1 | 76487 | 76661 | -174 | 11 | 10 | 44 |

Mediana `76574.0` contro
`76574.0`, delta `+0.0`.

## Contro E18.16

| Seat E18.23 | E18.23 | E18.16 | Margine | SW unlock day | PLANT skip | HARVEST skip |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 52379 | 79284 | -26905 | 12 | 11 | 40 |
| 1 | 51704 | 77693 | -25989 | 12 | 11 | 40 |

Mediana `52041.5` contro
`78488.5`, delta
`-26447.0`.

## Check

```json
{
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": true,
  "incumbent_gate_nonnegative_both_seats": false,
  "parent_delta_nonnegative_both_seats": false,
  "sw_unlocked_by_d11": false,
  "zero_errors": true,
  "zero_skipped_plant": false
}
```
