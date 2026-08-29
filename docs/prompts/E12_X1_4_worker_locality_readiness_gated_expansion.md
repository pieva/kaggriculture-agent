# E12-X1.4 — Worker Locality & Readiness-Gated Expansion

## Obiettivo

Le verifiche D1 e successive hanno chiarito il collo di bottiglia reale di E12-X1.3:

- non esistono pozzi o altra infrastruttura idrica;
- `WATER` è un'azione diretta del worker sulla tile coltivata;
- X1.3 ha raggiunto la massa geometrica target (~24–25 crop tile), ma:
  - il **61.4%** delle azioni worker è stato speso in movimento;
  - soltanto il **38.6%** delle azioni è rimasto produttivo;
  - circa il **72% delle colture piantate** non è arrivato a raccolto;
  - il rapporto harvest/planted si è fermato intorno al **28%**;
  - l'espansione Q1/Q2/Q3 è avvenuta troppo presto rispetto alla capacità operativa disponibile;
  - sul seed 200, il fallback a `CARROT` ha sovrascritto tile WHEAT dedicate al feed, azzerando il MILK.

Quindi E12-X1.4 NON deve modificare la geometria di fondo né rimettere in discussione Cow #1.

Il nuovo esperimento deve risolvere due problemi coordinati:

1. **worker locality**;
2. **expansion readiness**.

Nome:

**E12-X1.4 — Worker Locality & Readiness-Gated Expansion**

---

## 1. Ipotesi X1.4

### H12-X1.4

Mantenendo:

- opening livestock;
- Cow #1;
- feed loop;
- geometria centered;
- crop mass target comparabile a X1.7;

e introducendo:

- assegnazione locale dei worker;
- espansione dei Quarter subordinata a soglie operative reali;
- protezione assoluta dei tile WHEAT feed-critical;

è possibile ridurre drasticamente il movement overhead, aumentare il productive action ratio e portare il crop harvest yield verso i livelli osservati nei top.

Obiettivo tecnico:

```text
movement_ratio <= 25–30%
productive_action_ratio >= 70–75%
harvest_yield_ratio >= 75–80%
```

Queste soglie sono target empirici/diagnostici, non valori da hardcodare alla cieca senza verifica.

---

## 2. Principio fondamentale

NON implementare:

```text
if day >= 4: buy Q1
if day >= 8: buy Q2
```

I giorni osservati nei top sono **outcome**, non trigger.

La policy corretta deve essere:

> **Inferisci una readiness condition che faccia emergere naturalmente un timing simile a quello dei top.**

Il timing Day 4–5 per Q1 e Day 8–10 per Q2 deve essere usato soltanto come benchmark di validazione ex post.

---

## 3. Readiness-Gated Expansion

Definire una funzione concettuale:

```text
EXPANSION_READY(current_region)
```

basata su quattro famiglie di indicatori.

### A. Operational Health

Misurare su una finestra recente, preferibilmente rolling:

- `movement_ratio`
- `productive_action_ratio`
- `idle/pass ratio`

Gate target iniziale:

```text
movement_ratio <= 0.30
productive_action_ratio >= 0.70
```

Preferibile:

```text
movement_ratio <= 0.25
productive_action_ratio >= 0.75
```

Non usare una singola osservazione istantanea: utilizzare una finestra temporale sufficientemente stabile.

---

## 4. Crop Control

Prima di espandere, la superficie attuale deve essere realmente sotto controllo.

Misurare:

- planted;
- watered;
- harvested;
- withered/dead;
- backlog WATER;
- backlog HARVEST;
- backlog PLANT;
- backlog DIG/weed-management.

Definire:

```text
recent_harvest_yield_ratio =
recent_harvested /
max(recent_planted, 1)
```

Target:

```text
recent_harvest_yield_ratio >= 0.75–0.80
```

Aggiungere una condizione:

```text
critical_water_backlog == 0
```

o equivalente, se il backlog può essere misurato direttamente.

Se esistono crop già a rischio di drought, NON espandere.

---

## 5. Local Saturation

Non comprare nuovo land mentre l'area corrente contiene ancora capacità centered inutilizzata e facilmente gestibile.

Definire per l'area attualmente accessibile:

```text
local_utilization =
active_productive_tiles /
eligible_centered_tiles
```

