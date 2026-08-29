# Kaggriculture --- Experimental Training of Decision Models

Kaggriculture è un laboratorio sperimentale per l'**addestramento, il
tuning e la validazione di modelli decisionali espliciti** in un
ambiente competitivo.

La competizione Kaggle **Kaggriculture** fornisce l'ambiente, le regole
e un target economico osservabile. Non costituisce più l'obiettivo
principale del progetto: è l'**ambiente sperimentale** nel quale
formulare modelli strategici, trasformarli in policy eseguibili,
raccogliere evidenza e revisionare progressivamente il modello.

L'obiettivo non è soltanto produrre una submission con uno score
maggiore, ma costruire un processo verificabile per stabilire:

-   quali variabili del sistema sono realmente **feature** utili
    rispetto al target;
-   quali relazioni esistono tra feature e performance;
-   quali soglie separano regimi operativi differenti;
-   quali parametri e iperparametri devono essere sottoposti a tuning;
-   quando un miglioramento generalizza e quando è overfitting
    sull'evidenza già osservata.

Il modello finale può essere una policy deterministica interamente
scritta a mano.

> **Addestrare un modello non significa necessariamente addestrare una
> rete neurale.**

## Parallelo con il Machine Learning

  -----------------------------------------------------------------------
  Machine Learning                    Kaggriculture
  ----------------------------------- -----------------------------------
  **Training data / evidence**        Replay, telemetria e osservazioni
                                      degli esperimenti

  **Feature space**                   Ontologia canonica delle variabili
                                      e dei concetti osservabili

  **Model**                           `MODEL_SPEC_<AGENT>.md` del modello
                                      decisionale

  **Parameters**                      Valori quantitativi che
                                      caratterizzano il comportamento
                                      della policy

  **Hyperparameters**                 Soglie, target dimensionali,
                                      timing, gating e configurazioni
                                      sottoposte a selezione sperimentale

  **Target**                          Performance economica,
                                      principalmente `final_money`

  **Training**                        Evidenza → revisione del modello →
                                      implementazione → nuovo esperimento

  **Feature discovery**               Individuazione delle variabili
                                      candidate tramite esperimenti e
                                      analisi di sensibilità

  **Feature discrimination**          Verifica sperimentale dei concetti
                                      realmente discriminanti

  **Initial bounding**                Prima delimitazione di soglie,
                                      regimi e intervalli candidati

  **Hyperparameter tuning**           Esperimenti successivi per
                                      restringere soglie e intervalli

  **Validation**                      Valutazione su evidenza non
                                      utilizzata per il tuning

  **Error analysis**                  Analisi forense di telemetria,
                                      failure mode e scostamenti model →
                                      policy → execution

  **Model comparison**                Confronto controllato tra modelli
                                      alternativi

  **Overfitting**                     Adattamento a seed, opponent o
                                      evidenza già usata per revisionare
                                      il modello

  **Generalization**                  Stabilità su condizioni non
                                      utilizzate durante training e
                                      tuning

  **Ablation**                        Rimozione o variazione controllata
                                      di componenti del modello

  **Model selection**                 Selezione sulla base di evidenza
                                      comparativa e validation
  -----------------------------------------------------------------------

### Parametri, iperparametri e struttura

Nel Machine Learning non è necessario rappresentare il fenomeno mediante
una formula scelta esplicitamente dal progettista.

In una regressione polinomiale, per esempio, i coefficienti sono
**parametri appresi dai dati**, mentre il grado del polinomio può essere
trattato come **iperparametro** e selezionato confrontando modelli
differenti. Altre famiglie apprendono strutture operative: un Decision
Tree può apprendere split e soglie, mentre profondità massima e altri
vincoli configurano il processo di apprendimento.

Kaggriculture applica gli stessi principi a un modello decisionale
esplicito. Oggi molte soglie e configurazioni vengono formulate dai
modeler e verificate sperimentalmente. Una possibile evoluzione è
utilizzare modelli interpretabili, come Decision Tree, per apprendere
dai dati soglie e interazioni tra feature.

Occorre distinguere:

-   **struttura del modello** --- quali feature e relazioni sono
    considerate;
-   **parametri** --- valori quantitativi del modello/policy;
-   **iperparametri** --- configurazioni e soglie sottoposte a selezione
    e tuning;
-   **target** --- misura rispetto alla quale il modello viene valutato;
-   **generalizzazione** --- capacità di funzionare su evidenza non
    utilizzata per costruirlo.

