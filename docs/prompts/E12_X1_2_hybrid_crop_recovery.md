# E12-X1.2 — Hybrid Crop Recovery

## Obiettivo

E12-X1.1 ha chiuso con successo la pipeline livestock:

`WHEAT -> FEED -> MILK -> SELL`

Risultati verificati sui 5 paired seed:

- 3 unità MILK per seed;
- mean MILK revenue: `$782.60`;
- 2 cow attive;
- zero starvation;
- Mean Final Money E12-X1.1: `$6,005.40`;
- Mean Final Money E11-X1.7: `$28,083.80`.

La conclusione corretta NON è:

> "crop-first outperforms livestock"

e NON dobbiamo tornare a discutere se valga la pena iniziare con gli animali.

L'evidenza osservata nei top player mostra che il livestock fa parte dell'opening. Il problema sperimentale ora è un altro:

> **come mantenere l'opening livestock e far partire subito dopo una massa agricola centered comparabile a quella di E11?**

E12-X1.1 ha dimostrato che sappiamo far funzionare gli animali. Ha però sacrificato quasi completamente il motore crop.

Il prossimo esperimento è quindi:

**E12-X1.2 — Hybrid Crop Recovery**

---

## 1. Ipotesi X1.2

### H12-X1.2

È possibile combinare:

- opening livestock precoce;
- feed loop funzionante;
- 1–2 cow operative vicino all'origine;
- riattivazione immediata della crop engine;
- scaling centered compatto;
- diversificazione agricola;

senza lasciare che la gestione livestock monopolizzi capitale, tile e worker actions.

L'obiettivo di X1.2 NON è aumentare il numero di cow.

L'obiettivo è recuperare rapidamente la **massa agricola** dopo il bootstrap animale.

---

## 2. Architettura sperimentale

Usare come composizione concettuale:

```text
E12-X1.1 livestock opening
        +
E11-X1.7 crop engine
        =
E12-X1.2 hybrid strategy
```

Non reinventare la crop strategy se la logica E11-X1.7 può essere riutilizzata.

Il test deve essere il più isolato possibile:

- mantenere ciò che X1.1 ha già validato per Cow/Feed/Milk;
- ripristinare quanto più possibile la capacità produttiva crop di X1.7;
- introdurre soltanto il coordinamento necessario tra i due sottosistemi.

---

## 3. Sequenza strategica target

La sequenza NON deve essere:

```text
livestock opening
-> livestock scaling
-> altre cow
-> crop quando rimane tempo/capitale
```

Deve essere:

```text
livestock bootstrap
        |
        v
feed capability verified
        |
        v
Cow #1 productive
        |
        v
IMMEDIATE CROP RECOVERY
        |
        v
centered crop mass scaling
        |
        +---- livestock maintenance in parallel
        |
        v
Cow #2 only if sustainable
        |
        v
hybrid farm expansion
```

Dopo la prima cow produttiva, le crop diventano nuovamente una priorità primaria.

---

## 4. Cow cap temporaneo per X1.2

Per questo esperimento:

- Cow #1: obbligatoria nell'opening;
- Cow #2: consentita solo se non interrompe la crop recovery;
- Cow #3 e Cow #4: DISABILITATE in X1.2.

Questo NON significa che 3–4 cow siano strategicamente sbagliate.

È un vincolo sperimentale per isolare il problema corrente.

Prima dobbiamo dimostrare di poter costruire:

`livestock early + crop mass`

Poi una futura X1.3 potrà riaprire il livestock scaling.

---

## 5. Livestock core

Mantenere riservato il 2×2 centered già verificato:

`[(3,3), (3,4), (4,3), (4,4)]`

ma costruire soltanto le pasture necessarie alle cow effettivamente attive.

Quindi in X1.2:

- reserved livestock capacity: 4 tile;
- active pasture target iniziale: 1;
- eventuale seconda pasture: solo con Cow #2;
- nessuna pasture #3/#4.

