# E12-D2 — Weed Mechanics & Productive Surface Retention Audit

## Obiettivo

E12-X1.4 ha migliorato diversi aspetti operativi:

- movement ratio medio ridotto a circa `33.6%`;
- productive action ratio medio portato a circa `64.1%`;
- Cow #1 attiva e produttiva su tutti i seed;
- feed loop stabile;
- Q1 sbloccato con timing emergente intorno al Day 7.

Nonostante questo, il risultato economico è peggiorato:

- E12-X1.4 Mean Final Money: `$4,859.20`;
- E12-X1.3 Mean Final Money: `$7,015.40`;
- E11-X1.7 Mean Final Money: `$28,083.80`.

Inoltre, l'osservazione visuale dei replay mostra un problema molto evidente:

> **la superficie produttiva del nostro agente degrada nel tempo e viene progressivamente occupata/bloccata dalle erbacce.**

Il valore `Harvest Yield = 496.7%` NON può essere usato come proxy della salute complessiva della farm, perché colture multi-harvest possono generare più raccolti sulla stessa tile.

Il prossimo passo deve quindi essere un audit puramente diagnostico.

Nome:

**E12-D2 — Weed Mechanics & Productive Surface Retention Audit**

Durante D2:

- NON modificare la strategia;
- NON cambiare Q1/Q2 timing;
- NON cambiare Cow;
- NON cambiare crop mix;
- NON cambiare worker count;
- NON fare tuning.

Sono consentiti soltanto:

- ispezione motore;
- telemetry;
- script diagnostici;
- replay/trace analysis;
- report.

---

## 1. Domanda principale

Dobbiamo rispondere quantitativamente a:

> **Le erbacce stanno riducendo il working set produttivo della nostra farm più rapidamente di quanto i worker riescano a recuperarlo?**

E, se sì:

> **quanto action budget costa questa maintenance debt?**

---

## 2. Verifica meccanica delle WEEDS

Ispezionare direttamente il codice ufficiale dell'environment `kaggriculture.py`.

Documentare con precisione:

### Spawn
- quando può comparire una weed;
- probabilità/frequenza;
- su quali tile state può comparire;
- se può comparire su:
  - soil vuoto;
  - tile preparata;
  - tile coltivata;
  - tile appena raccolta;
  - tile inattiva;
- se la probabilità dipende da tempo, Quarter, crop, worker o altri fattori.

### Effetti
Verificare cosa provoca una weed:

- blocca `PLANT`?
- sostituisce una crop?
- impedisce `WATER`?
- impedisce `HARVEST`?
- azzera lo stato precedente della tile?
- richiede `DIG`, `CLEAR`, altra azione?

### Recovery cost
Ricostruire il ciclo esatto:

```text
WEED
  ->
[action]
  ->
SOIL/EMPTY
  ->
PLANT
  ->
WATER
  ->
HARVEST
```

Per il recupero completo di una tile infestata indicare:

- numero minimo di worker actions;
- movimento necessario;
- costi economici;
- seed da riacquistare;
- eventuale perdita della coltura precedente;
- tempo minimo prima che la tile torni a generare revenue.

---

## 3. Distinguere ownership, availability e working set

Definire tre concetti separati:

### OWNED LAND
Tile appartenente a Quarter acquistato.

### AVAILABLE TILE
Tile teoricamente utilizzabile dal planner.

### PRODUCTIVE WORKING SET
Tile che la strategia ha deciso di mantenere attivamente nel ciclo:

```text
prepare -> plant -> water -> harvest -> replant/maintain
```

Le weed fuori dal working set NON sono necessariamente un problema.

La metrica fondamentale è:

> **weed penetration inside the productive working set**

---

## 4. Working Set Membership

Per ogni tile definire se appartiene al working set corrente.

Una tile entra nel working set quando, ad esempio:

- viene assegnata alla crop engine;
- viene preparata/plantata con intenzione di mantenerla produttiva;
- appartiene al target geometry/ring corrente.

Una tile esce dal working set soltanto per decisione esplicita della strategia, NON semplicemente perché viene persa a weed/drought.

Questo permette di distinguere:

```text
planned contraction
```

da:

```text
productive surface loss
```

---

## 5. Nuovi KPI

### A. Sustained Productive Tiles

Definire:

```text
sustained_productive_tiles(day)
```

