# MODEL_SPEC Antigravity E18.2 — Capacity Governed V1 (Foundation C2.1 Review)

```text
AGENT_OWNER: ANTIGRAVITY
MODEL: Antigravity E18.2 Capacity Governed V1
VERSION: ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1
CANDIDATE_ID: ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1
BASE_POLICY_CHASSIS: ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1
STATUS: DEVELOPMENT_COMPLETE_NON_QUALIFYING / FROZEN_PERFORMANCE_GAP (2026-09-04)
DECISION: ITERATE (Non qualifying for tournament submission / frozen line)
FOUNDATION_BASELINE: C2.1 reconciled
ROUND: E18
IMPLEMENTATION_RUNTIME:
  - src/agricola/strategy/antigravity/antigravity_e18_capacity_governed_v2.py (Overlay)
  - src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py (Base Chassis)
```

---

## 1. Obiettivo e ipotesi

### 1.1 Risultato perseguito
L'obiettivo dell'architettura **Antigravity E18.2 Capacity Governed V1** è eliminare lo spreco strutturale di ore-lavoro e di throughput della manodopera agricola attraverso un governatore di capacità in loco (*on-tile service recovery*), garantendo la totale indipendenza strategica del modello (zero dipendenze da tabelle di routine o dati esterni, zero wrapper passivi).

Il modello si compone di due livelli strettamente integrati:
1. **Chassis reattivo E18.1 (`antigravity_e18_reactive_reboot_v1.py`)**: controllore autonomo end-to-end con pianificazione fenologica del ciclo colturale, logistica di deposito nella capanna centrale (*shed*), allocazione spaziale dei lavoratori priva di collisioni (*Manhattan dispatch*), dimensionamento della forza lavoro governato dal carico di lavoro (*backlog*) a costo di Fibonacci e classificazione dell'avversario tramite snapshot pubblico.
2. **Governatore di capacità E18.2 (`antigravity_e18_capacity_governed_v2.py`)**: strato di controllo sovrapposto che intercetta i lavoratori assegnati a comandi di spostamento (`MOVE_OPCODES`: `NORTH`, `SOUTH`, `EAST`, `WEST`, `PASS`) e, qualora si trovino su una cella con compiti insoddisfatti (`WEED` da estirpare, pianta matura da raccogliere, pianta in crescita da irrigare), sostituisce il movimento con un'azione di servizio locale a costo di spostamento nullo (*zero Manhattan displacement*).

### 1.2 Ambito e contesto operativo
- **Orizzonte temporale**: 30 giorni di simulazione, ciascuno suddiviso in 24 turni orari, per un totale di 720 passi per partita.
- **Topologia operativa**: gestione fondiaria scalare su 2-3 quadranti (Q0 Nord-Ovest, Q1 Nord-Est, opzionale Q2 Sud-Ovest).
- **Ciclo biologico**: ciclo colturale a due sementi (`CARROT` per rotazione rapida a basso capitale; `WHEAT` per accumulo di cassa e resa a volume).
- **Manodopera**: gestione simultanea del caposquadra (*farmer*) e di un organico scalabile di braccianti (*hands*, fino a un massimo di 6-7 unità).

### 1.3 Assunzioni
- **Assunzione di costo zero del servizio on-tile**: l'esecuzione di un'azione produttiva (`DIG`, `WATER`, `HARVEST`) sulla cella su cui il lavoratore si trova già ha un costo di spostamento pari a zero e non altera il piano logistico complessivo, purché il carico trasportato dal lavoratore sia inferiore alla soglia di rientro (< 2 unità) e l'azione non collida con un compito già assegnato ad altri lavoratori nel medesimo turno.
- **Assunzione di determinismo**: la simulazione rispetta l'ordine di esecuzione sequenziale formalizzato in [docs/foundation/ENGINE_CONTRACT.md](../../foundation/ENGINE_CONTRACT.md) (convalida semina -> azioni lavoratori -> ordini di mercato -> consumo biologico e decadimento -> refresh di fine giornata).
- **Assunzione di osservabilità epistemica**: le uniche informazioni utilizzate sono quelle autorizzate dallo stato pubblico e privato al turno corrente; nessuna informazione viene inferita da lookahead futuro o variabili non accessibili in osservazione.

### 1.4 Limiti strutturali verificati e stato della linea
- **Tetto economico del modello solo-colturale (*Crop-Only Ceiling*)**: la strategia implementata in Antigravity E18.2 gestisce esclusivamente il ciclo vegetale (`CARROT` e `WHEAT`). Non include alcun modulo zootecnico per l'acquisto, il ricovero (*pastures* / fienili) o la cura del bestiame (`COW`, `SHEEP`, `GOOSE`). L'assenza delle produzioni animali ad altissimo margine (`MILK`, `WOOL`, `EGG`) impone un tetto economico asintotico documentato tra $10.000 e $15.000.
- **Stato formale della linea Antigravity**: a seguito della valutazione E18.2 (che ha conseguito un verdetto formale di `ITERATE` con $11.369,72 di media su seed di sviluppo, insufficiente a raggiungere la soglia di qualificazione M1 di $15.000), in data 2026-09-04 l'intera linea di sviluppo Antigravity è stata posta in stato di **`FROZEN_PERFORMANCE_GAP`**. I relativi asset sono conservati a fini di comparazione storica e avversari di collaudo, senza autorizzazione a nuove submission finché non emergerà una proposta architetturale con modulo zootecnico causale.

