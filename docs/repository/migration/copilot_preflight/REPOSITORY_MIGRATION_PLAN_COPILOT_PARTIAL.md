# Repository migration plan (frozen at preflight)

## Status

This plan is intentionally frozen at the preflight stage. It is not a declaration that the repository reorganization is complete. It is the authoritative record of the non-controversial, Copilot-owned subset that can be safely triaged before the full three-agent reconciliation.

## Scope

- Preserve all canonical Foundation and runtime files.
- Keep user-owned historical artifacts intact.
- Avoid moving the Common or Codex-owned paths unless Codex owns the manifest and destination.
- Create the target `experiments/e17/` structure and place round-local outputs there only where ownership is clear.

## Planned moves (Copilot-owned / common non-controversial)

| Source | Destination | Owner | Reason |
|---|---|---|---|
| `experiments/e17/reports/copilot/E17_TOP3_REPLAY_ANALYSIS.md` | `experiments/e17/reports/copilot/E17_TOP3_REPLAY_ANALYSIS.md` | Copilot | Round report; belongs under E17 reports |
| `experiments/e17/artifacts/discovery/copilot/E17_TOP3_REPLAY_METRICS.json` | `experiments/e17/artifacts/derived/copilot/E17_TOP3_REPLAY_METRICS.json` | Copilot | Derived metrics artifact |
| `experiments/e17/reviews/copilot/E17_CROSS_AGENT_FEEDBACK_AND_COPILOT_CRITICAL_ANALYSIS_IT.md` | `experiments/e17/reviews/copilot/E17_CROSS_AGENT_FEEDBACK_AND_COPILOT_CRITICAL_ANALYSIS_IT.md` | Copilot | Review output; belongs in reviews |
| `experiments/e17/tools/copilot/analyze_top3_replays.py` | `experiments/e17/tools/copilot/analyze_top3_replays.py` | Copilot | Round-local analysis tool |
| `experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md` | `experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md` | Common | Round governance prompt |
| `experiments/e17/prompts/common/E17_TOP3_REPLAY_INDEPENDENT_ANALYSIS_PROMPT.md` | `experiments/e17/prompts/common/E17_TOP3_REPLAY_INDEPENDENT_ANALYSIS_PROMPT.md` | Common | Shared analysis prompt |
| `experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md` | `experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md` | Common | Draft strategy is round-scoped |
| `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md` | `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md` | Common | Common cross-agent report |
| `experiments/e17/reviews/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md` | `experiments/e17/reports/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md` | Common | Common reconciliation feedback |

## Decision

The migration is not executed as a blanket repository move because the full gate remains blocked. The freeze is a record of intended ownership and target placement, not a completed reorganization.

## Gate status

```text
REPOSITORY_TREE_MATCHES_ARCHITECTURE: NOT_YET
NO_LOST_TRACKED_FILES: PENDING
MIGRATION_MANIFEST_COVERAGE: 100% on Copilot subset only
IMMUTABLE_HASHES_PRESERVED: PASS for preserved artifact set
MARKDOWN_LINK_CHECK: PENDING
PYTHON_IMPORT_CHECK: PENDING
TEST_SUITE: PENDING
SUBMISSION_CODEX_SHA256: AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421
UNRESOLVED_BLOCKERS: 1 (missing three-agent reconciliation)
POST_MIGRATION_REVIEWS: 1/3 (Copilot only)
REPOSITORY_REORGANIZATION_STATUS: IN_PROGRESS
```
