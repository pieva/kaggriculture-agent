# Codex - Independent Review of Feature Model C2 - R1

```text
REVIEW TARGET: docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
REVIEW DATE: 2026-08-30
REVIEW SCOPE: informational contract C2, no MODEL_SPEC/runtime/policy changes
```

## 1. Executive verdict

```text
FEATURE MODEL C2 VERDICT: REVISE_MAJOR
MODEL_SPEC_C2_UPSTREAM_READY: NO
```

Il candidato recepisce correttamente diversi principi della Foundation
Reconciliation R1: neutralita rispetto ai consumer, consumer matrix esterna,
separazione dei clock, readiness completa, rischio crop multi-causa, rigetto del
countdown random-WEED, separazione need/eligibility/serviceability e provenance
market/inventory.

Non e tuttavia un Feature Model utilizzabile come upstream. Il documento
dichiara 74 feature e una distribuzione per classe, ma non pubblica alcuna riga
di catalogo con `feature_id`. C1 contiene 59 ID verificabili; C2 ne espone zero
nel proprio catalogo e soltanto sette righe di migrazione basate su nomi, non
sugli ID C1. Di conseguenza non sono verificabili identita, classi, formule,
fonti, availability, evidence status o l'incremento 59 -> 74.

Inoltre il classifier lifecycle centrale contraddice i propri boundary test e
le regole engine: classifica ogni `None` come `OUT_OF_SCOPE`, usa una variabile
`engine_step` non presente nella signature e tratta il solo raggiungimento di
`max_lifespan_step` come `RETIREMENT_DUE`, mascherando stati raccoglibili e
includendo crop non-ongoing. I contratti aggregate sono elencati come template,
ma non sono istanziati per feature e non separano operativamente
`CONTRACT_SCHEMA_COMPLETE` da `FEATURE_FORMULA_COMPLETE`.

### Conteggio findings

| Severita | Conteggio |
|---|---:|
| `P0 BLOCKER` | 2 |
| `P1 MAJOR` | 4 |
| `P2 MINOR` | 2 |
| `NOTE` | 2 |

## 2. Findings

