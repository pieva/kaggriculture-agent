# E18 · E19 · E20.2 — torneo e traiettorie dei 22 KPI

42 partite interne complete, 7 seed, tutti gli accoppiamenti e scambio di posizione. E18 = V4D 775; E19 = V48 770; E20.2 = variante congelata 772. Nessuna nuova submission Kaggle.

| Modello | Partite | Vittorie | Cassa media | Mediana | Minimo | Perdite animali |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 28 | 14 | 70.769,5 | 72.848,5 | 33.649,0 | 0 |
| E19 | 28 | 14 | 73.037,1 | 72.727,5 | 42.089,0 | 0 |
| E20.2 | 28 | 14 | 70.864,6 | 70.981,0 | 32.687,0 | 0 |

## Target e topologie osservate

| Modello | Target | Casi esatti | Topologie finali osservate |
|---|---|---:|---|
| E18 | 7–7–5 | 28/28 | 7–7–5: 28 |
| E19 | 7–7–0 | 28/28 | 7–7–0: 28 |
| E20.2 | 7–7–2 | 28/28 | 7–7–2: 28 |

Sono inclusi tutti i casi previsti dal protocollo, anche quelli che non raggiungono la topologia target. La topologia finale non equivale al numero di animali presenti; i pannelli 4–8 mostrano occupazione e strutture vuote.

## Scontri diretti

| Coppia | Partite | Cassa media primo | Cassa media secondo | Delta primo |
|---|---:|---:|---:|---:|
| E18 / E19 | 14 | 72.171,6 | 71.311,9 | 859,7 |
| E18 / E20.2 | 14 | 69.367,3 | 65.828,3 | 3.539,0 |
| E19 / E20.2 | 14 | 74.762,3 | 75.901,0 | -1.138,7 |

## Economia riconciliata

| Modello | Vendite medie | Acquisti medi | Assunzioni medie |
|---|---:|---:|---:|
| E18 | 116.308,9 | 37.856,4 | 7.683,0 |
| E19 | 102.358,2 | 21.836,8 | 7.484,4 |
| E20.2 | 101.425,8 | 23.205,2 | 7.356,0 |

| Prodotto | E18 | E19 | E20.2 |
|---|---:|---:|---:|
| WHEAT | 316,6 unità / 16.720,6 incassi | 324,4 unità / 9.660,6 incassi | 315,9 unità / 8.468,3 incassi |
| MELON | 98,0 unità / 16.275,1 incassi | 72,0 unità / 14.200,5 incassi | 72,0 unità / 14.200,5 incassi |
| STRAWBERRY | 224,5 unità / 35.780,4 incassi | 238,1 unità / 36.267,1 incassi | 242,1 unità / 35.940,8 incassi |
| MILK | 242,0 unità / 13.488,3 incassi | 242,9 unità / 15.314,1 incassi | 252,0 unità / 15.333,4 incassi |
| WOOL | 238,0 unità / 17.094,1 incassi | 127,9 unità / 11.673,0 incassi | 135,6 unità / 12.463,1 incassi |

Unità raccolte e incassi non danno un prezzo unitario esatto: gli incassi possono includere scorte iniziali o altri movimenti; la tabella distingue quantità prodotta da ricavo monetizzato. Il mercato e l’avversario reagiscono alle azioni di entrambi i giocatori.

## Servizi e fragilità operativa

| Modello | PASS medi/giorno | MOVE medi/giorno | WATER riusciti/giorno | FEED riusciti/giorno | CARE riusciti/giorno | Crop→weed dopo stress, media/partita |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 22,8 | 119,9 | 27,8 | 13,3 | 13,2 | 21,9 |
| E19 | 34,8 | 117,1 | 29,6 | 10,6 | 9,4 | 4,6 |
| E20.2 | 33,0 | 117,5 | 28,0 | 11,7 | 9,4 | 2,4 |

Crop→weed segue il diagnostico comune crop_service_audit: transizione osservata al cambio giorno dopo mancata acqua. È un indicatore complementare ai 22 KPI. Il vantaggio economico non implica una riduzione dello stress idrico; i casi individuali restano nei ledger e nel CSV.

## Traiettorie per fase

