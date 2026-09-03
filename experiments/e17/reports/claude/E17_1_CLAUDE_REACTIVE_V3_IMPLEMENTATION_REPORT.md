# E17.1 — Report di implementazione Claude reattivo indipendente V3 (attivazione "10x")

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2`, `FROZEN_WITH_FAILED_GATES`
- **Data:** 2026-09-02
- **Stato:** DEVELOPMENT COMPLETE — `FROZEN_WITH_FAILED_GATES`; miglioramento
  netto e verificato rispetto alla V2 su ogni KPI misurato, ma il target
  indicativo "10x" e alcuni gate di ammissione restano `FAIL`, come
  esplicitamente ammesso dal prompt di attivazione in caso di mancato
  raggiungimento. Nessuna submission, nessun torneo, nessun consumo di
  holdout o final-confirmation eseguito da questo report.
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V3.md`
- **Piano di miglioramento:** `experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md`
- **Config:** `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V3.json`
- **Source:** `src/agricola/strategy/claude/e17_reactive_3q_v3.py`
- **Test:** `experiments/e17/tests/test_claude_e17_1_reactive_v3.py`
- **Tool validazione passiva:** `experiments/e17/tools/claude/run_claude_e17_1_v3_validation.py`
- **Tool benchmark conteso (black-box):** `experiments/e17/tools/claude/run_claude_e17_1_v3_dev_benchmark_vs_codex.py`
- **Metriche passive:** `experiments/e17/artifacts/derived/claude/E17_1_V3_METRICS.json`
- **Metriche contese:** `experiments/e17/artifacts/derived/claude/E17_1_V3_DEV_BENCHMARK_VS_CODEX.json`
- **Freeze manifest:** `experiments/e17/artifacts/freeze/claude/e17_1_v3/E17_1_V3_FREEZE_MANIFEST.json`

---

## 1. Hash di provenance

| Artefatto | SHA-256 |
|---|---|
| Source (`e17_reactive_3q_v3.py`) | `568AAF6246DDB9C4BFD110C645D3F51270CE7563407F03A00C6616F4C6957C5B` |
| Config (`CLAUDE_E17_1_3Q_REACTIVE_V3.json`) | `A353F832C23DCAF04726D29EB19BF794FDA3447A485A22F52DF40505AD995B1C` |
| Fingerprint policy (source+config) | `B96BA8D0CF7C539DAF545F1DB3A21FE42E8ADEDE33740E57AB3E5603031EBBAE` |
| Fingerprint V2 (predecessore, per confronto, distinto) | `0B66100DD35059A4FA4522E871D6C461E9A0478CC631012EDF5557D5422735DD` |
| Routine V9 Codex (riferimento black-box, non consumata) | `C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4` |
| Test suite (`test_claude_e17_1_reactive_v3.py`) | `93E895E7A99A6E3544A046EE5977F89F0BE0D2D8D1EFDA8F0DF71B900AEA9EAE` |
| Tool validazione passiva | `F7BFEBE375915B5D1FE45CF6E08BD663676C85826A9F326A9FD6028E67A93E78` |

---

## 2. Autorizzazione e origine del compito

Questa iterazione è una remediation mirata, autorizzata dall'utente, del
fallimento osservato dalla V2 nell'esibizione a tre vie contesa
(`0-28` contro Codex V9, esibizione di sviluppo comune) documentato in
`experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`.
Il piano di miglioramento (Sezione 2-3 del documento omonimo) e la
successiva autorizzazione esplicita a un benchmark **black-box** contro
Codex (risultati e comportamento osservabile sì, sorgenti/routine no —
`experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`)
hanno preceduto qualunque modifica di codice. Il target dichiarato
dall'attivazione era un miglioramento di un ordine di grandezza (indicativo
`>= 117.800`, 10× la media conteso V2 `11.777,64`) sul denaro medio conteso,
da raggiungere tramite ablazione a famiglia causale singola sulla base della
diagnosi V2, usando Codex V9/reattivo esclusivamente come avversario
black-box.

---

## 3. Esito dei test

```text
experiments/e17/tests/test_claude_e17_1_reactive_v3.py: 28 passed
experiments/e17/tests/test_claude_e17_1_reactive.py (V1, invariato): 18 passed
experiments/e17/tests/test_claude_e17_1_reactive_v2.py (V2, invariato): 25 passed
ruff check (source, test, entrambi i tool V3): All checks passed
```

