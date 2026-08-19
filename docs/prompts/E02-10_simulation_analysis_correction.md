# E02 — Correzione dell'analisi osservabile della simulazione

La REVIEW eseguita con:

`docs/prompts/E02-09_simulation_review.md`

ha individuato alcune correzioni necessarie nel documento:

`docs/versions/E02_simulation_analysis.md`

Applica ora esclusivamente le correzioni supportate dalla REVIEW e dalle evidenze osservabili.

Non modificare la strategia, il codice o altri documenti di progetto.

## 1. Riconciliazione monetaria

Correggi la descrizione dei primi due cicli produttivi utilizzando la sequenza monetaria effettivamente osservata.

Distingui sempre:

* costo del seme attribuibile al ciclo;
* acquisto anticipato del seme buffer;
* acquisti relativi al ciclo successivo;
* ricavo lordo della vendita;
* profitto netto del singolo ciclo;
* variazione complessiva del capitale dell'agente.

Per i due raccolti completati mantieni, se confermati dalla REVIEW:

* Profitto netto Ciclo 1: `+$1547.0`;
* Profitto netto Ciclo 2: `+$1570.0`;
* Profitto netto complessivo dei due raccolti: `+$3117.0`.

Non confondere questo valore con la variazione finale del capitale.

Per l'episodio osservato:

* capitale iniziale: `$3000.0`;
* capitale finale: `$5957.0`;
* variazione complessiva del capitale: `+$2957.0`.

Riconcilia esplicitamente la differenza tra `+$3117.0` dei due raccolti completati e `+$2957.0` di variazione finale considerando gli acquisti di semi che non hanno ancora generato ricavi.

Non mantenere formulazioni ambigue come:

`+$2837.0 / +$2957.0`.

Deve comparire una sola ricostruzione contabile coerente.

## 2. Correzione del confronto CARROT vs MELON

Elimina il precedente calcolo:

`8 cicli × $70 - 8 × $20 = +$560`

perché confonde ricavo lordo e profitto netto.

Inserisci il confronto verificato dalla REVIEW distinguendo due scenari.

### Con resa effettiva irrigata

Per `CARROT`:

* `max_yield = 4`;
* ricavo lordo teorico su 8 cicli: `$1120.0`;
* profitto netto teorico su 8 cicli: `+$960.0`.

Per i due raccolti `MELON` effettivamente osservati:

* ricavo lordo complessivo: `$3277.0`;
* profitto netto complessivo attribuibile ai due raccolti: `+$3117.0`.

Esplicita che il confronto CARROT è teorico, mentre i valori MELON derivano dall'episodio osservato.

### Con Yield=2 utilizzato dalla formula E02

Riporta separatamente, se utile alla spiegazione:

* CARROT: `+$400.0` netto teorico;
* MELON: circa `+$923.2` netto teorico sulla base dei prezzi utilizzati nel confronto.

Non mescolare questi valori con quelli ottenuti usando `max_yield`.

## 3. Yield implementato e resa reale

Correggi il documento spiegando che la formula ROI implementata da E02 utilizza:

`Yield = 2`

come semplificazione conservativa.

Riporta i valori verificati dell'ambiente:

* `WHEAT`: `max_yield = 6`;
* `CARROT`: `max_yield = 4`;
* `TOMATO`: `max_yield = 4`;
* `STRAWBERRY`: `max_yield = 4`;
* `MELON`: `max_yield = 6`.

Spiega che l'irrigazione regolare consente nell'episodio osservato di raggiungere la resa massima.

## 4. Confronto del ranking ROI

Integra una tabella che confronti, per il momento decisionale iniziale già analizzato:

| Coltura | ROI con Yield=2 | ROI con MaxYield | Rank Yield=2 | Rank MaxYield |
| ------- | --------------: | ---------------: | -----------: | ------------: |

Utilizza esclusivamente i valori verificati durante la REVIEW.

Evidenzia il risultato metodologicamente importante:

`MELON` è Rank 1 sia con `Yield=2` sia utilizzando `max_yield`.

Di conseguenza, la semplificazione della resa rende il modello economico quantitativamente impreciso, ma **non altera la decisione iniziale osservata nell'episodio E02**.

## 5. Correzione dell'interpretazione causale

Sostituisci eventuali formulazioni troppo generali secondo cui il miglioramento sarebbe dimostrato come conseguenza della generica "selezione dinamica delle colture".

Utilizza come conclusione principale:

> E02 migliora principalmente perché la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.

Distingui chiaramente:

### Evidenza osservata

`ROICropAgent` seleziona inizialmente `MELON`, che rimane economicamente dominante nei primi cicli osservati.

### Interpretazione

Il forte miglioramento rispetto a E01 deriva principalmente dal passaggio dalla monocultura `CARROT` alla coltura `MELON`, molto più redditizia nelle condizioni osservate.

### Limite della conclusione

Un singolo episodio osservabile non dimostra che una strategia di switching dinamico tra numerose colture sia la causa generale del miglioramento.

## 6. Correzione della parte finale della stagione

La REVIEW ha rilevato un elemento importante rispetto alla precedente analisi: nella parte finale dell'episodio compare `STRAWBERRY`.

Correggi quindi ogni affermazione secondo cui:

* E02 utilizza `MELON` nel 100% dell'intero episodio;
* il terzo ciclo avviato a Day 24 sarebbe necessariamente `MELON`;
* `STRAWBERRY` non sarebbe mai selezionata.

Distingui:

* i **due cicli completati e venduti**, entrambi `MELON`;
* la coltura selezionata successivamente per il ciclo non completato entro la fine della stagione.

Ricostruisci questa parte esclusivamente dagli `env.steps` già analizzati nella REVIEW.

## 7. Limiti E02

Aggiorna la sezione sui limiti mantenendo distinti:

1. **End-of-Season Horizon**

   * l'agente avvia una coltura che non può maturare prima della fine dell'episodio;

2. **Single-Tile Limitation**

   * viene utilizzata una sola casella;

3. **Immediate Selling**

   * i prodotti vengono venduti immediatamente senza market timing;

4. **Yield Model Simplification**

   * il ROI usa `Yield=2` invece della resa massima specifica della coltura.

Non scegliere quale di questi aspetti debba diventare E03.

## 8. Vincoli

Modifica esclusivamente:

`docs/versions/E02_simulation_analysis.md`

Non modificare:

* codice sorgente;
* `ROICropAgent`;
* `CarrotLoopAgent`;
* `GameState`;
* test;
* benchmark runner;
* submission;
* risultati JSON;
* Implementation Plan;
* `PROJECT_STATE.md`;
* `EXPERIMENT_LOG.md`.

Non eseguire nuovi benchmark.

Non effettuare submission Kaggle.

Non iniziare E03.

Non effettuare commit.

## 9. Al termine

1. mostra il diff di `docs/versions/E02_simulation_analysis.md`;
2. conferma la riconciliazione:

   * profitto netto dei due raccolti completati: `+$3117.0`;
   * variazione complessiva del capitale: `+$2957.0`;
3. conferma che il confronto CARROT non utilizzi più `$560` come profitto netto;
4. conferma che sia documentata la differenza `Yield=2` vs `max_yield`;
5. conferma che `MELON` rimanga Rank 1 con entrambi i modelli nel momento decisionale analizzato;
6. conferma che la parte finale dell'episodio riporti correttamente l'eventuale selezione di `STRAWBERRY`;
7. mostra `git status`;
8. fermati senza commit.
