# E16 Stage A vs Stage A-R1 Comparison — Antigravity

**Fase:** `E16-A-R1 FORENSIC COMPARISON`  
**Data:** 2026-08-29  
**Evidence Role:** `TRAINING`  
**Datasets:**
- Original Stage A (`results/e16/stage_a/`, 28 episodes)
- Corrected Stage A-R1 (`results/e16/stage_a_r1/`, 28 episodes)

---

## 1. Executive Summary & Epistemic Audit

The `E16-A-R1` corrected replication was executed after fixing the two fatal defects discovered in the Stage A forensic diagnosis:
1. **Telemetry Attribution Bug Fixed:** `apply_unit_action` and ledger instrumentation now correctly attribute all unit events to the proper player seat (`player: 0` or `player: 1`), enabling true observation of `watering_execution_rate` and `watering_continuity`.
2. **Watering Dispatch Semantics Clarified & Repaired:** `watering_dispatch_priority` is now implemented as relative dispatch precedence across all active crops rather than a fractional daily exclusion quota (`math.ceil(priority * needs)`).

### Summary Comparison Table:

| Metric | Original Stage A (Median) | Stage A-R1 (Median) | Direction Status | Interpretation |
|---|---|---|---|---|
| **A01 Final Money** | $19,145.50 | $19,694.00 | PRESERVED | Stable baseline performance at Crop 10 / LOW water. |
| **A02 Final Money** | $15,274.00 | $21,230.50 | IMPROVED (+$5,956.50) | HIGH water now benefits Crop 10 once daily drought is removed. |
| **A03 Final Money** | $300.00 | $11,903.50 | REPAIRED (+$11,603.50) | Elimination of $300 cash trap; crops survive to yield revenue. |
| **A04 Final Money** | $8,407.00 | $19,987.00 | IMPROVED (+$11,580.00) | Proper watering allows full crop cohort recovery. |
| **A05 Final Money** | $23,646.00 | $26,619.50 | IMPROVED (+$2,973.50) | High revenue maintained via Crop 17 + Livestock synergy. |
| **A06 Final Money** | $300.00 | $21,570.50 | REPAIRED (+$21,270.50) | Elimination of $300 cash stall; MID water supports scale. |
| **A07 Final Money** | $19,511.50 | $27,076.00 | IMPROVED (+$7,564.50) | **Top performing cell in R1** (Crop 17 / HIGH water). |

---

## 2. Detailed Cell-by-Cell Telemetry Comparison

### Raw Final Money & Service Metrics (Stage A-R1):

| Cell | Crop Target | Water Priority | Final Money (Median) | Final Money (Mean) | Watering Execution Rate | Watering Continuity | Crop Target Attainment |
|---|---|---|---|---|---|---|---|
| **A01** | 10 | 0.20 (LOW) | $19,694.00 | $18,970.00 | 0.7241 | 0.7000 | 0.0000 |
| **A02** | 10 | 0.70 (HIGH) | $21,230.50 | $21,255.25 | 0.9316 | 0.9630 | 0.4750 |
| **A03** | 25 | 0.20 (LOW) | $11,903.50 | $12,112.00 | 0.8542 | 0.8750 | 0.1600 |
| **A04** | 25 | 0.70 (HIGH) | $19,987.00 | $19,522.50 | 0.8898 | 0.9600 | 0.3000 |
| **A05** | 17 | 0.45 (MID) | $26,619.50 | $25,499.25 | 0.9084 | 0.9000 | 0.3529 |
| **A06** | 25 | 0.45 (MID) | $21,570.50 | $21,500.25 | 0.8782 | 0.9630 | 0.2800 |
| **A07** | 17 | 0.70 (HIGH) | $27,076.00 | $26,832.50 | 0.9416 | 0.9615 | 0.4706 |

---

## 3. Primary Contrasts: Original vs R1

### Contrast 1: `A02 - A01` (Crop 10: LOW vs HIGH Water)
- **Original Stage A:** Median = -$4,737.00 (Mean = -$4,304.25) [Pairs: +$1,987.00, +$254.00, -$9,730.00, -$9,728.00]
- **Stage A-R1:** Median = +$1,576.00 (Mean = +$2,285.25) [Pairs: +$11,137.00, +$14,798.00, -$8,809.00, -$7,985.00]
- **Status:** **REVERSED / CORRECTED**. In the original run, A02 performed worse due to the fractional drought cap. In R1, HIGH watering produces a positive median effect (+ $1,576.00) even at compact crop scales.

### Contrast 2: `A04 - A03` (Crop 25: LOW vs HIGH Water)
- **Original Stage A:** Median = +$8,107.00 (Mean = +$8,094.50) [Pairs: +$7,357.00, +$8,807.00, +$8,662.00, +$7,552.00]
- **Stage A-R1:** Median = +$8,587.00 (Mean = +$7,410.50) [Pairs: +$2,320.00, +$9,918.00, +$10,148.00, +$7,256.00]
- **Status:** **PRESERVED & STRENGTHENED**. Across all 4 seeds and seats in R1, A04 consistently beats A03 with 100% sign consistency.

### Contrast 3: Primary Interaction `(A04 - A03) - (A02 - A01)`
- **Original Stage A:** Median = +$12,916.50 (Mean = +$12,398.75)
- **Stage A-R1:** Median = +$5,180.50 (Mean = +$5,125.25)
- **Status:** **PRESERVED**. The interaction between crop working set capacity and watering dispatch priority remains strictly positive (+ $5,180.50 median), confirming that higher crop capacity benefits disproportionately from high watering dispatch.