| ID | severity | artifact/feature | claim | evidence | impact | required correction |
|---|---|---|---|---|---|---|
| `P0-01` | `P0 BLOCKER` | Catalogo C2, conteggi, migrazione | Il catalogo di 74 feature non esiste come insieme di record verificabili. | C2 §2.2 dichiara 74 elementi; nel file non esiste alcuna riga con gli ID canonici C1 (`TMP-01`, `CRP-09`, ecc.); C2 §17 contiene solo 7 nomi semantici. C1 espone 59 ID. Il registry Ontology C2 dichiara 74 concept_id ma contiene 75 heading nel registry, quindi il numero non puo essere importato come conteggio feature. | Non e possibile auditare 59 -> 74, classi, over-expansion, formula, provenance o migrazione. Due consumer potrebbero ricostruire cataloghi diversi. | Pubblicare il catalogo completo riga-per-riga, preservare gli ID C1, assegnare nuovi ID alle sole aggiunte legittime, ricontare le classi e produrre una migrazione esaustiva. |
| `P0-02` | `P0 BLOCKER` | `tile_lifecycle_state` classifier | Il classifier non e totale, implementabile o coerente con engine/State Machine C2. | C2 §5.1 restituisce `OUT_OF_SCOPE` per `tile is None`, rendendo irraggiungibile `EMPTY_ASSIGNED`; accede a `tile.kind` per il valore nativo stringa `"LOCKED"`; usa `engine_step` senza parametro; assegna `RETIREMENT_DUE` per il solo crossing di `max_lifespan_step`. C2 §5.3 contraddice questi rami. | Classificazioni errate su input validi e perdita della distinzione finale ongoing/harvest-ready. Un MODEL_SPEC non puo consumare lo stato in modo deterministico. | Sostituire il classifier con predicati mutuamente esclusivi e una signature completa; usare `RETIREMENT_DUE` solo per ongoing esaurita dopo final HARVEST, con `yield_units == 0`, lifespan impostata e nessuna produzione schedulata residua; aggiungere test eseguibili. |
| `P1-01` | `P1 MAJOR` | Aggregate contracts | C2 definisce lo schema minimo ma non compila alcun contratto per-feature e non materializza i due assi di completezza. | C2 §9 elenca i campi e §9.1 offre soltanto `Status`, `Scope`, `Notes`; mancano sampling phase, window, numerator, denominator, zero convention, dedup, source class, formula version e boundary examples per ogni riga. | Nessuno degli aggregate auditati e freeze-ready; il downstream non puo distinguere formula assente da contratto formalmente compilato. | Aggiungere una tabella per-feature con `CONTRACT_SCHEMA_COMPLETE` e `FEATURE_FORMULA_COMPLETE` separati. Formula incompleta implica `freeze_ready=NO`. |
| `P1-02` | `P1 MAJOR` | Clock e feature temporali | La separazione clock e corretta in prosa, ma il contratto temporale richiesto non e applicato alle feature. | C2 §4 elenca requisiti; non esistono record/formule C2 per `CRP-13..15`, `action_phases_until_eod_refresh`, fertilizer timing o livestock timing. Il classifier usa `engine_step` senza source/phase. | Il blocker clock C1 non e chiuso: authoritative field e sampling phase restano non verificabili per feature. | Ripristinare i record temporali con clock autorevole, formula, phase e availability. `canonical_step` deve restare solo diagnostico e non alimentare deadline engine. |
| `P1-03` | `P1 MAJOR` | Livestock care bonus | C2 perde la congiunzione obbligatoria FEED+CARE. | C2 §16 riassume `CARE -> pending_care_bonus`; engine `_daily_refresh_animals` incrementa il bonus solo se `cared_today and fed_today`. La Reconciliation REC-08 e Antigravity FND-08 lo stabiliscono esplicitamente. | Una feature downstream potrebbe attribuire accumulo a CARE-only e stimare stato/yield non esistenti. | Definire accumulo come evento EOD `cared_today AND fed_today`; distinguere accumulo dal consumo su production day alimentato e dal semplice flag `cared_today`. |
| `P1-04` | `P1 MAJOR` | `POLICY_CONTEXT`, `TELEMETRY_ONLY`, `OUTCOME_LABEL` | Gli aumenti 2 -> 6, 3 -> 9 e 1 -> 3 non sono enumerati e mostrano rischio di catalogare campi event/provenance come feature. | C2 §2.2 fornisce solo conteggi. §15 nomina i quattro elementi C1; §19 dichiara esplicitamente che l'event schema non e una feature. Nessun ID identifica i 4 policy context, 6 telemetry e 2 outcome aggiunti. | Over-expansion e duplicazione non sono auditabili; campi come `transition_reason` e `executed_quantity` possono essere confusi con information objects. | Enumerare ogni elemento; spostare i puri event/provenance fields nello schema telemetry; conservare nel catalogo soltanto oggetti informativi con semantica, formula e granularita proprie. |
| `P2-01` | `P2 MINOR` | `CRP-18 active_crop_surface` | C2 degrada impropriamente la formula base a `PARTIALLY_KNOWN`. | C1 definisce `count(tile.kind == PLANT)`; C2 §9.1 e §17 la rende partial per scope/inclusion. | Si confonde formula del count con il contratto di scope. | Mantenere la formula base `FORMULA_COMPLETE=YES`; marcare il contratto `NO` finche board scope e phase non sono dichiarati. |
| `P2-02` | `P2 MINOR` | `action_eligible_now` | La definizione include genericamente "reachability", sovrapponendosi a serviceability. | C2 §8.2 include actor position or reachability; §8.3 riserva raggiungimento entro deadline a serviceability. | Ambiguita fra azione eseguibile nel tick corrente e percorso futuro. | Definire eligibility-now con actor gia nella posizione/relazione richiesta e precondizioni correnti; lasciare path e scheduling a `serviceable_before_deadline`. |
| `NOTE-01` | `NOTE` | Consumer neutrality | La rimozione di `current_MODEL_SPEC_usage` e il contratto di consumer matrix esterna sono corretti. | C2 §§1, 3 e 18 sono coerenti con REC-11/REC-12. | Nessun difetto intrinseco. | `NO_CHANGE`; non inserire runtime trace nel Feature Model. |
| `NOTE-02` | `NOTE` | HARVEST e crop risk | Il readiness predicate e la separazione missed-WATER/lifespan/random eligibility sono sostanzialmente corretti. | C2 §§6-7; engine HARVEST gate e tre cause WEED gia verificate. | Queste parti possono essere riusate nella revisione. | Preservare formule e divieto di `time_to_random_weed`; materializzarle nei record del catalogo. |

## 3. Audit 59 -> 74

### 3.1 Risultato quantitativo

| Verifica | Risultato |
|---|---:|
| ID canonici espliciti in C1 | 59 |
| ID canonici espliciti nel catalogo C2 | 0 |
| Righe della migration table C2 | 7 |
| Totale dichiarato C2 | 74 |
| Somma classi dichiarate C2 | 74 |
| Concept heading effettivi nel registry Ontology C2 | 75 |

Il candidato non permette di associare i conteggi di classe ai membri. La
coincidenza fra totale dichiarato del Feature Model e totale dichiarato
dell'Ontologia non e evidenza di validita: la foundation ammette esplicitamente
`NONE_DIRECT` e non richiede una biiezione.

### 3.2 Elementi nuovi, splittati o riclassificati rilevanti

