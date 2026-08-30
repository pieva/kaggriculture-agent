# Kaggriculture - Foundation Reconciliation R1 - Codex

```text
DOCUMENTO: CODEX_FOUNDATION_RECONCILIATION_R1.md
RUOLO: reconciliation tecnica delle review indipendenti Antigravity e Copilot
STATO FOUNDATION: CANDIDATE C1 / NOT FROZEN
DATA: 2026-08-30
```

## 1. Executive verdict

La divergenza fra le review e una **combinazione di differenza nel criterio di
freeze e conflitti tecnici circoscritti**.

Antigravity ha verificato con successo la correttezza sostanziale delle
meccaniche engine e della separazione epistemica introdotta da State Machine C1
e Feature Model C1. Copilot ha applicato un criterio ulteriore: due
implementazioni conformi devono poter calcolare gli stessi stati e deve essere
dimostrabile quale feature sia realmente consumata dal MODEL_SPEC e dal runtime.
Questo secondo criterio e necessario per il freeze.

Non emerge un conflitto sostanziale sulle regole engine principali. Emergono
invece due conflitti reali sull'adeguatezza eseguibile di C1:

1. la presenza di una lista di precedence per `tile_lifecycle_state` non equivale
   ancora a un classifier totale con predicati mutuamente esclusivi e boundary
   tests;
2. `canonical_step` e valido come ricostruzione diagnostica, ma non puo essere
   usato implicitamente come clock delle transizioni engine quando C1 stesso
   dichiara `step` semanticamente autorevole.

I tre P0 Copilot sono supportati e bloccano il freeze. Le correzioni richieste
non implicano il rigetto dell'architettura foundation: il nucleo concettuale e
valido, ma serve una revisione C2 cross-artefatto.

```text
FINDING_RECONCILIATI: 19
CONVERGENT: 3
COMPLEMENTARY: 5
CONFLICT: 2
PARTIAL_OVERLAP: 2
UNIQUE_SUPPORTED: 7
UNIQUE_UNSUPPORTED: 0

ONTOLOGY: REVISE_MAJOR
STATE_MACHINE_C1: REVISE_LIGHT
FEATURE_MODEL_C1: REVISE_MAJOR
MODEL_SPEC: REVISE_MAJOR
FREEZE_VERDICT: FOUNDATION_C2_REQUIRED
```

## 2. Divergenza reale e criterio di freeze

### 2.1 Area di convergenza sostanziale

Le review convergono sulla correttezza di:

- maturity gate di HARVEST basato anche su `first_yield_day`;
- separazione fra stato lifecycle e `care_due` ortogonale;
- struttura multi-causa di `crop_decay_risk_window`;
- distinzione `ENGINE_OBSERVABLE` / `TELEMETRY_OBSERVED`;
- rigetto di un `time_to_random_weed` deterministico;
- separazione fra surface attiva e maintained, cash corrente e buffer, quote
  corrente e valore realizzato, DIG preventivo e DIG recovery;
- permanenza esplicita di feature incomplete come `PARTIALLY_KNOWN` o
  `CONDITIONAL`.

### 2.2 Differenza di criterio

Il verdetto `ACCEPT` di Antigravity su State Machine e Feature Model significa
principalmente "meccaniche e categorie sostanzialmente corrette". Il
`DO_NOT_FREEZE` di Copilot significa "contratti non ancora sufficienti a
garantire classificazione, calcolo e consumo riproducibili". Questi giudizi non
sono mutuamente esclusivi: un candidato puo essere semanticamente corretto ma
non ancora congelabile.

### 2.3 Conflitti reali circoscritti

- **Classifier lifecycle:** Antigravity considera completa la copertura degli
  stati; Copilot contesta la sufficienza operativa. La precedence dichiarata
  nello schema e utile, ma le definizioni di `RETIREMENT_DUE` e il fallback non
  costituiscono ancora una funzione eseguibile totale. Copilot prevale sul
  requisito di freeze; Antigravity resta corretto sulla meccanica sottostante.
