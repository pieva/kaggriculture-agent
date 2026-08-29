# E11-X1.3-B2R — BUILD + VERIFY — Post-Surplus Cross-Boundary 3× EPU with Spatial Equivalence

## Contesto

La precedente implementazione **E11-X1.3-B2** NON ha testato correttamente l'ipotesi architetturale prevista.

Ha introdotto due deviazioni sostanziali:

1. `BUY_LAND` eseguito al **Day 0**, drenando working capital prima che EPU1 producesse surplus;
2. EPU2/EPU3 disposte con geometria operativa peggiore di EPU1, causando una **Labor Travel Penalty** non intrinseca al modello EPU.

Pertanto il precedente risultato:

> **$9,808.40 Mean Final Money**

NON falsifica la hypothesis:

> **single post-surplus land purchase → EPU2 + EPU3**

Falsifica soltanto:

> **Day-0 expansion + non-equivalent spatial layout**

---

# 1. Stato ufficiale del precedente B2

Registrare:

- **Geometry capacity (27 tiles in 2Q): VALIDATED**
- **Day-0 land purchase policy: FALSIFIED**
- **Previous EPU2/EPU3 spatial layout: NOT ACCEPTABLE**
- **Cross-boundary 3× EPU hypothesis: NOT YET CORRECTLY TESTED**

Non dichiarare:

> `Cross-Boundary Multi-EPU Activation falsified`

---

# 2. Obiettivo B2R

Procedere con:

> **E11-X1.3-B2R — Post-Surplus Cross-Boundary 3× EPU with Spatial Equivalence**

Domanda sperimentale:

> **Una EPU1 equivalente a E06 può produrre surplus sufficiente per finanziare un solo BUY_LAND e quindi attivare EPU2 ed EPU3 quasi consecutivamente, mantenendo per ogni EPU una geometria operativa e un movement burden equivalenti a EPU1?**

La sequenza corretta è:

```text
EPU1
  ↓
productive surplus
  ↓
single BUY_LAND
  ↓
EPU2 activation
  ↓
EPU3 activation
  ↓
27 active productive tiles
```

---

# 3. Vincolo assoluto — NO BUY_LAND DAY 0

È vietato acquistare terreno al Day 0.

EPU1 deve operare inizialmente da sola.

Il land purchase può avvenire solo dopo:

> **productive surplus verificabile**

Non usare un giorno hard-coded.

Il trigger deve essere economico.

---

# 4. Trigger economico derivato

Definire:

```text
required_cash_for_first_expansion =
land_cost
+ startup_capital_EPU2
+ startup_capital_EPU3_if_immediately_planned
+ operating_reserve_EPU1
```

Se EPU3 non può partire esattamente nello stesso momento, usare:

```text
land_cost
+ startup_capital_EPU2
+ operating_reserve_EPU1
+ protected_capital_for_near_term_EPU3
```

La formula deve essere derivata da:

- seed cost reali;
- daily hire cost;
- worker demand;
- operating reserve;
- current inventory;
- expected near-term harvest.

NON introdurre magic thresholds.

---

# 5. Nessun vincolo Day 14

Il Day 14 di X1.3-B è un risultato osservato, NON una regola.

B2R deve misurare il giorno effettivo di acquisto.

L'obiettivo è:

> **comprare appena il surplus rende sostenibili EPU2 + EPU3**

senza starvation.

---

# 6. Vincolo architetturale — Spatial Equivalence

La EPU non è soltanto "9 tile".

Una EPU è:

> **9 compact tiles + E06-equivalent scheduling + local workforce + low movement burden**

Quindi:

> **EPU2 ed EPU3 devono essere repliche spaziali equivalenti di EPU1.**

---

# 7. EPU1 reference geometry

Ricostruire la geometria EPU1 esatta.

E06 / EPU1:

Farmer cluster:

```text
(4,4), (4,3), (3,4), (3,3)
```

Hand 1 cluster:

```text
(4,2), (3,2), (2,4), (2,3), (2,2)
```

Totale:

> **9 tiles**

Registrare:

- centroid;
- average intra-cluster distance;
- maximum worker-to-target distance;
- MOVE actions;
- productive actions.

Queste metriche diventano riferimento.

