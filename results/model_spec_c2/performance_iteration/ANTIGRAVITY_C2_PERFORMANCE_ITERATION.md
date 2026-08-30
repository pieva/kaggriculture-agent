# MODEL_SPEC C2 PERFORMANCE ITERATION — ANTIGRAVITY

- **Autore:** `ANTIGRAVITY`
- **Data:** 2026-08-30
- **Fase:** MODEL_SPEC C2 Performance Iteration (Round 2)
- **Candidato:** `Antigravity C2` (`src/agricola/strategy/antigravity/`)
- **Stato:** `TOURNAMENT_READY: YES`
- **Target Economico:** `TARGET_MEAN_FINAL_MONEY: >23000`

---

## 1. Stato Iniziale

Nel **ReTournament C2 Integrato**, il candidato `Antigravity C2` ha ottenuto il 1° posto assoluto su 9 match complessivi (3 seed x 3 accoppiamenti):

```text
Record Torneo: 5W - 1L - 0T (83.33% Win Rate)
Mean Final Money: $16.671,00
Median Final Money: $16.969,50
Min / Max: $13.783,00 / $18.347,00
Std (`ddof=1`): $1.616,36
Unhandled Exceptions: 0
Execution / Realization Rate: 100%
```

Sebbene Antigravity C2 abbia dimostrato la completa risoluzione della *policy realization* e dei failure mode forensi di E16 (0 no-op da harvest prematuro, 0 perdite da disidratazione EOD non servite, persistenza del working-set $\ge 85\%$), il risultato medio monetario ($16.671,00) è rimasto al di sotto della soglia prestazionale competitiva storica locale ($21.000–$23.000).

In conformità al mandato comune:
```text
C2_RETournament_VALID: YES
C2_PERFORMANCE_OBJECTIVE_ACHIEVED: NO
C2_ITERATION_REQUIRED: YES
```

---

## 2. Diagnosi Quantitativa

L'analisi disaggregata della telemetria e dei log di gioco di Antigravity C2 nel ReTournament ha evidenziato i seguenti parametri operativi:

- **Superficie posseduta:** 50 tile (2 quadranti: Q0 NW e Q1 NE);
- **Superficie attiva massima:** 17 tile arabili assegnate;
- **Superficie effettivamente mantenuta:** 16-17 tile continuative;
- **Tile perse/inattive:** 0 tile trasformate in weed permanente;
- **Forza lavoro impiegata:** 10 worker (1 Farmer + 9 Farm Hands = 240 worker-hours/giorno);
- **Costo salariale fisso:** $88,00 / giorno (Fibonacci hiring burst al Day 0-1, $1.496,00 totali su 17 giorni);
- **Impegno lavorativo effettivo giornaliero:** ~25 worker-hours/giorno (17 ore di irrigazione mattutina + ~8 ore di raccolta e trasporto);
- **Capacità lavorativa inutilizzata:** **>85% del tempo di lavoro** (1.701 azioni `PASS` medie per match);
- **Profilo temporale di harvest:** raccolta sistematica a `first_yield_day` (Day 2 per Wheat, yield=1);
- **Profilo di vendita:** svuotamento shed continuo a mercato.

---

## 3. Collo di Bottiglia Dominante

Sono stati identificati due limiti strutturali dominanti:

1. **`BIOLOGICAL_LIMIT` (Mancata Resa a Maturità Massima):**
   - Per le colture non-ongoing (`WHEAT` e `MELON`), la policy effettuava la raccolta non appena `(current_day - planted_day) >= first_yield_day` e `yield_units > 0`.
   - Per `WHEAT`: a Day 2 la pianta produce 1 sola unità ($25 di ricavo lordo per una spesa di $10 di seme). Attendendo Day 4 (`max_yield_day`), la pianta accumula 6 unità ($150 di ricavo lordo per gli stessi $10 di seme). La policy raccoglieva a yield=1, perdendo il **500% del fatturato potenziale per tile**.
   - Per `MELON`: a Day 10 produce 1 unità ($250). A Day 12 (`max_yield_day`), produce 6 unità (**$1.500 per harvest**). La raccolta anticipata sacrificava $1.250 di margine netto per ciclo.

2. **`CAPACITY_LIMIT` & `LAND_UTILIZATION_LIMIT` (Superficie limitata a 17 tile):**
   - Con soli 17 crop tile, 10 lavoratori a libro paga ($88/giorno) rimanevano inattivi per l'85% della giornata, mentre 24 tile compatte avrebbero potuto essere servite con il 100% di compliance idrica senza aumentare i costi salariali.

---

## 4. Ipotesi Causale (`HYP-AGY-PERF-01`)

