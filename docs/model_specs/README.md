# Agent-owned model material

## Contenuto delle MODEL_SPEC

Una MODEL_SPEC descrive la strategia di un modello decisionale e come è
realizzata nel codice. Deve contenere:

1. Obiettivo, ambito e ipotesi del modello.
2. Pianificazione, criteri di scelta e priorità fra azioni concorrenti.
3. Vincoli, reazioni agli imprevisti e comportamento di chiusura.
4. Elenco dei file di implementazione, con collegamenti e responsabilità.
5. Collegamenti a configurazione, builder e verifiche della policy.

Distinguere il comportamento implementato da quello proposto. Stato del lavoro,
risultati dei benchmark e prossime attività vanno nei registri o nei report,
collegati dalla specifica. Gli esperimenti storici congelati restano preservati.

Esempio: [strategia Codex 770 e sorgenti](codex/e19/MODEL_SPEC_CODEX_770_V48.md).

## Organizzazione dei materiali

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
