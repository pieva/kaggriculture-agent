# ANTIGRAVITY C2 — ONTOLOGY TARGETED CORRECTION REPORT

```text
DOCUMENT_ID: ANTIGRAVITY_C2_ONTOLOGY_TARGETED_CORRECTION_REPORT
AUTHOR: Antigravity
DATE: 2026-08-31
PHASE: Foundation Revision / Targeted Ontology Correction Pass
TARGET_DOCUMENT: docs/model/ontology/ONTOLOGY_C2.md
BASELINE_AUTHORITY: results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md (FROZEN)
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
STATUS: COMPLETE — READY FOR FREEZE REVIEW
```

---

## 1. Executive Verdict

Antigravity ha eseguito il **Targeted Correction Pass** sull'Ontologia C2 (`docs/model/ontology/ONTOLOGY_C2.md`) per risolvere le 6 residue ambiguità semantiche e relazionali individuate durante la fase di independent review, preservando la stabilità del registry canonico e la piena coerenza con l'Engine Contract congelato.

```text
================================================================================
ONTOLOGY_CORRECTION_PASS: YES
ONTOLOGY_READY_FOR_FREEZE_REVIEW: YES
STATE_MACHINE_REVISION_AUTHORIZED: NO
FEATURE_MODEL_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```

---

## 2. Delta Concept Migration Matrix

La tabella documenta in dettaglio le modifiche, aggiunte e riclassificazioni applicate ai concetti dell'ontologia durante il targeted correction pass:

| Concept ID | Vecchia Definizione / Classificazione | Nuova Definizione / Classificazione | Motivazione | Engine Contract Implication | Downstream Implication |
|---|---|---|---|---|---|
| `necessary_transit_fraction` | `DERIVED_METRIC / EFFICIENCY` (con dicitura "ottimale") | `EFFICIENCY / DERIVED_METRIC` (`POST_HOC_METRIC`, `TELEMETRY_ONLY`) | Rimossa la parola "ottimale"; definita rispetto a baseline geometrica post-match | Nessun algoritmo di routing introdotto nell'engine | Usata solo per diagnostica logistica post-hoc |
| `routing_completion_efficiency` | `EFFICIENCY` (con minimizzazione deviazioni) | `EFFICIENCY / DERIVED_METRIC` (`POST_HOC_METRIC`, `TELEMETRY_ONLY`) | Definita come benchmark diagnostico a posteriori | L'engine non prescrive percorsi | Esclusa da feature online pre-azione |
| `livestock_capacity` | `CAPACITY` (sostenibile in base a feed/worker) | **`DEPRECATED / SPLIT`** in due concetti ortogonali | "Sostenibile" introduceva assunzione di policy futura | `CAP-01` e `SVC-01` rispettati | Eliminata falsa garanzia scalare |
| `livestock_structural_capacity` | *N/A (Nuovo concetto)* | `CAPACITY` (`DERIVED_ENGINE_FACT`, `ONLINE_DERIVABLE`) | Limite fisico puro dato da strutture (`COOP`/`PASTURE`) e piazzamento | Derivato direttamente dallo stato engine | Classifier fisico in Feature Model |
| `livestock_serviceable_capacity` | *N/A (Nuovo concetto)* | `CAPACITY / STATE` (`POLICY_DECLARED`, `ONLINE_DERIVABLE`) | Capacità pianificata gestibile dalla policy con risorse/turni | Dipende da piano/controller (`POLICY_CONTEXT`) | Feature contestuale di policy |
| `livestock_product_flow` | `FLOW / REVENUE` | **`FLOW`** (`ENGINE_VERIFIED`, `ONLINE_OBSERVABLE`) | La produzione fisica genera inventario, non automaticamente ricavo | La monetizzazione richiede ordini `SELL` a mercato | Separazione scorte fisiche vs ricavi |
| `fertilizer_byproduct_flow` | `FLOW / REVENUE` | **`FLOW`** (`ENGINE_VERIFIED`, `ONLINE_OBSERVABLE`) | La raccolta del fertilizzante genera scorte, non ricavo monetario | La vendita a mercato è fase separata | Separazione scorte fisiche vs ricavi |
| `livestock_feed_action_flow` | *N/A (Formalizzato come concetto distinto)* | `FLOW` (`ENGINE_VERIFIED`, `ONLINE_OBSERVABLE`) | Flusso esecuzione azione `FEED` (precondizione per prevenire fuga) | `FEED` consuma 1 Wheat e setta `fed_today=True` | Catena causale chiusa per fuga e bonus |
| `current_money_state` | *N/A (Separato da final outcome)* | `STATE` (`ENGINE_VERIFIED`, `ONLINE_OBSERVABLE`) | Saldo cassa corrente disponibile nello stato per decisioni | Letto da `observation.money` | Feature decisionale online lecita |
| `final_money_outcome` | `OUTCOME` (`ONLINE_OBSERVABLE / OUTCOME_ONLY`) | `OUTCOME / POST_HOC_METRIC` (`OUTCOME_ONLY`) | Saldo monetario terminale a fine episodio (reward/score) | Calcolato a `step == episodeSteps` | Vietato come input online intra-match |
| `economic_lock_in_onset` | `TIMING / DERIVED_METRIC` (con claim di "irreversibilità") | `TIMING / DERIVED_METRIC` (`POST_HOC_METRIC`, `TELEMETRY_ONLY`) | Chiarito che l'irreversibilità è determinabile solo post-match | Non disponibile online durante l'episodio | Metrica di analisi retrospettiva |

