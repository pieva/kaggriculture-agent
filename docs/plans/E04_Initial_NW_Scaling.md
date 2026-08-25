# Implementation Plan — E04 Initial NW Scaling (4 → 9 Tile Compact Cluster)

Define and implement **E04 (`NWClusterROIAgent`)** to scale the production footprint from a 4-tile cluster (2×2) to a **compact 9-tile cluster (3×3)** within the initial unlocked NW quadrant, operated by a single farmer without `BUY_LAND` and without `HIRE`.

## User Review Required

> [!IMPORTANT]
> **Single Experimental Variable Scoping:**
> E04 implements **strictly one strategic variable**: expanding the managed tile set from 4 tiles to 9 tiles `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` in the NW quadrant.
> - **NO `BUY_LAND`** (stays 100% inside starting NW quadrant).
> - **NO `HIRE`** (uses 1 single farmer).
> - **NO changes to ROI crop selection formula** (preserves E03 formula for baseline control).
> - **NO horizon filtering** (preserves E03 time logic).

> [!IMPORTANT]
> **Farmer Capacity & Water Starvation Verification:**
> La capacità del singolo farmer di gestire 9 tile senza causare water starvation **non è assunta a priori come garantita**, ma costituisce un'**ipotesi sperimentale da verificare empiricamente**.
> - **Proxy Osservabile Primaria (Severe Starvation):** Conteggio delle tile gestite che si convertono in `{"kind": "WEED"}` nel corso dei 30 episodi di benchmark (causato da $\ge 2$ giorni consecutivi di mancata irrigazione: `consecutive_unwatered >= 2`).
> - **Proxy Osservabile Secondaria (Early Warning Starvation):** Tasso di turni a fine giornata (`hour == 23`) in cui almeno una tile gestita con coltivazione attiva ha `watered_today == False`.
> - **Limiti delle Proxy:** La proxy `WEED` cattura solo il fallimento catastrofico (mancata irrigazione per 2 giorni), mentre la proxy a `hour == 23` rileva il ritardo di irrigazione singolo-giorno. Entrambe le informazioni sono direttamente presenti nella struttura `tiles` dell'observation space pubblico (`observation["farms"][player]["tiles"]`).

## Open Questions

None. Scoping and empirical verification plan resolved.

---

## Proposed Changes

### Strategy Layer (`src/agricola/strategy/`)

#### [NEW] [nw_cluster_roi.py](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/nw_cluster_roi.py)
- Create `NWClusterROIAgent` managing a 3×3 compact cluster of 9 adjacent tiles:
  `((4, 4), (4, 3), (4, 2), (3, 4), (3, 3), (3, 2), (2, 4), (2, 3), (2, 2))`
- Inherit ROI crop selection formula and immediate liquidation logic from E03.
- Adjust seed purchasing order quantity to match the count of empty managed tiles (up to 9).
- Apply spatial task priority `HARVEST > PLANT > WATER` with Manhattan distance routing and deterministic `(y, x)` tie-breaking.

---

### Package Entrypoint & Submission (`src/agricola/`, `submission/`, `scripts/`)

#### [MODIFY] [agent.py](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py)
- Import `NWClusterROIAgent` from `agricola.strategy.nw_cluster_roi`.
- Instantiate `_agent_instance = NWClusterROIAgent()`.

#### [MODIFY] [build_submission.py](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/build_submission.py)
- Update bundled strategy source import from `multi_tile_roi.py` to `nw_cluster_roi.py`.
- Instantiate `_agent_instance = NWClusterROIAgent()` in standalone template.

---

### Test Suite (`tests/`)

#### [NEW] [test_nw_cluster.py](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_nw_cluster.py)
- Unit tests for `NWClusterROIAgent`:
  - 9-tile seed purchasing matching empty tiles (up to 9 seeds).
  - Spatial task priority (`HARVEST > PLANT > WATER`) across 9 tiles.
  - Manhattan navigation and boundary movement across 3×3 grid.
  - Action execution on target tile and `PASS` when all 9 tiles are watered.

---

### Experiment Plan Documentation (`docs/plans/`)

#### [NEW] [E04_Initial_NW_Scaling.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E04_Initial_NW_Scaling.md)
- Document experimental specification, hypotheses, baseline comparison, metrics, and plan details.

---

## Verification Plan

### Automated Tests
1. Run pytest suite across all test files:
   ```bash
   .venv/Scripts/python.exe -m pytest tests/
   ```
2. Verify bundled standalone submission:
   ```bash
   .venv/Scripts/python.exe scripts/build_submission.py
   ```
3. Run local benchmark evaluation (30 episodes) against `pass`, `random`, `starter` with starvation tracking:
   ```bash
   .venv/Scripts/python.exe scripts/run_eval.py
   ```

### Metric Targets for E04 (vs E03 Control Baseline)

| Metric | E03 Control (`MultiTileROIAgent`) | E04 Target (`NWClusterROIAgent`) |
| :--- | :---: | :---: |
| **Footprint** | 4 tiles (2×2 cluster) | **9 tiles (3×3 cluster)** |
| **Total Episodes** | 30 | **30** |
| **Completion Rate** | 100.00% | **100.00%** |
| **Disqualification Rate** | 0.00% | **0.00%** |
| **Overall Win Rate** | 100.00% | **100.00%** |
| **Mean Final Money** | **$14682.47** | **$\ge \$22,000.00$ (+50% min)** |
| **Weed Conversion Count (Severe Starvation)** | 0 | **0 (Target da verificare)** |
| **Unwatered End-of-Day Ratio (Early Warning)** | 0.00% | **0.00% (Target da verificare)** |
| **Agent Mean Latency** | 0.0698 ms/turn | **$< 1.0$ ms/turn** |

