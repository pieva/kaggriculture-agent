# E11-X1.1 — BUILD + VERIFY — Pre-3Q Workforce Productivity Scaling

## Contesto

La nuova baseline quantitativa autorevole è:

> **E11-VB1 — Verified Baseline 1**

Run verificato:

`E11-VB1-20260827-084428`

Baseline macchina:

- Mean Final Money: **$429.00**
- 3Q / 75 tile unlock: **0 / 30**
- 4Q / 100 tile unlock: **0 / 30**
- Peak land: **50 tile / 2Q**
- Mean / Peak active tiles: **16.93 / 17**
- Mean / Peak workforce: **2 / 2**
- Livestock: **OFF**
- Provenance verifier: **PASS**

E11-X1 ha tentato di intervenire esclusivamente su:

> **essential spending vs next-land capital accumulation**

con:

- `accumulation_3q_mode = "DISCIPLINED_ACCUMULATION"`
- `accumulation_3q_optional_reserve = $500`

Risultato Stage B:

- 3Q unlock: **0 / 5**
- Mean Final Money: **$429**
- Peak active tiles: **17**
- Peak workforce: **2**
- capital gap to 3Q: circa **$191–$561**

Verdetto:

> **X1 NOT VALIDATED**

La riduzione della spesa non ha modificato il comportamento economico della baseline.

---

# 1. Nuova interpretazione del bottleneck

I dati verificati suggeriscono che il problema possa essere a monte del semplice accumulo di capitale:

```text
50 tile owned
    ↓
only 2 workers
    ↓
~17 active productive tiles
    ↓
low productive throughput
    ↓
insufficient revenue generation
    ↓
cash cannot reach 3Q land threshold
```

La farm possiede già:

> **2Q / 50 tile**

ma ne utilizza produttivamente solo circa:

> **17**

con:

> **2 worker**

Quindi la strategia sta tentando di finanziare ulteriore terreno senza sfruttare adeguatamente quello già disponibile.

---

# 2. Evidenza benchmark competitor

E11-B1 ha prodotto un benchmark competitor indipendente e mantenuto come evidenza valida dopo l'audit di provenance.

Riferimenti osservati nei top player:

## 3Q / 75 tile

- Mean expansion timing: **Day 4.20**
- Workforce: **4–6 worker**
- Active productive tiles: **35–45**
- Utilization: **46.7–60.0%**

## 4Q / 100 tile

- Mean expansion timing: **Day 8.53**
- Workforce: **8–10 worker**
- Active productive tiles: **75–85**
- Utilization: **75–85%**

## Livestock

- activation: **Day 9–12**

L'audit ha inoltre mostrato che:

> **l'hiring nei top avviene molto presto e cresce insieme all'espansione territoriale.**

Questa evidenza deve essere utilizzata per guidare E11-X1.1.

---

# 3. Riferimento storico di produttività

Le strategie precedenti su footprint molto più piccoli hanno già dimostrato che una workforce più ampia può sostenere livelli economici molto superiori alla E11-VB1.

In particolare, il vecchio riferimento E06 / 9-tile multi-worker ha prodotto risultati nell'ordine di:

> **~$25k Mean Final Money**

Non rieseguire E06 in questo task.

Usarlo esclusivamente come:

> **historical productivity reference**

e NON come baseline causale.

La domanda diagnostica è:

> **Se 50 tile con più workforce producono ancora molto meno di una vecchia strategia a 9 tile, allora il bottleneck non è solo il numero di worker ma probabilmente scheduling, watering, planting, movement o crop activation.**

---

# 4. Obiettivo E11-X1.1

Procedere con:

> **E11-X1.1 — Pre-3Q Workforce Productivity Scaling**

Domanda sperimentale:

> **Aumentando la workforce su 2Q / 50 tile prima del 3Q unlock, mantenendo invariati land gate e crop/capital policy della baseline verificata, riusciamo ad aumentare active footprint e revenue abbastanza da finanziare naturalmente il passaggio a 3Q / 75 tile?**

Questa iterazione deve testare:

```text
MORE WORKFORCE
      ↓
MORE ACTIVE TILES
      ↓
MORE PRODUCTIVE THROUGHPUT
      ↓
MORE REVENUE
      ↓
3Q CAPITAL ACCUMULATION
```

