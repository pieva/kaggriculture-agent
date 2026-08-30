# PROMPT OPERATIVO — CODEX C2 PERFORMANCE ITERATION V4

## Mandato

Proseguire **solo sul candidato Codex C2**.

Antigravity C2 e Copilot C2 sono congelati e non devono essere modificati.

Il precedente round Codex V3.2 si è concluso correttamente con:

```text
C2_PERFORMANCE_ITERATION_COMPLETE: YES
TOURNAMENT_READY: NO
TARGET_MEAN_FINAL_MONEY: >23000
```

Non eseguire il tournament comune.
Non usare i seed ufficiali del tournament.
Non eseguire Kaggle.
Non modificare Foundation C2, runner comuni o candidati altrui.

L'obiettivo di questa iterazione è formulare e verificare una **nuova ipotesi causale** a partire dalla falsificazione V3.2.

---

## 1. Evidenza congelata da cui partire

Il retournament C2 precedente mostrava per Codex:

```text
Mean Final Money: $15.156
Max active surface: 24
Mean active surface: 13,46
Daily WATER coverage: 69,89%
MOVE share: 79,52%
WHEAT yield/harvest: 1,084
Replant latency: 37,15 step
```

La performance iteration V3 ha ipotizzato che la raccolta WHEAT troppo precoce producesse churn e bassa yield density.

La catena V3 → V3.1 → V3.2 ha però falsificato il meccanismo nella forma prevista.

Risultati del preflight meccanico:

| Build | P0 WHEAT units/harvest | P1 | Esito |
|---|---:|---:|---|
| V3 | 2,25 | 2,25 | FAIL |
| V3.1 | 2,25 | 2,25 | FAIL |
| V3.2 | 2,17 | 2,50 | FAIL |

V3.2 ha comunque ottenuto:

```text
P0/P1 execution: PASS
Errors/fallback: 0
MELON cycle: PASS
Max active surface: 22
Daily WATER coverage: 75,02% / 78,33%
MOVE share: 58,86% / 56,04%
```

Gli eventi WHEAT mostrano che alcune tile raggiungono yield 3, ma la wave sincronizzata non viene interamente raccolta prima del decay.

HARVEST osservati:

```text
P0: [3, 3, 2, 1, 3, 1]
P1: [3, 3, 2, 1, 3, 3]
```

La conclusione congelata di V3.2 è:

> Il problema non è più semplicemente raggiungere la maturity economica. Una wave produttiva sincronizzata genera un picco di servizio che routing/workforce non riescono a smaltire prima del decay.

---

## 2. Nuovo DEFINE obbligatorio

NON iniziare modificando immediatamente V3.2.

Prima del BUILD devi formulare una nuova ipotesi distinta dalla precedente.

La nuova diagnosi deve analizzare almeno:

```text
HARVEST_WAVE_SYNCHRONIZATION
SERVICE_PEAK
WORKER_PREPOSITIONING
ROUTING_DISTANCE_AT_HARVEST
HARVEST_DEADLINE
DECAY_EXPOSURE
PLANT_STAGGERING
SERVICE_LOAD_DISTRIBUTION
```

Non è obbligatorio intervenire su tutti questi elementi.

Devi determinare quale meccanismo spiega principalmente la perdita di yield osservata.

### Domanda causale centrale

> Il problema è la resa biologica delle tile oppure l'incapacità della policy di trasformare simultaneamente tile mature in harvest monetizzato entro la loro finestra temporale utile?

Quantificare il fenomeno prima del BUILD.

---

## 3. Ipotesi V4

Produrre un nuovo blocco preregistrato:

```text
HYPOTHESIS_ID: CODEX-C2-...

OBSERVED_PROBLEM:

EVIDENCE:

CAUSAL_MECHANISM:

MODEL_CHANGE:

EXPECTED_INTERMEDIATE_EFFECT:

EXPECTED_ECONOMIC_EFFECT:
Final Money UP; target tournament mean > $23.000

FALSIFICATION_CONDITION:
```

La nuova ipotesi deve essere **distinta** da:

```text
"aspettare semplicemente più yield prima di HARVEST"
```

V3.2 ha già dimostrato che questo non basta.

---

## 4. Soluzioni ammissibili, non prescritte

Puoi valutare autonomamente, se supportato dall'evidenza:

- staggering temporale delle PLANT;
- staggering per gruppi/zone;
- pre-positioning dei worker prima della maturity;
- assegnazione anticipata dei target HARVEST;
- riduzione della dimensione della wave;
- distribuzione delle maturity;
- layout/routing specifico per harvest;
- priorità deadline-aware;
- riduzione del service peak;
- combinazioni minimali di questi meccanismi.

Questi sono **spazi di soluzione**, non istruzioni.

Non devi implementarli tutti.

Scegli il cambiamento minimo capace di falsificare o confermare la nuova ipotesi.

---

## 5. Vincolo di isolamento causale

Non cambiare contemporaneamente elementi non necessari come:

```text
land target
workforce target
livestock strategy
cash floor
numero di quadranti
market strategy generale
```

a meno che il nuovo DEFINE dimostri che uno di questi è parte necessaria del meccanismo.

La nuova catena deve restare:

```text
EVIDENZA V3.2
→
NUOVA IPOTESI
→
CAMBIAMENTO MINIMO
→
EFFETTO INTERMEDIO
→
VERIFY
```

