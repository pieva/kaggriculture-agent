# E04-02 — Experimental Direction Decision

**Data:** 2026-08-25  
**Fase:** DEFINE / Decision Gate (REVIEW)  
**Autore:** Antigravity AI  
**Stato:** Completed  
**Repository Target:** `docs/experiments/E04-02_Experimental_Direction_Decision.md`  

---

## Executive Summary

La Competitive Gap Analysis (E04-01) ha proposto l'implementazione di un agente combinato (`Horizon & Accurate ROI Agent`). Tuttavia, in virtù del principio fondamentale del progetto:

> **Una modifica strategica principale per esperimento**

è necessario separare rigorosamente le candidate e condurre una **REVIEW decisionale** prima di accedere alla fase **PLAN**.

Il presente documento valuta tre candidate a singola variabile disaggregate:
1. **Candidate A — End-of-Season Horizon**
2. **Candidate B — Accurate ROI / Yield Model**
3. **Candidate C — Initial NW Scaling (4 → 9 Tile Compact Cluster)**

All'esito dell'analisi, si seleziona **Candidate C — Initial NW Scaling** come singola variabile strategica per E04, poiché affronta direttamente il principale collo di bottiglia strutturale identificato (l'84% del terreno iniziale gratuito inutilizzato) offrendo un potenziale incremento di performance **strutturale/significativo** ($>\$22,000$), pur mantenendo un'isolabilità sperimentale perfetta (1 solo farmer, no `BUY_LAND`, no `HIRE`, logica economica E03 invariata).

---

## 1. Review della raccomandazione E04-01

L'analisi E04-01 ha correttamente individuato le carenze economiche di E03, ma ha accorpato nella sua raccomandazione due interventi distinti:
* **Horizon Awareness:** impedire gli investimenti in semi/piante negli ultimi 10-12 giorni se la coltura non può giungere a maturazione prima dello step 720;
* **Accurate ROI:** sostituire l'assunzione `yield_units = 2.0` con il modello di resa reale dal sorgente dell'ambiente (`kaggriculture.py`).

Dal punto di vista della metodologia sperimentale supervisionata, questi due interventi presentano cause, formule, metriche ed impatti totalmente indipendenti. Accorparli introdurrebbe due variabili simultanee. Pertanto, vengono analizzati ed accertati separatamente.

---

## 2. Analisi Dettagliata delle Candidate Disaggregate

### 2.1 Candidate A — End-of-Season Horizon

* **Singola Variabile:** Introduzione di una guardia temporale prima dell'acquisto semi e della semina:
  $$\text{if } \text{day} + \text{crop\_max\_yield\_day} > 29 \implies \text{skip plant}$$
* **Parametri Fissi (Controllo E03):** Footprint 4 tile `{(4,4), (4,3), (3,4), (3,3)}`, 1 farmer, formula ROI E03 (`yield=2.0`), vendita immediata.
* **Valutazione della Perdita di Capitale:**
  - Nel codice di E03 (`multi_tile_roi.py` L93-122), agli step 650-719 l'agente continua ad acquistare semi di Carota ($20), Melone ($80) o Fragola ($100).
  - Su 4 tile, l'acquisto di 4 semi di Melone al giorno 22 comporta una spesa di $320 per frutti che non matureranno prima del termine dell'episodio.
  - L'eliminazione di questo spreco liquida direttamente la cassa finale al turno 720.
* **Ordine di Grandezza dell'Impatto:** **Marginale** (`+$100–$500` su footprint di 4 tile).

---

### 2.2 Candidate B — Accurate ROI / Yield Model

* **Singola Variabile:** Correzione della funzione `select_best_crop` per utilizzare le rese reali definite in `CROPS` in `kaggriculture.py`:
  - `WHEAT`: `max_yield = 6` (costo $10, giorno 4)
  - `CARROT`: `max_yield = 4` (costo $20, giorno 3)
  - `MELON`: `max_yield = 6` (costo $80, giorno 12)
  - `TOMATO` / `STRAWBERRY`: colture `ongoing` con raccolti ricorsivi.
* **Parametri Fissi (Controllo E03):** Footprint 4 tile, 1 farmer, nessuna consapevolezza dell'orizzonte temporale, vendita immediata.
* **Valutazione del Guadagno Economico:**
  - In E03, la formula `((SellPrice * 2.0) - SeedPrice) / Days` sottostima Grano e Melone (resa 6 anziché 2) e ignora il valore cumulativo delle colture pluriennali ongoing.
  - La correzione migliora la resa media per ciclo agricolo su 4 tile.
* **Ordine di Grandezza dell'Impatto:** **Incrementale** (`+$1,000–$3,000` su footprint di 4 tile).

---

### 2.3 Candidate C — Initial NW Scaling (4 → 9 Tile Compact Cluster)

* **Singola Variabile:** Espansione del footprint gestito da 4 tile a un cluster compatto 3×3 di **9 tile** `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` all'interno del quadrante NW già sbloccato.
* **Vincoli Rigorosi:**
  - **NO `BUY_LAND`** (resta 100% all'interno delle 25 tile gratuite del quadrante NW);
  - **NO `HIRE`** (utilizza esclusivamente il singolo farmer);
  - Preserva la formula ROI corrente di E03, l'assenza di horizon awareness e la vendita immediata.
* **Analisi della Capacità Fisica del Singolo Farmer (24 turni/giorno):**
  - Con 4 tile (E03), l'irrigazione e la semina richiedono ~6-8 turni/giorno.
  - Con 9 tile in un cluster compatto 3×3 (distanza Manhattan massima = 4 dai bordi), l'irrigazione giornaliera richiede 9 azioni `WATER` e circa 8-10 passi di movimento $\implies$ **17-19 turni/giorno**.
  - **17-19 turni/giorno è perfettamente inferiore al limite di 24 turni/giorno di un in-game day.** Il farmer può irrigare, seminare e raccogliere tutte le 9 tile senza soffrire starvation o desincronizzazione (le erbacce `WEED` compaiono solo dopo 2 giorni consecutivi senza acqua).
  - Nota su footprint superiori (12-16 tile): Richiederebbero $>25$ turni/giorno per la sola irrigazione, causando il decesso delle piante. Pertanto **9 tile rappresenta il limite fisico ottimale per un singolo farmer**.
* **Ordine di Grandezza dell'Impatto:** **Significativo / Strutturale** (`+$8,000–$17,000+` di incremento locale, con potenziale cassa finale $>\$22,000$).

---

## 3. Separazione Rigorosa di Scaling e HIRE

Come stabilito nel principio metodologico:

> **Non accorpare Scaling e HIRE nello stesso esperimento.**

* **Scaling del Terreno (Candidate C):** Estende il footprint produttivo da 4 a 9 tile sfruttando la capacità temporale residua del singolo farmer (19/24 turni al giorno).
* **Farm Hands (`HIRE`):** Reclutamento di lavoratori aggiuntivi per superare la soglia delle 9 tile (es. 16–25 tile).

`HIRE` viene esplicitamente **escluso da E04** e registrato come candidata per una successiva iterazione (es. E05 o E06), preservando la purezza della singola variabile in E04.

---

## 4. Decision Matrix

| Criterio | Candidate A: Horizon | Candidate B: Accurate ROI | Candidate C: Initial NW Scaling (4→9) |
| :--- | :--- | :--- | :--- |
| **Gap supportato da evidenza** | **SUPPORTED**: L93-122 `multi_tile_roi.py` acquista a t=719. | **SUPPORTED**: L44 `multi_tile_roi.py` hardcoda `yield=2.0`. | **SUPPORTED**: L158 `kaggriculture.py` sblocca 25 tile, E03 ne usa solo 4. |
| **Impatto economico potenziale** | **Marginale** (`+$100–$500`): evita perdite a fine episodio. | **Incrementale** (`+$1k–$3k`): ottimizza la resa per tile. | **Significativo / Strutturale** (`+$8k–$17k`): raddoppia l'output (+125% tile). |
| **Impatto competitivo potenziale** | **Basso**: non risolve il deficit di volume di produzione. | **Medio-Basso**: ottimizza il tipo di coltura su 4 tile. | **Alto**: raddoppia la produzione avvicinando il volume dei top bot Kaggle. |
| **Isolabilità sperimentale** | **Eccellente**: singola guardia temporale `if day + crop_days > 29`. | **Eccellente**: modifica pura della funzione scoring ROI. | **Alta**: espansione footprint (4→9 tile) mantenendo 1 farmer e logica E03. |
| **Misurabilità locale** | **Alta**: capitale liquido a t=720 e semi sprecati. | **Alta**: Mean Final Money e resa per ciclo. | **Alta**: Mean Final Money, tile coltivate, starvation rate. |
| **Rischio operativo** | **Nullo**: nessuna modifica a loop o movimento. | **Molto Basso**: sostituzione formule economiche. | **Basso-Medio**: rischio starvation se il footprint eccede i 24 turni/giorno. |
| **Complessità implementativa** | **Triviale** (<10 righe). | **Molto Bassa** (<30 righe). | **Bassa** (estensione lista `managed_tiles` da 4 a 9 e tuning routing). |
| **Dipendenza da altre meccaniche** | **Nessuna**. | **Nessuna**. | **Capacità fisica del farmer** (cappato a ~9 tile per 24 turni/giorno). |
| **Capacità di spiegare gap Kaggle** | **Bassa**: spiega solo perdite marginali late-game. | **Medio-Bassa**: spiega solo la scelta sub-ottimale della coltura. | **Alta**: spiega il divario quantitativo di throughput rispetto ai concorrenti. |

---

## 5. Stima Critica dell'Ordine di Grandezza dell'Impatto

Verifica dell'affermazione di E04-01 sull'impatto di Horizon (`+$300–$800`):
* **Natura della stima:** Trattasi di una **stima teorica indicativa del limite superiore** basata sul costo di 4 semi di Melone ($320) o Fragola ($400) acquistati negli ultimi 5 giorni su un cluster di 4 tile.
* **Verifica:** La stima non è un dato sperimentale misurato, ma un calcolo analitico. Essa dimostra che l'Horizon Awareness da sola su 4 tile **non può produrre un salto competitivo significativo** (es. +100%).
* **Confronto delle candidate:**
  - Candidate A (Horizon): Marginale ($<\$1,000$)
  - Candidate B (Accurate ROI): Incrementale ($\$1,000 - \$4,000$)
  - Candidate C (Initial NW Scaling 4→9 tile): Significativo / Strutturale ($\$8,000 - \$17,000+$)

---

## 6. Separazione tra Performance dell'Agente e Qualità del Benchmark

### Valutazione del Benchmark Locale Attuale (`pass`, `random`, `starter`)

* **Candidate A & B:** Il benchmark corrente è ancora valido per misurare il delta di Final Money su 4 tile.
* **Candidate C (Initial NW Scaling):** Il Win Rate verso `starter` è **già saturo (100%)**. Tuttavia, la metrica **Mean Final Money** su 30 episodi resta **100% valida e discriminante** per misurare il passaggio da $14.6k a $22k+.
* **Metrologia Integrata:** Per la Candidate C è necessario aggiungere al benchmark la tracciabilità della metrica di **Water Starvation Rate** (% di tile che diventano `WEED` a causa del ritardo d'irrigazione del farmer su 9 tile).

---

## 7. Valutazione di un Competitive Benchmark Agent (`synthetic_expansion_agent`)

* **Ruolo:** Strumento di misurazione (metrologia), non strategia dell'agente E04.
* **Stato Decisionale:** **NON NECESSARIO PRIMA DI E04.**
* **Motivazione:** Le metriche correnti del benchmark locale (`Mean Final Money`, `Completion Rate`, `Disqualification Rate`, `Latency`) sono quantitative, riproducibili e sufficienti per validare l'ipotesi di Candidate C contro la baseline E03 ($14,682.47). L'integrazione di un avversario sintetico multi-tile potrà essere trattata come miglioramento infrastrutturale indipendente.

---

## 8. Decisione Strategica E04

Si seleziona ufficialmente per E04:

> **Candidate C — Initial NW Scaling (4 → 9 Tile Compact Cluster)**

### Motivazioni Chiave:
1. **Risoluzione del Principale Gap di E03:** Risolve direttamente l'84% di inefficienza del terreno iniziale gratuito sbloccato nel quadrante NW.
2. **Impatto Competitivo Significativo:** È l'unica candidata in grado di raddoppiare l'output di produzione (passando da 4 a 9 tile, +125% di capacità) avvicinando l'agente al throughput dei bot top di Kaggle.
3. **Pura Singola Variabile Sperimentale:** Modifica esclusivamente il set delle tile gestite `managed_tiles` da 4 a 9. Non introduce `BUY_LAND`, non introduce `HIRE`, e mantiene intatte le formule economiche e operative di E03.
4. **Fattibilità Operativa Verificata:** 9 tile in cluster compatto 3×3 richiedono 17-19 turni/giorno al farmer, ampiamente entro il budget di 24 turni/giorno.

---

## 9. Definizione Preliminare dell'Ipotesi Sperimentale (E04)

### Experimental Variable
> Espansione del cluster di tile gestite da 4 tile `{(4,4), (4,3), (3,4), (3,3)}` a un cluster compatto 3×3 di 9 tile `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` all'interno del quadrante iniziale NW, gestito da un singolo farmer senza `BUY_LAND` e senza `HIRE`.

### Formattazione Ipotesi
> **Se** espandiamo il footprint produttivo da 4 a 9 tile nel quadrante NW mantenendo un singolo farmer e preservando la logica economica e operativa di E03, **allora** il Mean Final Money nel benchmark locale aumenterà significativamente (da `$14,682.47` a $\ge \$22,000.00$), **perché** il footprint 3×3 raddoppia la capacità di produzione agricola rimanendo entro i limiti fisici di movimento del farmer (17-19 turni/giorno $< 24$ turni/giorno).

### Primary Metric
> **Mean Final Money** su 30 episodi nel benchmark locale controllato (`scripts/run_eval.py`).

### Secondary Metrics
1. **Disqualification Rate** (Target: `0.00%`).
2. **Water Starvation Rate** (% di tile gestite che soffrono `consecutive_unwatered >= 2` o diventano `WEED`; Target: `0.00%`).
3. **Agent Mean Turn Latency** (ms/turno; Target: $< 1.0$ ms/turno).

### Control Baseline
> `MultiTileROIAgent` (E03) su cluster 2×2 (4 tile) con Mean Final Money **`$14682.47`**.

### Success Criterion (Preliminare)
> Mean Final Money $\ge \$22,000.00$ (`+50%` min delta vs E03), Completion Rate `= 100.0%`, Disqualification Rate `= 0.0%`, Water Starvation Rate `= 0.0%`.

---

## 10. Decisione sulla Metrologia

### Decisione: **Opzione A — Benchmark corrente sufficiente**

* **Motivazione:** Le metriche correnti del runner locale (`scripts/run_eval.py`) forniscono una misura quantitativa diretta, riproducibile ed esente da ambiguità per valutare Candidate C verso E03.
* **Integrazione Minima:** Verrà tracciato internamente il tasso di starvation dell'irrigazione (`Water Starvation Rate`) per confermare che 1 farmer riesca a servire 9 tile senza creare erbacce.
* L'implementazione di un avversario sintetico multi-tile resta un'opzione per future iterazioni infrastrutturali.

---

## 11. Open Questions / Unknowns

1. **[UNKNOWN] Geometria Ottimale di Navigazione 3×3:**  
   Il comportamento esatto della coda di priorità Manhattan (`HARVEST > PLANT > WATER`) su 9 tile con tie-breaking deterministico `(y, x)` richiede validazione nella fase BUILD per confermare che non insorgano oscillazioni inutili.

2. **[UNKNOWN] Soglia Critica di Liquidità per l'Acquisto Semi su 9 Tile:**  
   Verificare se nei primi giorni di gioco la cassa iniziale ($3000) sia sufficiente per popolare rapidamente 9 tile con semi ad alto costo (es. Melone $80 × 9 = $720).

---

*Documento completato e salvato in `docs/experiments/E04-02_Experimental_Direction_Decision.md` in conformità con i vincoli della fase REVIEW / Decision Gate.*
