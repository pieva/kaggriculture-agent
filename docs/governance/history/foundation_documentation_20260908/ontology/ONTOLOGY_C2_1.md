# ONTOLOGY C2.1 — Ontologia comune riconciliata post-3Q

- **Fase:** Model Foundation C2.1 / Post-3Q Review Pass
- **Stato:** RECONCILED / FOUNDATION POST-3Q COMPLETE
- **Data:** 2026-09-01
- **Ambito:** Vocabolario semantico comune e neutrale per Antigravity, Codex e Copilot
- **Fonte normativa:** `results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md` (FROZEN)
- **Baseline di audit:** `results/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md` (FROZEN)
- **Reconciliation Authority:** `results/model_spec_c2/foundation_revision/FOUNDATION_CROSS_REVIEW_RECONCILIATION.md` (CONSOLIDATED)
- **Runtime di riferimento:** `kaggle-environments` 1.32.7 (`kaggriculture` 0.1.0) — Fingerprint: `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d`
- **Baseline congelata:** `docs/model/ontology/ONTOLOGY_C2.md`
- **Review candidate preservata:** `docs/model/ontology/ONTOLOGY_C2_1_POST_3Q_REVIEW_CANDIDATE.md`
- **Destinazione riconciliata:** `docs/model/ontology/ONTOLOGY_C2_1.md`

---

## 1. Scopo e governance

Questa ontologia definisce il vocabolario concettuale comune, period-aware e rigorosamente neutrale rispetto alle policy decisionali per descrivere i fenomeni del dominio simulato di **Kaggriculture**. È la revisione C2.1 riconciliata dopo i feedback indipendenti post-3Q; la baseline C2 resta preservata come riferimento storico congelato.

L'ontologia risponde alla domanda fondamentale:
> **Che cosa esiste nel dominio Kaggriculture, quali proprietà possiede e che cosa significa?**

### 1.1 Separazione di principio: Fatti di Dominio vs Policy
L'ontologia descrive **l'ambiente di simulazione**, non le preferenze o le strategie di un agente. Ogni concetto appartiene a una delle seguenti quattro classi di rigore epistemico:

1. `ENGINE_FACT`: fatto normativo primitivo o legge causale definita direttamente dal codice dell'ambiente (`kaggriculture.py`);
2. `DERIVED_ENGINE_FACT`: grandezza o predicato logicamente ed esattamente derivabile da fatti primitivi senza assunzioni di strategia;
3. `POLICY_CONTEXT`: concetto deliberativo, pianificato o stimato appartenente allo spazio decisionale dell'agente (es. target, riserve, prenotazioni, working set);
4. `POST_HOC_METRIC`: grandezza o evidenza diagnostica ricostruibile esclusivamente a posteriori (telemetria post-azione, outcome, label di validazione post-match).

L'ontologia **NON definisce né prescrive**:
- convenienza economica relativa di colture o specie animali (es. "Melon è ottimale", "Livestock è in perdita");
- decisioni di mix colturale o livestock ON/OFF;
- numero ottimale di worker o calendari di assunzione;
- regole di dispatching, precedenze o algoritmi di routing;
- percorsi o tempistiche di espansione territoriale;
- target economici di fatturato o soglie monetarie;
- architetture di implementazione, codice o submission.

### 1.2 Principio OR e criteri di ammissione
L'ontologia è l'**unione semantica (OR)** dei fenomeni rilevanti del dominio identificati e verificati nel codice dell'ambiente, non l'intersezione minimale delle scelte dei singoli modellatori.

Un concetto appartiene al registry canonico se soddisfa quattro criteri:
1. **Neutralità semantica:** descrive proprietà del sistema o classi informative, non prescrizioni di policy o scelte di convenienza locale;
2. **Distinguibilità fenomenologica:** identifica un meccanismo o una grandezza non riducibile ad altri concetti esistenti;
3. **Assenza di policy leakage:** non codifica euristiche proprietarie o assunzioni di strategia come leggi dell'ambiente;
4. **Engine grounding verificato:** dispone di una definizione fondata sulle regole dell'ambiente congelato (`ENGINE_VERIFIED`), formalmente derivata (`DERIVED`), esplicitamente dichiarata come contesto di policy (`POLICY_DECLARED`) o metrica post-hoc (`POST_HOC_METRIC`).

### 1.3 Mapping dei modelli e liceità di `NONE_DIRECT`
Ciascun `MODEL_SPEC` e ciascun layer downstream mappa i concetti canonici secondo la propria architettura decisionale:
- **Usage:** `USED`, `PARTIAL`, `NOT_USED`
- **Mapping semantico:** `FULL`, `PARTIAL`, `ABSENT`, `BROADER`, `NARROWER`, `CONFLICT`

**Liceità di `NONE_DIRECT`:** non esiste e non deve essere forzata una biiezione 1:1 tra Ontologia e Feature Model. Grandezze di conteggio runtime, derivazioni tecniche di clock o variabili puramente computazionali possono legittimamente avere mapping `NONE_DIRECT` verso l'ontologia se non costituiscono un concetto semantico generale riusabile.

---

## 2. Tassonomia ed Evidence Classification

