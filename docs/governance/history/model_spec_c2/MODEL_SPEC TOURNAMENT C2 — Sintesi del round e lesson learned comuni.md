# MODEL_SPEC TOURNAMENT C2 — Sintesi del round e lesson learned comuni

## 1. Scopo del documento

Questo documento consolida le evidenze emerse dal `MODEL_SPEC TOURNAMENT C2` e dalle successive failure review di Antigravity C2 e Copilot C2.

È destinato congiuntamente a:

- Antigravity;
- Codex;
- Copilot.

Lo scopo non è assegnare responsabilità né avviare remediation specifiche.

Lo scopo è rendere tutti gli agenti consapevoli dei problemi emersi nel round C2 e trasformarli in **lesson learned comuni per i successivi cicli MODEL_SPEC → BUILD → VERIFY → TOURNAMENT**.

Le evidenze specifiche delle singole review rimangono valide e separate.

---

# 2. Esito del tournament

Il tournament C2 è stato eseguito su tre candidati:

- Antigravity C2;
- Codex C2;
- Copilot C2.

Il protocollo ha utilizzato tre confronti pairwise con seed condivisi, senza duplicazione P0/P1.

Il precedente assessment aveva infatti trovato trascurabile l'effetto sistematico della posizione dell'ambiente.

## Risultato economico osservato

### Codex C2

```text
Mean final_money: $16,846.50
Median: $16,729.50
Min: $14,753
Max: $19,526
Record: 6W - 0L - 0T
Mean active surface: 9.17 tiles
```

Codex è stato l'unico candidato a realizzare un ciclo agricolo produttivo sostanziale.

Il risultato resta tuttavia inferiore alle migliori baseline storiche del progetto e la superficie produttiva osservata rimane inferiore al target nominale.

### Antigravity C2

```text
Mean final_money: $3,000
Active surface: 0
Policy realization: ~0%
```

Antigravity non ha realmente eseguito la policy prevista.

Un errore runtime nell'accesso a `observation["private"]` ha attivato il fail-closed, producendo `PASS` per l'intero episodio.

### Copilot C2

```text
Mean final_money: $3,000
Active surface: 0
PLANT: 0
MOVE: 0
Market orders: 0
```

Copilot ha completato gli episodi ma non ha realizzato un ciclo agricolo produttivo.

Sono state emesse numerose azioni locali, ma senza corrispondenti effetti produttivi sulla propria farm.

---

# 3. Interpretazione corretta del risultato

Il tournament è stato completato dal punto di vista esecutivo, ma **non costituisce un confronto prestazionale valido fra tre MODEL_SPEC pienamente realizzati**.

In pratica il tournament ha confrontato:

```text
CODEX
policy funzionante ma sottodimensionata

ANTIGRAVITY
policy non raggiunta a causa di failure runtime

COPILOT
policy locale incompleta e non in grado di inizializzare autonomamente
il ciclo produttivo
```

Di conseguenza:

> Il risultato economico di Codex non deve essere interpretato come prova definitiva della superiorità del relativo MODEL_SPEC rispetto agli altri due.

Antigravity e Copilot non hanno fornito una realizzazione sufficientemente valida delle rispettive policy per consentire tale inferenza.

---

# 4. Failure Antigravity C2

La failure review Antigravity ha identificato come causa immediata:

```text
observation["private"]
```

trattato come struttura multi-player indicizzata:

```text
privates[player_index]
```

mentre il runtime Kaggriculture fornisce al singolo agente il proprio `private` come `dict/Struct`.

Questo genera:

```text
KeyError: 0
```

Il fail-closed dell'agent wrapper intercetta quindi l'eccezione e restituisce:

```text
PASS
```

senza provocare crash o disqualification.

## Problema di processo

I test Antigravity utilizzavano mock con:

```text
"private": [{...}]
```

riproducendo l'assunzione errata dell'implementazione anziché il contratto del runtime reale.

