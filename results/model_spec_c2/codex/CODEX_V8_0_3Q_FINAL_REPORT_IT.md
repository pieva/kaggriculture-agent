# Codex V8.0 3Q — report finale di sviluppo e verifica

## Esito

La V8.0 3Q è stata implementata e verificata, ma **non raggiunge i target economici** e non è stata promossa come submission. Il protocollo canonico a sei episodi è tecnicamente valido; quando il gate ammette Q2, tuttavia, il satellite sottrae serviceability al nucleo Q0/Q1 e distrugge valore.

La migliore versione Codex promuovibile resta la V7.3 Dual-Q1 Cadence:

```text
V7.3 FINAL_MONEY_MEAN: 78036.17
V7.3 FINAL_MONEY_MIN: 71771.00
V7.3 ANIMAL_ESCAPES_TOTAL: 0
```

## Protocollo canonico

La verifica finale ha usato, senza selezione post-hoc:

```text
SEEDS: 26090101, 26090102, 26090103
SEATS: 0, 1
OPPONENT: INERT_PASS_POLICY
EPISODE_STEPS: 720
TURNS_PER_DAY: 24
EPISODES: 6
```

Gli artefatti numerici riproducibili sono `CODEX_V8_0_3Q_RESULTS.csv` e `CODEX_V8_0_3Q_RESULTS.json`.

## Sviluppo e iterazioni causali

### 1. Q2 crop-only: 12 MELON e una hand

Sul replay diagnostico seed 26090101, seat 0:

```text
V7.3: 88397
3Q CROP-ONLY: 83046
DELTA: -5351
Q2 MELON: 31
ANIMAL_ESCAPES: 0
PREZZO MELON TERMINALE: 10
```

La produzione Q2 aggiunge offerta al prodotto già dominante di Q0/Q1. Terra, seed e salario non vengono recuperati; il ciclo è stato respinto per cannibalizzazione.

### 2. Q2 livestock 6+6 con una hand

Il ledger include terra, 6 COW, 6 SHEEP, feed e salario marginale. Il netto proiettato resta tra 7.524 e 9.142, sotto il floor di 12.000; il gate respinge correttamente la variante prima dell'acquisto.

### 3. Q2 livestock e verifiche di capacità

Sono state provate, senza promozione:

- 6 COW + 6 SHEEP su W6/W12 senza nuove hands;
- una hand dedicata COW con W12 su SHEEP;
- due hands dedicate;
- FEED Q2 alternato sul contatore osservabile `consecutive_unfed`;
- sottocluster da tre animali e accesso shed `(4, 5)`;
- replay conclusivo a quattro sottocluster su W0, W6, W9 e W12, senza costo salariale incrementale.

La migliore configurazione canonica intermedia ha raggiunto una media di 68.889,17, ancora 9.147 sotto la V7.3. La configurazione conclusiva ripristina il floor economico obbligatorio di 12.000: Q2 viene ammesso in tre episodi su sei; negli altri tre il comportamento e il punteggio restano esattamente quelli della V7.3 appaiata. Tutti gli episodi che attivano Q2 peggiorano.

## Risultati canonici conclusivi

```text
FINAL_MONEY_MEAN: 65218.83
FINAL_MONEY_MEDIAN: 64638.50
FINAL_MONEY_MIN: 54089.00
FINAL_MONEY_MAX: 76183.00
DELTA_VS_V7_3: -12817.33
Q2_OBSERVED_NET_CONTRIBUTION_MEAN: -12817.33
Q2_ACTIVATED_EPISODES: 3/6
Q2_ACTIVATION_DAY_MEAN: 11.00
Q2_FULL_MODULE_DAY_MEAN: 23.67
Q2_FIRST_OUTPUT_DAY_MEAN: 19.67
Q2_MAX_ACTIVE_ANIMALS_MEAN: 6.00
Q2_MILK_UNITS_MEAN: 5.33
Q2_WOOL_UNITS_MEAN: 4.50
Q0_CROP_UNITS_MEAN: 121.83
Q1_CROP_UNITS_MEAN: 74.17
Q0_CROP_REGRESSION: 11.18%
Q1_CROP_REGRESSION: 13.59%
ANIMAL_ESCAPES_TOTAL: 23
MOVE_PER_PRODUCTIVE_ACTION: 3.1108
TECHNICAL_PASS: YES
MINIMUM_GATE_PASS: NO
CENTRAL_GATE_PASS: NO
```