### 2.1 Tipi ontologici primari
I tipi canonici assegnati ai concetti sono:
- `STATE`: proprietà discreta o continua dello stato del sistema o degli attori;
- `FLOW`: tasso di transizione, volume di azioni o movimento di entità/risorse nel tempo;
- `CAPACITY`: vincolo dimensionale, limite massimo o disponibilità multi-dimensionale di una risorsa o di un sottosistema;
- `COST`: spesa monetaria, consumo di risorse o overhead non reversibile;
- `REVENUE`: generazione monetaria da transazioni di mercato o liquidazione;
- `EFFICIENCY`: rapporto di rendimento tra output ottenuto e input/risorse impiegate;
- `CONSTRAINT`: regola o vincolo strutturale imposto dall'environment o dalla geometria della simulazione;
- `TIMING`: momento di accadimento, intervallo o coordinamento temporale di un evento/azione;
- `INTERACTION`: accoppiamento o trade-off strutturato tra due o più sottosistemi;
- `DERIVED_METRIC`: grandezza computata da stati, flussi o eventi elementari;
- `OUTCOME`: risultato terminale o metrica di sintesi aggregata dell'episodio.

### 2.2 Assi di classificazione epistemica

#### Asse dell'Evidenza (`evidence_status`):
- `ENGINE_VERIFIED`: comportamento o formula verificata direttamente nel codice sorgente dell'ambiente simulato (`kaggriculture.py`);
- `EMPIRICALLY_VERIFIED`: fenomeno osservato e replicato sperimentalmente su seed/match controllati;
- `DERIVED`: costrutto concettuale rigorosamente derivato da definizioni primitive senza gradi di libertà non specificati;
- `POLICY_DECLARED`: costrutto, soglia o prenotazione definita all'interno della sfera deliberativa del controller;
- `PARTIALLY_KNOWN`: fenomeno la cui dinamica qualitativa è accertata ma i cui parametri presentano margini di calibrazione.

#### Asse dell'Osservabilità (`observability`):
- `ONLINE_OBSERVABLE`: campo direttamente esposto dallo state dictionary dell'engine al momento decisionale;
- `ONLINE_DERIVABLE`: grandezza computabile in tempo reale dallo storico osservabile fino al giorno/step corrente;
- `TELEMETRY_ONLY`: grandezza ricostruibile esclusivamente a posteriori tramite log, ledger o replay post-match;
- `ENGINE_INTERNAL`: variabile interna mantenuta dall'environment non visibile all'agente;
- `OUTCOME_ONLY`: valore disponibile esclusivamente al termine dell'episodio o post-evento.

### 2.3 Quadripartizione Epistemica del Processo Decisionale (CORR-13)
L'ontologia formalizza quattro fasi temporali ed epistemicamente distinte del processo operativo:
1. `ACTION_REQUEST` ($A_t$): intenzione o comando formulato dall'agente sulla base dello stato $S_t$;
2. `SNAPSHOT_ELIGIBILITY`: legalità e ammissibilità teorica dell'azione valutata staticamente sullo snapshot $S_t$ prima dell'esecuzione;
3. `EXECUTION_OUTCOME`: risultato effettivo dell'elaborazione engine (`SUCCESS`, `NO_OP`, `REJECTED`);
4. `POST_STATE_EVIDENCE` ($S_{t+1}$): evidenza empirica osservata nello stato risultante post-transizione.

Nessun dato appartenente a `EXECUTION_OUTCOME` o `POST_STATE_EVIDENCE` è disponibile all'agente prima della transizione dell'engine.

---

## 3. Concetti Canonici (Canonical Registry C2)

Il registry canonico C2 consolida **85 concept_id** organizzati in 9 domini tematici (A–I).

---

## A. Terreno e superficie produttiva

### `land_surface_total`
- **Tipo:** `STATE / CAPACITY`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Superficie fisica totale posseduta o sbloccata dall'agente (espressa in tile o quadranti), pari a $(\text{boardSize} // 2)^2$ tile per quadrante (25 tile per quadrante nel default $10 \times 10$).

### `land_purchase_timing`
- **Tipo:** `TIMING`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Momento temporale (giorno/step) in cui viene eseguita una transazione di acquisto e sblocco di un nuovo quadrante di terreno (`BUY_LAND`).

### `activated_land_surface`
- **Tipo:** `STATE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Porzione della superficie posseduta convertita in un uso produttivo effettivo (tile occupate da colture attive o strutture/pascoli per il bestiame).

### `crop_surface_maintained`
- **Tipo:** `STATE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Numero di tile coltivate mantenute attivamente in condizioni compatibili con il completamento del ciclo colturale (prive di infestazione da weed e irrigate entro i limiti di disidratazione).

### `pasture_surface_maintained`
- **Tipo:** `STATE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Superficie dedicata a strutture per bestiame (`PASTURE` o `COOP`) attivamente occupate o mantenute funzionali.

### `maintained_productive_surface`
- **Tipo:** `STATE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Somma aggregata della superficie produttiva mantenuta (`crop_surface_maintained` + `pasture_surface_maintained`), accompagnata dal relativo breakdown.

### `monetized_productive_output`
- **Tipo:** `REVENUE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Flusso monetario effettivamente incassato dalla vendita a mercato di beni prodotti sulla superficie mantenuta.

### `land_activation_payback`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Rendimento o tempo necessario affinché il costo di acquisto/attivazione del terreno sia ammortizzato dal margine netto generato dall'output della superficie acquisita.

### `pasture_arable_surface_tradeoff`
- **Tipo:** `INTERACTION / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Vincolo di mutua esclusione spaziale tra l'uso del terreno per pascoli/strutture animali e l'uso per colture arabili all'interno delle coordinate possedute.

---

## B. Workforce, dispatch e logistica

### `workforce_headcount`
- **Tipo:** `STATE`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Numero totale di unità operative (Farmer permanente + Farm Hands con contratto giornaliero) disponibili al giocatore nello step corrente.

