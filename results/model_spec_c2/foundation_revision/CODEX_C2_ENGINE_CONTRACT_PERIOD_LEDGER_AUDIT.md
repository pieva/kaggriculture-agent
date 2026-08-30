# C2 â€” Codex Engine Contract / Period Ledger Audit

```text
AGENT: CODEX
PHASE: DEFINE / FOUNDATION AUDIT
TASK_ID: C2-ENGINE-CONTRACT-PERIOD-LEDGER-AUDIT
SCOPE: ENGINE SEMANTICS ONLY
AUDIT_DATE: 2026-08-30
```

## 1. Executive verdict

L'audit ricostruisce e congela, per il runtime locale identificato nella sezione 2, il clock, l'ordine delle transizioni, l'inventario delle specie e le regole biologiche necessarie al futuro lavoro di Foundation. Il period ledger Ã¨ `READY_FOR_INDEPENDENT_REVIEW`.

Esito sostanziale:

- l'inventario animale canonico Ã¨ `GOOSE`, `COW`, `SHEEP`; `CHICKEN` Ã¨ `NOT_SUPPORTED` nel runtime verificato;
- `turnsPerDay` Ã¨ configurabile e nessun periodo espresso in step puÃ² essere congelato universalmente come 24/48/72/96;
- in uno stato engine valido vale l'invariante numerico `step == day * turnsPerDay + hour`;
- un animale al primo giorno non alimentato, se non ha ancora raggiunto la soglia di fuga, produce comunque il base output nel giorno biologico previsto;
- `FEED` impedisce la fuga, abilita il consumo del bonus giÃ  accumulato e, con `CARE`, accumula bonus futuro; non Ã¨ il gate del base output;
- il fertilizzante rende l'incremento di resa pari a 2 invece di 1: l'uplift rispetto al caso base Ã¨ `+1`, non `+2 addizionali`;
- la perdita da overflow puÃ² avvenire sia nel drop automatico EOD sia nell'azione manuale `DROP`; non Ã¨ esclusivamente EOD;
- i P0 trovati nella Foundation corrente sono tutti risolti a livello di engine contract, ma non sono stati modificati i file Foundation.

Questo Ã¨ un audit di dominio, non una strategia. Non autorizza MODEL_SPEC, build, tournament o Kaggle. Il passo successivo previsto Ã¨ la revisione indipendente di questo contratto da parte di Antigravity e Copilot.

## 2. Engine identity, version e fingerprint

| Campo | Valore verificato |
|---|---|
| `ENGINE_PACKAGE` | `kaggle-environments` |
| `ENGINE_VERSION` | package `1.32.7`; environment metadata `0.1.0` |
| `ENGINE_SOURCE_ROOT` | `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture` |
| `GIT_COMMIT_OR_HASH` | nessun commit Git incorporato nel wheel installato; fingerprint aggregato SHA-256 `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d` |
| `RELEVANT_CONFIG` | `kaggriculture.json` |
| `turnsPerDay` | integer configurabile, default `24`, minimo `1` |
| `EPISODE_LENGTH` | `episodeSteps`, default `720` |
| `boardSize` | default `10` |
| `shedCapacity` | default `100` |
| `maxMarketOrdersPerTurn` | default `10` |
| `DATE_OF_AUDIT` | `2026-08-30` |

### 2.1 Specifica canonica di aggregazione

La serializzazione del fingerprint, resa esplicita dalla correzione `AGG-01` del 2026-08-31, Ã¨:

```text
PATH_ROOT: repository worktree root
PATH_SEPARATOR: /
PATH_CASE: preserved exactly as listed in the canonical manifest
SORT_ORDER: ascending Unicode code-point order, case-sensitive,
            by normalized relative path
FILE_HASH: SHA-256 of raw file bytes, lowercase hexadecimal
RECORD: normalized_relative_path + HTAB (0x09) + lowercase_file_sha256
TEXT_ENCODING: UTF-8
LINE_SEPARATOR_BETWEEN_RECORDS: LF (0x0A)
TRAILING_NEWLINE: NO
BOM: NO
PAYLOAD_LENGTH: 702 bytes
AGGREGATE: SHA-256 of the serialized payload bytes
```

In formula, dove `records` Ã¨ giÃ  ordinato con la regola case-sensitive sopra:

```text
payload = UTF8_NO_BOM(join(records, "\n"))
aggregate_sha256 = SHA256(payload)
```

Il precedente pseudocodice usava `sort(...)` senza dichiararne collation/case sensitivity e non esplicitava root, trailing newline o BOM. Il valore pubblicato era comunque quello prodotto dalla procedura canonica qui definita.

### 2.2 Manifest canonico

```text
.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA	5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md	e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md	3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json	a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py	bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
```

Il manifest Ã¨ esattamente il contenuto tra le fence, esclusi fence e newline che le delimitano. Non esiste LF dopo l'ultimo carattere esadecimale del record `kaggriculture.py` nel payload sottoposto a hash.

Comando PowerShell indipendente, da eseguire dalla repository root:

```powershell
.\.venv\Scripts\python.exe -c 'from pathlib import Path; import hashlib; ps=[Path(x) for x in (".venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py")]; es=sorted(((p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()) for p in ps),key=lambda x:x[0]); rows=[p+"\t"+h for p,h in es]; payload="\n".join(rows).encode("utf-8"); print("\n".join(rows)); print("AGGREGATE_SHA256="+hashlib.sha256(payload).hexdigest())'
```

Output aggregate atteso:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

La review Copilot aveva riportato `1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d`. Quel digest non Ã¨ riproducibile dal manifest sopra con la procedura dichiarata nÃ© con le comuni varianti di newline, collation, path separator, encoding o trailing newline. La correzione completa e le prove negative sono documentate in `CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md`.

Tutte le formule congelate in questo report valgono per questo fingerprint. Un cambio anche di un solo file richiede almeno un diff audit prima di riusarle.

## 3. Source inventory e gerarchia delle prove

| Fonte | Regioni/simboli consultati | Ruolo | SHA-256 |
|---|---|---|---|
| `kaggriculture.py` | `CROPS`, `ANIMALS`, `_new_plant`, `_new_animal`, `_apply_unit_action`, `_process_market`, `_commit_unit`, `_decay_plants`, `_daily_refresh_plants`, `_daily_refresh_animals`, `_drop_inventories_to_shed`, `_end_of_day`, `interpreter` | fonte primaria normativa | `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e` |
| `kaggriculture.json` | environment version e configuration schema | metadata/config primaria | `a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867` |
| package `METADATA` | package name/version | provenance runtime | `5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add` |
| `README.md` | documentazione di controllo | fonte secondaria, mai prevalente sul codice | `3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00` |
| `AGENTS.md` | istruzioni e note dell'environment | contesto locale, non fonte delle formule | `e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22` |

Non sono presenti test engine-specific nel source root installato. Per il P0 animale sono state quindi eseguite transizioni deterministiche sulla funzione `_daily_refresh_animals` estratta direttamente dall'AST del source fingerprintato, senza ricopiarne la logica. I quattro replay sono usati soltanto nella sezione 17 come `EMPIRICAL_VALIDATION`.

