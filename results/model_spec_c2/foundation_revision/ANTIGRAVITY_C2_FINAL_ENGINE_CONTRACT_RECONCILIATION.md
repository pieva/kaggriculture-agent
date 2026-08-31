# C2 — ANTIGRAVITY FINAL ENGINE CONTRACT RECONCILIATION & FREEZE DECISION

```text
DOCUMENT_ID: ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION
PHASE: C2 — Foundation Revision / Final Engine Contract Reconciliation
AUTHOR: Antigravity
DATE: 2026-08-31
STATUS: FROZEN — FINAL DECISION
TARGET_ENVIRONMENT: kaggle-environments 1.32.7 (kaggriculture 0.1.0)
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
PROVENANCE_STATUS: INDEPENDENTLY_VERIFIED
RECONCILIATION_VERDICT: ENGINE_CONTRACT_FREEZE = YES
```

---

## 1. Executive Verdict

Antigravity ha completato la **reconciliation finale e la chiusura formale dell'Engine Contract C2** di Kaggriculture, operando come autorità di riconciliazione tra l'audit di baseline prodotto da Codex, la review indipendente di Antigravity, la review indipendente di Copilot, la correzione di provenance `AGG-01` e la successiva reverification indipendente di Copilot.

### Verdetto Principale:
```text
================================================================================
ENGINE_CONTRACT_FREEZE: YES
================================================================================
```

### Sintesi delle determinazioni normative:
1. **Engine Identity e Provenance Chiusa:** L'identità dell'engine è formalmente congelata sull'ambiente `kaggle-environments` 1.32.7 (`kaggriculture` 0.1.0) con fingerprint SHA-256 aggregato canonico `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d`. Il rilievo `AGG-01` è formalmente **RESOLVED** ed è stato verificato in modo indipendente e riproducibile da tutti e tre i reviewer.
2. **Nessun Conflitto Semantico Residuo:** La convergenza cross-review sui fatti di dominio è del **100%**: tutti i quattro P0 identificati (`CLK-01`, `ANI-01`, `FER-01`, `INV-01`) e le restanti discrepanze (`ANI-02`, `FER-02`, `INV-02`, `SVC-01`, `CAP-01`, `OBS-01`, `HAR-01`, `SPC-01`, `PER-01`) sono risolti a livello di contratto sorgente e concordati all'unanimità.
3. **Separazione Fatti di Dominio / Policy:** Il contratto stabilisce la netta separazione tra regole normative dell'engine (`ENGINE_FACT`), derivazioni esatte (`DERIVED_ENGINE_FACT`), contesto di deliberazione strategica (`POLICY_CONTEXT`) e metriche di valutazione a posteriori (`POST_HOC_METRIC`).
4. **Pronto per la Revisione dell'Ontologia:** L'Engine Contract è congelato e funge da base immutabile per la successiva riscrittura di `docs/model/ontology/ONTOLOGY_C2.md`.

---

## 2. Scope e Non-Scope

### In-Scope (Riconciliato e Congelato):
- **Engine Contract & Period Ledger:** Norme di transizione dello stato, biologia delle colture e degli animali, meccanica dei fertilizzanti, gestione dell'inventario e dello shed, ordine atomico delle fasi di step.
- **Clock & Temporal Semantics:** Parametrizzazione di `turnsPerDay`, contatore `step`, invarianti orari e di giornata, semantica dell'End-of-Day (EOD).
- **Species Inventory:** Insieme chiuso delle specie vegetali e animali supportate; determinazione definitiva di `CHICKEN = NOT_SUPPORTED` e `GOOSE = SUPPORTED`.
- **Serviceability Taxonomy:** Tripartizione formale (`ACTION_ELIGIBLE_NOW`, `RESERVED_SERVICEABLE_BEFORE_DEADLINE`, `REALIZED_SERVICEABLE_IN_WINDOW`).
- **Discrepancy Matrix & Provenance:** Chiusura delle 13 discrepanze Foundation e del rilievo di aggregazione `AGG-01`.

