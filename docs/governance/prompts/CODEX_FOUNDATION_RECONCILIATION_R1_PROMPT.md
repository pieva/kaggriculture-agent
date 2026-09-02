# Kaggriculture — Codex Foundation Reconciliation R1

## Scopo

Questa sessione usa il residuo di crediti Codex esclusivamente per una **reconciliation tecnica delle due review indipendenti** prodotte da Antigravity e Copilot sulla Foundation C1.

Non è una sessione di implementazione, tuning, progettazione di treatment o modifica degli artefatti foundation.

Il compito è stabilire, usando le review come input principale e verificando nel repository solo quando necessario, quali finding siano convergenti, complementari, realmente in conflitto, non supportati, già risolti dai documenti C1, bloccanti per il freeze oppure semplici miglioramenti documentali.

## Artefatti da leggere

Leggi integralmente:

- `docs/governance/foundation/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md`
- `docs/governance/foundation/antigravity/ANTIGRAVITY_FOUNDATION_EVIDENCE_MATRIX.csv`
- `docs/governance/foundation/copilot/COPILOT_FOUNDATION_REVIEW_R1.md`

Per la verifica dei finding puoi consultare, quando necessario:

- `docs/foundation/ontology/ONTOLOGY.md`
- `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C1.md`
- `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C1.md`
- i MODEL_SPEC correnti/frozen/consolidati già presenti nel repository;
- il runtime Copilot solo per verificare affermazioni già formulate nella sua review;
- engine/schema/diagnostics E16 già presenti, ma **solo in modo mirato** per dirimere una specifica divergenza.

NON effettuare una nuova analisi sistematica dell'engine.

## Stato da preservare

La foundation resta:

```text
CANDIDATE C1
NOT FROZEN
```

Non modificare Ontologia, State Machine, Feature Model, MODEL_SPEC, policy, configurazioni, risultati E16, frozen artifacts o runtime. Non eseguire nuovi episodi o benchmark.

## Domanda primaria

Le due review sembrano divergere sul freeze:

- Antigravity: `STATE_MACHINE_C1 = ACCEPT`, `FEATURE_MODEL_C1 = ACCEPT`, con revisione materiale soprattutto di Ontologia e MODEL_SPEC.
- Copilot: `DO_NOT_FREEZE_FOUNDATION_C1`, con 3 P0 e 6 P1 che richiedono anche maggiore precisione in State Machine/Feature Model e nel contratto MODEL_SPEC↔runtime.

Determina se questa divergenza è:

1. un vero conflitto fattuale;
2. una differenza di criterio di freeze;
3. oppure una combinazione delle due.

Non fare media o majority vote: risolvi contro le evidenze.

## Reconciliation obbligatoria

Costruisci una matrice finding-by-finding che includa almeno:

```text
reconciliation_id
tema
finding_antigravity
finding_copilot
artefatti_interessati
relationship:
  CONVERGENT
  COMPLEMENTARY
  CONFLICT
  PARTIAL_OVERLAP
  UNIQUE_SUPPORTED
  UNIQUE_UNSUPPORTED
evidence_status
technical_resolution
freeze_impact:
  BLOCKER
  REQUIRED_BEFORE_FREEZE
  NON_BLOCKING
recommended_artifact_change
```

### Finding Antigravity da coprire

- `FND-01` maturity / `first_yield_day`
- `FND-02` `tile_lifecycle_state`
- `FND-03` `crop_decay_risk_window`
- `FND-04` `contract_inventory_loss`
- `FND-05` ontology mapping gaps
- `FND-06` worker multi-occupancy/collision
- `FND-07` FERTILIZE
- `FND-08` FEED+CARE bonus
- `FND-09` `ENGINE_OBSERVABLE != TELEMETRY_OBSERVED`
- `FND-10` rejection deterministic `time_to_random_weed`

### Finding Copilot da coprire

- `P0-01` authoritative MODEL_SPEC consumer ambiguity
- `P0-02` MODEL_SPEC overstates executable feature consumption
- `P0-03` surface/capacity concepts used before canonical formulas
- `P1-01` executable precedence for `tile_lifecycle_state`
- `P1-02` authoritative clock contract
- `P1-03` `tile_need` vs `action_eligible_now` vs `serviceable_before_deadline`
- `P1-04` aggregate contracts
- `P1-05` market/inventory provenance
- `P1-06` MODEL_SPEC vs active Copilot runtime/delegated thresholds

## Questioni da arbitrare esplicitamente

### 1. State Machine C1: ACCEPT o REVISE?

Antigravity la considera corretta e engine-verified.

Copilot non contesta in generale le meccaniche, ma sostiene che manchino classifier eseguibile/precedence, authoritative clock contract e distinzione tra tile need, action eligibility e serviceability.

Stabilisci per ognuno se è:
- errore della State Machine;
- requisito del Feature Model;
- requisito del MODEL_SPEC/policy;
- oppure requisito di documentazione/validation contract.

