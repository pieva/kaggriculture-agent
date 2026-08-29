# MANUTENZIONE REPOSITORY — Ricostruzione `.venv` riproducibile e aggiornamento documentazione

## Contesto

Nel repository Kaggriculture l'ambiente virtuale locale `.venv`, originariamente creato durante il lavoro con Antigravity, non è più affidabile dopo successive installazioni/modifiche effettuate da altri agenti/IDE.

Il problema da risolvere non è semplicemente "far funzionare di nuovo `.venv`", ma rendere l'ambiente Python del repository:

- dichiarativo;
- riproducibile;
- indipendente dall'agente utilizzato (Antigravity, Codex, Copilot);
- documentato;
- verificabile con smoke test.

Questa attività è esclusivamente di **environment repair + documentation**.

Non modificare la strategia Kaggriculture.
Non iniziare nuovi esperimenti.
Non cambiare MODEL_SPEC salvo eventuali riferimenti puramente operativi all'ambiente.
Non fare upload Kaggle.

---

## Repository

Lavora nel working tree locale corrente:

`C:\Users\pietr\Projects\kaggriculture-agent`

Non creare branch o worktree.

Prima di qualsiasi modifica eseguire e registrare:

```powershell
git branch --show-current
git status --short
git log -1 --oneline
python --version
py --version
```

Se disponibili, registrare anche:

```powershell
where.exe python
where.exe pip
```

Non assumere che il Python attualmente attivo appartenga a `.venv`.

---

# FASE 1 — Audit della configurazione Python versionata

Prima di eliminare `.venv`, individuare quali file versionati rappresentano attualmente la fonte di verità delle dipendenze.

Ispezionare almeno, se presenti:

- `pyproject.toml`
- `requirements.txt`
- `requirements-dev.txt`
- altri `requirements*.txt`
- `setup.py`
- `setup.cfg`
- lock file
- README
- script di setup/bootstrap
- workflow CI
- `.gitignore`

Determinare:

1. versione Python prevista/dichiarata;
2. dipendenze runtime;
3. dipendenze test/dev;
4. dipendenze necessarie per `kaggle-environments`;
5. eventuali versioni pinned;
6. eventuali installazioni documentate ma non dichiarate;
7. eventuali divergenze tra documentazione e configurazione reale.

Creare:

`results/environment/ENVIRONMENT_AUDIT.md`

con la diagnosi.

---

# FASE 2 — Verificare lo stato di `.venv`

Prima della cancellazione:

- verificare che `.venv` sia ignorato da Git;
- verificare che nessun file dentro `.venv` sia tracked;
- non cancellare alcun file versionato;
- registrare, se possibile senza spendere troppo tempo:
  - Python della `.venv`;
  - `pip --version`;
  - `pip freeze`;
  - errore/sintomo che rende l'ambiente non affidabile.

Salvare il vecchio `pip freeze`, se accessibile, in:

`results/environment/OLD_VENV_PIP_FREEZE.txt`

Questo file serve solo come evidenza diagnostica: **non deve diventare automaticamente la nuova fonte delle dipendenze**.

---

# FASE 3 — Definire la fonte canonica delle dipendenze

La ricostruzione deve partire esclusivamente da file versionati.

Se esiste già una fonte completa e coerente (`requirements*.txt`, `pyproject.toml`, ecc.), usarla.

Se invece le dipendenze necessarie sono disperse o implicite:

1. ricostruire il dependency set minimo realmente necessario dal repository;
2. distinguere runtime da test/dev quando opportuno;
3. creare o correggere il file dichiarativo più coerente con l'architettura esistente;
4. evitare dipendenze non necessarie;
5. non copiare ciecamente `pip freeze`;
6. non aggiornare arbitrariamente alle versioni più recenti;
7. preservare versioni già comprovate quando ricostruibili.

Qualsiasi modifica al dependency set deve essere spiegata in `ENVIRONMENT_AUDIT.md`.

---

# FASE 4 — Eliminare e ricreare `.venv`

Solo dopo l'audit.

Su Windows/PowerShell:

1. assicurarsi che nessun processo dipenda dalla vecchia `.venv`;
2. eliminare esclusivamente la directory locale `.venv`;
3. ricrearla usando la versione Python canonica determinata nell'audit;
4. aggiornare `pip` solo se necessario e compatibile;
5. installare le dipendenze esclusivamente dalla configurazione versionata.

Preferire comandi riproducibili e documentabili.

Esempio indicativo, da adattare alla configurazione reale:

```powershell
py -<VERSION> -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Non assumere `<VERSION>`: ricavarla dal repository / ambiente compatibile.

---

# FASE 5 — Smoke test ambiente

Dopo la ricostruzione verificare almeno:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
```

Poi verificare import essenziali realmente usati dal progetto, incluso `kaggle_environments` se previsto.

