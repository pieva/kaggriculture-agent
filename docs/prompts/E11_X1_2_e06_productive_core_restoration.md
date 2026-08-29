# E11-X1.2 — BUILD + VERIFY — E06 Productive Core Restoration + Corrected Multi-HIRE

## Contesto

Gli audit e i treatment verificati della serie E11 hanno chiarito diversi punti fondamentali.

La baseline quantitativa autorevole resta:

> **E11-VB1 — Verified Baseline 1**

Run verificato:

`E11-VB1-20260827-084428`

Baseline macchina:

- Mean Final Money: **$429.00**
- 3Q / 75 tile unlock: **0 / 30**
- Peak land: **50 tile / 2Q**
- Mean / Peak active tiles: **16.93 / 17**
- Mean / Peak workforce: **2 / 2**
- Livestock: **OFF**
- Provenance verifier: **PASS**

E11-X1 e E11-X1.1 non hanno sbloccato 3Q.

L'audit E11-X1.1A ha però falsificato un'ipotesi importante:

> **NON esiste un hard-cap workforce dipendente dal numero di quadranti.**

L'environment Kaggriculture consente più `HIRE` nello stesso giorno se il capitale è sufficiente.

È stato inoltre verificato che gli Hands sono:

> **daily contractors**

e vengono azzerati a fine giornata.

La precedente implementazione E11 emetteva un solo `HIRE` al giorno, limitando artificialmente la workforce a:

> Farmer + 1 Hand

anche quando il workload avrebbe richiesto più worker.

---

# 1. Evidenza E06 da recuperare

L'audit ha ricostruito un riferimento interno molto importante:

> **E06 — WaterFirstHIRENWClusterROIAgent**

Un episodio diagnostico macchina verificato su seed 0 ha prodotto:

> **Final Money = $25,847**

con:

- footprint compatto;
- 9 tile gestite;
- 2 worker;
- nessun land purchase;
- movimento molto basso;
- rotazioni veloci;
- forte continuità produttiva.

Questo risultato dimostra che:

> **anche una superficie molto piccola può generare un ordine di grandezza economico enormemente superiore a E11-VB1 se il productive core è efficiente.**

---

# 2. Contrasto strutturale E06 vs E11-VB1

## E06

```text
compact footprint
+ low movement
+ fast crop turnover
+ preserved working capital
+ effective worker usage
→ ~$25k
```

## E11-VB1

```text
premature land purchase
+ 50 tiles owned
+ ~17 active
+ high movement
+ working capital drained
+ long-cycle / multi-crop pressure
→ $429
```

La strategia E11 ha quindi introdotto una regressione produttiva fondamentale:

> **ha aumentato la capacità territoriale prima di avere un revenue engine sufficientemente efficiente.**

---

# 3. Benchmark competitor esterno

Il benchmark top validato rimane:

## 3Q / 75 tile

- Mean Day: **4.20**
- Workforce: **4–6**
- Active tiles: **35–45**

## 4Q / 100 tile

- Mean Day: **8.53**
- Workforce: **8–10**
- Active tiles: **75–85**

## Livestock

- Day **9–12**

Il benchmark competitor deve essere usato come secondo livello.

Prima però E11 deve recuperare almeno la capacità produttiva interna già dimostrata da E06.

---

# 4. Obiettivo E11-X1.2

Procedere con:

> **E11-X1.2 — E06 Productive Core Restoration + Corrected Multi-HIRE**

Domanda sperimentale:

> **Se ProductiveMassROIAgent ripristina un core produttivo compatto, ad alta rotazione e con Multi-HIRE corretto prima di espandersi, riesce a generare sufficiente surplus da finanziare naturalmente il primo land unlock senza distruggere il working capital?**

La sequenza da testare è:

```text
COMPACT PRODUCTIVE CORE
        ↓
LIQUID REVENUE
        ↓
WORKFORCE WHEN NEEDED
        ↓
SURPLUS CAPITAL
        ↓
LAND EXPANSION
```

e NON:

```text
LAND FIRST
   ↓
HOPE FOR PRODUCTION
```

---

# 5. Principio metodologico

X1.2 non deve essere un generico tuning simultaneo.

È consentito modificare due elementi perché entrambi rappresentano:

> **restauro di capacità produttive già dimostrate o correzione di regressioni funzionali accertate**

1. **Productive core behavior ispirato a E06**
2. **Corrected Multi-HIRE issuance**

NON modificare ancora:

- livestock;
- Q3-specific logic;
- end-game;
- competitor timing thresholds;
- advanced crop diversification;
- worker locality multi-quadrant.

---

# 6. Controlled Change A — E06 Productive Core Restoration

