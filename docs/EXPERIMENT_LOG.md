# Experiment Log

## E01 — Project definition, baseline implementation, benchmark runner & observable verification

**Date:** 2026-08-18 to 2026-08-19  
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW → CONSOLIDATE → SHIP  
**Tool:** Google Antigravity  
**Model:** Gemini 3.6 Flash

### Objective

Verificare se Antigravity è in grado di analizzare autonomamente Kaggriculture, produrre un Implementation Plan dettagliato, realizzare l'infrastruttura modulare del repository, implementare la baseline iniziale, costruire una suite di valutazione benchmark automatizzata, eseguire la verifica osservabile del ciclo decisionale del contadino e validare la submission sulla piattaforma Kaggle.

### Starting state

- repository Git vuoto;
- repository GitHub privato;
- nessun codice;
- nessuna struttura applicativa;
- nessuna baseline fornita;
- nessuna strategia suggerita manualmente.

### Prompt

See `docs/prompts/E01-01_define_plan.md`, `docs/prompts/E01-02_review_feedback.md`, `docs/prompts/E01-03_verify.md`, `docs/prompts/E01-04_verify_review.md`.

### Observations & Actions

1. **Studio Ambiente & Setup**: Configurato l'ambiente virtuale isolato Python 3.12 (`.venv`) con `kaggle-environments`.
2. **Implementation Plan & Repository Hygiene**: Prodotto ed approvato l'Implementation Plan; creato `README.md` e `.gitignore` per escludere cache e `.venv`.
3. **Infrastruttura Modulare & Bundling**:
   - Creato il pacchetto `src/agricola/` (`GameState`, `ActionBuilder`, `CarrotLoopAgent`, `agent.py`).
   - Implementato lo script `scripts/build_submission.py` che genera il file standalone `submission/submission.py`.
4. **Rinominazione Metrica Disqualification Rate**:
   - Rinominata la metrica da "Invalid Action Rate" a **Disqualification Rate (%)** per riflettere con esattezza l'osservabile misurato dall'engine (percentuale di episodi conclusi con stato `INVALID` o `ERROR`).
5. **Misurazione Precisa Latenza Agente**:
   - Implementato `TimedAgentWrapper` in `src/agricola/evaluation/runner.py` per misurare separatamente ed isolatamente la latenza decisionale dell'agente (**Agent Mean Turn Latency**), distinguendola dalla durata complessiva dello step di simulazione dell'engine (**Simulation Mean Step Time**).
6. **Livello di Verifica & Test**:
   - Chiaramente distinti gli unit test (`GameState`, `ActionBuilder`, `agent` output), gli smoke/integration test (`test_short_simulation_smoke`, `test_build_and_run_submission_smoke`) e il benchmark completo E01 (30 episodi $\times$ 720 turni = 21.600 turni).
7. **Validazione Kaggle Platform**:
   - `submission/submission.py` è stato caricato sulla piattaforma Kaggle ed eseguito con successo (Status **`Complete`**, Score iniziale **`600.0`**).
8. **Esecuzione Osservabile VERIFY**:
   - Eseguito un episodio completo di 720 turni tramite Antigravity ed ispezionato il registro degli stati `env.steps`.
   - Confermato e documentato in `docs/versions/E01_verify_antigravity.md` il ciclo operativo: `BUY_SEED → PLANT → WATER → PASS → HARVEST → PLANT → SELL`.
   - Verificato univocamente per l'episodio VERIFY: `status: DONE`, 720/720 turni completati, `money finale: 3564.0`, `reward finale: 3564.0` (`reward == farm["money"]`).

### Human intervention

- Approvazione dell'Implementation Plan (`docs/prompts/E01-01_define_plan.md`).
- Review indipendente tramite `docs/prompts/E01-02_review_feedback.md` (consolidamento metrica, latenza, README, `.gitignore`).
- Review del VERIFY tramite `docs/prompts/E01-04_verify_review.md` (chiarimento ed unificazione univoca di reward e money a 3564.0).

### Outcome & Verification Evidence

