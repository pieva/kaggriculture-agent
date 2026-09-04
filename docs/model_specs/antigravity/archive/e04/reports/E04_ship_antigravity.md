# SHIP & REVIEW Evidence — E04 Initial NW Scaling (`NWClusterROIAgent`)

**Date:** 2026-08-25  
**Strategy:** `NWClusterROIAgent`  
**Phase:** REVIEW → SHIP  
**Status:** Shipped (Consolidated Negative Experimental Result)  
**Tag:** `v0.4-e04-nw-scaling`  

---

## 1. Executive Summary & Experimental Scoping

In **E04 (`NWClusterROIAgent`)**, we tested **strictly one experimental variable**: expanding the managed tile footprint from 4 tiles (2×2 cluster) to a **compact 9-tile cluster (3×3)** `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` within the initial unlocked NW quadrant, operated by a single farmer without `BUY_LAND` and without `HIRE`.

- **Control Baseline:** `MultiTileROIAgent` (E03) on 4 tiles (Mean Final Money: `$14682.47`).
- **Target Economic Criterion (Plan):** Mean Final Money $\ge \$22,000.00$.
- **Actual Economic Result:** Mean Final Money **`$11232.47 ± $661.26`** (`-$3450.00` / `-23.49%` vs E03).
- **Economic Hypothesis Classification:** **`FALSIFIED`**
- **Experimental Integrity & Process Status:** **`PASSED / VALID`** (A methodologically sound experiment that falsifies the hypothesis provides valuable empirical evidence).

---

## 2. REVIEW Decision Matrix

| Dimensione | Esito REVIEW | Note & Evidenze |
| :--- | :---: | :--- |
| **Experimental Integrity** | **PASS** | 1 sola variabile strategica modificata (footprint 4→9 tile). ROI, orizzonte, selling policy e worker count invariati. |
| **Test Suite (`pytest`)** | **PASS** | 19/19 test superati (100% passing in 2.06s), inclusi 5 nuovi unit test in `tests/test_nw_cluster.py`. |
| **Standalone Submission** | **PASS** | `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py` generato e validato via `tests/test_submission.py`. |
| **Completion Rate** | **PASS** | 100.00% (30/30 episodi completati a 720 step). |
| **Disqualification Rate** | **PASS** | 0.00% (0 episodi con stato INVALID o ERROR). |
| **Economic Success Criterion** | **FAIL** | Target $\ge \$22,000.00$ non raggiunto (Effettivo: `$11232.47`). |
| **Water Starvation Criterion** | **FAIL** | Target 0 weed conversions non raggiunto (Effettivo: 238 weed conversions totali). |
| **Economic Hypothesis** | **FALSIFIED** | L'ipotesi che 9 tile con 1 farmer ed E03 policy incrementino il capitale finale è falsificata (-23.49%). |
| **Scaling 4→9 con policy E03** | **NOT SUSTAINABLE** | La policy E03 su 9 tile con 1 farmer causa starvation severa e degrado del capitale finale. |
| **Universal single-worker limit** | **NOT ESTABLISHED** | E04 dimostra l'insostenibilità della specifica policy E03 su 9 tile, non un limite universale invalicabile. |
| **E04 Experimental Value** | **VALID** | Risultato negativo metodologicamente solido che identifica con precisione il collo di bottiglia lavorativo/scheduling. |

---

## 3. Rigorous Interpretation of Results

### 3.1 Water Starvation & Weed Conversions
- **Valore Osservato:** 238 conversioni in `WEED` complessive su 30 episodi, pari a una media di **7.93 weed conversions per episodio**.
- **Chiarimento Metodologico:** I dati di benchmark registrano il numero di eventi di conversione a `WEED`. Poiché `NWClusterROIAgent` non esegue l'azione `DIG` per bonificare le erbacce, una tile convertita a `WEED` rimane occupata, riducendo lo spazio utile di coltivazione per il resto della partita.

