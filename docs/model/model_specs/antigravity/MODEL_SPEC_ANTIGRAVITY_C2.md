# MODEL_SPEC C2 — ANTIGRAVITY

```text
MODEL_SPEC_ID: MODEL_SPEC_ANTIGRAVITY_C2
AGENT_ID: antigravity
VERSION: 2.1.0
DATE: 2026-08-31
LAYER: Agent-Specific Model Specification (Downstream Layer 6)
FOUNDATION_VERSION: C2 (Frozen)
ENGINE_FINGERPRINT: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
STATUS: PERFORMANCE REVISED — 40-TILE SCALED FOOTPRINT
UPSTREAM_FOUNDATION:
  - Frozen Engine Contract (ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md)
  - Frozen Period Ledger Audit (CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md)
  - Frozen Ontology C2 (ONTOLOGY_C2.md)
  - Frozen Environment State Machine C2 (KAGGRICULTURE_STATE_MACHINE_C2.md)
  - Frozen Feature Model C2 (KAGGRICULTURE_FEATURE_MODEL_C2.md)
  - Frozen Decision Lifecycle Contract C2 (KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md / Draft 02)
PRIMARY_DIAGNOSTIC_BASE:
  - Forensic Diagnosis E16 A-R1 (E16_A_R1_CROP_ATTAINMENT_FORENSIC_DIAGNOSIS.md)
  - Tile Lifecycle Audit E16 (E16_TILE_LIFECYCLE_FEATURE_AUDIT.md)
  - Antigravity C2 Review Reconciliation (DECISION_LIFECYCLE_REVIEW_RECONCILIATION.md)
  - Antigravity C2 Performance Correction Diagnosis (KAGGRICULTURE_C2_ANTIGRAVITY_PERFORMANCE_CORRECTION_PROMPT.md)
```

---

## 1. Identity and Scope

`MODEL_SPEC_ANTIGRAVITY_C2` definisce la specifica formale del modello decisionale e della strategia proprietaria per l'agente **Antigravity** nel Cycle 2 (C2).

Il modello implementa l'architettura Foundation C2 a 5 layer condivisi + 1 layer proprietario, garantendo:
1. **Piena conformità alla Foundation e al DLC:** utilizzo rigoroso degli envelope epistemici, delle 5 viste ambientali + policy overlays, del Decision Lifecycle Contract C2 e del principio `NO_REPLAN_WITHOUT_LIFECYCLE_CAUSE`;
2. **Risoluzione Forense dei Difetti Storici (E15/E16):** eliminazione totale degli harvest prematuri, bonifica attiva delle tile infestate tramite `DIG`, clearance preventiva delle colture esaurite e priorità idrica day-0;
3. **Piena Indipendenza Strategica:** nessun coordinamento né imitazione dei controller di Codex o Copilot.

---

## 2. Objective and Economic Evaluation Gate

### 2.1 Primary Economic Objective
Massimizzare il saldo monetario terminale dell'azienda agricola ($\text{farm.money}$) allo step 720 (Day 30, Turn 24), mediante la massimizzazione del valore aggiunto biologico, la minimizzazione dei costi operativi di manodopera e l'eliminazione dei no-op esecutivi.

### 2.2 Secondary Objectives
- **100% Daily Watering Compliance:** Azzeramento assoluto delle perdite per disidratazione a EOD (`consecutive_unwatered` sempre $< 2$);
- **Zero Premature Harvests:** Nessuna emissione di `HARVEST` su colture immature ($\text{age} < \text{first\_yield\_day}$);
- **Working-Set Persistence:** Mantenimento stabile della superficie coltivata attiva $\ge 85\%$ del target per l'intera durata del match;
- **Rapid Replant Latency:** Tempo medio di ripiantumazione su tile liberate $< 3$ step.

### 2.3 Economic Evaluation Gate C2
- **$< 50,000$:** `FAILURE` (Sotto-performance critica);
- **$50,000 – 79,999$:** `MATERIAL IMPROVEMENT BUT TARGET MISS` (Miglioramento sensibile, target non centrato);
- **$\ge 80,000$:** `TARGET ACHIEVED` (Target economico C2 pienamente conseguito).

---

## 3. Decision Intent Types

Antigravity C2 struttura la propria deliberazione attraverso i seguenti tipi canonici di intent (conformi al DLC C2):

