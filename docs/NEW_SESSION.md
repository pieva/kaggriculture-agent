# NEW_SESSION — Kaggriculture

## Handoff E18.4 (2026-09-03)

Non caricare `CODEX-E18.4-STATE-DRIVEN-772-V1`: il gate 14-match è respinto.
Conservare topologia 7-7-2, sale ledger, Wheat reserve e harvest batching; la
prossima modifica deve riguardare esclusivamente il dispatcher. Gate anticipato
V2: move action <= E18.2 e productive action >=95% E18.2 prima del money.
Artifact e diagnosi sono in
`experiments/e18/artifacts/derived/codex/E18_4_STATE_DRIVEN_772_DEV_GATE_V1.json`
e `experiments/e18/reports/codex/E18_4_STATE_DRIVEN_772_DEV_GATE_REPORT_IT.md`.

## Ripresa operativa

```text
START_HERE: docs/PROJECT_STATE.md
FOUNDATION: C2.1 RECONCILED
FOUNDATION_MANIFEST: docs/foundation/FOUNDATION_C2_1_MANIFEST.md
REPOSITORY_CLEANUP: COMPLETE
REPOSITORY_REORGANIZATION: COMPLETE / A0-A7 PASS
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
COMMON_EXECUTION_PROMPT: experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md

CURRENT_CODEX_MODEL: CODEX-E17.3-TOPOLOGY-FILL-662-V2
CURRENT_CODEX_SUBMISSION: submission/submission_codex_e17_topology_662.py
CURRENT_CODEX_SUBMISSION_SHA256: 3DF5C15D078552AF0A3849653057303698C9D750B4C7BB087B8A29092FADBAE8
E18_2_CANDIDATE_MODEL: CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1
E18_2_CANDIDATE_SUBMISSION: submission/submission_codex_e18_2_capacity_governed_v4d.py
E18_2_CANDIDATE_SHA256: C5FB1FC4966B81F238CDD0DE4CA5E15B16EA6B8AE077A08ECC881F8729FD01F7
E18_3_CODEX_ABLATION: COMPLETE_70_OF_70 / FIVE_FIXED_TOPOLOGIES
E18_3_RESULT: NO_PROMOTION / SUBMISSION_NOT_AUTHORIZED
E18_3_MONEY_VS_CONTROL: 775_-0.82% / 772_-14.31% / 662_-42.98% / 770_-34.69% / 670_-40.31%
E18_3_NEXT_ARCHITECTURE: NATIVE_STATE_DRIVEN_MISSION_SCHEDULER / START_FROM_772
E18_4_V1_GATE: REJECTED_0_OF_14 / 55940_VS_83095.71 / DELTA_-32.68_PERCENT
E18_4_V1_ARCHITECTURE: EXACT_772_AND_FILLED_16_OF_16_IN_14_OF_14 / LOSSES_0
E18_4_V1_WORK: MOVE_+29.35_PERCENT / PRODUCTIVE_-20.95_PERCENT
E18_4_V1_UPLOAD: NOT_AUTHORIZED
E18_4_V2_NEXT: CLUSTER_OWNERSHIP / TASK_AGING / CARRIER_AFFINITY
E18_DIAGNOSTIC_MODEL: CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1
E18_DIAGNOSTIC_SUBMISSION: submission/submission_codex_e18_opponent_reactive_662_770.py
E18_DIAGNOSTIC_SUBMISSION_SHA256: 06727C1673EC289A323CE403596FAB8B272539535D27C9CEE74B8C917B78791B
CURRENT_CODEX_REACTIVE_SUBMISSION: submission/submission_codex_e17_reactive.py
CURRENT_CODEX_REACTIVE_SUBMISSION_SHA256: 0874EB10F287DC7E6A268CDB64517BAE98E246EB1A124EF9C643A3B7DCE0082C
KAGGLE_SCORE_PRIOR_SNAPSHOT: 1159.9
KAGGLE_POSITION_PRIOR_SNAPSHOT: 2542
KAGGLE_E17_INTERIM_RATING: 996
KAGGLE_E17_ENTRY_RATING: 600
KAGGLE_E17_INTERIM_DELTA: +396
KAGGLE_E17_SCORE_STATUS: STABILIZING_NOT_FINAL
KAGGLE_E17_CONTROL_RATING_SNAPSHOT: 1089.7
KAGGLE_E17_REACTIVE_RATING_SNAPSHOT: 1353.6
KAGGLE_E17_REACTIVE_DELTA: +263.9 (+24.2%)
VISIBLE_TOP3_2026_09_03: Crop_Dusta=2958.7, 3정훈=2948.1, sbol_ball=2929.8

NEXT_EXPERIMENT: E18
E17_PHASE: CLOSED / DEVELOPMENT COMPLETE / HOLDOUT NOT USED
E17_CLOSEOUT: COMPLETE_2026_09_03
E17_OBJECTIVE: COMPARE_CAUSAL_LINES_WITHOUT_PRESELECTING_ONE_ARCHETYPE
E17_POLICY_MUTATION: CODEX_SERVICE_ROUTING_V3_CONTROL / CODEX_POST_FEED_CAPACITY_BATCHING_V4D_INTERNAL
E17_CROSS_AGENT_REVIEW: CLOSED
E17_STRATEGY_FREEZE: experiments/e17/design/E17_STRATEGY_FROZEN_V1.md
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_1_AUTHORIZED: YES_BY_POST_FREEZE_OWNER_DECISION
E17_REACTIVE_DESIGN: experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md
E17_REACTIVE_AUTHORIZATION: experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md
E17_REACTIVE_TOURNAMENT: HOLDOUT_BLOCKED_CLAUDE_V2_FAILED_GATES
E17_REACTIVE_PARTICIPANTS: CODEX_V9_FROZEN, CODEX_REACTIVE, CLAUDE_REACTIVE
E17_DEVELOPMENT_EXHIBITION: COMPLETE_42_OF_42_NON_QUALIFYING
E17_EXTERNAL_SUBMISSION: REACTIVE_LIVE_SCORE_STABILIZING
E17_EXTERNAL_RELEASE: CODEX-E17.0-EXTERNAL-CONTROL-V1
E17_KAGGLE_SUBMISSION_ID: 559588638
E17_REACTIVE_KAGGLE_SUBMISSION_ID: 559631298
E17_REACTIVE_EXTERNAL_BENCHMARK: COMPLETE_10_EPISODES_5W_5L
E17_REACTIVE_EXTERNAL_MEAN_MONEY: 78808.7
E17_REACTIVE_ACTION_STREAMS: 1_UNIQUE_OF_10
E17_REACTIVE_STRUCTURAL_TRAJECTORIES: 4_UNIQUE_OF_10
E17_REACTIVE_Q2_VS_Q0_ANIMAL_TILE_DAYS: 63.29%
E17_TRUE_REACTIVITY_PLAN: experiments/e17/design/E17_CODEX_TRUE_REACTIVITY_ACTIVATION_PLAN_V1.md
E17_TRUE_REACTIVITY_V2: DEVELOPMENT_GATES_PASS_NOT_KAGGLE_READY
E17_TRUE_REACTIVITY_RUNS: 48
E17_TRUE_REACTIVITY_INERT_DELTA: +1.55%
E17_TRUE_REACTIVITY_OVERALL_DELTA_VS_V1: -0.26%
E17_TRUE_REACTIVITY_Q2_OUTCOME: FINAL_ANIMALS_8_6_5_UNCHANGED
E17_TRUE_REACTIVITY_REPORT: experiments/e17/reports/codex/E17_CODEX_TRUE_REACTIVITY_DEVELOPMENT_REPORT_IT.md
E17_SERVICE_ROUTING_PLAN: experiments/e17/design/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_PLAN_V2.md
E17_SERVICE_ROUTING_V2: SUPERSEDED_INTERNAL_BY_V3_D28
E17_SERVICE_ROUTING_V3: ALL_DEVELOPMENT_GATES_PASS_NOT_KAGGLE_RELEASED
E17_SERVICE_ROUTING_ACTIVATION_DAY: 28
E17_SERVICE_ROUTING_LIQUIDATION_DAY: 29
E17_SERVICE_ROUTING_RUNS: 12
E17_SERVICE_ROUTING_MEAN: 134351.33
E17_SERVICE_ROUTING_CONTROL_MEAN: 134060.17
E17_SERVICE_ROUTING_DELTA: +0.217%
E17_SERVICE_ROUTING_DELTA_VS_V2_D29: +1.82%
E17_SERVICE_ROUTING_UNIT_LEDGER: 3198/3198_CLASSIFIED
E17_SERVICE_ROUTING_MARKET_LEDGER: 78/78_CLASSIFIED
E17_SERVICE_ROUTING_COMMANDS: ROUTING_2256 / SERVICE_752
E17_SERVICE_ROUTING_SAFETY: NON_SELL_VIOLATIONS_0 / ANIMAL_ESCAPES_0
E17_SERVICE_ROUTING_TERMINAL_SELLABLE_RESIDUAL: 0
E17_SERVICE_ROUTING_REPORT: experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_REPORT_IT.md
E17_BATCHED_ROUTING_PLAN: experiments/e17/design/E17_CODEX_BATCHED_CLUSTER_ROUTING_PLAN_V1.md
E17_BATCHED_ROUTING_V4A: REJECTED_REWARD_MINUS_2.529%
E17_CLUSTERED_ROUTING_V4B: REJECTED_NO_LOGISTIC_GAIN
E17_CAPACITY_ROUTING_V4C: REJECTED_TRIGGER_BLOCKED_BY_WHEAT_GUARD
E17_POST_FEED_CAPACITY_V4D: ALL_DEVELOPMENT_GATES_PASS_NOT_KAGGLE_RELEASED
E17_V4D_RUNS: 12
E17_V4D_MEAN: 135096.83
E17_V4D_CONTROL_MEAN: 134351.33
E17_V4D_DELTA: +0.555%
E17_V4D_MIN_MATCHED_DELTA: +497
E17_V4D_MOVE_PER_SERVICE: 2.872
E17_V4D_LEDGER: UNIT_3198/3198 / MARKET_71/71
E17_V4D_SAFETY: ERRORS_0 / ESCAPES_0 / TERMINAL_RESIDUAL_0
E17_V4D_REPORT: experiments/e17/reports/codex/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md
E17_V4D_MARKET_STRESS: PASS_48_OF_48 / D27_ADMITTED
E17_V4D_MARKET_STRESS_MATCHED: 24_OF_24_NONNEGATIVE
E17_V4D_MARKET_STRESS_MEAN: 124090.17
E17_V4D_MARKET_STRESS_CONTROL_MEAN: 123199.54
E17_V4D_MARKET_STRESS_DELTA: +0.723%
E17_V4D_MARKET_STRESS_WORST_REGIME: INERT_+0.555%
E17_V4D_MARKET_STRESS_MOVE_PER_SERVICE: 2.922_VS_2.967
E17_V4D_MARKET_STRESS_REPORT: experiments/e17/reports/codex/E17_CODEX_V4D_CONTROLLED_MARKET_STRESS_REPORT_IT.md
E17_D27_HANDOFF_ABLATION: FAIL_REWARD / V4D_D28_RETAINED
E17_D27_RUNS: 12
E17_D27_MEAN: 133290.33
E17_D27_CONTROL_MEAN: 135096.83
E17_D27_DELTA: -1.337%
E17_D27_MATCHED_NONNEGATIVE: 0/6
E17_D27_MOVE_PER_SERVICE: 2.605_VS_2.872
E17_D27_CAUSAL_DIAGNOSIS: ONE_FEWER_Q0_CROP_IN_6/6
E17_D27_REPORT: experiments/e17/reports/codex/E17_CODEX_D27_HANDOFF_ABLATION_REPORT_IT.md
E17_V4D_KAGGLE_RELEASE: READY_FOR_OWNER_UPLOAD
E17_V4D_SUBMISSION: submission/submission_codex_e17_v4d.py
E17_V4D_SUBMISSION_SHA256: 2792244CA71115E6CAAFDFC942B6D9AAAF09B95FC717A5B182D07A31D9717CD7
E17_V4D_SUBMISSION_PARITY: 4314/4314
E17_V4D_KAGGLE_UPLOAD: NOT_YET_RECORDED
E17_V4D_RELEASE_REPORT: experiments/e17/reports/codex/E17_CODEX_V4D_KAGGLE_SUBMISSION_READINESS_REPORT_IT.md
E17_662_MODEL: CODEX-E17.3-TOPOLOGY-FILL-662-V2
E17_662_SUBMISSION: submission/submission_codex_e17_topology_662.py
E17_662_SUBMISSION_SHA256: 3DF5C15D078552AF0A3849653057303698C9D750B4C7BB087B8A29092FADBAE8
E17_662_TOPOLOGY: Q0_6 / Q1_6 / Q2_2 / FILLED_14_OF_14
E17_662_KAGGLE_SUBMISSION_ID: 559767808
E17_662_KAGGLE_SCORE_SNAPSHOT: 1009.8_STABILIZING_NOT_FINAL
E17_THREE_AGENT_TOURNAMENT: COMPLETE_42_OF_42_DEVELOPMENT_NON_QUALIFYING
E17_THREE_AGENT_STANDINGS: CODEX_28_0_0 / CLAUDE_14_14_0 / COPILOT_0_28_0
E17_THREE_AGENT_MEAN_MONEY: CODEX_123620.29 / CLAUDE_15511.21 / COPILOT_10537.18
E17_THREE_AGENT_REPORT: experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md
E17_DELTA_TOURNAMENT: COMPLETE_84_OF_84_DEVELOPMENT_NON_QUALIFYING
E17_DELTA_TOURNAMENT_REPORT: experiments/e17/reports/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3_REPORT_IT.md
E17_CLAUDE_V5_DELTA: SHARED_+8.53% / DIRECT_-9.57% / NOT_PROMOTED
E17_CLAUDE_V6_REGRESSION: 1W_13L / MEAN_1538.50 / 3Q_1_OF_14 / REJECTED
E17_CLAUDE_V6_BLACKBOX: 0W_16L / MEAN_622.88 / OPPONENT_MEAN_144654.75
E17_COPILOT_662_V3_DELTA: 0.00% / IDENTICAL_28_OF_28 / NOT_PROMOTED
E17_COPILOT_662_V4: LATE_TECHNICAL_PROTOTYPE / NOT_BENCHMARKED / NOT_ADMITTED
ACTIVE_DEVELOPMENT_AGENTS: NONE_E17_CLOSED
CODEX_REACTIVE_STATUS: 662_V2_RETAINED_AS_E18_BASELINE
CODEX_REACTIVE_DEVELOPMENT_MEAN: 139420.2857
CODEX_REACTIVE_DELTA_VS_V9: 0
CLAUDE_REACTIVE_STATUS: V1_REJECTED / V2_FROZEN_WITH_FAILED_GATES
CLAUDE_ACTIVATION_AUDIT: PASS_WITH_LOCAL_CLEANUP
CLAUDE_ROOT_BOOTSTRAP: REMOVED
CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK: AUTHORIZED_DEVELOPMENT_ONLY
CLAUDE_V3_IMPLEMENTATION: COMPLETE_FROZEN_WITH_FAILED_GATES
CLAUDE_V3_10X_PROMPT: experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_V3_10X_ACTIVATION_PROMPT_IT.md
REPLAY_JSON_ROOT: data/replays/json
REPLAY_JSON_CATALOG: data/replays/json/json.md
E17_RAW_CODEX_DEV_AND_CLAUDE_V1: REMOVED_REPRODUCIBLE
CLAUDE_V2_RAW: REMOVED_REPRODUCIBLE_CATALOG_RETAINED
ANTIGRAVITY_STATUS: OWNER_UNAVAILABLE_UNTIL_2026_09_04 / EXCLUDED_FROM_E17_3_TOURNAMENT
COPILOT_STATUS: 662_V3_BEHAVIORALLY_INERT / NOT_PROMOTED
NEW_KAGGLE_SUBMISSION: E17_662_ID_559767808 / SCORE_SNAPSHOT_1009.8_STABILIZING

E18_PHASE: OPEN_E18_4_V1_REJECTED_V2_LOCALITY_GATE_PENDING
E18_ECONOMIC_CONTROL: CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28
E18_CANDIDATE: CODEX-E18.4-STATE-DRIVEN-772-V1 / REJECTED_NO_UPLOAD
E18_OPENING_REPLAY: 105080066 / ANALYZED / TRAINING_EVIDENCE
E18_OPENING_DIAGNOSIS: CROP_LIFECYCLE_SERVICE_AND_HARVEST_CADENCE_GAP
E18_LIFECYCLE_OUTPUT: CODEX_586 / YUSUF_829 / DELTA_-243
E18_LIFECYCLE_WEED_EXITS: CODEX_49 / YUSUF_9
E18_LIVE_TOP3_CORPUS: 8_REPLAYS / BOTH_SEATS_PER_AGENT / ACQUIRED_AND_ANALYZED
E18_CODEX_EXTERNAL_REACTIVITY: 1_UNIQUE_LIFECYCLE_PROFILE_OF_3
E18_TOP3_EXTERNAL_REACTIVITY: 8_UNIQUE_LIFECYCLE_PROFILES_OF_8 / 5_TOPOLOGIES
E18_TOP3_Q2_PASTURES: ZERO_IN_7_OF_8 / RANGE_INCLUDES_10-7-0_AND_8-4-3
E18_LIVE_OUTPUT_DELTA: HARVEST_+48.9_PERCENT / WHEAT_+87.5_PERCENT / UNWATERED_-22.9_PERCENT
E18_OPPONENT_SIGNAL: PUBLIC_FARM_OBSERVABLE / RATING_AND_CROSS_EPISODE_HISTORY_UNAVAILABLE
E18_PIPELINE_GAP: BRIDGED_IN_CANDIDATE_WITH_PUBLIC_OPPONENT_FARM_OBSERVER
REPLAY_STORAGE: 0_RAW_JSON / 29_FILES_765.18_MIB_REMOVED_WITH_OWNER_AUTHORIZATION
REPLAY_RECOVERY: KAGGLE_EPISODE_ENDPOINT_PLUS_JSON_MD_SHA256
E18_CANDIDATE_INTAKE: CLAUDE_E18_1_AND_COPILOT_E18_1_ADMITTED / NOT_PROMOTED
E18_CANDIDATE_INTAKE_REPORT: experiments/e18/reports/common/E18_CLAUDE_COPILOT_CANDIDATE_INTAKE_IT.md
E18_TARGET_MONEY: 100000
E18_BASELINE_VS_CLAUDE: 132217.68
E18_BASELINE_SYMMETRIC_662: 79323.86
E18_GAP_TO_TARGET: 20676.14 / +26.1%_REQUIRED
E18_DYNAMIC_TOURNAMENT: COMPLETE_56_OF_56 / ARCHITECTURE_GATE_PASS_10_OF_10
E18_DYNAMIC_TOPOLOGY: 662_28_OF_42 / 770_14_OF_42
E18_DYNAMIC_MODE_BY_OPPONENT: CLAUDE_AND_CONTROL_662 / COPILOT_770
E18_DYNAMIC_DIVERGENCE: ACTION_14_OF_14 / TOPOLOGY_14_OF_14
E18_DYNAMIC_MONEY: OVERALL_111654.45 / VS_662_80456.43 / VS_CLAUDE_127072.71 / VS_COPILOT_127434.21
E18_DYNAMIC_DELTA_VS_662: -3472.29 / -4.14_PERCENT
E18_REACTIVITY_GATE: PASS_CONDITIONED_ACTION_AND_TOPOLOGY_DIVERGENCE
E18_SAFETY_GATE: PASS_14_OF_14 / VERIFIED_LOSSES_0 / ERRORS_0 / FALLBACKS_0 / BREACHES_0
E18_MANIFEST: experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json
E18_PLAN: experiments/e18/design/E18_REACTIVE_662_TOP3_BENCHMARK_PLAN_V1.md
E18_REPORT: experiments/e18/reports/common/E18_662_TOP3_BASELINE_BENCHMARK_IT.md
E18_LIFECYCLE_REPORT: experiments/e18/reports/common/E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md
E18_LIVE_BENCHMARK_REPORT: experiments/e18/reports/common/E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_IT.md
E18_DYNAMIC_REPORT: experiments/e18/reports/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md
E18_NEXT_CANDIDATE_PROMPT: experiments/e18/prompts/common/E18_DYNAMIC_ARCHITECTURE_NEXT_CANDIDATE_PROMPT_IT.md
E18_CLAUDE_BUILD_PROMPT: experiments/e18/prompts/claude/E18_CLAUDE_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md
E18_COPILOT_BUILD_PROMPT: experiments/e18/prompts/copilot/E18_COPILOT_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md
E18_FOUR_AGENT_TOURNAMENT: COMPLETE_84_OF_84 / 6_PAIRS / 7_DEV_SEEDS / BOTH_SEATS
E18_FOUR_AGENT_RECORDS: CODEX_42-0 / CLAUDE_26-16 / COPILOT_16-26 / ANTIGRAVITY_0-42
E18_FOUR_AGENT_MONEY: CODEX_125983.74 / CLAUDE_6467.48 / COPILOT_2840 / ANTIGRAVITY_0
E18_FOUR_AGENT_PROMOTION: NONE
E18_ANTIGRAVITY_ROUNDS: 42_TOTAL / 14_PER_OPPONENT / P0_21 / P1_21 / ENGINE_COMPATIBILITY_FAIL
E18_LATEST_VS_V4D_BENCHMARK: COMPLETE_56_NEW_MATCHES_PLUS_42_FROZEN_COMPARATORS
E18_LATEST_VS_V4D_DIRECT: LATEST_0-14 / 71831.00_VS_89760.57 / DELTA_-19.97_PERCENT
E18_LATEST_VS_V4D_COMMON_POOL: 125983.74_VS_143486.45 / DELTA_-12.20_PERCENT
E18_LATEST_VS_V4D_DIAGNOSIS: PRODUCTIVE_-6.11_PERCENT / PASS_+24.77_PERCENT / WEED_TILE_DAYS_+320_PERCENT
E18_ECONOMIC_CONTROL: E17_V4D_RESTORED / E18_1_DIAGNOSTIC_ONLY
E18_KAGGLE_LIVE_SNAPSHOT: E18_1_825.4 / E17_662_941.4 / V4D_1131.7 / REACTIVE_1077.5 / V9_1082.9
E18_PEER_V2_REAL_ENGINE_TOURNAMENT: COMPLETE_84_OF_84 / V4D_ONLY_GATE_PASS
E18_CLAUDE_V2_INTAKE: REAL_ENGINE_MEAN_9756.29 / LOSSES_44 / NOT_PROMOTED
E18_COPILOT_V2_INTAKE: REAL_ENGINE_MEAN_260 / NOT_PROMOTED
E18_ACTIVE_TEST_ROSTER: CODEX_V4D_CONTROL / CODEX_E18_1_ABLATION / CLAUDE_E18_2 / COPILOT_E18_2
E18_ANTIGRAVITY_ACTIVE_STATUS: EXCLUDED_UNTIL_NEW_RELEASE
E18_CODEX_V2_DEV_GATE: PASS_9_OF_9 / 56_0 / MONEY_121149.84
E18_CODEX_V2_DIRECT_V4D: 14_0 / +3.77_PERCENT
E18_CODEX_V2_TOPOLOGY: V4D_7_7_5_PRESERVED / ON_TILE_RECOVERY_ONLY
E18_CODEX_V2_SAFETY: LOSSES_0 / ERRORS_0 / FALLBACKS_0
E18_KAGGLE_STABILITY_RULE: 4_VALID_HOURLY_SNAPSHOTS_OVER_3H / SCORE_RANGE_LT_50
E18_KAGGLE_MONITOR_STATUS: PROTOCOL_READY_NOT_SCHEDULED / AUTOMATION_TOOL_UNAVAILABLE / BROWSER_READ_BLOCKED
E18_KAGGLE_MONITOR_PROTOCOL: experiments/e18/prompts/codex/E18_CODEX_KAGGLE_STABILITY_MONITOR_PROTOCOL_IT.md
E18_CLAUDE_V2_PROMPT: experiments/e18/prompts/claude/E18_CLAUDE_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md
E18_COPILOT_V2_PROMPT: experiments/e18/prompts/copilot/E18_COPILOT_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md
E18_ANTIGRAVITY_REBOOT_PROMPT: experiments/e18/prompts/antigravity/E18_ANTIGRAVITY_REACTIVE_V1_REBOOT_PROMPT_IT.md
E18_FOUR_AGENT_REPORT: experiments/e18/reports/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2_REPORT_IT.md
E18_SUBMISSION_PARITY: ISOLATED_PASS / 719_OF_719_BOTH_REGIMES
E18_SUBMISSION_ROLE: READY_EXTERNAL_DIAGNOSTIC_NOT_BASELINE_REPLACEMENT
E18_KAGGLE_STATUS: SUBMITTED_PENDING_2026_09_03 / SCORE_NOT_AVAILABLE
E18_HOLDOUT: NOT_CONSUMED / NOT_AUTHORIZED
NEXT_ACTION: BUILD_E18_4_V2_LOCALITY_TASK_AGING_ABLATION / NO_KAGGLE_UPLOAD
```

