# Codex C2 — Performance iteration

```text
AGENT_ID: CODEX
ITERATION_ID: CODEX-C2-MIN-YIELD-BEFORE-DECAY-V3.2
PHASE: VERIFY COMPLETE / MECHANISM FALSIFIED
DEFINE_FROZEN_BEFORE_BUILD: YES
SOURCE: C2 integrated retournament, 6 Codex player-episodes
```

## 1. Stato iniziale

Il retournament C2 è tecnicamente valido, ma Codex non soddisfa il criterio
economico del round successivo:

| Metrica | Valore corrente |
|---|---:|
| W-L-T | 4-2-0 |
| mean / median final money | $15.156 / $14.619 |
| sample std (`ddof=1`) | $1.300,92 |
| min / max | $14.267 / $17.691 |
| completion / error / fallback | 100% / 0 / 0 |
| target del prossimo round | mean final money > $23.000 |

La V2 ha risolto runtime, ciclo economico e scala iniziale. Non ha trasformato
la massa produttiva massima in sufficiente valore monetizzato.

## 2. Diagnosi quantitativa

Le misure seguenti derivano dai sei replay Codex congelati. I valori di action,
transizione e quantità sono medie per episodio.

### 2.1 Productive mass e continuità

| Livello | Definizione operativa | Valore |
|---|---|---:|
| `OWNED_SURFACE` | tile non-LOCKED nei due quadranti | 50 |
| `ACTIVE_SURFACE` | PLANT nel working set target 25 | mean 13,46; max globale 24; final mean 3,5 |
| `SERVICEABLE_SURFACE` | tile attive toccate da WATER almeno una volta nel giorno | coverage giornaliera mean 69,89%; minimo episodico medio 35,45% |
| `PRODUCTIVE_SURFACE` | working set che completa cicli con HARVEST effettivo | 142,83 HARVEST; active ≥20 soltanto 73,5/720 step (10,21%) |
| `MONETIZED_OUTPUT` | quantità effettivamente venduta al market | 182,17 unità; first revenue step 53 |

Ulteriori segnali di continuità:

- target inutilizzato medio: 11,54 tile su 25;
- WEED nel working set: mean 2,63, massimo episodico medio 5,83;
- DIG: 67; latenza media replant dopo perdita/raccolta: 37,15 step;
- PLANT: 183,5; WATER effettive: 396,3;
- cash minimo medio episodico $332,33; 113,17 step sotto $500;
- inventory totale mean 7,74, massimo episodico medio 24,17; shed massimo
  medio 20,67: non emerge un backlog di vendita dominante;
- workforce mean 8,62, massimo 9;
- MOVE 4.931,17 su circa 6.201 unit action, share 79,52%;
- pasture max 4,83, COW max 4; BUY_PRODUCT feed 50,33 unità;
- la condizione `active >= 20 && cash >= 1500` è vera soltanto 10 step medi,
  ma quattro COW vengono comunque acquistate: il livestock esiste, non è il
  failure runtime osservato.

### 2.2 Yield, churn e valore monetizzato

| Crop/prodotto | PLANT | HARVEST | Unità raccolte | Unità/harvest | Unità vendute | Valore lordo SELL osservato |
|---|---:|---:|---:|---:|---:|---:|
| WHEAT | 158,0 | 103,83 | 112,5 | **1,084** | 95,5 | **$2.832** |
| STRAWBERRY | 10,17 | 25,17 | 25,17 | 1,000 | 25,17 | $5.051 |
| MELON | 15,33 | 9,17 | 44,5 | **4,85** | 44,5 | **$11.172** |
| MILK | — | 4,67 | 9,67 | 2,07 | 8,17 | $2.506 |
| FERTILIZER | — | — | — | — | 8,83 | $877 |

Il WHEAT costituisce circa il 62% delle PLANT ma soltanto circa il 12,6% del
valore lordo SELL misurato. La prima latenza HARVEST WHEAT è 42,0 step, coerente
con la raccolta alla prima maturity legale (day 2); MELON e STRAWBERRY arrivano
rispettivamente a circa 236 step.

La regola engine permette al WHEAT non-ongoing di accumulare yield con WATER
fra day 2 e `max_yield_day=4`. La V2 lo raccoglie appena legalmente maturo,
tipicamente a una sola unità, rimuove la tile e riapre il ciclo seed→route→PLANT.

## 3. Collo di bottiglia dominante

