# E12-X1.3 — Hybrid Full Crop Scaling

## Obiettivo

E12-X1.2 ha risolto il problema principale di X1.1:

- livestock opening funzionante;
- feed loop funzionante;
- MILK prodotto e monetizzato;
- zero starvation;
- crop engine riattivata;
- Mean Final Money aumentato da `$6,005.40` a `$21,912.20`;
- mean MILK revenue: `$2,021.40`.

Il limite residuo è ora chiaramente strutturale:

- E12-X1.2 raggiunge tipicamente **15 active crop tiles**;
- E11-X1.7 raggiunge **26 active crop tiles**;
- Crop Recovery Ratio:
  - turn 24/48/72: `9/9 = 100%`;
  - turn 120+: `15/26 = 57.7%`.

Quindi NON dobbiamo più modificare o giustificare l'opening livestock.

Il prossimo esperimento deve isolare il plateau agricolo a 15 tile e rimuoverlo.

Nome esperimento:

**E12-X1.3 — Hybrid Full Crop Scaling**

---

## 1. Ipotesi X1.3

### H12-X1.3

Mantenendo invariato l'opening livestock validato di X1.2, è possibile far proseguire la crop engine centered oltre il plateau di 15 tile fino a una massa produttiva comparabile a E11-X1.7:

**target strutturale: almeno 24–26 active crop tiles.**

La domanda sperimentale è:

> **perché X1.2 recupera perfettamente la crop engine fino a 9–15 tile ma non continua lo scaling di X1.7 verso 24–26 tile?**

Non assumere in anticipo che la causa sia Q2.

Prima identificare esattamente il gate che blocca l'espansione.

---

## 2. Vincoli sperimentali

### Non modificare l'opening livestock

Preservare il comportamento X1.2 già validato:

- Cow #1 early;
- pasture centered;
- WHEAT/feed buffer;
- FEED;
- MILK;
- SELL;
- zero starvation;
- livestock core reserved.

Non fare tuning dell'opening per migliorare i cinque seed.

### Cow scaling congelato

Per X1.3:

- Cow #1: attiva e mantenuta;
- Cow #2: NON deve precedere il raggiungimento del target crop;
- Cow #3/#4: disabilitate.

Gate consigliato:

```text
allow Cow #2 only if active_crop_tiles >= 24
AND crop engine is not backlogged
AND feed capacity is sufficient
```

Se Cow #2 non viene mai acquistata durante X1.3, non è un fallimento.

Il focus è **full crop scaling**.

---

## 3. Pre-Build Diagnosis obbligatoria: perché 15?

Prima di modificare codice, confrontare X1.2 e X1.7 almeno tra turn 72 e 240.

Individuare esattamente quale condizione impedisce a X1.2 di passare:

`15 -> 18 -> 21 -> 24 -> 26 crop tiles`

Verificare separatamente i seguenti possibili colli di bottiglia.

### A. Q1 timing

Registrare per X1.2 e X1.7:

- turn acquisto Q1;
- cash immediatamente prima/dopo;
- active crop tiles al momento di Q1;
- tile che Q1 rende disponibili.

Calcolare:

`delta_Q1_turn = Q1_turn_X1.2 - Q1_turn_X1.7`

Se X1.2 ritarda Q1, identificare quale spesa/azione provoca il ritardo.

### B. Q2 timing

Verificare:

- se X1.7 necessita Q2 per arrivare a 26 tile;
- se X1.2 tenta Q2;
- se Q2 è bloccato da cash threshold, state machine o altra condizione;
- se Q2 è realmente necessario per superare 15 tile.

NON comprare Q2 automaticamente finché questo non è verificato.

### C. Planner visibility

Per ogni fase verificare quanti tile risultano:

- unlocked;
- eligible;
- reserved livestock;
- rejected by geometry;
- rejected by distance;
- rejected by crop planner;
- rejected by EPU/Quarter;
- rejected per insufficienza economica.

Aggiungere una diagnostica sintetica:

```text
candidate_tiles_total
eligible_crop_tiles
reserved_livestock_tiles
locked_tiles
geometry_rejected
economic_rejected
planner_rejected
```

### D. Target/cap implicito

Cercare configurazioni o condizioni che possano fermare E12 a 15:

- target tile count;
- farmer partition;
- EPU allocation;
- crop ring limit;
- radius;
- Quarter-specific cap;
- state-machine transition;
- hardcoded X1.2 threshold.

