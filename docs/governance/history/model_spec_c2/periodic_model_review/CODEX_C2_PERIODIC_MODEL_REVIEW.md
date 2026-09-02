# CODEX C2 â€” Periodic model review

```text
AGENT: CODEX
REVIEW_ID: CODEX-C2-PERIODIC-CAPACITY-REVIEW
PHASE: DEFINE / REVIEW
IMPLEMENTATION_CHANGED: NO
KAGGLE_RUN: NO
TOURNAMENT_RUN: NO
INDEPENDENT_FREEZE: YES
```

## 1. Esito

La formulazione iniziale Ã¨ supportata con una correzione importante:

```text
BASE POLICY = PLAN
MARKET CONDITION = REACT
OPERATIONAL DEVIATION = REACT
LEGALITY / LIQUIDITY = HARD OVERRIDE
```

Il MODEL_SPEC Codex V4 Ã¨ giÃ  parzialmente period-centric: lo staggering WHEAT
serve a distribuire nel tempo un carico biologico futuro. Rimane perÃ²
threshold-centric nell'ammissione del lavoro (`MAX_WHEAT_PLANTS_PER_DAY=2`),
nell'espansione, nella scala della workforce e nell'attivazione livestock. Il
numero `2` Ã¨ un proxy statico della capacitÃ  osservata, non un modello della
capacitÃ  futura.

