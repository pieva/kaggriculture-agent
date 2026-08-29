# E12-X1.6 — Functional Workforce & Hybrid Economic Scaling

## Obiettivo

Le osservazioni più recenti sui replay dei top player aggiungono un elemento architetturale importante:

- il **livestock core 2×2** è mantenuto vicino all'origine/shed;
- nel 2×2 sembra esserci **presidio umano quasi continuo**;
- gli altri worker si allontanano progressivamente per gestire le colture;
- già nelle primissime fasi risultano presenti circa **5 persone**;
- la superficie livestock viene progressivamente saturata con più animali;
- le crop vengono sviluppate nella corona circostante.

E12-X1.5 ha inoltre dimostrato che:

- il working set crop può essere mantenuto stabile;
- il vincolo `4 crop tiles / worker` elimina il maintenance collapse;
- emergency WATER e weed control funzionano;
- Cow #1 è produttiva;
- il problema residuo non è più la sopravvivenza delle crop.

Il prossimo esperimento deve quindi testare una vera **specializzazione funzionale della workforce** e la progressiva monetizzazione del livestock core.

Nome:

**E12-X1.6 — Functional Workforce & Hybrid Economic Scaling**

---

## 1. Ipotesi X1.6

### H12-X1.6

Una farm ibrida centered può aumentare drasticamente la resa economica se:

1. il livestock core 2×2 vicino all'origine viene progressivamente saturato;
2. almeno un worker viene assegnato prioritariamente alla gestione livestock;
3. gli altri worker vengono assegnati a cluster crop locali;
4. il vincolo di capacità resta pari a:
   - `4 crop tiles per crop worker`;
5. i worker crop non vengono distolti continuamente da task livestock;
6. Cow #2/#3/#4 vengono introdotte solo quando il feed loop e il worker livestock possono sostenerle;
7. il crop working set resta stabile e protetto.

---

## 2. Distinzione funzionale della workforce

Non usare più soltanto:

```text
active_workers
```

come proxy della capacità agricola.

Definire almeno:

```text
livestock_workers
crop_workers
```

e quindi:

```text
crop_working_set_capacity = 4 * crop_workers
```

Il worker dedicato/prevalentemente dedicato al livestock NON deve essere contato automaticamente nella capacità crop.

---

## 3. Target workforce iniziale

I replay dei top mostrano circa 5 persone già molto presto.

Non hardcodare un giorno specifico, ma verificare la sostenibilità di una configurazione target iniziale del tipo:

```text
1 livestock worker
+
4 crop workers
=
5 total workers
```

La domanda non è:

> "assumere 5 worker al turn X?"

ma:

> **"quando il capitale iniziale e la pipeline operativa consentono di arrivare rapidamente a una workforce funzionalmente completa senza interrompere feed e crop retention?"**

---

## 4. Audit obbligatorio prima del BUILD

Prima di implementare X1.6, misura nel motore il costo operativo reale del livestock.

Per 1 Cow attiva registra su almeno alcuni giorni:

- FEED actions/day;
- MILK-related actions/day;
- PICKUP/PLACE se ricorrenti;
- movement actions;
- shed/market interactions;
- tempo medio del worker nel livestock core;
- idle time del worker livestock.

Ripetere concettualmente o tramite simulazione per:

- 1 Cow;
- 2 Cow;
- 3 Cow;
- 4 Cow.

Obiettivo:

> capire se un worker livestock è realmente occupato a tempo pieno o può servire anche 1–2 crop adiacenti nei periodi morti.

Non assumere una dedicazione 100% se il motore non la richiede.

---

## 5. Livestock Worker Role

Definire un worker con:

```text
role = LIVESTOCK_PRIMARY
home_region = livestock_core
```

Priorità:

```text
1. FEED critical
2. MILK collect / livestock harvest
3. livestock state maintenance
4. shed interaction necessaria
5. emergency crop task vicino al core
6. local crop support se livestock idle
```

