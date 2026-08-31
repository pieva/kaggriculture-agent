# ANTIGRAVITY — FOUNDATION CONSOLIDATION PASS PROMPT

## 0. Mandato

Esegui come **unico Consolidation Agent** il pass di consolidamento della Model Foundation Kaggriculture Cycle 2.

La fonte operativa primaria è:

```text
results/model_spec_c2/foundation_cross_review/
FOUNDATION_CROSS_REVIEW_RECONCILIATION.md
```

Applica esclusivamente i finding e le correzioni canoniche approvate dalla reconciliation, con le integrazioni obbligatorie definite in questo prompt.

Questa non è una nuova review e non è autorizzata alcuna progettazione del `MODEL_SPEC`.

---

## 1. Input normativi

Leggi prima di modificare qualsiasi file:

```text
results/model_spec_c2/foundation_cross_review/
FOUNDATION_CROSS_REVIEW_RECONCILIATION.md

docs/model/ontology/ONTOLOGY_C2.md

docs/model/state_machine/
KAGGRICULTURE_STATE_MACHINE_C2.md

docs/model/feature_model/
KAGGRICULTURE_FEATURE_MODEL_C2.md
```

Usa come autorità superiore:

```text
Frozen Runtime / Source
Frozen Engine Contract
Frozen Period Ledger / verified Engine audit
```

Fingerprint:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

Gerarchia:

```text
RUNTIME/SOURCE
    ↓
ENGINE CONTRACT
    ↓
PERIOD LEDGER / VERIFIED AUDIT
    ↓
RECONCILIATION
    ↓
FOUNDATION DOCUMENTS
```

---

## 2. Scope autorizzato

Sei autorizzato a:

1. applicare il Foundation Correction Set riconciliato;
2. correggere coerentemente:
   - `ONTOLOGY_C2.md`;
   - `KAGGRICULTURE_STATE_MACHINE_C2.md`;
   - `KAGGRICULTURE_FEATURE_MODEL_C2.md`;
3. aggiornare `README.md` per riflettere la nuova architettura;
4. razionalizzare `results/model_spec_c2/foundation_revision/` secondo le regole di questo prompt;
5. produrre un report finale di consolidation e verifica documentale.

NON sei autorizzato a:

```text
creare Decision Lifecycle Contract
creare/modificare MODEL_SPEC
modificare codice agente
eseguire benchmark
eseguire tournament
eseguire Kaggle
```

---

# 3. Applicazione CORR-01 .. CORR-12

Applica integralmente:

```text
CORR-01 .. CORR-12
```

definite in `FOUNDATION_CROSS_REVIEW_RECONCILIATION.md`.

Non reinterpretarle strategicamente.

Dove una CORR coinvolge più file, correggi tutti i layer necessari affinché la semantica finale sia reciproca.

---

# 4. Integrazione obbligatoria — CORR-13

## ACTION REQUEST / ELIGIBILITY / EXECUTION / POST-STATE EVIDENCE

La reconciliation ha confermato:

```text
CAN-FND-P1-03
```

ma il Correction Set non lo ha materializzato in una CORR dedicata.

Aggiungi quindi:

```text
CORR-13
```

### Target

```text
ONTOLOGY_C2.md
KAGGRICULTURE_FEATURE_MODEL_C2.md
```

e, dove necessario per coerenza semantica:

```text
KAGGRICULTURE_STATE_MACHINE_C2.md
```

### Required change

Formalizza quattro fasi epistemicamente distinte:

```text
ACTION_REQUEST
SNAPSHOT_ELIGIBILITY
EXECUTION_OUTCOME
POST_STATE_EVIDENCE
```

Semantica:

```text
ACTION_REQUEST
= intenzione/comando formulato a partire da S_t

SNAPSHOT_ELIGIBILITY
= legalità/fattibilità derivabile dallo snapshot S_t
  prima dell'esecuzione

EXECUTION_OUTCOME
= risultato effettivo dell'engine:
  SUCCESS / NO_OP / REJECTED / altro esito engine verificato

POST_STATE_EVIDENCE
= evidenza osservata nel nuovo stato risultante
```

Preservare:

```text
STATE_t
  → ACTION_REQUEST_t
  → engine processing
  → EXECUTION_OUTCOME_t
  → STATE_t+1
  → POST_STATE_EVIDENCE_t+1
```

Non classificare execution outcome o post-state evidence come disponibili prima della transizione.

### Acceptance check

- nessun flow combina più intent ed execution outcome senza distinzione temporale;
- no-future-leakage verificabile;
- il futuro Decision Lifecycle potrà usare queste quattro classi senza ridefinirle.

---

# 5. Integrazione obbligatoria — CORR-14

## GLOBAL TRANSITION / EOD / TERMINAL SEMANTICS

La reconciliation ha confermato:

```text
CAN-FND-P1-04
```

ma il Correction Set non lo ha materializzato in una CORR dedicata.

Aggiungi:

```text
CORR-14
```

### Target

```text
KAGGRICULTURE_STATE_MACHINE_C2.md
ONTOLOGY_C2.md
```

e Feature Model se contiene feature/predicati terminali dipendenti.

### Required change

Allinea:

- ordine globale della transizione;
- posizione dell'EOD nella transizione che produce il nuovo stato;
- temporal indexing;
- terminal predicate;
- final-state semantics;

all'esatto runtime frozen.

Non utilizzare una semplificazione del tipo:

```text
step == episodeSteps
```

se non corrisponde esattamente al runtime.

### Acceptance check

- una sola convenzione temporale canonica;
- nessun off-by-one;
- EOD collocato correttamente nella transizione engine;
- terminal predicate documentato con la semantica esatta del runtime frozen;
- replay `state-action-state` non ambiguo.

---

# 6. Raffinamento obbligatorio — CORR-05

La reconciliation proponeva per `POST-08`:

```text
registra zero spesa cassa diretta
```

Non mantenere una metrica monetaria artificiale che registra sistematicamente zero.

Dato che nel runtime frozen:

```text
BUILD_COOP
BUILD_PASTURE
```

non hanno costo monetario diretto:

- elimina qualsiasi `structure_construction_cost` presentato come costo engine;
- rimuovi guardie di cassa e deduzioni monetarie associate;
- se serve telemetry sulle strutture, usa metriche neutrali quali:
  - numero di strutture costruite;
  - tipo;
  - tile occupancy;
  - timing;
  - worker/action usage;
- non trasformare occupancy o worker effort in costo monetario senza una regola esplicita agent-specific o un'analisi post-hoc.

---

# 7. Stato dei gate durante il consolidation

Non descrivere come già `VALIDATED` una proprietà che dipende dalle correzioni ancora in corso.

Durante l'editing usa:

```text
PENDING_CORRECTION
```

o:

```text
PENDING_VERIFICATION
```

per:

```text
ENGINE_ALIGNMENT
CROSS_LAYER_ALIGNMENT
POLICY_NEUTRALITY
NO_FUTURE_LEAKAGE
PERFORMANCE_ACCOUNTING
PROVENANCE
```

Solo dopo avere applicato e verificato tutte le correzioni puoi proporre `PASS`.

---

# 8. Tassonomie canoniche

Durante il consolidation verifica l'allineamento esatto delle tassonomie Foundation.

In particolare non introdurre sinonimi locali non dichiarati.

La tassonomia epistemica/di provenance deve essere coerente con quella Foundation approvata.

Verifica almeno:

```text
ENGINE_FACT
DERIVED_ENGINE_FACT
POLICY_CONTEXT
POST_HOC_METRIC
```

Evidence status:

```text
ENGINE_VERIFIED
EMPIRICALLY_VERIFIED
DERIVED
POLICY_DECLARED
PARTIALLY_KNOWN
```

Observability:

```text
ONLINE_OBSERVABLE
ONLINE_DERIVABLE
TELEMETRY_ONLY
ENGINE_INTERNAL
OUTCOME_ONLY
```

Se valori precedenti quali:

```text
ENGINE_STATE
RAW_OBSERVABLE
ACTION_BATCH_CONTEXT
POLICY_CONTEXT come observability
POST_HOC_METRIC come evidence_status
```

sono usati impropriamente, riallineali alla tassonomia canonica senza perdere la distinzione semantica necessaria.

