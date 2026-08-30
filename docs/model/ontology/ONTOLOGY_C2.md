# ONTOLOGY C2 — Ontologia canonica comune Kaggriculture

- **Fase:** Foundation C2 Candidate (post Foundation Reconciliation R1)
- **Stato:** CANDIDATE C2 / NOT FROZEN
- **Data:** 2026-08-30
- **Ambito:** Vocabolario semantico comune per Antigravity, Codex e Copilot
- **Fonte normativa:** Foundation Reconciliation R1 (Codex arbitrato)
- **Baseline di riferimento:** `docs/model/ontology/ONTOLOGY.md` (C1)
- **Destinazione repository:** `docs/model/ontology/ONTOLOGY_C2.md`

---

## 1. Scopo e governance

Questa ontologia definisce il vocabolario comune e neutrale per descrivere i fenomeni osservabili, strutturali e dinamici del dominio simulato di **Kaggriculture**, consentendo un confronto rigoroso, comparabile e falsificabile tra i modelli decisionali indipendenti di Antigravity, Codex e Copilot.

L'ontologia risponde alla domanda fondamentale:
> **Che cosa esiste nel dominio e che cosa significa?**

L'ontologia **NON definisce né prescrive**:
- ranking, pesi o importanza dei fattori nel processo decisionale;
- impatto relativo o confidence dei singoli modelli;
- policy, regole di dispatching o priorità di schedulazione;
- soglie strategiche o parametri numerici operativi;
- working-set o routing specifici;
- contratti di consumo o matrici di mapping per-consumer;
- architetture di implementazione, codice o submission.

### 1.1 Principio OR e criteri di ammissione

L'ontologia è l'**unione semantica (OR)** dei fenomeni rilevanti del dominio identificati e verificati, non l'intersezione su cui tutti i modellatori concordano.

Un concetto appartiene al registry canonico se soddisfa quattro criteri:
1. **Neutralità semantica:** descrive proprietà del sistema o classi informative, non prescrizioni di policy o scelte di convenienza locale;
2. **Distinguibilità fenomenologica:** identifica un meccanismo o una grandezza non riducibile ad altri concetti esistenti;
3. **Assenza di policy leakage:** non codifica euristiche proprietarie o assunzioni di strategia;
4. **Tracciabilità empirica o engine grounding:** dispone di una definizione fondata sulle regole dell'ambiente (`ENGINE_VERIFIED`), verificata empiricamente (`EMPIRICALLY_VERIFIED`), formalmente derivata (`DERIVED`) o esplicitamente dichiarata come provvisoria (`PARTIALLY_KNOWN`).

Il consenso tra tutti i modeler **non è requisito di ammissione**.

### 1.2 Mapping dei modelli e liceità di `NONE_DIRECT`

Ciascun `MODEL_SPEC` e ciascun livello downstream mappa i concetti canonici secondo la propria architettura decisionale:

- **Usage:** `USED`, `PARTIAL`, `NOT_USED`
- **Mapping semantico:** `FULL`, `PARTIAL`, `ABSENT`, `BROADER`, `NARROWER`, `CONFLICT`

**Liceità di `NONE_DIRECT`:** non esiste e non deve essere forzata una biiezione 1:1 tra Ontologia e Feature Model. Grandezze di conteggio runtime, derivazioni tecniche di clock o variabili puramente computazionali possono legittimamente avere mapping `NONE_DIRECT` verso l'ontologia se non costituiscono un concetto semantico generale riusabile.

---

## 2. Tassonomia ed Evidence Classification

### 2.1 Tipi ontologici primari

I tipi canonici assegnati ai concetti sono:
- `STATE`: proprietà discreta o continua dello stato del sistema o degli attori;
- `FLOW`: tasso di transizione, volume di azioni o movimento di entità/risorse nel tempo;
- `CAPACITY`: limite massimo, ampiezza o vincolo dimensionale di una risorsa o di un sottosistema;
- `COST`: spesa monetaria, consumo di risorse o overhead non reversibile;
- `REVENUE`: generazione monetaria da transazioni di mercato o liquidazione;
- `EFFICIENCY`: rapporto di rendimento tra output ottenuto e input/risorse impiegate;
- `CONSTRAINT`: regola o vincolo strutturale imposto dall'environment o dalla geometria della simulazione;
- `TIMING`: momento di accadimento, intervallo o coordinamento temporale di un evento/azione;
- `INTERACTION`: accoppiamento o trade-off strutturato tra due o più sottosistemi;
- `DERIVED_METRIC`: grandezza computata da stati, flussi o eventi elementari;
- `OUTCOME`: risultato terminale o metrica di sintesi aggregata dell'episodio.

### 2.2 Assi di classificazione epistemica

L'ontologia separa rigorosamente lo stato dell'evidenza dall'osservabilità decisionale:

