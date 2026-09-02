# POST-E15 --- MODEL_SPEC INDEPENDENT REVISION

> **Prompt canonico unico per Antigravity, Codex e Copilot**\
> Usare lo stesso testo per i tre modeler. L'unica variabile esterna
> ammessa è `MODELER_ID = ANTIGRAVITY | CODEX | COPILOT`. Le esecuzioni
> devono restare indipendenti.

Stai operando sul repository **Kaggriculture**.

Questa attività è una **REVISIONE INDIPENDENTE DEL MODEL_SPEC**
successiva alla chiusura epistemica di E15 e al superamento del POST-E15
MODEL CAPABILITY CHECK.

Non devi implementare una policy, generare codice, creare submission o
definire unilateralmente E16.

## 1. Obiettivo

Revisiona il MODEL_SPEC E15 del modeler identificato da `MODELER_ID`
usando: 1. quadro metodologico corrente; 2. evidenza primaria/frozen
E15; 3. capability check prodotto dallo stesso modeler; 4. inferenze
autonome chiaramente distinte dalle fonti.

Progressione:
`FEATURE IDENTIFICATION → RELATIONSHIP INFERENCE → INITIAL THRESHOLD/RANGE DISCOVERY → PARAMETER/HYPERPARAMETER TUNING`.

La revisione NON deve produrre valori ottimali.

## 2. Vincoli assoluti

-   NON modificare gli artefatti frozen E15.
-   NON sovrascrivere il MODEL_SPEC E15 frozen.
-   NON leggere output POST-E15 degli altri modeler.
-   NON copiare la policy o il MODEL_SPEC del vincitore E15.
-   NON generare codice o submission.
-   NON eseguire tuning o nuovi match.
-   NON utilizzare E15 come validation/test evidence indipendente.
-   NON trasformare valori osservati E15 in optimum.
-   NON progettare unilateralmente E16.
-   NON modificare altri file oltre al singolo artefatto richiesto.

`Victory != Model Validity.`\
`Defeat != Model Falsification.`

## 3. Letture obbligatorie

Prima della revisione: 1. leggi integralmente il `README.md` corrente;
2. identifica e leggi il MODEL_SPEC E15 frozen di `MODELER_ID`; 3.
consulta l'ontologia E15 frozen; 4. ricostruisci l'evidenza primaria E15
pertinente; 5. leggi il capability check POST-E15 prodotto dallo stesso
`MODELER_ID`.

Non leggere capability check o revisioni degli altri modeler.

Distingui sempre: 1. **METHODOLOGICAL FRAME** 2. **E15 FROZEN MODEL
DECLARATION** 3. **PRIMARY E15 EVIDENCE** 4. **POST-E15 SELF CAPABILITY
CHECK** 5. **YOUR INFERENCE**

Se il capability check contiene una conclusione non sostenuta
dall'evidenza primaria, correggila e dichiaralo.

## 4. Regole epistemiche

Per ogni concetto usa `FEATURE`, `NOT_FEATURE` o `UNRESOLVED`.

### FEATURE

Il concetto resta nel feature space per il prossimo training. La
relazione può essere `positive`, `negative`, `monotonic`,
`non_monotonic`, `thresholded`, `conditional`, `interaction` o
`unresolved`. Non-monotonicità non implica `NOT_FEATURE`.

### NOT_FEATURE

Usalo solo se l'evidenza supporta realmente rimozione o forte
deprioritizzazione nel regime modellato. Non basta che "più X non è
sempre meglio", che il valore maggiore abbia perso un match, che
esistano confounder o che non emerga monotonicità.

### UNRESOLVED

Usalo quando l'evidenza è insufficiente, il concetto non è isolato,
esistono confounder non separati o manca osservabilità. Preferisci
`UNRESOLVED` alla falsa precisione.

## 5. Initial bounds

`current_initial_bound` delimita soltanto una regione per il prossimo
training. Non è optimum, target definitivo, parametro frozen o soglia
causale dimostrata.

Distingui sempre valori osservati, regioni non osservate e valori
proposti.

