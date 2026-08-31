# ANTIGRAVITY C2 — FEATURE MODEL REVISION REPORT

```text
DOCUMENT_ID: ANTIGRAVITY_C2_FEATURE_MODEL_REVISION_REPORT
AUTHOR: Antigravity
DATE: 2026-08-31
PHASE: Foundation Revision / Feature Model C2 Revision Pass
TARGET_DOCUMENT: docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
BASELINE_AUTHORITY: results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md (FROZEN)
ONTOLOGY_AUTHORITY: docs/model/ontology/ONTOLOGY_C2.md (FROZEN)
STATE_MACHINE_AUTHORITY: docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md (FROZEN)
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
STATUS: COMPLETE — READY FOR INDEPENDENT REVIEW
```

---

## 1. Executive Verdict

Antigravity ha completato con successo la revisione formale del **Kaggriculture Feature Model C2** (`docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`).

Il Feature Model C2 definisce in modo rigoroso, causale, period-aware e privo di future-leakage l'insieme completo delle grandezze osservabili e derivabili a tempo $t$ utilizzabili dai controller decisionali, garantendo il pieno allineamento ai layer normativi congelati precedenti (Engine Contract, Ontology C2, State Machine C2).

```text
STATE_MACHINE_HOUSEKEEPING_COMPLETE: YES
FEATURE_MODEL_REVISION_COMPLETE: YES
FROZEN_INPUTS_CONSISTENT: YES
FEATURE_SCHEMA_COMPLETE: YES
ONLINE_OBSERVABILITY_EXPLICIT: YES
NO_FUTURE_LEAKAGE: YES
TILE_CLASSIFIER_DEFINED: YES
CROP_FEATURES_PERIOD_AWARE: YES
LIVESTOCK_FEATURES_PERIOD_AWARE: YES
ACTION_ELIGIBILITY_EXPLICIT: YES
SERVICEABILITY_TRIPARTITION_PRESERVED: YES
POST_HOC_TELEMETRY_SEPARATED: YES
EPISODE_PROVENANCE_DEFINED: YES
MERMAID_FEATURE_MODEL_PRESENT: YES
MERMAID_FEATURE_MODEL_RENDERABLE: YES
FEATURE_MODEL_READY_FOR_REVIEW: YES
```

---

## 2. Frozen Input Verification

Tutti i documenti a monte della catena normativa risultano congelati e sono stati assunti come autorità inderogabile:
- **Engine Contract Reconciliation:** [`ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md) (`FROZEN`)
- **Ontology C2:** [`ONTOLOGY_C2.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/model/ontology/ONTOLOGY_C2.md) (`FROZEN`)
- **Environment State Machine C2:** [`KAGGRICULTURE_STATE_MACHINE_C2.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md) (`FROZEN`)
- **Period Ledger Audit:** [`CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md) (`FROZEN`)

Nessun conflitto con i layer frozen è stato rilevato.

---

## 3. State Machine Housekeeping Correction

Prima dell'avvio della stesura del Feature Model, è stata applicata l'unica correzione editoriale autorizzata in `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`:
- Nel titolo del subgraph Mermaid (Sezione 8), la dicitura `2. Crop and Tile Lifecycle (6 Canonical States)` è stata sostituita con `2. Crop and Tile Lifecycle (6 Derived Views)`.
- Successivamente, il file della State Machine è stato impostato come **READ-ONLY**.

---

## 4. Feature Architecture

Il Feature Model struttura l'informazione su 4 livelli di granularità operativa online, con totale separazione dal ramo di telemetria retrospettiva:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ONLINE RUNTIME INTERFACE (Tempo reale t)                                               │
├──────────────────┬─────────────────────────────────────────────────────────────────────┤
│ 1. Global        │ Clock parametrico (T), cassa online, ordini residui, aggregati      │
├──────────────────┼─────────────────────────────────────────────────────────────────────┤
│ 2. Per-Tile      │ Kind, specie, età biologica, resa, readiness, allerta anti-loss     │
│                  │ Classifier delle 6 Derived Views (OUT_OF_SCOPE..LOST_WEED)          │
├──────────────────┼─────────────────────────────────────────────────────────────────────┤
│ 3. Per-Animal    │ Specie (Goose, Cow, Sheep), alimentazione, cura, rischio fuga, bonus│
├──────────────────┼─────────────────────────────────────────────────────────────────────┤
│ 4. Per-Worker    │ Coordinate [x,y], inventario, distanze geometriche, action eligibility│
└──────────────────┴─────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼ (Separazione Rigida)
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ OFFLINE REVIEW TELEMETRY (Post-Episode Only)                                           │
├──────────────────┬─────────────────────────────────────────────────────────────────────┤
│ Replay Trace     │ Metric decomposition, routing efficiency, final reward, lock-in     │
└──────────────────┴─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Online Observability Audit

