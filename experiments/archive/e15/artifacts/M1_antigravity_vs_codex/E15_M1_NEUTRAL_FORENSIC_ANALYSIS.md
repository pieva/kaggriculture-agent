# E15 — M1 Neutral Forensic Analysis
## Antigravity vs Codex — Seed 1113294977

**Stato:** analisi neutrale post-match, precedente alle challenge indipendenti degli agenti.  
**Vincolo:** Victory ≠ Model Validity; Defeat ≠ Model Falsification.  
**M2:** NON AUTORIZZATO.

## 1. Integrità del match

- Match: `M1_antigravity_vs_codex`
- Seed: `1113294977`
- Environment: `0.1.0`
- Steps: `720`
- P0: Antigravity — frozen submission SHA256 `629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d`
- P1: Codex — frozen submission SHA256 `fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3`
- Ontology SHA256: `5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa`
- Antigravity MODEL_SPEC SHA256: `f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46`
- Codex MODEL_SPEC SHA256: `9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7`
- Entrambi i player: `ACTIVE` per 719 step, `DONE` allo step finale.
- Remaining overage time osservato: 60 s per entrambi; nessun segnale di timeout/disqualification.

**Verdetto di validità tecnica M1:** `VALID_FOR_FORENSIC_ANALYSIS`.

Le eccezioni OpenSpiel stampate a console non risultano associate a interruzione, timeout o sostituzione del match: il replay è Kaggriculture 0.1.0, completo a 720 step, con entrambi i player `DONE`. Rimangono una anomalia infrastrutturale da registrare, ma non costituiscono evidenza di invalidazione di M1.

## 2. Esito competitivo

| Player | Final money |
|---|---:|
| Antigravity | $8,672 |
| Codex | $20,461 |

Delta Codex − Antigravity: **+$11,789**.  
Rapporto Codex / Antigravity: **2.36×**.

Questo risultato determina il punto di torneo, non il verdetto sui MODEL_SPEC.

## 3. Architettura fisica realizzata

### Antigravity

- Q1 (secondo quadrante) raggiunto: Day 9 Hour 1.
- Q2 (terzo quadrante) raggiunto: Day 19 Hour 1.
- Max hands: 12.
- Max pastures: 18.
- Max animals: 18.
- Max active crops: **8**.
- Final herd: 17 (13 Cow, 4 Sheep).

### Codex

- Q1 raggiunto: Day 11 Hour 1.
- Nessun Q2.
- Max hands: 10.
- Max pastures: 9.
- Max animals: 7.
- Max active crops: **28**.
- Final herd: 7 Cow, 0 Sheep.

**Discriminante:** Antigravity realizza più capacità fisica; Codex realizza molta più capacità agricola effettivamente attivata.

## 4. Action profile

| Action | Antigravity | Codex |
|---|---:|---:|
| WATER | 34 | 439 |
| PLANT | 93 | 111 |
| HARVEST | 414 | 105 |
| CARE | 266 | 102 |
| FEED | 309 | 109 |
| COLLECT_FERTILIZER | 15 | 0 |
| DIG | 91 | 61 |
| MOVE | 5,019 | 3,761 |
| PASS | 178 | 171 |

### Evidenza centrale: watering

- Antigravity: 34 WATER totali, con WATER > 0 in soli 5 giorni su 30.
- Codex: 439 WATER totali, con irrigazione continuativa nella grande maggioranza dei giorni produttivi.
- Rapporto Codex / Antigravity: **12.9×**.

Antigravity aveva classificato `watering_execution_rate` / `irrigation_dispatch_priority` come fattore #1, Critical/High. M1 non falsifica quella tesi: il vincitore è proprio il player che realizza il watering di un ordine di grandezza superiore. Ciò che M1 indebolisce è la conformità della submission Antigravity alla propria architettura dichiarata.

### Evidenza di dispatch

