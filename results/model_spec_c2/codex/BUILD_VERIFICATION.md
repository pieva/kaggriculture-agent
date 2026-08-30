# Codex C2 Build Verification

```text
AGENT_ID: CODEX
BUILD_ID: CODEX-C2-LIFECYCLE-REALIZATION-V1
MODEL_SPEC_C2_UPSTREAM_READY: YES
FOUNDATION_C2: NOT FROZEN
```

## Artefatti

```text
MODEL_SPEC:
docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md

CANDIDATE_EXECUTABLE:
src/agricola/strategy/codex_c2.py

CONFIGURATION:
configs/model_spec_c2/CODEX_C2_CONFIG.json

CONSUMER_MAPPING:
EMBEDDED in MODEL_SPEC section 5

TESTS_ADDED:
tests/test_codex_c2_candidate.py
```

## Verifiche

| Check | Risultato |
|---|---|
| Candidate tests | PASS: 15 passed |
| Baseline + Codex, esclusi i namespace C2 concorrenti | PASS: 158 passed |
| Repository `pytest` non filtrato | PASS: 168 passed |
| Candidate targeted ruff | PASS |
| `git diff --check` | PASS |
| Deterministic engine smoke | PASS: 48 steps, entrambi gli agenti `DONE` |

Lo smoke è stato usato soltanto per caricamento, schema azioni e compatibilità engine. Reward e money non sono stati usati per tuning o revisione ex post del MODEL_SPEC.

## Meccanismi verificati

- HARVEST prematuro rifiutato e HARVEST maturo accettato.
- HARVEST ongoing intermedio riclassificato `GROWING`.
- Yield finale ongoing con readiness mantiene precedenza su retirement.
- Post-final-HARVEST ongoing classificato `RETIREMENT_DUE` e servito con DIG preventivo.
- `max_lifespan_step` da solo non ritira una crop non-ongoing.
- `LOST_WEED` genera DIG recovery.
- EMPTY genera PLANT soltanto con una fase successiva disponibile per WATER.
- WATER critico precede recovery; HARVEST in decay window precede WATER sulla stessa tile.
- Diagnostica crop invalida blocca HARVEST e DIG distruttivi.
- Factory `create_agent` è importabile e fail-closed.

## Limitazioni note

- Il routing nearest-task e i controlli workforce/market/livestock sono deliberatamente invariati e possono restare colli di bottiglia.
- Il gate PLANT garantisce disponibilità temporale, non serviceability futura del worker.
- La persistence full-board di LOST_WEED richiede telemetry più completa per una misura non censurata.
- Il target 17 è una candidate operating region configurabile, non un optimum.
- Nessun torneo comparativo, submission Kaggle o review post-torneo è stato eseguito.

```text
TOURNAMENT_READY: YES
```
