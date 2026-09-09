# MODEL_SPEC — Claude E18.4 Capacity-Certified Growth V1

- **Policy ID:** `CLAUDE-E18.4-CAPACITY-CERTIFIED-V1`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-09
- **Foundation:** C2.1 (RECONCILED), esperimento E18
- **Predecessore:** `CLAUDE-E18.3-LIFECYCLE-SAFETY-V1`
- **Sorgente:** `src/agricola/strategy/claude/e18_capacity_certified_v4.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_4_CAPACITY_CERTIFIED_V1.json`
- **Test:** `docs/model_specs/claude/e18/tests/test_claude_e18_capacity_certified_v4.py`
- **Stato:** `PROPOSED / DEVELOPMENT`. Implementata e verificata a livello
  unitario e di regressione motore su un singolo seed (Sezione 8). **Non è
  stata eseguita** la matrice di sviluppo multi-seed (7 seed × 2 seat × N
  avversari) né alcun verdetto di gate economico o di sicurezza formale: non
  è una candidata promossa, è la nuova ipotesi preregistrata proposta per lo
  scongelamento della linea Claude (`FROZEN_PERFORMANCE_GAP` dal
  2026-09-04, vedi [README](README.md)). Nessuna submission Kaggle.

---

## 0. Provenienza e contesto

Questa versione nasce da una richiesta esplicita dell'utente in questa
sessione: leggere l'implementazione pubblica di Codex (MODEL_SPEC V48 770 e
i sorgenti pre-build che la realizzano) e proporre un'evoluzione della linea
Claude informata da quel confronto. È un'eccezione una tantum, autorizzata
esplicitamente per questa sessione, alla regola di governance normalmente
seguita da questa linea (Codex, Copilot e Antigravity vengono altrimenti
affrontati solo come avversari black-box tramite le rispettive factory
pubbliche, mai il sorgente); non cambia quella regola per i cicli di
sviluppo futuri non supervisionati.