### Non-Scope (Escluso in modo vincolante da questa fase):
- **Nessuna modifica al codice sorgente:** Nessun file in `src/` o `tests/` o `.venv/` è modificato.
- **Nessuna revisione di MODEL_SPEC:** Nessuna strategia di gioco, mix colturale o parametrizzazione di agenti è definita o alterata.
- **Nessuna modifica anticipata ai layer Foundation downstream:** `ONTOLOGY_C2.md`, `KAGGRICULTURE_STATE_MACHINE_C2.md` e `KAGGRICULTURE_FEATURE_MODEL_C2.md` non vengono modificati in questo task.
- **Nessun Tournament o benchmark:** Nessuna esecuzione competitiva o validazione prestazionale.
- **Nessuna submission Kaggle:** Nessun caricamento o packaging per la competizione.
- **Nessuna assunzione di Policy come Engine Fact:** Scelte di routing, allocazione della manodopera, espansione territoriale o soglie di riserva monetaria rimangono prerogative esclusive dei controller strategici.

---

## 3. Evidence Set e Provenance

La reconciliation si basa sul set completo e verificato dei seguenti artefatti:

| Artefatto | Ruolo nel Workflow | Autore / Fonte | SHA-256 / Stato | Utilizzo nella Reconciliation |
|---|---|---|---|---|
| [`CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md) | Baseline Semantica Primaria | Codex | `READY_FOR_REVIEW` (Aggiornato post AGG-01) | Baseline normativa dell'Engine Contract, della tassonomia e della matrice delle discrepanze. |
| [`ANTIGRAVITY_C2_ENGINE_CONTRACT_REVIEW.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_ENGINE_CONTRACT_REVIEW.md) | Independent Review 1 | Antigravity | `SEMANTIC_PASS` | Conferma forense riga per riga di tutti i fatti engine e delle risposte alle 18 domande di controllo. |
| [`COPILOT_C2_ENGINE_CONTRACT_INDEPENDENT_REVIEW.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/COPILOT_C2_ENGINE_CONTRACT_INDEPENDENT_REVIEW.md) | Independent Review 2 | Copilot | `ACCEPT_WITH_CORRECTIONS` | Conferma semantica completa; apertura formale del rilievo `AGG-01` su riproducibilità fingerprint. |
| [`CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md) | Risoluzione Provenance | Codex | `RESOLVED` | Esplicitazione della specifica di serializzazione a 702 byte e comando riproducibile. |
| [`COPILOT_C2_AGG_01_REVERIFICATION.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/COPILOT_C2_AGG_01_REVERIFICATION.md) | Reverification Indipendente | Copilot | `RESOLVED` | Validazione indipendente dell'hash canonico `4378b60f...` con esito positivo al 100%. |
| `kaggriculture.py` (runtime) | Fonte Primaria Normativa | `kaggle-environments` | `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e` | Codice dell'ambiente eseguibile nel venv locale. |
| `kaggriculture.json` (runtime) | Config / Schema Primario | `kaggle-environments` | `a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867` | Schema di configurazione parametri (default `turnsPerDay=24`, `episodeSteps=720`). |
| [`PROJECT_STATE.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/PROJECT_STATE.md) | Registro di Stato di Progetto | Governance | `C2 Foundation Revision` | Verifica di autorizzazioni, gate procedurali e vincoli metodologici. |

---

## 4. Baseline Authority

In conformità alla regola di riconciliazione **R1**, l'artefatto [`CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md) viene formalmente mantenuto e congelato come **baseline primaria normativa**.

### Rationale:
1. **Integrità Semantica:** Entrambe le review indipendenti (Antigravity e Copilot) hanno validato la totalità delle ricostruzioni semantiche fornite da Codex (clock, biologia, fertilizzante, overflow, transizioni di stato).
2. **Conservazione della Tassonomia:** Gli identificatori di discrepanza (`CLK-01`, `ANI-01`, etc.) e la classificazione di severità stabilita da Codex riflettono fedelmente l'impatto causale sull'ambiente e vengono preservati integralmente senza alterazioni spurie.
3. **Risoluzione Puntuale di `AGG-01`:** L'unica contestazione emersa (la riproducibilità del fingerprint sollevata da Copilot) ha riguardato la sotto-specificazione della serializzazione del manifest e non il codice sorgente dell'engine. Tale rilievo è stato corretto in [`CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md) e riverificato in [`COPILOT_C2_AGG_01_REVERIFICATION.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/model_spec_c2/foundation_revision/COPILOT_C2_AGG_01_REVERIFICATION.md) confermando l'hash originale `4378b60f...` senza rendere necessaria alcuna riapertura dell'audit di dominio.

---

## 5. Cross-Review Reconciliation Matrix

La tabella seguente riconcilia in modo esaustivo ogni discrepanza e area di analisi confrontando la baseline Codex con le valutazioni indipendenti di Antigravity e Copilot:

| ID / Topic | Codex Baseline | Antigravity Finding | Copilot Finding | Impatto AGG-01 | Classificazione Finale | Disposizione Finale (Reconciliation Decision) |
|---|---|---|---|---|:---:|---|
| **CLK-01** (Clock & Periodi Step) | P0: `turnsPerDay` parametrico; `step == day*T + hour`; periodi fissi in step rifiutati | Confermato (P0) | Confermato (P0) | Nessuno | `NO_CONFLICT` | **ACCETTATO**: clock engine ancorato a `day` e `hour`; formule biologiche espresse in funzione di `turnsPerDay`. |
| **ANI-01** (Base Animal Output vs FEED) | P0: Base output = 1 a schedule se non scappato; FEED non è gate del base yield | Confermato (P0) | Confermato (P0) | Nessuno | `NO_CONFLICT` | **ACCETTATO**: base yield dissociato da FEED giornaliero; FEED previene fuga e abilita consumo care bonus. |
| **ANI-02** (Care Bonus Semantics) | P1: Bonus additivo `pending_care_bonus`, differito, consumato solo se fed | Confermato (P1) | Confermato (P1) | Nessuno | `NO_CONFLICT` | **ACCETTATO**: bonus cura additivo, accumulato su fed+cared e consumato al successivo evento di produzione fed. |
| **FER-01** (Fertilizer Uplift) | P0: Incremento totale $=2$, base $=1$, uplift netto $= +1$ (non $+2$) | Confermato (P0) | Confermato (P0) | Nessuno | `NO_CONFLICT` | **ACCETTATO**: resa fertilizzata $=2$ per irrigazione/evento, uplift quantificato a $+1$ rispetto al base. |
| **FER-02** (Finestra Fertilizer) | P2: Durata 3 giorni inclusivi (`d .. d+2`); boolean saturation su animale | Confermato (P1 / Severity nuance) | Confermato | Nessuno | `CLASSIFICATION_VARIATION` | **ACCETTATO**: finestra temporale `current_day .. current_day+2`; flag animale boolean (non cumulativo). Conservata severity Codex P2. |
| **INV-01** (Shed Overflow & DROP) | P0: Manual `DROP` ed EOD scartano eccedenza oltre room; `PLACE` conserva residuo | Confermato (P0) | Confermato (P0) | Nessuno | `NO_CONFLICT` | **ACCETTATO**: manual DROP ed EOD auto-drop sono distruttivi dell'overflow; `PLACE` conserva il residuo nell'inventario del lavoratore. |
| **INV-02** (PLACE Capacity Awareness) | P3: Mappatura stale `contract_inventory_loss` da armonizzare con semantica PLACE | Confermato (P2 / Naming) | Confermato | Nessuno | `CLASSIFICATION_VARIATION` | **ACCETTATO**: rinominazione canonica in `shed_overflow_loss` distinta per cause `MANUAL_DROP` e `EOD_AUTO_DROP`. Conservata baseline. |
| **SVC-01** (Serviceability Definition) | P1: Distinzione netta tra guardie engine (fatto) e garanzia futura di piano (policy) | Confermato (P1) | Confermato (P1) | Nessuno | `NO_CONFLICT` | **ACCETTATO**: adozione formale della tripartizione della serviceability. |
| **CAP-01** (Capacity Definition) | P1: Capacità come upper bound multi-dimensionale incompleto, non scalare garantito | Confermato (P1) | Confermato (P1) | Nessuno | `NO_CONFLICT` | **ACCETTATO**: rifiuto del conteggio scalare rigido; inclusione di percorsi, inventari, precedenze e turni. |
| **OBS-01** (State Alignment & Actions) | P1: Allineamento $S_t \to A_t \to S_{t+1}$; richieste vs esecuzioni effettive | Confermato (P2 / Timing) | Confermato | Nessuno | `CLASSIFICATION_VARIATION` | **ACCETTATO**: separazione netta tra request online, esecuzione verificata e telemetry post-hoc. Conservata severity Codex P1. |
| **HAR-01** (Early Harvest Behavior) | P1: Early harvest su coltura immatura è silent no-op (nessuna distruzione pianta) | Confermato (P2 / Nuance) | Confermato | Nessuno | `CLASSIFICATION_VARIATION` | **ACCETTATO**: harvest immaturo è no-op silenzioso; danno limitato allo slot azione sprecato. Conservata severity Codex P1. |
| **SPC-01** (Species Inventory Closed Set) | P2: `CHICKEN = NOT_SUPPORTED`; `GOOSE` presente in `ANIMALS` (struttura `COOP`) | Confermato (P1 / Species) | Confermato | Nessuno | `CLASSIFICATION_VARIATION` | **ACCETTATO**: congelamento dell'inventario a 5 crop e 3 animali; `CHICKEN` rimosso formalmente. Conservata baseline. |
| **PER-01** (Period Ledger Parametrico) | P2: Formule origin-relative parametriche in $T$, indipendenti da policy di raccolta | Confermato (P1 / Foundation) | Confermato | Nessuno | `CLASSIFICATION_VARIATION` | **ACCETTATO**: adozione del Period Ledger canonico parametrizzato in $T$. Conservata baseline Codex. |
| **AGG-01** (Aggregate Fingerprint Provenance) | Baseline originaria sotto-specificata; hash $4378...$ corretto | Validato $4378...$ | Contestato $1c58...$ (P3) | Risolto via specifica 702 byte | `RESOLVED_BY_AGG_01` | **ACCETTATO & RISOLTO**: specifica di serializzazione formalizzata a 702 byte; hash canonico $4378...$ confermato da Copilot in re-verification. |

