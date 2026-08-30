# POST-E15 — MODEL_SPEC INDEPENDENT REVISION
## MODELER_ID = COPILOT

**Stato del documento:** candidate MODEL_SPEC revision. Non sostituisce [MODEL_SPEC_COPILOT_E15_FROZEN.md](../../../../results/e15/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md) e non è il MODEL_SPEC definitivo del round successivo. Nessun artefatto frozen è stato modificato. Nessun file oltre al presente è stato toccato. Non ho letto capability check o revisioni prodotte da Antigravity o Codex (verificato: [docs/model/model_specs/copilot/](.) non conteneva altri file al momento della scrittura).

`Victory != Model Validity.` `Defeat != Model Falsification.`

---

## 0. Legenda di provenienza

Ogni affermazione in questo documento è esplicitamente etichettata con la sua fonte epistemica primaria:

| Tag | Significato | Fonte primaria |
|---|---|---|
| **[FRAME]** | METHODOLOGICAL FRAME | [README.md](../../../../README.md), [ONTOLOGY_E15_FROZEN.md](../../../../results/e15/freeze/ONTOLOGY_E15_FROZEN.md) |
| **[SPEC-DECL]** | E15 FROZEN MODEL DECLARATION (Copilot, *ex ante*) | [MODEL_SPEC_COPILOT_E15_FROZEN.md](../../../../results/e15/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md) |
| **[PRIMARY-E15]** | MATCH OBSERVATION (E15, *ex post*) | Match M2/M3 JSON, replay visuale, E15 tournament synthesis |
| **[SELF-CHECK]** | POST-E15 SELF CAPABILITY CHECK (Copilot) | [COPILOT_CAPABILITY_CHECK.md](../../../../results/post_e15/capability_check/COPILOT_CAPABILITY_CHECK.md) |
| **[INFERENCE]** | Inferenza autonoma prodotta in questa revisione | Ragionamento originale in questo documento |

---

## A. Baseline reconstruction

### A.1 Principi del MODEL_SPEC E15 Copilot **[SPEC-DECL]**
Architettura dichiarata: "low-capacity, state-gated throughput policy" (`E12_X115_COPILOT_INDEPENDENT`). Principio centrale: l'allineamento fra working set, cash, pasture capacity e active crops è il driver primario, non "capacity first" né "Q2 always". Pre-E15 erano già state effettuate tre rimozioni esplicite (`fixed_hire_count`, `fixed_q2_priority`, `fixed_field_cleanliness_priority`) e tre riformulazioni (`target_cows`, `target_sheep`, `land_unlock_condition` → gate dinamici invece di target/giorni fissi).

Ranking *ex ante* (12 fattori, Section 4 del frozen spec):

| Rank | Nome locale | Impact | Confidence | Evidence status |
|---:|---|---|---|---|
| 1 | `throughput_to_cash_conversion` | Critical | Medium | SUPPORTED |
| 2 | `working_set_capacity_gate` | Critical | Medium | SUPPORTED |
| 3 | `crop_activation_and_monetization` | Critical | Medium | SUPPORTED |
| 4 | `land_unlock_condition` | High | Medium | SUPPORTED |
| 5 | `pasture_to_livestock_alignment` | High | Medium | SUPPORTED |
| 6 | `wheat_feed_security` | High | Medium | SUPPORTED |
| 7 | `cash_buffer_before_expansion` | High | Medium | WEAKLY_SUPPORTED |
| 8 | `milestone_day_gating` | Medium | Medium | WEAKLY_SUPPORTED |
| 9 | `herd_target_sensitivity` | Medium | Low | WEAKLY_SUPPORTED |
| 10 | `inventory_liquidation_and_shed_flush` | Medium | Medium | SUPPORTED |
| 11 | `field_cleanliness_priority` | Low | Medium | CONTRADICTED (deprecated) |
| 12 | `fixed_hire_count` | Low | High | FALSIFIED (removed) |

### A.2 Comportamento E15 osservato **[E15-EVIDENCE]**
Footprint riprodotto identicamente in M2 e M3: WATER 446/439, max pasture 5, max animali 4, max hands 9, SELL orders 298/302, 2 quadranti in entrambi i match, nessun Q2. Copilot ha vinto entrambi i match giocati (2–0 complessivo E15).

### A.3 Layer diagnosis — riconfermata, non ri-derivata **[SELF-CHECK]**
- **MODEL_VALIDITY:** `SUBSTANTIALLY_SUPPORTED`. I tre principi Rank 1–3 sono coerenti con M2/M3.
- **POLICY_REALIZATION:** `SUPPORTED`. Il footprint M2→M3 è quasi identico al comportamento dichiarato.
- **IMPLEMENTATION_FIDELITY:** `UNRESOLVED`. Nessun audit del codice sorgente è stato condotto; la stabilità comportamentale non prova correttezza di implementazione.

Non ri-derivo questi tre giudizi da zero: restano quelli del capability check, perché nessuna nuova evidenza E15 è stata introdotta da allora.

### A.4 Proposizioni supportate, indebolite, falsificate o unresolved **[SELF-CHECK] + [INFERENCE]**
- **Supportate:** `throughput_to_cash_conversion`, `working_set_capacity_gate`/`state_capacity_alignment`, `crop_activation_and_monetization`, `pasture_to_livestock_alignment`.
- **Indebolite (non falsificate):** `working_set_capacity_gate` come *meccanismo distintivo* — il proprio audit M2 lo classifica `NOT_DISCRIMINATED` perché entrambi i giocatori mostravano un gate attivo; ciò che discrimina è la *qualità* dell'allineamento, non la presenza del gate.
- **Confermate per assenza di smentita, non per prova diretta:** `wheat_feed_security` come formulazione "buffer/autarky forte" — M2/M3 mostrano Copilot vincere con intenso flusso di mercato Wheat, quindi la lettura autarchica resta `CONFOUNDED`.
- **Non testate in E15:** `herd_target_sensitivity` (differenziale Cow/Sheep — Copilot non ha mai schierato Sheep), `market_churn_cost` (mai quantificato).

### A.5 Correzioni rispetto al proprio capability check **[INFERENCE]**