I quattro replay mostrano che i periodi stabili non appartengono a una sola
architettura: compaiono nel Q1 denso di LuCcc, nelle farm 3Q miste di Gordeev e
Dipin e nella farm 4Q sheep-dominant di Petar. La conclusione non Ã¨ Â«copiare un
mixÂ», ma sostituire la generazione tardiva di task con un calendario per entitÃ
e prenotare la capacitÃ  prima di piantare, collocare animali o espandere.

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
```

## 2. Metodo e limiti

Fonti primarie lette indipendentemente:

- `data/replays/reference/103484828.json` â€” LuCcc;
- `data/replays/reference/103473619.json` â€” Gordeev;
- `data/replays/reference/103462357.json` â€” Dipin;
- `data/replays/reference/103464592.json` â€” Petar;
- `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md` â€” baseline Codex V4.

Le azioni sono state allineate alla transizione osservata tra snapshot
consecutivi. Un evento Ã¨ contato come effettivo soltanto se la tile o
l'inventario di produzione cambia coerentemente. I periodi sono intervalli per
entitÃ /posizione, non semplici distanze tra conteggi aggregati. Le quantitÃ  di
vendita sono ordini supportati da disponibilitÃ  osservata nello shed; non sono
una contabilitÃ  causale completa di profitto.

Quattro replay osservazionali non isolano prezzi, seed, avversario, capitale,
layout o implementation. Le regolaritÃ  sono quindi candidate strutturali e
condizioni di falsificazione, non parametri ottimizzati sugli score.

## 3. Evidenza comparativa

### 3.1 Architettura osservata

`Workforce` include il farmer. `Productive` Ã¨ `PLANT + pasture con animale`.

| Replay | Score | Q max / unlock | Active crop mean / max | Animal mean / max | Productive mean / max | Workforce mean / max | MOVE share |
|---|---:|---|---:|---:|---:|---:|---:|
| LuCcc | 56.772 | 1 / nessun acquisto | 13,97 / 19 | 5,42 / 6 | 19,39 / 25 | 6,65 / 7 | 30,29% |
| Gordeev | 88.648 | 3 / day 0, 11 | 33,41 / 52 | 7,63 / 10 | 41,04 / 62 | 8,21 / 13 | 58,22% |
| Dipin | 95.496 | 3 / day 6, 10 | 35,30 / 60 | 9,67 / 12 | 44,96 / 72 | 11,55 / 15 | 59,63% |
| Petar | 95.475 | 4 / day 9, 10, 12 | 10,30 / 29 | 13,99 / 22 | 24,29 / 51 | 8,20 / 19 | 50,90% |

La scala alza il ceiling osservato, ma non in modo uniforme: Petar compra 4Q e
li usa soprattutto per 22 sheep; Gordeev e Dipin mantengono superfici crop molto
piÃ¹ grandi. `OWNED_SURFACE` non predice da sola `MONETIZED_OUTPUT`.

### 3.2 Replay 103484828 â€” LuCcc, Q1 temporalmente denso

Architettura:

- un solo quadrante, 25 tile produttive al picco;
- 19 crop al picco, 3 COW e 3 SHEEP;
- massimo 7 worker inclusivo del farmer;
- 1.449 MOVE, soltanto 30,29% delle azioni worker;
- 100 richieste HARVEST, 100 transizioni effettive;
- cash minimo 9, prima crescita osservata allo step 25, massimo 57.444 e finale
  56.772.

Periodi crop:

| Crop | PLANT / staggering | WATER | HARVEST | Yield | Replant / ciclo |
|---|---|---|---|---|---|
| WHEAT | una tile ai day 0, 4, 8, 12, 16, 20, 24, 28 | mediana 24 step | tutte le 7 completion ad age 4; intervallo per tile 94â€“99, mediana 96 | 3 sempre | ciclo di circa 4 day; coorte massima 1 |
| MELON | 10 tile day 7; poi 9 day 19 e 1 day 20 | mediana 24 | 10 completion ad age 12 | 6 sempre | replant quasi immediato; ciclo circa 12 day |
| STRAWBERRY | 3 tile day 7 + 5 day 9; replica day 24/26 | mediana 24 | age 10, 12, 14, 16; intervallo per tile mediano 47,5 | 28/32 a yield 2, 4 a yield 1 | ciclo produttivo ricorrente di circa 48 step |

Periodi animal:

| Animal | Placement | FEED | CARE | Collection | Output osservato |
|---|---|---|---|---|---|
| COW | step 7, 7, 183 | mediana 24 | mediana 24 | mediana 48, quasi senza jitter | 26/29 raccolte da 3, 3 da 6 |
| SHEEP | step 15, 21, 188 | mediana 24 | mediana 24 | mediana 72 | 19/22 raccolte da 4, 3 da 6 |

Monetizzazione osservata:

- WHEAT 553, MILK 96, WOOL 92, STRAWBERRY 60, MELON 60 e FERTILIZER 22
  unitÃ  ordinate in vendita con disponibilitÃ ;
- STRAWBERRY Ã¨ venduta ogni 48 step in tutti i quattro intervalli osservati;
- MILK ha mediana 24 step tra vendite; 14/17 intervalli sono 24;
- FERTILIZER ha mediana 24; WHEAT Ã¨ prevalentemente giornaliera con coppie di
  ordini ravvicinati; MELON Ã¨ liquidato in un batch;
- 433 WATER, 160 FEED, 160 CARE e 100 HARVEST effettivi equivalgono a circa
  1,47 servizi biologici per entity-day sulla superficie produttiva media,
  prima di fertilizzazione e handling.

Interpretazione: gran parte del rendimento Q1 Ã¨ spiegabile da un calendario
compatto 24/48/72/96, staggering WHEAT e routing ridotto. Non Ã¨ prova che Q1
sia economicamente ottimo: gli score 88â€“95k mostrano un ceiling superiore con
scala. Ãˆ prova che una superficie piccola puÃ² arrivare al 100% di efficacia
HARVEST e saturare tutte le 25 tile senza un dispatcher principalmente
reattivo.

### 3.3 Replay 103473619 â€” Gordeev, 3Q misto

Architettura e monetizzazione:

- secondo Q dal day 0, terzo Q al day 11; 52 crop e 10 animali al picco;
- mix crop massimo: WHEAT 30, STRAWBERRY 26, MELON 9, CARROT 9, TOMATO 2;
- 6 COW e 4 SHEEP al picco;
- 238 HARVEST richiesti e 238 effettivi;
- vendite supportate osservate: WHEAT 244, MILK 134, FERTILIZER 132,
  STRAWBERRY 79, WOOL 52, MELON 38.

PeriodicitÃ :

- FEED COW mediana 24 e CARE 24; collection COW mediana 48;
- FEED SHEEP mediana 24, CARE 25; collection SHEEP mediana 71,5;
- STRAWBERRY: 66 raccolte, age concentrate a 10/12/14/16, intervallo per tile
  mediano 47;
- MELON: 9/10 raccolte ad age 10, una ad age 11, yield 4â€“6;
- WHEAT: 151 plant distribuite su 26 day, coorte massima 14, raccolta age 2â€“4
  e yield 2â€“6; il periodo biologico resta visibile ma l'ammissione Ã¨ molto piÃ¹
  elastica di LuCcc;
- WATER Ã¨ piÃ¹ irregolare (mediana per tile 37 step WHEAT e 41 STRAWBERRY).

Anomalie: gli ordini `BUY_LAND` ripetuti non rappresentano acquisti ripetuti;
le transizioni reali sono due. La cadence delle vendite Ã¨ piÃ¹ irregolare e
price-sensitive di LuCcc. Il replay sostiene un baseline periodico per gli
asset, non un calendario rigido per il mercato.

### 3.4 Replay 103462357 â€” Dipin, 3Q ad alta capacitÃ

Architettura e monetizzazione:

- Q2 al day 6 e Q3 al day 10;
- 60 crop, 12 animali e 72 entitÃ  produttive al picco;
- 8 COW e 4 SHEEP;
- 285 HARVEST richiesti, 284 effettivi e un solo no-op;
- vendite supportate: WHEAT 447, MILK 201, STRAWBERRY 180, FERTILIZER 173,
  WOOL 114, MELON 109.

PeriodicitÃ :

- FEED/CARE COW mediane 24; collection COW mediana 48;
- FEED/CARE SHEEP mediane 24; collection SHEEP mediana 72,5;
- MELON: 20 plant, incluse coorti da 8 e 10; 18/19 harvest a yield 6, age
  prevalentemente 10;
- STRAWBERRY: 26/32 plant nei day 11â€“12; 97 harvest, ciclo per tile mediano 47
  e yield prevalentemente 2;
- WHEAT: 109 plant, coorte massima 10, 67/81 harvest ad age 3, yield
  prevalentemente 2; Ã¨ un ciclo rapido differente dal full-yield age 4 di
  LuCcc;
- mediana replant effettivo 1 step, ma con una coda lunga di tile riutilizzate
  tardi.

Le vendite sono micro-batch frequenti: mediane tra ordini di 3,5 step WHEAT,
5 MILK, 3 STRAWBERRY e 3 FERTILIZER. La biologia resta periodica, mentre la
monetizzazione Ã¨ fortemente reattiva.

### 3.5 Replay 103464592 â€” Petar, 4Q sheep-dominant

Architettura e monetizzazione:

- Q2/Q3/Q4 ai day 9/10/12;
- 22 pasture con 22 SHEEP, nessun altro animale;
- soltanto 10,30 crop attive in media, contro 13,99 animali;
- 389 richieste HARVEST, 197 effetti e 192 no-op: lo score alto non implica
  dispatch pulito;
- 106 raccolte SHEEP; vendite supportate WOOL 377 e FERTILIZER 330 dominano,
  seguite da WHEAT 92 e MELON 72.

PeriodicitÃ :

- CARE SHEEP mediana 24; FEED mediana 25 con piÃ¹ jitter;
- collection SHEEP mediana 71, output piÃ¹ spesso 4;
- MELON: 12/12 harvest effettivi ad age 10 e yield 6;
- STRAWBERRY: tre tile, harvest age 10/12/14/16;
- WHEAT: 65/66 harvest ad age 2, yield 1â€“3; l'agente privilegia turnover e
  feed/liquiditÃ  rispetto al target Codex age 4;
- WOOL e FERTILIZER sono venduti spesso a cadence giornaliera, ma con batch
  reattivi intermedi.

Anomalia principale: metÃ  circa delle richieste HARVEST Ã¨ inefficace, in larga
parte per tentativi prematuri o sulla tile sbagliata. Questo replay supporta la
profittabilitÃ  potenziale di un modulo periodico livestock su larga scala, ma
anche la necessitÃ  di conservare legality predicates e verifica della
transizione. Non Ã¨ una policy da copiare.

## 4. Diagnosi del modello Codex V4

### 4.1 Parti giÃ  periodiche

- il cap di coorte WHEAT nasce per appiattire un `SERVICE_PEAK` futuro;
- `day`, `planted_day`, crop age e `max_lifespan_step` definiscono finestre;
- WATER ha una loss-boundary EOD;
- lo stato `HARVEST_SERVICE_PENDING` persiste fino alla completion;
- la distinzione `ACTIVE`, `SERVICEABLE`, `PRODUCTIVE`, `MONETIZED` Ã¨ giÃ  la
  base corretta per un capacity scheduler;
- il terminal horizon impedisce di aprire cicli che non possono completarsi.

### 4.2 Parti threshold-centric e collisioni

| Meccanismo corrente | Trigger / costante | Diagnosi | Classificazione |
|---|---|---|---|
| LegalitÃ  HARVEST | yield>0, age>=first yield | Vincolo engine, non sostituibile da timer | `KEEP_AS_THRESHOLD` |
| Readiness economica WHEAT | age>=4 e yield>=3 | Obiettivo di coorte; deve diventare una finestra prenotata, con soglia come guardia | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| Cap WHEAT | massimo 2 PLANT/day | Proxy statico della capacitÃ  V3.2; non scala con worker, route o Q | `CONVERT_TO_PERIOD` |
| Crop target | 10 bootstrap / 25 full | Count target privo del carico temporale futuro | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| Crop mix | 60/20/20, poi 40/20/40 | PuÃ² essere piano iniziale, non veritÃ  universale | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| WATER priority | loss imminente, accumulating, ordinary | Il bisogno nominale Ã¨ giornaliero; le soglie devono essere escalation | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| Replant | tile libera / task disponibile | Reazione dopo il fatto; nella maggioranza dei riusi rapidi il delay Ã¨ 1 | `CONVERT_TO_PERIOD` |
| FEED / CARE | stato odierno non servito | Ãˆ un ciclo nominale 24 step; lo stato resta guardia | `CONVERT_TO_PERIOD` |
| Product collection | yield disponibile | COW 48 e SHEEP circa 72 sono schedulabili; yield>0 resta legality guard | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| Workforce | 5 bootstrap / 8 full | Headcount fisso, non workload per finestra | `CONVERT_TO_PERIOD` |
| Land gate | active>=8 e cash>=1.600 | Non verifica calendario del clone nÃ© backlog futuro | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| Pasture/COW cap | 5 / 4 | Asset count separato da FEED/CARE/collect slots | `CONVERT_TO_PERIOD` |
| Livestock gate | active>=80% e cash>=1.500 | Readiness utile, ma incompleta senza period capacity | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| Cash floor | 300 | Protezione di liquiditÃ  in incertezza | `KEEP_AS_THRESHOLD` |
| Selling | inventory, prezzi, endgame | Il mercato Ã¨ incerto; serve anche una max holding window | `HYBRID_PERIOD_PLUS_THRESHOLD` |
| Retry senza transizione | task continua a essere emessa | Causa no-op come quelli visibili in Petar | `REMOVE` |
| Quadrant target implicito | massimo 2 nella V4 | Gli replay supportano Q1â€“Q4 condizionali, non un target fisso | `REMOVE` |

La collisione centrale Ã¨ questa:

```text
threshold opens task only when state becomes urgent
-> many entities cross together
-> routing and inventory work become simultaneous
-> fixed cap approximates yesterday's capacity
-> change of workforce / mix / land invalidates the approximation
```

Il periodo risolve la generazione anticipata del lavoro; la soglia resta
necessaria per legalitÃ , affordability e deviazioni.

## 5. Proposta architetturale

### 5.1 PLANNED_BASELINE + REACTIVE_OVERRIDE

```text
PLANNED_BASELINE
  entity registry
  -> biological phase clock
  -> rolling due-event calendar
  -> service-window reservations
  -> worker/route allocation
  -> plant/place/expansion admission
  -> completion verification

