# KAGGRICULTURE C2 — DECISION LIFECYCLE REVIEW RECONCILIATION

```text
DOCUMENT_ID: KAGGRICULTURE_DECISION_LIFECYCLE_REVIEW_RECONCILIATION
DATE: 2026-08-31
RECONCILER: Foundation Architecture
INPUT_1: ANTIGRAVITY_DECISION_LIFECYCLE_INDEPENDENT_REVIEW.md
INPUT_2: CODEX_DECISION_LIFECYCLE_INDEPENDENT_REVIEW.md
TARGET: KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md / C2-DRAFT-01
STATUS: COMPLETE — CANONICAL CORRECTION SET ESTABLISHED
```

## 1. Executive verdict

Le due review indipendenti convergono sulla validità dell'architettura generale del Decision Lifecycle Contract e sull'assenza di policy leakage agricolo e future leakage esplicito.

Il draft C2-DRAFT-01 non è tuttavia congelabile.

La riconciliazione accetta un correction set canonico di 11 correzioni (`DLC-CORR-01` .. `DLC-CORR-11`). Il blocker principale è la dipendenza circolare nella supersession. Ulteriori correzioni riguardano precedence, terminal closure, repair, feasibility provenance, VERIFY ledger, evidence timing, versioning, review completion e parità diagrammatica.

Nessuna correzione richiede la riapertura dei quattro layer Foundation già frozen.

## 2. Reconciliation principles

Gerarchia:

```text
Frozen Foundation
>
protocol determinism
>
auditability / replayability
>
strategy neutrality
>
reviewer-specific proposed wording
```

Una proposta dei reviewer viene:
- `ACCEPTED` se corregge un difetto reale senza spostare policy nel DLC;
- `ACCEPTED_WITH_REFORMULATION` se il problema è reale ma la soluzione proposta è troppo prescrittiva;
- `MERGED` se più finding descrivono lo stesso difetto;
- `REJECTED` se introdurrebbe policy o complessità non necessaria.

## 3. Canonical findings

### DLC-CORR-01 — Supersession non circolare — P0

**Origine:** Antigravity FND-DLC-02; Codex DLC-REV-P0-01.

**Decisione:** ACCEPTED_WITH_REFORMULATION.

Al momento della chiusura di A non deve essere richiesto un `successor_decision_id` riferito a un oggetto futuro.

Introdurre:

```text
supersession_intent_id
supersession_reason_code
supersession_policy_version
supersession_evidence_snapshot_id
```

`successor_decision_id` è nullable al momento della closure e viene valorizzato soltanto quando la nuova decisione viene effettivamente creata in `DEFINED`.

La relazione è:

```text
commitment_A
→ SUPERSEDED(supersession_intent_id)
→ REVIEW_READY
→ REVIEW_COMPLETE
→ DECISION_OPEN
→ DEFINED(decision_B)
→ link supersession_intent_id → successor_decision_id = decision_B
```

Il link successivo non modifica retroattivamente la causa della supersession: completa soltanto la provenance.

### DLC-CORR-02 — Precedence deterministica delle guardie — P1

**Origine:** Antigravity FND-DLC-01; Codex DLC-REV-P1-02.

**Decisione:** ACCEPTED_WITH_REFORMULATION.

Non adottare la proposta Antigravity basata sulla semantica specifica dell'“output integralmente acquisito”.

Precedence comune:

```text
1. TERMINAL
2. COMPLETION / INVALIDATION conflict resolution
3. INVALIDATION
4. COMPLETION
5. explicit CANCEL / SUPERSEDE
6. REPAIR
7. CONTINUE
```

Per il conflitto simultaneo `completion == true && invalidator == true`:
- il MODEL_SPEC può dichiarare **prima del commitment** una `completion_invalidation_precedence_policy`;
- se non dichiarata, fallback comune e conservativo: `INVALIDATED`;
- entrambi i predicate result restano registrati nel VERIFY record.

Il MODEL_SPEC definisce la policy; il DLC definisce il requisito di pre-dichiarazione e il fallback deterministico.

### DLC-CORR-03 — Terminal closure globale — P1

**Origine:** Codex DLC-REV-P1-01.

**Decisione:** ACCEPTED.

Il terminal boundary ha precedenza globale da ogni stato online non terminale.

Introdurre `terminal_closure_record` con:

```text
terminal_closure_id
previous_lifecycle_state
decision_id?
plan_id?
commitment_id?
terminal_transition_id
terminal_evidence_snapshot_id
closure_disposition = TERMINAL_PREEMPTION | TERMINAL_AFTER_COMPLETION | TERMINAL_AFTER_REVIEW
```

Dopo `TERMINAL_CLOSED` sono consentite soltanto materializzazioni offline/post-hoc; nessuna nuova transizione deliberativa online.

### DLC-CORR-04 — INFEASIBLE vs REJECTED disgiunti — P1

**Origine:** Codex DLC-REV-P1-03; Antigravity FND-DLC-04 parzialmente correlato.

**Decisione:** ACCEPTED.

Semantica:

```text
INFEASIBLE = il feasibility gate è stato eseguito e ha restituito FAIL.
REJECTED   = intent/plan abbandonato pre-commit per causa diversa dal FAIL del feasibility gate.
CANCELLED  = commitment già attivo terminato volontariamente.
```

Rimuovere `FEASIBILITY_REJECTION` dai reason code di `REJECTED`.

### DLC-CORR-05 — Repair record e failure semantics — P1

**Origine:** Codex DLC-REV-P1-04; Antigravity FND-DLC-03 per diagramma.

**Decisione:** ACCEPTED.

Introdurre:

```text
repair_id
commitment_id
repair_attempt
trigger_evidence_snapshot_id
repair_policy_version
plan_version_before
plan_version_after?
repair_result = SUCCEEDED | FAILED | ABORTED
```

Un repair fallito **non implica** automaticamente `INVALIDATED`.

Uscite ammesse:

```text
REPAIR_WITHIN_COMMITMENT → COMMITTED_EXECUTING
REPAIR_WITHIN_COMMITMENT → REPAIR_WITHIN_COMMITMENT
REPAIR_WITHIN_COMMITMENT → INVALIDATED   [solo invalidator valido]
REPAIR_WITHIN_COMMITMENT → CANCELLED
REPAIR_WITHIN_COMMITMENT → SUPERSEDED
REPAIR_WITHIN_COMMITMENT → TERMINAL_CLOSED
```

### DLC-CORR-06 — Governance di cancellation e supersession — P1

**Origine:** Codex DLC-REV-P1-05.

**Decisione:** ACCEPTED_WITH_REFORMULATION.

Non richiedere un invalidator pre-dichiarato per `CANCELLED` o `SUPERSEDED`.

Richiedere invece:

```text
decision_boundary_id
policy_version
authority/reference
reason_code
evidence_snapshot_id
```

La policy che consente cancellation/supersession è agent-specific. La provenance è Foundation-required.

Questo preserva la capacità di cambiare strategia legittimamente senza trasformare cancellation/supersession in alias non auditabili del silent replan.

### DLC-CORR-07 — Feasibility class ledger e freshness — P1

**Origine:** Codex DLC-REV-P1-06.

**Decisione:** ACCEPTED_WITH_REFORMULATION.

Il DLC non obbliga ogni piano a eseguire ogni classe di check.

Il feasibility record deve dichiarare, **quando applicabile**:

```text
check_class =
  SNAPSHOT_ACTION_ELIGIBILITY
  ATOMIC_BATCH_FEASIBILITY
  SERIALIZATION_FEASIBILITY
  CAPACITY_FEASIBILITY
  RESERVED_FUTURE_SERVICEABILITY
  MODEL_SPEC_OTHER

snapshot_id
batch_id?
execution_order_reference?
result
not_applicable_reason?
```

`RESERVED_FUTURE_SERVICEABILITY` è esplicitamente `POLICY_CONTEXT`, non engine guarantee.

Aggiungere:

```text
feasibility_captured_at_transition_id
feasibility_valid_until?
revalidation_policy_version?
revalidated_before_commit
```

Valori e criteri restano MODEL_SPEC-specific.

### DLC-CORR-08 — VERIFY execution-evidence ledger — P1

**Origine:** Codex DLC-REV-P1-07.

**Decisione:** ACCEPTED.

Il VERIFY record deve poter collegare:

```text
action_request_id
snapshot_eligibility_id
execution_outcome_id
post_state_evidence_id
```

con cardinalità esplicita e supporto a:
- nessuna request;
- request con NO_OP;
- request rejected;
- batch;
- azioni serializzate.

VERIFY registra guard evaluation e precedence result. Non seleziona autonomamente una nuova strategia.