Il capability check ha classificato `land_surface_total`, `workforce_headcount` e `livestock_headcount` come `NOT_FEATURE` con `relationship: non_monotonic`. Applicando la regola epistemica esplicita di questo task ("Non basta che 'più X non è sempre meglio' [...] o che non emerga monotonicità" per giustificare `NOT_FEATURE`), quella classificazione era **troppo aggressiva** e la correggo qui:

1. **`land_surface_total` → riclassificato `FEATURE` (`relationship: non_monotonic`, non `NOT_FEATURE`).** La superficie totale resta una precondizione abilitante (`land_surface_total enables activated_land_surface`, relazione canonica esplicita in ONTOLOGY_E15_FROZEN §4); E15 mostra solo che non è una condizione *sufficiente*, non che sia irrilevante.
2. **`workforce_headcount` → riclassificato `FEATURE` (`relationship: non_monotonic`).** Stesso ragionamento: il conteggio hands abilita capacità di dispatch ma non la garantisce.
3. **`livestock_headcount` → riclassificato `FEATURE` (`relationship: non_monotonic`).** Il README **[FRAME]** lo dichiara esplicitamente come esempio canonico: *"17–18 animali perdenti contro 4–7 non implica max_herd = 4: suggerisce che `livestock_headcount` merita di essere trattato come feature"*. Il mio capability check contraddiceva direttamente questa affermazione di frame; la correggo.

Confermo invece `NOT_FEATURE` per `productive_action_share` e `field_cleanliness_state`, perché in questi due casi l'evidenza supera la soglia "non è sufficiente che il valore maggiore abbia perso una volta": entrambi i concetti non discriminano **mai** (0/3 match) nella direzione attesa, e in un caso (M2 per `productive_action_share`, M1 per `field_cleanliness_state`) mostrano un'**inversione pulita** (il valore aggregato più alto perde). Questo è un'evidenza di deprioritizzazione reale, non semplice non-monotonicità.

---

## B. Concept-by-concept revision

### Rank 1 — `throughput_to_cash_conversion`

```text
concept_id: monetized_productive_output / worker_action_monetization_rate
feature_status: FEATURE
e15_relationship: positive come proxy macro; forma "netta" (dichiarata nello SPEC-DECL ma mai calcolata nei tre match) non verificata
current_initial_bound: not_established in valore assoluto; osservato solo il confronto relativo $7.13/azione (Copilot) vs $5.17/azione (Codex) in M2, proxy macro non ledger-based
parameter_or_hyperparameter: DERIVED_METRIC
next_training_values: calcolare esplicitamente sia forma macro sia forma netta (esclude MOVE) su ogni match futuro, non solo la forma macro
confounders: denominatore include ~70% MOVE in tutti i match; due policy con MOVE-share identico e monetizzazione diversa nascondono l'eterogeneità nella qualità delle azioni non-movement
validation_requirement: replica su ≥3 seed nuovi con entrambe le forme (macro e netta) calcolate esplicitamente, senza ri-userare i valori M2/M3 per tarare soglie
falsification_condition: se la forma netta invertisse il ranking Copilot/Codex osservato in M2, il concetto andrebbe riformulato come artefatto del denominatore aggregato
change_from_e15_spec: REVISED
change_rationale: rank/impact/confidence invariati; la propria correzione (Copilot audit M2: rank1 "NOT_DISCRIMINATED" come meccanismo) impone di non promuovere ulteriormente la confidence finché la forma netta non è misurata
```

### Rank 2 — `working_set_capacity_gate` / `state_capacity_alignment`

```text
concept_id: state_capacity_alignment
feature_status: FEATURE
e15_relationship: conditional / interaction — concetto più consistentemente SUPPORTED nei tre match, ma mai operazionalizzato con una formula
current_initial_bound: not_established — nessun match riporta un "alignment score" calcolato; l'evidenza è qualitativa (nominal capacity ≫ maintained capacity → perdita; nominal ≈ maintained/monetizzata meglio → vittoria)
parameter_or_hyperparameter: HYPERPARAMETER (le soglie del gate — cash minimo, crop attivi minimi, pasture readiness — sono impostazioni di policy configurabili)
next_training_values: pre-registrare una formula esplicita (es. crop_surface_maintained / activated_land_surface, oppure monetized_productive_output / worker_capacity_available) PRIMA di osservare il risultato del prossimo match
confounders: senza formula pre-registrata, il concetto rischia di essere un'etichetta post-hoc coerente con qualunque esito già noto (conferma circolare)
validation_requirement: applicare la formula pre-registrata a match futuri e verificare se il ranking per "alignment score" precede effettivamente il ranking per final_money, non il contrario
falsification_condition: un match dove il computed alignment score è più basso nel vincitore falsificherebbe la formula proposta (non il concetto stesso, che potrebbe richiedere riformulazione)
change_from_e15_spec: REVISED
change_rationale: retained come rank 2 critical, ma downgrade esplicito da "meccanismo distintivo dimostrato" a "fenomeno qualitativo da operazionalizzare", come già segnalato nel proprio audit M2 ("working_set_capacity_gate = WEAKENED perché entrambi i giocatori hanno un gate attivo")
```

### Rank 3 — `crop_activation_and_monetization`

```text
concept_id: crop_surface_maintained + watering_execution_rate (scorporati)
feature_status: FEATURE
e15_relationship: crop_surface_maintained = positive con evidenza di saturazione (M2: 28 batte 37); watering_execution_rate = thresholded (34/30 falliscono, 439/475/446 riescono, ma 475>446 perde)
current_initial_bound: watering — failure osservato ≤34, successo osservato ≥439; intervallo 35–438 mai campionato. crop_surface_maintained — failure osservato ≤9, successo osservato 25–28; 37 osservato con esito peggiore di 28 (non un limite superiore dimostrato, un solo punto dati)
parameter_or_hyperparameter: watering_execution_rate = DERIVED_METRIC (emerge dal dispatch, non è settato direttamente); il peso di priorità watering nel dispatcher = PARAMETER; il target dimensionale del working set crop = HYPERPARAMETER
next_training_values: watering — 100/200/300 azioni equivalenti per mappare il buco 35–438 (richiede varianti di policy, non le sole submission frozen); crop_surface_maintained — testare working set a 20/25/30/35 tenendo fissi gli altri fattori
confounders: watering e crop-surface sono realizzati dalla stessa policy che decide anche workforce/quadranti/dispatch; mai variati isolatamente
validation_requirement: nuovi seed con la submission frozen invariata per vedere se il pattern 28<37 (M2) si conferma o è rumore di singolo seed, prima di qualunque riformulazione del target di working set
falsification_condition: un working set Copilot-style a 35-37 crop che batte 28 a parità di altri fattori indebolirebbe l'ipotesi di saturazione intorno a 28
change_from_e15_spec: REVISED
change_rationale: lo SPEC-DECL trattava questi due fenomeni come un unico concetto bundled (`crop_activation_and_monetization`); l'evidenza E15 giustifica di scorporarli perché mostrano forme di relazione diverse (thresholded vs positive-con-saturazione) e conseguenze di tuning diverse
```