| feature_id | C1/C2 origin | C2 class dichiarata/inferibile | legitimate_catalog_member | reason | recommended_action |
|---|---|---|---|---|---|
| `TMP-01` / `engine_step` | C1, rinomina/clarification | non assegnata per-record | `YES` | Campo engine autorevole e decision-time observable. | Preservare `TMP-01`; usare `engine_step` come nome canonico e versionare la rinomina. |
| `TMP-04` / `canonical_step` | C1, clarified | `DERIVED_FEATURE` in prosa | `CONDITIONAL` | Derivabile online, ma valido solo come diagnostica/replay alignment. | Preservare ID e aggiungere validity limit che ne vieti l'uso per engine deadlines. |
| `CRP-09` / `tile_lifecycle_state` | C1, clarified | `DERIVED_FEATURE` | `YES` | Oggetto categoriale comune, ma classifier C2 errato. | Preservare ID dopo correzione P0-02. |
| `CRP-10` / `harvest_ready` | C1, formula versioned | `DERIVED_FEATURE` | `YES` | Predicato completo, online, no leakage. | Preservare ID e formula completa. |
| `CRP-17` / `crop_decay_risk_window` | C1, clarified | `DERIVED_FEATURE` | `YES` | Struttura multi-causa informativa. | Preservare ID e dare formula/clock a ogni componente. |
| `CRP-18` / `active_crop_surface` | C1, reclassified | `DERIVED_FEATURE` | `YES` | Count semplice legittimo; scope contract distinto. | Annullare il downgrade della formula; mantenere contratto non completo. |
| `state_capacity_alignment` | Non presente come feature ID C1; C2 la chiama reclassified | non assegnata, `NOT_FROZEN` | `CONDITIONAL` | Concetto ontologico possibile, ma nessuna formula. | Assegnare nuovo ID solo se resta nel catalogo; non presentarlo come migrazione C1. |
| `tile_need` | C2 added | non assegnata | `CONDITIONAL` | Puo essere una famiglia di predicati meccanici, non necessariamente una singola feature. | Definire domain/action class o mantenere predicati specifici (`care_due`, readiness). |
| `action_eligible_now` | C2 added | non assegnata | `CONDITIONAL` | Legittimo predicato actor-action-state se completamente definito. | Assegnare ID e separare precondizioni engine da policy admissibility. |
| `serviceable_before_deadline` | C2 added | `PARTIALLY_KNOWN`, classe non assegnata | `CONDITIONAL` | Stima dipendente da routing, scheduling, contention e policy memory. | Classificare come derived/policy-context con formula non completa e `freeze_ready=NO`. |
| `worker_multi_occupancy` | C2 added da evidence engine | non assegnata | `CONDITIONAL` | La regola statica appartiene a Ontologia/State Machine; una feature richiede un valore, es. co-location count. | Tenere la capability upstream oppure definire una feature osservabile per-coordinate. |
| `fertilizer_effect_window` | C2 added | non assegnata | `YES` | Finestra per-tile deterministica `day..day+2`. | Aggiungere ID, sources, active predicate/days remaining e phase. |
| `crop_fertilizer_bonus` | C2 added | non assegnata | `CONDITIONAL` | La regola +2 e upstream; la feature deve rappresentare eligibility/incremento corrente. | Definire un oggetto per-tile, senza inferenza economica. |
| `pending_care_bonus` / accumulation | C2 added | non assegnata | `YES` | Stato engine/informazione corrente utile, con transizione congiunta FEED+CARE. | Aggiungere record raw/derived e formula EOD corretta. |
| `shed_overflow_eod_loss` | Split/correction di C1 inventory mapping | non assegnata | `CONDITIONAL` | Il rischio pre-EOD e il loss realizzato post-EOD hanno timing diverso. | Splittare derived risk/amount-if-unchanged da realized telemetry event. |
| `displayed_quote` | C2 provenance split | non assegnata | `YES` | Stato market pre-request osservabile se esposto. | Catalogare come raw observable con source e phase. |
| `requested_quantity` | C2 provenance split | non assegnata | `NO` | E un campo del comando/event schema, non una feature comune autonoma. | Spostare in event schema/policy action record. |
| `executed_quantity` | C2 provenance split | non assegnata | `NO` | Esito post-action di un ordine. | Spostare in event schema; usarlo come source per metriche telemetry. |
| `realized_price` | C2 provenance split | non assegnata | `NO` | Provenance post-execution, non feature decision-time. | Event schema; mantenere `MKT-02` come metrica derivata se formalizzata. |
| `cash_delta` | C2 provenance split | non assegnata | `NO` | Campo evento post-action, non oggetto informativo autonomo. | Event schema con order/event ID. |
| `estimate` | C2 provenance split | non assegnata | `NO` | Valore consumer-specific senza metodo/versione comune. | Consumer matrix o diagnostic record con provenance, non catalogo comune. |
| `current_MODEL_SPEC_usage` | C1 consumer column, deprecated | non feature | `NO` | Proprieta del consumer, non della feature. | Conservare solo in consumer matrix storica esterna. |
| `TEL-NEW-01..06` | incremento dichiarato C2 | `TELEMETRY_ONLY` | `NO` finche non identificati | Nessun ID, semantica o formula nel documento. | Enumerare; spostare i puri event fields fuori catalogo. |
| `LBL-NEW-01..02` | incremento dichiarato C2 | `OUTCOME_LABEL` | `NO` finche non identificati | Nessun ID o definizione. | Enumerare o rimuovere dal conteggio. |
| `POL-NEW-01..04` | incremento dichiarato C2 | `POLICY_CONTEXT` | `NO` finche non identificati | Nessun ID; il testo cita genericamente assumptions e policy memory. | Enumerare contesti comuni; rimuovere memoria/assunzioni consumer-specifiche. |

