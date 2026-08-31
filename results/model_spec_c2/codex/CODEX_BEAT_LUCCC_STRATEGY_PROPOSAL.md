# KAGGRICULTURE C2 — Codex Strategy Proposal to Beat LuCcc

```text
AGENT_ID: CODEX
TASK_TYPE: INDEPENDENT_ANALYSIS_AND_DESIGN
REFERENCE_BENCHMARK: LUCCC_EPISODE_103484828
REFERENCE_SCORE: 56772
FOUNDATION_CHANGED: NO
DLC_CHANGED: NO
MODEL_SPEC_CHANGED: NO
IMPLEMENTATION_CHANGED: NO
BENCHMARK_EXECUTED: NO
TOURNAMENT_EXECUTED: NO
```

## 1. Executive Strategy

Il prossimo candidate Codex non deve essere una correzione incrementale della
V6. Deve essere un agente nuovo, costruito attorno a un'economia compatta Q0 e
a un sistema operativo di routine locali.

La scelta primaria è **A — compact Q0 hybrid, LuCcc-like**: sette worker totali,
sei pasture con 3 COW + 3 SHEEP e 18 crop tile, con MELON e STRAWBERRY come
motore economico e WHEAT come supporto. Il mix replica la parte di LuCcc già
validata economicamente; la policy non replica un'implementazione ignota. La
differenza proposta è un modello operativo esplicito: ruoli persistenti, zone
locali, route corte ricorrenti, commitment al singolo target e replan globale
soltanto a fine giornata o dopo invalidazioni strutturali.

La tesi causale è:

```text
stesso footprint Q0 economicamente valido
+ minore churn di assegnazione
+ protezione separata delle route crop e livestock
+ cohort staggering
+ admission basata su azioni e deadline osservabili
= recupero del gap di crop serviceability senza perdere MILK/WOOL
```

Il candidate deve battere prima 56.772 su Q0. L'obiettivo di progetto di 80.000
non è una previsione credibile per il primo test: richiederà probabilmente una
successiva scala Q1, ma solo dopo che il ciclo Q0 avrà dimostrato serviceability
e margine replicabili.

## 2. LuCcc Lessons Retained

Le lezioni trattenute sono quelle osservabili nel replay, non inferenze sul suo
codice:

- compattezza: un solo quadrante, sette worker e fino a 25 entità produttive;
- densità economica: 3 COW, 3 SHEEP, MELON e STRAWBERRY ad alto valore;
- periodicità: servizi animali 24/48/72 e routine crop 24/48/96 step;
- batching spaziale: coorti MELON compatte e STRAWBERRY sfalsate;
- efficacia: 100 HARVEST richiesti e 100 effetti osservati;
- controllo del transito: MOVE al 30,29% delle azioni, nonostante footprint pieno;
- output bilanciato: 96 MILK, 92 WOOL, 60 STRAWBERRY e 60 MELON.

Non viene assunto che LuCcc usasse davvero ruoli persistenti o route codificate:
l'evidenza su questi meccanismi è moderata/parziale. Sono ipotesi da isolare nel
prossimo esperimento. Non viene trattenuta l'idea che il mercato sia il vantaggio
primario: il gap dominante osservato è crop serviceability.

## 3. Current Codex V6 Failures

La V6 ha protetto un piano formale invece di produrre. I risultati — 9.851 di
final money medio, 28–32% di utilizzazione produttiva, nessun livestock
monetizzato e sei invalidazioni biologiche — mostrano quattro fallimenti:

1. **Capacità immobilizzata troppo presto.** Il calendario hard a 17 giorni
   tratta domanda futura incerta come carico corrente.
2. **Margini non osservabili.** Le reserve 20% + 15% sottraggono il 35% prima di
   misurare route, handling, deadline o capacità completata.
3. **Commitment alla scala sbagliata.** Congelare il giorno intero impedisce di
   riutilizzare worker liberi; il commitment utile è al target atomico.
4. **Architettura disallineata con la prova disponibile.** Due quadranti, otto
   hands, cap di due entità e livestock condizionale aggiungono transit e
   variabili mentre il problema da risolvere è rendere serviceable Q0.