### Rank 4 — `land_unlock_condition`

```text
concept_id: land_surface_total + land_activation_payback
feature_status: FEATURE
e15_relationship: land_surface_total = non_monotonic (corretto da NOT_FEATURE, vedi §A.5); land_activation_payback = conditional
current_initial_bound: not_established come variabile indipendente — mai isolata da workforce/livestock scaling simultaneo negli avversari osservati; Copilot stesso non ha mai attivato un Q2 in nessun match E15, quindi non esiste osservazione diretta Copilot di un'espansione territoriale riuscita o fallita
parameter_or_hyperparameter: HYPERPARAMETER (soglie di cash/crop-readiness che gatano l'acquisto di nuova superficie)
next_training_values: testare l'attivazione di un Q2 Copilot-style SOLO quando maintained_productive_surface e cash superano soglie dichiarate esplicitamente, e confrontare con il branch attuale "resta a 2Q"
confounders: negli avversari osservati (Antigravity), il timing dell'acquisto di land coincide sempre con ramp di workforce e livestock; non è mai stato isolato l'effetto marginale della sola superficie
validation_requirement: nessuna osservazione diretta di un'espansione territoriale Copilot esiste ancora; richiede un match dove la submission (variante futura, non quella frozen) acquisisce Q2 sotto le condizioni di gate dichiarate
falsification_condition: un Q2 acquisito sotto le condizioni di gate proposte che non produce crescita proporzionale di crop_surface_maintained entro un numero di giorni dichiarato falsificherebbe la sufficienza del gate attuale
change_from_e15_spec: REVISED
change_rationale: il gate stesso resta valido (rank 4, high impact), ma la componente `land_surface_total` è ripristinata a FEATURE per la ragione esposta in §A.5; inoltre si segnala che il gate non è mai stato osservato "attivarsi" nei match E15 (Copilot resta sempre a 2Q) — è quindi una regola non ancora testata positivamente, solo per assenza
```

### Rank 5 — `pasture_to_livestock_alignment`

```text
concept_id: pasture_arable_surface_tradeoff + livestock_headcount + pasture_capacity_alignment
feature_status: FEATURE
e15_relationship: pasture_arable_surface_tradeoff = negative (3/3 match coerenti); livestock_headcount = non_monotonic (corretto da NOT_FEATURE, vedi §A.5)
current_initial_bound: pasture — failure osservato a 9 e 18, success osservato a 5, intervallo 6–8 mai testato. livestock — intervallo iniziale 4–17 esplicitamente dichiarato non-ottimale dal README **[FRAME]**, da restringere non da fissare
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: pasture 5/7/9 a parità di crop-surface target (rompe la collinearità pasture↔animali); herd 4/7/10/13 (i valori di restringimento già indicati nel README, mai eseguiti)
confounders: pasture size e livestock_headcount sono quasi perfettamente collineari nei dati osservati (18↔18, 9↔7, 5↔4); l'effetto attribuito al numero di animali potrebbe appartenere in parte alla superficie pasture
validation_requirement: nuovi match/seed con herd size intermedio (7-13) e pasture scorporata dal conteggio animali, prima di stringere ulteriormente l'intervallo
falsification_condition: un herd di 10-13 correttamente allineato a pasture/feed che produce final_money comparabile o superiore a 4-7 falsificherebbe un vantaggio specifico degli herd piccoli in sé
change_from_e15_spec: REVISED
change_rationale: direzione e rank confermati; livestock_headcount ripristinato a FEATURE (§A.5); l'intervallo 4-17 è esplicitamente mantenuto largo, coerentemente con il vincolo di questo task di non trasformare un'osservazione in soglia
```

### Rank 6 — `wheat_feed_security`

```text
concept_id: feed_market_dependency + feed_security_buffer + wheat_operating_flow
feature_status: UNRESOLVED
e15_relationship: unresolved/confounded — CONFOUNDED in tutti e 3 i match; Copilot vince in M2/M3 pur con intenso flusso di mercato Wheat (BUY_PRODUCT richiesto 1.828-1.889), il che indebolisce la lettura "buffer interno forte/autarky" dichiarata nello SPEC-DECL
current_initial_bound: non proponibile — nessun match isola il costo netto della dipendenza dal mercato (manca ledger eseguito, vedi Sezione D)
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT (prima di poter trattare questo come parametro/hyperparameter serve un ledger eseguito con prezzo)
next_training_values: nessuno responsabile finché manca l'osservabilità; non proporre soglie di buffer interno finché il costo del market-flow non è quantificato
confounders: la quantità RICHIESTA di Wheat non distingue acquisto di emergenza (prezzo penalizzato) da flusso operativo deliberato per liquidità
validation_requirement: executed transaction ledger con prezzo per ordine, su nuovi seed
falsification_condition: se il ledger mostrasse che Copilot paga sistematicamente prezzi peggiori per il Wheat acquistato rispetto agli avversari, l'ipotesi "il market-flow è compatibile con sicurezza operativa" (proposta nel proprio consensus M2/M3) andrebbe indebolita
change_from_e15_spec: REVISED
change_rationale: downgrade da SUPPORTED (SPEC-DECL) a UNRESOLVED; lo SPEC-DECL trattava `wheat_feed_security` come un concetto singolo con polo negativo "dipendenza dal mercato"; l'evidenza E15 impone di separare esplicitamente "internal buffering" da "market-flow management" perché il secondo non si è mostrato dannoso quando Copilot lo ha usato intensamente e ha comunque vinto
```

### Rank 7 — `cash_buffer_before_expansion`

