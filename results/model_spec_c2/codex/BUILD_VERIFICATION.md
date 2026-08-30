# Codex C2 Build Verification

```text
AGENT_ID: CODEX
BUILD_ID: CODEX-C2-STAGGERED-HARVEST-SERVICE-V4
MODEL_SPEC_BUILD_ALIGNED: YES
REAL_ENGINE_P0_P1_EXECUTION: PASS
PREREGISTERED_MECHANISM_GATE: PASS
COMPARATIVE_TOURNAMENT: NOT EXECUTED
```

## Artefatti

```text
MODEL_SPEC: docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md
CANDIDATE: src/agricola/strategy/codex_c2.py
CONFIG: configs/model_spec_c2/CODEX_C2_CONFIG.json
TESTS: tests/test_codex_c2_candidate.py
PREFLIGHT_RUNNER: scripts/preflight_codex_c2.py
PREFLIGHT: results/model_spec_c2/performance_iteration/CODEX_C2_V4_PREFLIGHT.json
REPORT: results/model_spec_c2/performance_iteration/CODEX_C2_PERFORMANCE_ITERATION_V4.md
```

## Verifiche

| Check | Risultato |
|---|---|
| Candidate tests | PASS: 24 passed |
| Repository pytest | PASS: 182 passed |
| Targeted Ruff | PASS |
| `git diff --check` | PASS |
| Real-engine P0/P1 | PASS: DONE, 360 step, error/fallback 0/0 |
| Max WHEAT cohort | PASS: 2 / 2 |
| Peak simultaneous ready | PASS: 2 / 2 |
| Deadline miss | PASS: 0/15 / 0/15 |
| WHEAT HARVEST yield>=3 | PASS: 15/15 / 15/15 |
| MELON cycle | PASS: HARVEST e SELL effettivi P0/P1 |

Il VERIFY dimostra il meccanismo di load shaping, non il target economico del
prossimo torneo. Nessun torneo comune, seed ufficiale o invio Kaggle è stato
eseguito.

```text
TOURNAMENT_READY: YES
TOURNAMENT_EXECUTED: NO
```
