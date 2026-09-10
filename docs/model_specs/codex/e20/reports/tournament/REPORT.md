# E18 · E19 · E20 — torneo e traiettorie dei 22 KPI

42 partite interne complete, 7 seed, tutti gli accoppiamenti e scambio di posizione. E18 = V4D 775; E19 = V48 770; E20 = variante congelata 772. Nessuna nuova submission Kaggle.

| Modello | Partite | Vittorie | Cassa media | Mediana | Minimo | Perdite animali |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 28 | 20 | 67.047,4 | 67.001,5 | 39.302,0 | 5 |
| E19 | 28 | 15 | 70.452,5 | 74.657,0 | 44.679,0 | 0 |
| E20 | 28 | 7 | 67.513,5 | 73.431,0 | 35.407,0 | 0 |

## Target e topologie osservate

| Modello | Target | Casi esatti | Topologie finali osservate |
|---|---|---:|---|
| E18 | 7–7–5 | 26/28 | 6–7–5: 2; 7–7–5: 26 |
| E19 | 7–7–0 | 26/28 | 6–7–0: 2; 7–7–0: 26 |
| E20 | 7–7–2 | 27/28 | 6–7–2: 1; 7–7–2: 27 |

Sono inclusi tutti i casi previsti dal protocollo, anche quelli che non raggiungono la topologia target. La topologia finale non equivale al numero di animali presenti; i pannelli 4–8 mostrano occupazione e strutture vuote.

## Scontri diretti

| Coppia | Partite | Cassa media primo | Cassa media secondo | Delta primo |
|---|---:|---:|---:|---:|
| E18 / E19 | 14 | 68.762,7 | 63.921,0 | 4.841,7 |
| E18 / E20 | 14 | 65.332,1 | 61.943,1 | 3.389,0 |
| E19 / E20 | 14 | 76.984,1 | 73.084,0 | 3.900,1 |

## Economia riconciliata

| Modello | Vendite medie | Acquisti medi | Assunzioni medie |
|---|---:|---:|---:|
| E18 | 112.794,4 | 38.064,0 | 7.683,0 |
| E19 | 99.553,4 | 21.659,7 | 7.441,2 |
| E20 | 98.919,5 | 24.086,6 | 7.319,4 |

| Prodotto | E18 | E19 | E20 |
|---|---:|---:|---:|
| WHEAT | 316,5 unità / 16.866,5 incassi | 330,8 unità / 9.898,7 incassi | 301,6 unità / 8.508,1 incassi |
| MELON | 98,0 unità / 16.240,6 incassi | 72,0 unità / 14.200,5 incassi | 72,0 unità / 14.200,5 incassi |
| STRAWBERRY | 223,0 unità / 33.793,5 incassi | 239,0 unità / 35.919,2 incassi | 230,3 unità / 36.262,2 incassi |
| MILK | 241,4 unità / 14.154,0 incassi | 242,5 unità / 14.622,4 incassi | 269,3 unità / 15.679,0 incassi |
| WOOL | 237,2 unità / 14.927,3 incassi | 126,6 unità / 10.109,9 incassi | 149,9 unità / 9.308,9 incassi |

Unità raccolte e incassi non danno un prezzo unitario esatto: gli incassi possono includere scorte iniziali o altri movimenti; la tabella distingue quantità prodotta da ricavo monetizzato. Il mercato e l’avversario reagiscono alle azioni di entrambi i giocatori.

## Dalla selezione al torneo

La candidata E20v18 era stata congelata dopo un vantaggio medio del 4,6% su E19 nei sei casi development. La policy del torneo conserva lo stesso hash; i sette seed di torneo non sono stati usati per scegliere la variante.

A parità di avversario E18, seed e ruolo, E20 chiude a 61.943,1 contro 63.921,0 di E19: delta -1.977,9 (-3,1%), positivo in 2/14 casi. È una conferma separata dalla classifica complessiva, che mescola due avversari per modello.

