# Kaggriculture â€” Experimental Training of Decision Models

Kaggriculture Ã¨ un laboratorio sperimentale per lâ€™**addestramento, il tuning e la validazione di modelli decisionali espliciti** in un ambiente competitivo.

La competizione Kaggle **Kaggriculture** fornisce lâ€™ambiente, le regole e un target economico osservabile. Non costituisce lâ€™obiettivo principale del progetto: Ã¨ lâ€™**ambiente sperimentale** nel quale formulare modelli strategici, trasformarli in policy eseguibili, raccogliere evidenza e revisionare progressivamente il modello.

Lâ€™obiettivo non Ã¨ soltanto produrre una submission con uno score maggiore, ma costruire un processo verificabile per stabilire:

- quali variabili del sistema sono realmente **feature** utili rispetto al target;
- quali relazioni esistono tra feature e performance;
- quali soglie separano regimi operativi differenti;
- quali parametri e iperparametri devono essere sottoposti a tuning;
- quando un miglioramento generalizza e quando Ã¨ overfitting sullâ€™evidenza giÃ  osservata.

Il modello finale puÃ² essere una policy deterministica interamente scritta a mano.

> **Addestrare un modello non significa necessariamente addestrare una rete neurale.**

## Model Foundation

Kaggriculture separa esplicitamente la rappresentazione del dominio dalla policy che controlla lâ€™agente.

La **Model Foundation** Ã¨ costituita da quattro artefatti coordinati:

| Artefatto               | Percorso canonico           | Funzione                                                                                     | Domanda                                            |
|:------------------------|:----------------------------|:---------------------------------------------------------------------------------------------|:---------------------------------------------------|
| Ontologia               | `docs/model/ontology/`      | Vocabolario canonico del dominio, entitÃ , concetti e relazioni condivise.                    | **Che cosa esiste e che cosa significa?**          |
| State Machine           | `docs/model/state_machine/` | Stati, transizioni, condizioni dellâ€™engine ed evoluzione temporale.                          | **Come evolve il sistema?**                        |
| Feature Model           | `docs/model/feature_model/` | Informazioni osservabili o derivabili al decision time, con semantica, provenienza e limiti. | **Che cosa puÃ² conoscere lâ€™agente quando decide?** |
| `MODEL_SPEC_<AGENT>.md` | `docs/model/model_specs/`   | Uso dei concetti e delle feature ammissibili nel modello decisionale.                        | **Come viene usata lâ€™informazione per decidere?**  |

``` text
docs/model/
â”œâ”€â”€ ontology/
â”œâ”€â”€ state_machine/
â”œâ”€â”€ feature_model/
â”œâ”€â”€ model_specs/
â””â”€â”€ reviews/
```

`reviews/` Ã¨ la sede di governance, evidence review e reconciliation della Foundation e non costituisce un quinto artefatto del modello decisionale.

Lâ€™**Ontologia** definisce ciÃ² che esiste e il significato condiviso dei concetti; non prescrive policy, soglie o prioritÃ . La **State Machine** descrive la dinamica del dominio e separa le regole native dellâ€™engine dagli stati derivati. Il **Feature Model** Ã¨ il contratto informativo tra dominio e modello decisionale. Il **MODEL_SPEC** Ã¨ consumer della Foundation e traduce concetti e feature ammissibili in una rappresentazione decisionale verificabile.

``` text
ENGINE
   â†“
ONTOLOGY
   â†“
STATE MACHINE
   â†“
FEATURE MODEL
   â†“
MODEL_SPEC
   â†“
POLICY / RUNTIME
   â†“
EXECUTION / TELEMETRY
   â†“
FORENSIC ANALYSIS
   â†“
NEW EVIDENCE
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â†’ FOUNDATION REVIEW
```

Una feature puÃ² essere semanticamente valida senza essere ancora sufficientemente definita per lâ€™uso operativo. Feature con formula, denominatore, finestra temporale, fase di campionamento o provenienza incompleti devono rimanere esplicitamente qualificate come `PARTIALLY_KNOWN`, `CONDITIONAL` o equivalenti.

Analogamente:

``` text
MODEL_SPEC declares a feature USED
                 â‰
runtime demonstrably consumes that feature
```

La conformitÃ  richiede tracciabilitÃ  fino allâ€™esecuzione. Il mapping tra Feature Model e MODEL_SPEC deve distinguere input disponibili alla policy, feature derivate nel runtime, telemetria post-action e outcome di valutazione.

