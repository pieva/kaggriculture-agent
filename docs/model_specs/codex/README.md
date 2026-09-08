# Indice MODEL_SPEC Codex

## Checkpoint operativo 2026-09-08: V48 e PASS

**Priorità assoluta della prossima versione: ridurre i PASS evitabili attraverso la pianificazione biologica e della manodopera, solo 770.** V48 pubblicata (56101593) resta congelata; nessuna nuova variante o pubblicazione in questo checkpoint.

[Stato, piano, inventario completo dei sorgenti e riproduzione](../../foundation/V48_PLANNING_AND_BUILD_IT.md). I checkpoint precedenti sono storici; i nuovi Top sono ormai esposti e non costituiscono holdout.


Riferimento esterno: alias documentale **Top770**. Episode ID e hash restano
le fonti di provenienza; i nomi tecnici congelati in config, piani e schemi
dei test restano invariati per compatibilità.

Priorità corrente: [E18.33 — policy comuni di pascoli e colture](e18/MODEL_SPEC_CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.md).
[Audit dei residui e Q0](e18/reports/E18_33_LEGACY_POLICY_AUDIT_20260906_IT.md).
Kernel e adattatore nativo implementati: stessa policy per Q0/Q1/Q2, nessun
caricamento dei piani storici. **Prototipo non eleggibile**: 97 test mirati
E18.32/E18.33 passati; l'estensione dell'avvio V9 si rilascia D16–D17 ma fallisce
in tutti i quattro casi la 770. Non è autonomia dimostrata.
[Chiusura e prova di autonomia](e18/reports/E18_CLOSEOUT_AND_BOOTSTRAP_20260906_IT.md).
[Checkpoint completo](e18/reports/E18_33_NATIVE_POLICY_CHECKPOINT_20260906_IT.md).
[E19: roadmap parametrica 770/772/662](e19/MODEL_SPEC_CODEX_E19_PARAMETRIC_VALIDATION_DRAFT.md),
subordinata al consolidamento E18, nessun esperimento avviato.
E18.32 V9 è pubblicata come **controllo provvisorio, non benchmark E19**:
56056189, Complete, 2026-09-06 13:27:24 UTC. Conserva il calendario storico;
Q0 ha ancora dodici tile libere D11–D13. E18.31 resta controllo immutabile.
E18.30 V2 resta la baseline verificata; E18.31 è pubblicata per diagnosi esterna
(56050866, Complete), non promossa. E18.28 C è il parent pubblico immutabile
(56036993), E18.29 B3 resta development non
promossa. [Diagnosi esterna su 30 replay](e18/reports/E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md).

[Report D1-D30 completo e audit COOP](e18/reports/E18_27_TOP770_D01_D30_COMPLETE_KPI_IT.md),
salvato come esempio storico. Il [formato standard corrente V4](../../../experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V4_IT.md)
prevede Top770 vs una sola candidata, 22 pannelli con WATER/FEED/CARE separati e senza
Cause PASS, oltre ai KPI economico-operativi complementari.

[Diagnosi pubblica E18.31 e Top770-002](e18/reports/E18_31_PUBLIC_TOP002_DIAGNOSTIC_20260906_IT.md):
sei replay nostri (5 WIN / 1 LOSS), quattro 770 del nuovo riferimento su cinque
esaminati; ledger riconciliati. Registro comune aggiornato, entrambi i Top770
consumati per release future. Corpus, report e riferimenti di recupero sotto E18.

