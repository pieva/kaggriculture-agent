# E06 Implementation Plan — Water-First Scheduling (`WaterFirstHIRENWClusterROIAgent`)

**Date:** 2026-08-25  
**Author:** Google Antigravity  
**Phase:** PLAN  
**Target Plan File:** `docs/plans/E06_Water_First_Scheduling.md`  
**Status:** Plan Proposed — Awaiting User Approval before BUILD  

---

## 1. Experiment ID and Objective

- **Experiment ID:** `E06 — Water-First Scheduling`
- **Candidate Strategy Class:** `WaterFirstHIRENWClusterROIAgent`
- **Baseline Reference:** E05 (`HIRENWClusterROIAgent`, Shipped)
- **Objective:** Evaluate whether replacing the worker task priority policy `HARVEST > PLANT > WATER` with `WATER > HARVEST > PLANT` resolves the residual operational starvation observed in E05 (176 weed conversions, 3.33% unwatered end-of-day ratio) on the 9-tile NW multi-worker cluster, while maintaining economic non-regression (Mean Final Money `≥ $21200.00`).

---

## 2. Baseline E05

The E05 baseline (`HIRENWClusterROIAgent`) delivered the following consolidated performance across a 30-episode benchmark:

- **Managed Footprint:** 9 tiles in 3×3 NW cluster `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`
- **Workers & HIRE:** 1 Farmer Principal (4 tiles) + 1 Farm Hand ($1/day HIRE at `hour == 0`, 5 tiles)
- **Spatial Partitioning:** Fixed 4:5 (Farmer: 4 tiles, Hand 1: 5 tiles)
- **Task Priority:** `HARVEST > PLANT > WATER`
- **Completion Rate:** `100.00%`
- **Disqualification Rate:** `0.00%`
- **Overall Win Rate:** `100.00%`
- **Mean Final Money:** **`$21568.93 ± $361.25`**
- **Median Final Money:** **`$21442.00`**
- **Total Weed Conversions:** **`176`** (5.87 weeds/episode)
- **Mean Unwatered End-of-Day Ratio:** **`3.33%`**
- **Agent Mean Turn Latency:** `0.0924 ms/turn`
- **Kaggle External Validation Rating:** **`439.7`**

---

## 3. Experimental Hypothesis

> **A parità di footprint (9 tile NW), worker (1 farmer + 1 hand a $1/giorno), partitioning (4:5), crop selection (ROI/giorno E03), routing (Manhattan), opponent set (`pass`, `random`, `starter`) e seed (0–9), assegnare priorità a `WATER` prima di `HARVEST` e `PLANT` (`WaterFirstHIRENWClusterROIAgent`) ridurrà le conversioni in weed da 176 a < 50 (-71.6%) e il rapporto medio di tile non irrigate a fine giornata da 3.33% a < 1.0%, senza produrre una regressione economica inferiore a $21200.00 rispetto al baseline E05 ($21568.93 ± $361.25).**

---

## 4. Independent Variable

The **sole independent variable** modified in E06 is the worker task prioritization sequence evaluated inside `_compute_worker_action()`:

- **E05 Policy:** `HARVEST > PLANT > WATER`
  ```python
  if harvest_candidate_tiles:
      target_pos = select_nearest(harvest_candidate_tiles)
      task = "HARVEST"
  elif empty_tiles and target_seeds_owned > 0:
      target_pos = select_nearest(empty_tiles)
      task = "PLANT"
  elif water_candidate_tiles:
      target_pos = select_nearest(water_candidate_tiles)
      task = "WATER"
  ```

- **E06 Intervention Policy:** `WATER > HARVEST > PLANT`
  ```python
  if water_candidate_tiles:
      target_pos = select_nearest(water_candidate_tiles)
      task = "WATER"
  elif harvest_candidate_tiles:
      target_pos = select_nearest(harvest_candidate_tiles)
      task = "HARVEST"
  elif empty_tiles and target_seeds_owned > 0:
      target_pos = select_nearest(empty_tiles)
      task = "PLANT"
  ```

---

## 5. Controlled Variables

To maintain single-variable integrity, all other system parameters are strictly frozen:

1. **Footprint:** 9 tiles NW cluster `{(2,2), (2,3), (2,4), (3,2), (3,3), (3,4), (4,2), (4,3), (4,4)}`.
2. **Workers:** 1 Farmer Principal + 1 Farm Hand hired daily on `hour == 0` when `len(hands) == 0` and `hires_today == 0` ($1/day cost).
3. **Partitioning:** Farmer: `{(4,4), (4,3), (3,4), (3,3)}` (4 tiles); Hand 1: `{(4,2), (3,2), (2,4), (2,3), (2,2)}` (5 tiles).
4. **Crop Selection:** ROI per day formula ($2.0 \times \text{price} - \text{seed}) / \text{days}$.
5. **Liquidation:** Immediate shed sale during Market Phase (`hour >= 0`).
6. **Movement & Pathfinding:** Nearest Manhattan distance step computation.
7. **Episode Duration:** 720 steps (30 days).
8. **Opponent Set:** `['pass', 'random', 'starter']`, 10 episodes per opponent (total 30).
9. **Benchmark Protocol:** Seeds 0–9, 50% P0 / 50% P1.