```text
concept_id: operating_cash_buffer + deployable_capital_window
feature_status: FEATURE (deployable_capital_window) / UNRESOLVED (operating_cash_buffer in valore assoluto)
e15_relationship: deployable_capital_window = positive (timing dell'investimento, non l'ammontare); operating_cash_buffer = non_monotonic/thresholded verso il basso, CONFOUNDED
current_initial_bound: Copilot stesso ha operato con cash quasi a $225-$227 (M2 Day9, M3 Day9) senza conseguenze negative — questo è un dato Copilot-specifico che indebolisce l'idea di un "buffer minimo" fisso superiore a queste cifre; non propongo un bound numerico per il buffer
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: nessun valore di buffer minimo proponibile responsabilmente; priorità a separare "cash basso per scelta" da "cash basso per fallimento di conversione" (vedi confounder)
confounders: il livello di cash è un effetto a valle di tutte le decisioni di spesa simultanee; trattarlo come causa indipendente rischia di invertire la direzione causale reale
validation_requirement: nuovi seed dove si registri la traiettoria di cash giorno per giorno insieme al breakdown delle spese, per distinguere le due letture
falsification_condition: un match dove un buffer di cash elevato e stabile produce comunque un risultato peggiore di un buffer variabile/basso confermerebbe che il livello assoluto non è la variabile rilevante (già parzialmente osservato in M2)
change_from_e15_spec: REVISED
change_rationale: confidence esplicitamente non promossa oltre WEAKLY_SUPPORTED/LOCAL_ONLY (invariata dallo SPEC-DECL); si aggiunge la distinzione esplicita fra le due componenti, prima bundled
```

### Rank 8 — `milestone_day_gating`

```text
concept_id: land_purchase_timing (componente) + economic_lock_in_onset (diagnostica correlata)
feature_status: FEATURE (come fenomeno di timing) — ma la formulazione "giorno fisso" resta deprecata
e15_relationship: economic_lock_in_onset varia ampiamente fra i tre match (Day 19 in M1, ~Day 12 in M2, Day 10 Hour 12 in M3): questo CORROBORA, senza introdurre nuova evidenza contraria, la decisione pre-E15 di abbandonare i trigger a giorno fisso
current_initial_bound: not_established un giorno comune; i tre valori osservati differiscono per quasi un terzo dell'episodio
parameter_or_hyperparameter: NOT_YET_TUNABLE (concetto già deprecato in favore di gating state-based; non reintrodurre come parametro)
next_training_values: nessuno — non c'è motivo di reintrodurre soglie a giorno fisso
confounders: coincidenza numerica cross-esperimento ("Day 12" appare sia in E13 pre-E15 sia in M2): trattarla come legge universale sarebbe un pattern-matching non giustificato fra esperimenti diversi
validation_requirement: nessuna azione richiesta; monitorare comunque la distribuzione di lock-in su nuovi seed per confermare la varianza osservata
falsification_condition: se la distribuzione di lock-in su più seed si concentrasse strettamente attorno a un giorno specifico, la posizione "nessuna costante universale" andrebbe rivista
change_from_e15_spec: UNCHANGED
change_rationale: la deprecazione pre-E15 (`milestone_day_gating` → REFORMULATE) resta corretta; E15 aggiunge conferma, non correzione
```

### Rank 9 — `herd_target_sensitivity`

```text
concept_id: livestock_headcount (parametro) + species_margin_differential (sotto-claim)
feature_status: FEATURE (livestock_headcount, corretto da NOT_FEATURE) / UNRESOLVED (species_margin_differential)
e15_relationship: livestock_headcount = non_monotonic; species_margin_differential = unresolved (nessun confronto pulito Cow/Sheep — Copilot non ha mai schierato Sheep in E15)
current_initial_bound: livestock 4-17 (non narrowed); species_margin_differential — non proponibile, 2/3 match non contengono Sheep in nessuno dei due giocatori e nel terzo (M1) Sheep compare solo nell'avversario perdente con scala 4× più grande, rendendo l'effetto specie indistinguibile dall'effetto scala
parameter_or_hyperparameter: livestock_headcount = HYPERPARAMETER; species_margin_differential = OBSERVABILITY_REQUIREMENT
next_training_values: 4/7/10/13/17 per herd size; per le specie, un confronto diretto Cow-only vs Sheep-only a parità di headcount e pasture (nessuna submission frozen attuale lo permette)
confounders: herd size collineare con pasture (vedi Rank 5); specie confusa con scala complessiva
validation_requirement: nuovi match con herd a taglia intermedia; per le specie, un esperimento dedicato non ancora progettabile con le sole submission frozen
falsification_condition: vedi falsification_condition del Rank 5 per livestock; per species_margin, qualunque risultato futuro con dati sufficienti a isolare il margine per specie
change_from_e15_spec: REVISED
change_rationale: confidence Low (SPEC-DECL) mantenuta; corretto lo status da NOT_FEATURE implicito (via capability check) a FEATURE esplicito per la componente headcount
```

### Rank 10 — `inventory_liquidation_and_shed_flush`

```text
concept_id: inventory_to_cash_conversion + endgame_inventory_liquidation + shed_inventory_integrity + contract_inventory_loss
feature_status: FEATURE (inventory_to_cash_conversion, come proxy da conteggio ordini) / UNRESOLVED (endgame_inventory_liquidation come contributo causale indipendente)
e15_relationship: inventory_to_cash_conversion = positive (Copilot 298/302 SELL orders vs 212/198 avversari); endgame_inventory_liquidation = CONFOUNDED/INCONCLUSIVE in ogni consensus match — il vantaggio Copilot è già consolidato ben prima della fase di endgame
current_initial_bound: non proponibile in termini di valore monetario reale — tutti i numeri SELL sono conteggi di ordini richiesti, non quantità/valore eseguiti
parameter_or_hyperparameter: inventory_to_cash_conversion = DERIVED_METRIC; endgame_inventory_liquidation timing = HYPERPARAMETER; il valore economico reale = OBSERVABILITY_REQUIREMENT
next_training_values: nessuno responsabile finché manca il ledger eseguito
confounders: più ordini SELL richiesti potrebbero riflettere più tentativi (incl. falliti/ripetuti) piuttosto che più valore effettivamente incassato
validation_requirement: ledger eseguito con prezzo per ordine; senza di esso qualunque soglia sarebbe inventata
falsification_condition: se il ledger mostrasse che gran parte dei 298-302 SELL Copilot falliscono o si annullano reciprocamente (es. wash trading Wheat), la relazione "più SELL orders = più cash" risulterebbe artefattuale
change_from_e15_spec: REVISED
change_rationale: lo SPEC-DECL dichiara "aggressive liquidation... to maximize terminal cash" come se fosse causalmente dimostrato; l'evidenza E15 (CONFOUNDED/INCONCLUSIVE in ogni match) non lo sostiene come contributo indipendente — corretto a UNRESOLVED per questa componente specifica
```

