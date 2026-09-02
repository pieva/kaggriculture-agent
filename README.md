# Kaggriculture — Experimental Training of Decision Models

Kaggriculture è un laboratorio sperimentale per l'**addestramento, il tuning e la validazione di modelli decisionali espliciti** in un ambiente competitivo.

La competizione Kaggle **Kaggriculture** fornisce l'ambiente, le regole e un target economico osservabile. Non costituisce l'obiettivo principale del progetto: è l'**ambiente sperimentale** nel quale formulare modelli strategici, trasformarli in policy eseguibili, raccogliere evidenza e revisionare progressivamente il modello.

L'obiettivo non è soltanto produrre una submission con uno score maggiore, ma costruire un processo verificabile per stabilire:

- quali variabili del sistema sono realmente **feature** utili rispetto al target;
- quali relazioni esistono tra feature e performance;
- quali soglie separano regimi operativi differenti;
- quali parametri e iperparametri devono essere sottoposti a tuning;
- quando un miglioramento generalizza e quando è overfitting sull'evidenza già osservata.

Il modello finale può essere una policy deterministica interamente scritta a mano.

> **Addestrare un modello non significa necessariamente addestrare una rete neurale.**

> Status di governance del repository (2026-09-02): riordino completo con gate A7 `PASS`; strategia E17 riconciliata e congelata; E17.0 completato con gate tecnico `PASS`. Il controllo esterno Codex è attivo su Kaggle e ha raggiunto una rilevazione intermedia di `996` da un ingresso a `600`; il rating non è ancora stabilizzato. Copilot conserva la propria baseline nativa solo come evidenza locale, Antigravity è in pausa per esaurimento crediti e la prossima evoluzione resta sospesa fino a una misura esterna stabile.

## Model Foundation

Kaggriculture separa esplicitamente la rappresentazione del dominio dalla policy che controlla l'agente.

La **Model Foundation C2.1** (condivisa e neutrale) è articolata su **4 layer normativi coordinati**, a valle dei quali si collocano direttamente i **MODEL_SPEC specifici di ciascun agente**:

| Layer | Artefatto | Percorso canonico | Funzione | Domanda |
|---|---|---|---|---|
| 1. Engine Contract | Frozen Engine Contract | `docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md` | Ground truth formale e verificato delle regole e costanti della simulazione. | **Quali sono le regole e i vincoli primitivi del codice dell'ambiente?** |
| 2. Ontologia | `ONTOLOGY_C2_1.md` | `docs/foundation/ontology/ONTOLOGY_C2_1.md` | Vocabolario canonico del dominio, entità, concetti e relazioni condivise. | **Che cosa esiste nel dominio e che cosa significa?** |
| 3. State Machine | `KAGGRICULTURE_STATE_MACHINE_C2_1.md` | `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md` | Stati fisici, transizioni biologiche, guardie e ciclo causale dell'engine. | **Come evolve lo stato dell'ambiente?** |
| 4. Feature Model | `KAGGRICULTURE_FEATURE_MODEL_C2_1.md` | `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md` | Feature osservabili e derivabili online al decision time, con provenance, telemetria e no-leakage contract. | **Che cosa può conoscere l'agente quando decide?** |
| Downstream | `MODEL_SPEC_<AGENT>.md` | `docs/model_specs/` | Modello decisionale e strategico proprietario di ciascun agente (Antigravity, Codex, Copilot). | **Come usa l'agente le feature per formulare policy e azioni?** |

*Nota sulla nomenclatura C2:* La sigla **C2** indica il **Cycle 2** (ciclo di revisione, audit e provenance della Foundation), non un componente architetturale o un modello di strategia.

```text
docs/
|-- foundation/
|   |-- ontology/
|   |-- state_machine/
|   `-- feature_model/
|-- model_specs/
`-- governance/
```

`reviews/` è la sede di governance, evidence review e reconciliation della Foundation e non costituisce un layer del modello decisionale.

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
      +-----------------------------+-----------------------------+
      |                             |                             |
      v                             v                             v
MODEL_SPEC_ANTIGRAVITY      MODEL_SPEC_CODEX              MODEL_SPEC_COPILOT
      |                             |                             |
      v                             v                             v
   POLICY                        POLICY                        POLICY
      |                             |                             |
      +-----------------------------+-----------------------------+
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

Una feature può essere semanticamente valida senza essere ancora sufficientemente definita per l'uso operativo. Feature con formula, denominatore, finestra temporale, fase di campionamento o provenienza incompleti devono rimanere esplicitamente qualificate come `PARTIALLY_KNOWN`, `CONDITIONAL` o equivalenti.

Analogamente:

```text
MODEL_SPEC declares a feature USED
                 !=
runtime demonstrably consumes that feature
```

La conformità richiede tracciabilità fino all'esecuzione. Il mapping tra Feature Model e MODEL_SPEC deve distinguere input disponibili alla policy, feature derivate nel runtime, telemetria post-action e outcome di valutazione.

