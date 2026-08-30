# CODEX C2 â€” Feedback indipendente sul piano di revisione Foundation

```text
AGENT: CODEX
FEEDBACK_ID: CODEX-C2-FOUNDATION-REVISION-FEEDBACK-R1
PHASE: REVIEW
INDEPENDENT_FREEZE: YES
OTHER_MODELER_FEEDBACK_READ: NO
FOUNDATION_MODIFIED: NO
MODEL_SPEC_MODIFIED: NO
CODE_MODIFIED: NO
BUILD_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Fonti usate:

- sintesi comune `C2_FOUNDATION_REVISION_PLAN_AND_FEEDBACK_REQUEST.md`;
- quattro replay grezzi giÃ  analizzati nella periodic review Codex;
- periodic review Codex congelata;
- `ONTOLOGY_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md` e
  `KAGGRICULTURE_STATE_MACHINE_C2.md` correnti;
- metadata e transizioni della versione locale engine Kaggriculture `0.1.0`.

Il nome e la presenza di file di feedback altrui non sono stati usati come
evidenza; il loro contenuto non Ã¨ stato letto.

## VERDICT:

```text
PARTIALLY_SUPPORTED
PROCEED_ONLY_AFTER_MANDATORY_CHANGES
```

La direzione periodo -> carico futuro -> capacitÃ  Ã¨ corretta. Il piano non Ã¨
ancora pronto per avviare la revisione perchÃ© mescola tre livelli diversi:

1. semantica e transizioni dell'engine;
2. feature predittive e contesto di policy;
3. lifecycle del controller e protocollo sperimentale.

La nuova Foundation deve rendere espliciti i collegamenti tra questi livelli,
non fonderli in una sola State Machine. Prima di modellare reservation o
commitment occorre inoltre correggere due fatti engine: la specie avicola Ã¨
`GOOSE`, non `CHICKEN`, e la produzione base animale non Ã¨ condizionata a
`fed_today` nel modo dichiarato dalla State Machine corrente.

## SUPPORTED:

### Evidenza direttamente supportata

- I replay mostrano regolaritÃ  temporali per entitÃ . Nel caso Codex sono
  osservate candidate cadence 24/48/72/96 step con la configurazione a 24
  turn/day.
- LuCcc dimostra l'esistenza di almeno una traiettoria da 56.772 con un solo
  quadrante, 25 entitÃ  produttive al picco e 100/100 HARVEST effettivi.
- Gordeev, Dipin e Petar mostrano associazione tra architetture multi-Q e score
  88â€“95k, senza dimostrare che il solo acquisto del terreno causi lo score.
- I periodi biologici restano visibili in architetture diverse: crop-heavy,
  mixed livestock e sheep-dominant.
- La separazione tra ordine emesso ed effetto osservato Ã¨ necessaria. Petar ha
  389 richieste HARVEST ma soltanto 197 effetti, mentre LuCcc ha 100/100.
- `SERVICEABLE_SURFACE` deve includere una dimensione temporale futura; lo
  stato corrente e il raw headcount non bastano.
- LegalitÃ , affordability, inventory e hard deadlines devono restare guardie,
  anche in una policy pianificata.
- La Foundation deve precedere le revisioni indipendenti dei MODEL_SPEC e
  nessun BUILD deve iniziare prima del freeze comune.
- L'espansione deve distinguere terreno posseduto, attivato, serviceable,
  produttivo e monetizzato.

### Conclusioni architetturali supportate come direzione

```text
BIOLOGICAL PERIOD
-> FUTURE SERVICE DEMAND
-> CAPACITY FEASIBILITY
-> COMMITMENT
-> EXECUTION
-> TRANSITION VERIFICATION
```

Ãˆ supportato anche il principio secondo cui un commitment biologico non deve
essere riscritto continuamente da variazioni di mercato. Questo Ã¨ perÃ² un
contratto del controller da falsificare, non una legge dell'engine.

## PARTIALLY_SUPPORTED:

1. **RappresentativitÃ  delle tre review.** La sintesi Ã¨ coerente con la review
   Codex e con i replay primari. Non posso certificare in questo feedback che
   rappresenti integralmente le review Antigravity/Copilot senza violare il
   vincolo di indipendenza.
2. **`BASE PRODUCTION = PLAN`.** Ãˆ un'ipotesi forte e plausibile: l'engine ha
   cicli deterministici, ma i replay non contengono un controfattuale
   plan-driven vs threshold-only a bundle invariato.
3. **Scala multi-Q.** Gli score alti rendono plausibile un ceiling superiore,
   ma scala, mix, mercato, routing, workforce e implementazione sono confusi.
4. **Capacity reservation.** Ãˆ implementabile come forecast/certificato
   conservativo; non Ã¨ una garanzia deterministica ottenibile da una sola
   disuguaglianza scalare tra slot.
5. **`REACT at decision points / PLAN after commitment`.** Ãˆ utile, ma richiede
   una tassonomia formale dei decision point, invarianti del commitment e scope
   degli override.
6. **Exploration by replacement.** Riduce la distruzione di cicli funzionanti,
   ma il confronto intra-match Q0/Q1/Q2 non costituisce da solo un esperimento
   causale.
7. **Target 80k.** Ãˆ un obiettivo di progetto plausibile; non Ã¨ una proprietÃ
   della Foundation nÃ© una soglia inferita causalmente dai quattro replay.

## NOT_SUPPORTED:

- `CHICKEN` come specie engine-supported. L'engine locale canonico espone
  `GOOSE`, struttura `COOP`, prodotto `EGG`. `CHICKEN` puÃ² entrare soltanto se
  viene provato un alias/versione runtime diversa.
- I valori 24/48/72/96 come costanti Foundation in step. `turnsPerDay` Ã¨ un
  parametro di configurazione; le formule canoniche devono usare giorni e
  moltiplicare per il valore runtime.
- `FAILURE_BELOW: 50000` come conclusione tratta da LuCcc. Un singolo replay
  prova raggiungibilitÃ , non un floor della media su seed/opponent/seat diversi.
- La sequenza `Ontology -> Feature Model -> Environment State Machine`: il
  Feature Model corrente dipende giÃ  da fasi e transizioni della State Machine.
- L'inserimento lineare di `DEFINE -> PLAN -> BUILD -> VERIFY -> REVIEW` nella
  State Machine dell'ambiente. Sono stati/processi del controller, non stati
  nativi del dominio.
- La promozione automatica di tutti gli undici termini candidati a nuovi
  `concept_id`; diversi sono proprietÃ , feature o oggetti policy-local.
- Q0 come CONTROL e Q1/Q2 come trattamento imposto dalla Foundation. Ãˆ un
  protocollo sperimentale possibile, non semantica comune.
- L'obbligo Foundation di esplorare tutte le specie o sostituire i worst
  performers. Ãˆ una scelta di ricerca dei MODEL_SPEC/protocolli.

## ONTOLOGY_CHANGES:

### Concetti candidati da ammettere

L'Ontology dovrebbe aggiungere il minimo insieme semanticamente autonomo:

| Concetto | Tipo proposto | Motivazione |
|---|---|---|
| `biological_cycle` | `TIMING / INTERACTION` | Sequenza engine-grounded di fasi di un'entitÃ  biologica |
| `cycle_phase` | `STATE / TIMING` | Fase corrente derivabile da origin, metadata e clock |
| `service_need` | `STATE / CONSTRAINT` | Fabbisogno di servizio distinto dall'azione e dalla capacitÃ  |
| `service_window` | `TIMING / CONSTRAINT` | Intervallo in cui un servizio puÃ² completarsi senza violare il profilo dichiarato |
| `service_deadline` | `TIMING / CONSTRAINT` | Chiusura engine-hard o policy-declared della window |

`service_need` deve avere almeno due qualificatori non intercambiabili:

```text
ENGINE_HARD_NEED
  esempio: evitare la seconda EOD consecutiva senza WATER/FEED

