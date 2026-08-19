# Implementation Plan - Kaggriculture Agent (E01)

Questo documento definisce l'architettura iniziale, la prima baseline semplice, la modalità di esecuzione e valutazione locale e il sistema di tracciamento delle metriche per la competizione Kaggle **Kaggriculture**.

---

## 1. Studio della Competizione e dell'Ambiente

### Overview della Competizione
* **Obiettivo**: Massimizzare il capitale finale (money/net worth) di un'azienda agricola al termine di una stagione di 30 giorni di gioco.
* **Durata episodio**: 30 giorni $\times$ 24 ore/turno = **720 turni totali**.
* **Tipo di gioco**: Simulazione economica turn-based 1v1 simmetrica tra 2 agenti (Player 0 e Player 1).
* **Vincoli temporali**:
  * `actTimeout`: 1.0 secondo per turno.
  * `remainingOverageTime`: 60.0 secondi di overage budget cumulativo per l'intero episodio.
  * `runTimeout`: 1200 secondi totali per l'episodio.

### Stato Iniziale del Gioco
* Ogni giocatore parte con **3000.0 $** di capitale liquido.
* Griglia 10x10: 1 solo quadrante sbloccato all'inizio (**NW**, 5x5 tile giocabili; i restanti quadranti NE, SW, SE sono inizialmente "LOCKED").
* Contadino (Farmer) posizionato alle coordinate iniziali `(4, 4)`.
* Magazzino (Shed) vuoto (capacità 100 unità).
* Inventario semi vuoto.

---

## 2. Requisiti per una Submission Valida

Una submission valida per Kaggle deve soddisfare i seguenti requisiti:
1. **File unico Python** (es. `submission.py`) autocontenuto.
2. Definizione di una funzione top-level con la seguente firma:
   ```python
   def agent(observation, configuration):
       ...
       return {
           "farmer": ["ACTION", ...],
           "hands": [ ["ACTION", ...], ... ],
           "market": [ ["ORDER_TYPE", "ITEM", amount], ... ]
       }
   ```
3. Risposta entro 1.0s per turno senza sollevare eccezioni non gestite.
4. Output formattato secondo lo schema JSON atteso dall'ambiente `kaggle-environments`.

---

## 3. Interfaccia dell'Agente: Observation & Action Space

### Observation (`observation`)
L'agente riceve ad ogni turno un dizionario contenente:
* **Informazioni temporali e stato generale**:
  * `step` (0..719), `day` (0..29), `hour` (0..23), `player` (0 o 1).
  * `remainingOverageTime`: secondi di overage residui.
* **Stato delle fattorie (`farms`)**:
  * `farms[player]["money"]`: capitale liquido disponibile.
  * `farms[player]["tiles"]`: griglia 10x10 contenente lo stato di ogni casella (`null` se vuota, `"LOCKED"` se bloccata, oppure dict con stato di piante/animali).
  * `farms[player]["farmer"]`: coordinate `[x, y]` del contadino.
  * `farms[player]["hands"]`: lista di aiutanzi (farm hands) assunti.
  * `farms[player]["unlocked_quadrants"]`: es. `["NW"]`.
* **Inventario privato (`private`)**:
  * `shed`: quantitativo di risorse stoccate (colture e prodotti animali: `WHEAT`, `CARROT`, `TOMATO`, `STRAWBERRY`, `MELON`, `EGG`, `MILK`, `WOOL`, `FERTILIZER`, ecc.).
  * `seeds`: semi posseduti per ciascuna coltura.
* **Mercato e Città (`market`, `town`)**:
  * `market["prices"]`: prezzi correnti di acquisto e vendita.
  * `market["inventory"]`: disponibilità del mercato.
  * `town["unlocked_shops"]`: negozi sbloccati nel centro cittadino.

### Action Space (`actions`)
Ad ogni turno l'agente restituisce una struttura con tre liste di azioni:
1. **Azioni Contadino (`farmer`)**:
   * Movimento: `["MOVE", "N"|"S"|"E"|"W"]`
   * Gestione colture: `["PLANT", CROP_NAME]`, `["WATER"]`, `["HARVEST"]`, `["FERTILIZE"]`, `["CLEAR"]`
   * Animali e terreno: `["PLACE_ANIMAL", ANIMAL_NAME]`, `["BUY_LAND", QUADRANT]`, `["HIRE"]`
   * Inattività: `["PASS"]`
2. **Azioni Braccianti (`hands`)**: lista di liste di azioni per ogni bracciante.
3. **Ordini di Mercato (`market`)**:
   * `["BUY_SEED", CROP_NAME, QUANTITY]`
   * `["BUY_FERTILIZER", QUANTITY]`
   * `["BUY_ANIMAL", ANIMAL_NAME, QUANTITY]`
   * `["SELL", PRODUCT_NAME, QUANTITY]`

