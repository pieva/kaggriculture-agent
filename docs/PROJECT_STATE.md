# Project State

**Last update:** 2026-08-29
**Current State:** `E15 EPISTEMICALLY CLOSED` (Competitive Winner: Copilot 2–0)

---

## 1. Current Phase: E15 — Pairwise Tournament (COMPLETED & EPISTEMICALLY CLOSED)

- **E14 — Repository Isolation & Canonical Ontology (COMPLETED)**:
  - Repository isolated across three independent candidate architectures: **Antigravity**, **Codex**, **Copilot**.
  - Canonical Ontology established in `docs/model_specs/ONTOLOGY.md` containing exactly **64 canonical concept_ids**.
  - All three independent model specs mapped 64/64 canonical concepts with zero missing/extra concepts.
- **E15.0 — Pre-Tournament Freeze & Enforcement (COMPLETED)**:
  - **7/7 Frozen Artifacts** committed and locked under `results/e15/freeze/` with SHA256 manifest `results/e15/freeze/FREEZE_MANIFEST.md`.
  - **Copilot Ownership**: Independently verified and certified in `docs/model_specs/copilot/E15_0a_OWNERSHIP_VERIFICATION_REPORT.md`.
  - **P0/P1 Environment Audit**: Certified `NO_MATERIAL_POSITION_BIAS_FOUND` in `results/e15/P0_P1_ENVIRONMENT_AUDIT.md`.
  - **Freeze Enforcement Runner**: `scripts/run_e15_tournament.py` executes directly and exclusively from `results/e15/freeze/`, with SHA256 pre-execution validation and fail-closed abort.
- **E15 Tournament Execution & Post-Match Consensus (COMPLETED)**:
  - **M1 (Seed 1113294977)**: Antigravity ($8,672) vs Codex ($20,461) — Winner: **Codex**. Double ACK closed (`ACK_M1_CONSENSUS_ANTIGRAVITY`, `ACK_M1_CONSENSUS_CODEX`).
  - **M2 (Seed 3033283457)**: Codex ($27,510) vs Copilot ($37,752) — Winner: **Copilot**. Double ACK closed (`ACK_M2_CONSENSUS_CODEX`, `ACK_M2_CONSENSUS_COPILOT`).
  - **M3 (Seed 3122977751)**: Copilot ($26,629) vs Antigravity ($9,371) — Winner: **Copilot**. Double ACK closed (`ACK_M3_CONSENSUS_ANTIGRAVITY`, `ACK_M3_CONSENSUS_COPILOT`).
- **Competitive Winner**: **Copilot (2–0)** (Codex: 1–1, Antigravity: 0–2). Tie-break not required.
- **Frozen Artifacts**: `UNCHANGED`.
- **Tournament Synthesis Artifact**: `results/e15/E15_FINAL_TOURNAMENT_SYNTHESIS.md`.

---

## 2. Core Epistemic Findings & Two-Regime Empirical Model

### Key Replicated Findings:
1. **Antigravity Failure Mode Replication (M1 & M3)**:
   - Systematically replicated across seeds: extremely low watering (34 vs 30), unharvested crop drop, high movement (5,019 vs 5,047), over-expanded nominal footprint (3Q, 12 hands, 18 pasture/livestock) with severely depressed active maintained crop surface (8–9 crops).
2. **Copilot Policy Footprint Stability (M2 & M3)**:
   - Replicated compact working set: high continuous watering (446 vs 439), compact livestock (5 pasture, 4 animals), 9 hands, intensive monetization (298 vs 302 sell orders).
3. **State-Capacity Alignment & Monetized Capacity**:
   - Nominal capacity $\neq$ activated/maintained/monetized capacity.
   - Raw action volume or physical land scale without operational maintenance and monetization is counterproductive.

### Two-Regime Empirical Model:
1. **Regime A — Below Operational Threshold (Sub-threshold)**:
   - When irrigation, dispatch, or maintenance fail, working surface collapses. Nominal assets amplify misalignment. Irrigation, dispatch, and basic maintenance dominate outcomes (observed in M1 and M3).
2. **Regime B — Above Operational Threshold (Super-threshold)**:
   - When watering and maintenance are stabilized, raw physical capacity ceases to be monotonically beneficial. Monetization quality, state-capacity alignment, capital timing, inventory-to-cash conversion, and sell-through dominate outcomes (observed in M2).

---

## 3. Frozen Candidates & SHA256 Integrity Registry

All competitive executions strictly verified against `results/e15/freeze/FREEZE_MANIFEST.md`:

| Artifact | Source Path | Frozen Path | SHA256 Checksum |
|---|---|---|---|
| **Canonical Ontology** | `docs/model_specs/ONTOLOGY.md` | `results/e15/freeze/ONTOLOGY_E15_FROZEN.md` | `5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa` |
| **Antigravity MODEL_SPEC** | `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY.md` | `results/e15/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md` | `f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46` |
| **Codex MODEL_SPEC** | `docs/model_specs/codex/MODEL_SPEC_CODEX.md` | `results/e15/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md` | `9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7` |
| **Copilot MODEL_SPEC** | `docs/model_specs/copilot/MODEL_SPEC_COPILOT.md` | `results/e15/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md` | `d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686` |
| **Antigravity Submission** | `submission/submission_antigravity.py` | `results/e15/freeze/submission_antigravity_E15_FROZEN.py` | `629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d` |
| **Codex Submission** | `submission/submission_codex.py` | `results/e15/freeze/submission_codex_E15_FROZEN.py` | `fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3` |
| **Copilot Submission** | `submission/submission_copilot.py` | `results/e15/freeze/submission_copilot_E15_FROZEN.py` | `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb` |

---

## 4. Completed Tournament Summary

| Match ID | Player 0 (P0) | Player 1 (P1) | Seed | Final Scores | Winner | Status |
|---|---|---|:---:|:---:|:---:|:---:|
| **M1** | Antigravity | Codex | `1113294977` | $8,672 vs $20,461 | **Codex** | `CLOSED (Double ACK)` |
| **M2** | Codex | Copilot | `3033283457` | $27,510 vs $37,752 | **Copilot** | `CLOSED (Double ACK)` |
| **M3** | Copilot | Antigravity | `3122977751` | $26,629 vs $9,371 | **Copilot** | `CLOSED (Double ACK)` |

### Final Tournament Standings:
1. **Copilot**: 2–0 (Competitive Winner)
2. **Codex**: 1–1
3. **Antigravity**: 0–2

---

## 5. Next Mandatory Phase: POST-E15 — MODEL CAPABILITY CHECK

> [!IMPORTANT]
> **MANDATORY GATE:** Run the Model Capability Check across Antigravity, Codex, and Copilot BEFORE authorizing any MODEL_SPEC revision or new submission code generation.
>
> Rules:
> 1. DO NOT MODIFY E15 FROZEN ARTIFACTS.
> 2. DO NOT REVISE MODEL_SPEC BEFORE CAPABILITY CHECK.
> 3. DO NOT GENERATE NEW SUBMISSIONS YET.