La V6 resta riusabile per adapter engine, controlli di legalità, identificazione
delle entità, verifica request/effect e telemetria. Strategia produttiva e
planner vanno invece sostituiti.

## 4. Proposed Production Architecture

```text
PRIMARY_ARCHITECTURE: A_COMPACT_Q0_HYBRID_LUCCC_LIKE
SECONDARY_FALLBACK: D_Q0_VALIDATED_THEN_Q1_STAGED_SCALING
```

### Footprint primario

| Componente | Valore proposto | Stato |
|---|---:|---|
| Land | Q0 soltanto | fisso nel primo candidate |
| Worker | 7 totali, farmer incluso | fisso |
| Crop tile | 18 | fisso |
| MELON | 9 tile | fisso nel primo esperimento |
| STRAWBERRY | 8 tile | fisso nel primo esperimento |
| WHEAT | 1 tile di supporto | fisso nel primo esperimento |
| Pasture | 6 | fisso |
| COW | 3 | attivazione staged |
| SHEEP | 3 | attivazione staged |
| Shed | staging feed, fertilizer e prodotti | uso logistico |

Le 18 crop tile sono una scelta deliberatamente più leggera del picco
replay-verified di 19: riduce di una tile il carico giornaliero senza eliminare
una specie. Se un dry run tecnico dimostrasse una venticinquesima posizione
produttiva senza conflitto, la diciannovesima tile MELON sarebbe un parametro
sperimentale successivo, non un cambio durante i seed preregistrati.

### Opzioni respinte

| Famiglia | Verdetto | Motivo |
|---|---|---|
| B — Q0 hybrid con mix diverso | REJECT | nessuna evidenza che GOOSE o un rapporto animale diverso superi il 3+3; cambierebbe insieme economia e planning |
| C — pure horticulture | REJECT_AS_PRIMARY | 43.837,33 medio resta 12.934,67 sotto LuCcc e perde il loop fertilizer/livestock |
| D — Q0 + Q1 staged | REJECT_AS_FIRST / KEEP_AS_FALLBACK | aggiunge transit e confonde il test prima che Q0 sia serviceable |
| E — altra architettura | REJECT | manca evidenza economica superiore al Q0 3+3 già strutturalmente valido |

## 5. Worker Operating Model

L'organizzazione iniziale dei sette worker è:

```text
3 CROP WORKERS
  -> una zona da 6 crop tile ciascuno
2 LIVESTOCK WORKERS
  -> uno responsabile di 3 COW, uno di 3 SHEEP
1 FERTILIZER / LOGISTICS WORKER
  -> shed, feed staging, fertilizer sweep, inventory unblock
1 FLOAT / RESERVE WORKER
  -> farmer; copre picchi, assenze e hard interrupt senza vagare
```

I ruoli persistono attraverso più giorni se le metriche di zona restano sane.
Non sono professioni rigide: l'EOD può riassegnarli, e un hard interrupt può
prestare temporaneamente il reserve worker. Il worker crop non viene sottratto
alla propria zona per FEED/CARE ordinari.

| Meccanismo | Scelta | Regola |
|---|---|---|
| persistent roles | USE | riduce scansione globale e rende osservabile la responsabilità |
| dynamic roles | TEST | ammessi soltanto a EOD o per indisponibilità strutturale |
| fixed zones | USE | tre cluster crop da 6 tile e due cluster animali da 3 |
| dynamic zones | TEST | solo overflow dichiarato dopo misura del backlog |
| recurrent routes | USE | route nominali WATER/HARVEST e FEED/CARE/COLLECT riusate finché valide |
| global dispatcher | DO_NOT_USE | non turn-by-turn; resta un planner EOD |
| local dispatcher | USE | seleziona il prossimo target legale dentro ruolo/zona |
| task commitment | USE | target assegnato fino a effect, invalidation o hard interrupt |
| staging | USE | feed e prodotti passano per punti shed prevedibili |
| reserve worker | USE | svolge logistica e assorbe eccezioni; non resta necessariamente idle |

## 6. Planning and Replanning

Il planner usa due orizzonti, non un calendario hard uniforme:

- **strategic horizon:** fino a fine episodio per payback, mix e decisione Q1;
- **forecast horizon:** fino al primo output monetizzabile del nuovo asset; è
  soft e serve ad admission;
