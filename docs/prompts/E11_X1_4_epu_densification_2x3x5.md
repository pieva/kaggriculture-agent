# E11-X1.4 — FAST BUILD + VERIFY
## EPU Densification Before Replication — 2×3×5 vs B3 3×3×3

## Mandato operativo

Procedere immediatamente con una seconda ipotesi locale da confrontare questa sera con:

> **E11-X1.3-B3 — Fixed 3×3 3×EPU**

Obiettivo della sessione:

> avere entro stasera **due ipotesi machine-verified** da confrontare e scegliere quale utilizzare per il run notturno.

Le due architetture sono:

### Hypothesis A — B3
```text
3 EPU × 9 tiles
= 27 productive target tiles
```

### Hypothesis B — X1.4
```text
2 EPU × 15 tiles
= 30 productive target tiles
```

X1.4 deve verificare se:

> **densificare EPU1 ed EPU2 a 3×5 prima di attivare EPU3 produce più valore, migliore locality e migliore uso della workforce rispetto alla replica immediata di una terza EPU.**

---

# 1. Naming

Usare:

> **E11-X1.4 — EPU Densification Before Replication**

Short label:

> **2×3×5 Densification**

---

# 2. Ipotesi

Formalizzare:

> **H11-X1.4:** due EPU compatte da 15 tile possono superare tre EPU da 9 tile perché raggiungono una massa produttiva leggermente superiore (30 vs 27 tile) con meno unità indipendenti, minore startup overhead e potenzialmente minore workforce/movement overhead.

La sequenza da testare è:

```text
EPU1 3×3
   ↓
EPU1 densifies to 3×5
   ↓
realized productive surplus
   ↓
single BUY_LAND
   ↓
EPU2 3×3
   ↓
EPU2 densifies to 3×5
   ↓
30 active productive tiles
```

EPU3:

> **DISABLED / DELAYED in X1.4**

Non eliminarne il codice generale; semplicemente non attivarla in questo treatment.

---

# 3. Fixed geometry — NO SEARCH

NON eseguire nessuna ricerca geometrica.

Usare ESATTAMENTE:

## EPU1 3×5

```python
EPU1 = [
    (0,0), (0,1), (0,2), (0,3), (0,4),
    (1,0), (1,1), (1,2), (1,3), (1,4),
    (2,0), (2,1), (2,2), (2,3), (2,4),
]
```

## EPU2 3×5

```python
EPU2 = [
    (3,0), (3,1), (3,2), (3,3), (3,4),
    (4,0), (4,1), (4,2), (4,3), (4,4),
    (5,0), (5,1), (5,2), (5,3), (5,4),
]
```

Totale:

> **30 unique target tiles**

Verificare solamente:
- zero overlap;
- legal ownership sequence;
- 1 land purchase sufficiente;
- nessun secondo land necessario.

---

# 4. Preserve E06 startup

EPU1 NON deve partire immediatamente come 15-tile workload se questo altera il positive-control E06.

Startup:

> **EPU1 starts as the same 3×3 / 9-tile E06-equivalent core used in X1.3-A/B3.**

Initial EPU1 core:

```python
[
    (0,0), (0,1), (0,2),
    (1,0), (1,1), (1,2),
    (2,0), (2,1), (2,2),
]
```

Solo dopo che il core è operativo:

> densificare EPU1 verso `y=3..4`.

---

# 5. EPU1 densification trigger

NON usare un giorno hard-coded.

Densificare EPU1 9 → 15 quando:

- initial 9-tile core is operational;
- working capital is sufficient;
- additional six tiles can be started without starving existing production;
- workload can be served by available/daily hired workforce.

Derivare runtime:

```text
startup_cost_EPU1_extension =
actual seeds required for 6 additional tiles
+ incremental daily hire cost if required
```

---

# 6. Realized revenue gate for land

Come B3 corretto:

> **NO Day-0 BUY_LAND**

