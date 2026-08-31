# KAGGRICULTURE C2 — Codex Routine Planning Evidence Review

```text
AGENT_ID: CODEX
REVIEW_TYPE: READ_ONLY_ANALYTICAL_REVIEW
FOUNDATION_CHECKPOINT: f391ee2
IMPLEMENTATION_CHANGED: NO
MODEL_SPEC_CHANGED: NO
BENCHMARK_EXECUTED: NO
TOURNAMENT_EXECUTED: NO
```

## 1. Recovered LuCcc Evidence

La precedente analisi Codex è stata recuperata. La fonte primaria e più
completa è:

- `results/model_spec_c2/periodic_model_review/CODEX_C2_PERIODIC_MODEL_REVIEW.md`.

Il report dichiara esplicitamente analisi per transizione e per entità, con
effetto contato solo quando tile o inventario cambiano coerentemente. Sono stati
inoltre recuperati gli artefatti che la sostengono:

- `docs/benchmark/103484828.json` — replay grezzo LuCcc;
- `docs/benchmark/REPLAY_ANALYSIS_SUMMARY.json` — sommario persistente;
- `scripts/analyze_periodic_replays.py` — estrazione della traiettoria;
- `scripts/deep_inspect_replays.py` — ispezione agronomica e operativa.

Evidenza LuCcc già materializzata:

- score 56.772, un solo quadrante, nessun BUY_LAND effettivo;
- picco 19 crop + 6 animali, 7 worker inclusivo del farmer;
- 1.449 MOVE, pari al 30,29% delle azioni worker;
- 100 HARVEST richiesti e 100 effetti osservati;
- WHEAT sfalsato in coorti massime da una tile, raccolto sempre a age 4 e yield
  3, con riuso per tile circa ogni 96 step;
- MELON in coorti spazialmente compatte, raccolto a yield 6;
- STRAWBERRY con raccolte ricorrenti age 10/12/14/16 e intervallo per tile
  mediano 47,5 step;
- FEED e CARE per COW/SHEEP con mediana 24; collection COW circa 48 e SHEEP
  circa 72;
- 96 MILK, 92 WOOL, 60 STRAWBERRY e 60 MELON monetizzati.

Valutazione Q1:

| Proprietà | Giudizio | Evidenza |
|---|---|---|
| compact | confermata | un solo Q, tutte le 25 tile utili al picco |
| repetitive | confermata | cadence 24/48/72/96 per tile ed entità |
| route-local | moderatamente confermata | footprint Q0 e MOVE share bassa; manca una metrica per-worker di route recurrence |
| role-like | parzialmente confermata | flussi crop/livestock simultanei e regolari; l'analisi precedente non prova identità di ruolo persistente per worker |
| deadline-aware | fortemente confermata | 100/100 HARVEST effettivi, WHEAT age/yield stabile, service animale periodico |

Il replay conferma quindi una routine operativa osservabile a livello di sistema,
ma non consente di attribuirla con certezza a ruoli espliciti nel codice. Ruolo
persistente e route ricorrente restano inferenze da testare, non fatti già
dimostrati.

## 2. Codex Self-Diagnosis

Il risultato V6 — 28–32% di utilizzazione produttiva, 9.851 final money medio,
zero livestock monetizzato e sei invalidazioni biologiche — è compatibile con
planning eccessivamente conservativo. Non è però spiegato dal solo calendario:
le invalidazioni mostrano anche errore tra capacità prevista ed esecuzione reale.

Componenti probabilmente troppo conservative o coarse:

1. **Prenotazione hard per 17 giorni.** Tratta domanda futura incerta come
   impegno quasi equivalente a domanda corrente. Per crop lunghi serve forecast
   fino alla monetizzazione, non immobilizzazione uniforme della capacità.
2. **Reserve fisse 20% + 15%.** Sottraggono il 35% ogni giorno anche quando il
   footprint è compatto e il routing osservato richiede meno margine. La route
   reserve aggregata non usa distanza o route effettiva.
3. **Cinque service slot per worker/day.** È un proxy coarse: non distingue
   azione sulla tile, transit, pickup/place e batching locale.
