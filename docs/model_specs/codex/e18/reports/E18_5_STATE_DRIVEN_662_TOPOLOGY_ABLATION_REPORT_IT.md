# E18.5 — ablation topologica 6-6-2

## Decisione

**Efficiency gate: FAIL**. La candidata resta
development-only e nessun upload Kaggle è autorizzato.

## Confronto diretto

| KPI medio vs E18.2 | 6-6-2 | 7-7-2 frozen | Delta 6-6-2 |
|---|---:|---:|---:|
| Move | 4451.86 | 4477.43 | -0.57% |
| Productive | 2223.07 | 2217.43 | +0.25% |
| Move/productive | 2.0026 | 2.0192 | -0.82% |
| Money | 49179.43 | 47247.57 | +4.09% |
| Harvested units | 513.14 | 472.57 | +8.59% |
| Late weed tile-days | 21.79 | 36.36 | -40.08% |

## Check falliti

- `move_actions_at_least_5pct_lower`
- `move_per_productive_at_least_5pct_lower`

## Integrità

- match development: 14;
- topologia 6-6-2 esatta: 14/14;
- fill 14/14: 14/14;
- holdout/final: non consumati;
- errori/fallback/perdite: 0/0/0.

## Lettura causale

La riduzione topologica produce un segnale favorevole ma non materiale sulle
move: `-0,57%` move e `-0,82%` move/productive, molto sotto il `-5%` richiesto.
Le azioni produttive non calano (`+0,25%`). Money, raccolto e late weeds
migliorano rispetto alla 7-7-2, ma la candidata perde comunque 14/14 contro
E18.2. La topologia 6-6-2 da sola non risolve quindi il throughput gap del
dispatcher; la linea non viene promossa.
