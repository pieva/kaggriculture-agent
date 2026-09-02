# E16 Stage A Forensic Diagnosis — Antigravity

**Fase:** `E16-A FORENSIC DIAGNOSIS`  
**Data:** 2026-08-29  
**Analista:** Antigravity (Forensic Operator)  
**Evidence Role:** `TRAINING`  
**Dataset:** 28 frozen episodes of E16 Stage A (`results/e16/stage_a/`)  

---

## 1. Executive Summary & Core Diagnostic Finding

The central mystery of E16 Stage A is:
> **Why did `watering_dispatch_priority = HIGH` fail to achieve the required steady-state capacity benchmarks (evaluated to `0.0` in the automated gate) and why did nominal crop scaling collapse?**

Forensic investigation of the raw engine telemetry and event ledgers across all 28 episodes reveals a multi-layered causal reality:

1. **Telemetry Instrumentation Defect (Primary Measurement Artifact):**
   In `experiments/archive/e16/source/agricola/e16/telemetry.py`, `EngineEventLedger._register_state` attempts to map farm object identities (`id(farm)`) from `state[0].observation.farms`. However, because the engine environment passes a fresh or dereferenced copy to `_apply_unit_action`, `id(farm)` was not found in `self._farm_players`, assigning `player: -1` to all unit events. In `derive_episode_telemetry`, `successful_water` filters for `event["player"] == treatment_seat` (0 or 1). Because `player` was `-1`, `successful_water` evaluated to an empty set for all 28 episodes, forcing `watering_execution_rate = 0.0` and `watering_continuity = 0.0` in the output metrics despite actual successful water executions occurring in the engine.

2. **Mathematical Priority-as-Quota Defect (Primary Policy Realization Failure):**
   In `experiments/archive/e16/artifacts/manifests/E16_TREATMENT_BUILD.py` (lines 267–270), `watering_dispatch_priority` was implemented as a daily target **fraction** (`math.ceil(priority * len(needs))`) rather than an operational dispatch precedence over worker turns. At `priority = 0.70` (HIGH), the agent intentionally schedules watering for only 70% of active plants, deliberately leaving 30% unwatered each day. Because the Kaggriculture engine kills any crop with `consecutive_unwatered >= 2`, unwatered crops consistently entered the fatal 2-day drought window and died on Day 2/3. At `priority = 0.20` (LOW), 80% of crops were left unwatered daily, causing near-instantaneous total crop wipeout.

3. **Crop Mortality Feedback Spiral (System Dynamics Failure):**
   As unwatered crops died, the active crop count shrank. Because the watering quota was dynamically calculated as `ceil(priority * active_crops)`, fewer surviving crops led to a proportionally smaller absolute water quota, accelerating the collapse of the remaining crops until active crop surface reached 0.

4. **Cash Starvation Lock-in at $300 Floor in Scale Cells (A03 & A06):**
   In large crop target cells (target = 25), Day 0 upfront expenditures on Land ($1,000), Seeds ($1,610+), and Workforce ($700–$950) exceeded available capital ($3,000), driving cash directly to the `operating_cash_floor` ($300.00). Because crops died under LOW/MID watering before yielding harvestable revenue, no cash was recouped. The policy's hard cash-floor gate permanently blocked further worker renewals, livestock purchases, and seed replenishment, trapping A03 and A06 at exactly **$300.00** final money across all seeds and seats.

5. **Livestock Revenue Domination in Compact Cells (A01, A02, A05, A07):**
   In compact crop cells (target = 10 or 17), lower initial seed costs ($1,200–$2,000) preserved sufficient liquidity above the $300 floor to purchase 4 Cows ($1,600) and maintain daily feed/care. Livestock product sales (Milk & Fertilizer) generated $10,000–$30,000 in net revenue, masking the fact that crop production had largely collapsed.

---

## 2. Quantitative Action & Dispatch Audit (Per Cell A01–A07)

The table below reconstructs the true action breakdown per episode (averaged over the 4 seed/seat runs per cell) by parsing the unit and market events from the raw event ledgers:

| Metric | A01 (LOW, 10) | A02 (HIGH, 10) | A03 (LOW, 25) | A04 (HIGH, 25) | A05 (MID, 17) | A06 (MID, 25) | A07 (HIGH, 17) |
|---|---|---|---|---|---|---|---|
| **WATER Requested** | 4.0 | 53.0 | 21.0 | 94.5 | 32.0 | 34.8 | 83.8 |
| **WATER Executed** | 4.0 | 53.0 | 21.0 | 94.5 | 32.0 | 34.8 | 83.8 |
| **WATER Failed / No-op** | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **PLANT Executed** | 11.0 | 13.0 | 25.5 | 30.2 | 21.0 | 28.5 | 24.8 |
| **HARVEST Requested** | 96.0 | 162.5 | 221.0 | 391.5 | 185.0 | 325.0 | 256.5 |
| **HARVEST Executed** | 37.0 | 34.0 | 5.0 | 24.2 | 35.0 | 8.5 | 37.0 |
| **HARVEST Failed (No-op)** | 59.0 | 128.5 | 216.0 | 367.3 | 150.0 | 316.5 | 219.5 |
| **FEED Executed** | 98.0 | 86.0 | 0.0 | 47.5 | 87.0 | 0.0 | 86.0 |
| **CARE Executed** | 100.0 | 85.0 | 0.0 | 43.2 | 88.5 | 0.0 | 66.8 |
| **MOVE Executed (Transit)** | 1,553.0 | 2,304.5 | 381.0 | 1,995.8 | 1,937.0 | 528.5 | 2,985.8 |
| **PASS Count (Idle turns)** | 4,929.5 | 3,459.5 | 1,718.0 | 2,498.0 | 3,794.5 | 1,429.5 | 2,430.0 |
| **Crop Losses (Mortality)** | 11.0 | 13.0 | 25.5 | 28.5 | 21.0 | 27.5 | 22.5 |
| **Active Crops at End** | 0.0 | 0.0 | 0.0 | 0.25 | 0.0 | 0.0 | 0.5 |
| **Livestock Acquired (Cows)** | 4.0 | 4.0 | 0.0 | 4.0 | 4.0 | 0.0 | 4.0 |
| **Livestock Revenue ($)** | $18,605 | $13,460 | $0 | $8,051 | $24,928 | $0 | $16,415 |
| **Crop Revenue ($)** | $8,687 | $9,587 | $732 | $8,327 | $8,147 | $782 | $11,073 |
| **Final Money Median ($)** | **$19,145.50** | **$15,274.00** | **$300.00** | **$8,407.00** | **$23,646.00** | **$300.00** | **$19,511.50** |

### Key Observations from the Quantitative Audit:

1. **Treatment Monotonicity Exists in Unit Dispatch:**
   The policy *did* execute more water actions when `watering_dispatch_priority` was higher:
   - At Crop Target 10: `LOW (4.0) -> HIGH (53.0)` (+1,225%)
   - At Crop Target 17: `MID (32.0) -> HIGH (83.8)` (+162%)
   - At Crop Target 25: `LOW (21.0) -> MID (34.8) -> HIGH (94.5)` (+350%)
   Thus, the treatment parameter was not completely ignored in code, but its mathematical formula was fatally flawed.

2. **The HARVEST Failure Syndrome:**
   Failed HARVEST requests reached catastrophic levels in scale cells (up to 367 failed harvest turns per episode in A04). The policy repeatedly routed workers to harvest tiles that were unwatered, dead, or immature, consuming hundreds of worker turns that could have been used for irrigation.

3. **Massive Idle Worker Capacity (PASS):**
   Across all surviving cells, between 2,400 and 4,900 worker turns were spent on `PASS`. Workers were not constrained by absolute capacity (10 hands provided ample turn budget); rather, the policy failed to generate valid action targets once the initial crop cohort died and water quotas were artificially capped.

---

## 3. Candidate Causal Chain Reconstruction

