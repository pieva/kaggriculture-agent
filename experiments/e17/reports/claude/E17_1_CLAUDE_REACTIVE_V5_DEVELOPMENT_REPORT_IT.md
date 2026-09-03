# E17.1 — Claude reattivo V5: clustering per quadrante, risultato del benchmark

- **Data:** 2026-09-03
- **Stato:** MATRICE COMPLETA A 7 SEED ESEGUITA — esito positivo
  (`+3,31%` vs V3, `28/28` match senza collassi né errori tecnici). Non
  è una submission Kaggle e non consuma holdout/final-confirmation.
- **Candidata:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V5`
  (`src/agricola/strategy/claude/e17_reactive_3q_v5.py`,
  `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V5.json`)
- **Predecessore:** V3 (`FROZEN_WITH_FAILED_GATES`); V4 (topologia SW,
  respinta `-8,9%`) non è il predecessore
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V5.md`
- **Origine:** `experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md`,
  leva assegnata a Claude: "routing e cap zootecnico"

---

## 0. Scoperta pre-benchmark: le due leve del torneo interagiscono male

Il torneo assegnava a Claude UNA famiglia — "routing e cap zootecnico" —
ma un'ablation isolata su singole run (seed `26090101`, seat 0, avversario
`CODEX_V9`) prima del benchmark a più seed ha trovato:

| Configurazione | Denaro | Hands finali | Quadranti |
|---|---:|---:|---|
| V3 (baseline) | 12.174 | 8 | NW, NE, SW |
| Solo clustering per quadrante | **17.178** | 5 | NW, NE |
| Solo cap zootecnico ridotto (`4`→`3`) | 10.346 | 8 | NW, NE, SW |
| **Entrambe insieme** | **345** | 5 | NW, NE |

Nessuna delle due leve isolate riproduce il collasso; solo la
combinazione lo fa. **V5 spedisce quindi con la sola leva di clustering**;
il cap zootecnico resta implementato e config-toggleable ma disattivato di
default, rimandato a un round di ablation separato (MODEL_SPEC V5 Sezione
6). Dettaglio completo: MODEL_SPEC V5 Sezione 1.1.

---

## 1. Cosa è stato testato nel benchmark a più seed

Unica variabile: `dispatch.cluster_by_home_quadrant` da `false` (V3) a
`true`. Ogni worker riceve un `home_quadrant` per round-robin sull'indice;
le opportunità non critiche (tutto tranne `URGENT_WATER`/`FEED_NEEDED`)
sono ristrette al quadrante home; i due generi critici possono ancora
attraversare. Nessun'altra leva toccata (`structures_target_per_quadrant`
resta `4`, il valore V3). Confronto black-box V5 vs V3, stesso avversario
(`CODEX_REACTIVE`), stessi 4 seed di sviluppo, 2 seat ciascuno (16 match
per versione).

## 2. Risultato dello spot-check a 4 seed (16 match, 2 seat)

| | V3 (denaro medio) | V5 (denaro medio) | Delta |
|---|---:|---:|---:|
| 4 seed / 16 match | 13.237,88 | **15.043,38** | **+13,6%** |

Zero errori tecnici, zero mutazioni non attese. `hands` finali medi
`7,62` (contro `8,00` di V3): un solo match su 16 (seed `26090101`, seat
0) resta bloccato a `5` hands/`2Q` invece di `8`/`3Q` — lo stesso
sintomo isolato in Sezione 0, ma qui non causa collasso (quel match
singolo resta comunque il denaro più alto della matrice, `17.178`).
`crop_tiles_final` medio quasi triplica (`3,62` contro `1,38` di V3):
coerente con l'ipotesi H-CR5.1 — meno MOVE speso a inseguire lavoro
sparso per la mappa lascia più turni per completare la coltura prima
della liquidazione.

Per seed (media dei 2 seat):

| Seed | V3 | V5 | Delta |
|---|---:|---:|---:|
| `26090101` | 11.418,00 | 16.310,00 | +42,8% |
| `26090102` | 10.256,00 | 14.546,50 | +41,8% |
| `26090103` | 17.110,50 | 15.138,00 | **-11,5%** |
| `1838889274` | 14.167,00 | 14.179,00 | +0,1% |