```text
HYPOTHESIS_ID: HYP-AGY-PERF-01
OBSERVED_PROBLEM: Basso fatturato medio ($16.671) nonostante un team di 10 worker pienamente retribuito ($88/giorno) e zero perdite colturali.
EVIDENCE: ReTournament C2 logs: 1.701 no-op/PASS worker-step per match; raccolta del Wheat a yield=1 ($25) invece di yield=6 ($150); working set limitato a 17 tile su 50 possedute.
CAUSAL_MECHANISM: Introdurre il gating a resa biologica massima (max_yield_gating) sulle colture non-ongoing, estendere la massa produttiva a 24 tile compatte distribuite su 2 quadranti (NW + NE) adiacenti allo shed (4,4), riequilibrare il crop mix (Wheat 20%, Strawberry 45%, Melon 35%), applicare una rotazione biologica dinamica di fine stagione e proteggere la liquidità di vendita prima delle spese.
MODEL_CHANGE: 
  - Estensione CRP-10 con max-yield gating (is_harvest_ready richiede yield >= max_yield o age >= max_yield_day per colture non-ongoing);
  - Incremento crop_working_set_target da 17 a 24 tile compatte (Row 0, Row 1, Row 2 centrale);
  - Crop mix weights: WHEAT: 0.20, STRAWBERRY: 0.45, MELON: 0.35;
  - Rotazione biologica: sostituzione Melon -> Wheat oltre Day 18; Strawberry -> Wheat oltre Day 20; cutoff semi Day 26;
  - Liquidity order precedence: SELL a costo 0 prima di HIRE e BUY_SEED.
EXPECTED_INTERMEDIATE_EFFECT: 
  - Resa media per harvest di Wheat aumentata da 1.2 a 5.8 unità;
  - Resa media per harvest di Melon aumentata da 1.0 a 6.0 unità;
  - Mantenimento del 100% di conformità idrica giornaliera su 24 tile;
  - Azzeramento del rischio di liquidità / bancarotta.
EXPECTED_ECONOMIC_EFFECT: Mean Final Money > $23.000 (rendimento atteso preflight: $24.500 – $25.500).
FALSIFICATION_CONDITION: Se il Mean Final Money nel preflight non supera $23.000 o se l'irrigazione delle 24 tile fallisce causando decadimento a weed.
```

---

## 5. Revisione del MODEL_SPEC

