# ANTIGRAVITY C2 â€” PERIODIC MODEL REVIEW
## Da Architettura a Soglie Reattive a Modello a Periodi e Piani Biologici

```text
AGENT_ID: ANTIGRAVITY
REVIEW_PHASE: C2 PERIODIC MODEL REVIEW
STATUS: COMPLETE â€” PERIODIC EVOLUTION RECOMMENDED
EVIDENCE_BASE: 4 Kaggle Benchmark Replays (103484828, 103473619, 103462357, 103464592)
```

---

## 1. Executive Summary & Verdetto

L'audit forense comparativo tra la policy **Antigravity C2** ($27.565,17 di media nel tournament locale) e i quattro benchmark replay ad alte prestazioni su Kaggle (**LuCcc** $56.772 a 1Q, **Gordeev** $88.648 a 3Q, **Dipin** $95.496 a 3Q, **ÐŸÐµÑ‚Ð°Ñ€** $95.475 a 4Q) dimostra in modo inequivocabile che:

1. **Il modello puramente threshold-centric / reactive Ã¨ strutturalmente sub-ottimale:**
   Le decisioni basate esclusivamente su soglie di cassa, slot vuoti istantanei e yield terminali generano burst impulsivi (`SERVICE_PEAK`), bloccano la liquiditÃ  nei primi 10 giorni, saturano la forza lavoro con picchi di irrigazione non scalati e impediscono flussi di cassa giornalieri continui.
2. **I top performer operano secondo una chiara separazione:**
   $$\text{BASE POLICY} = \text{PLAN (Calendari Biologici + Servizio Periodico)}$$
   $$\text{MARKET \& ANOMALIES} = \text{REACT (LiquiditÃ  + Timing Ordini + Deviazioni)}$$
3. **Il ruolo causale del Livestock (Cows + Sheep):**
   Il bestiame non Ã¨ un'alternativa alle colture ma un **generatore di liquiditÃ  periodica quotidiana** ($500â€“$1.500/giorno da Milk e Wool) che finanzia costantemente i salari ($88â€“$150/giorno) e produce **Fertilizer**, dimezzando i tempi di maturazione delle colture.
4. **Il principio LuCcc (Massima densitÃ  su 1Q):**
   LuCcc dimostra che la perfetta sincronizzazione periodica di 6 pasture (3 Cow + 3 Sheep) e 18 crop tile con 6 worker fissi su un singolo quadrante genera **$56.772** con zero costi di espansione e tempo di spostamento (MOVE) inferiore al 15%.
