# Kaggriculture Parametric Strategy Model

## 1. Identita del modello

- Versione corrente: `X1.12`, baseline candidate per competitive learning.
- Strategy class / mode sorgente: `ProductiveMassROIAgent` con `ProductiveMassConfig.productive_core_mode="E12_TRUEBELIEF_ENGINE_X112"`.
- Standalone submission: `experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`, generata da `scripts/build_submission.py` dallo stesso sorgente.
- Benchmark locale corrente: seed `0` = `$42,491`; seed `421521921` = `$48,313`.
- Benchmark esterno: uploaded — result pending.
- Descrizione submission caricata: `E12-X1.12 Truebelief Engine — Q0+Q1, 7 Cow + 4 Sheep, competitive replay baseline`.
- Obiettivo primario: massimizzare `final_money`, con benchmark di ricerca corrente `final_money >= 80,000` su seed `0` e `421521921`.
- Correzione modello post-upload: `7 Cow / 4 Sheep` e `Q0+Q1 only` sono proprieta osservate/verificate della submission X1.12 e del riferimento truebelief, non vincoli strategici universali.

## Reference Trajectory vs Policy Target

Una traiettoria competitiva osservata fornisce evidenza, non target da riprodurre. truebelief `7 Cow / 4 Sheep`, truebelief Q1 Day 11, altri competitor con mix livestock o numero di Hands osservato sono `OBSERVED_REFERENCE` finche una regola generalizzata non migliora il modello nei VERIFY multi-seed e nella validazione Kaggle.

Un valore diventa `ADOPTED` solo dopo che il delta del modello e stato espresso come trigger parametrico, implementato, verificato localmente e confrontato con evidenza esterna. La policy deve distinguere benchmark osservato da regola generalizzabile.

## 2. Variabili di stato utilizzate dalla policy

La policy X1.12 usa `step`, `day + 1`, `hour`, `money`, `unlocked_quadrants`, posizione farmer, posizioni hands, numero di hands attive, tile possedute, tile libere, crop tile e pasture tile. Per le colture legge `kind`, `crop`, `watered_today`, `consecutive_unwatered`, `yield_units` e weed. Per il livestock legge pasture con `animal`, `fed_today`, `cared_today`, `yield_units`, `fertilizer_available`, piu animali nello shed e negli inventari worker.

Usa inoltre `private.shed`, `private.seeds`, `private.inventories`, prezzi correnti via `get_price`, conteggi virtuali di semi/crop durante l'assegnazione, set `reserved` per evitare collisioni fra worker nello stesso turno, telemetry interna, `owned_quadrants` interno e valori configurati nella submission X1.12 `target_cows=7`, `target_sheep=4`, `max_workers=6`, `stop_hire_day=1`. Dopo la correzione post-upload questi valori sono trattati come baseline implementata, non come target universali.

Variabili da misurare nel prossimo BUILD per de-hardcodare livestock e Q2: workload crop pendente, backlog weeds, tile harvested-empty, tile non watered, capacita worker residua, feed workload, care workload, harvest livestock workload, pickup/place/drop/logistics workload, cash / working capital, remaining horizon, marginal expected value del prossimo animale, utilizzo economico effettivo Q0+Q1, costo Q2, tempo stimato di attivazione Q2 e opportunity cost rispetto a crop/livestock/worker investment.

## 3. Fasi strategiche

X1.12 non implementa una macchina a stati esplicita: usa soglie su giorno, quadranti, cash e superficie attiva.

- Day 1: acquisto iniziale di `18 WHEAT`, `11 MELON`, `10 STRAWBERRY`; target workforce Q0 a 5 hands; costruzione pasture e semina iniziale tramite routing generico. La funzione `_x112_opening_action` esiste, ma non e collegata alla decisione X1.12 corrente.
- Pre-Q1, Day 2-10: resta in Q0; target crop mix `6 WHEAT / 8 MELON / 7 STRAWBERRY`; target pasture 4; cow ramp a 1 da Day 5 e 2 da Day 9.
- Q1 expansion: compra Q1 a `day >= 10`, `hour == 0`, cash `>= 1000`, se non ha ancora 2 quadranti.
- Q1 buildout: da Day 11 aumenta target cows fino a 7; da Day 12 abilita sheep target fino a 4; target pasture massimo 11; target crop cambia con orizzonte residuo.
- Endgame: da Day 28 liquida tutto il Wheat nello shed; da Day 29 desired hands va a 0; non pianta nuovi crop da Day 28.

