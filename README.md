# Kaggriculture Agent

Agente competitivo per la competizione Kaggle **Kaggriculture** sviluppato attraverso un approccio iterativo e supervisionato.

## Overview del Progetto

Kaggriculture è una simulazione economica turn-based 1v1 gestita tramite il pacchetto `kaggle-environments`.
L'obiettivo è massimizzare il capitale finale (money/net worth) dell'azienda agricola al termine di una stagione di 30 giorni di gioco (720 turni).

Il progetto adotta rigorosamente il ciclo di sviluppo supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

---

## Tabella delle Iterazioni Sperimentali

| Esperimento | Strategia | Variabile Modificata | Mean Final Money (Locale) | Win Rate vs `starter` | Validazione Kaggle |
| :--- | :--- | :--- | ---: | ---: | :--- |
| **E01** | `CarrotLoopAgent` | Baseline: monocultura statica `CARROT` | `$3567.63 ± $205.38` | 0.00% (100% Draw) | Validata (`v0.1-e01-baseline`) |
| **E02** | `ROICropAgent` | Selezione dinamica coltura via ROI/giorno | **`$5857.17 ± $132.37`** | **100.00% Vittorie** | **Complete** (rating iniziale `600.0`) |

> *Nota metodologica: Le metriche del benchmark locale ($ capitale finale) ed il Kaggle Skill Rating misurano aspetti differenti dell'agente e non devono essere confrontati direttamente.*

---

## Stato del Repository

- **Baseline Tag**: `v0.1-e01-baseline` (main allineato con `origin/main`).
- **Iterazione E02**: Completata, verificata, revisionata e consolidata (pronta per il tag `v0.2-e02-roicrop`).
- **Strategia Corrente**: `ROICropAgent` in `src/agricola/strategy/roi_crop.py`.
- **Submission Standalone**: Generata in `submission/submission.py` e verificata con successo su Kaggle.
- **Suite di Test**: 7/7 test automatizzati superati (`pytest tests/`).

---

## Documentazione ed Evidenze

Le evidenze analitiche e quantitative per ciascuna iterazione sono disponibili sotto `docs/`:

### Iterazione E01 (Baseline)
- [Documento di Baseline E01](docs/versions/E01_baseline.md)
- [Verifica Osservabile E01](docs/versions/E01_verify_antigravity.md)
- [Risultati Benchmark E01](results/e01_baseline.json)

### Iterazione E02 (ROI Crop Selection)
- [Implementation Plan E02](docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md)
- [Rapporto BUILD E02](docs/versions/E02_build_antigravity.md)
- [Rapporto VERIFY REVIEW E02](docs/versions/E02_verify_review_antigravity.md)
- [Analisi Osservabile della Simulazione E02](docs/versions/E02_simulation_analysis.md)
- [Rapporto SHIP REVIEW E02](docs/versions/E02_ship_review_antigravity.md)
- [Risultati Benchmark E02](results/e02_roi_crop.json)

### Registri di Progetto
- [Experiment Log](docs/EXPERIMENT_LOG.md)
- [Project State](docs/PROJECT_STATE.md)

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
│   ├── plans/                  # Implementation plans (es. E02_Dynamic_Crop_Selection_&_ROI_Scaling.md)
│   ├── prompts/                # Prompt operativi del processo supervisionato
│   ├── screenshots/            # Evidenze visive delle submission Kaggle
│   └── versions/               # Documenti di versione e review analitiche
├── src/
│   └── agricola/               # Pacchetto sorgente dell'agente
│       ├── agent.py            # Entrypoint per Kaggle Environments
│       ├── core/               # State parsing (state.py) ed Action building (actions.py)
│       ├── baseline/           # CarrotLoopAgent (E01)
│       ├── strategy/           # ROICropAgent (E02)
│       └── evaluation/         # Runner CLI e latenza agente (runner.py)
├── submission/
│   └── submission.py           # Submission standalone per Kaggle
├── tests/                      # Suite di unit ed integration smoke test
├── scripts/                    # Scripts di bundling e benchmark
└── results/                    # Report JSON dei benchmark locali (e01_baseline.json, e02_roi_crop.json)
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

### 3. Esecuzione del Benchmark Locale
```bash
.\.venv\Scripts\python.exe scripts/run_eval.py --opponents pass,random,starter --episodes 10 --output results/e02_roi_crop.json
```
