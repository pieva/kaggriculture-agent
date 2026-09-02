# E15 — M3 CONSENSUS SYNTHESIS
## Copilot (P0) vs Antigravity (P1) — Seed 3122977751

**Esito:** Copilot $26,629 vs Antigravity $9,371 — delta +$17,258 Copilot.  
**Stato:** consensus post-match completato; attende doppio ACK.  
**Principio:** Victory ≠ Model Validity; Defeat ≠ Model Falsification.

## 1. Fonti del consensus

Il consensus integra:
1. `E15_M3_NEUTRAL_FORENSIC_ANALYSIS.md`;
2. Copilot M3 Independent Audit;
3. `E15_M3_CHALLENGE_ANTIGRAVITY.md`.

Entrambi i model owner hanno restituito sostanzialmente `ACCEPT_WITH_CHALLENGES`.

Nessun artefatto frozen viene modificato.

## 2. Finding centrale

M3 replica il principale failure mode Antigravity già osservato in M1.

Antigravity realizza nuovamente:
- 3 quadranti;
- 12 hands;
- 18 pasture;
- 18 animali max / 17 final herd;
- WATER estremamente basso;
- HARVEST molto superiore a PLANT;
- elevato movement;
- working crop surface molto ridotta.

Copilot realizza invece una policy compatta e molto simile a M2:
- 2 quadranti;
- 9 hands;
- 5 pasture;
- 4 animali;
- 25 active crops max;
- 439 WATER;
- 302 SELL orders.

**Consensus core:** M3 non dimostra che la scala sia intrinsecamente negativa. Dimostra che la scala nominale non attivata e non mantenuta, combinata con dispatch inefficiente e pressione di capitale/livestock, non produce compounded throughput.

La replica M1→M3 rende questa diagnosi sistematica a livello di `POLICY_REALIZATION` / `IMPLEMENTATION_FIDELITY`.

## 3. Replication fingerprints

### Antigravity

| Metrica | M1 | M3 |
|---|---:|---:|
| WATER | 34 | 30 |
| HARVEST | 414 | 374 |
| FEED | 309 | 315 |
| MOVE | 5,019 | 5,047 |
| max hands | 12 | 12 |
| max pasture | 18 | 18 |
| max animals | 18 | 18 |
| final herd | 17 | 17 |
| quadrants | 3 | 3 |
| max active crops | 8 | 9 |
| final money | $8,672 | $9,371 |

### Copilot

| Metrica | M2 | M3 |
|---|---:|---:|
| WATER | 446 | 439 |
| PLANT | 116 | 115 |
| HARVEST | 110 | 113 |
| FEED | 84 | 84 |
| CARE | 84 | 84 |
| max pasture | 5 | 5 |
| max animals | 4 | 4 |
| SELL orders | 298 | 302 |
| max hands | 9 | 9 |

Il torneo produce quindi due policy fingerprints altamente riproducibili: uno economicamente efficace nei due match Copilot, uno sistematicamente disallineato nei due match Antigravity.

## 4. Consensus sui principali concept_id

