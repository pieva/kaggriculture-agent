# D20-D30: servizi residui fuori coda

6 casi appaiati contro E18. Delta cassa medio: -968.0 (-1.57%). Nessuna promozione su questo campione di sviluppo.

| Modello | Cassa finale | MOVE D20-D30 | PASS D20-D30 | WATER D20-D30 | Costo manovali D20-D30 | Coltivate: somma checkpoint D20-D30 |
|---|---:|---:|---:|---:|---:|---:|
| E20.1 | 61,571.7 | 1654.3 | 251.3 | 298.0 | 3765.0 | 419.7 |
| E20v31 | 60,603.7 | 1693.7 | 222.0 | 301.3 | 3766.0 | 427.7 |

| Seed | Ruolo | E20.1 | E20v31 | Delta |
|---|---:|---:|---:|---:|
| 180910101 | 1 | 62498.0 | 54473.0 | -8025.0 |
| 180910102 | 1 | 47507.0 | 52646.0 | +5139.0 |
| 180910103 | 1 | 74710.0 | 74692.0 | -18.0 |
| 180910101 | 0 | 62498.0 | 54473.0 | -8025.0 |
| 180910102 | 0 | 47507.0 | 52646.0 | +5139.0 |
| 180910103 | 0 | 74710.0 | 74692.0 | -18.0 |

Decisione: **NOT_ADOPTED**. I due ruoli verificano la simmetria; il campione contiene solo tre seed distinti, gia esposti.

| Modello | Stress colture, partita intera | Fughe animali | FEED D20-D30 | CARE D20-D30 | Vendite D20-D30 |
|---|---:|---:|---:|---:|---:|
| E20.1 | 2.33 | 0.00 | 149.67 | 102.00 | 36788.00 |
| E20v31 | 2.00 | 0.00 | 145.00 | 95.00 | 36333.67 |

Diagnosi E20.1, seed 180910101 ruolo 0: 719 azioni riprodotte esattamente, 209 PASS D20-D30. Nei tentativi associati a 167 PASS viaggio e lavoro superano gia il tempo residuo; in 132 compare un blocco di coda, in 15 mancano materiali, in 2 sono prenotati. Il rientro incide su 10 e il margine di approvvigionamento su 3. Le categorie si sovrappongono e non misurano PASS evitabili.

Soltanto 3 opportunita del lavoratore libero nelle ultime sei ore hanno un servizio preparabile rimuovendo il blocco di coda: D21 H21-H22 e D26 H20. Questo controfattuale locale non garantisce il beneficio della modifica, che puo cambiare anche assegnazioni gia eseguibili e traiettorie successive.

La variante applica la deroga di coda alle offerte di servizio durante l assegnazione, non solo dopo un PASS. Quindi puo anticipare o spostare servizi tra lavoratori. La prova misura questo comportamento complessivo, non un recupero isolato delle tre opportunita.

[Motivi dei rifiuti](DIAGNOSIS_SUMMARY.json) - [Traccia completa](ADMISSION_REASONS.json).

Valutazione: E20v31 non viene adottata. I PASS diminuiscono, ma aumentano gli spostamenti e la cassa media peggiora. Le coltivate aumentano leggermente e lo stress non peggiora: il problema di questa variante e economico, non una regressione biologica. E20.1 pubblicata resta il riferimento.

Il prossimo esperimento dovrebbe verificare il costo dei percorsi e dei rifornimenti prima del finale della giornata. La diagnosi non giustifica togliere il margine di rientro o aggiungere manovali: i rifiuti da soli non dimostrano che queste mosse migliorerebbero la produzione.

Tutte le azioni prima di D20 identiche al controllo. Entrambi gli agenti ricevono 719 chiamate; nessun errore del core E20v31. Missioni attive e controlli di tempo/materiali conservati. D30 conserva il gestore terminale originale. PASS e MOVE sono comandi richiesti; WATER/FEED/CARE sono esecuzioni verificate.

[Protocollo](PROTOCOL.md) - [Dati completi](RESULT.json)
