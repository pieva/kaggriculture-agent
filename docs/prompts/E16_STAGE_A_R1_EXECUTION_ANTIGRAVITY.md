# E16-A-R1 — CORRECTED REPLICATION EXECUTION — ANTIGRAVITY

## Ruolo

Agisci come **execution operator** della corrected replication `E16-A-R1`.

Il disegno sperimentale è già congelato e il repair è già stato completato e validato.

Il tuo compito è:

1. verificare il checkpoint post-repair;
2. eseguire esattamente i 28 episodi `E16-A-R1`;
3. preservare integralmente la provenance dei 28 run originali;
4. usare esclusivamente la build/config R1 corrette;
5. rieseguire l'analisi Stage A sul dataset R1;
6. calcolare il nuovo gate `C*`;
7. fermarti prima di Stage B.

Non sei autorizzato a modificare il DOE, cambiare parametri, fare tuning o correggere codice durante l'esecuzione.

---

# 1. LEGGI PRIMA DI AGIRE

Leggi integralmente:

```text
docs/experiment_designs/e16/E16_TRAINING_DESIGN_FROZEN.md
docs/experiment_designs/e16/E16_IMPLEMENTATION_REPAIR_SPEC.md
docs/experiment_designs/e16/E16_WATERING_SEMANTICS_CLARIFICATION.md
results/e16/manifests/E16_IMPLEMENTATION_MANIFEST.json
results/e16/instrumentation/E16_E0_REPORT.md
configs/e16/E16_R1_FROZEN_CONFIG.json
```

Poi ispeziona, senza modificarli:

```text
results/e16/manifests/E16_TREATMENT_BUILD_R1.py
scripts/run_e16_training.py
scripts/analyze_e16_stage_a.py
src/agricola/e16/
tests/test_e16_*.py
```

Usa esclusivamente le interfacce effettivamente implementate nel repository.

---

# 2. CHECKPOINT OBBLIGATORIO

Prima di qualsiasi run verifica:

```text
REPAIR_STATUS = READY
SEMANTIC_CLARIFICATION_APPLIED = YES

R1_WATERING_SEMANTICS = PASS
R2_LEDGER_ATTRIBUTION = PASS
R3_DERIVED_METRICS = PASS

TESTS = 143/143

E0_STATUS = PASS

ORIGINAL_STAGE_A_PRESERVED = YES
E16_A_R1_READY = YES
BLOCKERS = NONE
```

Verifica esattamente:

```text
NEW_TREATMENT_BUILD_SHA256 =
7f331511a235e409833a726a324a4cda9881f3c8836a1ee260a2d6f36b78e1a8

NEW_CONFIG_SHA256 =
f37496d1653cfc78672632c7fb779fc07ee93897a22341cf54f2242290e9f199

OPPONENT_SHA256 =
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Se uno degli hash non corrisponde:

```text
STOP
STATUS = BLOCKED_HASH_MISMATCH
```

Non ricostruire automaticamente gli artifact per forzare la corrispondenza.

---

# 3. PRESERVAZIONE DELL'ORIGINALE

I 28 episodi Stage A originali devono restare immutati.

NON modificare:

```text
results/e16/stage_a/
```

La corrected replication usa esclusivamente:

```text
results/e16/stage_a_r1/
```

Verifica prima del run che:

```text
original Stage A files unchanged
R1 manifest = PLANNED_NOT_RUN oppure equivalente pre-run
R1 completed training episodes = 0
```

Se risultano già presenti episodi R1 completati:

```text
STOP
STATUS = BLOCKED_EXISTING_R1_EVIDENCE
```

Non duplicare né sovrascrivere run.

---

# 4. FREEZE ASSOLUTO DURANTE R1

Durante l'esecuzione non modificare:

```text
src/agricola/e16/**
configs/e16/E16_R1_FROZEN_CONFIG.json
results/e16/manifests/E16_TREATMENT_BUILD_R1.py
opponent E15 frozen
seed
seat protocol
cell definitions
telemetry semantics
analysis formulas
Stage B gate
```

Non fare tuning.

Non fare bug fixing durante il training.

Non cambiare parametri in risposta ai risultati.

Non sostituire run negativi.

Non eliminare outlier.

Non aggiungere seed.

Non avviare submission Kaggle.

Se emerge un problema di implementazione:

```text
STOP
preserva tutti i risultati R1 già prodotti
documenta il problema
non correggere e riprendere autonomamente
```

---

# 5. SEMANTICA WATER R1

La semantica canonica è:

```text
watering_dispatch_priority
```

= priorità relativa di dispatch delle azioni WATER rispetto alle altre azioni concorrenti.

NON è:

```text
coverage target
percentuale di crop da irrigare
fixed-prefix quota
```

Mantieni distinti:

```text
watering_dispatch_priority   # trattamento controllato
watering_execution_rate      # metrica osservata
watering_continuity          # metrica osservata
```

Valori frozen:

```text
LOW  = 0.20
MID  = 0.45
HIGH = 0.70
```

---

# 6. STAGE A-R1 FROZEN

Le celle restano esattamente:

```text
A01 = watering LOW  0.20 × crop target 10
A02 = watering HIGH 0.70 × crop target 10

A03 = watering LOW  0.20 × crop target 25
A04 = watering HIGH 0.70 × crop target 25

A05 = watering MID  0.45 × crop target 17
A06 = watering MID  0.45 × crop target 25
A07 = watering HIGH 0.70 × crop target 17
```

Controls:

```text
quadrants_owned = 2
livestock_headcount_target = 4
pasture_allocation_target = 5
workforce_headcount = 10
livestock_species = Cow
opponent = Copilot E15 frozen
```

---

# 7. SEED E SEAT

Usa esclusivamente:

```text
1802163452
1678077158
```

Per ogni cella e seed:

```text
treatment P0 / opponent P1
opponent P0 / treatment P1
```

Totale atteso:

```text
7 cells × 2 seeds × 2 seats = 28 episodes
```

Né 27 né 29.

Gameplay failure o disqualification:

```text
retain as outcome
NO replacement
NO automatic rerun
```

Infrastructure failure può essere ripetuto solo secondo la rerun policy frozen e con identica configurazione.

---

# 8. ESECUZIONE

Prima esegui:

```text
pytest tests/test_e16_*.py
```

o il comando equivalente previsto dall'ambiente.

Poi esegui Stage A-R1 completo usando il runner ufficiale e la config R1.

Non interpretare i risultati dopo singole celle.

Non fermare celle che performano male.

Non cambiare ordine o protocollo in base a `final_money`.

Al termine verifica che il manifest contenga esattamente 28 episodi e che ciascuno includa almeno:

```text
cell_id
seed
treatment_seat
treatment_build_sha256
opponent_sha256
configuration_sha256
completion/failure status
telemetry provenance
```

---

# 9. INTEGRITY CHECK POST-RUN

Prima dell'analisi verifica:

```text
expected episodes = 28
observed episodes = 28
unexpected seeds = 0
unexpected cells = 0
missing seat swaps = 0

treatment hash mismatches = 0
opponent hash mismatches = 0
config hash mismatches = 0

post-freeze policy changes = 0
original Stage A mutations = 0
```

Verifica inoltre:

```text
no attributable unit-action has player = -1
watering metrics are finite or explicitly marked unavailable
treatment/opponent telemetry separation is correct
```

Riporta esplicitamente gameplay failures/disqualifications.

Se l'integrità strutturale non è rispettata:

```text
ANALYSIS_STATUS = BLOCKED
```

e fermati.

---

# 10. ANALISI R1

Esegui l'analisi Stage A usando esclusivamente i dati `stage_a_r1`.

Non mescolare i 28 run originali con R1.

Produci almeno:

```text
A02 - A01
A04 - A03

(A04 - A03) - (A02 - A01)

A03 -> A06 -> A04
A02 -> A07 -> A04

A05 vs A07
A05 vs corner interpolation
```

Mostra raw values per seed/seat oltre alle sintesi.

Mantieni distinti:

```text
MODEL_VALIDITY
POLICY_REALIZATION
IMPLEMENTATION_FIDELITY
```

Non usare test asintotici o p-value come prova di validazione.

Non dichiarare optima.

---

# 11. CONFRONTO FORENSE CON STAGE A ORIGINALE

Dopo aver analizzato R1, confronta qualitativamente e quantitativamente:

```text
Stage A original
vs
E16-A-R1
```

ma senza combinare i dataset.

Per ogni contrasto principale indica:

```text
original result
R1 result
direction preserved? YES/NO
magnitude materially changed? YES/NO
interpretation strengthened / weakened / reversed / unresolved
```

Valuta almeno:

```text
A02 - A01
A04 - A03
primary interaction
crop-17 working-region signal
crop-25 cash-floor signal
```

Lo Stage A originale resta evidence forense, non viene riabilitato automaticamente.

---

# 12. GATE C*

Calcola il gate esclusivamente sulle celle:

```text
A02 -> crop target 10 / HIGH watering
A07 -> crop target 17 / HIGH watering
A04 -> crop target 25 / HIGH watering
```

Usa esclusivamente:

```text
completion_rate
median post-ramp watering_execution_rate
median watering_continuity
median crop_target_attainment
```

Criteri frozen:

```text
completion_rate >= 0.80
median watering_execution_rate >= 0.60
median watering_continuity >= 0.75
median crop_target_attainment >= 0.80
```

Poi:

```text
C* = largest crop target among CAPACITY_ELIGIBLE cells
```

È vietato usare:

```text
final_money
opponent_money
```

come input del gate.

Se nessuna cella è eleggibile:

```text
STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR
```

Non inventare una regola alternativa.

---

# 13. STOP OBBLIGATORIO

Dopo:

1. 28 episodi E16-A-R1;
2. integrity check;
3. analisi R1;
4. confronto con Stage A originale;
5. calcolo gate `C*`;

FERMATI.

Non eseguire Stage B anche se il gate è PASS.

Non modificare MODEL_SPEC.

Non preparare submission Kaggle.

Non fare ulteriori repair.

Non fare commit/push salvo istruzione separata.

---

# 14. OUTPUT ATTESI

Usa o aggiorna gli artifact R1 previsti dall'implementazione, mantenendo separazione dall'originale.

Almeno:

```text
results/e16/stage_a_r1/E16_STAGE_A_R1_RUN_MANIFEST.json
results/e16/analysis/E16_STAGE_A_R1_ANALYSIS.md
results/e16/analysis/E16_STAGE_A_R1_COMPARISON.md
results/e16/analysis/E16_STAGE_B_GATE_R1.json
```

Se i nomi effettivamente implementati differiscono, usa quelli previsti dal repository senza alterare la semantica.

Preserva tutti i raw episode results e gli event ledger R1.

---

# 15. REPORT FINALE

Concludi con:

```text
E16_A_R1_STATUS: COMPLETE | BLOCKED

EPISODES_EXPECTED: 28
EPISODES_COMPLETED: ...

GAMEPLAY_FAILURES: ...
INFRASTRUCTURE_FAILURES: ...

TESTS: <passed>/<total>

TREATMENT_BUILD_SHA256_VERIFIED: YES | NO
CONFIG_SHA256_VERIFIED: YES | NO
OPPONENT_SHA256_VERIFIED: YES | NO

ORIGINAL_STAGE_A_PRESERVED: YES | NO
INTEGRITY_CHECK: PASS | FAIL

A01_FINAL_MONEY: ...
A02_FINAL_MONEY: ...
A03_FINAL_MONEY: ...
A04_FINAL_MONEY: ...
A05_FINAL_MONEY: ...
A06_FINAL_MONEY: ...
A07_FINAL_MONEY: ...

A02_MINUS_A01: ...
A04_MINUS_A03: ...
PRIMARY_INTERACTION: ...

CAPACITY_ELIGIBLE:
  A02: YES | NO
  A07: YES | NO
  A04: YES | NO

C_STAR: 10 | 17 | 25 | NONE
STAGE_B_GATE: PASS | BLOCKED

ORIGINAL_VS_R1:
  A02_MINUS_A01: PRESERVED | CHANGED | REVERSED | UNRESOLVED
  A04_MINUS_A03: PRESERVED | CHANGED | REVERSED | UNRESOLVED
  PRIMARY_INTERACTION: PRESERVED | CHANGED | REVERSED | UNRESOLVED
  CROP_17_SIGNAL: PRESERVED | CHANGED | REVERSED | UNRESOLVED
  CROP_25_CASH_FLOOR: PRESERVED | CHANGED | REVERSED | UNRESOLVED

MODEL_VALIDITY:
  ...

POLICY_REALIZATION:
  ...

IMPLEMENTATION_FIDELITY:
  ...

STAGE_B_EXECUTED: NO
BLOCKERS: NONE | ...
```

Per i valori `Axx_FINAL_MONEY`, specifica la statistica riportata e conserva comunque i valori grezzi nell'analysis artifact.

Il task termina qui.
