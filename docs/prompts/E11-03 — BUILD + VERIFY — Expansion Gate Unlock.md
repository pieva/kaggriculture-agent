# E11-03 — BUILD + VERIFY — Expansion Gate Unlock

## Contesto

Le iterazioni E11-01 ed E11-02 hanno chiarito progressivamente il collo di bottiglia che impedisce il dispiegamento della nuova architettura **Productive Mass Expansion**.

### E11-01

Risultato:

- Mean Final Money: circa `$23.8k`
- Land: 2 quadranti / 50 tile
- Peak workforce: 4 worker
- Livestock: OFF
- Q2/Q3: non acquistati

Diagnosi:

> **Expansion Cash Lock**

Il capitale generato veniva assorbito dalla produzione corrente prima di raggiungere la soglia necessaria per `BUY_LAND`.

### E11-02

È stata introdotta:

> **Expansion Capital Protection**

Risultato:

- Mean Final Money: `$15,682.50`
- Q2 Unlock Rate: `0%`
- Q3 Unlock Rate: `0%`
- Peak land: 50 tile
- Peak active tiles: 20
- Peak workforce: 4
- Livestock Activation Rate: `0%`

La protezione del capitale ha permesso alla cassa di raggiungere la disponibilità richiesta per l'acquisto del terreno, ma Q2 non è stato acquistato.

Il nuovo collo di bottiglia dominante è:

> **Active Tile Gate Lock / Seed Starvation Deadlock**

La condizione:

`active_tiles >= 15`

rimaneva sistematicamente non soddisfatta mentre la protezione capitale limitava la produzione a rotazioni Carrot/Wheat.

Il risultato è stato:

```text
Expansion Capital Protection
        ↓
high-value seeds blocked
        ↓
active_tiles oscillate around 12–14
        ↓
Q2 readiness condition never satisfied
        ↓
BUY_LAND never executes
        ↓
productive mass remains locked
```

---

# 1. Obiettivo E11-03

Procedere con:

> **E11-03 — Expansion Gate Unlock**

La domanda sperimentale è:

> **Se manteniamo invariata la Expansion Capital Protection di E11-02 ma rimuoviamo il gate assoluto che impedisce l'espansione territoriale, il capitale protetto riesce finalmente a trasformarsi in nuova massa produttiva?**

Questa iterazione deve modificare **una sola componente dominante**:

> **Land Expansion Readiness Gate**

Non modificare contemporaneamente crop spending, workforce, livestock, scheduling o altri sottosistemi.

---

# 2. Principio sperimentale

E11-03 deve essere un esperimento controllato.

Conservare E11-02 come baseline riproducibile.

La differenza tra E11-02 ed E11-03 deve essere limitata, per quanto possibile, a:

> **criterio di readiness per `BUY_LAND` Q2/Q3**

Non introdurre in questa iterazione:

- nuovo crop mix;
- nuova soglia per Melon/Strawberry;
- nuovo reinvestment threshold;
- nuovo operating reserve;
- nuovo hiring model;
- nuovo livestock count;
- nuova locality;
- nuova action hierarchy;
- nuovo end-game model.

---

# 3. Ipotesi E11-03

Formalizzare:

> **H11-03 — Expansion Gate Hypothesis:** il principale blocco residuo di E11-02 non è più la disponibilità di capitale, ma una condizione di productive readiness troppo restrittiva rispetto alla logica di compounding necessaria per Productive Mass Expansion.

La condizione `active_tiles >= 15` potrebbe essere concettualmente sbagliata perché richiede un livello di saturazione locale elevato **prima** di consentire l'aumento della capacità territoriale.

L'ipotesi alternativa è:

> la strategia deve poter espandere quando dispone di capitale sufficiente, capacità operativa minima e orizzonte temporale sufficiente, senza attendere la saturazione quasi completa del terreno corrente.

---

# 4. Non utilizzare un nuovo magic number arbitrario

Non sostituire semplicemente:

`active_tiles >= 15`

con:

`active_tiles >= 10`

senza una motivazione architetturale.

La precedente proposta:

`active_tiles >= (owned_quadrants - 1) * 10`

non deve essere adottata automaticamente.

Preferire un criterio interpretabile e riutilizzabile.

---

# 5. Nuovo modello di Expansion Readiness

Progettare il nuovo gate usando tre componenti:

## 5.1 Capital Readiness

Il capitale necessario al prossimo quadrante è disponibile rispettando il buffer operativo.

E11-02 ha già introdotto la protezione.

Mantenere tale logica.

Concettualmente:

```text
cash >= land_cost + expansion_operating_buffer
```

con i parametri E11-02 invariati, salvo necessità tecnica documentata.

---

