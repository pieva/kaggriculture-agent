# NEW SESSION — Kaggriculture Agent

## Stato del progetto

Il progetto ha completato e consolidato cinque iterazioni sperimentali supervisionate.

Metodo adottato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Branch corrente:

`main`

Stato Git atteso:

- `main` allineato con `origin/main`;
- working tree pulito.

Ultimo commit consolidato:

`Finalize E05 HIRE multi-worker scaling experiment`

Tag disponibili:

- `v0.1-e01-baseline`
- `v0.2-e02-roicrop`
- `v0.3-e03-multitile`
- `v0.4-e04-nw-scaling`
- `v0.5-e05-hire-multiworker`

---

## Progressione Sperimentale

`E01 operational baseline → E02 economic crop selection → E03 production scaling (4 tiles) → E04 NW scaling (9 tiles, single farmer, falsified) → E05 multi-worker HIRE (9 tiles, 2 workers, shipped)`

---

## E01 — Baseline

Strategia: `CarrotLoopAgent`
- Mean Final Money: `$3567.63 ± $205.38`
- Win Rate vs `starter`: `0.00%` (100% pareggi)
- Tag: `v0.1-e01-baseline`

---

## E02 — Dynamic Crop Selection & ROI Scaling

Strategia: `ROICropAgent`
- Mean Final Money: `$5857.17 ± $132.37` (`+64.18%` vs E01)
- Win Rate vs `starter`: `100.00%`
- Tag: `v0.2-e02-roicrop`

---

## E03 — Multi-Tile Scaling

Strategia: `MultiTileROIAgent`
- Mean Final Money: `$14682.47 ± $1164.33` (`+150.68%` vs E02)
- Win Rate vs `starter`: `100.00%`
- Tag: `v0.3-e03-multitile`

---

## E04 — Initial NW Scaling

Strategia: `NWClusterROIAgent`
- Footprint: 9 tile (3x3)
- Workers: 1 farmer
- Mean Final Money: `$11232.47 ± $661.26` (`-$3450.00` / `-23.49%` vs E03)
- Total Weed Conversions: `238`
- Ipotesi Economica: `FALSIFIED` (single farmer capacity limit)
- Tag: `v0.4-e04-nw-scaling`

---

## E05 — HIRE Multi-Worker Scaling

Strategia: `HIRENWClusterROIAgent`

Variabile sperimentale: **introduzione di 1 farm hand giornaliera tramite l'azione `HIRE` ($1/giorno) con partizionamento spaziale fisso 4:5 sul cluster a 9 tile nel quadrante NW `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`**.

### Risultati benchmark locale E05
- Total Episodes: `30`
- Completion Rate: `100.00%`
- Disqualification Rate: `0.00%`
- Overall Win Rate: `100.00%` (30W / 0L / 0D)
- Mean Final Money: **`$21568.93 ± $361.25`** (`+$10336.46` / `+92.02%` vs E04, `+$6886.46` / `+46.90%` vs E03)
- Median Final Money: **`$21442.00`**
- Total Weed Conversions: **176 weeds** (5.87 conversioni/episodio, `-26.05%` vs E04)
- Mean Unwatered End-of-Day Ratio: **3.33%**
- Agent Mean Turn Latency: **`0.0924 ms/turno`**

### REVIEW & SHIP
- Experimental Integrity: `PASSED`
- Test Suite & Standalone Build: `PASSED`
- Economic Hypothesis: **`SUPPORTED`**
- Worker Capacity Bottleneck: **`STRONGLY SUPPORTED`**
- Starvation Operational Status: **`STARVATION REDUCED BUT UNRESOLVED`**
- SHIP Status: **`PASSED`**
- Tag: `v0.5-e05-hire-multiworker`

### Evidenze E05
- Capability Analysis: [`docs/experiments/E05-01_HIRE_Capability_Analysis.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/experiments/E05-01_HIRE_Capability_Analysis.md)
- Implementation Plan: [`docs/plans/E05_HIRE_MultiWorker_Scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E05_HIRE_MultiWorker_Scaling.md)
- BUILD Document: [`docs/versions/E05_build_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E05_build_antigravity.md)
- VERIFY Document: [`docs/versions/E05_verify_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E05_verify_antigravity.md)
- REVIEW Document: [`docs/versions/E05_review_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E05_review_antigravity.md)
- SHIP Document: [`docs/versions/E05_ship_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E05_ship_antigravity.md)

---

## Punto di partenza della prossima sessione

> **E05 è concluso e shipped. Non iniziare automaticamente E06. Valutare prima le direzioni candidate emerse dalla REVIEW.**

