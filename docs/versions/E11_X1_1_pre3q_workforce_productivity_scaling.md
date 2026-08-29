# BUILD & VERIFY Report — E11-X1.1 Pre-3Q Workforce Productivity Scaling

**Date:** 2026-08-27  
**Phase:** E11-X1.1 PRE-3Q WORKFORCE PRODUCTIVITY SCALING  
**Status:** `E11-X1.1 BUILD + REDUCED LOCAL VERIFY COMPLETED — STOP GATE B ENFORCED`  
**Run ID:** `E11-X1.1-20260827-091219`  
**Stage Evaluated:** Stage B (5 Paired Episodes)  
**Provenance Verification Verdict:** **`PASS (100% MATCH)`**  
**Config SHA-256:** `20e9bdc18e61454807ee15ccaa05b51dd58c4ebc0a6b7d2ee21b82fb365a1ea7`  
**Episodes SHA-256:** `fc8baf9a2981e3f43398ae18aeedefbe60a3ecbb6bcfbc16fd1e0b0e5d9fe3d0`  
**Strategy File:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Runner Script:** [`scripts/benchmark_e11_x1_1.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/benchmark_e11_x1_1.py)  
**Verifier Script:** [`scripts/verify_e11_run_provenance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/verify_e11_run_provenance.py)  
**Dataset Directory:** [`results/e11/E11-X1.1-20260827-091219`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11/E11-X1.1-20260827-091219)  

---

## 1. Executive Summary

**E11-X1.1 — Pre-3Q Workforce Productivity Scaling** evaluated a single controlled modification over the verified baseline **`E11-VB1`**: attempting to scale workforce pre-3Q (`workforce_scaling_mode = "PRE_3Q_PRODUCTIVITY_SCALING"`, `target_tiles_per_worker = 5.0`) to expand active productive footprint from 17 tiles toward competitor levels (35–45 tiles) and generate the revenue required for 3Q land purchase.

The progressive evaluation protocol executed **Stage A (Smoke Test, 1 Episode)** and **Stage B (Mini Verification, 5 Paired Episodes vs E11-VB1)**. Stage B produced **0 / 5 3Q unlock (0.0%)**, with Mean Final Money of **$429.00 ± $0.00**, peak workforce of **2 workers**, and peak active tiles of **17**.

Per the mandatory progressive Stop Gate rules (*"Se Stage B = 0/5 a 3Q: Fermarsi. NON eseguire 10 episodi"*), **Stage C (10 Paired Episodes) was NOT executed**, and **30-episode validation is NOT recommended**.

Empirical trace inspection revealed a **fundamental environment constraint**:
> **In Kaggriculture, 2 Quadrants (50 tiles) hard-caps workforce at max 2 workers (1 Farmer + 1 Hand).**
Attempts to issue `HIRE` actions for a 3rd worker on 2 Quadrants are rejected by the environment mechanics. Therefore, workforce CANNOT be scaled to 3+ workers before 3Q (75 tiles) is unlocked.

---

## 2. Baseline & Controlled Single-Variable Delta

- **Authoritative Baseline:** `E11-VB1` (`Run ID: E11-VB1-20260827-084428`, Mean Money $429.00, 3Q unlock 0.0%, 2 workers).
- **Controlled Change:** Workforce scaling policy before 3Q unlock.

### Config Delta Table

| Parameter Field | E11-VB1 Baseline Value | E11-X1.1 Treatment Value | Description |
| :--- | :---: | :---: | :--- |
| `workforce_scaling_mode` | `"LEGACY"` | `"PRE_3Q_PRODUCTIVITY_SCALING"` | Workforce scaling mode before 3Q land purchase |
| `target_tiles_per_worker` | `7.0` | `5.0` | Target workload ratio per worker to trigger hiring |

*All other 40+ fields of `ProductiveMassConfig` remained 100% invariant.*

---

## 3. Telemetry & Provenance Protocol

- **Dataset Storage Path:** `results/e11/E11-X1.1-20260827-091219/`
  - `config.json` (SHA-256: `20e9bdc18e61454807ee15ccaa05b51dd58c4ebc0a6b7d2ee21b82fb365a1ea7`)
  - `episodes.json` (SHA-256: `fc8baf9a2981e3f43398ae18aeedefbe60a3ecbb6bcfbc16fd1e0b0e5d9fe3d0`)
  - `summary.json` (Recalculated summary metrics matching 100%)
