# Codex — Independent Review of FEATURE MODEL C2

## Obiettivo

Eseguire una **review indipendente e mirata** del candidato:

```text
docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
```

prima di autorizzare la costruzione dei MODEL_SPEC C2.

Questa NON è una nuova reconciliation generale e NON è un mandato per riscrivere il Feature Model.

Obiettivo: verificare che il Feature Model C2 prodotto da Copilot sia un contratto informativo:

- semanticamente corretto;
- consumer-neutral;
- computazionalmente preciso dove dichiarato;
- epistemicamente prudente dove incompleto;
- coerente verticalmente con Ontology C2 e State Machine C2;
- pronto, oppure no, a diventare upstream dei MODEL_SPEC C2.

Non modificare MODEL_SPEC, runtime, policy, training o telemetry implementation.

---

# 1. Fonti obbligatorie

Leggere integralmente:

```text
docs/model/ontology/ONTOLOGY_C2.md
docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C1.md
docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md

docs/model/reviews/reconciliation/CODEX_FOUNDATION_RECONCILIATION_R1.md
docs/model/reviews/copilot/COPILOT_FOUNDATION_REVIEW_R1.md
docs/model/reviews/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md
```

Consultare il codice engine/runtime solo quando necessario per verificare una specifica affermazione del C2.

La `CODEX_FOUNDATION_RECONCILIATION_R1.md` resta l'arbitrato normativo precedente.

---

# 2. Output

Creare:

```text
docs/model/reviews/codex/CODEX_FEATURE_MODEL_C2_REVIEW_R1.md
```

Se `docs/model/reviews/codex/` non esiste, crearlo.

Non modificare `KAGGRICULTURE_FEATURE_MODEL_C2.md` durante la review.

Il report deve concludere con uno dei verdict:

```text
ACCEPT
ACCEPT_WITH_LOCAL_FIXES
REVISE_MAJOR
```

e separatamente:

```text
MODEL_SPEC_C2_UPSTREAM_READY: YES | AFTER_LOCAL_FIXES | NO
```

---

# 3. Review question A — Le 74 feature sono legittime?

C1 conteneva 59 elementi:

```text
19 RAW_OBSERVABLE
34 DERIVED_FEATURE
2 POLICY_CONTEXT
3 TELEMETRY_ONLY
1 OUTCOME_LABEL
```

Il report Copilot dichiara per C2:

```text
12 ENGINE_STATE
18 RAW_OBSERVABLE
26 DERIVED_FEATURE
6 POLICY_CONTEXT
9 TELEMETRY_ONLY
3 OUTCOME_LABEL
TOTAL 74
```

Auditare l'incremento 59 -> 74.

Per ogni elemento nuovo o semanticamente splittato determinare se è realmente:

```text
FEATURE / INFORMATION OBJECT
```

oppure se appartiene più propriamente a:

```text
EVENT-SCHEMA FIELD
PROVENANCE FIELD
CONSUMER-MATRIX FIELD
DIAGNOSTIC RECORD
POLICY MEMORY
OUTCOME / LABEL
```

Non assumere che ogni campo necessario alla telemetria debba diventare una feature del catalogo.

Produrre una tabella:

```text
feature_id
C1/C2 origin
C2 class
legitimate_catalog_member YES/NO/CONDITIONAL
reason
recommended_action
```

per tutti gli elementi ADDED/SPLIT/RECLASSIFIED rilevanti.

Controllare in particolare perché:

```text
TELEMETRY_ONLY: 3 -> 9
OUTCOME_LABEL: 1 -> 3
POLICY_CONTEXT: 2 -> 6
```

e verificare che non vi sia over-expansion del catalogo.

---

# 4. Review question B — Lifecycle classifier realmente totale?

Verificare il classifier C2 per:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

Il classifier deve essere:

- deterministico;
- totale per input validi;
- semanticamente coerente con Ontology C2;
- coerente con le transizioni State Machine C2;
- privo di leakage;
- implementabile senza interpretazione.

Verificare esplicitamente:

```text
LOCKED
outside working set
None inside working set
WEED
PLANT immature with yield_units > 0
PLANT mature with yield_units > 0
ongoing immediately after valid HARVEST
ongoing before future scheduled production
ongoing after final useful production
non-ongoing before maturity
invalid/missing telemetry input
```

## RETIREMENT_DUE

Prestare particolare attenzione alla definizione.

Verificare che sia derivabile da:

- crop type/rules;
- planted_day;
- current day/phase;
- production schedule;
- current tile state;

senza usare informazione futura non disponibile.

Distinguere:

```text
known static future production schedule
```

da:

```text
future outcome
```

Il primo può essere decision-time derivable; il secondo sarebbe leakage.