La prossima sessione dovrà partire dalla scelta tra le candidate emerse dalla REVIEW di E05:

1. **Candidate A — Water-First Scheduling con HIRE (Raccomandata dalla REVIEW):** Mantenere 9 tile, 1 farmer + 1 hand e 4:5 partitioning, modificando la priorità operativa verso l'irrigazione (`WATER > HARVEST > PLANT`) per azzerare le 176 weed residue senza costi aggiuntivi.
2. **Candidate B — DIG / Weed Recovery con HIRE:** Introdurre l'azione `DIG` per bonificare le tile coperte da erbacce.
3. **Candidate C — Dynamic Worker Partitioning:** Ribilanciare dinamicamente le tile assegnate ai worker.
4. **Candidate D — Multi-Hand Scaling (2+ HIRE):** Testare l'ingaggio di una seconda farm hand ($2/giorno).
5. **Candidate E — Further Spatial Scaling:** Espandersi oltre le 9 tile sbloccando nuovi terreni.


## E05 — HIRE / Multi-Worker Scaling — SHIPPED

E05 è concluso e shipped.

### Risultato locale consolidato

- Agent: `HIRENWClusterROIAgent`
- Footprint: 9 tile NW
- Workers: 1 farmer + 1 farm hand giornaliera
- Partitioning: 4:5 fisso
- Policy: `HARVEST > PLANT > WATER`
- Episodes: 30
- Completion Rate: 100%
- Disqualification Rate: 0%
- Win Rate: 100%
- Mean Final Money: `$21568.93 ± $361.25`
- Median Final Money: `$21442.00`
- Delta vs E04: `+$10336.46 / +92.02%`
- Delta vs E03: `+$6886.46 / +46.90%`
- Weed Conversions: `176`
- Weed reduction vs E04: `-26.05%`
- Mean Unwatered End-of-Day Ratio: `3.33%`

Decisioni:

- Economic Hypothesis: `SUPPORTED`
- Worker Capacity Bottleneck: `STRONGLY SUPPORTED`
- Starvation: `REDUCED BUT UNRESOLVED`
- Experiment: `STRONG SUCCESS`

Tag:

`v0.5-e05-hire-multiworker`

## Kaggle External Validation — VALIDATA & STABILIZZATA

È stata effettuata la submission ufficiale Kaggle della standalone E05:

`submission/submission.py` (`HIRENWClusterROIAgent`)

Score osservato e stabilizzato: **`439.7`** (External Validation Passed, +161.4 pts / +57.99% vs E03 278.3).

Riferimenti storici Kaggle attualmente disponibili:

- E01: `600.0` storico
- E02: `285.1` storico
- E03: `278.3`
- E04: nessuna submission
- E05: `439.7` (stabilizzato)

## E06 — Water-First Scheduling — SHIPPED

E06 è concluso e shipped (`v0.6-e06-water-first`).

### Risultato locale consolidato
- Agent: `WaterFirstHIRENWClusterROIAgent`
- Footprint: 9 tile NW
- Workers: 1 farmer + 1 farm hand giornaliera ($1/giorno)
- Partitioning: 4:5 fisso
- Task Priority: `WATER > HARVEST > PLANT`
- Episodes: 30
- Completion Rate: 100%
- Disqualification Rate: 0%
- Win Rate: 100%
- Mean Final Money: **`$24662.00 ± $1932.04`** (+14.34% vs E05)
- Median Final Money: **`$25847.00`** (+20.54% vs E05)
- Weed Conversions: **`70`** (-60.23% vs E05)
- Mean Weed Rate: 2.33 weeds/episode
- Paired Money Win Rate: 96.7% (29/30)
- Paired Weed Win Rate: 100% (30/30)

Decisioni:
- Experimental Integrity: `PASSED`
- Operational Result: `PARTIAL SUPPORT` (-60.23% weeds)
- Economic Result: `ECONOMIC IMPROVEMENT` (+$3093.07 money)
- Hypothesis Verdict: `SUPPORTED`
- SHIP Status: `PASSED`
- Tag Git: `v0.6-e06-water-first`

## E07 — Competitive Baseline Reconstruction — VERIFICA PRESTAZIONALE COMPLETATA

