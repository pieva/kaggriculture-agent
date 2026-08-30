# POST-E15 --- CONSOLIDATED MODEL_SPEC

**Stato:** `FINAL POST-E15 CONSOLIDATION — APPROVED FOR E16 DESIGN`\
**Fase:** POST-E15 --- cross-review e arbitraggio preliminare\
**Scopo:** consolidare le tre revisioni indipendenti Antigravity, Codex
e Copilot prima del design comune E16.\
**Vincolo:** questo documento non sostituisce i MODEL_SPEC E15 frozen e
non costituisce ancora il MODEL_SPEC definitivo del round successivo.

## 1. Fonti e disciplina epistemica

Il consolidamento usa quattro livelli distinti:

1.  **PRIMARY E15 EVIDENCE** --- artefatti frozen e replay/telemetry
    E15.
2.  **INDEPENDENT MODEL_SPEC REVISIONS** --- Antigravity, Codex,
    Copilot.
3.  **CROSS-REVIEW ARBITRATION** --- confronto concetto-per-concetto fra
    le tre revisioni.
4.  **EXTERNAL OBSERVATIONAL SUPPORT** --- osservazioni precedenti sui
    player top; non sono evidenza E15 e non devono essere confuse con
    essa.

Regole: - E15 resta **TRAINING evidence**. - Nessun valore osservato
viene promosso a optimum. - `FEATURE` non implica monotonicità. -
`NOT_FEATURE` richiede evidenza sufficiente a rimuovere/deprioritizzare
il concetto. - In presenza di confounding o osservabilità insufficiente
usare `UNRESOLVED`. - Parametri direttamente controllabili,
hyperparameter, derived metric e observability requirement devono
restare distinti. - Le classificazioni `UNRESOLVED` introdotte dal
consolidamento possono riflettere una **scelta di cautela in
cross-review** in presenza di evidenza insufficiente/confounded; non
implicano nuova evidenza negativa.

## 2. Arbitraggio consolidato

### 2.1 Land, superficie e attivazione

``` text
concept_id: land_surface_total
feature_status: FEATURE
relationship: conditional / thresholded / non_monotonic
current_initial_bound:
  E15 competitive observations: quadrants_owned = 2
  E15 overextension/failure observation: quadrants_owned = 3 nel bundle Antigravity
  external_observational_support: MIXED; sono state osservate policy competitive/top sia con 2 sia con 3 quadranti totali
  candidate_operating_region: quadrants_owned = 2 come baseline E16
parameter_or_hyperparameter: PARAMETER
next_training_values: nessuna variazione prioritaria in E16; usare quadrants_owned = 2 come controlled baseline iniziale
confounders: activated surface, watering, workforce, livestock, pasture, cash, routing
validation_requirement: il bound sulla superficie dovrà essere validato successivamente su seed/opponent indipendenti e con confronto controllato
falsification_condition: evidenza controllata e replicata che quadrants_owned = 1 o quadrants_owned = 3 producano risultati superiori alla baseline a parità di capacità operativa
```

**Arbitraggio:** `quadrants_owned = 2` è la **candidate operating region
/ controlled baseline E16**, non un optimum. L'evidenza primaria E15
mostra la regione competitiva osservata a 2 quadranti totali e il bundle
Antigravity perdente a 3 quadranti totali, ma non isola causalmente
l'effetto della superficie. L'evidenza osservazionale esterna è
**mista**: sono state osservate policy competitive/top sia con 2 sia con
3 quadranti totali. Questo supporta il mantenimento di
`land_surface_total` come FEATURE condizionale/non monotona, ma non
autorizza un optimum. In E16 si usa `quadrants_owned = 2` come baseline
controllata per concentrare information gain sulle variabili interne.
Gli identificatori ambientali `Q0/Q1/Q2` non devono essere usati come
sinonimi del numero totale di quadranti.

``` text
concept_id: activated_land_surface
feature_status: FEATURE
relationship: positive / conditional
current_initial_bound: not_established
parameter_or_hyperparameter: DERIVED_METRIC
```

Non congelare una percentuale finché non viene definito formalmente cosa
conta come superficie "activated".

``` text
concept_id: crop_surface_maintained
feature_status: FEATURE
relationship: thresholded / conditional / potentially non_monotonic
observed_failure_region: 8–9 active-crop proxy
observed_competitive_region: 25–37
unobserved_region: 10–24
parameter_or_hyperparameter: DERIVED_METRIC
```