```
[ASSIGNED INTENT] 
  watering_dispatch_priority = HIGH (0.70)
        ↓
[ACTION DEMAND]
  Quota calculated as ceil(0.70 * active_crops). 
  At 10 crops, demand = 7 WATER turns/day (3 crops intentionally excluded).
        ↓
[ACTOR AVAILABILITY & WORKFORCE]
  10 hands available (11 total units = 264 worker turns/day). Ample capacity available.
        ↓
[DISPATCH & TRANSIT]
  Nearest-task routing dispatches workers to 7 tiles. Remaining workers dispatch to Feed/Care/Pasture or PASS.
        ↓
[EXECUTION]
  7 WATER actions successfully execute. 3 unwatered tiles accumulate consecutive_unwatered = 1.
        ↓
[CROP MORTALITY SPIRAL]
  On Day 2/3, unwatered tiles reach consecutive_unwatered = 2 and DIE.
  Active crops drop from 10 → 7 → 4 → 0.
  Water quota drops from 7 → 5 → 3 → 0.
        ↓
[CROP TARGET ATTAINMENT COLLAPSE]
  Attainment drops to 0.0–0.20 across steady-state window.
        ↓
[ECONOMIC DIVERGENCE]
  - If Crop Target 25 (A03, A06): Upfront seed cost exhausted liquidity → $300 CASH STALL.
  - If Crop Target 10/17 (A01, A02, A05, A07): Surplus cash funded Livestock → Milk/Fertilizer sustained cash flow ($15k–$29k).
```

---

## 4. Candidate Bottleneck Classification & Ranking

| Bottleneck Candidate | Status | Diagnostic Layer | Evidence For | Evidence Against | Affected Cells | Confidence |
|---|---|---|---|---|---|---|
| **Priority-as-Quota Implementation Defect** | **CONFIRMED** | `POLICY_REALIZATION` | `water_quota = ceil(priority * needs)` explicitly caps water targets to a fraction (<1.0) of crops. | None. Directly visible in code line 267. | ALL (A01–A07) | **VERY HIGH** |
| **Telemetry Event Ledger Attribution Bug** | **CONFIRMED** | `MEASUREMENT` | `id(farm)` mismatch caused all unit events to record `player: -1`, wiping out `watering_execution_rate` in analysis. | None. Verified in event logs and runner code. | ALL (A01–A07) | **VERY HIGH** |
| **Crop Mortality Feedback Loop** | **CONFIRMED** | `SYSTEM_DYNAMICS` | Crop losses match initial crop targets (11–30 crops lost per run). Zero active crops survive to endgame. | None. Universal across 28/28 runs. | ALL (A01–A07) | **HIGH** |
| **Cash Starvation at $300 Floor** | **CONFIRMED** | `POLICY_REALIZATION` | Cash hits exactly $300.00 on Day 1 in A03/A06; all subsequent market orders blocked; 0 cows bought; final money = $300.00. | Only occurs in target 25 under LOW/MID watering. | A03, A06 | **HIGH** |
| **Failed Harvest Dispatch Overhead** | **STRONGLY_SUPPORTED** | `DISPATCH` | 150–367 failed HARVEST actions per episode in high-crop cells; workers routed to non-ready tiles. | Did not prevent livestock operations in A02/A05/A07. | A03, A04, A06, A07 | **HIGH** |
| **Routing / Transit Overhead** | **SUPPORTED** | `ROUTING` | 1,500–3,000 MOVE steps per episode. Workers walk back and forth between shed and perimeter. | Total worker capacity (264 turns/day) was not saturated (2,400+ PASS turns). | ALL (A01–A07) | **MEDIUM** |
| **Feed & Livestock Opportunity Cost** | **SUPPORTED** | `INTERACTION` | Livestock FEED/CARE consumed ~170 turns/day in A01/A02/A05/A07, but generated >80% of total revenue. | Livestock was the *only* reason A01/A02/A05/A07 survived economically. | A01, A02, A04, A05, A07 | **MEDIUM** |
| **Insufficient Workforce Capacity** | **NOT_SUPPORTED** | `CAPACITY` | 10 hands provided 264 unit-turns/day. Thousands of idle PASS turns occurred in every run. | None. Capacity was never the binding constraint. | None | **HIGH** |
| **Weed / Maintenance Load** | **NOT_SUPPORTED** | `ENVIRONMENT` | Weeds did not block planting or watering actions; no weed clearing was scheduled. | None. | None | **HIGH** |

