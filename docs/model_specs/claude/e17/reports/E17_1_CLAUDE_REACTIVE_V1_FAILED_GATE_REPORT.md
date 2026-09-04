# E17.1 Claude Reactive V1 — failed-gate report

- **Data:** 2026-09-02
- **Policy:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V1`
- **Verdetto:** REJECTED BEFORE TOURNAMENT
- **Epistemic role:** DEVELOPMENT ONLY
- **Holdout / final confirmation:** NOT CONSUMED / NOT CONSUMED

## Sintesi

La V1 è una policy nativa e reattiva, supera l'audit di indipendenza, produce
batch validi e attiva Q0/Q1/Q2 in tutte le 14 run. Non supera però i gate
economico e di sicurezza animale.

```text
RUNS: 14
FINAL_MONEY_MEAN: 9201.7143
FINAL_MONEY_MEDIAN: 9126
FINAL_MONEY_MIN: 5415
FINAL_MONEY_MAX: 13625
TARGET: >= 50000
DERIVED_EOD_ESCAPES: 8
TECHNICAL_ERRORS: 0
INVALID_BATCHES: 0
LEDGER_RECORD_COVERAGE: 100%
THREE_QUADRANTS_ALL_RUNS: PASS
STATE_REACTIVITY: PASS
INDEPENDENCE: PASS
```

## Diagnosi iniziale

Nel primo run sono richiesti 3.369 movimenti (`EAST/NORTH/SOUTH/WEST`) contro
621 comandi produttivi fra `DIG`, `PLANT`, `WATER`, `HARVEST` e costruzioni.
Il rapporto grezzo MOVE/produttive è quindi circa 5,42. Nello stesso episodio
si osservano 156 richieste `HIRE`, a fronte del tetto configurato di sei hands:
il controller ritenta frequentemente ordini che non convertono risorse.

Questi dati indicano tre gap da verificare causalmente sulla sola V1:

1. dispatch stateless con oscillazioni e target che cambiano a ogni turno;
2. espansione 3Q prima che Q0 abbia capacità economica sufficiente;
3. serviceability animale incompleta, confermata dalle otto fughe.

La diagnosi non autorizza a importare routine o planner Codex. V2 deve restare
strategicamente indipendente e può utilizzare soltanto Foundation, fatti
engine, osservazioni, ledger V1 e seed development.

## Decisione

Il manifest `FROZEN_WITH_FAILED_GATES` conserva il tentativo, ma non equivale
a un freeze di ammissione. La V1 non partecipa al torneo. È autorizzata una V2
su nuovi path, con nuovi source/config hash e con lo stesso protocollo di test.