Antigravity esegue 414 HARVEST con soli 93 PLANT e un massimo simultaneo di 8 colture. Codex esegue 105 HARVEST con 111 PLANT e fino a 28 colture simultanee.

Il rapporto HARVEST/PLANT è:
- Antigravity: 4.45
- Codex: 0.95

Il dato è compatibile con una forte pressione di dispatch/retry non monetizzata in Antigravity, ma il replay non consente di attribuire ogni singolo HARVEST a un fallimento senza una action-effectiveness audit dedicata.

## 5. Revenue architecture osservabile

Market-order requests registrati:

### Antigravity
- SELL Wheat: 912 unità richieste
- SELL Milk: 215
- SELL Wool: 89
- SELL Fertilizer: 12
- Nessun SELL Strawberry/Melon registrato
- BUY_PRODUCT Wheat: 1,007 unità richieste

### Codex
- SELL Wheat: 1,266
- SELL Strawberry: 52
- SELL Melon: 47
- SELL Milk: 84
- BUY_PRODUCT Wheat: 1,483 unità richieste

Le quantità sono richieste di market order; non vanno automaticamente trattate come quantità tutte eseguite o come revenue effettiva.

La differenza osservabile più robusta è qualitativa: **Codex completa il ciclo di cash-crop monetization (Strawberry/Melon); Antigravity compra semi cash-crop ma non registra vendite di Strawberry/Melon.**

## 6. Cash trajectory

Day-end money selezionato:

| Day | Antigravity | Codex |
|---:|---:|---:|
| 0 | 232 | 928 |
| 8 | 2,092 | 444 |
| 10 | 806 | 6,365 |
| 12 | 800 | 5,963 |
| 18 | 7,184 | 2,555 |
| 19 | 81 | 3,583 |
| 22 | 2,193 | 6,218 |
| 24 | 4,178 | 12,153 |
| 26 | 4,784 | 18,501 |
| 29 | 8,672 | 20,461 |

Il lead non è monotono. Antigravity supera Codex nei giorni 8–9 e di nuovo al giorno 18. Il vantaggio Codex diventa permanente dal Day 19, coincidente con la fase in cui Antigravity completa Q2, scala a 12 hands/18 pastures/18 animals e porta il cash di fine giornata a $81.

Questo è forte supporto alla distinzione tra **asset acquisition** e **asset activation/payback**, ma non prova che Q2 sia causalmente responsabile del gap: Q2, herd ramp, workforce ramp e dispatch sono simultanei e quindi confounded.

## 7. Canonical concept classification — M1

La classificazione seguente riguarda ciò che M1 discrimina. Non sostituisce ranking/confidence congelati e non modifica retroattivamente i MODEL_SPEC.

