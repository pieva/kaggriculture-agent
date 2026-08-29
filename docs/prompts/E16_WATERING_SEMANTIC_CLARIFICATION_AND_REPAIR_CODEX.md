# E16 — WATERING SEMANTIC CLARIFICATION + REPAIR AUTHORIZATION — CODEX

## Obiettivo

Rimuovere il blocker semantico identificato nella forensic review E16-A, formalizzare la semantica corretta di `watering_dispatch_priority`, implementare i repair R1/R2/R3, rieseguire esclusivamente i test e l'instrumentation gate E0, quindi fermarsi.

NON eseguire ancora E16-A-R1.

## Decisione normativa

La semantica canonica di `watering_dispatch_priority` è:

> Variabile controllata della policy che determina la precedenza relativa delle azioni WATER rispetto alle altre classi di azione concorrenti quando esiste domanda di irrigazione.

NON significa percentuale di crop needs da irrigare, percentuale di tile da selezionare, quota fissa di crop da servire o fixed-prefix coverage.

Mantieni distinti:

```text
watering_dispatch_priority   # controlled policy variable
watering_execution_rate      # derived observed metric
watering_continuity          # derived observed metric
```

Mantieni i valori frozen:

```text
LOW  = 0.20
MID  = 0.45
HIGH = 0.70
```

Interpretali come intensità relativa di dispatch/prioritizzazione, non come coverage target.

La loro implementazione deve:
- alterare ordinamento/scoring/precedenza delle richieste WATER rispetto ad azioni concorrenti;
- non escludere permanentemente una frazione fissa delle crop needs;
- consentire che tutte le crop needs possano essere servite se capacità e timing lo permettono;
- preservare il resto del comportamento frozen.

## R1 — Watering semantics

Correggi l'implementazione in modo che `watering_dispatch_priority` sia una vera dispatch preference.

Acceptance conditions:
1. LOW/MID/HIGH modificano la precedenza relativa di WATER;
2. HIGH > MID > LOW nella priorità WATER;
3. nessun livello implica automaticamente una quota fissa di crop non servite;
4. a capacità sufficiente tutte le needs possono essere servite;
5. la selezione non usa un fixed prefix permanente;
6. comportamento deterministico dato stesso stato/seed/config.

Aggiungi test specifici.

## R2 — Event ledger attribution

Correggi l'attribuzione degli eventi unit-action.

Ogni evento attribuibile deve riportare correttamente almeno:

```text
player
seat
unit
cell_id
seed
step
action/requested_payload
execution_status
```

Non devono esistere eventi unit-action attribuibili con `player = -1`, salvo casi realmente non attribuibili, che devono essere esplicitamente classificati e non usati nelle metriche treatment/opponent.

Test obbligatori per treatment/opponent in P0/P1.

## R3 — Derived watering metrics

Correggi e formalizza:

```text
watering_execution_rate
watering_continuity
```

Le formule devono essere documentate e testate con casi sintetici.

Requisiti:

```text
0 <= watering_execution_rate <= 1
0 <= watering_continuity <= 1
```

`watering_execution_rate` deve riflettere WATER effettivamente eseguite rispetto alle opportunità/domande definite dalla metrica.

`watering_continuity` deve misurare continuità temporale del servizio secondo la definizione frozen/implementata.

Aggiungi synthetic tests con risultato noto.

## Preservazione provenance

I 28 run originali restano associati a:

```text
OLD_TREATMENT_BUILD_SHA256 =
8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e
```

Non sovrascriverli e non modificare `results/e16/stage_a/`.

La corrected replication futura userà:

```text
E16-A-R1
results/e16/stage_a_r1/
```

e un nuovo treatment build hash.

## Config / versioning

Poiché la semantica frozen viene chiarita formalmente, aggiorna la config/spec necessaria e genera:

```text
NEW_TREATMENT_BUILD_SHA256
NEW_CONFIG_SHA256
```

Preserva il vecchio config/hash nella provenance dei run originali.

Documenta chiaramente `semantic clarification`, `implementation repair`, `telemetry repair` come motivi della nuova versione.

## Test

Dopo l'implementazione esegui l'intera suite.

Devono passare almeno tutti i test precedenti più i nuovi regression test per:
1. LOW < MID < HIGH nella priorità WATER;
2. no fixed-prefix exclusion;
3. possibilità di 100% coverage con capacità sufficiente;
4. corretta attribution P0/P1;
5. no `player=-1` per eventi attribuibili;
6. execution rate sintetico;
7. continuity sintetica;
8. treatment/opponent separation;
9. backward provenance;
10. manifest/hash consistency.

## E0 instrumentation gate

Dopo test PASS:
- rigenera il treatment artifact corretto;
- verifica opponent hash invariato;
- verifica nuova config hash;
- esegui esclusivamente E0 instrumentation smoke test;
- verifica che WATER attribution e derived metrics siano coerenti.

E0 non è training evidence.

## Stop obbligatorio

FERMATI dopo:

```text
repair implementation
tests
new hashes
E0 PASS
```

NON eseguire:

```text
E16-A-R1
Stage B
Kaggle submission
MODEL_SPEC tuning
```

## Output attesi

Aggiorna/crea almeno:

```text
docs/experiment_designs/e16/E16_IMPLEMENTATION_REPAIR_SPEC.md
results/e16/manifests/E16_IMPLEMENTATION_MANIFEST.json
results/e16/instrumentation/E16_E0_REPORT.md
```

e gli artifact/hash necessari alla nuova treatment build.

Preserva integralmente la forensic review precedente.

## Report finale

Concludi con:

```text
REPAIR_STATUS: READY | BLOCKED

SEMANTIC_CLARIFICATION_APPLIED: YES | NO

R1_WATERING_SEMANTICS: PASS | FAIL
R2_LEDGER_ATTRIBUTION: PASS | FAIL
R3_DERIVED_METRICS: PASS | FAIL

TESTS: <passed>/<total>

OLD_TREATMENT_BUILD_SHA256:
8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e

NEW_TREATMENT_BUILD_SHA256: ...

OLD_CONFIG_SHA256:
4c6ca43025d5a95acd6b2c8c5eb51a17a4bc4cadd672146055c317d54864ec92

NEW_CONFIG_SHA256: ...

OPPONENT_SHA256_VERIFIED: YES | NO

E0_STATUS: PASS | FAIL

ORIGINAL_STAGE_A_PRESERVED: YES | NO

E16_A_R1_READY: YES | NO

NEW_RUNS_EXECUTED: 0
STAGE_B_EXECUTED: NO

BLOCKERS: NONE | ...

FILES_CHANGED:
  ...
```

Il task termina qui.