| Seed | E19 contro E18 | E20 contro E18 | Delta E20 |
|---|---:|---:|---:|
| 180910101 | 46.548,0 | 38.570,0 | -7.978,0 |
| 180910102 | 44.679,0 | 35.407,0 | -9.272,0 |
| 180910103 | 74.657,0 | 69.892,0 | -4.765,0 |
| 180910104 | 54.250,0 | 43.374,5 | -10.875,5 |
| 180910105 | 78.106,0 | 73.431,0 | -4.675,0 |
| 180910106 | 92.703,0 | 86.867,0 | -5.836,0 |
| 180910107 | 56.504,0 | 86.060,0 | 29.556,0 |

Ogni riga media i due ruoli dello stesso seed. Il seed è l’unità indipendente: quattordici confronti non equivalgono a quattordici scenari. Il mercato evolve in risposta alle due policy; il confronto fissa condizioni iniziali e avversario, non l’intera traiettoria dei prezzi.

Sulle stesse condizioni contro E18, E20 cambia il carico medio stagionale rispetto a E19: PASS -79,0, MOVE 29,6, FEED 37,0, CARE 35,4, WATER -53,5. Le transizioni crop→weed dopo stress passano da 3,5 a 9,6 per partita.

Questa combinazione segnala una competizione fra allevamento e servizio delle colture. Non è una prova causale isolata: la variante cambia anche rotte, raccolti e prezzi. La riduzione dei PASS non basta a dimostrare un miglioramento economico.

## Lettura delle traiettorie

D1–D11: l’avvio E20 riproduce E19. L’espansione iniziale di manodopera, colture e bestiame va letta insieme ai gradini del terreno nel pannello 3. D12 introduce i due pascoli Q2: il confronto fra pannelli 4–8 e FEED/CARE permette di distinguere capacità costruita, animali presenti e servizio effettivo.

D12–D20: le nuove risorse competono con l’irrigazione e con i viaggi. Più animali non garantiscono più margine: contano raccolto, prezzo di vendita e costo del grano acquistato. I pannelli 9–13 mostrano il mix di colture; MOVE/PASS vanno letti insieme ai servizi riusciti, senza considerare ogni riduzione dei PASS un miglioramento.

D21–D30: cassa e superficie coltivata descrivono raccolti e chiusura. Il calo terminale di colture o personale non identifica da solo una perdita: va confrontato con le vendite e con il calendario biologico. I pannelli 17–19 e la tabella seguente segnalano invece la fragilità idrica e le perdite.

## Servizi e fragilità operativa

| Modello | PASS medi/giorno | MOVE medi/giorno | WATER riusciti/giorno | FEED riusciti/giorno | CARE riusciti/giorno | Crop→weed dopo stress, media/partita |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 22,9 | 119,9 | 27,7 | 13,2 | 13,2 | 22,0 |
| E19 | 35,3 | 115,9 | 29,7 | 10,5 | 9,4 | 3,4 |
| E20 | 32,4 | 117,1 | 28,0 | 11,7 | 10,5 | 9,5 |

Crop→weed segue il diagnostico comune crop_service_audit: transizione osservata al cambio giorno dopo mancata acqua. È un indicatore complementare ai 22 KPI. Il vantaggio economico non implica una riduzione dello stress idrico; i casi individuali restano nei ledger e nel CSV.

## Traiettorie per fase

Ogni riga mostra media D1–D10 → D11–D20 → D21–D30. Per consistenze e cassa sono medie dei checkpoint; per azioni e perdite, medie giornaliere. Il CSV conserva ogni singola traiettoria.