### `worker_capacity_available`
- **Tipo:** `CAPACITY`
- **Evidence status:** `DERIVED_ENGINE_FACT`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Limite superiore teorico del budget di slot azione per step o per orizzonte giornaliero ($\text{workforce\_headcount} \times \text{turnsPerDay}$). **Non esiste un limite di capienza fisica di trasporto nell'inventario del worker** (`kaggriculture.py:299-309`).

### `hire_order_scheduling`
- **Tipo:** `TIMING`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Distribuzione temporale e sequenza dei comandi di assunzione (`HIRE`) emessi dall'agente nella fase di mercato. Gli Hands assunti diventano operativi nello step successivo e vengono rimossi a EOD.

### `marginal_hire_payback`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Rendimento marginale netto apportato da un worker addizionale rispetto al suo costo progressivo di ingaggio (governato dalla formula Fibonacci intra-day).

### `productive_action_share`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Frazione del tempo operativo della workforce spesa in azioni di mutazione diretta rispetto al totale dei passi (incluso movimento e wait).

### `movement_overhead`
- **Tipo:** `COST / EFFICIENCY`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Quota di comandi/step consumata da azioni di spostamento (`MOVE`), necessaria per il transito logistico ma priva di effetto di produzione diretta.

### `necessary_transit_fraction`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Quota del movimento spaziale valutata a posteriori rispetto a una distanza geometrica di riferimento tra la posizione operativa di partenza e la destinazione assegnata (`POST_HOC_METRIC`).

### `routing_completion_efficiency`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Metrica diagnostica a posteriori che confronta i passi di spostamento effettivamente eseguiti rispetto alla distanza di base tra coordinate operative (`POST_HOC_METRIC`).

### `action_dispatch_failure`
- **Tipo:** `CONSTRAINT / FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Azioni emesse verso l'engine che risultano silent no-op per violazione di guardie di legalità o stato non conforme (es. harvest precoce, semina senza semi, feed senza grano).

### `worker_action_monetization_rate`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Valore economico netto monetizzato generato per singola unità di azione o slot worker impiegato.

### `worker_multi_occupancy`
- **Tipo:** `STATE / CAPACITY`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Proprietà fisica dell'ambiente che ammette la compresenza simultanea di molteplici worker sulla medesima coordinata spaziale $(x, y)$ senza collisioni fisiche né blocchi di movimento imposti dall'engine.

---

## C. Crop production, care, maturity e fertilization

### `crop_care_action_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Flusso aggregato delle azioni operative dedicate alla gestione delle piante (semina, irrigazione, fertilizzazione e raccolta).

### `planting_action_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Volume ed esecuzione delle azioni atomiche `PLANT`. Richiede che il worker si trovi su una tile sbloccata con valore `None` e possieda almeno un seme della specie richiesta. Se la domanda aggregata per specie nello step supera i semi posseduti, tutte le semine di quella specie nello step falliscono atomicamente (`kaggriculture.py:417-429`).

### `watering_execution_rate`
- **Tipo:** `FLOW / EFFICIENCY`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Frequenza e volume delle azioni atomiche `WATER`. La prima WATER riuscita nel giorno imposta `watered_today = True`. Ulteriori irrigazioni sulla stessa pianta nello stesso giorno sono silent no-op.

### `watering_continuity`
- **Tipo:** `TIMING / FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Regolarità temporale dell'irrigazione necessaria per prevenire che `consecutive_unwatered` raggiunga 2 all'EOD, innescando la trasformazione della pianta in `WEED`.

### `crop_harvest_action_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Frequenza e volume delle azioni atomiche `HARVEST` su colture. Trasferisce l'intera resa nel worker inventory; per colture non-ongoing la tile torna `None`, per colture ongoing la resa torna a 0.

### `first_yield_day`
- **Tipo:** `CONSTRAINT / TIMING`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Età minima ($\text{day} - \text{planted\_day} \ge \text{first\_yield\_day}$) affinché `HARVEST` sia legale. Valori: WHEAT (2), CARROT (2), TOMATO (8), STRAWBERRY (10), MELON (10).

### `crop_harvest_readiness`
- **Tipo:** `STATE / TIMING`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Condizione necessaria e sufficiente per il successo di `HARVEST` su tile `PLANT`:
  $$\text{tile.kind} == \text{PLANT} \quad \land \quad \text{yield\_units} > 0 \quad \land \quad (\text{day} - \text{planted\_day}) \ge \text{first\_yield\_day}$$
  Tentativi di raccolta su colture immature sono silent no-op.

### `crop_fertilizer_bonus`
- **Tipo:** `FLOW / EFFICIENCY`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Incremento di resa generato dall'engine su colture ongoing a EOD: produce una resa incrementale totale di 2 (uplift netto canonico di **$+1$** rispetto alla resa base di 1) **se e solo se** la pianta è stata irrigata nel giorno corrente (`was_watered == True`) ed è fertilizzata (`fertilized_until_day >= current_day`) (`kaggriculture.py:799`).

### `fertilizer_effect_window`
- **Tipo:** `TIMING / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Finestra temporale di persistenza impostata dall'azione `FERTILIZE`: $\text{fertilized\_until\_day} = \max(\text{precedente}, \text{current\_day} + 2)$, avente durata inclusiva di 3 giorni di calendario ($\text{current\_day} \dots \text{current\_day} + 2$).

### `crop_care_completion_rate`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Rapporto a posteriori tra il fabbisogno di cure giornaliere richieste dal campo e le cure effettivamente erogate con successo.

### `crop_decay_risk_window`
- **Tipo:** `TIMING / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Finestra in cui una pianta rischia decadimento deterministico o morte (disidratazione al 2° EOD consecutivo, o lifespan decay ogni 2 step da `max_lifespan_step`).

