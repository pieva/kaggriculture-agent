# Antigravity — STATE MACHINE C2

## Obiettivo

Costruire il candidato **State Machine C2** della Model Foundation, partendo dalla State Machine C1 già accettata come sostanzialmente corretta e recependo esclusivamente le revisioni richieste dalla Foundation Reconciliation R1 e dalla nuova Ontologia C2.

Questa è una revisione **REVISE_LIGHT**, non una riscrittura architetturale.

Non iniziare `FEATURE_MODEL_C2`, `MODEL_SPEC_C2`, consumer matrix, runtime implementation, policy changes, training o nuovi esperimenti.

---

# 1. Fonti normative

Usare almeno:

```text
docs/foundation/ontology/ONTOLOGY_C2.md
docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C1.md
docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C1.md
docs/governance/foundation/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md
docs/governance/foundation/copilot/COPILOT_FOUNDATION_REVIEW_R1.md
docs/governance/foundation/reconciliation/CODEX_FOUNDATION_RECONCILIATION_R1.md
```

La **Foundation Reconciliation R1 di Codex** resta l'arbitrato normativo.

La nuova `ONTOLOGY_C2.md` è l'upstream semantico candidato da rispettare.

Non riaprire finding già arbitrati salvo contraddizione fattuale diretta e documentabile.

---

# 2. Output

NON sovrascrivere C1.

Creare:

```text
docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
```

con stato:

```text
CANDIDATE C2
NOT FROZEN
UPSTREAM: ONTOLOGY_C2 CANDIDATE
DERIVED FROM FOUNDATION RECONCILIATION R1
```

La C1 deve restare disponibile per confronto.

---

# 3. Principio di revisione

Preservare tutto ciò che in C1 è già supportato e non contraddetto.

La review Antigravity aveva dato:

```text
STATE_MACHINE_C1: ACCEPT
```

La reconciliation finale ha dato:

```text
STATE_MACHINE_C1: REVISE_LIGHT
```

Quindi:

- non ridisegnare la macchina globale;
- non inventare nuovi stati per completezza estetica;
- non trasformare policy in engine semantics;
- correggere solo precisione temporale, lifecycle e meccaniche ora meglio formalizzate.

---

# 4. MUST — Clock e phase semantics

Formalizzare esplicitamente due concetti distinti.

## 4.1 Engine clock

Quando una regola engine utilizza `step`, questo è l'orologio autorevole della regola.

Non sostituire automaticamente `step` con `canonical_step`.

## 4.2 Diagnostic canonical clock

Preservare:

```text
canonical_step = day * turnsPerDay + hour
```

come ricostruzione diagnostica deterministica utile quando la telemetria `observation.step` è difettosa o incompleta.

Esplicitare:

```text
engine_step != canonical_step by definition
```

anche se in condizioni normali possono coincidere numericamente.

Il primo è una variabile engine; il secondo è una derivazione osservazionale/diagnostica.

## 4.3 Phase contract

Per le transizioni/deadline rilevanti specificare la fase temporale in cui avvengono, coerentemente con il loop engine già verificato:

1. inizializzazione stato se necessario;
2. lettura azioni;
3. validazione atomica PLANT same-player per crop;
4. applicazione azione main farmer;
5. applicazione azioni hands;
6. market orders;
7. town consumption;
8. `_decay_plants`;
9. EOD refresh quando il giorno termina;
10. aggiornamento day/hour;
11. eventuale terminal reward.

Verificare l'esatto ordine contro C1/reconciliation e non modificarlo senza evidenza.

Indicare quale clock/fase governa almeno:

- HARVEST maturity;
- lifespan decay;
- WATER deadline/EOD loss;
- fertilizer window;
- livestock production/escape;
- random EMPTY→WEED spawn.

---

# 5. MUST — Crop/tile lifecycle C2

Recepire semanticamente `ONTOLOGY_C2`.

Preservare i sei stati lifecycle candidati:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

Ma NON dichiarare ancora che esista un classifier totale eseguibile già validato.

La State Machine deve descrivere transizioni e condizioni supportate; il classifier totale con predicati, precedence, fallback e boundary tests sarà formalizzato downstream.

## 5.1 HARVEST readiness

Correggere ogni semantica che possa implicare:

```text
yield_units > 0 => HARVEST_READY
```

La readiness richiede semanticamente:

```text
tile.kind == PLANT
AND tile.yield_units > 0
AND day - tile.planted_day >= CROPS[tile.crop].first_yield_day
```

Distinguere:

```text
yield available
!=
harvest ready
```

Preservare la differenza fra colture ongoing e non-ongoing.

## 5.2 Non-ongoing

Per HARVEST valido:

```text
HARVEST_READY
    -> inventory receives yield
    -> tile becomes None / EMPTY_ASSIGNED when in working-set scope
```

La successiva PLANT è una nuova transizione, non parte implicita di HARVEST.

## 5.3 Ongoing

Per HARVEST valido:

```text
HARVEST_READY
    -> inventory receives yield
    -> yield_units = 0
    -> tile remains PLANT
    -> GROWING/regrowth
```

Dopo l'ultima produzione prevista, rappresentare correttamente l'ingresso semantico in:

```text
RETIREMENT_DUE
```

quando la coltura non ha più una produzione futura utile prevista ma la tile resta occupata.

Non introdurre qui una policy obbligatoria di DIG: descrivere la transizione engine possibile.

---

# 6. MUST — CARE_DUE ortogonale

`tile_care_due_condition` / `care_due` non deve diventare uno stato strutturale alternativo ai sei lifecycle states.

Rappresentarlo come condizione ortogonale applicabile a una tile PLANT nei lifecycle states pertinenti.

Per missed-WATER:

- una nuova PLANT nasce con `consecutive_unwatered = 1`;
- EOD watered -> reset a 0;
- EOD not watered -> incremento;
- se raggiunge la soglia engine verificata -> WEED.

Formalizzare la condizione meccanica di perdita a EOD senza trasformarla in una priorità policy.

---

# 7. MUST — WEED causes

Preservare esplicitamente le tre famiglie causalmente distinte:

```text
1. missed-WATER deterministic loss
2. deterministic lifespan loss
3. stochastic random spawn on EMPTY
```

Non introdurre un singolo `time_to_weed`.

Per random EMPTY→WEED:

- rappresentare eligibility/hazard;
- non rappresentare un countdown deterministico;
- RNG/seed non osservabile non deve entrare come feature decisionale.

---

# 8. MUST — DIG semantics

Recepire la distinzione ontologica:

```text
preventive_dig_action
recovery_dig_action
```

### Preventive DIG

Può liberare una tile occupata da una coltura esaurita / `RETIREMENT_DUE` prima della degradazione successiva.

### Recovery DIG

Può bonificare:

```text
LOST_WEED -> EMPTY_ASSIGNED
```

Non presentare recovery DIG come risposta primaria alle cause di perdita evitabili.

La State Machine deve descrivere capacità/transizioni engine, non imporre strategia.

---

# 9. MUST — Worker occupancy e serviceability

Promuovere a `ENGINE_VERIFIED`:

```text
worker_multi_occupancy
```

ovvero più worker possono condividere la stessa coordinata senza collisione engine che renda illegale la posizione.

Ma distinguere rigorosamente:

```text
tile_need
action_eligible_now
serviceable_before_deadline
```

La co-location non dimostra automaticamente serviceability.

Non completare `serviceable_before_deadline` se richiede ancora contratti su:

- reachability;
- actor position;
- action phase;
- inventory;
- routing;
- policy memory;
- deadline.

Marcarlo `PARTIALLY_KNOWN` dove necessario.

---

# 10. SHOULD — FERTILIZE

Integrare nella State Machine le sole meccaniche engine già verificate in Ontology C2:

```text
fertilized_until_day = max(fertilized_until_day, day + 2)
```

con finestra inclusiva:

```text
day .. day+2
```

e il bonus crop esatto documentato:

- +2 yield per refresh su ongoing irrigata quando fertilizzazione attiva;
- +2 yield per WATER nella finestra di resa delle non-ongoing quando fertilizzazione attiva;

solo se questa è la formulazione effettivamente verificata e riportata in `ONTOLOGY_C2.md`.

Non inferire convenienza economica o adozione policy.

---

# 11. SHOULD — Livestock FEED + CARE

Formalizzare la meccanica engine verificata:

```text
CARE -> pending_care_bonus accumulation
```

e il consumo/effetto del bonus nei production days secondo le condizioni engine supportate, incluso il requisito di alimentazione dove previsto.

