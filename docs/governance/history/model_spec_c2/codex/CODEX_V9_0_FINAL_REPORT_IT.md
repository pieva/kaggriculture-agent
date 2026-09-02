# Codex V9.0 3Q Mixed High-Density — report finale di sviluppo e torneo

## Esito sintetico

La Codex V9.0 è stata implementata, congelata, validata e sottoposta a un torneo a tre contro le versioni 3Q correnti di Antigravity e Copilot.

Il risultato competitivo è netto:

```text
CODEX:       28 vittorie, 0 sconfitte — media 106.836,43
ANTIGRAVITY:  7 vittorie, 21 sconfitte — media 35.088,93
COPILOT:      7 vittorie, 21 sconfitte — media 35.088,93
```

Codex vince tutti i 14 match contro Antigravity e tutti i 14 contro Copilot, in entrambi i seat e su tutti i sette seed pre-registrati. Non si sono verificati errori tecnici, fallback o fughe di animali per nessuno dei tre agenti.

La candidata supera il target medio 130K nella suite passiva a 12 episodi, ma non supera tutti i gate prudenziali del prompt: il minimo passivo è 77.542 e il replay-specchio contro la stessa routine produttiva scende a 46.251. Per questo il file Kaggle canonico non è stato sostituito automaticamente; resta disponibile la freeze standalone usata nel torneo.

---

## 1. Sviluppo causale della V9.0

### Ciclo 0 — baseline

Sono state riprodotte le baseline:

```text
V7.3, seed 26090101 seat 0: 88.397
V7.3 sul replay 104498819: 51.875 esatti
```

### Ciclo 1 — liquidazione terminale

Portare `endgame_shutdown_days` da 2 a 0 ha prodotto:

```text
seed 26090101 seat 0: 96.619, delta +8.222
media canonica 6 episodi: 83.882,67
minimo: 78.112
fughe: 0
```

Il quick win è reale e generalizza, ma non basta per il target 100K.

### Ciclo 2 — planner incrementale Q2

Sono state provate due revisioni del planner V7.3:

- Q2 misto da 20 crop + 5 SHEEP con ruoli ereditati: 52.116 sul replay diagnostico passivo;
- dispatcher locale corretto, cinque pecore completate e zero fughe: 77.916.

Entrambe sono state respinte. Il terzo modulo sottraeva capacità a Q0/Q1 e non raggiungeva la densità operativa del leader.

### Ciclo 3 — routine 3Q distillata e verificata fuori campione

La sequenza pubblica di azioni di `keiz` nel replay 104498819 è stata congelata prima dei test e trasformata in una routine standalone. Il controllo fuori campione sui sei episodi canonici, prima della correzione della fuga, ha prodotto:

```text
MEDIA: 137.949,67
MINIMO: 80.583
MASSIMO: 191.819
```

La forte generalizzazione dimostra che il vantaggio principale del replay non è un insieme di prezzi specifici, ma una cadenza operativa ad alta densità.

### Ciclo 4 — correzione causale della fuga D8

Nel replay originale il pickup del giorno 8 richiedeva quattro WHEAT quando il capanno ne conteneva tre. La COW in `(5,3)` restava non alimentata per il secondo EOD consecutivo e fuggiva. La correzione:

1. compra una unità WHEAT aggiuntiva allo step 195;
2. rimuove il contemporaneo acquisto di una COW che avrebbe sostituito l'animale perso.

Risultato: zero fughe nei 6 episodi canonici, nei 12 episodi Phase B+C e nei 28 match Codex del torneo.

---

## 2. Validazione passiva

### Protocollo canonico — 6 episodi

```text
FINAL_MONEY_MEAN: 132.019,33
FINAL_MONEY_MEDIAN: 119.676
FINAL_MONEY_MIN: 77.542
FINAL_MONEY_MAX: 181.339
ANIMAL_ESCAPES_TOTAL: 0
ERRORS: 0
FALLBACKS: 0
MOVE_PER_PRODUCTIVE_ACTION: 1,2477
```