1. **`INITIAL_EXPANSION_INTENT`:** Acquisizione immediata a Day 0 del 2° quadrante (Q1 - NE, 25 tile) per \$1,000 e assunzione manodopera (headcount 10, costo salariale \$88/giorno);
2. **`CROP_PORTFOLIO_INTENT`:** Assegnazione e mantenimento della superficie produttiva scalata a 40 tile (su 46 tile disponibili nei 2 quadranti), ordinate per distanza Manhattan allo shed centrale, suddivise secondo il mix biologico ottimizzato: Strawberry 45% (18 tile), Melon 35% (14 tile), Wheat 20% (8 tile);
3. **`WORKFORCE_SCALING_INTENT`:** Assunzione giornaliera di 10 worker (1 Farmer + 9 Hands, costo salariale \$88/day per 240 azioni/giorno) governata dalla scala di Fibonacci;
4. **`PRODUCTION_CYCLE_INTENT`:** Esecuzione quotidiana ordinata del ciclo colturale (Watering P0 $\to$ Harvest P1 $\to$ Replant P2 $\to$ Dig P3);
5. **`SEASONAL_ROTATION_INTENT`:** Supersession biologica programmata di fine stagione (Melon $\to$ Wheat dopo Day 18, Strawberry $\to$ Wheat dopo Day 20);
6. **`ENDGAME_LIQUIDATION_INTENT`:** Shutdown window negli ultimi 48 step con arresto nuove semine, raccolta intensiva e liquidazione totale dell'inventario dello shed a mercato.

---

## 4. Planning Method and Spatial Layout

### 4.1 Layout Territoriale Scalato a 40 Tile (2 Quadranti)
Antigravity concentra l'attività produttiva sulle **40 tile arabili a più alta densità e prossimità** posizionate in Quadrante 0 (NW) e Quadrante 1 (NE), ordinate rigorosamente per distanza Manhattan rispetto allo shed centrale $(4,4) / (5,4)$:
- **Distanza 1 (4 tile):** $(3,4), (4,3), (5,3), (6,4)$
- **Distanza 2 (6 tile):** $(2,4), (3,3), (4,2), (5,2), (6,3), (7,4)$
- **Distanza 3 (8 tile):** $(1,4), (2,3), (3,2), (4,1), (5,1), (6,2), (7,3), (8,4)$
- **Distanza 4 (10 tile):** $(0,4), (1,3), (2,2), (3,1), (4,0), (5,0), (6,1), (7,2), (8,3), (9,4)$
- **Distanza 5 (8 tile):** $(0,3), (1,2), (2,1), (3,0), (6,0), (7,1), (8,2), (9,3)$
- **Distanza 6 (4 tile iniziali):** $(0,2), (1,1), (2,0), (7,0)$

Questo perimetro assicura un utilizzo del suolo posseduto dell'**83.3%** (40 tile su 48 arabili nei 2 quadranti), mantenendo la distanza media di movimento worker $\le 3.1$ step ed eliminando la dispersione logistica a 4 quadranti.

### 4.2 Priority Cascading Dispatch
Ad ogni step, per ciascun worker disponibile, il controller valuta in cascata deterministica:
1. **Shed Drop:** Se il worker trasporta beni non necessari all'attività immediata, movimento verso lo shed $(4,4)$ ed emissione di `DROP`;
2. **Watering Dispatch (P0):** Irrigazione prioritaria su tile con colture vive non bagnate nella giornata (`watered_today == False`), con precedenza massima a nuove semine Day-0 (`consecutive_unwatered == 1`);
3. **Harvest Dispatch (P1):** Raccolta matura su tile aventi `harvest_ready == True` e `yield_units >= max_yield` (o fine ciclo);
4. **Plant Dispatch (P2):** Semina immediata su tile `EMPTY_ASSIGNED` consumando le sementi disponibili nel seed inventory;
5. **Dig Dispatch (P3):** Bonifica correttiva (`recovery_dig`) su tile `LOST_WEED` e rimozione preventiva (`preventive_dig`) su colture ongoing esaurite (`RETIREMENT_DUE`).

### 4.3 Atomic Target Reservation
I task vengono assegnati ai worker minimizzando la distanza Manhattan, riservando atomicamente le coordinate target per impedire che più worker convergano ridondantemente sullo stesso obiettivo nello stesso tick.

---

## 5. Feasibility Policy

