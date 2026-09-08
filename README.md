# Kaggriculture — Experimental Training of Decision Models

Kaggriculture è un laboratorio sperimentale per sviluppare e valutare **modelli decisionali che gestiscono una fattoria simulata**: decidono cosa coltivare, come impiegare la manodopera, quando acquistare risorse e come organizzare produzione e vendite. I modelli sono *espliciti* perché le loro regole, ipotesi e priorità sono documentate e tradotte in codice eseguibile, chiamato **policy**.

Il progetto impiega più **agenti di sviluppo interni** — Antigravity (AG), Codex, Claude e Copilot — per costruire modelli alternativi e revisionare la documentazione condivisa. Questi strumenti sviluppano le policy; sono poi le policy a prendere le decisioni durante le partite.

La **validazione dei modelli** avviene attraverso test e partite simulate in locale, seguiti dal confronto con avversari esterni nella competizione Kaggle **Kaggriculture**. Kaggle fornisce l'ambiente di gioco, le regole e una misura dei risultati economici. Le revisioni tra agenti interni verificano invece la qualità delle ipotesi, della documentazione e dell'implementazione: sono un'attività distinta dalla valutazione delle prestazioni in partita.

L'obiettivo non è soltanto produrre una submission con uno score maggiore, ma costruire un processo verificabile per stabilire:

- quali variabili del sistema sono realmente **feature** utili rispetto al target;
- quali relazioni esistono tra feature e performance;
- quali soglie separano regimi operativi differenti;
- quali parametri e iperparametri devono essere sottoposti a tuning;
- quando un miglioramento generalizza e quando è overfitting sull'evidenza già osservata.

## Ruolo dei modeler

Antigravity, Codex, Claude e Copilot sono **modeler indipendenti**. Ricevono la stessa Foundation e la stessa evidenza comune, ma revisionano separatamente i propri `MODEL_SPEC`.

### Ambienti e modelli

| Modeler | IDE / ambiente | Modello mostrato nella UI | Effort |
|---|---|---|---|
| Antigravity | Antigravity | Gemini 3.8 Flash | High |
| Codex | Codex | 5.6 Sol | Molto alto |
| Claude | Claude | Sonnet 5 | Alto |
| Copilot | GitHub Copilot | MAI-Code-1.1-Flash | High |

Le etichette sono uno snapshot di provenance ricavato dalle schermate fornite
dal proprietario il 2026-09-03; non costituiscono dipendenze runtime del
repository.

Devono distinguere evidenza da inferenza, identificare feature, valutare relazioni con il target, proporre range solo quando supportati, dichiarare confidence e confounder, progettare esperimenti discriminanti e definire condizioni di falsificazione.

Le divergenze tra modeler sono informative: indicano le parti del modello sulle quali l'evidenza non consente ancora una conclusione robusta.

## Model Foundation

La **Model Foundation** raccoglie la descrizione condivisa del gioco: regole, entità, evoluzione della fattoria e informazioni disponibili per decidere. È organizzata in quattro livelli e costituisce la base comune usata dagli agenti di sviluppo interni.

Ogni modello decisionale ha poi una propria **MODEL_SPEC**, cioè una specifica che descrive come usare questa base per scegliere le azioni. Le specifiche sono raccolte per agente di sviluppo autore del modello (Antigravity, Codex, Claude o Copilot) e guidano l'implementazione delle rispettive policy. La Foundation descrive quindi il mondo in cui si gioca; le MODEL_SPEC definiscono le strategie con cui affrontarlo.

Ogni MODEL_SPEC deve spiegare la **strategia del modello**: obiettivi, pianificazione, priorità, vincoli e gestione degli imprevisti. Deve inoltre elencare i **file che la implementano**, indicando il ruolo di ciascuno. Risultati degli esperimenti, avanzamento del lavoro e prossime attività appartengono ai report e ai registri di stato.