- **Clock:** Antigravity accetta `canonical_step` come clock diagnostico
  seat-invariant; Copilot rileva correttamente che `CRP-13..15` lo usano per
  deadline descritte come engine transitions. Il live engine clock e il clock
  di replay devono essere distinti per ogni formula.

Non vi e alcun majority vote: le decisioni sotto derivano dai documenti C1,
dall'Ontologia, dai MODEL_SPEC e dalle sole verifiche runtime/engine mirate
necessarie a dirimere i finding gia formulati.

## 3. Reconciliation matrix completa

| reconciliation_id | tema | finding_antigravity | finding_copilot | artefatti_interessati | relationship | evidence_status | technical_resolution | freeze_impact | recommended_artifact_change |
|---|---|---|---|---|---|---|---|---|---|
| `REC-01` | Maturity HARVEST | `FND-01`: `first_yield_day` omesso da Ontologia/MODEL_SPEC | P0-02 e P1-01 richiedono input e predicato realmente computati | ONTOLOGY, FEATURE_MODEL, MODEL_SPEC, consumer matrix | `CONVERGENT` | `ENGINE_VERIFIED` + `EMPIRICALLY_VERIFIED` | `harvest_ready` richiede PLANT, `yield_units>0` e `day-planted_day>=first_yield_day`; la presenza nel catalogo non prova il consumo runtime. | `BLOCKER` | Aggiungere concetto readiness; mantenere il predicato C1; dichiarare consumer e funzione runtime o `NOT_USED`. |
| `REC-02` | `tile_lifecycle_state` | `FND-02`: stati strutturali corretti e da integrare | `P1-01`: manca classifier eseguibile | ONTOLOGY, STATE_MACHINE, FEATURE_MODEL, validation contract, MODEL_SPEC | `PARTIAL_OVERLAP` | `DERIVED_ENGINE_GROUNDED` | I sei valori sono supportati; la lista di precedence non basta per il freeze. L'adozione nel MODEL_SPEC non e automatica. | `REQUIRED_BEFORE_FREEZE` | Aggiungere decision table/pseudocode totale e test vettoriali; mappare il concetto; per ciascun MODEL_SPEC dichiarare uso versionato. |
| `REC-03` | `crop_decay_risk_window` | `FND-03`: vincolo strutturato assente dal MODEL_SPEC | `P1-02`: deadline lifespan usa clock ambiguo | FEATURE_MODEL, MODEL_SPEC, clock contract | `PARTIAL_OVERLAP` | `ENGINE_VERIFIED` + `DERIVED` | Conservare la struttura multi-causa; separare missed-WATER, lifespan deterministico e sola eligibility RNG; associare a ogni deadline il clock autorevole. | `REQUIRED_BEFORE_FREEZE` | Correggere `CRP-13..15`; nel MODEL_SPEC dichiarare componenti realmente usate senza scalarizzazione. |
| `REC-04` | Inventory EOD | `FND-04`: `contract_inventory_loss` e in realta overflow dello shed al drop automatico | Nessun finding specifico | ONTOLOGY, MODEL_SPEC, consumer mappings | `UNIQUE_SUPPORTED` | `ENGINE_VERIFIED` | `_drop_inventories_to_shed` trasferisce automaticamente fino a capacity e scarta l'eccedenza; non serve un rientro manuale per evitare una perdita da scadenza contrattuale. | `BLOCKER` | Correggere o rinominare il concetto, la relazione e ogni MODEL_SPEC che descrive il reset/return manuale. |
| `REC-05` | Mapping ontologico | `FND-05`: gap per clock, readiness, lifecycle e opponent state | P0-01/P0-03 mostrano che mapping e consumo/formula sono contratti distinti | ONTOLOGY, FEATURE_MODEL, consumer matrix | `COMPLEMENTARY` | `DOCUMENT_VERIFIED` + `DERIVED` | Il Principio OR supporta readiness e lifecycle. Non ogni `NONE_DIRECT` richiede un concept_id: `step` e `canonical_step` possono restare primitive/derivazioni tecniche. | `REQUIRED_BEFORE_FREEZE` | Aggiungere solo concetti semanticamente riusabili; documentare `NONE_DIRECT` legittimi; non forzare una biiezione Ontologia-Feature Model. |
| `REC-06` | Worker multi-occupancy | `FND-06`: co-locazione consentita; reservation e policy | `P1-03` mantiene serviceability separata, senza verifica specifica dell'occupancy | STATE_MACHINE, FEATURE_MODEL | `UNIQUE_SUPPORTED` | `ENGINE_VERIFIED` | Il movimento non verifica collisioni e lo spawn minimizza occupancy senza imporre un limite. Questo rimuove un unknown, ma non prova reachability o serviceability. | `NON_BLOCKING` | Promuovere la sola regola di multi-occupancy a `ENGINE_VERIFIED`; lasciare routing/reservation nella POLICY. |
| `REC-07` | FERTILIZE | `FND-07`: effetto deterministico inclusivo fino a `day+2` | Nessun finding specifico | STATE_MACHINE, FEATURE_MODEL | `UNIQUE_SUPPORTED` | `ENGINE_VERIFIED` | Durata a tre giorni e bonus crop sono sufficientemente fondati; monetizzazione e policy restano separati. | `NON_BLOCKING` | In C2 documentare transizioni e `fertilized_days_remaining`; non promuovere automaticamente a feature usata dal MODEL_SPEC. |
| `REC-08` | FEED+CARE bonus | `FND-08`: accumulo congiunto e consumo su production day alimentato | Nessun finding specifico | STATE_MACHINE, FEATURE_MODEL | `UNIQUE_SUPPORTED` | `ENGINE_VERIFIED` | `pending_care_bonus` aumenta solo con FEED e CARE nello stesso giorno e viene consumato su un giorno di produzione se `fed_today`. | `NON_BLOCKING` | In C2 precisare accumulo, reset e consumo; mantenere margini economici `PARTIALLY_KNOWN`. |
| `REC-09` | Osservabilita vs log | `FND-09`: online observability diversa da persistenza R1 | Copilot preserva esplicitamente la stessa separazione | FEATURE_MODEL, TELEMETRY | `CONVERGENT` | `EMPIRICALLY_VERIFIED` | Nessuna correzione semantica: un gap di replay non riduce l'osservabilita engine online. | `NON_BLOCKING` | `NO_CHANGE`; la futura telemetry puo aumentare la validabilita senza cambiare la feature class. |
| `REC-10` | Random WEED | `FND-10`: rigetto del countdown deterministico | Copilot preserva il rigetto e ammette solo eligibility | FEATURE_MODEL | `CONVERGENT` | `ENGINE_VERIFIED` + `DERIVED` | Il draw futuro e hidden; e lecita solo l'esposizione corrente `empty_random_weed_eligible`. | `NON_BLOCKING` | `NO_CHANGE`. |
| `REC-11` | Consumer autorevole | Nessun finding specifico; Antigravity valuta il Codex frozen indicato dal C1 | `P0-01`: `current_MODEL_SPEC_usage` e Codex-specifico ma sembra comune | FEATURE_MODEL, MODEL_SPEC consumer contract | `UNIQUE_SUPPORTED` | `DOCUMENT_VERIFIED` | Il Feature Model comune non deve possedere una colonna "current" consumer-specifica. La sola rinomina riduce l'ambiguita ma conserva coupling e proliferazione di colonne. | `BLOCKER` | Spostare i valori storici in una matrice consumer esterna, versionata, con path/hash/revision del MODEL_SPEC; rimuovere la colonna dal catalogo comune. |
| `REC-12` | Uso dichiarato vs runtime | Antigravity richiede revisione MODEL_SPEC per gap semantici | `P0-02`: numerosi `USED/FULL` non sono input o derivazioni dimostrate del runtime Copilot | MODEL_SPEC, runtime, consumer matrix | `COMPLEMENTARY` | `DOCUMENT_AND_RUNTIME_VERIFIED` | `MODEL_SPEC says USED != runtime demonstrably consumes`. Ogni mapping deve avere ruolo, formula, fase e consumer; telemetry/outcome non sono input pre-action. | `BLOCKER` | Introdurre `POLICY_INPUT`, `RUNTIME_DERIVED`, `POST_ACTION_TELEMETRY`, `OUTCOME_ONLY` nella consumer matrix e correggere i mapping Copilot. |
| `REC-13` | Surface/capacity senza formula | Antigravity rileva gap di Ontologia/MODEL_SPEC ma accetta il catalogo C1 | `P0-03`: aggregati `USED/FULL` e gate senza schema computabile | ONTOLOGY, FEATURE_MODEL, MODEL_SPEC, aggregate contracts | `COMPLEMENTARY` | `DOCUMENT_VERIFIED` | Feature incomplete possono restare nel catalogo come `CONDITIONAL`/`PARTIALLY_KNOWN`; non possono essere `FULL` o gate operativo senza formula versionata. | `BLOCKER` | Pubblicare aggregate contract per ogni gate o downgradare a `PARTIAL`/`NOT_USED`; non congelare `state_capacity_alignment`. |
| `REC-14` | Precedence lifecycle | Antigravity dichiara completa e non ridondante la classificazione | `P1-01`: precedence non eseguibile e confini sovrapposti | STATE_MACHINE, FEATURE_MODEL, validation contract | `CONFLICT` | `DOCUMENT_VERIFIED` | Antigravity ha ragione sui valori; Copilot ha ragione sulla congelabilita. `OUT_OF_SCOPE` prima di kind e il confine finale ongoing devono essere tradotti in predicati totali. | `REQUIRED_BEFORE_FREEZE` | Feature/validation contract: funzione ordinata, fallback e test inside/outside working set; State Machine: esempi di confine, senza trasformarla in policy. |
| `REC-15` | Clock autorevole | Antigravity accetta `canonical_step` come clock diagnostico invariant | `P1-02`: lifespan mescola engine `step` e ricostruzione day/hour | STATE_MACHINE, FEATURE_MODEL, TELEMETRY | `CONFLICT` | `DOCUMENT_VERIFIED` | `step` resta autorevole per le regole engine che lo consumano; `canonical_step` e ricostruzione diagnostica. Ogni deadline deve nominare fonte e fase; l'eventuale equivalenza va verificata, non assunta. | `REQUIRED_BEFORE_FREEZE` | Chiarimento leggero in State Machine; correggere formule/classi di `CRP-13..15`; conservare entrambi i clock nei log. |
| `REC-16` | Need, eligibility, serviceability | `FND-06` risolve soltanto la collisione | `P1-03`: tile predicate non prova attore, inventory, path o phase disponibili | STATE_MACHINE, FEATURE_MODEL, POLICY/consumer contract | `COMPLEMENTARY` | `METHODOLOGICALLY_VERIFIED` | `tile_need` appartiene al Feature Model; `action_eligible_now` combina precondizioni engine e actor; `serviceable_before_deadline` richiede stato workforce e policy memory. | `REQUIRED_BEFORE_FREEZE` | Aggiungere i tre livelli e mantenerli distinti; lasciare gli ultimi due `PARTIALLY_KNOWN` finche privi di contratto. |
| `REC-17` | Aggregate contract | Antigravity conferma aggregate utili e alcuni mapping gap | `P1-04`: denominatori, ownership e finestre non canonici | ONTOLOGY, FEATURE_MODEL, MODEL_SPEC, TELEMETRY | `COMPLEMENTARY` | `DOCUMENT_VERIFIED` | Il contratto completo e necessario per ogni aggregate usato da MODEL_SPEC o policy gate; e un perfezionamento rinviabile per un concetto solo diagnostico e dichiarato incompleto. | `REQUIRED_BEFORE_FREEZE` | Definire scope, sampling phase, window, numerator, denominator, zero convention, dedup key, source class, formula version e boundary examples. |
| `REC-18` | Provenance market/inventory | Nessun finding specifico oltre alla correzione inventory EOD | `P1-05`: quote, request, execution, realized ed estimate sono confusi | FEATURE_MODEL, MODEL_SPEC, TELEMETRY | `UNIQUE_SUPPORTED` | `DOCUMENT_VERIFIED` | Base price o quote e valore realizzato non sono intercambiabili; un cash delta aggregato non attribuisce un ordine in modo univoco. | `REQUIRED_BEFORE_FREEZE` | Contratto per `displayed_quote_pre_request`, requested/executed quantity, realized price/cash delta e provenance; downgrade degli estimate. |
| `REC-19` | MODEL_SPEC vs Copilot runtime | Nessun audit specifico del runtime Copilot; solo verdict MODEL_SPEC REVISE | `P1-06`: soglie fisse e delega X112 non descritte | MODEL_SPEC, runtime, consumer matrix | `UNIQUE_SUPPORTED` | `RUNTIME_VERIFIED` | Il wrapper inoltra solo parte di `CopilotConfig`; la routine sceglie target discreti `(1,0)..(7,4)` e delega a X112. Il MODEL_SPEC puo essere concettuale oppure eseguibile, non entrambe le cose senza trace. | `REQUIRED_BEFORE_FREEZE` | Versionare il decision graph e la delega X112, oppure ridurre esplicitamente il MODEL_SPEC a modello concettuale e non dichiarare consumo runtime. |

