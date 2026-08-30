# MODEL_SPEC CODEX C2

```text
AGENT_ID: CODEX
STATUS: CANDIDATE C2 / PRE-REGISTERED / NOT TOURNAMENT TESTED
FOUNDATION: C2 CANDIDATE / NOT FROZEN
HYPOTHESIS_ID: CODEX-C2-LIFECYCLE-REALIZATION-V1
```

## 1. Scopo e ipotesi operativa

Questo MODEL_SPEC è un'ipotesi causale implementabile per il `MODEL_SPEC TOURNAMENT C2`. La tesi è che il principale limite R1 non fosse una carenza primaria di WATER, seed o cash, ma l'incapacità del dispatcher di trasformare capacità nominale in manutenzione persistente del working set.

L'intervento Codex è deliberatamente stretto:

```text
tile lifecycle state
    -> action eligibility corretta
    -> arbitration per deadline engine
    -> prevenzione delle perdite deterministiche
    -> recovery residuale delle tile LOST_WEED
```

Il target 17 è usato come `candidate operating region` configurabile. Non è un optimum, non è `C*` e non deriva da tuning del candidato.

## 2. Evidenza utilizzata

- E16 Stage A-R1 completato: 28/28 episodi, Stage B bloccato, `C*=NONE`.
- 5.804 tentativi crop-HARVEST prematuri, 655 validi, nessun'altra famiglia di failure HARVEST.
- Il predicato engine richiede `PLANT`, `yield_units > 0` e `day - planted_day >= first_yield_day`.
- 329 ingressi WEED osservati: 314 con precedente PLANT, 3 con precedente EMPTY, 12 unresolved.
- Zero azioni DIG in R1; una WEED nel working set era quindi un sink persistente.
- WATER execution HIGH tra 0,8898 e 0,9416 e continuity circa 0,96: WATER resta essenziale ma non è il bottleneck primario residuo.
- A07 HIGH/17 ha attainment corretto 0,4706 e median money 27.076: regione diagnostica interessante, non optimum.
- Routing e workforce intermittente amplificano il problema, ma non lo spiegano da soli: i gap restano anche a capacità piena.
- Seed stockout e market pacing non sono supportati come causa primaria.

## 3. Diagnosi causale prioritaria

```text
yield_units > 0 usato come readiness
    -> HARVEST prematuri / no-op
    -> slot e movimento sprecati
    -> minore capacità utile per WATER, HARVEST valido e PLANT

perdita crop o random EMPTY spawn
    -> LOST_WEED
    -> nessun DIG
    -> nessun replant
    -> gap del working set assorbente
```

Il meccanismo primario è `POLICY_REALIZATION`: eligibility e lifecycle non erano rappresentati nel dispatch. Il meccanismo secondario è l'amplificazione da routing/workforce intermittente.

## 4. Meccanismi non prioritari

| Sottosistema | Trattamento | Motivo |
|---|---|---|
| Crop mix | `UNCHANGED` | Mantiene WHEAT/STRAWBERRY/MELON 40/40/20 per isolare il lifecycle. |
| Workforce target | `UNCHANGED` | Conserva 10 hands; l'insufficienza nominale non è causa unica. |
| Routing | `UNCHANGED` | Nearest-task deterministico; contributo causale non identificato indipendentemente. |
| Market/cash | `UNCHANGED` | Floor 300 e pacing E16; secondari, non causa primaria. |
| Livestock | `NOT_CAUSALLY_PRIORITIZED` | Mantiene COW target 4 e pasture 5 senza nuova logica economica. |
| Land | `UNCHANGED` | Due quadranti; nessuna nuova espansione. |
| Random WEED prediction | `FORBIDDEN` | Il draw futuro non è osservabile. |

## 5. Feature C2 consumate

Il consumer mapping minimo è incorporato qui. Tutti i fallback sono fail-closed e non usano outcome futuri.

