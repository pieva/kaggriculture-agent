# MODEL_SPEC CODEX C2 — Staggered harvest service V4

```text
AGENT_ID: CODEX
BUILD_ID: CODEX-C2-STAGGERED-HARVEST-SERVICE-V4
STATUS: VERIFY COMPLETE / CORE MECHANISM CONFIRMED / TOURNAMENT READY
HYPOTHESIS_ID: CODEX-C2-STAGGERED-HARVEST-SERVICE-V4
TARGET_MEAN_FINAL_MONEY: >23000
```

## 1. Tesi causale

La V3.2 dimostra che la WHEAT raggiunge yield 3, ma non che la policy riesca a
raccoglierla prima del decay. Nove tile della stessa coorte diventano ready
insieme; soltanto due sono completate nella finestra utile di 24 step.

```text
PLANT burst day 0
    -> maturity sincronizzata day 4
    -> 9 HARVEST simultaneamente ready
    -> routing/inventory service backlog
    -> 7/9 deadline miss
    -> decay di yield già prodotto
    -> monetized output insufficiente
```

La V4 distribuisce il carico alla sorgente: ammette al massimo due nuove PLANT
WHEAT effettive per giorno, pari alla capacità on-time osservata. Non attende
più yield e non aumenta la capacità nominale.

## 2. Evidenza congelata

Preflight V3.2, seed neutrale `26083001`, identico in P0/P1 sulla prima wave:

| Metrica | Valore |
|---|---:|
| WHEAT a yield 3 entro day 3 | 9 |
| economic-ready step | 96 |
| decay start step | 120 |
| finestra utile | 24 step |
| completion step | 108, 117, 123, 125 |
| completion prima del decay | 2/9 |
| deadline miss | 7/9 = 77,78% |
| ready-to-completed latency | 12, 21, 27, 29 step |
| HARVEST yield>=3 | P0 50,00%; P1 66,67% |

La resa biologica esiste prima della deadline. Il limite dominante è il
`SERVICE_PEAK`, amplificato da routing e inventory handling; non è una nuova
evidenza a favore di ulteriore attesa biologica.

## 3. Capacità economica

| Livello | Definizione V4 |
|---|---|
| `OWNED_SURFACE` | tile non-LOCKED nei quadranti acquistati |
| `ACTIVE_SURFACE` | PLANT osservate nel working set |
| `SERVICEABLE_SURFACE` | PLANT con domanda temporale entro la capacità della finestra |
| `PRODUCTIVE_SURFACE` | PLANT che completano HARVEST prima del decay distruttivo |
| `MONETIZED_OUTPUT` | output depositato e venduto con effetto osservato |

Una tile biologicamente pronta non genera valore se il sistema non dispone
della capacità temporale e logistica per raccoglierla prima del decadimento.

## 4. Macchina a stati harvest locale

Gli stati non modificano la Foundation C2 e derivano soltanto dallo snapshot:

| Stato | Predicato | Consumer |
|---|---|---|
| `ENGINE_HARVEST_ELIGIBLE` | PLANT, yield>0, age>=first_yield_day | blocco di legalità |
| `ECONOMIC_HARVEST_READY` | engine eligible e age>=economic_harvest_day | accesso al servizio |
| `HARVEST_SERVICE_PENDING` | economic ready, completion non ancora osservata | coda HARVEST |
| `HARVEST_DEADLINE_RISK` | service pending e step vicino/oltre `max_lifespan_step` | urgenza e telemetry miss |
| `HARVEST_COMPLETED` | transizione HARVEST con yield ridotto/tile rimossa | throughput e monetization |

Gli stati tile persistenti restano:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
YIELD_ACCUMULATING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

Per WHEAT: first yield day 2, economic day 4, soglia pre-harvest 3,
`max_lifespan_step=(planted_day+5)*turnsPerDay`. `HARVEST_DEADLINE_RISK` non
autorizza un HARVEST illegale e non sostituisce la loss-boundary WATER.

## 5. Trattamento V4: load shaping

```text
MAX_WHEAT_PLANTS_PER_DAY: 2
```

Regola:

1. contare nel working set le WHEAT osservate con `planted_day == day`;
2. calcolare `remaining_daily_slots = max(0, 2 - observed_today)`;
3. generare al massimo quel numero di task `PLANT WHEAT` nello step;
4. continuare a generare normalmente PLANT STRAWBERRY/MELON;
5. al successivo snapshot il conteggio osservato sostituisce ogni prenotazione;
6. WATER, HARVEST, DIG e crop già vive non sono mai bloccati dal cap.

