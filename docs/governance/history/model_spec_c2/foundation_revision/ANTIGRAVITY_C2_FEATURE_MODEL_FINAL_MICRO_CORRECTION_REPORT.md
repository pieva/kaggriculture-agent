# ANTIGRAVITY C2 — FEATURE MODEL FINAL MICRO-CORRECTION REPORT

```text
DOCUMENT_ID: ANTIGRAVITY_C2_FEATURE_MODEL_FINAL_MICRO_CORRECTION_REPORT
AUTHOR: Antigravity
DATE: 2026-08-31
PHASE: Foundation Revision / Feature Model C2 Final Micro-Correction Pass
TARGET_DOCUMENT: docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
BASELINE_AUTHORITY: docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md (FROZEN)
ONTOLOGY_AUTHORITY: docs/foundation/ontology/ONTOLOGY_C2.md (FROZEN)
STATE_MACHINE_AUTHORITY: docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md (FROZEN)
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
STATUS: COMPLETE — READY FOR FREEZE REVIEW
```

---

## 1. Executive Verdict

Antigravity ha eseguito e completato la **micro-correzione finale** del **Kaggriculture Feature Model C2** (`docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`), recependo con assoluta precisione i quattro punti sollevati dalla freeze review indipendente:
1. Corretto `policy_retirement_due` (`POL-RET`) come **puro `POLICY_CONTEXT`** senza alcuna regola biologica hardcoded e senza restrizione a colture ongoing;
2. Eseguito il source-check sull'engine reale (`kaggriculture.py` / `kaggriculture.json`) riconciliando la tassonomia delle azioni in 23 predicati di ammissibilità (`ELG-01` .. `ELG-23`);
3. Completato il catalogo della telemetria post-hoc (`POST-01` .. `POST-38`) con la piena decomposizione per specie vegetale/animale di mangime, strutture, bilancio fisico, timing, fertilizzante e assorbimento risorse;
4. Risolta la collisione semantica di `realized_serviceable_in_window`, assegnandole l'ID univoco `POST-02`.

```text
RETIREMENT_DUE_IS_PURE_POLICY_CONTEXT: YES
RETIREMENT_DUE_NO_BIOLOGICAL_DECISION_RULE: YES

ACTION_TAXONOMY_SOURCE_CHECK_COMPLETE: YES
ACTION_TAXONOMY_SOURCE_ALIGNED: YES
ELIGIBILITY_CATALOG_SOURCE_ALIGNED: YES

PERFORMANCE_DECOMPOSITION_COMPLETE: YES
FEED_TELEMETRY_BY_SPECIES_PRESENT: YES
STRUCTURE_COST_AND_OCCUPANCY_TELEMETRY_PRESENT: YES
PRODUCTION_FLOW_SPLIT_CROP_LIVESTOCK: YES
WORKER_SERVICE_ACTION_TELEMETRY_PRESENT: YES
ACTIVATION_AND_OUTPUT_TIMING_PRESENT: YES
FERTILIZER_FLOW_TELEMETRY_PRESENT: YES
CAUSAL_ATTRIBUTION_LIMITS_EXPLICIT: YES

REALIZED_SERVICEABLE_HAS_UNIQUE_POST_ID: YES
POST_ID_UNIQUENESS: YES
POST_ID_REFERENCE_INTEGRITY: YES
FEATURE_ID_UNIQUENESS: YES
FEATURE_ID_REFERENCE_INTEGRITY: YES
ONTOLOGY_MAPPING_REFERENCE_INTEGRITY: YES
ENGINE_COVERAGE_MAPPING_REFERENCE_INTEGRITY: YES

NO_FUTURE_LEAKAGE: YES
ENVIRONMENT_FEATURE_VECTOR_POLICY_NEUTRAL: YES
MERMAID_ARCHITECTURAL_ALIGNMENT: YES
FROZEN_INPUTS_CONSISTENT: YES

FEATURE_MODEL_READY_FOR_FREEZE_REVIEW: YES
```

---

## 2. Frozen Input Verification

