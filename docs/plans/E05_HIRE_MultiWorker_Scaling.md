# Implementation Plan — E05 HIRE / Multi-Worker Scaling (`HIRENWClusterROIAgent`)

Define the technical implementation plan for **E05 (`HIRENWClusterROIAgent`)** to evaluate whether introducing 1 daily farm hand via `HIRE` ($1/day) with fixed spatial partitioning (4:5) eliminates the worker capacity/scheduling bottleneck of E04 and renders the 9-tile NW footprint economically sustainable.

---

## 1. Objective

Test the hypothesis that adding worker capacity via a single daily `HIRE` enables the 9-tile NW production footprint to scale economically without suffering from the severe water starvation (238 weed conversions) observed in E04.

---

## 2. Experimental Question

> **L'aggiunta giornaliera di una farm hand tramite `HIRE` fornisce capacità lavorativa sufficiente a rendere economicamente sostenibile il footprint E04 da 9 tile?**

---

## 3. Hypothesis

> **Se** introduciamo un lavoratore subordinato giornaliero tramite l'azione `HIRE` (costo $1/giorno) e partizioniamo lo spazio di lavoro 4:5 tra Farmer principale e Farm Hand 1, mantenendo invariata la policy economica E03/E04, **allora** il Mean Final Money nel benchmark locale aumenterà significativamente rispetto a E04 (`$11232.47`) verso o oltre il livello E03 (`$14682.47`), **perché** la seconda unità lavorativa elimina il collo di bottiglia temporale d'irrigazione, azzerando le morti per disidratazione e ripristinando la piena produttività agricola sulle 9 tile.

---

## 4. Control and Treatment

### Control — E04 (`NWClusterROIAgent`)
- 1 farmer principal.
- 9-tile NW footprint: `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`.
- Operational policy derived from E03 (`HARVEST > PLANT > WATER`).
- No `HIRE`, no `BUY_LAND`, no `DIG`.
- Mean Final Money baseline: **`$11232.47 ± $661.26`** (238 weed conversions).

### Treatment — E05 (`HIRENWClusterROIAgent`)
- 1 farmer principal + 1 farm hand hired daily ($1/day).
- Same 9-tile NW footprint.
- Same E03 ROI crop selection logic (`yield=2.0`).
- Same operational priority hierarchy (`HARVEST > PLANT > WATER`).
- Fixed spatial partitioning 4:5 between Farmer and Hand 1.

---

## 5. Primary Experimental Variable

> **Capacità lavorativa aggiuntiva introdotta tramite un singolo `HIRE` giornaliero ($1/giorno).**

Strictly **one treatment**: 1 daily farm hand. No testing of multiple hands, no dynamic rebalancing, no additional heuristics.

---

## 6. Variables Held Constant

To preserve strict experimental isolation, the following parameters remain **identical to E04**:

- Managed footprint: 9 tiles `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` in starting NW quadrant;
- ROI crop selection formula E03 (`yield = 2.0`);
- Task priority hierarchy (`HARVEST > PLANT > WATER`);
- Immediate liquidation/selling of products in shed;
- Absence of terminal horizon logic;
- No `BUY_LAND`;
- No `DIG` (no weed recovery);
- No Water-First scheduling;
- Same 30-episode benchmark protocol against `pass`, `random`, `starter`.

---

## 7. Verified HIRE Constraints

Derived from E05-01 environment code audit (`kaggriculture.py`):
1. `HIRE` action issued in market: `action["market"] = [["HIRE"]]`.
2. First hire of the day costs **$1** (`fib(0)=1`), charged immediately from shared farm money.
3. Order issued at step $S$ creates Hand 1 at step $S$ market phase; Hand 1 is active and receives actions at step $S+1$.
4. Hand 1 vanishes at end of day (`hour == 23` refresh), inventories deposited to shed, `hands` list reset to `[]`, `hires_today` reset to 0.
5. Hand 1 must be re-hired **every day at `hour == 0`** (total expected cost: **$30 / episode**).
6. Aggregate `PLANT` orders exceeding owned seeds are cancelled atomically (`PASS`).

---

## 8. Fixed Worker Coordination (4:5 Spatial Partitioning)