Se il classifier usa precedence, verificare che non mascheri sovrapposizioni semantiche non risolte.

---

# 5. Review question C — Aggregate contract vs formula completeness

Questa è una verifica critica.

Il Feature Model C2 può definire uno **schema completo di contratto** senza avere una **formula congelabile** per ogni aggregate.

Verificare che il documento distingua esplicitamente:

```text
CONTRACT_SCHEMA_COMPLETE
```

da:

```text
FEATURE_FORMULA_COMPLETE
```

e che nessun aggregate incompleto venga presentato come freeze-ready solo perché possiede campi contract.

Auditare almeno:

```text
active_crop_surface
crop_surface_maintained
watering_execution
continuity
care_completion
harvest_action_flow
cleanliness
weed_backlog_cost
workforce_capacity
movement_overhead
dispatch_failure
productive_action_share
state_capacity_alignment
operating_cash_buffer
```

Per ciascuno riportare:

```text
feature_id
contract schema complete?
formula complete?
denominator canonical?
sampling phase defined?
dedup defined?
online computable?
freeze-ready?
missing evidence/definition
```

Regola:

```text
formula incomplete => NOT FREEZE-READY
```

anche se lo schema del contratto è completo.

Controllare soprattutto:

```text
state_capacity_alignment
crop_surface_maintained
operating_cash_buffer
care_completion
productive_action_share
```

---

# 6. Review question D — Consumer-neutrality reale

Verificare che C2 non contenga residui normativi di:

```text
current_MODEL_SPEC_usage
Codex E15 frozen consumer
Copilot runtime
Antigravity runtime
```

come proprietà intrinseche delle feature.

Lo storico può essere conservato solo se chiaramente etichettato come:

```text
historical consumer evidence
```

e non come semantica del Feature Model.

Verificare che la futura consumer matrix sia esterna.

Controllare che il Feature Model non affermi implicitamente:

```text
USED
FULL
NOT_USED
```

senza nominare un consumer versionato.

---

# 7. Consumer-neutral runtime mapping: chiarimento

Il report Copilot indica tra i blocker:

```text
assenza di un vero consumer-neutral mapping eseguibile del runtime
```

Valutare questa frase.

L'architettura approvata prevede:

```text
FEATURE MODEL = consumer-neutral
CONSUMER MATRIX = consumer-specific
RUNTIME TRACE = consumer-specific
```

Quindi l'assenza di un mapping runtime direttamente nel Feature Model:

- NON deve essere classificata come difetto intrinseco del Feature Model;
- PUÒ essere classificata come freeze exit criterion downstream della Foundation C2.

Esplicitare il verdetto su questo punto.

---

# 8. Clock / phase

Verificare che:

```text
engine_step
```

e:

```text
canonical_step = day * turnsPerDay + hour
```

siano distinti correttamente.

Controllare tutte le feature temporali rilevanti, soprattutto:

```text
harvest_ready
care_due
water_loss_at_eod_if_unserved
action_phases_until_eod_refresh
lifespan_decay_started
next_lifespan_decay_phase
lifespan_loss_phase_if_no_action
fertilizer_effect_window
livestock production timing
```

Verificare:

- authoritative clock;
- sampling phase;
- pre/post-action availability;
- no future leakage.

Non assumere equivalenza fra engine_step e canonical_step.

---

# 9. HARVEST readiness

Verificare il predicato:

```text
tile.kind == "PLANT"
AND tile.yield_units > 0
AND day - tile.planted_day >= CROPS[tile.crop].first_yield_day
```

e che nessuna feature/aggregate C2 reintroduca implicitamente:

```text
yield_units > 0 => harvestable
```

Verificare ongoing e non-ongoing.

---

# 10. Crop decay risk

Verificare che restino causalmente separati:

```text
missed-WATER deterministic risk
lifespan deterministic risk
EMPTY random-WEED eligibility/hazard
```

Il Feature Model deve continuare a rifiutare:

```text
time_to_random_weed
```

come countdown deterministico.

---

# 11. Need / eligibility / serviceability

Verificare la distinzione:

```text
tile_need
action_eligible_now
serviceable_before_deadline
```

In particolare `serviceable_before_deadline`:

- non deve significare garanzia;
- deve restare `PARTIALLY_KNOWN` finché routing, scheduling, inventory, contention, action phase e policy memory non sono completamente contrattualizzati;
- non deve essere usato come aggregate freeze-ready o gate operativo se la formula non è completa.

---

# 12. Workforce / inventory / market provenance

Verificare che C2 separi correttamente:

## Workforce

```text
position
headcount
multi-occupancy
capacity
movement
dispatch
serviceability
```

senza inferire serviceability dalla co-location.

## Inventory

```text
worker inventory
shed inventory
seed inventory
shed capacity
automatic EOD transfer
shed_overflow_eod_loss
```

