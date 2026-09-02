# ONTOLOGY — Ontologia canonica comune Kaggriculture

- **Fase:** E14.5 — Consolidamento canonico
- **Stato:** CANONICAL
- **Data:** 2026-08-29
- **Ambito:** vocabolario semantico comune per Antigravity, Codex e Copilot
- **Destinazione repository:** `docs/foundation/ontology/ONTOLOGY.md`

---

## 1. Scopo e governance

Questa ontologia definisce un vocabolario comune per descrivere i fenomeni rilevanti di Kaggriculture e consentire confronti coerenti tra i modelli Antigravity, Codex e Copilot.

L'ontologia **non** definisce:
- ranking dei fattori;
- impact;
- confidence del singolo modello;
- policy;
- soglie strategiche;
- priorità di dispatch;
- timing prescrittivi;
- architetture implementative;
- scelte di build o submission.

### 1.1 Principio OR

L'ontologia è l'**unione semantica (OR)** dei fenomeni rilevanti individuati dai tre modelli, non l'intersezione dei fenomeni sui quali i tre concordano.

Un concetto può quindi essere canonico anche se:
- è utilizzato da un solo modello;
- gli altri modelli lo classificano `NOT_USED`;
- i modelli gli attribuiscono importanza o confidence differenti;
- la sua evidenza è ancora `PROVISIONAL`.

L'ammissione richiede:
1. neutralità semantica;
2. distinguibilità del fenomeno;
3. assenza di policy leakage;
4. tracciabilità minima dell'origine o dell'evidenza.

Il consenso fra i tre modelli **non è requisito di ammissione**.

### 1.2 Mapping dei modelli

Ogni `MODEL_SPEC.md` può mappare ciascun concetto canonico come:

- `USED`
- `PARTIAL`
- `NOT_USED`

Il mapping semantico fra formulazioni locali e concetto canonico può essere:

- `FULL`
- `PARTIAL`
- `ABSENT`
- `BROADER`
- `NARROWER`
- `CONFLICT`

La presenza nell'ontologia non obbliga alcun modello ad attribuire importanza al concetto.

---

## 2. Tassonomia

I tipi canonici sono:

- `STATE`
- `FLOW`
- `CAPACITY`
- `COST`
- `REVENUE`
- `EFFICIENCY`
- `CONSTRAINT`
- `TIMING`
- `INTERACTION`
- `DERIVED_METRIC`
- `OUTCOME`

Un concetto può avere più tipi quando necessario.

### 2.1 Evidenza e osservabilità sono assi distinti

Lo **stato dell'evidenza** indica quanto è supportata l'esistenza o la caratterizzazione del fenomeno:

- `REPLAY_SUPPORTED`
- `LOCAL_SUPPORTED`
- `ENGINE_RULE_SUPPORTED`
- `KAGGLE_SUPPORTED`
- `MIXED`
- `PROVISIONAL`

L'**osservabilità** indica invece come il fenomeno o la relativa metrica può essere misurato:

- `AVAILABLE_FROM_REPLAY`
- `DERIVABLE_FROM_REPLAY`
- `REQUIRES_EXTRA_TELEMETRY`
- `ENGINE_ONLY`
- `NOT_CURRENTLY_OBSERVABLE`

Un concetto può essere canonico e contemporaneamente `PROVISIONAL` o `NOT_CURRENTLY_OBSERVABLE`.

---

# 3. Concetti canonici

**Canonical concept registry: 64 `concept_id`.**

Solo i `concept_id` definiti nelle sezioni A–H di questo capitolo appartengono al registry canonico.
I nomi riportati successivamente nella sezione 7 sono esclusivamente termini storici esclusi, fusi o non canonici e **NON devono essere mappati come `concept_id` canonici nei MODEL_SPEC**.


## A. Terreno e superficie produttiva

### `land_surface_total`
**Tipo:** `STATE / CAPACITY`  
Superficie totale posseduta o sbloccata, indipendentemente dall'uso produttivo.

### `land_purchase_timing`
**Tipo:** `TIMING`  
Momento in cui viene acquisita o sbloccata nuova superficie.

