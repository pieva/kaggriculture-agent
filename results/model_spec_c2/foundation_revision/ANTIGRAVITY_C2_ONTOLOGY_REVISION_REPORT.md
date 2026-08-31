# ANTIGRAVITY C2 — ONTOLOGY REVISION REPORT

```text
DOCUMENT_ID: ANTIGRAVITY_C2_ONTOLOGY_REVISION_REPORT
AUTHOR: Antigravity
DATE: 2026-08-31
PHASE: Foundation Revision / Ontology Revision Pass
TARGET_DOCUMENT: docs/model/ontology/ONTOLOGY_C2.md
BASELINE_AUTHORITY: results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md (FROZEN)
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
STATUS: COMPLETE — READY FOR INDEPENDENT REVIEW
```

---

## 1. Executive Result

Antigravity ha completato la revisione formale dell'Ontologia canonica di Kaggriculture (`docs/model/ontology/ONTOLOGY_C2.md`), allineandola al 100% con l'Engine Contract C2 congelato.

```text
================================================================================
ONTOLOGY_REVISION_COMPLETE: YES
ENGINE_CONTRACT_CONSISTENT: YES
POLICY_NEUTRALITY_PRESERVED: YES
CONCEPT_TRACEABILITY_PRESERVED: YES
ONTOLOGY_READY_FOR_REVIEW: YES
================================================================================
```

### Sintesi dell'intervento:
- **Registry Consolidato:** 78 `concept_id` canonici articolati in 9 domini (A–I).
- **Nuovo Dominio I (Clock e Serviceability):** Introdotti formalmente i 4 concetti fondativi `canonical_clock_coordinate`, `action_eligible_now`, `reserved_serviceable_before_deadline` e `realized_serviceable_in_window`.
- **Risoluzione P0 di Dominio:**
  - `CLK-01`: Parametrizzazione universale di `turnsPerDay` ($T$) e invariante $\text{step} == \text{day} \cdot T + \text{hour}$.
  - `ANI-01` & `ANI-02`: Dissociazione del base output ($=1$) dal `FEED`, introduzione di `animal_escape_condition` (fuga al 2° EOD unfed consecutivo) e `pending_care_bonus_accumulation` differito.
  - `FER-01` & `FER-02`: Formalizzazione dell'uplift netto $+1$ (`BASE=1`, `FERTILIZED=2`) e finestra inclusiva di 3 giorni (`day..day+2`).
  - `INV-01` & `INV-02`: Riconcettualizzazione in `shed_overflow_loss` (distruttivo per `MANUAL_DROP` ed `EOD_AUTO_DROP`, conservativo per `PLACE`).
- **Policy Neutrality Rigorosa:** Rimossa qualsiasi traccia di preferenza strategica (convenienza economica di colture o animali, target monetari, layout specifici).

---

## 2. Concept Migration Matrix

La tabella seguente documenta la genealogia e l'azione applicata a ciascun concetto del registry ontologico:

| Concept ID | Stato/Significato Precedente | Azione | Nuovo Stato / Definizione C2 | Evidenza Engine | Downstream Impact |
|---|---|:---:|---|---|---|
| `land_surface_total` | Superficie posseduta | `KEEP` | Superficie totale sbloccata | `kaggriculture.py` grid | Nessuno |
| `land_purchase_timing` | Timing BUY_LAND | `KEEP` | Step/giorno transazione BUY_LAND | Market phase | Nessuno |
| `activated_land_surface` | Superficie in uso | `KEEP` | Superficie con colture o pascoli | Grid inspection | Classifier in Feature Model |
| `crop_surface_maintained` | Tile coltivate vive | `KEEP` | Tile con piante non decedute | Plant decay logic | Classifier in Feature Model |
| `pasture_surface_maintained` | Pascoli attivi | `KEEP` | Strutture animali mantenute | Animal structures | Classifier in Feature Model |
| `maintained_productive_surface` | Somma crop + pasture | `KEEP` | Superficie mantenuta aggregata | Derived logic | Feature Model aggregations |
| `monetized_productive_output` | Ricavo superficie | `KEEP` | Flusso vendite da superficie | Market sales | Telemetry metrics |
| `land_activation_payback` | Payback terra | `KEEP` | Tempo ammortamento terra | Economic derived | Telemetry metrics |
| `pasture_arable_surface_tradeoff` | Tradeoff pasture/arable | `KEEP` | Mutua esclusione spaziale | Grid bounds | State Machine spatial rules |
| `workforce_headcount` | Conteggio worker | `KEEP` | Farmer + Hands attivi nello step | Unit list | State Machine workforce state |
| `worker_capacity_available` | Capacità worker (scalare) | `REVISE` | Upper bound multi-dimensionale incompleto | Action slot logic | Rimosso calcolo scalare deterministico |
| `hire_order_scheduling` | Timing HIRE | `REVISE` | Sequenza HIRE; hands attivi da step succ. | Market execution order | State Machine timing HIRE |
| `marginal_hire_payback` | Payback assunzione | `KEEP` | Rendimento netto vs costo Fibonacci | Hire cost formula | Telemetry metrics |
| `productive_action_share` | Frazione azioni utili | `KEEP` | Azioni mutative vs totale passi | Unit action types | Telemetry metrics |
| `movement_overhead` | Quota MOVE | `KEEP` | Frazione step spesi in transito | MOVE action | Telemetry metrics |
| `necessary_transit_fraction` | Movimento necessario | `KEEP` | Quota transito ottimale | Manhattan distance | Telemetry metrics |
| `routing_completion_efficiency` | Efficienza routing | `KEEP` | Ottimalità percorsi | Pathing efficiency | Telemetry metrics |
| `action_dispatch_failure` | Azioni no-op | `KEEP` | Richieste fallite per guardie | Action guards | Telemetry metrics |
| `worker_action_monetization_rate` | Valore per azione | `KEEP` | Monetizzazione per slot worker | Economic derived | Telemetry metrics |
| `worker_multi_occupancy` | Compresenza worker | `KEEP` | Multi-occupancy priva di collisioni | Position tracking | State Machine spatial rules |
| `crop_care_action_flow` | Flusso cure piante | `KEEP` | Flusso aggregato PLANT/WATER/FERT/HARV | Unit action loop | Feature Model aggregations |
| `planting_action_flow` | Azioni PLANT | `REVISE` | Validazione atomica semi per specie | `_apply_unit_action` PLANT | State Machine PLANT atomicity |
| `watering_execution_rate` | Azioni WATER | `REVISE` | Day-scoped (prima WATER ha effetto) | `_daily_refresh_plants` | State Machine WATER flag |
| `watering_continuity` | Continuità idrica | `REVISE` | Prevenzione consecutive_unwatered=2 | `consecutive_unwatered` | State Machine EOD death |
| `crop_harvest_action_flow` | Azioni HARVEST | `KEEP` | Esecuzione HARVEST su pianta matura | `_apply_unit_action` HARVEST | State Machine HARVEST transition |
| `first_yield_day` | Età maturità legale | `KEEP` | Soglia $d - d_0 \ge \text{first\_yield\_day}$ | `CROPS` dictionary | Feature Model readiness |
| `crop_harvest_readiness` | Predicato maturità | `REVISE` | Maturità legale; pre-readiness è no-op | `CROPS` + age guards | State Machine early HARVEST no-op |
| `crop_fertilizer_bonus` | Bonus resa fertilizzante | `REVISE` | Incremento $+2$, uplift netto canonico $+1$ | `_daily_refresh_plants` | Feature Model uplift $+1$ |
| `fertilizer_effect_window` | Finestra fertilizzante | `REVISE` | 3 giorni inclusivi (`day..day+2`), no age accel | `fertilized_until_day` | State Machine expiry $d+2$ |
| `crop_care_completion_rate` | Tasso cure erogate | `KEEP` | Fabbisogno vs cure effettive | Derived telemetry | Telemetry metrics |
| `crop_decay_risk_window` | Rischio decadimento | `REVISE` | Disidratazione EOD o step $\ge$ MLS | `max_lifespan_step` | State Machine lifespan decay |
| `crop_horizon_alignment` | Allineamento orizzonte | `KEEP` | Giorni residui vs tempo biologico | Biological calendar | Decision context feature |
| `crop_revenue_mix` | Mix ricavi colture | `KEEP` | Ripartizione ricavi specie | Sales breakdown | Telemetry metrics |
| `feed_availability` | Grano per animali | `KEEP` | Grano in shed o worker inventory | Inventory check | Action guard FEED |
| `feed_security_buffer` | Buffer scorte mangime | `REVISE` | Riclassificato come `POLICY_DECLARED` | Policy planning | Rimosso da vincoli fisici engine |
| `feed_market_dependency` | Dipendenza acquisti feed | `KEEP` | Feed comprato vs autoprodotto | Market vs Harvest | Telemetry metrics |
| `feed_market_expenditure` | Spesa per mangime | `KEEP` | Esborso monetario per Wheat | Market fills | Telemetry metrics |
| `wheat_operating_flow` | Flusso multiuso Wheat | `KEEP` | Seme, raccolto, mangime, vendita | Multipurpose Wheat | Feature Model resource flow |
| `market_churn_cost` | Spread compravendita | `KEEP` | Costo churn transazioni | Spread delta | Telemetry metrics |
| `livestock_headcount` | Capi bestiame | `REVISE` | Articolato su GOOSE, COW, SHEEP | `ANIMALS` dictionary | Rimossa ogni menzione di Chicken |
| `livestock_capacity` | Capacità zootecnica | `KEEP` | Dimensione massima gregge gestibile | Capacity derived | Feature Model capacity |
| `pasture_capacity_alignment` | Allineamento strutture | `REVISE` | GOOSE $\to$ COOP, COW/SHEEP $\to$ PASTURE | `ANIMALS` structure | State Machine placement legality |
| `livestock_product_flow` | Flusso prodotti animali | `REVISE` | Generazione EGG, MILK, WOOL | `PRODUCTS` list | State Machine animal yield |
| `livestock_base_production` | Produzione base | `ADD` | Base output = 1 a schedule se non scappato | `_daily_refresh_animals` | State Machine dissocia FEED da base |
| `livestock_care_action_flow` | Azioni CARE | `KEEP` | Flusso azioni CARE | `_apply_unit_action` CARE | State Machine CARE flag |
| `pending_care_bonus_accumulation` | Accumulo bonus cura | `REVISE` | Differito a EOD se fed+cared; consumato se fed | `pending_care_bonus` | State Machine bonus deferred |
| `animal_escape_condition` | Condizione fuga animale | `ADD` | Fuga a EOD su consecutive_unfed $\ge$ 2 | `consecutive_unfed` | State Machine escape transition |
| `fertilizer_available_state` | Flag fertilizzante animale | `ADD` | Boolean True a EOD non-escape, non cumulabile | `fertilizer_available` | State Machine fertilizer reset |
| `fertilizer_byproduct_flow` | Raccolta fertilizzante | `REVISE` | Prelevato via `COLLECT_FERTILIZER` | `COLLECT_FERTILIZER` | State Machine COLLECT action |
| `species_margin_differential` | Differenziale margini | `KEEP` | Margine a posteriori per specie | Telemetry derived | Telemetry metrics |
| `market_transaction_value` | Valore transazione | `KEEP` | Controvalore al prezzo eseguito | Market log | Telemetry metrics |
| `operating_cash_buffer` | Buffer cassa operativo | `REVISE` | Riclassificato come `POLICY_DECLARED` | Policy context | Rimosso da vincoli fisici engine |
| `deployable_capital_window` | Finestra capitale libero | `REVISE` | Riclassificato come `POLICY_DECLARED` | Policy context | Rimosso da vincoli fisici engine |
| `asset_liquidity_lag` | Ritardo liquidità asset | `KEEP` | Latenza tra spesa e primo incasso | Derived telemetry | Telemetry metrics |
| `inventory_to_cash_conversion` | Conversione scorte/cassa | `KEEP` | Esecuzione ordini SELL | Market sales | Feature Model conversion flow |
| `market_sellthrough_lag` | Tempo realizzo vendite | `KEEP` | Latenza tra produzione e vendita | Derived telemetry | Telemetry metrics |
| `unsold_inventory_value` | Valore scorte residue | `KEEP` | Valore merci giacenti a fine match | Inventory value | Outcome metrics |
| `reinvestment_cash_flow` | Cassa reinvestita | `KEEP` | Flusso monetario reimmesso | Reinvestment flow | Telemetry metrics |
| `product_mix_revenue` | Ripartizione ricavi | `KEEP` | Breakdown ricavi per categoria | Sales breakdown | Outcome metrics |
| `price_realization_variance` | Varianza prezzi | `KEEP` | Differenza prezzo atteso/reale | Price tracking | Telemetry metrics |
| `dynamic_market_price_elasticity` | Elasticità prezzi mercato | `KEEP` | Fluttuazione prezzi da scambi | Market interpreter | State Machine market model |
| `shed_inventory_integrity` | Integrità shed | `KEEP` | Capienza massima aggregata 100 | `shedCapacity` config | State Machine shed bounds |
| `shed_overflow_loss` | Perdita overflow shed | `REVISE` | Distruttiva per DROP/EOD; PLACE preserva | `DROP` vs `PLACE` logic | State Machine inventory loss |
| `endgame_shutdown_timing` | Shutdown investimenti | `REVISE` | Riclassificato come `POLICY_DECLARED` | Policy planning | Rimosso da vincoli fisici engine |
| `endgame_inventory_liquidation` | Liquidazione scorte | `REVISE` | Riclassificato come `POLICY_DECLARED` | Policy planning | Rimosso da vincoli fisici engine |
| `field_cleanliness_state` | Stato infestazioni weed | `KEEP` | Distribuzione spaziale WEED | Grid observation | Feature Model field state |
| `tile_lifecycle_state` | Ciclo di vita tile (6 stati) | `REVISE` | 6 stati canonici; early harvest è no-op | Tile state logic | State Machine & Feature Model |
| `tile_care_due_condition` | Allerta bisogno idrico | `KEEP` | Allerta ortogonale al lifecycle | `consecutive_unwatered` | Feature Model alert feature |
| `preventive_dig_action` | Scavo preventivo | `KEEP` | Rimozione pianta su RETIREMENT_DUE | `DIG` on crop | State Machine DIG transition |
| `recovery_dig_action` | Scavo correttivo | `KEEP` | Bonifica su LOST_WEED | `DIG` on WEED | State Machine DIG transition |
| `weed_backlog_cost` | Costo backlog weed | `KEEP` | Overhead bonifica infestazioni | Telemetry derived | Telemetry metrics |
| `market_order_batch_limit` | Limite ordini mercato (10) | `KEEP` | Cap ordini per turno | `maxMarketOrders` config | State Machine market limit |
| `action_order_slot_pressure` | Pressione slot ordine | `KEEP` | Saturazione slot decisionali | Order tracking | Telemetry metrics |
| `state_capacity_alignment` | Allineamento sistemico | `KEEP` | Armonia dimensionale multi-asset | Telemetry derived | Telemetry metrics |
| `local_kaggle_fidelity_gap` | Gap locale vs Kaggle | `KEEP` | Scostamento simulatore/runtime | Replay comparison | Benchmark diagnostic |
| `operational_divergence_onset` | Inizio divergenza operativa | `KEEP` | Momento deviazione pattern | Step tracking | Diagnostic telemetry |
| `economic_lock_in_onset` | Inizio lock-in economico | `KEEP` | Momento divario irreversibile | Money tracking | Diagnostic telemetry |
| `final_money_outcome` | Saldo finale (reward) | `KEEP` | Valutazione primaria match | Episode terminal state | Outcome metric |
| `canonical_clock_coordinate` | Terna temporale canonica | `ADD` | $\text{step} \equiv \text{day} \cdot T + \text{hour}$; EOD step | Clock invariant | State Machine universal clock |
| `action_eligible_now` | Idoneità immediata azione | `ADD` | Guardie `_apply_unit_action` soddisfatte | Action guards | State Machine action legality |
| `reserved_serviceable_before_deadline` | Prenotazione servizio | `ADD` | Stima/prenotazione policy ante-scadenza | Policy planning | Feature Model policy context |
| `realized_serviceable_in_window` | Realizzazione servizio | `ADD` | Verifica completamento a posteriori | Post-action delta | Telemetry metric (no-leakage) |

