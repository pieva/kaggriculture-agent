# E16 --- TRAINING DESIGN FROZEN

**Stato:** `FROZEN — AUTHORIZED FOR IMPLEMENTATION`\
**Fase epistemica:**
`TRAINING / INITIAL BOUNDING + INTERACTION DISCRIMINATION`\
**Data:** 2026-08-29

## 1. Scopo

E16 è il primo round di training successivo al consolidamento post-E15.

L'obiettivo è ottenere massimo information gain su due problemi
principali:

1.  `watering_dispatch_priority × crop_working_set_target`;
2.  `livestock_headcount_target × pasture_allocation_target`.

E16 non cerca un optimum globale. E16 serve a:

-   localizzare regioni di failure, transizione e working
    competitiveness;
-   separare MODEL_VALIDITY, POLICY_REALIZATION e
    IMPLEMENTATION_FIDELITY;
-   restringere intervalli non osservati dopo E15;
-   preparare round successivi di training e, separatamente, VALIDATION
    con seed/opponent indipendenti.

I risultati E16 sono **TRAINING evidence** e non possono essere
riutilizzati come independent VALIDATION o TEST evidence.

------------------------------------------------------------------------

## 2. Baseline canonica

``` text
quadrants_owned = 2
```

Questa è una **controlled E16 baseline**, non un optimum e non un land
threshold frozen.

Gli identificatori ambientali `Q0/Q1/Q2/...` non devono essere usati
come sinonimi del numero totale di quadranti.

`quadrants_owned = 3` resta una regione condizionale non risolta e non
viene manipolata in E16.

------------------------------------------------------------------------

## 3. Architettura del disegno sperimentale

``` text
design_id: E16-FROZEN-S12-MINIMAL
design_type: blocked staged response-surface subset
stage_A_cells: 7
stage_B_cells: 5
planned_max_cells: 12

shared_training_seeds: 2
seat_positions_per_seed: 2

stage_A_episodes: 28
stage_B_episodes: 20
planned_max_episodes: 48

staged: YES
```

L'architettura deriva dal design Codex, con riduzione di costo al
protocollo a 2 seed × 2 seat.

Il terzo seed non viene consumato uniformemente in E16. Resta
disponibile per un successivo approfondimento dei bound o per un nuovo
TRAINING round preregistrato.

------------------------------------------------------------------------

## 4. Opponent frozen

E16 utilizza un singolo opponent E15 frozen:

``` text
artifact:
experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py

sha256:
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

La corrispondenza artefatto ↔ hash è verificata dalla documentazione
frozen E15.

Per riferimento:

``` text
submission_codex_E15_FROZEN.py
fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3

submission_copilot_E15_FROZEN.py
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Pertanto l'opponent E16 frozen è **Copilot**, non Codex.

Tutti i risultati E16 restano opponent-conditional.

------------------------------------------------------------------------

## 5. Common opening e treatment onset

Tutte le celle devono utilizzare una sola implementazione E16 comune.

Il build/hash della treatment policy deve essere identico tra le celle;
possono cambiare esclusivamente i campi dichiarati MANIPULATED.

Definizione di `T0`:

``` text
T0 = primo stato successivo all'esecuzione verificata
     dell'acquisizione che porta quadrants_owned = 2
```

Prima di `T0`:

-   opening identica per tutte le celle;
-   crop working set temporaneamente limitato a 10;
-   nessuna acquisizione di pasture o livestock;
-   stesso schedule workforce pre-treatment;
-   stessa logica di routing, cash e land acquisition.

Dopo `T0`:

-   `quadrants_owned` hard cap = 2;
-   nessun ordine per un terzo quadrante;
-   entrano in vigore i treatment parameters della cella;
-   tutti i moduli non manipolati restano identici.

Se un episodio non raggiunge `T0`, non viene sostituito: è registrato
come opening/policy-realization failure.

------------------------------------------------------------------------

# STAGE A --- IRRIGATION × CROP WORKING SET

## 6. Ipotesi Stage A

### H-A1 --- SERVICE FLOOR

``` text
concepts:
  watering_dispatch_priority
  watering_execution_rate
  watering_continuity
  crop_surface_maintained

relationship:
  thresholded / conditional
```

