# E03 — Multi-Tile Scaling — SHIP

Le fasi precedenti di E03 sono completate e approvate.

Metodo:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Esiti REVIEW:

- Experimental Integrity: `PASSED`
- Operational Readiness: `READY FOR SHIP`
- Economic Hypothesis: `SUPPORTED`

Benchmark E03:

- Mean Final Money: `$14682.47`
- Sample Std Dev (`ddof=1`): `$1164.33`
- Median Final Money: `$14146.00`
- Overall Win Rate: `100.00%`
- Win Rate vs `starter`: `100.00%`
- Completion Rate: `100.00%`
- Disqualification Rate: `0.00%`
- Agent Mean Turn Latency: `0.0698 ms/turno`

Confronto E02 → E03:

- `$5857.17 → $14682.47`
- `+$8825.30`
- `+150.68%`

Procedi ora esclusivamente con la fase:

# SHIP

## 1. Verifica finale della submission standalone

Verifica:

`submission/submission.py`

Conferma che:

- includa `MultiTileROIAgent`;
- sia self-contained;
- non dipenda da import locali;
- utilizzi il movement format corretto;
- rappresenti esattamente il codice validato durante VERIFY;
- non contenga modifiche sperimentali successive alla REVIEW.

Se necessario, rigenera il file utilizzando esclusivamente:

`scripts/build_submission.py`

senza modificare la strategia.

---

## 2. Test finali pre-SHIP

Esegui la suite completa:

```powershell
.\.venv\Scripts\pytest
```

Richiedi:

- 0 failure;
- nessuna regressione;
- smoke test submission superato.

Se un test fallisce:

**STOP**

e non caricare nulla su Kaggle.

---

## 3. Validazione locale finale della submission

Esegui una validazione smoke della submission standalone nell'ambiente Kaggriculture.

Verifica almeno:

- import/esecuzione corretta;
- azioni valide;
- movimento funzionante;
- nessuna disqualification immediata;
- utilizzo effettivo del comportamento multi-tile.

Non eseguire tuning.

---

## 4. Upload Kaggle

Solo se tutte le verifiche precedenti sono superate:

carica realmente:

`submission/submission.py`

nella competizione Kaggriculture.

Documenta:

- data/ora dell'upload;
- nome/versione della submission;
- stato Kaggle;
- eventuale messaggio di errore;
- Skill Rating iniziale osservato, se disponibile.

Attendi che lo stato della submission risulti almeno:

`Complete`

prima di considerare SHIP completato.

---

## 5. Evidenze

Salva screenshot coerenti con la convenzione del progetto in:

`docs/screenshots/`

Usa nomi progressivi E03, ad esempio:

- `E03-001_kaggle_submission_ready.png`
- `E03-002_kaggle_submission_successful.png`
- eventuale screenshot del rating iniziale

Non sovrascrivere evidenze E01/E02.

---

## 6. Documentazione SHIP

Crea:

`docs/versions/E03_ship_antigravity.md`

Documenta:

- stato pre-SHIP;
- test finali;
- validazione submission;
- upload Kaggle;
- stato finale;
- rating iniziale osservato;
- eventuali osservazioni;
- distinzione tra benchmark locale e Skill Rating Kaggle.

Mantieni esplicitamente la formulazione:

> Il benchmark locale e il Kaggle Skill Rating misurano aspetti differenti e non devono essere confrontati direttamente.

---

## 7. Valutazione SHIP

Classifica:

- `PASSED`
- `PASSED WITH OBSERVATIONS`
- `FAILED`

Utilizza come criterio minimo:

- submission caricata realmente;
- status Kaggle `Complete`;
- nessuna disqualification;
- nessun errore tecnico di packaging/esecuzione.

Il rating iniziale Kaggle non determina da solo il successo o il fallimento dello SHIP.

---

## 8. Git

Dopo il completamento dello SHIP mostra:

```powershell
git status --short
```

Non eseguire ancora commit o tag.

---

# STOP

NON modificare la strategia.

NON fare tuning dopo aver osservato il rating Kaggle.

NON introdurre E04.

NON eseguire commit.

NON creare tag.

Al termine mostra soltanto:

1. test finali;
2. validazione submission;
3. esito upload Kaggle;
4. status Kaggle;
5. Skill Rating iniziale osservato;
6. valutazione SHIP;
7. screenshot prodotti;
8. documento SHIP creato;
9. stato Git.

Attendi la revisione finale prima del consolidamento, commit e tag di E03.