### `crop_horizon_alignment`
- **Tipo:** `TIMING / INTERACTION`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Compatibilità tra i giorni residui dell'episodio e il ciclo biologico necessario affinché una specie maturi e possa essere raccolta/monetizzata.

### `crop_revenue_mix`
- **Tipo:** `REVENUE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Ripartizione analitica del ricavo ottenuto dalle varie specie vegetali nell'episodio.

---

## D. Feed, Wheat e livestock

### `feed_availability`
- **Tipo:** `STATE / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Disponibilità fisica di `WHEAT` nello shed o nell'inventario del worker per eseguire l'azione atomica `FEED`.

### `feed_security_buffer`
- **Tipo:** `STATE / CAPACITY`
- **Evidence status:** `POLICY_DECLARED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Margine di scorta di mangime pianificato dalla policy per garantire continuità alimentare al gregge (`POLICY_CONTEXT`).

### `feed_market_dependency`
- **Tipo:** `FLOW / COST`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Quota del mangime animale approvvigionata tramite acquisto a mercato rispetto a quella autoprodotta sul campo.

### `feed_market_expenditure`
- **Tipo:** `COST`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Esborso monetario totale sostenuto per l'acquisto di `WHEAT` sul mercato.

### `wheat_operating_flow`
- **Tipo:** `FLOW / INTERACTION`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Flusso multi-funzionale del Wheat: semente per semina, prodotto di raccolta, mangime per animali (`FEED`), bene vendibile a mercato.

### `market_churn_cost`
- **Tipo:** `COST / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Perdita economica netta dovuta a spread compravendita in transazioni ravvicinate senza utilità produttiva.

### `livestock_headcount`
- **Tipo:** `STATE`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Numero totale di animali posseduti, articolato per specie supportate (`GOOSE`, `COW`, `SHEEP`).

### `livestock_structural_capacity`
- **Tipo:** `CAPACITY`
- **Evidence status:** `DERIVED_ENGINE_FACT`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Capienza fisica massima determinata dal conteggio delle strutture dedicate disponibili (`COOP` per GOOSE, `PASTURE` per COW/SHEEP), derivabile direttamente dallo stato dell'ambiente.

### `livestock_output_storage_capacity`
- **Tipo:** `CAPACITY / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Limite massimo di resa accumulabile sulla tile della struttura animale (`ANIMALS[species]["max_held"]`: GOOSE 4, COW 6, SHEEP 6). Non si applica all'inventario del lavoratore (`kaggriculture.py:827`).

### `structure_construction_cost`
- **Tipo:** `COST / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Costo diretto dell'edificazione di strutture (`BUILD_COOP`, `BUILD_PASTURE`), pari a **0 cassa** nell'engine (`kaggriculture.py:493-503`). L'overhead è esclusivamente in slot temporali lavoratore.

### `pasture_capacity_alignment`
- **Tipo:** `INTERACTION`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Vincolo strutturale di allineamento: ciascun animale richiede una struttura dedicata e vuota del tipo corrispondente (`GOOSE -> COOP`, `COW/SHEEP -> PASTURE`).

### `livestock_product_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Flusso di generazione biologica e prelievo tramite `HARVEST` dei prodotti animali primari (`EGG`, `MILK`, `WOOL`) nell'inventario del lavoratore.

### `livestock_base_production`
- **Tipo:** `FLOW / STATE`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Erogazione di base dell'output animale ($\text{base\_output} = 1$) nel giorno biologico programmato a patto che l'animale non sia fuggito (`consecutive_unfed < 2`). **L'azione `FEED` non è il gate abilitante del base output.**

### `livestock_feed_action_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Flusso delle azioni atomiche `FEED` somministrate agli animali consumando 1 unità di Wheat dal worker inventory e impostando `fed_today = True`.

### `livestock_care_action_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Flusso delle azioni atomiche `CARE` somministrate agli animali, che impostano `cared_today = True`.

### `pending_care_bonus_accumulation`
- **Tipo:** `STATE / FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Incremento additivo a EOD di `pending_care_bonus` se `cared_today == True` $\land$ `fed_today == True`. **Ad ogni giorno di produzione programmata, `pending_care_bonus` viene resettato a 0** (convertito in prodotto se `fed_today == True`, perso se unfed) (`kaggriculture.py:823-828`).

### `animal_escape_condition`
- **Tipo:** `CONSTRAINT / STATE`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Se all'EOD `consecutive_unfed` raggiunge 2 (secondo giorno consecutivo senza `FEED`), l'animale fugge prima della produzione e la casella regredisce alla struttura vuota corrispondente.

### `fertilizer_available_state`
- **Tipo:** `STATE`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Flag booleano `fertilizer_available` impostato a `True` a ogni EOD in cui l'animale sopravvive. È non-cumulativo (mantiene `True` fino alla raccolta tramite `COLLECT_FERTILIZER`).

### `fertilizer_byproduct_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Flusso di `FERTILIZER` prelevato dagli animali tramite l'azione atomica `COLLECT_FERTILIZER` nell'inventario del lavoratore.

### `species_margin_differential`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Differenziale di margine operativo a posteriori tra specie animali diverse.

---

## E. Capitale, mercato, conversione e reinvestimento

### `current_money_state`
- **Tipo:** `STATE`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Saldo monetario liquido disponibile al giocatore nello step decisionale corrente (`observation.farms[player].money`, esposto anche dalla vista agente equivalente). Non va confuso con il saldo terminale o con una stima controfattuale.