## Stato raggiunto

E17 è chiuso. La candidata Codex 6-6-2 mantiene 14 pascoli target riempiti,
cinque celle recuperate a crop, zero breach Q2 e zero fughe. La submission
Kaggle `559767808` ha uno snapshot `1009,8`, ancora in stabilizzazione.

La diagnostica E18.1 aggiunge un selector D6 sulla sola farm pubblica
avversaria: `6-6-2` contro Claude/controllo e `7-7-0` contro Copilot. Nel
torneo development da 56 match supera tutti i gate dinamici e di sicurezza,
con 14/14 pascoli e zero perdite verificate. La media globale è 111.654,45,
ma nel diretto col controllo 662 perde il 4,14%; resta quindi una submission
diagnostica, non la nuova baseline. Claude e Copilot devono ora presentare
candidate valutate anche su regime activation, action/topology divergence e
lifecycle, non soltanto sullo score.

Il successivo benchmark controllato contro il bundle V4D corregge il
riferimento economico: E18.1 perde `14/14` diretti, con `71.831,00` contro
`89.760,57` (`-19,97%`), e resta sotto del `12,20%` sul pool comune. Il calo
di azioni produttive (`-6,11%`) si converte quasi interamente in `PASS`
(`+24,77%`), mentre i weed tile-days crescono del `320%`. V4D torna quindi
controllo economico obbligatorio; E18.1 conserva solo il ruolo diagnostico.

