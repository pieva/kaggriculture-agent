# MODEL_SPEC — Claude E17.1 3Q Reactive Independent V2

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-02
- **Foundation:** C2.1 (RECONCILED)
- **Stato:** AS-BUILT (development, remediation della V1)
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V1`,
  `REJECTED BEFORE TOURNAMENT`
  (`experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V1_FAILED_GATE_REPORT.md`)
- **Autorizzazione:** `experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_V2_REMEDIATION_PROMPT.md`,
  `experiments/e17/reviews/common/E17_REACTIVE_TOURNAMENT_CANDIDATE_AMENDMENT_1.md`
- **Sorgente:** `src/agricola/strategy/claude/e17_reactive_3q_v2.py`
- **Config:** `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V2.json`

---

## 1. Diagnosi verificata sulla V1 (non assunta)

Prima di progettare la V2 sono state misurate direttamente, sui ledger e sui
run reali della V1 conservati sotto `experiments/e17/artifacts/runs/claude/e17_1/`,
le sei ipotesi elencate dal prompt di remediation. Metodo e risultato per
ciascuna:

| Ipotesi | Metodo di verifica | Esito |
|---|---|---|
| Oscillazione da dispatcher stateless | Conteggio inversioni immediate di direzione del farmer (`A` poi `opposite(A)`) sul run `S26090101-P0` | **CONFERMATA (parziale):** `46/557` mosse farmer (`8,3%`) sono inversioni immediate; il dispatcher stateless non ha memoria di un target in corso, quindi una tile marginalmente più vicina ma di priorità pari o inferiore può interrompere un tragitto già iniziato |
| Target non persistenti e percorsi lunghi | Stesso run: `3.369` comandi `MOVE` su `4.355` record totali (`77,4%`) | **CONFERMATA:** la quota di movimento puro è dominante; assenza di persistenza del target è la causa architetturale primaria |
| `HIRE` ripetuti senza cash o senza necessità | Ricostruzione stato-per-stato di `farm.hires_today` osservato contro il conteggio di ordini `HIRE` richiesti per ogni giorno, sull'intero episodio `S26090101-P0` | **FALSIFICATA:** `156` ordini `HIRE` richiesti nell'episodio, **zero** giorni in cui le richieste hanno superato gli hire effettivamente accreditati (`hires_today` osservato). Il numero elevato riflette il fatto d'ambiente `ENGINE_VERIFIED` per cui gli Hands scadono ogni EOD e vanno riassunti da zero ogni giorno, non un difetto del controller |
| Espansione Q1/Q2 prematura rispetto al motore Q0 | Lettura diretta del ledger: giorno del primo `BUY_LAND`, giorno del primo `PLANT` eseguito, giorno del primo `HARVEST` eseguito, conteggio harvest prima del primo `BUY_LAND` | **CONFERMATA in modo netto:** primo `BUY_LAND` al **giorno 0**, con **zero** `HARVEST` eseguiti prima di quell'ordine (il primo harvest reale avviene al giorno 2). La guardia di espansione V1 (`service_pressure <= soglia`) è calcolata come `care_due / max(1, plant_tiles)`: con zero piante possedute vale `0/1 = 0`, cioè supera banalmente la soglia. La guardia non distingue "nessuna pressione perché il nucleo è maturo" da "nessuna pressione perché il nucleo non esiste ancora" |
| Densità/resa insufficiente per tile | Non isolabile come fattore indipendente prima di correggere l'espansione prematura (fattori confusi) | **NON CONCLUSIVA in questa iterazione**; rivalutabile dopo il fix di espansione |
| Guardie feed incapaci di garantire zero fughe | Conteggio fughe derivate per run (`8` totali su `14`, mai più di `2` per run) più ispezione della coda di priorità V1 (`FEED_NEEDED` a priorità 2, ma un solo worker spesso disponibile) | **CONFERMATA come effetto di capacità, non di logica della guardia:** la guardia `FEED_NEEDED` è correttamente ad alta priorità; il problema è che il numero di worker disponibili in un dato momento è insufficiente a coprire il carico simultaneo generato dall'espansione prematura |

Conseguenza diretta per il design: la causa dominante confermata con
evidenza più forte è **l'espansione territoriale prima che il nucleo Q0
produca**, che poi genera sia il sovraccarico di movimento sia le fughe per
diluizione della capacità di servizio. La V2 tratta questa come causa
primaria e la oscillazione di target come causa secondaria concorrente. La
V2 non implementa alcuna correzione per l'ipotesi `HIRE`, perché la verifica
diretta l'ha falsificata: aggiungere una guardia per un problema non
confermato avrebbe violato il principio di correggere solo le cause
confermate.

---

## 2. Ipotesi strategiche V2

1. **H-CR2.1 (nucleo prima dell'espansione):** un secondo guardiano di
   espansione, ortogonale alla cassa e all'orizzonte, che richieda una prova
   agent-local di produzione reale del nucleo (non solo assenza di
   pressione), elimina l'espansione a costo-zero-di-evidenza osservata in
   V1 e permette a Q0 di generare margine prima che il worker pool venga
   diviso su più territorio.
2. **H-CR2.2 (target persistenti con invalidazione):** assegnare ad ogni
   worker un compito che sopravvive tra le chiamate finché resta valido, con
   un solo livello di interruzione opportunistica (l'azione più urgente
   sulla tile attualmente occupata) riduce la quota di comandi `MOVE` senza
   perdere reattività, perché l'invalidazione avviene comunque ad ogni
   chiamata sulla base dello stato osservato corrente.
3. **H-CR2.3 (workforce guidata dal carico osservato):** dimensionare il
   target di headcount sul numero di esigenze di servizio effettivamente in
   coda (non su un moltiplicatore fisso per quadrante) fa crescere la
   workforce quando serve davvero e ne evita l'eccesso quando il territorio
   posseduto è ancora piccolo.
4. **H-CR2.4 (ratchet zootecnico a rischio zero):** vietare l'acquisto di un
   nuovo animale finché un capo già posseduto è a rischio di fuga imminente
   (`consecutive_unfed == 1` e non ancora nutrito oggi, il predicato
   `LIV-08`) impedisce strutturalmente che la crescita del gregge superi la
   capacità di servizio dimostrata, senza bisogno di stimare quella
   capacità in anticipo.

---

## 3. Provenance e indipendenza strategica

Identica alla V1 (Sezione 2 del MODEL_SPEC V1): nessun import da
`agricola.strategy.codex`, `agricola.strategy.antigravity` o
`agricola.strategy.copilot`; nessuna tabella di azioni indicizzata per step;
le uniche dipendenze condivise sono `agricola.core.observation_contract` e
le formule pubbliche `ENGINE_VERIFIED`/`DERIVED_ENGINE_FACT` della Foundation
C2.1 (identiche a quelle già documentate e verificate nella V1: classifier
di tile lifecycle, `crop_harvest_readiness`, finestra fertilizzante,
Fibonacci `HIRE`, geometria quadranti/shed). La V2 riusa la propria
evidenza V1 (ledger, summary, diagnosi) come previsto dall'autorizzazione;
non deriva alcuna decisione dalla routine Codex né dal target economico in
sé (il numero 50k non giustifica l'importazione di logica altrui).

---

## 4. Stato interno agent-local (differenza principale rispetto alla V1)

La V1 era quasi interamente stateless per costruzione. La V2 introduce
**stato agent-local persistente esplicitamente autorizzato dal prompt di
remediation** ("ruolo/target/coda breve... deriva da osservazioni correnti,
si invalida quando il target cambia"), mantenuto sull'istanza
`ClaudeE17ReactiveAgentV2`:

| Campo | Ruolo | Invalidazione |
|---|---|---|
| `_assignments: dict[worker_key, _Assignment]` | target/compito corrente per worker (`farmer`, `hand:0`, ...) | ricalcolata ad ogni chiamata contro lo stato osservato corrente (Sezione 6.2); azzerata per gli `hand:*` ad ogni cambio di giorno (`clock.day`), perché gli Hands sono entità fisicamente diverse ogni giorno (fatto d'ambiente `ENGINE_VERIFIED`) |
| `_core_harvest_requests: int` | contatore monotono delle proprie richieste `HARVEST` dispacciate, usato solo come guardia di maturità Q0 (Sezione 6.4) | mai azzerato entro un episodio (nuova istanza per episodio, coerente con `create_claude_e17_agent_v2` per-episodio) |
| `technical_errors`, `_telemetry` | identici alla V1, solo diagnostica passiva | non riletti dal planner |

Nessun campo qui rappresenta una tabella indicizzata per step: `_assignments`
è una mappa worker→compito di cardinalità limitata (numero di worker attivi,
al più `workforce.max_hands + 1`), rivalidata ogni chiamata contro
l'osservazione corrente, non una sequenza precompilata di azioni.
`_core_harvest_requests` è un contatore scalare delle proprie richieste
passate, non un piano futuro.

---

## 5. Feature C2.1 effettivamente consumate

Stesso insieme della V1 (MODEL_SPEC V1 Sezione 4), con un'aggiunta esplicita:
`LIV-07`/`LIV-08` (`consecutive_unfed`, allerta fuga EOD) sono ora usate
anche come guardia di acquisto zootecnico (Sezione 6.5), non solo come
priorità di dispatch.

---

## 6. Architettura V2

### 6.1 Pipeline

Identica nella forma alla V1 (parsing → feature → planner → dispatch →
market → telemetria), con due inserimenti:

```text
1. SNAPSHOT
2. FEATURES           (+ at_risk_animal_count da LIV-08, core_established)
3. GOAL PLANNER        (coda di opportunità, invariata nella forma)
4. DISPATCH            (+ risoluzione/validazione di _assignments persistenti
                         prima della ricerca ex-novo; stall-timeout)
