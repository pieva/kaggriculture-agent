# E11-X1.3 — E06 Productive Unit Replication & Scaling

## Mandato

Procedere con una nuova iterazione verificata E11 basata su un cambio di prospettiva:

> **E06 non è soltanto un benchmark storico: deve essere trattato come unità produttiva elementare da replicare e poi scalare.**

Non partire più da:

> comprare terreno → provare ad attivarlo

ma da:

> replicare una productive unit verificata → raddoppiarla → triplicarla → acquistare terreno solo quando serve ad ospitare ulteriore capacità produttiva.

L'ipotesi da verificare è che la precedente osservazione empirica del gap ~3× possa essere spiegata, almeno in parte, non da "3× terreno", ma dalla necessità di costruire circa:

> **3× E06-equivalent productive units**

---

# 1. Evidenza disponibile

## E06 sanity reference

Riferimento macchina già verificato:

- Strategy: `WaterFirstHIRENWClusterROIAgent`
- episodio diagnostico seed 0 vs `pass`
- Final Money: **$25,847**
- footprint: **9 tile compatte**
- workforce: **2 worker**
- land purchase: **nessuno**
- comportamento: compact / low movement / Water-First / fast ROI rotation

NON assumere che $25,847 sia la media E06 senza verificarlo nei dati storici disponibili.

Usarlo come:

> **verified seed-0 sanity reference**

Se esistono risultati macchina storici E06 affidabili e con provenance sufficiente, estrarre anche Mean/Median/Std senza rieseguire inutilmente benchmark lunghi.

---

# 2. E11-X1.2 verified treatment

Ultimo treatment verificato:

> **E11-X1.2 — E06 Productive Core Restoration + Corrected Multi-HIRE**

Stage C:

- 10 episodi;
- Mean Final Money: **$7,476.20**
- VB1 control nello stesso Stage C: **$2,192.20**
- delta: **+$5,284 / +241%**
- range X1.2: **$6,883 – $7,877**
- peak workforce: **3**
- peak active tiles: **17**
- owned land finale: **2Q / 50 tile**
- 3Q unlock: **0/10**
- provenance: **PASS**

Interpretazione:

> X1.2 ha corretto una regressione importante, ma NON ha ancora replicato il productive throughput E06.

---

# 3. Benchmark top

Mantenere come riferimento competitivo esterno verificato:

## 3Q / 75 tile

- Mean Day: **4.20**
- workforce: **4–6**
- active tiles: **35–45**

## 4Q / 100 tile

- Mean Day: **8.53**
- workforce: **8–10**
- active tiles: **75–85**

## Final Money

- circa **$70k–$75k+**

Il benchmark top NON deve guidare direttamente il BUILD X1.3.

Serve come ceiling competitivo.

---

# 4. Osservazione quantitativa da verificare

Il seed-0 E06 produce:

> **$25,847**

Tre volte questo valore:

> **$77,541**

che cade molto vicino al benchmark top di circa $75k.

Questa NON è una previsione.

Registrarla come:

> **H11-X1.3 exploratory scaling observation**

da verificare sperimentalmente.

Non assumere linearità.

---

# 5. Nuova unità concettuale

Definire:

> **E06 Productive Unit (EPU)**

Prima approssimazione:

```text
1 EPU =
9 compact productive tiles
+ E06-equivalent crop rotation
+ E06-equivalent Water-First behavior
+ sufficient daily workforce
+ low movement burden
+ preserved working capital
```

L'EPU NON deve essere definita solo come "9 tile".

È una combinazione di:

- footprint;
- scheduling;
- crop rotation;
- workforce;
- locality;
- capital discipline.

---

# 6. Obiettivo X1.3

Verificare una scaling ladder:

```text
1× EPU
  ↓
2× EPU
  ↓
3× EPU
```

corrispondente inizialmente a:

```text
9 productive tiles
18 productive tiles
27 productive tiles
```

Il land expansion deve essere subordinato alla necessità di ospitare la productive mass successiva.

---

# 7. Regola fondamentale

NON procedere direttamente a 18 o 27 tile.

Prima:

> **replicare E06 a 9 tile dentro ProductiveMassROIAgent**

Se la replica 9t fallisce:

> STOP.

Non ha senso scalare un'unità che non è stata replicata.

---

# 8. Struttura sperimentale X1.3

Separare X1.3 in tre sottofasi.

## X1.3-A — 1× EPU Replication

Target operativo:

> 9 tile compatte

Scopo:

> verificare che `ProductiveMassROIAgent` possa riprodurre il meccanismo economico E06.

## X1.3-B — 2× EPU Scaling

Solo se A è validata.

Target operativo:

> 18 tile produttive

Scopo:

> misurare scaling efficiency da 1× a 2×.

## X1.3-C — 3× EPU Scaling

Solo se B è validata.

