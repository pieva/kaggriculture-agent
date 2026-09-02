# KAGGRICULTURE C2 — DECISION LIFECYCLE CONTRACT INDEPENDENT REVIEW

## 0. Ruolo

Agisci come **Independent Decision Lifecycle Reviewer**.

Devi eseguire una review critica del documento:

```text
docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md
```

Il documento è un **DRAFT** del quinto layer condiviso della Model Foundation.

Questa attività è **REVIEW ONLY**.

Non modificare:
- Decision Lifecycle Contract;
- Engine Contract;
- Ontology;
- Environment State Machine;
- Feature Model;
- README;
- MODEL_SPEC;
- codice.

Non proporre una strategia di gioco.

---

## 1. Autorità e documenti da leggere

Prima della review leggi almeno:

```text
docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md

docs/foundation/ontology/ONTOLOGY_C2.md
docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md

results/model_spec_c2/foundation_revision/
ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md

results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md

results/model_spec_c2/foundation_revision/
FOUNDATION_CROSS_REVIEW_RECONCILIATION.md

results/model_spec_c2/foundation_revision/
FOUNDATION_FINAL_FREEZE_REVIEW.md

README.md
```

Se necessario, consulta direttamente il runtime/source congelato per verificare affermazioni che il DLC attribuisce all'ambiente.

Gerarchia di autorità:

```text
runtime/source
>
Frozen Engine Contract
>
Frozen Ontology / Environment State Machine / Feature Model
>
Foundation reconciliation/freeze reports
>
Decision Lifecycle Draft
```

La Foundation frozen non deve essere riaperta per accomodare il DLC.

Se il DLC contraddice la Foundation, il finding è nel DLC.

---

## 2. Obiettivo della review

Determina se il Decision Lifecycle Contract è:

1. completo come protocollo deliberativo comune;
2. coerente con la Foundation frozen;
3. strategy-neutral;
4. sufficientemente preciso da vincolare i futuri MODEL_SPEC;
5. non eccessivamente prescrittivo;
6. privo di future leakage;
7. privo di ambiguità tra stato ambiente e stato deliberativo;
8. capace di rappresentare failure, repair, invalidation, cancellation, supersession e terminal closure;
9. sufficientemente tracciabile per replay, audit e performance review.

Non valutare se una particolare strategia agricola sarebbe efficace.

---

## 3. Architettura da preservare

La separazione normativa deve restare:

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

Il DLC definisce **come una decisione viene formalmente aperta, pianificata, committed, verificata, chiusa e riesaminata**.

Il MODEL_SPEC definisce **come l'agente sceglie**.

Segnala come policy leakage qualsiasi regola del DLC che prescriva impropriamente:

```text
crop/livestock mix
economic target
utility/scoring
workforce size
routing
market policy
expansion policy
planning horizon
commitment duration
cash/feed buffers
risk tolerance
exploration
retirement/liquidation
action priority
opponent response
quantitative invalidation thresholds
```

---

## 4. Review della macchina a stati

Verifica individualmente:

```text
DECISION_OPEN
DEFINED
PLAN_FEASIBLE
INFEASIBLE
REJECTED
COMMITTED_EXECUTING
REPAIR_WITHIN_COMMITMENT
INVALIDATED
CANCELLED
SUPERSEDED
COMPLETED
REVIEW_READY
TERMINAL_CLOSED
```

Per ogni stato controlla:

- semantica univoca;
- entry condition;
- exit condition;
- transizioni mancanti;
- transizioni impossibili;
- sovrapposizioni semantiche;
- rischio di dead-end;
- rischio di loop non governato;
- possibilità di rappresentazione tramite evidenza Foundation.

Controlla specificamente se la macchina gestisce correttamente:

```text
feasibility failure
pre-commit rejection
successful completion
repair success
repair failure
commitment invalidation
explicit cancellation
supersession
terminal during planning
terminal during execution
terminal during review
```

---

## 5. REACT e VERIFY

Verifica criticamente la scelta di NON rappresentare `REACT` e `VERIFY` come semplici stati lineari.

### REACT

Deve essere un meccanismo di intake/evaluation degli eventi e non una scorciatoia per:

```text
event → arbitrary strategy change
```

Verifica che non permetta di bypassare:

```text
DEFINE
PLAN
FEASIBILITY
COMMIT
```

### VERIFY

Deve operare durante `COMMITTED_EXECUTING` sulla base di:

```text
ACTION_REQUEST
SNAPSHOT_ELIGIBILITY
EXECUTION_OUTCOME
POST_STATE_EVIDENCE
```

Verifica che VERIFY non diventi implicitamente un secondo planner.

---

## 6. Commitment e anti-oscillation

Valuta la regola:

```text
NO_REPLAN_WITHOUT_LIFECYCLE_CAUSE
```

Controlla che:

- impedisca silent replanning;
- non impedisca una reazione necessaria;
- non obblighi artificialmente a completare un piano divenuto irrazionale;
- repair e replan siano distinguibili;
- un cambiamento materiale di intent/scope sia versionato;
- invalidation, cancellation e supersession abbiano semantiche distinte.

