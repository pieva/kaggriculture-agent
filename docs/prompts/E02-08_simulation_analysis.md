# E02 — Analisi osservabile della simulazione e origine del miglioramento ROI

E02 ha superato BUILD, VERIFY e REVIEW quantitativa.

Il benchmark verificato mostra:

* E01 Mean Final Money: `$3567.63`;
* E02 Mean Final Money: `$5857.17`;
* incremento assoluto: `+$2289.53`;
* incremento percentuale: `+64.18%`;
* Win Rate E02 vs `starter`: `100%`.

Questi valori dimostrano quantitativamente il miglioramento, ma non spiegano ancora **da quali decisioni operative ed economiche emerga il vantaggio di `ROICropAgent`**.

Esegui quindi un'analisi osservabile della simulazione E02 finalizzata a comprendere il comportamento dell'agente e a produrre evidenze utili alla progettazione dell'esperimento successivo.

Non modificare la strategia.

## 1. Obiettivo

Ricostruisci il comportamento economico di `ROICropAgent` durante un episodio completo di 720 turni.

L'analisi deve rispondere principalmente alla domanda:

> Perché E02 produce un capitale finale significativamente superiore alla baseline E01 basata esclusivamente su `CARROT`?

Non limitarti ad analizzare il codice. Utilizza l'esecuzione effettiva dell'ambiente e gli stati osservabili della simulazione.

## 2. Esecuzione osservabile

Esegui un episodio completo di 720 turni tramite `kaggle_environments` utilizzando `ROICropAgent`.

Utilizza `env.steps` per ricostruire:

* stato del mercato;
* capitale `money`;
* semi disponibili;
* contenuto dello `shed`;
* coltura presente sulla casella;
* azioni `farmer`;
* azioni `market`;
* reward;
* cambiamenti significativi della strategia.

Non modificare codice persistente per effettuare l'analisi.

Eventuali script diagnostici devono essere temporanei/scratch e non devono essere aggiunti al repository.

## 3. Ricostruzione dei cicli produttivi

Non stampare indiscriminatamente tutti i 720 turni.

Ricostruisci invece i singoli **cicli produttivi significativi**:

`scelta → BUY_SEED → PLANT → WATER → HARVEST → SELL`

Per ogni ciclo determina, per quanto ricostruibile dall'ambiente:

* giorno di inizio;
* coltura scelta;
* capitale disponibile al momento della scelta;
* SeedPrice;
* SellPrice osservato al momento della scelta;
* Days;
* Yield utilizzato dalla formula;
* NetProfitPerDay stimato;
* prezzo effettivo al momento della vendita;
* quantità raccolta;
* ricavo effettivo;
* capitale dopo la vendita.

Evidenzia in particolare ogni passaggio nel quale la coltura scelta differisce da quella del ciclo precedente.

## 4. Confronto delle alternative ROI

Nei momenti in cui viene effettuata una nuova scelta, ricostruisci il valore di:

`NetProfitPerDay(c)`

per tutte le colture acquistabili.

Utilizza la formula effettivamente implementata:

`((SellPrice_c × Yield_c) - SeedPrice_c) / Days_c`

Produci una tabella sintetica per alcuni momenti decisionali rappresentativi contenente almeno:

| Giorno | Coltura | SellPrice | SeedPrice | Days | ROI/giorno | Selezionata |
| ------ | ------- | --------: | --------: | ---: | ---------: | ----------- |

L'obiettivo è rendere osservabile **perché** una coltura venga preferita alle altre.

## 5. Distribuzione delle colture selezionate

Sull'intero episodio calcola:

* numero di cicli produttivi;
* numero di volte in cui viene selezionata ciascuna coltura;
* percentuale dei cicli per coltura;
* eventuali colture mai selezionate.

Determina se il miglioramento E02 deriva:

* dall'utilizzo sistematico di una particolare coltura;
* dall'alternanza dinamica tra colture;
* oppure da entrambe le componenti.

## 6. Confronto comportamentale con E01

Utilizza la baseline E01 come riferimento concettuale:

`CARROT` esclusivamente.

Per alcuni momenti rappresentativi della simulazione E02, calcola anche quale sarebbe stato il `NetProfitPerDay` della `CARROT`.

