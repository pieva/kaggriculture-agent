# KAGGRICULTURE C2 — ANTIGRAVITY RESULTS CLEANUP AND CONSOLIDATION

## Mandato

Ripulire e consolidare:

```text
results/model_spec_c2/
```

con l'obiettivo di eliminare artefatti sperimentali, prompt, report e directory ormai superati, mantenendo soltanto ciò che serve ancora come evidenza utile e tracciabile per il lavoro C2 corrente.

La directory deve diventare molto più semplice da leggere.

### Obiettivo strutturale principale

Per Antigravity deve rimanere **una sola sottodirectory**:

```text
results/model_spec_c2/antigravity/
```

Tutto ciò che ha senso conservare delle attuali directory Antigravity deve essere selezionato, consolidato e spostato lì.

Le altre directory Antigravity specialistiche/sperimentali devono essere eliminate dopo il consolidamento.

---

# 1. Safety constraints

Prima di modificare qualsiasi cosa:

```powershell
git branch --show-current
git status --short
```

Lavorare solo su:

```text
results/model_spec_c2/
```

Non modificare:

```text
docs/
src/
configs/
scripts/
submission/
tests/
```

salvo che sia strettamente necessario aggiornare un riferimento rotto dentro `results/model_spec_c2/`; in tal caso fermarsi e segnalarlo invece di modificare file esterni.

Non toccare:

```text
results/model_spec_c2/codex/
```

La directory Codex è attualmente attiva.

Non fare commit.
Non fare push.

---

# 2. Inventario iniziale obbligatorio

Prima della pulizia, produrre un inventario completo di:

```text
results/model_spec_c2/
```

Classificare ogni elemento in una delle categorie:

```text
KEEP
MERGE_INTO_ANTIGRAVITY
DELETE_OBSOLETE
DELETE_DUPLICATE
KEEP_OTHER_ACTIVE
UNCERTAIN
```

Non cancellare elementi `UNCERTAIN` finché non ne è stata verificata la funzione.

Usare contenuto, riferimenti incrociati e stato sperimentale corrente, non soltanto i nomi dei file.

---

# 3. Directory Antigravity da consolidare

Dalla situazione corrente risultano almeno directory come:

```text
antigravity/
antigravity_livestock/
antigravity_livestock_ablation/
antigravity_luccc_comparison/
antigravity_luccc_replication/
antigravity_routine_planning/
performance_iteration/
performance_tournament/
```

Verificare tutte le directory effettivamente presenti e non assumere che questo elenco sia esaustivo.

Dopo la pulizia deve rimanere soltanto:

```text
results/model_spec_c2/antigravity/
```

per tutto ciò che riguarda Antigravity C2.

---

# 4. Cosa conservare per Antigravity

Conservare soltanto artefatti che abbiano ancora valore come:

```text
current agent result
causal evidence
forensic evidence
benchmark comparison
active experiment
finalized build verification
important negative result
decision-driving evidence
```

In particolare devono essere conservate, se presenti e coerenti, le evidenze relative a:

```text
pure horticulture baseline
livestock negative/positive ablations
same-tile crop integrity
LuCcc production audit
Q0 2+2 result
Q0 3+3 replication
Q0 3+3 forensic gap analysis
routine worker planning experiment
```

Non serve mantenere ogni prompt o ogni passaggio intermedio se il relativo risultato finale è già materializzato.

---

# 5. Struttura target Antigravity

Riorganizzare in modo leggibile, preferibilmente:

```text
results/model_spec_c2/antigravity/
    README.md
    current/
    evidence/
    experiments/
```

oppure una struttura equivalente ancora più semplice se sufficiente.

Esempio consigliato:

```text
antigravity/
├── README.md
├── current/
│   ├── BUILD_VERIFICATION.md
│   └── <eventuali artefatti correnti realmente necessari>
├── evidence/
│   ├── PURE_HORTICULTURE_BASELINE.md
│   ├── LIVESTOCK_ABLATION.md
│   ├── SAME_TILE_CROP_INTEGRITY.md
│   ├── LUCCC_PRODUCTION_AUDIT.md
│   └── Q0_3X3_FORENSIC_GAP_ANALYSIS.md
└── experiments/
    ├── Q0_2PLUS2/
    ├── Q0_3X3/
    └── ROUTINE_PLANNING/
```

Non creare directory vuote o micro-directory inutili.

Se un singolo file è sufficiente, preferire il file alla directory.

---

# 6. README Antigravity

Creare/aggiornare:

```text
docs/governance/history/model_spec_c2/antigravity/README.md
```

Deve diventare l'indice canonico delle evidenze Antigravity C2.

Per ogni artefatto conservato indicare sinteticamente:

```text
purpose
status
key result
whether superseded or current
```

Esempio:

```text
Q0 3+3 replication
status: evidence
result: mean final money 37,997.67
interpretation: architecture structurally valid, crop serviceability bottleneck
```

Il README deve rendere inutile navigare directory storiche per capire la sequenza.

---

# 7. File sulla radice di results/model_spec_c2/

Pulire anche i file direttamente presenti in:

```text
results/model_spec_c2/
```

Eliminare:

```text
prompt già eseguiti
prompt duplicati
prompt superseded
report intermedi sostituiti da report finali
copie ridondanti
artifact che appartengono chiaramente ad Antigravity e sono stati consolidati
```

Mantenere sulla root soltanto artefatti realmente trasversali/canonici ancora utili.

La root non deve essere usata come archivio storico indiscriminato.

---

# 8. Directory obsolete non agent-specific

Verificare e, se superate, eliminare directory come:

```text
feedback/
tournament/
retournament/
performance_tournament/
remediation/
```

e altre directory analoghe ormai chiuse.

