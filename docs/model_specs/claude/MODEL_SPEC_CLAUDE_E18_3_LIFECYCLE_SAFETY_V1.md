# MODEL_SPEC — Claude E18.3 Lifecycle-Safety V1

- **Policy ID:** `CLAUDE-E18.3-LIFECYCLE-SAFETY-V1`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-04
- **Foundation:** C2.1 (RECONCILED), esperimento E18
- **Predecessore:** `CLAUDE-E18.2-OPPONENT-REACTIVE-V2`
- **Sorgente:** `src/agricola/strategy/claude/e18_lifecycle_safety_v3.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json`
- **Origine:** `docs/model_specs/claude/e18/prompts/E18_CLAUDE_LIFECYCLE_SAFETY_V3_BUILD_PROMPT_IT.md`
- **Stato:** `FROZEN` — linea Claude congelata dal 2026-09-04 (`FROZEN_PERFORMANCE_GAP`,
  vedi [README](README.md)). Candidata più recente e meglio verificata della
  linea E18, ma non promossa: `SAFETY_GATE = FAIL` (13/28 perdite verificate,
  richiesto 0/28). Non descrive una policy attiva né sottomessa a Kaggle.
  Le Sezioni 7-13 aggiungono struttura di revisione (obiettivo, strategia,
  decisioni, reazioni, coerenza con la Foundation, stato di realizzazione,
  file di implementazione) al testo diagnostico originale delle Sezioni 0-6,
  lasciato invariato perché citato per numero di sezione dal
  [report di sviluppo](e18/reports/E18_CLAUDE_LIFECYCLE_SAFETY_V3_DEVELOPMENT_REPORT_IT.md).

---

## 0. File concorrenti già presenti (git status, non miei, non toccati)

All'apertura di questo lavoro `git status --short` mostrava una riorganizzazione
di repository su larga scala già in corso da altre sessioni (rimozione e
spostamento dei report `experiments/archive/e0*`, modifiche a
`docs/model_specs/*/README.md` e ai `MODEL_SPEC` storici E17/E18.1/E18.2,
`experiments/README.md`, `.gitignore`, oltre ai file già registrati nella
sessione precedente per il torneo Claude/Copilot/Antigravity). Nessuno di
questi file è stato letto oltre a quanto già autorizzato o modificato da
questa sessione; sono stati creati soltanto nuovi path V3 nel namespace
Claude.

---

## 1. Audit diagnostico (obbligatorio prima di qualunque modifica)

Il torneo Claude/Copilot/Antigravity (42 match) ha chiuso V2 con
`verified_livestock_losses = 24` su 28 match contro Copilot E18.2 e
Antigravity E18.1 — peggio dei 31/42 di V1, nonostante il fix del buffer di
grano proattivo di V2. Il match peggiore (seed `180903002`, seat 0 vs
Copilot E18.2, 4 perdite verificate) è stato tracciato turno per turno
prima di scrivere qualunque fix, seguendo la stessa disciplina delle sessioni
precedenti ("niente tuning cieco delle soglie").

### 1.1 Causa A — l'identità del worker era un indice di lista, non stabile

Tracciando `self._assignments` turno per turno (giorno 21), lo stesso
`FEED_NEEDED (1, 0)` salta fisicamente da `hand:6` a `hand:5` a `hand:2` a
`hand:1` a `hand:0` a `farmer` in dieci turni consecutivi. Causa isolata:
`worker_keys = ["farmer"] + [f"hand:{i}" for i in range(...)]` viene
ricostruito da `observation["farms"][seat]["hands"]` a ogni chiamata, e
l'ordine di quella lista non è stabile — un dump diretto della lista grezza
(`hands`) su turni adiacenti mostra sia crescita (nuove assunzioni) sia
riordino delle posizioni esistenti. Il worker "con quell'incarico" non è mai
lo stesso worker fisico per due turni di fila: l'incarico non converge mai
perché parte da una posizione diversa a ogni turno.

### 1.2 Causa B — il timeout di stallo non scattava mai su un PICKUP bloccato

