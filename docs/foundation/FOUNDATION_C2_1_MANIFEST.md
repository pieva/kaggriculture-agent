# Model Foundation C2.1 — Manifest corrente

## ACTIVE / RECONCILED

| Layer | File | SHA-256 |
|---|---|---|
| Ontology | `ontology/ONTOLOGY_C2_1.md` | `10C910388EE4DED8D99B5A5530035D26B336EDE2E4D8EB02026C3599C4566778` |
| Environment State Machine | `state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md` | `5E4056555315AB23B80038DB96889EA1F659E1B6FC74B9047BF004A6F572676E` |
| Feature Model | `feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md` | `4FCBBDEC664BD25217A3F2EB8B76142E95E4335AD98947A33D60C326A4F0A3CA` |
| Observation Contract runtime | `../../src/agricola/core/observation_contract.py` | `3E7509888B09103C79B86FD058984651337CBFC32AB60CD934E6351A4F2A81A9` |

Engine aggregate fingerprint:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

## REVIEW & RECONCILIATION EVIDENCE

- `../governance/history/model_spec_c2/foundation_revision/C2_1_POST_3Q_FOUNDATION_RECONCILIATION.md`;
- `../governance/history/model_spec_c2/foundation_revision_feedback/ANTIGRAVITY_C2_1_POST_3Q_FOUNDATION_REVIEW.md`;
- `../governance/history/model_spec_c2/foundation_revision_feedback/COPILOT_C2_1_POST_3Q_FOUNDATION_REVIEW.md`.

## HISTORICAL / FROZEN

- `ontology/ONTOLOGY_C2.md`;
- `state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`;
- `feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`.

Le baseline C2 non vanno cancellate: servono come confronto frozen e audit trail.

## Contratto osservativo runtime

Clock, snapshot, hashing e normalizzazione sono isolati in `src/agricola/core/observation_contract.py`. La Foundation non contiene una macchina di deliberazione condivisa: planner, priorità, working set e routine sono agent-local.

## Regola di indipendenza

I tre agenti condividono Foundation, engine facts, schema di telemetria e protocolli. Non condividono routine, action table, planner, dispatcher o schedule. Un modello che importa una routine altrui è una baseline derivativa, anche se cambia namespace, config o liquidazione terminale.

## Prossimo lavoro

La revisione Foundation post-3Q è chiusa. La sequenza sperimentale riprende dal primo esperimento successivo a E16, normalmente E17.