## 4. Decisione sui tre P0 Copilot

### P0-01 - Confermato come blocker

`current_MODEL_SPEC_usage` identifica nel testo il frozen Codex E15, ma il nome
della colonna appare generale. La soluzione metodologicamente preferibile non e
aggiungere una colonna per ogni modeler nel Feature Model comune.

Decisione:

```text
Feature Model comune:
  feature identity, information class, observability, availability,
  formula/status e validity limits

Versioned MODEL_SPEC consumer matrix esterna:
  consumer_id, MODEL_SPEC path/hash/revision, feature_id/concept_id,
  declared usage, runtime role, formula/phase, consuming function,
  implementation evidence e conformance status
```

I valori attuali devono essere preservati storicamente come consumer
`codex_e15_frozen`, non semplicemente rinominati dentro il catalogo comune.

### P0-02 - Confermato come blocker

La tassonomia richiesta e adottata:

```text
POLICY_INPUT
RUNTIME_DERIVED
POST_ACTION_TELEMETRY
OUTCOME_ONLY
```

Essa appartiene primariamente alla **consumer matrix versionata**, perche
descrive la relazione fra una versione del MODEL_SPEC e una versione del
runtime. Il Feature Model continua a definire la classe informativa generale;
il MODEL_SPEC dichiara il ruolo strategico; la consumer matrix dimostra il
consumer concreto, la fase e la funzione. `POST_ACTION_TELEMETRY` e
`OUTCOME_ONLY` non possono essere input della stessa decisione che li genera.