---

## 2. Strategia

### 2.1 Pianificazione della produzione colturale
Il modello adotta una pianificazione del ciclo fenologico rigorosamente allineata a [docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md](../../foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md):
1. **Diserbo preventivo (`DIG`)**: le celle contrassegnate con `kind == "WEED"` all'interno dei quadranti posseduti generano task di diserbo per liberare suolo coltivabile e azzerare penalizzazioni.
2. **Semina ordinata (`PLANT`)**: le celle vuote (`tile is None`) nei quadranti posseduti e abilitati vengono seminate se lo stock privato di sementi è positivo. La selezione della semente è zonale:
   - Quadrante Q0 (Nord-Ovest): assegnato a `CARROT` (ciclo breve, primo raccolto a giorno 2, picco di resa a giorno 3).
   - Quadranti Q1 (Nord-Est) e Q2 (Sud-Ovest): assegnati a `WHEAT` (prezzo di vendita $50, primo raccolto a giorno 2, picco a giorno 3).
   - **Sospensione terminale della semina**: nessuna semina viene effettuata a partire dal giorno 27 (`day < 27`), poiché le sementi piantate non raggiungerebbero la maturazione prima della fine dell'episodio (giorno 30).
3. **Irrigazione sistematica (`WATER`)**: tutte le piante in fase di crescita che presentano `watered_today == False` ricevono priorità di irrigazione giornaliera.
4. **Raccolta selettiva alla massima resa (`HARVEST`)**:
   - La raccolta viene pianificata solo se l'età della coltura soddisfa `age >= first_yield_day` (2 giorni) e sono presenti frutti (`yield_units > 0`).
   - Il trigger principale attende la piena maturazione: `age >= max_yield_day` (3 giorni) oppure `yield_units >= max_yield` (4 unità).
   - Negli ultimi due giorni (`day >= 28`), il vincolo di attesa della resa massima viene rilassato per raccogliere qualsiasi unità disponibile prima della conclusione.

### 2.2 Logistica del raccolto e movimentazione
- **Capacità di trasporto individuale**: ogni lavoratore ha una capacità nominale di carico. Il controllore monitora `private.inventories[worker_idx]`.
- **Rotta di scarico (*Shed Dropoff*)**:
  - Quando un lavoratore accumula $\ge 2$ unità di prodotto, abbandona qualsiasi task di campo e punta verso la capanna centrale (*shed*) situata alle coordinate `(4, 4)`.
  - Nelle ore serali (`hour >= 22`) o negli ultimi giorni (`day >= 27`), la soglia di rientro viene ridotta a $\ge 1$ unità per evitare che merci rimangano intrappolate negli zaini dei braccianti durante la notte o a fine partita.
  - Giunto a `(4, 4)`, il lavoratore esegue l'azione `DROP`.

### 2.3 Pianificazione degli investimenti e capitale di riserva
La gestione finanziaria opera a ciclo continuo mediante il modulo `_market_orders`:
- **Riserva di capitale inviolabile (*Seed Capital Reserve*)**: il sistema mantiene costantemente una riserva di cassa minima non intaccabile pari a **$150,00**. Nessun ordine di espansione fondiaria o di assunzione di manodopera può essere emesso se ridurrebbe la liquidità al di sotto di questa soglia, garantendo la liquidità per l'approvvigionamento di sementi.
- **Rifornimento sementi (`BUY_SEED`)**:
  - Per ciascuna coltura (`CARROT`, `WHEAT`), il modello mantiene uno stock obiettivo configurato dal regime attivo (6 sementi in `BALANCED_SERVICE`, 8 in `EXPANSION_TEMPO`).
  - Se le sementi in deposito (`private.seeds`) scendono sotto il target e `day < 28`, il sistema ordina l'acquisto al mercato. Se il capitale non consente il lotto completo, viene acquistata la quantità massima consentita dal bilancio residuo.
- **Vendita dei prodotti (`SELL`)**:
  - I prodotti stoccati nello shed vengono venduti sul mercato appena la quantità raggiunge la soglia configurata (`sell_threshold = 2` in Balanced, `1` in Expansion).
  - La vendita è incondizionata (anche per 1 unità) se la cassa scende sotto $300,00 o a partire dal giorno 25 per massimizzare il flusso di cassa finale.