| KPI | E18 | E19 | E20 |
|---|---:|---:|---:|
| Cassa | 571,0 → 21.122,2 → 50.486,3 | 571,0 → 22.431,2 → 53.530,4 | 571,0 → 21.586,9 → 51.451,7 |
| Persone | 7,4 → 12,9 → 12,8 | 7,4 → 12,8 → 12,3 | 7,4 → 12,7 → 12,3 |
| Coltivate e terreno sbloccato | 25,3 → 51,0 → 47,1 | 25,3 → 56,5 → 39,9 | 25,3 → 54,4 → 35,7 |
| Animali collocati | 7,2 → 18,3 → 18,9 | 7,2 → 13,6 → 13,9 | 7,2 → 15,5 → 16,0 |
| Mucche | 4,8 → 8,0 → 8,0 | 4,8 → 8,9 → 9,0 | 4,8 → 9,8 → 10,0 |
| Pecore | 2,4 → 9,4 → 9,9 | 2,4 → 4,8 → 4,9 | 2,4 → 5,7 → 6,0 |
| Oche | 0,0 → 0,9 → 1,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Pascoli vuoti | 1,4 → 1,0 → 1,0 | 1,4 → 0,3 → 0,0 | 1,4 → 0,2 → 0,0 |
| Meloni | 12,0 → 7,2 → 1,7 | 12,0 → 0,0 → 0,0 | 12,0 → 0,0 → 0,0 |
| Grano | 6,2 → 12,9 → 22,6 | 6,2 → 20,7 → 15,9 | 6,2 → 19,5 → 13,3 |
| Fragole | 7,1 → 30,9 → 22,8 | 7,1 → 35,8 → 20,8 | 7,1 → 34,9 → 20,3 |
| Carote | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 3,2 | 0,0 → 0,0 → 2,2 |
| Pomodori | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Pollai vuoti | 0,0 → 0,1 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| MOVE | 66,4 → 140,2 → 153,0 | 66,4 → 133,9 → 147,4 | 66,4 → 132,2 → 152,6 |
| PASS | 38,7 → 23,3 → 6,6 | 38,7 → 42,8 → 24,3 | 38,7 → 38,7 → 19,9 |
| Colture non irrigate a H24 | 5,0 → 22,8 → 23,0 | 5,0 → 22,3 → 14,8 | 5,0 → 21,5 → 14,3 |
| Perdite animali verificate | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Infestanti | 0,1 → 0,1 → 1,7 | 0,1 → 0,3 → 7,8 | 0,1 → 0,7 → 11,6 |
| WATER riusciti | 23,6 → 32,5 → 27,1 | 23,6 → 36,1 → 29,3 | 23,6 → 35,1 → 25,2 |
| FEED riusciti | 6,2 → 17,5 → 16,1 | 6,2 → 13,6 → 11,8 | 6,2 → 15,5 → 13,6 |
| CARE riusciti | 7,1 → 18,0 → 14,6 | 7,1 → 12,6 → 8,4 | 7,1 → 14,8 → 9,7 |

## Metodo e limiti

I ledger verificano i saldi contro l’engine a ogni transizione. WATER, FEED e CARE contano esecuzioni riuscite, non richieste. MOVE e PASS seguono la definizione del report comune. Checkpoint 24×D−1: prima dell’ultimo batch D1–D29, terminale D30. La superficie coltivata esclude i pascoli; il pannello 3 include il terreno sbloccato.

Il grafico interattivo presenta mediana puntuale e min–max, sempre due avversari delle stesse partite. Non sono intervalli di confidenza. Gli aggregati complessivi usano due avversari per modello: gli scontri diretti restano la misura più chiara della superiorità relativa. Gli scambi di ruolo non sono nuovi seed indipendenti.

Seed: 180910101, 180910102, 180910103, 180910104, 180910105, 180910106, 180910107. I risultati interni non dimostrano il ranking esterno né una superiorità universale. Consultare il protocollo congelato e il registro development per distinguere tuning e valutazione.

[Dashboard interattiva](REPORT.html) · [Dati aggregati](data.json) · [KPI per partita](daily_kpi.csv)

## Registro degli scontri e dei ruoli