#### Asse dell'Evidenza (`evidence_status`):
- `ENGINE_VERIFIED`: comportamento o formula verificata direttamente nel codice sorgente dell'ambiente simulato (`kaggriculture.py`);
- `EMPIRICALLY_VERIFIED`: fenomeno osservato e replicato sperimentalmente su seed/match controllati;
- `DERIVED`: costrutto concettuale rigorosamente derivato da definizioni primitive senza gradi di libertà non specificati;
- `PARTIALLY_KNOWN`: fenomeno la cui dinamica qualitativa è accertata ma i cui parametri/formule esatte presentano margini da completare;
- `NOT_ANALYZED`: concetto ipotizzato o preliminare non ancora sottoposto a verifica diretta.

#### Asse dell'Osservabilità (`observability`):
- `ONLINE_OBSERVABLE`: campo direttamente esposto dallo state dictionary dell'engine al momento decisionale;
- `ONLINE_DERIVABLE`: grandezza computabile in tempo reale dallo storico osservabile fino al giorno/step corrente;
- `TELEMETRY_ONLY`: grandezza ricostruibile esclusivamente a posteriori tramite log, ledger o replay post-match;
- `ENGINE_INTERNAL`: variabile interna mantenuta dall'environment non visibile all'agente;
- `OUTCOME_ONLY`: valore disponibile esclusivamente al termine dell'episodio o post-evento.

---

# 3. Concetti Canonici (Canonical Registry C2)

Il registry canonico C2 consolida **74 concept_id** organizzati in 8 domini tematici (A–H).

---

## A. Terreno e superficie produttiva

### `land_surface_total`
**Tipo:** `STATE / CAPACITY`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Superficie fisica totale posseduta o sbloccata dall'agente (espressa in tile o quadranti), indipendentemente dal suo stato di coltivazione o destinazione d'uso.

### `land_purchase_timing`
**Tipo:** `TIMING`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Momento temporale (giorno/step) in cui viene eseguita una transazione di acquisto e sblocco di un nuovo quadrante di terreno.

### `activated_land_surface`
**Tipo:** `STATE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Porzione della superficie posseduta convertita in un uso produttivo effettivo (tile occupate da colture attive o destinate funzionalmente a pasture per il bestiame).

### `crop_surface_maintained`
**Tipo:** `STATE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Numero di tile coltivate mantenute attivamente in condizioni compatibili con il completamento del ciclo colturale (prive di infestazione bloccante e con stato di irrigazione non decaduto).

### `pasture_surface_maintained`
**Tipo:** `STATE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Superficie dedicata a pascolo recintato/funzionale al mantenimento del bestiame posseduto.

### `maintained_productive_surface`
**Tipo:** `STATE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Somma aggregata della superficie produttiva mantenuta (`crop_surface_maintained` + `pasture_surface_maintained`), accompagnata dal relativo breakdown.