REACTIVE_OVERRIDE
  legality failure
  cash / feed shortage
  missed service or weed
  worker loss / route obstruction
  price and market inventory
  exceptional sell opportunity
  terminal horizon
```

| Meccanismo | PLAN | REACT | Classe finale |
|---|---|---|---|
| Plant cohort e staggering | calendario con slot futuri WATER/HARVEST | seed/cash/market cambia la prossima coorte | `PLAN` con override |
| WATER | servizio nominale ogni day | loss-boundary e recovery | `HYBRID` |
| HARVEST crop | finestra e deadline registrate alla PLANT | legality, decay risk, inventory blockage | `HYBRID` |
| Replant | evento `completion + nominal_delay` | cash, horizon, cambio mix | `HYBRID` |
| FEED / CARE | cadence 24 per animale | shortage e missed-service recovery | `HYBRID` |
| Collection | 48 COW / circa 72 SHEEP come candidate | yield osservato e storage | `HYBRID` |
| Workforce | turni derivati dal carico rolling | cash/contract loss | `HYBRID` |
| Routing | route batch per cluster e finestra | task urgente / worker deviato | `HYBRID` |
| Selling | max holding window e flush pianificato | prezzo, inventory, domanda, cash | `REACT` dominante |
| Expansion | replica sfasata di un ciclo serviceable | payback, cash, horizon | `HYBRID` |
| No-op retry | nessun ruolo | completion mismatch genera diagnosi, non spam | `REMOVE` |

### 5.2 CapacitÃ  prenotata

Per ogni finestra `w`:

```text
required_slots(w)
  = crop_water_due
  + crop_harvest_due
  + animal_feed_due
  + animal_care_due
  + product_collect_due
  + inventory_handling_due
  + route_allowance