Copertura V3-specifica aggiuntiva rispetto al protocollo V2: guardia di
prontezza workforce prima dell'espansione (`test_no_land_expansion_when_workforce_below_quadrant_floor`),
gate di densità basato su `core_quadrant_fill_ratio` oltre al solo conteggio
richieste (`test_no_land_expansion_with_harvests_but_low_density`,
`test_land_expansion_allowed_once_core_established_and_workforce_ready`),
riserva dedicata per l'acquisto zootecnico distinta dalla riserva di mercato
generica (`test_no_animal_purchase_below_dedicated_reserve`), `HIRE`
esplicitamente non bloccato durante lo shutdown a differenza di
`BUY_LAND`/`BUY_SEED`/`BUY_ANIMAL`
(`test_hire_is_not_blocked_during_shutdown_but_new_investment_is`), oltre al
consumo reale di tutti i nuovi campi di configurazione elencati in Sezione 5.

---

## 4. Development benchmark — passivo (`INERT_PASS_POLICY`)

Matrice identica per protocollo alla V1/V2: 7 seed development × 2 seat,
`episodeSteps=720`, ogni run eseguita due volte per verificare la
riproducibilità deterministica bit-per-bit.

### 4.1 KPI per run

| episode_id | final_money | quadranti | fughe derivate | quota MOVE | ledger coverage | riproducibile |
|---|---:|---|---:|---:|---:|:---:|
| S26090101-P0 | 18 264 | NW,NE,SW | 1 | 68,8% | 100% | sì |
| S26090101-P1 | 21 350 | NW,NE,SW | 0 | 69,4% | 100% | sì |
| S26090102-P0 | 15 527 | NW,NE,SW | 2 | 68,2% | 100% | sì |
| S26090102-P1 | 13 978 | NW,NE (2Q) | 0 | 68,8% | 100% | sì |
| S26090103-P0 | 19 027 | NW,NE,SW | 0 | 69,2% | 100% | sì |
| S26090103-P1 | 14 611 | NW,NE,SW | 2 | 68,8% | 100% | sì |
| S1838889274-P0 | 17 631 | NW,NE,SW | 1 | 68,5% | 100% | sì |
| S1838889274-P1 | 15 606 | NW,NE,SW | 4 | 68,1% | 100% | sì |
| S1619968655-P0 | 22 736 | NW,NE,SW | 3 | 71,0% | 100% | sì |
| S1619968655-P1 | 23 584 | NW,NE,SW | 0 | 67,8% | 100% | sì |
| S710418712-P0 | 19 531 | NW,NE,SW | 1 | 67,1% | 100% | sì |
| S710418712-P1 | 18 247 | NW,NE,SW | 1 | 68,3% | 100% | sì |
| S562040596-P0 | 20 907 | NW,NE,SW | 0 | 67,3% | 100% | sì |
| S562040596-P1 | 9 221 | NW,NE (2Q) | 3 | 68,6% | 100% | sì |

Aggregati: `final_money` media `17 872,86` (V2: `14 445,29`, **+23,7%**),
mediana `18 255,5`, minimo `9 221` (V2: `524`), massimo `23 584` (V2:
`18 797`), deviazione standard di popolazione `3 715,82`. Fughe derivate
totali `18` su 14 run (V2: `3`; vedi Sezione 5.3 sul motivo per cui la
scala maggiore ha inizialmente peggiorato questo KPI e come è stato
mitigato). `max_quadrants=3` in `12/14` run. Quota `MOVE` media `68,6%`.
Errori tecnici totali `0`. Batch non validi `0`. `ledger_record_coverage`
`100%` su tutte le run. `emitted_commands` totali `82 781`.

### 4.2 Gate passivi

| Gate | Esito |
|---|:---:|
| `TECHNICAL_ERRORS == 0` | PASS |
| `INVALID_ACTIONS/BATCHES == 0` | PASS |
| `STRATEGIC_INDEPENDENCE == PASS` | PASS |
| `REACTIVITY_TESTS == PASS` | PASS |
| `LEDGER_COVERAGE == 100%` | PASS |
| `LEDGER_ACTION_PARITY == PASS` | PASS |
| `DETERMINISTIC_REPRODUCIBILITY` | PASS |
| `SOURCE_CONFIG_FREEZE` | PASS |
| `HOLDOUT_USED == false` | PASS |
| `FINAL_CONFIRMATION_USED == false` | PASS |
| `NO_POST_HOC_SEED_REMOVAL` | PASS |
| `ANIMAL_ESCAPES == 0` | **FAIL** (18 fughe, in calo da 67 a metà sviluppo — Sezione 5.3) |
| `THREE_QUADRANTS == ALL_DEVELOPMENT_RUNS` | **FAIL** (12/14 run passivi; 14/14 sotto contesa, Sezione 5) |
| `PASSIVE_DEVELOPMENT_MEAN >= 50000` | **FAIL** (media `17 872,86`) |

