# E11-R2 — Historical Benchmark Provenance Audit

## Contesto

Gli audit **E11-R0** ed **E11-R1** hanno stabilito due fatti distinti.

### E11-R0

È stata identificata e corretta una contaminazione reale delle configurazioni E11:

- default config modificati dalle iterazioni successive;
- factory benchmark non sufficientemente isolate;
- varianti storiche che potevano ereditare semantica/configurazioni successive.

Risultato:

> **configuration isolation restored**

ma:

> **historical behavioral reproducibility NOT restored**

### E11-R1

È stata tentata la ricostruzione comportamentale della baseline storica E11-03.

Il fingerprint storico documentato era:

- 3Q / 75 tiles unlock: **83.3% (25/30)**
- Mean 3Q timing: **~Day 5.4**
- 4Q / 100 tiles unlock: **60.0% (18/30)**
- Mean 4Q timing: **~Day 11.2–11.4**
- Peak land: **100 tiles**
- Peak active productive tiles: **~54**
- Peak workforce: **~6**
- Mean Final Money: **~$7,193.77**

La ricostruzione isolata ha invece prodotto:

- 3Q unlock: **0%**
- 4Q unlock: **0%**
- Peak land: **50 tiles**
- Peak active tiles: **17**
- Peak workforce: **2**

Verdetto:

> **E11-03 NOT REPRODUCED**

---

# 1. Problema metodologico emerso da R1

R1 ha inoltre stabilito che, per quanto ricostruibile:

- `active_tiles` semantics = `IDENTICAL`
- land readiness = `IDENTICAL`
- capital protection = `IDENTICAL`
- essential seed behavior = `IDENTICAL`
- workforce policy = `IDENTICAL`

ma ha contemporaneamente attribuito la mancata riproduzione a:

> **Expansion Capital Protection Deadlock & Essential Seed Over-buying**

Queste due conclusioni non possono essere considerate sufficienti insieme.

Se la E11-03 storica utilizzava realmente gli stessi meccanismi e raggiungeva:

- 3Q nel 83.3%;
- 4Q nel 60%;

mentre l’attuale ricostruzione raggiunge:

- 3Q nello 0%;
- 4Q nello 0%;

deve esistere:

1. almeno una differenza storica non ancora individuata;

oppure:

2. un problema nella provenienza o interpretazione del benchmark storico.

---

# 2. Vincolo sul “minimal historical fix” di R1

R1 ha proposto come possibile correzione:

> proteggere il float `$1,100` dagli acquisti essential seed quando cash ≥ `$950`.

NON implementare questa modifica in E11-R2.

Se la documentazione storica indica che Carrot/Wheat erano acquistabili fino alla operating reserve di `$300`, la soglia `$950` rappresenterebbe:

> **una nuova policy**

e non:

> **una ricostruzione storica dimostrata**.

Quindi nessun tuning strategico è consentito.

---

# 3. Obiettivo E11-R2

Eseguire:

> **E11-R2 — Historical Benchmark Provenance Audit**

Domanda principale:

> **Da quali episodi reali, configurazioni, record e campi telemetrici derivano i valori storici attribuiti a E11-03: 25/30 episodi a 3Q e 18/30 episodi a 4Q?**

L’obiettivo NON è riprodurre quei numeri.

L’obiettivo è prima stabilire:

> **se quei numeri rappresentano realmente esecuzioni osservate della E11-03 che pensavamo di benchmarkare.**

---

# 4. Possibili esiti dell’audit

E11-R2 deve discriminare tra almeno quattro ipotesi.

## H-R2-A — Genuine Historical Execution

I record storici mostrano realmente:

- 25 episodi E11-03 con 3Q;
- 18 episodi E11-03 con 4Q;

e sono associabili alla corretta configurazione.

In questo caso:

> **il benchmark storico è valido**

e bisognerà successivamente ricostruire la differenza semantica mancante.

---

## H-R2-B — Variant Misattribution

I record esistono, ma appartengono:

- a un’altra variante;
- a una configurazione diversa;
- a un run sperimentale non corrispondente alla E11-03 documentata.

In questo caso:

> **historical benchmark mislabeled**

---

## H-R2-C — Telemetry Interpretation Error

Gli episodi sono E11-03, ma:

- Q2/Q3;
- quadrants;
- owned tiles;
- unlock event;

sono stati interpretati erroneamente.

In questo caso:

> **historical telemetry interpretation invalid**

---