Preservare come `PARTIALLY_KNOWN` o `NOT_ANALYZED`:

- convenienza economica;
- ROI;
- scheduling ottimo;
- policy di feeding/care;
- interazione economica completa con fertilizer.

Non trasformare meccanica engine in strategia.

---

# 12. Inventory EOD correction

Allineare la State Machine a:

```text
shed_overflow_eod_loss
```

A EOD:

```text
worker inventories
    -> automatic transfer to shed up to capacity
    -> overflow beyond capacity lost
```

Eliminare qualsiasi semantica che implichi:

```text
worker must manually return before contract expiry
```

se presente.

Preservare la distinzione tra:

- worker inventory;
- shed capacity;
- automatic EOD transfer;
- overflow loss.

---

# 13. ENGINE / POLICY boundary

Rivedere la tabella/sezione di separazione ENGINE/POLICY.

Devono restare chiaramente POLICY, salvo evidenza contraria:

```text
working set selection
crop mix
numeric WATER level
routing
cash floor
worker target
shutdown
land expansion strategy
market pacing
serviceability heuristics
```

Devono restare ENGINE/derived semantics:

```text
maturity predicate inputs
WATER loss mechanics
lifespan decay
random weed eligibility
FERTILIZE duration/effect
worker co-location legality
automatic EOD inventory transfer
livestock production/escape mechanics supportate
```

---

# 14. Diagrammi e tabelle

Aggiornare Mermaid/tabelle solo con transizioni supportate.

Non inserire nei diagrammi:

- optimum;
- soglie apprese;
- target di policy;
- formule aggregate non congelate;
- serviceability non dimostrata;
- deterministic random-WEED countdown.

Se una condizione è `PARTIALLY_KNOWN`, renderlo esplicito nel testo anziché farla apparire certa nel diagramma.

---

# 15. Cross-artifact impact

Alla fine aggiungere:

```text
## Impatto downstream per Foundation C2
```

Separare:

```text
FEATURE_MODEL_C2
MODEL_SPEC_C2
CONSUMER MATRIX / RUNTIME TRACE
```

Non implementare questi artefatti.

Indicare almeno che Feature Model C2 dovrà:

- implementare il classifier lifecycle totale;
- formalizzare clock/phase dei derived features;
- separare need / eligibility / serviceability;
- definire aggregate contracts dove richiesti;
- restare consumer-neutral.

---

# 16. Verifica differenziale C1 -> C2

Produrre nel documento o nel report una matrice sintetica:

```text
C1 element
C2 change
reason
evidence/reconciliation finding
status
```

Classificare ogni modifica come:

```text
UNCHANGED
CLARIFIED
CORRECTED
PROMOTED_EVIDENCE
ADDED_SUPPORTED
```

Questo serve a dimostrare che `REVISE_LIGHT` non è diventata una riscrittura incontrollata.

---

# 17. Verifiche repository

Eseguire:

```powershell
git diff --check
.\.venv\Scripts\pytest.exe
```

Se `ruff` fa parte dei check correnti, eseguirlo.

Poi:

```powershell
git status --short
git diff -- docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
```

Non eseguire episodi o benchmark.

Non fare commit.

---

# 18. Stop condition

Dopo la creazione e verifica di:

```text
docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
```

FERMARSI.

Non iniziare:

```text
FEATURE_MODEL_C2
MODEL_SPEC_C2
consumer matrix
runtime trace
policy implementation
training
```

---

# Output finale richiesto

Restituire in italiano:

1. path e stato del candidato State Machine C2;
2. principali modifiche C1 -> C2;
3. clock/phase contract adottato;
4. lifecycle e HARVEST readiness;
5. WEED/DIG semantics;
6. worker occupancy/serviceability;
7. FERTILIZE e FEED/CARE;
8. inventory EOD;
9. punti ancora `PARTIALLY_KNOWN` / `NOT_ANALYZED`;
10. downstream impact;
11. risultato `git diff --check`;
12. risultato test/lint;
13. `git status --short`;
14. eventuali problemi residui.

Chiudere con:

```text
ONTOLOGY C2: CANDIDATE / NOT FROZEN
STATE MACHINE C2: CANDIDATE CREATED / NOT FROZEN
FEATURE MODEL C2: NOT STARTED
MODEL_SPEC C2: NOT STARTED
FOUNDATION C2: NOT FROZEN
```

STOP.
