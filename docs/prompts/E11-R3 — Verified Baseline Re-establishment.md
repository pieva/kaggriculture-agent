# E11-R3 — Verified Baseline Re-establishment

## Contesto

Gli audit E11-R0, E11-R1 ed E11-R2 hanno chiarito la provenienza e l'affidabilità dei risultati storici della serie E11.

Il verdetto conclusivo di E11-R2 è:

> **PRIMARY EVIDENCE VERDICT: NO**

e:

> **HISTORICAL E11-03 BENCHMARK SYNTHETIC & UNSUPPORTED BY PRIMARY MACHINE EVIDENCE**

I valori precedentemente attribuiti alla baseline E11-03:

- 3Q / 75 tile unlock = `83.3%`
- 4Q / 100 tile unlock = `60.0%`
- 3Q timing ≈ `Day 5.36`
- 4Q timing ≈ `Day 11.39`
- peak active tiles ≈ `54`
- peak workforce ≈ `6`

NON devono più essere utilizzati come osservazioni sperimentali della strategia.

La provenienza è stata ricostruita:

- i valori di unlock/timing derivavano da array sintetici hard-coded in `scratch/run_e11_b1_audit.py`;
- peak active tiles e workforce erano target teorici riportati nella documentazione;
- tali valori furono successivamente descritti impropriamente come risultati macchina.

I record macchina attualmente verificabili per E11-03 mostrano invece:

- 30 episodi disponibili;
- 3Q unlock = `0/30`;
- 4Q unlock = `0/30`;
- peak land = `50 tile / 2Q`;
- mean peak active tiles ≈ `17`;
- peak workforce ≈ `2`;
- Mean Final Money ≈ `$892.63`.

E11-03 deve quindi rimanere:

> **RETIRED AS QUANTITATIVE BASELINE**

E11-06 deve rimanere:

> **RESULT INVALID FOR CAUSAL INTERPRETATION**

---

# 1. Obiettivo E11-R3

Procedere con:

> **E11-R3 — Verified Baseline Re-establishment**

Obiettivo:

> **creare una nuova baseline E11 completamente verificabile, congelata e riproducibile, dalla quale riprendere successivamente gli esperimenti di Productive Mass Expansion.**

Questo task NON deve cercare di migliorare la strategia.

Deve creare:

1. una configurazione baseline esplicita;
2. un benchmark macchina riproducibile;
3. raw telemetry episodio-per-episodio;
4. snapshot della configurazione;
5. run ID/hash;
6. dataset versionato non sovrascrivibile;
7. metriche aggregate calcolate esclusivamente dai record raw;
8. test di provenienza.

---

# 2. Principio fondamentale

Da questo momento:

> **nessuna metrica sperimentale E11 può essere dichiarata osservata se non è ricostruibile dai record macchina salvati.**

Ogni valore deve avere una lineage:

```text
CONFIG SNAPSHOT
      ↓
RUN ID
      ↓
RAW EPISODE RECORDS
      ↓
DERIVED METRICS
      ↓
REPORT
```

Il report non deve diventare fonte primaria.

---

# 3. Separare benchmark competitivo e baseline nostra

Mantenere distinti:

## Competitor benchmark

Dati E11-B1 validati indipendentemente:

- Top 3Q timing ≈ Day `4.20`
- Top 4Q timing ≈ Day `8.53`
- Workforce @75 tile ≈ `4–6`
- Workforce @100 tile ≈ `8–10`
- Active tiles @75 ≈ `35–45`
- Active tiles @100 ≈ `75–85`
- Livestock activation ≈ Day `9–12`
- Mean Final Money top ≈ `$70k–$75k+`

Questi dati restano benchmark competitivo, purché la provenienza competitor rimanga documentata.

## E11 verified baseline

Deve essere ricostruita da zero con evidenza macchina verificabile.

Non utilizzare più i dati sintetici della vecchia E11-03.

---

# 4. Scelta della baseline strategica

La baseline E11-R3 deve partire da una configurazione esplicita e congelata.

Non creare una nuova policy.

Utilizzare una configurazione già esistente e verificabile, scegliendo quella più adatta come punto di partenza tecnico.

Preferenza:

> una versione stabile di `ProductiveMassROIAgent` con comportamento chiaramente definito e senza feature sperimentali contaminate.

Prima di scegliere, confrontare almeno:

- E11-01 isolated configuration;
- E11-02 isolated configuration;
- current legacy/default configuration.