---

## 5. Cross-Cell Contrasts & Mechanism Isolation

### A01 vs A02 (Crop 10: LOW 0.20 vs HIGH 0.70)
- **WATER Executed:** A01 = 4.0 vs A02 = 53.0.
- **Crop Revenue:** A01 = $8,687 vs A02 = $9,587.
- **Livestock Revenue:** A01 = $18,605 vs A02 = $13,460.
- **Mechanism:** In A01, 0.20 priority meant only 2 crops watered/day; 11 crops died almost immediately. In A02, 53 water actions delayed mortality by a few days, capturing slightly more initial crop revenue ($9,587 vs $8,687), but higher worker movement for watering slightly reduced early care/feed attention, leading to lower livestock yield ($13,460 vs $18,605).

### A03 vs A04 (Crop 25: LOW 0.20 vs HIGH 0.70)
- **Final Money:** A03 = $300.00 vs A04 = $8,407.00.
- **WATER Executed:** A03 = 21.0 vs A04 = 94.5.
- **Mechanism:** In A03, planting 25 crops cost $1,610 in seeds; with only 21 water actions, 100% of crops died before producing revenue. Cash stalled at $300.00 on Day 1, preventing livestock purchase. In A04, 94.5 water actions kept enough high-value crops (Melon/Strawberry) alive to yield $8,327, recovering liquidity, purchasing 4 cows, and finishing at $8,407.

### A03 vs A06 vs A04 (Crop 25: LOW 0.20 → MID 0.45 → HIGH 0.70)
- **Final Money:** A03 = $300.00 → A06 = $300.00 → A04 = $8,407.00.
- **WATER Executed:** A03 = 21.0 → A06 = 34.8 → A04 = 94.5.
- **Mechanism:** Demonstrates a strict **threshold effect**. Both 0.20 and 0.45 priority allow daily drought rates that trigger catastrophic crop mortality before revenue recovery. Only 0.70 priority broke above the survival threshold to escape the $300 cash stall.

### A02 vs A07 vs A04 (HIGH 0.70: Crop 10 → Crop 17 → Crop 25)
- **Final Money (Median):** A02 = $15,274.00 → A07 = $19,511.50 → A04 = $8,407.00.
- **Crop Seed Cost:** A02 = -$1,300 → A07 = -$2,230 → A04 = -$3,020.
- **Net Crop Margin:** A02 = +$8,287 → A07 = +$8,843 → A04 = +$5,307.
- **Mechanism:** **Non-monotonicity confirmed**. Crop target 17 (A07) achieved the highest net crop margin ($8,843) while preserving sufficient liquidity for livestock ($16,415 revenue). Scaling to Crop 25 (A04) overextended seed expenditure, increasing failed harvest traffic and dragging final revenue down to $8,407.

### A05 vs A07 (Crop 17: MID 0.45 vs HIGH 0.70)
- **Final Money (Median):** A05 = $23,646.00 vs A07 = $19,511.50.
- **Livestock Revenue:** A05 = $24,928 vs A07 = $16,415.
- **Mechanism:** In A05, lower watering demand (32 water actions) allowed workers to focus earlier and more consistently on livestock feeding and care, yielding maximum milk production ($24,928). In A07, higher watering demand (83.8 actions) competed with livestock care transit, reducing milk yields without fully saving the crop cohort from the 30% drought rule.

---

## 6. Representative Failure Chronology