available_slots(w)
  = contracted_worker_actions(w)
  - mandatory_transit_reserve(w)
  - safety_reserve(w)
```

Una nuova entitÃ  Ã¨ `SERVICEABLE` soltanto se tutte le sue finestre fino al
primo output monetizzabile possono essere prenotate. Il cap giornaliero non Ã¨
piÃ¹ `2`: Ã¨ il numero di nuove entitÃ  il cui profilo temporale entra nel
calendario. Un limite numerico puÃ² restare come safety fallback fino alla
validazione, non come tesi causale.

## 6. Ipotesi causale

```text
HYPOTHESIS_ID: CODEX-C2-PERIODIC-CAPACITY-SCHEDULER-V5
OBSERVED_PROBLEM: V4 elimina il primo service peak WHEAT con un cap statico,
  ma continua a generare gran parte del lavoro da soglie di stato e non puÃ²
  trasferire automaticamente quella capacitÃ  a mix, workforce o Q diversi.
EVIDENCE: LuCcc ottiene 56.772 su 1Q con 100/100 HARVEST effettivi e cicli
  24/48/72/96; Gordeev e Dipin mantengono gli stessi periodi biologici a 3Q e
  88â€“95k; Petar monetizza 22 SHEEP su 4Q con collection circa 72 ma mostra 192
  HARVEST no-op, dimostrando che periodo senza legality/completion non basta.