- **Suite di Test (`pytest tests/`)**: 5/5 test superati con successo (3 unit test, 2 smoke integration test).
- **Bundling Submission (`scripts/build_submission.py`)**: `submission/submission.py` generato e verificato su Kaggle (Score `600.0`).
- **Benchmark Metric Summary E01 (`results/e01_baseline.json`)**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: 100.00%
  - Disqualification Rate: 0.00%
  - Overall Win Rate: 66.67% (20W / 0L / 10D)
  - Win Rate vs `pass`: 100.00% ($3594.30)
  - Win Rate vs `random`: 100.00% ($3577.00)
  - Draw Rate vs `starter`: 100.00% Draw / 0% Sconfitte ($3531.60)
  - Mean Final Money: **$3567.63** (Sample Std Dev `ddof=1`: **± $205.38**; Population Std Dev `ddof=0`: **± $201.93**)
  - Median Final Money: **$3528.00**
  - Agent Mean Turn Latency: **0.0142 ms/turno**
  - Simulation Mean Step Time: **3.69 ms/step**

### Method assessment

DEFINE: PASSED  
PLAN: PASSED  
BUILD: PASSED  
VERIFY: PASSED  
REVIEW: PASSED  
CONSOLIDATE: PASSED  
SHIP: PASSED (Tag: `v0.1-e01-baseline`)

---

## E02 — Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)

**Date:** 2026-08-19  
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW (SHIP Pending)  
**Tool:** Google Antigravity  
**Model:** Gemini 3.6 Flash

### Objective

Sostituire la monocultura statica di carote della baseline E01 (`CarrotLoopAgent`) con una regola di selezione dinamica della coltura basata sul profitto netto stimato per giorno ($\text{NetProfitPerDay} = \frac{(\text{SellPrice} \times \text{Yield}) - \text{SeedPrice}}{\text{Days}}$), al fine di massimizzare la crescita del capitale ed eliminare il pareggio con l'agente `starter`.

### Baseline E01 utilizzata per il confronto

- **Mean Final Money E01**: **`$3567.63 ± $205.38`** (Deviazione standard campionaria `ddof=1`; deviazione standard popolazione `ddof=0`: `$201.93`)
- **Median Final Money E01**: **`$3528.00`**
- **Win Rate vs `starter`**: **`0.00%`** (100.00% Pareggi / 10D)

*Nota storica sull'evoluzione del riferimento quantitativo*: Durante la fase di PLAN e BUILD era stata inizialmente utilizzata la stima `$3578.80` (derivata dalla media aritmetica delle tre medie aggregate per avversario documentate provvisoriamente). La successiva fase di VERIFY e REVIEW ha rilevato che `$3578.80` non era riproducibile dai 30 episodi grezzi memorizzati in `results/e01_baseline.json` ed ha ricostruito con esattezza la baseline persistente reale pari a **`$3567.63 ± $205.38`**.

### Prompt

References:
- `docs/prompts/E02-01_start.md`
- `docs/prompts/E02-02_plan_review.md`
- `docs/prompts/E02-03_plan_final_check.md`
- `docs/prompts/E02-04_build_approval.md`
- `docs/prompts/E02-05_verify.md`
- `docs/prompts/E02-06_verify_review.md`
- `docs/prompts/E02-07_verify_review_correction.md`
- `docs/prompts/E02-08_simulation_analysis.md`
- `docs/prompts/E02-09_simulation_analysis_review.md`
- `docs/prompts/E02-10_simulation_analysis_correction.md`

### Implementation Plan & Evidenze

