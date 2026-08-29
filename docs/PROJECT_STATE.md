# Project State

**Last update:** 2026-08-29
**Current State:** `E16-A-R1 COMPLETED / STAGE B BLOCKED` (Evidence Role: `TRAINING`)
**Repository Test Suite:** `143/143 PASS`

---

## 1. Current Phase: E16 — Training Phase (Stage A-R1 Completed)

### 1.1 E16-A Original Execution & Forensic Diagnosis
- **Original Stage A:** Executed across all 28 episodes (A01–A07, 2 seeds, 2 seats vs Copilot E15 frozen).
- **Forensic Diagnosis (`E16_STAGE_A_FORENSIC_DIAGNOSIS.md`):**
  - Discovered measurement artifact: `id(farm)` reference mismatch caused `player: -1` in unit events, setting `watering_execution_rate = 0.0` in automated analysis.
  - Discovered policy realization defect: `watering_dispatch_priority` was implemented as a fractional daily exclusion quota (`math.ceil(priority * needs)`), deliberately leaving (1-p) crops unwatered and inducing 2-day drought mortality.
  - Discovered capital exhaustion in 25-crop cells: Day 0 expenditures drove cash to $300 operating floor, causing unrecoverable cash stall in A03/A06.
- **Original Stage A Status:** Completed but causally contaminated; preserved intact under `results/e16/stage_a/` exclusively as forensic baseline evidence.

### 1.2 Implementation Repair (R1, R2, R3)
- **R1 (Watering Semantics):** Clarified and implemented priority as operational worker dispatch precedence over active crops, eliminating fractional drought exclusion.
- **R2 (Ledger Attribution):** Fixed farm/player binding in `apply_unit_action` and event logger so that unit events are accurately attributed to player 0 or player 1.
- **R3 (Derived Metrics & Gates):** Updated telemetry formulas, ramp windows, and gate verification logic.
- **Repair Verification:** 143/143 tests passing (`pytest tests/`), instrumentation gate `PASS`, SHA256 hashes locked.

### 1.3 Corrected Replication: E16-A-R1 Execution
- **Replication Status:** `COMPLETE` (28/28 episodes executed under `results/e16/stage_a_r1/`).
- **Failures:** 0 gameplay failures, 0 infrastructure failures.
- **Integrity Check:** `PASS` (28 episodes, 0 unexpected seeds/cells, 0 hash mismatches, 0 unit actions with `player = -1`, strict treatment/opponent separation).
- **Watering Repair Validation:**
  - `watering_execution_rate`: 0.8898–0.9416 across HIGH cells (vs 0.0 in contaminated run).
  - `watering_continuity`: ~0.96 across all HIGH cells.
  - Synthetic daily drought successfully eliminated.

---

## 2. Quantitative Results: Stage A-R1

### 2.1 Cell-by-Cell Final Money & Telemetry:

| Cell | Crop Target | Water Priority | Final Money (Median) | Final Money (Mean) | Watering Execution Rate | Watering Continuity | Crop Target Attainment |
|---|---|---|---|---|---|---|---|
| **A01** | 10 | 0.20 (LOW) | **$19,694.00** | $18,970.00 | 0.7241 | 0.7000 | 0.0000 |
| **A02** | 10 | 0.70 (HIGH) | **$21,230.50** | $21,255.25 | 0.9316 | 0.9630 | 0.4750 |
| **A03** | 25 | 0.20 (LOW) | **$11,903.50** | $12,112.00 | 0.8542 | 0.8750 | 0.1600 |
| **A04** | 25 | 0.70 (HIGH) | **$19,987.00** | $19,522.50 | 0.8898 | 0.9600 | 0.3000 |
| **A05** | 17 | 0.45 (MID) | **$26,619.50** | $25,499.25 | 0.9084 | 0.9000 | 0.3529 |
| **A06** | 25 | 0.45 (MID) | **$21,570.50** | $21,500.25 | 0.8782 | 0.9630 | 0.2800 |
| **A07** | 17 | 0.70 (HIGH) | **$27,076.00** | $26,832.50 | 0.9416 | 0.9615 | 0.4706 |