Eseguire quindi i test più economici e rappresentativi, senza modificare strategy:

1. `py_compile` sui moduli principali;
2. test core;
3. behavioral-equivalence test esistente;
4. un benchmark/smoke episode breve o benchmark stabile già disponibile, se ragionevolmente rapido.

Se la suite completa è abbastanza rapida, eseguire:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/
```

Altrimenti documentare quali test sono stati eseguiti e perché.

Non interpretare un warning `.pytest_cache` come failure se i test passano.

---

# FASE 6 — Verifica di non regressione

L'environment repair non deve cambiare il comportamento della strategy.

Usare almeno un benchmark noto e confrontarlo con un risultato storico riproducibile, se disponibile.

L'obiettivo non è ottimizzare il punteggio, ma verificare:

> stesso codice + ambiente ricostruito → comportamento compatibile con il baseline atteso.

Se emerge una divergenza materiale:

- non correggere la strategy;
- fermarsi;
- identificare quale dipendenza/versione produce la divergenza.

---

# FASE 7 — Aggiornamento documentazione repository

Aggiornare `README.md` e/o la documentazione operativa appropriata con una sezione canonica:

## Ambiente Python

Deve contenere:

### Prerequisiti

- versione Python supportata;
- eventuali prerequisiti esterni.

### Creazione ambiente

Comandi PowerShell esatti.

### Installazione dipendenze

Comandi esatti dalla fonte versionata.

### Verifica

Comandi per:

- Python version;
- `pip check`;
- test;
- eventuale benchmark smoke.

### Ricostruzione ambiente

Specificare chiaramente che `.venv` è disposable:

> `.venv` è un artifact locale e non una fonte di verità. In caso di incoerenza deve essere eliminato e ricreato dalla configurazione versionata del repository.

---

# FASE 8 — Regola multi-agent

Aggiungere alla documentazione operativa del repository una regola esplicita:

## Environment discipline per agenti

Antigravity, Codex, Copilot e altri agenti che lavorano sul repository devono:

1. usare la `.venv` canonica del repository;
2. non considerare pacchetti installati localmente come fonte di verità;
3. non eseguire installazioni permanenti ad hoc per "far passare" un task senza aggiornare la configurazione versionata;
4. prima di aggiungere/modificare una dipendenza:
   - verificare la configurazione esistente;
   - motivare la modifica;
   - aggiornare il file dichiarativo;
   - eseguire `pip check` e test;
5. non cambiare versione Python o dependency set silenziosamente;
6. segnalare qualsiasi incompatibilità tra ambiente e repository.

Principio:

> `Repository configuration → .venv → verification`

e non:

> `Agent-specific installation → implicit environment state`

---

# FASE 9 — Eventuale helper script

Se il repository non dispone già di un bootstrap semplice, valutare la creazione di uno script minimale, per esempio:

`scripts/setup_env.ps1`

che:

1. verifica Python;
2. crea `.venv`;
3. installa le dipendenze canoniche;
4. esegue `pip check`.

Crearlo solo se riduce realmente l'ambiguità e non duplica tooling esistente.

Lo script non deve nascondere errori o installare dipendenze non dichiarate.

---

# FASE 10 — Aggiornamento file di stato

Aggiornare `docs/PROJECT_STATE.md` e `docs/NEW_SESSION.md` solo per registrare:

- environment repair completato;
- fonte canonica delle dipendenze;
- comando canonico di attivazione/esecuzione;
- `.venv` disposable;
- environment discipline multi-agent.

Non modificare lo stato strategico X1.12/X1.13/X1.14 se non necessario.

---

# Verifica finale obbligatoria

Al termine riportare:

1. causa dell'incoerenza rilevata, se determinabile;
2. versione Python canonica;
3. fonte canonica delle dipendenze;
4. `.venv` precedente eliminata: sì/no;
5. nuova `.venv` creata: sì/no;
6. `pip check`;
7. test eseguiti e risultati;
8. benchmark/smoke result;
9. file documentali aggiornati;
10. eventuali file dependency modificati;
11. eventuale `scripts/setup_env.ps1`;
12. `git diff --stat`;
13. `git status --short`.

Confermare esplicitamente:

`ENVIRONMENT REBUILT FROM VERSIONED CONFIGURATION`

`MULTI-AGENT ENVIRONMENT DISCIPLINE DOCUMENTED`

`STRATEGY CODE: NOT MODIFIED BY ENVIRONMENT REPAIR`

---

# Vincoli finali

- non fare commit;
- non fare upload Kaggle;
- non modificare strategy per far passare i test;
- non modificare submission per far passare i test;
- non usare `pip freeze` come requirements senza analisi;
- non installare pacchetti globalmente;
- non creare nuovi worktree;
- non cancellare file versionati;
- fermarsi e segnalare eventuali incompatibilità invece di mascherarle.