Il land purchase richiede:

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
+ operating_reserve(EPU1 expanded)
```

EPU3 non è inclusa perché X1.4 la ritarda.

Nessun magic threshold.

---

# 7. Land purchase purpose

Il primo BUY_LAND deve abilitare:

> **EPU2 3×5**

Non comprare terreno per future EPU non ancora attivate.

Registrare:
- land purchase day;
- step;
- cash pre/post;
- runtime required_cash;
- realized revenue at purchase.

---

# 8. EPU2 activation

Dopo il land purchase:

1. attivare il core 3×3 di EPU2;
2. densificare rapidamente a 3×5 quando working capital/workforce lo consentono.

Non richiedere un altro land purchase.

---

# 9. EPU3 deliberately delayed

Per X1.4:

```text
EPU3 activation = OFF
```

La domanda è precisamente:

> **30 tiles in 2 dense EPUs vs 27 tiles in 3 replicated EPUs**

Non contaminare il confronto attivando EPU3 successivamente nello stesso run.

---

# 10. Productive mechanism invariants

Mantenere invariati rispetto a E06/B3:

- WATER > HARVEST > PLANT;
- dynamic ROI/day crop selection;
- on-demand seed buying;
- immediate relevant market liquidation;
- realized-revenue tracking;
- daily Hands;
- corrected Multi-HIRE;
- no livestock.

Non introdurre crop tuning.

---

# 11. Workforce hypothesis

Workforce deve essere workload-driven.

Non assumere che 2 EPU richiedano necessariamente meno worker.

Misurare:

```text
workers/day
peak workforce
active_tiles/worker
productive_actions/worker
hire_cost/day
```

Confrontare direttamente con B3.

---

# 12. Locality hypothesis

Il vantaggio teorico di X1.4 è:

> meno unità indipendenti e cluster densificati.

Misurare:

- MOVE actions;
- MOVE/productive action;
- productive actions/worker;
- startup moves;
- local moves if available.

Non richiedere uguaglianza perfetta col vecchio EPU 3×3.

Il confronto primario è:

> **X1.4 vs B3**

---

# 13. Densification telemetry

Registrare:

```text
EPU1_core_activation_day
EPU1_15t_activation_day
EPU2_core_activation_day
EPU2_15t_activation_day
```

e:

```text
delta_EPU1_9_to_15
delta_land_to_EPU2_9
delta_EPU2_9_to_15
```

---

# 14. Time-to-mass metric

Aggiungere:

```text
day_15_active_tiles
day_18_active_tiles
day_27_active_tiles
day_30_active_tiles
```

e soprattutto:

```text
day_reaching_27_active_tiles
day_reaching_30_active_tiles
```

Confrontare con B3.

---

# 15. Economic comparison

Metriche principali:

```text
Mean Final Money
Median
Std Dev
Min
Max
```

e:

```text
daily revenue
cumulative realized revenue
cash trajectory
seed expenditure
hire expenditure
land expenditure
```

---

# 16. Unit economics

Calcolare:

```text
revenue_per_active_tile
revenue_per_worker
active_tiles_per_worker
MOVE_per_productive_action
```

Questo confronto è essenziale per capire se 2×15 è più efficiente di 3×9.

---

# 17. No additional geometry research

È vietato:
- cercare layout migliori;
- cambiare coordinate;
- provare 4×4;
- provare 5×3 alternative;
- ottimizzare bordi.

Usare il layout supervisore e misurarlo.

---

# 18. FAST verification protocol

Eseguire SOLO:

## Stage A0
1 episodio:
- seed 0;
- opponent pass.

Se crash / illegal / land pre-revenue / production collapse:
STOP.

Altrimenti:

## Stage B
5 episodi:
- stessi seed/protocollo usati da B3.

STOP dopo 5.

NON fare 10.
NON fare 30.

---

# 19. References — reuse only

NON rieseguire B3.

Usare il dataset verificato esistente.

B3 reference:

- Stage A0: **$30,234**
- Stage B Mean: **$26,445.60**
- Median: **$30,072**
- Peak active target: **27**
- Peak workforce: **4**
- BUY_LAND: **Day 13**
- EPU2/EPU3 activation: **Day 16** nello scenario seed0 verificato
- provenance: PASS

Usare anche come riferimento:

### X1.3-B
Mean:
**$28,727.40**

### X1.3-A
Mean:
**$26,888.40**

---

# 20. B3 vs X1.4 comparison matrix

Produrre:

| Metric | B3 — 3×9 | X1.4 — 2×15 |
|---|---:|---:|
| Target active tiles | 27 | 30 |
| Independent EPUs | 3 | 2 |
| Land purchases | 1 | target 1 |
| Land purchase day | 13 seed0 | |
| Time to ≥27 active | | |
| Time to 30 active | n/a | |
| Peak workforce | 4 | |
| Active tiles/worker | | |
| MOVE/productive | | |
| Mean Money | 26445.60 | |
| Median | 30072 | |
| Std | | |
| Min | 20014 | |
| Max | 31460 | |
| Revenue/tile | | |
| Revenue/worker | | |

---

# 21. Night-run decision gate

Lo scopo è scegliere la configurazione per il run notturno.

Classificare:

## X1.4 CLEAR WINNER

se:
- stable 30-tile activation;
- Mean > B3;
- no major lower-tail regression;
- locality/workforce metrics >= B3.

## B3 CLEAR WINNER

se:
- X1.4 Mean < B3;
- densification slower;
- 30 tiles not reached reliably;
- movement/workforce efficiency worse.

## MIXED

se:
- X1.4 Mean <= B3 ma median/min/trajectory migliore;
- oppure X1.4 più efficiente ma meno monetizzato entro Day 30.

In caso MIXED:

> raccomandare il candidato notturno in base al rischio/rendimento osservato, senza inventare nuovi treatment.

---

# 22. Important lower-tail analysis

B3 ha mostrato:

- Seed 300: ~$20k
- Seed 400: ~$20.4k

Quindi X1.4 deve essere valutata anche per:

> **stabilità / downside risk**

Non scegliere solo sulla media.

Confrontare:
- min;
- std;
- paired wins;
- seed-by-seed delta vs B3.

---

# 23. Paired comparison

Usare gli stessi 5 seed di B3.

Produrre:

| Seed | B3 | X1.4 | Delta |
|---:|---:|---:|---:|
| 0 | 30234 | | |
| 100 | 30072 | | |
| 200 | 31460 | | |
| 300 | 20014 | | |
| 400 | 20448 | | |

Calcolare:

```text
paired_wins
mean_paired_delta
median_paired_delta
```

---

# 24. Provenance

Creare run append-only:

```text
E11-X1.4-<timestamp>
```

con:
- config.json
- episodes.json
- summary.json
- config hash
- episodes hash
- verifier PASS

---

# 25. Tests

Aggiungere test minimi:

1. EPU1 3×3 startup preserved.
2. EPU1 expansion target exactly 3×5 / 15 unique tiles.
3. EPU2 target exactly 3×5 / 15 unique tiles.
4. EPU1/EPU2 no overlap.
5. 30 unique tiles total.
6. one land purchase sufficient.
7. EPU3 disabled.
8. no Day0 BUY_LAND.
9. realized-revenue land gate.
10. no magic land threshold.
11. E06 crop/Water/seed/market invariants.
12. provenance.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 26. Submission handling tonight

B3 standalone submission artifact è già verificato semanticamente ed è pronto.

Per X1.4:

se Stage B mostra `X1.4 CLEAR WINNER`:

> build anche X1.4 standalone artifact e verificarlo con un solo deterministic smoke.

Se B3 vince:

> non perdere tempo a creare artifact X1.4; usare B3 per il run notturno.

Se MIXED:

> preparare X1.4 artifact solo se serve per la scelta finale.

NON caricare automaticamente due submission contemporaneamente salvo richiesta esplicita del supervisore.

---

# 27. Documentation

Creare:

```text
docs/versions/E11_X1_4_epu_densification_before_replication.md
```

Aggiornare:
- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Aggiornare README solo con una riga/stato sintetico se X1.4 diventa trattamento corrente o candidato notturno.

---

# 28. Final recommendation

Il deliverable deve terminare con:

> **TONIGHT RECOMMENDATION: B3 / X1.4**

con motivazione quantitativa basata su:
- paired money;
- stability;
- active mass timing;
- workforce efficiency;
- movement;
- downside.

---

# 29. Git

Al termine:

```powershell
git status
git diff --stat
git diff --check
```

NON fare:
- tag;
- release;
- ulteriori treatment.

---

# Deliverable finale obbligatorio

Riportare:

1. X1.4 BUILD status
2. exact EPU1 3×5 coordinates
3. exact EPU2 3×5 coordinates
4. EPU3 disabled YES/NO
5. tests
6. A0 result
7. EPU1 9t activation
8. EPU1 15t activation
9. BUY_LAND day/step
10. runtime trigger
11. cash pre/post land
12. EPU2 9t activation
13. EPU2 15t activation
14. day reaching 27 active
15. day reaching 30 active
16. peak active tiles
17. peak workforce
18. active tiles/worker
19. MOVE/productive
20. Stage B Mean
21. Median
22. Std
23. Min/Max
24. paired seed table vs B3
25. paired wins
26. mean paired delta
27. cumulative revenue comparison
28. lower-tail comparison
29. B3 vs X1.4 matrix
30. provenance
31. config hash
32. episodes hash
33. X1.4 verdict
34. B3 verdict
35. TONIGHT RECOMMENDATION
36. candidate artifact built YES/NO
37. files changed
38. next action

---

# STOP RULE

Questa è l'ultima iterazione locale prima della decisione serale.

Flusso:

> **implement 2×3×5 → smoke → 5 episodes → compare with B3 → choose tonight run**

NON:
- ottimizzare X1.4 dopo il risultato;
- introdurre EPU3;
- provare altre geometrie;
- fare 10/30 episodi;
- sviluppare X1.5.

Dobbiamo arrivare alla decisione con due ipotesi pulite:

> **B3 = replicate first (3×9)**

vs

> **X1.4 = densify first (2×15)**.
