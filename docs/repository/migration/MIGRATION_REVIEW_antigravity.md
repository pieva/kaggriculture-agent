# MIGRATION REVIEW Antigravity

Data review: 2026-09-02
Ambito: A0 preflight/review read-only del file `docs/repository/migration/MIGRATION_INVENTORY_antigravity.csv`
Reviewer: Antigravity

## Input verificati

Lettura completata di:

- `experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md`
- `docs/model_specs/antigravity/README.md`
- `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md`
- `docs/repository/migration/MIGRATION_INVENTORY_antigravity.csv`

Stato worktree osservato durante la review:

- `README.md`, `docs/NEW_SESSION.md`, `docs/PROJECT_STATE.md` risultano `tracked_modified`
- diversi file `docs/benchmark/*.json` risultano `tracked_deleted`
- artefatti E17 e documenti di repository reorganization risultano presenti come `untracked`

## Sintesi inventario

- Righe CSV: `1035`
- Ownership `antigravity`: `98`
- Ownership `common`: `814`
- Ownership `codex`: `82`
- Ownership `copilot`: `41`
- Action `archive`: `800`
- Action `move`: `168`
- Action `keep`: `51`
- Action `candidate_delete`: `16`
- Tracked `clean`: `992`
- Tracked `modified`: `3`
- Tracked `deleted`: `5`
- `untracked`: `35`

Controllo collisioni:

- nessuna collisione rilevata su `proposed_destination` nel CSV reviewato

## Verifiche eseguite

### 1. Copertura dei documenti e artefatti obbligatori

Confermata la presenza nell’inventario dei path comuni richiesti per il fronte A / barriera A→B:

- `experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md`
- `docs/repository/REPOSITORY_ARCHITECTURE.md`
- `experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md`
- `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`
- `experiments/e17/reviews/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md`
- `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`

### 2. Verifica hash su campione significativo di file esistenti

Hash `SHA-256` confermati uguali al CSV per il seguente campione:

- `docs/model_specs/antigravity/configs/ANTIGRAVITY_C2_V4_0_3Q_HIGH_DENSITY_CONFIG.json`
- `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md`
- `docs/model_specs/antigravity/README.md`
- `docs/governance/foundation/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md`
- `docs/governance/foundation/antigravity/ANTIGRAVITY_FOUNDATION_EVIDENCE_MATRIX.csv`
- `experiments/archive/e14/prompts/E14_01_antigravity_repository_model_isolation.md`
- `data/screenshots/E01-007_antigravity_observable_execution.png`
- `docs/governance/history/model_spec_c2/antigravity/freeze/submission_antigravity_v4_tournament.py`
- `experiments/e17/tools/antigravity/analyze_top3_replays.py`
- `src/agricola/strategy/antigravity/antigravity_3q_high_density_v4.py`

Esito campione: `10/10` coerenti con il CSV.

### 3. Verifica hash su file `tracked_deleted`

Per i file assenti dal working tree ma presenti in `HEAD`, il CSV è coerente con il blob Git verificato:

- `docs/benchmark/101462495.json`
- `docs/benchmark/101761797.json`
- `docs/benchmark/101891362.json`
- `docs/benchmark/104515697.json`
- `docs/benchmark/json.txt`

Esito campione: `5/5` coerenti con il blob `HEAD`.

### 4. Verifica copertura dei path Antigravity

Copertura confermata per:

- `docs/model/model_specs/antigravity/`
- `docs/model/reviews/antigravity/`
- `scripts/e17/antigravity/`
- `results/model_spec_c2/antigravity/`

Per `src/agricola/strategy/antigravity/` i soli file non presenti nel CSV sono artefatti generati in `__pycache__/` (`19` file `.pyc` untracked).

### 5. Verifica `references_found`

Campione verificato su righe con riferimenti:

- `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md`
- `experiments/archive/e15/artifacts/M1_antigravity_vs_codex/E15_M1_CHALLENGE_ANTIGRAVITY.md`
- `experiments/archive/e15/artifacts/M3_copilot_vs_antigravity/E15_M3_CHALLENGE_ANTIGRAVITY.md`
- `docs/governance/history/model_spec_c2/antigravity/README.md`

Nel campione i riferimenti elencati esistono e non emergono path rotti.

### 6. Verifica duplicati per contenuto

Il CSV segnala duplicati byte-identici coerenti con il mandato A0, senza rimozione automatica. Campioni rilevanti:

- `data/replays/reference/101294736.json` identico a `experiments/archive/e12/artifacts/x111/101294736.json`
- `docs/governance/history/model_spec_c2/antigravity/freeze/submission_antigravity_v4_tournament.py`
  `docs/governance/history/model_spec_c2/post_3q_closure_tournament/freeze/submission_antigravity_v4.py`
  `experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py`

La segnalazione del duplicato esiste; nessuna azione distruttiva è stata eseguita.

## Rilievi

### MINOR-01 — Cache Python non inventariate separatamente

Nel tree `src/agricola/strategy/antigravity/__pycache__/` sono presenti `19` file `.pyc` untracked non rappresentati nel CSV e non segnalati separatamente nelle note.

Impatto:

- non blocca A0 sui file sorgente o sui freeze
- riduce però la completezza della fotografia del worktree, dato che il prompt ammette una segnalazione separata di cache e directory vuote

Raccomandazione:

- aggiungere una nota esplicita in reconciliation o in un inventario integrativo che classifichi `__pycache__/` come artefatto transient/cache non migrabile

### MINOR-02 — Review A0 valida, ma non sufficiente a chiudere il fronte A

Il CSV reviewato è consistente nel campione controllato, ma il prompt richiede tre inventari e successiva reconciliation Codex prima di dichiarare il riordino completo.

Impatto:

- nessun blocco locale A0
- impossibile promuovere da questa review lo stato di Fronte A a `COMPLETE`

## Blocker

Nessun `BLOCKER` emerso nella review del CSV Antigravity.

## Decisione A0

`A0_DECISION: PASS_CON_RILIEVI_MINOR`

Motivazione sintetica:

- inventario strutturalmente coerente
- nessuna collisione su `proposed_destination`
- hash confermati su campione significativo di file presenti e `tracked_deleted`
- copertura buona degli artefatti Antigravity e dei documenti comuni obbligatori
- residuo soltanto un debt minore sulla segnalazione esplicita delle cache `__pycache__`

## Stato operativo

- `A0_REVIEW_LOCAL_STATUS: PASS`
- `UNRESOLVED_BLOCKERS: 0`
- `READY_FOR_A1_RECONCILIATION_INPUT: YES`
- `AUTHORIZED_TO_START_E17: NO`