Tutti gli input normativi congelati rimangono immutati e conformi:
- **Engine Contract:** [`ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md) (`FROZEN`)
- **Ontology C2:** [`ONTOLOGY_C2.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/foundation/ontology/ONTOLOGY_C2.md) (`FROZEN`)
- **State Machine C2:** [`KAGGRICULTURE_STATE_MACHINE_C2.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md) (`FROZEN`)
- **Period Ledger Audit:** [`CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/governance/history/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md) (`FROZEN`)

---

## 3. `policy_retirement_due` Correction

- **Rimozione di regole decisionali biologiche:** Eliminata la formula `is_ongoing(crop) and ongoing_events_exhausted`;
- **Inquadramento come puro `POLICY_CONTEXT`:** `policy_retirement_due` (`POL-RET`) è formalmente definito come un flag deliberativo assegnato dalla policy/Decision Lifecycle downstream per marcare una pianta candidata al ritiro (tramite azione `DIG`);
- **Invarianza dell'Environment Feature Vector:** L'Environment Derived Tile Classifier rimane confinato alle 5 viste pure (`OUT_OF_SCOPE`, `LOST_WEED`, `EMPTY_AVAILABLE`, `HARVEST_READY`, `GROWING`).

---

## 4. Engine Action Taxonomy Source-Check

È stato condotto un audit sistematico sul source code dell'engine `kaggle-environments` 1.32.7 (`kaggriculture.py` e `kaggriculture.json`).

### Evidenza Source:
- **Unit Actions (`_apply_unit_action`, righe 312-531):**
  - Movimento: `NORTH`, `SOUTH`, `EAST`, `WEST`, `PASS`;
  - Operazioni Shed:
    - `PICKUP <item> [n]`: preleva merce dallo shed verso worker (righe 358-375);
    - `PLACE <item> [n]` (Shed branch): trasferimento conservativo worker $\to$ shed fino a capienza 100, l'eccesso resta nel worker (righe 393-410);
    - `DROP`: scarico distruttivo worker $\to$ shed fino a capienza 100, **l'eccesso viene cancellato** (`del inv[item]`, righe 343-356);
  - Operazioni Strutture & Animali:
    - `PLACE <animal>` (Animal branch): colloca animale da worker su struttura vuota (`COOP`/`PASTURE`, righe 384-392);
    - `FEED`: nutre animale consumando 1 Wheat da worker (righe 505-513);
    - `CARE`: imposta `cared_today = True` (righe 524-530);
    - `COLLECT_FERTILIZER`: preleva fertilizzante da animale (righe 515-522);
    - `BUILD_COOP`, `BUILD_PASTURE`: edifica strutture su tile libera (righe 493-503);
  - Operazioni Colturali:
    - `PLANT <crop>`: consuma semente da `private.seeds` (righe 417-429);
    - `WATER`: irriga pianta (righe 431-444);
    - `HARVEST`: raccoglie resa colturale o prodotto animale (righe 446-473);
    - `FERTILIZE`: consuma 1 fertilizzante da worker, estende fino a `day + 2` (righe 475-482);
    - `DIG`: rimuove piante, erbacce o strutture vuote (righe 484-491);
- **Market Orders (`_process_market` / `_parse_order`, righe 544-688):**
  - `BUY_SEED <crop> <n>`, `BUY_PRODUCT <item> <n>`, `BUY_ANIMAL <animal> <n>`, `SELL <item> <n>`, `HIRE`, `BUY_LAND`.

```text
ACTION_TAXONOMY_SOURCE_CHECK_COMPLETE: YES
ACTION_TAXONOMY_SOURCE_ALIGNED: YES
```

---

## 5. Eligibility Catalog Reconciliation

I predicati di ammissibilità `action_eligible_now` sono stati mappati biunivocamente su tutte le forme di azione/richiesta engine:

| Engine Action / Request | Parametri Engine | Feature Eligibility ID | Source Evidence | Note di Ammissibilità / Guardie |
|---|---|---|---|---|
| `NORTH`/`SOUTH`/`EAST`/`WEST` | N/A | `ELG-01` | `kaggriculture.py:323` | Destinazione entro coordinate farm $[0, \text{dim}-1]$ |
| `PASS` | N/A | `ELG-02` | `kaggriculture.py:334` | Sempre ammissibile per worker attivo |
| `PICKUP` | `<item> [n]` | `ELG-03` | `kaggriculture.py:358` | Adiacente a shed, scorta shed $> 0$, spazio worker $> 0$ |
| `PLACE` (Shed branch) | `<item> [n]` | `ELG-04` | `kaggriculture.py:393` | Adiacente a shed, merce in worker inv, spazio shed $> 0$ (conservativo) |
| `PLACE` (Animal branch) | `<animal>` | `ELG-05` | `kaggriculture.py:384` | Su struttura vuota compatibile, animale in worker inv |
| `DROP` | N/A | `ELG-06` | `kaggriculture.py:343` | Adiacente a shed, worker possiede beni (distruttivo oltre 100) |
| `PLANT` | `<crop>` | `ELG-07` | `kaggriculture.py:417` | Su tile libera posseduta (`None`), sementi $\ge 1$ |
| `WATER` | N/A | `ELG-08` | `kaggriculture.py:431` | Su tile `PLANT`, $\text{watered\_today} == \text{False}$ |
| `HARVEST` (Crop) | N/A | `ELG-09` | `kaggriculture.py:451` | Su tile `PLANT`, $\text{CRP-10} == \text{True}$, spazio worker $> 0$ |
| `HARVEST` (Animal) | N/A | `ELG-10` | `kaggriculture.py:469` | Su struttura con animale, `output_available == True`, spazio worker $> 0$ |
| `FERTILIZE` | N/A | `ELG-11` | `kaggriculture.py:475` | Su tile `PLANT`, fertilizzante in worker inv $\ge 1$ |
| `DIG` | N/A | `ELG-12` | `kaggriculture.py:484` | Su tile arabile (`PLANT`, `WEED` o struttura vuota priva di animale) |
| `BUILD_COOP` | N/A | `ELG-13` | `kaggriculture.py:493` | Su tile libera posseduta (`None`) |
| `BUILD_PASTURE` | N/A | `ELG-14` | `kaggriculture.py:499` | Su tile libera posseduta (`None`) |
| `FEED` | N/A | `ELG-15` | `kaggriculture.py:505` | Su struttura con animale, $\text{fed\_today} == \text{False}$, Wheat in worker $\ge 1$ |
| `CARE` | N/A | `ELG-16` | `kaggriculture.py:524` | Su struttura con animale, $\text{cared\_today} == \text{False}$ |
| `COLLECT_FERTILIZER` | N/A | `ELG-17` | `kaggriculture.py:515` | Su struttura con animale, `fertilizer_available == True`, spazio worker $> 0$ |
| `BUY_SEED` | `<crop> <n>` | `ELG-18` | `kaggriculture.py:602` | Slot batch $< 10$, cassa $\ge \text{costo}$ |
| `BUY_PRODUCT` | `<item> <n>` | `ELG-19` | `kaggriculture.py:598` | Slot batch $< 10$, cassa $\ge \text{prezzo}$, spazio shed $> 0$ |
| `BUY_ANIMAL` | `<animal> <n>` | `ELG-20` | `kaggriculture.py:604` | Slot batch $< 10$, cassa $\ge \text{costo}$, spazio shed $> 0$ |
| `SELL` | `<item> <n>` | `ELG-21` | `kaggriculture.py:596` | Slot batch $< 10$, merce presente nello shed $\ge 1$ |
| `HIRE` | N/A | `ELG-22` | `kaggriculture.py:576` | Slot batch $< 10$, cassa $\ge \text{hire\_cost}$ |
| `BUY_LAND` | N/A | `ELG-23` | `kaggriculture.py:579` | Slot batch $< 10$, cassa $\ge \text{land\_cost}$, quadranti bloccati disponibili |

```text
ELIGIBILITY_CATALOG_SOURCE_ALIGNED: YES
```

---

## 6. Performance Decomposition Telemetry Completion