Il resto della farm deve essere utilizzato aggressivamente dalle crop.

---

## 6. Crop Recovery Gate

Introdurre un evento/stato esplicito:

`CROP_RECOVERY_START`

che deve scattare immediatamente dopo che Cow #1 ha dimostrato il primo ciclo produttivo minimo necessario.

Non attendere:

- più cicli MILK;
- Cow #2;
- accumulo di grande cash reserve;
- Q2;
- completamento del 2×2 livestock.

Il gate deve essere il più precoce possibile compatibilmente con la pipeline verificata.

Una volta entrati in `CROP_RECOVERY`, il planner deve tornare a costruire rapidamente massa agricola.

---

## 7. Riutilizzo di E11-X1.7

Ispeziona la policy E11-X1.7 e identifica precisamente:

- tile ordering center-out;
- corner pruning;
- target productive tiles;
- crop selection;
- seed acquisition;
- plant/water/harvest priority;
- eventuali threshold economici;
- movement policy;
- Q1/Q2 handling.

Riusa direttamente queste componenti quando compatibili.

Non duplicare codice se è possibile parametrizzare o richiamare la logica esistente.

Documenta quali parti di X1.7 vengono:

- riutilizzate senza modifiche;
- adattate;
- disabilitate;
- sostituite per incompatibilità con livestock.

---

## 8. Geometria ibrida

Il livestock core deve essere integrato nel center-out planner.

La crop engine deve trattare i tile livestock attivi/riservati come esclusioni, ma continuare a saturare lo spazio immediatamente circostante.

Obiettivo geometrico:

```text
          crop crop crop
       crop crop crop crop
     crop [ livestock ] crop
     crop [   core    ] crop
       crop crop crop crop
          crop crop
```

Non creare un secondo centro produttivo distante.

Non compensare i 2×2 riservati espandendosi prematuramente molto più lontano.

Prima saturare la corona centered utile.

---

## 9. Crop diversification

I replay mostrano che i top player non sembrano utilizzare una sola coltura.

X1.2 deve quindi consentire diversificazione, ma NON fare un nuovo tuning globale basato sui 5 benchmark seed.

Separare almeno:

### Feed crop
WHEAT necessario al livestock.

### Cash/ROI crops
Riutilizzare la logica E11/X1.7 dove possibile e verificare quali colture sono economicamente disponibili nelle varie fasi.

La scelta deve tenere conto di:

- seed cost;
- revenue;
- cycle time;
- worker actions;
- distance;
- Quarter availability;
- feed requirement.

Non trasformare però X1.2 in un esperimento di crop-mix optimization: il focus è recuperare **massa produttiva agricola**.

---

## 10. Worker action budget

Questo è un punto centrale di X1.2.

E12-X1.1 suggerisce che il worker può essere assorbito dalla pipeline livestock.

Aggiungere telemetria per classificare ogni farmer action almeno come:

- `MOVEMENT`
- `LIVESTOCK_SETUP`
- `LIVESTOCK_MAINTENANCE`
- `FEED_PRODUCTION`
- `CROP_SETUP`
- `CROP_MAINTENANCE`
- `CROP_HARVEST`
- `MARKET/SHED`
- `PASS/OTHER`

Calcolare per finestre:

- turn 1–24;
- 25–48;
- 49–72;
- 73–120;
- 121–240;
- 241–480;
- 481–720.

Obiettivo diagnostico:

> capire se, dopo il livestock bootstrap, il farmer torna effettivamente a dedicare la maggioranza delle azioni produttive alla costruzione e gestione della crop mass.

---

## 11. Crop mass telemetry

Registrare almeno ai turn:

`12, 24, 48, 72, 120, 240, 480, 720`

per E12-X1.2:

- active crop tiles;
- crop tiles per tipo;
- WHEAT tiles;
- harvested crop count;
- cumulative crop revenue;
- livestock tiles;
- active cow count;
- MILK revenue;
- total productive tiles;
- max productive Manhattan radius;
- cash;
- Q1/Q2 state.

