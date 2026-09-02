# ANTIGRAVITY — FOUNDATION PATH HOUSEKEEPING & FINAL FREEZE REVIEW PROMPT

## 0. Mandato

Esegui un ultimo pass **esclusivamente documentale e di housekeeping** sulla Model Foundation C2.

La directory:

```text
results/model_spec_c2/foundation_cross_review/
```

è stata eliminata intenzionalmente.

Tutti gli artefatti di review, reconciliation e consolidation che devono essere conservati hanno ora come directory canonica:

```text
results/model_spec_c2/foundation_revision/
```

Questo pass NON deve riaprire la revisione tecnica della Foundation.

---

## 1. Obiettivi

1. Eliminare tutti i riferimenti obsoleti a:

```text
results/model_spec_c2/foundation_cross_review/
```

2. Rendere coerenti i path canonici nei documenti conservati.
3. Verificare che la provenance necessaria sia presente in:

```text
results/model_spec_c2/foundation_revision/
```

4. Eseguire una **Final Foundation Freeze Review** documentale.
5. Se non emergono difetti sostanziali, proporre il freeze finale.

---

## 2. Artefatti canonici da preservare

Verifica la presenza, con i nomi effettivamente esistenti nel repository, degli artefatti necessari, inclusi almeno:

```text
ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md

ANTIGRAVITY_FOUNDATION_CROSS_REVIEW.md
COPILOT_FOUNDATION_CROSS_REVIEW.md
CODEX_FOUNDATION_CROSS_REVIEW.md

FOUNDATION_CROSS_REVIEW_RECONCILIATION.md
FOUNDATION_CONSOLIDATION_REPORT.md
```

Non ricreare `foundation_cross_review/`.

Se uno di questi file ha un nome leggermente diverso, usa il file realmente presente e documentalo.

---

## 3. Correzione path

Cerca nel repository tutti i riferimenti testuali a:

```text
foundation_cross_review
results/model_spec_c2/foundation_cross_review
```

Correggi soltanto i riferimenti che indicano artefatti ora collocati in:

```text
results/model_spec_c2/foundation_revision/
```

Controlla almeno:

```text
README.md
FOUNDATION_CONSOLIDATION_REPORT.md
FOUNDATION_CROSS_REVIEW_RECONCILIATION.md
i tre report indipendenti di cross-review
eventuali manifest / PROJECT_STATE / NEW_SESSION / EXPERIMENT_LOG
```

Non modificare riferimenti storici se sono chiaramente descrittivi e non rappresentano un path operativo, salvo che generino ambiguità.

---

## 4. Correzione obbligatoria del Consolidation Report

Nel `FOUNDATION_CONSOLIDATION_REPORT.md` aggiorna:

- `Autorità di Riconciliazione`;
- `Destinazione Repository`;
- riferimenti agli input tri-agent;
- riferimenti alla reconciliation;
- qualsiasi altro path che punti alla directory eliminata.

La destinazione canonica del report deve essere:

```text
results/model_spec_c2/foundation_revision/
FOUNDATION_CONSOLIDATION_REPORT.md
```

Non alterare il suo contenuto tecnico salvo correzioni strettamente necessarie di path/provenance.

---

## 5. Final Freeze Review — scope limitato

Dopo il housekeeping, esegui una verifica finale sui tre artefatti consolidati:

```text
docs/foundation/ontology/ONTOLOGY_C2.md
docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
```

Lo scopo NON è una nuova cross-review.

Verifica soltanto che il consolidation dichiarato sia effettivamente presente e internamente consistente:

```text
CORR-01 .. CORR-14 applicate
nessun riferimento residuo a worker carrying capacity engine
raw observation paths corretti
configuration-parametric constants
fertilizer ongoing con watering
BUILD_COOP/BUILD_PASTURE senza costo monetario
pending_care_bonus reset corretto
5 environment tile views + policy overlays
batch/serialization semantics
Wheat physical vs monetary accounting
configuration provenance
traceability mappings
policy neutrality
ACTION_REQUEST / SNAPSHOT_ELIGIBILITY / EXECUTION_OUTCOME / POST_STATE_EVIDENCE
EOD / terminal semantics
epistemic/evidence/observability taxonomy
```