### `activated_land_surface`
**Tipo:** `STATE`  
Porzione della superficie posseduta convertita a un uso produttivo effettivo, inclusi crop e pasture.

### `crop_surface_maintained`
**Tipo:** `STATE / DERIVED_METRIC`  
Superficie coltivata mantenuta in condizioni compatibili con la prosecuzione del ciclo produttivo. La formula operativa deve dichiarare i criteri di maintenance utilizzati.

### `pasture_surface_maintained`
**Tipo:** `STATE / DERIVED_METRIC`  
Superficie a pasture effettivamente mantenuta e funzionale al subsystem livestock.

### `maintained_productive_surface`
**Tipo:** `STATE / DERIVED_METRIC`  
Aggregato della superficie produttiva effettivamente mantenuta. Deve essere accompagnato dal breakdown crop/pasture.

### `monetized_productive_output`
**Tipo:** `REVENUE / DERIVED_METRIC`  
Output derivante dalla superficie produttiva che è stato effettivamente convertito in valore monetario.

### `land_activation_payback`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`  
Tempo o rendimento con cui il costo di acquisizione/attivazione del terreno viene recuperato attraverso output monetizzato. La formula deve essere esplicitata quando utilizzata.

### `pasture_arable_surface_tradeoff`
**Tipo:** `INTERACTION`  
Competizione per la superficie fra utilizzo arabile e utilizzo pasture.

---

## B. Workforce, dispatch e logistica

### `workforce_headcount`
**Tipo:** `STATE`  
Numero di worker disponibili/assunti in un dato intervallo.

### `worker_capacity_available`
**Tipo:** `CAPACITY`  
Capacità teorica di lavoro disponibile in un intervallo definito. Il denominatore temporale e l'eventuale inclusione del Farmer devono essere dichiarati.

### `hire_order_scheduling`
**Tipo:** `TIMING`  
Distribuzione temporale degli ordini di assunzione.

### `marginal_hire_payback`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`  
**Evidence status:** `PROVISIONAL`  
Rendimento marginale attribuibile a un'unità addizionale di workforce. Richiede una metodologia controfattuale o di attribuzione esplicita.

### `productive_action_share`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`  
Quota delle azioni worker classificata come produttiva rispetto al denominatore dichiarato. La tassonomia delle azioni deve essere condivisa.

### `movement_overhead`
**Tipo:** `COST / EFFICIENCY`  
Quota o quantità di capacità worker consumata dal movimento. Non equivale automaticamente a spreco.

### `necessary_transit_fraction`
**Tipo:** `DERIVED_METRIC / EFFICIENCY`  
Quota del movimento attribuibile a transito funzionale al completamento di un'azione produttiva o logistica. La regola di attribuzione e la finestra temporale devono essere dichiarate. Un modello può mapparlo `NOT_USED`.

### `routing_completion_efficiency`
**Tipo:** `EFFICIENCY`  
Capacità del routing di trasformare movimento e posizionamento in completamento di loop produttivi/logistici.

### `action_dispatch_failure`
**Tipo:** `CONSTRAINT / FLOW`  
Dispatch che non produce progresso utile, includendo quando distinguibili azioni invalide, ridondanti e loop ripetuti senza progresso.

### `worker_action_monetization_rate`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`  
Valore monetizzato per unità di attività worker.

Per E15 devono essere riportate almeno due forme:

1. **Macro:** ricavi realizzati / tutte le azioni worker;
2. **Netta:** ricavi realizzati / azioni produttive e logistiche utili, escludendo il puro movimento.

Le categorie del denominatore devono essere dichiarate.

---

## C. Crop production e care

### `crop_care_action_flow`
**Tipo:** `FLOW`  
Flusso aggregato delle azioni necessarie alla gestione delle colture. È parent semantico dei flussi atomici di planting, watering e harvesting.

### `planting_action_flow`
**Tipo:** `FLOW`  
Flusso delle azioni `PLANT`.

### `watering_execution_rate`
**Tipo:** `FLOW / EFFICIENCY`  
Tasso o volume delle azioni `WATER`. Rimane un concetto first-class distinto dall'intera pipeline crop-care.