5. MARKET BUILDER       (+ guardia core_established su BUY_LAND;
                         + ratchet LIV-08 su BUY_ANIMAL;
                         + target_headcount guidato dal carico)
6. TELEMETRY
```

### 6.2 Dispatch con target persistenti

Per ogni worker, in ordine farmer-poi-hands (identico alla V1):

1. Se esiste un'assegnazione (`_assignments[worker_key]`) **e** la sua
   condizione di validità è ancora vera sullo stato osservato corrente
   (stessa logica di guardia usata per generare l'opportunità originale:
   es. per `URGENT_WATER` la tile deve essere ancora `PLANT` con
   `watered_today == False`) **e** la tile non è nel frattempo stata
   assegnata a un altro worker in questa stessa chiamata, l'assegnazione
   resta e viene risolta nel comando corrente (azione se il worker è già
   sulla tile, movimento verso di essa altrimenti).
2. Altrimenti l'assegnazione viene scartata e il worker partecipa alla
   ricerca greedy della migliore opportunità libera (stessa cascata di
   priorità della V1, Sezione 6.3), esclusi i target già impegnati da altre
   assegnazioni correnti (persistenti, non solo quelle di questa chiamata).
3. **Interruzione opportunistica a costo zero:** indipendentemente dal
   punto 1/2, se il worker si trova già su una tile che richiede
   `URGENT_WATER` o `FERTILIZE` (fertilizzante già in mano), esegue
   quell'azione immediata senza abbandonare l'assegnazione corrente per il
   turno successivo (identico nello spirito all'`_opportunistic_fertilize`
   della V1, esteso a `WATER` sulla tile occupata).
4. **Timeout di stallo:** se il comando risolto per un'assegnazione è
   `PASS` per `dispatch.assignment_stall_timeout` chiamate consecutive
   (es. `FEED_NEEDED` in attesa di WHEAT che non arriva in shed), la si
   scarta e il worker rientra nella ricerca libera al turno successivo,
   evitando un blocco permanente su un compito momentaneamente non
   servibile.
5. **Prelazione d'urgenza (trovata e corretta durante lo sviluppo V2,
   Sezione 9.1):** la sola persistenza (punti 1-2) non basta a evitare
   perdite: se un worker è già impegnato su un compito a bassa priorità
   (es. `PLANT_OPPORTUNITY`) e nel frattempo compare un'esigenza a rischio
   di perdita EOD (`URGENT_WATER` o `FEED_NEEDED`, priorità ≤ 2) rimasta
   scoperta perché ogni altro worker è a sua volta impegnato, la stickiness
   da sola lascerebbe quell'esigenza scoperta fino alla prossima
   invalidazione naturale. Prima di riusare un'assegnazione esistente non
   già critica, il dispatcher verifica se la migliore opportunità libera
   allo stato corrente è critica (priorità ≤ 2): in tal caso l'assegnazione
   corrente viene abbandonata (non persa: resta un'opportunità valida e
   potrà essere ripresa da un altro worker) e il worker si dirige
   sull'esigenza critica. Nessun'altra categoria può prelazionare né essere
   prelazionata da un'altra categoria non critica: la stickiness resta piena
   ovunque tranne che per queste due categorie a rischio di perdita
   irreversibile.

Questo elimina l'oscillazione osservata in V1 (Sezione 1) mantenendo la
reattività: la validità di ogni assegnazione è ricalcolata da zero ad ogni
chiamata sullo stato osservato, non da un piano salvato.

### 6.3 Coda di opportunità per tile

Stessa cascata di priorità della V1 (`URGENT_WATER` > `FEED_NEEDED` >
`PLACE_ANIMAL_NEEDED` > `HARVEST_READY` > `RECOVERY_DIG` > `CARE_NEEDED` >
`COLLECT_FERTILIZER_READY` > `BUILD_OPPORTUNITY` > `PLANT_OPPORTUNITY`),
riverificata come corretta dalla diagnosi V1 (nessuna ipotesi ha
falsificato l'ordine delle priorità in sé). Non modificata in V2.

### 6.4 Guardia di maturità del nucleo Q0 (nuova, causa primaria)

`BUY_LAND` resta condizionato dalle guardie di cassa/capacità/orizzonte
della V1 (capitale disponibile oltre riserva, orizzonte residuo minimo,
`service_pressure` sotto soglia) **più** una nuova guardia obbligatoria:

```text
core_established ⟺ plant_tiles_count > 0
                   ∧ self._core_harvest_requests >= expansion.core_min_harvest_requests
