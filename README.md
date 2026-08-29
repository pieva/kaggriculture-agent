# Kaggriculture Agent

Agente economico per la competizione Kaggle **Kaggriculture** sviluppato attraverso un approccio rigoroso, empirico e supervisionato.

## Overview del Progetto

Kaggriculture è una simulazione economica turn-based 1v1 gestita tramite il pacchetto `kaggle-environments`.
L'obiettivo è massimizzare il capitale finale (money/net worth) dell'azienda agricola al termine di una stagione di 30 giorni di gioco (720 turni).

### Obiettivi Competitivi
- **Target hard corrente (E12-X1.12):** **$80,000.00** su seed `0` e `421521921`.
- **Baseline locale corrente:** **$42,491 / $48,313**.
- **Riferimento competitivo:** `truebelief` episodio `101294736`, seed `421521921`, **$86,297**.
- **Stato Kaggle:** X1.12 caricata manualmente, risultato esterno pending.

Il progetto adotta rigorosamente il ciclo di sviluppo supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

---

## Metodologia & Correzione della Provenance (E11-R0 ... E11-R3)

Durante la serie **E11**, un audit metodologico (E11-R0 ... E11-R2) ha evidenziato che alcuni dati storici di espansione erano derivati da metriche sintetiche non riproducibili sul codice macchina. Il repository è stato interamente bonificato:

1. **Config Isolation Restored (E11-R0):** Isolamento totale delle configurazioni e ripristino delle factory benchmark indipendenti.
2. **Provenance Audit (E11-R2):** Ritirati i dati sintetici e introdotto il verificatore SHA-256 (`scripts/verify_e11_run_provenance.py`).
3. **Verified Baseline (E11-R3 / E11-VB1):** Stabilita la baseline macchina autorevole **E11-VB1** ($429.00 Mean Money su 30 episodi verificati).
4. **Append-Only Run Directories:** Tutti i run di benchmark generano directory append-only immutabili con snapshot `config.json`, `episodes.json` e fingerprint SHA-256.

---

## Tabella delle Iterazioni Sperimentali

| Versione | Architettura / Idee Chiave | Footprint / Land | Mean Local Money | Ruolo / Stato Sperimentale |
| :--- | :--- | :--- | ---: | :--- |
| **E01** | Monocultura statica `CARROT` | 1 tile (Q0) | `$3,567.63` | Riferimento storico (`v0.1-e01-baseline`) |
| **E02** | Selezione dinamica ROI/giorno | 1 tile (Q0) | `$5,857.17` | Riferimento storico (`v0.2-e02-roicrop`) |
| **E03** | Cluster 2x2 multi-tile | 4 tile (Q0) | `$14,682.47` | Riferimento storico (`v0.3-e03-multitile`) |
| **E04** | Cluster 3x3 NW (Single Farmer) | 9 tile (Q0) | `$11,232.47` | Falsificato — sovraccarico farmer (`v0.4-e04-nw-scaling`) |
| **E05** | Multi-Worker Scaling (1 Farmer + 1 Hand) | 9 tile (Q0) | `$21,568.93` | Validato su Kaggle (Score: 439.7) |
| **E06** | Water-First Priority Scheduling | 9 tile (Q0) | **`$25,847.00`** | **Sanity Reference Storico** (`v0.6-e06-water-first`) |
| **E07–E10** | Esperimenti espansione, livestock e capitale | 9–40 tile | Variable | Esperimenti storici intermedi |
| **E11-VB1** | Baseline macchina verificata post-audit | 50 tile (2Q) | `$429.00` | Baseline autorevole verificata SHA-256 |
| **E11-X1.2** | Ripristino core E06 + Multi-HIRE | 17 tile (2Q) | `$7,476.20` | Trattamento verificato localmente |
| **E11-X1.3-A** | Replica 1× EPU (E06 Replicated) | 9 tile (1Q) | **`$26,888.40`** | **Controllo Positivo Verificato (100% exact E06 match)** |
| **E11-X1.3-B** | **Scaling 2× EPU (Causal Q1 Buy)** | **18 tile (2Q)** | **`$28,727.40`** | **Trattamento Corrente / Validazione Esterna Kaggle** |
| **E11-X1.3-C** | Scaling 3× EPU | 27 tile (3Q) | — | *Bloccato (Stop Gate B in vigore su efficienza scaling)* |

> *Nota: $25,847.00 rappresenta il risultato verificato di E06 sul diagnostico Seed 0 vs Pass. $26,888.40 (X1.3-A) rappresenta la replica verificata su 5 episodi.*

---

## Architettura EPU (Elementary Productive Unit) & E11-X1.3

L'esperimento **E11-X1.3** riorganizza l'agente considerando **E06** come un'**Unità Produttiva Elementare (EPU)** compatta:
- **EPU Elementare (9 tile):** 4 tile Farmer + 5 tile Hand 1 in configurazione Water-First NW Cluster.
- **Principio di Espansione:** L'acquisto di terreno (Q1, $1,000) non avviene a giorno fisso, ma come conseguenza diretta del surplus di cassa generato dall'EPU1 ($\ge \$1,435.00$ capitale operativo di sicurezza).
- **Attivazione EPU2 (18 tile):** L'acquisto di Q1 al Giorno 14 sblocca EPU2 (9 tile NE in Q1) gestita da Hand 2 (3 lavoratori totali), portando il footprint a 18 tile attive.

