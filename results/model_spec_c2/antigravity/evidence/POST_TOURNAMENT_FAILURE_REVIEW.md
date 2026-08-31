# C2 POST-TOURNAMENT FAILURE REVIEW — ANTIGRAVITY

- **Review Date:** 2026-08-30
- **Candidate Reviewed:** `Antigravity C2`
- **Candidate Executable:** `src/agricola/strategy/antigravity/agent_c2.py`
- **Candidate Policy:** `src/agricola/strategy/antigravity/c2_policy.py`
- **Candidate Config:** `src/agricola/strategy/antigravity/c2_config.py`
- **MODEL_SPEC:** `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md`
- **Review Type:** Neutral Forensic Failure Review (Root Cause & Process Escape Analysis)

---

## 1. Evidenza Osservata

Nel `MODEL_SPEC TOURNAMENT C2`, Antigravity C2 ha ottenuto i seguenti risultati aggregati su 6 match e 3 seed indipendenti:

```text
Record: 0W - 3L - 3T
Mean final_money: $3,000.00 (Std: $0.00, Min: $3,000.00, Max: $3,000.00)
Mean active_crop_surface: 0.00 tiles
Total WATER: 0
Total HARVEST: 0
Total PLANT: 0
Total DIG: 0
Total MOVE: 0
Total PASS: 720 / episode (100% dei turni)
Total Market Orders: 0
Policy Realization: 0.0%
```

### 1.1 Runtime Diagnostic Trace
L'ispezione della telemetria runtime e dell'esecuzione disaggregata per step ha rivelato:

```python
Traceback (most recent call last):
  File "src/agricola/strategy/antigravity/agent_c2.py", line 21, in act
    unit_actions = self.policy.decide_actions(observation, player_index=player_index)
  File "src/agricola/strategy/antigravity/c2_policy.py", line 187, in decide_actions
    private = privates[player_index] if player_index < len(privates) else {}
KeyError: 0
```

Il metodo `__call__` di `AntigravityC2Agent` ha intercettato l'eccezione tramite il blocco `try...except` globale e ha restituito il fallback di sicurezza fail-closed:
```python
{"farmer": ["PASS"], "hands": [], "market": []}
```
L'episodio è continuato fino allo step 720 senza generare crash del processo o squalifiche dell'engine (`status: DONE`), ma producendo una paralisi operativa totale e una realizzazione della policy pari allo 0%.

---

## 2. Ricostruzione della Catena Causale Completa

```text
FOUNDATION C2
  │ (Definisce correttamente il feature contract CRP-01..12, INV-01..03, WRK-01..02)
  ▼
MODEL_SPEC ANTIGRAVITY C2
  │ (Specifica correttamente le feature di INV-01/02/03 come campi di 'private', ma omette
  │  un contratto formale sulla struttura top-level di 'observation' e criteri di smoke test E2E)
  ▼
BUILD
  │ (c2_policy.py:186-187 e 339-340 introducono l'assunzione errata 'privates = observation.get("private", [])'
  │  e 'privates[player_index]', assumendo che 'private' sia una lista multi-player analoga a 'farms')
  ▼
BUILD VERIFICATION
  │ (Verifica unicamente unit test isolati con mock artigianali ad-hoc; omette qualsiasi smoke test locale
  │  eseguito contro l'istanza reale di 'kaggle_environments.make("kaggriculture")')
  ▼
TEST SUITE (168 passed)
  │ (I 5 test in tests/test_antigravity_c2.py mockano 'observation["private"]' come lista contenente un dict:
  │  'private: [ {shed: ..., seeds: ...} ]'. I test passano al 100% confermando un mock errato)
  ▼
TOURNAMENT_READY: YES
  │ (Dichiarazione prematura di prontezza basata su gate superati che non coprivano il runtime integration)
  ▼
REAL KAGGRICULTURE RUNTIME
  │ (kaggle_environments inietta 'state[i].observation.private' come dict/Struct, non lista)
  ▼
FAILURE (KeyError: 0 -> Fail-closed PASS loop -> 0% Policy Realization)
```

---

## 3. MODEL_SPEC Review

L'analisi di `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md` evidenzia:

### 3.1 Punti di Forza e Correttezza Specifica
- **Consumer Mapping (Sezione 5):** Le feature `INV-01`, `INV-02`, `INV-03` indicano come sorgente runtime `private.seeds`, `private.shed`, `private.inventories`. La specifica fa riferimento ai campi interni corretti del dizionario privato.
- **Logica C2:** I gate `CRP-10` (`harvest_ready`), `CRP-09` (lifecycle a 6 stati) e la prevenzione DIG sono specificati in modo semanticamente solido.