5. **Espansione come Replica Controllata di Cicli:**
   L'espansione a 2Q/3Q/4Q (Dipin $95.5k, Petar $95.5k) ha successo solo quando replica un modulo periodico autosufficiente con adeguamento proporzionale della workforce.

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
```

---

## A. Evidenza Osservata sui Quattro Replay Benchmark

### Quadro Comparativo Generale

| Parametro / Metrica | LuCcc (`103484828`) | Gordeev (`103473619`) | Dipin (`103462357`) | ÐŸÐµÑ‚Ð°Ñ€ (`103464592`) | Antigravity C2 (Attuale) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Score Finale** | **$56.772,00** | **$88.648,00** | **$95.496,00** | **$95.475,00** | **$27.565,17** |
| **Quadranti Finali** | **1 (NW)** | **3 (NW, NE, SW)** | **3 (NW, NE, SW)** | **4 (NW, NE, SW, SE)** | **2 (NW, NE)** |
| **Workforce (Hands)** | **6 fisse (Day 0-29)** | **12 (Day 1-29)** | **12 (Day 1-29)** | **12â€“18 (scalati)** | **9 fisse** |
| **Pasture / Bestiame** | **6 tile: 3 Cow, 3 Sheep** | **11 tile: 6 Cow, 4 Sheep** | **12 tile: 8 Cow, 4 Sheep** | **22 tile: 22 Sheep** | **0 (Solo colture)** |
| **Daily Routine Livestock** | **6 Feed + 6 Care / giorno** | **10 Feed + 10 Care / giorno** | **12 Feed + 12 Care / giorno** | **22 Feed + 22 Care / giorno** | **Nessuna** |
| **Fertilizer Generato/Usato** | **22 venduti + applicato** | **138 venduti + applicato** | **173 venduti + applicato** | **330 venduti + applicato** | **0** |
| **Crop Mix Primario** | **Melon (21), Strawberry (16), Wheat (8)** | **Wheat (163), Strawberry (40), Melon (18)** | **Wheat (112), Strawberry (32), Melon (20)** | **Wheat (104), Melon (12), Strawberry (6)** | **Strawberry (45%), Melon (35%), Wheat (20%)** |
| **Planting Pattern** | **Staggered wave (D7, D9, D19, D24)** | **Continuous wheat (3-8/d) + wave** | **Continuous wheat + Strawberry D11** | **Continuous wheat + Sheep feed** | **Burst su slot aperti (D0 rush)** |
| **Monetizzazione** | **Giornaliera (Milk, Wool, Fert, Melon)** | **Giornaliera (Milk, Wool, Fert, Wheat)** | **Giornaliera (Milk, Wool, Fert, Strawb)** | **Giornaliera (Wool, Fert, Wheat)** | **Batch finale (D10-12, D20-24)** |
| **Quota MOVE su Totale** | **< 15% (altissima densitÃ )** | **28%** | **26%** | **34%** | **48%** |

---

### A.1 Analisi Dettagliata Replay LuCcc (`103484828` â€” Score: $56.772)

- **Architettura Produttiva:** 1 Quadrante compatto (NW). Layout a 24 tile: 6 Pasture adiacenti allo shed `[(1,4), (2,4), (3,3), (3,4), (4,2), (4,3)]` e 18 Crop tile.
- **Livestock Routine:**
  - Day 0: Acquisto 2 Cow + 2 Sheep.
  - Day 7: Acquisto 1 Cow + 1 Sheep (capacitÃ  totale 3 Cow + 3 Sheep).
  - Ogni giorno (Day 0-29): esattamente 6 `FEED` e 6 `CARE`.
  - Raccolta automatica e regolare di `MILK` ($120/unitÃ ) e `WOOL` ($150/unitÃ ).
  - Raccolta e applicazione di `FERTILIZER` che accelera le colture adiacenti.
- **PeriodicitÃ  delle Colture:**
  - Non semina tutto a Day 0. Attende l'attivazione del bestiame e poi semina a onde coordinate: Day 7 (10 Melon, 3 Strawberry), Day 9 (5 Strawberry), Day 19-20 (replant 11 Melon).
  - Raccolta di massa Melon a Day 20: 60 unitÃ  vendute in un solo blocco per un incasso immediato di **$3.600+**.
- **Flusso Finanziario:**
  - Nessun blocco di liquiditÃ . Il bestiame fornisce un cash flow giornaliero di $400â€“$800, consentendo di assumere 6 worker ogni giorno ($88/giorno) e comprare semi/mangimi senza mai toccare il cash floor.

---

### A.2 Analisi Dettagliata Replay Gordeev (`103473619` â€” Score: $88.648)

- **Architettura Produttiva:** 3 Quadranti (NW, NE, SW).
- **Workforce:** 12 worker assunti fin dal Day 1.
- **Livestock Routine:**
  - 11 Pasture: 6 Cow + 4 Sheep.
  - Genera 170 Milk, 74 Wool, 138 Fertilizer venduti a mercato, oltre a fertilizzare costantemente il perimetro di colture ad alto valore.
- **PeriodicitÃ  delle Colture:**
  - Wheat continuo scaglionato (3â€“10 unitÃ  piantate al giorno), che garantisce mangime interno e turnover rapido.
  - Strawberry a Day 3, 6, 8, 11, 12, 17 con raccolta continuativa pluriennale.
  - Melon a Day 0 (8 unitÃ ), Day 5 (3 unitÃ ), Day 8 (2 unitÃ ), Day 10 (3 unitÃ ) scaglionati in modo da non creare un unico picco di servizio.

---

### A.3 Analisi Dettagliata Replay Dipin (`103462357` â€” Score: $95.496)

- **Architettura Produttiva:** 3 Quadranti (NW, NE, SW).
- **Flusso Produttivo Ibrido Perfetto:**
  - 12 Pasture: 8 Cow + 4 Sheep.
  - Produzione totale venduta: 201 Milk, 114 Wool, 173 Fertilizer, 180 Strawberry, 109 Melon, 447 Wheat.
  - Totale ordini di vendita a mercato: 243 `SELL` (vendite giornaliere a lotti di 3â€“15 unitÃ  non appena disponibili nello shed).
- **PeriodicitÃ :**
  - Day 0â€“10: Wheat + Bestiame generano una cassa di oltre $15.000.
  - Day 11: Espansione e semina massiva di 13 Strawberry + 10 Melon quando la cassa e la forza lavoro (12 worker) sono pienamente a regime.
  - Risultato: Nessun deperimento (`LOST_WEED` = 0, deadline miss = 0%).

---

### A.4 Analisi Dettagliata Replay ÐŸÐµÑ‚Ð°Ñ€ (`103464592` â€” Score: $95.475)

- **Architettura Produttiva:** 4 Quadranti (Full Board).
- **Specializzazione Estrema su Sheep + Wheat:**
  - 22 Pasture: 22 Sheep.
  - 377 Wool vendute ($150/unitÃ  $\implies$ **$56.550** solo da Wool!).
  - 330 Fertilizer venduti ($40/unitÃ  $\implies$ **$13.200** solo da Fertilizer!).
  - Wheat continuo (104 plant) per autosufficienza mangimi.
  - Workforce scalata progressivamente fino a 18 worker a fine partita per gestire 22 pasture e le crop su 4 quadranti.

---

## B. Diagnosi del Modello Corrente (Antigravity C2)

L'analisi dell'attuale implementazione Antigravity C2 rivela 4 patologie causali:

```text
PATOLOGIA 1: ZERO-LIVESTOCK BIAS
Diagnosi: Antigravity C2 ha target_cows=0, target_sheep=0, pasture_target=0.
Effetto Causal: Zero entrate nei giorni 0-10. Tutta la cassa iniziale ($3.000) viene spesa
in Land ($2.000) e semi ($800), lasciando l'agente a ridosso del cash floor ($50).
I salari giornalieri consumano la cassa residua, impedendo flessibilitÃ .