## 4. Regole decisionali: trigger e target

| Decisione | Trigger | Target / parametro corrente | Fonte dell'evidenza | Stato |
|---|---|---|---|---|
| Acquisto iniziale semi | `state.step == 0` | `18 WHEAT`, `11 MELON`, `10 STRAWBERRY` | `src/agricola/strategy/productive_mass_roi.py` | IMPLEMENTED |
| HIRE | `hour == 0` e hands attive < desired | Q0: 5; Q1 Day <=12: 6; Day 13: 9; Day 14-18: 10; Day 19-28: 11 o 12 nei giorni 20/22/24; Day >=29: 0 | `_x112_desired_hands` | IMPLEMENTED |
| Acquisto Q1 | `owned_quadrants < 2`, `day >= 10`, `hour == 0`, cash `>= 1000` | Solo Q0+Q1 nel candidato | `_decide_e12_truebelief_engine_x112` e verify X1.12 | TESTED |
| Crop allocation Q0 | `owned < 2` | `6 WHEAT`, `8 MELON`, `7 STRAWBERRY` | `_x112_target_crop_counts` | IMPLEMENTED |
| Crop allocation Q1 early | `owned >= 2`, Day <=17 | `10 WHEAT`, `10 MELON`, `19 STRAWBERRY` | `_x112_target_crop_counts` | IMPLEMENTED |
| Crop allocation mid | Day 18-20 | `17 WHEAT`, `10 MELON`, `12 STRAWBERRY` | `_x112_target_crop_counts` | IMPLEMENTED |
| Crop allocation late | Day 21-24 | `18 WHEAT`, `25-day MELON floor`, `12 STRAWBERRY` | `_x112_target_crop_counts` | IMPLEMENTED |
| Crop allocation end | Day 25-27, Day >=28 | Day 25-27: `18 WHEAT`, `12 STRAWBERRY`; Day >=28: `8 WHEAT` target, no planting | `_x112_target_crop_counts`, worker planting guard | IMPLEMENTED |
| Pasture construction | Missing target pasture and tile empty | 4 pasture through Day 10; then `min(11, max(4, target_cows + target_sheep))` | `_x112_worker_action`, `_x112_crop_positions` | IMPLEMENTED |
| Cow acquisition | Pasture exists, cash >= cost + reserve | Day 5: 1; Day 9: 2; Day 11+ Q1: 7, capped by config; buy qty max 5 | `_decide_e12_truebelief_engine_x112` | IMPLEMENTED |
| Sheep acquisition | Q1, pasture >=6, active crops >=20, cash gate | Day 12+ target up to 4, capped by config; buy qty max 5 | `_decide_e12_truebelief_engine_x112` | IMPLEMENTED |
| Retail Wheat | Day >=10, projected wheat below need, cash >=80 | `wheat_need=max(8, animal_tiles*3+8)`, buy up to 14 | `_decide_e12_truebelief_engine_x112` | IMPLEMENTED |
| Feed provisioning | Unfed animal exists, worker has no wheat | Pickup Wheat from shed, up to 6, when inventory empty | `_x112_worker_action` | IMPLEMENTED |
| FEED | Worker carries Wheat and target animal is unfed | Nearest reserved unfed animal | `_x112_worker_action` | IMPLEMENTED |
| CARE | Animal fed and not cared | Nearest reserved careable animal, before harvest | `_x112_worker_action` | IMPLEMENTED |
| Animal HARVEST | Pasture animal has `yield_units > 0` | Nearest ready animal | `_x112_worker_action` | IMPLEMENTED |
| Fertilizer collection | Fertilizer available, worker is a hand, Day >=16 | Nearest ready pasture after crop tasks | `_x112_worker_action` | IMPLEMENTED |
| Product logistics | Worker carries Milk/Wool/Fertilizer/crops or excess Wheat | Return to shed cluster `(4,4),(5,4),(4,5),(5,5)` and `PLACE` items | `_x112_worker_action` | IMPLEMENTED |
| SELL | Product count in shed > 0 | Sell all `MILK`, `WOOL`, `FERTILIZER`, `MELON`, `STRAWBERRY`, `CARROT`, `TOMATO`; sell excess Wheat | `_decide_e12_truebelief_engine_x112` | IMPLEMENTED |
| Worker routing | Every unit receives nearest feasible reserved target | Priority: place carried goods, place animals, pickup/feed, care, animal harvest, pasture build, crop harvest/water/dig/plant, fertilizer, care fallback | `_x112_worker_action` | IMPLEMENTED |
| Weed recovery | Crop task loop sees `kind == WEED` | `DIG` nearest reserved weed inside crop positions | `_x112_worker_action` | IMPLEMENTED |
| Endgame liquidation | Day >=28 | Sell all shed Wheat; no new planting from Day 28; no desired hands from Day 29 | X1.12 decision code | TESTED |
| truebelief reference trajectory | Episode `101294736` | Day-1 diversified opening, delayed Q1, Cow + Sheep, Milk/Wool/Fertilizer monetization | raw replay and parsed benchmark | OBSERVED_REFERENCE |
| Livestock capacity gate | Prossimo BUILD: valore marginale atteso animale > costo marginale complessivo e capacita residua sufficiente | Crescere livestock solo se crop SLA resta mantenibile | prime evidenze esterne X1.12 + diagnosi crop degradation | INFERRED |
| Q2 conditional expansion | Prossimo BUILD: expected value Q2 > costo terreno + working capital + costo operativo, con workforce sufficiente | Q2 non vietato; BUY_Q2 solo se payback stimato entro horizon e Q0+Q1 non degrada materialmente | prime osservazioni esterne di competitor con Q2 | INFERRED |