Segnala eventuali casi in cui il MODEL_SPEC non sarebbe in grado di cambiare strategia legittimamente.

---

## 7. Feasibility

Il DLC deve standardizzare il **protocollo** di feasibility, non l'algoritmo.

Verifica che:

```text
FEASIBLE
INFEASIBLE
```

siano esiti comuni sufficienti e che rimangano agent-specific:

```text
resource requirements
time horizon
risk model
economic criterion
buffers
reservation margins
capacity policy
```

Controlla inoltre l'allineamento con la Foundation su:

```text
ACTION_ELIGIBLE_NOW
batch feasibility
serialization effects
multidimensional capacity
RESERVED_SERVICEABLE_BEFORE_DEADLINE
```

Non consentire che il DLC trasformi `RESERVED_SERVICEABLE_BEFORE_DEADLINE` in un engine fact.

---

## 8. Evidence timing e No-Future-Leakage

Verifica rigorosamente:

```text
S_t
→ ACTION_REQUEST_t
→ SNAPSHOT_ELIGIBILITY_t
→ engine processing
→ EXECUTION_OUTCOME_t
→ S_t+1
→ POST_STATE_EVIDENCE_t+1
→ VERIFY
```

Cerca:

- hindsight leakage;
- uso retroattivo di execution outcome;
- uso anticipato di post-state evidence;
- invalidator definiti dopo il fatto;
- review metric usate come online feature;
- outcome-only data usati per giustificare decisioni precedenti.

Valuta la regola anti-retroattività degli invalidator.

---

## 9. Repair, invalidation, cancellation, supersession

Questa è una parte critica della review.

Verifica che siano realmente distinti:

### Repair

```text
same intent
same commitment
same strategic scope
local execution change
```

### Invalidation

Una condizione necessaria dichiarata non è più soddisfatta.

### Cancellation

Il commitment viene terminato esplicitamente senza richiedere che sia diventato impossibile.

### Supersession

Una decisione successiva sostituisce formalmente il commitment precedente.

Controlla in particolare che la sequenza di supersession non produca:

- circular dependency;
- impossibilità di creare `successor_decision_id`;
- necessità di conoscere una decisione futura prima di poter chiudere quella corrente;
- violazione di `REVIEW before reopen`.

---

## 10. Terminal semantics

Confronta `TERMINAL_CLOSED` con la semantica terminale frozen della Environment State Machine.

Verifica:

- nessun nuovo intent dopo il terminal boundary;
- gestione di un commitment ancora attivo al terminale;
- gestione di decisione DEFINED/PLAN_FEASIBLE al terminale;
- possibilità di final review/post-hoc telemetry;
- assenza di azioni online dopo terminal closure.

Segnala eventuale conflitto tra stato assorbente e materializzazione della review finale.

---

## 11. REVIEW

Verifica la distinzione:

```text
DIRECT_ACCOUNTING
DESCRIPTIVE_DIAGNOSTICS
CAUSAL_OR_COUNTERFACTUAL_ANALYSIS
```

Controlla che il DLC:

- non presenti correlazione come causalità;
- non obblighi il controller online a produrre inferenza causale;
- consenta analisi per categoria/specie nei tournament futuri;
- mantenga `EXPAND / MAINTAIN / REDUCE / REMOVE / INCONCLUSIVE` come output di review e non come policy Foundation.

---

## 12. Provenance

Verifica che sia possibile ricostruire senza ambiguità:

```text
run
episode
transition
decision
decision version
plan
plan version
commitment
action request
execution outcome
post-state evidence
review
supersession chain
```

Controlla la compatibilità con:

```text
(run_id, episode_id)
engine_fingerprint
configuration_hash
foundation_version
feature_schema_version
telemetry_schema_version
agent_id
model_spec_version
```

Segnala ID mancanti o relazioni insufficienti.

---

## 13. Boundary DLC ↔ MODEL_SPEC

Questa verifica è obbligatoria.

Per ogni concetto del DLC chiediti:

> è un protocollo comune necessario a tutti gli agenti, oppure è già una scelta di controller?

Segnala:

### `FOUNDATION_REQUIRED`

se deve restare nel DLC.

### `MODEL_SPEC_REQUIRED`

se deve essere spostato downstream.

### `AMBIGUOUS_BOUNDARY`

se necessita di una definizione più neutrale.

Non progettare il MODEL_SPEC.

---

## 14. Conformance invariants

Verifica uno per uno:

```text
DLC-INV-01 No future leakage
DLC-INV-02 Explicit commitment
DLC-INV-03 No silent replan
DLC-INV-04 Evidence-driven invalidation
DLC-INV-05 Repair preserves commitment
DLC-INV-06 Explicit execution evidence
DLC-INV-07 Review before reopen
DLC-INV-08 Terminal closure
DLC-INV-09 Strategy neutrality
DLC-INV-10 Version integrity
```