Gerarchia applicata:

```text
CODICE RUNTIME + CONFIG
> TRANSIZIONE DETERMINISTICA RIPRODUCIBILE
> DOCUMENTAZIONE DELLO STESSO PACKAGE
> FOUNDATION CORRENTE
> REPLAY / POLICY OSSERVATA
```

## 4. Clock contract

### 4.1 UnitÃ  e invarianti

Sia `T = turnsPerDay`.

| Concetto | Contratto canonico | Stato |
|---|---|---|
| `step` | contatore discreto 0-indexed letto da `observation.step`; Ã¨ l'unitÃ  canonica infra-day | `ENGINE_VERIFIED` |
| `turn` | una invocazione decisionale/interpreter sullo stato corrente; nel codice non esiste un secondo contatore autonomo distinto da `step` | `ENGINE_VERIFIED` |
| `day` | `floor(step / T)` per la transizione corrente | `ENGINE_VERIFIED` |
| `hour` | nel next state Ã¨ `(step + 1) mod T`; negli stati validi correnti Ã¨ `step mod T` | `ENGINE_VERIFIED` |
| invariante | `step == day * T + hour` per ogni stato engine internamente coerente | `ENGINE_VERIFIED` |
| periodo in step | `period_steps = period_days * T`, solo per eventi realmente periodici in giorni | `DERIVED_FORMULA` |
| EOD action step | ultimo step del giorno `d`: `EOD_STEP(d) = (d + 1) * T - 1` | `DERIVED_FROM_ENGINE` |

`day * T + hour` puÃ² essere usato come ricostruzione diagnostica se un replay non espone correttamente `step`, ma non Ã¨ un clock numericamente diverso dall'engine in uno stato valido. Ãˆ un valore derivato equivalente, con diversa provenance.

### 4.2 EOD e reset

L'EOD si attiva dopo le azioni e il decay quando:

```text
(step + 1) % T == 0
```

Alla fine di quella transizione vengono aggiornati `day = (step + 1) // T` e `hour = (step + 1) % T`. I flag `watered_today`, `fed_today` e `cared_today` vengono valutati durante il refresh e poi azzerati. `fertilizer_available` non viene azzerato a EOD: per un animale sopravvissuto viene impostato a `True`. `fertilized_until_day` non ha reset giornaliero; scade per confronto col giorno.

### 4.3 Action-time vs transition-time

La convenzione corretta per l'engine Ã¨:

```text
STATE_t --ACTION_t / transition phases at engine step t--> STATE_t+1
```

Un effetto va attribuito confrontando lo stato pre-azione con quello post-interpreter. Nei file replay Kaggle osservati, la riga `i` registra tipicamente l'azione che trasforma l'osservazione della riga `i-1` nell'osservazione della riga `i`; la riga iniziale Ã¨ un placeholder. Ãˆ una convenzione di serializzazione del replay, non una diversa semantica engine.

## 5. Action-transition semantics e boundary examples

### 5.1 Ordine normativo della transizione

Per ogni step attivo:

1. per ciascun player, si valida atomicamente la domanda `PLANT` per crop rispetto ai semi correnti;
2. si applica l'azione del main farmer;
3. si applicano in ordine le azioni dei farm hands dello stesso player;
4. completati i player, si processano gli ordini market in lockstep;
5. si esegue `_town_consume`;
6. si esegue `_decay_plants`;
7. se Ã¨ EOD: refresh piante, refresh animali, RNG weed spawn, drop inventari, reset/rimozione workforce e aggiornamento town/shop;
8. si aggiornano `day` e `hour` del next state;
9. al confine terminale si assegna il reward.

Le azioni illegali o malformate sono silent no-op. Le azioni dei worker sono serializzate: un hand successivo puÃ² osservare la mutazione prodotta dal farmer o da un hand precedente nello stesso step. I player condividono board/market ma le unit action sono applicate in ordine player; gli ordini market vengono invece regolati dopo tutte le unit action.

### 5.2 Boundary example A â€” azione appena prima di EOD

Configurazione default `T=24`, stato `step=23`, `day=0`, `hour=23`. Una pianta sopravvissuta ha `consecutive_unwatered=1` e `watered_today=False`.

```text
STATE_23
  -> WATER durante action phase
  -> watered_today=True
  -> decay phase
  -> EOD plant refresh vede was_watered=True
  -> consecutive_unwatered=0; watered_today=False
  -> STATE_24: day=1, hour=0
```

La WATER all'ultimo step Ã¨ tempestiva perchÃ© precede EOD. Se invece si esegue `PLANT` allo step 23, la pianta nasce con `consecutive_unwatered=1` e `watered_today=False`: senza un'altra unitÃ  co-locata che esegua `WATER` piÃ¹ tardi nello stesso ordine seriale, il refresh porta il contatore a 2 e trasforma subito la pianta in `WEED`.

### 5.3 Boundary example B â€” primo turn del nuovo giorno

Stato `step=24`, `day=1`, `hour=0`. `WATER` imposta `watered_today=True`; il flag resta vero in tutti gli stati intermedi fino all'EOD dello step 47. Ogni ulteriore `WATER` sulla stessa pianta nello stesso giorno Ã¨ no-op. Allo step 47 il refresh consuma il flag e lo azzera nello stato 48.

Quindi il bisogno Ã¨ day-scoped, non â€œogni 24 step dalla precedente WATERâ€. Una WATER allo step 23 e una allo step 24 sono entrambe valide e appartengono a due giorni diversi.

### 5.4 Boundary example C â€” origin e primo evento biologico

Con origin day `d0=0`:

- una `STRAWBERRY` piantata nel giorno 0 deve comunque essere irrigata prima dell'EOD del giorno 0 per non morire subito; il primo incremento biologico viene eseguito all'EOD del giorno 9 ed Ã¨ visibile nello stato del giorno 10;
- una `COW` collocata nel giorno 0 ha il primo evento di produzione all'EOD del giorno 7, visibile nello stato del giorno 8;
- una `WHEAT` piantata nel giorno 0 nasce con yield 1, ma `HARVEST` resta illegale fino al giorno 2. Gli incrementi da WATER sono ammessi nelle etÃ  2, 3 e 4.

La formula degli eventi EOD usa `next_day = current_day + 1`: il giorno dichiarato nelle costanti Ã¨ il giorno del next state in cui l'output diventa osservabile.

## 6. Canonical species inventory

### 6.1 Crops

| Entity | Engine supported | Source constant |
|---|---:|---|
| `WHEAT` | YES | `CROPS` |
| `CARROT` | YES | `CROPS` |
| `TOMATO` | YES | `CROPS` |
| `STRAWBERRY` | YES | `CROPS` |
| `MELON` | YES | `CROPS` |

Non risultano altre crop in `CROPS` o in `PRODUCTS` per il fingerprint verificato.

### 6.2 Livestock