``` text
concept_id: pasture_arable_surface_tradeoff
feature_status: FEATURE
relationship: interaction / conditional
parameter_or_hyperparameter: DERIVED_METRIC
```

### 2.2 Watering, care e dispatch

``` text
concept_id: watering_execution_rate
feature_status: FEATURE
relationship: thresholded / conditional
observed_low_service_region: E15 low-outcome runs
observed_high_service_region: E15 competitive runs
unobserved_transition: ampia; non localizzata
parameter_or_hyperparameter: DERIVED_METRIC
```

La metrica osservata non deve essere confusa con il parametro di policy:

``` text
watering_dispatch_priority: PARAMETER
watering_execution_rate: DERIVED_METRIC
```

``` text
concept_id: watering_continuity
feature_status: FEATURE
relationship: thresholded / temporal
parameter_or_hyperparameter: DERIVED_METRIC
```

``` text
concept_id: action_dispatch_failure
feature_status: FEATURE
relationship: negative / plausibly thresholded
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
```

Il rapporto HARVEST/PLANT resta una proxy diagnostica, non una misura
diretta di fallimento.

### 2.3 Workforce e capacità

``` text
concept_id: workforce_headcount
feature_status: UNRESOLVED
relationship: conditional / non_monotonic
observed_region: 9–12
parameter_or_hyperparameter: PARAMETER
```

E15 mostra che il conteggio grezzo non è un predittore monotono. M2
mostra inoltre che lo stesso headcount può produrre outcome molto
diversi.

``` text
concept_id: worker_capacity_available
feature_status: FEATURE
relationship: positive fino a saturazione / conditional
parameter_or_hyperparameter: DERIVED_METRIC
```

``` text
concept_id: productive_action_share
feature_status: UNRESOLVED
relationship: composition-sensitive / non_monotonic
parameter_or_hyperparameter: DERIVED_METRIC
training_priority: LOW
```

La metrica aggregata attuale deve essere sostituita o affiancata da
varianti execution-aware e value-aware.

### 2.4 Livestock, pasture e feed

``` text
concept_id: livestock_headcount
feature_status: FEATURE
relationship: non_monotonic / thresholded / conditional
observed_competitive_region: 4–7
observed_failure_region: 17–18
unobserved_region: 8–16
parameter_or_hyperparameter: PARAMETER
```

`4–7` è una regione osservata competitiva, non un range ottimale.

``` text
concept_id: pasture_surface_maintained
feature_status: FEATURE
relationship: conditional on herd and arable opportunity cost
parameter_or_hyperparameter: DERIVED_METRIC
```

``` text
concept_id: feed_market_dependency
feature_status: UNRESOLVED
relationship: unresolved / possibly non_monotonic
parameter_or_hyperparameter: DERIVED_METRIC
```

La formulazione "market dependency = catastrophic drain" è indebolita da
E15.

``` text
concept_id: wheat_operating_flow
feature_status: FEATURE
relationship: interaction
parameter_or_hyperparameter: DERIVED_METRIC
```

Deve distinguere Wheat come seed, crop output, feed, acquisto, vendita e
riserva.

``` text
concept_id: species_margin_differential
feature_status: UNRESOLVED
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
```

``` text
concept_id: fertilizer_byproduct_flow
feature_status: UNRESOLVED
priority: LOW
```

### 2.5 Capital, market e monetizzazione

``` text
concept_id: operating_cash_buffer
feature_status: FEATURE
relationship: thresholded / conditional / non_monotonic
parameter_or_hyperparameter: HYPERPARAMETER
```

Più cash non è automaticamente meglio; conta la capacità di sostenere
obblighi e investimenti senza stall.

``` text
concept_id: deployable_capital_window
feature_status: FEATURE
relationship: conditional timing state
parameter_or_hyperparameter: DERIVED_METRIC
```

``` text
concept_id: inventory_to_cash_conversion
feature_status: UNRESOLVED
relationship: conceptually positive, empirically unresolved in E15
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
```

``` text
concept_id: market_transaction_value
feature_status: UNRESOLVED
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
```

Gli ordini richiesti non equivalgono a transazioni eseguite.

``` text
concept_id: crop_revenue_mix
feature_status: UNRESOLVED
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
```

