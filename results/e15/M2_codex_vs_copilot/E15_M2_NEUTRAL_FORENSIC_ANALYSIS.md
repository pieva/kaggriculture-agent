# E15 — M2 Neutral Forensic Analysis
## Codex vs Copilot — Seed 3033283457

**Stato:** analisi neutrale post-match, precedente alle challenge indipendenti.  
**Vincolo:** Victory ≠ Model Validity; Defeat ≠ Model Falsification.  
**M3:** NON AUTORIZZATO.

## 1. Integrità del match

- Match: `M2_codex_vs_copilot`
- Seed: `3033283457`
- Environment: `0.1.0`
- Steps: `720`
- P0: Codex
- P1: Copilot
- Codex submission SHA256: `fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3`
- Copilot submission SHA256: `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb`
- Ontology SHA256: `5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa`
- Codex MODEL_SPEC SHA256: `9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7`
- Copilot MODEL_SPEC SHA256: `d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686`

Gli hash e il mapping dei player coincidono con il freeze pre-dichiarato.

**Verdetto tecnico preliminare:** `VALID_FOR_FORENSIC_ANALYSIS`.

Le eccezioni OpenSpiel osservate sono identiche a M1 e non risultano associate a interruzione del match. Restano anomalia infrastrutturale non causalmente collegata all'esito.

## 2. Esito competitivo

| Player | Final money |
|---|---:|
| Codex | $27,510 |
| Copilot | $37,752 |

Delta Copilot − Codex: **+$10,242**.  
Rapporto Copilot / Codex: **1.37×**.

## 3. Similarità strutturali — ciò che M2 NON discrimina bene

M2 è particolarmente utile perché le due policy condividono numerosi tratti:

- stessa apertura fino al Day 3;
- entrambi partono con $3,000;
- entrambi chiudono Day 0 a $928;
- entrambi raggiungono Q1 allo step 265 (Day 11 Hour 1);
- entrambi raggiungono max 10 hands;
- MOVE quasi identici: Codex 3,763 vs Copilot 3,768;
- WATER entrambi molto alti: Codex 475 vs Copilot 446;
- action count complessivo quasi identico: Codex 5,320 vs Copilot 5,297.

Questo rende M2 un test migliore di M1 per distinguere **qualità/composizione della capacità** da volume grezzo di azioni.

## 4. Working-set architecture

### Codex
- max active crops: **37**
- max pastures: **9**
- max animals: **7**
- max hands: **10**
- Q1: Day 11 Hour 1

### Copilot
- max active crops: **28**
- max pastures: **5**
- max animals: **4**
- max hands: **10**
- Q1: Day 11 Hour 1

Copilot vince con un working set fisicamente più piccolo.

Questa osservazione:
- indebolisce una lettura monotona di `crop_surface_maintained` come driver autonomo;
- supporta `state_capacity_alignment`, `throughput_to_cash_conversion` e `working_set_capacity_gate`;
- supporta la tesi Copilot secondo cui pasture/herd devono essere subordinate alla capacità reale del working set.

## 5. Action profile

| Action | Codex | Copilot |
|---|---:|---:|
| WATER | 475 | 446 |
| PLANT | 126 | 116 |
| HARVEST | 91 | 110 |
| CARE | 100 | 84 |
| FEED | 107 | 84 |
| COLLECT_FERTILIZER | 1 | 2 |
| DIG | 76 | 71 |
| MOVE | 3,763 | 3,768 |
| PASS | 172 | 154 |
| OTHER | 409 | 462 |

Azioni operative totali:
- Codex: **5,320**
- Copilot: **5,297**

Quota azioni produttive grezza:
- Codex: **18.35%**
- Copilot: **17.24%**

Quota MOVE:
- Codex: **70.73%**
- Copilot: **71.13%**

Final money / total action, usato solo come proxy:
- Codex: **$5.17/action**
- Copilot: **$7.13/action**

