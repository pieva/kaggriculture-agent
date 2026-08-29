# E11-06 — BUILD + VERIFY — Workforce–Land Co-Scaling

## Contesto

L’audit **E11-B1 — Competitor Expansion Timing Audit** ha chiarito che il gap rispetto ai top player è **misto**, ma con una componente dominante di **Activation Gap**.

Riferimenti osservati:

- **Top competitor 3Q / 75 tile:** Mean Day `4.20`
- **E11-03 3Q / 75 tile:** Mean Day `5.36`
- **Gap:** `+1.16 giorni`

- **Top competitor 4Q / 100 tile:** Mean Day `8.53`
- **E11-03 4Q / 100 tile:** Mean Day `11.39`
- **Gap:** `+2.86 giorni`

Il ritardo territoriale esiste ed è rilevante, ma non spiega da solo il gap economico.

Il divario principale emerge nella capacità di attivare il terreno acquistato:

| Metrica | Top competitor | E11-03 |
|---|---:|---:|
| Workforce @75 tile | 4–6 | 4 |
| Workforce @100 tile | 8–10 | 6 |
| Active tiles @75 | 35–45 | 20 |
| Active tiles @100 | 75–85 | 54 |
| Livestock | Day 9–12 | OFF |
| Mean Final Money | ~$76k | ~$7.5k |

La conclusione dell’audit è:

> **Il timing territoriale è moderatamente peggiore dei top, ma il gap dominante è la capacità di attivare e monetizzare rapidamente la superficie acquisita.**

---

# 1. Nuova interpretazione architetturale

Le iterazioni precedenti hanno trattato spesso workforce come elemento downstream:

```text
LAND
  ↓
WORKFORCE
  ↓
PRODUCTION
```

Il benchmark dei top suggerisce invece:

```text
LAND + WORKFORCE CO-SCALING
          ↓
ACTIVE PRODUCTIVE FOOTPRINT
          ↓
PRODUCTION
          ↓
REVENUE
```

La workforce non viene introdotta soltanto dopo il completamento dell’espansione.

Nei competitor di vertice cresce **insieme** alla superficie posseduta.

---

# 2. Obiettivo E11-06

Procedere con:

> **E11-06 — Workforce–Land Co-Scaling**

Domanda sperimentale:

> **Portando la workforce alla scala osservata nei top mentre 75 e 100 tile vengono acquisiti, ProductiveMassROIAgent riesce a convertire tempestivamente la nuova superficie in 70–80 tile produttive senza compromettere il timing territoriale raggiunto da E11-03?**

Questa iterazione deve verificare il legame causale:

```text
MORE LAND
+
MORE LABOR
    ↓
MORE ACTIVE TILES
    ↓
MORE PRODUCTIVE CAPACITY
```

---

# 3. Baseline di riferimento

Ripartire dalla configurazione:

> **E11-03 — Expansion Gate Unlock**

NON utilizzare E11-04 o E11-05 come base comportamentale.

E11-03 è la configurazione che ha dimostrato sperimentalmente:

- Q2/3Q unlock = `83.3%`
- Q3/4Q unlock = `60.0%`
- 4 quadranti / 100 tile raggiungibili
- peak active tiles = `54`
- peak workforce = `6`

Ripristinare quindi, come baseline:

- `expansion_gate_mode = "MIN_OPERATIONAL"`
- Expansion Capital Protection rigida
- crop spending policy E11-03
- action hierarchy E11-03
- locality E11-03
- livestock logic E11-03
- end-game logic E11-03

---

# 4. Controlled Change

E11-06 deve modificare una sola area rispetto a E11-03:

> **Workforce Scaling Policy durante l’espansione territoriale**

Non modificare contemporaneamente:

- crop spending;
- seed protection;
- land readiness;
- livestock;
- crop portfolio;
- locality;
- end-game;
- action priority generale.

---

# 5. Ipotesi E11-06

Formalizzare:

> **H11-06 — Workforce–Land Co-Scaling Hypothesis:** E11-03 riesce ad acquistare nuova capacità territoriale, ma non dispone di workforce sufficiente per attivarla rapidamente. Consentire hiring progressivo durante l’espansione, mantenendo la protezione del capitale per il terreno, dovrebbe aumentare significativamente active tiles senza compromettere il timing di acquisizione di 75 e 100 tile.