Se possibile, produrre le stesse metriche per E11-X1.7 sugli stessi seed.

---

## 12. Nuova metrica: Crop Recovery Ratio

Per ogni milestone calcolare:

```text
Crop Recovery Ratio =
E12-X1.2 active crop tiles
/
E11-X1.7 active crop tiles
```

e, se disponibile:

```text
Crop Revenue Recovery Ratio =
E12-X1.2 cumulative crop revenue
/
E11-X1.7 cumulative crop revenue
```

Obiettivo:

misurare direttamente quanto velocemente la strategia ibrida recupera la capacità agricola del champion.

Non usare soltanto Final Money.

---

## 13. Diagnosi preliminare prima del BUILD

Prima di implementare:

1. confronta il trace X1.1 con X1.7 nei primi 120 turn;
2. identifica il primo punto in cui il numero di crop tile diverge materialmente;
3. identifica quali azioni X1.1 sostituiscono le azioni crop di X1.7;
4. quantifica capitale speso in:
   - cow;
   - pasture;
   - WHEAT/feed;
   - crop seeds;
   - land/Quarter;
5. quantifica worker actions spese in livestock;
6. identifica tile inutilizzati nelle prime fasi;
7. verifica se il planner crop rimane bloccato da uno stato livestock anche quando non serve.

Restituisci questa diagnosi nel report finale, ma puoi procedere direttamente al BUILD dopo aver identificato il collo di bottiglia.

---

## 14. Implementazione

Modificare `productive_mass_roi.py` introducendo una variante/config esplicita X1.2, senza sovrascrivere la possibilità di riprodurre X1.0/X1.1.

La policy deve avere almeno le macro-fasi:

```text
HYBRID_BOOTSTRAP
FEED_READY
COW1_PRODUCTIVE
CROP_RECOVERY
HYBRID_STEADY_STATE
```

In `CROP_RECOVERY`:

- livestock maintenance rimane attiva;
- crop expansion/maintenance torna ad alta priorità;
- Cow #2 è subordinata alla crop recovery;
- Cow #3/#4 sono disabilitate.

---

## 15. Gate per Cow #2

Cow #2 NON deve essere sbloccata soltanto perché Cow #1 ha prodotto MILK.

Richiedere anche una condizione di crop recovery.

Ad esempio, derivare una condizione basata su:

- numero minimo di active crop tiles;
- feed buffer;
- capacità di finanziare seed/ciclo successivo;
- nessun backlog crop critico.

Non hardcodare una soglia arbitraria senza confrontarla con la dinamica X1.7.

Preferire una soglia relativa al target crop della fase.

---

## 16. Q1 e Q2

### Q1
Mantieni/riusa il comportamento che consente lo scaling centered.

Verifica che il livestock bootstrap non ritardi Q1 in modo distruttivo rispetto a X1.7.

Registra il delta:

`turn_Q1_X1.2 - turn_Q1_X1.7`

### Q2
Non ottimizzare Q2 in questa iterazione.

Se il recupero crop porta naturalmente a Q2, registralo.

Non sacrificare la crop recovery per anticiparlo.

---

## 17. Stage A0 — Functional Hybrid Smoke Test

Usare seed `0`.

A0 PASS solo se:

- Cow #1 viene attivata;
- FEED funziona;
- MILK viene prodotto/raccolto/venduto;
- la crop engine riparte;
- il numero di crop tile cresce materialmente dopo `CROP_RECOVERY_START`;
- almeno un crop non-WHEAT completa un ciclo produttivo;
- non vengono costruite pasture #3/#4;
- provenance valida.

Se MILK funziona ma le crop restano quasi ferme:

**A0 FAIL — non eseguire Stage B.**

---

## 18. Stage A1

Ripetere smoke test su seed `100`.

Stessi gate A0.

Stage B può partire soltanto se A0 e A1 mostrano contemporaneamente:

`livestock functional + crop recovery functional`.

---

## 19. Stage B

