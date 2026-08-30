# MODEL_SPEC_COPILOT_C2.md

```text
AGENT_ID = COPILOT
STATO = CANDIDATE C2 / PERFORMANCE ITERATION / FROZEN FOR NEXT TOURNAMENT
TOURNAMENT_READY = YES
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
2. impedire la perdita di tile in `LOST_WEED` o in `RETIREMENT_DUE` senza clearance preventiva.

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
3. `DIG` è eseguito su `LOST_WEED` e su `RETIREMENT_DUE` per ripristinare il tile.
4. La policy preferisce la prevenzione rispetto alla recovery.
5. I tile vuoti o `EMPTY_ASSIGNED` possono essere riempiti con il crop preferito solo se ci sono semi disponibili.
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

La classificazione è:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

Regole applicate:

- `tile is None` o `LOCKED` fuori working set -> `OUT_OF_SCOPE`;
- `tile is None` in posizione assegnata -> `EMPTY_ASSIGNED`;
- `WEED` -> `LOST_WEED`;
- `PLANT` + `yield_units > 0` + age >= `first_yield_day` -> `HARVEST_READY`;
- `PLANT` + non matured -> `GROWING`;
- `PLANT` + `yield_units == 0` + lifespan reached -> `RETIREMENT_DUE`.

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

- se tile vuota e ci sono semi disponibili, plantare una crop preferita (`WHEAT` di default);
- il replant è secondario rispetto al mantenimento delle tile già attive;
- al primo stato reale con zero seed, acquistare i semi WHEAT necessari a riempire tutte le 25 tile NW serviceable;
- non avviare PLANT dopo day 27, perché WHEAT non raggiunge il primo yield entro l'orizzonte rimanente;
- la policy non assume un optimum economico di mezzo ciclo; il comportamento è espressamente conservativo.

## 13. DIG preventive / recovery policy

```text
if tile lifecycle in {LOST_WEED, RETIREMENT_DUE}: DIG
```

La policy usa `DIG` come azione di ripristino/clearance, ma non come soluzione primaria ai problemi evitabili; il suo compito è contenere il danno.

## 14. Workforce / movement policy

La policy usa le 25 tile possedute del quadrante NW come `OWNED_SURFACE` e
`SERVICEABLE_SURFACE`; `ACTIVE_SURFACE` conta le tile PLANT e
`PRODUCTIVE_SURFACE` solo quelle che ricevono WATER, HARVEST e vendita effettiva.
Ogni turno assegna greedy un target distinto a farmer e hand, minimizzando la
distanza Manhattan dell'unità disponibile.

1. assegnare `HARVEST_READY`;
2. assegnare PLANT non irrigate;
3. assegnare `LOST_WEED` o `RETIREMENT_DUE`;
4. assegnare tile vuote per `PLANT`, limitate ai seed realmente disponibili;
5. altrimenti `PASS`.

Il worker emette un movimento cardinale verso il target se non è già sulla tile.
Questa è una limitata allocazione serviceable NW, non routing globale o
espansione territoriale.

## 15. Inventory / market policy

La policy usa il mercato solo per chiudere il loop produttivo minimo:

- `BUY_SEED WHEAT` colma il deficit tra semi disponibili e tutte le 25 tile NW, più la riserva, rispettando il capitale disponibile;
- `SELL` vende tutte le unità crop presenti nello shed;
- `HIRE` riporta la workforce a nove; `SELL`, `HIRE` e `BUY_SEED` sono troncati a dieci ordini, senza ordini speculativi;
- non sono introdotti market timing, espansione fondiaria o livestock.

## 16. Livestock policy

Non usata in questa versione C2. `UNCHANGED` / `DEFERRED` per ridurre la superficie del modello e rispettare il principio di Minimal Causal Intervention.

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
