# VERIFY Final Reward & Asset Liquidation — E07 (`E07-04`)

**Date:** 2026-08-26  
**Phase:** VERIFY (Environment Grounding & Terminal Mechanics)  
**Status:** `VERIFY PASSED WITH END-GAME CORRECTIONS`  
**Decision:** `GO FOR BUILD WITH END-GAME CORRECTIONS`  

---

## 1. Executive Summary & Verification Objective

This document performs a direct, empirical verification of the final reward calculation, asset valuation rules, and liquidation mechanics of the Kaggriculture environment by auditing `kaggle_environments.envs.kaggriculture.kaggriculture` and running targeted environment test scripts.

### Key Finding & Verdict
1. **Final Reward Formula:** The Kaggle final reward assigned at step 720 is **STRICTLY equal to liquid bank cash**:
   $$\text{Final Reward} = \text{float}(\text{farm}["\text{money}"])$$
2. **Zero Automatic Valuation:** Crops on field (mature or growing), shed inventory (crops, animal products, seeds), livestock (Cows, Sheep, Geese), land (`BUY_LAND` quadrants), and structures (`PASTURE`, `COOP`) **DO NOT produce ANY automatic terminal reward value**.
3. **No Animal Resale / `SELL_ANIMAL`:** There is **NO `SELL_ANIMAL` action or livestock resale/refund mechanism** in Kaggriculture. Capital invested in animals, land, and structures is 100% illiquid and un-recoverable except through products harvested and sold prior to step 720.
4. **Decision:** **`GO FOR BUILD WITH END-GAME CORRECTIONS`**.

---

## 2. Environment Source Code Audit (`kaggriculture.py`)

We inspected `kaggle_environments.envs.kaggriculture.kaggriculture` to verify exact code implementation:

### A. Final Reward Assignment
- **File / Location:** `kaggriculture.py` $\rightarrow$ `interpreter` function (lines 960–964).
- **Exact Code Snippet:**
  ```python
  if step >= cfg.episodeSteps - 2:
      for s in state:
          s.status = "DONE"
          s.reward = float(obs0.farms[s.observation.player]["money"])
  ```
- **Verified Behavior:** Upon episode completion, the agent reward is set exclusively to the float value of `farm["money"]`. No asset valuation or inventory liquidation functions are called.

### B. Market Order Processing & Unit Operations
- **File / Location:** `kaggriculture.py` $\rightarrow$ `_commit_unit` function.
- **Supported Operations:**
  - `SELL`: Sells 1 unit from `private["shed"]` for market price, adding cash to `farm["money"]`. Valid only for items in `PRODUCTS` (`WHEAT`, `CARROT`, `TOMATO`, `STRAWBERRY`, `MELON`, `EGG`, `MILK`, `WOOL`, `FERTILIZER`).
  - `BUY_PRODUCT`: Buys product from market to shed.
  - `BUY_SEED`: Buys seed to `private["seeds"]`.
  - `BUY_ANIMAL`: Buys animal (`COW`, `SHEEP`, `GOOSE`) to shed.
- **Non-Existent Operations:**
  - `SELL_ANIMAL`: **DOES NOT EXIST**.
  - `SELL_LAND`: **DOES NOT EXIST**.
  - `SELL_STRUCTURE`: **DOES NOT EXIST**.

---

## 3. Real Action Space Inventory

The exact, authoritative action space supported by `kaggriculture.py` consists of:

### Unit Actions (Farmer / Farm Hands)
- **Movement:** `NORTH` (`N`), `SOUTH` (`S`), `EAST` (`E`), `WEST` (`W`)
- **Turn Idle:** `PASS`
- **Crop Operations:** `PLANT <CROP>`, `WATER`, `HARVEST`, `DIG`, `FERTILIZE`
- **Storage / Item:** `PICKUP`, `DROP`, `PLACE`
- **Structure Operations:** `BUILD_COOP`, `BUILD_PASTURE`
- **Livestock Operations:** `FEED`, `CARE`, `COLLECT_FERTILIZER`

### Market Orders (`market` list)
- `HIRE`
- `BUY_LAND`
- `BUY_SEED <CROP>`
- `BUY_ANIMAL <ANIMAL>`
- `BUY_PRODUCT <PRODUCT>`
- `SELL <PRODUCT>` (Products: Wheat, Carrot, Tomato, Strawberry, Melon, Egg, Milk, Wool, Fertilizer)

---

## 4. Terminal Value Audit Table

| Asset | Contributes automatically to final reward? | Can be liquidated? | Mechanism | Terminal Risk |
| :--- | :---: | :---: | :--- | :--- |
| **Cash (`farm["money"]`)** | **`YES`** | **`YES`** | Direct 1:1 reward | None (100% liquid) |
| **Crop Inventory (Shed)** | **`NO`** | **`YES`** | Market order `["SELL", product, qty]` | High if unsold at step 720 ($0 reward value) |
| **Mature Crops on Field** | **`NO`** | **`CONDITIONAL`** | Must be harvested $\rightarrow$ shed $\rightarrow$ `SELL` order | High if unharvested before step 720 |
| **Immature Crops** | **`NO`** | **`NO`** | None (cannot mature in time) | 100% loss of seed cost & labor if planted late |
| **Cows ($400)** | **`NO`** | **`NO`** | Daily Milk sales ($160/2d) over lifetime | 100% capital lockup. Must amortize before D30 |
| **Sheep ($500)** | **`NO`** | **`NO`** | Daily Wool sales ($200/3d) over lifetime | 100% capital lockup. Must amortize before D30 |
| **Land (`BUY_LAND` Q1)** | **`NO`** | **`NO`** | Production capacity expansion | 100% capital lockup ($1,000). Must pay off before D30 |
| **Structures (`PASTURE`)** | **`NO`** | **`NO`** | Enables animal placement | 100% labor/space lockup |