## 4. Lifecycle classifier review

### 4.1 Boundary audit

| Input richiesto | Esito C2 | Review result | Motivo |
|---|---|---|---|
| `LOCKED` | tenta `tile.kind == "LOCKED"` | `FAIL` | Il valore engine e la stringa `"LOCKED"`; il contratto non dichiara una normalizzazione. |
| outside working set | `OUT_OF_SCOPE` | `PASS` per tile non-None | Precedence policy-context coerente. |
| `None` inside working set | `OUT_OF_SCOPE` | `FAIL` | Il primo ramo precede il controllo working set; `EMPTY_ASSIGNED` e irraggiungibile per il valore engine valido. |
| `WEED` inside working set | `LOST_WEED` | `PASS` se rappresentata come dict normalizzato | No leakage. |
| PLANT immature con `yield_units > 0` | normalmente `GROWING` | `CONDITIONAL_FAIL` | Diventa erroneamente `RETIREMENT_DUE` se lifespan crossing, anche per non-ongoing. |
| PLANT mature con `yield_units > 0` | normalmente `HARVEST_READY` | `CONDITIONAL_FAIL` | Il ramo lifespan ha precedence e puo mascherare una raccolta ancora valida prima del decay di fase 8. |
| ongoing subito dopo HARVEST intermedio | `GROWING` | `PASS` | La tile resta PLANT con yield zero e produzione futura. |
| ongoing subito dopo HARVEST finale | non definito esattamente | `FAIL` | Deve essere `RETIREMENT_DUE`, mai `EMPTY_ASSIGNED`; HARVEST ongoing non rimuove la tile. |
| ongoing prima di produzione futura | `GROWING` | `PASS` se lifespan non impostata | Schedule statico noto, nessun leakage. |
| ongoing all'ultima produzione, prima di HARVEST | `RETIREMENT_DUE` possibile | `FAIL` | Con yield positivo deve restare `HARVEST_READY`; retirement segue il valid final HARVEST. |
| ongoing dopo final HARVEST | `RETIREMENT_DUE` atteso | `FAIL` come predicato esplicito | Mancano `ongoing`, `yield_units == 0` e assenza di future production. |
| non-ongoing prima della maturity | `GROWING` | `PASS` solo prima del lifespan crossing | Il solo `max_lifespan_step` non puo creare retirement. |
| invalid/missing telemetry input | OOS o invalid record | `FAIL` | Errore dati e stato engine valido non devono essere collassati; la funzione usa inoltre variabili/campi non validati. |

### 4.2 RETIREMENT_DUE e leakage

Il calendario di produzione ongoing e statico, noto da `crop_rules` e dallo
stato corrente. Derivare che non esistono produzioni schedulate residue non e
future leakage. E leakage usare invece l'esito futuro di un'azione, un draw RNG
o una produzione non determinata dalle regole correnti.

Il classifier corretto deve almeno applicare:

```text
if invalid_input:
    return INVALID_DIAGNOSTIC_RECORD  # fuori dal lifecycle
if not in_working_set or tile == "LOCKED" or tile is non-crop structure:
    return OUT_OF_SCOPE
if tile is None:
    return EMPTY_ASSIGNED
if tile.kind == "WEED":
    return LOST_WEED
if tile.kind == "PLANT":
    ready = yield_units > 0 and age >= first_yield_day
    retired = crop_rules.ongoing \
              and yield_units == 0 \
              and max_lifespan_step >= 0 \
              and no_future_scheduled_production(current_state, crop_rules)
    if ready:
        return HARVEST_READY
    if retired:
        return RETIREMENT_DUE
    return GROWING
```

`phase` e `engine_step` devono essere input dichiarati soltanto per i predicati
che li consumano; il raggiungimento della lifespan e un risk/deadline predicate,
non la definizione di retirement.

## 5. Aggregate-contract review

Il documento definisce un **template di schema**, non contratti compilati.
Pertanto `contract schema complete?` vale `NO` per ogni riga. La formula base di
alcuni count C1 resta nota, ma non rende l'aggregate C2 freeze-ready senza scope,
phase e versionamento.