4. **Commitment immutabile per tutto il giorno.** Impedisce di ricomporre una
   route dopo completion anticipata, worker availability o backlog reale, pur
   senza richiedere un cambio di obiettivo economico.
5. **Cap massimo due nuove entità/day.** È un secondo freno statico sopra la
   feasibility dinamica e limita la velocità con cui una superficie vuota viene
   resa produttiva.
6. **Gate concatenati.** Land, crop fraction, cash, slack e feed ritardano il
   ramo livestock; nello smoke il ramo non ha mai monetizzato.

Conclusione: l'over-conservatism è supportato come causa importante della bassa
scala, ma non esclusiva. Il planner ha protetto la formalità del commitment
senza ottenere sufficiente service completion economica.

## 3. AG Evidence Assessment

Le nuove evidenze sostengono tre conclusioni distinte:

- **workload/serviceability:** ridurre 40→38 tile aumenta WATER sulle stesse 38
  tile (595,7→628) e gross revenue (+1.393,33); più superficie non equivale a
  più output quando il servizio è saturo;
- **architettura Q0 3+3:** 37.997,67 medio contro 24.646,67 del 2+2 (+54,2%);
  quindi il footprint compatto 18 crop + 6 pasture è strutturalmente valido;
- **gap operativo:** market timing non spiega il divario, livestock è vicino a
  LuCcc, mentre crop units sono 24,7 contro 120. Il gap attribuito è soprattutto
  crop serviceability (25.105,33), poi fertilizer (7.366,86).

Questo supporta fortemente una carenza di esecuzione crop. Supporta solo
parzialmente la diagnosi specifica “AG è troppo reattivo”: i dati forniti non
misurano ancora retarget count, route churn, distanza per completion o
duplicazione. Le alternative “priorità errata”, “routing inefficiente” e
“capacity stealing del livestock” restano compatibili con gli stessi risultati.

## 4. Routine Planning Hypothesis

L'evidenza giustifica l'introduzione di routine operative persistenti come
principio C2, ma non prova ancora una particolare implementazione.

La sintesi dei due estremi è plausibile:

```text
AG: serviceability insufficiente con architettura valida
  -> probabile churn/priorità/routing non stabile

Codex: commitment e reservation verificabili
  -> margini, cap e orizzonte hard troppo conservativi

target:
  ruolo/zona persistenti
  + target commitment atomico
  + route locale breve
  + hard reservation a breve orizzonte
  + forecast soft a lungo orizzonte
  + interrupt solo con perdita/opportunità materiale
```

La routine non deve congelare l'intero giorno né fare rescan globale a ogni
turno. Deve stabilizzare l'assegnazione locale lasciando che completion ed eventi
hard riaprano il breve piano.

Verdetto: **SUPPORTED**, non `STRONGLY_SUPPORTED`, perché manca ancora un test
CONTROL/TEST che isoli il routine-planning package e misuri il churn.

## 5. Planning Timescale

| Timescale | Valutazione |
|---|---|
| turn-by-turn global replanning | troppo instabile; utile solo per legality e hard interrupt |
| daily immutable commitment | troppo coarse; impedisce riuso della capacità liberata nello stesso giorno |
| short-horizon rolling plan | preferito per route e task execution |
| event/deadline-driven replanning | necessario come trigger, non come unico planner |

Raccomandazione concreta a doppio orizzonte:

- **ruolo e zona:** persistenti per più giorni, finché una review non dimostra
  overload o sottoutilizzo;
- **target commitment:** persistente fino a completion, invalidazione o hard
  deadline conflict;
- **route plan hard:** rolling per il resto del giorno corrente, aggiornato a
  completion e al boundary giornaliero;
- **capacity reservation hard:** giorno corrente e prossimo service boundary;
- **forecast soft:** fino al primo output monetizzabile per decidere admission,
  senza sottrarre oggi tutta la capacità prevista a 10–17 giorni;
- **replan globale:** EOD, variazione strutturale di workforce/asset o
  invalidazione, non a ogni step.

## 6. Worker Role / Route Assessment

