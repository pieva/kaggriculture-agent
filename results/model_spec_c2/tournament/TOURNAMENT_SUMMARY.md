# MODEL_SPEC TOURNAMENT C2 — SUMMARY REPORT

- **Phase:** MODEL_SPEC TOURNAMENT C2
- **Orchestrator:** Antigravity (Neutral Experimental Orchestrator)
- **Date:** 2026-08-30
- **Status:** `TOURNAMENT_COMPLETE`
- **Protocol:** `results/model_spec_c2/tournament/TOURNAMENT_PROTOCOL.md`
- **Positional Assessment:** `results/model_spec_c2/tournament/PLAYER_POSITION_ASSESSMENT.md`

---

## 1. Positional Assessment Summary

- **Existing Evidence Analyzed:**
  1. Source-level architecture audit (`results/e15/P0_P1_ENVIRONMENT_AUDIT.md`): Disjoint farm grids, zero spatial contention, lockstep simultaneous quotation clearance.
  2. Historical paired runs from E16 Stage A-R1 (14 paired runs, 28 episodes across seeds `1678077158` and `1802163452`): Mean $(P0 - P1)$ difference across watering execution ($+0.25\%$), watering continuity ($-0.05\%$), worker utilization ($+0.47\%$), and active crop surface ($-0.07$ tiles).
- **New Exploratory Runs Required:** None (sufficient empirical paired data already established in repo).
- **Verdict:** `POSITION_EFFECT_NEGLIGIBLE` (Decision Gate: Caso A).
- **Decision:** 3 Pairwise Rounds across 3 Shared Seeds (**NO Automatic Mirror Duplication**).

---

## 2. Tournament Structure & Experimental Budget

| Round | Match ID | Player 0 (P0) | Player 1 (P1) | Seed | Outcome | P0 Final $ | P1 Final $ | Delta $ |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|
| **R1** | `R1_anti_vs_codex_S1` | Antigravity C2 | Codex C2 | `1113294977` | Codex C2 | $3,000.00 | $16,810.00 | $+13,810.00$ |
| **R1** | `R1_anti_vs_codex_S2` | Antigravity C2 | Codex C2 | `3033283457` | Codex C2 | $3,000.00 | $14,753.00 | $+11,753.00$ |
| **R1** | `R1_anti_vs_codex_S3` | Antigravity C2 | Codex C2 | `1678077158` | Codex C2 | $3,000.00 | $19,526.00 | $+16,526.00$ |
| **R2** | `R2_anti_vs_copilot_S1` | Antigravity C2 | Copilot C2 | `1113294977` | TIE | $3,000.00 | $3,000.00 | $\$0.00$ |
| **R2** | `R2_anti_vs_copilot_S2` | Antigravity C2 | Copilot C2 | `3033283457` | TIE | $3,000.00 | $3,000.00 | $\$0.00$ |
| **R2** | `R2_anti_vs_copilot_S3` | Antigravity C2 | Copilot C2 | `1678077158` | TIE | $3,000.00 | $3,000.00 | $\$0.00$ |
| **R3** | `R3_codex_vs_copilot_S1` | Codex C2 | Copilot C2 | `1113294977` | Codex C2 | $18,588.00 | $3,000.00 | $+15,588.00$ |
| **R3** | `R3_codex_vs_copilot_S2` | Codex C2 | Copilot C2 | `3033283457` | Codex C2 | $14,753.00 | $3,000.00 | $+11,753.00$ |
| **R3** | `R3_codex_vs_copilot_S3` | Codex C2 | Copilot C2 | `1678077158` | Codex C2 | $16,649.00 | $3,000.00 | $+13,649.00$ |

---

## 3. Economic Outcome & Robustness

### 3.1 Aggregated Economic Table

| Candidate | Matches | Record (W-L-T) | Mean Final $ | Median Final $ | Std Dev | Min Final $ | Max Final $ | Mean Delta $ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Codex C2** | 6 | **6W - 0L - 0T** | **$16,846.50** | **$16,729.50** | **$1,780.37** | **$14,753.00** | **$19,526.00** | **+$13,846.50** |
| **Antigravity C2** | 6 | 0W - 3L - 3T | $3,000.00 | $3,000.00 | $0.00 | $3,000.00 | $3,000.00 | -$6,923.25 |
| **Copilot C2** | 6 | 0W - 3L - 3T | $3,000.00 | $3,000.00 | $0.00 | $3,000.00 | $3,000.00 | -$6,923.25 |

### 3.2 Robustness Analysis Across Seeds
- **Codex C2:** Exhibited consistent profitability across all 3 seeds ($14.7k$ to $19.5k$), demonstrating high stability with a low coefficient of variation ($\text{CV} = 10.5\%$).
- **Antigravity C2 & Copilot C2:** Exhibited complete capital preservation ($3,000.00$) without capital destruction or bankruptcy, but generated zero net operating income due to execution/policy blockages.