### 2.6 State-capacity alignment

``` text
concept_id: state_capacity_alignment
feature_status: UNRESOLVED
relationship: high-priority interaction hypothesis
parameter_or_hyperparameter: NOT_YET_TUNABLE
```

Il concetto è fortemente coerente con E15, ma non esiste ancora una
formula canonica non circolare. Non deve essere congelato come metrica
finché non vengono definiti componenti e formula senza utilizzare
`final_money` come input.

### 2.7 Movement e field condition

``` text
concept_id: movement_overhead
feature_status: FEATURE
relationship: negative only for avoidable movement
parameter_or_hyperparameter: DERIVED_METRIC
```

``` text
concept_id: necessary_transit_fraction
feature_status: FEATURE
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
```

``` text
concept_id: field_cleanliness_state
feature_status: NOT_FEATURE
scope: autonomous objective only
```

``` text
concept_id: weed_backlog_cost
feature_status: FEATURE
relationship: conditional
```

### 2.8 Outcome

``` text
concept_id: final_money_outcome
feature_status: NOT_FEATURE
role: PRIMARY TARGET
```

`final_money` è il target, non una feature esplicativa.

## 3. Requisiti di osservabilità obbligatori prima/durante E16

Il nuovo round deve introdurre un event ledger minimo:

``` text
episode
player
step
actor_or_order
requested_payload
executed_payload
success
failure_reason
executed_quantity
realized_price
realized_value
cash_flow_category
state_before
state_after
provenance
```

Sono inoltre richiesti: - daily serviced crop surface; - watering need
denominator; - action success/failure; - pasture occupancy; - feed
demand/coverage; - necessary transit vs movement overhead; -
purchase-to-activation lag; - cash-flow breakdown; - terminal inventory
by product; - `quadrants_owned: int` come stato esplicito, distinto
dagli identificatori ambientali `Q0/Q1/Q2`; -
`unsold_inventory_quantity` e una eventuale
`unsold_inventory_value_estimate` terminale con metodo di valutazione e
provenance espliciti; tale stima non deve essere confusa con
`realized_value`.

Questa infrastruttura è requisito di misura, non feature sperimentale.

## 4. Bounds che NON devono essere congelati

Non congelare ancora: - WATER \~400/440; - herd 4/7; - crop surface
25/28; - workforce 9/10; - pasture 5; - alcun cash floor; - alcuna
formula di `state_capacity_alignment`.

`quadrants_owned = 2` è la baseline operativa proposta per il prossimo
TRAINING round. Non è un optimum né un land threshold frozen.
`quadrants_owned = 3` resta una regione condizionale non risolta da
testare successivamente in modo controllato; l'evidenza osservazionale
esterna sulla superficie è mista.

## 5. Priorità informative per il prossimo round

1.  **Irrigation service × maintained crop working set** --- localizzare
    la regione di transizione senza assumere un optimum.
2.  **Livestock × pasture × crop allocation** --- separare herd scale
    dall'opportunity cost del pasture.
3.  **Workload × workforce × dispatch quality** --- distinguere
    headcount da capacità utile.
4.  **Executed market/economic telemetry** --- rendere misurabili
    conversion, feed economics, churn, product mix e payback.
5.  **State-capacity alignment formalization** --- definire una formula
    preregistrata solo dopo aver stabilito componenti osservabili.

## 6. Implicazione per il design E16

E16 dovrà essere un **TRAINING experiment comune**, non un nuovo torneo
generico.

Vincolo operativo preliminare:

``` text
quadrants_owned = 2  # controlled E16 baseline; NOT an optimum
```

Questa baseline consente di concentrare l'information gain su: -
watering/service; - crop working set; - livestock/pasture tradeoff; -
workforce/dispatch; - osservabilità economica.

Il design fattoriale definitivo non è ancora congelato in questo
documento.

## 7. Stato finale

Questo consolidato finale chiude il cross-review e l'arbitraggio
post-E15 delle tre revisioni indipendenti e costituisce la base per il
prossimo artefatto:

``` text
POST_E15_E16_TRAINING_DESIGN.md
```

Prima del freeze E16 dovranno essere pre-dichiarati: - variabili
manipulate; - variabili controllate; - candidate values; - seed; -
opponent/benchmark protocol; - telemetry/event ledger; - criteri di
falsificazione; - TRAINING / VALIDATION / TEST split.
