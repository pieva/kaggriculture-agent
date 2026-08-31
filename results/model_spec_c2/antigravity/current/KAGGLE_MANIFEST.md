# KAGGLE MANIFEST — ANTIGRAVITY MODEL_SPEC C2 (75K DUAL-QUADRANT)

- **AGENT_ID:** `antigravity`
- **Submission Name:** `submission_antigravity_75k.py`
- **Submission Path:** `submission/submission_antigravity_75k.py` (e `submission/submission.py`)
- **MODEL_SPEC Version:** `ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0`
- **Date:** 2026-08-31
- **Status:** `KAGGLE_READY: YES` | `KAGGLE_SUBMITTED: NO`

---

## 1. Submission Artifact Specification

- **File Path:** `submission/submission_antigravity_75k.py` & `submission/submission.py`
- **File Size:** ~173 KB (completamente standalone, monolitico)
- **Top-Level Callable Entrypoint:** `agent(observation, configuration=None) -> dict`
- **Self-Contained Dependencies:** Usa esclusivamente librerie standard Python (`dataclasses`, `math`, `typing`, `collections`, `statistics`, `json`, `hashlib`).
- **Act Timeout Constraint:** Tempo medio di decisione per step $< 5.0\text{ ms}$ (limite Kaggle standard: $1,000\text{ ms}$).

---

## 2. Build and Validation Commands

### 2.1 Build Command
```powershell
.venv\Scripts\python.exe scripts/build_submission_antigravity_75k.py --submission-py
```

### 2.2 Local Behavioral Validation Command
```powershell
.venv\Scripts\python.exe scripts/verify_antigravity_75k_submission.py
```

**Esito:** 100% Exact Step-by-Step Action Equivalence su 3 seed da 120 step (100% Bit-Exact Match). Mean Final Net Money: **$60,437.17** (Phase B) / **$63,811.17** (Phase C), Picco max **$72,695.00**, 0 fughe animali, 0 hard misses.

---

## 3. Local Import and Smoke Test

```python
import importlib.util

spec = importlib.util.spec_from_file_location("submission_antigravity_75k", "submission/submission_antigravity_75k.py")
sub_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sub_module)

assert hasattr(sub_module, "agent")
assert callable(sub_module.agent)
```
**Esito:** Caricamento riuscito in memoria isolata senza errori né side effect.

---

## 4. Kaggle Submission Readiness Gate

```text
KAGGLE_MANIFEST: READY
KAGGLE_ARTIFACT_READY: YES
KAGGLE_LOCAL_VALIDATION_PASS: YES
KAGGLE_NO_FORBIDDEN_DEPS: YES
KAGGLE_NO_LOCAL_PATHS: YES
KAGGLE_TIMEOUT_COMPLIANT: YES

KAGGLE_READY: YES
KAGGLE_SUBMITTED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