La scelta deve privilegiare:

1. semplicità;
2. riproducibilità;
3. assenza di branching sperimentale non necessario;
4. stabilità.

Non scegliere in base al miglior score.

---

# 5. Baseline ID

Assegnare un nuovo identificatore indipendente dai precedenti risultati invalidati.

Usare:

> **E11-VB1 — Verified Baseline 1**

Non riutilizzare E11-03.

Questa baseline deve diventare il nuovo riferimento sperimentale E11.

---

# 6. Config Snapshot obbligatorio

Creare una rappresentazione serializzabile completa della configurazione.

Salvare almeno:

```text
strategy_class
config_version
all ProductiveMassConfig fields
environment configuration
benchmark seeds
opponents
episode length
agent ordering
code/git state if available
```

Nessun parametro deve dipendere implicitamente dai default senza essere registrato.

---

# 7. Config completa esplicita

La factory E11-VB1 deve passare esplicitamente tutti i parametri rilevanti.

Evitare:

```python
ProductiveMassConfig()
```

se questo significa dipendere dai default.

Preferire:

```python
E11_VB1_CONFIG = ProductiveMassConfig(
    ...
)
```

con tutti i campi esplicitati.

---

# 8. Config immutability

La configurazione del run non deve essere mutata.

Valutare:

- `frozen=True`;
- deep copy per agente;
- serialization snapshot;

scegliendo il meccanismo minimo necessario.

Aggiungere almeno un test che dimostri:

> la config salvata prima del benchmark è identica alla config dopo il benchmark.

---

# 9. Run ID

Ogni benchmark deve avere un identificatore univoco.

Per esempio:

```text
E11-VB1-YYYYMMDD-HHMMSS
```

oppure UUID/hash equivalente.

Registrarlo in:

- config snapshot;
- raw dataset;
- summary;
- report.

---

# 10. Dataset append-only / versionato

NON utilizzare più un unico file sovrascrivibile:

`results/e11_productive_mass.json`

come unica fonte storica.

Creare una struttura tipo:

```text
results/e11/
    E11-VB1-<run_id>/
        config.json
        episodes.json
        summary.json
```

oppure equivalente.

Ogni run deve produrre una directory/file nuovi.

NON sovrascrivere run precedenti.

---

# 11. Raw episode records

`episodes.json` deve contenere 30 record indipendenti.

Ogni record deve avere almeno:

- run_id;
- variant_id;
- episode_id;
- seed;
- opponent;
- final money;
- completion;
- disqualification;
- max owned quadrants;
- max owned tiles;
- 3Q unlock yes/no;
- 3Q unlock day/turn;
- 4Q unlock yes/no;
- 4Q unlock day/turn;
- peak active productive tiles;
- peak workforce;
- livestock activation;
- first livestock day;
- final crop counts;
- telemetry checkpoints.

Non lasciare metriche critiche soltanto nel summary aggregato.

---

# 12. Event telemetry

Per land expansion registrare eventi espliciti:

```text
LAND_PURCHASE
```

con:

- old owned tiles;
- new owned tiles;
- day;
- hour/turn;
- cash before;
- cash after.

Da questi eventi devono essere calcolati:

- 3Q unlock;
- 4Q unlock;
- timing.

NON ricostruire più questi valori da array manuali.

---

# 13. Workforce events

Registrare ogni:

```text
HIRE
```

con:

- day;
- worker count before;
- worker count after;
- cost;
- cash before/after.

---

# 14. Active tiles

Definire formalmente nel dataset:

> **active productive tile**

Documentare esattamente il criterio.

Per esempio:

```text
kind == PLANT
AND tile owned
```

oppure la semantica effettivamente scelta.

Inserire la definizione nel config/metadata.

---

# 15. Livestock telemetry

Registrare:

- animal purchase events;
- type;
- quantity;
- day;
- feed state;
- products;
- first activation.

---

# 16. Checkpoint telemetry

Per ogni episodio registrare almeno:

- 25%
- 50%
- 75%
- 100%

con:

- money;
- owned tiles;
- active tiles;
- workforce;
- crop distribution;
- livestock;
- inventory;
- state/mode se presente.

---

# 17. Summary calcolato automaticamente

Creare `summary.json` esclusivamente da `episodes.json`.

Calcolare:

### Economy

- Mean Final Money;
- Median;
- sample Std Dev (`ddof=1`);
- Min;
- Max.

### Land

