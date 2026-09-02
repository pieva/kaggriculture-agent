# MODEL_SPEC — Claude E17.1 3Q Reactive Independent

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V1`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-02
- **Foundation:** C2.1 (RECONCILED)
- **Stato:** AS-BUILT (development)
- **Ambito:** policy nativa, state-reactive, per il torneo reattivo a tre
  definito in `experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`
- **Sorgente:** `src/agricola/strategy/claude/e17_reactive_3q.py`
- **Config:** `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V1.json`

---

## 1. Ipotesi strategiche proprie (`H-CLAUDE-R`)

Il modello formula tre ipotesi indipendenti, distinte da quelle Codex e non
derivate dai replay Top 3 (usati solo come contesto storico, mai come fonte
di azioni):

1. **H-CR1 (guardie di manutenzione dominano sul planning a lungo termine):**
   una policy che ricalcola ad ogni step le priorità di manutenzione (WATER,
   FEED, HARVEST, recovery `DIG`) direttamente dallo stato osservato evita
   perdite biologiche (weed, fughe) meglio di un piano fisso, perché nessuna
   sequenza precompilata può conoscere in anticipo l'esatta distribuzione
   spaziale delle scadenze biologiche generate dalla concorrenza e dal
   routing reale.
2. **H-CR2 (espansione condizionata, non calendarizzata):** l'attivazione di
   Q1 e Q2 deve dipendere congiuntamente da tre guardie osservabili — cassa
   disponibile oltre riserva, pressione di servizio sulla superficie già
   attiva, orizzonte residuo sufficiente per ammortizzare — non da un giorno
   fisso. Se le tre guardie sono soddisfatte prima del giorno atteso nei
   replay storici, l'espansione anticipata non deve introdurre fughe o weed
   aggiuntive.
3. **H-CR3 (liquidazione e feed buffer devono restringersi con l'orizzonte):**
   una riserva di WHEAT dimensionata sul numero di animali vivi e sui giorni
   residui, insieme a una liquidazione che si intensifica solo quando
   l'orizzonte residuo scende sotto una soglia esplicita, riduce sia il
   rischio di fuga per fame sia l'inventario terminale invenduto, rispetto a
   un buffer costante o a uno schedule di vendita fisso.

Il modello non assume che 3Q o 12 hands siano ottimi globali (principio
cardine di `E17_STRATEGY_FROZEN_V1.md`): sono un bersaglio operativo dato dal
mandato del prompt, non un'inferenza causale dai replay.

---

## 2. Provenance e indipendenza strategica

- Nessun import da `agricola.strategy.codex`, `agricola.strategy.antigravity`
  o `agricola.strategy.copilot`.
- Nessuna tabella di azioni indicizzata per step (`ROUTINE_ACTIONS` o
  equivalente). L'unico stato letto dal costruttore è il file di
  configurazione JSON di questo agente.
- Dipendenze consentite effettivamente usate:
  - `agricola.core.observation_contract` (parsing/validazione neutrale
    dell'osservazione, clock canonico);
  - formule pubbliche `ENGINE_VERIFIED`/`DERIVED_ENGINE_FACT` documentate in
    `ONTOLOGY_C2_1.md`, `KAGGRICULTURE_STATE_MACHINE_C2_1.md` e
    `KAGGRICULTURE_FEATURE_MODEL_C2_1.md` (es. classifier delle 5 viste di
    tile lifecycle, predicato di `crop_harvest_readiness`, finestra
    fertilizzante, formula Fibonacci del costo `HIRE`, mappatura quadrante
    `NW/NE/SW/SE` da coordinate). Queste formule sono fatti dell'ambiente
    condivisi dalla Foundation, non routine proprietarie di un altro agente.
- I nove replay Top 3 e il documento di frozen strategy sono stati letti solo
  come contesto storico per formulare le ipotesi in Sezione 1; nessuna
  sequenza di azioni, timing esatto o tabella da quei replay è stata copiata
  o trascritta nel codice.
- Il planner, il dispatcher worker-per-worker, lo zoning spaziale
  crop/livestock e le guardie di mercato sono progettati e implementati
  nativamente per questo modello.

---

## 3. Stato interno agent-local

La policy è **quasi interamente stateless tra le chiamate**: ogni decisione è
ricalcolata da zero a partire dall'osservazione e dalla configurazione
correnti, senza memoria persistente di target, piani o sequenze pregresse.
Questo garantisce per costruzione:

- determinismo a parità di osservazione;
- reattività: uno stato diverso allo stesso step produce una scansione delle
  priorità diversa e quindi un'azione diversa, senza dipendere da un indice
  di step precompilato.

Stato realmente mantenuto sull'istanza (`ClaudeE17ReactiveAgent`):

| Campo | Ruolo | Letto dalla logica decisionale? |
|---|---|:---:|
| `config` | configurazione congelata al construction time | SÌ |
| `technical_errors` | contatore diagnostico di fallback attivati | NO (solo telemetria) |
| `_telemetry` | contatori passivi (azioni per categoria, guardie attivate) | NO (solo telemetria) |

Nessun campo di stato interno influenza mai la prossima decisione: la
telemetria è scritta ma mai riletta dal planner (separazione esplicita fra
stato online e telemetria post-hoc, vedi Sezione 8).

All'interno di una singola chiamata `agent(observation, configuration)`
viene costruito un insieme locale e temporaneo `reserved_targets` per
coordinare farmer e hands nello stesso step (evitare che due worker mirino
alla stessa tile nello stesso step); questo insieme non sopravvive oltre la
chiamata corrente.

---

## 4. Feature C2.1 effettivamente consumate

Elenco per `feature_id` (Feature Model C2.1, Sezione 4) realmente letto o
derivato a runtime — non dichiarazione nominale:

| Dominio | Feature consumate |
|---|---|
| TIME | `TMP-01` (step), `TMP-02` (day), `TMP-04` (turnsPerDay), `TMP-08`/`TMP-09` (giorni/step residui) |
| LAND | `FRM-01` (money), `FRM-03` (superficie totale), `MKT-06` (costo prossimo quadrante, ricostruito da `LAND_PRICES`/`LAND_ORDER` pubblici) |
| CROP | `CRP-01` (`tile.kind`), `CRP-02` (`tile.crop`), `CRP-04` (età), `CRP-08` (`first_yield_day`), `CRP-09`/`CRP-10` (readiness), `CRP-11` (`watered_today`), `CRP-12` (`consecutive_unwatered`) |
| CARE | `CAR-01`, `CAR-02` (`tile_care_due_condition`) |
| FERTILIZER | `FRT-01`, `FRT-02` (finestra attiva) |
| LIVESTOCK | `LIV-01` (specie), `LIV-05` (`fed_today`), `LIV-06` (`cared_today`), `LIV-07` (`consecutive_unfed`), `LIV-08` (allerta fuga), `LIV-10` (`fertilizer_available`), `LIV-11` (`yield_units` struttura), `LIV-STRUCT` (capacità strutturale) |
| WORKFORCE | `WRK-01`/`WRK-02` (identità worker), `WRK-03` (posizione), `WRK-04`/`WRK-05` (inventario worker), `WRK-08` (distanza dallo shed) |
| INVENTORY | `INV-01`/`INV-02` (shed), `INV-05` (semi) |
| MARKET | `MKT-01` (cassa), `MKT-02`/`MKT-03` (prezzi/inventario mercato), `MKT-04`/`MKT-05` (batch corrente/slot residui), `MKT-LIMIT` (limite ordini) |
| ELIGIBILITY | `ELG-01`/`ELG-02` (movimento/pass), `ELG-04` (`PLACE` a shed), `ELG-07`..`ELG-17` (guardie per-azione riflesse nelle condizioni di dispatch), `ELG-18`..`ELG-23` (idoneità ordini di mercato) |
| POLICY CONTEXT | `POL-WS` (zoning crop/livestock, agent-local), `POL-CAP` (capacità zootecnica servibile, derivata da buffer feed e struttura) |

Feature esplicitamente **non consumate** (dichiarate `NOT_USED` per questo
modello): telemetria post-hoc (`MKT-10`..`MKT-13`, tutte le `POST-*`),
`reserved_serviceable_before_deadline` (`POL-RES`) come prenotazione formale
— la sua funzione è assorbita implicitamente dalle guardie di orizzonte in
Sezione 6.3, senza una struttura dati dedicata.

---

## 5. Architettura del planner/dispatcher

Pipeline eseguita ad ogni chiamata, con moduli separati per responsabilità
(vedi commenti di sezione nel sorgente):

```text
1. SNAPSHOT       -> parsing via observation_contract, farm/private/market correnti
2. FEATURES       -> derivazione online (clock, tile views, readiness, care-due,
                      pressione di servizio, capacità strutturale/serviceable)