### Rank 11 — `field_cleanliness_priority`

```text
concept_id: field_cleanliness_state + weed_backlog_cost
feature_status: NOT_FEATURE
e15_relationship: unresolved/negative-if-anything — M1: Codex termina con 22 weeds e vince; Antigravity con 5 weeds e perde
current_initial_bound: non applicabile
parameter_or_hyperparameter: NOT_YET_TUNABLE (già deprecato)
next_training_values: nessuno prioritario
confounders: pochi weeds in un giocatore possono riflettere un campo scarsamente coltivato (meno tile attive da infestare), non gestione superiore — causalità potenzialmente invertita
validation_requirement: nessuna azione richiesta a breve termine
falsification_condition: un caso dove un campo pulito E ampiamente coltivato produce un vantaggio economico chiaro rispetto a un campo sporco ma altrettanto coltivato risolleverebbe il concetto
change_from_e15_spec: UNCHANGED
change_rationale: la deprecazione pre-E15 resta valida; l'evidenza E15 (inversione in M1) la rinforza senza modificarla; qui la classificazione NOT_FEATURE è mantenuta esplicitamente perché l'evidenza supera la soglia "sempre non discriminante o invertita", non solo "non monotona" (vedi §A.5)
```

### Rank 12 — `fixed_hire_count`

```text
concept_id: workforce_headcount
feature_status: FEATURE (corretto da NOT_FEATURE — si veda distinzione sotto)
e15_relationship: non_monotonic
current_initial_bound: not_established come variabile indipendente; osservato 9-10 hands nei vincitori (Codex M1, Copilot M2/M3) contro 12 nel perdente ripetuto (Antigravity)
parameter_or_hyperparameter: HYPERPARAMETER
next_training_values: nessun valore aggiuntivo prioritario rispetto a quanto già osservato; risorse andrebbero investite su action_dispatch_failure (vedi sotto) prima che su ulteriori variazioni di headcount
confounders: più hands richiede più coordinamento spaziale (MOVE); il numero di hands è confuso con l'efficienza del routing della stessa policy
validation_requirement: una policy con 12 hands e dispatch quality comparabile ai vincitori attuali, per verificare se il conteggio conta indipendentemente dal dispatch
falsification_condition: se una tale policy perdesse comunque, rafforzerebbe l'irrilevanza del conteggio isolato; se vincesse, andrebbe riconsiderato come feature condizionata alla qualità del dispatch
change_from_e15_spec: REVISED
change_rationale: distinzione esplicita fra la *policy* `fixed_hire_count` (giustamente rimossa pre-E15, resta REMOVED) e il *concetto canonico* `workforce_headcount` (che resta osservabile e rilevante come stato, ripristinato a FEATURE per la ragione in §A.5). Il MODEL_SPEC Copilot non deve confondere "non fissare un numero rigido" con "il numero non conta come variabile di stato"
```

### Aggiunte cross-cutting (non nel ranking Rank 1-12, emerse da E15 come rilevanti per Copilot)

```text
concept_id: action_dispatch_failure
feature_status: UNRESOLVED (per Copilot specificamente)
e15_relationship: negative — firma HARVEST≫PLANT osservata SOLO nell'avversario Antigravity (rapporto 3.74-4.45), mai in Copilot (rapporto ~0.95-0.98)
current_initial_bound: Copilot non mostra la firma di fallimento nei match disputati; questo NON dimostra che il proprio dispatch sia privo di inefficienze su seed non ancora testati — assenza di evidenza non è evidenza di assenza
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT (serve un flag di successo/fallimento per singola azione, oggi assente)
next_training_values: monitorare esplicitamente il rapporto HARVEST/PLANT e altre firme di dispatch anche per Copilot su nuovi seed, non solo per gli avversari
confounders: il rapporto è una proxy, non una misura diretta di fallimento; è anche meccanicamente legato al numero di PLANT oltre che di HARVEST
validation_requirement: telemetria action-level success/failure su nuovi match, inclusi quelli con Copilot come giocatore
falsification_condition: se Copilot mostrasse un rapporto HARVEST/PLANT elevato su un nuovo seed pur vincendo, indebolirebbe il legame fra questa firma e la sconfitta in generale
change_from_e15_spec: ADDED
change_rationale: lo SPEC-DECL tratta `action_dispatch_failure` come PARTIAL/implicito ("failures are monitored but not isolated"); l'evidenza E15 mostra che è uno dei concetti più discriminanti del torneo per l'avversario — merita monitoraggio esplicito anche se Copilot non ne ha mostrato i sintomi finora
```

```text
concept_id: market_transaction_value
feature_status: UNRESOLVED
e15_relationship: unresolved — osservabilità insufficiente in tutti e tre i match (INCONCLUSIVE)
current_initial_bound: non proponibile
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT
next_training_values: nessuno finché l'osservabilità non esiste
confounders: qualunque interpretazione di "prezzo realizzato" costruita sui soli conteggi di ordini richiesti sarebbe una sovrainterpretazione
validation_requirement: aggiungere alla harness la cattura di prezzo × quantità eseguita per ordine
falsification_condition: non applicabile finché l'osservabilità non esiste
change_from_e15_spec: REVISED
change_rationale: lo SPEC-DECL dichiara questo concetto USED/FULL ("Copilot reconstructs transaction prices from action ledgers when available"), ma nessuno dei tre match E15 espone un ledger eseguito nei propri artefatti osservabili (`telemetry.json` contiene solo conteggi di ordini per tipo). Corretto lo status da FULL/SUPPORTED a UNRESOLVED per quanto riguarda la sua verificabilità **con l'evidenza E15 disponibile**; non nego che la logica interna di Copilot tenti la ricostruzione, ma questa non è verificabile dall'esterno con gli artefatti attuali
```

