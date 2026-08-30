# C2 â€” REVIEW INDIPENDENTE DEL CODEX ENGINE CONTRACT / PERIOD LEDGER AUDIT

```text
PHASE: REVIEW
TASK_ID: C2-ENGINE-CONTRACT-INDEPENDENT-REVIEW
REVIEWERS: ANTIGRAVITY / COPILOT
INDEPENDENT_REVIEW: YES
FOUNDATION_MODIFICATION_AUTHORIZED: NO
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
CODE_MODIFICATION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Oggetto della review

Revisionare indipendentemente il documento congelato:

```text
results/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

Il documento Ã¨ stato prodotto da Codex come audit source-grounded dell'engine locale Kaggriculture.

Questa review NON deve:

- proporre una nuova strategia;
- modificare Ontology, Feature Model o State Machine;
- modificare MODEL_SPEC;
- modificare codice;
- fare tuning;
- eseguire tournament o Kaggle;
- reinterpretare i replay come fonte normativa;
- riscrivere l'audit per preferenza stilistica.

Lo scopo Ã¨ tentare di **falsificare** il contratto engine proposto da Codex prima che diventi input della revisione Foundation.

---

# 2. Vincolo di indipendenza

Ogni reviewer deve lavorare separatamente.

Non leggere:

- il feedback dell'altro reviewer;
- eventuali reconciliation successive;
- eventuali modifiche Foundation effettuate dopo l'audit.

Ãˆ consentito leggere:

1. `CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`;
2. il source engine locale fingerprintato dall'audit;
3. `kaggriculture.json`;
4. package metadata;
5. la Foundation C2 corrente, esclusivamente per controllare la discrepancy matrix;
6. i quattro replay citati dall'audit, esclusivamente per controllare la replay reconciliation.

La fonte normativa primaria resta il source engine.

---

# 3. Engine target

Verificare anzitutto che il runtime effettivamente disponibile corrisponda a quello dichiarato:

```text
ENGINE_PACKAGE: kaggle-environments
ENGINE_VERSION: package 1.32.7
ENVIRONMENT_VERSION: 0.1.0
ENGINE_SOURCE_ROOT:
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture

EXPECTED_AGGREGATE_SHA256:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

EXPECTED_KAGGRICULTURE_PY_SHA256:
bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
```

Se il fingerprint non coincide:

```text
ENGINE_IDENTITY_MATCH: NO
```

e distinguere chiaramente:

- errore dell'audit;
- runtime locale cambiato dopo l'audit;
- file aggiuntivo/mancante nel fingerprint;
- differenza irrilevante rispetto alle formule biologiche.

Non validare formule contro un engine differente senza segnalarlo.

---

# 4. Metodo di review

Per ogni affermazione importante dell'audit classificare:

```text
CONFIRMED
PARTIALLY_CONFIRMED
CONTRADICTED
AMBIGUOUS
NOT_REPRODUCED
OUT_OF_SCOPE
```

Per ogni `CONTRADICTED`, `AMBIGUOUS` o `NOT_REPRODUCED` fornire:

```text
CLAIM:
SOURCE_SYMBOL:
SOURCE_EVIDENCE:
REPRODUCTION:
IMPACT:
PROPOSED_CORRECTION:
SEVERITY:
```

Severity:

```text
P0 = engine contract materially wrong
P1 = semantic/modeling ambiguity capable of corrupting downstream Foundation
P2 = missing relevant fact
P3 = documentation/naming/provenance issue
```

Non usare consenso con Codex come prova.

---

# 5. Clock contract

Verificare indipendentemente:

- `step`;
- `turn`;
- `day`;
- `hour`;
- `turnsPerDay`;
- configurabilitÃ  di `turnsPerDay`;
- EOD trigger;
- formula `EOD_STEP(d)`;
- invariante:

```text
step == day * turnsPerDay + hour
```

negli stati engine validi;

- ordine action / decay / EOD / next-state;
- reset dei daily flags;
- replay serialization offset.

Controllare i tre boundary examples dell'audit:

1. azione allo step immediatamente precedente EOD;
2. azione al primo step del nuovo giorno;
3. plant/place e primo evento biologico.

