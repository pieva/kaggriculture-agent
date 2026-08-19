# NEW SESSION — Kaggriculture Agent

## Stato del progetto

Il progetto ha completato e consolidato due iterazioni sperimentali supervisionate.

Metodo adottato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Branch corrente:

`main`

Stato Git atteso:

- `main` allineato con `origin/main`;
- working tree pulito.

Ultimo commit consolidato:

`107e82b — Finalize E02 documentation`

Tag disponibili:

- `v0.1-e01-baseline`
- `v0.2-e02-roicrop`

---

## E01 — Baseline

Strategia:

`CarrotLoopAgent`

Caratteristiche principali:

- coltura fissa `CARROT`;
- singola tile `(4, 4)`;
- nessun movimento;
- ciclo operativo:

`BUY_SEED → PLANT → WATER → HARVEST → SELL`

Baseline quantitativa definitiva ricostruita dai dati persistenti:

- Mean Final Money: `$3567.63`;
- Sample Std Dev (`ddof=1`): `± $205.38`;
- Median Final Money: `$3528.00`;
- Overall Win Rate: `66.67%`;
- Win Rate vs `starter`: `0.00%`;
- Draw Rate vs `starter`: `100.00%`.

Tag:

`v0.1-e01-baseline`

La submission Kaggle E01 era stata validata inizialmente con rating osservato `600.0`.

In uno screenshot successivo il rating E01 risultava `328.4`.

Il rating Kaggle è dinamico e non deve essere confuso con le metriche del benchmark locale.

---

## E02 — Dynamic Crop Selection & ROI Scaling

Strategia:

`ROICropAgent`

Variabile sperimentale modificata rispetto a E01:

**selezione dinamica della coltura in funzione del ROI/giorno e della liquidità disponibile**

Formula implementata:

`NetProfitPerDay(c) = ((SellPrice_c × Yield_c) - SeedPrice_c) / Days_c`

L'esperimento mantiene invariati:

- singola tile `(4, 4)`;
- assenza di movimento;
- infrastruttura di benchmark;
- durata degli episodi;
- avversari;
- ciclo operativo fondamentale.

Tag:

`v0.2-e02-roicrop`

### Risultati benchmark locale E02

- Total Episodes: `30`;
- Completion Rate: `100.00%`;
- Disqualification Rate: `0.00%`;
- Overall Win Rate: `100.00%`;
- Win Rate vs `starter`: `100.00%`;
- Mean Final Money: `$5857.17`;
- Sample Std Dev (`ddof=1`): `± $132.37`;
- Median Final Money: `$5837.00`;
- Agent Mean Turn Latency: `0.0267 ms/turno`.

Confronto E01 → E02:

- Mean Final Money: `$3567.63 → $5857.17`;
- incremento assoluto: `+$2289.53`;
- incremento percentuale: `+64.18%`;
- Win Rate vs `starter`: `0% → 100%`.

Ipotesi E02:

`SUPPORTATA nelle condizioni sperimentali testate`

---

## Evidenza osservabile del miglioramento E02

La simulation analysis ha mostrato che il miglioramento non deriva genericamente da una strategia complessa, ma soprattutto dal fatto che la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.

Principali evidenze:

- `MELON` risulta Rank 1 sia con il modello implementato `Yield=2` sia utilizzando `max_yield`;
- i primi due cicli completati e venduti sono `MELON`;
- l'irrigazione consente di raggiungere la resa massima;
- i due raccolti completati producono un profitto netto complessivo di circa `+$3117`;
- nella parte finale della stagione viene osservata anche la selezione di `STRAWBERRY`.

Conclusione interpretativa consolidata:

> E02 migliora principalmente perché la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.

---

## Limiti osservati in E02

Le evidenze hanno fatto emergere quattro dimensioni ancora non ottimizzate.

### 1. End-of-Season Horizon

L'agente può acquistare o piantare una coltura che non ha tempo di maturare prima della fine della stagione.

Nell'episodio osservato sono stati spesi soldi per semi in coda stagione che non hanno prodotto ricavi entro il turno 719.

### 2. Single-Tile Limitation

Il farmer continua a operare esclusivamente sulla casella `(4, 4)`.