---

# 6. Benchmark competitivo da seguire

Utilizzare i valori E11-B1 come riferimento empirico.

### A 75 tile / 3Q

Top competitor:

- Mean timing: Day `4.20`
- workforce: `4–6`
- active tiles: `35–45`

### A 100 tile / 4Q

Top competitor:

- Mean timing: Day `8.53`
- workforce: `8–10`
- active tiles: `75–85`

Questi valori sono benchmark osservativi.

NON trasformarli automaticamente in costanti rigide.

---

# 7. Target architetturali E11-06

Utilizzare come riferimento:

## 3Q / 75 tile

- timing: idealmente `≤ Day 5`
- workforce: `≥4`, preferibilmente `4–6`
- active tiles: obiettivo indicativo `≥35`

## 4Q / 100 tile

- timing: idealmente `≤ Day 10`
- workforce: almeno `≥8`
- active tiles: almeno `≥70`

Questi valori servono per valutare il gap.

Non usare failure automatico per differenze minime dovute al campione.

---

# 8. Protezione del capitale territoriale

La lezione E11-01 → E11-05 è chiara:

> **il capitale destinato a Q2/Q3 non deve essere consumato da spesa discrezionale.**

Mantenere quindi la protezione E11-03.

Tuttavia, E11-06 deve distinguere:

- seed/livestock spending discrezionale;
- hiring necessario alla capacità operativa.

L’hiring può essere consentito durante l’accumulo territoriale **solo se non compromette materialmente il prossimo BUY_LAND**.

---

# 9. Costo reale dell’hiring

Le meccaniche dell’ambiente hanno già verificato il costo Fibonacci di `HIRE`.

Riutilizzare i valori reali.

Non assumere che hiring e BUY_LAND abbiano lo stesso impatto finanziario.

Dato che i primi hire hanno costo molto basso rispetto a `$1,000` di terreno, E11-06 deve verificare se è possibile sostenere un workforce ramp senza compromettere il land timing.

Registrare il costo cumulativo reale sostenuto.

---

# 10. Workforce Stage Model

Implementare una logica di co-scaling semplice.

Concettualmente:

```text
2Q / 50 tiles
    ↓
bootstrap workforce
    ↓
3Q / 75 tiles
    ↓
scale workforce
    ↓
4Q / 100 tiles
    ↓
scale workforce again
```

Non utilizzare obbligatoriamente numeri hard-coded per ogni quadrante se l’architettura consente una regola dinamica migliore.

---

# 11. Hiring Readiness

La decisione di assumere deve considerare almeno:

- owned tiles;
- active tiles;
- pending work/backlog;
- current workforce;
- next land funding requirement;
- operating reserve;
- remaining horizon.

La regola deve evitare entrambi gli estremi:

### Underhiring

Nuovo terreno posseduto ma inattivo.

### Overhiring

Worker aggiuntivi senza lavoro produttivo sufficiente.

---

# 12. Workforce Target Logic

Preferire una funzione legata alla capacità produttiva prevista.

Per esempio, se coerente con il codice:

```text
desired_workers = f(
    owned_tiles,
    active_tiles,
    expansion_stage
)
```

oppure modello equivalente.

Non implementare semplicemente:

```text
if 75_tiles:
    workers = 6
if 100_tiles:
    workers = 10
```

se esiste una logica più robusta.

I benchmark 4–6 e 8–10 devono guidare la scala, non sostituire il ragionamento.

---

# 13. Hiring prima del nuovo terreno

L’audit B1 mostra che parte della workforce viene aumentata **prima o contestualmente** al completamento dell’espansione.

E11-06 può quindi assumere worker prima del prossimo BUY_LAND se:

1. il costo dell’hire è basso;
2. il capitale per il terreno rimane realisticamente protetto;
3. la workforce aggiuntiva può già essere utilizzata;
4. l’hire riduce il rischio che il nuovo terreno rimanga inattivo.

Questo rappresenta il punto nuovo dell’esperimento.

---

# 14. Land Timing Preservation

Non accettare un miglioramento workforce ottenuto ritardando fortemente l’espansione.