## 5.2 Minimum Operational Readiness

La farm deve avere una capacità produttiva minima sufficiente a evitare espansioni completamente premature.

Questa condizione deve essere volutamente **più debole** della precedente saturazione `active_tiles >= 15`.

Può utilizzare, a seconda dell'architettura effettiva:

- numero minimo di active productive tiles;
- numero minimo di worker;
- presenza di un ciclo produttivo funzionante;
- combinazione semplice di questi fattori.

Il gate non deve pretendere che il quadrante corrente sia quasi saturo.

Lo scopo è soltanto impedire situazioni assurde come:

> acquistare nuovo terreno quando la farm corrente non è ancora realmente operativa.

---

## 5.3 Remaining Horizon

Non acquistare terreno troppo tardi se non esiste tempo sufficiente per:

- prepararlo;
- seminarlo;
- produrre;
- raccogliere;
- monetizzare.

Utilizzare il concetto già presente di:

> **remaining productive horizon**

Non introdurre un nuovo tuning end-game.

Riutilizzare la logica esistente.

---

# 6. Preferenza per readiness relativa

Se compatibile con l'architettura, valutare una metrica relativa del tipo:

```text
productive_utilization = active_tiles / usable_owned_tiles
```

e un:

```text
expansion_utilization_threshold
```

configurabile.

Tuttavia non introdurre questo rapporto solo per eleganza.

Se una condizione più semplice è più coerente con lo stato disponibile nell'ambiente, preferire la soluzione più robusta.

L'obiettivo è:

> **rimuovere il deadlock senza introdurre nuova complessità non necessaria.**

---

# 7. Regola di espansione desiderata

Il comportamento concettuale deve essere:

```text
IF
    next_quadrant_available
AND capital_ready
AND minimum_operational_readiness
AND sufficient_remaining_horizon
THEN
    BUY_LAND
```

Non richiedere saturazione quasi completa del quadrante corrente.

Le azioni produttive veramente urgenti continuano ad avere priorità secondo la gerarchia E11 esistente.

---

# 8. Q2 e Q3

Applicare la nuova logica sia a Q2 sia a Q3.

Non correggere soltanto Q2 creando poi lo stesso deadlock su Q3.

Registrare separatamente:

- readiness Q2;
- purchase Q2;
- readiness Q3;
- purchase Q3.

La logica può usare gli stessi principi con parametri differenti solo se realmente necessario.

Preferire una regola generale.

---

# 9. Preservare Expansion Capital Protection

La protezione introdotta in E11-02 deve rimanere attiva.

Non modificare in E11-03 la policy che blocca:

- seed discrezionali ad alto costo;
- hiring opzionale;
- livestock;

quando tali spese consumerebbero il capitale protetto per il prossimo quadrante.

Questo è essenziale per l'attribuzione causale.

Non consentire in questa iterazione Melon/Strawberry semplicemente sopra una nuova soglia come `$600`.

Un cambiamento di questo tipo costituirebbe un secondo esperimento.

---

# 10. Preservare crop policy E11-02

Il crop portfolio e la spending policy devono rimanere invariati.

Quindi:

- nessuna nuova ottimizzazione Carrot/Wheat;
- nessuna nuova quota Melon;
- nessuna nuova quota Strawberry;
- nessuna nuova rotazione Tomato;
- nessuna nuova allocazione high-value.

L'obiettivo E11-03 NON è aumentare subito il money tramite crop tuning.

È verificare:

> **se il capitale protetto può finalmente essere convertito in land.**

---

# 11. Preservare workforce logic

Non modificare:

- target worker ratio;
- max workers;
- locality;
- hiring safeguards;

salvo adattamenti tecnici strettamente necessari all'acquisto di Q2/Q3.

La workforce deve rimanere downstream:

```text
land expansion
    ↓
more usable capacity
    ↓
workforce scaling
```

Se dopo Q2/Q3 la workforce non scala, quello diventerà il nuovo bottleneck.

Non correggerlo nello stesso esperimento.

---

# 12. Preservare livestock logic

Non modificare:

- target Cow;
- target Sheep;
- livestock activation condition;
- feed logic;
- livestock spending rules.

Se Q2/Q3 vengono acquistati ma livestock rimane OFF, questo deve emergere come nuovo risultato diagnostico.

Non anticipare artificialmente gli animali.

---

# 13. Configurazione E11-03

Creare una configurazione riproducibile distinta da:

- E11-01
- E11-02

Per esempio:

`E11_03_CONFIG`

oppure equivalente coerente con il repository.

Introdurre il minor numero possibile di nuovi parametri, ad esempio:

```text
expansion_readiness_mode
expansion_min_operational_tiles
expansion_utilization_threshold
```

