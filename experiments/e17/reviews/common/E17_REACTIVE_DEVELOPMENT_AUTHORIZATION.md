# E17 — Autorizzazione successiva allo sviluppo reattivo e al torneo a tre

- **Data:** 2026-09-02
- **Autorità:** proprietario del repository
- **Stato:** AUTHORIZED
- **Natura:** decision record successivo al freeze E17.0

## Decisione

Il proprietario autorizza lo sviluppo di due nuove candidate reattive e il
successivo torneo locale a tre:

1. Codex V9 corrente, immutabile, come controllo open-loop;
2. Codex reattivo, derivato dichiaratamente dalla baseline V9;
3. Claude reattivo, sviluppato come policy strategicamente indipendente.

Antigravity e Copilot vengono congelati nello stato corrente. Non partecipano
allo sviluppo né al torneo autorizzato da questo record.

## Rapporto con il freeze precedente

Questo record non modifica retroattivamente
`experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`. Il precedente stop prima di
E17.1 resta la preregistrazione storica valida al momento del freeze; la
decisione odierna ne supera prospetticamente il confine di autorizzazione.

## Confini

```text
E17_1_REACTIVE_DEVELOPMENT: AUTHORIZED
THREE_WAY_LOCAL_TOURNAMENT: AUTHORIZED_AFTER_BOTH_CANDIDATES_FREEZE
ANTIGRAVITY: FROZEN_EXCLUDED
COPILOT: FROZEN_EXCLUDED
CLAUDE_STRATEGIC_INDEPENDENCE: REQUIRED
NEW_KAGGLE_SUBMISSION: NOT_AUTHORIZED
COMMIT: NOT_AUTHORIZED_BY_THIS_RECORD
PUSH: NOT_AUTHORIZED_BY_THIS_RECORD
```

Il confronto V9 vs Codex reattivo può essere interpretato come evoluzione
intra-agent e, quando monofattoriale, come ablation. Il confronto con Claude
misura una diversa famiglia di modello e non deve essere presentato come
ablation di una singola leva.