| Stato | File | Uso |
|---|---|---|
| FOUNDATION | `MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md` | baseline C2.1 riconciliata |
| AS-BUILT | `e17/CODEX_V9_E17_RUNTIME_AND_FOUNDATION_MAPPING_IT.md` | mapping tra runtime V9/E17 e Foundation |
| FROZEN | `e17/MODEL_SPEC_CODEX_E17_1_3Q_REACTIVE_GUARDED.md` | linea reattiva E17 |
| EXTERNAL CONTROL | `e18/MODEL_SPEC_CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.md` | candidata E18.2 promossa a controllo esterno |
| REJECTED | `e18/MODEL_SPEC_CODEX_E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.md` | ablation topologica senza candidata |
| REJECTED | `e18/MODEL_SPEC_CODEX_E18_4_STATE_DRIVEN_772_V1.md` | primo dispatcher state-driven 7-7-2 |
| REJECTED AT GATE A | `e18/MODEL_SPEC_CODEX_E18_4_STATE_DRIVEN_772_V2.md` | locality/task-aging: integrità pass, efficienza fail |
| REJECTED AT EFFICIENCY GATE | `e18/MODEL_SPEC_CODEX_E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.md` | 6-6-2: segnale move favorevole ma sotto soglia 5% |
| RESEARCH CONTROL | `e18/MODEL_SPEC_CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD_V2.md` | miglior controllo locale exact 7-7-0 |
| EXTERNAL VALIDATION | `e18/MODEL_SPEC_CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1.md` | cap risorse COW/SHEEP 14 e FEED critico D20; Gate A pass, Gate B fail |
| ORACLE PLAN | `e18/MODEL_SPEC_CODEX_E18_18_770_CAPACITY_TRAJECTORY_PLANNER_V1.md` | piano nativo 7-7-0: Gate 0 pass, smoke live fail |
| DEVELOPMENT — INCUMBENT GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_19_770_RETRYING_TRAJECTORY_V1.md` | retry state-aware: delta E18.18 pass, smoke E18.16 fail |
| DEVELOPMENT — INCUMBENT GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_20_770_WHEAT_MARKET_NETTING_V1.md` | netting Wheat D11+: parent delta pass, effetto economico insufficiente |
| DEVELOPMENT — INCUMBENT GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_21_770_WHEAT_OBLIGATION_LEDGER_V1.md` | guard per-worker sui pickup Wheat in-flight; parent delta pass, effetto marginale |
| DEVELOPMENT — INCUMBENT GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_22_770_WHEAT_JIT_D1_V1.md` | procurement Wheat D+1: parent delta +2,84%, churn quasi allineato a E18.16 |
| REJECTED PRE-GATE | `e18/MODEL_SPEC_CODEX_E18_23_770_SW_UNLOCK_LIQUIDITY_V1.md` | anticipo JIT a D10: nessun risparmio né anticipo SW, delta parent nullo |
| REJECTED PRE-GATE | `e18/MODEL_SPEC_CODEX_E18_24_770_DEFERRED_PLANT_ON_WATER_V1.md` | recupero PLANT sulla visita WATER: target già occupati, nessun delta contro E18.16 |
| DEVELOPMENT — INCUMBENT GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_25_770_D10_LABOR_STEP_V1.md` | 12 unità reali a D10; delta matched +184/+184, capacità produttiva ancora inutilizzata |
| DEVELOPMENT — STRUCTURAL / INCUMBENT GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_26_770_TOP770_BOOST_D10_V1.md` | BoostD10, delta matched parent +2.139; prossima priorità D10-D15, poi chiusura D30 separata |
| DEVELOPMENT — ROBUSTNESS / INCUMBENT GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_27_770_D10_D15_CASHFLOW_V3.md` | Melon D11, Q2 D12, zero fughe; +13,44% matched su sette seed contro E18.16, 10/14 positivi; non promossa |
| PUBLISHED — EXTERNAL VALIDATION | `e18/MODEL_SPEC_CODEX_E18_28_770_FULL_SEASON_V1.md` | C pubblicata; 30 replay esterni, 17 sconfitte, 13 vittorie; non incumbent |
| DEVELOPMENT — SAFETY GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_29_770_ANTI_PASS_V3.md` | B3 +7,68% matched, PASS -26,78%; morte crop ereditata, non promossa |
| VERIFIED DEVELOPMENT BASELINE | `e18/MODEL_SPEC_CODEX_E18_30_770_MISSION_DISPATCHER_V1.md` | CROP_POOL: +10,05% matched, 14/14 safety, 371 test; standalone verificato, NON pubblicato |
| PUBLISHED DIAGNOSTIC — ECONOMY NOT YET PASSED | `e18/MODEL_SPEC_CODEX_E18_31_770_PRODUCTIVE_EXPANSION_V1.md` | UNIFIED V11 / 56050866: 28/28 safety interno, sei primi replay pubblici senza perdite; non promossa |
| FROZEN INTERNAL CONTROL | `e18/MODEL_SPEC_CODEX_E18_32_770_READY_WORK_V1.md` | DEMAND RELEASE V9 verificata; calendario legacy, non conforme alla policy comune; non pubblicata |
| CURRENT DEVELOPMENT — GATE FAIL | `e18/MODEL_SPEC_CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.md` | Kernel e prototipo nativo, 67 test; V5 non raggiunge 770, economia -12,95% su quattro casi matched; non eleggibile |
| ROADMAP — NOT STARTED | `e19/MODEL_SPEC_CODEX_E19_PARAMETRIC_VALIDATION_DRAFT.md` | Confronto 770/772/662 con stessa policy soltanto dopo consolidamento E18 |

Handoff corrente: `docs/NEW_SESSION.md`.
Il seguente handoff E18.27 è storico (2026-09-05):
`e18/reports/E18_27_D10_D15_CONSOLIDATED_V3_REPORT_IT.md`.
Specifica e stato operativo E18.27 V3 documentano quella iterazione, non la priorità attuale.
Diagnosi di origine:
`e18/reports/E18_26_D10_D15_CASH_FEED_DIAGNOSIS_AND_NEXT_PRIORITIES_IT.md`.
Consolida gradino Melon D11, fughe al cambio D14 e mancata risposta ai
pascoli vuoti, con gate della prossima versione e seconda fase di chiusura.

Le specifiche e gli asset riproducibili di Codex sono raggruppati per round in
`e17/`, `e18/` ed `e19/`: model spec, config, design, prompt, report, review, tool, test
e artifact.
I manifest, i tornei e i confronti condivisi restano sotto `experiments/`.