Il worker livestock deve restare vicino all'origine e non attraversare la mappa per task marginali.

---

## 6. Crop Worker Roles

Gli altri worker devono essere:

```text
role = CROP_PRIMARY
```

con cluster locali.

Ogni crop worker gestisce massimo:

```text
4 crop tiles
```

Per X1.6 questo valore resta fisso.

Esempio:

```text
4 crop workers -> max 16 crop working-set tiles
```

La capacità crop NON include le pasture.

---

## 7. Cluster locality

Ogni crop worker deve avere:

- home cluster;
- tile assegnate;
- emergency WATER backlog locale;
- HARVEST backlog locale;
- weed recovery locale.

Preferire cluster compatti e centered.

Non ragionare necessariamente per Quarter se una geometria a cluster riduce meglio le distanze.

---

## 8. Livestock Core Saturation

Il 2×2:

```text
[(3,3), (3,4), (4,3), (4,4)]
```

resta riservato alla componente livestock.

A differenza di X1.5, X1.6 deve provare a monetizzarlo progressivamente:

```text
Cow #1
-> Cow #2
-> Cow #3
-> Cow #4
```

NON acquistare tutte e quattro insieme.

---

## 9. Cow Scaling Gate

Definire una funzione:

```text
NEXT_COW_READY
```

basata almeno su:

### Feed readiness
- WHEAT buffer sufficiente;
- feed production rate sufficiente;
- nessun rischio di starvation.

### Livestock worker readiness
- livestock task backlog sotto controllo;
- worker non già saturo;
- projected actions/day sostenibili.

### Crop stability
- retention >= 90%;
- no emergency WATER backlog persistente;
- crop working set entro `4 * crop_workers`.

### Financial readiness
- costo pasture/cow;
- feed costs;
- seed cycle;
- operating buffer.

### Core capacity
- pasture tile disponibile nel 2×2.

---

## 10. No day-based cow scaling

NON implementare:

```text
Cow #2 at Day 2
Cow #3 at Day 4
Cow #4 at Day 6
```

Il timing deve emergere dalle soglie operative.

Il replay top è benchmark ex post.

---

## 11. Crop Economics

X1.6 deve anche evitare di sprecare i crop tile stabili su colture a basso rendimento non necessarie.

Prima del BUILD, costruire una tabella economica completa di tutte le crop disponibili.

Per ogni crop:

- seed cost;
- growth days;
- regrowth behavior;
- harvest count;
- sale price;
- WATER requirements;
- worker actions per ciclo;
- expected gross revenue;
- net revenue per tile-day;
- net revenue per worker-action.

Questa tabella deve usare esclusivamente valori verificati nel motore.

---

## 12. Revenue per Worker-Action

La metrica primaria per il crop portfolio deve essere:

```text
net_revenue_per_worker_action
```

perché il worker action budget è una risorsa scarsa.

Non scegliere le crop soltanto per sale price.

---

## 13. Feed vs Cash Crops

Distinguere:

### FEED CROPS
WHEAT necessario agli animali.

### CASH CROPS
tile rimanenti, assegnati alle colture con miglior rendimento operativo compatibile con la fase.

La superficie WHEAT deve crescere in funzione del numero di Cow, non tramite costante fissa.

---

## 14. Dynamic Wheat Capacity

Definire:

```text
required_wheat_tiles = f(active_cows, feed_consumption, wheat_yield, cycle_time)
```

Mantenere un buffer sufficiente, ma evitare sovrapproduzione.

Registrare:

- wheat planted;
- wheat harvested;
- wheat consumed;
- wheat buffer;
- excess wheat sold.

---

## 15. Crop Working Set Capacity

Vincolo invariato:

```text
crop_working_set_capacity = 4 * crop_workers
```

Non aumentare a 4.5 o 5 in X1.6.

Questo è fondamentale per isolare l'effetto di:

- workforce functional specialization;
- livestock scaling;
- crop economics.

---

## 16. Hiring Strategy

L'HIRE deve essere interpretato come investimento in capacità produttiva.

Separare:

```text
hire_for_livestock
hire_for_crop_capacity
```

Un nuovo crop worker aggiunge:

```text
+4 crop tiles capacity
```

Un nuovo livestock worker aggiunge capacità di gestione animali, non tile crop.

---

## 17. Early Workforce Scaling

I replay suggeriscono che i top arrivano rapidamente a circa 5 persone.

X1.6 deve quindi evitare riserve finanziarie eccessivamente conservative che ritardino la workforce.

Ma ogni HIRE deve essere collegato a una funzione:

```text
new worker -> defined productive role
```

Non assumere worker senza task capacity da assegnare.

---

## 18. Workforce Utilization KPI

Per ogni worker registrare:

- role;
- home region;
- movement;
- crop actions;
- livestock actions;
- idle actions;
- productive actions;
- assigned tiles;
- reassignment count.

Calcolare:

```text
role_purity_ratio =
actions_in_primary_role /
total_productive_actions
```

Obiettivo:

- livestock worker prevalentemente livestock;
- crop workers prevalentemente crop.

---

## 19. Livestock Utilization KPI

Per il 2×2 registrare:

```text
livestock_core_utilization =
active_pastures /
4
```

e:

```text
livestock_revenue_per_core_tile
```

L'obiettivo è evitare di riservare 4 tile centrali e utilizzarne soltanto 1.

---

## 20. Crop Utilization KPI

Per la corona crop:

```text
crop_capacity_utilization =
active_working_set_crop_tiles /
(4 * crop_workers)
```

Target:

```text
>= 80–90%
```

senza compromettere retention.

---

## 21. Retention Invariants

Mantenere i successi X1.5:

```text
retention >= 90%
weed penetration <= 10%
no persistent emergency WATER backlog
zero maintenance collapse
```

Se livestock scaling riduce retention sotto questi livelli:

- bloccare Cow successiva;
- non sacrificare le crop.

---

## 22. Q1/Q2/Q3

Non fare tuning esplicito del land timing.

La land expansion deve restare subordinata alla capacità operativa.

Priorità:

1. saturare economicamente il core;
2. mantenere crop working set stabile;
3. aggiungere workforce;
4. espandere land quando esiste capacità reale.

---

## 23. Density Before Expansion

Principio forte:

> **Prima massimizzare la densità economica del nucleo centered, poi espandere la proprietà.**

Densità economica:

```text
milk revenue
+
crop revenue
```

per tile/worker nel core disponibile.

---

## 24. Stage A0

Seed `0`.

A0 PASS soltanto se:

- Cow #1 produttiva;
- almeno Cow #2 viene attivata se sostenibile;
- livestock worker role funziona;
- crop workers mantengono `4 tiles/worker`;
- retention >= 90%;
- weed penetration <= 10%;
- zero starvation;
- revenue > X1.5 seed 0;
- provenance valida.

Non richiedere Cow #4 in A0.

---

## 25. Stage A1

Seed `100`.

Stessi gate.

Stage B soltanto dopo doppio PASS.

---

## 26. Canonical Stage B

Seed:

`0, 100, 200, 300, 400`

stessi opponent storici.

Confrontare:

- E12-X1.6;
- E12-X1.5;
- E11-X1.7 canonical.

Baseline:

**E11-X1.7 Mean = `$28,083.80`**

---

## 27. Metriche economiche

Riportare:

- Mean Final Money;
- Median;
- std;
- min/max;
- delta vs X1.5;
- delta vs X1.7;
- paired win rate.

Separare:

```text
crop revenue
milk revenue
other revenue
```

---

## 28. Livestock Scaling Metrics

Per seed:

- Cow #1 turn;
- Cow #2 turn;
- Cow #3 turn;
- Cow #4 turn;
- final cow count;
- pasture count;
- milk units;
- milk revenue;
- feed actions;
- livestock actions;
- worker livestock utilization.

---

## 29. Crop Metrics

Per seed:

- crop workers;
- crop capacity;
- active crop tiles;
- capacity utilization;
- retention;
- weed penetration;
- crop revenue;
- crop revenue per tile;
- crop revenue per worker;
- crop revenue per worker-action;
- crop mix.

---

## 30. Workforce Metrics

Per seed:

- total workers;
- livestock workers;
- crop workers;
- hires timing;
- movement ratio;
- productive ratio;
- role purity;
- idle ratio.

---

## 31. Economic Density Metrics

Calcolare:

```text
revenue_per_owned_tile
revenue_per_working_set_tile
revenue_per_worker
revenue_per_worker_action
livestock_revenue_per_core_tile
```

Queste metriche devono spiegare se il core 2×2 viene finalmente monetizzato.

---

## 32. Primary Success Criterion

```text
Mean Final Money X1.6 > $28,083.80
```

Se superato con paired results credibili:

`E12 LOCAL CHAMPION`

---

## 33. Secondary Structural Success

Se X1.6 non supera 28k ma dimostra:

- 3–4 Cow sostenibili;
- core utilization alta;
- retention crop >= 90%;
- crop capacity utilization alta;
- revenue molto superiore a X1.5;

allora la struttura hybrid è validata e il prossimo passo potrà essere capacity optimization.

---

## 34. Interpretazione

### A — Cow scaling distrugge retention
`REWORK LIVESTOCK WORKFORCE CAPACITY`

### B — Cow scaling funziona ma revenue bassa
`REWORK LIVESTOCK ECONOMICS`

### C — Crop mix resta low-value
`PROCEED CROP PORTFOLIO OPTIMIZATION`

### D — Revenue cresce forte ma <28k
`PROCEED CAPACITY OPTIMIZATION`

### E — >28k
`E12 LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION`

---

## 35. Conclusioni vietate

Non concludere:

- che Cow #1 sia sufficiente;
- che il 2×2 possa restare sottoutilizzato;
- che 4 tile/worker vada aumentato durante X1.6;
- che serva acquistare più land prima di saturare economicamente il core.

---

## 36. Provenance

Run ID:

```text
E12-X1.6-*
```

Mantenere:

- source hash;
- config hash;
- seed;
- opponent;
- SHA-256 100%.

---

## 37. Submission

Non sostituire X1.7 nella submission finché X1.6 non supera il benchmark canonico in modo credibile.

---

## 38. Output richiesto

Restituisci:

### A. Livestock action-cost audit
### B. Crop economics table
### C. Functional workforce architecture
### D. Cow scaling gate
### E. Tests
### F. A0
### G. A1
### H. Canonical Stage B
### I. Workforce specialization analysis
### J. Livestock core utilization
### K. Economic comparison vs X1.5/X1.7
### L. Recommendation

Una sola:

- `REWORK LIVESTOCK WORKFORCE CAPACITY`
- `REWORK LIVESTOCK ECONOMICS`
- `PROCEED E12-X1.7 CROP PORTFOLIO OPTIMIZATION`
- `PROCEED E12-X1.7 CAPACITY OPTIMIZATION`
- `E12 LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION`

---

## Approval

Questo prompt autorizza:

1. audit;
2. BUILD X1.6;
3. test;
4. A0;
5. A1;
6. Stage B dopo doppio PASS.

Non richiedere approvazioni intermedie.

---

## Principio guida

> **Il 2×2 più prezioso della farm è riservato al livestock: deve essere progressivamente monetizzato. I worker devono specializzarsi per funzione, e la capacità crop resta conservativamente fissata a 4 tile per crop worker finché la farm ibrida non dimostra di poter superare il benchmark dei 28k.**
