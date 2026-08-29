# E16 — TRAINING DESIGN PROPOSAL (Independent)
## MODELER_ID = COPILOT

**Stato:** proposta indipendente, non frozen, pronta per cross-review. Non sostituisce [POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md](../../model_specs/post_e15/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md). Nessun file del repository è stato modificato. Nessuna policy è stata implementata. Nessuna submission è stata generata. E16 non è qui dichiarato frozen.

**Indipendenza:** al momento della scrittura, [docs/experiment_designs/](.) non esisteva ancora nel repository — non ho letto né confrontato proposte E16 di altri modeler. Ho letto integralmente [README.md](../../../README.md) e [POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md](../../model_specs/post_e15/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md) (versione FINAL, non la candidate). Ho usato la mia [capability check](../../../results/post_e15/capability_check/COPILOT_CAPABILITY_CHECK.md) e la mia [MODEL_SPEC revision](../../model_specs/post_e15/COPILOT_MODEL_SPEC_REVISION.md) esclusivamente come supporto secondario. Non ho riaperto l'arbitraggio consolidato: la versione FINAL ha già corretto (rispetto alla candidate) sia la notazione `Q2` ambigua sia il claim di convergenza esterna, sostituendole con `quadrants_owned = <int>` e con "external support MIXED" — nessun errore fattuale residuo che invaliderebbe questo design è stato identificato.

`quadrants_owned = 2` è qui trattato **esclusivamente** come baseline controllata, non come optimum. `final_money` non è mai usato come input di una metrica composita.

---

## A. DESIGN SUMMARY

```text
design_id: E16_COPILOT_PROPOSAL
training_goal: Localizzare la regione di transizione fra regime operativo insufficiente e regime competitivo per (1) crop working set × irrigation service e (2) herd size × pasture allocation × crop opportunity cost, sotto una baseline controllata quadrants_owned=2, senza stimare un optimum.
design_type: due blocchi (E16-A, E16-B), ciascuno un design fattoriale sparso (non full-factorial), E16-B staged su un risultato di E16-A
total_cells: 14 (PREFERRED) / 10 (MINIMAL) — vedi Sezione J
seeds_per_cell: 3 (PREFERRED) / 2 (MINIMAL)
total_episodes: 42 (PREFERRED) / 20 (MINIMAL)
staged: YES
```

---

## B. HYPOTHESES

```text
hypothesis_id: H1
concepts: crop_surface_maintained, watering_execution_rate, action_dispatch_failure
relationship: thresholded — sotto una soglia di service coverage (watering eseguito / watering necessario) la crop_surface_maintained realizzata collassa rispetto al target; sopra soglia, converge al target
current_evidence: E15 osserva solo gli estremi — 8-9 crop attivi con WATER 30-34 (failure, 2 repliche indipendenti M1/M3) vs 25-37 crop attivi con WATER 439-475 (competitive, 3 osservazioni M1/M2/M3); l'intervallo 10-24 crop / 35-438 WATER non è mai stato campionato
uncertainty_to_resolve: se, tenendo fissa una policy di watering ad alta priorità, esiste una taglia di working set oltre la quale la capacità di servizio non tiene il passo (interazione superficie×capacità), oppure se la realized crop_surface_maintained segue linearmente il target fino a 30 senza discontinuità sotto priorità alta
falsification_condition: se realized_crop_surface_maintained ≈ target_crop_working_set_size (entro una tolleranza pre-dichiarata, es. ±10%) per TUTTI i livelli 9-30 sotto watering_dispatch_priority=HIGH, l'ipotesi di una regione di transizione capacità-limitata in questo intervallo è falsificata: il collasso E15 sarebbe allora attribuibile a priorità di dispatch, non a taglia del working set
```