La Sezione 16 del Feature Model è stata strutturata ed espansa in 38 metriche post-hoc esaustive (`POST-01` .. `POST-38`):
- **Cassa & Serviceability:** `POST-01` (Reward terminale), `POST-02` (`realized_serviceable_in_window`);
- **Ricavi Diretti per Specie:** `POST-03` (Colture), `POST-04` (Prodotti animali), `POST-05` (Fertilizzante venduto);
- **Costi Diretti di Investimento e Conduzione:** `POST-06` (Sementi), `POST-07` (Animali), `POST-08` (Strutture per tipo), `POST-09` (Mangime acquistato), `POST-10` (Fertilizzante acquistato), `POST-11` (Assunzioni Hands), `POST-12` (Sblocco Terreni);
- **Bilancio Fisico per Specie:** `POST-13`..`POST-14` (Generate), `POST-15`..`POST-16` (Raccolte), `POST-17`..`POST-18` (Vendute), `POST-19`..`POST-20` (Perse);
- **Mangime & Fertilizzante:** `POST-21` (Consumo Wheat mangime), `POST-22`..`POST-25` (Ciclo fertilizzante: generato da animale, raccolto, applicato a coltura, venduto);
- **Timing:** `POST-26` (Giorno attivazione per specie), `POST-27` (Primo output realizzato), `POST-28` (Ultimo output utile);
- **Assorbimento Risorse & Routing:** `POST-29` (`necessary_transit_fraction`), `POST-30` (`routing_completion_efficiency`), `POST-31` (`economic_lock_in_onset`), `POST-32`..`POST-34` (Perdite shed overflow, weed, fughe animali), `POST-35`..`POST-36` (Giorni occupazione suolo e strutture per specie), `POST-37` (Breakdown azioni lavoratore per categoria), `POST-38` (Contributo netto contabile diretto per specie).

---

## 7. `realized_serviceable_in_window` ID Correction

- A `realized_serviceable_in_window` è stato assegnato in modo univoco ed esclusivo l'identificativo **`POST-02`**;
- Aggiornate tutte le occorrenze, le sezioni normative (§2, §14, §16), il Diagramma Mermaid (§18), e le matrici di copertura (§19 Ref SVC-01, §20 Dominio Clock).

---

## 8. Feature / Post ID Integrity Audit

Audit sistematico di tutti gli identificatori:
- **Feature IDs (`TMP-01..10`, `FRM-01..05`, `CRP-01..15`, `CAR-01..04`, `FRT-01..05`, `LIV-01..15`, `LIV-STRUCT`, `WRK-01..09`, `INV-01..08`, `MKT-01..09`, `MKT-LIMIT`, `ELG-01..23`, `POL-WS`, `POL-RES`, `POL-CAP`, `POL-RET`):** univoci, definiti nel Master Catalog con 17 campi completi;
- **Post-Hoc Metric IDs (`POST-01..38`):** univoci, definiti in Sezione 16, privi di collisioni o riferimenti dangling.

```text
POST_ID_UNIQUENESS: YES
POST_ID_REFERENCE_INTEGRITY: YES
FEATURE_ID_UNIQUENESS: YES
FEATURE_ID_REFERENCE_INTEGRITY: YES
```

---

## 9. Ontology Mapping Integrity

Tutti i concetti dell'Ontology C2 citati nella matrice §20 mappano fedelmente sui feature IDs e post IDs reali senza alcuna divergenza:
- `necessary_transit_fraction` $\to$ `POST-29`;
- `routing_completion_efficiency` $\to$ `POST-30`;
- `economic_lock_in_onset` $\to$ `POST-31`;
- `shed_overflow_loss` $\to$ `INV-07`, `INV-08`, `POST-32`;
- `realized_serviceable_in_window` $\to$ `POST-02`.

```text
ONTOLOGY_MAPPING_REFERENCE_INTEGRITY: YES
```

---

## 10. Engine Discrepancy Coverage Integrity