Lo snapshot Kaggle ora accessibile mostra `825,4` per E18.1, `941,4` per la
6-6-2 E17.3 e `1.131,7` per V4D. Le nuove peer V2 entrano in intake senza
Antigravity: Claude ha evidenza real-engine ma fallisce ancora i gate;
Copilot è callable, mentre il suo benchmark dichiarato è sintetico e deve
essere rifatto integralmente nel motore reale.

Il torneo delta finale è completo: 84 match development, senza holdout/final.
Claude V5 non è promossa (`+8,53%` shared ma `-9,57%` diretto); V6 è respinta
(`1-13`, 3Q `1/14`). La 6-6-2 V3 attribuita al lavoro Copilot è identica alla
V2 in `28/28` profili ed è anch'essa non promossa.

E18 è aperto con la V2 come baseline. Il benchmark Top 3 è osservazionale:
gli archetipi storici `tetsuya`, `OceanMix` e `Crop Dusta` provengono da replay
E17 già consumati. Il primo gate è dimostrare attivazione causale; solo dopo si
misura il gap self-play di `20.676,14` (`+26,1%`) verso 100k.

La Foundation C2.1 e il riordino del repository sono chiusi con gate A7
`PASS`. La strategia E17 è stata riconciliata e congelata dopo tre review
indipendenti. E17.0 è completo per Codex, Antigravity e Copilot. Una decisione
successiva del proprietario autorizza ora E17.1, con Codex V9 congelata come
controllo, Codex reattivo come evoluzione derivativa e Claude reattivo come
policy indipendente. Antigravity e Copilot restano congelati. Codex V9 resta la
baseline e la submission Kaggle correnti. Il benchmark discovery E17 è stato
completato su nove replay unici dei tre player che occupavano il Top 3 nello
snapshot di raccolta (`tetsuya`, `OceanMix`, `Crop Dusta`), con 18 player-seat
e 720 step per episodio.

