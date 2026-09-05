# E18.18 — confronto consistenze 7-7-0 con Top770

## Verdetto

Il confronto è sufficientemente pulito: cinque replay esatti `7-7-0` di Top770, incluso il recente `105565293`, hanno un solo action shape, 14 animali, peak crop 62 e la stessa traiettoria delle colture fino a D25. Due replay recenti `10-7-0` sono stati esclusi esplicitamente.

La nostra consistenza zootecnica è quasi allineata nel totale ma non nel mix; quella colturale è allineata soltanto fino a D10. Il gap principale non è la superficie: E18.16 ha 509 crop tile-days D21-D30 contro 515, ma raccoglie 580 unità contro 885. Mancano turnover, servizio e liquidazione coerenti con la capacità già disponibile.

## Traiettoria delle consistenze

| Giorno | Top770 770 — colture | E18.16 — colture | Top770 770 — animali | E18.16 — animali |
|---|---:|---:|---:|---:|
| D01 | M 12 + W 7 | M 12 + W 7 | Cow 2 + Sheep 2 | Cow 2 + Sheep 2 |
| D05 | M 12 + W 7 | M 12 + W 7 | Cow 4 + Sheep 2 | Cow 4 + Sheep 2 |
| D10 | M 12 + S 20 + W 5 | M 12 + S 20 + W 5 | Cow 9 + Sheep 4 | Cow 8 + Sheep 4 |
| D15 | S 38 + W 23 | M 8 + S 34 + W 13 | Cow 9 + Sheep 5 | Cow 8 + Sheep 6 |
| D20 | S 38 + W 23 | M 8 + S 42 + W 9 | Cow 9 + Sheep 5 | Cow 8 + Sheep 6 |
| D25 | S 22 + W 39 | S 25 + W 32 | Cow 9 + Sheep 5 | Cow 8 + Sheep 6 |
| D30 | C 2 / W 2 | S 14 + W 1 | Cow 9 + Sheep 5 | Cow 8 + Sheep 6 |

## KPI di capacità e conversione

| KPI | Top770 770 | E18.16 | Delta Codex |
|---|---:|---:|---:|
| Peak crop | 62 | 59 | -4.8% |
| Crop tile-days totali | 1350 | 1308 | -3.1% |
| Crop tile-days D21-D30 | 515 | 509 | -1.2% |
| Unità raccolte | 885 | 580 | -34.5% |
| PLANT | 243 | 202 | -16.9% |
| WATER | 1172 | 926 | -21.0% |
| HARVEST | 467 | 403 | -13.7% |
| MOVE | 3473 | 3603 | +3.7% |
| PASS | 515 | 851 | +65.2% |

## Lettura strategica

1. **Animali:** Top770 usa invariabilmente `9 COW + 5 SHEEP`; E18.16 usa `8 COW + 6 SHEEP`. Il totale 14 è corretto, ma a D10 Codex è ancora a 12 contro 13. La `9+5` va provata come ablation separata, senza riaprire topologia o cap.
2. **Colture iniziali:** D1, D5 e D10 coincidono esattamente. Questa parte del nostro piano è validata dal benchmark.
3. **Regime D15-D20:** Top770 ha già eliminato MELON e mantiene `38 STRAWBERRY + 23 WHEAT` su 61 tile. Codex conserva 8 MELON, resta a 55-59 tile e sbilancia il mix verso STRAWBERRY.
4. **Chiusura:** a D25 Top770 passa a `22 STRAWBERRY + 39 WHEAT`; a D30 lascia soltanto due annuali. Codex arriva con 15 colture, di cui 14 STRAWBERRY: è la prova più netta che il calendario di stop/liquidazione non è ancora chiuso.
5. **Adattamento utile:** Top770 conserva volumi invarianti di MELON e STRAWBERRY, ma scambia CARROT e WHEAT in funzione dello scenario. Il planner deve vincolare la famiglia `CARROT+WHEAT`, non una ripartizione rigida.

## Specifiche candidate per Gate 0 E18.18

- topologia `7-7-0`, cap 14 invariati;
- ablation zootecnica `9 COW + 5 SHEEP`;
- peak 62 crop entro D13 e plateau 61 tra D15 e D25;
- checkpoint crop uguali alla tabella fino a D25;
- `CARROT+WHEAT` adattivi a parità di volume complessivo;
- massimo 2 crop residui a D30;
- capacità minima di servizio coerente con 243 PLANT, 1.172 WATER e 467 HARVEST, prima di aumentare il numero di tile.

## Limiti

Il campione Top770 è condizionato alla topologia finale `7-7-0`; Top770 usa anche `10-7-0` in altri replay. Seed, avversari e mercato differiscono dal mirror locale, quindi questi sono target di pianificazione descrittivi, non effetti economici causali.
