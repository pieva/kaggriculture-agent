# SHIP / Experimental Closure Report — E08 Productive Scale Optimization (`E08-06`)

**Date:** 2026-08-26  
**Phase:** SHIP / Experimental Closure  
**Status:** `E08 COMPLETED & CLOSED`  
**Decision:** **`E08 FALSIFIED — SHIPPED BASELINE E06 REMAINS ACTIVE`**  
**Strategy Class:** `HybridLivestockClusterROIAgent`  
**Active Shipped Agent Entrypoint:** [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py) (`WaterFirstHIRENWClusterROIAgent` — E06)  

---

## 1. Summary of Experimental Cycle E08

The experimental cycle **E08 — Productive Scale Optimization** followed the complete supervised lifecycle:

1. **E08-01 DEFINE:** Formulated hypothesis that expanding target productive crop tiles from 24 to 40 across Q0+Q1 would utilize owned land and increase Mean Final Money. (Approved).
2. **E08-02 PLAN:** Designed 40-tile layout, spatial worker partitioning (Workers 0-1 in Q0, Workers 2-3 in Q1), cross-boundary water assist, and staggered seed purchasing with $300 cash floor. (Approved with metric corrections).
3. **E08-03 BUILD:** Implemented `HybridLivestockClusterROIAgent` config/telemetry extensions, spatial dispatcher, and backlog loggers. Verified 100% unit test pass (42/42) and submission parity. (Approved).
4. **E08-04 VERIFY:** Conducted V1 functional verification (`FUNCTIONAL VERIFY PASS WITH WARNINGS`) and V2 30-episode paired benchmark (`VERIFY FAIL`). E08 Mean Money fell to **$11,880.30** (-10.81% vs E07 $13,320.37, -52.46% vs E06 $24,987.67).
5. **E08-05 & E08-05B REVIEW:** Reconciled baseline values, audited E06 metrics, confirmed worker throughput saturation (61.6% movement share, 17.96 `plant_pending` backlog/day), and identified livestock direct net financial loss (-$3,977.34). Defined single-variable ablation for E09. (Approved).
6. **E08-06 SHIP:** Formally closed E08 as a falsified experimental hypothesis.

---

## 2. Final Deployment Decision

- **Kaggle Candidate:** **NO.** E08 (`HybridLivestockClusterROIAgent` 40 tiles) is **NOT candidated** for Kaggle submission.
- **Active Shipped Baseline:** **E06 (`WaterFirstHIRENWClusterROIAgent`)** remains the active shipped baseline in [`src/agricola/agent.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/agent.py) and [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py).
- **Code & Artifact Preservation:** All E08 strategy code, unit tests, benchmark runners, and JSON result artifacts (`experiments/archive/e08/artifacts/productive_scale.json`) are preserved in the repository as valid empirical evidence.

---

## 3. Transition to E09

With E08 formally closed, the repository is ready for **E09 DEFINE — Livestock Subsystem Ablation**:
- **Primary Hypothesis:** Complete ablation of the livestock subsystem (0 cows, 0 sheep, 0 pastures, 0 feed actions) on the frozen E07 24-tile footprint with 4 workers will eliminate livestock financial loss (-$3,977) and free worker turns, increasing Mean Final Money above E07 ($13,320.37).

---

<!-- END OF DOCUMENT -->
