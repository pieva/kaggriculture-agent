# NEW_SESSION — Kaggriculture

## Ripresa operativa

```text
START_HERE:
Model Foundation C2 Layer 1–5 frozen and committed.
Proceed with independent agent-specific MODEL_SPEC C2 revision and BUILD.

AUTHORIZED:
- MODEL_SPEC revision: YES
- BUILD: YES

NOT YET AUTHORIZED:
- comparative tournament
- Kaggle submission
```

---

## 1. Stato della Model Foundation C2 (Frozen)

Tutti i 5 layer condivisi della Model Foundation C2 sono formalmente congelati:

1. **Engine Contract:** `results/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md`
2. **Ontology C2:** `docs/model/ontology/ONTOLOGY_C2.md`
3. **Environment State Machine C2:** `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`
4. **Feature Model C2:** `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`
5. **Decision Lifecycle Contract C2:** `docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md` (certificato da `results/model_spec_c2/foundation_revision/DECISION_LIFECYCLE_TARGETED_FINAL_FREEZE_REVIEW.md`)

---

## 2. Documenti chiave da consultare

Per la stesura e verifica dei `MODEL_SPEC`:
- `docs/model/ontology/ONTOLOGY_C2.md`
- `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`
- `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`
- `docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md`
- `results/model_spec_c2/foundation_revision/FOUNDATION_FINAL_FREEZE_REVIEW.md`
- `results/model_spec_c2/foundation_revision/DECISION_LIFECYCLE_TARGETED_FINAL_FREEZE_REVIEW.md`

---

## 3. Protocollo di indipendenza dei tre agenti

Ciascun agente (`Antigravity`, `Codex`, `Copilot`) deve redigere il proprio `MODEL_SPEC` e controller in **totale isolamento strategico**:
- Nessun cross-reading dei `MODEL_SPEC` altrui;
- Nessuna imitazione o copia di logiche di controllo proprietarie;
- Rispetto rigoroso dell'interfaccia di conformità del DLC (Sez. 20).

---

## 4. Gestione dello stash Antigravity

È presente lo stash:
`stash@{0}: On main: WIP Antigravity C2 model spec build before governance alignment`

All'avvio della sessione operativa su Antigravity:
1. Applicare `stash@{0}` (`git stash pop` o `git stash apply`);
2. Verificare la conformità di `MODEL_SPEC_ANTIGRAVITY_C2.md` rispetto al DLC congelato;
3. Verificare i test (`pytest tests/test_antigravity_c2.py`);
4. Compilare il submission artifact `submission/submission_antigravity.py` e il relativo `BUILD_VERIFICATION.md`.

---

## 5. Performance target e decomposizione

Obiettivi economici di progetto:
- `< 50,000` = failure gate di progetto;
- `50,000 – 79,999` = material improvement / target miss;
- `>= 80,000` = project target.

Requisiti metodologici post-build:
- Episode/run identity progressiva e distinta da seed/config/player position;
- Performance decomposition per specie (Wheat, Strawberry, Melon, ecc.), per risorsa e per fase biologica;
- Tracciamento separato di guasti tecnici (no-op, crash) rispetto al rendimento economico.

---

```text
STATUS:
FOUNDATION_LAYERS_1_5_FROZEN: YES
FOUNDATION_CHECKPOINT: COMPLETE
GOVERNANCE_ALIGNED: YES

NEXT_ACTION:
INDEPENDENT_AGENT_MODEL_SPEC_REVISION_AND_BUILD
```
