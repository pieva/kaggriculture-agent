# Prompt operativo Codex — E16 Tile Lifecycle Feature Audit

## Ruolo

Operi come **agente di analisi semantica e di feature engineering controllato** sul repository Kaggriculture.

La forensic diagnosis E16-A-R1 ha identificato come bottleneck primario il `PLANTING / REPLANTING LOOP`, con due componenti direttamente supportate:

- tentativi HARVEST prematuri rispetto a `first_yield_day`;
- perdita di tile del working set verso `WEED`, che nella policy frozen diventa irreversibile per assenza di recovery.

Il supervisore propone di verificare una direzione più preventiva:

> rappresentare esplicitamente il **ciclo di vita della tile** come stato/feature operativa, in modo che la policy possa intervenire **prima** che una tile produttiva degradi o venga persa.

Questa sessione NON deve implementare un nuovo trattamento né modificare i MODEL_SPEC frozen. Deve stabilire se tale feature è semanticamente fondata, osservabile online e utile per un successivo esperimento di TRAINING.

---

## 1. Obiettivo principale

Rispondere rigorosamente a:

> **Esiste nel motore Kaggriculture uno stato o una sequenza di stati osservabile prima della perdita della tile che consenta di definire una feature `tile_lifecycle_state` e/o `crop_decay_risk_window` senza future leakage?**

e, se sì:

> **quali variabili minime deve contenere la feature affinché il dispatcher possa distinguere una tile sana, una tile che richiede servizio imminente, una tile pronta alla raccolta, una tile post-harvest da ripristinare e una tile già persa?**

La priorità metodologica è **prevenzione > recovery**.

`DIG` deve essere trattato come eventuale recovery residuale, NON come soluzione primaria assunta a priori.

---

## 2. Evidenza già disponibile da rispettare

La forensic diagnosis R1 ha stabilito:

- `PLANTING / REPLANTING LOOP = PRIMARY`;
- 5,804 / 5,804 crop-HARVEST falliti prima del requisito engine `first_yield_day`;
- tutte le 28 run espongono almeno una tile nominale come `WEED`;
- zero eventi `DIG`;
- A02 raggiunge 10/10 ma decade fino a circa 1 tile attiva;
- A07 raggiunge 15/17 ma decade fino a circa 1.5;
- A04 raggiunge solo 16/25 e decade fino a circa 2;
- WATER HIGH execution/continuity resta adeguato e non è il bottleneck primario;
- seed replenishment non è supportato come causa primaria;
- routing e workforce sono amplificatori secondari.

Non reinterpretare questi finding.

---

## 3. Collegamento con l'ontologia esistente

Verifica esplicitamente i concetti già presenti nella documentazione, in particolare:

- `crop_care_action_flow`
- `crop_harvest_action_flow`
- `crop_care_completion_rate`
- `crop_decay_risk_window`
- `crop_surface_maintained`
- `maintained_productive_surface`

`crop_decay_risk_window` risulta già definito ontologicamente come concetto PROVISIONAL / ENGINE_RULE_NEEDED.

Scopo della sessione:

- verificare se il motore consente di promuoverlo a concetto semanticamente verificato;
- NON modificare direttamente l'ontologia frozen;
- produrre una proposta di mapping e evidence status per successiva revisione umana/indipendente.

---

## 4. Vincoli non negoziabili

### NON fare

- NON modificare MODEL_SPEC.
- NON modificare ONTOLOGY frozen.
- NON modificare treatment policy frozen.
- NON eseguire Stage B.
- NON creare nuove submission Kaggle.
- NON avviare nuovi episodi di TRAINING per generare evidenza.
- NON fare tuning.
- NON introdurre threshold arbitrari.
- NON creare un risk score opaco se il motore fornisce già condizioni meccaniche esplicite.
- NON usare informazioni future/non disponibili alla policy al momento della decisione.
- NON assumere che ogni WEED sia prevenibile.
- NON assumere che `DIG` sia necessario se la perdita può essere evitata a monte.

### È consentito

- ispezionare il codice engine/environment;
- leggere policy, telemetry, R1 ledgers e artefatti diagnostici;
- produrre script diagnostici read-only;
- verificare la computabilità online delle feature;
- ricostruire transizioni tile-level dai dati esistenti;
- creare report e tabelle diagnostiche;
- aggiungere test solo per script/feature extractor diagnostici separati dalla policy, se strettamente necessario.

---

## 5. STEP 0 — Preflight

Esegui:

```powershell
git branch --show-current
git status --short
git log -1 --oneline
```

