# BUILD_VERIFICATION — COPILOT C2

```text
AGENT_ID: COPILOT
MODEL_SPEC path: docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md
candidate executable path: src/agricola/strategy/copilot/c2_policy.py
configuration path: src/agricola/strategy/copilot/c2_config.py
entrypoint path: src/agricola/strategy/copilot/agent_c2.py
tests added/changed: tests/test_copilot_c2.py
```

## Verifica eseguita dopo remediation

- pytest mirato: PASS (`tests/test_copilot_c2.py`, 7 passed);
- pytest completo: 164 passed, 8 failed, tutti in `tests/test_codex_c2_candidate.py` e
  relativi a modifiche concorrenti del candidato Codex; nessun test Copilot fallito;
- compilazione: PASS (`python -m py_compile src/agricola/strategy/copilot/c2_policy.py src/agricola/strategy/copilot/agent_c2.py`);
- `git diff --check`: PASS;
- real-engine preflight: PASS in P0 e P1, 144 step contro `starter`, seed `1113294977`.

Il preflight ha osservato in entrambe le seat: `DONE`, 4 posizioni uniche, 24 MOVE,
12 PLANT, 24 WATER, 8 HARVEST, 9 `BUY_SEED`, 2 `SELL`, massimo 4 tile PLANT,
massimo 4 unità crop nello shed e capitale finale `$3,083` da `$3,000`.

## Limiti noti

- la policy è intenzionalmente preventiva e non ottimizza la totalità del mercato o dell'espansione di superficie;
- il modello è dedicato alla riduzione del failure pattern E16 e non alla massimizzazione assoluta del denaro in tutte le fasi;
- `livestock`, market timing ed espansione restano non prioritari; il mercato è usato soltanto per bootstrap dei semi e vendita crop.

```text
TOURNAMENT_READY: YES
```
