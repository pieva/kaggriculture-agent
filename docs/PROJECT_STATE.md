# Project State

**Last update:** 2026-08-30
**Current phase:** `MODEL_SPEC TOURNAMENT C2 — READY TO RUN`
**Repository Test Suite:** `168 passed`
**Repository Hygiene:** `git diff --check PASS`

---

## 1. Current Phase Summary

```text
Current phase:
MODEL_SPEC TOURNAMENT C2 — READY TO RUN

Foundation:
C2 upstream-ready
Feature Model blockers closed
Foundation C2: NOT FROZEN (upstream-ready, non-blocking for tournament)

Candidates:
Antigravity C2 — TOURNAMENT_READY (YES)
Codex C2       — TOURNAMENT_READY (YES)
Copilot C2     — TOURNAMENT_READY (YES)

Repository validation:
168 passed
git diff --check PASS

Tournament:
NOT RUN

Post-tournament reviews:
PENDING

Kaggle validation:
NOT RUN
```

---

## 2. Foundation C2 Status

- **Ontology C2:** `docs/model/ontology/ONTOLOGY_C2.md` — Formal vocabulary, lifecycle states, FEED+CARE mechanics defined.
- **State Machine C2:** `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md` — 11-phase execution cycle, lifecycle transitions, EOD bonus mechanics verified.
- **Feature Model C2:** `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md` — Canonical feature contracts established, blockers closed.
- **Freeze Status:** `NOT FROZEN` (upstream-ready for model specs; no formal freeze procedure executed, does not block tournament).

---

## 3. C2 Candidates Overview

### 3.1 Antigravity C2
- **MODEL_SPEC:** `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md`
- **Candidate Executable:** `src/agricola/strategy/antigravity/agent_c2.py`
- **Policy / Config:** `src/agricola/strategy/antigravity/c2_policy.py`, `src/agricola/strategy/antigravity/c2_config.py`
- **Verification:** `results/model_spec_c2/antigravity/BUILD_VERIFICATION.md` (`TOURNAMENT_READY: YES`)
- **Tests:** `tests/test_antigravity_c2.py` (PASS)

### 3.2 Codex C2
- **MODEL_SPEC:** `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md`
- **Candidate Executable:** `src/agricola/strategy/codex_c2.py`
- **Configuration:** `configs/model_spec_c2/CODEX_C2_CONFIG.json`
- **Verification:** `results/model_spec_c2/codex/BUILD_VERIFICATION.md` (`TOURNAMENT_READY: YES`)
- **Tests:** `tests/test_codex_c2_candidate.py` (PASS)

### 3.3 Copilot C2
- **MODEL_SPEC:** `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md`
- **Candidate Executable:** `src/agricola/strategy/copilot/agent_c2.py`
- **Policy / Config:** `src/agricola/strategy/copilot/c2_policy.py`, `src/agricola/strategy/copilot/c2_config.py`
- **Verification:** `results/model_spec_c2/copilot/BUILD_VERIFICATION.md` (`TOURNAMENT_READY: YES`)
- **Tests:** `tests/test_copilot_c2.py` (PASS)

---

## 4. Next Phase Protocol (Handoff)

1. Common tournament protocol definition & freeze (same seeds, opponents, telemetry, budget).
2. Direct 3-way evaluation execution.
3. Comparative post-tournament forensic reviews across all 3 agents.
4. Winner selection & external Kaggle validation.