La review cross-agent è formalmente chiusa:

- Copilot: `ACCEPT_WITH_CHANGES`;
- Antigravity: `ACCEPT`;
- audit fughe Crop Dusta: 31/31 eventi compatibili con fuga secondo criterio
  EOD stretto, classificati `DERIVED`;
- nessuna policy è stata modificata durante benchmark e review.

L'audit successivo dell'attivazione Claude è
`PASS_WITH_LOCAL_CLEANUP`: tutte le scritture sono rimaste nei namespace
assegnati, non risultano letture dei sorgenti strategici altrui, import
proibiti, uso dei seed riservati o mutazioni Git. Il bootstrap locale
`CLAUDE.md` è stato rimosso; i prompt puntano ora ai documenti canonici. I
replay grezzi sono consolidati nella cartella unica `data/replays/json/` e
catalogati in `json.md`. I ledger Codex development e Claude V1, riproducibili
e già sintetizzati, sono stati rimossi; i ledger Claude V2 restano disponibili
localmente per la remediation V3 e sono esclusi da Git.

Il benchmark esterno della probe reattiva è completo su dieci replay della
submission Kaggle `559631298`: 5W-5L, denaro medio `78.808,7`, zero fughe e
3Q in 10/10. La policy ha emesso una sola sequenza completa di comandi nei
dieci episodi, mentre lo stato strutturale eseguito presenta quattro hash:
nel campione le guardie reattive non hanno quindi prodotto una divergenza
osservabile dell'action stream. La quota Q2 è il `63,29%` degli
animal-tile-days Q0 tra sblocco Q2 e D28, intermedia fra tetsuya (`75,38%`),
Crop Dusta (`38,17%`) e OceanMix (`0%`). La quota Q2 è diventata un outcome,
non il trattamento. Il controller `MARKET_REGIME_ADAPTATION` V2 è stato
verificato su 48 episodi development: +1,55% sul controllo inerte,
action-stream discriminanti, 100% di override tracciati, zero errori e zero
fughe. La composizione animale Q0/Q1/Q2 resta 8/6/5: il solo timing
commerciale non rende ancora reattiva la struttura. I replay esterni restano
diagnostici e holdout/final confirmation non sono stati usati. Report:
`experiments/e17/reports/codex/E17_CODEX_TRUE_REACTIVITY_DEVELOPMENT_REPORT_IT.md`.