L'aumento della priorità assegnata al watering dovrebbe aumentare il
servizio effettivamente eseguito fino a saturazione della capacità.

La relazione è falsificata come relazione di MODEL_VALIDITY se la
priorità assegnata modifica realmente il servizio ma non produce
differenze coerenti in maintained surface, failures o outcome.

Se la priorità assegnata non modifica il servizio realizzato, la
diagnosi ricade invece su POLICY_REALIZATION o IMPLEMENTATION_FIDELITY.

### H-A2 --- SERVICE × SURFACE

``` text
concepts:
  watering_dispatch_priority
  watering_execution_rate
  crop_surface_maintained
  worker_capacity_available
  action_dispatch_failure
```

Il valore marginale di una superficie coltivata maggiore è condizionato
dalla capacità di servizio.

Il principale contrasto è una difference-in-differences sul 2×2 LOW/HIGH
watering × LOW/HIGH crop target.

------------------------------------------------------------------------

## 7. Fattori Stage A

### Manipulated

``` text
watering_dispatch_priority:
  LOW  = 0.20 successful-service intent
  MID  = 0.45 successful-service intent
  HIGH = 0.70 successful-service intent

crop_working_set_target:
  10
  17
  25
```

`watering_dispatch_priority` è un PARAMETER di policy.

`watering_execution_rate` è una DERIVED_METRIC.

Non devono essere confusi.

### Controls

``` text
quadrants_owned = 2
livestock_headcount_target = 4
pasture_allocation_target = 5
workforce_headcount = 10
livestock_species = Cow
crop_mix = fixed 40% Wheat / 40% Strawberry / 20% Melon
feed_coverage_rule = common fixed rule
operating_cash_rule = common fixed rule
routing_module = identical
hire_and_renewal_schedule = identical
land_acquisition_timing = common opening
endgame_module = identical
opponent = frozen Copilot E15
```

Tutti questi valori sono controlli sperimentali, non optima.

------------------------------------------------------------------------

## 8. Celle Stage A

  Cell     Watering priority   Crop target Ruolo
  ------ ------------------- ------------- -------------------------------------
  A01               LOW 0.20            10 low-low corner
  A02              HIGH 0.70            10 high-water / low-crop corner
  A03               LOW 0.20            25 low-water / high-crop stress corner
  A04              HIGH 0.70            25 high-high corner
  A05               MID 0.45            17 joint center
  A06               MID 0.45            25 watering-axis bridge
  A07              HIGH 0.70            17 crop-axis bridge

Le quattro celle A01-A04 costituiscono il contrasto 2×2 necessario per
separare main effects e interaction.

A05 verifica curvature/joint transition.

A06 localizza la transizione di servizio al crop load elevato.

A07 localizza la transizione di working-set sotto servizio elevato.

Nessuna delle sette celle può essere eliminata durante l'esecuzione
sulla base di risultati intermedi.

------------------------------------------------------------------------

# STAGE B --- LIVESTOCK × PASTURE

## 9. Ipotesi Stage B

### H-B1 --- HERD SCALE

A pasture footprint controllato, l'aumento della herd scale può
introdurre:

-   acquisition burden;
-   feed burden;
-   CARE burden;
-   dispatch burden;
-   cash pressure;
-   displacement della crop capacity.

La relazione può essere non monotona e condizionale.

### H-B2 --- PASTURE OPPORTUNITY COST

A herd size fissato, pasture aggiuntiva può sottrarre superficie arabile
e capacità di routing senza produrre valore proporzionale.

L'obiettivo è separare herd scale e pasture footprint, che in E15 erano
fortemente confusi.

------------------------------------------------------------------------

## 10. Determinazione preregistrata di `C*`

Stage B viene eseguito solo se Stage A identifica un crop working-set
capacity anchor.

Sono eleggibili esclusivamente:

``` text
A02 -> crop target 10 / HIGH watering
A07 -> crop target 17 / HIGH watering
A04 -> crop target 25 / HIGH watering
```

Per ciascuna cella calcolare:

``` text
completion_rate
median post-ramp watering_execution_rate
median watering_continuity
median crop_target_attainment
```

Steady window:

``` text
dal terzo full day successivo a T0
fino all'inizio del common endgame shutdown
```

Una cella è:

``` text
CAPACITY_ELIGIBLE
```

se soddisfa contemporaneamente:

``` text
completion_rate >= 0.80
median watering_execution_rate >= 0.60
median watering_continuity >= 0.75
median crop_target_attainment >= 0.80
```

Questi sono **advancement criteria procedurali**, non feature thresholds
appresi e non optima.

Definire:

``` text
C* = largest crop target among CAPACITY_ELIGIBLE cells
```

`final_money` e opponent money sono **vietati** come input della regola.

Se nessuna cella è eleggibile:

``` text
STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR
```

Stage B non viene eseguito.

Non è permesso sostituire post hoc target, watering level, seed o
soglia.

------------------------------------------------------------------------

## 11. Celle Stage B

Tutte le celle B utilizzano:

``` text
watering_dispatch_priority = HIGH 0.70
crop_working_set_target = C*
quadrants_owned = 2
workforce_headcount = 10
species = Cow
```

  Cell     Herd target   Pasture target Ruolo
  ------ ------------- ---------------- -------------------------------
  B01                4                5 compact baseline
  B02                4               18 pasture-only excess sentinel
  B03               10               11 middle herd / support pasture
  B04               10               18 middle herd / excess pasture
  B05               17               18 E15 failure-scale herd anchor

Contrasti primari:

``` text
Pasture effect at herd 4:
B02 - B01

Pasture effect at herd 10:
B04 - B03

Pasture × herd interaction:
(B04 - B03) - (B02 - B01)

Herd response at fixed pasture 18:
B02 -> B04 -> B05
```

La sequenza:

``` text
B01 -> B03 -> B05
```

può essere descritta solo come supported-bundle scale response, perché
herd e pasture cambiano insieme.

------------------------------------------------------------------------

# SEED / SEAT / RUN PROTOCOL

## 12. Seed

Usare i primi due seed preregistrati del proposal Codex:

``` text
seed_1 = 1802163452
seed_2 = 1678077158
```

Provenance:

``` text
SHA256("E16-CODEX-TRAINING-SEED-1") first unsigned 32 bits
SHA256("E16-CODEX-TRAINING-SEED-2") first unsigned 32 bits
```

Questi seed sono TRAINING seeds.

Non possono essere sostituiti, esclusi o modificati dopo l'osservazione
dei risultati.

Il terzo seed proposto da Codex:

``` text
935131029
```

non appartiene al frozen E16 execution set e non deve essere aggiunto
post hoc.

------------------------------------------------------------------------

## 13. Seat swap

Per ogni cella e seed eseguire due episodi:

``` text
episode 1:
treatment = P0
frozen opponent = P1

episode 2:
frozen opponent = P0
treatment = P1
```

Unità di blocking:

``` text
(seed, treatment_seat)
```

Il seat swap è obbligatorio.

------------------------------------------------------------------------

## 14. Episodi totali

Stage A:

``` text
7 cells × 2 seeds × 2 seats = 28 episodes
```

Stage B, se autorizzato dal gate:

``` text
5 cells × 2 seeds × 2 seats = 20 episodes
```

Totale massimo:

``` text
48 episodes
```

Se Stage B è bloccato:

``` text
28 episodes
```

Nessuna cella può essere fermata anticipatamente per performance
economica bassa.

------------------------------------------------------------------------

# INSTRUMENTATION GATE

## 15. E0 --- smoke validation

Prima di qualunque episodio TRAINING deve essere superato un
instrumentation gate.

Smoke run e test tecnici:

-   non sono TRAINING evidence;
-   non contano nei 28/48 episodi;
-   non possono aggiornare MODEL_SPEC o bound.

Devono verificare almeno:

1.  event ledger presente;
2.  requested vs accepted vs executed vs failed/no-op distinguibili;
3.  `realized_price` e `realized_value` riconciliabili;
4.  cash before/after riconciliabile;
5.  inventory flow riconciliabile;
6.  failure reasons non mancanti;
7.  treatment build hash corretto;
8.  opponent frozen hash corretto;
9.  configuration hash corretto;
10. `quadrants_owned` numerico distinto dagli ID Q0/Q1/Q2.