Non trasformare V4 in un nuovo tuning generale del candidato.

---

## 6. MODEL_SPEC prima del codice

Aggiornare prima:

```text
docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md
```

La nuova specifica deve rappresentare esplicitamente, se confermato dal DEFINE, la differenza tra:

```text
ENGINE_HARVEST_ELIGIBLE
ECONOMIC_HARVEST_READY
HARVEST_SERVICE_PENDING
HARVEST_DEADLINE_RISK
HARVEST_COMPLETED
```

I nomi sono indicativi: usare quelli più coerenti con il modello.

Il punto concettuale è obbligatorio:

> Una tile biologicamente pronta non genera valore se il sistema non dispone della capacità temporale/logistica per raccoglierla prima del decadimento.

Questa evidenza sarà successivamente candidata all'integrazione nella macchina a stati comune, ma **non modificare ora la Foundation C2**.

---

## 7. Preregistrazione delle metriche

Prima del BUILD congelare almeno due metriche.

Una deve misurare direttamente il problema di service peak.

Esempi:

```text
METRIC_A:
HARVEST_READY_TO_COMPLETED_LATENCY

METRIC_B:
FRACTION_OF_WHEAT_HARVESTED_AT_YIELD_GE_3

METRIC_C:
HARVEST_DEADLINE_MISS_RATE

METRIC_D:
PEAK_SIMULTANEOUS_HARVEST_READY_TILES
```

Scegliere metriche effettivamente osservabili.

La previsione economica resta:

```text
EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: >23000
```

Il final money del preflight non costituisce prova del target.

---

## 8. BUILD

Implementare soltanto dopo il freeze del DEFINE.

Scope autorizzato:

```text
docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md
src/agricola/strategy/codex_c2.py
configs/model_spec_c2/CODEX_C2_CONFIG.json
tests relativi a Codex C2
preflight Codex C2
report Codex performance iteration
```

Non modificare:

```text
Foundation C2
Antigravity
Copilot
runner tournament comune
submission
seed tournament
```

---

## 9. VERIFY

Usare un seed neutrale non appartenente al tournament.

Verificare separatamente P0 e P1.

Minimo:

```text
status DONE
0 unhandled errors
0 pathological fallback
own-player binding corretto
nuovo meccanismo osservabile
MELON cycle ancora realizzato
nessuna regressione evidente del lifecycle
```

Il VERIFY deve verificare la nuova ipotesi, non stimare il risultato competitivo.

### Regola anti-tuning

Non eseguire una sequenza aperta di tentativi sullo stesso seed fino a ottenere il risultato desiderato.

Se la previsione preregistrata fallisce:

1. registrare il FAIL;
2. diagnosticare il motivo;
3. se emerge un nuovo meccanismo realmente distinto, congelare un nuovo addendum DEFINE prima di modificare il BUILD;
4. non reinterpretare retroattivamente il criterio.

---

## 10. Gate finale

Puoi dichiarare:

```text
TOURNAMENT_READY: YES
```

solo se:

- P0 PASS;
- P1 PASS;
- error/fallback PASS;
- nuova previsione causale essenziale PASS;
- test Codex PASS;
- suite repository PASS;
- `git diff --check` PASS;
- nessun blocker noto.

Se il meccanismo preregistrato fallisce:

```text
TOURNAMENT_READY: NO
```

anche se tutto il codice funziona.

---

## 11. Budget operativo

Il budget disponibile può essere limitato.

Priorità assoluta:

```text
1. DEFINE causale
2. preregistrazione
3. MODEL_SPEC
4. BUILD minimo
5. test mirati
6. preflight P0/P1
7. report/freeze
```

Evitare:

- esplorazioni laterali;
- refactoring non necessario;
- benchmark competitivi;
- tuning generale;
- documentazione ridondante.

Se il budget termina, lasciare il repository in uno stato riprendibile con:

```text
CURRENT_PHASE:
LAST_COMPLETED_STEP:
CURRENT_HYPOTHESIS:
FILES_CHANGED:
TEST_STATUS:
PREFLIGHT_STATUS:
NEXT_EXACT_ACTION:
```

Non sacrificare il rigore del DEFINE o del VERIFY per completare artificialmente l'iterazione.

---

## 12. Report

Aggiornare/produrre:

```text
results/model_spec_c2/performance_iteration/CODEX_C2_PERFORMANCE_ITERATION_V4.md
```

Struttura minima:

```text
1. Evidenza V3.2
2. Diagnosi del service peak
3. Ipotesi V4
4. Metriche preregistrate
5. MODEL_SPEC revision
6. BUILD
7. VERIFY P0/P1
8. Risultati causali
9. Test
10. Limiti residui
11. Freeze artifact
12. Stato finale
```

Chiudere obbligatoriamente con:

```text
C2_PERFORMANCE_ITERATION_V4_COMPLETE: YES|NO
TOURNAMENT_READY: YES|NO
TARGET_MEAN_FINAL_MONEY: >23000
TOURNAMENT_EXECUTED: NO
KAGGLE_RUN: NO
```

---

## 13. Stop condition

Se:

```text
TOURNAMENT_READY: YES
```

fermati.

Non eseguire il tournament.

Se:

```text
TOURNAMENT_READY: NO
```

fermati comunque dopo aver documentato la falsificazione e il prossimo problema causale.

La decisione sull'eventuale ulteriore iterazione spetta all'orchestrazione comune.