Di conseguenza:

```text
unit tests PASS
```

non implicava:

```text
runtime integration PASS
```

La review ha inoltre individuato ulteriori failure latenti che richiederanno verifica durante la remediation, fra cui:

- gestione dinamica di `player_index`;
- parametri biologici non completamente allineati all'engine;
- incompletezza di alcune operazioni relative alla zootecnia.

---

# 5. Failure Copilot C2

La failure Copilot è diversa e più strutturale.

La review ha identificato tre blocker indipendenti.

## 5.1 Player-state binding

L'entrypoint usa:

```text
player_index=0
```

anche quando:

```text
observation.player == 1
```

Nelle partite del tournament Copilot giocava P1.

La policy leggeva quindi lo stato di `farms[0]`, mentre le azioni venivano applicate alla propria farm `farms[1]`.

Questo spiega la presenza di molte azioni apparentemente operative senza effetti sulla farm Copilot.

## 5.2 Bootstrap economico assente

La configurazione iniziale presenta zero seed.

Copilot restituisce permanentemente:

```text
market: []
```

e non possiede un percorso operativo `BUY_SEED`.

Pertanto:

```text
zero seeds
    ↓
no BUY_SEED
    ↓
PLANT unreachable
    ↓
no crop
    ↓
no harvest
    ↓
no revenue
```

Il ciclo produttivo è quindi impossibile da inizializzare anche indipendentemente dal problema `player_index`.

## 5.3 Movement/routing assente

La policy non contiene un percorso operativo per:

```text
NORTH
SOUTH
EAST
WEST
```

né target spaziali o routing verso tile produttive.

Il farmer rimane quindi allo spawn.

---

# 6. Convergenza delle due failure review

Antigravity e Copilot hanno fallito per ragioni tecniche differenti.

Tuttavia le review convergono su una stessa debolezza metodologica:

> `TOURNAMENT_READY` certificava principalmente conformità locale, invocabilità, unit test e action dispatch, ma non certificava una minima realizzazione end-to-end della policy nell'ambiente Kaggriculture reale.

Questa è la principale lesson learned del round C2.

---

# 7. Action dispatch non equivale a policy realization

Il round C2 dimostra che verificare:

```text
agent emits DIG
agent emits PLANT
agent emits WATER
agent emits HARVEST
```

non è sufficiente.

Occorre verificare:

```text
DIG
→ tile state realmente modificato

PLANT
→ seed realmente consumato
→ crop realmente creato

WATER
→ crop realmente irrigato

HARVEST
→ crop realmente raccolto
→ inventory realmente modificato

SELL
→ prodotto realmente venduto
→ cash realmente modificato
```

Il principio comune futuro deve essere:

> I gate di verifica devono validare gli effetti osservabili delle azioni sullo stato dell'ambiente, non soltanto l'action dispatch.

---

# 8. Unit test e runtime integration sono livelli distinti

Un secondo insegnamento generale è:

```text
UNIT TEST PASS
≠
REAL ENVIRONMENT PASS
```

Mock e fixture possono verificare correttamente la logica locale ma possono anche incorporare le stesse assunzioni errate dell'implementazione.

Per ogni candidato futuro è quindi necessario mantenere distinti almeno:

```text
UNIT TEST
        ↓
REAL-ENGINE SMOKE TEST
        ↓
POLICY REALIZATION TEST
        ↓
TOURNAMENT READINESS
```

---

# 9. P0/P1: distinzione importante

Il precedente assessment del tournament ha indicato che la posizione P0/P1 dell'ambiente non produce un effetto sistematico sufficientemente materiale da giustificare automaticamente la duplicazione speculare di tutti i match.

Questa conclusione resta valida.

Le failure C2 hanno però evidenziato un problema differente:

> Un candidato deve utilizzare correttamente `observation.player` e accedere sempre alla propria farm/private state.