- **Espansione fondiaria governata dal capitale (`BUY_LAND`)**:
  - Sblocco Quadrante Q1: autorizzato se `day >= q1_unlock_day` (D5 in Balanced, D4 in Expansion) e `money >= q1_min_cash` ($1.400 in Balanced, $1.200 in Expansion; costo sblocco: $1.000).
  - Sblocco Quadrante Q2: autorizzato se `day >= q2_unlock_day` (D12 in Balanced, D8 in Expansion) e `money >= q2_min_cash` ($2.600 in Balanced, $2.200 in Expansion; costo sblocco: $2.000).

### 2.4 Pianificazione e dimensionamento della manodopera
- **Finestra temporale esclusiva**: gli ordini di assunzione (`HIRE`) vengono emessi esclusivamente a **ora 0** (`hour == 0`) di ciascuna giornata, massimizzando il ritorno operativo delle 24 ore successive.
- **Costo incrementale di Fibonacci**: il costo di ciascuna assunzione giornaliera segue la sequenza `_FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]`, tracciando rigorosamente `hires_today`.
- **Dimensionamento governato dal carico (*Backlog-Governed Hiring*)**:
  - Il numero desiderato di braccianti non è prefissato, ma scala con il numero di compiti attivi non serviti:
    $$\text{desired\_hands} = \min\left(\text{max\_hands}, \max\left(\text{target\_hands}, 1 + \left\lfloor \frac{\text{backlog}}{4} \right\rfloor\right)\right)$$
  - Al giorno 0, l'assunzione è limitata a un massimo cautelativo di 2 unità per preservare il capitale iniziale.

### 2.5 Orizzonte del piano e condizioni di revisione
- **Orizzonte operativo orario**: assegnazione dinamica turno per turno, con memoria dell'obiettivo per singolo lavoratore (`_worker_assignments`) per garantire stabilità di traiettoria verso celle distanti.
- **Snapshot e selezione del regime (Giorno 4-8, default Giorno 6)**:
  - All'ora 0 del giorno target, il sistema analizza lo stato pubblico della fattoria avversaria attraverso `_public_opponent_snapshot`:
    $$\text{pressure\_score} = 2 \cdot \text{crop\_tiles} + 3 \cdot \text{weed\_tiles} + 3 \cdot \text{hands} + 2 \cdot \text{animal\_tiles}$$
  - Se $\text{pressure\_score} \ge 20.0$, il sistema seleziona il regime `EXPANSION_TEMPO` (soglia vendita 1, target hands 5, target semi 8, sblocco Q1 anticipato a D4 con cassa $1.200, sblocco Q2 a D8 con cassa $2.200).
  - Altrimenti, conferma il regime `BALANCED_SERVICE` (soglia vendita 2, target hands 4, target semi 6, sblocco Q1 a D5/$1.400, Q2 a D12/$2.600).
  - La decisione è **rigida (*sticky*)**: una volta selezionato, il regime non oscilla più fino al termine della partita.
- **Fase terminale (Giorno 28+)**:
  - Disattivazione del governatore di capacità (*terminal passthrough*).
  - Vendita al mercato di qualsiasi merce presente nello shed senza riserva minima.
  - Sospensione degli acquisti di terra e sementi per concentrare ogni risorsa sulla monetizzazione.

---

## 3. Decisioni implementate

### 3.1 Feature realmente usate
Le decisioni operative dipendono esclusivamente da feature normalizzate tramite `CodexObservationAdapter` in [src/agricola/core/observation_contract.py](../../../src/agricola/core/observation_contract.py), catalogate in conformità a [docs/foundation/feature_model/FEATURE_CATALOG.md](../../foundation/feature_model/FEATURE_CATALOG.md):

| Feature nel codice | Espressione / Origine | Classe epistemica | Utilizzo decisionale |
|---|---|---|---|
| `clock.day` | `step // 24` | Pubblica | Controllo ciclo di vita, date di sblocco quadranti, terminal passthrough |
| `clock.hour` | `step % 24` | Pubblica | Trigger assunzioni (`hour == 0`), rientro serale allo shed (`hour >= 22`) |
| `farm.money` | `farms[player].money` | Privata | Verifica riserva di cassa ($150), gating sblocco quadranti, acquisto sementi |
| `farm.tiles[y][x].kind` | Matrice griglia 10x10 | Privata / Pubblica locale | Identificazione `WEED` (trigger `DIG`) ed esame celle vuote |
| `farm.tiles[y][x].crop` | Matrice griglia 10x10 | Privata / Pubblica locale | Riconoscimento coltura (`CARROT`, `WHEAT`) |
| `farm.tiles[y][x].planted_day` | Matrice griglia 10x10 | Privata / Pubblica locale | Calcolo età colturale: $\text{age} = \text{day} - \text{planted\_day}$ |
| `farm.tiles[y][x].yield_units` | Matrice griglia 10x10 | Privata / Pubblica locale | Verifica maturazione e prontezza al raccolto |
| `farm.tiles[y][x].watered_today` | Matrice griglia 10x10 | Privata / Pubblica locale | Trigger irrigazione giornaliera (`WATER`) se `False` |
| `farm.farmer`, `farm.hands` | Coordinate $(x, y)$ | Privata / Pubblica locale | Calcolo distanze Manhattan, posizionamento lavoratori e recupero on-tile |
| `farm.unlocked_quadrants` | Elenco quadranti | Privata / Pubblica locale | Filtro perimetrale di assegnazione task (`_owned_quadrants`) |
| `private.seeds` | Dizionario sementi | Privata | Controllo stock disponibile prima di emettere comandi `PLANT` |
| `private.shed` | Dizionario inventario capanna | Privata | Generazione ordini di vendita `SELL` al mercato |
| `private.inventories` | Lista inventari lavoratori | Privata | Calcolo carico trasportato (`carrying`), trigger rotta verso lo shed |
| `farms[opp].tiles`, `hands` | Fattoria avversaria | Pubblica | Calcolo `pressure_score` durante la finestra di snapshot D4-D8 |

