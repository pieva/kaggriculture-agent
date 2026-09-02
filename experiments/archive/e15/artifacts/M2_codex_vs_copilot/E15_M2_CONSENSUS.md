# E15 — M2 CONSENSUS SYNTHESIS
## Codex vs Copilot — Seed 3033283457

**Stato:** consenso post-match completato.  
**Esito:** Copilot $37,752 vs Codex $27,510 — delta +$10,242 Copilot.  
**Principio:** Victory ≠ Model Validity; Defeat ≠ Model Falsification.

## 1. Fonti

Il consenso integra:
1. `E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md`
2. Codex M2 Self-Audit (`ACCEPT_WITH_CHALLENGES`)
3. `M2_COPILOT_INDEPENDENT_AUDIT.md` (`ACCEPT_WITH_CHALLENGES`)

Nessun artefatto frozen viene modificato.

## 2. Decisione generale

M2 non è principalmente un test di watering, land timing, workforce o movement:
- entrambi raggiungono Q1 allo stesso momento;
- entrambi raggiungono max 10 hands;
- WATER è alto per entrambi (475 Codex, 446 Copilot);
- MOVE è praticamente identico;
- action volume totale è praticamente identico.

La discriminante principale è la **conversione economica di un working set di dimensione diversa**.

Codex mantiene un working set fisicamente maggiore (max 37 crop, 9 pasture, 7 animali); Copilot vince con un working set più compatto (max 28 crop, 5 pasture, 4 animali) e più SELL orders.

**Consensus core:** M2 supporta `monetized_productive_output`, `worker_action_monetization_rate`, `state_capacity_alignment`, `pasture_arable_surface_tradeoff`, `deployable_capital_window` e `inventory_to_cash_conversion`. Non supporta l'idea che più superficie, più WATER, più productive-action share o più livestock producano monotonicamente più final money.

## 3. Consensus concept_id