---

## 4. User Review Required

> [!IMPORTANT]
> **Scelta del runtime Python**: L'installazione di `kaggle-environments` su Windows con Python 3.14 falliva a causa della mancanza di `distutils` in Pygame. È stato quindi creato un ambiente virtuale isolato `.venv` basato su **Python 3.12**, perfettamente compatibile con le wheel precompilate di `kaggle-environments` e `pygame`.

> [!NOTE]
> **Approccio iterativo**: In questa prima fase E01 definiremo esclusivamente la baseline minima (`RuleBasedBaseline`), l'infrastruttura di progetto e la suite di valutazione locale. La ricerca di strategie avanzate (es. ottimizzazione del ROI, pianificazione temporale, arbitraggio sul mercato) avverrà nelle iterazioni successive.

---

## 5. Proposed Changes & Repository Structure

Proponiamo la seguente struttura modulare per il repository:

```text
kaggriculture-agent/
├── .venv/                      # Ambiente virtuale Python 3.12 (già creato)
├── pyproject.toml              # Definizione dipendenze e configurazione ruff/pytest
├── README.md                   # Documentazione generale del progetto
├── docs/                       # Documentazione esperimenti e registri
│   ├── EXPERIMENT_LOG.md
│   ├── PROJECT_STATE.md
│   └── prompts/
├── src/
│   └── agricola/               # Pacchetto principale dell'agente
│       ├── __init__.py
│       ├── agent.py            # Entry point ufficiale Kaggle: agent(obs, config)
│       ├── baseline/
│       │   ├── __init__.py
│       │   └── carrot_loop.py  # Baseline semplice basata su loop Carrot
│       ├── core/
│       │   ├── __init__.py
│       │   ├── state.py        # Wrapper per parsing e interrogazione pulita dello stato
│       │   └── actions.py      # Builder e validatore delle azioni
│       └── evaluation/
│           ├── __init__.py
│           └── runner.py       # Runner per simulazioni locali e benchmark
├── submission/
│   └── submission.py           # Script unico compilato per il submit su Kaggle
├── tests/
│   ├── __init__.py
│   ├── test_baseline.py        # Test di completamento partita e assenza errori
│   └── test_submission.py      # Test di validità del file di submission
├── scripts/
│   ├── run_eval.py             # CLI per eseguire simulazioni locali vs agenti reference
│   └── build_submission.py     # Script di bundling per generare submission/submission.py
└── results/                    # Log e metriche JSON delle simulazioni locali
```

---

## 6. Componenti Principali

### 1. `src/agricola/core/state.py`
Fornisce una vista orientata agli oggetti o tramite strutture dati pulite sopra il dict `observation`.
* Traduzione delle coordinate e griglia dei terreni (`tiles`).
* Verifica rapida di risorse nel magazzino, semi e liquidità.
* Calcolo dell'età della pianta e verifica dello stato d'irrigazione (`watered_today`).

### 2. `src/agricola/baseline/carrot_loop.py` (`CarrotLoopAgent`)
Una baseline deterministica, semplice e priva di errori:
* **Mercato**:
  * Se nel magazzino sono presenti carote harvestate (`shed["CARROT"] > 0`), vende immediatamente tutte le carote.
  * Se i semi di carota sono esauriti (`seeds["CARROT"] == 0`) e la liquidità è sufficiente ($\ge 35$), acquista 1 seme di carota.
* **Contadino**:
  * Se la casella corrente è vuota e abbiamo almeno 1 seme $\rightarrow$ `["PLANT", "CARROT"]`.
  * Se la casella ha una pianta di carota pronta per il raccolto ($age \ge max\_yield\_day$) $\rightarrow$ `["HARVEST"]`.
  * Se la casella ha una pianta di carota non ancora innaffiata oggi $\rightarrow$ `["WATER"]`.
  * Altrimenti $\rightarrow$ `["PASS"]`.

### 3. `src/agricola/agent.py`
Modulo bridge che espone la funzione `agent(observation, configuration)` richiamata dal runner Kaggle. Inizializza l'agente ed esegue il dispatch.

### 4. `src/agricola/evaluation/runner.py` & `scripts/run_eval.py`
Infrastruttura per simulare partite locali in parallelo o sequenziali.
* Agenti avversari di riferimento supportati nativamente da `kaggle-environments`:
  * `'pass'` (agente inattivo)
  * `'random'` (agente con azioni casuali)
  * `'starter'` (agente starter di Kaggle)
* Esegue N partite con scambio di posizione (Player 0 vs Player 1 e Player 1 vs Player 0) per eliminare il bias di primo turno.
* Calcola metriche aggregate e salva i dettagli in formato JSON sotto `results/`.

