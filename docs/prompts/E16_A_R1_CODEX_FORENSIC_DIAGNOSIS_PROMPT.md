# Prompt operativo Codex --- E16-A-R1 Forensic Diagnosis

## Ruolo

Operi come **agente di analisi forense del repository Kaggriculture**.

Il tuo compito in questa sessione **non è correggere la policy,
ottimizzare l'agente o progettare direttamente E16-R2/Stage B**. Devi
determinare, usando esclusivamente le evidenze già prodotte da **E16
Stage A-R1**, perché la policy non riesce a mantenere il `crop_target`
nominale nonostante la correzione del dispatch WATER.

L'output deve permettere al supervisore umano di decidere quale sia il
prossimo esperimento di TRAINING.

------------------------------------------------------------------------

## 1. Stato sperimentale da assumere come vincolo

Stato corrente:

-   `E15`: CLOSED --- Copilot 2--0.
-   `E16 Stage A-R1`: COMPLETED --- 28/28 episodi.
-   `Stage B`: BLOCKED.
-   `C*`: NONE.
-   artefatti frozen: **UNCHANGED & LOCKED**.
-   test repository al checkpoint: `143/143 PASS`.

E16-A-R1 ha già stabilito:

-   HIGH watering execution rate: `0.8898–0.9416`;
-   watering continuity: circa `0.96` sulle celle HIGH;
-   il synthetic daily drought della precedente esecuzione contaminata è
    stato eliminato;
-   il WATER dispatch **non deve quindi essere assunto come bottleneck
    primario corrente**.

Risultati economici mediani:

  Cell   Water     Crop target   Median final money
  ------ ------- ------------- --------------------
  A01    LOW                10          \$19,694.00
  A02    HIGH               10          \$21,230.50
  A03    LOW                25          \$11,903.50
  A04    HIGH               25          \$19,987.00
  A05    MID                17          \$26,619.50
  A06    MID                25          \$21,570.50
  A07    HIGH               17          \$27,076.00

Contrasti già osservati:

-   `A02 - A01`: median `+$1,576.00`;
-   `A04 - A03`: median `+$8,587.00`;
-   primary interaction `((A04-A03)-(A02-A01))`: median `+$5,180.50`;
-   A07 / Crop 17 è la regione economicamente più promettente osservata,
    ma **non è un optimum né una capacity threshold**.

Capacity Gate frozen:

-   Completion `>= 0.80`
-   Watering Execution Rate `>= 0.60`
-   Watering Continuity `>= 0.75`
-   Crop Target Attainment `>= 0.80`

Fallimento del gate:

-   A02 attainment `0.4750`;
-   A07 attainment `0.4706`;
-   A04 attainment `0.3000`;
-   pertanto `CAPACITY_ELIGIBLE = NO` per tutte;
-   `C* = NONE`;
-   `STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR`.

------------------------------------------------------------------------

## 2. Principio metodologico

Mantieni rigorosamente separati questi tre livelli:

1.  **MODEL_VALIDITY** --- attualmente `STRONGLY SUPPORTED`.
2.  **POLICY_REALIZATION** --- nuovo bottleneck da discriminare.
3.  **IMPLEMENTATION_FIDELITY** --- verificata dopo le repair R1/R2/R3.

Non reinterpretare automaticamente il basso attainment come
falsificazione del modello.

Non trasformare una correlazione osservata in una causa.

Non trasformare Crop 17 in un optimum.

Non modificare le soglie frozen per far passare il gate.

------------------------------------------------------------------------

## 3. Obiettivo della diagnosi

Spiegare quantitativamente il deficit:

``` text
nominal crop target
        ↓
realized active crop working set
        ↓
crop_target_attainment < 0.80
```

Devi identificare **dove, quando e attraverso quale meccanismo
operativo** si perde la capacità necessaria a mantenere il working set
nominale.

Le famiglie causali candidate da discriminare sono almeno:

1.  `ROUTING / TRANSIT OVERHEAD`
2.  `WORKFORCE / ACTION CAPACITY`
3.  `SEED REPLENISHMENT`
4.  `PLANTING / REPLANTING LOOP`
5.  `MARKET PACING / CAPITAL AVAILABILITY`

