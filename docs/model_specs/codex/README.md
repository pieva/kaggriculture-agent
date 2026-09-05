# Indice MODEL_SPEC Codex

Riferimento esterno: alias documentale **Top770**. Episode ID e hash restano
le fonti di provenienza; i nomi tecnici congelati in config, piani e schemi
dei test restano invariati per compatibilità.

Priorità corrente: [E18.30 — motore di assegnazione](e18/MODEL_SPEC_CODEX_E18_30_770_MISSION_DISPATCHER_V1.md).
E18.28 C è l'ultima pubblicata (56036993), E18.29 B3 resta development non
promossa. [Diagnosi esterna su 30 replay](e18/reports/E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md).

[Report D1-D30 completo e audit COOP](e18/reports/E18_27_TOP770_D01_D30_COMPLETE_KPI_IT.md),
salvato come esempio storico. Il [formato standard corrente V3](../../../experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V3_IT.md)
prevede Top770 vs una sola candidata, 21 pannelli con WATER/FEED e senza
Cause PASS, oltre ai KPI economico-operativi complementari.

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
| ACTIVE DEVELOPMENT | `e18/MODEL_SPEC_CODEX_E18_30_770_MISSION_DISPATCHER_V1.md` | riprogettazione assegnazione, manodopera reale e missioni confermate |

Handoff corrente: `docs/NEW_SESSION.md`.
Il seguente handoff E18.27 è storico (2026-09-05):
`e18/reports/E18_27_D10_D15_CONSOLIDATED_V3_REPORT_IT.md`.
Specifica e stato operativo E18.27 V3 documentano quella iterazione, non la priorità attuale.
Diagnosi di origine:
`e18/reports/E18_26_D10_D15_CASH_FEED_DIAGNOSIS_AND_NEXT_PRIORITIES_IT.md`.
Consolida gradino Melon D11, fughe al cambio D14 e mancata risposta ai
pascoli vuoti, con gate della prossima versione e seconda fase di chiusura.

Le specifiche e gli asset riproducibili di Codex sono raggruppati per round in
`e17/` ed `e18/`: model spec, config, design, prompt, report, review, tool, test
e artifact.
I manifest, i tornei e i confronti condivisi restano sotto `experiments/`.