---

# 8. EPU2/EPU3 geometry design

Prima del BUILD creare:

`scratch/design_b2r_epu_geometry.py`

o equivalente.

Generare candidate layouts per EPU2/EPU3 che rispettino:

1. esattamente 9 tile ciascuna;
2. nessuna sovrapposizione;
3. proprietà legale dopo UN SOLO land purchase;
4. cluster compatti;
5. stessa topologia 4+5 o equivalente funzionale;
6. distanze worker→tile comparabili a EPU1;
7. spazio sufficiente per entrambe le unità;
8. nessun attraversamento sistematico della mappa.

---

# 9. Cross-boundary clarification

"EPU2 cross-boundary" NON significa:

> creare una forma lunga che attraversa due quadranti.

Significa:

> utilizzare efficientemente il bordo del terreno disponibile mantenendo una unità compatta.

La compattezza ha priorità sulla simmetria grafica.

---

# 10. Spatial acceptance criteria

Per EPU2 e EPU3 calcolare:

```text
avg_worker_target_distance
max_worker_target_distance
MOVE_actions_per_day
MOVE_per_productive_action
```

Confrontare con EPU1.

Classificare:

## SPATIALLY EQUIVALENT

se movement burden è nella stessa classe di EPU1.

## MODERATE SPATIAL PENALTY

se leggermente superiore ma plausibile.

## NOT EPU-EQUIVALENT

se esiste una penalità strutturale rilevante.

Non procedere al benchmark con layout `NOT EPU-EQUIVALENT`.

---

# 11. Nessun "Hand 3 travel penalty" accettabile

La frase:

> `Labor Travel Penalty (Hand 3)`

NON deve comparire come inevitabile conseguenza dello scaling.

Se Hand 3/Hand 4 devono percorrere 5–6 step extra rispetto a EPU1:

> **il layout è sbagliato**

e deve essere ridisegnato prima del benchmark.

---

# 12. Local workforce assignment

Ogni EPU deve avere workforce locale.

Definire una mappatura stabile:

- EPU1 workers;
- EPU2 workers;
- EPU3 workers.

Non consentire che un Hand assegnato a EPU3 attraversi sistematicamente EPU1/EPU2.

---

# 13. Farmer uniqueness

Esiste un solo Farmer permanente.

Non modellare "Farmer/Hand pair" replicata letteralmente.

Per EPU2/EPU3 usare Hands giornalieri con:

> **equivalente capacità locale di servizio**

La replica è funzionale, non identitaria.

---

# 14. Workforce scaling

Workforce workload-driven.

Registrare ogni giorno:

- Farmer;
- Hands requested;
- Hands accepted;
- EPU assignment;
- cost.

Non fissare automaticamente 6 worker.

---

# 15. EPU2 activation

Dopo il BUY_LAND:

EPU2 può attivarsi appena:

- tile legalmente disponibili;
- startup capital disponibile;
- workforce disponibile.

Registrare:

```text
EPU2_activation_day
EPU2_activation_step
```

---

# 16. EPU3 activation

EPU3 NON è più bloccata.

Può attivarsi appena:

- EPU2 è operativa;
- startup capital sufficiente;
- operating reserve protetta;
- workforce locale disponibile.

Registrare:

```text
EPU3_activation_day
EPU3_activation_step
```

---

# 17. Near-simultaneous activation

Calcolare:

```text
delta_activation =
EPU3_activation_day - EPU2_activation_day
```

Interpretazione:

- 0–1 day: `NEAR-SIMULTANEOUS`
- 2–3 days: `FAST FOLLOW`
- >3 days: `DELAYED`

Le soglie sono diagnostiche.

---

# 18. One-land-purchase constraint

Prima dell'attivazione EPU3:

```text
land_purchase_count == 1
```

Acceptance criterion:

> **EPU3 must activate without second BUY_LAND**

Se serve secondo terreno:

STOP.

---

# 19. EPU1 invariant

EPU1 deve restare semanticamente equivalente a X1.3-A.

Non modificarne:

- tile;
- crop ROI;
- Water-First;
- seed logic;
- market liquidation;
- local workforce behavior.

---

# 20. Crop policy invariata