Puoi identificare ulteriori meccanismi solo se emergono direttamente dai
dati R1.

------------------------------------------------------------------------

## 4. Vincoli non negoziabili

### NON fare

-   NON eseguire Stage B.
-   NON creare nuovi esperimenti.
-   NON eseguire nuovi episodi per produrre evidenza sperimentale.
-   NON modificare alcun `MODEL_SPEC`.
-   NON modificare ontologia o artefatti frozen.
-   NON modificare treatment policy frozen.
-   NON preparare submission Kaggle.
-   NON ottimizzare parametri o hyperparameter.
-   NON introdurre una patch della policy durante la diagnosi.
-   NON usare risultati di nuovi gameplay come scorciatoia diagnostica.
-   NON dichiarare una causa primaria senza evidenza quantitativa.
-   NON selezionare C\*.
-   NON reinterpretare retroattivamente i criteri frozen.

### È consentito

-   leggere codice, documentazione, configurazioni, risultati e ledger;
-   scrivere script diagnostici **read-only rispetto agli artefatti
    sperimentali**;
-   produrre tabelle, CSV/JSON diagnostici e report;
-   eseguire test repository;
-   verificare/calcolare metriche derivate dagli artefatti R1;
-   confrontare episodi/celle/giorni usando esclusivamente dati già
    esistenti.

Qualunque script diagnostico deve essere chiaramente separato dalla
policy e non deve alterare gli input o gli artefatti originali.

------------------------------------------------------------------------

## 5. Workflow obbligatorio

### STEP 0 --- Repository preflight

Prima di qualsiasi analisi:

1.  mostra branch corrente;
2.  mostra `git status --short`;
3.  mostra ultimo commit;
4.  verifica presenza e struttura almeno di:
    -   `results/e16/stage_a_r1/`
    -   `results/e16/analysis/`
5.  identifica i file contenenti:
    -   episode summaries;
    -   event ledgers;
    -   cell/config metadata;
    -   derived metrics;
    -   integrity report;
6.  verifica che gli artefatti frozen attesi siano presenti e non
    modificati;
7.  esegui i test appropriati o la suite completa se ragionevole.

Se trovi working tree sporco o divergenze che potrebbero contaminare la
diagnosi, **non correggerle automaticamente**: documentale e valuta se
impediscono l'analisi.

### STEP 1 --- Data inventory

Costruisci un inventario dei 28 episodi R1.

Per ogni episodio identifica almeno:

-   cella A01--A07;
-   seed;
-   water priority;
-   nominal `crop_target`;
-   durata/completion;
-   final money;
-   crop target attainment;
-   watering execution rate;
-   watering continuity;
-   workforce disponibile/attiva, se telemetrata;
-   quantità/eventi di seed acquisition, se telemetrati;
-   planting/replanting events;
-   harvest events;
-   movement/transit events o proxy ricostruibili;
-   market/buy/sell events;
-   eventuali idle/no-op/action-failure events.

Non inventare campi assenti. Distingui:

-   **direct telemetry**;
-   **derived metric**;
-   **proxy/inference**.

### STEP 2 --- Ricostruzione temporale del working set

Per ogni episodio, ricostruisci per quanto possibile una serie temporale
del numero di crop tile:

-   nominalmente richiesti;
-   effettivamente planted/active;
-   harvest-ready;
-   harvested ma non ancora replanted;
-   eventualmente dead/dry/weeded/unproductive, se distinguibili.

Preferisci granularità per turn; aggrega anche per day quando utile.

Calcola almeno, se supportato dai dati:

-   `active_crop_count(t)`;
-   `target_gap(t) = crop_target - active_crop_count(t)`;
-   tempo al primo raggiungimento di 50%, 80%, 100% target;
-   quota di tempo sopra 50%, 80%, 100% target;
-   durata media/mediana dei gap post-harvest prima del replant;
-   massima e mediana ampiezza del deficit;
-   deficit cumulativo, ad esempio area sotto `target_gap(t)`.

Se una metrica non è ricostruibile in modo affidabile, dichiaralo.

### STEP 3 --- Decomposizione causale del deficit

Analizza separatamente le cinque famiglie candidate.

#### 3A. Routing / transit overhead