Ogni feature è stata catalogata secondo 5 classi di osservabilità mutuamente esclusive:
1. `ONLINE_OBSERVABLE`: grandezze visibili direttamente nell'osservazione o stato privato a tempo $t$;
2. `ONLINE_DERIVABLE`: grandezze derivate deterministicamente al tick corrente;
3. `POLICY_CONTEXT`: asserzioni o contesti deliberativi della policy (`in_working_set`, `reserved_serviceable`);
4. `TELEMETRY_ONLY`: eventi o esiti post-azione intra-step;
5. `OUTCOME_ONLY` / `POST_HOC_METRIC`: metriche consolitate a posteriori a fine episodio.

---

## 6. Derived Feature Audit

Tutte le feature derivate possiedono una formula matematica/logica esplicita e deterministica, priva di parametri magici o dipendenze non tracciate. Il calcolo si basa unicamente su grandezze $S_{\le t}$.

---

## 7. Tile Classifier Audit (6 Derived Lifecycle Views)

Il Feature Model formalizza il classifier totale computazionale con predicati logici chiusi e precedenza rigida a cascata:
1. `OUT_OF_SCOPE` (non posseduta / `"LOCKED"`, fuori dal working set, o struttura `COOP`/`PASTURE`);
2. `LOST_WEED` (`kind == "WEED"`);
3. `EMPTY_ASSIGNED` (`kind == None` posseduta in working set);
4. `HARVEST_READY` (`kind == "PLANT"` con `crop_harvest_readiness == True`);
5. `RETIREMENT_DUE` (`kind == "PLANT"` ongoing con ciclo biologico esaurito secondo criterio di policy);
6. `GROWING` (fallback per pianta viva in accrescimento).

*Governance:* `RETIREMENT_DUE` è chiaramente documentata come *derived/policy classification* e non come transizione causale nativa dell'engine.

---

## 8. Crop Feature Audit

Tutte le colture rispettano il period ledger congelato:
- `WHEAT`: $d_0 + 2$, water $2 \dots 4$, max yield 6, non-ongoing, lifespan $(d_0 + 5)T$;
- `CARROT`: $d_0 + 2$, water $2 \dots 3$, max yield 4, non-ongoing, lifespan $(d_0 + 4)T$;
- `TOMATO`: $d_0 + 8$, intervallo 1d (4 eventi), max yield 4, ongoing, lifespan $(d_0 + 12)T$;
- `STRAWBERRY`: $d_0 + 10$, intervallo 2d (4 eventi), max yield 4, ongoing, lifespan $(d_0 + 17)T$;
- `MELON`: prima raccolta legale $d_0 + 10$, water $6 \dots 12$, max yield 6, non-ongoing, lifespan $(d_0 + 13)T$.
- **Readiness legale:** $\text{crop\_harvest\_readiness} \iff \text{kind} == \text{PLANT} \land \text{yield} > 0 \land \text{day} - \text{planted} \ge \text{first\_yield\_day}$.

---

## 9. Livestock Feature Audit

- **Closed set:** `GOOSE` (\$300, Coop, max 4), `COW` (\$400, Pasture, max 6), `SHEEP` (\$500, Pasture, max 6). `CHICKEN = NOT_SUPPORTED`;
- **Produzione Base:** disaccoppiata da `FEED` se l'animale non è fuggito ed è nel giorno biologico programmato;
- **Care Bonus:** `pending_care_bonus` consumato alla produzione se alimentato è unicamente quello preesistente; il nuovo bonus accumulato per la cura odierna è registrato per eventi futuri;
- **Fertilizer:** flag booleano non cumulativo `fertilizer_available = True` a EOD per animali vivi.

---

## 10. Worker / Spatial Feature Audit