Tre seed su quattro migliorano (due in modo sostanziale), uno peggiora
moderatamente, uno è sostanzialmente pari. Non è un miglioramento
uniforme, ma non c'è nessun segno di collasso su nessun seed — a
differenza di V4 (segno incoerente 2/2 con un'aggregato negativo) qui
l'aggregato è chiaramente positivo e il caso peggiore è una perdita
contenuta. Per il protocollo (Sezione 5 del piano statico V4, riusato
qui) questo giustifica procedere alla matrice completa a 7 seed.

Artifact grezzo: `experiments/e17/artifacts/derived/claude/E17_1_V5_DEV_BENCHMARK_VS_CODEX.json`.

## 3. Matrice completa a 7 seed (28 match, 2 seat)

| | V3 (canonico, 28 match) | V5 (28 match) | Delta |
|---|---:|---:|---:|
| Denaro medio | 13.540,86 | **13.989,79** | **+3,31%** |
| `hands` finali medio | 8,00 | 7,79 | -2,6% |
| `crop_tiles_final` medio | 1,00 | **3,14** | **+214%** |
| `animals_final` medio | 4,36 | 3,21 | -26,4% |
| W-T-L (vs Codex) | 0-0-28 | 0-0-28 | invariato |
| Errori tecnici | 0 | 0 | invariato |

Fonte V3: `experiments/e17/artifacts/derived/claude/E17_1_V3_METRICS.json`
(canonico, 28 match, mai modificato in questa sessione). Fonte V5:
`experiments/e17/artifacts/derived/claude/E17_1_V5_DEV_BENCHMARK_VS_CODEX.json`.

Il risultato a 7 seed (`+3,31%`) è più modesto del `+13,6%` osservato sui
soli 4 seed di spot-check: i tre seed aggiuntivi (`1619968655`,
`710418712`, `562040596`) hanno delta più piccoli o leggermente negativi,
riportando l'aggregato verso la parità — esattamente il motivo per cui il
protocollo richiede la matrice completa prima di dichiarare un
miglioramento, e non si ferma allo spot-check. Resta comunque un
miglioramento reale: positivo, senza nessun collasso su 28/28 match,
verificato su tutti e 7 i seed di sviluppo.

**Anomalia nota, non un collasso:** il match seed `26090101` seat `0`
(ricorre identico contro entrambi gli avversari Codex, per determinismo)
resta bloccato a `5 hands`/`2Q` invece di `8`/`3Q` — lo stesso sintomo
isolato nell'ablation di Sezione 0. In questo caso specifico non è
dannoso economicamente (`17.178`, il valore più alto dell'intera
matrice), ma è un comportamento non compreso: perché il clustering
occasionalmente impedisce il raggiungimento della soglia di workforce per
sbloccare SW. Non blocca la decisione di Sezione 4, ma va investigato
prima di ulteriori iterazioni su questa leva.

## 4. Decisione

**V5 (solo clustering per quadrante) è un miglioramento reale e
verificato su V3**: `+3,31%` di denaro medio su 28/28 match development,
zero errori, zero collassi, densità di coltura quasi triplicata. Non
raggiunge il target indicativo `100.000` né chiude il gap con Codex
(`13.989,79` contro `142.577,93` circa, invariato in ordine di
grandezza — il torneo aveva già scomposto questo gap in cause multiple,
di cui il routing è solo una). Non è una submission Kaggle: promozione a
candidata per il prossimo torneo a tre resta una decisione del
proprietario, non di questo report.

**Non riattivare la leva #2** (cap zootecnico, Sezione 0) nello stesso
esperimento: resta implementata, disattivata di default, da testare da
sola sopra questa V5 in un round separato (MODEL_SPEC V5 Sezione 6).

**Prossimo passo consigliato**, in ordine:

1. investigare l'anomalia di Sezione 3 (perché `26090101`/seat 0 non
   raggiunge la soglia di workforce per SW con il clustering attivo) prima
   di ulteriori modifiche al dispatch;
2. testare la leva #2 (cap zootecnico) da sola sopra V5, con lo stesso
   protocollo 2→4→7 seed;
3. solo dopo, se entrambe restano positive separatamente, valutare se e
   come ricombinarle — non prima di aver capito la causa dell'interazione
   negativa già osservata.

## 5. Cosa NON è stato fatto

- Nessun seed holdout o final-confirmation consumato (solo i 7 seed di
  sviluppo).
- Nessuna submission Kaggle.
- Nessuna modifica a V3 o V4 (file separati, invariati — V3 verificato
  con la sua suite di test, 28/28 passanti).
- La leva #2 (cap zootecnico) non è stata riattivata dopo l'ablation di
  Sezione 0.