Per ciascuno assegna:

```text
PASS
FAIL
AMBIGUOUS
```

e motiva eventuali FAIL/AMBIGUOUS.

---

## 15. Failure-mode challenge

Esegui almeno questi test concettuali senza inventare policy:

### FM-01
Piano dichiarato feasible, ma la prima action request produce `NO_OP`.

### FM-02
Il commitment resta tecnicamente eseguibile ma cambia fortemente lo stato del mercato.

### FM-03
Una reservation diventa insufficiente durante il commitment.

### FM-04
Un repair locale fallisce.

### FM-05
Il terminal boundary arriva durante `COMMITTED_EXECUTING`.

### FM-06
Il terminal boundary arriva in `REVIEW_READY`.

### FM-07
Due eventi nello stesso transition suggeriscono contemporaneamente completion e invalidation.

### FM-08
Un nuovo piano appare preferibile, ma nessun invalidator del commitment corrente è attivato.

### FM-09
Un commitment viene cancellato volontariamente.

### FM-10
Un commitment deve essere superseded da una nuova decisione che non esiste ancora.

Per ciascun caso determina se il DLC produce una transizione:

```text
DETERMINISTIC
AMBIGUOUS
IMPOSSIBLE
```

I casi `AMBIGUOUS` o `IMPOSSIBLE` devono diventare finding.

---

## 16. Severity

Classifica i finding:

### P0 — BLOCKER
Il DLC non può essere congelato:
- contraddizione con Foundation/runtime;
- future leakage;
- state machine incoerente;
- deadlock strutturale;
- policy leakage sostanziale;
- impossibilità di rappresentare una normale decisione.

### P1 — MAJOR
Il modello è valido ma necessita correzione prima del freeze:
- transizione ambigua;
- lifecycle failure non coperto;
- provenance insufficiente;
- boundary DLC/MODEL_SPEC non chiaro;
- reason/evidence semantics incomplete.

### P2 — MINOR
Correzione editoriale o precisione non strutturale:
- naming;
- diagramma;
- mapping;
- wording;
- esempio non perfettamente allineato.

Non abbassare artificialmente la severity per arrivare a PASS.

---

## 17. Output

Crea:

```text
results/model_spec_c2/foundation_revision/
<AGENT>_DECISION_LIFECYCLE_INDEPENDENT_REVIEW.md
```

dove `<AGENT>` identifica il reviewer.

Struttura:

```text
1. Executive Verdict
2. Documents Reviewed
3. Foundation Alignment
4. State Machine Review
5. REACT / VERIFY Review
6. Commitment & Anti-Oscillation Review
7. Feasibility Review
8. Evidence Timing / No-Future-Leakage
9. Repair / Invalidation / Cancellation / Supersession
10. Terminal Semantics
11. REVIEW Semantics
12. Provenance
13. DLC ↔ MODEL_SPEC Boundary
14. Conformance Invariants
15. Failure-Mode Challenge
16. Findings Register
17. Required Corrections
18. Final Gate
```

Finding register minimo:

```text
finding_id
severity
section
claim
evidence
impact
required_correction
```

---

## 18. Final Gate

Usa:

```text
FOUNDATION_ALIGNMENT:
DLC_STATE_COMPLETENESS:
DLC_TRANSITION_COMPLETENESS:
REACT_SEMANTICS:
VERIFY_SEMANTICS:
COMMITMENT_ANTI_OSCILLATION:
FEASIBILITY_BOUNDARY:
EVIDENCE_TIMING_ALIGNMENT:
NO_FUTURE_LEAKAGE:
REPAIR_VS_REPLAN:
INVALIDATION_SEMANTICS:
CANCELLATION_SEMANTICS:
SUPERSESSION_SEMANTICS:
TERMINAL_SEMANTICS:
REVIEW_SEMANTICS:
PROVENANCE_SUFFICIENCY:
MODEL_SPEC_BOUNDARY:
STRATEGY_NEUTRALITY:
CONFORMANCE_INVARIANTS:
FAILURE_MODE_COVERAGE:
MERMAID_RENDERABILITY:

P0_OPEN:
P1_OPEN:
P2_OPEN:

DECISION_LIFECYCLE_REVIEW:
DECISION_LIFECYCLE_FREEZE_RECOMMENDED:
```

Verdetti consentiti:

```text
PASS
PASS_WITH_P2
CORRECTIONS_REQUIRED
FAIL_WITH_BLOCKERS
```

`DECISION_LIFECYCLE_FREEZE_RECOMMENDED: YES` soltanto se:

```text
P0_OPEN = 0
P1_OPEN = 0
```

---

## 19. Stop condition

Dopo aver scritto il report:

**FERMATI.**

Non modificare il DLC.
Non riconciliare i finding degli altri agenti.
Non creare MODEL_SPEC.
Non modificare codice.
Non eseguire benchmark.
Non eseguire tournament.
Non eseguire Kaggle.
