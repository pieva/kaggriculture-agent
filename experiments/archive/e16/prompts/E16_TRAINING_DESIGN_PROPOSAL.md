# E16 --- TRAINING DESIGN PROPOSAL

**Stato:** `CANONICAL PROMPT — INDEPENDENT DESIGN PROPOSAL`\
**Fase:**
`E16 — TRAINING / INITIAL BOUNDING + INTERACTION DISCRIMINATION`

## 1. Scopo

Proporre il design sperimentale E16 a partire dal MODEL_SPEC consolidato
post-E15.

E16 è un esperimento di **TRAINING**. Non è VALIDATION e non è TEST. I
risultati E16 potranno essere usati per aggiornare bound, relazioni e
parametri, ma non potranno essere successivamente presentati come
evidenza indipendente di validazione o generalizzazione.

L'obiettivo non è trovare un optimum globale. L'obiettivo è ottenere il
massimo **information gain** con un budget sperimentale contenuto,
discriminando le principali regioni e interazioni ancora irrisolte dopo
E15.

## 2. Input obbligatori

Leggi integralmente, prima di formulare la proposta:

1.  `README.md`;
2.  `docs/model_specs/post_e15/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md`;
3.  la documentazione primaria E15 necessaria a verificare valori e
    provenance;
4.  la tua precedente capability check e MODEL_SPEC revision,
    esclusivamente come supporto secondario.

Il MODEL_SPEC consolidato finale è il riferimento canonico post-E15. Non
riaprire l'arbitraggio già chiuso salvo identificazione di un errore
fattuale che renderebbe invalido il design.

## 3. Vincoli epistemici

Devi rispettare tutti i seguenti vincoli:

-   non trasformare intervalli osservati in optima;
-   non trattare E15 come VALIDATION;
-   non usare `final_money` come feature causale;
-   distinguere `MODEL_VALIDITY`, `POLICY_REALIZATION` e
    `IMPLEMENTATION_FIDELITY`;
-   distinguere PARAMETER, HYPERPARAMETER, DERIVED_METRIC,
    OBSERVABILITY_REQUIREMENT e NOT_YET_TUNABLE;
-   distinguere richieste di azione da azioni effettivamente eseguite;
-   non confondere correlazione osservata con causalità;
-   non usare evidenza esterna osservazionale come sostituto di un
    confronto controllato;
-   non modificare file del repository;
-   non implementare policy;
-   non generare submission;
-   non definire ancora E16 come frozen.

## 4. Convenzione obbligatoria sulla superficie

Non usare `Q1`, `Q2`, `Q3` come sinonimi del numero totale di quadranti
posseduti.

Usa esclusivamente:

``` text
quadrants_owned = <int>
```

Gli identificatori ambientali `Q0/Q1/Q2/...` restano distinti dalla
quantità totale di quadranti.

Per questo proposal:

``` text
quadrants_owned = 2
```

è la **controlled E16 baseline**.

Non è un optimum e non è un land threshold frozen.

`quadrants_owned = 3` resta una regione condizionale non risolta, ma
**non è un fattore prioritario del proposal E16** salvo dimostrazione
che escluderlo renda il design non identificabile.

## 5. Problemi sperimentali prioritari

Il proposal deve concentrarsi su due interaction problems.

### E16-A --- Irrigation × crop working set

Obiettivo: localizzare meglio il bordo tra regime operativo
insufficiente e regime competitivo, evitando di assumere come soglia i
soli valori E15.

Concetti canonici rilevanti:

-   `watering_dispatch_priority` --- PARAMETER;
-   `watering_execution_rate` --- DERIVED_METRIC;
-   watering/service continuity;
-   `crop_surface_maintained`;
-   action/dispatch failure;
-   worker capacity disponibile.

E15 ha lasciato una regione intermedia insufficientemente osservata tra
i bundle a bassa superficie/servizio e quelli a maggiore
superficie/servizio.

Il proposal deve stabilire come campionare questa regione con il minor
numero di celle utile a identificare:

-   failure region;
-   transition region;
-   success/competitive working region;
-   eventuale interazione tra superficie coltivata e capacità di
    servizio.

### E16-B --- Livestock × pasture × crop opportunity cost

