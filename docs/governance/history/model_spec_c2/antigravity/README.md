# Indice artefatti Antigravity C2

Questa directory contiene esclusivamente la baseline Antigravity V4 corrente
e la relativa evidenza finale. Le linee transitorie 50K, 75K, 90K, 100K e
150K sono state rimosse dopo la chiusura della Foundation C2.1.

## ACTIVE

- `ANTIGRAVITY_V4_0_FINAL_REPORT_IT.md`: report finale V4;
- `ANTIGRAVITY_V4_0_RESULTS.json` / `.csv`: suite canonica;
- `ANTIGRAVITY_V4_0_HOLDOUT_RESULTS.json` / `.csv`: holdout;
- `ANTIGRAVITY_V4_0_THREE_WAY_TOURNAMENT_RESULTS.json` / `.csv`: torneo V4;
- `freeze/submission_antigravity_v4_tournament.py`: standalone V4 congelata.

## Implementazione corrente

- source: `src/agricola/strategy/antigravity/antigravity_3q_high_density_v4.py`;
- entry point: `src/agricola/strategy/antigravity/agent_c2_3q_v4.py`;
- config: `docs/model_specs/antigravity/configs/ANTIGRAVITY_C2_V4_0_3Q_HIGH_DENSITY_CONFIG.json`;
- MODEL_SPEC: `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md`;
- builder: `scripts/build_submission_antigravity_v4.py`;
- benchmark: `scripts/benchmark_antigravity_v4_3q.py`;
- submission canonica: `experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py`.

La submission canonica e la freeze sono byte-identiche, con SHA-256
`5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872`.
La V4 resta una baseline derivativa perché riusa la routine Codex: non supera
il gate di indipendenza strategica e non va presentata come modello autonomo.
