# Pascoli degli avversari E22: tipologie e traiettorie

Analisi dei 20 replay E22 disponibili nel campione congelato di 78 partite. Tutti gli avversari sono inventariati; i sei con pascoli su tutte e tre le coordinate Q0 hanno estrazione dettagliata. Non sono 78 replay analizzati né repliche multiple della stessa submission. Le azioni di servizio sono riapplicate su copie dello stato precedente per distinguere esiti effettivi e richieste senza effetto. Le traiettorie usano coordinate zero-based e D/H visuali one-based; operaio 0 = fattore. Nessun codice sorgente degli avversari è stato recuperato.

| Submission | Episodio | Mix finale | Pollaio Q2 | Margine su E22 | Fughe |
|---|---|---|---|---:|---:|
| 56020742 | 108544555 | {'SHEEP': 8, 'COW': 9} | False | -7,243 | 0 |
| 56124096 | 108549619 | {'SHEEP': 11, 'COW': 5} | True | +10,234 | 0 |
| 56171606 | 108558711 | {'SHEEP': 10, 'COW': 6} | True | +23,731 | 1 |
| 56165125 | 108561064 | {'SHEEP': 10, 'COW': 6} | True | +8,990 | 0 |
| 56198022 | 108562089 | {'SHEEP': 14, 'COW': 7, 'GOOSE': 2} | False | +24,117 | 0 |
| 56205921 | 108575585 | {'SHEEP': 10, 'COW': 6} | True | +56,815 | 0 |

## Costruzioni e collocamenti nelle tre coordinate

Il motore ha un unico tipo PASTURE, utilizzabile da mucche o pecore: le tipologie osservate sono differenze di occupazione, mix e calendario. Tutti e sei i casi costruiscono (2,3) a D11 H15 e collocano la pecora a D12 H7. (3,2) viene costruito a D11 H18–19 e popolato a H19–20; (4,1) a H19–20, popolato a H20–21 in quattro casi e mai popolato negli altri due.

La regola di raccolta si ripete in tutti i casi popolati: (3,2) e (4,1) a D17/20/23/26/29; (2,3) a D18/21/24/27/30. La prima raccolta rende 5–6 lane nei casi osservati; le successive spesso 4, ma scendono a 3 e in un caso a 1 quando il servizio diverge. Quindi è riproducibile il calendario relativo (età 6 giorni, poi ogni 3); la resa richiede verifica di alimentazione e cure.

56165125 e 56205921 condividono tutte le 186 richieste di servizio sulle tre coordinate con identici giorno, ora, operazione, efficacia e quantità (62 in (4,1), 66 in (3,2), 58 in (2,3)); (4,1) resta sempre vuoto. Le azioni complete di tutti gli operai coincidono solo in 455/719 turni, le azioni complete incluse le transazioni in 420/719: il modulo Q0 è stabile, il piano globale no. I loro margini osservati su E22 sono +8.990 e +56.815: la stessa traiettoria Q0 non spiega da sola il risultato economico.

56171606 popola anche (4,1), ma perde una pecora in (5,2) alla transizione D10: il suo 6C10S finale non equivale al 6C10S con pascolo vuoto. 56124096 usa 5C11S; 56020742 9C8S; 56198022 espande oltre le tre caselle e chiude 7C14S2G. Manca la ripetizione della stessa submission su più seed nel campione disponibile: questa è evidenza di un modulo condiviso tra replay, non prova di robustezza del codice.

Trasferimento consigliato: riusare collocamenti e cicli produttivi con controlli sullo stato; tenere separati 8C9S e replica 6C10S. Non riprodurre le alimentazioni fallite: nei due casi con pascolo vuoto (3,2) non riceve FEED efficace a D14/26/29 e (2,3) a D14/25. Il template osservato è in OBSERVED_TEMPLATE.json, i percorsi di tutti gli operai nei JSON per episodio.

### Submission 56020742 · episodio 108544555

- D11 H15 · (2,3) · pascolo vuoto
- D11 H19 · (3,2) · pascolo vuoto
- D11 H20 · (3,2) · SHEEP
- D11 H20 · (4,1) · pascolo vuoto
- D11 H21 · (4,1) · SHEEP
- D12 H7 · (2,3) · SHEEP

### Submission 56124096 · episodio 108549619

- D11 H15 · (2,3) · pascolo vuoto
- D11 H18 · (3,2) · pascolo vuoto
- D11 H19 · (3,2) · SHEEP
- D11 H19 · (4,1) · pascolo vuoto
- D11 H20 · (4,1) · SHEEP
- D12 H7 · (2,3) · SHEEP

### Submission 56171606 · episodio 108558711

- D11 H15 · (2,3) · pascolo vuoto
- D11 H18 · (3,2) · pascolo vuoto
- D11 H19 · (3,2) · SHEEP
- D11 H19 · (4,1) · pascolo vuoto
- D11 H20 · (4,1) · SHEEP
- D12 H7 · (2,3) · SHEEP

### Submission 56165125 · episodio 108561064

- D11 H15 · (2,3) · pascolo vuoto
- D11 H19 · (3,2) · pascolo vuoto
- D11 H20 · (3,2) · SHEEP
- D11 H20 · (4,1) · pascolo vuoto
- D12 H7 · (2,3) · SHEEP

### Submission 56198022 · episodio 108562089

- D11 H15 · (2,3) · pascolo vuoto
- D11 H19 · (3,2) · pascolo vuoto
- D11 H20 · (3,2) · SHEEP
- D11 H20 · (4,1) · pascolo vuoto
- D11 H21 · (4,1) · SHEEP
- D12 H7 · (2,3) · SHEEP

### Submission 56205921 · episodio 108575585

- D11 H15 · (2,3) · pascolo vuoto
- D11 H19 · (3,2) · pascolo vuoto
- D11 H20 · (3,2) · SHEEP
- D11 H20 · (4,1) · pascolo vuoto
- D12 H7 · (2,3) · SHEEP


[Dashboard mappe e traiettorie](REPORT.html) · [Tutte le traiettorie per casella, CSV](TILE_DAILY.csv) · [Sintesi e similarità](SUMMARY.json)