### 3.2 Difetti e Lacune del MODEL_SPEC
1. **Assenza di Schema di Integrazione Runtime:** Il MODEL_SPEC non definisce il tipo e la segnatura esatta del payload `observation` fornito dal runner Kaggle (es. se `private` sia indicizzato per `player` o pre-filtrato per il chiamante).
2. **Omissione dei Criteri di Accettazione End-to-End (Smoke Gate):** Nella Sezione 10 ("Metriche di Verifica"), il MODEL_SPEC elenca metriche astratte (`crop_target_attainment`, `premature_harvest_count`), ma non prescrive un gate di accettazione E2E minimo (es. esecuzione di 1 episodio reale con output azioni non-PASS) come prerequisito per `TOURNAMENT_READY`.
3. **Classificazione del Difetto:** **Combinazione di B (BUILD defect), C (VERIFY defect) e D (Interface misunderstanding)**, con concorso di **A (MODEL_SPEC defect)** nella definizione dei contratti di runtime e dei gate di verifica.

---

## 4. BUILD Review

### 4.1 Origine dell'Assunzione Errata su `private`
Nell'engine Kaggle (`kaggle_environments/envs/kaggriculture/kaggriculture.py`), l'ambiente tiene internamente una lista:
```python
privates = [_new_private() for _ in range(num_agents)]
```
Tuttavia, quando l'engine passa l'osservazione a ciascun agente (`state[i].observation`), l'ambiente assegna:
```python
state[i].observation.player = i
state[i].observation.private = privates[i]  # Un singolo dict/Struct!
state[i].observation.farms = farms          # Una lista [farm0, farm1]
```
Lo sviluppatore di `c2_policy.py` ha osservato `farms = observation.get("farms", [])` e `farm = farms[player_index]` e ha applicato per simmetria lo stesso pattern a `private`:
```python
privates = observation.get("private", [])
private = privates[player_index] if player_index < len(privates) else {}
```

Quando `observation["private"]` è un dizionario (es. con 5 chiavi: `shed`, `seeds`, `inventories`, ecc.):
- `len(privates)` è `5`;
- `player_index < len(privates)` è `0 < 5` $\implies$ `True`;
- Viene eseguito `privates[0]`;
- Trattandosi di un dizionario con chiavi stringa, Python solleva `KeyError: 0`.

Questo identico pattern è ripetuto due volte:
1. In `decide_actions` (`c2_policy.py:186-187`);
2. In `decide_market_orders` (`c2_policy.py:339-340`).

---

## 5. VERIFY Review

### 5.1 Come ha fatto la suite a dare "168 passed" e "3/3 TOURNAMENT_READY"?
In `tests/test_antigravity_c2.py`, l'autore dei test ha scritto mock per `observation` che rispecchiavano l'implementazione errata invece del runtime reale:

```python
# tests/test_antigravity_c2.py (righe 118-124, 166-172, 203-209)
"private": [
    {
        "shed": {},
        "seeds": {"WHEAT": 5},
        "inventories": [{}],
    }
]
```

Tutti i test unitari hanno verificato la policy contro il **proprio mock non conforme**, passando con successo. Nessun test ha mai istanziato `kaggle_environments.make("kaggriculture")` ed eseguito `agent(env.steps[0][0]['observation'])`.

### 5.2 Il Test Minimo che Avrebbe Intercettato il Problema
Un test di fumo reale di 2 righe:
```python
def test_antigravity_c2_real_engine_smoke():
    env = kaggle_environments.make("kaggriculture", configuration={"episodeSteps": 5})
    env.reset()
    agent = AntigravityC2Agent()
    action = agent(env.steps[0][0]["observation"])
    # Fallisce immediatamente con KeyError / PASS se la struttura observation è errata!
    assert action != {"farmer": ["PASS"], "hands": [], "market": []}
```
Questo test avrebbe intercettato il difetto prima del commit.

---

## 6. Fail-Closed Analysis

In `src/agricola/strategy/antigravity/agent_c2.py`:
```python
def __call__(self, observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    try:
        return self.act(observation)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
```

