# Review Codex post-migrazione

- **Data:** 2026-09-02
- **Ambito:** Fronte A / A6
- **Verdetto:** `PASS_WITH_ACCEPTED_DEBT`
- **Blocker irrisolti:** `0`

## Esito dei controlli

| Controllo | Esito | Evidenza |
|---|---|---|
| `NO_LOST_TRACKED_FILES` | `PASS` | 1.058 righe riconciliate: 964 move/archive verificati, 89 keep verificati, 5 cancellazioni già presenti prima della migrazione e non ripristinate. |
| `SOURCE_DESTINATION_COVERAGE` | `PASS` | Tutte le 964 source migrate sono assenti e tutte le rispettive destination sono presenti; `MIGRATION_EXECUTION_RESULTS.csv`. |
| `SHA256_PRESERVATION` | `PASS` | Hash verificato durante i move. Stato corrente: 822 match byte-identici, 218 file con sola riscrittura di riferimenti e 13 correzioni strutturali/path o indici documentate. Gli artefatti immutabili coincidono con il freeze. |
| `MARKDOWN_LINKS` | `PASS` | Superficie attiva: 65 file, 36 link locali, 0 broken. Otto riferimenti a artefatti storici mai presenti sono stati resi esplicitamente non navigabili; gli archivi storici sono esclusi dal gate attivo. |
| `PYTHON_IMPORTS` | `PASS` | Import di core, Codex, Antigravity e Copilot eseguito con `PYTHONDONTWRITEBYTECODE=1`. |
| `TEST_SUITE` | `PASS` | `49 passed in 49.45s`, cache provider disabilitato. |
| `CONFIG_PATHS` | `PASS` | I tre JSON agent-local sono validi e i loader attivi puntano a `docs/model_specs/<agent>/configs/`. |
| `REPLAY_MANIFEST` | `PASS` | 18 replay presenti e hash-conformi: 9 `DISCOVERY`, 9 `TRAINING_HISTORY`; Episode ID e ruolo epistemico conservati. |
| `SUBMISSION_HASH` | `PASS` | `submission/submission_codex.py` = `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421`; unica submission presente. |
| `GIT_STATUS` | `PASS` | Il diff esteso è coerente con una migrazione non ancora committata; nessun reset, commit o push eseguito. |
| `AGENT_OWNERSHIP` | `PASS` | Eseguiti 806 move Codex/common, 110 Antigravity e 48 Copilot secondo owner unico nel manifest. |

## Hash immutabili

```text
ONTOLOGY_C2_1:       10C910388EE4DED8D99B5A5530035D26B336EDE2E4D8EB02026C3599C4566778
STATE_MACHINE_C2_1: 5E4056555315AB23B80038DB96889EA1F659E1B6FC74B9047BF004A6F572676E
FEATURE_MODEL_C2_1: 4FCBBDEC664BD25217A3F2EB8B76142E95E4335AD98947A33D60C326A4F0A3CA
OBSERVATION_CONTRACT: 3E7509888B09103C79B86FD058984651337CBFC32AB60CD934E6351A4F2A81A9
CODEX_ROUTINE_DATA: AC5819014EBB85ED86BA5D25D4F01DE46F9E4760465B7188DF11E69C8812F774
SUBMISSION_CODEX:   AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421
```

## Rilievi classificati

- `ACCEPTED_DEBT` — `.pytest_cache`, `.pytest_temp` e `.ruff_cache` locali hanno ACL non leggibili; sono ignorati da Git e non fanno parte del prodotto migrato.
- `ACCEPTED_DEBT` — i documenti in `experiments/archive/` e `docs/governance/history/` possono conservare riferimenti storici non risolvibili nell'istantanea; il gate link riguarda la documentazione attiva.
- `ACCEPTED_DEBT` — cinque file risultavano già cancellati all'inizio del preflight; path e SHA-256 sono conservati nel manifest e i blob restano recuperabili dalla cronologia Git.

Non risultano rilievi `BLOCKER`, `MAJOR` o `MINOR` aperti.

## Decisione

La review Codex approva la chiusura del Fronte A, subordinatamente alla presenza
delle altre due review indipendenti e alla reconciliation A7. Nessuna attività
E17 è stata avviata durante questa review.
