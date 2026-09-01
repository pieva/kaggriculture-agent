# NEW_SESSION — Kaggriculture

## Ripresa operativa

```text
START_HERE: docs/PROJECT_STATE.md
FOUNDATION: C2.1 RECONCILED
FOUNDATION_MANIFEST: docs/model/FOUNDATION_C2_1_MANIFEST.md
REPOSITORY_CLEANUP: COMPLETE

CURRENT_CODEX_MODEL: CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY
CURRENT_CODEX_SUBMISSION: submission/submission_codex.py
KAGGLE_SCORE_SNAPSHOT: 1159.9
KAGGLE_POSITION_SNAPSHOT: 2542
VISIBLE_LEADER_SCORE: 2943.6

NEXT_EXPERIMENT: E17
E17_PHASE: DEFINE
E17_OBJECTIVE: DEFINE_3Q_OPTIMIZATION_BENCHMARK_STRATEGY
```

## Perché E17 parte dal benchmark

Codex V9 3Q ha quasi raddoppiato lo score Kaggle rispetto alla V7.3 dual-Q
(`1159,9` contro `598,3`), ma raggiunge soltanto il `39,4%` del punteggio del
leader visibile. Il salto dimostra che 3Q è una direzione promettente; non
dimostra ancora quali componenti della strategia producano il vantaggio né
come colmare il gap residuo.

Il replay pubblico `docs/benchmark/104498819.json` mostra inoltre tre
quadranti attivi in una strategia ad alto rendimento. È evidenza a favore
dell'ipotesi 3Q, non prova che l'intera fascia alta della leaderboard usi la
stessa architettura.

## Missione E17

Definire, preregistrare e congelare il benchmark che guiderà le successive
ottimizzazioni 3Q. E17 è una fase `DEFINE`: non deve selezionare una policy
nuova usando dati già osservati e non deve iniziare con tuning opportunistico.

Il deliverable deve specificare:

- baseline e hash immutabili;
- seed di sviluppo e holdout, seat swap e matrice degli avversari;
- metriche economiche, operative e competitive per Q0/Q1/Q2;
- famiglie di leve causali da testare separatamente: timing di attivazione,
  workforce, geometria, mix crop/livestock, feeding, market cadence,
  trasporto e liquidazione terminale;
- protocollo requested/executed, errori e fallback;
- criteri di vittoria, floor, robustezza e arresto;
- regola di promozione verso un test Kaggle successivo;
- metodo per stimare la correlazione, ancora non dimostrata, fra benchmark
  locale e score leaderboard.

## Baseline disponibili

- Codex V9: baseline 3Q canonica e submission Kaggle corrente;
- Antigravity V4: baseline derivativa con liquidazione terminale;
- Copilot V2: baseline derivativa diagnostica, senza submission canonica;
- torneo di chiusura: ablation riproducibile, non torneo indipendente.

## Vincoli inderogabili

- nessun agente può importare o copiare routine, action table, planner,
  dispatcher o schedule di un altro;
- Foundation e protocollo di benchmark possono essere condivisi;
- ogni variazione deve avere ipotesi causale e falsificazione dichiarate;
- nessuna submission Kaggle durante la sola fase `E17 DEFINE`;
- distinguere sempre `final_money` locale dallo score leaderboard Kaggle.

## Documenti da leggere

- `docs/PROJECT_STATE.md`;
- `docs/model/FOUNDATION_C2_1_MANIFEST.md`;
- `results/model_spec_c2/foundation_revision/C2_1_POST_3Q_FOUNDATION_RECONCILIATION.md`;
- `results/model_spec_c2/post_3q_closure_tournament/POST_3Q_CLOSURE_TOURNAMENT_REPORT_IT.md`;
- `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`.
