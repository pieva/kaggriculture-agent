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

<!-- END OF DOCUMENT -->