| Seed | Posizione 0 | Cassa 0 | Posizione 1 | Cassa 1 | Esito |
|---|---|---:|---|---:|---|
| 180910101 | E18 | 42.240,0 | E19 | 46.548,0 | E19 |
| 180910102 | E18 | 55.568,0 | E19 | 44.679,0 | E18 |
| 180910103 | E18 | 75.678,0 | E19 | 74.657,0 | E18 |
| 180910104 | E18 | 65.141,0 | E19 | 59.003,0 | E18 |
| 180910105 | E18 | 77.933,0 | E19 | 78.106,0 | E19 |
| 180910106 | E18 | 115.697,0 | E19 | 92.703,0 | E18 |
| 180910107 | E18 | 56.642,0 | E19 | 56.504,0 | E18 |
| 180910101 | E18 | 41.110,0 | E20 | 38.570,0 | E18 |
| 180910102 | E18 | 42.095,0 | E20 | 35.407,0 | E18 |
| 180910103 | E18 | 68.862,0 | E20 | 69.892,0 | E20 |
| 180910104 | E18 | 57.941,0 | E20 | 49.566,0 | E18 |
| 180910105 | E18 | 75.164,0 | E20 | 73.431,0 | E18 |
| 180910106 | E18 | 95.520,0 | E20 | 86.867,0 | E18 |
| 180910107 | E18 | 85.952,0 | E20 | 86.060,0 | E20 |
| 180910101 | E19 | 46.548,0 | E18 | 42.240,0 | E19 |
| 180910102 | E19 | 44.679,0 | E18 | 55.568,0 | E18 |
| 180910103 | E19 | 74.657,0 | E18 | 75.678,0 | E18 |
| 180910104 | E19 | 49.497,0 | E18 | 50.021,0 | E18 |
| 180910105 | E19 | 78.106,0 | E18 | 77.933,0 | E19 |
| 180910106 | E19 | 92.703,0 | E18 | 115.697,0 | E18 |
| 180910107 | E19 | 56.504,0 | E18 | 56.642,0 | E18 |
| 180910101 | E19 | 63.776,0 | E20 | 56.571,0 | E19 |
| 180910102 | E19 | 54.070,0 | E20 | 48.378,0 | E19 |
| 180910103 | E19 | 77.690,0 | E20 | 74.856,0 | E19 |
| 180910104 | E19 | 75.873,0 | E20 | 77.019,0 | E20 |
| 180910105 | E19 | 84.040,0 | E20 | 77.822,0 | E19 |
| 180910106 | E19 | 102.682,0 | E20 | 104.880,0 | E20 |
| 180910107 | E19 | 86.511,0 | E20 | 81.776,0 | E19 |
| 180910101 | E20 | 38.570,0 | E18 | 41.110,0 | E18 |
| 180910102 | E20 | 35.407,0 | E18 | 42.095,0 | E18 |
| 180910103 | E20 | 69.892,0 | E18 | 68.862,0 | E20 |
| 180910104 | E20 | 37.183,0 | E18 | 39.302,0 | E18 |
| 180910105 | E20 | 73.431,0 | E18 | 75.164,0 | E18 |
| 180910106 | E20 | 86.867,0 | E18 | 95.520,0 | E18 |
| 180910107 | E20 | 86.060,0 | E18 | 85.952,0 | E20 |
| 180910101 | E20 | 56.571,0 | E19 | 63.776,0 | E19 |
| 180910102 | E20 | 48.378,0 | E19 | 54.070,0 | E19 |
| 180910103 | E20 | 74.856,0 | E19 | 77.690,0 | E19 |
| 180910104 | E20 | 57.591,0 | E19 | 64.366,0 | E19 |
| 180910105 | E20 | 77.822,0 | E19 | 84.040,0 | E19 |
| 180910106 | E20 | 104.880,0 | E19 | 102.682,0 | E20 |
| 180910107 | E20 | 81.776,0 | E19 | 86.511,0 | E19 |