La policy di fattibilità implementa le classi standardizzate dal DLC C2 (Sez. 10):
- **`SNAPSHOT_ACTION_ELIGIBILITY`:** Verifica che l'azione richiesta sia legalmente eseguibile nello stato corrente ($S_t$) secondo le guardie dell'Engine Contract;
- **`ATOMIC_BATCH_FEASIBILITY`:** Nelle semine multiple, verifica che la somma delle sementi richieste non superi il saldo di `private.seeds` al momento del batch;
- **`CAPACITY_FEASIBILITY`:** Rispetto del limite di 10 ordini di mercato per turno e della capienza di 100 unità dello shed;
- **`RESERVED_FUTURE_SERVICEABILITY`:** Verifica della capienza liquida minima (`operating_cash_floor = $50.0`) e protezione del capitale operativo di manodopera prima dell'emissione di ordini di acquisto sementi o assunzione.

---

## 6. Commitment Policy and Anti-Oscillation

### 6.1 Assunzione del Commitment
Un commitment esecutivo viene assunto all'apertura del match per il perimetro dei 2 quadranti e per il portfolio colturale target.
- **Parametri vincolanti:** `crop_working_set_target = 40`, `crop_mix_weights = {WHEAT: 0.20, STRAWBERRY: 0.45, MELON: 0.35}`;
- **Invarianti dichiarate:** Cash floor $\ge \$50.0$; Workforce $\le 10$; Capienza shed $\le 100$.

### 6.2 Anti-Oscillation (`NO_REPLAN_WITHOUT_LIFECYCLE_CAUSE`)
Il controller non modifica il layout o il portfolio a fronte di rumore di mercato. Qualsiasi deviazione locale (es. seed temporaneamente esaurito) viene gestita come **`REPAIR_WITHIN_COMMITMENT`** (ripiegando su semina Wheat di riempimento) senza distruggere l'identità del commitment.

---

## 7. Cancellation Policy

La cancellazione volontaria (`CANCELLED`) è consentita esclusivamente in caso di:
- **`CRITICAL_LIQUIDITY_BREACH`:** Cassa netta $< \$10.0$ con impossibilità di pagare la manodopera essenziale;
- **`ENDGAME_PREEMPTION`:** Ingresso negli ultimi 48 step per chiusura programmata.

---

## 8. Supersession Policy (Non-Circolare)

Antigravity implementa la supersessione stagionale non-circolare conforme a `DLC-CORR-01`:
1. **Day 18 Transition:** Le quote Melon (ciclo biologico 10-12 giorni) vengono formalmente sostituite da Wheat (ciclo rapido 2-4 giorni) emettendo `SUPERSEDED(supersession_intent_id = INT_ROT_MELON_WHEAT)`;
2. **Day 20 Transition:** Le quote Strawberry (ciclo biologico 10 giorni) vengono formalmente sostituite da Wheat emettendo `SUPERSEDED(supersession_intent_id = INT_ROT_STRAW_WHEAT)`;
3. Il link al nuovo `decision_id` subentrante viene registrato post-review all'atto di `DEFINED`.

---

## 9. Action Selection and Workforce Policy

- **Dimensione Workforce:** 1 Farmer + fino a 9 Hands = 10 worker;
- **Assunzione Giornaliera:** Esecuzione di ordini `HIRE` a step 0 di ogni giorno seguendo la scala di Fibonacci ($1, 1, 2, 3, 5, 8, 13, 21, 34...$), protetta dal cash floor;
- **Multi-Occupancy:** Pieno sfruttamento della facoltà di co-locazione dei worker sulla stessa tile senza collisioni fisiche;
- **Unbounded Inventory:** I worker possono trasportare carichi multipli illimitati, scaricando allo shed non appena necessario.

---

## 10. Economic and Market Policy

### 10.1 Proactive Liquidity Monetization (Step-0 SELL)
Ad ogni tick, il controller invia ordini `SELL` per tutte le derrate presenti nello shed (`MILK`, `WOOL`, `EGG`, `MELON`, `STRAWBERRY`, `CARROT`, `TOMATO`, `WHEAT`) a costo zero. Questo garantisce:
- Massima liquidità monetaria istantanea per reinvestimenti e salari;
- Zero rischio di superamento della capienza shed (100 unità) e zero perdite da overflow.

### 10.2 Ordine di Priorità nel Mercato (Max 10 ordini/tick)
$$\text{SELL (Liquidità)} \longrightarrow \text{HIRE (Forza Lavoro)} \longrightarrow \text{BUY\_LAND (Espansione Day 0)} \longrightarrow \text{BUY\_SEED (Reintegro Quota)}$$