| Livello | Artefatto | Funzione | Domanda |
|---|---|---|---|
| 1. Engine Contract | [Contratto dell'engine](docs/foundation/ENGINE_CONTRACT.md) | Regole e costanti verificate nel codice della simulazione. | **Quali sono le regole del gioco?** |
| 2. Ontologia | [Ontologia](docs/foundation/ontology/ONTOLOGY_C2_1.md) | Definizioni condivise delle entità e delle loro relazioni. | **Che cosa esiste nel gioco e che cosa significa?** |
| 3. State Machine | [Macchina a stati](docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md) | Stati della fattoria, transizioni biologiche e condizioni che le attivano. | **Come evolve la fattoria?** |
| 4. Feature Model | [Modello delle feature](docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md) | Informazioni osservabili o calcolabili quando si decide, con origine e limiti d'uso. | **Che cosa può conoscere la policy quando decide?** |
| Specifiche dei modelli | [MODEL_SPEC per agente di sviluppo](docs/model_specs/) | Strategie e criteri decisionali da implementare nelle singole policy. | **Come si scelgono le azioni usando queste informazioni?** |

Le specifiche condivise e quelle dei singoli modelli si trovano in queste cartelle:

```text
docs/
|-- foundation/
|   |-- ontology/
|   |-- state_machine/
|   `-- feature_model/
`-- model_specs/
```

Gli agenti di sviluppo revisionano questi documenti confrontandoli con il codice del gioco e con i risultati degli esperimenti. Le osservazioni vengono confrontate e le eventuali correzioni concordate prima di aggiornare la base condivisa. Questo processo di revisione è descritto nella sezione [Foundation Tournament](#foundation-tournament).

```text
ENGINE CONTRACT
      |
      v
   ONTOLOGY
      |
      v
STATE MACHINE
      |
      v
FEATURE MODEL
      |
      +-------------------+-------------------+-------------------+
      |                   |                   |                   |
      v                   v                   v                   v
MODEL_SPEC_            MODEL_SPEC_         MODEL_SPEC_         MODEL_SPEC_
ANTIGRAVITY            CODEX               CLAUDE              COPILOT
      |                   |                   |                   |
      v                   v                   v                   v
   POLICY              POLICY              POLICY              POLICY
      |                   |                   |                   |
      +-------------------+-------------------+-------------------+
                                      |
                                      v
                             EXECUTION / TELEMETRY
                                    |
                                    v
                            FORENSIC ANALYSIS
                                    |
                                    v
                              NEW EVIDENCE
                                    |
                                    v
                           FOUNDATION REVIEW
```

### Foundation Tournament

I layer della Foundation non vengono aggiornati automaticamente dopo ogni esperimento. Nuove evidenze provenienti da replay, telemetria, forensic analysis, audit dell'engine o error analysis vengono prima sottoposte a review indipendente e reconciliation.

Quando l'evidenza giustifica una revisione strutturale viene eseguito un **Foundation Tournament**. Non è un torneo di performance della policy: il suo obiettivo è migliorare correttezza, completezza, coerenza e verificabilità della rappresentazione condivisa.

La revisione non comporta necessariamente modifiche: un documento può essere confermato se risulta corretto, completo e coerente con le evidenze disponibili.

Solo dopo review, reconciliation e freeze della Foundation possono essere avviati nuovi cicli di policy training che dipendono dalle modifiche introdotte.

Lo **stato corrente** della Foundation e gli hash dei documenti sono mantenuti nel [manifest della Foundation](docs/foundation/FOUNDATION_C2_1_MANIFEST.md); lo stato operativo complessivo è nel [Project State](docs/PROJECT_STATE.md).

## Parallelo con il Machine Learning

Kaggriculture riprende dal Machine Learning il metodo sperimentale: usare dati per migliorare un modello e verificarlo su casi nuovi. Qui le regole decisionali sono formulate e riviste esplicitamente dagli agenti di sviluppo.

### Parametri, iperparametri e struttura

- **Struttura:** quali informazioni e regole il modello usa per decidere.
- **Parametri:** i valori numerici usati dalle regole, come una riserva minima di cassa.
- **Iperparametri:** le scelte che governano la ricerca dei parametri, come gli intervalli e il budget degli esperimenti.

Il risultato economico è il **target** della valutazione. Un miglioramento deve funzionare anche su partite non usate per svilupparlo: questa è la **generalizzazione**.

| Concetto del Machine Learning | Applicazione in Kaggriculture |
|---|---|
| **Dati** | Replay e misure raccolte durante le partite. |
| **Modello** | Regole decisionali documentate e implementate nella policy. |
| **Addestramento e tuning** | Revisione delle regole e dei parametri attraverso esperimenti. |
| **Validazione** | Confronto su partite e avversari non usati per il tuning. |
| **Overfitting** | Miglioramento limitato ai casi già analizzati, che non si conferma su casi nuovi. |

## Ciclo di addestramento sperimentale

```text
osservazioni / replay
        |
        v
analisi esplorativa e sensibilità
        |
        v
candidate feature
        |
        v
ontologia = feature space comune
        |
        v
MODEL_SPEC indipendenti
        |
        v
policy eseguibili
        |
        v
esperimenti controllati
        |
        v
telemetria + target
        |
        v
feature discrimination / error analysis
        |
        v
initial bounding
        |
        v
parameter & hyperparameter tuning
        |
        v
validation
        |
        v
generalization test
```

La telemetria consente di distinguere:

1. **MODEL_VALIDITY** — il modello descrive adeguatamente il sistema?
2. **POLICY_REALIZATION** — la policy traduce correttamente il modello?
3. **IMPLEMENTATION_FIDELITY** — l'esecuzione realizza effettivamente la policy prevista?

> **Victory != Model Validity**
> **Defeat != Model Falsification**

## Evoluzione sperimentale

Il metodo procede per cicli: ogni esperimento serve a capire quali scelte funzionano, perché funzionano e in quali condizioni.

1. **Esplorare:** variare singole componenti per individuare le variabili che influenzano i risultati.
2. **Formalizzare:** tradurre le osservazioni in ipotesi e modelli decisionali confrontabili.
3. **Sperimentare e affinare:** confrontare strategie e parametri, verificando che il codice realizzi le decisioni previste e produca gli effetti attesi.
4. **Validare:** valutare le policy su partite e avversari non usati per svilupparle, anche attraverso Kaggle.

Le ipotesi smentite vengono registrate e guidano le revisioni successive. I casi già usati per correggere un modello non diventano prove indipendenti della sua qualità.

Una lezione emersa dagli esperimenti è che l'espansione va pianificata insieme alla manodopera: acquistare terreno è utile quando si riesce a mantenerlo produttivo e a venderne i prodotti.

## Protocollo di revisione dei MODEL_SPEC

Dopo ogni round, la revisione non consiste nel copiare la strategia vincente. Ogni modeler riesamina indipendentemente i concetti della Foundation e produce evidenza strutturata, per esempio:

```text
concept_id
feature_status
relationship
evidence
failure_region
success_region
candidate_threshold_or_interval
confidence
confounders
next_test_values
falsification_condition
```

`feature_status` distingue almeno:

```text
FEATURE
NOT_FEATURE
UNRESOLVED
```

Una soglia osservata costituisce una **inizializzazione del search space**, non un valore ottimale.

## Stato del progetto

Il README non contiene snapshot dello stato corrente, classifiche, score, commit o conteggi di test, perché diventano rapidamente obsoleti.

Le fonti canoniche sono:

- [Project State](docs/PROJECT_STATE.md) — stato corrente e gate operativo;
- [Experiment Log](docs/EXPERIMENT_LOG.md) — cronologia degli esperimenti e risultati;
- [New Session Restart Point](docs/NEW_SESSION.md) — punto operativo di ripresa;
- `experiments/` — design, prompt, evidenza, freeze e report delle singole iterazioni;
- `data/replays/json/` — cartella unica dei replay grezzi esterni; `json.md`
  ne registra origine, hash, ruolo epistemico e uso.

## Ambiente Python

La fonte canonica delle dipendenze è `pyproject.toml`. La directory `.venv` è un artifact locale disposable.

Versione Python e dipendenze validate devono essere verificate nella configurazione corrente del repository, anziché duplicate qui come snapshot potenzialmente obsoleti.

### Creazione ambiente

```powershell
.\scripts\setup_env.ps1 -Recreate
```

### Verifica ambiente

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\pytest.exe tests/
```

### Environment discipline

```text
Repository configuration -> .venv -> verification
```

Non cambiare dipendenze, versione Python o configurazione dell'ambiente silenziosamente.

## Installazione ed esecuzione

```powershell
# Attivazione ambiente
.\.venv\Scripts\Activate.ps1

# Suite completa
.\.venv\Scripts\pytest.exe tests/
```

Runner sperimentali, verifiche di freeze e builder delle submission dipendono dalla fase corrente e sono documentati nei registri di progetto e negli artifact pertinenti. Non vengono fissati nel README per evitare riferimenti rapidamente obsoleti.

## Principio di documentazione

```text
README
-> identità, architettura, metodo e utilizzo stabile

PROJECT_STATE
-> stato corrente e prossimo gate

EXPERIMENT_LOG
-> storia quantitativa degli esperimenti

NEW_SESSION
-> punto operativo di ripresa

experiments/
-> ciclo completo e artifact riproducibili di ciascun round

data/
-> input esterni e replay immutabili
```

Questa separazione consente al README di descrivere l'approccio sperimentale senza trasformarsi nella fotografia di una specifica iterazione.
1*Nota sulla nomenclatura C2:* La sigla **C2** indica il **Cycle 2** (ciclo di revisione, audit e provenance della Foundation), non un componente architetturale o un modello di strategia.