| concept_id | M1 status | Evidenza / interpretazione |
|---|---|---|
| `land_surface_total` | WEAKENED | 3 quadranti Antigravity perdono contro 2 Codex; superficie posseduta non predice da sola il risultato. |
| `activated_land_surface` | SUPPORTED | Codex attiva fino a 28 crop + 9 pasture su 2Q; Antigravity, pur a 3Q, non supera 8 crop + 18 pasture. |
| `crop_surface_maintained` | SUPPORTED | Il vincitore mantiene una superficie coltivata molto maggiore. |
| `maintained_productive_surface` | SUPPORTED | Capacità realmente mantenuta discrimina meglio della superficie nominale. |
| `land_activation_payback` | SUPPORTED | Q2/scale Antigravity assorbono capitale senza produrre un vantaggio terminale; coerente con la tesi Codex del payback. |
| `pasture_arable_surface_tradeoff` | SUPPORTED | 18 pasture Antigravity coincidono con footprint crop molto ridotto; Codex preserva più spazio agricolo. Impatto economico preciso resta parzialmente confounded. |
| `workforce_headcount` | WEAKENED | 12 hands non battono una policy che raggiunge al massimo 10 e scende successivamente. |
| `worker_capacity_available` | CONFOUNDED | Più capacità esiste, ma il problema è come viene allocata; M1 non isola il valore marginale della capacità. |
| `hire_order_scheduling` | NOT_DISCRIMINATED | Nessuna evidenza M1 sufficiente di ordini critici dropped per batch limit. |
| `marginal_hire_payback` | SUPPORTED | Maggior headcount Antigravity non genera payoff proporzionale; coerente con hiring elastico Codex. |
| `productive_action_share` | INCONCLUSIVE | La definizione aggregata disponibile non separa nettamente i player; la composizione delle azioni è molto più discriminante della quota grezza. |
| `movement_overhead` | NOT_DISCRIMINATED | Antigravity ha più MOVE assoluti, ma la quota MOVE sul totale delle azioni operative è ~71% per entrambi. |
| `routing_completion_efficiency` | CONFOUNDED | Il diverso completamento dei cicli è evidente, ma non è separabile da crop mix, watering e herd workload. |
| `action_dispatch_failure` | SUPPORTED | 414 HARVEST / 93 PLANT e max 8 crop costituiscono una forte firma di dispatch inefficiente; richiede audit di effectiveness per causalità completa. |
| `worker_action_monetization_rate` | SUPPORTED | Codex produce 2.36× final money con meno azioni operative complessive; la conversione economica per capacità usata discrimina fortemente. |
| `watering_execution_rate` | SUPPORTED | 439 vs 34 WATER; è la differenza operativa più netta del match. |
| `watering_continuity` | SUPPORTED | Codex irriga con continuità; Antigravity irriga solo in 5 giorni. |
| `crop_care_completion_rate` | SUPPORTED | La combinazione footprint crop + continuità WATER è fortemente associata al vincitore. |
| `crop_revenue_mix` | SUPPORTED | Codex monetizza Strawberry/Melon; Antigravity non registra SELL di cash crops. |
| `feed_market_dependency` | WEAKENED | Antigravity dichiara feed autarky come Critical, ma il match registra grande ricorso a BUY_PRODUCT Wheat; Codex ricorre anch'esso al mercato e vince. |
| `feed_market_expenditure` | INCONCLUSIVE | Le quantità richieste sono osservabili, ma non abbiamo un ledger verificato della spesa eseguita per isolare l'impatto monetario. |
| `wheat_operating_flow` | SUPPORTED | Il winner usa Wheat come grande flusso operativo buy/sell; coerente con la formulazione Codex più ampia rispetto all'autarky necessaria. |
| `market_churn_cost` | CONFOUNDED | Elevato churn Wheat in entrambi, senza transaction-value ledger sufficiente per attribuire costo netto. |
| `livestock_headcount` | WEAKENED | Antigravity scala a 18 animali; Codex vince con 7. Herd size non è un driver sufficiente e la necessità di un target alto è indebolita. |
| `pasture_capacity_alignment` | NOT_DISCRIMINATED | Entrambi dispongono di pasture capacity sufficiente per il proprio herd; non è il differenziale principale. |
| `livestock_product_flow` | CONFOUNDED | Antigravity monetizza più Milk/Wool/Fertilizer ma perde; il loop è redditizio, ma M1 non ne isola il ROI marginale rispetto ai cash crops. |
| `species_margin_differential` | WEAKENED | Il winner termina con 7 Cow e 0 Sheep; M1 indebolisce l'idea che sheep scaling sia necessario/alto impatto, senza falsificare il margine unitario Wool. |
| `fertilizer_byproduct_flow` | WEAKENED | Antigravity raccoglie Fertilizer, Codex zero, ma Codex vince nettamente; indebolito come differenziale High-impact, non come margine positivo. |
| `operating_cash_buffer` | SUPPORTED | Opening: Codex $928 vs Antigravity $176; il vincitore preserva più liquidità mentre costruisce la crop engine. |
| `deployable_capital_window` | SUPPORTED | La capacità di investire senza soffocare il ciclo operativo è coerente con la traiettoria Codex; forte stress Antigravity al Day 19. |
| `inventory_to_cash_conversion` | SUPPORTED | Il winner completa una più ampia monetizzazione di prodotti, in particolare cash crops. |
| `product_mix_revenue` | SUPPORTED | Revenue breadth e cash-crop conversion discriminano fortemente. |
| `endgame_shutdown_timing` | NOT_DISCRIMINATED | Entrambi arrivano a 0 crop finali; Codex azzera anche le hands, ma M1 non isola il valore causale del shutdown. |
| `endgame_inventory_liquidation` | INCONCLUSIVE | Entrambi lasciano residui di Wheat/seeds; non è disponibile un valore terminale completo degli inventory residui. |
| `field_cleanliness_state` | WEAKENED | Codex termina con 22 weeds e vince; Antigravity con 5 weeds perde. Cleanliness non è un obiettivo competitivo sufficiente. |
| `weed_backlog_cost` | CONFOUNDED | Il costo esiste solo se interferisce con superficie produttiva; M1 non fornisce un'ablation isolata. |
| `state_capacity_alignment` | SUPPORTED | Codex allinea meglio crop footprint e care capacity; Antigravity possiede più land/workers/animals ma non converte la capacità in crop throughput. |
| `operational_divergence_onset` | SUPPORTED | La divergenza è visibile già al Day 0: 20 crop/16 WATER Codex vs 4 crop/0 WATER Antigravity. |
| `economic_lock_in_onset` | CONFOUNDED | Il cash lead cambia più volte; il vantaggio Codex diventa permanente solo dal Day 19. Nessun Day-12 lock-in universale è dimostrato. |
| `local_kaggle_fidelity_gap` | NOT_DISCRIMINATED | M1 è un singolo match locale controllato; non confronta local vs Kaggle. |
| `final_money_outcome` | SUPPORTED | Outcome terminale valido e osservato: $20,461 vs $8,672. |