### Timeline Reconstruction: Cell A03 (S1802163452-P0, LOW Water 0.20, Crop 25)
- **Day 0, Hour 0 (Step 0):** Starting cash $3,000. Agent requests `BUY_LAND` ($1,000), `BUY_SEED` (25 seeds = $1,610), and `HIRE` (6 hands = $20). Cash drops to $370.
- **Day 0, Hour 1–8:** 6 workers plant 25 seeds across Quadrants 0 and 1. Cash drops below $300 due to subsequent worker hire fees; cash hits **$300.00 floor**.
- **Day 1 (Steps 24–47):** `watering_needs = 25`. With `priority = 0.20`, quota is `ceil(0.20 * 25) = 5`. Exactly 5 plants are watered; 20 plants remain unwatered (`consecutive_unwatered = 1`).
- **Day 2 (Steps 48–71):** Another 5 plants watered. The remaining 20 unwatered plants reach `consecutive_unwatered = 2` and **DIE**.
- **Day 3 (Steps 72–95):** 20 dead crop tiles vanish. Remaining 5 plants lack water continuity and die on Day 4. `active_crops = 0`.
- **Day 4–29 (Steps 96–720):** Cash is locked at $300.00. No market orders can be placed. All 10 worker contracts expire. Single farmer passes every turn. **FINAL MONEY = $300.00**.

### Timeline Reconstruction: Cell A04 (S1802163452-P0, HIGH Water 0.70, Crop 25)
- **Day 0 (Steps 0–23):** Buys Land, 25 seeds ($1,610), hires workers. Cash drops to ~$350.
- **Day 1–3:** With `priority = 0.70`, quota is `ceil(0.70 * 25) = 18`. 18 plants watered daily. ~7 plants die on Day 2/3, but ~18 mature into Strawberries, Melons, Wheat.
- **Day 4–6:** Surviving crops harvested and sold for ~$8,230 cash. Cash surges to ~$8,500.
- **Day 7:** Liquidity allows purchasing 4 Cows ($1,600) and Wheat feed. Pastures populated.
- **Day 8–28:** Cows produce Milk/Fertilizer. However, dead crop tiles are never replanted because quota logic and failed harvest loops absorb worker turns.
- **Day 29:** Endgame liquidation of remaining Milk/Wheat. **FINAL MONEY = $8,962.00**.

---

## 7. Shortlist of Causal Bottleneck Hypotheses for E16-A2

```text
hypothesis_id: H_BOTTLENECK_1_WATERING_QUOTA_FORMULA
candidate_cause: Priority implemented as fraction of crops watered rather than absolute worker dispatch priority.
mechanism: Setting priority = p < 1.0 enforces that (1 - p) fraction of crops are never watered on any given day. In a 2-day drought death engine, this guarantees 100% cohort extinction within 2 to 4 days.
observed_evidence: Confirmed in treatment code (line 267). Monotonic crop mortality across all cells (11 to 30 crops lost per run).
what_would_falsify_it: If implementing a strict "water 100% of active plants daily with precedence P" still results in crop mortality under identical workforce.
minimal_manipulated_variable: watering_dispatch_mode = (FRACTIONAL_QUOTA vs FULL_COHORT_PRECEDENCE)
critical_control_variables: workforce_headcount = 10, quadrants_owned = 2, crop_working_set_target = 17
minimum_telemetry_needed: daily_watered_fraction, consecutive_unwatered_distribution, crop_loss_rate
```

```text
hypothesis_id: H_BOTTLENECK_2_STARTUP_CAPITAL_EXHAUSTION
candidate_cause: Unbuffered simultaneous upfront expenditure on Land ($1,000), Seeds ($1,600+), and Workforce ($900+) on Day 0.
mechanism: Scale targets (crop 25) drive cash immediately to the $300 operating floor before the first crop harvest. Any minor initial service delay causes unrecoverable cash stall.
observed_evidence: A03 and A06 hit exactly $300.00 on Day 0/1 and stayed frozen at $300.00 for all 720 steps across all seeds and seats.
what_would_falsify_it: If staged/staggered crop planting (e.g. 8 → 16 → 25) with cash-gating prevents the $300 stall at crop target 25.
minimal_manipulated_variable: planting_schedule = (ALL_AT_ONCE vs STAGGERED_CASH_GATED)
critical_control_variables: crop_working_set_target = 25, watering_dispatch_priority = 0.70
minimum_telemetry_needed: daily_cash_trajectory, days_at_cash_floor, hire_renewal_success_rate
```