Il confronto (riportato nella conversazione di questa sessione, non in un
documento separato) ha isolato un gap strutturale concreto nella linea
Claude V1-V3, distinto dalla causa residua già diagnosticata e non ancora
corretta (MODEL_SPEC V3 Sezione 5, abbinamento greedy dell'identità worker):
V1-V3 ammettono nuovi impegni di crescita con **soglie a rapporto statiche**
(`expansion_service_pressure_ceiling`, `max_serviceable_crop_tiles_per_worker`)
che non ragionano mai su quanti turni-lavoratore restano effettivamente
*questo giorno*. Il kernel di Codex
(`submission/submission_codex_e19_control_770_v2.py`, metodo
`_day_route_certificate`) e il suo override V48
(`docs/model_specs/codex/e19/tools/daily_routes_770_v48.py`, funzione
`pack_routes`) simulano invece gli obblighi residui della giornata contro il
budget di passi realmente residuo di ciascun worker prima di ammettere un
nuovo investimento, e lo rifiutano se la simulazione mostra che non
ci starebbe.

## 1. Obiettivo e ipotesi

**Obiettivo:** ridurre gli impegni di crescita (nuovo terreno, nuova
semina, nuovo animale) presi quando la manodopera attuale non ha più
margine temporale sufficiente nella giornata corrente per onorarli insieme
al carico critico già esistente (irrigazione urgente, alimentazione
animale) — la stessa classe di errore che l'audit V1→V2 aveva già
diagnosticato in forma più cruda (38 tile coltivate con 10-11 worker,
MOVE ≈ 3× le azioni produttive) e che V2 aveva mitigato solo con un tetto
statico per-worker, non con una verifica di budget giornaliero.

**Ipotesi centrale:** un singolo meccanismo aggiuntivo e isolato — un
gate booleano `growth_capacity_available`, calcolato una volta per
chiamata e usato per bloccare `BUY_LAND`, un nuovo `PLANT_OPPORTUNITY` e
`BUY_ANIMAL` — riduce la frequenza di sovra-impegno senza toccare nessun
altro meccanismo già verificato (dispatch, lifecycle, buffer di grano,
coda di emergenza), preservando così la disciplina di questa linea di non
combinare cause non isolate nella stessa versione.

**Ambito:** nessun seed di sviluppo o holdout è stato consumato in questa
revisione (Sezione 8). L'ipotesi non è stata ancora misurata su una
matrice di partite: la sua efficacia economica resta da verificare.

**Limiti dichiarati:**
- il gate è un'**approssimazione aggregata a livello di chiamata**, non
  una certificazione per-missione come quella di Codex: usa un costo
  medio configurabile per opportunità critica
  (`growth_capacity_average_service_cost_steps`, default 4,0 passi) invece
  di calcolare la distanza reale di ciascun worker da ciascuna
  opportunità. È un'approssimazione dichiarata, non un difetto nascosto;
- i valori di default (`average_service_cost_steps=4,0`,
  `safety_margin_steps_per_worker=2,0`) sono un'inizializzazione dello
  spazio di ricerca, non una soglia calibrata (cfr. README, "Una soglia
  osservata costituisce una inizializzazione del search space, non un
  valore ottimale");
- non risolve la causa residua di MODEL_SPEC V3 Sezione 5 (abbinamento
  worker non ottimale sotto affollamento): resta un lavoro futuro
  distinto, deliberatamente non bundlato qui.

## 2. Strategia

Il gate agisce come una precondizione aggiuntiva, non come una
ripianificazione: non cambia *come* si pianifica la produzione, la
manodopera o gli investimenti (Sezioni 8-10 di MODEL_SPEC V3, invariate),
cambia solo **quando** un nuovo impegno di crescita può essere ammesso.

**Meccanismo** (`_growth_capacity_available`, calcolato in
`_extract_features` subito dopo il ciclo principale sulle tile, prima
dell'emissione di `PLANT_OPPORTUNITY`):

```text
remaining_steps_today = turns_per_day - (current_step % turns_per_day)
available_budget       = worker_count * remaining_steps_today
critical_backlog       = count(opportunità con priority <= CRITICAL_PRIORITY_CEILING)
committed_cost          = critical_backlog * average_service_cost_steps
safety_margin           = worker_count * safety_margin_steps_per_worker

growth_capacity_available = (available_budget - committed_cost) >= safety_margin
```

`CRITICAL_PRIORITY_CEILING` (2) seleziona esattamente `URGENT_WATER` e
`FEED_NEEDED` — le due categorie che, se non servite, producono una
perdita irreversibile (WEED, fuga animale) al prossimo EOD. Il gate non
considera `HARVEST_READY`, `ROTATION_DIG`, `CARE_NEEDED`: quelle possono
attendere un ciclo senza perdita immediata.

**Dove è applicato (Sezione 3) e dove no (Sezione 3):** il gate protegge
solo i tre impegni che creano un nuovo obbligo di servizio ricorrente o
spendono cassa su espansione — `BUY_LAND`, nuova semina, nuovo animale.
`HIRE`, `BUY_SEED` e il buffer di grano restano esenti, per lo stesso
motivo per cui la coda di emergenza di V2 li esenta già: sono ciò che
*risolve* la pressione di capacità, non ciò che la contende.

**Orizzonte e condizioni di revisione:** invariati da V3 (Sezione 8 di
MODEL_SPEC V3) — nessuna pianificazione multi-partita, nessuna modifica
alla finestra di snapshot D4-D8 né alla sua sticky-ness.

## 3. Decisioni

**Cosa è gated dal nuovo meccanismo:**

| Ordine/opportunità | Gated da V4 | Motivazione |
|---|:---:|---|
| `BUY_LAND` (`_expansion_guard`) | **Sì** | Impegno di cassa più durevole (non scade mai); controllo aggiunto in testa alla funzione, sopra le condizioni V1-V3 invariate |
| `BUY_ANIMAL` (`_animal_orders`) | **Sì** | Un nuovo animale crea un obbligo FEED/CARE ricorrente immediato |
| Nuovo `PLANT_OPPORTUNITY` (`_extract_features`) | **Sì** | Impegna un turno-worker e crea un futuro obbligo `URGENT_WATER` |
| `HIRE` (`_hire_orders`) | **No** | Aumenta la capacità di domani, non la contende |
| `BUY_SEED` (`_seed_orders`) | **No** | Rifornisce solo l'inventario; non impegna un turno-worker né crea un obbligo di servizio da sola |
| `BUY_WHEAT` (`_wheat_stock_orders`) | **No** | Buffer di manutenzione per animali già esistenti, non nuova crescita |
| `SELL` | **No** | Non crea alcun obbligo futuro |

**Parametri nuovi e motivazione:**

| Parametro | Default | Motivazione |
|---|---:|---|
| `growth_capacity_average_service_cost_steps` | 4,0 | Costo medio stimato di un servizio critico (viaggio + eventuale prelievo + azione); coerente in ordine di grandezza con `_resolve_feed`/`_resolve_place_animal` |
| `growth_capacity_safety_margin_steps_per_worker` | 2,0 | Margine per worker oltre al backlog noto, per assorbire imprevisti (nuove tile che diventano `URGENT_WATER` nello stesso giorno) |

**Vincoli invariati:** identici a V1-V3 — nessun import da
`agricola.strategy.codex`, `agricola.strategy.antigravity` o
`agricola.strategy.copilot` nel sorgente eseguito a runtime; nessuna
tabella di azioni indicizzata per step; snapshot dell'avversario limitato
a `observation["farms"][opponent_seat]` pubblico. Il meccanismo è una
reimplementazione indipendente di un'idea osservata leggendo Codex in
questa sessione (Sezione 0), non codice importato o copiato.

## 4. Reazioni

Invariate da V3 (fallback tecnico `SAFE_PASS_ACTION`, stall-timeout
esteso a `PICKUP`, coda di emergenza zootecnica, chiusura di partita
`in_shutdown`/`in_liquidation`) — nessuna di queste reazioni è stata
toccata. Il nuovo gate aggiunge una sola reazione: quando
`growth_capacity_available` è `False`, la crescita viene semplicemente
**rimandata alla chiamata successiva**, non annullata né sostituita da
un'azione alternativa; il worker che non riceve un nuovo impegno di
crescita ricade sulla coda di opportunità di servizio esistente o
sull'idle/deposit (`_idle_or_deposit`), esattamente come in V3.

## 5. Coerenza con la Foundation

Il meccanismo non introduce alcun nuovo fatto di dominio: usa solo
grandezze già presenti nel Feature Model (`TMP-01` `step`, `TMP-04`
`turnsPerDay`, il conteggio dei worker) e la classificazione di priorità
già propria di questa linea (non un concetto della Foundation). Non
tocca `crop_harvest_readiness`, `animal_escape_condition` o alcun altro
concetto `ENGINE_VERIFIED`/`DERIVED_ENGINE_FACT` verificato nella
revisione precedente (MODEL_SPEC E18.3, Sezione 11). Resta valida la
discrepanza già segnalata in quella sezione (duplicazione locale di
`CROPS`/`ANIMALS` invece di lettura dinamica dalla configurazione
dell'engine): non corretta in questa revisione, invariata da V3.

**Nessuna nuova discrepanza introdotta.** Il gate è un costrutto
`POLICY_CONTEXT` puro (una stima deliberativa di capacità futura,
categoria che l'ontologia colloca esplicitamente fra i concetti
`POLICY_DECLARED` come `reserved_serviceable_before_deadline`), non un
fatto d'ambiente.

## 6. Stato di realizzazione

**Implementato:**
- il gate `_growth_capacity_available` come funzione pura;
- il collegamento a `_expansion_guard` (BUY_LAND) e `_animal_orders`
  (BUY_ANIMAL);
- la soppressione della sola emissione di nuove opportunità
  `PLANT_OPPORTUNITY` in `_extract_features`;
- un contatore diagnostico `growth_capacity_denials` esposto in
  `telemetry_snapshot()`;
- tutti i meccanismi V1-V3 (snapshot, classificatore, selettore sticky,
  lifecycle colturale, identità worker, stall-timeout, buffer di grano,
  coda di emergenza), riportati byte-per-byte invariati.

**Non implementato / proposto per il futuro:**
- il matching a costo minimo per l'identità worker (causa residua di
  MODEL_SPEC V3 Sezione 5) — deliberatamente non bundlato in questa
  versione;
- una certificazione per-missione (distanza reale per worker, come in
  Codex) al posto dell'attuale stima aggregata a costo medio fisso;
- qualunque calibrazione dei due nuovi parametri: i default sono
  un'inizializzazione, non un valore verificato su partite.

**Non in ambito di questa revisione:** nessuna matrice di sviluppo
multi-seed, nessun verdetto di gate economico o di sicurezza, nessuna
submission Kaggle. Questa MODEL_SPEC descrive un'ipotesi implementata e
testata unitariamente, non una candidata promossa.

## 7. Verifica eseguita in questa revisione

Eseguiti realmente in questa sessione, con
`.venv/Scripts/python.exe -m pytest`:

- `docs/model_specs/claude/e18/tests/test_claude_e18_capacity_certified_v4.py`
  (esclusa la regressione motore): **24/24 PASS**.
- La stessa suite includendo la regressione motore a singolo seed
  (`test_v4_does_not_regress_the_worst_traced_v2_match`, seed `180903002`,
  seat 0 vs Copilot E18.2): **25/25 PASS** — `verified_livestock_losses == 0`,
  `technical_errors == 0`, invariato rispetto a V3 su questo match.
- L'intera directory `docs/model_specs/claude/e18/tests/` (V1+V2+V3+V4):
  **100/100 PASS** — nessuna regressione incrociata rilevata sui test
  esistenti delle versioni precedenti.

**Non eseguito:** la matrice di sviluppo a 7 seed × 2 seat richiesta dal
protocollo E18 per un verdetto di gate (Sezione 6); nessuna partita
economica è stata giocata oltre al singolo seed di regressione sopra.
Qualunque affermazione su un miglioramento delle prestazioni economiche
resta un'ipotesi non ancora misurata.

## 8. File di implementazione

| File | Ruolo | Parte della strategia implementata | Categoria |
|---|---|---|---|
| [e18_capacity_certified_v4.py](../../../src/agricola/strategy/claude/e18_capacity_certified_v4.py) | Controller a 5 livelli, identico a V3 tranne il nuovo gate `_growth_capacity_available` e i suoi tre punti di collegamento | Sezioni 1-6 | Runtime |
| [observation_contract.py](../../../src/agricola/core/observation_contract.py) | Parsing e normalizzazione policy-neutral dell'osservazione, condiviso e invariato | Ingresso dati | Runtime (condiviso) |
| [CLAUDE_E18_4_CAPACITY_CERTIFIED_V1.json](e18/configs/CLAUDE_E18_4_CAPACITY_CERTIFIED_V1.json) | Configurazione V3 invariata più la sezione `growth_capacity` (due nuovi parametri) | Tabella parametri Sezione 3 | Configurazione |
| [test_claude_e18_capacity_certified_v4.py](e18/tests/test_claude_e18_capacity_certified_v4.py) | Fixture di lifecycle/identità/stallo riprodotte da V3 (non regressione), fixture nuove per il gate e le sue esenzioni, regressione motore a singolo seed | Sezione 7 | Test |

**Builder/submission:** nessuno. Questa versione non ha un builder di
bundle né una submission: è un candidato di sviluppo, non un artefatto da
consegnare.

**Non incluso nella tabella perché invariato e già censito:** i vincoli,
le costanti di gioco (`CROPS`, `ANIMALS`) e la struttura a 5 livelli sono
gli stessi già documentati in
[MODEL_SPEC_CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.md](MODEL_SPEC_CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.md)
Sezione 13, a cui si rimanda per i dettagli non modificati da questa
versione.
