# E18 — Reactive 6-6-2 toward Top-3 behavior

## Status

```text
PHASE: OPEN / ENTRY_BASELINE_FROZEN
BASELINE: CODEX-E17.3-TOPOLOGY-FILL-662-V2
PLANNED_CANDIDATE: CODEX-E18.1-REACTIVE-662-V1
OBJECTIVE: OBSERVABLE_MARKET_AND_SERVICE_REGIME_SELECTION_WITH_662_INVARIANTS
TOP3_BENCHMARK: TETSUYA / OCEANMIX / CROP_DUSTA_HISTORICAL_REPLAY_ARCHETYPES
TARGET_MONEY: 100000
BASELINE_MONEY_VS_CLAUDE: 132217.68
BASELINE_MONEY_SYMMETRIC_662: 79323.86
BASELINE_SELFPLAY_GAP: 20676.14
BASELINE_REACTIVITY: FAIL_28_OF_28_ACTION_COUNT_PROFILES_IDENTICAL_V3_V2
BASELINE_SAFETY: 14_OF_14 / Q2_2 / ESCAPES_0 / BREACHES_0
HOLDOUT: NOT_CONSUMED / NOT_AUTHORIZED
FINAL_CONFIRMATION: NOT_CONSUMED / NOT_AUTHORIZED
NEXT_ACTION: IMPLEMENT_ACTIVATION_FIXTURES_BEFORE_POLICY_OPTIMIZATION
```

## Entry point

E18 conserva il layout 6-6-2 e apre una sola linea causale: rendere mercato e
servizio realmente dipendenti dallo stato. Il benchmark Top 3 è osservazionale
e usa replay già consumati come training evidence; non è un confronto
head-to-head con policy eseguibili.

Materiali iniziali:

- `design/E18_REACTIVE_662_TOP3_BENCHMARK_PLAN_V1.md`;
- `artifacts/baseline/E18_662_TOP3_BASELINE_BENCHMARK_V1.json`;
- `reports/common/E18_662_TOP3_BASELINE_BENCHMARK_IT.md`;
- `tools/common/build_e18_662_top3_baseline.py`;
- `tests/test_e18_662_top3_baseline.py`.

## Evidence boundary

- E17 development e Top-3 replay: training evidence riusata;
- E18 development: nuovo set preregistrato nel manifest E18;
- holdout/final: non consumati e non autorizzati;
- Kaggle: external validation successiva, non parte dell'entry benchmark.
