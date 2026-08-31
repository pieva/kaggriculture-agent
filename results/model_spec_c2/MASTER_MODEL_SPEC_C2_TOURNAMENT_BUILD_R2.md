# MASTER PROMPT — MODEL_SPEC C2 Tournament Build

## Mandato comune per Antigravity, Codex e Copilot

Questo prompt deve essere eseguito **separatamente e senza modifiche** da:

```text
ANTIGRAVITY
CODEX
COPILOT
```

Ogni agente deve lavorare in modo **indipendente**.

L'obiettivo NON è convergere verso una soluzione comune prima del test.

L'obiettivo è produrre **tre ipotesi operative realmente concorrenti**, costruite sulla stessa Foundation C2 e sulle stesse evidenze, da confrontare successivamente nel:

```text
MODEL_SPEC TOURNAMENT C2
```

---

# 0. Identità del concorrente

Prima di qualsiasi attività determinare quale agente sta eseguendo il prompt:

```text
ANTIGRAVITY
CODEX
COPILOT
```

Impostare:

```text
AGENT_ID = ANTIGRAVITY | CODEX | COPILOT
```

Usare `AGENT_ID` nei nomi degli artefatti specifici.

NON leggere, confrontare o utilizzare MODEL_SPEC C2, implementazioni C2, note di lavoro o risultati prodotti dagli altri due concorrenti.

Se tali file esistono già nel repository perché un altro agente ha terminato prima:

```text
IGNORARLI
NON APRIRLI
NON USARLI COME EVIDENZA
```

L'indipendenza tra concorrenti è parte del protocollo sperimentale.

---

# 1. Gate upstream già chiuso

La verifica finale Codex ha stabilito:

```text
MODEL_SPEC_C2_UPSTREAM_READY: YES
```

Tutti i blocker Feature Model necessari all'avvio dei MODEL_SPEC sono chiusi.

La Foundation C2 resta formalmente:

```text
NOT FROZEN
```

ma è sufficientemente non ambigua per questo torneo.

NON riaprire la Foundation.

NON eseguire una nuova review generale di:

```text
Ontology
State Machine
Feature Model
```

Sono ammesse soltanto segnalazioni locali se durante l'implementazione emerge una contraddizione realmente bloccante.

---

# 2. Obiettivo del torneo

La domanda sperimentale centrale è:

> **Individua i meccanismi che hanno contribuito maggiormente alle prestazioni insufficienti delle policy precedenti e determina quali modifiche decisionali concrete, supportate dalle evidenze disponibili, possono migliorare il risultato.**

Ogni concorrente deve costruire una propria risposta operativa attraverso:

```text
DIAGNOSI
   ↓
INTERVENTO
   ↓
PREVISIONE VERIFICABILE
   ↓
MODEL_SPEC C2
   ↓
IMPLEMENTAZIONE ESEGUIBILE
   ↓
TORNEO COMUNE
```

Il MODEL_SPEC non è un documento descrittivo.

È una **ipotesi causale implementabile**.

---

# 3. Evidenza di partenza comune

Assumere come quadro sperimentale comune:

```text
E15: CLOSED
E16 Stage A-R1: COMPLETED 28/28
E16 Stage B: BLOCKED
C*: NONE
MODEL_VALIDITY: STRONGLY SUPPORTED
dominant bottleneck: POLICY_REALIZATION
```

R1 ha eliminato il falso problema di synthetic drought.

Watering execution HIGH:

```text
0.8898 – 0.9416
```

Watering continuity:

```text
~0.96
```

Median money:

```text
A01 LOW/10   = 19,694
A02 HIGH/10  = 21,230.5
A03 LOW/25   = 11,903.5
A04 HIGH/25  = 19,987
A05 MID/17   = 26,619.5
A06 MID/25   = 21,570.5
A07 HIGH/17  = 27,076
```

Capacity gate:

```text
completion >= .80
watering execution >= .60
continuity >= .75
crop target attainment >= .80
```

Nessuna configurazione raggiunge il gate.

Corrected crop-target attainment:

```text
A02 HIGH/10 = .5000
A07 HIGH/17 = .4706
A04 HIGH/25 = .3600
```

A07 HIGH/17 è una regione diagnostica interessante.

NON è un optimum.

NON ottimizzare per imitare A07.

---

# 4. Evidenza forense obbligatoria

