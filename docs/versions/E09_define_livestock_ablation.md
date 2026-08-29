# DEFINE Report — E09-01 Livestock Subsystem Ablation (Revised)

**Date:** 2026-08-26  
**Phase:** E09-01 DEFINE (Methodological Revision Pass)  
**Status:** `DEFINE COMPLETED`  
**Decision:** **`READY FOR E09-01 BUILD`**  
**Experiment Type:** Controlled Single-Variable Ablation  
**Primary Baseline:** **E08 — 40 tile — Livestock ON** ([`results/e08_productive_scale.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e08_productive_scale.json))  
**Secondary Historical Reference:** E07 — 24 tile — Livestock ON  

---

## 1. Context & Methodological Rationale

Following the closure of **E08 — Productive Scale Optimization** (where expanding nominal crop footprint from 24 to 40 tiles across 50 owned tiles degraded Mean Final Money by **-10.81%** vs E07 due to worker movement saturation at **61.6%**), experiment **E09-01** initiates a controlled single-variable ablation line.

### Experimental Progression Chain
```text
E07: 24 tile + Livestock ON (Mean Money = $13,320.37)
        |
        | Productive Scale Expansion (24 -> 40 tiles)
        v
E08: 40 tile + Livestock ON (Mean Money = $11,880.30)
        |
        | Single-Variable Livestock Ablation (Livestock ON -> OFF)
        v
E09-01: 40 tile + Livestock OFF (Mean Money = ?)
```

### Methodological Rule:
To achieve a **pure controlled ablation**, E09-01 must modify **exactly one independent variable**:

$$\text{Livestock ON (E08)} \longrightarrow \text{Livestock OFF (E09-01)}$$

while holding the 40-tile productive footprint, 4-worker workforce, land expansion policy, Water-First priority, and crop selection strictly **identical to E08**.

Evaluating E09-01 directly against **E08** tests a fundamental architectural question: *Was the 40-tile footprint intrinsically inefficient, or was it rendered inefficient by the operational overhead and financial drain (-$3,977.34) of the livestock subsystem?*

---

## 2. Experimental Question

> **"Se rimuoviamo il livestock da E08 (40 tile) senza cambiare nient'altro, la configurazione produttiva da 40 tile consente di utilizzare meglio capitale, azioni, movimento e spazio, recuperando valore?"**

Specifically: What is the economic performance, operational efficiency, and worker throughput of the 40-tile strategy when the livestock subsystem (animals, pastures, feeding, milk/wool harvesting, feed safety buffer) is completely ablated while preserving all 40-tile crop, land, worker, and task priority logic?

---

## 3. Hypotheses

- **H0 (Null Hypothesis):** Removing the livestock subsystem from the E08 40-tile configuration does not produce a consistent economic or operational improvement over E08.
- **H1 (Experimental Hypothesis):** Removing the livestock subsystem from the E08 40-tile configuration produces a consistent, measurable improvement in Mean Final Money over E08 by eliminating direct financial loss (-$3,977.34) and freeing worker turns for high-ROI 40-tile crop management.

---

## 4. Primary Baseline vs Secondary Historical Reference

### Primary Baseline: E08 — 40 tile — Livestock ON
The primary causal delta ($\Delta_{\text{causal}}$) of E09-01 is defined strictly against **E08**:

$$\Delta_{\text{causal}} = \text{Mean Money}_{\text{E09-01}} - \text{Mean Money}_{\text{E08}}$$

- **Primary Baseline Dataset:** [`results/e08_productive_scale.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e08_productive_scale.json)
- **E08 Mean Final Money:** **$11,880.30**
- **E08 Sample Std Dev (`ddof=1`):** **± $6,475.07**
- **E08 Median Final Money:** **$9,790.50**
- **E08 Vs `pass` Mean Money:** $10,987.80
- **E08 Vs `random` Mean Money:** $11,123.70
- **E08 Vs `starter` Mean Money:** $13,529.40
- **E08 Livestock Direct Net Balance:** **-$3,977.34** ($4,426.67 spending vs $449.33 revenue)
- **E08 Worker Movement Share:** **61.6%**
- **E08 `plant_pending` Backlog:** **17.96 tiles/day**

### Secondary Historical Reference: E07 — 24 tile — Livestock ON
E07 ($13,320.37 paired mean money) serves as a **secondary descriptive reference**. Comparing E09-01 against E07 answers the strategic question: *Does livestock ablation allow the 40-tile footprint to recover or surpass the 24-tile E07 performance level?*

---

## 5. Audit of Current Livestock Subsystem in E08

The audit of `HybridLivestockClusterROIAgent` ([`src/agricola/strategy/hybrid_livestock_cluster_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/hybrid_livestock_cluster_roi.py)) identified the following touchpoints:

| Touchpoint Phase | Strategy Component | Implementation / Action | Resource & Capital Impact |
| :--- | :--- | :--- | :--- |
| **Configuration** | Attributes | `pasture_tiles_cow` (4 tiles: 0,0..1,1), `pasture_tiles_sheep` (1 tile: 0,2), `target_cows` (4), `target_sheep` (2), `feed_safety_buffer` (5 Wheat). | 5 Q0 tiles allocated to pastures; 5 Wheat reserved in shed. |
| **Market Purchases** | `_process_market_decisions` | `BUY_ANIMAL COW` ($400/ea), `BUY_ANIMAL SHEEP` ($500/ea) when cash $\ge \$1500$, day $\ge 6$, feed buffer $\ge 5$, shed space $\le 95$. | Total spending: **$4,426.67** across 30 episodes. Drains liquidity prior to Day 12 land purchase. |
| **Farmer Placement** | `_get_worker_action` (Farmer) | Farmer picks up `COW`/`SHEEP` from shed, moves to `(0,0)..(0,2)`, executes `BUILD_PASTURE` then `PLACE COW`/`SHEEP`. | Farmer turn consumption; travel between shed `(4,4)` and pasture grid `(0,0)..(0,2)`. |
| **Feeding Loop** | `_get_worker_action` (Farmer/Hand 1) | Checks unfed placed animals; picks up Wheat from shed `(4,4)` if needed; moves to pasture tile; executes `FEED`. | `wheat_fed += 1` per animal/day; Wheat consumed; worker movement to pastures. |
| **Product Harvest** | `_get_worker_action` (Farmer/Hand 1) | Checks `yield_units > 0` on pastures; moves to pasture; executes `HARVEST`; moves to shed `(4,4)`; executes `DROP`. | Worker movement and action turns for Milk/Wool items in inventory. |
| **Market Sales** | `_process_sales` | Sells `MILK` ($160/unit) and `WOOL` ($200/unit) from shed. Reserves 5 Wheat before selling Wheat ($25/unit). | Total realized revenue: **$449.33** across 30 episodes. Net financial balance: **-$3,977.34**. |

---

## 6. Operational Definition of E09-01 Treatment ("Livestock Disabled")

In **E09-01**, the livestock subsystem is transitioned from **`ON` $\rightarrow$ `OFF`**:

### Active Strategic Behaviors Disabled:
1. **Zero Animal Purchases:** `buy_animal("COW")` and `buy_animal("SHEEP")` calls completely disabled (`target_cows = 0`, `target_sheep = 0`).
2. **Zero Pasture Construction & Placement:** `BUILD_PASTURE` and `PLACE COW`/`PLACE SHEEP` actions completely disabled.
3. **Zero Animal Feeding:** `FEED` action, unfed pasture checks, and `PICKUP WHEAT` for feeding completely disabled (`wheat_fed = 0`).
4. **Zero Product Harvesting & Dropping:** Livestock `HARVEST` (Milk/Wool), `PICKUP COW/SHEEP`, and `DROP` (Milk/Wool) actions completely disabled.
5. **Zero Feed Buffer & Wheat Reservation:** `feed_safety_buffer` set to 0. All harvested Wheat is available for regular market sale ($25/unit) or crop cycle management.
6. **Zero Milk/Wool Market Sales:** Milk and Wool sales logic disabled (0 units produced/sold).

### Preserved 40-Tile Footprint Handling:
- The 40-tile target crop footprint (20 Q0 + 20 Q1) is preserved.
- The 5 tiles previously allocated to pastures `(0,0)..(0,2)` remain unbuilt as pastures and are treated according to the natural E08 crop/tile dispatch logic without creating new strategy branches.

---

## 7. Single Independent Variable & Controlled Variables

### Independent Variable (Single):
- **Livestock Subsystem:** **`ON` (E08) $\rightarrow$ `OFF` (E09-01)**.

### Controlled / Frozen Variables (Preserved Invariant from E08):
- **Target Crop Footprint:** Exactly **40 tiles** (20 Q0 + 20 Q1).
- **Workforce Size & Hiring Schedule:** Exactly 4 workers (1 Farmer + 3 Hands, hired at Day 1, 6, 12).
- **Land Expansion:** Day 12 `BUY_LAND` Q1 ($1,000).
- **Spatial Worker Partitioning:** Worker 0 (Farmer Q0), Worker 1 (Hand 1 Q0), Worker 2 (Hand 2 Q1), Worker 3 (Hand 3 Q1).
- **Task Priority:** Water-First priority (`WATER > HARVEST > PLANT`).
- **Cross-Boundary Water Assist:** Preserved from E08.
- **Liquidation Policy:** Day 27+ inventory flush.
- **Benchmark Protocol:** 30 paired episodes vs `pass`, `random`, `starter` with identical seeds (`seed = episode_idx * 100`).

---

## 8. Analysis of Confounders

| Potential Confounder | Mechanism of Action | Mitigation in E09-01 |
| :--- | :--- | :--- |
| **Freed Capital ($4,426.67)** | Capital previously spent on animals/pastures remains in bank balance. | Seed buying logic retains the $300.0 cash reserve floor, preventing runaway seed purchasing. |
| **Freed Worker Turns** | Farmer & Hand 1 no longer travel to `(0,0)..(0,2)` for feeding/harvesting. | Freed turns naturally fall into 40-tile Water-First crop servicing (`WATER > HARVEST > PLANT`). |
| **Wheat Inventory Disposition** | Wheat previously reserved for feed buffer ($5) is now unreserved. | Wheat is sold on market at regular price ($25/unit) during flush or normal sales. |

---

## 9. Benchmark & Evaluation Protocol for E09-01

- **Local Benchmark Script:** `scripts/benchmark_e09_performance.py` (to be created in BUILD).
- **Episodes:** 30 total episodes (10 vs `pass`, 10 vs `random`, 10 vs `starter`).
- **Paired Seeds:** Identical seeds as E08 (`seed = episode_idx * 100`).
- **Primary Metric:** Paired delta ($\text{paired\_delta}_i = \text{money}_{\text{E09-01}, i} - \text{money}_{\text{E08}, i}$).
- **Output Artifact:** `results/e09_livestock_ablation.json`.

---

## 10. Decision Criteria

| Outcome | Quantitative Criteria vs E08 Primary Baseline | Causal & Strategic Conclusion |
| :--- | :--- | :--- |
| **Conclusion A: Livestock Negative in E08** | E09-01 Mean Money consistently exceeds E08 ($\Delta_{\text{causal}} > +\$1,500$); Paired Win Rate vs E08 > 60%; Movement share reduced. | H1 Supported. The livestock subsystem contributed negatively to the E08 40-tile configuration. If E09-01 also recovers E07 level ($13,320.37+), it proves the 40-tile scale was obstructed by livestock overhead. |
| **Conclusion B: Livestock Positive in E08** | E09-01 Mean Money consistently degrades vs E08 ($\Delta_{\text{causal}} < -\$1,000$). | H0 Supported. Livestock provided indirect benefits despite direct loss. |
| **Conclusion C: Inconclusive** | Paired delta within $\pm \$1,000$; Paired Win Rate ~ 50%. | Contribution of livestock is non-deterministic or marginal under current noise. |

---

## 11. Proposed BUILD & VERIFY Plan

1. **BUILD (E09-02):** Implement `LivestockAblationROIAgent` in `src/agricola/strategy/livestock_ablation_roi.py` preserving E08 40-tile logic with `enable_livestock=False` flag.
2. **VERIFY V1 (Functional):** Run single diagnostic episode (`seed=100` vs `starter`) to confirm 40 tile configuration, 0 animal buys, 0 pasture builds, 0 feed actions, 0 milk/wool sales.
3. **VERIFY V2 (Performance):** Execute 30-episode paired benchmark runner (`scripts/benchmark_e09_performance.py`) and output `results/e09_livestock_ablation.json`.
4. **Kaggle Condition:** Proceed to Kaggle submission packaging only if local VERIFY shows consistent improvement over E08 and 100% submission parity test pass.

---

## 12. Open Questions & Recommendations

- None. Methodological alignment completed. E08 (40 tiles, Livestock `ON`) is confirmed as the primary baseline; E07 (24 tiles, Livestock `ON`) is confirmed as secondary historical reference.

---

<!-- END OF DOCUMENT -->