### Foundation Tournament

I quattro artefatti non vengono aggiornati automaticamente dopo ogni esperimento. Nuove evidenze provenienti da replay, telemetria, forensic analysis, audit dellâ€™engine o error analysis vengono prima sottoposte a review indipendente e reconciliation.

Quando lâ€™evidenza giustifica una revisione strutturale viene eseguito un **Foundation Tournament**. Non Ã¨ un torneo di performance della policy: il suo obiettivo Ã¨ migliorare correttezza, completezza, coerenza e verificabilitÃ  della rappresentazione condivisa.

Per ciascun artefatto `NO_CHANGE` Ã¨ un risultato valido. Solo dopo review, reconciliation e freeze della Foundation possono essere avviati nuovi cicli di policy training che dipendono dalle modifiche introdotte.

Lo **stato corrente** della Foundation non Ã¨ duplicato nel README: Ã¨ mantenuto in `docs/PROJECT_STATE.md`.

## Parallelo con il Machine Learning

| Machine Learning             | Kaggriculture                                                                                    |
|:-----------------------------|:-------------------------------------------------------------------------------------------------|
| **Training data / evidence** | Replay, telemetria e osservazioni degli esperimenti                                              |
| **Feature space**            | Ontologia canonica delle variabili e dei concetti osservabili                                    |
| **Model**                    | `MODEL_SPEC_<AGENT>.md` del modello decisionale                                                  |
| **Parameters**               | Valori quantitativi che caratterizzano il comportamento della policy                             |
| **Hyperparameters**          | Soglie, target dimensionali, timing, gating e configurazioni sottoposte a selezione sperimentale |
| **Target**                   | Performance economica, principalmente `final_money`                                              |
| **Training**                 | Evidenza â†’ revisione del modello â†’ implementazione â†’ nuovo esperimento                           |
| **Feature discovery**        | Individuazione delle variabili candidate tramite esperimenti e analisi di sensibilitÃ             |
| **Feature discrimination**   | Verifica sperimentale dei concetti realmente discriminanti                                       |
| **Initial bounding**         | Prima delimitazione di soglie, regimi e intervalli candidati                                     |
| **Hyperparameter tuning**    | Esperimenti successivi per restringere soglie e intervalli                                       |
| **Validation**               | Valutazione su evidenza non utilizzata per il tuning                                             |
| **Error analysis**           | Analisi forense di telemetria, failure mode e scostamenti model â†’ policy â†’ execution             |
| **Model comparison**         | Confronto controllato tra modelli alternativi                                                    |
| **Overfitting**              | Adattamento a seed, opponent o evidenza giÃ  usata per revisionare il modello                     |
| **Generalization**           | StabilitÃ  su condizioni non utilizzate durante training e tuning                                 |
| **Ablation**                 | Rimozione o variazione controllata di componenti del modello                                     |
| **Model selection**          | Selezione sulla base di evidenza comparativa e validation                                        |

### Parametri, iperparametri e struttura

Kaggriculture applica principi analoghi a quelli del Machine Learning a un modello decisionale esplicito. Molte soglie e configurazioni vengono formulate dai modeler e verificate sperimentalmente.

Occorre distinguere:

- **struttura del modello** â€” quali feature e relazioni sono considerate;
- **parametri** â€” valori quantitativi del modello/policy;
- **iperparametri** â€” configurazioni e soglie sottoposte a selezione e tuning;
- **target** â€” misura rispetto alla quale il modello viene valutato;
- **generalizzazione** â€” capacitÃ  di funzionare su evidenza non utilizzata per costruirlo.

## Ciclo di addestramento sperimentale

``` text
osservazioni / replay
        â†“
analisi esplorativa e sensibilitÃ
        â†“
candidate feature
        â†“
ontologia = feature space comune
        â†“
MODEL_SPEC indipendenti
        â†“
policy eseguibili
        â†“
esperimenti controllati
        â†“
telemetria + target
        â†“
feature discrimination / error analysis
        â†“
initial bounding
        â†“
parameter & hyperparameter tuning
        â†“
validation
        â†“
generalization test
```

La telemetria consente di distinguere:

1.  **MODEL_VALIDITY** â€” il modello descrive adeguatamente il sistema?
2.  **POLICY_REALIZATION** â€” la policy traduce correttamente il modello?
3.  **IMPLEMENTATION_FIDELITY** â€” lâ€™esecuzione realizza effettivamente la policy prevista?

> **Victory â‰  Model Validity**
> **Defeat â‰  Model Falsification**

