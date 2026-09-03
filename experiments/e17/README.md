# E17 — experiment entry point

## Status

```text
PHASE: E17.3 6-6-2 TOURNAMENT COMPLETE / HOLDOUT NOT USED
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
E17_LAUNCH: E17_0_EXECUTED
E17_POLICY_MUTATION: CODEX_SERVICE_ROUTING_V3_CONTROL / CODEX_POST_FEED_CAPACITY_BATCHING_V4D_INTERNAL
BASELINE: CODEX V9 frozen; source/config/hash preserved
COMMON_REVIEW: STRATEGY_RECONCILED_AND_FROZEN
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_EXTERNAL_SUBMISSION: REACTIVE_LIVE_SCORE_STABILIZING
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
E17_662_SUBMISSION: submission/submission_codex_e17_topology_662.py
E17_662_TOPOLOGY: Q0_6 / Q1_6 / Q2_2 / FILLED_14_OF_14
E17_THREE_AGENT_TOURNAMENT: COMPLETE_42_OF_42_DEVELOPMENT_NON_QUALIFYING
E17_THREE_AGENT_STANDINGS: CODEX_28_0_0 / CLAUDE_14_14_0 / COPILOT_0_28_0
E17_THREE_AGENT_REPORT: experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md
ACTIVE_DEVELOPMENT_AGENTS: CODEX, CLAUDE, COPILOT
CODEX_REACTIVE_STATUS: FROZEN_FOR_REACTIVE_TOURNAMENT
CLAUDE_REACTIVE_STATUS: V1_REJECTED / V2_FROZEN_WITH_FAILED_GATES
CLAUDE_ACTIVATION_AUDIT: PASS_WITH_LOCAL_CLEANUP
CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK: AUTHORIZED_DEVELOPMENT_ONLY
CLAUDE_V3_IMPLEMENTATION: COMPLETE_FROZEN_WITH_FAILED_GATES
CLAUDE_V3_10X_PROMPT: experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_V3_10X_ACTIVATION_PROMPT_IT.md
THREE_WAY_TOURNAMENT: OFFICIAL_HOLDOUT_BLOCKED
THREE_WAY_DEVELOPMENT_EXHIBITION: COMPLETE_42_OF_42_NON_QUALIFYING
ANTIGRAVITY: OWNER_UNAVAILABLE_UNTIL_2026_09_04 / EXCLUDED_FROM_E17_3_TOURNAMENT
COPILOT: E17_0_NATIVE_INCLUDED_IN_DEVELOPMENT_TOURNAMENT / NO_POLICY_MUTATION
NEW_KAGGLE_SUBMISSION: E17_662_OWNER_ACTION_REPORTED / ID_AND_SCORE_PENDING
NEXT_ACTION: RECORD_E17_662_KAGGLE_ID_AND_SCORE / RUN_ONE_FACTOR_DEVELOPMENT_ABLATIONS
```

## Goal

E17 è il round di benchmark e misura della famiglia 3Q. Il riordino del
repository ha superato il gate A7, la strategia è stata congelata ed E17.0 è
stato completato senza mutazioni della policy Codex. Un decision record
successivo autorizza ora lo sviluppo E17.1 e il torneo reattivo a tre.

## Common protocol

- Foundation and observation contract remain shared.
- Agent-specific policies stay agent-local and must not import or copy another agent's routines or action table.
- The ledger must be measured before optimization and must be kept outside the decision path.

## Ownership and responsibilities

- Codex: repository integration owner for the common migration and reconciliation.
- Claude: own an independent state-reactive policy in the Claude namespace.
- Antigravity: frozen and unavailable until 2026-09-04; excluded from the
  E17.3 development tournament.
- Copilot: E17.0 native freeze reused without mutation in the E17.3
  development tournament.

## Materiali correnti e congelati

