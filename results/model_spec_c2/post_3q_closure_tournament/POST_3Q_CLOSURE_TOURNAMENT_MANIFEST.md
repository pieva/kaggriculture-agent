# Post-3Q Closure Tournament — Manifest congelato

- **Protocol:** `POST_3Q_CLOSURE_THREE_WAY_FROZEN_V1`
- **Freeze date:** 2026-09-01
- **Match:** 42
- **Seed:** 7 preregistrati
- **Seat:** entrambi per ogni coppia e seed
- **Post-hoc selection:** vietata
- **Scopo:** fotografia di chiusura dell'ultimo round 3Q, mentre i feedback Foundation sono in attesa

## Seed congelati

```text
26090101
26090102
26090103
1838889274
1619968655
710418712
562040596
```

## Coppie

```text
ANTIGRAVITY vs CODEX
ANTIGRAVITY vs COPILOT
CODEX vs COPILOT
```

Ogni coppia viene eseguita nelle due assegnazioni di seat per ciascun seed: 14 match per coppia, 28 match per agente.

## Candidate freeze

| Agente | Versione | Freeze | SHA-256 file |
|---|---|---|---|
| Antigravity | `ANTIGRAVITY-C2-V4.0-3Q-HIGH-DENSITY-MEGA-CLUSTER` | `freeze/submission_antigravity_v4.py` | `5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872` |
| Codex | `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY` | `freeze/submission_codex_v9.py` | `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421` |
| Copilot | `COPILOT-C2-V2.0-3Q-HIGH-DENSITY` | `freeze/submission_copilot_v2.py` | `DABD7FEFBBBC36396AEE04BD883CE0770D4B96D1312BB3CE009E051AC3C20A94` |

Il runner verifica questi hash prima del primo match e si arresta su qualsiasi divergenza.

## Gate di indipendenza preregistrato

```text
STRATEGIC_INDEPENDENCE_GATE: FAIL
COMMON_ROUTINE_SHA256: C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
```

Motivazione: Antigravity V4 e Copilot V2 riusano la routine Codex V9. Copilot è azione-per-azione equivalente; Antigravity aggiunge la liquidazione terminale agli step 717–719. Queste differenze permettono di misurare l'effetto della liquidazione, ma non costituiscono tre strategie indipendenti.

Di conseguenza:

- il torneo è valido come replica congelata e misura di side effect/seat/terminal liquidation;
- non è valido per attribuire indipendentemente la strategia ai tre agenti;
- non promuove automaticamente alcun MODEL_SPEC o submission;
- il prossimo torneo comparativo richiederà il pass di tutti i gate di indipendenza definiti nel prompt di cross-review.

## Output attesi

```text
POST_3Q_CLOSURE_TOURNAMENT_RESULTS.json
POST_3Q_CLOSURE_TOURNAMENT_RESULTS.csv
POST_3Q_CLOSURE_TOURNAMENT_REPORT_IT.md
```

Runner: `scripts/run_post_3q_closure_tournament.py`.