come il numero di tile appartenenti al working set che rimangono effettivamente nel ciclo produttivo senza essere perse per weed/drought/maintenance failure.

Calcolare almeno giornalmente.

### B. Productive Surface Retention

Definire:

```text
Productive Surface Retention =
sustained_productive_tiles
/
working_set_target_tiles
```

oppure una definizione equivalente più rigorosa, purché documentata.

### C. Weed Penetration

```text
Weed Penetration =
weed_tiles_inside_working_set
/
working_set_target_tiles
```

### D. Recovery Rate

```text
Weed Recovery Rate =
weed_tiles_recovered
/
weed_tiles_entered_working_set
```

### E. Mean Recovery Time

```text
Mean Weed Recovery Time =
mean(turn_recovered - turn_weed_detected)
```

---

## 6. Daily time series obbligatoria

Per ciascun seed D2 registrare Day 1–30 almeno:

- working_set_target_tiles;
- sustained_productive_tiles;
- active_crop_tiles;
- weed_tiles_inside_working_set;
- weed_tiles_outside_working_set;
- crop_tiles_lost_to_weeds;
- crop_tiles_lost_to_drought;
- weed_tiles_recovered;
- unrecovered_weed_tiles;
- mean weed recovery time;
- WATER backlog;
- HARVEST backlog;
- WEED/DIG backlog;
- worker count;
- movement ratio;
- productive action ratio;
- cash.

Obiettivo:

produrre una curva che renda visibile l'eventuale degradazione del working set.

---

## 7. Event telemetry per tile

Per ogni tile del working set, registrare quando possibile eventi:

```text
WORKING_SET_ENTER
WEED_APPEAR
WEED_CLEAR_START
WEED_CLEARED
REPLANTED
WATERED
HARVESTED
WORKING_SET_LOST
WORKING_SET_RECOVERED
```

Ogni evento deve includere:

- turn;
- day;
- coordinate;
- worker;
- crop precedente;
- crop successiva;
- cash se rilevante.

---

## 8. Weed-control action budget

Classificare separatamente:

- movement verso weed;
- weed clear/dig;
- replant post-weed;
- water post-recovery;
- harvest post-recovery.

Calcolare:

```text
weed_maintenance_actions
/
total_worker_actions
```

e:

```text
weed_recovery_actions
/
productive_actions
```

Vogliamo capire se le weed stanno creando un ciclo di manutenzione che assorbe progressivamente la capacità dei worker.

---

## 9. Maintenance Debt

Definire una metrica sintetica, per esempio:

```text
Maintenance Debt =
critical_water_backlog
+ critical_harvest_backlog
+ weed_tiles_inside_working_set
```

oppure una formulazione equivalente pesata.

Non introdurre pesi arbitrari senza motivazione.

L'obiettivo è capire se la farm entra in una spirale:

```text
backlog
 -> weed/drought loss
 -> recovery actions
 -> meno tempo per maintenance
 -> nuovo backlog
```

---

## 10. Confronto X1.4 vs X1.3 vs X1.7

Eseguire lo stesso audit, dove possibile, su:

- E12-X1.4;
- E12-X1.3;
- E11-X1.7.

Sugli stessi paired seed:

`0, 100, 200, 300, 400`

Confrontare almeno:

- sustained productive tiles;
- weed penetration;
- crop loss;
- recovery time;
- weed-control action ratio;
- movement ratio;
- final money.

Non modificare nessuna delle strategie durante l'audit.

---

## 11. Confronto visuale con replay competitor

Usare i replay già osservati soltanto come benchmark qualitativo.

Per i competitor distinguere:

- weed su land non utilizzato;
- weed dentro il nucleo produttivo;
- working set apparentemente mantenuto;
- aree volutamente non coltivate.

NON confrontare semplicemente:

```text
numero totale weed
```

Il confronto corretto è:

> **weed penetration nel nucleo/working set produttivo.**

---

## 12. Domande causali da risolvere

D2 deve rispondere almeno a:

1. Le weed possono distruggere o sostituire crop?
2. Quanto costa recuperare una tile infestata?
3. Quante tile del working set X1.4 vengono perse alle weed?
4. Quanto tempo rimangono indisponibili?
5. Quante azioni worker vengono spese per recuperarle?
6. Il backlog weed cresce nel tempo?
7. Il decadimento del working set precede il crollo economico?
8. X1.7 mantiene un working set più stabile?
9. La locality X1.4 riduce movement ma peggiora la capacità di weed control globale?
10. Esiste una soglia di working-set size oltre la quale la manutenzione collassa?