### `watering_continuity`
**Tipo:** `TIMING / FLOW`  
Continuità temporale dell'irrigazione sulle colture attive.

### `crop_harvest_action_flow`
**Tipo:** `FLOW`  
Flusso delle azioni `HARVEST`.

### `crop_care_completion_rate`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`  
Quota del fabbisogno di crop care effettivamente completata. Quando utilizzata in E15 deve avere un denominatore operativo esplicito.

### `crop_decay_risk_window`
**Tipo:** `TIMING / CONSTRAINT`  
Finestra temporale in cui care insufficiente, inclusa la mancata irrigazione consecutiva quando prevista dall'engine, espone la coltura a stagnazione, decadimento o perdita.  
**Evidence status:** mantenere qualificato secondo la verifica effettiva delle regole engine.

### `crop_horizon_alignment`
**Tipo:** `TIMING / INTERACTION`  
Compatibilità tra orizzonte residuo dell'episodio e tempo necessario al completamento/monetizzazione del ciclo colturale.

### `crop_revenue_mix`
**Tipo:** `REVENUE`  
Composizione del ricavo derivante dalle diverse colture. Quantità venduta e valore monetario devono rimanere distinguibili.

---

## D. Feed, Wheat e livestock

### `feed_availability`
**Tipo:** `STATE / CONSTRAINT`  
Disponibilità fisica di feed. Quando possibile distinguere shed inventory, worker inventory e produzione futura.

### `feed_security_buffer`
**Tipo:** `STATE / CAPACITY`  
Copertura del fabbisogno di feed rispetto alla domanda attesa, senza soglia canonica prescrittiva.

### `feed_market_dependency`
**Tipo:** `FLOW / COST`  
Quota o grado di dipendenza dall'approvvigionamento di feed attraverso il mercato.

### `feed_market_expenditure`
**Tipo:** `COST`  
Spesa monetaria sostenuta per l'acquisto di feed.

### `wheat_operating_flow`
**Tipo:** `FLOW / INTERACTION`  
Flusso operativo del Wheat nei suoi diversi ruoli: seed, crop output, feed, inventory, acquisto, vendita e fonte di cassa. Non prescrive buy, autarky o una loro combinazione.

### `market_churn_cost`
**Tipo:** `COST / DERIVED_METRIC`  
**Evidence status:** `PROVISIONAL`  
Costo associato a cicli di acquisto/vendita della stessa commodity che distruggono valore rispetto al suo uso produttivo o alla detenzione.

### `livestock_headcount`
**Tipo:** `STATE`  
Numero di animali, preferibilmente disaggregato per specie.

### `livestock_capacity`
**Tipo:** `CAPACITY`  
Capacità sostenibile del subsystem livestock rispetto a pasture, feed, workforce e altri vincoli rilevanti. La formula deve essere dichiarata quando quantificata.

### `pasture_capacity_alignment`
**Tipo:** `INTERACTION`  
Allineamento fra superficie/capacità pasture e livestock supportato.

### `livestock_product_flow`
**Tipo:** `FLOW / REVENUE`  
Flusso di produzione, raccolta e monetizzazione dei prodotti primari livestock, quali Milk e Wool.

### `species_margin_differential`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`  
Differenza di rendimento o margine fra specie, considerando quando disponibile costi, feed, timing e output.

### `fertilizer_byproduct_flow`
**Tipo:** `FLOW / REVENUE`  
Flusso del Fertilizer generato come byproduct del subsystem livestock, distinto da Milk e Wool.

La sorgente ontologica è la presenza/capacità biologica del livestock, non `livestock_product_flow`.

---

## E. Capitale, mercato, conversione e reinvestimento

### `market_transaction_value`
**Tipo:** `FLOW / DERIVED_METRIC`  
Valore monetario associato a una transazione BUY/SELL.

Quando ricostruito deve qualificare la fonte del prezzo, ad esempio:
- `observed`;
- `reconstructed`;
- `base_price_estimate`.

È primitive comune per rendere confrontabili expenditure, revenue e price-realization metrics.