| Entity | Structure | Product | Engine supported | Source constant |
|---|---|---|---:|---|
| `GOOSE` | `COOP` | `EGG` | YES | `ANIMALS` |
| `COW` | `PASTURE` | `MILK` | YES | `ANIMALS` |
| `SHEEP` | `PASTURE` | `WOOL` | YES | `ANIMALS` |
| `CHICKEN` | N/A | N/A | NO â€” `NOT_SUPPORTED` | assente da `ANIMALS`, `PRODUCTS`, config e action legality |

`CHICKEN` non Ã¨ un alias, un nome legacy dichiarato o una runtime variant nel materiale fingerprintato. Non puÃ² essere acquistato nÃ© collocato: la classificazione canonica Ã¨ `NOT_SUPPORTED`.

## 7. Crop period ledger

### 7.1 Parametri per specie

| Crop | Seed cost | First yield day | Max yield day | Autonomous interval | Max yield | Mode | Water-yield ages | Max lifespan formula |
|---|---:|---:|---:|---:|---:|---|---|---|
| `WHEAT` | 10 | 2 | 4 | N/A (`interval=0`) | 6 | non-ongoing | 2..4 | `(d0 + 5) * T` |
| `CARROT` | 20 | 2 | 3 | N/A (`interval=0`) | 4 | non-ongoing | 2..3 | `(d0 + 4) * T` |
| `TOMATO` | 50 | 8 | 8 | 1 day | 4 | ongoing | scheduled states 8,9,10,11 | `(d0 + 12) * T`, impostato al quarto evento |
| `STRAWBERRY` | 100 | 10 | 10 | 2 days | 4 | ongoing | scheduled states 10,12,14,16 | `(d0 + 17) * T`, impostato al quarto evento |
| `MELON` | 80 | 10 | 12 | N/A (`interval=0`) | 6 | non-ongoing | 6..12 | `(d0 + 13) * T` |

`d0` Ã¨ `planted_day`; `T` Ã¨ `turnsPerDay`. Il campo `max_yield_day` delle ongoing Ã¨ metadata, ma il loro calendario effettivo Ã¨ governato da `first_yield_day`, `interval` e dal limite di quattro production counts.

### 7.2 Semantica completa comune e per-mode

| Campo richiesto | Contratto engine |
|---|---|
| terrain / structure | tile sbloccata con valore `None`; il worker deve stare sulla tile |
| plant legality | crop in `CROPS`, tile `None`, almeno un seed privato; le richieste same-player della stessa crop sono tutte bloccate se la domanda aggregata dello step supera i seed disponibili |
| origin day | `planted_day = current day` al momento dell'azione riuscita |
| stato iniziale | `watered_today=False`, `consecutive_unwatered=1`; yield 1 per non-ongoing, 0 per ongoing; fertilizer expiry `-1` |
| water requirement | una sola WATER riuscita per pianta per giorno; evita l'incremento del contatore EOD e lo porta a 0 |
| consecutive unwatered | a EOD: 0 se irrigata, altrimenti `+1`; a 2 la pianta diventa `WEED` prima di eventuale produzione ongoing |
| non-ongoing progression | la prima WATER giornaliera da `floor((max_yield_day+1)/2)`, implementato come `(max_yield_day+1)//2`, fino a `max_yield_day`, aggiunge 1, oppure 2 se fertilizzata; cap `max_yield` |
| ongoing progression | a EOD, se la pianta sopravvive e `next_day-d0-first_yield_day` Ã¨ multiplo dell'intervallo, aggiunge 1, oppure 2 se era irrigata e fertilizzata; cap `max_yield`; al massimo quattro eventi schedulati |
| harvest legality | tile `PLANT`, `yield_units>0`, `day-d0 >= first_yield_day` |
| harvest effect | trasferisce tutto lo yield nel worker inventory; una non-ongoing torna `None`, una ongoing resta con yield 0 |
| early harvest | silent no-op senza consumo o mutazione della pianta |
| harvest window | si apre quando maturitÃ  e yield sono entrambi veri; non esiste un unico giorno engine di optimum economico |
| weed / decay | oltre alla disidratazione e al random spawn sulle tile `None`, da `max_lifespan_step` lo yield della pianta viva cala di 1 ogni 2 step; a yield `<=0` diventa `WEED` |
| no-loss decay deadline | l'action phase allo step `max_lifespan_step` precede il decay dello stesso step; un HARVEST legale in quella phase salva ancora lo yield pre-decay |
| ultimate harvest close | se non intervengono acqua/RNG/DIG e lo yield all'inizio del lifespan decay Ã¨ `Y>0`, l'ultimo action step legale Ã¨ `max_lifespan_step + 2*(Y-1)` |
| fertilizer interaction | finestra day-inclusive; incremento totale 2 invece di 1; non cambia maturitÃ , calendario, cap o survival |
| daily reset | `watered_today` Ã¨ azzerato a EOD; il contatore e l'expiry fertilizer persistono |
| inventory / output | genera item con lo stesso nome della crop nel worker inventory; l'item Ã¨ sellable dopo il deposito nello shed |
| confidence | `ENGINE_VERIFIED` dal source `kaggriculture.py` righe 11â€“17, 215â€“226, 417â€“482, 752â€“803 |

`HARVEST legal from age X` non implica `HARVEST economically optimal at age Y`. Per esempio, MELON Ã¨ legalmente raccoglibile da age 10, anche se l'engine ammette incrementi WATER fino ad age 12. La scelta 10, 11 o 12 Ã¨ policy/economia.

## 8. Animal period ledger

### 8.1 Parametri per specie

| Animal | Required structure | Purchase cost | Max held | Origin | First output state day | Interval | Max productions | Base product |
|---|---|---:|---:|---|---:|---:|---|---|
| `GOOSE` | `COOP` | 300 | 4 | `placed_day=d0` | `d0+4` | 1 day | unbounded until escape/episode end | 1 `EGG` |
| `COW` | `PASTURE` | 400 | 6 | `placed_day=d0` | `d0+8` | 2 days | unbounded until escape/episode end | 1 `MILK` |
| `SHEEP` | `PASTURE` | 500 | 6 | `placed_day=d0` | `d0+6` | 3 days | unbounded until escape/episode end | 1 `WOOL` |

### 8.2 Semantica completa