## Evoluzione sperimentale

Questa sezione descrive **lâ€™evoluzione del metodo**, non la cronologia di score e classifiche. I risultati contingenti dei singoli round sono conservati in `docs/EXPERIMENT_LOG.md` e `results/`.

### Esplorazione e sensitivity analysis

La prima fase utilizza prevalentemente esperimenti **One Factor At a Time (OFAT)**: una componente della strategia viene modificata mantenendo il piÃ¹ possibile stabile il resto.

Lo scopo Ã¨ sviluppare sensibilitÃ  empirica: individuare variabili candidate, distinguere effetti forti o marginali, osservare failure mode e identificare dimensioni che meritano ulteriori esperimenti.

Lâ€™output Ã¨ un insieme di **candidate feature**, non una lista di feature giÃ  validate.

### Formalizzazione e modelli concorrenti

Le osservazioni accumulate vengono trasformate in modelli strategici espliciti. Il processo introduce progressivamente:

- separazione tra model, policy e implementation;
- ontologia canonica;
- State Machine e Feature Model condivisi;
- `MODEL_SPEC` indipendenti;
- provenance dellâ€™evidenza;
- modeler indipendenti che possono formulare strategie differenti sullo stesso dominio.

Le candidate feature diventano cosÃ¬ concetti formalizzati e ipotesi confrontabili.

### Feature discrimination e initial bounding

I modelli congelati vengono confrontati mediante esperimenti controllati.

Il risultato competitivo non equivale alla selezione definitiva del modello. Questa fase serve a:

1.  stabilire se un concetto mostra evidenza sufficiente per essere trattato come **feature**;
2.  stimare direzione o forma preliminare della relazione con il target;
3.  identificare regimi operativi differenti;
4.  ottenere una **prima soglia o un primo intervallo candidato**;
5.  individuare confounder e variabili non discriminate;
6.  progettare gli esperimenti di tuning successivi.

Un valore osservato non determina automaticamente un optimum: costituisce una prima delimitazione del search space da restringere o falsificare con nuova evidenza.

### Parameter e hyperparameter tuning

I round successivi restringono progressivamente gli intervalli delle feature e degli iperparametri supportati.

``` text
candidate interval
       â†“
preregistered test values
       â†“
controlled experiment
       â†“
better-supported interval
       â†“
finer tuning or falsification
```

Ogni esperimento dichiara prima dellâ€™esecuzione il proprio ruolo:

``` text
TRAINING EVIDENCE
VALIDATION EVIDENCE
TEST EVIDENCE
```

Lâ€™evidenza usata per scegliere o restringere un parametro non puÃ² essere riutilizzata come prova indipendente della sua generalizzazione.

### Runtime realization e verifica sullâ€™engine reale

Test unitari e conformitÃ  formale non sono sufficienti a garantire che un modello sia realmente eseguito dallâ€™engine.

``` text
MODEL_SPEC
   â†“
BUILD
   â†“
UNIT TEST
   â†“
REAL-ENGINE SMOKE
   â†“
POLICY REALIZATION
   â†“
TOURNAMENT READINESS
   â†“
CONTROLLED TOURNAMENT
```

Una action dispatchata non equivale necessariamente a una transizione di stato, e una transizione valida non equivale necessariamente a un effetto produttivo o economico.

Quando rilevante, la telemetria deve distinguere:

``` text
action dispatched
action accepted
state transition
productive effect
economic effect
```

### Performance iteration e falsificazione causale

Quando una policy Ã¨ tecnicamente valida ma non raggiunge il target economico, il processo non considera sufficiente il semplice tuning opportunistico.

``` text
evidenza
   â†“
problema osservato
   â†“
ipotesi causale preregistrata
   â†“
MODEL_SPEC revision
   â†“
BUILD minimo
   â†“
VERIFY
   â†“
conferma / falsificazione
```

Una previsione intermedia fallita deve essere registrata come **falsificazione**, anche quando il codice funziona e tutti i test sono verdi. Le iterazioni fallite costituiscono parte dellâ€™evidenza e non vengono reinterpretate retroattivamente.

### CapacitÃ , serviceability e monetizzazione

Lâ€™evoluzione del modello ha progressivamente distinto quantitÃ  che inizialmente potevano apparire equivalenti:

``` text
OWNED_SURFACE
      â†“
ACTIVE_SURFACE
      â†“
SERVICEABLE_SURFACE
      â†“
PRODUCTIVE_SURFACE
      â†“
MONETIZED_OUTPUT
```

