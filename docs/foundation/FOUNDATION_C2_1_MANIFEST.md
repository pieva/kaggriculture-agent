# Manifest della Foundation

Questo indice identifica le descrizioni correnti del dominio e ne registra
gli hash per verificarne l’integrità. Non contiene il piano di sviluppo delle policy.
La [guida di lettura](README.md) spiega il ruolo di ciascun documento.

## Documenti correnti

| Documento | File | SHA-256 |
|---|---|---|
| ENGINE_CONTRACT.md | `ENGINE_CONTRACT.md` | `34EDFE102B7FB5949F1189029978138A375BB76A0BF27E474AAA1F9CEACC4CB8` |
| ontology/ONTOLOGY_C2_1.md | `ontology/ONTOLOGY_C2_1.md` | `63C6BF13D03C0376C49AB589B69190DB626868D759CBFE3BB7ED1A1927D2FF82` |
| state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md | `state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md` | `954E943E16C816204C63CADC566847C6DA51E90A139E5DF5BB3FCD735869BE0E` |
| feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md | `feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md` | `80A5600CC086259484ABC84BE4AC2582473789ADF6D3D094EA17418649C136D2` |
| feature_model/FEATURE_CATALOG.md | `feature_model/FEATURE_CATALOG.md` | `EBA5BD23955E1C858F7770FA1F0A112FE0C96127CB7660B185A36003677BBF2F` |

## Fonti e confini

Le fonti effettivamente lette per l’engine sono identificate in
[ENGINE_SOURCE_MANIFEST.json](ENGINE_SOURCE_MANIFEST.json). Il contratto
osservativo del progetto è in [observation_contract.py](../../src/agricola/core/observation_contract.py).
Quest’ultimo normalizza osservazioni, clock e snapshot; non definisce una strategia.

I modelli condividono concetti, regole e definizioni delle misure. Planner,
priorità e routine appartengono alle MODEL_SPEC. La revisione editoriale
non modifica engine o policy e non costituisce una nuova certificazione incrociata.

## Archivio e provenienza

- [Copie precedenti e manifest dei loro hash](../governance/history/foundation_documentation_20260908/README.md).
- [Verbale storico di riconciliazione dell’engine](../governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md).
- [Inventario degli artefatti conservati localmente](evidence/LOCAL_ARTIFACTS_20260908.json).

Le vecchie copie C1/C2 e le evidenze di ambiente sono conservate per audit;
non sostituiscono i documenti correnti elencati sopra.
