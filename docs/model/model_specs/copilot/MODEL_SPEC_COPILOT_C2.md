# MODEL_SPEC_COPILOT_C2.md

```text
AGENT_ID = COPILOT
STATO = CANDIDATE C2 / POST PERFORMANCE_CORRECTION PASS (POST-FOUNDATION-FREEZE)
FOUNDATION_CHECKPOINT = f391ee2
TOURNAMENT_READY = NO (TOURNAMENT_AUTHORIZED remains NO at this gate)
```

## 1. Scopo e ipotesi operativa

Il concorrente COPILOT costruisce una policy C2 centrata su un principio di prevenzione: evitare gli errori già diagnosticati in E16, prima di ricorrere a recovery e riassegnazione. La performance iteration corregge il limite di capacità osservato nel retournament: il ciclo minimo era realizzato, ma un core di quattro tile e un solo worker non poteva generare throughput competitivo.

- premature HARVEST dispatch;
- irrigazione intermittente non corretta;
- perdita di tile deterministica che diventa WEED;
- assenza di un criterio di clearance preventivo.

La policy assume che la soluzione più forte sia mantenere un working set stabile, rispettare il lifecycle canonico e fermare ogni action che violi la semantica `harvest_ready` e `care_due` dell'engine.

## 2. Evidenza utilizzata

- E15: CLOSED
- E16 Stage A-R1: COMPLETED 28/28
- dominant bottleneck: POLICY_REALIZATION
- failure forensic: 5,804 / 5,804 crop HARVEST attempts prima della maturity
- policy frozen: `yield_units > 0` == harvest-ready (falso)
- engine requirement: `tile.kind == PLANT AND yield_units > 0 AND age >= first_yield_day`
- evidence: 89.86% HARVEST prematuro su attempts analizzati
- evidence: `WEED` permanente senza DIG dopo perda deterministica
- state machine C2 + ontology C2 + feature model C2

## 3. Diagnosi causale prioritaria

La catena causale supportata è:

```text
routing + workforce intermittency
    + premature HARVEST dispatch
    ↓
service/action waste
    ↓
crop loss
    ↓
WEED / lost tile
    ↓
no recovery / no replant
    ↓
irreversible target gap
```

Il nostro modello assegna massima priorità a due meccanismi:

1. bloccare HARVEST prematuro con una gate `harvest_ready` rigorosa;
2. impedire la perdita di tile in `LOST_WEED` o in `policy_retirement_due` (`POL-RET`) senza clearance preventiva.

## 4. Ipotesi causale performance iteration

```text
HYPOTHESIS_ID: COPILOT_C2_PI_H1_SERVICEABLE_NW_THROUGHPUT
OBSERVED_PROBLEM: mean final money $4,154, active max 4, workforce max 1,
  no land expansion e minimum cash $2,920 nel retournament valido.
EVIDENCE: PLANT/WATER/HARVEST/MOVE Copilot producevano state transition;
  non esiste evidenza di un service o biological failure nel core, mentre
  $2,920 di capitale restavano inutilizzati.
CAUSAL_MECHANISM: il working set 3x3 configurato con raggio 1 era ulteriormente
  ridotto a quattro tile raggiunte da un farmer senza hand. Il throughput di
  raccolto e vendita era quindi limitato dalla capacità, non dalla correttezza
  del lifecycle.
MODEL_CHANGE: lavorare tutte le 25 tile possedute nel quadrante NW con una
  workforce totale di 9, assegnazione greedy a target distinti, WHEAT rapido,
  semina entro day 27 e vendita/reinvestimento continui.
EXPECTED_INTERMEDIATE_EFFECT: active surface >=20 e workforce >=9 in preflight
  P0/P1, con WATER, HARVEST e SELL che producono transizioni osservabili.
EXPECTED_ECONOMIC_EFFECT: maggiore massa serviceable e throughput monetizzato;
  direzione final_money UP verso mean >$23,000 nel prossimo tournament.
FALSIFICATION_CONDITION: se P0 o P1 non raggiunge 20 PLANT e 9 unità, oppure
  non osserva WATER, HARVEST e SELL effect, H1 è falsificata. Il target
  economico resta falsificato dal prossimo tournament se mean <=$23,000.
```

