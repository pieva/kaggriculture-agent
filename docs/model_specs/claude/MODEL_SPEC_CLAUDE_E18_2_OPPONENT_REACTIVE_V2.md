# MODEL_SPEC — Claude E18.2 Opponent-Reactive V2 (remediation)

- **Policy ID:** `CLAUDE-E18.2-OPPONENT-REACTIVE-V2`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-03
- **Foundation:** C2.1 (RECONCILED), esperimento E18
- **Predecessore:** `CLAUDE-E18.1-OPPONENT-REACTIVE-V1`
- **Sorgente:** `src/agricola/strategy/claude/e18_opponent_reactive_v2.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_2_OPPONENT_REACTIVE_V2.json`
- **Origine:** `docs/model_specs/claude/e18/prompts/E18_CLAUDE_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md`

---

## 0. File concorrenti già presenti (git status, non miei, non toccati)

Per istruzione esplicita del prompt di remediation, registro qui i file
già presenti/modificati da altre sessioni all'apertura di questo lavoro,
senza correggerli o attribuirli a errori propri:

```text
 M .gitignore
 D data/replays/json/*.json (18 file, pulizia raw replay)
 M data/replays/json/json.md
 M docs/EXPERIMENT_LOG.md
 M docs/NEW_SESSION.md
 M docs/PROJECT_STATE.md
 M experiments/e18/README.md
 M experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json
 M src/agricola/strategy/copilot/__init__.py
?? src/agricola/strategy/codex/codex_e18_opponent_reactive_topology.py
?? src/agricola/strategy/copilot/e18_opponent_reactive_v1.py
?? submission/submission_codex_e18_opponent_reactive_662_770.py
?? experiments/e18/tools/common/run_e18_four_agent_reactive_tournament_v2.py
?? experiments/e18/tests/test_e18_four_agent_reactive_tournament_v2.py
?? experiments/e18/reports/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2_REPORT_IT.md
(più i miei stessi file V1 non ancora committati)
```

Nessuno di questi è stato letto oltre a quanto già autorizzato (config e
report comuni, mai sorgenti strategici Codex/Copilot/Antigravity).

---

## 1. Audit diagnostico (obbligatorio prima di qualunque modifica)

Due seed sono stati tracciati giorno per giorno prima di scrivere
qualunque fix, come richiesto ("niente tuning cieco delle soglie"):
`180903001` e `180903003`, entrambi V1 contro Codex E18.1 (seat 1).

### 1.1 Seed `180903001` — sotto-monetizzazione senza collasso