---

# 5. Controlled Change

Rispetto a E11-VB1 modificare una sola area:

> **workforce scaling before 3Q**

Mantenere invariati:

- land readiness;
- capital protection;
- crop policy;
- seed policy;
- locality;
- livestock;
- action hierarchy;
- end-game;
- environment;
- benchmark protocol.

NON combinare X1.1 con:

- Strict Land Float Lock;
- nuova crop allocation;
- nuovo expansion gate;
- nuovo livestock logic;
- nuova seed release.

---

# 6. Ipotesi E11-X1.1

Formalizzare:

> **H11-X1.1 — Pre-3Q Workforce Productivity Hypothesis:** E11-VB1 non riesce ad accumulare capitale per 3Q perché 2 worker non riescono a utilizzare abbastanza dei 50 tile già posseduti. Una workforce portata progressivamente nella fascia osservata nei competitor prima o durante il primo expansion unlock dovrebbe aumentare active tiles, throughput e revenue senza compromettere in modo materiale il capitale necessario a BUY_LAND.

---

# 7. Benchmark-driven workforce target

NON inventare un target arbitrario.

Utilizzare come riferimento competitor:

> **4–6 worker già intorno al passaggio a 3Q / 75 tile**

E11-X1.1 deve quindi testare una workforce pre-3Q che possa crescere da:

> **2 worker**

verso:

> **4–6 worker**

senza imporre automaticamente 6 worker in ogni episodio.

Il range competitor guida la scala.

---

# 8. Hiring timing

Il benchmark competitor indica che l'hiring avviene molto presto.

Per questo E11-X1.1 deve permettere hiring:

> **prima del raggiungimento di 3Q**

e non soltanto dopo l'acquisto del nuovo quadrante.

Registrare esattamente:

- first hire day;
- second hire day;
- subsequent hire days;
- worker count per day;
- cash before/after hire.

---

# 9. Hiring affordability

Il costo HIRE è stato verificato come curva Fibonacci e i primi hire hanno costo molto ridotto rispetto al costo land di `$1,000`.

Non trattare quindi hiring e BUY_LAND come investimenti equivalenti.

La decisione di assumere deve considerare:

- hire cost reale;
- current cash;
- next-land capital gap;
- operating reserve;
- active tiles;
- workload;
- idle capacity.

---

# 10. Hiring rule

Preferire una logica semplice basata su capacità sottoutilizzata.

Concettualmente:

```text
IF
    owned_tiles == 50
AND active_tiles below desired productive footprint
AND additional worker can be afforded safely
AND expected workload exists
THEN
    HIRE
```

Non usare giorni hard-coded se non strettamente necessario.

---

# 11. Desired productive footprint

Il benchmark competitor mostra:

- 35–45 active tiles a 75 tile owned.

Prima del 3Q, su 50 tile, X1.1 deve almeno verificare se una workforce maggiore riesce a superare nettamente i:

> **17 active tiles di VB1**

Usare come obiettivo diagnostico:

> **30–40 active tiles**

NON come soglia rigida di successo.

---

# 12. Workforce utilization

Non considerare automaticamente positivo assumere più worker.

Registrare:

- productive actions;
- movement actions;
- idle actions;
- active tiles per worker;
- backlog;
- worker utilization proxy.

Se worker aumentano ma active tiles non crescono:

> il bottleneck diventa scheduling / activation, non hiring.

---

# 13. Capital impact of hiring

Registrare:

- cumulative hire spending;
- capital gap to 3Q prima/dopo ogni hire;
- tempo necessario a recuperare il costo dell'hire tramite revenue.

L'obiettivo è verificare empiricamente se:

> **il costo minimo dell'hiring viene più che compensato dall'aumento della produzione.**

---

# 14. 3Q unlock resta il gate primario

La metrica primaria resta:

> **3Q / 75 tile unlock rate**

Baseline VB1:

> **0%**

X1.1 deve produrre:

> **>0% come requisito minimo**

e idealmente mostrare unlock ripetuto.

---

# 15. Timing competitor

Benchmark top:

> **3Q Mean Day = 4.20**

Registrare X1.1 timing quando l'unlock avviene.

Non imporre Day 4.20 come target immediato.

Usarlo come:

> **benchmark competitivo**

---

# 16. Secondary Gate — productivity before expansion

Prima dell'evento 3Q registrare:

- active tiles;
- worker count;
- cash;
- cumulative revenue;
- capital gap.

Il trattamento è promettente anche prima dell'unlock se mostra:

> workforce ↑ → active footprint ↑ → revenue ↑ → capital gap ↓

---

# 17. Non usare Final Money come gate primario

Final Money resta diagnostico.

X1.1 può essere utile anche se il risultato finale resta basso, purché dimostri causalmente:

- workforce scaling;
- footprint scaling;
- maggiore revenue;
- riduzione del capital gap;
- primo 3Q unlock.

---

# 18. Historical 9x9 / E06 reference

Nel report includere una sezione:

> **Historical Productivity Sanity Check**

Confrontare senza rieseguire:

| Metric | Historical E06 / small footprint | E11-VB1 | E11-X1.1 |
|---|---:|---:|---:|
| Mean Final Money | ~25k historical | $429 | |
| Workforce | multi-worker | 2 | |
| Owned/Productive footprint | small | 50 owned / ~17 active | |

Specificare chiaramente che:

> E06 è un riferimento storico di sanità produttiva, NON una baseline machine-verifiable del trattamento corrente.

---

# 19. Protocollo rapido confermato

Utilizzare:

> **1 → 5 → 10**

NON 30 episodi automatici.

## Stage A

1 episodio.

## Stage B

5 episodi appaiati.

## Stage C

10 episodi appaiati solo se Stage B mostra un cambiamento reale.

Confronto ordinario:

- E11-VB1
- E11-X1.1

NON rieseguire tutte le versioni precedenti.

---

# 20. Stop Gate Stage B

Se dopo 5 episodi:

- worker rimangono 2;
- oppure worker aumentano ma active tiles restano ~17;
- oppure 3Q resta 0/5 e capital gap non migliora;

fermarsi.

Non eseguire Stage C.

Identificare il primo bottleneck downstream.

---

# 21. Stage C

Eseguire 10 episodi solo se Stage B mostra almeno uno di questi segnali:

- 3Q unlock > 0;
- active tiles aumentano sostanzialmente;
- capital gap diminuisce in modo sistematico;
- revenue trajectory migliora.

---

# 22. Provenance

Usare integralmente il protocollo R3:

```text
CONFIG SNAPSHOT
      ↓
RUN ID
      ↓
RAW EPISODES
      ↓
SUMMARY
      ↓
SHA-256
      ↓
PROVENANCE VERIFIER
```

Run ID:

> `E11-X1.1-<timestamp>`

Dataset:

```text
results/e11/<RUN_ID>/
    config.json
    episodes.json
    summary.json
```

Nessun overwrite.

---

# 23. Config delta

Produrre:

| Parameter | VB1 | X1.1 |
|---|---|---|

Il delta deve riguardare esclusivamente workforce scaling.

Se emergono altre differenze:

> correggere prima del benchmark.

---

# 24. Telemetria obbligatoria

Registrare per episodio:

### Workforce

- workforce per checkpoint;
- first hire day;
- each hire event;
- hire cost;
- cumulative hire spending;
- productive actions;
- movement;
- idle proxy.

### Production

- active tiles;
- planted tiles;
- harvested tiles;
- revenue trajectory;
- active tiles / worker.

### Capital

- cash;
- capital gap to 3Q;
- cash before/after hire;
- cash before/after harvest;
- cash before BUY_LAND.

### Land

- 3Q readiness;
- 3Q unlock;
- unlock timing.

---

# 25. Checkpoint comparison

Confrontare VB1 vs X1.1 almeno a:

- 25%
- 50%
- 75%
- 100%

Tabella:

| Metric | VB1 | X1.1 |
|---|---:|---:|
| Workers | | |
| Active tiles | | |
| Money | | |
| Capital gap to 3Q | | |
| 3Q owned | | |

---

# 26. Test specifici

Aggiungere test per:

1. VB1 factory invariata.
2. X1.1 config distinta.
3. X1.1 modifica solo workforce policy.
4. pre-3Q hire possibile.
5. hire bloccato se operating reserve non sicura.
6. workforce target non supera config max.
7. hiring non avviene senza workload.
8. land readiness invariata.
9. capital protection invariata.
10. crop policy invariata.
11. livestock invariato.
12. config immutable during run.
13. provenance schema valido.

