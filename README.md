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
| **E02** | `ROICropAgent` | Selezione dinamica coltura via ROI/giorno | `$5857.17 ± $132.37` | 100.00% Vittorie | Complete (`v0.2-e02-roicrop`) |
| **E03** | `MultiTileROIAgent` | Espansione coltivazione su cluster 2x2 (4 tile) | `$14682.47 ± $1164.33` | 100.00% Vittorie | Complete (`v0.3-e03-multitile`) |
| **E04** | `NWClusterROIAgent` | NW Scaling su cluster 3x3 (9 tile, 1 farmer) | `$11232.47 ± $661.26` | 100.00% Vittorie | **Shipped / Falsified** (`v0.4-e04-nw-scaling`) |

> *Nota metodologica: Le metriche del benchmark locale ($ capitale finale) ed il Kaggle Skill Rating misurano aspetti differenti dell'agente e non devono essere confrontati direttamente.*

---

## Stato del Repository

- **Baseline Tag**: `v0.1-e01-baseline` (main allineato con origin/main).
- **Tag E02**: `v0.2-e02-roicrop`.
- **Tag E03**: `v0.3-e03-multitile`.
- **Tag E04**: `v0.4-e04-nw-scaling` (consolidata falsificazione dell'ipotesi 4→9 single farmer).
- **Strategia Corrente**: `NWClusterROIAgent` in `src/agricola/strategy/nw_cluster_roi.py`.
- **Submission Standalone**: Generata in `submission/submission.py` e verificata.
- **Suite di Test**: 19/19 test automatizzati superati (`pytest tests/`).

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

### Iterazione E03 (Multi-Tile Scaling)
- [Implementation Plan E03](docs/plans/E03_Multi_Tile_Scaling.md)
- [Rapporto BUILD E03](docs/versions/E03_build_antigravity.md)
- [Rapporto VERIFY E03](docs/versions/E03_verify_antigravity.md)
- [Rapporto REVIEW E03](docs/versions/E03_review_antigravity.md)
- [Rapporto SHIP E03](docs/versions/E03_ship_antigravity.md)
- [Risultati Benchmark E03](results/e03_multi_tile.json)

### Iterazione E04 (Initial NW Scaling)
- [Competitive Gap Analysis E04-01](docs/experiments/E04-01_Competitive_Gap_Analysis.md)
- [Experimental Direction Decision E04-02](docs/experiments/E04-02_Experimental_Direction_Decision.md)
- [Implementation Plan E04](docs/plans/E04_Initial_NW_Scaling.md)
- [Rapporto VERIFY E04](docs/versions/E04_verify_antigravity.md)
- [Rapporto SHIP E04](docs/versions/E04_ship_antigravity.md)

### Registri di Progetto
- [Experiment Log](docs/EXPERIMENT_LOG.md)
- [Project State](docs/PROJECT_STATE.md)
- [New Session Restart Point](docs/NEW_SESSION.md)

---

## Installazione e Requisiti

Il progetto richiede Python 3.10+ (raccomandato **Python 3.12**).

```bash
# Creazione dell'ambiente virtuale con Python 3.12 (tramite venv)
python -m venv .venv

# Attivazione dell'ambiente virtuale (Windows PowerShell)
.\.venv\Scripts\activate

# Installazione delle dipendenze di sviluppo
pip install -e ".[dev]"
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
│   ├── NEW_SESSION.md
│   ├── plans/                  # Implementation plans (es. E03_Multi_Tile_Scaling.md)
│   ├── prompts/                # Prompt operativi del processo supervisionato
│   ├── screenshots/            # Evidenze visive delle submission Kaggle
│   └── versions/               # Documenti di versione e review analitiche
├── src/
│   └── agricola/               # Pacchetto sorgente dell'agente
│       ├── agent.py            # Entrypoint per Kaggle Environments
│       ├── core/               # State parsing (state.py) ed Action building (actions.py)
│       ├── baseline/           # CarrotLoopAgent (E01)
│       ├── strategy/           # ROICropAgent (E02), MultiTileROIAgent (E03)
│       └── evaluation/         # Runner CLI e latenza agente (runner.py)
├── submission/
│   └── submission.py           # Submission standalone per Kaggle
├── tests/                      # Suite di unit ed integration smoke test
├── scripts/                    # Scripts di bundling e benchmark
└── results/                    # Report JSON dei benchmark locali (e01_baseline.json, e02_roi_crop.json, e03_multi_tile.json)
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
.\.venv\Scripts\python.exe scripts/run_eval.py --opponents pass,random,starter --episodes 10 --output results/e03_multi_tile.json
```
