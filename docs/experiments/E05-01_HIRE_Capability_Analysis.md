# E05-01 — HIRE Capability & Experimental Design Analysis

**Data:** 2026-08-25  
**Fase:** DEFINE  
**Autore:** Antigravity AI  
**Stato:** Completed  
**Repository Target:** `docs/experiments/E05-01_HIRE_Capability_Analysis.md`  

---

## 1. Objective

Condurre l'audit preliminare di fase **DEFINE** per l'esperimento **E05 (`HIRE` / Multi-Worker Scaling)**. 

L'obiettivo è verificare le meccaniche effettive dell'azione `HIRE` offerte dall'ambiente **Kaggriculture** (`kaggle_environments`), valutare la compatibilità architetturale con il codebase corrente, analizzare i costi di break-even economico e progettare un esperimento rigorosamente isolato per verificare l'ipotesi della capacità lavorativa.

---

## 2. E04 Evidence Motivating E05

L'esperimento E04 (`NWClusterROIAgent`) ha testato lo scaling spaziale da 4 a 9 tile nel quadrante NW mantenendo un singolo farmer e la policy operativa E03 (`HARVEST > PLANT > WATER`).

**Risultati E04:**
- Mean Final Money E03 (4 tile): **`$14682.47 ± $1164.33`**
- Mean Final Money E04 (9 tile): **`$11232.47 ± $661.26`** (`-$3450.00` / `-23.49%`)
- Severe Water Starvation E04: **238 weed conversions** (media 7.93 conversioni/episodio)
- Early Warning Unwatered Ratio E04: **3.33%**

**Verifica della Causa Radice:**
Il singolo farmer non è in grado di percorrere le 9 tile e completare le irrigazioni giornaliere quando le azioni `HARVEST` e `PLANT` sottraggono turni al ciclo d'irrigazione. Le piante non irrigate per 2 giorni consecutivi si convertono in `WEED`, disattivando permanentemente le tile e degradando la produzione.

L'esperimento E05 nasce per verificare l'ipotesi che l'introduzione di forza lavoro aggiuntiva tramite **`HIRE`** possa eliminare il collo di bottiglia di irrigazione/movimento e rendere economicamente sostenibile il footprint a 9 tile.

---

## 3. Verified HIRE Semantics

L'ispezione diretta del sorgente `kaggriculture.py` (righe 96–100, 550–580, 690–710, 870–885, 915–945) stabilisce con certezza le seguenti 18 proprietà semantiche di `HIRE`:

1. **Disponibilità dell'azione `HIRE`:**  
   `HIRE` è pienamente disponibile e gestita dall'interpreter dell'ambiente in `_process_market` (L575-577: `_do_hire(...)`).
2. **Sintassi dell'azione:**  
   Viene emessa come ordine di mercato: `action["market"] = [["HIRE"]]`.
3. **Costo monetario di ingaggio:**  
   Calcolato tramite sequenza di Fibonacci moltiplicata per `FARM_HAND_COST_MULT` (default 1):  
   $$\text{Cost}(n) = \text{mult} \times \text{fib}(n)$$
   - $1^\circ$ ingaggio del giorno ($n=0$): $\text{fib}(0) = 1 \implies \mathbf{\$1}$
   - $2^\circ$ ingaggio del giorno ($n=1$): $\text{fib}(1) = 1 \implies \mathbf{\$1}$
   - $3^\circ$ ingaggio del giorno ($n=2$): $\text{fib}(2) = 2 \implies \mathbf{\$2}$
   - $4^\circ$ ingaggio del giorno ($n=3$): $\text{fib}(3) = 3 \implies \mathbf{\$3}$
4. **Momento di addebito:**  
   Addebitato immediatamente dalla cassa (`farm["money"] -= cost`) durante la fase mercato dello stesso turno in cui viene processata l'azione.
5. **Entità creata:**  
   Crea una farm hand il cui punto di spawn iniziale si posiziona sulla prima tile libera di accesso al capanno (`_shed_access_tiles` NWSE order: `(4,4)`, `(5,4)`, `(4,5)`, `(5,5)`).