| Categoria | Valutazione | Evidenza |
|---|---|---|
| `CAPACITY_LIMIT` | non dominante | max active 24 su target 25 dimostra capacità di picco |
| `SERVICE_LIMIT` | secondario forte | water coverage 69,89%, WEED 2,63, active mean solo 13,46 |
| `ROUTING_LIMIT` | secondario forte | MOVE share 79,52%, replant 37,15 step |
| `BIOLOGICAL_LIMIT` | **dominante** | WHEAT raccolto a 1,084 unità contro una finestra di accumulo fino a day 4 |
| `CAPITAL_LIMIT` | secondario | cash vicino al floor, ma first revenue 53 e closure completa |
| `MARKET_LIMIT` | non dominante | SELL frequenti e inventory contenuta; manca valore per ciclo, non accesso al market |
| `WORKFORCE_LIMIT` | non primario | workforce 9 raggiunta; il churn ne consuma la capacità |
| `LAND_UTILIZATION_LIMIT` | secondario forte | 50 tile possedute, soltanto 13,46 crop attive medie |
| `LIVESTOCK_LIMIT` | secondario | quattro COW attive ma contributo MILK contenuto |

Il meccanismo dominante è quindi la bassa **yield density per ciclo servito**:
la policy confonde readiness legale con timing economicamente efficiente.

## 4. Ipotesi causale

```text
HYPOTHESIS_ID: CODEX-C2-YIELD-DENSITY-CONTINUITY-V3

OBSERVED_PROBLEM:
Codex raggiunge 24 crop ma chiude a $15.156 mean; 158 PLANT WHEAT e 103,83
HARVEST producono soltanto 112,5 unità, mentre churn e MOVE assorbono capacità.

EVIDENCE:
WHEAT yield/harvest 1,084; MOVE share 79,52%; replant latency 37,15 step;
WHEAT gross SELL ~$2.832 contro MELON ~$11.172 con sole 9,17 harvest.

CAUSAL_MECHANISM:
HARVEST alla first_yield_day rimuove WHEAT prima dell'accumulo di yield fino
al max_yield_day. Ogni raccolto prematuro genera nuovo seed cost, viaggio,
PLANT e WATER di bootstrap. Il churn abbassa continuità e monetized output.

MODEL_CHANGE:
Separare maturity legale da economic harvest readiness; mantenere WHEAT fino
al day 4 e irrigarlo prima della raccolta finale. Conservare un bootstrap
60/20/20 per liquidità, poi usare un mix full 40/20/40
WHEAT/STRAWBERRY/MELON. Usare l'economic harvest day nel terminal horizon.

EXPECTED_INTERMEDIATE_EFFECT:
WHEAT yield/harvest >= 3; meno PLANT/replant WHEAT; maggiore quota MELON;
meno churn, migliore service continuity e minore MOVE share.

EXPECTED_ECONOMIC_EFFECT:
Più unità e valore venduti per seed e per attraversamento; final money UP,
con target comune mean > $23.000.

FALSIFICATION_CONDITION:
Il meccanismo è falsificato se il preflight P0/P1 non realizza WHEAT
yield/harvest >= 3 o un ciclo MELON, oppure introduce error/fallback. L'ipotesi
economica è falsificata nel prossimo tournament se mean final money <= $23.000,
anche se test e metriche intermedie passano.
```

## 5. Revisione del MODEL_SPEC prevista

La V3 distinguerà esplicitamente:

- `ENGINE_HARVEST_ELIGIBLE`: action legalmente valida;
- `ECONOMIC_HARVEST_READY`: yield/timing coerente col valore per ciclo;
- piano `BOOTSTRAP` 60/20/20 e piano `FULL` 40/20/40;
- horizon basato sul giorno economico di raccolta, non sulla prima eligibility;
- `YIELD_ACCUMULATING` come stato vivo da mantenere e irrigare.

Non cambiano target 25, due quadranti, workforce 5→8 hands, lifecycle WEED,
floor 300, gate land e failure containment. Questo mantiene isolabile
l'ipotesi yield-density/continuity.

### 5.1 Addendum DEFINE V3.1 congelato prima della correzione

Il primo preflight meccanico valido della V3 ha realizzato P0/P1, zero
error/fallback e il ciclo MELON, ma ha falsificato la previsione WHEAT:
`9 unità / 4 HARVEST = 2,25` in entrambi i seat. L'ispezione delle regole engine
conferma che WATER aggiunge yield WHEAT soltanto nella finestra age 2..4.

```text
HYPOTHESIS_AMENDMENT_ID: CODEX-C2-YIELD-WINDOW-SERVICE-V3.1
OBSERVED_PROBLEM: economic day 4 senza precedenza WATER produce 2,25, non >=3
CAUSAL_MECHANISM: WATER di WHEAT YIELD_ACCUMULATING resta nella coda ordinaria
MODEL_CHANGE: coda yield-window WATER dopo critical WATER e prima di HARVEST
EXPECTED_INTERMEDIATE_EFFECT: WHEAT yield/harvest >=3 in P0 e P1
FALSIFICATION_CONDITION: stesso preflight neutrale resta sotto 3 o perde ciclo MELON
```