Non inglobare né modificare file appartenenti alla pulizia documentale concorrente di Antigravity.

Identifica:

- engine/environment Kaggriculture;
- struttura dati della tile;
- crop definitions;
- regole WATER;
- regole HARVEST;
- regole di maturazione;
- regole di perdita/degrado;
- regole di comparsa WEED;
- regole DIG/clear;
- telemetry già disponibile per tile.

---

## 6. STEP 1 — Ricostruire la macchina a stati reale della tile

Deriva **dal codice del motore**, non da supposizioni, la state machine di una tile appartenente al crop working set.

Documenta le transizioni effettive, per esempio solo se supportate:

```text
EMPTY / SOIL
    ↓ PLANT
PLANTED
    ↓ growth / care
GROWING
    ↓ maturity
HARVEST_READY
    ↓ HARVEST
POST_HARVEST / REGROWING / EMPTY
    ↓ ...
```

e le transizioni di perdita:

```text
<productive state>
    ↓ missed care / engine event / other cause
DEGRADED
    ↓
WEED / LOST
```

Non inventare stati logici che il motore non distingue: se servono stati derivati, marcarli `DERIVED`.

Per ogni transizione indica:

- condizione engine;
- variabili coinvolte;
- se deterministica o probabilistica;
- se osservabile online dalla policy;
- azione che può prevenirla;
- eventuale azione di recovery;
- costo minimo in worker actions;
- eventuale costo economico;
- effetto sulla revenue opportunity.

---

## 7. STEP 2 — Determinare come nasce WEED

Questa è la domanda critica.

Stabilisci dal motore:

1. se `WEED` deriva direttamente da mancata cura/mancato WATER;
2. se può apparire stochasticamente;
3. su quali tile state può apparire;
4. se può sostituire una crop viva;
5. se esiste un intervallo tra ultimo servizio corretto e conversione a WEED;
6. quali segnali sono osservabili prima della transizione;
7. se il rischio dipende da:
   - crop age;
   - water state;
   - last watered;
   - maturity;
   - harvest state;
   - time since harvest;
   - tile state;
   - giorno/ora;
   - random draw;
   - altri fattori engine.

Classifica ogni causa come:

- `DETERMINISTIC_PREVENTABLE`
- `STOCHASTIC_PARTIALLY_PREVENTABLE`
- `STOCHASTIC_NOT_PREVENTABLE`
- `UNRESOLVED`

Questa classificazione deve determinare se la strategia `prevention > DIG recovery` è realmente supportata.

---

## 8. STEP 3 — HARVEST lifecycle semantics

Formalizza esattamente la readiness HARVEST.

Individua:

- variabili engine necessarie;
- relazione tra `yield_units`, `planted_day`, crop age e `first_yield_day`;
- eventuali cooldown / repeat harvest / multi-harvest semantics;
- stato dopo harvest;
- quando è necessario replant;
- quando NON deve essere generato un task HARVEST.

Definisci una funzione concettuale verificabile, ad esempio:

```text
harvest_ready(tile, crop, current_day) -> bool
```

solo usando informazioni disponibili online.

Non implementarla nella policy in questa sessione.

---

## 9. STEP 4 — Candidate `tile_lifecycle_state`

Proponi la **rappresentazione minima**, evitando feature proliferation.

Valuta se basti una feature categoriale derivata, per esempio:

```text
UNASSIGNED
EMPTY_ASSIGNED
PLANTED_GROWING
CARE_DUE
HARVEST_READY
POST_HARVEST_REPLANT_DUE
AT_RISK
LOST_WEED
```

oppure se il motore richieda una rappresentazione diversa.

Per ogni stato candidato indica:

- definizione deterministica;
- variabili sorgente;
- computabile online: YES/NO;
- future leakage: YES/NO;
- engine-supported / derived;
- azioni valide;
- azioni da NON emettere;
- transizione successiva attesa.

Non mantenere categorie ridondanti.

---

## 10. STEP 5 — Candidate `crop_decay_risk_window`

Verifica se può essere definita una feature temporale meccanicamente fondata, ad esempio:

```text
time_to_required_service
time_since_last_required_service
time_to_maturity
time_since_maturity
time_to_loss
```

SOLO se il motore rende tali quantità determinabili senza conoscere il futuro.

Se `time_to_loss` dipende da RNG non osservabile, NON rappresentarlo come countdown deterministico.

In quel caso proponi una formulazione corretta, ad esempio:

```text
decay_risk_eligible
```

o un hazard/state condition basato esclusivamente sull'informazione disponibile.

