# E04-01 — Competitive Gap Analysis

**Data:** 2026-08-25  
**Fase:** DEFINE / Investigation  
**Autore:** Antigravity AI  
**Stato:** Completed  
**Repository Target:** `docs/experiments/E04-01_Competitive_Gap_Analysis.md`  

---

## Executive Summary

L'esperimento E03 (`MultiTileROIAgent`) ha dimostrato la fattibilità e l'efficacia dello scaling produttivo multi-tile su un cluster compatto 2×2, registrando nel benchmark locale controllato un incremento del **+150.68%** nel Mean Final Money (`$5857.17` → `$14682.47`) con Win Rate del **100%** su 30 episodi.

Tuttavia, l'evidenza osservata sulla piattaforma Kaggle evidenzia un miglioramento competitivo reale molto più contenuto:
* **E02 Kaggle Skill Rating osservato:** `285.1` (con picco iniziale `600.0`);
* **E03 Kaggle Score/Rating osservato:** `294.4` (posizione leaderboard circa `#5642`).

Il presente documento costituisce l'audit completo di **Competitive Gap Analysis** per identificare le disconnessioni strutturali tra il benchmark locale, la policy decisionale di E03 e l'ambiente reale di simulazione **Kaggriculture** (`kaggle_environments`).

---

## 1. Environment Capability Inventory

L'ispezione diretta del sorgente dell'ambiente (`kaggle_environments/envs/kaggriculture/kaggriculture.py`) e delle sue specifiche JSON rivela un ambiente ricco e multi-sfaccettato con 100 tile per farm, 4 quadranti 5×5, lavoratori aggiuntivi (*farm hands*), consumo dinamico della città (*town shops*) ed economia degli animali/fertilizzanti.

### 1.1 Observation Space Audit

| Elemento di Osservazione | Descrizione e Struttura | Stato di Utilizzo in E03 |
| :--- | :--- | :--- |
| `step` / `day` / `hour` | Progresso temporale (0..720 step, 0..30 giorni, 0..24 ore/giorno). | **Parzialmente Utilizzato**: `day` è usato solo per calcolare l'età della pianta (`day - planted_day`). Il tempo residuo dell'episodio è **completamente ignorato**. |
| `farms[player].money` | Capitale liquido disponibile per il player. | **Utilizzato**: Usato per verificare l'affordabilità dei semi (`money >= seed_cost`). |
| `farms[player].farmer` | Coordinate `(x, y)` del farmer principale. | **Utilizzato**: Usato per il calcolo delle distanze Manhattan e il routing del movimento. |
| `farms[player].tiles` | Griglia 10×10 (100 tile) del terreno della farm. | **Parzialmente Utilizzato**: E03 ispeziona solo **4 tile** sulle 25 sbloccate nel quadrante iniziale NW (e 100 totali). Le restanti 21 tile sono ignorate. |
| `farms[player].hands` | Posizioni dei lavoratori subordinati (*farm hands*). | **Ignorato**: E03 non assume farm hands, la lista rimane vuota. |
| `farms[player].unlocked_quadrants` | Lista dei quadranti sbloccati (default `["NW"]`). | **Ignorato**: E03 non acquista mai nuovi quadranti (`NE`, `SW`, `SE`). |
| `private.shed` | Inventario dei prodotti raccolti e stipati nel capanno (cap. 100). | **Utilizzato**: E03 controlla il shed ad ogni turno ed emette ordini di `SELL` per tutti i prodotti presenti. |
| `private.seeds` | Inventario dei semi posseduti per ciascuna coltura. | **Utilizzato**: E03 controlla i semi disponibili per determinare quanti semi acquistare e piantare. |
| `market.prices` | Prezzi correnti di mercato per tutti i 9 prodotti. | **Utilizzato**: E03 legge i prezzi correnti per calcolare la formula ROI/giorno. |
| `market.inventory` | Stock globale di ciascun prodotto nel mercato (default $I_0 = 10000$). | **Ignorato**: E03 non osserva lo stock di mercato né l'elasticità di prezzo/curva d'offerta. |
| `town.unlocked_shops` | Lista dei negozi sbloccati in città (sblocco ogni 3gg, max 8). | **Ignorato**: E03 ignora la domanda della città, che consuma merci dal mercato creando picchi di prezzo. |
| `farms[1 - player]` | **Stato completo della farm avversaria** (money, farmer, tiles, unlocked). | **Ignorato**: E03 è **100% cieco** rispetto alle azioni, alla posizione e alla strategia dell'avversario. |
| `remainingOverageTime` | Budget di tempo residuo (secondi banked). | **Ignorato**. |

