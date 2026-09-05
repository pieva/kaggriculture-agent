# E18.18 — Gate 0A capacity trajectory planner

## Verdetto

`PASS` per il Gate 0A offline.
Il piano nativo `7-7-0` realizza i checkpoint del benchmark Top770, usa
`9 COW + 5 SHEEP`, non produce starvation/fughe/comandi illegali nel modello
biologico shadow e rispetta la riserva operativa preregistrata ogni giorno.

Questo **non** è ancora il Gate 0 completo e non autorizza un executor o una
submission. Mancano replay nell'engine reale, ledger monetario/inventari/shed e
ack delle vendite terminali.

## Risultato sintetico

| KPI | Piano E18.18 Gate 0A | Riferimento Top770 770 |
|---|---:|---:|
| Peak crop | 62 (D12) | 62 (entro D13) |
| Output crop shadow | 892 | 885 |
| Melon | 72 | 72 |
| Strawberry | 240 | 260 |
| Annuali Wheat/Carrot | 580 | 553 |
| MOVE teoriche | 2852 | 3.473 osservate |
| WATER | 1020 | 1.172 osservate |
| PLANT | 169 | 243 osservate |
| Fertilizzazioni | 114 | n.d. |
| Riserva minima | 1.35% (D24) | target >=1% |
| Crop residui D30 | 0 | <=2 |

L'output shadow è `892`: +7
rispetto alle 885 unità del riferimento. Il mix è molto vicino
(`72 MELON`, `240 STRAWBERRY`,
`580 WHEAT`). La riduzione di MOVE è un lower
bound del route solver, non ancora una previsione di risultato nell'engine.

## Checkpoint di consistenza

| Giorno | Colture | Animali | Esito |
|---|---|---|---|
| D01 | `{"MELON": 12, "WHEAT": 7}` | `{"COW": 2, "SHEEP": 2}` | PASS |
| D05 | `{"MELON": 12, "WHEAT": 7}` | `{"COW": 4, "SHEEP": 2}` | PASS |
| D10 | `{"MELON": 12, "STRAWBERRY": 20, "WHEAT": 5}` | `{"COW": 9, "SHEEP": 4}` | PASS |
| D15 | `{"STRAWBERRY": 38, "WHEAT": 23}` | `{"COW": 9, "SHEEP": 5}` | PASS |
| D20 | `{"STRAWBERRY": 38, "WHEAT": 23}` | `{"COW": 9, "SHEEP": 5}` | PASS |
| D25 | `{"STRAWBERRY": 22, "WHEAT": 39}` | `{"COW": 9, "SHEEP": 5}` | PASS |
| D30 | `{}` | `{"COW": 9, "SHEEP": 5}` | PASS |

La settima pasture di Q0 è coltivata nella fase iniziale. Il piano raggiunge
37 crop e 13 pasture entro D10, occupa Q2 con 25 crop entro D12, poi raccoglie
i 12 MELON e converte quella tile nel quattordicesimo pascolo. A D15 restano
esattamente 61 crop. Sedici STRAWBERRY vengono ruotate verso annuali fra D21 e
D25; ogni nuova semina annuale si ferma a D25 e le colture terminali sono
liquidate entro D29.

## Scelte di capacità

- WATER alternato quando non incide sul yield; WATER obbligatorio nelle
  finestre produttive annuali e sui nuovi PLANT;
- fertilizzante raccolto soltanto fino al fabbisogno pianificato: nessuna
  raccolta eccedente dopo D16;
- HARVEST permanenti distribuiti per fase di tile e WATER remoti di Q2 rinviati
  al massimo di un giorno nei picchi, senza starvation shadow;
- ogni route che raccoglie torna a uno dei quattro accessi dello shed e chiude
  con DROP nello stesso giorno;
- la capacità usa il timing reale: farmer e primi dieci HIRE iniziano le route
  al turno 2; gli ultimi due hands, quando necessari, dal turno 3;
- hash del piano: `844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1`;
- seconda costruzione identica: `True`.

## Gate 0B ancora obbligatorio

1. eseguire le route contro l'interprete Kaggriculture reale con weed disabilitate;
2. modellare BUY_LAND, HIRE, semi, animali, Wheat di FEED, shed capacity e cash;
3. verificare DROP/SELL terminali e ack di ogni task;
4. soltanto dopo un PASS costruire l'executor state-driven e avviare Gate 1 e
   confronti matched con E18.16.

## Check automatici

```json
{
  "all_composition_checkpoints": true,
  "all_daily_routes_feasible": true,
  "daily_reserve_target_met": true,
  "deterministic_two_run_hash": true,
  "exact_770_layout": true,
  "exact_9_cow_5_sheep": true,
  "peak_62_crops_by_d13": true,
  "real_hire_timing_and_peak_12_hands": true,
  "shadow_crop_output_at_least_jesse_reference_885": true,
  "terminal_residual_crops_at_most_2": true,
  "trajectory_within_720_steps": true,
  "zero_shadow_animal_escape": true,
  "zero_shadow_crop_starvation": true,
  "zero_shadow_illegal_actions": true
}
```
