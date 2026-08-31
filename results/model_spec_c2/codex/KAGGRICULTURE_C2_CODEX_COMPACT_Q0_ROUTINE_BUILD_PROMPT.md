# KAGGRICULTURE C2 — CODEX BUILD: COMPACT Q0 HYBRID ROUTINE CANDIDATE

## Mandato

Implementare il nuovo candidate Codex definito in:

```text
results/model_spec_c2/codex/CODEX_BEAT_LUCCC_STRATEGY_PROPOSAL.md
```

Obiettivo immediato:

```text
BEAT_LUCCC:
FINAL_MONEY > 56,772
```

Il candidate deve essere costruito come **nuovo planner/policy agent-specific**, non come tuning marginale della V6.

La V6 va riutilizzata solo dove il report strategico l'ha dichiarata utile:

```text
engine adapter
legality guards
stable entity identity
request/effect verification
telemetry
standalone compatibility
```

La strategia produttiva e il planner V6 devono essere sostituiti.

---

# 1. Gate e vincoli

```text
FOUNDATION_CHECKPOINT:
f391ee2

FOUNDATION:
DO NOT MODIFY

DLC:
DO NOT MODIFY in this build

MODEL_SPEC:
UPDATE AUTHORIZED for Codex agent-specific implementation

TOURNAMENT:
NOT AUTHORIZED

KAGGLE:
NOT AUTHORIZED

COMMIT:
NOT AUTHORIZED

PUSH:
NOT AUTHORIZED
```

Non modificare file Antigravity.
Non modificare Copilot.
Non modificare evidenze Foundation.
Non usare Q1 nel primo candidate.

---

# 2. Architettura produttiva obbligatoria

Implementare il candidate primario:

```text
LAND:
Q0 only

WORKERS:
7 total, farmer included

CROP_TILES:
18

CROP_MIX:
9 MELON
8 STRAWBERRY
1 WHEAT

PASTURES:
6

LIVESTOCK:
3 COW
3 SHEEP

GOOSE:
0
```

La configurazione 18 crop + 6 pasture è il footprint congelato del primo candidate.

Non aggiungere una diciannovesima crop tile durante questo build.

---

# 3. Livestock activation

Non attivare necessariamente 3+3 immediatamente.

Usare staged activation:

```text
BOOTSTRAP:
2 COW + 2 SHEEP tra day 0 e day 1

EXPANSION:
+1 COW circa day 7
+1 SHEEP circa day 8
```

La seconda fase deve essere subordinata alla capacity admission rule.

Se la capacity rule non passa, non forzare il 3+3.

Registrare:

```text
animal_activation_day
activation_admitted
activation_rejected
rejection_reason
```

---

# 4. Worker operating model

Implementare:

```text
3 CROP workers
2 LIVESTOCK workers
1 FERTILIZER_LOGISTICS worker
1 FLOAT_RESERVE worker
```

Ruoli persistenti, rivalutabili principalmente a EOD.

## CROP workers

Tre zone da circa 6 crop tile ciascuna.

Ogni worker:

```text
owns one crop zone
uses local recurrent route
does not serve ordinary livestock tasks
commits to one target until completion/invalidation/hard interrupt
```

## LIVESTOCK workers

Uno responsabile principalmente delle COW, uno delle SHEEP:

```text
FEED
CARE
MILK/WOOL collection
local animal route
```

## FERTILIZER_LOGISTICS

Responsabilità:

```text
shed
feed staging
fertilizer collection
fertilizer delivery
inventory unblock
PLACE / market logistics support
```

## FLOAT_RESERVE

Responsabilità:

```text
hard interrupt support
temporary overload
worker absence/unavailability
critical crop/livestock assistance
```

Non deve vagare senza target.

---

# 5. Planning model

Eliminare dalla V6:

```text
17-day hard capacity calendar
20% fixed route reserve
15% fixed exception reserve
immutable daily commitment
max 2 new entities/day
2-quadrant default
```

Sostituire con:

```text
persistent roles
local rolling routes
atomic task commitment
short hard scheduling horizon
soft long-horizon forecast
event/deadline-driven interrupt
EOD global review
```

---

# 6. Replanning rules

## Global replan

Solo:

```text
EOD
workforce change
asset change
structural invalidation
hard-deadline set infeasible
```

Non eseguire global rescan a ogni turn.

## Local replan

Solo dopo:

```text
target completion
target invalidation
worker unavailability
hard interrupt
```

## Commitment

Il target corrente resta committed fino a:

```text
COMPLETED
INVALIDATED
HARD_INTERRUPT
```

Non cambiare target per un piccolo vantaggio opportunistico.

---

# 7. Hard vs soft interrupts

Implementare reason code espliciti.

## HARD_INTERRUPT

```text
animal escape prevention
FEED deadline vicino a EOD
crop WATER deadline con perdita biologica
HARVEST deadline con perdita/retirement/terminal risk
blocking inventory con loss imminente
worker/target legality invalidation
```

## SOFT / NON-INTERRUPTING

```text
CARE opportunity
fertilizer opportunity
market price opportunity
ordinary inventory clearing
newly ready low-risk crop
```

CARE e fertilizer devono essere schedulati, ma non rompere arbitrariamente una route crop critica.

---

# 8. Crop scheduling

## MELON

```text
9 tiles
3 cohorts of 3
```

Usare cohort staggering coerente con il report strategico.

Target iniziale:

```text
day offsets ~0 / 1 / 2
```

Congelare gli offset prima del benchmark preregistrato.

## STRAWBERRY

```text
8 tiles
2 cohorts of 4
```

Sfalsare le due coorti di circa 2 giorni.

Proteggere raccolte ricorrenti.

## WHEAT

```text
1 tile
```

Scopo primario:

```text
FEED buffer
```

Target full-yield age 4 quando compatibile con serviceability.

Non sacrificare MELON/STRAWBERRY per espandere WHEAT nel primo candidate.

---

# 9. Biological task priority

Usare priorità lessicografica:

```text
1. irreversible loss before next feasible service
2. economic value at risk
3. deadline proximity / remaining slack
4. route-local completion cost
```

Applicarla a:

```text
WATER
HARVEST
FEED
CARE
MILK collection
WOOL collection
fertilizer collection
fertilizer application
REPLANT
```

La routine deve impedire che il livestock servicing affami le crop.

---

# 10. Fertilizer loop

Implementare closed loop:

```text
pasture
→ fertilizer collection
→ high-value eligible crop
→ same-day WATER if serviceable
```

Priorità:

```text
1. MELON cohort con valore imminente
2. STRAWBERRY early recurring cycle
3. WHEAT only if feed critical
```

Non applicare fertilizer se il WATER same-day non è schedulabile.

---

# 11. Market policy

Market priority:

```text
LOW_PRIORITY
```

Non costruire vantaggio sul trading.

Vendere prevalentemente:

```text
MILK
WOOL
MELON
STRAWBERRY
```

con batching giornaliero o quando inventory blockage minaccia collection.

WHEAT reserve target:

```text
2 × active_animals
```

A pieno footprint:

```text
12 units
```

Non comprare per rivendere.

Non interrompere routine biologiche per oscillazioni di prezzo.

---

# 12. Capacity admission rule

Implementare una capacity rule basata su azioni osservabili.

Per ogni finestra rilevante:

```text
AVAILABLE(w)
=
worker action slots disponibili

REQUIRED(w)
=
hard service actions
+ route MOVE actions
+ PICKUP / PLACE
+ inventory handling
+ candidate asset actions

SLACK(w)
=
AVAILABLE(w) - REQUIRED(w)
```

Ammettere un nuovo asset soltanto se:

```text
all hard deadlines remain feasible
AND min(SLACK(w)) >= 0
AND feed buffer covers 2 FEED rounds
AND cash covers committed biological inputs
AND inventory has a legal collection/sale path
AND first monetizable output is before payback cutoff
AND forecast peak demand does not exceed observed capacity
```

