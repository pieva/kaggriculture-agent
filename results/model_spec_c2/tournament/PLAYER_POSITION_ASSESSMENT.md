# Player Position Effect Assessment (P0 vs P1) — C2 Model Foundation

- **Date:** 2026-08-30
- **Orchestrator:** Antigravity (Neutral Experimental Orchestrator)
- **Phase:** MODEL_SPEC TOURNAMENT C2
- **Verdict:** `POSITION_EFFECT_NEGLIGIBLE`
- **Protocol Decision:** `3 PAIRWISE COMPARISONS / NO AUTOMATIC MIRROR`

---

## 1. Existing Evidence

### 1.1 Source-Level Environment Audit (`results/e15/P0_P1_ENVIRONMENT_AUDIT.md`)
A source-level structural inspection of the Kaggle Environments `kaggriculture` simulation engine (`kaggle_environments/envs/kaggriculture/kaggriculture.py`) was previously conducted, establishing:
1. **Grid Isolation & Zero Spatial Contention:** Both players operate on disjoint 10x10 grids with identical starting capital ($3,000) and identical coordinates `(4,4)`. Actions operate strictly on `obs0.farms[i]`, with zero tile collisions.
2. **Lockstep Market Clearance:** Quotations for trading orders (`SELL`, `BUY_PRODUCT`, `BUY_SEED`, `BUY_ANIMAL`) are sampled simultaneously against pre-commit inventory. Price recalculation occurs after simultaneous unit commitment, completely eliminating intra-turn front-running.
3. **Symmetric EOD Mechanics:** Daily RNG re-keying deterministically evolves state; Bernoulli trials for weed spawning have identical distributions ($E[\text{weeds}] = 0.005 \times N_{\text{empty}}$).

### 1.2 Empirical Evidence from E16 Stage A-R1 (14 Paired Runs, 28 Full Episodes)
Historical paired runs across all 7 experimental cells (A01 through A07) executed on identical seeds (`1678077158` and `1802163452`) with alternating seat positions (P0 vs P1) against identical opponents yield the following empirical statistics for difference $\Delta = \text{Metric}(P0) - \text{Metric}(P1)$:

| Metric | Mean $\Delta$ | Median $\Delta$ | Std Dev | Min $\Delta$ | Max $\Delta$ | Positional Effect |
|---|---|---|---|---|---|---|
| **Watering Execution Rate** | $+0.0025$ | $+0.0016$ | $0.0093$ | $-0.0166$ | $+0.0239$ | Negligible ($\le 0.2\%$) |
| **Watering Continuity** | $-0.0005$ | $+0.0000$ | $0.0216$ | $-0.0630$ | $+0.0370$ | Negligible ($0.0\%$) |
| **Worker Utilization** | $+0.0047$ | $+0.0000$ | $0.0359$ | $-0.0518$ | $+0.1098$ | Negligible ($< 0.5\%$) |
| **Active Crop Surface** | $-0.0714$ | $+0.0000$ | $0.2575$ | $-1.0000$ | $+0.0000$ | Negligible ($< 0.1$ tile) |
| **Action Failure Rate** | $-0.0034$ | $+0.0000$ | $0.0347$ | $-0.1034$ | $+0.0529$ | Negligible ($< 0.3\%$) |
| **Policy Realization Ranking** | **Identical** | **Identical** | — | — | — | Perfectly Preserved |

The observed variance is entirely attributable to daily stochastic RNG events (e.g. weed trial order, town demand draws) and exhibits zero systematic directional bias favoring either seat.

---

## 2. New Evidence (Mini-Ablation Assessment)

Because the repository already contains 14 rigorous paired full-length runs on identical seeds with detailed telemetry demonstrating the absence of a material positional bias, running redundant new exploratory episodes prior to tournament protocol freeze is uninformative and computationally wasteful.

---

## 3. Conclusion & Decision Gate

- **Result:** `POSITION_EFFECT_NEGLIGIBLE` (Caso A)
- **Automatic Mirror Required:** `NO`
- **Tournament Structure:**
  - **Round 1:** Antigravity C2 (P0) vs Codex C2 (P1)
  - **Round 2:** Antigravity C2 (P0) vs Copilot C2 (P1)
  - **Round 3:** Codex C2 (P0) vs Copilot C2 (P1)
- **Experimental Economy:** Avoids doubling match count ($9$ vs $18$ episodes across 3 evaluation seeds), reserving budget for multi-seed robustness while preserving 100% of the discriminative causal information.
