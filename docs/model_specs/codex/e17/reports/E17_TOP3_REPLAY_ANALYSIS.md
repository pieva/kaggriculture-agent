# E17 — benchmark forense Codex sui replay Top 3

## Esito

Corpus elaborato integralmente: **9 episodi, 18 player-seat, 6,480 step di episodio**.
Tutti i replay sono validi, distinti, `DONE/DONE`, su `module_version 1.32.7`.

Clock: `D#:H##` usa giorno e ora zero-based del replay. Lo sblocco è il primo stato in cui il quadrante risulta osservabile come posseduto.
I move sono comandi cardinali emessi e non implicano necessariamente uno spostamento riuscito. Una fuga è conteggiata soltanto se, attraverso un EOD, una tile passa da animale a stessa struttura vuota con `consecutive_unfed=1` e `fed_today=false` nello stato precedente.

## Sintesi per episodio e partecipante

| Ep. | Partecipante | Esito | Score | Q1 | Q2 | Move | Move/azioni attive | Assistenti | Fughe | Picco crop/animali | Crop finali | Animali finali | Non-crop finali | Tile inattive finali |
|---:|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 104527555 | tetsuya | WIN | 81,050 | D7:H01 / s169 (NE) | D10:H01 / s241 (SW) | 3,415 | 52.64% | 11 | 0 | 58/15 | 4 | 15 | 71 | 56 |
| 104527555 | Driz Lo | LOSS | 52,953 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 2,938 | 47.08% | 11 | 0 | 58/9 | 0 | 9 | 75 | 66 |
| 104541810 | tetsuya | WIN | 109,204 | D7:H01 / s169 (NE) | D10:H01 / s241 (SW) | 3,344 | 52.27% | 11 | 0 | 58/15 | 11 | 15 | 64 | 49 |
| 104541810 | QQ Farming | LOSS | 97,241 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 2,969 | 47.21% | 11 | 0 | 58/11 | 0 | 11 | 75 | 64 |
| 104543983 | Crop Dusta | WIN | 83,634 | D6:H11 / s155 (NE) | D9:H02 / s218 (SW) | 3,958 | 55.15% | 12 | 3 | 60/18 | 2 | 15 | 73 | 58 |
| 104543983 | tetsuya | LOSS | 76,264 | D7:H01 / s169 (NE) | D10:H01 / s241 (SW) | 3,399 | 52.77% | 11 | 0 | 58/15 | 0 | 15 | 75 | 60 |
| 104547425 | OceanMix | WIN | 114,361 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 3,207 | 48.95% | 11 | 0 | 58/17 | 0 | 17 | 75 | 58 |
| 104547425 | Crop Dusta | LOSS | 106,328 | D5:H02 / s122 (NE) | D8:H07 / s199 (SW) | 4,001 | 54.64% | 12 | 6 | 57/20 | 2 | 14 | 73 | 59 |
| 104564762 | Driz Lo | WIN | 90,185 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 2,970 | 48.82% | 10 | 0 | 62/13 | 0 | 13 | 75 | 62 |
| 104564762 | Crop Dusta | LOSS | 87,152 | D5:H02 / s122 (NE) | D8:H09 / s201 (SW) | 4,147 | 56.69% | 12 | 9 | 60/15 | 11 | 6 | 64 | 58 |
| 104577270 | yukino | WIN | 90,053 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 2,970 | 48.82% | 10 | 0 | 62/13 | 0 | 13 | 75 | 62 |
| 104577270 | OceanMix | LOSS | 86,580 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 3,148 | 49.29% | 11 | 0 | 62/14 | 0 | 14 | 75 | 61 |
| 104578185 | tetsuya | WIN | 119,754 | D7:H01 / s169 (NE) | D10:H01 / s241 (SW) | 3,351 | 52.23% | 11 | 0 | 58/15 | 4 | 15 | 71 | 56 |
| 104578185 | Crop Dusta | LOSS | 114,881 | D6:H11 / s155 (NE) | D8:H20 / s212 (SW) | 4,204 | 58.14% | 12 | 8 | 62/17 | 4 | 9 | 71 | 62 |
| 104586335 | Crop Dusta | WIN | 64,811 | D5:H02 / s122 (NE) | D8:H11 / s203 (SW) | 4,040 | 55.72% | 12 | 5 | 64/14 | 1 | 9 | 74 | 65 |
| 104586335 | OceanMix | LOSS | 51,238 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 2,974 | 48.87% | 10 | 0 | 62/13 | 0 | 13 | 75 | 62 |
| 104586487 | OceanMix | WIN | 77,962 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 2,974 | 48.87% | 10 | 0 | 62/13 | 0 | 13 | 75 | 62 |
| 104586487 | Driz Lo | LOSS | 75,760 | D6:H07 / s151 (NE) | D11:H02 / s266 (SW) | 2,970 | 48.82% | 10 | 0 | 62/13 | 0 | 13 | 75 | 62 |

