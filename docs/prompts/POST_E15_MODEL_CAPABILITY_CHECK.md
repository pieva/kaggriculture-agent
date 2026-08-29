# POST-E15 — MODEL CAPABILITY CHECK

> **Prompt canonico unico per Antigravity, Codex e Copilot**  
> Utilizzare lo stesso testo, senza adattamenti sostanziali, per i tre modeler.  
> Le esecuzioni devono essere indipendenti e non devono avere accesso agli output degli altri modeler.

Stai operando sul repository **Kaggriculture**.

Questa attività è un **CAPABILITY CHECK del modeler**, non una richiesta di implementazione, ottimizzazione della policy o generazione di una nuova submission.

## 1. Contesto metodologico

Kaggriculture viene utilizzato come ambiente sperimentale per l'**addestramento, il tuning e la validazione di modelli decisionali espliciti**.

La competizione costituisce il **benchmark/environment**, non il fine del progetto.

La fase **E15 è epistemicamente chiusa**.

L'evidenza E15 deve essere trattata come **TRAINING EVIDENCE** per la fase successiva.

```text
Victory != Model Validity.
Defeat != Model Falsification.
```

E15 **non determina valori ottimali**. Le osservazioni E15 possono supportare feature hypothesis, relazioni preliminari, failure/success region e initial candidate bounds.

## 2. Vincoli assoluti

- **NON modificare alcun file.**
- **NON modificare gli artefatti frozen E15.**
- **NON modificare alcun MODEL_SPEC.**
- **NON generare codice.**
- **NON generare submission.**
- **NON correggere o ottimizzare alcuna policy.**
- **NON assumere che la policy vincitrice E15 rappresenti il modello corretto.**
- **NON utilizzare conoscenza derivata dalle risposte di altri modeler.**
- **NON trasformare una singola osservazione E15 in un valore ottimale.**

Devi lavorare esclusivamente come **MODEL ANALYST**.

## 3. Lettura metodologica obbligatoria

Prima di iniziare qualsiasi analisi, **leggi integralmente il `README.md` corrente del repository**.

Il `README.md` definisce il quadro metodologico aggiornato di Kaggriculture e deve essere utilizzato per comprendere:

- che cosa viene considerato "modello";
- il ruolo della competizione come benchmark/environment;
- la distinzione tra model, policy e implementation;
- il significato di training, tuning, validation e test;
- il ruolo delle feature e della canonical ontology;
- il significato epistemico degli esperimenti E01–E15;
- il passaggio corrente da feature discrimination a initial bounding e successivamente a parameter/hyperparameter tuning.

Usa il `README.md` come **riferimento metodologico**, NON come sostituto dell'evidenza sperimentale primaria E15.

Se il `README.md` contiene interpretazioni o sintesi dei risultati E15, trattale come contesto metodologico o ipotesi già formulate, non come evidenza primaria sufficiente a dimostrarle.

Per ricostruire ciò che E15 ha effettivamente osservato devi risalire, quando disponibili, agli artefatti canonici/frozen pertinenti.

Mantieni distinta la provenienza di:

1. **METHODOLOGICAL FRAME** — definizioni e metodo;
2. **PRIMARY E15 EVIDENCE** — osservazioni e misure frozen;
3. **POST-E15 INTERPRETATION** — interpretazioni già formulate;
4. **YOUR INFERENCE** — inferenze prodotte autonomamente in questo capability check.

Non assumere che una proposizione sia empiricamente dimostrata soltanto perché compare nel `README.md`, in `NEW_SESSION.md` o in un documento di sintesi.

## 4. Fonti

Esamina autonomamente il repository e identifica le fonti canoniche necessarie a ricostruire E15.

Distingui sempre:

- evidenza osservata;
- interpretazione;
- inferenza;
- ipotesi;
- informazione non osservabile o insufficiente.

Quando possibile, indica il **file o artefatto** da cui deriva ciascuna evidenza rilevante.

Non colmare lacune informative mediante supposizioni.

## 5. Obiettivo

Valuta ciò che E15 permette realmente di apprendere sul modello decisionale.

Devi dimostrare capacità di:

1. ricostruire fedelmente l'evidenza E15;
2. non confondere correlazione di score con causalità;
3. distinguere:
   - `MODEL_VALIDITY`;
   - `POLICY_REALIZATION`;
   - `IMPLEMENTATION_FIDELITY`;
4. identificare i concetti candidati a costituire feature del modello;
5. classificare ciascun concetto come:
   - `FEATURE`;
   - `NOT_FEATURE`;
   - `UNRESOLVED`;
6. inferire, quando supportato, la relazione preliminare feature → target;
7. distinguere:
   - failure region;
   - success region;
   - unresolved region;
8. proporre soltanto initial candidate threshold/range supportati dall'evidenza;
9. identificare confounder e limiti di osservabilità;
10. distinguere **requested market orders** da **executed transactions**;
11. evitare di utilizzare E15 come validation evidence indipendente;
12. progettare il prossimo esperimento in modo da restringere o falsificare le ipotesi correnti.