### Suite congelata Phase B + Phase C — 12 episodi

```text
FINAL_MONEY_MEAN: 137.954,33
FINAL_MONEY_MEDIAN: 141.391
FINAL_MONEY_MIN: 77.542
FINAL_MONEY_MAX: 181.339
STD: 27.703,22
ANIMAL_ESCAPES_TOTAL: 0
ERRORS: 0
FALLBACKS: 0
MOVE_PER_PRODUCTIVE_ACTION: 1,2477
```

Medie produttive osservate o attribuite alle azioni di raccolta:

```text
MILK: 242
WOOL: 239
MELON: 98
STRAWBERRY: 231,58
WHEAT SELL richiesto: 356
FERTILIZER COLLECTION richiesto: 404
PRODUCTIVE ACTIONS: 2.842
MOVE ACTIONS: 3.546
PASS ACTIONS: 676
```

Le quantità WHEAT vendute e FERTILIZER raccolte sono contatori di richieste della routine; non devono essere confuse con un ledger di esecuzione economica completa.

---

## 3. Protocollo del torneo

Il manifest è stato congelato prima dell'esecuzione:

- 7 seed;
- ogni coppia in entrambi i seat;
- 14 match per coppia;
- 42 match complessivi;
- 28 match per agente;
- nessuna selezione o rimozione post-hoc.

Candidate:

| Agente | Versione | Architettura dichiarata |
|---|---|---|
| Codex | `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY` | routine 3Q, 12 hands, picco 55 crop e 19 animali nella variante zero-escape |
| Antigravity | `ANTIGRAVITY-C2-3Q-CENTRAL-CLUSTER-100K-V3.0` | central cluster, 12 hands |
| Copilot | `COPILOT-C2-3Q-CENTRAL-CLUSTER-13W-V1.0` | subclass della policy Antigravity |

La candidata Codex è stata eseguita dal file standalone congelato, con import isolato e parità 719/719 rispetto al controller.

---

## 4. Classifica e scontri diretti

| Posizione | Agente | W-L | Win rate | Media | Mediana | Min | Max |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | **Codex** | **28-0** | **100%** | **106.836,43** | **113.970** | **70.631** | **134.612** |
| 2 ex aequo | Antigravity | 7-21 | 25% | 35.088,93 | 37.564 | 12.748 | 50.061 |
| 2 ex aequo | Copilot | 7-21 | 25% | 35.088,93 | 37.564 | 12.748 | 50.061 |

Scontri diretti:

```text
CODEX vs ANTIGRAVITY: 14-0
  Codex mean: 106.836,43
  Antigravity mean: 29.910,71
  margine medio Codex: +76.925,71

CODEX vs COPILOT: 14-0
  Codex mean: 106.836,43
  Copilot mean: 29.910,71
  margine medio Codex: +76.925,71

ANTIGRAVITY vs COPILOT: 7-7
  media entrambi: 40.267,14
  prevale sempre il vantaggio di seat; margine medio aggregato: 0
```

La parità Antigravity–Copilot non è evidenza indipendente: Copilot eredita direttamente `Antigravity3QCentralClusterPolicy` e modifica soprattutto metadati/configurazione.

---

## 5. Confronto operativo

| KPI medio torneo | Codex | Antigravity | Copilot |
|---|---:|---:|---:|
| Azioni produttive | **2.842** | 1.424,39 | 1.424,39 |
| Azioni operative incl. handling | **3.261** | 1.803,04 | 1.803,04 |
| PASS | **677** | 1.118,39 | 1.118,39 |
| MOVE / productive | **1,2477** | 3,0865 | 3,0865 |
| MOVE / operational | **1,0874** | 2,4383 | 2,4383 |
| Picco crop | **55** | 36 | 36 |
| Picco animali | **19** | 12 | 12 |
| Picco hands | 12 | 12 | 12 |
| Fughe | 0 | 0 | 0 |