### `monetized_productive_output`
**Tipo:** `REVENUE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Flusso monetario effettivamente incassato dalla vendita di beni prodotti sulla superficie mantenuta.

### `land_activation_payback`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Rendimento o tempo necessario affinché il costo di acquisto/attivazione del terreno sia ammortizzato dal margine netto generato dall'output della superficie acquisita.

### `pasture_arable_surface_tradeoff`
**Tipo:** `INTERACTION / CONSTRAINT`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Vincolo di mutua esclusione spaziale e competitività allocativa tra l'uso del terreno per pascolo e l'uso per colture arabili all'interno dei quadranti posseduti.

---

## B. Workforce, dispatch e logistica

### `workforce_headcount`
**Tipo:** `STATE`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Numero totale di agenti operativi (Farmer + Worker assunti) disponibili all'agente nel giorno corrente.

### `worker_capacity_available`
**Tipo:** `CAPACITY`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Quantità teorica totale di slot azione/tempo disponibili per l'intera workforce nell'orizzonte di una giornata operativa (step per worker moltiplicati per headcount).

### `hire_order_scheduling`
**Tipo:** `TIMING`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Distribuzione temporale e sequenza dei comandi di assunzione (`HIRE`) emessi dall'agente.

### `marginal_hire_payback`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Rendimento marginale netto apportato da un worker addizionale rispetto al suo costo di ingaggio e mantenimento.

### `productive_action_share`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Frazione del tempo operativo totale della workforce spesa in azioni direttamente produttive (`PLANT`, `WATER`, `HARVEST`, `CARE`, `FEED`, `FERTILIZE`, `DIG`) rispetto al tempo totale di esecuzione.

### `movement_overhead`
**Tipo:** `COST / EFFICIENCY`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Frazione di tempo/azioni consumata da comandi di spostamento nello spazio, non coincidente automaticamente con inefficienza quando funzionale al riposizionamento logistico.

### `necessary_transit_fraction`
**Tipo:** `DERIVED_METRIC / EFFICIENCY`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Quota del movimento spaziale strettamente necessaria per raggiungere target di lavoro o punti logistici essenziali (shed, market, tile assegnata).

### `routing_completion_efficiency`
**Tipo:** `EFFICIENCY`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Capacità dell'algoritmo di navigazione/routing di completare task allocati minimizzando i passi di spostamento non produttivi.

### `action_dispatch_failure`
**Tipo:** `CONSTRAINT / FLOW`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `TELEMETRY_ONLY`
Azioni emesse verso l'engine che risultano no-op, non eseguibili per vincoli di stato o ridondanti rispetto all'obiettivo prefissato.

### `worker_action_monetization_rate`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Valore economico monetizzato generato per singola unità di azione worker (espresso sia come tasso lordo su tutte le azioni, sia come tasso netto sulle sole azioni produttive).

### `worker_multi_occupancy`
**Tipo:** `STATE / CAPACITY`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Proprietà fisica dell'ambiente che ammette la compresenza simultanea di molteplici worker sulla medesima coordinata spaziale $(x, y)$ senza collisioni fisiche native né blocchi di movimento imposti dall'engine.

---

## C. Crop production, care, maturity e fertilization

### `crop_care_action_flow`
**Tipo:** `FLOW`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Flusso aggregato delle azioni operative dedicate alla cura e gestione delle piante (semina, irrigazione, fertilizzazione e raccolta).

### `planting_action_flow`
**Tipo:** `FLOW`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Frequenza e volume di esecuzione delle azioni atomiche `PLANT`.

### `watering_execution_rate`
**Tipo:** `FLOW / EFFICIENCY`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Frequenza e volume delle azioni atomiche `WATER` eseguite sulle tile coltivate.

### `watering_continuity`
**Tipo:** `TIMING / FLOW`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Regolarità temporale dell'irrigazione che garantisce l'assenza di finestre di disidratazione critica capaci di arrestare la crescita o innescare il decadimento.

### `crop_harvest_action_flow`
**Tipo:** `FLOW`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Frequenza e volume delle azioni atomiche `HARVEST`.

### `first_yield_day`
**Tipo:** `CONSTRAINT / TIMING`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Parametro canonico dell'ambiente che definisce il numero minimo di giorni di maturazione continuativa che devono intercorrere dal giorno di semina (`day - planted_day >= first_yield_day`) affinché la pianta entri nella finestra di readiness e possa essere raccolta con successo.

### `crop_harvest_readiness`
**Tipo:** `STATE / TIMING`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Condizione necessaria e sufficiente di maturità colturale affinché un'azione `HARVEST` produca prelievo di yield senza distruzione improduttiva della pianta:
$$\text{tile.kind} == \text{PLANT} \quad \land \quad \text{yield\_units} > 0 \quad \land \quad (\text{day} - \text{planted\_day}) \ge \text{first\_yield\_day}$$
Rappresenta formalmente la separazione tra semplice presenza di yield non maturo e maturità fisiologica raccoglibile.

### `crop_fertilizer_bonus`
**Tipo:** `FLOW / EFFICIENCY`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Incremento additivo di yield generato dall'engine su tile con fertilizzazione attiva (`day <= fertilized_until_day`), documentato nel codice dell'ambiente come +2 unità di yield per ciclo di refresh su colture ongoing irrigate o per azione `WATER` nella finestra di resa su colture non-ongoing. Non include alcuna inferenza di marginalità economica, ROI o convenienza di policy.

### `fertilizer_effect_window`
**Tipo:** `TIMING / CONSTRAINT`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Finestra temporale di persistenza dello stato fertilizzato sulla tile impostata dall'engine (`fertilized_until_day = max(fertilized_until_day, day + 2)`), avente durata inclusiva di 3 cicli giornalieri consecutivi: dall'istante di applicazione (`day`) fino al secondo giorno successivo (`day .. day+2`).

### `crop_care_completion_rate`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Rapporto tra il fabbisogno di cure giornaliere richieste dal footprint colturale attivo e le cure effettivamente erogate dalla workforce.

### `crop_decay_risk_window`
**Tipo:** `TIMING / CONSTRAINT`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Finestra temporale strutturata in cui la combinazione di disidratazione prolungata, superamento della lifespan massima della pianta o mancata raccolta espone la coltura a transizione irreversibile verso decadimento, blocco di crescita o generazione di weed.

### `crop_horizon_alignment`
**Tipo:** `TIMING / INTERACTION`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Compatibilità tra i giorni residui prima della fine dell'episodio ($\text{max\_steps} - \text{current\_step}$) e il tempo biologico necessario a una coltura per raggiungere `crop_harvest_readiness` ed essere monetizzata.

### `crop_revenue_mix`
**Tipo:** `REVENUE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Ripartizione analitica del ricavo ottenuto dalle varie specie coltivate nell'episodio.

---

## D. Feed, Wheat e livestock

### `feed_availability`
**Tipo:** `STATE / CONSTRAINT`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Disponibilità quantitativa di mangime (Wheat o altro feed) allocato nello shed o trasportato dai worker, indispensabile per il sostentamento del bestiame.

### `feed_security_buffer`
**Tipo:** `STATE / CAPACITY`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Margine di scorta di feed detenuto rispetto al fabbisogno cumulato atteso per il gregge posseduto fino all'orizzonte di rifornimento pianificato.