La fase di verifica prestazionale `E07-08 — VERIFY Local Performance` è stata completata con successo (30 episodi controllati e paired):
- **Strategy Implementation:** `HybridLivestockClusterROIAgent` in [`src/agricola/strategy/hybrid_livestock_cluster_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/hybrid_livestock_cluster_roi.py)
- **VERIFY Local Performance Report:** [`docs/versions/E07_verify_local_performance.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E07_verify_local_performance.md)
- **Benchmark Data:** [`results/e07_competitive_baseline.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e07_competitive_baseline.json)

### Sintesi Benchmark Locale (30 Episodi Paired)
- **Decisione Finale VERIFY:** **`ARCHITECTURALLY VALID, ECONOMICALLY WEAK`**
- **E07 Mean Final Money:** **`$15,364.57 ± $3,144.39`** (Median: `$15,990.50`, Min: `$7,253.00`, Max: `$18,423.00`, Win Rate vs Opponents: `100.0%`).
- **Confronto vs E06 (`$25,180.30`):** Delta Medio **`-$9,815.73` (`-38.98%`)**, Delta Mediano **`-$9,856.50` (`-38.13%`)**, Paired Win Rate **`0/30 (0.0%)`**.
- **Confronto vs E05 (`$21,485.87`):** Delta Medio **`-$6,121.30` (`-28.49%`)**, Delta Mediano **`-$5,451.50` (`-25.42%`)**, Paired Win Rate **`0/30 (0.0%)`**.

### Cause Principali della Regressione Economica E07
1. **Costo d'opportunità del Wheat (Causa Principale):** 6 delle 9 mattonelle Q0 riservate al Wheat ($25 ricavo lordo) anziché Carrots/Melons ($140-$250 ricavo lordo).
2. **Capitale immobilizzato nel Livestock:** Bovini costano $400 + 5 mattonelle pascolo + 6 feed tiles + 14 giorni ciclo, generando solo $389.33 di Milk entro il giorno 30 (non ripagano il costo diretto di $573.34).
3. **Espansione Terreni Q1 e Distanza di Spostamento:** L'acquisto di Q1 costa $1,000 cash al giorno 12. Gli spostamenti dei worker su 50 mattonelle aumentano il movement al 54.2%, aumentando le malerbe a 7.73/episodio (vs 2.1 in E06).

## E08 — Productive Scale Optimization — DEFINE COMPLETED

La fase `E08-01 — DEFINE Productive Scale Optimization` è stata completata con successo ([`docs/versions/E08_define_productive_scale.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E08_define_productive_scale.md)).

### Punteggi Kaggle Rilevati
- **E05:** `429.5`
- **E06:** `375.7`
- **E07:** `339.5` (sottoutilizzo del terreno acquistato: 24 tile coltive su 50 possedute).

### Ipotesi e Configurazione E08 Selezionata (Scenario S2 — High Scale)
- **Variabile Primaria Modificata:** **`PRODUCTIVE SCALE`** (Target productive tiles incrementato da **24 a 40**, land utilization da 48.0% a 80.0%).
- **Crop Allocation:** 6 Wheat (feed), 22 Melon (+10 cash), 12 Carrot (+6 liquidity).
- **Variabili Congelate da E07:**
  - Workforce: 4 worker (1 Farmer + 3 Hands) — capacità ampiamente sufficiente (96 worker-turn/giorno, 54.2% carico produttivo).
  - Livestock: 4 Cow, 2 Sheep, 6 Wheat feed loop.
  - Land Expansion: Giorno 12 `BUY_LAND` Q1 ($1,000).
  - Task Priority: `WATER > FEED > HARVEST > PLANT` (Water-First).
  - Liquidation & Market Policy: Invariati.
## E08 — Productive Scale Optimization — COMPLETED & CLOSED

L'esperimento **E08 — Productive Scale Optimization** è stato completato e formalmente chiuso ([`docs/versions/E08_ship_productive_scale.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E08_ship_productive_scale.md)).

### Sintesi Finale E08:
1. **Esito Sperimentale:** Ipotesi falsificata. Lo scaling a 40 tile ha ridotto il Mean Final Money del **-10.81%** ($11,880.30 vs E07 $13,320.37).
2. **Candidatura Kaggle:** **NON CANDIDATO.** La baseline shipped attiva in `src/agricola/agent.py` rimane **E06 `WaterFirstHIRENWClusterROIAgent`** ($25,000+).
3. **Preservazione:** Il codice `HybridLivestockClusterROIAgent`, la suite di unit test (42/42 passati) ed i risultati JSON (`results/e08_productive_scale.json`) rimangono salvati come evidenza empirica.

## Punto di ripartenza (Prossima Azione: E09-01 DEFINE)

Procedere con la fase **E09-01 DEFINE — Livestock Subsystem Ablation (ON → OFF)** per isolare la causalità dell'allevamento rispetto alla baseline primaria E07 (24 tile, 4 worker).

<!-- END OF DOCUMENT -->