senza falso obbligo di rientro worker.

## Market

```text
displayed_quote
requested_quantity
executed_quantity
realized_price
cash_delta
estimate
```

senza usare dati post-action come input pre-action dello stesso step.

---

# 13. TELEMETRY_ONLY e OUTCOME_LABEL

Auditare i 9 `TELEMETRY_ONLY` e 3 `OUTCOME_LABEL`.

Verificare che:

- siano davvero informazioni concettualmente utili al Feature Model;
- non siano semplicemente colonne dell'event schema;
- non siano decision-time features;
- non siano duplicate.

Prestare attenzione almeno a:

```text
MKT-02
GLB-02
GLB-03
LBL-01
```

e ai nuovi elementi aggiunti in C2.

Se un elemento appartiene solo al contratto telemetry, raccomandare di spostarlo fuori dal catalogo feature.

---

# 14. POLICY_CONTEXT

Auditare l'aumento:

```text
2 -> 6
```

Verificare che ogni POLICY_CONTEXT rappresenti realmente contesto necessario per derivare/interpretare una feature comune e non una scelta specifica di un consumer.

Il Feature Model può dipendere da contesto policy quando semanticamente necessario, per esempio working-set membership, ma non deve incorporare:

- soglie specifiche di una policy;
- target numerici specifici;
- learned weights;
- strategie AG/Codex/Copilot.

---

# 15. Coerenza verticale

Costruire una matrice sintetica:

```text
Ontology C2 concept
State Machine C2 state/transition
Feature Model C2 representation
status
issue
```

Non richiedere una biiezione.

`NONE_DIRECT` è valido.

Segnalare:

- feature senza semantic basis upstream;
- concetti upstream che necessitano una feature ma non la possiedono;
- duplicazioni;
- overaggregation;
- semantic drift.

---

# 16. Deviazione procedurale Copilot

Il mandato `COPILOT_FEATURE_MODEL_C2.md` richiedeva la lettura di:

```text
docs/model/reviews/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md
```

Il report Copilot afferma invece:

```text
ho rispettato anche il vincolo di non leggere la review Antigravity
```

ma tale vincolo non era presente nel mandato.

Verificare se questa omissione ha causato perdita di finding materiali.

Non penalizzare automaticamente il documento: classificare l'impatto reale come:

```text
NONE
MINOR
MATERIAL
```

La reconciliation Codex aveva già arbitrato entrambe le review, quindi valutare sostanza, non formalismo.

---

# 17. Classificazione findings

Usare:

```text
P0 BLOCKER
P1 MAJOR
P2 MINOR
NOTE
```

Un `P0` deve impedire:

```text
MODEL_SPEC_C2_UPSTREAM_READY: YES
```

Per ogni finding indicare:

```text
ID
severity
artifact/feature
claim
evidence
impact
required correction
```

---

# 18. Eventuali fix

NON modificare il Feature Model durante questa review.

Se il verdict è:

```text
ACCEPT_WITH_LOCAL_FIXES
```

fornire una lista di fix atomici, ordinati e sufficientemente precisi da poter essere applicati da un altro agente senza reinterpretazione.

Se emerge `REVISE_MAJOR`, spiegare perché l'architettura C2 non è ancora utilizzabile come upstream.

---

# 19. Verifiche repository

Eseguire:

```powershell
git diff --check
.\.venv\Scripts\pytest.exe
```

Se `ruff` è disponibile, eseguirlo ma distinguere problemi preesistenti/non correlati.

Mostrare:

```powershell
git status --short
```

Non eseguire episodi o benchmark.

Non fare commit.

---

# 20. Output finale

Il report deve includere:

1. executive verdict;
2. conteggio findings per severità;
3. audit 59 -> 74;
4. lifecycle classifier review;
5. aggregate-contract review;
6. consumer-neutrality review;
7. clock/phase review;
8. HARVEST/decay review;
9. need/eligibility/serviceability review;
10. workforce/inventory/market provenance;
11. TELEMETRY_ONLY / OUTCOME_LABEL audit;
12. POLICY_CONTEXT audit;
13. vertical consistency matrix;
14. impatto dell'omessa lettura review Antigravity;
15. lista fix richiesta;
16. freeze blockers;
17. test/check results;
18. repository status.

Chiudere esattamente con:

```text
FEATURE MODEL C2 REVIEW: COMPLETED
FEATURE MODEL C2 VERDICT: <ACCEPT | ACCEPT_WITH_LOCAL_FIXES | REVISE_MAJOR>
MODEL_SPEC_C2_UPSTREAM_READY: <YES | AFTER_LOCAL_FIXES | NO>
FOUNDATION C2: NOT FROZEN
```

STOP.

Non iniziare MODEL_SPEC C2.
