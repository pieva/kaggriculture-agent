# Prompt operativo — Antigravity
## Riordino immediato della Model Foundation nel repository

### Contesto

La **Foundation Reconciliation R1** è stata completata da Codex con esito:

- `ONTOLOGY`: `REVISE_MAJOR`
- `STATE_MACHINE_C1`: `REVISE_LIGHT`
- `FEATURE_MODEL_C1`: `REVISE_MAJOR`
- `MODEL_SPEC`: `REVISE_MAJOR`
- `FREEZE_VERDICT`: `FOUNDATION_C2_REQUIRED`
- `UNRESOLVED_EVIDENCE_GAP`: `NONE`

La Foundation C1 **non è congelata**. Prima di iniziare la revisione C2 vogliamo eliminare l'attuale dispersione dei documenti della Model Foundation nel repository.

L'obiettivo di questo task è **solo repository governance / riordino dei path**.

NON modificare contenuti concettuali, semantici o tecnici della Foundation C1.
NON implementare ancora le correzioni C2 emerse dalla reconciliation.
NON eseguire episodi, benchmark, training o nuovi esperimenti.

---

# 1. Obiettivo

Portare tutta la documentazione strutturale della Model Foundation sotto un unico root canonico:

```text
docs/model/
```

Attualmente i materiali sono dispersi almeno fra:

```text
docs/model/
docs/model_specs/
results/foundation_review/
```

Dopo il riordino, `docs/model/` deve diventare la sede canonica di:

1. Ontologia
2. State Machine
3. Feature Model
4. MODEL_SPEC
5. review indipendenti Foundation
6. reconciliation Foundation
7. eventuali consumer matrix / validation contract futuri

`results/` deve restare destinato a risultati sperimentali, diagnostica, telemetry, benchmark, freeze artifacts e altri output di esecuzione, non alla documentazione strutturale della Foundation.

---

# 2. Struttura target

Adotta come struttura canonica:

```text
docs/model/
│
├── ontology/
│   └── ONTOLOGY.md
│
├── state_machine/
│   └── KAGGRICULTURE_STATE_MACHINE_C1.md
│
├── feature_model/
│   └── KAGGRICULTURE_FEATURE_MODEL_C1.md
│
├── model_specs/
│   ├── antigravity/
│   │   └── ...
│   ├── codex/
│   │   └── ...
│   ├── copilot/
│   │   └── ...
│   └── post_e15/
│       └── ...
│
└── reviews/
    ├── antigravity/
    │   ├── ANTIGRAVITY_FOUNDATION_REVIEW_R1.md
    │   └── ANTIGRAVITY_FOUNDATION_EVIDENCE_MATRIX.csv
    ├── copilot/
    │   └── COPILOT_FOUNDATION_REVIEW_R1.md
    └── reconciliation/
        └── CODEX_FOUNDATION_RECONCILIATION_R1.md
```

Se esistono altri file Foundation chiaramente appartenenti a questi insiemi, spostali nella sottodirectory semanticamente corretta.

Non creare copie parallele: usare `git mv` quando possibile.

---

# 3. File da ricollocare

## 3.1 Da `docs/model/`

Spostare:

```text
docs/model/KAGGRICULTURE_STATE_MACHINE_C1.md
→ docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C1.md

docs/model/KAGGRICULTURE_FEATURE_MODEL_C1.md
→ docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C1.md
```

## 3.2 Da `docs/model_specs/`

Spostare l'intero contenuto strutturale della directory sotto:

```text
docs/model/model_specs/
```

Inclusi almeno:

```text
docs/model_specs/ONTOLOGY.md
docs/model_specs/antigravity/
docs/model_specs/codex/
docs/model_specs/copilot/
docs/model_specs/post_e15/
```

MA `ONTOLOGY.md` deve terminare in:

```text
docs/foundation/ontology/ONTOLOGY.md
```

e non dentro `model_specs/`.

La directory originaria `docs/model_specs/` deve risultare vuota e quindi rimossa.

## 3.3 Da `results/foundation_review/`

Spostare:

```text
results/foundation_review/antigravity/
→ docs/model/reviews/antigravity/

results/foundation_review/copilot/
→ docs/model/reviews/copilot/

results/foundation_review/reconciliation/
→ docs/model/reviews/reconciliation/
```

La directory `results/foundation_review/` deve essere rimossa se, a migrazione completata, non contiene altro materiale che debba legittimamente restare in `results/`.

---

# 4. Reconciliation da preservare integralmente

Il file:

```text
CODEX_FOUNDATION_RECONCILIATION_R1.md
```

è l'arbitrato canonico da cui partirà la Foundation C2.

Deve essere spostato senza modifiche semantiche in:

```text
docs/governance/foundation/reconciliation/CODEX_FOUNDATION_RECONCILIATION_R1.md
```

Non alterare finding, classificazioni, verdict o testo tecnico.

Il verdetto da preservare è:

```text
FOUNDATION_C2_REQUIRED
UNRESOLVED_EVIDENCE_GAP: NONE
```

---

# 5. Aggiornamento riferimenti

Dopo i `git mv`, cercare sistematicamente nel repository tutti i riferimenti ai vecchi path:

```text
docs/model_specs/
docs/model/KAGGRICULTURE_STATE_MACHINE_C1.md
docs/model/KAGGRICULTURE_FEATURE_MODEL_C1.md
results/foundation_review/
```

Aggiornare i riferimenti ai nuovi path in:

- `README.md`
- documentazione Foundation
- prompt operativi
- review
- reconciliation
- script diagnostici/audit
- eventuali test
- `PROJECT_STATE.md`
- `NEW_SESSION.md`
- `EXPERIMENT_LOG.md`
- altri Markdown, CSV, JSON o codice che usino path letterali.

Distinguere fra riferimenti operativi/canonici correnti, che DEVONO essere aggiornati, e citazioni storiche che descrivono esplicitamente un path usato in passato, che possono restare se il loro significato storico dipende dal vecchio path.

Non riscrivere indiscriminatamente il contenuto storico.

---

# 6. README

Aggiornare la sezione **Model Foundation** del `README.md` affinché mostri i nuovi path canonici.

La lettura strutturale deve risultare immediata:

```text
docs/model/
├── ontology/
├── state_machine/
├── feature_model/
├── model_specs/
└── reviews/
```

Preservare la distinzione concettuale:

```text
ONTOLOGY
    ↓
STATE MACHINE
    ↓
FEATURE MODEL
    ↓
MODEL_SPEC
    ↓
POLICY / RUNTIME
```

Il riordino fisico non deve trasformare le review in un quinto artefatto del modello: `reviews/` è governance/evidence review della Foundation.

---

# 7. Vincoli importanti

NON:

- implementare C2;
- correggere `ONTOLOGY`, State Machine, Feature Model o MODEL_SPEC in base ai finding;
- cambiare formule;
- introdurre consumer matrix nuove;
- implementare classifier lifecycle;
- cambiare clock contract;
- modificare policy/runtime/config;
- eseguire nuovi episodi;
- eseguire benchmark Kaggle;
- fare tuning;
- ripristinare le cancellazioni intenzionali già presenti sotto `docs/experiments/`, `docs/plans/`, `docs/walkthroughs/`;
- inglobare nel commit file E16 o script non collegati a questo riordino;
- usare `git add .`.

Questo task deve restare un **commit di repository reorganization** chiaramente separato dalla futura Foundation C2.

---

# 8. Working tree attuale da rispettare

Sono già presenti cancellazioni intenzionali non ancora committate sotto:

```text
docs/experiments/
docs/plans/
docs/walkthroughs/
```

NON revertirle e NON includerle automaticamente nel commit del riordino.

Sono inoltre untracked altri artefatti E16/prompt/script:

```text
docs/model_specs/codex/archive/e16/prompts/E16_A_R1_CODEX_FORENSIC_DIAGNOSIS_PROMPT.md
docs/model_specs/codex/archive/e16/prompts/E16_CODEX_TILE_LIFECYCLE_FEATURE_AUDIT.md
results/e16/diagnostics/
experiments/archive/e01/tools/audit_e16_tile_lifecycle_feature.py
experiments/archive/e01/tools/diagnose_e16_a_r1_crop_attainment.py
```

NON includerli nel commit salvo che un riferimento testuale ai nuovi path richieda una modifica strettamente necessaria. In quel caso fermati e segnala il problema prima di stage/commit.

Il prompt:

```text
docs/governance/prompts/CODEX_FOUNDATION_RECONCILIATION_R1_PROMPT.md
```

può essere aggiornato solo se contiene path Foundation diventati invalidi, ma resta un artefatto storico-operativo: non riscriverne il contenuto metodologico.

---

# 9. Verifiche obbligatorie

Prima di qualsiasi commit eseguire:

```powershell
git status --short
git diff --check
```

Poi verificare i vecchi path con ricerche equivalenti a:

```powershell
git grep -n "docs/model_specs/"
git grep -n "results/foundation_review/"
git grep -n "docs/model/KAGGRICULTURE_STATE_MACHINE_C1.md"
git grep -n "docs/model/KAGGRICULTURE_FEATURE_MODEL_C1.md"
```

Interpretare manualmente eventuali match storici prima di modificarli.

Eseguire inoltre la test suite esistente:

```powershell
.\.venv\Scripts\pytest.exe
```

Se sono disponibili check lint già standardizzati nel progetto, eseguirli.

Il riordino non deve cambiare comportamento runtime.

---

# 10. Stage selettivo

NON usare:

```powershell
git add .
```

Usare staging selettivo soltanto dei file interessati alla migrazione e agli aggiornamenti di path.

Prima del commit mostrare:

```powershell
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
```

Verificare che le cancellazioni storiche intenzionali e gli artefatti E16 non correlati non siano staged.

---

# 11. Commit

Se tutte le verifiche sono verdi, creare un commit dedicato con messaggio:

```text
Reorganize Model Foundation repository structure
```

Poi:

```powershell
git status --short
git log -1 --oneline
```

NON fare altre modifiche dopo il commit.

---

# 12. Output finale richiesto

Restituire un report conciso in italiano con:

1. struttura finale di `docs/model/`;
2. elenco dei `git mv` principali;
3. riferimenti aggiornati;
4. eventuali vecchi path rimasti intenzionalmente per ragioni storiche;
5. risultato `git diff --check`;
6. risultato test;
7. elenco esatto dei file inclusi nel commit;
8. commit SHA;
9. `git status --short` residuo;
10. conferma esplicita:

```text
FOUNDATION CONTENT CHANGES: NONE
FOUNDATION C2 IMPLEMENTATION: NOT STARTED
REPOSITORY REORGANIZATION: COMPLETED
```

Dopo questo report, STOP.
