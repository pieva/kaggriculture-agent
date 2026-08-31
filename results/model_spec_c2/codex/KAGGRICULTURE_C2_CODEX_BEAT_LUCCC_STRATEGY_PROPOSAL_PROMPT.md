# KAGGRICULTURE C2 — CODEX STRATEGY PROPOSAL TO BEAT LUCCC

## Mandato

Produrre una **proposta strategica indipendente** su come Codex intende battere il benchmark esterno LuCcc, usando:

1. la tua MODEL_SPEC C2 e il tuo build appena completato;
2. la tua precedente analisi/replay analysis di LuCcc;
3. la review appena prodotta su routine planning;
4. le evidenze Antigravity già disponibili.

Questo task è **analysis/design only**.

Non implementare.
Non modificare Foundation.
Non modificare DLC.
Non modificare MODEL_SPEC.
Non lanciare nuovi benchmark lunghi.
Non fare tournament.
Non inviare Kaggle.
Non committare.

L'obiettivo è capire **che agente costruiresti adesso**, non correggere quello esistente.

---

# 1. Contesto architetturale da assumere

Non assumere che venga introdotto un nuovo `Operational Planning Model`.

È in valutazione una semplificazione dell'architettura documentale:

```text
ENGINE CONTRACT
ONTOLOGY
STATE MACHINE
FEATURE MODEL
MODEL_SPEC agent-specific
```

con possibile rimozione o forte riduzione di:

```text
DECISION LIFECYCLE CONTRACT
OPERATIONAL PLANNING MODEL
```

La ragione è che commitment, scheduling, routing, replanning e interrupt sembrano essere **policy altamente agent-specific e sperimentali**, non abbastanza deterministiche da meritare necessariamente layer condivisi distinti.

Per questo task:

> non proporre automaticamente nuovi layer di Foundation.

Se ritieni indispensabile conservare parti del DLC, indica **quali principi minimi** meritano di sopravvivere e quali possono essere assorbiti nella MODEL_SPEC.

---

# 2. Benchmark da battere

Replay di riferimento:

```text
PLAYER: LuCcc
EPISODE_ID: 103484828
FINAL_SCORE: 56,772
```

Evidenza consolidata:

```text
LAND:
Q0 only
no expansion

WORKERS:
7 total

FOOTPRINT:
~24 productive tiles + shed

LIVESTOCK:
3 COW
3 SHEEP
6 pasture

CROPS:
~18 crop tiles
high-value MELON / STRAWBERRY
WHEAT support

MILK:
96 units

WOOL:
92 units

STRAWBERRY:
60 units

MELON:
60 units

HARVEST:
100 requested
100 observed effects

MOVE:
1,449
30.29% worker actions

SERVICE CADENCE:
FEED / CARE ≈ 24 steps
COW collection ≈ 48
SHEEP collection ≈ 72
WHEAT reuse ≈ 96
STRAWBERRY recurrent harvest ≈ 47.5 median interval/tile
```

Final objective:

```text
BEAT_LUCCC:
FINAL_MONEY > 56,772
```

Economic project gates:

```text
< 50,000 = failure
50,000–79,999 = material improvement / target miss
>= 80,000 = target
```

Quindi 56,772 è il benchmark immediato, non il target finale del progetto.

---

# 3. Stato Codex da cui partire

Il tuo ultimo C2:

```text
FINAL_MONEY_MEAN: 9,851
PRODUCTIVE_UTILIZATION: 28–32%
LIVESTOCK_MONETIZED: none
BIOLOGICAL_INVALIDATIONS: 6

planning:
17-day capacity calendar
20% route reserve
15% exception reserve
immutable daily commitment
max 2 new entities/day
2 quadrants
8 hands
```

La tua self-diagnosis precedente:

```text
CODEX_OVERCONSERVATIVE_PLANNING: SUPPORTED
```

e:

```text
PREFERRED_PLANNING_TIMESCALE:
ROLLING_CURRENT_DAY_WITH_EVENT_DRIVEN_REPLAN_AND_SOFT_LONG_HORIZON_FORECAST
```

---

# 4. Evidenza Antigravity da considerare

AG pure horticulture:

```text
FINAL_MONEY_MEAN:
43,837.33
```

AG Q0 2+2:

```text
24,646.67
```

AG Q0 3+3:

```text
37,997.67
```

AG Q0 3+3 production:

```text
MILK:
93

WOOL:
74

TOTAL_CROP_UNITS:
24.7
```

LuCcc:

```text
MILK:
96

WOOL:
92

TOTAL_CROP_UNITS:
120
```

Forensic verdict:

```text
MARKET_TIMING_GAP:
NONE

PRIMARY_GAP_CLASS:
CROP_SERVICEABILITY

Q0_3X3_ARCHITECTURE_VERDICT:
STRUCTURALLY_VALID
```