## 8. Neutral model verdict after M1

### Antigravity

**Non falsificato.** Diversi principi causali centrali sono anzi coerenti con il match:
- watering è critico;
- raw land/headcount non bastano;
- field cleanliness non basta;
- monetized throughput è ciò che conta.

Ma M1 produce una severa **model-to-policy / model-to-implementation inconsistency**:
- il MODEL_SPEC mette watering al rank #1; la submission realizza 34 WATER;
- dichiara cash-crop rotation; non registra vendite Strawberry/Melon;
- dichiara feed autarky; registra forte BUY_PRODUCT Wheat;
- dichiara capital-protected expansion; al completamento della massima scala si osserva forte compressione di liquidità;
- costruisce 3Q/12 hands/18 herd ma non supera 8 crop attive.

**Verdetto M1 Antigravity:** `MODEL CORE PARTIALLY SUPPORTED / POLICY REALIZATION STRONGLY WEAKENED`.

### Codex

M1 supporta molte delle riformulazioni distintive del MODEL_SPEC:
- land optional unless activated/payback-positive;
- marginal hire rather than fixed workforce target;
- inventory-to-cash conversion;
- product/revenue breadth;
- monetized throughput over raw asset counts;
- cash/deployable capital discipline;
- compact Q0/Q1 branch as viable architecture.

Ma non dimostra ancora:
- causalità di ogni singolo fattore;
- superiorità generale su seed differenti;
- validità delle componenti NOT_USED/ABSENT;
- che Q2 sia svantaggioso in generale.

**Verdetto M1 Codex:** `MODEL DIRECTION SUBSTANTIALLY SUPPORTED / GENERALIZATION NOT YET ESTABLISHED`.

## 9. Post-M1 status

- Neutral forensic analysis: **COMPLETED**
- Independent Antigravity challenge: **PENDING**
- Independent Codex challenge: **PENDING**
- ChatGPT consensus synthesis: **PENDING**
- Model updates: **PENDING**
- M2 authorization: **NO**