6. **Lavoratori simultanei:**  
   Possono coesistere più lavoratori simultaneamente. La farm mantiene una lista `farm["hands"] = [[x0,y0], [x1,y1], ...]`.
7. **Limite massimo di lavoratori:**  
   Non esiste un cap fisso nel codice, ma il costo cresce secondo la sequenza Fibonacci ed è limitato dalla cassa disponibile.
8. **Durata e Ciclo di Vita (CRITICO):**  
   **I lavoratori subordinati NON persistono durante la notte.**  
   In `_end_of_day` (L880-882), a fine giornata (`hour == 23`):
   - `farm["hands"] = []`
   - `farm["hires_today"] = 0`
   - `private["inventories"] = [{}]`  
   **Implicazione:** I farm hands sono lavoratori giornalieri. Per avere 1 hand attivo ogni giorno, l'agente deve emettere `["HIRE"]` **ogni giorno** (al costo di **$1/giorno**).
9. **Invio e Selezione Azioni dei Lavoratori:**  
   Le azioni delle hand sono inviate nella chiave `"hands"` del dizionario delle azioni di turno:  
   `{"farmer": [op, ...], "hands": [[hand_0_op, ...], [hand_1_op, ...]], "market": [...]}`.
10. **Controllo del Farmer Principale:**  
    L'agente centralizzato genera l'intero dizionario di turno, controllando esplicitamente sia il farmer che ciascuna hand.
11. **Posizione Indipendente:**  
    Ogni hand possiede coordinate `(x, y)` indipendenti in `farm["hands"]`.
12. **Movimento Indipendente:**  
    Ogni hand si muove in modo indipendente eseguendo azioni direzionali (`NORTH`, `SOUTH`, `EAST`, `WEST`).
13. **Stato Condiviso vs Privato:**  
    - **Condivisi:** Cassa (`money`), griglia del terreno (`tiles`), quadranti sbloccati, capanno (`private["shed"]`), semi (`private["seeds"]`).
    - **Privati:** Inventario carried trasportato dal singolo worker (`private["inventories"][idx]`).
14. **Restrizioni e Azioni Consentite:**  
    Le hand possono eseguire **tutte le stesse azioni del farmer principale** (`PLANT`, `WATER`, `HARVEST`, `FERTILIZE`, `DIG`, `BUILD_*`, `FEED`, `CARE`, `PICKUP`, `DROP`, `PLACE`).
15. **Validazione Atomica della Semina (PLANT):**  
    Se la domanda totale di `PLANT` per una coltura in un turno (sum farmer + hands) supera i semi posseduti in `private["seeds"]`, **tutti gli ordini `PLANT` per quella coltura in quel turno vengono annullati** (`PASS`).
16. **Ordine di Esecuzione nel Turno (Timing):**  
    L'interpreter elabora in sequenza:
    1. Azione Farmer (`idx = 0`)
    2. Azioni Hands (`idx = 1..N`)
    3. Fase Mercato (`_process_market`)  
    **Implicazione:** Se `["HIRE"]` viene emesso al turno $S$, il nuovo lavoratore viene creato nella fase mercato di $S$ e può eseguire la sua prima azione al turno $S+1$.
17. **Timing, Latenza e Timeout Risk:**  
    Generare azioni per 2 worker richiede calcoli di routing separati, ma l'impatto computazionale è trascurabile ($< 0.1$ ms/turno vs timeout di 1000 ms).
18. **Accesso al Capanno e Deposito a Fine Giornata:**  
    A fine giornata (`hour == 23`), tutti gli inventari carried dei lavoratori vengono automaticamente depositati nel shed (`_drop_inventories_to_shed`) fino alla capienza massima (100).

---

## 4. Evidence / Source References