Se trovi un difetto sostanziale:

```text
FOUNDATION_FREEZE = NO
```

e documentalo precisamente.

Non correggere automaticamente nuovi difetti sostanziali non coperti dal consolidation; fermati e riportali.

Sono invece autorizzate correzioni puramente editoriali, path, link interni e typo che non cambiano semantica.

---

## 6. Mermaid

Verifica che i blocchi Mermaid presenti nei Markdown:

- siano ancora sintatticamente validi;
- non contengano riferimenti obsoleti;
- riflettano i documenti consolidati.

Non generare immagini.

---

## 7. README

Il README deve rappresentare:

```text
MODEL FOUNDATION
├── Engine Contract
├── Ontology
├── Environment State Machine
├── Feature Model
└── Decision Lifecycle Contract
        ↓
AGENT-SPECIFIC MODEL_SPEC
├── Antigravity MODEL_SPEC
├── Codex MODEL_SPEC
└── Copilot MODEL_SPEC
```

e deve chiarire:

```text
C2 = Cycle 2
```

Il `Decision Lifecycle Contract` deve risultare:

```text
ARCHITECTURAL_LAYER_APPROVED
DOCUMENT_NOT_YET_CREATED_OR_FROZEN
```

Non scrivere il Decision Lifecycle Contract in questo pass.

---

## 8. Verifiche repository

Esegui almeno:

```text
git status --short
git diff --check
```

Cerca riferimenti residui:

```text
foundation_cross_review
```

e verifica che non esista più la directory eliminata.

Se sono disponibili controlli documentali già esistenti nel repository, eseguili.

---

## 9. Report finale

Crea o aggiorna in:

```text
results/model_spec_c2/foundation_revision/
FOUNDATION_FINAL_FREEZE_REVIEW.md
```

Struttura minima:

```text
1. Scope
2. Canonical Foundation Revision Layout
3. Path Housekeeping
4. Consolidation Verification
5. Cross-Layer Consistency Check
6. README Alignment
7. Mermaid Verification
8. Repository Verification
9. Residual Findings
10. Final Freeze Gate
```

---

## 10. Final Freeze Gate

Usa:

```text
ENGINE_CONTRACT_FREEZE:
ONTOLOGY_FREEZE:
STATE_MACHINE_FREEZE:
FEATURE_MODEL_FREEZE:

FOUNDATION_ENGINE_ALIGNMENT:
FOUNDATION_CROSS_LAYER_ALIGNMENT:
EPISTEMIC_TAXONOMY_ALIGNMENT:
POLICY_NEUTRALITY:
NO_FUTURE_LEAKAGE:
ACTION_EVIDENCE_SEPARATION:
PERFORMANCE_ACCOUNTING:
PROVENANCE:
MERMAID_RENDERABILITY:
README_ARCHITECTURE_ALIGNED:
FOUNDATION_REVISION_LAYOUT_ALIGNED:

P0_OPEN:
P1_OPEN:
P2_OPEN:

FOUNDATION_FREEZE:
DECISION_LIFECYCLE_DRAFTING_RECOMMENDED:

DECISION_LIFECYCLE_DRAFTING_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Se tutti i controlli sostanziali sono PASS e non esistono P0/P1 aperti:

```text
FOUNDATION_FREEZE: YES
DECISION_LIFECYCLE_DRAFTING_RECOMMENDED: YES
```

Questo freeze riguarda i quattro artefatti Foundation già materializzati:

```text
Engine Contract
Ontology
Environment State Machine
Feature Model
```

Il `Decision Lifecycle Contract` è il **prossimo layer da redigere** e non è incluso nel freeze documentale corrente.

---

## 11. Stop condition

Dopo housekeeping, verifica e report:

**FERMATI.**

Non creare il Decision Lifecycle Contract.
Non creare o modificare MODEL_SPEC.
Non modificare codice.
Non eseguire benchmark.
Non eseguire tournament.
Non eseguire Kaggle.