### `operating_cash_buffer`
**Tipo:** `STATE / CAPACITY`  
Cassa mantenuta disponibile per sostenere obblighi e operatività corrente, senza imporre una soglia canonica.

### `deployable_capital_window`
**Tipo:** `TIMING / STATE`  
Finestra in cui il capitale disponibile eccede gli obblighi operativi definiti e può essere impiegato in investimenti. La formula degli obblighi deve essere dichiarata.

### `asset_liquidity_lag`
**Tipo:** `TIMING / DERIVED_METRIC`  
**Evidence status:** `PROVISIONAL`  
Ritardo fra immobilizzazione di capitale in un asset e ritorno di liquidità attribuibile all'asset.

### `inventory_to_cash_conversion`
**Tipo:** `FLOW / EFFICIENCY`  
Conversione dell'inventory fisico in cassa attraverso il mercato.

### `market_sellthrough_lag`
**Tipo:** `TIMING`  
Ritardo tra disponibilità dell'output vendibile e vendita effettiva.

### `unsold_inventory_value`
**Tipo:** `STATE / DERIVED_METRIC`  
Valore attribuito all'inventory terminale o invenduto.

La **quantità** di inventory e la sua **valorizzazione** devono essere mantenute distinte; la valorizzazione deve dichiarare il prezzo utilizzato.

### `reinvestment_cash_flow`
**Tipo:** `FLOW`  
Cassa realizzata che torna disponibile per il reinvestimento nel ciclo produttivo.

### `product_mix_revenue`
**Tipo:** `REVENUE`  
Ripartizione dei ricavi fra categorie produttive. Deve conservare il breakdown sottostante.

### `price_realization_variance`
**Tipo:** `DERIVED_METRIC`  
**Evidence status:** `PROVISIONAL`  
Scostamento tra prezzo di riferimento dichiarato e prezzo effettivamente realizzato.

### `dynamic_market_price_elasticity`
**Tipo:** `CONSTRAINT / INTERACTION`  
Fenomeno per cui prezzi o condizioni economiche di mercato variano in relazione ai volumi/ordini scambiati secondo le regole dell'environment.  
È concetto canonico anche se un modello lo mappa `NOT_USED`. Lo stato dell'evidenza deve essere qualificato separatamente in base alla verifica engine/transaction ledger.

---

## F. Endgame e integrità dell'inventory

### `shed_inventory_integrity`
**Tipo:** `STATE / CONSTRAINT`  
Integrità e persistenza dell'inventory depositato nello shed.

### `contract_inventory_loss`
**Tipo:** `CONSTRAINT`  
Perdita di inventory associata alla scadenza/reset del contratto worker quando i beni non sono stati trasferiti allo storage persistente secondo le regole dell'environment.

**Canonical status:** incluso.  
**Evidence status:** `ENGINE_RULE_SUPPORTED` secondo le verifiche E14 disponibili; resta possibile correggere tale status se successiva verifica dell'engine lo falsifica senza rimuovere automaticamente il concetto dall'ontologia.

### `endgame_shutdown_timing`
**Tipo:** `TIMING`  
Momento in cui viene ridotta o interrotta la creazione di nuovi cicli produttivi in funzione dell'orizzonte residuo. Non prescrive un giorno canonico.

### `endgame_inventory_liquidation`
**Tipo:** `FLOW / TIMING`  
Conversione intenzionale delle scorte in cassa prima della conclusione dell'episodio.

---

## G. Condizione del campo e recovery

### `field_cleanliness_state`
**Tipo:** `STATE`  
Stato oggettivo della presenza/distribuzione di weeds o altre condizioni di campo rilevanti.

### `weed_backlog_cost`
**Tipo:** `COST / DERIVED_METRIC`  
Costo/opportunity cost associato al recupero del backlog di weeds, distinguendo quando possibile superficie produttiva e fallow.

---

## H. Vincoli, diagnostica e outcome

### `market_order_batch_limit`
**Tipo:** `CONSTRAINT`  
Limite dell'environment al numero di ordini di mercato processabili/applicabili in una singola unità decisionale.