`Tile inattive finali` = arabile vuota + weed + struttura vuota + stato non classificato, sui 75 tile posseduti. Le tile occupate da animali non sono incluse fra le inattive.

## Aggregazione per nome agente

| Agente | N | W-L | Score medio | Q1 mediano | Q2 mediano | Move medi | Move/attive | Assistenti | Fughe | Picco crop | Picco animali | Attivazione tile | Crop finali | Animali finali | Inattive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tetsuya | 4 | 3-1 | 96,568 | 169 | 241 | 3,377.25 | 52.48% | 11 | 0 | 58 | 15 | 87.44% | 4.75 | 15 | 55.25 |
| OceanMix | 4 | 2-2 | 82,535.25 | 151 | 266 | 3,075.75 | 48.99% | 10.50 | 0 | 61 | 14.25 | 92.19% | 0 | 14.25 | 60.75 |
| Crop Dusta | 5 | 2-3 | 91,361.20 | 122 | 203 | 4,070 | 56.07% | 12 | 31 | 60.60 | 16.80 | 87.26% | 4 | 10.60 | 60.40 |
| Driz Lo | 3 | 1-2 | 72,966 | 151 | 266 | 2,959.33 | 48.24% | 10.33 | 0 | 60.67 | 11.67 | 87.19% | 0 | 11.67 | 63.33 |
| QQ Farming | 1 | 0-1 | 97,241 | 151 | 266 | 2,969 | 47.21% | 11 | 0 | 58 | 11 | 83.01% | 0 | 11 | 64 |
| yukino | 1 | 1-0 | 90,053 | 151 | 266 | 2,970 | 48.82% | 10 | 0 | 62 | 13 | 92.27% | 0 | 13 | 62 |

## Lettura descrittiva immediata

- `OBSERVED/DERIVED`: Crop Dusta sblocca prima: Q1 mediano s122 e Q2 mediano s203, contro s169/s241 per tetsuya e s151/s266 per OceanMix.
- `DERIVED`: alla maggiore precocità di Crop Dusta è associato il carico di movimento più alto (4,070 move medi; 56.07% delle azioni attive), rispetto a tetsuya (3,377.25; 52.48%) e OceanMix (3,075.75; 48.99%). Questa è associazione, non effetto causale identificato.
- `OBSERVED`: la workforce finale media è 12 per Crop Dusta, 11 per tetsuya e 10.50 per OceanMix.
- `DERIVED`: tutti i 31 eventi compatibili con fuga secondo il criterio EOD stretto appartengono a Crop Dusta; distribuzione per EOD: giorno 23: 1, giorno 27: 5, giorno 28: 25. La concentrazione terminale suggerisce una scelta di abbandono o servicing ridotto, ma il valore economico causale resta da testare.
- `DERIVED`: i picchi medi giornalieri crop/animali sono 58/15 per tetsuya, 61/14.25 per OceanMix e 60.60/16.80 per Crop Dusta.
- `UNKNOWN`: la composizione finale non rappresenta da sola l'impiego stagionale del terreno; per questo il CSV giornaliero conserva le traiettorie complete.