La griglia disponibile rimane largamente inutilizzata.

### 3. Immediate Selling

Il raccolto viene venduto immediatamente.

Non esiste ancora alcuna strategia di market timing.

### 4. Yield Model Simplification

La formula ROI utilizza:

`Yield = 2`

mentre l'ambiente dispone di `max_yield` specifici per coltura.

La semplificazione non altera la scelta iniziale di `MELON`, che rimane Rank 1, ma limita la precisione economica del modello.

---

## SHIP E02

La submission standalone:

`submission/submission.py`

è stata:

- rigenerata;
- verificata con la suite di test;
- caricata realmente su Kaggle;
- completata con Status `Complete`.

Rating iniziale osservato E02:

`600.0`

Valutazione SHIP:

`PASSED WITH OBSERVATIONS`

Interpretazione corretta:

> E02 ha superato la validazione esterna Kaggle ed è entrata nel sistema competitivo con rating iniziale osservato `600.0`. Il benchmark locale dimostra il miglioramento rispetto a E01 nelle condizioni sperimentali testate; il confronto competitivo esterno richiede invece l'osservazione dell'evoluzione successiva del rating Kaggle.

Non confrontare direttamente:

- Mean Final Money locale;
- Kaggle Skill Rating.

Misurano aspetti differenti.

---

## Evidenze principali E02

Implementation Plan:

`docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`

Benchmark:

`results/e02_roi_crop.json`

BUILD:

`docs/versions/E02_build_antigravity.md`

VERIFY REVIEW:

`docs/versions/E02_verify_review_antigravity.md`

Simulation Analysis:

`docs/versions/E02_simulation_analysis.md`

SHIP REVIEW:

`docs/versions/E02_ship_review_antigravity.md`

Screenshot Kaggle:

- `docs/screenshots/E02-004_kaggle_submission_ready.png`
- `docs/screenshots/E02-005_kaggle_submission_successful.png`

Prompt E02:

`docs/prompts/E02-01_start.md`

fino a:

`docs/prompts/E02-15_final_consolidation.md`

---

## Punto di partenza della prossima sessione

Non iniziare automaticamente E03.

La prossima attività consiste nel decidere quale **singola variabile sperimentale** modificare rispetto a E02.

Le principali candidate emerse dalle evidenze sono:

- End-of-Season Horizon;
- espansione multi-tile;
- market timing della vendita;
- utilizzo di `max_yield` nella formula ROI.

Prima di scegliere, confrontare:

1. impatto potenziale;
2. isolamento sperimentale;
3. complessità introdotta;
4. capacità di attribuire il risultato alla singola modifica;
5. valore didattico e metodologico dell'esperimento.

La successiva iterazione deve continuare a mantenere la logica:

**una modifica strategica principale per esperimento**

e deve essere definita solo dopo revisione delle evidenze E02.

## Post-SHIP observation

Dopo la chiusura e il tagging di E02 (`v0.2-e02-roicrop`), l'evoluzione
del Kaggle Skill Rating ha fornito una nuova evidenza competitiva.

- E01 `CarrotLoopAgent`: Skill Rating osservato `328.4`.
- E02 `ROICropAgent`: Skill Rating osservato `273.0`.
- Il leaderboard continua a mostrare il profilo con rating `328.4`,
  corrispondente alla migliore performance osservata di E01.
- Evidenze:
  - `docs/screenshots/E02-006_kaggle_rating_e02_below_e01.png`
  - `docs/screenshots/E02-007_kaggle_leaderboard_e01.png`

Questa osservazione non modifica i risultati del benchmark locale E02:
`ROICropAgent` migliora il Mean Final Money da `$3567.63` a `$5857.17`
(`+64.18%`) nelle condizioni sperimentali testate.

Mostra invece che l'ottimizzazione locale basata sul ROI della coltura
non si traduce automaticamente in una migliore performance competitiva
contro gli agenti presenti sulla piattaforma Kaggle.

La prossima iterazione non deve quindi partire automaticamente da una
soluzione già decisa. Deve prima analizzare la divergenza tra benchmark
locale e comportamento competitivo, utilizzando le evidenze disponibili,
per formulare una nuova ipotesi sperimentale E03.

<!-- END OF DOCUMENT -->