La diagnosi E16 A-R1 ha identificato:

```text
5,804 / 5,804 failed crop HARVEST attempts
prima della maturity
```

La policy frozen usava:

```text
yield_units > 0
```

come equivalente di harvest-ready.

L'engine richiede invece anche:

```text
crop age >= first_yield_day
```

Quindi:

```text
harvest_ready =
    tile.kind == PLANT
    AND yield_units > 0
    AND age >= first_yield_day
```

Il failure rate HARVEST prematuro osservato è circa:

```text
89.86%
```

dei crop-HARVEST attempts analizzati.

Inoltre:

```text
nominal working-set tiles possono diventare WEED
frozen dispatcher aveva zero DIG
```

Una tile persa poteva quindi diventare un sink permanente:

```text
WEED
→ no DIG
→ no PLANT
→ target gap persistente
```

La catena causale supportata è:

```text
routing + workforce intermittency
        +
premature HARVEST dispatch
        ↓
service/action waste
        ↓
crop loss
        ↓
WEED
        ↓
no recovery / no replant
        ↓
irreversible target gap
```

Ma la priorità metodologica è:

```text
PREVENTION > RECOVERY
```

DIG non deve diventare la risposta primaria a errori evitabili.

---

# 5. Tile lifecycle evidence

La Foundation C2 distingue:

```text
OUT_OF_SCOPE
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

Principali transizioni:

```text
EMPTY_ASSIGNED
    --PLANT-->
GROWING

GROWING
    --maturity / scheduled production-->
HARVEST_READY

HARVEST_READY
    --valid non-ongoing HARVEST-->
EMPTY_ASSIGNED

HARVEST_READY
    --valid ongoing intermediate HARVEST-->
GROWING

HARVEST_READY
    --valid final ongoing HARVEST-->
RETIREMENT_DUE

RETIREMENT_DUE
    --planned DIG-->
EMPTY_ASSIGNED

GROWING / HARVEST_READY / RETIREMENT_DUE
    --deterministic missed-WATER or lifespan loss-->
LOST_WEED

LOST_WEED
    --DIG-->
EMPTY_ASSIGNED
```

Per EMPTY soil esiste inoltre random WEED spawn.

Non esiste un countdown deterministico valido per tale RNG.

---

# 6. Prevention semantics

Tre famiglie WEED:

```text
1. missed WATER
   deterministic / preventable

2. post-lifespan loss
   deterministic / preventable

3. random EMPTY spawn
   stochastic / partially preventable