3. GOAL PLANNER   -> coda di opportunità (tile, categoria, priorità) scansionando
                      tutte le tile possedute; NON è una sequenza per step, è
                      ricalcolata da zero ad ogni chiamata sullo stato corrente
4. DISPATCH       -> assegnazione greedy worker-per-worker (farmer poi hands,
                      ordine coerente con l'esecuzione sequenziale dell'engine),
                      con reserved_targets locale alla chiamata
5. MARKET BUILDER -> guardie di HIRE / BUY_LAND / BUY_SEED / BUY_ANIMAL /
                      BUY_PRODUCT(WHEAT) / SELL, entro il limite di batch
6. TELEMETRY      -> contatori passivi, mai riletti dal planner
```

Nessuno stadio consulta un indice di step per decidere *cosa* fare; lo step e
il giorno vengono usati solo come feature di orizzonte residuo (Sezione 6.3)
e non come chiave di lookup.

---

## 6. Priorità e guardie

### 6.1 Coda di opportunità per tile (ordine di priorità)

L'ordine seguente è quello effettivamente implementato dopo l'audit
diagnostico di Sezione 9.1 (as-built, non la prima bozza): la priorità
grezza "cardinalità della categoria" (molte `PLANT_OPPORTUNITY` disponibili
contro un'unica `PLACE_ANIMAL_NEEDED`) si è dimostrata insufficiente da sola
a garantire che compiti rari ma a costo già affondato (bestiame acquistato,
strutture a costo zero) venissero mai serviti da un dispatcher greedy con
workforce limitata; l'ordine finale protegge esplicitamente quel costo
affondato.

1. `URGENT_WATER` — qualunque tile `PLANT` con `watered_today == False`,
   ordinata per `consecutive_unwatered` decrescente (le tile a rischio
   immediato di `WEED`, cioè con `tile_care_due_condition`, vengono servite
   per prime all'interno di questa categoria).
2. `FEED_NEEDED` — struttura occupata con `fed_today == False`.
3. `PLACE_ANIMAL_NEEDED` — un singolo animale già acquistato (in shed) in
   attesa di essere posizionato sulla struttura vuota compatibile più vicina
   (Sezione 6.2): capitale già speso, priorità alta per non sprecarlo.
4. `HARVEST_READY` — `crop_harvest_readiness` vera oppure resa animale
   accumulata (`yield_units > 0`) sulla struttura.
5. `RECOVERY_DIG` — tile in stato `LOST_WEED`.
6. `CARE_NEEDED` — struttura occupata con `cared_today == False` (valutata
   dopo `FEED_NEEDED`: un worker che deve nutrire un animale non lo cura
   nello stesso step, ma la cura resta in coda e viene raccolta da un
   worker successivo).
7. `COLLECT_FERTILIZER_READY` — struttura con `fertilizer_available == True`.
8. `BUILD_OPPORTUNITY` — tile `EMPTY_AVAILABLE` nella livestock zone, se la
   capacità strutturale corrente è sotto il target di quadrante (costo $0,
   quota piccola e autolimitata: precede `PLANT_OPPORTUNITY` per evitare che
   il pool molto più grande di tile crop-zone monopolizzi permanentemente i
   worker liberi).
9. `PLANT_OPPORTUNITY` — tile `EMPTY_AVAILABLE` nella crop zone (Sezione 7),
   se esiste una specie con semi disponibili e l'orizzonte biologico lo
   consente (Sezione 6.3).

Compiti dipendenti dall'inventario del worker (non tile-only) sono gestiti
nel dispatcher come logistica a due tappe (Sezione 6.2): `FEED_NEEDED` e
`PLACE_ANIMAL_NEEDED` compaiono nella coda sopra come categorie, ma la loro
risoluzione concreta (inseguire l'oggetto necessario allo shed oppure agire
subito) dipende dall'inventario corrente del worker assegnato.

### 6.2 Logistica a due tappe

- **Feed:** se esiste almeno un animale non nutrito e lo shed ha WHEAT
  disponibile, un worker viene instradato verso lo shed per un `PICKUP`
  batch (`min(shed_wheat, animali_non_nutriti)`), poi verso l'animale più
  vicino per `FEED`. La decisione è ricalcolata ogni step dall'inventario
  osservato del worker, non da un flag persistente.
- **Placement animale:** se lo shed contiene un animale acquistato e una
  struttura vuota corrispondente è disponibile, un worker viene instradato a
  `PICKUP` l'animale (batch fino al numero di strutture vuote compatibili) e
  poi a `PLACE` sulla struttura più vicina.
- **Fertilizzazione:** applicata opportunisticamente — se un worker porta già
  `FERTILIZER` in inventario (da una precedente `COLLECT_FERTILIZER` non
  ancora depositata) e transita su una tile `PLANT` la cui finestra
  (`fertilized_until_day < day`) è scaduta, applica `FERTILIZE` prima di
  proseguire. Non esiste una logistica dedicata di prelievo fertilizzante
  dallo shed: è un **limite dichiarato** del modello (Sezione 9).
- **Deposito:** un worker senza compito assegnato in questa chiamata, se
  porta inventario, si dirige verso la tile adiacente allo shed più vicina e
  deposita (`PLACE`, conservativo) la categoria di beni prioritaria
  (prodotti vendibili prima di `WHEAT` eccedente il buffer di sicurezza,
  prima di `FERTILIZER`).

### 6.3 Guardie di orizzonte ed endgame

- Un worker non pianifica `PLANT` di una specie se
  `giorni_residui < first_yield_day(specie) + margine_minimo` (guardia di
  `crop_horizon_alignment`): evita di avviare cicli che non possono
  monetizzare.
- `endgame.shutdown_days_remaining`: sotto questa soglia di giorni residui,
  si bloccano nuovi `BUY_LAND`, `HIRE`, `BUY_SEED`, `BUY_ANIMAL`,
  `BUILD_COOP`/`BUILD_PASTURE`. Manutenzione (`WATER`/`HARVEST`/`FEED`/
  `CARE`) e vendita continuano.
- `endgame.liquidation_days_remaining` (< shutdown): il buffer di sicurezza
  WHEAT si restringe a `animali_vivi × giorni_residui` (anziché al buffer
  fisso per animale) e la costruzione di ordini `SELL` copre l'intero shed
  eccedente quel buffer ridotto, entro lo slot di batch residuo.

### 6.4 Guardie di espansione Q1/Q2 (`H-CR2`)

`BUY_LAND` viene emesso solo se **tutte** le condizioni seguenti sono vere:

1. `len(unlocked_quadrants) < target_quadrants` (capacità di destinazione);
2. `money >= costo_prossimo_quadrante + land_purchase_reserve` (capitale);
3. `giorni_residui >= min_days_for_expansion_payback` (orizzonte residuo);
4. `service_pressure <= expansion_service_pressure_ceiling`, dove
   `service_pressure = tile_in_care_due / max(1, tile_PLANT_possedute)`
   (capacità di servizio corrente: non ci si espande se la superficie già
   attiva sta già collassando).

Nessuna delle quattro guardie fa riferimento a un giorno fisso o a un indice
di step precompilato.

### 6.5 Guardie di workforce (`HIRE`)

- `HIRE` viene emesso se `headcount_attuale < target_headcount(quadranti)` e
  `headcount_attuale < workforce.max_hands` e
  `money >= hire_reserve + costo_hire_stimato`, dove il costo stimato usa la
  formula pubblica Fibonacci (`ENGINE_VERIFIED`, `MKT-07`) applicata a
  `hires_today` osservato.
- Al massimo `workforce.hire_batch_limit_per_turn` ordini `HIRE` per step,
  per non far esplodere il costo marginale intra-day.

### 6.6 Guardie di mercato (fill/prezzo-aware)

- `BUY_PRODUCT WHEAT` viene emesso solo se lo stock di sicurezza è sotto
  soglia **e** il prezzo corrente quotato (`MKT-02`) è
  `<= livestock.wheat_buy_price_ceiling`; altrimenti la policy attende
  piuttosto che comprare a prezzo inflazionato (guardia fill/prezzo-aware
  osservabile, coerente con RQ1 del design comune senza importarne
  l'implementazione Codex).
- `SELL` non viene mai emesso per quantità 0, esclude sempre le specie
  animali (`GOOSE`/`COW`/`SHEEP`) in attesa di posizionamento — non sono
  merce, sono capitale già speso in attesa di `PLACE_ANIMAL_NEEDED` — e
  rispetta sempre il buffer di sicurezza WHEAT corrente (Sezione 6.3) fuori
  dalla finestra di liquidazione terminale.
- Gli ordini vengono costruiti fino al limite `MKT-05` (slot residui nel
  batch), calcolato a runtime dalla configurazione osservata
  (`maxMarketOrdersPerTurn`, fallback dal config file se assente).

---

## 7. Zoning spaziale crop/livestock (`POL-WS`)

Per ogni quadrante sbloccato, la policy riserva deterministicamente le prime
`livestock.structures_target_per_quadrant` tile in ordine di scansione
(`y` crescente poi `x` crescente, esclusa la tile adiacente allo shed del
quadrante) alla zona livestock; il resto del quadrante è zona crop. La
regola è puramente geometrica e ricalcolata ad ogni chiamata dai confini di
quadrante correnti (`board_size` osservato/di configurazione); non dipende
da alcuna sequenza o replay esterno.

---

## 8. Separazione stato online / telemetria post-hoc

- Le guardie di Sezione 6 leggono esclusivamente campi `ONLINE_OBSERVABLE`/
  `ONLINE_DERIVABLE` dell'osservazione corrente e la configurazione.
- Il ledger E17 (`agricola.core.e17_ledger`) è collegato **esternamente**
  dallo strumento di validazione tramite `instrument_policy`; la policy non
  lo importa né lo consulta per decidere.
- I contatori `_telemetry` (azioni per categoria, guardie attivate,
  fallback) sono scritti dopo la decisione e non vengono mai riletti prima
  della prossima decisione: sono strumentazione, non stato deliberativo.

---

## 9. Failure mode e fallback

- L'intera pipeline (Sezione 5) è eseguita dentro un blocco protetto.
  Qualunque eccezione (parsing malformato, indice fuori range, tipo
  inatteso) incrementa `technical_errors` e restituisce l'azione sicura
  `{"farmer": ["PASS"], "hands": [], "market": []}`.
- Limiti dichiarati (non falsificati, solo fuori scope in questa iterazione):
  - nessuna logistica dedicata di prelievo fertilizzante dallo shed
    (Sezione 6.2): il fertilizzante viene applicato solo se già in mano;
  - nessuna riassegnazione dinamica della zona crop/livestock dopo il primo
    sblocco del quadrante (lo zoning è fissato geometricamente, non
    ribilanciato in corsa);
  - l'assegnazione worker→tile è un greedy per-step (priorità poi distanza),
    non un solver di assegnamento globale: può produrre percorsi
    localmente non ottimi quando molte esigenze competono nello stesso
    step.

### 9.1 Iterazioni diagnostiche (audit as-built pre-freeze)

Tre difetti tecnici sono stati trovati e corretti durante lo sviluppo, prima
del benchmark development registrato nel report di implementazione. Sono
documentati qui per tracciabilità, non nascosti:

1. **Deadlock semi/opportunità:** la prima versione generava
   `PLANT_OPPORTUNITY` solo se esistevano già semi in stock, e decideva
   `BUY_SEED` solo se esisteva già una `PLANT_OPPORTUNITY` in coda — un
   ciclo che non si avvia mai da stock zero. Corretto separando il segnale
   "esiste una tile crop-zone libera sotto il target di fill" (usato da
   `BUY_SEED`) dalla verifica di fattibilità semi (usata per generare
   l'opportunità).
2. **Fame di priorità su `BUILD`/`PLACE`:** con `BUILD_OPPORTUNITY` alla
   priorità più bassa, il pool molto più numeroso di `PLANT_OPPORTUNITY`
   occupava permanentemente i worker liberi; nessuna struttura veniva mai
   costruita. Corretto con la rinumerazione di Sezione 6.1.
3. **Rivendita di animali acquistati:** `SELL` iterava su tutto lo shed
   ordinato alfabeticamente, includendo le specie animali appena comprate e
   in attesa di essere posizionate, vendendole di nuovo prima che un worker
   potesse raggiungerle. Corretto escludendo esplicitamente le chiavi in
   `ANIMALS` dalla scansione di `_sell_orders`.

Dopo le correzioni, un'unica variante di calibrazione cassa è stata provata
e adottata (non falsificata, non scartata): `hire_reserve` e
`land_purchase_reserve` erano fissati a valori (`300`/`600`) superiori al
flusso di cassa realmente osservato nelle prime run, creando una trappola in
cui la cassa oscillava sotto la soglia di riserva e bloccava ogni `HIRE`
successivo (workforce bloccata a 1 worker, manutenzione insufficiente).
Ridotti a `50`/`300` nella configurazione consegnata. Nessuna variante è
stata scartata selezionando sull'holdout; tutte le iterazioni hanno usato
esclusivamente il seed development `26090101`.

---

## 10. Target e criteri di falsificazione

Target ereditati dal prompt operativo (gate desiderati, non promessi):

```text
TECHNICAL_ERRORS == 0
INVALID_BATCHES == 0
STRATEGIC_INDEPENDENCE == PASS
STATE_REACTIVITY_TEST == PASS
LEDGER_ACTION_PARITY == PASS
ANIMAL_ESCAPES == 0
MAX_QUADRANTS == 3 su tutte le run ammesse
DEVELOPMENT_MEAN_FINAL_MONEY >= 50000
```

Criteri di falsificazione dichiarati prima di osservare il risultato:

- **`H-CR1` falsificata** se, su seed development contro `INERT_PASS_POLICY`,
  si osservano fughe derivate (`ANIMAL_ESCAPES > 0`) o una quota di tile
  `LOST_WEED` terminali non nulla nonostante la guardia `URGENT_WATER` a
  priorità massima: indicherebbe che il dispatch greedy non riesce a
  garantire manutenzione tempestiva neanche in assenza di contesa.
- **`H-CR2` falsificata** se l'espansione condizionata non raggiunge comunque
  3 quadranti entro l'orizzonte su seed development senza contesa, o se li
  raggiunge ma la pressione di servizio post-espansione collassa
  (`service_pressure` resta sopra soglia per più giorni consecutivi dopo
  ogni `BUY_LAND`).
- **`H-CR3` falsificata** se il buffer/liquidazione reattivi non riducono,
  rispetto a un buffer costante equivalente misurato nello stesso run,
  l'inventario terminale invenduto o il rischio di fuga per fame nella
  finestra di liquidazione.

Se un gate economico non è raggiunto, il report di implementazione
(Sezione finale del processo) documenta diagnosi e varianti provate, senza
alterare il risultato osservato.
