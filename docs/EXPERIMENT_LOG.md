# Experiment Log

## E01 — Project definition, baseline implementation & benchmark runner

**Date:** 2026-08-18  
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW → CONSOLIDATE  
**Tool:** Google Antigravity  
**Model:** Gemini 3.6 Flash

### Objective

Verificare se Antigravity è in grado di analizzare autonomamente Kaggriculture, produrre un Implementation Plan dettagliato, realizzare l'infrastruttura modulare del repository, implementare la baseline iniziale, costruire una suite di valutazione benchmark automatizzata ed effettuare la consolidazione del repository seguendo la revisione indipendente.

### Starting state

- repository Git vuoto;
- repository GitHub privato;
- nessun codice;
- nessuna struttura applicativa;
- nessuna baseline fornita;
- nessuna strategia suggerita manualmente.

### Prompt

See `docs/prompts/E01_define_plan.md` and `docs/prompts/E01_review_feedback.md`.

### Observations & Consolidation Actions

1. **Studiato l'ambiente**: analizzate specifiche di `kaggriculture` (720 turni per stagione, 1.0s actTimeout) in ambiente isolato Python 3.12 (`.venv`).
2. **Implementation Plan**: prodotto ed approvato dall'utente prima dell'implementazione.
3. **Repository Hygiene & README**:
   - Creato `README.md` completo di guida all'installazione, comandi di test e struttura del repository.
   - Creato `.gitignore` e rimosse cache Python (`__pycache__`, `.pytest_cache`).
4. **Metric Precision & Disqualification Rate**:
   - Rinominata la metrica da "Invalid Action Rate" a **Disqualification Rate (%)** per riflettere con esattezza l'osservabile misurato dall'engine (percentuale di episodi conclusi con stato `INVALID` o `ERROR`).
5. **Exact Agent Latency Measurement**:
   - Implementato `TimedAgentWrapper` in `src/agricola/evaluation/runner.py` per misurare in modo preciso ed isolato la latenza di decisione dell'agente (**Agent Mean Turn Latency**), distinguendola dal tempo complessivo di simulazione dell'engine (**Simulation Mean Step Time**).
6. **Livello di Verifica & Test**:
   - Chiaramente distinti i test unitari (`GameState`, `ActionBuilder`, `agent` output), gli smoke/integration test (`test_short_simulation_smoke`, `test_build_and_run_submission_smoke`) e il benchmark completo E01 (30 episodi $\times$ 720 turni = 21.600 turni).

### Human intervention

- Approvazione dell'Implementation Plan.
- Feedback di revisione indipendente per consolidamento E01 (`docs/prompts/E01_review_feedback.md`).

### Outcome & Verification Evidence

- **Suite di Test (`pytest tests/`)**: 5/5 test superati con successo (3 unit test, 2 smoke integration test).
- **Bundling Submission (`scripts/build_submission.py`)**: `submission/submission.py` generato e verificato.
- **Benchmark Metric Summary E01 (`results/e01_baseline.json`)**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: 100.00% (30/30 episodi completati)
  - Disqualification Rate: 0.00% (0 episodi squalificati)
  - Overall Win Rate: 66.67% (20W / 0L / 10D)
  - Win Rate vs `pass`: 100.00% (Capitale medio: $3594.30)
  - Win Rate vs `random`: 100.00% (Capitale medio: $3610.50)
  - Draw Rate vs `starter`: 100.00% Draw / 0% Sconfitte (Capitale medio: $3531.60)
  - Agent Mean Turn Latency: **0.0142 ms/turno**
  - Simulation Mean Step Time: **3.69 ms/step**

### Method assessment

DEFINE: PASSED  
PLAN: PASSED  
BUILD: PASSED  
VERIFY: PASSED  
REVIEW: PASSED  
CONSOLIDATE: PASSED