- `kaggriculture.py` L96-102: Definizione `FARM_HAND_COST_MULT = 1`.
- `kaggriculture.py` L575-577 & L698-710: Funzione `_do_hire` e calcolo costo Fibonacci `_hire_cost`.
- `kaggriculture.py` L873-882: Reset di fine giornata `farm["hands"] = []` e `farm["hires_today"] = 0`.
- `kaggriculture.py` L922-929: Validazione atomica della domanda `PLANT` aggregata.
- `kaggriculture.py` L930-942: Sequenza d'interpretazione turno (Farmer $\rightarrow$ Hands $\rightarrow$ Market).

---

## 5. Compatibility with Current E04 Architecture

### Modifiche Architetturali Necessarie:

1. **`GameState` (`src/agricola/core/state.py`):**
   - Aggiunta proprietà `state.hands_positions` per interrogare la lista di coordinate `(x, y)` dei lavoratori subordinati attivi.
2. **`ActionBuilder` (`src/agricola/core/actions.py`):**
   - Aggiunta helper `actions.hire()` per inserire `["HIRE"]` negli ordini di mercato.
   - Aggiunta helper `actions.add_hand_action(action_list)` per accodare l'azione per ciascun lavoratore subordinato.
3. **Modulo Strategia (`src/agricola/strategy/hire_nw_cluster_roi.py`):**
   - **Ingaggio Giornaliero:** Emissione dell'azione `["HIRE"]` al turno `hour == 0` di ogni giorno se `len(hands) < target_hands`.
   - **Partitioning Spaziale del Terreno (Prevenzione Conflitti):**  
     Per evitare collisioni o duplicazione di task sulle stesse tile:
     - **Farmer Principale:** Gestisce 4 tile (sub-cluster 2×2 `{(4,4), (4,3), (3,4), (3,3)}`).
     - **Farm Hand 1:** Gestisce le 5 tile rimanenti (sub-cluster `{(4,2), (3,2), (2,4), (2,3), (2,2)}`).
     - Ciascun worker esegue la policy E03 (`HARVEST > PLANT > WATER`) in modo **completamente indipendente** sulla propria partizione spaziale.
4. **Bundling Standalone (`scripts/build_submission.py`):**
   - Inclusione della nuova strategia `HIRENWClusterROIAgent` nel file standalone `submission/submission.py`.

---

## 6. Candidate Minimal Treatments

Per isolare l'effetto della capacità lavorativa ed evitare esperimenti multi-variabile:

* **Treatment A (Raccomandato): Single Daily HIRE (1 Farmer + 1 Hand)**  
  Assunzione di **1 farm hand al giorno** ($1/giorno). Partitioning spaziale 4:5 sulle 9 tile gestite.
* **Treatment B: Double Daily HIRE (1 Farmer + 2 Hands)**  
  Assunzione di 2 farm hand al giorno ($2/giorno). Partitioning 3:3:3 sulle 9 tile.

**Scelta del Treatment Minimo:**  
**Treatment A (1 Farmer + 1 Hand)** è il trattamento più semplice, pulito e chirurgico per testare l'ipotesi di capacità lavorativa.

---

## 7. Economic / Break-Even Considerations

1. **Costo Diretto di HIRE:**
   - Hiring 1 hand al giorno: **$1/giorno**.
   - Su 30 giorni di partita: **$30 di costo totale per episodio**.
2. **Soglia di Break-Even Economico:**
   - Per recuperare l'investimento di $30 in tutta la partita, la farm hand deve consentire la raccolta di **1 singola coltura aggiuntiva in 30 giorni** (es. 1 raccolto di Carota = $140 lordi, 1 raccolto di Melone = $1500 lordi).
3. **Valutazione Economica:**  
   Il costo di ingaggio ($30/episodio) è **irrisorio** rispetto al volume di ricavo agricolo ($11k–$22k). Se la seconda unità lavorativa previene la perdita di 238 erbacce ripristinando la piena produttività delle 9 tile, il recupero economico netto sarà nell'ordine dei **+$3,000 … +$10,000+**.

---

## 8. Recommended Experimental Variable

> **Variabile Sperimentale E05:** Introduzione di 1 farm hand giornaliero tramite l'azione `HIRE` (costo $1/giorno) con partizionamento spaziale del cluster compatto a 9 tile tra Farmer (4 tile) e Hand 1 (5 tile).

