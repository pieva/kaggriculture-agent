# MODEL SPEC — Codex E18.4 State-Driven 7-7-2 V1

## Stato

`REJECTED_AT_DEVELOPMENT_ECONOMIC_GATE`.

La candidata è una ablation architetturale utile ma non è autorizzata per una
submission Kaggle. Holdout e final-confirmation non sono stati consumati.

## Ipotesi e contratto causale

E18.4 verifica un handoff completo a uno scheduler state-driven dal giorno 11,
con E18.2 come bootstrap e provider di land, hire e input:

- giorni 0-10: passthrough esatto E18.2;
- dal giorno 11: unit action ricostruite dall'osservazione;
- topologia fissa 7-7-2, 16 pascoli e un coop;
- cap di 16 risorse COW/SHEEP;
- feed, care, water, harvest, fill, dig e plant derivati dallo stato corrente;
- raccolte batchate fino alla capacità biologica o alla deadline;
- vendita dallo shed osservato, con riserva Wheat e liquidazione D29;
- nessuna memoria cross-episode o informazione privata avversaria.

## Gate di sviluppo

Sette seed E18 preregistrati, entrambi i seat contro E18.2, 14 match.

| KPI | E18.4 V1 | E18.2 | Delta/esito |
|---|---:|---:|---:|
| Money medio | 55.940 | 83.095,7 | -32,68% |
| Money max | 82.402 | 124.199 | fail target 100k |
| Harvested units | 486,0 | 601,3 | 80,83% |
| Crop tile-days D21-D30 | 450,3 | 472,9 | 95,23% |
| Mean units/harvest | 3,156 | 2,585 | +22,06% |
| Move actions | 4.636,6 | 3.584,6 | +29,35% |
| Productive actions | 2.215,4 | 2.802,6 | -20,95% |
| Late weed tile-days | 44,1 | 15,0 | +194,29% |
| Topologia esatta | 14/14 | n/a | pass |
| Pascoli target pieni | 14/14 | n/a | pass |
| Fughe/errori/fallback | 0/0/0 | 0/0/0 | pass |

## Verdetto e requisito V2

Lo scheduler risolve cap, fill, perdite e persistenza della superficie, ma il
dispatcher greedy trasforma capacità utile in movimento. V1 è una base
diagnostica, non un agente da caricare. V2 dovrà aggiungere ownership dei
cluster NW/NE/SW, task aging e carrier affinity. Il gate preliminare richiede
move action non superiori al controllo e productive action almeno al 95% del
controllo, prima di valutare il money.

