# MODEL_SPEC CODEX C2 â€” Periodic capacity scheduler V5

```text
AGENT_ID: CODEX
BUILD_ID: CODEX-C2-PERIODIC-CAPACITY-SCHEDULER-V5
STATUS: DEFINE FROZEN / READY FOR PLAN-BUILD / NOT IMPLEMENTED
HYPOTHESIS_ID: CODEX-C2-PERIODIC-CAPACITY-SCHEDULER-V5
BASELINE_IMPLEMENTATION: CODEX-C2-STAGGERED-HARVEST-SERVICE-V4
TOURNAMENT_READY: NO
TOURNAMENT_EXECUTED: NO
```

## 1. Tesi causale

La V4 ha confermato che una coorte WHEAT sincronizzata puÃ² superare la capacitÃ
di servizio e che lo staggering elimina il deadline miss. Il cap fisso di due
PLANT al giorno risolve quel caso, ma rappresenta soltanto la capacitÃ  osservata
nel preflight V3.2. Non descrive la domanda futura di WATER, HARVEST, FEED, CARE,
collection, routing e inventory, nÃ© scala con workforce, mix o superficie.

La V5 generalizza il meccanismo:

```text
plant / place candidate
  -> derive complete biological service profile
  -> reserve slots in every future service window
  -> admit only if the profile is serviceable
  -> execute a planned route before urgency
  -> verify every completion from the next snapshot
  -> use reactive overrides only for real deviations
```

Tesi:

```text
PLANNED_BASELINE
  = biological cycles
  + entity service calendar
  + capacity reservation
  + phase-shifted cohorts
  + planned routing and workforce
  + controlled expansion sequence

REACTIVE_OVERRIDE
  = legality
  + price / market inventory
  + cash / feed shortage
  + missed service / weed / worker loss
  + sell opportunity
  + terminal horizon
```

Un periodo non autorizza mai un'azione illegale. Una soglia di stato non deve
piÃ¹ essere il solo meccanismo che scopre un task biologico prevedibile.

## 2. Evidenza congelata

Baseline V4, seed neutrale `26083001`, P0/P1:

- cap WHEAT massimo 2 PLANT/day;
- peak economic-ready 2;
- deadline miss 0/15;
- 15/15 HARVEST WHEAT a yield almeno 3;
- ciclo MELON con HARVEST e SELL effettivi;
- zero error/fallback.

Replay esterni usati come evidenza comparativa, non come tuning:

| Policy | Score | Scala | Periodi principali | Segnale di capacitÃ  |
|---|---:|---|---|---|
| LuCcc | 56.772 | 1Q, max 25 entitÃ  produttive | service 24; COW 48; SHEEP 72; WHEAT circa 96 | 100/100 HARVEST effettivi, MOVE 30,29% |
| Gordeev | 88.648 | 3Q, max 62 entitÃ  | 24/48/72 conservati con crop piÃ¹ irregolari | 238/238 HARVEST effettivi |
| Dipin | 95.496 | 3Q, max 72 entitÃ  | 24/48/72, WHEAT spesso age 3 | 284/285 HARVEST effettivi |
| Petar | 95.475 | 4Q, 22 SHEEP | CARE 24, collection circa 72 | 197/389 HARVEST effettivi; 192 no-op |

L'evidenza supporta il calendario biologico e l'espansione condizionale. Non
supporta un mix unico, un target di Q, un harvest age universale o la copia di
una policy esterna.

## 3. Ontologia di capacitÃ

| Livello | Definizione V5 |
|---|---|
| `OWNED_SURFACE` | tile non-LOCKED nei quadranti acquistati |
| `ACTIVE_SURFACE` | entitÃ  PLANT o animal osservate |
| `SERVICEABLE_SURFACE` | entitÃ  le cui finestre fino al primo output monetizzabile hanno slot prenotati |
| `PRODUCTIVE_SURFACE` | entitÃ  con service completato e output raccolto entro deadline |
| `MONETIZED_OUTPUT` | output depositato e venduto con effetto osservato |

`ACTIVE_SURFACE` non puÃ² essere usata come sinonimo di capacitÃ . L'ammissione
lavora sul passaggio incrementale `candidate -> SERVICEABLE_SURFACE`.

## 4. Entity registry

Ogni asset biologico ha una singola entry persistente:

```text
ENTITY_PERIOD_MODEL
  entity_id
  tile
  kind
  phase
  origin_step
  nominal_period
  next_due_step
  service_window_open
  service_window_target
  service_window_close
  hard_deadline
  expected_output
  required_worker_slots
  route_cluster
  inventory_requirement
  completion_evidence
  deviation_state
  reactive_overrides
```

L'entry deriva dallo snapshot e viene riconciliata a ogni decisione. Una
prenotazione non sostituisce lo stato engine. Se posizione, kind o phase non
sono riconciliabili, l'entitÃ  entra in `DEVIATION_REPLAN_REQUIRED` e non genera
azioni speculative.

## 5. Modelli di periodo candidati

I valori esterni sono candidate windows. Prima del BUILD devono essere
riconciliati con la Foundation e i metadata engine; l'evidenza insufficiente non
crea una nuova costante.

### 5.1 Crop

| Crop | Piano nominale | Window / deadline | Output osservato | Nota V5 |
|---|---|---|---|---|
| WHEAT | WATER giornaliero; harvest mode preregistrato per coorte | legalitÃ  da first-yield; target V4 full-yield age 4; deadline da `max_lifespan_step` | age 2â€“4, yield 1â€“6; LuCcc yield 3 stabile ad age 4 | il numero di PLANT deriva dalle reservation, non da cap 2 |
| MELON | WATER giornaliero; ciclo candidato 10â€“12 day | harvest nella window prenotata, replant dopo completion | yield 6 frequente | non aprire un ciclo oltre horizon |
| STRAWBERRY | WATER giornaliero; collection candidata ogni 48 step | output ricorrente circa age 10/12/14/16; hard deadline da lifespan | yield 1â€“2 frequente | mantenere tile ongoing finchÃ© serviceable |
| CARROT | Foundation-defined | nessuna nuova window numerica congelata | evidenza age 2â€“3 limitata | fallback ai metadata engine |
| TOMATO | Foundation-defined | nessuna nuova window numerica congelata | evidenza insufficiente | fallback ai metadata engine |

Il `harvest_mode` WHEAT distingue almeno:

```text
FULL_YIELD
  target = policy economic target V4
  role = monetized crop

FAST_TURN
  target = earlier legal window, only after independent validation
  role = feed / liquidity / horizon-constrained cohort
```

La modalitÃ  Ã¨ scelta prima della PLANT usando ruolo previsto, horizon, capacitÃ
e output per slot. Non oscilla per una singola variazione di prezzo.

### 5.2 Animal

| Animal | FEED | CARE | Production / collection candidate | Output tipico osservato | Deadline |
|---|---:|---:|---:|---|---|
| COW | 24 step | 24 step | circa 48 step | MILK 3, bonus fino a 6 | service entro il day; collect prima del successivo ciclo compatibile |
| SHEEP | 24 step | 24 step | circa 72 step | WOOL 4, bonus variabile | service entro il day; collect prima del successivo ciclo compatibile |

Placement richiede reservation per FEED, CARE, collection, fertilizer handling,
feed inventory e route fino al primo output monetizzabile. Livestock Ã¨ un modulo
opzionale, non un requisito V5.

### 5.3 Fertilizer e inventory

FERTILIZER usa uno sweep candidato giornaliero, accorpato alla route animal,
soltanto quando la disponibilitÃ  Ã¨ osservata. DROP, market sell e liberazione
dell'inventory hanno slot espliciti: un harvest biologico non Ã¨ serviceable se
non puÃ² completare handling e monetization.

## 6. Rolling service calendar

Per ogni finestra `w`:

```text
required_slots(w)
  = crop_water_due(w)
  + crop_harvest_due(w)
  + animal_feed_due(w)
  + animal_care_due(w)
  + product_collect_due(w)
  + fertilizer_due(w)
  + inventory_handling_due(w)
  + route_allowance(w)

available_slots(w)
  = contracted_worker_actions(w)
  - mandatory_transit_reserve(w)
  - exception_reserve(w)

reservation_slack(w)
  = available_slots(w) - required_slots(w)
```

Regola di ammissione:

```text
ADMIT(entity)
  iff legal_to_create(entity)
  and affordable(entity)
  and horizon_complete(entity)
  and for every required service window w:
        reservation_slack_after_admission(w) >= 0
```