- `experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md`
- `experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`
- `experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json`
- `experiments/e17/reviews/common/E17_STRATEGY_RECONCILIATION.md`
- `experiments/e17/reports/common/E17_0_GATE_AND_BLOCKER_SUMMARY.md`
- `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`
- `experiments/e17/reports/common/E17_RQ3_Q2_TIMING_PRECHECK_IT.md`
- `experiments/e17/reviews/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md`
- `experiments/e17/reports/copilot/E17_TOP3_REPLAY_ANALYSIS.md`
- `experiments/e17/artifacts/discovery/copilot/E17_TOP3_REPLAY_METRICS.json`
- `experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md`
- `experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`
- `experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_3Q_INDEPENDENT_BUILD_PROMPT.md`
- `experiments/e17/reviews/common/E17_REACTIVE_TOURNAMENT_CANDIDATE_AMENDMENT_2.md`
- `experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`
- `experiments/e17/reviews/common/E17_CLAUDE_ACTIVATION_COMPLIANCE_AND_CLEANUP_AUDIT.md`
- `experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`
- `experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md`
- `experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_V3_10X_ACTIVATION_PROMPT_IT.md`
- `experiments/e17/reports/codex/E17_REACTIVE_EXTERNAL_REPLAY_BENCHMARK_IT.md`
- `experiments/e17/design/E17_CODEX_TRUE_REACTIVITY_ACTIVATION_PLAN_V1.md`
- `experiments/e17/reports/codex/E17_CODEX_TRUE_REACTIVITY_DEVELOPMENT_REPORT_IT.md`
- `experiments/e17/design/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.md`
- `experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md`

## Sviluppo reattivo autorizzato

- Codex V9 resta immutabile come controllo open-loop.
- Codex sviluppa una variante reattiva derivativa con override tracciati.
- Claude sviluppa una policy reattiva nativa e indipendente.
- Si usano soltanto seed development prima del freeze delle candidate.
- Il torneo round-robin holdout richiede entrambi i freeze con gate PASS;
  Claude V2 non ha superato il gate e quindi l'holdout resta bloccato.
- L'esibizione development a tre è completa: 42 match seat-balanced sui sette
  seed già consumati, con ruolo `DEVELOPMENT_ONLY_NON_QUALIFYING`.
- Antigravity e Copilot non sono modificati e non partecipano.
- L'audit dell'attivazione Claude è `PASS_WITH_LOCAL_CLEANUP`; il bootstrap
  locale in radice è stato rimosso e i ledger grezzi restano locali/gitignored.
- La futura V3 può affrontare Codex come benchmark black-box development, ma
  non può leggere, analizzare, copiare o importare artefatti strategici Codex.

## Gate repository chiuso

```text
REPOSITORY_TREE_MATCHES_ARCHITECTURE: PASS
NO_LOST_TRACKED_FILES: PASS
MIGRATION_MANIFEST_COVERAGE: 100%
IMMUTABLE_HASHES_PRESERVED: PASS
MARKDOWN_LINK_CHECK: PASS
PYTHON_IMPORT_CHECK: PASS
TEST_SUITE: PASS
UNRESOLVED_BLOCKERS: 0
POST_MIGRATION_REVIEWS: 3/3
```

Le tre review indipendenti e i tre report E17.0 sono disponibili. I gate
tecnici sono superati, ma la competitività delle baseline native non è stata
stabilita: Antigravity è 3Q ma non produttiva, Copilot è produttiva ma ancora
economicamente debole rispetto a Codex V9. Questo è il verdetto storico di
E17.0; E17.1 è ora autorizzato dal decision record successivo.

Poiché Antigravity non è disponibile, il proprietario ha escluso il torneo
locale incompleto e autorizzato la preparazione di un controllo esterno Kaggle.
La candidate mantiene parità comportamentale completa con la V9 e non
costituisce una nuova ottimizzazione; cambiano soltanto i metadati di release.

## Controllo esterno E17

