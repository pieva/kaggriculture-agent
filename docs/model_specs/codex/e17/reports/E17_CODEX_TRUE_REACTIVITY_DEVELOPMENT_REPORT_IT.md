# E17.1 — sviluppo della reattività reale Codex

- **Data:** 2026-09-02
- **Ruolo dell'evidenza:** `DEVELOPMENT_ONLY`
- **Candidata:** `CODEX-E17.1-TRUE-REACTIVE-V2`
- **Controllo:** `CODEX-E17.1-3Q-REACTIVE-GUARDED-V1`
- **Famiglia causale modificata:** `MARKET_REGIME_ADAPTATION`
- **Holdout/final confirmation:** non usati
- **Verdetto:** `TECHNICAL_AND_REACTIVITY_GATES_PASS / NOT_KAGGLE_READY`

## 1. Decisione metodologica

La quota di allevamento Q2 non è stata trattata come parametro da impostare.
È stata mantenuta fra gli outcome insieme a timing Q1/Q2, densità, workforce e
composizione colturale. La priorità è verificare che Codex emetta decisioni
diverse quando cambia lo stato osservato e che ogni divergenza sia motivata e
riproducibile.

La V2 è il primo incremento controllato, non una policy completamente
state-driven. Conserva la V9 e la guardia V1 come provider immutabile, ma rende
reattiva una sola famiglia sicura: il timing delle vendite di output fungibili.
Può differire una vendita a prezzo basso, monetizzare un'opportunità osservata
e rilasciare obbligatoriamente l'inventario differito dopo sei step. Non vende
Wheat opportunisticamente e non cancella acquisti strutturali di animali.

## 2. Correzione causale durante lo smoke test

Il primo prototipo vendeva il Wheat eccedente la riserva alimentare
istantanea e poteva differire acquisti di animali. Il test ha mostrato il
failure mode: una routine precompilata continua a eseguire azioni successive
che presuppongono quegli acquisti; inoltre la riserva istantanea non copre il
servicing futuro. Il risultato preliminare era economicamente distruttivo e
produceva fughe.

La candidata definitiva ha quindi:

- escluso Wheat dalle vendite opportunistiche;
- disabilitato la soppressione degli acquisti strutturali;
- limitato la dilazione a sei step con rilascio automatico;
- lasciato invariati routing, espansione e allocazione dei quadranti.

Questa correzione dimostra anche il limite architetturale corrente: la
reattività strutturale richiede che acquisto, placement, servicing e routing
siano ripianificati insieme dallo stato; non può essere ottenuta cancellando
singoli comandi di una sequenza open-loop.

## 3. Disegno definitivo

Sono stati eseguiti 48 episodi:

```text
3 seed development × 2 seat × 4 regimi × 2 policy
```

I regimi sono:

| Regime | Avversario/perturbazione |
|---|---|
| `INERT` | policy `PASS`, nessuna contesa |
| `WHEAT_SCARCITY` | V9 congelata più acquisto concorrente di Wheat |
| `OUTPUT_PRESSURE` | V9 congelata più vendita dell'output disponibile |
| `LIQUIDITY_STRESS` | combinazione delle due perturbazioni di mercato |

Il confronto economico è sempre candidato–controllo sullo stesso seed, seat e
regime. I valori assoluti nei regimi perturbati sono diagnostici: l'iniezione
modifica deliberatamente anche l'economia dell'avversario.

## 4. Risultati

| Regime | N candidata | Mean V2 | Mean V1 | Delta matched | Delta % | Override V2 | Fughe |
|---|---:|---:|---:|---:|---:|---:|---:|
| `INERT` | 6 | 134.060,17 | 132.019,33 | +2.040,83 | +1,55% | 934 | 0 |
| `WHEAT_SCARCITY` | 6 | 131.225,00 | 129.588,00 | +1.637,00 | +1,26% | 994 | 0 |
| `OUTPUT_PRESSURE` | 6 | 94.463,00 | 96.112,17 | −1.649,17 | −1,72% | 1.147 | 0 |
| `LIQUIDITY_STRESS` | 6 | 131.050,67 | 134.379,50 | −3.328,83 | −2,48% | 994 | 0 |
| **Totale** | **24** | **122.699,71** | **123.024,75** | **−325,04** | **−0,26%** | **4.069** | **0** |

