# KAGGLE MANIFEST — ANTIGRAVITY MODEL_SPEC C2

- **AGENT_ID:** `antigravity`
- **Submission Name:** `submission_antigravity.py`
- **Submission Path:** `submission/submission_antigravity.py`
- **MODEL_SPEC Version:** `2.1.0`
- **Date:** 2026-08-31
- **Status:** `KAGGLE_READY: YES` | `KAGGLE_SUBMITTED: NO`

---

## 1. Submission Artifact Specification

- **File Path:** `submission/submission_antigravity.py`
- **File Size:** ~16 KB (completamente standalone, zero overhead)
- **Top-Level Callable Entrypoint:** `agent(observation, configuration=None) -> dict`
- **Self-Contained Dependencies:** Usa esclusivamente librerie standard Python (`dataclasses`, `math`, `typing`, `collections`) compatibili con l'ambiente Kaggle.
- **Act Timeout Constraint:** Tempo medio di decisione per step $< 1.5\text{ ms}$ (limite Kaggle standard: $1,000\text{ ms}$).

---

## 2. Build and Validation Commands

### 2.1 Build Command
```powershell
.venv\Scripts\python.exe scripts/build_submission_antigravity.py
```

### 2.2 Local Behavioral Validation Command
```powershell
.venv\Scripts\python.exe scripts/verify_antigravity_submission.py
```

**Esito:** 100% Exact Step-by-Step Action Equivalence su 3 seed da 720 step (2,160 step verificati senza alcuna discrepanza). Mean Final Money: **$43,837.33** (+50.58% rispetto a v2.0.0).

---

## 3. Local Import and Smoke Test

```python
import importlib.util

spec = importlib.util.spec_from_file_location("submission_antigravity", "submission/submission_antigravity.py")
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

> **NOTA DI GOVERNANCE:** In conformità con la Sezione 14 del Mandato C2, la submission **NON è stata inviata a Kaggle**. L'invio formale avverrà unicamente a valle del tournament e della relativa autorizzazione formale di gate.
