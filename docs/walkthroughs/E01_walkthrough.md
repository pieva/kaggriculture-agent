# Walkthrough - E01 Baseline & Environment Setup

L'iterazione **E01** per la competizione Kaggle **Kaggriculture** è stata completata con successo. L'agente baseline è stato realizzato, l'infrastruttura di simulazione e benchmark locale è operativa e la submission per Kaggle è stata impacchettata e verificata.

---

## 1. Struttura del Repository Realizzata

Il progetto segue una struttura modulare, orientata all'estensibilità e ai test automatizzati:

```text
kaggriculture-agent/
├── .venv/                      # Ambiente Python 3.12 isolato con kaggle-environments
├── pyproject.toml              # Dipendenze di progetto e configurazione pytest
├── README.md                   # Documentazione di base del progetto
├── docs/
│   ├── EXPERIMENT_LOG.md       # Log dell'esperimento E01 aggiornato
│   ├── PROJECT_STATE.md        # Stato corrente del progetto aggiornato
│   └── prompts/
│       └── E01_define_plan.md
├── src/
│   └── agricola/               # Pacchetto principale dell'agente AI
│       ├── __init__.py
│       ├── agent.py            # Entrypoint per Kaggle Environments
│       ├── core/
│       │   ├── __init__.py
│       │   ├── state.py        # GameState wrapper per il parsing dell'observation
│       │   └── actions.py      # ActionBuilder per la generazione sicura delle azioni
│       ├── baseline/
│       │   ├── __init__.py
│       │   └── carrot_loop.py  # Baseline CarrotLoopAgent
│       └── evaluation/
│           ├── __init__.py
│           └── runner.py       # Motore di valutazione multi-episodio
├── submission/
│   └── submission.py           # Submission standalone per Kaggle
├── tests/
│   ├── __init__.py
│   ├── test_baseline.py        # Test unitari per GameState, ActionBuilder ed agent
│   └── test_submission.py      # Test d'integrazione sul file di submission
├── scripts/
│   ├── build_submission.py     # Bundler standalone per Kaggle
│   └── run_eval.py             # CLI per i benchmark di valutazione locale
└── results/
    └── e01_baseline.json       # Risultati in JSON della prima simulazione benchmark
```

---

## 2. Componenti Realizzati

### `src/agricola/core/state.py` ([`state.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/core/state.py))
Classe `GameState` che incapsula ed estrae in modo sicuro le informazioni dal dizionario di observation:
- Gestione della posizione del contadino `(x, y)` e dello stato delle caselle (`tiles`).
- Interrogazione del capitale liquido (`money`), del magazzino (`shed`), dei semi (`seeds`) e del mercato (`market_prices`).

### `src/agricola/core/actions.py` ([`actions.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/core/actions.py))
Classe `ActionBuilder` che garantisce la costruzione di dizionari di azione conformi allo schema richiesto (`farmer`, `hands`, `market`).

### `src/agricola/baseline/carrot_loop.py` ([`carrot_loop.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/baseline/carrot_loop.py))
Baseline semplice e deterministica (`CarrotLoopAgent`):
1. **Mercato**: vende le carote raccolte nel magazzino e compra 1 seme di carota se non posseduto e con liquidità sufficiente.
2. **Terreno**: semina, annaffia o raccoglie carote sulla casella corrente del contadino.

### `scripts/build_submission.py` ([`build_submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/build_submission.py))
Genera il file standalone [`submission/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/submission/submission.py) unificando tutti i moduli senza richiedere dipendenze locali.

### `scripts/run_eval.py` ([`run_eval.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/run_eval.py)) & `src/agricola/evaluation/runner.py` ([`runner.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/evaluation/runner.py))
Infrastruttura CLI e motore di valutazione per eseguire batterie di simulazioni (N partite con scambio di turno tra Player 0 e Player 1) contro avversari di riferimento (`pass`, `random`, `starter`) e registrare le metriche in formato JSON.

---

## 3. Risultati della Valutazione Locale (Benchmark E01)

Abbiamo eseguito **30 episodi** completi (720 turni per partita = 21.600 turni totali) salvando le metriche in [`results/e01_baseline.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e01_baseline.json).

| Metrica | Risultato E01 | Target E01 | Status |
| :--- | :---: | :---: | :---: |
| **Completion Rate (%)** | **100.00%** (30/30) | 100% | ✅ PASS |
| **Invalid Action Rate (%)** | **0.00%** | 0.0% | ✅ PASS |
| **Win Rate vs `pass`** | **100.00%** (10/10) | 100% | ✅ PASS |
| **Win Rate vs `random`** | **100.00%** (10/10) | 100% | ✅ PASS |
| **Draw Rate vs `starter`** | **100.00%** (0% Loss) | $\ge 50\%$ | ✅ PASS |
| **Mean Final Money ($)** | **$3545.03 ± $194.05** | $> 3500.0 \$$ | ✅ PASS |
| **Mean Latency (ms/turno)** | **3.84 ms** | $< 10 \text{ ms}$ | ✅ PASS |

### Dettaglio per Avversario
- **vs `pass`**: 10 vittorie su 10, media capitale finale **$3594.30**.
- **vs `random`**: 10 vittorie su 10, media capitale finale **$3509.20**.
- **vs `starter`**: 10 pareggi su 10 (0 sconfitte), media capitale finale **$3531.60** (le due strategie eseguono il loop di carote sulla singola casella iniziale).

---

## 4. Validazione dei Test Automatizzati

Abbiamo eseguito la suite di test con `pytest`:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\pietr\Projects\kaggriculture-agent
configfile: pyproject.toml
collected 5 items

tests\test_baseline.py ....                                              [ 80%]
tests\test_submission.py .                                               [100%]

============================== 5 passed in 1.95s ==============================
```

---

## 5. Prossimi Passi (E02)

1. **Ottimizzazione Economica & Colture Multi-Tile**: Espandere l'agente per gestire colture a maggior resa (es. Tomati, Fragole, Meloni) ed effettuare la semina su più caselle adiacenti.
2. **Pianificazione dei Movimenti**: Aggiungere un modulo di pathfinding/navigazione del contadino sulla griglia.
3. **Gestione Dinamica del Mercato**: Tracciare le fluttuazioni dei prezzi nel tempo per vendere nei momenti di massimo margine.