### P0-03 - Confermato come blocker

Una feature `CONDITIONAL` o `PARTIALLY_KNOWN` puo restare nel Feature Model.
Questa e una qualifica epistemica lecita, non un difetto da eliminare. La regola
di freeze e invece:

```text
MODEL_SPEC USED/FULL o policy gate
  => formula/aggregate contract completo e versionato
     oppure downgrade a PARTIAL/NOT_USED
```

Il contratto e necessario per ogni aggregate che influenza una decisione. Per
aggregati soltanto diagnostici, la formalizzazione completa puo essere
rinviata, pur mantenendo evidente lo stato incompleto e vietandone confronti
come se fossero metriche canoniche.

## 5. Decisione sui finding Antigravity unici

| Finding | Decisione | Impatto C2 |
|---|---|---|
| `FND-04` inventory loss | Supportato e bloccante. La definizione ontologica e il mapping `USED/FULL` Copilot contengono una regola engine falsa. | Correzione MUST in Ontologia e consumer MODEL_SPEC. |
| `FND-06` multi-occupancy | Supportato. L'engine non impone collisioni o occupancy massima. | Promozione mirata a `ENGINE_VERIFIED`; non risolve routing/serviceability. |
| `FND-07` FERTILIZE | Supportato per durata inclusiva `day..day+2` e bonus osservati nel codice. | Documentazione C2 SHOULD; economia e policy restano fuori. |
| `FND-08` FEED+CARE | Supportato per accumulo e consumo del `pending_care_bonus`. | Documentazione C2 SHOULD; nessuna inferenza di margine/optimum. |

