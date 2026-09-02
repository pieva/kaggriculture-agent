# E16 — ANTIGRAVITY TRAINING DESIGN PROPOSAL

**Modeler:** `ANTIGRAVITY`  
**Date:** 2026-08-29  
**Status:** `CANDIDATE PROPOSAL` (Ready for cross-review)  
**Goal:** INITIAL BOUNDING + INTERACTION DISCRIMINATION

---

## A. DESIGN SUMMARY

```text
design_id: AGY-E16-TRAINING-V1
training_goal: Identificare i bounds iniziali e separare gli effetti causali tra irrigazione, superficie coltivata e carico livestock.
design_type: Minimal Fractional Factorial (Staged)
total_cells: 8
seeds_per_cell: 5
total_episodes: 40
staged: YES
```

---

## B. HYPOTHESES

```text
hypothesis_id: H_WATERING_THRESHOLD
concepts: watering_execution_rate, final_money_outcome
relationship: thresholded
current_evidence: Failure at 34 (Antigravity), competitive at 440 (Codex/Copilot). Interval [35-439] unobserved.
uncertainty_to_resolve: Location of the minimum viable threshold (elbow of the response curve).
falsification_condition: If WATER=100 produces FINAL_MONEY comparable to WATER=400, the threshold is very low and high irrigation is not strictly necessary.
```

```text
hypothesis_id: H_CROP_SURFACE_CURVE
concepts: crop_surface_maintained, state_capacity_alignment
relationship: thresholded / non_monotonic
current_evidence: 8-9 failed, 25-28 competitive, 37 lost to 28 in M2.
uncertainty_to_resolve: Diminishing returns/penalty for overextending crop surface beyond 25.
falsification_condition: If active_crops=35 with adequate watering matches or beats active_crops=25, the M2 result was due to monetization quality, not surface overextension.
```

```text
hypothesis_id: H_LIVESTOCK_OPPORTUNITY_COST
concepts: livestock_headcount, pasture_arable_surface_tradeoff
relationship: non_monotonic
current_evidence: 4-7 competitive, 17-18 failure.
uncertainty_to_resolve: Is 10 viable if adequately supported, or does the pasture/feed cost immediately degrade returns?
falsification_condition: If livestock=10 with WATER=400 achieves competitive FINAL_MONEY, then 4-7 is not an optimum, and the failure of 17-18 was due to extreme scale or poor implementation.
```

---

## C. FACTORS AND CONTROLS

| variable | role | type | candidate_values_or_control | rationale |
|---|---|---|---|---|
| `quadrants_owned` | CONTROL | PARAMETER | 2 | Controlled E16 baseline as prescribed. |
| `workforce_headcount` | CONTROL | PARAMETER | 9 | Held constant to prevent workforce/dispatch variations from confounding watering limits. |
| `watering_target` | MANIPULATED | PARAMETER | 100, 250, 400 | Tests failure bound (100), transition region (250), and competitive bound (400). |
| `active_crops_target`| MANIPULATED | PARAMETER | 15, 25, 35 | Tests compact (15), competitive (25), and extended bounds (35). |
| `livestock_headcount`| MANIPULATED | PARAMETER | 0, 4, 10 | Tests absence (0), competitive baseline (4), and unobserved mid-high range (10). |
| `feed_market_dependency`| OBSERVABILITY| DERIVED_METRIC| N/A | Monitored via event ledger to understand cash drain. |
| `species_margin_differential`| OBSERVABILITY| DERIVED_METRIC| N/A | Only Cows will be used to avoid species confounding. |

---

## D. EXPERIMENT CELLS

### STAGE 1 (Irrigation × Crop Working Set)

```text
cell_id: A1
factor_values: water=100, crops=25, livestock=4
comparison_role: Low-bound anchor
epistemic_question: Where is the failure floor for watering?
why_required: Establishes the lower bound of the transition region.
```

```text
cell_id: A2
factor_values: water=250, crops=25, livestock=4
comparison_role: Transition test
epistemic_question: Is 250 sufficient, or is the threshold higher?
why_required: Bisects the unobserved E15 gap [35-439].
```

```text
cell_id: A3
factor_values: water=400, crops=25, livestock=4
comparison_role: Central Baseline
epistemic_question: What is the expected performance of a known competitive setup under controlled conditions?
why_required: Serves as the central reference point for all other cells.
```

```text
cell_id: A4
factor_values: water=400, crops=15, livestock=4
comparison_role: Compact crop test
epistemic_question: Does a highly compact setup leave money on the table?
why_required: Identifies the lower bound of profitable crop surface.
```

```text
cell_id: A5
factor_values: water=400, crops=35, livestock=4
comparison_role: Extended crop test
epistemic_question: Does 35 crops degrade returns even with adequate watering?
why_required: Tests whether Codex's M2 loss was intrinsic to surface size or due to execution.
```

```text
cell_id: A6
factor_values: water=250, crops=35, livestock=4
comparison_role: Interaction stress test
epistemic_question: How rapidly does performance collapse when surface exceeds watering capacity?
why_required: Isolates the interaction effect between overextension and under-servicing.
```

### STAGE 2 (Livestock × Pasture)

*(Note: Cell A3 serves as the baseline for this stage: livestock=4)*

