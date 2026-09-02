# E17 — experiment entry point

## Status

```text
PHASE: E17.0 COMPLETE / EXTERNAL CONTROL LIVE / E17.1 NOT STARTED
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
E17_LAUNCH: E17_0_EXECUTED
E17_POLICY_MUTATION: NOT_STARTED
BASELINE: CODEX V9 frozen; source/config/hash preserved
COMMON_REVIEW: STRATEGY_RECONCILED_AND_FROZEN
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_EXTERNAL_SUBMISSION: LIVE_SCORE_STABILIZING
E17_KAGGLE_SUBMISSION_ID: 559588638
ACTIVE_DEVELOPMENT_AGENT: CODEX_ONLY
```

## Goal

E17 è il round di benchmark e misura della famiglia 3Q. Il riordino del
repository ha superato il gate A7, la strategia è stata congelata ed E17.0 è
stato completato senza mutazioni della policy Codex e senza avviare E17.1.

## Common protocol

- Foundation and observation contract remain shared.
- Agent-specific policies stay agent-local and must not import or copy another agent's routines or action table.
- The ledger must be measured before optimization and must be kept outside the decision path.

## Ownership and responsibilities

- Codex: repository integration owner for the common migration and reconciliation.
- Antigravity: own the non-controversial Antigravity-specific migration set.
- Copilot: own the non-controversial Copilot-specific migration set and preserve truthful derivative disclosure.

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

## Prossimo step causale proposto

Il prossimo esperimento proposto è il test monofattoriale di `RQ3` sul timing
di Q2:

- `D11` come baseline di controllo;
- `D10` come timing intermedio;
- `D8` come frontiera aggressiva da validare.

Il test richiede ancora autorizzazione esplicita e deve essere eseguito senza
mutare la baseline Codex congelata, con ledger obbligatorio per ogni run.

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
economicamente debole rispetto a Codex V9. E17.1 non è iniziato.

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
- rating osservato: `600 -> 996` (`+396`), rilevazione intermedia non stabile;
- Copilot: baseline nativa conservata localmente, nessuna submission;
- Antigravity: pausa per esaurimento crediti;
- prossima decisione: dopo la stabilizzazione del rating esterno.