Per ciascuna:

1. verificare se contiene evidenza unica ancora necessaria;
2. se sì, spostare l'evidenza significativa nella directory canonica appropriata;
3. eliminare il contenitore storico.

Non mantenere directory solo perché contengono vecchi prompt o copie di risultati già assorbiti altrove.

---

# 9. Foundation revision

Trattare con maggiore cautela:

```text
foundation_revision/
```

Non eliminarla automaticamente.

Verificare se contiene freeze report/evidenze che sono ancora la prova storica del checkpoint Foundation.

Se questi artefatti sono già materializzati altrove e referenziati in governance, documentare il motivo dell'eventuale eliminazione.

Se esiste anche un minimo dubbio, conservarla.

---

# 10. periodic_model_review

Trattare con cautela:

```text
periodic_model_review/
```

Questa directory può contenere analisi Codex/LuCcc ancora utilizzate.

Non eliminarla automaticamente.

Se contiene analisi ancora referenziate dal lavoro Codex corrente, mantenerla.

Non spostare materiale Codex nella directory Antigravity.

---

# 11. Prompts

Regola generale:

```text
PROMPT EXECUTED + RESULT MATERIALIZED
→ prompt eliminabile
```

Mantenere un prompt soltanto se:

```text
è ancora operativo
non è stato eseguito
serve come protocollo sperimentale corrente
oppure il report finale dipende esplicitamente dal suo contenuto e non lo incorpora
```

Il prompt attuale della routine AG può essere conservato finché l'esperimento è in corso.

---

# 12. Duplicati

Quando due artefatti riportano sostanzialmente la stessa evidenza:

- mantenere quello più recente/completo;
- se il più recente corregge numeri del precedente, eliminare il precedente;
- riportare nel README il risultato canonico.

Esempio noto:

la forensic Q0 3+3 più recente deve prevalere sulle prime stime di decomposition se le ha corrette.

---

# 13. Non perdere i numeri canonici

Prima di eliminare artefatti, assicurarsi che rimangano materializzati almeno i principali risultati correnti Antigravity:

```text
PURE_HORTICULTURE_MEAN:
43,837.33

Q0_2PLUS2_MEAN:
24,646.67

Q0_3X3_MEAN:
37,997.67

LUCCC_EXTERNAL_SCORE:
56,772

AG_Q0_3X3_MILK:
93

AG_Q0_3X3_WOOL:
74

AG_Q0_3X3_CROP_UNITS:
24.7

LUCCC_MILK:
96

LUCCC_WOOL:
92

LUCCC_CROP_UNITS:
120

PRIMARY_GAP_CLASS:
CROP_SERVICEABILITY

Q0_3X3_ARCHITECTURE_VERDICT:
STRUCTURALLY_VALID
```

Se i numeri sono già presenti in un report canonico, non duplicarli inutilmente altrove.

---

# 14. Cross-reference check

Dopo gli spostamenti/eliminazioni:

cercare nel repository riferimenti ai path rimossi.

Esempi:

```powershell
git grep "antigravity_livestock"
git grep "antigravity_luccc"
git grep "retournament"
git grep "performance_tournament"
git grep "feedback/"
```

Se esistono riferimenti in file fuori `results/model_spec_c2/`:

- non modificarli automaticamente;
- elencarli nel report finale;
- distinguere riferimenti storici innocui da link/path realmente rotti.

---

# 15. Verifica finale filesystem

Alla fine mostrare:

```powershell
Get-ChildItem results/model_spec_c2
Get-ChildItem results/model_spec_c2/antigravity -Recurse
git status --short
git diff --check
```

Obiettivo visivo:

```text
results/model_spec_c2/
├── antigravity/
├── codex/
├── foundation_revision/        # solo se ancora necessario
├── periodic_model_review/      # solo se ancora necessario
└── pochi eventuali artefatti trasversali realmente canonici
```

Non è obbligatorio ottenere esattamente cinque elementi: è obbligatorio eliminare la struttura sperimentale frammentata e obsoleta.

---

# 16. Report finale

Creare:

```text
results/model_spec_c2/antigravity/CLEANUP_REPORT.md
```

con:

1. Before Inventory
2. Retention Criteria
3. Files Moved
4. Files Deleted
5. Directories Deleted
6. Directories Retained
7. Canonical Antigravity Evidence
8. Remaining Root Artifacts
9. External References to Removed Paths
10. Final Tree
11. Git Status
12. Final Verdict

Chiudere con:

```text
ANTIGRAVITY_SINGLE_DIRECTORY:
YES | NO

OBSOLETE_ANTIGRAVITY_DIRECTORIES_REMOVED:
YES | NO

OBSOLETE_ROOT_FILES_REMOVED:
YES | NO

OBSOLETE_FEEDBACK_REMOVED:
YES | NO | NOT_APPLICABLE

OBSOLETE_TOURNAMENT_REMOVED:
YES | NO | NOT_APPLICABLE

OBSOLETE_RETOURNAMENT_REMOVED:
YES | NO | NOT_APPLICABLE

FOUNDATION_EVIDENCE_PRESERVED:
YES | NO

CODEX_FILES_UNTOUCHED:
YES | NO

CURRENT_AG_EXPERIMENT_PRESERVED:
YES | NO

BROKEN_EXTERNAL_REFERENCES:
<number>

RESULTS_MODEL_SPEC_C2_CLEAN:
YES | PARTIAL | NO

COMMIT_AUTHORIZED:
NO

PUSH_AUTHORIZED:
NO
```

## STOP

Dopo la pulizia e il report fermarsi.

Non fare commit.
Non fare push.
Non modificare Codex.
Non modificare Foundation documentale.
Non avviare nuovi test o benchmark.
