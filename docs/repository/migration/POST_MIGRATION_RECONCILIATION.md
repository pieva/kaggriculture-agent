# Reconciliation post-migrazione

- **Data:** 2026-09-02
- **Integration owner:** Codex
- **Fronte:** A7
- **Verdetto:** `PASS`

## Reconciliation delle review indipendenti

| Agente | Review | Verdetto | Blocker |
|---|---|---|---:|
| Antigravity | `POST_MIGRATION_REVIEW_antigravity.md` | `PASS_WITH_ACCEPTED_DEBT` | 0 |
| Codex | `POST_MIGRATION_REVIEW_codex.md` | `PASS_WITH_ACCEPTED_DEBT` | 0 |
| Copilot | `POST_MIGRATION_REVIEW_COPILOT.md` | `PASS` | 0 |

Le tre review convergono su copertura completa, importabilità, suite, config,
replay e hash della submission. I rilievi sugli hash source Antigravity e
Copilot sono stati risolti dai rispettivi owner aggiornando la provenance dopo
le sole correzioni path/import. Nessuna routine o decisione è stata modificata
nel Fronte A.

## Copertura della migrazione

```text
FILES_INVENTORIED: 1058
FILES_MOVED: 188
FILES_ARCHIVED: 776
FILES_KEPT: 89
FILES_DELETED_BY_MIGRATION: 0
PREEXISTING_DELETIONS_DOCUMENTED: 5
SOURCE_DESTINATION_ROWS_VERIFIED: 1058/1058
```

`MIGRATION_EXECUTION_RESULTS.csv` verifica presenza/assenza delle source e
destination. `REFERENCE_REWRITE_MANIFEST.csv` registra 1.481 sostituzioni in
223 file. Le variazioni successive al move sono limitate a riferimenti,
config path, indici, provenance e documenti di gate.

## Gate A7

```text
REPOSITORY_TREE_MATCHES_ARCHITECTURE: PASS
NO_LOST_TRACKED_FILES: PASS
MIGRATION_MANIFEST_COVERAGE: 100%
IMMUTABLE_HASHES_PRESERVED: PASS
MARKDOWN_LINK_CHECK: PASS
PYTHON_IMPORT_CHECK: PASS
TEST_SUITE: PASS
SUBMISSION_CODEX_SHA256: AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421
UNRESOLVED_BLOCKERS: 0
POST_MIGRATION_REVIEWS: 3/3
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
```

Evidenza sintetica:

- albero target: 35/35 directory richieste presenti e archivi E01–E16 presenti;
- superficie Markdown attiva: 65 file, 36 link locali, 0 broken;
- import check: core e tre namespace agent-local importabili;
- test suite: 49/49 pass;
- replay: 18/18 file presenti e conformi al manifest;
- submission: unico file `submission/submission_codex.py`, hash invariato;
- Foundation C2.1, observation contract e routine Codex: hash congelati invariati.

## Debito accettato

1. Cache locali ignorate da Git con ACL non leggibili (`.pytest_cache`,
   `.pytest_temp`, `.ruff_cache`), estranee al prodotto.
2. Riferimenti d'epoca nei soli archivi E01–E16 e nella governance storica,
   esclusi dalla superficie operativa.
3. Cinque cancellazioni antecedenti al preflight, tutte registrate con path e
   SHA-256 e recuperabili dalla cronologia Git.

## Decisione A→B

Il Fronte A è chiuso. È autorizzato il solo Fronte B previsto dal prompt:
review/freeze della strategia comune e implementazione di E17.0. Restano
vietati E17.1, mutazioni di policy, torneo non indipendente, submission Kaggle,
commit e push.
