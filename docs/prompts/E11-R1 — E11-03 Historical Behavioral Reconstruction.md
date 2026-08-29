# E11-R1 — E11-03 Historical Behavioral Reconstruction

## Contesto

L’audit **E11-R0 — Baseline Reproducibility Audit** ha identificato e corretto due problemi reali di isolamento delle configurazioni E11:

1. contaminazione dei default di `ProductiveMassConfig`;
2. parameter leak nelle factory di `scripts/benchmark_e11_performance.py`.

Sono stati quindi ripristinati:

- default legacy;
- factory esplicite e indipendenti;
- isolamento delle configurazioni;
- test contro la contaminazione tra varianti.

Tuttavia **E11-R0 non può essere considerato concluso come ripristino della riproducibilità storica**, perché il principale acceptance criterion non è stato soddisfatto.

Il benchmark post-fix attribuisce a E11-03:

- Mean Final Money: **$892.63**
- Mean quadrants: **2.00**
- Q2 unlock: **0.0%**

mentre il report storico di E11-03 documentava un comportamento architetturale radicalmente differente:

- **3Q / 75 tiles unlock rate: ~83.3%**
- **4Q / 100 tiles unlock rate: ~60.0%**
- **100 tiles raggiungibili**
- **peak active productive tiles: ~54**
- **peak workforce: ~6**
- Mean Final Money nell’ordine di **~$7k**

Il problema residuo non è quindi più principalmente:

> configuration isolation

ma:

> **historical behavioral reproducibility**

---

# 1. Stato ufficiale da utilizzare

Correggere lo stato di E11-R0 in:

> **E11-R0 PARTIALLY COMPLETED — configuration isolation restored, historical behavioral reproducibility NOT restored**

E11-03 deve essere classificata:

> **NOT REPRODUCED**

finché non torna a mostrare un fingerprint architetturale compatibile con il risultato storico.

E11-06 deve rimanere:

> **RESULT INVALID FOR CAUSAL INTERPRETATION**

Non progettare né implementare E11-07.

---

# 2. Obiettivo E11-R1

Eseguire:

> **E11-R1 — E11-03 Historical Behavioral Reconstruction**

Obiettivo:

> **ricostruire esattamente perché l’attuale E11-03 non riproduce più il comportamento architetturale documentato nel benchmark storico e ripristinare tale comportamento senza introdurre alcuna nuova strategia.**

La domanda sperimentale principale è:

> **Qual è il primo punto di divergenza tra la E11-03 storica documentata e l’attuale implementazione isolata?**

---

# 3. Principio metodologico

NON partire dal risultato economico.

Il fingerprint primario di E11-03 è architetturale.

La ricostruzione deve seguire questa catena causale:

```text
cash
  ↓
crop/seed decisions
  ↓
active productive tiles
  ↓
expansion readiness
  ↓
BUY_LAND Q2
  ↓
75 tiles
  ↓
cash accumulation
  ↓
BUY_LAND Q3
  ↓
100 tiles
  ↓
workforce scaling
  ↓
54+ active tiles / ~6 workers
```

Individuare **il primo nodo della catena che diverge dal comportamento storico**.

Non correggere sintomi downstream prima di aver identificato la prima divergenza.

---

# 4. Fonti di verità

Leggere integralmente prima di modificare codice:

- `docs/versions/E11_03_expansion_gate_unlock.md`
- `docs/versions/E11_02_expansion_capital_protection.md`
- `docs/versions/E11_04_seed_expansion_synchronization.md`
- `docs/versions/E11_R0_baseline_reproducibility_audit.md`
- `docs/versions/E11_plan_productive_mass_expansion.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Leggere inoltre:

- `src/agricola/strategy/productive_mass_roi.py`
- `scripts/benchmark_e11_performance.py`
- `tests/test_e11_productive_mass.py`

Se esistono altri script `scratch/` creati durante E11-03 o R0, ispezionarli quando possono contenere informazioni utili.

---

# 5. Ricostruzione della E11-03 storica

Creare una sezione:

## Historical E11-03 Behavioral Specification

Ricavare ESCLUSIVAMENTE dalla documentazione storica:

### Configurazione

Registrare tutti i parametri documentabili:

- `protect_expansion_capital`
- `expansion_gate_mode`
- `expansion_crop_policy`
- `capital_release_mode`
- operating reserve
- land reserve
- land purchase threshold
- Q1 readiness
- Q2 readiness
- Q3 readiness
- workforce parameters
- crop policy
- livestock policy
- seed cutoffs
- max workers
- active tile thresholds

Per ogni parametro indicare:

- valore storico documentato;
- valore attuale;
- source file.

Se un valore storico NON è documentato:

> segnalarlo come `UNKNOWN`

Non inventarlo.

---

# 6. Historical Fingerprint

Formalizzare il fingerprint storico E11-03:

| Metrica | E11-03 storico |
|---|---:|
| 3Q / 75 tiles unlock | ~83.3% |
| Mean 3Q timing | ~Day 5.4 |
| 4Q / 100 tiles unlock | ~60.0% |
| Mean 4Q timing | ~Day 11.2–11.4 |
| Peak land | 100 tiles |
| Peak active productive tiles | ~54 |
| Peak workforce | ~6 |
| Livestock | 0% |
| Mean Final Money | ~ordine $7k |

Usare i valori esatti dei report quando disponibili.

Questo fingerprint costituisce l’acceptance target.

---

# 7. NON usare il money come criterio principale

Una configurazione che produce ~$7k ma rimane a 50 tile:

> **NON è E11-03 riprodotta.**

Una configurazione che riproduce:

- 3Q;
- 4Q;
- active footprint;
- workforce;

ma produce un money moderatamente differente può essere classificata:

> `BEHAVIORALLY REPRODUCED — ECONOMIC DRIFT`

La priorità è ricostruire il comportamento.

---

# 8. Git Historical Audit

Eseguire:

```powershell
git log --oneline --all -- src/agricola/strategy/productive_mass_roi.py
git log -p --all -- src/agricola/strategy/productive_mass_roi.py
git log --oneline --all -- scripts/benchmark_e11_performance.py
git log -p --all -- scripts/benchmark_e11_performance.py
```

Verificare se esiste un commit/snapshot corrispondente temporalmente a E11-03.

Se sì:

- NON fare checkout distruttivo;
- usare `git show`;
- confrontare il file storico con quello corrente.

Esempio:

```powershell
git show <commit>:src/agricola/strategy/productive_mass_roi.py
```

Se E11-03 non era ancora committata:

> dichiararlo esplicitamente.

In tal caso la documentazione E11-03 diventa la principale fonte storica.

---

# 9. Semantic Diff

Non limitarsi al diff dei parametri.

Confrontare la semantica delle funzioni che influenzano la catena E11-03.

In particolare cercare:

- land readiness;
- land purchase;
- active tile counting;
- crop selection;
- seed purchasing;
- reserve calculation;
- hiring;
- worker assignment;
- planting;
- watering;
- action priority.

Individuare tutte le funzioni coinvolte.

Creare tabella:

| Function / Logic | Historical semantics | Current semantics | Changed? | Potential impact |
|---|---|---|---|---|

---

# 10. Active Tiles Definition Audit

Questa verifica è prioritaria.

E11-03 storicamente riusciva a soddisfare:

- Q2 readiness `active_tiles >= 8`;
- Q3 readiness `active_tiles >= 12`.

L’attuale E11-03 rimane a 2Q.

Verificare esattamente:

> **come viene calcolato `active_tiles` oggi**

e confrontarlo con la semantica utilizzata nel benchmark storico.

Controllare se conta:

- planted;
- growing;
- watered;
- harvestable;
- harvested-but-not-replanted;
- dug;
- occupied;
- crop-bearing tiles.

Una modifica apparentemente piccola nella definizione può spiegare il fallimento del gate.

---

# 11. Land Readiness Audit

Isolare la funzione/condizione che decide:

```text
CAN BUY NEXT QUADRANT?
```

Per ogni giorno di un episodio E11-03 registrare:

```text
day
cash
owned_quadrants
active_tiles
required_active_tiles
cash_threshold
readiness_boolean
BUY_LAND_allowed
BUY_LAND_executed
```

Dobbiamo sapere se il fallimento avviene perché:

A. manca cash;

B. mancano active tiles;

C. readiness è true ma BUY_LAND non viene selezionata;

D. BUY_LAND viene selezionata ma non eseguita;

E. il conteggio quadranti è errato.

---

# 12. Capital Protection Audit

Ricostruire esattamente la E11-03 storica.

Dal precedente esperimento risultava che la protezione rigida consentiva l’espansione territoriale ma bloccava le colture ad alto rendimento.

Verificare quindi che l’attuale implementazione non abbia trasformato:

> protezione del capitale per il terreno

in:

> blocco generalizzato della produzione necessaria a raggiungere il gate.

Registrare separatamente:

- essential seed spending;
- optional seed spending;
- operating reserve;
- land reserve;
- hire reserve.

---

# 13. Essential Seed Audit

Verificare la semantica di:

- Carrot;
- Wheat;

durante capital protection.

E11-03 storicamente riusciva a mantenere abbastanza produzione di base da raggiungere:

- active tiles >= 8;
- successivamente >= 12.

Controllare:

- quantità minima di semi;
- inventory threshold;
- prezzo;
- reserve floor;
- plant selection;
- eventuale starvation.

---

# 14. Workforce Audit

Non ottimizzare la workforce.

Verificare solo che la workforce storica di E11-03 sia ricostruita.

Controllare:

- numero iniziale;
- primo HIRE;
- hire thresholds;
- max workers;
- reserve;
- rapporto tile/worker;
- priorità HIRE rispetto a BUY_LAND.

L’attuale E11-03 deve poter raggiungere circa:

> **6 worker peak**

quando raggiunge il terreno completo.

---

# 15. Action Priority Audit

Verificare se la gerarchia attuale è ancora compatibile con E11-03.

In particolare:

```text
HIRE / BUY_LAND
WATER
FEED
HARVEST
PLANT
DIG
MOVE
PASS
```

Controllare se una modifica successiva ha introdotto un’azione che impedisce:

- planting;
- harvesting;
- BUY_LAND;
- hiring.

---

# 16. Single-Seed Historical Reconstruction

Se il report storico contiene dati per seed, utilizzare uno di quelli che raggiungeva 4Q.

Se non contiene tale informazione:

- utilizzare seed `0` come diagnostica iniziale;
- successivamente cercare tra i 30 seed storici un episodio che dovrebbe raggiungere 4Q in base alla distribuzione aggregata.

Non assumere che seed 0 fosse necessariamente un episodio 4Q.

---

# 17. Trace giornaliera

Creare uno script diagnostico:

`scratch/trace_e11_03_historical_reconstruction.py`

Output minimo:

```text
DAY  CASH  Q  ACTIVE  WORKERS  SEEDS  READY_NEXT_Q  BUY_LAND  MODE
```

Aggiungere quando utile:

- crop counts;
- seed inventory;
- planted;
- harvestable;
- reserve;
- target quadrant.

---

# 18. First Divergence Analysis

Il deliverable centrale deve contenere:

## First Behavioral Divergence

Esempio concettuale:

```text
Day 3:
Historical expected:
active_tiles >= 8

