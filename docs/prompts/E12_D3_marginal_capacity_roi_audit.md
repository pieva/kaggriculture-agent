# E12-D3 — Marginal Capacity ROI Audit
## Why Worker #5 Adds Only +1.7%

## Obiettivo

E12-X1.7 ha testato una sola leva:

```text
4 CROP_PRIMARY -> 5 CROP_PRIMARY
```

mantenendo invariato:

```text
4 crop tiles / crop worker
```

Il risultato canonico è stato:

- E12-X1.6 Mean Final Money: `$22,008.80`
- E12-X1.7 Mean Final Money: `$22,386.80`
- Delta: `+$378.00`
- Delta percentuale: `+1.7%`

A fronte di:

- +25% crop-worker capacity teorica;
- working-set capacity teorica da 16 a 20 crop tile;
- aumento delle productive actions;
- retention invariata.

Il rendimento marginale del quinto crop worker è quindi molto inferiore a quanto atteso.

Prima di aggiungere un sesto crop worker, dobbiamo capire **perché le tile 17–20 non generano abbastanza revenue marginale**.

Nome audit:

**E12-D3 — Marginal Capacity ROI Audit**

D3 è diagnostico puro.

NON modificare la strategia durante l'audit.

---

# 1. Domanda principale

Rispondere quantitativamente a:

> **Perché il quinto crop worker e le quattro tile aggiuntive producono soltanto +$378 medi rispetto a X1.6?**

Dobbiamo distinguere almeno tra:

```text
LATE_CAPACITY_ACTIVATION
LOW_TILE_UTILIZATION
LOW_CYCLE_COMPLETION
HIGH_MOVEMENT_OVERHEAD
CAPITAL_CROWDING_OUT
LAND_UNLOCK_DELAY
CROP_PORTFOLIO_MISMATCH
WORKER_IDLE
OTHER_VERIFIED_CAUSE
```

---

# 2. Confronto diretto X1.6 vs X1.7

Usare gli stessi paired seed canonici:

```text
0
100
200
300
400
```

e gli stessi opponent.

Confrontare X1.6 e X1.7 turn-by-turn.

Non usare valori aggregati soltanto.

---

# 3. Identificare precisamente Worker #5

In X1.7 identificare il nuovo crop worker aggiuntivo rispetto a X1.6.

Registrare:

```text
worker5_id
hire_turn
hire_day
cash_before_hire
cash_after_hire
assigned_cluster
assigned_tiles
```

---

# 4. Tile marginali 17–20

Identificare le quattro tile che esistono nel working set X1.7 ma non in X1.6.

Per ciascuna registrare:

```text
coordinate
working_set_enter_turn
first_plant_turn
first_water_turn
first_harvest_turn
crop_type
harvest_count
replant_count
revenue_generated
weed_events
drought_events
```

Queste tile sono il centro dell'audit.

---

# 5. Time-to-Revenue

Per Worker #5 e tile 17–20 calcolare:

```text
hire_to_first_plant
hire_to_first_harvest
hire_to_first_revenue
```

e:

```text
working_set_enter_to_first_revenue
```

Se il primo ricavo arriva molto tardi nell'episodio, classificare:

```text
LATE_CAPACITY_ACTIVATION
```

---

# 6. Remaining Economic Horizon

Al momento del primo planting e del primo harvest delle tile 17–20 calcolare:

```text
turns_remaining = 720 - current_turn
days_remaining
```

Per MELON stimare quanti cicli completi restano teoricamente disponibili.

Confrontare:

```text
theoretical_remaining_cycles
actual_completed_cycles
```

---

# 7. Cycle Completion Audit

Per ogni tile marginale:

```text
cycles_started
cycles_completed
harvests_per_cycle
revenue_per_cycle
```

Calcolare:

```text
cycle_completion_ratio =
completed_cycles /
theoretical_cycles_available_after_activation
```

Se le tile entrano presto ma completano pochi cicli, la causa NON è soltanto timing.

---

# 8. Marginal Crop Revenue

Calcolare:

```text
crop_revenue_X1.7
-
crop_revenue_X1.6
```

e confrontarlo con:

```text
Final Money delta = +$378
```

Separare:

- incremental crop revenue;
- incremental milk revenue;
- incremental costs;
- incremental land cost;
- incremental hire cost;
- incremental seed cost.

Costruire:

```text
Marginal Worker P&L
```

---

# 9. Marginal Worker P&L