**Interpretazione neutrale:** Copilot non vince perché compie più azioni, più WATER o più crop maintenance. Vince pur avendo una quota produttiva grezza leggermente inferiore. M2 supporta quindi la distinzione tra **action volume/share** e **action monetization quality**.

## 6. Market architecture

### Requested market quantities — Codex
- BUY_SEED Wheat: 94
- BUY_SEED Melon: 34
- BUY_SEED Strawberry: 63
- BUY_PRODUCT Wheat: 1,334
- SELL Wheat: 1,143
- SELL Melon: 56
- SELL Strawberry: 30
- SELL Milk: 78
- SELL Fertilizer: 1
- BUY_ANIMAL: 10 Cow + 6 Sheep requests
- SELL market orders: 212

### Requested market quantities — Copilot
- BUY_SEED Wheat: 79
- BUY_SEED Melon: 73
- BUY_SEED Strawberry: 43
- BUY_PRODUCT Wheat: 1,828
- SELL Wheat: 1,767
- SELL Melon: 49
- SELL Strawberry: 52
- SELL Milk: 90
- SELL Fertilizer: 2
- BUY_ANIMAL: 4 Cow requests
- SELL market orders: 298

Le quantità sono **requested quantities**, non executed transaction ledger.

Differenze osservabili robuste:
- Copilot ha **298 SELL orders vs 212**;
- Copilot mostra un flusso Wheat buy/sell molto più intenso;
- Copilot monetizza più Strawberry requests (52 vs 30);
- Codex ha maggiore struttura zootecnica e maggiore crop footprint.

Non è lecito dedurre direttamente margini netti da questi dati.

## 7. Cash trajectory

Fine giornata selezionata:

| Day | Codex | Copilot | Copilot − Codex |
|---:|---:|---:|---:|
| 0 | 928 | 928 | 0 |
| 3 | 792 | 792 | 0 |
| 4 | 807 | 461 | -346 |
| 9 | 837 | 225 | -612 |
| 10 | 5,007 | 6,095 | +1,088 |
| 11 | 3,377 | 3,060 | -317 |
| 12 | 6,072 | 7,210 | +1,138 |
| 15 | 4,454 | 6,421 | +1,967 |
| 18 | 3,215 | 8,054 | +4,839 |
| 20 | 5,810 | 12,133 | +6,323 |
| 22 | 9,768 | 17,582 | +7,814 |
| 24 | 16,419 | 26,473 | +10,054 |
| 26 | 26,315 | 33,368 | +7,053 |
| 29 | 27,510 | 37,752 | +10,242 |

Il lead cambia più volte fino al Day 12:
- Copilot investe più aggressivamente prima;
- Codex mantiene più cash nei Days 4–9;
- Copilot prende il lead al Day 10;
- Codex lo riprende temporaneamente al Day 11;
- Copilot torna avanti al Day 12 e non perde più il vantaggio.

**M2 distingue quindi `operational_divergence_onset` da `economic_lock_in_onset`: il lock-in economico è circa Day 12 in questo match, non una costante universale.**

## 8. Livestock / pasture tradeoff

Day 18:
- Codex: 30 crops, 9 pasture, 7 Cow
- Copilot: 24 crops, 5 pasture, 4 Cow

Day 20:
- Codex: 31 crops, 9 pasture, 7 Cow
- Copilot: 27 crops, 5 pasture, 4 Cow

Nonostante la struttura Codex sia più grande, Copilot ha già un vantaggio di $4.8k–$6.3k.

Questo supporta:
- `pasture_arable_surface_tradeoff`;
- `pasture_to_livestock_alignment`;
- `livestock_headcount` dinamico/condizionale;
- working-set capacity gating.

Non dimostra che 4 animali siano universalmente ottimali.

## 9. Canonical concept classification — M2

