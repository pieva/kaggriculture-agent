# E08-06 — SHIP / Repository Closure

## Contesto

L'esperimento **E08 — Productive Scale Optimization** è stato completato dal punto di vista sperimentale e documentale:

- DEFINE completato;
- PLAN completato;
- BUILD completato;
- VERIFY completato con ipotesi falsificata;
- REVIEW completata;
- REVIEW Correction Pass completata;
- report di SHIP/closure creato.

Decisioni consolidate:

- **E08 è FALSIFICATO**;
- **E08 NON è candidato a Kaggle**;
- il codice e i risultati E07/E08 devono essere preservati come evidenza sperimentale;
- l'entrypoint competitivo deve restare sulla baseline attiva **E06 `WaterFirstHIRENWClusterROIAgent`**;
- NON deve essere inviata alcuna submission Kaggle;
- dopo la chiusura repository si potrà iniziare **E09-01 DEFINE — Livestock Subsystem Ablation**.

Il precedente SHIP ha completato la chiusura documentale, ma il repository presenta ancora modifiche e file untracked. Questa fase serve esclusivamente a completare la **repository closure E08**.

---

# Obiettivo

Portare il repository a uno stato:

> **E08 CLOSED + Git working tree clean**

preservando integralmente il patrimonio sperimentale E07/E08 e mantenendo E06 come entrypoint competitivo.

Questa fase NON deve modificare la strategia.

NON iniziare E09.

---

# S1 — Verifica entrypoint competitivo

Controlla:

`src/agricola/agent.py`

Conferma che l'entrypoint utilizzato per la submission attiva punti ancora a:

> **E06 `WaterFirstHIRENWClusterROIAgent`**

Verifica inoltre che la generazione della submission non abbia accidentalmente promosso E07 o E08 come agente attivo.

Se E06 è già correttamente attivo:

> NON modificare l'entrypoint.

Se trovi E07/E08 attivo per errore:

> fermati e segnala il problema prima di effettuare commit.

---

# S2 — Audit finale dei file E07/E08

Esegui:

```powershell
git status --short
```

Esamina tutti i file modificati e untracked.

L'obiettivo è includere nel commit finale tutto il patrimonio sperimentale pertinente E07/E08, inclusi quando presenti:

- `docs/plans/`
- `docs/prompts/`
- `docs/versions/`
- `results/e07_competitive_baseline.json`
- `results/e08_productive_scale.json`
- benchmark script E07/E08;
- strategia `hybrid_livestock_cluster_roi.py`;
- test E07/E08;
- modifiche necessarie a core/actions/state;
- `scripts/build_submission.py`;
- `submission/submission.py`;
- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`.

## Scratch

Esamina `scratch/`.

NON committare automaticamente file temporanei, log o diagnostici usa-e-getta.

Mantieni nel repository soltanto elementi di `scratch/` che abbiano un valore permanente e documentato.

Se sono esclusivamente artefatti temporanei:

- lasciali fuori dal commit;
- se appropriato secondo le convenzioni esistenti del repository, rimuovili o assicurati che siano ignorati;
- non introdurre modifiche invasive a `.gitignore` senza necessità.

---

# S3 — Verifica documentale finale

Controlla che esistano e siano coerenti almeno i deliverable E08:

- `docs/versions/E08_define_productive_scale.md`
- `docs/plans/E08_Productive_Scale_Optimization.md`
- `docs/versions/E08_plan_productive_scale.md`
- `docs/versions/E08_build_productive_scale.md`
- `docs/versions/E08_verify_functional_utilization.md`
- `docs/versions/E08_verify_local_performance.md`
- `docs/versions/E08_verify_competitive_evidence.md`
- `docs/versions/E08_review_productive_scale.md`
- `docs/versions/E08_review_corrections.md`
- `docs/versions/E08_ship_productive_scale.md`

Preserva anche i prompt operativi E08-01...E08-05B presenti nel repository.

Non riscrivere la documentazione salvo errori materiali evidenti.

Conferma in `PROJECT_STATE.md` e `NEW_SESSION.md`:

- E08 CLOSED;
- E08 falsificato;
- E08 non candidato a Kaggle;
- E06 baseline competitiva attiva;
- prossimo esperimento previsto E09, ma **non ancora iniziato**.

---

# S4 — Test finale

Esegui l'intera suite:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

Criterio:

> **100% test pass**

Registra:

- numero test;
- passed;
- failed;
- durata.

Se anche un solo test fallisce:

> **FERMATI. NON COMMITTARE.**

Riporta il problema e attendi supervisione.

---

# S5 — Submission parity

Rigenera la submission soltanto tramite il normale processo del repository:

```powershell
.venv\Scripts\python.exe scripts/build_submission.py
```

Poi esegui almeno:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_submission.py
```

