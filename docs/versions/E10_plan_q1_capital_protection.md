# PLAN Report — E10-01 Q1 Expansion Capital Protection

**Date:** 2026-08-26  
**Phase:** E10-02 PLAN  
**Status:** `PLANNED — READY FOR BUILD`  
**Primary Baseline:** E09-01 (`LivestockAblationROIAgent`, 40 tiles, Livestock OFF)  
**Strategy Class:** `Q1CapitalProtectedROIAgent` ([`src/agricola/strategy/q1_capital_protected_roi.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/q1_capital_protected_roi.py))  

---

## 1. Plan Overview & Architecture

E10-01 introduces a controlled, single-variable delta over E09-01: **Q1 Expansion Capital Protection**.

The architectural design protects liquid capital required for the Day 12 `BUY_LAND` Q1 expansion ($1,000.0) without altering any crop allocation, movement, spatial partitioning, hiring, or scheduling logic.

```text
E09-01 (Baseline)
 ├── 40 tiles (20 Q0 + 20 Q1)
 ├── Livestock OFF
 ├── 4 workers (Day 1, 6, 12)
 ├── Water-First (WATER > HARVEST > PLANT)
 └── Market Seed Reserve: Static $300.0 floor
        │
        │ Single Variable Change: Capital Protection Rule
        ▼
E10-01 (Treatment)
 ├── 40 tiles (20 Q0 + 20 Q1) [INVARIANT]
 ├── Livestock OFF [INVARIANT]
 ├── 4 workers (Day 1, 6, 12) [INVARIANT]
 ├── Water-First (WATER > HARVEST > PLANT) [INVARIANT]
 └── Market Seed Reserve: Dynamic Capital Floor
      ├── Pre-Expansion (Days 8-11, Q1 unowned): Floor = max($300, $1000)
      ├── Land Purchase (Day >= 12, Q1 unowned): Execute BUY_LAND if cash >= $1000
      └── Post-Expansion (Q1 owned): Floor = $300 (released)
```

---

## 2. Implementation Specifications

### 2.1 Strategy File & Class Name
- **File:** `src/agricola/strategy/q1_capital_protected_roi.py`
- **Class Name:** `Q1CapitalProtectedROIAgent`

### 2.2 Exact Delta (E09 -> E10)

```python
# --- Seed Purchasing with Capital Protection ---
def _buy_seeds_if_needed(self, state: GameState, builder: ActionBuilder, cash: float, reserve: float):
    day = state.day
    if day > self.config.all_plant_cutoff_day:
        return
        
    # Determine effective cash reserve floor
    effective_reserve = reserve
    if self.owned_quadrants < 2 and day >= 8:
        effective_reserve = max(reserve, 1000.0)

    if state.get_seed_count("WHEAT") < 4 and cash - 10.0 >= effective_reserve:
        builder.buy_seed("WHEAT", 6)
        self.telemetry.spending_seeds += 60.0
        self.telemetry.wheat_bought += 6
        cash -= 60.0
        
    if state.get_seed_count("CARROT") < 4 and cash - 20.0 >= effective_reserve:
        builder.buy_seed("CARROT", 6)
        self.telemetry.spending_seeds += 120.0
        cash -= 120.0

    if day <= self.config.melon_plant_cutoff_day and state.get_seed_count("MELON") < 4 and cash - 80.0 >= effective_reserve:
        builder.buy_seed("MELON", 4)
        self.telemetry.spending_seeds += 320.0
        cash -= 320.0

# --- Land Expansion Execution ---
if day >= self.config.expansion_day and self.owned_quadrants < self.config.target_quadrants:
    land_cost = 1000.0
    if cash >= land_cost:
        builder.buy_land()
        self.owned_quadrants = 2
        ...
```

---

## 3. Telemetry & Diagnostic Instrumentation

In addition to standard E09 telemetry, `Q1CapitalProtectedROIAgent` will record:
- `cash_at_day_12_h0`: Liquid cash balance at Day 12, Hour 0.
- `q1_purchased_on_time`: Boolean flag indicating if `BUY_LAND` Q1 was executed on Day 12 (or Day 13).
- `q1_land_buy_day`: Exact day when Q1 land expansion was executed.

---

## 4. Testing & Verification Plan

### 4.1 Unit & Functional Tests (`tests/test_e10_q1_capital_protection.py`)
1. **Test Seed Protection Floor:** Verify seed buying is blocked on Day 10 when cash is $1,100 ($1,100 - $320 < $1,000 floor).
2. **Test Timely BUY_LAND:** Verify `BUY_LAND` executes on Day 12 when cash is $1,050.
3. **Test Post-Expansion Release:** Verify seed buying uses standard $300 floor after `owned_quadrants == 2`.
4. **Test Full Invariants:** Confirm 4 workers, 40-tile footprint, Water-First priority, and Livestock OFF.

### 4.2 Full Regression Suite
Execute `pytest tests/` to confirm 100% test pass across all workspace tests.

### 4.3 Single Episode Technical Smoke Test
Execute a single 720-step episode in `kaggle_environments` engine to verify no disqualifications or runtime crashes.

### 4.4 Local Safety Verification Benchmark (30 Paired Episodes)
Run a 30-episode paired benchmark (10 x `pass`, 10 x `random`, 10 x `starter`) using identical seeds (0, 100, ..., 900) comparing:
- E09-01 baseline
- E10-01 treatment
- E06 secondary reference

---

## 5. Entrypoint, Freeze & Packaging Plan

1. Update `src/agricola/agent.py` to instantiate `Q1CapitalProtectedROIAgent`.
2. Update `scripts/build_submission.py` to bundle `Q1CapitalProtectedROIAgent` into `submission/submission.py`.
3. Run `pytest tests/test_submission.py` to verify standalone submission package execution.
4. Freeze E10 implementation.

---

## 6. Morning Kaggle Verdict Criteria

- **SUCCESS:** E10 stabilizes higher Kaggle score than E09 (347.0), eliminates severe drop episodes on Kaggle, increases Q1 tile utilization, and preserves top performance.
- **PARTIAL SUCCESS:** E10 improves land acquisition timing and local robustness, but competitive rating remains below E06 due to downstream worker movement/scheduling bottlenecks in Q1.
- **FAILURE:** E10 fails to improve Q1 expansion timing or performance remains identical to E09.

---

<!-- END OF FILE -->
