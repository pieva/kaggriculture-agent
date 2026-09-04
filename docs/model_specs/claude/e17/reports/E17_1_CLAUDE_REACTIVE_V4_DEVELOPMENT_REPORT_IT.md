# E17.1 — Claude reattivo V4: risultato del benchmark a 4 seed (SW/Q2 livestock)

- **Data:** 2026-09-03
- **Stato:** SPOT-CHECK COMPLETO SU 4 SEED — **esito negativo in aggregato,
  matrice completa NON eseguita**. Nessun seed holdout o
  final-confirmation consumato.
- **Candidata:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V4`
  (`src/agricola/strategy/claude/e17_reactive_3q_v4.py`,
  `docs/model_specs/claude/e17/configs/CLAUDE_E17_1_3Q_REACTIVE_V4.json`)
- **Predecessore:** V3 (`FROZEN_WITH_FAILED_GATES`), confrontata sugli
  stessi seed con lo stesso strumento
  (`run_claude_e17_1_v3_dev_benchmark_vs_codex.py`)
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V4.md`
- **Piano di origine:** `docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V4_STATIC_PLAN_IT.md`
  Sezione 5 (protocollo: 2 seed, poi 4 se stabile, poi matrice completa
  solo se stabile su 4)
- **Artifact grezzo:** `docs/model_specs/claude/e17/artifacts/derived/E17_1_V4_4SEED_SPOTCHECK_VS_CODEX.json`
  (V4, 16 match) confrontato con una rigenerazione mirata dello stesso
  strumento V3 sugli stessi 4 seed (numeri riportati in Sezione 2; il
  benchmark canonico V3 a 7 seed/28 match citato da
  `E17_1_CLAUDE_REACTIVE_V4_100K_IMPROVEMENT_PLAN.md`, con media
  `13.540,86`, resta in `E17_1_V3_METRICS.json` ed è stato rigenerato
  in `E17_1_V3_DEV_BENCHMARK_VS_CODEX.json` dopo questo confronto)

---

## 1. Cosa è stato testato

Unica variabile isolata: `max_quadrants_for_livestock` da `2` a `3`, con
SW che riceve una soglia di costruzione propria e più piccola
(`livestock_structures_target_third_quadrant = 2`) invece di ereditare
quella di NW/NE (`4`). Nessun'altra leva toccata (dettaglio in MODEL_SPEC
V4 Sezione 3). Confronto black-box V4 vs V3, stesso avversario
(`CODEX_REACTIVE`), stessi 4 seed di sviluppo, 2 seat ciascuno (16 match
per versione).

## 2. Risultato per seed

| Seed | V3 denaro medio | V4 denaro medio | Delta | V3 animali finali | V4 animali finali |
|---|---:|---:|---:|---:|---:|
| `26090101` | 11.418,00 | 9.110,00 | **-20,2%** | 3,5 | 3,5 |
| `26090102` | 10.256,00 | 10.528,50 | +2,7% | 3,0 | 8,0 |
| `26090103` | 17.110,50 | 17.840,00 | +4,3% | 4,0 | 1,0 |
| `1838889274` | 14.167,00 | 10.737,50 | **-24,2%** | 3,5 | 6,0 |
| **Media (16 match)** | **13.237,88** | **12.054,00** | **-8,9%** | **3,50** | **4,63** |

Zero errori tecnici, zero fughe (`weed=0` in ogni run), workforce
identica (8 hands finali, invariata da V3) in tutti gli otto run.
Nessuna regressione di sicurezza: la variabile ha effetto solo economico.

## 3. Interpretazione

Il segno del delta è **incoerente fra seed** (2 negativi, 2 positivi) e
l'aggregato è **negativo** (`-8,9%`), non lo zero/stabile richiesto dal
protocollo per procedere alla matrice completa a 7 seed. La variabile non
è quindi promuovibile allo stato attuale.

Il dato più interessante non è il segno del delta ma la sua causa
probabile: V4 ottiene in media **più animali** (`4,63` contro `3,50`,
+32%) ma **meno denaro** (`-8,9%`). Questo è coerente con l'ipotesi
§2.2 di `E17_1_CLAUDE_REACTIVE_V4_100K_IMPROVEMENT_PLAN.md` (soffitto di
workforce non ancora verificato su V3): con lavoratori invariati a 8 contro
i 10 di Codex, aprire un terzo quadrante zootecnico più lontano dal centro
(SW, non adiacente all'NW "core") aggiunge MOVE/BUILD/FEED su una
superficie più ampia senza aumentare la capacità di servirla. Il piccolo
guadagno in capi (+32%) non compensa l'overhead di spostamento fra tre
quadranti invece di due — la stessa dinamica di overhead di movimento già
CONFERMATA in `E17_1_CLAUDE_REACTIVE_V4_100K_IMPROVEMENT_PLAN.md` §2.1
(`move_command_fraction = 68,6%`), qui applicata a una superficie
zootecnica più dispersa invece che più densa.

**Non falsifica** l'evidenza Kaggle live di Sezione 0 del piano statico
(Codex live e shiggriculture *possono* sostenere bestiame in tutti e 3 i
quadranti restando sopra 100k): quei due archetipi operano con più
lavoratori e/o meno overhead di movimento di Claude V3/V4. Falsifica
invece l'ipotesi più debole implicita nel piano — che bastasse copiare la
*topologia* (dove costruire) per avvicinarsi al loro risultato, senza
prima risolvere la capacità di servirla.

## 4. Decisione

- **Non promuovere V4 a candidata primaria.** Non eseguire la matrice
  completa a 7 seed × 2 seat su questa variabile da sola: il protocollo
  la richiede solo dopo stabilità/positività su 4 seed, non presente qui.
- **Non scartare il file `e17_reactive_3q_v4.py`**: resta un'infrastruttura
  valida (config-toggle singolo, test dedicati, tutti passanti) per
  ri-testare la stessa ipotesi *dopo* aver affrontato il soffitto di
  workforce (leva #2 del piano di miglioramento 100k), invece che prima.
- **Prossimo passo consigliato**: eseguire prima la leva #2 già pianificata
  (ablation `max_hands`/`hire_reserve` su V3, isolata) per verificare se
  Claude può sostenere più di 8 hands sotto contesa reale; solo se quella
  leva alza stabilmente il tetto di workforce, ri-testare l'apertura SW
  su V4 con più lavoratori disponibili per servirla, invece di
  combinare le due variabili nello stesso esperimento.

## 5. Cosa NON è stato fatto

- Nessun seed holdout o final-confirmation consumato (solo
  `26090101/02/03`, `1838889274`, tutti nel set di sviluppo).
- Nessuna matrice completa a 7 seed.
- Nessuna modifica a V3 (file separato, invariato — verificato con la
  sua suite di test, 28/28 passanti prima e dopo).
- Nessuna submission Kaggle.
