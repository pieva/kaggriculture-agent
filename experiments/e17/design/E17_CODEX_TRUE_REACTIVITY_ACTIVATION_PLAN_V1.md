# E17 — piano di attivazione della reattività reale Codex

- **Data:** 2026-09-02
- **Stato:** `EXECUTED / V2 DIAGNOSTIC GATES PASS / NOT KAGGLE READY`
- **Ambito:** Codex E17, seed development già consumati
- **Holdout:** vietato
- **Controllo congelato:** `CODEX-E17.1-3Q-REACTIVE-GUARDED-V1`
- **Evidenza di partenza:** 10 replay Kaggle `EXTERNAL_DIAGNOSTIC`

## 1. Decisione

La prossima priorità non è ottimizzare direttamente la quota di allevamento
Q2. La quota Q2 deve diventare un **outcome endogeno** della policy, determinato
da prezzi, inventario di mercato, liquidità, capacità di servicing, stato
delle colture e progresso effettivo dei quadranti.

Il trattamento causale successivo è quindi l'introduzione di un vero
meccanismo di decisione state-dependent. Timing Q1/Q2, quota animale per
quadrante, specie e densità saranno misure di risposta, non soglie selezionate
prima del test.

## 2. Evidenza che invalida la priorità precedente

Nei dieci replay esterni della submission `559631298`:

- l'action stream richiesto ha **un solo SHA-256** in 10/10 episodi;
- lo stato strutturale eseguito ha quattro SHA-256 e la traiettoria dominante
  ricorre in 7/10 episodi;
- score Codex: min `42.850`, max `120.014`, media `78.808,7`;
- timing, workforce, comandi e composizione finale sono quasi invarianti;
- Q2/Q0 animal-tile-days è `63,29%`, ma nove episodi hanno lo stesso profilo
  `8/6/5` animali medi Q0/Q1/Q2.

La variazione economica osservata non ha quindi prodotto una variazione delle
decisioni emesse. Questo non dimostra che nessuna guardia possa mai attivarsi,
ma dimostra che nel corpus esterno la candidata non si è comportata come una
policy adattiva.

## 3. Causa radice nel disegno V1

La candidata corrente delega sempre la proposta alla V9 congelata e limita le
modifiche alla famiglia `WHEAT_FEED_SERVICEABILITY`. La guardia di mercato è
ammessa soltanto se viene inferito un acquisto Wheat non eseguito o se esiste
un animale critico a EOD. La guardia FEED richiede inoltre un worker già sulla
tile critica e Wheat nel suo inventario.

Queste sono protezioni di emergenza rare. Non rispondono ai normali segnali
economici: prezzi relativi, pressione sull'inventory condiviso, liquidità,
ritardi di esecuzione, saturazione dei quadranti o rendimento marginale di
crop e bestiame. I test sintetici correnti provano la raggiungibilità dei rami,
non la loro rilevanza nel normale dominio operativo.

## 4. Prima famiglia causale: regime di mercato

La prima nuova candidata deve modificare una sola famiglia:

```text
MARKET_REGIME_ADAPTATION
```

Il controller osserva esclusivamente campi disponibili nel contratto della
Foundation e classifica lo stato economico almeno in:

1. `NORMAL` — nessuna deviazione dalla proposta V9;
2. `INPUT_SCARCITY` — input necessario scarso/costoso o ordine non eseguito;
3. `OUTPUT_PRESSURE` — prezzo o inventory rende non conveniente monetizzare
   secondo lo schedule fisso;
4. `LIQUIDITY_STRESS` — la cassa non sostiene simultaneamente produzione,
   servicing ed espansione.

La classificazione non deve imporre direttamente quanti animali collocare in
Q2. Deve produrre priorità e budget osservabili; la topologia emerge dalle
azioni economicamente e logisticamente ammissibili.

## 5. Benchmark discriminante

Usare gli stessi seed development, seat-balanced, contro regimi avversari
controllati:

| Regime | Perturbazione | Risposta attesa |
|---|---|---|
| `INERT` | nessuna contesa | parità o quasi-parità col controllo |
| `WHEAT_SCARCITY` | acquisti concorrenti di Wheat | protezione servicing e sostituzione/defer delle spese |
| `OUTPUT_PRESSURE` | vendite concorrenti sulle produzioni dominanti | timing o mix di monetizzazione differente |
| `LIQUIDITY_STRESS` | contesa input/land che riduce la cassa realizzata | espansione e acquisti condizionati alla cassa osservata |

Il confronto primario è **within-seed fra regimi**, non fra seed diversi. La
policy V1 congelata è il controllo negativo: ci si attende un action stream
invariante salvo le sue rare guardie di emergenza.

## 6. Gate di reattività

```text
PAIRED_OBSERVATION_DISCRIMINATION == PASS
SAME_STATE_DETERMINISM == PASS
ACTION_STREAM_DIVERGES_ACROSS_MARKET_REGIMES == PASS
EACH_DIVERGENCE_HAS_OBSERVED_TRIGGER_AND_REASON == PASS
NATURAL_OVERRIDE_COUNT > 0_IN_AT_LEAST_TWO_NON_INERT_REGIMES
INERT_REGRESSION_VS_CONTROL >= -5%
TECHNICAL_ERRORS == 0
INVALID_ACTIONS == 0
ANIMAL_ESCAPES == 0
HOLDOUT_USED == false
```

Un numero elevato di override non costituisce un successo. Il gate richiede
divergenze motivate negli scenari perturbati e assenza di variazioni spurie
quando lo stato rilevante è equivalente.

## 7. Telemetria obbligatoria

Per ogni deviazione registrare:

- feature osservate e loro fonte Foundation;
- regime classificato;
- proposta del provider V9;
- azione emessa;
- ragione e budget coinvolto;
- esito al passo successivo (`requested` distinto da `executed`);
- effetti su cassa, inventory, service debt e densità dei quadranti.

KPI economici, Q1/Q2, workforce, quota animale Q0/Q1/Q2, specie, crop,
MOVE/produttive, ordini non eseguiti e fughe restano outcome secondari.

## 8. Stop boundary

Questa preregistrazione non autorizza uso dell'holdout, modifica della
submission Kaggle o selezione retroattiva di soglie dai dieci replay esterni.
La prima candidata viene promossa soltanto se dimostra reattività naturale e
tracciabile nei regimi development senza violare i gate di sicurezza.