Il passo successivo è stato eseguito con
`REACTIVE_SERVICE_AND_ROUTING_CORE_V2`. Il core ricostruisce dallo stato
osservato task di servizio e percorsi, senza cambiare il blocco market. Un
override locale della routine è stato respinto perché i suoi `PASS` sono
anche punti impliciti di sincronizzazione; la soluzione promossa usa un
handoff progressivo al giorno 29. Su 12 episodi development matched ottiene
`131.947,17` contro `134.060,17` (`−1,576%`), genera 750 comandi di routing e
252 servizi, classifica tutti i 1.434 record del ledger e mantiene a zero
errori, mutazioni market e fughe. È una prova architetturale, non una
submission. Il prossimo test è anticipare l'handoff a D28 coordinando
raccolta, deposito e liquidazione terminale. Report:
`experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_DEVELOPMENT_REPORT_IT.md`.

La V3 ha completato il passaggio a D28: FEED e WATER preparano l'ultimo ciclo,
gli output vengono depositati senza serializzare artificialmente gli accessi
shed e D29 coordina DROP e SELL nello stesso batch. Nei 12 episodi matched la
media è `134.351,33` contro `134.060,17` (`+0,217%`), ossia circa `+1,82%`
rispetto alla V2 D29. Il residuo vendibile terminale è zero, con zero fughe,
errori e violazioni market. Holdout e final confirmation restano intatti e la
V3 non è una submission. La prossima sessione deve mantenere D28, introdurre
routing per cluster e rientri basati su inventario/slack, e tentare D27 solo
dopo avere preservato score, sicurezza e liquidazione completa. Report:
`experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_REPORT_IT.md`.

