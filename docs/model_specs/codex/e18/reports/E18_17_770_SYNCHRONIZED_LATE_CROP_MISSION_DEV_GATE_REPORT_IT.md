# E18.17 — synchronized late crop mission V1

## Verdetto

Gate A causale: `FAIL`. Gate B diagnostico:
`FAIL`.
Controllo topology-matched: E18.16.

| KPI | E18.17 | E18.16 | Delta |
|---|---:|---:|---:|
| Money | 65632.29 | 65632.29 | +0.00% |
| MOVE | 3608.14 | 3608.14 | +0.00% |
| PASS | 846.14 | 846.14 | +0.00% |
| PLANT richiesti | 192.00 | 192.00 | +0.00% |
| HARVEST ack rate | 62.91% | 62.91% | +0.00 pp |
| Unità raccolte | 579.79 | 579.79 | +0.00% |
| Late unwatered | 232.00 | 232.00 | +0.00% |
| Starved-to-weed | 12.00 | 12.00 | +0.00 |

Record `1-1`; money matched medio
`+0.00%`, peggiore
`-0.08%`.

Il record grezzo include l'effetto seat: sul solo seed non-TIE, `180903004`,
candidata e controllo ottengono lo stesso money quando occupano lo stesso
seat. Non è quindi evidenza di un vantaggio del trattamento.

## Attivazione

- PLANT bloccati medi: `0.00`;
- override HARVEST locali: `0.00`;
- override WATER locali: `0.00`;
- missioni avviate/ack: `79.00` /
  `79.00`;
- MOVE provider sostituiti: `0.00`;
- override non-MOVE non autorizzati: `0.00`.

## Gate A

```json
{
  "controller_observed_all_matches": true,
  "exact_filled_770_all_matches": true,
  "harvest_ack_rate_not_lower": true,
  "harvested_units_not_lower": true,
  "late_unwatered_not_worse": true,
  "max_fourteen_livestock_resources_all_matches": true,
  "mission_ack_observed_all_matches": true,
  "money_not_below_control": true,
  "move_not_higher_by_more_than_1pct": true,
  "starved_to_weed_not_worse": true,
  "treatment_action_effect_all_matches": false,
  "worst_matched_money_delta_at_least_minus_2pct": true,
  "zero_errors_and_fallbacks": true,
  "zero_livestock_losses": true,
  "zero_unauthorized_non_move_overrides": true
}
```

Holdout e final-confirmation non consumati. Il confronto con gli altri campioni
interni è ammesso soltanto se il Gate A passa. In caso di trattamento senza
effetto sulle azioni, E18.16 resta la base interna e la candidata non è
promuovibile né candidabile alla submission quotidiana.
