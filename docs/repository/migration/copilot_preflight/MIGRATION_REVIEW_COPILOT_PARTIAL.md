# Copilot repository migration preflight

## Scope

This review applies to the Copilot-owned round-specific artifacts and to the uncontroversial common E17 materials that are already in a migration candidate state. It does not claim a repository-wide reconciliation because the prompt requires three independent inventories and a common reconciliation by Codex before the full gate is valid.

## Direct findings

- The repository already contains a valid Copilot model spec under `docs/model/model_specs/copilot/` and it remains in the truthful derivative state.
- The E17 benchmark artifacts are still located under `results/e17/` and `scripts/e17/`, which is not aligned with the target tree described in the common prompt.
- The design and prompting materials for E17 are still in `docs/` and should be moved under `experiments/e17/` once the full migration gate is closed.
- The existing `docs/versions/` and `docs/prompts/` directories still carry a large number of historical documents. They remain historically important but are outside the scope of the current Copilot-only preflight.

## Non-controversial action plan for the Copilot-owned subset

1. Keep the active model spec under `docs/model/model_specs/copilot/` with no semantic changes.
2. Move the Copilot E17 report and review into `experiments/e17/reports/copilot/` and `experiments/e17/reviews/copilot/`.
3. Move the machine-readable metrics into `experiments/e17/artifacts/derived/copilot/`.
4. Move the round-local extractor into `experiments/e17/tools/copilot/`.
5. Move the common E17 prompt and strategy draft into `experiments/e17/prompts/common/` and `experiments/e17/design/` once the common migration manifest is reconciled.

## Gate status

```text
REPOSITORY_PRECHECK: PASS
THREE_AGENT_INVENTORIES_AVAILABLE: NO
FULL_RECONCILIATION: NO
E17_LAUNCH: BLOCKED
COMMON_REPOSITORY_REORGANIZATION_GATES: A0-A1 PARTIAL ONLY
```

## Rationale

The template requires `MIGRATION_INVENTORY_<AGENT_ID>.csv` and a common reconciliation manifest. Those artifacts are now created for the Copilot-owned subset, but the repository-level gate cannot be declared complete until Codex has reconciled the three inventories and there are zero unresolved blockers.

This is the correct operational status: preserve the user-owned and historical files, keep the current truthful Copilot derivative documentation, and stop before E17 launch until the migration gates are closed.