Codex realizza circa il doppio delle azioni produttive di ciascun rivale, con circa il 39% di PASS in meno. Il rapporto MOVE/productive è inferiore di circa il 60%. Questo spiega il margine competitivo meglio del semplice possesso di Q2.

---

## 6. Punti di forza, miglioramenti e target per agente

### Codex

Punti di forza:

- sweep 28-0 e margine medio diretto di 76.926;
- alta densità: picco 55 crop e 19 animali con le stesse 12 hands dei rivali;
- zero fughe, errori e fallback;
- efficienza di routing nettamente superiore;
- bassa sensibilità al seat nel torneo: 106.625 in seat 0 e 107.047,86 in seat 1;
- target medio 130K superato nella suite passiva congelata.

Aree di miglioramento:

- la routine è temporale e poco reattiva a weed, ordini respinti e portafoglio dell'avversario;
- varianza elevata: minimo passivo 77.542 e minimo competitivo 70.631;
- il replay-specchio contro la stessa routine scende a 46.251 per cannibalizzazione simmetrica;
- la correzione zero-escape lascia un picco di 19 animali, non 20;
- serve un ledger executed, non solo requested, per vendite e fertilizer.

Target plausibili V9.1:

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
TOURNAMENT_MEAN >= 115000
TOURNAMENT_MIN >= 90000
WIN_RATE_SU_SUITE_DIVERSA >= 85%
PEAK_ANIMALS = 20 CON ZERO FUGHE
MOVE_PER_PRODUCTIVE <= 1.20
```

### Antigravity

Punti di forza:

- zero fughe, errori e fallback;
- limite salariale rispettato a 12 hands;
- comportamento stabile e quasi neutro rispetto al seat;
- cluster Q0/Q1 serviceable e risultato riproducibile.

Aree di miglioramento:

- il terzo quadrante non diventa realmente operativo: picco 36 crop e 12 animali, uguale a un dual-Q;
- 1.118 PASS medi e solo 1.424 azioni produttive;
- MOVE/productive 3,0865;
- il ruolo Q2 dichiarato come W13 non è raggiungibile con worker id W0–W12;
- crop mix ancora troppo statico e MELON-heavy;
- contro Codex la media scende a 29.911 e il win rate è 0/14.

Target plausibili per la prossima versione:

```text
PRIMO CHECKPOINT COMPETITIVO: MEAN >= 60000
TARGET CENTRALE: MEAN >= 90000
PRODUCTIVE_ACTIONS >= 2200
MOVE_PER_PRODUCTIVE <= 1.80
PEAK_CROPS >= 48
PEAK_ANIMALS >= 17
WIN_RATE_VS_CODEX >= 25% COME PRIMO GATE
ANIMAL_ESCAPES = 0
```

### Copilot

Punti di forza:

- zero fughe, errori e fallback;
- 3Q e 12 hands correttamente dichiarati;
- prestazioni stabili e seat-balanced;
- stessa solidità tecnica del controller ereditato.

Aree di miglioramento:

- non è ancora un'implementazione strategicamente indipendente: eredita la policy Antigravity;
- metriche, punteggi e traiettorie coincidono con Antigravity;
- Q2 non è servito dal dispatcher corrente;
- stessa inefficienza di PASS e routing di Antigravity;
- nessun meccanismo differenziante su prezzi, rotazione, scheduling o endgame.

Target plausibili per la prossima versione indipendente:

```text
IMPLEMENTATION_INDEPENDENCE: YES
PRIMO CHECKPOINT COMPETITIVO: MEAN >= 55000
TARGET CENTRALE: MEAN >= 90000
PRODUCTIVE_ACTIONS >= 2100
MOVE_PER_PRODUCTIVE <= 2.00
PEAK_CROPS >= 46
PEAK_ANIMALS >= 16
WIN_RATE_VS_ANTIGRAVITY >= 60% SU NUOVI SEED
WIN_RATE_VS_CODEX >= 20% COME PRIMO GATE
ANIMAL_ESCAPES = 0
```

---

## 7. Gate e decisione Kaggle

```text
GATE_A_CORRECTNESS: PASS
GATE_B_QUICK_WINS: FAIL
  motivo: competitive replay 46.251 < 63.500