### 6.1 Ruolo e Patologia del Fail-Closed
1. **In Produzione (Kaggle):** Un fail-closed è indispensabile per prevenire squalifiche per timeout o unhandled exception in match competitivi ufficiali.
2. **In BUILD / VERIFY:** Il fail-closed incondizionato, privo di logging o contatori diagnostici, agisce come un **meccanismo di occultamento (masking)** che converte errori fatali in risposte formalmente lecite (`PASS`).
3. **Requisiti Futuri:**
   - La policy deve esporre contatori diagnostici (`error_count`, `last_exception`);
   - In modalità test o smoke, il fail-closed NON deve mascherare eccezioni o deve sollevare assert se invocato in ambienti non di produzione;
   - Un agente che emette `PASS` per 100% dei turni deve essere rigettato dal gate di build readiness.

---

## 7. Root Cause Analysis (RCA)

```text
OBSERVED FAILURE:
  Antigravity C2 ha emesso 720 turni di PASS in tutte le 6 partite del torneo,
  ottenendo $3,000 (0% policy realization).

IMMEDIATE CAUSE:
  KeyError: 0 generato in c2_policy.py:187 e 340 dall'istruzione 'privates[player_index]'
  a causa del disallineamento di tipo ('dict' vs 'list') del campo 'observation["private"]'.

CONTRIBUTING CAUSE:
  1. Il blocco try...except globale in agent_c2.py ha silenziosamente intercettato l'eccezione,
     impedendo il fallimento esplicito del processo.
  2. I test unitari in tests/test_antigravity_c2.py hanno replicato il mock errato a lista.
  3. Mancanza di verifiche sull'output di azioni (nessun controllo su azioni diverse da PASS).

PROCESS ESCAPE:
  Assenza di un gate di Build Verification con 'Real Environment Smoke Test' (esecuzione
  locale di 1 episodio con kaggle_environments) prima della dichiarazione TOURNAMENT_READY.

ROOT CAUSE:
  Mancanza di una procedura di verifica di integrazione standardizzata e vincolante a livello
  di repository, che imponga l'esecuzione dell'agente nel runtime reale prima di rilasciare
  il tag TOURNAMENT_READY.
```

---

## 8. Escape Analysis

| Gate | Attivato? | Perché ha fallito / Come è sfuggito il difetto? |
|---|:---:|---|
| **Static / Type Check** | Parziale | `observation` è tipizzato come generico `Dict[str, Any]`; `privates[player_index]` è sintatticamente lecito per `Any`. |
| **Unit Test Suite** | SÌ | I test utilizzavano mock custom `{"private": [...]}` che rispecchiavano l'assunzione errata del codice. |
| **Full Pytest Suite (168 passed)** | SÌ | Nessun test nella suite pre-esistente invocava `AntigravityC2Agent` all'interno di un'istanza reale di `kaggle_environments`. |
| **Build Verification Gate** | SÌ | `BUILD_VERIFICATION.md` ha dichiarato `TOURNAMENT_READY: YES` basandosi esclusivamente sul superamento dei test unitari mockati. |
| **Harness Pre-Flight** | SÌ | Il pre-flight del torneo verificava hash e importabilità statica, non l'esecuzione dinamica di turni. |

---

## 9. Verifica Statica di Possibili Failure Latenti

Un'ispezione approfondita del codice di `c2_policy.py` senza modifiche ha identificato i seguenti elementi di rischio latente:

| Elemento / Linea | Descrizione | Livello di Rischio | Evidenza nel Codice |
|---|---|:---:|---|
| **Tabella `CROPS` (`c2_policy.py:19-24`)** | Incongruenza su `first_yield_day`: Strawberry impostato a 5 (reale = 10), Melon a 8 (reale = 10). Se il KeyError fosse risolto, l'agente tenterebbe harvest prematuri rifiutati dall'engine. | **CONFIRMED** | `CROPS["STRAWBERRY"]["first_yield_day"] = 5` vs `state.py:10` (`first_yield_day = 10`) |
| **Player Index Resolution (`agent_c2.py:19-38`)** | `__call__` invoca `self.act(observation)` senza estrarre `observation.get("player", 0)`. Se l'agente gioca come P1, interrogherà `farms[0]` (avversario) invece di `farms[1]`. | **CONFIRMED** | `def act(..., player_index=0)` e `__call__` non passa `player_index` |
| **Livestock Cow Transport (`c2_policy.py:274-306`)** | Il codice non contiene logica `PICKUP COW` dallo shed verso i pasture. Le mucche acquistate restano bloccate nello shed. | **CONFIRMED** | Nessuna azione `["PICKUP", "COW", ...]` presente nel loop di dispatch |
| **Reserved Targets Co-locazione** | La prenotazione `reserved.add(target_pos)` riserva la coordinata prima di verificare se l'agente vi sia arrivato, riducendo l'efficienza multi-occupancy. | **POSSIBLE** | `c2_policy.py:171` |
| **Land Expansion Check** | Controllo `quad_count < self.config.quadrants_owned` in `decide_market_orders`: `add_order(["BUY_LAND"], 1000.0)` emette correttamente `BUY_LAND`. | **NO EVIDENCE (OK)** | `c2_policy.py:359-363` |