```text
hypothesis_id: H2
concepts: watering_dispatch_priority, watering_execution_rate, action_dispatch_failure
relationship: conditional — il fallimento a basso servizio osservato in E15 (Antigravity, M1/M3) dipende dalla priorità di dispatch assegnata al watering, non dalla sola taglia del working set
current_evidence: E15 non isola priorità da taglia: nei match osservati bassa priorità/bassa taglia realizzata (Antigravity) e alta priorità/alta taglia (Codex, Copilot) sono sempre co-occorse
uncertainty_to_resolve: se una taglia piccola (9) con priorità bassa replica comunque il pattern di fallimento (confermando che la priorità conta indipendentemente dalla taglia) e se una taglia grande (30) con priorità bassa fallisce anch'essa (mostrando che la sola taglia grande non compensa una cattiva priorità)
falsification_condition: se (WS=9, priorità=LOW) NON produce un profilo simile al fallimento Antigravity osservato in E15 (watering_execution_rate e crop_surface_maintained comparabili al regime competitivo), l'ipotesi che la priorità di dispatch sia il meccanismo determinante è falsificata a favore di una spiegazione alternativa (es. bug di routing specifico della submission Antigravity, non riproducibile variando solo la priorità)
```

```text
hypothesis_id: H3
concepts: livestock_headcount, pasture_arable_surface_tradeoff, pasture_surface_maintained
relationship: conditional / interaction — il fallimento osservato a herd grande (17-18) dipende dal costo opportunità di un pasture footprint sovradimensionato rispetto alla superficie arabile, non dalla sola numerosità del herd
current_evidence: E15 osserva herd 4-7 (competitive) sempre abbinato a pasture piccola (5-9) e herd 17-18 (failure) sempre abbinato a pasture grande (18); le due dimensioni sono perfettamente collineari nei dati osservati, mai scorporate
uncertainty_to_resolve: se un herd grande (18) con pasture allocata in modo efficiente (proporzionata al herd, non sovradimensionata) evita il collasso della crop_surface_maintained osservato in E15, e se un herd piccolo (4) con pasture sovradimensionata (fissa a 18 tile indipendentemente dal herd) produce comunque un danno da opportunity cost
falsification_condition: se (herd=18, pasture=TIGHT) produce un profilo di final_money e crop_surface_maintained comparabile a (herd=18, pasture=LOOSE) — cioè il danno persiste anche con pasture efficiente — l'ipotesi dell'opportunity cost pasture-driven è falsificata a favore di un meccanismo herd-size-driven indipendente (es. carico di CARE/FEED assoluto)
```

Nota esplicita: l'interazione a tre vie fra taglia del crop working set (E16-A) e taglia del herd (E16-B) **non è testata in questo round** — E16-B fissa il crop working set come controllo (vedi Sezione E). Questo è un limite dichiarato, non un'omissione.

---

## C. FACTORS AND CONTROLS

