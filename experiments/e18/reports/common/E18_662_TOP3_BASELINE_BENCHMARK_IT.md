# E18 — baseline 6-6-2 verso gli archetipi Top 3

- **Data:** 2026-09-03
- **Stato:** ENTRY BASELINE FROZEN
- **Baseline:** `CODEX-E17.3-TOPOLOGY-FILL-662-V2`
- **Candidata pianificata:** `CODEX-E18.1-REACTIVE-662-V1`
- **Target:** denaro medio locale `100.000`
- **Holdout/final:** non consumati e non autorizzati

## Sintesi

La 6-6-2 entra in E18 con una base economica e strutturale forte: `14/14`
pascoli, Q2 limitato a due tile, zero fughe, Q1 medio D6, Q2 medio D11, circa
`59,93` crop di picco e `15` animali. Contro Claude supera 100k; contro una
6-6-2 equivalente scende però a `79.323,86`.

La revisione V3 non dimostra reattività: su 28 run comparabili produce metriche
complete e conteggi azione identici alla V2. E18 si apre quindi per correggere
la selezione di regime, non la topologia.

## Benchmark Top 3 osservazionale

| Profilo | Episodi | Score medio | Q1 mediano | Q2 mediano | Peak crop | Peak animali | MOVE | Fughe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tetsuya` | 4 | 96.568 | step 169 / D7 | step 241 / D10 | 58 | 15 | 3.377,25 | 0 |
| `OceanMix` | 4 | 82.535,25 | step 151 / D6 | step 266 / D11 | 61 | 14,25 | 3.075,75 | 0 |
| `Crop Dusta` | 5 | 91.361,20 | step 122 / D5 | step 203 / D8 | 60,6 | 16,8 | 4.070 | 31 |
| 6-6-2 E17 | 42 run locali | 114.586,40 all-regime | D6 medio | D11 medio | 59,93 | 15 | 3.592,43 | 0 |

I Top 3 sono archetipi selezionati da replay E17 già consumati, non policy
eseguibili e non una garanzia sulla leaderboard live corrente. Score dei
replay e denaro locale non sono perfettamente exchangeable perché cambiano
opposizione e regime di mercato.

## Gate di ingresso

| Gate | Osservato | Stato |
|---|---:|---|
| Denaro vs Claude ≥100k | 132.217,68 | PASS |
| Denaro in contesa simmetrica ≥100k | 79.323,86; gap 20.676,14 | **FAIL** |
| Q1 nel range Top 3 D5–D7 | D6 | PASS |
| Q2 nel range Top 3 D8–D11 | D11 | PASS, al limite lento |
| Peak crop ≥58 | 59,93 | PASS |
| Pascoli 14/14 e Q2≤2 | 14/14; 2 | PASS |
| Fughe | 0 | PASS |
| Action-stream divergence V3/V2 | 0/28 | **FAIL** |
| Telemetria causale di attivazione | assente | **MISSING** |

## Delta da colmare in E18

1. **Contesa simmetrica:** servono `+20.676,14`, cioè circa `+26,1%`, per
   portare il self-play sopra 100k.
2. **Reattività reale:** almeno uno scenario deve cambiare action stream in
   modo previsto e registrare la feature che ha causato l'override.
3. **Telemetria:** transizioni di regime, guard activation, ordini visti,
   ordini throttled e unità soppresse sono prerequisiti, non analisi post-hoc.
4. **Confrontabilità logistica:** E18 deve produrre sia MOVE/produttive locale
   sia move share active dei replay; le due misure non vanno equiparate.
5. **Robustezza:** mantenere D6/D11, ~60 crop, 15 animali, 14/14 e zero fughe
   mentre si migliora la contesa.

## Decisione di apertura

E18 è aperto con una sola famiglia causale:
`OBSERVABLE_MARKET_AND_SERVICE_REGIME_SELECTION_WITH_662_INVARIANTS`.
Prima di nuovi match economici devono essere costruite activation fixture che
forzino i regimi e dimostrino divergenza dal controllo. Holdout e
final-confirmation restano bloccati.

Fonti:

- `experiments/e18/artifacts/baseline/E18_662_TOP3_BASELINE_BENCHMARK_V1.json`;
- `experiments/e17/artifacts/discovery/codex/E17_TOP3_REPLAY_METRICS.json`;
- `experiments/e17/artifacts/derived/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3.json`;
- `experiments/e18/design/E18_REACTIVE_662_TOP3_BENCHMARK_PLAN_V1.md`.