```

WATER:

```text
new PLANT starts with consecutive_unwatered = 1
```

Quindi una nuova crop deve essere servibile con WATER nello stesso giorno.

Segnale meccanico:

```text
kind == PLANT
AND not watered_today
AND consecutive_unwatered + 1 >= 2
```

=> perdita a EOD se non servita.

Lifespan:

```text
max_lifespan_step
```

è un deadline/risk signal.

NON equivale automaticamente a:

```text
RETIREMENT_DUE
```

Per ongoing crops, dopo l'ultima produzione e il final HARVEST:

```text
yield_units = 0
no future scheduled production
=> RETIREMENT_DUE
```

Qui DIG può essere **preventive clearance** per liberare la tile prima della degradazione.

---

# 7. R1 coverage rilevante

Disponibile come training evidence:

```text
28 episodes
516 assigned working-set positions
512 observed
49,261 unique tile-step observations
48,749 intervals
35,688 exact consecutive intervals
13,061 gapped intervals
317 kind changes
329 observed WEED entries
```

WEED entries:

```text
314 / 329 prior PLANT deterministic/preventable family
3 stochastic EMPTY
12 unresolved
```

HARVEST:

```text
5,804 premature crop-HARVEST attempts
655 valid
0 other failures
```

DIG:

```text
0 treatment actions
```

A07 representative:

```text
target = 17
reaches 15/17 by step 18
below 50% by step 70
45 crop harvest executed
357 premature harvest failures
22 matched replants
median replant latency = 22.5
11 nominal positions observed WEED
0 DIG
final active crop = 1
final seed inventory = 16
```

Seeds are NOT supported as primary bottleneck.

Market pacing is secondary.

WATER is NOT the primary R1 bottleneck after R1 repair.

---

# 8. Foundation C2 obbligatoria

Leggere integralmente almeno:

```text
docs/model/ontology/ONTOLOGY_C2.md
docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md
docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md
```

Leggere le evidenze e review necessarie a ricostruire correttamente il quadro, incluse almeno:

```text
docs/model/reviews/reconciliation/CODEX_FOUNDATION_RECONCILIATION_R1.md
docs/model/reviews/codex/CODEX_FEATURE_MODEL_C2_REVIEW_R1.md
docs/model/reviews/codex/CODEX_FEATURE_MODEL_C2_BLOCKER_VERIFICATION_R2_1.md
docs/model/reviews/codex/CODEX_FEATURE_MODEL_C2_BLOCKER_REVERIFICATION_R2_2.md
docs/model/reviews/antigravity/ANTIGRAVITY_FOUNDATION_REVIEW_R1.md
```

Leggere inoltre i report/evidence E16 A-R1 pertinenti presenti nel repository.

NON leggere i nuovi MODEL_SPEC C2 degli altri concorrenti.

---

# 9. MODEL_SPEC C2 — mandato

Produrre:

```text
docs/model/model_specs/<agent>/MODEL_SPEC_<AGENT>_C2.md
```

dove `<agent>` segue la directory esistente:

```text
antigravity
codex
copilot
```

e `<AGENT>` è l'identificatore coerente con la convenzione repository.

Il documento deve essere in italiano salvo:

```text
technical identifiers
engine fields
action names
metric names
file names
commands
canonical values
```

---

# 10. MODEL_SPEC — struttura minima obbligatoria

Il MODEL_SPEC deve contenere almeno:

```text
1. Scopo e ipotesi operativa
2. Evidenza utilizzata
3. Diagnosi causale prioritaria
4. Meccanismi NON prioritari
5. Feature C2 consumate
6. Regole decisionali
7. Priorità / arbitration
8. Tile lifecycle policy
9. WATER policy
10. HARVEST policy
11. PLANT / replant policy
12. DIG preventive/recovery policy
13. Workforce / movement policy
14. Inventory / market policy
15. Livestock policy, se utilizzata
16. Failure containment
17. Expected mechanism changes
18. Previsioni verificabili
19. Metriche di verifica
20. Assunzioni e limiti
```

Non è obbligatorio intervenire materialmente su tutti i sottosistemi.

Un sottosistema può essere dichiarato:

```text
UNCHANGED
DEFERRED
NOT_CAUSALLY_PRIORITIZED
```

se motivato.

---

# 11. Principio di progettazione

Non modificare tutto.

Identificare i pochi meccanismi con maggiore probabilità di produrre miglioramento materiale.

Per ogni intervento principale costruire una catena esplicita:

```text
EVIDENZA
    ↓
MECCANISMO
    ↓
FEATURE C2
    ↓
MODIFICA DECISIONALE
    ↓
EFFETTO ATTESO
    ↓
METRICA DI VERIFICA
```

Esempio:

```text
5,804 premature HARVEST
    ↓
action waste
    ↓
harvest_ready
    ↓
HARVEST only if harvest_ready == true
    ↓
lower failed/no-op HARVEST
higher productive action availability
    ↓
