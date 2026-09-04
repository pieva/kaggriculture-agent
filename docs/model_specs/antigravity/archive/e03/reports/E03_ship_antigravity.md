# Rapporto SHIP — E03: Multi-Tile Scaling

## 1. Stato Definitivo della Submission Standalone

- **File della Submission**: [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py)
- **Codice Contenuto**: `MultiTileROIAgent` operante su cluster 2x2 `{(4,4), (4,3), (3,4), (3,3)}`.
- **Verifica di Autonomia**: Self-contained, 0 import locali, include `GameState`, `CROPS`, `ActionBuilder` e il fix delle azioni direzionali (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
- **Invarianza**: Rigenerata tramite `scripts/build_submission.py` e verificata priva di modifiche sperimentali post-REVIEW.

---

## 2. Test Pre-SHIP

Suite di test eseguita tramite `pytest`:

```bash
.\.venv\Scripts\pytest
```

- **Risultato**: `14 passed in 2.78s` (0 errori, 0 regressioni).
- **Smoke test submission**: Superato.

---

## 3. Validazione Locale dell'Eseguibile

Smoke match locale da 48 step nell'engine `kaggle_environments`:
- **Stato finale**: `DONE`
- **Capitale maturato**: `$2680.00`
- **Esito**: Esecuzione valida, movimento direzionale confermato, nessuna disqualificazione.

---

## 4. Evidenza Kaggle E03

L'invio reale della submission standalone `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py` sulla piattaforma Kaggle è stato completato e verificato.

- **Evidenza Visiva Persistente**: [`data/screenshots/E03-001_kaggle_submission_successful.png`](file:///c:/Users/pietr/Projects/kaggriculture-agent/data/screenshots/E03-001_kaggle_submission_successful.png)
- **Nome File Submission**: `submission.py`
- **Descrizione Registrata**: `E03 supervised iteration: Multi-Tile ROI Agent 2x2 cluster`
- **Status Kaggle**: **`Complete`**
- **Skill Rating Iniziale E03 Osservato**: **`600.0`**
- **Skill Rating E02 Osservato (nello stesso screenshot)**: `285.1`

---

## 5. Metodologia di Interpretazione dei Risultati

> **Distinzione Metodologica Fondamentale**:  
> Il benchmark locale e il Kaggle Skill Rating misurano aspetti differenti e non devono essere confrontati direttamente.

- **Skill Rating Iniziale (`600.0`)**: Valore di default assegnato dalla piattaforma Kaggle al momento dell'ingresso nel sistema competitivo; non costituisce prova di superiorità o inferiorità competitiva.
- **Rating Competitivo E03**: Rimanente **IN OSSERVAZIONE** in attesa che l'agente disputi il pool di episodi sul leaderboard globale.
- **Benchmark Locale (`experiments/archive/e03/artifacts/multi_tile.json`)**: Dimostra la capacità produttiva di laboratorio ($14,682.47 vs E02 $5,857.17, +150.68%) in condizioni controllate contro agenti di riferimento (`pass`, `random`, `starter`).

---

## 6. SHIP Assessment

### Valutazione Rilasciata: **`PASSED`**

**Motivazione Rigorosa**:  
- Submission realmente caricata su Kaggle;
- Status della submission sulla piattaforma: **`Complete`**;
- Packaging standalone e dipendenze totalmente validati;
- 100% di successo nella suite di test locale (14/14 passed);
- Smoke test di esecuzione locale superato con status `DONE`.
