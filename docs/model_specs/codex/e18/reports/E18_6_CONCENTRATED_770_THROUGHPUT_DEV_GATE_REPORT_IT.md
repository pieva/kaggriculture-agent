# E18.6 — gate 7-7-0 concentrata contro E18.2

## Verdetto

`FAIL` sui KPI Top-3 aggiornati. La candidata usa pasture `7-7-0`,
converte in crop le cinque celle Q2 della E18.2 e conserva il routing provider
salvo traduzione in-place e fill zootecnico.

La topologia concentrata è tecnicamente realizzabile, ma l'ipotesi di un
guadagno di efficienza non è confermata: la candidata perde tutti i 14 match,
non riduce le move e riduce il lavoro produttivo.

## Risultati

| KPI | E18.6 770 | E18.2 controllo | Delta 770 |
|---|---:|---:|---:|
| Money | 58957.00 | 71104.43 | -17.08% |
| Move | 3603.79 | 3592.43 | +0.32% |
| Produttive | 2643.07 | 2802.86 | -5.70% |
| Move/produttive | 1.3635 | 1.2817 | +6.38% |
| PASS | 850.14 | 689.71 | +23.26% |
| Harvest | 560.36 | 601.86 | -6.90% |
| Harvest/1.000 move | 155.49 | 167.54 | -7.19% |
| Late unwatered/crop | 0.4780 | 0.4882 | -2.09% |

Topologia esatta: `14/14`; fill 14/14:
`14/14`; perdite verificate:
`14`. Record:
`0-14`.

## Lettura causale

Il risparmio geometrico esiste: cinque pasture e quattro animali finali in
meno, con le cinque celle Q2 effettivamente utilizzate come crop. Non diventa
però risparmio logistico. Le move medie restano quasi identiche
(`+0.32%`), le produttive calano di `5.70%`
e i PASS crescono di `23.26%`. Il lavoro zootecnico rimosso non è
sostituito da un ciclo crop abbastanza intenso; harvest e harvest per 1.000
move scendono rispettivamente di `6.90%` e
`7.19%`.

La piccola riduzione del late-unwatered (`2.09%`)
non raggiunge il target del 10% e non compensa il throughput perso. Il cap di
15 risorse animali per 14 pasture introduce inoltre un transito
sovrannumerario: il verificatore osserva una perdita in ciascun match. È un
difetto di safety da non conservare, ma non spiega da solo il gap economico
medio del `17.08%`.

La prima esecuzione completa aveva prodotto una topologia invalida `6-5-0`
perché il carrier fill sovrascriveva tre BUILD_PASTURE. È stata corretta
soltanto la precedenza del comando, senza cambiare KPI; quel tentativo non è
usato per la decisione.

## Decisione

E18.6 V1 è `REJECTED_AT_DEVELOPMENT_GATE`. Non consumare holdout o final e non
preparare/uploadare una submission. Il prossimo trattamento non deve essere
un altro overlay geometrico: prima serve un lifecycle scheduler capace di
trasformare il Q2 crop-only in lavoro produttivo e di ridurre davvero le
tratte; un'eventuale 7-7-0 nativa dovrà inoltre usare cap animali 14.

## Check

```json
{
  "exact_770_topology_all_matches": true,
  "filled_14_of_14_all_matches": true,
  "harvest_per_1000_moves_at_least_200": false,
  "harvested_units_at_least_20pct_above_control": false,
  "harvested_units_at_least_720": false,
  "late_unwatered_rate_at_least_10pct_better": false,
  "money_not_below_control_minus_5pct": false,
  "move_per_productive_at_least_5pct_better": false,
  "move_per_productive_at_most_1_20": false,
  "productive_at_least_10pct_above_control": false,
  "productive_at_least_3000": false,
  "worst_matched_money_delta_at_least_minus_5pct": false,
  "zero_fallbacks": true,
  "zero_global_rerouting": true,
  "zero_q2_pastures_observed": true,
  "zero_technical_errors": true,
  "zero_topology_breaches": true,
  "zero_verified_livestock_losses": false
}
```
