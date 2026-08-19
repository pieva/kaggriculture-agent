# Implementation Plan - E02: Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)

Questo documento definisce il piano di implementazione rivisto e consolidato per l'evoluzione **E02**, la seconda iterazione supervisionata del progetto **Kaggriculture Agent**.

---

## 1. Analisi della Baseline E01 e Motivazione dell'Evoluzione

In **E01**, l'agente baseline (`CarrotLoopAgent`) ha dimostrato la stabilità dell'infrastruttura di esecuzione (100% completion rate, 0% squalifiche, score di 600.0 su Kaggle). Tuttavia, utilizzava solo una frazione minima delle informazioni disponibili in `GameState`:
* Coltura fissa: piantava esclusivamente `CARROT` (costo seme 20, resa 2 carote/3 giorni).
* Prezzi e ROI ignorati: nessun confronto tra il rendimento/giorno delle 5 colture disponibili (`WHEAT`, `CARROT`, `TOMATO`, `STRAWBERRY`, `MELON`).

In **E02**, introduciamo un'evoluzione incrementale e rigorosamente controllata: **Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)**.

---

## 2. Definizione ed Origine delle Metrike di Baseline E01

Per garantire la massima rigorosità nel confronto quantitativo tra E01 ed E02, si chiarisce la distinzione tra le evidenze prodotte in E01:

* **Baseline Quantitativa E01 per il Confronto Benchmark**:
  * **`Mean Final Money E01` = $3578.80 ± $206.65** (Media calcolata sui 30 episodi del benchmark locale E01 salvati in `results/e01_baseline.json`).
  * **`Overall Win Rate E01` = 66.67%** (20 Vittorie vs `pass`/`random`, 0 Sconfitte, 10 Pareggi / 0% Win Rate vs `starter`).
* **Valore del Singolo Episodio VERIFY**:
  * **`Final Money / Reward VERIFY` = 3564.0** (Valore puntuale ottenuto nell'unico episodio di ispezione comportamentale eseguito con Antigravity al turno 719).

Nel seguito del documento e nelle valutazioni dell'esperimento E02, il riferimento per il confronto statistico sarà esclusivamente la media del benchmark **`Mean Final Money E01 = $3578.80`**.

---

## 3. Ipotesi Sperimentale di E02

> **Ipotesi Sperimentale (da verificare)**:
> Se l'agente seleziona dinamicamente ad ogni ciclo la coltura a maggior rendimento netto giornaliero ($\text{ROI / giorno}$) compatibile con il capitale liquido disponibile (`money`), anziché coltivare esclusivamente carote, allora si ipotizza che:
> 1. Il capitale medio finale a fine stagione (720 turni) aumenterà significativamente rispetto al valore medio della baseline E01 ($3578.80$).
> 2. L'agente otterrà una percentuale di vittorie (Win Rate) positiva contro lo `starter` agent di Kaggle (superando la condizione di pareggio sistematico di E01).

### Risultati ed Obiettivi Attesi (Target Sperimentali):
* **Target Mean Final Money E02**: $> 4500.0 \$$ (risultato atteso da verificare).
* **Target Win Rate vs `starter`**: $> 90.0\%$ (risultato atteso da verificare).

---

## 4. Origine dei Dati e Formula del Calcolo ROI

La selezione della coltura ottimale avverrà tramite una stima del profitto netto giornaliero basata su due strutture distinte dell'ambiente, entrambe legittimamente osservabili dall'agente ad ogni turno:

### Origine delle Informazioni:
1. **Prezzo di vendita dinamico ($\text{SellPrice}_c$)**: letto dinamicamente dal mercato tramite `state.get_price(c)` (ovvero `observation["market"]["prices"][c]`).
2. **Prezzo del seme ($\text{SeedPrice}_c$)**: estratto dalla configurazione del costo del seme della coltura `CROPS[c]["seed"]` (es. `CARROT`=20, `TOMATO`=50, `MELON`=80).
3. **Resa per raccolto ($\text{Yield}_c$)**: resa standard osservata con irrigazione regolare (2 unità).
4. **Giorni di crescita ($\text{Days}_c$)**: parametro statico di crescita estratto da `CROPS[c]["max_yield_day"]` (`WHEAT`=2, `CARROT`=3, `TOMATO`=4, `STRAWBERRY`=5, `MELON`=12).

### Formula del Rendimento Giornaliero:
$$\text{NetProfitPerDay}(c) = \frac{(\text{SellPrice}_c \times \text{Yield}_c) - \text{SeedPrice}_c}{\text{Days}_c}$$

### Regola Decisionale:
Tra tutte le colture $c$ per cui $\text{SeedPrice}_c \le \text{money}$, l'agente sceglierà la coltura $c^*$ che massimizza $\text{NetProfitPerDay}(c^*)$.

---

## 5. Isolamento Sperimentale

Per garantire che l'eventuale variazione delle metriche sia **interamente attribuibile alla selezione dinamica della coltura**, le seguenti dimensioni rimarranno **rigorosamente invariate** rispetto a E01:

* **Posizione e mobilità**: Il contadino rimane sulla singola casella iniziale `(4, 4)` senza effettuare movimenti (`MOVE`).
* **Ciclo operativo fondamentale**: `BUY_SEED → PLANT → WATER → PASS → HARVEST → PLANT → SELL`.
* **Infrastruttura**: Stesso runner di valutazione (`scripts/run_eval.py`), stessi test automatizzati e bundler per la submission.
* **Parametri di benchmark**: 30 episodi stagionali da 720 turni contro la stessa suite di avversari (`pass`, `random`, `starter`).

---

## 6. Proposed Changes & Componenti

### Core Package (`src/agricola/`)

#### [NEW] [`src/agricola/strategy/roi_crop.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/roi_crop.py)
* Implementazione della classe `ROICropAgent`.
* Metodo `select_best_crop(state: GameState)` per calcolare il ROI giornaliero sulle 5 colture e scegliere la migliore dato il capitale disponibile.
* Esecuzione del ciclo dinamico di acquisto, semina, irrigazione e vendita per la coltura selezionata.

#### [MODIFY] [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py)
* Aggiornamento dell'entrypoint per utilizzare `ROICropAgent` anziché `CarrotLoopAgent`.

#### [MODIFY] [`scripts/build_submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/build_submission.py)
* Aggiornamento del bundler per incorporare la classe `ROICropAgent` nel file standalone `submission/submission.py`.

---

## 7. Verification Plan & Comparabilità E01 $\rightarrow$ E02

Il confronto avverrà mediante la stessa suite di metriche consolidate in E01 (`results/e01_baseline.json` vs `results/e02_roi_crop.json`):

| Metrica | Baseline E01 (30 Episodi) | Target Sperimentale E02 | Note di Confronto |
| :--- | :---: | :---: | :--- |
| **Completion Rate (%)** | **100.00%** | **100.00%** | Nessuna regressione ammessa |
| **Disqualification Rate (%)** | **0.00%** | **0.00%** | Nessuna squalifica o errore ammesso |
| **Win Rate vs `starter` (%)** | **0.00%** (100% Draw) | $> \mathbf{90.00\%}$ | Verifica superamento dello starter |
| **Overall Win Rate (%)** | **66.67%** (20W/0L/10D) | $> \mathbf{95.00\%}$ | Incremento vittorie complessive |
| **Mean Final Money ($)** | **$3578.80 ± $206.65** | $> \mathbf{4500.00 \$\$}$ | Valutazione impatto economico ROI |
| **Agent Mean Turn Latency** | **0.0142 ms/turno** | $< \mathbf{0.1 \text{ ms/turno}}$ | Latenza decisionale contenuta |