Current:
active_tiles = 6

Reason:
essential seed purchase blocked by ...
```

oppure:

```text
Day 5:
cash = 1,140
active_tiles = 9
readiness = TRUE

BUY_LAND not executed because HIRE has higher priority
```

Non procedere alla correzione finché questo punto non è stato identificato.

---

# 19. Ricostruzione incrementale

Una volta individuata la prima divergenza:

applicare **la minima modifica necessaria per ripristinare la semantica storica**.

NON introdurre nuovi parametri strategici salvo siano indispensabili per rappresentare una differenza storica già esistente.

---

# 20. Historical Compatibility Mode

Se la classe corrente è diventata semanticamente troppo diversa per rappresentare E11-03 con i soli parametri esistenti, è consentito introdurre:

```text
behavior_version = "E11_03"
```

o meccanismo equivalente.

Ma SOLO se necessario.

Preferire:

- branching esplicito;
- piccolo;
- documentato.

Non duplicare l’intero agente se evitabile.

---

# 21. No Optimization Rule

Qualsiasi modifica deve rispondere alla domanda:

> **questa logica esisteva già implicitamente o esplicitamente nella E11-03 storica?**

Se la risposta è NO:

> non implementarla.

Questo non è un esperimento di miglioramento.

---

# 22. Progressive Reproduction Test

Non lanciare immediatamente 30 episodi dopo ogni modifica.

Usare:

### Stage A — Single episode

1 seed.

### Stage B — Mini batch

5 seed.

### Stage C — Intermediate

10 seed.

### Stage D — Full reproduction

30 episodi paired.

Procedere allo stage successivo solo se emerge il fingerprint previsto.

---

# 23. Stage A Acceptance

Nel singolo episodio deve almeno emergere la possibilità di:

- superare 2Q;
- aumentare active tiles;
- aumentare workforce.

Se resta a 2Q per starvation evidente:

> continuare diagnosi.

---

# 24. Stage B Acceptance

Su 5 seed:

- almeno alcuni episodi devono raggiungere 3Q;
- almeno uno dovrebbe poter raggiungere 4Q se il campione lo consente;
- active footprint deve crescere oltre 20.

Non usare percentuali storiche come requisito rigido su N=5.

---

# 25. Stage C Acceptance

Su 10 seed il comportamento deve iniziare ad avvicinarsi chiaramente al fingerprint storico.

Verificare:

- 3Q frequency;
- 4Q frequency;
- active tiles;
- workers.

---

# 26. Full 30-Episode Acceptance

Solo sul benchmark completo confrontare quantitativamente:

| Metric | Historical | Reconstructed | Delta |
|---|---:|---:|---:|
| 3Q unlock % | ~83.3% | | |
| 3Q mean day | ~5.4 | | |
| 4Q unlock % | ~60.0% | | |
| 4Q mean day | ~11.2–11.4 | | |
| Peak land | 100 | | |
| Peak active | ~54 | | |
| Peak workers | ~6 | | |
| Mean Final Money | ~historical | | |

---

# 27. Reproduction Classification

Classificare E11-03 come:

### `FULLY REPRODUCED`

se comportamento architetturale e risultati economici sono compatibili.

### `BEHAVIORALLY REPRODUCED — ECONOMIC DRIFT`

se:

- land expansion;
- active footprint;
- workforce;

sono compatibili, ma il money differisce significativamente.

### `PARTIALLY REPRODUCED`

se solo parte del fingerprint viene recuperata.

### `NOT REPRODUCED`

se rimane a 2Q o manca il comportamento fondamentale.

---

# 28. Tolleranze

Non pretendere identità numerica artificiale.

Come guida diagnostica, non come automatismo:

- 3Q unlock entro circa ±10 punti percentuali;
- 4Q unlock entro circa ±10 punti percentuali;
- mean timing entro circa ±1 giorno;
- peak active tiles nella stessa classe (~50+);
- workforce nella stessa classe (~6).

Se i risultati sono appena fuori soglia, analizzare prima di classificare.

---

# 29. Verifica della telemetria

Assicurarsi che:

- Q2/Q3 naming sia coerente;
- 3Q significhi 75 tiles;
- 4Q significhi 100 tiles;
- unlock timing sia misurato allo stesso evento;
- peak active sia calcolato nello stesso modo.

Una differenza di telemetria NON deve essere scambiata per una differenza strategica.

---

# 30. Correzione E11-R0

Aggiornare:

`docs/versions/E11_R0_baseline_reproducibility_audit.md`

Correggendo qualsiasi dichiarazione:

> `E11-03 REPRODUCED & RESTORED`

in base al nuovo stato verificato.

Registrare chiaramente:

> **Configuration isolation was restored in E11-R0, but behavioral reproducibility remained unresolved because E11-03 failed its historical architecture fingerprint.**

---

# 31. Deliverable E11-R1

Creare:

`docs/versions/E11_R1_e11_03_historical_behavioral_reconstruction.md`

Struttura minima:

1. Executive Summary
2. R0 Correction
3. Historical E11-03 Specification
4. Historical Fingerprint
5. Git Historical Audit
6. Configuration Diff
7. Semantic Code Diff
8. Active Tiles Audit
9. Land Readiness Audit
10. Capital Protection Audit
11. Essential Seed Audit
12. Workforce Audit
13. Action Priority Audit
14. Telemetry Compatibility Audit
15. Single-Seed Trace
16. First Behavioral Divergence
17. Root Cause
18. Minimal Historical Fix
19. Stage A Result
20. Stage B Result
21. Stage C Result
22. 30-Episode Reproduction Benchmark
23. Historical vs Reconstructed Matrix
24. Reproduction Verdict
25. Impact on E11-06
26. Next Step Recommendation

---

# 32. Test suite

Aggiungere test specifici che proteggano il fingerprint semantico recuperato.

Non testare soltanto:

```text
config.expansion_gate_mode == "MIN_OPERATIONAL"
```

Testare il comportamento.

Esempi:

- readiness true a active threshold corretto;
- essential seed spending consentito durante protection;
- BUY_LAND eseguibile con readiness + cash;
- historical E11-03 factory produce config corretta;
- E11-03 non eredita workforce co-scaling E11-06.

---

# 33. Aggiornamento progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato durante il lavoro:

> **E11-R1 Historical Behavioral Reconstruction IN PROGRESS**

---

# 34. E11-06

NON rieseguire E11-06 durante la fase diagnostica.

Solo se E11-03 viene classificata almeno:

> **BEHAVIORALLY REPRODUCED**

allora è consentito predisporre il successivo re-run pulito di E11-06.

Se E11-03 resta:

> `NOT REPRODUCED`

fermarsi.

---

# 35. E11-07

NON:

- progettare;
- implementare;
- benchmarkare;

E11-07.

Non introdurre:

- Dynamic Adaptive Capital Release;
- nuove crop policy;
- nuovi gate;
- nuovi workforce target;
- nuove strategie livestock.

---

# 36. Git final check

Alla fine eseguire:

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

1. **stato corretto E11-R0**
2. **E11-03 historical configuration reconstructed**
3. **historical fingerprint**
4. **git historical evidence available / unavailable**
5. **first behavioral divergence**
6. **root cause**
7. **file/function responsabile**
8. **minimal historical fix**
9. **active_tiles historical/current semantic comparison**
10. **land readiness historical/current comparison**
11. **capital protection historical/current comparison**
12. **essential seed behavior historical/current comparison**
13. **workforce historical/current comparison**
14. **Stage A result**
15. **Stage B result**
16. **Stage C result**
17. **test suite result**
18. **30-episode Mean Final Money**
19. **3Q unlock rate**
20. **3Q mean timing**
21. **4Q unlock rate**
22. **4Q mean timing**
23. **peak land**
24. **peak active productive tiles**
25. **peak workforce**
26. **livestock activation**
27. **historical vs reconstructed delta matrix**
28. **E11-03 reproduction verdict**
29. **E11-06 causal status**
30. **overall E11 reproducibility status**
31. **file creati/modificati**
32. **next-step recommendation**

---

# Stop Gate

## Caso A — E11-03 riprodotta

Se E11-03 raggiunge almeno:

> **BEHAVIORALLY REPRODUCED**

fermarsi e proporre esclusivamente:

> **clean re-run di E11-06 contro la E11-03 storicamente ripristinata**

Non eseguire automaticamente il re-run senza approvazione del supervisore.

## Caso B — E11-03 non riprodotta

Se il fingerprint rimane incompatibile:

> **STOP**

Non procedere a E11-06.

Non procedere a E11-07.

Riportare esattamente quale divergenza rimane aperta.

---

# Regola metodologica finale

L’obiettivo di E11-R1 NON è ottenere un risultato migliore.

L’obiettivo è poter affermare nuovamente:

> **“Quando eseguiamo E11-03, otteniamo la stessa classe di comportamento che avevamo osservato e documentato quando E11-03 fu originariamente validata.”**

Solo dopo questa condizione la serie sperimentale E11 può tornare a produrre confronti causali affidabili.