### 2. Feature Model C1: ACCEPT o REVISE?

Verifica in particolare:

- `current_MODEL_SPEC_usage`: deve restare nel Feature Model comune?
- È corretto rinominarlo solo a `codex_e15_frozen_usage`, oppure sarebbe metodologicamente più pulito spostare il consumo in una **versioned MODEL_SPEC consumer matrix esterna**?
- Le feature `CONDITIONAL`/`PARTIALLY_KNOWN` possono restare nel Feature Model anche se non hanno formula canonica?
- Quale regola deve valere quando un MODEL_SPEC dichiara `USED/FULL` per una feature non completamente computabile?

### 3. MODEL_SPEC ↔ runtime

Valuta il principio proposto da Copilot:

```text
MODEL_SPEC says USED
    !=
runtime demonstrably consumes the feature
```

Stabilisci se il futuro contratto deve distinguere:

```text
POLICY_INPUT
RUNTIME_DERIVED
POST_ACTION_TELEMETRY
OUTCOME_ONLY
```

e se questa tassonomia appartenga al Feature Model, a una consumer matrix o al MODEL_SPEC.

### 4. Aggregate contract

Valuta se ogni aggregate usato da MODEL_SPEC/policy gate debba avere formalmente:

```text
scope
sampling phase
window
numerator
denominator
zero-denominator convention
deduplication key
source class
formula version
boundary examples
```

Distingui requisito necessario per freeze da perfezionamento utile.

### 5. Nuove evidenze engine Antigravity

Verifica se sono sufficientemente fondate per modificare C2:

- worker multi-occupancy consentita;
- `FERTILIZE` deterministic lifecycle / `fertilized_until_day`;
- Care Bonus congiunto `FEED + CARE`;
- `contract_inventory_loss` come shed overflow automatico.

Non ampliare l'analisi oltre quanto necessario.

## Output richiesto

Crea esclusivamente:

`docs/governance/foundation/reconciliation/CODEX_FOUNDATION_RECONCILIATION_R1.md`

Il report deve essere in italiano.

Struttura minima:

1. Executive verdict.
2. Divergenza reale vs differenza di freeze criterion.
3. Reconciliation matrix completa.
4. Decisione sui 3 P0 Copilot.
5. Decisione sui finding Antigravity unici.
6. Classificazione finale dei quattro artefatti:

```text
ONTOLOGY:
  ACCEPT | REVISE_LIGHT | REVISE_MAJOR | REJECT

STATE_MACHINE_C1:
  ACCEPT | REVISE_LIGHT | REVISE_MAJOR | REJECT

FEATURE_MODEL_C1:
  ACCEPT | REVISE_LIGHT | REVISE_MAJOR | REJECT

MODEL_SPEC:
  ACCEPT | REVISE_LIGHT | REVISE_MAJOR | REJECT
```

7. Freeze verdict:

```text
FREEZE_ALLOWED
FREEZE_AFTER_TARGETED_CORRECTIONS
FOUNDATION_C2_REQUIRED
FOUNDATION_REDESIGN_REQUIRED
```

8. Elenco preciso delle modifiche da portare nel prossimo Foundation Tournament, separate in MUST, SHOULD, DEFER.
9. Identifica esplicitamente i punti che **non richiedono** ulteriori analisi o esperimenti.
10. Se restano vere dispute tecniche non risolvibili con gli artefatti esistenti, elencale come `UNRESOLVED_EVIDENCE_GAP`; non avviare nuovi esperimenti.

## Principi metodologici

- Nessuna modifica deve essere proposta solo per “far convergere” le review.
- `NO_CHANGE` è un esito valido.
- Un concetto incompleto può rimanere nel Feature Model come `PARTIALLY_KNOWN`, ma non può essere trasformato implicitamente in una feature operativa completa da un MODEL_SPEC senza contratto.
- Una telemetry post-action non è automaticamente una feature decisionale online.
- Un requisito di logging non deve essere confuso con una regola dell'engine.
- Una condizione di tile non deve essere confusa con la possibilità operativa che un worker la serva in tempo.
- Distinguere sempre ENGINE, ONTOLOGY, STATE MACHINE, FEATURE MODEL, MODEL_SPEC, POLICY e TELEMETRY.

## Vincoli assoluti

- Nessuna modifica ai quattro artefatti foundation.
- Nessuna modifica a codice/policy/config.
- Nessun nuovo episodio.
- Nessun benchmark.
- Nessuna nuova analisi sistematica dell'engine.
- Nessun Foundation Tournament in questa sessione.
- Nessuna proposta di soglie/pesi ottimali.

Al termine mostra:

- file creato;
- numero di finding riconciliati;
- numero di convergenze/complementarità/conflitti;
- verdict sui quattro artefatti;
- freeze verdict;
- eventuali `UNRESOLVED_EVIDENCE_GAP`;
- `git status --short`.

Poi **FERMATI**.
