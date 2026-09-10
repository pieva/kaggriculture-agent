# E18 · E19 · E20.1 — torneo e traiettorie dei 22 KPI

42 partite interne complete, 7 seed, tutti gli accoppiamenti e scambio di posizione. E18 = V4D 775; E19 = V48 770; E20.1 = variante congelata 772. Nessuna nuova submission Kaggle.

| Modello | Partite | Vittorie | Cassa media | Mediana | Minimo | Perdite animali |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 28 | 20 | 60.978,9 | 59.941,0 | 34.677,0 | 2 |
| E19 | 28 | 13 | 61.443,1 | 53.249,5 | 36.786,0 | 0 |
| E20.1 | 28 | 9 | 59.671,4 | 51.529,0 | 33.991,0 | 0 |

## Target e topologie osservate

| Modello | Target | Casi esatti | Topologie finali osservate |
|---|---|---:|---|
| E18 | 7–7–5 | 28/28 | 7–7–5: 28 |
| E19 | 7–7–0 | 28/28 | 7–7–0: 28 |
| E20.1 | 7–7–2 | 28/28 | 7–7–2: 28 |

Sono inclusi tutti i casi previsti dal protocollo, anche quelli che non raggiungono la topologia target. La topologia finale non equivale al numero di animali presenti; i pannelli 4–8 mostrano occupazione e strutture vuote.

## Scontri diretti

| Coppia | Partite | Cassa media primo | Cassa media secondo | Delta primo |
|---|---:|---:|---:|---:|
| E18 / E19 | 14 | 62.271,9 | 58.398,9 | 3.873,1 |
| E18 / E20.1 | 14 | 59.685,9 | 55.001,9 | 4.684,0 |
| E19 / E20.1 | 14 | 64.487,4 | 64.341,0 | 146,4 |

## Economia riconciliata

| Modello | Vendite medie | Acquisti medi | Assunzioni medie |
|---|---:|---:|---:|
| E18 | 106.186,2 | 37.524,3 | 7.683,0 |
| E19 | 90.611,3 | 21.683,4 | 7.484,8 |
| E20.1 | 90.227,1 | 23.197,2 | 7.358,4 |

| Prodotto | E18 | E19 | E20.1 |
|---|---:|---:|---:|
| WHEAT | 315,9 unità / 16.248,1 incassi | 320,4 unità / 9.194,2 incassi | 317,2 unità / 8.552,5 incassi |
| MELON | 98,0 unità / 16.233,2 incassi | 72,0 unità / 14.200,5 incassi | 72,0 unità / 14.200,5 incassi |
| STRAWBERRY | 223,5 unità / 27.556,0 incassi | 238,8 unità / 28.706,4 incassi | 236,8 unità / 28.194,6 incassi |
| MILK | 241,7 unità / 10.477,1 incassi | 243,2 unità / 12.657,2 incassi | 255,5 unità / 12.352,5 incassi |
| WOOL | 237,6 unità / 18.745,1 incassi | 128,7 unità / 10.183,0 incassi | 144,9 unità / 10.891,9 incassi |

Unità raccolte e incassi non danno un prezzo unitario esatto: gli incassi possono includere scorte iniziali o altri movimenti; la tabella distingue quantità prodotta da ricavo monetizzato. Il mercato e l’avversario reagiscono alle azioni di entrambi i giocatori.

## Conferma indipendente E20.1

E20.1 è E20v28: inserimento dei tile lontani prima di quelli vicini a parità di priorità, più filtro dei CARE senza produzione incrementale possibile. Apertura D1–D11 e topologia target 7–7–2 restano le stesse. I sette seed sono stati riservati prima degli esperimenti; nessuna modifica della candidata dopo il congelamento.

Contro lo stesso E18: cassa media 55.001,9 contro 58.398,9 di E19 (-5,8%). Seed positivi: 1/7; mediana delle differenze per seed -3.442,0. Stress colture 3,8 contro 4,7; perdite animali 0. Gate indipendente: NON superato.

Il confronto appaiato e la classifica del torneo misurano cose diverse: il primo mantiene fisso l’avversario, la seconda include due avversari per modello. [Dettagli appaiati](../e20_1/confirmation/REPORT.md).

## Servizi e fragilità operativa

| Modello | PASS medi/giorno | MOVE medi/giorno | WATER riusciti/giorno | FEED riusciti/giorno | CARE riusciti/giorno | Crop→weed dopo stress, media/partita |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 22,9 | 119,9 | 27,8 | 13,2 | 13,2 | 21,9 |
| E19 | 35,4 | 116,5 | 29,5 | 10,6 | 9,4 | 4,7 |
| E20.1 | 33,1 | 117,0 | 28,1 | 11,7 | 9,8 | 3,6 |

