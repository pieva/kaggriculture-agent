# Copilot — Cross-review indipendente C2.1 post-3Q

**Data:** 2026-09-01
**Scope:** review read-only delle candidate comuni e della documentazione Copilot. Nessun candidato comune, runtime, submission canonica o artefatto di altri owner è stato modificato.

## Evidenza e controlli

Sono stati letti integralmente i tre candidati C2.1, le tre baseline C2 congelate, il MODEL_SPEC Codex V9 candidato e il report di migrazione obbligatorio. Il report obbligatorio registra il fingerprint dell'engine a cinque file come:

```text
ENGINE_AGGREGATE_SHA256: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
MATCH_WITH_FROZEN_FOUNDATION: YES
```

La review non trova evidenza di engine drift. Il test runtime locale mirato `tests/test_copilot_3q.py` passa (3 passed); è un test di prefisso di 72 step e non certifica né una telemetria executed né indipendenza strategica.

## A. Ontology C2.1

**Verdetto: ACCEPT_WITH_CHANGES.**

Il delta rispetto a `ONTOLOGY_C2.md` corregge opportunamente `market_transaction_value`: quantità, prezzo e controvalore realizzati sono post-transizione, non dati online certi. L'aggiunta di `shared_market_contention_externality` è necessaria per rendere nominabile la cannibalizzazione vista nel mercato condiviso senza prescrivere una policy. Il candidato conserva la neutralità: buffer di cassa e finestre di impiego restano `POLICY_CONTEXT`, non obblighi per controller.

Conferme runtime/baseline:

- non è introdotto alcun salario o wage floor EOD;
- `HIRE` è un costo di commit nella curva Fibonacci intra-day, non una passività ricorrente;
- gli Hands decadono incondizionatamente a EOD;
- quote pre-stato e fill/prezzo/controvalore post-stato restano distinti.

**Modifica puntuale richiesta — sezione E, `shared_market_contention_externality`:** sostituire `Evidence status: ENGINE_VERIFIED` con `Evidence status: DERIVED` e sostituire “Effetto causale ... attribuibile” con:

> Differenza post-transizione tra l'esito osservato e una baseline pre-stato dichiarata. Il lockstep e l'ordine di commit sono engine-verificati; l'attribuzione numerica alla contesa è una derivazione di telemetria, non un campo nativo né un controfattuale identificato dall'engine.

Questo evita di presentare una decomposizione causale di policy/opponent come primitiva dell'engine.

## B. State Machine C2.1

**Verdetto: ACCEPT.**

Il delta rispetto alla baseline completa correttamente la lacuna di mercato: troncamento per batch, intenti sul medesimo pre-stato dello slot, commit sequenziale per player, refresh dopo commit e seat sensitivity. È coerente con il report obbligatorio e rende esplicito perché una quota online non garantisce fill o prezzo.

Le sezioni workforce/EOD sono corrette e non regrediscono: costo `HIRE` una sola volta al commit Fibonacci, Hands attivi da `t+1`, rimozione EOD incondizionata, reset `hires_today`, e nessun salario/wage floor/insolvenza salariale. La separazione tra domanda, risoluzione ed evidenza post-stato evita leakage e non prescrive dispatching.

Nessuna modifica testuale bloccante proposta.

## C. Feature Model C2.1

**Verdetto: ACCEPT_WITH_CHANGES.**

Il delta rispetto alla baseline ripara `MKT-02..13`: disponibilità e prezzo quotati sono pre-commit; fill, prezzo regolato, controvalore e delta cassa sono `TELEMETRY_ONLY`. `POST-44..56` è un set sufficiente per registrare requested/executed, fill, prezzo, contesa, densità, PASS/desync, serviceability per Q e picco workforce. Tutte queste metriche sono esplicitamente offline e quindi non contaminano il vettore online né prescrivono routine.

La sola ambiguità materiale è `POST-57`: “hash della routine **o** dell'implementazione” consente di omettere proprio l'identità della action table condivisa. È rilevante nel runtime Copilot: `three_quadrant.py` importa direttamente sia `ROUTINE_ACTIONS` sia `ROUTINE_SHA256` da Codex.

**Modifica puntuale richiesta — sezione 16.8, sostituire `POST-57`:**

> `POST-57` (`strategy_provenance`): record immutabile con `implementation_sha256`, `routine_action_table_sha256` quando esiste, `routine_origin`, `parent_routine_sha256`, `behavioral_delta` e `independence_status`. Nessun campo può sostituire l'altro; per policy senza action table il valore della tabella è `NONE`.

**Modifica puntuale richiesta — sezione 16.8, integrare `POST-46` e `POST-49`:**