La sessione deve dire esplicitamente se `crop_decay_risk_window` può passare da:

```text
PROVISIONAL / ENGINE_RULE_NEEDED
```

a uno status più forte.

---

## 11. STEP 6 — Prevention actionability

Per ogni stato/risk condition determina quale intervento **prima della perdita** è semanticamente possibile.

Considera almeno:

- WATER;
- valid HARVEST;
- REPLANT;
- worker reassignment;
- task priority escalation;
- eventuale sospensione di task non critici.

Distingui:

```text
PREVENTIVE ACTION
```

da:

```text
RECOVERY ACTION
```

`DIG` appartiene al secondo gruppo salvo evidenza engine contraria.

Quantifica, dove possibile dai dati R1:

- quante tile loss erano precedute da una condizione rilevabile;
- quanto anticipo temporale era disponibile;
- quante azioni premature/inutili potevano essere eliminate;
- se il worker action budget liberato sarebbe temporalmente disponibile prima della perdita.

Non dichiarare causalità dove R1 non consente counterfactual.

---

## 12. STEP 7 — Offline replayability / feature coverage

Usando esclusivamente le 28 run R1:

verifica quale percentuale delle transizioni tile-level può essere classificata ex post con la candidate lifecycle feature.

Produci almeno:

- numero tile/transition osservabili;
- coverage;
- ambiguous transitions;
- pre-WEED detectable cases;
- non-preventable/stochastic cases se identificabili;
- premature HARVEST attempts che la nuova semantics avrebbe escluso;
- action opportunities potenzialmente liberate.

Se la telemetry esistente non basta, documenta esattamente il gap senza falsificare una ricostruzione.

---

## 13. STEP 8 — Feature proposal, NON MODEL_SPEC change

Produrre una proposta formale contenente:

### A. `tile_lifecycle_state`
- type;
- canonical definition;
- source variables;
- state values;
- engine evidence;
- online availability;
- relation to existing ontology concepts.

### B. `crop_decay_risk_window`
- confermare / ridefinire / respingere;
- definizione;
- evidence status proposto;
- limiti.

### C. Eventuali feature atomiche indispensabili
Solo se necessarie.

Per esempio:

```text
harvest_ready_valid
care_due
replant_due
working_set_member
```

Non introdurre feature duplicate se derivabili da `tile_lifecycle_state`.

---

## 14. Decision rule

Il report deve terminare con:

# SUPERVISOR DECISION INPUT

### Tile lifecycle feature
Una delle:

```text
SUPPORTED_FOR_TRAINING_TEST
SUPPORTED_WITH_TELEMETRY_GAP
NOT_SUPPORTED
```

### Preventive control potential
Una delle:

```text
HIGH
MODERATE
LOW
UNRESOLVED
```

### WEED preventability
Riportare la classificazione meccanica effettiva.

### Recommended minimal treatment
Descrivere il **minimo cambiamento sperimentale** che permetterebbe di testare la feature, senza implementarlo.

Preferire un trattamento preventivo e isolato.

### Recovery role
Specificare se `DIG` deve essere:

```text
NOT_REQUIRED_FOR_FIRST_TEST
RESIDUAL_SAFETY_RECOVERY
REQUIRED_BY_ENGINE_MECHANICS
UNRESOLVED
```

### Ontology implication
Dire se `crop_decay_risk_window` può essere promosso, ridefinito o deve restare provisional.

### Stage B
Deve rimanere:

```text
STAGE B: BLOCKED
C*: NONE
```

---

## 15. Output richiesto

Crea un report:

```text
results/e16/diagnostics/tile_lifecycle_feature/
E16_TILE_LIFECYCLE_FEATURE_AUDIT.md
```

e, se utile:

- state transition table CSV;
- R1 lifecycle coverage CSV;
- machine-readable feature schema JSON;
- script diagnostico separato e read-only.

Non sovrascrivere gli artefatti forensic R1 esistenti.

---

## 16. Stop condition

Al termine:

1. riporta file creati/modificati;
2. riporta test/comandi eseguiti;
3. riporta la state machine verificata;
4. riporta la decisione sulla feature;
5. riporta la prevenibilità delle WEED;
6. riporta il trattamento minimo consigliato;
7. riporta eventuali telemetry gaps;
8. mostra `git status --short`.

Poi **FERMATI**.

NON implementare la nuova policy.
NON creare un nuovo esperimento.
NON modificare MODEL_SPEC/ONTOLOGY frozen.
NON eseguire Stage B.
