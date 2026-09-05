# E17.1 Codex reattivo — implementazione, calibrazione e freeze

- **Data:** 2026-09-02
- **Candidato:** `CODEX-E17.1-3Q-REACTIVE-GUARDED-V1`
- **Baseline:** `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY`
- **Verdetto development:** PASS
- **Stato:** FROZEN FOR REACTIVE TOURNAMENT
- **Holdout / final confirmation consumati:** NO / NO

## Risultato

Il candidato Codex reattivo è ammesso al torneo. Mantiene esattamente la
performance V9 nella matrice development inerte e reagisce nei test costruiti
a due perturbazioni: mancato acquisto Wheat e rischio di fuga EOD non coperto.
Non è ancora dimostrato un vantaggio competitivo.

| Metrica | Codex V9 | Codex reattivo |
|---|---:|---:|
| run | 14 | 14 |
| final money medio | 139.420,29 | 139.420,29 |
| mediana | — | 148.216 |
| minimo | — | 77.542 |
| massimo | — | 181.339 |
| delta medio | riferimento | 0 |
| errori tecnici | 0 | 0 |
| fallback | 0 | 0 |
| fughe derivate | 0 | 0 |
| attivazione 3Q | 14/14 | 14/14 |
| copertura ledger | — | 100% |
| override naturali contro inert | — | 0 |

Nel mirror development Codex reattivo vs V9, su sette seed e seat scambiati:

```text
RUNS: 14
REACTIVE_MEAN: 88576.2857
V9_MEAN: 88576.2857
MEAN_MATCHED_DELTA: 0
W/T/L: 1/12/1
NATURAL_OVERRIDES: 0
DETECTED_UNFILLED_WHEAT: 0
TECHNICAL_ERRORS: 0
DERIVED_ESCAPES: 0
```

La coppia vittoria/sconfitta è un unico seat effect simmetrico di `+68/-68`,
non un effetto della policy. Il mirror non dimostra quindi valore aggiunto,
ma esclude un costo nascosto nel confronto competitivo omologo.

## Calibrazione causale

Una prima guardia più ampia proteggeva continuamente una riserva Wheat e
anticipava `FEED`. Nella matrice development ha prodotto:

```text
REACTIVE_MEAN: 136440.57
V9_MEAN: 139420.29
MEAN_DELTA: -2979.71
OVERRIDE_BATCHES: 140
DERIVED_ESCAPES: 0
```

La causa osservata era l'interferenza con vendite e azioni `CARE` che la V9
recuperava correttamente più avanti. Questa variante è stata respinta prima
del freeze. Non viene promossa come risultato positivo e i numeri restano
evidenza di development, non holdout.

La versione congelata restringe l'attivazione a:

1. fill shortfall Wheat derivato conservativamente dallo stato successivo;
2. ultimo turno della giornata con animale critico non già coperto da `FEED`.

Il passaggio da -2.979,71 a parità non prova un miglioramento rispetto alla
V9: prova soltanto che sono stati rimossi gli override spuri osservati contro
l'avversario inerte.

## Test eseguiti

```text
pytest reactive + V9: 7 passed
compileall source + runner: PASS
development seeds: 7/7
seat: 0 e 1
episode per policy: 720 step
holdout in runner development: hard-forbidden
```

I test di reattività verificano che:

- uno stato sicuro emetta lo stesso batch della V9;
- un acquisto Wheat non riempito modifichi il batch seguente;
- a parità di step, uno stato EOD critico possa produrre `FEED` mentre quello
  sicuro conserva la V9;
- la policy sia fail-closed senza errori nello smoke test del motore.

## Artefatti

- source: `src/agricola/strategy/codex/codex_e17_reactive_guarded.py`;
- config: `docs/model_specs/codex/e17/configs/CODEX_E17_1_3Q_REACTIVE_GUARDED_V1.json`;
- MODEL_SPEC: `docs/model_specs/codex/e17/MODEL_SPEC_CODEX_E17_1_3Q_REACTIVE_GUARDED.md`;
- test: `docs/model_specs/codex/e17/tests/test_codex_e17_1_reactive.py`;
- runner: `docs/model_specs/codex/e17/tools/run_codex_e17_1_development.py`;
- metrics: `docs/model_specs/codex/e17/artifacts/derived/E17_1_DEVELOPMENT_METRICS.json`;
- mirror: `docs/model_specs/codex/e17/artifacts/derived/E17_1_COMPETITIVE_DEVELOPMENT_METRICS.json`;
- freeze: `docs/model_specs/codex/e17/artifacts/freeze/e17_1/E17_1_FREEZE_MANIFEST.json`;
- run artifacts: `docs/model_specs/codex/e17/artifacts/runs/e17_1_development/`.

## Hash congelati

```text
SOURCE_SHA256: 4B9F1FE9BD839F284D25030B39292CEF77F9195C6CA29711CF908EE5D2968607
CONFIG_SHA256: 5B4D4B24C4791E42A08937F9CCD7F7BCE5B4B05BA960E7FE8F066DA4C6BED5A0
DEVELOPMENT_METRICS_SHA256: 020648595C8C69698B0FF20B20774183D0C43680349D9FB38CD490E6384C1C6D
```

## Stop boundary

Il candidato è congelato. Non sono stati eseguiti torneo holdout, conferma
finale, modifica della submission, upload Kaggle, commit o push. Il torneo può
iniziare soltanto dopo il freeze verificato del candidato Claude.