La coincidenza esatta con V7.3 nei tre episodi non ammessi isola l'effetto causale: la regressione non è prodotta dalla semplice presenza del controller V8, ma dall'attivazione economico-operativa del terzo modulo.

## Perché il target 90k non è raggiungibile con questa estensione

Il target richiede almeno +11.963,83 sulla media V7.3. Q2 arriva con circa 18 giorni utili e incontra tre vincoli simultanei:

1. il MELON addizionale cannibalizza un mercato già saturo;
2. il livestock senza nuove hands sottrae azioni di feed, care, raccolta e logistica al nucleo;
3. le hands aggiuntive hanno costo Fibonacci: dopo le dodici hands V7.3, la tredicesima costa 233 al giorno e la quattordicesima 377; sei hands ulteriori porterebbero la spesa giornaliera complessiva a 6.764.

La copia nominale di Q0/Q1 in Q2 non è quindi finanziariamente equivalente: l'engine rende la capacità marginale molto più costosa. Nessuna variante osservata soddisfa insieme payback ≥12k, zero fughe e regressione crop ≤3%.

## Test e qualità

```text
TEST MIRATI V8.0: 3 passed
RUFF V8.0: passed
REGRESSION SUITE REPOSITORY: 214 passed
ERRORI TECNICI NEI 6 REPLAY: 0
FALLBACK NEI 6 REPLAY: 0
```

L'avviso `PytestCacheWarning` riguarda soltanto i permessi della cache `.pytest_cache` e non l'esecuzione dei test.

## Decisione sulla submission

Poiché la V8.0 non supera i gate, non è corretto produrre una submission V8. Il file canonico `submission/submission_codex.py` contiene invece la migliore V7.3 standalone, verificata con parità esatta su 6 × 719 decisioni e SHA-256:

```text
EB5EB01D04201C084B87747BBB57B38ABB9D9C04580D92AA8C19E88A50CC89F5
```

Nella cartella `submission` resta un solo file corrispondente a `submission_codex*.py`; le submission non Codex non sono state modificate o eliminate da questa operazione.

## Blocco finale

```text
CANDIDATE_VERSION: CODEX-C2-V8.0-3Q-ELASTIC-SATELLITE
Q0_Q1_CORE_PRESERVED: NO
Q2_ACTIVATION_DAY_MEAN: 11.00
Q2_FULL_MODULE_DAY_MEAN: 23.67
Q2_FIRST_OUTPUT_DAY_MEAN: 19.67
FINAL_MONEY_MEAN: 65218.83
FINAL_MONEY_MEDIAN: 64638.50
FINAL_MONEY_MIN: 54089.00
FINAL_MONEY_MAX: 76183.00
DELTA_VS_V7_3: -12817.33
Q2_NET_CONTRIBUTION: -12817.33
Q0_CROP_UNITS_MEAN: 121.83
Q1_CROP_UNITS_MEAN: 74.17
Q2_CROP_UNITS_MEAN: 0.00
ANIMAL_ESCAPES_TOTAL: 23
MOVE_PER_PRODUCTIVE_ACTION: 3.1108
OBJECTIVE_88000_REACHED: NO
OBJECTIVE_90000_REACHED: NO
TECHNICAL_PASS: YES
SUBMISSION_PARITY: V8_NOT_APPLICABLE; V7_3_FALLBACK_YES_6X719
ONLY_CANONICAL_CODEX_SUBMISSION_REMAINS: YES
PRIMARY_REMAINING_BOTTLENECK: Q2_INCREMENTAL_SERVICEABILITY_AND_PAYBACK
NEXT_STEP: REJECT_3Q_AND_RETAIN_V7_3
TOURNAMENT_AUTHORIZED: NO
KAGGLE_EXECUTION_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```
