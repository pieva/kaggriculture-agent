# Claude strategy namespace

This directory is reserved for Claude's strategically independent policies.

Claude may use shared modules under `agricola.core`, including the observation
contract and E17 ledger integration points. It must not import, copy or wrap
code, routines, planners, action tables or schedules from another agent's
strategy namespace.

The first authorized deliverable is described in:

`docs/model_specs/claude/e17/prompts/E17_CLAUDE_REACTIVE_3Q_INDEPENDENT_BUILD_PROMPT.md`

V1 was rejected and V2 was frozen with failed economic, escape and passive
3Q gates. A future V3 is planned but not started. During V3 development Claude
may face frozen Codex candidates strictly as black-box opponents; it may not
read, analyse, copy or import Codex strategic artifacts. The authorization is:

`experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`
