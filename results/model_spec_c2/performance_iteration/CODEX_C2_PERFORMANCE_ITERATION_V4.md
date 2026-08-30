# Codex C2 — Performance iteration V4

```text
AGENT_ID: CODEX
ITERATION_ID: CODEX-C2-STAGGERED-HARVEST-SERVICE-V4
PHASE: DEFINE FROZEN / BUILD COMPLETE / VERIFY PASS / FROZEN
DEFINE_FROZEN_BEFORE_BUILD: YES
SOURCE: frozen V3.2 neutral preflight, seed 26083001
```

## 1. Evidenza V3.2

V3.2 ha separato maturity engine e readiness economica, ma non ha trasformato
in tempo utile tutte le WHEAT mature:

| Metrica | P0 | P1 |
|---|---:|---:|
| esecuzione / error / fallback | DONE / 0 / 0 | DONE / 0 / 0 |
| WHEAT yield/harvest | 2,17 | 2,50 |
| WHEAT HARVEST yield >=3 | 3/6 (50,00%) | 4/6 (66,67%) |
| MELON cycle | PASS | PASS |
| max active | 22 | 22 |
| WATER coverage | 75,02% | 78,33% |
| MOVE share | 58,86% | 56,04% |

Nove WHEAT della coorte `planted_day=0` risultano irrigate a yield 3 entro il
day 3 in entrambi i seat. La resa biologica desiderata è quindi presente prima
della scadenza; è la sua conversione in HARVEST a fallire.

## 2. Diagnosi del service peak

Per la coorte day 0:

```text
ECONOMIC_READY_STEP: 96 (day 4)
DECAY_START_STEP: 120 (day 5)
USEFUL_SERVICE_WINDOW: 24 step
SIMULTANEOUS_READY_WHEAT: 9
HARVEST_COMPLETED_BEFORE_DECAY: 2
OBSERVED_ON_TIME_SERVICE_CAPACITY: 2 tile / window
DEADLINE_MISS: 7/9 = 77,78%
COMPLETION_STEPS: 108, 117, 123, 125
READY_TO_COMPLETED_LATENCY: 12, 21, 27, 29 step
```

La lettura dei fattori richiesti è:

| Fattore | Diagnosi congelata |
|---|---|
| `HARVEST_WAVE_SYNCHRONIZATION` | dominante: nove WHEAT diventano economicamente ready insieme |
| `SERVICE_PEAK` | dominante: domanda 9 contro capacità osservata 2 entro 24 step |
| `WORKER_PREPOSITIONING` | non misurato direttamente; latenza minima 12 è proxy di assenza dal target |
| `ROUTING_DISTANCE_AT_HARVEST` | non disponibile come distanza esatta; latenze 12–29 dimostrano costo logistico materiale |
| `HARVEST_DEADLINE` | hard boundary osservabile a step 120 |
| `DECAY_EXPOSURE` | 77,78% non raccolto prima del primo decay; output tardivo scende a 2/1 |
| `PLANT_STAGGERING` | assente: nove WHEAT sono concentrate nel day 0 |
| `SERVICE_LOAD_DISTRIBUTION` | fortemente impulsiva, non allineata alla capacità temporale osservata |

Il numero nominale di worker non è il collo di bottiglia isolato: il sistema
ha fino a nove attori ma inventory, movimento e altre task impediscono nove
completion entro la finestra. Aumentare workforce o attendere altro yield
cambierebbe più meccanismi e non è giustificato da questa evidenza.

## 3. Ipotesi V4

