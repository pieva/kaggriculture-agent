# E18.20 — Wheat market netting pre-gate

## Verdetto

Delta causale E18.19:
`PASS`.
Gate incumbent E18.16:
`FAIL`.

## Contro E18.19

| Seat E18.20 | E18.20 | E18.19 | Margine | SELL W | BUY W | Overlap |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 75324 | 74868 | +456 | 2377 | 2216 | 1 |
| 1 | 75135 | 75057 | +78 | 2331 | 2174 | 1 |

Mediana `75229.5` contro
`74962.5`, delta `+267.0`.

## Contro E18.16

| Seat E18.20 | E18.20 | E18.16 | Margine | SELL W | BUY W | Overlap |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 51857 | 79437 | -27580 | 2377 | 2211 | 1 |
| 1 | 51187 | 77860 | -26673 | 2377 | 2211 | 1 |

Mediana `51522.0` contro
`78648.5`, delta
`-27126.5`.

Il netting rimuove soltanto le quantità Wheat comprate e vendute nello stesso
batch. La variante che allineava anche la riserva SELL all'orizzonte D+2 è
stata respinta nel pre-gate perché riduceva il churn ma peggiorava il money.

## Check

```json
{
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": true,
  "incumbent_gate_nonnegative_both_seats": false,
  "parent_delta_nonnegative_both_seats": true,
  "zero_candidate_same_batch_wheat_overlap": true,
  "zero_errors": true
}
```