Paired seed:

`0, 100, 200, 300, 400`

con gli stessi opponent utilizzati finora.

Confronto principale:

**E12-X1.2 vs E11-X1.7**

Baseline:

- E11-X1.7 Mean Final Money: `$28,083.80`;
- Median: `$30,081.00`;
- Peak: `$33,371.00`.

Riportare:

### Financial
- Mean;
- Median;
- std `ddof=1`;
- min/max;
- delta vs X1.7;
- paired win rate.

### Livestock
- first cow turn;
- first feed;
- first milk;
- MILK revenue;
- active cow count.

### Crops
- crop tile milestones;
- crop mix;
- crop revenue;
- first non-WHEAT harvest;
- Crop Recovery Ratio;
- Crop Revenue Recovery Ratio.

### Operations
- action budget per categoria;
- movement burden;
- idle/pass actions;
- Q1/Q2 timing.

---

## 20. Criterio di successo X1.2

Il primo obiettivo NON è battere immediatamente X1.7.

La domanda è:

> **possiamo conservare il livestock opening e recuperare quasi tutta la macchina agricola di E11?**

Interpretazione:

### A — Crop Recovery < 50%
La policy livestock continua a bloccare la farm.

`REWORK HYBRID SCHEDULING`

### B — Crop Recovery 50–80%
La combinazione funziona ma il costo operativo è ancora eccessivo.

Analizzare action budget e timing.

### C — Crop Recovery > 80% ma final money ancora molto inferiore
La farm produce, ma livestock/feed/crop mix ha un costo economico da ottimizzare.

Questo è un candidato valido per X1.3.

### D — Crop Recovery > 80% e gap economico ridotto sostanzialmente
Evidenza forte che la strategia ibrida è sulla traiettoria corretta.

### E — X1.2 >= X1.7
Prima validazione economica forte della strategia hybrid.

---

## 21. Conclusioni vietate

Non concludere da X1.2 o dai risultati precedenti che:

- "gli animali non convengono";
- "crop-first è la strategia corretta";
- "le cow hanno ROI inferiore quindi vanno eliminate".

Queste conclusioni non rispondono all'ipotesi che stiamo testando.

L'evidenza dei top player costituisce il vincolo strategico di partenza:

**livestock early è parte della configurazione competitiva osservata.**

Il nostro problema ingegneristico è riprodurre una farm ibrida efficiente.

---

## 22. Provenance e disciplina sperimentale

Mantenere SHA-256 provenance al 100%.

Non modificare policy tra seed dello stesso benchmark.

Non effettuare tuning post-hoc sui cinque seed.

Non sostituire automaticamente X1.7 nella submission.

X1.7 rimane champion/control finché una variante E12 non dimostra un vantaggio locale credibile.

---

## 23. Output richiesto

Restituisci:

1. **Pre-build diagnosis X1.1 vs X1.7**
2. **Implementation changes**
3. **Tests**
4. **A0**
5. **A1**
6. **Stage B**, solo dopo doppio smoke PASS
7. **Crop Recovery analysis**
8. **Worker Action Budget analysis**
9. **Financial comparison**
10. **Recommended next step**

La raccomandazione finale deve essere una tra:

- `REWORK HYBRID SCHEDULING`
- `PROCEED E12-X1.3 LIVESTOCK SCALING`
- `PROCEED E12-X1.3 HYBRID OPTIMIZATION`
- `E12 LOCAL CHAMPION — PREPARE EXTERNAL VALIDATION`

---

## Approval

Questo prompt autorizza direttamente:

- diagnosi;
- BUILD X1.2;
- test;
- A0;
- A1;
- Stage B se entrambi gli smoke test passano.

Non richiedere ulteriori approvazioni intermedie.

---

## Principio guida

> **Gli animali non sono più la variabile da giustificare. La variabile da risolvere è quanto rapidamente, dopo l'opening livestock, riusciamo a ricostruire una farm agricola centered, densa e redditizia.**