### `market_transaction_value`
- **Tipo:** `FLOW / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Controvalore monetario effettivamente regolato per una transazione di acquisto (`BUY`) o vendita (`SELL`). Prima della risoluzione congiunta non è una feature online certa: quantità eseguita e prezzo realizzato dipendono dagli ordini simultanei, dalla disponibilità e dalla priorità di commit. È ricostruibile solo dal risultato della transizione o da delta post-stato.

### `shared_market_contention_externality`
- **Tipo:** `INTERACTION / POST_HOC_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Differenza post-transizione tra l'esito osservato e una baseline pre-stato dichiarata. Il lockstep, la quotazione comune per unità e l'ordine di commit sono engine-verificati; l'attribuzione numerica alla contesa è una derivazione di telemetria, non un campo nativo né un controfattuale identificato dall'engine. L'ordine dell'avversario non è osservabile prima della risoluzione del medesimo slot.

### `operating_cash_buffer`
- **Tipo:** `STATE / CAPACITY`
- **Evidence status:** `POLICY_DECLARED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Livello di liquidità monetaria trattenuto deliberatamente dalla policy per finanziare ordini futuri, come acquisti di sementi, foraggio o ingaggi `HIRE` dei turni successivi (`POLICY_CONTEXT`). L'engine non addebita alcun costo o salario di mantenimento a EOD.

### `deployable_capital_window`
- **Tipo:** `TIMING / STATE`
- **Evidence status:** `POLICY_DECLARED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Finestra in cui il capitale liquido eccede le riserve operative ed è allocabile in investimenti espansivi (`POLICY_CONTEXT`).

### `asset_liquidity_lag`
- **Tipo:** `TIMING / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Intervallo temporale tra l'esborso monetario per un asset e il primo flusso monetario netto derivante dal suo output.

### `inventory_to_cash_conversion`
- **Tipo:** `FLOW / EFFICIENCY`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Processo e velocità di trasformazione dei beni stoccati nello shed in liquidità tramite ordini `SELL`.

### `market_sellthrough_lag`
- **Tipo:** `TIMING`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Tempo intercorrente tra la produzione/raccolta di un bene e la sua liquidazione effettiva sul mercato.

### `unsold_inventory_value`
- **Tipo:** `STATE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Valore economico stimato delle scorte fisiche giacenti nello storage al termine dell'episodio.

### `reinvestment_cash_flow`
- **Tipo:** `FLOW`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Flusso monetario incassato e riallocato per sostenere espansione fondiaria o acquisto di input produttivi.

### `product_mix_revenue`
- **Tipo:** `REVENUE / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Composizione aggregata dei ricavi disaggregata per macro-categorie.

### `price_realization_variance`
- **Tipo:** `DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Scostamento tra prezzo atteso/nominale e prezzo effettivo di regolazione registrato a mercato.

### `dynamic_market_price_elasticity`
- **Tipo:** `CONSTRAINT / INTERACTION`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Meccanismo dell'ambiente per cui i prezzi di vendita e acquisto dei beni variano dinamicamente in funzione dei volumi scambiati nel turno e dei consumi cittadini.

---

## F. Endgame e integrità dell'inventory

### `shed_inventory_integrity`
- **Tipo:** `STATE / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Persistenza e integrità dell'inventario depositato all'interno dello shed centrale entro il limite di capienza configurato (`shedCapacity`, default 100).

### `shed_overflow_loss`
- **Tipo:** `CONSTRAINT / COST`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Perdita irreversibile di inventario per saturazione della capacità dello shed (`shedCapacity`), distinta nelle due cause reali di engine:
  1. `MANUAL_DROP`: scarica fino a capienza residua e **cancella irreversibilmente l'intero inventario eccedente del worker**;
  2. `EOD_AUTO_DROP`: la procedura automatica a fine giornata scarica fino a capienza residua e **cancella irreversibilmente l'eccedenza**.
  *Nota:* L'azione `PLACE` nello shed **è conservativa** (trasferisce la quota possibile e trattiene il residuo nel worker).

### `endgame_shutdown_timing`
- **Tipo:** `TIMING`
- **Evidence status:** `POLICY_DECLARED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Orizzonte temporale pianificato in cui cessa l'avvio di nuovi cicli biologici non completabili prima di `episodeSteps` (`POLICY_CONTEXT`).

### `endgame_inventory_liquidation`
- **Tipo:** `FLOW / TIMING`
- **Evidence status:** `POLICY_DECLARED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Flusso e tempistica di liquidazione programmata delle scorte prima del termine della simulazione (`POLICY_CONTEXT`).

---

## G. Condizione del campo, tile lifecycle e recovery

### `field_cleanliness_state`
- **Tipo:** `STATE`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Presenza, densità e distribuzione spaziale delle erbe infestanti (`WEED`) sulla superficie posseduta.

### `tile_lifecycle_state` (CORR-07)
- **Tipo:** `STATE / DERIVED_METRIC`
- **Evidence status:** `DERIVED_ENGINE_FACT`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Partizione fisica esaustiva e deterministica dello stato della tile nell'ambiente (5 viste ambientali pure):
  1. `OUT_OF_SCOPE`: tile bloccata (`"LOCKED"`) o struttura (`"COOP"`, `"PASTURE"`);
  2. `LOST_WEED`: tile infestata da erbacce (`"WEED"`);
  3. `EMPTY_AVAILABLE`: tile arabile sbloccata libera (`None`);
  4. `HARVEST_READY`: tile con pianta matura soddisfacente `crop_harvest_readiness`;
  5. `GROWING`: tile con pianta in accrescimento non ancora matura.
  *Nota:* L'assegnazione al working set (`in_working_set`) e la marcatura per il ritiro (`policy_retirement_due`) sono sovrapposizioni di policy (`POLICY_CONTEXT`).

### `tile_care_due_condition`
- **Tipo:** `STATE / CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Condizione ortogonale che segnala la necessità immediata di irrigazione (`consecutive_unwatered == 1` $\land$ `watered_today == False`) per prevenire la morte della pianta all'EOD.

