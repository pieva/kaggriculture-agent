# E18.19 — Gate 1 development smoke

## Verdetto

`FAIL` sul primo seed development in
entrambi i seat. La variazione rispetto a E18.18 riguarda soltanto il layer di
esecuzione con retry; piano `7-7-0`, composizione e mercato restano congelati.

Check falliti: `candidate_median_not_below_control`.

| Seat candidato | E18.19 | E18.16 | Margine | Topologia | Animali | Weed finali | Backlog |
|---:|---:|---:|---:|---|---|---:|---:|
| 0 | 51853 | 79440 | -27587 | {"Q0": 7, "Q1": 7} | {"COW": 9, "SHEEP": 5} | 2 | 4 |
| 1 | 51181 | 77867 | -26686 | {"Q0": 7, "Q1": 7} | {"COW": 9, "SHEEP": 5} | 2 | 4 |

## Diagnostica retry

### Seat 0

- Recovery: `{"PARTIAL_PICKUP": 4, "PLANNED_MOVE": 2762, "POSITION_CORRECTION": 90}`
- Deferred: `{"PICKUP": 5, "PLANT": 11}`
- Stale saltate: `{"DIG": 9, "DROP": 6, "FEED": 19, "FERTILIZE": 80, "HARVEST": 40, "PICKUP": 36, "PLANT": 11, "WATER": 102}`
- Backlog a fine giornata: `{"12": 1, "30": 3}`

### Seat 1

- Recovery: `{"PARTIAL_PICKUP": 4, "PLANNED_MOVE": 2762, "POSITION_CORRECTION": 90}`
- Deferred: `{"PICKUP": 5, "PLANT": 11}`
- Stale saltate: `{"DIG": 8, "DROP": 6, "FEED": 19, "FERTILIZE": 80, "HARVEST": 40, "PICKUP": 36, "PLANT": 11, "WATER": 102}`
- Backlog a fine giornata: `{"12": 1, "30": 3}`

## Check

```json
{
  "candidate_median_not_below_control": false,
  "exact_final_770_both_seats": true,
  "exact_final_9_cow_5_sheep_both_seats": true,
  "positive_candidate_reward_both_seats": true,
  "zero_controller_errors": true
}
```