Conferma:

1. build completata;
2. test submission passato;
3. entrypoint finale ancora E06.

NON inviare la submission a Kaggle.

NON aprire browser.

NON tentare autenticazioni Kaggle.

---

# S6 — Diff finale prima del commit

Esegui:

```powershell
git status --short
git diff --stat
git diff --check
```

`git diff --check` non deve riportare errori di whitespace significativi.

Esamina il diff per assicurarti che:

- non siano presenti credenziali;
- non siano presenti file temporanei indesiderati;
- non sia stato promosso E08 nell'entrypoint;
- non siano presenti modifiche E09;
- siano preservate le evidenze E07/E08.

---

# S7 — Commit

Solo se S1–S6 sono tutti superati:

aggiungi al commit tutti i file permanenti pertinenti alla chiusura E07/E08.

Usa un messaggio di commit chiaro, ad esempio:

```powershell
git commit -m "Close E08 productive scale experiment"
```

Il commit deve preservare anche il lavoro E07 ancora pendente che costituisce la base sperimentale necessaria per comprendere E08.

NON creare commit separati artificialmente se tutto il lavoro pendente appartiene alla stessa sequenza sperimentale E07→E08.

---

# S8 — Push

Dopo il commit:

```powershell
git push origin main
```

Se il push fallisce:

- non tentare workaround distruttivi;
- riporta l'errore;
- non creare il tag remoto finché `main` non è stato correttamente pubblicato.

---

# S9 — Tag E08

Solo dopo commit e push riusciti, crea un tag annotato coerente con la convenzione esistente del repository.

Prima verifica i tag:

```powershell
git tag --list
```

Usa il naming coerente con i tag precedenti.

Se la convenzione corrente è `v0.x-eNN-*`, usa:

```powershell
git tag -a v0.8-e08-productive-scale -m "E08 Productive Scale Optimization closed — hypothesis falsified"
git push origin v0.8-e08-productive-scale
```

Se esiste una convenzione differente nel repository, rispettala e documenta il nome effettivamente utilizzato.

Il tag deve rappresentare:

> **chiusura di un esperimento falsificato**

e NON una promozione di E08 a baseline competitiva.

---

# S10 — Working tree clean

Dopo commit, push e tag esegui:

```powershell
git status
git log -1 --oneline
git tag --list
```

Criterio finale:

```text
nothing to commit, working tree clean
```

Se rimangono file untracked:

- determina se sono temporanei;
- non dichiarare la chiusura completa finché il loro stato non è spiegato/risolto.

---

# Vincoli assoluti

Durante questa fase:

- NON modificare la strategia E06;
- NON modificare E07/E08 per migliorarne le performance;
- NON iniziare E09;
- NON creare codice E09;
- NON eseguire benchmark E09;
- NON inviare submission Kaggle;
- NON cambiare la baseline competitiva attiva;
- NON cancellare le evidenze di esperimenti falsificati.

---

# Output finale richiesto

Restituisci:

## E08-06 — SHIP / Repository Closure

### 1. Entrypoint competitivo
Conferma agente attivo.

### 2. Test finali
- full suite;
- submission test.

### 3. Patrimonio E07/E08 preservato
Sintesi dei file permanenti inclusi.

### 4. Scratch / file temporanei
Cosa è stato escluso, rimosso o ignorato.

### 5. Diff pre-commit
Esito:
- `git status --short`
- `git diff --stat`
- `git diff --check`

### 6. Commit
- hash;
- messaggio.

### 7. Push
Esito.

### 8. Tag
- nome;
- messaggio;
- push remoto.

### 9. Stato finale repository
Riporta:
- `git status`
- `git log -1 --oneline`

### 10. Decisione finale

Usa una sola:

- `E08 CLOSED — REPOSITORY CLEAN — READY FOR E09 DEFINE`
- `E08 REPOSITORY CLOSURE BLOCKED — SUPERVISION REQUIRED`

---

# STOP OBBLIGATORIO

Dopo la chiusura repository:

**FERMATI.**

NON iniziare E09-01 DEFINE.

NON modificare ulteriormente il codice.

NON inviare submission Kaggle.

Attendi esplicita approvazione prima di E09.
