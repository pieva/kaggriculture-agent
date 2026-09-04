# MODEL_SPEC — Claude E18.1 Opponent-Reactive V1

- **Policy ID:** `CLAUDE-E18.1-OPPONENT-REACTIVE-V1`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-03
- **Foundation:** C2.1 (RECONCILED), esperimento E18
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3` (baseline E18,
  media `12.850,18`, `12,85%` del target — le linee V4/V5/V6 non sono
  predecessori: V4 e V6 sono state respinte, V5 è ricerca non promossa)
- **Sorgente:** `src/agricola/strategy/claude/e18_opponent_reactive_v1.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_1_OPPONENT_REACTIVE_V1.json`
- **Origine:** `docs/model_specs/claude/e18/prompts/E18_CLAUDE_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md`

---

## 1. Mandato e vincoli

Il prompt E18 richiede un'architettura esplicita a cinque livelli
(snapshot pubblico dell'avversario, classificatore di regime, selettore
sticky, controller di capacità/lifecycle, arbiter delle azioni), gate
architetturali separati dal denaro, e un gate economico con milestone
`16k → 25k → 50k → 100k`. Fonti di evidenza: il torneo delle architetture
dinamiche E18 V1 (Claude V3 unico candidato Claude: 28 action stream
emergenti ma nessun selector esplicito, 19 perdite zootecniche verificate,
nessun lifecycle colturale) e la forensics dell'episodio `105080066`
(Codex 6-6-2 perde `-22,6%` contro un Top3 con topologia comparabile
perché non ruota Strawberry→Wheat e raccoglie Wheat a resa media troppo
bassa).

---

## 2. Architettura a cinque livelli

### 2.1 `PUBLIC_OPPONENT_SNAPSHOT`

`_extract_opponent_snapshot(observation, my_seat)` legge esclusivamente
`observation["farms"][1 - my_seat]`: quadranti sbloccati, hands, crop
tile, weed tile, animali, pascoli. Non tocca mai `private` (che nel
contratto di osservazione contiene solo shed/seed/inventario del giocatore
osservante, mai dell'avversario), né nome, rating, replay ID o seed. Lo
snapshot è catturato una sola volta nella finestra dichiarata D4-D8
(`opponent_snapshot.window_start_day/window_end_day` in config); se non
c'è ancora evidenza a D8 la decisione viene comunque forzata con uno
snapshot nullo, per garantire esattamente una decisione per run anche in
assenza di dati.

### 2.2 `REGIME_CLASSIFIER`

`_classify_regime` calcola un punteggio di pressione serializzabile:

```text
pressure = crop_tiles + animal_count*3 + hands*2 + pasture_count
regime = HIGH_PRESSURE_WHEAT_TEMPO se pressure >= soglia (26.0), altrimenti LOW_PRESSURE_BALANCED
```

Nessun uso di nome, rating, seed, replay ID o memoria cross-episodio.

### 2.3 `STICKY_POLICY_SELECTOR`

`ClaudeE18OpponentReactiveAgentV1._maybe_decide_regime` blocca la
decisione al primo momento utile nella finestra e non la rivaluta più
(`self._regime` è sticky per il resto dell'episodio). `mode_decisions`
resta sempre `1` per run — verificato in test
(`test_regime_is_decided_exactly_once_inside_the_window`).

I due regimi differiscono materialmente su più delle due dimensioni
richieste dal prompt:

| Dimensione | `LOW_PRESSURE_BALANCED` | `HIGH_PRESSURE_WHEAT_TEMPO` |
|---|---|---|
| Workforce (`max_hands` / floor per quadrante) | 12 / 3 | 15 / 4 |
| Mix colturale (pesi target) | Wheat 40%, Strawberry 20%, Carrot 20%, Melon 20% | Wheat 70%, Carrot 15%, Strawberry 10%, Melon 5% |
| Zootecnia (strutture per quadrante) | 3 | 2 |

### 2.4 `CAPACITY_AND_LIFECYCLE_CONTROLLER`

**Lifecycle colturale** (`_plant_lifecycle_opportunity`), verificato contro
il motore ufficiale (`kaggle_environments/envs/kaggriculture/kaggriculture.py`,
regole pubbliche del gioco, non un'altra strategia):

- per le colture `ongoing` (Strawberry, Tomato) `max_lifespan_step` resta
  `-1` (nessuna vera scadenza) finché il motore non imposta un valore
  reale al raggiungimento dell'ultimo ciclo di produzione schedulato
  (`production_count == max_yield`). `ROTATION_DIG` (`DIG`) scatta solo
  quando: (a) il motore ha impostato una vera scadenza vicina, oppure (b)
  l'episodio è entrato nella finestra tardiva
  (`rotation_episode_late_days_remaining`, default 10 giorni residui) —
  **mai** su un valore sentinella negativo scambiato per "già scaduto";
- per le colture non-`ongoing` (Wheat, Carrot, Melon), `yield_units`
  cresce solo tramite `WATER` ed esclusivamente entro la finestra
  `[⌈max_yield_day/2⌉, max_yield_day]` giorni di età; l'`HARVEST` è
  differito fino a `harvest_yield_ratio` (default `0,6`) del
  `max_yield`, ma mai oltre la chiusura della finestra stessa
  (`age > max_yield_day`), non oltre un margine a step fisso pensato per
  una perenne pluri-settimanale (che avrebbe divorato l'intera finestra
  di ~2 giorni di Wheat — bug trovato e corretto durante lo sviluppo,
  Sezione 4);
- `URGENT_WATER` (priorità 1) precede sempre sia `ROTATION_DIG` (5) sia
  `HARVEST_READY` (4): un'innaffiatura pendente non viene mai scavalcata
  da una decisione di lifecycle.

**Zootecnia a rischio zero**: `_animal_orders` blocca nuovi acquisti se
*qualunque* animale ha `unfed_animal_count > 0` (non solo il ratchet V1-V3
sul secondo mancato pasto consecutivo), oltre al vincolo di capacità
strutturale e di lavoro già presente nella linea E17.

### 2.5 `ACTION_ARBITER`

Dispatch persistente per worker con coda di opportunità ordinata per
priorità (`_best_opportunity`), ereditato dalla disciplina V1-V3 di
questo stesso agente (stickiness, preemption solo per i due generi
critici, claim per evitare doppie assegnazioni). `ROTATION_DIG` condivide
il comando motore `DIG` con `RECOVERY_DIG` (weed) ma è un'opportunità
distinta con priorità propria (5, fra `HARVEST_READY` e `CARE_NEEDED`).

---

## 3. Sicurezza e lifecycle: fixture richieste

Tutte implementate come test (`docs/model_specs/claude/e18/tests/test_claude_e18_opponent_reactive_v1.py`,
29/29 passanti):

1. `test_late_strawberry_is_marked_for_rotation_dig_not_left_to_expire` —
   Strawberry vicina alla scadenza reale (motore) → `DIG`;
2. `test_strawberry_with_pending_yield_is_harvested_before_being_dug` —
   resa pendente raccolta prima di scavare;
3. `test_wheat_is_not_harvested_at_the_first_available_unit` /
   `test_wheat_is_harvested_once_it_reaches_its_yield_target` — Wheat non
   raccolto prematuramente, raccolto al target di resa;
4. `test_wheat_harvest_is_never_deferred_past_the_liquidation_window` —
   nessuna raccolta differita oltre la finestra di liquidazione;
5. `test_urgent_water_still_outranks_a_deferred_harvest` — nessuna
   coltura servibile abbandonata a weed;
6. `test_livestock_emergency_outranks_non_urgent_land_expansion` —
   emergenza zootecnica prevalente;
7. `test_no_animal_purchase_while_any_animal_is_unfed` — ledger a rischio
   zero.

---

## 4. Bug trovato e corretto durante lo sviluppo

La prima implementazione leggeva `max_lifespan_step` senza distinguere il
sentinella `-1` (colture `ongoing` ancora produttive) da una vera
scadenza, e usava lo stesso margine di sicurezza a step fisso
(`rotation_lookahead_steps`, 48 step / 2 giorni) sia per le perenni sia
per Wheat. Risultato osservato prima della correzione: partite senza
collasso di cassa ma con denaro persistentemente basso (`2.904` contro
Copilot su un seed, con fino a 38 tile coltivate contemporaneamente) —
il margine di sicurezza forzava una raccolta anticipata quasi ad ogni
ciclo Wheat, vanificando il differimento verso il target di resa. Dopo la
correzione (Sezione 2.4: `age > max_yield_day` per le non-ongoing, vero
sentinella per le ongoing) lo stesso seed passa da `2.904` a `7.482` sullo
stesso confronto. Non è stato un collasso stile V4/V5/V6 (zero tecnica a
rischio, zero errori) ma una sotto-monetizzazione sistematica; il fix è
verificato dai test di Sezione 3, non solo dal singolo seed di diagnosi.

---

## 5. Provenienza e vincoli

Nessun import da `agricola.strategy.codex`, `agricola.strategy.antigravity`
o `agricola.strategy.copilot` (verificato in test,
`test_source_has_no_other_agent_strategy_dependency`). Le costanti
numeriche di gioco (prezzi semi, `first_yield_day`, `max_yield_day`,
costi animali, formula Fibonacci di `HIRE`, geometria dello shed) sono
fatti pubblici `ENGINE_VERIFIED`, letti dal motore ufficiale
`kaggle_environments` (non da un'altra strategia) e già portati avanti
dalla propria linea E17. Codex E18 è stato affrontato solo come
avversario black-box (la sua sola factory pubblica, mai il sorgente).
Nessun seed holdout o final-confirmation consumato; nessuna submission
Kaggle senza nuova autorizzazione.

---

## 6. Stato del benchmark

Vedi `docs/model_specs/claude/e18/reports/E18_CLAUDE_OPPONENT_REACTIVE_V1_DEVELOPMENT_REPORT_IT.md`
per la matrice di sviluppo completa (7 seed × 2 seat × 3 avversari) e i
quattro verdetti richiesti dal prompt.
