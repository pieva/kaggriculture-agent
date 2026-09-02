# Rapporto VERIFY REVIEW E02 — Ricostruzione Baseline E01 e Valutazione Impatto E02

Questo documento costituisce l'evidenza persistente della fase di **VERIFY REVIEW indipendente** dell'evoluzione **E02 (`ROICropAgent`)**, condotta tramite Antigravity.

---

## 1. Ricostruzione Indipendente dei Dati Grezzi della Baseline E01

Dall'elaborazione diretta dell'intero dataset di 30 episodi conservato nel file [`experiments/archive/e01/artifacts/baseline.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e01/artifacts/baseline.json):

### 1.1 I 30 Valori del Capitale Finale (`my_reward`)
- **vs `pass` (10 episodi)**: `[3421.0, 3532.0, 4506.0, 3441.0, 3637.0, 3474.0, 3421.0, 3441.0, 3649.0, 3421.0]` (Somma = 35943.0)
- **vs `random` (10 episodi)**: `[3524.0, 3576.0, 3522.0, 3597.0, 3843.0, 3627.0, 3714.0, 3421.0, 3482.0, 3464.0]` (Somma = 35770.0)
- **vs `starter` (10 episodi)**: `[3579.0, 3608.0, 3690.0, 3503.0, 3536.0, 3539.0, 3503.0, 3425.0, 3390.0, 3543.0]` (Somma = 35316.0)

### 1.2 Medie per Avversario
- **vs `pass`**: $\text{Somma} = 35943.0 / 10 \rightarrow \mathbf{\$3594.30}$
- **vs `random`**: $\text{Somma} = 35770.0 / 10 \rightarrow \mathbf{\$3577.00}$
- **vs `starter`**: $\text{Somma} = 35316.0 / 10 \rightarrow \mathbf{\$3531.60}$

### 1.3 Calcolo della Media sui 30 Episodi
$$\text{Somma Totale} = 35943.0 + 35770.0 + 35316.0 = 107029.0$$
$$\text{Mean Final Money E01} = \frac{107029.0}{30} = 3567.6333... \rightarrow \mathbf{\$3567.63}$$

### 1.4 Statistiche di Sintesi E01
- **Median Final Money E01**: $\mathbf{\$3528.00}$
- **Deviazione Standard Popolazione (`ddof=0`)**: $\mathbf{\pm \$201.93}$ ($201.92878...$)
- **Deviazione Standard Campionaria (`ddof=1`)**: $\mathbf{\pm \$205.38}$ ($205.38080...$)

---

## 2. Analisi Epistemica dei Valori Precedentemente Riportati (`$3578.80` e `$206.65`)

### 2.1 Origine di `$3578.80`
- È matematicamente verificabile che il valore `$3578.80` si ottiene dalla media dei tre valori aggregati precedentemente documentati:
  $$\frac{3594.30 + 3610.50 + 3531.60}{3} = \frac{10736.4}{3} = 3578.80$$
- Tuttavia, non è verificabile dai dati grezzi persistenti attualmente conservati in `experiments/archive/e01/artifacts/baseline.json` la ragione per cui il valore per `random` fosse stato precedentemente indicato pari a `$3610.50` (mentre i 10 episodi conservati sul disco danno come media `$3577.00`).
- L'ipotesi che tale cifra derivasse da un run intermedio precedente costituisce una possibile spiegazione, ma non una certezza dimostrata in assenza dei dati grezzi di quel run.

### 2.2 Origine di `$206.65`
- Sui 30 valori effettivamente presenti in `experiments/archive/e01/artifacts/baseline.json`, la deviazione standard della popolazione (`ddof=0`) è **`$201.93`** e la deviazione standard campionaria (`ddof=1`) è **`$205.38`**.
- Di conseguenza, `$206.65` **non è la deviazione standard campionaria dei 30 episodi E01 attualmente conservati**.
- Tale cifra potrebbe derivare da un diverso insieme di osservazioni o da un precedente calcolo, ma non può essere attribuita con certezza ad uno specifico run in assenza dell'evidenza grezza persistente.

---

## 3. Baseline E01 Definitiva e Ricalcolo del Confronto E01 $\rightarrow$ E02

### 3.1 Baseline E01 Definitiva per il Benchmark
Per garantire la massima coerenza metodologica, il riferimento quantitativo per la baseline E01 si basa esclusivamente sui 30 episodi conservati sul disco con deviazione standard campionaria (`ddof=1`):

$$\mathbf{\text{Mean Final Money E01} = \$3567.63 \pm \$205.38}$$

### 3.2 Confronto Quantitativo E01 $\rightarrow$ E02
Utilizzando il valore verificato per E02 dai dati grezzi di [`experiments/archive/e02/artifacts/roi_crop.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e02/artifacts/roi_crop.json):
- **Mean Final Money E02**: **`$5857.17`** ($5857.1666...$)
- **Sample Std Dev E02 (`ddof=1`)**: **`± $132.37`** ($132.3688...$)
- **Population Std Dev E02 (`ddof=0`)**: **`± $130.14`** ($130.1440...$)

#### Incrementi Ricalcolati:
$$\text{Incremento Assoluto} = 5857.1666... - 3567.6333... = \mathbf{+\$2289.53}$$
$$\text{Incremento Percentuale} = \frac{2289.5333...}{3567.6333...} \times 100 = \mathbf{+64.18\%}$$

*(Tra le cifre discusse nelle prime stime, **+64.18%** è il valore matematicamente corretto calcolato dai file grezzi di benchmark).*

#### Esito vs `starter`:
- **E01**: 100.00% Pareggi (0 Vittorie, 10 Pareggi, 0 Sconfitte)
- **E02**: **100.00% Vittorie** (10 Vittorie, 0 Pareggi, 0 Sconfitte)

---

## 4. Valutazione dell'Isolamento Sperimentale e dell'Ipotesi E02

### 4.1 Isolamento Sperimentale
**`PASSED WITH OBSERVATIONS`**

**Motivazione dell'osservazione**: L'aggiornamento dei parametri `CROPS` in `src/agricola/core/state.py` ha allineato la configurazione locale con i valori dell'engine `kaggriculture`. Poiché per `CARROT` la durata di crescita max_yield_day=3 è rimasta invariata e l'agente baseline E01 controllava `money >= seed` ($3000 \ge 20$), il comportamento di `CarrotLoopAgent` rimane **100% invariato** ed il confronto diretto E01 $\rightarrow$ E02 è pienamente valido.

### 4.2 Valutazione dell'Ipotesi E02
**`SUPPORTATA nelle condizioni sperimentali testate`**

L'ipotesi che la selezione dinamica ROI aumenti il capitale finale ed elimini il pareggio con lo `starter` agent è pienamente supportata dai dati di benchmark nei 30 episodi testati (+64.18% di capitale finale, 100% di vittorie).

---

## 5. Elenco dei Documenti da Correggere Successivamente (senza modificarli in questa fase)

Nessun file di progetto o documentazione è stato modificato durante questa REVIEW. Nelle fasi successive verranno aggiornati:
1. [`docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md): aggiornare baseline E01 a `$3567.63 \pm $205.38` ed incremento a `+64.18%`.
2. [`docs/PROJECT_STATE.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/PROJECT_STATE.md): aggiornare il valore medio E01 a `$3567.63` ed esito E02.
3. [`docs/EXPERIMENT_LOG.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/EXPERIMENT_LOG.md): registrare la conclusione di E02 ed i valori definitivi di benchmark.
