# MODEL_SPEC Codex E18.4 V2 — dispatcher locality/task-aging

## Identità e decisione

- candidate: `CODEX_E18_4_STATE_DRIVEN_772_V2`;
- model spec: `CODEX-E18.4-STATE-DRIVEN-772-V2`;
- ruolo: ablation development-only, nessun upload Kaggle;
- base di bootstrap: E18.2 fino a D10 incluso;
- architettura produttiva: E18.4 V1 `7-7-2` dal D11;
- unica variabile sperimentale: dispatcher delle unità.

## Esito build e gate — 2026-09-04

La candidata è stata implementata e misurata sui 14 match development
preregistrati. Gate A è `FAIL`; Gate B non è stato eseguito e nessun upload
Kaggle è autorizzato. Passano topologia/fill `14/14`, perdite/errori/fallback
`0/0/0`, `PASS` su tile azionabile `0` e route thrashing `0`. Falliscono i
cinque KPI di lavoro: move `4.477,43`, productive `2.217,43`,
move/productive `2,0192`, harvested units `472,57` e late weed tile-days
`36,36`. Il money, registrato ma non decisionale per Gate A, è `47.247,57`
contro `77.644,29` del controllo (`0-14`).

Artifact e report canonici:

- `docs/model_specs/codex/e18/artifacts/derived/E18_4_STATE_DRIVEN_772_V2_DEV_GATE.json`;
- `docs/model_specs/codex/e18/reports/E18_4_STATE_DRIVEN_772_V2_DEV_GATE_REPORT_IT.md`.

V2 conserva integralmente topologia, cap zootecnico, Wheat reserve, harvest
batching, costruzione, input market, sale ledger e liquidazione D29 di V1. Non
modifica la generazione dei task né le priorità biologiche. Sostituisce soltanto
il matching globale greedy di `CoreTask` a worker.

## Ipotesi causale

Il reset giornaliero di `last_assignments` e il ranking globale
`priority → distanza` causano ping-pong quando classi di task diverse si
alternano. Una ownership persistente dei cluster, un'età esplicita dei task e
affinità per i carrier devono ridurre le traversate senza sacrificare sicurezza
o throughput.

Il successo non è definito dal money in prima battuta. Prima deve essere
dimostrato che il nuovo dispatcher converte spostamenti in azioni produttive.

## Contratto del dispatcher

### 1. Cluster e ownership

I target appartengono a quattro domini stabili:

- `Q0_NW`: celle con `x < 5, y < 5`;
- `Q1_NE`: celle con `x >= 5, y < 5`;
- `Q2_SW`: celle con `x < 5, y >= 5`;
- `SHED_CORRIDOR`: i quattro accessi allo shed e i task di pickup/drop.

Al D11 ogni worker riceve un `home_cluster` con matching deterministico
min-cost rispetto alla posizione corrente e al carico atteso del cluster.
L'ownership persiste fra turni e giorni; non deve essere cancellata al cambio
giorno. Un worker può cambiare cluster soltanto per:

1. emergenza `CRITICAL_FEED` o `CRITICAL_WATER` senza owner disponibile;
2. cluster locale senza task eseguibili per almeno 12 step consecutivi;
3. backlog remoto con età almeno 12 step e differenziale di almeno 3 task;
4. carrier che deve raggiungere o lasciare lo shed.

Il riequilibrio ordinario è limitato a un worker per cluster e per giorno.

### 2. Task identity, aging e deadline

Per ogni `CoreTask.identity` il dispatcher mantiene:

- `first_seen_step`;
- `last_seen_step`;
- `age_steps`;
- `deadline_slack`, quando derivabile da starvation, lifespan o D29;
- `assigned_worker` e `assignment_started_step`;
- numero e motivo delle preemption.

L'età non cambia la classe di sicurezza, ma impedisce starvation all'interno
della stessa classe. L'ordine è lessicografico:

1. classe di sicurezza/deadline;
2. task già eseguibile sul tile corrente;
3. task già assegnato allo stesso worker;
4. task nel `home_cluster`;
5. carrier affinity;
6. age bucket decrescente;
7. distanza Manhattan;
8. worker ID e coordinate target come tie-break deterministici.

Una assegnazione resta sticky finché il task è eseguito, scompare, diventa
invalido o viene preemptato da una classe di sicurezza superiore. Un task
ordinario più vicino non può causare preemption.

### 3. Carrier affinity

- un worker con Wheat serve prima gli animali del proprio cluster;
- un worker con seed resta nel cluster crop finché esistono target compatibili;
- un worker con prodotto raccolto mantiene la coda locale fino a soglia
  inventario o deadline di drop;
- un worker con animale è riservato a `PLACE_ANIMAL` compatibile;
- pickup allo shed deve preferire il carrier già più vicino e non strappare un
  owner che sta eseguendo un task critico.

### 4. Regole anti-spreco

- se il worker è già su un tile con task valido, esegue il servizio prima di
  qualsiasi movimento, salvo emergenza di classe superiore;