> Entrambe devono essere indicizzate almeno da `seat`, `order_slot`, `order_type` e `item`; `fill_ratio` usa `executed / max(1, requested)` e registra `requested == 0` separatamente. `POST-49` deve registrare anche la baseline pre-stato dichiarata; non implica un'attribuzione causale esatta.

Il requisito non pretende che l'attuale V2 Copilot già emetta tale ledger: la sua `telemetry_snapshot()` contiene soltanto versione, candidate id, routine hash, errori/fallback. La Foundation definisce lo schema, non può attestare una telemetria non ancora implementata.

## D. Orientamento `decision_lifecycle`

**Verdetto: REMOVE_AFTER_MIGRATION.**

Il report obbligatorio rileva 14 file che usano `CodexClock`, `CodexSnapshot`, `CodexObservationAdapter`, hashing/normalizzazione, e zero istanziazioni nei controller correnti della macchina completa `CodexDecisionLifecycle`. I consumer attivi sono quindi gli adapter/snapshot condivisi in strategie, benchmark/builder e test; non la macchina deliberativa completa. Le evidenze nominate includono strategie che importano `CodexObservationAdapter`/`CodexSnapshot`, i test candidati Codex/Antigravity e le copie standalone storiche. Il controller V2 Copilot qui documentato non importa `codex_lifecycle.py` né istanzia il full DLC.

Destinazione proposta: un modulo neutrale, ad esempio `src/agricola/core/observation_contract.py`, per `Clock`, snapshot immutabile, adapter, hashing stabile e normalizzazione; nessuna routine, priorità, working set o stato di decisione agent-local deve entrarvi.

Test di compatibilità richiesti prima della rimozione:

1. parità adapter/snapshot/hash sul corpus di osservazioni P0/P1 e sulle configurazioni non default;
2. tutti gli import migrati, con test che dimostra zero consumer del vecchio modulo;
3. test che dimostra zero istanziazioni di `CodexDecisionLifecycle`;
4. rebuild verso output non canonico e parità byte/azione delle submission congelate;
5. suite completa senza builder/test che scriva una submission canonica.

Il rischio Foundation è alto se gli stati `DEFINE/PLAN/...`, una routine o un working set locale vengono spostati nel contratto neutrale. Estrarre soltanto i tipi di osservazione evita tale contaminazione. Non eliminare oggi il contenitore: romperebbe gli adapter ancora usati.

## E. Provenance Copilot e gate di indipendenza

Il runtime corrente è una implementazione derivativa, non una strategia indipendente:

```text
SOURCE: src/agricola/strategy/copilot/three_quadrant.py
IMPORT: from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_ACTIONS, ROUTINE_SHA256
PARENT_ROUTINE_SHA256: C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
BEHAVIORAL_DELTA: at step 195 raise the first BUY_PRODUCT WHEAT quantity to >=4; remove BUY_ANIMAL COW orders
```

The direct import makes the action table Codex-owned at execution time. A Copilot namespace, `object` base class, config, or this one-step patch cannot pass the no-import, no-copy, no-identical-SHA, or no-thin-wrapper gates. It may be retained and run only as a disclosed derivative baseline/replica; it must not receive independent comparative credit.

```text
NO_IMPORT_OTHER_AGENT_ROUTINE: FAIL
NO_COPY_OTHER_AGENT_ACTION_TABLE: FAIL
NO_IDENTICAL_ROUTINE_SHA: FAIL
NO_THIN_WRAPPER_AS_MODEL: FAIL
PROVENANCE_DISCLOSURE: PASS
STRATEGIC_INDEPENDENCE_GATE: FAIL
```

## F. Scope closure

No reconciliation was performed, no C2.1 candidate was edited, no E17 was started, and no canonical submission was replaced. The companion MODEL_SPEC and cleanup index make the V2 status and documentation-only cleanup explicit.

```text
ONTOLOGY_VERDICT: ACCEPT_WITH_CHANGES
STATE_MACHINE_VERDICT: ACCEPT
FEATURE_MODEL_VERDICT: ACCEPT_WITH_CHANGES
DECISION_LIFECYCLE_VERDICT: REMOVE_AFTER_MIGRATION
STRATEGIC_INDEPENDENCE_GATE: FAIL
MODEL_SPEC_PATH: docs/model_specs/copilot/MODEL_SPEC_COPILOT_C2_3Q_POST_FOUNDATION_REVIEW.md
CLEANUP_INDEX_PATH: docs/governance/history/model_spec_c2/copilot/README.md
FOUNDATION_READY_FOR_RECONCILIATION: YES
```