| feature_id | runtime source | calculation point | decision phase | consumer | fallback behavior |
|---|---|---|---|---|---|
| TMP-01 | `observation.step` | ingresso policy | pre-action | deadline lifespan e shutdown | non emettere azione dipendente da lifespan |
| TMP-02 | `observation.day` | ingresso policy | pre-action | maturity e calendario crop | non emettere HARVEST crop |
| TMP-03 | `observation.hour` | ingresso policy | pre-action | planting serviceable prima di EOD | non emettere PLANT |
| TMP-05 | `hour`, `turnsPerDay` | raccolta task | pre-action | gate PLANT tardivo | nessuna nuova PLANT |
| FRM-02 | `farm.tiles` | ogni decisione | pre-action snapshot | classificazione full working set | PASS per target non leggibile |
| FRM-03 | piano statico prime 17 `CROP_POSITIONS` | inizializzazione/config | pre-action | scope del classifier | posizione esterna `OUT_OF_SCOPE` |
| CRP-01 | valore tile nativo / `kind` | scansione working set | pre-action | classifier | diagnostic invalid, nessuna azione distruttiva |
| CRP-02 | `crop` + regole statiche C2 | scansione PLANT | pre-action | maturity/ongoing | WATER consentito se osservabile; HARVEST/DIG bloccati |
| CRP-03 | `planted_day` | scansione PLANT | pre-action | crop age | HARVEST bloccato |
| CRP-05 | `yield_units` | scansione PLANT | pre-action | readiness/retirement | HARVEST bloccato se mancante/non valido |
| CRP-06 | `watered_today` | scansione PLANT | pre-action | WATER need | stato mancante trattato come non servito |
| CRP-07 | `consecutive_unwatered` | scansione PLANT | pre-action | loss boundary EOD | priorità WATER conservativa |
| CRP-08 | `max_lifespan_step` | scansione PLANT | pre-action | decay/retirement | nessuna inferenza retirement dal solo crossing |
| CRP-09 | derivazione locale `classify_tile_lifecycle` | scansione working set | pre-action | task generation | diagnostic error fuori lifecycle |
| CRP-10 | kind/yield/age/rule | scansione PLANT | pre-action | eligibility HARVEST | HARVEST non emesso |
| CRP-11 | PLANT e non `watered_today` | scansione PLANT | pre-action | generazione WATER | WATER conservativo se flag assente |
| CRP-12 | care due e counter + 1 >= 2 | scansione PLANT | pre-action | coda WATER critica | assume critica se counter non valido |
| CRP-13 | step >= `max_lifespan_step` | scansione PLANT | pre-decay action phase | HARVEST urgente | nessuna promozione a retirement |
| CRP-17 | CRP-11/12/13 + lifecycle | arbitration | pre-action | ordinamento preventivo | ordine WATER-first conservativo |
| CRP-18 | count PLANT nel working set | market planning | pre-market | seed deficit / target tracking | nessuna espansione oltre target |
| WRK-01 | farmer/hands positions | arbitration | pre-action | nearest-task routing | PASS per posizione invalida |
| WRK-02 | `1 + len(hands)` | ingresso policy | pre-action | capacità corrente | task prioritari serviti per primi |
| INV-01 | `private.seeds` | scansione EMPTY | pre-action/pre-market | PLANT e BUY_SEED | PLANT bloccato senza seed |
| INV-02 | `private.shed` | unit/market planning | pre-action/pre-market | pickup, feed, sell | nessun ordine non coperto |
| INV-03 | `private.inventories` | unit planning | pre-action | carry/drop/place/feed | ritorno/drop conservativo |
| MKT-01 | market prices/inventory | market phase | pre-market | acquisti/vendite E16 | nessun ordine se quote invalida |
| MKT-03 | money meno floor policy | market phase | pre-market | protezione cash | ordine rifiutato sotto floor |

## 6. Regole decisionali

La classificazione locale è totale per il dominio engine valido:

```text
not in working set or tile == "LOCKED" -> OUT_OF_SCOPE
tile is None                           -> EMPTY_ASSIGNED
tile.kind == WEED                      -> LOST_WEED
invalid PLANT diagnostics              -> DIAGNOSTIC_ERROR

ready = PLANT and yield_units > 0
        and day - planted_day >= first_yield_day

retired = PLANT and crop.ongoing
          and yield_units == 0
          and max_lifespan_step >= 0

ready                                  -> HARVEST_READY
retired                                -> RETIREMENT_DUE
other valid PLANT                      -> GROWING
```

`max_lifespan_step >= 0` indica che la produzione ongoing finale è stata emessa; non basta da solo: readiness con yield positivo ha precedenza, e retirement richiede ongoing con yield zero.

## 7. Priorità e arbitration

Le code sono ordinate così:

1. `HARVEST_READY` con decay dovuto nell'engine step corrente;
2. WATER con `water_loss_at_eod_if_unserved`;
3. altri WATER dovuti nel giorno corrente;
4. HARVEST valido non immediatamente a rischio;
5. `RETIREMENT_DUE -> DIG` preventive clearance;
6. `LOST_WEED -> DIG` recovery residuale;
7. task livestock E16 invariati;
8. `EMPTY_ASSIGNED -> PLANT` soltanto se resta almeno una action phase successiva prima di EOD;
9. PASS.

