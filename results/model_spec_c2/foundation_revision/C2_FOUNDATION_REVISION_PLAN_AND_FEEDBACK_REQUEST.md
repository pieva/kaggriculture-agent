# C2 --- Sintesi delle Periodic Review e piano di revisione della Foundation

``` text
DOCUMENT_TYPE: COMMON_SYNTHESIS_AND_FEEDBACK_REQUEST
PHASE: REVIEW / FOUNDATION REDESIGN
STATUS: PROPOSED â€” REQUESTING INDEPENDENT FEEDBACK
BUILD: NO
TOURNAMENT_RUN: NO
KAGGLE_RUN: NO
```

## 1. Scopo

Le tre review indipendenti di Antigravity, Codex e Copilot convergono
sulla necessitÃ  di evolvere C2 da una policy prevalentemente
`threshold-centric / reactive` verso una Foundation capace di
rappresentare esplicitamente cicli biologici, periodi e fasi, finestre e
deadline di servizio, carico futuro, capacitÃ  prenotata, commitment
produttivi, decision point e override reattivi.

Questa sintesi propone il piano comune per la prossima revisione della
Foundation e i nuovi obiettivi economici. **Non autorizza ancora
modifiche alla Foundation o al codice.** Prima di procedere sono
richiesti tre feedback indipendenti.

## 2. Evidenza consolidata

Replay esterni selezionati:

-   Q0 --- `103484828.json`, LuCcc: **56.772**, un solo quadrante, forte
    regolaritÃ  temporale e alta densitÃ  produttiva.
-   Q2 --- `103473619.json`, Gordeev: **88.648**.
-   Q2 --- `103462357.json`, Dipin: **95.496**.
-   Q3 --- `103464592.json`, ÐŸÐµÑ‚Ð°Ñ€: **95.475**.

LuCcc dimostra che 50k+ Ã¨ raggiungibile senza espansione. I replay
multi-Q mostrano che la scala puÃ² innalzare fortemente il ceiling, ma
non che `BUY_LAND` sia sufficiente: superficie, workforce, cicli
biologici, routing e monetizzazione devono restare compatibili.

Codex, dopo aver allineato le azioni alle transizioni
`STATE_t -> ACTION_t -> STATE_t+1`, osserva regolaritÃ  temporali
candidate nell'ordine di 24/48/72/96 step e mostra che tali periodi
devono essere verificati per entitÃ  e riconciliati con la semantica
dell'engine prima di diventare canonici.

## 3. Convergenza delle tre review

``` text
BASE PRODUCTION       = PLAN
MARKET CONDITION      = REACT
OPERATIONAL DEVIATION = REACT
LEGALITY / LIQUIDITY  = HARD OVERRIDE
```

La formulazione viene raffinata cosÃ¬:

> PLAN e REACT non sono categorie immutabili di azioni. Si alternano tra
> punti decisionali e commitment produttivi.

Esempio:

``` text
HARVEST
-> REVIEW
-> DEFINE / REACT sul mercato e sulle evidenze
-> SELECT next crop
-> PLAN biological cycle
-> COMMIT / PLANT
-> VERIFY services and deadlines
-> HARVEST
-> REVIEW
-> ...
```

Una volta effettuato il commitment, il mercato non deve continuamente
riscrivere il ciclo biologico. Il `REACT` torna dominante al successivo
decision point, salvo override.

## 4. Ciclo guida della nuova policy

La prossima revisione deve valutare esplicitamente:

``` text
DEFINE
-> PLAN
-> BUILD / COMMIT
-> VERIFY
-> REVIEW
-> DEFINE
-> ...
```

### DEFINE --- prevalentemente REACT

Osserva mercato, prezzi, domanda/inventory, risultati precedenti,
capacitÃ  disponibile, horizon, alternative ed evidenza sperimentale.
Decide **cosa** produrre o quale capacitÃ  riallocare.

### PLAN

Definisce periodo biologico, phase, service windows, deadline,
staggering, routing, input, workforce, future workload, capacity
reservation, output atteso e completion evidence.