Giorno 28, stesso match: il farmer resta fermo alla shed e riemette
`["PICKUP", "WHEAT", 1]` per 24 turni consecutivi, mentre `shed["WHEAT"]`
resta esattamente a `0` per l'intera giornata. `assignment.stalled_steps`
incrementava soltanto su un `PASS` letterale; un `PICKUP` ripetuto — che
V2 emette solo quando la risorsa cercata è ancora assente dall'inventario —
non veniva mai riconosciuto come uno stallo, quindi l'incarico non veniva
mai abbandonato né riassegnato: un intero giorno bruciato con zero
progresso di alimentazione.

Due cause distinte, entrambe nel solo layer `ACTION_ARBITER`, nessuna delle
due toccata da V1→V2.

---

## 2. Modifiche implementate (due fix meccanici, nessuna terza leva)

### 2.1 Identità stabile del worker (`_track_worker_identities`)

Nuovo metodo che sostituisce la chiave posizionale con un'identità persistente
assegnata per corrispondenza greedy alla posizione precedente più vicina: un
worker si muove al massimo una tile per turno (ogni comando non-move lo
lascia fermo, distanza 0), quindi una distanza `<=1` da un'identità precedente
non ancora reclamata è un abbinamento sicuro; ciò che resta senza
corrispondenza è una nuova assunzione. Il farmer resta la chiave letterale
`"farmer"` (campo distinto, indice 0, mai parte della lista `hands`
riordinata). `self._hand_identity_positions` e `self._assignments` (tranne
`"farmer"`) vengono azzerati a ogni cambio di giorno, poiché l'audit conferma
che la manodopera assunta viene ricostituita da zero ogni giorno (ogni match
osservato crolla al solo farmer al primo turno di ogni nuova giornata).

### 2.2 PICKUP trattato come PASS ai fini dello stallo

`_resolve_feed` e `_resolve_place_animal` emettono `PICKUP` soltanto quando
la risorsa cercata è ancora assente dall'inventario, e un singolo pickup
riuscito porta sempre a un comando `MOVE`/terminale alla chiamata
successiva (basta una sola unità per procedere). Un `PICKUP` *ripetuto* può
quindi significare solo che la shed non ha davvero nulla da dare in quel
momento: `if command[0] in ("PASS", "PICKUP"): stalled_steps += 1` cattura
esattamente questo caso senza mai penalizzare un pickup che sta
legittimamente progredendo.

### 2.3 Cosa NON è cambiato

Layer 1-3 (snapshot D4-D8, classificatore, selettore sticky), lifecycle
colturale KEEP/HARVEST/ROTATION_DIG, buffer di grano proattivo, cap di
superficie coltivata e coda di emergenza restano identici byte-per-byte a
V2. Nessun terzo regime, nessun nuovo campo di snapshot, nessuna soglia
ritoccata: la config V3 è identica a V2 a parte `policy_id`/`model_spec`.

---

## 3. Verifica diretta sul match di diagnosi

| | V2 | V3 |
|---|---:|---:|
| Seed `180903002` seat 0 vs Copilot E18.2, perdite verificate | 4 | **0** |
| Denaro seat 0 | 14.871,00 | 12.124,00 |

Riproduzione automatizzata in
`docs/model_specs/claude/e18/tests/test_claude_e18_lifecycle_safety_v3.py::test_v3_eliminates_losses_on_the_worst_traced_v2_match`.

---

## 4. Gate e stato del benchmark

Eseguito sui sette seed development E18, entrambi i seat, contro Copilot
E18.2 e Antigravity E18.1 (gli stessi avversari del torneo che ha aperto
questo ciclo). Risultati completi, verdetti e decisione finale in
`docs/model_specs/claude/e18/reports/E18_CLAUDE_LIFECYCLE_SAFETY_V3_DEVELOPMENT_REPORT_IT.md`.

Sintesi: `verified_livestock_losses` scende da 24/28 a **13/28** (-45,8%),
zero errori/fallback, 28-0 il record contro entrambi gli avversari. Il gate
di sicurezza (`== 0` in 28/28, bloccante) **non è ancora superato**: un
terzo pattern residuo, distinto dalle cause A/B, è stato tracciato (Sezione
5) e diagnosticato ma non corretto in questo ciclo, per non combinare più
cause non isolate nello stesso passaggio (stessa disciplina già registrata
nel ciclo E17 V4→V5→V6 e nel report V2, Sezione 6).

---

