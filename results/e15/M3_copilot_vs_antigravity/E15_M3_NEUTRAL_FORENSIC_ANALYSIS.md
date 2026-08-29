# E15 — M3 Neutral Forensic Analysis
## Copilot (P0) vs Antigravity (P1) — Seed 3122977751

**Stato:** analisi forense neutrale post-match  
**Esito:** Copilot **$26,629** vs Antigravity **$9,371** — delta **+$17,258 Copilot**  
**Durata:** 720 step  
**Principio:** Victory ≠ Model Validity; Defeat ≠ Model Falsification.

## 1. Integrità

Gli artefatti `match_metadata.json`, `summary.json`, `telemetry.json` e `raw_replay.json` sono presenti.

Il metadata conferma:
- Match `M3`
- seed `3122977751`
- Copilot P0 / Antigravity P1
- environment `0.1.0`
- submission Copilot SHA `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb`
- submission Antigravity SHA `629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d`
- ontology SHA `5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa`
- MODEL_SPEC Copilot SHA `d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686`
- MODEL_SPEC Antigravity SHA `f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46`

**Verdict integrità: `VALID_FOR_FORENSIC_ANALYSIS`.**

## 2. Finding centrale

M3 replica con notevole precisione il failure mode Antigravity osservato in M1.

Antigravity costruisce più capacità nominale:
- **3 quadranti** vs 2 Copilot;
- **max 12 hands** vs 9;
- **18 pasture** vs 5;
- **18 animali max** vs 4;
- ma soltanto **9 crop attivi max** vs 25 Copilot.

Contemporaneamente:
- WATER: **30 Antigravity vs 439 Copilot**
- HARVEST: **374 vs 113**
- FEED: **315 vs 84**
- MOVE: **5,047 vs 3,765**
- SELL orders: **198 vs 302**

Il risultato economico è $9,371 vs $26,629.

La spiegazione più parsimoniosa supportata dagli osservabili non è “Antigravity possiede troppo” in astratto, ma:

> **Antigravity converte capitale in asset/workforce/livestock più rapidamente di quanto riesca a convertire quella capacità in superficie crop mantenuta e monetizzata.**

Questa non è più soltanto una firma single-seed: M3 costituisce una **replica indipendente** della principale debolezza di policy realization emersa in M1.

## 3. Action profile

| Action | Copilot | Antigravity |
|---|---:|---:|
| WATER | 439 | 30 |
| PLANT | 115 | 100 |
| HARVEST | 113 | 374 |
| CARE | 84 | 283 |
| FEED | 84 | 315 |
| COLLECT_FERTILIZER | 0 | 15 |
| DIG | 62 | 97 |
| MOVE | 3,765 | 5,047 |
| PASS | 151 | 144 |
| OTHER | 461 | 656 |

Antigravity ripete la firma `HARVEST >> PLANT`: **3.74** contro circa **0.98** Copilot. Come in M1, ciò è una forte firma di dispatch/routing inefficiency; non dimostra che ogni HARVEST sia fallito.

## 4. Working set fisico

### Copilot
- Q1: step 265 = Day 11 Hour 1
- nessun Q2
- max hands: 9
- max active crops: 25
- max pasture: 5
- max animals: 4
- final herd: 4 Cow

### Antigravity
- Q1: step 217 = Day 9 Hour 1
- Q2: step 433 = Day 18 Hour 1
- max hands: 12
- max active crops: 9
- max pasture: 18
- max animals: 18
- final herd: 17 = 13 Cow + 4 Sheep

La divergenza è strutturale: Antigravity espande land/workforce/livestock prima e molto di più, ma mantiene una superficie crop drasticamente inferiore.

## 5. Cash trajectory

Daily end money:

| Day | Copilot | Antigravity |
|---:|---:|---:|
| 0 | 928 | 232 |
| 5 | 439 | 363 |
| 8 | 326 | 2,209 |
| 9 | 227 | 572 |
| 10 | 6,267 | 958 |
| 11 | 3,135 | 629 |
| 12 | 7,357 | 1,070 |
| 18 | 6,820 | 73 |
| 21 | 9,021 | 3,172 |
| 24 | 17,761 | 5,513 |
| 27 | 27,280 | 10,456 |
| 29 | 26,629 | 9,371 |

Il lead cambia più volte nella fase iniziale. Il vantaggio Copilot diventa **permanente allo step 252 = Day 10 Hour 12**, prima dell'acquisto Q1 Copilot e molto prima del Q2 Antigravity.

Quindi il Q2 Antigravity non causa l'inizio del failure: è piuttosto coerente con una successiva amplificazione di un disallineamento già visibile.

## 6. Market requests