---

# 9. Tile lifecycle

Applicando CORR-07, rendi coerente ovunque la partizione ambientale:

```text
OUT_OF_SCOPE
LOST_WEED
EMPTY_AVAILABLE
HARVEST_READY
GROWING
```

Working-set assignment e retirement rimangono overlay agent/policy:

```text
in_working_set
policy_retirement_due
```

Non devono diventare environment states.

---

# 10. Capacity

Applicando CORR-01 e le altre correzioni:

- elimina worker carrying capacity inesistente;
- non ridurre la capacità zootecnica a un unico numero se la compatibilità dipende da struttura/specie/output;
- mantieni separate le dimensioni strutturali e operative;
- `max_held` appartiene alla capacità di output della tile animale per specie.

---

# 11. Performance accounting

Separare esplicitamente:

```text
DIRECT ACCOUNTING
DESCRIPTIVE DIAGNOSTICS
CAUSAL / COUNTERFACTUAL ANALYSIS
```

## Wheat

L'identità fisica deve usare soltanto unità fisiche omogenee.

Non usare:

```text
wheat_market_purchase_cost_total
```

come quantità acquistata.

Se necessario materializza una metrica distinta:

```text
wheat_purchased_units
```

e conserva separatamente:

```text
wheat_market_purchase_cost_total
```

in valuta.

Il bilancio deve considerare correttamente stock e flussi effettivamente rappresentabili dal runtime.

## Fertilizer

Il flag:

```text
fertilizer_available
```

è booleano/non cumulativo.

Non contare come nuova unità una transizione che lascia `True → True`.

---

# 12. Policy neutrality

Rimuovi dalla Foundation ogni prescrizione strategica confermata dalla reconciliation.

In particolare:

```text
operating_cash_buffer
feed_security_buffer
deployable_capital_window
endgame shutdown/liquidation
working-set selection rule
livestock-capacity policy
retirement trigger
```

possono essere:

- rimossi;
- oppure rappresentati esclusivamente come generic agent-declared context/envelope,

ma non devono avere valori, soglie o regole comuni.

---

# 13. Provenance

Materializza almeno:

```text
run_id
episode_id
(run_id, episode_id) documented identity
seed
agent_id
model_spec_version
foundation_version
player_position
opponent identity/configuration
engine/environment fingerprint
configuration_snapshot
configuration_hash
feature_schema_version
telemetry_schema_version
transition/event ordering identity
```

Il fingerprint del codice engine NON sostituisce il configuration hash.

Mantieni la numerazione progressiva degli episodi compatibile con confronti longitudinali.

---

# 14. README — aggiornamento autorizzato

Ora il README può essere aggiornato.

Deve descrivere chiaramente:

```text
MODEL FOUNDATION
├── Engine Contract
├── Ontology
├── Environment State Machine
├── Feature Model
└── Decision Lifecycle Contract

        ↓

AGENT-SPECIFIC MODEL_SPEC
├── Antigravity MODEL_SPEC
├── Codex MODEL_SPEC
└── Copilot MODEL_SPEC
```

Specificare:

```text
C2 = Cycle 2
```

come identificatore del ciclo di revisione/provenance e non come layer architetturale.

Chiarire inoltre:

```text
environment truth
deterministic derivation
policy context
action request
execution outcome
post-state evidence
post-hoc telemetry
```

Non descrivere il `Decision Lifecycle Contract` come già scritto o frozen.

Deve risultare:

```text
ARCHITECTURAL_LAYER_APPROVED
DOCUMENT_NOT_YET_CREATED/FROZEN
```

---

# 15. Pulizia foundation_revision

Razionalizza:

```text
results/model_spec_c2/foundation_revision/
```

solo dopo avere completato le correzioni e verificato che i file necessari siano conservati altrove o nel loro path canonico.

Conservare obbligatoriamente gli artefatti normativi/provenance ancora necessari, inclusi:

```text
ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

e il report di reconciliation nel suo path canonico:

```text
results/model_spec_c2/foundation_cross_review/
FOUNDATION_CROSS_REVIEW_RECONCILIATION.md
```

Rimuovere/archiviare soltanto prompt e pass intermedi chiaramente superati.

Prima di cancellare:

- verificare che il file non sia l'unica copia di evidenza normativa;
- verificare riferimenti da README/report/manifest;
- evitare broken references;
- documentare nel consolidation report cosa è stato mantenuto, spostato o rimosso.

Non cancellare i tre report indipendenti di cross-review: costituiscono provenance della reconciliation.

---

# 16. Mermaid e diagrammi

Qualsiasi diagramma Mermaid modificato deve:

- rimanere nel file Markdown;
- essere sintatticamente renderizzabile;
- rappresentare la semantica finale;
- non essere sostituito con PNG/JPG o altra figura generata.

Verifica in particolare:

- State Machine;
- separazione Environment Feature Vector / Policy Context;
- nuova architettura nel README, se resa con Mermaid.

---

# 17. Verifica finale

Dopo le modifiche esegui una verifica documentale completa:

```text
git diff --check
git status --short
```

e i controlli disponibili per:

- riferimenti/ID;
- duplicate IDs;
- dangling mappings;
- Mermaid syntax/renderability;
- tassonomie;
- raw observation paths;
- hard-coded engine constants;
- dimensional consistency;
- policy leakage;
- no-future leakage;
- provenance.

Se esistono test documentali già presenti nel repository, eseguili.

Non creare nuovi test runtime/build salvo che siano strettamente necessari per verificare i documenti e non modifichino il prodotto.

---

# 18. Output

Crea:

```text
results/model_spec_c2/foundation_cross_review/
FOUNDATION_CONSOLIDATION_REPORT.md
```

Struttura:

```text
1. Executive Verdict
2. Inputs and Normative Authority
3. Applied Corrections CORR-01..CORR-14
4. Ontology Consolidation
5. State Machine Consolidation
6. Feature Model Consolidation
7. Cross-Layer Alignment
8. Engine Alignment Verification
9. Policy-Neutrality Verification
10. No-Future-Leakage Verification
11. Performance Accounting Verification
12. Provenance Verification
13. README Architecture Update
14. foundation_revision Cleanup
15. Files Changed
16. Verification Commands / Results
17. Residual Risks
18. Final Gate
```

---

# 19. Final Gate

Terminare con:

```text
CORR_01_14_APPLIED:
ENGINE_CONTRACT_ALIGNMENT:
ONTOLOGY_STATE_MACHINE_ALIGNMENT:
STATE_MACHINE_FEATURE_MODEL_ALIGNMENT:
ONTOLOGY_FEATURE_MODEL_ALIGNMENT:

EPISTEMIC_TAXONOMY_ALIGNMENT:
POLICY_NEUTRALITY:
NO_FUTURE_LEAKAGE:
ACTION_EVIDENCE_SEPARATION:
PERFORMANCE_ACCOUNTING:
PROVENANCE:
MERMAID_RENDERABILITY:

README_ARCHITECTURE_ALIGNED:
FOUNDATION_REVISION_CLEANUP_COMPLETE:

P0_OPEN:
P1_OPEN:
P2_OPEN:

FOUNDATION_CONSOLIDATION:
FOUNDATION_FREEZE_RECOMMENDED:
DECISION_LIFECYCLE_REQUIREMENTS_READY:

DECISION_LIFECYCLE_DRAFTING_AUTHORIZED: NO
MODEL_SPEC_REVISION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Anche se:

```text
FOUNDATION_FREEZE_RECOMMENDED = YES
```

non dichiarare autonomamente il freeze.

Il freeze finale verrà deciso dopo la review del consolidation report.

---

# 20. Stop condition

Dopo avere:

1. applicato CORR-01..CORR-14;
2. riallineato i tre artefatti Foundation;
3. aggiornato README;
4. razionalizzato `foundation_revision/`;
5. verificato Mermaid e riferimenti;
6. creato `FOUNDATION_CONSOLIDATION_REPORT.md`;
7. eseguito i controlli finali;

**FERMATI.**

Non creare il Decision Lifecycle Contract.
Non modificare alcun MODEL_SPEC.
Non modificare il controller.
Non avviare build, benchmark, tournament o Kaggle.