## 5. Causa residua diagnosticata (non ancora corretta, per V4)

Un secondo audit sul match ancora in perdita dopo il fix (stesso seed,
giorno 26) mostra `self._assignments` contenente **due** chiavi diverse
(`farmer` e un `hand:N`) puntate sullo stesso `FEED_NEEDED (1, 0)`
contemporaneamente, e nello stesso giorno vengono coniati **quindici** id di
mano distinti mentre la forza lavoro osservata resta stabile a nove — molti
più del numero di assunzioni reali quel giorno. Causa isolata: l'abbinamento
greedy per distanza minima (Sezione 2.1) non è un matching ottimale; quando
più worker sono ravvicinati (comune vicino alla shed centrale su una
board 10×10), può fallire l'abbinamento corretto e coniare id nuovi non
necessari, ricreando in forma più lieve lo stesso sintomo che il fix doveva
chiudere. La prossima iterazione deve sostituire l'abbinamento greedy con un
matching a costo minimo (es. algoritmo ungherese) sulle distanze, non
un ulteriore ritocco del raggio di tolleranza.

---

## 6. Vincoli invariati

Identici a V1/V2: nessun import da `agricola.strategy.codex`,
`agricola.strategy.antigravity` o `agricola.strategy.copilot`; nessuna
tabella di azioni indicizzata per step; snapshot dell'avversario limitato a
`observation["farms"][opponent_seat]` pubblico, mai `private`, mai
nome/rating/replay ID/seed/memoria cross-episodio. Copilot E18.2 e
Antigravity E18.1 affrontati solo come avversari black-box tramite le
rispettive factory pubbliche. Nessun seed holdout o final-confirmation
consumato; nessuna modifica al manifest comune; nessuna submission Kaggle.

---

## 7. Obiettivo e ipotesi

**Obiettivo perseguito:** massimizzare la cassa finale (`final_money_outcome`)
di una fattoria E18 (board 10×10, 3 quadranti target) rispettando due vincoli
bloccanti del prompt di sviluppo: zero perdite verificate di bestiame per
fuga (`verified_livestock_losses == 0`, gate di sicurezza) e un lifecycle
colturale che non lasci una coltura decadere in `WEED` o scadere senza
raccolta.

**Ipotesi centrale:** un controller a cinque livelli espliciti — fotografia
pubblica dell'avversario, classificatore di regime, selettore sticky,
controller di capacità/lifecycle, arbiter di dispatch — permette di
condizionare mix colturale, dimensione della manodopera e densità zootecnica
al regime osservato dell'avversario, separando "cosa fare" (livelli 1-4) da
"chi lo fa e come" (livello 5), senza introdurre memoria cross-episodio né
dipendenza da nome/rating/seed dell'avversario.

**Ambito:** sette seed di sviluppo E18 (`180903001`-`180903007`), entrambi i
seat, contro due soli avversari congelati affrontati come black-box (Copilot
E18.2, Antigravity E18.1). Nessun seed holdout o final-confirmation è stato
consumato.

**Assunzioni:**
- i fatti numerici di gioco (prezzi semi, `first_yield_day`, `max_yield_day`,
  costi animali, formula Fibonacci di `HIRE`) sono valori `ENGINE_VERIFIED`
  **duplicati nel sorgente stesso** (dizionari `CROPS`/`ANIMALS`), non letti
  dinamicamente dalla configurazione dell'engine a runtime;
- l'avversario è affrontato esclusivamente come funzione black-box: l'unica
  evidenza usata per classificare il regime è
  `observation["farms"][opponent_seat]` pubblico, catturato una sola volta
  nella finestra D4-D8;
- l'evidenza economica riportata (Sezione 4) riguarda solo i due avversari
  congelati usati in questo ciclo, non Copilot/Antigravity in generale né Codex.

**Limiti dichiarati:** il gate di sicurezza non è chiuso (Sezioni 4-5); un
solo regime (`LOW_PRESSURE_BALANCED`) è stato osservato nei 28 match di
sviluppo, quindi il ramo `HIGH_PRESSURE_WHEAT_TEMPO` resta verificato solo
dai test unitari, non da un match end-to-end contro un avversario che lo attivi.

## 8. Strategia

