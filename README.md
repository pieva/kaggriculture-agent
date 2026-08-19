# Kaggriculture Agent

Agente competitivo per la competizione Kaggle **Kaggriculture** sviluppato attraverso un approccio iterativo e supervisionato.

## Overview del Progetto

Kaggriculture è una simulazione economica turn-based 1v1 gestita tramite il pacchetto `kaggle-environments`.
L'obiettivo è massimizzare il capitale finale (money/net worth) dell'azienda agricola al termine di una stagione di 30 giorni di gioco (720 turni).

### Stato Corrente: E01 Completata (`v0.1-e01-baseline`)
- **Baseline Agent**: `CarrotLoopAgent` (strategia deterministica basata sul ciclo di coltivazione e vendita delle carote).
- **Validazione Kaggle**: Submission caricata con successo sulla piattaforma Kaggle, ottenendo uno score iniziale sul leaderboard di **`600.0`**.
- **Verifica Osservabile Antigravity**: Esecuzione locale ed ispezione comportamentale documentata in [`docs/versions/E01_verify_antigravity.md`](docs/versions/E01_verify_antigravity.md).
- **Architettura Modulare**: Pacchetto Python in `src/agricola/`, bundler per Kaggle in `scripts/build_submission.py` e suite di test in `tests/`.
- **Benchmark Locale**: Runner CLI (`scripts/run_eval.py`) con report di metriche registrato in [`results/e01_baseline.json`](results/e01_baseline.json).

---

## Documentazione del Repository

- **Versioni e Analisi**: Disponibili sotto [`docs/versions/`](docs/versions/) (contiene [`E01_baseline.md`](docs/versions/E01_baseline.md) ed [`E01_verify_antigravity.md`](docs/versions/E01_verify_antigravity.md)).
- **Prompt Operativi**: Conservati sotto [`docs/prompts/`](docs/prompts/).
- **Registro Esperimenti**: Consultabile in [`docs/EXPERIMENT_LOG.md`](docs/EXPERIMENT_LOG.md) e [`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md).
- **Prossima Iterazione**: Il punto di ingresso per avviare la fase E02 è la prompt [`docs/prompts/E02-01_start.md`](docs/prompts/E02-01_start.md).

---

## Installazione e Requisiti

Il progetto richiede Python 3.10+ (raccomandato **Python 3.12**).

```bash
# Creazione dell'ambiente virtuale con Python 3.12 (tramite uv o venv)
uv venv --python 3.12 .venv

# Attivazione dell'ambiente virtuale (Windows PowerShell)
.\.venv\Scripts\activate

# Installazione delle dipendenze di sviluppo
uv pip install -e ".[dev]"
```

---

## Struttura del Repository

```text
kaggriculture-agent/
├── .venv/                      # Ambiente virtuale Python 3.12 (non versionato)
├── pyproject.toml              # Definizione dipendenze e configurazione pytest
├── README.md                   # Documentazione principale
├── .gitignore                  # File e directory ignorati da git
├── docs/                       # Documentazione del progetto e registro esperimenti
│   ├── EXPERIMENT_LOG.md
│   ├── PROJECT_STATE.md
│   ├── prompts/                # Prompt operativi (es. E02-01_start.md)
│   └── versions/               # Documenti di versione (E01_baseline.md, E01_verify_antigravity.md)
├── src/
│   └── agricola/               # Pacchetto sorgente dell'agente
│       ├── agent.py            # Entrypoint per Kaggle Environments
│       ├── core/
│       │   ├── state.py        # Wrapper GameState per l'observation
│       │   └── actions.py      # Builder ActionBuilder per le azioni
│       ├── baseline/
│       │   └── carrot_loop.py  # Baseline CarrotLoopAgent
│       └── evaluation/
│           └── runner.py       # Motore per simulazioni e benchmark
├── submission/
│   └── submission.py           # Submission standalone per Kaggle
├── tests/
│   ├── test_baseline.py        # Unit test per stato e azioni + smoke test simulazione
│   └── test_submission.py      # Integration test per il bundle di submission
├── scripts/
│   ├── build_submission.py     # Script di bundling per generare submission.py
│   └── run_eval.py             # CLI per la valutazione locale benchmark
└── results/
    └── e01_baseline.json       # Report metriche JSON del benchmark E01
```

---

## Esecuzione dei Test e Valutazione

### 1. Esecuzione dei Test Automatizzati
```bash
.\.venv\Scripts\pytest tests/
```

### 2. Generazione del Bundle di Submission per Kaggle
```bash
.\.venv\Scripts\python.exe scripts/build_submission.py
```

### 3. Esecuzione del Benchmark Locale E01
```bash
.\.venv\Scripts\python.exe scripts/run_eval.py --opponents pass,random,starter --episodes 10 --output results/e01_baseline.json
```