La soglia definitiva deve derivare dalla geometria e dall'esperienza X1.7/top.

Indicativamente, verificare readiness quando:

```text
local_utilization >= 0.70–0.80
```

ma NON hardcodare questa soglia prima di controllare la distribuzione reale dei tile.

L'obiettivo è:

> aprire nuovo spazio quando quello corrente è sufficientemente sfruttato, non quando esiste semplicemente il denaro per comprarlo.

---

## 6. Financial Readiness

La precedente espansione X1.3 ha portato la liquidità fino a circa `$50`.

Questo non deve ripetersi.

Definire:

```text
financial_ready =
cash >= land_cost
      + next_seed_cycle_cost
      + mandatory_feed_cost
      + required_hire_cost
      + immediate_operating_cost
      + small_safety_margin
```

Il `small_safety_margin` deve essere minimo e giustificato.

NON utilizzare grandi cash reserve arbitrarie.

Obiettivo:

> comprare il Quarter solo se il sistema può iniziare a sfruttarlo senza interrompere il ciclo produttivo esistente.

---

## 7. Workforce Capacity Readiness

Non aprire una nuova area se nessun worker può assorbirla localmente.

Definire:

```text
workforce_ready =
exists worker capacity for new region
OR
hire can be funded sustainably
```

Il nuovo worker deve essere associato a una regione/area, non lasciato libero di attraversare continuamente l'intera mappa.

---

## 8. Worker Locality

Implementare un sistema di **regional worker assignment**.

Non è necessario hardcodare esattamente:

```text
Farmer -> Q0
Hand1 -> Q0
Hand2 -> Q1
...
```

ma la logica deve minimizzare attraversamenti cross-map.

Ogni worker deve avere:

- `home_region`;
- `assigned_tiles`;
- `current_local_backlog`;
- possibilità di essere riallocato solo quando esiste una ragione forte.

Obiettivo:

```text
worker performs most actions within local region
```

---

## 9. Reassignment Policy

La locality non deve diventare una gabbia rigida.

Consentire reassignment quando:

- la regione locale è sotto controllo;
- un'altra regione ha backlog critico;
- non esiste worker locale disponibile;
- il costo di trasferimento viene compensato da un numero sufficiente di azioni produttive successive.

Evitare oscillazioni:

```text
Q0 -> Q2 -> Q0 -> Q3 -> Q1
```

Introdurre, se necessario, un hysteresis/cooldown logico per reassignment.

---

## 10. Movement Cost Awareness

Ogni assegnazione task deve considerare:

```text
task_value
-
movement_cost
```

o una proxy equivalente.

Preferire:

- task locali;
- cluster di azioni consecutive;
- percorsi che consentono più operazioni produttive vicine.

Evitare di inviare un worker lontano per una singola azione marginale.

---

## 11. Local Task Queues

Per ogni regione/worker creare o derivare una queue locale con priorità:

```text
1. emergency WATER
2. HARVEST ready
3. WHEAT/feed critical
4. required DIG/weed control
5. PLANT
6. non-critical maintenance
```

Le priorità globali devono evitare drought.

In particolare:

> una nuova espansione non può avere priorità su WATER/HARVEST critici nell'area corrente.

---

## 12. Feed Tile Priority Lock

Implementare come fix causale diretto.

I tile feed-critical:

`(2,3), (2,4), (1,3), (1,4)`

o la configurazione effettiva derivata dalla strategia devono essere marcati esplicitamente come:

```text
FEED_CRITICAL_WHEAT_TILE
```

Su questi tile:

- `CARROT` fallback vietato;
- altri crop cash vietati;
- WHEAT ha priorità assoluta quando serve feed;
- la liquidità bassa NON può cambiare crop type;
- la tile può uscire dal feed role solo tramite decisione esplicita della state machine.

Questo corregge il bug osservato sul seed 200.

---

## 13. Cow #1

Preservare:

- Cow #1 early;
- pasture centered;
- FEED;
- MILK;
- SELL;
- zero starvation.

Non aggiungere Cow #2 prima che:

```text
crop_system_stable == True
AND expansion/readiness metrics are healthy
AND active_crop_tiles >= 24
```

Per X1.4 Cow #2 rimane secondaria.

---

## 14. Q1 Readiness

Definire Q1 readiness come:

```text
Q1_READY =
operational_health_good
AND crop_control_good
AND local_saturation_good
AND financial_ready
AND workforce_ready
```

Registrare il turn in cui Q1 diventa READY e il turn in cui viene effettivamente acquistato.

Poi confrontare ex post il timing con il top-player benchmark.

Se emerge naturalmente circa Day 4–5, è un segnale favorevole.

Se emerge prima o dopo ma con metriche operative migliori, NON forzarlo verso Day 4–5.

---

## 15. Q2 Readiness

Q2 deve richiedere che Q1 sia **assorbito produttivamente**.

Definire:

```text
Q2_READY =
Q1_owned
AND Q1_region_utilization >= threshold
AND recent_harvest_yield_ratio healthy
AND movement_ratio healthy
AND productive_action_ratio healthy
AND financial_ready
AND workforce_ready
```

Il timing Day 8–10 resta benchmark, non trigger.

---

## 16. Q3

Applicare lo stesso principio.

Non aprire Q3 solo perché Q2 esiste.

Ogni nuovo Quarter deve superare il medesimo gate di readiness.

---

## 17. Rolling Metrics

Implementare rolling windows per evitare decisioni rumorose.

Suggerimento da validare:

```text
last 24 turns
last 48 turns
```

Calcolare almeno:

- movement ratio;
- productive action ratio;
- water actions;
- harvest actions;
- planted;
- harvested;
- crop deaths;
- backlog;
- local utilization.

La finestra precisa può essere adattata, ma deve essere coerente e documentata.

---

## 18. Drought Telemetry

Aggiungere contatori espliciti:

- crop planted;
- crop watered;
- crop missed-water;
- crop died/withered;
- crop harvested;
- crop cycles completed.

Per ogni crop death, se tecnicamente determinabile, registrare:

```text
death_reason = DROUGHT | OTHER | UNKNOWN
```

Questo deve permettere di verificare direttamente che X1.4 riduca il problema diagnosticato.

---

## 19. Worker Telemetry

Per ogni worker registrare:

- home region;
- current region;
- movement actions;
- productive actions;
- WATER;
- HARVEST;
- PLANT;
- DIG;
- livestock actions;
- reassignment count;
- tiles served;
- average Manhattan distance per task.

Produrre anche aggregati globali.

---

## 20. Expansion Event Telemetry

Ogni acquisto Q1/Q2/Q3 deve produrre un evento:

```text
QUADRANT_UNLOCK
```

con:

- turn;
- day;
- cash before;
- cash after;
- movement ratio rolling;
- productive action ratio rolling;
- harvest yield ratio rolling;
- local utilization;
- active crop tiles;
- worker count;
- backlog;
- feed buffer.

Questo è necessario per capire quale soglia ha causato l'espansione.

---

## 21. Pre-Build Validation

Prima del BUILD:

1. identifica come vengono assegnati oggi i task ai worker;
2. misura cross-region reassignment;
3. identifica dove inserire locality senza riscrivere l'intero planner;
4. identifica come calcolare rolling metrics;
5. identifica l'esatto punto decisionale BUY_LAND;
6. verifica i feed-critical tiles reali;
7. definisci Q1/Q2/Q3 readiness policy.

Puoi procedere direttamente al BUILD dopo questa verifica.

---

## 22. Test

Aggiungere test almeno per:

1. WHEAT feed-critical non sostituibile da CARROT;
2. worker preferisce task locale a task remoto equivalente;
3. worker può essere riallocato se regione locale è idle;
4. Q1 bloccato con harvest yield basso;
5. Q1 bloccato con movement ratio alto;
6. Q1 bloccato con water backlog critico;
7. Q1 consentito quando readiness completa;
8. Q2 richiede utilizzo produttivo di Q1;
9. nuovo land non porta cash sotto operating requirement;
10. Cow #1 continua a produrre;
11. nessuna regressione suite.

Eseguire:

`.venv\Scripts\pytest.exe tests/`

---

## 23. Stage A0

Seed `0`.

A0 PASS soltanto se:

```text
Cow #1 productive
AND zero starvation
AND movement_ratio < X1.3
AND productive_action_ratio > X1.3
AND harvest_yield_ratio materially > 28%
AND crop deaths materially reduced
AND feed tiles preserved
```

Target preferito:

```text
movement <= 30%
productive >= 70%
harvest yield >= 75%
```

Non è necessario che tutti i target ideali siano raggiunti immediatamente, ma il miglioramento deve essere sostanziale.

Se movement resta >50% o harvest yield resta vicino al 28%:

**A0 FAIL — NON eseguire Stage B.**

---

## 24. Stage A1

Seed `100`.

Stesso gate.

Stage B solo dopo doppio PASS.

---

## 25. Stage B

Seed:

`0, 100, 200, 300, 400`

stessi opponent.

Confrontare:

- E12-X1.4;
- E12-X1.3;
- E12-X1.2;
- E11-X1.7.

---

## 26. Metriche Stage B

### Financial
- Mean Final Money;
- Median;
- std;
- min/max;
- delta vs X1.3;
- delta vs X1.7;
- paired win rate.

### Efficiency
- movement ratio;
- productive action ratio;
- harvest yield ratio;
- crop deaths;
- harvest count;
- planted count.

### Expansion
- Q1 turn/day;
- Q2 turn/day;
- Q3 turn/day;
- readiness metrics at unlock.

### Workforce
- worker count;
- local action ratio;
- reassignment count;
- distance per productive action.

### Livestock
- Cow #1;
- milk units;
- milk revenue;
- starvation;
- feed buffer failures.

---

## 27. Top Benchmark Validation

Dopo Stage B confrontare il timing emerso con i top.

Non chiedere:

> "Abbiamo comprato Q1 esattamente Day 4?"

Chiedere:

> "La readiness policy produce una traiettoria simile ai top in termini di movement, yield, cash e utilization?"

Timing top:

- Q1 circa Day 4–5;
- Q2 circa Day 8–10;

rimane un riferimento osservativo.

---

## 28. Interpretazione

### A — Movement ridotto, yield ancora basso
Problema residuo di crop scheduling/WATER priority.

### B — Yield recuperato, money ancora basso
Passare a crop economics / crop mix / harvest monetization.

### C — Yield e movement recuperati, espansione troppo lenta
Readiness gate troppo conservativo.

### D — Yield e movement recuperati, espansione troppo precoce
Financial/local saturation gate troppo permissivo.

### E — Yield >75%, movement <30%, money cresce nettamente
Conferma della diagnosi D1.

### F — X1.4 si avvicina/supera X1.7
Passare a ottimizzazione hybrid finale / external validation.

---

## 29. Conclusioni vietate

Non concludere che:

- Q1 deve essere comprato Day 4;
- Q2 deve essere comprato Day 8;
- i giorni osservati nei top siano la policy;
- Cow #1 sia il problema;
- servano pozzi.

Il motore non contiene WELL.

La variabile corretta è:

**capacità operativa di irrigare, raccogliere e mantenere produttivo il terreno già aperto.**

---

## 30. Provenance

Mantenere:

- variant ID corretto `E12-X1.4`;
- source hash;
- config hash;
- seed;
- opponent;
- SHA-256 match 100%.

Nessun tuning tra seed Stage B.

---

## 31. Documentazione

Aggiornare dopo risultati verificati:

- `docs/versions/E12_X1_4_worker_locality_readiness_expansion.md`
- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`

E11-X1.7 rimane submission champion finché X1.4 non dimostra vantaggio locale credibile.

---

## 32. Output richiesto

Restituisci:

### A. Pre-build locality diagnosis
### B. Readiness formula
### C. Worker locality architecture
### D. Feed priority fix
### E. Tests
### F. A0
### G. A1
### H. Stage B
### I. Comparison vs top timing
### J. Recommendation

Raccomandazione finale:

- `REWORK WORKER LOCALITY`
- `REWORK EXPANSION READINESS`
- `PROCEED E12-X1.5 CROP PRODUCTIVITY`
- `PROCEED E12-X1.5 HYBRID ECONOMICS`
- `E12 LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION`

---

## Approval

Questo prompt autorizza:

1. diagnosi;
2. BUILD X1.4;
3. test;
4. A0;
5. A1;
6. Stage B dopo doppio PASS.

Non richiedere approvazioni intermedie.

---

## Principio guida

> **Non espandere quando arriva il giorno giusto. Espandere quando la farm dimostra di saper controllare produttivamente l'area corrente e possiede capacità marginale reale per assorbire quella successiva.**