---

## 10. Proposta di Acceptance Gates Minimi per Future Build

Per impedire categoricamente che un candidato con difetti di runtime integration possa essere dichiarato `TOURNAMENT_READY`, vengono definiti i seguenti gate vincolanti:

### 10.1 BUILD GATE (Static & Interface Integrity)
1. Convalida delle costanti biologiche contro `src/agricola/core/state.py` o l'engine runtime.
2. Risoluzione dinamica obbligatoria di `player_index` da `observation.get("player", 0)`.
3. Supporto trasparente per `observation["private"]` sia come `dict` che come `Struct`.

### 10.2 RUNTIME SMOKE GATE (Real Engine Execution)
1. Istanziazione obbligatoria di `kaggle_environments.make("kaggriculture", configuration={"episodeSteps": 48})`.
2. Esecuzione di almeno 48 step in posizione P0 e in posizione P1.
3. Verifica: **Zero eccezioni interne sollevate** (nessuna attivazione del fallback fail-closed).

### 10.3 POLICY REALIZATION GATE (Action & Metric Telemetry)
1. Presenza documentata di azioni operative: `total_plant_actions > 0`, `total_water_actions > 0`, `total_move_actions > 0`.
2. Produzione di ordini di mercato: `total_market_orders > 0` (`BUY_LAND`, `BUY_SEED`).
3. Mantenimento superficie attiva: `max_active_surface > 0` entro i primi 48 step.

### 10.4 TOURNAMENT READINESS GATE (Freeze Declaration)
1. `TOURNAMENT_READY: YES` può essere apposto in `BUILD_VERIFICATION.md` **esclusivamente** se tutti e tre i gate precedenti (Build, Smoke, Policy Realization) sono formalmente superati e loggati con evidenza numerica.

---

## 11. Conclusione della Review

Nessun codice, configurazione o MODEL_SPEC è stato alterato in questa sessione. La presente review stabilisce in modo univoco e documentato la catena causale del failure di Antigravity C2, identificando sia la causa immediata che i difetti latenti e le lacune di processo nei gate di verifica.

```text
ANTIGRAVITY C2 FAILURE VERDICT
==============================

Failure class: INTERFACE_TYPE_MISMATCH_AND_SILENT_FAIL_CLOSED_MASKING
Immediate cause: Unhandled KeyError: 0 in c2_policy.py:187/340 (observation['private'] trattato come list invece di dict/Struct).
Root cause: Assenza di un Real-Engine Smoke Test nei gate di Build Verification e dipendenza esclusiva da unit test con mock disallineati.
MODEL_SPEC defect: Omissione dello schema formale di integrazione runtime e dei criteri minimi di smoke test E2E.
BUILD defect: Assunzione errata su 'private', hardcoding di crop yield days errati (Strawberry=5, Melon=8), mancata gestione di player_index e pickup mucche.
VERIFY defect: Unit test basati su mock errati e totale assenza di verifica dinamica su kaggle_environments.
Process escape: Superamento del gate BUILD_VERIFICATION e dichiarazione TOURNAMENT_READY senza esecuzione di fumo reale.
Fail-closed contribution: Il blocco try...except in agent_c2.py ha mascherato l'errore convertendolo in 720 azioni PASS lecite, impedendo l'abort precoce.
Latent failure risk: HIGH (first_yield_day errati genererebbero premature harvest; player_index hardcoded romperebbe P1; pickup mucche assente).
Minimum required remediation: Correzione accesso private, allineamento tabella CROPS, estrazione player_index, e implementazione Real-Engine Smoke Test.
Required acceptance gates: Build Gate -> Runtime Smoke Gate (48 step real env) -> Policy Realization Gate (active_surface > 0) -> Tournament Readiness Gate.
Confidence: ABSOLUTE (100% replicabile su dati e codice congelati).
```