- submission: `submission/submission_codex.py`;
- release: `CODEX-E17.0-EXTERNAL-CONTROL-V1`;
- SHA-256: `0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6`;
- report: `experiments/e17/reports/codex/E17_EXTERNAL_SUBMISSION_READINESS_REPORT_IT.md`;
- manifest: `experiments/e17/artifacts/freeze/codex/E17_EXTERNAL_SUBMISSION_MANIFEST.json`;
- upload: eseguito, submission Kaggle `559588638`;
- rating controllo osservato nello snapshot successivo: `1089,7`;
- submission reattiva separata: `submission/submission_codex_e17_reactive.py`;
- rating reattivo osservato: `1353,6`, delta `+263,9` (`+24,2%`) dal controllo;
- Copilot: congelato, escluso dal torneo reattivo;
- Antigravity: congelato, escluso dal torneo reattivo;
- Codex reattivo: development `PASS`, congelato per il torneo;
- Claude reattivo V1: respinto (mean 9.201,71; otto fughe);
- Claude V2: indipendenza e tecnica PASS, ma gate complessivo FAIL (mean
  14.445,29; tre fughe; 3Q 13/14 nel passivo);
- esibizione: Codex V9 e reattivo `15-12-1`, Claude `0-0-28`; holdout intatto;
- Claude V3: implementazione completa e congelata con gate falliti; resta un
  benchmark indipendente di sviluppo, non una candidata al torneo holdout;
- Codex true-reactive V2: 48 run development, gate di reattività e sicurezza
  PASS, ma solo la famiglia commerciale è state-dependent;
- Codex service-routing core V2: 12 run matched, handoff D29, media
  `131.947,17` vs `134.060,17` (`−1,576%`), architettura ora superata
  internamente dalla V3;
- Codex service-routing V3: handoff D28, media `134.351,33` vs `134.060,17`
  (`+0,217%`), zero residuo vendibile, fughe ed errori; tutti i gate
  development PASS, nessuna submission e nessun holdout consumato;
- prossima decisione: mantenere D28 e ridurre `MOVE/service = 3,000` con
  routing raggruppato per cluster e inventario prima di tentare D27.

## E17.2 — service and routing state-driven

Il dispatcher `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V2` costruisce dallo
snapshot corrente task fattibili di WATER, FEED, staging Wheat, HARVEST, CARE,
BUILD, PLACE, PICKUP, DIG, PLANT e DROP, assegnandoli per priorità, distanza e
continuità. Per il benchmark congelato subentra alla routine soltanto dal
giorno 29 e, nella finestra terminale, attiva HARVEST e DROP; il market resta
identico al controllo.

L'handoff progressivo evita di trattare i `PASS` della routine come slot
inutili: gli smoke test hanno mostrato che contengono sincronizzazione
posizionale implicita. Tutti i gate development passano, ma l'architettura
deve ancora dimostrare equivalenza economica su una finestra più ampia. Piano
e report canonici:

- `experiments/e17/design/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_PLAN_V1.md`;
- `experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_DEVELOPMENT_REPORT_IT.md`.

La V3 estende lo stesso core al giorno 28, prepara l'ultimo ciclo con FEED e
WATER e coordina HARVEST→DROP→SELL rispettando l'ordine di applicazione
dell'engine. I rientri possono condividere l'accesso shed e il liquidatore
considera anche i DROP fattibili nello stesso batch. La matrice matched di 12
episodi produce `134.351,33` contro `134.060,17` (`+0,217%`), zero unità
vendibili residue contro 54 del controllo, zero fughe e copertura completa dei
ledger unità (`3198/3198`) e market (`78/78`). È una candidata interna, non una
release Kaggle. Piano e report:

- `experiments/e17/design/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_PLAN_V2.md`;
- `experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_REPORT_IT.md`.

Il round V4 separa batching, affinità topologica e pressione di capacità. V4A
e V4C riducono i MOVE ma perdono `2,529%` per overflow EOD; V4B non migliora
la logistica. V4D abilita il flush dei carrier Wheat soltanto dopo che tutti
gli animali sono alimentati e passa tutti i gate: media `135.096,83` contro
`134.351,33` (`+0,555%`), delta positivo 6/6, `MOVE/service` 2,872, zero
fughe e residui terminali. La candidata resta development-only; il prossimo
passo è lo stress sui regimi market controllati. Piano e report:

- `experiments/e17/design/E17_CODEX_BATCHED_CLUSTER_ROUTING_PLAN_V1.md`;
- `experiments/e17/reports/codex/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md`.