Target operativo:

> 27 tile produttive

Scopo:

> misurare scaling efficiency da 2× a 3× e verificare se emerge una traiettoria compatibile con il benchmark competitivo.

---

# 9. X1.3-A — replica E06, non reinterpretazione

Prima del BUILD:

ispezionare direttamente il codice E06:

- `WaterFirstHIRENWClusterROIAgent`
- classi parent;
- tile selection;
- crop selection;
- seed purchasing;
- Water-First;
- harvest;
- plant;
- movement;
- HIRE;
- market sell;
- inventory handling.

Produrre una tabella:

| Mechanism | E06 exact behavior | X1.2 behavior | X1.3-A behavior |
|---|---|---|---|

NON dedurre il comportamento E06 dal nome della classe o dalla documentazione storica se il codice è disponibile.

---

# 10. Replica minima

X1.3-A deve riprodurre nel nuovo agente almeno:

- stesso footprint iniziale E06;
- stessa logica di selezione tile;
- stessa logica crop ROI;
- stessa semantica Water-First;
- stessa logica HIRE necessaria;
- stessa disciplina di seed purchase;
- stessa gestione movement;
- stessa vendita rilevante.

Evitare funzionalità E11 che alterino la replica durante A.

---

# 11. Isolamento X1.3-A

Durante X1.3-A disabilitare:

- land expansion;
- livestock;
- multi-quadrant locality;
- high-yield portfolio E11;
- Q2/Q3 triggers;
- qualsiasi comportamento che E06 non possiede e che possa alterare il confronto.

Obiettivo:

> **apples-to-apples E06 mechanism replication**

---

# 12. Workforce A

Non imporre 3 worker perché X1.2 li usa.

Usare il numero di worker richiesto dal meccanismo E06.

Se E06 lavora correttamente con:

> Farmer + 1 Hand

X1.3-A deve replicare quel comportamento.

La correzione Multi-HIRE resta disponibile nell'architettura, ma non deve essere usata senza workload.

---

# 13. Benchmark A

Protocollo:

## A0 — deterministic equivalence diagnostic

Eseguire:

- E06 seed 0 vs pass
- X1.3-A seed 0 vs pass

Confrontare:

- final money;
- daily money trajectory;
- crop mix;
- active tiles;
- workforce;
- MOVE;
- productive actions;
- seed purchases;
- market sales.

Se possibile, confrontare giorno per giorno.

---

# 14. Equivalence Gate A0

Classificare:

## EXACT / NEAR REPLICATION

se trajectory e final money sono molto vicini.

## MECHANISM REPLICATED, ECONOMIC DELTA

se scheduling e comportamento coincidono ma resta una differenza economica spiegabile.

## REPLICATION FAILED

se la trajectory diverge strutturalmente.

Non procedere a B in caso di `REPLICATION FAILED`.

---

# 15. A1 — reduced verification

Se A0 passa:

eseguire massimo **5 episodi** X1.3-A.

Non rieseguire 30 episodi E06.

Se esistono dati storici E06 verificabili, usarli.

Altrimenti il confronto causale primario resta seed-0 + comportamento macchina.

---

# 16. Gate economico X1.3-A

Non usare `$5k` come soglia sufficiente.

X1.3-A deve recuperare una quota sostanziale del throughput E06.

Usare:

### FAIL

`< 50%` del riferimento E06 comparabile

### PARTIAL REPLICATION

`50% – <80%`

### STRONG REPLICATION

`80% – <95%`

### NEAR EQUIVALENCE

`≥95%`

Calcolare rispetto allo stesso protocollo comparabile.

---

# 17. X1.3-B — 2× EPU

Solo dopo validazione A.

Target:

> **18 active productive tiles**

Non semplicemente 18 owned tiles.

Il footprint deve essere:

- compatto;
- organizzato in due cluster/unità logiche;
- gestibile dalla workforce;
- con movement controllato.

---

# 18. Replica spaziale B

Preferire:

> **2 × cluster E06-like**

rispetto a:

> un rettangolo arbitrario da 18 tile

se la geometria dell'environment lo consente.

Documentare esattamente la disposizione.

---

# 19. Workforce B

Partire dal workload.

Verificare empiricamente:

- 2 worker;
- 3 worker;
- eventualmente 4 worker;

senza assumere linearità.

Usare la correzione Multi-HIRE già verificata.

---

# 20. Scaling efficiency B

Definire:

```text
economic_scaling_B =
Revenue_or_FinalMoney_2x /
Revenue_or_FinalMoney_1x
```

e:

```text
efficiency_B =
economic_scaling_B / 2
```

Esempi:

- ratio 2.0× → 100% scaling efficiency;
- ratio 1.8× → 90%;
- ratio 1.5× → 75%.

---

# 21. Gate B

Classificare:

## STRONG SCALE

