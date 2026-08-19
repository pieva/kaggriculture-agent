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
  - Win Rate vs `random`: 100.00% ($3610.50)
  - Draw Rate vs `starter`: 100.00% Draw / 0% Sconfitte ($3531.60)
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