## 5. Obiettivi economici e vincoli

Formula ottimizzata localmente: final money dell'ambiente, letto dal reward finale. Non esiste una formula esplicita di payback per investimento; il codice implementa soglie e riserve operative.

Cash reserve implementate: `crop_engine_reserve=2600` quando Q1 e Day <=15 con meno di 35 crop attivi, altrimenti `100`; `animal_reserve=max(crop_engine_reserve, 450 se Q0 altrimenti 100)`; sheep reserve `800` fino a Day 16, poi `100`; retail Wheat mantiene buffer `max(8, animal_tiles*3+8)`. Wheat shed reserve e `max(6, animal_tiles*2+2)`, salvo liquidazione Day >=28.

Crop ROI e contribution non sono calcolati come valore atteso per tile; sono rappresentati da target crop horizon-aware. Livestock economics nella submission X1.12 sono rappresentate da valori configurati cows/sheep, feed buffer, vendita immediata di Milk/Wool/Fertilizer e priorita FEED/CARE/HARVEST. La regola concettuale corretta e `INFERRED`: il livestock puo crescere solo finche il suo valore marginale atteso rimane superiore al costo marginale complessivo e la capacita operativa residua e sufficiente a mantenere il motore crop entro gli SLA di manutenzione.

Il costo marginale worker non e stimato dinamicamente: il modello usa una schedule desired hands per giorno/quadrante. La submission X1.12 compra solo Q1 e lavora tile con `y < 5`, ma `Q0+Q1 only` non e piu un hard constraint permanente. La regola Q2 corretta e `INFERRED`: `BUY_Q2` soltanto quando il valore marginale atteso della nuova superficie supera costo del terreno + working capital + costo operativo di attivazione, e quando la workforce puo mantenere la nuova superficie senza degradare materialmente Q0+Q1.

## 6. Target di benchmark correnti

### Target hard di ottimizzazione

- seed `0`: `>= 80,000`
- seed `421521921`: `>= 80,000`
- source/submission behavioral equivalence
- provenance e riproducibilita

### Baseline X1.12 corrente

- seed `0`: `$42,491`
- seed `421521921`: `$48,313`
- land osservato nella submission X1.12: `Q0+Q1 only`
- livestock osservato nella submission X1.12: `7 Cow / 4 Sheep`
- `Q0+Q1 only`, `7 Cow`, `4 Sheep`, crop mix specifico e numero fisso di Hands non sono hard constraint strategici permanenti.

### Riferimento competitivo

- replay truebelief episodio `101294736`
- seed `421521921`
- final money `$86,297`