| concept_id | Consensus M2 | Decisione |
|---|---|---|
| `land_surface_total` | NOT_DISCRIMINATED | Stesso 2Q. |
| `land_purchase_timing` | NOT_DISCRIMINATED | Q1 allo stesso step. |
| `activated_land_surface` | CONFOUNDED | Codex attiva più superficie ma perde. |
| `crop_surface_maintained` | WEAKENED | 37 crop Codex vs 28 Copilot; quantità maggiore non è sufficiente. |
| `maintained_productive_surface` | CONFOUNDED | Conta la monetizzazione, non solo la quantità mantenuta. |
| `monetized_productive_output` | SUPPORTED | Copilot ottiene più final cash con working set più piccolo. |
| `land_activation_payback` | NOT_DISCRIMINATED | Land branch sostanzialmente identico. |
| `pasture_arable_surface_tradeoff` | SUPPORTED | Copilot usa meno pasture/herd e preserva un working set più compatto. |
| `workforce_headcount` | NOT_DISCRIMINATED | Max 10 entrambi. |
| `worker_capacity_available` | NOT_DISCRIMINATED | Capacità simile. |
| `marginal_hire_payback` | NOT_DISCRIMINATED | HIRE requests identiche. |
| `productive_action_share` | WEAKENED | Codex ha share grezza maggiore e perde. |
| `movement_overhead` | NOT_DISCRIMINATED | MOVE/share quasi identici. |
| `routing_completion_efficiency` | CONFOUNDED | Manca effectiveness ledger. |
| `action_dispatch_failure` | NOT_DISCRIMINATED | Nessuna firma estrema come M1. |
| `worker_action_monetization_rate` | SUPPORTED | Proxy $7.13/action Copilot vs $5.17 Codex; non è un transaction ledger. |
| `watering_execution_rate` | WEAKENED | Entrambi superano una soglia operativa elevata; Codex irriga di più e perde. M2 indebolisce una lettura monotona, non la necessità del watering. |
| `watering_continuity` | NOT_DISCRIMINATED | Entrambi continui. |
| `crop_revenue_mix` | SUPPORTED | Differenze qualitative di sell-through/cash crops coerenti con il winner. |
| `feed_availability` | CONFOUNDED | Forte uso market Wheat in entrambi. |
| `feed_security_buffer` | CONFOUNDED | Copilot vince pur con forte market-Wheat flow. |
| `feed_market_dependency` | CONFOUNDED | Maggiore dipendenza richiesta non impedisce la vittoria Copilot. |
| `feed_market_expenditure` | INCONCLUSIVE | Manca executed transaction-value ledger. |
| `wheat_operating_flow` | SUPPORTED | Forte flusso operativo Wheat, senza inferire profitto. |
| `market_churn_cost` | INCONCLUSIVE | Costo netto non osservato. |
| `livestock_headcount` | WEAKENED | Herd maggiore Codex non produce outcome superiore. |
| `livestock_capacity` | SUPPORTED | M2 favorisce capacità subordinata al working set. |
| `pasture_capacity_alignment` | SUPPORTED | 5 pasture/4 animali Copilot vs 9/7 Codex; non implica target universale. |
| `livestock_product_flow` | CONFOUNDED | Causalità non isolata. |
| `species_margin_differential` | NOT_DISCRIMINATED | Nessun confronto pulito Cow/Sheep. |
| `fertilizer_byproduct_flow` | NOT_DISCRIMINATED | Volumi troppo piccoli. |
| `operating_cash_buffer` | CONFOUNDED | Copilot accetta meno cash early e poi recupera; buffer alto non è obiettivo monotono. |
| `deployable_capital_window` | SUPPORTED | Timing investimento/payback discrimina la traiettoria. |
| `asset_liquidity_lag` | SUPPORTED | L'investimento anticipa il ritorno economico. |
| `inventory_to_cash_conversion` | SUPPORTED | Copilot registra più SELL orders e maggiore final cash. |
| `reinvestment_cash_flow` | SUPPORTED | Vantaggio Copilot persistente dal Day 12 e crescente. |
| `product_mix_revenue` | SUPPORTED | Supporto qualitativo; valore netto non ricostruito. |
| `market_transaction_value` | INCONCLUSIVE | Ledger eseguito non disponibile nel dossier corrente. |
| `state_capacity_alignment` | SUPPORTED | Miglior discriminante strutturale di M2. |
| `operational_divergence_onset` | SUPPORTED | Divergenze precedono il lock-in monetario. |
| `economic_lock_in_onset` | SUPPORTED | In M2 il vantaggio Copilot diventa permanente allo step 301 / Day 12 Hour 13; non è soglia universale. |
| `endgame_shutdown_timing` | CONFOUNDED | Non isolato causalmente. |
| `endgame_inventory_liquidation` | INCONCLUSIVE | La review Copilot lo considera coerente col modello, ma gli artefatti disponibili non consentono attribuzione causale forte. |
| `field_cleanliness_state` | NOT_DISCRIMINATED | Non emerge come driver. |
| `local_kaggle_fidelity_gap` | NOT_DISCRIMINATED | Non testato. |
| `final_money_outcome` | SUPPORTED | $37,752 vs $27,510. |

## 4. Arbitraggio Codex

### `watering_execution_rate`
Challenge accolta con formulazione di soglia.

M1: watering estremamente basso è associato al collasso della capacità crop.
M2: una volta raggiunto un livello elevato, più WATER non produce monotonicamente più cash.

**Consensus:** `WEAKENED` come driver monotono in M2; il concetto resta strategicamente rilevante.

### `productive_action_share`
Challenge accolta. La share grezza è insufficiente.

### `worker_action_monetization_rate`
Challenge accolta con limitazione. `SUPPORTED` come proxy macro, non come ricavo marginale misurato.

### `operating_cash_buffer`
Challenge accolta. È un vincolo dinamico, non un obiettivo da massimizzare.

### `market_churn_cost`
Challenge accolta. `INCONCLUSIVE`.

## 5. Arbitraggio Copilot

### `throughput_to_cash_conversion`
Accolto come `SUPPORTED`, ma la formula “+41% vendite” deve essere letta come maggiore numero di SELL orders, non come +41% revenue realizzata.

### `working_set_capacity_gate`
La review Copilot lo classifica `WEAKENED` perché entrambi possiedono un gate. Il consensus distingue presenza del meccanismo da qualità dell'allineamento:
- il gate come semplice presenza non è discriminato;
- `state_capacity_alignment`, che ne rappresenta l'esito osservabile, è `SUPPORTED`.

### `crop_activation_and_monetization`
Accolto come direzione `SUPPORTED`, ma non perché Copilot abbia più crop: ne ha meno. Il supporto deriva dal maggiore sell-through/final cash con working set più piccolo.

### `pasture_to_livestock_alignment`
Accolto come `SUPPORTED`, senza trasformare 4 animali/5 pasture in target universale.

