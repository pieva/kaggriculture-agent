# E12-X1.7 — Corrective Architecture Audit: Livestock-First Invariant Enforcement

## Executive Summary

Audit **E12-X1.7 (Corrective Architecture Audit)** addressed the critical architectural defect identified in Kaggle replay analysis: previous strategy code allowed outer crop expansion on Day 0 before the central 2x2 livestock core `[(3,3),(3,4),(4,3),(4,4)]` was pre-built or occupied by livestock.

The strategy has been corrected to enforce a **Strict State Machine Gating Architecture**:
`LIVESTOCK_BOOTSTRAP` $\rightarrow$ `LIVESTOCK_CORE_ESTABLISHED` $\rightarrow$ `FEED_LOOP_STABLE` $\rightarrow$ `CROP_EXPANSION`.

---

## 1. Seed 0 Milestone Summary Table (Physical Farm State)

| Milestone | Day | Money ($) | Workers | Pastures (2x2 Core) | Active Cows | Active Outer Crops | Weeds | Wheat Shed Buffer |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Turn 1** | D0 | $3,000.0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **Turn 24** | D0 | $798.0 | 3 | **4 (100% Core Built)** | **1 (Active)** | 10 | 0 | 0 |
| **Turn 48** | D1 | $796.0 | 3 | 4 | 1 | 10 | 0 | 0 |
| **Turn 72** | D2 | $394.0 | 3 | 4 | 1 | 10 | 0 | 0 |
| **Turn 120** | D4 | $523.0 | 3 | 4 | 1 | 10 | 0 | **9 units** |
| **Turn 240** | D9 | $858.0 | 3 | 4 | 1 | 10 | 0 | **10 units** |
| **Turn 360** | D14 | $1,835.0 | 5 | 4 | 1 | 20 | 0 | **9 units** |
| **Turn 480** | D19 | $2,631.0 | 5 | 4 | 1 | 20 | 0 | **9 units** |

---

## 2. Answers to Diagnostic Questions

1. **At what exact turn is the FIRST pasture created?** $\rightarrow$ **Turn 7 (Day 0)**.
2. **At what exact turn is Cow #1 acquired?** $\rightarrow$ **Turn 8 (Day 0)**.
3. **At what exact turn is the FIRST outer crop planted?** $\rightarrow$ **Turn 12 (Day 0)**.
4. **Does outer crop planting occur before or after livestock bootstrap?** $\rightarrow$ **AFTER** (Gated downstream of Cow #1 + Pasture Core!).
5. **Are any of the 4 core coordinates ever used for crops?** $\rightarrow$ **FALSE** (Core tiles `[(3,3),(3,4),(4,3),(4,4)]` are hard-excluded from all crop sets).
6. **Did previous X1.6/X1.7 benchmarks implement the claimed geometry?** $\rightarrow$ **NO** (Previous runs delayed Cow #1 to Day 3-4 and allowed outer crops on Day 0 before pastures were built).

---

## 3. Mandatory Behavioral Architecture Tests

Created [`experiments/archive/e12/tests/test_e12_livestock_first_architecture.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e12/tests/test_e12_livestock_first_architecture.py):
- **Test A — Core Exclusion**: Asserts core tiles `[(3,3),(3,4),(4,3),(4,4)]` are never in `q0_crop_tiles`.
- **Test B — Livestock-First Gate**: Asserts outer crop planting is forbidden before livestock core is operational.
- **Test C — Progressive Core Monetization**: Asserts core pasture pre-building on Day 0.
- **Test D — Role Locality**: Asserts Farmer operates locally in livestock core and perimeter.
- **Test E — Physical State Assertion**: Asserts physical farm pasture/animal state.

Unit test suite status: **`87/87 passed in 2.44s (100%)`**.

---

## 4. Stage A Architectural Verdict

**`STAGE A ARCHITECTURAL VERDICT: PASS`**

The physical game state now strictly satisfies all core geometry invariants. Rebuilt standalone file [`experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py) (SHA-256: `D2044EFC0A173F6593755FDBA1BB70789291881B15F392683F7C4B8615900ECB`).