| concept_id | Consensus M3 | Decisione |
|---|---|---|
| `land_surface_total` | WEAKENED | 3Q Antigravity perde nettamente contro 2Q; land totale non è driver monotono. |
| `land_purchase_timing` | WEAKENED | Early Q1/Q2 non è sufficiente; il lock-in Copilot precede Q2. |
| `activated_land_surface` | CONFOUNDED | Ownership/pasture non equivalgono a crop activation. |
| `crop_surface_maintained` | SUPPORTED | 25 crop max Copilot vs 9 Antigravity. |
| `maintained_productive_surface` | SUPPORTED | Capacità mantenuta discrimina meglio della capacità nominale. |
| `monetized_productive_output` | SUPPORTED | Copilot produce final cash 2.84×. |
| `land_activation_payback` | SUPPORTED | Espansione Antigravity non mostra payback relativo. |
| `pasture_arable_surface_tradeoff` | SUPPORTED | 18 pasture/9 crops vs 5 pasture/25 crops. |
| `workforce_headcount` | WEAKENED | 12 hands non superano 9 hands meglio allineate. |
| `worker_capacity_available` | CONFOUNDED | Capacità nominale ≠ capacità monetizzata. |
| `marginal_hire_payback` | SUPPORTED | Workforce extra Antigravity non mostra ritorno relativo. |
| `productive_action_share` | WEAKENED | Volume operativo grezzo non predice final money. |
| `movement_overhead` | SUPPORTED | 5,047 vs 3,765; in M3 discrimina. |
| `routing_completion_efficiency` | SUPPORTED | Movement + HARVEST/PLANT indicano completion inefficiente. |
| `action_dispatch_failure` | SUPPORTED | HARVEST/PLANT 3.74 Antigravity vs ~0.98 Copilot, replica M1. |
| `worker_action_monetization_rate` | SUPPORTED | Supportato come proxy macro; nessun ledger marginale. |
| `watering_execution_rate` | SUPPORTED | 439 vs 30: M3 è chiaramente nel regime sotto-soglia Antigravity. |
| `watering_continuity` | SUPPORTED | Differenza operativa ampia e replicata. |
| `crop_revenue_mix` | SUPPORTED | Copilot realizza cash-crop flow assente in Antigravity. |
| `feed_market_dependency` | CONFOUNDED | Copilot usa market Wheat intensamente e vince. |
| `feed_market_expenditure` | INCONCLUSIVE | Manca executed transaction-value ledger. |
| `wheat_operating_flow` | SUPPORTED | Intenso flusso Wheat Copilot; non prova profitto del churn. |
| `market_churn_cost` | INCONCLUSIVE | Nessuna attribuzione di margine netto. |
| `livestock_headcount` | WEAKENED | 18 vs 4; target alto non è sufficiente. |
| `livestock_capacity` | WEAKENED | Grande subsystem livestock compete con altre capacità. |
| `pasture_capacity_alignment` | SUPPORTED | Alignment deve includere crop/cash/workforce, non solo pasture:animals. |
| `livestock_product_flow` | CONFOUNDED | Milk/Wool/Fertilizer Antigravity esistono ma non isolano valore marginale. |
| `species_margin_differential` | NOT_DISCRIMINATED | Nessun confronto causale pulito. |
| `fertilizer_byproduct_flow` | WEAKENED | Presente ma non sufficiente. |
| `operating_cash_buffer` | SUPPORTED | $73 Day18 evidenzia forte fragilità finanziaria durante espansione. |
| `deployable_capital_window` | SUPPORTED | Copilot entra prima in cash generation sostenuta. |
| `asset_liquidity_lag` | SUPPORTED | Espansione asset Antigravity precede il ritorno e comprime la cassa. |
| `inventory_to_cash_conversion` | SUPPORTED | 302 vs 198 SELL orders, con cautela requests≠executions. |
| `reinvestment_cash_flow` | SUPPORTED | Copilot costruisce un ciclo di cassa sostenuto dopo Day10. |
| `product_mix_revenue` | SUPPORTED | Supporto qualitativo, non decomposizione transaction-value. |
| `market_transaction_value` | INCONCLUSIVE | Ledger eseguito assente. |
| `state_capacity_alignment` | SUPPORTED | Discriminante strutturale principale. |
| `operational_divergence_onset` | SUPPORTED | Divergenza precede il lock-in monetario. |
| `economic_lock_in_onset` | SUPPORTED | Copilot avanti permanentemente da step 252 / Day10 Hour12. |
| `endgame_shutdown_timing` | CONFOUNDED | Gap formatosi molto prima. |
| `endgame_inventory_liquidation` | INCONCLUSIVE | Contributo indipendente non isolato. |
| `field_cleanliness_state` | CONFOUNDED | Non emerge come causa primaria. |
| `local_kaggle_fidelity_gap` | NOT_DISCRIMINATED | Non testato. |
| `final_money_outcome` | SUPPORTED | $26,629 vs $9,371. |

## 5. Arbitraggio delle challenge Antigravity

### Irrigation Rank #1
Accolta la distinzione tra `MODEL_VALIDITY` e realizzazione.

M1 e M3 supportano fortemente che un regime di WATER estremamente basso sia incompatibile con una working crop surface ampia e mantenuta.

Non viene però accolta la formulazione “dimostrazione definitiva” basata sulla coincidenza di **439 WATER** dei due vincitori: la stessa quantità è una coincidenza osservazionale, non identifica un optimum universale né causalità esclusiva.

**Consensus:** `watering_execution_rate = SUPPORTED`; soglia/optimum quantitativo non determinato.

### Dispatch bug
La firma HARVEST/PLANT è replicata e fortemente diagnostica.

Non viene elevata a prova che ogni HARVEST sia stato inviato a tile non mature, né che l'intero deficit derivi da un singolo bug.

**Consensus:** `action_dispatch_failure = SUPPORTED` come firma osservabile; causa implementativa precisa da verificare nel codice post-freeze.

### Wheat trading vs emergency feed
Challenge accolta solo parzialmente.

È plausibile che i due flussi abbiano funzioni diverse, ma le richieste BUY/SELL non costituiscono ledger eseguito. Non è quindi dimostrato che il churn Copilot “generi liquidità” né che i 904 Wheat Antigravity siano tutti emergency feed.

**Consensus:** `feed_market_dependency = CONFOUNDED`, `market_churn_cost = INCONCLUSIVE`.

### Livestock opportunity cost
Accolta come interpretazione strutturale: il subsystem Antigravity è molto più grande e compete con crop surface, workforce e cash.

Non si attribuisce però un costo monetario preciso alle 598 CARE+FEED senza action-value ledger.

### Q2
Challenge accolta integralmente: il permanent lead Copilot inizia allo step 252 / Day10 Hour12, molto prima del Q2 Antigravity. Q2 è quindi un amplificatore/sintomo plausibile, non la causa iniziale del divergence.

## 6. Arbitraggio delle challenge Copilot

### Stability M2→M3
Accolta. La stabilità del footprint Copilot su due seed e due avversari diversi costituisce evidenza di robustezza relativa.