| concept_id | M2 status | Evidenza / interpretazione |
|---|---|---|
| `land_surface_total` | NOT_DISCRIMINATED | Entrambi raggiungono gli stessi 2Q allo stesso step. |
| `land_purchase_timing` | NOT_DISCRIMINATED | Q1 identico: Day 11 Hour 1. |
| `activated_land_surface` | CONFOUNDED | Codex attiva più crop/pasture ma perde; superficie attivata da sola non spiega il risultato. |
| `crop_surface_maintained` | WEAKENED | Codex raggiunge 37 crop vs 28 Copilot e perde; non è sufficiente come driver monotono. |
| `maintained_productive_surface` | CONFOUNDED | La quantità mantenuta non coincide con il miglior outcome; conta la qualità economica del working set. |
| `monetized_productive_output` | SUPPORTED | Copilot ottiene più final money con working set e action volume più piccoli. |
| `land_activation_payback` | NOT_DISCRIMINATED | Stesso land unlock; nessuna differenza netta di branch. |
| `pasture_arable_surface_tradeoff` | SUPPORTED | Copilot preserva più superficie da pasture expansion e vince con herd più piccolo. |
| `workforce_headcount` | NOT_DISCRIMINATED | Entrambi max 10 hands. |
| `worker_capacity_available` | NOT_DISCRIMINATED | Capacità massima molto simile. |
| `marginal_hire_payback` | NOT_DISCRIMINATED | HIRE count identico (232 requests). |
| `productive_action_share` | WEAKENED | Codex ha share produttiva grezza superiore ma perde. |
| `movement_overhead` | NOT_DISCRIMINATED | MOVE e MOVE-share quasi identici. |
| `routing_completion_efficiency` | CONFOUNDED | Outcome diverso con action volume simile, ma manca effectiveness ledger. |
| `action_dispatch_failure` | NOT_DISCRIMINATED | Nessuna firma estrema tipo M1 Antigravity. |
| `worker_action_monetization_rate` | SUPPORTED | Proxy final-money/action: $7.13 Copilot vs $5.17 Codex. Ledger completo ancora mancante. |
| `watering_execution_rate` | NOT_DISCRIMINATED | Entrambi elevati: 475 vs 446; Codex irriga persino di più e perde. |
| `watering_continuity` | NOT_DISCRIMINATED | Entrambi mostrano elevata continuità. |
| `crop_care_completion_rate` | NOT_DISCRIMINATED | Nessun gap macroscopico comparabile a M1. |
| `crop_revenue_mix` | SUPPORTED | Copilot registra maggiore conversione Strawberry e SELL-order volume; supporto qualitativo. |
| `feed_availability` | CONFOUNDED | Entrambi usano forte market Wheat; nessuna misura netta del costo. |
| `feed_security_buffer` | CONFOUNDED | Copilot dichiara feed security ma usa più Wheat di mercato; possibile working-flow, non autarky dimostrata. |
| `feed_market_dependency` | CONFOUNDED | Copilot usa più BUY_PRODUCT Wheat e vince. Dipendenza non predice da sola il risultato. |
| `feed_market_expenditure` | INCONCLUSIVE | Manca executed transaction-value ledger. |
| `wheat_operating_flow` | SUPPORTED | Copilot mostra flusso Wheat molto più intenso e vince; supporta commodity-operating-flow, non profitto del churn. |
| `market_churn_cost` | INCONCLUSIVE | Churn alto, costo netto non osservabile. |
| `livestock_headcount` | SUPPORTED | Copilot vince con max 4 animali vs 7 Codex; supporta herd dinamico/compatto, non target 4 universale. |
| `livestock_capacity` | SUPPORTED | Copilot allinea herd a 5 pasture; Codex usa 9 pasture/7 animals. |
| `pasture_capacity_alignment` | SUPPORTED | Working set Copilot più compatto e coerente. |
| `livestock_product_flow` | CONFOUNDED | Entrambi monetizzano Milk; Copilot più SELL Milk requests ma causalità non isolata. |
| `species_margin_differential` | NOT_DISCRIMINATED | Copilot usa solo Cow; non testa margine Sheep vs Cow. |
| `fertilizer_byproduct_flow` | NOT_DISCRIMINATED | 1 vs 2 collection: troppo piccolo per discriminare. |
| `operating_cash_buffer` | CONFOUNDED | Copilot accetta cash molto più basso nei Days 4–9 e poi vince; un buffer maggiore non è monotonicamente migliore. |
| `deployable_capital_window` | SUPPORTED | Copilot investe presto, poi converte più rapidamente in crescita di cash; timing dinamico supportato. |
| `asset_liquidity_lag` | SUPPORTED | Le differenze early investment/cash precedono la crescita; payback non è immediato. |
| `inventory_to_cash_conversion` | SUPPORTED | Più SELL orders e maggiore final cash con working set più piccolo. |
| `reinvestment_cash_flow` | SUPPORTED | Dal Day 12 il vantaggio Copilot cresce in modo persistente. |
| `product_mix_revenue` | SUPPORTED | Copilot realizza un profilo di monetizzazione più frequente/diverso; valore preciso non quantificato. |
| `market_transaction_value` | INCONCLUSIVE | Non ricostruito nel report neutrale. |
| `state_capacity_alignment` | SUPPORTED | È il discriminante strutturale più coerente con M2. |
| `operational_divergence_onset` | SUPPORTED | Prime divergenze di stato/cash emergono Day 4. |
| `economic_lock_in_onset` | SUPPORTED | In M2 il vantaggio Copilot diventa permanente dal Day 12; non generalizzare la soglia. |
| `endgame_shutdown_timing` | CONFOUNDED | Entrambi scendono a 0 hands; differenze finali non isolate causalmente. |
| `endgame_inventory_liquidation` | INCONCLUSIVE | Restano semi/Wheat in entrambi; Copilot anche Milk in inventario worker finale. |
| `field_cleanliness_state` | NOT_DISCRIMINATED | Non emerge come discriminante economico primario. |
| `local_kaggle_fidelity_gap` | NOT_DISCRIMINATED | Non è un confronto local/Kaggle. |
| `final_money_outcome` | SUPPORTED | Outcome terminale valido: $37,752 vs $27,510. |