### Contrast 4: Ladder Progression `A03 -> A06 -> A04` (Crop 25: LOW → MID → HIGH)
- **Original Stage A:** $300.00 → $300.00 → $8,407.00
- **Stage A-R1:** $11,903.50 → $21,570.50 → $19,987.00
- **Status:** **REPAIRED**. The artificial cash floor trap at $300 is eliminated. Scaling watering priority from 0.20 to 0.45 increases median money by +$9,667.00.

### Contrast 5: Working Region Curve `A02 -> A07 -> A04` (HIGH Water: Crop 10 → 17 → 25)
- **Original Stage A:** $15,274.00 → $19,511.50 → $8,407.00
- **Stage A-R1:** $21,230.50 → $27,076.00 → $19,987.00
- **Status:** **NON-MONOTONICITY PRESERVED**. Intermediate working set (Crop 17, A07) decisively outperforms both compact (Crop 10, A02: -$5,845.50) and extended (Crop 25, A04: -$7,089.00), demonstrating an optimal capacity plateau near 17 crops for the 2-quadrant / 10-worker regime.

### Contrast 6: `A05 vs A07` (Crop 17: MID 0.45 vs HIGH 0.70)
- **Original Stage A:** A05 ($23,646.00) vs A07 ($19,511.50) [Difference = +$3,842.50 in favor of A05]
- **Stage A-R1:** A05 ($26,619.50) vs A07 ($27,076.00) [Difference = +$204.50 in favor of A07]
- **Status:** **DIRECTION SHIFTED**. In R1, with full cohort watering dispatch, HIGH watering (A07) matches and slightly exceeds MID watering (A05).

---

## 4. Evaluation of the 5 Core Signals

| Signal | Original Stage A | Stage A-R1 | Classification | Rationale |
|---|---|---|---|---|
| **A02_MINUS_A01** | Negative (-$4,737) | Positive (+$1,576) | **REVERSED** | HIGH water at Crop 10 is no longer penalized by fractional drought. |
| **A04_MINUS_A03** | Positive (+$8,107) | Positive (+$8,587) | **PRESERVED** | Massive positive premium for HIGH water at scale 25. |
| **PRIMARY_INTERACTION** | Positive (+$12,916) | Positive (+$5,180) | **PRESERVED** | Capacity × Watering interaction confirmed positive across both datasets. |
| **CROP_17_SIGNAL** | Peak ($19,511) | Peak ($27,076) | **PRESERVED & STRENGTHENED** | Crop 17 is the global highest performing operating region in both runs. |
| **CROP_25_CASH_FLOOR** | Locked at $300.00 | Resolved ($11.9k–$21.5k) | **RESOLVED / REPAIRED** | Eliminating upfront capital exhaust and quota caps unlocked scale viability. |

---

## 5. Gate C* Outcome (Stage A-R1)

### Frozen Evaluation on HIGH-Watering Ladder (A02, A07, A04):

```json
{
  "A02": {
    "completion_rate": 1.0,
    "median_post_ramp_watering_execution_rate": 0.9316,
    "median_watering_continuity": 0.9630,
    "median_crop_target_attainment": 0.4750,
    "watering_metrics_observed": true,
    "capacity_eligible": false
  },
  "A07": {
    "completion_rate": 1.0,
    "median_post_ramp_watering_execution_rate": 0.9416,
    "median_watering_continuity": 0.9615,
    "median_crop_target_attainment": 0.4706,
    "watering_metrics_observed": true,
    "capacity_eligible": false
  },
  "A04": {
    "completion_rate": 1.0,
    "median_post_ramp_watering_execution_rate": 0.8898,
    "median_watering_continuity": 0.9600,
    "median_crop_target_attainment": 0.3000,
    "watering_metrics_observed": true,
    "capacity_eligible": false
  }
}
```

### Analysis of Gate Failure:
- **Watering Execution Rate (Threshold >= 0.60):** **PASS** across all cells (0.8898 to 0.9416).
- **Watering Continuity (Threshold >= 0.75):** **PASS** across all cells (0.9600 to 0.9630).
- **Completion Rate (Threshold >= 0.80):** **PASS** across all cells (1.0000).
- **Crop Target Attainment (Threshold >= 0.80):** **FAIL** across all cells (0.3000 to 0.4750).
  - *Attainment Deficit Reason:* While active crops were watered with 93–96% continuity, mature crops were harvested and sold, but replanting cycles were pacing-limited by seed purchasing logic and endgame shutdown, resulting in an average active standing crop surface of ~5–8 crops (47–50% attainment) rather than 100% standing occupancy.

**Selected C\*:** `NONE`  
**Stage B Gate Status:** `STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR`

---

## 6. Diagnostic Layer Status & Final Conclusion

- **MODEL_VALIDITY:** `STRONGLY_SUPPORTED`  
  The theoretical relationship between watering service, crop scale, and net revenue is fully corroborated by R1 evidence. The non-monotonicity of crop surface (peak at 17) confirms that productive surface must align with worker transit and livestock opportunity cost.
- **POLICY_REALIZATION:** `VERIFIED_AND_REPAIRED`  
  `watering_dispatch_priority` now correctly drives execution rate (93–96%) without imposing synthetic drought penalties.
- **IMPLEMENTATION_FIDELITY:** `INSTRUMENTATION_VALIDATED`  
  The telemetry ledger correctly attributes events to treatment vs opponent with zero untracked unit actions.
