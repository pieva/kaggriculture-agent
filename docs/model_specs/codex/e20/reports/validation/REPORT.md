# E18 · E19 · E20 — torneo e traiettorie dei 22 KPI

6 partite interne complete, 3 seed, tutti gli accoppiamenti e scambio di posizione. E18 = V4D 775; E19 = V48 770; E20 = variante congelata 772. Nessuna nuova submission Kaggle.

| Modello | Partite | Vittorie | Cassa media | Mediana | Minimo | Perdite animali |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 6 | 0 | 91.248,3 | 95.747,0 | 67.892,0 | 0 |
| E20 | 6 | 6 | 96.405,3 | 101.638,0 | 68.986,0 | 0 |

## Target e topologie osservate

| Modello | Target | Casi esatti | Topologie finali osservate |
|---|---|---:|---|
| E18 | 7–7–5 | 6/6 | 7–7–5: 6 |
| E20 | 7–7–2 | 6/6 | 7–7–2: 6 |

Sono inclusi tutti i casi previsti dal protocollo, anche quelli che non raggiungono la topologia target. La topologia finale non equivale al numero di animali presenti; i pannelli 4–8 mostrano occupazione e strutture vuote.

## Scontri diretti

| Coppia | Partite | Cassa media primo | Cassa media secondo | Delta primo |
|---|---:|---:|---:|---:|
| E18 / E20 | 6 | 91.248,3 | 96.405,3 | -5.157,0 |

## Economia riconciliata

| Modello | Vendite medie | Acquisti medi | Assunzioni medie |
|---|---:|---:|---:|
| E18 | 136.864,7 | 37.933,3 | 7.683,0 |
| E20 | 127.967,0 | 24.244,3 | 7.317,3 |

## Servizi e fragilità operativa

| Modello | PASS medi/giorno | MOVE medi/giorno | WATER riusciti/giorno | FEED riusciti/giorno | CARE riusciti/giorno | Crop→weed dopo stress, media/partita |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 23,0 | 119,7 | 27,8 | 13,3 | 13,2 | 22,0 |
| E20 | 32,3 | 117,2 | 27,9 | 11,8 | 10,6 | 10,0 |

Crop→weed segue il diagnostico comune crop_service_audit: transizione osservata al cambio giorno dopo mancata acqua. È un indicatore complementare ai 22 KPI. Il vantaggio economico non implica una riduzione dello stress idrico; i casi individuali restano nei ledger e nel CSV.

## Traiettorie per fase

Ogni riga mostra media D1–D10 → D11–D20 → D21–D30. Per consistenze e cassa sono medie dei checkpoint; per azioni e perdite, medie giornaliere. Il CSV conserva ogni singola traiettoria.

| KPI | E18 | E20 |
|---|---:|---:|
| Cassa | 558,4 → 21.954,3 → 63.699,8 | 558,4 → 22.464,9 → 66.886,7 |
| Persone | 7,4 → 12,9 → 12,8 | 7,4 → 12,7 → 12,3 |
| Coltivate e terreno sbloccato | 25,4 → 51,2 → 47,3 | 25,4 → 54,4 → 35,5 |
| Animali collocati | 7,2 → 18,3 → 19,0 | 7,2 → 15,6 → 16,0 |
| Mucche | 4,8 → 8,0 → 8,0 | 4,8 → 9,8 → 10,0 |
| Pecore | 2,4 → 9,4 → 10,0 | 2,4 → 5,8 → 6,0 |
| Oche | 0,0 → 0,9 → 1,0 | 0,0 → 0,0 → 0,0 |
| Pascoli vuoti | 1,4 → 1,1 → 1,0 | 1,4 → 0,2 → 0,0 |
| Meloni | 12,0 → 7,2 → 1,7 | 12,0 → 0,0 → 0,0 |
| Grano | 6,2 → 12,9 → 22,6 | 6,2 → 19,5 → 13,1 |
| Fragole | 7,2 → 31,1 → 23,0 | 7,2 → 34,9 → 20,3 |
| Carote | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 2,1 |
| Pomodori | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Pollai vuoti | 0,0 → 0,1 → 0,0 | 0,0 → 0,0 → 0,0 |
| MOVE | 66,4 → 140,2 → 152,4 | 66,4 → 132,2 → 153,0 |
| PASS | 38,7 → 23,3 → 7,1 | 38,7 → 38,5 → 19,7 |
| Colture non irrigate a H24 | 5,0 → 22,9 → 23,1 | 5,0 → 21,5 → 14,2 |
| Perdite animali verificate | 0,0 → 0,0 → 0,0 | 0,0 → 0,0 → 0,0 |
| Infestanti | 0,0 → 0,0 → 1,5 | 0,0 → 0,8 → 11,9 |
| WATER riusciti | 23,6 → 32,6 → 27,2 | 23,6 → 35,1 → 25,1 |
| FEED riusciti | 6,2 → 17,5 → 16,1 | 6,2 → 15,5 → 13,7 |
| CARE riusciti | 7,1 → 18,0 → 14,6 | 7,1 → 14,8 → 9,8 |

## Metodo e limiti

I ledger verificano i saldi contro l’engine a ogni transizione. WATER, FEED e CARE contano esecuzioni riuscite, non richieste. MOVE e PASS seguono la definizione del report comune. Checkpoint 24×D−1: prima dell’ultimo batch D1–D29, terminale D30. La superficie coltivata esclude i pascoli; il pannello 3 include il terreno sbloccato.

Il grafico interattivo presenta mediana puntuale e min–max, sempre due avversari delle stesse partite. Non sono intervalli di confidenza. Gli aggregati complessivi usano due avversari per modello: gli scontri diretti restano la misura più chiara della superiorità relativa. Gli scambi di ruolo non sono nuovi seed indipendenti.

Seed: 180903001, 180903002, 180903003. I risultati interni non dimostrano il ranking esterno né una superiorità universale. Consultare il protocollo congelato e il registro development per distinguere tuning e valutazione.

[Dashboard interattiva](REPORT.html) · [Dati aggregati](data.json) · [KPI per partita](daily_kpi.csv)
