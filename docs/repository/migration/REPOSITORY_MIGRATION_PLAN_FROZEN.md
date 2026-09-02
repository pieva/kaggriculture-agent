# Piano di migrazione del repository — frozen

- **Freeze:** 2026-09-02
- **Integration owner:** Codex
- **Manifest:** `REPOSITORY_MIGRATION_MANIFEST.csv`
- **Inventario di copertura:** `MIGRATION_INVENTORY_codex.csv`

## Copertura riconciliata

| Misura | Valore |
|---|---:|
| Source inventariate | 1.058 |
| Move canonici | 188 |
| Archiviazioni | 776 |
| Keep | 89 |
| Cancellazioni pregresse, non eseguite | 5 |
| Collisioni destinazione | 0 |
| Move assegnati Antigravity | 110 |
| Move assegnati Codex | 806 |
| Move assegnati Copilot | 48 |

I deliverable A0/A1 generati durante il preflight sono conservati sotto
`docs/repository/migration/`; non fanno parte del corpus storico da migrare e
non creano una dipendenza circolare nel gate di copertura.

## Input indipendenti

- Antigravity: inventario completo da 1.035 righe e review
  `PASS_CON_RILIEVI_MINOR`;
- Copilot: preflight originale preservato in `copilot_preflight/`, audit
  indipendente delle omissioni e metadati riconciliati nel CSV canonico da
  109 righe;
- Codex: inventario completo da 1.058 righe, comprensivo dei deliverable
  comparsi durante A0.

## Decisioni di reconciliation

1. L'albero normativo è quello di
   `docs/repository/REPOSITORY_ARCHITECTURE.md`.
2. Le destinazioni Copilot che conservavano il vecchio
   `docs/model/model_specs/` sono sostituite da `docs/model_specs/`.
3. Le metriche dei nove replay sono `DISCOVERY` e vanno in
   `experiments/e17/artifacts/discovery/`, non in `derived/` generico.
4. Review e feedback E17 vanno in `reviews/<owner>/`; analisi e profili vanno
   in `reports/<owner>/`.
5. E01–E16 vengono archiviati senza cancellare contenuti informativi.
6. Le cinque cancellazioni tracciate già presenti all'avvio restano tali e
   non vengono ripristinate.
7. Le submission non canoniche vengono archiviate; la submission Codex resta
   byte-identica.
8. I move agent-local sono assegnati al relativo owner; common e Codex sono
   eseguiti da Codex.

## Disciplina di esecuzione

- il manifest è l'unica allowlist dei move;
- ogni destinazione viene risolta e verificata dentro il repository;
- il file viene hashato prima e dopo il move;
- nessuna modifica semantica è ammessa durante i move;
- i riferimenti vengono corretti in una fase distinta e registrati in
  `REFERENCE_REWRITE_MANIFEST.csv`;
- nessuna directory viene rimossa ricorsivamente;
- nessuna policy viene modificata sul Fronte A.

## Gate prima dell'esecuzione

```text
THREE_AGENT_A0_INPUTS: PASS
SOURCE_DESTINATION_COVERAGE: 100%
DESTINATION_COLLISIONS: 0
PREEXISTING_DELETIONS_PRESERVED: 5
SUBMISSION_CODEX_SHA256: AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421
MIGRATION_EXECUTION: AUTHORIZED_BY_USER_PROMPT
E17_LAUNCH: BLOCKED_UNTIL_A7
```
