# E11-X1.6 — FAST BUILD + VERIFY
## Progressive Center-Out 3×3 → 4×4 EPU Scaling

## 0. Mandato

Implementare e verificare **una sola nuova ipotesi**:

> partire da un core produttivo 3×3 composto dalle tile più vicine al centro/shed, densificarlo a 4×4 verso l'esterno, quindi replicare la stessa sequenza in modo speculare sul quadrante adiacente.

La progressione obbligatoria è:

```text
EPU1 3×3 (9t)
    ↓
EPU1 4×4 (16t)
    ↓
BUY_LAND
    ↓
EPU2 3×3 (25t cumulative)
    ↓
EPU2 4×4 (32t cumulative)
```

Nome esperimento:

> **E11-X1.6 — Progressive Center-Out 3×3 → 4×4 EPU Scaling**

Questo treatment deve combinare:

- bootstrap compatto 3×3 già supportato da E06/B3;
- densificazione progressiva supportata dalla stabilità di X1.4;
- centralità;
- protezione del working capital;
- un solo land purchase;
- nessuna EPU3.

NON cambiare contemporaneamente crop policy o altre componenti strategiche.

---

# 1. Principio architetturale fondamentale

Formalizzare nel codice e nella documentazione:

> **CENTER-OUT DENSIFICATION RULE:** ogni EPU nasce dalle tile disponibili più vicine al centro/shed e viene successivamente densificata verso l'esterno.

Non trattare il 3×3 come un sottoinsieme arbitrario del 4×4.

Le prime 9 tile devono essere il core più centrale.

Le successive 7 tile devono essere l'anello periferico necessario a completare il 4×4.

---

# 2. Coordinate — FIXED, NO GEOMETRY SEARCH

Assumere indicizzazione da 0 e mantenere `(4,4)` come riferimento centrale lato EPU1.

## EPU1 — core 3×3

Usare ESATTAMENTE:

```python
EPU1_3x3 = [
    (2,2), (2,3), (2,4),
    (3,2), (3,3), (3,4),
    (4,2), (4,3), (4,4),
]
```

Totale: **9 tile**.

---

# 3. EPU1 — densificazione 4×4

Usare ESATTAMENTE:

```python
EPU1_4x4 = [
    (1,1), (1,2), (1,3), (1,4),
    (2,1), (2,2), (2,3), (2,4),
    (3,1), (3,2), (3,3), (3,4),
    (4,1), (4,2), (4,3), (4,4),
]
```

Verificare:

```text
EPU1_3x3 ⊂ EPU1_4x4
```

Le sole nuove tile devono essere:

```python
EPU1_DENSIFICATION_RING = sorted(
    set(EPU1_4x4) - set(EPU1_3x3)
)
```

Numero atteso:

> **7 tile**

---

# 4. EPU2 — core 3×3 speculare

Dopo il land purchase, EPU2 deve nascere dal lato opposto del centro usando:

```python
EPU2_3x3 = [
    (5,2), (5,3), (5,4),
    (6,2), (6,3), (6,4),
    (7,2), (7,3), (7,4),
]
```

Totale: **9 tile**.

---

# 5. EPU2 — densificazione 4×4

Usare:

```python
EPU2_4x4 = [
    (5,1), (5,2), (5,3), (5,4),
    (6,1), (6,2), (6,3), (6,4),
    (7,1), (7,2), (7,3), (7,4),
    (8,1), (8,2), (8,3), (8,4),
]
```

Verificare:

```text
EPU2_3x3 ⊂ EPU2_4x4
```

e:

> **7 nuove tile di densificazione**

---

# 6. Simmetria

Verificare programmaticamente che EPU1 ed EPU2 abbiano:

- stessa dimensione 3×3;
- stessa dimensione 4×4;
- stesso numero di tile aggiunte 3×3 → 4×4;
- geometria locale equivalente;
- nessun overlap.

Non fare geometry optimization.

---

# 7. Target ladder

La state machine produttiva deve distinguere chiaramente:

```text
PHASE_1_EPU1_CORE
PHASE_2_EPU1_DENSIFY
PHASE_3_ACCUMULATE_FOR_LAND
PHASE_4_EPU2_CORE
PHASE_5_EPU2_DENSIFY
PHASE_6_STEADY_32T
```

Registrare il passaggio tra le fasi in telemetry.

---

# 8. Fase 1 — EPU1 3×3

All'avvio:

> lavorare SOLO sulle 9 tile di `EPU1_3x3`.

Preservare il productive mechanism E06/B3:

```text
WATER > HARVEST > PLANT
dynamic ROI/day crop selection
on-demand seed buying
immediate market liquidation
daily workforce hiring
```

Nessun land purchase.

Nessuna tile dell'anello 4×4 finché il core 3×3 non è realmente operativo.

