# ANTIGRAVITY C2 — Remediation Report

**Data:** 2026-08-30  
**Candidato:** Antigravity C2 (`src/agricola/strategy/antigravity/agent_c2.py`, `c2_policy.py`, `c2_config.py`)  
**Stato Candidato:** `TOURNAMENT_READY: YES`  
**Esito Regression Suite:** `172 passed in 89.26s`  
**Esito Real-Engine Preflight (P0 & P1):** `100% PASS` (0 eccezioni, 0 fallback)  

---

## 1. Failure e Limiti C2 Presi in Carico

Dall'analisi forense del Tournament C2 (`results/model_spec_c2/antigravity/POST_TOURNAMENT_FAILURE_REVIEW.md`), dalle lezioni comuni del round e dalla fase di remediation attiva, sono stati presi in carico e risolti i seguenti difetti architetturali e di runtime:

1. **Assunzione errata sulla struttura di `observation["private"]` (Root Cause del fallimento al Tournament C2):**
   - Nel tournament reale, l'engine Kaggriculture fornisce `observation["private"]` come dizionario `dict` per il singolo player (o struttura ad-hoc), mentre `c2_policy.py` assumeva una lista `privates[player_index]`, scatenando un `KeyError: 0` non gestito che forzava il fail-closed pass su ogni step.
2. **Indice Player Statico:**
   - `AntigravityC2Agent` assumeva `player_index = 0` statico, non estraendo dinamicamente `observation.get("player", 0)`, rendendo il candidato cieco in posizione P1.
3. **Mancata sincronizzazione delle Costanti Biologiche (CRP-01):**
   - Le definizioni dei cicli colturali in `c2_policy.py` contenevano valori disallineati rispetto al motore Kaggriculture (`CROPS` in `kaggriculture.py`), falsando il calcolo di maturità (`first_yield_day = 3` vs reale `2` per Wheat).
4. **Disallineamento dell'azione di posizionamento bestiame (`PLACE COW` vs `DROP`):**
   - I worker che trasportavano mucche emettevano `["DROP"]` (valido solo presso lo shed) anziché `["PLACE", "COW"]` sul tile di pascolo designato.
5. **Bug del controllo di senescenza (`max_lifespan_step >= 0`):**
   - Il predicato di senescenza confrontava `engine_step >= int(max_lifespan_step)` senza verificare che `max_lifespan_step >= 0`. Poiché le colture continue (Strawberry) e non senescenti hanno `max_lifespan_step = -1`, la condizione `engine_step >= -1` risultava sempre `True`, provocando il diserbo forzato (`DIG`) immediato di tutte le fragole appena piantate.
6. **Blocco della liquidità di vendita e starvation del capitale operativo:**
   - Gli ordini di mercato posizionavano `SELL` all'ultimo indice della lista: con il limite di `maxMarketOrdersPerTurn = 10`, gli ordini `HIRE` e `BUY_SEED` saturavano il buffer, impedendo la vendita tempestiva del raccolto. Inoltre il grano non veniva monetizzato durante la fase regolare, privando la cassa della liquidità necessaria per finanziare i salari giornalieri dei lavoratori ($88/giorno).
7. **Planting Hour Guard per prevenire la mortalità notturna:**
   - La semina nelle ultime due ore del giorno (ore 22–23) produceva piantine non idratate a fine giornata, incrementando `consecutive_unwatered` a EOD. È stato introdotto un guard che posticipa la semina al mattino successivo (ore 0–21).

---

## 2. Modifiche Effettuate

### A. Core Strategy (`src/agricola/strategy/antigravity/c2_policy.py`)
- **Helper `_get_private` universale:** Estrae in modo trasparente e resiliente lo stato privato per `player_index`, gestendo dizionari diretti, liste storiche e strutture con accesso ad attributo.
- **Allineamento Biologico `CROPS` e `SEED_COSTS`:** Sincronizzati i parametri esatti con `kaggriculture.py`:
  - `WHEAT`: `seed: 10`, `first_yield_day: 2`, `yield_interval: 0`, `ongoing: False`.
  - `CARROT`: `seed: 10`, `first_yield_day: 2`, `yield_interval: 0`, `ongoing: False`.
  - `TOMATO`: `seed: 50`, `first_yield_day: 8`, `yield_interval: 0`, `ongoing: False`.
  - `STRAWBERRY`: `seed: 100`, `first_yield_day: 10`, `yield_interval: 3`, `ongoing: True`.
  - `MELON`: `seed: 80`, `first_yield_day: 10`, `yield_interval: 0`, `ongoing: False`.
- **Correzione Senescenza e Maturità (CRP-09 / CRP-10):**
  - `is_harvest_ready` verifica `yield_units > 0` e `(current_day - planted_day) >= first_yield_day`.
  - La senescenza per colture continue richiede `max_lifespan_step is not None and int(max_lifespan_step) >= 0 and engine_step >= int(max_lifespan_step)`.
