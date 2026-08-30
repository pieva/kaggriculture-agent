# PROMPT OPERATIVO — C2 COMMON PERFORMANCE TOURNAMENT

## Ruolo

Agisci esclusivamente come **orchestratore e auditor neutrale** del tournament comune C2.

I tre candidati sono congelati e `TOURNAMENT_READY: YES`:

- Antigravity C2 performance iteration;
- Codex C2 V4;
- Copilot C2 performance iteration.

**NON SEI AUTORIZZATO A MODIFICARE, OTTIMIZZARE, CORREGGERE O RIFATTORIZZARE NESSUNO DEI TRE CANDIDATI**, incluso Antigravity.

In questa fase il codice dei candidati è materiale sperimentale congelato.

Non eseguire Kaggle.

---

## 1. Stato sperimentale

Il precedente C2 retournament era tecnicamente valido ma non aveva raggiunto l'obiettivo economico:

| Candidate | Mean Final Money |
|---|---:|
| Antigravity | $16.671 |
| Codex | $15.156 |
| Copilot | $4.154 |

Il criterio immediato preregistrato per questa performance iteration è:

```text
C2_PERFORMANCE_SUCCESS:
almeno un candidato con Mean Final Money > $23.000
```

Il riferimento strategico superiore resta $50k–$75k, ma NON è il gate immediato di questo round.

---

## 2. Amendment metodologico obbligatorio: nuovi seed

I tre seed storici C2:

```text
1113294977
3033283457
1678077158
```

NON devono essere usati come primary evaluation set.

Motivo: durante la performance iteration Antigravity sono stati utilizzati in verifiche private, quindi non costituiscono più un test indipendente per quel candidato.

### Procedura obbligatoria

Prima di eseguire qualsiasi episodio:

1. genera/seleziona **3 nuovi seed** validi per l'engine;
2. i seed devono essere diversi tra loro;
3. non devono coincidere con i tre seed storici sopra;
4. registrali immediatamente nel protocollo;
5. salva il protocollo prima del primo episodio;
6. dopo il freeze del protocollo, i seed non possono più essere cambiati per alcun motivo basato sui risultati.

Creare:

```text
results/model_spec_c2/performance_tournament/C2_PERFORMANCE_TOURNAMENT_PROTOCOL.md
```

Il file deve contenere esplicitamente:

```text
PRIMARY_SEED_1:
PRIMARY_SEED_2:
PRIMARY_SEED_3:
SEEDS_FROZEN_BEFORE_EXECUTION: YES
HISTORICAL_SEEDS_EXCLUDED_FROM_PRIMARY_SET: YES
```

I seed storici possono essere citati come baseline descrittiva, ma **non rieseguirli in questo round**.

---

## 3. Freeze e controllo iniziale

Prima del tournament:

- identifica esattamente gli artifact correnti dei tre candidati;
- registra commit/branch/stato repository;
- registra SHA256 dei file candidati/config/MODEL_SPEC rilevanti;
- esegui `git diff --check`;
- esegui la suite repository;
- verifica che gli entrypoint dei tre candidati siano importabili.

Non modificare i candidati se emerge un problema.

Se uno dei tre non è eseguibile:

```text
TOURNAMENT_ABORTED: YES
```

documenta il blocker e fermati.

Un failure del freeze/readiness NON autorizza un fix.

---

## 4. Disegno del tournament

Usare lo stesso disegno pairwise del retournament C2:

```text
Antigravity vs Codex
Antigravity vs Copilot
Codex vs Copilot
```

Per ciascun pairing eseguire i **3 nuovi seed congelati**.

Totale:

```text
3 pairing × 3 seed = 9 episodi
720 step per episodio
```

Non aggiungere run, mirror, rerun o seed dopo aver osservato i risultati.

La precedente verifica E16 ha classificato il positional effect come negligibile; mantenere quindi il formato pairwise già usato nel C2 retournament, salvo blocker tecnico documentato.

Il player-index binding deve comunque essere corretto.

---

## 5. Integrità dell'esecuzione

Per ogni episodio registrare almeno:

```text
pairing
seed
player assignment
completion
final money P0
final money P1
winner
errors
fallback
steps
```

Verificare:

```text
completion = 100%
errors = 0
pathological fallback = 0
expected steps = 720
```

Mantenere l'audit delle decisioni/action come nel precedente C2 retournament, se il runner corrente lo supporta.

Non confondere:

```text
action dispatched
action accepted
state transition
productive effect
economic effect
```

---

## 6. Metriche economiche obbligatorie

Per ciascun candidato aggregare sui suoi 6 player-episodes:

```text
W-L-T
Mean Final Money
Median Final Money
Sample Std (ddof=1)
Min
Max
```

Calcolare inoltre, quando disponibile dalla telemetria:

```text
OWNED_SURFACE
ACTIVE_SURFACE
SERVICEABLE_SURFACE
PRODUCTIVE_SURFACE
MONETIZED_OUTPUT

max active surface
mean active surface
final active surface
daily WATER coverage
workforce mean/max
worker utilization
MOVE share
HARVEST count
yield per HARVEST per crop
SELL quantity/value
first revenue step
minimum cash
WEED burden
replant latency
```

Per Codex V4 includere esplicitamente, se osservabile:

```text
peak simultaneous WHEAT harvest-ready tiles
WHEAT harvest deadline miss rate
fraction WHEAT HARVEST with yield >= 3
ready-to-completed HARVEST latency
```

Per Antigravity e Copilot non inventare metriche non supportate dalla loro telemetria.

---

## 7. Confronto causale

Il report deve distinguere tre livelli:

### A. Runtime realization

```text
La policy viene realmente eseguita?
```

### B. Economic closure

```text
Il ciclo produce e monetizza output?
```

### C. Competitive capacity

```text
La policy trasforma capacità produttiva in Final Money competitivo?
```

Non usare `TOURNAMENT_READY`, test passati o una vittoria pairwise come sinonimo di successo economico.

---

## 8. Baseline di confronto

Confrontare i risultati primari con il precedente C2 retournament:

```text
Antigravity: $16.671 mean
Codex:       $15.156 mean
Copilot:      $4.154 mean
```

Calcolare per ogni candidato:

```text
absolute delta
percentage delta
```

Questo confronto è descrittivo: i nuovi seed rendono il test indipendente ma non paired con il precedente retournament.

Non attribuire causalmente tutta la differenza alla revisione del candidato senza evidenza sufficiente.

---

## 9. Gate economico C2

Applicare letteralmente:

```text
IF max(candidate Mean Final Money) > 23000:
    C2_PERFORMANCE_SUCCESS = YES
ELSE:
    C2_PERFORMANCE_SUCCESS = NO
```

Attenzione: la condizione riguarda la **mean sui 6 player-episodes del candidato**, non:

- il massimo episodio;
- la mediana;
- una vittoria pairwise;
- un preflight;
- un singolo seed.

Se nessuno supera $23.000:

```text
C2_STATUS:
VALID TOURNAMENT — PERFORMANCE OBJECTIVE NOT ACHIEVED — ITERATION REQUIRED
```

Se almeno uno supera $23.000:

```text
C2_STATUS:
PERFORMANCE OBJECTIVE ACHIEVED — READY FOR REVIEW
```

Non dichiarare automaticamente raggiunto il target strategico $50k–$75k.

---

## 10. Nessun intervento post-hoc

Dopo l'avvio del primo episodio sono vietati:

```text
candidate edits
config tuning
seed replacement
selective reruns
discarding bad episodes
post-hoc parameter changes
```

Se un episodio fallisce per un problema infrastrutturale chiaramente esterno alla policy:

1. preserva il failure;
2. documenta esattamente l'evento;
3. non eseguire autonomamente un rerun selettivo;
4. ferma il tournament e richiedi decisione all'orchestrazione superiore.

---

## 11. Artifact

Creare almeno:

```text
results/model_spec_c2/performance_tournament/
    C2_PERFORMANCE_TOURNAMENT_PROTOCOL.md
    C2_PERFORMANCE_TOURNAMENT_SUMMARY.md
    aggregated_results.json
    aggregated_results.csv
    raw/
```

Preservare i replay/raw output dei 9 episodi.

Il summary deve contenere:

1. freeze iniziale;
2. amendment sui nuovi seed;
3. seed preregistrati;
4. protocollo;
5. integrità degli episodi;
6. ranking economico;
7. metriche produttive;
8. confronto con C2 retournament;
9. analisi causale prudente;
10. gate >$23.000;
11. limiti;
12. stato finale.

---

## 12. Output finale obbligatorio

Riporta una tabella:

```text
Rank | Candidate | W-L-T | Mean | Median | Std | Min | Max | Delta vs prior C2
```

Poi dichiara esattamente:

```text
C2_PERFORMANCE_TOURNAMENT_COMPLETE: YES|NO
C2_PERFORMANCE_SUCCESS: YES|NO
BEST_CANDIDATE:
BEST_MEAN_FINAL_MONEY:
TARGET_MEAN_FINAL_MONEY: >23000
C2_STATUS:
KAGGLE_RUN: NO
```

---

## 13. Stop condition

Dopo la produzione e verifica degli artifact:

**FERMATI.**

Non:

- modificare MODEL_SPEC;
- modificare la Foundation;
- iniziare C3;
- aggiornare la state machine;
- eseguire Kaggle;
- fare una nuova performance iteration.

La REVIEW del C2 e l'eventuale integrazione delle evidenze nella macchina a stati verranno decise separatamente dopo aver letto il risultato del tournament.