- Implementation Plan: [`docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md)
- Benchmark JSON E02: [`results/e02_roi_crop.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e02_roi_crop.json)
- Evidenza BUILD: [`docs/versions/E02_build_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E02_build_antigravity.md)
- Evidenza VERIFY REVIEW: [`docs/versions/E02_verify_review_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E02_verify_review_antigravity.md)
- Evidenza Analisi Simulazione: [`docs/versions/E02_simulation_analysis.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E02_simulation_analysis.md)

### Human intervention

1. **Scelta e approvazione dell'evoluzione E02**: Definizione del focus su ROI crop selection anziché movimento o multi-tile.
2. **Review dell'Implementation Plan**: Richiesta di chiarimenti su `MELON max_yield_day = 12`, distinzione tra SeedPrice (statico) e SellPrice (dinamico), ed eliminazione di ambiguita sulla dispersione.
3. **Approvazione esplicita per BUILD**: Rilascio del via libera all'implementazione senza modifiche non concordate.
4. **Review indipendente VERIFY**: Esecuzione del ricalcolo indipendente dei dati di benchmark senza alterare il codice.
5. **Rilevazione incoerenza baseline E01**: Segnalazione della discrepanza tra `$3578.80` e `$3567.63`, guidando la ricostruzione dai dati grezzi.
6. **Correzione delle formulazioni causali**: Rimozione di affermazioni causali eccessivamente forti non dimostrate dai dati grezzi.
7. **Review dell'Analisi Osservabile della Simulazione**: Identificazione di imprecisioni nella contabilità dei cicli, nel confronto CARROT e nel modello di resa, ed approvazione della ricostruzione finale.

### Modifiche Implementate

1. **Allineamento Parametri `CROPS` (`src/agricola/core/state.py`)**:
   - Aggiornati i valori statici del dizionario `CROPS` con i parametri ufficiali dell'engine `kaggriculture` (`WHEAT`: max_yield_day=4; `CARROT`: seed=20; `TOMATO`: seed=50, max_yield_day=8; `STRAWBERRY`: seed=100, max_yield_day=10; `MELON`: seed=80, max_yield_day=12).
2. **Modulo Strategico `ROICropAgent` (`src/agricola/strategy/roi_crop.py`)**:
   - Creato l'agente che seleziona la coltura ad alto ROI giornaliero ($\text{NetProfitPerDay}(c) = \frac{(\text{SellPrice}_c \times \text{Yield}_c) - \text{SeedPrice}_c}{\text{Days}_c}$) filtrando per liquidità disponibile ($\text{SeedPrice}_c \le \text{money}$).
3. **Entrypoint & Bundling (`src/agricola/agent.py`, `scripts/build_submission.py`)**:
   - Collegata la nuova classe `ROICropAgent` nell'entrypoint principale e rigenerato lo script standalone `submission/submission.py`.
4. **Unit Testing (`tests/test_roi_crop.py`)**:
   - Aggiunti unit test specifici per verificare il calcolo del ROI ed il comportamento di fallback con basso capitale.

### Verification & Outcome

- **Suite di Test (`pytest tests/`)**: **7/7 test superati** (100% success rate in 2.88s).
- **Integrazione Submission (`pytest tests/test_submission.py`)**: Superata in 2.73s.
- **Benchmark Metric Summary E02 (`results/e02_roi_crop.json`)**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: 100.00%
  - Disqualification Rate: 0.00%
  - Overall Win Rate: **100.00%** (30W / 0L / 0D)
  - Win Rate vs `pass`: 100.00% ($5908.50)
  - Win Rate vs `random`: 100.00% ($5829.00)
  - Win Rate vs `starter`: **100.00% Vittorie** (10W / 0L / 0D; Mean Money: $5834.00)
  - Mean Final Money E02: **`$5857.17`**
  - Sample Std Dev E02 (`ddof=1`): **`± $132.37`** (Population Std Dev `ddof=0`: **`± $130.14`**)
  - Median Final Money E02: **`$5837.00`**
  - Agent Mean Turn Latency: **0.0267 ms/turno**
  - Simulation Mean Step Duration: **3.45 ms/step**

### Confronto Quantitativo E01 $\rightarrow$ E02

- **Incremento Assoluto Capitale Medio**: $5857.17 - 3567.63 = \mathbf{+\$2289.53}$
- **Incremento Percentuale Capitale Medio**: $\mathbf{+64.18\%}$
- **Esito vs `starter`**: **`0.00% Vittorie (E01)` $\rightarrow$ `100.00% Vittorie (E02)`**

### Interpretazione Verificata & Limiti

> **Conclusione Principale**: E02 migliora principalmente perché la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.

- **Evidenze**: `ROICropAgent` seleziona `MELON` fin dal turno 1 (Rank 1 sia con `Yield=2` sia con `max_yield=6`); i primi due cicli completati nella simulazione generano oltre $1600 di incasso lordo ciascuno su singola casella; a fine stagione l'agente seleziona `STRAWBERRY`.
- **Limiti E02 Identificati**:
  1. *End-of-Season Horizon*: acquisto/semina di colture in coda stagione che non giungono a maturazione prima del turno 719 ($200 spesi per 2 semi inutilizzati);
  2. *Single-Tile Limitation*: isolamento sulla sola casella `(4, 4)`;
  3. *Immediate Selling*: vendita immediata al raccolto senza timing sui picchi di mercato;
  4. *Yield Model Simplification*: uso di `Yield=2` anziché dei valori `max_yield` specifici della coltura.

### Method assessment

DEFINE: PASSED  
PLAN: PASSED  
BUILD: PASSED  
VERIFY: PASSED  
REVIEW: PASSED  
CONSOLIDATE: PASSED  
SHIP: PENDING (In attesa dell'invio della submission Kaggle reale e del tag di versione)
