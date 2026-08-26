# PLAN Evidence — E07 Configurable Competitive Baseline (`E07-03`)

**Date:** 2026-08-26  
**Phase:** PLAN  
**Status:** `PLAN COMPLETED`  
**Decision:** `GO FOR BUILD WITH OPEN PARAMETERS`  

Refer to the complete implementation plan document: [`docs/plans/E07_Competitive_Baseline_Reconstruction.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E07_Competitive_Baseline_Reconstruction.md).

---

## 1. Executive Summary

E07 designs the 2nd-generation baseline strategy: `HybridLivestockClusterROIAgent`. It introduces a multi-capability modular architecture (Livestock Cashflow Engine, 2-Quadrant Expansion `BUY_LAND`, 4-Worker HIRE Schedule, Premium-First Market Brokerage, 4-Phase Lifecycle, and End-Game Asset Liquidation).

All quantitative parameters are exposed via `CompetitiveConfig` as **`OPEN / TUNABLE`**.

---

## 2. Open Parameters Table (`OPEN / TUNABLE`)

| Parameter | Initial Candidate Value | Status |
| :--- | :---: | :---: |
| **Target Quadrants** | `2` (50 tiles) | **`OPEN`** |
| **Active Crop Tiles** | `24` tiles | **`OPEN`** |
| **Wheat Tiles (Feed)** | `6` tiles | **`OPEN`** |
| **Melon Tiles (Cash)** | `12` tiles | **`OPEN`** |
| **Carrot Tiles (Flex)** | `6` tiles | **`OPEN`** |
| **Target Workers** | `4` (1 Farmer + 3 Hands) | **`OPEN`** |
| **Hiring Schedule** | `(1, 6, 12)` at `hour == 0` | **`OPEN`** |
| **Target Cows** | `4` cows (cutoff Day 20) | **`OPEN`** |
| **Target Sheep** | `2` sheep (cutoff Day 18) | **`OPEN`** |
| **Expansion Day** | `Day 12` | **`OPEN`** |
| **Cash Reserve Float** | `$300.0` | **`OPEN`** |
| **Stop Melon Day** | `Day 18` (12d growth cycle) | **`OPEN`** |
| **Liquidation Start Day** | `Day 27` (100% shed flush) | **`OPEN`** |
| **Market Queue Priority** | `Milk/Wool > Melon > Carrot` | **`OPEN`** |

---

## 3. Implementation Sequence (B1–B10)

`B1 Config & Instrumentation` $\rightarrow$ `B2 Phase Manager` $\rightarrow$ `B3 Land Manager` $\rightarrow$ `B4 Workforce Manager` $\rightarrow$ `B5 Crop Manager` $\rightarrow$ `B6 Livestock & Feed` $\rightarrow$ `B7 Task Dispatcher` $\rightarrow$ `B8 Market Broker` $\rightarrow$ `B9 End-Game` $\rightarrow$ `B10 Integration & pytest`

---

## 4. Decision

> **`GO FOR BUILD WITH END-GAME CORRECTIONS`**
