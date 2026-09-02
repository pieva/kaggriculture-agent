# E17.1 — Report di implementazione Claude reattivo indipendente

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V1`
- **Data:** 2026-09-02
- **Stato:** DEVELOPMENT COMPLETE — gate tecnico e gate economico entrambi
  `FAIL` sui seed development; nessuna submission, nessun torneo, nessun
  consumo di holdout eseguito da questo report.
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE.md`
- **Config:** `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V1.json`
- **Source:** `src/agricola/strategy/claude/e17_reactive_3q.py`
- **Test:** `experiments/e17/tests/test_claude_e17_1_reactive.py`
- **Tool:** `experiments/e17/tools/claude/run_claude_e17_1_validation.py`
- **Metriche:** `experiments/e17/artifacts/derived/claude/E17_1_METRICS.json`
- **Freeze manifest:** `experiments/e17/artifacts/freeze/claude/E17_1_FREEZE_MANIFEST.json`

---

## 1. Hash di provenance

| Artefatto | SHA-256 |
|---|---|
| Source (`e17_reactive_3q.py`) | `D92F9F58E4E169F98E62965D5C0370FC82DABFEC402E9CCAA23A7300CA2F947E` |
| Config (`CLAUDE_E17_1_3Q_REACTIVE_V1.json`) | `B8342A90C9161BFD87BF1A9D98752074E90A0799FAAE0617E74CEC36481CCDB9` |
| Fingerprint policy (source+config, `claude_policy_fingerprint()`) | `9A8B1B71A2942DE7A1292F2E3CA592B2E7933694D07B8FC7340211E0EB472063` |
| Routine V9 Codex (riferimento, non consumata) | `C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4` |

Il fingerprint Claude è distinto dalla routine V9 Codex; non esiste una
tabella di azioni indicizzata per step in questo controller (`fingerprint`
copre source+config, non un artefatto di routine separato).

---

## 2. Esito dei test

```text
experiments/e17/tests/test_claude_e17_1_reactive.py
18 passed in 5.5s
```

Copertura richiesta dal prompt operativo, tutta verificata:

| Requisito | Test |
|---|---|
| Import e factory | `test_factory_returns_callable_agent_with_expected_interface`, `test_factory_accepts_explicit_run_context_and_config_path` |
| Batch schema e limiti | `test_action_schema_matches_shared_interface_contract`, `test_market_batch_never_exceeds_configured_limit` |
| Fallback | `test_malformed_observation_falls_back_to_safe_pass`, `test_non_mapping_observation_falls_back_to_safe_pass` |
| Determinismo controllato | `test_same_observation_produces_identical_action`, `test_same_agent_instance_is_deterministic_across_repeated_calls` |
| Reattività a stato diverso, stesso step | `test_reactivity_to_unwatered_plant_at_same_step`, `test_reactivity_to_unfed_animal_at_same_step` |
| Config realmente consumata | `test_config_is_actually_read_and_changes_behavior`, `test_config_target_fill_ratio_gates_plant_opportunities`, `test_config_is_frozen_and_holdout_not_consumed` |
| Assenza import/token proibiti | `test_source_has_no_other_agent_strategy_dependency`, `test_policy_fingerprint_is_a_distinct_sha256` |
| Episode smoke completo | `test_short_episode_smoke_completes_without_technical_errors` |
| Ledger wrapper non cambia le azioni | `test_ledger_wrapper_does_not_change_actions`, `test_ledger_errors_do_not_affect_returned_action` |

`ruff check` pulito su source, test e tool (`All checks passed!`).

---

## 3. Development benchmark

Matrice: 7 seed development × 2 seat, opponent `INERT_PASS_POLICY`,
`episodeSteps=720`. Ogni run eseguita due volte (stesso seed/seat) per
verificare riproducibilità deterministica prima dell'aggregazione. Nessun
seed holdout o final-confirmation è stato eseguito.

### 3.1 KPI per run