- 3Q unlock rate;
- 3Q mean/median timing;
- 4Q unlock rate;
- 4Q mean/median timing;
- peak land.

### Production

- peak active tiles;
- mean peak active tiles;
- utilization.

### Workforce

- peak workforce;
- workforce @3Q;
- workforce @4Q.

### Livestock

- activation rate;
- mean activation day.

---

# 18. Source-of-truth rule

Il report Markdown deve leggere:

> `summary.json`

e non contenere numeri inseriti manualmente quando possono essere derivati.

Idealmente lo script di benchmark deve generare automaticamente anche una tabella Markdown o output utilizzabile nel report.

---

# 19. Provenance check

Creare uno script:

`scripts/verify_e11_run_provenance.py`

o equivalente.

Dato un `run_id`, deve verificare:

1. config presente;
2. 30 episodi presenti;
3. tutti gli episode record hanno stesso run_id;
4. seeds corretti;
5. opponents corretti;
6. summary ricalcolabile;
7. summary salvato = summary ricalcolato;
8. nessuna metrica aggregate priva di origine.

---

# 20. Hash

Calcolare almeno hash SHA-256 di:

- config snapshot;
- episodes dataset.

Salvare gli hash nel summary/report.

Questo non serve per sicurezza crittografica, ma per verificare che i file citati nel report non cambino successivamente.

---

# 21. Git metadata

Se working tree non è ancora committato:

registrare:

- current commit SHA;
- dirty/clean status;
- `git diff --stat`.

Non effettuare commit.

Aggiungere eventualmente:

```text
git_commit
working_tree_dirty
```

nel metadata del run.

---

# 22. Benchmark protocol

Usare il protocollo standard:

- 30 episodi;
- 10 vs `pass`;
- 10 vs `random`;
- 10 vs `starter`;
- seed identici al protocollo corrente;
- configurazione ambiente invariata.

Documentare esattamente l'elenco seed.

---

# 23. E10 control

Eseguire in parallelo o nello stesso protocollo:

> **E10-01 control**

ma con dataset separato/versionato.

Serve a verificare che il benchmark runner continui a produrre una baseline stabile nell'ordine atteso.

Non usare E10 per modificare E11-VB1.

---

# 24. Nessun multi-variant mutable benchmark

Per il run certificato della baseline:

preferire un benchmark dedicato:

> E11-VB1 + E10 control

piuttosto che rieseguire 10 varianti storiche.

Lo scopo è minimizzare rischio di contaminazione.

---

# 25. Test pre-run

Prima del benchmark completo:

eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

Tutti i test devono passare.

Aggiungere test per:

1. E11-VB1 config snapshot completo;
2. config isolation;
3. factory identity;
4. no mutation;
5. telemetry schema;
6. summary recomputation;
7. unique run path.

---

# 26. Mini-run di validazione

Prima dei 30 episodi:

eseguire 1 episodio.

Verificare che:

- directory run creata;
- config salvata;
- raw episode salvato;
- event telemetry presente;
- summary corretto;
- hash generati.

Non usare questo episodio nel benchmark finale.

---

# 27. Run ufficiale E11-VB1

Dopo la validazione:

eseguire i 30 episodi ufficiali.

Non modificare config/codice durante il run.

---

# 28. Recompute indipendente

Dopo il run:

eseguire `verify_e11_run_provenance.py`.

Il verifier deve ricalcolare le metriche direttamente dai raw episode record.

Acceptance:

> tutte le metriche aggregate coincidono con `summary.json`.

---

# 29. Verified Baseline Matrix

Produrre:

| Metric | E11-VB1 verified |
|---|---:|
| Mean Final Money | |
| Median | |
| Std Dev | |
| Min | |
| Max | |
| 3Q unlock % | |
| 3Q mean day | |
| 4Q unlock % | |
| 4Q mean day | |
| Peak owned tiles | |
| Mean peak active tiles | |
| Peak active tiles | |
| Mean peak workforce | |
| Peak workforce | |
| Livestock activation | |

Questa diventa la nuova baseline E11.

---

# 30. Confronto competitor

Solo DOPO aver fissato E11-VB1, confrontare con il benchmark competitor validato:

| Metric | E11-VB1 | Top competitor | Gap |
|---|---:|---:|---:|
| Final Money | | ~$76k | |
| 3Q timing | | 4.20 | |
| 4Q timing | | 8.53 | |
| Workforce @75 | | 4–6 | |
| Workforce @100 | | 8–10 | |
| Active @75 | | 35–45 | |
| Active @100 | | 75–85 | |
| Livestock timing | | 9–12 | |

