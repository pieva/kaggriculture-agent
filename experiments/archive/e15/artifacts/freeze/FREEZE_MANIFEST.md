# E15.0 Pre-Match Freeze Manifest

- **Freeze Date**: 2026-08-29T08:51:30.670352+02:00
- **Git Branch**: main
- **Last Commit**: 4445aa0 Close E08 productive scale experiment
- **Working Tree State**: DIRTY (Pre-E15 authoritative working tree state)
- **Integrity Status**: All 7 canonical artifacts frozen and verified via SHA256.

---

## 1. Frozen Artifacts Registry

| Artifact Name | Source Path | Frozen Path | SHA256 Checksum |
|---|---|---|---|
| Canonical Ontology | docs/model_specs/ONTOLOGY.md | experiments/archive/e15/artifacts/freeze/ONTOLOGY_E15_FROZEN.md | 5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa |
| Antigravity MODEL_SPEC | docs/model_specs/antigravity/MODEL_SPEC.md | experiments/archive/e15/artifacts/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md | f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46 |
| Codex MODEL_SPEC | docs/model_specs/codex/MODEL_SPEC.md | experiments/archive/e15/artifacts/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md | 9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7 |
| Copilot MODEL_SPEC | docs/model_specs/copilot/MODEL_SPEC.md | experiments/archive/e15/artifacts/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md | d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686 |
| Antigravity Submission Candidate | experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py | experiments/archive/e15/artifacts/freeze/submission_antigravity_E15_FROZEN.py | 629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d |
| Codex Submission Candidate | submission/submission_codex.py | experiments/archive/e15/artifacts/freeze/submission_codex_E15_FROZEN.py | fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3 |
| Copilot Submission Candidate | submission/submission_copilot.py | experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py | 604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb |

---

## 2. Freeze Governance & Integrity Notice

1. **Strict Immutability**: All frozen files in 
esults/e15/freeze/ represent the authoritative baseline for the E15 Pairwise Tournament (M1, M2, M3).
2. **Zero Modification Policy**: From this freeze point until the conclusion of Match 3, no MODEL_SPEC, strategy code, configuration, or submission candidate may be altered.
3. **Reproducibility Guarantee**: Any post-match replay or verdict evaluation must reference these exact SHA256 hashes to guarantee provenance.
