# E12-X1.7 — Workforce Capacity Scaling
## Scale First, Optimize Later

## Obiettivo

E12-X1.6 ha finalmente prodotto una base ibrida strutturalmente credibile:

- Mean Final Money: **$22,008.80**
- livestock core 2×2 funzionante;
- Cow scaling progressivo;
- workforce specializzata per funzione;
- crop working set stabile;
- emergency WATER / weed control funzionanti;
- MELON come principale cash crop ad alto ROI;
- feed loop WHEAT sostenibile;
- bassa varianza tra seed.

Il prossimo obiettivo NON è ottimizzare l'architettura.

Il prossimo obiettivo è dimostrare che l'architettura X1.6 può essere **scalata** fino a una baseline ibrida credibile **> $25,000 Mean Final Money**, prima di qualsiasi tuning fine.

Principio:

> **Scale first, optimize later.**

E12-X1.7 deve quindi modificare una sola leva strutturale:

> aumentare da 4 a 5 i `CROP_PRIMARY`, mantenendo invariato il carico massimo di **4 crop tile per crop worker**.

---

# 1. Ipotesi

## H12-X1.7

Il gap economico residuo di X1.6 deriva almeno in parte da insufficiente capacità produttiva crop.

Con:

```text
1 LIVESTOCK_PRIMARY
+
5 CROP_PRIMARY
=
6 worker totali
```

e:

```text
4 crop tiles / crop worker
```

la capacità teorica diventa:

```text
5 × 4 = 20 crop tiles
```

senza aumentare il maintenance burden individuale validato in X1.6.

---

# 2. Success Criteria

## Primary Gate — Credible Hybrid Baseline

```text
Mean Final Money > $25,000
```

Se superato stabilmente:

```text
E12 CREDIBLE HYBRID BASELINE
```

## Champion Target

Resta:

```text
E11-X1.7 = $28,083.80
```

Il superamento di $28,083.80 è desiderabile ma NON necessario per validare X1.7.

---

# 3. Una sola leva sperimentale

Modificare:

```text
crop_workers: 4 -> 5
```

Mantenere:

```text
crop_working_set_capacity =
4 * crop_workers
```

quindi:

```text
X1.6 = 16 crop tiles
X1.7 = 20 crop tiles
```

NON modificare contemporaneamente il rapporto tile/worker.

---

# 4. Invarianti da preservare

Non modificare salvo bug strettamente necessario:

- centered livestock architecture;
- livestock core 2×2;
- Cow #1 → #2 → #3 → #4 progressive scaling;
- `LIVESTOCK_PRIMARY`;
- functional workforce specialization;
- crop locality;
- emergency WATER priority;
- weed recovery;
- retention logic;
- dynamic WHEAT feed loop;
- MELON-oriented cash crop portfolio;
- economic crop selection logic;
- livestock action priorities;
- financial readiness logic;
- existing land readiness logic.

---

# 5. Capacity Invariant

Deve rimanere:

```text
crop_working_set_capacity =
4 * active_crop_workers
```

Non:

```text
4 * total_workers
```

Il `LIVESTOCK_PRIMARY` resta escluso dalla capacità crop ordinaria.

---

# 6. Target Architecture

Target:

```text
Worker 0 -> LIVESTOCK_PRIMARY
Worker 1 -> CROP_PRIMARY cluster A
Worker 2 -> CROP_PRIMARY cluster B
Worker 3 -> CROP_PRIMARY cluster C
Worker 4 -> CROP_PRIMARY cluster D
Worker 5 -> CROP_PRIMARY cluster E
```

Ogni crop worker:

```text
max 4 crop tiles
```

Target crop working set:

```text
20 active maintained crop tiles
```

---

# 7. Hiring Worker 5

Non hardcodare un giorno.

Definire una readiness threshold per il quinto crop worker.

Il nuovo HIRE deve avvenire quando:

- esiste capacità finanziaria sostenibile;
- livestock/feed non sono in crisi;
- il working set corrente è stabile;
- esistono tile utilizzabili per il nuovo cluster;
- il nuovo worker può essere immediatamente convertito in capacità produttiva.

Registrare:

```text
worker5_hire_turn
money_before_hire
money_after_hire
crop_tiles_before_hire
crop_tiles_after_hire
```

---

# 8. Non essere eccessivamente conservativi

I replay dei top mostrano workforce numerosa già nell'opening.

Non introdurre soglie finanziarie arbitrarie che ritardino Worker 5 fino a quando il suo ROI residuo diventa basso.

La soglia deve essere economico-operativa, non calendariale.

---

# 9. Cluster E

Il quinto crop worker deve ricevere un cluster:

- compatto;
- vicino alla superficie già attiva;
- con minima distanza dal core compatibilmente con i cluster esistenti;
- senza cross-map traversal inutile.

Non aprire automaticamente un quadrante remoto soltanto per assegnargli 4 tile.

---

# 10. Land Expansion

Non fare tuning di Q1/Q2/Q3 in X1.7.

Tuttavia, se Worker 5 necessita di nuova terra, l'unlock può avvenire quando necessario.

Registrare:

```text
Q1 unlock turn
Q2 unlock turn
Q3 unlock turn
```

e soprattutto:

```text
time_from_unlock_to_productive_use
```

Un quadrante acquistato ma non utilizzato rapidamente deve essere segnalato come inefficienza futura, NON corretto in X1.7.

---

# 11. Livestock Core

Il 2×2 deve continuare a essere progressivamente monetizzato.

Registrare:

```text
Cow #1 turn
Cow #2 turn
Cow #3 turn
Cow #4 turn
final cow count
livestock_core_utilization
milk units
milk revenue
```

Non ridurre il livestock per finanziare artificialmente Worker 5.

---

# 12. Feed Loop

Mantenere WHEAT dinamico in funzione delle Cow.

Il quinto crop worker NON deve provocare:

- starvation;
- riduzione del feed buffer sotto soglia;
- sostituzione involontaria di feed tile con MELON;
- vendita accidentale del buffer WHEAT.

---

# 13. Crop Portfolio

Mantenere la logica economica validata in X1.6.

In particolare non fare un nuovo crop portfolio tuning in X1.7.

Le nuove 4 tile devono usare lo stesso criterio economico delle altre cash crop.

---

# 14. Retention Gate

X1.7 deve mantenere:

```text
retention >= 90%
weed penetration <= 10%
no persistent emergency WATER backlog
```

Se 20 tile non sono mantenibili con 5 crop worker, X1.7 fallisce come capacity scaling.

Non correggere aumentando a 5 tile/worker.

---

# 15. Movement Gate

Registrare movement ratio globale e per worker.

Confrontare:

```text
X1.6 = 33.6% mean movement ratio
```

Il quinto worker non deve generare un nuovo cross-map movement collapse.

Segnalare:

```text
movement_delta_vs_x16
```

---

# 16. Productive Ratio

Baseline X1.6:

```text
64.7%
```

Misurare X1.7.

L'aumento di workforce deve tradursi in maggiore output economico, non soltanto in più movement.

---

# 17. Capacity Utilization

Calcolare:

```text
crop_capacity_utilization =
active_crop_tiles /
(4 * active_crop_workers)
```

Dopo Worker 5:

target:

```text
>= 80%
```

Idealmente:

```text
18–20 active crop tiles
```

---

# 18. Marginal Worker ROI

Misurare esplicitamente il contributo del quinto crop worker.

Calcolare almeno:

```text
incremental_revenue_vs_X1.6
incremental_crop_tiles
incremental_crop_revenue
worker5_productive_actions
worker5_movement_actions
worker5_idle_actions
```

e una stima:

```text
worker5_net_contribution
```

---

# 19. Revenue Decomposition

Per seed separare:

```text
crop revenue
milk revenue
other revenue
```

Dobbiamo sapere se il salto da $22k verso $25k+ arriva realmente dall'aumento della capacità crop.

---

# 20. Non ottimizzare ancora

In X1.7 NON modificare:

- 4 → 4.5/5 tile per worker;
- timing Cow;
- numero massimo Cow;
- crop ranking;
- feed formula;
- WATER threshold;
- weed threshold;
- Q1/Q2 timing;
- market policy;
- livestock worker duty cycle.

Annotare le inefficienze osservate per X1.8.

---

# 21. Stage A0

Seed `0`.

PASS se:

- Worker 5 viene assunto;
- diventa `CROP_PRIMARY`;
- il working set cresce oltre X1.6;
- target operativo verso 20 crop tile;
- retention >= 90%;
- weed penetration <= 10%;
- Cow/feed loop resta sano;
- no maintenance collapse;
- final money > X1.6 seed 0 (`$21,752`);
- provenance valida.

---

# 22. Stage A1

Seed `100`.

Stessi gate.

Stage B solo dopo doppio PASS.

---

# 23. Canonical Stage B

Usare:

```text
0
100
200
300
400
```

con gli stessi opponent canonici.

Confrontare:

- E12-X1.7;
- E12-X1.6;
- E11-X1.7.

---

# 24. Benchmark Table

Produrre almeno:

| Seed | X1.7 Money | X1.6 Money | E11-X1.7 Money | Workers | Crop Workers | Peak Crop Tiles | Final Cows | Retention | Movement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|

Aggiungere:

- Mean;
- Median;
- std;
- min;
- max.

---