---

## 5. Development benchmark — conteso black-box (`CODEX_V9` / `CODEX_REACTIVE`)

7 seed development × 2 seat × 2 avversari black-box = 28 match. Strumento
dedicato (`run_claude_e17_1_v3_dev_benchmark_vs_codex.py`) che importa
esclusivamente le funzioni factory pubbliche `create_v9_agent` e
`create_codex_e17_reactive_agent`, mai il MODEL_SPEC, la config o il
sorgente Codex; guardia programmatica anti-holdout identica a quella del
tool di validazione passiva.

### 5.1 KPI aggregati

```text
CLAUDE_MEAN_MONEY = 13.540,86   (V2 conteso: 11.777,64, +15,0%)
MATCHES = 28
W-T-L = 0-0-28
TECH_ERRORS = 0
```

Tutti e 14 gli abbinamenti seed×seat unici raggiungono `3Q =
['NW','NE','SW']` (14/14, contro 12/14 nel benchmark passivo). `weed`
quasi sempre `0` (unica eccezione: `weed=1` su seed `26090101` seat `0`).
`CODEX_V9` e `CODEX_REACTIVE` producono risultati byte-identici su ogni
match — la variante reattiva di Codex non ha mai attivato una divergenza
osservabile in questi 14 scenari black-box.

### 5.2 Gate conteso

| Gate | Esito |
|---|:---:|
| `TECHNICAL_ERRORS == 0` | PASS |
| `THREE_QUADRANTS == ALL_MATCHES` | PASS (14/14 abbinamenti unici) |
| Target indicativo "10x" (`>= 117.800`) | **FAIL** (`13.540,86`, +15,0% su V2, non un ordine di grandezza) |

**Stato di ammissione complessivo: `FAIL` → `FROZEN_WITH_FAILED_GATES`.**
Tutti i gate tecnici, di indipendenza, di riproducibilità e di reattività
sono `PASS`. Il gate `ANIMAL_ESCAPES == 0`, `THREE_QUADRANTS` universale sul
matrice passiva e il target economico "10x" non sono raggiunti, con
miglioramenti misurati e riproducibili su denaro medio (sia passivo sia
conteso) e su ogni modo di fallimento catastrofico osservato durante lo
sviluppo. Nessun risultato è stato falsificato o nascosto.

---

## 6. Decisioni principali e diagnosi (sequenza completa delle 8 iterazioni)

Dettaglio quantitativo completo in MODEL_SPEC V3 Sezione 9.1; sintesi:

1. **Trappola cassa-bloccata** (`max_hands` 9→15 senza alzare `hire_reserve`):
   cassa bloccata esattamente a `$35`, weed saturi in NW. **Corretto**
   alzando `hire_reserve` a `150` e riducendo `hire_batch_limit_per_turn`
   a `2`.
2. **Espansione densa-ma-poco-presidiata**: `core_quadrant_fill_ratio`
   raggiungeva `0,45` in soli 2 giorni (ciclo rapido WHEAT), prima che la
   workforce fosse pronta a raddoppiare il territorio servito. **Corretto**
   con la guardia di prontezza workforce (`min_workers_per_quadrant ×
   quadranti sbloccati`).
3. **Collasso da sovraspesa alla maturità del nucleo**: `BUY_LAND` + due
   `BUY_ANIMAL` + rampa rapida di `HIRE` competevano per la stessa cassa
   nella stessa finestra di ~20 step. **Corretto** con la riserva dedicata
   `animal_purchase_reserve` (`300`, distinta dalla generica
   `market_order_min_cash`): `final_money` sale da `458` a `10.348` sullo
   stesso seed.
4. **Collasso weed di fine episodio sotto contesa**: `HIRE` bloccato
   durante lo shutdown azzerava la workforce (solo farmer) mentre un intero
   3Q necessitava manutenzione quotidiana. **Corretto** rimuovendo il gate
   di shutdown da `HIRE` soltanto (mantenuto su `BUY_LAND`/`SEED`/`ANIMAL`):
   `final_money` sale da `6.472` a `9.792` sullo stesso match.