La reservation copre almeno il primo ciclo monetizzabile. Per asset ongoing
copre anche una rolling window successiva. Un task completato libera la sua
prenotazione; un task mancato consuma `exception_reserve` e forza replan.

## 7. Staggering V5

La V4:

```text
MAX_WHEAT_PLANTS_PER_DAY = 2
```

La V5:

```text
MAX_NEW_ENTITIES_IN_WINDOW
  = count of candidate profiles that fit all future reservations
```

Il cap `2` non Ã¨ una costante universale V5. PuÃ² restare soltanto come safety
fallback iniziale se il calendario Ã¨ invalido. Lo staggering sceglie phase
offset che minimizzano il futuro `SERVICE_PEAK`, con questi vincoli:

1. nessuna concentrazione di HARVEST/COLLECT oltre `available_slots`;
2. WATER/FEED/CARE hard service protetti prima dei task differibili;
3. route cluster coerente con le finestre;
4. completion dello snapshot precedente prima di replant/reuse;
5. nessuna PLANT aggiunta soltanto per raggiungere un raw target.

## 8. PLANNED_BASELINE

Ordine di costruzione del piano:

1. riconciliare entity registry e completion;
2. materializzare eventi nominali nella rolling window;
3. caricare hard deadlines e servizi giornalieri;
4. allocare worker e route cluster;
5. allocare handling e sell-through minimo;
6. valutare nuove PLANT, animal placement, HIRE ed espansione;
7. scegliere phase offset delle nuove entitÃ ;
8. emettere azioni due-safe e verificabili;
9. confrontare piano ed effetti allo snapshot successivo.

La workforce non Ã¨ `5/8` come tesi causale. Il planner calcola worker-window
necessari dal carico e ammette HIRE soltanto se:

- aumenta `available_slots` in una finestra vincolante;
- il nuovo worker puÃ² raggiungere il cluster utile;
- wage e horizon conservano il cash floor;
- la capacitÃ  aggiunta Ã¨ utilizzata da output monetizzabile.

## 9. REACTIVE_OVERRIDE

Precedenza:

1. engine legality e own-player binding;
2. imminente hard-deadline miss;
3. feed/cash/inventory impossibility;
4. missed WATER/FEED/CARE o weed su tile produttiva;
5. worker contract loss / route obstruction;
6. market price, inventory/demand e cash opportunity;
7. terminal shutdown/liquidation;
8. ritorno al baseline replanned.

Un override:

- modifica il minimo numero di eventi;
- conserva le altre reservation;
- registra causa, evento spostato e nuova deadline;
- non ripete un'azione senza transition evidence;
- non usa prezzo o urgenza per bypassare la legalitÃ .

## 10. Market model

Il mercato resta `REACT` dominante:

```text
SELL_DECISION
  = observed_sellable_inventory
  + price / inventory condition
  + cash need
  + max_holding_window
  + terminal horizon
```

Il piano fornisce output previsto, earliest sell step, max holding window e slot
di handling. Il market override sceglie quantitÃ  e timing. Una vendita Ã¨
`MONETIZED_OUTPUT` soltanto dopo effetto osservato; un ordine emesso non Ã¨
revenue.

## 11. Espansione

L'espansione Ã¨ una replica controllata del ciclo, non un `BUY_LAND` isolato:

```text
Q1 stable serviceable cycle
  -> shadow schedule Q2 with phase offset
  -> reserve workforce / route / cash / sell-through
  -> activate Q2 progressively
  -> reconcile predicted vs actual load
  -> optional Q3/Q4 by the same gate
```

`EXPANSION_ADMIT(Qn)` richiede:

- nessun hard-deadline miss persistente nel ciclo corrente;
- output giÃ  passato da `ACTIVE` a `PRODUCTIVE` e `MONETIZED`;
- reservation non negativa fino al primo ciclo monetizzabile del clone;
- land, activation, seed/animal, wage e feed compatibili con cash floor;
- payback horizon plausibile;
- phase offset diverso dal Q precedente;
- stop automatico se serviceability o period adherence peggiorano.

Non esiste un quadrant target V5. Q1, Q2, Q3 e Q4 sono risultati condizionali.

## 12. Classificazione delle soglie V4