Non equivale a generalizzazione stabilita.

### Gate → alignment → monetization
La sequenza temporale/strutturale è coerente con il MODEL_SPEC Copilot, ma M3 osservazionale non identifica una catena causale controfattuale.

**Consensus:** `state_capacity_alignment = SUPPORTED`; causal ordering non stabilito.

### Worker action monetization
`SUPPORTED` come proxy macro. Non viene riutilizzato il valore `$7.13/action` di M2 per M3 e non viene interpretato come marginal revenue/action.

### Strongly validated / excellent fidelity
Tali etichette non appartengono alla tassonomia E15. Il consensus mantiene le classificazioni canoniche e formula il giudizio globale separatamente.

## 7. Model verdict M3

### Antigravity

**MODEL_VALIDITY = PARTIALLY_SUPPORTED**

Il modello contiene principi che M3 supporta: irrigation priority, maintained crop surface, land activation/payback, pasture/arable tradeoff, marginal hire payback e state-capacity alignment.

**POLICY_REALIZATION = STRONGLY_WEAKENED**

I target rigidi di scala — 3Q, 12 hands, 18 livestock — vengono raggiunti senza working crop surface e monetizzazione proporzionate.

**IMPLEMENTATION_FIDELITY = STRONGLY_WEAKENED**

M1 e M3 replicano WATER estremamente basso, HARVEST/PLANT anomalo e movement elevato, in conflitto con le priorità dichiarate del modello.

La replica rende il verdetto più robusto rispetto a M1.

### Copilot

**MODEL_VALIDITY = SUBSTANTIALLY_SUPPORTED**

M3 è coerente con throughput-to-cash, compact working set, crop maintenance/monetization, pasture/livestock alignment e state-capacity alignment.

**POLICY_REALIZATION = SUPPORTED**

Il footprint M2→M3 è molto stabile e coerente con il frozen MODEL_SPEC.

**GENERALIZATION = PARTIALLY_SUPPORTED, NOT ESTABLISHED**

Due seed e due avversari diversi migliorano l'evidenza rispetto a M2, ma non sostituiscono una validazione multi-seed sistematica.

## 8. Delta post-M3 — registrare, non applicare ai frozen

### Antigravity
- mantenere irrigation come priorità critica, ma verificare enforcement nel dispatcher;
- introdurre guardie contro retry HARVEST non produttivi;
- rendere Q2 condizionale a active crop surface, cash e utilization;
- sostituire herd target rigido con crescita dinamica subordinata al surplus crop/cash;
- rendere hiring elastico al workload reale;
- verificare il codice che genera la replica M1/M3 prima di una nuova submission;
- distinguere esplicitamente MODEL_SPEC correctness da implementation conformance.

### Copilot
- mantenere throughput-to-cash e state-capacity alignment ai massimi livelli;
- non trasformare 4 livestock / 5 pasture / 9 hands in target universali;
- mantenere expansion gating dinamico;
- separare feed security da autarky: market flow può essere compatibile con sicurezza operativa;
- richiedere transaction ledger prima di attribuire profitto al Wheat churn;
- mantenere generalization confidence limitata fino a multi-seed.

## 9. Implicazione cross-match E15

M1, M2 e M3 insieme suggeriscono un modello a due regimi:

1. **Regime sotto-soglia operativa:** se irrigation/dispatch/maintenance falliscono, la capacità nominale non viene attivata e la scala amplifica il disallineamento.
2. **Regime sopra-soglia operativa:** una volta garantita la manutenzione minima, la discriminazione si sposta su monetizzazione, state-capacity alignment, capital timing e sell-through.

M1 e M3 forniscono due osservazioni indipendenti del primo regime.
M2 discrimina soprattutto il secondo.

Questa è una sintesi empirica E15, non una legge universale dell'ambiente.

## 10. Stato competitivo E15

| Agent | Record |
|---|---:|
| Copilot | **2–0** |
| Codex | **1–1** |
| Antigravity | **0–2** |

**Vincitore competitivo E15: COPILOT.**

Nessun tie-break necessario.

Questo outcome non viene equiparato automaticamente a “MODEL_SPEC Copilot universalmente migliore”.

## 11. Gate di chiusura M3

Completati:
- [x] M3 execution
- [x] integrity verification
- [x] neutral forensic analysis
- [x] Copilot independent review
- [x] Antigravity independent review
- [x] consensus synthesis
- [x] concept-level arbitration
- [x] post-M3 deltas recorded
- [x] frozen artifacts unchanged

Da completare:
- [ ] `ACK_M3_CONSENSUS_COPILOT`
- [ ] `ACK_M3_CONSENSUS_ANTIGRAVITY`

### Decisione

**M3 CLOSED SUBJECT TO CONSENSUS ACK.**

Dopo il doppio ACK:
1. M3 diventa `CLOSED`;
2. E15 può essere dichiarato epistemicamente chiuso;
3. si produce la sintesi finale E15;
4. solo allora si apre la fase post-tournament di revisione MODEL_SPEC / capability check dei modelli / nuova submission.

**Nessuna modifica agli artefatti frozen prima della chiusura.**
