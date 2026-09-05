# E18.24 — Deferred PLANT on WATER pre-gate

## Verdetto

Delta causale E18.22:
`FAIL`.
Gate incumbent E18.16:
`FAIL`.

## Contro E18.22

| Seat E18.24 | E18.24 | E18.22 | Margine | PLANT recuperati | HARVEST skip | PLANT skip storico |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 74682 | 74378 | +304 | 1 | 43 | 10 |
| 1 | 74510 | 74550 | -40 | 1 | 44 | 10 |

Mediana `74596.0` contro
`74464.0`, delta `+132.0`.

## Contro E18.16

| Seat E18.24 | E18.24 | E18.16 | Margine | PLANT recuperati | HARVEST skip | PLANT skip storico |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 52379 | 79284 | -26905 | 0 | 40 | 11 |
| 1 | 51704 | 77693 | -25989 | 0 | 40 | 11 |

Mediana `52041.5` contro
`78488.5`, delta
`-26447.0`.

## Check

```json
{
  "all_d11_locked_plants_recovered": false,
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": true,
  "harvest_skips_below_parent_baseline": false,
  "incumbent_gate_nonnegative_both_seats": false,
  "parent_delta_nonnegative_both_seats": false,
  "zero_errors": true
}
```