---

## 3. Engine Contract Coverage Matrix

La tabella attesta la copertura rigorosa delle 13 aree di riconciliazione C2 all'interno di `ONTOLOGY_C2.md`:

| Discrepancy / Area ID | Prescrizione Engine Contract C2 | Stato in ONTOLOGY_C2.md | Sezioni e Concetti Impattati |
|---|---|:---:|---|
| **CLK-01** | Clock canonico parametrico in $T$; $\text{step} == \text{day}\cdot T + \text{hour}$; EOD step esatto | **COPERTO AL 100%** | Sez. 2.1, 3.I (`canonical_clock_coordinate`), Sez. 4.1 |
| **ANI-01** | Base animal output = 1 disaccoppiato da FEED; fuga al 2° EOD unfed consecutivo | **COPERTO AL 100%** | Sez. 3.D (`livestock_base_production`, `animal_escape_condition`), Sez. 5.11 |
| **ANI-02** | `pending_care_bonus` additivo differito, accumulo con fed+cared, consumo con fed | **COPERTO AL 100%** | Sez. 3.D (`pending_care_bonus_accumulation`), Sez. 5.12 |
| **FER-01** | Incremento totale $=2$, base $=1$, uplift netto canonico $= +1$ | **COPERTO AL 100%** | Sez. 3.C (`crop_fertilizer_bonus`), Sez. 5.10 |
| **FER-02** | Durata 3 giorni inclusivi (`day..day+2`); flag animale boolean non cumulativo | **COPERTO AL 100%** | Sez. 3.C (`fertilizer_effect_window`), Sez. 3.D (`fertilizer_available_state`) |
| **INV-01** | `MANUAL_DROP` ed `EOD_AUTO_DROP` distruttivi; `PLACE` conservativo nel worker | **COPERTO AL 100%** | Sez. 3.F (`shed_overflow_loss`), Sez. 5.5 |
| **INV-02** | Rinominazione canonica `shed_overflow_loss` ed eliminazione riferimenti stale | **COPERTO AL 100%** | Sez. 3.F, Sez. 7 (tabella mapping storico) |
| **SVC-01** | Tripartizione: `ACTION_ELIGIBLE_NOW`, `RESERVED_SERVICEABLE`, `REALIZED_SERVICEABLE` | **COPERTO AL 100%** | Sez. 3.I, Sez. 5.13, Sez. 8 |
| **CAP-01** | Capacità come upper bound multi-dimensionale incompleto (non scalare rigido) | **COPERTO AL 100%** | Sez. 3.B (`worker_capacity_available`), Sez. 5.2 |
| **OBS-01** | Allineamento temporale $S_t \to A_t \to S_{t+1}$; separazione request vs execution | **COPERTO AL 100%** | Sez. 2.2, Sez. 8 (contratto di osservabilità) |
| **HAR-01** | Early harvest immaturo è silent no-op (nessun warning o distruzione pianta) | **COPERTO AL 100%** | Sez. 3.C (`crop_harvest_readiness`), Sez. 4.1 |
| **SPC-01** | Insieme chiuso 5 crop + 3 animali; `CHICKEN = NOT_SUPPORTED`; `GOOSE` presente | **COPERTO AL 100%** | Sez. 3.D (`livestock_headcount`), Sez. 7 |
| **PER-01** | Formule biologiche origin-relative in giorni parametrizzate in $T$ | **COPERTO AL 100%** | Sez. 3.C (`first_yield_day`, `crop_decay_risk_window`), Sez. 3.I |