| feature_id | contract schema complete? | formula complete? | denominator canonical? | sampling phase defined? | dedup defined? | online computable? | freeze-ready? | missing evidence/definition |
|---|---|---|---|---|---|---|---|---|
| `CRP-18 active_crop_surface` | NO | YES, core count C1 | N/A | NO | NO | YES | NO | board/ownership/working-set scope, phase, formula version |
| `CRP-19 crop_surface_maintained` | NO | NO | N/A | NO | NO | CONDITIONAL | NO | included states, maintenance window/success rule |
| `CRP-20 watering_execution_rate` | NO | NO | NO | NO | NO | YES per history past | NO | request/execution predicate, tile-day demand denominator, retries |
| `CRP-21 watering_continuity` | NO | NO | NO | NO | NO | YES per history past | NO | interval closure, gaps, late service, zero-demand convention |
| `CRP-22 crop_care_completion_rate` | NO | NO | NO | NO | NO | CONDITIONAL | NO | canonical need set, completion predicate, dedup tile/day/task |
| `CRP-23 crop_harvest_action_flow` | NO | NO | NO | NO | NO | YES per history past | NO | requested/executed/valid/yielded stages and event IDs |
| `CRP-24 field_cleanliness_state` | NO | PARTIAL | N/A | NO | NO | YES | NO | WEED map/count e scope sono computabili; nessuno scalar cleanliness canonico |
| `CRP-25 weed_backlog_cost` | NO | NO | NO/N/A | NO | NO | CONDITIONAL | NO | recovery actions, opportunity-cost method, attribution window |
| `WRK-03 worker_capacity_available` | NO | PARTIAL | N/A | NO | NO | YES per theoretical slots | NO | separare theoretical action slots da effective/service capacity |
| `WRK-04 movement_overhead` | NO | PARTIAL | NO | NO | NO | YES per history past | NO | MOVE count vs necessary transit, denominator e attribution |
| `WRK-05 action_dispatch_failure` | NO | NO | NO/N/A | NO | NO | YES per completed past events | NO | request/execution/no-op taxonomy, failure reason, dedup |
| `WRK-06 productive_action_share` | NO | NO | NO | NO | NO | CONDITIONAL | NO | productive taxonomy, denominator, failed/PASS/MOVE treatment |
| `NEW-ID state_capacity_alignment` | NO | NO | NO | NO | NO | NO | NO | components, weights, formula, scope, examples |
| `MKT-03 operating_cash_buffer` | NO | NO | N/A | NO | NO | CONDITIONAL | NO | versioned obligation model, horizon, treatment of committed orders |

La futura tabella deve esporre due campi distinti:

```text
CONTRACT_SCHEMA_COMPLETE: YES | NO
FEATURE_FORMULA_COMPLETE: YES | NO
```

Il primo certifica che tutti i metadati richiesti sono compilati; il secondo
certifica che l'algoritmo produce un unico valore. `FEATURE_FORMULA_COMPLETE=NO`
implica sempre `freeze_ready=NO`.

## 6. Consumer-neutrality review

### Verdetto

```text
CONSUMER_NEUTRALITY: PASS
```

C2 non usa `USED`, `FULL` o `NOT_USED` come proprieta intrinseca delle feature,
non include il Codex E15 frozen come consumer autorevole e non incorpora
Copilot/Antigravity runtime nella semantica. La consumer matrix e correttamente
esterna e versionata.

L'assenza di un "consumer-neutral runtime mapping eseguibile" dentro il Feature
Model **non e un difetto intrinseco del Feature Model**. L'architettura corretta
e:

```text
FEATURE MODEL = consumer-neutral
CONSUMER MATRIX = consumer-specific
RUNTIME TRACE = consumer-specific
```

Consumer matrices e runtime traces restano freeze exit criterion downstream
prima di dichiarare conforme un MODEL_SPEC C2, non contenuto da inserire nel
catalogo comune.

## 7. Clock / phase review

La distinzione di principio `engine_step != canonical_step` e corretta. Non e
pero sufficiente: mancano i record C2 delle feature temporali e quindi non sono
verificabili clock, phase e availability per ciascuna.

| Informazione | Review |
|---|---|
| `harvest_ready` | Corretta: usa `day`, `planted_day`, regola statica; pre-action. |
| `care_due` | Concettualmente corretta; manca record con sampling pre-action e reset EOD. |
| `water_loss_at_eod_if_unserved` | Causalmente corretta; manca formula/version/phase. |
| `action_phases_until_eod_refresh` | Non materializzata; deve usare `hour`/`turnsPerDay` e dichiarare inclusivita della fase corrente. |
| `lifespan_decay_started` | Non materializzata; deve usare `engine_step`, mai `canonical_step` come source engine. |
| `next_lifespan_decay_phase` | Non materializzata; richiede periodicita pari da `max_lifespan_step` su engine clock. |
| `lifespan_loss_phase_if_no_action` | Non materializzata; e un deadline no-intervention, non prediction della policy. |
| `fertilizer_effect_window` | Regola day-based corretta in prosa; mancano ID, source, action/EOD phase. |
| livestock production timing | Schedule statico decision-time derivable; manca feature/contract; CARE bonus formula e inoltre errata. |

Non deve essere assunta equivalenza numerica fra i due clock, neppure quando i
valori coincidono in un replay specifico.

## 8. HARVEST e crop decay review

### HARVEST

Il predicato C2 §6 e corretto per ongoing e non-ongoing:

```text
tile.kind == "PLANT"
AND tile.yield_units > 0
AND day - tile.planted_day >= CROPS[tile.crop].first_yield_day
```

Nessun aggregate C2 afferma esplicitamente `yield_units > 0 => harvestable`.
Il classifier §5 puo tuttavia mascherare readiness con il ramo lifespan e deve
essere corretto come P0-02.

### Crop decay

C2 mantiene correttamente separati:

- missed-WATER deterministico a EOD;
- lifespan deterministico su `engine_step`;
- sola eligibility/hazard RNG per `EMPTY -> WEED`.