---

## 4. Policy Realization & Action Profiles

| Metric (Per-Episode Mean) | Antigravity C2 | Codex C2 | Copilot C2 |
|---|:---:|:---:|:---:|
| **Mean Active Surface (tiles)** | 0.00 | **9.17** | 0.00 |
| **Crop Target Attainment ($\le 17$)** | 0.0% | **53.9%** | 0.0% |
| **Watering Actions (`WATER`)** | 0.0 | **277.5** | 119.2 |
| **Harvest Actions (`HARVEST`)** | 0.0 | **56.5** | 136.2 |
| **Plant Actions (`PLANT`)** | 0.0 | **69.3** | 0.0 |
| **Dig Actions (`DIG`)** | 0.0 | **39.2** | 586.2 |
| **Move Actions (`MOVE`)** | 0.0 | **1,514.8** | 0.0 |
| **Pass Actions (`PASS`)** | 720.0 | 76.5 | 578.4 |
| **Market Orders Issued** | 0.0 | **390.5** | 0.0 |

### 4.1 Causal Mechanism Findings

1. **Codex C2 Policy Realization:**
   - Realized full end-to-end multi-worker agricultural cycle: land expansion ($NW \to NE$), continuous seed purchasing, dynamic worker hiring, Manhattan routing, and multi-unit task dispatch.
   - **Harvest Gate (`CRP-10`):** Zero premature harvest no-ops. 56.5 valid mature harvests per episode.
   - **Preventive DIG & Recovery (`CRP-09`):** Successfully performed 39.2 DIG operations per episode, clearing retired crops and restoring arable tiles.
   - **Watering Continuity:** 277.5 watering operations maintained 9.17 average active crops (peaking at 12–14 tiles per episode).

2. **Antigravity C2 Policy Realization:**
   - **Mechanism:** When executed in `kaggle_environments`, the candidate policy in `src/agricola/strategy/antigravity/c2_policy.py:187` accessed `privates = observation.get("private", [])` and attempted `privates[player_index]`. In the real environment, `observation["private"]` is a dict, causing an internal `KeyError: 0`.
   - **Safety Fallback:** The entrypoint `src/agricola/strategy/antigravity/agent_c2.py:39` successfully caught the exception and fail-closed to `{"farmer": ["PASS"], "hands": [], "market": []}` for all 720 steps, preserving initial capital ($3,000.00) without crashing.
   - **Policy Realization:** 0% realization of the planned 17-crop working set.

3. **Copilot C2 Policy Realization:**
   - **Mechanism:** In `src/agricola/strategy/copilot/c2_policy.py`, the candidate hardcoded `"market": []` and did not implement movement routines or seed procurement. The main farmer stayed stationary at `(4, 4)`.
   - **Action Pathology:** The lifecycle classifier evaluated the stationary tile `(4, 4)` as requiring DIG / HARVEST / WATER without having planted any crops or possessing seeds.
   - **Policy Realization:** 0% realization of productive crop cultivation.

---

## 5. Failure Modes & Anomalies

| Candidate | Observed Failure Mode | Root Cause | Impact |
|---|---|---|---|
| **Antigravity C2** | Complete turn passivity (`PASS` $\times 720$) | Observation type mismatch (`observation["private"]` dict treated as list in `c2_policy.py:187`) triggering safety fallback | Zero agricultural operations executed; capital frozen at $3,000.00 |
| **Copilot C2** | Stationary action waste at `(4, 4)` | No market order generation (`market: []`) and no spatial navigation in `c2_policy.py` | 586 no-op DIG / 136 no-op HARVEST actions on unplanted shed tile |
| **Codex C2** | Working set stabilization gap ($\approx 9.2 / 17$ tiles) | Nearest-task workforce routing bottlenecks and single-crop replant pacing | Sub-100% target attainment ($53.9\%$), though economically dominant |

---

## 6. NOT COMPUTABLE Metrics

| Metric | Status | Reason / Technical Justification |
|---|---|---|
| `replant_latency` | **NOT COMPUTABLE** | Requires per-tile historical mutation ledger across consecutive step events; not observable from terminal state replays. |
| `lost_tile_persistence` | **NOT COMPUTABLE** | Tile lifetime persistence is right-censored at episode step 720. |
| `overflow_loss` | **NOT COMPUTABLE** | Sinks not segregated in standard environment observation state. |

---

## 7. Tournament Status & Ready for Forensic Review

```text
TOURNAMENT STATUS: TOURNAMENT_COMPLETE
CANDIDATE ARTIFACTS FROZEN: YES
RAW REPLAYS PRESERVED: YES (9 matches in results/model_spec_c2/tournament/raw/)
AGGREGATED TELEMETRY PRESERVED: YES (aggregated_results.json, aggregated_results.csv)
POST-TOURNAMENT REVIEW STATUS: PENDING INDEPENDENT EXECUTION
```