Il target primario è **FINAL_MONEY**.

## 6. Principio di calibrazione

Preferisci `UNRESOLVED` a una conclusione non supportata.

Un intervallo incompleto ma giustificato è migliore di una soglia precisa inventata.

Non cercare necessariamente un optimum.

Non assumere monotonicità.

Una relazione può essere:

- `positive`;
- `negative`;
- `monotonic`;
- `non_monotonic`;
- `thresholded`;
- `conditional`;
- `unresolved`.

Usa soltanto classificazioni sostenute dall'evidenza disponibile.

## 7. Analisi richiesta

### A. Evidence reconstruction

Ricostruisci sinteticamente:

- struttura dell'esperimento E15;
- risultati osservati;
- evidenze strategiche rilevanti;
- limiti dell'evidenza disponibile.

Se rilevi differenze tra requested actions/orders ed executed actions/transactions, rendile esplicite.

### B. Layer diagnosis

Valuta separatamente, senza inferire automaticamente un livello dall'altro:

#### MODEL_VALIDITY

- cosa suggerisce E15 sulla validità delle feature hypothesis?

#### POLICY_REALIZATION

- quanto le policy osservate realizzano effettivamente i modelli dichiarati?

#### IMPLEMENTATION_FIDELITY

- quale evidenza permette di verificare che l'implementazione realizzi correttamente la policy?

Quando l'evidenza non permette una conclusione, indica `UNRESOLVED`.

### C. Feature analysis

Individua autonomamente i concetti rilevanti emersi da E15.

Per **CIASCUN concetto** usa **ESATTAMENTE** questo schema:

```text
concept_id:
feature_status: FEATURE | NOT_FEATURE | UNRESOLVED
relationship:
e15_evidence:
failure_region:
success_region:
candidate_threshold_or_interval:
confidence:
confounders:
next_test_values:
falsification_condition:
```

Regole:

- `candidate_threshold_or_interval` **NON è un optimum**;
- non inventare estremi non osservati;
- separa valori osservati da valori proposti per il prossimo test;
- `confidence` deve riflettere la qualità dell'evidenza, non la plausibilità intuitiva della spiegazione;
- `next_test_values` deve essere scelto per aumentare informazione e discriminazione, non semplicemente per massimizzare il prossimo score;
- `falsification_condition` deve indicare quale risultato futuro indebolirebbe o falsificherebbe l'ipotesi.

### D. Confounder analysis

Identifica i principali confounder che impediscono di attribuire variazioni di `FINAL_MONEY` a una singola feature.

Per ciascuno indica:

- quali feature mette in relazione;
- quale interpretazione può falsamente suggerire;
- quale osservabilità manca;
- quale esperimento potrebbe separarne gli effetti.

### E. Candidate design for the next common training round

Proponi il **disegno candidato per il prossimo round comune di training** che, secondo la tua analisi indipendente, massimizza l'**information gain** sulle principali incertezze emerse.

Non assumere che questa proposta verrà eseguita direttamente. Sarà confrontata con le proposte indipendenti degli altri modeler e sottoposta a **cross-review** prima della definizione dell'unico esperimento comune successivo.

Cerca il **minimo disegno sperimentale sufficiente** a discriminare le ipotesi principali: non aggiungere test che non aumentino materialmente l'informazione ottenibile.

Specifica:

```text
training_or_validation: TRAINING | VALIDATION | TEST
hypothesis:
feature_under_test:
controlled_variables:
test_values:
expected_discrimination:
falsification_condition:
evidence_that_must_be_recorded:
```

**ATTENZIONE:** l'evidenza E15 è già `TRAINING EVIDENCE`. Non può essere riutilizzata come validation o test evidence indipendente.

### F. Epistemic audit

Concludi indicando esplicitamente:

#### SUPPORTED

Conclusioni che ritieni direttamente sostenute da E15.

#### PROVISIONAL

Inferenze ragionevoli ma ancora da sottoporre a tuning/falsificazione.

#### UNRESOLVED

Questioni che E15 non consente di determinare.

#### DO_NOT_INFER

Conclusioni apparentemente plausibili che **NON** devono essere ricavate dall'evidenza disponibile.

## 8. Output finale

Produci un **report Markdown** come risposta del capability check.

Non modificare il repository.

Non implementare nulla.

Non proporre una nuova `MODEL_SPEC` completa.

Non scegliere una policy vincitrice.

Non dichiarare parametri ottimali.

Il tuo compito termina con:

1. ricostruzione dell'evidenza;
2. feature discrimination;
3. initial bounding;
4. identificazione dei confounder;
5. proposta indipendente del candidate design per il prossimo round comune e falsificabile.

Questo output verrà confrontato con output indipendenti prodotti da altri modeler sullo **stesso identico task**.