- **Provenance Verifier:** **`PASS (100% MATCH)`** via [`scripts/verify_e11_run_provenance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/verify_e11_run_provenance.py).

---

## 4. Progressive Stage Results Summary

### Stage A — Smoke Test (1 Episode, Seed 0 vs `pass`)
- **Status:** PASS
- **Result:** Money $429.00, Q = 2, Active Tiles = 17, Workers = 2, Provenance PASS.

### Stage B — Mini Verification (5 Paired Episodes vs E11-VB1)
- **Status:** COMPLETED — STOP GATE ENFORCED
- **E11-VB1 Baseline:** Mean Money $429.00, 3Q Unlock Rate 0.0% (0/5), Peak Workers 2
- **E11-X1.1 Treatment:** Mean Money $429.00, 3Q Unlock Rate 0.0% (0/5), Peak Workers 2
- **3Q Unlock Result:** **`0 / 5 (0.0%)`**

### Stage C — Standard Benchmark (10 Paired Episodes)
- **Status:** **`NOT EXECUTED`** (Halted at Stop Gate B).

---

## 5. Benchmark Metrics Summary Matrix (Stage B, N=5 Paired Episodes)

| Metric Dimension | E11-VB1 Baseline | E11-X1.1 Treatment | Delta / Status |
| :--- | :---: | :---: | :--- |
| **3Q / 75 tiles Unlock Rate** | **`0.0% (0/5)`** | **`0.0% (0/5)`** | **`0.0% (Stop Gate B Enforced)`** |
| **3Q Mean Unlock Day** | N/A | **N/A** | Never unlocked |
| **4Q / 100 tiles Unlock Rate** | 0.0% | **0.0% (0/5)** | Never unlocked |
| **Mean Final Money** | **$429.00** | **$429.00** | **± $0.00** |
| **Median / Std Dev / Min / Max** | $429.00 / ±$0 / $429 / $429 | $429.00 / ±$0 / $429 / $429 | Deterministic spread |
| **Mean Owned Quadrants** | 2.00 (50 tiles) | **2.00 (50 tiles)** | 50 tiles max |
| **Mean Peak Active Tiles** | 16.93 | **16.80** | Active tiles trapped at ~17 |
| **Mean Peak Workforce** | 2.0 | **2.0** | Environment hard-cap (max 2) |
| **Livestock Activation** | 0.0% | **0.0%** | 0 animals |

---

## 6. Historical Productivity Sanity Check & Competitor Reference

| Metric Dimension | Historical E06 (9-tile multi-worker) | E11-VB1 Baseline | E11-X1.1 Treatment | Top Competitor Reference |
| :--- | :---: | :---: | :---: | :---: |
| **Owned Land** | 9 tiles | **50 tiles** | **50 tiles** | **75 – 100 tiles** |
| **Peak Workforce** | 2 – 3 workers | **2 workers** | **2 workers** | **4 – 6 workers @ 75** |
| **Active Tiles** | 9 active tiles | **17 active tiles** | **17 active tiles** | **35 – 45 active tiles @ 75** |
| **Mean Final Money** | **~$25,000** | **$429.00** | **$429.00** | **~$70,000 – $75,000+** |

*Sanity Check Verdict:* Historical E06 achieved ~$25k on 9 tiles with 2-3 workers. E11-X1.1 is hard-capped at 2 workers on 50 tiles due to environment mechanics, producing only 17 active tiles.

---

## 7. Dominant Bottleneck Discovery

Step-by-step trace of `E11-X1.1` hiring attempts:
1. **Day 0 (step 0):** `HIRE` executes. Worker 2 (Hand 1) is spawned. Workforce = 2.
2. **Day 1 (step 24):** `HIRE` is attempted for Worker 3. Environment rejects action (2 Quadrants allows max 2 workers: 1 Farmer + 1 Hand).
3. **Days 2–11 (steps 48–264):** `HIRE` is repeatedly attempted at hour 0, but rejected every single day.
4. Workforce remains **2 workers** throughout the episode.

**Conclusion:** Scaling workforce to 3+ workers to boost revenue throughput BEFORE 3Q land purchase is impossible under Kaggriculture game mechanics. The land purchase ($1,100 threshold) MUST be unlocked by optimizing the revenue throughput of the existing 2 workers on 50 tiles.

---

## 8. Validation Verdict & Recommendations

### Validation Verdict: **`X1.1 NOT VALIDATED`** (Stage B 3Q unlock rate = 0/5).

### 30-Episode Validation Recommendation: **`NO`** (Do NOT execute 30-episode run).

### Next Step Recommendation
**STOP GATE B ENFORCED:** Propose **`E11-X1.2 — 2-Worker Revenue Throughput Optimization`**, focusing on optimizing crop rotation turnover (fast Carrot/Tomato rotation) for the 2 allowed workers on 50 tiles to cross the $1,100 threshold and unlock 3Q.

---

<!-- END OF FILE -->