CAUSAL_MECHANISM: le soglie tardive concentrano task giÃ  urgenti; un calendario
  anticipa la domanda, ammette asset solo dopo reservation e sfasa i cicli,
  riducendo collisioni, transit e deadline miss. Le soglie restano guardie per
  incertezza reale.
MODEL_CHANGE: sostituire cap/headcount/asset-count autonomi con un entity period
  registry, rolling service calendar, capacity reservations e reactive
  overrides; rendere l'espansione una replica sfasata del ciclo.
EXPECTED_INTERMEDIATE_EFFECT: piÃ¹ alto rapporto SERVICEABLE/ACTIVE, minori
  service peak e no-op, maggiore on-time completion, period adherence stabile
  dopo l'espansione e meno MOVE per output monetizzato.
EXPECTED_ECONOMIC_EFFECT: piÃ¹ output raccolto e venduto per worker-action,
  reinvestimento anticipato e capacitÃ  di scalare oltre Q1 senza distruggere il
  rendimento del ciclo base.
FALSIFICATION_CONDITION: a paritÃ  di asset, seed e mercato, il scheduler non
  migliora on-time completion o monetized output rispetto a V4; oppure peggiora
  deadline miss/cash, non conserva period adherence dopo una replica Q2, o un
  dispatcher threshold-only eguaglia sistematicamente i risultati con minore
  complessitÃ  su episodi indipendenti.
