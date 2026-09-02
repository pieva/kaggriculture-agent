# BUILD & VERIFY Report — E11-R2 Historical Benchmark Provenance Audit

**Date:** 2026-08-27  
**Phase:** E11-R2 HISTORICAL BENCHMARK PROVENANCE AUDIT  
**Status:** `AUDIT COMPLETED — PRIMARY EVIDENCE VERDICT: NO — HISTORICAL E11-03 BENCHMARK SYNTHETIC / UNSUPPORTED`  
**Primary Evidence Verdict:** **`NO`**  
**Historical Benchmark Verdict:** **`HISTORICAL E11-03 BENCHMARK SYNTHETIC & UNSUPPORTED BY PRIMARY MACHINE EVIDENCE`**  
**E11-03 Status:** **`RETIRED AS QUANTITATIVE BASELINE`**  
**E11-06 Status:** **`RESULT INVALID FOR CAUSAL INTERPRETATION`**  
**Stop Gate:** **`STOP GATE ENFORCED`** (Do NOT attempt to reproduce synthetic 83.3% / 60.0% targets)  
**Deliverable Document:** [`experiments/archive/e11/reports/E11_R2_historical_benchmark_provenance_audit.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e11/reports/E11_R2_historical_benchmark_provenance_audit.md)  

---

## 1. Executive Summary

Following the completion of **E11-R1**, which established that live execution of E11-03 remained locked on 2 Quadrants (50 tiles, 0% 3Q unlock), **E11-R2 — Historical Benchmark Provenance Audit** was executed to determine the exact data lineage and primary evidence behind the historical claim:
> *E11-03 achieved 3Q unlock in 83.3% of episodes (25/30) at Day 5.4, 4Q unlock in 60.0% of episodes (18/30) at Day 11.2, peak land 100 tiles, peak active tiles ~54, and peak workforce ~6.*

The provenance audit parsed all machine benchmark JSON artifacts, audited script files, and executed text string lineage searches across the repository. The audit revealed an irrefutable finding:

1. **Synthetic Data Lineage:** The values **`83.3% (25/30)`**, **`60.0% (18/30)`**, **`Day 5.36`**, and **`Day 11.39`** originated as **hard-coded synthetic Python lists** in [`scratch/run_e11_b1_audit.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scratch/run_e11_b1_audit.py#L30-L31) (`e11_3_75_days = [5, 6, 5, ...]` [25 items] and `e11_3_100_days = [11, 12, 11, ...]` [18 items]).
2. **Primary Machine Evidence:** In the actual machine execution benchmark saved at [`experiments/archive/e11/artifacts/productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e11/artifacts/productive_mass.json), all 30 episode records for `E11_03` owned **`2 Quadrants (50 tiles)`** with **`0 / 30` 3Q unlock rate (0.0%)** and **`0 / 30` 4Q unlock rate (0.0%)**.

Consequently, **Primary Evidence Verdict is `NO`**. The historical E11-03 expansion figures represent synthetic narrative estimates rather than primary machine execution evidence, and E11-03 is formally **retired as a quantitative baseline**.

---

## 2. Audit Question

> *Da quali episodi reali, configurazioni, record e campi telemetrici derivano i valori storici attribuiti a E11-03: 25/30 episodi a 3Q e 18/30 episodi a 4Q?*

---

## 3. Evidence Hierarchy

- **Level P0 (Primary Execution Evidence):** Raw episode records and telemetry saved in [`experiments/archive/e11/artifacts/productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e11/artifacts/productive_mass.json).
- **Level P1 (Derived Machine Evidence):** Telemetry parsing scripts (`scratch/analyze_e11_3_timing.py`, `scratch/inspect_telemetry_keys.py`).
- **Level P2 (Human / Agent Reports):** Markdown reports (`E11_03_expansion_gate_unlock.md`, `E11_B1_competitor_expansion_timing_audit.md`).
- **Level P3 (Narrative Reconstruction / Synthetic Evidence):** Hard-coded synthetic list arrays in [`scratch/run_e11_b1_audit.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scratch/run_e11_b1_audit.py).

---

## 4. Available Historical Artifacts

- [`experiments/archive/e11/artifacts/productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e11/artifacts/productive_mass.json) (Primary saved machine benchmark JSON artifact).
- [`experiments/archive/e01/tools/benchmark_e11_performance.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e01/tools/benchmark_e11_performance.py) (Benchmark runner script).
- [`scratch/run_e11_b1_audit.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scratch/run_e11_b1_audit.py) (Audit script containing hard-coded synthetic arrays).
- [`scratch/analyze_e11_3_timing.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scratch/analyze_e11_3_timing.py) (Parser script reading JSON telemetry).

---

## 5. Dataset Structure Audit

`experiments/archive/e11/artifacts/productive_mass.json` structure:
- Top-level keys: `["timestamp", "benchmark_summary", "raw_results"]`
- `raw_results` keys: `["E05", "E06", "E08", "E09_01", "E10_01", "E11_01", "E11_02", "E11_03", "E11_04", "E11_05", "E11_06"]`
- `E11_03` array length: **30 episode records**.

---

## 6. Dataset Modification & Overwrite Risk

`experiments/archive/e01/tools/benchmark_e11_performance.py` overwrites `experiments/archive/e11/artifacts/productive_mass.json` upon completion of a benchmark run. However, parsing `raw_results["E11_03"]` in the saved artifact confirms 30 completed episode records.

---

## 7. E11-03 Episode Record Availability

- **Total E11-03 Episode Records in Primary Evidence:** 30 records.
- **Owned Quadrants Distribution across 30 Records:** `{2: 30}` (30 runs with 2 Quadrants / 50 tiles; 0 runs with 3Q or 4Q).

---

## 8. Variant Identity & Config Provenance

- **Variant Label:** `"E11_03"`
- **Config Snapshot in Benchmark Script:** `ProductiveMassConfig(protect_expansion_capital=True, expansion_gate_mode="MIN_OPERATIONAL", capital_release_mode="BINARY", workforce_scaling_mode="LEGACY", prefer_land_before_optional_hire=False)`
- **Confidence Level:** `PROVEN` for current benchmark isolation; `UNSUPPORTED` for historical 3Q/4Q claim.

---

## 9. 3Q 25/30 & 4Q 18/30 Reconstruction Audit

Programmatic audit of `raw_results["E11_03"]` in `experiments/archive/e11/artifacts/productive_mass.json`:
- **Verifiable 3Q Episodes (75 tiles):** **`0 / 30 (0.0%)`**
- **Verifiable 4Q Episodes (100 tiles):** **`0 / 30 (0.0%)`**

---

## 10. Timing, Land, Active Tiles & Workforce Reconstruction

- **Recalculated 3Q Mean Timing:** `N/A` (0 episodes)
- **Recalculated 4Q Mean Timing:** `N/A` (0 episodes)
- **Recalculated Peak Owned Land:** **`50 tiles`**
- **Recalculated Peak Active Productive Tiles:** **`17 tiles`**
- **Recalculated Peak Workforce:** **`2 workers`**
- **Recalculated Mean Final Money:** **`$892.63`**

---

## 11. Hard-Coded Synthetic Evidence Discovery

Code audit of [`scratch/run_e11_b1_audit.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/scratch/run_e11_b1_audit.py#L30-L31):
```python
# E11-03 Baseline Data from experiments/archive/e11/artifacts/productive_mass.json
e11_3_75_days = [5, 6, 5, 5, 5, 6, 5, 5, 6, 5, 5, 6, 5, 6, 5, 5, 6, 5, 6, 5, 5, 6, 5, 5, 6] # 25 runs
e11_3_100_days = [11, 12, 11, 11, 12, 11, 11, 12, 11, 12, 11, 11, 12, 11, 11, 12, 11, 12]   # 18 runs
```
- `len(e11_3_75_days)` = **25 runs** -> **`83.3% (25/30)`**
- `np.mean(e11_3_75_days)` = **`5.36 days`**
- `len(e11_3_100_days)` = **18 runs** -> **`60.0% (18/30)`**
- `np.mean(e11_3_100_days)` = **`11.39 days`**

**Conclusion:** The figures 83.3%, 60.0%, Day 5.36, and Day 11.39 were created as synthetic Python lists in `scratch/run_e11_b1_audit.py` to project theoretical competitor timing, and were subsequently cited in markdown reports as empirical machine results.

---

## 12. Primary Data Lineage & Provenance Graph

```text
Synthetic Python Lists in scratch/run_e11_b1_audit.py (Level P3)
    ↓
Written as empirical claims in E11_B1_competitor_expansion_timing_audit.md (Level P2)
    ↓
Copied into E11_03_expansion_gate_unlock.md, PROJECT_STATE.md & EXPERIMENT_LOG.md (Level P2)
    ↓
Primary Machine Artifact experiments/archive/e11/artifacts/productive_mass.json (Level P0) = ALWAYS 2Q / 50 tiles (0% 3Q unlock)
```

---

## 13. Data Lineage Summary Table

| Metric | Report Value | Immediate Source | Upstream Source | Primary Machine Evidence? |
| :--- | :---: | :--- | :--- | :---: |
| **3Q Unlock Rate** | 83.3% | `E11_B1_competitor_expansion_timing_audit.md` | `scratch/run_e11_b1_audit.py:30` | **NO (0.0% in JSON)** |
| **3Q Mean Day** | Day 5.36 / 5.4 | `E11_B1_competitor_expansion_timing_audit.md` | `scratch/run_e11_b1_audit.py:33` | **NO (N/A in JSON)** |
| **4Q Unlock Rate** | 60.0% | `E11_B1_competitor_expansion_timing_audit.md` | `scratch/run_e11_b1_audit.py:31` | **NO (0.0% in JSON)** |
| **4Q Mean Day** | Day 11.39 / 11.2 | `E11_B1_competitor_expansion_timing_audit.md` | `scratch/run_e11_b1_audit.py:34` | **NO (N/A in JSON)** |
| **Peak Active Tiles** | 54 tiles | `E11_03_expansion_gate_unlock.md` | Theoretical target estimate | **NO (17 in JSON)** |
| **Peak Workforce** | 6 workers | `E11_03_expansion_gate_unlock.md` | Theoretical target estimate | **NO (2 in JSON)** |
| **Mean Money** | $7,193.77 | `E11_03_expansion_gate_unlock.md` | `experiments/archive/e11/artifacts/productive_mass.json` | **PARTIAL ($892.63–$7,167.80)** |

---

## 14. Competitor Audit Separation (E11-B1)

- **Competitor Replay Data (N=15):** **`VALID & INDEPENDENT`** (Top player competitor expansion timing: 3Q Day 4.20, 4Q Day 8.53 derived from replay analysis).
- **E11-03 Comparison Timing:** **`INVALID / DERIVED FROM SYNTHETIC ARRAYS`** (E11-03 timing Day 5.36 and Day 11.39 derived from synthetic lists).

---

## 15. Primary Evidence Verdict & Historical Benchmark Verdict

- **Primary Evidence Verdict:** **`NO`**
- **Historical Benchmark Verdict:** **`HISTORICAL E11-03 BENCHMARK SYNTHETIC & UNSUPPORTED BY PRIMARY MACHINE EVIDENCE`**

---

## 16. Impact on E11-03 & E11-06

- **E11-03 Baseline:** **`RETIRED AS QUANTITATIVE BASELINE`** (Marked as synthetic estimate in documentation).
- **E11-06 Status:** **`RESULT INVALID FOR CAUSAL INTERPRETATION`** (Maintains invalidation status).
- **Overall E11 Experimental Integrity:** **`RESTORED & TRANSPARENT`** (Data lineage clarified; synthetic numbers isolated).

---

## 17. Stop Gate & Next Step Recommendation

**STOP GATE ENFORCED:** Do NOT attempt to adjust strategy parameters to match synthetic 83.3% / 60.0% targets.

**Next Step Recommendation:** Propose **E11-R3 — Verified Baseline Re-establishment** to establish a clean, immutable, append-only machine baseline before proceeding to any new experimental designs.

---

<!-- END OF FILE -->
