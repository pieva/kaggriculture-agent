# KAGGRICULTURE C2 — CODEX V7.2 DUAL-Q ACTIVATION

## Mandato

Costruire e verificare una candidata Codex derivata dalla V7.1 Serviceability che estenda il modello produttivo da Q0 a **Q0+Q1**, mantenendo Q0 stabile e attivando in Q1 un secondo modulo analogo ma avviato più tardi.

Target centrale:

```text
FINAL_MONEY_MEAN: 75000
```

La candidata deve rimanere isolata dalla V7.1 canonica fino al completamento della verifica. Non sostituire `submission/submission_codex.py` e non modificare i risultati V7.1.

## Autorizzazioni

```text
TASK_TYPE: IMPLEMENTATION_AND_LOCAL_VALIDATION
IMPLEMENTATION_AUTHORIZED: YES
LOCAL_REPLAY_AUTHORIZED: YES
BOUNDED_CAUSAL_ITERATION_AUTHORIZED: YES
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
FOUNDATION_MODIFICATION_AUTHORIZED: NO
ENGINE_MODIFICATION_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

## Baseline obbligatoria

Usare come baseline immutabile:

- controller: `src/agricola/strategy/codex_compact_q0.py`;
- config: `configs/model_spec_c2/CODEX_C2_CONFIG.json`;
- risultati: `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_RESULTS.json`;
- report: `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_FINAL_REPORT_IT.md`;
- commit di riferimento: `beefae1`.

Metriche V7.1:

```text
FINAL_MONEY_MEAN: 61118.83
FINAL_MONEY_MIN: 57859.00
MELON: 103.00
STRAWBERRY: 36.83
MILK: 90.00
WOOL: 60.00
ANIMAL_ESCAPES: 0
MOVE_PER_PRODUCTIVE_ACTION: 3.0321
```

## Architettura V7.2

### Q0 — modulo congelato

```text
18 CROP
3 COW
3 SHEEP
6 PASTURE
6 WORKER OPERATIVI
```

Conservare:

- footprint, mix e coorti V7.1;
- serviceable bootstrap binding;
- inventory-aware feed dispatch;
- feed-first cluster batching;
- tre zone crop;
- ownership e reservation atomica;
- fertilizer logistics;
- zero fughe.

### Q1 — secondo modulo

```text
18 CROP
3 COW
3 SHEEP
6 PASTURE
6 WORKER OPERATIVI DEDICATI
```

Q1 deve replicare i meccanismi di Q0 usando coordinate locali del quadrante e propri proprietari di cluster/zone. Non deve sottrarre worker operativi a Q0.

### Capacità condivisa

```text
1 FARMER / RELIEF_LOGISTICS CONDIVISO
12 HANDS
13 WORKERS TOTALI
1 SHED
1 MARKET PLANNER
```

## Vincoli economici reali

Il costo giornaliero delle 12 assunzioni è la somma Fibonacci:

```text
1+1+2+3+5+8+13+21+34+55+89+144 = 376
```

Q1 deve quindi produrre un contributo netto positivo dopo:

- 1.000 di terra;
- costo degli animali;
- salari marginali;
- WHEAT e riserva feed;
- seed;
- minore orizzonte biologico;
- congestione dello shed;
- impatto dell'offerta sui prezzi di mercato.

Distribuire HIRE, BUY, SELL e seed procurement su più turni rispettando il limite di 10 ordini market per turno.

## Attivazione Q1

Non usare un giorno fisso privo di verifica. Ammettere Q1 soltanto quando:

```text
Q0_ANIMAL_ESCAPES = 0
Q0_FEED_SET_SERVICEABLE = YES
Q0_CROP_HARD_TASKS_WITHIN_CAPACITY = YES
CASH_COVERS_LAND_AND_OPERATING_BUFFER = YES
REMAINING_HORIZON_SUPPORTS_FIRST_OUTPUT = YES
```

Finestra obiettivo: **D6–D8**. Se l'attivazione avviene dopo D10, classificare il rischio di payback e non acquistare automaticamente l'intero modulo.

Usare un ledger esplicito di attivazione con costi previsti, primo output monetizzabile, capacità richiesta e slack osservato.

## Ruoli

Una mappa consigliata è:

| Worker | Ruolo |
|---|---|
| W0 | GLOBAL_RELIEF_LOGISTICS |
| W1–W6 | proprietari operativi Q0 |
| W7–W12 | proprietari operativi Q1 |

Per ciascun quadrante:

- 2 specialisti livestock;
- 3 proprietari di zone crop;
- 1 fertilizer/logistics.

I fallback per roster incompleto devono essere locali al quadrante e limitati alla chiusura delle urgenze. Vietare cross-quadrant assist ordinario.

## Serviceability obbligatoria

Per entrambi i moduli:

1. ogni cluster animale ha un owner attivo;
2. FEED richiede WHEAT trasportato oppure commitment composto `SHED→PICKUP→PASTURE→FEED`;
3. pickup batch sull'intero insieme di feed dovuti;
4. FEED precede CARE, product collection e fertilizer collection;
5. le crop hard WATER precedono task soft;
6. cross-zone assist solo con zona originaria libera;
7. fertilizzante applicato soltanto a crop irrigate e legalmente eleggibili;
8. nessun target duplicato;
9. nessun movimento verso un'interazione illegalmente non serviceable.

## Gate di accettazione

### Gate minimo

```text
TECHNICAL_PASS: YES
ERRORS: 0
FALLBACKS: 0
FINAL_MONEY_MEAN >= 68000
FINAL_MONEY_MIN >= 55000
ANIMAL_ESCAPES_TOTAL = 0
Q0_CROP_REGRESSION <= 5%
Q1_NET_CONTRIBUTION > 0
```

### Target centrale

```text
FINAL_MONEY_MEAN >= 75000
FINAL_MONEY_MIN >= 65000
TOTAL_MILK >= 145
TOTAL_WOOL >= 100
TOTAL_CROP_UNITS >= 220
Q0_CROP_UNITS >= 130
Q1_CROP_UNITS >= 85
MOVE_PER_PRODUCTIVE_ACTION <= 3.50
```

### Stretch

```text
FINAL_MONEY_MEAN: 82000-85000
FINAL_MONEY_MIN >= 70000
```

## Protocollo di verifica

Usare senza selezione post-hoc:

```text
SEEDS: 26090101, 26090102, 26090103
SEATS: 0, 1
OPPONENT: INERT_PASS_POLICY
EPISODE_STEPS: 720
TURNS_PER_DAY: 24
EPISODES: 6
```

Confrontare ogni episodio contro la corrispondente baseline V7.1. Conservare tutti i run, inclusi gli outlier.

Sono ammessi al massimo tre cicli causali. Dopo ogni ciclo decomporre:

- ricavi Q0 e Q1;
- costi terra, animali, feed, seed e salari;
- giorno di attivazione Q1;
- primo output Q1;
- produzione per quadrante;
- FEED/CARE/COLLECT per quadrante;
- MOVE, PASS e commitment abbandonati per ruolo;
- congestione e overflow shed;
- realized price per prodotto.

## Artefatti richiesti

- candidata Codex Dual-Q versionata e isolata;
- configurazione separata;
- test dedicati;
- benchmark separato;
- `results/model_spec_c2/codex/CODEX_V7_2_DUAL_Q_RESULTS.csv`;
- `results/model_spec_c2/codex/CODEX_V7_2_DUAL_Q_RESULTS.json`;
- `results/model_spec_c2/codex/CODEX_V7_2_DUAL_Q_FINAL_REPORT_IT.md`.

Non sovrascrivere gli artefatti V7.1.

## Blocco finale obbligatorio

```text
CANDIDATE_VERSION: <value>
Q0_MODULE_PRESERVED: YES | PARTIAL | NO
Q1_ACTIVATION_DAY_MEAN: <value>
Q1_FULL_MODULE_DAY_MEAN: <value>
FINAL_MONEY_MEAN: <value>
FINAL_MONEY_MEDIAN: <value>
FINAL_MONEY_MIN: <value>
FINAL_MONEY_MAX: <value>
DELTA_VS_V7_1: <value>
Q1_NET_CONTRIBUTION: <value>
MILK_MEAN: <value>
WOOL_MEAN: <value>
Q0_CROP_UNITS_MEAN: <value>
Q1_CROP_UNITS_MEAN: <value>
TOTAL_CROP_UNITS_MEAN: <value>
ANIMAL_ESCAPES_TOTAL: <value>
MOVE_PER_PRODUCTIVE_ACTION: <value>
OBJECTIVE_68000_REACHED: YES | NO
OBJECTIVE_75000_REACHED: YES | NO
TECHNICAL_PASS: YES | NO
PRIMARY_REMAINING_BOTTLENECK: <value or NONE>
NEXT_STEP: FREEZE_DUAL_Q | ONE_MORE_CAUSAL_ITERATION | REJECT_DUAL_Q
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

## STOP

Dopo la verifica e il report fermarsi. Non sostituire la submission V7.1, non eseguire torneo/Kaggle e non creare commit o push.