Segnalare qualsiasi off-by-one.

---

# 6. Species inventory

Verificare direttamente `CROPS`, `ANIMALS`, `PRODUCTS` e action legality.

Confermare o falsificare:

```text
CROPS:
WHEAT
CARROT
TOMATO
STRAWBERRY
MELON

ANIMALS:
GOOSE
COW
SHEEP

CHICKEN:
NOT_SUPPORTED
```

Verificare inoltre:

```text
GOOSE -> COOP -> EGG
COW   -> PASTURE -> MILK
SHEEP -> PASTURE -> WOOL
```

Non inferire alias non presenti nel runtime.

---

# 7. Crop ledger

Controllare specie per specie:

```text
WHEAT
CARROT
TOMATO
STRAWBERRY
MELON
```

e verificare almeno:

- seed cost;
- origin semantics;
- first yield;
- max yield day;
- interval;
- ongoing/non-ongoing;
- max production count;
- initial yield;
- WATER legality e daily flag;
- consecutive unwatered;
- yield progression;
- fertilizer interaction;
- HARVEST legality;
- early HARVEST;
- max lifespan;
- decay;
- WEED transition;
- inventory transfer.

Verificare esplicitamente le formule origin-relative e ogni boundary `d0 + n`.

Controllare che l'audit distingua correttamente:

```text
ENGINE BIOLOGICAL EVENT
LEGAL WINDOW
POLICY HARVEST CHOICE
```

---

# 8. Animal ledger

Controllare separatamente:

```text
GOOSE
COW
SHEEP
```

Verificare:

- purchase cost;
- required structure;
- max held;
- placement;
- first output day;
- interval;
- base output;
- yield cap;
- FEED;
- CARE;
- `pending_care_bonus`;
- `consecutive_unfed`;
- escape;
- fertilizer generation;
- daily reset;
- product collection;
- fertilizer collection.

---

# 9. P0 specifico â€” FEED / CARE / animal production

Tentare esplicitamente di falsificare:

```text
An animal on a scheduled production day produces base output = 1
when fed_today == FALSE, provided it has not escaped.
```

Verificare l'ordine:

```text
unfed counter
-> escape check
-> scheduled production
-> base output
-> consumption of pending care bonus
-> accumulation of new care bonus
-> fertilizer availability
-> daily reset
```

Riprodurre almeno una matrice minima per una specie con:

```text
fed + cared
fed + not cared
not fed + cared
not fed + not cared
```

e verificare se la stessa logica Ã¨ condivisa da GOOSE/COW/SHEEP.

Verificare anche il caso:

```text
consecutive_unfed == 1
fed_today == FALSE
```

al momento EOD.

---

# 10. P0 specifico â€” Fertilizer

Tentare di falsificare:

```text
BASE_INCREMENT_TOTAL = 1
FERTILIZED_INCREMENT_TOTAL = 2
FERTILIZER_UPLIFT = +1
```

Verificare:

- origine da animale;
- flag boolean;
- mancato stacking sull'animale;
- raccolta;
- applicazione;
- `current_day + 2`;
- inclusivitÃ  della finestra;
- repeated application;
- crop non-ongoing;
- crop ongoing;
- dipendenza da WATER;
- cap;
- assenza di accelerazione del biological clock.

Controllare almeno un esempio WHEAT e uno STRAWBERRY/TOMATO.

---

# 11. P0 specifico â€” Inventory / overflow

Tentare di falsificare la distinzione:

```text
MANUAL DROP
  may discard overflow

EOD AUTO-DROP
  may discard overflow

PLACE to shed
  deposits only what fits and leaves remainder with worker
```

Verificare:

- shed capacity;
- worker inventory mutation;
- overflow;
- ordine delle operazioni;
- eventuali altre cause di inventory loss non riportate.

---

# 12. Clock e periodicitÃ

Controllare che nessuna periodicitÃ  sia erroneamente congelata in step.

Verificare il principio:

```text
period_steps = period_days * turnsPerDay
```

solo dove applicabile.

In particolare controllare la conclusione:

```text
WHEAT ~96 step observed cycle
!=
engine biological period of 96 universal steps
```