---

## 5. Experimental Test Results (`scratch/verify_reward.py`)

We executed empirical test scripts using `kaggle_environments.make("kaggriculture")`:

- **Test A (Cash):** Episode completed with $3,000 cash. Output: `P0 Final Money: $3000.0`, `P0 Final Reward: 3000.0`. Result: **`Reward == Money (100% Verified)`**.
- **Test B (Inventory):** Episode ended holding 10 Wheat seeds ($100 spent, $2,900 cash). Output: `End Money: $2900.0`, `End Reward: 2900.0`. Result: **`Unsold seeds/items do NOT add to reward ($0 terminal value)`**.
- **Test C (Livestock):** Episode ended holding 1 Cow ($400 spent, $2,600 cash). Output: `End Money: $2600.0`, `End Reward: 2600.0`. Result: **`Owned animals do NOT add to reward ($0 terminal value)`**.
- **Test D (Field Asset):** Episode ended with mature Wheat crop on field. Output: `End Reward == Money`. Result: **`Unharvested crops do NOT add to reward ($0 terminal value)`**.

---

## 6. Re-evaluation of E07 End-Game Policy & Claim Audit

| DEFINE / PLAN Claim | Evaluation | Classification | Correction Required |
| :--- | :--- | :---: | :--- |
| **"Total inventory sell-off (Days 29–30)"** | Shed items must be sold via market `SELL` to convert to reward. | **`VALID`** | Retain 100% shed flush on Days 27–30. |
| **"Total animal sell-off (Days 29–30)"** | Animals CANNOT be sold (`SELL_ANIMAL` does not exist). | **`INVALID`** | **REMOVE animal sell-off completely from E07 Plan**. |
| **"Day 29–30 asset liquidation"** | Valid for crop/shed products; invalid for livestock/land/structures. | **`PARTIALLY VALID`** | Restrict liquidation term to shed inventory sales. |

---

## 7. Distinguishing Production vs Scoring Metrics

To eliminate design ambiguity, we explicitly distinguish:

- **Final Money (`farm["money"]`):** Liquid cash on hand at step 720. **`COINCIDES 100% WITH KAGGLE REWARD`**.
- **Kaggle Reward:** `float(farm["money"])`. **`COINCIDES 100% WITH FINAL MONEY`**.
- **Farm Productive Capacity:** Total earning potential of installed crops/herd. **`DOES NOT COINCIDE WITH REWARD`**.
- **Residual Asset Value:** Theoretical book value of land, animals, structures, and unsold crops. **`DOES NOT COINCIDE WITH REWARD (WORTH $0 AT STEP 720)`**.

---

## 8. Revised End-Game Policy & Operational Cutoffs for E07

Based on illiquid capital lockup mechanics, we establish strict **Economic Amortization Cutoffs**:

### 1. Livestock Purchase Hard Cutoff
- **Cow Amortization:** $400 purchase price / ($160 Milk / 2 days = $80/day) = **5 days (120 steps)** to break even.
- **Sheep Amortization:** $500 purchase price / ($200 Wool / 3 days = $66.7/day) = **7.5 days (180 steps)** to break even.
- **Rule:** **No Cow purchases after Day 20**; **No Sheep purchases after Day 18**. Any animal bought after these days is guaranteed capital loss.

### 2. Crop Planting Hard Cutoffs
- **Melon (12-day growth):** **Last planting day = Day 18**. Any Melon planted after Day 18 will not mature before Day 30 and represents 100% wasted seed/labor capital.
- **Carrot (3-day growth):** **Last planting day = Day 26**.
- **Wheat (2-day growth):** **Last planting day = Day 27** (or Day 26 for feed).

### 3. Land Expansion (`BUY_LAND` Q1) Hard Cutoff
- **Rule:** Execute `BUY_LAND` Q1 ($1,000) on or before **Day 12**. Buying land after Day 15 will not provide enough remaining crop cycles to pay off the $1,000 purchase price.

### 4. Market Shed Flush Schedule
- **Days 1–26:** Sell Milk/Wool daily; sell Melons upon harvest; sell Carrots for liquidity.
- **Days 27–30 (Turns 648–720):** Execute continuous 100% shed flush. Sell all Milk, Wool, Melons, Carrots, and excess Wheat to ensure zero items remain in shed at step 720.

---

## 9. PLAN Corrections Applied

We updated [`docs/plans/E07_Competitive_Baseline_Reconstruction.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E07_Competitive_Baseline_Reconstruction.md) and [`docs/versions/E07_plan_competitive_baseline.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E07_plan_competitive_baseline.md) to:
1. Remove all references to animal sell-off or `SELL_ANIMAL`.
2. Add Cow purchase cutoff (Day 20) and Sheep purchase cutoff (Day 18).
3. Adjust Melon last planting day to **Day 18** (instead of Day 25) to guarantee 12-day maturity before Day 30.
4. Set shed inventory flush window to **Days 27–30**.

---

## 10. Decision

> **`GO FOR BUILD WITH END-GAME CORRECTIONS`**

The terminal reward mechanics are 100% verified and grounded in official environment code. The E07 architecture is valid, and the corrected end-game cutoffs ensure zero capital waste on illiquid late-game assets.