## Composizione finale per quadrante

Ogni riga somma a 25 tile. `Non-crop` include animali, strutture, vuote e weed; `Inattive` esclude gli animali ma include strutture vuote.

| Ep. | Partecipante | Q | Sblocco | Vuote | Weed | Strutture vuote | Wheat | Carrot | Tomato | Strawberry | Melon | Goose | Cow | Sheep | Crop | Animali | Non-crop | Inattive |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 104527555 | tetsuya | Q0 (NW) | D0:H00 / s0 | 17 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 1 | 7 | 24 | 17 |
| 104527555 | tetsuya | Q1 (NE) | D7:H01 / s169 | 20 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 3 | 2 | 22 | 20 |
| 104527555 | tetsuya | Q2 (SW) | D10:H01 / s241 | 18 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 5 | 0 | 6 | 25 | 19 |
| 104527555 | Driz Lo | Q0 (NW) | D0:H00 / s0 | 15 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 0 | 7 | 25 | 18 |
| 104527555 | Driz Lo | Q1 (NE) | D6:H07 / s151 | 18 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 | 25 | 23 |
| 104527555 | Driz Lo | Q2 (SW) | D11:H02 / s266 | 24 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104541810 | tetsuya | Q0 (NW) | D0:H00 / s0 | 15 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 3 | 7 | 22 | 15 |
| 104541810 | tetsuya | Q1 (NE) | D7:H01 / s169 | 15 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 7 | 3 | 18 | 15 |
| 104541810 | tetsuya | Q2 (SW) | D10:H01 / s241 | 15 | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 1 | 5 | 24 | 19 |
| 104541810 | QQ Farming | Q0 (NW) | D0:H00 / s0 | 15 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 0 | 8 | 25 | 17 |
| 104541810 | QQ Farming | Q1 (NE) | D6:H07 / s151 | 18 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 3 | 25 | 22 |
| 104541810 | QQ Farming | Q2 (SW) | D11:H02 / s266 | 24 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104543983 | Crop Dusta | Q0 (NW) | D0:H00 / s0 | 16 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 2 | 0 | 5 | 25 | 20 |
| 104543983 | Crop Dusta | Q1 (NE) | D6:H11 / s155 | 18 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 1 | 1 | 0 | 6 | 25 | 19 |
| 104543983 | Crop Dusta | Q2 (SW) | D9:H02 / s218 | 19 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 3 | 1 | 2 | 4 | 23 | 19 |
| 104543983 | tetsuya | Q0 (NW) | D0:H00 / s0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 0 | 7 | 25 | 18 |
| 104543983 | tetsuya | Q1 (NE) | D7:H01 / s169 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 2 | 25 | 23 |
| 104543983 | tetsuya | Q2 (SW) | D10:H01 / s241 | 11 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 0 | 6 | 25 | 19 |
| 104547425 | OceanMix | Q0 (NW) | D0:H00 / s0 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 6 | 0 | 10 | 25 | 15 |
| 104547425 | OceanMix | Q1 (NE) | D6:H07 / s151 | 17 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 2 | 0 | 7 | 25 | 18 |
| 104547425 | OceanMix | Q2 (SW) | D11:H02 / s266 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104547425 | Crop Dusta | Q0 (NW) | D0:H00 / s0 | 14 | 0 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 2 | 6 | 23 | 17 |
| 104547425 | Crop Dusta | Q1 (NE) | D5:H02 / s122 | 19 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 5 | 25 | 20 |
| 104547425 | Crop Dusta | Q2 (SW) | D8:H07 / s199 | 18 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 3 | 25 | 22 |
| 104564762 | Driz Lo | Q0 (NW) | D0:H00 / s0 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 6 | 25 | 19 |
| 104564762 | Driz Lo | Q1 (NE) | D6:H07 / s151 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 4 | 0 | 7 | 25 | 18 |
| 104564762 | Driz Lo | Q2 (SW) | D11:H02 / s266 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104564762 | Crop Dusta | Q0 (NW) | D0:H00 / s0 | 16 | 0 | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 21 | 21 |
| 104564762 | Crop Dusta | Q1 (NE) | D5:H02 / s122 | 12 | 3 | 4 | 0 | 0 | 5 | 0 | 0 | 0 | 1 | 0 | 5 | 1 | 20 | 19 |
| 104564762 | Crop Dusta | Q2 (SW) | D8:H09 / s201 | 15 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 5 | 0 | 0 | 2 | 5 | 23 | 18 |
| 104577270 | yukino | Q0 (NW) | D0:H00 / s0 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 6 | 25 | 19 |
| 104577270 | yukino | Q1 (NE) | D6:H07 / s151 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 4 | 0 | 7 | 25 | 18 |
| 104577270 | yukino | Q2 (SW) | D11:H02 / s266 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104577270 | OceanMix | Q0 (NW) | D0:H00 / s0 | 16 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 0 | 7 | 25 | 18 |
| 104577270 | OceanMix | Q1 (NE) | D6:H07 / s151 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 2 | 0 | 7 | 25 | 18 |
| 104577270 | OceanMix | Q2 (SW) | D11:H02 / s266 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104578185 | tetsuya | Q0 (NW) | D0:H00 / s0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 0 | 7 | 25 | 18 |
| 104578185 | tetsuya | Q1 (NE) | D7:H01 / s169 | 19 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 4 | 2 | 21 | 19 |
| 104578185 | tetsuya | Q2 (SW) | D10:H01 / s241 | 18 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 5 | 0 | 6 | 25 | 19 |
| 104578185 | Crop Dusta | Q0 (NW) | D0:H00 / s0 | 14 | 2 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 1 | 1 | 4 | 24 | 20 |
| 104578185 | Crop Dusta | Q1 (NE) | D6:H11 / s155 | 15 | 0 | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 2 | 1 | 5 | 24 | 19 |
| 104578185 | Crop Dusta | Q2 (SW) | D8:H20 / s212 | 17 | 6 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 23 | 23 |
| 104586335 | Crop Dusta | Q0 (NW) | D0:H00 / s0 | 18 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 3 | 25 | 22 |
| 104586335 | Crop Dusta | Q1 (NE) | D5:H02 / s122 | 20 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 | 25 | 22 |
| 104586335 | Crop Dusta | Q2 (SW) | D8:H11 / s203 | 21 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 1 | 3 | 24 | 21 |
| 104586335 | OceanMix | Q0 (NW) | D0:H00 / s0 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 6 | 25 | 19 |
| 104586335 | OceanMix | Q1 (NE) | D6:H07 / s151 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 4 | 0 | 7 | 25 | 18 |
| 104586335 | OceanMix | Q2 (SW) | D11:H02 / s266 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104586487 | OceanMix | Q0 (NW) | D0:H00 / s0 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 6 | 25 | 19 |
| 104586487 | OceanMix | Q1 (NE) | D6:H07 / s151 | 17 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 4 | 0 | 7 | 25 | 18 |
| 104586487 | OceanMix | Q2 (SW) | D11:H02 / s266 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |
| 104586487 | Driz Lo | Q0 (NW) | D0:H00 / s0 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 6 | 25 | 19 |
| 104586487 | Driz Lo | Q1 (NE) | D6:H07 / s151 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 4 | 0 | 7 | 25 | 18 |
| 104586487 | Driz Lo | Q2 (SW) | D11:H02 / s266 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 |