premature_harvest_count
productive_action_share
crop_target_attainment
final_money
```

L'esempio NON prescrive l'intero MODEL_SPEC.

---

# 12. Libertà competitiva

Ogni agente può proporre una strategia differente.

Sono ammesse differenze su:

```text
working-set maintenance
crop mix
target productive surface
expansion pacing
worker allocation
routing
serviceability logic
replant urgency
retirement handling
inventory policy
market timing
livestock usage
capacity realization
```

purché supportate dalla Foundation/evidence e implementabili.

NON introdurre learned thresholds senza evidenza.

Se è necessario un parametro operativo non determinato dalla Foundation:

```text
dichiararlo esplicitamente
motivarlo
renderlo configurabile
non presentarlo come optimum
```

---

# 13. Consumer mapping minimo

È consentito creare **solo il mapping minimo necessario** tra MODEL_SPEC e runtime.

Non creare una nuova tassonomia generale.

Per ogni feature C2 realmente consumata dal MODEL_SPEC documentare:

```text
feature_id
runtime source
calculation point
decision phase
consumer
fallback behavior
```

Questo mapping può stare nel MODEL_SPEC oppure in un piccolo artefatto specifico del concorrente.

Non modificare il Feature Model per adattarlo alla policy.

---

# 14. Implementazione eseguibile

Dopo aver congelato logicamente il proprio MODEL_SPEC, implementare una policy eseguibile specifica del concorrente.

La policy deve essere identificabile univocamente come candidato C2 del relativo agente.

Preferire l'architettura esistente del repository.

NON duplicare inutilmente l'intero agent stack.

Separare:

```text
shared infrastructure
candidate-specific decision logic
candidate-specific configuration
```

La policy deve poter essere invocata dal futuro runner del torneo senza modifica manuale del codice.

---

# 15. Nessuna contaminazione tra concorrenti

NON:

```text
leggere MODEL_SPEC C2 degli altri agenti
leggere candidate implementation C2 degli altri agenti
copiare le loro regole
confrontare le loro scelte
adattare la propria soluzione per battere un candidato già presente
```

Il confronto avverrà solo nel torneo.

È consentito usare shared infrastructure preesistente.

---

# 16. Invarianti minime di correttezza

La policy non deve reintrodurre errori già diagnosticati.

## HARVEST

Non usare:

```text
yield_units > 0
```

come unico readiness criterion.

Usare la semantica C2:

```text
harvest_ready
```

## WATER

Non degradare il comportamento R1 corretto.

Le deadline devono usare clock engine autorevole.

## Lifecycle

Distinguere almeno:

```text
EMPTY_ASSIGNED
GROWING
HARVEST_READY
RETIREMENT_DUE
LOST_WEED
```

quando rilevanti alla decisione.

## DIG

Distinguere:

```text
preventive clearance
recovery
```

Prevention resta preferibile a recovery.

## Ongoing crops

Dopo intermediate valid HARVEST:

```text
yield_units = 0
future production exists
=> GROWING
```

Dopo final valid HARVEST:

```text
yield_units = 0
no future production
=> RETIREMENT_DUE
```

---

# 17. Failure containment

La policy deve avere comportamento definito per:

```text
missing/invalid diagnostic data
temporarily unavailable feature
insufficient workforce
insufficient cash
insufficient seed/inventory
unserviceable tile
LOST_WEED
movement contention
multi-occupancy
action failure
```

Non usare informazione futura non disponibile al decision time.

---

# 18. Previsioni verificabili

Prima di eseguire qualsiasi test del candidato, scrivere nel MODEL_SPEC previsioni verificabili.

Almeno:

```text
P1. premature HARVEST attempts devono diminuire materialmente
P2. working-set crop persistence deve migliorare
P3. lost/WEED tile persistence deve diminuire
P4. replant latency deve diminuire dove la policy la prioritizza
P5. productive_action_share non deve peggiorare strutturalmente
P6. WATER execution/continuity non deve regredire materialmente
P7. crop target attainment deve migliorare rispetto al failure pattern E16
P8. final money deve essere misurato, non assunto
```

Ogni concorrente può aggiungere proprie previsioni specifiche.

NON prevedere arbitrariamente un miglioramento economico 10x.

---

# 19. Metriche comuni del futuro torneo

Predisporre il candidato affinché il torneo possa misurare, quando disponibili/computabili:

```text
final_money
completion
crop_target_attainment
active_crop_surface
maintained_productive_surface
watering_execution
watering_continuity
premature_harvest_count
failed_action_count
no_op_action_count
WEED/lost_tile_count
lost_tile_persistence
replant_latency
movement_share
productive_action_share
workforce_utilization
inventory state
market activity
livestock contribution, se rilevante
```

Non inventare una metrica se il repository non consente di calcolarla correttamente.

In tal caso indicare:

```text
NOT_CURRENTLY_COMPUTABLE
```

---

# 20. Test consentiti in questa fase

Questa fase serve a costruire e verificare gli eseguibili.

È consentito:

```text
unit test
integration test
deterministic smoke test
short execution sanity check
existing validation harness
```

NON eseguire il torneo comparativo a tre.

NON utilizzare i risultati di un altro concorrente.

NON selezionare un vincitore.

NON eseguire submission Kaggle.

---

# 21. Verifica dell'implementazione

Aggiungere test mirati almeno per i meccanismi introdotti.

In particolare, se pertinenti alla policy:

```text
premature HARVEST rejected
mature HARVEST accepted
intermediate ongoing HARVEST lifecycle
final ongoing HARVEST retirement
WATER deadline behavior
LOST_WEED recovery
RETIREMENT_DUE preventive DIG
EMPTY_ASSIGNED replant
worker/action arbitration
```

Non costruire test che codificano come optimum una configurazione E16.

---

# 22. Artefatti concorrente

Alla fine devono esistere almeno:

```text
MODEL_SPEC C2 del concorrente
candidate executable/configuration
test specifici necessari
eventuale minimal consumer mapping
breve build/verification report
```

Usare directory coerenti con la struttura repository esistente.

Non creare una nuova proliferazione di documenti se le informazioni possono stare nel MODEL_SPEC o nel report di build.

---

# 23. Build/verification report

Creare un solo report sintetico specifico del concorrente, ad esempio:

```text
results/model_spec_c2/<agent>/BUILD_VERIFICATION.md
```

oppure percorso equivalente coerente con il repository.

Deve riportare:

```text
AGENT_ID
MODEL_SPEC path
candidate executable path
configuration path, se presente
tests added/changed
pytest result
git diff --check result
smoke/integration result
known limitations
TOURNAMENT_READY: YES | NO
```

---

# 24. Responsabilità POST-torneo — contratto obbligatorio

Nel MODEL_SPEC inserire una sezione:

```text
POST-TOURNAMENT REVIEW CONTRACT
```

Dopo il torneo locale a tre, lo stesso agente dovrà ricevere i risultati di:

```text
ANTIGRAVITY
CODEX
COPILOT
```

e analizzare **tutti e tre**, non soltanto il proprio candidato.

La review post-torneo dovrà ripetere la stessa domanda causale:

> Quali meccanismi hanno performato peggio, perché, quali decisioni del MODEL_SPEC li hanno causati e quali modifiche concrete possono migliorarli?

Struttura:

```text
RISULTATO
    ↓