- nessun `PASS` è ammesso su un tile `HARVEST`, `WATER`, `DIG`, `FEED` o
  `CARE` eseguibile dal worker;
- nessun movimento cross-cluster è ammesso se esiste un task locale di classe
  uguale o superiore;
- la continuazione verso il target sticky prevale sul ricalcolo globale;
- una oscillazione A→B→A dello stesso worker entro quattro step è una
  `route_thrashing_violation` e fallisce il gate tecnico.

## Invarianti congelati

- passthrough E18.2 esatto D0-D10;
- topologia `7-7-2`, 16 pascoli target e coop NW invariati;
- cap COW/SHEEP `16` invariato;
- Wheat reserve, safety buffer e pickup batch invariati;
- task generation e harvest maturity di V1 invariati;
- market acquisition, vendita, batching e liquidazione D29 invariati;
- sole feature proprie/pubbliche correnti; nessun nome, rating, seed, replay ID
  o memoria cross-episode;
- fail closed, zero holdout/final.

## Telemetria obbligatoria

Ogni record di dispatch deve includere step, worker, posizione, cluster,
inventario rilevante, task, età, classe, target, distanza, ownership,
continuazione/preemption e motivo della scelta. Gli aggregati minimi sono:

- move e productive action per giorno e cluster;
- `move_per_productive`;
- task latency p50/p90/max per kind;
- task aged oltre 6/12/24 step;
- preemption e cross-cluster transfer;
- route thrashing;
- PASS su tile actionable;
- harvest-ready backlog, unwatered backlog e weed exit;
- carrier utilization e pickup/drop round-trip;
- ownership changes e tempo idle per cluster.

## Gate sequenziali

### Gate A — integrità e lavoro, 14 match

Sette seed development E18 preregistrati, entrambi i seat, avversario E18.2.
Money è registrato ma non decide questo gate.

| KPI medio | Soglia V2 |
|---|---:|
| Move actions | `<= 3.584,6` (E18.2) |
| Productive actions | `>= 2.663` (`95%` di E18.2) |
| Move/productive | `<= 1,28` |
| Harvested units | `>= 571,3` (`95%` di E18.2) |
| Crop tile-days D21-D30 | `>= 449,3` (`95%` di E18.2) |
| Mean units/harvest | `>= 3,0` |
| Late weed tile-days | `<= 16,5` (`110%` di E18.2) |
| PASS su tile actionable | `0` |
| Route-thrashing violations | `0` |
| Topologia/fill | `7-7-2` e `16/16` in `14/14` |
| Perdite/errori/fallback | `0/0/0` |

Tutte le soglie sono congiunte; una media non compensa una violazione di
sicurezza o un episodio fuori topologia.

### Gate B — economia, soltanto dopo Gate A

- money medio `>= 100.000`;
- money medio non inferiore a E18.2 nello stesso diretto;
- almeno `10/14` delta matched non negativi;
- nessun episodio sotto il `90%` del controllo matched;
- zero regressioni di sicurezza, ledger e liquidazione.

### Gate C — robustezza development

Soltanto dopo A+B, eseguire il pool E18 congelato senza Antigravity obsoleto.
Richiedere:

- media non inferiore a E18.2 sul pool comune;
- nessuna regressione oltre `5%` per classe di avversario;
- medesimi gate di sicurezza e integrità;
- holdout/final ancora non consumati;
- nessun upload automatico.

## Test minimi prima del runner

1. ownership persistente oltre il cambio giorno;
2. task sticky non preemptato da task ordinario più vicino;
3. aging risolve un backlog senza violare la classe di sicurezza;
4. carrier Wheat/seed/animal resta compatibile con il task;
5. emergenza remota abilita cross-cluster e viene tracciata;
6. worker su tile actionable non emette `PASS` o movimento;
7. fixture anti-oscillazione A→B→A;
8. parità completa D0-D10 con E18.2;
9. topologia esatta `7-7-2` e cap 16;
10. determinismo a parità di seed, seat e osservazioni.

## File previsti per il build

- source: `src/agricola/strategy/codex/codex_e18_state_driven_772_v2.py`;
- config: `docs/model_specs/codex/e18/configs/CODEX_E18_4_STATE_DRIVEN_772_V2.json`;
- test: `docs/model_specs/codex/e18/tests/test_codex_e18_state_driven_772_v2.py`;
- runner: `docs/model_specs/codex/e18/tools/run_e18_4_state_driven_772_v2_gate.py`;
- artifact: `docs/model_specs/codex/e18/artifacts/derived/E18_4_STATE_DRIVEN_772_V2_DEV_GATE.json`;
- report: `docs/model_specs/codex/e18/reports/E18_4_STATE_DRIVEN_772_V2_DEV_GATE_REPORT_IT.md`;
- model spec: `docs/model_specs/codex/MODEL_SPEC_CODEX_E18_4_STATE_DRIVEN_772_V2.md`.

## Non-obiettivi

Non introdurre un nuovo selector avversario, non cambiare geometria, specie,
pricing, crop mix o activation day e non usare i replay Kaggle come fixture di
test. Questa iterazione deve isolare il valore causale del dispatcher.