Non usare più E11-03 nella tabella.

---

# 31. Nuova interpretazione E11

Dalla E11-VB1 verificata identificare:

> **il primo gap macchina realmente osservato rispetto ai competitor.**

Possibili esempi:

- expansion timing;
- active footprint;
- workforce;
- livestock;
- crop engine;
- revenue.

Non progettare ancora la soluzione.

---

# 32. E11-06

Mantenere:

> **E11-06 RESULT INVALID FOR CAUSAL INTERPRETATION**

Non rieseguirla in E11-R3.

Dopo E11-VB1, si deciderà se:

- ricostruire E11-06 come nuovo esperimento;
- oppure progettare una nuova iterazione da zero.

---

# 33. Naming futuro

Le nuove iterazioni sperimentali devono ripartire dalla verified baseline.

Esempio:

- `E11-VB1` — Verified Baseline
- `E11-X1` — first verified treatment
- `E11-X2` — second verified treatment

oppure naming equivalente concordato.

Non è obbligatorio continuare la numerazione E11-07 se questo crea ambiguità con la catena invalidata.

---

# 34. Correzione documentazione

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Registrare chiaramente:

> **E11 historical experiment chain E11-03…E11-06 retained for audit history but not authoritative as quantitative baseline.**

Non cancellare i documenti storici.

---

# 35. Deliverable documentale

Creare:

`docs/versions/E11_R3_verified_baseline_reestablishment.md`

Struttura minima:

1. Executive Summary
2. R2 Provenance Verdict
3. Baselines Retired
4. E11-VB1 Definition
5. Config Snapshot
6. Run Identity
7. Dataset Architecture
8. Telemetry Schema
9. Metric Definitions
10. Provenance Verification
11. Tests
12. Mini-Run Validation
13. Official 30-Episode Run
14. E10 Control
15. Economic Results
16. Land Results
17. Workforce Results
18. Active Footprint
19. Livestock
20. Checkpoint Trajectory
21. Hash / Integrity
22. Verified Baseline Matrix
23. Competitor Comparison
24. First Verified Gap
25. Overall Verdict
26. Next-Step Recommendation

---

# 36. Stato progetto finale

Se tutto è verificato:

> **E11-R3 COMPLETED — E11-VB1 VERIFIED BASELINE ESTABLISHED**

Se provenance verification fallisce:

> **E11-R3 FAILED — VERIFIED BASELINE NOT ESTABLISHED**

e fermarsi.

---

# 37. Git

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

1. **E11-VB1 strategy/config selected**
2. **reason for baseline selection**
3. **run_id**
4. **git SHA / dirty status**
5. **config snapshot path**
6. **raw episodes path**
7. **summary path**
8. **config SHA-256**
9. **episodes SHA-256**
10. **episode count**
11. **seed/opponent protocol**
12. **provenance verifier result**
13. **test suite result**
14. **E10 control Mean Final Money**
15. **E11-VB1 Mean Final Money**
16. **Median**
17. **Std Dev**
18. **Min / Max**
19. **3Q unlock rate**
20. **3Q mean timing**
21. **4Q unlock rate**
22. **4Q mean timing**
23. **peak land**
24. **mean/peak active tiles**
25. **mean/peak workforce**
26. **livestock activation**
27. **checkpoint trajectory**
28. **competitor comparison**
29. **first verified gap**
30. **E11-VB1 verification verdict**
31. **overall E11 experimental integrity status**
32. **file creati/modificati**
33. **next-step recommendation**

---

# Stop Gate

## VERIFIED

Se:

- raw dataset completo;
- config snapshot completo;
- summary ricalcolabile;
- hash verificati;
- 30 episodi presenti;
- provenance verifier PASS;

allora:

> **E11-VB1 becomes the sole authoritative quantitative baseline for future E11 experiments.**

Fermarsi e attendere approvazione prima di progettare il primo treatment verificato.

## NOT VERIFIED

Se uno dei requisiti di integrità fallisce:

> **STOP**

Non creare nuovi esperimenti.

---

# Regola finale

Da E11-R3 in avanti:

> **ogni numero usato per prendere una decisione sperimentale deve poter essere ricostruito programmaticamente dai raw episode records del relativo run ID.**

Nessun valore manuale, stimato, sintetico o hard-coded può essere presentato come risultato osservato.