## H-R2-D — Synthetic / Reconstructed Benchmark Evidence

I valori 83.3% / 60% non derivano da record episodio-per-episodio verificabili, ma da:

- dati ricostruiti;
- dati sintetici;
- assunzioni;
- report intermedi;
- trasformazioni non tracciabili.

In questo caso:

> **historical E11-03 benchmark unsupported by primary evidence**

e non deve più essere utilizzato come baseline sperimentale.

---

# 5. Regola fondamentale di provenienza

Applicare una gerarchia esplicita delle evidenze.

## Livello P0 — Primary execution evidence

Massima affidabilità:

- raw episode records;
- environment telemetry;
- event logs;
- per-step traces;
- benchmark output salvato direttamente dall’esecuzione.

## Livello P1 — Derived machine evidence

- JSON aggregato derivato dai record P0;
- script che calcola metriche da P0;
- CSV derivato.

## Livello P2 — Human/agent report

- Markdown E11-03;
- EXPERIMENT_LOG;
- PROJECT_STATE;
- NEW_SESSION.

## Livello P3 — Narrative reconstruction

- commenti;
- inferenze;
- valori ricostruiti successivamente;
- script che incorporano numeri hard-coded.

Un dato P2/P3 non deve essere trattato come prova primaria se manca P0/P1.

---

# 6. Fonti da ispezionare

Ispezionare integralmente:

- `results/e11_productive_mass.json`
- `scripts/benchmark_e11_performance.py`
- `scratch/analyze_e11_3_timing.py`
- `scratch/run_e11_b1_audit.py`
- `scratch/analyze_e11_results.py`
- `scratch/inspect_e11_3_json.py`
- eventuali altri script `scratch/` relativi a E11-03/B1

e:

- `docs/versions/E11_03_expansion_gate_unlock.md`
- `docs/versions/E11_B1_competitor_expansion_timing_audit.md`
- `docs/versions/E11_R0_baseline_reproducibility_audit.md`
- `docs/versions/E11_R1_e11_03_historical_behavioral_reconstruction.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

---

# 7. Non fidarsi dei nomi dei file

Il fatto che un file si chiami:

```text
e11_productive_mass.json
```

non dimostra che contenga raw telemetry originale.

Per ogni file stabilire:

- quando è stato creato;
- da quale script;
- se è stato sovrascritto;
- se contiene raw episode data;
- se contiene aggregati;
- se contiene dati hard-coded;
- se contiene risultati di run differenti.

---

# 8. Audit di `results/e11_productive_mass.json`

Documentare la struttura completa.

Identificare:

- top-level keys;
- variant names;
- episode records;
- seeds;
- opponent;
- final money;
- quadrant events;
- active tiles;
- workforce;
- timestamps/day;
- configuration snapshot.

Rispondere esplicitamente:

> **Esistono 30 record episodio-per-episodio identificabili come E11-03?**

Se NO:

> dichiararlo.

---

# 9. Ricostruzione dei 25/30

Individuare esattamente i record che avrebbero prodotto:

> **3Q unlock = 25/30**

Produrre una tabella:

| Episode | Seed | Opponent | Variant Label | 3Q? | 3Q Day | Source Record |
|---:|---:|---|---|---|---:|---|

Devono esserci esattamente 30 righe se il dato storico è realmente derivato da 30 episodi.

Contare programmaticamente:

```text
3Q = 25
non-3Q = 5
```

Non utilizzare il valore scritto nel report.

Ricalcolarlo dai record.

---

# 10. Ricostruzione dei 18/30

Analogamente produrre:

| Episode | Seed | Opponent | Variant Label | 4Q? | 4Q Day | Source Record |
|---:|---:|---|---|---|---:|---|

Ricalcolare:

```text
4Q = 18
non-4Q = 12
```

Se non è possibile:

> il dato storico non è supportato da primary evidence disponibile.

---

# 11. Timing Audit

Dagli stessi record ricalcolare:

- mean 3Q day;
- median 3Q day;
- std dev;
- min;
- max;

e:

- mean 4Q day;
- median 4Q day;
- std dev;
- min;
- max.

Confrontare con:

- Day ~5.4;
- Day ~11.2–11.4.

---

# 12. Peak Metrics Audit

Dagli stessi episodi ricalcolare:

- peak owned land;
- peak quadrants;
- peak active tiles;
- peak workforce;
- livestock activation.

Verificare se emergono davvero:

- 100 tiles;
- ~54 active;
- ~6 workers;
- livestock 0%.

---

# 13. Economic Consistency Audit

Per gli stessi 30 episodi ricalcolare:

- Mean Final Money;
- Median;
- Std Dev;
- Min;
- Max.

Verificare se il dataset che produce 25/30 e 18/30 produce anche:

> Mean Final Money ~$7,193.77

Se land metrics e money provengono da dataset differenti:

> evidenziare la contaminazione.

---

# 14. Variant Identity Audit

Per ogni record storico verificare quali elementi permettono di affermare:

> `this is E11-03`

Cercare:

- explicit variant label;
- config snapshot;
- strategy class;
- `expansion_gate_mode`;
- `protect_expansion_capital`;
- hash;
- timestamp;
- filename;
- run identifier.

Classificare l’identità:

- `PROVEN`
- `STRONGLY SUPPORTED`
- `WEAKLY INFERRED`
- `UNSUPPORTED`

---

# 15. Config Provenance Audit

Per i record E11-03 cercare una configurazione salvata insieme al run.

Idealmente:

```text
protect_expansion_capital = True
expansion_gate_mode = MIN_OPERATIONAL
capital_release_mode = BINARY
workforce_scaling_mode = LEGACY
...
```

Se la config non è salvata:

> non dichiarare che il dataset rappresenta con certezza quella configurazione.

---

# 16. Audit degli script scratch

Questa è una verifica critica.

Ispezionare:

`scratch/analyze_e11_3_timing.py`

e stabilire:

- legge dati reali?
- genera dati?
- contiene liste hard-coded?
- contiene percentuali hard-coded?
- ricostruisce unlock timing da proxy?

Fare lo stesso per:

`scratch/run_e11_b1_audit.py`

e tutti gli script correlati.

---

# 17. Hard-Coded Evidence Search

Cercare nel repository:

```powershell
git grep -n "83.3"
git grep -n "60.0"
git grep -n "5.4"
git grep -n "11.2"
git grep -n "11.39"
git grep -n "7193.77"
```

Usare anche ricerca testuale non-Git se i file non sono tracked.

Obiettivo:

> identificare il primo punto in cui questi valori compaiono.

---

# 18. Data Lineage

Per ciascuna metrica storica creare:

| Metric | Report Value | Immediate Source | Upstream Source | Primary Evidence? |
|---|---:|---|---|---|
| 3Q unlock | 83.3% | | | |
| 3Q day | 5.4 | | | |
| 4Q unlock | 60.0% | | | |
| 4Q day | 11.2 | | | |
| Peak active | 54 | | | |
| Peak workforce | 6 | | | |
| Mean money | 7193.77 | | | |

Questa è la tabella centrale di E11-R2.

---

# 19. Provenance Graph

Produrre anche una rappresentazione testuale:

```text
RAW EXECUTION
    ↓
???
    ↓
results/e11_productive_mass.json
    ↓
analyze_e11_3_timing.py
    ↓
E11_03_expansion_gate_unlock.md
    ↓