---

# 9. Gate EPU1 3×3 → 4×4

NON usare un giorno hard-coded.

La densificazione deve iniziare quando il core ha dimostrato capacità produttiva.

Usare un gate derivato da runtime state.

Minimo obbligatorio:

```text
cumulative_realized_revenue > 0
```

e disponibilità di working capital sufficiente per:

```text
startup_cost(7 additional tiles)
+ operating_reserve(existing 9 tiles)
```

Calcolare startup cost con:

- inventory reale;
- seed mancanti;
- crop corrente;
- runtime seed price;
- eventuale hire cost.

NON hardcodare un valore monetario.

---

# 10. Fase 2 — EPU1 4×4

Una volta aperto il gate:

> aggiungere SOLO le 7 tile mancanti.

NON ripiantare/riprogettare il core 3×3.

L'obiettivo è passare:

```text
9 → 16 active productive tiles
```

con minimo disruption.

Registrare:

```text
EPU1_3x3_activation_day
EPU1_densification_start_day
EPU1_16t_activation_day
```

---

# 11. Gate EPU1 4×4 → BUY_LAND

Il land purchase NON deve dipendere da:

- Day 13;
- Day 14;
- `$1300`;
- `$1500`;
- `$1570`;
- altro magic threshold.

Condizione:

```text
EPU1 sufficiently operational
AND
cumulative_realized_revenue > 0
AND
cash >= required_cash
```

dove:

```text
required_cash =
actual_land_cost
+ actual_startup_cost(EPU2_3x3)
+ operating_reserve(EPU1_4x4)
```

`actual_startup_cost(EPU2_3x3)` deve usare inventory offset.

---

# 12. Working-capital protection

Questa è una correzione esplicita rispetto a X1.5.

X1.5 ha fallito nel raggiungere 32 tile perché:

> la costruzione diretta di EPU1 4×4 e la successiva inizializzazione di EPU2 hanno assorbito troppo capitale operativo.

X1.6 deve quindi verificare:

> **il bootstrap 3×3 genera il cashflow che finanzia la densificazione successiva.**

Registrare ad ogni transition gate:

```text
cash_before_transition
protected_startup_cost
operating_reserve
cash_after_transition
```

---

# 13. BUY_LAND

Deve esserci:

> **massimo 1 BUY_LAND**

e:

> **zero BUY_LAND Day 0**

Registrare:

```text
BUY_LAND_day
BUY_LAND_step
cash_before_BUY_LAND
cash_after_BUY_LAND
required_cash_at_BUY_LAND
```

---

# 14. Fase 4 — EPU2 3×3

Subito dopo l'acquisto del terreno, NON tentare direttamente 16 nuove tile.

Avviare prima:

> **EPU2_3x3 = 9 tile centrali speculari**

Quindi il target cumulativo diventa:

```text
16 + 9 = 25 productive tiles
```

Registrare:

```text
EPU2_core_start_day
day_reaching_25_active
```

---

# 15. Gate EPU2 3×3 → 4×4

Stesso principio di EPU1.

Non usare timing hard-coded.

Densificare EPU2 quando:

```text
EPU2 has productive activity
AND
working capital supports 7 additional tiles
AND
existing productive core is not starved
```

Calcolare runtime il costo effettivo delle 7 tile.

---

# 16. Fase 5 — EPU2 4×4

Aggiungere solo l'anello di 7 tile.

Target:

```text
25 → 32 active productive tiles
```

Registrare:

```text
EPU2_densification_start_day
day_reaching_30_active
day_reaching_32_active
```

---

# 17. Fase 6 — steady 32t

Una volta raggiunte 32 tile:

- NON espandere ulteriormente;
- NON comprare altro terreno;
- NON creare EPU3;
- NON introdurre livestock.

Usare il tempo restante per massimizzare il rendimento delle 32 tile.

---

# 18. Workforce — workload driven

NON fissare artificialmente:

```text
2 workers
3 workers
4 workers
```

La workforce deve essere derivata dal backlog produttivo.

Correggere/riutilizzare la logica Multi-HIRE già verificata.

Ricordare:

> i Hands sono giornalieri e vanno riassunti quando necessari.

Registrare per giorno:

```text
workers
HIRE_count
hire_cost
productive_backlog
active_tiles
```

---

# 19. Workforce telemetry

Misurare almeno:

```text
peak_workforce
mean_workforce
active_tiles_per_worker
productive_actions_per_worker
```

Confrontare con:

```text
B3 peak workforce = 4
X1.4 peak workforce = 3
```

---

# 20. Movement telemetry

Poiché l'ipotesi riguarda centralità + compattezza, registrare:

```text
MOVE_actions
productive_actions
MOVE_per_productive_action
avg_worker_target_distance
max_worker_target_distance
```

