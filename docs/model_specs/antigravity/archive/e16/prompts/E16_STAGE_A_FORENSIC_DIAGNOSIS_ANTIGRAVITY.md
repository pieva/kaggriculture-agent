# E16-A --- FORENSIC DIAGNOSIS PROMPT --- ANTIGRAVITY

## Ruolo

Agisci come **forensic analyst** sui 28 episodi già completati di E16
Stage A.

Non sei autorizzato a modificare la policy, il disegno sperimentale
frozen, i risultati, i seed, le celle o gli artifact E16.

Il tuo compito è esclusivamente diagnostico: identificare perché
`watering_dispatch_priority = HIGH` non si traduce in
`watering_execution_rate` e `watering_continuity` adeguati nello steady
state.

------------------------------------------------------------------------

## 1. Fonti da leggere

Leggi integralmente:

``` text
experiments/archive/e16/design/E16_TRAINING_DESIGN_FROZEN.md
experiments/archive/e16/artifacts/analysis/E16_STAGE_A_ANALYSIS.md
experiments/archive/e16/artifacts/analysis/E16_STAGE_B_GATE.json
experiments/archive/e16/artifacts/stage_a/E16_STAGE_A_RUN_MANIFEST.json
experiments/archive/e16/artifacts/instrumentation/E16_E0_REPORT.md
```

Poi analizza i raw episode JSON e la telemetry E16 Stage A.

------------------------------------------------------------------------

## 2. Vincoli

NON:

-   modificare codice;
-   modificare config;
-   rilanciare episodi;
-   correggere la policy;
-   proporre tuning numerico come se fosse già validato;
-   eseguire Stage B;
-   aggiornare MODEL_SPEC;
-   trasformare correlazioni in cause;
-   usare solo `final_money` per spiegare i risultati.

Mantieni distinti:

``` text
MODEL_VALIDITY
POLICY_REALIZATION
IMPLEMENTATION_FIDELITY
```

------------------------------------------------------------------------

## 3. Domanda principale

Spiega, sulla base della telemetry osservata:

``` text
perché HIGH watering intent
non produce HIGH watering execution/continuity
nello steady state?
```

Ricostruisci la catena causale candidata, senza saltare passaggi:

``` text
assigned intent
→ action demand
→ actor availability
→ dispatch
→ movement/transit
→ execution/no-op/failure
→ crop survival
→ crop target attainment
→ economic outcome
```

------------------------------------------------------------------------

## 4. Diagnosi richiesta

Quantifica per cella A01-A07 e, dove possibile, per seed/seat:

1.  numero e quota di WATER richieste;
2.  WATER eseguite con successo;
3.  WATER failed/no-op;
4.  motivi di fallimento/no-op;
5.  worker time/capacity disponibile;
6.  worker utilization;
7.  competing action classes:
    -   feed;
    -   livestock care;
    -   harvest;
    -   planting/replanting;
    -   trade;
    -   movement;
    -   weed/maintenance;
    -   altre azioni;
8.  necessary transit vs avoidable transit;
9.  crop mortality/loss prima e dopo T0;
10. active/serviced/surviving/harvest-ready surface;
11. pasture/feed burden;
12. inventory/trade burden;
13. cash stalls e relative cause prossime;
14. eventuali differenze fra LOW/MID/HIGH che dimostrino che il
    trattamento è stato almeno parzialmente realizzato.

------------------------------------------------------------------------

## 5. Bottleneck ranking

Produci una classifica dei colli di bottiglia candidati usando questa
scala:

``` text
CONFIRMED
STRONGLY_SUPPORTED
SUPPORTED
WEAK
NOT_SUPPORTED
UNOBSERVABLE
```

Valuta almeno:

``` text
insufficient workforce capacity
watering dispatch ordering
routing/transit overhead
feed handling
livestock care
trade dispatch
harvest/plant competition
weed/maintenance load
cash starvation
crop mortality feedback loop
implementation defect
telemetry artifact
```

Per ciascuno indica:

``` text
evidence_for
evidence_against
affected_cells
seed/seat consistency
diagnostic_layer
confidence
```

------------------------------------------------------------------------

## 6. Cross-cell contrasts

Usa in particolare:

``` text
A01 vs A02   # stessa crop scale, LOW vs HIGH watering
A03 vs A04   # crop 25, LOW vs HIGH
A03 vs A06 vs A04  # LOW → MID → HIGH a crop 25
A02 vs A07 vs A04  # crop 10 → 17 → 25 con HIGH watering
A05 vs A07   # crop 17 MID vs HIGH
```

Cerca differenze nei meccanismi, non solo nel denaro finale.

------------------------------------------------------------------------

## 7. Failure chronology

Per almeno un episodio rappresentativo di:

``` text
A03
A04
A05
A07
```

ricostruisci una timeline sintetica:

``` text
T0
crop expansion
first service deficit
first crop mortality
first cash pressure
first repeated WATER miss
steady-state collapse or stabilization
endgame
```

Se due seed mostrano dinamiche diverse, mostra entrambe.

------------------------------------------------------------------------

## 8. Obiettivo per E16-A2

Alla fine NON progettare ancora un esperimento completo.

Produci invece una shortlist di massimo **3 causal bottleneck
hypotheses** che meritano discriminazione sperimentale in E16-A2.

Per ciascuna:

``` text
hypothesis_id
candidate_cause
mechanism
observed evidence
what would falsify it
minimal manipulated variable
critical control variables
minimum telemetry needed
```

Preferisci ipotesi che possano essere discriminate con pochi
esperimenti.

Non selezionare la prossima policy sulla base del maggiore
`final_money`.

------------------------------------------------------------------------

## 9. Output

Salva:

``` text
experiments/archive/e16/artifacts/analysis/E16_STAGE_A_FORENSIC_DIAGNOSIS.md
```

Concludi con:

``` text
FORENSIC_STATUS: COMPLETE | BLOCKED

TOP_BOTTLENECK_1: ...
CONFIDENCE: ...

TOP_BOTTLENECK_2: ...
CONFIDENCE: ...

TOP_BOTTLENECK_3: ...
CONFIDENCE: ...

IMPLEMENTATION_DEFECT_DETECTED: YES | NO | UNRESOLVED

MODEL_VALIDITY_STATUS:
  ...

POLICY_REALIZATION_STATUS:
  ...

IMPLEMENTATION_FIDELITY_STATUS:
  ...

E16_A2_HYPOTHESES_READY: YES | NO

FILES_CHANGED:
  experiments/archive/e16/artifacts/analysis/E16_STAGE_A_FORENSIC_DIAGNOSIS.md
```

Non modificare altri file salvo output diagnostici strettamente
necessari.

Il compito termina con la diagnosi, senza implementazione e senza nuovi
run.