Il target hard non e stato raggiunto.

## 7. Diagnosi strutturale corrente

Fatto misurato: X1.12 riproduce l'ordine di grandezza livestock del riferimento, con `7 Cow / 4 Sheep` totali, e migliora X1.11 sui due seed locali. Fatto misurato: resta molto sotto truebelief sul seed `421521921` (`$48,313` contro `$86,297`). Interpretazione corrente: la superficie crop produttiva e il throughput dopo Q1 sono il principale collo di bottiglia. Movement, FEED/CARE, animal HARVEST, PICKUP/PLACE e market timing assorbono capacita operativa che non viene convertita abbastanza in planting/watering Q1.

La prossima ottimizzazione deve concentrarsi su routing e assignment throughput prima di cambiare costanti economiche arbitrarie.

Evidenza esterna iniziale post-upload e benchmark batch: nelle prime partite Kaggle X1.12 la strategia mostra forte concentrazione livestock, crop surface ridotta nel mid/late game, weeds e tile vuote; i replay competitivi analizzati nel batch `docs/benchmark` raggiungono `$86,297` e `$90,137` senza Q2, e `101717011` batte la nostra policy `$50,420` contro `$24,314` restando su un solo quadrante. Interpretazione `INFERRED`: il modello deve allocare dinamicamente capitale, superficie e capacita worker fra crop, livestock, logistica ed eventuale espansione territoriale sulla base di rendimento marginale e backlog operativo.

## 8. Evidenze di riferimento

- Raw replay: `experiments/archive/e12/artifacts/x111/101294736.json`
- SHA-256: `6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695`
- Parser / benchmark replay: artifact in `results/e12/x111`
- Summary: `experiments/archive/e12/artifacts/x111/TRUEBELIEF_BENCHMARK.md`
- Machine-readable benchmark: `experiments/archive/e12/artifacts/x111/truebelief_benchmark.json`
- Timeline comparativa: `experiments/archive/e12/artifacts/x111/x111_truebelief_comparison_timeline.csv`
- Counterfactual X1.12: `experiments/archive/e12/artifacts/x112/COUNTERFACTUAL_LOG.md`
- Verifica submission candidate: `experiments/archive/e12/artifacts/x112/submission_candidate_verification.json`

L'evidenza raw primaria ha precedenza sulle sintesi derivate.

## 9. Protocollo quotidiano di training / competitive learning

Nel progetto, "training" significa aggiornare trigger, target e regole decisionali in modo esplicito e verificabile sulla base di nuove evidenze competitive. Non vengono addestrate reti neurali e non vengono aggiornati pesi mediante backpropagation. L'unita di apprendimento e il delta del modello decisionale, tracciato da evidenza a risultato.

1. Identificare un competitor forte per la giornata.
2. Individuare un episodio Kaggle utile.
3. Acquisire e conservare integralmente il raw replay senza trasformazioni.
4. Registrare episode ID, competitor, seed, reward, data di acquisizione, URL sorgente e SHA-256.
5. Trasformare il replay nel formato benchmark machine-readable canonico.
6. Confrontare la traiettoria del competitor con il modello corrente.
7. Individuare solo divergenze strutturali ad alto impatto.
8. Aggiornare prima `MODEL_SPEC.md` con evidenza, ipotesi, modifica proposta ed effetto atteso.
9. Implementare nel codice esclusivamente il delta del modello approvato.
10. Eseguire VERIFY sui seed standard e su validation seed quando utile.
11. Costruire e verificare la standalone submission.
12. L'utente effettua manualmente l'upload su Kaggle.
13. Registrare il risultato esterno.
14. Il giorno successivo usare, quando possibile, un competitor differente.

## 10. Disciplina di aggiornamento del modello

Ogni modifica quotidiana deve seguire:

`Evidence -> Hypothesis -> Model delta -> Code delta -> Local VERIFY -> Kaggle result`

Non passare direttamente dall'osservazione del competitor a imitazione hardcoded. Non codificare `BUY Q1 on Day 11` solo perche truebelief lo ha fatto; preferire trigger economici e operativi. Non codificare un numero fisso di hands come universale; derivare quando possibile la workforce da workload e throughput.

## 11. Model Change Log