```text
concept_id: movement_overhead / necessary_transit_fraction
feature_status: UNRESOLVED
e15_relationship: conditional — SUPPORTED in M3, NOT_DISCRIMINATED in M1/M2, nessuna spiegazione strutturale registrata per la discrepanza
current_initial_bound: non proponibile
parameter_or_hyperparameter: OBSERVABILITY_REQUIREMENT (richiede `necessary_transit_fraction`, mai popolata in nessun match)
next_training_values: nessuno finché la metrica di transito necessario non è calcolata
confounders: senza `necessary_transit_fraction`, MOVE assoluto o percentuale non distingue movimento sprecato da movimento necessario alla logistica di un working set più grande
validation_requirement: calcolare `necessary_transit_fraction` su nuovi match, per Copilot e per gli avversari
falsification_condition: se, una volta introdotta la metrica, il movimento "in eccesso" risultasse comparabile in proporzione fra tutte le policy, l'ipotesi di un differenziale di efficienza di routing risulterebbe indebolita
change_from_e15_spec: ADDED
change_rationale: lo SPEC-DECL assorbe questo concetto interamente dentro `throughput_to_cash_conversion` ("Movement is captured in throughput-to-cash efficiency"); l'evidenza E15 mostra verdetti incoerenti fra match che giustificano di scorporarlo come concetto monitorato a sé, non solo implicito
```

---

## C. Feature interaction map

```text
interaction_id: INT-01
features: state_capacity_alignment × pasture_arable_surface_tradeoff × livestock_headcount
reason: il working set (crop attivi) compete fisicamente con pasture; l'herd size deve restare subordinato allo spazio arabile residuo e non viceversa
current_evidence: SUPPORTED in 3/3 match (18 pasture/8-9 crop nel perdente ripetuto vs 5 pasture/25-28 crop nel vincitore ripetuto)
confounding_risk: Alto — pasture e livestock_headcount sono quasi collineari nei dati osservati; l'interazione a tre vie non è mai stata scomposta
training_implication: qualunque test futuro su herd size intermedio (7/10/13) deve tenere fissa la superficie pasture o farla variare indipendentemente, altrimenti l'interazione resta non isolabile
```

```text
interaction_id: INT-02
features: working_set_capacity_gate × deployable_capital_window
reason: il gate di espansione (rank 2) e la finestra di capitale deployabile (rank 7) condividono lo stesso meccanismo sottostante: espandere solo quando lo stato lo consente
current_evidence: SUPPORTED qualitativamente; Copilot ha investito con cash molto basso (M2 Day 4-9: $225-$461) e comunque vinto, suggerendo che la finestra dipende più dal *timing* che dal *livello assoluto* di cash
confounding_risk: Medio — nessun match separa esplicitamente "gate su crop/pasture readiness" da "gate su cash readiness"; potrebbero essere lo stesso meccanismo osservato da due angolazioni
training_implication: un test futuro dovrebbe variare separatamente la soglia di cash-readiness e quella di crop/pasture-readiness per verificare se sono davvero due gate distinti o uno solo
```

```text
interaction_id: INT-03
features: wheat_feed_security (market-flow component) × operating_cash_buffer
reason: un uso intenso del mercato Wheat per il feed potrebbe drenare cash, riducendo il buffer disponibile per l'espansione
current_evidence: CONFOUNDED — Copilot usa intensamente il mercato Wheat in M2/M3 e opera comunque con cash molto basso in alcune fasi senza che ciò impedisca la vittoria; non è chiaro se il flusso Wheat sia un dreno netto o una fonte di liquidità (il flusso include sia BUY sia SELL Wheat)
confounding_risk: Alto — manca il ledger eseguito per calcolare il saldo netto Wheat per Copilot in nessuno dei match
training_implication: priorità assoluta all'osservabilità (Sezione D) prima di qualunque tuning su questa interazione
```

```text
interaction_id: INT-04
features: crop_activation_and_monetization × workforce_headcount × action_dispatch_failure
reason: un working set esteso richiede workforce sufficiente E dispatch efficiente; se manca il secondo, più workforce non aiuta (osservato nell'avversario, non ancora in Copilot)
current_evidence: SUPPORTED per l'avversario Antigravity (12 hands, dispatch inefficiente, working set collassato); UNRESOLVED per Copilot (mai osservata una firma di dispatch fallimentare, ma anche mai stressato con working set molto più grande dell'attuale)
confounding_risk: Medio — l'assenza del fallimento in Copilot potrebbe riflettere un dispatch realmente più efficiente oppure semplicemente un working set mai abbastanza esteso da rivelare il problema
training_implication: un test che estenda il working set Copilot oltre l'attuale (28 crop) permetterebbe di verificare se il dispatch regge a scala maggiore o se la firma di fallimento emerge anche qui
```

---

## D. Observability requirements

| Requisito | Stato in E15 | Verdetto |
|---|---|---|
| Requested vs executed **actions** (WATER, HARVEST, PLANT, MOVE, ecc.) | Conteggi per tipo azione sono **direttamente osservabili** in `telemetry.json` (`action_counts`), già sufficienti per l'analisi comportamentale svolta | **Sufficientemente osservabile** — non dichiaro mancante ciò che già uso nella Sezione B |
| Requested vs executed **market transactions** | `telemetry.json` (`market_orders`) riporta solo conteggi di ordini per tipo (HIRE, BUY_LAND, BUY_SEED, BUY_ANIMAL, BUY_PRODUCT, SELL); nessun campo di quantità/prezzo eseguito | **Non sufficientemente osservabile** |
| Quantità e prezzo realizzati | Assenti in tutti e tre i dossier match (`summary.json`, `telemetry.json`, `raw_replay.json` non ispezionato in dettaglio ma i forensic report derivati non riportano alcun prezzo eseguito) | **Non sufficientemente osservabile** |
| Action success/failure reason | Nessun flag per singola azione; solo proxy aggregate (es. rapporto HARVEST/PLANT) | **Non sufficientemente osservabile** |
| Daily maintained/serviced surface | Riportato solo il **massimo** per episodio (es. "max active crops: 28"), non la serie giornaliera | **Parzialmente osservabile** — il massimo è noto, l'andamento giorno-per-giorno no |
| Cash-flow breakdown (per categoria) | `money_trajectory`/day-end snapshots sono osservabili come **aggregato totale**; nessuna scomposizione per categoria di ricavo/costo (crop vs livestock vs feed vs land) | **Parzialmente osservabile** |
| Movement necessario vs overhead | Solo conteggio MOVE assoluto e quota sul totale azioni; `necessary_transit_fraction` mai calcolata | **Non sufficientemente osservabile** |
| Purchase-to-activation/payback lag | Inferibile qualitativamente incrociando lo step di acquisto (es. Q1/Q2 day) con la traiettoria di cash nei giorni successivi (fatto nella Sezione B, Rank 4/7), ma non esiste una metrica continua dedicata | **Parzialmente osservabile** |