**Pianificazione della produzione.** Nessun calendario fisso: a ogni
chiamata `_extract_features` ricostruisce una coda di opportunità per-tile e
per-animale (`URGENT_WATER`, `FEED_NEEDED`, `PLACE_ANIMAL_NEEDED`,
`HARVEST_READY`/`ROTATION_DIG`/`RECOVERY_DIG`, `CARE_NEEDED`,
`COLLECT_FERTILIZER_READY`, `PLANT_OPPORTUNITY`, `BUILD_OPPORTUNITY`),
ordinata per una priorità numerica fissa (1 = irrigazione urgente, 10 = nuova
semina). Il mix varietale delle nuove semine segue pesi target per regime
(`crop_species_weights`), scelti dal deficit rispetto al mix corrente
(`_choose_plant_species`), non dal semplice conteggio meno-piantato usato
nelle versioni E17.

**Pianificazione degli investimenti.** L'espansione fondiaria (`BUY_LAND`) è
ammessa solo quando il quadrante core (NW) è "stabilito" (`_core_established`:
soglia di richieste di raccolta e di fill ratio) e la pressione di servizio
(`service_pressure`) resta sotto un tetto configurato; l'acquisto di semi e
animali è sospeso durante un'emergenza zootecnica (Sezione 10). L'acquisto
di un nuovo animale richiede che il buffer di grano di sicurezza esista già
nello shed (`_wheat_stock_orders`, attivato dalla sola presenza di una
struttura, non dalla presenza di un animale).

**Pianificazione della manodopera.** `_hire_orders` dimensiona il target di
`HIRE` sul massimo fra un floor per quadrante
(`min_workers_per_quadrant × quadranti`) e un carico derivato dal backlog di
servizio diviso per un tasso di compiti-per-lavoratore-al-giorno, entro il
tetto `max_hands` del regime attivo. L'identità dei worker (fix V3) è
tracciata per abbinamento greedy alla posizione precedente più vicina, così
un incarico persistente segue lo stesso lavoratore fisico invece di un
indice di lista che l'engine può riordinare.

**Orizzonte del piano e condizioni di revisione.** Il piano è puramente
intra-episodio: nessuno stato sopravvive fra partite. All'interno di un
episodio, il regime è deciso una sola volta nella finestra dichiarata D4-D8 e
resta sticky. Fra un round di sviluppo e il successivo (V1→V2→V3), la
revisione richiede un audit causale verificato turno per turno sul match
peggiore prima di scrivere qualunque correzione — mai un ritocco cieco delle
soglie — e ogni ciclo corregge al massimo le cause isolate in
quell'audit, rimandando esplicitamente le cause residue diagnosticate ma non
ancora corrette (Sezione 5) alla versione successiva.

## 9. Decisioni

**Feature realmente usate** (verificate leggendo il sorgente, non dichiarate):

| Dominio Feature Model | Feature usate | Dove nel codice |
|---|---|---|
| TIME (`TMP-01/02/04/08/09`) | `step`, `day`, `turns_per_day`, giorni/step residui | `snap.clock.*` dentro `_extract_features` |
| CROP (`CRP-01..04, 08, 11..13`) | `tile.kind`, `crop`, `planted_day`, età, `watered_today`, `consecutive_unwatered`, `max_lifespan_step` | `_extract_features`, `_plant_lifecycle_opportunity` |
| FERTILIZER (`FRT-01`) | `fertilized_until_day` | `_opportunistic_fertilize` |
| LIVESTOCK (`LIV-02, 05..07, 10`) | tipo struttura, `fed_today`, `cared_today`, `consecutive_unfed`, `fertilizer_available` | `_extract_features` |
| WORKFORCE (`WRK-03..05`) | posizioni e inventari di farmer/hands | `_extract_features`, `_track_worker_identities` |
| INVENTORY (`INV-01, 05`) | `private.shed`, `private.seeds` | `_extract_features` |
| MARKET (`FRM-01, MKT-02, MKT-07, MKT-LIMIT`) | `farm.money`, `market.prices`, formula Fibonacci `HIRE`, `maxMarketOrdersPerTurn` | `_extract_features`, `_hire_orders`, `_build_market_orders` |

