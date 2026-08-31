# ANTIGRAVITY C2 — FEATURE MODEL TARGETED CORRECTION REPORT

```text
DOCUMENT_ID: ANTIGRAVITY_C2_FEATURE_MODEL_TARGETED_CORRECTION_REPORT
AUTHOR: Antigravity
DATE: 2026-08-31
PHASE: Foundation Revision / Feature Model C2 Targeted Correction Pass
TARGET_DOCUMENT: docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
BASELINE_AUTHORITY: results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md (FROZEN)
ONTOLOGY_AUTHORITY: docs/model/ontology/ONTOLOGY_C2.md (FROZEN)
STATE_MACHINE_AUTHORITY: docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md (FROZEN)
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
STATUS: COMPLETE — READY FOR FREEZE REVIEW
```

---

## 1. Executive Verdict

Antigravity ha completato con successo il **targeted correction pass** sul **Kaggriculture Feature Model C2** (`docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`), risolvendo integralmente entrambi i blocker P0 e tutti i rilievi P1 identificati in sede di Independent Review.

```text
TILE_CLASSIFIER_POLICY_NEUTRAL: YES
WORKING_SET_ORTHOGONAL_TO_ENVIRONMENT_VIEW: YES
RETIREMENT_DUE_POLICY_DEPENDENCY_EXPLICIT: YES

FEATURE_CONTRACT_MATERIALIZED: YES
ALL_CANONICAL_FEATURES_HAVE_COMPLETE_SCHEMA: YES
DANGLING_FEATURE_REFERENCES_ZERO: YES

ONLINE_OBSERVABILITY_PROVENANCE_AUDITED: YES
MARKET_ORDER_CONTEXT_CLASSIFIED_CORRECTLY: YES
NO_ENGINE_INTERNAL_PROMOTED_TO_ONLINE_WITHOUT_EVIDENCE: YES

OVERFLOW_EXPOSURE_NON_PREDICTIVE: YES
NO_FUTURE_LEAKAGE: YES

ENVIRONMENT_FEATURE_VECTOR_POLICY_NEUTRAL: YES
POLICY_CONTEXT_SEPARATE_CONTROLLER_INPUT: YES
POST_HOC_SEPARATE_FROM_ONLINE: YES

PERFORMANCE_DECOMPOSITION_COMPLETE: YES
CROP_SPECIES_ECONOMIC_TELEMETRY_PRESENT: YES
LIVESTOCK_SPECIES_ECONOMIC_TELEMETRY_PRESENT: YES
RESOURCE_ABSORPTION_TELEMETRY_PRESENT: YES
CAUSAL_ATTRIBUTION_LIMITS_EXPLICIT: YES

EPISODE_PROVENANCE_DEFINED: YES
PROGRESSIVE_RUN_EPISODE_ID_SUPPORTED: YES

MERMAID_FEATURE_MODEL_PRESENT: YES
MERMAID_FEATURE_MODEL_RENDERABLE: YES
MERMAID_ARCHITECTURAL_ALIGNMENT: YES

FROZEN_INPUTS_CONSISTENT: YES
FEATURE_MODEL_READY_FOR_FREEZE_REVIEW: YES
```

---

## 2. Frozen Input Verification

Tutti gli input a monte rimangono congelati, immutati e conformi:
- **Engine Contract:** [`ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md) (`FROZEN`)
- **Ontology C2:** [`ONTOLOGY_C2.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/model/ontology/ONTOLOGY_C2.md) (`FROZEN`)
- **State Machine C2:** [`KAGGRICULTURE_STATE_MACHINE_C2.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md) (`FROZEN`)
- **Period Ledger Audit:** [`CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md) (`FROZEN`)

---

## 3. Tile Classifier Policy-Neutral Correction (Risoluzione Blocker P0)

- **Disaccoppiamento del Working Set:** `in_working_set` è stato rimosso come guardia di classificazione dell'ambiente ed è stato formalizzato come asse ortogonale di policy (`POL-WS`, classe `POLICY_CONTEXT`);
- **Classifier Environment-Derived Puro:** il classifier associa a ogni coordinata $[x, y]$ una vista basata unicamente sullo stato fisico primitivo (`OUT_OF_SCOPE`, `LOST_WEED`, `EMPTY_AVAILABLE`, `HARVEST_READY`, `GROWING`);
- **Isolamento di `policy_retirement_due`:** trattato esplicitamente come overlay di policy / derived lifecycle assessment applicabile a piante ongoing a ciclo esaurito, senza contaminare la parte engine-derived dell'ambiente.

---

## 4. Feature Contract Materialization (Risoluzione Blocker P0)