Il trattamento logistico è stato poi scomposto causalmente. V4A riduce i MOVE
ma perde `2,529%` per overflow EOD dello shed; V4B mostra che l'affinità di
quadrante non aggiunge efficienza; V4C rileva la pressione di capacità ma la
guardia Wheat impedisce il flush. V4D rilascia i carrier soltanto dopo il feed
completo e supera tutti i gate: `135.096,83` contro `134.351,33` (`+0,555%`),
delta positivo in 6/6 confronti, `MOVE/service = 2,872`, zero fughe, errori e
residui terminali. È la candidata interna corrente, non una submission. La
prossima sessione deve stressare V4D nei regimi market development già
controllati prima di valutare D27. Report:
`experiments/e17/reports/codex/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md`.

## Evidenza E17 consolidata

I nove replay mostrano tre archetipi diversi, tutti 3Q NW→NE→SW e senza Q3:

| Profilo | Q1 | Q2 | Topologia | MOVE/produttive | Rischio terminale |
|---|---|---|---|---:|---|
| `tetsuya` | D7 | D10 | bestiame distribuito, Q1 crop-dense | 1,2553 | 0 fughe, inventario 0 |
| `OceanMix` | D6 | D11 | livestock Q0/Q1, Q2 crop-only | 1,0468 | 0 fughe |
| `Crop Dusta` | D5–D6 | D8–D9 | tre quadranti misti e dispersi | 1,4267 | 31 fughe derivate |