e distinguere service cadence day-scoped da â€œlast service + Tâ€.

---

# 13. Service needs e deadlines

Revisionare la tassonomia:

```text
ENGINE_HARD_NEED
POLICY_OUTPUT_NEED
OPTIONAL_BONUS_SERVICE
```

Verificare soprattutto:

- WATER survival;
- WATER yield;
- FEED survival;
- FEED bonus;
- CARE;
- HARVEST;
- COLLECT_FERTILIZER;
- FERTILIZE.

Controllare se il concetto â€œhard needâ€ Ã¨ formulato senza trasformare una scelta economica in regola engine.

---

# 14. Capacity-relevant constraints

Controllare nel source i vincoli elencati dall'audit:

- action slots;
- worker lifecycle;
- HIRE timing;
- movement;
- occupancy;
- worker ordering;
- spatial legality;
- structures;
- seeds;
- feed/fertilizer inventory locality;
- market timing;
- market order cap;
- shed cap;
- DROP/PLACE;
- daily flags;
- EOD phase;
- RNG WEED.

Segnalare qualsiasi vincolo engine rilevante per future reservation/serviceability omesso dall'audit.

Non progettare un algoritmo di scheduling.

---

# 15. Three-way serviceability

Valutare se la distinzione Ã¨ semanticamente corretta:

```text
ACTION_ELIGIBLE_NOW
RESERVED_SERVICEABLE_BEFORE_DEADLINE
REALIZED_SERVICEABLE_IN_WINDOW
```

Verificare in particolare che:

- `ACTION_ELIGIBLE_NOW` possa essere engine/derived state;
- `RESERVED_SERVICEABLE_BEFORE_DEADLINE` resti `POLICY_CONTEXT`;
- `REALIZED_SERVICEABLE_IN_WINDOW` resti post-hoc.

Segnalare qualsiasi rischio di falsa garanzia o future leakage.

---

# 16. Discrepancy matrix

Controllare una per una le discrepancy:

```text
CLK-01
ANI-01
ANI-02
FER-01
FER-02
INV-01
INV-02
SVC-01
CAP-01
OBS-01
HAR-01
SPC-01
PER-01
```

Per ciascuna dare:

```text
DISCREPANCY_ID:
CODEX_CLASSIFICATION:
REVIEWER_CLASSIFICATION:
CURRENT_FOUNDATION_CLAIM_VERIFIED:
ENGINE_EVIDENCE_VERIFIED:
RECOMMENDED_CHANGE_VALID:
NOTES:
```

Prestare particolare attenzione ai quattro P0 dichiarati:

```text
CLK-01
ANI-01
FER-01
INV-01
```

---

# 17. Canonical Period Ledger v1

Revisionare ogni riga della sezione 16 dell'audit.

Per ogni riga classificare:

```text
ACCEPT_AS_ENGINE_CONTRACT
ACCEPT_WITH_CORRECTION
REQUIRES_EVIDENCE
REJECT
```

Verificare:

- event day;
- period days;
- formulas;
- open/close;
- hard deadline;
- ongoing;
- max productions;
- source;
- fingerprint.

Qualsiasi off-by-one deve essere trattato almeno `P1`, o `P0` se altera il comportamento biologico downstream.

---

# 18. Replay reconciliation

I replay sono controllo empirico, non fonte normativa.

Controllare soltanto se la classificazione Codex:

```text
ENGINE_CONFIRMED
ENGINE_COMPATIBLE_POLICY_PATTERN
POLICY_SPECIFIC
REPLAY_MEASUREMENT_ARTIFACT
UNEXPLAINED
```

Ã¨ coerente con engine e delta osservabili.

Non rivalutare la forza competitiva dei player.

Non dedurre nuovi periodi engine dai replay.

---

# 19. No-future-leakage

Controllare la separazione:

```text
PRE_ACTION_ENGINE_STATE
DERIVED_PRE_ACTION_FEATURE
POLICY_CONTEXT
POST_ACTION_TRANSITION_EVIDENCE
POST_WINDOW_METRIC
```

Tentare di trovare:

- completion evidence usata troppo presto;
- realized serviceability usata come forecast;
- action request confusa con execution;
- replay offset;
- final reward leakage;
- metriche di window non ancora chiusa.