MECCANISMO OSSERVATO
    ↓
DECISIONE MODEL_SPEC
    ↓
SPIEGAZIONE CAUSALE
    ↓
MODIFICA PROPOSTA
    ↓
PREVISIONE VERIFICABILE
```

Non razionalizzare vittoria o sconfitta.

Il maggior `final_money` non implica automaticamente il miglior MODEL_SPEC.

Una policy può correggere un meccanismo senza averlo ancora convertito pienamente in denaro.

---

# 25. Preparazione al torneo

Il candidato deve essere lasciato in stato:

```text
TOURNAMENT_READY
```

ma il torneo NON va eseguito in questa sessione.

Il futuro torneo userà:

```text
stesso protocollo
stessi opponent/seed/configuration rules
stessa telemetry
stesse metriche
stesso budget sperimentale
```

per tutti e tre.

Non creare vantaggi specifici per il proprio candidato nel runner comune.

Se serve una piccola estensione shared per rendere il candidato invocabile, deve essere neutrale rispetto ai tre concorrenti.

---

# 26. Chiusura del mandato del singolo concorrente

Una volta ottenuto:

```text
TOURNAMENT_READY: YES
```

il lavoro del singolo concorrente è terminato.

Ogni agente deve fermarsi dopo aver prodotto e verificato:

```text
MODEL_SPEC C2 del proprio concorrente
candidate executable/configuration
test specifici necessari
eventuale minimal consumer mapping
BUILD_VERIFICATION
```

NON deve occuparsi della chiusura generale della fase.

---

# 27. Attività esplicitamente vietate al singolo concorrente

NON modificare per attività di chiusura/session handoff:

```text
PROJECT_STATE.md
EXPERIMENT_LOG.md
NEW_SESSION.md
README.md
```

salvo che uno di questi file sia strettamente necessario all'eseguibilità tecnica del candidato; in tal caso NON usarlo per registrare lo stato complessivo del progetto.

NON eseguire:

```text
pulizia generale di docs/prompts/
rimozione dei micro-prompt consumati
riorganizzazione documentale generale
freeze della Foundation
commit
push
torneo a tre
review post-torneo
submission Kaggle
```

Queste attività saranno affidate separatamente ad Antigravity dopo che tutti e tre i concorrenti avranno completato il proprio lavoro.

---

# 28. Nessun coordinamento finale tra concorrenti

Il singolo agente NON deve:

```text
verificare se gli altri due candidati sono pronti
aggiornare lo stato globale 1/3, 2/3 o 3/3
preparare NEW_SESSION
decidere il commit finale
pulire artefatti prodotti dagli altri
```

Deve limitarsi al proprio candidato.

L'isolamento competitivo resta valido fino alla chiusura di tutti e tre i build.

---

# 29. Git discipline

Non usare:

```text
git add .
```

Non fare staging.

Non fare commit.

Non fare push.

È consentito usare:

```powershell
git status --short
git diff --check
git diff -- <file propri>
```

solo per verificare che le proprie modifiche siano corrette e per identificare chiaramente gli artefatti prodotti.

Non revertire modifiche preesistenti o appartenenti ad altri agenti.

---

# 30. Verifiche finali concorrente

Eseguire almeno:

```powershell
git diff --check
.\.venv\Scripts\pytest.exe
git status --short
```

Eseguire inoltre gli smoke/integration test specifici del candidato.

Se esiste un validator specifico, usarlo.

Non trasformare errori `ruff` repository-wide preesistenti in un refactoring fuori scope.

---

# 31. Condizioni TOURNAMENT_READY

Dichiarare:

```text
TOURNAMENT_READY: YES
```

soltanto se:

```text
MODEL_SPEC C2 esiste
diagnosi causale esplicita
interventi concreti
previsioni scritte prima dei test
consumer mapping sufficiente
candidate executable invocabile
nessun premature-HARVEST semantics regression
lifecycle semantics rispettata
test specifici passano
repository tests passano
git diff --check passa
nessun blocker noto impedisce il torneo
```

Altrimenti:

```text
TOURNAMENT_READY: NO
```

e descrivere il blocker.

---

# 32. Divieto di ottimizzazione ex post

Non modificare il MODEL_SPEC dopo aver osservato risultati di smoke/integration che costituiscano già una misura economica comparabile al futuro torneo, salvo bug di implementazione evidente.

Se viene corretto un bug:

```text
documentare bug
documentare fix
non reinterpretarlo come tuning
```

Il torneo deve confrontare ipotesi formulate prima della misurazione comparativa.

---

# 33. Output finale dell'agente

Riportare in forma compatta:

```text
AGENT_ID: <...>