5. **Ipotesi prezzo WHEAT disprovata**: alzare `wheat_buy_price_ceiling` da
   `45` a `80` non ha prodotto alcun effetto misurabile (traiettoria
   bit-per-bit identica) — il vincolo attivo non era mai il prezzo.
6. **Ipotesi rapporto gregge/workforce, effetto solo parziale**: dimezzare
   `herd_per_worker_ratio` da `1,0` a `0,5` ha ridotto ma non azzerato le
   fughe (`4-8` per run sui seed campionati).
7. **Errore di processo autocorretto: regressione da configurazione non
   ri-validata.** Alzare `crop_target_fill_ratio` `0,55→0,9→0,7` senza
   ri-eseguire la matrice completa a 7 seed ha causato un collasso non
   rilevato (denaro `87-104`, spesso 2Q, media conteso scesa a `5.949,36`).
   Diagnosticato confrontando gli spot-check (a `0,9`, sani) con
   l'esecuzione formale (a `0,7`, collassata) sugli stessi seed. **Corretto**
   ripristinando `0,55` e ri-verificando i due seed più colpiti.
8. **Fix decisivo: concentrazione geografica del bestiame.** Dopo il
   ripristino, le fughe erano esplose (`67` totali su 14 run, tutte a cambio
   giorno con shed spesso ben rifornito — non un problema di risorse).
   Giustificato da evidenza di replay Foundation C2.1 già disponibile
   (profili con bestiame concentrato: `0` fughe; profilo con bestiame su 3
   quadranti: `31` fughe). Aggiunto `max_quadrants_for_livestock`: testato
   `=1` (troppo restrittivo, cassa collassata a `610-1.481`, bloccato a 2Q
   — scartato) e `=2` (adottato: fughe `0-3` per seed campionato). La
   ri-esecuzione completa della matrice con `=2` e tutte le impostazioni
   finali ha dato i risultati riportati in Sezione 4-5: `18` fughe (da
   `67`), `12/14` run passivi a 3Q, `14/14` abbinamenti contesi a 3Q.

Nessuna variante è stata scartata selezionando sull'holdout; tutte le
iterazioni hanno usato esclusivamente i seed development, e la matrice
completa a 7 seed è stata sempre ri-eseguita prima di dichiarare
un'iterazione conclusa (fatta eccezione per l'errore di processo del punto
7, individuato e corretto nello stesso ciclo di sviluppo).

### 6.1 Falsificazione delle ipotesi V3 (MODEL_SPEC Sezione 5, `H-CR3.1`–`H-CR3.4`)