Eseguire:

`.venv\Scripts\pytest.exe tests/`

---

# 27. Success classification

## X1.1 NOT VALIDATED

Se:

- workforce non cresce;
- oppure cresce ma active footprint/revenue non migliorano;
- 3Q resta bloccato senza riduzione del capital gap.

## X1.1 PARTIAL

Se:

- workforce cresce;
- active footprint/revenue migliorano;
- ma 3Q resta instabile.

## X1.1 VALIDATED

Se:

- workforce cresce nella direzione benchmark;
- active tiles aumentano significativamente;
- 3Q viene raggiunto ripetutamente;
- provenance PASS.

---

# 28. Diagnostica successiva

Interpretare:

| Esito | Diagnosi |
|---|---|
| Workers restano 2 | hiring trigger bottleneck |
| Workers 4–6, active ~17 | scheduling/activation bottleneck |
| Workers 4–6, active 30–40, 3Q ancora 0 | capital/revenue conversion bottleneck |
| 3Q raggiunto | first land unlock validated |
| 3Q stabile ma timing molto >4.2 | expansion cadence bottleneck |

---

# 29. Nessun intervento su Q3

Anche se X1.1 raggiunge 3Q:

NON correggere automaticamente 3Q → 4Q nello stesso task.

Fermarsi dopo la verifica.

---

# 30. Benchmark da 30

NON eseguire automaticamente.

Se X1.1 è VALIDATED su 10 episodi:

> raccomandare 30-episode validation.

---

# 31. Deliverable documentale

Creare:

`docs/versions/E11_X1_1_pre3q_workforce_productivity_scaling.md`

Struttura minima:

1. Executive Summary
2. E11-VB1 Baseline
3. X1 Failure
4. Competitor Workforce Benchmark
5. Historical Productivity Reference
6. H11-X1.1
7. Controlled Change
8. Config Delta
9. Pre-3Q Hiring Logic
10. Hiring Cost Analysis
11. Workforce Utilization
12. Active Footprint
13. Capital Gap
14. Provenance
15. Tests
16. Stage A
17. Stage B
18. Stage C
19. 3Q Unlock
20. Timing
21. Productivity Sanity Check
22. X1.1 Verdict
23. Dominant Bottleneck
24. 30-Episode Recommendation
25. Next Step

---

# 32. Aggiornamento progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato:

> **E11-X1.1 BUILD + REDUCED LOCAL VERIFY COMPLETED — awaiting supervisor review**

---

# 33. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

NON:

- commit;
- tag;
- push;
- Kaggle submission.

---

# Deliverable finale obbligatorio

Riportare:

1. E11-X1.1 BUILD status
2. run_id
3. controlled change
4. config delta
5. test suite
6. Stage A result
7. Stage B result
8. Stage C executed YES/NO
9. workforce VB1
10. workforce X1.1
11. first hire timing
12. peak workforce
13. cumulative hire cost
14. active tiles VB1
15. active tiles X1.1
16. active tiles / worker
17. capital gap trajectory
18. Mean Final Money
19. revenue trajectory
20. 3Q unlock rate
21. 3Q timing
22. competitor 3Q timing reference
23. historical E06 productivity sanity check
24. workforce productivity verdict
25. provenance PASS/FAIL
26. config SHA-256
27. episodes SHA-256
28. X1.1 validation verdict
29. dominant bottleneck
30. 30-episode validation recommended YES/NO
31. file creati/modificati
32. next-step recommendation

---

# Regola finale

E11-X1.1 deve sfruttare direttamente il benchmark competitivo:

> **i top assumono presto e raggiungono già 4–6 worker intorno a 75 tile.**

Non trattare più la workforce come un sottosistema da attivare soltanto dopo l'espansione.

L'ipotesi da verificare è:

> **prima di comprare altro terreno, una farm con 50 tile deve essere abbastanza produttiva da finanziare il salto successivo.**

Se più workforce non aumenta active footprint e revenue, il prossimo trattamento dovrà concentrarsi sull'attivazione operativa/scheduling e NON su ulteriore hiring o nuove soglie cash.
