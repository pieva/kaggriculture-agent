# E17 — benchmark esterno della submission Codex reattiva

## Verdetto sintetico

Il corpus contiene **10 episodi esterni unici**, bilanciati in **5 vittorie e 5 sconfitte**. Lo score medio osservato è **78,808.70**; la media delle sconfitte (**85,154.20**) supera quella delle vittorie (**72,463.20**), quindi lo score assoluto non è una misura autonoma di qualità strategica: forza e interazione dell'avversario sono confondenti rilevanti.

La candidata mantiene una zootecnia Q2 intermedia: tra lo sblocco di Q2 e D28, Q2 vale **63.3%** degli animal-tile-days di Q0. È sotto tetsuya, sopra Crop Dusta e molto sopra OceanMix: non esiste quindi un'unica quota vincente, ma una leva causale da sottoporre ad ablation.

Gli hash completi mostrano **una sola sequenza di comandi richiesta** nei dieci replay, a fronte di **4 traiettorie strutturali eseguite**; la traiettoria dominante ricorre in 7/10 episodi. Le guardie non hanno quindi prodotto una divergenza osservabile dell'action stream in questo campione, ma ciò non prova che la policy non possa reagire in altri stati.

## Protocollo e limiti epistemici

- corpus: replay Kaggle della submission reattiva, ruolo `EXTERNAL_DIAGNOSTIC`;
- clock: giorni e ore zero-based del replay; D29 è separato perché può includere liquidazione terminale;
- stato di farm, tile, denaro, hands e sblocchi: `OBSERVED/EXECUTED_STATE`;
- azioni presenti nel replay: `REQUESTED`, non prova automatica dell'esecuzione;
- fughe: `DERIVED` col criterio EOD stretto condiviso col benchmark Top-3;
- correlazioni e differenze W/L: osservazionali, non effetti causali identificati.

## Risultati per episodio — Pietro Valocchi

| Episodio | Esito | Score | Avversario | Score avv. | Margine | Q1 | Q2 | Hands | Move/attive | Fughe | Crop finali | Animali finali |
|---:|---|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| 104857899 | LOSS | 63,709 | Venneth | 75,505 | -11,796 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104860472 | LOSS | 97,285 | Artyom Sayapin | 111,893 | -14,608 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104863004 | LOSS | 120,014 | seowoohyeon | 124,145 | -4,131 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104863880 | LOSS | 42,850 | tongmian1314 | 44,785 | -1,935 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104864729 | WIN | 68,449 | Jose Santiago Echevarria | 65,424 | 3,025 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104865577 | WIN | 78,228 | Dante Dyches-Chandler | 71,949 | 6,279 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104866465 | WIN | 86,857 | xubenzheng | 66,584 | 20,273 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104867319 | LOSS | 101,913 | Joseph Franck | 110,973 | -9,060 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104868160 | WIN | 83,846 | Operator-X | 55,433 | 28,413 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |
| 104869022 | WIN | 44,936 | SireeshLimbu | 34,785 | 10,151 | D6:H07 | D11:H02 | 10 | 51.8% | 0 | 14 | 19 |

## Confronto vittorie e sconfitte

| Gruppo | N | Score medio | Score avv. | Margine | Q1 mediano (step) | Q2 mediano (step) | Hands | Move/attive | Fughe | Animali Q0/Q1/Q2 da Q2 a D28 | Q2/Q0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| ALL | 10 | 78,808.70 | 76,147.60 | 2,661.10 | 151 | 266 | 10 | 51.8% | 0 | 7.90/6.10/5.00 | 63.3% |
| WIN | 5 | 72,463.20 | 58,835 | 13,628.20 | 151 | 266 | 10 | 51.8% | 0 | 7.80/6.20/5.00 | 64.1% |
| LOSS | 5 | 85,154.20 | 93,460.20 | -8,306 | 151 | 266 | 10 | 51.8% | 0 | 8.00/6.00/5.00 | 62.5% |

## Quota allevamento Q2 per episodio

Le medie coprono ogni giorno dallo sblocco Q2 a D28 incluso. `D28→D29` rende visibile l'eventuale liquidazione terminale.

| Episodio | Esito | Animali medi Q0/Q1/Q2 | Q2/Q0 | Quota Q2 sul totale | Q2 D28→D29 | Crop Q2 D28→D29 | Specie Q2 D28 G/C/S |
|---:|---|---|---:|---:|---:|---:|---|
| 104857899 | LOSS | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104860472 | LOSS | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104863004 | LOSS | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104863880 | LOSS | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104864729 | WIN | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104865577 | WIN | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104866465 | WIN | 7.00/7.00/5.00 | 71.4% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104867319 | LOSS | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104868160 | WIN | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |
| 104869022 | WIN | 8.00/6.00/5.00 | 62.5% | 26.3% | 5→5 | 9→6 | 0/0/5 |

## Confronto con gli archetipi Top-3

Il confronto usa la stessa finestra, lo stesso parser e le stesse definizioni, ma corpus e avversari diversi.

| Agente | Corpus | Episodi | Animali medi Q0/Q1/Q2 | Q2/Q0 | Quota Q2 sul totale 3Q |
|---|---|---:|---|---:|---:|
| Codex reattivo | external diagnostic | 10 | 7.90/6.10/5.00 | 63.3% | 26.3% |
| tetsuya | Top-3 discovery | 4 | 7.00/2.25/5.28 | 75.4% | 36.3% |
| OceanMix | Top-3 discovery | 4 | 7.22/7.00/0.00 | 0.0% | 0.0% |
| Crop Dusta | Top-3 discovery | 5 | 7.03/5.45/2.68 | 38.2% | 17.7% |

## Lettura per E17.2

- `DERIVED`: correlazione esplorativa Q2/Q0–score = **0.115**; Q2/Q0–margine = **0.4432**. Con N=10 e avversari diversi e nove profili Q2 identici, il coefficiente non è interpretabile come segnale causale.
- `OBSERVED/DERIVED`: sono state rilevate **0 fughe**; qualunque riduzione di Q2 deve conservare il gate assoluto di zero fughe.
- `HYPOTHESIS`: una Q2 zootecnica pari a circa due terzi di Q0 può sottrarre tile, servicing e movimento a colture o liquidità senza produrre un ritorno marginale equivalente.
- `HYPOTHESIS`: l'effetto può dipendere dal timing Q2 e dalla contesa; ridurre Q2 non va confuso con ritardare Q2.

### Esperimento raccomandato: reactivity-first

Non variare direttamente il cap zootecnico Q2. Il trattamento successivo deve
essere un controller `MARKET_REGIME_ADAPTATION`, confrontato within-seed
contro regimi avversari controllati: inert, scarsità Wheat, pressione sugli
output e stress di liquidità. La candidata deve emettere azioni diverse quando
cambiano i segnali economici rilevanti e restare deterministica a parità di
stato. Timing, workforce e animal/crop tile-days Q0/Q1/Q2 diventano outcome:
la diversa quota Q2 deve essere una conseguenza motivata della risposta, non
un parametro scelto dal benchmark esterno.

Piano preregistrato:
`experiments/e17/design/E17_CODEX_TRUE_REACTIVITY_ACTIVATION_PLAN_V1.md`.

## Artefatti riproducibili

- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_REPLAY_METRICS.json`;
- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_PARTICIPANTS.csv`;
- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_Q2_LIVESTOCK.csv`;
- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_DAILY_TIMELINE.csv`;
- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_ESCAPE_EVENTS.csv`;
- `experiments/e17/tools/codex/analyze_reactive_external_replays.py`.