- Coordinate $[x, y]$ e tracciamento inventari per ciascun lavoratore;
- Distanze calcolate esplicitamente come **geometric distance** (Manhattan distance);
- `worker_multi_occupancy = allowed` (nessuna collisione fisica nell'ambiente);
- Esclusione online di metriche di efficienza di routing (`necessary_transit_fraction`).

---

## 11. Inventory / Storage Feature Audit

Modellate distintamente le 3 semantiche di scarico merci sullo shed (capacità fissa 100):
- `PLACE`: conservativo (l'eccedenza resta nel lavoratore);
- `MANUAL_DROP`: distruttivo (l'eccedenza oltre capienza viene cancellata);
- `EOD_AUTO_DROP`: distruttivo (l'eccedenza totale dei worker oltre 100 viene distrutta).

---

## 12. Market / Capital Feature Audit

- `current_money_state`: saldo cassa liquido online osservabile;
- `market_orders_used_this_turn` e `market_orders_remaining_turn`: basati sul batch limit strutturale di 10 ordini/turno;
- `final_money_outcome`: classificata rigorosamente come `OUTCOME_ONLY` ed esclusa dal vettore online.

---

## 13. Action Eligibility Audit (`action_eligible_now`)

Formalizzati i predicati deterministici di ammissibilità istantanea per tutte le 17 azioni possibili (`MOVE`, `PLANT`, `WATER`, `HARVEST`, `DIG`, `FERTILIZE`, `BUILD_COOP`, `BUILD_PASTURE`, `PLACE_ANIMAL`, `FEED`, `CARE`, `COLLECT_FERT`, `PLACE_SHED`, `MANUAL_DROP`, `BUY/SELL`, `BUY_LAND`, `HIRE`). Per ciascuna è documentata la conseguenza di violazione (silent no-op).

---

## 14. Serviceability Separation Audit

Separati i tre livelli:
- `action_eligible_now` (`ONLINE_DERIVABLE`): predicato engine-derived;
- `reserved_serviceable_before_deadline` (`POLICY_CONTEXT`): prenotazione logica di policy;
- `realized_serviceable_in_window` (`POST_HOC_METRIC`): consuntivo post-hoc.

---

## 15. Horizon / No-Leakage Audit

Le feature di orizzonte (`days_until_first_legal_harvest`, `steps_until_max_lifespan`, `days_remaining`) derivano unicamente da costanti biologiche e dal clock corrente, senza formulare previsioni o speculazioni su ricavi futuri o ROI.

---

## 16. Post-Hoc Telemetry Specification

Definite formalmente 8 metriche retrospettive (`POST-01`..`POST-08`) per la decomposizione delle performance post-match (es. `final_money_outcome`, `realized_serviceable_in_window`, `necessary_transit_fraction`, `routing_completion_efficiency`, `economic_lock_in_onset`, perdite da disidratazione e overflow).

---

## 17. Ontology Coverage Matrix

Tutti gli 85 concetti canonici dell'Ontology C2 sono stati mappati esaustivamente:
- 48 concetti mappati come `FEATURE` online;
- 18 concetti mappati come `POLICY_CONTEXT` o `CONTEXT_ONLY`;
- 19 concetti mappati come `POST_HOC_ONLY` o `TELEMETRY_ONLY`.

---

## 18. Engine Discrepancy Coverage Matrix (14 Ref IDs)

Tutti i 14 punti di riconciliazione dell'Engine Contract C2 (`CLK-01`, `ANI-01`, `ANI-02`, `FER-01`, `FER-02`, `INV-01`, `INV-02`, `SVC-01`, `CAP-01`, `OBS-01`, `HAR-01`, `SPC-01`, `PER-01`, `AGG-01`) sono coperti al 100% nel Feature Model.

---

## 19. Mermaid Validation

Il Diagramma Mermaid inserito nella Sezione 18 di `KAGGRICULTURE_FEATURE_MODEL_C2.md` è stato validato tramite script:
- 0 tag HTML `<br/>` o simboli vietati negli edge labels;
- Archi espliciti individuali (0 fan-in con `&`);
- Separazione visiva netta tra pipeline online e ramo diagnostico offline.

---

## 20. Files Modified

- **`docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`** (Housekeeping: aggiornato titolo subgraph Mermaid);
- **`docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`** (Creato/riscritto interamente secondo lo standard normativo C2);
- **`results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FEATURE_MODEL_REVISION_REPORT.md`** (Creato).

---

## 21. Open Issues

```text
RESIDUAL_AMBIGUITIES: 0 (NONE)
UNRESOLVED_BLOCKERS: 0 (NONE)
FUTURE_LEAKAGE_RISKS: 0 (NONE)
```

---

## 22. Final Gate

```text
================================================================================
STATE_MACHINE_HOUSEKEEPING_COMPLETE: YES

FEATURE_MODEL_REVISION_COMPLETE: YES
FROZEN_INPUTS_CONSISTENT: YES
FEATURE_SCHEMA_COMPLETE: YES
ONLINE_OBSERVABILITY_EXPLICIT: YES
NO_FUTURE_LEAKAGE: YES
TILE_CLASSIFIER_DEFINED: YES
CROP_FEATURES_PERIOD_AWARE: YES
LIVESTOCK_FEATURES_PERIOD_AWARE: YES
ACTION_ELIGIBILITY_EXPLICIT: YES
SERVICEABILITY_TRIPARTITION_PRESERVED: YES
POST_HOC_TELEMETRY_SEPARATED: YES
EPISODE_PROVENANCE_DEFINED: YES
MERMAID_FEATURE_MODEL_PRESENT: YES
MERMAID_FEATURE_MODEL_RENDERABLE: YES
FEATURE_MODEL_READY_FOR_REVIEW: YES
================================================================================
FEATURE_MODEL_FREEZE: NO
DECISION_LIFECYCLE_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```
