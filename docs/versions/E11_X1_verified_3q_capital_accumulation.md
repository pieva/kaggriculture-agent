# BUILD & VERIFY Report — E11-X1 Verified 3Q Capital Accumulation

**Date:** 2026-08-27  
**Phase:** E11-X1 VERIFIED 3Q CAPITAL ACCUMULATION  
**Status:** `E11-X1 BUILD + REDUCED LOCAL VERIFY COMPLETED — STOP GATE B ENFORCED`  
**Run ID:** `E11-X1-20260827-090315`  
**Stage Evaluated:** Stage B (5 Paired Episodes)  
**Provenance Verification Verdict:** **`PASS (100% MATCH)`**  
**Config SHA-256:** `da0493e56842caccc52cfad8faeccecd8f2fbff6eb77fb0450536c2a13cc7eb5`  
**Episodes SHA-256:** `d77474e72f5dd35abd3cfc941fc3aa7eaedbe8ecf1ebf4ac9bdecced91fb5e4e`  
**Strategy File:** [`src/agricola/strategy/productive_mass_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/productive_mass_roi.py)  
**Runner Script:** [`scripts/benchmark_e11_x1.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/benchmark_e11_x1.py)  
**Verifier Script:** [`scripts/verify_e11_run_provenance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/verify_e11_run_provenance.py)  
**Dataset Directory:** [`results/e11/E11-X1-20260827-090315`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11/E11-X1-20260827-090315)  

---

## 1. Executive Summary

**E11-X1 — Verified 3Q Capital Accumulation** evaluated a single controlled modification over the verified baseline **`E11-VB1`**: introducing a `DISCIPLINED_ACCUMULATION` policy (`accumulation_3q_mode = "DISCIPLINED_ACCUMULATION"`, `accumulation_3q_optional_reserve = $500.0`) designed to resolve the verified **Expansion Capital Protection Deadlock** during 3Q land accumulation.

The progressive evaluation protocol executed **Stage A (Smoke Test, 1 Episode)** and **Stage B (Mini Verification, 5 Paired Episodes vs E11-VB1)**. Stage B produced **0 / 5 3Q unlock (0.0%)**, with Mean Final Money of **$429.00 ± $0.00**.

Per the mandatory progressive Stop Gate rules (*"Se Stage B = 0/5 a 3Q: Fermarsi. NON eseguire 10 episodi. Diagnosticare il deadlock residuo"*), **Stage C (10 Paired Episodes) was NOT executed**, and **30-episode validation is NOT recommended**.

Empirical trace diagnosis revealed the exact residue deadlock: lowering the optional reserve floor to $500 allowed discretionary Melon ($320) and Tomato ($200) seed purchases as soon as liquid cash crossed $500–$700, continuously draining liquid cash float and preventing cash from reaching the **$1,100 threshold required for `BUY_LAND` Q2**.

---

## 2. Baseline & Controlled Single-Variable Delta

- **Authoritative Baseline:** `E11-VB1` (`Run ID: E11-VB1-20260827-084428`, Mean Money $429.00, 3Q unlock 0.0%).
- **Controlled Change:** Essential spending vs next-land capital accumulation during `ACCUMULATE_3Q` (when `owned_quadrants == 2`).

### Config Delta Table

| Parameter Field | E11-VB1 Baseline Value | E11-X1 Treatment Value | Description |
| :--- | :---: | :---: | :--- |
| `accumulation_3q_mode` | `"LEGACY_LOCK"` | `"DISCIPLINED_ACCUMULATION"` | Spending deferral policy during 3Q land accumulation |
| `accumulation_3q_optional_reserve` | `$1,300.0` | `$500.0` | Reserve floor for discretionary seed buys during 3Q land accumulation |

*All other 40+ fields of `ProductiveMassConfig` remained 100% invariant.*

---

## 3. Telemetry & Provenance Protocol

- **Dataset Storage Path:** `results/e11/E11-X1-20260827-090315/`
  - `config.json` (SHA-256: `da0493e56842caccc52cfad8faeccecd8f2fbff6eb77fb0450536c2a13cc7eb5`)
  - `episodes.json` (SHA-256: `d77474e72f5dd35abd3cfc941fc3aa7eaedbe8ecf1ebf4ac9bdecced91fb5e4e`)
  - `summary.json` (Recalculated summary metrics matching 100%)
- **Provenance Verifier:** **`PASS (100% MATCH)`** via [`scripts/verify_e11_run_provenance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scripts/verify_e11_run_provenance.py).

---

## 4. Progressive Stage Results Summary