Nella Sezione 4 di `KAGGRICULTURE_FEATURE_MODEL_C2.md` è stata materializzata la **Master Canonical Feature Catalog Table**, in cui ogni singola feature canonica espone esplicitamente tutti i 17 campi dello schema normativo:
`feature_id`, `source_concept_id`, `domain`, `semantic_type`, `epistemic_class`, `evidence_status`, `observability`, `source_fields`, `formula / derivation`, `unit`, `temporal_reference`, `validity / preconditions`, `nullability_state`, `update_frequency`, `policy_dependency`, `future_leakage_risk`, `notes`.

Tutte le definizioni sono ora completamente machine-auditable e auto-consistenti.

---

## 5. Online Observability Provenance Audit

È stato condotto un audit sistematico su ogni feature classificata `ONLINE_OBSERVABLE`:
- Tutti i campi temporali (`TMP-01`..`TMP-03`) mappano su campi diretti dell'osservazione;
- I campi di stato delle tile (`CRP-01`..`CRP-03`, `CRP-05`, `CRP-11`..`CRP-13`, `FRT-01`) e le coordinate/inventari worker (`WRK-01`..`WRK-05`, `WRK-07`) mappano su campi effettivi di `farm.tiles` e `private`;
- I campi zootecnici (`LIV-01`..`LIV-02`, `LIV-05`..`LIV-07`, `LIV-09`..`LIV-11`) mappano su campi delle strutture in `farm.tiles`;
- Nessun dato `ENGINE_INTERNAL` è stato promosso indebitamente a feature online.

---

## 6. Overflow Exposure Correction (Risoluzione Rilievo P1)

- La feature `INV-08` è stata ridefinita con semantica statica e non predittiva:
  $$\text{eod\_auto\_drop\_overflow\_if\_state\_unchanged} = \max(0, \sum \text{worker\_inventory\_total} - \text{shed\_remaining\_capacity})$$
- È stato formalizzato esplicitamente nel contratto che tale grandezza rappresenta una **misura di esposizione counterfactual istantanea** e NON una previsione dell'overflow reale a fine giornata, che dipende dalle azioni intraprese fino ad EOD.

---

## 7. Market Order Context Correction (Risoluzione Rilievo P1)

- `MKT-04` (`market_orders_in_current_batch`) e `MKT-05` (`market_orders_remaining_turn`) sono state riclassificate correttamente come `ACTION_BATCH_CONTEXT` / `POLICY_CONTEXT` con `policy_dependency = SÌ (Batch)`;
- `MKT-LIMIT` (`market_order_batch_limit` $= 10$) è formalizzata come costante strutturale `ONLINE_DERIVABLE` / `ENGINE_VERIFIED`.

---

## 8. Environment Feature Vector vs Policy Context Separation (Risoluzione Rilievo P1)

Nel testo normativo e nel Diagramma Mermaid (Sezione 18) l'architettura è stata ristrutturata per mostrare due ingressi rigorosamente separati verso il controller:
1. **Ramo Environment Feature Vector:** $\text{Observation} \to \text{Raw Observables} \to \text{Deterministic Derivations} \to \text{Environment Feature Vector}$;
2. **Ramo Policy & Planning Context:** $\text{Working Set Map} (\text{POL-WS}), \text{Reservations} (\text{POL-RES}), \text{Capacity Cap} (\text{POL-CAP}), \text{Retirement Due Overlay}, \text{Batch Context} \to \text{Controller}$;
3. **Ramo Offline Review (Post-Hoc):** $\text{Replay Trace} \to \text{Post-Hoc Metrics} \to \text{Offline Review Dashboard}$.

Nessun arco attraversa il confine tra Policy Context e Deterministic Environment Derivations.

---

## 9. Performance Decomposition Telemetry Expansion (Risoluzione Rilievo P1)

La Sezione 16 del Feature Model è stata estesa con 20 metriche post-hoc esaustive (`POST-01` .. `POST-20`) articolate su:
- **Ricavi e Costi Diretti per Specie:** ricavi colturali e animali, spese sementi, animali, strutture, assunzioni, sblocco terreni, fertilizzante;
- **Bilancio Fisico e Perdite:** unità prodotte, raccolte, vendute, perse per disidratazione (`POST-14`), overflow shed (`POST-13`), fughe animali (`POST-15`);
- **Assorbimento Risorse e Routing:** giorni occupazione suolo, breakdown azioni lavoratore, frazione di transito minimo teorico (`POST-18`), efficienza di routing (`POST-19`), onset di blocco economico del capitale (`POST-20`);
- **Confine Causale Esplicito:** chiarito che tali metriche costituiscono consuntivi contabili/fisici e che il contributo marginale richiede disegni causali dedicati (ablation/paired comparison).

