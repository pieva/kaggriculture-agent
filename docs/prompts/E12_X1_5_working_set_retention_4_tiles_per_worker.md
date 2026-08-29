# E12-X1.5 — Working Set Retention @ 4 Tiles/Worker

## Obiettivo

E12-D2 ha chiarito il problema operativo principale della linea E12:

- una crop lasciata senza acqua per 2 giorni consecutivi converte a `WEED`;
- il recupero richiede almeno `DIG + PLANT + WATER`;
- questo genera maintenance debt;
- la maintenance debt sottrae action budget alle crop ancora sane;
- il sistema può quindi entrare in una spirale di collasso operativo.

L'audit D2 ha inoltre stimato empiricamente una capacità prudenziale iniziale pari a circa:

**4 tile produttive sostenibili per worker attivo.**

Per E12-X1.5 questo valore deve essere trattato come **vincolo sperimentale fisso**, NON come parametro da ottimizzare.

Nome esperimento:

**E12-X1.5 — Working Set Retention @ 4 Tiles/Worker**

L'obiettivo è molto preciso:

> **verificare se una farm ibrida cow-first, centered e mantenuta entro la capacità operativa di 4 tile per worker riesce finalmente a superare il benchmark canonico E11-X1.7 = $28,083.80 Mean Final Money.**

Non ottimizzare ancora `tiles/worker`.

---

## 1. Benchmark economico canonico

Usare come baseline ufficiale:

**E11-X1.7 — Corner-Pruned 26t**

- Mean Final Money: `$28,083.80`
- Median: `$30,081.00`
- Peak: `$33,371.00`

IMPORTANTE:

I valori economici prodotti dall'audit diagnostico D2 NON devono sostituire il benchmark canonico, perché l'audit ha prodotto valori non equivalenti alle run ufficiali.

La valutazione economica X1.5 deve usare esclusivamente il benchmark runner canonico e provenance verificata.

---

## 2. Ipotesi X1.5

### H12-X1.5

Se:

1. il working set viene limitato a `4 × active_workers`;
2. ogni crop del working set viene difesa preventivamente dal drought;
3. le weed interne al working set vengono recuperate rapidamente;
4. le weed esterne vengono ignorate;
5. l'espansione viene subordinata alla capacità manutentiva reale;

allora la farm ibrida può mantenere una superficie produttiva stabile abbastanza a lungo da convertire la massa fisica in reddito.

---

## 3. Working Set Capacity — vincolo fisso

Implementare:

```text
working_set_capacity = 4 * active_workers
```

Per X1.5 questa formula è FISSA.

NON testare:

- 4.5 tile/worker;
- 5 tile/worker;
- adaptive tiles/worker;
- soglie diverse per Quarter;
- tuning per seed.

Prima vogliamo sapere se **4 tile/worker** produce finalmente una farm stabile e competitiva.

---

## 4. Working Set Definition

Una tile appartiene al working set quando:

- è assegnata alla crop engine;
- deve essere mantenuta nel ciclo produttivo;
- la strategia intende difenderla da weed/drought;
- consuma capacità manutentiva.

Distinguere:

```text
OWNED_LAND
AVAILABLE_TILE
WORKING_SET_TILE
ACTIVE_CROP_TILE
WEED_INSIDE_WORKING_SET
WEED_OUTSIDE_WORKING_SET
```

L'acquisto di terreno NON implica automaticamente ingresso nel working set.

---

## 5. Working Set Admission Gate

Una nuova tile può entrare nel working set soltanto se:

```text
current_working_set_size < 4 * active_workers
```

e contemporaneamente:

- nessun emergency WATER backlog;
- weed backlog interno sotto controllo;
- feed loop stabile;
- seed/cash sufficiente;
- worker locality compatibile.

Se la capacità è esaurita:

```text
DO NOT ADD NEW PRODUCTIVE TILE
```

anche se esistono land, seed e cash disponibili.

---

## 6. Priorità operativa X1.5

La task priority deve essere orientata alla **retention**.

Ordine concettuale:

```text
1. EMERGENCY WATER
2. TIME-CRITICAL HARVEST
3. WORKING-SET WEED RECOVERY
4. FEED-CRITICAL WHEAT
5. NORMAL WATER
6. NORMAL HARVEST
7. REPLANT / PLANT
8. WORKING SET EXPANSION
9. LAND EXPANSION
10. NON-CRITICAL TASKS
```

La gerarchia esatta deve rispettare le meccaniche del motore, ma il principio deve essere inequivocabile.

---

## 7. Emergency WATER

Qualsiasi crop del working set con:

```text
consecutive_unwatered >= 1
```

deve diventare **ABSOLUTE EMERGENCY**.

Questa azione deve precedere:

- DIG;
- PLANT;
- nuova espansione;
- land purchase;
- task economici marginali;
- movement non urgente.

Obiettivo:

> nessuna crop del working set deve raggiungere `consecutive_unwatered >= 2`.

Telemetria obbligatoria:

- emergency water candidates;
- emergency water actions;
- missed emergency water;
- crops lost after emergency state.

---

## 8. Weed Recovery dentro il Working Set

Una weed dentro il working set è maintenance debt.

Policy:

```text
WEED_INSIDE_WORKING_SET
    ->
DIG
    ->
REPLANT
    ->
WATER
```

Il recupero deve essere prioritario ma NON deve precedere una crop viva in emergency WATER.

Quindi:

```text
live crop at risk > weed recovery
```

Registrare:

- turn weed detected;
- turn DIG;
- turn replanted;
- turn watered;
- recovery time;
- recovery actions.

---

## 9. Weed fuori dal Working Set

Regola forte:

> **Ignorare completamente le weed fuori dal working set**, salvo che la tile stia per essere ammessa nel working set.

Non sprecare action budget per "pulire la farm".

Il terreno può rimanere infestato se non è attualmente necessario alla produzione.

---

## 10. Feed Tiles

Mantenere il fix già verificato:

- feed-critical tiles restano WHEAT;
- fallback `CARROT` vietato;
- cash shortage non può sostituire WHEAT;
- feed buffer preservato.

Cow #1 deve rimanere:

- attiva;
- nutrita;
- produttiva;
- zero starvation.

---

## 11. Cow Scaling

Per X1.5:

- Cow #1: obbligatoria;
- Cow #2: NON prioritaria;
- Cow #3/#4: disabilitate.

Cow #2 può essere consentita soltanto se:

```text
working_set_retention is healthy
AND crop system is stable
AND active_workers provide unused working-set capacity
AND feed buffer is sufficient
```

Se non viene mai acquistata, non è un fallimento.

---

## 12. Workforce

Mantenere worker locality se non interferisce con retention.

La capacità lavorativa determina direttamente il working set:

```text
1 worker -> 4 tiles
2 workers -> 8 tiles
3 workers -> 12 tiles
4 workers -> 16 tiles
5 workers -> 20 tiles
6 workers -> 24 tiles
```

Questa è la capacity envelope X1.5.

NON superarla.

---

## 13. Hiring Readiness

Assumere un worker aggiuntivo significa aumentare la capacità teorica di 4 tile.

Ma HIRE deve avvenire soltanto se:

- cash sostenibile;
- backlog corrente sotto controllo;
- il nuovo worker può essere utilizzato localmente;
- esiste futura domanda produttiva.

Non assumere worker solo per aumentare artificialmente il cap.

---

## 14. Land Unlock vs Working Set Expansion

Separare rigorosamente:

### LAND_UNLOCK
Acquisto Q1/Q2/Q3.

### WORKING_SET_EXPANSION
Aggiunta di tile realmente mantenute.

È consentito possedere più land di quanto si coltiva.

Non è consentito allargare il working set oltre:

```text
4 * active_workers
```

---

## 15. Expansion Readiness

Per Q1/Q2/Q3 mantenere il principio readiness-gated.

Ma la condizione più importante ora diventa:

```text
working_set_stable
```

Definire almeno:

```text
working_set_stable =
no_emergency_water_backlog
AND weed_inside_ws_backlog manageable
AND recent_crop_loss low
AND retention high
```

Il timing Day 4–7 / Day 8–10 osservato nei top resta solo benchmark ex post.

---

## 16. Retention KPI

Aggiungere come metriche primarie:

### Sustained Productive Tiles

```text
sustained_productive_tiles
```

### Productive Surface Retention

```text
retention =
sustained_productive_tiles /
working_set_target_tiles
```

### Weed Penetration

```text
weed_penetration =
weed_inside_working_set /
working_set_target_tiles
```

### Crop Loss Rate

```text
crop_loss_rate =
crops_lost_to_weed_or_drought /
crops_entered_working_set
```

### Surface Churn

```text
surface_churn =
working_set_state_transitions /
working_set_size
```

---

## 17. Target operativo

Per considerare X1.5 stabile:

```text
Productive Surface Retention >= 90%
```

preferibile:

```text
>= 95%
```

e:

```text
weed penetration inside working set <= 10%
```

preferibile:

```text
<= 5%
```

e:

```text
crops lost to drought materially reduced vs X1.4
```

---

## 18. Worker Efficiency Metrics

Continuare a misurare:

- movement ratio;
- productive action ratio;
- water actions;
- harvest actions;
- weed recovery actions;
- replant actions;
- idle actions.

Target preferito:

```text
movement <= 30–35%
productive >= 65–70%
```

Ma X1.5 deve privilegiare retention rispetto a massimizzare astrattamente il productive ratio.

---

## 19. Day-by-Day Telemetry

Per Day 1–30 registrare almeno:

- cash;
- workers;
- working_set_capacity;
- working_set_target;
- sustained_productive_tiles;
- active_crop_tiles;
- weed_inside_ws;
- weed_outside_ws;
- retention;
- weed penetration;
- crops lost to drought;
- crops lost to weed;
- weeds recovered;
- emergency water backlog;
- normal water backlog;
- harvest backlog;
- maintenance debt;
- movement ratio;
- productive ratio;
- milk revenue;
- crop revenue;
- Q1/Q2/Q3.

---

## 20. Working Set Capacity Invariant

Aggiungere assert/telemetry:

```text
working_set_size <= 4 * active_workers
```

Se violato:

- registrare `CAPACITY_VIOLATION`;
- Stage A0 deve fallire.

Nessuna violazione è ammessa in X1.5.

---

## 21. Pre-Build Diagnosis

Prima del BUILD:

1. individua dove il planner aggiunge tile al working set;
2. identifica come contare active workers;
3. identifica la priorità WATER corrente;
4. identifica come leggere `consecutive_unwatered`;
5. identifica weed inside/outside working set;
6. identifica come evitare DIG fuori working set;
7. verifica feed tiles;
8. verifica che il benchmark runner canonico sia distinto dal tooling D2.

Puoi procedere direttamente al BUILD.

---

## 22. Test

Aggiungere test almeno per:

1. capacity = 4 × workers;
2. quinta tile vietata con 1 worker;
3. nona tile vietata con 2 workers;
4. emergency WATER prioritaria su crop con 1 giorno senza acqua;
5. crop emergency WATER prioritaria su weed recovery;
6. weed inside working set recuperata;
7. weed outside working set ignorata;
8. feed tile resta WHEAT;
9. Cow #1 resta produttiva;
10. land unlock non forza working set expansion;
11. nessuna capacity violation;
12. suite completa senza regressioni.

Eseguire:

`.venv\Scripts\pytest.exe tests/`

---

## 23. Stage A0

Seed `0`.

A0 PASS soltanto se:

- capacity invariant sempre rispettata;
- Cow #1 produttiva;
- zero starvation;
- retention >= 90% nella fase stabile;
- weed penetration <= 10% nella fase stabile;
- crop loss da drought drasticamente ridotto;
- nessun maintenance collapse;
- provenance valida.

Se retention resta bassa o il working set collassa:

**A0 FAIL — NON eseguire Stage B.**

---

## 24. Stage A1

Seed `100`.

Stessi gate.

Stage B solo dopo doppio PASS.

---

## 25. Stage B Canonico

Usare il benchmark canonico sui paired seed:

`0, 100, 200, 300, 400`

con gli stessi opponent storici.

Confrontare:

- E12-X1.5;
- E12-X1.4;
- E12-X1.3;
- E12-X1.2;
- E11-X1.7 canonico.

IMPORTANTE:

Per X1.7 usare i risultati benchmark canonici validati, NON i valori prodotti dall'audit D2.

---

## 26. Metriche Stage B

### Economiche
- Mean Final Money;
- Median;
- std `ddof=1`;
- min/max;
- delta assoluto vs `$28,083.80`;
- delta percentuale;
- paired win rate vs X1.7.

### Retention
- mean sustained productive tiles;
- retention;
- weed penetration;
- crop loss;
- surface churn;
- recovery time.

### Workforce
- worker count;
- working-set capacity;
- capacity utilization;
- movement ratio;
- productive ratio.

### Livestock
- Cow #1;
- milk units;
- milk revenue;
- starvation.

### Expansion
- Q1/Q2/Q3 timing;
- land owned;
- working set actually used.

---

## 27. Primary Success Criterion

Il successo economico principale è:

```text
Mean Final Money E12-X1.5 > $28,083.80
```

Questo è il primo vero tentativo E12 in cui vogliamo verificare direttamente il superamento del tetto di X1.7 con una farm ibrida operativamente stabile.

---

## 28. Secondary Success Criterion

Se X1.5 NON supera `$28,083.80`, ma ottiene:

```text
retention >= 90%
weed penetration <= 10%
zero maintenance collapse
stable Cow #1
```

allora il problema operativo può essere considerato sostanzialmente risolto.

In quel caso il gap residuo diventa realmente economico/strategico.

Solo allora sarà sensato ottimizzare:

- tiles/worker;
- crop mix;
- Cow #2/#3/#4;
- land timing;
- economic thresholds.

---

## 29. Interpretazione

### A — Retention ancora bassa
`REWORK WORKING SET RETENTION`

### B — Retention alta, money < $20k
Problema economico/crop mix/workforce cost ancora forte.

### C — Retention alta, money $20k–$28k
Base operativa sana; procedere con ottimizzazione.

### D — Retention alta, money > $28,083.80
E12 supera il champion locale.

### E — Mean > X1.7 e paired win rate robusto
`E12 LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION`

---

## 30. Nessuna ottimizzazione tiles/worker

Durante X1.5 è vietato modificare:

```text
4 tiles / worker
```

anche se un singolo seed sembra poter sostenere più tile.

L'ottimizzazione della capacità verrà fatta soltanto DOPO aver ottenuto una baseline ibrida stabile.

---

## 31. Provenance

Mantenere:

- Run ID corretto `E12-X1.5-*`;
- source hash;
- config hash;
- seed;
- opponent;
- SHA-256 100% match.

Non mescolare tooling diagnostico D2 con benchmark canonico.

---

## 32. Submission

NON sostituire automaticamente E11-X1.7 nella submission.

Solo se:

```text
Mean X1.5 > 28,083.80
AND
paired results are credible
AND
provenance verified
```

preparare E12-X1.5 come nuovo candidate submission.

---

## 33. Documentazione

Aggiornare dopo verifica:

- `docs/versions/E12_X1_5_working_set_retention_4_tiles_per_worker.md`
- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`

---

## 34. Output richiesto

Restituisci:

### A. Pre-build analysis
### B. Working-set architecture
### C. Priority policy
### D. Tests
### E. A0
### F. A1
### G. Canonical Stage B
### H. Retention analysis
### I. Economic comparison vs E11-X1.7
### J. Recommendation

Raccomandazione finale una sola:

- `REWORK WORKING SET RETENTION`
- `PROCEED E12-X1.6 ECONOMIC OPTIMIZATION`
- `PROCEED E12-X1.6 CAPACITY OPTIMIZATION`
- `E12 LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION`

---

## Approval

Questo prompt autorizza:

1. diagnosi;
2. BUILD X1.5;
3. test;
4. A0;
5. A1;
6. benchmark canonico Stage B dopo doppio PASS.

Non richiedere approvazioni intermedie.

---

## Principio guida

> **Per X1.5 non vogliamo coltivare il massimo numero di tile possibile. Vogliamo mantenere produttive tutte le tile che decidiamo di coltivare, con un limite conservativo e fisso di 4 tile per worker, e verificare se una farm ibrida finalmente stabile riesce a superare $28,083.80.**