- **hard scheduling horizon:** resto del giorno corrente e prossimo service
  boundary di ogni entità;
- **rolling local plan:** breve sequenza route-local, ricomposta dopo completion;
- **EOD review:** riconcilia domanda prevista, azioni completate, miss, route
  cost, cash e inventory.

```text
HOW_OFTEN_GLOBAL_REPLAN:
EOD, workforce/asset change, structural invalidation, or infeasible hard-deadline set.

HOW_OFTEN_LOCAL_REPLAN:
After target completion, target invalidation, worker unavailability, or a hard interrupt.

WHAT_IS_COMMITTED:
One entity/action objective plus the short pickup/move/interact sequence needed to complete it.

WHAT_CAN_INTERRUPT:
Imminent irreversible loss, engine-legality change, worker loss, blocking inventory,
or a newly infeasible hard-deadline set.

WHAT_IS_FORECAST_ONLY:
Services beyond the next entity boundary, long maturation, expected revenue, and possible Q1 demand.
```

Una tile appena pronta, un prezzo migliore o un task con priorità appena
superiore non interrompono da soli un target già in corso.

## 7. Biological Scheduling

La priorità è lessicografica:

```text
1. irreversible loss before the next feasible service
2. economic value at risk
3. deadline proximity / remaining slack
4. route-local completion cost
```

| Attività | Classe operativa | Regola |
|---|---|---|
| WATER | HARD quando il prossimo EOD causa loss; altrimenti routine crop | route giornaliera per zona prima del lavoro discrezionale |
| HARVEST | HARD a decay/termine; HIGH quando output ad alto valore è pronto | reservation per tile e verifica effect prima del replant |
| FEED | HARD solo vicino all'escape boundary; routine ogni giorno | i worker livestock non usano normalmente worker crop |
| CARE | SOFT con cadence giornaliera | batched con FEED; non scavalca WATER/HARVEST hard |
| MILK collection | HIGH prima del successivo ciclo/cap | route COW circa ogni 48 step, poi PLACE/sale batch |
| WOOL collection | HIGH prima del successivo ciclo/cap | route SHEEP circa ogni 72 step |
| fertilizer collection | SOFT routine | sweep logistico dopo i giri animali |
| fertilizer application | SOFT ad alto valore | solo a MELON/STRAWBERRY irrigabili nello stesso giorno |
| REPLANT | GROWTH task | solo dopo effect HARVEST e capacity admission del nuovo ciclo |

La separazione delle zone impedisce il capacity stealing ordinario. In caso di
conflitto interviene prima il float/reserve, poi il worker logistico. Un worker
crop viene prestato al livestock solo per prevenire una perdita irreversibile;
l'evento viene contato come interrupt e spiegato all'EOD.

## 8. Crop Strategy

### MELON

Nove tile sono divise in tre coorti spaziali da 3. Gli offset iniziali proposti
sono day 0/1/2 rispetto all'ammissione della prima coorte. L'offset è un
**parametro sperimentale preregistrato**: può essere adattato una volta prima dei
seed in base a liquidità/legality, mai durante CONTROL/TEST. MELON produce batch
ad alto valore senza un unico picco di nove HARVEST/REPLANT.

### STRAWBERRY

Otto tile sono due coorti compatte da 4, sfalsate di due giorni. La route torna
nella finestra ricorrente circa ogni 48 step e protegge le raccolte successive
age 10/12/14/16. STRAWBERRY fornisce cash flow ricorrente tra i batch MELON.

### WHEAT

Una tile è una coorte singola di supporto, con target full-yield age 4 e riuso
circa ogni 96 step. Il primo scopo è il buffer FEED; la vendita è residuale. Se
la produzione interna non copre il consumo, il mercato rifornisce il buffer:
non si moltiplicano automaticamente tile WHEAT sottraendo servizio alle colture
ad alto valore.

### Fertilizer

```text
1. MELON cohort con harvest atteso entro l'horizon utile
2. STRAWBERRY all'inizio di una sequenza produttiva ricorrente
3. nessuna applicazione se WATER same-day non è già schedulabile
4. WHEAT solo se un vincolo feed rende il rendimento economicamente critico
```

