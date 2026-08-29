# E16 --- STAGE A EXECUTION PROMPT --- ANTIGRAVITY

## Ruolo

Agisci come **execution operator** del disegno sperimentale E16 già
congelato.

Non sei autorizzato a ridisegnare, ottimizzare o correggere
l'esperimento.

Il tuo compito è:

1.  verificare il checkpoint E16 READY/E0-PASS;
2.  eseguire **esattamente** i 28 episodi frozen di Stage A;
3.  preservare integralmente config, seed, seat, opponent e treatment
    build;
4.  eseguire l'analisi Stage A già predisposta;
5.  calcolare il gate `C*` già definito;
6.  fermarti **prima di Stage B** e riportare i risultati.

------------------------------------------------------------------------

# 1. LEGGI PRIMA DI AGIRE

Leggi integralmente:

``` text
docs/experiment_designs/e16/E16_TRAINING_DESIGN_FROZEN.md
docs/prompts/E16_IMPLEMENTATION_PROMPT.md
configs/e16/E16_FROZEN_CONFIG.json
results/e16/manifests/E16_IMPLEMENTATION_MANIFEST.json
results/e16/instrumentation/E16_E0_REPORT.md
```

Poi ispeziona, senza modificarli:

``` text
scripts/run_e16_training.py
scripts/analyze_e16_stage_a.py
src/agricola/e16/
tests/test_e16_*.py
```

Usa le convenzioni e i comandi effettivamente implementati nel
repository. Non inventare CLI alternative se gli script espongono già
l'interfaccia corretta.

------------------------------------------------------------------------

# 2. CHECKPOINT OBBLIGATORIO

Prima di qualsiasi training run verifica:

``` text
IMPLEMENTATION_STATUS = READY
TESTS = 130/130
E0_STATUS = PASS
STAGE_A_READY = YES
BLOCKERS = NONE

TREATMENT_BUILD_SHA256 =
8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e

CONFIG_SHA256 =
4c6ca43025d5a95acd6b2c8c5eb51a17a4bc4cadd672146055c317d54864ec92

OPPONENT_SHA256 =
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Verifica inoltre che il working tree e gli artifact corrispondano al
checkpoint autorizzato.

Se uno degli hash non corrisponde:

``` text
STOP
STATUS = BLOCKED_HASH_MISMATCH
```

Non ricostruire automaticamente l'artifact per far tornare l'hash.

------------------------------------------------------------------------

# 3. FREEZE ASSOLUTO DURANTE STAGE A

Durante l'esecuzione non modificare:

``` text
src/agricola/e16/**
configs/e16/E16_FROZEN_CONFIG.json
results/e16/manifests/E16_TREATMENT_BUILD.py
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

Se emerge un vero problema di implementazione:

``` text
STOP
preserva tutti i risultati già prodotti
documenta il problema
non correggere e riprendere autonomamente
```

------------------------------------------------------------------------

# 4. STAGE A FROZEN

Le celle sono esattamente:

``` text
A01 = watering LOW  0.20 × crop target 10
A02 = watering HIGH 0.70 × crop target 10

A03 = watering LOW  0.20 × crop target 25
A04 = watering HIGH 0.70 × crop target 25

A05 = watering MID  0.45 × crop target 17
A06 = watering MID  0.45 × crop target 25
A07 = watering HIGH 0.70 × crop target 17
```

Controls:

``` text
quadrants_owned = 2
livestock_headcount_target = 4
pasture_allocation_target = 5
workforce_headcount = 10
livestock_species = Cow
opponent = Copilot E15 frozen
```

------------------------------------------------------------------------

# 5. SEED E SEAT

Usa esclusivamente:

``` text
1802163452
1678077158
```

Per ogni cella e seed:

``` text
treatment P0 / opponent P1
opponent P0 / treatment P1
```

Totale atteso:

``` text
7 cells × 2 seeds × 2 seats = 28 episodes
```

Né 27 né 29.

Gameplay failure o disqualification:

``` text
retain as outcome
NO replacement
NO automatic rerun
```

Infrastructure failure può essere ripetuto solo secondo la rerun policy
frozen e con identica configurazione.

------------------------------------------------------------------------

# 6. ESECUZIONE

Prima esegui una verifica rapida della suite pertinente e degli hash.

Poi usa il runner E16 implementato per eseguire Stage A completo.

Non interpretare i risultati dopo singole celle.

Non fermare celle che performano male.

Non cambiare ordine o protocollo in base a `final_money`.

Al termine verifica che il manifest contenga esattamente 28 episodi
previsti e che tutti abbiano:

``` text
cell_id
seed
treatment_seat
treatment_build_sha256
opponent_sha256
configuration_sha256
completion/failure status
telemetry provenance
```

------------------------------------------------------------------------

# 7. INTEGRITY CHECK POST-RUN

Prima dell'analisi verifica:

``` text
expected episodes = 28
observed episodes = 28
unexpected seeds = 0
unexpected cells = 0
missing seat swaps = 0
treatment hash mismatches = 0
opponent hash mismatches = 0
config hash mismatches = 0
post-freeze policy changes = 0
```

Riporta esplicitamente eventuali gameplay failures/disqualifications.

Se l'integrità strutturale non è rispettata:

``` text
ANALYSIS_STATUS = BLOCKED
```

e fermati.

------------------------------------------------------------------------

# 8. ANALISI STAGE A

Se l'integrity check passa, esegui:

``` text
scripts/analyze_e16_stage_a.py
```

o l'interfaccia effettiva prevista dal repository.

L'analisi deve usare il piano frozen e produrre almeno i confronti:

``` text
A02 - A01
A04 - A03

(A04 - A03) - (A02 - A01)

A03 -> A06 -> A04
A02 -> A07 -> A04

A05 vs corner interpolation
```

Mantieni distinti:

``` text
MODEL_VALIDITY
POLICY_REALIZATION
IMPLEMENTATION_FIDELITY
```

Mostra i raw values per seed/seat oltre alle sintesi.

Non trasformare due seed in una pretesa di statistical validation.

Non dichiarare optima.

------------------------------------------------------------------------

# 9. GATE C\*

Calcola il gate esclusivamente sulle celle:

``` text
A02 -> crop target 10 / HIGH watering
A07 -> crop target 17 / HIGH watering
A04 -> crop target 25 / HIGH watering
```

Usa esclusivamente:

``` text
completion_rate
median post-ramp watering_execution_rate
median watering_continuity
median crop_target_attainment
```

Criteri frozen:

``` text
completion_rate >= 0.80
median watering_execution_rate >= 0.60
median watering_continuity >= 0.75
median crop_target_attainment >= 0.80
```

Poi:

``` text
C* = largest crop target among CAPACITY_ELIGIBLE cells
```

È vietato usare:

``` text
final_money
opponent_money
```

come input del gate.

Se nessuna cella è eleggibile:

``` text
STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR
```

Non cercare una regola alternativa.

------------------------------------------------------------------------

# 10. STOP OBBLIGATORIO

Dopo:

1.  28 episodi Stage A;
2.  integrity check;
3.  analisi Stage A;
4.  calcolo e scrittura del gate `C*`;

**FERMATI.**

Non eseguire Stage B, anche se:

``` text
STAGE_B_GATE = PASS
```

Stage B richiede autorizzazione successiva.

Non modificare MODEL_SPEC.

Non preparare submission Kaggle.

Non fare commit/push salvo che ciò sia esplicitamente richiesto
separatamente.

------------------------------------------------------------------------

# 11. OUTPUT ATTESI

Aggiorna/producI secondo l'implementazione esistente almeno:

``` text
results/e16/stage_a/E16_STAGE_A_RUN_MANIFEST.json
results/e16/analysis/E16_STAGE_A_ANALYSIS.md
results/e16/analysis/E16_STAGE_B_GATE.json
```

Preserva i raw episode results e la telemetry necessaria alla
riproducibilità.

------------------------------------------------------------------------

# 12. REPORT FINALE

Concludi in forma compatta con:

``` text
E16_STAGE_A_STATUS: COMPLETE | BLOCKED
EPISODES_EXPECTED: 28
EPISODES_COMPLETED: ...
GAMEPLAY_FAILURES: ...
INFRASTRUCTURE_FAILURES: ...

TESTS: <passed>/<total>

TREATMENT_BUILD_SHA256_VERIFIED: YES | NO
OPPONENT_SHA256_VERIFIED: YES | NO
CONFIG_SHA256_VERIFIED: YES | NO

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

C_STAR: <10 | 17 | 25 | NONE>
STAGE_B_GATE: PASS | BLOCKED

MODEL_VALIDITY_NOTES:
  ...

POLICY_REALIZATION_NOTES:
  ...

IMPLEMENTATION_FIDELITY_NOTES:
  ...

STAGE_B_EXECUTED: NO
BLOCKERS: NONE | ...
```

Per `Axx_FINAL_MONEY`, specifica chiaramente la statistica riportata
(es. median/mean dei quattro episodi) e conserva comunque i valori
grezzi nell'analysis artifact.

Il compito termina qui.