Verificare esplicitamente che non esista un cap involontario.

### E. Worker scheduling

Tra turn 72 e 240 confrontare action budget X1.2 vs X1.7.

Misurare almeno:

- MOVEMENT;
- LIVESTOCK_SETUP;
- LIVESTOCK_MAINTENANCE;
- FEED_PRODUCTION;
- CROP_SETUP;
- CROP_MAINTENANCE;
- CROP_HARVEST;
- MARKET_SHED;
- PASS_OTHER.

Individuare quante azioni che in X1.7 servono all'espansione crop vengono sostituite in X1.2 da livestock/feed.

### F. Capital competition

Tra turn 72 e 240 ricostruire cash flow per categorie:

- Cow;
- pasture;
- WHEAT/feed;
- crop seeds;
- Q1;
- Q2;
- altre spese.

Individuare se X1.2 dispone del capitale per espandere ma non lo fa, oppure se il capitale è realmente insufficiente.

---

## 4. Output della diagnosi

Prima del BUILD devi essere in grado di classificare il plateau a 15 tile principalmente come una o più di queste cause:

```text
LAND_UNLOCK_BOTTLENECK
PLANNER_CAP_BOTTLENECK
WORKER_ACTION_BOTTLENECK
CAPITAL_BOTTLENECK
LIVESTOCK_SCHEDULING_BOTTLENECK
GEOMETRY_BOTTLENECK
OTHER_VERIFIED_BOTTLENECK
```

Documenta le evidenze.

Puoi poi procedere direttamente al BUILD senza richiedere approvazione.

---

## 5. Strategia X1.3

La policy target è:

```text
HYBRID_BOOTSTRAP
    ->
COW1_PRODUCTIVE
    ->
CROP_RECOVERY
    ->
FULL_CROP_SCALING
    ->
HYBRID_FULL_SCALE
```

La nuova fase fondamentale è:

`FULL_CROP_SCALING`

In questa fase:

1. Cow #1 viene mantenuta;
2. feed minimo necessario viene mantenuto;
3. nessuna nuova pasture viene costruita;
4. nessuna nuova cow viene acquistata;
5. tutta la capacità produttiva residua viene indirizzata allo scaling crop;
6. la geometria resta centered;
7. vengono riutilizzate le regole E11-X1.7 compatibili;
8. Q1/Q2 vengono acquistati soltanto quando necessari allo scaling verificato.

---

## 6. Riutilizzo rigoroso di E11-X1.7

L'obiettivo non è inventare una nuova espansione.

Riutilizzare il più possibile la logica che ha già portato X1.7 a 26 tile.

Confrontare e allineare:

- EPU progression;
- center-out ordering;
- corner pruning;
- land acquisition;
- crop target;
- seed purchase;
- crop selection;
- plant/water/harvest priorities;
- movement policy.

Le differenze rispetto a X1.7 devono essere soltanto quelle inevitabili:

- livestock core reserved;
- Cow #1;
- feed production;
- livestock maintenance.

Ogni altra differenza deve essere giustificata.

---

## 7. Target geometrico

Non richiedere necessariamente gli stessi identici 26 tile di X1.7, perché il livestock core occupa parte della geometria centrale.

Target:

**24–26 active crop tiles + livestock core**

oppure una configurazione equivalente che mantenga la stessa massa produttiva complessiva senza espansione periferica inefficiente.

Priorità:

1. saturare tile centered disponibili;
2. utilizzare nuovi Quarter/EPU quando necessario;
3. evitare corner/peripheral tile a basso ROI/hour;
4. non compensare il livestock con espansione lontana indiscriminata.

---

## 8. Q1

Q1 deve essere trattato come parte della pipeline di scaling.

Se la diagnosi mostra che X1.2 lo acquista troppo tardi:

- ripristinare il timing di X1.7 quanto più possibile;
- preservare soltanto il capitale minimo necessario a mantenere Cow #1 produttiva.

Non mantenere cash reserve arbitraria.

Telemetria obbligatoria:

- Q1 turn;
- cash before/after;
- active crop tiles before/after;
- next expansion turn.

---

## 9. Q2

Q2 va introdotto SOLO se la diagnosi dimostra che è necessario per raggiungere 24–26 tile.

Se necessario, usare una condizione di sustainable reinvestment:

```text
cash >= Q2 cost
      + immediate feed requirement
      + immediate seed requirement
      + mandatory next-cycle costs
      + small justified margin
```