### Risultati Verificati E11-X1.3:
- **X1.3-A (1× EPU 9t):** Mean Money **$26,888.40** (Gate A Passed).
- **X1.3-B (2× EPU 18t):** Mean Money **$28,727.40** (Scaling Ratio 1.07×, Scaling Efficiency 53.4%).
- **Stop Gate B:** Attivato su efficienza locale ($53.4\% < 60.0\%$). La submission **X1.3-B** serve ad acquisire evidenza competitiva esterna su Kaggle prima di apportare ulteriori modifiche alla strategia.

---

## Stato del Repository & Artifacts

- **Submission File Standalone:** `submission/submission.py` (generato automaticamente via `scripts/build_submission.py`).
- **Trattamento Inserito in Submission:** `ProductiveMassROIAgent` in modalita `E12_TRUEBELIEF_ENGINE_X112` (X1.12 Q0+Q1, 7 Cow + 4 Sheep).
- **Benchmark locale X1.12:** seed `0` `$42,491`; seed `421521921` `$48,313`; 80k gate FAIL.
- **Stato Kaggle X1.12:** uploaded manually; external result pending.
- **Correzione modello post-upload:** `Q0+Q1 only` e `7 Cow + 4 Sheep` sono evidenze/reference della candidate X1.12, non vincoli hard permanenti; il prossimo BUILD deve trattare Q2 e livestock come decisioni marginal-value + capacity-gated.
- **Spec canonica del modello:** `docs/MODEL_SPEC.md`.
- **Verifica candidate:** `results/e12/x112/submission_candidate_verification.json`.

---

## Ambiente Python

La fonte canonica delle dipendenze è `pyproject.toml`. La directory `.venv` è un artifact locale disposable: non è fonte di verità e, se diventa incoerente, deve essere eliminata e ricreata dalla configurazione versionata del repository.

Versione validata:

- Python `3.12.13`
- `kaggle-environments==1.32.7`
- progetto installato in editable mode: `kaggriculture-agent==0.1.0`

`pyproject.toml` dichiara `requires-python = ">=3.10,<3.14"` perché la ricostruzione con Python `3.14.4` ha fallito sulla dipendenza transitive `pygame` richiesta da `kaggle-environments`.

### Creazione ambiente

PowerShell:

```powershell
.\scripts\setup_env.ps1 -Recreate
```

Comandi manuali equivalenti, usando un Python 3.12 disponibile:

```powershell
<PYTHON_3_12>\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .[dev]
```

### Verifica ambiente

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import kaggle_environments, agricola; print(kaggle_environments.__version__)"
.\.venv\Scripts\python.exe -m py_compile src\agricola\core\state.py src\agricola\core\actions.py src\agricola\agent.py src\agricola\strategy\productive_mass_roi.py
.\.venv\Scripts\python.exe -m pytest tests\test_hire_nw_cluster.py tests\test_water_first_hire_nw_cluster.py tests\test_submission_behavioral_equivalence.py
.\.venv\Scripts\python.exe scripts\verify_x112_submission_candidate.py
```

Un warning su `.pytest_cache` non è una failure se i test passano.

### Environment discipline per agenti

Antigravity, Codex, Copilot e altri agenti devono seguire:

`Repository configuration -> .venv -> verification`

Regole:

1. usare la `.venv` canonica del repository;
2. non trattare pacchetti installati localmente come fonte di verità;
3. non eseguire installazioni permanenti ad hoc senza aggiornare la configurazione versionata;
4. prima di aggiungere o modificare una dipendenza, verificare la configurazione esistente, motivare la modifica, aggiornare il file dichiarativo ed eseguire `pip check` e test;
5. non cambiare versione Python o dependency set silenziosamente;
6. segnalare qualsiasi incompatibilità tra ambiente e repository.

## Installazione ed Esecuzione

```bash
# Attivazione ambiente virtuale (Windows PowerShell)
.\.venv\Scripts\activate

# Esecuzione della suite completa di unit test
.\.venv\Scripts\pytest tests/

# Rigenerazione del file di submission standalone per Kaggle
.\.venv\Scripts\python.exe scripts/build_submission.py

# Verifica provenance di un run di benchmark
.\.venv\Scripts\python.exe scripts/verify_e11_run_provenance.py results/e11/E11-X1.3-B-20260827-100010
```

---

## Registri di Progetto & Versioning

- [Documento di Versione E11-X1.3-B](docs/versions/E11_X1_3_B_kaggle_external_validation.md)
- [Documento di Versione E11-X1.3](docs/versions/E11_X1_3_e06_productive_unit_replication_scaling.md)
- [Documento di Versione E11-VB1 Baseline](docs/versions/E11_R3_verified_baseline_reestablishment.md)
- [Experiment Log Completo](docs/EXPERIMENT_LOG.md)
- [Project State](docs/PROJECT_STATE.md)
- [New Session Restart Point](docs/NEW_SESSION.md)