---

## 6. Canonical Engine Contract (Congelato)

Si formalizza di seguito il **contratto normativo completo e non ridotto** dell'Engine Kaggriculture.

### 6.1 Clock Contract & Invarianti Temporali
Sia $T = \text{turnsPerDay}$ (parametro configurabile in `kaggriculture.json`, default $T = 24$).
- **Contatore Infra-Day:** Lo stato engine espone `step` come intero 0-indexed ($0 \le \text{step} < \text{episodeSteps}$).
- **Relazione Canonica di Stato Valido:**
  $$\text{day} = \lfloor \text{step} / T \rfloor, \quad \text{hour} = \text{step} \bmod T$$
  $$\text{step} \equiv \text{day} \cdot T + \text{hour}$$
- **Transizione EOD (End-of-Day):** L'EOD scatta atomicamente al termine dello step che soddisfa:
  $$(\text{step} + 1) \bmod T == 0$$
- **Step di Azione EOD:** L'ultimo step infra-day disponibile per azioni nel giorno $d$ è:
  $$\text{EOD\_STEP}(d) = (d + 1) \cdot T - 1$$
- **Aggiornamento Next State:** All'EOD, il next state incrementa $\text{day} \to d + 1$ e resetta $\text{hour} \to 0$. I flag giornalieri (`watered_today`, `fed_today`, `cared_today`) vengono azzerati dopo la fase di refresh.

### 6.2 Ordine Atomico delle Transizioni (Step Execution Pipeline)
Per ogni step $t$, l'interpreter esegue rigorosamente la seguente sequenza:
1. **Validazione Atomica Semi (PLANT Demands):** Per ciascun giocatore, se la domanda aggregata di semi per una data specie supera la disponibilità privata, **tutte** le richieste di semina di quella specie per quel giocatore nello step falliscono (silent no-op).
2. **Esecuzione Azione Farmer:** Applicazione dell'azione dell'unità Farmer (Worker 0).
3. **Esecuzione Seriale Farm Hands:** Applicazione in ordine sequenziale delle azioni dei lavoratori subordinati (Hands 1..N). I lavoratori successivi osservano immediatamente le mutazioni di stato (es. tile occupate, inventari) prodotte dai lavoratori precedenti nello stesso step.
4. **Regolazione Ordini di Mercato (Market Phase):** Esecuzione in lockstep di acquisti/vendite e contratti di lavoro (`HIRE`). Limite massimo configurabile di ordini per turno: 10.
5. **Consumo Cittadino (`_town_consume`):** Aggiornamento della domanda locale di mercato.
6. **Decadimento Piante (`_decay_plants`):** Applicazione del decadimento naturale per piante che hanno superato il `max_lifespan_step`.
7. **Fase EOD (se step di fine giornata):**
   - Refresh biologico piante (`_daily_refresh_plants`);
   - Refresh biologico animali ed evasione fughe (`_daily_refresh_animals`);
   - Spawn casuale erbacce (`WEED`) su caselle `None` sbloccate;
   - Scarico automatico inventari lavoratori nello shed (`_drop_inventories_to_shed`);
   - Rimozione totale della forza lavoro subordinata (gli Hands hanno contratto giornaliero e scadono a EOD);
   - Reset prezzi e stock negozio.