| Data | Versione modello | Competitor / episodio di riferimento | Evidenza | Modifica al modello | Locale prima | Locale dopo | Risultato Kaggle | Verdetto |
|---|---|---|---|---|---:|---:|---|---|
| 2026-08-28 | X1.11 -> X1.12 | truebelief / `101294736` | Day-1 diversified opening, delayed Q1, Cow + Sheep, Milk/Wool/Fertilizer monetization; raw SHA-256 `6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695` | Nuovo mode `E12_TRUEBELIEF_ENGINE_X112` con Q0+Q1, livestock+crops, Wheat feed buffer, monetizzazione Milk/Wool/Fertilizer, target crop horizon-aware e routing multi-worker | seed 0 `$29,858`; seed 421521921 `$24,827` | seed 0 `$42,491`; seed 421521921 `$48,313` | PENDING | LOCAL IMPROVEMENT / 80K GATE FAIL / EXTERNAL VALIDATION PENDING |
| 2026-08-28 | X1.12 model correction | truebelief / `101294736` + prime osservazioni Kaggle X1.12 | truebelief aveva mostrato `7 Cow / 4 Sheep` e Q0+Q1; prime osservazioni esterne X1.12 mostrano sovraconcentrazione livestock e degrado crop surface; competitor competitivi osservati usano anche Q2 | livestock target -> capacity/ROI-gated; Q2 forbidden -> economically/operationally gated | n/a | n/a | PENDING | INFERRED / DA IMPLEMENTARE E TESTARE NEL PROSSIMO BUILD |
| 2026-08-28 | X1.13 verification build | X1.12 baseline + corrected model | Dynamic livestock/Q2/capacity allocation tested on seed `0` and `421521921`; artifacts in `results/e12/x113` | Nuovo mode `E12_DYNAMIC_ALLOCATION_X113`; variants B-E testano livestock gate, workload HIRE, dynamic Q2 gate e crop-SLA assignment | X1.12: `$42,491 / $48,313` | Best X1.13 variant B: `$34,230 / $30,389` | n/a | TESTED / REJECTED FOR ADOPTION / STRUCTURAL CEILING MEASURED |
| 2026-08-28 | Competitive Benchmark Batch #1 | truebelief / `101294736`; Dr. Mikholae Hutchinson / `101705751`; Alexander Sokolov / `101717011` | Competitor `$86,297`, `$90,137`, `$50,420`; all avoid Q2; Sokolov beats our `$24,314` with one quadrant; peak hands `12`, `10`, `8`; peak productive tiles `50`, `46`, `15`; livestock `9 Cow / 5 Sheep`, `7 Cow / 4 Sheep / 2 Goose`, `4 Cow / 2 Sheep`; broad Milk/Fertilizer/Wool/crop selling | MODEL UPDATE only: reinforce throughput/workforce/capital deployment hypotheses; downgrade Q2 from near-term target to conditional option; downgrade Q1 from invariant to payback-gated expansion; reject fixed livestock and fixed hand counts as universal targets | n/a | n/a | n/a | BENCHMARK BATCH ANALYZED / CODE DELTA NOT STARTED |
| 2026-08-28 | X1.14 fast workforce build | Benchmark Batch #1 + X1.12 baseline | Variants B-F test preventive HIRE, crop maintenance priority, Q1-protected workforce and livestock brake; weeds improve but final money regresses on required seeds | Nuovo mode `E12_WORKFORCE_CAPACITY_X114`; no standalone rebuild because no variant beats X1.12 on both seed `0` and `421521921` | X1.12: `$42,491 / $48,313` | Best X1.14 required-seed variant B/D: `$39,301 / $36,238` or `$31,744 / $35,654`; seed `1273000467` B improves `$54,228` vs `$43,021` | n/a | IMPLEMENTED / TESTED / REJECTED / DO NOT UPLOAD |

## 12. X1.13 Verify Results

Mode implemented: `E12_DYNAMIC_ALLOCATION_X113`.

Counterfactual artifacts:

- `experiments/archive/e12/artifacts/x113/IMPLEMENTATION_DELTA.md`
- `experiments/archive/e12/artifacts/x113/COUNTERFACTUAL_LOG.md`
- `experiments/archive/e12/artifacts/x113/counterfactual_results.json`
- `experiments/archive/e12/artifacts/x113/counterfactual_results.csv`