Quindi:

```text
ENVIRONMENT POSITION EFFECT
```

e:

```text
CANDIDATE PLAYER-INDEX CORRECTNESS
```

sono due problemi distinti.

Il primo può essere trascurabile.

Il secondo deve essere obbligatoriamente verificato.

---

# 10. Nuovo principio per TOURNAMENT_READY

A seguito del round C2, una futura dichiarazione:

```text
TOURNAMENT_READY: YES
```

non dovrebbe essere basata esclusivamente su:

```text
code exists
+
candidate imports
+
unit tests pass
+
git diff --check passes
+
agent returns valid action structure
```

Deve includere evidenza runtime.

La pipeline raccomandata diventa:

```text
MODEL_SPEC
    ↓
BUILD
    ↓
UNIT TEST
    ↓
REAL-ENGINE SMOKE
    ↓
POLICY REALIZATION
    ↓
TOURNAMENT_READY
    ↓
TOURNAMENT
```

---

# 11. Gate comuni emersi dal C2

I dettagli definitivi dovranno essere formalizzati separatamente.

Le review C2 indicano tuttavia almeno quattro classi di gate.

## BUILD GATE

Verificare:

- contratto delle observation;
- `observation.player`;
- accesso alla propria farm;
- accesso al proprio private state;
- raggiungibilità delle principali branch della policy;
- allineamento delle costanti critiche con l'engine.

## REAL-ENGINE SMOKE GATE

Eseguire il candidato nell'ambiente Kaggriculture reale.

Verificare almeno:

- inizializzazione corretta;
- nessuna eccezione nascosta;
- nessun silent fail-closed loop;
- comportamento corretto sia come P0 sia come P1;
- presenza di state transition reali.

## POLICY REALIZATION GATE

Verificare gli effetti minimi richiesti dal MODEL_SPEC.

Quando pertinenti alla policy:

```text
resource acquisition
movement / tile access
successful DIG
successful PLANT
active productive surface > 0
successful WATER
crop maturation
successful HARVEST
inventory transition
market transaction
revenue transition
```

Non tutte le future policy devono necessariamente utilizzare ogni meccanismo, ma ciò che il MODEL_SPEC dichiara essenziale deve essere osservato nel runtime.

## TOURNAMENT READINESS GATE

`TOURNAMENT_READY: YES` deve essere consentito soltanto dopo il superamento documentato dei gate precedenti.

---

# 12. Fail-safe e fail-closed

Il fail-safe rimane utile in produzione per evitare crash o disqualification.

Il C2 mostra però che durante BUILD e VERIFY può occultare failure strutturali.

Principio futuro:

> Un fail-safe attivato durante un test deve essere osservabile e non deve poter contribuire a un falso `TOURNAMENT_READY`.

Devono quindi essere considerate almeno:

- exception telemetry;
- fallback counters;
- fail-closed activation counters;
- rejection del candidate quando il fallback sostituisce sistematicamente la policy.

---

# 13. Telemetria futura

La telemetria del tournament ha consentito di individuare parte dei problemi, ma il C2 dimostra che i soli conteggi delle azioni sono insufficienti.

Dovrà essere possibile distinguere almeno:

```text
ACTION DISPATCHED
ACTION ACCEPTED
ACTION NO-OP
ACTION FAILED
STATE TRANSITION OBSERVED
```

Quando economicamente rilevante dovranno inoltre essere tracciati:

```text
inventory delta
seed delta
cash delta
productive surface delta
tile lifecycle transition
```

Questo permetterà di distinguere una policy realmente operativa da una policy che produce soltanto comandi formalmente validi.

---

# 14. Stato di Codex C2

Codex C2 non presenta i failure bloccanti osservati negli altri due candidati.

Ha realizzato:

- superficie produttiva;
- planting;
- watering;
- harvesting;
- market activity;
- risultati economici positivi.