**Non usate, dichiaratamente:** i 23 predicati formali `ELG-01..23` non sono
calcolati come predicati espliciti e riusabili — le stesse guardie sono
reimplementate ad hoc dentro ciascun `_resolve_*`/`_*_orders`, con rischio di
divergenza silenziosa se una guardia dell'engine cambia senza un
aggiornamento corrispondente qui. `livestock_output_storage_capacity`
(`ANIMALS[...].max_held` nella Foundation) non è letto: il controller non
verifica se la resa di un animale è vicina al tetto di accumulo sulla tile
prima di rimandare la raccolta. La telemetria `POST-*` è realizzata solo
parzialmente (`telemetry_snapshot()`/`_day_counters`: harvest/water/dig/feed/
move/pass/venduto per giorno), non l'intero catalogo `POST-01..57`.

**Criteri di scelta e priorità fra azioni concorrenti.** Priorità fissa e
totalmente ordinata (`priority`, poi `secondary`, poi penalità
fuori-quadrante, poi distanza): 1 `URGENT_WATER` — 2 `FEED_NEEDED` — 3
`PLACE_ANIMAL_NEEDED` — 4 `HARVEST_READY` — 5 `ROTATION_DIG` — 6
`RECOVERY_DIG` — 7 `CARE_NEEDED` — 8 `COLLECT_FERTILIZER_READY` — 9
`BUILD_OPPORTUNITY` — 10 `PLANT_OPPORTUNITY`. Solo le priorità ≤
`CRITICAL_PRIORITY_CEILING` (2) possono interrompere un incarico persistente
già assegnato a un worker.

**Vincoli:** nessun import da `agricola.strategy.codex`,
`agricola.strategy.antigravity` o `agricola.strategy.copilot`; nessuna
tabella di azioni indicizzata per step; snapshot dell'avversario limitato a
`observation["farms"][opponent_seat]` pubblico, mai a `private`, nome,
rating, replay ID, seed o memoria cross-episodio.

**Parametri principali e motivazione** (config
`CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json`):

| Parametro | Valore | Motivazione registrata |
|---|---:|---|
| `regime_pressure_threshold` | 26,0 | Soglia di pressione avversaria (MODEL_SPEC E18.1 Sezione 2.2) |
| `harvest_yield_ratio` | 0,6 | Frazione del `max_yield` a cui differire la raccolta di colture non-ongoing (E18.1 Sezione 4, corregge una raccolta prematura) |
| `max_serviceable_crop_tiles_per_worker` | 3,0 | Cap di superficie coltivata legato ai worker realmente assunti (E18.2 remediation item 3; audit: MOVE ≈ 3× le azioni produttive con 38 tile e 10-11 worker) |
| `feed_security_buffer_per_animal` | 3 | Scorta minima di grano per capo prima di autorizzare un nuovo acquisto (E18.2 remediation item 1) |
| `max_at_risk_animals_for_new_purchase` | 0 | Nessuna crescita del gregge finché un animale ha saltato un pasto (gate di sicurezza) |
| `assignment_stall_timeout` | 3 | Turni di stallo (`PASS`/`PICKUP` ripetuto) prima di riassegnare un worker (E18.3, causa B, Sezione 1.2) |

## 10. Reazioni

**Fallback tecnico.** `__call__` avvolge l'intera decisione in un
`try/except` generico: qualunque eccezione incrementa `technical_errors` e
restituisce `SAFE_PASS_ACTION` (`{"farmer": ["PASS"], "hands": [], "market": []}`),
mai propagata.

**Carenze e stalli.** Un worker con un incarico persistente che riemette
`PASS` o `PICKUP` per `assignment_stall_timeout` chiamate consecutive viene
liberato e ricandidato alla migliore opportunità disponibile (`_decide_worker`).

**Conflitti fra bisogni concorrenti.** Quando almeno un animale non è stato
nutrito oggi (`animals_at_risk`), `BUY_LAND` e `BUY_SEED` sono soppressi per
quella chiamata; `HIRE`, gli ordini di grano e `SELL` restano attivi perché
risolvono l'emergenza invece di contenderla (`_build_market_orders`).