| episode_id | final_money | quadranti | fughe derivate | errori tecnici | ledger coverage | riproducibile |
|---|---:|---|---:|---:|---:|:---:|
| S26090101-P0 | 7 483 | NW,NE,SW | 0 | 0 | 100% | sì |
| S26090101-P1 | 8 390 | NW,NE,SW | 0 | 0 | 100% | sì |
| S26090102-P0 | 7 710 | NW,NE,SW | 0 | 0 | 100% | sì |
| S26090102-P1 | 8 604 | NW,NE,SW | 0 | 0 | 100% | sì |
| S26090103-P0 | 10 287 | NW,NE,SW | 0 | 0 | 100% | sì |
| S26090103-P1 | 9 203 | NW,NE,SW | 1 | 0 | 100% | sì |
| S1838889274-P0 | 10 017 | NW,NE,SW | 1 | 0 | 100% | sì |
| S1838889274-P1 | 9 049 | NW,NE,SW | 0 | 0 | 100% | sì |
| S1619968655-P0 | 9 616 | NW,NE,SW | 2 | 0 | 100% | sì |
| S1619968655-P1 | 5 415 | NW,NE,SW | 0 | 0 | 100% | sì |
| S710418712-P0 | 8 918 | NW,NE,SW | 1 | 0 | 100% | sì |
| S710418712-P1 | 10 220 | NW,NE,SW | 0 | 0 | 100% | sì |
| S562040596-P0 | 13 625 | NW,NE,SW | 2 | 0 | 100% | sì |
| S562040596-P1 | 10 287 | NW,NE,SW | 1 | 0 | 100% | sì |

Aggregati: `final_money` media `9 201,7`, mediana `9 126`, minimo `5 415`,
massimo `13 625`, deviazione standard di popolazione `1 781,5`. Fughe
derivate totali `8` su 14 run. Errori tecnici totali `0`. Batch non validi
`0`. `ledger_record_coverage` `100%` su tutte le run.

### 3.2 Gate

| Gate | Esito |
|---|:---:|
| `TECHNICAL_ERRORS == 0` | PASS |
| `INVALID_BATCHES == 0` | PASS |
| `LEDGER_RECORD_COVERAGE == 100%` | PASS |
| `STRATEGIC_INDEPENDENCE == PASS` | PASS |
| `STATE_REACTIVITY_TEST == PASS` | PASS |
| `LEDGER_ACTION_PARITY == PASS` | PASS |
| `DETERMINISTIC_REPRODUCIBILITY` | PASS |
| `SOURCE_CONFIG_FREEZE` | PASS |
| `HOLDOUT_NOT_CONSUMED` | PASS |
| `NO_POST_HOC_SEED_REMOVAL` | PASS |
| `ANIMAL_ESCAPES == 0` | **FAIL** (8 fughe derivate su 14 run) |
| `MAX_QUADRANTS == 3` su tutte le run | PASS |
| `DEVELOPMENT_MEAN_FINAL_MONEY >= 50000` | **FAIL** (media `9 201,7`) |

**Stato di ammissione complessivo: `FAIL`.** Tutti i gate tecnici e di
indipendenza sono `PASS`; i due gate economico/di sicurezza zootecnica non
sono raggiunti. Questo esito non è stato falsificato né nascosto: è
riportato con diagnosi in Sezione 5.

---

## 4. Feature C2.1 effettivamente consumate

Vedi MODEL_SPEC Sezione 4 per l'elenco completo per `feature_id`. In sintesi
per dominio: `TMP-01/02/04/08/09` (clock e orizzonte residuo), `FRM-01/03`
e `MKT-06` (cassa e costo quadrante), `CRP-01/02/04/08/09/10/11/12`
(lifecycle e readiness colturale), `CAR-01/02` (allerta anti-loss),
`FRT-01/02` (finestra fertilizzante), `LIV-01/05/06/07/08/10/11/LIV-STRUCT`
(stato e capacità zootecnica), `WRK-01/02/03/04/05/08` (identità,
posizione, inventario worker), `INV-01/02/05` (shed e semi),
`MKT-01/02/03/04/05/LIMIT` (cassa, prezzi, batch), `ELG-01/02/04/07..23`
(idoneità azioni riflessa nelle guardie), `POL-WS`/`POL-CAP` (zoning e
capacità servibile agent-local). Nessuna feature `POST-*` o telemetria
post-hoc è stata letta dal percorso decisionale (verificato per costruzione:
il ledger è collegato solo esternamente dallo strumento di validazione).