### DLC-CORR-09 — Evidence snapshot timing e immutabilità — P1

**Origine:** Codex DLC-REV-P1-08.

**Decisione:** ACCEPTED.

Ogni evidence snapshot DLC deve includere almeno:

```text
evidence_snapshot_id
captured_at_transition_id
available_at_decision_boundary_id
source_state_id?
target_state_id?
evidence_class
```

Gli snapshot sono append-only/versioned.

DEFINE, PLAN, FEASIBILITY e COMMIT possono usare soltanto evidence disponibile al rispettivo decision boundary.

### DLC-CORR-10 — Provenance/version integrity + REVIEW completion — P1

**Origine:** Codex DLC-REV-P1-09 e DLC-REV-P1-10.

**Decisione:** MERGED / ACCEPTED_WITH_REFORMULATION.

Aggiungere:

```text
lifecycle_event_id
decision_version
plan_version
commitment_version
repair_id
review_version
created_at_transition_id
completed_at_transition_id?
parent_version_id?
```

`REVIEW_READY` significa “pronto per review”, non “review completata”.

Introdurre guardia:

```text
REVIEW_READY → DECISION_OPEN
only if review_status == COMPLETE
and review_id exists
```

Per `CAUSAL_OR_COUNTERFACTUAL_ANALYSIS`, se presente, richiedere:

```text
analysis_method
comparator_or_counterfactual
evidence_window
assumptions
limitations
```

Se tali elementi non esistono, classificare l'analisi come `DESCRIPTIVE_DIAGNOSTICS`.

Il DLC non obbliga a produrre causal analysis.

### DLC-CORR-11 — Diagrammi, REACT wording e reason codes — P2

**Origine:** Antigravity FND-DLC-03/FND-DLC-04; Codex DLC-REV-P2-01/P2-02.

**Decisione:** MERGED / ACCEPTED.

Aggiornare Mermaid alla transition table finale.

REACT deve distinguere:
- eventi che aggiornano evidence e guard evaluation;
- decisioni esplicite del MODEL_SPEC che possono autorizzare cancel/supersede.

Reason codes devono distinguere chiaramente pre-commit e post-commit.

## 4. Finding disposition summary

```text
ANTIGRAVITY:
FND-DLC-01 -> MERGED INTO DLC-CORR-02
FND-DLC-02 -> MERGED INTO DLC-CORR-01
FND-DLC-03 -> MERGED INTO DLC-CORR-05/11
FND-DLC-04 -> MERGED INTO DLC-CORR-04/11

CODEX:
DLC-REV-P0-01 -> DLC-CORR-01
DLC-REV-P1-01 -> DLC-CORR-03
DLC-REV-P1-02 -> DLC-CORR-02
DLC-REV-P1-03 -> DLC-CORR-04
DLC-REV-P1-04 -> DLC-CORR-05
DLC-REV-P1-05 -> DLC-CORR-06
DLC-REV-P1-06 -> DLC-CORR-07
DLC-REV-P1-07 -> DLC-CORR-08
DLC-REV-P1-08 -> DLC-CORR-09
DLC-REV-P1-09 -> DLC-CORR-10
DLC-REV-P1-10 -> DLC-CORR-10
DLC-REV-P2-01 -> DLC-CORR-11
DLC-REV-P2-02 -> DLC-CORR-11
```

## 5. Rejected reviewer formulations

Non vengono adottate come regole canoniche:

1. `COMPLETED` prevale automaticamente se un output è “integralmente acquisito”: troppo dipendente dalla semantica agent-specific dell'output.
2. Cancellation/supersession richiedono necessariamente un invalidator pre-dichiarato: troppo restrittivo; devono invece essere policy-governed, versionate e auditabili.
3. Ogni feasibility deve sempre eseguire tutte le classi di check Foundation: eccessivamente prescrittivo; le classi sono obbligatorie quando applicabili e devono essere dichiarate/N.A.

## 6. Gate di riconciliazione

```text
FOUNDATION_REOPEN_REQUIRED: NO

CANONICAL_CORRECTIONS: 11
P0_CANONICAL: 1
P1_CANONICAL: 9
P2_CANONICAL: 1

DLC_CORRECTION_SET_READY: YES
DLC_DRAFT_02_AUTHORIZED: YES

DECISION_LIFECYCLE_FREEZE: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