**Chiusura della partita.** `in_shutdown` (giorni residui ≤
`shutdown_days_remaining`, default 5) sospende nuovi impegni di crescita
(terreno, semi, animali); `in_liquidation` (giorni residui ≤
`liquidation_days_remaining`, default 3) forza la raccolta immediata di
colture non-ongoing con resa residua e di colture ongoing vicine alla
scadenza, indipendentemente dal target di resa altrimenti atteso
(`_plant_lifecycle_opportunity`).

**Imprevisti non ancora risolti.** La causa residua diagnosticata alla
Sezione 5 (abbinamento greedy dell'identità worker non ottimale sotto
affollamento) non ha una reazione implementata: è documentata come lavoro
futuro, non corretta con un ulteriore ritocco di soglia, per evitare di
combinare cause non isolate nello stesso ciclo (disciplina dichiarata fin da
E17 V4→V5→V6).

## 11. Coerenza con la Foundation

**Concetti della Foundation usati correttamente, verificati contro il
codice in questa revisione:**
- `crop_harvest_readiness` (Ontologia, sez. C; Feature Model `CRP-10`) è
  rispettato: `_plant_lifecycle_opportunity` non emette mai `HARVEST_READY`
  con `yield_units <= 0`;
- la distinzione fra sentinella `max_lifespan_step = -1` (colture ongoing
  ancora produttive) e scadenza reale, richiesta dalla State Machine
  (sezione "Fertilizer State Machine" / Crop & Tile), è rispettata
  esplicitamente (`has_real_deadline`);
- `animal_escape_condition` (Ontologia, sez. D: fuga al secondo
  `consecutive_unfed`) motiva la soglia `max_at_risk_animals_for_new_purchase = 0`,
  anche se il controller implementa un divieto di crescita del gregge, non
  un contatore esplicito di "giorni alla fuga";
- `worker_multi_occupancy` (Ontologia, sez. B) è implicitamente rispettato:
  il codice non impone alcun vincolo di collisione fra worker sulla stessa cella.

**Separazione dichiarata fra fatti e scelte:** i dizionari `CROPS`/`ANIMALS`
nel sorgente sono un **duplicato locale** dei fatti `ENGINE_VERIFIED` della
Foundation (prezzi semi, `first_yield_day`, `max_yield_day`, `max_yield`,
costi animali), non una lettura dinamica della configurazione dell'engine a
runtime. Confrontati riga per riga con `ENGINE_CONTRACT.md` e
`KAGGRICULTURE_STATE_MACHINE_C2_1.md` durante questa revisione, i valori
risultano coerenti per tutte e cinque le colture e i tre animali.
**Discrepanza segnalata, non corretta in questa revisione documentale:**
questa duplicazione è un rischio di manutenzione futura, non un errore
osservato oggi — se l'engine cambiasse questi valori, il sorgente Claude non
se ne accorgerebbe automaticamente, a differenza di una lettura da
`configuration_snapshot`.

**Concetti della Foundation non sfruttati dal controller:**
`livestock_output_storage_capacity` (`ANIMALS[...].max_held`, Ontologia sez.
D) non è letto; il controller può quindi ritardare `HARVEST` su una tile
animale già satura, perdendo resa oltre il tetto — un caso distinto dalla
fuga per fame, non coperto né dal gate di sicurezza attuale né da alcuna
fixture di test.

**Nessuna presunzione fuori Foundation individuata** nelle sezioni
verificate: le costanti numeriche, le finestre temporali (fertilizzante,
finestra acqua) e i vincoli di batch di mercato letti dal codice
corrispondono ai valori pubblicati in `ENGINE_CONTRACT.md` e nel Feature Catalog.

## 12. Stato di realizzazione

**Implementato e verificato da test/matrice di sviluppo:**
- i cinque livelli (snapshot, classificatore, selettore sticky, controller
  lifecycle/capacità, arbiter);
- lifecycle colturale `KEEP`/`HARVEST`/`ROTATION_DIG` per colture ongoing e
  non-ongoing;
- buffer di grano proattivo e coda di emergenza zootecnica;
- cap di superficie coltivata legato alla manodopera;
- identità stabile del worker e stall-timeout esteso a `PICKUP` (correzioni V3).

**Parzialmente realizzato:**
- `SAFETY_GATE` (bloccante per la promozione) **non superato**: 13/28
  perdite verificate contro un requisito di 0/28 (Sezione 4). Le due cause
  corrette (identità worker, stallo `PICKUP`) sono verificate; una terza
  causa (abbinamento greedy non ottimale sotto affollamento) è diagnosticata
  ma non corretta (Sezione 5);