---

### 1.2 Action Space Audit

Le azioni in Kaggriculture sono strutturate in tre canali per turno: `{"farmer": [...], "hands": [...], "market": [...]}`.

#### Worker Actions (Farmer & Hands)
* **`NORTH`, `SOUTH`, `EAST`, `WEST`**: **Utilizzati** (Movimento Manhattan 1 step/turno).
* **`PASS`**: **Utilizzato** (Azione di default quando non ci sono task).
* **`PLANT <crop>`**: **Utilizzato** (Semina su tile vuota sbloccata).
* **`WATER`**: **Utilizzato** (Irrigazione della tile su cui si trova il worker).
* **`HARVEST`**: **Utilizzato** (Raccolta del prodotto su tile matura).
* **`DIG`**: **Mai Utilizzato** (Rimuove erbacce `WEED`, piante o strutture).
* **`FERTILIZE`**: **Mai Utilizzato** (Applica fertilizzante raddoppiando l'incremento di resa).
* **`PICKUP` / `DROP` / `PLACE`**: **Mai Utilizzati** (Manipolazione inventario worker / animali).
* **`BUILD_COOP` / `BUILD_PASTURE`**: **Mai Utilizzati** (Costruzione strutture per animali).
* **`FEED` / `CARE` / `COLLECT_FERTILIZER`**: **Mai Utilizzati** (Gestione e cura degli animali).

#### Market Actions
* **`BUY_SEED <crop> <n>`**: **Utilizzato** (Acquisto semi abbinato al conteggio tile vuote gestite).
* **`SELL <item> <n>`**: **Utilizzato** (Vendita immediata di tutti i prodotti presenti nel shed).
* **`BUY_PRODUCT <item> <n>`**: **Mai Utilizzato** (Acquisto di grano/fertilizzante dal mercato).
* **`BUY_ANIMAL <animal> <n>`**: **Mai Utilizzato** (Acquisto mucche, pecore, oche).
* **`HIRE`**: **Mai Utilizzato** (Reclutamento farm hands per il giorno a costo Fibonacci: $1, $1, $2, $3, $5, $8...).
* **`BUY_LAND`**: **Mai Utilizzato** (Sblocco quadranti aggiuntivi per $1000, $2000, $4000).

---

## 2. E03 Decision Policy Reconstruction

`MultiTileROIAgent` è configurato come una policy **singolo-worker, miope, deterministica, basata su micro-cluster spaziale 2×2**.

```
                       ┌────────────────────────────────┐
                       │  Ogni Turno (Step 0..720)      │
                       └───────────────┬────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────┐                             ┌───────────────────────┐
│ 1. Phase Mercato      │                             │ 2. Selezione Coltura  │
│ Liquida SHED          │                             │ ROI/giorno Miope      │
│ (SELL immediato)      │                             │ (assunzione yield=2.0)│
└───────────────────────┘                             └───────────┬───────────┘
                                                                  │
                                                                  ▼
                                                      ┌───────────────────────┐
                                                      │ 3. Acquisto Semi      │
                                                      │ BUY_SEED per tile     │
                                                      │ vuote gestite (max 4) │
                                                      └───────────┬───────────┘
                                                                  │
                                                                  ▼
                                                      ┌───────────────────────┐
                                                      │ 4. Priority Spaziale  │
                                                      │ HARVEST > PLANT >     │
                                                      │ WATER (Manhattan)     │
                                                      └───────────────────────┘
```

### Regole Decisionali e Criticità Identificate:

1. **Selezione della Coltura (Formula ROI/giorno):**
   $$\text{NetProfitPerDay} = \frac{(\text{SellPrice} \times 2.0) - \text{SeedPrice}}{\max(1, \text{max\_yield\_day})}$$
   * **Assunzione errata:** Hardcoda `yield_units = 2.0` per tutte le colture. Nella realtà del gioco:
     - Grano (`WHEAT`): `max_yield` = **6** (costo seme $10, giorno 4);
     - Carota (`CARROT`): `max_yield` = **4** (costo seme $20, giorno 3);
     - Melone (`MELON`): `max_yield` = **6** (costo seme $80, giorno 12);
     - Pomodoro (`TOMATO`) & Fragola (`STRAWBERRY`): colture **ongoing** (multiraccolto ricorsivo ogni 1-2 giorni dopo la maturazione).
   * **Conseguenza:** L'agente sottostima gravemente il valore economico del Melone, del Grano e delle colture ricorsive ongoing.

2. **Ciechezza all'Orizzonte Temporale (Horizon Blindness):**
   * L'agente applica la stessa regola di acquisto/semina al giorno 0 come al giorno 29 (step 710).
   * Seminare un Pomodoro (8 giorni) o una Fragola (10 giorni) al giorno 25 comporta una perdita netta pari al costo del seme, poiché la pianta non giungerà mai a maturazione prima dello step 720.

3. **Restrizione Spaziale Volontaria:**
   * L'agente gestisce esclusivamente 4 tile `{(4,4), (4,3), (3,4), (3,3)}`.
   * **21 tile sbloccate** nel quadrante NW (l'84% del terreno iniziale gratuito) e **75 tile** sull'intera mappa rimangono inutilizzate per l'intera durata dell'episodio.

4. **Assenza di Lavoro di Squadra (`HIRE`):**
   * Reclutare lavoratori aggiuntivi costa appena $1 per il primo hand e $1 per il secondo (sequenza Fibonacci). Un singolo farmer deve percorrere la griglia a piedi (1 step/tile), creando un collo di bottiglia temporale nell'irrigazione non appena le tile coltivate superano le 6-8 unità.

---

## 3. Competitive Objective Analysis

### 3.1 Distinzione tra Benchmark Locale e Valutazione Kaggle

In Kaggriculture, l'obiettivo dell'ambiente è il **Final Money al turno 720** (`reward = money`). Tuttavia, la valutazione competitiva su Kaggle obbedisce a dinamiche matchmaking (Skill Rating / Elo):

```
┌─────────────────────────────────────────┐      ┌─────────────────────────────────────────┐
│         BENCHMARK LOCALE                │      │            KAGGLE LEADERBOARD           │
├─────────────────────────────────────────┤      ├─────────────────────────────────────────┤
│ Opponente: 'starter' (bot 1-tile fixed) │      │ Opponenti: Agenti avanzati / Umani      │
│ Score E03: $14,682.47                   │      │ Score E03: Skill Rating ~294.4 (#5642)  │
│ Win Rate: 100.0%                        │      │ Strategie avversarie: 25+ tile, HIRE,   │
│ Valutazione: Assoluta vs baseline fissa │      │ ongoing multi-crop, shop exploitation   │
└─────────────────────────────────────────┘      └─────────────────────────────────────────┘
```

### 3.2 Limite Metrologico del Benchmark Locale
* `starter_agent` (definito in `kaggriculture.py` L1054) coltiva **1 sola tile di Carota**, non si muove mai e chiude la partita con circa **$3,421**.
* Qualsiasi agente che coltivi 4 tile supera il benchmark locale con un Win Rate del 100%.
* Vincere contro `starter` con $14.6k non fornisce alcuna indicazione sulla capacità di vincere contro agenti che producono **$50,000 – $100,000+** sfruttando l'intero quadrante NW o sbloccando nuovi quadranti.

---

## 4. Local vs Kaggle Divergence Analysis

Per spiegare il fenomeno per cui E03 migliora del `+150.68%` nel benchmark locale ma ottiene solo una modesta posizione su Kaggle (~294.4), analizziamo le cause fondamentali classificate secondo evidenza:

### [SUPPORTED] 1. Baseline Locale Debole (Opponent Floor)
* **Evidenza:** Ispezione di `kaggriculture.py` L1054 e `runner.py`. Gli unici opponenti locali usati sono `pass` ($0), `random` ($100) e `starter` ($3.5k).
* **Conclusione:** Il benchmark locale misura solo il superamento del minimo operativo, non la forza competitiva reale.

### [SUPPORTED] 2. Grave Sotto-Utilizzo del Terreno Iniziale (Scale Bottleneck)
* **Evidenza:** `kaggriculture.py` L158 sblocca 25 tile nel quadrante NW all'inizio della partita. E03 ne usa solo 4 (16%).
* **Conclusione:** Gli agenti competitor su Kaggle che utilizzano 12-25 tile producono un volume da 3x a 6x superiore rispetto a E03.

### [SUPPORTED] 3. Sprecato di Capitale a Fine Stagione (Horizon Waste)
* **Evidenza:** `multi_tile_roi.py` effettua acquisti e semine negli ultimi 10 giorni dell'episodio senza verificare l'orizzonte residuo.
* **Conclusione:** Capitale liquido viene convertito in semi e piante immature che valgano $0 al turno 720, riducendo il punteggio finale.

### [PLAUSIBLE] 4. Collo di Bottiglia del Singolo Lavoratore (No HIRE)
* **Evidenza:** `kaggriculture.py` L698 permette di assumere farm hands per $1. E03 usa solo 1 farmer.
* **Conclusione:** Impossibile scalare la produzione oltre 6-8 tile mantenendo l'irrigazione giornaliera senza assumere almeno 1-2 farm hands.

### [PLAUSIBLE] 5. Errore nella Stima della Resa e Sottostima delle Colture Ongoing
* **Evidenza:** `multi_tile_roi.py` hardcoda `yield=2.0`, ignorando che `WHEAT` e `MELON` producono 6 unità e `TOMATO`/`STRAWBERRY` forniscono flussi di cassa continui per tutta la stagione.
* **Conclusione:** E03 seleziona colture sub-ottimali dal punto di vista economico reale.

---

## 5. Competitive Gap Matrix

| Meccanica / Capacità | Disponibile nell'Ambiente | Utilizzata da E03 | Rilevanza Strategica | Evidenza nel Codice / Simulazione | Gap Potenziale Identificato |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Sfruttamento Quadrante NW (25 Tile)** | **Sì** (25 tile sbloccate gratis) | Parziale (4 tile 2×2: 16%) | **CRITICA** | `kaggriculture.py` L158 (`_initial_tile`) | **84% del terreno iniziale inutilizzato**. Produzione cappata a 1/6 della capacità immediata. |
| **Orizzonte Temporale End-of-Season** | **Sì** (720 step / 30 giorni) | **No** (Miope fino a step 719) | **CRITICA** | `multi_tile_roi.py` L93-122 | **Spreco di capitale negli ultimi 10 giorni** per semi/piante che non matureranno mai. |
| **Forza Lavoro Multi-Worker (`HIRE`)** | **Sì** (Costo Fibonacci: $1, $1, $2...) | **No** (0 hands assunti) | **ALTA** | `kaggriculture.py` L698 (`_do_hire`) | **Bottleneck di movimento e irrigazione**. Impossibile gestire oltre ~6 tile con 1 solo worker. |
| **Espansione Land (`BUY_LAND`)** | **Sì** (Quadranti NE, SW, SE per $1k..$4k) | **No** (Mai usata) | **ALTA** | `kaggriculture.py` L96 (`LAND_ORDER`) | Impossibilità di scalare oltre le 25 tile iniziali verso la dimensione massima (100 tile). |
| **Modello di Resa Reale (`max_yield` / Ongoing)** | **Sì** (Wheat/Melon yield 6, Tomato/Strawberry ongoing) | **No** (Hardcoded `yield=2.0`) | **ALTA** | `kaggriculture.py` L11-17 (`CROPS`) | **Sottostima delle colture ad alto rendimento** e dei flussi ricorsivi delle piante pluriennali. |
| **Consumo Città & Demand Spikes (`town.unlocked_shops`)** | **Sì** (Shop sbloccati ogni 3gg assorbono stock) | **No** (Vendita immediata spot) | **MEDIA-ALTA** | `kaggriculture.py` L103 (`SHOPS`), L728 | Perte di opportunità di profitto non sfruttando i picchi di prezzo creati dai negozi cittadini. |
| **Gestione Erbacce (`WEED` & `DIG`)** | **Sì** (Spawn 0.5%/giorno) | **No** (Ignora tile se WEED) | **MEDIA** | `kaggriculture.py` L836 (`_spawn_weeds`), L485 | Ostruzione progressiva delle tile libere da parte delle erbacce senza azione di bonifica (`DIG`). |
| **Fertilizzanti & Animali (`FERTILIZE`, `ANIMALS`)** | **Sì** (Coop/Pasture, latte, lana, uova, fertilizzante) | **No** (Mai usati) | **MEDIA** | `kaggriculture.py` L19-23 (`ANIMALS`), L475 | Mancato utilizzo di meccaniche ad alto valore aggiunto (es. raddoppio rese tramite fertilizzante). |
| **Adattamento Strategico all'Avversario** | **Sì** (Stato opp. visibile in `farms[1-p]`) | **No** (100% blind) | **MEDIA** | `state.py` L29 (`opponent_farm`) | Nessuna reazione se l'avversario inonda lo stesso mercato o satura un prodotto. |
| **Metrologia di Benchmark Locale** | **Sì** (`runner.py`) | Parziale (Solo vs `starter`) | **CRITICA** | `runner.py` L134-188 | **Falso senso di ottimalità**: battere `starter` non predice la posizione nel leaderboard Kaggle. |

---

## 6. Reassessment of Existing E04 Candidates

Riallineamento delle direzioni candidate precedentemente ipotizzate:

### Candidate 1: End-of-Season Horizon
* **Classificazione:** **Ottimizzazione Economica Incrementale / Efficienza di Capitale**.
* **Valutazione:** Fondamentale per eliminare lo spreco di liquidità negli ultimi 10-12 giorni dell'episodio. Altissima isolabilità sperimentale. Tuttavia, applicato solo a 4 tile, il guadagno assoluto è stimato in circa +$300–$800. Necessario ma non sufficiente a colmare il gap di scala su Kaggle.

### Candidate 2: Market Timing & Demand Exploitation
* **Classificazione:** **Miglioramento Competitivo / Adattivo**.
* **Valutazione:** Sfrutta lo stoccaggio nel capanno per vendere durante i picchi dei negozi cittadini. Presenta però il vincolo del limite di capacità del shed (100 oggetti). Richiede un volume di produzione elevato per produrre impatti significativi.

### Candidate 3: Modello Economico Esatto (`max_yield` & Ongoing)
* **Classificazione:** **Ottimizzazione Economica Incrementale**.
* **Valutazione:** Corregge la formula ROI sostituendo il valore hardcoded `yield=2.0` con la resa effettiva (es. Melone=6, Grano=6) e il rendimento cumulativo delle colture ongoing (Pomodoro, Fragola). Rischio nullo, elevata chiarezza concettuale.

### Candidate 4: Scaling Geografico oltre 4 Tile (NW 25-Tile / `HIRE`)
* **Classificazione:** **Miglioramento di Scalabilità e Capacità Produttiva**.
* **Valutazione:** Rappresenta il vero salto quantico per competere sul leaderboard globale (passando da 4 tile a 12-25 tile e integrando i lavoratori subordinati). Introduce tuttavia complessità di movimento e coordinamento spaziale.

---

## 7. Top Strategic Gaps

Al termine dell'audit, si individuano i **4 Strategic Gaps principali**:

### 1. Gap Spaziale e Lavorativo: Sotto-Utilizzo del Quadrante Iniziale (4 vs 25 Tile & 1 vs N Workers)
1. **Meccanica Ignorata:** 21 tile sbloccate nel quadrante NW inutilizzate; azione `HIRE` per farm hands inutilizzata.
2. **Evidenza:** `kaggriculture.py` `_initial_tile` e `_do_hire`.
3. **Comportamento E03:** Hardcoded cluster 2×2 di 4 tile, 1 solo farmer.
4. **Impatto Competitivo:** Gli avversari su Kaggle sfruttano l'intero quadrante producendo $50k–$100k+.
5. **Misurazione:** Resa per giorno, volume raccolto totale, tile coltivate, conteggio worker.
6. **Rischio Sperimentale:** Medio-Alto (richiede coordinamento di movimento e irrigazione per evitare starvation).
7. **Isolabilità:** Isolabile come estensione della policy di footprinting e allocazione lavoratori.

### 2. Gap di Orizzonte Temporale: Blindness all'End-of-Season
1. **Meccanica Ignorata:** Limite dell'episodio al giorno 30 (step 720).
2. **Evidenza:** `multi_tile_roi.py` ordina semi e pianta al giorno 28-29.
3. **Comportamento E03:** Nessun controllo sul tempo residuo di maturazione della coltura.
4. **Impatto Competitivo:** Blocco e perdita di liquidità finale in semi unharvested.
5. **Misurazione:** Capitale sprecato in piante non maturate a fine partita / liquidità al giorno 30.
6. **Rischio Sperimentale:** Molto Basso (regola di guardia: `if day + crop_days > 29: skip_plant`).
7. **Isolability:** **Perfetta singola variabile sperimentale**.

### 3. Gap Economico: Inaccuratezza del Modello di Resa (`max_yield` e Ongoing)
1. **Meccanica Ignorata:** Parametri di resa reali (`max_yield` WHEAT/MELON=6, CARROT=4; `ongoing` TOMATO/STRAWBERRY).
2. **Evidenza:** `kaggriculture.py` L11-17 vs `multi_tile_roi.py` L44 (`yield_units = 2.0`).
3. **Comportamento E03:** Selezione coltura basata su assunzione di resa errata.
4. **Impatto Competitivo:** Selezione sub-ottimale della coltura ad ogni ciclo produttivo.
5. **Misurazione:** ROI/giorno effettivo calcolato vs ROI reale misurato post-raccolto.
6. **Rischio Sperimentale:** Molto Basso.
7. **Isolability:** **Perfetta singola variabile sperimentale**.

### 4. Gap Metrologico: Baseline Locale Insufficiente per la Validazione Competitiva
1. **Meccanica Ignorata:** Valutazione contro opponenti competitivi a multi-tile nel benchmark locale.
2. **Evidenza:** `runner.py` testa solo contro `pass`, `random`, `starter`.
3. **Comportamento E03:** Raggiunge il 100% win rate locale contro avversari banali, creando un'illusione di dominanza.
4. **Impatto Competitivo:** Nessun feedback locale sulla capacità dell'agente di battere strategie espansive.
5. **Misurazione:** Creazione di un avversario sintetico multi-tile di riferimento (`synthetic_expansion_agent`).
6. **Rischio Sperimentale:** Basso (aggiornamento dell'infrastruttura di benchmark).
7. **Isolability:** Indipendente.

---

## 8. Recommended E04 Direction

### Raccomandazione Direzionale per E04:

Per rispettare rigorosamente il metodo sperimentale supervisionato (**una modifica strategica principale per esperimento**), si raccomanda di strutturare E04 focalizzandosi sul **Modello Economico Consapevole dell'Orizzonte e della Resa Reale**:

> **E04 Candidate Goal:** `Horizon & Accurate ROI Agent` (**`HorizonROIAgent`**)

#### Motivazione Tecnico-Sperimentale:

1. **Isolabilità Sperimentale Perfetta:**  
   Fissando il footprint a 4 tile (o espandendolo in modo controllato senza introdurre lavoratori multipli), questa modifica isola con precisione chirurgica due difetti logici fondamentali di E03:
   - **Filtro Orizzonte di Fine Stagione:** Blocco acquisto/semina quando `day + max_yield_day > 29`.
   - **Accuratezza ROI & Resa Reale:** Sostituzione di `yield=2.0` con i reali `max_yield` (`WHEAT`=6, `CARROT`=4, `MELON`=6) e integrazione del valore ricorsivo delle colture `ongoing` (`TOMATO`/`STRAWBERRY`).

2. **Misurabilità e Sicurezza Operativa:**  
   L'impatto di questa modifica si misura direttamente in:
   - Zero spesa in semi non maturi negli ultimi 10 giorni;
   - Maggiore liquidità finale disponibile al turno 720;
   - Selezione dinamica orientata verso colture a maggior resa reale (es. Melone/Grano).

3. **Propedeuticità allo Scaling Futuro (E05):**  
   Risolvere l'ottimizzazione economica e l'orizzonte temporale su piccola scala fornisce le fondamenta matematiche necessarie prima di affrontare lo scaling su 25 tile e la gestione dei *farm hands* in E05.

---

## 9. Open Questions / Unknowns

Durante l'audit sono stati identificati i seguenti elementi classificati come **UNKNOWN** in quanto non derivabili univocamente dal codice locale o dalla documentazione Kaggle:

1. **[UNKNOWN] Distribuzione delle Strategie Avversarie su Kaggle:**  
   Non è noto quale percentuale degli agenti correnti sul leaderboard Kaggle utilizzi l'acquisto di nuovi quadranti (`BUY_LAND`), l'assunzione di *farm hands* (`HIRE`), o la vendita mirata ai negozi della città.

2. **[UNKNOWN] Algoritmo Esatto di Matchmaking e Decadimento Rating Kaggle:**  
   La frequenza delle partite giocate sulla piattaforma e l'impatto esatto dell'incertezza (volatilità) del rating Skill non sono trasparenti dal solo leaderboard UI.

3. **[UNKNOWN] Elasticità del Prezzo sotto Produzione Ad Alta Volumetria:**  
   L'impatto sul prezzo di mercato quando due agenti vendono simultaneamente centinaia di unità di Melone o Carote nello stesso turno richiede simulazioni diagnostiche dedicate.

---

*Documento completato e salvato in `docs/experiments/E04-01_Competitive_Gap_Analysis.md` in conformità con i vincoli della fase DEFINE.*
