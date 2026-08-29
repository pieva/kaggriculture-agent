# E11-X1.3-B2R — RESTART PROMPT
## Post-Surplus 3× EPU Scaling with Bounded Geometry Search

Riprendiamo E11-X1.3-B2R dopo la chiusura forzata della precedente sessione Antigravity.

La precedente ricerca `scratch/search_epu_trio_geometry.py` è stata interrotta manualmente dopo oltre 30 minuti. La causa probabile è una ricerca combinatoria esaustiva di tutte le coppie possibili di cluster da 9 tile.

**NON riprendere quella ricerca e NON tentare nuovamente un'ottimizzazione globale esaustiva.**

L'obiettivo non è dimostrare l'ottimo geometrico matematico. Serve trovare rapidamente una configurazione EPU2/EPU3:
- compatta;
- non sovrapposta;
- disponibile con un solo acquisto di terreno;
- operativamente equivalente alla EPU1;
- sufficientemente buona da sottoporre a verifica sperimentale.

---

# 1. Stato sperimentale da preservare

## Riferimenti verificati

### E11-X1.3-A — 1× EPU
- 9 tile;
- meccanismo E06 replicato;
- Mean Final Money: **$26,888.40**;
- positive control.

### E11-X1.3-B — 2× EPU
- 18 tile;
- un'espansione post-surplus;
- Mean Final Money: **$28,727.40**;
- attuale Kaggle candidate, ma submission in HOLD finché B2R non è verificata.

### Old E11-X1.3-B2
- 27 tile;
- BUY_LAND Day 0;
- layout EPU3 con travel burden eccessivo;
- Mean Final Money: **$9,808.40**.

Interpretazione ufficiale:

- capacità geometrica di 27 tile in 2 quadranti: **VALIDATED**;
- Day-0 land purchase: **FALSIFIED**;
- vecchio layout EPU3: **NOT ACCEPTABLE**;
- hypothesis "post-surplus single-land → EPU2 + EPU3": **NOT YET CORRECTLY TESTED**.

Non descrivere B2R come prosecuzione della policy Day-0.

---

# 2. Obiettivo B2R

Verificare la sequenza:

```text
EPU1 equivalente a E06
        ↓
genera working-capital surplus
        ↓
UN SOLO BUY_LAND
        ↓
EPU2 + EPU3 diventano geometricamente disponibili
        ↓
attivazione EPU2
        ↓
attivazione EPU3 immediata o quasi immediata
        ↓
27 productive tiles
```

La domanda sperimentale è:

> Possiamo ottenere 3× EPU con un solo acquisto post-surplus, mantenendo l'efficienza operativa locale della EPU originale?

---

# 3. Vincolo assoluto: NO BUY_LAND Day 0

`BUY_LAND` al Day 0 è vietato.

Non usare neppure Day 13, Day 14 o qualsiasi altro giorno hard-coded.

Il terreno deve essere acquistato:

> **al primo step in cui il requisito economico derivato è realmente soddisfatto.**

---

# 4. Trigger economico dinamico

NON hardcodare `$1,570`.

Calcolare runtime:

```text
required_cash =
    actual_land_cost
  + actual_startup_cost(EPU2)
  + protected_near_term_startup_cost(EPU3)
  + operating_reserve(EPU1)
```

Se EPU2 ed EPU3 possono essere avviate contestualmente:

```text
required_cash =
    actual_land_cost
  + actual_startup_cost(EPU2)
  + actual_startup_cost(EPU3)
  + operating_reserve(EPU1)
```

Gli startup cost devono derivare dalla reale policy E06 replicata:
- crop selezionato runtime;
- seed price runtime;
- quantità realmente necessaria;
- inventory disponibile;
- workforce necessaria.

Se il risultato concreto è `$1,570`, registrarlo come valore osservato, NON come magic threshold.

---

# 5. Correzione fondamentale della Spatial Equivalence

NON richiedere:

```text
avg_distance_from_shed(EPU2/EPU3) == avg_distance_from_shed(EPU1)
```

Le EPU successive sono necessariamente più lontane dal punto di spawn/shed.

La metrica fondamentale è:

> **LOCAL OPERATIONAL MOVEMENT BURDEN**

Dopo che il worker ha raggiunto la propria EPU, EPU2 ed EPU3 devono richiedere movimenti interni comparabili a EPU1.

Distinguere quindi:

## A. Startup / commute movement
Distanza iniziale:
```text
spawn/shed → assigned EPU
```

Può essere maggiore per EPU2/EPU3.

## B. Local productive movement
Movimento:
```text
tile → tile
```