| Meccanismo | Giudizio | Motivazione |
|---|---|---|
| persistent worker roles | PARTIALLY_SUPPORTED | coesistenza stabile dei cicli lo rende plausibile, ma il replay recuperato non traccia persistenza del ruolo per actor id |
| local service zones | SUPPORTED | Q0 compatto, bassa MOVE share e service per tile regolare sostengono clustering spaziale |
| recurrent routes | PARTIALLY_SUPPORTED | periodicità e routing ridotto sono coerenti; manca route-recurrence per worker |
| staging positions | PARTIALLY_SUPPORTED | shed/feed/fertilizer richiedono punti logistici, ma il loro valore incrementale non è isolato |
| target reservations | SUPPORTED | 100/100 HARVEST e cadence per tile sono coerenti con anti-duplicazione e commitment fino a completion |
| task commitment | SUPPORTED | evita wandering senza imporre un piano immutabile per l'intero giorno |

Questi giudizi autorizzano un esperimento, non l'implementazione in questo gate.

## 7. Interrupt Model

| Evento | Classe primaria | Regola |
|---|---|---|
| animal escape prevention | HARD_INTERRUPT | perdita irreversibile dell'asset al boundary |
| FEED deadline | HARD_INTERRUPT | hard vicino a EOD; non deve interrompere anticipatamente se esiste slack dichiarato |
| CARE opportunity | SOFT_INTERRUPT | bonus/opportunità giornaliera, non gate alla produzione base |
| crop watering deadline | HARD_INTERRUPT | hard quando il mancato servizio causa loss al prossimo EOD; prima è task schedulato |
| crop harvest deadline | HARD_INTERRUPT condizionale | hard a decay/retirement/terminale; altrimenti SOFT_INTERRUPT nella finestra legale |
| fertilizer opportunity | SOFT_INTERRUPT | valore incrementale, da batchare con route crop same-day |
| market price opportunity | NO_INTERRUPT per worker | il market order non deve rompere la route biologica; resta decisione market separata |
| inventory clearing | SOFT_INTERRUPT condizionale | diventa hard solo con shed bloccato o overflow EOD imminente |

Gli interrupt hard devono essere pochi, verificabili e associati a perdita
irreversibile o deadline. Un prezzo migliore o una tile appena diventata ready
non giustificano da soli il retarget globale.

## 8. Foundation vs Operational Planning Layer

Ordine raccomandato:

1. **C — introdurre un Operational Planning Model/layer distinto**;
2. **B — collegarlo nelle MODEL_SPEC agent-specific**;
3. **D — policy tuning**, solo dopo che il contratto sperimentale del layer è
   definito;
4. **A — reopen Foundation: non richiesto**.

La Foundation descrive correttamente clock, stato, azioni, loss boundary e
precedenze. Il DLC è semanticamente sufficiente per identità, commitment,
repair, invalidation, review ed evidence. Non prescrive — e non dovrebbe
prescrivere come semantica engine — zone, role persistence, route construction,
hard/soft scheduling horizon, anti-duplication o interrupt budget.

Il gap è quindi tra MODEL_SPEC strategica e dispatcher, non nella Foundation.
Un layer operativo esplicito rende confrontabili forecast, assignment, route e
completion senza trasformare il DLC in un algoritmo di scheduling.

## 9. AG Experiment Review

Verdetto: **VALID_WITH_CORRECTIONS**.

Il CONTROL vs routine-planning-only TEST su Q0/18 crop/3+3/7 worker è pulito per
stimare l'effetto del *package* routine, purché siano preregistrate e congelate:

1. stesse crop tile/specie/coorti, pasture/animali, workforce, market policy,
   admission schedule e interrupt legality;
2. seed e player position paired, repliche held-out e nessun tuning sui seed di
   valutazione;
3. primary endpoint `crop units` e crop gross revenue sulle stesse tile;
4. livestock output come non-inferiority constraint, non soltanto score finale;
5. logging di retarget count, target dwell time, duplicate assignment, MOVE per
   completion, deadline miss, idle, fertilizer collected/applied e inventory
   blockage;