Per Worker #5 stimare:

```text
+ crop revenue attributable to tiles 17–20
- hire cost
- additional seed cost
- additional land cost attributable to capacity
- additional movement/opportunity cost proxy
= marginal net contribution
```

Non attribuire costi comuni arbitrariamente.

Distinguere:

```text
direct_cost
shared_cost
unallocated_cost
```

---

# 10. Worker #5 Action Audit

Registrare per tutto l'episodio:

```text
movement_actions
plant_actions
water_actions
harvest_actions
dig_actions
idle_actions
other_actions
```

Calcolare:

```text
productive_action_ratio_worker5
movement_ratio_worker5
idle_ratio_worker5
```

Confrontare con Worker 1–4.

---

# 11. Role/Cluster Utilization

Calcolare:

```text
assigned_tile_utilization =
time tiles are productively occupied /
time tiles are available to worker
```

e:

```text
worker_capacity_utilization =
productive actions /
available worker actions
```

Se Worker #5 è spesso idle, classificare:

```text
WORKER_IDLE
```

---

# 12. Movement Comparison

X1.6 mean movement:

```text
33.6%
```

X1.7 mean movement:

```text
35.4%
```

Il delta è:

```text
+1.8 percentage points
```

Verificare:

- quanto del delta deriva da Worker #5;
- se Worker #5 attraversa regioni;
- distanza media per task;
- distanza media delle tile 17–20 dal home cluster/core.

---

# 13. Q1/Q2 Timing Interaction

X1.6:

```text
Q1 ≈ Turn 252
Q2 ≈ Turn 260
```

X1.7:

```text
Q1 ≈ Turn 258
Q2 ≈ Turn 263
```

Verificare causalmente:

- l'HIRE del quinto worker ritarda Q1/Q2?
- l'HIRE usa cash che sarebbe servito al land unlock?
- le tile 17–20 diventano disponibili soltanto dopo questi unlock?

Calcolare:

```text
hire_to_Q1
hire_to_Q2
Q1_to_first_marginal_tile
Q2_to_first_marginal_tile
```

---

# 14. Capital Crowding-Out

Ricostruire cash trajectory X1.6 vs X1.7:

```text
turn -> cash
```

Soprattutto attorno a:

- quinto HIRE;
- Q1;
- Q2;
- acquisto seed;
- Cow scaling.

Identificare se Worker #5 produce un costo opportunità che riduce o ritarda altri investimenti.

---

# 15. Cow / Livestock Interaction

Verificare che X1.7 e X1.6 abbiano la stessa traiettoria livestock:

```text
Cow #1
Cow #2
Cow #3
Cow #4
milk revenue
feed cost
```

Se X1.7 ritarda Cow scaling per finanziare Worker #5, registrarlo.

Non assumere che il crop worker aggiuntivo sia economicamente indipendente dal livestock.

---

# 16. Crop Portfolio Check

Verificare le crop effettivamente piantate nelle tile 17–20.

Se non sono MELON/high-ROI quando dovrebbero esserlo, classificare:

```text
CROP_PORTFOLIO_MISMATCH
```

Registrare:

```text
crop_type_share
revenue_per_tile
revenue_per_worker_action
```

---

# 17. Marginal Tile Productivity

Per tile 17–20 calcolare:

```text
revenue_per_tile
harvests_per_tile
worker_actions_per_tile
revenue_per_worker_action
```

Confrontare con le tile 1–16 di X1.6/X1.7.

Se le tile marginali rendono molto meno delle tile core, capire se la causa è:

- distanza;
- timing;
- crop type;
- cycle count;
- water/harvest scheduling.

---

# 18. Spatial Marginal Cost

Per tile 17–20 calcolare:

```text
distance_from_core
distance_from_worker_home
movement_actions_per_harvest
movement_actions_per_cycle
```

Confrontare con il working set core.

---

# 19. Revenue Curve Over Time

Produrre curve cumulative:

```text
turn -> crop revenue X1.6
turn -> crop revenue X1.7
```

e:

```text
turn -> delta cumulative revenue
```

Individuare il momento in cui X1.7 comincia realmente a guadagnare rispetto a X1.6.

Se il delta diventa positivo soltanto molto tardi, è forte evidenza di late activation.

---

# 20. Marginal Capacity Activation Curve

Produrre:

```text
turn -> number of active marginal tiles
turn -> marginal tile cumulative revenue
```

Vogliamo vedere:

```text
0 -> 1 -> 2 -> 3 -> 4 marginal tiles
```

e quando ciascuna diventa economicamente produttiva.

---

# 21. Benchmark Horizon Counterfactual

Senza modificare la strategia, stimare diagnosticamente:

> Se l'episodio durasse più a lungo, Worker #5 recupererebbe il proprio costo?

Usare esclusivamente il rendimento osservato, non simulazioni speculative.

Ad esempio:

```text
observed revenue rate after stabilization
```

per stimare il payback period.

Etichettare chiaramente come:

```text
DIAGNOSTIC EXTRAPOLATION
```

---

# 22. Decision Rule

Classificare la causa primaria.

## Caso A — Late activation

Se:

- Worker #5 viene assunto tardi;
- tile 17–20 entrano tardi;
- pochi cicli MELON restano disponibili;

raccomandazione:

```text
X1.8 EARLIER WORKFORCE / CAPACITY ACTIVATION
```

NON aggiungere Worker #6.

---

# 23. Caso B — Worker underutilized

Se:

- Worker #5 è spesso idle;
- tile marginali non disponibili;
- capacity utilization bassa;

raccomandazione:

```text
X1.8 CAPACITY UTILIZATION FIX
```

---

# 24. Caso C — Marginal spatial inefficiency

Se:

- tile 17–20 richiedono troppo movement;
- revenue/action molto inferiore;

raccomandazione:

```text
X1.8 CLUSTER / LOCALITY OPTIMIZATION
```

---

# 25. Caso D — Capital crowding-out

Se Worker #5:

- ritarda land;
- ritarda Cow;
- riduce seed liquidity;

raccomandazione:

```text
X1.8 HIRING / CAPITAL TIMING
```

---

# 26. Caso E — Marginal worker genuinely profitable and timely

Solo se:

- Worker #5 è produttivo;
- tile 17–20 attive presto;
- revenue/action comparabile;
- marginal contribution positiva;
- capacity utilization alta;

allora:

```text
PROCEED E12-X1.8 — 6 CROP WORKERS @ 4 TILES/WORKER
```

---

# 27. Nessun BUILD strategico

D3 è audit puro.

Consentito:

- telemetry;
- trace scripts;
- report;
- comparative execution;
- diagnostic calculations.

Vietato:

- modificare HIRE threshold;
- aggiungere Worker #6;
- cambiare tiles/worker;
- cambiare crop portfolio;
- cambiare Q1/Q2;
- cambiare Cow scaling.

---

# 28. Output richiesto

Restituire:

### A. Worker #5 identity and hire timing
### B. Tile 17–20 lifecycle table
### C. Time-to-revenue analysis
### D. Remaining-cycle analysis
### E. Worker #5 action budget
### F. Marginal crop revenue
### G. Marginal Worker P&L
### H. Q1/Q2 interaction
### I. Cow interaction
### J. Spatial efficiency
### K. Cumulative revenue delta curve
### L. Root cause classification
### M. Single recommendation

La raccomandazione deve essere una sola:

```text
X1.8 EARLIER WORKFORCE / CAPACITY ACTIVATION
```

oppure:

```text
X1.8 CAPACITY UTILIZATION FIX
```

oppure:

```text
X1.8 CLUSTER / LOCALITY OPTIMIZATION
```

oppure:

```text
X1.8 HIRING / CAPITAL TIMING
```

oppure:

```text
PROCEED E12-X1.8 — 6 CROP WORKERS @ 4 TILES/WORKER
```

---

# 29. Obiettivo finale dell'audit

Dobbiamo poter rispondere con numeri a:

> **Le quattro tile aggiuntive di X1.7 rendono poco perché arrivano troppo tardi, perché sono poco utilizzate, perché costano troppo da raggiungere, oppure perché il quinto worker sottrae capitale ad altre parti della farm?**

Solo dopo questa risposta decidiamo se scalare a 6 crop worker.

---

# Approval

Questo prompt autorizza:

1. audit X1.6 vs X1.7;
2. telemetry;
3. esecuzioni comparative;
4. report D3.

NON autorizza modifiche strategiche.

---

# Principio guida

> **Prima di aggiungere altra capacità, misurare il rendimento marginale della capacità appena aggiunta. Il quinto crop worker ha aumentato la capacità teorica del 25% ma il denaro solo dell'1.7%: dobbiamo capire dove si perde quel rendimento prima di aggiungere il sesto.**