To prevent worker collision and task contention, the 9-tile cluster is partitioned deterministically:

### Farmer Principal (4 tiles):
`{(4,4), (4,3), (3,4), (3,3)}`

### Farm Hand 1 (5 tiles):
`{(4,2), (3,2), (2,4), (2,3), (2,2)}`

> *Methodological Note: This 4:5 spatial partitioning is a fixed coordination mechanism required to operationalize multi-worker execution. It is NOT a second experimental variable to optimize.*

---

## 9. Daily HIRE Lifecycle

```
┌──────────────────────────────────────────────────────────┐
│ Step S (hour == 0): New Day Starts                        │
│ - Check: len(hands) == 0 AND hires_today == 0            │
│ - Emit: action["market"] = [["HIRE"]] ($1 cost)          │
│ - Farmer executes task on 4-tile partition               │
└──────────────────────────┬───────────────────────────────┘
                           │ Market Phase processes HIRE
                           ▼
┌──────────────────────────────────────────────────────────┐
│ Step S+1 (hour == 1): Hand 1 Active                      │
│ - Hand 1 spawned at (4,4) (shed access tile)             │
│ - State exposes hand at hands_positions[0]               │
│ - Farmer executes task on 4-tile partition               │
│ - Hand 1 executes task on 5-tile partition               │
└──────────────────────────┬───────────────────────────────┘
                           │ Regular day execution (hours 1..22)
                           ▼
┌──────────────────────────────────────────────────────────┐
│ Step S+23 (hour == 23): End of Day                        │
│ - Final turn of the day                                  │
│ - Environment resets farm["hands"] = [] and hires=0      │
│ - Carried inventories auto-dropped to shed               │
└──────────────────────────────────────────────────────────┘
```

---

## 10. Worker Scheduling & Shared Resource Coordination

### Independent Worker Scheduling
- **Farmer:** Applies `HARVEST > PLANT > WATER` with Manhattan routing strictly on its assigned 4 tiles.
- **Hand 1:** Applies `HARVEST > PLANT > WATER` with Manhattan routing strictly on its assigned 5 tiles.

### Shared Resource Protection
- **Seeds & Atomic PLANT Protection:** Before issuing a `PLANT` action, check `state.get_seed_count(crop)`. Farmer evaluates and reserves seed demand first. Hand 1 only issues `PLANT` if remaining seed count exceeds Hand 1's plant demand.
- **Money & Selling:** HIRE cost ($1/day) is automatically deducted from shared farm money. Selling phase liquidates shed items into shared farm money.

---

## 11. Architectural Changes & File Map

### Files to Create (`[NEW]`):
1. **`src/agricola/strategy/hire_nw_cluster_roi.py`**: Implementation of `HIRENWClusterROIAgent`.
2. **`tests/test_hire_nw_cluster.py`**: Unit test suite for HIRE lifecycle, 4:5 partitioning, seed protection, and multi-worker action generation.
3. **`docs/plans/E05_HIRE_MultiWorker_Scaling.md`**: This plan document.

### Files to Modify (`[MODIFY]`):
1. **`src/agricola/core/state.py`**: Add `hands_positions` property returning list of `(x, y)` tuples for active farm hands.
2. **`src/agricola/core/actions.py`**: Add `hire()` method to `ActionBuilder` and `add_hand_action(action_list)`.
3. **`src/agricola/agent.py`**: Update entrypoint to instantiate `HIRENWClusterROIAgent`.
4. **`scripts/build_submission.py`**: Update standalone bundler template to bundle `HIRENWClusterROIAgent`.

---

## 12. Instrumentation & Comparative Metrics

### Primary Comparative Metric:
- **Mean Final Money E05 vs E04 ($11232.47 ± $661.26)**
- Absolute Delta: $\text{Mean}_{E05} - 11232.47$
- Percentage Delta: $\frac{\text{Mean}_{E05} - 11232.47}{11232.47} \times 100\%$

### Reference Benchmark Comparison:
- **Mean Final Money E05 vs E03 ($14682.47 ± $1164.33)**

### Agricultural Starvation Metrics:
- **Total Weed Conversions E05 vs E04 (238 weeds)**
- **Mean Unwatered End-of-Day Ratio (%)**