---

## 13. Working Set Capacity

Stimare empiricamente, per ogni worker count, quanti tile possono essere mantenuti stabilmente.

Definire una curva:

```text
workers -> sustained productive tiles
```

Non usare il numero massimo di tile mai piantate.

Usare il numero mantenuto in produzione per una finestra sufficientemente lunga.

Non inventare numeri; ricavarli dai trace.

---

## 14. Surface Churn

Aggiungere:

```text
Surface Churn =
tiles_entering_or_leaving_productive_state
/
working_set_size
```

Se X1.4 ha 24 tile target ma continuamente perde e ripristina tile, il churn sarà alto.

Questo è importante perché:

> un picco di 24 active tiles non equivale a 24 tile stabilmente produttive.

---

## 15. Crop Revenue per Sustained Tile

Calcolare:

```text
Crop Revenue per Sustained Tile =
cumulative_crop_revenue
/
mean_sustained_productive_tiles
```

Questo è più informativo di revenue per peak active tile.

---

## 16. Diagnosi attesa

Classificare il risultato in una delle seguenti categorie:

### A. WEED_MECHANICS_NOT_CAUSAL
Le weed sono principalmente su terreno non utilizzato.

### B. WEED_CONTROL_BACKLOG
Le weed penetrano nel working set e non vengono rimosse in tempo.

### C. WORKING_SET_OVERCOMMITMENT
La strategia assegna più tile di quante i worker possano mantenere.

### D. LOCALITY_SIDE_EFFECT
Il pinning locale impedisce di redistribuire worker dove le weed stanno crescendo.

### E. DROUGHT_PRIMARY_WEED_SECONDARY
La perdita primaria è ancora WATER/drought; le weed arrivano dopo.

### F. MULTI_MAINTENANCE_COLLAPSE
WATER + HARVEST + WEED competono per lo stesso action budget e producono una spirale di maintenance debt.

---

## 17. Nessun BUILD durante D2

D2 è diagnostico puro.

NON implementare:

- nuove priorità weed;
- nuovi worker;
- nuovi threshold;
- nuova expansion policy;
- nuovo crop mix.

Prima dobbiamo quantificare il fenomeno.

---

## 18. Output richiesto

Produrre:

### A. Engine Weed Mechanics
Tabella completa e verificata.

### B. Recovery Cost
Azioni/costi necessari per recuperare una tile.

### C. Working Set Definition
Definizione implementata per l'audit.

### D. Day 1–30 Time Series
Per X1.4 e, se disponibile, X1.3/X1.7.

### E. Weed Penetration Analysis
Dentro vs fuori working set.

### F. Sustained Productive Surface
Curva nel tempo.

### G. Maintenance Action Budget
Quota di azioni assorbita da weed/recovery.

### H. Working Set Capacity
Tile sostenibili per worker count.

### I. Root Cause Classification
Una o più categorie tra A–F.

### J. Recommendation for X1.5

La raccomandazione finale deve essere una sola:

- `X1.5 WORKING SET RETENTION`
- `X1.5 WEED PRIORITY CONTROL`
- `X1.5 WORKFORCE CAPACITY`
- `X1.5 LOCALITY REBALANCING`
- `X1.5 WATER/MAINTENANCE SCHEDULING`
- `X1.5 MULTI-MAINTENANCE RECOVERY`
- `WEEDS NOT PRIMARY — RETURN TO ECONOMIC DIAGNOSIS`

---

## 19. Decision rule

Non passare a X1.5 finché non possiamo rispondere chiaramente:

> **quante tile produttive stabili perdiamo alle weed, quanto ci costa recuperarle e se la dimensione del working set supera la capacità manutentiva dei worker.**

---

## Approval

Questo prompt autorizza:

- ispezione motore;
- telemetry;
- script diagnostici;
- esecuzione comparativa X1.4/X1.3/X1.7;
- report D2.

NON autorizza modifiche strategiche.

---

## Principio guida

> **Non misurare quante tile riusciamo ad attivare. Misurare quante tile riusciamo a mantenere produttive nel tempo senza perderle a weed, drought e maintenance debt.**