**Canonical status:** incluso.  
**Evidence status:** `ENGINE_RULE_SUPPORTED` secondo le verifiche E14 disponibili; può essere corretto successivamente se l'ispezione dell'engine produce evidenza contraria.

Il limite vincola il ritmo di acquisizione/allocazione degli ordini e **non** riduce direttamente la capacità lavorativa già acquisita.

### `action_order_slot_pressure`
**Tipo:** `CONSTRAINT / DERIVED_METRIC`  
**Evidence status:** `PROVISIONAL`  
Pressione esercitata dalla domanda di ordini sugli slot disponibili. È distinta dal limite strutturale stesso.

### `state_capacity_alignment`
**Tipo:** `INTERACTION / DERIVED_METRIC`  
**Evidence status:** `PROVISIONAL`  
Metrica composita dell'allineamento fra stati e capacità rilevanti. Quando usata deve dichiarare esplicitamente sotto-metriche, pesi e formula; non può incorporare implicitamente una policy.

### `local_kaggle_fidelity_gap`
**Tipo:** `CONSTRAINT / DERIVED_METRIC`  
Scostamento fra comportamento/performance locale e comportamento/performance Kaggle. Qualifica le conclusioni ottenute da benchmark locali.

### `operational_divergence_onset`
**Tipo:** `TIMING / DERIVED_METRIC`  
Primo momento in cui due strategie manifestano una divergenza operativa definita. La dimensione osservata e la soglia devono essere dichiarate.

### `economic_lock_in_onset`
**Tipo:** `TIMING / DERIVED_METRIC`  
Momento successivo in cui una divergenza economica raggiunge una soglia/persistenza definita tale da configurare lock-in diagnostico. Non è sinonimo di `operational_divergence_onset`.

### `final_money_outcome`
**Tipo:** `OUTCOME`  
Valore monetario terminale utilizzato come risultato finale. Non costituisce da solo una spiegazione causale.

---

# 4. Relazioni canoniche

Le relazioni descrivono struttura o ipotesi diagnostiche. Non costituiscono automaticamente prova causale.

- `land_surface_total enables activated_land_surface`
- `activated_land_surface enables maintained_productive_surface`
- `maintained_productive_surface enables monetized_productive_output`
- `worker_capacity_available enables productive_action_share`
- `movement_overhead constrains worker_action_monetization_rate`
- `necessary_transit_fraction qualifies movement_overhead`
- `routing_completion_efficiency qualifies movement_overhead`
- `action_dispatch_failure constrains productive_action_share`
- `watering_execution_rate contributes_to crop_care_action_flow`
- `watering_continuity enables crop_care_completion_rate`
- `crop_care_completion_rate enables crop_revenue_mix`
- `feed_availability constrains livestock_product_flow`
- `feed_market_dependency interacts_with operating_cash_buffer`
- `pasture_capacity_alignment enables livestock_capacity`
- `livestock_headcount enables fertilizer_byproduct_flow`
- `livestock_capacity enables fertilizer_byproduct_flow`
- `market_transaction_value measures feed_market_expenditure`
- `market_transaction_value measures product_mix_revenue`
- `inventory_to_cash_conversion produces reinvestment_cash_flow`
- `operating_cash_buffer constrains deployable_capital_window`
- `deployable_capital_window enables land_purchase_timing`
- `asset_liquidity_lag constrains reinvestment_cash_flow`
- `market_sellthrough_lag constrains reinvestment_cash_flow`
- `endgame_shutdown_timing interacts_with endgame_inventory_liquidation`
- `field_cleanliness_state interacts_with maintained_productive_surface`
- `market_order_batch_limit constrains hire_order_scheduling`
- `market_order_batch_limit interacts_with action_order_slot_pressure`
- `local_kaggle_fidelity_gap qualifies local_performance_claims`

## 4.1 Relazioni deliberatamente non adottate

Non viene adottata:

`market_order_batch_limit constrains worker_capacity_available`

perché confonderebbe il ritmo di acquisizione della workforce con la capacità dei worker già disponibili.

Non viene adottata:

`livestock_product_flow produces fertilizer_byproduct_flow`

perché Fertilizer deriva dal subsystem biologico livestock, non dal flusso commerciale Milk/Wool.