```

`plant_tiles_count > 0` chiude esplicitamente il caso osservato in V1 in cui
`service_pressure` vale banalmente `0` perché non esiste ancora nessuna
pianta, non perché il nucleo sia maturo. `_core_harvest_requests` è
incrementato ad ogni chiamata in cui il dispatch di questo worker emette
`HARVEST` (Sezione 4): richiede quindi che il nucleo abbia effettivamente
completato un numero minimo di cicli di raccolta prima di autorizzare
l'espansione territoriale, non solo che abbia piantato.

La stessa guardia `core_established` è stata estesa a `BUY_ANIMAL` durante
lo sviluppo V2 (Sezione 9.1): un primo test diagnostico ha mostrato che,
senza di essa, capitale scarso veniva dirottato su bestiame prima che le
colture generassero reddito, e `PLACE_ANIMAL_NEEDED` (priorità 3, sopra
`HARVEST_READY`) distoglieva i worker dalla raccolta proprio nella fase in
cui serviva di più.

### 6.5 Ratchet zootecnico a rischio zero (nuovo)

`BUY_ANIMAL` per una specie è consentito solo se, oltre alle guardie di
struttura/cassa già presenti in V1 e alla guardia `core_established`
(Sezione 6.4):

```text
at_risk_animal_count == 0
animal_headcount < max(1, len(worker_positions) // livestock.herd_size_workforce_divisor)
```

dove `at_risk_animal_count` conta gli animali posseduti con
`consecutive_unfed == 1 ∧ fed_today == False` (predicato `LIV-08`,
`ENGINE_VERIFIED`): capi che, se non nutriti entro la fine della giornata
corrente, fuggiranno al prossimo EOD. Il gregge non cresce finché il
servicing del gregge esistente non è dimostrabilmente in regola in questo
preciso istante osservato. Il secondo vincolo (aggiunto durante lo sviluppo
V2, Sezione 9.1) lega la dimensione massima del gregge alla workforce
attuale invece che alla sola capacità strutturale: costruire `COOP`/
`PASTURE` costa \$0 ed è quindi un pessimo proxy per la capacità reale di
foraggiamento. Inoltre, per chiamata viene autorizzato **al massimo un**
`BUY_ANIMAL`: autorizzarne più d'uno nella stessa chiamata permetterebbe a
un intero lotto di nuovi animali di atterrare prima che la chiamata
successiva possa rivalutare `at_risk_animal_count` contro di loro,
vanificando il ratchet.

### 6.6 Workforce guidata dal carico osservato (nuova)

Il target di headcount non è più `hands_target_per_quadrant × quadranti`
(formula fissa V1) ma:

```text
backlog = |URGENT_WATER| + |FEED_NEEDED| + |HARVEST_READY|
        + |RECOVERY_DIG| + |CARE_NEEDED|
target_headcount = clamp(
    ceil(backlog / workforce.tasks_per_worker_per_day),
    workforce.min_workers_per_quadrant × quadranti_sbloccati,
    workforce.max_hands
)
```

`tasks_per_worker_per_day` è configurato e realmente consumato (non
decorativo): stima quante voci della coda un worker può smaltire in una
giornata di `turnsPerDay` step, dato il costo di spostamento osservato in
V1. Il floor per quadrante evita di restare sotto-organico quando il
backlog è transitoriamente basso ma il territorio posseduto no.

### 6.7 Guardie invariate rispetto alla V1

`HIRE` (guardia di cassa + costo Fibonacci stimato, invariata: la verifica
di Sezione 1 non ha trovato difetti da correggere), politica crop
(irrigazione, raccolta, rotazione specie, guardia di orizzonte biologico),
zoning spaziale crop/livestock, guardie di mercato fill/prezzo-aware,
liquidazione terminale/endgame: ereditate dalla V1 senza modifiche
strutturali, salvo il collegamento del nuovo `target_headcount` guidato dal
carico (Sezione 6.6) al posto del moltiplicatore fisso.

---

## 7. Separazione stato online / telemetria post-hoc

Identica alla V1 (MODEL_SPEC V1 Sezione 8). Le nuove guardie (Sezioni
6.4-6.6) leggono esclusivamente campi `ONLINE_OBSERVABLE`/`ONLINE_DERIVABLE`
e il contatore agent-local delle proprie richieste passate
(`_core_harvest_requests`), mai telemetria post-hoc o outcome del ledger.

---

## 8. Failure mode e fallback

Identico alla V1: intera pipeline protetta da un blocco try/except unico,
qualunque eccezione incrementa `technical_errors` e restituisce
`{"farmer": ["PASS"], "hands": [], "market": []}`.

Limiti dichiarati aggiuntivi rispetto alla V1:

- `_core_harvest_requests` conta richieste, non conferme d'esecuzione (per
  rispettare il divieto di leggere telemetria post-hoc nel percorso
  decisionale): in linea di principio una richiesta `HARVEST` potrebbe
  fallire silenziosamente (tile già svuotata da un'altra causa nello stesso
  step) e contribuire comunque al contatore. Non osservato nei run
  development, ma dichiarato come margine di approssimazione;
  ancora nessuna logistica dedicata di prelievo fertilizzante dallo shed;
  ancora nessuna riassegnazione dinamica della zona crop/livestock dopo il
  primo sblocco quadrante; assegnazione worker→tile ancora greedy per-step,
  non un solver globale (mitigata ma non eliminata dalla persistenza dei
  target).

### 8.1 Iterazioni diagnostiche V2 (prima del benchmark registrato)

Il primo assemblaggio della V2 (guardia `core_established` solo su
`BUY_LAND`, nessun limite di gregge, nessuna prelazione d'urgenza) è stato
testato sul seed development `26090101` prima di eseguire la matrice
completa e ha rivelato tre problemi ulteriori, corretti in sequenza:

1. **Capitale dirottato su bestiame prematuro:** senza la guardia
   `core_established` anche su `BUY_ANIMAL`, il primo test ha prodotto
   `final_money = 272` con Q1/Q2 mai sbloccati per l'intero episodio,
   contro `7 483` della V1 sullo stesso seed. Diagnosticato tramite ledger:
   `BUY_ANIMAL` avveniva ripetutamente nei primi giorni, e
   `PLACE_ANIMAL_NEEDED` (priorità 3) distoglieva i worker da
   `HARVEST_READY` (priorità 4). Corretto in Sezione 6.4.
2. **Trappola di bootstrap del backlog:** `SERVICE_BACKLOG_KINDS` escludeva
   inizialmente `PLANT_OPPORTUNITY`, quindi un Q0 ancora vuoto aveva
   backlog di manutenzione nullo, mantenendo il target di headcount al
   solo floor minimo proprio quando servivano più worker per riempirlo.
   Corretto includendo `PLANT_OPPORTUNITY` nel backlog (Sezione 6.6) e
   riportando `min_workers_per_quadrant` a `3` (valore noto funzionante
   dalla V1).
3. **Fughe aumentate da 8 (V1) a 77 (prima correzione V2, su 14 run):**
   diagnosticato tracciando gli eventi di fuga direttamente sullo stato
   grezzo dell'ambiente (non sul ledger, che non attribuisce ordini
   multipli nello stesso batch): ogni singola fuga osservata avveniva
   esattamente al primo step di un nuovo giorno (`hour == 0`), con lo shed
   spesso pieno di WHEAT — non un problema di risorse. Causa: la
   persistenza (Sezione 6.2, punti 1-2) impediva a un worker di abbandonare
   un compito a bassa priorità anche quando l'unico animale posseduto
   diventava `FEED_NEEDED` e nessun altro worker era libero. Due varianti
   minori (limite di un solo `BUY_ANIMAL` per chiamata; cap del gregge
   legato alla workforce) hanno ridotto le fughe solo marginalmente
   (`77 → 74`), confermando che la causa non era la dimensione del gregge.
   La correzione risolutiva è stata la prelazione d'urgenza di Sezione 6.2,
   punto 5: dopo la sua introduzione, `13` run su `14` hanno chiuso con
   `DERIVED_EOD_ESCAPES = 0` sul benchmark registrato (Sezione 10).

Nessuna di queste tre correzioni è stata scelta osservando l'holdout; tutte
le iterazioni hanno usato esclusivamente il seed development `26090101` (più
`1838889274` per la verifica specifica della fuga, anch'esso development).

---

## 9. Target e criteri di falsificazione

Gate del prompt di remediation (identici, ripetuti per completezza):

```text
TECHNICAL_ERRORS == 0
INVALID_BATCHES == 0
STRATEGIC_INDEPENDENCE == PASS
STATE_REACTIVITY == PASS
LEDGER_RECORD_COVERAGE == 100%
DERIVED_EOD_ESCAPES == 0
MAX_QUADRANTS == 3 IN ALL RUNS
MEAN_FINAL_MONEY >= 50000
```

Criteri di falsificazione per le nuove ipotesi (dichiarati prima di
osservare il risultato del benchmark V2):

- **`H-CR2.1` falsificata** se, nonostante la guardia di maturità Q0, il
  `MEAN_FINAL_MONEY` non migliora in modo materiale rispetto alla V1
  (`9 201,7`) sugli stessi sette seed development: indicherebbe che
  l'espansione prematura non era la causa dominante, contrariamente
  all'evidenza di Sezione 1.
- **`H-CR2.2` falsificata** se la quota di comandi `MOVE` sul totale non
  scende in modo apprezzabile rispetto al `77,4%` osservato in V1 sullo
  stesso seed `26090101`: indicherebbe che la persistenza del target non
  riduce l'oscillazione come previsto.
- **`H-CR2.3` falsificata** se `DERIVED_EOD_ESCAPES` resta `> 0` nonostante
  il ratchet di Sezione 6.5: indicherebbe che la causa delle fughe non è la
  crescita del gregge oltre la capacità di servizio, ma un'altra guardia
  (es. la logistica di prelievo WHEAT).
- **`H-CR2.4` falsificata** se, isolatamente dal ratchet, si osservano
  comunque fughe attribuibili non a un animale nuovo ma a uno già presente
  da prima dell'ultima espansione del gregge: indicherebbe una debolezza
  nella logistica `FEED_NEEDED` stessa, non nel tasso di crescita.

Se un gate non è raggiunto anche in V2, il report di implementazione
documenta diagnosi e varianti provate, senza alterare il risultato
osservato, coerentemente con il processo sperimentale del repository.