Cerca evidenza che una quota significativa della capacità d'azione venga
assorbita da movimento.

Quantifica, se possibile:

-   movement actions / total actions;
-   distanza o turn di transito per ciclo produttivo;
-   tempo tra harvest e nuova attività produttiva;
-   differenze di routing tra target 10, 17 e 25;
-   relazione tra superficie/dispersione e attainment.

Obiettivo: determinare se l'aumento del target produce un costo di
routing incompatibile con il mantenimento del working set.

#### 3B. Workforce / action capacity

Quantifica domanda e offerta di azioni.

Cerca:

-   worker count nel tempo;
-   productive actions per worker/day;
-   backlog di WATER/PLANT/HARVEST/REPLANT;
-   competizione tra categorie di azioni;
-   saturazione della workforce;
-   eventuali idle actions nonostante backlog produttivo.

Verifica in particolare se il passaggio `10 → 17 → 25` produce una
crescita della domanda di azioni superiore alla capacità effettivamente
disponibile.

#### 3C. Seed replenishment

Ricostruisci il ciclo:

``` text
seed inventory
→ planting demand
→ seed purchase/acquisition
→ availability
→ plant/replant
```

Cerca episodi in cui tile disponibili e capacità di lavoro esistono ma
il planting è ritardato per assenza di seed.

Quantifica:

-   stockout;
-   durata stockout;
-   gap tra bisogno e acquisition;
-   gap tra acquisition e planting;
-   relazione stockout ↔ target gap.

#### 3D. Planting / replanting loop

Verifica se il sistema raggiunge inizialmente una quota ragionevole del
target ma non riesce a mantenerla dopo harvest o perdita di
produttività.

Quantifica:

-   initial ramp-up;
-   harvest→replant latency;
-   tile-time perso tra cicli;
-   backlog di replant;
-   decadimento del working set nel tempo;
-   eventuali differenze tra prima occupazione e mantenimento.

Questa analisi deve distinguere chiaramente:

``` text
failure to attain
```

da:

``` text
failure to maintain
```

#### 3E. Market pacing / capital availability

Verifica se le decisioni economiche impediscono seed acquisition,
workforce scaling o altre azioni necessarie al target.

Quantifica quando possibile:

-   cash disponibile nei momenti di deficit;
-   acquisti differiti;
-   eventuali periodi in cui il capitale è il vincolo attivo;
-   relazione tra market actions e ritardo del ciclo produttivo.

Non confondere una strategia economicamente redditizia con una strategia
capace di soddisfare il capacity gate.

------------------------------------------------------------------------

## 6. Confronti prioritari

La diagnosi deve sfruttare il disegno Stage A.

### Water effect a target costante

Confronta:

-   A01 LOW/10 vs A02 HIGH/10;
-   A03 LOW/25 vs A04 HIGH/25.

Scopo: verificare quali deficit restano anche quando WATER è realizzato
correttamente.

### Target scaling

Confronta le regioni:

-   target 10;
-   target 17;
-   target 25.

Scopo: identificare il punto in cui cresce il deficit operativo e quale
componente cresce con esso.

### Focus A07

A07 HIGH/17:

-   è economicamente la cella più promettente;
-   attainment = `0.4706`;
-   non è un optimum;
-   non è C\*.

Usala come caso diagnostico prioritario per capire come possa coesistere
**alta performance economica** con **bassa realizzazione della capacità
nominale**.

------------------------------------------------------------------------

## 7. Classificazione dell'evidenza

Per ogni finding importante assegna una classe:

-   `DIRECT` --- osservato direttamente nella telemetria/ledger;
-   `DERIVED` --- calcolato deterministicamente da dati osservati;
-   `INFERRED` --- spiegazione supportata ma non direttamente
    osservabile;
-   `UNRESOLVED` --- dati insufficienti per discriminare.

Per ogni candidato bottleneck assegna inoltre:

-   `PRIMARY`
-   `SECONDARY`
-   `NOT_SUPPORTED`
-   `UNRESOLVED`

solo se l'evidenza consente tale classificazione.

Se due cause sono interdipendenti, esplicita la catena causale invece di
forzare una classificazione artificiale.

------------------------------------------------------------------------

## 8. Test di falsificazione