Ogni riga mostra media D1–D10 → D11–D20 → D21–D30. Per consistenze e cassa sono medie dei checkpoint; per azioni e perdite, medie giornaliere. Il CSV conserva ogni singola traiettoria.

| KPI | E18 | E19 | E20.2 |
|---|---:|---:|---:|
| Cassa | 570,2 → 20.825,7 → 53.172,6 | 570,2 → 21.907,6 → 55.025,5 | 570,2 → 21.583,7 → 54.430,9 |
| Persone | 7,4 → 12,9 → 12,8 | 7,4 → 12,8 → 12,3 | 7,4 → 12,7 → 12,2 |
| Coltivate e terreno sbloccato | 25,4 → 51,2 → 47,3 | 25,4 → 55,8 → 39,0 | 25,4 → 54,1 → 37,3 |
| Animali collocati | 7,2 → 18,3 → 19,0 | 7,2 → 13,7 → 14,0 | 7,2 → 15,6 → 16,0 |
| Mucche | 4,8 → 8,0 → 8,0 | 4,8 → 8,9 → 9,0 | 4,8 → 9,8 → 10,0 |
| Pecore | 2,4 → 9,4 → 10,0 | 2,4 → 4,9 → 5,0 | 2,4 → 5,8 → 6,0 |
| Oche | 0,0 → 0,9 → 1,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Pascoli vuoti | 1,4 → 1,1 → 1,0 | 1,4 → 0,3 → 0,0 | 1,4 → 0,2 → 0,0 |
| Meloni | 12,0 → 7,2 → 1,7 | 12,0 → 0,0 → 0,0 | 12,0 → 0,0 → 0,0 |
| Grano | 6,2 → 12,9 → 22,6 | 6,2 → 20,2 → 15,2 | 6,2 → 19,4 → 15,3 |
| Fragole | 7,2 → 31,1 → 23,0 | 7,2 → 35,5 → 20,1 | 7,2 → 34,7 → 19,5 |
| Carote | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 3,7 | 0,0 → 0,0 → 2,4 |
| Pomodori | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Pollai vuoti | 0,0 → 0,1 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| MOVE | 66,4 → 140,2 → 153,1 | 66,4 → 136,2 → 148,5 | 66,4 → 134,2 → 152,0 |
| PASS | 38,7 → 23,3 → 6,4 | 38,7 → 41,5 → 24,0 | 38,7 → 38,2 → 22,2 |
| Colture non irrigate a H24 | 5,0 → 22,9 → 23,1 | 5,0 → 22,0 → 13,7 | 5,0 → 21,1 → 15,0 |
| Perdite animali verificate | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Infestanti | 0,0 → 0,0 → 1,5 | 0,0 → 0,5 → 8,5 | 0,0 → 0,0 → 8,4 |
| WATER riusciti | 23,6 → 32,6 → 27,2 | 23,6 → 35,8 → 29,3 | 23,6 → 35,0 → 25,4 |
| FEED riusciti | 6,2 → 17,5 → 16,1 | 6,2 → 13,6 → 12,0 | 6,2 → 15,6 → 13,4 |
| CARE riusciti | 7,1 → 18,0 → 14,6 | 7,1 → 12,7 → 8,3 | 7,1 → 13,4 → 7,6 |

## Metodo e limiti

I ledger verificano i saldi contro l’engine a ogni transizione. WATER, FEED e CARE contano esecuzioni riuscite, non richieste. MOVE e PASS seguono la definizione del report comune. Checkpoint 24×D−1: prima dell’ultimo batch D1–D29, terminale D30. La superficie coltivata esclude i pascoli; il pannello 3 include il terreno sbloccato.

Il grafico interattivo presenta mediana puntuale e min–max, sempre due avversari delle stesse partite. Non sono intervalli di confidenza. Gli aggregati complessivi usano due avversari per modello: gli scontri diretti restano la misura più chiara della superiorità relativa. Gli scambi di ruolo non sono nuovi seed indipendenti.

Seed: 180911301, 180911302, 180911303, 180911304, 180911305, 180911306, 180911307. I risultati interni non dimostrano il ranking esterno né una superiorità universale. Consultare il protocollo congelato e il registro development per distinguere tuning e valutazione.

[Dashboard interattiva](REPORT.html) · [Dati aggregati](data.json) · [KPI per partita](daily_kpi.csv)

