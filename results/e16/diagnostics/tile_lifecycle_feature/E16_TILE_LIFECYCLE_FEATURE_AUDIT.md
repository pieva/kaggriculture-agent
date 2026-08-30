# E16 Tile Lifecycle Feature Audit

## 1. Scope e risposta

Questa e una verifica semantica e diagnostica read-only. Non modifica policy,
MODEL_SPEC, ontologia, configurazioni o risultati R1; non genera episodi e non
propone E16 Stage B.

**Risposta principale:** si. Il motore espone online, nella tile pubblica, gli
stati necessari a riconoscere readiness di raccolta, fabbisogno WATER, confine
deterministico di perdita idrica e decadimento di lifespan. Una feature
`tile_lifecycle_state` e quindi semanticamente fondata e priva di future
leakage. Una sola categoria piatta, pero, non basta: readiness HARVEST e
fabbisogno WATER sono ortogonali, soprattutto per le crop ongoing.

`crop_decay_risk_window` puo essere promosso sul piano della regola engine, ma
va ridefinito come vincolo strutturato multi-causa. Non puo essere un unico
countdown: il passaggio `EMPTY -> WEED` dipende da un draw RNG non osservabile.
La convalida longitudinale sui 28 replay resta parziale perche la telemetry R1
salva la tile dell'attore, non tutte le tile del working set a ogni step.

Decisione sintetica: `SUPPORTED_WITH_TELEMETRY_GAP`, con potenziale preventivo
`HIGH` ma senza una stima controfattuale dell'incremento di reward.

## 2. Preflight e provenienza

Comandi STEP 0:

```text
git branch --show-current  -> main
git log -1 --oneline       -> 178461c chore: consolidate historical prompts
git status --short         -> working tree gia dirty per pulizia documentale
                              concorrente e artefatti diagnostici precedenti
```

Le cancellazioni gia presenti sotto `docs/experiments`, `docs/plans` e
`docs/walkthroughs` non sono state toccate. Gli output di questa sessione sono
confinati a `results/e16/diagnostics/tile_lifecycle_feature/` e allo script
read-only `scripts/audit_e16_tile_lifecycle_feature.py`.

Fonti primarie:

- engine: `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py`, SHA-256 `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e`;
- schema/README engine: `kaggriculture.json`, `README.md`, `AGENTS.md` nella stessa directory;
- policy frozen R1: `results/e16/manifests/E16_TREATMENT_BUILD_R1.py`, SHA-256 `7f331511a235e409833a726a324a4cda9881f3c8836a1ee260a2d6f36b78e1a8`;
- 28 summary e 28 ledger in `results/e16/stage_a_r1/`;
- configurazione: `configs/e16/E16_R1_FROZEN_CONFIG.json`;
- forensic precedente: `results/e16/diagnostics/e16_a_r1_crop_attainment/E16_A_R1_CROP_ATTAINMENT_FORENSIC_DIAGNOSIS.md`.

Tutte le 28 run risultano complete a 720 step, con engine
`kaggle-environments=1.32.7;python=3.12.13`, configuration hash
`f37496d1653cfc78672632c7fb779fc07ee93897a22341cf54f2242290e9f199` e
treatment hash R1 identico.

## 3. Stato engine osservabile

La farm pubblica contiene l'intera matrice `tiles`; ogni tile e `None`,
`"LOCKED"` o un dict. Una PLANT pubblica espone:

```text
kind, crop, planted_day, watered_today, consecutive_unwatered,
yield_units, max_lifespan_step, fertilized_until_day
```

Sono pubblici anche `day` e `hour`. Le definizioni crop sono regole statiche
dell'engine. La policy puo quindi calcolare lo stato senza risultati futuri.
Il seed episodio usato per gli spawn casuali viene invece rimosso dalla
configuration visibile e non puo entrare nella feature.

Regole R1 pertinenti:

| Crop | Ongoing | `first_yield_day` | Produzione / fine ciclo |
|---|---:|---:|---|
| WHEAT | no | 2 | finestra WATER fino a `max_yield_day=4`; lifespan da `(planted_day+5)*24` |
| STRAWBERRY | si | 10 | produzione ai giorni 10, 12, 14, 16; poi viene impostato `max_lifespan_step` |
| MELON | no | 10 | finestra WATER fino a `max_yield_day=12`; lifespan da `(planted_day+13)*24` |

Il clock diagnostico corretto e `day * turnsPerDay + hour`. R1 ha un difetto
separato: `state_rows.step` del seat 1 resta zero; day/hour rimangono validi.

## 4. Macchina a stati verificata

La rappresentazione minima strutturale e:

```text
OUT_OF_SCOPE
    | working-set assignment + owned tile
    v
EMPTY_ASSIGNED --PLANT--> GROWING <--valid ongoing HARVEST-- HARVEST_READY
       ^                    |                                  |
       |                    | age / scheduled production      | valid non-ongoing HARVEST
       |                    v                                  |
       |              HARVEST_READY ---------------------------+
       |                    |
       |                    | final ongoing HARVEST
       |                    v
       +-- planned DIG -- RETIREMENT_DUE

GROWING / HARVEST_READY / RETIREMENT_DUE
       | deterministic missed-WATER or lifespan loss
       v
LOST_WEED --DIG--> EMPTY_ASSIGNED

EMPTY_ASSIGNED --end-of-day RNG draw--> LOST_WEED
```

`GROWING` include crescita iniziale e regrowth ongoing: l'azione valida e la
stessa e non serve duplicare lo stato. `EMPTY_ASSIGNED` include sia suolo mai
piantato sia post-HARVEST non-ongoing; entrambi richiedono `PLANT`, quindi
`POST_HARVEST_REPLANT_DUE` sarebbe ridondante. La provenienza della transizione
puo essere loggata, ma non deve diventare una feature di dispatch.

`CARE_DUE` non appartiene alla categoria strutturale: una tile puo essere
simultaneamente `HARVEST_READY` e non irrigata. Il fabbisogno entra nel vincolo
`crop_decay_risk_window`.

La tabella completa con condizioni, costi e azioni e in
`E16_TILE_STATE_TRANSITIONS.csv`.

## 5. Come nasce WEED

Il motore ha esattamente tre famiglie rilevanti.

### 5.1 Mancato WATER: `DETERMINISTIC_PREVENTABLE`

Una nuova PLANT nasce con `consecutive_unwatered=1`. Al refresh di fine giornata:

```text
if watered_today: consecutive_unwatered = 0
else:             consecutive_unwatered += 1
if consecutive_unwatered >= 2: tile = WEED
```

Quindi:

- una crop piantata deve ricevere WATER nello stesso giorno, altrimenti e persa;
- dopo un giorno correttamente irrigato, una prima giornata senza WATER porta il
  contatore a 1 ma non uccide la crop;
- una seconda giornata consecutiva senza WATER la converte a `WEED`.

Il segnale preventivo e interamente online:

```text
water_loss_at_eod_if_unserved =
    kind == PLANT
    and not watered_today
    and consecutive_unwatered + 1 >= 2
```

L'azione preventiva minima e un WATER prima del refresh (1 worker action,
nessun costo cash). Per PLANT tardive occorre evitare il planting non
serviceable o avere una seconda unita co-locata nello stesso turno.

### 5.2 Lifespan: `DETERMINISTIC_PREVENTABLE`

Da `max_lifespan_step`, a ogni offset pari il motore decrementa `yield_units`.
Quando il valore diventa `<=0`, la PLANT diventa `WEED`. Le azioni worker sono
processate prima del decay: una raccolta valida puo ancora agire nella fase
corretta, ma pianificare prima del confine e piu robusto.

Per le crop non-ongoing, HARVEST valido raccoglie e rende la tile `None`. Per una
crop ongoing, HARVEST azzera il yield ma lascia la PLANT: dopo l'ultima
produzione lo stato e `RETIREMENT_DUE` e un `DIG` pianificato e l'unico modo
engine per liberare il suolo prima della conversione a WEED. Qui DIG e
clearance preventiva di fine ciclo, non recovery da una perdita gia avvenuta.

### 5.3 Spawn su EMPTY: `STOCHASTIC_PARTIALLY_PREVENTABLE`

A fine giornata, solo una tile `None` puo ricevere una WEED casuale con
`rng.random() < weedSpawnChance` (default 0.005). Lo spawn non sostituisce mai
direttamente una PLANT viva. Il draw e il seed non sono osservabili, quindi non
esiste un countdown tile-specifico corretto.

L'esposizione e riducibile mantenendo una posizione assegnata non vuota, per
esempio replantando tempestivamente; il singolo draw non e prevedibile. Dopo lo
spawn, `DIG` e la recovery engine (1 action), seguito da `PLANT` e costo seed.

## 6. Semantica HARVEST

La funzione concettuale verificata e:

```text
harvest_ready(tile, current_day) =
    tile.kind == PLANT
    and tile.yield_units > 0
    and current_day - tile.planted_day
        >= CROPS[tile.crop].first_yield_day
```