```text
HYPOTHESIS_ID: CODEX-C2-STAGGERED-HARVEST-SERVICE-V4

OBSERVED_PROBLEM:
Una coorte di 9 WHEAT economicamente ready genera soltanto 2 HARVEST prima del
decay; 7/9 tile mancano la deadline e gli HARVEST tardivi perdono yield.

EVIDENCE:
Le nove tile raggiungono yield 3 entro day 3; ready step 96, decay step 120;
completion step 108/117/123/125; miss rate 77,78%; yield>=3 soltanto 50,00%
in P0 e 66,67% in P1.

CAUSAL_MECHANISM:
Il burst PLANT day 0 sincronizza la maturity. La domanda istantanea di nove
HARVEST supera la capacità logistica osservata di due completion nella finestra
utile. Il backlog attraversa la deadline e il decay distrugge yield già creato.

MODEL_CHANGE:
Limitare a due le nuove PLANT WHEAT effettive per giorno, pari alla capacità
on-time osservata. Non cambiare target, layout, workforce, land, livestock,
cash floor, market o readiness biologica V3.2.

EXPECTED_INTERMEDIATE_EFFECT:
Coorte WHEAT giornaliera <=2; peak simultaneo economic-ready <=4; deadline miss
rate <=25%; almeno 80% degli HARVEST WHEAT con yield>=3 in ciascun seat.

EXPECTED_ECONOMIC_EFFECT:
Final Money UP; target tournament mean > $23.000, da verificare esclusivamente
nel futuro protocollo comune.

FALSIFICATION_CONDITION:
La V4 è falsificata se P0 o P1 supera peak ready 4, supera deadline miss 25%,
scende sotto 80% HARVEST WHEAT a yield>=3, perde il ciclo MELON o introduce
error/fallback. Il final cash del preflight non prova il target economico.
```

## 4. Metriche preregistrate

```text
METRIC_A: PEAK_SIMULTANEOUS_WHEAT_ECONOMIC_READY
CURRENT_VALUE: 9
EXPECTED_VALUE: <=4 in P0 e P1
WHY_CAUSAL: misura direttamente la riduzione del service peak

METRIC_B: WHEAT_HARVEST_DEADLINE_MISS_RATE
CURRENT_VALUE: 7/9 = 77.78% sulla prima wave V3.2
EXPECTED_VALUE: <=25% in P0 e P1
WHY_CAUSAL: misura la conversione di readiness in completion prima del decay

METRIC_C: FRACTION_WHEAT_HARVESTED_AT_YIELD_GE_3
CURRENT_VALUE: P0 50.00%; P1 66.67%
EXPECTED_VALUE: >=80% in P0 e P1
WHY_CAUSAL: verifica che lo staggering preservi yield monetizzabile

METRIC_D: MAX_WHEAT_PLANT_COHORT_PER_DAY
CURRENT_VALUE: 9
EXPECTED_VALUE: <=2 in P0 e P1
WHY_CAUSAL: verifica la realizzazione esatta del trattamento

EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: >23000
```

## 5. MODEL_SPEC revision

Il MODEL_SPEC V4 è stato aggiornato prima del codice con:

- macchina a stati `ENGINE_HARVEST_ELIGIBLE` → `ECONOMIC_HARVEST_READY` →
  `HARVEST_SERVICE_PENDING` / `HARVEST_DEADLINE_RISK` →
  `HARVEST_COMPLETED`;
- distinzione esplicita fra capacità biologica e capacità temporale/logistica;
- trattamento isolato `MAX_WHEAT_PLANTS_PER_DAY=2`;
- invarianti per target, workforce, land, livestock, cash, market e routing;
- metriche e gate V4 preregistrati.

## 6. BUILD

Il BUILD applica esclusivamente il trattamento preregistrato:

- config schema `model_spec_c2.codex.v3` con
  `max_wheat_plants_per_day=2`;
- conteggio fail-closed delle WHEAT osservate per `planted_day` corrente;
- al massimo due task PLANT WHEAT per coorte/giorno;
- nessun cap su WATER/HARVEST/DIG o sulle crop già vive;
- test mirati su cap nello stesso giorno e riapertura degli slot il giorno
  successivo;
- preflight V4 con cohort size, peak ready, deadline miss, latency e fraction
  yield>=3.

Target, mix, workforce, layout/routing, land, livestock, market e cash floor
non sono stati modificati.

## 7. VERIFY P0/P1

Protocollo: seed neutrale preregistrato `26083001`, 360 step, avversario
inerte, un run Codex in P0 e uno in P1. È una verifica del meccanismo, non un
benchmark competitivo.

| Gate | P0 | P1 | Soglia | Esito |
|---|---:|---:|---:|---|
| status / error / fallback | DONE / 0 / 0 | DONE / 0 / 0 | DONE / 0 / 0 | PASS |
| own-player binding | sì | sì | sì | PASS |
| max WHEAT plant cohort | 2 | 2 | <=2 | PASS |
| peak simultaneous ready | 2 | 2 | <=4 | PASS |
| deadline miss | 0/15 (0%) | 0/15 (0%) | <=25% | PASS |
| HARVEST WHEAT yield>=3 | 15/15 (100%) | 15/15 (100%) | >=80% | PASS |
| ready→completed latency mean/max | 9,20 / 19 | 8,73 / 16 | diagnostica | — |
| MELON HARVEST / unità | 9 / 53 | 9 / 52 | >0 | PASS |
| MELON SELL drawdown | 47 | 35 | >0 | PASS |