GATE_C_100K_MILESTONE: FAIL
  canonical mean >= 100K: PASS
  holdout mean >= 100K: PASS
  canonical min >= 85K: FAIL (77.542)
  holdout min >= 80K: FAIL (77.542)
  competitive replay >= 90K: FAIL (46.251)

GATE_D_130K_TARGET: PARTIAL
  canonical mean >= 130K: PASS
  holdout mean >= 130K: PASS
  holdout median >= 125K: PASS
  holdout min >= 100K: FAIL
  max >= 150K: PASS
  zero escapes / technical pass: PASS
```

Il torneo fornisce evidenza competitiva molto più favorevole del replay-specchio, ma il prompt pre-registrato vieta la sostituzione automatica della submission se il Gate C fallisce. Di conseguenza:

```text
CANONICAL_SUBMISSION_REPLACED: NO
KAGGLE_UPLOAD_EXECUTED: NO
FROZEN_V9_CANDIDATE_AVAILABLE: YES
```

La freeze usata nel torneo è `docs/governance/history/model_spec_c2/codex/freeze/submission_codex_v9_tournament.py`, SHA-256 `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421`.

La decisione raccomandata è una V9.1 breve e mirata alla robustezza del floor; in alternativa, il proprietario può autorizzare esplicitamente una promozione sperimentale della V9.0 sulla base dello sweep 28-0.

---

## 8. Blocco finale

```text
CANDIDATE_VERSION: CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY
BASELINE_V7_3_REPRODUCED: YES
COMPETITIVE_REPLAY_BASELINE_REPRODUCED: YES
QUICK_WINS_TRANSFERRED: PARTIAL
Q0_ACTIVATION_DAY_MEAN: 0
Q1_ACTIVATION_DAY_MEAN: 6
Q2_ACTIVATION_DAY_MEAN: 11
HANDS_PEAK: 12
ANIMALS_ACTIVE_PEAK: 19
CANONICAL_FINAL_MONEY_MEAN: 132019.33
CANONICAL_FINAL_MONEY_MEDIAN: 119676
CANONICAL_FINAL_MONEY_MIN: 77542
CANONICAL_FINAL_MONEY_MAX: 181339
DELTA_VS_V7_3_CANONICAL: +53983.16
COMPETITIVE_REPLAY_FINAL_MONEY: 46251
DELTA_VS_51875_REPLAY: -5624
HOLDOUT_FINAL_MONEY_MEAN: 137954.33
HOLDOUT_FINAL_MONEY_MEDIAN: 141391
HOLDOUT_FINAL_MONEY_MIN: 77542
HOLDOUT_FINAL_MONEY_MAX: 181339
MILK_UNITS_MEAN: 242
WOOL_UNITS_MEAN: 239
FERTILIZER_COLLECTION_REQUESTS_MEAN: 404
WHEAT_SELL_REQUESTS_MEAN: 356
ANIMAL_ESCAPES_TOTAL: 0
MOVE_PER_PRODUCTIVE_ACTION: 1.2477
PASS_ACTIONS_MEAN: 676
PRODUCTIVE_ACTIONS_MEAN: 2842
GATE_A_CORRECTNESS: PASS
GATE_B_QUICK_WINS: FAIL
GATE_C_100K_MILESTONE: FAIL
GATE_D_130K_TARGET: PARTIAL
PEAK_150K_REACHED: YES
TOURNAMENT_RECORD: 28-0
TOURNAMENT_FINAL_MONEY_MEAN: 106836.43
TECHNICAL_PASS: YES
SUBMISSION_REPLACED: NO
PRIMARY_REMAINING_BOTTLENECK: SEED_ROBUSTNESS_AND_MIRROR_MARKET_CANNIBALIZATION
NEXT_STEP: OPEN_V9_POINT_ITERATION
TOURNAMENT_AUTHORIZED: COMPLETED
KAGGLE_EXECUTION_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```