durante WATER / HARVEST / PLANT.

Questo deve restare comparabile a EPU1.

---

# 6. Definizione operativa di EPU

Una EPU è:

> **9 compact productive tiles + E06 scheduling + local workforce + E06-like local movement efficiency**

NON è semplicemente un insieme di 9 tile.

---

# 7. EPU1 — positive-control geometry

Preservare esattamente la geometria verificata.

Farmer:

```text
(4,4), (4,3), (3,4), (3,3)
```

Hand 1:

```text
(4,2), (3,2), (2,4), (2,3), (2,2)
```

Totale: **9 tile**.

Non modificare EPU1 per rendere più semplice il fitting di EPU2/EPU3.

---

# 8. Nuova ricerca geometrica — BOUNDED ONLY

Creare un nuovo script, ad esempio:

```text
scratch/search_b2r_geometry_bounded.py
```

NON riutilizzare automaticamente la precedente ricerca esaustiva.

La ricerca deve essere:
- bounded;
- deterministic;
- time-limited;
- early-stopping.

---

# 9. HARD RUNTIME LIMIT

La ricerca geometrica deve avere:

> **hard runtime limit = 60 seconds**

Se entro 60 secondi non trova un layout che soddisfa tutti i criteri:

1. interrompere automaticamente;
2. NON continuare in background;
3. NON aumentare automaticamente il search space;
4. restituire i migliori **10 candidate pairs** trovati;
5. riportare le metriche;
6. fermarsi per supervisor review.

Non eseguire ricerche di durata indefinita.

---

# 10. Search-space restriction

Limitare la ricerca alle tile:
- disponibili con Q0 + il primo quadrante acquistato;
- ragionevolmente vicine alla frontiera EPU1 / nuovo terreno;
- compatibili con due cluster compatti da 9 tile.

NON enumerare tutte le combinazioni `C(n,9)`.

Usare:
- template translations;
- compact shapes;
- connected-cluster generation locale;
- bounded BFS/DFS;
- beam search;
- greedy/local search;

o equivalente.

Preferire una soluzione semplice e verificabile.

---

# 11. Candidate generation

Partire dalla forma EPU1 e generare prima:

1. translations;
2. reflections, se utili;
3. rotations, se semanticamente equivalenti;
4. piccole deformazioni locali solo se necessarie.

Solo successivamente considerare altri connected 9-tile clusters.

Questo evita di reinventare arbitrariamente la EPU.

---

# 12. EPU2/EPU3 constraints

Ogni candidate pair deve soddisfare:

```text
len(EPU2) == 9
len(EPU3) == 9
EPU1 ∩ EPU2 == ∅
EPU1 ∩ EPU3 == ∅
EPU2 ∩ EPU3 == ∅
```

Inoltre:

- entrambe disponibili dopo UN SOLO land purchase;
- cluster connessi;
- nessuna forma lunga/artificialmente dispersa;
- nessun secondo BUY_LAND necessario per EPU3.

---

# 13. Geometry scoring

Per ciascuna EPU calcolare almeno:

```text
startup_distance
avg_local_pairwise_distance
max_local_pairwise_distance
estimated_local_move_cost
compactness
```

Non usare la sola distanza dallo shed come score principale.

---

# 14. Primary ranking

Ordine di priorità:

1. **local movement equivalence**
2. compactness
3. EPU2/EPU3 disjointness
4. one-land feasibility
5. startup distance

Quindi una EPU più lontana dallo shed ma molto compatta è preferibile a una più vicina ma allungata.

---

# 15. Stage G — Geometry acceptance

Classificare ogni EPU:

## `SPATIALLY EQUIVALENT`
local movement burden nella stessa classe di EPU1.

## `ACCEPTABLE MINOR PENALTY`
leggera penalità locale, da verificare empiricamente.

## `NOT EPU-EQUIVALENT`
penalità strutturale significativa.

Solo le prime due possono passare allo smoke test.

`NOT EPU-EQUIVALENT` → STOP.

---

# 16. Non compensare geometria inefficiente con workforce

È vietato concludere:

> "EPU3 è più lontana, quindi aggiungiamo worker."

Prima deve essere corretta la geometria.

Workforce e geometry sono variabili distinte.

---

# 17. Worker locality

Ogni Hand deve avere una EPU/cluster assegnata.

Evitare cross-EPU servicing sistematico.

Misurare runtime:
- worker → first assigned tile;
- MOVE interni;
- productive actions.

---

# 18. Runtime spatial telemetry

Durante A0 e Stage B registrare PER EPU:

```text
startup_moves
local_moves
productive_actions
water_actions
harvest_actions
plant_actions
MOVE_per_productive_action
productive_actions_per_worker
```

