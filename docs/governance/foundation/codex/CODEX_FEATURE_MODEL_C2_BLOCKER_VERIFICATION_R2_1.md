# Codex - Feature Model C2 Blocker Verification R2.1

```text
REVIEW TARGET: docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
REVIEW BASELINE: docs/governance/foundation/codex/CODEX_FEATURE_MODEL_C2_REVIEW_R1.md
REVIEW SCOPE: P0-01, P0-02, P1-01..04 e regression check P2-01..02
ANTIGRAVITY_FOUNDATION_REVIEW_R1: READ
```

## Verdetto

| Finding | Verdict | Evidence | Blocking |
|---|---|---|---|
| P0-01 | CLOSED | Il catalogo contiene 58 ID ammissibili unici; classi e membership coincidono, la migrazione copre i 58 ID piu `REJ-01`, che resta fuori dal totale. | NO |
| P0-02 | OPEN | Il classifier usa `tile.kind == "LOCKED"` senza un contratto di normalizzazione del valore engine nativo `"LOCKED"`. Inoltre il vector "immediately after intermediate harvest" conserva `yield_units > 0 => HARVEST_READY`, mentre il post-HARVEST engine e `yield_units = 0`, produzione futura presente, quindi `GROWING`. Classifier e test vectors non sono coerenti. | YES |
| P1-01 | OPEN | I flag dei 13 aggregate controllati sono discordanti tra catalogo e aggregate-contract table: `CRP-18` ha schema `YES` nel catalogo ma `NO` nella tabella; `CRP-19..25`, `WRK-03..06` e `MKT-03` hanno schema `NO` nel catalogo ma `YES` nella tabella. | YES |
| P1-02 | CLOSED | `TMP-01`, `TMP-04`, `TMP-05` e `CRP-11..15` espongono clock, source/derivation, phase, availability e leakage. Le deadline lifespan usano `engine_step`; `canonical_step` resta diagnostico. | NO |
| P1-03 | CLOSED | Il Feature Model richiede esplicitamente `cared_today AND fed_today` per l'accumulo EOD e separa flag giornalieri, accumulo e consumo su production day. La wording upstream incompatibile richiede una correzione locale, ma il contratto necessario ai MODEL_SPEC e non ambiguo. | NO |
| P1-04 | CLOSED | Le membership sono esplicite e coincidono con il catalogo. I campi market puramente event/provenance restano fuori; `GLB-02` e `GLB-03` sono definiti come telemetry post-action/post-transition con granularita propria e non come input decisionali. | NO |
| P2-01 | REGRESSION | La formula `count(tile.kind == PLANT)` e correttamente completa e `freeze_ready = NO`, ma `CONTRACT_SCHEMA_COMPLETE` vale `YES` nel catalogo e `NO` nella tabella e nella sezione dedicata. | YES |
| P2-02 | OK | Eligibility riguarda relazione spaziale e precondizioni correnti; serviceability e una stima futura con routing/scheduling/contention, resta `PARTIALLY_KNOWN`, formula incompleta, non freeze-ready e non e una garanzia. | NO |

## Verifica meccanica

```text
CANONICAL_CATALOG_TOTAL: 58
CLASS_COUNT_SUM: 58
CATALOG_TOTAL_MATCH: YES
DUPLICATE_FEATURE_IDS: 0
DUPLICATE_CLASS_MEMBERSHIP: 0
MIGRATION_COVERAGE: COMPLETE
REJ-01: OUTSIDE_ADMISSIBLE_FEATURE_TOTAL
COMPLETENESS_FLAG_CONTRADICTIONS: 13
```

Conteggi derivati dal catalogo:

```text
ENGINE_STATE: 14
RAW_OBSERVABLE: 5
DERIVED_FEATURE: 33
POLICY_CONTEXT: 2
TELEMETRY_ONLY: 3
OUTCOME_LABEL: 1
```

Non esistono violazioni locali delle implicazioni `schema/formula NO => freeze_ready NO`; le 13 contraddizioni sono divergenze tra le due rappresentazioni canoniche degli stessi record.

## Correzioni richieste

Prima di una nuova verifica blocker:

- rendere il ramo `LOCKED` eseguibile sul valore nativo oppure dichiarare e applicare una normalizzazione prima della validazione;
- correggere il vector ongoing post-HARVEST intermedio in `yield_units = 0`, future production `YES`, stato `GROWING`;
- uniformare i tre flag di completezza dei 13 aggregate tra catalogo, aggregate-contract table e sezioni dedicate, mantenendo per `CRP-18` `NO / YES / NO`.

```text
LOCAL_CORRECTIONS_BEFORE_FOUNDATION_FREEZE:
- State Machine C2 sezione 9.2 e transition table: CARE imposta cared_today; pending_care_bonus aumenta a EOD soltanto con cared_today AND fed_today.
- Ontology C2 pending_care_bonus_accumulation: esplicitare la stessa congiunzione FEED+CARE per l'accumulo, distinta dal consumo.
```

## Check repository

```text
git diff --check: PASS
pytest: PASS (143 passed; 1 warning non bloccante sulla cache pytest)
ruff: NOT RUN (opzionale)
```

FEATURE MODEL C2 BLOCKER VERIFICATION: COMPLETED
P0-01: CLOSED
P0-02: OPEN
P1-01: OPEN
P1-02: CLOSED
P1-03: CLOSED
P1-04: CLOSED
MODEL_SPEC_C2_UPSTREAM_READY: NO
FOUNDATION C2: NOT FROZEN
