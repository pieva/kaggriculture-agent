# Project State

**Last update:** 2026-08-29
**Current State:** `PRE-TOURNAMENT CHECKPOINT COMPLETE` (Ready for E15 Match Execution)

---

## 1. Current Phase: E15.0 — Pre-Tournament Freeze & Governance (COMPLETED)

- **E14 — Repository Isolation & Canonical Ontology (COMPLETED)**:
  - Repository isolated across three independent candidate architectures: **Antigravity**, **Codex**, **Copilot**.
  - Canonical Ontology established in `docs/model_specs/ONTOLOGY.md` containing exactly **64 canonical concept_ids**.
  - All three independent `MODEL_SPEC.md` files mapped 64/64 canonical concepts with zero missing/extra concepts.
- **E15.0 — Pre-Tournament Freeze & Enforcement (COMPLETED)**:
  - **7/7 Frozen Artifacts** committed and locked under `results/e15/freeze/` with SHA256 manifest `results/e15/freeze/FREEZE_MANIFEST.md`.
  - **Copilot Ownership**: Independently verified and certified in `docs/model_specs/copilot/E15_0a_OWNERSHIP_VERIFICATION_REPORT.md`.
  - **P0/P1 Environment Audit**: Certified `NO_MATERIAL_POSITION_BIAS_FOUND` in `results/e15/P0_P1_ENVIRONMENT_AUDIT.md`.
  - **Freeze Enforcement Runner**: `scripts/run_e15_tournament.py` executes directly and exclusively from `results/e15/freeze/`, with SHA256 pre-execution validation and fail-closed abort.
  - **Final Certification**: Codex E15.0d review issued `ACCEPT_E15_FREEZE`.
- **Match Status**: **0 / 3 matches executed** (`NO MATCH EXECUTED`).

---

## 2. Frozen Candidates & SHA256 Integrity Registry

All competitive executions use exclusively the frozen artifacts verified in `results/e15/freeze/FREEZE_MANIFEST.md`:

| Artifact | Source Path | Frozen Path | SHA256 Checksum |
|---|---|---|---|
| **Canonical Ontology** | `docs/model_specs/ONTOLOGY.md` | `results/e15/freeze/ONTOLOGY_E15_FROZEN.md` | `5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa` |
| **Antigravity MODEL_SPEC** | `docs/model_specs/antigravity/MODEL_SPEC.md` | `results/e15/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md` | `f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46` |
| **Codex MODEL_SPEC** | `docs/model_specs/codex/MODEL_SPEC.md` | `results/e15/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md` | `9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7` |
| **Copilot MODEL_SPEC** | `docs/model_specs/copilot/MODEL_SPEC.md` | `results/e15/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md` | `d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686` |
| **Antigravity Submission** | `submission/submission_antigravity.py` | `results/e15/freeze/submission_antigravity_E15_FROZEN.py` | `629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d` |
| **Codex Submission** | `submission/submission_codex.py` | `results/e15/freeze/submission_codex_E15_FROZEN.py` | `fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3` |
| **Copilot Submission** | `submission/submission_copilot.py` | `results/e15/freeze/submission_copilot_E15_FROZEN.py` | `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb` |

---

## 3. Pre-Declared Tournament Schedule & Seeds

Tournament plan defined in `results/e15/TOURNAMENT_PLAN.md`:

| Match ID | Player 0 (P0) | Player 1 (P1) | Pre-Declared Seed | Status |
|---|---|---|:---:|:---:|
| **M1** | Antigravity | Codex | `1113294977` | `READY (NEXT ACTION)` |
| **M2** | Codex | Copilot | `3033283457` | `FROZEN_PENDING_M1` |
| **M3** | Copilot | Antigravity | `3122977751` | `FROZEN_PENDING_M2` |

### Pre-Declared Tie-Breaking Criteria:
1. **Primary**: Number of head-to-head match wins (W-L record).
2. **Tie-Break (if all 1–1)**: Aggregate signed final-money differential $D_i = \sum (\text{final\_money}_i - \text{final\_money}_{\text{opponent}})$.

---

## 4. Python Environment & Verification

- **Python**: `3.12.13` (via `.venv`)
- **Kaggle Environments**: `1.32.7` (`kaggriculture` v0.1.0)
- **Validation Command**: `python scripts/run_e15_tournament.py --validate`
- **Validation Status**: `FREEZE INTEGRITY: PASS` | `M1/M2/M3: READY` | `NO MATCH EXECUTED`

---

## 5. Next Immediate Action for New Session

```powershell
python scripts/run_e15_tournament.py --match M1
```
*Strict rule: Do NOT run M2 or M3 until M1 has been executed and evaluated through the neutral post-match review protocol.*