Se non è possibile distinguere perfettamente startup/local move, implementare una classificazione documentata e riproducibile.

---

# 19. Runtime equivalence > theoretical equivalence

La geometria teorica è solo Gate G.

Il verdetto finale deve usare soprattutto:

```text
MOVE_per_productive_action
productive_actions_per_worker
```

EPU2/EPU3 vs EPU1.

---

# 20. EPU3 non deve essere artificialmente bloccata

Rimuovere qualsiasi gate legacy che imponga:

```text
EPU3 disabled
```

oppure:

```text
wait for another land purchase
```

EPU3 deve potersi attivare non appena:
- il terreno è già disponibile;
- startup capital disponibile;
- workforce disponibile;
- EPU1 reserve protetta.

---

# 21. Near-simultaneous activation target

Registrare:

```text
EPU2_activation_day
EPU3_activation_day
activation_delta
```

Classificazione:

```text
0–1 day = NEAR-SIMULTANEOUS
2–3 days = FAST FOLLOW
>3 days = DELAYED
```

Questa è diagnostica, non un trigger hard-coded.

---

# 22. One-land invariant

Prima dell'attivazione EPU3:

```text
land_purchase_count == 1
```

Se EPU3 richiede un secondo acquisto:

> **B2R architectural objective FAILED**

---

# 23. E06 invariants

Non modificare per B2R:
- WATER > HARVEST > PLANT;
- dynamic ROI/day crop selection;
- on-demand seed buying;
- immediate market liquidation;
- EPU1 geometry;
- EPU1 positive-control semantics.

B2R NON è crop tuning.

---

# 24. Stage execution protocol

Eseguire soltanto:

```text
Stage G → Stage A0 → Stage B
```

### Stage G
Geometry only.

### Stage A0
1 episode:
- seed 0;
- opponent pass.

### Stage B
5 paired episodes.

STOP dopo Stage B.

NON eseguire:
- 10 episode;
- 30 episode;
- Kaggle submission.

---

# 25. Stage G Stop Gate

Se nessun layout soddisfa il criterio entro 60 secondi:

STOP e mostra Top 10.

Non procedere automaticamente ad A0.

---

# 26. Stage A0 acceptance

Verificare:

1. no Day0 BUY_LAND;
2. EPU1 starts alone;
3. EPU1 productive behavior preserved;
4. BUY_LAND only after dynamic surplus trigger;
5. exactly one land purchase before EPU3;
6. EPU2 activates;
7. EPU3 activates;
8. 27-tile target reachable;
9. no major runtime spatial penalty;
10. no illegal actions;
11. provenance PASS.

Se uno dei punti strutturali 1, 4, 5, 6 o 7 fallisce:

STOP.

---

# 27. Stage B — 5 episodes only

Usare protocollo ridotto già adottato.

Non rieseguire benchmark completi delle versioni precedenti.

Riutilizzare artifact verificati per:

### X1.3-A
Mean Final Money:
**$26,888.40**

### X1.3-B
Mean Final Money:
**$28,727.40**

### Old B2
Mean Final Money:
**$9,808.40**

---

# 28. Stage B decision

## VALIDATED

se:
- one land purchase;
- EPU2/EPU3 majority activation;
- 27 active tiles achieved;
- no structural movement penalty;
- Mean B2R > Mean B;
- provenance PASS.

## PARTIAL

se architecture works ma economic gain è limitato.

## FAILED

se:
- working-capital starvation;
- EPU3 requires second land;
- EPU3 cannot activate;
- movement burden destroys productivity;
- Mean <= B without compensating architectural advantage.

---

# 29. Economic metrics

Calcolare:

```text
B2R_vs_A_delta
B2R_vs_B_delta
B2R_vs_A_ratio
3x_scaling_efficiency
```

e:

```text
land_amortization_gain =
(B2R - A) / (B - A)
```

Gestire esplicitamente il caso denominator vicino a zero.

---

# 30. Time-adjusted scaling

Registrare per EPU:

```text
activation_day
active_EPU_days
```

e, se misurabile:

```text
revenue_per_active_EPU_day
productive_actions_per_active_EPU_day
```

Non giudicare una EPU attivata tardi come se avesse avuto 30 giorni completi.

---

# 31. Productive density

Registrare:

```text
peak_active_tiles
mean_active_tiles
owned_tiles
active_tiles / owned_tiles
active_tiles / land_purchase_count
```

---

# 32. Geometry report

Prima di A0 mostrare:

| Metric | EPU1 | EPU2 | EPU3 |
|---|---:|---:|---:|
| Tiles | 9 | 9 | 9 |
| Startup distance | | | |
| Avg local distance | | | |
| Max local distance | | | |
| Compactness | | | |
| Estimated local move cost | | | |
| Classification | | | |

e coordinate complete.

---

# 33. Runtime movement report

Dopo Stage B:

| Metric | EPU1 | EPU2 | EPU3 |
|---|---:|---:|---:|
| Startup moves | | | |
| Local moves | | | |
| Productive actions | | | |
| MOVE/productive action | | | |
| Productive actions/worker | | | |

---

# 34. Tests

Aggiungere/aggiornare test per:

1. no Day0 BUY_LAND;
2. dynamic trigger;
3. no `$1570` magic threshold;
4. EPU1 unchanged;
5. 9 tiles EPU2;
6. 9 tiles EPU3;
7. no overlap;
8. one-land feasibility;
9. EPU3 enabled;
10. local worker assignment;
11. geometry search timeout;
12. geometry search boundedness;
13. deterministic geometry selection;
14. WATER-first unchanged;
15. crop ROI unchanged;
16. seed buying unchanged;
17. market liquidation unchanged;
18. provenance.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 35. Provenance

Continuare a usare artifact append-only sotto:

```text
results/e11/
```

Registrare:
- run ID;
- config snapshot;
- episodes;
- summary;
- config SHA-256;
- episodes SHA-256.

Non sovrascrivere dataset precedenti.

---

# 36. Documentation

Creare:

```text
docs/versions/E11_X1_3_B2R_post_surplus_spatially_equivalent_3x_epu.md
```

Aggiornare:
- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Il vecchio B2 deve restare nella storia come:

> **incorrect implementation of intended B2R hypothesis**

---

# 37. README

NON modificare il current Kaggle candidate prima del risultato Stage B.

X1.3-B resta candidate in HOLD.

Se B2R supera B ed è architetturalmente valido:
- aggiornare README;
- proporre B2R come nuova candidate.

Altrimenti:
- mantenere B.

---

# 38. Git

Al termine:

```powershell
git status
git diff --stat
git diff --check
```

NON eseguire:
- commit;
- tag;
- push;
- Kaggle upload.

---

# 39. Deliverable finale obbligatorio

Riportare almeno:

1. search runtime;
2. timeout respected YES/NO;
3. candidates evaluated;
4. selected EPU2 coordinates;
5. selected EPU3 coordinates;
6. overlap check;
7. one-land geometry check;
8. theoretical EPU1 local movement metrics;
9. theoretical EPU2 local movement metrics;
10. theoretical EPU3 local movement metrics;
11. Stage G verdict;
12. tests;
13. Stage A0 result;
14. Day0 BUY_LAND check;
15. actual BUY_LAND day/step;
16. actual dynamic trigger value at purchase;
17. cash before/after land;
18. EPU2 activation;
19. EPU3 activation;
20. activation delta;
21. land purchase count;
22. peak active tiles;
23. mean active tiles;
24. peak workforce;
25. runtime MOVE/productive EPU1;
26. runtime MOVE/productive EPU2;
27. runtime MOVE/productive EPU3;
28. productive actions/worker;
29. Stage B episode count;
30. Mean Final Money;
31. Median;
32. Std;
33. Min/Max;
34. A reference;
35. B reference;
36. Old B2 reference;
37. B2R vs B delta;
38. 3× scaling efficiency;
39. land amortization gain;
40. active EPU days;
41. working-capital trajectory;
42. provenance verdict;
43. config hash;
44. episodes hash;
45. architecture verdict;
46. economic verdict;
47. Kaggle candidate verdict;
48. files changed;
49. next recommended action.

---

# 40. STOP RULE

Non lanciare processi geometrici indefiniti o in background.

Se una ricerca geometrica supera **60 secondi**, deve terminare.

Se Stage G non trova una soluzione accettabile:

> STOP e chiedi supervisor review.

Se Stage A0 fallisce un invariant strutturale:

> STOP.

Se Stage B termina:

> STOP e presenta i risultati.

---

# Principio architetturale finale

Non stiamo cercando:

> **27 tile a qualsiasi costo**

Stiamo cercando:

> **3 repliche funzionali dell'E06 EPU che condividano efficientemente il terreno acquistato.**

L'espansione deve preservare contemporaneamente:

```text
productive mechanism
+ local spatial efficiency
+ working capital
+ land amortization
```

Il maggiore tragitto iniziale verso EPU2/EPU3 è accettabile.

Una maggiore inefficienza di movimento **dentro** EPU2/EPU3 non lo è.
