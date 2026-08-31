# BUILD VERIFICATION — ANTIGRAVITY MODEL_SPEC C2

```text
DOCUMENT_ID: BUILD_VERIFICATION_ANTIGRAVITY_C2
AGENT_ID: antigravity
MODEL_SPEC_ID: MODEL_SPEC_ANTIGRAVITY_C2
MODEL_SPEC_VERSION: 2.1.0
DATE: 2026-08-31
FOUNDATION_CHECKPOINT_COMMIT: f391ee2
FOUNDATION_LAYERS_1_5_FROZEN: YES
TECHNICAL_BUILD_VERDICT: BUILD_READY
PERFORMANCE_VERDICT: PERFORMANCE_FAILURE
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

---

## 1. Candidate Artifacts

| Componente | Percorso |
|---|---|
| **MODEL_SPEC C2** | `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md` |
| **Candidate Executable** | `src/agricola/strategy/antigravity/agent_c2.py` |
| **Candidate Policy** | `src/agricola/strategy/antigravity/c2_policy.py` |
| **Candidate Config** | `src/agricola/strategy/antigravity/c2_config.py` |
| **Package Exports** | `src/agricola/strategy/antigravity/__init__.py` |
| **Standalone Submission** | `submission/submission_antigravity.py` |
| **Test Suite Specific** | `tests/test_antigravity_c2.py` |

---

## 2. Verification Results

### 2.1 Unit & Integration Test Suite (`tests/test_antigravity_c2.py`)
Esecuzione tramite `.venv\Scripts\python.exe -m pytest tests/test_antigravity_c2.py -v`:
- `test_antigravity_c2_harvest_readiness_rejection_and_acceptance`: **PASSED**
- `test_antigravity_c2_tile_lifecycle_classification`: **PASSED**
- `test_antigravity_c2_recovery_and_preventive_dig_dispatch`: **PASSED**
- `test_antigravity_c2_no_premature_harvest_dispatch`: **PASSED**
- `test_antigravity_c2_agent_callable_interface`: **PASSED**
- `test_antigravity_c2_player1_support`: **PASSED**
- `test_antigravity_c2_real_engine_smoke_48_steps`: **PASSED**
- `test_antigravity_c2_expanded_footprint_and_crop_plan`: **PASSED**
- `test_antigravity_c2_late_planting_biological_cutoff`: **PASSED**

**Risultato:** `9 passed in 3.53s` (100% PASS).

### 2.2 Standalone Submission Behavioral Equivalence
Esecuzione di `scripts/verify_antigravity_submission.py` su 3 simulazioni complete da 720 step:
- **Seed 1838889274:** Exact Step-by-Step Equivalence! Final Money: **$41,548.00**
- **Seed 1619968655:** Exact Step-by-Step Equivalence! Final Money: **$44,698.00**
- **Seed 710418712:** Exact Step-by-Step Equivalence! Final Money: **$45,266.00**

**Risultato:** 100% Step-by-step match tra il sorgente `AntigravityC2Agent` e `submission/submission_antigravity.py` (2,160/2,160 step identici).
- **Mean Final Money:** **$43,837.33** (Baseline v2.0.0: $29,112.33, $\Delta = +\$14,725.00$ / $+50.58\%$)
- **Median Final Money:** **$44,698.00**
- **Standard Deviation:** **$2,002.32**

### 2.3 Determinism and Packaging Verification
- **Determinismo:** Verificato; 0 differenze comportamentali a parità di osservazione e seed;
- **Packaging:** Standalone bundle `submission/submission_antigravity.py` autocontenuto, privo di import non standard o dipendenze da file system locale.

---

## 3. Conformance and Quality Invariants

- **Zero Unhandled Exceptions:** Nessun crash interno, timeout o fallback a `PASS` forzato;
- **Zero Invalid Actions:** Azioni emesse sempre legalmente conformi allo schema `kaggriculture`;
- **Multiplayer Index Independence:** Validata la corretta esecuzione sia come Player 0 che come Player 1;
- **Zero Future Leakage:** Tutte le decisioni sono rigorosamente basate sulle osservazioni disponibili al decision time;
- **No Silent Replan:** Piena conformità al Decision Lifecycle Contract C2.

---

## 4. Known Limitations

- Il footprint a 2 quadranti (40 tile) raggiunge \$43.8k, migliorando del +50.6% la baseline, ma resta sotto la soglia di \$50,000 per l'approvazione economica piena;
- L'espansione a 4 quadranti (60–80 tile) richiede una revisione algoritmica di zonizzazione / routing per superare l'overhead di transito e il vincolo dei salari prima del giorno 11;
- Strategia Livestock azzerata (scelta deliberata supportata da ablazione economica E08).

---

## 5. Build Verdict

```text
AGENT_ID: antigravity
MODEL_SPEC_VERSION: 2.1.0
FOUNDATION_CHECKPOINT: f391ee2
FOUNDATION_LAYERS_1_5_FROZEN: YES

TESTS_PASS: YES (9/9)
BEHAVIORAL_EQUIVALENCE_PASS: YES (2160/2160 steps)
TECHNICAL_BUILD_VERDICT: BUILD_READY
PERFORMANCE_VERDICT: PERFORMANCE_FAILURE (Mean $43,837.33 < $50,000 threshold)

TOURNAMENT_MANIFEST: READY
KAGGLE_MANIFEST: READY

TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
