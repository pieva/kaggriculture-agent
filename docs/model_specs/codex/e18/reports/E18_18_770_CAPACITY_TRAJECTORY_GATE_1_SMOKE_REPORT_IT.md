# E18.18 — Gate 1 development smoke

## Verdetto

`FAIL` sul primo seed development in
entrambi i seat. Questo smoke non sostituisce il Gate 1 preregistrato a 14
match.

Check falliti: `exact_final_9_cow_5_sheep_both_seats, candidate_median_not_below_control`.

| Seat candidato | E18.18 | E18.16 | Margine | Topologia | Animali | Weed finali |
|---:|---:|---:|---:|---|---|---:|
| 0 | 55934 | 85578 | -29644 | {"Q0": 7, "Q1": 7} | {"COW": 7, "SHEEP": 4} | 2 |
| 1 | 55934 | 85578 | -29644 | {"Q0": 7, "Q1": 7} | {"COW": 7, "SHEEP": 4} | 2 |

## Check

```json
{
  "candidate_median_not_below_control": false,
  "exact_final_770_both_seats": true,
  "exact_final_9_cow_5_sheep_both_seats": false,
  "positive_candidate_reward_both_seats": true,
  "zero_controller_errors": true
}
```