Quantità richieste, **non automaticamente quantità eseguite o revenue**.

### Copilot
- BUY_PRODUCT Wheat: 1,889
- SELL Wheat: 1,831
- SELL Melon: 58
- SELL Strawberry: 54
- SELL Milk: 90
- BUY_ANIMAL Cow: 4
- SELL orders: 302

### Antigravity
- BUY_PRODUCT Wheat: 904
- SELL Wheat: 774
- SELL Milk: 218
- SELL Wool: 91
- SELL Fertilizer: 12
- BUY_ANIMAL Cow: 14
- BUY_ANIMAL Sheep: 4
- SELL orders: 198

Copilot presenta ancora un intenso Wheat operating flow. Antigravity monetizza prodotti livestock diversificati, ma ciò non compensa il gap nella macchina crop/cash complessiva.

## 7. Concept discrimination

| concept_id | Verdict M3 | Motivazione |
|---|---|---|
| `land_surface_total` | WEAKENED | Antigravity possiede 3Q e perde nettamente contro 2Q. Più land non è driver monotono. |
| `land_purchase_timing` | WEAKENED | Antigravity compra Q1 prima e Q2; il vantaggio Copilot diventa permanente prima del suo Q1. Early unlock non è sufficiente. |
| `activated_land_surface` | CONFOUNDED | Ownership e pasture non equivalgono a crop activation. |
| `crop_surface_maintained` | SUPPORTED | 25 crop max Copilot vs 9 Antigravity, insieme a 439 vs 30 WATER. |
| `maintained_productive_surface` | SUPPORTED | Replica M1: capacità nominale Antigravity non diventa working crop surface mantenuta. |
| `monetized_productive_output` | SUPPORTED | Copilot chiude quasi 2.84× Antigravity. |
| `land_activation_payback` | SUPPORTED | Antigravity compra prima/più land senza ritorno comparabile. |
| `pasture_arable_surface_tradeoff` | SUPPORTED | 18 pasture Antigravity vs 5 Copilot con crop surface 9 vs 25. |
| `workforce_headcount` | WEAKENED | 12 hands Antigravity vs 9 Copilot; più workforce non basta. |
| `worker_capacity_available` | CONFOUNDED | Capacità nominale maggiore ma utilizzo economico peggiore. |
| `marginal_hire_payback` | SUPPORTED | Workforce extra Antigravity non mostra payback relativo nel match. |
| `productive_action_share` | WEAKENED | Volume grezzo di azioni di cura/raccolta/feed non implica monetizzazione. |
| `movement_overhead` | SUPPORTED | Antigravity 5,047 MOVE vs 3,765; a differenza di M2 qui discrimina nettamente. |
| `routing_completion_efficiency` | SUPPORTED | Firma HARVEST/PLANT e movement coerente con inefficienza di completion. |
| `action_dispatch_failure` | SUPPORTED | HARVEST/PLANT 3.74 Antigravity vs ~0.98 Copilot replica M1. |
| `worker_action_monetization_rate` | SUPPORTED | Final money per action favorisce fortemente Copilot; proxy macro, non ledger marginale. |
| `watering_execution_rate` | SUPPORTED | 439 vs 30: M3 ricade nel regime “sotto soglia” già osservato in M1. |
| `watering_continuity` | SUPPORTED | La differenza di volume è troppo ampia per essere spiegata da ottimizzazione marginale. |
| `crop_revenue_mix` | SUPPORTED | Copilot mantiene crop monetizzabili; Antigravity è fortemente livestock-oriented. |
| `feed_market_dependency` | CONFOUNDED | Copilot compra più Wheat e vince; dipendenza market non è automaticamente negativa. |
| `wheat_operating_flow` | SUPPORTED | 1,889 BUY / 1,831 SELL requests Copilot. Non prova profitto del churn. |
| `market_churn_cost` | INCONCLUSIVE | Manca executed transaction-value ledger. |
| `livestock_headcount` | WEAKENED | 18 max Antigravity vs 4 Copilot; herd grande non è sufficiente. |
| `livestock_capacity` | WEAKENED | Grande capacità livestock compete con crop/worker/cash capacity. |
| `pasture_capacity_alignment` | SUPPORTED | Copilot mantiene subsystem compatto; Antigravity alloca 18 pasture. |
| `livestock_product_flow` | CONFOUNDED | Antigravity vende Milk/Wool/Fertilizer ma perde; flow presente, marginal value non isolato. |
| `species_margin_differential` | NOT_DISCRIMINATED | Nessun confronto causale pulito. |
| `fertilizer_byproduct_flow` | WEAKENED | Presente Antigravity ma non è differenziatore sufficiente. |
| `operating_cash_buffer` | SUPPORTED | Antigravity arriva a $73 Day18 durante la seconda espansione; forte pressione di capitale. |
| `deployable_capital_window` | SUPPORTED | Copilot entra nel regime di cash generation sostenuta prima. |
| `asset_liquidity_lag` | SUPPORTED | Asset expansion Antigravity anticipa ritorni e comprime cash. |
| `inventory_to_cash_conversion` | SUPPORTED | 302 SELL orders Copilot vs 198; con cautela sulle esecuzioni. |
| `reinvestment_cash_flow` | SUPPORTED | Copilot crea un ciclo cash crescente dopo Day10. |
| `product_mix_revenue` | SUPPORTED | Mix crop+Milk Copilot supera economicamente mix livestock-heavy Antigravity; valori non decomposti. |
| `market_transaction_value` | INCONCLUSIVE | Manca ledger eseguito. |
| `state_capacity_alignment` | SUPPORTED | Concetto strutturale più forte: working set Copilot è molto più coerente con capacità di manutenzione/monetizzazione. |
| `operational_divergence_onset` | SUPPORTED | La divergenza operativa precede il lock-in monetario. |
| `economic_lock_in_onset` | SUPPORTED | Copilot avanti permanentemente da step 252 / Day10 Hour12. |
| `endgame_shutdown_timing` | CONFOUNDED | Non spiega un gap formatosi molto prima. |
| `endgame_inventory_liquidation` | INCONCLUSIVE | Non isolato causalmente. |
| `field_cleanliness_state` | CONFOUNDED | Weeds esistono in entrambi; non emerge come causa primaria. |
| `local_kaggle_fidelity_gap` | NOT_DISCRIMINATED | Match locale frozen; nessun confronto Kaggle. |
| `final_money_outcome` | SUPPORTED | $26,629 vs $9,371. |