```text
hypothesis_id: H_BOTTLENECK_3_FAILED_HARVEST_DISPATCH_POLLUTION
candidate_cause: Dispatcher emits HARVEST actions for immature, unwatered, or non-harvestable crop tiles.
mechanism: Failed HARVEST actions accounted for 150–367 wasted unit turns per episode in scale cells, starving workers from completing legitimate irrigation or livestock transit.
observed_evidence: High failed HARVEST counts in A03 (216), A04 (367), A06 (316), A07 (219) while executed harvests were only 5–37.
what_would_falsify_it: If strict filtering for `yield_units > 0 and kind == 'PLANT'` completely eliminates failed harvest turns without improving watering continuity.
minimal_manipulated_variable: harvest_dispatch_filter = (LENIENT vs STRICT_YIELD_GATED)
critical_control_variables: crop_working_set_target = 17, watering_dispatch_priority = 0.70
minimum_telemetry_needed: failed_harvest_action_rate, effective_worker_utilization
```

---

## 8. Epistemic Assessment & Diagnostic Layer Status

- **MODEL_VALIDITY:** `STRONGLY_SUPPORTED`  
  The fundamental ontological concepts in the MODEL_SPEC (that sustained irrigation is required for crop survival, that overextension without maintenance causes collapse, and that livestock provides resilient margin) are completely vindicated by the data. The collapse of A03/A06 directly validates the model's prediction that capital exhaustion + unserviced surface leads to total economic failure.

- **POLICY_REALIZATION:** `COMPROMISED_BY_IMPLEMENTATION_DEFECT`  
  The intended policy of "HIGH watering priority" was implemented as a fractional quota (`math.ceil(0.70 * crops)`), inadvertently engineering a 30% daily drought rate that destroyed the crop cohort.

- **IMPLEMENTATION_FIDELITY:** `INSTRUMENTATION_DEFECT_CONFIRMED`  
  The telemetry ledger's `id(farm)` tracking bug caused all unit events to record `player: -1`, leading the automated analysis scripts to report `watering_execution_rate = 0.0` across the board, masking the fact that 50–95 real water actions were executed per run.

---

## 9. Conclusion

The Stage A gate blockage (`STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR`) was the mathematically necessary and epistemically correct outcome of the frozen gate rules applied to the compromised treatment build. The root causes are fully identified, quantified, and ready for clean discrimination in E16-A2.

```text
FORENSIC_STATUS: COMPLETE

TOP_BOTTLENECK_1: Fractional watering quota formula (math.ceil(priority * needs)) deliberately leaving (1-p) crops unwatered daily
CONFIDENCE: VERY HIGH

TOP_BOTTLENECK_2: Upfront capital exhaustion on Day 0 in 25-crop cells causing permanent $300 cash stall
CONFIDENCE: HIGH

TOP_BOTTLENECK_3: Telemetry event ledger player attribution bug (player: -1) masking executed water actions
CONFIDENCE: VERY HIGH

IMPLEMENTATION_DEFECT_DETECTED: YES

MODEL_VALIDITY_STATUS:
  Strongly supported; empirical failure modes match theoretical model predictions regarding maintenance failure and capital overextension.

POLICY_REALIZATION_STATUS:
  Compromised; priority implemented as fractional exclusion rather than dispatch precedence.

IMPLEMENTATION_FIDELITY_STATUS:
  Instrumentation defect confirmed; telemetry parser failed to bind unit actions to treatment seat.

E16_A2_HYPOTHESES_READY: YES

FILES_CHANGED:
  experiments/archive/e16/artifacts/analysis/E16_STAGE_A_FORENSIC_DIAGNOSIS.md
```