8. **Assegnazione Stato Finale / Reward:** Controllo condizioni terminali a `episodeSteps` (default 720) e calcolo liquidità finale.

### 6.3 Species Inventory & Strutture
L'insieme delle entità biologiche e delle strutture supportate è rigorosamente chiuso:

```text
CROPS    = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}
ANIMALS  = {"GOOSE": structure "COOP", product "EGG", cost 300, max_held 4},
            "COW":   structure "PASTURE", product "MILK", cost 400, max_held 6},
            "SHEEP": structure "PASTURE", product "WOOL", cost 500, max_held 6}}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]

CHICKEN  = NOT_SUPPORTED (assente dall'engine)
```

### 6.4 Crop Biology & Period Ledger
Per una pianta seminata al giorno $d_0 = \text{planted\_day}$:
- **Stato Iniziale alla Semina:** `consecutive_unwatered = 1`, `watered_today = False`, `fertilized_until_day = -1`. Resa iniziale $=1$ per non-ongoing, $=0$ per ongoing.
- **Fabbisogno Idrico di Sopravvivenza:** Una `WATER` riuscita imposta `watered_today = True`. All'EOD, se `watered_today == True` il contatore `consecutive_unwatered` si azzera; se `False`, si incrementa di 1. Se `consecutive_unwatered >= 2`, la pianta muore e si trasforma irreversibilmente in `WEED`.
- **Incremento di Resa Non-Ongoing:** La prima irrigazione giornaliera effettuata nelle età comprese tra $\lfloor ( \text{max\_yield\_day} + 1 ) / 2 \rfloor$ e $\text{max\_yield\_day}$ incrementa la resa di $+1$ (oppure $+2$ se concimata con fertilizzante attivo), fino al cap $\text{max\_yield}$.
- **Incremento di Resa Ongoing:** All'EOD, se la pianta sopravvive e $\text{next\_day} - d_0 - \text{first\_yield\_day}$ è un multiplo non-negativo dell'intervallo, la resa aumenta di $+1$ (oppure $+2$ se la pianta è stata sia irrigata sia concimata quel giorno), fino al cap $\text{max\_yield}$, per un massimo di 4 eventi schedulati.
- **Raccolta (`HARVEST`):** Legale solo se $\text{current\_day} - d_0 \ge \text{first\_yield\_day}$ e $\text{yield\_units} > 0$. Trasferisce l'intera resa nell'inventario del lavoratore. Le colture non-ongoing tornano `None` (suolo libero); le ongoing azzerano la resa a 0 e mantengono la pianta attiva. Tentativi di raccolta precoce o su resa zero sono silent no-op.
- **Lifespan Decay:** A partire dallo step $\text{max\_lifespan\_step}$, la resa della pianta cala di 1 unità ogni 2 step. Raggiunto yield $\le 0$, la pianta si trasforma in `WEED`. L'azione di `HARVEST` eseguita nello step $\text{max\_lifespan\_step}$ precede il decay di quello step e salva la resa intatta.

### 6.5 Animal Biology, FEED, CARE & Fuga
Per un animale collocato al giorno $d_0 = \text{placed\_day}$:
- **Stato Iniziale al Piazzamento:** `yield_units = 0`, `consecutive_unfed = 0`, `fed_today = False`, `cared_today = False`, `fertilizer_available = False`, `pending_care_bonus = 0`.
- **Evasione Fuga all'EOD:** Se `fed_today == True`, `consecutive_unfed` viene azzerato; se `False`, viene incrementato di 1. **Se `consecutive_unfed >= 2`, l'animale scappa**: la casella regredisce alla struttura vuota e non avviene alcuna produzione o generazione di fertilizzante.
- **Produzione Base (Disaccoppiata da FEED):** Se l'animale **non è scappato** (`consecutive_unfed <= 1`) ed è un giorno programmato di produzione ($\text{next\_day} - d_0 \ge \text{first\_output\_day}$ e multiplo dell'intervallo):
  $$\text{base\_output} = 1$$
  L'output base $=1$ viene erogato anche se `fed_today == False`, purché l'animale non sia fuggito.
