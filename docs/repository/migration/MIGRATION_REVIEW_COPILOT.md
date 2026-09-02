# Review pre-migrazione Copilot

- **Decisione:** `PASS_WITH_RECONCILED_METADATA`
- **Inventario canonico:** `MIGRATION_INVENTORY_COPILOT.csv`
- **Righe:** 109
- **Artefatti ownership Copilot:** 55
- **Controlli common/Codex:** 54

## Provenance della review

La prima mini-inventory Copilot da 10 righe è stata preservata integralmente
in `copilot_preflight/`. L'audit indipendente Copilot ha poi verificato un
perimetro minimo di 88 file e rilevato 78 omissioni, nove `tracked_status`
errati, tre hash mancanti e una destinazione MODEL_SPEC incompatibile con
l'albero target.

Codex, come integration owner, ha completato esclusivamente i metadati
meccanici già richiesti dall'audit: hash, tracked status e destinazioni. Il CSV
canonico contiene ora 109 righe perché include anche i deliverable di
governance comparsi durante il preflight. Le valutazioni strategiche e i
rilievi restano quelli formulati indipendentemente da Copilot.

## Rilievi confermati

1. Il MODEL_SPEC Copilot deve passare a `docs/model_specs/copilot/`.
2. Config, runtime, test, freeze, review Foundation ed evidenza E12–E17 non
   potevano essere omessi dall'inventario agent-local.
3. I replay e la Foundation sono common; la submission Codex è inclusa solo
   come controllo di integrità.
4. La freeze V2 storica esiste e deve restare tracciata anche se il MODEL_SPEC
   dichiara il contrario.
5. Il gate d'indipendenza Copilot resta `FAIL`: il controller importa la
   routine Codex. La correzione è lavoro E17.0 e non va mescolata al riordino.

## Gate A0

```text
COPILOT_INDEPENDENT_AUDIT: COMPLETE
COPILOT_METADATA_RECONCILIATION: COMPLETE
DESTINATION_COLLISIONS_IN_SUBSET: 0
FILES_MOVED: 0
POLICY_MUTATION: NONE
E17_LAUNCH: BLOCKED_PENDING_A1_A7
```