### 2.2 Primary Contrasts & Signals:
- **A02 - A01:** Median **+$1,576.00** (Mean +$2,285.25) — *Direction reversed from negative to positive; HIGH watering is now beneficial even at Crop 10.*
- **A04 - A03:** Median **+$8,587.00** (Mean +$7,410.50) — *Strong positive premium for HIGH watering at scale 25 preserved.*
- **Primary Interaction `(A04 - A03) - (A02 - A01)`:** Median **+$5,180.50** (Mean +$5,125.25) — *Positive Capacity × Watering interaction preserved.*
- **Working Region Non-Monotonicity (`A02 -> A07 -> A04`):** $21,230.50 → $27,076.00 → $19,987.00. *Crop 17 is the most economically promising operating region in Stage A-R1, but is NOT a capacity threshold nor an optimum.*
- **Scale 25 Cash Floor Resolution:** A03 ($11.9k) and A06 ($21.5k) recovered from the $300 cash stall.

---

## 3. Capacity Gate C* & Stage B Status

### 3.1 Frozen Capacity Evaluation:
- **Criteria:** Completion Rate >= 0.80, Watering Execution Rate >= 0.60, Watering Continuity >= 0.75, Crop Target Attainment >= 0.80.
- **Evaluation on HIGH Ladder:**
  - **A02 (Crop 10):** Completion=1.0, WaterRate=0.9316, Continuity=0.9630, Attainment=**0.4750** (< 0.80) ➔ **CAPACITY_ELIGIBLE = NO**
  - **A07 (Crop 17):** Completion=1.0, WaterRate=0.9416, Continuity=0.9615, Attainment=**0.4706** (< 0.80) ➔ **CAPACITY_ELIGIBLE = NO**
  - **A04 (Crop 25):** Completion=1.0, WaterRate=0.8898, Continuity=0.9600, Attainment=**0.3000** (< 0.80) ➔ **CAPACITY_ELIGIBLE = NO**

### 3.2 Gate Verdict:
- **Selected C\*:** `NONE`
- **Gate Status:** `STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR`
- **Stage B Executed:** `NO` (Frozen execution protocol strictly enforced; Stage B cannot run without a valid C* capacity anchor).

---

## 4. Epistemic Interpretation & Layer Separation

1. **MODEL_VALIDITY:** `STRONGLY SUPPORTED`
   - Theoretical model predictions regarding irrigation necessity, capital preservation, and surface/workforce alignment are validated.
   - Failure modes in scale cells match theoretical predictions regarding unmaintained footprint costs.
2. **POLICY_REALIZATION:** `NEW BOTTLENECK ISOLATED`
   - The repair successfully eliminated WATER dispatch as the primary bottleneck.
   - However, the policy fails to maintain the nominal crop working-set target (attainment 0.30–0.475 vs >= 0.80 required).
   - Candidate causes include routing/transit overhead, workforce/action capacity allocation, seed replenishment pacing, planting/replanting timing, or other operational constraints. No single cause should be assumed without empirical diagnosis.
3. **IMPLEMENTATION_FIDELITY:** `VERIFIED`
   - Instrumentation and telemetry attribution fully verified with zero untracked unit events.

---

## 5. Decision & Next Session Agenda

> [!IMPORTANT]
> **E16 IS STOPPED FOR TODAY.**
> - DO NOT EXECUTE STAGE B.
> - DO NOT CREATE NEW EXPERIMENTS.
> - DO NOT MODIFY MODEL_SPEC.
> - DO NOT PREPARE KAGGLE SUBMISSIONS.

### Next Session Agenda:
1. Verify repository integrity and E16-A-R1 dataset state.
2. Execute a forensic diagnosis of the low `crop_target_attainment` utilizing the existing 28 R1 runs.
3. Identify and classify the new operational bottleneck (routing, capacity, replanting, market pacing).
4. Decide the next TRAINING experiment design only after completing the diagnosis.
5. Keep Stage B blocked until a valid C* anchor exists or an explicit methodological design decision is frozen.