`efficiency_B >= 0.80`

## PARTIAL SCALE

`0.60 <= efficiency_B < 0.80`

## SCALING BOTTLENECK

`efficiency_B < 0.60`

Se scaling bottleneck:

> STOP prima di X1.3-C.

---

# 22. Diagnosi B

Se 18t non scalano:

attribuire il gap principalmente a una delle categorie:

- workforce;
- movement;
- watering;
- planting;
- harvest;
- seed capital;
- crop cycle;
- market;
- spatial layout.

Non correggere più categorie nello stesso run.

---

# 23. X1.3-C — 3× EPU

Solo se B raggiunge almeno:

> **PARTIAL SCALE**

Target:

> **27 active productive tiles**

Organizzati come:

> 3 EPU equivalenti

per quanto consentito dalla geometria.

---

# 24. Workforce C

Derivare dal workload.

Confrontare con il benchmark top:

- top @ 35–45 active tiles = 4–6 worker.

Non usare ancora questo range come target rigido.

Serve come sanity reference.

---

# 25. Scaling efficiency C

Definire:

```text
economic_scaling_C =
Revenue_or_FinalMoney_3x /
Revenue_or_FinalMoney_1x
```

```text
efficiency_C =
economic_scaling_C / 3
```

Classificazione:

## STRONG 3× SCALE

`efficiency_C >= 0.80`

## PARTIAL 3× SCALE

`0.60 <= efficiency_C < 0.80`

## NON-LINEAR BOTTLENECK

`efficiency_C < 0.60`

---

# 26. Land expansion come conseguenza

X1.3 non deve acquistare terreno perché:

- Day X;
- cash > magic threshold;
- competitor lo compra.

Deve acquistare terreno quando:

> **la prossima EPU non entra nel terreno disponibile**

e quando:

> **l'unità produttiva esistente genera sufficiente surplus per pagare il terreno senza distruggere il working capital.**

---

# 27. Trigger land derivato

Definire:

```text
required_cash_for_expansion =
land_cost
+ next_EPU_startup_capital
+ operating_reserve_existing_EPUs
```

Acquistare solo se:

```text
cash >= required_cash_for_expansion
```

NON introdurre `$2,100`, `$1,500`, `$1,300` o altra soglia come costante arbitraria se può essere derivata.

---

# 28. Next EPU startup capital

Calcolare da meccaniche reali:

- seed cost;
- daily hires;
- eventuali input necessari;
- operating buffer.

Documentare il calcolo.

---

# 29. Territorial mapping

Prima di B/C determinare:

- quante EPU entrano in Q0;
- quando serve Q1;
- quando serve Q2;
- quando serve Q3.

Non assumere che:

> 1 EPU = 1 quadrant.

Una EPU è 9 tile produttive, non 25 tile possedute.

---

# 30. Utilization

Registrare:

```text
productive_utilization =
active_productive_tiles / owned_tiles
```

e:

```text
EPU_density =
active_productive_tiles / 9
```

Obiettivo:

> evitare nuovamente 50/75/100 tile possedute ma inattive.

---

# 31. Benchmark ladder

Produrre:

| Level | Productive tiles | EPU | Workers | Money/Revenue | Scaling ratio | Efficiency |
|---|---:|---:|---:|---:|---:|---:|
| E06 reference | 9 | 1× | 2 | | 1.00 | 1.00 |
| X1.3-A | 9 | 1× | | | | |
| X1.3-B | 18 | 2× | | | | |
| X1.3-C | 27 | 3× | | | | |

---

# 32. Competitive extrapolation

Solo dopo C calcolare, come analisi:

```text
3 × E06 reference
```

e confrontarlo con:

> top ~$70–75k+

Etichettare chiaramente:

> **linear extrapolation / NOT observed result**

Non confonderlo con dati macchina.

---

# 33. Provenance

Ogni sottofase deve produrre dataset append-only.

Run IDs:

```text
E11-X1.3-A-<timestamp>
E11-X1.3-B-<timestamp>
E11-X1.3-C-<timestamp>
```

Directory:

```text
results/e11/<RUN_ID>/
```

contenente:

- `config.json`
- `episodes.json`
- `summary.json`

SHA-256 e verifier obbligatori.

---

# 34. Protocollo rapido

Per ciascuna fase:

## Smoke

1 episodio.

## Mini

5 episodi solo se smoke passa.

## Standard

10 episodi SOLO se necessario per confermare una fase promettente.

NON eseguire 30 episodi automaticamente.

---

# 35. Stop gates

## Stop A

Replica E06 fallita.

## Stop B

2× scaling efficiency <60%.

## Stop C

3× scaling efficiency <60%.

In ogni STOP:

> diagnosticare prima di modificare.

---

# 36. Confronti precedenti

Non rieseguire tutte le versioni E11.

Usare dataset append-only esistenti per:

- VB1;
- X1.2.

E06:

- usare evidenza storica verificabile;
- massimo diagnostic run mirato se indispensabile.

---

# 37. Telemetry

Per ogni EPU level registrare:

## Economy

- daily revenue;
- cumulative revenue;
- cash;
- seed expenditure;
- hire expenditure;
- land expenditure;
- productive surplus.

## Production

- active tiles;
- watered;
- planted;
- harvested;
- crop mix;
- crop loss.

## Workforce

- worker count;
- requested/accepted hires;
- productive actions / worker.

## Spatial

- MOVE actions;
- movement per productive action;
- cluster assignment.

## Land

- owned tiles;
- utilization;
- expansion event;
- cash before/after.

---

# 38. Daily trajectory

Produrre per A, B, C:

| Day | Money | Daily Revenue | Active | Workers | Revenue/Tile | Revenue/Worker | MOVE | Owned Land |
|---|---:|---:|---:|---:|---:|---:|---:|---:|

---

# 39. Unit economics

Calcolare:

```text
revenue_per_active_tile
revenue_per_worker
productive_actions_per_worker
movement_per_active_tile
capital_per_EPU
```

Queste metriche devono spiegare perché lo scaling è o non è lineare.

---

# 40. Test

Aggiungere test per:

1. X1.3-A fixed 9t footprint.
2. E06-equivalent tile selection.
3. E06-equivalent crop policy.
4. Water-First equivalence.
5. E06-equivalent worker demand.
6. land disabled in A.
7. B = 18 productive tile target.
8. C = 27 productive tile target.
9. Multi-HIRE workload-driven.
10. derived land expansion cash requirement.
11. no magic land threshold in X1.3.
12. working capital preservation.
13. EPU mapping.
14. provenance.
15. config immutability.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 41. Documentazione

Creare:

`docs/versions/E11_X1_3_e06_productive_unit_replication_scaling.md`

Struttura minima:

1. Executive Summary
2. Verified Evidence Base
3. E06 Reference
4. X1.2 Reference
5. TOP Benchmark
6. 3× Observation
7. EPU Definition
8. Experimental Ladder
9. E06 Code Audit
10. Mechanism Equivalence Matrix
11. X1.3-A Config
12. X1.3-A A0 Diagnostic
13. X1.3-A Reduced Benchmark
14. Replication Gate
15. X1.3-B Config
16. 2× Spatial Layout
17. Workforce B
18. B Results
19. Scaling Efficiency B
20. B Bottleneck
21. X1.3-C Config
22. 3× Spatial Layout
23. Workforce C
24. C Results
25. Scaling Efficiency C
26. C Bottleneck
27. Land Expansion Logic
28. Working Capital
29. Unit Economics
30. Daily Trajectories
31. EPU Ladder
32. E06 ↔ A ↔ B ↔ C ↔ TOP
33. Competitive Extrapolation
34. Provenance
35. Tests
36. Stop Gates
37. Final Verdict
38. Next Step

---

# 42. Project state

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Lo stato finale deve indicare esattamente l'ultima sottofase effettivamente completata.

Non dichiarare B/C completate se uno Stop Gate precedente le impedisce.

---

# 43. Git

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

1. X1.3 status
2. E06 evidence used
3. E06 exact mechanisms identified
4. EPU formal definition
5. A run_id
6. A provenance
7. A final money
8. A equivalence ratio vs E06
9. A replication verdict
10. B executed YES/NO
11. B run_id
12. B productive tiles
13. B workforce
14. B money/revenue
15. B scaling ratio
16. B scaling efficiency
17. B verdict
18. C executed YES/NO
19. C run_id
20. C productive tiles
21. C workforce
22. C money/revenue
23. C scaling ratio
24. C scaling efficiency
25. C verdict
26. owned land per level
27. utilization per level
28. movement per level
29. revenue/tile
30. revenue/worker
31. hire cost
32. seed cost
33. land cost
34. productive surplus
35. expansion events
36. derived land cash requirement
37. 3Q unlock if any
38. 3Q timing if any
39. competitor 3Q reference
40. 4Q status
41. E06 ↔ A ↔ B ↔ C ↔ TOP matrix
42. linear 3× extrapolation clearly labeled
43. dominant bottleneck
44. next verified experiment
45. files created/modified

---

# Regola finale

Non tentare di costruire una farm da 100 tile.

Tentare di costruire:

> **una E06 che funziona**

poi:

> **due E06-equivalent productive units che funzionano insieme**

poi:

> **tre E06-equivalent productive units che funzionano insieme.**

Solo a quel punto tornare alla domanda:

> **quanto terreno serve per continuare a replicare il motore produttivo?**

Il terreno è capacità.

La EPU è produzione.

L'obiettivo E11 è scalare la produzione, non il possesso del terreno.