```text
cell_id: B1
factor_values: water=400, crops=25, livestock=0
comparison_role: Absence test
epistemic_question: What is the pure opportunity cost of maintaining livestock?
why_required: Establishes if livestock is strictly additive or parasitic at baseline levels.
```

```text
cell_id: B2
factor_values: water=400, crops=25, livestock=10
comparison_role: Scale test
epistemic_question: Can a herd of 10 be profitable if watering and crops are well-managed?
why_required: Tests the unobserved region between 7 (Codex) and 17 (Antigravity).
```

---

## E. STAGE / ADVANCEMENT RULES

**Staged:** YES

**Rule:** 
Stage 1 (A1-A6) is executed first. 
Stage 2 (B1-B2) is executed **ONLY IF** Cell A3 (the central baseline) achieves an average `FINAL_MONEY` > $15,000. 

*Rationale:* If A3 fails to establish a functional baseline due to implementation/policy errors in the agent, running Stage 2 will only produce confounded data where livestock effects cannot be separated from baseline dysfunction.

---

## F. SEED / OPPONENT PROTOCOL

- **Minimum seeds:** 5 (e.g., statically chosen `1000`, `2000`, `3000`, `4000`, `5000`).
- **Shared seeds:** Yes, the exact same 5 seeds must be used across all 8 cells.
- **Opponent configuration:** A static, "do-nothing" or minimal survival agent (e.g., an agent that just passes turns). 
  *Rationale:* This prevents opponent-driven market price fluctuations from confounding the internal efficiency metrics being tested.
- **Randomization:** Execution order of the 40 episodes should be randomized to prevent systematic infrastructure bias.
- **Evaluation criterion:** Pairwise t-tests or ANOVA against the central baseline (A3) to distinguish treatment effects from seed-induced variance.

---

## G. TELEMETRY REQUIREMENTS

1. **Mandatory Event Ledger:** As prescribed in the prompt (requested vs executed payloads, realized price, etc.).
2. **Additional Derived Metrics Required:**
   - `realized_wheat_cashflow`: Net realized value of all wheat BUY/SELL transactions.
   - `daily_watered_fraction`: (Crops watered today) / (Total active crops today).
   - `pasture_opportunity_cost`: Estimated revenue lost per tile converted to pasture (requires tracking baseline crop yield per tile).

---

## H. ANALYSIS PLAN

- **Primary Comparisons:**
  - `A3` vs `A1`, `A2`: Defines the watering response curve and locates the threshold.
  - `A3` vs `A4`, `A5`: Defines the crop surface response curve.
  - `A3` vs `B1`, `B2`: Defines the livestock scaling curve.
- **Secondary Comparisons:**
  - `A5` vs `A6`: Quantifies the penalty of the `crop_surface × watering_deficit` interaction.
- **Failure Handling:** Disqualified runs (e.g., timeouts) are excluded from statistical analysis and flagged for engineering review.
- **Forbidden Conclusions:** 
  - Identifying any cell as the "optimum" or "best strategy".
  - Using these results as validation data for E17.

---

## I. INFORMATION-GAIN AUDIT

| cell_id | information_gained | what_is_lost_if_removed |
|---|---|---|
| **A1** | Failure floor for watering | Cannot confirm if 100 is fatal. |
| **A2** | Transition region viability | Leaves massive gap between 100 and 400. |
| **A3** | Central baseline performance | Eliminates the control group for all comparisons. |
| **A4** | Floor for viable crop surface | Cannot measure penalty of being too compact. |
| **A5** | Ceiling for viable crop surface | Cannot determine if Codex M2 loss was intrinsic. |
| **A6** | Interaction penalty magnitude | Cannot prove that overextension *causes* service failure. |
| **B1** | Livestock absolute opportunity cost | Cannot prove if livestock are strictly necessary. |
| **B2** | Viability of medium-large herds | Leaves the [8-16] animal range permanently unobserved. |

*Redundant cells eliminated during design:* 
- Full factorial `water × crops × livestock` (27 cells) was reduced to a central composite design (8 cells) by assuming independence of extreme interactions outside of A6.

---

## J. COST

```text
total_cells: 8
episodes_per_cell: 5
total_episodes: 40
relative_cost_vs_E15: 13.3x (40 vs 3 episodes)
```

**MINIMAL Alternative:** 6 cells (30 episodes) — drop A6 (Interaction stress test) and B1 (Livestock absence test). 
*Epistemic penalty:* Loses the ability to quantify the exact penalty of overextension and the absolute necessity of livestock, but preserves the primary curve bounding.

---

## K. DESIGN RISKS

1. **Implementation Failure:** The agent's policy may fail to actually realize the target variables (e.g., targets WATER=400 but only achieves 50). This invalidates the cell.
2. **Static Opponent Artifacts:** Training against a static opponent may create a non-representative market environment, skewing price realizations.
3. **Cash Starvation Confounder:** High targets (e.g., 35 crops) may fail simply because the agent runs out of seed money, not because of intrinsic surface limits.
4. **Seed Variance:** 5 seeds might be insufficient to overcome RNG variance in crop yields or shop unlocks.
5. **Livestock Species Confounding:** If the agent buys sheep instead of cows, B2 results won't map cleanly to baseline expectations. (Must be controlled in code).

---

## L. RECOMMENDATION

```text
RECOMMENDED_DESIGN: AGY-E16-TRAINING-V1
READY_FOR_CROSS_REVIEW: YES
BLOCKERS: NONE
```