Prima dell'espansione territoriale, ProductiveMassROIAgent deve mantenere un:

> **compact high-turnover productive core**

Non possedere più terreno del necessario finché il core non genera surplus.

Riutilizzare, dove possibile, meccanismi già presenti e verificati in E06:

- compact tile selection;
- short movement distances;
- Water-First behavior;
- harvest/plant continuity;
- fast ROI crop rotation;
- minimal idle productive capacity.

Non copiare ciecamente l'intero agente E06.

Estrarre e riutilizzare solo i meccanismi produttivi realmente responsabili del throughput.

---

# 7. Compact footprint

Prima del primo nuovo land purchase, limitare il footprint operativo a un cluster compatto.

Usare come riferimento iniziale:

> **9–16 tile compatte**

Non come target rigido finale.

La scelta deve privilegiare:

- distanza ridotta dallo shed;
- movement cost basso;
- workload gestibile;
- continuità Water/Harvest/Plant.

---

# 8. Non acquistare terreno al Day 1 per default

E11-VB1 acquista terreno troppo presto e immobilizza `$1,000`.

X1.2 NON deve eseguire land purchase semplicemente perché possibile.

Il nuovo trigger deve aspettare:

> **productive surplus**

---

# 9. Productive surplus

Definire un concetto semplice:

```text
productive_surplus =
cash
- operating capital required for current productive core
- near-term seed/hire obligations
```

Il land purchase deve diventare possibile quando:

> **productive_surplus >= land cost**

Non usare un magic number fisso `$1,500` se non strettamente necessario.

La soglia effettiva deve derivare da:

- land cost;
- operating reserve;
- next crop cycle cost;
- hire cost;
- current inventory.

---

# 10. Working capital preservation

Prima dell'espansione:

NON compromettere il working capital necessario a:

- semi;
- watering/production;
- hiring giornaliero;
- harvest continuity.

L'obiettivo è evitare:

```text
BUY_LAND
↓
cash starvation
↓
production collapse
```

---

# 11. Controlled Change B — Corrected Multi-HIRE

Correggere l'emissione degli HIRE.

L'environment consente:

> **multiple HIRE orders nello stesso giorno**

e gli Hands vengono resettati ogni giorno.

La logica deve quindi poter emettere:

```text
["HIRE", "HIRE", ...]
```

nello stesso market/action step quando necessario.

Non limitarsi a:

> un singolo `builder.hire()` per Day.

---

# 12. Workforce target non hard-coded

NON imporre subito:

- 3 worker;
- 4 worker;
- 6 worker;

come valori fissi.

Determinare il numero di Hands giornalieri in funzione di:

- active tiles;
- harvest backlog;
- watering backlog;
- planting backlog;
- movement burden;
- available cash;
- productive footprint.

---

# 13. E06 workforce sanity reference

E06 dimostra che:

> **2 worker possono essere sufficienti per 9 tile compatte**

Quindi X1.2 non deve aumentare worker solo perché può farlo.

Il benchmark top dimostra invece che:

> **4–6 worker sono normali intorno a 75 tile**

La workforce deve scalare insieme al workload.

---

# 14. Daily workforce

Poiché gli Hands sono giornalieri:

registrare per ogni day:

- requested hires;
- accepted hires;
- worker count;
- total hire cost;
- active tiles;
- workload.

Questa telemetry diventa obbligatoria.

---

# 15. Crop policy — restaurare il meccanismo E06

Non introdurre ancora un crop optimizer.

Riutilizzare il principio E06:

> **fast liquid rotation first**

Analizzare dal codice E06 quali crop erano effettivamente scelti e perché.

Se E06 usa principalmente:

- Carrot;
- Wheat;

preservare quel meccanismo nella fase pre-expansion.

Non assumere automaticamente che Tomato/Melon/Strawberry debbano entrare presto.

---

# 16. Water-First behavior

Verificare e ripristinare la semantica Water-First E06.

La priorità deve evitare:

- crop death;
- delayed growth;
- backlog che immobilizza capitale.

Documentare il delta rispetto a VB1.

---

# 17. Movement minimization

X1.2 deve ridurre il movimento rispetto a VB1.

Registrare:

- MOVE actions;
- average distance proxy;
- productive actions / worker;
- idle actions.

Target diagnostico:

> **movement burden significativamente inferiore a VB1**

---

# 18. Action hierarchy

Confrontare e, dove necessario, restaurare il productive ordering E06.

Non cambiare più del necessario.

Il core deve mantenere:

> WATER / HARVEST / PLANT continuity

prima di attività territoriali premature.

---

# 19. Primo gate X1.2 — Productive Core