Tuttavia il risultato medio di circa `$16.8k` e una superficie attiva media di circa `9.17 tiles` indicano che il candidato non deve essere considerato automaticamente soddisfacente.

Il round C2 non dimostra che:

```text
CODEX MODEL_SPEC = soluzione ottimale
```

Dimostra soltanto che:

```text
CODEX C2 = unico candidato del round che ha realizzato
           una policy agricola sostanzialmente funzionante
```

Anche Codex deve quindi incorporare le lesson learned C2 nei futuri BUILD/VERIFY.

---

# 15. Implicazioni per i prossimi cicli

Le lesson learned del C2 devono essere considerate comuni a tutti gli agenti.

In particolare:

1. nessun MODEL_SPEC deve assumere implicitamente l'esistenza di uno stato produttivo che il candidato non sa creare;
2. ogni MODEL_SPEC deve essere valutato rispetto allo stato iniziale reale dell'ambiente;
3. BUILD deve rispettare i runtime contract reali;
4. unit test e integration test devono essere distinti;
5. action dispatch non costituisce evidenza sufficiente di policy realization;
6. P0 e P1 devono essere verificati per correttezza dell'implementazione anche quando il positional effect dell'ambiente è trascurabile;
7. fail-safe e fail-closed devono essere osservabili durante VERIFY;
8. `TOURNAMENT_READY` deve implicare una minima realizzazione verificata della policy;
9. la telemetria deve misurare state transition oltre agli action count;
10. il tournament deve confrontare policy effettivamente realizzate, non semplicemente executable formalmente invocabili.

---

# 16. Lesson learned principale

Il risultato più importante del MODEL_SPEC TOURNAMENT C2 non è il ranking economico.

È la seguente evidenza metodologica:

> Una specifica formalmente coerente, un BUILD completato e una suite di test interamente verde non garantiscono che la policy descritta esista realmente nel runtime.

Il processo deve quindi verificare esplicitamente la catena:

```text
SPECIFICATION
    ↓
IMPLEMENTATION
    ↓
REAL ENVIRONMENT EXECUTION
    ↓
STATE TRANSITION
    ↓
POLICY REALIZATION
    ↓
ECONOMIC OUTCOME
```

Ogni passaggio è distinto e deve produrre propria evidenza.

---

# 17. Stato del round C2

```text
TOURNAMENT EXECUTION:
COMPLETE

THREE-CANDIDATE PERFORMANCE COMPARISON:
NOT CONCLUSIVE

ANTIGRAVITY POLICY REALIZATION:
FAILED

COPILOT POLICY REALIZATION:
FAILED

CODEX POLICY REALIZATION:
FUNCTIONAL BUT UNDER TARGET

COMMON PROCESS DEFECT:
TOURNAMENT_READY DID NOT REQUIRE
END-TO-END POLICY REALIZATION

FOUNDATION C2:
NO EVIDENCE OF A FOUNDATION-LEVEL
ROOT CAUSE FROM THE TWO FAILURE REVIEWS

NEXT PHASE:
COMMON READINESS-GATE FORMALIZATION
FOLLOWED BY CANDIDATE-SPECIFIC REMEDIATION
```

---

# 18. Vincolo per il lavoro successivo

Questo documento è una **lesson learned comune**.

Non autorizza automaticamente:

- modifica della Foundation C2;
- modifica dei MODEL_SPEC;
- modifica dei candidate executable;
- tuning;
- remediation;
- nuovo tournament;
- Kaggle validation.

Le successive modifiche devono essere autorizzate e tracciate nelle rispettive fasi.

Tutti gli agenti devono tuttavia considerare le evidenze qui raccolte come parte del contesto metodologico obbligatorio per i successivi cicli Kaggriculture.

```text
C2 ROUND LESSONS CONSOLIDATED
COMMON AWARENESS REQUIRED
REMEDIATION NOT AUTHORIZED BY THIS DOCUMENT
```