Confrontare con E11-03:

- 3Q mean Day `5.36`
- 4Q mean Day `11.39`

E con i top:

- 3Q mean Day `4.20`
- 4Q mean Day `8.53`

E11-06 deve idealmente:

- preservare o migliorare E11-03;
- ridurre, se possibile, il gap verso i top.

---

# 15. Land Regression Gate

Classificare:

## NO TIMING REGRESSION

Timing uguale o migliore di E11-03.

## MODERATE TIMING REGRESSION

Ritardo limitato con forte miglioramento di active footprint, da valutare quantitativamente.

## MAJOR TIMING REGRESSION

Il workforce scaling ritarda sostanzialmente Q2/Q3 o riduce fortemente gli unlock rate.

In questo caso E11-06 non è accettabile.

---

# 16. Active Footprint Activation

Questo è il principale risultato da misurare.

E11-03:

- active tiles @75 ≈ `20`
- peak active tiles ≈ `54`

Top:

- `35–45` @75
- `75–85` @100

E11-06 deve verificare se workforce co-scaling consente di colmare questo divario.

Target indicativi:

> **≥35 active tiles a 75 tile owned**

e

> **≥70 active tiles a 100 tile owned**

---

# 17. Worker Utilization

Aggiungere instrumentation per evitare di confondere più worker con maggiore capacità reale.

Registrare, quando possibile:

- active actions per worker;
- idle turns;
- movement turns;
- productive actions;
- backlog;
- tile/worker ratio.

Se una metrica esatta non è disponibile, usare proxy espliciti.

---

# 18. Travel Dilution

Con 8–10 worker e 100 tile, locality diventa importante.

NON modificare la locality policy in E11-06.

Ma misurarne il comportamento.

Registrare:

- average movement actions;
- cross-quadrant movements;
- idle worker;
- backlog per quadrante, se ricostruibile.

Se workforce aumenta ma active footprint non cresce:

> **Travel / Scheduling Bottleneck** può diventare il successivo candidato.

---

# 19. Crop Policy invariata

Non cambiare seed spending o crop allocation rispetto a E11-03.

Questo è importante per l’attribuzione.

Quindi E11-06 NON deve:

- riabilitare E11-04;
- introdurre Productive Window E11-05;
- cambiare Melon/Strawberry timing;
- cambiare Tomato usage;
- cambiare Wheat/Carrot logic.

Se con più worker i crop rimangono insufficienti, questo deve emergere come nuovo bottleneck.

---

# 20. Livestock invariato

Non modificare la logica livestock.

Registrare però:

- activation rate;
- timing;
- Cow;
- Sheep;
- Wheat availability;
- workforce al momento dell’attivazione.

L’audit B1 mostra livestock competitor attivato circa Day `9–12`.

Se land + workforce + active tiles migliorano e livestock rimane OFF:

> livestock sarà candidato naturale per E11-07.

---

# 21. Configurazione E11-06

Creare configurazione distinta e riproducibile:

`E11_06_CONFIG`

oppure equivalente.

Possibili nuovi parametri:

```text
workforce_scaling_mode = "LAND_CO_SCALING"
target_worker_ratio = ...
pre_land_hiring_enabled = True
max_pre_land_hiring_cost = ...
```

Introdurre solo parametri realmente necessari.

---

# 22. Hiring Cost Protection

Implementare una safeguard semplice.

Prima di un hire durante accumulo territoriale:

```text
cash_after_hire
```

deve rimanere compatibile con:

- operating reserve;
- next land acquisition;
- capacità produttiva corrente.

Non è necessario preservare fisicamente `$1,300` dopo ogni singolo hire se il costo è minimo e la farm sta generando revenue.

Ma non ricreare Expansion Cash Lock.

---

# 23. Telemetria workforce

Registrare per episodio:

- first hire timing;
- ogni hire event;
- hire cost;
- cumulative hire spending;
- workforce @50 tiles;
- workforce @75 tiles;
- workforce @100 tiles;
- peak workforce;
- active tiles per worker;
- idle/proxy utilization;
- movement/proxy travel burden.

---

# 24. Telemetria land + workforce combinata

Per ogni evento:

### 3Q / 75 tile

registrare:

- day
- cash
- workers
- active tiles
- utilization
- cumulative hire spending

### 4Q / 100 tile

registrare:

- day
- cash
- workers
- active tiles
- utilization
- cumulative hire spending

Questa è la tabella centrale di E11-06.

---

# 25. Test specifici E11-06

Estendere la suite.

Testare almeno:

1. E11-03 rimane riproducibile.
2. E11-06 usa `MIN_OPERATIONAL`.
3. Capital Protection rimane attiva.
4. pre-land hiring consentito quando finanziariamente sicuro.
5. pre-land hiring bloccato quando comprometterebbe BUY_LAND.
6. workforce cresce con owned/active capacity.
7. workforce non supera max configurato.
8. hiring non continua se non esiste workload sufficiente.
9. Q2 può essere acquistato.
10. Q3 può essere acquistato.
11. crop policy invariata.
12. livestock logic invariata.
13. locality invariata.
14. action legality.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

Tutti i test devono passare.

---

# 26. Benchmark locale

Eseguire benchmark paired da **30 episodi** sugli stessi seed.

Confrontare almeno:

- E10-01
- E11-01
- E11-03
- E11-06

Mantenere E11-02/04/05 solo se utile e senza complicare l’output.

Metriche economiche:

- Mean Final Money
- Median
- Sample Std Dev (`ddof=1`)
- Min
- Max
- Completion
- Disqualification
- breakdown opponent
- paired wins vs E10
- paired wins vs E11-03
- delta
- ratio

---

# 27. Benchmark architetturale

Registrare:

## Timing

- 3Q unlock rate
- mean/median 3Q day
- 4Q unlock rate
- mean/median 4Q day

## Workforce

- workforce @50
- workforce @75
- workforce @100
- peak workforce

## Active Footprint

- active tiles @50
- active tiles @75
- active tiles @100
- peak active tiles

## Utilization

- utilization @75
- utilization @100

---

# 28. Confronto con competitor

Produrre:

| Metrica | Top | E11-03 | E11-06 |
|---|---:|---:|---:|
| 3Q day | 4.20 | 5.36 | |
| 4Q day | 8.53 | 11.39 | |
| Workers @75 | 4–6 | 4 | |
| Workers @100 | 8–10 | 6 | |
| Active @75 | 35–45 | 20 | |
| Active @100 | 75–85 | 54 | |
| Utilization @75 | 46.7–60% | 26.7% | |
| Utilization @100 | 75–85% | 54% | |
| Livestock timing | 9–12 | OFF | |

---

# 29. Success Gate architetturale

## WORKFORCE CO-SCALING NOT VALIDATED

Se:

- workforce non supera significativamente E11-03;
- active tiles non aumentano;
- oppure land timing regredisce fortemente.

---

## PARTIAL CO-SCALING

Se:

- workforce cresce;
- active footprint migliora;
- ma 4Q o 70+ active tile non sono stabili.

---

## WORKFORCE–LAND CO-SCALING VALIDATED

Se la maggioranza delle run raggiunge indicativamente:

- 3Q con `≥4–6 worker`;
- 4Q con `≥8 worker`;
- active footprint significativamente superiore a E11-03;
- idealmente `≥70 active tiles`;
- senza major land timing regression.

---

# 30. Compounding Test

Valutare:

```text
LAND
+
WORKFORCE
    ↓
ACTIVE FOOTPRINT
    ↓
PRODUCTION
    ↓
REVENUE
```

Classificare:

- `NOT OBSERVED`
- `WEAK`
- `PARTIAL`
- `STRONG`

Non considerare `WORKFORCE + LAND` sufficiente se la produzione non aumenta.

---

# 31. Economic Decision Gate

Rimane invariato:

| Mean Final Money | Verdict |
|---:|---|
| `< $50k` | `FAIL` |
| `$50k – <$60k` | `MINIMUM SUCCESS` |
| `$60k – <$70k` | `COMPETITIVE` |
| `$70k – <$75k` | `NEAR TOP BENCHMARK` |
| `≥ $75k` | `TARGET ACHIEVED` |

Ma E11-06 deve essere interpretato prima di tutto come esperimento di activation.

---

# 32. Matrice diagnostica

