# E18.25 — D10 labor step pre-gate

## Verdetto

Delta causale matched contro E18.22: `PASS`. Il trattamento porta D10 da
`7` a
`12` unità attive, senza cambiare
il multiset di azioni agricole pianificate.

Sul medesimo seed, seat e avversario E18.16, la mediana passa da
`52041.5` a
`52225.5`: delta `+184.0`;
delta per seat `{'0': 184.0, '1': 184.0}`.

## Stress competitivo diretto contro E18.22

| Seat E18.25 | E18.25 | E18.22 | Margine | Unità D10 E18.25 | Unità D10 opp. | Denaro D10 E18.25 | Denaro D10 opp. |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 82434 | 67439 | +14995 | 12 | 7 | 1583 | 1660 |
| 1 | 82264 | 67609 | +14655 | 12 | 7 | 1583 | 1660 |

Mediana `82349.0` contro
`67524.0`, delta `+14825.0`.

## Contro E18.16

| Seat E18.25 | E18.25 | E18.16 | Margine | Unità D10 E18.25 | Unità D10 opp. | Denaro D10 E18.25 | Denaro D10 opp. |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 52563 | 79755 | -27192 | 12 | 12 | 1337 | 2105 |
| 1 | 51888 | 78164 | -26276 | 12 | 12 | 1337 | 2105 |

Mediana `52225.5` contro
`78959.5`, delta `-26734.0`.

## Check

```json
{
  "biological_plan_unchanged": true,
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": true,
  "d10_actual_hands_11": true,
  "d10_planned_active_units_12": true,
  "d10_productive_action_multiset_unchanged": true,
  "incumbent_delta_nonnegative_both_seats": false,
  "matched_parent_delta_positive_both_seats": true,
  "plan_gate_0a_passed": true,
  "zero_errors": true
}
```
