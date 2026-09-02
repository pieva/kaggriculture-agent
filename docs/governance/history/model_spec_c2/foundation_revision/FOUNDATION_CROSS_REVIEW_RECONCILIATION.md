# KAGGRICULTURE C2 — TRI-AGENT FOUNDATION CROSS-REVIEW RECONCILIATION REPORT

```text
DOCUMENT_ID: FOUNDATION_CROSS_REVIEW_RECONCILIATION
RECONCILER: Antigravity (Sole Reconciler)
DATE: 2026-08-31
PHASE: Model Foundation Cycle 2 (C2) / Tri-Agent Cross-Review Reconciliation
INPUT_REPORTS:
  - docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_FOUNDATION_CROSS_REVIEW.md
  - docs/governance/history/model_spec_c2/foundation_revision/COPILOT_FOUNDATION_CROSS_REVIEW.md
  - docs/governance/history/model_spec_c2/foundation_revision/CODEX_FOUNDATION_CROSS_REVIEW.md
NORMATIVE_AUTHORITY:
  - Frozen Runtime Source: kaggle_environments/envs/kaggriculture/kaggriculture.py & kaggriculture.json
  - Frozen Engine Contract: docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md
  - Frozen Period Ledger: docs/governance/history/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
STATUS: COMPLETE — CANONICAL CORRECTION SET ESTABLISHED
```

---

## 1. Executive Reconciliation Verdict

In conformità con il mandato di **reconciler unico indipendente**, Antigravity ha esaminato integralmente i tre report di cross-review prodotti da Antigravity, Copilot e Codex, verificando ogni singolo finding direttamente contro il runtime e i contratti congelati dell'engine.

### Verdetto di Riconciliazione:
- Il precedente verdetto di `PASS` emesso dalla prima review Antigravity **viene formalmente revocato**. La verifica diretta del codice sorgente dell'interprete (`kaggriculture.py`) conferma la fondatezza tecnica e normativa dei **sei difetti critici P0** individuati da Codex, unitamente a convergenze architetturali P1 identificate da Copilot e Codex;
- La Model Foundation necessita di un **ciclo chirurgico di consolidamento (Foundation Correction Set)** per eliminare le contraddizioni con l'engine reale, disallineare le assunzioni spurie di policy e stabilire un contratto matematicamente rigoroso;
- La nuova architettura a 5 livelli (con **`DECISION LIFECYCLE CONTRACT`** come layer Foundation condiviso e **`MODEL_SPEC`** agent-specific) è confermata e validata;
- Nessun file sorgente della Foundation, né il `README.md`, né la directory `foundation_revision/` è stato modificato in questa fase.

```text
RECONCILIATION_VERDICT: CORRECTIONS_MANDATED_BEFORE_FREEZE
P0_CONFIRMED: 6 (CAN-FND-P0-01 .. CAN-FND-P0-06)
P1_CONFIRMED: 7 (CAN-FND-P1-01 .. CAN-FND-P1-07)
P2_CONFIRMED: 3 (CAN-FND-P2-01 .. CAN-FND-P2-03)
P0_REJECTED: 0
P1_REJECTED: 0
P2_REJECTED: 0
FOUNDATION_READY_FOR_CONSOLIDATION: YES
DECISION_LIFECYCLE_REQUIREMENTS_READY: YES
```

---

## 2. Sources and Authority Hierarchy

In caso di discordanza tra i report e i testi della Foundation, la riconciliazione ha applicato la seguente rigorosa gerarchia di autorità:

```text
┌────────────────────────────────────────────────────────┐
│ 1. FROZEN RUNTIME / SOURCE CODE (kaggriculture.py)     │
│    SHA-256 Fingerprint: 4378b60f...                    │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ 2. FROZEN ENGINE CONTRACT & PERIOD LEDGER AUDIT        │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ 3. FOUNDATION ARTEFACTS (Ontology, State Machine, FM)  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ 4. CROSS-REVIEW REPORTS (Antigravity, Copilot, Codex)  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Tri-Agent Verdict Comparison

| Revisore | Verdetto Iniziale | P0 Dichiarati | P1 Dichiarati | P2 Dichiarati | Valutazione del Reconciler |
|---|:---:|:---:|:---:|:---:|---|
| **Antigravity** | `PASS` | 0 | 0 | 1 | **Non normativo / Superato:** Ha trascurato 6 difetti reali dell'engine runtime celati dietro convenzioni non verificate. |
| **Copilot** | `ACCEPT_WITH_CORRECTIONS` | 0 | 2 | 1 | **Accurato su architettura:** Ha colto la divergenza tassonomica sui tile lifecycle (`P1-01`) e le lacune di invalidazione del Decision Lifecycle (`P1-02`). |
| **Codex** | `FAIL_WITH_BLOCKERS` | 6 | 8 | 3 | **Accurato su engine runtime:** Ha condotto un source audit perfetto su `kaggriculture.py`, scoprendo 6 contraddizioni P0 critiche con l'engine. |

---

## 4. P0 Source Verification (Codex P0 Findings Audit)

Tutti i 6 finding P0 sollevati da Codex sono stati verificati riga per riga su `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py`.

### 4.1 `CR-FND-P0-01` — Nonexistent Worker Carrying Capacity
- **SOURCE CHECK:** `kaggriculture.py:299-309` (`_inv_add`), `358-375` (`PICKUP`), `451-473` (`HARVEST`), `515-522` (`COLLECT_FERTILIZER`), `827` (`_daily_refresh_animals`).
- **ENGINE/RUNTIME EVIDENCE:** `_inv_add` inserisce merce nel dizionario `private["inventories"][idx]` senza alcun controllo di capienza massima. Il campo `ANIMALS[species]["max_held"]` regola unicamente l'accumulo di resa sulla tile della struttura zootecnica (`min(a["max_held"], tile["yield_units"] + base + bonus)`).
- **FOUNDATION EVIDENCE:** `KAGGRICULTURE_FEATURE_MODEL_C2.md` definiva `WRK-06` (`worker_capacity_available`) e vincolava l'ammissibilità di `PICKUP` (`ELG-03`), `HARVEST` (`ELG-09`, `ELG-10`) e `COLLECT_FERTILIZER` (`ELG-17`) a `worker_capacity > 0`.
- **VERDICT:** **CONFIRMED (CAN-FND-P0-01)**.
- **FINAL SEVERITY:** **P0**.
- **FILES AFFECTED:** `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`, `docs/foundation/ontology/ONTOLOGY_C2.md`, `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`.
- **MINIMAL CORRECTION:** Eliminare la nozione di capienza limitata del worker; rimuovere `WRK-06`; rimuovere le guardie di spazio worker da `ELG-03`, `ELG-09`, `ELG-10`, `ELG-17`; ridenominare `max_held` esclusivamente come capacità massima di stoccaggio sulla tile animale.

### 4.2 `CR-FND-P0-02` — Runtime Observation Paths Inexistent in Observation State
- **SOURCE CHECK:** `kaggriculture.py:180-182` (`_new_market`), `230-241` (`_new_animal`), `261-275` (`_initialize`).
- **ENGINE/RUNTIME EVIDENCE:** Le tile zootecniche contengono un dizionario piatto: `{"kind": a["structure"], "animal": animal, "yield_units": 0, "fertilizer_available": False, ...}`. Non esiste alcun oggetto annidato `structure.*`. Lo stato del mercato espone `market = {"inventory": ..., "prices": ...}`; non esistono mappe `buy_prices` o `sell_prices`.
- **FOUNDATION EVIDENCE:** `KAGGRICULTURE_FEATURE_MODEL_C2.md` indicava raw observation paths inesistenti: `structure.animal.species` (`LIV-01`), `structure.fertilizer_available` (`LIV-10`), `structure.output_available` (`LIV-11`), `market.buy_prices` (`MKT-02`), `market.sell_prices` (`MKT-03`).
- **VERDICT:** **CONFIRMED (CAN-FND-P0-02)**.
- **FINAL SEVERITY:** **P0**.
- **FILES AFFECTED:** `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`.
- **MINIMAL CORRECTION:** Correggere i raw paths con i campi effettivi (`tile.animal`, `tile.fertilizer_available`, `tile.yield_units`, `market.prices[item]`) o classificarli come derivazioni deterministiche esplicite.

### 4.3 `CR-FND-P0-03` — Hard-Coded Land and Capacity Constants Contradict Configuration
- **SOURCE CHECK:** `kaggriculture.py:134, 147, 251` (`_shed_access_tiles`, `_new_farm`, `boardSize`), `kaggriculture.json`.
- **ENGINE/RUNTIME EVIDENCE:** La dimensione del quadrante è `(boardSize // 2) * (boardSize // 2)`. Con `boardSize = 10` di default, ogni quadrante contiene 25 tile (e non 16). La capienza dello shed (`shedCapacity = 100`) e il limite ordini di mercato (`maxMarketOrdersPerTurn = 10`) sono parametri di `configuration` e non costanti universali immodificabili.
- **FOUNDATION EVIDENCE:** `KAGGRICULTURE_FEATURE_MODEL_C2.md` hardcodava 16 tile per quadrante in `FRM-03` e costanti scalari non parametriche.
- **VERDICT:** **CONFIRMED (CAN-FND-P0-03)**.
- **FINAL SEVERITY:** **P0**.
- **FILES AFFECTED:** `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`, `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`.
- **MINIMAL CORRECTION:** Parametrizzare l'area del quadrante in funzione di `boardSize` e legare i limiti di shed e mercato ai campi di `configuration`.

### 4.4 `CR-FND-P0-04` — Ongoing Fertilizer Effect Omits Same-Transition Watering Predicate
- **SOURCE CHECK:** `kaggriculture.py:777-800` (`_daily_refresh_plants`).
- **ENGINE/RUNTIME EVIDENCE:** L'effetto del fertilizzante all'EOD colturale è:
  `fertilized = was_watered and tile.get("fertilized_until_day", -1) >= current_day`
  `tile["yield_units"] = min(cd["max_yield"], tile["yield_units"] + (2 if fertilized else 1))`.
  Se la pianta non è stata irrigata (`was_watered == False`), il bonus non viene applicato!
- **FOUNDATION EVIDENCE:** `KAGGRICULTURE_STATE_MACHINE_C2.md` e `KAGGRICULTURE_FEATURE_MODEL_C2.md` (`FRT-04`) definivano l'uplift $+1$ (totale 2) come dipendente unicamente da `fertilized_until_day >= day`, omettendo la condizione congiuntiva fondamentale di irrigazione nel giorno corrente.
- **VERDICT:** **CONFIRMED (CAN-FND-P0-04)**.
- **FINAL SEVERITY:** **P0**.
- **FILES AFFECTED:** `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`, `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`, `docs/foundation/ontology/ONTOLOGY_C2.md`.
- **MINIMAL CORRECTION:** Esplicitare la congiunzione: l'incremento a 2 unità si verifica se e solo se `was_watered == True` E `fertilized_until_day >= day`.

### 4.5 `CR-FND-P0-05` — Structure Construction Assigned Fictitious Cash Cost
- **SOURCE CHECK:** `kaggriculture.py:493-503` (`BUILD_COOP`, `BUILD_PASTURE`).
- **ENGINE/RUNTIME EVIDENCE:**
  ```python
  if op == "BUILD_COOP":
      if tile is not None: return
      farm["tiles"][fy][fx] = {"kind": "COOP"}
      return
  ```
  Le azioni `BUILD_COOP` e `BUILD_PASTURE` non effettuano alcun controllo di cassa né deducono denaro (`farm.money`). Richiedono esclusivamente che la tile sia libera (`None`).
- **FOUNDATION EVIDENCE:** `KAGGRICULTURE_STATE_MACHINE_C2.md` e `KAGGRICULTURE_FEATURE_MODEL_C2.md` imponevano una guardia `money >= cost` e registravano in `POST-08` spese monetarie inesistenti.
- **VERDICT:** **CONFIRMED (CAN-FND-P0-05)**.
- **FINAL SEVERITY:** **P0**.
- **FILES AFFECTED:** `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`, `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`, `docs/foundation/ontology/ONTOLOGY_C2.md`.
- **MINIMAL CORRECTION:** Rimuovere qualsiasi requisito di cassa e deduzione per l'edificazione di strutture. `POST-08` registra zero esborso finanziario diretto.

### 4.6 `CR-FND-P0-06` — Pending Animal-Care Reset Semantics Incorrect
- **SOURCE CHECK:** `kaggriculture.py:823-828` (`_daily_refresh_animals`).
- **ENGINE/RUNTIME EVIDENCE:**
  ```python
  if days_since_first >= 0 and days_since_first % a["interval"] == 0:
      base = 1
      bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
      tile["yield_units"] = min(a["max_held"], tile["yield_units"] + base + bonus)
      tile["pending_care_bonus"] = 0
  ```
  In ogni giorno di produzione programmata, `pending_care_bonus` viene resettato a `0`, sia che l'animale sia stato nutrito (dove il bonus viene convertito in prodotto), sia che non sia stato nutrito (dove il bonus va perduto). Non persiste indefinitamente fino al successivo giorno alimentato!
- **FOUNDATION EVIDENCE:** La Foundation descriveva il bonus di cura come permanente e consumato solo alla prima produzione alimentata utile.
- **VERDICT:** **CONFIRMED (CAN-FND-P0-06)**.
- **FINAL SEVERITY:** **P0**.
- **FILES AFFECTED:** `docs/foundation/ontology/ONTOLOGY_C2.md`, `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`, `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`.
- **MINIMAL CORRECTION:** Specificare che il reset di `pending_care_bonus` avviene ad ogni giorno di produzione programmata dell'animale.

---

## 5. Copilot/Codex Convergence Reconciliation

### 5.1 Tile Lifecycle Taxonomy (Copilot `P1-01` & Codex `CR-FND-P1-02`)
- **Analisi:** Copilot e Codex convergono sulla disarmonia tra la tassonomia a 6 stati (Ontology/State Machine con `EMPTY_ASSIGNED` e `RETIREMENT_DUE`) e la tassonomia a 5 stati fisici (Feature Model con `EMPTY_AVAILABLE` e retirement come `POL-RET`).
- **Disposizione:** **MERGED into CAN-FND-P1-01**.
- **Correzione Canonica:**
  1. La partizione fisica dell'ambiente deve consistere ovunque di **5 Derived Views deterministiche ed esaustive**:
     - `OUT_OF_SCOPE`: tile bloccata (`"LOCKED"`) o struttura (`"COOP"`, `"PASTURE"`);
     - `LOST_WEED`: tile infestata da erbacce (`"WEED"`);
     - `EMPTY_AVAILABLE`: tile arabile libera sbloccata (`None`);
     - `HARVEST_READY`: tile con coltura matura (`kind == "PLANT"` e `crop_harvest_readiness == True`);
     - `GROWING`: tile con coltura in crescita (`kind == "PLANT"` e `crop_harvest_readiness == False`).
  2. Le nozioni di allocazione al working set (`EMPTY_ASSIGNED` / `in_working_set`) e di marcatura per il ritiro (`RETIREMENT_DUE` / `policy_retirement_due`) sono **sovrapposizioni di policy (`POLICY_CONTEXT`)** e non stati intrinseci dell'ambiente.
  3. Allineare `ONTOLOGY_C2.md`, `KAGGRICULTURE_STATE_MACHINE_C2.md` e `KAGGRICULTURE_FEATURE_MODEL_C2.md` a questa definizione univoca.

### 5.2 Decision Lifecycle Invalidation Semantics (Copilot `P1-02` & Codex `CR-FND-P1-08`)
- **Analisi:** Entrambi i revisori evidenziano che la sequenza candidata `DECISION_OPEN` $\to$ `DEFINED` $\to$ `PLAN_FEASIBLE` $\to$ `COMMITTED_EXECUTING` $\to$ `REVIEW_READY` manca di transizioni formali di invalidazione, fallimento, riparazione e chiusura terminale.
- **Disposizione:** **MERGED into CAN-REQ-DLC-01** (Requisiti per il futuro contratto Decision Lifecycle).
- **Correzione Canonica:** Formalizzare nel futuro Decision Lifecycle Contract:
  - Transizione `PROPOSED` $\to$ `INFEASIBLE` / `REJECTED`;
  - Transizione `COMMITTED_EXECUTING` $\to$ `INVALIDATED` (su trigger osservabili di violazione invarianti di piano);
  - Transizione `COMMITTED_EXECUTING` $\to$ `REPAIR_WITHIN_COMMITMENT`;
  - Transizione `COMMITTED_EXECUTING` $\to$ `SUPERSEDED` / `CANCELLED`;
  - Transizione di chiusura terminale dell'episodio.

---

## 6. Remaining P1/P2 Reconciliation

### 6.1 `CR-FND-P1-01` — Batch- and Serialization-Aware Eligibility
- **Evidenza:** La semina di gruppo su medesima semente valida la domanda aggregata; le azioni multi-worker sono eseguite sequenzialmente e possono mutare l'inventario prima del turno del worker successivo.
- **Disposizione:** **CONFIRMED (CAN-FND-P1-02)**.
- **Azione:** Distinguere l'ammissibilità statica allo snapshot $t$ dalla fattibilità di batch e registrare la validazione atomica di semina.

### 6.2 `CR-FND-P1-03` — Epistemic Conflation of Intent and Execution Evidence
- **Evidenza:** Alcuni concetti ontologici ed elementi di catalogo combinano l'intento di azione con l'esito di transizione.
- **Disposizione:** **CONFIRMED (CAN-FND-P1-03)**.
- **Azione:** Strutturare gli eventi in 4 classi temporali disgiunte: *Action Request*, *Snapshot Eligibility*, *Execution Outcome (Success/No-op)*, *Post-State Evidence*.

### 6.3 `CR-FND-P1-04` — Global Transition & Terminal Boundary Semantics
- **Evidenza:** La sequenza di EOD e la terminazione dell'episodio richiedono l'esatto allineamento all'ordine di esecuzione del runtime.
- **Disposizione:** **CONFIRMED (CAN-FND-P1-04)**.
- **Azione:** Allineare i diagrammi di sequenza e il predicato di terminazione all'offset esatto dell'engine.

### 6.4 `CR-FND-P1-05` — Agent Strategy Leaks into Common Foundation
- **Evidenza:** Concetti come buffer di cassa/mangime, finestre di capitale e classificazioni soggettive di "azioni produttive" non sono leggi dell'ambiente.
- **Disposizione:** **CONFIRMED (CAN-FND-P1-05)**.
- **Azione:** Riconfinare questi elementi nei successivi `MODEL_SPEC` agent-specific.

### 6.5 `CR-FND-P1-06` — Performance Accounting & Wheat Flow Dimensional Consistency
- **Evidenza:** L'equazione di bilancio del Wheat deve considerare tutte le scorte (tile yield, worker inv, shed stock) e flussi; saturazione booleana del fertilizzante.
- **Disposizione:** **CONFIRMED (CAN-FND-P1-06)**.
- **Azione:** Rendere l'identità contabile del Wheat dimensionale ed esaustiva.

### 6.6 `CR-FND-P1-07` — Experimental Provenance Configuration Snapshot
- **Evidenza:** `boardSize`, `turnsPerDay`, `shedCapacity`, `maxMarketOrdersPerTurn` influenzano il gioco indipendentemente dal codice.
- **Disposizione:** **CONFIRMED (CAN-FND-P1-07)**.
- **Azione:** Inserire nei metadati di provenance l'hash immutabile della configurazione e la chiave composita `(run_id, episode_id)`.

### 6.7 `Copilot P2-01` — `source_concept_id` Traceability Mappings
- **Evidenza:** Alcuni ID concettuali nell'Ontology mapping del Feature Model erano semanticamente incongrui (es. prezzi mappati su action flows).
- **Disposizione:** **CONFIRMED (CAN-FND-P2-01)**.
- **Azione:** Introdurre concetti ontologici precisi o valorizzare `NONE_DIRECT`.

### 6.8 `CR-FND-P2-02` & `CR-FND-P2-03` / `Antigravity FND-01` — Documentation & Diagrams
- **Disposizione:** **CONFIRMED (CAN-FND-P2-02, CAN-FND-P2-03)**.

---

## 7. Cross-Layer Additional Checks

### 7.1 Wheat Accounting Dimensional Consistency
L'equazione di conservazione del Wheat è formalizzata come identità di bilancio di massa:
$$\text{Stock}_{t=0} + \text{Purchased Units} + \text{Harvested Units} = \text{Fed Units} + \text{Sold Units} + \text{Lost Units} + \text{Stock}_{t=\text{end}}$$
dove:
- $\text{Stock} = \text{Shed Stock} + \sum \text{Worker Inv} + \sum \text{Tile Yield Units}$;
- $\text{Purchased Units}$ è la quantità fisica (unità) derivata dagli ordini `BUY_PRODUCT` WHEAT (distinta dalla spesa monetaria in valuta di `POST-09`).

### 7.2 Fertilizer Saturation Semantics
Se un animale ha già `fertilizer_available == True`, l'EOD non genera una seconda unità; il flag rimane `True` senza accumulo. La telemetria post-hoc `POST-22` misura gli eventi in cui il fertilizzante viene effettivamente reso disponibile rispetto a transizioni neutre.

---

## 8. Canonical Confirmed Finding Set

| Canonical ID | Originating Finding(s) | Status | Final Severity | Layer | Normative Evidence | Affected File(s) | Blocks Freeze | Blocks Decision Lifecycle |
|---|---|:---:|:---:|---|---|---|:---:|:---:|
| **CAN-FND-P0-01** | Codex `CR-FND-P0-01` | `CONFIRMED` | **P0** | Feature Model / Engine Contract | `kaggriculture.py:299-309` (`_inv_add`), `827` | `KAGGRICULTURE_FEATURE_MODEL_C2.md`, `ONTOLOGY_C2.md`, `KAGGRICULTURE_STATE_MACHINE_C2.md` | **YES** | **YES** |
| **CAN-FND-P0-02** | Codex `CR-FND-P0-02` | `CONFIRMED` | **P0** | Feature Model / Observations | `kaggriculture.py:180, 230` | `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | **YES** |
| **CAN-FND-P0-03** | Codex `CR-FND-P0-03` | `CONFIRMED` | **P0** | Feature Model / Config | `kaggriculture.py:134, 251` | `KAGGRICULTURE_FEATURE_MODEL_C2.md`, `KAGGRICULTURE_STATE_MACHINE_C2.md` | **YES** | **YES** |
| **CAN-FND-P0-04** | Codex `CR-FND-P0-04` | `CONFIRMED` | **P0** | State Machine / Feature Model | `kaggriculture.py:799` | `KAGGRICULTURE_STATE_MACHINE_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md`, `ONTOLOGY_C2.md` | **YES** | **YES** |
| **CAN-FND-P0-05** | Codex `CR-FND-P0-05` | `CONFIRMED` | **P0** | State Machine / Feature Model | `kaggriculture.py:493-503` | `KAGGRICULTURE_STATE_MACHINE_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md`, `ONTOLOGY_C2.md` | **YES** | **YES** |
| **CAN-FND-P0-06** | Codex `CR-FND-P0-06` | `CONFIRMED` | **P0** | State Machine / Feature Model | `kaggriculture.py:823-828` | `ONTOLOGY_C2.md`, `KAGGRICULTURE_STATE_MACHINE_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | **YES** |
| **CAN-FND-P1-01** | Copilot `P1-01`, Codex `CR-FND-P1-02` | `MERGED` | **P1** | All Foundation Artefacts | Section 5.1 reconciliation | `ONTOLOGY_C2.md`, `KAGGRICULTURE_STATE_MACHINE_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | **YES** |
| **CAN-FND-P1-02** | Codex `CR-FND-P1-01` | `CONFIRMED` | **P1** | Feature Model / Actions | `kaggriculture.py:417, 544` | `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | NO |
| **CAN-FND-P1-03** | Codex `CR-FND-P1-03` | `CONFIRMED` | **P1** | Ontology / Feature Model | Section 6.2 reconciliation | `ONTOLOGY_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | NO |
| **CAN-FND-P1-04** | Codex `CR-FND-P1-04` | `CONFIRMED` | **P1** | State Machine / Timings | `kaggriculture.py:860` | `KAGGRICULTURE_STATE_MACHINE_C2.md`, `ONTOLOGY_C2.md` | **YES** | NO |
| **CAN-FND-P1-05** | Codex `CR-FND-P1-05` | `CONFIRMED` | **P1** | Ontology / Policy Boundary | Section 6.4 reconciliation | `ONTOLOGY_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | NO |
| **CAN-FND-P1-06** | Codex `CR-FND-P1-06` | `CONFIRMED` | **P1** | Performance Telemetry | Section 6.5 & 7.1 | `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | NO |
| **CAN-FND-P1-07** | Codex `CR-FND-P1-07` | `CONFIRMED` | **P1** | Provenance | Section 6.6 reconciliation | `KAGGRICULTURE_FEATURE_MODEL_C2.md` | **YES** | NO |
| **CAN-FND-P2-01** | Copilot `P2-01` | `CONFIRMED` | **P2** | Feature Model / Ontology | Section 6.7 reconciliation | `KAGGRICULTURE_FEATURE_MODEL_C2.md` | NO | NO |
| **CAN-FND-P2-02** | Codex `CR-FND-P2-02` | `CONFIRMED` | **P2** | Documentation / Diagrams | Section 6.8 reconciliation | `KAGGRICULTURE_STATE_MACHINE_C2.md`, `KAGGRICULTURE_FEATURE_MODEL_C2.md` | NO | NO |
| **CAN-FND-P2-03** | Antigravity `FND-01`, Codex `CR-FND-P2-03` | `MERGED` | **P2** | Documentation / README | Mandate Section 14 | `README.md` | NO | NO |

---

## 9. Foundation Correction Set (Mandato per il Consolidation Agent)

Le seguenti correzioni formano il **Foundation Correction Set canonico** che dovrà essere applicato nel successivo consolidation pass:

```text
================================================================================
CORR-01: WORKER CAPACITY & ELIGIBILITY CORRECTION
  - TARGET FILES: KAGGRICULTURE_FEATURE_MODEL_C2.md, ONTOLOGY_C2.md, KAGGRICULTURE_STATE_MACHINE_C2.md
  - TARGET SECTIONS: Master Catalog WRK-06, ELG-03, ELG-09, ELG-10, ELG-17; Section 7/8/9
  - REQUIRED CHANGE: Rimuovere worker capacity; eliminare guardie su capienza worker; ridenominare max_held come tile-storage capacity per specie animale.
  - NORMATIVE BASIS: kaggriculture.py:299-309, 827.
  - ACCEPTANCE CHECK: Zero riferimenti a worker carrying capacity; predicati ELG non condizionati da spazio inventario worker.

CORR-02: RAW OBSERVATION PATHS ALIGNMENT
  - TARGET FILE: KAGGRICULTURE_FEATURE_MODEL_C2.md
  - TARGET SECTIONS: Master Catalog LIV-01, LIV-10, LIV-11, MKT-02, MKT-03
  - REQUIRED CHANGE: Sostituire percorsi annidati con percorsi osservabili reali (tile.animal, tile.fertilizer_available, tile.yield_units, market.prices).
  - NORMATIVE BASIS: kaggriculture.py:180-182, 230-241.
  - ACCEPTANCE CHECK: Tutti i raw observation paths corrispondono a chiavi reali dell'environment state.

CORR-03: CONFIGURATION-PARAMETRIC LAND & CAPACITY CONSTANTS
  - TARGET FILES: KAGGRICULTURE_FEATURE_MODEL_C2.md, KAGGRICULTURE_STATE_MACHINE_C2.md
  - TARGET SECTIONS: FRM-03, INV-03, MKT-LIMIT
  - REQUIRED CHANGE: Parametrizzare area quadrante come (boardSize//2)^2 (25 default) e legare capienza shed e ordini mercato ai parametri di configuration.
  - NORMATIVE BASIS: kaggriculture.py:134, 251.
  - ACCEPTANCE CHECK: Nessun hardcode di 16 tile/quadrante; formule dipendenti da configuration.

CORR-04: CONJUNCTIVE ONGOING FERTILIZER PREDICATE (WATERING REQUIREMENT)
  - TARGET FILES: KAGGRICULTURE_STATE_MACHINE_C2.md, KAGGRICULTURE_FEATURE_MODEL_C2.md, ONTOLOGY_C2.md
  - TARGET SECTIONS: State Machine EOD Crop Transition, FM FRT-04
  - REQUIRED CHANGE: Esplicitare che il bonus +1 (totale 2) richiede was_watered == True E fertilized_until_day >= day.
  - NORMATIVE BASIS: kaggriculture.py:799.
  - ACCEPTANCE CHECK: Formula di calcolo resa fertilizzata esplicitamente condizionata a was_watered.

CORR-05: STRUCTURE ZERO-CASH COST RECONCILIATION
  - TARGET FILES: KAGGRICULTURE_STATE_MACHINE_C2.md, KAGGRICULTURE_FEATURE_MODEL_C2.md, ONTOLOGY_C2.md
  - TARGET SECTIONS: State Machine BUILD transitions, FM POST-08, ELG-13, ELG-14
  - REQUIRED CHANGE: Eliminare qualsiasi guardia di cassa e costo monetario per BUILD_COOP e BUILD_PASTURE. POST-08 registra zero spesa cassa diretta.
  - NORMATIVE BASIS: kaggriculture.py:493-503.
  - ACCEPTANCE CHECK: Transizioni BUILD prive di requisiti monetari; POST-08 coerente con spesa reale zero.

CORR-06: PENDING ANIMAL CARE RESET SEMANTICS
  - TARGET FILES: ONTOLOGY_C2.md, KAGGRICULTURE_STATE_MACHINE_C2.md, KAGGRICULTURE_FEATURE_MODEL_C2.md
  - TARGET SECTIONS: Ontology Liv-06, SM Livestock Transition, FM LIV-06/09
  - REQUIRED CHANGE: Formalizzare che pending_care_bonus viene azzerato a 0 ad ogni giorno di produzione programmata (applicato se fed, perso se unfed).
  - NORMATIVE BASIS: kaggriculture.py:823-828.
  - ACCEPTANCE CHECK: Descrizione del ciclo di vita animale allineata al reset programmato.

CORR-07: CANONICAL 5-ENVIRONMENT TILE PARTITION & POLICY OVERLAYS
  - TARGET FILES: ONTOLOGY_C2.md, KAGGRICULTURE_STATE_MACHINE_C2.md, KAGGRICULTURE_FEATURE_MODEL_C2.md
  - TARGET SECTIONS: Ontology Domini Terreno/Colture, SM Sezione 3.1 & 11, FM Sezione 5
  - REQUIRED CHANGE: Standardizzare ovunque le 5 viste ambientali pure (OUT_OF_SCOPE, LOST_WEED, EMPTY_AVAILABLE, HARVEST_READY, GROWING) e trattare working set (POL-WS) e retirement (POL-RET) come sovrapposizioni di policy.
  - NORMATIVE BASIS: CAN-FND-P1-01 reconciliation.
  - ACCEPTANCE CHECK: Vocabolario e numero di stati identico e consistente in tutti e 3 i documenti.

CORR-08: BATCH- & SERIALIZATION-AWARE ACTION FEASIBILITY
  - TARGET FILE: KAGGRICULTURE_FEATURE_MODEL_C2.md
  - TARGET SECTIONS: Section 13 (Action Eligibility), ELG-07
  - REQUIRED CHANGE: Distinguere ammissibilità su snapshot da validazione atomica aggregata di semina e ordinamento sequenziale multi-worker.
  - NORMATIVE BASIS: kaggriculture.py:417, 544.
  - ACCEPTANCE CHECK: Esplicitata la semantica di validazione batch e mutazione sequenziale.

CORR-09: RIGOROUS WHEAT MASS BALANCE & FERTILIZER SATURATION
  - TARGET FILE: KAGGRICULTURE_FEATURE_MODEL_C2.md
  - TARGET SECTIONS: Section 16 (POST-09, POST-21, POST-22, Wheat Flow Accounting)
  - REQUIRED CHANGE: Riconciliare l'identità a 5 vie del Wheat includendo tutte le scorte (tile yield, worker inv, shed stock) e distinguendo unità fisiche da spesa monetaria. Specificare la saturazione booleana del fertilizzante animale.
  - NORMATIVE BASIS: CAN-FND-P1-06 reconciliation.
  - ACCEPTANCE CHECK: Equazione di bilancio dimensionale esatta e coerente.

CORR-10: CONFIGURATION SNAPSHOT & PROVENANCE JOIN KEYS
  - TARGET FILE: KAGGRICULTURE_FEATURE_MODEL_C2.md
  - TARGET SECTIONS: Section 17 (Metadata di Provenance)
  - REQUIRED CHANGE: Introdurre la chiave composita (run_id, episode_id) e l'identificatore/hash immutabile dello snapshot di configuration.
  - NORMATIVE BASIS: CAN-FND-P1-07 reconciliation.
  - ACCEPTANCE CHECK: Metadati sufficienti a garantire riproducibilità e unicità dei record di match.

CORR-11: REFINED ONTOLOGY CONCEPT TRACEABILITY MAPPINGS
  - TARGET FILE: KAGGRICULTURE_FEATURE_MODEL_C2.md
  - TARGET SECTIONS: Section 4 (Master Catalog source_concept_id)
  - REQUIRED CHANGE: Correggere i mapping concettuali spuri (CRP-02, MKT-08, MKT-09) verso concetti ontologici precisi o NONE_DIRECT.
  - NORMATIVE BASIS: Copilot P2-01.
  - ACCEPTANCE CHECK: Zero mapping semantici impropri nel Master Catalog.

CORR-12: REMOVAL OF HARDCODED STRATEGIC BUFFERS FROM ONTOLOGY
  - TARGET FILE: ONTOLOGY_C2.md
  - TARGET SECTIONS: Domini F (Capitale) e I (Governance)
  - REQUIRED CHANGE: Rimuovere o riclassificare come CONTEXT_ONLY definizioni normative di operating_cash_buffer, feed_security_buffer, deployable_capital_window e endgame liquidation, demandandole a MODEL_SPEC.
  - NORMATIVE BASIS: CAN-FND-P1-05 reconciliation.
  - ACCEPTANCE CHECK: Ontology puramente descrittiva delle leggi fisiche/economiche dell'ambiente.
================================================================================
```

---

## 10. Decision Lifecycle Requirements

La riconciliazione stabilisce i seguenti requisiti formali per la successiva stesura del **`DECISION LIFECYCLE CONTRACT`** (Foundation condivisa):

1. **Protocollo di Stati Deliberativi Governatore:**
   $$\text{DECISION\_OPEN} \longrightarrow \text{DEFINED} \longrightarrow \text{PLAN\_FEASIBLE} \longrightarrow \text{COMMITTED\_EXECUTING} \longrightarrow \text{REVIEW\_READY} \longrightarrow \text{DECISION\_OPEN}$$
2. **Transizioni di Fallimento ed Eccezione:**
   - $\text{DEFINED} \to \text{INFEASIBLE} / \text{REJECTED} \to \text{DECISION\_OPEN}$;
   - $\text{COMMITTED\_EXECUTING} \to \text{INVALIDATED}$ (su violazione osservabile di pre-condizioni o risorse);
   - $\text{COMMITTED\_EXECUTING} \to \text{REPAIR\_WITHIN\_COMMITMENT}$;
   - $\text{COMMITTED\_EXECUTING} \to \text{SUPERSEDED} / \text{CANCELLED}$;
   - Chiusura forzata su $\text{TERMINAL\_CLOSED}$.
3. **Evidence Timing e Anti-Oscillazione:**
   - `VERIFY` opera in modo continuo registrando evidenze sullo stato post-transizione;
   - Nessun replanning automatico ad ogni tick: il commitment rimane stabile fino al verificarsi di condizioni di completamento (`COMPLETED`) o guardie esplicite di invalidazione (`INVALIDATED`).

---

## 11. MODEL_SPEC Boundary Requirements

Rimangono rigorosamente confinati ai futuri **`MODEL_SPEC` agent-specific** (Antigravity, Codex, Copilot):
- Obiettivi strategici, scoring e pesi di utilità;
- Scelta del portafoglio colturale e zootecnico (crop mix, livestock ON/OFF);
- Politiche di assunzione e dimensionamento della forza lavoro;
- Euristiche di routing, geometric transit optimization e pathfinding;
- Soglie quantitative di cassa, scorte di sicurezza e finestre di allocazione capitale;
- Trigger deliberativi di ritiro asset (`policy_retirement_due`) ed espansione fondiaria.

---

## 12. Documentation / README Requirements (per il Consolidation Agent)

Il successivo consolidation pass recepirà nella documentazione di progetto (`README.md`):
1. La formalizzazione della nuova architettura metodologica a 5 layer:
   $$\text{Engine Contract} \longrightarrow \text{Ontology} \longrightarrow \text{State Machine} \longrightarrow \text{Feature Model} \longrightarrow \text{Decision Lifecycle Contract} \Longrightarrow \text{MODEL\_SPEC (Agent-Specific)}$$
2. Il chiarimento definitivo che **`C2` = Cycle 2** (ciclo di revisione della Model Foundation) e non un componente o una strategia;
3. La netta separazione epistemica tra *Action Request*, *Execution Outcome* e *State Transition*.

---

## 13. foundation_revision Cleanup Requirements (per il Consolidation Agent)

Nel consolidation pass, la directory `results/model_spec_c2/foundation_revision/` dovrà essere razionalizzata:
- Conservare i report di riconciliazione e gli audit normativi ufficiali (`ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md`, `CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`, `FOUNDATION_CROSS_REVIEW_RECONCILIATION.md`);
- Archiviare i prompt intermedi di micro-correzione superati.

---

## 14. Residual Source Checks

Nessun punto critico rimane aperto a livello di codice engine: tutti i comportamenti contestati sono stati verificati in modo esaustivo su `kaggriculture.py`.

---

## 15. Final Gate

```text
================================================================================
P0_CONFIRMED: 6
P1_CONFIRMED: 7
P2_CONFIRMED: 3

P0_REJECTED: 0
P1_REJECTED: 0
P2_REJECTED: 0

FOUNDATION_ENGINE_ALIGNMENT: PENDING_CORRECTIONS (Correction Set Ready)
FOUNDATION_CROSS_LAYER_ALIGNMENT: PENDING_CORRECTIONS (Correction Set Ready)
POLICY_NEUTRALITY: VALIDATED_IN_CORRECTION_SET
NO_FUTURE_LEAKAGE: VALIDATED_IN_CORRECTION_SET
PERFORMANCE_ACCOUNTING: FORMALIZED_IN_CORRECTION_SET
PROVENANCE: FORMALIZED_IN_CORRECTION_SET

FOUNDATION_CORRECTION_REQUIRED: YES
FOUNDATION_READY_FOR_CONSOLIDATION: YES
DECISION_LIFECYCLE_REQUIREMENTS_READY: YES

DECISION_LIFECYCLE_DRAFTING_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
README_MODIFICATION_AUTHORIZED: NO
FOUNDATION_REVISION_CLEANUP_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```