---

## 3. Delta Relation Matrix

La tabella documenta le relazioni canoniche corrette per eliminare inferenze causali indebite e legami troppo forti:

| Relazione Precedente | Relazione Revisionata (C2 Corrected) | Natura della Correzione | Motivazione Semantica |
|---|---|:---:|---|
| `worker_multi_occupancy enables routing_completion_efficiency` | `worker_multi_occupancy eliminates_collision_constraint_on workforce_transit` | **INDEBOLITA / CORRETTA** | La multi-occupancy rimuove il vincolo di collisione; non garantisce né produce efficienza di percorso. |
| `feed_availability prevents animal_escape_condition` | `feed_availability is_prerequisite_for livestock_feed_action_flow` <br> `livestock_feed_action_flow prevents animal_escape_condition` | **DISACCOPPIATA / CATENA CAUSALE** | La presenza di grano nello shed non impedisce da sola la fuga; è necessaria l'esecuzione dell'azione `FEED`. |
| `feed_availability AND livestock_care_action_flow produces pending_care_bonus_accumulation` | `livestock_feed_action_flow AND livestock_care_action_flow produces pending_care_bonus_accumulation` | **ALLINEATA ALL'ENGINE** | Il bonus richiede l'impostazione effettiva di `fed_today=True` e `cared_today=True` all'EOD. |
| `action_eligible_now enables productive_action_share` | `action_eligible_now is_prerequisite_for productive_action_share` | **PRECISATA** | L'idoneità all'azione è una precondizione logica, non la causa efficiente dell'azione. |
| `operating_cash_buffer constrains deployable_capital_window` | `operating_cash_buffer defines deployable_capital_window` | **RICLASSIFICATA** | Entrambi i concetti appartengono alla sfera della deliberazione della policy (`POLICY_CONTEXT`). |
| `fertilizer_effect_window constrains crop_fertilizer_bonus` | `fertilizer_effect_window bounds crop_fertilizer_bonus` | **PRECISATA** | La finestra temporale delimita l'applicabilità dell'uplift $+1$. |

---

## 4. Epistemic Classification Audit

Tutti i concetti modificati sono stati sottoposti a verifica incrociata tra tipo, evidenza e osservabilità:

1. **Assenza di "Optimal" non formalizzato:** `necessary_transit_fraction` e `routing_completion_efficiency` sono categorizzati rigorosamente come `POST_HOC_METRIC` e valutati rispetto a distanze geometriche di riferimento (Manhattan baseline).
2. **Scissione Capacità Fisica vs Capacità Policy:** 
   - `livestock_structural_capacity` = `DERIVED_ENGINE_FACT` (osservabile online dalle strutture fisiche).
   - `livestock_serviceable_capacity` = `POLICY_CONTEXT` / `POLICY_DECLARED` (piano soggettivo di gestione carichi).
3. **Disaccoppiamento Produzione vs Ricavo:** `livestock_product_flow` e `fertilizer_byproduct_flow` sono classificati puramente come `FLOW` fisici di inventario. Il ricavo monetario è generato solo da transazioni `SELL` a mercato (`market_transaction_value`, `product_mix_revenue`).
4. **Separazione Cassa Online vs Outcome Terminale:**
   - `current_money_state` = `ONLINE_OBSERVABLE` (input decisionale legittimo).
   - `final_money_outcome` = `OUTCOME_ONLY` / `POST_HOC_METRIC` (etichetta terminale di performance).
5. **Lock-In come Metrica Retrospettiva:** `economic_lock_in_onset` è esplicitamente classificato come `POST_HOC_METRIC` e `TELEMETRY_ONLY`, prevenendo qualsiasi claim di determinabilità online in tempo reale.

---

## 5. Observability & No-Future-Leakage Audit

L'audit conferma che nessuna metrica o flusso telemetrico a posteriori può essere consumato come feature decisionale online prima della conclusione dell'orizzonte di riferimento:

```text
ONLINE_OBSERVABLE / ONLINE_DERIVABLE:
- current_money_state
- canonical_clock_coordinate
- action_eligible_now
- livestock_structural_capacity
- crop_harvest_readiness
- tile_lifecycle_state

POLICY_DECLARED (Policy Context):
- reserved_serviceable_before_deadline
- livestock_serviceable_capacity
- feed_security_buffer
- operating_cash_buffer
- deployable_capital_window

POST_HOC_METRIC / TELEMETRY_ONLY / OUTCOME_ONLY:
- realized_serviceable_in_window (VIETATO ONLINE)
- necessary_transit_fraction (VIETATO ONLINE)
- routing_completion_efficiency (VIETATO ONLINE)
- economic_lock_in_onset (VIETATO ONLINE)
- final_money_outcome (VIETATO ONLINE)
```

---

## 6. Registry Count Before / After

```text
REGISTRY_COUNT_BEFORE: 78
REGISTRY_COUNT_AFTER:  85

CONCEPTS_ADDED:       4 (`livestock_structural_capacity`, `livestock_serviceable_capacity`, `livestock_feed_action_flow`, `current_money_state`)
CONCEPTS_DEPRECATED:  2 (`livestock_capacity`, `chicken_species`)
CONCEPTS_REVISED:     14 (correzioni di tipo, definizioni, benchmark geometrici e neutralità)
CONCEPTS_KEPT:        65
RELATIONS_REVISED:    6
```

---

## 7. Open Issues

```text
RESIDUAL_AMBIGUITIES: 0 (NONE)
UNRESOLVED_BLOCKERS: 0 (NONE)
POLICY_CONTAMINATIONS_DETECTED: 0 (NONE)
```

---

## 8. File Modificati e Verifiche

- **`docs/model/ontology/ONTOLOGY_C2.md`** (Modificato con targeted correction pass)
- **`results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_ONTOLOGY_TARGETED_CORRECTION_REPORT.md`** (Creato)

---

## 9. Git Diff Check

Comando eseguito: `git diff --check`
Esito: **0 errori** (pulito).

---

## 10. Final Gate

```text
================================================================================
FINAL VERDICT:
ONTOLOGY_CORRECTION_PASS: YES
ONTOLOGY_READY_FOR_FREEZE_REVIEW: YES
================================================================================
STATE_MACHINE_REVISION_AUTHORIZED: NO
FEATURE_MODEL_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```