---

# 20. Domande obbligatorie del reviewer

Rispondere esplicitamente:

1. Il fingerprint engine Ã¨ riproducibile?
2. Il clock contract Ã¨ corretto?
3. Esiste qualche off-by-one biologico?
4. `CHICKEN=NOT_SUPPORTED` Ã¨ corretto?
5. Il ledger include tutte le specie supportate?
6. Animal base production senza FEED Ã¨ confermata?
7. La semantica CARE/pending bonus Ã¨ corretta?
8. Fertilizer total=2/uplift=+1 Ã¨ corretto?
9. La finestra fertilizer `d..d+2` Ã¨ corretta?
10. Manual DROP puÃ² perdere overflow?
11. PLACE conserva l'eccedenza?
12. Ci sono altre P0 contradiction non individuate?
13. Ci sono P0 Codex che in realtÃ  non sono P0?
14. Il period ledger Ã¨ sufficientemente source-grounded?
15. Il ledger separa correttamente engine facts e policy choices?
16. La tripartizione della serviceability Ã¨ corretta?
17. La discrepancy matrix Ã¨ completa abbastanza per iniziare Ontology revision?
18. Esiste qualche fatto ancora `UNRESOLVED` che deve bloccare il freeze?

---

# 21. Output separati

## Antigravity

Creare:

```text
results/model_spec_c2/foundation_revision/
ANTIGRAVITY_C2_ENGINE_CONTRACT_REVIEW.md
```

## Copilot

Creare:

```text
results/model_spec_c2/foundation_revision/
COPILOT_C2_ENGINE_CONTRACT_REVIEW.md
```

Non modificare il report Codex.

---

# 22. Schema finale obbligatorio

Ogni review deve chiudersi con:

```text
REVIEWER:
ENGINE_IDENTITY_MATCH: YES/NO
CLOCK_CONTRACT_CONFIRMED: YES/NO/PARTIAL
SPECIES_INVENTORY_CONFIRMED: YES/NO/PARTIAL
GOOSE_CHICKEN_RESOLUTION_CONFIRMED: YES/NO
ANIMAL_FEED_PRODUCTION_CONFIRMED: YES/NO/PARTIAL
CARE_BONUS_SEMANTICS_CONFIRMED: YES/NO/PARTIAL
FERTILIZER_SEMANTICS_CONFIRMED: YES/NO/PARTIAL
INVENTORY_OVERFLOW_SEMANTICS_CONFIRMED: YES/NO/PARTIAL
PERIOD_LEDGER_CONFIRMED: YES/NO/PARTIAL
SERVICEABILITY_TRIPARTITION_CONFIRMED: YES/NO/PARTIAL
FOUNDATION_DISCREPANCY_MATRIX_CONFIRMED: YES/NO/PARTIAL

NEW_P0_FOUND: <integer>
NEW_P1_FOUND: <integer>
UNRESOLVED_BLOCKERS: <integer>

ENGINE_CONTRACT_READY_TO_FREEZE: YES/NO
ONTOLOGY_REVISION_SAFE_AFTER_RECONCILIATION: YES/NO

FOUNDATION_MODIFIED: NO
MODEL_SPEC_MODIFIED: NO
CODE_MODIFIED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Se:

```text
NEW_P0_FOUND > 0
```

oppure:

```text
UNRESOLVED_BLOCKERS > 0
```

allora:

```text
ENGINE_CONTRACT_READY_TO_FREEZE: NO
```

e il reviewer deve identificare esattamente il blocker.

---

# 23. Criterio della review

La review non deve chiedere:

> â€œIl documento Codex sembra ragionevole?â€

Deve chiedere:

> â€œPosso riprodurre dal source ogni fatto che stiamo per rendere canonico, e riesco a trovare almeno un caso che lo falsifichi?â€

Il valore della review Ã¨ massimo se trova un errore prima del freeze.

```text
NEXT_ACTION_AFTER_BOTH_REVIEWS:
CROSS-REVIEW RECONCILIATION
-> ENGINE CONTRACT FREEZE OR RETURN TO AUDIT
```