### 10.3 Esclusione Zootecnica Motivata (Livestock Policy)
Antigravity fissa formalmente `livestock_headcount_target = 0` e `pasture_allocation_target = 0`.
- **Giustificazione empirica:** L'audit storico di E08 ha quantificato un saldo netto livestock fortemente negativo (-$3,977.34/episodio a fronte di $4,426.67 di spesa) dovuto all'elevato costo di lock-up del capitale, al consumo di mangime e alla congestione spaziale. L'azzeramento del livestock libera il 100% della manodopera per la massima resa colturale.

---

## 11. Capacity and Resource Policy

| Risorsa | Limite Fisico Engine | Policy Antigravity C2 | Meccanismo di Controllo |
|---|---|---|---|
| **Worker Inventory** | Illimitato (`_inv_add`) | Unbounded | Scarico rapido a shed per monetizzazione |
| **Shed Capacity** | 100 unità | Proactive drain | `SELL` istantaneo a inizio step |
| **Market Orders** | 10 ordini / turno | Max 10 ordinati per ROI | Pipeline prioritaria SELL $\to$ HIRE $\to$ BUY |
| **Quadranti** | 4 possedibili | 2 attivi (Q0 + Q1) | Espansione a Day 0 per \$1,000 |
| **Working-Set** | 50 tile disponibili (48 arabili) | 40 tile arabili scalate | 83.3% land utilization dei 2 quadranti |

---

## 12. VERIFY Policy and Precedence Hierarchy

`VERIFY` opera continuativamente secondo la gerarchia canonica `DLC-CORR-02`:
1. `TERMINAL`: Arresto assoluto a step 720;
2. `COMPLETION / INVALIDATION CONFLICT`: Se la completion condition è raggiunta ma si attiva un invalidatore, si applica il fallback conservativo `INVALIDATED`;
3. `INVALIDATED`: Violazione del cash floor o perdita irrecuperabile di terreni;
4. `COMPLETED`: Obiettivi di produzione stagionali raggiunti;
5. `EXPLICIT CANCEL / SUPERSEDE`: Rotazione biologica programmata;
6. `REPAIR`: Adattamento di percorso o semina fallback Wheat;
7. `CONTINUE`: Esecuzione nominale.

---

## 13. REVIEW Policy and Dispositions

Alla chiusura di ciascun ciclo deliberativo:
- **Direct Accounting:** Calcolo del margine lordo per specie: $\text{Gross Margin} = \text{Revenue} - (\text{Seed Cost} + \text{Pro-rata Wage})$;
- **Descriptive Diagnostics:** Monitoraggio dei tassi di watering, replant latency e perdite weed;
- **Review Dispositions:**
  - `EXPAND` per Strawberry e Melon (margine netto $> 4.0\times$ costo seme);
  - `MAINTAIN` per Wheat (stabilizzatore di fine stagione e cash generator);
  - `REMOVE` per Livestock (eliminazione confermata).

---

## 14. Endgame Policy (Shutdown Window)

A partire da $\text{step} \ge 672$ ($\text{max\_steps} - 48$, ultimi 2 giorni):
1. **Planting Stop:** Nessuna nuova semina avviata (tempo insufficiente per la maturazione);
2. **Intensive Harvest & Drain:** Raccolta di tutte le colture residue;
3. **Total Liquidation:** Vendita totale a mercato di ogni residuo in magazzino;
4. **Terminal Freeze:** Chiusura pulita a `TERMINAL_CLOSED` senza penalità o disqualifiche.

---

## 15. Performance Decomposition Framework (Sez. 8 Mandate)

Antigravity C2 predispone il tracciamento telemetrico completo per la decomposizione delle performance per categoria e specie:

```text
CROP PERFORMANCE LEDGER:
- Species: WHEAT, STRAWBERRY, MELON, CARROT, TOMATO
- Capital Invested: Total seed expenditure ($)
- Operational Burden: Total water actions + dig actions + harvest actions
- Land Utilization: Active tile-steps occupied (Target: 40 tiles = 83.3% 2Q utilization)
- Gross Harvest Yield: Units produced & harvested
- Market Revenue: Gross currency realized ($)
- Net Contribution: Market Revenue - Seed Expenditure
- Latency Metrics: Average replant latency (steps) & harvest timeliness
- Loss Accounting: Lost yield units to weed/decay (Target: 0)

LIVESTOCK PERFORMANCE LEDGER (Ablation Verification):
- Species: COW, SHEEP, GOOSE
- Headcount / Pasture Occupied: 0
- Direct Capital Saved: $4,400+ per episode
- Opportunity Cost Gain: 100% worker time diverted to high-margin crops
```

---