POLICY_OUTPUT_NEED
  esempio: CARE giornaliera per bonus o harvest a max-yield
```

Senza questa separazione, una preferenza economica diventa erroneamente una
regola dell'ambiente.

### ProprietÃ /relazioni, non nuovi concept_id autonomi

- `BIOLOGICAL_PERIOD`, `SERVICE_PERIOD` e `PRODUCTION_PERIOD`: proprietÃ
  temporali di `biological_cycle`/`service_need`;
- `HARVEST_WINDOW`: specializzazione di `service_window`;
- `origin_step`, `nominal_period`, `next_due_step`, window open/target/close:
  proprietÃ  del profilo e feature runtime;
- `CAPACITY_REQUIREMENT`: derivazione del set di `service_need` in una window;
- `period_adherence`, `deadline_slack`, `forecast_error`: metriche derivate;
- `completion_evidence`: evento/provenance post-transizione.

### Termini da tenere fuori dall'Ontology di dominio

- `CAPACITY_RESERVATION`: contesto del planner/policy;
- `COMMITMENT`: stato del controller o relazione policy-asset;
- `DECISION_POINT`: evento del controller;
- `REACTIVE_OVERRIDE`: transizione del controller.

Se si desidera un'ontologia del controllo separata, questi quattro termini
possono essere registrati lÃ¬, con namespace distinto; non vanno presentati
come fatti nativi dell'ambiente.

## FEATURE_MODEL_CHANGES:

### Feature engine/derivate necessarie

```text
entity_origin_day / entity_origin_step
engine_cycle_phase
next_engine_event_day_or_step
service_need_type
service_window_open
service_window_close
engine_hard_deadline
time_to_window_close
```

### Policy context esplicito

```text
commitment_id
schedule_version
planned_target_step
reserved_capacity_by_window
route_cluster
declared_output_objective
safety_margin
```

Questi campi devono essere marcati `POLICY_CONTEXT`, non
`ENGINE_STATE`/`DERIVED_FEATURE` neutrale.

### Metriche derivate e telemetry

```text
required_capacity_by_window
available_capacity_by_window
deadline_slack
period_adherence_to_date
completion_evidence          # post-action / telemetry
capacity_forecast_error      # dopo il confronto forecast-realized
realized_service_completion  # post-window
```

`period_adherence_to_date` puÃ² essere online soltanto sul passato osservato;
non puÃ² incorporare future completion. `completion_evidence` e forecast error
non devono diventare input pre-azione dello stesso evento.

### Tre nozioni di serviceability

```text
action_eligible_now
  deterministic current-state predicate