Possedere o attivare piÃ¹ superficie non garantisce automaticamente maggiore performance. La capacitÃ  deve poter essere servita nel tempo, mantenuta produttiva e trasformata in output monetizzato.

Allo stesso tempo, lâ€™efficienza di una superficie limitata non implica che la scala sia irrilevante: lâ€™espansione produttiva diventa utile quando cresce insieme alla capacitÃ  di servizio.

Il problema sperimentale non Ã¨ quindi semplicemente **massimizzare il terreno utilizzato**, ma aumentare la **serviceable productive capacity** senza perdere continuitÃ  operativa.

### Validation e generalization

Le policy che superano i gate locali vengono valutate su evidenza non utilizzata per costruirle.

La disciplina sperimentale separa:

- evidenza utilizzata per formulare o correggere il modello;
- evidenza utilizzata per validation;
- evidenza utilizzata come test indipendente.

Seed, opponent o replay giÃ  utilizzati nel tuning non devono essere presentati successivamente come prova indipendente di generalizzazione.

Kaggle costituisce un livello di **external validation**: permette di osservare le policy contro strategie non controllate localmente e di raccogliere nuova evidenza per i cicli successivi.

## Protocollo di revisione dei MODEL_SPEC

Dopo ogni round, la revisione non consiste nel copiare la strategia vincente. Ogni modeler riesamina indipendentemente i concetti della Foundation e produce evidenza strutturata, per esempio:

``` text
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

``` text
FEATURE
NOT_FEATURE
UNRESOLVED
```

Una soglia osservata costituisce una **inizializzazione del search space**, non un valore ottimale.

## Ruolo dei modeler

Antigravity, Codex e Copilot sono **modeler indipendenti**. Ricevono la stessa Foundation e la stessa evidenza comune, ma revisionano separatamente i propri `MODEL_SPEC`.

Devono distinguere evidenza da inferenza, identificare feature, valutare relazioni con il target, proporre range solo quando supportati, dichiarare confidence e confounder, progettare esperimenti discriminanti e definire condizioni di falsificazione.

Le divergenze tra modeler sono informative: indicano le parti del modello sulle quali lâ€™evidenza non consente ancora una conclusione robusta.

## Stato del progetto

Il README non contiene snapshot dello stato corrente, classifiche, score, commit o conteggi di test, perchÃ© diventano rapidamente obsoleti.

Le fonti canoniche sono:

- [Project State](docs/PROJECT_STATE.md) â€” stato corrente e gate operativo;
- [Experiment Log](docs/EXPERIMENT_LOG.md) â€” cronologia degli esperimenti e risultati;
- [New Session Restart Point](docs/NEW_SESSION.md) â€” punto operativo di ripresa;
- `results/` â€” evidenza, freeze, tournament, report e artifact delle singole iterazioni.

## Ambiente Python

La fonte canonica delle dipendenze Ã¨ `pyproject.toml`. La directory `.venv` Ã¨ un artifact locale disposable.

Versione Python e dipendenze validate devono essere verificate nella configurazione corrente del repository, anzichÃ© duplicate qui come snapshot potenzialmente obsoleti.

### Creazione ambiente

``` powershell
.\scripts\setup_env.ps1 -Recreate
```

### Verifica ambiente

``` powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\pytest.exe tests/
```

### Environment discipline

``` text
Repository configuration â†’ .venv â†’ verification
```

Non cambiare dipendenze, versione Python o configurazione dellâ€™ambiente silenziosamente.

## Installazione ed esecuzione

``` powershell
# Attivazione ambiente
.\.venv\Scripts\Activate.ps1

# Suite completa
.\.venv\Scripts\pytest.exe tests/
```

Runner sperimentali, verifiche di freeze e builder delle submission dipendono dalla fase corrente e sono documentati nei registri di progetto e negli artifact pertinenti. Non vengono fissati nel README per evitare riferimenti rapidamente obsoleti.

## Principio di documentazione

``` text
README
â†’ identitÃ , architettura, metodo e utilizzo stabile

PROJECT_STATE
â†’ stato corrente e prossimo gate

EXPERIMENT_LOG
â†’ storia quantitativa degli esperimenti

NEW_SESSION
â†’ punto operativo di ripresa

results/
â†’ evidenza e artifact riproducibili
```

Questa separazione consente al README di descrivere lâ€™approccio sperimentale senza trasformarsi nella fotografia di una specifica iterazione.