### `feed_market_dependency`
**Tipo:** `FLOW / COST`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Frazione dell'alimentazione animale approvvigionata tramite acquisto diretto a mercato rispetto a quella prodotta internamente.

### `feed_market_expenditure`
**Tipo:** `COST`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Spesa monetaria totale sostenuta per l'acquisto di feed sul mercato.

### `wheat_operating_flow`
**Tipo:** `FLOW / INTERACTION`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Flusso operativo multi-funzionale del Wheat: semente, prodotto di raccolta, feed per animali, bene commerciabile a mercato e fonte di liquidità.

### `market_churn_cost`
**Tipo:** `COST / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Perdita economica netta derivante da cicli ravvicinati di compravendita della medesima commodity (spread acquisto/vendita) senza utilità produttiva o detentiva.

### `livestock_headcount`
**Tipo:** `STATE`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Numero totale di capi di bestiame posseduti, articolato per specie animale.

### `livestock_capacity`
**Tipo:** `CAPACITY`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Dimensione massima sostenibile del gregge in relazione alla disponibilità di pasture, risorse idriche, mangime e capacità logistica.

### `pasture_capacity_alignment`
**Tipo:** `INTERACTION`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Condizione strutturale di proporzionalità tra superficie a pasture recintata e numero di animali supportati.

### `livestock_product_flow`
**Tipo:** `FLOW / REVENUE`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Flusso di generazione, raccolta e vendita dei prodotti primari dell'allevamento (Milk e Wool).

### `livestock_care_action_flow`
**Tipo:** `FLOW`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Flusso delle azioni atomiche `CARE` somministrate al bestiame, che impostano `cared_today = true`.

### `pending_care_bonus_accumulation`
**Tipo:** `STATE / FLOW`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Accumulo progressivo a fine giornata (EOD) del contatore `pending_care_bonus` sull'animale, che incrementa se e solo se l'animale risulta sia nutrito sia accudito nello stesso giorno (`cared_today == true` e `fed_today == true`). L'accumulo a EOD è semanticamente distinto dal consumo del bonus, il quale avviene esclusivamente durante i giorni di produzione attiva con animale alimentato (`fed_today == true`).

### `species_margin_differential`
**Tipo:** `EFFICIENCY / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Differenziale di margine operativo netto generato tra specie diverse (es. Mucche vs Pecore) tenendo conto di costo d'acquisto, consumo di mangime e valore di mercato dell'output.

### `fertilizer_byproduct_flow`
**Tipo:** `FLOW / REVENUE`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Flusso di Fertilizer generato automaticamente come sottoprodotto biologico della presenza di bestiame attivo, semanticamente distinto dai prodotti primari commerciali (Milk/Wool).

---

## E. Capitale, mercato, conversione e reinvestimento

### `market_transaction_value`
**Tipo:** `FLOW / DERIVED_METRIC`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Controvalore monetario esatto di una singola operazione di acquisto (`BUY`) o vendita (`SELL`) eseguita a mercato, tracciato con fonte di prezzo esplicita (`observed_fill_price`).

### `operating_cash_buffer`
**Tipo:** `STATE / CAPACITY`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Livello di liquidità monetaria disponibile a decision time mantenuto per far fronte a costi correnti e transazioni impreviste, senza imposizione di soglie fisse nell'ontologia.

### `deployable_capital_window`
**Tipo:** `TIMING / STATE`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Fase o intervallo in cui il capitale liquido eccede gli obblighi a breve termine ed è allocabile in investimenti espansivi (nuovi terreni, worker, bestiame).

### `asset_liquidity_lag`
**Tipo:** `TIMING / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Latenza temporale che intercorre tra l'impiego di capitale in un asset fisico e il ritorno in forma di liquidità monetaria generata da quell'asset.

### `inventory_to_cash_conversion`
**Tipo:** `FLOW / EFFICIENCY`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Processo e tasso di trasformazione di beni materiali stoccati in cassa tramite esecuzione di ordini di vendita a mercato.

### `market_sellthrough_lag`
**Tipo:** `TIMING`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Tempo intercorrente tra il completamento della produzione di un bene vendibile e la sua effettiva liquidazione a mercato.

### `unsold_inventory_value`
**Tipo:** `STATE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Stima del valore economico delle scorte fisiche giacenti nello shed o presso i worker al termine dell'episodio o a uno step arbitrario, con indicazione esplicita del criterio di prezzo adottato.

### `reinvestment_cash_flow`
**Tipo:** `FLOW`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Flusso di cassa monetizzato che viene re-immesso nel sistema operativo per sostenere espansione o acquisto input.

### `product_mix_revenue`
**Tipo:** `REVENUE / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Composizione complessiva dei ricavi disaggregata per macro-categorie (colture, prodotti animali primari, scorte endgame).

### `price_realization_variance`
**Tipo:** `DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Differenza tra il prezzo unitario atteso o nominale di un bene e il prezzo effettivo di esecuzione registrato a mercato.

