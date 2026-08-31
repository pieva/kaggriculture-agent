# ANTIGRAVITY C2 — STATE MACHINE FINAL MICRO-CORRECTION REPORT

```text
DOCUMENT_ID: ANTIGRAVITY_C2_STATE_MACHINE_FINAL_MICRO_CORRECTION_REPORT
AUTHOR: Antigravity
DATE: 2026-08-31
PHASE: Foundation Revision / State Machine Final Micro-Correction
TARGET_DOCUMENT: docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
BASELINE_AUTHORITY: results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md (FROZEN)
ONTOLOGY_AUTHORITY: docs/model/ontology/ONTOLOGY_C2.md (FROZEN)
STATUS: COMPLETE — READY FOR FREEZE REVIEW
```

---

## 1. Executive Verdict

Antigravity ha completato con successo la **Final Micro-Correction** su `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`.

È stata eliminata l'incoerenza tassonomica residuale, distinguendo formalmente e inequivocabilmente le **variabili di stato engine-native primitive** dalle **viste derivate di lifecycle (`DERIVED LIFECYCLE VIEWS`)** utilizzate a livello di Ontology e Feature Model.

```text
TILE_TAXONOMY_CORRECTED: YES
ENGINE_NATIVE_VS_DERIVED_SEPARATION_EXPLICIT: YES
RETIREMENT_DUE_IS_DERIVED: YES
NO_NATIVE_TRANSITION_TO_RETIREMENT_DUE: YES
FEATURE_MODEL_DOWNSTREAM_WORDING_CORRECT: YES

MERMAID_GLOBAL_DIAGRAM_PRESENT: YES
MERMAID_TAXONOMY_ALIGNED: YES

ENGINE_CONTRACT_CONSISTENT: YES
ONTOLOGY_CONSISTENT: YES
STATE_MACHINE_READY_FOR_FREEZE_REVIEW: YES
```

---

## 2. Original Taxonomy Inconsistency

Nella versione precedente, la Sezione 3.1 introduceva un'ambiguità qualificando congiuntamente:
- I sei label (`OUT_OF_SCOPE`, `EMPTY_ASSIGNED`, `GROWING`, `HARVEST_READY`, `RETIREMENT_DUE`, `LOST_WEED`) come *"sei stati strutturali canonici ed esaustivi"* dell'ambiente;
- E contestualmente `RETIREMENT_DUE` come *"derived view / policy classification"*, non nativa dell'engine.

Questa sovrapposizione concettuale rischiava di confondere i campi di memoria primitivi dell'engine (`tile.kind`, `consecutive_unwatered`, `yield_units`, ecc.) con le categorie analitiche aggregate derivate dalla Foundation per guidare le decisioni dell'agente.

---

## 3. Engine-Native vs Derived-View Separation

La State Machine esplicita ora la netta separazione su due livelli:

1. **Livello 1 — Stato e Variabili Engine-Native:**
   - Coordinate, ownership e sblocco quadranti (`"LOCKED"` vs sbloccato);
   - `tile.kind` nativo (`None`, `"LOCKED"`, `PLANT`, `WEED`, `COOP`, `PASTURE`);
   - Parametri colturale/biologici (`crop`, `planted_day`, `yield_units`, `max_lifespan_step`);
   - Contatori e flags idrici (`watered_today`, `consecutive_unwatered`);
   - Finestra di fertilizzazione (`fertilized_until_day`);
   - Strutture e stato animale (`consecutive_unfed`, `fed_today`, `cared_today`, `pending_care_bonus`, `fertilizer_available`).
   - *Tutte le transizioni causali fisiche sono governate unicamente da queste variabili.*

2. **Livello 2 — Derived Tile Lifecycle Views (Classificazioni Funzionali):**
   - I sei label (`OUT_OF_SCOPE`, `EMPTY_ASSIGNED`, `GROWING`, `HARVEST_READY`, `RETIREMENT_DUE`, `LOST_WEED`) sono viste analitiche derivate deterministicamente dal Livello 1;
   - `RETIREMENT_DUE` è confermato come classificazione descrittiva/policy e non come stato o transizione causale obbligatoria dell'engine;
   - Per le specie ongoing, dopo l'harvest la pianta permane viva sulla tile con yield azzerato, in attesa di successivi eventi biologici o di un'azione volontaria `DIG`.

---

## 4. Section 3.1 Correction

La Sezione 3.1 di `KAGGRICULTURE_STATE_MACHINE_C2.md` è stata riscritta articolandola in:
- **3.1.A — Stato e Variabili Engine-Native:** catalogo esaustivo dei campi fisici primitivi;
- **3.1.B — Derived Tile Lifecycle Views (Classificazioni Funzionali):** definizione dei 6 label canonici come layer derivato, con regole di governance epistemica esplicite.

---

## 5. Mermaid Consistency Check

- Il diagramma Mermaid globale (Sezione 8) è rimasto intatto e renderizzabile (0 errori sintattici);
- Il nodo `RETIREMENT_DUE` è connesso tramite arco tratteggiato `-.->|derived view: final cycle complete|` e marcato come `RETIREMENT_DUE<br>(derived classification)`;
- `DIG` è rappresentata come azione esplicita dell'agente verso `EMPTY_ASSIGNED`.

---

## 6. Transition Table Consistency Check

- La Tabella Canonica delle Transizioni (Sezione 9) cataloga esclusivamente transizioni causali reali dell'ambiente;
- Non contiene alcuna transizione engine-native verso `RETIREMENT_DUE`;
- Per le ongoing, la transizione di `HARVEST` riporta il reset di `yield_units = 0` con permanenza della pianta nello stato biologico (`GROWING`), coerentemente con le regole dell'engine.

---

## 7. Downstream Feature Model Wording Correction

La Sezione 11 è stata aggiornata rimuovendo l'obbligo di *"assegnare a ogni coordinata esattamente uno dei 6 stati come obbligo engine"* e sostituendola con la corretta direttiva:
- Il Feature Model C2 implementerà un *derived classifier* computazionale basato su predicati chiusi e ordine deterministico di precedenza;
- `RETIREMENT_DUE` sarà gestito come classificazione derivata/policy;
- Sarà preservata la distinzione fondamentale tra lo stato primitivo osservato dall'engine e le feature derivate consumate dai controller.

---

## 8. Files Modified

- **`docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`** (Correzione tassonomica Sez. 3.1 e Sez. 11);
- **`results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_STATE_MACHINE_FINAL_MICRO_CORRECTION_REPORT.md`** (Creato).

---

## 9. Final Gate

```text
================================================================================
TILE_TAXONOMY_CORRECTED: YES
ENGINE_NATIVE_VS_DERIVED_SEPARATION_EXPLICIT: YES
RETIREMENT_DUE_IS_DERIVED: YES
NO_NATIVE_TRANSITION_TO_RETIREMENT_DUE: YES
FEATURE_MODEL_DOWNSTREAM_WORDING_CORRECT: YES

MERMAID_GLOBAL_DIAGRAM_PRESENT: YES
MERMAID_TAXONOMY_ALIGNED: YES

ENGINE_CONTRACT_CONSISTENT: YES
ONTOLOGY_CONSISTENT: YES
STATE_MACHINE_READY_FOR_FREEZE_REVIEW: YES
================================================================================
STATE_MACHINE_FREEZE: NO
FEATURE_MODEL_REVISION_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
================================================================================
```