### 3.2 Limite della Policy Single-Farmer (No Sovrainterpretazione)
- **Evidenza Conclusiva:** Estendere direttamente la policy E03 (`HARVEST > PLANT > WATER` con routing Manhattan e acquisto semi immediato) da 4 a 9 tile mantenendo un singolo farmer è operativamente insostenibile.
- **Ambito del Risultato:** E04 evidenzia l'esistenza di un **bottleneck di capacità e scheduling**. Non dimostra che *qualsiasi* strategia single-farmer oltre 4 tile sia impossibile (es. strategie water-first o footprint intermedi di 6 tile potrebbero mostrare comportamenti differenti).

### 3.3 Revisione della Stima Teorica del Carico Operativo (17–19 turni/giorno)
- **Stima Statica del PLAN:** 9 azioni `WATER` + ~8–10 passi di movimento = 17–19 turni/giorno (teoricamente $<24$ turni/giorno).
- **Evidenza Acquisita in VERIFY:** Il semplice conteggio `WATER + movimento` **non rappresenta l'intero carico operativo della policy**. Il farmer deve anche gestire:
  1. Azioni `HARVEST`;
  2. Azioni `PLANT`;
  3. Percorsi di transizione fra task di natura diversa;
  4. Distribuzione temporale dei task durante la giornata;
  5. Conflitti di priorità dove task `HARVEST` e `PLANT` rinviano l'irrigazione oltre la soglia critica dei 2 giorni.

---

## 4. Experimental Value of a Negative Result

In accordo con il metodo scientifico supervisionato, un esperimento eseguito con integrità che **falsifica un'ipotesi** non costituisce un fallimento del processo, ma un **risultato empirico di grande valore**:
1. Dimostra che il collo di bottiglia principale dell'agente non è la disponibilità di spazio sulla griglia, ma la capacità di scheduling e lavorazione del singolo worker.
2. Fornisce baseline e metriche quantitative di starvation (`weed_conversions`, `unwatered_end_of_day_ratio`) per valutare le successive iterazioni.

---

## 5. Candidate Directions for Future Iterations (Without E05 Selection)

In conformità con i vincoli di REVIEW/SHIP, si registrano le seguenti 4 direzioni candidate per iterazioni future, **senza selezionare né pianificare E05**:

1. **Capacity Boundary (Footprint Intermedio):**  
   Testare un footprint intermedio (es. 4 → 6 tile) mantenendo la stessa policy e un singolo farmer, per identificare il vero confine di capacita fisica prima della starvation.
2. **Water-First / Scheduling Strategy:**  
   Mantenere il footprint a 9 tile con un singolo farmer, ma invertire la gerarchia di priorità o introdurre uno scheduling proattivo d'irrigazione (`WATER > HARVEST > PLANT`).
3. **HIRE / Multi-Worker:**  
   Mantenere il footprint a 9 tile e introdurre l'assunzione di lavoratori subordinati (`HIRE`) a costo Fibonacci ($1, $1, $2...).
4. **DIG / Weed Recovery:**  
   Introdurre l'azione `DIG` per bonificare le tile coperte da erbacce, classificata principalmente come meccanismo di **recovery** e non come soluzione della causa radice della starvation.

---

## 6. Verification Artifacts & Links

- **Competitive Gap Analysis:** [`docs/experiments/E04-01_Competitive_Gap_Analysis.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/experiments/E04-01_Competitive_Gap_Analysis.md)
- **Experimental Direction Decision:** [`docs/experiments/E04-02_Experimental_Direction_Decision.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/experiments/E04-02_Experimental_Direction_Decision.md)
- **Implementation Plan:** [`docs/plans/E04_Initial_NW_Scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E04_Initial_NW_Scaling.md)
- **VERIFY Evidence:** [`experiments/archive/e04/reports/E04_verify_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e04/reports/E04_verify_antigravity.md)
- **Benchmark JSON Output:** [`experiments/archive/e01/artifacts/baseline.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e01/artifacts/baseline.json)