### `dynamic_market_price_elasticity`
**Tipo:** `CONSTRAINT / INTERACTION`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Meccanismo dell'ambiente per cui i prezzi di vendita e di acquisto dei beni fluttuano dinamicamente in funzione dei volumi scambiati e delle condizioni simulate dal mercato.

---

## F. Endgame e integrità dell'inventory

### `shed_inventory_integrity`
**Tipo:** `STATE / CONSTRAINT`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Persistenza e integrità dell'inventario depositato all'interno dello shed centrale entro il limite strutturale di capienza (`shedCapacity` = 100 unità complessive).

### `shed_overflow_eod_loss`
*(precedentemente indicata come `contract_inventory_loss`)*
**Tipo:** `CONSTRAINT / COST`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_DERIVABLE`
Perdita irreversibile di inventario che si verifica **esclusivamente per overflow** oltre la capienza massima dello storage centrale (`shedCapacity`) durante la procedura automatica di fine giornata (`_end_of_day` $\to$ `_drop_inventories_to_shed`).
*Chiarimento semantico C2:* l'engine trasferisce **automaticamente** allo shed tutti i beni trasportati da qualsiasi worker a fine giornata; non esiste alcuna perdita dovuta alla scadenza del contratto del worker né alcun obbligo di rientro fisico prima di EOD per preservare i beni.

### `endgame_shutdown_timing`
**Tipo:** `TIMING`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Intervallo temporale in prossimità della conclusione dell'episodio in cui cessa l'avvio di nuovi cicli biologici (semina, acquisto animali) a causa dell'impossibilità di ammortamento o raccolta prima della fine della partita.

### `endgame_inventory_liquidation`
**Tipo:** `FLOW / TIMING`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Svendita/liquidazione accelerata e programmata di tutte le scorte residue giacenti nello storage prima del termine dell'episodio per massimizzare il saldo monetario terminale.

---

## G. Condizione del campo, tile lifecycle e recovery

### `field_cleanliness_state`
**Tipo:** `STATE`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Stato quantitativo della presenza, distribuzione e densità di erbe infestanti (`WEED`) sulla superficie arabile posseduta.

### `tile_lifecycle_state`
**Tipo:** `STATE / DERIVED_METRIC`
**Evidence status:** `ENGINE_VERIFIED / DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Stato del ciclo di vita assunto da una specifica tile di terreno all'interno del modello dinamico della simulazione. Comprende le sei categorie/stati lifecycle canonici candidati e semanticamente distinti:
1. `OUT_OF_SCOPE`: tile non posseduta o non appartenente al perimetro operativo attivo;
2. `EMPTY_ASSIGNED`: tile posseduta, libera da ostacoli e disponibile per allocazione/semina;
3. `GROWING`: tile con coltura attiva in fase di accrescimento fisiologico non ancora raccoglibile (`day - planted_day < first_yield_day`);
4. `HARVEST_READY`: tile con coltura matura soddisfacente il predicato di readiness (`crop_harvest_readiness`);
5. `RETIREMENT_DUE`: tile con coltura esaurita, degradata o non più produttiva che richiede rimozione programmata;
6. `LOST_WEED`: tile infestata da erbe infestanti (`WEED`) che bloccano l'uso arabile e richiedono un'azione di scavo.

*Nota di governance C2:* l'ontologia definisce il significato e la distinzione semantica di queste sei categorie candidate; la formalizzazione del classifier totale eseguibile (predicati computazionali mutuamente esclusivi, ordine di precedenza operativa, fallback e boundary tests) è demandata al successivo Feature/validation contract C2.

### `tile_care_due_condition`
**Tipo:** `STATE / CONSTRAINT`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Condizione ortogonale allo stato strutturale del lifecycle colturale che segnala la necessità immediata di un intervento manutentivo (irrigazione per prevenire disidratazione) nel ciclo giornaliero corrente, senza mutare lo stato discreto della tile da `GROWING` o `HARVEST_READY`.

### `preventive_dig_action`
**Tipo:** `FLOW`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Esecuzione pianificata di un'azione `DIG` finalizzata alla rimozione intenzionale di una pianta giunta a fine ciclo colturale (`RETIREMENT_DUE`) per ripristinare la tile allo stato `EMPTY_ASSIGNED` in vista di una nuova semina.

### `recovery_dig_action`
**Tipo:** `FLOW / COST`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Esecuzione correttiva/di emergenza di un'azione `DIG` su una tile caduta nello stato `LOST_WEED`, volta a bonificare l'infestazione e recuperare il terreno all'uso arabile. Non costituisce la strategia primaria per cause di perdita prevenibili.

### `weed_backlog_cost`
**Tipo:** `COST / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Costo opportunità ed energetico (azioni worker e tempo impiegato) necessario per bonificare le infestazioni da weed accumulate sul campo.

---

## H. Vincoli, diagnostica e outcome

### `market_order_batch_limit`
**Tipo:** `CONSTRAINT`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE`
Limite strutturale imposto dall'environment al numero massimo di transazioni di mercato eseguibili all'interno di un singolo step decisionale.