Il rigetto di `time_to_random_weed` deterministico e confermato. Manca il
contratto computazionale per le componenti lifespan, non la separazione causale.

## 9. Need / eligibility / serviceability review

| Livello | Classificazione corretta | Stato C2 |
|---|---|---|
| `tile_need` | Predicato meccanico/biologico indipendente dall'attore; `DERIVED_FEATURE` o famiglia di feature specifiche. | Concettualmente corretto, non catalogato. |
| `action_eligible_now` | Predicato actor-action allo stato e phase correnti, incluse risorse e co-location. | Parziale; il termine reachability va rimosso o ristretto all'adiacenza corrente. |
| `serviceable_before_deadline` | Stima derivata da routing, scheduling, inventory, contention, phase e policy memory. | Correttamente `PARTIALLY_KNOWN` e non garantito; non catalogato. |

`serviceable_before_deadline` non e freeze-ready e non puo diventare gate
operativo finche formula, sources, policy-memory version e boundary examples non
sono completi.

## 10. Workforce, inventory e market provenance

### Workforce

C2 separa correttamente posizione, headcount, capacity, movement, dispatch e
serviceability. `worker_multi_occupancy` non implica serviceability, capacita
doppia o assenza di contention. Resta da decidere se la capability statica
appartenga solo upstream o se esista una feature per-coordinate derivata dalle
posizioni.

### Inventory

La correzione e sostanzialmente corretta:

```text
worker inventory != shed inventory != seed inventory
automatic EOD transfer
loss only from shed overflow
```

Non viene reintrodotto il falso obbligo di rientro worker. Serve pero uno split
tra rischio/quantita pre-EOD derivabile e `shed_overflow_eod_loss` realmente
osservato post-refresh.

### Market

Le sei nozioni sono correttamente separate in prosa. La loro sede non e la
stessa:

| Oggetto | Sede corretta |
|---|---|
| displayed quote pre-request | raw observable feature, se esposto |
| requested quantity | policy action/event schema |
| executed quantity | post-action event schema |
| realized price | post-action provenance field |
| cash delta | post-action event field |
| estimate | consumer-specific diagnostic con method/version |

Nessun post-action value puo essere input della richiesta che lo ha generato.

## 11. TELEMETRY_ONLY e OUTCOME_LABEL audit

| Elemento | Classe C2 attesa | Catalog member? | Decisione |
|---|---|---|---|
| `MKT-02 market_transaction_value` | `TELEMETRY_ONLY` derived metric | `CONDITIONAL` | Puo restare se definito da executed quantity e realized price con provenance. |
| `GLB-02 action_execution_result` | event field / diagnostic record | `NO` | Spostare nello schema eventi; gli aggregate di failure lo consumano. |
| `GLB-03 transition_reason` | provenance/event field | `NO` | Spostare nello schema eventi; non e una feature autonoma. |
| `LBL-01 final_money_outcome` | `OUTCOME_LABEL` | `YES` | Conservare come target terminale, mai input pre-termine. |
| sei nuovi `TELEMETRY_ONLY` dichiarati | non identificabili | `NO` finche non enumerati | Pubblicare ID/semantica o rimuovere dal conteggio. |
| due nuovi `OUTCOME_LABEL` dichiarati | non identificabili | `NO` finche non enumerati | Pubblicare ID/target timing o rimuovere dal conteggio. |

La crescita 3 -> 9 e 1 -> 3 non e supportata dal documento. La sola necessita
di logging non trasforma una colonna dello schema evento in feature.

## 12. POLICY_CONTEXT audit

| Oggetto nominato/inferibile | Legittimita | Decisione |
|---|---|---|
| `FRM-03 working_set_member` | `YES` | Contesto comune indispensabile per `EMPTY_ASSIGNED`; mantenere assignment/version. |
| `MKT-03 operating_cash_buffer` | `CONDITIONAL` | Richiede obligation model versionato; nessun floor numerico nel Feature Model. |
| `tile_need` | non e policy context per natura | Classificare derived meccanico; working-set scope puo essere policy context separato. |
| `action_eligible_now` | misto | Separare engine eligibility da reservation/policy admissibility. |
| `serviceable_before_deadline` | `CONDITIONAL` | Policy-memory dependent, `PARTIALLY_KNOWN`, non gate. |
| generic `policy_memory` | `NO` come singola feature | E storage/version provenance; catalogare solo valori semantici specifici. |
| `actor position assumptions` | `NO` | Posizioni reali sono raw state; assunzioni consumer-specifiche restano nel consumer. |
| quattro nuovi POLICY_CONTEXT dichiarati | non identificabili | Enumerare con ID o rimuovere dal conteggio. |

Non sono presenti soglie, target, learned weights o strategie specifiche dei tre
modeler. Il problema e l'assenza di membership esplicita, non policy leakage
numerico.

## 13. Coerenza verticale