Niente reserve percentuali fisse.

---

# 13. Observed capacity

Dopo almeno 3 giorni completi:

```text
observed_capacity
=
minimum useful actions actually completed across last 3 days
adjusted for observed MOVE / handling
```

Prima di 3 giorni:

```text
no growth beyond preregistered bootstrap
based only on optimistic forecast
```

---

# 14. MODEL_SPEC revision

Aggiornare:

```text
docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md
```

per assorbire direttamente l'operatività del candidate.

Non creare nuovi layer documentali.

La MODEL_SPEC deve contenere in forma sintetica:

```text
objective
production architecture
worker roles
zones/routes
planning horizon
task commitment
interrupt rules
capacity admission
crop cohorts
livestock activation
fertilizer loop
market policy
verification
performance metrics
review criteria
```

Non duplicare formalismo DLC non necessario.

---

# 15. Lifecycle simplification within Codex implementation

Nel runtime mantenere solo ciò che serve:

```text
decision identity
PLAN
target commitment
VERIFY post-state
invalidation
hard interrupt reason code
simple evidence logging
```

Non è necessario mantenere una macchina a stati complessa se non serve al controller.

Non modificare il DLC condiviso in questo task.

---

# 16. Instrumentation obbligatoria

Registrare almeno:

```text
FINAL_MONEY
crop revenue
livestock revenue
market/trading contribution

MILK units
WOOL units
MELON units
STRAWBERRY units
WHEAT consumed
WHEAT sold

fertilizer collected
fertilizer applied

productive actions
MOVE actions
PASS actions

MOVE_PER_PRODUCTIVE_ACTION
PRODUCTIVE_UTILIZATION

ON_TIME_CROP_SERVICE_RATIO
HARD_DEADLINE_MISSES
ANIMAL_ESCAPE

RETARGET_COUNT
TARGET_DWELL_TIME
DUPLICATE_ASSIGNMENTS
INTERRUPTS_BY_REASON

ROLE_CHANGES
CROSS_ZONE_ASSISTS
```

---

# 17. Leading indicators

Calcolare obbligatoriamente:

```text
1. ON_TIME_CROP_SERVICE_RATIO
2. HARD_DEADLINE_MISSES
3. HIGH_VALUE_CROP_UNITS_VS_COHORT_PLAN
4. MOVE_PER_PRODUCTIVE_ACTION
5. RETARGET_COUNT_PER_WORKER_DAY
```

---

# 18. Technical verification before performance

Prima dei benchmark economici verificare:

```text
source controller imports
standalone builds
standalone isolated import
source/standalone parity
no manual DROP
legal actions only
terminal handling
request/effect verification
```

Eseguire test agent-specific e repository test applicabili.

Non lanciare benchmark economico finché la verifica tecnica non passa.

---

# 19. Performance experiment

Dopo PASS tecnico, eseguire il candidate sui seed preregistrati:

```text
26090101
26090102
26090103
```

Entrambi i player seat se il runner lo supporta senza introdurre avversari diversi/non controllati.

Se l'infrastruttura corrente non supporta paired seat in modo coerente, usare almeno i 3 seed e documentare la limitazione.

Non fare tuning sui seed dopo aver visto i risultati.

---

# 20. Performance targets

Predizione preregistrata Codex:

```text
EXPECTED_FINAL_MONEY:
60,000–68,000

MINIMUM_ACCEPTABLE:
56,773

EXPECTED_MILK:
90–100

EXPECTED_WOOL:
85–95

EXPECTED_STRAWBERRY:
45–60

EXPECTED_MELON:
48–60

EXPECTED_PRODUCTIVE_UTILIZATION:
80–96%
```

Project gates:

```text
< 50,000:
FAILURE

50,000–56,772:
MATERIAL_IMPROVEMENT_BUT_BELOW_LUCCC

56,773–79,999:
LUCCC_BEATEN_TARGET_80K_MISSED

>= 80,000:
PROJECT_TARGET_MET
```