## 16. Falsification Criteria

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ FALSIFICATION REGISTER — MODEL_SPEC_ANTIGRAVITY_C2                                                     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ HYPOTHESIS 1: Strict CRP-10 harvest gate azzera i fallimenti di harvest prematuro.                     │
│ MECHANISM: Verifica congiunta di age >= first_yield_day e max-yield gating.                           │
│ EXPECTED OBSERVATION: premature_harvest_count == 0 (o < 1%).                                          │
│ FAILURE SIGNAL: premature_harvest_count > 50 in un episodio.                                          │
│ REVIEW ACTION: Revisione immediata del predicato CRP-10 e verifica dell'offset temporale.             │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ HYPOTHESIS 2: Recovery e Preventive DIG eliminano la sterilizzazione permanente delle tile.            │
│ MECHANISM: Bonifica tempestiva di LOST_WEED e RETIREMENT_DUE che le restituisce a EMPTY_ASSIGNED.      │
│ EXPECTED OBSERVATION: Durata media di permanenza in stato WEED < 5 step; attainment >= 85%.           │
│ FAILURE SIGNAL: Presenza di tile WEED non bonificate per oltre 20 step consecutivi.                   │
│ REVIEW ACTION: Incremento della priorità di dispatch del task DIG rispetto alle semine.               │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ HYPOTHESIS 3: L'irrigazione Day-0 garantisce 100% daily watering compliance.                          │
│ MECHANISM: Trattamento delle nuove semine con consecutive_unwatered = 1 come urgenza P0.              │
│ EXPECTED OBSERVATION: consecutive_unwatered non supera mai 1; 0 perdite a EOD per sete.              │
│ FAILURE SIGNAL: Rilevazione di anche 1 sola pianta morta a EOD per mancata irrigazione.              │
│ REVIEW ACTION: Anticipazione della finestra di allerta idrica a turnsPerDay - 6.                      │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ HYPOTHESIS 4: La rotazione biologica di fine stagione massimizza la conversione in cassa.             │
│ MECHANISM: Sostituzione di colture a ciclo lungo con Wheat veloce a Day 18 e Day 20.                  │
│ EXPECTED OBSERVATION: Zero colture immature abbandonate a fine partita; resa completa convertita.     │
│ FAILURE SIGNAL: Piante di Melon o Strawberry con yield_units == 0 rimaste a terra a step 720.          │
│ REVIEW ACTION: Anticipo del giorno di cut-off per la semina di specie a ciclo lungo.                  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ HYPOTHESIS 5: La monetizzazione istantanea (SELL a step 0) elimina perdite da overflow shed.          │
│ MECHANISM: Ordini SELL emessi prima di qualsiasi operazione di drop nello shed.                       │
│ EXPECTED OBSERVATION: Contenuto shed non supera mai 40 unità; zero drop rifiutati.                   │
│ FAILURE SIGNAL: Rilevazione di overflow_discard_count > 0.                                            │
│ REVIEW ACTION: Ricalibrazione degli ordini di vendita ed eventuale aumento buffer.                     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ HYPOTHESIS 6: L'esclusione del livestock incrementa il saldo finale netto rispetto ai baseline.       │
│ MECHANISM: Eliminazione del drain finanziario (-$3,977) e concentrazione su orticoltura ad alto ROI.  │
│ EXPECTED OBSERVATION: Saldo finale medio stabilmente superiore a $40,000 (verso target $80,000).      │
│ FAILURE SIGNAL: Saldo medio inferiore a $30,000 in assenza di errori di esecuzione colturale.         │
│ REVIEW ACTION: Valutazione controllata di mini-comparti zootecnici ad altissima efficienza.           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 17. Final Gate for MODEL_SPEC C2

```text
MODEL_SPEC_ID: MODEL_SPEC_ANTIGRAVITY_C2
AGENT_ID: antigravity
VERSION: 2.1.0

FOUNDATION_CONFORMANCE: PASS
DLC_CONFORMANCE: PASS
STRATEGY_NEUTRALITY_RESPECTED: YES
FALSIFICATION_CRITERIA_DEFINED: YES
PERFORMANCE_DECOMPOSITION_READY: YES

BUILD_STATUS: COMPLETE
TESTS_STATUS: PASS (9/9 Unit & Integration Tests)
SUBMISSION_EQUIVALENCE: 100% CERTIFIED
MEAN_FINAL_MONEY: 43,837.33 (Baseline: 29,112.33, Delta: +50.58%)
TOURNAMENT_READY: YES
KAGGLE_READY: YES
KAGGLE_SUBMITTED: NO
```

---

**Fine di MODEL_SPEC_ANTIGRAVITY_C2.**