---

## 6. Implementation Strategy

To ensure zero risk of mutating or regressing E05, we adopt an **Object-Oriented Subclassing Pattern**:

1. Create a new strategy file: [`src/agricola/strategy/water_first_hire_nw_cluster_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/water_first_hire_nw_cluster_roi.py).
2. Define class `WaterFirstHIRENWClusterROIAgent` subclassing `HIRENWClusterROIAgent`.
3. Override **only** the helper method `_compute_worker_action()` to prioritize `water_candidate_tiles` over `harvest_candidate_tiles` and `empty_tiles`.
4. All other methods (`act`, `select_best_crop`, `calculate_net_profit_per_day`, `_get_step_direction`) are inherited directly from `HIRENWClusterROIAgent`.

This guarantees:
- **E05 code in `hire_nw_cluster_roi.py` remains 100% untouched.**
- Zero code duplication for crop selection, market sales, HIRE lifecycle, or movement logic.

---

## 7. Files and Classes Impacted

### New Files to Create during BUILD
- `[NEW]` [`src/agricola/strategy/water_first_hire_nw_cluster_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/water_first_hire_nw_cluster_roi.py) (`WaterFirstHIRENWClusterROIAgent`)
- `[NEW]` [`tests/test_water_first_hire_nw_cluster.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_water_first_hire_nw_cluster.py) (Unit test suite for Water-First policy)

### Existing Files to Modify during BUILD
- `[MODIFY]` [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py) (Update main entrypoint to instantiate `WaterFirstHIRENWClusterROIAgent` for verification)

### Artifact Files Preserved / Created
- `[PRESERVED]` [`results/e05_hire_multiworker.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e05_hire_multiworker.json)
- `[EXPECTED NEW]` `results/e06_water_first.json` (Isolated benchmark output)

---

## 8. Primary Metrics

1. **Total Weed Conversions (Primary Operational Metric):**
   - Cumulative count of tiles converted into `WEED` status at the end of episodes across 30 episodes.
   - **E05 Baseline:** `176` weeds (5.87 weeds/ep).

2. **Mean Final Money (Primary Economic Metric):**
   - Mean final money accumulated across 30 benchmark episodes.
   - **E05 Baseline:** `$21568.93 ± $361.25`.

---

## 9. Secondary Metrics

- **Mean Unwatered End-of-Day Ratio (%):** Percentage of days where at least 1 tile had `watered_today == False` at `hour == 23`. (E05 Baseline: `3.33%`).
- **Completion Rate (%):** Target `100.00%`.
- **Disqualification Rate (%):** Target `0.00%`.
- **Win Rate (%):** Target `100.00%`.
- **Opponent Breakdown:** Individual rewards and win rates against `pass`, `random`, and `starter`.
- **Agent Mean Turn Latency (ms):** Per-turn decision latency. (Target: `< 1.0 ms`).

---

## 10. Operational Success Classification

We classify the operational outcome for **Total Weed Conversions** into three distinct categories:

| Category | Total Weed Conversions | Interpretation |
| :--- | ---: | :--- |
| **`STRONG SUCCESS`** | **`< 50`** | Water-First eliminates `> 71.6%` of weed conversions; priority deferral was the primary root cause. |
| **`PARTIAL SUPPORT`** | **`50–119`** | Water-First significantly reduces starvation, but residual weeds remain; capacity/partitioning issues contribute. |
| **`FALSIFIED`** | **`≥ 120`** | Priority deferral was not the primary cause of starvation; policy change fails to solve operational failure mode. |

---

## 11. Economic Guardrail

To evaluate economic non-regression without making unwarranted statistical significance claims, we establish **`$21200.00`** as a practical operational guardrail (~1 sample standard deviation below the E05 mean of `$21568.93 ± $361.25`):

| Economic Outcome | Mean Final Money ($) | Interpretation |
| :--- | :--- | :--- |
| **Economic Expansion** | `> $21568.93` | Water-First improves economics (saved weeds > rotation delays). |
| **Substantial Neutrality** | `[$21200.00, $21568.93]` | Water-First maintains economics within acceptable ~1 std dev tolerance. |
| **Moderate Regression** | `[$20500.00, $21199.99]` | Rotation delays cause noticeable economic loss below guardrail. |
| **Severe Regression** | `< $20500.00` | Rotation delays cause severe productivity loss. |

---

## 12. Paired E05/E06 Comparison Plan

Because E05 and E06 use identical episode seeds ($0, 100, 200, \dots, 900$ for each opponent) and turn-order assignments (P0/P1), we will perform a **seed-by-seed paired analysis**:

$$\Delta \text{Money}_i = \text{Money}_{\text{E06}, i} - \text{Money}_{\text{E05}, i}$$
$$\Delta \text{Weeds}_i = \text{Weeds}_{\text{E06}, i} - \text{Weeds}_{\text{E05}, i}$$

We will extract episode data from [`results/e05_hire_multiworker.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e05_hire_multiworker.json) and compute:
- Mean paired delta money ($\overline{\Delta \text{Money}}$) and sample std dev.
- Percentage of episodes where E06 Money $\ge$ E05 Money.
- Percentage of episodes where E06 Weeds $<$ E05 Weeds.

*Note: Paired comparison is an additional diagnostic metric and does not replace global mean, std dev, or opponent breakdown.*

---

## 13. Trade-off Analysis Protocol

To detect whether Water-First causes hidden crop rotation delays:
1. We will monitor if planting steps are deferred while workers water already-planted crops.
2. We will analyze if total revenue or harvest events drop on specific long-growth episodes.
3. If rotation delays occur, they will be documented as an empirical consequence of the Water-First policy (no ad-hoc policy tuning inside E06).

---

## 14. Confounder Controls

- **No Pathfinding Alteration:** Manhattan distance movement remains unchanged.
- **No Crop Policy Change:** ROI per day formula remains unchanged.
- **No HIRE Modification:** Daily $1/day hire on hour 0 remains unchanged.
- **No Spatial Partitioning Modification:** Farmer (4) and Hand 1 (5) tiles remain fixed.

---

## 15. Test Plan (Unit Testing)

Before running the full benchmark, the unit test suite (`pytest tests/`) must pass 100%:

1. **`test_water_first_priority`**: Construct a state with 1 harvestable tile, 1 empty tile (with seeds), and 1 unwatered plant tile. Verify `WaterFirstHIRENWClusterROIAgent` chooses `WATER`.
2. **`test_e05_priority_unmodified`**: Construct the same state for `HIRENWClusterROIAgent`. Verify it chooses `HARVEST`.
3. **`test_water_first_full_flow`**: Test worker movement, hire execution, and 4:5 partition adherence under `WaterFirstHIRENWClusterROIAgent`.

---

## 16. Benchmark Protocol

- **Runner Command:** `python -m agricola.evaluation.runner` or evaluation script.
- **Episodes:** 30 episodes total (10 vs `pass`, 10 vs `random`, 10 vs `starter`).
- **Seeds:** Seeds 0–9 per opponent, matching E05.
- **Output File:** `results/e06_water_first.json` (Strictly isolated from `e05_hire_multiworker.json`).

---

## 17. Decision Matrix

| Scenario | Weed Conversions | Mean Final Money ($) | Completion / Disqualification | Overall Decision & Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **A — Strong Success** | **`< 50`** | **`≥ $21200.00`** | 100% / 0% | **`SHIP CANDIDATE`** — Starvation resolved with non-inferior money. |
| **B — Operational Win / Economic Trade-off** | **`< 50`** | **`< $21200.00`** | 100% / 0% | **`REJECT / TRADE-OFF NEGATIVE`** — Starvation fixed, but rotation delay cost exceeds guardrail. |
| **C — Partial Support** | **`50–119`** | **`≥ $21200.00`** | 100% / 0% | **`REVISE / PARTIAL`** — Starvation reduced, but scheduling alone is insufficient. |
| **D — Falsified** | **`≥ 120`** | Any | 100% / 0% | **`FALSIFIED`** — Priority deferral is not the primary cause of starvation. |
| **E — Reliability Failure** | Any | Any | `< 100%` or `> 0%` | **`REJECT`** — Execution instability or crashes. |

---

## 18. Rollback & Preservation of E05

- `HIRENWClusterROIAgent` remains preserved in `src/agricola/strategy/hire_nw_cluster_roi.py`.
- `results/e05_hire_multiworker.json` is untouched.
- If E06 is falsified or rejected, `src/agricola/agent.py` can be reverted to `HIRENWClusterROIAgent` in 1 line.

---

## 19. Expected Artifacts for E06 Progression

- Plan Document: `docs/plans/E06_Water_First_Scheduling.md`
- Code Strategy: `src/agricola/strategy/water_first_hire_nw_cluster_roi.py`
- Test Suite: `tests/test_water_first_hire_nw_cluster.py`
- Benchmark Output: `results/e06_water_first.json`
- Verification Evidence: `docs/versions/E06_verify_antigravity.md`
- Review Evidence: `docs/versions/E06_review_antigravity.md`
- Ship Evidence: `docs/versions/E06_ship_antigravity.md`

---

## 20. GO / REVISE / NO-GO Recommendation for BUILD

### Recommendation: **`GO` for BUILD**

The plan is complete, isolated, and strictly single-variable. It preserves E05 historical reproducibility while establishing clear, falsifiable criteria for E06.

---
*Awaiting User Approval before executing BUILD phase.*