---

# 5. Separazioni canoniche non negoziabili

La normalizzazione E14 ha esplicitamente rifiutato le seguenti equivalenze:

1. terreno posseduto = terreno produttivo;
2. worker count = throughput;
3. crop care = WATER;
4. feed security = feed autarky;
5. livestock count = livestock economic value;
6. inventory prodotto = revenue;
7. movement = waste;
8. clean field = profitable field;
9. operational divergence = economic lock-in;
10. local score = Kaggle validity.

Queste separazioni fanno parte della semantica canonica.

---

# 6. Concetti model-local esclusi dall'ontologia

Restano fuori dall'ontologia, salvo futura emersione come fenomeni neutrali:

- fixed herd targets;
- fixed Q1/Q2 days;
- autarky-first doctrine;
- dispatch priority rules;
- fixed cash reserves;
- hard-coded worker counts;
- candidate names;
- strategy class names;
- submission/build paths;
- implementation architecture;
- ranking;
- impact;
- confidence;
- policy thresholds.

---

# 7. Termini storici esclusi, fusi o non canonici

**Questa sezione NON fa parte del canonical concept registry.**
I nomi riportati qui servono esclusivamente a conservare la tracciabilità delle decisioni E14 e non devono comparire come righe canoniche nella sezione `Canonical Ontology Mapping` dei `MODEL_SPEC.md`.

La regola OR non implica proliferazione incontrollata. Le formulazioni che non identificano un fenomeno distinto restano escluse o assorbite.

**Termine storico: `action_retry_penalty`**
**Stato:** `MERGED` in `action_dispatch_failure` salvo futura evidenza di una penalità engine distinta.

**Termine storico: `tile_utility_decay`**
**Stato:** `NOT_CANONICAL`  
Attualmente coperto da fenomeni più specifici quali `crop_decay_risk_window`, `field_cleanliness_state` e `weed_backlog_cost`.

**Termine storico: `decision_lag_from_observed_market_state`**
**Stato:** `NOT_CANONICAL`  
Attualmente descrive principalmente comportamento interno dell'agente e richiede telemetry decisionale specifica.

**Termine storico: `late_game_sell_pressure`**
**Stato:** `MERGED` in `endgame_inventory_liquidation`, `market_sellthrough_lag` e interazioni con il mercato.

**Termine storico: `capital_lock_in_risk`**
**Stato:** `MERGED` in `asset_liquidity_lag`, `operating_cash_buffer` e `deployable_capital_window`.

**Termine storico: `spatial_shed_congestion_penalty`**
**Stato:** `MERGED/PARTIAL` in `movement_overhead` e `routing_completion_efficiency`. Può essere promosso in futuro se emerge evidenza di un fenomeno spaziale distinto.

---

# 8. Contratto minimo di telemetry E15

E15 deve distinguere sempre:
- osservazione diretta;
- derivazione;
- stima;
- regola engine;
- informazione non osservabile.

## 8.1 Outcome ed economia

Registrare almeno:
- `final_money_outcome`;
- ricavi realizzati;
- costi/spese di mercato;
- `market_transaction_value` con provenance del prezzo;
- ricavi per categoria/prodotto;
- inventory terminale in quantità;
- `unsold_inventory_value` con metodo di valorizzazione.

## 8.2 Terreno

Registrare:
- `land_surface_total` nel tempo;
- `activated_land_surface`;
- `crop_surface_maintained`;
- `pasture_surface_maintained`;
- `maintained_productive_surface`.

## 8.3 Workforce e routing

Registrare:
- `workforce_headcount`;
- capacità worker disponibile;
- azioni totali;
- azioni per categoria;
- movement;
- dispatch failure quando identificabile;
- `productive_action_share`;
- entrambe le forme di `worker_action_monetization_rate`;
- `necessary_transit_fraction` quando il modello/analizzatore dispone di una regola di attribuzione esplicita.

## 8.4 Crop

Registrare:
- PLANT/WATER/HARVEST/DIG per giorno;
- `watering_execution_rate`;
- `watering_continuity`;
- output crop;
- revenue crop per prodotto;
- `crop_care_completion_rate` solo se il denominatore è definibile.