Se possibile separare:

```text
EPU1 movement
EPU2 movement
```

---

# 21. Transition economics

Per ciascun salto:

```text
9 → 16
16 → 25
25 → 32
```

registrare:

```text
transition_day
cash_before
cash_after
revenue_before
startup_cost
days_to_next_transition
```

Questa telemetry è obbligatoria.

Vogliamo sapere **dove il compounding accelera o si rompe**.

---

# 22. Historical references — NON RIESGUIRE

Usare i risultati già verificati.

## B3 — Kaggle current competitive reference

Local:

```text
Mean   = $26,445.60
Median = $30,072.00
Std    = $5,687.21
Min    = $20,014
Max    = $31,460
Peak active tiles = 27
Peak workforce = 4
```

External Kaggle:

> **Score = 541.3**

Questo è il benchmark competitivo corrente.

---

# 23. X1.4 reference

```text
Mean   = $27,209.20
Median = $28,274.00
Std    = $2,604.28
Min    = $22,555
Max    = $28,508
Peak active tiles = 30
Peak workforce = 3
```

Interpretazione:

> densificazione più stabile, ma ceiling inferiore a B3.

---

# 24. X1.5 reference

```text
Mean   = $25,029.00
Median = $24,154.00
Std    = $2,001.35
Min    = $24,070
Max    = $28,601
Peak active tiles = 26
Target tiles = 32
```

Interpretazione obbligatoria:

> X1.5 NON ha realmente verificato il rendimento di 32 tile centrali perché non è riuscito ad attivarle tutte.

Quindi NON classificare automaticamente la geometria 2×4×4 come falsificata.

La variabile corretta da testare ora è:

> **progressive activation order**.

---

# 25. FAST verification protocol

NON eseguire benchmark lunghi.

## Stage A0

1 episodio:

```text
seed = 0
opponent = pass
steps = 720
```

Controllare:

- no crash;
- no illegal action;
- EPU1 parte 3×3;
- EPU1 densifica a 4×4;
- no Day0 land;
- BUY_LAND solo dopo gate economico;
- EPU2 parte 3×3;
- EPU2 prova a densificare 4×4;
- telemetry completa.

Se structural failure:

> STOP.

Altrimenti Stage B.

---

# 26. Stage B

Eseguire SOLO 5 episodi sugli stessi seed già usati:

```text
0
100
200
300
400
```

Usare gli stessi opponent mapping del benchmark precedente.

STOP dopo 5.

NON fare:

- 10 episodi;
- 30 episodi;
- benchmark storico aggiuntivo.

---

# 27. Paired comparison

Produrre:

| Seed | B3 | X1.4 | X1.5 | X1.6 | Winner |
|---:|---:|---:|---:|---:|---|
| 0 | 30234 | 22555 | 24223 | | |
| 100 | 30072 | 28235 | 24154 | | |
| 200 | 31460 | 28274 | 24097 | | |
| 300 | 20014 | 28474 | 24070 | | |
| 400 | 20448 | 28508 | 28601 | | |

Calcolare:

```text
wins_vs_B3
wins_vs_X1.4
wins_vs_X1.5

mean_delta_vs_B3
mean_delta_vs_X1.4
mean_delta_vs_X1.5
```

---

# 28. Statistical metrics

Per X1.6:

```text
Mean
Median
Std Dev ddof=1
Min
Max
```

---

# 29. Primary success criteria

X1.6 è particolarmente interessante se:

1. raggiunge stabilmente **32 active tiles**;
2. supera X1.5 economicamente;
3. mantiene o migliora la stabilità di X1.4;
4. si avvicina/supera il ceiling locale B3;
5. movement burden resta basso;
6. workforce riesce realmente a servire il footprint.

---

# 30. Important diagnostic outcomes

Classificare separatamente:

## A. GEOMETRY SUCCESS
32 tile raggiunte e operative.

## B. CAPITAL SUCCESS
ogni transition è finanziata senza starvation.

## C. WORKFORCE SUCCESS
backlog gestibile e produttive throughput adeguato.

## D. ECONOMIC SUCCESS
Final Money migliora i reference.

Non comprimere tutto in un singolo verdict.

---

# 31. Decision rule

## X1.6 CLEAR WINNER

Se:

```text
Mean > X1.4
AND
32 tiles reliably reached
AND
no severe lower-tail regression
```

con preferenza ulteriore se:

```text
Median >= B3
```

---

## X1.6 STRUCTURALLY VALID / ECONOMICALLY PROMISING

Se:

- 32 tile raggiunte;
- working capital stabile;
- movement/workforce migliori;
- money non ancora superiore.

In questo caso NON falsificare l'architettura.

---

## X1.6 NOT VALIDATED

Se:

- non supera 26–30 active tiles;
- starvation ricompare;
- transition 9→16 o 16→25 peggiora il core;
- economics nettamente peggiori.

---

# 32. Night-run recommendation

Concludere obbligatoriamente con:

> **TONIGHT RECOMMENDATION: B3 / X1.4 / X1.6**

La scelta deve considerare:

1. Kaggle evidence B3 = **541.3**
2. Mean local
3. Median
4. lower-tail
5. peak ceiling
6. 32t achievement
7. transition timing
8. movement efficiency
9. workforce efficiency

Non scegliere soltanto sulla media locale.

---

# 33. Provenance

Creare:

```text
results/e11/E11-X1.6-<timestamp>/
```

con:

```text
config.json
episodes.json
summary.json
```

Calcolare:

```text
Config SHA-256
Episodes SHA-256
```

Eseguire provenance verifier.

---

# 34. Unit tests

Aggiungere test almeno per:

1. exact EPU1 3×3 coordinates;
2. exact EPU1 4×4 coordinates;
3. EPU1 subset invariant;
4. EPU1 ring = 7;
5. exact EPU2 3×3;
6. exact EPU2 4×4;
7. EPU2 subset invariant;
8. EPU2 ring = 7;
9. EPU1/EPU2 no overlap;
10. cumulative 9/16/25/32 targets;
11. no EPU3;
12. max one land purchase;
13. no Day0 land;
14. realized revenue gate;
15. dynamic transition costs;
16. inventory offset;
17. no hardcoded transition days;
18. productive mechanism invariants;
19. Multi-HIRE behavior;
20. provenance.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 35. Files

Creare:

```text
scripts/benchmark_e11_x1_6.py
docs/versions/E11_X1_6_progressive_center_out_epu_scaling.md
```

Modificare solo quanto necessario:

```text
src/agricola/strategy/productive_mass_roi.py
tests/test_e11_productive_mass.py
docs/PROJECT_STATE.md
docs/EXPERIMENT_LOG.md
docs/NEW_SESSION.md
```

README solo se X1.6 diventa nuovo candidate/reference.

---

# 36. Submission handling

NON sovrascrivere prematuramente il bundle B3 verificato.

Prima:

```text
BUILD
→ tests
→ A0
→ Stage B
→ comparison
```

Solo se X1.6 viene scelto come candidate:

1. build standalone submission;
2. deterministic semantic equivalence;
3. smoke seed 0;
4. dichiarare artifact ready.

Se X1.6 non vince:

> mantenere B3 come submission/reference verificata.

---

# 37. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

NON:

- tag;
- release;
- X1.7;
- benchmark aggiuntivi.

---

# 38. Deliverable finale obbligatorio

Riportare in ordine:

1. experiment status;
2. exact EPU1 3×3;
3. exact EPU1 4×4;
4. exact EPU2 3×3;
5. exact EPU2 4×4;
6. center-out invariant PASS/FAIL;
7. tests;
8. Stage A0 money;
9. EPU1 3×3 activation day;
10. EPU1 densification start;
11. day reaching 16 active;
12. BUY_LAND day/step;
13. required cash;
14. cash pre/post land;
15. EPU2 3×3 activation;
16. day reaching 25 active;
17. EPU2 densification start;
18. day reaching 30 active;
19. day reaching 32 active;
20. peak active tiles;
21. peak workforce;
22. mean workforce;
23. active tiles/worker;
24. productive actions/worker;
25. MOVE/productive action;
26. avg/max worker-target distance;
27. economics 9→16;
28. economics 16→25;
29. economics 25→32;
30. Stage B Mean;
31. Median;
32. Std;
33. Min/Max;
34. paired table B3/X1.4/X1.5/X1.6;
35. wins vs references;
36. mean deltas;
37. lower-tail comparison;
38. GEOMETRY verdict;
39. CAPITAL verdict;
40. WORKFORCE verdict;
41. ECONOMIC verdict;
42. provenance verdict;
43. config hash;
44. episodes hash;
45. X1.6 overall verdict;
46. TONIGHT RECOMMENDATION;
47. candidate artifact built YES/NO;
48. files changed;
49. next action.

---

# 39. STOP RULE

Questo è ancora un esperimento rapido.

Eseguire ESATTAMENTE:

> **3×3 center core → 4×4 densification → one land → mirrored 3×3 → mirrored 4×4 → 5 episodes → decision**

NON:

- geometry search;
- EPU3;
- livestock;
- crop-policy redesign;
- 10/30 episode benchmark;
- nuova variante;
- ottimizzazioni successive.

L'obiettivo è isolare una domanda:

> **il bootstrap 3×3 seguito da densificazione center-out consente di raggiungere e monetizzare realmente un core compatto da 32 tile senza il working-capital starvation osservato in X1.5?**
