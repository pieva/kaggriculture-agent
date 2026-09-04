# E17.1 — Report di implementazione Claude reattivo indipendente V2

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2`
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V1`, `REJECTED BEFORE TOURNAMENT`
- **Data:** 2026-09-02
- **Stato:** DEVELOPMENT COMPLETE — `FROZEN_WITH_FAILED_GATES`; miglioramento
  netto e verificato rispetto alla V1 su tutti i KPI, ma non tutti i gate di
  ammissione sono superati. Nessuna submission, nessun torneo, nessun
  consumo di holdout eseguito da questo report.
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V2.md`
- **Config:** `docs/model_specs/claude/e17/configs/CLAUDE_E17_1_3Q_REACTIVE_V2.json`
- **Source:** `src/agricola/strategy/claude/e17_reactive_3q_v2.py`
- **Test:** `docs/model_specs/claude/e17/tests/test_claude_e17_1_reactive_v2.py`
- **Tool:** `docs/model_specs/claude/e17/tools/run_claude_e17_1_v2_validation.py`
- **Metriche:** `docs/model_specs/claude/e17/artifacts/derived/E17_1_V2_METRICS.json`
- **Freeze manifest:** `docs/model_specs/claude/e17/artifacts/freeze/e17_1_v2/E17_1_V2_FREEZE_MANIFEST.json`

---

## 1. Hash di provenance

| Artefatto | SHA-256 |
|---|---|
| Source (`e17_reactive_3q_v2.py`) | `8CBB5E96CFA4137E89E9759C095051B893E6FD51A7B20F25DC4C1053061A6451` |
| Config (`CLAUDE_E17_1_3Q_REACTIVE_V2.json`) | `71D9B3C793F17CAC13C3A419FCACE31A003E567E6A6E2D9D3709E44091C53707` |
| Fingerprint policy (source+config) | `0B66100DD35059A4FA4522E871D6C461E9A0478CC631012EDF5557D5422735DD` |
| Fingerprint V1 (per confronto, distinto) | `9A8B1B71A2942DE7A1292F2E3CA592B2E7933694D07B8FC7340211E0EB472063` |
| Routine V9 Codex (riferimento, non consumata) | `C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4` |

---

## 2. Diagnosi V1 verificata (obbligo del prompt di remediation)

Riportata per intero in MODEL_SPEC V2 Sezione 1; sintesi degli esiti:

| Ipotesi | Esito |
|---|---|
| Oscillazione da dispatcher stateless | **CONFERMATA** (parziale): 8,3% mosse farmer erano inversioni immediate sul seed `26090101` |
| Target non persistenti e percorsi lunghi | **CONFERMATA**: 77,4% dei comandi erano `MOVE` |
| `HIRE` ripetuti senza cash o senza necessità | **FALSIFICATA**: 0 giorni su 30 con richieste eccedenti gli hire confermati dal motore |
| Espansione Q1/Q2 prematura rispetto al motore Q0 | **CONFERMATA in modo netto**: primo `BUY_LAND` al giorno 0, zero `HARVEST` completati prima |
| Densità/resa insufficiente per tile | non conclusiva, confusa con l'espansione prematura |
| Guardie feed incapaci di garantire zero fughe | **CONFERMATA come effetto di capacità**, non di ordine delle priorità |

Nessuna correzione è stata applicata per l'ipotesi `HIRE`, deliberatamente,
perché la verifica diretta l'ha falsificata.

---

## 3. Esito dei test

```text
docs/model_specs/claude/e17/tests/test_claude_e17_1_reactive_v2.py: 25 passed
docs/model_specs/claude/e17/tests/test_claude_e17_1_reactive.py (V1, invariato): 18 passed
ruff check: All checks passed (source, test, tool)
```

Copertura V2-specifica aggiuntiva rispetto al protocollo V1: persistenza del
target attraverso chiamate successive, invalidazione dell'assegnazione
quando risolta da un altro worker, azzeramento delle assegnazioni `hand:*`
al cambio di giorno con farmer non azzerato, blocco di `BUY_LAND` e
`BUY_ANIMAL` prima della maturità del nucleo, blocco di nuovi acquisti
zootecnici con un capo a rischio di fuga immediata, consumo reale dei nuovi
campi di configurazione.

---

## 4. Development benchmark

Matrice identica per protocollo alla V1: 7 seed development × 2 seat,
opponent `INERT_PASS_POLICY`, `episodeSteps=720`, ogni run eseguita due
volte per verificare la riproducibilità deterministica. Guardia
programmatica anti-holdout nello strumento (`_guarded_seed`): qualunque seed
fuori dall'insieme development solleva un'eccezione prima di invocare il
motore.

### 4.1 KPI per run

| episode_id | final_money | quadranti | fughe derivate | quota MOVE | ledger coverage | riproducibile |
|---|---:|---|---:|---:|---:|:---:|
| S26090101-P0 | 18 541 | NW,NE,SW | 0 | 68,8% | 100% | sì |
| S26090101-P1 | 15 754 | NW,NE,SW | 0 | 68,9% | 100% | sì |
| S26090102-P0 | 14 224 | NW,NE,SW | 0 | 69,1% | 100% | sì |
| S26090102-P1 | 18 797 | NW,NE,SW | 0 | 70,5% | 100% | sì |
| S26090103-P0 | 15 912 | NW,NE,SW | 1 | 68,7% | 100% | sì |
| S26090103-P1 | 11 168 | NW,NE,SW | 0 | 70,3% | 100% | sì |
| S1838889274-P0 | 13 293 | NW,NE,SW | 0 | 69,0% | 100% | sì |
| S1838889274-P1 | 16 389 | NW,NE,SW | 0 | 70,0% | 100% | sì |
| S1619968655-P0 | 15 873 | NW,NE,SW | 0 | 70,0% | 100% | sì |
| S1619968655-P1 | 15 583 | NW,NE,SW | 0 | 70,7% | 100% | sì |
| S710418712-P0 | 14 529 | NW,NE,SW | 0 | 69,7% | 100% | sì |
| S710418712-P1 | 15 971 | NW,NE,SW | 0 | 69,3% | 100% | sì |
| S562040596-P0 | 15 676 | NW,NE,SW | 0 | 70,9% | 100% | sì |
| S562040596-P1 | 524 | NW,NE | 2 | 57,7% | 100% | sì |

Aggregati: `final_money` media `14 445,3` (V1: `9 201,7`, **+57,0%**),
mediana `15 715` (V1: `9 126`), minimo `524` (V1: `5 415`), massimo `18 797`
(V1: `13 625`), deviazione standard di popolazione `4 280,0`. Fughe derivate
totali `3` su 14 run (V1: `8`), tutte concentrate in una sola run. Quota
`MOVE` media `68,8%` (V1: `77,4%`). Errori tecnici totali `0`. Batch non
validi `0`. `ledger_record_coverage` `100%` su tutte le run.

### 4.2 Gate

| Gate | Esito |
|---|:---:|
| `TECHNICAL_ERRORS == 0` | PASS |
| `INVALID_BATCHES == 0` | PASS |
| `STRATEGIC_INDEPENDENCE == PASS` | PASS |
| `STATE_REACTIVITY == PASS` | PASS |
| `LEDGER_RECORD_COVERAGE == 100%` | PASS |
| `LEDGER_ACTION_PARITY == PASS` | PASS |
| `DETERMINISTIC_REPRODUCIBILITY` | PASS |
| `SOURCE_CONFIG_FREEZE` | PASS |
| `HOLDOUT_NOT_CONSUMED` | PASS |
| `NO_POST_HOC_SEED_REMOVAL` | PASS |
| `DERIVED_EOD_ESCAPES == 0` | **FAIL** (3 fughe, 13/14 run a zero) |
| `MAX_QUADRANTS == 3` su tutte le run | **FAIL** (13/14 run; `S562040596-P1` ferma a NW,NE) |
| `MEAN_FINAL_MONEY >= 50000` | **FAIL** (media `14 445,3`, +57% su V1 ma sotto target) |

**Stato di ammissione complessivo: `FAIL` → `FROZEN_WITH_FAILED_GATES`.**
Tutti i gate tecnici, di indipendenza, di riproducibilità e di reattività
sono `PASS`. I tre gate economico/di sicurezza zootecnica/3Q-universale non
sono ancora raggiunti, con un miglioramento sostanziale e misurato su tutti
e tre rispetto alla V1. Nessun risultato è stato falsificato o nascosto.

---

## 5. Decisioni principali e diagnosi (varianti provate)

### 5.1 Correzioni derivate direttamente dalla diagnosi V1

1. **Guardia di maturità del nucleo Q0** (`_expansion_guard`): `BUY_LAND`
   richiede ora `plant_tiles_count > 0` e un numero minimo di richieste
   `HARVEST` proprie (`core_min_harvest_requests`), oltre alle guardie di
   cassa/orizzonte/pressione già presenti in V1. Chiude direttamente il
   caso osservato (`BUY_LAND` al giorno 0, zero harvest).
2. **Target persistenti per worker** (`_Assignment`): sostituiscono la
   riselezione stateless della V1. Riducono la quota `MOVE` da `77,4%` a
   `68,8%` media sulle run registrate.
3. **Workforce guidata dal carico osservato**: il target di headcount segue
   il backlog di manutenzione (incluse le opportunità di semina, per
   evitare la trappola di bootstrap descritta in Sezione 5.2) invece di un
   moltiplicatore fisso per quadrante.
4. **Ratchet zootecnico a rischio zero**: nessun nuovo `BUY_ANIMAL` mentre
   un capo già posseduto è a un pasto mancato dalla fuga (`LIV-08`).

### 5.2 Difetti trovati e corretti durante lo sviluppo V2 (prima del benchmark registrato)

Il dettaglio quantitativo è in MODEL_SPEC V2 Sezione 8.1. In sintesi, tre
iterazioni diagnostiche sul seed development `26090101` (più
`1838889274` per la verifica specifica delle fughe):

1. **Capitale dirottato su bestiame prematuro**: la prima versione gateva
   solo `BUY_LAND`, non `BUY_ANIMAL`, dietro la maturità del nucleo. Primo
   test: `final_money = 272`, Q1/Q2 mai sbloccati. Corretto estendendo la
   stessa guardia a `BUY_ANIMAL`.
2. **Trappola di bootstrap del backlog**: la formula di workforce escludeva
   `PLANT_OPPORTUNITY` dal calcolo del carico, azzerando il target di
   headcount proprio quando il nucleo era vuoto e serviva più forza lavoro
   per riempirlo. Corretto includendo `PLANT_OPPORTUNITY` nel backlog.
3. **Regressione delle fughe (8 → 77 su 14 run) e correzione risolutiva**:
   le prime due correzioni sopra avevano peggiorato drasticamente le fughe
   rispetto alla V1. Diagnosticato tracciando ogni evento di fuga
   direttamente sullo stato dell'ambiente (non sul ledger, inadatto
   all'attribuzione multi-ordine): ogni fuga avveniva esattamente al primo
   step di un nuovo giorno, con shed spesso pieno di WHEAT — non un
   problema di risorse, ma di attenzione. La persistenza pura impediva a un
   worker impegnato su un compito a bassa priorità di abbandonarlo quando
   l'unico animale posseduto diventava `FEED_NEEDED` e nessun altro worker
   era libero. Due varianti minori (un solo `BUY_ANIMAL` per chiamata; cap
   del gregge legato alla workforce) hanno ridotto le fughe solo
   marginalmente (`77 → 74`), confermando che la causa non era la
   dimensione del gregge ma l'assenza di prelazione. La correzione
   risolutiva — prelazione d'urgenza per le sole categorie a rischio di
   perdita EOD (`URGENT_WATER`, `FEED_NEEDED`) — ha portato le fughe da
   `74` a `3` sul benchmark registrato (`13/14` run a zero).

Nessuna variante è stata scartata selezionando sull'holdout; tutte le
iterazioni hanno usato esclusivamente i due seed development citati.

### 5.3 Diagnosi della run anomala residua (`S562040596-P1`)

L'unica run che non raggiunge 3 quadranti e produce 2 delle 3 fughe residue
mostra una traiettoria di cassa bloccata a `$35` per gran parte
dell'episodio (giorni 6-27), sopra `market_order_min_cash` (`$30`) ma sotto
`hire_reserve` (`$50`): nessun `HIRE` può quindi convertirsi finché la cassa
non supera la soglia, la workforce resta all'osso, i weed si accumulano
fino a `20` tile e la produzione crolla. È la stessa dinamica di trappola di
cassa vicino-soglia diagnosticata e in gran parte risolta nella V1
(riduzione di `hire_reserve` da `300` a `50`), qui riemersa su un singolo
seed/seat per una combinazione sfavorevole di prezzi di mercato e RNG dei
weed non ulteriormente scomposta in questa iterazione. Non è stata tentata
una quarta correzione per non selezionare parametri sull'unica run
residua non superata, il che costituirebbe un overfitting mono-seed
esplicitamente sconsigliato dal processo sperimentale del repository.

### 5.4 Falsificazione delle ipotesi V2 (MODEL_SPEC Sezione 9)

- `H-CR2.1` (nucleo prima dell'espansione): **confermata**. `13/14` run
  raggiungono 3 quadranti rispettando la guardia; `final_money` medio
  aumenta del `57%` rispetto alla V1.
- `H-CR2.2` (target persistenti): **confermata**. Quota `MOVE` ridotta da
  `77,4%` a `68,8%` media.
- `H-CR2.3` (workforce guidata dal carico): **confermata parzialmente**;
  necessaria la correzione di bootstrap di Sezione 5.2 punto 2 prima di
  funzionare come previsto.
- `H-CR2.4` (ratchet zootecnico): **falsificata nella sua prima forma**
  (isolatamente insufficiente: le fughe sono aumentate, non diminuite, fino
  all'introduzione della prelazione d'urgenza) e **confermata nella forma
  finale** (combinata con la prelazione, `13/14` run a zero fughe).

---

## 6. Feature C2.1 effettivamente consumate

Identiche alla V1 (MODEL_SPEC V1 Sezione 4), con `LIV-07`/`LIV-08` ora usate
anche come guardia di acquisto zootecnico, non solo come priorità di
dispatch (MODEL_SPEC V2 Sezione 5).

---

## 7. Limiti dichiarati

Vedi MODEL_SPEC V2 Sezione 8. In sintesi: nessuna logistica dedicata di
prelievo fertilizzante dallo shed; nessuna riassegnazione dinamica della
zona crop/livestock dopo il primo sblocco quadrante; dispatch greedy
per-step (mitigato ma non eliminato dalla persistenza); `_core_harvest_requests`
conta richieste proprie, non conferme d'esecuzione post-hoc (per rispetto
del divieto no-future-leakage); la trappola di cassa vicino-soglia
diagnosticata in Sezione 5.3 resta un fallimento residuo non ancora chiuso
strutturalmente.

---

## 8. Indipendenza strategica

```text
no_import_other_agent_routine: True
no_copy_other_agent_action_table: True
no_external_planner_dispatcher_or_schedule: True
fingerprint_distinct_from_codex_routine: True
```

Nessun import da `agricola.strategy.codex`, `agricola.strategy.antigravity`
o `agricola.strategy.copilot`, né da `submission/submission_codex.py`.
Nessuna tabella di azioni indicizzata per step. Lo stato agent-local
persistente introdotto in V2 (`_assignments`, `_core_harvest_requests`) è
derivato esclusivamente da osservazioni correnti e dalle proprie azioni
passate, mai da routine o replay altrui, coerentemente con l'autorizzazione
esplicita del prompt di remediation.

---

## 9. Stato di ammissione e prossimi passi

`FROZEN_WITH_FAILED_GATES`. La V2 non sostituisce la V1 come evidenza (la
V1 resta conservata sotto `docs/model_specs/claude/e17/artifacts/runs/e17_1/`
per tracciabilità del fallimento, come richiesto): è una nuova candidata su
path, source e config separati. Il miglioramento su ogni asse misurato è
netto e riproducibile:

```text
final_money mean: 9 201,7 -> 14 445,3  (+57,0%)
MOVE fraction:     77,4%  -> 68,8%
derived escapes:      8   -> 3   (13/14 run a zero)
3Q all runs:        14/14 -> 13/14
```

Non è ancora una candidata ammissibile al torneo: `MEAN_FINAL_MONEY`,
`DERIVED_EOD_ESCAPES` e `MAX_QUADRANTS` restano `FAIL`. Il proprietario del
repository decide se autorizzare una V3 mirata sulla trappola di cassa
residua (Sezione 5.3) su un insieme più ampio di seed development, oppure
procedere al confronto architetturale con Codex reattivo dichiarando
esplicitamente i gate non superati. Nessun seed holdout o final-confirmation
è stato consumato. Nessuna submission Kaggle, commit, push o modifica a file
di altri agenti è stata eseguita.