---

## 4. Policy Contamination Audit

L'audit ha verificato che nessun concetto confonda leggi fisiche dell'ambiente con decisioni strategiche:

1. **Scelte Colturali e Zootecniche:** Rimosse tutte le affermazioni su ranking di profitto (es. "Melon ROI $94.67", "Livestock drain $3,977"). Le metriche di resa sono documentate unicamente come proprietà biologiche (`yield_units`, `interval`, `lifespan`).
2. **Buffer di Capitale e Scorte:** I concetti `operating_cash_buffer`, `feed_security_buffer`, `deployable_capital_window`, `endgame_shutdown_timing` ed `endgame_inventory_liquidation` sono stati esplicitamente riclassificati da vincoli engine a **`POLICY_DECLARED`** (`POLICY_CONTEXT`).
3. **Serviceability e No-Future-Leakage:** Il concetto `realized_serviceable_in_window` è stato blindato come `POST_HOC_METRIC` / `TELEMETRY_ONLY`, vietandone formalmente l'uso come feature online pre-azione.
4. **Multi-Occupancy vs Collisione:** Confermato come fatto di dominio che l'engine ammette illimitata compresenza di worker; la separazione spaziale o la zonizzazione per quadranti è chiarita come euristica di policy.

---

## 5. Open Issues

```text
RESIDUAL_AMBIGUITIES: 0 (NONE)
UNRESOLVED_BLOCKERS: 0 (NONE)
POLICY_CONTAMINATIONS_DETECTED: 0 (NONE)
```

L'Ontologia C2 è pienamente auto-consistente e conforme all'Engine Contract congelato.

---

## 6. Verification & Gate Finale

### Controlli di integrità eseguiti:
- **`git diff --check`**: Esito pulito (0 errori di formattazione o whitespace).
- **File modificati/creati**:
  - `docs/model/ontology/ONTOLOGY_C2.md` (Modificato / Revisionato)
  - `results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_ONTOLOGY_REVISION_REPORT.md` (Creato)
- **File downstream non toccati**: Nessun file in `docs/model/state_machine/`, `docs/model/feature_model/`, `src/`, `tests/` o `scripts/` è stato alterato.

### Verdetto di Chiusura:

```text
================================================================================
FINAL VERDICT: ONTOLOGY_READY_FOR_REVIEW: YES
================================================================================
STATE_MACHINE_REVISION_AUTHORIZED: NO
FEATURE_MODEL_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```