Ragioni registrate: `LOW_PRICE_SALE_DEFERRED` 3.288,
`DEFERRED_SALE_RELEASED` 1.285 e `HIGH_PRICE_OPPORTUNISTIC_SALE` 47. Una
singola deviazione può avere più ragioni, quindi il totale delle ragioni è
maggiore del numero di batch modificati.

Per ogni coppia seed/seat la candidata produce tre o quattro action-stream
distinti fra i quattro regimi. La copertura di tracciabilità delle 4.069
divergenze è 100%: trigger osservato, fatti, hash della proposta e hash
dell'azione emessa sono presenti. La determinazione same-state è coperta dai
test mirati.

## 5. Gate

| Gate | Esito |
|---|---|
| discriminazione paired-observation | `PASS` |
| determinismo same-state | `PASS` |
| action-stream divergente fra regimi | `PASS` |
| trigger e ragione per ogni divergenza | `PASS` — 100% |
| override naturali in almeno due regimi non inerti | `PASS` — 3/3 |
| regressione inerte almeno −5% | `PASS` — +1,55% |
| errori tecnici | `PASS` — 0 |
| forme d'azione invalide | `PASS` — 0 |
| fughe EOD strette | `PASS` — 0 |
| holdout/final confirmation intatti | `PASS` |

Il superamento dei gate dimostra che il ramo commerciale è realmente
state-dependent e sicuro nel perimetro testato. Non dimostra che l'intero
agente sia già reattivo né che la V2 generalizzi su Kaggle.

## 6. Outcome 3Q

La composizione animale finale resta `Q0/Q1/Q2 = 8/6/5` in tutti i 24 episodi
della candidata. Q2 vale il `59,86%` degli animal-tile-days Q0 nella finestra
misurata; la composizione crop finale cambia soltanto fra `6/1/6` e `7/1/6`.

Questo risultato è atteso e informativo: una modifica esclusivamente
commerciale non ha ancora propagato una decisione strutturale alla quota
allevamento Q2. Forzare quella quota ora violerebbe l'impostazione causale.

## 7. Verdetto e sviluppo successivo

La V2 viene conservata come **proof of reactivity** e benchmark di sviluppo,
ma non sostituisce la submission reattiva V1 e non è autorizzata per Kaggle.
Il risultato economico è misto e la policy dipende ancora dalla sequenza V9
per unità, acquisti strutturali ed espansione.

Il prossimo incremento deve introdurre un
`STATE_DRIVEN_EXECUTION_CORE`, una famiglia alla volta:

1. rappresentare obiettivi e code di servizio anziché comandi per step;
2. scegliere soltanto azioni fattibili dallo stato corrente;
3. collegare acquisto, placement e servicing degli animali in un unico piano;
4. assegnare budget e workforce in base a cassa, feed debt, crop deadline e
   rendimento osservato;
5. lasciare che timing Q1/Q2 e quota animale/crop di ogni quadrante emergano
   dalle priorità e dai vincoli.

La prima sottofamiglia proposta è `REACTIVE_SERVICE_AND_ROUTING`: deve
risolvere feed/care/harvest urgenti e ripianificare il percorso quando una
precondizione non è realizzata. Solo dopo questo passaggio sarà lecito
attivare `REACTIVE_ACQUISITION_AND_PLACEMENT`; allora la variazione della quota
allevamento Q2 potrà diventare una conseguenza reale della policy.

## 8. Artefatti

- piano: `docs/model_specs/codex/e17/design/E17_CODEX_TRUE_REACTIVITY_ACTIVATION_PLAN_V1.md`;
- configurazione: `docs/model_specs/codex/e17/configs/CODEX_E17_1_TRUE_REACTIVE_V2.json`;
- policy: `src/agricola/strategy/codex/codex_e17_true_reactive.py`;
- runner: `docs/model_specs/codex/e17/tools/run_codex_e17_true_reactivity_development.py`;
- test: `docs/model_specs/codex/e17/tests/test_codex_e17_true_reactive.py`;
- metriche compatte: `docs/model_specs/codex/e17/artifacts/derived/E17_1_TRUE_REACTIVITY_DEVELOPMENT_METRICS.json`.