Crop→weed segue il diagnostico comune crop_service_audit: transizione osservata al cambio giorno dopo mancata acqua. È un indicatore complementare ai 22 KPI. Il vantaggio economico non implica una riduzione dello stress idrico; i casi individuali restano nei ledger e nel CSV.

## Traiettorie per fase

Ogni riga mostra media D1–D10 → D11–D20 → D21–D30. Per consistenze e cassa sono medie dei checkpoint; per azioni e perdite, medie giornaliere. Il CSV conserva ogni singola traiettoria.

| KPI | E18 | E19 | E20.1 |
|---|---:|---:|---:|
| Cassa | 551,4 → 18.794,9 → 44.956,0 | 551,4 → 20.157,2 → 45.978,1 | 551,4 → 19.376,3 → 44.841,9 |
| Persone | 7,4 → 12,9 → 12,8 | 7,4 → 12,8 → 12,3 | 7,4 → 12,8 → 12,2 |
| Coltivate e terreno sbloccato | 25,4 → 51,2 → 47,3 | 25,4 → 55,7 → 39,1 | 25,4 → 54,1 → 37,1 |
| Animali collocati | 7,2 → 18,3 → 19,0 | 7,2 → 13,8 → 14,0 | 7,2 → 15,6 → 16,0 |
| Mucche | 4,8 → 8,0 → 8,0 | 4,8 → 8,9 → 9,0 | 4,8 → 9,8 → 10,0 |
| Pecore | 2,4 → 9,4 → 10,0 | 2,4 → 4,9 → 5,0 | 2,4 → 5,8 → 6,0 |
| Oche | 0,0 → 0,9 → 1,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Pascoli vuoti | 1,4 → 1,1 → 1,0 | 1,4 → 0,2 → 0,0 | 1,4 → 0,2 → 0,0 |
| Meloni | 12,0 → 7,2 → 1,7 | 12,0 → 0,0 → 0,0 | 12,0 → 0,0 → 0,0 |
| Grano | 6,2 → 12,9 → 22,6 | 6,2 → 20,2 → 15,1 | 6,2 → 19,4 → 15,2 |
| Fragole | 7,2 → 31,1 → 23,0 | 7,2 → 35,5 → 20,3 | 7,2 → 34,7 → 19,0 |
| Carote | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 3,7 | 0,0 → 0,0 → 2,9 |
| Pomodori | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Pollai vuoti | 0,0 → 0,1 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| MOVE | 66,4 → 140,2 → 153,1 | 66,4 → 135,8 → 147,2 | 66,4 → 134,3 → 150,3 |
| PASS | 38,7 → 23,3 → 6,6 | 38,7 → 42,1 → 25,5 | 38,7 → 38,1 → 22,6 |
| Colture non irrigate a H24 | 5,0 → 22,9 → 23,1 | 5,0 → 22,0 → 14,0 | 5,0 → 21,0 → 14,6 |
| Perdite animali verificate | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Infestanti | 0,0 → 0,0 → 1,6 | 0,0 → 0,6 → 8,8 | 0,0 → 0,0 → 8,4 |
| WATER riusciti | 23,6 → 32,6 → 27,2 | 23,6 → 35,7 → 29,1 | 23,6 → 35,0 → 25,6 |
| FEED riusciti | 6,2 → 17,5 → 16,1 | 6,2 → 13,6 → 12,0 | 6,2 → 15,6 → 13,2 |
| CARE riusciti | 7,1 → 18,0 → 14,6 | 7,1 → 12,7 → 8,4 | 7,1 → 13,7 → 8,7 |

## Metodo e limiti

I ledger verificano i saldi contro l’engine a ogni transizione. WATER, FEED e CARE contano esecuzioni riuscite, non richieste. MOVE e PASS seguono la definizione del report comune. Checkpoint 24×D−1: prima dell’ultimo batch D1–D29, terminale D30. La superficie coltivata esclude i pascoli; il pannello 3 include il terreno sbloccato.

Il grafico interattivo presenta mediana puntuale e min–max, sempre due avversari delle stesse partite. Non sono intervalli di confidenza. Gli aggregati complessivi usano due avversari per modello: gli scontri diretti restano la misura più chiara della superiorità relativa. Gli scambi di ruolo non sono nuovi seed indipendenti.