- **Bonus Cura (`CARE`):**
  - Se nel giorno di produzione `fed_today == True`, l'animale consuma il `pending_care_bonus` precedentemente accumulato: $\text{yield\_units} = \min(\text{max\_held}, \text{yield\_units} + \text{base} + \text{pending\_care\_bonus})$, e il pending bonus si azzera.
  - Al termine della fase di produzione, se $\text{cared\_today} \land \text{fed\_today} == \text{True}$, l'animale incrementa `pending_care_bonus += 1` per le produzioni future. `CARE` senza `FEED` non produce accumulo di bonus.
- **Generazione Fertilizzante:** Ogni animale sopravvissuto al controllo fuga imposta `fertilizer_available = True` a EOD, indipendentemente da alimentazione, cura o produzione. Il flag è un booleano (non cumulabile oltre 1 unità non raccolta).

### 6.6 Meccanica del Fertilizzante
- **Raccolta:** L'azione `COLLECT_FERTILIZER` su un animale con `fertilizer_available == True` preleva esattamente 1 unità di `FERTILIZER` nel worker inventory e azzera il flag a `False`.
- **Applicazione (`FERTILIZE`):** Consuma 1 unità di `FERTILIZER` dall'inventario del lavoratore su una tile `PLANT`.
- **Finestra di Efficacia:** Imposta `fertilized_until_day = max(fertilized_until_day, current_day + 2)`, coprendo 3 giorni inclusivi (`current_day`, `current_day + 1`, `current_day + 2`).
- **Effetto Quantitativo:**
  $$\text{BASE\_INCREMENT\_TOTAL} = 1, \quad \text{FERTILIZED\_INCREMENT\_TOTAL} = 2 \implies \text{FERTILIZER\_UPLIFT} = +1$$
  Il fertilizzante non accelera il clock biologico (`age`), non altera i vincoli di maturità legale e non supera il cap di resa massimo della specie.

### 6.7 Meccanica di Inventario e Perdite Shed Overflow
- **Capacità Shed:** Fissata da configurazione (default 100 unità aggregate).
- **Azione Manuale `DROP`:** Se il lavoratore esegue `DROP` adiacente allo shed, lo shed assorbe $\text{take} = \min(n, \text{room})$. **L'intera eccedenza residua ($n - \text{take}$) viene cancellata e persa irreversibilmente.**
- **Auto-Drop EOD:** Al termine della giornata, l'engine esegue un drop automatico con la stessa logica distruttiva: i prodotti che eccedono la capacità residua dello shed vengono scartati.
- **Azione `PLACE` nello Shed:** Se il lavoratore esegue `PLACE` verso lo shed, vengono trasferite solo le unità che entrano ($\min(n, \text{room})$); **il residuo eccedente rimane intatto nell'inventario del lavoratore.**

### 6.8 Tabella Period Ledger Canonica (v1 - Congelata)