Obiettivo: discriminare herd scale, pasture allocation e costo
opportunità sulla superficie produttiva.

Concetti canonici rilevanti:

-   `livestock_headcount`;
-   pasture allocation;
-   crop/pasture trade-off;
-   feed dependency;
-   wheat/feed interaction;
-   livestock service burden;
-   deployable capital e operating cash come possibili confounder.

Non assumere che 4--7 animali sia un optimum. È una regione competitiva
osservata in E15; 17--18 appartiene al bundle di failure osservato; la
regione intermedia resta scarsamente osservata.

## 6. Fattori che NON devono esplodere il DOE

Non proporre un full factorial indiscriminato.

In particolare, salvo motivazione metodologica forte, tratta come
controlli o diagnostiche e non come fattori factorial principali:

-   workforce headcount;
-   crop mix dettagliato;
-   routing;
-   land acquisition timing;
-   cash policy;
-   endgame policy;
-   `productive_action_share`;
-   species-specific livestock margin;
-   market/revenue mix.

Se uno di questi deve necessariamente variare per rendere interpretabile
E16, dichiaralo e dimostra perché non può essere controllato.

`productive_action_share` è UNRESOLVED ma a **training priority LOW**:
non allocare celle dedicate senza una giustificazione eccezionale.

## 7. Osservabilità obbligatoria

Ogni proposta deve presupporre un event ledger capace di distinguere
richiesta, esecuzione ed effetto.

Come minimo devono essere osservabili:

-   episode;
-   player;
-   step;
-   actor/order;
-   requested action/payload;
-   executed action/payload;
-   failure/no-op reason;
-   quantity;
-   realized price;
-   realized value;
-   cash-flow category;
-   relevant state before/after;
-   provenance;
-   `quadrants_owned: int`;
-   daily serviced surface;
-   watering need denominator;
-   watering execution/success/failure;
-   pasture occupancy;
-   feed coverage;
-   necessary vs avoidable transit;
-   purchase-to-activation lag;
-   terminal inventory by product;
-   unsold terminal inventory quantity;
-   eventuale `unsold_inventory_value_estimate` con metodo e provenance
    espliciti.

`unsold_inventory_value_estimate` non è `realized_value`.

Se ritieni necessario un campo aggiuntivo per rendere falsificabile una
relazione, includilo nella proposta.

## 8. Budget e parsimonia

Progetta il **minimo DOE informativo**.

Non massimizzare il numero di celle. Minimizza il costo sperimentale
compatibilmente con:

1.  discriminazione delle interaction hypotheses;
2.  stima iniziale dei bound;
3.  identificazione dei principali failure modes;
4.  confronto replicabile tra celle;
5.  possibilità di falsificare l'ipotesi che guida ciascuna variazione.

Per ogni cella proposta devi poter rispondere:

> Quale distinzione epistemica perderemmo eliminando questa cella?

Se non esiste una risposta precisa, elimina la cella.

Indica separatamente:

-   numero di configurazioni/celle;
-   numero di seed per cella;
-   numero totale di episodi;
-   eventuale staged/adaptive design.

Puoi proporre un design staged nel quale E16-B dipenda da un risultato
di E16-A, purché la regola di avanzamento sia **pre-dichiarata** e non
scelta post hoc.

## 9. Seed e opponent protocol

Proponi un protocollo comune e riproducibile.

Specifica:

-   numero minimo di seed;
-   se gli stessi seed devono essere condivisi tra tutte le celle;
-   opponent/configurazione avversaria;
-   ordine o randomizzazione delle esecuzioni;
-   criterio per distinguere effetto del trattamento da seed/opponent
    variance.

Non usare seed selection post hoc.

## 10. Baseline reconstruction e controls

Dichiara esplicitamente:

-   baseline E16;
-   variabili frozen/control;
-   variabili manipolate;
-   derived metrics;
-   observability-only fields.

La baseline deve essere ricostruibile senza ambiguità.

Se un controllo non può essere mantenuto identico tra celle, dichiaralo
come confounder previsto.

## 11. Falsification-first design

Per ogni interaction problem formula prima:

1.  ipotesi;
2.  relazione attesa;
3.  osservazione che la falsificherebbe;
4.  solo dopo, le celle necessarie.