## 10. Neutral model verdict after M2

### Codex

M2 **non falsifica** il modello Codex, ma indebolisce alcune letture troppo aggregate:

- `productive_action_share` non discrimina;
- maggiore crop surface non garantisce monetizzazione superiore;
- maggiore watering non basta contro una policy che monetizza meglio;
- herd/pasture più ampi non producono un vantaggio;
- il modello resta forte su `worker_action_monetization_rate`, deployable capital, revenue breadth e state-capacity alignment, ma M2 mostra che Copilot li realizza meglio in questa seed.

**Verdetto M2 Codex:**  
`MODEL CORE PARTIALLY SUPPORTED / RELATIVE POLICY REALIZATION WEAKENED`.

### Copilot

M2 è fortemente coerente con i principali elementi ex ante del MODEL_SPEC Copilot:

- `throughput_to_cash_conversion` rank #1;
- `working_set_capacity_gate` rank #2;
- `crop_activation_and_monetization` rank #3;
- land non obbligatoria oltre il working set sostenibile;
- pasture/livestock allineati;
- fixed workforce e fixed herd target rifiutati;
- cash buffer come vincolo dinamico, non soglia rigida.

Due elementi richiedono cautela:
- `wheat_feed_security`: Copilot usa più market Wheat, quindi M2 non supporta una lettura forte di autarky/minima dipendenza;
- `operating_cash_buffer`: Copilot opera con cash inferiore a Codex per diversi giorni iniziali e vince, quindi conta la capacità di recupero/payback, non il buffer alto in sé.

**Verdetto M2 Copilot:**  
`MODEL DIRECTION SUBSTANTIALLY SUPPORTED / GENERALIZATION NOT YET ESTABLISHED`.

## 11. Post-M2 status

- Match integrity: **VERIFIED**
- Neutral forensic analysis: **COMPLETED**
- Independent Codex challenge: **PENDING**
- Independent Copilot challenge: **PENDING**
- Consensus synthesis: **PENDING**
- M3 authorization: **NO**