| ENTITY | TYPE | BIOLOGICAL_EVENT | PERIOD_DAYS | FORMULA / SCHEDULE | FIRST_EVENT | WINDOW_OPEN | WINDOW_CLOSE | HARD_DEADLINE | ENGINE_SOURCE | STATUS |
|---|---|---|:---:|---|:---:|:---:|:---:|---|---|:---:|
| **WHEAT** | Crop | Resa da WATER | 1 (in finestra) | 1 WATER/giorno, età 2..4 | $d_0 + 2$ | Età 2 | Età 4 | EOD giornaliero (fuga a 2 miss) | `kaggriculture.py` L420-430 | `ENGINE_VERIFIED` |
| **WHEAT** | Crop | Harvest / Lifespan | Non-periodico | Età $\ge 2$, Yield $> 0$; MLS=$(d_0+5)T$ | $d_0 + 2$ | Età 2 | Dinamica fino a WEED | Step MLS (pre-decay) | `kaggriculture.py` L445, L760 | `ENGINE_VERIFIED` |
| **CARROT** | Crop | Resa da WATER | 1 (in finestra) | 1 WATER/giorno, età 2..3 | $d_0 + 2$ | Età 2 | Età 3 | EOD giornaliero (fuga a 2 miss) | `kaggriculture.py` L420-430 | `ENGINE_VERIFIED` |
| **CARROT** | Crop | Harvest / Lifespan | Non-periodico | Età $\ge 2$, Yield $> 0$; MLS=$(d_0+4)T$ | $d_0 + 2$ | Età 2 | Dinamica fino a WEED | Step MLS (pre-decay) | `kaggriculture.py` L445, L760 | `ENGINE_VERIFIED` |
| **MELON** | Crop | Resa da WATER | 1 (in finestra) | 1 WATER/giorno, età 6..12 | $d_0 + 6$ | Età 6 | Età 12 | EOD giornaliero (fuga a 2 miss) | `kaggriculture.py` L420-430 | `ENGINE_VERIFIED` |
| **MELON** | Crop | Harvest / Lifespan | Non-periodico | Età $\ge 10$, Yield $> 0$; MLS=$(d_0+13)T$ | $d_0 + 10$ | Età 10 | Dinamica fino a WEED | Step MLS (pre-decay) | `kaggriculture.py` L445, L760 | `ENGINE_VERIFIED` |
| **TOMATO** | Crop | Incremento Schedulato | 1 | Evento a $d_0 + 8 + k$, $k=0..3$ | $d_0 + 8$ | Post-EOD Event | Quarto evento $d_0+11$ | Sopravvivenza a ogni EOD; MLS=$(d_0+12)T$ | `kaggriculture.py` L435-442 | `ENGINE_VERIFIED` |
| **TOMATO** | Crop | Harvest Ripetibile | Opportunità | Età $\ge 8$, Yield $> 0$ | $d_0 + 8$ | Primo yield $>0$ | Dinamica (4 max yield) | Step MLS (pre-decay) | `kaggriculture.py` L445-455 | `ENGINE_VERIFIED` |
| **STRAWBERRY** | Crop | Incremento Schedulato | 2 | Evento a $d_0 + 10 + 2k$, $k=0..3$ | $d_0 + 10$ | Post-EOD Event | Quarto evento $d_0+16$ | Sopravvivenza a ogni EOD; MLS=$(d_0+17)T$ | `kaggriculture.py` L435-442 | `ENGINE_VERIFIED` |
| **STRAWBERRY** | Crop | Harvest Ripetibile | Opportunità | Età $\ge 10$, Yield $> 0$ | $d_0 + 10$ | Primo yield $>0$ | Dinamica (4 max yield) | Step MLS (pre-decay) | `kaggriculture.py` L445-455 | `ENGINE_VERIFIED` |
| **GOOSE** | Animal | Produzione Uova (`EGG`) | 1 | Evento a $d_0 + 4 + k$, $k \ge 0$ | $d_0 + 4$ | Post-EOD yield $>0$ | Illimitata (Cap 4) | Secondo EOD unfed (fuga pre-evento) | `kaggriculture.py` L470-482 | `ENGINE_VERIFIED` |
| **COW** | Animal | Produzione Latte (`MILK`) | 2 | Evento a $d_0 + 8 + 2k$, $k \ge 0$ | $d_0 + 8$ | Post-EOD yield $>0$ | Illimitata (Cap 6) | Secondo EOD unfed (fuga pre-evento) | `kaggriculture.py` L470-482 | `ENGINE_VERIFIED` |
| **SHEEP** | Animal | Produzione Lana (`WOOL`) | 3 | Evento a $d_0 + 6 + 3k$, $k \ge 0$ | $d_0 + 6$ | Post-EOD yield $>0$ | Illimitata (Cap 6) | Secondo EOD unfed (fuga pre-evento) | `kaggriculture.py` L470-482 | `ENGINE_VERIFIED` |
| **ALL ANIMALS** | Animal | Fertilizzante Disponibile | 1 | Ogni EOD sopravvissuto | $d_0 + 1$ | Post-EOD giorno succ. | Fino a raccolta/fuga | Raccolta prima di successivo EOD | `kaggriculture.py` L480-482 | `ENGINE_VERIFIED` |

---

## 7. Fingerprint Reconciliation & Provenance Verification

Il controllo di integrità dell'ambiente è stato eseguito applicando la specifica canonica rigorosa a 702 byte.

### 7.1 Specifiche del Manifest e Payload Canonico
```text
PATH_ROOT: Repository workspace root
PATH_SEPARATOR: /
PATH_CASE: As listed in canonical manifest
SORT_ORDER: Unicode code-point ascending (case-sensitive)
FILE_HASH: SHA-256 su raw bytes (lowercase hex)
RECORD_FORMAT: normalized_path + '\t' + file_sha256
TEXT_ENCODING: UTF-8 (No BOM)
RECORD_SEPARATOR: LF (0x0A)
TRAILING_NEWLINE: NO
PAYLOAD_LENGTH: 702 bytes
```

### 7.2 Manifest e Hash dei Singoli File
```text
.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA	5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md	e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md	3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json	a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py	bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
```

