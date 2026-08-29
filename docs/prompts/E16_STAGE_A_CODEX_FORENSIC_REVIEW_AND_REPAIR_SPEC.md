# E16-A — INDEPENDENT FORENSIC REVIEW + REPAIR SPECIFICATION — CODEX

## Ruolo

Agisci come **independent forensic reviewer** dell'implementazione e dell'evidenza E16-A.

Devi verificare in modo indipendente la diagnosi prodotta da Antigravity sui 28 episodi E16 Stage A e preparare una **repair specification minimale e verificabile**.

Non sei autorizzato a:
- ridisegnare E16-A;
- eseguire nuovi training run;
- eseguire Stage B;
- modificare MODEL_SPEC;
- reinterpretare automaticamente i risultati contaminati come training evidence valida;
- correggere il codice prima di aver concluso la review forense e classificato l'evidenza.

L'obiettivo è stabilire con precisione:

1. quali difetti sono realmente presenti;
2. quali risultati E16-A sono ancora validi;
3. quali risultati sono contaminati o invalidi;
4. quale repair minimale serve;
5. se, dopo il repair, E16-A debba essere replicato integralmente con lo stesso frozen DOE.

---

# 1. FONTI OBBLIGATORIE

Leggi integralmente:

```text
docs/experiment_designs/e16/E16_TRAINING_DESIGN_FROZEN.md
docs/prompts/E16_IMPLEMENTATION_PROMPT.md
docs/prompts/E16_STAGE_A_EXECUTION_ANTIGRAVITY.md
results/e16/manifests/E16_IMPLEMENTATION_MANIFEST.json
results/e16/instrumentation/E16_E0_REPORT.md
results/e16/stage_a/E16_STAGE_A_RUN_MANIFEST.json
results/e16/analysis/E16_STAGE_A_ANALYSIS.md
results/e16/analysis/E16_STAGE_B_GATE.json
results/e16/analysis/E16_STAGE_A_FORENSIC_DIAGNOSIS.md
```

Poi ispeziona almeno:

```text
results/e16/manifests/E16_TREATMENT_BUILD.py
src/agricola/e16/policy.py
src/agricola/e16/runner.py
src/agricola/e16/telemetry.py
src/agricola/e16/analysis.py
src/agricola/e16/config.py
tests/test_e16_policy.py
tests/test_e16_telemetry.py
tests/test_e16_analysis.py
tests/test_e16_config.py
```

Analizza inoltre i raw episode JSON e i relativi event ledger `*.events.jsonl` per campioni rappresentativi e, dove necessario, per tutte le 28 esecuzioni.

---

# 2. BASELINE DI INTEGRITÀ

Prima della review verifica e riporta:

```text
TREATMENT_BUILD_SHA256 =
8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e

CONFIG_SHA256 =
4c6ca43025d5a95acd6b2c8c5eb51a17a4bc4cadd672146055c317d54864ec92

OPPONENT_SHA256 =
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Conferma inoltre:

```text
28/28 Stage A episodes present
2 frozen seeds only
2 seats per cell/seed
7 Stage A cells only
0 post-freeze treatment substitutions
```

Se questa baseline non è verificabile, segnala il problema ma continua la review forense fin dove possibile.

---

# 3. CLAIM ANTIGRAVITY DA VERIFICARE INDIPENDENTEMENTE

Non assumere che siano corretti. Devi provarli o falsificarli.

## Claim F1 — Watering semantics

Antigravity sostiene:

```text
watering_dispatch_priority
```

sia implementato come quota:

```text
ceil(priority * watering_needs)
```

e quindi non come vera priorità di dispatch.

Verifica:

- formula esatta;
- punto del codice;
- significato operativo;
- se LOW/MID/HIGH definiscono un sottoinsieme quantitativo di crop da servire;
- se una quota `(1-p)` viene esclusa deliberatamente ogni ciclo;
- se esiste rotazione/fairness fra crop esclusi;
- se il comportamento può produrre drought mortality anche senza overload di workforce;
- se la semantica è coerente o incoerente con il trattamento frozen.

Classifica:

```text
CONFIRMED
PARTIALLY_CONFIRMED
REFUTED
UNRESOLVED
```

---

## Claim F2 — Event ledger / player attribution

Antigravity sostiene che esista un difetto per cui eventi unit-action siano registrati con:

```text
player = -1
```

o comunque non associati correttamente al treatment seat, contaminando:

```text
watering_execution_rate
watering_continuity
```

Verifica:

- schema event ledger;
- binding fra farm/player/unit;
- origine di `player = -1`;
- se riguarda WATER soltanto o tutte le unit actions;
- se riguarda treatment, opponent o entrambi;
- se la derivazione delle metriche filtra erroneamente questi eventi;
- ampiezza della distorsione;
- se è possibile ricostruire ex post le metriche corrette dai raw events senza nuovi run;
- se il bug compromette solo osservabilità/analysis oppure anche il comportamento della policy.

Classifica separatamente:

```text
BEHAVIORAL_IMPACT
OBSERVABILITY_IMPACT
ANALYSIS_IMPACT
```

---

## Claim F3 — Day-0 capital exhaustion at crop target 25

Antigravity sostiene che A03/A06 arrivino al cash floor `$300` per espansione iniziale eccessiva, con successivo stall operativo.

Verifica:

- sequenza temporale delle spese;
- saldo prima/dopo le operazioni principali;
- causalità prossima del floor;
- se il floor è conseguenza diretta del crop target o di altre azioni confondenti;
- se A04 differisce per capacità operativa o solo per cash-flow successivo;
- se il risultato è replicato su entrambi seed e seat;
- se questo segnale resta interpretabile anche in presenza dei difetti F1/F2.

Classifica:

```text
VALID_TRAINING_EVIDENCE
PARTIALLY_SALVAGEABLE
CONTAMINATED
INVALID
```

---

# 4. RICOSTRUZIONE DEL TRATTAMENTO REALE

Per ogni cella A01-A07, ricostruisci la differenza fra:

```text
ASSIGNED_TREATMENT
IMPLEMENTED_TREATMENT
REALIZED_TREATMENT
OBSERVED_METRIC
```

Usa una tabella con almeno:

```text
cell_id
crop_target
assigned_watering_priority
implemented_watering_rule
realized_water_requests
realized_water_successes
reconstructed_execution_rate
reported_execution_rate
crop_target_attainment
final_money
evidence_class
```

Se una metrica non è ricostruibile con sufficiente affidabilità, scrivi `UNOBSERVABLE`.

---

# 5. EVIDENCE SALVAGE CLASSIFICATION

Classifica ogni principale conclusione E16-A come:

```text
VALID
PARTIALLY_SALVAGEABLE
CONTAMINATED
INVALID
```

Valuta almeno:

```text
A02 - A01 final_money contrast
A04 - A03 final_money contrast
primary interaction
crop target 17 working-region signal
crop target 25 cash-floor signal
watering_execution_rate gate
watering_continuity gate
crop_target_attainment gate
C_STAR = NONE
Stage B blocking decision
```

Per ogni voce indica:

```text
classification
reason
affected defect
can_be_recomputed_without_rerun
safe_for_model_update
```

Non usare una conclusione contaminata per aggiornare threshold del MODEL_SPEC.

---

# 6. DISTINZIONE OBBLIGATORIA DEI TRE LIVELLI

Produci una valutazione separata di:

## MODEL_VALIDITY

Domanda:

```text
le relazioni teoriche testate restano supportate, falsificate o non interpretabili?
```

## POLICY_REALIZATION

Domanda:

```text
la policy implementa il trattamento scientificamente assegnato?
```

## IMPLEMENTATION_FIDELITY

Domanda:

```text
runner, telemetry e analysis misurano correttamente ciò che è realmente accaduto?
```

Per ciascuno usa:

```text
PASS
PASS_WITH_LIMITATIONS
FAIL
UNRESOLVED
```

e motivazione verificabile.

---

# 7. REPAIR SPECIFICATION — SOLO DOPO LA REVIEW

Solo dopo aver completato la classificazione forense, prepara una repair specification minimale.

Non implementarla ancora.

Per ogni repair richiesto specifica:

```text
repair_id
defect
files_affected
required_behavior
forbidden_behavior
acceptance_test
regression_test
impact_on_frozen_semantics
requires_new_treatment_hash: YES/NO
requires_new_config_hash: YES/NO
```

Considera almeno:

### R1 — Watering treatment semantics

Definisci quale implementazione realizza davvero il significato frozen di:

```text
watering_dispatch_priority
```

Se il frozen design è semanticamente ambiguo, non scegliere arbitrariamente: segnala il blocker e proponi la correzione testuale minima necessaria prima del codice.

### R2 — Event ledger attribution

Definisci come ogni unit action deve essere associata inequivocabilmente a:

```text
player
seat
unit
cell
seed
step
```

### R3 — Derived watering metrics

Definisci formule e test per:

```text
watering_execution_rate
watering_continuity
```

incluse invarianti e casi sintetici.

---

# 8. TEST DI ACCETTAZIONE DEL REPAIR

La specification deve prevedere almeno:

1. unit test sulla semantica LOW/MID/HIGH;
2. test che HIGH non significhi automaticamente esclusione permanente del 30% delle crop needs, salvo che il frozen design dica esplicitamente questo;
3. test di fairness/coverage se la policy usa budget parziale;
4. test `player != -1` per unit actions attribuibili;
5. test trattamento P0 e P1;
6. test opponent P0 e P1;
7. test di ricostruzione WATER requested/executed;
8. synthetic episode con execution rate noto;
9. synthetic continuity noto;
10. regression test che impedisca il ritorno del bug;
11. E0 instrumentation gate aggiornato;
12. hash verification del nuovo treatment artifact.

---

# 9. DECISIONE SULLA REPLICATION

Concludi scegliendo una sola delle seguenti:

```text
REPLICATION_NOT_REQUIRED
PARTIAL_REPLICATION_SUFFICIENT
FULL_STAGE_A_CORRECTED_REPLICATION_REQUIRED
BLOCKED_PENDING_SEMANTIC_CLARIFICATION
```

Criterio:

se il trattamento WATER originariamente assegnato non è stato realmente implementato, la default recommendation deve essere:

```text
FULL_STAGE_A_CORRECTED_REPLICATION_REQUIRED
```

salvo prova forte che le quantità rilevanti possano essere ricostruite senza introdurre bias sperimentale.

Se raccomandi replica completa:

- mantieni lo stesso DOE Stage A;
- stesse 7 celle;
- stessi 2 seed;
- stesso seat swap;
- stesso frozen opponent;
- nessun Stage B;
- distingui chiaramente i nuovi run come corrected replication;
- non sovrascrivere i 28 run originali.

Nome candidato:

```text
E16-A-R1
```

Non autorizzare comunque l'esecuzione in questa fase.

---

# 10. VERSIONING / PROVENANCE

Se il repair modifica il comportamento del treatment build:

```text
NEW_TREATMENT_BUILD_SHA256_REQUIRED = YES
```

Il vecchio hash:

```text
8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e
```

deve restare associato ai 28 run originali.

Non sovrascrivere:

```text
results/e16/stage_a/
```

Per una eventuale corrected replication prevedi uno spazio separato, ad esempio:

```text
results/e16/stage_a_r1/
```

Preserva integralmente la provenance dell'esperimento fallito/contaminato.

---

# 11. OUTPUT RICHIESTI

Crea:

```text
results/e16/analysis/E16_STAGE_A_CODEX_FORENSIC_REVIEW.md
docs/experiment_designs/e16/E16_IMPLEMENTATION_REPAIR_SPEC.md
```

Non modificare codice operativo in questa fase.

Non eseguire nuovi episodi.

---

# 12. REPORT FINALE

Concludi esattamente con una sezione sintetica del tipo:

```text
FORENSIC_REVIEW_STATUS: COMPLETE | BLOCKED