Il mix mantiene i ruoli economici LuCcc con una tile MELON in meno rispetto al
picco replay-verified, così il primo test conserva slack osservabile.

## 9. Livestock Strategy

**COW** resta perché LuCcc mostra 96 MILK e collection circa 48, mentre AG 3+3
raggiunge già 93 MILK: è il ramo più vicino alla non-inferiority.

**SHEEP** resta perché WOOL diversifica cadenza e ricavo, usa collection circa
72 e nel benchmark produce 92 unità. Le 74 unità AG mostrano un gap recuperabile
ma reale.

**GOOSE** non entra: manca evidenza comparabile che compensi la perdita di una
COW/SHEEP o riduca il servizio. Testarla ora renderebbe ambiguo il risultato.

Attivazione proposta:

1. predisporre le sei pasture in Q0;
2. attivare 2 COW + 2 SHEEP tra day 0 e day 1 solo con buffer feed e liquidità;
3. completare almeno un ciclo COW e un ciclo SHEEP senza miss;
4. attivare la terza COW circa day 7 e la terza SHEEP circa day 8, se la regola
   di capacity admission passa.

Gli offset day 7/8 sono parametri sperimentali congelati prima dei seed; la
condizione di capacità non è negoziabile. FEED + CARE vengono eseguiti in un
unico giro locale. COW collection è prenotata circa ogni 48 step, SHEEP circa
ogni 72; fertilizer viene raccolto dal worker logistico nello stesso cluster.

Il ramo è valido solo se, sul batch sperimentale, raggiunge:

```text
MILK >= 90 mean units
WOOL >= 85 mean units
FEED/CARE on-time >= 95%
ANIMAL_ESCAPE = 0
```

## 10. Market Strategy

Il mercato è **LOW_PRIORITY** come fonte di vantaggio, pur restando necessario
per liquidità e conversione dell'output.

- vendere MILK, WOOL, MELON e STRAWBERRY in un batch giornaliero dopo le route
  biologiche, oppure prima se shed blockage impedirebbe una collection;
- mantenere WHEAT pari ad almeno due giri FEED completi, cioè `2 × animali
  attivi` (12 unità a pieno footprint);
- mantenere fertilizer soltanto per la prossima coorte già ammessa, con cap
  operativo di 6 unità; vendere l'eccesso nel batch giornaliero;
- non mantenere riserve speculative di MILK, WOOL o fruit;
- non interrompere worker biologici per oscillazioni di prezzo a breve;
- non comprare per rivendere nel primo candidate.

La contribution da trading speculativo attesa è zero e viene misurata
separatamente per non mascherare la qualità produttiva.

## 11. Scaling Policy

Il primo candidate resta Q0-only. La compattezza domina perché:

1. il benchmark immediato è già stato raggiunto su Q0;
2. AG dimostra che 3+3 Q0 è strutturalmente valido ma crop-serviceability è
   insufficiente;
3. Q1 aggiunge transit, workforce e nuovi cicli prima di isolare la causa;
4. la V6 mostra che superficie teorica e output monetizzato divergono;
5. un Q0 denso misura più pulitamente ruoli/zone/route.

Q1 è il fallback verso 80.000, non parte del primo tentativo. Può essere
valutato soltanto dopo:

- superamento held-out di 56.772 su Q0;
- almeno un ciclo lungo senza hard deadline miss o animal escape;
- MELON + STRAWBERRY almeno 90 unità medie;
- livestock non inferiore a 90 MILK / 85 WOOL;
- shadow schedule Q1 con slack non negativo usando costi route osservati;
- payback previsto prima della fine episodio;
- rollback se l'output retained Q0 cala oltre il 10%.

## 12. Capacity Admission Rule

La capacità non è una percentuale astratta. Per ogni finestra `w` dal momento
corrente al prossimo service boundary si calcolano quantità osservabili:

```text
AVAILABLE(w) = worker action slots realmente disponibili nella finestra

REQUIRED(w) = service actions dovute
            + exact route MOVE actions dal posizionamento corrente
            + PICKUP / PLACE / inventory handling
            + azioni richieste dall'asset candidato

SLACK(w) = AVAILABLE(w) - REQUIRED(w)
```