## Indicazione temporale per i tre quadranti

Legenda cella: `C` crop attive, `A` animali presenti, `I` tile inattive. Gli snapshot sono le ultime osservazioni del giorno indicato; il CSV giornaliero conserva specie e categorie complete.

| Ep. | Partecipante | D0 | D5 | D10 | D15 | D20 | D25 | D29 |
|---:|---|---|---|---|---|---|---|---|
| 104527555 | tetsuya | Q0 C10/A3/I12; Q1 locked; Q2 locked | Q0 C15/A7/I3; Q1 locked; Q2 locked | Q0 C18/A7/I0; Q1 C23/A2/I0; Q2 C17/A2/I6 | Q0 C18/A7/I0; Q1 C23/A2/I0; Q2 C17/A6/I2 | Q0 C17/A7/I1; Q1 C23/A2/I0; Q2 C11/A6/I8 | Q0 C18/A7/I0; Q1 C22/A2/I1; Q2 C16/A6/I3 | Q0 C1/A7/I17; Q1 C3/A2/I20; Q2 C0/A6/I19 |
| 104527555 | Driz Lo | Q0 C19/A3/I3; Q1 locked; Q2 locked | Q0 C19/A5/I1; Q1 locked; Q2 locked | Q0 C12/A6/I7; Q1 C15/A2/I8; Q2 locked | Q0 C13/A7/I5; Q1 C15/A2/I8; Q2 C25/A0/I0 | Q0 C13/A7/I5; Q1 C15/A2/I8; Q2 C25/A0/I0 | Q0 C15/A7/I3; Q1 C18/A2/I5; Q2 C25/A0/I0 | Q0 C0/A7/I18; Q1 C0/A2/I23; Q2 C0/A0/I25 |
| 104541810 | tetsuya | Q0 C10/A3/I12; Q1 locked; Q2 locked | Q0 C15/A7/I3; Q1 locked; Q2 locked | Q0 C18/A7/I0; Q1 C22/A3/I0; Q2 C18/A2/I5 | Q0 C18/A7/I0; Q1 C22/A3/I0; Q2 C18/A5/I2 | Q0 C17/A7/I1; Q1 C22/A3/I0; Q2 C18/A5/I2 | Q0 C16/A7/I2; Q1 C22/A3/I0; Q2 C18/A5/I2 | Q0 C3/A7/I15; Q1 C7/A3/I15; Q2 C1/A5/I19 |
| 104541810 | QQ Farming | Q0 C19/A3/I3; Q1 locked; Q2 locked | Q0 C19/A5/I1; Q1 locked; Q2 locked | Q0 C14/A7/I4; Q1 C16/A3/I6; Q2 locked | Q0 C15/A8/I2; Q1 C16/A3/I6; Q2 C25/A0/I0 | Q0 C15/A8/I2; Q1 C16/A3/I6; Q2 C25/A0/I0 | Q0 C15/A8/I2; Q1 C18/A3/I4; Q2 C25/A0/I0 | Q0 C0/A8/I17; Q1 C0/A3/I22; Q2 C0/A0/I25 |
| 104543983 | Crop Dusta | Q0 C13/A5/I7; Q1 locked; Q2 locked | Q0 C18/A6/I1; Q1 locked; Q2 locked | Q0 C18/A7/I0; Q1 C21/A3/I1; Q2 C19/A2/I4 | Q0 C17/A8/I0; Q1 C20/A5/I0; Q2 C20/A3/I2 | Q0 C17/A8/I0; Q1 C19/A6/I0; Q2 C21/A3/I1 | Q0 C14/A8/I3; Q1 C19/A6/I0; Q2 C20/A4/I1 | Q0 C0/A5/I20; Q1 C0/A6/I19; Q2 C2/A4/I19 |
| 104543983 | tetsuya | Q0 C10/A3/I12; Q1 locked; Q2 locked | Q0 C14/A7/I4; Q1 locked; Q2 locked | Q0 C18/A7/I0; Q1 C23/A2/I0; Q2 C8/A2/I15 | Q0 C18/A7/I0; Q1 C23/A2/I0; Q2 C17/A6/I2 | Q0 C14/A7/I4; Q1 C23/A2/I0; Q2 C16/A6/I3 | Q0 C18/A7/I0; Q1 C23/A2/I0; Q2 C17/A6/I2 | Q0 C0/A7/I18; Q1 C0/A2/I23; Q2 C0/A6/I19 |
| 104547425 | OceanMix | Q0 C19/A4/I2; Q1 locked; Q2 locked | Q0 C19/A6/I0; Q1 locked; Q2 locked | Q0 C11/A9/I5; Q1 C18/A7/I0; Q2 locked | Q0 C15/A10/I0; Q1 C17/A7/I1; Q2 C25/A0/I0 | Q0 C15/A10/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C15/A10/I0; Q1 C14/A7/I4; Q2 C24/A0/I1 | Q0 C0/A10/I15; Q1 C0/A7/I18; Q2 C0/A0/I25 |
| 104547425 | Crop Dusta | Q0 C13/A5/I7; Q1 locked; Q2 locked | Q0 C17/A5/I3; Q1 C9/A0/I16; Q2 locked | Q0 C16/A6/I3; Q1 C20/A4/I1; Q2 C18/A3/I4 | Q0 C17/A8/I0; Q1 C18/A5/I2; Q2 C19/A4/I2 | Q0 C15/A8/I2; Q1 C18/A6/I1; Q2 C15/A4/I6 | Q0 C15/A9/I1; Q1 C19/A6/I0; Q2 C20/A4/I1 | Q0 C2/A6/I17; Q1 C0/A5/I20; Q2 C0/A3/I22 |
| 104564762 | Driz Lo | Q0 C19/A4/I2; Q1 locked; Q2 locked | Q0 C19/A6/I0; Q1 locked; Q2 locked | Q0 C16/A6/I3; Q1 C17/A7/I1; Q2 locked | Q0 C19/A6/I0; Q1 C17/A7/I1; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C17/A7/I1; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C16/A7/I2; Q2 C24/A0/I1 | Q0 C0/A6/I19; Q1 C0/A7/I18; Q2 C0/A0/I25 |
| 104564762 | Crop Dusta | Q0 C13/A5/I7; Q1 locked; Q2 locked | Q0 C17/A5/I3; Q1 C8/A0/I17; Q2 locked | Q0 C18/A5/I2; Q1 C20/A5/I0; Q2 C18/A2/I5 | Q0 C20/A5/I0; Q1 C19/A5/I1; Q2 C18/A5/I2 | Q0 C19/A5/I1; Q1 C20/A5/I0; Q2 C20/A5/I0 | Q0 C19/A5/I1; Q1 C18/A5/I2; Q2 C18/A5/I2 | Q0 C4/A0/I21; Q1 C5/A1/I19; Q2 C2/A5/I18 |
| 104577270 | yukino | Q0 C19/A4/I2; Q1 locked; Q2 locked | Q0 C19/A6/I0; Q1 locked; Q2 locked | Q0 C16/A6/I3; Q1 C18/A7/I0; Q2 locked | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C16/A7/I2; Q2 C24/A0/I1 | Q0 C0/A6/I19; Q1 C0/A7/I18; Q2 C0/A0/I25 |
| 104577270 | OceanMix | Q0 C19/A4/I2; Q1 locked; Q2 locked | Q0 C19/A6/I0; Q1 locked; Q2 locked | Q0 C16/A6/I3; Q1 C18/A7/I0; Q2 locked | Q0 C18/A7/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C18/A7/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C18/A7/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C0/A7/I18; Q1 C0/A7/I18; Q2 C0/A0/I25 |
| 104578185 | tetsuya | Q0 C10/A3/I12; Q1 locked; Q2 locked | Q0 C15/A7/I3; Q1 locked; Q2 locked | Q0 C18/A7/I0; Q1 C23/A2/I0; Q2 C17/A1/I7 | Q0 C18/A7/I0; Q1 C23/A2/I0; Q2 C17/A6/I2 | Q0 C16/A7/I2; Q1 C23/A2/I0; Q2 C13/A6/I6 | Q0 C17/A7/I1; Q1 C23/A2/I0; Q2 C17/A6/I2 | Q0 C0/A7/I18; Q1 C4/A2/I19; Q2 C0/A6/I19 |
| 104578185 | Crop Dusta | Q0 C13/A5/I7; Q1 locked; Q2 locked | Q0 C18/A6/I1; Q1 locked; Q2 locked | Q0 C17/A8/I0; Q1 C20/A4/I1; Q2 C24/A0/I1 | Q0 C17/A8/I0; Q1 C16/A9/I0; Q2 C25/A0/I0 | Q0 C15/A8/I2; Q1 C16/A9/I0; Q2 C23/A0/I2 | Q0 C12/A8/I5; Q1 C14/A9/I2; Q2 C25/A0/I0 | Q0 C1/A4/I20; Q1 C1/A5/I19; Q2 C2/A0/I23 |
| 104586335 | Crop Dusta | Q0 C13/A5/I7; Q1 locked; Q2 locked | Q0 C17/A5/I3; Q1 C8/A0/I17; Q2 locked | Q0 C18/A6/I1; Q1 C21/A4/I0; Q2 C23/A0/I2 | Q0 C18/A7/I0; Q1 C21/A4/I0; Q2 C22/A2/I1 | Q0 C18/A7/I0; Q1 C21/A4/I0; Q2 C22/A3/I0 | Q0 C16/A7/I2; Q1 C20/A4/I1; Q2 C22/A3/I0 | Q0 C0/A3/I22; Q1 C0/A3/I22; Q2 C1/A3/I21 |
| 104586335 | OceanMix | Q0 C19/A4/I2; Q1 locked; Q2 locked | Q0 C19/A6/I0; Q1 locked; Q2 locked | Q0 C16/A6/I3; Q1 C18/A7/I0; Q2 locked | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C16/A7/I2; Q2 C24/A0/I1 | Q0 C0/A6/I19; Q1 C0/A7/I18; Q2 C0/A0/I25 |
| 104586487 | OceanMix | Q0 C19/A4/I2; Q1 locked; Q2 locked | Q0 C19/A6/I0; Q1 locked; Q2 locked | Q0 C16/A6/I3; Q1 C18/A7/I0; Q2 locked | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C16/A7/I2; Q2 C24/A0/I1 | Q0 C0/A6/I19; Q1 C0/A7/I18; Q2 C0/A0/I25 |
| 104586487 | Driz Lo | Q0 C19/A4/I2; Q1 locked; Q2 locked | Q0 C19/A6/I0; Q1 locked; Q2 locked | Q0 C16/A6/I3; Q1 C18/A7/I0; Q2 locked | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C18/A7/I0; Q2 C25/A0/I0 | Q0 C19/A6/I0; Q1 C16/A7/I2; Q2 C24/A0/I1 | Q0 C0/A6/I19; Q1 C0/A7/I18; Q2 C0/A0/I25 |