Status by rule:

| Rule | Implementation status | Verify status | Adoption status |
|---|---|---|---|
| Livestock capacity/ROI gate | IMPLEMENTED | TESTED | REJECTED |
| Workload-based HIRE | IMPLEMENTED | TESTED | REJECTED |
| Dynamic Q2 gate | IMPLEMENTED | TESTED | NOT ADOPTED; gate did not fire |
| Crop-SLA-first assignment | IMPLEMENTED | TESTED | REJECTED |

Measured outcome:

- X1.12 baseline A: seed `0` `$42,491`, seed `421521921` `$48,313`.
- Best X1.13 tested variant B: seed `0` `$34,230`, seed `421521921` `$30,389`.
- Variant B improved crop surface (`mean 21.53`, `peak 37`) and reduced weed/unwatered tile-days, but suppressed livestock to `0 Cow / 0 Sheep` and lost too much Milk/Wool/Fertilizer cash conversion.
- Variants C/D/E collapsed below `$10,000` on at least one required seed.
- Q2 was not purchased in any variant, so Q2 is still an inferred opportunity requiring a better activation/payback gate, not a rejected expansion concept.

Conclusion: `X1.13 STRUCTURAL CEILING: MEASURED`. The tested dynamic allocation rules are not adopted into the Kaggle candidate.

## 13. Competitive Benchmark Batch #1

### Benchmark Evidence Base

Primary replay evidence:

| Episode | Seed | Competitor | Our reward | Competitor reward | Replay SHA-256 |
|---|---:|---|---:|---:|---|
| `101294736` | `421521921` | `truebelief` | `$6,825` | `$86,297` | `6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695` |
| `101705751` | `1056561958` | `Dr. Mikholae Hutchinson` | `$38,815` | `$90,137` | `79be341c03a5f471baaa28cf6419ff89d85c06fc88de50901c5c1e3da92ac6b3` |
| `101717011` | `1273000467` | `Alexander Sokolov` | `$24,314` | `$50,420` | `f298356ebe1bf9e7aad4acff32a6114db4f015f90f613e8e913565913494f3b9` |

Derived analysis artifacts are in `results/benchmark`: `BENCHMARK_REGISTRY.md`, `benchmark_registry.json`, per-episode daily timelines, consolidated daily timeline and `q2_evidence.json`. Raw replay JSON remains unchanged in `docs/benchmark`.

### Cross-Competitor Invariants

Patterns supported by the replay competitors:

- All three competitors avoid Q2. Q2 is not supported as a near-term required target by this batch.
- Land expansion is not invariant: truebelief and Dr. Mikholae Hutchinson use Q1; Alexander Sokolov beats our two-quadrant run while staying in `NW`.
- Productive capacity must be maintainable and monetizable. The elite Q0+Q1 runs peak at `50` and `46` productive tiles; the compact one-quadrant win peaks at only `15`.
- Backlog control is decisive for elite scores: the >86k replays show weed tile-days `10` and `11`, while our side in episode `101705751` accumulates `158`.
- Workforce is state-dependent: peak hands are `12`, `10` and `8`, so the invariant is throughput fit, not a copied count.
- All competitors monetize multiple channels instead of a single crop/livestock path: Fertilizer, Milk, Wheat and premium crops are visible in sold-product totals.
- All competitors combine crop engine and livestock engine; livestock is valuable but appears as part of a throughput system, not as an isolated fixed target.

### Conditional Behaviors

- Livestock mix varies: truebelief ends with `9 Cow / 5 Sheep`; Dr. Mikholae Hutchinson ends with `7 Cow / 4 Sheep / 2 Goose`; Alexander Sokolov ends with `4 Cow / 2 Sheep`.
- Peak hands vary between `8` and `12`; the model should derive workforce from workload, travel, backlog and horizon, not copy a constant.
- Crop mix varies by seed and market. truebelief sells large Wheat/Melon/Milk/Fertilizer volumes; Dr. Mikholae Hutchinson sells more Fertilizer/Milk/Strawberry/Egg.
- Q1 timing and usage vary: Day 11, Day 14, or no Q1. This supports an economic/operational gate rather than a calendar-only trigger.
- Wheat remains operational commodity and sale product, but overproducing/selling Wheat alone is not sufficient when crop surface and livestock monetization lag.