Questi dati supportano il 3Q e il picco di 12 hands come baseline di lavoro,
non come ottimi globali. Non identificano causalmente il vantaggio di D10,
della topologia compatta o della diversificazione. Rating Kaggle, denaro finale
dei replay e score dei runner locali restano metriche diverse.

Lo snapshot leaderboard del 2026-09-02 cambia l'ordine: `Crop Dusta` è primo
con 2.917,8, `tetsuya` secondo con 2.890,3 e `3정훈` terzo con 2.878,5;
`OceanMix` non compare nei primi sette visibili. Il benchmark resta valido
come confronto di tre archetipi, ma non va più chiamato fotografia del Top 3
corrente. La leadership di Crop Dusta rende obbligatorio mantenere in E17 una
frontiera di espansione precoce/diversificata; non annulla però le 31 fughe
derivate né autorizza a saltare ledger e vincoli di serviceability.

## Strategia E17 congelata

Il draft iniziale resta disponibile come provenance; il riferimento normativo
corrente è:

`experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`

Principio cardine: **E17 non deve convergere a priori verso un singolo
archetipo**. `tetsuya`, `OceanMix` e `Crop Dusta` sono tre combinazioni
osservate di fattori. Timing, topologia, densità, capitale, specie e chiusura
devono essere separati e testati causalmente. Solo dopo la misura degli effetti
principali sono ammessi test di interazione e una candidata composita.

La sequenza condivisa è:

1. `E17.0` — ledger requested/executed a parità comportamentale;
2. `E17.1` — singola guardia fill-aware sul mercato WHEAT;
3. `E17.2` — contrasto topologico distribuito vs livestock compatto Q0/Q1;
4. `E17.3` — anticipo isolato di Q2 da D11 a D10;
5. `E17.4` — liquidazione terminale reattiva;
6. `E17.5` — diversificazione di una sola specie per esperimento;
7. `E17.6` — checkpoint obbligatorio della frontiera Q2 D8, soltanto con zero
   fughe e serviceability provata.

Le linee minime da confrontare includono:

- timing Q2 `D11 / D10 / D8`;
- livestock `distribuito / compatto Q0-Q1 / misto nei tre quadranti`;
- diversificazione crop `3 / 4 / 5 specie`;
- diversificazione animale `2 / 3 specie`;
- reinvestimento aggressivo vs riserva di liquidità;
- liquidazione e servicing terminale reattivi vs schedule fisso.

E17.0 ha aggiunto il ledger comune `E17_LEDGER_V1` fuori dal decision path.
Codex ha dimostrato parità `4314/4314`, outcome e stato terminale `6/6`, senza
modificare la V9. Antigravity e Copilot hanno eliminato la dipendenza dalle
routine Codex e costruito baseline native con audit locale d'indipendenza
`PASS`. Tutti i ledger hanno record coverage del 100%, zero errori tecnici e
zero fughe EOD derivate.