### `wheat_feed_security`
La formulazione forte di buffer/autarky non è supportata da M2. Copilot usa un intenso market-Wheat flow.

**Consensus:** `CONFOUNDED`.

### `cash_buffer_before_expansion`
La review Copilot propone `INCONCLUSIVE`; Codex propone `CONFOUNDED`. Gli stati osservati mostrano che più cash early non predice l'esito, mentre investimento/payback differiscono.

**Consensus canonico:** `operating_cash_buffer = CONFOUNDED`; `deployable_capital_window = SUPPORTED`.

### Endgame liquidation
La review Copilot la considera una delle tre tesi validate. Il dossier M2 non isola il contributo causale dell'endgame rispetto al vantaggio già consolidato dal Day 12.

**Consensus:** `endgame_inventory_liquidation = INCONCLUSIVE`.

### Correzione fattuale
Per il consensus si usa il dato replay/forensics **max 4 animali Copilot**, non la formulazione “3 animali” presente nel sommario della review Copilot.

## 6. Verdict sui MODEL_SPEC

### Codex

`MODEL_VALIDITY = PARTIALLY_SUPPORTED`

Restano supportati:
- monetized throughput;
- deployable capital;
- inventory-to-cash;
- revenue/product mix;
- state-capacity alignment.

M2 indebolisce:
- productive-action share come KPI autonomo;
- crop surface come driver monotono;
- watering volume oltre la soglia operativa;
- herd/pasture size come proxy di performance.

`RELATIVE_POLICY_REALIZATION = WEAKENED`

### Copilot

`MODEL_VALIDITY = SUBSTANTIALLY_SUPPORTED`

M2 è coerente con i tre principi più importanti:
1. throughput-to-cash conversion;
2. working-set/state-capacity alignment;
3. crop activation and monetization.

Supporta inoltre pasture/livestock alignment e asset/cash timing.

Restano confounded/inconclusive:
- strong wheat feed security/autarky;
- cash buffer in forma rigida;
- endgame liquidation come causa indipendente.

`GENERALIZATION = NOT_ESTABLISHED`

## 7. Delta post-M2 — registrare, non applicare ai frozen

### Codex
- rendere `watering_execution_rate` diagnostica autonoma ma non monotona;
- separare action share da action quality/monetization;
- ridurre fiducia in crop/pasture/herd quantity come driver diretti;
- trattare cash buffer come vincolo dinamico;
- rafforzare `state_capacity_alignment`;
- richiedere executed transaction ledger.

### Copilot
- mantenere rank elevato a throughput-to-cash e working-set alignment;
- precisare `crop_activation_and_monetization` come velocità/qualità di conversione, non massimizzazione superficie;
- separare feed security in internal buffering e market-flow management;
- non promuovere confidence sulla base di una sola seed;
- mantenere herd target dinamico;
- non considerare endgame liquidation validata causalmente da M2.

## 8. Insight cross-match provvisorio

M1 e M2 insieme suggeriscono una funzione a due regimi:

1. **Sotto una soglia di capacità operativa**, failure di watering/dispatch/activation domina il risultato.
2. **Sopra la soglia**, il vantaggio dipende soprattutto da conversione, allineamento del working set, timing del capitale e sell-through.

Questa è una **ipotesi post-M2**, non ancora una regola del modello. M3 è il test indipendente successivo.

## 9. Gate M2 → M3

- [x] M2 frozen execution completed
- [x] integrity verified
- [x] neutral forensic analysis completed
- [x] Codex independent challenge completed
- [x] Copilot independent challenge completed
- [x] consensus synthesis completed
- [x] concept-level arbitration completed
- [x] post-M2 deltas recorded
- [x] frozen artifacts unchanged

### DECISIONE

**M2 CLOSED SUBJECT TO CONSENSUS ACK.**

Prima dell'esecuzione di M3:
1. Codex deve leggere questo consensus e restituire `ACK_M2_CONSENSUS_CODEX` oppure un errore fattuale bloccante.
2. Copilot deve leggerlo e restituire `ACK_M2_CONSENSUS_COPILOT` oppure un errore fattuale bloccante.
3. Solo con doppio ACK, M3 è autorizzato.

M3 previsto:
`M3 — Copilot (P0) vs Antigravity (P1)`  
Seed: `3122977751`

**M3 NON ANCORA AUTORIZZATO.**