## Registro degli scontri e dei ruoli

| Seed | Posizione 0 | Cassa 0 | Posizione 1 | Cassa 1 | Esito |
|---|---|---:|---|---:|---|
| 180911301 | E18 | 89.366,0 | E19 | 68.345,0 | E18 |
| 180911302 | E18 | 43.397,0 | E19 | 46.377,0 | E19 |
| 180911303 | E18 | 76.092,0 | E19 | 82.183,0 | E19 |
| 180911304 | E18 | 85.204,0 | E19 | 89.031,0 | E19 |
| 180911305 | E18 | 69.605,0 | E19 | 76.679,0 | E19 |
| 180911306 | E18 | 83.636,0 | E19 | 91.310,0 | E19 |
| 180911307 | E18 | 56.586,0 | E19 | 44.446,0 | E18 |
| 180911301 | E18 | 94.032,0 | E20.2 | 77.837,0 | E18 |
| 180911302 | E18 | 33.649,0 | E20.2 | 33.618,0 | E18 |
| 180911303 | E18 | 67.685,0 | E20.2 | 69.210,0 | E20.2 |
| 180911304 | E18 | 82.241,0 | E20.2 | 85.354,0 | E20.2 |
| 180911305 | E18 | 62.148,0 | E20.2 | 61.605,0 | E18 |
| 180911306 | E18 | 90.005,0 | E20.2 | 87.713,0 | E18 |
| 180911307 | E18 | 55.925,0 | E20.2 | 44.767,0 | E18 |
| 180911301 | E19 | 68.345,0 | E18 | 89.366,0 | E18 |
| 180911302 | E19 | 47.809,0 | E18 | 46.386,0 | E19 |
| 180911303 | E19 | 82.183,0 | E18 | 76.092,0 | E19 |
| 180911304 | E19 | 89.224,0 | E18 | 84.846,0 | E19 |
| 180911305 | E19 | 76.679,0 | E18 | 69.605,0 | E19 |
| 180911306 | E19 | 91.310,0 | E18 | 83.636,0 | E19 |
| 180911307 | E19 | 44.446,0 | E18 | 56.586,0 | E18 |
| 180911301 | E19 | 64.578,0 | E20.2 | 67.478,0 | E20.2 |
| 180911302 | E19 | 42.089,0 | E20.2 | 42.276,0 | E20.2 |
| 180911303 | E19 | 68.021,0 | E20.2 | 66.860,0 | E19 |
| 180911304 | E19 | 90.416,0 | E20.2 | 92.807,0 | E20.2 |
| 180911305 | E19 | 78.155,0 | E20.2 | 77.708,0 | E19 |
| 180911306 | E19 | 110.979,0 | E20.2 | 111.862,0 | E20.2 |
| 180911307 | E19 | 68.776,0 | E20.2 | 71.628,0 | E20.2 |
| 180911301 | E20.2 | 77.837,0 | E18 | 94.032,0 | E18 |
| 180911302 | E20.2 | 32.687,0 | E18 | 33.766,0 | E18 |
| 180911303 | E20.2 | 70.334,0 | E18 | 67.370,0 | E20.2 |
| 180911304 | E20.2 | 86.549,0 | E18 | 82.211,0 | E20.2 |
| 180911305 | E20.2 | 61.605,0 | E18 | 62.148,0 | E18 |
| 180911306 | E20.2 | 87.713,0 | E18 | 90.005,0 | E18 |
| 180911307 | E20.2 | 44.767,0 | E18 | 55.925,0 | E18 |
| 180911301 | E20.2 | 67.478,0 | E19 | 64.578,0 | E20.2 |
| 180911302 | E20.2 | 43.965,0 | E19 | 43.657,0 | E20.2 |
| 180911303 | E20.2 | 66.044,0 | E19 | 68.010,0 | E19 |
| 180911304 | E20.2 | 93.310,0 | E19 | 89.503,0 | E20.2 |
| 180911305 | E20.2 | 77.708,0 | E19 | 78.155,0 | E19 |
| 180911306 | E20.2 | 111.862,0 | E19 | 110.979,0 | E20.2 |
| 180911307 | E20.2 | 71.628,0 | E19 | 68.776,0 | E20.2 |