Il PASS è tecnico, non competitivo. Antigravity attiva tre quadranti ma
consuma tutto il capitale iniziale (`max_hands=0`, reward 0 in 6/6); Copilot è
produttiva ma ottiene mean 8.941,5 contro opponent inert. Codex V9 ottiene mean
132.019,3 sulla stessa matrice development. Al termine di E17.0 queste
differenze non autorizzavano una promozione; il nuovo torneo è autorizzato da
un decision record successivo e non modifica retroattivamente quel verdetto.

## Prossima azione operativa

1. costruire fixture controllate per `growth`, `service_pressure`,
   `market_contention` e `liquidation`;
2. registrare transizioni, feature causali, guard activation, ordini visti,
   ordini throttled e unità soppresse;
3. richiedere divergenza spiegabile dalla V2 prima di qualsiasi torneo
   economico E18;
4. preservare `6-6-2`, `14/14`, Q2 ≤2, zero fughe e residuo terminale zero;
5. usare soltanto i nuovi seed development preregistrati nel manifest E18;
   holdout e final-confirmation restano non autorizzati.

## Esibizione reattiva development a tre

La matrice seat-balanced sui sette seed development è completa: 42/42 match,
zero errori. Codex V9 e Codex reattivo sono primi ex aequo con `15-12-1`,
media 112.149,21, zero fughe e delta diretto medio zero. Claude V2 chiude
`0-0-28`, media 11.777,64, due fughe e MOVE/produttive 2,9719. In ogni match
competitivo Claude ha comunque raggiunto 3Q. Nessun override Codex è scattato,
quindi il vantaggio Kaggle non è riprodotto dalla matrice locale corrente.

Report:
`experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`.

## Confronto esterno E17

Antigravity non è disponibile per esaurimento dei crediti. Il proprietario ha
quindi escluso il torneo locale incompleto e autorizzato una submission E17
per confronto esterno. La candidate mantiene le azioni V9 con soli metadati
di release aggiornati ed è identificata come controllo
`CODEX-E17.0-EXTERNAL-CONTROL-V1`. La submission Kaggle `559588638` è attiva:
la rilevazione più recente fornita dal proprietario è `996`, dopo un ingresso
a `600` (`+396`), con un episodio ancora in corso nello snapshot. È evidenza
osservata ma non ancora un rating stabile né uno score conclusivo. Il report è
in
`experiments/e17/reports/codex/E17_EXTERNAL_SUBMISSION_READINESS_REPORT_IT.md`.

## Gate E17 storici

Questi gate appartenevano alla proposta E17 e non sono i gate operativi E18;
E18 usa il manifest e il piano activation-first elencati sotto.

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
COMPETITIVE_MIRROR >= 90000
ANIMAL_ESCAPES == 0
MOVE_PER_PRODUCTIVE <= 1.20
EXECUTED_MARKET_LEDGER_COVERAGE == 100%
STRATEGIC_INDEPENDENCE_GATE == PASS  # per il prossimo torneo a tre
```

## Vincoli inderogabili

- nessun agente può importare o copiare routine, action table, planner,
  dispatcher o schedule di un altro;
- Foundation, replay discovery, schema del ledger e protocollo di benchmark
  possono essere condivisi;
- ogni variazione strategica deve modificare una sola famiglia causale;
- i nove replay Top 3 sono dati offline di discovery, mai input online;
- distinguere sempre `requested`, `executed`, `DERIVED` e `UNKNOWN`;
- nessuna submission Kaggle prima del superamento dei gate preregistrati,
  salvo autorizzazione esplicita del proprietario per un controllo esterno
  dichiarato e senza mutazione di policy.

## Documenti da leggere

- `docs/PROJECT_STATE.md`;
- `experiments/e18/README.md`;
- `experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json`;
- `experiments/e18/design/E18_REACTIVE_662_TOP3_BENCHMARK_PLAN_V1.md`;
- `experiments/e18/reports/common/E18_662_TOP3_BASELINE_BENCHMARK_IT.md`;
- `experiments/e17/reports/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3_REPORT_IT.md`;
- `experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md`;
- `docs/repository/REPOSITORY_ARCHITECTURE.md`;
- `docs/repository/migration/POST_E17_EXTERNAL_RELEASE_CLEANUP.md`;
- `experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`;
- `experiments/e17/reviews/common/E17_STRATEGY_RECONCILIATION.md`;
- `experiments/e17/reports/common/E17_0_GATE_AND_BLOCKER_SUMMARY.md`;
- `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`;
- `experiments/e17/reviews/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md`;
- `experiments/e17/reports/codex/E17_TOP3_REPLAY_ANALYSIS.md`;
- `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`;
- `docs/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`;
- `docs/model_specs/codex/CODEX_V9_E17_RUNTIME_AND_FOUNDATION_MAPPING_IT.md`;
- `experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md`;
- `experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`;
- `experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_3Q_INDEPENDENT_BUILD_PROMPT.md`;
- `experiments/e17/reviews/common/E17_CLAUDE_ACTIVATION_COMPLIANCE_AND_CLEANUP_AUDIT.md`;
- `experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`;
- `experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md`.