Solo quelli effettivamente necessari.

Non introdurre parametri ridondanti.

---

# 14. Test specifici

Estendere la suite E11.

Testare almeno:

1. E11-02 rimane riproducibile con il vecchio gate.
2. E11-03 non richiede più `active_tiles >= 15` rigidamente.
3. `BUY_LAND Q2` avviene con capital readiness + minimum operational readiness.
4. `BUY_LAND Q3` utilizza la stessa logica generale.
5. espansione bloccata se operating capital insufficiente.
6. espansione bloccata se farm non minimamente operativa.
7. espansione bloccata se remaining horizon insufficiente.
8. Expansion Capital Protection rimane attiva.
9. seed spending E11-02 rimane invariato.
10. hiring policy rimane invariata.
11. livestock policy rimane invariata.
12. action legality.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

Tutti i test devono passare.

---

# 15. Benchmark locale

Eseguire il benchmark paired standard da 30 episodi sugli stessi seed.

Confrontare almeno:

- E10-01
- E11-01
- E11-02
- E11-03

Non cambiare protocollo sperimentale.

Metriche economiche:

- Mean Final Money
- Median
- Sample Std Dev (`ddof=1`)
- Min
- Max
- Completion Rate
- Disqualification Rate
- breakdown per opponent
- paired wins vs E10-01
- paired wins vs E11-01
- paired wins vs E11-02
- delta assoluto
- delta percentuale
- ratio

---

# 16. Metriche prioritarie E11-03

In questa iterazione le metriche architetturali hanno priorità diagnostica.

Registrare:

## Land

- Q2 unlock rate
- Q2 mean unlock day
- Q3 unlock rate
- Q3 mean unlock day
- peak quadrants
- peak owned tiles

## Utilization

- peak active productive tiles
- mean active productive tiles ai checkpoint
- idle owned tiles

## Workforce

- peak workers
- workforce ai checkpoint
- first expansion hire timing

## Livestock

- activation rate
- Cow count
- Sheep count
- first livestock timing

## Economy

- cash before Q2
- cash after Q2
- cash before Q3
- cash after Q3

---

# 17. Checkpoint trajectory

Confrontare ai checkpoint:

- 25%
- 50%
- 75%
- 100%

almeno:

| Metric | E10-01 | E11-01 | E11-02 | E11-03 |
|---|---:|---:|---:|---:|
| Money | | | | |
| Quadrants | | | | |
| Active tiles | | | | |
| Workforce | | | | |
| Livestock | | | | |

La domanda centrale è:

> **La rimozione del gate permette al capitale protetto di trasformarsi in nuova capacità?**

---

# 18. Architecture Deployment Verdict

Classificare E11-03 secondo questa scala.

## ARCHITECTURE NOT DEPLOYED

Se Q2 continua a non essere acquistato stabilmente.

Interpretazione:

> il nuovo expansion gate è ancora insufficiente o esiste un altro blocco precedente all'espansione.

---

## PARTIAL LAND DEPLOYMENT

Se Q2 viene acquistato stabilmente ma Q3 no.

Interpretazione:

> primo salto territoriale riuscito; diagnosticare il blocco Q3.

---

## FULL LAND DEPLOYMENT

Se Q2 e Q3 vengono acquistati stabilmente e vengono raggiunti:

> **4 quadranti / 100 tile owned**

ma workforce/livestock non scalano ancora.

Interpretazione:

> land bottleneck risolto; nuovo collo di bottiglia downstream.

---

## PARTIAL MASS DEPLOYMENT

Se:

- 4 quadranti raggiunti;
- active productive footprint cresce significativamente;
- workforce cresce;

ma livestock o altri elementi rimangono bloccati.

---

## FULL MASS DEPLOYMENT

Considerare l'architettura di massa realmente dispiegata quando la maggioranza delle run raggiunge indicativamente:

- 4 quadranti / 100 tile;
- significativa crescita active footprint;
- almeno circa 8 worker, salvo evidenza empirica che una workforce inferiore sia sufficiente;
- livestock attivato.

Solo questo stato costituisce il primo test economico pieno dell'ipotesi E11.

---

# 19. Interpretazione economica

La classificazione economica rimane:

| Mean Final Money | Verdict |
|---:|---|
| `< $50,000` | `FAIL` |
| `$50,000 – <$60,000` | `MINIMUM SUCCESS` |
| `$60,000 – <$70,000` | `COMPETITIVE` |
| `$70,000 – <$75,000` | `NEAR TOP BENCHMARK` |
| `≥ $75,000` | `TARGET ACHIEVED` |
| `> $75,000` | `BENCHMARK EXCEEDED` |

Ma riportare sempre il risultato combinato:

> **Architecture Verdict + Economic Verdict**

