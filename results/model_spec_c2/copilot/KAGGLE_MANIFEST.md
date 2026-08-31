# KAGGLE_MANIFEST — COPILOT C2

```text
AGENT_ID: COPILOT
FOUNDATION_CHECKPOINT: f391ee2
MODEL_SPEC: docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md
BUILD_VERDICT: BUILD_READY
```

## Packaging compatibility

Il candidato `CopilotC2Agent` (in `src/agricola/strategy/copilot/`) è costituito da
tre moduli puri Python senza dipendenze esterne oltre `agricola.core.state.CROPS`,
compatibili con l'inclusione statica in un unico file di submission Kaggle secondo
lo stesso schema già usato da `scripts/build_submission_codex.py` (concatenazione di
codice comune + config + policy + agent + `create_agent()`), non eseguito in questo
task.

Verifiche tecniche eseguite (senza generare né inviare submission):

- `python -m py_compile` su tutti i moduli del candidato: PASS;
- entrypoint compatibile con la firma richiesta da `kaggle_environments`
  (`__call__(self, obs, configuration=None)`), verificato con
  `kaggle_environments.make("kaggriculture", ...)` in P0 e P1 reali;
- nessuna dipendenza da moduli o artefatti degli altri agenti.

## Cosa NON è stato fatto

- Nessuna submission è stata generata o inviata;
- nessuna automazione browser Kaggle è stata utilizzata;
- nessuna submission esistente è stata cancellata, sostituita o interpretata;
- il leaderboard non è stato consultato.

```text
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