Queste conclusioni sono sufficienti per modificare C2 senza nuovi episodi. Le
ultime tre non sono blocker perche C1 aveva dichiarato quei sottosistemi
`PARTIALLY_KNOWN`; diventano correzioni di perimetro, non falsificazioni del
nucleo crop/tile.

## 6. Classificazione finale dei quattro artefatti

### ONTOLOGY: `REVISE_MAJOR`

Motivi: `contract_inventory_loss` contiene un errore fattuale con implicazione
strategica; maturity/lifecycle richiedono un mapping canonico; i contratti di
aggregate gia richiesti dall'Ontologia non sono rispettati dai MODEL_SPEC.
`REVISE_MAJOR` non significa rigetto del vocabolario esistente.

### STATE_MACHINE_C1: `REVISE_LIGHT`

Le meccaniche principali restano sostanzialmente corrette e engine-grounded.
Le revisioni necessarie sono: authoritative clock per transizione, boundary
examples del lifecycle e promozione mirata delle nuove evidenze engine. Il
classifier eseguibile appartiene primariamente al Feature/validation contract;
actor eligibility e serviceability appartengono anche a Feature Model e policy
contract, non sono nuovi stati engine.

### FEATURE_MODEL_C1: `REVISE_MAJOR`

La tassonomia informativa e valida, ma la revisione e strutturale: esternalizzare
il consumer-specific usage, correggere il contratto clock/lifespan, rendere
eseguibile il lifecycle classifier e distinguere need/eligibility/serviceability.
Le feature incomplete possono e devono restare nel catalogo con la qualifica
corretta.