Confrontalo con quello della coltura effettivamente scelta.

Non simulare una nuova strategia E01 e non modificare la baseline.

Lo scopo è mostrare concretamente dove `ROICropAgent` trova opportunità economiche che `CarrotLoopAgent` ignora.

## 7. Profitto stimato e profitto realizzato

La decisione E02 utilizza il prezzo disponibile **al momento della scelta**, mentre la vendita avviene successivamente.

Verifica quindi se il prezzo di mercato cambia durante il ciclo produttivo.

Per alcuni cicli rappresentativi confronta:

* profitto previsto al momento della scelta;
* prezzo previsto/observed utilizzato nella scelta;
* prezzo effettivo al momento della vendita;
* profitto effettivamente realizzato.

Determina se la volatilità del mercato:

* migliora il risultato;
* peggiora il risultato;
* oppure tende a compensarsi nell'episodio osservato.

Questo punto è importante per individuare eventuali limiti del criterio ROI istantaneo.

## 8. Evoluzione del capitale

Ricostruisci l'evoluzione del capitale durante l'episodio utilizzando checkpoint significativi, almeno:

* Day 0;
* Day 5;
* Day 10;
* Day 15;
* Day 20;
* Day 25;
* Day 29/finale.

Mostra una tabella:

| Giorno | Money E02 | Coltura/ciclo corrente | Osservazione |
| ------ | --------: | ---------------------- | ------------ |

Individua in quali fasi della stagione si accumula maggiormente il vantaggio economico.

## 9. Origine del miglioramento E02

Sulla base esclusiva delle evidenze osservate, distingui chiaramente:

### Evidenze

Ciò che è direttamente osservabile nella simulazione.

### Interpretazioni

Le spiegazioni ragionevolmente supportate dalle evidenze.

### Limiti

Ciò che non può essere concluso da un singolo episodio.

Spiega quali meccanismi sembrano contribuire maggiormente al miglioramento rispetto a E01.

Non attribuire causalità a fenomeni che non siano supportati dai dati.

## 10. Indicazioni per E03

Non progettare e non implementare E03.

Individua però le **dimensioni strategiche ancora inutilizzate o potenzialmente inefficienti** emerse dall'osservazione.

Considera, solo se supportato dalla simulazione:

* utilizzo di una sola casella;
* assenza di movimento;
* ROI calcolato sul prezzo istantaneo;
* variazione del prezzo tra semina e vendita;
* momento della vendita;
* gestione della liquidità;
* diversificazione delle colture;
* informazioni sul terreno;
* stato dell'avversario;
* altre informazioni presenti in `GameState` ma non utilizzate.

Per ciascuna opportunità indica l'evidenza osservata che la rende interessante.

Non scegliere ancora quale sarà E03.

## 11. Evidenza persistente

Salva il rapporto completo in:

`docs/versions/E02_simulation_analysis.md`

Il documento deve essere comprensibile indipendentemente dal log della conversazione Antigravity e deve permettere di ricostruire:

1. come si comporta E02;
2. perché supera E01;
3. quali limiti rimangono;
4. quali dimensioni possono essere investigate nell'esperimento successivo.

## Vincoli

Non modificare:

* codice sorgente;
* `ROICropAgent`;
* `CarrotLoopAgent`;
* `GameState`;
* test;
* benchmark runner;
* risultati JSON;
* submission;
* Implementation Plan;
* `PROJECT_STATE.md`;
* `EXPERIMENT_LOG.md`.

Non effettuare nuovi benchmark comparativi.

Non effettuare submission Kaggle.

Non effettuare commit.

## Al termine

Mostra:

1. sintesi dell'episodio osservato;
2. cicli produttivi;
3. distribuzione delle colture;
4. esempi di confronto ROI;
5. evoluzione del capitale;
6. confronto con `CARROT`;
7. differenza tra profitto stimato e realizzato;
8. spiegazione supportata del miglioramento E02;
9. limiti osservati;
10. possibili dimensioni da investigare in E03;
11. conferma della creazione di `docs/versions/E02_simulation_analysis.md`;
12. `git status`.

Fermati senza modificare la strategia e senza effettuare commit.