- `DYNAMIC_GATE` è solo informativo: il ramo `HIGH_PRESSURE_WHEAT_TEMPO` non
  è mai stato esercitato in un match di sviluppo (nessun avversario
  congelato lo attiva), quindi resta verificato solo a livello di test
  unitari, non di comportamento end-to-end osservato.

**Proposto ma non implementato in questo sorgente:** un matching a costo
minimo (es. algoritmo ungherese) per l'identità dei worker, indicato come
prossimo passo nel report di sviluppo (Sezione 6 del report).

**Non in ambito di questa revisione:** nessuna submission Kaggle esiste per
questa candidata o per qualunque versione della linea Claude; la linea è
congelata dal 2026-09-04 e non riprende sviluppo o benchmark finché non
viene preregistrata una nuova ipotesi che superi insieme il gate economico e
quello di sicurezza (vedi [README](README.md)).

## 13. File di implementazione

| File | Ruolo | Parte della strategia implementata | Categoria |
|---|---|---|---|
| [e18_lifecycle_safety_v3.py](../../../src/agricola/strategy/claude/e18_lifecycle_safety_v3.py) | Controller a 5 livelli: snapshot, classificatore, selettore sticky, capacità/lifecycle, arbiter; fallback `SAFE_PASS_ACTION`; telemetria giornaliera | Sezioni 8-10, 2.1-2.4 | Runtime |
| [observation_contract.py](../../../src/agricola/core/observation_contract.py) | Parsing e normalizzazione policy-neutral dell'osservazione (`CodexObservationAdapter.parse`), clock e snapshot condivisi fra modeler | Ingresso dati per Sezione 8 (`snap.clock`, `snap.farm`, `snap.private`, `snap.market`) | Runtime (condiviso, autorizzato dal manifest Foundation) |
| [CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json](e18/configs/CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json) | Parametri di riserva cassa, dispatch, espansione, colture, lifecycle, zootecnia, endgame, finestra snapshot, profili di regime | Tabella parametri Sezione 9 | Configurazione |
| [run_claude_e18_v3_lifecycle_safety_dev_matrix.py](e18/tools/run_claude_e18_v3_lifecycle_safety_dev_matrix.py) | Esegue la matrice di sviluppo (7 seed × 2 seat × 2 avversari congelati black-box) e produce l'artifact derivato | Verifica di Sezione 4/12 | Builder (runner di sviluppo; non genera submission) |
| [test_claude_e18_lifecycle_safety_v3.py](e18/tests/test_claude_e18_lifecycle_safety_v3.py) | Fixture di lifecycle ereditate da V2, fixture nuove per identità worker e stallo `PICKUP`, regressione end-to-end sul match di diagnosi | Sezioni 3 (audit), 10 (reazioni) | Test |

**Submission:** nessuna. La linea Claude non ha prodotto un bundle o un file
`main.py` per Kaggle; è congelata dal 2026-09-04 prima di raggiungere il
gate di sicurezza richiesto per la promozione.

**Non incluso nella tabella perché non è codice implementativo:**
[E18_CLAUDE_LIFECYCLE_SAFETY_V3_DEV_MATRIX.json](e18/artifacts/derived/E18_CLAUDE_LIFECYCLE_SAFETY_V3_DEV_MATRIX.json)
e il relativo `.csv` sono l'output generato dal runner, evidenza diagnostica
citata nel [report di sviluppo](e18/reports/E18_CLAUDE_LIFECYCLE_SAFETY_V3_DEVELOPMENT_REPORT_IT.md),
non un file sorgente.

**Dipendenze non verificabili come implementazione della strategia
Claude:** il runner importa le factory pubbliche di Copilot E18.2 e
Antigravity E18.1 (`agricola.strategy.copilot.e18_opponent_reactive_v2`,
`agricola.strategy.antigravity.antigravity_e18_reactive_reboot_v1`)
esclusivamente come avversari black-box; questi moduli non sono stati letti
oltre al punto di ingresso pubblico, come previsto dai vincoli della Sezione
6, e non sono quindi elencati come file di implementazione della strategia Claude.