### 3.2 Criteri di scelta e priorità tra azioni concorrenti

#### Gerarchia di generazione dei compiti di campo (`_generate_tasks`)
1. **Priorità 0 — Raccolta matura (`HARVEST`)**: colture con $\text{age} \ge 2$ e $\text{yield\_units} > 0$ che hanno raggiunto la piena maturazione ($\text{age} \ge 3$ o $\text{yield\_units} \ge 4$ o $\text{day} \ge 28$).
2. **Priorità 1 — Irrigazione vitale (`WATER`)**: colture in crescita non ancora irrigate nel turno odierno (`watered_today == False`).
3. **Priorità 2 — Diserbo rigenerativo (`DIG`)**: celle infestate da erbacce (`WEED`) per liberare terreno.
4. **Priorità 3 — Nuova semina (`PLANT`)**: celle libere nei quadranti autorizzati, condizionata alla disponibilità di sementi in `seed_stock` e $\text{day} < 27$.

#### Assegnazione spaziale Manhattan dei lavoratori (`_allocate_workers`)
- Se $\text{carrying} \ge 2$ (o $\ge 1$ con $\text{hour} \ge 22$ o $\text{day} \ge 27$): il lavoratore punta verso la capanna centrale `(4, 4)` con passo Manhattan; se già su `(4, 4)`, esegue `DROP`.
- Altrimenti:
  1. Se il lavoratore si trova già sulla cella di un task libero, prende in carico quel task ed esegue l'azione immediatamente sul posto.
  2. Se ha un incarico memorizzato (`_worker_assignments`) ancora valido e non conteso, prosegue verso di esso.
  3. Altrimenti, seleziona il task libero a priorità più alta con la minima distanza Manhattan $\Delta x + \Delta y$.
  4. Gli incarichi assegnati vengono registrati in `assigned_tasks` per impedire a due lavoratori di convergere sullo stesso obiettivo.

#### Governatore di capacità in loco (*On-Tile Recovery*)
Il modulo `_route_on_tile_recovery` intercetta l'azione elaborata dallo chassis base:
- Identifica lavoratori il cui comando pianificato appartiene a `MOVE_OPCODES` (`NORTH`, `SOUTH`, `EAST`, `WEST`, `PASS`).
- Verifica che il lavoratore non sia in rotta di scarico verso lo shed ($\text{carrying} < 2$).
- Ispeziona la cella su cui il lavoratore si trova attualmente:
  - Cella con `WEED` non ancora servita nel turno -> comando sostituito con `["DIG"]`.
  - Cella con `PLANT` matura pronta al raccolto -> comando sostituito con `["HARVEST"]`.
  - Cella con `PLANT` non irrigata e $\text{day} < 28$ -> comando sostituito con `["WATER"]`.
- Registra l'azione nel set `fulfilled` per evitare conflitti concorrenti.

### 3.3 Vincoli e parametri principali

I parametri sono definiti in [docs/model_specs/antigravity/e18/configs/ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json](e18/configs/ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json):