| variable | role | type | candidate_values_or_control | rationale |
|---|---|---|---|---|
| `target_crop_working_set_size` | MANIPULATED | PARAMETER | E16-A: {9, 14, 19, 24, 30} (WP=HIGH); {9, 30} (WP=LOW) | Ancora ai due estremi osservati E15 + 3 punti interni nel gap 10-24 mai campionato |
| `watering_dispatch_priority` | MANIPULATED | PARAMETER | {LOW, HIGH} | Isola l'effetto della priorità di dispatch dalla taglia del working set (H2) |
| `target_herd_size` | MANIPULATED | PARAMETER | E16-B: {4, 10, 13, 16, 18} (pasture=TIGHT); {4, 18} (pasture=LOOSE) | Ancora ai due estremi osservati E15 + 3 punti interni nel gap 8-16 mai campionato |
| `pasture_allocation_policy` | MANIPULATED | HYPERPARAMETER | {TIGHT, LOOSE} | TIGHT = pasture scalata al herd corrente; LOOSE = pasture fissa a ~18 tile indipendentemente dal herd (isola l'opportunity cost, H3) |
| `quadrants_owned` | CONTROL | PARAMETER | fisso = 2 per l'intera durata dell'episodio, nessun acquisto di terreno | Baseline controllata dichiarata dal consolidato; escluderla non compromette l'identificabilità di H1-H3 poiché tutte le taglie testate (fino a 30 crop attivi) sono state osservate raggiungibili entro quadrants_owned=2 in E15 (Copilot, fino a 28) |
| `workforce_headcount` | CONTROL | PARAMETER | fisso = 10 hands in tutte le celle | Coincide con il livello usato da 2/3 configurazioni vincenti E15 (Codex M1, M2); evita sia lo starvation artificiale sia la firma di scala (12) associata al fallimento Antigravity; workforce non è un fattore di questo round (§6 del prompt) |
| `opponent_policy` | CONTROL | — | fisso = submission Codex E15 frozen, invariata, stesso ruolo in tutte le celle | Record 1-1 in E15: riferimento "medio", non ancoraggio all'estremo vincitore né perdente |
| `crop_type_selection` | CONTROL | — | fisso = singola rotazione semplice identica in tutte le celle | Evita che crop_revenue_mix diventi un confounder non controllato di H1 |
| `land_acquisition_timing` | CONTROL | — | nessun acquisto durante l'episodio (coerente con quadrants_owned=2 fisso) | Elimina land_purchase_timing come dimensione libera |
| `cash_reserve_policy` | CONTROL | — | soglia di riserva minima identica in tutte le celle | operating_cash_buffer resta diagnostica, non manipolata |
| `endgame_policy` | CONTROL | — | regola di stop-pianta/liquidazione identica in tutte le celle | endgame_shutdown_timing/endgame_inventory_liquidation restano diagnostici, non manipolati |
| `routing_logic` | CONTROL | — | logica di movimento/dispatch identica in tutte le celle salvo i fattori manipolati | movement_overhead/necessary_transit_fraction restano diagnostici |
| `species_composition` | CONTROL | — | fisso = una sola specie (Cow) in tutte le celle E16-B | species_margin_differential resta UNRESOLVED e non è testato in questo round |
| `seed_set` | CONTROL | — | 3 (o 2) seed condivisi, identici in ogni cella, mai riusati da E15 | Isola l'effetto trattamento dalla varianza seed (§F) |
| `realized_crop_surface_maintained` | DERIVED_METRIC | — | osservato, non impostato | Outcome di H1: può divergere dal target se il servizio non tiene il passo |
| `watering_execution_rate` | DERIVED_METRIC | — | osservato | Outcome, distinto dal parametro `watering_dispatch_priority` |
| `service_coverage_ratio` | DERIVED_METRIC | — | = watering eseguito / watering necessario (per giorno, poi aggregato) | Metrica centrale per H1; introdotta perché E15 non la calcolava mai |
| `pasture_arable_surface_tradeoff_realized` | DERIVED_METRIC | — | osservato | Outcome di H3 |
| `worker_capacity_utilization` | DERIVED_METRIC | — | osservato | Verifica che workforce fisso a 10 non sia esso stesso il collo di bottiglia |
| `action_dispatch_failure_rate` | OBSERVABILITY | — | richiede success/failure flag per azione | Sostituisce la sola proxy HARVEST/PLANT con una misura diretta |
| `market_transaction_value` / `realized_price` / `realized_value` | OBSERVABILITY | — | richiede event ledger eseguito | Necessario per non confondere ordini richiesti con transazioni eseguite |
| `unsold_inventory_quantity` / `unsold_inventory_value_estimate` | OBSERVABILITY | — | richiede tracciamento terminale per prodotto | `_value_estimate` esplicitamente non equivalente a `realized_value` |

---

## D. EXPERIMENT CELLS

### Blocco E16-A — Irrigation × crop working set (controllo: workforce=10, opponent=Codex frozen, quadrants_owned=2)

```text
cell_id: A1
factor_values: target_crop_working_set_size=9, watering_dispatch_priority=HIGH
comparison_role: anchor — replica il regime failure-size E15 ma sotto buona disciplina di watering
epistemic_question: una taglia piccola con priorità alta produce un profilo diverso dal fallimento Antigravity (34 WATER/8 crop)?
why_required: senza questa cella non sappiamo se la taglia 9 è intrinsecamente un problema o solo un sintomo della bassa priorità osservata in E15
```

```text
cell_id: A2
factor_values: target_crop_working_set_size=14, watering_dispatch_priority=HIGH
comparison_role: interno-1, primo punto nel gap 10-24
epistemic_question: il servizio regge già a 14 sotto priorità alta?
why_required: localizza il bordo inferiore della regione di transizione, mai osservata da E15
```

```text
cell_id: A3
factor_values: target_crop_working_set_size=19, watering_dispatch_priority=HIGH
comparison_role: interno-2, punto centrale del gap
epistemic_question: il servizio regge a metà del gap non osservato?
why_required: senza un punto centrale, un'eventuale transizione non lineare fra 14 e 24 non sarebbe distinguibile da una retta
```

```text
cell_id: A4
factor_values: target_crop_working_set_size=24, watering_dispatch_priority=HIGH
comparison_role: interno-3, prossimo al confine superiore del gap
epistemic_question: il servizio regge appena sotto la regione competitiva nota (25-37)?
why_required: localizza il bordo superiore della regione di transizione prima dell'ancora competitiva
```

```text
cell_id: A5
factor_values: target_crop_working_set_size=30, watering_dispatch_priority=HIGH
comparison_role: anchor — replica il regime competitivo E15 sotto priorità alta
epistemic_question: la taglia 30 con priorità alta replica il pattern competitivo osservato (Copilot/Codex M1/M2/M3)?
why_required: senza questa cella non abbiamo un'ancora competitiva sotto il protocollo E16 (nuovi seed, nuovo opponent) con cui confrontare A1-A4
```

```text
cell_id: A6
factor_values: target_crop_working_set_size=9, watering_dispatch_priority=LOW
comparison_role: contrasto diretto con A1 — isola l'effetto della priorità a parità di taglia piccola
epistemic_question: la bassa priorità, non la taglia, è ciò che genera il pattern di fallimento?
why_required: è la cella che testa H2 direttamente; senza di essa non possiamo distinguere "la taglia 9 fallisce" da "la priorità bassa fallisce"
```

```text
cell_id: A7
factor_values: target_crop_working_set_size=30, watering_dispatch_priority=LOW
comparison_role: contrasto diretto con A5 — verifica se una taglia grande fallisce comunque con priorità bassa
epistemic_question: una taglia grande "salva" un servizio con priorità bassa, o fallisce comunque?
why_required: senza questa cella non sapremmo se il vantaggio dei vincitori E15 dipendeva dalla priorità di watering piuttosto che da qualunque altra caratteristica correlata alla taglia
```

### Blocco E16-B — Livestock × pasture × crop opportunity cost (controllo: workforce=10, opponent=Codex frozen, quadrants_owned=2, crop working set = valore derivato da E16-A, vedi Sezione E)

```text
cell_id: B1
factor_values: target_herd_size=4, pasture_allocation_policy=TIGHT
comparison_role: anchor — replica il regime competitivo E15 con allocazione efficiente
epistemic_question: herd piccolo con pasture proporzionata replica il pattern competitivo?
why_required: ancora competitiva sotto il protocollo E16
```

```text
cell_id: B2
factor_values: target_herd_size=10, pasture_allocation_policy=TIGHT
comparison_role: interno-1, primo punto nel gap 8-16
epistemic_question: un herd moderato con pasture efficiente resta competitivo?
why_required: localizza il bordo inferiore della regione di transizione herd, mai osservata da E15
```

```text
cell_id: B3
factor_values: target_herd_size=13, pasture_allocation_policy=TIGHT
comparison_role: interno-2, punto centrale del gap
epistemic_question: il punto centrale del gap mostra degrado graduale o soglia netta?
why_required: distingue una transizione graduale da una soglia netta fra 10 e 16
```

```text
cell_id: B4
factor_values: target_herd_size=16, pasture_allocation_policy=TIGHT
comparison_role: interno-3, prossimo al confine del bundle failure noto (17-18)
epistemic_question: appena sotto la regione di fallimento nota, l'allocazione efficiente basta a evitare il collasso?
why_required: localizza il bordo superiore della regione di transizione prima dell'ancora di fallimento
```

```text
cell_id: B5
factor_values: target_herd_size=18, pasture_allocation_policy=TIGHT
comparison_role: test diretto di H3 — stessa taglia del fallimento Antigravity, ma pasture efficiente
epistemic_question: un herd di taglia 18 fallisce anche con pasture allocata in modo efficiente?
why_required: è la cella cruciale per H3; senza di essa non possiamo separare "herd grande" da "pasture sovradimensionata" come causa del fallimento E15
```

```text
cell_id: B6
factor_values: target_herd_size=4, pasture_allocation_policy=LOOSE
comparison_role: contrasto con B1 — isola l'effetto della pasture sovradimensionata a parità di herd piccolo
epistemic_question: una pasture sovradimensionata danneggia le prestazioni anche con un herd piccolo che non la richiede?
why_required: testa se il solo costo opportunità della pasture (indipendente dal herd) è dannoso, componente necessaria di H3
```

```text
cell_id: B7
factor_values: target_herd_size=18, pasture_allocation_policy=LOOSE
comparison_role: anchor — replica il bundle di fallimento Antigravity (herd grande + pasture grande)
epistemic_question: la combinazione osservata in E15 (herd 17-18 + pasture 18) replica il fallimento sotto il protocollo E16?
why_required: ancora di fallimento sotto il protocollo E16, necessaria come riferimento per B1-B6
```

---

## E. STAGE / ADVANCEMENT RULES

```text
stage: 1
scope: Blocco E16-A (celle A1-A7)
advancement_rule: >
  Al termine di E16-A, calcolare per ciascun livello di target_crop_working_set_size
  in {9,14,19,24,30} sotto watering_dispatch_priority=HIGH la media, sui seed disponibili,
  di final_money e di service_coverage_ratio.
  Selezionare come crop_surface_control_for_E16B il PIÙ PICCOLO livello che soddisfa
  ENTRAMBE le condizioni:
    (i) service_coverage_ratio medio >= 0.85;
    (ii) final_money medio non inferiore di oltre il 10% al final_money medio massimo
         osservato fra tutte le celle A1-A5.
  Se nessun livello soddisfa entrambe le condizioni simultaneamente, selezionare il
  livello con final_money medio massimo fra quelli con service_coverage_ratio medio >= 0.75
  e dichiarare esplicitamente questa deviazione nel report E16-B come fallback pre-dichiarato.
  Le soglie 0.85 / 0.75 / 10% sono parametri procedurali della regola di selezione,
  non affermazioni empiriche su optimum di gioco.
verifiability: la regola è puramente aritmetica sui dati raccolti; non richiede giudizio soggettivo post-hoc
```

Non viene usata alcuna formulazione tipo "scegliere il migliore e provare altro": la regola sopra è l'unico meccanismo ammesso per fissare il controllo di E16-B.

---

## F. SEED / OPPONENT PROTOCOL

```text
seed_count_preferred: 3 seed condivisi
seed_count_minimal: 2 seed condivisi
seed_sharing: gli stessi seed sono usati IDENTICI in ogni cella di E16-A e di E16-B (nessun seed diverso per cella)
seed_provenance: i seed devono essere selezionati e documentati PRIMA dell'esecuzione di qualunque cella; devono essere seed NUOVI, esplicitamente diversi dai tre seed E15 (1113294977, 3033283457, 3122977751), per non riutilizzare TRAINING evidence E15 come se fosse nuova osservazione
opponent: submission Codex E15 frozen (`submission_codex_E15_FROZEN.py`), invariata, identica in tutte le celle e tutti i seed — nessuna rotazione di opponent in questo round
opponent_rationale: record E15 1-1, posizione "mediana" fra il vincitore (Copilot) e il perdente ripetuto (Antigravity); evita di ancorare il confronto a un estremo
position_protocol: per ogni cella, alternare la posizione della variante testata (P0/P1) fra i seed disponibili (es. con 3 seed: P0, P1, P0), a costo zero aggiuntivo, per raccogliere una corroborazione incidentale del P0_P1_ENVIRONMENT_AUDIT esistente; questo non è l'obiettivo primario del round e non deve essere sovra-interpretato con questo solo campione
execution_order: le celle non devono essere eseguite in un ordine che introduca drift sistematico (es. non eseguire tutte le celle "attese vincenti" per prime); ordine raccomandato: randomizzare l'ordine delle celle una sola volta prima dell'esecuzione e congelare quell'ordine, documentandolo
treatment_vs_variance: poiché seed e opponent sono condivisi/fissi fra celle, ogni differenza sistematica fra celle (calcolata seed-per-seed, non solo in media — vedi Sezione H) è attribuibile al fattore manipolato; la varianza residua fra i seed di una stessa cella stima il rumore di seed
no_post_hoc_seed_selection: nessun seed può essere sostituito, escluso o aggiunto dopo aver osservato risultati parziali
```

---

## G. TELEMETRY REQUIREMENTS

Campi minimi obbligatori (ereditati dal consolidato finale, invariati):

```text
episode, player, step, actor_or_order, requested_payload, executed_payload,
success, failure_reason, executed_quantity, realized_price, realized_value,
cash_flow_category, state_before, state_after, provenance, quadrants_owned,
daily_serviced_crop_surface, watering_need_denominator, watering_execution_success_failure,
pasture_occupancy, feed_demand_coverage, necessary_vs_avoidable_transit,
purchase_to_activation_lag, terminal_inventory_by_product,
unsold_inventory_quantity, unsold_inventory_value_estimate (con metodo e provenance)
```

Campi aggiuntivi richiesti da questo design, per renderlo falsificabile:

```text
target_crop_working_set_size          # etichetta di trattamento per episodio/cella
watering_dispatch_priority_level      # LOW | HIGH, etichetta di trattamento
target_herd_size                      # etichetta di trattamento per episodio/cella
pasture_allocation_policy             # TIGHT | LOOSE, etichetta di trattamento
realized_pasture_footprint_tiles      # verifica che TIGHT/LOOSE sia stato implementato come da design
service_coverage_ratio                # derived: watering eseguito / watering necessario, per giorno e aggregato episodio
disqualification_flag                 # bool
disqualification_reason               # stringa, se applicabile
```

`unsold_inventory_value_estimate` non è mai trattato come `realized_value` in nessuna analisi.

---

## H. ANALYSIS PLAN

**Confronti primari:**
- E16-A: andamento di `final_money`, `realized_crop_surface_maintained` e `service_coverage_ratio` lungo {9,14,19,24,30} sotto `watering_dispatch_priority=HIGH` (localizzazione H1).
- E16-A: confronto appaiato A1↔A6 e A5↔A7 (stessa taglia, priorità diversa) per isolare l'effetto priorità (H2).
- E16-B: andamento delle stesse metriche lungo {4,10,13,16,18} sotto `pasture_allocation_policy=TIGHT` (localizzazione H3).
- E16-B: confronto appaiato B1↔B6 e B5↔B7 (stesso herd, allocazione pasture diversa) per isolare l'effetto opportunity cost (H3).

**Confronti secondari:**
- Consistenza fra i seed condivisi entro ciascuna cella (vedi regola sotto).
- Sub-confronto P0 vs P1 entro l'alternanza di posizione, solo come corroborazione incidentale.
- Correlazione fra la proxy HARVEST/PLANT (usata in E15) e `action_dispatch_failure_rate` misurato direttamente in E16, per validare se la proxy resta utile in assenza di ledger completo nei round futuri.

**Come interpretare le interazioni:** un effetto del fattore manipolato è dichiarato solo se la direzione è coerente in almeno 2 dei 3 (o 2 dei 2, per MINIMAL) seed condivisi entro la cella; una media calcolata solo cross-seed senza verifica di coerenza direzionale non è sufficiente per dichiarare un effetto.

**Gestione failure/disqualification:** un episodio disqualificato non viene scartato silenziosamente né imputato con un valore sostitutivo; viene riportato come outcome della cella (un tasso di disqualification a una certa taglia/herd è esso stesso un dato rilevante su una failure region). Il confronto quantitativo di `final_money` fra celle esclude gli episodi disqualificati dal calcolo della media ma li riporta separatamente.

**Trattamento degli outlier:** dato il numero ridotto di seed per cella (2-3), non si applica alcuna esclusione statistica di outlier. Un seed che diverge nettamente dagli altri entro la stessa cella deve essere riportato esplicitamente e segnalato come candidato per approfondimento futuro, non escluso.

**Conclusioni consentite:**
- Affermazioni sulla presenza/assenza di una regione di transizione osservabile nelle condizioni controllate testate (workforce=10, opponent=Codex frozen, questi seed).
- Restringimento (non eliminazione) delle regioni non osservate 10-24 e 8-16.
- Attribuzione relativa fra priorità-di-dispatch e taglia-del-working-set come spiegazione del pattern di fallimento E15 (H2).
- Attribuzione relativa fra taglia-del-herd e allocazione-pasture come spiegazione del pattern di fallimento E15 (H3).

**Conclusioni vietate:**
- Dichiarare un valore ottimale per qualunque fattore manipolato.
- Generalizzare oltre le condizioni controllate (workforce=10, opponent unico, questi seed) senza un round di VALIDATION dedicato.
- Trattare E16 come VALIDATION o TEST della revisione MODEL_SPEC.
- Dedurre conclusioni sull'interazione a tre vie crop-working-set × herd-size, non testata in questo round.
- Interpretare conteggi di ordini richiesti come transazioni eseguite anche in presenza del nuovo ledger, salvo che `success`/`executed_payload` lo confermi esplicitamente.
- Usare `state_capacity_alignment` come metrica di valutazione formale in questo round: resta `NOT_YET_TUNABLE` fino a formalizzazione indipendente da `final_money`.

---

## I. INFORMATION-GAIN AUDIT

```text
cell_id: A1
information_gained: stabilisce se taglia=9 con priorità alta evita il pattern di fallimento osservato in E15
what_is_lost_if_removed: nessuna ancora di riferimento a bassa taglia sotto buona disciplina; H1 e H2 non sarebbero verificabili all'estremo inferiore
```

```text
cell_id: A2
information_gained: primo punto di localizzazione nel gap 10-24
what_is_lost_if_removed: il bordo inferiore della regione di transizione resterebbe non localizzato
```

```text
cell_id: A3
information_gained: punto centrale, distingue transizione graduale da soglia netta
what_is_lost_if_removed: un salto non lineare fra 14 e 24 non sarebbe distinguibile da un andamento lineare
```

```text
cell_id: A4
information_gained: localizza il bordo superiore della regione di transizione
what_is_lost_if_removed: nessuna evidenza su quanto vicino al regime competitivo (25-37) la transizione si chiuda
```

```text
cell_id: A5
information_gained: ancora competitiva sotto protocollo E16 (nuovi seed/opponent)
what_is_lost_if_removed: nessun riferimento competitivo comparabile per A1-A4 e A7
```

```text
cell_id: A6
information_gained: isola l'effetto della priorità di dispatch a parità di taglia (test diretto H2)
what_is_lost_if_removed: non sapremmo se la taglia o la priorità genera il pattern di fallimento E15
```

```text
cell_id: A7
information_gained: verifica se una taglia grande fallisce comunque con priorità bassa (secondo test H2)
what_is_lost_if_removed: un'eventuale asimmetria (taglia grande "protegge" da priorità bassa) resterebbe invisibile
```

```text
cell_id: B1
information_gained: ancora competitiva per il blocco herd/pasture
what_is_lost_if_removed: nessun riferimento competitivo per B2-B7
```

```text
cell_id: B2
information_gained: primo punto di localizzazione nel gap 8-16
what_is_lost_if_removed: bordo inferiore della regione di transizione herd non localizzato
```

```text
cell_id: B3
information_gained: punto centrale, distingue degrado graduale da soglia netta
what_is_lost_if_removed: un salto non lineare fra 10 e 16 non sarebbe distinguibile da un andamento lineare
```

```text
cell_id: B4
information_gained: localizza il bordo superiore, appena sotto il bundle di fallimento noto
what_is_lost_if_removed: nessuna evidenza su quanto vicino a 17-18 il collasso inizi
```

```text
cell_id: B5
information_gained: test diretto e cruciale di H3 (herd=18 con pasture efficiente)
what_is_lost_if_removed: H3 non sarebbe verificabile alla taglia esatta del fallimento E15 osservato
```

```text
cell_id: B6
information_gained: isola il costo opportunità della pasture a parità di herd piccolo (componente di H3)
what_is_lost_if_removed: non sapremmo se una pasture sovradimensionata è dannosa indipendentemente dal herd
```

```text
cell_id: B7
information_gained: ancora di fallimento sotto protocollo E16, replica il bundle Antigravity
what_is_lost_if_removed: nessun riferimento di fallimento comparabile per B1-B6
```

**Celle considerate e rimosse durante il design:** un disegno full-factorial 5×2 per E16-A (10 celle) e per E16-B (10 celle) è stato scartato. Sono state rimosse le celle interne sotto priorità bassa/pasture loose (es. WS=14/19/24 con priorità LOW; herd=10/13/16 con pasture LOOSE), perché il ramo "bassa disciplina"/"allocazione inefficiente" richiede solo ancore di replica alle due estremità (già note da E15) e non una localizzazione fine, che è invece necessaria solo nel ramo ad alta disciplina/allocazione efficiente per rispondere a H1/H3. Questo dimezza il costo (14 celle invece di 20) senza perdere le distinzioni epistemiche richieste da H1-H3.

---

## J. COST

```text
# MINIMAL
total_cells: 10  (A: 9,19,30/HIGH + 9,30/LOW = 5; B: 4,13,18/TIGHT + 4,18/LOOSE = 5)
episodes_per_cell: 2
total_episodes: 20
relative_cost_vs_E15: ~6.7x (E15 = 3 episodi totali)
```

```text
# PREFERRED
total_cells: 14  (A: 9,14,19,24,30/HIGH + 9,30/LOW = 7; B: 4,10,13,16,18/TIGHT + 4,18/LOOSE = 7)
episodes_per_cell: 3
total_episodes: 42
relative_cost_vs_E15: ~14x (E15 = 3 episodi totali)
```

**Differenza epistemica:** MINIMAL localizza solo grossolanamente il bordo della regione di transizione (un solo punto interno per blocco) e distingue debolmente il rumore di seed dall'effetto strutturale (2 repliche). PREFERRED aggiunge due punti interni per blocco (localizzazione più fine della non-linearità) e una terza replica per cella (verifica di coerenza direzionale su 2/3 seed invece che su un confronto 1/1 non dirimente). MINIMAL è accettabile se il budget è vincolante; PREFERRED è raccomandato perché la domanda "transizione graduale o soglia netta" (centrale per H1 e H3) richiede almeno un punto centrale oltre ai due punti limite.

---

## K. DESIGN RISKS

```text
1. Opponent singolo (Codex frozen): nessun risultato di questo round è generalizzabile a un opponent diverso; l'indipendenza dall'opponent non è stabilita e non deve essere assunta.
2. Numero di seed ridotto (2-3): ogni cella resta rumorosa; questo è un round di TRAINING per localizzazione grossolana, non un round a potenza statistica piena.
3. Il controllo crop-surface di E16-B dipende dalla regola di avanzamento §E applicata ai risultati (rumorosi) di E16-A; se la stima è instabile, l'intero blocco E16-B eredita quell'instabilità. Mitigazione: la regola richiede coerenza fra soglie, non un singolo punto dato migliore.
4. La distinzione operativa TIGHT/LOOSE per pasture_allocation_policy richiede una formula precisa (qui solo descritta a livello di design, non implementata); se la formula reale devia dall'intento (es. TIGHT non davvero proporzionale), B1-B7 non testerebbero H3 come previsto.
5. La nuova infrastruttura di telemetria (event ledger, success/failure flag, realized price/value) non esiste ancora; bug o lacune in questa infrastruttura lascerebbero irrisolti gli stessi concetti (`market_transaction_value`, `action_dispatch_failure`) rimasti UNRESOLVED dopo E15.
6. I controlli fissi (workforce=10, cash policy, endgame policy, crop mix, routing) sono scelte singole non testate in questo round: i risultati sono condizionati a queste scelte specifiche e non vanno generalizzati come validi "a qualunque livello di workforce/cash policy".
7. `species_margin_differential` resta completamente non testato (herd a specie singola in tutto E16-B); nessuna conclusione, positiva o negativa, sul margine Cow/Sheep può essere tratta da questo round.
```

---

## L. RECOMMENDATION

```text
RECOMMENDED_DESIGN: E16_COPILOT_PROPOSAL (variante PREFERRED; MINIMAL accettabile come fallback a budget vincolato)
READY_FOR_CROSS_REVIEW: YES
BLOCKERS: NONE
```

Dettagli implementativi ancora da fissare prima del freeze (non bloccanti per la cross-review del design): formula esatta di `pasture_allocation_policy=TIGHT/LOOSE`, lista concreta dei seed (nuovi, non E15), disponibilità e formato dell'event ledger descritto in Sezione G.