E11_B1_competitor_expansion_timing_audit.md
```

oppure la lineage realmente osservata.

Non assumere questa struttura in anticipo.

---

# 20. File Modification History

Eseguire dove possibile:

```powershell
git log --follow --stat -- results/e11_productive_mass.json
git log --follow --stat -- scratch/analyze_e11_3_timing.py
git log --follow --stat -- scratch/run_e11_b1_audit.py
git log --follow --stat -- docs/versions/E11_03_expansion_gate_unlock.md
```

Se non tracked:

> registrarlo.

Controllare inoltre metadata filesystem quando disponibili.

---

# 21. Overwrite Risk

Determinare se:

`results/e11_productive_mass.json`

viene sovrascritto a ogni benchmark.

Se sì, verificare se il dataset originale E11-03:

> **è stato perso.**

Questo punto deve essere dichiarato esplicitamente.

---

# 22. Benchmark Script Evolution

Verificare se `benchmark_e11_performance.py`:

- scrive sempre nello stesso JSON;
- aggiorna sezioni;
- sostituisce sezioni;
- cambia schema;
- ricostruisce baseline precedenti usando codice corrente.

Questa distinzione è essenziale.

Se il benchmark corrente “ricalcola E11-03” usando codice corrente:

> non è evidenza storica.

---

# 23. Historical vs Recomputed

Separare rigorosamente:

## HISTORICAL OBSERVATION

dato salvato al momento dell’esperimento.

## CURRENT RECOMPUTATION

nuovo run della variante nominalmente E11-03.

## RECONSTRUCTED / DERIVED

dato creato successivamente.

Non mescolare le tre categorie.

---

# 24. Competitor Audit Contamination

E11-B1 ha utilizzato E11-03 come confronto con i competitor.

Verificare se i valori:

- E11-03 Day 5.36;
- E11-03 Day 11.39;

sono stati:

- letti da raw telemetry;
- letti dal report E11-03;
- generati da uno script;
- hard-coded.

Se B1 dipende da dati E11-03 non verificati:

> classificare anche le relative conclusioni come da riesaminare.

Non invalidare invece i dati competitor se hanno provenienza indipendente e verificabile.

---

# 25. Competitor Evidence Separation

Separare:

### Competitor evidence

- 3Q Day 4.20
- 4Q Day 8.53
- workforce
- active tiles
- livestock timing

da:

### E11-03 comparison evidence

- Day 5.36
- Day 11.39
- 54 active
- 6 workers

Determinare la provenienza separatamente.

---

# 26. No Code Strategy Changes

Durante R2:

NON modificare:

- `productive_mass_roi.py` per strategia;
- crop policy;
- seed policy;
- workforce policy;
- expansion gates;
- reserves;
- livestock.

Sono consentiti:

- script diagnostici read-only;
- test di provenienza;
- parser;
- report.

---

# 27. Provenance Utility

È consentito creare:

`scratch/audit_e11_03_provenance.py`

che deve:

1. leggere i dataset disponibili;
2. enumerare record;
3. identificare variant labels;
4. ricalcolare metriche;
5. mostrare source fields;
6. NON simulare nuovi episodi.

---

# 28. Nessun nuovo benchmark

E11-R2 è un audit storico.

NON eseguire un nuovo benchmark per “verificare” i valori storici.

Un nuovo benchmark dimostra il comportamento corrente, non la provenienza del dato storico.

Sono consentite solo analisi dei dati già esistenti.

---

# 29. Primary Evidence Decision

Alla fine rispondere:

> **Esistono primary execution records sufficienti a dimostrare che la E11-03 storica raggiunse realmente 3Q in 25/30 episodi e 4Q in 18/30?**

Risposta ammessa:

- `YES`
- `PARTIAL`
- `NO`

---

# 30. Se Primary Evidence = YES

Se esistono record verificabili:

1. identificare i 25 episodi 3Q;
2. identificare i 18 episodi 4Q;
3. identificare almeno un episodio 4Q rappresentativo;
4. salvare la sua trace/provenance;
5. confrontare successivamente tale episodio con R1.

Verdetto:

> **HISTORICAL E11-03 BENCHMARK VALIDATED**

A quel punto proporre:

> **E11-R3 — Historical vs Current Trace Differential Audit**

Non eseguirlo automaticamente.

---

# 31. Se Primary Evidence = PARTIAL

Se esistono alcuni dati ma non abbastanza per verificare 25/30 e 18/30:

Verdetto:

> **HISTORICAL E11-03 BENCHMARK PARTIALLY SUPPORTED**

Specificare esattamente quali metriche sono supportate e quali no.

Non usare quelle non supportate come acceptance criteria rigidi.

---

# 32. Se Primary Evidence = NO

Se non esistono record sufficienti:

Verdetto:

> **HISTORICAL E11-03 BENCHMARK NOT VERIFIABLE**

Se emergono prove di hard-coding, synthetic data o misattribution:

usare una classificazione più specifica:

- `HISTORICAL BENCHMARK MISATTRIBUTED`
- `HISTORICAL BENCHMARK SYNTHETIC`
- `HISTORICAL TELEMETRY INTERPRETATION INVALID`

Non cercare più di riprodurre artificialmente il fingerprint 83.3% / 60%.

---

# 33. Conseguenza se benchmark storico non verificabile

Se `NO`:

la baseline E11-03 storica deve essere ritirata come fonte quantitativa autorevole.

NON significa che l’idea E11-03 fosse necessariamente sbagliata.

Significa che:

> **non possediamo evidenza sperimentale verificabile sufficiente per attribuirle quei risultati.**

---

# 34. Nuova baseline — solo raccomandazione

Se il benchmark storico viene invalidato:

NON creare ancora una nuova strategia.

Proporre come passo successivo:

> **E11-R3 — Verified Baseline Re-establishment**

che dovrà:

- partire da codice/config congelati;
- salvare config snapshot;
- salvare episode telemetry;
- usare dataset append-only/versionato;
- produrre hash/run ID;
- impedire sovrascrittura.

Non eseguirlo senza approvazione.

---

# 35. Correzione documentazione storica

Se necessario aggiornare:

- `E11_03_expansion_gate_unlock.md`
- `E11_B1_competitor_expansion_timing_audit.md`
- `E11_R0_baseline_reproducibility_audit.md`
- `E11_R1_e11_03_historical_behavioral_reconstruction.md`

NON cancellare i risultati originali.

Marcarli come:

> `HISTORICAL RESULT — provenance [VALIDATED / PARTIAL / NOT VERIFIABLE]`

Preservare audit trail.

---

# 36. Deliverable

Creare:

`docs/versions/E11_R2_historical_benchmark_provenance_audit.md`

Struttura minima:

1. Executive Summary
2. Audit Question
3. Evidence Hierarchy
4. Available Historical Artifacts
5. Dataset Structure
6. Dataset Modification / Overwrite Risk
7. E11-03 Episode Record Availability
8. Variant Identity
9. Config Provenance
10. 3Q 25/30 Reconstruction
11. 4Q 18/30 Reconstruction
12. Timing Reconstruction
13. Peak Land Reconstruction
14. Active Tiles Reconstruction
15. Workforce Reconstruction
16. Economic Consistency
17. Script Audit
18. Hard-Coded Evidence Search
19. Data Lineage
20. Provenance Graph
21. B1 Dependency Audit
22. Competitor Evidence Separation
23. Primary Evidence Verdict
24. Historical Benchmark Verdict
25. Documentation Corrections
26. Impact on E11-03
27. Impact on E11-06
28. Overall E11 Experimental Integrity
29. Next Step Recommendation

---

# 37. Aggiornamento progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato:

> **E11-R2 Historical Benchmark Provenance Audit COMPLETED**

con verdict esplicito.

---

# 38. Test

Non è necessario modificare la strategy test suite se non viene cambiato codice produttivo.

Se vengono creati parser diagnostici:

verificarli con assert semplici sui conteggi.

Non introdurre test strategici nuovi in R2.

---

# 39. Git

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

Al termine riportare:

1. **Primary Evidence Verdict: YES / PARTIAL / NO**
2. **Historical E11-03 Benchmark Verdict**
3. **numero di raw E11-03 episode records disponibili**
4. **numero di episodi 3Q verificabili**
5. **numero di episodi 4Q verificabili**
6. **3Q timing ricalcolato**
7. **4Q timing ricalcolato**
8. **peak land ricalcolato**
9. **peak active tiles ricalcolato**
10. **peak workforce ricalcolato**
11. **Mean Final Money ricalcolato dagli stessi record**
12. **variant identity confidence**
13. **config provenance confidence**
14. **origine esatta del valore 83.3%**
15. **origine esatta del valore 60.0%**
16. **origine esatta Day 5.4**
17. **origine esatta Day 11.2/11.39**
18. **origine esatta peak 54**
19. **origine esatta workforce 6**
20. **origine esatta $7,193.77**
21. **eventuali valori hard-coded**
22. **eventuali dati sintetici**
23. **eventuale misattribution**
24. **overwrite status di `e11_productive_mass.json`**
25. **B1 competitor evidence validity**
26. **B1 E11-03 comparison validity**
27. **E11-03 status aggiornato**
28. **E11-06 status aggiornato**
29. **overall E11 experimental integrity verdict**
30. **file creati/modificati**
31. **next-step recommendation**

---

# Stop Gate

## Se Primary Evidence = YES

Fermarsi dopo aver documentato gli episodi reali.

Proporre:

> **E11-R3 — Historical vs Current Trace Differential Audit**

## Se Primary Evidence = PARTIAL

Fermarsi.

Proporre un audit mirato esclusivamente sulle metriche mancanti.

## Se Primary Evidence = NO

Fermarsi.

NON tentare ulteriormente di riprodurre 83.3% / 60%.

Proporre:

> **E11-R3 — Verified Baseline Re-establishment**

---

# Regola metodologica finale

Non dobbiamo dimostrare che il vecchio report fosse giusto.

Non dobbiamo nemmeno dimostrare che fosse sbagliato.

Dobbiamo stabilire:

> **quale evidenza primaria esiste realmente dietro ogni numero che abbiamo usato per prendere decisioni.**

Solo i risultati con provenienza verificabile possono continuare a essere utilizzati come baseline quantitativa della serie E11.