Inventory carry, PLACE/FEED e drop restano precondizioni forti prima delle code generali. Ogni target è riservato a un solo worker per step. Multi-occupancy è ammessa dall'engine ma non è assunta come capacità doppia.

## 8. Tile lifecycle policy

| Stato | Azione policy | Divieto |
|---|---|---|
| `OUT_OF_SCOPE` | nessuna task crop | nessun PLANT/WATER/HARVEST/DIG crop |
| `EMPTY_ASSIGNED` | PLANT se seed, non shutdown e serviceable prima di EOD | nessuna PLANT tardiva non servibile |
| `GROWING` | WATER secondo rischio; attesa maturità | HARVEST vietato |
| `HARVEST_READY` | HARVEST, con precedenza al decay imminente | nessun readiness basato sul solo yield |
| `RETIREMENT_DUE` | DIG preventivo, poi replant | nessun WATER/attesa passiva |
| `LOST_WEED` | DIG recovery residuale, poi replant | nessun PLANT diretto su WEED |

## 9. WATER policy

Il livello HIGH E16 resta invariato; cambia soltanto l'ordinamento meccanico fra need già validi. Una PLANT non irrigata con `consecutive_unwatered + 1 >= 2` entra nella coda critica. Le altre PLANT non irrigate restano WATER-due ma sotto i decay-HARVEST immediati.

Una nuova PLANT nasce con counter 1. La policy non pianta nell'ultima action phase del giorno: deve esistere almeno una fase successiva per WATER. Questo è un vincolo di sicurezza configurabile, non un optimum.

## 10. HARVEST policy

HARVEST crop è emesso esclusivamente se `CRP-10 harvest_ready` è vero. Per WHEAT e MELON il yield iniziale non autorizza HARVEST prima della maturity. Per STRAWBERRY:

- HARVEST intermedio azzera yield e lascia `GROWING` con produzione futura;
- HARVEST finale azzera yield; con `max_lifespan_step >= 0` la tile diventa `RETIREMENT_DUE` al passo decisionale successivo.

## 11. PLANT e replant policy

Il piano stabile usa il pattern ripetuto WHEAT/STRAWBERRY/WHEAT/STRAWBERRY/MELON sulle prime 17 posizioni, ottenendo quota 7/7/3 senza riassegnare le posizioni già attive. EMPTY e post-HARVEST non-ongoing condividono la stessa regola PLANT. Seed disponibile e finestra WATER serviceable sono precondizioni.

## 12. DIG preventive/recovery policy

`DIG` ha due cause distinte:

- preventive: `RETIREMENT_DUE`, prima del decay a WEED;
- recovery: `LOST_WEED`, sotto tutte le azioni preventive vive.

DIG non sostituisce WATER o HARVEST e non viene emesso su una PLANT `GROWING`/`HARVEST_READY`.

## 13. Workforce e movement policy

Il target resta 10 hands più farmer. Il routing nearest-task e la reservation E16 restano invariati per evitare un secondo trattamento non identificabile. La sola modifica è la qualità e priorità delle task offerte al router. Se la workforce è insufficiente, il prefisso di coda preserva prima le perdite deterministiche più imminenti.

## 14. Inventory e market policy

Acquisto della seconda land, seed replenishment, hire renewal, COW/feed, vendite e floor 300 restano quelli E16. Il floor è una scelta policy, non una regola engine né un optimum. Il calcolo seed usa il target e il conteggio PLANT corrente; la presenza di WEED non genera acquisti infiniti perché il deficit include seed già posseduti.

## 15. Livestock policy

`NOT_CAUSALLY_PRIORITIZED`. Target COW 4 e pasture 5 restano invariati. FEED, CARE, HARVEST animale e fertilizer mantengono il comportamento condiviso. Il candidato non usa livestock per spiegare o mascherare il crop-attainment failure.

## 16. Failure containment

| Failure | Comportamento |
|---|---|
| diagnostics tile/crop mancanti | WATER conservativo se PLANT osservabile; nessun HARVEST o DIG distruttivo |
| feature temporaneamente indisponibile | task dipendente bloccata, altre code continuano |
| workforce insufficiente | serve il prefisso preventivo, nessuna promessa di serviceability |
| cash insufficiente | market order rifiutato sotto floor |
| seed insufficiente | nessun PLANT; BUY_SEED entro floor/slot |
| tile non serviceable | resta in coda al passo seguente; nessuna prediction futura |
| `LOST_WEED` | DIG residuale e replant successivo |
| movement contention | reservation per target; co-location engine non trattata come conflitto |
| action failure | stato ricalcolato dallo snapshot successivo, nessun optimistic state update |
| input top-level invalido | entrypoint del futuro runner deve fallire a PASS senza azioni market |