F1_WATERING_SEMANTICS:
  STATUS: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | UNRESOLVED
  IMPACT: ...

F2_LEDGER_ATTRIBUTION:
  STATUS: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | UNRESOLVED
  BEHAVIORAL_IMPACT: ...
  OBSERVABILITY_IMPACT: ...
  ANALYSIS_IMPACT: ...

F3_CASH_FLOOR:
  STATUS: CONFIRMED | PARTIALLY_CONFIRMED | REFUTED | UNRESOLVED
  EVIDENCE_CLASS: ...

MODEL_VALIDITY: PASS | PASS_WITH_LIMITATIONS | FAIL | UNRESOLVED
POLICY_REALIZATION: PASS | PASS_WITH_LIMITATIONS | FAIL | UNRESOLVED
IMPLEMENTATION_FIDELITY: PASS | PASS_WITH_LIMITATIONS | FAIL | UNRESOLVED

E16_A_EVIDENCE:
  VALID: ...
  PARTIALLY_SALVAGEABLE: ...
  CONTAMINATED: ...
  INVALID: ...

C_STAR_NONE_VALID: YES | NO | UNRESOLVED
STAGE_B_BLOCK_DECISION_VALID: YES | NO | UNRESOLVED

REPAIR_REQUIRED: YES | NO
REPAIR_IDS: ...

NEW_TREATMENT_BUILD_SHA256_REQUIRED: YES | NO
NEW_CONFIG_SHA256_REQUIRED: YES | NO

REPLICATION_DECISION:
  REPLICATION_NOT_REQUIRED |
  PARTIAL_REPLICATION_SUFFICIENT |
  FULL_STAGE_A_CORRECTED_REPLICATION_REQUIRED |
  BLOCKED_PENDING_SEMANTIC_CLARIFICATION

PROPOSED_REPLICATION_ID: E16-A-R1 | NONE

NEW_RUNS_EXECUTED: 0
STAGE_B_EXECUTED: NO

FILES_CHANGED:
  results/e16/analysis/E16_STAGE_A_CODEX_FORENSIC_REVIEW.md
  docs/experiment_designs/e16/E16_IMPLEMENTATION_REPAIR_SPEC.md
```

Il task termina qui.

Non implementare il repair.
Non eseguire E16-A-R1.
Non eseguire Stage B.
