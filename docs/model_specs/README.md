# Agent-owned model material

`docs/model_specs/<agent>/` is the canonical home for every asset owned by a
single agent. This includes model specifications and, under the round folder,
agent-specific configs, designs, prompts, reports, reviews, tools, tests,
candidate harnesses and provenance artifacts.

```text
docs/model_specs/<agent>/
|-- MODEL_SPEC_*.md
|-- README.md
|-- e17/
|   |-- artifacts/{derived,discovery,freeze,runs}/
|   |-- candidates/
|   |-- configs/
|   |-- design/
|   |-- prompts/
|   |-- reports/
|   |-- reviews/
|   |-- tests/
|   `-- tools/
`-- e18/
    `-- ...
```

`experiments/` contains only round-level material shared across agents:
manifests, neutral designs and prompts, common runners and tests, cross-agent
tournaments, shared discovery data and common reports. A common asset may
name one or more agents when it compares them; ownership is determined by its
role and directory, not by the mere occurrence of an agent name.

Frozen and historical evidence is moved without changing its contents, so
embedded provenance continues to describe the layout in which the evidence
was originally produced. Current code and documentation must use the
canonical paths above.

Runtime policy code under `src/`, release submissions under `submission/` and
the repository-wide test suite under `tests/` keep their existing package or
release layout; this rule governs model material and round-scoped experiments.
