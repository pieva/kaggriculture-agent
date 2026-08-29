# E11-X1.5 — FAST BUILD + VERIFY
## Centered 2×4×4 Productive Core

## Mandato

Procedere con una nuova variante locale da confrontare rapidamente con:

- **E11-X1.3-B3 — 3×3×3 / 27 tiles**
- **E11-X1.4 — 2×3×5 / 30 tiles**

La nuova ipotesi è:

> **massimizzare la densità produttiva attorno al centro/shed prima di creare ulteriori EPU periferiche.**

La nuova architettura deve usare:

> **2 EPU identiche da 4×4 = 32 productive target tiles**

entrambe attaccate al centro e adiacenti tra loro.

---

# 1. Naming

Usare:

> **E11-X1.5 — Centered 2×4×4 Productive Core**

Short label:

> **Centered 32t Core**

---

# 2. Ipotesi

Formalizzare:

> **H11-X1.5:** due EPU centrali e compatte da 16 tile ciascuna possono produrre più valore di 3×9 e 2×15 perché aumentano la massa produttiva totale riducendo contemporaneamente movement burden, numero di unità indipendenti e dispersione spaziale.

La sequenza da verificare è:

```text
EPU1 4×4 central core
        ↓
productive surplus
        ↓
single BUY_LAND
        ↓
EPU2 4×4 adjacent central core
        ↓
32 active productive tiles
```

Nessuna EPU3 in questo treatment.

---

# 3. Fixed Geometry — NO SEARCH

NON eseguire ricerche geometriche.

Usare ESATTAMENTE:

## EPU1 — 4×4

```python
EPU1 = [
    (1,1), (1,2), (1,3), (1,4),
    (2,1), (2,2), (2,3), (2,4),
    (3,1), (3,2), (3,3), (3,4),
    (4,1), (4,2), (4,3), (4,4),
]
```

## EPU2 — 4×4

```python
EPU2 = [
    (5,1), (5,2), (5,3), (5,4),
    (6,1), (6,2), (6,3), (6,4),
    (7,1), (7,2), (7,3), (7,4),
    (8,1), (8,2), (8,3), (8,4),
]
```

Totale:

> **32 unique target productive tiles**

---

# 4. Geometry invariants

Verificare soltanto:

```text
len(EPU1) == 16
len(EPU2) == 16
EPU1 ∩ EPU2 == ∅
total unique tiles == 32
```

e:

- un solo land purchase sufficiente;
- nessun secondo land necessario;
- entrambe le EPU vicine alla fascia centrale;
- nessuna tile periferica oltre il necessario.

---

# 5. Nessuna EPU3

Per X1.5:

```text
EPU3 = DISABLED
```

La domanda è:

> **quanto rende un core centrale da 32 tile prima di introdurre una terza unità?**

Non contaminare il test con ulteriore replication.

---

# 6. Startup policy

Non partire immediatamente con entrambe le EPU.

Sequenza:

1. avviare EPU1;
2. renderla produttiva;
3. generare realized revenue;
4. acquistare terreno quando economicamente sostenibile;
5. attivare EPU2;
6. portare entrambe le EPU a piena operatività.

---

# 7. EPU1 startup

EPU1 deve partire direttamente come **4×4 / 16 tile**, salvo che ciò provochi una regressione evidente del positive-control E06.

Se il codice richiede una fase di bootstrap più graduale, è ammesso:

```text
EPU1 3×3 core → 4×4 completion
```

ma il target deve essere rapidamente 16 tile.

Registrare:

```text
EPU1_core_activation_day
EPU1_16t_activation_day
```

---

# 8. Realized revenue gate

NO Day-0 BUY_LAND.

Il land purchase deve richiedere:

```text
cumulative_realized_revenue > 0
AND
cash >= required_cash
```

con:

```text
required_cash =
actual_land_cost
+ actual_startup_cost(EPU2)
+ operating_reserve(EPU1)
```

Nessun giorno hard-coded.

Nessun magic threshold.

---

# 9. Startup cost EPU2

Calcolare runtime usando:

- seed realmente mancanti;
- inventory disponibile;
- crop selected;
- seed price runtime;
- workforce/hire cost necessario;
- operating reserve.

Non assumere automaticamente `16 × seed_price`.

Usare costo effettivamente necessario.

---

# 10. EPU2 activation

Dopo BUY_LAND:

> attivare EPU2 il più rapidamente possibile.

Registrare:

```text
BUY_LAND_day
EPU2_activation_day
delta_land_to_EPU2
```

Target:

> minimo delta compatibile con working capital e workload.

---

# 11. Productive mechanism invariants

Mantenere invariati:

- WATER > HARVEST > PLANT;
- dynamic ROI/day crop selection;
- on-demand seed buying;
- immediate market liquidation;
- realized revenue tracking;
- daily Hands;
- corrected Multi-HIRE;
- no livestock.

X1.5 testa:

> **central geometry + density**

non crop tuning.

---

# 12. Workforce scaling

Workforce workload-driven.

Non imporre un numero fisso.

Misurare:

```text
workers/day
peak workforce
active_tiles/worker
productive_actions/worker
hire_cost/day
```

Confrontare:

- B3 peak = 4 workers
- X1.4 peak = 3 workers

---

# 13. Centrality metrics

Aggiungere metriche esplicite:

```text
avg_worker_target_distance
max_worker_target_distance
MOVE_actions
MOVE_per_productive_action
productive_actions_per_worker
```

La domanda centrale è:

> **stare vicino al centro riduce davvero il costo operativo abbastanza da aumentare la monetizzazione?**

---

# 14. Time-to-mass

Registrare:

```text
day_reaching_16_active
day_reaching_24_active
day_reaching_30_active
day_reaching_32_active
```

Confrontare con B3 e X1.4.

---

# 15. Utilization

Calcolare:

```text
active_tiles / owned_tiles
```

ai checkpoint:

- pre-land;
- EPU2 startup;
- peak.

---

# 16. FAST protocol

Eseguire SOLO:

## Stage A0
1 episodio:
- seed 0
- opponent pass

Se:
- crash;
- illegal action;
- Day0 land;
- capital starvation grave;
- EPU1 non operativa;

STOP.

Altrimenti:

## Stage B
5 episodi:
- stessi seed già usati per B3/X1.4:
  - 0
  - 100
  - 200
  - 300
  - 400

STOP dopo 5.

NON fare 10.
NON fare 30.

---

# 17. Reuse existing references

NON rieseguire B3 o X1.4.

Usare:

## B3 — 3×9
- Mean: **$26,445.60**
- Median: **$30,072.00**
- Std: **$5,687.21**
- Min: **$20,014**
- Max: **$31,460**
- Peak active: **27**
- Peak workforce: **4**

## X1.4 — 2×15
- Mean: **$27,209.20**
- Median: **$28,274.00**
- Std: **$2,604.28**
- Min: **$22,555**
- Max: **$28,508**
- Peak active: **30**
- Peak workforce: **3**

---

# 18. Paired seed comparison

Produrre:

| Seed | B3 | X1.4 | X1.5 | Best |
|---:|---:|---:|---:|---|
| 0 | 30234 | 22555 | | |
| 100 | 30072 | 28235 | | |
| 200 | 31460 | 28274 | | |
| 300 | 20014 | 28474 | | |
| 400 | 20448 | 28508 | | |

Calcolare:

```text
paired_wins_vs_B3
paired_wins_vs_X1.4
mean_delta_vs_B3
mean_delta_vs_X1.4
```

---

# 19. Statistical comparison

Riportare:

```text
Mean
Median
Std Dev
Min
Max
```

per X1.5.

---

# 20. Lower-tail comparison

Prestare particolare attenzione a:

> **seed 300 e 400**

perché hanno mostrato il punto debole di B3.

Verificare se il layout centrale mantiene la stabilità di X1.4.

---

# 21. Operational comparison matrix

Produrre:

| Metric | B3 3×9 | X1.4 2×15 | X1.5 2×16 |
|---|---:|---:|---:|
| Target tiles | 27 | 30 | 32 |
| EPUs | 3 | 2 | 2 |
| Land buys | 1 | 1 | 1 |
| Peak workforce | 4 | 3 | |
| Active/worker | | | |
| MOVE/productive | | | |
| Mean Money | 26445.60 | 27209.20 | |
| Std | 5687.21 | 2604.28 | |
| Min | 20014 | 22555 | |
| Max | 31460 | 28508 | |

---

# 22. Decision logic

Classificare:

## X1.5 CLEAR WINNER
se:
- Mean > both B3 and X1.4;
- no severe downside;
- 32 tiles reached reliably;
- movement/workforce metrics competitive.

## X1.5 PROMISING
se:
- Mean comparable;
- better operational efficiency;
- lower variance;
- stronger scaling trajectory.

## X1.5 NOT BETTER
se:
- Mean materially lower;
- 32 tiles delayed/unreliable;
- movement/workforce worse.

---

# 23. Night-run decision

Concludere con:

> **TONIGHT RECOMMENDATION: B3 / X1.4 / X1.5**

La scelta deve considerare:

1. Mean Final Money
2. lower-tail
3. stability
4. peak/ceiling
5. active mass timing
6. workforce efficiency
7. movement burden

Non scegliere solo sulla base di paired-win count.

---

# 24. Provenance

Creare:

```text
results/e11/E11-X1.5-<timestamp>/
```

con:

- config.json
- episodes.json
- summary.json
- SHA-256
- provenance verifier PASS

---

# 25. Tests

Aggiungere test minimi:

1. EPU1 = exact 4×4.
2. EPU2 = exact 4×4.
3. no overlap.
4. 32 unique target tiles.
5. one land purchase sufficient.
6. EPU3 disabled.
7. no Day0 BUY_LAND.
8. realized-revenue gate.
9. dynamic startup EPU2 cost.
10. no magic threshold.
11. E06 productive mechanism unchanged.
12. provenance.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 26. Submission handling

Non costruire automaticamente tre artifact.

Dopo Stage B:

### Se X1.5 è winner
- build X1.5;
- deterministic source-vs-bundle smoke;
- proporre X1.5 per run notturno.

### Se X1.4 resta migliore
- usare X1.4.

### Se B3 resta migliore
- usare B3 già verificata.

NON eseguire ulteriori treatment.

---

# 27. Documentation

Creare:

```text
docs/versions/E11_X1_5_centered_2x4x4_productive_core.md
```

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

README:
- aggiornamento sintetico solo se X1.5 diventa candidato corrente.

---

# 28. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

NON:
- tag;
- release;
- ulteriori esperimenti.

---

# Deliverable finale obbligatorio

Riportare:

1. X1.5 BUILD status
2. exact EPU1 coordinates
3. exact EPU2 coordinates
4. EPU3 disabled YES/NO
5. tests
6. A0 final money
7. EPU1 16t activation day
8. BUY_LAND day/step
9. runtime required_cash
10. cash pre/post land
11. EPU2 activation day
12. day reaching 24 active
13. day reaching 30 active
14. day reaching 32 active
15. peak active tiles
16. peak workforce
17. active tiles/worker
18. avg worker-target distance
19. MOVE/productive action
20. productive actions/worker
21. Stage B Mean
22. Median
23. Std
24. Min/Max
25. paired seed table
26. wins vs B3
27. wins vs X1.4
28. mean delta vs B3
29. mean delta vs X1.4
30. lower-tail comparison
31. B3 vs X1.4 vs X1.5 matrix
32. provenance verdict
33. config hash
34. episodes hash
35. X1.5 verdict
36. TONIGHT RECOMMENDATION
37. candidate artifact built YES/NO
38. files changed
39. next action

---

# STOP RULE

Questa è una verifica rapida.

Flusso:

> **fixed 2×4×4 → smoke → 5 episodes → compare → choose**

NON:
- cambiare geometria;
- fare crop tuning;
- attivare EPU3;
- fare 10/30 episodi;
- creare X1.6.

L'obiettivo è verificare una sola ipotesi:

> **centralità + densificazione 32t**
vs
> **replication 27t**
vs
> **densification 30t**.
