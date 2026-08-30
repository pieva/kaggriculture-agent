# C2 — Frozen retournament protocol

```text
PROTOCOL_ID: MODEL_SPEC_C2_RETOURNAMENT_FROZEN_V2
STATUS: EXECUTED AS PREREGISTERED
EPISODES: 9
EPISODE_STEPS: 720
MIRRORING: NO
PRIMARY_METRIC: final_money
```

## Candidate congelati

| Candidate | Entrypoint | SHA-256 eseguibile |
|---|---|---|
| Antigravity C2 | `src/agricola/strategy/antigravity/agent_c2.py` | `da37cdb20660c369905c9b833bc31cad438d2b866efcfd418bb8d628184219a1` |
| Codex C2 | `src/agricola/strategy/codex_c2.py` | `9d67aa44b6dae89a2a05619a77b280e3a6d8b6abcb8a6c67a3f3714921d2bc3a` |
| Copilot C2 | `src/agricola/strategy/copilot/agent_c2.py` | `1c24af2fa5a9d068e45dab457a05bc2ab73551d1fe4f6f0b34cb186dc6b4256d` |

Nessun MODEL_SPEC, policy, config o test è stato modificato durante la fase.

## Matrice preregistrata

Shared seed, in ordine:

```text
1113294977
3033283457
1678077158
```

| Round | P0 | P1 | Episodi |
|---|---|---|---:|
| R1 | Antigravity C2 | Codex C2 | 3 |
| R2 | Antigravity C2 | Copilot C2 | 3 |
| R3 | Codex C2 | Copilot C2 | 3 |

Totale: 3 matchup × 3 seed = 9 episodi, 6.480 frame engine. Non sono
state aggiunte seed e non è stato introdotto mirroring.

## Runner e neutralità

Il runner precedente è stato riutilizzato. Le sole modifiche di fase sono:

- destinazione parametrica degli output nella directory `retournament`;
- deviazione standard campionaria con `ddof=1`;
- post-processing dei replay per le metriche mancanti.

Queste modifiche non alterano istanziazione, osservazioni, action, ordine dei
player, seed o configurazione engine.

```text
RUNNER_SHA256: 8eec39f5e8668253d33186ec0ff787994af067ba7578c06fbbf21060f34ece2d
ANALYZER_SHA256: 2882ac8af7b71b7425cf8b7032a55307e42cd93b5b63c5511a57b9e03d842a5c
```

## Tassonomia della telemetria

Le metriche sono separate in tre piani:

1. `ACTION DISPATCH`: opcode restituiti dalla candidate;
2. `STATE TRANSITION`: cambiamenti osservati nel frame successivo coerenti con
   l'opcode, per esempio incremento superficie dopo PLANT;
3. `ECONOMIC EFFECT`: cassa, vendita realizzata e primo revenue step.

Un opcode da solo non è contato come realization. Gli effetti sono allineati
all'action registrata nel frame corrente e alla differenza rispetto al frame
precedente.

Sono raccolti per episodio:

- status, completion, error/fallback e audit di riproduzione action;
- final/min cash e first revenue step;
- active surface mean/max/final;
- PLANT/WATER/HARVEST/DIG/MOVE dispatch ed effetti;
- market total, BUY_SEED/SELL/BUY_LAND/HIRE dispatch ed effetti;
- quadranti e workforce effettiva.

## Artifact

```text
results/model_spec_c2/retournament/INTEGRATED_READINESS.md
results/model_spec_c2/retournament/RETournament_PROTOCOL.md
results/model_spec_c2/retournament/RETournament_SUMMARY.md
results/model_spec_c2/retournament/aggregated_results.json
results/model_spec_c2/retournament/aggregated_results.csv
results/model_spec_c2/retournament/raw/<9 match>/summary.json
results/model_spec_c2/retournament/raw/<9 match>/replay.json
```

Nessuna submission Kaggle fa parte del protocollo.