| Stato | Diagnosi |
|---|---|
| workforce cresce ma 3Q/4Q regrediscono | hiring troppo aggressivo |
| land preservato, workers ≤6 | workforce trigger insufficiente |
| land + workers crescono, active tiles basse | scheduling/crop activation bottleneck |
| land + workers + active tiles crescono, livestock OFF | livestock activation bottleneck |
| active footprint ≥70 ma money ancora basso | crop/output/monetization bottleneck |
| ≥$50k | E11 architecture direction validated |
| ≥$75k | Competitive target achieved |

---

# 33. Dominant Bottleneck

Al termine identificare un solo:

> **dominant bottleneck**

Possibili esiti:

- land timing regression;
- workforce trigger;
- worker utilization;
- travel dilution;
- crop activation;
- watering throughput;
- harvest throughput;
- livestock activation;
- feed;
- market throughput;
- end-game conversion.

Non correggerlo nello stesso task.

---

# 34. Deliverable documentale

Creare:

`docs/versions/E11_06_workforce_land_co_scaling.md`

Struttura minima:

1. Executive Summary
2. E11-B1 Findings
3. H11-06 Hypothesis
4. Controlled Change
5. E11-03 Baseline Restored
6. Workforce–Land Co-Scaling Architecture
7. Hiring Readiness
8. Land Capital Protection
9. Workforce Target Logic
10. Pre-Land Hiring
11. Configuration Delta
12. Invariants Preserved
13. Tests
14. Benchmark Protocol
15. Economic Results
16. 3Q Timing
17. 4Q Timing
18. Workforce @50/75/100
19. Active Tiles @50/75/100
20. Utilization
21. Competitor Comparison
22. Worker Utilization
23. Travel Observation
24. Livestock Observation
25. Trajectory
26. Compounding Verdict
27. Architecture Verdict
28. Economic Verdict
29. Dominant Bottleneck
30. Recommendation for E11-07

---

# 35. Aggiornamento documentazione

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato finale:

> **E11-06 BUILD + LOCAL VERIFY COMPLETED — awaiting supervisor review**

Non dichiarare E11 completato.

---

# 36. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

Non effettuare:

- commit finale;
- tag;
- push;
- Kaggle submission.

---

# Deliverable finale

Al termine fermarsi e riportare:

1. **E11-06 BUILD status**
2. **controlled change**
3. **workforce co-scaling logic**
4. **invarianti preservate**
5. **test result**
6. **Mean Final Money**
7. **Median / Std / Min / Max**
8. **delta vs E10-01**
9. **delta vs E11-03**
10. **paired wins**
11. **3Q unlock rate**
12. **3Q mean/median timing**
13. **4Q unlock rate**
14. **4Q mean/median timing**
15. **Land Timing Regression Verdict**
16. **workers @50**
17. **workers @75**
18. **workers @100**
19. **peak workforce**
20. **active tiles @50**
21. **active tiles @75**
22. **active tiles @100**
23. **peak active tiles**
24. **utilization @75**
25. **utilization @100**
26. **worker utilization/travel**
27. **livestock activation**
28. **confronto top vs E11-03 vs E11-06**
29. **Compounding Verdict**
30. **Architecture Deployment Verdict**
31. **Economic Decision Gate**
32. **dominant bottleneck**
33. **file creati/modificati**
34. **proposta E11-07**

## Regola finale

Se l’hiring causa una regressione importante del land timing:

> **ridurre esclusivamente l’aggressività del workforce scaling.**

Se il land timing è preservato ma workforce non arriva alla scala benchmark:

> **correggere successivamente il workforce trigger.**

Se land + workforce raggiungono la scala attesa ma active tiles rimangono basse:

> **il prossimo esperimento deve intervenire sull’attivazione/scheduling, non su ulteriore hiring.**

Se land + workforce + active footprint si avvicinano ai top ma livestock resta OFF:

> **E11-07 deve concentrarsi sul livestock.**

Se viene raggiunto **≥$50k**, la direzione E11 è validata.

Se viene raggiunto **≥$75k**, il Competitive Target è raggiunto.

**Non modificare crop policy, livestock, locality o end-game in E11-06. Fermarsi dopo BUILD + LOCAL VERIFY e attendere approvazione.**