| Ontology C2 concept | State Machine C2 state/transition | Feature Model C2 representation | status | issue |
|---|---|---|---|---|
| `crop_harvest_readiness` | `GROWING -> HARVEST_READY`; HARVEST gate | `harvest_ready` in prosa | `ALIGNED_PARTIAL` | Formula corretta, record/ID assente. |
| `tile_lifecycle_state` | sei stati e transizioni | classifier §5 | `CONFLICT` | Classifier contraddice None/retirement e usa input indefiniti. |
| `crop_decay_risk_window` | missed-WATER, lifespan, RNG spawn distinti | struttura §7 | `ALIGNED_PARTIAL` | Causalita corretta; clock/formule componenti assenti. |
| `tile_care_due_condition` | predicato ortogonale | `tile_need`/care prose | `ALIGNED_PARTIAL` | Record/phase assente. |
| `worker_multi_occupancy` | co-location engine-verified | workforce prose | `NONE_DIRECT_VALID` | Capability statica non richiede per forza una feature dedicata. |
| `fertilizer_effect_window` | day..day+2, action/EOD effects | livestock/fertilizer prose | `ALIGNED_PARTIAL` | Manca feature ID e phase contract. |
| `pending_care_bonus_accumulation` | State Machine C2 §9/transition table indica CARE accumulation, ma engine e Reconciliation richiedono FEED+CARE a EOD | `CARE -> pending_care_bonus` | `UPSTREAM_AND_FEATURE_CONFLICT` | La stessa congiunzione FEED e persa upstream e nel Feature Model; prevale l'evidenza engine normativa. |
| `shed_overflow_eod_loss` | auto-drop EOD e overflow | inventory provenance prose | `ALIGNED_PARTIAL` | Manca split pre-EOD risk / realized post-EOD loss. |
| `crop_surface_maintained` | derived from lifecycle/maintenance | aggregate partial | `ALIGNED_INCOMPLETE` | Formula e contratto non completi, correttamente non freeze-ready ma non materializzati. |
| `state_capacity_alignment` | nessuna transizione engine dedicata | `NOT_FROZEN` prose | `NONE_DIRECT_VALID` | Non deve diventare feature completa senza formula. |
| `market_transaction_value` | market execution phase | telemetry prose | `ALIGNED_PARTIAL` | Serve record metric con executed provenance; event fields separati. |
| `final_money_outcome` | terminal reward | outcome prose | `ALIGNED_PARTIAL` | Label legittima, record assente. |
| clock engine/canonical | phase map C2 | clock §4 | `ALIGNED_PARTIAL` | Principio corretto; applicazione per-feature assente. |

Non e richiesta una biiezione. Il problema dominante non e la presenza di
`NONE_DIRECT`, ma l'assenza dell'intero layer di rappresentazione tabellare che
consenta di dimostrare il mapping.

## 14. Deviazione procedurale Copilot

```text
IMPACT: MATERIAL
```

Il mandato `COPILOT_FEATURE_MODEL_C2.md` richiedeva esplicitamente la lettura
integrale della review Antigravity. La dichiarazione di non averla letta non e
un criterio di penalizzazione automatico, perche la Reconciliation Codex aveva
gia arbitrato entrambe le review e poteva trasferire i finding.

L'impatto sostanziale e pero materiale su un punto: Feature Model C2 §16 e la
formulazione upstream di State Machine C2 §9 degradano FND-08 da `FEED AND CARE
-> pending_care_bonus increment at EOD` a `CARE -> pending_care_bonus`.
Multi-occupancy, FERTILIZE e shed overflow sono invece stati recepiti.
L'omissione non spiega tutti i blocker, ma ha coinciso con la perdita di un
finding engine-verified che la fonte obbligatoria e la reconciliation esponevano
in modo inequivoco.

## 15. Lista fix richiesta

Questi interventi costituiscono una revisione architetturale del documento, non
local fixes:

1. Ripubblicare il catalogo completo con una riga per ogni feature e almeno:
   `feature_id`, name, class, type, ontology/state mapping, source variables,
   derivation/formula version, granularity, authoritative clock, sampling phase,
   online/decision-time availability, leakage, evidence, validity limits,
   `CONTRACT_SCHEMA_COMPLETE`, `FEATURE_FORMULA_COMPLETE`, `freeze_ready`.
2. Preservare tutti i 59 ID C1 salvo deprecation/split espliciti; assegnare ID
   nuovi alle sole aggiunte legittime; ricostruire una migration table esaustiva
   e ricontare le classi senza importare il numero dei concept ontologici.
3. Correggere il classifier come in §4.2 e aggiungere test vectors per tutti i
   boundary richiesti, inclusi final ongoing pre/post HARVEST e invalid input.
4. Materializzare `CRP-13..15` e ogni feature temporale con `engine_step` o
   day/hour appropriato; mantenere `canonical_step` diagnostico.
5. Compilare un aggregate contract per ciascun aggregate; separare schema e
   formula completeness; marcare ogni formula incompleta `freeze_ready=NO`.
6. Enumerare le 9 telemetry, 3 outcome e 6 policy-context candidates; spostare
   event/provenance/storage fields fuori dal catalogo e ricalcolare i conteggi.
7. Correggere livestock bonus con la congiunzione FEED+CARE EOD e consumo
   distinto su production day alimentato.