Questo è un fix di realizzazione del meccanismo, non una stima di performance:
seed, durata, mix, target, floor, workforce, land e livestock restano congelati.
Il preflight V3 fallito è preservato separatamente e non viene reinterpretato.

### 5.2 Addendum DEFINE V3.2 congelato prima della correzione

La telemetria evento-per-evento della V3.1 mostra che le WHEAT raggiungono
yield 3 al day 3 e spesso 4 al day 4. Il WATER massimizzante su tutte le tile
ritarda però il routing HARVEST; dal day 5 il decay sottrae una unità ogni due
step. Gli HARVEST effettivi diventano `[2, 1, 4, 2]` in entrambi i seat.

```text
HYPOTHESIS_AMENDMENT_ID: CODEX-C2-MIN-YIELD-BEFORE-DECAY-V3.2
OBSERVED_PROBLEM: massimizzare yield prima di HARVEST espone al decay di routing
CAUSAL_MECHANISM: il costo temporale del WATER finale supera il bonus marginale
MODEL_CHANGE: WHEAT economic minimum yield=3; WATER finale solo sotto 3,
              HARVEST immediato a day 4 se yield>=3
EXPECTED_INTERMEDIATE_EFFECT: WHEAT yield/harvest >=3 in P0 e P1
FALSIFICATION_CONDITION: stesso preflight resta sotto 3 o perde ciclo MELON
```

Anche questo addendum lascia invariati seed, durata e tutti i gate economici.

## 6. Modifiche implementate

Tutte le modifiche sono circoscritte al candidato Codex:

- `MODEL_SPEC_CODEX_C2.md`: stati engine/economici separati, piano bootstrap
  60/20/20, piano full 40/20/40, horizon economico e arbitration yield-window;
- `CODEX_C2_CONFIG.json`: schema `model_spec_c2.codex.v2`, pattern bootstrap
  esplicito e pattern full con 40% MELON;
- `codex_c2.py`: `YIELD_ACCUMULATING`, economic harvest day, selezione del
  piano per fase, WATER yield-window/completion e soglia WHEAT 3;
- `test_codex_c2_candidate.py`: test dei due mix, accumulo, soglia economica,
  WATER finale e priorità yield-window;
- `preflight_codex_c2.py`: telemetria causale su HARVEST/SELL effettivi,
  yield per crop, WATER coverage, MOVE share ed eventi WHEAT.

Non sono stati modificati runner/protocollo comune, seed tournament, candidati
altrui, Foundation C2 o submission Kaggle.

## 7. Previsioni preregistrate

```text
EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: > 23000

METRIC_A: WHEAT units per successful HARVEST
CURRENT_VALUE: 1.084
EXPECTED_VALUE_OR_DIRECTION: >= 3.0 nel preflight meccanico P0/P1
WHY_CAUSAL: misura direttamente il differimento dalla first maturity al day 4

METRIC_B: WHEAT PLANT churn
CURRENT_VALUE: 158.0 PLANT/episodio tournament
EXPECTED_VALUE_OR_DIRECTION: DOWN; meno cicli seed→PLANT per tile
WHY_CAUSAL: ogni raccolto più denso deve richiedere meno replant a parità di output

METRIC_C: service continuity
CURRENT_VALUE: daily WATER coverage 69.89%; MOVE share 79.52%
EXPECTED_VALUE_OR_DIRECTION: WATER coverage UP, MOVE share DOWN
WHY_CAUSAL: il minor churn libera workforce per mantenimento invece di routing

METRIC_D: high-value crop realization
CURRENT_VALUE: full target mix MELON 20%; 44.5 unità vendute/episodio
EXPECTED_VALUE_OR_DIRECTION: full target mix MELON 40%; almeno un ciclo MELON
osservato nel preflight
WHY_CAUSAL: verifica che il valore potenziale non resti soltanto in configurazione
```

## 8. Preflight P0/P1

Protocollo meccanico: seed neutrale preregistrato `26083001`, 360 step,
avversario inerte, stesso candidato eseguito una volta in P0 e una in P1. Non
è un torneo privato e il final cash non è usato come stima del prossimo round.

Tre artifact preservano la catena di falsificazione/correzione:

| Build | P0 WHEAT unit/harvest | P1 | Esito |
|---|---:|---:|---|
| V3 timing + final WATER | 2,25 | 2,25 | FAIL metrica A |
| V3.1 yield-window priority | 2,25 | 2,25 | FAIL metrica A |
| V3.2 min-yield prima del decay | 2,17 | 2,50 | FAIL metrica A |

