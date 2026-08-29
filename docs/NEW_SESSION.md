# NEW SESSION — Kaggriculture Agent

- **Experiment Phase**: `E15 — PAIRWISE TOURNAMENT`
- **Current State**: `PRE-TOURNAMENT FREEZE COMPLETE & VERIFIED`
- **Next Action**: **`RUN M1 ONLY`**
- **Match M1**: **Antigravity (P0) vs Codex (P1)** | **Seed**: `1113294977`

---

## 1. Quick Start & Execution Command

To execute Match 1 strictly under the certified freeze governance, run:

```powershell
.\.venv\Scripts\python.exe scripts/run_e15_tournament.py --match M1
```

> [!IMPORTANT]
> **DO NOT RUN M2 OR M3 UNTIL M1 HAS BEEN FULLY EXECUTED, PARSED, AND EVALUATED THROUGH THE MULTI-AGENT POST-MATCH PROTOCOL.**

---

## 2. Certified Pre-Match Freeze Status

The tournament baseline is 100% frozen, hash-locked, and fail-closed:
- **Codex Final Review Status**: `ACCEPT_E15_FREEZE`
- **SHA256 Manifest Integrity**: `7/7 MATCH` (`results/e15/freeze/FREEZE_MANIFEST.md`)
- **Execution Mechanism**: `scripts/run_e15_tournament.py` executes **directly and exclusively from `results/e15/freeze/`**.
- **Fail-Closed Protection**: Any hash mismatch or missing frozen file automatically aborts before environment instantiation.

### Frozen Artifacts Registry:
| Artifact | Frozen Path | SHA256 (Expected & Verified) |
|---|---|---|
| **Canonical Ontology** | `results/e15/freeze/ONTOLOGY_E15_FROZEN.md` | `5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa` |
| **Antigravity MODEL_SPEC** | `results/e15/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md` | `f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46` |
| **Codex MODEL_SPEC** | `results/e15/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md` | `9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7` |
| **Copilot MODEL_SPEC** | `results/e15/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md` | `d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686` |
| **Antigravity Submission** | `results/e15/freeze/submission_antigravity_E15_FROZEN.py` | `629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d` |
| **Codex Submission** | `results/e15/freeze/submission_codex_E15_FROZEN.py` | `fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3` |
| **Copilot Submission** | `results/e15/freeze/submission_copilot_E15_FROZEN.py` | `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb` |

---

## 3. Tournament Structure & Seed Schedule

| Match | Player 0 (P0) | Player 1 (P1) | Seed (Pre-Declared) | Status |
|---|---|---|:---:|:---:|
| **M1** | Antigravity | Codex | `1113294977` | **NEXT ACTION** |
| **M2** | Codex | Copilot | `3033283457` | PENDING M1 ANALYSIS |
| **M3** | Copilot | Antigravity | `3122977751` | PENDING M2 ANALYSIS |

### Pre-Declared Tie-Breaking Rule:
1. **Primary**: Number of match wins (W-L record).
2. **Tie-Break (if all 1–1)**: Aggregate signed final-money differential $D_i = \sum (\text{final\_money}_i - \text{final\_money}_{\text{opponent}})$.

---

## 4. Mandatory Post-M1 Analysis Protocol

Immediately after executing M1:
1. **Artifact Archival**: Verify output files in `results/e15/M1_antigravity_vs_codex/` (`match_metadata.json`, `summary.json`, `telemetry.json`, `raw_replay.json`).
2. **Neutral Analysis (ChatGPT)**: Perform independent forensic analysis comparing telemetry against the frozen `ONTOLOGY.md` and both participants' frozen `MODEL_SPEC.md`.
3. **Concept Verdict Classification**: Classify all discriminated canonical `concept_id`s using strictly permitted verdicts:
   - `SUPPORTED`
   - `WEAKENED`
   - `NOT_DISCRIMINATED`
   - `CONFOUNDED`
   - `INCONCLUSIVE`
4. **Independent Agent Feedback**: Collect independent feedback/challenges from Antigravity and Codex.
5. **Consensus Synthesis (ChatGPT)**: Consolidate findings and record post-match model updates.
6. **Authorization Gate**: Only after completing the post-M1 evaluation will Match M2 be authorized.

### Foundational Principles:
- **Victory $\neq$ Model Validity**: Global match victory does not validate all assumptions of a strategy.
- **Defeat $\neq$ Model Falsification**: A loss does not invalidate correct individual parametric hypotheses.
- **Observability Discipline**: Do not infer unobservable metrics from final score alone.