---

# 21. Success criteria

Il build è `BUILD_READY_FOR_REVIEW` se:

```text
technical verification PASS
AND mean final money >= 56,773
AND no animal escapes
AND livestock output materially preserved
AND crop serviceability materially improved
```

Strong success:

```text
mean final money >= 60,000
```

Project-level success:

```text
mean final money >= 80,000
```

---

# 22. Failure interpretation

Se il candidate fallisce, classificare il primary bottleneck tra:

```text
ROUTING
ROLE_ALLOCATION
CROP_SERVICEABILITY
LIVESTOCK_SERVICEABILITY
COHORT_TIMING
CAPACITY_ADMISSION
INVENTORY_LOGISTICS
FERTILIZER_LOOP
MARKET_CONVERSION
ACTIVATION_COST
IMPLEMENTATION_DEFECT
OTHER
```

Non fare tuning automatico dopo il risultato.

---

# 23. Output

Aggiornare/creare in:

```text
results/model_spec_c2/codex/
```

almeno:

```text
CODEX_COMPACT_Q0_ROUTINE_BUILD_REPORT.md
CODEX_COMPACT_Q0_ROUTINE_RESULTS.csv
BUILD_VERIFICATION.md
TOURNAMENT_MANIFEST.md
KAGGLE_MANIFEST.md
```

I manifest devono restare chiusi salvo gate esplicito successivo.

---

# 24. Report finale

Struttura minima:

1. Executive Verdict
2. Foundation / Repository Verification
3. MODEL_SPEC Changes
4. V6 Components Removed
5. Production Architecture
6. Worker Roles and Zones
7. Planning and Replanning
8. Capacity Admission
9. Crop Cohorts
10. Livestock Activation
11. Fertilizer / Logistics
12. Technical Verification
13. Seed-Level Performance
14. Production Decomposition
15. Worker Efficiency Metrics
16. Comparison vs AG Q0 3+3
17. Comparison vs LuCcc
18. Failure/Success Diagnosis
19. Final Gate

Chiudere con:

```text
AGENT_ID:
codex

ARCHITECTURE:
Q0_18CROP_6PASTURE_3COW_3SHEEP_7WORKERS

MODEL_SPEC_REVISION:
COMPLETE | INCOMPLETE

TECHNICAL_BUILD:
PASS | FAIL

FINAL_MONEY_MEAN:
<value>

FINAL_MONEY_MEDIAN:
<value>

FINAL_MONEY_STD:
<value>

MILK_MEAN:
<value>

WOOL_MEAN:
<value>

MELON_MEAN:
<value>

STRAWBERRY_MEAN:
<value>

PRODUCTIVE_UTILIZATION:
<value>

MOVE_PER_PRODUCTIVE_ACTION:
<value>

RETARGET_PER_WORKER_DAY:
<value>

ON_TIME_CROP_SERVICE_RATIO:
<value>

HARD_DEADLINE_MISSES:
<value>

ANIMAL_ESCAPES:
<value>

DELTA_VS_CODEX_V6_9851:
<value>

DELTA_VS_AG_Q0_3X3_37997_67:
<value>

DELTA_VS_LUCCC_56772:
<value>

ECONOMIC_GATE:
FAILURE |
MATERIAL_IMPROVEMENT_BELOW_LUCCC |
LUCCC_BEATEN |
PROJECT_TARGET_MET

PRIMARY_BOTTLENECK:
<value or NONE>

BUILD_VERDICT:
BUILD_NOT_READY |
BUILD_READY_FOR_REVIEW

TOURNAMENT_AUTHORIZED:
NO

KAGGLE_AUTHORIZED:
NO

COMMIT_AUTHORIZED:
NO

PUSH_AUTHORIZED:
NO
```

## STOP

Dopo il build, la verifica e il benchmark preregistrato fermarsi.

Non fare tuning post-hoc.
Non fare tournament.
Non inviare Kaggle.
Non fare commit.
Non fare push.
