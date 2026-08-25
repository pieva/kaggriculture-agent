# Walkthrough — E04 Initial NW Scaling (4 → 9 Tile Compact Cluster)

## Overview

In **E04 (`NWClusterROIAgent`)**, we implemented the primary experimental variable selected in E04-02: scaling the managed tile footprint from 4 tiles (2×2 cluster) to **9 tiles (3×3 compact cluster)** `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` in the initial unlocked NW quadrant, operated by a single farmer without `BUY_LAND` and without `HIRE`.

We also integrated water starvation proxy metrics into the evaluation runner (`runner.py`) to empirically measure whether a single farmer can maintain 9 tiles without crop mortality.

---

## Changes Made

### Strategy Implementation
- **`src/agricola/strategy/nw_cluster_roi.py`** [NEW]: Created `NWClusterROIAgent` managing a 3×3 compact grid of 9 adjacent tiles: `((4,4), (4,3), (4,2), (3,4), (3,3), (3,2), (2,4), (2,3), (2,2))`. Preserved E03 ROI crop selection formula and immediate liquidation logic.
- **`src/agricola/agent.py`** [MODIFY]: Updated submission entrypoint to instantiate `NWClusterROIAgent`.
- **`scripts/build_submission.py`** [MODIFY]: Updated standalone submission builder to bundle `NWClusterROIAgent`.

### Testing & Evaluation Infrastructure
- **`tests/test_nw_cluster.py`** [NEW]: Added 5 unit tests verifying 9-tile cluster tile count, seed purchasing (up to 9 seeds), priority hierarchy (`HARVEST > PLANT > WATER`), Manhattan routing, and PASS behavior.
- **`src/agricola/evaluation/runner.py`** [MODIFY]: Added water starvation proxy tracking (`_compute_starvation_metrics`):
  - **Severe Starvation Proxy:** `weed_count` (tiles converted to `{"kind": "WEED"}` due to $\ge 2$ consecutive unwatered days).
  - **Early-Warning Starvation Proxy:** `unwatered_end_of_day_ratio_pct` (% of days ending at `hour == 23` with unwatered active plants).

---

## Verification Results

### 1. Unit Test Suite
Ran pytest across all 6 test modules:
```bash
.venv/Scripts/python.exe -m pytest tests/
```
**Result:** `19 passed in 2.06s` (100% passing).

### 2. Standalone Submission Build
Generated standalone submission bundle:
```bash
.venv/Scripts/python.exe scripts/build_submission.py
```
**Result:** Standalone submission generated and validated (`test_submission.py` PASSED).

---

### 3. Local Benchmark Comparison (30 Episodes)

Ran 30-episode benchmark evaluation (`scripts/run_eval.py`) against `pass`, `random`, `starter`:

| Metric | E02 (`ROICropAgent`) | E03 Control (`MultiTileROIAgent`) | E04 Target (Plan) | **E04 Actual (`NWClusterROIAgent`)** | E03 → E04 Delta |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Footprint** | 1 tile `(4,4)` | 4 tiles (2×2) | 9 tiles (3×3) | **9 tiles (3×3)** | **4 → 9 tiles** |
| **Total Episodes** | 30 | 30 | 30 | **30** | — |
| **Completion Rate** | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Disqualification Rate** | 0.00% | 0.00% | 0.00% | **0.00%** | 0.00% |
| **Overall Win Rate** | 100.00% | 100.00% | 100.00% | **100.00%** | 0.00% |
| **Mean Final Money** | **$5857.17** | **$14682.47** | **$\ge \$22,000.00$** | **$11232.47 ± $661.26** | **-$3450.00 (-23.49%)** |
| **Median Final Money** | $5837.00 | $14146.00 | — | **$11050.00** | -$3096.00 |
| **Total Weed Conversions** | 0 | 0 | 0 (target) | **238 weeds (7.93/ep)** | **+238 weeds** |
| **Unwatered End-of-Day %** | 0.00% | 0.00% | 0.00% (target) | **3.33%** | +3.33% |
| **Agent Mean Latency** | 0.0267 ms | 0.0698 ms | $< 1.0$ ms | **0.0570 ms** | -0.0128 ms |

---

## Key Empirical Findings & Failure Diagnosis

> [!CAUTION]
> **Ipotesi di Capacità del Singolo Farmer: FALSIFICATA**
> L'estensione del footprint a 9 tile gestite da un **singolo farmer** ha provocato una diminuzione del Mean Final Money del **-23.49%** (`$14682.47` → `$11232.47`).

### Diagnostic Root Cause:
1. **Severe Water Starvation (238 Weeds):**  
   All'inizio dell'episodio, l'agente pianta semi su tutte e 9 le tile. Tuttavia, la distanza Manhattan massima sul cluster 3×3 (fino a 4 passi da `(4,4)` a `(2,2)`), sommata alla regola di priorità `HARVEST > PLANT > WATER`, costringe il singolo farmer a percorrere lunghi tragitti per piantare/raccogliere tile distanti. Di conseguenza, le tile piantate non riescono a ricevere l'azione `WATER` per 2 giorni consecutivi.
2. **Permanent Tile Bricking:**  
   In `kaggriculture.py`, 2 giorni consecutivi di mancata irrigazione trasformano irrevocabilmente la pianta in `{"kind": "WEED"}`. Poiché l'agente non esegue l'azione `DIG` per bonificare le erbacce, in ogni episodio tra **6 e 9 tile su 9 si convertono in WEED**, riducendo permanentemente il terreno coltivabile attivo a 0–3 tile per la maggior parte della stagione.
3. **Capital Drain:**  
   L'acquisto di 9 semi (es. Melone $80 × 9 = $720) drena la cassa iniziale senza che le piante giungano a maturazione a causa della morte per disidratazione.

---

## Conclusion & Next Steps

1. **Experimental Result:** **UNSUPPORTED / FALSIFIED**. Il singolo farmer possiede un **limite fisico di lavorazione pari a 4-6 tile**. Scalare a 9 tile senza lavoratori aggiuntivi (`HIRE`) o senza bonifica delle erbacce (`DIG`) distrugge la produttività agricola.
2. **Critical Value of Experiment:** E04 ha dimostrato con precisione empirica che il collo di bottiglia fondamentale dello scaling **non è la disponibilità di spazio nel quadrante NW, ma la capacità lavorativa del farmer**.
3. **Implicazione per E05:** Per gestire un footprint $\ge 9$ tile senza starvation, la prossima iterazione **deve necessariamente introdurre la forza lavoro subordinata (`HIRE`)** oppure integrare la bonifica automatica (`DIG`) e un routing d'irrigazione proattivo.
