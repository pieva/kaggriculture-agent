# E18.18 — Gate 0B exact-engine oracle

## Verdetto

`PASS` nel replay weed-free dell'interprete Kaggriculture reale.

Check falliti: `nessuno`.
Money terminale: `117077`; topologia finale:
`{"Q0": 7, "Q1": 7}`; animali finali:
`{"COW": 9, "SHEEP": 5}`; crop residui:
`{}`.

`policy_build_authorized=true`;
`executor_authorized=false` finché la policy non è stata materialmente costruita
e verificata nei Gate 1–2.

Il Gate richiede inoltre zero crop starvation, 100% di PLANT, DIG e WATER
effettivamente emessi riconosciuti, shed terminale vuoto e un secondo replay
esatto identico.

Le guardie state-aware rimuovono prima dell'emissione i comandi divenuti
inapplicabili. Il PASS oracle autorizza l'estrazione della policy, non la
submission: il rolling replan resta soggetto al Gate 1 development.

## Check

```json
{
  "all_composition_checkpoints": true,
  "all_emitted_water_actions_acknowledged": true,
  "all_plant_and_dig_actions_acknowledged": true,
  "all_three_target_quadrants_unlocked": true,
  "deterministic_exact_replay": true,
  "exact_final_770": true,
  "exact_final_9_cow_5_sheep": true,
  "exact_planned_planting_acknowledged": true,
  "gate_0a_precondition": true,
  "positive_terminal_money": true,
  "terminal_crop_cap": true,
  "zero_controller_errors": true,
  "zero_exact_crop_starvation": true,
  "zero_terminal_shed_inventory": true
}
```

## Checkpoint

```json
{
  "D01": {
    "animal_match": true,
    "crop_match": true
  },
  "D05": {
    "animal_match": true,
    "crop_match": true
  },
  "D10": {
    "animal_match": true,
    "crop_match": true
  },
  "D15": {
    "animal_match": true,
    "crop_match": true
  },
  "D20": {
    "animal_match": true,
    "crop_match": true
  },
  "D25": {
    "animal_match": true,
    "crop_match": true
  },
  "D30": {
    "animal_match": true,
    "crop_match": true
  }
}
```
