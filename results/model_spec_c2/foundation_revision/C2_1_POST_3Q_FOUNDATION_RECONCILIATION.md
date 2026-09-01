# Foundation C2.1 post-3Q — Riconciliazione finale

## Stato

```text
RECONCILIATION_DATE: 2026-09-01
ENGINE_AGGREGATE_SHA256: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
ANTIGRAVITY_FEEDBACK_COMPLETE: YES
COPILOT_FEEDBACK_COMPLETE: YES
FOUNDATION_C2_1_STATUS: RECONCILED
POST_3Q_FOUNDATION_PHASE: COMPLETE
SHARED_DELIBERATION_LAYER: REMOVED_AFTER_MIGRATION
OBSERVATION_CONTRACT: src/agricola/core/observation_contract.py
NEXT_EXPERIMENT_SEQUENCE: RESUME_AFTER_E16
```

La riconciliazione è stata eseguita soltanto dopo la comparsa di entrambi i feedback richiesti. Dopo l'accettazione della revisione, le candidate transitorie sono state rimosse; restano i tre file C2.1 finali, le baseline C2 congelate, i feedback e questo ledger di riconciliazione.

## Input

Candidate comuni usate durante la review e rimosse dopo l'accettazione:

- `docs/model/ontology/ONTOLOGY_C2_1_POST_3Q_REVIEW_CANDIDATE.md`;
- `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1_POST_3Q_REVIEW_CANDIDATE.md`;
- `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1_POST_3Q_REVIEW_CANDIDATE.md`.

Feedback indipendenti:

- `results/model_spec_c2/foundation_revision_feedback/ANTIGRAVITY_C2_1_POST_3Q_FOUNDATION_REVIEW.md`;
- `results/model_spec_c2/foundation_revision_feedback/COPILOT_C2_1_POST_3Q_FOUNDATION_REVIEW.md`.

Evidenza primaria aggiuntiva:

- `_process_market`, `_commit_unit`, `_do_hire` ed EOD del runtime fingerprintato;
- torneo di chiusura congelato `POST_3Q_CLOSURE_THREE_WAY_FROZEN_V1`;
- import runtime delle routine Antigravity e Copilot.

## Artefatti riconciliati

| Layer | File | SHA-256 |
|---|---|---|
| Ontology | `docs/model/ontology/ONTOLOGY_C2_1.md` | `10C910388EE4DED8D99B5A5530035D26B336EDE2E4D8EB02026C3599C4566778` |
| State Machine | `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md` | `5E4056555315AB23B80038DB96889EA1F659E1B6FC74B9047BF004A6F572676E` |
| Feature Model | `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md` | `4FCBBDEC664BD25217A3F2EB8B76142E95E4335AD98947A33D60C326A4F0A3CA` |
| Observation Contract runtime | `src/agricola/core/observation_contract.py` | `3E7509888B09103C79B86FD058984651337CBFC32AB60CD934E6351A4F2A81A9` |
| Codex MODEL_SPEC | `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md` | `6DE5046650BFC2D6037747B7CF9DA8FBEF02DC14B6F6C71B76779748B7930FFF` |

## Decisioni sul feedback

### Ontology

Accolto da Antigravity:

- `operating_cash_buffer` chiarisce che la riserva finanzia ordini futuri scelti dalla policy e che non esistono costi di mantenimento a EOD.

Accolto da Copilot:

- `shared_market_contention_externality` passa da `ENGINE_VERIFIED` a `DERIVED`;
- la misura è definita rispetto a una baseline pre-stato dichiarata e non come controfattuale causale nativo dell'engine.

Verdetto riconciliato: `ACCEPT_WITH_CHANGES -> ACCEPTED`.

### State Machine

Accolto il nucleo condiviso dei feedback:

- costo `HIRE` una sola volta al commit Fibonacci;
- nessun salario, wage floor o insolvenza EOD;
- Hands rimossi incondizionatamente a EOD;
- mercato per slot e per unità, con quote comuni e commit ordinato;
- obbligo di bilanciare i seat nei tornei.

Respinta la modifica Antigravity che affermava l'esaurimento dello stock da parte di Player 0. La lettura diretta dell'engine mostra:

1. per ogni unità vengono calcolate entrambe le quote prima di qualsiasi commit;
2. Player 0 e Player 1 vengono poi committati con le rispettive quote congelate;
3. la successiva unità viene riquotata sul market aggiornato;
4. `_refresh_prices` avviene a fine slot;
5. `_commit_unit(BUY_PRODUCT)` verifica cassa e capienza shed, ma non verifica che `market.inventory[item] > 0`; l'inventario può diventare negativo.

È stata quindi corretta nella versione finale anche la formulazione della candidata iniziale, che lasciava intendere che il secondo commit osservasse una quota già aggiornata. Il documento finale distingue ordine di commit, quote congelate e guardie effettive; i due feedback preservano l'evidenza del review pass.

Verdetto riconciliato: `ACCEPT_WITH_CORRECTION -> ACCEPTED`.

### Feature Model

Accolto da Antigravity:

- nota `MKT-07` resa inequivocabile sull'assenza di stipendi e penalità EOD.

Accolto da Copilot:

- `POST-46` e `POST-49` indicizzati per seat, slot, tipo e item;
- `POST-49` richiede una baseline dichiarata e non implica causalità esatta;
- `POST-57` diventa un record di provenance con hash implementazione, hash action table, origine, parent hash, delta comportamentale e stato di indipendenza.

Verdetto riconciliato: `ACCEPT_WITH_CHANGES -> ACCEPTED`.

## Chiusura del vecchio layer deliberativo

Entrambi i reviewer convergono su `REMOVE_AFTER_MIGRATION`. Il vecchio modulo non era istanziato dai controller correnti, ma ospitava adapter, clock, snapshot e normalizzazione usati dai consumer runtime.

Decisione finale:

```text
EXTRACT_NEUTRAL_OBSERVATION_CONTRACT: COMPLETE
MIGRATE_IMPORTS_WITH_PARITY: COMPLETE
ZERO_OLD_IMPORTS: PASS
DELETE_OLD_RUNTIME_CONTAINER: COMPLETE
DELETE_OLD_FOUNDATION_DOCUMENT: COMPLETE
```

Il contratto neutrale risultante è `src/agricola/core/observation_contract.py` e non contiene routine, working set, priorità o stati cognitivi agent-local. La migrazione ha superato i test mirati prima della rimozione del vecchio contenitore.

## MODEL_SPEC dei tre agenti

### Codex

Il MODEL_SPEC finale è `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`. Documenta correttamente routine, hash, limiti, contratto osservativo neutrale e fallimento di indipendenza dei confronti derivativi correnti.

### Copilot

`docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2_3Q_POST_FOUNDATION_REVIEW.md` è accettato come disclosure onesta di una **baseline derivativa**. Dichiara correttamente l'import diretto della routine Codex e `STRATEGIC_INDEPENDENCE_GATE: FAIL`. Non è ancora un MODEL_SPEC di una strategia Copilot indipendente.

### Antigravity

`docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md` è accettato, dopo remediation, come disclosure onesta di una **baseline derivativa**:

1. il source corrente importa direttamente `ROUTINE_ACTIONS` e `ROUTINE_SHA256` da `agricola.strategy.codex_v9_routine_data`;
2. il routine hash dichiarato a runtime è lo stesso Codex `C2466262...`;
3. la liquidazione terminale è un delta comportamentale utile ma non rende autonoma l'action table di base;
4. source, config, freeze e submission canonica sono ora riallineati agli hash dichiarati;
5. il torneo è correttamente classificato come misura del delta terminale sulla stessa routine, non come confronto strategico indipendente.

Gate riconciliato Antigravity:

```text
NO_IMPORT_OTHER_AGENT_ROUTINE: FAIL
NO_COPY_OTHER_AGENT_ACTION_TABLE: FAIL
NO_IDENTICAL_ROUTINE_SHA: FAIL
NO_THIN_WRAPPER_AS_MODEL: FAIL
PROVENANCE_DISCLOSURE: PARTIAL
STRATEGIC_INDEPENDENCE_GATE: FAIL
```

L'originario `PASS` sui gate di indipendenza resta respinto; il MODEL_SPEC corrente dichiara invece correttamente `FAIL` e può essere mantenuto come baseline derivativa.

## Risultato del torneo concorrente

Il torneo di chiusura è terminato senza errori:

| Agente | W-L-T | Media | Interpretazione |
|---|---:|---:|---|
| Antigravity V4 | 26-2-0 | 89.280,86 | routine Codex + liquidazione terminale |
| Codex V9 | 2-14-12 | 88.576,29 | routine base |
| Copilot V2 | 2-14-12 | 88.576,29 | routine base equivalente |

Il delta medio Antigravity è +704,57, con metriche operative identiche. `STRATEGIC_INDEPENDENCE_GATE: FAIL`; il risultato è valido come replica e ablation della liquidazione terminale.

## Chiusura della fase e ritorno agli esperimenti

La Foundation post-3Q è ora chiusa. Da questo punto:

- C2.1 è il riferimento documentale riconciliato;
- le baseline C2, i feedback e la riconciliazione restano preservati per audit; le candidate transitorie sono state rimosse;
- nuove correzioni Foundation richiedono evidenza engine falsificante, non semplici differenze di policy;
- ogni agente deve sviluppare e congelare una strategia propria, senza routine condivise;
- la sequenza sperimentale riprende dopo E16, con il prossimo ID normalmente `E17`;
- E17 deve avere ipotesi causale, baseline congelata, seed preregistrati, seat bilanciati e ledger requested/executed;
- nessun E17 è stato avviato durante la riconciliazione.

## Blocco finale

```text
ONTOLOGY_C2_1: RECONCILED
STATE_MACHINE_C2_1: RECONCILED
FEATURE_MODEL_C2_1: RECONCILED
CODEX_MODEL_SPEC: ACTIVE_POST_FOUNDATION
ANTIGRAVITY_MODEL_SPEC: ACCEPTED_AS_DERIVATIVE_BASELINE
COPILOT_MODEL_SPEC: ACCEPTED_AS_DERIVATIVE_BASELINE
SHARED_DELIBERATION_LAYER: REMOVED
OBSERVATION_CONTRACT: ACTIVE
POST_3Q_TOURNAMENT: COMPLETE_DERIVATIVE_BASELINE
FOUNDATION_PHASE: COMPLETE
NEXT_SEQUENCE: E17
```
