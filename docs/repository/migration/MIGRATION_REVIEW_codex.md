# Review pre-migrazione Codex

- **Snapshot inventariato:** 2026-09-02, prima dei move del Fronte A
- **Inventario:** `MIGRATION_INVENTORY_codex.csv`
- **Righe:** 1.047
- **Move verso percorsi canonici:** 188
- **Archiviazioni:** 776
- **Keep:** 78
- **Cancellazioni già presenti nel worktree:** 5

## Stato iniziale preservato

Il worktree non era pulito all'avvio. L'inventario conserva come stato del
proprietario:

- cinque cancellazioni tracciate già presenti sotto `docs/benchmark/`;
- nove replay E17 e il catalogo `json.md` non tracciati;
- documentazione e risultati E17 non tracciati;
- modifiche a `README.md`, `docs/NEW_SESSION.md` e
  `docs/PROJECT_STATE.md`;
- un preflight Copilot concorrente sotto `docs/repository/` ed
  `experiments/`.

Le cinque cancellazioni pregresse sono classificate `candidate_delete`: non
vengono ripristinate né reinterpretate come effetto della migrazione.

## Esito dell'inventario

Il mapping Codex copre file tracciati e non tracciati visibili, assegna hash,
ruolo, round, ownership e destinazione. Non risultano collisioni fra
destinazioni proposte.

Decisioni strutturali principali:

1. E17 viene ricomposto verticalmente sotto `experiments/e17/`;
2. E01–E16 vengono conservati sotto `experiments/archive/eNN/`;
3. i replay esterni passano a `data/replays/reference/` oppure
   `data/replays/e17-discovery/`;
4. Foundation, MODEL_SPEC e governance vengono separati sotto `docs/`;
5. la submission canonica Codex resta immutata; le altre submission vengono
   archiviate, non cancellate;
6. il runtime Codex attivo viene namespacizzato sotto
   `src/agricola/strategy/codex/`.

## Rischi e controlli richiesti

| Severità | Rischio | Controllo |
|---|---|---|
| BLOCKER | inventari indipendenti Antigravity/Copilot ancora da riconciliare | attendere 3/3 prima del manifest frozen |
| MAJOR | riferimenti storici ai vecchi path | sostituzione meccanica e link audit post-move |
| MAJOR | import Python del controller Codex | aggiornare import e rieseguire suite |
| MAJOR | corpus storico molto ampio | manifest source→destination al 100% e controllo hash |
| MINOR | preflight Copilot usa maiuscole nei nomi file | trattare Windows come case-insensitive e preservare il file esistente |

## Decisione A0

```text
CODEX_INVENTORY: COMPLETE
DESTINATION_COLLISIONS: 0
MIGRATION_EXECUTION: NOT_STARTED
E17_LAUNCH: BLOCKED
POLICY_MUTATION: NONE
```