Tutti i 14 punti di riconciliazione dell'Engine Contract C2 risultano coperti e verificati:
- `CLK-01`: `TMP-01`..`TMP-10`;
- `ANI-01`, `ANI-02`: `LIV-06`, `LIV-07`, `LIV-08`, `LIV-09`, `LIV-14`, `ELG-15`, `ELG-16`;
- `FER-01`, `FER-02`: `FRT-01`..`FRT-05`, `LIV-10`, `ELG-11`, `ELG-17`;
- `INV-01`, `INV-02`: `INV-06`..`INV-08`, `ELG-04`, `ELG-06`, `POST-32`;
- `SVC-01`: `ELG-01`..`ELG-23`, `POL-RES`, `POST-02`;
- `CAP-01`: `WRK-06`, `INV-04`, `MKT-LIMIT`, `LIV-STRUCT`, `POL-CAP`;
- `OBS-01`: `ELG-01`..`ELG-23`;
- `HAR-01`: `CRP-09`, `CRP-10`, `ELG-09`;
- `SPC-01`: `CRP-02`, `LIV-01`, `MKT-08`, `MKT-09`;
- `PER-01`: `CRP-04`, `CRP-08`, `CRP-14`, `LIV-12`, `LIV-15`;
- `AGG-01`: SHA-256 fingerprint verified (`4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d`).

```text
ENGINE_COVERAGE_MAPPING_REFERENCE_INTEGRITY: YES
```

---

## 11. Mermaid Regression Check

Il diagramma Mermaid (§18) è stato validato con script di test:
- 0 tag non consentiti;
- 0 fan-in con `&`;
- Ramo Online e Ramo Offline rigorosamente disaccoppiati;
- Ingressi separati verso il Decision Controller per Environment Feature Vector e Policy Context.

```text
MERMAID_FEATURE_MODEL_PRESENT: YES
MERMAID_FEATURE_MODEL_RENDERABLE: YES
MERMAID_ARCHITECTURAL_ALIGNMENT: YES
```

---

## 12. Files Modified

- **`docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`** (Final micro-correction pass completato con successo);
- **`docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FEATURE_MODEL_FINAL_MICRO_CORRECTION_REPORT.md`** (Creato).

---

## 13. Residual Issues

```text
RESIDUAL_BLOCKERS: 0 (NONE)
OPEN_AMBIGUITIES: 0 (NONE)
POLICY_CONTAMINATION_IN_ENGINE_STATE: 0 (NONE)
FUTURE_LEAKAGE_VULNERABILITIES: 0 (NONE)
```

---

## 14. Final Gate

```text
================================================================================
RETIREMENT_DUE_IS_PURE_POLICY_CONTEXT: YES
RETIREMENT_DUE_NO_BIOLOGICAL_DECISION_RULE: YES

ACTION_TAXONOMY_SOURCE_CHECK_COMPLETE: YES
ACTION_TAXONOMY_SOURCE_ALIGNED: YES
ELIGIBILITY_CATALOG_SOURCE_ALIGNED: YES

PERFORMANCE_DECOMPOSITION_COMPLETE: YES
FEED_TELEMETRY_BY_SPECIES_PRESENT: YES
STRUCTURE_COST_AND_OCCUPANCY_TELEMETRY_PRESENT: YES
PRODUCTION_FLOW_SPLIT_CROP_LIVESTOCK: YES
WORKER_SERVICE_ACTION_TELEMETRY_PRESENT: YES
ACTIVATION_AND_OUTPUT_TIMING_PRESENT: YES
FERTILIZER_FLOW_TELEMETRY_PRESENT: YES
CAUSAL_ATTRIBUTION_LIMITS_EXPLICIT: YES

REALIZED_SERVICEABLE_HAS_UNIQUE_POST_ID: YES
POST_ID_UNIQUENESS: YES
POST_ID_REFERENCE_INTEGRITY: YES
FEATURE_ID_UNIQUENESS: YES
FEATURE_ID_REFERENCE_INTEGRITY: YES
ONTOLOGY_MAPPING_REFERENCE_INTEGRITY: YES
ENGINE_COVERAGE_MAPPING_REFERENCE_INTEGRITY: YES

NO_FUTURE_LEAKAGE: YES
ENVIRONMENT_FEATURE_VECTOR_POLICY_NEUTRAL: YES
MERMAID_ARCHITECTURAL_ALIGNMENT: YES
FROZEN_INPUTS_CONSISTENT: YES

FEATURE_MODEL_READY_FOR_FREEZE_REVIEW: YES
================================================================================
FEATURE_MODEL_FREEZE: NO
DECISION_LIFECYCLE_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```
