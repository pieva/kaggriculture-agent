# TOURNAMENT PROTOCOL — MODEL_SPEC TOURNAMENT C2

- **Phase:** MODEL_SPEC TOURNAMENT C2
- **Orchestrator:** Antigravity (Neutral Experimental Orchestrator)
- **Status:** `FROZEN_TOURNAMENT_PROTOCOL`
- **Date:** 2026-08-30
- **Git Branch:** `main`
- **Position Effect Verdict:** `POSITION_EFFECT_NEGLIGIBLE` (No Automatic Mirror)

---

## 1. Frozen Candidates & Artifact Provenance

| Candidate | MODEL_SPEC | Executable Path | Configuration Path | Build Verification |
|---|---|---|---|---|
| **Antigravity C2** | `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md` | `src/agricola/strategy/antigravity/agent_c2.py` | `src/agricola/strategy/antigravity/c2_config.py` | `results/model_spec_c2/antigravity/BUILD_VERIFICATION.md` |
| **Codex C2** | `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md` | `src/agricola/strategy/codex_c2.py` | `configs/model_spec_c2/CODEX_C2_CONFIG.json` | `results/model_spec_c2/codex/BUILD_VERIFICATION.md` |
| **Copilot C2** | `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md` | `src/agricola/strategy/copilot/agent_c2.py` | `src/agricola/strategy/copilot/c2_config.py` | `results/model_spec_c2/copilot/BUILD_VERIFICATION.md` |

**Candidate Immutability Rule:** No edits, tuning, refactoring, or heuristic transfers permitted during or after the tournament.

---

## 2. Match Structure & Shared Seeds

The tournament consists of **3 Pairwise Rounds**, each executed across **3 Pre-Declared Shared Seeds**:

| Round | Player 0 (P0) | Player 1 (P1) | Seed 1 (`E15_BENCH`) | Seed 2 (`HIGH_VAR`) | Seed 3 (`E16_STAGE_A`) | Total Runs |
|---|---|---|:---:|:---:|:---:|:---:|
| **Round 1 (R1)** | Antigravity C2 | Codex C2 | `1113294977` | `3033283457` | `1678077158` | 3 |
| **Round 2 (R2)** | Antigravity C2 | Copilot C2 | `1113294977` | `3033283457` | `1678077158` | 3 |
| **Round 3 (R3)** | Codex C2 | Copilot C2 | `1113294977` | `3033283457` | `1678077158` | 3 |

**Total Tournament Runs:** $3 \times 3 = 9$ full episodes (6,480 total simulation steps).

---

## 3. Environment & Simulation Parameters

- **Engine:** `kaggle_environments` `kaggriculture` (v0.1.0)
- **Episode Steps:** 720 steps (30 days $\times$ 24 hours)
- **Starting Money:** $3,000 per player
- **Starting Board:** 10x10 grid, NW quadrant unlocked (`["NW"]`)
- **Starting Coordinates:** Farmer at `(4, 4)`
- **Shed Capacity:** Default (100 units)
- **Market Dynamics:** Default dynamic quotation with simultaneous per-unit clearance

---

## 4. Common Instrumentation & Telemetry

Both agents in every match are instrumented under strictly identical observation collectors.

### 4.1 Computable Metrics
1. **Economic Performance:**
   - `final_money` (Terminal cash reward)
   - `money_trajectory` (Step-by-step cash evolution)
2. **Execution & Robustness:**
   - `completion` (720 steps reached with status `DONE`)
   - `disqualification_rate` (`INVALID` or `ERROR` occurrences)
   - `decision_latency_ms` (Mean and P99 latency per turn)
3. **Action Distribution:**
   - `WATER`, `PLANT`, `HARVEST`, `DIG`, `CARE`, `FEED`, `COLLECT_FERTILIZER`, `MOVE`, `PASS`
4. **Market Orders:**
   - `BUY_LAND`, `HIRE`, `BUY_SEED`, `BUY_PRODUCT`, `BUY_ANIMAL`, `SELL`
5. **Crop & Surface Realization:**
   - `active_crop_surface` (Active `PLANT` tiles)
   - `harvest_ready_surface` (`PLANT` tiles meeting yield and age criteria)
   - `weed_count` (`WEED` tiles on grid)

### 4.2 NOT COMPUTABLE Metrics (with Rationale)
- `replant_latency`: Non-computable without historical per-tile mutation tracking that requires modifying the simulation engine.
- `lost_tile_persistence`: Censored at episode termination unless lifetime tracking ledger is attached.
- `premature_harvest_count`: Only observable if agent explicitly emits `HARVEST` on immature crop.
- `overflow_loss`: Sinks not separated in standard environment observation without intrusive wrapper.

---

## 5. Failure Handling & Comparability Criteria

1. **Fail-Closed Execution:** If an agent throws an unhandled exception, `kaggle_environments` assigns `INVALID`/`ERROR` status and terminal reward `None` or 0.
2. **Error-Containment Fallback:** If an agent's internal fallback catches exceptions and returns `PASS`, the match completes cleanly with `status: DONE` and the resulting economic/policy realization is recorded faithfully as produced.
3. **Ranking Criteria:**
   - Primary: Mean `final_money` across all played tournament episodes.
   - Secondary: Pairwise Head-to-Head win-loss record.
   - Tertiary: Aggregate signed money differential:
     $$\Delta = \sum_{m} \left( \text{final\_money}_{\text{candidate}}^{(m)} - \text{final\_money}_{\text{opponent}}^{(m)} \right)$$

---

## 6. Freeze Commitment

This protocol is frozen prior to tournament execution. No modifications to seeds, match configurations, or scoring rules are permitted based on intermediate tournament outcomes.