### 5. `scripts/build_submission.py` & `tests/test_submission.py`
Standardizza l'esportazione del codice in un unico file `submission/submission.py` ed esegue un test end-to-end con `kaggle_environments` per verificare che la submission sia accettata senza errori.

---

## 7. Dipendenze del Progetto

* `kaggle-environments` ($\ge 1.32.7$): ambiente di simulazione ufficiale.
* `python` ($3.12$): versione raccomandata nell'ambiente virtuale `.venv`.
* `pytest` ($\ge 8.0$): framework di testing unitario e integration test.
* `pandas`, `numpy`: manipolazione e aggregazione metriche.

Tutte le dipendenze principali sono già state installate ed esaminate con successo in `.venv`.

---

## 8. Modalità di Esecuzione Locale e Test

### Esecuzione Singola Simulata
```bash
.\.venv\Scripts\python.exe -c "import kaggle_environments; env = kaggle_environments.make('kaggriculture'); env.run(['src/agricola/agent.py', 'starter']); print(env.render(mode='text'))"
```

### Benchmark di Valutazione Locale
```bash
.\.venv\Scripts\python.exe scripts/run_eval.py --agent src/agricola/agent.py --opponents pass,random,starter --episodes 10 --output results/e01_baseline.json
```

### Suite di Test Automatizzati
```bash
.\.venv\Scripts\pytest tests/
```

---

## 9. Metriche da Raccogliere

Per ogni iterazione e confronto benchmark, raccoglieremo le seguenti metriche quantitative in `results/*.json`:

| Metrica | Descrizione | Obiettivo E01 |
| :--- | :--- | :--- |
| **Completion Rate (%)** | Percentuale di partite completate fino al turno 720 senza eccezioni o crash | **100%** |
| **Invalid Action Rate (%)** | Percentuale di turni in cui l'azione restituita è stata rifiutabile o non valida | **0.0%** |
| **Win Rate vs Pass (%)** | Percentuale di vittorie contro l'agente inattivo | **100%** |
| **Win Rate vs Random (%)** | Percentuale di vittorie contro l'agente random | **100%** |
| **Win Rate vs Starter (%)** | Percentuale di vittorie contro lo starter agent ufficiale | $\ge \mathbf{50\%}$ |
| **Average Final Money** | Media del capitale finale (money) ottenuto al turno 720 | **$> 3500.0 \$$** |
| **Mean Latency per Turn (ms)** | Tempo medio impiegato dall'agente per turno | **$< 10 \text{ ms}$** (limite 1000ms) |

---

## 10. Passi Previsti per la Prima Iterazione (E01)

1. **Infrastruttura del repository**:
   * Creare `pyproject.toml` e file di configurazione base.
   * Creare le directory `src/agricola/`, `submission/`, `tests/`, `scripts/`, `results/`.
2. **Implementazione Core & Baseline**:
   * Implementare `src/agricola/core/state.py` per estrarre lo stato.
   * Implementare `src/agricola/baseline/carrot_loop.py`.
   * Implementare `src/agricola/agent.py`.
3. **Infrastruttura di Valutazione & Bundling**:
   * Creare lo script `scripts/build_submission.py` per generare `submission/submission.py`.
   * Creare lo script `scripts/run_eval.py` per la valutazione di benchmark.
4. **Test & Verifiche**:
   * Scrivere unit test in `tests/` per validare l'agente e la submission.
   * Eseguire il benchmark locale contro `pass`, `random`, `starter`.
   * Generare il report delle metriche sotto `results/e01_baseline.json`.
5. **Documentazione & Chiusura E01**:
   * Aggiornare `docs/PROJECT_STATE.md` ed `docs/EXPERIMENT_LOG.md` con i risultati ottenuti.

---

## 11. Principali Rischi o Aspetti da Verificare

1. **Bundling per Kaggle**: Assicurarsi che l'agente impacchettato in `submission/submission.py` contenga tutte le funzioni necessarie senza dipendenze da moduli esterni relativi alla struttura del repository local.
2. **Timeout e Latenza**: Verificare che l'elaborazione dello stato non superi mai 1 secondo per turno anche con griglie o dati di mercato più ampi.
3. **Stabilità contro anomalie dello stato**: Garantire che l'agente gestisca con grazia risposte inattese (es. soldi insufficienti per gli acquisti o magazzino pieno) evitando eccezioni non catturate.

---

## Verification Plan

### Automated Tests
* `.\.venv\Scripts\pytest tests/`: esecuzione di tutti i test unitari e di integrazione.
* Esecuzione di `scripts/build_submission.py` seguita da test di simulazione con `kaggle_environments` per verificare la submission.

### Manual Verification
* Verifica visiva dell'output generato da `scripts/run_eval.py`.
* Controllo dell'integrità del file `submission/submission.py` generato.
* Aggiornamento del registro esperimenti in `docs/EXPERIMENT_LOG.md`.