Il costo route deriva dalla breve sequenza sulle posizioni correnti e sui
cluster assegnati; non è una reserve del 20%. Le deadline derivano dallo stato
engine e dalle finestre biologiche.

```text
ADMIT_NEW_ASSET if and only if:
  all current assets and the candidate meet every hard deadline
  in the current-day / next-service-boundary schedule
AND min(SLACK(w)) >= 0
AND feed on hand or immediately affordable covers two FEED rounds
AND cash after acquisition covers already committed biological inputs
AND inventory has a legal collection/sale path
AND first monetizable output occurs before the episode payback cutoff
AND forecast peak demand to first output does not exceed observed capacity.
```

Dopo tre giorni completi, `observed capacity` è il minimo delle azioni utili
effettivamente completate nei tre giorni, corretto con MOVE/handling osservati.
Prima di avere tre giorni, nessuna crescita oltre il bootstrap preregistrato è
ammessa sulla sola base di forecast. La regola governa terza COW, terza SHEEP,
replant e ogni futura espansione.

## 13. Performance Model

Il final money viene decomposto, non usato come unica spiegazione:

| Famiglia | Metriche obbligatorie |
|---|---|
| economia | final money, crop revenue, livestock revenue, market/trading contribution |
| output | MILK, WOOL, MELON, STRAWBERRY, WHEAT consumed/sold, fertilizer collected/applied |
| servizio | WATER/HARVEST/FEED/CARE/COLLECT on-time, deadline misses, invalidation, no-op |
| capacità | productive action ratio, productive utilization, MOVE/productive action, PASS ratio |
| stabilità | retarget count, target dwell time, duplicate assignment, interrupt by reason |
| conversione | revenue per worker-action, crop units per crop-tile-day, livestock output per animal-cycle |

Le cinque leading indicator preregistrate sono:

1. `ON_TIME_CROP_SERVICE_RATIO` — WATER + HARVEST nelle finestre;
2. `HARD_DEADLINE_MISSES` — deve restare vicino a zero;
3. `HIGH_VALUE_CROP_UNITS_VS_COHORT_PLAN` — MELON + STRAWBERRY cumulative;
4. `MOVE_PER_PRODUCTIVE_ACTION` — misura se zone/route liberano capacità;
5. `RETARGET_COUNT_PER_WORKER_DAY` — misura direttamente il churn.

Productive utilization resta una metrica chiave, ma non sostituisce l'on-time
service: una tile occupata ma non serviceable non vale come successo.

## 14. Preregistered Prediction

```text
EXPECTED_FINAL_MONEY:
60000-68000

MINIMUM_ACCEPTABLE:
56773

EXPECTED_MILK:
90-100

EXPECTED_WOOL:
85-95

EXPECTED_STRAWBERRY:
45-60

EXPECTED_MELON:
48-60

EXPECTED_PRODUCTIVE_UTILIZATION:
80-96%
```

La previsione non assume il target 80.000. Parte dal Q0 3+3 AG di 37.997,67.
L'analisi forense attribuisce circa 25.105 al gap crop, 7.367 al fertilizer e
circa 1.200 all'endgame. Recuperare il 70–90% di quel gap porta grossolanamente
a 61,6–68,3k; il range 60–68k include arrotondamento e il costo della tile MELON
rimossa rispetto al picco LuCcc.

MILK è ancorato ai 93 AG e 96 LuCcc. WOOL richiede recupero rispetto a 74 AG ma
resta sotto/attorno a 92 LuCcc. I range crop recuperano circa 75–100% delle 120
unità high-value LuCcc, con MELON più prudente per la configurazione a nove
tile. L'utilizzazione viene conteggiata come productive e serviceable, non solo
active.

## 15. V6 Components to Keep/Remove/Rewrite

