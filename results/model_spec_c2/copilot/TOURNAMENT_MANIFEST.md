# TOURNAMENT_MANIFEST — COPILOT C2

```text
AGENT_ID: COPILOT
FOUNDATION_CHECKPOINT: f391ee2
MODEL_SPEC: docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md
CANDIDATE ENTRYPOINT: agricola.strategy.copilot.agent_c2.CopilotC2Agent
CANDIDATE MODULES:
  src/agricola/strategy/copilot/agent_c2.py
  src/agricola/strategy/copilot/c2_policy.py
  src/agricola/strategy/copilot/c2_config.py
TESTS: tests/test_copilot_c2.py
BUILD_VERDICT: BUILD_READY (results/model_spec_c2/copilot/BUILD_VERIFICATION.md)
```

## Package identity

Il candidato è invocabile tramite `CopilotC2Agent()(observation, configuration)` e
tramite `.act(state)` / `.decide(state)` per compatibilità con lo state wrapper
`agricola.core.state.GameState`. Non ha dipendenze da moduli o artefatti di altri
agenti. Legge `observation.player` per il binding P0/P1 e non presuppone la seat.

## Readiness tecnica osservata

- test mirati e suite Copilot: PASS;
- compilazione: PASS;
- real-engine preflight P0/P1 (288 step, opponent inerte, seed 1113294977):
  risultati identici in entrambe le seat, `DONE`, 25 tile PLANT attive, capitale
  `$3,000 -> $4,215`.

Questo manifest descrive esclusivamente la readiness tecnica dell'artefatto.

## Aggiornamento — performance correction pass

Una verifica economica full-episode (720 step) successiva ha applicato
correzioni evidence-based (crop mix, workforce co-scaling, endgame cutoff;
dettaglio in `MODEL_SPEC_COPILOT_C2.md` Sezione 24 e
`BUILD_VERIFICATION.md`). Risultato: `mean_final_money = $28,909.00` (3 seed
canonici, P0/P1), ancora sotto il gate economico di $50,000
(`PERFORMANCE_FAILURE` per il gate stretto), nonostante un miglioramento di
+206.8% rispetto al baseline pre-correzione ($9,422.67). Questo aggiornamento
non modifica la readiness tecnica sopra descritta né apre alcun gate di
autorizzazione.

```text
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

La presenza di questo manifest non apre alcun gate di autorizzazione. L'autorizzazione
al tournament comune a tre agenti resta subordinata a un gate di governance separato
(`THREE_AGENT_BUILD_RECONCILIATION`), non ancora concesso.