reserved_serviceable_before_deadline
  policy forecast under declared route/resource assumptions

realized_serviceable_in_window
  post-hoc transition-backed outcome
```

La seconda resta `PARTIALLY_KNOWN`: un conteggio di slot Ã¨ necessario ma non
sufficiente. La capacity ha dimensioni almeno:

- worker-action e worker contract per day;
- spazio/route e posizione iniziale;
- ordine e concorrenza dei task;
- inventory/seed/feed/fertilizer;
- handling e shed capacity;
- market-order capacity quando la monetizzazione Ã¨ nel commitment;
- uncertainty/exception reserve.

Il risultato di una reservation deve includere un witness schedule fattibile o
un bound conservativo, non soltanto `required_slots <= available_slots`.

### Period ledger engine-grounded

La revisione deve materializzare una tabella versionata con fonte, formula,
clock, phase e hash engine. Per l'engine locale `0.1.0` sono direttamente
congelabili:

| EntitÃ  | Metadata engine congelabile | Interpretazione corretta |
|---|---|---|
| WHEAT | first yield 2 day, max-yield day 4, non-ongoing | WATER genera yield nella window age 2â€“4; harvest age Ã¨ scelta policy dopo la legalitÃ  |
| CARROT | first yield 2, max-yield day 3, non-ongoing | WATER yield window age 2â€“3 |
| MELON | first yield 10, max-yield day 12, non-ongoing | WATER yield window age 6â€“12; HARVEST legal da age 10 |
| TOMATO | first yield 8, interval 1, max 4 produzioni, ongoing | produzione EOD deterministica parametrizzata |
| STRAWBERRY | first yield 10, interval 2, max 4 produzioni, ongoing | produzione candidata age 10/12/14/16 |
| GOOSE | first yield 4, interval 1, max held 4 | COOP, prodotto EGG |
| COW | first yield 8, interval 2, max held 6 | PASTURE, prodotto MILK |
| SHEEP | first yield 6, interval 3, max held 6 | PASTURE, prodotto WOOL |

Sono inoltre congelabili, come formule parametrizzate:

- EOD ogni `turnsPerDay`, default 24;
- flags WATER/FEED/CARE reset a EOD;
- loss dopo `consecutive_unwatered >= 2`;
- fuga dopo `consecutive_unfed >= 2`;
- fertilizer crop attivo `day..day+2`;
- non-ongoing `max_lifespan_step = (planted_day + max_yield_day + 1) *
  turnsPerDay`.

Richiedono correzione/verifica prima del freeze:

1. **Animal production vs FEED.** Nel codice engine locale il production day
   aggiunge sempre `base = 1` se l'animale supera prima il check di fuga; FEED
   governa il bonus accumulato/consumato e il rischio di fuga. La State Machine
   corrente dice invece che senza FEED la produzione non avviene.
2. **Specie avicola.** Usare `GOOSE`, salvo prova di alias runtime `CHICKEN`.
3. **Boundary EOD e offset.** Pubblicare esempi per placement/plant day e
   `next_day`, non dedurre gli offset dai replay.
4. **Fidelity.** Legare la tabella a versione/hash dell'engine usato nel
   tournament e dichiarare eventuale gap col runtime Kaggle.
5. **Periodi replay.** 24/48/72/96 restano validazione empirica della
   configurazione, non sostituiscono i metadata engine.

## STATE_MACHINE_CHANGES:

### Separare due macchine ortogonali

#### A. Environment / Domain State Machine

Resta descrittiva e consumer-neutral. Contiene:

- clock e phase contract engine;
- lifecycle crop, animal, worker, inventory, market;
- production events e service needs;
- legalitÃ , EOD, deadline e loss transition;
- correzioni GOOSE e animal production/FEED.

Non contiene `DEFINE`, scelta crop, exploration, capacity reservation o target
economici.

#### B. Decision Lifecycle / Controller State Machine

Nuovo contratto separato, downstream del Feature Model:

```text
DECISION_OPEN
-> DEFINED
-> PLAN_FEASIBLE
-> COMMITTED_EXECUTING
-> REVIEW_READY
-> DECISION_OPEN
```

`VERIFY` non Ã¨ una fase soltanto successiva a BUILD: Ã¨ una regione ortogonale
attiva a ogni snapshot durante `COMMITTED_EXECUTING`.

```text
COMMITTED_EXECUTING
  || continuous VERIFY
  -> ON_TRACK
  -> DEVIATION_RECOVERABLE
  -> COMMITMENT_INFEASIBLE / HARD_OVERRIDE