---

## 5. Decisioni principali e diagnosi (varianti provate)

### 5.1 Architettura

Planner interamente ricalcolato ad ogni chiamata (nessuna memoria di target
persistente tra step): scansione dello stato per costruire una coda di
opportunità per tile con priorità fissa, dispatch greedy farmer-poi-hands
con coordinamento `reserved_targets` locale alla chiamata, costruzione
ordini di mercato guidata da guardie di cassa/capacità/orizzonte. Dettagli
completi in MODEL_SPEC Sezioni 5-7.

### 5.2 Difetti trovati e corretti prima del benchmark registrato

Tre difetti tecnici sono stati diagnosticati e corretti sul seed development
`26090101` prima di eseguire la matrice completa registrata in Sezione 3
(dettaglio in MODEL_SPEC Sezione 9.1):

1. **Deadlock semi/opportunità** — `BUY_SEED` dipendeva dall'esistenza di
   una `PLANT_OPPORTUNITY` già in coda, ma quella veniva generata solo con
   semi già in stock: ciclo che non parte mai da stock zero. Corretto
   separando il segnale di fattibilità spaziale da quello di disponibilità
   semi.
2. **Fame di priorità su `BUILD`/`PLACE`** — con la costruzione di
   strutture zootecniche all'ultima priorità, il pool molto più grande di
   opportunità di semina monopolizzava permanentemente i worker liberi:
   nessuna struttura veniva mai costruita (`coop=0, pasture=0` per l'intero
   episodio nel run diagnostico). Corretto rinumerando le priorità
   (Sezione 6.1 del MODEL_SPEC).