## Eventi di fuga derivati con criterio EOD stretto

La fuga non è un campo evento nativo. Ogni riga è derivata da: animale ancora presente a H23, `consecutive_unfed=1`, `fed_today=false`, nessun FEED/PICKUP richiesto all'EOD e stessa struttura vuota nel primo stato del giorno successivo. Il CSV audit conserva tutti i campi pre/post.

| Ep. | Partecipante | Specie | Quadrante | Coordinata | EOD dopo giorno | Prima assenza osservata |
|---:|---|---|---|---|---:|---|
| 104543983 | Crop Dusta | SHEEP | Q0 (NW) | (2,4) | 28 | D29 / s696 |
| 104543983 | Crop Dusta | SHEEP | Q0 (NW) | (3,3) | 28 | D29 / s696 |
| 104543983 | Crop Dusta | SHEEP | Q0 (NW) | (4,1) | 28 | D29 / s696 |
| 104547425 | Crop Dusta | COW | Q2 (SW) | (8,4) | 23 | D24 / s576 |
| 104547425 | Crop Dusta | SHEEP | Q0 (NW) | (2,3) | 28 | D29 / s696 |
| 104547425 | Crop Dusta | SHEEP | Q0 (NW) | (2,4) | 28 | D29 / s696 |
| 104547425 | Crop Dusta | SHEEP | Q0 (NW) | (3,3) | 28 | D29 / s696 |
| 104547425 | Crop Dusta | SHEEP | Q1 (NE) | (3,8) | 28 | D29 / s696 |
| 104547425 | Crop Dusta | SHEEP | Q2 (SW) | (5,2) | 28 | D29 / s696 |
| 104564762 | Crop Dusta | SHEEP | Q0 (NW) | (2,4) | 27 | D28 / s672 |
| 104564762 | Crop Dusta | SHEEP | Q0 (NW) | (3,3) | 27 | D28 / s672 |
| 104564762 | Crop Dusta | COW | Q0 (NW) | (3,4) | 28 | D29 / s696 |
| 104564762 | Crop Dusta | COW | Q1 (NE) | (3,5) | 28 | D29 / s696 |
| 104564762 | Crop Dusta | COW | Q1 (NE) | (3,6) | 28 | D29 / s696 |
| 104564762 | Crop Dusta | COW | Q0 (NW) | (4,3) | 28 | D29 / s696 |
| 104564762 | Crop Dusta | COW | Q0 (NW) | (4,4) | 28 | D29 / s696 |
| 104564762 | Crop Dusta | COW | Q1 (NE) | (4,5) | 28 | D29 / s696 |
| 104564762 | Crop Dusta | COW | Q1 (NE) | (4,6) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | SHEEP | Q0 (NW) | (2,0) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | SHEEP | Q0 (NW) | (2,4) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | SHEEP | Q1 (NE) | (2,7) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | SHEEP | Q0 (NW) | (3,3) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | COW | Q1 (NE) | (3,5) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | SHEEP | Q1 (NE) | (3,7) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | COW | Q0 (NW) | (4,3) | 28 | D29 / s696 |
| 104578185 | Crop Dusta | COW | Q1 (NE) | (4,6) | 28 | D29 / s696 |
| 104586335 | Crop Dusta | SHEEP | Q0 (NW) | (2,4) | 27 | D28 / s672 |
| 104586335 | Crop Dusta | SHEEP | Q0 (NW) | (3,3) | 27 | D28 / s672 |
| 104586335 | Crop Dusta | SHEEP | Q1 (NE) | (4,5) | 27 | D28 / s672 |
| 104586335 | Crop Dusta | COW | Q0 (NW) | (4,3) | 28 | D29 / s696 |
| 104586335 | Crop Dusta | COW | Q0 (NW) | (4,4) | 28 | D29 / s696 |