```

`BUILD` Ã¨ ambiguo con il build software. Nel controller usare
`ALLOCATE_COMMIT` o `ASSET_COMMITTED`.

### Decision point e override

Decision point pianificati:

- completion del ciclo o della coorte;
- tile/structure che torna allocabile;
- review di espansione preregistrata;
- scadenza del commitment o terminal shutdown.

Decision point eccezionali:

- plan infeasible dopo una transizione;
- perdita di worker/capacitÃ  o input;
- missed service con hard deadline;
- cash/feed/storage incompatibile;
- illegalitÃ  o mismatch action-transition.

Un normale cambio prezzo non deve annullare un asset committed. PuÃ² modificare
sell timing, prossima coorte o capacitÃ  non ancora impegnata. Un override deve
dichiarare causa, scope mutato, reservation liberate/consumate e nuova
completion condition.

### Sequenza Foundation corretta

```text
ENGINE CONTRACT / PERIOD LEDGER AUDIT
-> ONTOLOGY
-> ENVIRONMENT STATE MACHINE
-> FEATURE MODEL
-> DECISION LIFECYCLE CONTRACT
-> VERTICAL CROSS-REVIEW
-> FOUNDATION FREEZE
-> THREE INDEPENDENT MODEL_SPEC REVISIONS
```

L'Environment State Machine precede il Feature Model perchÃ© authoritative
clock, phase e transition semantics sono input delle derivazioni. Il Decision
Lifecycle segue il Feature Model perchÃ© consuma feature e policy context.

## MODEL_SPEC_BOUNDARY:

La Foundation puÃ² imporre:

- vocabolario engine-grounded;
- period/phase/window/deadline schemas;
- classi di osservabilitÃ  e provenance;
- distinzione need/eligibility/forecast/realized completion;
- contratto minimo di commitment e override;
- metriche comparabili e no-future-leakage.

Devono restare nei MODEL_SPEC o nei protocolli sperimentali:

- crop/livestock mix e harvest mode;
- worker count e safety margin;
- algoritmo di routing/scheduling;
- strategia di mercato;
- quando e quanto espandere;
- se usare exploration by replacement;
- quale Q Ã¨ control/treatment;
- replacement criterion;
- score targets e acceptance gates.

La frase `BASE PRODUCTION = PLAN` puÃ² essere un'interfaccia consigliata della
Foundation. Non deve impedire a un MODEL_SPEC di usare una policy reattiva come
controllo o di dimostrare che un'altra architettura Ã¨ migliore.

## EXPLORATION_REVIEW:

`Exploration by replacement, not by disruption` Ã¨ metodologicamente sensato
come principio di contenimento del rischio, ma Q0 vs Q1/Q2 nella stessa partita
Ã¨ un confronto accoppiato, non un A/B causale.

Confondenti obbligatori:

| Confondente | Effetto |
|---|---|
| Shared market | ogni modulo modifica prezzi/inventory dell'altro |
| Quadrant topology | distanza, ordine di unlock e route non sono equivalenti |
| Start time / horizon | il replacement ha meno tempo per payback |
| Capital and wage allocation | cross-subsidy tra moduli |
| Shared workers/inventory/feed | attribuzione non identificabile senza ledger |
| Asset age and phase | output differisce anche con stessa specie |
| Worst-performer selection | regression to the mean e selection bias |
| Opponent actions | domanda e prezzi cambiano endogenamente |
| Spillover fertilizer/seed/Wheat | input fungibili contaminano i moduli |

Requisiti minimi:

1. module/cohort IDs preregistrati prima del commitment;
2. confronto tra cicli completi phase-aligned;
3. budget di capitale, worker-actions, route e input attribuiti;
4. regola di replacement preregistrata, non scelta post-hoc;
5. rotazione/counterbalancing del quadrante su episodi indipendenti;
6. clone-control che separi novitÃ  da semplice espansione;
7. ledger per prodotti fungibili e criteri espliciti di cost allocation;
8. holdout seed/opponent/seat non usato per selezionare l'alternativa;
9. analisi intra-match dichiarata descrittiva, corroborata da confronti
   inter-episode controllati.

La copertura di GOOSE/COW/SHEEP e di tutte le crop Ã¨ un obiettivo di knowledge
coverage, non un requisito che ogni policy debba soddisfare in partita.

## TARGET_REVIEW:

```text
TARGET_MEAN_FINAL_MONEY: >= 80000
```

PuÃ² restare come target competitivo di progetto se:

- Ã¨ congelato prima dei seed di valutazione;
- non entra come feature, reward shaping o parametro della policy;
- il protocollo dichiara numero episodi, seat, opponent e seed holdout;
- si riportano dispersione e intervallo di confidenza, non soltanto la media;
- il confronto usa la stessa distribuzione di condizioni per baseline e
  candidato;
- fallimenti tecnici e score economici restano separati.

```text
FAILURE_BELOW: 50000
```

Non Ã¨ ancora supportato come floor empirico della media. Va riclassificato come
aspirational project gate oppure `REQUIRES_EVIDENCE` fino al common tournament.
La traiettoria LuCcc prova esistenza, non una lower bound generale. Nessuno dei
due numeri appartiene a Ontology, Feature Model o State Machine.

## MAIN_RISK:

Il rischio principale Ã¨ una **category error trasformata in falsa garanzia di
capacitÃ **:

```text
engine period
-> scalar slot count
-> policy reservation
-> labeled SERVICEABLE as if deterministic
```

Routing, contratti giornalieri, inventory, feed, EOD e task ordering possono
rendere impossibile un piano anche quando la somma degli slot Ã¨ sufficiente. Se
il lifecycle del controller viene inoltre incorporato nella State Machine
dell'ambiente, proprietÃ  della policy possono essere etichettate
`ENGINE_VERIFIED` e poi consumate senza provenance corretta.

## MANDATORY_CHANGE_BEFORE_PROCEEDING:

Pubblicare e cross-verificare un **Periodic Foundation Contract a due piani**:

1. `ENGINE_PERIOD_LEDGER`, versionato e hash-linked, per tutte le cinque crop e
   `GOOSE/COW/SHEEP`, con clock, phase, formule, boundary examples e correzione
   della semantica animal-production/FEED;
2. separazione formale tra `ENVIRONMENT_STATE_MACHINE` e
   `DECISION_LIFECYCLE`, con il Feature Model collocato tra i due;
3. definizione tripartita `eligible / reserved-serviceable /
   realized-serviceable` e provenance di ciascuna.

Senza questo contratto, non autorizzare Ontology Revision nÃ© la successiva
catena di freeze.

## Disposizione proposta delle osservazioni

| Osservazione | Classificazione Codex | Condizione |
|---|---|---|
| Estendere la Foundation a cicli e finestre | `ACCEPT` | dopo engine ledger |
| Serviceability temporale | `ACCEPT` | tripartita e non garantita da raw slots |
| Period -> future demand -> feasibility | `ACCEPT` | reservation resta policy context |
| PLAN tra decision point | `ACCEPT` | nel Decision Lifecycle separato |
| Undici nuovi concept_id | `REJECT` | ammettere solo primitivi non ridondanti |
| Sequenza Ontology -> Feature -> State Machine | `REJECT` | usare la sequenza a due piani |
| Expansion as phase-shifted clone | `DEFER` | pattern MODEL_SPEC/esperimento, non legge Foundation |
| Exploration Q0 vs Q1/Q2 | `REQUIRES_EVIDENCE` | controlli e corroborazione inter-episode |
| Copertura progressiva di tutte le specie | `DEFER` | research backlog; usare GOOSE, non CHICKEN |
| 80k target | `DEFER` | project gate con holdout e CI |
| <50k failure | `REQUIRES_EVIDENCE` | un replay Q0 non stabilisce il floor |
| Avvio BUILD | `REJECT` | Foundation non congelata |

## FINAL_RECOMMENDATION:

```text
FOUNDATION_REVISION_PLAN_STATUS: PROPOSED_WITH_MANDATORY_CHANGES
ONTOLOGY_REVISION_AUTHORIZED: NO
FEATURE_MODEL_REVISION_AUTHORIZED: NO
STATE_MACHINE_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
NEXT_ACTION: CLASSIFY_THREE_FEEDBACKS_AND_RESOLVE_ENGINE_CONTRACT_BLOCKERS
```

Accettare la direzione period-centric, ma non procedere direttamente con la
sequenza proposta. Prima classificare i tre feedback indipendenti, risolvere i
fatti engine e congelare il confine tra dominio, feature e controller. Solo
dopo puÃ² iniziare una revisione Foundation consumer-neutral.