Esempi:

`FULL LAND DEPLOYMENT + FAIL`

oppure:

`FULL MASS DEPLOYMENT + MINIMUM SUCCESS`

---

# 20. Matrice diagnostica E11-03

Utilizzare questa interpretazione:

| Stato osservato | Diagnosi |
|---|---|
| Q2 non acquistato | Expansion Gate ancora bloccante |
| Q2 sì, Q3 no | Second Expansion Bottleneck |
| Q2+Q3, workforce ≤4 | Workforce Scaling Bottleneck |
| 4Q + workforce scaling, active tiles basse | Productive Activation Bottleneck |
| 4Q + ≥8 worker, livestock OFF | Livestock Activation Bottleneck |
| 4Q + ≥8 worker + livestock ON | **FULL MASS DEPLOYMENT** |
| Full Mass + `<$50k` | Efficienza/output nuovo bottleneck |
| Full Mass + `≥$50k` | E11 architecture direction validated |
| Full Mass + `≥$75k` | Competitive target achieved |

---

# 21. Dominant Bottleneck

Al termine identificare un solo nuovo:

> **dominant bottleneck**

Non procedere a correggerlo nello stesso task.

Possibili esiti:

- expansion gate still locked;
- Q3 capital recovery;
- workforce scaling;
- active-tile activation;
- seed starvation after expansion;
- travel dilution;
- livestock activation;
- feed supply;
- capital allocation;
- end-game conversion.

---

# 22. Non perseguire il risultato economico a ogni costo

E11-03 può produrre un Mean Final Money inferiore a E11-01/E10 pur essendo sperimentalmente utile.

Per esempio:

> Q2/Q3 vengono finalmente acquistati, ma il nuovo terreno resta inattivo.

In questo caso:

- economic verdict = FAIL;
- architectural result = progresso sostanziale;
- nuovo bottleneck = productive activation.

Non annullare l'espansione soltanto perché la prima run a 100 tile non è immediatamente redditizia.

---

# 23. Deliverable documentale

Creare:

`docs/versions/E11_03_expansion_gate_unlock.md`

Struttura minima:

1. Executive Summary
2. E11-02 Diagnosis
3. H11-03 Expansion Gate Hypothesis
4. Controlled Change
5. Old Readiness Logic
6. New Readiness Logic
7. Configuration Delta
8. Invariants Preserved
9. Tests
10. Benchmark Protocol
11. Economic Results
12. Q2 Unlock Analysis
13. Q3 Unlock Analysis
14. Land Deployment
15. Active Footprint
16. Workforce Scaling
17. Livestock Activation
18. 25/50/75/100 Trajectory
19. Architecture Deployment Verdict
20. Economic Verdict
21. Dominant Bottleneck
22. Recommendation for E11-04

---

# 24. Aggiornare stato progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Registrare:

> **E11-03 BUILD + LOCAL VERIFY COMPLETED — awaiting supervisor review**

Non dichiarare E11 completato.

---

# 25. Git

Al termine eseguire:

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

1. **E11-03 BUILD status**
2. **readiness logic precedente**
3. **nuova readiness logic**
4. **invarianti E11-02 preservate**
5. **test result**
6. **Mean Final Money**
7. **Median / Std / Min / Max**
8. **delta vs E10-01**
9. **delta vs E11-01**
10. **delta vs E11-02**
11. **paired wins**
12. **Q2 unlock rate**
13. **Q2 mean unlock timing**
14. **Q3 unlock rate**
15. **Q3 mean unlock timing**
16. **peak quadrants / owned tiles**
17. **peak active productive tiles**
18. **peak workforce**
19. **livestock activation rate**
20. **trajectory 25/50/75/100**
21. **Architecture Deployment Verdict**
22. **Economic Decision Gate**
23. **dominant bottleneck**
24. **file creati/modificati**
25. **proposta E11-04**

## Regola finale

Se Q2 non viene ancora acquistato stabilmente:

> **non passare a crop/workforce/livestock tuning. Continuare a diagnosticare il land expansion gate.**

Se Q2 viene acquistato ma Q3 no:

> **diagnosticare esclusivamente il secondo salto territoriale.**

Se vengono raggiunti 4 quadranti ma workforce o active tiles non scalano:

> **considerare risolto il land bottleneck e intervenire successivamente sul primo sottosistema downstream bloccante.**

Se viene raggiunto **FULL MASS DEPLOYMENT**:

> **per la prima volta valutare seriamente il risultato economico rispetto a $50k/$75k e usare il nuovo bottleneck per guidare E11-04.**

**Non modificare la crop spending policy in E11-03. Fermarsi dopo BUILD + LOCAL VERIFY e attendere approvazione.**