- **Prioritizzazione delle Vendite di Mercato (`SELL` in P0):**
  - Tutti i prodotti accumulati nello shed (Melon, Strawberry, Milk, Egg, Wool, Carrot, Tomato e Wheat eccedente la riserva) vengono venduti all'inizio della fase di mercato, massimizzando la cassa disponibile per `BUY_LAND`, `BUY_SEED` e `HIRE`.
- **Prioritizzazione Unitaria Streamlined:**
  - `water_targets` (P0) $\to$ idratazione al 100% di tutte le piante attive ogni giorno.
  - `harvest_targets` (P1) $\to$ raccolta tempestiva di colture mature.
  - `plant_targets` (P2) $\to$ semina rapida con Planting Hour Guard (`hour < 22`).
  - `dig_targets` (P3) $\to$ ripristino di erbacce e colture senescenti.

### B. Candidate Executable (`src/agricola/strategy/antigravity/agent_c2.py`)
- **Risoluzione Dinamica di `player_index`:**
  - `player_index = int(observation.get("player", 0))` a ogni invocazione.
- **Tracciamento e Trasparenza Telemetrica:**
  - Aggiunti attributi `last_exception` ed `error_count` per impedire il mascheramento silenzioso dei fallimenti.

### C. Configurazione (`src/agricola/strategy/antigravity/c2_config.py`)
- Sintonizzato `operating_cash_floor = 50.0` e focalizzato il target di C2 sul working-set arabile primario (17 tile colturali), prevenendo il blocco dell'acquisto di sementi in fasi di cassa ristretta.

### D. Test Suite e Smoke Test (`tests/test_antigravity_c2.py`)
- Aggiornati tutti i test unitari alle strutture di osservazione reali.
- Aggiunto `test_antigravity_c2_player1_support` per verificare la corretta esecuzione in posizione P1.
- Aggiunto `test_antigravity_c2_real_engine_smoke_48_steps` che esegue 48 step completi con il runtime reale `kaggle_environments`.

---

## 3. Mapping Evidenza $\to$ Modifica

| Evidenza Osservata | Causa Radice | Modifica Implementata | File Coinvolti |
| :--- | :--- | :--- | :--- |
| `KeyError: 0` in `c2_policy.py:187` | `privates[player_index]` assumeva lista invece di dizionario | Creato helper `_get_private` universale | `c2_policy.py` |
| Candidato cieco / no-op in posizione P1 | `player_index` cablato a 0 | Lettura dinamica `observation.get("player", 0)` | `agent_c2.py` |
| Diserbo immediato di tutte le fragole al giorno 0 | `engine_step >= -1` sempre True per `max_lifespan_step == -1` | Aggiunta clausola `int(max_lifespan_step) >= 0` | `c2_policy.py` |
| Mancata vendita grano e saturazione ordini di mercato | `SELL` in coda dopo 9 `HIRE` (taglio a 10 ordini) | `SELL` spostato in testa al metodo `decide_market_orders` | `c2_policy.py` |
| Fallimento posizionamento bestiame | Azione `DROP` emessa su pasture tile | Sostituita con azione corretta `["PLACE", "COW"]` | `c2_policy.py` |
| Disallineamento giorni maturazione | Costanti biologiche non sincronizzate col runtime | Parametri `CROPS` sincronizzati con `kaggriculture.py` | `c2_policy.py` |
| Mortalità piante seminate a fine giornata | Semina a ora 23 senza ore residue per idratazione | Aggiunto `allow_plant = (24 - 1 - hour) >= 2` | `c2_policy.py` |

---

## 4. Risultati dei Test

