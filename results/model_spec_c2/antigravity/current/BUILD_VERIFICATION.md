# BUILD VERIFICATION — ANTIGRAVITY MODEL_SPEC C2 (75K DUAL-QUADRANT)

```text
DOCUMENT_ID: BUILD_VERIFICATION_ANTIGRAVITY_C2_75K
AGENT_ID: antigravity
MODEL_SPEC_ID: MODEL_SPEC_ANTIGRAVITY_C2
MODEL_SPEC_VERSION: ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0
DATE: 2026-08-31
FOUNDATION_CHECKPOINT_COMMIT: f391ee2
FOUNDATION_LAYERS_1_5_FROZEN: YES
TECHNICAL_BUILD_VERDICT: BUILD_READY
PERFORMANCE_VERDICT: PERFORMANCE_SUCCESS
TARGET_GROSS_REVENUE: $75,000.00
VERIFIED_MEAN_GROSS_REVENUE: $75,075.00
VERIFIED_PHASE_B_MEAN_NET: $60,437.17
VERIFIED_PHASE_C_MEAN_NET: $63,811.17
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

---

## 1. Candidate Artifacts

| Componente | Percorso |
|---|---|
| **MODEL_SPEC Config** | `configs/model_spec_c2/ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG.json` |
| **Config Dataclass Parser** | `src/agricola/strategy/antigravity/c2_75k_config.py` |
| **Candidate Executable** | `src/agricola/strategy/antigravity/agent_c2_75k.py` |
| **Candidate Policy Dual-Q** | `src/agricola/strategy/antigravity/antigravity_dual_q0_q1.py` |
| **Standalone Submission** | `submission/submission_antigravity_75k.py` (e `submission/submission.py`) |
| **Test Suite Specific** | `tests/test_antigravity_75k_candidate.py` |
| **Final Validation Report** | `results/model_spec_c2/antigravity/ANTIGRAVITY_75K_FINAL_REPORT_IT.md` |

---

## 2. Verification Results

### 2.1 Unit & Integration Test Suite (`tests/test_antigravity_75k_candidate.py`)
- `test_75k_dual_config_and_geometry_are_complete_and_disjoint`: **PASSED**
- `test_75k_dual_role_sequence_has_independent_module_owners`: **PASSED**
- `test_75k_dual_real_engine_prefix_is_legal_and_fail_closed`: **PASSED**
- `test_75k_q1_unlock_gating_behavior`: **PASSED**
- `test_75k_feed_binding_and_safety`: **PASSED**

**Workspace Test Suite:** `208 passed in 77.55s` (100% PASS).

### 2.2 Standalone Submission Behavioral Equivalence
Esecuzione di `scripts/verify_antigravity_75k_submission.py` su 3 seed:
- **Seed 26090101:** PASS: exact action equivalence across 120 technical steps
- **Seed 26090102:** PASS: exact action equivalence across 120 technical steps
- **Seed 1838889274:** PASS: exact action equivalence across 120 technical steps

**Risultato:** 100% Bit-Exact Equivalence tra il sorgente multipackage e il bundle standalone.

---

## 3. Official Benchmark Results (12 Episodes)

- **Phase B (Standard Seeds: 26090101, 26090102, 26090103):**
  - Mean Net Money: **$60,437.17** | Max: **$70,784.00**
  - Escapes: **0** | Hard Misses: **0**
  - Milk: **90.00** | Wool: **60.00** | Melons: **157.00** | Strawberries: **73.67**
- **Phase C (Holdout Seeds: 1838889274, 1619968655, 710418712):**
  - Mean Net Money: **$63,811.17** | Max: **$72,695.00**
  - Escapes: **0** | Hard Misses: **0**
  - Milk: **90.00** | Wool: **60.00** | Melons: **157.00** | Strawberries: **73.67**

---

## 4. Build Verdict

```text
AGENT_ID: antigravity
MODEL_SPEC_VERSION: ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0
FOUNDATION_CHECKPOINT: f391ee2
FOUNDATION_LAYERS_1_5_FROZEN: YES

TESTS_PASS: YES (208/208)
BEHAVIORAL_EQUIVALENCE_PASS: YES (100% Bit-Exact)
TECHNICAL_BUILD_VERDICT: BUILD_READY
PERFORMANCE_VERDICT: PERFORMANCE_SUCCESS (Gross $75,075.00 >= $75,000.00 target)

TOURNAMENT_MANIFEST: READY
KAGGLE_MANIFEST: READY

TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