```

## 7. ENTITY_PERIOD_MODEL proposto

Schema comune:

```text
ENTITY_PERIOD_MODEL
- entity_id / tile / kind
- phase
- origin_step
- nominal_period
- next_due_step
- service_window [open, target, close]
- hard_deadline
- expected_output
- required_worker_capacity by window
- route_cluster / inventory requirement
- completion_evidence
- reactive_overrides
```

Candidate osservate, da riconciliare con la Foundation engine prima del BUILD:

| Entity | Phase / nominal period | Service window | Output osservato | Override |
|---|---|---|---|---|
| WHEAT | WATER circa 24; harvest mode scelto per coorte tra turnover e full-yield | legalitÃ  da first-yield; target Codex V4 age 4; hard deadline da `max_lifespan_step` | age 2â€“4, yield 1â€“6; LuCcc 3 stabile ad age 4 | cash/feed, yield reale, decay risk |
| MELON | WATER circa 24; ciclo candidato 10â€“12 day | harvest window age 10â€“12, poi replant slot | yield 6 frequente | horizon, water miss, mercato |
| STRAWBERRY | WATER circa 24; produzione circa 48 | collection candidate age 10/12/14/16 | yield 1â€“2 piÃ¹ frequente | lifespan, inventory, missed water |
| CARROT/TOMATO | periodo non congelato: evidenza insufficiente | metadata engine + reservation | pochi eventi | nessun parametro nuovo |
| COW | FEED 24, CARE 24, production/collection 48 | completare service nel day; collect prima del ciclo successivo | MILK 3 tipico, talvolta bonus 6 | feed/cash/storage |
| SHEEP | FEED 24, CARE 24, production/collection circa 72 | completare service nel day; collect prima del ciclo successivo | WOOL 4 tipico | feed/cash/storage |
| FERTILIZER | sweep candidato giornaliero dopo service animal | quando disponibile e route-compatible | flusso rilevante in tutti i mix animal | storage/prezzo/worker load |

Il `harvest mode` WHEAT deve essere scelto prima della coorte in base a output
atteso per slot, horizon e ruolo feed/liquiditÃ . Non deve oscillare a ogni step
soltanto perchÃ© una soglia di prezzo cambia.

## 8. Espansione come replica controllata

```text
Q1 productive cycle
  -> observe at least complete biological periods
  -> reconcile forecast vs actual service demand
  -> build a shadow Q2 calendar with phase offset
  -> reserve worker, route, cash and sell-through capacity
  -> activate Q2 gradually
  -> repeat validation before Q3/Q4
```

Gate Q2 proposto:

1. nessun hard-deadline miss persistente nel ciclo base;
2. `PRODUCTIVE_SURFACE` e `MONETIZED_OUTPUT` confermano che l'attuale
   `ACTIVE_SURFACE` Ã¨ servita, non soltanto piantata;
3. lo shadow calendar del clone entra in `available_slots(w)` per tutto il
   primo ciclo monetizzabile;
4. workforce e route sono prenotate prima dell'attivazione;
5. costi di land, seed/animal, wage e feed lasciano il cash floor e un horizon
   di payback plausibile;
6. il clone Ã¨ phase-shifted: non replica la stessa maturity wave.

Q3/Q4 non sono vietati. Dipin e Gordeev mostrano che 3Q possono conservare
periodi 24/48/72 con 60â€“72 entitÃ  produttive al picco; Petar mostra un percorso
4Q livestock. Ogni replica deve perÃ² misurare la quota conservata:

```text
retained_cycle_yield(Qn)
  = monetized_output_per_period(Qn)
  / projected_monetized_output_from_Q(n-1)_cycle
```

Nessuna linearitÃ  Ã¨ assunta. Se period adherence, serviceability o conversione
calano, l'espansione si arresta e il modello ripara il ciclo corrente.

## 9. Metriche per la successiva fase PLAN/BUILD

- `period_adherence_by_entity`;
- `due_events`, `completed_in_window`, `hard_deadline_miss`;
- `reserved_slots`, `consumed_slots`, `forecast_error`;
- `service_peak` e `route_allowance` per finestra;
- `ACTIVE_SURFACE`, `SERVICEABLE_SURFACE`, `PRODUCTIVE_SURFACE` separate;
- `monetized_output_per_worker_action` e per entity-period;
- `replant_delay` e `collection_delay`;
- `noop_action_rate` verificata da transizioni;
- `retained_cycle_yield` dopo ogni espansione;
- `sellthrough_lag`, cash trajectory e feed coverage.

La successiva verifica dovrÃ  confrontare V5 e V4 su episodi indipendenti,
separando l'effetto del calendario dall'effetto di mix, headcount, espansione e
mercato. Nessun valore degli score esterni diventa un target di tuning.

## 10. Confini

- nessuna modifica a codice, configurazione, test o runner;
- nessun tournament o Kaggle;
- livestock opzionale: entra soltanto se il suo profilo periodico Ã¨
  serviceable e monetizzabile;
- market reaction non puÃ² autorizzare azioni biologicamente illegali;
- una scadenza pianificata non prova completion: ogni evento richiede la
  transizione osservata;
- il MODEL_SPEC V5 Ã¨ pronto per una fase successiva PLAN/BUILD, non Ã¨
  dichiarato implementato o tournament-ready.

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
```