### `preventive_dig_action`
- **Tipo:** `FLOW`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Esecuzione pianificata di `DIG` su una pianta marcata per il ritiro (`policy_retirement_due`) per liberare la tile.

### `recovery_dig_action`
- **Tipo:** `FLOW / COST`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Esecuzione di emergenza dell'azione `DIG` su una tile caduta nello stato `LOST_WEED` per bonificare l'infestazione.

### `weed_backlog_cost`
- **Tipo:** `COST / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Costo in termini di azioni worker e tempo impiegato per bonificare le infestazioni da weed accumulate sul terreno.

---

## H. Vincoli strutturali, diagnostica e outcome

### `market_order_batch_limit`
- **Tipo:** `CONSTRAINT`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Limite strutturale parametrico al numero massimo di ordini di mercato emettibili in un singolo turno (`maxMarketOrdersPerTurn`, default: 10).

### `action_order_slot_pressure`
- **Tipo:** `CONSTRAINT / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Saturazione del batch ordini di mercato rispetto alla domanda simultanea di transazioni.

### `state_capacity_alignment`
- **Tipo:** `INTERACTION / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Valutazione a posteriori dell'allineamento dimensionale tra espansione del terreno, bestiame, forza lavoro e risorse.

### `local_kaggle_fidelity_gap`
- **Tipo:** `CONSTRAINT / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Scostamento quantificabile tra prestazione in simulazione locale e runtime ufficiale Kaggle.