| Meccanismo | Decisione V5 |
|---|---|
| engine harvest legality | `KEEP_AS_THRESHOLD` |
| cash floor 300 | `KEEP_AS_THRESHOLD` fino a nuova validazione |
| WHEAT economic target | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| WATER loss boundary | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| product yield availability | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| market price/inventory | `HYBRID_PERIOD_PLUS_THRESHOLD` con REACT dominante |
| `MAX_WHEAT_PLANTS_PER_DAY=2` | `CONVERT_TO_PERIOD` / capacity reservations |
| FEED e CARE non-serviti oggi | `CONVERT_TO_PERIOD` con state guard |
| replant su tile libera | `CONVERT_TO_PERIOD` con completion guard |
| workforce 5/8 | `CONVERT_TO_PERIOD` / window workload |
| pasture/COW cap 5/4 | `CONVERT_TO_PERIOD` / asset service profile |
| crop target e mix | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| land e livestock gate | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| fixed quadrant target | `REMOVE` |
| retry senza transizione | `REMOVE` |

## 13. Arbitration V5

```text
1. legality / SAFE_PASS
2. hard-deadline rescue
3. planned service whose window closes now
4. missed-service recovery
5. planned service at target step
6. route-compatible early service within window
7. inventory handling required by a due harvest/collect
8. market override with protected biological reservations
9. planned PLANT / PLACE admitted by reservations
10. planned HIRE / expansion admitted by capacity and cash
11. PASS
```

Tra task dello stesso livello: earliest deadline, poi lowest slack, poi route
cost, poi stable entity id. Questo evita oscillazioni threshold-centric.

## 14. Consumer mapping

| Feature | Consumer | Fallback |
|---|---|---|
| day/hour/step, origin step | phase clock e due events | nessuna nuova entitÃ  se clock invalido |
| crop/animal metadata | period profile e legality | Foundation-only profile |
| yield/lifespan/service flags | completion, deadline, override | task bloccato se ambiguo |
| worker position/contract | available slots e route | capacitÃ  non prenotabile |
| inventories/shed | handling, feed e sell-through | proteggere service, nessuna vendita presunta |
| money e market | affordability e REACT | cash floor / nessun ordine speculativo |
| tile transition | completion evidence | evento resta unresolved, no retry spam |
| unlocked quadrants | owned surface / expansion | nessuna inferenza da BUY_LAND order |

Own-player binding, factory isolata, due-safe action generation e SAFE_PASS
restano invarianti della Foundation.

## 15. Previsioni e falsificazione

Direzioni preregistrate rispetto alla V4, a paritÃ  di bundle e protocollo:

```text
SERVICEABLE_TO_ACTIVE_RATIO: UP_OR_EQUAL
HARD_DEADLINE_MISS_RATE: DOWN_OR_EQUAL
NOOP_ACTION_RATE: DOWN
MONETIZED_OUTPUT_PER_WORKER_ACTION: UP
SERVICE_PEAK_OVER_CAPACITY: DOWN
PERIOD_ADHERENCE_AFTER_Q2: PRESERVED
FINAL_MONEY: UP_DIRECTIONAL, NO EXTERNAL-SCORE TARGET
```

Il modello Ã¨ falsificato se:

- non migliora completion/monetized output rispetto a V4 su episodi
  indipendenti;
- aumenta deadline miss, cash failure o no-op;
- non conserva period adherence dopo un clone Q2;
- reservation forecast non predice il carico reale meglio dei raw count;
- il dispatcher V4 eguaglia sistematicamente l'economia con complessitÃ  minore.

La validazione deve separare calendario, mix, workforce, land e market. Nessuno
score dei quattro replay Ã¨ un target di tuning.

## 16. Contratto per la fase successiva

Prima del BUILD:

1. riconciliare tutti i periodi candidati con la Foundation engine;
2. definire rolling horizon e unitÃ  di `route_allowance` senza score tuning;
3. preregistrare baseline V4, metriche e falsification gates;
4. implementare telemetry di due/completed/missed/reserved slots;
5. costruire il planner dietro mode isolata;
6. verificare P0/P1 e completion effects;
7. solo dopo, eseguire il protocollo autorizzato.

In questa fase non sono autorizzati codice, config, test, runner, tournament,
Kaggle o submission.

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
IMPLEMENTATION_STATUS: NOT_STARTED
TOURNAMENT_READY: NO
```