Tutti gli input sono disponibili online. `yield_units > 0` da solo e errato:
WHEAT e MELON non-ongoing nascono con un'unita, ma il motore rifiuta HARVEST
prima di `first_yield_day`. Questa e precisamente la condizione omessa dalla
policy R1, che genera `crop_harvest` appena vede `yield_units > 0`.

Effetti:

- HARVEST prematuro: silent no-op, nessun inventario, tile invariata;
- HARVEST valido non-ongoing: tutto il yield va all'inventario, tile `None`, poi
  serve `PLANT`;
- HARVEST valido ongoing: tutto il yield va all'inventario, `yield_units=0`, la
  PLANT resta e puo produrre agli intervalli statici successivi;
- dopo l'ultima produzione ongoing non c'e un nuovo ciclo implicito: serve
  clearance/replant per mantenere la superficie produttiva.

Non deve essere generato HARVEST se la funzione e falsa. Non emergono cooldown
di azione oltre alla disponibilita di `yield_units`; la ripetibilita ongoing e
governata dal calendario ancorato a `planted_day`, non dall'ultimo HARVEST.

## 7. Feature proposta

### 7.1 `tile_lifecycle_state`

```text
type: DERIVED_CATEGORICAL_FEATURE
values: OUT_OF_SCOPE | EMPTY_ASSIGNED | GROWING |
        HARVEST_READY | RETIREMENT_DUE | LOST_WEED
online: YES
future_leakage: NO
```

| Stato | Regola | Azioni valide principali | Azioni da non emettere | Prossima transizione |
|---|---|---|---|---|
| `OUT_OF_SCOPE` | non membro, locked o struttura non-crop | nessuna task crop | PLANT/WATER/HARVEST crop | assegnazione/unlock |
| `EMPTY_ASSIGNED` | membro e tile `None` | PLANT | WATER, HARVEST | GROWING o random WEED a EOD |
| `GROWING` | PLANT, HARVEST non valido, produzione futura possibile | WATER se due; attendere calendario | HARVEST | HARVEST_READY / LOST_WEED |
| `HARVEST_READY` | predicato readiness vero | HARVEST; WATER resta ortogonale per ongoing | HARVEST ripetuto dopo yield zero | EMPTY, GROWING o RETIREMENT_DUE |
| `RETIREMENT_DUE` | ongoing, ultima produzione gia raccolta, `max_lifespan_step>=0`, yield zero | DIG pianificato, poi PLANT | attesa passiva | EMPTY o LOST_WEED |
| `LOST_WEED` | `kind==WEED` | DIG residuale | PLANT/WATER/HARVEST | EMPTY_ASSIGNED |

Lo schema deterministico completo e in
`E16_TILE_LIFECYCLE_FEATURE_SCHEMA.json`.

### 7.2 `crop_decay_risk_window`

Proposta: `DERIVED_STRUCTURED_TIMING_CONSTRAINT`, non score opaco e non singola
feature scalare.

Componenti minime:

```text
care_due
water_loss_at_eod_if_unserved
action_phases_until_eod_refresh
lifespan_decay_started
next_lifespan_decay_phase
lifespan_loss_phase_if_no_action
empty_random_weed_eligible
```

`lifespan_loss_phase_if_no_action` e un deadline meccanico condizionale, non una
predizione della futura policy. `empty_random_weed_eligible` e un hazard binario:
non viene trasformato in `time_to_loss`.

Evidence status proposto:

```text
PROVISIONAL / ENGINE_RULE_NEEDED
    -> ENGINE_VERIFIED_WITH_R1_LONGITUDINAL_TELEMETRY_GAP
```

Non e una promozione a optimum, parametro o hyperparameter; resta una feature
derivata da validare in un successivo TRAINING preregistrato.

## 8. Azionabilita preventiva

| Condizione | Intervento prima della perdita | Minimo costo worker | Cash | Recovery se fallisce |
|---|---|---:|---:|---|
| WATER loss boundary | WATER entro EOD; evitare PLANT tardiva non serviceable | 1 | 0 | DIG + PLANT |
| HARVEST_READY prima del decay | HARVEST valido | 1 | 0 | DIG + PLANT se WEED |
| RETIREMENT_DUE ongoing | DIG pianificato, poi PLANT | 2 inclusa PLANT | seed | DIG + PLANT dopo WEED |
| EMPTY random eligible | replant tempestivo se economicamente previsto | 1 PLANT | seed | DIG + PLANT |
| LOST_WEED | nessuna prevenzione residua | - | - | DIG, poi PLANT |

La priorita metodologica `prevention > recovery` e supportata: le due vie da
PLANT viva sono deterministiche e hanno segnali pre-loss pubblici. DIG non
sostituisce WATER o HARVEST valido. Rimane pero necessario come safety recovery
per spawn casuali/violazioni e come clearance preventiva specifica delle crop
ongoing esaurite.

