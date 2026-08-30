# Project State

**Last update:** 2026-08-30
**Current phase:** `MODEL_SPEC C2 — PERFORMANCE TOURNAMENT COMPLETED / SHIP READY / KAGGLE VALIDATION PENDING`
**Repository Test Suite:** `182 passed`
**Repository Hygiene:** `git diff --check PASS`

---

## 1. Current Phase Summary

```text
Current phase:
MODEL_SPEC C2 — PERFORMANCE TOURNAMENT COMPLETED / SHIP READY

Gate & Results:
C2_PERFORMANCE_SUCCESS: YES
Codex C2 V4:       Mean Final Money $31,579.50 | 6W-0L-0T (Primary Candidate)
Antigravity C2:    Mean Final Money $27,565.17 | 3W-3L-0T
Copilot C2:        Mean Final Money  $7,823.67 | 0W-6L-0T
Economic Threshold: max(Candidate Mean) = $31,579.50 > $23,000.00 (EXCEEDED)

Submission SHIP Artifacts:
submission/submission_codex.py       — CERTIFIED STANDALONE (100% Behavioral Equivalence on tournament seeds)
submission/submission_antigravity.py — CERTIFIED STANDALONE (100% Behavioral Equivalence on tournament seeds)

Repository validation:
182 passed
git diff --check PASS

Kaggle validation:
PENDING (No unobservable external scores declared)

Next Action:
External Kaggle validation & post-C2 Foundation consolidation (State machine update pending future milestone).
```

---

## 2. Tournament & Performance Summary

The **C2 Common Performance Tournament** was executed across 9 pairwise matches (18 player-episodes, 6,480 steps total) on 3 newly generated and frozen primary seeds (`1838889274`, `1619968655`, `710418712`).

### 2.1 Official Ranking

| Rank | Candidate | Record | Mean Final Money | Median Final Money | Std (`ddof=1`) | Min Final Money | Max Final Money | Delta vs Prior C2 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Codex C2 V4** | **6W-0L-0T** | **$31,579.50** | **$31,130.50** | $3,705.61 | $27,724.00 | $37,165.00 | **+$16,423.50 (+108.36%)** |
| **2** | **Antigravity C2** | **3W-3L-0T** | **$27,565.17** | **$27,726.00** | $3,092.40 | $23,545.00 | $30,563.00 | **+$10,894.17 (+65.35%)** |
| **3** | **Copilot C2** | **0W-6L-0T** | **$7,823.67** | **$7,742.00** | $287.78 | $7,582.00 | $8.369.00 | **+$3,669.67 (+88.34%)** |

### 2.2 Descriptions
- `C2 Codex V4 — Performance Iteration — Mean $31.6k local tournament`
- `C2 Antigravity — Performance Iteration — Mean $27.6k local tournament`

---

## 3. Core Lesson Learned

> **Principal Scientific Finding (C2):**
> `ACTIVE_SURFACE` o peak tile count non sono sufficienti a spiegare la performance. La capacità produttiva deve essere convertita lungo la catena causale:
> $$\text{SERVICEABLE\_SURFACE} \longrightarrow \text{PRODUCTIVE\_SURFACE} \longrightarrow \text{MONETIZED\_OUTPUT}$$
> Codex V4 ha inoltre dimostrato causalmente che la sincronizzazione temporale delle maturity (burst PLANT) può creare `SERVICE_PEAK` e `HARVEST_DEADLINE` che superano la capacità logistica on-time e riducono la resa (decay), mentre il **plant staggering** (es. `MAX_WHEAT_PLANTS_PER_DAY=2`) elimina il collo di bottiglia e massimizza la conversione a yield pieno.

---

## 4. Standalone Submission Artifacts (SHIP)

| Submission Artifact | Backing Frozen Candidate | SHA256 | Behavioral Equivalence | Smoke Test |
| :--- | :--- | :--- | :---: | :---: |
| `submission/submission_codex.py` | `src/agricola/strategy/codex_c2.py` | `b9e9f2bdcd8b...` | **100% PASS (720/720 steps on all 3 seeds)** | **PASS** |
| `submission/submission_antigravity.py` | `src/agricola/strategy/antigravity/` | `0aa3764cf7ad...` | **100% PASS (720/720 steps on all 3 seeds)** | **PASS** |

---

## 5. Next Steps

1. Execute external Kaggle validation according to platform availability.
2. Consolidate C2 empirical findings and lifecycle state mechanics into the Model Foundation (`ONTOLOGY_C2`, `KAGGRICULTURE_STATE_MACHINE_C2`, `KAGGRICULTURE_FEATURE_MODEL_C2`) during the dedicated Foundation consolidation phase.
