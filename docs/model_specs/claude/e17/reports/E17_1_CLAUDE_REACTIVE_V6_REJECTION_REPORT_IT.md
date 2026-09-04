# E17 — Claude V6 regression check e rifiuto

- **Data:** 2026-09-03
- **Candidata:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V6`
- **Controllo:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
- **Ruolo evidenza:** `DEVELOPMENT_ONLY_NON_QUALIFYING`
- **Decisione:** REJECTED
- **Holdout/final:** non consumati

## Ipotesi

V6 disattiva il clustering per quadrante quando la workforce è insufficiente.
La modifica correggeva il collasso V5 osservato sul singolo caso seed
`26090102`, seat 1 (`78` → `15.743`), ma doveva superare un controllo di
generalizzazione prima di qualunque confronto esterno.

## Protocollo

Confronto V6 contro V3 sui sette seed development E17 già consumati e sui due
orientamenti di seat: `14` match. Nessun seed holdout o final-confirmation.
La V6 usa il proprio namespace e non importa policy di altri modeler.

## Risultati

| Indicatore | V6 | V3 / riferimento |
|---|---:|---:|
| W-L | `1-13` | `13-1` |
| Denaro medio | `1.538,50` | `17.119,36` |
| Delta medio | `-15.580,86` (`-91,01%`) | — |
| Minimo V6 | `32` | — |
| Massimo V6 | `15.743` | — |
| Run V6 sotto 5k | `13/14` | — |
| 3Q V6 | `1/14` | — |
| Errori tecnici V6 | `0` | — |

Il solo caso usato per formulare la correzione passa, mentre tutti gli altri
tredici falliscono. L'assenza di errori tecnici conferma una regressione di
policy: il gate workforce evita uno specifico deadlock ma altera il dispatch
globale in modo economicamente distruttivo.

## Decisione

Un benchmark black-box parallelo contro Codex V9 e Codex reattivo, su quattro
seed development e due seat, produce altri `16` match: V6 chiude `0-16`, media
`622,88` contro `144.654,75`, senza raggiungere 3Q e con zero errori tecnici.
Il risultato conferma che la regressione è strategica.

V6 è respinta. V5 resta un'ablation di ricerca non promossa; V3 resta soltanto
il controllo storico Claude. Nessuna versione Claude accede a E18, holdout o
submission Kaggle.

Fonti:

- `docs/model_specs/claude/e17/artifacts/derived/E17_1_V6_VS_V3_REGRESSION_CHECK.json`;
- `docs/model_specs/claude/e17/artifacts/derived/E17_1_V6_DEV_BENCHMARK_VS_CODEX.json`;
- `docs/model_specs/claude/e17/tools/run_claude_e17_1_v6_vs_v3_regression_check.py`;
- `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V6.md`.