| Elemento V6 | Decisione | Motivo |
|---|---|---|
| 17-day hard capacity calendar | REMOVE | hard horizon breve + forecast soft fino al primo output |
| 20% route reserve | REMOVE | route MOVE simulata/osservata |
| 15% exception reserve | REMOVE | hard interrupt espliciti e slack in azioni |
| immutable daily commitment | REWRITE | commitment atomico al target, route locale rolling |
| max 2 new entities/day | REMOVE | admission dipende da deadline, azioni, feed, cash e slack |
| 2-quadrant default | REMOVE | Q0-only finché il ciclo non batte LuCcc |
| 8-hand default | REWRITE | 7 worker totali; crescita capacity-driven |
| conditional COW branch | REWRITE | ramo 3 COW + 3 SHEEP staged, centrale nel test |

Da mantenere:

- adapter osservazione/azione e compatibilità standalone;
- legalità engine e guardie biologiche;
- identità stabile di worker, tile, crop e animal;
- verifica request/effect prima di dichiarare completion;
- metriche di invalidation/no-op e attribution economica.

Il giudizio complessivo di riuso V6 è **MEDIUM**: infrastruttura e verificabilità
sono utili, architettura produttiva e planner non lo sono.

## 16. MODEL_SPEC / Lifecycle Simplification

Non serve un DLC separato né un nuovo Operational Planning Model per questo
candidate. Le policy operative sono agent-specific e devono stare nella
MODEL_SPEC Codex; engine semantics, ontology e state machine restano nei layer
condivisi esistenti.

| Concetto | Classificazione | Forma minima |
|---|---|---|
| decision identity | MODEL_SPEC_CORE | run/seed/seat, worker, target e action request identificabili |
| DEFINE | REMOVE | objective/configurazione statici nella MODEL_SPEC, non fase runtime |
| PLAN | MODEL_SPEC_CORE | priority, zone, route e admission rule |
| commitment | MODEL_SPEC_CORE | target atomico fino a completion/invalidation/hard interrupt |
| VERIFY | MODEL_SPEC_CORE | request non equivale a effect; verificare post-state |
| REVIEW | IMPLEMENTATION_DETAIL | riconciliazione EOD e report esperimento |
| SHIP | REMOVE | processo repository, non lifecycle dell'agente |
| repair | IMPLEMENTATION_DETAIL | ricostruzione locale di task/route |
| invalidation | MODEL_SPEC_CORE | insieme piccolo e nominato di trigger |
| supersession | REMOVE | invalidare e creare nuovo target è sufficiente |
| evidence ledger | IMPLEMENTATION_DETAIL | event log semplice; campi minimi richiesti dalla MODEL_SPEC |
| capacity reservation | MODEL_SPEC_CORE | current day + next service boundary, in azioni osservabili |
| roles | MODEL_SPEC_CORE | responsabilità persistenti e regole di prestito |
| routes | MODEL_SPEC_CORE | cluster e ricomposizione locale |
| interrupts | MODEL_SPEC_CORE | hard cause enumerate e reason code |

I soli principi DLC che devono sopravvivere sono: identità osservabile della
decisione, nessun replan silenzioso del target, verifica post-state, reason code
per hard interrupt e distinzione tra invalidation e completion. Sopravvivono
come sezioni brevi della MODEL_SPEC, non come macchina a stati separata.

Questa conclusione aggiorna la precedente review: il contenuto operativo allora
raccomandato resta utile, ma il nuovo contesto mostra che non richiede un layer
condiviso. La comparabilità si ottiene con metriche e configurazione congelate.

## 17. Minimum Next Experiment

Un solo esperimento paired isola il package routine dall'architettura:

```text
EXPERIMENT_ID:
CODEX-C2-Q0-ROUTINE-CAUSAL-01

CONTROL:
Q0, 18 crop (9 MELON / 8 STRAWBERRY / 1 WHEAT), 3 COW, 3 SHEEP,
7 worker, stessi cohort/activation/market/admission e priority rules;
dispatcher globale reattivo senza ruoli persistenti, route ricorrenti o
target commitment oltre il turn.

TEST:
Identica economia e identici interrupt; 3 crop roles, 2 livestock roles,
1 logistics role, 1 float, zone fisse, route locali ricorrenti e commitment
atomico fino a effect/invalidation/hard interrupt.

SEEDS:
26090101, 26090102, 26090103; entrambi i player seat; pairing esatto;
nessun tuning sui sei episodi.

PRIMARY_ENDPOINT:
Mean total high-value crop units = MELON + STRAWBERRY.

SECONDARY_ENDPOINTS:
Final money, crop/livestock revenue, MILK, WOOL, fertilizer applied,
on-time service, MOVE/productive action, PASS, hard misses, retarget,
duplicate assignment and productive utilization.

SUCCESS_CRITERION:
TEST mean high-value crop units >= 90 and >= CONTROL by 30 units;
TEST mean final money > 56772;
at least 4/6 TEST episodes > 50000;
TEST MILK+WOOL >= 90% of CONTROL;
zero animal escape.
```

