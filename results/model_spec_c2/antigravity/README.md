# ANTIGRAVITY C2 — CANONICAL RESULTS & EVIDENCE INDEX

```text
MODULE: results/model_spec_c2/antigravity
LAST_UPDATED: 2026-08-31
FOUNDATION_CHECKPOINT: f391ee2
FOUNDATION_LAYERS_1_5_FROZEN: YES
```

Questo documento costituisce l'**indice canonico e unificato** di tutti i risultati sperimentali, verifiche forensi e manifest di submission per l'agente **Antigravity C2**.

---

## 1. Architettura della Directory

```text
results/model_spec_c2/antigravity/
├── README.md                      # Indice canonico delle evidenze (questo file)
├── CLEANUP_REPORT.md              # Report di consolidamento e pulizia filesystem
├── current/                       # Stato corrente, build verification e manifest
│   ├── BUILD_VERIFICATION.md      # Smoke test e build verification locale (v2.1.0)
│   ├── KAGGLE_MANIFEST.md         # Manifest submission Kaggle
│   └── TOURNAMENT_MANIFEST.md     # Manifest tournament locale
├── evidence/                      # Evidenze causali, ablazioni e benchmark audit
│   ├── LIVESTOCK_ABLATION.md      # Ablazione controllata same-tile (A: Pure Horti vs B: Livestock 2+2)
│   ├── LIVESTOCK_ABLATION_RESULTS.csv
│   ├── SAME_TILE_CROP_INTEGRITY.md # Verifica integrità crop same-tile (C vs A: +$1,148 gain)
│   ├── SAME_TILE_CROP_INTEGRITY.csv
│   ├── LUCCC_PRODUCTION_AUDIT.md  # Audit forense replay LuCcc 103484828 ($56,772 score)
│   ├── LUCCC_PRODUCTION_AUDIT.csv
│   ├── Q0_3X3_FORENSIC_GAP_ANALYSIS.md # Analisi del gap 56.8k vs 38.0k (dimostrazione crop serviceability)
│   ├── Q0_3X3_FORENSIC_GAP_ANALYSIS.csv
│   ├── POST_TOURNAMENT_FAILURE_REVIEW.md # Analisi storica failure post-tournament Round 2
│   └── EXTERNAL_DIAGNOSTIC_RUN.md # Diagnostica benchmark esterno
└── experiments/                   # Serie sperimentale iterativa
    ├── Q0_2PLUS2/                 # Test comparativo Q0 vs Q0+Q1 2+2 ($24,646 vs $6,334)
    │   ├── LUCCC_STYLE_Q0_Q1_2PLUS2_LOCAL_TEST.md
    │   └── LUCCC_STYLE_Q0_Q1_2PLUS2_LOCAL_RESULTS.csv
    ├── Q0_3X3/                    # Replica esatta architettura LuCcc Q0 3 COW + 3 SHEEP ($37,997.67)
    │   ├── LUCCC_EXACT_Q0_3COW_3SHEEP_REPLICATION.md
    │   └── LUCCC_EXACT_Q0_3COW_3SHEEP_RESULTS.csv
    └── ROUTINE_PLANNING/          # Ottimizzazione causale worker routing & zoning ($39,695.33)
        ├── Q0_3X3_ROUTINE_WORKER_PLANNING_TEST.md
        └── Q0_3X3_ROUTINE_WORKER_PLANNING_RESULTS.csv
```

---

## 2. Sintesi delle Evidenze e Numeri Canonici

| Esperimento / Evidenza | Path Relativo | Final Money (Mean) | Status | Esito / Conclusione Chiave |
|---|---|---:|---|---|
| **Pure Horticulture Baseline (2Q)** | `current/BUILD_VERIFICATION.md` | **$43,837.33** | `CANONICAL` | Baseline orticola pura su 40 tile (10 braccianti, 0 animali, $1k spesi in terra). |
| **Livestock Controlled Ablation** | `evidence/LIVESTOCK_ABLATION.md` | **$21,556.00** | `EVIDENCE` | Variant B (2+2 su Q0+Q1) perde -$22.2k rispetto a Pure Horti per dispersione manodopera su 40 tile. |
| **Same-Tile Crop Integrity** | `evidence/SAME_TILE_CROP_INTEGRITY.md` | **$44,985.67** | `EVIDENCE` | Dimostrato che Variant C (38 tile pure) supera Variant A (40 tile) di +$1,148.34 grazie alla concentrazione dei 10 worker. |
| **LuCcc Production Audit** | `evidence/LUCCC_PRODUCTION_AUDIT.md` | **$56,772.00** | `BENCHMARK` | Forensic del replay `103484828`: Q0-only ($0 terra), 7 worker, 3 COW + 3 SHEEP, 18 crop, $35.9k revenue livestock (63%). |
| **Q0 2+2 vs Q0+Q1 Local Test** | `experiments/Q0_2PLUS2/` | **$24,646.67** | `SUPERSEDED` | H1 (Q0 2+2) = $24.6k vs H2 (Q0+Q1 2+2) = $6.3k. Prova che l'espansione territoriale tardiva con animali fallisce. |
| **Q0 3+3 Exact Replication** | `experiments/Q0_3X3/` | **$37,997.67** | `SUPERSEDED` | Replica esatta 6 animali + 18 crop. Guadagno di +$13.3k rispetto a 2+2. Picco $42,455 su seed 1838889274. |
| **Q0 3+3 Forensic Gap Analysis** | `evidence/Q0_3X3_FORENSIC_GAP_ANALYSIS.md`| — | `CANONICAL` | Riconciliato il gap di $18.8k: prezzi/timing AG superiori a LuCcc; il gap è 100% da congestione worker orticola (24.7 vs 120 crop units). |
| **Routine Worker Planning** | `experiments/ROUTINE_PLANNING/` | **$39,695.33** | `CURRENT` | Routing a zone fisse e ruoli stabili sblocca la produzione: crop units da 24.7 a 85.33 (**63.62% gap recovery**), varianza ridotta del 63.1%. |

---

## 3. Riepilogo Causale dell'Evoluzione Antigravity C2

1. **Il Dilemma Territoriale Risolto:** L'acquisizione di Q1 per il livestock è subottimale se non supportata da densità immediata; LuCcc vince comprimendo 6 animali e 18 colture su Q0 a costo terra zero ($0.00).
2. **Validità Strutturale del Modello 3+3:** L'architettura 3 COW + 3 SHEEP su Q0 è stata provata come strutturalmente valida (produce oltre $39k lordi da animali con 0 fughe).
3. **Risoluzione del Collo di Bottiglia Operativo:** La causa della perdita orticola non era la configurazione ma il routing non deterministico. L'introduzione del **Routine Worker Planner** (ruoli stabili + zone orticole da 6 tile) ha triplicato la produzione di meloni e fragole (da 24.7 a 85.33 unità), portando la media a **$39,695.33** e ponendo le basi per l'espansione scalata su Q0+Q1.