PRE-TOURNAMENT DIAGNOSIS:
- primary mechanism:
- secondary mechanism:
- intentionally deprioritized mechanisms:

MODEL_SPEC_C2:
<path>

CANDIDATE_EXECUTABLE:
<path>

CONSUMER_MAPPING:
<path or EMBEDDED>

BUILD_VERIFICATION:
<path>

KEY DECISION CHANGES:
- ...
- ...
- ...

PRE-REGISTERED PREDICTIONS:
- ...
- ...
- ...

TESTS:
git diff --check: PASS | FAIL
pytest: PASS | FAIL
candidate smoke/integration: PASS | FAIL

TOURNAMENT_READY: YES | NO

FILES_CREATED:
- ...

FILES_MODIFIED:
- ...

GLOBAL_STATE_UPDATE: NOT PERFORMED
NEW_SESSION: NOT MODIFIED
MICRO_PROMPT_CLEANUP: NOT PERFORMED
COMMIT: NOT PERFORMED
PUSH: NOT PERFORMED
```

Chiudere esattamente con:

```text
MODEL_SPEC C2 BUILD: COMPLETED | BLOCKED
AGENT_ID: <...>
TOURNAMENT_READY: YES | NO
THREE_WAY_TOURNAMENT: NOT RUN
POST_TOURNAMENT_REVIEW: PENDING
KAGGLE_VALIDATION: NOT RUN
REPOSITORY_CLOSURE: DEFERRED_TO_ANTIGRAVITY
```

---

# 34. STOP

Dopo aver completato e verificato il proprio candidato:

```text
STOP
```

Non attendere gli altri concorrenti.

Non leggere i loro artefatti.

Non eseguire attività di chiusura generale.

Quando Antigravity, Codex e Copilot avranno tutti completato i rispettivi candidati, verrà impartito **un mandato separato ad Antigravity** per:

```text
verifica integrità 3/3
pulizia controllata dei micro-prompt
correzioni locali Foundation eventualmente ancora pendenti
aggiornamento PROJECT_STATE / EXPERIMENT_LOG / README
preparazione NEW_SESSION per MODEL_SPEC TOURNAMENT C2
test finali repository
staging selettivo
commit unico
eventuale push
```

Solo dopo quella chiusura inizierà la nuova chat/esperimento:

```text
MODEL_SPEC TOURNAMENT C2
```