| Campo richiesto | Contratto engine |
|---|---|
| placement legality | il worker sta su una struttura vuota del tipo richiesto e possiede l'animale nel proprio inventory |
| initial state | yield 0, `consecutive_unfed=0`, `fed_today=False`, `cared_today=False`, `fertilizer_available=False`, `pending_care_bonus=0` |
| FEED | una sola volta al giorno; consuma 1 WHEAT dal worker inventory; imposta `fed_today=True` |
| CARE | una sola volta al giorno; nessun costo inventory; imposta `cared_today=True` |
| EOD escape order | prima si aggiorna `consecutive_unfed`; se raggiunge 2, l'animale fugge e la struttura resta vuota; produzione, fertilizer e reset successivi non avvengono su quell'entitÃ  |
| base production | 1 unitÃ  a ogni evento schedulato se l'animale non Ã¨ fuggito, anche quando `fed_today=False` |
| prior care bonus | nel giorno di produzione viene aggiunto solo se `fed_today=True`; Ã¨ additivo, non un moltiplicatore; poi il pending viene azzerato |
| current care effect | dopo l'eventuale produzione, `cared_today AND fed_today` accumula `+1` per una futura produzione; non aumenta la produzione dello stesso EOD |
| cap | `min(max_held, current_yield + base + consumed_bonus)`; output eccedente il cap non viene accodato |
| fertilizer | ogni animale che supera il controllo fuga esce dall'EOD con `fertilizer_available=True`, indipendentemente da feed, care o giorno di produzione |
| daily reset | per un animale sopravvissuto, `fed_today` e `cared_today` tornano `False`; pending e yield persistono |
| collection | `HARVEST` Ã¨ legale con `yield_units>0`, trasferisce tutto il prodotto nel worker inventory e azzera lo yield; nessun age gate aggiuntivo |
| fertilizer collection | `COLLECT_FERTILIZER` richiede il flag True, lo porta False e aggiunge esattamente 1 `FERTILIZER` al worker inventory |
| inventory / sale | i prodotti e il fertilizzante vanno prima nel worker inventory; sono sellable dallo shed dopo deposito/drop |
| confidence | `ENGINE_VERIFIED` da `ANIMALS`, `_new_animal`, `_apply_unit_action`, `_daily_refresh_animals` |

## 9. P0 audit â€” Animal production vs FEED

### 9.1 Risposta bloccante

```text
QUESTION:
Does an animal produce base output on a production day if fed_today == FALSE,
provided it has not escaped?

ANSWER: YES
```

Nell'ordine source, il controllo fuga avviene prima della produzione. Se il nuovo `consecutive_unfed` Ã¨ 1, l'animale resta e il ramo di produzione esegue sempre `base = 1`. `fed_today` governa soltanto il consumo del `pending_care_bonus` e, insieme a CARE, il nuovo accumulo.

```text
BASE_OUTPUT: 1 on scheduled production if not escaped
FEED_BONUS: no independent numeric bonus
CARE_BONUS: accumulated only by fed+cared; consumed only on a later fed production
ESCAPE_RISK: second consecutive unfed EOD removes animal before output
PRODUCTION_ELIGIBILITY: schedule + not escaped; FEED is not a base-output gate
```

### 9.2 Transizioni minime riproducibili

Precondizioni comuni: primo evento della specie, `yield_units=0`, `consecutive_unfed=0`, `pending_care_bonus=1`, cap non saturo. Il pending iniziale a 1 rende osservabile la differenza tra base e bonus; con pending 0 tutti e quattro i casi producono base 1, salvo fuga.

| Species | EOD current day -> next state day | fed | cared | Output delta | New unfed counter | New pending | Fertilizer |
|---|---|---:|---:|---:|---:|---:|---:|
| `GOOSE` | 3 -> 4 | YES | YES | 2 = base 1 + prior bonus 1 | 0 | 1, accumulato dopo produzione | True |
| `GOOSE` | 3 -> 4 | YES | NO | 2 | 0 | 0 | True |
| `GOOSE` | 3 -> 4 | NO | YES | 1 base | 1 | 0 | True |
| `GOOSE` | 3 -> 4 | NO | NO | 1 base | 1 | 0 | True |
| `COW` | 7 -> 8 | YES | YES | 2 | 0 | 1 | True |
| `COW` | 7 -> 8 | YES | NO | 2 | 0 | 0 | True |
| `COW` | 7 -> 8 | NO | YES | 1 base | 1 | 0 | True |
| `COW` | 7 -> 8 | NO | NO | 1 base | 1 | 0 | True |
| `SHEEP` | 5 -> 6 | YES | YES | 2 | 0 | 1 | True |
| `SHEEP` | 5 -> 6 | YES | NO | 2 | 0 | 0 | True |
| `SHEEP` | 5 -> 6 | NO | YES | 1 base | 1 | 0 | True |
| `SHEEP` | 5 -> 6 | NO | NO | 1 base | 1 | 0 | True |

Caso fuga: con `consecutive_unfed=1` pre-EOD e `fed_today=False`, il nuovo contatore diventa 2 e la tile viene sostituita dalla struttura vuota. Non si produce base output, non si genera fertilizer e non resta un animale su cui applicare i reset.

```text
FOUNDATION_DISCREPANCY: YES
SEVERITY: P0
AFFECTED_SEMANTICS: livestock production eligibility, feed need, care bonus,
  period ledger, capacity demand and economics
PROPOSED_CORRECTION: gate base output on scheduled production + non-escape;
  use FEED for escape prevention, prior-bonus consumption and fed+care accumulation
```

## 10. P0 audit â€” Fertilizer

| Aspetto | Contratto verificato |
|---|---|
| origin | animale collocato e sopravvissuto al controllo fuga EOD |
| producers | `GOOSE`, `COW`, `SHEEP` |
| production condition | ogni EOD in cui l'animale non fugge; non richiede FEED, CARE o production day |
| representation | boolean `fertilizer_available`, non contatore |
| accumulation | nessuno stacking lato animale; piÃ¹ EOD senza raccolta mantengono True ma non accumulano unitÃ  |
| collection | una `COLLECT_FERTILIZER` riuscita produce esattamente 1 unitÃ  e porta il flag a False |
| crop application | `FERTILIZE` consuma 1 unitÃ  dal worker inventory su una tile `PLANT` |
| duration | `fertilized_until_day = max(existing, current_day+2)`, attivo nei giorni `d`, `d+1`, `d+2` inclusi |
| stacking | applicazioni ripetute possono estendere la data massima, ma non moltiplicano l'effetto nello stesso evento |
| non-ongoing effect | sulla prima WATER valida del giorno e nella finestra di yield, incremento totale 2 invece di 1 |
| ongoing effect | a un EOD di produzione, incremento totale 2 invece di 1 solo se la pianta era anche irrigata quel giorno |
| age interaction | non cambia age, first-yield legality o calendario; fuori dalla finestra/evento non genera yield |
| max-yield interaction | resta il cap della specie; nessun overflow di yield |
| expiry/reset | nessun reset; inattivo quando `current_day > fertilized_until_day` |

Esempio non-ongoing con origin `d0=0`: una `WHEAT` fertilizzata nel giorno 1 ha expiry 3. La WATER a age 2 e 3 aggiunge 2 per giorno; una WATER a age 4 aggiunge 1 se non c'Ã¨ stata estensione. Ogni incremento resta soggetto al cap 6. `FERTILIZE` e `WATER` sono azioni separate; servono due unit-action/step distinti o due step.

Esempio ongoing: una `STRAWBERRY` con primo evento nell'EOD 9 riceve 2 unitÃ , non 3, se Ã¨ stata WATERed nel giorno 9 e `fertilized_until_day >= 9`. Senza entrambe le condizioni riceve il base 1, se sopravvive.

La dicitura corretta Ã¨ quindi:

```text
FERTILIZED_INCREMENT_TOTAL = 2
BASE_INCREMENT_TOTAL = 1
FERTILIZER_UPLIFT = +1
```

## 11. Service-need taxonomy