### Foundation Tournament

I layer della Foundation non vengono aggiornati automaticamente dopo ogni esperimento. Nuove evidenze provenienti da replay, telemetria, forensic analysis, audit dell'engine o error analysis vengono prima sottoposte a review indipendente e reconciliation.

Quando l'evidenza giustifica una revisione strutturale viene eseguito un **Foundation Tournament**. Non è un torneo di performance della policy: il suo obiettivo è migliorare correttezza, completezza, coerenza e verificabilità della rappresentazione condivisa.

Per ciascun artefatto `NO_CHANGE` è un risultato valido. Solo dopo review, reconciliation e freeze della Foundation possono essere avviati nuovi cicli di policy training che dipendono dalle modifiche introdotte.

Lo **stato corrente** della Foundation e gli hash dei tre documenti C2.1 sono mantenuti in `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`; lo stato operativo complessivo è in `docs/PROJECT_STATE.md`.

## Parallelo con il Machine Learning

| Machine Learning | Kaggriculture |
|---|---|
| **Training data / evidence** | Replay, telemetria e osservazioni degli esperimenti |
| **Feature space** | Ontologia canonica delle variabili e dei concetti osservabili |
| **Model** | `MODEL_SPEC_<AGENT>.md` del modello decisionale |
| **Parameters** | Valori quantitativi che caratterizzano il comportamento della policy |
| **Hyperparameters** | Soglie, target dimensionali, timing, gating e configurazioni sottoposte a selezione sperimentale |
| **Target** | Performance economica, principalmente `final_money` |
| **Training** | Evidenza -> revisione del modello -> implementazione -> nuovo esperimento |
| **Feature discovery** | Individuazione delle variabili candidate tramite esperimenti e analisi di sensibilità |
| **Feature discrimination** | Verifica sperimentale dei concetti realmente discriminanti |
| **Initial bounding** | Prima delimitazione di soglie, regimi e intervalli candidati |
| **Hyperparameter tuning** | Esperimenti successivi per restringere soglie e intervalli |
| **Validation** | Valutazione su evidenza non utilizzata per il tuning |
| **Error analysis** | Analisi forense di telemetria, failure mode e scostamenti model -> policy -> execution |
| **Model comparison** | Confronto controllato tra modelli alternativi |
| **Overfitting** | Adattamento a seed, opponent o evidenza già usata per revisionare il modello |
| **Generalization** | Stabilità su condizioni non utilizzate durante training e tuning |
| **Ablation** | Rimozione o variazione controllata di componenti del modello |
| **Model selection** | Selezione sulla base di evidenza comparativa e validation |

### Parametri, iperparametri e struttura

Kaggriculture applica principi analoghi a quelli del Machine Learning a un modello decisionale esplicito. Molte soglie e configurazioni vengono formulate dai modeler e verificate sperimentalmente.

Occorre distinguere:

- **struttura del modello** — quali feature e relazioni sono considerate;
- **parametri** — valori quantitativi del modello/policy;
- **iperparametri** — configurazioni e soglie sottoposte a selezione e tuning;
- **target** — misura rispetto alla quale il modello viene valutato;
- **generalizzazione** — capacità di funzionare su evidenza non utilizzata per costruirlo.

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

Questa sezione descrive **l'evoluzione del metodo**, non la cronologia di score e classifiche. I risultati contingenti dei singoli round sono indicizzati in `docs/EXPERIMENT_LOG.md` e conservati nelle vertical slice sotto `experiments/`.

### Esplorazione e sensitivity analysis

La prima fase utilizza prevalentemente esperimenti **One Factor At a Time (OFAT)**: una componente della strategia viene modificata mantenendo il più possibile stabile il resto.

Lo scopo è sviluppare sensibilità empirica: individuare variabili candidate, distinguere effetti forti o marginali, osservare failure mode e identificare dimensioni che meritano ulteriori esperimenti.

L'output è un insieme di **candidate feature**, non una lista di feature già validate.

### Formalizzazione e modelli concorrenti

Le osservazioni accumulate vengono trasformate in modelli strategici espliciti. Il processo introduce progressivamente:

- separazione tra model, policy e implementation;
- ontologia canonica;
- State Machine e Feature Model condivisi;
- `MODEL_SPEC` indipendenti;
- provenance dell'evidenza;
- modeler indipendenti che possono formulare strategie differenti sullo stesso dominio.

Le candidate feature diventano così concetti formalizzati e ipotesi confrontabili.

### Feature discrimination e initial bounding

I modelli congelati vengono confrontati mediante esperimenti controllati.

Il risultato competitivo non equivale alla selezione definitiva del modello. Questa fase serve a:

1. stabilire se un concetto mostra evidenza sufficiente per essere trattato come **feature**;
2. stimare direzione o forma preliminare della relazione con il target;
3. identificare regimi operativi differenti;
4. ottenere una **prima soglia o un primo intervallo candidato**;
5. individuare confounder e variabili non discriminate;
6. progettare gli esperimenti di tuning successivi.