Non usare `$2,500` o altre soglie arbitrarie.

Registrare:

- Q2 turn;
- cash before/after;
- crop tile count before/after;
- tempo necessario affinché Q2 produca nuovi tile attivi.

---

## 10. Feed policy durante Full Crop Scaling

Cow #1 deve continuare a produrre.

Ma il feed subsystem deve essere minimale.

Mantenere:

- feed buffer sufficiente;
- WHEAT production sufficiente;
- zero starvation.

Evitare:

- sovrapproduzione WHEAT;
- buffer eccessivi;
- worker action inutili;
- vendita accidentale del feed buffer.

Registrare:

```text
wheat_buffer
wheat_consumed
wheat_excess_sold
feed_actions
milk_output
```

---

## 11. Crop policy

Non effettuare un esperimento separato di crop mix optimization.

Riutilizzare la crop policy X1.7 per i cash crops, salvo incompatibilità verificata.

WHEAT rimane una coltura funzionale al feed.

Il focus è:

**numero di tile produttivi + continuità operativa**, non ricerca del crop mix perfetto.

---

## 12. Milestone telemetry

Per ogni seed registrare ai turn:

`24, 48, 72, 96, 120, 144, 168, 192, 240, 360, 480, 720`

almeno:

- cash;
- Q1/Q2;
- active crop tiles;
- crop tiles per tipo;
- reserved livestock tiles;
- active pasture;
- active cow;
- WHEAT buffer;
- MILK revenue;
- crop revenue;
- total productive tiles;
- max Manhattan radius;
- current macro-phase;
- eligible crop candidate tiles;
- blocked candidate tiles per causa.

---

## 13. Crop Recovery / Scaling Ratios

Continuare a calcolare:

```text
Crop Recovery Ratio =
X1.3 active crop tiles /
X1.7 active crop tiles
```

Aggiungere:

```text
Crop Revenue Recovery Ratio =
X1.3 cumulative crop revenue /
X1.7 cumulative crop revenue
```

e:

```text
Productive Mass Ratio =
(X1.3 active crop tiles + active livestock tiles)
/
X1.7 active crop tiles
```

---

## 14. Structural Success Gate

Prima di considerare X1.3 economicamente riuscito, deve superare il gate:

```text
peak_active_crop_tiles >= 24
AND
Cow #1 productive
AND
MILK revenue > 0
AND
zero cow starvation
```

Target preferito:

`24–26 crop tiles`.

Se non raggiunge 24 tile, il problema di full scaling NON è risolto, indipendentemente dal Final Money.

---

## 15. Stage A0

Seed `0`.

A0 PASS soltanto se:

- livestock opening X1.2 rimane funzionante;
- Cow #1 produce MILK;
- crop engine supera chiaramente il plateau precedente;
- active crop tiles >= 24 oppure esiste evidenza inequivocabile che il target viene raggiunto nel normale orizzonte dell'episodio;
- nessuna Cow #2 prematura;
- provenance valida.

Se resta a 15 tile:

**A0 FAIL — NON eseguire Stage B.**

Tornare alla diagnosi del plateau.

---

## 16. Stage A1

Seed `100`.

Stessi gate.

Stage B solo dopo:

`A0 PASS + A1 PASS`.

---

## 17. Stage B

Paired seed:

`0, 100, 200, 300, 400`

stessi opponent delle iterazioni precedenti.

Confronto primario:

**E12-X1.3 vs E11-X1.7**

Baseline X1.7:

- Mean Final Money: `$28,083.80`;
- Median: `$30,081.00`;
- Peak: `$33,371.00`.

Confronto secondario:

**E12-X1.3 vs E12-X1.2**

X1.2:

- Mean: `$21,912.20`;
- Median: `$21,953.00`;
- mean MILK revenue: `$2,021.40`;
- peak active crop tiles tipico: `15`.

---

## 18. Metriche Stage B

### Financial
- Mean Final Money;
- Median;
- std `ddof=1`;
- min/max;
- delta assoluto e % vs X1.7;
- delta assoluto e % vs X1.2;
- paired win rate.

### Crop scaling
- peak active crop tiles;
- steady crop tiles;
- turn first 18 tiles;
- turn first 21 tiles;
- turn first 24 tiles;
- turn first 26 tiles;
- Crop Recovery Ratio;
- Crop Revenue Recovery Ratio.

