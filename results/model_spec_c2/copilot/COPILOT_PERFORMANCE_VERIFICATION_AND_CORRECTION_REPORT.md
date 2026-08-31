# KAGGRICULTURE C2 — COPILOT PERFORMANCE VERIFICATION AND CORRECTION REPORT

```text
AGENT_ID: COPILOT
FOUNDATION_CHECKPOINT: f391ee2
SOURCE_PROMPT: results/model_spec_c2/KAGGRICULTURE_C2_COPILOT_PERFORMANCE_CORRECTION_PROMPT.md
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Full-Episode Baseline

Il preflight tecnico di una revisione precedente (288 step) verificava solo
sanità operativa (nessun crash, binding P0/P1 corretto), non l'economia
dell'intero episodio. Questa sessione ha eseguito il benchmark obbligatorio a
720 step (≈29-30 giorni) PRIMA di ogni modifica strategica, su 3 seed
canonici (`1838889274`, `1619968655`, `710418712`), in entrambe le posizioni
P0 e P1, con l'engine reale (`kaggle_environments.make("kaggriculture", ...)`),
tramite il nuovo script `scripts/benchmark_copilot_c2_performance.py`.

**Baseline (codice pre-correzione, invariato):**

| metrica | valore |
|---|---|
| mean final_money | $9,422.67 |
| median | $9,253.00 |
| stdev (ddof=1) | $1,719.79 |
| P0 vs P1 | identici (binding corretto, confermato) |
| land utilization | 25/25 tile NW, stabile per l'intero episodio (nessuna crescita) |
| idle rate | ~31% dei turni-worker erano `PASS` |

## 2. Economic Gate (baseline)

`mean_final_money = $9,422.67 < $50,000` → **PERFORMANCE_FAILURE**.

## 3. Failure Diagnosis (quantitativa, pre-modifica)

Root cause identificate tramite probe mirati sull'engine reale (non stime):

1. **E-C2-PERF-01 — HIRE cost curve**: il costo di `HIRE` segue una
   progressione Fibonacci-like *entro lo stesso giorno* (1,1,2,3,5,8,13,21,
   34,...) e le hand si resettano a 0 ogni giorno (day-laborer, non
   persistenti). Un `target_workforce` fisso a 9/giorno indipendente dal
   footattivo produceva sovra-costo o idle rate elevato.
2. **E-C2-PERF-02 — working set hardcoded**: `_working_positions()` in
   `c2_policy.py` era limitato staticamente al quadrante NW
   (`x<=4 and y<=4`), quindi il working set non cresceva mai anche in
   presenza di land posseduta oltre lo start; `market_orders()` inoltre non
   emetteva mai `BUY_LAND`.
3. **E-C2-PERF (endgame, scoperta durante il primo tentativo di
   correzione)**: gli acquisti di terra continuavano a verificarsi
   nell'ultimo giorno dell'episodio, immobilizzando capitale in terra
   inutilizzabile nel tempo residuo.

## 4. Land Utilization

Board 10x10 (100 tile); solo il quadrante NW (25 tile) sbloccato all'inizio.
`BUY_LAND` sblocca nell'ordine NE ($1000) → SW ($2000) → SE ($4000).
Nel baseline, land utilization resta fissa a 25/100 tile per l'intero
episodio nonostante il capitale disponibile fosse sufficiente per uno o più
acquisti — perché il bug E-C2-PERF-02 impediva sia l'acquisto sia
l'utilizzo di superficie aggiuntiva.

## 5. Workforce Analysis

Analisi del costo HIRE per-giorno ha mostrato che 3-6 hand/giorno restano a
costo marginale contenuto ($1-2/giorno aggiuntivo), mentre oltre 8-9/giorno
il costo esplode rapidamente (dozzine/centinaia di $ per hand aggiuntiva).
Un target fisso di 9/giorno indipendente dal footprint produceva sia
over-hiring costoso (con footprint piccolo) sia under-hiring con idle rate
elevato (con footprint grande, se l'espansione fosse stata attiva). È stata
introdotta una co-scalatura: `target_workforce_effettivo =
clamp(ceil(active_tiles / target_tiles_per_worker), min_workforce=2,
target_workforce=9)`, con `target_tiles_per_worker=6.0` come valore ottimo
da grid search (testati 2,3,4,6,8,10,15,25).

## 6. Crop Economics

Testati tutti i 5 crop disponibili (WHEAT, CARROT, TOMATO, STRAWBERRY,
MELON) a parità di configurazione (land expansion disattivata,
`target_tiles_per_worker=4`):

| crop | mean final_money |
|---|---|
| WHEAT (default originale) | $10,640 |
| STRAWBERRY | $19,502 |
| MELON | $26,184 (poi $28,909 dopo tuning cutoff/riserva) |

MELON (`seed=80, first_yield_day=10, max_yield_day=12, max_yield=6`) è
risultato dominante nonostante il seed cost più alto e il ciclo più lungo
rispetto a WHEAT (`seed=10, first_yield_day=2, max_yield=6`), grazie al
rapporto prezzo/yield più favorevole nel bilanciamento dell'engine.
`default_crop` e `replant_preferred_crop` sono stati cambiati a MELON.

## 7. Expansion Scenarios

Grid search con `enable_land_expansion=True` su
`target_tiles_per_worker` ∈ {10,15,20,25} × `last_land_purchase_day` ∈
{10,15,20}: miglior risultato $7,027 (tpw=10), inferiore al risultato senza
espansione ($10,640+ con WHEAT, $28,909 con MELON). Ripetuto con la
configurazione MELON finale (tpw=6, last_plant_day=11) e cutoff di acquisto
{0,1,2,3}: migliore risultato con espansione ≈ $22,707, comunque inferiore
a $28,909 senza espansione. **Conclusione evidence-based: l'espansione
fondiaria è disattivata per default** (`enable_land_expansion=False`) perché
il capitale investito in nuova terra non genera throughput
raccolto/venduto sufficiente entro l'orizzonte di 29 giorni per compensare
il costo, specialmente con il ciclo lungo di MELON. La feature resta
implementata e gated (`last_land_purchase_day=11`) per un uso futuro con
presupposti economici diversi.

## 8. Selected Strategy

- crop: MELON (default e replant preferito);
- `seed_reserve=0` (ottimo da grid search su 0,1,2,4,8);
- `last_plant_day=11` (ottimo da grid search su 10,11,12,13,14,15,18,20,22,25,27; crop-specifico, sostituisce il generico 27 tarato su WHEAT);
- `target_tiles_per_worker=6.0`, `target_workforce=9` (tetto), `min_workforce=2`;
- `enable_land_expansion=False` (evidence-based, vedi Sezione 7);
- `last_land_purchase_day=11` (gate dormiente, mantenuto per sicurezza/uso futuro);
- livestock: non introdotto (vedi Sezione 9).

## 9. Livestock Consideration

Rivalutato esplicitamente come richiesto dal prompt (non assunto
aprioristicamente negativo). Verifica di fattibilità: `BUY_ANIMAL COW` costa
~$400; il modulo pascolo richiede una sequenza `PLACE`/build_pasture non
presente nella policy attuale (verificato riferimento incrociato con
l'agente non correlato `productive_mass_roi.py` per capire la meccanica
shed/pasture). Implementare un modulo livestock completo e validarlo contro
l'engine reale eccede il time-budget di questa sessione di correzione.
Decisione: **DEFERRED**, documentata esplicitamente come limite di
tempo/scope, non come conclusione che il livestock sia intrinsecamente
negativo.

## 10. DLC Compliance Check

Il cambiamento nella firma di `market_orders()` (aggiunta di `current_day`)
resta una decisione a singolo turno, deterministica, senza introdurre
repair/cancel/supersede impliciti: ogni chiamata valuta lo stato corrente e
produce ordini indipendenti, coerente con il Decision Lifecycle Contract
C2 frozen. Nessuna nuova azione multi-step o stato persistente è stata
introdotta.

## 11. Implementation Changes

- `src/agricola/strategy/copilot/c2_config.py`: crop MELON, `seed_reserve=0`,
  `last_plant_day=11`, nuovi campi `enable_land_expansion`,
  `land_expansion_reserve`, `max_quadrants`, `last_land_purchase_day`,
  `target_tiles_per_worker`, `min_workforce`; `target_workforce` ridefinito
  a tetto.
- `src/agricola/strategy/copilot/c2_policy.py`: `_working_positions()` non
  più limitato a NW; nuovi `_quadrants_owned()`, `_LAND_PRICE_LADDER`,
  `_next_land_cost()`, `_target_workforce()`; `market_orders()` accetta
  `current_day` e emette `BUY_LAND` gated; `decide()` propaga `current_day`.
- `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md`: Sezioni 12, 14,
  15, 16 aggiornate; Sezione 24 estesa con il nuovo registro revisione
  `COPILOT_PERFORMANCE_CORRECTION`.
- `results/model_spec_c2/copilot/BUILD_VERIFICATION.md`,
  `TOURNAMENT_MANIFEST.md`: aggiornati con esito della correzione,
  preservando `TOURNAMENT_AUTHORIZED: NO` / `KAGGLE_AUTHORIZED: NO`.

## 12. Tests

- `tests/test_copilot_c2.py`: 3 assertion aggiornate per il crop MELON
  (seed dict, `BUY_SEED`/`PLANT` target) e per il conteggio HIRE derivato
  dal footprint (1 anziché 8, footprint di test a 1 tile).
- Esito: `tests/test_copilot_c2.py` + `tests/test_e12_x1_15_copilot.py` →
  **10 passed**, 0 failed.

## 13. Paired 720-Step Results (post-correzione)

Script: `scripts/benchmark_copilot_c2_performance.py`; output completo in
`results/model_spec_c2/copilot/PERFORMANCE_BENCHMARK_720_RAW.json`.

| seed | P0 final_money | P1 final_money |
|---|---|---|
| 1838889274 | 28,909.00 | 28,909.00 |
| 1619968655 | 28,909.00 | 28,909.00 |
| 710418712 | 28,909.00 | 28,909.00 |

`mean = $28,909.00`, `median = $28,909.00`, `stdev (ddof=1) = 0.0`
(risultato deterministico su tutti e 6 i run — la policy non dipende dal
seed una volta disattivata l'espansione, contro un opponent inerte). P0=P1
confermato identico in ogni seed (binding corretto).

## 14. Performance Decomposition

- final_money: $28,909.00 (media), da $9,422.67 baseline (+206.8%);
- land utilization: 25/25 tile NW attive (espansione volutamente disattivata);
- crop: 100% MELON, 47 `PLANT` per run, 34 `HARVEST` per run;
- workforce: 5 worker (co-scalati sul footprint di 25 tile / tpw=6 ≈ 4.2 → clamp a 5 con farmer+hand);
- idle/serviceability: `PASS` resta la maggioranza delle azioni (~1615-1634 su 720 step × N unità), riflettendo che con MELON (ciclo lungo, `last_plant_day=11`) la maggior parte dei restanti giorni non richiede intervento attivo su tile già piantate e in crescita — non un fallimento operativo ma la natura del ciclo colturale scelto;
- NO_OP/rejected: nessun rejected osservato nei run (status `DONE` in tutti);
- repair/invalidation/cancellation/supersession: nessuno introdotto (Sezione 10);
- terminal losses: nessun acquisto di terra o piantagione residua stranded al giorno 29 (cutoff a day 11 applicato correttamente).

## 15. Build Verification (riferimento)

Vedi `results/model_spec_c2/copilot/BUILD_VERIFICATION.md` per il dettaglio
tecnico completo (pytest, compilazione, git diff --check, preflight P0/P1).

## Final Gate

```text
PERFORMANCE_VERDICT: PERFORMANCE_FAILURE
MEAN_FINAL_MONEY: 28909.00
MEDIAN_FINAL_MONEY: 28909.00
STDEV_FINAL_MONEY: 0.0
BASELINE_MEAN_FINAL_MONEY: 9422.67
IMPROVEMENT_PCT: +206.8%
ECONOMIC_GATE_THRESHOLD: 50000
GATE_RESULT: mean < 50000 -> PERFORMANCE_FAILURE (classificazione stretta, riportata onestamente nonostante il miglioramento di ~3x)
BUILD_VERDICT: BUILD_READY (technical, invariato)
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
FOUNDATION_CHECKPOINT: f391ee2 (invariato)
SCOPE_ISOLATION: rispettato — solo file src/agricola/strategy/copilot/*, tests/test_copilot_c2.py, docs/model/model_specs/copilot/*, results/model_spec_c2/copilot/*, scripts/benchmark_copilot_c2_performance.py toccati; nessun artefatto Antigravity/Codex letto o modificato.
STOP_CONDITION: applicata — diagnosi completa + una iterazione di correzione evidence-based eseguite; nessuna ottimizzazione aperta ulteriore (es. livestock, redesign espansione) tentata oltre lo scope della sessione di correzione, come da Sezione 15 del prompt.
```