### BUILD / COMMIT

Alloca tile/pasture, seed/animal, capitale, worker capacity, route
capacity ed eventuale nuova superficie.

### VERIFY

Controlla `period_adherence`, service completion, legality, deadline,
transizione effettiva, deviazioni e forecast error.

### REVIEW

Misura output, monetizzazione, worker-actions, capitale, service misses,
yield per ciclo e rendimento relativo; decide quali evidenze passano
alla nuova DEFINE.

## 5. Principio: periodo -\> capacitÃ  futura

La periodicitÃ  non deve produrre una policy rigidamente a timer.

``` text
BIOLOGICAL PERIOD
-> FUTURE SERVICE DEMAND
-> CAPACITY RESERVATION
-> COMMITMENT
-> EXECUTION
-> TRANSITION VERIFICATION
```

Una nuova entitÃ  Ã¨ realmente `SERVICEABLE` solo se il suo profilo
temporale puÃ² essere sostenuto almeno fino al primo output
monetizzabile.

I vecchi cap statici devono quindi essere rivalutati come proxy di:

``` text
required_slots(window) <= available_slots(window)
```

Le soglie restano ammissibili come safety guard, legality predicate o
protezione di liquiditÃ .

# 6. Piano di revisione della Foundation

## 6.1 ONTOLOGY --- estensione controllata

La periodicitÃ  Ã¨ conoscenza comune del dominio e deve essere
formalizzata prima dei MODEL_SPEC.

Concetti candidati da verificare:

``` text
BIOLOGICAL_PERIOD
CYCLE_PHASE
SERVICE_PERIOD
SERVICE_WINDOW
PRODUCTION_PERIOD
HARVEST_WINDOW
SERVICE_DEADLINE
CAPACITY_REQUIREMENT
CAPACITY_RESERVATION
COMMITMENT
DECISION_POINT
REACTIVE_OVERRIDE
```

Non tutti devono necessariamente diventare nuovi `concept_id`: occorre
distinguere concetti primitivi, proprietÃ  e relazioni.

La ricognizione deve coprire **tutte le specie engine-supported**,
incluse almeno:

``` text
CROPS
WHEAT
STRAWBERRY
MELON
CARROT
TOMATO

ANIMALS
COW
SHEEP
CHICKEN
```

I valori canonici devono provenire dalla semantica verificata
dell'engine. I replay servono come evidenza empirica e validazione.

## 6.2 FEATURE MODEL --- revisione sostanziale

Dal modello:

``` text
current state + need + eligibility + threshold
```

a un modello che includa:

``` text
cycle_phase
origin_step
nominal_period
next_due_step
service_window
hard_deadline
expected_output
required_capacity
reserved_capacity
deadline_slack
period_adherence
completion_evidence
forecast_error
```

`SERVICEABLE_SURFACE` deve diventare capacitÃ  sostenibile **nel tempo**,
non soltanto superficie teoricamente servibile nello stato corrente.

## 6.3 STATE MACHINE --- revisione sostanziale

Deve incorporare:

``` text
DEFINE
PLAN
BUILD / COMMIT
VERIFY
REVIEW
```

`PLAN` governa biological calendar, service scheduling, staggering,
capacity reservation, workforce, routing, completion windows ed
expansion schedule.

`REACT` governa la scelta della prossima produzione al decision point,
mercato, liquiditÃ , missed service, weed, deviazioni, opportunitÃ
eccezionali e terminal horizon.

`HARD OVERRIDE` protegge da illegalitÃ , input/capitale insufficienti,
commitment non sostenibile e deadline critiche.

Principio:

> **REACT sceglie e rialloca capacitÃ  nei decision point. PLAN governa
> il commitment tra un decision point e il successivo. VERIFY controlla
> che il piano resti realizzabile.**

## 6.4 MODEL_SPEC --- solo dopo Foundation freeze

Sequenza:

``` text
ONTOLOGY
-> FEATURE MODEL
-> STATE MACHINE
-> FOUNDATION CROSS-REVIEW
-> FOUNDATION FREEZE
-> THREE INDEPENDENT MODEL_SPEC REVISIONS
```

La Foundation non deve imporre crop mix, livestock mix, worker count,
quadrant count, percentuale di exploration, strategia di mercato o
sequenza di espansione.

## 7. Espansione

> **L'espansione non Ã¨ nÃ© condizione sufficiente nÃ© comportamento da
> escludere. Deve essere trattata come replica controllata di capacitÃ
> produttiva funzionante.**

``` text
Q0 stable productive cycle
-> forecast clone workload
-> reserve capacity
-> phase-shift replica
-> activate Q1
-> verify retained cycle performance
-> eventual Q2/Q3
```

Non assumere scaling lineare.

## 8. Exploration by replacement

Per ora non viene proposta una percentuale fissa di innovazione.

``` text
Q0
= best-known productive plan / CONTROL

Q1 and Q2
= mostly scale best-known plan
+ partial replacement of worst performers
```

L'esperimento parte al naturale decision point, senza interrompere cicli
funzionanti:

``` text
cycle completion
-> REVIEW
-> identify worst performer / knowledge gap
-> DEFINE alternative
-> PLAN full experimental cycle
-> BUILD
-> VERIFY
-> REVIEW
```

> **Exploration by replacement, not by disruption.**

Gli esperimenti devono progressivamente coprire le varietÃ  rilevanti,
comprese quelle finora trascurate come `CHICKEN`, completando cicli
sufficienti a produrre evidenza utile.

Il confronto Q0 vs Q1/Q2 avviene nello stesso mercato e nella stessa
partita. La telemetria deve perÃ² attribuire correttamente capitale,
worker-actions, service load e monetized output ai diversi moduli.

# 9. Nuovi obiettivi economici

``` text
MEAN FINAL MONEY < 50,000
=> FAIL

50,000 <= MEAN FINAL MONEY < 80,000
=> MATERIAL IMPROVEMENT, TARGET NOT ACHIEVED

MEAN FINAL MONEY >= 80,000
=> TARGET ACHIEVED
```

``` text
TARGET_MEAN_FINAL_MONEY: >= 80000
FAILURE_BELOW: 50000
```

Il floor Ã¨ coerente con l'evidenza 50k+ su Q0. Il target 80k resta
inferiore agli score esterni osservati di circa 88--95k ed Ã¨ competitivo
ma empiricamente plausibile.

## 10. Metriche richieste nel prossimo ciclo

Metrica primaria:

``` text
Mean Final Money
```

Metriche causali minime:

``` text
period_adherence_by_entity
due_events
completed_in_window
hard_deadline_miss
reserved_slots
consumed_slots
capacity_forecast_error
service_peak
ACTIVE_SURFACE
SERVICEABLE_SURFACE
PRODUCTIVE_SURFACE
MONETIZED_OUTPUT
monetized_output_per_worker_action
monetized_output_per_entity_period
replant_delay
collection_delay
noop_action_rate
sellthrough_lag
cash_trajectory
feed_coverage
retained_cycle_yield_after_expansion
```

# 11. Sequenza operativa proposta

``` text
EXTERNAL REPLAY EVIDENCE
-> THREE INDEPENDENT PERIODIC REVIEWS
-> COMMON SYNTHESIS
-> THREE INDEPENDENT FEEDBACKS ON FOUNDATION PLAN
-> ONTOLOGY PERIODIC EXTENSION
-> FEATURE MODEL REVISION
-> STATE MACHINE REVISION
-> FOUNDATION CROSS-REVIEW
-> FOUNDATION FREEZE
-> THREE INDEPENDENT MODEL_SPEC REVISIONS
-> BUILD
-> REAL-ENGINE VERIFY
-> COMMON TOURNAMENT ON INDEPENDENT SEEDS
-> REVIEW AGAINST 50k / 80k
-> eventual SHIP / KAGGLE
```