### `action_order_slot_pressure`
**Tipo:** `CONSTRAINT / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `ONLINE_DERIVABLE`
Grado di saturazione della capacità decisionale o degli slot ordine dell'agente rispetto alla domanda simultanea di azioni generate dalla workforce.

### `state_capacity_alignment`
**Tipo:** `INTERACTION / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Metrica composita che valuta l'armonia quantitativa e temporale tra espansione del terreno, dimensione del gregge, consistenza della workforce e risorse idriche/finanziarie disponibili.

### `local_kaggle_fidelity_gap`
**Tipo:** `CONSTRAINT / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Scostamento misurabile tra il comportamento/prestazione osservato nell'ambiente di simulazione locale e l'ambiente di runtime ufficiale Kaggle.

### `operational_divergence_onset`
**Tipo:** `TIMING / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Istante temporale (giorno/step) in cui due configurazioni o modelli decisionali manifestano la prima deviazione significativa e misurabile nei pattern di azione o allocazione delle risorse.

### `economic_lock_in_onset`
**Tipo:** `TIMING / DERIVED_METRIC`
**Evidence status:** `DERIVED`
**Osservabilità:** `TELEMETRY_ONLY`
Momento temporale in cui una divergenza operativa sfocia in un divario economico cumulato o strutturale irreversibile rispetto all'avversario o al benchmark.

### `final_money_outcome`
**Tipo:** `OUTCOME`
**Evidence status:** `ENGINE_VERIFIED`
**Osservabilità:** `ONLINE_OBSERVABLE / OUTCOME_ONLY`
Saldo monetario finale realizzato dall'agente al termine dell'episodio, coincidente con la metrica di valutazione primaria della competizione.

---

# 4. Relazioni canoniche C2

Le relazioni ontologiche descrivono dipendenze funzionali, abilitazioni, vincoli e interazioni tra concetti del dominio:

### Terreno, Workforce e Produttività
- `land_surface_total enables activated_land_surface`
- `activated_land_surface enables maintained_productive_surface`
- `maintained_productive_surface enables monetized_productive_output`
- `workforce_headcount enables worker_capacity_available`
- `worker_capacity_available enables productive_action_share`
- `worker_multi_occupancy enables routing_completion_efficiency`
- `movement_overhead constrains worker_action_monetization_rate`
- `necessary_transit_fraction qualifies movement_overhead`
- `routing_completion_efficiency qualifies movement_overhead`
- `action_dispatch_failure constrains productive_action_share`

### Crop, Maturity, Lifecycle e Care
- `planting_action_flow transitions tile_lifecycle_state (EMPTY_ASSIGNED -> GROWING)`
- `first_yield_day constrains crop_harvest_readiness`
- `crop_harvest_readiness enables crop_harvest_action_flow`
- `crop_harvest_action_flow transitions tile_lifecycle_state (HARVEST_READY -> RETIREMENT_DUE / EMPTY_ASSIGNED)`
- `watering_execution_rate contributes_to crop_care_action_flow`
- `watering_continuity prevents crop_decay_risk_window`
- `fertilizer_effect_window constrains crop_fertilizer_bonus`
- `crop_fertilizer_bonus qualifies monetized_productive_output`
- `tile_care_due_condition qualifies crop_care_action_flow`
- `preventive_dig_action transitions tile_lifecycle_state (RETIREMENT_DUE -> EMPTY_ASSIGNED)`
- `recovery_dig_action transitions tile_lifecycle_state (LOST_WEED -> EMPTY_ASSIGNED)`
- `crop_decay_risk_window transitions tile_lifecycle_state (GROWING / HARVEST_READY -> LOST_WEED / RETIREMENT_DUE)`

### Livestock, Feed e Byproducts
- `livestock_headcount enables livestock_capacity`
- `pasture_capacity_alignment enables livestock_capacity`
- `feed_availability enables livestock_product_flow`
- `livestock_care_action_flow AND feed_availability produces pending_care_bonus_accumulation`
- `pending_care_bonus_accumulation qualifies livestock_product_flow`
- `livestock_headcount enables fertilizer_byproduct_flow`
- `feed_market_dependency interacts_with operating_cash_buffer`

### Capitale, Mercato e Storage
- `market_transaction_value measures feed_market_expenditure`
- `market_transaction_value measures product_mix_revenue`
- `inventory_to_cash_conversion produces reinvestment_cash_flow`
- `operating_cash_buffer constrains deployable_capital_window`
- `deployable_capital_window enables land_purchase_timing`
- `asset_liquidity_lag constrains reinvestment_cash_flow`
- `market_sellthrough_lag constrains reinvestment_cash_flow`
- `shed_inventory_integrity constrains shed_overflow_eod_loss`
- `shed_overflow_eod_loss constrains unsold_inventory_value`
- `endgame_shutdown_timing interacts_with endgame_inventory_liquidation`
- `market_order_batch_limit constrains hire_order_scheduling`
- `market_order_batch_limit interacts_with action_order_slot_pressure`
- `local_kaggle_fidelity_gap qualifies local_performance_claims`