---

## E. Candidate training priorities

```text
priority: 1
concept_or_interaction: executed transaction ledger (market_transaction_value, INT-03)
information_gap: nessun prezzo/quantità eseguita in nessuno dei tre match
why_it_matters: blocca la verifica di quasi ogni claim di profittabilità (wheat_feed_security, inventory_liquidation, worker_action_monetization_rate forma netta)
candidate_values_or_measurement: instrumentare l'harness per loggare fill-quantity e prezzo per ogni ordine, senza modificare le policy
expected_information_gain: Alto — sblocca la risoluzione di ≥5 concetti oggi UNRESOLVED/CONFOUNDED
```

```text
priority: 2
concept_or_interaction: generalizzazione multi-seed (tutte le FEATURE con relationship non_monotonic/thresholded)
information_gap: ogni verdetto E15 deriva da N=1 seed per pairing
why_it_matters: senza replica, ogni "SUPPORTED" potrebbe essere specifico del seed/avversario testato, non un pattern strutturale della policy Copilot
candidate_values_or_measurement: rieseguire le tre submission frozen (invariate) su ≥3-5 seed nuovi, in entrambe le posizioni P0/P1
expected_information_gain: Alto — è la sola via per promuovere GENERALIZATION da NOT_ESTABLISHED
```

```text
priority: 3
concept_or_interaction: state_capacity_alignment (formula esplicita)
information_gap: il concetto più consistentemente SUPPORTED nei tre match non ha mai una formula operazionale dichiarata
why_it_matters: senza formula pre-registrata, rischia di restare un'etichetta post-hoc non falsificabile
candidate_values_or_measurement: pre-registrare crop_surface_maintained / activated_land_surface (o alternativa) e calcolarla PRIMA del risultato di un nuovo match
expected_information_gain: Medio-Alto — trasforma il concetto più centrale del proprio MODEL_SPEC da qualitativo a misurabile
```

```text
priority: 4
concept_or_interaction: action_dispatch_failure applicato a Copilot (INT-04)
information_gap: Copilot non ha mai mostrato la firma di fallimento, ma non è mai stato stressato con un working set più esteso dell'attuale (max 28)
why_it_matters: la robustezza del dispatch Copilot a scala maggiore è sconosciuta; è un rischio non testato prima di qualunque revisione che alzi i target di working set
candidate_values_or_measurement: monitorare il rapporto HARVEST/PLANT e MOVE-share per Copilot su nuovi seed, inclusi eventuali test con working set più esteso
expected_information_gain: Medio — riduce il rischio di un'estensione del working set che riveli problemi di dispatch non ancora osservati
```

```text
priority: 5
concept_or_interaction: wheat_feed_security — separazione internal buffering vs market-flow
information_gap: CONFOUNDED in 3/3 match; Copilot vince con intenso flusso di mercato ma la propria SPEC-DECL dichiara un polo "sicurezza interna"
why_it_matters: una revisione futura rischia di rafforzare erroneamente l'autarky come principio se non si separano i due meccanismi
candidate_values_or_measurement: dipende dalla priority 1 (ledger eseguito) per essere quantificato
expected_information_gain: Medio — condizionato al completamento della priority 1
```

```text
priority: 6
concept_or_interaction: species_margin_differential
information_gap: Copilot non ha mai schierato Sheep in E15; nessun confronto diretto disponibile
why_it_matters: `herd_target_sensitivity` (rank 9) resta a bassa confidence anche per questo motivo
candidate_values_or_measurement: nessuna submission frozen attuale lo permette; richiede una variante di policy dedicata, fuori scope per questo round
expected_information_gain: Basso nel breve termine (bloccato da vincoli di scope), Medio nel medio termine
```

---

## F. Changeset rispetto al MODEL_SPEC E15

