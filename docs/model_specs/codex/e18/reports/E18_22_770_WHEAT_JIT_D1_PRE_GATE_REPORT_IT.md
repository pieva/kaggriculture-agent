# E18.22 — Wheat JIT D+1 pre-gate

## Verdetto

Delta causale E18.21:
`PASS`.
Gate incumbent E18.16:
`FAIL`.

## Contro E18.21

| Seat E18.22 | E18.22 | E18.21 | Margine | SELL W | BUY W | FEED skip | BUY D+2 rimossi |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 76966 | 74673 | +2293 | 365 | 216 | 7 | 4308 |
| 1 | 76793 | 74846 | +1947 | 359 | 214 | 7 | 4308 |

Mediana `76879.5` contro
`74759.5`, delta `+2120.0`.

## Contro E18.16

| Seat E18.22 | E18.22 | E18.16 | Margine | SELL W | BUY W | FEED skip | BUY D+2 rimossi |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 52379 | 79284 | -26905 | 365 | 220 | 12 | 4299 |
| 1 | 51704 | 77693 | -25989 | 365 | 220 | 12 | 4299 |

Mediana `52041.5` contro
`78488.5`, delta
`-26447.0`.

## Check

```json
{
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": true,
  "d2_wheat_buys_removed": true,
  "incumbent_gate_nonnegative_both_seats": false,
  "parent_delta_nonnegative_both_seats": true,
  "zero_candidate_same_batch_wheat_overlap_from_activation": true,
  "zero_errors": true
}
```