---

## 4.1 Relazioni deliberatamente escluse o falsificate

La riconciliazione R1 e le verifiche sull'engine hanno formalmente escluso e falsificato le seguenti relazioni:

1. **`contract expiration causes inventory destruction` [FALSIFICATA]:** l'engine deposita automaticamente l'inventario dei worker nello shed a fine giornata;
2. **`yield_units > 0 implies crop_harvest_readiness` [FALSIFICATA]:** prima di `first_yield_day`, raccogliere non produce esito utile e distrugge la semina;
3. **`worker coordinate overlap triggers collision / movement stall` [FALSIFICATA]:** l'engine consente sovrapposizione spaziale illimitata tra worker;
4. **`care_due is a discrete structural state of tile_lifecycle` [RESPINTA]:** il bisogno di cura/irrigazione è una condizione di allerta ortogonale allo stato strutturale;
5. **`market_order_batch_limit constrains worker_capacity_available` [RESPINTA]:** il vincolo di slot riguarda gli ordini di acquisto/vendita/assunzione emessi dall'agente, non la capacità lavorativa dei worker già in campo.

---

# 5. Separazioni canoniche non negoziabili C2

L'ontologia C2 adotta formalmente le seguenti 12 distinzioni semantiche non negoziabili:

1. **Terreno posseduto $\neq$ Terreno attivato $\neq$ Terreno mantenuto:** la proprietà fondiaria non implica produzione attiva né manutenzione sostenibile.
2. **Worker headcount $\neq$ Throughput operativo $\neq$ Azioni monetizzate:** avere più worker non aumenta il valore generato se il movimento o il disallineamento operativo saturano la capacità.
3. **`yield available` $\neq$ `harvest ready`:** la presenza di yield grezzo nel dictionary dell'engine non abilita l'azione `HARVEST` prima del compimento di `first_yield_day`.
4. **Scadenza contrattuale $\neq$ Perdita di inventario:** il reset del contratto non distrugge i beni portati dal worker; la perdita si verifica unicamente come overflow oltre la capienza dello shed (100 unità).
5. **Crop care $\neq$ Solo irrigazione:** la cura colturale comprende semina, sequenza idrica, fertilizzazione, protezione da decay e tempestività di raccolta.
6. **`tile_lifecycle_state` $\neq$ `tile_care_due_condition`:** lo stato strutturale della tile (es. `GROWING`, `HARVEST_READY`) è ortogonale alla condizione istantanea di allerta idrica.
7. **Preventive DIG $\neq$ Recovery DIG:** la clearance programmata di una pianta a fine ciclo (`RETIREMENT_DUE`) è fisiologica; lo scavo di emergenza su `LOST_WEED` è un costo di recupero di una perdita.
8. **Worker spatial overlap $\neq$ Collisione:** la compresenza sulla stessa coordinata è permessa dall'engine; la separazione spaziale è un'euristica di dispatching della policy, non un vincolo fisico.
9. **Fertilizer applicato $\neq$ Boost permanente:** l'effetto fertilizzante ha una finestra finita e determinata dall'engine (`day .. day+2`).
10. **CARE somministrata $\neq$ Margine livestock immediato:** l'azione `CARE` accumula un bonus che viene consumato solo durante i giorni di produzione attiva con animale alimentato (`FEED`).
11. **Feed security $\neq$ Autarchia alimentare:** la sicurezza delle scorte può essere garantita indifferentemente da autoproduzione di Wheat o da canali di acquisto a mercato.
12. **Divergenza operativa $\neq$ Lock-in economico:** differenze nel timing di una transazione o nello schema di semina non costituiscono di per sé un divario competitivo incolmabile.

---

# 6. Concetti model-local esclusi dall'ontologia

Restano categoricamente esclusi dall'ontologia canonica:
- target rigidi di capi di bestiame (es. 4, 7, 10, 13 animali);
- giorni fissi di acquisto terreno (es. Q1 al giorno 5, Q2 al giorno 8);
- soglie numeriche di cassa o percentuali arbitrarie di buffer;
- regole di dispatch priority o routing algoritmico;
- nomi di classi di strategia (`AntigravityROIAgent`, `CopilotAgent`, `ProductiveMassROIAgent`);
- percorsi di script di submission o configurazioni di packaging;
- classificazioni di ranking, impatto e confidence proprietarie del singolo modellatore.

---

# 7. Tracciabilità dei termini storici e mapping C1 $\to$ C2