## 17. Expected mechanism changes

```text
5.804 premature HARVEST evidence
    -> CRP-10 exact readiness
    -> zero dispatch intenzionale prima di maturity
    -> meno action failure/no-op

329 observed WEED entries + zero DIG
    -> CRP-09 LOST_WEED
    -> recovery DIG residuale
    -> tile nuovamente EMPTY_ASSIGNED e replantabile

ongoing final production
    -> CRP-08 + CRP-09 RETIREMENT_DUE
    -> preventive DIG
    -> minore esposizione a lifespan WEED

new PLANT counter = 1
    -> CRP-12 + TMP-05
    -> niente PLANT nell'ultima phase
    -> minore perdita same-day
```

## 18. Previsioni verificabili preregistrate

Queste previsioni sono fissate prima di qualsiasi test economico del candidato:

1. `premature_harvest_count` intenzionale deve essere 0 quando i campi diagnostici sono validi.
2. `failed_action_count` e `no_op_action_count` crop devono diminuire materialmente rispetto al failure pattern R1 matched.
3. La persistenza di PLANT nel working set deve aumentare rispetto ad A07 R1; non è preregistrata una grandezza economica.
4. Ogni `LOST_WEED` osservata e serviceable deve diventare DIG-eligible; `lost_tile_persistence` deve diminuire.
5. La latenza recovery-DIG-to-replant deve essere inferiore alla persistenza right-censored R1; la replant latency complessiva è attesa sotto la mediana A07 di 22,5 step, ma dipende dal routing.
6. `productive_action_share` non deve peggiorare strutturalmente e dovrebbe aumentare eliminando task HARVEST impossibili.
7. WATER execution non deve perdere più di 0,05 e continuity più di 0,03 rispetto al matched HIGH/17 R1; il confronto resta paired e non assume equivalenza fra run.
8. `crop_target_attainment` target 17 è atteso maggiore di 0,4706; questa è una previsione falsificabile, non un optimum dichiarato.
9. `final_money` deve essere misurato senza previsione direzionale forte: la correzione meccanica può non monetizzarsi integralmente nel primo torneo.
10. DIG su PLANT viva deve avvenire soltanto per `RETIREMENT_DUE`; recovery e preventive clearance devono essere separabili nei log.

## 19. Metriche di verifica

| Metrica | Stato computabilità |
|---|---|
| final_money, completion | computabile dal summary |
| crop_target_attainment, active_crop_surface | computabile; dichiarare window/scope |
| watering_execution, watering_continuity | computabile con telemetry E16 v2 |
| premature_harvest_count | computabile da requested/applied action + maturity fields |
| failed_action_count, no_op_action_count | computabile dal ledger execution-aware |
| WEED/lost_tile_count | full-board richiede nuova snapshot; actor-local è lower bound |
| lost_tile_persistence | `NOT_CURRENTLY_COMPUTABLE` in modo completo con soli ledger R1 actor-local |
| replant_latency | computabile per transizioni/eventi osservati; right-censoring esplicito |
| movement_share, productive_action_share | computabile dal ledger con tassonomia versionata |
| workforce_utilization | computabile da actor events/capacity state |
| inventory e market activity | computabile da summary/market ledger |
| livestock contribution | computabile ma secondaria per questa ipotesi |

## 20. Assunzioni e limiti

- La schedule crop statica è parte dell'engine; nessun outcome futuro è letto.
- `max_lifespan_step >= 0` è usato solo insieme a ongoing e yield zero per retirement.
- Il target 17, il floor 300 e i controlli E16 sono policy/configuration, non Foundation optima.
- Il nearest-task routing può restare un collo di bottiglia; non viene risolto in questo candidato.
- Il gate PLANT tardivo garantisce solo una action phase disponibile, non che un worker completerà WATER.
- La recovery DIG riduce l'assorbimento ma non dimostra che tutte le tile saranno ripiantate rapidamente.
- Il candidato non è stato valutato economicamente prima del torneo.

## POST-TOURNAMENT REVIEW CONTRACT

Dopo il torneo locale a tre, Codex analizzerà i risultati ANTIGRAVITY, CODEX e COPILOT con lo stesso schema causale:

```text
RISULTATO
    -> MECCANISMO OSSERVATO
    -> DECISIONE MODEL_SPEC
    -> SPIEGAZIONE CAUSALE
    -> MODIFICA PROPOSTA
    -> PREVISIONE VERIFICABILE
```

La review non razionalizzerà vittoria o sconfitta e non userà il solo `final_money` come criterio di qualità. Verificherà separatamente correzione meccanica, persistence, action efficiency, WATER, attainment e monetizzazione.
