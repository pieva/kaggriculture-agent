# E18.4 — Gate della 7-7-2 state-driven

## Verdetto

`REJECTED_DEVELOPMENT_ONLY_NO_KAGGLE_UPLOAD`.

E18.4 V1 supera tutti i vincoli strutturali, ma fallisce il gate economico. Il
risultato distingue il problema di topologia dal problema di dispatch: ridurre
Q2 a due pascoli è eseguibile senza vuoti o fughe, ma lo scheduler nativo
percorre troppa distanza per unità di lavoro.

## Protocollo

- avversario unico: E18.2 capacity-governed V4D;
- seed `180903001` … `180903007`, entrambi i seat;
- 14 episodi, nessun peer agent, Antigravity escluso;
- holdout e final-confirmation non consumati;
- target economico: 100.000 money medio.

## Risultati

| Misura | E18.4 V1 | E18.2 controllo | Delta |
|---|---:|---:|---:|
| Money medio | 55.940,0 | 83.095,7 | -27.155,7 (-32,68%) |
| Money mediano | 55.455 | 75.235 | -19.780 |
| Intervallo | 25.152–82.402 | 48.161–124.199 | — |
| Vittorie | 0/14 | 14/14 | — |
| Harvested units | 486,0 | 601,3 | -19,17% |
| Crop tile-days D21-D30 | 450,3 | 472,9 | -4,77% |
| Units per harvest | 3,156 | 2,585 | +22,06% |
| Move actions | 4.636,6 | 3.584,6 | +29,35% |
| Productive actions | 2.215,4 | 2.802,6 | -20,95% |
| Late weed tile-days | 44,1 | 15,0 | +194,29% |
| Abandoned crops | 29,0 | 47,0 | -38,30% |

## Diagnosi

Passano topologia 14/14, fill 16/16 14/14, zero fughe/errori/fallback,
persistenza tardiva al 95,23% e batching (+22,06% unità per raccolta). Il campo
rimane occupato, ma il dispatcher greedy perde località quando priorità globali
diverse si alternano: +1.052 move action e -587 azioni produttive per episodio.
Le colture arrivano quindi più spesso a weed e producono 115 unità in meno.

## Decisione

Nessuna submission E18.4 V1. La prossima ablation cambia soltanto il dispatcher:
cluster persistenti, aging e carrier affinity. Market, 7-7-2, batching biologico
e cap restano congelati finché il gate di efficienza del lavoro non è superato.

