# Model Foundation C2.1 — Manifest corrente

## ACTIVE / RECONCILED

| Layer | File | SHA-256 |
|---|---|---|
| Ontology | `ontology/ONTOLOGY_C2_1.md` | `F9A44BD57511C062EC03E6D8493E4CF4A76C0BA321E2A1EFDBAFF6B0AEC9D2BD` |
| Environment State Machine | `state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md` | `26E901DB33FC5F138ACC7807AB4970F2200C1B178967858E21980C69A63BF3C3` |
| Feature Model | `feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md` | `9AF8D3043DC82D9F1D0C97F21311407ADA0D012854ABED7536930621473E4470` |
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

La baseline post-3Q resta riconciliata. Stato operativo al 2026-09-08: V48 pubblicata; prossima versione 770 dedicata ai PASS evitabili. Gli hash sopra includono il supplemento operativo del 8 settembre, non attestano una nuova revisione incrociata.


## Checkpoint operativo 2026-09-08: V48 e PASS

Catena completa e protocollo: [V48 e priorità PASS](V48_PLANNING_AND_BUILD_IT.md). Le baseline C1/C2 e i verbali storici rimangono congelati.