Non cercare soltanto conferme.

Per ogni candidato bottleneck formula almeno una previsione che dovrebbe
essere osservabile nei 28 run se l'ipotesi fosse vera e cerca anche
controesempi.

Esempio concettuale:

``` text
Hypothesis:
workforce saturation causes low attainment.

Expected evidence:
target gap rises when productive-action demand approaches/exceeds available
worker action capacity.

Potential falsifier:
large target gaps persist while workers are idle and all required inputs
are available.
```

Applica lo stesso principio alle altre famiglie causali.

------------------------------------------------------------------------

## 9. Output richiesti

Crea una directory diagnostica coerente con la struttura esistente,
senza sovrascrivere artefatti R1.

Produci almeno:

### A. Report principale

`E16_A_R1_CROP_ATTAINMENT_FORENSIC_DIAGNOSIS.md`

Struttura minima:

1.  Executive diagnosis
2.  Data provenance & integrity
3.  Working-set reconstruction
4.  Temporal anatomy of crop-target deficit
5.  Routing analysis
6.  Workforce/action-capacity analysis
7.  Seed replenishment analysis
8.  Plant/replant loop analysis
9.  Market/capital pacing analysis
10. Cross-cell comparison
11. A07 forensic case
12. Falsification tests
13. Bottleneck classification
14. Evidence limitations
15. Implications for next TRAINING decision

### B. Evidence table

Produci una tabella machine-readable, preferibilmente CSV, con almeno:

``` text
finding_id
cell
episode/seed
time_window
candidate_bottleneck
metric/evidence
value
evidence_class
interpretation
supports
contradicts
source_artifact
```

### C. Episode/cell diagnostic summary

Una tabella sintetica con le metriche diagnostiche disponibili per tutti
i 28 episodi e aggregazioni per A01--A07.

### D. Event-level trace selettiva

Per almeno:

-   un episodio rappresentativo A02;
-   un episodio rappresentativo A07;
-   un episodio rappresentativo A04;

produci una timeline leggibile del ciclo:

``` text
movement → water → harvest → seed acquisition → plant/replant
```

o della sequenza realmente supportata dal ledger.

La selezione dell'episodio deve essere motivata (es. vicino alla mediana
della cella), non arbitraria.

------------------------------------------------------------------------

## 10. Decision rule finale

Il report deve terminare con una sezione:

# SUPERVISOR DECISION INPUT

contenente esclusivamente:

### Dominant diagnosis

Una delle forme:

``` text
PRIMARY BOTTLENECK: <name>
```

oppure:

``` text
NO SINGLE PRIMARY BOTTLENECK
```

oppure:

``` text
INSUFFICIENT EVIDENCE TO DISCRIMINATE
```

### Supporting evidence

Massimo 5 finding quantitativi, con riferimenti agli artefatti.

### Competing explanation

La migliore spiegazione alternativa e l'evidenza che la indebolisce o
mantiene aperta.

### Identifiability gap

Quale domanda causale, se presente, non può essere risolta dai 28 run
esistenti.

### Recommended next experimental question

Formula **la domanda sperimentale**, non implementare il trattamento.

Esempio di forma:

``` text
Does reducing X while holding Y constant increase crop-target attainment
without degrading watering continuity?
```

### Stage B status

Deve rimanere:

``` text
STAGE B: BLOCKED
C*: NONE
```

salvo che il supervisore umano approvi successivamente una diversa
decisione metodologica.

------------------------------------------------------------------------

## 11. Stop condition

Quando hai completato:

-   verifica repository;
-   analisi forense;
-   artefatti diagnostici;
-   test pertinenti;
-   `SUPERVISOR DECISION INPUT`;

**FERMATI.**

Non:

-   implementare il trattamento suggerito;
-   creare E16-R2/R4 o un nuovo esperimento;
-   modificare policy/model spec;
-   lanciare benchmark;
-   preparare Kaggle;
-   sbloccare Stage B.

Riporta infine:

1.  file creati/modificati;
2.  comandi/test eseguiti e relativo esito;
3.  diagnosi dominante;
4.  livello di confidenza;
5.  unresolved questions;
6.  `git status --short`.

Attendi la revisione del supervisore.