`failure observed <= A` e `success observed >= B` NON autorizzano
`threshold = B` o `optimum = B`.

Se non esiste un bound utile, usa `UNRESOLVED` o `not_established`.

## 6. Parameter vs hyperparameter

Per ogni concetto utile indica: - `PARAMETER` - `HYPERPARAMETER` -
`DERIVED_METRIC` - `OBSERVABILITY_REQUIREMENT` - `NOT_YET_TUNABLE`

Motiva brevemente. Non trasformare automaticamente ogni `concept_id` in
parametro controllabile.

## 7. Revisione richiesta

### A. Baseline reconstruction

Riassumi principi del MODEL_SPEC E15, feature hypothesis ex ante,
comportamento E15, divergenze modello/policy/implementazione e
proposizioni supportate, indebolite, falsificate o unresolved.

Mantieni separati `MODEL_VALIDITY`, `POLICY_REALIZATION`,
`IMPLEMENTATION_FIDELITY`.

### B. Concept-by-concept revision

Per **CIASCUN concetto** usa esattamente:

``` text
concept_id:
feature_status: FEATURE | NOT_FEATURE | UNRESOLVED
e15_relationship:
current_initial_bound:
parameter_or_hyperparameter: PARAMETER | HYPERPARAMETER | DERIVED_METRIC | OBSERVABILITY_REQUIREMENT | NOT_YET_TUNABLE
next_training_values:
confounders:
validation_requirement:
falsification_condition:
change_from_e15_spec: UNCHANGED | REVISED | ADDED | DEPRIORITIZED | REMOVED
change_rationale:
```

`next_training_values` sono candidati, non il design definitivo E16. Se
un concetto non è controllabile, non forzare valori numerici.
`validation_requirement` deve indicare evidenza futura indipendente
necessaria dopo il tuning.

### C. Feature interaction map

Per ciascuna interazione:

``` text
interaction_id:
features:
reason:
current_evidence:
confounding_risk:
training_implication:
```

Distingui interazioni empiricamente supportate da ipotesi plausibili.

### D. Observability requirements

Verifica esplicitamente la necessità di: - requested vs executed
actions; - requested vs executed market transactions; - quantità e
prezzo realizzati; - action success/failure reason; - daily
maintained/serviced surface; - cash-flow breakdown; - movement
necessario vs overhead; - purchase-to-activation/payback lag.

Non dichiarare mancante ciò che l'evidenza primaria rende già
sufficientemente osservabile.

### E. Candidate training priorities

Ordina le incertezze:

``` text
priority:
concept_or_interaction:
information_gap:
why_it_matters:
candidate_values_or_measurement:
expected_information_gain:
```

Questa sezione alimenta il successivo design comune E16. NON assemblare
E16 completo.

### F. Changeset rispetto al MODEL_SPEC E15

  ---------------------------------------------------------------------------------
  Concept     E15                 Revised     Change      Evidence    Remaining
              status/hypothesis   status                  basis       uncertainty
  ----------- ------------------- ----------- ----------- ----------- -------------

  ---------------------------------------------------------------------------------

### G. Epistemic audit

Concludi con: - **RETAIN** - **REVISE** - **DEPRIORITIZE_OR_REMOVE** -
**UNRESOLVED** - **DO_NOT_FREEZE_YET**

## 8. Output

Produci un unico report Markdown e salvalo in:

``` text
docs/model_specs/post_e15/<MODELER_ID>_MODEL_SPEC_REVISION.md
```

Puoi creare `docs/model_specs/post_e15/` se non esiste. Non modificare
altri file.

Il documento è una **candidate MODEL_SPEC revision**: non sostituisce il
MODEL_SPEC frozen E15 e non è ancora il MODEL_SPEC definitivo del round
successivo.

## 9. Condizione di chiusura

Il task termina con: 1. baseline reconstruction; 2. concept-by-concept
revision; 3. feature interaction map; 4. observability requirements; 5.
candidate training priorities; 6. changeset; 7. epistemic audit; 8. file
Markdown nella destinazione prescritta.

Non procedere a cross-review, arbitraggio, design E16 definitivo, policy
o codice.