## Ciclo di addestramento sperimentale

``` text
osservazioni / replay
        ↓
analisi esplorativa e sensibilità
        ↓
candidate feature
        ↓
ontologia = feature space comune
        ↓
MODEL_SPEC indipendenti
        ↓
policy eseguibili
        ↓
esperimenti controllati
        ↓
telemetria + target
        ↓
feature discrimination / error analysis
        ↓
initial bounding
        ↓
parameter & hyperparameter tuning
        ↓
validation
        ↓
generalization test
```

L'**ontologia** definisce il feature space comune. I `MODEL_SPEC`
formalizzano feature, relazioni e parametri. Le submission implementano
i modelli come **policy eseguibili**.

La telemetria consente di distinguere:

1.  **MODEL_VALIDITY** --- il modello descrive adeguatamente il sistema?
2.  **POLICY_REALIZATION** --- la policy traduce correttamente il
    modello?
3.  **IMPLEMENTATION_FIDELITY** --- l'esecuzione realizza effettivamente
    la policy prevista?

> **Victory ≠ Model Validity**\
> **Defeat ≠ Model Falsification**

## Evoluzione sperimentale

### E01--E11 --- Exploratory Sensitivity / Candidate Feature Discovery

La prima fase ha utilizzato prevalentemente esperimenti **One Factor At
a Time (OFAT)**: una componente della strategia veniva modificata
mantenendo il più possibile stabile il resto.

Lo scopo era sviluppare **sensibilità empirica**: capire quali variabili
sembravano influenzare il target, quali producevano effetti marginali,
quali failure mode emergevano e quali dimensioni meritavano ulteriori
esperimenti.

L'output è stato un insieme di **candidate feature**, non una lista di
feature già validate.

### E12--E14 --- Feature Formalization / Competing Models

Le osservazioni accumulate sono state trasformate in modelli strategici
più espliciti. Sono stati introdotti la separazione
model/policy/implementation, l'ontologia canonica, `MODEL_SPEC`
indipendenti per Antigravity, Codex e Copilot e una disciplina più
rigorosa sulla provenance dell'evidenza.

Le candidate feature emerse dall'esplorazione sono così diventate
concetti formalizzati e ipotesi confrontabili.

### E15 --- Feature Discrimination & Initial Bounding

E15 segna il passaggio dall'esplorazione all'**addestramento strutturato
dei modelli**.

Tre modelli indipendenti sono stati congelati e confrontati in un torneo
pairwise controllato:

  Match                           Risultato
  ------------------------------- ----------------------------------------
  M1 --- Antigravity vs Codex     `$8,672` vs `$20,461` --- **Codex**
  M2 --- Codex vs Copilot         `$27,510` vs `$37,752` --- **Copilot**
  M3 --- Copilot vs Antigravity   `$26,629` vs `$9,371` --- **Copilot**

Classifica: **Copilot 2--0**, **Codex 1--1**, **Antigravity 0--2**.

Il risultato competitivo non equivale alla selezione definitiva del
modello. Il ruolo di E15 è:

1.  stabilire se un concetto dell'ontologia mostra evidenza sufficiente
    per essere trattato come **feature**;
2.  stimare direzione o forma preliminare della relazione con il target;
3.  identificare differenti regimi operativi;
4.  ottenere una **prima soglia o un primo intervallo candidato**;
5.  individuare confounder e variabili non discriminate;
6.  progettare gli esperimenti di tuning successivi.

E15 **non determina valori ottimali**. Per esempio, 17--18 animali
perdenti contro 4--7 non implica `max_herd = 4`: suggerisce che
`livestock_headcount` merita di essere trattato come feature e che
l'evidenza fornisce un primo intervallo da restringere. Analogamente, i
valori `WATER` osservati nei modelli vincenti delimitano regimi, non un
optimum.

### E16+ --- Parameter & Hyperparameter Tuning

I round successivi devono essere progettati per **restringere
progressivamente gli intervalli delle feature e degli iperparametri
supportati**, non come semplici repliche del torneo.

``` text
livestock_headcount
E15 initial bound: 4 ─────────────── 17
                         ↓
next round:       4 / 7 / 10 / 13 / 17
                         ↓
                  intervallo migliore
                         ↓
                     tuning fine
```

Ogni nuovo esperimento deve dichiarare **prima dell'esecuzione** il
proprio ruolo:

``` text
TRAINING EVIDENCE
VALIDATION EVIDENCE
TEST EVIDENCE
```

L'evidenza usata per scegliere o restringere un parametro non può essere
riutilizzata come prova indipendente della sua generalizzazione.

## Protocollo di revisione dei MODEL_SPEC

Dopo ogni round, la revisione non consiste nel copiare la strategia
vincente. Ogni modeler deve riesaminare indipendentemente i concetti
dell'ontologia e produrre:

``` text
concept_id
feature_status
relationship
e15_evidence
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

Una soglia osservata costituisce una **inizializzazione del search
space**, non un valore ottimale. Il round successivo deve restringere o
falsificare quell'intervallo.

## Ruolo dei modeler

Antigravity, Codex e Copilot sono **modeler indipendenti**. Ricevono la
stessa ontologia e la stessa evidenza, ma revisionano separatamente i
propri `MODEL_SPEC`.

Devono distinguere evidenza da inferenza, identificare feature, valutare
relazioni con il target, proporre range solo quando supportati,
dichiarare confidence/confounder, progettare esperimenti discriminanti e
definire condizioni di falsificazione.

Le divergenze tra modeler sono informative: indicano le parti del
modello sulle quali l'evidenza non consente ancora una conclusione
robusta.

## Stato corrente

-   **E15**: `EPISTEMICALLY CLOSED`
-   **Competitive winner**: `Copilot (2–0)`
-   **Frozen integrity**: `7/7 PASS`
-   **Test suite post-E15**: `102/102 PASS`
-   **E15 closure commit**: `922015f`
-   **Post-E15 maintenance commit**: `d599d0e`
-   **Next gate**: `MODEL CAPABILITY CHECK`

Il prossimo gate deve verificare che il runtime/model utilizzato da
ciascun modeler sia adeguato al compito:

> **feature identification → relationship inference → initial threshold
> discovery → experiment design**

senza overfitting sull'evidenza E15. Solo dopo viene autorizzata la
revisione indipendente dei `MODEL_SPEC`.

## Stato del Repository & Artifacts

### Model specs correnti

``` text
docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY.md
docs/model_specs/codex/MODEL_SPEC_CODEX.md
docs/model_specs/copilot/MODEL_SPEC_COPILOT.md
```

### E15

``` text
results/e15/E15_FINAL_TOURNAMENT_SYNTHESIS.md
results/e15/freeze/
results/e15/M1_antigravity_vs_codex/
results/e15/M2_codex_vs_copilot/
results/e15/M3_copilot_vs_antigravity/
```

Gli artefatti sotto `results/e15/freeze/` sono immutabili.

## Ambiente Python

La fonte canonica delle dipendenze è `pyproject.toml`. La directory
`.venv` è un artifact locale disposable.

Versione validata:

-   Python `3.12.13`
-   `kaggle-environments==1.32.7`
-   progetto installato in editable mode: `kaggriculture-agent==0.1.0`

`pyproject.toml` dichiara `requires-python = ">=3.10,<3.14"` per
compatibilità con le dipendenze di `kaggle-environments`.

### Creazione ambiente

``` powershell
.\scripts\setup_env.ps1 -Recreate
```

### Verifica ambiente

``` powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\pytest.exe tests/
.\.venv\Scripts\python.exe scriptsun_e15_tournament.py --validate
```

### Environment discipline

Antigravity, Codex, Copilot e altri modeler devono seguire:

``` text
Repository configuration → .venv → verification
```

Non cambiare dipendenze, versione Python o configurazione dell'ambiente
silenziosamente.

## Installazione ed esecuzione

``` powershell
# Attivazione ambiente
.\.venv\Scriptsctivate

# Suite completa
.\.venv\Scripts\pytest.exe tests/

# Verifica integrità E15
.\.venv\Scripts\python.exe scriptsun_e15_tournament.py --validate

# Generazione submission — solo quando autorizzata dal protocollo
.\.venv\Scripts\python.exe scriptsuild_submission.py
```

## Registri di progetto

-   [Experiment Log](docs/EXPERIMENT_LOG.md)
-   [Project State](docs/PROJECT_STATE.md)
-   [New Session Restart Point](docs/NEW_SESSION.md)
-   [E15 Final Tournament
    Synthesis](results/e15/E15_FINAL_TOURNAMENT_SYNTHESIS.md)
