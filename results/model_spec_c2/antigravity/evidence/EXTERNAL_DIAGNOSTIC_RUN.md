# EXTERNAL DIAGNOSTIC RUN — ANTIGRAVITY C2 LIVESTOCK VARIANT (LS1)

```text
DOCUMENT_ID: EXTERNAL_DIAGNOSTIC_RUN_ANTIGRAVITY_LS1
VARIANT_ID: ANTIGRAVITY_C2_V2.1.0_LS1
BASELINE_VARIANT: ANTIGRAVITY_C2_V2.1.0_PURE
DATE: 2026-08-31
PURPOSE: EXTERNAL_DIAGNOSTIC_ABLATION
```

---

## 1. Controlled Diagnostic Framework

L'esperimento controllato pone a confronto due modelli con identica base algoritmica:
- **Variante A (Pure Horticulture):** `Antigravity C2 v2.1.0` (40 tile arabili, 0 livestock, \$43,837.33);
- **Variante B (Centered Livestock Hybrid LS1):** `Antigravity C2 v2.1.0-LS1` (38 tile arabili, 2 pascoli COW centrati a `(3,4)` e `(6,4)` adiacenti allo shed a Day 11, \$38,059.00).

---

## 2. Local Paired Metrics (3 Canon Seeds: 1838889274, 1619968655, 710418712)

| Metrica | Pure Horticulture (v2.1.0) | Centered Livestock (v2.1.0-LS1) | Delta Assoluto | Delta % |
|---|---|---|---|---|
| **Seed 1838889274** | \$41,548.00 | \$38,603.00 | -\$2,945.00 | -7.09% |
| **Seed 1619968655** | \$44,698.00 | \$37,870.00 | -\$6,828.00 | -15.28% |
| **Seed 710418712** | \$45,266.00 | \$37,704.00 | -\$7,562.00 | -16.71% |
| **Mean Final Money** | **$43,837.33** | **$38,059.00** | **-$5,778.33** | **-13.18%** |
| **Median Final Money** | **$44,698.00** | **$37,870.00** | -\$6,828.00 | -15.28% |
| **Standard Deviation** | \$2,002.32 | \$478.43 | — | — |
| **Escaped Animals** | 0 (N/A) | **0 (Zero fughe)** | — | — |
| **Feed Transit Distance** | N/A | **1 step (Central Shed Corridor)** | — | — |
| **Feed (Wheat) Consumed** | 0 | **36 unità** | +36 unità | — |
| **Milk Produced & Sold** | 0 | **22 unità** (~$3,520 lordo) | +22 unità | — |

---

## 3. Kaggle External Submission Record

- **Submission Artifact:** `submission/submission_antigravity_livestock.py`
- **Bundle SHA256:** `ea86afe02062c073346801b3df8d311e3bdbe31db2d1444a2d45e9d894dd7014`
- **Submission Message:** `C2 Antigravity v2.1 LS1 - 2 COW centered diagnostic`
- **Authorized:** `YES` (1 submission autorizzata per scopo diagnostico)
- **External Evaluation Status:** `SUBMISSION_READY / PENDING_EXTERNAL_RUN`