| Parametro | Valore | Motivazione |
|---|---:|---|
| `capacity_governor_enabled` | `true` | Abilita l'intercettazione dei passi oziosi e il recupero di servizio on-tile |
| `terminal_passthrough_day` | `28` | Dal giorno 28 disattiva il governatore per garantire la liquidazione finale incontaminata |
| `recovery_on_tile_only` | `true` | Vincola il recupero esclusivamente alla cella attuale senza deviazioni |
| `capital_reserve_seed` | `150.0` | Riserva di cassa intoccabile per garantire l'acquisto prioritario di sementi |
| `capital_reserve_land` | `100.0` | Margine prudenziale mantenuto prima di spese per la terra |
| `shed_sell_min_cash` | `300.0` | Sotto questa soglia di cassa le vendite dallo shed avvengono anche per 1 sola unità |
| `pressure_threshold` | `20.0` | Soglia di punteggio avversario per il passaggio a `EXPANSION_TEMPO` |
| `target_hands` (Balanced / Expansion) | `4 / 5` | Organico minimo obiettivo per quadrante |
| `max_hands` (Balanced / Expansion) | `6 / 7` | Organico massimo consentito per contenere i costi di assunzione di Fibonacci |
| `seed_target` (CARROT / WHEAT) | `6 / 6` (Bal), `8 / 8` (Exp) | Scorta polmone di sementi da mantenere nello stock privato |
| `q1_unlock_day` / `q1_min_cash` | D5 / $1.400 (Bal), D4 / $1.200 (Exp) | Condizioni di cassa e tempo per lo sblocco del quadrante Q1 (costo $1.000) |
| `q2_unlock_day` / `q2_min_cash` | D12 / $2.600 (Bal), D8 / $2.200 (Exp) | Condizioni di cassa e tempo per lo sblocco del quadrante Q2 (costo $2.000) |

---

## 4. Reazioni e gestione imprevisti

### 4.1 Gestione anomalie ed errori tecnici (Architettura Fail-Closed)
- Entrambi i componenti runtime (`AntigravityE18CapacityGovernedPolicy` e `AntigravityE18ReactiveRebootPolicy`) sono incapsulati in blocchi di protezione contro le eccezioni non gestite.
- Se l'adattatore dell'osservazione o la computazione decisionale solleva un errore inatteso:
  - Il controllore cattura l'eccezione, incrementa i contatori diagnostici `technical_errors`, `error_count` e `fallback_count`.
  - Registra l'errore in `last_exception`.
  - Emette immediatamente il fallback di sicurezza `SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}`, garantendo che l'episodio non incorra in squalifica per comando malformato (*fail-closed safety*).

### 4.2 Carenze di liquidità e gestione del mercato
- Se il mercato non fornisce prezzi o la cassa è insufficiente per acquistare le quote complete di sementi, il codice calcola l'acquisto parziale compatibile con la liquidità residua: `can_buy = int(money // price)`.
- Se la liquidità totale scende sotto $300,00, il controllore azzera la soglia minima di vendita (`sell_threshold = 1`) e liquida immediatamente qualsiasi scorta giacente nella capanna per ripristinare il capitale circolante.

### 4.3 Prevenzione conflitti e collisioni tra lavoratori
- **Deduplicazione turnaria dei task**: `assigned_tasks` memorizza le coordinate già affidate a un lavoratore, impedendo che due braccianti convergano sulla medesima tile.
- **Deduplicazione del recupero on-tile**: `fulfilled` traccia la coppia `(posizione, comando)` per impedire che due lavoratori sovrapposti o contigui tentino la medesima azione o che il governatore assegni un'azione ridondante rispetto a un comando già emesso.

### 4.4 Chiusura della partita (Endgame Phase)
- **Giorno 27**: stop definitivo a qualsiasi operazione di semina (`PLANT`) per evitare investimenti a fondo perduto.
- **Giorno 28+**:
  - Attivazione del *terminal passthrough*: il governatore di capacità cessa di intercettare i comandi per evitare qualsiasi deviazione dalle manovre di sgombero.
  - Raccolta anticipata di qualsiasi coltura con $\text{yield\_units} > 0$, senza attendere la maturazione massima.
  - Liquidazione sistematica di tutte le giacenze di magazzino in cassa.

---

## 5. Coerenza con la Foundation C2.1

### 5.1 Collegamento formale alle regole della Foundation
La strategia implementata rispetta puntualmente le specifiche della Foundation riconciliata C2.1:

| Documento Foundation | Principio applicato | Recepimento nel modello Antigravity |
|---|---|---|
| [ENGINE_CONTRACT.md](../../foundation/ENGINE_CONTRACT.md) | Sequenza deterministica del turno (fasi 1-6) | Nessuna assunzione di esecuzione parallela o fuori fase; separazione netta tra ordini di mercato e azioni di movimento. |
| [ENGINE_CONTRACT.md](../../foundation/ENGINE_CONTRACT.md) | Limite ordini di mercato | Il metodo `_market_orders` limita gli ordini per turno a un massimo di 8 (`orders[:8]`). |
| [ONTOLOGY_C2_1.md](../../foundation/ontology/ONTOLOGY_C2_1.md) | Modello di entità, ruoli e confini | Distinzione rigida tra `Farmer` e `Hands`; gestione dello `Shed` a `(4, 4)`; rispetto dei quadranti fondiari. |
| [KAGGRICULTURE_STATE_MACHINE_C2_1.md](../../foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md) | Transizioni fenologiche e della terra | Rispetto rigoroso dei cicli biologici: `EMPTY` -> `PLANTED` -> `GROWING` -> `MATURE`; `WEED` -> `DIG` -> `EMPTY`. |
| [FEATURE_MODEL_C2_1.md](../../foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md) | Confini epistemici (Pubblico vs Privato) | Le decisioni usano solo feature derivabili dal turno corrente; lo snapshot avversario legge solo feature pubbliche della fattoria rivale. |
| [FEATURE_CATALOG.md](../../foundation/feature_model/FEATURE_CATALOG.md) | Formule canoniche di derivazione | Età pianta calcolata esattamente come $\text{day} - \text{planted\_day}$; distanze modellate come norma Manhattan $L_1$. |