| Entity/service | ENGINE_HARD_NEED | POLICY_OUTPUT_NEED | OPTIONAL_BONUS_SERVICE |
|---|---|---|---|
| crop `WATER` | necessaria entro EOD quando `consecutive_unwatered + 1 >= 2`; nessuna pianta puÃ² sopravvivere a due EOD consecutivi non irrigati | scegliere WATER nelle etÃ  di resa non-ongoing; programmare continuitÃ  e routing | WATER su ongoing production day abilita l'effetto fertilizer, ma il base output non richiede WATER se la pianta non muore |
| crop `HARVEST` | legalitÃ  engine: yield>0 e age>=first; prima del decay se si vuole evitare perdita deterministica | il giorno economicamente desiderato, batch e replant sono policy | anticipare/rinviare entro la finestra legale |
| animal `FEED` | necessario entro EOD quando il contatore preesistente Ã¨ 1 per impedire la fuga; in generale vieta due EOD unfed consecutivi | puÃ² essere pianificato ogni giorno per affidabilitÃ  | abilita consumo del pending e, con CARE, nuovo bonus; non abilita il base output |
| animal `CARE` | nessun requisito di survival o base production | puÃ² essere omesso da una policy che non compra capacitÃ  bonus | con FEED accumula `+1 pending_care_bonus` dopo l'eventuale produzione |
| animal product `HARVEST` | legalitÃ : yield>0 | raccogliere prima che `max_held` faccia perdere incrementi futuri Ã¨ una scelta output-preserving derivata | batch/routing/sale timing |
| `COLLECT_FERTILIZER` | nessuna scadenza di rimozione finchÃ© l'animale resta; il flag Ã¨ boolean | raccogliere prima di successivi EOD evita opportunity loss da mancato accumulo | frequenza e uso dipendono dalla policy |
| `FERTILIZE` | mai richiesto per legalitÃ  o survival | puÃ² aumentare output per action/crop | timing e ROI sono policy |

Un â€œbisogno giornalieroâ€ non equivale sempre a un hard deadline giornaliero. WATER e FEED tollerano un primo miss quando il contatore precedente Ã¨ 0; il secondo miss consecutivo produce la perdita engine.

## 12. Window e deadline taxonomy

| Servizio/evento | Open | Close / deadline | Reset | Classificazione |
|---|---|---|---|---|
| WATER giornaliera | dalla creazione della pianta o dall'inizio del giorno | action phase di `EOD_STEP(day)`, inclusa | EOD | `ENGINE_DEFINED` |
| WATER anti-loss | quando `watered=False` e il miss EOD porterebbe counter a 2 | stesso EOD action step | EOD | `DERIVED_FROM_ENGINE`, hard |
| WATER yield non-ongoing | etÃ  `(max_yield_day+1)//2` | etÃ  `max_yield_day`, prima WATER del giorno | flag EOD | `ENGINE_DEFINED` |
| ongoing production | EOD che porta il next state a `d0+first+k*interval` | stesso EOD, evento automatico | N/A | `ENGINE_DEFINED` |
| crop HARVEST | yield>0 e age>=first | dinamico: rimozione, WEED o terminale; no-loss deadline da lifespan | nessuno | legality `ENGINE_DEFINED`; target day `POLICY_DECLARED` |
| FEED | dopo placement o inizio giorno | action phase dell'EOD corrente | flag EOD | `ENGINE_DEFINED` |
| CARE | dopo placement o inizio giorno | action phase dell'EOD corrente per accumulare il bonus di quel giorno | flag EOD | `ENGINE_DEFINED` |
| animal product collection | appena yield>0 | nessuna close temporale fissa; escape/cap/terminale sono vincoli | yield azzerato da HARVEST | legality `ENGINE_DEFINED`; collection target `POLICY_DECLARED` |
| fertilizer collection | next state dopo un EOD sopravvissuto, o finchÃ© il flag resta True | raccolta o escape; nessuna expiry autonoma | COLLECT porta False, EOD riporta True | `ENGINE_DEFINED` |
| fertilizer effect | applicazione nel giorno d | fine giorno d+2 incluso | nessun reset, solo expiry | `ENGINE_DEFINED` |
| reserved service window | planner-defined range dentro i confini sopra | planner-defined | planner | `POLICY_DECLARED` |

`SERVICE_WINDOW` come oggetto con `[open,target,close]` non Ã¨ una primitive del runtime. I suoi confini legali possono essere derivati dall'engine; target, slack e prenotazioni sono policy.

## 13. Capacity-relevant engine constraints

La capacity Ã¨ multidimensionale; un conteggio scalare di slot non Ã¨ una garanzia sufficiente.

| Dimensione | Vincolo engine |
|---|---|
| action slots | ogni farmer/hand riceve al massimo una unit action per step |
| workforce lifecycle | il farmer Ã¨ permanente; gli hands sono assunti nel market phase, quindi non agiscono nello step dell'assunzione; tutti gli hands vengono rimossi a EOD |
| hire cost | costo Fibonacci rispetto a `hires_today`, moltiplicato dal parametro di config; reset EOD |
| movement | una casella ortogonale per MOVE, bounds enforced; si puÃ² camminare su `LOCKED`, ma le tile action lÃ¬ sono no-op |
| occupancy | multi-occupancy dei worker consentita; nessun collision stall nativo |
| ordering | farmer poi hands per player; mutazioni serializzate; market dopo tutte le unit action |
| spatial legality | PLANT/WATER/HARVEST/FERTILIZE/DIG/BUILD/FEED/CARE/COLLECT richiedono il worker sulla tile; shed ops richiedono adiacenza ortogonale |
| structures | animale solo nella struttura corrispondente e vuota; DIG non rimuove un animale collocato |
| seeds | storage privato separato; PLANT same-crop atomicamente bloccate tutte se domanda aggregata > disponibilitÃ  |
| feed/fertilizer | devono essere nel worker inventory al momento della unit action; la sola presenza nello shed non basta |
| market timing | acquisti e HIRE sono processati dopo le unit action: quanto comprato non puÃ² essere usato da un worker nello stesso step |
| market batch | massimo configurabile di ordini per turn, default 10; gli ordini eccedenti non vengono processati |
| shed | cap aggregato configurabile, default 100; acquisti product/animal falliscono a cap pieno |
| inventory drop | EOD deposita automaticamente fino al cap e scarta overflow; `DROP` manuale scarta anch'esso l'eccedenza perchÃ© svuota l'intero inventory; `PLACE` verso shed deposita solo quanto entra e lascia il resto al worker |
| daily flags | una seconda WATER/FEED/CARE sulla stessa entitÃ  nel giorno Ã¨ no-op e consuma comunque lo slot dell'unitÃ  che l'ha richiesta |
| biological phase | un'azione valida appena prima EOD puÃ² cambiare la transizione EOD; l'azione appena dopo EOD appartiene al giorno successivo |
| uncertainty | random WEED su tile `None` a EOD e dinamiche di mercato impediscono di ridurre la capacitÃ  futura a una sola uguaglianza deterministica |

Le dimensioni minime della futura capacity sono: tempo/phase, unitÃ , posizione e distanza, precedenze, inventory compartment, species legality, structure, market slots, cash, storage, serialized ordering, deadline e incertezza. `required_slots <= available_slots` Ã¨ necessario in alcune astrazioni, ma non sufficiente.

