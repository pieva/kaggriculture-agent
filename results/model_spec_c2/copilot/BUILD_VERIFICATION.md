# BUILD_VERIFICATION — COPILOT C2

```text
AGENT_ID: COPILOT
MODEL_SPEC path: docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md
candidate executable path: src/agricola/strategy/copilot/c2_policy.py
configuration path: src/agricola/strategy/copilot/c2_config.py
entrypoint path: src/agricola/strategy/copilot/agent_c2.py
tests added/changed: tests/test_copilot_c2.py
```

## Verifica eseguita

- pytest: PASS (`tests/test_copilot_c2.py`)
- git diff --check: PASS
- smoke execution: PASS

## Known limitations

- la policy è intenzionalmente preventiva e non ottimizza la totalità del mercato o dell'espansione di superficie;
- il modello è dedicato alla riduzione del failure pattern E16 e non alla massimizzazione assoluta del denaro in tutte le fasi;
- `livestock` e `market` restano non prioritari in questa versione, coerenti con il principio di minimal causal intervention.

```text
TOURNAMENT_READY: YES
```