## 8.5 Feed e livestock

Registrare:
- livestock per specie;
- feed disponibile;
- feed acquistato;
- `feed_market_expenditure`;
- Milk/Wool/Fertilizer prodotti e venduti;
- pasture utilization quando derivabile.

## 8.6 Capitale e mercato

Registrare:
- traiettoria cash;
- timing degli acquisti;
- produced inventory vs sold inventory;
- `market_sellthrough_lag` quando osservabile;
- reinvestment cash;
- prezzi osservati/ricostruiti;
- `market_order_batch_limit` e pressione sugli slot quando misurabile.

## 8.7 Diagnostica

Registrare:
- `operational_divergence_onset` con definizione della soglia;
- `economic_lock_in_onset` con soglia e persistenza;
- scope di validità locale/Kaggle.

Se una metrica necessaria a valutare un concetto non è osservabile, il match deve produrre `INCONCLUSIVE` per quel concetto anziché inferirlo dal solo risultato finale.

---

# 9. Vocabolario di interpretazione E15

I verdict match-level sono:

- `SUPPORTED`
- `WEAKENED`
- `NOT_DISCRIMINATED`
- `CONFOUNDED`
- `INCONCLUSIVE`

Questi verdict:
- riguardano l'evidenza prodotta dal singolo match;
- non modificano automaticamente lo status canonico del concetto;
- non equivalgono al ranking del concetto nel singolo modello;
- non trasformano una vittoria in validazione globale del modello.

---

# 10. Regole per l'adozione nei MODEL_SPEC

Dopo l'adozione di questo documento:

1. ciascun agente usa i `concept_id` canonici per fenomeni semanticamente equivalenti;
2. ciascun agente mantiene autonomamente ranking, impact, confidence e policy;
3. un agente può usare `NOT_USED` per concetti canonici che non considera rilevanti;
4. un agente può contestare in futuro un concetto sulla base di nuova evidenza;
5. una contestazione futura modifica prima evidence status/definition/mapping e non cancella automaticamente il concetto;
6. nuovi fenomeni possono essere aggiunti all'ontologia se soddisfano il principio OR e i criteri di ammissione;
7. non si devono riscrivere retroattivamente le valutazioni pre-match dopo E15.

---

# 11. Freeze per E15

Prima del torneo E15 devono essere congelati:

- `docs/model_specs/ONTOLOGY.md`;
- snapshot pre-match dei tre `MODEL_SPEC.md`;
- ranking/confidence pre-match dei singoli modelli;
- tre submission candidate;
- definizioni delle metriche E15 effettivamente utilizzate.

Il freeze serve a impedire che aggiornamenti post-match riscrivano le ipotesi precedenti.

---

# 12. Provenienza E14

Questa ontologia consolida:

- `docs/model_specs/ONTOLOGY_DRAFT.md` — E14.3;
- `docs/model_specs/antigravity/ONTOLOGY_VERIFICATION.md` — E14.4;
- `docs/model_specs/codex/ONTOLOGY_VERIFICATION.md` — E14.4;
- `docs/model_specs/copilot/ONTOLOGY_VERIFICATION.md` — E14.4.

Decisioni principali della sintesi E14.5:
- fissato il canonical concept registry a **64 concept_id**;
- confermata l'architettura E14.3;
- adottato formalmente il principio OR;
- confermate le separazioni capacity/throughput/monetization;
- adottati due denominatori per `worker_action_monetization_rate`;
- mantenuti `contract_inventory_loss`, `market_order_batch_limit` e `dynamic_market_price_elasticity` come concetti canonici;
- `contract_inventory_loss` e `market_order_batch_limit` qualificati come engine constraints sulla base delle verifiche E14 disponibili;
- aggiunto `market_transaction_value`;
- aggiunto `necessary_transit_fraction` come metrica derivata opzionale;
- corretta la relazione di `fertilizer_byproduct_flow`;
- separati formalmente evidence status e observability;
- preservata l'indipendenza dei tre modelli.

---

**Fine del documento canonico E14.5.**
