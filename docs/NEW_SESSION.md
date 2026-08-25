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

## Punto di ripartenza per la prossima sessione (E07)

Alla ripresa della prossima sessione:

1. Iniziare l'esperimento **E07 — DEFINE** a partire dalle candidate valutate nella REVIEW E06.
2. Candidate raccomandate per E07:
   - **Candidate A — `DIG` / Weed Recovery:** Attivare `DIG` per eliminare le 70 erbacce residue e recuperare le tile morte.
   - **Candidate B — Dynamic Worker Partitioning:** Bilanciare dinamicamente i carichi tra Farmer e Hand 1.
   - **Candidate C — Dynamic Priority Scheduling:** Prioritizzare `WATER_URGENT > HARVEST > PLANT > WATER_NON_URGENT`.
3. Non iniziare BUILD o benchmark prima di aver completato DEFINE e PLAN E07.

<!-- END OF DOCUMENT -->