La nuova ipotesi in test da AG è:

```text
persistent roles
local zones
recurrent routes
task commitment
short-horizon capacity reservation
critical interrupts only
```

Non assumere che questa sia necessariamente la soluzione migliore: proponi la tua strategia.

---

# 5. Domanda centrale

Rispondi come progettista dell'agente:

> Se dovessi costruire da zero il prossimo Codex candidate con l'obiettivo immediato di superare 56,772, quale strategia useresti e perché?

Non limitarti a descrivere correzioni marginali della V6.

Puoi:

```text
KEEP
REMOVE
REWRITE
REPLACE
```

qualunque elemento agent-specific del precedente design.

---

# 6. Architecture choice

Devi scegliere esplicitamente tra almeno queste famiglie:

```text
A. compact Q0 hybrid, LuCcc-like
B. compact Q0 hybrid but different animal/crop mix
C. pure horticulture optimized
D. Q0 + Q1 staged scaling
E. another architecture
```

Indica:

```text
PRIMARY_ARCHITECTURE
SECONDARY_FALLBACK
REJECTED_OPTIONS
```

con motivazione economica e operativa.

---

# 7. Productive footprint

Definisci il footprint che useresti:

```text
land/quadrants
worker count
crop tile count
crop mix
pasture count
animal species/count
shed usage
```

Non usare range vaghi se puoi proporre valori concreti.

Se non sei sufficientemente sicuro di un valore, dichiaralo come parametro sperimentale.

---

# 8. Worker operating model

Definisci come lavorerebbero i worker.

Confronta almeno:

```text
persistent roles
dynamic roles
fixed zones
dynamic zones
recurrent routes
global dispatcher
local dispatcher
task commitment
staging
reserve worker
```

Per ogni meccanismo indica:

```text
USE
DO_NOT_USE
TEST
```

e perché.

---

# 9. Planning / replanning

Definisci il timescale operativo concreto.

Esempio di struttura possibile:

```text
strategic horizon
admission horizon
daily rolling plan
atomic task commitment
event interrupt
EOD review
```

Ma non devi adottarla se ritieni migliore un'altra.

Rispondi esplicitamente:

```text
HOW_OFTEN_GLOBAL_REPLAN
HOW_OFTEN_LOCAL_REPLAN
WHAT_IS_COMMITTED
WHAT_CAN_INTERRUPT
WHAT_IS_FORECAST_ONLY
```

---

# 10. Biological scheduling

Descrivi come proteggere:

```text
WATER
HARVEST
FEED
CARE
MILK collection
WOOL collection
fertilizer collection/application
REPLANT
```

Ordina le attività per:

```text
irreversible loss risk
economic value at risk
deadline proximity
```

e spiega come evitare che livestock servicing affami le crop.

---

# 11. Crop strategy

Spiega:

```text
MELON role
STRAWBERRY role
WHEAT role
```

e se replicheresti il mix LuCcc o lo cambieresti.

Specificare:

```text
crop tile counts
planting cohorts
harvest cadence
fertilizer targeting
```

per quanto sostenibile dall'evidenza.

---

# 12. Livestock strategy

Spiega:

```text
why COW
why SHEEP
why not GOOSE
```

oppure proponi un mix diverso.

Specificare:

```text
activation timing
feed support
care routine
collection routine
fertilizer loop
```

e quanto output minimo pretenderesti prima di considerare il ramo valido.

---

# 13. Market policy

La forensic precedente ha escluso il market timing come gap primario.

Quindi:

> non costruire la strategia attorno al trading se non hai nuova evidenza.

Indica comunque:

```text
when to sell
what inventory reserve to keep
whether to exploit short-term price oscillations
```

e soprattutto se questa componente è:

```text
PRIMARY
SECONDARY
LOW_PRIORITY
```

---

# 14. Scaling policy

Rispondi:

> proveresti a battere LuCcc prima su Q0 oppure useresti Q1 già nel primo candidate?

Se proponi Q1, devi giustificare:

```text
when land is bought
when workforce increases
when livestock/crops activate
how Q0 serviceability is protected
payback horizon
rollback condition
```

Se non proponi Q1:

```text
why compactness dominates expansion
```

---

# 15. Capacity model

Non usare reserve percentuali fisse senza giustificazione.

Proponi invece un modello basato su quantità osservabili, ad esempio:

```text
required service actions
travel actions
productive actions
deadline windows
worker availability
slack
```

Definisci una semplice regola:

```text
ADMIT_NEW_ASSET if ...
```

che possa essere verificata a runtime.

---

# 16. Performance decomposition

Definisci quali output devono essere misurati separatamente.

