# MODEL_SPEC_COPILOT_C2.md

```text
AGENT_ID = COPILOT
STATO = CANDIDATE C2 / NOT FROZEN
TOURNAMENT_READY = YES
```

## 1. Scopo e ipotesi operativa

Il concorrente COPILOT costruisce una policy C2 centrata su un principio di prevenzione: evitare gli errori già diagnosticati in E16, prima di ricorrere a recovery e riassegnazione. La causa prioritaria non è la scarsità di semi o il timing di mercato, ma la combinazione di:

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

## 4. Meccanismi NON prioritari

- market timing: secondario rispetto alla pulizia e alla continuità del working set;
- seed scarcity: non è il collo di bottiglia principale in E16 R1;
- pure scale-up aggressiva: non produce beneficio se le azioni sono sprecate;
- livestock-first: fuori dal perimetro di questa versione per ridurre complessità non causale.

## 5. Feature C2 consumate

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

## 6. Regole decisionali

1. `HARVEST` è consentito solo se `harvest_ready == true`.
2. `WATER` è prioritario su tile PLANT non irrigate, specialmente quando `consecutive_unwatered + 1 >= 2`.
3. `DIG` è eseguito su `LOST_WEED` e su `RETIREMENT_DUE` per ripristinare il tile.
4. La policy preferisce la prevenzione rispetto alla recovery.
5. I tile vuoti o `EMPTY_ASSIGNED` possono essere riempiti con il crop preferito solo se ci sono semi disponibili.

## 7. Priorità / arbitration

```text
1. safety / irreversible loss prevention
2. harvest readiness validity
3. water maintenance
4. preventive DIG
5. replant / recovery
6. PASS
```

La priorità non usa una matrice avanzata: usa una gerarchia deterministica e localmente verificabile.

## 8. Tile lifecycle policy

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

## 9. WATER policy

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

## 10. HARVEST policy

```text
harvest_ready =
    tile.kind == PLANT
    AND yield_units > 0
    AND age >= first_yield_day
```

Niente `yield_units > 0` da solo. La policy rifiuta tutte le azioni `HARVEST` non conformi.

## 11. PLANT / replant policy

- se tile vuota e ci sono semi disponibili, plantare una crop preferita (`WHEAT` di default);
- il replant è secondario rispetto al mantenimento delle tile già attive;
- la policy non assume un optimum economico di mezzo ciclo; il comportamento è espressamente conservativo.

## 12. DIG preventive / recovery policy

```text
if tile lifecycle in {LOST_WEED, RETIREMENT_DUE}: DIG
```

La policy usa `DIG` come azione di ripristino/clearance, ma non come soluzione primaria ai problemi evitabili; il suo compito è contenere il danno.

## 13. Workforce / movement policy

La policy usa il worker locale in modo semplice e verificabile:

- se il worker è su tile in `LOST_WEED` o `RETIREMENT_DUE`, `DIG`;
- se il worker è su una crop da raccogliere, `HARVEST` solo se `harvest_ready`;
- se la crop è non irrigata, `WATER`;
- altrimenti `PASS`.

Non si introduce un routing complesso non supportato dall'evidenza.

## 14. Inventory / market policy

In questa fase la policy non introduce nuovi vincoli di mercato. Le transazioni di mercato sono lasciate invarianti, con il solo requisito di non distorcere la gestione operativa del working set.

## 15. Livestock policy

Non usata in questa versione C2. `UNCHANGED` / `DEFERRED` per ridurre la superficie del modello e rispettare il principio di Minimal Causal Intervention.

## 16. Failure containment

La policy contiene i fallimenti principali:

- missing/invalid diagnostic data -> default conservative PASS;
- temporarily unavailable feature -> fallback to `PASS` or strict rejection;
- insufficient workforce -> no speculative over-allocation;
- insufficient cash -> no forced expansion;
- insufficient seed/inventory -> no plant action;
- LOST_WEED -> DIG;
- action failure -> conservative no-op fallback.

## 17. Expected mechanism changes

```text
EVIDENZA
    ↓
premature HARVEST + WEED persistence
    ↓
feature `harvest_ready` + lifecycle classifier
    ↓
strict action gate + preventive DIG
    ↓
less failed/no-op HARVEST
    ↓
better productive action share
    ↓
higher crop persistence and target attainment
```

## 18. Previsioni verificabili

P1. `premature_harvest_count` deve diminuire materialmente.
P2. `maintained_productive_surface` deve migliorare relativamente al pattern E16.
P3. `WEED/lost_tile_count` deve diminuire.
P4. `replant_latency` deve diminuire dove la policy la prioritizza.
P5. `productive_action_share` non deve peggiorare strutturalmente.
P6. `watering_execution` e `watering_continuity` non devono regredire materialmente.
P7. `crop_target_attainment` deve migliorare rispetto al failure pattern E16.
P8. `final_money` viene misurato, non assunto.

## 19. Metriche di verifica

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

## 20. Assunzioni e limiti

- il modello non pretende di ottimizzare il rendimento assoluto su tutte le seed, ma di ridurre il failure pattern stabilito;
- l'intervallo di validità è limitato alla Foundation C2 e ai suoi invarianti;
- il modello non introduce threshold non supportati senza evidenza; i parametri restano configurabili e dichiarati come policy envelope;
- questa versione non sostituisce il torneo comune e non si fonda su dati del concorrente avversario.

## 21. POST-TOURNAMENT REVIEW CONTRACT

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