Qualunque errore di riconciliazione blocca E16.

------------------------------------------------------------------------

# TELEMETRIA

## 16. Event ledger minimo

Ogni record deve contenere almeno:

``` text
design_id
stage
cell_id
episode_id
seed
treatment_seat
player
step
day
hour
actor_or_order_id
actor_or_order_type
target_tile_or_commodity
requested_payload
executed_payload
success
failure_or_noop_reason
requested_quantity
executed_quantity
displayed_price_at_request
realized_price
realized_value
cash_flow_category
cash_before
cash_after
relevant_state_before
relevant_state_after
provenance
treatment_build_sha256
opponent_sha256
engine_version
configuration_sha256
quadrants_owned
```

Stati minimi addizionali:

``` text
assigned_crop_target
achieved_crop_surface
assigned_watering_priority
watering_need_denominator
successful_watering_effects
assigned_herd_target
achieved_herd
assigned_pasture_target
achieved_pasture
workforce_state
pasture_occupancy
feed_demand
feed_coverage
purchase_to_activation_lag
necessary_transit
avoidable_transit
terminal_inventory_by_product
unsold_inventory_quantity
unsold_inventory_value_estimate
```

`unsold_inventory_value_estimate` deve includere metodo di valutazione e
provenance e non può essere trattato come `realized_value`.

------------------------------------------------------------------------

## 17. Derived metrics

``` text
watering_execution_rate =
unique successful crop-day WATER effects
/
unique crop-day watering needs
```

``` text
watering_continuity =
productive days with watering_execution_rate >= 0.50
/
productive days
```

``` text
crop_target_attainment =
daily active crop surface
/
assigned crop target
```

``` text
pasture_occupancy =
occupied pasture
/
constructed pasture
```

``` text
action_failure_rate =
failed_or_noop actor actions
/
requested actor actions
```

Devono inoltre essere riportati separatamente:

-   active crop surface;
-   serviced crop surface;
-   surviving crop surface;
-   harvest-ready surface;
-   crop losses;
-   realized cash flow by category;
-   livestock acquisition/feed/service cost;
-   product units generated/collected/stored/sold;
-   terminal unsold inventory;
-   worker capacity/utilization;
-   necessary vs avoidable transit.

`final_money` non può essere incorporato in nessuna derived composite
feature.

------------------------------------------------------------------------

# ANALYSIS PLAN

## 18. Tre layer diagnostici

### MODEL_VALIDITY

Confronti primari basati sulla cella assegnata.

### POLICY_REALIZATION

Confronto fra trattamento assegnato e stato realmente raggiunto:

``` text
assigned watering vs executed watering
assigned crop target vs maintained crop surface
assigned herd vs achieved herd
assigned pasture vs achieved pasture
```

### IMPLEMENTATION_FIDELITY

Verifica:

-   hashes;
-   config allowlist;
-   event reconciliation;
-   action application;
-   missing/unknown failures;
-   engine consistency.

Se il trattamento assegnato non produce una differenza nel meccanismo
realizzato, non è consentito falsificare la relazione MODEL_SPEC sulla
sola base del risultato economico.

------------------------------------------------------------------------

## 19. Confronti Stage A

``` text
watering effect at crop 10:
A02 - A01

watering effect at crop 25:
A04 - A03

primary interaction:
(A04 - A03) - (A02 - A01)

watering transition at crop 25:
A03 -> A06 -> A04

crop transition under HIGH watering:
A02 -> A07 -> A04

joint-middle curvature:
A05 vs interpolation of corner cells
```

Per ogni `(seed, seat)` devono essere mostrati i raw paired values.

Con soli 2 seed:

-   non usare asymptotic p-values come prova;
-   non dichiarare statistical validation;
-   riportare sign consistency, median/range e valori grezzi;
-   un contrasto con direzione incoerente tra i due seed resta
    `UNRESOLVED`.

------------------------------------------------------------------------

## 20. Confronti Stage B

``` text
pasture opportunity cost at herd 4:
B02 - B01

pasture opportunity cost at herd 10:
B04 - B03

pasture × herd interaction:
(B04 - B03) - (B02 - B01)

herd response at fixed pasture 18:
B02 -> B04 -> B05
```

