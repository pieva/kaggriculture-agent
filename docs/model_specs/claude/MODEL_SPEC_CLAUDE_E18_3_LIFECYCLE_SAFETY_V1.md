# MODEL_SPEC — Claude E18.3 Lifecycle-Safety V1

- **Policy ID:** `CLAUDE-E18.3-LIFECYCLE-SAFETY-V1`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-04
- **Foundation:** C2.1 (RECONCILED), esperimento E18
- **Predecessore:** `CLAUDE-E18.2-OPPONENT-REACTIVE-V2`
- **Sorgente:** `src/agricola/strategy/claude/e18_lifecycle_safety_v3.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_3_LIFECYCLE_SAFETY_V1.json`
- **Origine:** `docs/model_specs/claude/e18/prompts/E18_CLAUDE_LIFECYCLE_SAFETY_V3_BUILD_PROMPT_IT.md`

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