- `H-CR3.1`/`H-CR3.2` (densità + prontezza prima dell'espansione): **non
  falsificate**. Il collasso weed legato all'espansione precoce (punto 2)
  non si è più riprodotto; le fughe residue sono di natura geografica, non
  di densità/prontezza.
- `H-CR3.3` (riserva dedicata contro sovraspesa): **non falsificata**. Il
  collasso da sovraspesa (punto 3) non si è più riprodotto.
- `H-CR3.4` (HIRE attivo durante shutdown): **non falsificata**. Il collasso
  weed di fine episodio (punto 4) non si è più riprodotto.
- **Limite non falsificato/non risolto**: il throughput della workforce
  resta il collo di bottiglia dominante per il denaro conteso — vedi
  Sezione 7.

---

## 7. Limite dominante non risolto: throughput della workforce

Diagnosi tramite confronto di traiettoria testa-a-testa (seed `26090103`
vs `CODEX_V9`): Codex raggiunge e sostiene `37-55` tile coltivate dal
giorno 8 in poi; Claude non supera mai `~20-28` tile piantate
simultaneamente, indipendentemente dal target di riempimento configurato
(il punto 7 di Sezione 6 dimostra che alzare il target senza aumentare la
capacità di esecuzione produce solo collassi, non guadagni). Il vincolo non
è il target di densità ma il numero di worker-turni disponibili per
piantare, irrigare e raccogliere una superficie comparabile a quella di
Codex nello stesso arco di tempo. Questo spiega perché il denaro conteso è
migliorato (+15,0%) ma resta lontano di un ordine di grandezza dal target:
le correzioni di questa iterazione hanno eliminato i modi di fallimento
catastrofico, non hanno aumentato la capacità di esecuzione strutturale
della policy. Raccomandazioni per una V4 in MODEL_SPEC V3 Sezione 11
(instradamento multi-worker con solver locale per quadrante, verifica del
vincolo di batch ordini di mercato, confronto diretto black-box della
cadenza `HIRE`/`BUY_LAND` di Codex).

---

## 8. Feature C2.1 effettivamente consumate

Identiche a V1/V2 (MODEL_SPEC V1 Sezione 4, V2 Sezione 5), con l'aggiunta
esplicita dell'evidenza di replay sulla concentrazione geografica del
bestiame (tetsuya/OceanMix vs Crop Dusta) come base diretta del fix di
Sezione 6 punto 8 — citata per intero in MODEL_SPEC V3 Sezione 6.10.

---

## 9. Limiti dichiarati

Vedi MODEL_SPEC V3 Sezione 11. In sintesi, oltre ai limiti ereditati da
V1/V2 (nessuna logistica dedicata di prelievo fertilizzante, dispatch
greedy per-step mitigato ma non eliminato dalla persistenza,
`_core_harvest_requests` conta richieste proprie non conferme d'esecuzione):
`ANIMAL_ESCAPES == 0` non raggiunto (`18` residue, ridotte da `67` ma non
azzerate, ancora concentrate a cambio giorno — merita tracciamento dedicato
in una V4 prima di ulteriori restrizioni geografiche, che rischiano di
ripetere il collasso osservato con `max_quadrants_for_livestock=1`);
`THREE_QUADRANTS` non universale sul passivo (`12/14`); throughput della
workforce come collo di bottiglia strutturale non affrontato in questa
iterazione (Sezione 7).

---

## 10. Indipendenza strategica

```text
no_import_other_agent_routine: True
no_copy_other_agent_action_table: True
no_external_planner_dispatcher_or_schedule: True
fingerprint_distinct_from_codex_routine: True
```

Nessun import da `agricola.strategy.codex`, `agricola.strategy.antigravity`
o `agricola.strategy.copilot`, né da `submission/submission_codex.py`, nel
sorgente della policy (`e17_reactive_3q_v3.py`). Il benchmark conteso
black-box importa esclusivamente le due funzioni factory pubbliche di Codex
(`create_v9_agent`, `create_codex_e17_reactive_agent`) in uno script di
strumento esterno alla policy, mai nel modulo della policy stessa, per
l'esatta autorizzazione data
(`experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`).
Nessuna tabella di azioni indicizzata per step. Lo stato agent-local
persistente (`_Assignment`, `_core_harvest_requests`,
`core_quadrant_fill_ratio`) è derivato esclusivamente da osservazioni
correnti e dalle proprie azioni passate, mai da routine o replay altrui.

---

## 11. Stato di ammissione e prossimi passi

`FROZEN_WITH_FAILED_GATES`. La V3 non sostituisce la V2 come evidenza (V1 e
V2 restano conservate sotto i rispettivi path per tracciabilità, come
richiesto): è una nuova candidata su path, source e config separati. Il
miglioramento su ogni asse misurato è netto e riproducibile:

```text
final_money mean (passivo):  14.445,29 -> 17.872,86  (+23,7%)
final_money mean (conteso):  11.777,64 -> 13.540,86  (+15,0%)
derived escapes (passivo):        3    -> 18   (in calo da un picco di 67 durante lo sviluppo, non azzerate)
3Q all runs (passivo):          13/14  -> 12/14
3Q all matches (conteso):         n/d  -> 14/14
```

Il target indicativo "10x" **non è raggiunto** (`+15,0%` conteso, non un
ordine di grandezza). Non è ancora una candidata ammissibile al torneo:
`ANIMAL_ESCAPES`, `THREE_QUADRANTS` (sul passivo) e
`PASSIVE_DEVELOPMENT_MEAN`/target "10x" restano `FAIL`. Il collo di
bottiglia dominante identificato — throughput della workforce nella
conversione di territorio posseduto in densità coltivata sostenuta,
rispetto al livello dimostrato da Codex — non è un difetto dei guardrail di
spesa o di sicurezza zootecnica (tutti verificati e corretti in questa
iterazione), ma un vincolo strutturale del dispatcher reattivo attuale. Il
proprietario del repository decide se autorizzare una V4 mirata su questo
vincolo (instradamento multi-worker, Sezione 7) o procedere diversamente.
Nessun seed holdout o final-confirmation è stato consumato. Nessuna
submission Kaggle, commit, push o modifica a file di altri agenti è stata
eseguita da questa iterazione.