PATOLOGIA 2: BURST PLANTING E PICCO DI SERVIZIO NON SCAGLIONATO
Diagnosi: L'allocazione a slot aperti pianta 24 crop tutte a Day 0.
Effetto Causal: 24 colture richiedono 24 WATER al giorno per 10 giorni consecutivi.
A Day 10-12, 24 colture diventano mature contemporaneamente. I worker devono scegliere
tra WATER, HARVEST e SELL, creando saturazione e inefficienza di routing.

PATOLOGIA 3: HARVEST GATING RIGIDO BASATO SU MAX_YIELD SENZA LIFESPAN AWARENESS
Diagnosi: L'agente attende rigidamente yield=6 prima di raccogliere.
Effetto Causal: Se una pianta subisce 1 giorno di mancata irrigazione, non raggiungerÃ  mai yield=6
prima del lifespan step (decay), rimanendo bloccata senza essere raccolta nÃ© liberata.

PATOLOGIA 4: REATTIVITÃ€ AD HOC SUL MERCATO (ASSENZA DI CALENDARIO DI MONETIZZAZIONE)
Diagnosi: Le vendite avvengono solo quando lo shed Ã¨ pieno o a fine giornata.
Effetto Causal: Mancanza di liquiditÃ  tempestiva per assumere il massimo della forza lavoro.
```

---

## C. Proposta Architetturale: Da Soglie a Piani + ReattivitÃ

Classificazione di tutti i meccanismi decisionali:

| Meccanismo | Tipo Attuale | Nuova Classificazione | Razionale Architetturale |
|---|:---:|:---:|---|
| **Livestock Placement & Sizing** | Threshold (`cash >= 400`) | **PLAN** | 4-6 Pasture attorno allo shed pianificate a Day 0; acquisto 2 Cow + 2 Sheep a Day 0; espansione programmata a Day 6. |
| **Daily Feeding & Care** | Assente | **PLAN** | Task giornaliera fissa all'ora 0-2 per tutti gli animali attivi (prioritÃ  massima). |
| **Planting Schedule & Quotas** | Threshold (slot aperti) | **PLAN** | Staggered planting calendar: max 2-3 Wheat/giorno; Melon/Strawberry pianificati a onde Day 0 (Wave 1) e Day 10 (Wave 2). |
| **Daily Watering Dispatch** | Threshold (`watered_today == False`) | **PLAN** | Orario di servizio programmato per coorte; saturazione giornaliera limitata al budget worker disponibile. |
| **Harvest Window & Deadlines** | Threshold (`yield == max_yield`) | **HYBRID** | Plan di raccolta alla finestra biologica economica (Day 4 per Wheat, Day 10 per Melon/Strawb) con fallback reattivo anti-decay prima del lifespan step. |
| **Workforce Hiring** | Threshold (`cash >= floor + cost`) | **PLAN** | Assunzione programmata fissa di 6-8 worker a Day 0-29 garantita dal cash flow degli animali. |
| **Land Expansion** | Threshold (`active >= 20 and cash >= 2000`) | **HYBRID** | Espansione pianificata non prima di Day 10, solo quando il ciclo Q1 Ã¨ autosufficiente e ha generato >$5.000 di surplus. |
| **Selling & Cash Management** | Threshold (fine giornata) | **REACT** | Vendita immediata ad ogni passaggio nello shed se quantitÃ  > 0 (costo zero) per massimizzare la cassa liquida. |
| **Recovery & Preventive DIG** | Threshold (lost weed) | **REACT** | Gestione delle eccezioni (weed accidentale o pianta deperita). |

---

## D. Ipotesi Causale Preregistrata

```text
HYPOTHESIS_ID: HYP-AGY-PERIODIC-01