Con campionamento corretto a fine giornata (non nell'istante di reset
giornaliero delle `hands`, errore già commesso e corretto in sessioni
E17 precedenti): workforce cresce regolarmente (3→11), `HIRE` e `SELL`
funzionano (267 e 46 ordini nell'intera partita). Ma `MOVE` (4.055)
supera di circa 3× la somma di tutte le azioni produttive (harvest 172 +
water 872 + dig 46 + plant 165 + sell 46 + place 33 ≈ 1.334), con
superficie coltivata fino a 38 tile concorrenti. Denaro finale `6.160`.

### 1.2 Seed `180903003` — collasso a cassa bloccata + perdita animale

Traccia posizione-per-posizione degli animali: `SHEEP` piazzato a D11,
`fed_today=False` sia a D11 sia a D12 (`consecutive_unfed=1`), fuggito a
D13. Causa isolata: il buffer di grano (`_wheat_stock_orders` V1) si
attivava solo con `animal_headcount > 0`, cioè **dopo** che il primo
animale era già presente — nessun grano in shed nella finestra in cui
serviva. Separatamente, D20-D29: `hands` crolla da 10 a 2 a 0 e resta a
`0` per 9 giorni consecutivi, con denaro bloccato esattamente a `138`
(sotto `hire_reserve=150`, quindi `HIRE` si rifiuta correttamente di
spendere l'ultima riserva, ma senza lavoratori il denaro non risale mai).
Stesso pattern della trappola a cassa bloccata già diagnosticata e
parzialmente affrontata in E17 (V5/V6): un'eccessiva superficie coltivata
relativa alla workforce reale precede il crollo di cassa.

**Due cause distinte, non un'ipotesi sola**: (a) il buffer di grano è
reattivo invece che proattivo; (b) nessun limite lega la superficie
piantata alla capacità di servizio realmente disponibile.

---

## 2. Modifiche implementate (due famiglie causali, nessuna terza)

### 2.1 Buffer di grano proattivo (`_wheat_stock_orders`, `_animal_orders`)

- `_wheat_stock_orders` si attiva da `structures_total > 0` (una
  struttura zootecnica esiste) invece che da `animal_headcount > 0` (un
  animale esiste già). Il target di scorta usa `max(1, animal_headcount)`,
  quindi accumula per almeno un capo anche a zero animali.
- `_animal_orders` aggiunge un controllo esplicito: nessun `BUY_ANIMAL`
  se `shed["WHEAT"] < feed_security_buffer_per_animal`. L'acquisto
  aspetta che il buffer esista già, invece di crearlo dopo.

### 2.2 Coda di emergenza (`_build_market_orders`, nuovo campo `_Features.animals_at_risk`)

Quando almeno un animale non è stato nutrito oggi
(`unfed_animal_count > 0`), `BUY_LAND` e `BUY_SEED` sono soppressi per
quella chiamata; `HIRE`, gli ordini di grano e `SELL` restano attivi
(più lavoratori e più scorta di grano risolvono l'emergenza, non la
contendono). Il dispatch dei worker già preempta gli incarichi non
critici quando emerge `FEED_NEEDED` (priorità 2, meccanismo ereditato
da V1/E17); la coda di emergenza aggiunge il livello di mercato mancante.

### 2.3 Cap di superficie coltivata (`_extract_features`, nuovo `serviceable_crop_capacity`)

Nuovo campo di config `crop.max_serviceable_crop_tiles_per_worker`
(default `3,0`). Le nuove opportunità `PLANT_OPPORTUNITY` sono limitate a
`worker_count * max_serviceable_crop_tiles_per_worker` tile piantate
correnti, oltre al target di riempimento per quadrante già esistente
(`crop_target_fill_ratio`, invariato). Non cambia dove si pianta, solo
quante nuove semine vengono offerte per chiamata quando la capacità è
già impegnata da tile in servizio.

### 2.4 Telemetria economica giornaliera (`telemetry_snapshot()["daily_log"]`)

Nuovo log per-giorno: `harvest`, `water`, `dig`, `feed`, `move`, `pass`,
`sold_units`, `residual_sellable_inventory`, `serviced_crop_tiles`,
`backlog`, `hands`, `money`. Registrato al rollover di ogni giornata; il
giorno in corso (non ancora chiuso) resta disponibile separatamente come
`current_day_partial`.

### 2.5 Cosa NON è cambiato

Layer 1-3 (snapshot D4-D8, classificatore, selettore sticky) invariati
byte-per-byte da V1, nessun nuovo campo di snapshot, nessun terzo regime.
Il lifecycle colturale KEEP/HARVEST/DIG (Sezione 2.4 di MODEL_SPEC V1,
verificato contro il motore ufficiale) resta identico: cosa deciso non
cambia, solo quanta NUOVA superficie viene offerta.

---

## 3. Verifica diretta sui seed di diagnosi

| | V1 | V2 |
|---|---:|---:|
| Seed `180903003` (collasso), denaro finale | 138 | 568 |

Miglioramento reale (4×) ma non risolutivo da solo: la matrice di
sviluppo completa (Sezione successiva, nel report) è il giudizio, non
questo singolo seed — stesso principio già imparato nel ciclo E17
V4→V5→V6 (un caso riparato non implica generalizzazione).

---

## 4. Gate e stato del benchmark

Eseguito secondo il protocollo del prompt di remediation: 7 seed
development E18 (`180903001`-`180903007`), entrambi i seat, contro i tre
avversari congelati Codex E18.1, Copilot E18.1 e Antigravity E17
(obsoleto) — non più contro Claude V3/Copilot Native usati in V1.
Risultati completi, quattro verdetti separati (`TECHNICAL`, `SAFETY`,
`DYNAMIC`, `ECONOMIC`) e decisione finale in
`docs/model_specs/claude/e18/reports/E18_CLAUDE_OPPONENT_REACTIVE_V2_DEVELOPMENT_REPORT_IT.md`.

---

## 5. Vincoli invariati

Identici a V1: nessun import da `agricola.strategy.codex`,
`agricola.strategy.antigravity` o `agricola.strategy.copilot`; nessuna
tabella di azioni indicizzata per step; snapshot dell'avversario limitato
a `observation["farms"][opponent_seat]` pubblico, mai `private`, mai
nome/rating/replay ID/seed/memoria cross-episodio. Codex E18.1, Copilot
E18.1 e Antigravity E17 affrontati solo come avversari black-box tramite
le rispettive factory pubbliche. Nessun seed holdout o final-confirmation
consumato; nessuna modifica al manifest comune; nessuna submission
Kaggle.