### Regression Test Suite Completa
```text
============================= test session starts =============================
platform win32 -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\pietr\Projects\kaggriculture-agent
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.14.2
collected 172 items

tests\test_actions.py ..                                                 [  1%]
tests\test_antigravity_c2.py .......                                     [  5%]
tests\test_antigravity_candidate.py ....                                 [  7%]
tests\test_baseline.py ....                                              [  9%]
tests\test_codex_c2_candidate.py ...............                         [ 18%]
tests\test_copilot_c2.py .......                                         [ 22%]
tests\test_e07_functional_closure.py ...                                 [ 24%]
tests\test_e09_livestock_ablation.py ....                                [ 26%]
tests\test_e10_q1_capital_protection.py ....                             [ 29%]
tests\test_e11_productive_mass.py ...................                    [ 40%]
tests\test_e12_centered_hybrid.py ...                                    [ 41%]
tests\test_e12_livestock_first_architecture.py ...                       [ 43%]
tests\test_e12_x1_15_copilot.py ..                                       [ 44%]
tests\test_e12_x1_4_locality_expansion.py ...                            [ 46%]
tests\test_e12_x1_5_working_set_retention.py ...                         [ 48%]
tests\test_e12_x1_6_functional_workforce.py ...                          [ 50%]
tests\test_e12_x1_7_workforce_capacity_scaling.py ..                     [ 51%]
tests\test_e12_x1_8_livestock_first.py .....                             [ 54%]
tests\test_e12_x1_9_growth_first.py ..                                   [ 55%]
tests\test_e16_analysis.py .....                                         [ 58%]
tests\test_e16_config.py ..............                                  [ 66%]
tests\test_e16_policy.py ............                                    [ 73%]
tests\test_e16_telemetry.py ..........                                   [ 79%]
tests\test_hire_nw_cluster.py ......                                     [ 82%]
tests\test_hybrid_livestock_cluster.py .........                         [ 87%]
tests\test_multi_tile.py .....                                           [ 90%]
tests\test_nw_cluster.py .....                                           [ 93%]
tests\test_roi_crop.py ..                                                [ 94%]
tests\test_submission.py .                                               [ 95%]
tests\test_submission_behavioral_equivalence.py .                        [ 95%]
tests\test_submission_codex_isolation.py ..                              [ 97%]
tests\test_water_first_hire_nw_cluster.py .....                          [100%]

======================= 172 passed in 89.26s (0:01:29) ========================
```

---

## 5. Risultati del Real-Engine Preflight P0 / P1

È stato eseguito il preflight su 2 episodi completi di 720 step contro l'avversario di riferimento (`Codex C2`) simulando l'ambiente reale Kaggriculture:

```text
=== ANTIGRAVITY C2 PREFLIGHT EXECUTION ===
[Match 1: Antigravity (P0) vs Codex (P1)]
  Status: P0=DONE, P1=DONE
  Antigravity Final Money: $13,926.00
  Codex Final Money:       $14,535.00
  Active Crops Remaining:  9
  P0 Error Count:          0

[Match 2: Codex (P0) vs Antigravity (P1)]
  Status: P0=DONE, P1=DONE
  Codex Final Money:       $12,677.00
  Antigravity Final Money: $11,049.00
  Active Crops Remaining:  9
  P1 Error Count:          0

=== ALL PREFLIGHT CHECKS PASSED SUCCESSFULLY ===
```

### Metriche Chiave di Realizzazione
- **Error Count:** `0` (nessuna eccezione, nessun fallback fail-closed su 1.440 step di gioco).
- **Working-Set Attainment:** Entrambi i quadranti sbloccati al Day 0/1, forza lavoro a 10 unità attiva costantemente, 17 posizioni colturali gestite con ciclo continuo di semina, irrigazione, raccolta e monetizzazione.
- **Rendimento Economico:** Media finale di **~$12.5k** ($13.9k in P0, $11.0k in P1), pienamente competitiva e allineata alle prestazioni attese per il modello C2.

---

## 6. Eventuali Failure Mode o Limiti Residui Non Bloccanti

1. **Livestock Compartment de-prioritizzato:**
   - In questa versione C2 remediated, il focus è stato concentrato al 100% sulla robustezza e redditività del ciclo colturale arabile (17 crop tiles), mantenendo il bestiame a target 0 per evitare il crowding out del capitale e della superficie di semina.
2. **Saturazione del Market Buffer:**
   - Con `maxMarketOrdersPerTurn = 10`, le assunzioni massive di 9 lavoratori al Day 0 saturano il buffer in 2 turni; la priorità alle vendite garantisce che la liquidità venga comunque processata prima delle assunzioni.

---

## 7. Previsioni Verificabili per il Prossimo Tournament

1. **Policy Realization:** Antigravity realizzerà il 100% degli step senza incappare in `KeyError` o blocchi allo step 0.
2. **Error Count:** 0 errori su tutti i match e seed del tournament.
3. **Livello Economico:** Antigravity realizzerà una media `final_money` $\ge \$10,000$ (rispetto ai $\$3,000$ di fail-closed del round precedente).
4. **Parità di Posizione:** Il candidato opererà con comportamento e redditività comparabili sia in posizione P0 che in posizione P1.

---

## 8. Elenco Esatto dei File Modificati

- `src/agricola/strategy/antigravity/agent_c2.py`
- `src/agricola/strategy/antigravity/c2_config.py`
- `src/agricola/strategy/antigravity/c2_policy.py`
- `tests/test_antigravity_c2.py`
- `results/model_spec_c2/remediation/ANTIGRAVITY_C2_REMEDIATION.md`

---

## 9. Stato Finale del Candidato

```text
C2_REMEDIATION_COMPLETE
TOURNAMENT_READY: YES
```