3. **Rivendita di animali acquistati** — `_sell_orders` iterava su tutte le
   chiavi dello shed in ordine alfabetico, incluse le specie animali appena
   comprate e in attesa di posizionamento, vendendole di nuovo prima che un
   worker potesse raggiungerle (`shed` mostrava `GOOSE/COW/SHEEP` acquistati
   ma `animal=0` su tutta la board per l'intero episodio). Corretto
   escludendo esplicitamente le chiavi `ANIMALS` dalla scansione vendibile.

### 5.3 Calibrazione cassa (unica variante di tuning adottata)

Dopo le tre correzioni, un run diagnostico mostrava cassa oscillante intorno
a `280-300` per molti giorni consecutivi con `hands=0` quasi ovunque:
`hire_reserve=300` e `land_purchase_reserve=600` erano superiori al flusso
di cassa realmente osservato nella prima fase dell'episodio, bloccando ogni
`HIRE` (workforce ferma a 1 worker) — una trappola di povertà auto-rinforzante
osservabile, non un errore di implementazione. Provata e adottata un'unica
variante: `hire_reserve: 300 -> 50`, `land_purchase_reserve: 600 -> 300`,
insieme a `hands_target_per_quadrant: 4 -> 3` e `hire_batch_limit_per_turn:
1 -> 2` per un ramp-up giornaliero più rapido della workforce. Nessuna
variante è stata scartata selezionando sull'holdout; tutte le iterazioni
hanno usato esclusivamente il seed development `26090101`.

### 5.4 Perché i gate economico e fughe non sono ancora superati

Diagnosi coerente su tutte le 14 run: il dispatcher greedy con una
workforce ancora modesta (`hands_target_per_quadrant=3`, `max_hands=9`, con
reset giornaliero completo degli hands per fatto d'ambiente) deve coprire
fino a ~60 opportunità simultanee per 3 quadranti attivi (irrigazione,
raccolta, semina, cura, posizionamento). Con priorità `URGENT_WATER` e
`FEED_NEEDED` sempre in testa, il farmer da solo (unico worker persistente,
gli hands esistono solo per parte della giornata) non riesce a coprire ogni
esigenza di `FEED_NEEDED` prima che `consecutive_unfed` raggiunga 2 in ogni
run: questo produce le fughe residue osservate (`8` eventi derivati su 14
run, mai più di 2 per run). La stessa contesa sulla capacità di servizio
limita il numero di cicli colturali completati per episodio, tenendo
`final_money` un ordine di grandezza sotto il target `50 000`. Non è stata
osservata alcuna causa tecnica (errori, batch invalidi, azioni rifiutate in
modo sistematico): il ledger mostra copertura `100%` e nessun errore.

Ipotesi causale non ancora testata per un round successivo: aumentare
`hands_target_per_quadrant` oltre `3` senza ripetere la trappola di cassa di
Sezione 5.3 richiede una guardia di `HIRE` che scali con il fabbisogno di
servizio osservato (`service_pressure`), non solo con il numero di
quadranti; questa non è stata implementata in questa iterazione ed è
dichiarata come lavoro futuro, non come promozione mancata per errore.

### 5.5 Falsificazione delle ipotesi (MODEL_SPEC Sezione 10)

- `H-CR1` (guardie di manutenzione dominano): **parzialmente falsificata**.
  La guardia `URGENT_WATER` a priorità massima ha eliminato la perdita
  colturale da mancata irrigazione come causa dominante (nessuna evidenza di
  weed massiva da mancata acqua nelle run registrate), ma non è sufficiente
  da sola a garantire `ANIMAL_ESCAPES == 0` sotto la contesa di capacità
  osservata: la causa non è l'ordine delle guardie ma il numero di worker
  disponibili rispetto al carico.
- `H-CR2` (espansione condizionata): **confermata operativamente**. Tutte le
  14 run raggiungono 3 quadranti (`NW, NE, SW`) rispettando le guardie di
  cassa/capacità/orizzonte, senza collasso di `service_pressure` osservato
  dopo l'espansione.
- `H-CR3` (buffer/liquidazione reattivi): **non conclusiva** in questa
  iterazione. Il buffer WHEAT reattivo non ha prevenuto le fughe residue
  perché la causa binding è la disponibilità di worker per l'azione `FEED`,
  non la disponibilità di WHEAT nello shed (mai stata la causa diagnosticata
  nelle run osservate).

---

## 6. Limiti dichiarati

Vedi MODEL_SPEC Sezione 9 per l'elenco completo. In sintesi: nessuna
logistica dedicata di prelievo fertilizzante dallo shed (solo uso
opportunistico); nessuna riassegnazione dinamica della zona crop/livestock
dopo il primo sblocco quadrante; dispatch greedy per-step, non un solver di
assegnamento globale; nessuna guardia di `HIRE` che scali dinamicamente con
la pressione di servizio osservata (causa diagnosticata in Sezione 5.4).

---

## 7. Indipendenza strategica

Audit automatico (`_independence_audit` nello strumento di validazione,
ripetuto in `test_source_has_no_other_agent_strategy_dependency`):

```text
no_import_other_agent_routine: True
no_copy_other_agent_action_table: True
no_external_planner_dispatcher_or_schedule: True
fingerprint_distinct_from_codex_routine: True
```

Nessun import da `agricola.strategy.codex`, `agricola.strategy.antigravity`
o `agricola.strategy.copilot`. Nessuna tabella di azioni indicizzata per
step. I soli fatti riusati dell'ambiente condiviso sono documentati e
attribuiti nel MODEL_SPEC (Sezione 2) e nel docstring del sorgente.

---

## 8. Stato di ammissione e prossimi passi

`STRATEGIC_INDEPENDENCE`, `STATE_REACTIVITY_TEST`, `LEDGER_ACTION_PARITY` e
tutti i gate tecnici/di processo sono `PASS`. `ANIMAL_ESCAPES == 0` e
`DEVELOPMENT_MEAN_FINAL_MONEY >= 50000` sono `FAIL`, con diagnosi causale
riportata in Sezione 5.4-5.5 e senza alcuna alterazione dei risultati
osservati. La candidate non viene presentata come pronta per il torneo a tre
in questo stato: il proprietario del repository decide se autorizzare
un'ulteriore iterazione (guardia di `HIRE` scalata sulla pressione di
servizio) sui soli seed development, oppure procedere comunque al confronto
architetturale con Codex reattivo dichiarando esplicitamente i due gate non
superati.

Nessun seed holdout o final-confirmation è stato consumato da questo
sviluppo. Nessuna submission Kaggle, nessun commit, nessun push, nessuna
modifica a file di altri agenti o a documenti di stato condivisi è stata
eseguita.