### MODEL_SPEC: `REVISE_MAJOR`

I gap maturity/lifecycle/risk sono confermati. Inoltre il Copilot MODEL_SPEC
confonde concetti, diagnostiche, telemetry e consumo runtime, usa `FULL` senza
formule canoniche e non descrive fedelmente soglie/delega del runtime attivo.
Serve un contratto versionato, non una nuova scelta di soglie.

## 7. Freeze verdict

```text
FREEZE_VERDICT: FOUNDATION_C2_REQUIRED
FOUNDATION_REDESIGN_REQUIRED: NO
```

Una semplice approvazione condizionata di C1 non e sufficiente: i blocker
attraversano Ontologia, Feature Model, MODEL_SPEC e consumer/runtime trace e
richiedono una nuova revisione coerente degli artefatti. Non serve pero un
redesign: la separazione ENGINE -> ONTOLOGY -> STATE MACHINE -> FEATURE MODEL ->
MODEL_SPEC -> POLICY resta valida.

## 8. Modifiche per il prossimo Foundation Tournament

### MUST

1. Correggere `contract_inventory_loss` come overflow al drop automatico EOD e
   rettificare tutti i MODEL_SPEC/mapping che prescrivono il rientro manuale.
2. Aggiungere maturity/readiness all'Ontologia e imporre il predicato completo
   dove un consumer dichiara HARVEST readiness.