### 7.3 Esito Verifica Eseguibile Indipendente
Comando eseguito nel runtime locale:
```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; import hashlib; ps=[Path(x) for x in ('.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA','.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md','.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md','.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json','.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py')]; es=sorted(((p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()) for p in ps),key=lambda x:x[0]); rows=[p+'\t'+h for p,h in es]; payload='\n'.join(rows).encode('utf-8'); print('\n'.join(rows)); print('AGGREGATE_SHA256='+hashlib.sha256(payload).hexdigest())"
```

Risultato osservato:
```text
EXPECTED_AGGREGATE_SHA256: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
OBSERVED_AGGREGATE_SHA256: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
FINGERPRINT_MATCH: YES
AGG_01_STATUS: RESOLVED
INDEPENDENT_REVERIFICATION_COPILOT: YES (Pass)
INDEPENDENT_REVERIFICATION_ANTIGRAVITY: YES (Pass)
```

---

## 8. Residual Discrepancy Assessment

Valutazione formale delle discrepanze residue:

```text
BLOCKING_DISCREPANCIES: 0 (NONE)
NON_BLOCKING_SEMANTIC_GAPS: 0 (NONE)
PROVENANCE_BLOCKERS: 0 (NONE)
UNRESOLVED_DISCREPANCIES: NONE
```

Tutte le 13 discrepanze e il rilievo di provenance `AGG-01` sono completamente risolti. Nessun ostacolo impedisce il congelamento dell'Engine Contract.

---

## 9. Foundation Implications (Linee Guida per i Task Successivi)

Le seguenti direttive vincolanti dovranno essere applicate, **esclusivamente nel task successivo autorizzato**, alla documentazione Foundation (senza modificare nulla in questo task):

### 1. Per `docs/model/ontology/ONTOLOGY_C2.md`:
- Aggiornare l'inventario biologico: formalizzare `GOOSE` (struttura `COOP`, prodotto `EGG`), dichiarare `CHICKEN = NOT_SUPPORTED`.
- Riformulare la semantica di `FEED`: definire `FEED` come misura anti-evasione e abilitatore del consumo del care bonus, dissociandolo dal base output schedulato.
- Correggere la resa del fertilizzante: stabilire $\text{base} = 1$, $\text{fertilized} = 2$, $\text{uplift} = +1$.
- Correggere la perdita di inventario: rinominare e classificare `shed_overflow_loss` per cause `MANUAL_DROP` ed `EOD_AUTO_DROP`, documentando che `PLACE` preserva il residuo nel worker.
- Introdurre formalmente la tripartizione della serviceability.

### 2. Per `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`:
- Correggere la transizione biologica animale: emettere l'evento di produzione base se $\text{consecutive\_unfed} < 2$, indipendentemente da `fed_today`.
- Riformulare `CLK-01`: chiarire la perfetta uguaglianza algebrica `step == day * turnsPerDay + hour` in ogni stato valido.
- Chiarire che un harvest immaturo è un silent no-op (nessun warning distruttivo).

### 3. Per `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`:
- Allineare i predetti di serviceability e capacità alle tre classi rigorose (`ACTION_ELIGIBLE_NOW`, `RESERVED_SERVICEABLE_BEFORE_DEADLINE`, `REALIZED_SERVICEABLE_IN_WINDOW`).
- Rimuovere ogni possibile futuro data-leakage (es. completion evidence o reward utilizzati come feature decisionali pre-azione).

---

## 10. Authorization Gate

In accordo con la sequenza rigorosa stabilita dal processo C2 Foundation:

```text
================================================================================
ENGINE_CONTRACT_FREEZE: YES
================================================================================
ONTOLOGY_REVISION_AUTHORIZED: YES
STATE_MACHINE_REVISION_AUTHORIZED: NO
FEATURE_MODEL_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```

*Nota procedurale:* L'autorizzazione per la State Machine e il Feature Model sarà rilasciata sequenzialmente solo dopo la conclusione e l'approvazione della revisione dell'Ontologia C2.

---

## 11. Final Verdict

```text
================================================================================
FINAL VERDICT: ENGINE_CONTRACT_FREEZE: YES
================================================================================
L'Engine Contract e il Period Ledger C2 sono formalmente riconciliati,
verificati all'unanimità dai tre reviewer e CONGELATI.
L'identità dell'ambiente è sigillata con fingerprint 4378b60f...
Il progetto è formalmente autorizzato a procedere alla revisione dell'Ontologia C2.
================================================================================
```