## 8. Cross-match replication: M1 vs M3

La replica è forte:

| Firma Antigravity | M1 | M3 |
|---|---:|---:|
| WATER | 34 | 30 |
| HARVEST | 414 | 374 |
| FEED | 309 | 315 |
| MOVE | 5,019 | 5,047 |
| max pasture | 18 | 18 |
| max animals | 18 | 18 |
| final herd | 17 | 17 |
| quadranti | 3 | 3 |
| final money | $8,672 | $9,371 |

Questa stabilità è molto più informativa del solo record 0–2.

**Inference:** la submission Antigravity realizza in modo sistematico una policy di grande scala livestock/territory/workforce con watering crop estremamente basso e forte dispatch/movement load. Il failure mode osservato in M1 è quindi **replicato in M3 su seed e avversario differenti**.

Questo rafforza soprattutto un verdetto di **POLICY_REALIZATION / IMPLEMENTATION_FIDELITY**, non autorizza da solo a dichiarare falso l'intero MODEL_SPEC Antigravity.

## 9. Model verdict preliminari

### Antigravity
**MODEL_VALIDITY: PARTIALLY_SUPPORTED**  
**POLICY_REALIZATION: STRONGLY_WEAKENED**  
**IMPLEMENTATION_FIDELITY: STRONGLY_WEAKENED**

M3 replica esattamente la frattura già osservata in M1 tra modello dichiarato e policy realizzata: la teoria attribuisce alta priorità a irrigation dispatch e compounded throughput, ma la submission realizza 30 WATER, 18 pasture/18 animals, 3Q e 12 hands con solo 9 active crops max.

La replica indipendente rende questa diagnosi molto più robusta.

### Copilot
**MODEL_VALIDITY: SUBSTANTIALLY_SUPPORTED**  
**GENERALIZATION: PARTIALLY_SUPPORTED, NOT ESTABLISHED**

Copilot vince M2 e M3 con la stessa architettura compatta e state-gated. M3, diversamente da M2, testa anche il regime di avversario sotto-soglia e conferma che Copilot mantiene watering/crop surface senza inseguire la scala nominale Antigravity.

Due seed vincenti migliorano la generalizzazione relativa rispetto a M2, ma non equivalgono a validazione multi-seed sistematica.

## 10. Implicazione E15

Il risultato competitivo è definitivo:

- Copilot: **2–0**
- Codex: **1–1**
- Antigravity: **0–2**

Nessun tie-break necessario.

Tuttavia la chiusura epistemica E15 richiede ancora:
1. challenge indipendente Copilot su M3;
2. challenge indipendente Antigravity su M3;
3. consensus M3;
4. doppio ACK;
5. solo dopo, sintesi finale E15 e deltas post-tournament.

**M3 non è ancora CLOSED. E15 non è ancora epistemicamente CLOSED.**
