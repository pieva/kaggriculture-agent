# MODEL_SPEC_ANTIGRAVITY_C2_LIVESTOCK — Antigravity C2 Diagnostic Hybrid Livestock Model

```text
MODEL_SPEC_ID: MODEL_SPEC_ANTIGRAVITY_C2_LIVESTOCK
AGENT_ID: antigravity_livestock
VERSION: 2.1.0-LS1
DATE: 2026-08-31
STATUS: DIAGNOSTIC VARIANT — 2 COW CENTERED HYBRID (EXTERNAL EVALUATION)
FOUNDATION_VERSION: C2 (f391ee2)
PARENT_MODEL_SPEC: MODEL_SPEC_ANTIGRAVITY_C2 (v2.1.0)
PURPOSE: EXTERNAL_DIAGNOSTIC_ABLATION
```

---

## 1. Intent and Scope

Questa specifica definisce la **variante diagnostica con modulo zootecnico centrato (`LS1`)** di Antigravity C2.
I pascoli sono posizionati **immediatamente adiacenti allo shed centrale** a coordinate `(3, 4)` e `(6, 4)` (distanza Manhattan = 1 step dallo shed), azzerando l'overhead di transito e riducendo il tempo di alimentazione e raccolta a 1 step.

> **Nota di Isolamento:** Questa variante NON modifica e NON sovrascrive la baseline `MODEL_SPEC_ANTIGRAVITY_C2` (Pure Horticulture v2.1.0, \$43,837.33).

---

## 2. Foundation Conformance & Livestock Invariants

In piena conformità con i Layer 1–5 congelati al commit `f391ee2`:
1. **Specie Zootecniche Valide:** `COW` (2 capi);
2. **Modulo Diagnostic Centered LS1:** 2 `COW` collocate in pascoli centrati `(3, 4)` e `(6, 4)` (adiacenti allo shed `(4,4)` e `(5,4)`);
3. **Consumo Feed:** `FEED` consuma esattamente 1 `WHEAT` dall'inventario del bracciante;
4. **Transit Efficiency:** Distanza di foraggiamento pari a 1 step dal magazzino centrale;
5. **Escape Prevention:** **0 fughe** verificate su tutte le simulazioni (100% feed compliance);
6. **Monetizzazione:** Raccolta automatica del `MILK` (fino a 6 unità max held) e vendita immediata a mercato.

---

## 3. Parametric Configuration

```python
AntigravityC2LivestockConfig(
    quadrants_owned=2,
    crop_working_set_target=38,
    pasture_allocation_target=2,
    livestock_headcount_target=2,
    livestock_species="COW",
    livestock_activation_day=11,
    workforce_headcount=10,
    operating_cash_floor=50.0,
    endgame_shutdown_steps=48,
    enable_strict_harvest_gate=True,
    enable_recovery_dig=True,
    enable_preventive_dig=True,
    enable_day0_water_priority=True,
    crop_mix_weights={"WHEAT": 0.20, "STRAWBERRY": 0.45, "MELON": 0.35},
)
```

---

## 4. Local Benchmark Performance (3 Canon Seeds)

| Metrica | Pure Horticulture (v2.1.0) | Centered Livestock (v2.1.0-LS1) | Delta vs Pure |
|---|---|---|---|
| **Mean Final Money** | **$43,837.33** | **$38,059.00** | -$5,778.33 (-13.18%) |
| **Median Final Money** | **$44,698.00** | **$37,870.00** | -$6,828.00 |
| **Standard Deviation (ddof=1)** | $2,002.32 | $478.43 | — |
| **Escaped Animals** | 0 (N/A) | **0 (100% Retained)** | — |
| **Pasture Transit Distance** | N/A | **1 step (Ultra-Compact)** | — |
| **Technical Build Verdict** | `BUILD_READY` | `BUILD_READY` | Identico |

---

## 5. Final Gate

```text
MODEL_SPEC_ID: MODEL_SPEC_ANTIGRAVITY_C2_LIVESTOCK
AGENT_ID: antigravity_livestock
VERSION: 2.1.0-LS1

FOUNDATION_CONFORMANCE: PASS
BUILD_STATUS: COMPLETE
TESTS_STATUS: PASS (5/5 Unit & Smoke Tests)
SUBMISSION_EQUIVALENCE: 100% CERTIFIED (2,160/2,160 steps)
KAGGLE_AUTHORIZED: YES
KAGGLE_PURPOSE: EXTERNAL_DIAGNOSTIC
```