L'analisi economica livestock deve usare transazioni eseguite e cash
flow reale.

BUY/SELL request counts non costituiscono evidenza di valore realizzato.

------------------------------------------------------------------------

## 21. Completion e disqualification

Completion failure e disqualification sono outcomes sperimentali.

Non devono essere:

-   esclusi silenziosamente;
-   sostituiti;
-   imputati;
-   rerollati.

Per `final_money` e altre metriche quantitative, gli episodi non
completati possono essere esclusi dalla media della metrica solo se
riportati separatamente come failure outcome.

Il tasso di failure rimane parte dell'interpretazione della cella.

------------------------------------------------------------------------

## 22. Outlier e missing data

Con 2 seed non viene applicata alcuna rimozione statistica di outlier.

Non:

-   trim;
-   winsorize;
-   eliminare un seed per risultato estremo.

Mandatory telemetry missing:

-   non autorizza imputation;
-   rende la metrica non interpretabile;
-   può invalidare l'episodio per quella metrica;
-   può bloccare il round se il problema è sistematico.

------------------------------------------------------------------------

## 23. Rerun policy

Gameplay failure/disqualification:

``` text
NO RERUN
```

Provato infrastructure failure:

``` text
rerun ammesso solo con:
same cell
same seed
same seat
same treatment hash
same opponent hash
same engine hash
same configuration
```

Entrambi i tentativi restano nell'audit trail.

Nessun replacement seed.

------------------------------------------------------------------------

# CONCLUSIONI CONSENTITE E VIETATE

## 24. Consentite

E16 può:

-   identificare candidate failure regions;
-   identificare candidate transition regions;
-   identificare working regions sotto i controlli testati;
-   restringere regioni non osservate;
-   aggiornare FEATURE / UNRESOLVED status;
-   aggiornare candidate threshold/range;
-   discriminare model validity da realization/implementation failure;
-   preparare nuovi TRAINING round.

## 25. Vietate

E16 non può:

-   dichiarare optima;
-   dichiarare una globally best policy;
-   essere chiamato VALIDATION o TEST;
-   generalizzare a opponent non testati;
-   generalizzare a seed non testati;
-   inferire risultati su `quadrants_owned = 3`;
-   inferire workforce optimum;
-   inferire crop-mix optimum;
-   inferire Cow superiority;
-   inferire cash-floor optimum;
-   inferire routing optimum;
-   inferire endgame optimum;
-   usare E16 come independent validation futura;
-   usare requested action/order counts come prova di execution;
-   incorporare `final_money` in `state_capacity_alignment` o altra
    feature.

------------------------------------------------------------------------

# FREEZE REQUIREMENTS

## 26. Prima dell'esecuzione

L'implementazione E16 deve produrre e congelare:

``` text
treatment submission/build artifact
treatment sha256
configuration schema
12 cell definitions
2 training seeds
seat protocol
opponent artifact + sha256
engine/environment version
telemetry schema
analysis configuration
```

Il runner deve essere fail-closed su hash/config mismatch.

Le sole differenze di configurazione tra celle devono appartenere a una
allowlist esplicita dei MANIPULATED parameters.

------------------------------------------------------------------------

## 27. Freeze statement

``` text
E16 DESIGN STATUS = FROZEN
E16 EVIDENCE ROLE = TRAINING
E16 BASELINE quadrants_owned = 2
E16 OPPONENT = Copilot E15 frozen
E16 OPPONENT SHA256 =
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb

STAGE A = 7 cells × 2 seeds × 2 seats = 28 episodes
STAGE B = 5 cells × 2 seeds × 2 seats = 20 episodes
MAXIMUM = 48 episodes

STAGE B REQUIRES = preregistered capacity anchor C*
FINAL_MONEY IN ADVANCEMENT RULE = FORBIDDEN

OPTIMUM CLAIMS = FORBIDDEN
VALIDATION CLAIMS = FORBIDDEN
POST-HOC SEED/CELL SELECTION = FORBIDDEN
```

Il prossimo passo autorizzato è **IMPLEMENT E16**, preceduto
dall'instrumentation gate E0.
