# E18.21 — Wheat obligation ledger pre-gate

## Verdetto

Variante selezionata: `INFLIGHT_ONLY`.
Delta causale E18.20:
`PASS`.
Gate incumbent E18.16:
`FAIL`.

Le varianti con contratti D+2 sono riportate soltanto come diagnosi: reiterano
la riserva multi-day già respinta in E18.20 e non fanno parte del candidato.

## Ablation dei componenti contro E18.20

| Variante | E18.21 | E18.20 | Delta mediano |
|---|---:|---:|---:|
| INFLIGHT_ONLY | 75203.5 | 74988.5 | +215.0 |
| CONTRACTS_ONLY | 75518.5 | 74986.0 | +532.5 |
| INFLIGHT_AND_CONTRACTS | 75515.5 | 74962.5 | +553.0 |

### Controllo delle varianti contro E18.16

| Variante | E18.21 | E18.16 | Delta mediano |
|---|---:|---:|---:|
| INFLIGHT_ONLY | 51534.5 | 78644.5 | -27110.0 |
| CONTRACTS_ONLY | 51314.0 | 78651.5 | -27337.5 |
| INFLIGHT_AND_CONTRACTS | 51292.0 | 78657.5 | -27365.5 |

## Variante selezionata contro E18.20

| Seat E18.21 | E18.21 | E18.20 | Margine | SELL W | BUY W | FEED skip | W protetto |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 75282 | 74911 | +371 | 1798 | 1651 | 14 | 115 |
| 1 | 75125 | 75066 | +59 | 1792 | 1649 | 14 | 115 |

Mediana `75203.5` contro
`74988.5`, delta `+215.0`.

## Variante selezionata contro E18.16

| Seat E18.21 | E18.21 | E18.16 | Margine | SELL W | BUY W | FEED skip | W protetto |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 51868 | 79438 | -27570 | 1798 | 1646 | 19 | 115 |
| 1 | 51201 | 77851 | -26650 | 1798 | 1646 | 19 | 115 |

Mediana `51534.5` contro
`78644.5`, delta
`-27110.0`.

## Check

```json
{
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": true,
  "incumbent_gate_nonnegative_both_seats": false,
  "parent_delta_nonnegative_both_seats": true,
  "zero_candidate_same_batch_wheat_overlap_from_activation": true,
  "zero_errors": true
}
```