Interpretazione preregistrata del fallimento:

- crop non migliora e retarget/MOVE non calano: package non realizzato o
  meccanismi incapaci di controllare il churn;
- retarget/MOVE calano ma crop non migliora: causa in priorità, cohort timing,
  inventory o fertilizer, non instabilità di route;
- crop migliora ma livestock scende oltre 10%: ruoli/zone allocano male la
  capacità o il livestock continua a rubare slack;
- output fisico migliora ma final money non batte LuCcc: problema di mix,
  activation cost o endgame conversion, non market timing intraday;
- output reggono ma score resta 50–56,7k: material improvement ma target miss;
  valutare mix/19a tile prima di Q1;
- hard miss o escape: admission/interrupt policy falsificata e Q1 vietato.

Il test misura l'intero package routine. Le ablation dei singoli componenti
vengono dopo e non fanno parte dell'esperimento minimo.

## 18. Final Verdict

La via con più evidenza per superare LuCcc è rendere eseguibile una farm Q0 3+3
già validata, non aggiungere land, trading o formalismo. Codex deve sostituire il
planner V6 con responsabilità persistenti, route locali, commitment atomico e
capacity admission basata su azioni/deadline osservabili.

Il primo candidate punta realisticamente a 60–68k. È sufficiente a falsificare
o confermare la strategia e a superare il benchmark immediato, ma non autorizza
ancora l'obiettivo 80k. Q1 diventa razionale solo quando Q0 dimostra capacità
liberata reale, misurata e replicabile.

```text
PRIMARY_ARCHITECTURE:
A_COMPACT_Q0_HYBRID_LUCCC_LIKE_WITH_ROUTINE_LOCAL_EXECUTION

SECONDARY_FALLBACK:
D_Q0_VALIDATED_THEN_Q1_STAGED_SCALING

TARGET_TO_BEAT:
56772

EXPECTED_FINAL_MONEY:
60000-68000

MINIMUM_ACCEPTABLE:
56773

Q0_ONLY_FIRST:
YES

WORKER_MODEL:
3_CROP_2_LIVESTOCK_1_FERTILIZER_LOGISTICS_1_FLOAT_RESERVE

PLANNING_MODEL:
PERSISTENT_ROLES_LOCAL_ROLLING_ROUTES_SOFT_LONG_HORIZON_FORECAST

GLOBAL_REPLAN_FREQUENCY:
EOD_OR_STRUCTURAL_INVALIDATION_ONLY

TASK_COMMITMENT:
ATOMIC_TARGET_UNTIL_COMPLETION_INVALIDATION_OR_HARD_INTERRUPT

LIVESTOCK_CONFIGURATION:
6_PASTURE_3_COW_3_SHEEP_STAGED_2PLUS2_THEN_1PLUS1

CROP_CONFIGURATION:
18_TILES_9_MELON_8_STRAWBERRY_1_WHEAT

MARKET_PRIORITY:
LOW_PRIORITY

CURRENT_V6_REUSABLE:
MEDIUM

DLC_REQUIRED_AS_SEPARATE_LAYER:
NO

OPERATIONAL_PLANNING_LAYER_REQUIRED:
NO

MODEL_SPEC_SHOULD_ABSORB_OPERATIONS:
YES

NEXT_EXPERIMENT:
Q0_FIXED_ARCHITECTURE_REACTIVE_CONTROL_VS_ROUTINE_TEST_3_PAIRED_SEEDS_BOTH_SEATS

IMPLEMENTATION_AUTHORIZED:
NO

TOURNAMENT_AUTHORIZED:
NO

KAGGLE_AUTHORIZED:
NO
```