6. stesso action budget e stessa semantica di completion per CONTROL/TEST;
7. report di tutti i seed, non solo media/mediana.

Il trattamento combina ruoli, zone, route, staging, commitment e reservation:
può provare causalmente il package complessivo, non l'effetto di ciascun
componente. Per attribuzione interna servono ablation successive, non necessarie
per il primo gate.

## 10. Q1 Scaling Preconditions

Il successivo Q0+Q1 con 3 COW + 3 SHEEP per quadrante è sensato solo in modo
condizionale. Prima di espandere devono essere soddisfatti:

1. routine TEST superiore al CONTROL su seed/seat paired e held-out;
2. crop units e revenue Q0 materialmente maggiori, con output MILK/WOOL non
   inferiore oltre la tolleranza preregistrata;
3. almeno un ciclo lungo completo Q0 con WATER/HARVEST/FEED/CARE on-time e senza
   aumento materiale di invalidation/no-op;
4. route cost reale e retarget rate misurati, non sostituiti da una reserve
   percentuale fissa;
5. capacity shadow Q1 che includa transit, feed logistics, collection,
   fertilizer e inventory handling lasciando slack osservato;
6. cassa, feed, shed e horizon sufficienti al primo output monetizzabile Q1;
7. zone Q1 e responsabilità worker non ambigue; nessun raddoppio se il servizio
   aggiunto riduce la serviceability crop Q0;
8. rollback/reduce gate preregistrato se la retained output del ciclo Q0 cala.

Non è giustificato duplicare 3+3 soltanto perché Q0 ha score maggiore del 2+2:
deve prima essere dimostrato che il planning routine, non il seed o il mix, ha
liberato capacità replicabile.

## 11. Final Verdict

L'evidenza disponibile giustifica routine operative persistenti come principio
di planning C2. La forma raccomandata è un layer operativo a doppio orizzonte:
ruoli/zone persistenti, commitment atomico del target, route rolling entro il
giorno, hard reservation breve, forecast biologico lungo ma soft, e interrupt
limitati a deadline o perdite materiali.

LuCcc fornisce evidenza forte del risultato sistemico — compattezza, periodicità,
basso movement share, 100% harvest effectiveness — ma solo moderata sul
meccanismo interno di ruolo/route. Le evidenze AG rendono crop serviceability il
gap primario; l'esperimento proposto è necessario per distinguere routine
planning da priorità o capacity stealing.

```text
LUCCC_ANALYSIS_RECOVERED:
YES

LUCCC_ROUTINE_EVIDENCE:
MODERATE

CODEX_OVERCONSERVATIVE_PLANNING:
SUPPORTED

AG_OVERREACTIVE_PLANNING:
PARTIALLY_SUPPORTED

ROUTINE_PLANNING_HYPOTHESIS:
SUPPORTED

PREFERRED_PLANNING_TIMESCALE:
ROLLING_CURRENT_DAY_WITH_EVENT_DRIVEN_REPLAN_AND_SOFT_LONG_HORIZON_FORECAST

PERSISTENT_ROLES:
PARTIALLY_SUPPORTED

LOCAL_ZONES:
SUPPORTED

RECURRENT_ROUTES:
PARTIALLY_SUPPORTED

TASK_COMMITMENT:
SUPPORTED

SHORT_HORIZON_CAPACITY_RESERVATION:
SUPPORTED

FOUNDATION_REOPEN_REQUIRED:
NO

OPERATIONAL_PLANNING_LAYER_RECOMMENDED:
YES

AG_ROUTINE_EXPERIMENT:
VALID_WITH_CORRECTIONS

Q0_PLUS_Q1_3X3_NEXT_IF_Q0_SUCCEEDS:
CONDITIONAL

TOP_3_RECOMMENDATIONS:
1. Testare il package routine su Q0 con architettura e market policy congelate, seed/seat paired e logging di churn/route/completion.
2. Separare hard reservation del giorno corrente dal forecast soft fino al primo output monetizzabile.
3. Espandere a Q1 solo dopo miglioramento crop held-out, non-inferiority livestock e shadow capacity basata su route cost osservato.

IMPLEMENTATION_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