## 9. Copertura offline R1

L'estrattore legge soltanto le 28 run completate. Un intervallo e `exact` quando
la stessa posizione e osservata in due engine step consecutivi; e `gapped`
quando il ledger actor-local non osserva gli step intermedi.

### 9.1 Copertura generale

| Misura | Risultato |
|---|---:|
| episode | 28 |
| posizioni working-set assegnate, sommate per episodio | 516 |
| posizioni osservate almeno una volta | 512 / 516 = 99.22% |
| osservazioni uniche tile-step | 49,261 |
| intervalli osservati | 48,749 |
| intervalli consecutivi exact | 35,688 / 48,749 = 73.21% |
| intervalli gapped | 13,061 |
| intervalli con cambio di kind | 317 |
| cambi exact | 7 / 317 = 2.21% |
| cambi gapped | 310 / 317 = 97.79% |

Il 73.21% non e copertura di tutte le transizioni reali: e la quota degli
intervalli actor-local che non ha gap. Proprio i cambi di stato avvengono spesso
mentre nessun worker visita la tile, quindi la copertura temporale exact dei
cambi e solo 2.21%.

### 9.2 Entrate in WEED

| Evidenza sul primo stato WEED osservato | Conteggio | Classificazione |
|---|---:|---|
| precedente `PLANT`, intervallo exact | 7 | tutte lifespan `DETERMINISTIC_PREVENTABLE` |
| precedente `PLANT`, intervallo gapped | 307 | famiglia plant-loss deterministica; WATER vs lifespan non separabile |
| precedente `EMPTY`, intervallo gapped | 3 | random empty spawn `STOCHASTIC_PARTIALLY_PREVENTABLE` |
| nessuno stato precedente (left-censored) | 12 | `UNRESOLVED` |
| totale tile working-set viste WEED | 329 | tutte le 28 run positive |

La prior-state coverage e `317/329 = 96.35%`. Le 307 transizioni gapped da
PLANT appartengono necessariamente a una delle due vie deterministiche
dell'engine: qualsiasi azione treatment sulla posizione avrebbe prodotto uno
snapshot actor-local nell'intervallo. Non e tuttavia lecito attribuirle
specificamente a WATER o lifespan, ne misurare l'anticipo disponibile.

Il contatore R1 `crop_losses=583` non viene usato come denominatore causale:
deriva da differenze full-board, ma l'attribuzione delle rimozioni usa
`observation.step`, difettoso per seat 1. Viene conservato nel CSV come source
telemetry, non reinterpretato come 583 perdite causalmente classificate.

### 9.3 HARVEST e budget azioni

| Misura | Risultato |
|---|---:|
| tentativi crop-HARVEST prematuri | 5,804 |
| tentativi crop-HARVEST validi | 655 |
| altri fallimenti crop-HARVEST | 0 |
| quota prematura | 5,804 / 6,459 = 89.86% |
| DIG treatment | 0 |

Il predicato readiness avrebbe escluso tutti i 5,804 tentativi prematuri usando
solo informazione online. Sono 5,804 opportunita di azione logica potenzialmente
liberate (media 207.3 per episodio), ma non si dichiara che tutte sarebbero state
convertite in WATER/HARVEST/PLANT utile: posizione worker, travel, prenotazioni
simultanee e ordine dei task richiedono un controfattuale non presente in R1.

Sono presenti 6,258 snapshot actor-local con condizione meccanica
`water_loss_at_eod_if_unserved`, ma sono osservazioni duplicate nel tempo, non
6,258 perdite uniche. Dimostrano disponibilita del segnale, non l'effetto di un
nuovo dispatcher.

Artefatti di coverage:

- `E16_R1_TILE_LIFECYCLE_COVERAGE.csv`: metriche per episodio;
- `E16_R1_TILE_LIFECYCLE_COVERAGE_SUMMARY.json`: aggregato e qualificazioni;
- `E16_R1_EXACT_TILE_STATE_CHANGES.csv`: le 7 transizioni exact di kind.

## 10. Telemetry gap esatto

La computabilita online e piena, ma il replay R1 non conserva una history
tile-level completa. Per una validazione futura senza ambiguita servono, per
ogni working-set tile e fase:

1. snapshot pre-action e post-engine-refresh con clock canonico day/hour;
2. `kind`, `crop`, `planted_day`, `watered_today`,
   `consecutive_unwatered`, `yield_units`, `max_lifespan_step`;
