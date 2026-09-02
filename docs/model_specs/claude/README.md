# Indice MODEL_SPEC Claude

| Stato | File | Uso |
|---|---|---|
| REJECTED BEFORE TOURNAMENT | [`MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE.md`](MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE.md) | V1, gate economico e di sicurezza zootecnica falliti; conservata come evidenza. Report: [`E17_1_CLAUDE_REACTIVE_V1_FAILED_GATE_REPORT.md`](../../../experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V1_FAILED_GATE_REPORT.md) e [`E17_1_CLAUDE_REACTIVE_IMPLEMENTATION_REPORT.md`](../../../experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_IMPLEMENTATION_REPORT.md) |
| FROZEN_WITH_FAILED_GATES / DEVELOPMENT | [`MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V2.md`](MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V2.md) | V2, remediation della V1: miglioramento netto su tutti i KPI (money +57%, fughe 8→3, MOVE 77%→69%) ma non ancora ammissibile al torneo. Report: [`E17_1_CLAUDE_REACTIVE_V2_IMPLEMENTATION_REPORT.md`](../../../experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V2_IMPLEMENTATION_REPORT.md) |
| AUTHORIZED PLAN / NOT EXECUTED | [`E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md`](../../../experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md) | V3 non ancora implementata; autorizzato soltanto il benchmark Codex black-box sui seed development. |

Claude condivide la Foundation C2.1, il contratto osservativo e il protocollo
E17, ma possiede autonomamente modello, feature effettivamente consumate,
planner, priorità, routing e implementazione.

Le candidate Codex congelate possono essere usate da runner esterni come
avversari black-box, non come sorgente o componente della policy Claude. La
decisione normativa è in
[`E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`](../../../experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md).