3. Esternalizzare `current_MODEL_SPEC_usage` in consumer matrix versionate con
   path, revision e hash del MODEL_SPEC e del runtime.
4. Applicare la tassonomia `POLICY_INPUT | RUNTIME_DERIVED |
   POST_ACTION_TELEMETRY | OUTCOME_ONLY` a ogni mapping dichiarato `USED`.
5. Correggere o downgradare ogni `USED/FULL` non dimostrato dal runtime.
6. Pubblicare un classifier totale per `tile_lifecycle_state`, con predicati,
   precedence, fallback e boundary tests.
7. Pubblicare l'authoritative clock/phase contract per transizioni e deadline;
   correggere `CRP-13..15` e preservare separatamente il clock diagnostico.
8. Definire aggregate contract completi per ogni aggregate usato da un gate;
   mantenere `state_capacity_alignment` non congelato finche privo di formula.
9. Allineare il Copilot MODEL_SPEC alla routine attiva e alla delega X112,
   oppure dichiararlo esplicitamente non eseguibile e concettuale.
10. Separare quote, request, executed quantity, realized price/cash delta ed
    estimate con provenance e fase.

### SHOULD

1. Aggiungere i concetti lifecycle solo dove soddisfano il Principio OR e
   documentare i `NONE_DIRECT` legittimi senza forzare una biiezione.
2. Distinguere formalmente `tile_need`, `action_eligible_now` e
   `serviceable_before_deadline`.
3. Promuovere worker multi-occupancy a `ENGINE_VERIFIED` mantenendo reservation
   e routing nella policy.
4. Documentare durata/bonus FERTILIZE e la feature
   `fertilized_days_remaining` senza adozione automatica nel MODEL_SPEC.
5. Documentare il lifecycle congiunto FEED+CARE e il consumo del bonus.
6. Versionare un event schema capace di validare request, execution, no-op,
   transition reason e aggregate constituents.

### DEFER

1. Formula e tuning di aggregati solo diagnostici non usati da gate.
2. Margini economici livestock, fertilizer e care bonus.
3. Elasticita market completa e strategie di prezzo.
4. Modelli opponent e fairness multi-player non necessari ai blocker.
5. Qualunque soglia, peso, ranking o optimum di policy.

## 9. Punti che non richiedono ulteriori analisi o esperimenti

Non servono nuovi episodi, benchmark o trattamenti per stabilire:

- formula del maturity gate e causa dei premature HARVEST R1;
- tre cause WEED e rigetto del countdown RNG deterministico;
- distinzione online observability / replay persistence;
- trasferimento automatico EOD e perdita per shed overflow;
- worker multi-occupancy;
- durata inclusiva FERTILIZE e bonus crop verificati;
- accumulo congiunto FEED+CARE e consumo del bonus;
- natura policy-owned di working set, reservation, routing e cash floor;
- consumer ambiguity della colonna C1;
- mancato inoltro di parte di `CopilotConfig`, target discreti e delega X112;
- necessita metodologica dei consumer e aggregate contracts.

Le correzioni possono essere validate con review documentale, unit/boundary
tests e runtime trace statico. Non richiedono evidenza prestazionale nuova.

## 10. Unresolved evidence gaps

```text
UNRESOLVED_EVIDENCE_GAP: NONE
```

Restano decisioni di governance e contratti ancora da scrivere, non dispute
fattuali che richiedano nuova evidenza sperimentale. In particolare, la scelta
se un MODEL_SPEC consumera in futuro FERTILIZE, care bonus o aggregati parziali
e una scelta di modello/policy e non un evidence gap dell'engine.

## 11. Vincoli rispettati

- Nessuna modifica a Ontologia, State Machine, Feature Model o MODEL_SPEC.
- Nessuna modifica a policy, runtime, codice o configurazioni.
- Nessun episodio, benchmark o Foundation Tournament eseguito.
- Nessuna nuova analisi sistematica dell'engine: sono state effettuate solo
  verifiche mirate dei finding gia formulati nelle due review.