| Termine storico C1 | Stato C2 | Trattamento in C2 |
|---|---|---|
| `contract_inventory_loss` | **CORRETTO** | Rinominato/ridefinito come `shed_overflow_eod_loss`. Falsificato il meccanismo di perdita da mancato rientro manuale. |
| `harvest_readiness` | **AGGIUNTO** | Formalizzato come `crop_harvest_readiness` vincolato da `first_yield_day`. |
| `tile_lifecycle` | **AGGIUNTO** | Formalizzato come `tile_lifecycle_state` con 6 stati esaustivi. |
| `care_due` | **AGGIUNTO** | Formalizzato come `tile_care_due_condition` ortogonale al lifecycle. |
| `worker_multi_occupancy` | **AGGIUNTO** | Promosso a `ENGINE_VERIFIED`. |
| `fertilizer_window` | **AGGIUNTO** | Formalizzato come `fertilizer_effect_window` (`day..day+2`) e `crop_fertilizer_bonus`. |
| `care_bonus_accumulation` | **AGGIUNTO** | Formalizzato come `pending_care_bonus_accumulation`. |
| `preventive_vs_recovery_dig` | **AGGIUNTO** | Formalizzati come `preventive_dig_action` e `recovery_dig_action`. |
| `action_retry_penalty` | **MERGED** | Mantenuto assorbito in `action_dispatch_failure`. |
| `tile_utility_decay` | **NOT_CANONICAL** | Coperto da `crop_decay_risk_window` e `field_cleanliness_state`. |
| `capital_lock_in_risk` | **MERGED** | Assorbito in `asset_liquidity_lag` e `operating_cash_buffer`. |
| `spatial_shed_congestion_penalty`| **NOT_CANONICAL** | Falsificato dall'assenza di collisioni native (`worker_multi_occupancy`). |

---

# 8. Contratto di osservabilità e telemetry per C2 / E16

Ogni analisi, log o telemetry prodotta da framework diagnostici o simulatori deve qualificare le grandezze registrate secondo la tabella di osservabilità:

1. **Stato Online:** grandezze fornite dall'engine al momento del comando (`step`, `money`, `farmer_pos`, `inventory`, `tiles`, `market_prices`, `day`).
2. **Stato Derivato Online:** grandezze computabili deterministicamente dal contesto corrente (`crop_harvest_readiness`, `tile_lifecycle_state`, `tile_care_due_condition`, `fertilizer_effect_window`, `operating_cash_buffer`).
3. **Telemetria Post-Azione:** log degli eventi generati dall'engine a seguito dell'azione (`applied_actions`, `fill_price`, `shed_overflow_eod_loss`, `action_dispatch_failure`).
4. **Outcome ed Economia Finale:** metriche terminali aggregate (`final_money_outcome`, `product_mix_revenue`, `marginal_hire_payback`, `operational_divergence_onset`).

Nessun dato appartenente alla classe *Telemetria Post-Azione* o *Outcome* può essere consumato come input online da una policy decisionale.

---

# 9. Impatto downstream per Foundation C2

La pubblicazione del candidato `ONTOLOGY_C2.md` impone i seguenti requisiti di allineamento sui restanti livelli della Model Foundation:

### STATE_MACHINE_C2
- Adottare `shed_overflow_eod_loss` come unica causa di perdita EOD (rimuovendo qualsiasi transizione legata a perdita per scadenza contratto);
- Integrare `first_yield_day` nella transizione verso `HARVEST_READY`;
- Formalizzare la separazione tra gli stati strutturali del ciclo di vita (`GROWING`, `HARVEST_READY`, `RETIREMENT_DUE`, `LOST_WEED`) e l'allerta idrica `tile_care_due_condition`;
- Documentare le transizioni per `preventive_dig_action` e `recovery_dig_action`;
- Definire l'authoritative transition clock e i boundary examples per ciascuno stato.

### FEATURE_MODEL_C2
- Pubblicare il classifier totale eseguibile per `tile_lifecycle_state` (predicati logici mutualmente esclusivi, ordine di precedenza formale e fallback);
- Implementare il predicato computabile per `crop_harvest_readiness` basato su `planted_day` e `first_yield_day`;
- Rimuovere dal catalogo le feature predittive deterministiche sul countdown del random WEED spawn;
- Integrare la durata `day..day+2` per le feature collegate a FERTILIZE;
- Documentare i contratti di aggregazione e separare esplicitamente need, eligibility e serviceability;
- Mantenere la classificazione `NONE_DIRECT` dove applicabile.

### MODEL_SPEC_C2
- Esternalizzare la colonna `current_MODEL_SPEC_usage` in matrici di consumo versionate e indipendenti per ciascun agente (Antigravity, Codex, Copilot);
- Rimuovere prescrizioni operative errate sul rientro forzato dei worker prima di EOD;
- Dichiarare l'uso effettivo del predicato di readiness per evitare comandi HARVEST prematuri;
- Rettificare ogni dichiarazione di consumo `USED / FULL` che non corrisponda a codice effettivamente eseguito nel runtime;
- Distinguere parametri controllabili, soglie di calibrazione e requisiti diagnostici.

### CONSUMER MATRIX / RUNTIME TRACE
- Collegare ciascun MODEL_SPEC al commit SHA e all'hash del wrapper di esecuzione;
- Verificare la conformità statica ed empirica tra le feature dichiarate consumate e le variabili lette dalla policy.

---

**Fine del candidato ONTOLOGY C2.**