### Rejected Hard Targets

- `7 Cow / 4 Sheep` is rejected as a universal livestock target. It remains `OBSERVED_REFERENCE` for X1.12 and one competitor-like trajectory, while the batch shows stronger alternatives with additional Cow/Sheep and Goose.
- `Q0+Q1 only` is rejected as a permanent rule but confirmed as sufficient for two strong replays. `Q0 only` is also competitive enough to beat us in `101717011`, so expansion must be payback-gated.
- Fixed peak Hands values are rejected. `10`, `12`, and X1.12 schedule values are reference points for a workload function.
- Fixed Q1 Day 11 is rejected. Day 11, Day 14 and no-Q1 are all observed outcomes, so Q1 must be state/payback gated.
- Fixed crop allocation counts are rejected. The invariant is maintained productive surface with low weeds and sellable output, not a literal crop vector.

### Current Model Hypotheses

- `Deployable Capital` (`INFERRED`): cash that can be converted into productive capacity within the remaining horizon, net of working capital, travel cost, maintenance workload and payback. It is distinct from raw cash and can argue against Q1 when one-quadrant monetization is stronger.
- `Workforce Throughput Gate` (`INFERRED`): HIRE target should be a function of active crop tiles, livestock care/feed/harvest tasks, logistics distance, weeds/unwatered backlog and remaining horizon.
- `Crop SLA Before Expansion` (`INFERRED`): new livestock or land must not degrade crop SLA beyond an allowed backlog envelope.
- `Balanced Product Monetization` (`INFERRED`): high scores require coordinated crop sale, Milk/Wool/Egg/Fertilizer sale and endgame liquidation with enough logistics bandwidth.
- `Conditional Q2` (`INFERRED`): BUY_Q2 should fire only when Q0+Q1 are near capacity, backlog is controlled, deployable capital exceeds land plus activation cost, and payback fits the remaining horizon.

### Evidence On Q2

| Episode | Competitor | Q2 bought? | Day | Economic state before purchase | Q0+Q1 before purchase | Backlog/weeds | Hands | Payback / final impact |
|---|---|---|---|---|---|---|---:|---|
| `101294736` | truebelief | no | n/a | n/a | Competitor remains `NW, NE` | Weed tile-days `10` | Peak `12` | Final `$86,297` without Q2 |
| `101705751` | Dr. Mikholae Hutchinson | no | n/a | n/a | Competitor remains `NW, NE` | Weed tile-days `11` | Peak `10` | Final `$90,137` without Q2 |
| `101717011` | Alexander Sokolov | no | n/a | n/a | Competitor remains `NW` only | Weed tile-days `145` | Peak `8` | Final `$50,420` without Q1 or Q2; beats our `$24,314` two-quadrant run |

Conclusion: `CONSISTENT REJECTION` for Q2 as a near-term required target in this benchmark batch. This does not prove Q2 is bad; it keeps Q2 as conditional expansion option until a replay or counterfactual shows reliable payback. Q1 is `MIXED EVIDENCE`: two elite replays use it, but `101717011` proves it is not required to beat the current model.

### Assumption Review