8. Ripristinare la formula completa di `active_crop_surface`, lasciando
   incompleto soltanto il suo contract scope/phase.
9. Separare eligibility corrente da reachability/serviceability futura.
10. Aggiungere la matrice verticale effettiva per ogni feature, ammettendo
    `NONE_DIRECT` e segnalando upstream inconsistencies senza copiarle.

## 16. Freeze blockers

```text
BLOCKER 1: no canonical 74-row feature catalog or auditable migration exists
BLOCKER 2: tile_lifecycle_state classifier is incorrect and non-executable
MODEL_SPEC_C2_UPSTREAM_READY: NO
```

Aggregate contracts, temporal records e class expansion sono material gaps che
devono essere risolti nella stessa revisione. Non e sufficiente applicare poche
correzioni locali al testo esistente.

## 17. Test e check

| Check | Risultato |
|---|---|
| `git diff --check` | `PASS` (exit 0) |
| `.\.venv\Scripts\pytest.exe` | `PASS`: 143 passed in 79.21s |
| Pytest warning | cache non scrivibile: `.pytest_cache`, `WinError 5`; non incide sui test |
| `.\.venv\Scripts\ruff.exe check .` | `FAIL`: 4803 errori repository-wide, 4118 auto-fixable |
| Relazione ruff con la review | Preesistenti/non correlati; il nuovo artefatto e Markdown e non modifica codice Python |

Non sono stati eseguiti episodi, benchmark, training o modifiche a MODEL_SPEC,
runtime, policy e telemetry implementation.

## 18. Repository status

Lo status riportato al termine e quello completo del workspace condiviso. Le
modifiche non relative alla review erano gia presenti e non sono state alterate.

```text
M  docs/experiment_designs/e16/CODEX_E16_TRAINING_PROPOSAL.md
M  docs/experiment_designs/e16/COPILOT_E16_TRAINING_PROPOSAL.md
 D docs/experiments/E04-01_Competitive_Gap_Analysis.md
 D docs/experiments/E04-02_Experimental_Direction_Decision.md
 D docs/experiments/E05-01_HIRE_Capability_Analysis.md
 D docs/experiments/E06-01_Water_First_Capability_Analysis.md
M  docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C1.md
R  docs/model/model_specs/post_e15/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md -> docs/model/model_specs/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md
R  docs/model/model_specs/post_e15/ANTIGRAVITY_MODEL_SPEC_REVISION.md -> docs/model/model_specs/antigravity/ANTIGRAVITY_MODEL_SPEC_REVISION.md
R  docs/model/model_specs/post_e15/CODEX_MODEL_SPEC_REVISION.md -> docs/model/model_specs/codex/CODEX_MODEL_SPEC_REVISION.md
R  docs/model/model_specs/post_e15/COPILOT_MODEL_SPEC_REVISION.md -> docs/model/model_specs/copilot/COPILOT_MODEL_SPEC_REVISION.md
 D docs/plans/E01_Kaggriculture_Agent_implementation_plan.md
 D docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md
 D docs/plans/E03_Multi_Tile_Scaling.md
 D docs/plans/E04_Initial_NW_Scaling.md
 D docs/plans/E05_HIRE_MultiWorker_Scaling.md
 D docs/plans/E06_Water_First_Scheduling.md
 D docs/plans/E07_Competitive_Baseline_Reconstruction.md
 D docs/plans/E08_Productive_Scale_Optimization.md
 D docs/walkthroughs/E01_walkthrough.md
 D docs/walkthroughs/E01_walkthrough_consolidated.md
 D docs/walkthroughs/walkthrough.md
?? docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
?? docs/model/ontology/ONTOLOGY_C2.md
?? docs/model/reviews/codex/
?? docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
?? docs/prompts/ANTIGRAVITY_MODEL_FOUNDATION_REPOSITORY_REORGANIZATION.md
?? docs/prompts/ANTIGRAVITY_MODEL_SPECS_CLEANUP_AND_ONTOLOGY_C2.md
?? docs/prompts/ANTIGRAVITY_ONTOLOGY_C2_MICRO_REVIEW.md
?? docs/prompts/ANTIGRAVITY_STATE_MACHINE_C2.md
?? docs/prompts/CODEX_FEATURE_MODEL_C2_REVIEW_R1.md
?? docs/prompts/CODEX_FOUNDATION_RECONCILIATION_R1_PROMPT.md
?? docs/prompts/COPILOT_FEATURE_MODEL_C2.md
?? docs/prompts/E16_A_R1_CODEX_FORENSIC_DIAGNOSIS_PROMPT.md
?? docs/prompts/E16_CODEX_TILE_LIFECYCLE_FEATURE_AUDIT.md
?? results/e16/diagnostics/
?? scripts/audit_e16_tile_lifecycle_feature.py
?? scripts/diagnose_e16_a_r1_crop_attainment.py
```

FEATURE MODEL C2 REVIEW: COMPLETED
FEATURE MODEL C2 VERDICT: REVISE_MAJOR
MODEL_SPEC_C2_UPSTREAM_READY: NO
FOUNDATION C2: NOT FROZEN