---

## 10. Episode / Run Provenance Verification

I metadati di provenance dell'episodio (`episode_id`, `run_id`, `seed`, `agent_id`, `model_spec_version`, `foundation_version`, `player_position`, `opponent_id`, `environment_fingerprint`, `turnsPerDay`, `episodeSteps`) supportano la numerazione progressiva longitudinale e mantengono separati gli identificatori dalle configurazioni sperimentali.

---

## 11. Dangling Feature ID Audit

Verificato che tutti gli identificatori citati nelle matrici di mapping e nel testo corrispondano a feature canoniche formalmente definite nel Master Catalog:
- `FRM-01` .. `FRM-05`: Definiti in Sezione 4;
- `CRP-01` .. `CRP-15`: Definiti in Sezione 4;
- `CAR-01` .. `CAR-04`: Definiti in Sezione 4;
- `FRT-01` .. `FRT-05`: Definiti in Sezione 4;
- `LIV-01` .. `LIV-15`, `LIV-STRUCT`: Definiti in Sezione 4;
- `WRK-01` .. `WRK-09`: Definiti in Sezione 4;
- `INV-01` .. `INV-08`: Definiti in Sezione 4;
- `MKT-01` .. `MKT-09`, `MKT-LIMIT`: Definiti in Sezione 4;
- `ELG-01` .. `ELG-17`: Definiti in Sezione 4;
- `POL-WS`, `POL-RES`, `POL-CAP`: Definiti in Sezione 4;
- `POST-01` .. `POST-20`: Definiti in Sezione 16.

**Conteggio Dangling Feature IDs: 0 (ZERO).**

---

## 12. Mermaid Validation

Il diagramma Mermaid in Sezione 18 è stato validato con script automatico:
- Sintassi pura standard compatibile GitHub/Markdown;
- 0 tag HTML `<br/>` o caratteri non ammessi negli edge labels;
- 0 fan-in con `&`;
- Conformità architetturale con separazione netta tra Online Environment, Policy Context e Offline Telemetry.

---

## 13. Files Modified

- **`docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`** (Targeted correction pass completato con successo);
- **`results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FEATURE_MODEL_TARGETED_CORRECTION_REPORT.md`** (Creato).

---

## 14. Residual Issues

```text
RESIDUAL_BLOCKERS: 0 (NONE)
OPEN_AMBIGUITIES: 0 (NONE)
POLICY_CONTAMINATION_IN_ENGINE_STATE: 0 (NONE)
FUTURE_LEAKAGE_VULNERABILITIES: 0 (NONE)
```

---

## 15. Final Gate

```text
================================================================================
TILE_CLASSIFIER_POLICY_NEUTRAL: YES
WORKING_SET_ORTHOGONAL_TO_ENVIRONMENT_VIEW: YES
RETIREMENT_DUE_POLICY_DEPENDENCY_EXPLICIT: YES

FEATURE_CONTRACT_MATERIALIZED: YES
ALL_CANONICAL_FEATURES_HAVE_COMPLETE_SCHEMA: YES
DANGLING_FEATURE_REFERENCES_ZERO: YES

ONLINE_OBSERVABILITY_PROVENANCE_AUDITED: YES
MARKET_ORDER_CONTEXT_CLASSIFIED_CORRECTLY: YES
NO_ENGINE_INTERNAL_PROMOTED_TO_ONLINE_WITHOUT_EVIDENCE: YES

OVERFLOW_EXPOSURE_NON_PREDICTIVE: YES
NO_FUTURE_LEAKAGE: YES

ENVIRONMENT_FEATURE_VECTOR_POLICY_NEUTRAL: YES
POLICY_CONTEXT_SEPARATE_CONTROLLER_INPUT: YES
POST_HOC_SEPARATE_FROM_ONLINE: YES

PERFORMANCE_DECOMPOSITION_COMPLETE: YES
CROP_SPECIES_ECONOMIC_TELEMETRY_PRESENT: YES
LIVESTOCK_SPECIES_ECONOMIC_TELEMETRY_PRESENT: YES
RESOURCE_ABSORPTION_TELEMETRY_PRESENT: YES
CAUSAL_ATTRIBUTION_LIMITS_EXPLICIT: YES

EPISODE_PROVENANCE_DEFINED: YES
PROGRESSIVE_RUN_EPISODE_ID_SUPPORTED: YES

MERMAID_FEATURE_MODEL_PRESENT: YES
MERMAID_FEATURE_MODEL_RENDERABLE: YES
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