3. transition reason engine: action, missed WATER, lifespan decay o random spawn;
4. task eligibility, deadline e priorita che hanno prodotto la scelta worker;
5. distinzione tra DIG di `RETIREMENT_DUE` e DIG recovery di `LOST_WEED`.

Questo e un `OBSERVABILITY_REQUIREMENT`, non un nuovo parametro di policy.
Consente coverage full-board e anticipo pre-loss esatto senza memorizzare il draw
RNG futuro.

## 11. Mapping ontologico

| Concetto esistente | Implicazione dell'audit |
|---|---|
| `crop_care_action_flow` | il flow deve contare task validi/effectful per stato, non richieste premature |
| `crop_harvest_action_flow` | `HARVEST_READY` fornisce il denominatore di opportunita valide e separa ongoing/non-ongoing |
| `crop_care_completion_rate` | puo usare obblighi tile-day espliciti; il denominatore va preregistrato e non deve includere task impossibili |
| `crop_decay_risk_window` | regola engine verificata; ridefinizione strutturata, con hazard RNG separato |
| `crop_surface_maintained` | va contato con una regola di maintenance dichiarata, distinguendo PLANT sana, retirement e WEED |
| `maintained_productive_surface` | riceve il componente crop corretto ma conserva obbligatoriamente il breakdown crop/pasture |

La proposta non modifica l'ontologia frozen. Raccomanda una revisione umana che
promuova solo l'evidence status della regola engine, non una relazione causale
di outcome e non una regione ottima.

## 12. Trattamento minimo raccomandato, non implementato

Per un successivo TRAINING preregistrato, mantenere invariati cella R1, crop
mix, target, WATER priority band, workforce, routing distance, land, market e
shutdown. Variare un solo modulo semantico di task eligibility/lifecycle:

1. generare HARVEST crop solo in `HARVEST_READY`;
2. ordinare i WATER gia eleggibili usando il deadline meccanico
   `water_loss_at_eod_if_unserved`, senza cambiare il livello numerico di WATER;
3. gestire `RETIREMENT_DUE` con clearance DIG pianificata;
4. mantenere `LOST_WEED -> DIG` come coda residuale sotto le azioni preventive.

Questo e il minimo trattamento completo: il solo maturity gate eliminerebbe i
5,804 no-op, ma lascerebbe non trattati il fine ciclo ongoing e lo spawn casuale
assorbente. Il confronto deve separare in telemetry prevenzione, retirement e
recovery, cosi l'effetto non viene attribuito genericamente a DIG.

Non viene proposta alcuna soglia appresa: tutti i confini provengono dal motore.

# SUPERVISOR DECISION INPUT

### Tile lifecycle feature

`SUPPORTED_WITH_TELEMETRY_GAP`

### Preventive control potential

`HIGH`

Motivo qualificato: 314/329 entrate WEED osservate hanno precedente PLANT e
quindi appartengono a vie deterministiche prevenibili; 5,804 azioni HARVEST
premature sono eliminabili semanticamente. L'effetto economico controfattuale
resta da testare.

### WEED preventability

- `DETERMINISTIC_PREVENTABLE`: missed-WATER e lifespan su PLANT; 314 casi R1 con precedente PLANT, di cui 7 exact lifespan e 307 senza sub-causa temporalmente separabile.
- `STOCHASTIC_PARTIALLY_PREVENTABLE`: spawn RNG su EMPTY; 3 casi R1 con precedente EMPTY. L'esposizione e riducibile, il draw non e prevedibile.
- `UNRESOLVED`: 12 tile R1 left-censored senza stato precedente.

### Recommended minimal treatment

Un solo modulo lifecycle che applica readiness HARVEST esatta, deadline WATER
engine-derived, retirement ongoing pianificato e DIG solo come recovery
residuale; nessun cambiamento a target, priority band, workforce, routing,
economia o crop mix. Non implementato in questa sessione.

### Recovery role

`RESIDUAL_SAFETY_RECOVERY`

DIG resta recovery per `LOST_WEED`; il suo uso separato su
`RETIREMENT_DUE` e clearance preventiva richiesta dalla semantica ongoing, non
la soluzione primaria a mancato WATER o HARVEST prematuro.

### Ontology implication

Promuovere `crop_decay_risk_window` da `PROVISIONAL / ENGINE_RULE_NEEDED` a
`ENGINE_VERIFIED_WITH_R1_LONGITUDINAL_TELEMETRY_GAP`, ridefinendolo come
vincolo strutturato multi-causa. Non promuoverlo a optimum/parameter e non
assegnare un countdown deterministico allo spawn RNG.

### Stage B

STAGE B: BLOCKED
C*: NONE
