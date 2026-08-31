# PROJECT_STATE — Kaggriculture

## Stato corrente

```text
PROJECT: Kaggriculture
PHASE: C2 — CODEX V7 ROUTINE BUILD EVALUATION / FORENSIC HANDOFF
STATUS_DATE: 2026-08-31

ENGINE_CONTRACT_FREEZE: YES
ONTOLOGY_FREEZE: YES
STATE_MACHINE_FREEZE: YES
FEATURE_MODEL_FREEZE: YES
DECISION_LIFECYCLE_FREEZE: YES
FOUNDATION_LAYERS_1_5_FROZEN: YES

CODEX_V7_TECHNICAL_BUILD: PASS
CODEX_V7_ECONOMIC_GATE: FAILURE (39,265.67)
CODEX_V7_BUILD_VERDICT: BUILD_NOT_READY

FORENSIC_ANALYSIS_AUTHORIZED: YES (READ-ONLY)
IMPLEMENTATION_AUTHORIZED: NO
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

Tutti i 5 layer della Model Foundation rimangono rigorosamente congelati (`FOUNDATION_LAYERS_1_5_FROZEN: YES`).

La sequenza di governance completata e lo stato attuale sono:

```text
ENGINE CONTRACT / PERIOD LEDGER AUDIT (FROZEN)
-> ONTOLOGY REVISION (FROZEN)
-> ENVIRONMENT STATE MACHINE REVISION (FROZEN)
-> FEATURE MODEL REVISION (FROZEN)
-> TRI-AGENT FOUNDATION CROSS-REVIEW & RECONCILIATION (FROZEN, CORR-01..14)
-> DECISION LIFECYCLE CONTRACT (DRAFT 01 -> INDEPENDENT REVIEWS -> RECONCILIATION -> DRAFT 02 -> TARGETED FREEZE PASS)
-> FOUNDATION CHECKPOINT (COMPLETE)
-> CODEX V7 ROUTINE BUILD (TECHNICAL PASS / BUILD_NOT_READY — MEAN 39,265.67)
-> AG-VS-CODEX V7 SERVICEABILITY/ROUTING FORENSIC (READ-ONLY NEXT STEP)
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

## 3. Decision Lifecycle Contract C2 e Policy Architetturale

Il DLC (Layer 5) è formalmente congelato:
- Applicate al 100% le 11 correzioni canoniche (`DLC-CORR-01` .. `DLC-CORR-11`);
- Risolte le dipendenze circolari di supersession tramite `supersession_intent_id` differito;
- Stabilita la gerarchia deterministica di precedenza delle guardie in `VERIFY` (con fallback `INVALIDATED`);
- Separati formalmente `INFEASIBLE`, `REJECTED` e `CANCELLED`;
- Assoluta neutralità strategica: zero prescrizioni su mix colturali, livestock, workforce o routing.

> [!NOTE]
> **Decisione Architetturale Differita**: L'eventuale semplificazione o snellimento del Decision Lifecycle Contract (DLC) e della relativa operational policy resta una decisione architetturale esplicitamente differita a valle dell'evidenza empirico-sperimentale derivante dall'analisi forense. Nessuna modifica alla Foundation viene autorizzata in questa fase.

## 4. Performance Target Round C2 e Risultati Build Codex V7

### Target di Progetto
```text
FAILURE_GATE: Mean Final Money < 50,000
MATERIAL_IMPROVEMENT: 50,000 <= Mean Final Money < 80,000
TARGET: Mean Final Money >= 80,000
```

### Sintesi Build Candidate Codex V7 (`CODEX-C2-COMPACT-Q0-ROUTINE-V7`)
- **Verdetto Tecnico**: `PASS` (6/6 episodi completati `DONE`, zero errori, zero fallback).
- **Verdetto Economico**: `FAILURE` (`BUILD_NOT_READY`).
- **Mean Final Money**: `39.265,67` (Median: `38.943,00`, Std: `1.312,86`, Range: `37.520 – 41.156`).
- **Crop Serviceability**: Fortemente migliorata (`MELON 95,00`, `STRAWBERRY 40,17`, Crop Revenue `$29.786,67`, pari al 73,64% della revenue produttiva).
- **Livestock Serviceability (Primary Bottleneck)**: `MILK 28,17`, `WOOL 14,67`, Livestock Revenue `$10.664,83`, `24 escape` (4 per episodio), `100,33` WHEAT consumato con scarsa conversione in output.
- **Routing & Efficienza Lavorativa**: Ancora inefficiente (`MOVE/productive 3,1923`, Productive Utilization `67,43%`, On-Time Crop Service `79,49%`, `50 hard misses`).
- **Benchmark Comparativo**: `+29.414,67` vs Codex V6 (`9.851`), `+1.267,997` (+3,34%) vs AG Q0 3+3 (`37.997,67`), `-17.506,333` (-30,84%) vs LuCcc (`56.772`).

## 5. Prossime Azioni e Vincoli Operativi

```text
AUTORIZZATO:
1. Analisi forense read-only AG-vs-Codex V7 su serviceability e routing (ispezione replay ed evidenze quantitative);
2. Preservazione integrale della Model Foundation (Layer 1–5 frozen).

NON AUTORIZZATO:
- Nessuna nuova implementazione o modifica di codice strategico/runtime;
- Nessuna esecuzione di tornei competitivi C2;
- Nessuna submission esterna su piattaforma Kaggle.
```

---

```text
FOUNDATION_LAYERS_1_5_FROZEN: YES
FOUNDATION_CHECKPOINT: COMPLETE
GOVERNANCE_ALIGNED: YES

CODEX_V7_STATUS: TECHNICAL PASS / BUILD_NOT_READY (MEAN 39,265.67)
NEXT_PHASE: READ_ONLY_AG_VS_CODEX_V7_SERVICEABILITY_ROUTING_FORENSIC
```