| Regola corrente | Evidenza precedente | Nuova evidenza benchmark | Stato aggiornato | Azione |
|---|---|---|---|---|
| Day-1 diversified opening | truebelief reference trajectory | Competitors diversify early, but with different crop mix and ramp | OBSERVED_REFERENCE | CONFIRM as pattern, not constants |
| Delayed Q1 | truebelief Q1 Day 11 | Hutchinson Q1 Day 14; Sokolov no Q1 and still beats us | INFERRED | REFORMULATE as economic/operational/payback gate |
| Q0+Q1 only | X1.12 candidate and truebelief replay | Two competitors score >86K with Q0+Q1; one beats us with Q0 only | TESTED | DOWNGRADE from constraint to sufficient observed envelope |
| Q2 conditional expansion | post-upload inference | No competitor Q2 in three-replay batch | INFERRED | DEPRIORITIZE; keep conditional option |
| `7 Cow / 4 Sheep` livestock target | X1.12 and truebelief-inspired build | truebelief stronger path shows `9 Cow / 5 Sheep`; Hutchinson shows `7 Cow / 4 Sheep / 2 Goose` | OBSERVED_REFERENCE | REFORMULATE as capacity/ROI-gated mix |
| Crop maintenance | X1.13 diagnostics | Strong competitors keep weed tile-days `10/11`; our failing replay has `158` | INFERRED | CONFIRM as high-priority model delta |
| HIRE schedule | X1.12 day schedule | Strong competitors peak `10/12` hands with different timing | INFERRED | REFORMULATE as workload target |
| Liquidity/capital | X1.12 static reserves | Competitors deploy capital into throughput while still ending high cash | INFERRED | NEW HYPOTHESIS: Deployable Capital |
| Crop mix | X1.12 fixed horizon-aware counts | Competitive crop/product sales differ by replay | OBSERVED_REFERENCE | REFORMULATE to horizon/market/workload allocation |
| Commodity Wheat | feed buffer + endgame sale | Wheat sold in both replays and remains logistics/feed commodity | INFERRED | CONFIRM as operational commodity |
| Worker assignment | X1.13 assignment attempts failed locally | Benchmark gap aligns with productive/logistics throughput, not one missed constant | INFERRED | REFORMULATE around role capacity/backlog |
| Shed logistics | X1.12 pickup/place pipeline | Competitors sell broad product set, implying robust collection throughput | INFERRED | CONFIRM and expand telemetry |
| Selling cadence | X1.12 sells products when shed count >0 | Competitors monetize diverse goods; timing still not fully inferred | INFERRED | CONFIRM concept; refine cadence later |
| Land expansion | X1.12 Q1 fixed gate; Q2 conditional | Competitive batch supports Q1 for elite runs but also shows one-quadrant win over us | INFERRED | REFORMULATE Q1/Q2 as deployable-capital and throughput gates |

### Training Interpretation

Il modello viene aggiornato tramite evidenza competitiva osservabile e modifiche esplicite a trigger/target/regole. Non vengono aggiornati pesi di reti neurali.

### Next Model Delta Pointer

The proposed next model delta is documented in `experiments/archive/e12/artifacts/benchmark/NEXT_MODEL_DELTA.md`. It is intentionally analysis-only: no strategy, submission, build, upload or commit is part of Competitive Benchmark Batch #1.

## 14. X1.14 Fast Workforce Capacity Build

Mode implemented: `E12_WORKFORCE_CAPACITY_X114`.

Artifacts:

- `experiments/archive/e12/artifacts/x114/IMPLEMENTATION_DELTA.md`
- `experiments/archive/e12/artifacts/x114/COUNTERFACTUAL_LOG.md`
- `experiments/archive/e12/artifacts/x114/counterfactual_results.json`
- `experiments/archive/e12/artifacts/x114/counterfactual_results.csv`

Status by rule:

| Rule | Implementation status | Verify status | Adoption status |
|---|---|---|---|
| Preventive/aggressive HIRE | IMPLEMENTED | TESTED | REJECTED |
| Crop maintenance priority | IMPLEMENTED | TESTED | REJECTED |
| Livestock expansion brake | IMPLEMENTED | TESTED | REJECTED |
| Q1-protected workforce | IMPLEMENTED | TESTED | REJECTED |
| Q2 disabled for fast build | IMPLEMENTED | TESTED | CONFIRMED for X1.14 scope |

Measured outcome:

- X1.12 baseline A: seed `0` `$42,491`, seed `421521921` `$48,313`.
- X1.14 B: seed `0` `$39,301`, seed `421521921` `$36,238`; weeds drop to `21/21`, but Sheep and Q1 value collapse on required seeds.
- X1.14 C/D: weeds drop to `6/6`, but final money remains below X1.12.
- X1.14 E/F: Q1-protected variants fail economically.
- Seed `1273000467` exception: B reaches `$54,228` vs X1.12 `$43,021`, supporting land-discipline as a future conditional branch rather than immediate adoption.

Conclusion: `X1.14 NO IMPROVEMENT: DO NOT UPLOAD`. Workforce Capacity First is not adopted as tested; the next model should combine workload-based capacity with explicit monetization density and Q1 payback rather than hiring/crop-priority alone.