Il cap è un limite di coorte, non una riduzione del target: le posizioni WHEAT
vuote vengono riempite nei giorni successivi. Il valore 2 è preregistrato dalla
capacità V3.2 di due completion prima del decay, non da ricerca parametrica.

## 6. Parametri invariati

| Parametro | Valore |
|---|---:|
| bootstrap/full crop target | 10 / 25 |
| bootstrap mix | 60/20/20 WHEAT/STRAWBERRY/MELON |
| full mix | 40/20/40 |
| bootstrap/full workforce | 5 / 8 hands |
| land gate | active>=8, cash>=1.600 |
| pasture/COW cap | 5 / 4 |
| livestock gate | active>=80%, cash>=1.500 |
| cash floor | 300 |
| quadrants | 2 |
| crop horizon margin | 24 step |

Layout, routing sticky, reservation, inventory handling, market, lifecycle,
terminal horizon e soglie biologiche V3.2 restano invariati per isolare lo
staggering.

## 7. Arbitration invariata

1. HARVEST con decay già iniziato;
2. WATER con perdita EOD imminente;
3. WATER nella finestra `YIELD_ACCUMULATING`;
4. WATER di completamento sotto soglia economica;
5. HARVEST economicamente ready;
6. WATER ordinario;
7. DIG retirement;
8. DIG recovery;
9. PLANT soggetta al solo cap di coorte WHEAT;
10. task livestock/pasture.

## 8. Consumer mapping V4

| Feature | Calcolo | Consumer | Fallback |
|---|---|---|---|
| `day`, `planted_day`, crop | conteggio coorte ogni decisione | gate PLANT WHEAT | nessuna nuova WHEAT se diagnostica invalida |
| `yield_units`, crop age | snapshot tile | economic readiness | HARVEST bloccato se invalido |
| `max_lifespan_step`, step | snapshot tile | risk/miss telemetry | nessuna inferenza deadline |
| worker positions | snapshot farm | routing esistente | PASS su posizione invalida |
| tile transition | snapshot successivo | HARVEST_COMPLETED | evento non contato se ambiguo |

Tutti gli altri consumer/fallback V3.2, own-player binding, factory isolata e
SAFE_PASS restano invariati.

## 9. Previsioni preregistrate

```text
EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: >23000

MAX_WHEAT_PLANT_COHORT_PER_DAY:
current = 9
expected <= 2 in P0 and P1

PEAK_SIMULTANEOUS_WHEAT_ECONOMIC_READY:
current = 9
expected <= 4 in P0 and P1

WHEAT_HARVEST_DEADLINE_MISS_RATE:
current = 77.78%
expected <= 25% in P0 and P1

FRACTION_WHEAT_HARVESTED_AT_YIELD_GE_3:
current P0 = 50.00%
current P1 = 66.67%
expected >= 80% in P0 and P1

HIGH_VALUE_REALIZATION:
expected = effective MELON HARVEST and SELL in P0 and P1
```

La V4 è falsificata se una sola metrica essenziale fallisce in un seat, se il
ciclo MELON scompare o se compaiono errori/fallback. Final cash del preflight
non dimostra il target economico.

## 10. Failure containment e gate

`TOURNAMENT_READY: YES` richiede:

- P0/P1 `DONE`, own-player binding, 0 error/fallback;
- cap coorte, peak ready, miss rate e fraction yield tutti PASS;
- ciclo MELON effettivo;
- test Codex e repository PASS;
- Ruff e `git diff --check` PASS;
- nessun blocker noto.

## 11. Limiti

- Lo staggering può ritardare l'attainment nominale senza ridurne il target.
- La distanza worker-target V3.2 non è disponibile; la latenza è il proxy.
- La capacità osservata 2 potrebbe non generalizzare al torneo: sarà falsificata
  dal protocollo comune, non ottimizzata nel preflight.
- Nessun torneo comune, seed ufficiale, Kaggle, submission o C3 è autorizzato.

## 12. Esito VERIFY V4

Il preflight neutrale P0/P1 completa 360 step con own-player binding e zero
error/fallback. In entrambi i seat:

- coorte WHEAT massima 2;
- peak simultaneo economic-ready 2;
- deadline miss 0/15;
- HARVEST WHEAT yield>=3: 15/15;
- ciclo MELON con HARVEST e SELL effettivi.

```text
PREREGISTERED_CORE_MECHANISM: PASS
TOURNAMENT_READY: YES
TOURNAMENT_EXECUTED: NO
```