OBSERVED_PROBLEM:
Antigravity C2 genera $27.5k di media perchÃ© opera senza bestiame (zero entrate nei giorni 0-10),
subisce un burst iniziale di 24 colture sincronizzate che saturano la capacitÃ  di servizio e spende
$2.000 di espansione terreno precoce senza avere la liquiditÃ  e i worker per saturarla con profitto.
I benchmark a paritÃ  o maggiore scala estraggono $56k-$95k grazie a livestock integrato e cicli periodici.

EVIDENCE:
- LuCcc (103484828): 1Q compatto, 3 Cow + 3 Sheep, 6 worker fissi, 18 crop tile a onde => $56.772.
- Dipin (103462357): 3Q, 8 Cow + 4 Sheep, 12 worker, Wheat continuo + Melon/Strawb periodici => $95.496.
- Petar (103464592): 4Q, 22 Sheep, 377 Wool + 330 Fertilizer => $95.475.
- Antigravity Tournament C2: $27.565, 0 animali, 0 fertilizer, 48% movement share.

CAUSAL_MECHANISM:
L'integrazione di un nucleo di livestock (Cow/Sheep) attorno allo shed genera $500-$1.200 di liquiditÃ
giornaliera costante e Fertilizer, eliminando i colli di bottiglia finanziari e accelerando le colture.
Lo scaglionamento temporale (staggering) delle colture linearizza il carico di irrigazione/raccolta,
mentre la densitÃ  logistica riduce il MOVE share dal 48% a <25%, aumentando le azioni produttive per worker.

MODEL_CHANGE:
1. Adottare la separazione strutturale BASE POLICY = PLAN (cicli biologici e calendari) + REACT (mercato ed eccezioni).
2. Introdurre il modulo Livestock a Day 0: 4-6 Pasture adiacenti allo shed con mix Cow (Milk $120) e Sheep (Wool $150 + Fertilizer).
3. Sostituire il burst planting Day 0 con un calendario a onde e wheat continuo scaglionato (max 2-3/giorno).
4. Sincronizzare la raccolta alla finestra economica e alla scadenza di decay anzichÃ© alla sola soglia di resa massima.
5. Pianificare l'espansione territoriale come replica controllata solo dopo la stabilizzazione del ciclo primario (Day 10+).

EXPECTED_INTERMEDIATE_EFFECT:
- Cash flow giornaliero positivo a partire da Day 1 ($300-$800/giorno).
- 100% compliance giornaliera di Feed + Care.
- Generazione e uso di Fertilizer (>50 unitÃ /partita).
- Riduzione della quota di movimento (MOVE share < 25%).
- Zero deadline miss e zero decay loss sulle colture mature.

EXPECTED_ECONOMIC_EFFECT:
- Final Money medio atteso > $45.000 in configurazione 1Q (stile LuCcc).
- Final Money medio atteso > $70.000 in configurazione multi-Q replicata (stile Dipin/Gordeev).

FALSIFICATION_CONDITION:
L'ipotesi Ã¨ falsificata se l'integrazione di Cow/Sheep riduce il saldo netto (costo mangime/acquisto > ricavi latte/lana),
se i worker non riescono a completare FEED+CARE+WATER nello stesso giorno, o se lo staggering riduce la monetizzazione
complessiva rispetto al burst planting.
```

---

## E. Period Model: Specificazione dei Cicli Biologici e di Servizio

```text
================================================================================
ENTITY_PERIOD_MODEL (Specificazione Canonica)
================================================================================