### Livestock
- first cow;
- feed actions;
- milk units;
- MILK revenue;
- starvation;
- Cow #2 turn, se applicabile.

### Land
- Q1 turn;
- Q2 turn;
- land unlock cost;
- time from unlock to productive utilization.

### Operations
- action budget;
- movement burden;
- pass/idle;
- blocked expansion reasons.

---

## 19. Interpretazione

### A — <18 crop tiles
Full scaling ancora bloccato.

`REWORK FULL CROP SCALING`

### B — 18–23 crop tiles
Miglioramento, ma plateau non risolto.

Identificare il nuovo gate.

### C — >=24 crop tiles, final money < X1.2
Scaling ottenuto ma economicamente inefficiente.

Analizzare travel/action/capital cost.

### D — >=24 crop tiles, X1.3 > X1.2 ma < X1.7
Strategia ibrida strutturalmente valida.

Procedere a ottimizzazione economica.

### E — >=24 crop tiles e gap vs X1.7 molto ridotto
Forte conferma della traiettoria E12.

### F — X1.3 >= X1.7
E12 diventa candidato local champion e può passare a validazione esterna.

---

## 20. Conclusioni da NON anticipare

Non concludere che:

- livestock early sia sbagliato;
- Cow #1 debba essere rimossa;
- crop-first sia superiore;
- il gap residuo rappresenti il costo inevitabile degli animali.

Queste conclusioni saranno valutabili soltanto DOPO aver confrontato:

**X1.7 full crop mass**

contro

**E12 full crop mass + livestock**.

Finché E12 rimane a 15 crop tile, il confronto economico non è omogeneo.

---

## 21. Test

Aggiornare i test per verificare almeno:

1. Cow #1 invariata rispetto a X1.2;
2. Cow #2 bloccata prima di 24 crop tile;
3. pasture #2/#3/#4 non costruite prematuramente;
4. feed buffer preservato;
5. crop planner può superare 15 tile;
6. EPU/Quarter successivi diventano eleggibili;
7. nessun cap hardcoded a 15;
8. Q1/Q2 non rompono feed loop;
9. suite completa senza regressioni.

Eseguire:

`.venv\Scripts\pytest.exe tests/`

---

## 22. Provenance

Mantenere verifica SHA-256 al 100%.

Correggere anche la nomenclatura dei Run ID: i run X1.2/X1.3 NON devono continuare a essere etichettati `E12-X1.0-*`.

Ogni run deve identificare correttamente:

- experiment variant;
- timestamp;
- source hash;
- config hash;
- seed;
- opponent.

Questo è necessario per evitare ambiguità nella provenance futura.

---

## 23. Documentazione

Aggiornare soltanto dopo risultati verificati:

- `docs/versions/E12_X1_3_hybrid_full_crop_scaling.md`
- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`

Non sostituire E11-X1.7 in `submission/submission.py` finché X1.3 non dimostra un vantaggio locale credibile.

---

## 24. Output richiesto

Restituisci:

### A. Plateau diagnosis
Causa/e verificate del limite a 15 tile.

### B. X1.3 implementation
Modifiche effettuate e differenze rispetto a X1.2/X1.7.

### C. Tests
Esito completo.

### D. A0
Inclusa curva active crop tiles nel tempo.

### E. A1
Stessa diagnostica.

### F. Stage B
Solo se entrambi superano il structural gate.

### G. Full scaling analysis
Confronto milestone X1.3/X1.2/X1.7.

### H. Economic analysis
Final money, crop revenue, MILK revenue, land cost, action budget.

### I. Recommendation
Una sola:

- `REWORK FULL CROP SCALING`
- `PROCEED E12-X1.4 HYBRID ECONOMIC OPTIMIZATION`
- `PROCEED E12-X1.4 LIVESTOCK SCALING`
- `E12 LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION`

---

## Approval

Questo prompt autorizza:

1. diagnosi del plateau;
2. BUILD X1.3;
3. test;
4. A0;
5. A1;
6. Stage B soltanto dopo doppio structural PASS.

Non richiedere approvazioni intermedie.

Se A0 o A1 rimangono bloccati a 15 tile, fermati e correggi il full crop scaling prima di lanciare il benchmark completo.

---

## Principio guida

> **Non dobbiamo più dimostrare che gli animali funzionano. Dobbiamo dare alla farm ibrida la stessa massa agricola che ha reso competitivo E11-X1.7, senza sacrificare l'opening livestock.**