Nessun nuovo Kaggle run Ã¨ autorizzato in questa fase.

# 12. Richiesta di feedback indipendente ai tre modeler

## Mandato

Antigravity, Codex e Copilot devono leggere **questa sintesi comune** e
produrre ciascuno un feedback indipendente.

Non modificare ancora Ontology, Feature Model, State Machine,
MODEL_SPEC, codice, configurazioni o test. Questa Ã¨ una fase `REVIEW`.

### Domande obbligatorie

1.  La sintesi rappresenta correttamente l'evidenza dei quattro replay e
    delle tre periodic review?
2.  Quali conclusioni sono supportate direttamente e quali restano
    ipotesi?
3.  La sequenza
    `Ontology -> Feature Model -> State Machine -> MODEL_SPEC` Ã¨
    corretta?
4.  Quali concetti periodici devono entrare nell'Ontology e quali devono
    restare proprietÃ /feature derivate?
5.  Quali periodi biologici possono essere congelati dall'engine e quali
    richiedono ancora verifica?
6.  La definizione futura di `SERVICEABLE` basata sulla capacitÃ
    prenotabile nel tempo Ã¨ corretta e implementabile?
7.  Il ciclo `DEFINE -> PLAN -> BUILD/COMMIT -> VERIFY -> REVIEW` Ã¨
    adatto alla State Machine o confonde process state e domain state?
8.  `REACT at decision points / PLAN after commitment` Ã¨
    sufficientemente preciso?
9.  `Exploration by replacement` su Q1/Q2 Ã¨ metodologicamente valida?
    Quali confondenti vanno controllati rispetto a Q0?
10. La Foundation lascia sufficiente libertÃ  ai MODEL_SPEC o incorpora
    giÃ  scelte strategiche?
11. Quali parti aumentano complessitÃ  senza evidenza sufficiente?
12. I target `<50k FAIL / >=80k TARGET` sono adeguati senza diventare
    parametri di tuning?
13. Qual Ã¨ il principale rischio tecnico o metodologico?
14. Quale modifica al piano Ã¨ indispensabile prima di procedere?

### Formato

``` text
VERDICT:
SUPPORTED:
PARTIALLY_SUPPORTED:
NOT_SUPPORTED:
ONTOLOGY_CHANGES:
FEATURE_MODEL_CHANGES:
STATE_MACHINE_CHANGES:
MODEL_SPEC_BOUNDARY:
EXPLORATION_REVIEW:
TARGET_REVIEW:
MAIN_RISK:
MANDATORY_CHANGE_BEFORE_PROCEEDING:
FINAL_RECOMMENDATION:
```

Salvare come:

``` text
results/model_spec_c2/foundation_revision_feedback/
ANTIGRAVITY_C2_FOUNDATION_REVISION_FEEDBACK.md

results/model_spec_c2/foundation_revision_feedback/
CODEX_C2_FOUNDATION_REVISION_FEEDBACK.md

results/model_spec_c2/foundation_revision_feedback/
COPILOT_C2_FOUNDATION_REVISION_FEEDBACK.md
```

### Vincolo di indipendenza

Ogni modeler deve produrre e congelare il proprio feedback **prima di
leggere i feedback degli altri due**.

Non cercare consenso artificiale. Le divergenze motivate sono evidenza
utile.

# 13. Criterio di uscita

Dopo i tre feedback, classificare ogni osservazione:

``` text
ACCEPT
REJECT
DEFER
REQUIRES_EVIDENCE
```

Solo allora autorizzare:

``` text
ONTOLOGY REVISION
-> FEATURE MODEL REVISION
-> STATE MACHINE REVISION
```

Non prima.

``` text
FOUNDATION_REVISION_PLAN_STATUS: PROPOSED
TARGET_MEAN_FINAL_MONEY: >= 80000
FAILURE_BELOW: 50000
AWAITING_INDEPENDENT_FEEDBACK: ANTIGRAVITY, CODEX, COPILOT
BUILD_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
