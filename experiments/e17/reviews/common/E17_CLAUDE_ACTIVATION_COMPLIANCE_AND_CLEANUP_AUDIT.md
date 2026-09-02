# E17.1 — Audit attivazione Claude e pulizia repository

- **Data:** 2026-09-02
- **Verdetto:** `PASS_WITH_LOCAL_CLEANUP`
- **Ambito:** attività Claude V1/V2 e piano V3 eseguite dopo l'attivazione
- **Holdout/final confirmation:** `NOT_CONSUMED`

## Esito

Claude si è mosso nel repository secondo le direttive di ownership e
indipendenza. L'audit della sessione locale e dell'albero di lavoro non ha
rilevato accessi ai sorgenti strategici altrui, mutazioni Git, scritture nella
submission o uso dei seed riservati.

| Controllo | Esito |
|---|---:|
| scritture fuori dai namespace Claude/E17 autorizzati | `0` |
| letture di strategie o submission altrui | `0` |
| import proibiti nel decision path Claude | `0` |
| comandi Git mutanti | `0` |
| comandi di cancellazione | `0` |
| comandi con seed holdout/final | `0` |
| scritture in `submission/` | `0` |

Le scritture osservate ricadono esclusivamente in:

- `src/agricola/strategy/claude/`;
- `docs/model_specs/claude/`;
- `experiments/e17/{configs,tools,tests,reports}/claude` o file di test Claude;
- `experiments/e17/artifacts/{runs,derived,freeze}/claude/`.

## Verifiche della candidata V2

- source SHA-256:
  `8CBB5E96CFA4137E89E9759C095051B893E6FD51A7B20F25DC4C1053061A6451`;
- config SHA-256:
  `71D9B3C793F17CAC13C3A419FCACE31A003E567E6A6E2D9D3709E44091C53707`;
- source coerente con il freeze: `PASS`;
- test Claude: `25 passed`;
- lint: `PASS`;
- indipendenza degli import: `PASS`.

Il verdetto di conformità non promuove la V2: restano falliti i gate economico,
fughe e copertura 3Q passiva documentati nel relativo report.

## Pulizia applicata

- rimosso `CLAUDE.md` dalla radice: era un bootstrap locale e duplicava
  regole ora conservate nei documenti versionati di governance;
- rimosso `.claude/settings.local.json` e aggiunto `.claude/` a `.gitignore`;
- aggiornati i prompt Claude affinché puntino ai riferimenti canonici;
- mantenuti localmente, ma esclusi da Git, i ledger grezzi riproducibili di
  E17.1 (circa 533 MiB complessivi);
- mantenuti in versione source, config, test, runner, manifest, metriche
  compatte e report necessari alla provenance.

## Autorizzazione successiva

Il proprietario autorizza Claude a usare Codex esclusivamente come benchmark
black-box development per la futura V3. Vincoli e gate sono definiti in
`E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`.