| Concept | E15 status/hypothesis | Revised status | Change | Evidence basis | Remaining uncertainty |
|---|---|---|---|---|---|
| `monetized_productive_output` / `worker_action_monetization_rate` (rank 1) | SUPPORTED, Critical/Medium | FEATURE, positive (proxy macro) | REVISED | E15-EVIDENCE (M2 proxy $7.13 vs $5.17); SELF-CHECK (audit M2: NOT_DISCRIMINATED come meccanismo) | Forma netta mai calcolata; nessun ledger |
| `state_capacity_alignment` (rank 2) | SUPPORTED, Critical/Medium | FEATURE, conditional/interaction | REVISED | E15-EVIDENCE (SUPPORTED in 3/3 consensus); SELF-CHECK (audit M2: WEAKENED come meccanismo) | Nessuna formula pre-registrata |
| `crop_surface_maintained` / `watering_execution_rate` (rank 3) | SUPPORTED, Critical/Medium, bundled | FEATURE, scorporati (saturazione vs thresholded) | REVISED | E15-EVIDENCE (M1/M3 collasso a bassa watering; M2 28<37) | Buco di osservazione 35-438 WATER; saturazione oltre 28 crop da 1 sola osservazione |
| `land_surface_total` (componente di rank 4) | Implicitamente NOT_FEATURE nel capability check | FEATURE, non_monotonic | REVISED (correzione) | FRAME (relazione canonica `land_surface_total enables activated_land_surface`); INFERENCE (§A.5) | Copilot non ha mai testato un'espansione Q2 |
| `workforce_headcount` (rank 12 / componente) | Implicitamente NOT_FEATURE nel capability check | FEATURE, non_monotonic | REVISED (correzione) | INFERENCE (§A.5); regola epistemica esplicita di questo task | Mai isolato da dispatch quality |
| `livestock_headcount` (rank 5/9) | Implicitamente NOT_FEATURE nel capability check | FEATURE, non_monotonic | REVISED (correzione) | FRAME (README, esempio esplicito); E15-EVIDENCE (4-17 osservato) | Intervallo 4-17 non narrowed |
| `pasture_arable_surface_tradeoff` (rank 5) | SUPPORTED, High/Medium | FEATURE, negative | RETAINED (invariato) | E15-EVIDENCE (3/3 match coerenti) | Collinearità con livestock_headcount |
| `wheat_feed_security` (rank 6) | SUPPORTED, High/Medium | UNRESOLVED | REVISED (downgrade) | E15-EVIDENCE (CONFOUNDED in 3/3 match) | Manca ledger eseguito per costo netto |
| `cash_buffer_before_expansion` (rank 7) | WEAKLY_SUPPORTED, High/Medium | FEATURE (deployable_capital_window) / UNRESOLVED (buffer assoluto) | REVISED | E15-EVIDENCE (Copilot vince con cash molto basso in M2) | Direzione causale fra cash e conversione non isolata |
| `milestone_day_gating` (rank 8) | WEAKLY_SUPPORTED, deprecato pre-E15 | NOT_YET_TUNABLE, deprecato | UNCHANGED | E15-EVIDENCE (lock-in varia Day10-19, corrobora deprecazione) | Nessuna |
| `herd_target_sensitivity` (rank 9) | WEAKLY_SUPPORTED, Low | FEATURE (headcount) / UNRESOLVED (specie) | REVISED | E15-EVIDENCE; FRAME | Nessun test diretto Cow vs Sheep |
| `inventory_liquidation_and_shed_flush` (rank 10) | SUPPORTED, Medium/Medium | FEATURE (conversion) / UNRESOLVED (endgame timing causale) | REVISED (downgrade parziale) | E15-EVIDENCE (endgame CONFOUNDED/INCONCLUSIVE in 3/3 consensus) | Manca ledger; contributo endgame isolato non dimostrato |
| `field_cleanliness_priority` (rank 11) | CONTRADICTED, deprecato pre-E15 | NOT_FEATURE | UNCHANGED | E15-EVIDENCE (M1 inversione) | Nessuna |
| `fixed_hire_count` (rank 12, policy) | FALSIFIED, rimosso pre-E15 | NOT_YET_TUNABLE (policy) / FEATURE (concetto sottostante `workforce_headcount`) | UNCHANGED (policy) / ADDED (distinzione concetto) | INFERENCE (§A.5) | — |
| `action_dispatch_failure` | PARTIAL/implicito nello SPEC-DECL | UNRESOLVED, monitorare esplicitamente | ADDED | E15-EVIDENCE (discriminante primario per l'avversario) | Mai osservato in Copilot; INT-04 non testata |
| `market_transaction_value` | USED/FULL nello SPEC-DECL | UNRESOLVED | REVISED (downgrade) | E15-EVIDENCE (nessun ledger esposto in alcun match) | Verificabilità esterna assente |
| `movement_overhead` / `necessary_transit_fraction` | Assorbito implicitamente nello SPEC-DECL | UNRESOLVED, monitorare separatamente | ADDED | E15-EVIDENCE (verdetti incoerenti fra match) | Metrica mai calcolata |

---

## G. Epistemic audit

### RETAIN
- `pasture_arable_surface_tradeoff` (rank 5) — direzione e rank invariati, evidenza coerente in 3/3 match.
- `crop_activation_and_monetization` come principio generale (rank 3) — pur scorporato internamente in due sotto-concetti, il principio "attivazione + monetizzazione conta più della superficie nominale" resta pienamente supportato.
- `milestone_day_gating` come deprecazione (rank 8) — corroborata, non richiede ulteriore azione.
- `field_cleanliness_priority` come deprecazione (rank 11) — corroborata.
- `fixed_hire_count` come policy rimossa (rank 12) — corroborata.

### REVISE
- `throughput_to_cash_conversion` (rank 1) — richiede la forma "netta" mai calcolata prima di ulteriore promozione di confidence.
- `working_set_capacity_gate`/`state_capacity_alignment` (rank 2) — richiede formula pre-registrata.
- `land_unlock_condition` (rank 4) — ripristinare `land_surface_total` come FEATURE; nessuna osservazione diretta Copilot di un'espansione riuscita.
- `wheat_feed_security` (rank 6) — separare internal buffering da market-flow management.
- `cash_buffer_before_expansion` (rank 7) — trattare come vincolo dinamico, non soglia fissa.
- `herd_target_sensitivity` (rank 9) — headcount promosso a FEATURE esplicito; specie resta separata come UNRESOLVED.
- `inventory_liquidation_and_shed_flush` (rank 10) — scorporare la componente endgame-timing (UNRESOLVED) dalla componente conversion (FEATURE).

### DEPRIORITIZE_OR_REMOVE
- Nessun nuovo elemento in questa categoria oltre a quanto già deprioritizzato pre-E15 (`field_cleanliness_priority`, `fixed_hire_count`, `fixed_q2_priority`). `productive_action_share` (concetto ontologico più ampio, non nel ranking Copilot) resta deprioritizzato come metrica aggregata, per la ragione esposta in §A.5.

### UNRESOLVED
- `market_transaction_value`
- `action_dispatch_failure` (per Copilot specificamente)
- `movement_overhead` / `necessary_transit_fraction`
- `species_margin_differential`
- `market_churn_cost` (mai quantificato, non affrontato in un blocco dedicato perché assente dal ranking Copilot e senza osservabilità)

### DO_NOT_FREEZE_YET
- Qualunque valore numerico in `next_training_values` in Sezione B (herd 4/7/10/13, pasture 5/7/9, watering 100/200/300, working set 20/25/30/35): sono candidati per il prossimo round comune, non soglie.
- La formula di `state_capacity_alignment`: deve essere pre-registrata e concordata prima di essere usata per valutare un match, non dedotta a posteriori.
- Qualunque soglia di `operating_cash_buffer` o `deployable_capital_window`: la direzione (timing conta più del livello assoluto) è ragionevole ma non quantificata.

---

**Chiusura:** baseline reconstruction, concept-by-concept revision, feature interaction map, observability requirements, candidate training priorities, changeset ed epistemic audit sono completati. Non è stata proposta alcuna E16 definitiva, alcun arbitraggio cross-model, alcuna policy o codice. Questo documento è stato salvato come unico artefatto in `docs/model/model_specs/copilot/COPILOT_MODEL_SPEC_REVISION.md`; nessun altro file è stato modificato.
