# ANTIGRAVITY C2 — CANONICAL RESULTS & EVIDENCE INDEX

```text
MODULE: results/model_spec_c2/antigravity
LAST_UPDATED: 2026-08-31
FOUNDATION_CHECKPOINT: f391ee2
FOUNDATION_LAYERS_1_5_FROZEN: YES
ACTIVE_CANDIDATE: ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0
```

Questo documento costituisce l'**indice canonico e unificato** di tutti i risultati sperimentali, verifiche forensi, benchmark e manifest di submission per l'agente **Antigravity C2**.

---

## 1. Architettura della Directory

```text
results/model_spec_c2/antigravity/
├── README.md                      # Indice canonico delle evidenze (questo file)
├── SUBMISSION_DESCRIPTION.md      # Scheda tecnica dettagliata della release 75K
├── ANTIGRAVITY_75K_FINAL_REPORT_IT.md # Report formale di validazione a 16 sezioni (75K)
├── ANTIGRAVITY_75K_DUAL_Q_BUILD_PROMPT_IT.md # Prompt formale di ingegnerizzazione (75K)
├── ANTIGRAVITY_75K_RESULTS.csv / .json # Dati grezzi benchmark Phase B (75K)
├── ANTIGRAVITY_75K_PHASE_C_RESULTS.csv / .json # Dati grezzi benchmark Phase C (75K)
├── ANTIGRAVITY_50K_FINAL_REPORT_IT.md # Report storico baseline Q0 compatto (50K)
├── CLEANUP_REPORT.md              # Report storico di consolidamento e pulizia
├── current/                       # Stato corrente, build verification e manifest
│   ├── BUILD_VERIFICATION.md      # Certificazione build e benchmark (75K)
│   ├── KAGGLE_MANIFEST.md         # Manifest submission Kaggle (75K)
│   └── TOURNAMENT_MANIFEST.md     # Manifest tournament locale
├── evidence/                      # Evidenze causali, ablazioni e benchmark audit
│   ├── LIVESTOCK_ABLATION.md      # Ablazione controllata same-tile
│   ├── LUCCC_PRODUCTION_AUDIT.md  # Audit forense replay LuCcc 103484828 ($56,772 score)
│   ├── Q0_3X3_FORENSIC_GAP_ANALYSIS.md # Analisi del gap di serviceability
│   └── POST_TOURNAMENT_FAILURE_REVIEW.md
└── experiments/                   # Serie sperimentale iterativa
    ├── Q0_2PLUS2/                 # Test comparativo Q0 vs Q0+Q1 2+2
    ├── Q0_3X3/                    # Replica architettura LuCcc Q0 3+3
    └── ROUTINE_PLANNING/          # Routine worker planner e zoning
```

---

## 2. Sintesi delle Evidenze e Numeri Canonici

| Candidato / Evidenza | Target / Modulo | Net Money (Phase B) | Net Money (Phase C) | Gross Revenue | Escapes | Status |
|---|---|---:|---:|---:|:---:|---|
| **Antigravity C2 Dual-Q 75K** | **Q0+Q1 (13 Hands)** | **$60,437.17** | **$63,811.17** | **$75,075.00** | **0** | `ACTIVE_RELEASE` |
| **Antigravity C2 Compact 50K**| Q0 (7 Hands) | $56,386.50 | $57,756.33 | $37,537.50 | 0 | `SUPERSEDED_BASELINE` |
| **LuCcc Production Benchmark**| Q0 (7 Hands) | — | $56,772.00 | — | 0 | `EXTERNAL_BENCHMARK` |
| **Pure Horticulture (2Q)** | Q0+Q1 (10 Hands) | — | $43,837.33 | — | 0 | `HISTORICAL_ABLATION` |

---

## 3. Evoluzione Strategica Antigravity C2

1. **Raggiungimento Target 75K**: Con l'espansione coordinata a 13 ruoli e gating di liquidità, la produzione ha raggiunto il 100% dell'output massimo teorico zootecnico (90 latte, 60 lana) e il doppio esatto della resa orticola (157 meloni, 74 fragole), superando il target economico con **\$75,075.00** di fatturato lordo.
2. **Sicurezza Assoluta**: 0 fughe animali (`ANIMAL_ESCAPE = 0`) e 0 scadenze mancate (`HARD_DEADLINE_MISSES = 0`) su tutti i seed testati.
3. **Parità Standalone**: Il file `submission/submission_antigravity_75k.py` e il canonico `submission/submission.py` garantiscono parità comportamentale bit-exact al 100% rispetto al codice sorgente multipackage.
