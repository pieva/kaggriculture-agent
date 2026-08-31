# PROJECT_STATE — Kaggriculture

## Stato corrente

```text
PROJECT: Kaggriculture
PHASE: C2 — MODEL_SPEC REVISION / BUILD PREPARATION
STATUS_DATE: 2026-08-31

ENGINE_CONTRACT_FREEZE: YES
ONTOLOGY_FREEZE: YES
STATE_MACHINE_FREEZE: YES
FEATURE_MODEL_FREEZE: YES
DECISION_LIFECYCLE_FREEZE: YES
FOUNDATION_LAYERS_1_5_FROZEN: YES

FOUNDATION_CHECKPOINT: COMPLETE
MODEL_SPEC_REVISION_AUTHORIZED: YES
BUILD_AUTHORIZED: YES
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Contesto

Il ciclo C2 della Model Foundation ha completato la revisione rigorosa e il consolidamento formale di tutti i cinque layer condivisi:

1. **Engine / Domain Contract** — fatti normativi dell'ambiente (FROZEN in `ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md`);
2. **Ontology C2** — concetti di dominio, 85 concept_id (FROZEN in `ONTOLOGY_C2.md`);
3. **Environment State Machine C2** — 11 fasi engine, transizioni ed EOD (FROZEN in `KAGGRICULTURE_STATE_MACHINE_C2.md`);
4. **Feature Model C2** — 5 viste pure + 2 overlays, flat paths, quadripartizione epistemica (FROZEN in `KAGGRICULTURE_FEATURE_MODEL_C2.md`);
5. **Decision Lifecycle Contract C2** — protocollo deliberativo comune, non-circular supersession, precedenza guardie deterministica (FROZEN in `KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md`, certificato da `DECISION_LIFECYCLE_TARGETED_FINAL_FREEZE_REVIEW.md`).

La sequenza di governance completata è:

```text
ENGINE CONTRACT / PERIOD LEDGER AUDIT (FROZEN)
-> ONTOLOGY REVISION (FROZEN)
-> ENVIRONMENT STATE MACHINE REVISION (FROZEN)
-> FEATURE MODEL REVISION (FROZEN)
-> TRI-AGENT FOUNDATION CROSS-REVIEW & RECONCILIATION (FROZEN, CORR-01..14)
-> DECISION LIFECYCLE CONTRACT (DRAFT 01 -> INDEPENDENT REVIEWS -> RECONCILIATION -> DRAFT 02 -> TARGETED FREEZE PASS)
-> FOUNDATION CHECKPOINT (COMPLETE)
-> THREE INDEPENDENT MODEL_SPEC REVISIONS + BUILD (AUTHORIZED)
```

## 2. Architettura a 5 Layer e Separazione Normativa

L'architettura comune Kaggriculture separa rigorosamente i fatti fisici dell'ambiente dal processo deliberativo degli agenti:

```text
┌────────────────────────────────────────────────────────┐
│ MODEL FOUNDATION (5 Shared Frozen Layers)              │
│ 1. Engine Contract                                     │
│ 2. Ontology C2                                         │
│ 3. Environment State Machine C2                        │
│ 4. Feature Model C2                                    │
│ 5. Decision Lifecycle Contract C2                      │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
      MODEL_SPEC      MODEL_SPEC      MODEL_SPEC
      Antigravity        Codex          Copilot
            │               │               │
            ▼               ▼               ▼
        BUILD C2        BUILD C2        BUILD C2
```

## 3. Decision Lifecycle Contract C2 — Certificazione di Freeze

Il DLC (Layer 5) è stato certificato con verdetto `PASS` tramite `DECISION_LIFECYCLE_TARGETED_FINAL_FREEZE_REVIEW.md`:
- Applicate al 100% le 11 correzioni canoniche (`DLC-CORR-01` .. `DLC-CORR-11`);
- Risolte le dipendenze circolari di supersession tramite `supersession_intent_id` differito;
- Stabilita la gerarchia deterministica di precedenza delle guardie in `VERIFY` (con fallback `INVALIDATED`);
- Separati formalmente `INFEASIBLE` (fallimento feasibility gate), `REJECTED` (pre-commit rejection) e `CANCELLED` (post-commit termination);
- Governativo il repair (con record e attempt counter) senza forzatura ad `INVALIDATED`;
- Assoluta neutralità strategica: zero prescrizioni su mix colturali, livestock, workforce o routing.

## 4. Performance Target Round C2

Target di progetto validi per tutti i candidati downstream:

```text
FAILURE_GATE: Mean Final Money < 50,000
MATERIAL_IMPROVEMENT: 50,000 <= Mean Final Money < 80,000
TARGET: Mean Final Money >= 80,000
```

Valutazione richiesta con holdout seeds pre-dichiarati, simmetria P0/P1, rotazione avversari e decomposizione empirica per fonte di profitto.

## 5. Prossime Azioni Autorizzate

Con il completamento del checkpoint della Model Foundation:

```text
AUTORIZZATO:
1. Revisione indipendente dei tre MODEL_SPEC C2 (Antigravity, Codex, Copilot);
2. BUILD e compilazione dei tre candidati tournament;
3. Esecuzione dei test unitari e di integrazione locali.

NON ANCORA AUTORIZZATO:
- Esecuzione del torneo competitivo C2;
- Submission Kaggle esterna.
```

---

```text
FOUNDATION_LAYERS_1_5_FROZEN: YES
FOUNDATION_CHECKPOINT: COMPLETE
GOVERNANCE_ALIGNED: YES

MODEL_SPEC_REVISION_AUTHORIZED: YES
BUILD_AUTHORIZED: YES
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO

NEXT_PHASE:
INDEPENDENT_AGENT_MODEL_SPEC_REVISION_AND_BUILD
```