Non introdurre Fast-EPU2-specific crops.

Usare E06 replicated mechanism per tutte le EPU.

B2R testa:

> **spatial density + activation timing + single-land amortization**

non crop tuning.

---

# 21. Water-First invariato

Preservare esattamente la semantica verificata.

---

# 22. Market policy invariata

Preservare:

- on-demand seed;
- immediate relevant liquidation;
- E06 ROI/day crop selection.

---

# 23. Benchmark protocol

Eseguire:

## Stage G — Geometry

NO simulation benchmark.

Verificare layout.

## Stage A0 — Smoke

1 episode seed0/pass.

## Stage B — Mini

5 paired episodes.

STOP dopo Stage B.

NON eseguire 10/30 automaticamente.

---

# 24. Stage G Stop Gate

Se EPU2/EPU3 non sono spatially equivalent:

> STOP.

Ridisegnare layout.

NON compensare con più workforce.

---

# 25. Stage A0 acceptance

Verificare:

1. Day 0: no BUY_LAND.
2. EPU1 behaves like A.
3. land purchased only after surplus.
4. only 1 land purchase before EPU3.
5. EPU2 active.
6. EPU3 active.
7. spatial equivalence retained.
8. no illegal actions.
9. provenance PASS.

---

# 26. Stage B acceptance

Su 5 episodes:

## NOT VALIDATED

se:

- EPU3 non si attiva;
- secondo BUY_LAND necessario;
- mean money <= B;
- movement penalty significativa;
- working capital collapse.

## PARTIAL

se:

- EPU3 si attiva solo in parte dei run;
- activation delayed;
- modest economic gain.

## VALIDATED

se:

- EPU2/EPU3 activate from one land purchase in majority;
- 27 active tiles achieved;
- B2R mean > B;
- movement equivalent;
- provenance PASS.

---

# 27. Existing references

NON rieseguire A e B.

Usare:

## X1.3-A

Mean:

> **$26,888.40**

## X1.3-B

Mean:

> **$28,727.40**

EPU2 Day:

> circa **14–15**

Usare dataset verificati esistenti.

---

# 28. Key economic comparison

Calcolare:

```text
B2R_increment_vs_A =
Money_B2R - Money_A
```

```text
B_increment_vs_A =
Money_B - Money_A
```

```text
land_amortization_gain =
B2R_increment_vs_A / B_increment_vs_A
```

Questo misura quanto più valore produce il primo land purchase.

---

# 29. 3× scaling efficiency

Calcolare:

```text
ratio_3x = Money_B2R / Money_A
efficiency_3x = ratio_3x / 3
```

Ma interpretare insieme al tempo di attivazione.

Una EPU attivata a metà episodio non può essere confrontata ingenuamente con 30 giorni completi.

---

# 30. Time-adjusted EPU productivity

Aggiungere una metrica:

```text
active_EPU_days
```

Per ciascuna EPU.

Calcolare:

```text
money_or_revenue_per_active_EPU_day
```

quando derivabile.

Questo permette di distinguere:

- unit efficiency;
- late activation penalty.

---

# 31. Productive density

Calcolare:

```text
active_tiles / owned_tiles
active_tiles / land_purchase_count
```

Target architetturale:

> massimizzare productive tiles abilitate per land purchase.

---

# 32. Movement comparison

Produrre:

| Metric | EPU1 | EPU2 | EPU3 |
|---|---:|---:|---:|
| Avg distance | | | |
| Max distance | | | |
| MOVE / productive action | | | |
| Productive actions / worker | | | |

EPU2/EPU3 devono restare nella classe EPU1.

---

# 33. Submission status

La precedente submission candidate X1.3-B resta:

> **READY BUT ON HOLD**

NON inviarla ancora.

Se B2R è `VALIDATED` e migliora B:

> B2R diventa nuova Kaggle candidate.

Se B2R fallisce correttamente:

> tornare a X1.3-B submission.

---

# 34. Packaging

NON costruire la submission definitiva finché Stage B non termina.

Se B2R diventa candidate:

preparare artifact in task successivo o, se già autorizzato dal supervisore, prepararlo ma NON caricarlo automaticamente.

---

# 35. Config delta

Produrre:

| Behavior | B | Old B2 | B2R |
|---|---|---|---|
| Day0 land | no | yes | **no** |
| Land trigger | post-surplus | immediate | **derived surplus** |
| EPU2 | yes | yes | yes |
| EPU3 | no | yes | **yes** |
| EPU3 same land | n/a | yes | **yes** |
| spatial equivalence | EPU1/EPU2 partial | poor EPU3 | **mandatory** |
| crop policy | E06 | E06 | **E06** |

---

# 36. Tests

Aggiungere test per:

1. no Day0 BUY_LAND B2R;
2. EPU1 unchanged;
3. EPU2 9 unique tiles;
4. EPU3 9 unique tiles;
5. no overlap;
6. one land purchase sufficient;
7. EPU3 gate enabled;
8. derived surplus trigger;
9. spatial distance threshold;
10. local workforce mapping;
11. no cross-EPU long travel;
12. crop policy unchanged;
13. Water-First unchanged;
14. market policy unchanged;
15. config immutability;
16. provenance.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 37. Documentation

Creare:

`docs/versions/E11_X1_3_B2R_post_surplus_spatially_equivalent_3x_epu.md`

Struttura minima:

1. Executive Summary
2. Correction of Previous B2
3. Hypothesis Status
4. No-Day0 Rule
5. Surplus Trigger
6. EPU Definition
7. Spatial Equivalence Standard
8. Geometry Audit
9. EPU1 Geometry
10. EPU2 Geometry
11. EPU3 Geometry
12. Distance Matrix
13. Workforce Mapping
14. Config Delta
15. Tests
16. Stage A0
17. Stage B
18. Land Purchase Timing
19. EPU2 Activation
20. EPU3 Activation
21. Activation Delta
22. One-Land Verification
23. Productive Density
24. Movement Equivalence
25. Economics
26. Time-Adjusted EPU Productivity
27. A vs B vs Old B2 vs B2R
28. Validation Verdict
29. Kaggle Candidate Verdict
30. Next Step

---

# 38. Project state

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Non sovrascrivere la storia del vecchio B2.

Marcarlo come:

> **incorrect implementation of intended hypothesis**

---

# 39. README

Se il README attuale indica X1.3-B come current submission candidate:

NON cambiarlo prima di Stage B.

Dopo Stage B:

- se B2R validated → aggiornare current local treatment;
- se B2R failed → lasciare B candidate.

---

# 40. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

NON:

- tag;
- push;
- Kaggle upload automatico.

---

# Deliverable finale obbligatorio

Riportare:

1. B2R BUILD status
2. previous B2 correction recorded YES/NO
3. Day0 land purchase eliminated YES/NO
4. geometry audit verdict
5. EPU1 coordinates
6. EPU2 coordinates
7. EPU3 coordinates
8. EPU overlap
9. EPU1 avg/max distance
10. EPU2 avg/max distance
11. EPU3 avg/max distance
12. spatial equivalence verdict
13. land trigger formula
14. actual land purchase day mean
15. land purchase count before EPU3
16. EPU2 activation day mean
17. EPU3 activation day mean
18. delta activation mean
19. near-simultaneous classification
20. peak active tiles
21. peak owned tiles
22. utilization
23. workforce per EPU
24. peak workforce
25. movement comparison
26. productive actions/worker
27. Mean Final Money
28. Median
29. Std
30. Min / Max
31. A Mean reference
32. B Mean reference
33. Old B2 Mean reference
34. B2R/A ratio
35. 3× scaling efficiency
36. incremental money vs A
37. land amortization gain vs B
38. active EPU days
39. revenue/money per active EPU day
40. working capital trajectory
41. provenance
42. config hash
43. episodes hash
44. tests
45. B2R verdict
46. Kaggle candidate: B or B2R
47. README update
48. files changed
49. next action

---

# Regola finale

La B2R è valida solo se verifica contemporaneamente:

> **NO Day-0 land purchase**

e:

> **EPU2/EPU3 spatially equivalent to EPU1**

e:

> **EPU3 activated without second land purchase**

Non accettare come "scaling" un layout che aumenta il movement burden.

Una EPU replicata deve mantenere:

> **la stessa efficienza spaziale dell'unità originale.**