Entrambi i run raggiungono max active 22 e due quadranti. Daily WATER coverage
è 89,36% / 88,40%; MOVE share è 53,69% / 52,97%.

## 8. Risultati causali

Il trattamento realizza la catena preregistrata senza addendum post-hoc:

```text
coorte massima 9 -> 2
peak ready 9 -> 2
deadline miss 77,78% -> 0%
fraction HARVEST yield>=3 50/66,67% -> 100/100%
WHEAT yield/harvest 2,17/2,50 -> 3,00/3,00
```

La domanda causale centrale riceve quindi una risposta positiva per il
meccanismo V4: la resa biologica era disponibile, ma il burst temporale ne
impediva la conversione. Distribuire le PLANT secondo la capacità on-time
osservata elimina il backlog prima del decay.

Il final cash del preflight ($16.238 P0, $15.998 P1) non è usato per sostenere
il target $23k: durata, avversario e protocollo non sono quelli del tournament.

## 9. Test

- test Codex mirati: `24 passed`;
- suite repository: `182 passed`;
- Ruff su policy, test e preflight: PASS;
- `git diff --check`: PASS; i warning LF/CRLF sono informativi;
- preflight P0/P1: PASS;
- nessuna regressione lifecycle osservata: PLANT/WATER/HARVEST/DIG/SELL e
  seconda land restano effettivi.

Il warning pytest sulla `.pytest_cache` deriva dai permessi della sandbox e non
impedisce l'esecuzione della suite.

## 10. Limiti residui

- Il VERIFY conferma il meccanismo, non il mean tournament >$23.000.
- Lo staggering può ritardare l'attainment nominale; max active resta 22 nel
  preflight breve.
- Il cap 2 deriva da un singolo contesto neutrale e dovrà generalizzare nel
  protocollo comune senza ulteriore tuning.
- Il preflight di 360 step non attiva le COW; il sottosistema resta invariato.
- Non è stato eseguito alcun torneo, seed ufficiale o invio Kaggle.

## 11. Freeze artifact

Baseline V3.2 prima del BUILD V4:

```text
POLICY_SHA256: 99754AE47D6CD8A4FA249BD3B97B50BB9E695BB2CB8EEE3E3F72448988616D09
CONFIG_SHA256: 6B85154DE327F9E7B87F241D1D6A65355C1277B9D1FD8B0CFACF1B71DF462F1B
MODEL_SPEC_SHA256: 4B2DA55E1FF37BC3352E5C49519688252188A06B593BEA47467ED12F72F2F737
```

Build V4 verificato:

```text
POLICY_SHA256: 333730C6D78246D7C9FB621CE80E81C34736D868688FD836D09926E31A6861D5
CONFIG_SHA256: C5C3C1558ECBED55D0FBBB351930DF43EED62E633F58CBAEDF71C1135CB4375C
MODEL_SPEC_SHA256: A4215F6213EB445AC4402EBF07B36194A08F805231F9B17580619496AC2FBE93
PREFLIGHT_RUNNER_SHA256: 9B2357C1F98F87F4C50BDF11C86B876B9EF24C86AA64BE42AA31B893229BC6FF
TARGETED_TEST_SHA256: C557FD3D43BA50ED598608125A18EC7FF2C89F2755C745750A514CB6D6AE89F4
PREFLIGHT_EVIDENCE_SHA256: D5AC30EB3ECEB07F1601808C004FF18893C7C9F86718C1F1AD6FAE0361D30AC2
```

Artifact VERIFY:
`results/model_spec_c2/performance_iteration/CODEX_C2_V4_PREFLIGHT.json`.

## 12. Stato finale

Tutti i gate di readiness richiesti dal prompt V4 sono soddisfatti. Questo
stato autorizza soltanto la futura partecipazione al torneo comune; non è una
dichiarazione di successo economico.

```text
C2_PERFORMANCE_ITERATION_V4_COMPLETE: YES
TOURNAMENT_READY: YES
TARGET_MEAN_FINAL_MONEY: >23000
TOURNAMENT_EXECUTED: NO
KAGGLE_RUN: NO
```