## Artefatti riproducibili

- `docs/model_specs/codex/e17/artifacts/discovery/E17_TOP3_REPLAY_METRICS.json`: provenance, summary, composizioni ed eventi;
- `docs/model_specs/codex/e17/artifacts/discovery/E17_PARTICIPANT_SUMMARY.csv`: una riga per player-seat;
- `docs/model_specs/codex/e17/artifacts/discovery/E17_FINAL_QUADRANT_COMPOSITION.csv`: una riga per player-seat e quadrante;
- `docs/model_specs/codex/e17/artifacts/discovery/E17_QUADRANT_DAILY_TIMELINE.csv`: snapshot giornaliero per specie, player-seat e quadrante;
- `docs/model_specs/codex/e17/artifacts/discovery/E17_ANIMAL_ESCAPE_EVENTS.csv`: audit degli eventi di fuga derivati con coordinate, stato pre/post-EOD e prove FEED/PICKUP;
- `docs/model_specs/codex/e17/tools/analyze_top3_replays.py`: estrattore indipendente Codex.

## Limiti

- `OBSERVED`: reward, stati tile, hands, quadranti e comandi emessi provengono direttamente dai replay.
- `DERIVED`: composizioni, quote move, margini ed eventi di fuga sono calcoli deterministici documentati sopra.
- `UNKNOWN`: il replay non certifica che ogni comando move emesso sia stato eseguito con successo; per questo la metrica è denominata `issued`.
- Il campione è osservazionale, con mercato e avversario condivisi: non identifica da solo l'effetto causale di una singola scelta strategica.
