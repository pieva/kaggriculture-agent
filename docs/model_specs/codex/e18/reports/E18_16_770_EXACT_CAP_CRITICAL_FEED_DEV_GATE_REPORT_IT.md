# E18.16 — cap 14 + critical FEED

## Validazione esterna Kaggle

Submission completata il 2026-09-04 con score pubblico `729,0`. Il controllo
esterno E18.2 è a `1199,7`: delta `-470,7` (`-39,24%`). La piccola crescita
locale e la safety perfetta non trasferiscono sulla distribuzione pubblica.
Verdetto aggiornato: `EXTERNAL_REGRESSION_CONFIRMED / NOT_PROMOTED`. Il cap 14
e il guard FEED restano invarianti di sicurezza, non prova di superiorità
economica dell'intero controller.

## Verdetto

Gate A: `PASS`. Gate B
Top-3: `FAIL`.
Controllo E18.10 V2.

| KPI | E18.16 | E18.10 V2 | Delta |
|---|---:|---:|---:|
| Money | 65817.07 | 65049.21 | +1.18% |
| Perdite | 0 | 14 | n/a |
| MOVE | 3607.86 | 3603.21 | +0.13% |
| PASS | 846.43 | 848.14 | -0.20% |
| WATER | 925.93 | 924.93 | +0.11% |
| Crop service | 1577.71 | 1576.64 | +0.07% |
| Harvest | 242.79 | 242.71 | +0.03% |
| Unità | 579.79 | 578.71 | +0.19% |

Record `8-6`; money matched medio
`+0.67%`, peggiore
`-0.95%`.

## Interpretazione causale

Il quindicesimo animale era ammesso dal buffer legacy: 14 risorse erano già
presenti a D12 H2, ma un ulteriore `BUY_ANIMAL SHEEP 1` a D12 H3 passava sotto
il cap 15. Con il solo cap, la morte D20 obbligava a ricomprare un rimpiazzo;
con il solo FEED, il surplus restava nello shed e il worst era `-2,85%`.
E18.16 impedisce entrambi gli sprechi e porta il worst a `-0,95%`.

## Gate A

```json
{
  "animal_clamp_activated_all_matches": true,
  "control_loss_reproduced_each_match": true,
  "crop_service_not_lower_by_more_than_0_5pct": true,
  "exact_filled_770_candidate_all_matches": true,
  "exact_filled_770_control_all_matches": true,
  "harvest_events_not_lower_by_more_than_0_5pct": true,
  "harvested_units_not_lower_by_more_than_0_5pct": true,
  "late_unwatered_not_worse_by_more_than_0_5pct": true,
  "max_fourteen_livestock_resources_all_matches": true,
  "money_not_below_control": true,
  "move_not_higher_by_more_than_0_5pct": true,
  "one_critical_feed_override_each_match": true,
  "only_registered_mutations": true,
  "water_not_lower_by_more_than_0_5pct": true,
  "worst_matched_money_delta_at_least_minus_2pct": true,
  "zero_candidate_livestock_losses": true,
  "zero_errors_and_fallbacks": true,
  "zero_topology_breaches": true
}
```

Holdout e final-confirmation non sono stati consumati. L'upload Kaggle è stato
successivamente autorizzato come sola verifica esterna ed è chiuso a `729,0`.