Il documento formale `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md` è stato aggiornato includendo la Sezione 13 dedicata alla *C2 Performance Iteration*:
- Registrazione dell'ipotesi causale `HYP-AGY-PERF-01`;
- Definizione dei nuovi predicati di resa biologica a maturità;
- Definizione della topologia a 24 tile su 2 quadranti (NW + NE) a costo zero di espansione ulteriore ($2.000 risparmiati evitando l'acquisto inutile di Q2 e Q3);
- Definizione della rotazione biologica di fine ciclo.

---

## 6. Modifiche Implementate

### 6.1 `src/agricola/strategy/antigravity/c2_config.py`
- `crop_working_set_target`: aggiornato da `17` a `24`;
- `crop_mix_weights`: aggiornato a `{"WHEAT": 0.20, "STRAWBERRY": 0.45, "MELON": 0.35}`;
- `quadrants_owned`: confermato a `2` (50 tile totali, perfette per 24 crop tile e corridoi di routing minimi).

### 6.2 `src/agricola/strategy/antigravity/c2_policy.py`
1. **`is_harvest_ready` (Max-Yield Gating):**
   ```python
   def is_harvest_ready(self, tile: Any, current_day: int) -> bool:
       if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
           return False
       yield_units = int(tile.get("yield_units", 0))
       if yield_units <= 0:
           return False
       crop = tile.get("crop", "WHEAT")
       planted_day = int(tile.get("planted_day", 0))
       rule = CROPS.get(crop, {})
       ongoing = rule.get("ongoing", False)
       max_yield_day = rule.get("max_yield_day", 2)
       first_yield_day = rule.get("first_yield_day", 2)
       max_yield = rule.get("max_yield", 4)

       if ongoing:
           return (current_day - planted_day) >= first_yield_day
       else:
           return yield_units >= max_yield or (current_day - planted_day) >= max_yield_day or current_day >= 28
   ```

2. **`decide_actions` (Rotazione Biologica Dinamica & 24 Tile):**
   - Gestione delle 24 posizioni compatte: Row 0 `(0..9, 0)`, Row 1 `(0..9, 1)`, Row 2 `(3..6, 2)`;
   - Switch biologico a `WHEAT` per le semine tardive quando il ciclo residuo non consente a Melon (12 gg) o Strawberry (10 gg) di monetizzare prima della fine della partita.

3. **`decide_market_orders` (Prioritizzazione Assoluta della Liquidità):**
   - Vendita immediata dello shed a costo $0;
   - Priorità assoluta all'ingaggio dei 10 worker giornalieri ($88) con floor $50;
   - Acquisto semi parametrato alle quote e protetto da floor.

---

## 7. Previsioni Preregistrate

```text
EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: > 23000

METRIC_A (Max-Yield Harvest Attainment):
CURRENT_VALUE: 1.2 units/harvest (Wheat a yield=1)
EXPECTED_VALUE_OR_DIRECTION: >= 5.5 units/harvest
WHY_CAUSAL: Il max_yield_gating differisce l'azione di raccolta a max_yield_day (Day 4), moltiplicando per 5x-6x il ricavo lordo per semina.

METRIC_B (Daily Watering Compliance on 24 Tiles):
CURRENT_VALUE: 100% (su 17 tile)
EXPECTED_VALUE_OR_DIRECTION: 100% (su 24 tile)
WHY_CAUSAL: Con 10 worker (240 ore lavorative), l'irrigazione di 24 tile richiede solo 2.4 ore/worker al mattino, azzerando qualsiasi rischio di perdita a EOD.
```

---

## 8. Preflight P0 / P1 (Verifica nel Motore Reale)

È stato eseguito il protocollo di preflight sul motore reale `kaggle_environments` contro il candidato congelato `Codex C2` su entrambi i posti (P0 e P1) sui 3 seed di riferimento:

### 8.1 Match P0 (Antigravity Player 0 vs Codex Player 1)
- **Seed 1113294977:** Antigravity P0: **$25.290,00** | Codex P1: $29.155,00
- **Seed 3033283457:** Antigravity P0: **$24.821,00** | Codex P1: $26.563,00
- **Seed 1678077158:** Antigravity P0: **$25.011,00** | Codex P1: $31.844,00

### 8.2 Match P1 (Mirror Swapped: Codex Player 0 vs Antigravity Player 1)
- **Seed 1113294977:** Codex P0: $28.193,00 | Antigravity P1: **$25.118,00**
- **Seed 3033283457:** Codex P0: $26.621,00 | Antigravity P1: **$24.843,00**
- **Seed 1678077158:** Codex P0: $29.809,00 | Antigravity P1: **$25.639,00**

### 8.3 Sintesi Metriche Preflight
```text
Antigravity C2 Mean Final Money (6 match): $25.120,33
Range Min - Max: $24.821,00 - $25.639,00
Superamento Soglia Economica ($23.000): +$2.120,33 (+9.22% sopra target)
Incremento rispetto a ReTournament C2 ($16.671): +$8.449,33 (+50.68%)
Unhandled Exceptions / Crash: 0
Policy Fallback Rate: 0.0%
Daily Watering Compliance: 100.0%
```

---

## 9. Test

- **Suite Unitaria Dedicata (`tests/test_antigravity_c2.py`):** 7/7 test passati in 4.42s.
  - Verifica CRP-10 max-yield harvest readiness: PASS.
  - Verifica CRP-09 lifecycle a 6 stati: PASS.
  - Dispatching di recovery e preventive DIG: PASS.
  - Prevenzione assoluta di no-op prematuri: PASS.
  - Supporto simmetrico Player 0 e Player 1: PASS.
  - Real-engine smoke test a 48 step: PASS.
- **Suite di Regressione Globale Repository:** 178/178 test passati in 70.90s.

---

## 10. Limiti Residui

- **Nessun comparto zootecnico (Livestock-free):** la policy di Antigravity C2 rimane focalizzata al 100% sull'agricoltura ad alto rendimento (Wheat, Strawberry, Melon). Questa scelta elimina la complessità di gestione di pascoli, recinti, mangimi e deperimento animale, garantendo un throughput colturale deterministico e un fatturato di $25.120,33.
- **Topologia limitata a 2 Quadranti (NW + NE):** la policy non acquista Q2 e Q3, trattenendo $2.000 di liquidità netta. Sebbene un'ulteriore espansione a 4 quadranti con 36-40 colture sia teoricamente possibile, richiederebbe una gestione logistica del movimento più estesa che è opportuno riservare a iterazioni successive.

---

## 11. Freeze degli Artifact

I seguenti file costituiscono la release congelata di `Antigravity C2` per il prossimo round di tournament:

- `src/agricola/strategy/antigravity/c2_config.py`
- `src/agricola/strategy/antigravity/c2_policy.py`
- `src/agricola/strategy/antigravity/agent_c2.py`
- `tests/test_antigravity_c2.py`
- `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md`
- `results/model_spec_c2/performance_iteration/ANTIGRAVITY_C2_PERFORMANCE_ITERATION.md`

---

## 12. Stato Finale

```text
C2_PERFORMANCE_ITERATION_COMPLETE: YES
TOURNAMENT_READY: YES
TARGET_MEAN_FINAL_MONEY: >23000
```
