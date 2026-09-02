# Repository handbook

## Scope

This folder holds the repository-level governance needed to keep the project auditable: state, migration rules, ownership conventions, and the frozen migration plan.

## Current status

```text
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
E17_LAUNCH: EXTERNAL_CONTROL_LIVE / E17_1_NOT_AUTHORIZED
COMMON_GATE: PASS
POST_MIGRATION_REVIEWS: 3/3
THREE_AGENT_RECONCILIATION: COMPLETE
ACTIVE_DEVELOPMENT_AGENT: CODEX_ONLY
POST_E17_CLEANUP: PASS_WITH_LOCAL_CACHE_DEBT
```

## Target architecture

The target structure is the vertical round layout described in the E17 common prompt:

- `docs/` for stable cross-round documentation only
- `experiments/<round>/` for the full lifecycle of an experiment
- `data/` for immutable external inputs
- `src/` for maintained runtime code
- `submission/` for the canonical submission only

## Artefatti canonici di migrazione

- `docs/repository/migration/MIGRATION_INVENTORY_antigravity.csv`
- `docs/repository/migration/MIGRATION_INVENTORY_codex.csv`
- `docs/repository/migration/MIGRATION_INVENTORY_COPILOT.csv`
- `docs/repository/migration/REPOSITORY_MIGRATION_PLAN_FROZEN.md`
- `docs/repository/migration/REPOSITORY_MIGRATION_MANIFEST.csv`
- `docs/repository/migration/MIGRATION_EXECUTION_RESULTS.csv`
- `docs/repository/migration/POST_MIGRATION_REVIEW_antigravity.md`
- `docs/repository/migration/POST_MIGRATION_REVIEW_codex.md`
- `docs/repository/migration/POST_MIGRATION_REVIEW_COPILOT.md`
- `docs/repository/migration/POST_MIGRATION_RECONCILIATION.md`
- `docs/repository/migration/POST_E17_EXTERNAL_RELEASE_CLEANUP.md`

Il gate A7 è chiuso con copertura 1.058/1.058 e zero blocker. Il proprietario
ha successivamente autorizzato il checkpoint Git e il push dopo la pulizia
post-release E17.