V3.2 realizza comunque i controlli tecnici e il ciclo high-value:

| Metrica V3.2 | P0 | P1 |
|---|---:|---:|
| status / step | DONE / 360 | DONE / 360 |
| error / fallback | 0 / 0 | 0 / 0 |
| own-farm binding | verificato | verificato |
| max active / quadranti | 22 / 2 | 22 / 2 |
| MELON HARVEST / unità | 6 / 28 | 7 / 33 |
| MELON SELL drawdown | 24 | 33 |
| daily WATER coverage | 75,02% | 78,33% |
| MOVE share | 58,86% | 56,04% |

La metrica D passa e MOVE resta sotto il baseline tournament 79,52%; la
coverage WATER è sopra 69,89% soltanto in questa misura aggregata. La metrica
A essenziale fallisce. Gli eventi mostrano crop a yield 3 al day 3, ma la wave
sincronizzata non viene interamente raccolta prima del decay: gli HARVEST P0
sono `[3, 3, 2, 1, 3, 1]`, quelli P1 `[3, 3, 2, 1, 3, 3]`.

```text
P0_REAL_ENGINE_EXECUTION: PASS
P1_REAL_ENGINE_EXECUTION: PASS
ERROR_FALLBACK_CONTROL: PASS
HIGH_VALUE_CYCLE: PASS
PREREGISTERED_CORE_MECHANISM: FAIL
```

## 9. Test

- test candidato: `22 passed`;
- suite repository: `180 passed`;
- Ruff mirato su policy, test e preflight: PASS;
- `git diff --check`: PASS (soli warning informativi LF/CRLF);
- preflight real-engine V3.2: esecuzione PASS, gate meccanico FAIL.

Il warning pytest sulla `.pytest_cache` non riguarda il candidato: la sandbox
non consente la creazione della cache, mentre tutti i test vengono eseguiti.

## 10. Limiti residui

- Il target $23k resta preregistrato e non dimostrato.
- Il limite ora osservato è una wave WHEAT sincronizzata: il routing verso
  HARVEST non svuota tutte le tile prima del decay day 5.
- Una prossima iterazione dovrà formulare prima del BUILD un'ipotesi distinta
  su staggering/pre-positioning o riduzione del picco di servizio; non viene
  improvvisata su questo seed.
- Più MELON immobilizza capitale e il preflight breve non attiva le COW.
- Final cash P0/P1 del preflight non è performance evidence comparabile.
- Nessun tournament comune è stato eseguito.

## 11. Freeze degli artifact

Baseline prima del BUILD:

```text
POLICY_SHA256: 9D67AA44B6DAE89A2A05619A77B280E3A6D8B6ABCB8A6C67A3F3714921D2BC3A
CONFIG_SHA256: 7288281403E8CEBE5E0F941AD6F4A6E8A28ACDF0E5843F1F5CD27454DD4F4357
MODEL_SPEC_SHA256: E664788936E3AED9A33D02D76C78AC9B35735FE0F216D4A6431D07854977DF8F
```

Build V3.2 verificato:

```text
POLICY_SHA256: 99754AE47D6CD8A4FA249BD3B97B50BB9E695BB2CB8EEE3E3F72448988616D09
CONFIG_SHA256: 6B85154DE327F9E7B87F241D1D6A65355C1277B9D1FD8B0CFACF1B71DF462F1B
MODEL_SPEC_SHA256: 4B2DA55E1FF37BC3352E5C49519688252188A06B593BEA47467ED12F72F2F737
PREFLIGHT_RUNNER_SHA256: 225CFDD43898EB1702DE812820F2385152D70EB8689D4F5D2506492147882966
TARGETED_TEST_SHA256: AC610D66BBF6A8BDF3F7EC4117851DBC73B3BA4066C8F9325B8AB6DC2598D847
```

Evidenza:

- `CODEX_C2_V3_PREFLIGHT.json`: primo FAIL timing/final WATER;
- `CODEX_C2_V3_1_PREFLIGHT.json`: FAIL dopo yield-window priority;
- `CODEX_C2_V3_2_PREFLIGHT.json`: verifica finale, meccanismo FAIL.

## 12. Stato finale

Il BUILD è implementato e tecnicamente eseguibile, ma il requisito 7 del gate
`TOURNAMENT_READY` non è soddisfatto: l'effetto intermedio essenziale
preregistrato non è osservabile. Dichiarare readiness sarebbe contrario al
prompt comune.

```text
C2_PERFORMANCE_ITERATION_COMPLETE: YES
TOURNAMENT_READY: NO
TARGET_MEAN_FINAL_MONEY: >23000
```