## 14. Three-way serviceability analysis

| Livello | Source | Observability | Status | Dependencies |
|---|---|---|---|---|
| `ACTION_ELIGIBLE_NOW` | guardie di `_apply_unit_action` + stato pre-action | online e deterministico nello snapshot corrente, se tutte le componenti private rilevanti sono disponibili | `DETERMINISTIC` | posizione, tile, day, daily flags, inventory worker, seeds, structure, shed adjacency/cap, action shape |
| `RESERVED_SERVICEABLE_BEFORE_DEADLINE` | nessun campo engine; derivazione del planner su regole e forecast engine | online come previsione della policy, non come fatto realizzato | `PARTIALLY_KNOWN / POLICY_CONTEXT` | route, assegnazione worker, future hires, precedenze, risorse, contesa, market, slack, deviazioni e RNG |
| `REALIZED_SERVICEABLE_IN_WINDOW` | differenza pre/post state piÃ¹ azione ed esatta phase attribution | solo post-action/post-window | `POST_HOC` | log richiesta, stato pre, stato post, eventi EOD/decay/RNG, identitÃ  entitÃ  e window dichiarata |

La prenotazione puÃ² essere deterministica rispetto al piano scelto, ma non diventa una garanzia engine. La realizzazione non puÃ² essere usata come input pre-action dell'evento che sta misurando.

## 15. Current Foundation discrepancy matrix

| ID / Severity | Current Foundation claim | Engine evidence | Why it matters | Layer | Recommended change |
|---|---|---|---|---|---|
| `CLK-01` `P0_ENGINE_CONTRADICTION` | State Machine 2.1: `engine_step != canonical_step by definition` | `day=step//T`; next `day=(step+1)//T`, `hour=(step+1)%T`; negli stati validi `step=day*T+hour` | altera periodi, replay alignment e deadline | State Machine, Feature Model | distinguere provenance/uso dei due valori, ma congelarne l'uguaglianza numerica in stato valido |
| `ANI-01` `P0_ENGINE_CONTRADICTION` | State Machine 9.2/transition table: se non fed la produzione non avviene; product yield richiede fed | `_daily_refresh_animals`: dopo il non-escape esegue sempre `base=1`; FEED controlla solo bonus | cambia produzione, feed demand, capacity ed economia | State Machine, Ontology, Feature Model | riscrivere eligibility come schedule + non-escape; separare base, bonus, survival |
| `ANI-02` `P1_SEMANTIC_AMBIGUITY` | bonus descritto come â€œmoltiplicatoreâ€ | source aggiunge l'intero `pending_care_bonus`; Ã¨ additivo e cap-limited | formule quantitative e cap possono divergere | State Machine, Feature Model | usare `base + pending`, specificare consumo/reset e ordine con CARE corrente |
| `FER-01` `P0_ENGINE_CONTRADICTION` | State Machine 8.2: â€œ+2 unitÃ  addizionaliâ€ | non-ongoing e ongoing aggiungono 2 invece di 1 | puÃ² modellare 3 invece di 2 per evento | State Machine, Ontology, Feature Model | dichiarare total 2, uplift +1, cap invariato |
| `FER-02` `P2_MISSING_DOMAIN_FACT` | fertilizer flow genericamente â€œgenerato automaticamenteâ€ | il producer Ã¨ un boolean: un'unitÃ  raccoglibile, non accumulabile; fuga precede generazione | determina opportunity loss e collection cadence | Ontology, State Machine | aggiungere boolean saturation, collection transition e ordering fuga/generazione |
| `INV-01` `P0_ENGINE_CONTRADICTION` | Ontology `shed_overflow_eod_loss`: overflow â€œesclusivamenteâ€ durante EOD | `_apply_unit_action` `DROP` deposita fino a room e poi elimina tutto l'inventory, scartando overflow; EOD fa lo stesso | una perdita reale sarebbe invisibile fuori EOD | Ontology, State Machine, Feature Model | generalizzare a shed overflow loss con cause `MANUAL_DROP` e `EOD_AUTO_DROP`; distinguere `PLACE` che conserva il resto |
| `INV-02` `P3_NAMING_OR_MODELING_ISSUE` | Feature Model `INV-03` mappa ancora a `contract_inventory_loss` | Ontology ha rinominato in `shed_overflow_eod_loss`; inoltre il nome EOD Ã¨ troppo stretto | mapping verticale incoerente | Feature Model, Ontology | adottare un solo nome corretto dopo la revisione semantica INV-01 |
| `SVC-01` `P1_SEMANTIC_AMBIGUITY` | State Machine definisce serviceability come â€œcertezzaâ€, poi la marca `PARTIALLY_KNOWN` | l'engine espone guardie correnti, non una garanzia futura di routing/esecuzione | confonde forecast e fatto | State Machine, Ontology, Feature Model | separare i tre livelli della sezione 14 |
| `CAP-01` `P1_SEMANTIC_AMBIGUITY` | Ontology: capacity giornaliera = step per worker * headcount, `ENGINE_VERIFIED` | headcount varia intra-day; hire avviene dopo action phase; hands spariscono EOD; route/inventory/precedenze limitano gli slot | sovrastima fattibilitÃ  e induce falsa garanzia scalare | Ontology, Feature Model | retrocedere a upper bound derivato con intervallo attivo per unitÃ ; non usarlo come serviceability |
| `OBS-01` `P1_SEMANTIC_AMBIGUITY` | Ontology `crop_harvest_action_flow` Ã¨ `ONLINE_OBSERVABLE` come azioni eseguite | una request Ã¨ nota online, ma successo/no-op richiede post-state o instrumentation; Feature Model GLB-02 lo riconosce correttamente | rischio future leakage e denominatori errati | Ontology, Feature Model | separare requested flow da realized flow e completion evidence |
| `HAR-01` `P1_SEMANTIC_AMBIGUITY` | State Machine: early HARVEST â€œrischia di distruggere l'investimento temporaleâ€ | il ramo ritorna senza mutare pianta o inventory | puÃ² essere letto come perdita engine immediata | State Machine | specificare silent no-op; l'unico danno diretto Ã¨ lo slot sprecato, piÃ¹ eventuale opportunity cost |
| `SPC-01` `P2_MISSING_DOMAIN_FACT` | nessun inventario Foundation chiuso che dichiari esplicitamente CHICKEN unsupported | `ANIMALS` contiene soltanto GOOSE/COW/SHEEP | evita alias/specie inventate nei layer successivi | Ontology, State Machine | congelare inventory e fingerprint; dichiarare `CHICKEN=NOT_SUPPORTED` |
| `PER-01` `P2_MISSING_DOMAIN_FACT` | mancano ledger versionato, formule origin-relative e cap/max-production completi | costanti e refresh source forniscono formule esatte | impedisce periodi portabili con T configurabile | tutti i layer Foundation | adottare, dopo review, un ledger source-grounded versionato |

Nessuna correzione Ã¨ stata applicata in questo audit.

## 16. Canonical period ledger v1

