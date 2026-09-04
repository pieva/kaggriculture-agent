# Indice MODEL_SPEC Codex

| Stato | File | Uso |
|---|---|---|
| FOUNDATION | `MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md` | baseline C2.1 riconciliata |
| AS-BUILT | `CODEX_V9_E17_RUNTIME_AND_FOUNDATION_MAPPING_IT.md` | mapping tra runtime V9/E17 e Foundation |
| FROZEN | `MODEL_SPEC_CODEX_E17_1_3Q_REACTIVE_GUARDED.md` | linea reattiva E17 |
| EXTERNAL CONTROL | `MODEL_SPEC_CODEX_E18_2_CAPACITY_GOVERNED_V4D_V1.md` | candidata E18.2 promossa a controllo esterno |
| REJECTED | `MODEL_SPEC_CODEX_E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.md` | ablation topologica senza candidata |
| REJECTED | `MODEL_SPEC_CODEX_E18_4_STATE_DRIVEN_772_V1.md` | primo dispatcher state-driven 7-7-2 |
| REJECTED AT GATE A | `MODEL_SPEC_CODEX_E18_4_STATE_DRIVEN_772_V2.md` | locality/task-aging: integrità pass, efficienza fail |
| REJECTED AT EFFICIENCY GATE | `MODEL_SPEC_CODEX_E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.md` | 6-6-2: segnale move favorevole ma sotto soglia 5% |
| RESEARCH CONTROL | `MODEL_SPEC_CODEX_E18_10_770_WATER_BEFORE_DIG_GUARD_V2.md` | miglior controllo locale exact 7-7-0 |
| EXTERNAL VALIDATION | `MODEL_SPEC_CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1.md` | cap risorse COW/SHEEP 14 e FEED critico D20; Gate A pass, Gate B fail |

Gli asset riproducibili specifici di Codex sono raggruppati per round in
`e17/` ed `e18/`: config, design, prompt, report, review, tool, test e artifact.
I manifest, i tornei e i confronti condivisi restano sotto `experiments/`.