Prima del 3Q unlock, verificare:

> **il productive core genera una trajectory economica chiaramente migliore di VB1**

Baseline VB1:

> `$429 final`

Sanity reference E06:

> `$25,847` seed 0 diagnostic

X1.2 non deve necessariamente raggiungere E06 subito.

Ma se rimane nella fascia:

> `$429–2k`

allora il productive core non è stato restaurato.

---

# 20. Secondo gate — 3Q unlock

Solo dopo aver dimostrato migliore produttività:

verificare se il surplus permette:

> **2Q / 50 → 3Q / 75**

Il 3Q unlock resta il primo gate territoriale.

---

# 21. Competitor timing

Top:

> **3Q Mean Day 4.20**

Non usare questo timing come target rigido X1.2.

Prima:

> produrre surplus.

Poi:

> confrontare il timing.

---

# 22. Nessun Q3 optimization

Se X1.2 raggiunge 3Q:

NON ottimizzare automaticamente Q3 nello stesso task.

Registrare l'evento e fermarsi secondo protocollo.

---

# 23. Protocollo rapido

Confermare:

> **1 → 5 → 10**

## Stage A

1 episodio smoke.

## Stage B

5 episodi.

## Stage C

10 episodi solo se Stage B mostra:

- revenue improvement significativo;
- active footprint efficiente;
- oppure 3Q unlock > 0.

NON eseguire automaticamente 30.

---

# 24. Confronti da eseguire

Benchmark causale:

- **E11-VB1**
- **E11-X1.2**

NON rieseguire E06 su 5/10/30 episodi.

Usare E06 come:

> **sanity benchmark interno verificato**

Un solo episodio diagnostico E06 già eseguito è sufficiente per questa iterazione.

---

# 25. Triple benchmark matrix

Nel report produrre:

| Metric | E06 sanity reference | E11-VB1 | E11-X1.2 | TOP |
|---|---:|---:|---:|---:|
| Final Money | $25,847 seed0 | $429 | | ~$70–75k+ |
| Active footprint | 9 compact | ~17 scattered | | 35–45 @3Q |
| Workforce | 2 | 2 | | 4–6 @3Q |
| 3Q timing | n/a | never | | Day 4.20 |
| Movement | low | high | | optimized |
| Revenue engine | fast rotation | stalled | | high throughput |

---

# 26. Provenance protocol

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

> `E11-X1.2-<timestamp>`

Dataset append-only:

```text
results/e11/<RUN_ID>/
    config.json
    episodes.json
    summary.json
```

---

# 27. Config delta

Produrre:

| Parameter / Behavior | VB1 | X1.2 |
|---|---|---|

Differenze ammesse:

- productive-core mode;
- compact footprint behavior;
- corrected Multi-HIRE issuance;
- land purchase trigger derived from productive surplus.

Non devono esistere altri cambiamenti non documentati.

---

# 28. Telemetry obbligatoria

Registrare:

## Economy

- cash;
- daily revenue;
- cumulative revenue;
- productive surplus;
- land capital gap.

## Workforce

- daily hires requested;
- daily hires accepted;
- worker count;
- cumulative hire cost.

## Production

- active tiles;
- harvested tiles;
- planted tiles;
- watered tiles;
- crop mix;
- crop losses if measurable.

## Movement

- MOVE actions;
- movement proxy;
- productive actions.

## Land

- land purchase events;
- cash before/after;
- 3Q unlock;
- timing.

---

# 29. Daily trajectory

Produrre almeno per Stage A e un episodio rappresentativo Stage B:

| Day | Money | Daily Revenue | Workers | Active Tiles | Crop Mix | MOVE | Productive Surplus | Land |
|---|---:|---:|---:|---:|---|---:|---:|---|

Questa tabella è centrale.

---

# 30. Test

Aggiungere test per:

1. VB1 invariata.
2. X1.2 config distinta.
3. multiple HIRE orders possono essere emessi nello stesso day.
4. daily Hands reset gestito correttamente.
5. workforce count deriva dal workload.
6. compact footprint attivo pre-expansion.
7. Water-First restored.
8. no premature land purchase.
9. land purchase possibile con productive surplus.
10. working capital preserved.
11. crop policy pre-expansion coerente con E06 mechanism.
12. provenance schema.
13. config immutability.

Eseguire:

`.venv\Scripts\pytest.exe tests/`

---

# 31. Stage A acceptance

Nel singolo episodio cercare almeno:

- Final Money nettamente > VB1;
- productive core attivo;
- movement ridotto;
- worker usage corretto;
- daily Multi-HIRE disponibile se richiesto.

Se Final Money resta ~$429:

> STOP e diagnosticare.