# 25. Primary Comparison

Baseline E12:

```text
X1.6 = $22,008.80
```

Credible-baseline threshold:

```text
$25,000
```

Champion:

```text
E11-X1.7 = $28,083.80
```

Calcolare:

```text
delta_vs_X1.6
percent_delta_vs_X1.6

delta_vs_25k
percent_delta_vs_25k

delta_vs_X1.7
percent_delta_vs_X1.7
```

---

# 26. Paired Results

Calcolare:

```text
paired wins vs X1.6
paired wins vs E11-X1.7
```

Il superamento dei $25k deve essere robusto, non prodotto da un singolo outlier.

---

# 27. Interpretazione

## A — Mean < X1.6

```text
CAPACITY SCALING FAILED
```

Diagnosticare Worker 5.

## B — X1.6 < Mean < $25k

```text
CAPACITY SCALING POSITIVE BUT INSUFFICIENT
```

Valutare 6 crop workers @ 4 tile/worker.

## C — Mean >= $25k ma < $28,083.80

```text
E12 CREDIBLE HYBRID BASELINE
```

Non fare tuning immediato nello stesso esperimento.

X1.8 potrà iniziare l'ottimizzazione controllata.

## D — Mean >= $28,083.80

```text
E12 NEW LOCAL CHAMPION
```

Preparare validazione esterna prima di ulteriori modifiche.

---

# 28. Decisione sul sesto Crop Worker

Se X1.7 resta sotto $25k ma:

- retention è sana;
- Worker 5 è produttivo;
- capacity utilization è alta;
- marginal ROI Worker 5 è positivo;

la raccomandazione deve essere:

```text
PROCEED E12-X1.8 — 6 CROP WORKERS @ 4 TILES/WORKER
```

NON:

```text
increase tiles/worker
```

---

# 29. Quando inizieremo l'ottimizzazione

L'ottimizzazione fine comincia soltanto quando esiste una baseline ibrida credibile:

```text
Mean >= $25,000
```

Da quel momento potremo testare separatamente:

1. HIRE timing;
2. Cow scaling thresholds;
3. crop portfolio;
4. feed buffer;
5. land unlock thresholds;
6. market policy;
7. 4 → 4.5 → 5 tiles/worker;
8. movement optimization.

---

# 30. Provenance

Run ID:

```text
E12-X1.7-*
```

Mantenere:

- source hash;
- config hash;
- seed/opponent;
- SHA-256;
- canonical comparability.

---

# 31. Submission

Non sostituire automaticamente la submission champion.

Regole:

### Mean < $25k
Nessuna promozione.

### $25k <= Mean < $28,083.80
Marcare X1.7 come:

```text
E12 CREDIBLE HYBRID BASELINE
```

ma mantenere E11-X1.7 come local champion.

### Mean >= $28,083.80
Marcare:

```text
E12 NEW LOCAL CHAMPION
```

e preparare submission candidate.

---

# 32. Documentazione

Creare:

```text
docs/versions/E12_X1_7_workforce_capacity_scaling.md
```

Aggiornare:

```text
docs/PROJECT_STATE.md
docs/EXPERIMENT_LOG.md
```

Documentare esplicitamente che X1.7 è un esperimento di **scaling**, non di optimization.

---

# 33. Output finale richiesto

Restituire:

### A. Implementation delta vs X1.6
### B. Worker 5 readiness gate
### C. Tests
### D. Stage A0
### E. Stage A1
### F. Canonical Stage B
### G. Capacity utilization analysis
### H. Worker 5 marginal ROI
### I. Livestock stability
### J. Crop retention / weeds
### K. Revenue decomposition
### L. Comparison vs X1.6 / $25k / E11-X1.7
### M. Recommendation

Una sola raccomandazione finale:

```text
CAPACITY SCALING FAILED
```

oppure:

```text
PROCEED E12-X1.8 — 6 CROP WORKERS @ 4 TILES/WORKER
```

oppure:

```text
E12 CREDIBLE HYBRID BASELINE — BEGIN CONTROLLED OPTIMIZATION
```

oppure:

```text
E12 NEW LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION
```

---

# Approval

Questo prompt autorizza:

1. BUILD X1.7;
2. test;
3. A0;
4. A1;
5. Stage B dopo doppio PASS;
6. documentazione.

Non richiedere approvazioni intermedie.

---

# Principio guida

> **Abbiamo finalmente capito come deve iniziare e come deve essere strutturata la farm ibrida. Ora non dobbiamo ottimizzarla prematuramente: dobbiamo scalarla fino a una baseline credibile sopra $25k. Mantieni 4 crop tile per crop worker, aggiungi capacità produttiva con il quinto crop worker e misura se l'architettura scala.**