Simboli: `T=turnsPerDay`, `d0=origin_day`, `a=day-d0`, `EOD(d)=(d+1)T-1`. `event day` Ã¨ il giorno del next state in cui l'output diventa visibile. Hash abbreviato in tabella: `bc8a5487â€¦` = SHA-256 completo della sezione 2.

| ENTITY | ENTITY_TYPE | BIOLOGICAL_EVENT | PERIOD_DAYS | PERIOD_FORMULA | FIRST_EVENT_DAY | WINDOW_OPEN | WINDOW_CLOSE | HARD_DEADLINE | DAILY_RESET_DEPENDENCY | ONGOING | MAX_PRODUCTIONS | ENGINE_SOURCE | ENGINE_HASH | STATUS |
|---|---|---|---:|---|---|---|---|---|---|---:|---|---|---|---|
| WHEAT | crop | WATER-driven yield increment | 1 in age window | one successful WATER/day, ages 2..4 | `d0+2` | age 2 | age 4 | each relevant EOD; survival hard on second miss | watered flag | NO | N/A; cap 6 | `CROPS`, WATER | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| WHEAT | crop | harvest eligibility/lifespan | non-periodic | age>=2 and yield>0; MLS=`(d0+5)T` | `d0+2` | age 2 | dynamic until WEED | no-loss action phase at MLS | water survival | NO | one terminal harvest | HARVEST, decay | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| CARROT | crop | WATER-driven yield increment | 1 in age window | one successful WATER/day, ages 2..3 | `d0+2` | age 2 | age 3 | each relevant EOD; survival hard on second miss | watered flag | NO | N/A; cap 4 | `CROPS`, WATER | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| CARROT | crop | harvest eligibility/lifespan | non-periodic | age>=2 and yield>0; MLS=`(d0+4)T` | `d0+2` | age 2 | dynamic until WEED | no-loss action phase at MLS | water survival | NO | one terminal harvest | HARVEST, decay | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| MELON | crop | WATER-driven yield increment | 1 in age window | one successful WATER/day, ages 6..12 | `d0+6` | age 6 | age 12 | each relevant EOD; survival hard on second miss | watered flag | NO | N/A; cap 6 | `CROPS`, WATER | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| MELON | crop | harvest eligibility/lifespan | non-periodic | age>=10 and yield>0; MLS=`(d0+13)T` | `d0+10` | age 10 | dynamic until WEED | no-loss action phase at MLS | water survival | NO | one terminal harvest | HARVEST, decay | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| TOMATO | crop | scheduled yield increment | 1 | `event_day=d0+8+k`, `k=0..3` | `d0+8` | post-EOD state at event | fourth event `d0+11` | survival by each prior EOD; MLS=`(d0+12)T` | watered for survival; watered+fertilizer for doubled increment | YES | 4 scheduled events; yield cap 4 | plant refresh | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| TOMATO | crop | harvest | opportunity after yield | yield>0 and age>=8 | `d0+8` | first positive yield | dynamic until WEED/terminal | no-loss action phase at MLS | none beyond plant survival | YES | repeatable while plant alive | HARVEST, decay | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| STRAWBERRY | crop | scheduled yield increment | 2 | `event_day=d0+10+2k`, `k=0..3` | `d0+10` | post-EOD state at event | fourth event `d0+16` | survival by each prior EOD; MLS=`(d0+17)T` | watered for survival; watered+fertilizer for doubled increment | YES | 4 scheduled events; yield cap 4 | plant refresh | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| STRAWBERRY | crop | harvest | opportunity after yield | yield>0 and age>=10 | `d0+10` | first positive yield | dynamic until WEED/terminal | no-loss action phase at MLS | none beyond plant survival | YES | repeatable while plant alive | HARVEST, decay | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| GOOSE | animal | product increment | 1 | `event_day=d0+4+k` | `d0+4` | post-EOD yield>0 | none fixed; cap/escape/terminal | second unfed EOD causes escape before event | FEED/CARE flags | YES | unbounded; held cap 4 | animal refresh | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| COW | animal | product increment | 2 | `event_day=d0+8+2k` | `d0+8` | post-EOD yield>0 | none fixed; cap/escape/terminal | second unfed EOD causes escape before event | FEED/CARE flags | YES | unbounded; held cap 6 | animal refresh | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| SHEEP | animal | product increment | 3 | `event_day=d0+6+3k` | `d0+6` | post-EOD yield>0 | none fixed; cap/escape/terminal | second unfed EOD causes escape before event | FEED/CARE flags | YES | unbounded; held cap 6 | animal refresh | `bc8a5487â€¦` | `ENGINE_VERIFIED` |
| ALL ANIMALS | service/byproduct | FEED/CARE reset + fertilizer availability | 1 | each EOD survived | first survived EOD | within current day / next state for fertilizer | EOD for flags; collection/escape for fertilizer | feed hard only on second miss | FEED, CARE | YES | unbounded | animal refresh | `bc8a5487â€¦` | `ENGINE_VERIFIED` |

Le costanti 24/48/72 sono soltanto le istanze default di `1T/2T/3T`. Il ciclo WHEAT di 96 step osservato in alcune policy non Ã¨ un periodo biologico autonomo: deriva da una scelta di harvest/replant intorno a quattro giorni.

## 17. Replay reconciliation

Fonti empiriche, non normative: `docs/benchmark/103484828.json`, `103473619.json`, `103462357.json`, `103464592.json`. Gli eventi sono stati attribuiti tramite delta coerenti di tile/inventory tra snapshot consecutivi; le richieste senza effetto non sono state trattate come completion.