1. COW (Bovino da Latte)
   - Costo acquisto: $400
   - Slot: 1 Pasture adiacente allo shed (distanza Manhattan 1-2)
   - Ciclo giornaliero:
     * Ora 0-2: FEED (consuma 1 Wheat dalla tasca o shed)
     * Ora 0-3: CARE (richiede worker sul pasture)
   - Output: 1 Milk ($120) ogni giorno + Fertilizer potenziale
   - Finestra di servizio: Giornaliera (entro ora 23)
   - Margine netto: $120 ricavo - $10 mangime = +$110/giorno per capo.

2. SHEEP (Ovino da Lana e Fertilizzante)
   - Costo acquisto: $500
   - Slot: 1 Pasture adiacente allo shed
   - Ciclo giornaliero:
     * Ora 0-2: FEED (1 Wheat)
     * Ora 0-3: CARE
   - Output: 1 Wool ($150) ogni 2 giorni + 1 Fertilizer ($40) quasi quotidiano
   - Margine netto: ($150/2 + $40) - $10 = +$105/giorno per capo.

3. WHEAT (Coltura Continua di Supporto & Mangime)
   - Costo seme: $10
   - Semina: Scaglionata (2-3 tile/giorno)
   - Irrigazione: Giornaliera per 2-4 giorni
   - Finestra di raccolta: Day 2 (yield 2) a Day 4 (yield 6)
   - Utilizzo: 50% mangime interno (zero acquisti a mercato a prezzo gonfiato), 50% vendita ($25/unitÃ ).

4. MELON (Coltura Cash di Massa)
   - Costo seme: $80
   - Semina: A onde (Wave 1: Day 0-1, Wave 2: Day 12-14)
   - Irrigazione: Giornaliera per 10-12 giorni (accelerata con Fertilizer a 8-10 giorni)
   - Finestra di raccolta: Day 10 a Day 12 (Hard deadline pre-decay: Day 13)
   - Output: 6 unitÃ  * $60 = $360 per tile (ROI 450%).

5. STRAWBERRY (Coltura da Rendita Continuativa)
   - Costo seme: $100
   - Semina: Day 0 (Wave 1)
   - Irrigazione: Giornaliera fino a Day 10, poi ogni 2 giorni
   - Raccolta: Day 10, Day 12, Day 14, Day 16, Day 18, Day 20, Day 22, Day 24, Day 26, Day 28 (10 raccolti!)
   - Output: 4 unitÃ  * $40 * 10 = $1.600 per tile (ROI 1600%).
```

---

## F. Modello di Espansione: Replica Modulare Controllata

L'espansione non deve essere una decisione ad-hoc basata sul solo saldo di cassa, ma una **replica temporale di un modulo operativo standard**:

```text
MODULO BASE Q1 (Saturazione ad Alta DensitÃ  â€” Stile LuCcc):
- 6 Pasture adiacenti allo shed (3 Cow, 3 Sheep)
- 18 Crop Tile (4 Wheat continuo, 8 Melon, 6 Strawberry)
- 6 Worker dedicati (2 Livestock/Feed/Care, 3 Water/Harvest, 1 Logistics/Fertilize)
- Rendimento stimato: $50.000 - $60.000

REPLICA MODULO Q2 (Espansione a Nord-Est â€” Stile Gordeev/Dipin):
- Condizione di attivazione: Day >= 10, Cassa >= $4.000, Q1 a regime
- Azione: BUY_LAND (NE) + HIRE fino a 12 worker
- Layout NE: 4 Pasture supplementari (2 Cow, 2 Sheep) + 20 Crop Tile
- Rendimento incrementale stimato: +$30.000 - $40.000

TOTALE ATTESO A 2Q/3Q: $80.000 - $95.000
```

---

## Conclusione della Review

- **Verdetto:** `PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES`
- **Direttiva:** Questa review chiude la fase di analisi. Il MODEL_SPEC di Antigravity viene arricchito con la formalizzazione della periodicitÃ  e del modulo Livestock, pronto per guidare la successiva pianificazione ed evoluzione senza alterare prematuramente il codice congelato.

---

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
ANALYSIS_REPLAYS_COUNT: 4
PRIMARY_BENCHMARK_SCORE: 95496.0 (Dipin) / 56772.0 (LuCcc 1Q)
CORE_ARCHITECTURE: PLAN_DRIVEN_BIOLOGICAL_PERIODS + REACTIVE_MARKET_OVERRIDE
MODEL_SPEC_READY_FOR_NEXT_CYCLE: YES
KAGGLE_RUN: NO
```