Minimo:

```text
final money
crop revenue
livestock revenue
market/trading contribution
milk units
wool units
melon units
strawberry units
wheat consumed/sold
fertilizer collected/applied
productive action ratio
MOVE/productive action
PASS ratio
deadline misses
retarget count
```

Indica quali 5 metriche useresti come leading indicators.

---

# 17. Preregistered performance prediction

Non basta dire “dovrebbe migliorare”.

Fornisci una previsione preregistrata per il candidate proposto.

Formato:

```text
EXPECTED_FINAL_MONEY:
<value or range>

MINIMUM_ACCEPTABLE:
<value>

EXPECTED_MILK:
<value/range>

EXPECTED_WOOL:
<value/range>

EXPECTED_STRAWBERRY:
<value/range>

EXPECTED_MELON:
<value/range>

EXPECTED_PRODUCTIVE_UTILIZATION:
<value/range>
```

Spiega da quale evidenza deriva.

---

# 18. What must be removed from current Codex V6

Elenca senza ambiguità gli elementi della V6 che elimineresti.

Valuta almeno:

```text
17-day hard capacity calendar
20% route reserve
15% exception reserve
immutable daily commitment
max 2 new entities/day
2-quadrant default
8-hand default
conditional COW branch
```

Per ciascuno:

```text
KEEP
REMOVE
REWRITE
```

con una riga di motivazione.

---

# 19. MODEL_SPEC / lifecycle simplification

Dato il dubbio architetturale corrente, rispondi anche:

> quanto del DLC e del planning contract serve davvero al candidate?

Proponi una versione **minimalista**.

Classifica i concetti:

```text
decision identity
DEFINE
PLAN
commitment
VERIFY
REVIEW
SHIP
repair
invalidation
supersession
evidence ledger
capacity reservation
roles
routes
interrupts
```

come:

```text
MODEL_SPEC_CORE
IMPLEMENTATION_DETAIL
REMOVE
```

Obiettivo:

> evitare che la documentazione formale diventi più complessa della policy che dovrebbe descrivere.

Non modificare i documenti in questo task.

---

# 20. Esperimento minimo consigliato

Proponi il **singolo esperimento locale successivo** che faresti per verificare la tua strategia.

Deve specificare:

```text
CONTROL
TEST
seeds
primary endpoint
secondary endpoints
success criterion
failure interpretation
```

Preferire un esperimento ad alto valore informativo, non una batteria di tuning.

---

# 21. Output

Creare un solo file:

```text
results/model_spec_c2/codex/
CODEX_BEAT_LUCCC_STRATEGY_PROPOSAL.md
```

Struttura obbligatoria:

1. Executive Strategy
2. LuCcc Lessons Retained
3. Current Codex V6 Failures
4. Proposed Production Architecture
5. Worker Operating Model
6. Planning and Replanning
7. Biological Scheduling
8. Crop Strategy
9. Livestock Strategy
10. Market Strategy
11. Scaling Policy
12. Capacity Admission Rule
13. Performance Model
14. Preregistered Prediction
15. V6 Components to Keep/Remove/Rewrite
16. MODEL_SPEC / Lifecycle Simplification
17. Minimum Next Experiment
18. Final Verdict

Chiudere con:

```text
PRIMARY_ARCHITECTURE:
<value>

SECONDARY_FALLBACK:
<value>

TARGET_TO_BEAT:
56772

EXPECTED_FINAL_MONEY:
<value/range>

MINIMUM_ACCEPTABLE:
<value>

Q0_ONLY_FIRST:
YES | NO

WORKER_MODEL:
<value>

PLANNING_MODEL:
<value>

GLOBAL_REPLAN_FREQUENCY:
<value>

TASK_COMMITMENT:
<value>

LIVESTOCK_CONFIGURATION:
<value>

CROP_CONFIGURATION:
<value>

MARKET_PRIORITY:
PRIMARY | SECONDARY | LOW_PRIORITY

CURRENT_V6_REUSABLE:
HIGH | MEDIUM | LOW

DLC_REQUIRED_AS_SEPARATE_LAYER:
YES | NO | MINIMAL_ONLY

OPERATIONAL_PLANNING_LAYER_REQUIRED:
YES | NO

MODEL_SPEC_SHOULD_ABSORB_OPERATIONS:
YES | NO | PARTIALLY

NEXT_EXPERIMENT:
<value>

IMPLEMENTATION_AUTHORIZED:
NO

TOURNAMENT_AUTHORIZED:
NO

KAGGLE_AUTHORIZED:
NO
```

## STOP

Dopo la proposta fermarsi.

Non implementare.
Non modificare MODEL_SPEC.
Non modificare Foundation.
Non produrre un secondo report.