### `operational_divergence_onset`
- **Tipo:** `TIMING / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Istante temporale (giorno/step) in cui due configurazioni o modelli manifestano la prima deviazione significativa nei pattern operativi.

### `economic_lock_in_onset`
- **Tipo:** `TIMING / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY`
- **Descrizione:** Metrica diagnostica retrospettiva post-match che identifica a posteriori l'istante in cui una deviazione operativa è sfociata in un divario economico cumulato non più recuperabile (`POST_HOC_METRIC`).

### `final_money_outcome`
- **Tipo:** `OUTCOME / POST_HOC_METRIC`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `OUTCOME_ONLY`
- **Descrizione:** Saldo monetario finale realizzato dall'agente al termine dell'episodio (`step >= episodeSteps`).

---

## I. Clock, serviceability e coordinamento temporale

### `canonical_clock_coordinate`
- **Tipo:** `STATE / TIMING`
- **Evidence status:** `ENGINE_VERIFIED`
- **Osservabilità:** `ONLINE_OBSERVABLE`
- **Descrizione:** Coordinata temporale esatta $(\text{step}, \text{day}, \text{hour})$ legata dall'invariante:
  $$\text{step} \equiv \text{day} \cdot T + \text{hour}, \quad \text{con } T = \text{turnsPerDay}$$
  L'EOD si attiva allo step $\text{EOD\_STEP}(d) = (d+1) \cdot T - 1$.

### `action_eligible_now`
- **Tipo:** `STATE / DERIVED_METRIC`
- **Evidence status:** `DERIVED_ENGINE_FACT`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Predicato deterministico online che certifica la legalità immediata di una specifica azione per un worker nello step corrente, verificando tutte le guardie reali di `_apply_unit_action`.

### `reserved_serviceable_before_deadline`
- **Tipo:** `STATE / CAPACITY`
- **Evidence status:** `POLICY_DECLARED`
- **Osservabilità:** `ONLINE_DERIVABLE`
- **Descrizione:** Stima e prenotazione deliberativa della fattibilità pianificata di servire un'entità entro la scadenza biologica (`POLICY_CONTEXT`).

### `realized_serviceable_in_window`
- **Tipo:** `EFFICIENCY / DERIVED_METRIC`
- **Evidence status:** `DERIVED`
- **Osservabilità:** `TELEMETRY_ONLY / POST_HOC_METRIC`
- **Descrizione:** Valutazione a posteriori dell'effettivo completamento del servizio entro la finestra biologica utile.

---

## 4. Relazioni canoniche C2

### Terreno, Workforce e Produttività
- `land_surface_total enables activated_land_surface`
- `activated_land_surface enables maintained_productive_surface`
- `maintained_productive_surface enables monetized_productive_output`
- `workforce_headcount enables worker_capacity_available`
- `worker_capacity_available enables productive_action_share`
- `worker_multi_occupancy eliminates_collision_constraint_on workforce_transit`
- `movement_overhead constrains worker_action_monetization_rate`
- `necessary_transit_fraction qualifies movement_overhead`
- `routing_completion_efficiency qualifies movement_overhead`
- `action_dispatch_failure constrains productive_action_share`

### Crop, Maturity, Lifecycle e Care
- `planting_action_flow transitions tile_lifecycle_state (EMPTY_AVAILABLE -> GROWING)`
- `first_yield_day constrains crop_harvest_readiness`
- `crop_harvest_readiness enables crop_harvest_action_flow`
- `crop_harvest_action_flow transitions tile_lifecycle_state (HARVEST_READY -> EMPTY_AVAILABLE)`
- `watering_execution_rate contributes_to crop_care_action_flow`
- `watering_continuity prevents crop_decay_risk_window`
- `fertilizer_effect_window bounds crop_fertilizer_bonus`
- `crop_fertilizer_bonus qualifies monetized_productive_output`
- `tile_care_due_condition qualifies crop_care_action_flow`
- `preventive_dig_action transitions tile_lifecycle_state (GROWING / HARVEST_READY -> EMPTY_AVAILABLE)`
- `recovery_dig_action transitions tile_lifecycle_state (LOST_WEED -> EMPTY_AVAILABLE)`
- `crop_decay_risk_window transitions tile_lifecycle_state (GROWING / HARVEST_READY -> LOST_WEED)`

### Livestock, Feed, Cura e Byproducts
- `livestock_headcount enables livestock_structural_capacity`
- `pasture_capacity_alignment enables livestock_structural_capacity`
- `livestock_headcount enables livestock_base_production`
- `feed_availability is_prerequisite_for livestock_feed_action_flow`
- `livestock_feed_action_flow prevents animal_escape_condition`
- `livestock_feed_action_flow AND livestock_care_action_flow produces pending_care_bonus_accumulation`
- `pending_care_bonus_accumulation qualifies livestock_product_flow`
- `livestock_headcount enables fertilizer_available_state`
- `fertilizer_available_state enables fertilizer_byproduct_flow`
- `feed_market_dependency interacts_with operating_cash_buffer`

### Capitale, Mercato, Storage e Clock
- `canonical_clock_coordinate governs land_purchase_timing`
- `canonical_clock_coordinate governs crop_horizon_alignment`
- `action_eligible_now is_prerequisite_for productive_action_share`
- `reserved_serviceable_before_deadline interacts_with crop_care_completion_rate`
- `current_money_state enables market_transaction_value`
- `market_transaction_value measures feed_market_expenditure`
- `market_transaction_value measures product_mix_revenue`
- `shared_market_contention_externality modifies market_transaction_value`
- `dynamic_market_price_elasticity conditions shared_market_contention_externality`
- `shared_market_contention_externality requires post_transition_observation`
- `inventory_to_cash_conversion produces reinvestment_cash_flow`
- `operating_cash_buffer defines deployable_capital_window`
- `deployable_capital_window enables land_purchase_timing`
- `asset_liquidity_lag constrains reinvestment_cash_flow`
- `market_sellthrough_lag constrains reinvestment_cash_flow`
- `shed_inventory_integrity constrains shed_overflow_loss`
- `shed_overflow_loss constrains unsold_inventory_value`
- `endgame_shutdown_timing interacts_with endgame_inventory_liquidation`
- `market_order_batch_limit constrains hire_order_scheduling`
- `market_order_batch_limit interacts_with action_order_slot_pressure`
- `local_kaggle_fidelity_gap qualifies local_performance_claims`

---

## 5. Separazioni canoniche non negoziabili C2

1. **Terreno posseduto $\neq$ Terreno attivato $\neq$ Terreno mantenuto:** la proprietà fondiaria non implica produzione attiva né manutenzione sostenibile.
2. **Worker headcount $\neq$ Throughput operativo $\neq$ Azioni monetizzate:** avere più worker non aumenta il valore generato se il movimento saturano la capacità temporale.
3. **Capienza Worker (Inesistente) $\neq$ Resa Massima su Tile Animale (`max_held`):** i worker non hanno limite di carico nell'inventario; `max_held` limita l'accumulo sulla tile della struttura animale.
4. **`yield available` $\neq$ `harvest ready`:** la presenza di resa non abilita `HARVEST` prima del compimento di `first_yield_day`.
5. **Scadenza contrattuale $\neq$ Perdita di inventario:** il reset a EOD degli Hands esegue un auto-drop nello shed, distruggendo solo l'eccedenza oltre `shedCapacity`.
6. **`MANUAL_DROP` / `EOD_AUTO_DROP` (Distruttivi) $\neq$ `PLACE` (Conservativo):** il drop cancella l'eccedenza; il place trasferisce solo fino a capienza e preserva il resto nel worker.
7. **Produzione / Raccolta $\neq$ Ricavo monetario:** la raccolta incrementa le scorte; la monetizzazione richiede ordini `SELL` a mercato.
8. **`tile_lifecycle_state` (5 Viste Fisiche) $\neq$ `POLICY_CONTEXT` Overlays:** l'ambiente espone 5 stati fisici; `in_working_set` e `policy_retirement_due` sono decisioni dell'agente.
9. **Preventive DIG $\neq$ Recovery DIG:** la rimozione di una pianta per rotazione è deliberativa; lo scavo su `LOST_WEED` è bonifica di un danno.
10. **Fertilizer applicato $\neq$ Boost incondizionato:** l'uplift colturale a 2 unità a EOD richiede che la pianta sia stata irrigata (`was_watered == True`) nella giornata corrente.
11. **FEED (Sopravvivenza/Bonus) $\neq$ Gate di Produzione Base:** l'alimentazione evita la fuga ed abilita il care bonus; non condiziona l'erogazione del base output $=1$.
12. **`ACTION_REQUEST` $\neq$ `SNAPSHOT_ELIGIBILITY` $\neq$ `EXECUTION_OUTCOME` $\neq$ `POST_STATE_EVIDENCE`:** la catena causale temporale separa rigorosamente intenzione, legalità a priori, esito engine ed evidenza post-stato.
13. **Costruzione Strutture $\neq$ Esborso Monetario:** `BUILD_COOP` e `BUILD_PASTURE` costano 0 cassa nell'engine.

---

## 6. Concetti model-local e policy esclusi dall'ontologia

Restano categoricamente esclusi dall'ontologia canonica:
- assunzioni dogmatiche di convenienza economica;
- target rigidi di bestiame o sblocco terreni;
- soglie numeriche obbligatorie di cassa o riserva;
- regole di routing algoritmico proprietario;
- classi o nomi di agenti;
- script di submission o configurazioni di packaging.

---

## 7. Tracciabilità dei termini storici e mapping C1 $\to$ C2

| Termine storico C1 | Stato C2 | Trattamento in C2 |
|---|---|---|
| `contract_inventory_loss` | **CORRETTO** | Rinominato/ridefinito come `shed_overflow_loss`. |
| `shed_overflow_eod_loss` | **REVISED** | Generalizzato in `shed_overflow_loss` (`MANUAL_DROP` ed `EOD_AUTO_DROP`). |
| `harvest_readiness` | **AGGIUNTO** | Formalizzato come `crop_harvest_readiness` vincolato da `first_yield_day`. |
| `tile_lifecycle` | **REVISED** | Formalizzato come `tile_lifecycle_state` a 5 stati fisici + 2 overlay di policy. |
| `care_due` | **AGGIUNTO** | Formalizzato come `tile_care_due_condition` ortogonale al lifecycle. |
| `worker_multi_occupancy` | **AGGIUNTO** | Promosso a `ENGINE_VERIFIED`. |
| `worker_capacity` | **CORRETTO** | Riconosciuta l'assenza di capienza fisica di carico del lavoratore (`_inv_add`). |
| `livestock_capacity` | **DEPRECATED / SPLIT** | Suddiviso in `livestock_structural_capacity` e `livestock_output_storage_capacity` (`max_held`). |
| `fertilizer_window` | **CORRETTO** | Formalizzato come `fertilizer_effect_window` (`day..day+2`, richiede `was_watered`). |
| `care_bonus_accumulation` | **CORRETTO** | Formalizzato con reset programmato ad ogni produzione (`pending_care_bonus_accumulation`). |
| `structure_cost` | **CORRETTO** | Formalizzato a costo monetario 0 (`structure_construction_cost`). |
| `feed_production_gate` | **FALSIFICATO** | Sostituito da `livestock_base_production` dissociato da FEED. |
| `chicken_species` | **DEPRECATED** | Dichiarato `CHICKEN = NOT_SUPPORTED`; sostituito da `GOOSE`. |

---

## 8. Contratto di osservabilità, no-future-leakage e telemetry

Ogni analisi o componente di feature engineering deve rispettare le quattro classi di osservabilità:
1. **Stato Online Primario (`ONLINE_OBSERVABLE`):** grandezze direttamente esposte dall'observation dictionary (`step`, `money`, `farmer_pos`, `inventory`, `tiles`, `market_prices`, `day`).
2. **Stato Derivato Online (`ONLINE_DERIVABLE`):** grandezze computabili deterministicamente dallo stato corrente senza informazione futura (`crop_harvest_readiness`, `tile_lifecycle_state`, `tile_care_due_condition`, `fertilizer_effect_window`, `action_eligible_now`, `livestock_structural_capacity`).
3. **Contesto di Policy / Pianificazione (`POLICY_DECLARED`):** grandezze generate dalla deliberazione dell'agente (`reserved_serviceable_before_deadline`, `livestock_serviceable_capacity`, `feed_security_buffer`, `operating_cash_buffer`, `deployable_capital_window`, `in_working_set`, `policy_retirement_due`).
4. **Telemetria Post-Azione e Outcome (`TELEMETRY_ONLY / POST_HOC_METRIC`):** evidenze registrate a posteriori (`realized_serviceable_in_window`, `necessary_transit_fraction`, `routing_completion_efficiency`, `shed_overflow_loss`, `action_dispatch_failure`, `economic_lock_in_onset`, `final_money_outcome`).

La categoria 4 include inoltre `market_transaction_value` e `shared_market_contention_externality`: il prezzo quotato corrente è osservabile, mentre fill, prezzo realizzato e impatto dell'ordine simultaneo avversario sono disponibili soltanto dopo la transizione.

**Vincolo di No-Future-Leakage:** nessun dato appartenente a *Telemetria Post-Azione* o *Outcome* può essere consumato come feature decisionale online prima della conclusione della finestra/evento a cui si riferisce.

---

## 9. Delta C2.1 sottoposti a revisione

1. corretto il percorso canonico della liquidità online;
2. riclassificato il controvalore effettivo di mercato come telemetria post-azione;
3. introdotta l'esternalità di contesa del mercato condiviso;
4. mantenuta la separazione tra fatti di dominio, contesto di policy e metriche post-hoc;
5. esclusi falsi costi salariali a EOD: `HIRE` addebita soltanto il costo Fibonacci al commit dell'ordine e gli Hands scadono a EOD senza un secondo addebito.

**Fine di ONTOLOGY C2.1 (Reconciled; Foundation post-3Q completata).**


## Checkpoint operativo 2026-09-08: V48 e PASS

Distinguere capacità disponibile, lavoro biologico dovuto, lavoro fattibile e attesa. PASS è un esito osservabile, non prova di assenza di lavoro. Piante produttive, esaurite e prodotto detenuto sono concetti distinti. Le categorie diagnostiche di policy non sono nuove regole dell’engine.

Pianificazione e inventario downstream: [V48 e priorità PASS](../V48_PLANNING_AND_BUILD_IT.md). Nessuna modifica alle costanti dell’engine; supplemento operativo alla baseline riconciliata.
