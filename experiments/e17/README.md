# E17 — experiment entry point

## Status

```text
PHASE: E17.1 DEVELOPMENT EXHIBITION COMPLETE / OFFICIAL HOLDOUT BLOCKED
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
E17_LAUNCH: E17_0_EXECUTED
E17_POLICY_MUTATION: CODEX_REACTIVE_FROZEN / CLAUDE_V2_FAILED_GATES
BASELINE: CODEX V9 frozen; source/config/hash preserved
COMMON_REVIEW: STRATEGY_RECONCILED_AND_FROZEN
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_EXTERNAL_SUBMISSION: REACTIVE_LIVE_SCORE_STABILIZING
E17_KAGGLE_SUBMISSION_ID: 559588638
ACTIVE_DEVELOPMENT_AGENTS: CODEX, CLAUDE
CODEX_REACTIVE_STATUS: FROZEN_FOR_REACTIVE_TOURNAMENT
CLAUDE_REACTIVE_STATUS: V1_REJECTED / V2_FROZEN_WITH_FAILED_GATES
CLAUDE_ACTIVATION_AUDIT: PASS_WITH_LOCAL_CLEANUP
CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK: AUTHORIZED_DEVELOPMENT_ONLY
CLAUDE_V3_IMPLEMENTATION: NOT_STARTED
THREE_WAY_TOURNAMENT: OFFICIAL_HOLDOUT_BLOCKED
THREE_WAY_DEVELOPMENT_EXHIBITION: COMPLETE_42_OF_42_NON_QUALIFYING
ANTIGRAVITY_AND_COPILOT: FROZEN_EXCLUDED
NEW_KAGGLE_SUBMISSION: REACTIVE_PROBE_UPLOADED_BY_OWNER
NEXT_ACTION: BENCHMARK_KAGGLE_REACTIVE_RESULTS
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
- Antigravity: frozen; excluded from the reactive tournament.
- Copilot: frozen; excluded from the reactive tournament.

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
- prossima decisione: remediation Claude V3 oppure esclusione esplicita dal
  protocollo prima di qualsiasi torneo ufficiale.
- stato V3: piano autorizzato ma implementazione non avviata; prima attività
  comune successiva: benchmark dei risultati Kaggle della probe reattiva.