### Stage A — Smoke Test (1 Episode, Seed 0 vs `pass`)
- **Status:** PASS
- **Result:** Money $429.00, Q = 2, Active Tiles = 17, Workers = 2, Provenance PASS.

### Stage B — Mini Verification (5 Paired Episodes vs E11-VB1)
- **Status:** COMPLETED — STOP GATE ENFORCED
- **E11-VB1 Baseline:** Mean Money $429.00, 3Q Unlock Rate 0.0% (0/5)
- **E11-X1 Treatment:** Mean Money $429.00, 3Q Unlock Rate 0.0% (0/5)
- **3Q Unlock Result:** **`0 / 5 (0.0%)`**

### Stage C — Standard Benchmark (10 Paired Episodes)
- **Status:** **`NOT EXECUTED`** (Halted at Stop Gate B).

---

## 5. Benchmark Metrics Summary Matrix (Stage B, N=5 Paired Episodes)

| Metric Dimension | E11-VB1 Baseline | E11-X1 Treatment | Delta / Status |
| :--- | :---: | :---: | :--- |
| **3Q / 75 tiles Unlock Rate** | **`0.0% (0/5)`** | **`0.0% (0/5)`** | **`0.0% (Stop Gate B Enforced)`** |
| **3Q Mean Unlock Day** | N/A | **N/A** | Never unlocked |
| **4Q / 100 tiles Unlock Rate** | 0.0% | **0.0% (0/5)** | Never unlocked |
| **Mean Final Money** | **$429.00** | **$429.00** | **± $0.00** |
| **Median / Std Dev / Min / Max** | $429.00 / ±$0 / $429 / $429 | $429.00 / ±$0 / $429 / $429 | Deterministic spread |
| **Mean Owned Quadrants** | 2.00 (50 tiles) | **2.00 (50 tiles)** | 50 tiles max |
| **Mean Peak Active Tiles** | 16.93 | **16.80** | Farm active (16-17 tiles) |
| **Mean Peak Workforce** | 2.0 | **2.0** | 1 Farmer + 1 Hand |
| **Livestock Activation** | 0.0% | **0.0%** | 0 animals |

---

## 6. Competitor Benchmark Reference Comparison

| Metric Dimension | E11-VB1 Baseline | E11-X1 Treatment | Top Competitor Reference |
| :--- | :---: | :---: | :---: |
| **3Q / 75 tiles Unlock Day** | **Never (0.0%)** | **Never (0.0%)** | **Day 4.20** |
| **4Q / 100 tiles Unlock Day** | **Never (0.0%)** | **Never (0.0%)** | **Day 8.53** |
| **Mean Final Money** | **$429.00** | **$429.00** | **~$70,000 – $75,000+** |

---

## 7. Residue Deadlock Diagnosis

Step-by-step trace of `E11-X1` during `ACCUMULATE_3Q` (Days 1–18):
1. **Day 1 (post-Q1 buy):** Cash = **$899.0**. `optional_reserve` = `$500.0`.
2. $899.0 - 200.0 (Tomato) = $699.0 $\ge \$500.0$. Tomato 4 ($200) is bought! Cash drops to **$699.0**.
3. **Day 4:** Carrots harvest (+ $210). Cash reaches **$909.0**.
4. $909.0 - 320.0 (Melon) = $589.0 $\ge \$500.0$. Melon 4 ($320) is bought! Cash drops to **$589.0**.
5. **Day 5:** Wheat harvests (+ $150). Cash reaches **$739.0**.
6. **Day 6:** Tomato 4 ($200) is bought again! Cash drops to **$539.0**.

**Conclusion:** Lowering the optional reserve floor to $500 allowed discretionary Melon ($320) and Tomato ($200) seed purchases as soon as liquid cash reached $700–$900. These seed buys repeatedly drained liquid cash float, keeping cash trapped in the $539–$909 range and preventing it from ever reaching the **$1,100 threshold required for `BUY_LAND` Q2**.

---

## 8. Validation Verdict & Recommendations

### Validation Verdict: **`X1 NOT VALIDATED`** (Stage B 3Q unlock rate = 0/5).

### 30-Episode Validation Recommendation: **`NO`** (Do NOT execute 30-episode run).

### Next Step Recommendation
**STOP GATE B ENFORCED:** Propose targeted **`E11-X1.1 — Strict 3Q Land Float Lock`**, where discretionary seed purchases are strictly blocked during `ACCUMULATE_3Q` until cash reaches **$1,100** and `BUY_LAND` Q2 executes.

---

<!-- END OF FILE -->
