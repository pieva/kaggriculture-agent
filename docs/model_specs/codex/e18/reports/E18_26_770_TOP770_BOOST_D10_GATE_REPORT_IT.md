# E18.26 — Top770 BoostD10 internal gate

## D1–D10

| KPI | Top770 7-7-0 | E18.25 | E18.26 |
|---|---:|---:|---:|
| PLANT | 63 | 51 | 63 |
| WATER | 254 | 186 | 254 |
| HARVEST | 32 | 18 | 30 |
| MOVE | 790 | 457 | 529 |

E18.26 replica esattamente PLANT e WATER. I due HARVEST mancanti sono output
animali non ancora disponibili nello shadow model; non vengono sostituiti con
no-op o comandi illegali. Le MOVE restano inferiori al riferimento Top770.

## Contro E18.25

| Seat E18.26 | E18.26 | E18.25 | Margine | Money D10 | Unità D10 |
|---:|---:|---:|---:|---:|---:|
| 0 | 63172 | 61196 | +1976 | 1952 | 12 |
| 1 | 63020 | 61343 | +1677 | 1952 | 12 |

Mediana `63096.0` contro `61269.5`.

## Contro E18.16

| Seat E18.26 | E18.26 | E18.16 | Margine | Money D10 | Unità D10 |
|---:|---:|---:|---:|---:|---:|
| 0 | 54761 | 81797 | -27036 | 1451 | 12 |
| 1 | 53968 | 80770 | -26802 | 1451 | 12 |

Delta matched rispetto a E18.25: `+2139.0`;
per seat `{'0': 2198.0, '1': 2080.0}`.

## Check

```json
{
  "actual_crop_checkpoints_match_jesse": false,
  "candidate_exact_770": true,
  "candidate_exact_9_cow_5_sheep": false,
  "d10_actual_hands_11": true,
  "incumbent_delta_nonnegative_both_seats": false,
  "jesse_harvest_gap_at_most_two": true,
  "jesse_plant_exact": true,
  "jesse_water_exact": true,
  "matched_parent_delta_positive_both_seats": true,
  "plan_gate_0a_passed": true,
  "zero_errors": true
}
```

## Verdetto

Il segnale economico è positivo rispetto al parent: delta matched
`+2139.0` e positivo in entrambi i seat. Il gate
strutturale resta però FAIL: contro E18.25 il checkpoint D5 perde
temporaneamente due Wheat, e dopo D12 la copertura FEED non conserva il mix
finale `9 COW + 5 SHEEP`. D10 è exact in tutte le esecuzioni.

E18.26 resta una candidata development. Gate 1, holdout, final confirmation e
upload Kaggle non sono autorizzati. Il successore deve congelare D1–D10 e
ripianificare D11–D14 con una sequenza harvest-first per il Wheat maturo D13.
