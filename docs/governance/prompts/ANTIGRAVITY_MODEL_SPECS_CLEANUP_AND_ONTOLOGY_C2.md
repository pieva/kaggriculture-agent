# Antigravity — MODEL_SPEC cleanup + ONTOLOGY C2

## Obiettivo

Eseguire in sequenza due attività:

1. completare un piccolo riordino della directory `docs/model/model_specs/`;
2. subito dopo costruire il candidato **ONTOLOGY C2**, applicando integralmente le decisioni della Foundation Reconciliation R1.

Le due attività devono restare logicamente distinguibili. Il riordino non deve modificare la semantica dei documenti; la successiva revisione dell'Ontologia deve invece implementare i finding C2 già arbitrati.

Non eseguire nuovi episodi, benchmark, training o tuning.

---

# FASE A — Riordino finale dei MODEL_SPEC

## A1. Struttura target

La directory deve diventare:

```text
docs/model/model_specs/
│
├── antigravity/
│   ├── MODEL_SPEC_ANTIGRAVITY.md
│   └── ANTIGRAVITY_MODEL_SPEC_REVISION.md
│
├── codex/
│   ├── MODEL_SPEC_CODEX.md
│   └── CODEX_MODEL_SPEC_REVISION.md
│
├── copilot/
│   ├── MODEL_SPEC_COPILOT.md
│   ├── COPILOT_MODEL_SPEC_REVISION.md
│   └── E15_0a_OWNERSHIP_VERIFICATION_REPORT.md
│
└── POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md
```

Per il momento preservare i tre MODEL_SPEC individuali. NON consolidarli e NON sostituirli con un unico MODEL_SPEC.

## A2. Spostamenti

Eseguire preferibilmente con `git mv`:

```text
docs/model/model_specs/post_e15/ANTIGRAVITY_MODEL_SPEC_REVISION.md
→ docs/model/model_specs/antigravity/ANTIGRAVITY_MODEL_SPEC_REVISION.md

docs/model/model_specs/post_e15/CODEX_MODEL_SPEC_REVISION.md
→ docs/model/model_specs/codex/CODEX_MODEL_SPEC_REVISION.md

docs/model/model_specs/post_e15/COPILOT_MODEL_SPEC_REVISION.md
→ docs/model/model_specs/copilot/COPILOT_MODEL_SPEC_REVISION.md

docs/model/model_specs/post_e15/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md
→ docs/model_specs/history/POST_E15_CONSOLIDATED_MODEL_SPEC_FINAL.md
```

Rimuovere `docs/model/model_specs/post_e15/` quando vuota.

Per questa fase lasciare `E15_0a_OWNERSHIP_VERIFICATION_REPORT.md` nella directory Copilot. Non serve riaprire ora la classificazione di questo file.

## A3. Riferimenti

Cercare e aggiornare tutti i riferimenti canonici ai vecchi path `docs/model/model_specs/post_e15/...`.

Preservare eventuali citazioni storiche solo quando il vecchio path è parte esplicita della storia documentata e non un riferimento operativo corrente.

Aggiornare README e altri documenti correnti se necessario.

## A4. Checkpoint

Prima di passare alla Fase B verificare:

```powershell
git diff --check
git status --short
```

Non fare un commit intermedio salvo necessità tecnica. Nel report finale distinguere chiaramente le modifiche di path dalle modifiche semantiche dell'Ontologia.

---

# FASE B — Costruzione di ONTOLOGY C2

## B1. Fonti normative

Usare come base:

```text
docs/foundation/ontology/ONTOLOGY.md
docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C1.md
docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C1.md
docs/governance/foundation/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md
docs/governance/foundation/copilot/COPILOT_FOUNDATION_REVIEW_R1.md
docs/governance/foundation/reconciliation/CODEX_FOUNDATION_RECONCILIATION_R1.md
```

La **Foundation Reconciliation R1 di Codex è l'arbitrato normativo** per le modifiche C2.

Verdetto da rispettare:

```text
ONTOLOGY: REVISE_MAJOR
STATE_MACHINE_C1: REVISE_LIGHT
FEATURE_MODEL_C1: REVISE_MAJOR
MODEL_SPEC: REVISE_MAJOR
FREEZE_VERDICT: FOUNDATION_C2_REQUIRED
UNRESOLVED_EVIDENCE_GAP: NONE
```

Non riaprire dispute già risolte dalla reconciliation salvo trovare una contraddizione fattuale diretta e documentabile. In tal caso fermarsi e segnalarla, senza inventare una nuova soluzione.

## B2. Output

NON sovrascrivere immediatamente la C1.

Creare:

```text
docs/foundation/ontology/ONTOLOGY_C2.md
```

con stato esplicito:

```text
CANDIDATE C2
NOT FROZEN
DERIVED FROM FOUNDATION RECONCILIATION R1
```

`ONTOLOGY.md` deve restare disponibile come baseline C1 durante la review del candidato.

## B3. Correzioni MUST

Implementare nell'Ontologia C2 almeno i seguenti punti già arbitrati.

### 1. Inventory EOD / `contract_inventory_loss`

Correggere la semantica errata.

La meccanica engine verificata è:

- a EOD gli inventari dei worker vengono trasferiti automaticamente allo shed;
- il trasferimento avviene fino alla capacità disponibile;
- l'eccedenza viene persa;
- non esiste una necessità engine di rientro manuale del worker per evitare una presunta perdita da scadenza contrattuale.

Correggere o rinominare `contract_inventory_loss` affinché rappresenti correttamente **shed overflow at automatic EOD drop**, non un obbligo di rientro manuale.

Aggiornare relazioni e definizioni ontologiche dipendenti senza introdurre policy.

### 2. HARVEST maturity/readiness

Formalizzare semanticamente la readiness di raccolta.

Il concetto deve riflettere:

```text
tile.kind == PLANT
AND yield_units > 0
AND day - planted_day >= first_yield_day
```

Distinguere chiaramente:

```text
yield available
≠
harvest ready
```

`first_yield_day` deve entrare nel vocabolario ontologico dove semanticamente appropriato.

Non trasformare il predicato ontologico in una prescrizione di policy.

### 3. Tile lifecycle

Aggiungere/migliorare il mapping ontologico dei concetti lifecycle riusabili, coerentemente con i sei stati candidati:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

L'Ontologia deve definire significato e relazioni, non necessariamente implementare il classifier totale: il classifier eseguibile sarà responsabilità primaria del Feature/validation contract C2.

Preservare `care_due` come condizione ortogonale, non come stato strutturale del lifecycle.

### 4. DIG preventivo vs recovery

Formalizzare la distinzione semantica:

```text
preventive DIG
```

per esempio clearance pianificata di `RETIREMENT_DUE` quando necessaria nel lifecycle;

versus:

```text
recovery DIG
```

per recuperare una tile `LOST_WEED`.

Non descrivere DIG recovery come strategia primaria per cause di perdita prevenibili.

### 5. Mapping Ontology ↔ Feature Model

Allineare i concetti semanticamente riusabili emersi in C1/Codex reconciliation, in particolare maturity/readiness e lifecycle.

NON forzare una biiezione Ontologia ↔ Feature Model.

Primitive tecniche o derivazioni come `step` / `canonical_step` possono restare senza `concept_id` ontologico se non soddisfano il criterio semantico di riuso.

Documentare esplicitamente che `NONE_DIRECT` può essere legittimo.

## B4. Evidenze SHOULD già supportate

Integrare nell'Ontologia solo se soddisfano il criterio ontologico di riuso, senza trasformarle automaticamente in feature o policy:

- worker multi-occupancy engine-permitted;
- FERTILIZE: durata inclusiva `day..day+2` e bonus crop verificato;
- FEED + CARE: accumulo congiunto di `pending_care_bonus` e consumo su production day alimentato.

Economia, convenienza, marginalità e uso decisionale di queste meccaniche restano fuori dall'Ontologia se non già supportati.

## B5. Cose da NON introdurre nell'Ontologia

Non spostare nell'Ontologia responsabilità che appartengono ai livelli successivi.

In particolare NON definire qui:

- consumer matrix;
- `POLICY_INPUT | RUNTIME_DERIVED | POST_ACTION_TELEMETRY | OUTCOME_ONLY`;
- runtime trace;
- consuming function;
- formule complete degli aggregate contract;
- soglie operative;
- ranking;
- pesi;
- target crop;
- working-set policy;
- routing policy;
- cash floor;
- `serviceable_before_deadline` come fatto engine se dipende dalla policy;
- optimum economici;
- opponent strategy.

L'Ontologia deve rispondere a:

> Che cosa esiste nel dominio e che cosa significa?

non:

> Come deve decidere la policy?

## B6. Provenienza ed evidence status

Per ogni concetto nuovo o corretto indicare, coerentemente con lo stile dell'Ontologia, il livello di evidenza appropriato.

Non promuovere una conclusione oltre ciò che è stato arbitrato.

Distinguere almeno dove pertinente:

```text
ENGINE_VERIFIED
EMPIRICALLY_VERIFIED
DERIVED
PARTIALLY_KNOWN
NOT_ANALYZED
```

Le correzioni MUST sopra non richiedono nuovi episodi: Codex ha concluso `UNRESOLVED_EVIDENCE_GAP: NONE`.

## B7. Cross-artifact impact

Alla fine di `ONTOLOGY_C2.md` aggiungere una sezione:

```text
## Impatto downstream per Foundation C2
```

che elenchi esclusivamente gli aggiornamenti che i livelli successivi dovranno recepire, senza implementarli.

Separare almeno:

```text
STATE_MACHINE_C2
FEATURE_MODEL_C2
MODEL_SPEC_C2
CONSUMER MATRIX / RUNTIME TRACE
```

Esempio: l'Ontologia definisce `harvest readiness`; il Feature Model dovrà poi fornire il predicato computabile e il MODEL_SPEC dovrà dichiararne l'eventuale consumo.

---

# FASE C — Verifica

## C1. Controlli documentali

Verificare che `ONTOLOGY_C2.md`:

- non contenga path obsoleti introdotti dal riordino;
- non contraddica la Reconciliation R1;
- non trasformi feature/policy in entità engine;
- non dichiari come deterministico il random WEED timing;
- non confonda `ENGINE_OBSERVABLE` con `TELEMETRY_OBSERVED`;
- non reintroduca il falso obbligo di worker return;
- non consideri `yield_units > 0` sufficiente per HARVEST readiness.

## C2. Repository checks

Eseguire almeno:

```powershell
git diff --check
.\.venv\Scripts\pytest.exe
```

Eseguire anche `ruff` se fa parte dei check correnti del repository.

NON eseguire episodi o benchmark.

---

# FASE D — Stop prima di State Machine C2

NON iniziare autonomamente:

```text
STATE_MACHINE_C2
FEATURE_MODEL_C2
MODEL_SPEC_C2
consumer matrix
runtime implementation
policy changes
training
```

Dopo aver prodotto `ONTOLOGY_C2.md`, fermarsi.

Non congelare C2.

---

# Output finale richiesto

Restituire in italiano:

1. struttura finale di `docs/model/model_specs/`;
2. spostamenti effettuati;
3. riferimenti aggiornati;
4. path di `ONTOLOGY_C2.md`;
5. elenco dei concetti ontologici aggiunti/corretti;
6. elenco delle principali differenze C1 → C2;
7. eventuali punti lasciati `PARTIALLY_KNOWN` / `NOT_ANALYZED`;
8. downstream impact dichiarato;
9. risultato `git diff --check`;
10. risultato test/lint;
11. `git status --short`;
12. conferma:

```text
MODEL_SPEC INDIVIDUALIZATION: PRESERVED
ONTOLOGY C2: CANDIDATE CREATED
STATE MACHINE C2: NOT STARTED
FEATURE MODEL C2: NOT STARTED
MODEL_SPEC C2: NOT STARTED
FOUNDATION C2: NOT FROZEN
```

Non fare commit automaticamente. Fermarsi dopo il report, così il candidato ONTOLOGY C2 può essere revisionato prima di proseguire.