Seed: 180910201, 180910202, 180910203, 180910204, 180910205, 180910206, 180910207. I risultati interni non dimostrano il ranking esterno né una superiorità universale. Consultare il protocollo congelato e il registro development per distinguere tuning e valutazione.

[Dashboard interattiva](REPORT.html) · [Dati aggregati](data.json) · [KPI per partita](daily_kpi.csv)

## Registro degli scontri e dei ruoli

| Seed | Posizione 0 | Cassa 0 | Posizione 1 | Cassa 1 | Esito |
|---|---|---:|---|---:|---|
| 180910201 | E18 | 43.673,0 | E19 | 38.856,0 | E18 |
| 180910202 | E18 | 74.814,0 | E19 | 51.290,0 | E18 |
| 180910203 | E18 | 38.765,0 | E19 | 43.568,0 | E19 |
| 180910204 | E18 | 97.067,0 | E19 | 95.881,0 | E18 |
| 180910205 | E18 | 60.896,0 | E19 | 60.358,0 | E18 |
| 180910206 | E18 | 73.424,0 | E19 | 79.850,0 | E19 |
| 180910207 | E18 | 59.219,0 | E19 | 52.887,0 | E18 |
| 180910201 | E18 | 50.035,0 | E20.1 | 43.717,0 | E18 |
| 180910202 | E18 | 61.532,0 | E20.1 | 45.594,0 | E18 |
| 180910203 | E18 | 34.677,0 | E20.1 | 37.365,0 | E20.1 |
| 180910204 | E18 | 101.964,0 | E20.1 | 95.528,0 | E18 |
| 180910205 | E18 | 39.036,0 | E20.1 | 33.991,0 | E18 |
| 180910206 | E18 | 72.991,0 | E20.1 | 78.523,0 | E20.1 |
| 180910207 | E18 | 45.472,0 | E20.1 | 37.517,0 | E18 |
| 180910201 | E19 | 36.786,0 | E18 | 41.686,0 | E18 |
| 180910202 | E19 | 50.726,0 | E18 | 73.358,0 | E18 |
| 180910203 | E19 | 40.734,0 | E18 | 39.025,0 | E19 |
| 180910204 | E19 | 95.881,0 | E18 | 97.067,0 | E18 |
| 180910205 | E19 | 38.001,0 | E18 | 40.432,0 | E18 |
| 180910206 | E19 | 79.850,0 | E18 | 73.424,0 | E19 |
| 180910207 | E19 | 52.916,0 | E18 | 58.957,0 | E18 |
| 180910201 | E19 | 47.209,0 | E20.1 | 48.982,0 | E20.1 |
| 180910202 | E19 | 58.458,0 | E20.1 | 59.595,0 | E20.1 |
| 180910203 | E19 | 43.432,0 | E20.1 | 44.371,0 | E20.1 |
| 180910204 | E19 | 103.637,0 | E20.1 | 103.628,0 | E19 |
| 180910205 | E19 | 53.583,0 | E20.1 | 53.520,0 | E19 |
| 180910206 | E19 | 88.166,0 | E20.1 | 86.961,0 | E19 |
| 180910207 | E19 | 60.075,0 | E20.1 | 57.156,0 | E19 |
| 180910201 | E20.1 | 43.717,0 | E18 | 50.035,0 | E18 |
| 180910202 | E20.1 | 49.538,0 | E18 | 60.663,0 | E18 |
| 180910203 | E20.1 | 37.365,0 | E18 | 34.677,0 | E20.1 |
| 180910204 | E20.1 | 95.528,0 | E18 | 101.964,0 | E18 |
| 180910205 | E20.1 | 55.505,0 | E18 | 63.126,0 | E18 |
| 180910206 | E20.1 | 78.523,0 | E18 | 72.991,0 | E20.1 |
| 180910207 | E20.1 | 37.615,0 | E18 | 46.439,0 | E18 |
| 180910201 | E20.1 | 45.905,0 | E19 | 44.296,0 | E20.1 |
| 180910202 | E20.1 | 62.141,0 | E19 | 57.446,0 | E20.1 |
| 180910203 | E20.1 | 43.927,0 | E19 | 45.129,0 | E19 |
| 180910204 | E20.1 | 103.628,0 | E19 | 103.637,0 | E19 |
| 180910205 | E20.1 | 45.874,0 | E19 | 49.231,0 | E19 |
| 180910206 | E20.1 | 86.961,0 | E19 | 88.166,0 | E19 |
| 180910207 | E20.1 | 58.125,0 | E19 | 60.358,0 | E19 |