| Replay / player | Pattern osservato | Reconciliation class | Spiegazione engine-grounded |
|---|---|---|---|
| 103484828 / LuCcc | WATER mediana 24 | `ENGINE_COMPATIBLE_POLICY_PATTERN` | coincide con un giorno default, ma l'engine definisce flag/day boundary, non una cadence obbligatoria dalla WATER precedente |
| LuCcc | STRAWBERRY harvest ~47.5 step, ages 10/12/14/16 | `ENGINE_COMPATIBLE_POLICY_PATTERN` | segue il periodo di produzione `2T`; la scelta di raccogliere ogni evento Ã¨ policy |
| LuCcc | COW collection 48, SHEEP 72 | `ENGINE_COMPATIBLE_POLICY_PATTERN` | coincide con `2T`/`3T`; collection timing resta policy e puÃ² accumulare fino al cap |
| LuCcc | WHEAT harvest age 4 e ciclo per tile ~96 | `POLICY_SPECIFIC` | age 4 Ã¨ legale ed entro il yield window, ma l'engine consente harvest da age 2 e non impone replant a 4 giorni |
| LuCcc | MELON harvest age 12, yield 6 | `POLICY_SPECIFIC` | age 12 Ã¨ la fine del yield window, non il primo giorno legale (10) |
| 103473619 / Gordeev | COW 48, SHEEP ~71.5, STRAWBERRY ~47 | `ENGINE_COMPATIBLE_POLICY_PATTERN` | jitter di execution/route intorno ai periodi `2T`/`3T` |
| Gordeev | WHEAT harvest age 2..4, yield 2..6 | `ENGINE_CONFIRMED` per legalitÃ ; `POLICY_SPECIFIC` per mix di etÃ  | tutto ricade nel contratto; nessun singolo optimum Ã¨ engine-defined |
| Gordeev | WATER per tile mediana >24 | `POLICY_SPECIFIC` | il primo miss puÃ² essere tollerato; aggregare cadence non equivale a un nuovo periodo engine |
| 103462357 / Dipin | COW 48, SHEEP ~72.5, STRAWBERRY ~47 | `ENGINE_COMPATIBLE_POLICY_PATTERN` | calendario osservato compatibile con `2T`/`3T` |
| Dipin | WHEAT prevalentemente age 3; MELON prevalentemente age 10 | `POLICY_SPECIFIC` | entrambe scelte legali, differenti dalla massimizzazione tardiva |
| 103464592 / Petar | SHEEP collection ~71; CARE ~24, FEED ~25 | `ENGINE_COMPATIBLE_POLICY_PATTERN` | output `3T`, service day-scoped con jitter; nessun nuovo periodo |
| Petar | WHEAT 65/66 harvest age 2 | `POLICY_SPECIFIC` | age 2 Ã¨ il primo giorno legale, non una regola universale di harvest |
| Petar | molte HARVEST request senza effetto | `ENGINE_CONFIRMED` come possibilitÃ  di silent no-op, non come periodo | mostra perchÃ© request e realized completion devono restare separati |
| tutti | apparente offset di una riga tra azione e delta | `REPLAY_MEASUREMENT_ARTIFACT` | la riga replay post-transition porta l'azione rispetto allo snapshot precedente; non cambia il clock engine |
| tutti | nessun `CHICKEN` | nessuna promozione probatoria | l'assenza empirica non fonda il fatto; `NOT_SUPPORTED` deriva dal source |

Non restano periodicitÃ  biologiche `UNEXPLAINED` rilevanti nei quattro replay dopo la distinzione tra periodo engine, legal window e policy di collection/harvest.

## 18. Provenance e no-future-leakage

| Classe | Esempi leciti | Momento | Uso consentito |
|---|---|---|---|
| `PRE_ACTION_ENGINE_STATE` | step/day/hour, tile, flags, yield, worker position, private inventory, seeds, shed | prima dell'azione | input online |
| `DERIVED_PRE_ACTION_FEATURE` | age, harvest legality, EOD step, anti-loss predicate, current action eligibility | derivata solo dallo stato corrente | input online con formula/versione |
| `POLICY_CONTEXT` | reservation, route plan, target harvest day, forecast di capacity | prima dell'azione ma prodotto dal controller | input policy, mai dichiarato fatto engine |
| `POST_ACTION_TRANSITION_EVIDENCE` | azione riuscita/no-op, delta yield/inventory, escape, decay, overflow | dopo la transizione | telemetry/label per il passato |
| `POST_WINDOW_METRIC` | realized serviceability, completion rate, forecast error, period adherence | dopo la chiusura della window | valutazione/apprendimento futuro, non input retroattivo |

Findings:

1. `completion_evidence` non Ã¨ disponibile al decision time dell'azione che deve confermare.
2. `forecast_error` richiede forecast antecedente e outcome successivo; usare l'errore della stessa finestra prima della close Ã¨ leakage.
3. `realized_serviceability` Ã¨ post hoc; la versione pre-action deve chiamarsi reserved/forecast serviceability e conservare uncertainty.
4. Il Feature Model corrente classifica correttamente `action_execution_result` e `transition_reason` come telemetry-only; l'Ontology contraddice parzialmente questa disciplina marcando il flow delle azioni HARVEST â€œeseguiteâ€ come online observable.
5. Il reward/final money non puÃ² entrare nelle feature pre-terminali dello stesso episodio.
6. Nel replay, associare `action[i]` a `observation[i] -> observation[i+1]` invece che alla transizione precedente crea leakage/offset e falsi periodi.
7. Una reservation non prova completion; una request non prova execution; yield disponibile non prova che una HARVEST richiesta sia riuscita senza il predicato di maturitÃ  e il delta.

Ogni futuro artefatto deve registrare almeno `source_class`, `observation_phase`, `formula_version` e `engine_fingerprint` per le feature temporali o biologiche.

## 19. Required corrections before Ontology revision

Prima di riscrivere l'Ontology, il working set della revisione deve incorporare esplicitamente, senza modificare ancora i MODEL_SPEC:

1. correggere il clock: distinzione di provenance, uguaglianza numerica in stato valido;
2. correggere il P0 animale: schedule + non-escape producono base; FEED non Ã¨ base-output gate;
3. modellare `pending_care_bonus` come additivo, consumato su produzione fed e accumulato dopo la produzione corrente;
4. correggere il P0 fertilizer: incremento totale 2, uplift +1, cap invariato;
5. correggere il P0 inventory: overflow loss sia da manual `DROP` sia da EOD auto-drop; `PLACE` non scarta il resto;
6. congelare species inventory con `GOOSE` e `CHICKEN=NOT_SUPPORTED` per questo fingerprint;
7. incorporare boolean saturation e ordering di `fertilizer_available`;
8. adottare il ledger origin-relative e parametrico in `T`, senza hardcode universali 24/48/72/96;
9. separare `ACTION_ELIGIBLE_NOW`, forecast/reserved serviceability e realized serviceability;
10. separare action request, action execution e completion evidence;
11. sostituire la capacity scalare giornaliera con un upper bound esplicitamente incompleto e dimensioni di legalitÃ /route/inventory/phase;
12. risolvere il mapping stale `contract_inventory_loss` e scegliere un nome coerente con entrambe le cause reali di overflow;
13. ancorare ogni fatto congelato al fingerprint della sezione 2.

I P0 non sono `UNRESOLVED`: il source li risolve in modo deterministico. Tuttavia la Foundation corrente resta semanticamente non congelabile finchÃ© le correzioni non vengono applicate e sottoposte a vertical review.

## 20. Final authorization verdict

Il contratto Ã¨ tecnicamente sufficiente per iniziare la revisione dell'Ontology dopo la revisione indipendente prevista. `ONTOLOGY_REVISION_SAFE_TO_START: YES` significa che non resta un blocker semantico engine irrisolto; non salta il gate procedurale Antigravity + Copilot e non autorizza nessuna fase downstream.

```text
NEXT_PHASE_IF_PASS:
INDEPENDENT REVIEW OF ENGINE CONTRACT BY ANTIGRAVITY + COPILOT
```

```text
ENGINE_CONTRACT_AUDIT_COMPLETE: YES
ENGINE_IDENTITY_FROZEN: YES
CLOCK_CONTRACT_VERIFIED: YES
SPECIES_INVENTORY_VERIFIED: YES
GOOSE_CHICKEN_RESOLVED: YES
ANIMAL_FEED_PRODUCTION_SEMANTICS_RESOLVED: YES
FERTILIZER_SEMANTICS_RESOLVED: YES
PERIOD_LEDGER_READY_FOR_REVIEW: YES
FOUNDATION_DISCREPANCIES_IDENTIFIED: YES
ONTOLOGY_REVISION_SAFE_TO_START: YES
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
