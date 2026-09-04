# E17.0 Codex — implementazione ledger e measurement parity

- **Data:** 2026-09-02
- **Agente:** Codex
- **Baseline:** `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY`
- **Verdetto:** `PASS`
- **Policy mutation:** `NO`
- **Holdout/final confirmation consumati:** `NO / NO`

## Implementazione

È stato aggiunto il ledger neutrale `E17_LEDGER_V1` in
`src/agricola/core/e17_ledger.py`. Il wrapper invoca prima la policy, registra
poi una copia profonda dell'azione e non rende la telemetria accessibile al
decision path. Un errore del ledger non può sostituire l'azione della policy;
nel test eseguito gli errori sono zero.

Il ledger produce un record per ogni comando emesso, incluso `PASS`, con
identità deterministica, batch hash, stato pre/post, cash, inventory, asset,
outcome e provenance. La classificazione è conservativa: ordini di mercato
con delta condiviso fra più richieste restano `UNKNOWN`.

## Matrice eseguita

Sono stati usati esclusivamente i tre seed development frozen, entrambi i
seat, contro `INERT_PASS_POLICY`. Per ciascuna cella sono stati eseguiti un
episodio V9 non strumentato e uno strumentato sullo stesso seed/seat/opponent.

| Seed | Seat | Reward baseline | Reward ledger | Azioni | Parità outcome |
|---:|---:|---:|---:|---:|---|
| 26090101 | 0 | 181.339 | 181.339 | 719/719 | PASS |
| 26090101 | 1 | 181.339 | 181.339 | 719/719 | PASS |
| 26090102 | 0 | 119.676 | 119.676 | 719/719 | PASS |
| 26090102 | 1 | 119.676 | 119.676 | 719/719 | PASS |
| 26090103 | 0 | 77.542 | 77.542 | 719/719 | PASS |
| 26090103 | 1 | 112.544 | 112.544 | 719/719 | PASS |

```text
ACTION_PARITY: 4314/4314 PASS
ACTION_SEQUENCE_SHA256: B6E0C7A679645ACD0DBD17BFDE5CA822EA88F783FAFCAB8F18A960AF3F262822
OUTCOME_PARITY: 6/6 PASS
TERMINAL_STATE_PARITY: 6/6 PASS
TECHNICAL_ERRORS: 0
FALLBACK_DELTA: 0
DERIVED_EOD_ESCAPE_COUNT: 0
```

L'action-sequence hash include la patch V9 allo step 195; il parent routine
hash congelato resta
`C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4`.

## Copertura ledger

```text
ACTION_BATCHES: 4314
LEDGER_RECORDS: 51834
LEDGER_RECORD_COVERAGE: 100%
OUTCOME_EXECUTED: 43190
OUTCOME_NOT_EXECUTED: 2452
OUTCOME_UNKNOWN: 6192
MARKET_RECORDS: 6726
MARKET_EXECUTED: 1267
MARKET_NOT_EXECUTED: 5
MARKET_UNKNOWN: 5454
MARKET_CLASSIFIED_OUTCOME_COVERAGE: 18.9116859946476%
```

La bassa quota di classificazione market non è un errore di copertura: tutti
gli ordini hanno un record, ma un delta aggregato non permette di attribuire
con certezza l'esito a più ordini simultanei. Gli `UNKNOWN` non sono stati
convertiti. Per E17.1 servirà un evento engine correlabile se si vuole portare
la classification coverage al 100% senza falsi positivi.

## Freeze e provenance

```text
CODEX_SOURCE_SHA256: 4D99C919B59DAE9B307C403FCF3198763B08FB9D15324AB8C937C4FC2B32090E
CODEX_CONFIG_SHA256: 44DD0EC2F33C9EEEE74AE5676580DC833325AB969D8A9D262EC870FEAAAC6C99
SUBMISSION_SHA256: AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421
LEDGER_SOURCE_SHA256: A22C97584D4AE81A341485744C8AF0FFBBF14A9C9A8491BD3210FC768AD672C9
RUNNER_SHA256: 1D629D48C94459C5F360E0C28CB6E6F82D6B5D7DE248A7BBCD1F09BD8F34E1F9
```

Artefatti:

- `docs/model_specs/codex/e17/artifacts/derived/E17_0_METRICS.json`;
- `docs/model_specs/codex/e17/artifacts/freeze/E17_0_FREEZE_MANIFEST.json`;
- `docs/model_specs/codex/e17/artifacts/runs/e17_0/`.

## Gate Codex E17.0

```text
ACTION_PARITY: PASS
LEDGER_RECORD_COVERAGE: PASS
MARKET_OUTCOME_COVERAGE: DECLARED_WITH_UNKNOWN
TECHNICAL_ERRORS: PASS
FALLBACK_DELTA: PASS
ANIMAL_ESCAPE_LEDGER: AUDITABLE / ZERO_OBSERVED
SOURCE_CONFIG_FREEZE: PASS
STRATEGIC_INDEPENDENCE_GATE: PASS (Codex baseline owner)
E17_0_STATUS: PASS
```

Non sono stati eseguiti guardia WHEAT, timing D10/D8, nuove topologie,
diversificazione, torneo, submission Kaggle, commit o push.