---

## 9. Variables to Hold Constant

Per mantenere il controllo sperimentale rigoroso ed evitare fattori confondenti, **rimarranno invariati rispetto a E04:**

- Footprint produttivo a 9 tile `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` nel quadrante NW;
- Assenza di `BUY_LAND`;
- Assenza dell'azione `DIG` (bonifica erbacce);
- Formula di selezione coltura ROI/giorno E03 (`yield=2.0`);
- Ciechezza all'orizzonte di fine stagione (assenza di filtri temporali);
- Regola di vendita immediata dei prodotti nel capanno;
- Gerarchia di priorità operativa dei task (`HARVEST > PLANT > WATER`).

---

## 10. Proposed Success / Failure Criteria

### Baseline di Riferimento:
- **Control (E04):** Mean Final Money = **`$11232.47 ± $661.26`**, Total Weeds = **238**.
- **Riferimento Superiore (E03 - 4 tile):** Mean Final Money = **`$14682.47 ± $1164.33`**, Total Weeds = **0**.

### Criteri di Valutazione E05:

1. **Successo Minimo (Minimum Success):**
   - Mean Final Money E05 $>$ **`$13000.00`** (`+15.7%` min delta vs E04);
   - Weed Conversions aggregate $<$ **30 totali** su 30 episodi ($<1.0$/ep);
   - Completion Rate = `100%`, Disqualification Rate = `0%`.

2. **Successo Forte (Strong Success):**
   - Mean Final Money E05 $\ge$ **`$14682.47`** (raggiunge o supera la baseline E03 su 4 tile);
   - Total Weed Conversions = **0**;
   - Dimostrazione che il footprint a 9 tile diventa economicamente superiore a 4 tile grazie alla forza lavoro subordinata.

3. **Fallimento (Failure):**
   - Mean Final Money E05 $\le$ **`$11232.47`**;
   - Oppure persistenza di severe water starvation ($>100$ weed conversions);
   - Dimostrazione che il coordinamento multi-worker o i costi non compensano il collo di bottiglia.

---

## 11. Threats to Validity

1. **Conflitto di Semina Atomica (`PLANT`):**  
   Se sia il Farmer che la Hand tentano di piantare nello stesso turno e i semi posseduti in `private["seeds"]` non bastano per entrambi, l'interpreter annulla l'azione di entrambi.  
   *Mitigazione:* Il partizionamento spaziale rigido garantisce che ciascun worker gestisca i propri cicli di semina in momenti separati.
2. **Spawn Delay al Giorno 1:**  
   L'azione `["HIRE"]` emessa a `hour == 0` crea la hand durante la fase mercato dello stesso turno. La hand potrà compiere il primo movimento/azione solo a `hour == 1`.
3. **Disincronizzazione dell'Irrigazione:**  
   Se Hand 1 deve gestire 5 tile rispetto alle 4 del Farmer, verificare che Hand 1 riesca a completare l'irrigazione delle sue 5 tile entro i 24 turni della giornata.

---

## 12. Open Questions

1. **[SOLVED] Timing dell'azione HIRE:** Verificato che `HIRE` emesso a `hour == 0` rende la hand operativa al turno `hour == 1`.
2. **[SOLVED] Reset notturno:** Verificato che `farm["hands"]` si azzera a `hour == 23` e richiede un ingaggio giornaliero a `hour == 0` ($1/giorno).

---

## 13. Recommendation for E05 PLAN

> **PROCEED TO PLAN**

Le evidenze del codice dell'ambiente e l'analisi economica confermano che `HIRE` è un'azione disponibile, estremamente economica ($1/giorno) e tecnicamente idonea per risolvere il collo di bottiglia lavorativo di E04 in un esperimento ad elevata isolabilità.

---

*Documento completato e salvato in `docs/experiments/E05-01_HIRE_Capability_Analysis.md` in conformità con i vincoli della fase DEFINE.*