Un valore osservato non determina automaticamente un optimum: costituisce una prima delimitazione del search space da restringere o falsificare con nuova evidenza.

### Parameter e hyperparameter tuning

I round successivi restringono progressivamente gli intervalli delle feature e degli iperparametri supportati.

```text
candidate interval
       |
       v
preregistered test values
       |
       v
controlled experiment
       |
       v
better-supported interval
       |
       v
finer tuning or falsification
```

Ogni esperimento dichiara prima dell'esecuzione il proprio ruolo:

```text
TRAINING EVIDENCE
VALIDATION EVIDENCE
TEST EVIDENCE
```

L'evidenza usata per scegliere o restringere un parametro non può essere riutilizzata come prova indipendente della sua generalizzazione.

### Runtime realization e verifica sull'engine reale

Test unitari e conformità formale non sono sufficienti a garantire che un modello sia realmente eseguito dall'engine.

```text
MODEL_SPEC
   |
   v
BUILD
   |
   v
UNIT TEST
   |
   v
REAL-ENGINE SMOKE
   |
   v
POLICY REALIZATION
   |
   v
TOURNAMENT READINESS
   |
   v
CONTROLLED TOURNAMENT
```

Una action dispatchata non equivale necessariamente a una transizione di stato, e una transizione valida non equivale necessariamente a un effetto produttivo o economico.

Quando rilevante, la telemetria deve distinguere:

```text
action dispatched
action accepted
state transition
productive effect
economic effect
```

### Performance iteration e falsificazione causale

Quando una policy è tecnicamente valida ma non raggiunge il target economico, il processo non considera sufficiente il semplice tuning opportunistico.

```text
evidenza
   |
   v
problema osservato
   |
   v
ipotesi causale preregistrata
   |
   v
MODEL_SPEC revision
   |
   v
BUILD minimo
   |
   v
VERIFY
   |
   v
conferma / falsificazione
```

Una previsione intermedia fallita deve essere registrata come **falsificazione**, anche quando il codice funziona e tutti i test sono verdi. Le iterazioni fallite costituiscono parte dell'evidenza e non vengono reinterpretate retroattivamente.

### Capacità, serviceability e monetizzazione

L'evoluzione del modello ha progressivamente distinto quantità che inizialmente potevano apparire equivalenti:

```text
OWNED_SURFACE
      |
      v
ACTIVE_SURFACE
      |
      v
SERVICEABLE_SURFACE
      |
      v
PRODUCTIVE_SURFACE
      |
      v
MONETIZED_OUTPUT
```

Possedere o attivare più superficie non garantisce automaticamente maggiore performance. La capacità deve poter essere servita nel tempo, mantenuta produttiva e trasformata in output monetizzato.

Allo stesso tempo, l'efficienza di una superficie limitata non implica che la scala sia irrilevante: l'espansione produttiva diventa utile quando cresce insieme alla capacità di servizio.

Il problema sperimentale non è quindi semplicemente **massimizzare il terreno utilizzato**, ma aumentare la **serviceable productive capacity** senza perdere continuità operativa.

### Validation e generalization

Le policy che superano i gate locali vengono valutate su evidenza non utilizzata per costruirle.

La disciplina sperimentale separa:

- evidenza utilizzata per formulare o correggere il modello;
- evidenza utilizzata per validation;
- evidenza utilizzata come test indipendente.

Seed, opponent o replay già utilizzati nel tuning non devono essere presentati successivamente come prova indipendente di generalizzazione.

Kaggle costituisce un livello di **external validation**: permette di osservare le policy contro strategie non controllate localmente e di raccogliere nuova evidenza per i cicli successivi.

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

## Ruolo dei modeler

Antigravity, Codex e Copilot sono **modeler indipendenti**. Ricevono la stessa Foundation e la stessa evidenza comune, ma revisionano separatamente i propri `MODEL_SPEC`.

Devono distinguere evidenza da inferenza, identificare feature, valutare relazioni con il target, proporre range solo quando supportati, dichiarare confidence e confounder, progettare esperimenti discriminanti e definire condizioni di falsificazione.

Le divergenze tra modeler sono informative: indicano le parti del modello sulle quali l'evidenza non consente ancora una conclusione robusta.

## Stato del progetto

Il README non contiene snapshot dello stato corrente, classifiche, score, commit o conteggi di test, perché diventano rapidamente obsoleti.

Le fonti canoniche sono:

- [Project State](docs/PROJECT_STATE.md) — stato corrente e gate operativo;
- [Experiment Log](docs/EXPERIMENT_LOG.md) — cronologia degli esperimenti e risultati;
- [New Session Restart Point](docs/NEW_SESSION.md) — punto operativo di ripresa;
- `experiments/` — design, prompt, evidenza, freeze e report delle singole iterazioni;
- `data/replays/` — replay esterni con manifest e ruolo epistemico.

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