### 5.2 Discrepanze tra Foundation e codice implementato
La disamina analitica del codice rispetto alla Foundation evidenzia le seguenti discrepanze:
1. **Assenza della Zootecnia (Livestock Engine)**:
   - *Foundation*: [ONTOLOGY_C2_1.md](../../foundation/ontology/ONTOLOGY_C2_1.md) definisce animali (`COW`, `SHEEP`, `GOOSE`), strutture (`PASTURE`), comandi (`BUY_ANIMAL`, `BUILD_PASTURE`, `FEED`, `CARE`, `COLLECT_FERTILIZER`) e prodotti ad alto valore (`MILK`, `WOOL`, `EGG`, `FERTILIZER`).
   - *Codice Antigravity E18.2*: non contiene alcuna logica di acquisto, alimentazione o ricovero per animali. Il codice è interamente confinato al ciclo vegetale. Questa è la causa diretta del divario economico rispetto a modelli completi come Codex V48.
2. **Prezzi di mercato statici nel controller**:
   - *Foundation*: i prezzi di mercato dei prodotti variano dinamicamente in base alla domanda e all'offerta aggregata.
   - *Codice Antigravity E18.2*: assume parametri economici costanti nel file di configurazione (`seed_price` e `sale_price`), senza tracciare la volatilità del mercato in tempo reale né ottimizzare il timing di vendita rispetto ai picchi di prezzo.

---

## 6. Stato di realizzazione

### 6.1 Comportamento implementato e verificato
- [x] Controllore sovrapposto di capacità in loco (`AntigravityE18CapacityGovernedPolicy`) in [src/agricola/strategy/antigravity/antigravity_e18_capacity_governed_v2.py](../../../src/agricola/strategy/antigravity/antigravity_e18_capacity_governed_v2.py).
- [x] Chassis autonomo reattivo con ciclo biologico, logistica shed e allocazione Manhattan in [src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py](../../../src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py).
- [x] Adattatore osservativo neutro condiviso [src/agricola/core/observation_contract.py](../../../src/agricola/core/observation_contract.py).
- [x] Configurazione parametrica JSON in [docs/model_specs/antigravity/e18/configs/ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json](e18/configs/ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json).
- [x] Suite di test unitari e di verifica controfattuale in [docs/model_specs/antigravity/e18/tests/test_antigravity_e18_capacity_governed.py](e18/tests/test_antigravity_e18_capacity_governed.py) e [docs/model_specs/antigravity/e18/tests/test_antigravity_e18_lifecycle.py](e18/tests/test_antigravity_e18_lifecycle.py).
- [x] Runner del torneo di validazione locale con diagnostica ed export metriche in [docs/model_specs/antigravity/e18/tools/run_antigravity_e18_capacity_governed_tournament.py](e18/tools/run_antigravity_e18_capacity_governed_tournament.py).

### 6.2 Realizzazione parziale
- [~] **Reattività all'avversario**: limitata a una sola osservazione macroscopica nella finestra Day 4 - Day 8 che calcola il `pressure_score` e seleziona il regime in modo immutabile (*sticky*). Non vi è alcun monitoraggio continuo né adattamento tattico alle strategie concorrenti dopo il Giorno 8.

### 6.3 Proposta futura (non implementata)
- [ ] **Motore zootecnico a zero fughe (*Zero-Escape Livestock Module*)**: integrazione di un cluster di pascoli centrali Chebyshev $\le 2$ con razionamento causale garantito del grano (`WHEAT`) per eliminare le fughe di bestiame e sbloccare la produzione di latte e lana.
- [ ] **Pianificatore predittivo di mercato**: monitoraggio delle serie storiche dei prezzi locali per concentrare le vendite nei momenti di domanda favorevole.
- [ ] **Riconversione fondiaria ciclica (*Pasture Reclaiming*)**: rotazione dinamica tra pascoli dismessi e colture ad alto rendimento.

---

## 7. File di implementazione

La seguente tabella censita ricostruisce l'elenco completo dei file che concorrono all'implementazione, configurazione e verifica del modello **Antigravity E18.2 Capacity Governed V1**, partendo dall'entry point e dalle dipendenze dirette:

| File, con link relativo funzionante | Ruolo | Parte della strategia implementata | Categoria |
|---|---|---|---|
| [../../../src/agricola/strategy/antigravity/antigravity_e18_capacity_governed_v2.py](../../../src/agricola/strategy/antigravity/antigravity_e18_capacity_governed_v2.py) | Controller runtime sovrapposto e factory dell'agente. | `AntigravityE18CapacityGovernedPolicy`, recupero del servizio on-tile (`_route_on_tile_recovery`), terminal passthrough a giorno 28+, telemetria. | Runtime |
| [../../../src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py](../../../src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py) | Controllore di base chassis e logica decisionale. | `AntigravityE18ReactiveRebootPolicy`, generazione task (`_generate_tasks`), allocazione Manhattan (`_allocate_workers`), ordini mercato (`_market_orders`), snapshot avversario. | Runtime |
| [../../../src/agricola/core/observation_contract.py](../../../src/agricola/core/observation_contract.py) | Contratto osservativo neutro condiviso. | `CodexObservationAdapter`, parsing normalizzato dell'osservazione, clock, farm e stato privato. | Runtime |
| [e18/configs/ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json](e18/configs/ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.json) | Configurazione parametrica del candidato E18.2. | Parametri del governatore di capacità, riserve di cassa, profili colturali, regimi `BALANCED_SERVICE` ed `EXPANSION_TEMPO`. | Configurazione |
| [e18/configs/ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.json](e18/configs/ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.json) | Configurazione di fallback per lo chassis base E18.1. | Parametri di default ereditati dallo chassis base in assenza di overlay. | Configurazione |
| [e18/tools/run_antigravity_e18_capacity_governed_tournament.py](e18/tools/run_antigravity_e18_capacity_governed_tournament.py) | Runner di validazione del torneo e misurazione throughput. | Esecuzione match controllati su seed di sviluppo contro avversari frozen, calcolo metriche e diagnostica. | Builder / verifica |
| [e18/tools/run_antigravity_e18_tournament.py](e18/tools/run_antigravity_e18_tournament.py) | Runner di valutazione per lo chassis E18.1 base. | Esecuzione partite a coppie e validazione delle metriche dello chassis base. | Builder / verifica |
| [e18/tools/run_antigravity_e18_gate_a.py](e18/tools/run_antigravity_e18_gate_a.py) | Runner di convalida Gate A. | Verifica tecnica di assenza di errori e conformità dei comandi su seed di controllo. | Builder / verifica |
| [e18/tools/run_antigravity_e18_gate_b.py](e18/tools/run_antigravity_e18_gate_b.py) | Runner di convalida Gate B. | Verifica della reattività e sensibilità dello snapshot avversario. | Builder / verifica |
| [e18/tests/test_antigravity_e18_capacity_governed.py](e18/tests/test_antigravity_e18_capacity_governed.py) | Test unitari e controfattuali del governatore di capacità. | Test su diserbo, raccolta e irrigazione on-tile, test controfattuale di spegnimento e terminal passthrough. | Test |
| [e18/tests/test_antigravity_e18_lifecycle.py](e18/tests/test_antigravity_e18_lifecycle.py) | Test del ciclo vitale colturale e task generation. | Verifica non-raccolta di piante immature, trigger raccolta matura e irrigazione su piante giovani. | Test |
| [e18/tests/test_antigravity_e18_counterfactual.py](e18/tests/test_antigravity_e18_counterfactual.py) | Test controfattuali dello snapshot avversario. | Verifica della sensibilità a variazioni di pressione dell'avversario e corretta transizione di regime. | Test |
| [e18/tests/test_antigravity_e18_gate_a.py](e18/tests/test_antigravity_e18_gate_a.py) | Test di conformità tecnica fail-closed Gate A. | Esecuzione simulata con asserzione su `technical_errors == 0` e `fallback_count == 0`. | Test |

*Dichiarazione di conformità sulle submission*: nessun artefatto di submission o bundle Kaggle è stato compilato o autorizzato per questa versione (`ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1`), in quanto il modello ha concluso il ciclo di sviluppo con esito `DEVELOPMENT_COMPLETE_NON_QUALIFYING` (decisione `ITERATE`) e la linea si trova in stato di congelamento `FROZEN_PERFORMANCE_GAP`.

---

### 7.1 Inventario della Baseline Storica Congelata (Antigravity C2 V4.0)
A fini di trasparenza e tracciabilità storica, si riporta di seguito l'inventario distinto della baseline precedente **Antigravity C2.1 V4.0** ([MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md](MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md)), congelata e conservata esclusivamente come riferimento e avversario di test:

| File storico, con link relativo | Ruolo storico | Categoria |
|---|---|---|
| [../../../src/agricola/strategy/antigravity/antigravity_3q_high_density_v4.py](../../../src/agricola/strategy/antigravity/antigravity_3q_high_density_v4.py) | Runtime baseline storica C2 V4.0 (derivata con patch Step 195 e liquidazione Step 717). | Runtime (storico) |
| [../../../src/agricola/strategy/antigravity/agent_c2_3q_v4.py](../../../src/agricola/strategy/antigravity/agent_c2_3q_v4.py) | Entry point della baseline C2 V4.0. | Runtime (storico) |
| [../../../src/agricola/strategy/antigravity/__init__.py](../../../src/agricola/strategy/antigravity/__init__.py) | Package init del modulo Antigravity per le versioni C2 ed E17. | Runtime (storico) |
| [../../../scripts/build_submission_antigravity_v4.py](../../../scripts/build_submission_antigravity_v4.py) | Script builder per la generazione del bundle congelato C2 V4.0. | Builder (storico) |
| [../../governance/history/model_spec_c2/antigravity/freeze/submission_antigravity_v4_tournament.py](../../governance/history/model_spec_c2/antigravity/freeze/submission_antigravity_v4_tournament.py) | Bundle congelato standalone per il torneo a 42 match C2. | Submission (congelata) |
| [archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py](archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py) | Bundle standalone storico conservato nell'archivio E16. | Submission (legacy) |
| [../../../tests/test_antigravity_v4_3q.py](../../../tests/test_antigravity_v4_3q.py) | Test di non-regressione e parità byte-per-byte per la baseline congelata C2 V4.0. | Test (storico) |

---

## 8. Benchmark, evidenza diagnostica e cronologia

### 8.1 Evidenza sperimentale E18.2
I risultati diagnostici e di validazione per il modello E18.2 sono documentati in [docs/model_specs/antigravity/e18/reports/E18_ANTIGRAVITY_CAPACITY_GOVERNED_V1_REPORT_IT.md](e18/reports/E18_ANTIGRAVITY_CAPACITY_GOVERNED_V1_REPORT_IT.md) e nei relativi registri:

- **Riconciliazione controfattuale del throughput**:
  - Baseline E18.1 Reboot V1 (senza governatore): cassa media **$10.722,86** (2 vittorie, 2 sconfitte su seed di sviluppo S26090101-S26090104).
  - Candidato E18.2 Capacity Governed V1: cassa media **$11.369,72** (2 vittorie, 2 sconfitte).
  - **Guadagno causale netto**: **+$646,86** per partita, attribuibile esclusivamente al recupero di 120-160 comandi di servizio in loco su passi altrimenti sprecati in `MOVE` o `PASS`.
- **Integrità tecnica**:
  - `technical_errors`: **0** su tutte le partite.
  - `fallback_count`: **0**.
  - `animal_escapes`: **0** (nessun animale presente nell'architettura).
- **Esito del ciclo**: verdetto formale di `DEVELOPMENT_COMPLETE_NON_QUALIFYING` con decisione `ITERATE`. Il modello non qualifica per submission a causa del divario con i benchmark multi-zootecnici.

### 8.2 Cronologia documentale Antigravity
- [docs/model_specs/antigravity/README.md](README.md): registro principale della linea Antigravity, con dichiarazione di congelamento per divario prestazionale (`FROZEN_PERFORMANCE_GAP`).
- [docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.md](MODEL_SPEC_ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1.md): specifica pre-review E18.2 congelata con hash SHA-256 (`CFDB5A5872105348AD92AB322B1B3EF54896E5F523E7E6C7238116032E56C0D9`).
- [docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.md](MODEL_SPEC_ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.md): specifica pre-review E18.1 dello chassis base congelata.
- [docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md](MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md): specifica della baseline derivata storica C2 V4.0 congelata.

---

## 9. Discrepanze o parti non ancora implementate

1. **Assenza di modulo zootecnico causale**: il modello non include logiche di acquisto né di gestione di animali da allevamento (`COW`, `SHEEP`, `GOOSE`). Questa lacuna impedisce di generare le merci a massimo valore del gioco (`MILK`, `WOOL`), limitando l'accumulo di cassa al solo comparto vegetale.
2. **Snapshot avversario puntuale e non dinamico**: la reattività all'avversario viene determinata una sola volta (a Giorno 6) e fissa il regime per tutta la durata dell'episodio, senza aggiornamenti tattici in tempo reale durante i giorni successivi.
3. **Modellazione dei prezzi di mercato statica**: il modello non analizza l'andamento dinamico della curva di domanda/offerta al mercato per ottimizzare il timing delle vendite.
4. **Assenza di pipeline di submission attiva**: a seguito del verdetto `ITERATE` e del blocco `FROZEN_PERFORMANCE_GAP`, non è presente alcuno script attivo per compilare bundle per Kaggle di questo candidato.

---

## 10. Riepilogo di chiusura

La presente `MODEL_SPEC` documenta in modo esaustivo e verificabile la candidata autonoma più recente di Antigravity (**E18.2 Capacity Governed V1**), descrivendone con rigore l'architettura a due livelli (chassis E18.1 e governatore E18.2), i confini operativi, la piena coerenza con la Foundation C2.1 e le cause oggettive del congelamento della linea sotto `FROZEN_PERFORMANCE_GAP`.