Evita design costruiti soltanto per confermare il MODEL_SPEC.

Una buona proposta E16 deve poter produrre un risultato che obblighi a
ridurre, eliminare o riclassificare almeno una delle feature candidate.

## 12. Metriche

`final_money` resta il target principale.

Non limitarti però al ranking finale. Specifica le metriche diagnostiche
necessarie per attribuire il risultato ai meccanismi proposti.

Come minimo considera:

-   final_money;
-   completion/disqualification;
-   watering execution/service;
-   maintained productive surface;
-   action failures/no-op;
-   livestock/pasture/feed state;
-   realized cash flows;
-   terminal unsold inventory;
-   worker/dispatch capacity;
-   capital deployment timing.

Non costruire una metrica composita con `final_money` incorporato come
input.

## 13. Output richiesto

Produci una sola proposta strutturata come segue.

### A. DESIGN SUMMARY

``` text
design_id:
training_goal:
design_type:
total_cells:
seeds_per_cell:
total_episodes:
staged: YES | NO
```

### B. HYPOTHESES

Per ogni ipotesi:

``` text
hypothesis_id:
concepts:
relationship:
current_evidence:
uncertainty_to_resolve:
falsification_condition:
```

### C. FACTORS AND CONTROLS

Tabella con:

``` text
variable
role
type
candidate_values_or_control
rationale
```

Ruoli ammessi:

``` text
MANIPULATED
CONTROL
DERIVED_METRIC
OBSERVABILITY
```

### D. EXPERIMENT CELLS

Per ogni cella:

``` text
cell_id:
factor_values:
comparison_role:
epistemic_question:
why_required:
```

### E. STAGE / ADVANCEMENT RULES

Se staged, definisci ex ante le regole che determinano quali celle/stage
vengono eseguiti successivamente.

Non usare formulazioni come "scegliere il migliore e provare altro". La
regola deve essere verificabile.

### F. SEED / OPPONENT PROTOCOL

Protocollo completo e riproducibile.

### G. TELEMETRY REQUIREMENTS

Campi minimi e metriche derivate necessarie.

### H. ANALYSIS PLAN

Definisci prima dei run:

-   confronti primari;
-   confronti secondari;
-   come interpretare interazioni;
-   come gestire failure/disqualification;
-   come trattare outlier;
-   quali conclusioni sono consentite;
-   quali conclusioni sono vietate.

### I. INFORMATION-GAIN AUDIT

Per ogni cella:

``` text
cell_id:
information_gained:
what_is_lost_if_removed:
```

Concludi indicando eventuali celle ridondanti eliminate durante il
design.

### J. COST

``` text
total_cells:
episodes_per_cell:
total_episodes:
relative_cost_vs_E15:
```

Se il costo è elevato, proponi una versione `MINIMAL` e una `PREFERRED`,
spiegando la differenza epistemica.

### K. DESIGN RISKS

Massimo 7 rischi concreti, ordinati per severità.

### L. RECOMMENDATION

Concludi con:

``` text
RECOMMENDED_DESIGN: <design_id>
READY_FOR_CROSS_REVIEW: YES | NO
BLOCKERS: NONE | ...
```

## 14. Criterio di qualità

La proposta migliore non è quella più complessa.

È quella che, con il minor numero ragionevole di episodi:

-   separa meglio le ipotesi concorrenti;
-   localizza i bound senza inventare optima;
-   rende visibili policy realization e implementation failures;
-   produce risultati falsificabili;
-   evita confondenti inutili;
-   prepara un successivo VALIDATION split realmente indipendente.

## 15. Divieti finali

Non:

-   modificare il MODEL_SPEC consolidato;
-   congelare E16;
-   implementare E16;
-   generare submission;
-   usare risultati E16 non ancora esistenti;
-   scegliere valori perché "sembrano ottimali";
-   reinterpretare `quadrants_owned = 2` come optimum;
-   chiamare TRAINING ciò che poi verrà riutilizzato come VALIDATION;
-   leggere o confrontare le proposte E16 degli altri modeler prima di
    aver completato la tua.

Il tuo compito termina con una **proposta indipendente di design E16
pronta per cross-review**.