---

# 32. Stage B acceptance

Su 5 episodi:

## NOT VALIDATED

Se:

- Mean money resta molto basso;
- productive throughput non migliora;
- active tiles non vengono gestite efficacemente.

## PRODUCTIVE CORE PARTIAL

Se:

- revenue aumenta nettamente;
- productive core funziona;
- ma 3Q non è ancora raggiunto.

## PRODUCTIVE CORE VALIDATED

Se:

- forte aumento revenue;
- movimento controllato;
- working capital stabile;
- almeno alcuni episodi raggiungono 3Q.

---

# 33. Stage C

Eseguire 10 episodi solo se Stage B mostra:

> **PRODUCTIVE CORE PARTIAL o VALIDATED**

Non eseguire Stage C se la regressione E06 non è stata recuperata.

---

# 34. Internal Productivity Gate

Usare tre fasce diagnostiche, NON come target assoluti:

### Severe regression

`< $5k`

### Partial productivity restoration

`$5k – <$15k`

### Strong internal restoration

`≥ $15k`

E06 sanity reference:

> ~$25.8k seed0

Queste fasce servono solo a capire se X1.2 si muove nella giusta classe economica.

---

# 35. 3Q Gate

Se il productive core è forte ma 3Q resta 0/10:

> il nuovo bottleneck è il land surplus trigger.

Se 3Q compare:

> first verified territorial transition achieved.

---

# 36. Dominant bottleneck matrix

| Result | Diagnosis |
|---|---|
| Money <5k | productive-core restoration failed |
| Money improves, movement high | locality/scheduling issue |
| Money >15k, 3Q never | surplus/land trigger bottleneck |
| 3Q occurs, production collapses | post-expansion activation bottleneck |
| 3Q stable | proceed to next verified treatment |

---

# 37. Deliverable documentale

Creare:

`docs/versions/E11_X1_2_e06_productive_core_restoration.md`

Struttura minima:

1. Executive Summary
2. VB1 Verified Baseline
3. X1/X1.1 Findings
4. X1.1A Audit Findings
5. E06 Sanity Benchmark
6. TOP Benchmark
7. H11-X1.2
8. Controlled Changes
9. E06 Mechanisms Restored
10. Multi-HIRE Correction
11. Compact Footprint
12. Working Capital Preservation
13. Productive Surplus Land Trigger
14. Crop Rotation
15. Water-First
16. Movement
17. Config Delta
18. Tests
19. Provenance
20. Stage A
21. Stage B
22. Stage C
23. Daily Trajectory
24. Internal Productivity Gate
25. 3Q Unlock
26. E06 ↔ VB1 ↔ X1.2 ↔ TOP Matrix
27. Dominant Bottleneck
28. X1.2 Verdict
29. 30-Episode Recommendation
30. Next Step

---

# 38. Aggiornamento progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato:

> **E11-X1.2 BUILD + REDUCED LOCAL VERIFY COMPLETED — awaiting supervisor review**

---

# 39. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

NON effettuare:

- commit;
- tag;
- push;
- Kaggle submission.

---

# Deliverable finale obbligatorio

Riportare:

1. E11-X1.2 BUILD status
2. run_id
3. controlled changes
4. exact E06 mechanisms restored
5. Multi-HIRE correction
6. config delta
7. test suite
8. provenance verdict
9. Stage A result
10. Stage B result
11. Stage C executed YES/NO
12. Mean Final Money
13. Median / Std / Min / Max
14. daily revenue trajectory
15. cumulative revenue
16. productive surplus trajectory
17. land capital gap
18. daily workforce
19. peak workforce
20. daily hire costs
21. active footprint
22. active tiles / worker
23. crop portfolio
24. Water-First behavior
25. movement burden
26. productive actions / worker
27. 3Q unlock rate
28. 3Q timing
29. competitor 3Q timing reference
30. E06 sanity comparison
31. VB1 comparison
32. TOP comparison
33. internal productivity gate verdict
34. productive-core verdict
35. dominant bottleneck
36. X1.2 validation verdict
37. 30-episode validation recommended YES/NO
38. files created/modified
39. next-step recommendation

---

# Regola finale

E11-X1.2 non deve cercare ancora di raggiungere direttamente i $75k.

Il percorso corretto è:

> **prima recuperare la capacità produttiva interna già dimostrata da E06**

poi:

> **usare quel motore per finanziare l'espansione**

e infine:

> **scalare verso il benchmark competitivo dei top.**

Il benchmark E06 è il sanity floor interno.

Il benchmark top è il competitive ceiling esterno.

E11 deve prima smettere di essere peggiore di una strategia compatta già validata internamente.