### HIRE Operational Diagnostics:
- Total `HIRE` actions executed (Target: 30 per episode)
- Total HIRE cost (Expected: $30/episode)
- Farmer actions count breakdown (`HARVEST`, `PLANT`, `WATER`, `MOVE`, `PASS`)
- Hand 1 actions count breakdown (`HARVEST`, `PLANT`, `WATER`, `MOVE`, `PASS`)

---

## 13. Success & Failure Criteria

### Minimum Economic Success:
$$\text{Mean Final Money}_{E05} > \text{Mean Final Money}_{E04} \quad (>\$11,232.47)$$
Demonstrates that adding 1 daily farm hand improves the inefficient 9-tile single-farmer setup.

### Strong Economic Success:
$$\text{Mean Final Money}_{E05} \ge \text{Mean Final Money}_{E03} \quad (\ge \$14,682.47)$$
Demonstrates that multi-worker 9-tile scaling matches or exceeds the 4-tile benchmark.

### Operational Success:
$$\text{Total Weed Conversions}_{E05} = 0 \quad (\text{vs 238 in E04})$$
Complete elimination of the severe water starvation failure mode.

### Experimental Failure:
$$\text{Mean Final Money}_{E05} \le \text{Mean Final Money}_{E04} \quad (\le \$11,232.47)$$
Falsifies the hypothesis that worker capacity was the primary bottleneck, or indicates that HIRE cost/coordination overhead outweighs productivity gains.

---

## 14. Implementation Sequence (BUILD Plan)

1. **Step 1: Core State & Action Support**
   - Update `state.py` to expose `hands_positions`.
   - Update `actions.py` to support `hire()` and `add_hand_action()`.
2. **Step 2: Core HIRE Unit Tests**
   - Create `tests/test_hire_nw_cluster.py` testing `HIRE` market action format, hand position parsing, and 4:5 partitioning rules.
3. **Step 3: Strategy Implementation (`HIRENWClusterROIAgent`)**
   - Create `src/agricola/strategy/hire_nw_cluster_roi.py`.
   - Implement daily HIRE trigger on `hour == 0`.
   - Implement independent 4:5 spatial scheduling for Farmer and Hand 1.
   - Implement shared seed protection logic.
4. **Step 4: Unit Test Verification**
   - Run pytest suite (`.venv/Scripts/python.exe -m pytest tests/`).
5. **Step 5: Agent Entrypoint & Standalone Bundling**
   - Update `src/agricola/agent.py` and `scripts/build_submission.py`.
   - Verify standalone submission execution (`test_submission.py`).
6. **Step 6: 30-Episode Benchmark Execution**
   - Run `scripts/run_eval.py` across 30 episodes against `pass`, `random`, `starter`.
7. **Step 7: Verification & Report Generation**
   - Produce `walkthrough.md` / `docs/versions/E05_verify_antigravity.md` with comparative results.

---

## 15. Risks & STOP Conditions

### Identified Risks:
1. **Accidental Duplicate Hiring:** Issuing `HIRE` multiple times per day would escalate costs ($1, $1, $2, $3...).  
   *Mitigative Guard:* Check `len(state.hands_positions) == 0` AND `state.my_farm.get("hires_today", 0) == 0` before issuing `HIRE`.
2. **Atomic PLANT Cancellation:** Both workers issuing `PLANT` for the same crop with only 1 seed in stock.  
   *Mitigative Guard:* Shared seed reservation check in strategy `act()` method.
3. **Hand Action Serialization Index Mismatch:** Sending hand action when `hands` is empty in environment observation.  
   *Mitigative Guard:* Only append to `actions.hands` if `len(state.hands_positions) > 0`.

### STOP Conditions:
- If `HIRE` action fails to create a hand unit in environment execution;
- If standalone submission fails to execute cleanly;
- If unit tests fail regression.

---

## 16. Readiness Decision

> **`READY FOR BUILD`**

The experimental design is strictly isolated to 1 single variable (1 daily HIRE + fixed 4:5 partitioning), preserves all E04 control parameters, and provides clear quantitative metrics for empirical evaluation.