## 5. Meccanismi NON prioritari

- market timing e ottimizzazione dei prezzi: secondari rispetto alla pulizia e alla continuità del working set;
- seed scarcity oltre il bootstrap del working set: non è il collo di bottiglia principale in E16 R1;
- pure scale-up aggressiva: non produce beneficio se le azioni sono sprecate;
- livestock-first: fuori dal perimetro di questa versione per ridurre complessità non causale.

## 6. Feature C2 consumate

| feature_id | runtime source | calculation point | decision phase | consumer | fallback behavior |
|---|---|---|---|---|---|
| `tile_kind` | farm.tiles | pre-action | action selection | lifecycle classifier | treat unknown as `OUT_OF_SCOPE` |
| `yield_units` | tile object | pre-action | HARVEST gate | `harvest_ready` | reject if <= 0 |
| `planted_day` | tile object | pre-action | HARVEST gate | age calculation | reject if missing |
| `first_yield_day` | CROPS table | pre-action | HARVEST gate | maturity check | conservative false |
| `watered_today` | tile object | pre-action / pre-refresh | WATER policy | risk prevention | WATER if missing/false |
| `consecutive_unwatered` | tile object | pre-action | WATER policy | missed-water prevention | enforce WATER if count >= 1 |
| `max_lifespan_step` | tile object | pre-action | DIG prevention | exit lifecycle | clear on retirement |
| `tile_lifecycle_state` | derived classifier | pre-action | action arbitration | state gating | default PASS |
| `player` | observation.player | pre-action | player binding | own-farm selection | P0 only if missing |
| `private.seeds` | observation.private | pre-action | bootstrap / PLANT | seed balance | buy WHEAT for empty core |
| `private.shed` | observation.private | pre-action | market sale | harvested inventory | SELL crop units |

## 7. Regole decisionali

1. `HARVEST` è consentito solo se `harvest_ready == true`.
2. `WATER` è prioritario su tile PLANT non irrigate, specialmente quando `consecutive_unwatered + 1 >= 2`.
3. `DIG` è eseguito su `LOST_WEED` e su `GROWING` con overlay `policy_retirement_due` per ripristinare il tile.
4. La policy preferisce la prevenzione rispetto alla recovery.
5. I tile vuoti o `EMPTY_AVAILABLE` possono essere riempiti con il crop preferito solo se ci sono semi disponibili.
6. Con zero o insufficienti semi nel quadrante NW, la policy emette `BUY_SEED WHEAT` fino al fabbisogno delle tile vuote più una riserva di due seed.
7. Le unità raccolte depositate nello shed sono vendute con `SELL`; il capitale risultante finanzia il bootstrap e i replant successivi.
8. A ogni giorno la policy riassume fino a una workforce totale di nove unità, entro il limite di dieci ordini market.

## 8. Priorità / arbitration

```text
1. harvest readiness validity
2. water maintenance / irreversible loss prevention
3. preventive DIG
4. replant / recovery
5. PASS
```

La priorità non usa una matrice avanzata: usa una gerarchia deterministica e localmente verificabile.

## 9. Tile lifecycle policy

La classificazione è quella canonica del Feature Model C2 (`OUT_OF_SCOPE`, `LOST_WEED`, `EMPTY_AVAILABLE`, `HARVEST_READY`, `GROWING`, tutti `DERIVED_ENGINE_FACT`), con l'overlay `POLICY_CONTEXT` `policy_retirement_due` (`POL-RET`) sovrapposto a `GROWING` per candidati alla rimozione:

```text
OUT_OF_SCOPE
LOST_WEED
EMPTY_AVAILABLE
GROWING (+ policy_retirement_due overlay)
HARVEST_READY
```

Regole applicate:

- `tile is None` o `LOCKED` fuori working set -> `OUT_OF_SCOPE`;
- `tile is None` in posizione unlocked -> `EMPTY_AVAILABLE` (`DERIVED_ENGINE_FACT`, non un'assegnazione di policy);
- `WEED` -> `LOST_WEED`;
- `PLANT` + `yield_units > 0` + age >= `first_yield_day` -> `HARVEST_READY`;
- `PLANT` + non matured -> `GROWING`;
- `PLANT` + `yield_units == 0` + lifespan reached -> `GROWING` con overlay deliberativo `policy_retirement_due` (`POL-RET`, `POLICY_CONTEXT`) che innesca `DIG` preventivo; la Foundation non riconosce `RETIREMENT_DUE` come categoria fisica distinta e questo MODEL_SPEC allinea la propria implementazione a tale confine per conformità (P1-01 della cross-review Foundation risolto lato agent-specific).

## 10. WATER policy

La policy applica una regola conservativa:

```text
if tile.kind == PLANT and not watered_today:
    WATER
```

e in caso di rischio di perdita deterministica:

```text
if tile.kind == PLANT and not watered_today and consecutive_unwatered + 1 >= 2:
    WATER before any harvest or move decision
```

Questo evita il falso problema dei missed-WATER ma non ripristina eccessivamente la semantica R1 correggere.

## 11. HARVEST policy

```text
harvest_ready =
    tile.kind == PLANT
    AND yield_units > 0
    AND age >= first_yield_day
```

Niente `yield_units > 0` da solo. La policy rifiuta tutte le azioni `HARVEST` non conformi.

## 12. PLANT / replant policy

- se tile vuota e ci sono semi disponibili, plantare una crop preferita (`MELON` di default, dal PERFORMANCE_CORRECTION pass — vedi Sezione 24, E-C2-PERF-03);
- il replant è secondario rispetto al mantenimento delle tile già attive;
- al primo stato reale con zero seed, acquistare i semi MELON necessari a riempire tutte le 25 tile NW serviceable, senza riserva aggiuntiva (`seed_reserve=0`, E-C2-PERF-05);
- non avviare PLANT dopo day 11 (`last_plant_day=11`), perché MELON (first_yield_day=10) richiede un margine di crescita/raccolta/vendita prima del terminale a day 29 (E-C2-PERF-04); il valore 27 usato per WHEAT è troppo tardivo per un ciclo lungo come quello di MELON;
- la policy non assume un optimum economico di mezzo ciclo; il comportamento resta conservativo, ma il cutoff è ora derivato empiricamente per-crop invece che fissato genericamente.

## 13. DIG preventive / recovery policy

```text
if tile lifecycle in {LOST_WEED} or policy_retirement_due(tile): DIG
```

La policy usa `DIG` come azione di ripristino/clearance, ma non come soluzione primaria ai problemi evitabili; il suo compito è contenere il danno.

## 14. Workforce / movement policy

La policy usa le 25 tile possedute del quadrante NW come `OWNED_SURFACE` e
`SERVICEABLE_SURFACE`; `ACTIVE_SURFACE` conta le tile PLANT e
`PRODUCTIVE_SURFACE` solo quelle che ricevono WATER, HARVEST e vendita effettiva.
Ogni turno assegna greedy un target distinto a farmer e hand, minimizzando la
distanza Manhattan dell'unità disponibile.

PERFORMANCE_CORRECTION (E-C2-PERF-02): `_working_positions()` restituisce ora
tutte le tile non-`LOCKED` dell'intero board, non più un filtro hardcoded
`x<=4 and y<=4`; questo rimuove un bug che impediva l'espansione del working
set anche in presenza di `BUY_LAND` riuscito. La workforce giornaliera è
co-scalata al footprint attivo tramite `target_tiles_per_worker=6.0` come
rapporto (`ceil(active_tiles / target_tiles_per_worker)`, clampato tra
`min_workforce=2` e il tetto `target_workforce=9`), invece di un target fisso
di 9 hand/giorno indipendente dalla superficie coltivata. Questo riflette il
fatto (E-C2-PERF-01) che il costo HIRE segue una curva Fibonacci-like
per-giorno e si resetta ogni giorno (hand giornalieri, non persistenti):
assumere un target fisso indipendente dal footprint produceva sovra-hiring
costoso o sotto-hiring con idle rate elevato.

1. assegnare `HARVEST_READY`;
2. assegnare PLANT non irrigate;
3. assegnare `LOST_WEED` o tile con `policy_retirement_due` attivo;
4. assegnare tile vuote per `PLANT`, limitate ai seed realmente disponibili;
5. altrimenti `PASS`.

Il worker emette un movimento cardinale verso il target se non è già sulla tile.
Questa è una limitata allocazione serviceable NW, non routing globale o
espansione territoriale.

## 15. Inventory / market policy

La policy usa il mercato solo per chiudere il loop produttivo minimo:

- `BUY_SEED MELON` colma il deficit tra semi disponibili e tutte le 25 tile NW, senza riserva aggiuntiva, rispettando il capitale disponibile;
- `SELL` vende tutte le unità crop presenti nello shed;
- `HIRE` riporta la workforce al target co-scalato con il footprint (Sezione 14), non più un valore fisso; `SELL`, `HIRE` e `BUY_SEED` sono troncati a dieci ordini, senza ordini speculativi;
- `BUY_LAND` è implementato (`_next_land_cost()`, ladder NW->NE->SW->SE a 1000/2000/4000) ma **disabilitato per default** (`enable_land_expansion=False`, E-C2-PERF-06): il grid search del PERFORMANCE_CORRECTION pass ha mostrato che, con l'economia crop attuale e l'orizzonte di 29 giorni, il capitale investito in nuova terra non genera abbastanza throughput raccolto/venduto da compensare il costo, in ogni combinazione testata di `target_tiles_per_worker` e `last_land_purchase_day`. La feature resta disponibile e gated a `current_day <= last_land_purchase_day=11` per un eventuale utilizzo futuro con un'economia diversa, ma non è adottata in questa configurazione;
- non sono introdotti market timing speculativo o livestock.

## 16. Livestock policy

Non usata in questa versione C2. `UNCHANGED` / `DEFERRED` per ridurre la superficie del modello e rispettare il principio di Minimal Causal Intervention.

PERFORMANCE_CORRECTION (E-C2-PERF-07): il livestock (es. `BUY_ANIMAL COW`, shed
pasture) è stato esplicitamente rivalutato durante il performance correction
pass del `KAGGRICULTURE_C2_COPILOT_PERFORMANCE_CORRECTION_PROMPT.md`, come
richiesto dalla Sezione 9 del prompt. La valutazione di fattibilità (costo
COW ~400, necessità di una sequenza `PLACE`/`build_pasture` non presente
nella policy attuale) ha concluso che l'implementazione di un modulo
livestock completo eccede il time-budget della sessione di correzione e
introdurrebbe complessità di stato/azione non ancora validata contro
l'engine reale. Coerentemente con l'istruzione di NON introdurre un
meccanismo se il suo effetto atteso non è verificabile come positivo entro
lo scope della sessione, il livestock resta `DEFERRED`: questa è una
decisione esplicita basata su evidenza (vincolo di tempo/scope), non
un'omissione silenziosa.

## 17. Failure containment

La policy contiene i fallimenti principali:

- missing/invalid diagnostic data -> default conservative PASS;
- temporarily unavailable feature -> fallback to `PASS` or strict rejection;
- insufficient workforce -> no speculative over-allocation;
- insufficient cash -> acquisto semi limitato alla quantità finanziabile, senza espansione forzata;
- insufficient seed -> bootstrap `BUY_SEED` per le tile vuote del core;
- LOST_WEED -> DIG;
- nessun fallback silenzioso per un errore di runtime: il preflight real-engine P0/P1 è requisito di freeze.

## 18. Expected mechanism changes

```text
EVIDENZA
    ↓
premature HARVEST + WEED persistence
    ↓
feature `harvest_ready` + lifecycle classifier
    + bootstrap seed + bounded routing + crop sales
    ↓
strict action gate + preventive DIG + productive loop
    ↓
25-tile serviceable mass + nine-worker throughput
    ↓
higher maintained and monetized output
    ↓
higher economic capacity
```

## 19. Previsioni preregistrate

```text
EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: > 23000

METRIC_A: active_surface / workforce
CURRENT_VALUE: active max 4, workforce max 1
EXPECTED_VALUE_OR_DIRECTION: >=20 active tile e >=9 workforce nel preflight
WHY_CAUSAL: H1 aumenta soltanto la capacità che può essere servita e monetizzata.

METRIC_B: WATER / HARVEST / SELL state-transition effects
CURRENT_VALUE: ciclo corretto ma throughput di quattro tile
EXPECTED_VALUE_OR_DIRECTION: effect osservabili su working set >=20 in P0 e P1
WHY_CAUSAL: dimostra che la massa aggiunta è serviceable e non sola superficie.
```

## 20. Metriche di verifica

- `final_money`
- `completion`
- `crop_target_attainment`
- `active_crop_surface`
- `maintained_productive_surface`
- `watering_execution`
- `watering_continuity`
- `premature_harvest_count`
- `failed_action_count`
- `no_op_action_count`
- `WEED/lost_tile_count`
- `lost_tile_persistence`
- `replant_latency`
- `movement_share`
- `productive_action_share`
- `workforce_utilization`
- `inventory state`
- `market activity`

Se una metrica non è computabile nel runner comune, la documentazione indica `NOT_CURRENTLY_COMPUTABLE`.

## 21. Assunzioni e limiti

- il modello non pretende di ottimizzare il rendimento assoluto su tutte le seed, ma di ridurre il failure pattern stabilito;
- l'intervallo di validità è limitato alla Foundation C2 e ai suoi invarianti;
- il modello non introduce threshold non supportati senza evidenza; i parametri restano configurabili e dichiarati come policy envelope;
- questa versione non sostituisce il torneo comune e non si fonda su dati del concorrente avversario.

## 22. POST-TOURNAMENT REVIEW CONTRACT

Dopo il torneo locale a tre, il concorrente COPILOT riceverà i risultati di ANTIGRAVITY, CODEX e COPILOT e ripeterà la stessa domanda causale:

> Quali meccanismi hanno performato peggio, perché, quali decisioni del MODEL_SPEC li hanno causati e quali modifiche concrete possono migliorarli?

```text
RISULTATO
    ↓
MECCANISMO OSSERVATO
    ↓
DECISIONE MODEL_SPEC
    ↓
SPIEGAZIONE CAUSALE
    ↓
MODIFICA PROPOSTA
    ↓
PREVISIONE VERIFICABILE
```

Questo contratto garantisce che la vittoria non sia confusa con la correttezza del modello e che le correzioni future si basino sul dissenso empirico e non sul bias del proprio candidato.

## 23. Decision Lifecycle Mapping (Layer 5 conformance)

Questo MODEL_SPEC dichiara la propria discretizzazione locale del ciclo `DEFINE -> PLAN -> BUILD -> VERIFY -> REVIEW -> SHIP` sugli stati canonici del DLC frozen (`docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md`).

```text
DECISION_OPEN
    per-tile/per-turno: la policy acquisisce l'evidence snapshot dell'observation corrente
    (farms[player], private, market) e valuta il classificatore tile_lifecycle_state.

DEFINED
    intent_type in {HARVEST_INTENT, WATER_INTENT, DIG_INTENT, PLANT_INTENT,
                    MARKET_BOOTSTRAP_INTENT, MOVE_INTENT}
    intent_payload = (worker, target_tile, azione)

PLAN_FEASIBLE / INFEASIBLE / REJECTED
    feasibility_check_class = SNAPSHOT_ACTION_ELIGIBILITY
    FEASIBLE se: harvest_ready valida per HARVEST_INTENT; seed disponibile per
    PLANT_INTENT; deficit > 0 e capitale disponibile per MARKET_BOOTSTRAP_INTENT.
    INFEASIBLE se il predicato locale corrispondente è falso (fallback PASS, non
    fallimento silenzioso: la decisione ritorna a DECISION_OPEN nello stesso turno).

COMMITTED_EXECUTING
    scope = singola azione worker (o singolo batch market) per il turno corrente;
    declared_completion_condition = azione osservata come effetto post-stato
    (transizione tile/inventory/money) nel prossimo snapshot.

COMPLETED
    verificato se l'effetto atteso (es. watered_today diventa True, yield_units
    consumato, shed decrementato, money incrementato) è osservato nello snapshot
    successivo. Alimenta la telemetria di Sezione 20.

INVALIDATED
    la policy tratta come invalidator: harvest_ready diventa falso prima
    dell'esecuzione (crop rimosso/raccolto da altro worker nello stesso batch),
    o il seed/capitale dichiarato feasible al feasibility check non è più
    disponibile alla serializzazione (violazione ATOMIC_BATCH_FEASIBILITY).
    Fallback deterministico: nessun repair locale dichiarato per questa versione,
    quindi in caso di conflitto COMPLETION/INVALIDATION si applica il fallback
    del DLC (`INVALIDATED`).

REPAIR_WITHIN_COMMITMENT
    NON dichiarato in questa versione: il MODEL_SPEC non introduce un repair
    locale distinto dal replan al turno successivo, per Minimal Causal
    Intervention. Ogni azione fallita torna a DECISION_OPEN via TERMINAL riga
    per riga (nessun oscillamento silenzioso: la ripianificazione avviene solo
    al turno successivo con nuovo evidence snapshot, mai a metà batch).

CANCELLED / SUPERSEDED
    NON usati esplicitamente: la policy non cancella un commitment già assunto
    nello stesso turno; ogni azione, una volta serializzata, è eseguita fino a
    COMPLETED o INVALIDATED.

REVIEW_READY -> DECISION_OPEN
    ad ogni turno la policy chiude il micro-ciclo con un record osservabile
    (azione emessa, esito atteso) e riapre DECISION_OPEN al turno successivo,
    fino al TERMINAL_CLOSED di fine episodio (step + 1 >= max_steps).

TERMINAL_CLOSED
    forzato dal confine episodico comune; nessun nuovo intent viene aperto oltre
    l'ultimo step osservabile.
```

Non-oscillazione: la policy non effettua replan intra-turno silenzioso; ogni
decisione per worker è unica per turno e la sua validità è rivalutata solo al
turno successivo con evidence snapshot fresco (`NO_REPLAN_WITHOUT_LIFECYCLE_CAUSE`).

## 24. Registro delle revisioni

```text
REVISION: MODEL_SPEC_REVISION_BUILD (post Foundation freeze f391ee2)
DATA: 2026 (successiva a FOUNDATION_FINAL_FREEZE_REVIEW.md e
  DECISION_LIFECYCLE_TARGETED_FINAL_FREEZE_REVIEW.md)
MOTIVAZIONE: allineamento terminologico alla tassonomia canonica del Feature
  Model C2 frozen e aggiunta della Decision Lifecycle Mapping richiesta dal
  Layer 5 frozen.
MODIFICHE:
  - Sezione 9: `EMPTY_ASSIGNED` -> `EMPTY_AVAILABLE` (DERIVED_ENGINE_FACT);
    `RETIREMENT_DUE` sostituito da `GROWING` + overlay POLICY_CONTEXT
    `policy_retirement_due` (POL-RET), coerente con CORR-07 e con la
    risoluzione P1-01 della cross-review Foundation;
  - Sezioni 7, 13, 14: riferimenti terminologici aggiornati coerentemente;
  - Sezione 23 (nuova): Decision Lifecycle Mapping esplicito;
  - Sezione 24 (nuova): questo registro.
NON MODIFICATO: ipotesi causale (Sezione 4), regole HARVEST/WATER/PLANT/market
  bootstrap, priorità/arbitration, failure containment: nessuna evidenza
  disponibile in questo task giustifica una revisione della strategia oltre
  la conformità terminologica e la mappatura DLC.
```

```text
REVISION: COPILOT_PERFORMANCE_CORRECTION (post Foundation freeze f391ee2)
DATA: 2026 (successiva a KAGGRICULTURE_C2_COPILOT_PERFORMANCE_CORRECTION_PROMPT.md)
MOTIVAZIONE: il preflight tecnico a 288 step (revisione precedente) non
  copriva l'intero episodio da 720 step; una verifica economica full-episode
  ha rilevato PERFORMANCE_FAILURE (mean_final_money baseline = $9,422.67 su 3
  seed canonici, gate economico $50,000). Diagnosi quantitativa obbligatoria
  eseguita PRIMA di ogni modifica strategica, come richiesto dal prompt.
DIAGNOSI (evidenza, root cause):
  - E-C2-PERF-01: `HIRE` segue una curva costo Fibonacci-like PER-GIORNO
    (1,1,2,3,5,8,...) e le hand si resettano a 0 ogni giorno (day-laborer,
    non persistenti). Un target_workforce fisso indipendente dal footprint
    produceva o over-hiring costoso o idle rate elevato (~31% PASS nel
    baseline).
  - E-C2-PERF-02: `_working_positions()` era hardcoded a `x<=4 and y<=4`
    (quadrante NW), quindi il working set non cresceva mai anche quando
    `BUY_LAND` avrebbe sbloccato altra superficie; inoltre `market_orders()`
    non emetteva mai `BUY_LAND`.
  - E-C2-PERF-03: analisi economica su tutti i 5 crop disponibili (WHEAT,
    CARROT, TOMATO, STRAWBERRY, MELON) a parità di configurazione ha mostrato
    MELON dominante ($26,184 iniziale vs $10,640 di WHEAT, land expansion
    disattivata), nonostante il seed cost più alto (80) e il ciclo più lungo
    (first_yield_day=10 vs 2).
  - E-C2-PERF-04: grid search su `last_plant_day` specifico per MELON ha
    determinato day=11 come ottimo (day=10 prematuro, day>=12 nessun
    guadagno aggiuntivo), sostituendo il cutoff generico 27 tarato su WHEAT.
  - E-C2-PERF-05: `seed_reserve=0` risultato ottimo dopo grid search
    (0,1,2,4,8): nessuna riserva di semi extra migliora il risultato dato il
    cutoff di piantagione già stretto.
  - E-C2-PERF-06: espansione fondiaria (`BUY_LAND`) testata con grid search
    su `target_tiles_per_worker` e `last_land_purchase_day`: ogni
    configurazione con espansione attiva ha ottenuto un risultato inferiore
    alla configurazione statica a 25 tile NW, dato l'orizzonte di 29 giorni e
    il ciclo lungo di MELON. Implementata ma disattivata per default con
    evidenza documentata (non e' un limite di scope, e' una scelta basata sui
    dati).
  - E-C2-PERF-07: livestock rivalutato esplicitamente (Sezione 9 del prompt)
    e mantenuto DEFERRED per vincolo di tempo/scope, non per assunzione aprioristica
    che sia negativo (Sezione 16).
MODIFICHE:
  - `c2_config.py`: `default_crop`/`replant_preferred_crop` WHEAT->MELON;
    `seed_reserve` 2->0; `last_plant_day` 27->11; aggiunti
    `enable_land_expansion` (default False), `land_expansion_reserve`,
    `max_quadrants`, `last_land_purchase_day=11`,
    `target_tiles_per_worker=6.0`, `min_workforce=2`; `target_workforce=9`
    ridefinito semanticamente da target fisso a tetto massimo.
  - `c2_policy.py`: `_working_positions()` non piu' limitato al quadrante NW;
    aggiunti `_quadrants_owned()`, `_LAND_PRICE_LADDER`, `_next_land_cost()`,
    `_target_workforce(active_tile_count)`; `market_orders()` ora accetta
    `current_day` e emette `BUY_LAND` solo se `enable_land_expansion` e
    entro `last_land_purchase_day`; `decide()` propaga `current_day`
    dall'osservazione.
  - Sezioni 12, 14, 15, 16: aggiornate per riflettere crop MELON, workforce
    co-scaling, land expansion disattivata con evidenza, livestock DEFERRED
    con evidenza esplicita.
  - `tests/test_copilot_c2.py`: assertion aggiornate per MELON e per il
    conteggio HIRE derivato dal footprint (non piu' fisso a 8).
RISULTATO (720 step, 3 seed canonici, P0 e P1):
  mean_final_money = $28,909.00 (median $28,909.00, stdev(ddof=1) = 0.0,
  deterministico su tutti i 6 run), rispetto al baseline $9,422.67
  (+206.8%). Classificazione secondo il gate del prompt: mean < $50,000 =>
  ancora PERFORMANCE_FAILURE in senso stretto, nonostante il miglioramento
  di ~3x. Riportato onestamente senza riclassificazione opportunistica.
NON MODIFICATO: Foundation (f391ee2), TOURNAMENT_AUTHORIZED=NO,
  KAGGLE_AUTHORIZED=NO, nessun artefatto Antigravity/Codex toccato.
```
