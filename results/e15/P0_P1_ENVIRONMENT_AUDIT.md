# E15.0 Player Position Bias Audit (P0 vs P1 Environment Inspection)

- **Audit Date**: 2026-08-29
- **Environment**: Kaggle Environments `kaggriculture` (`kaggle_environments/envs/kaggriculture/kaggriculture.py`)
- **Auditor**: Antigravity (Independent Technical Audit)
- **Verdict**: `NO_MATERIAL_POSITION_BIAS_FOUND`

---

## 1. Executive Summary

A comprehensive source-level audit of `kaggle_environments/envs/kaggriculture/kaggriculture.py` was conducted to evaluate whether playing as Player 0 (P0) vs Player 1 (P1) introduces structural asymmetries, first-mover advantages, or position-dependent penalties.

The inspection concludes: **`NO_MATERIAL_POSITION_BIAS_FOUND`**.
Both players operate on completely disjoint farm grids with independent starting capital, identical spawn locations, and a per-unit lockstep market clearance engine that prevents front-running on dynamic price updates.

---

## 2. Detailed Technical Audit Findings

### 2.1 Initialization & Farm State Symmetry (`_initialize`, lines 244–276)
- **Starting Money**: Identical (`$3,000` for both agents, line 252).
- **Board & Quadrants**: Both farms initialize on separate 10x10 grids (`_new_farm`, lines 142–154) with NW unlocked (`["NW"]`) and identical starting coordinates (`farmer=(4,4)`, line 150/162).
- **Private Inventory & Seeds**: Both players initialize with identical empty sheds and zero seeds (`_new_private`, lines 169–176).

### 2.2 Unit Actions & Grid Isolation (`interpreter`, lines 913–940)
- Actions (`farmer`, `hands`) are applied sequentially in a player loop (`for i, s in enumerate(state)`).
- **Zero Spatial Interference**: Because all movement, planting, watering, care, and harvesting operate exclusively on `obs0.farms[i]` (line 935–940), there is **zero tile collision or spatial contention** between P0 and P1.

### 2.3 Market Clearance & Lockstep Quotation (`_process_market`, lines 544–630)
- **Atomic Orders (`HIRE`, `BUY_LAND`)**: Executed in player order (lines 572–582). However, costs are determined entirely by the individual player's own farm state (number of hires today, number of unlocked quadrants) and do not draw from a shared resource.
- **Trading Orders (`SELL`, `BUY_PRODUCT`, `BUY_SEED`, `BUY_ANIMAL`)**: Executed via **per-unit lockstep loop** (lines 583–628).
  - Quotes for both players are sampled *simultaneously* against pre-commit market inventory (`quoted = [None, None]`, line 590).
  - Both players see the exact same price for unit $k$ before transactions are committed (`_commit_unit`, line 618).
  - Dynamic price recalculation occurs only after simultaneous commitment (`_refresh_prices`, line 628).
  - **No Front-Running**: P0 cannot front-run P1 within the same market order slot.

### 2.4 End-of-Day Progression & RNG Consumption (`_end_of_day`, lines 860–893)
- **Seed Resolution**: Deterministically re-keyed at midnight:
  ```python
  rng = random.Random((seed * 1_000_003) ^ day)
  ```
- **Weed Spawning**: `_spawn_weeds` iterates over P0 then P1 with probability `weed_chance = 0.005` per empty tile. While P0 draws from the RNG stream first, the Bernoulli trials are identically distributed ($E[\text{weeds}] = 0.005 \times N_{\text{empty}}$ for both players).
- **Town Shop Unlocks**: Drawn from the same daily `rng` instance. Differences in shop timing or type are purely stochastic and exhibit no systematic directional bias toward either player index.

---

## 3. Seed Comparability & Trajectory Coupling

- **Seed Re-initialization**: The episode seed determines the base state and daily RNG sequence.
- **Trajectory Coupling**: In a 2-player match on a given seed, market price trajectories are coupled through shared product sales and purchases.
- **Cross-Match Comparability**: Using the same seed across different agent pairings does *not* produce identical price histories because agent trading decisions actively shape market inventory $I(t)$ and town consumption.

---

## 4. Conclusion & Tournament Design Recommendation

The environment is mathematically symmetric with respect to player indexing:
- P0 and P1 share identical game mechanics, pricing formulas, and starting conditions.
- The standard round-robin design where each agent plays exactly once as P0 and once as P1 guarantees complete structural balance across the tournament.
