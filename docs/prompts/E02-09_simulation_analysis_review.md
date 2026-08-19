# E02 — REVIEW dell'analisi osservabile della simulazione

È stato prodotto il documento:

`docs/versions/E02_simulation_analysis.md`

che analizza un episodio completo E02 e prova a spiegare l'origine economica del miglioramento di `ROICropAgent`.

Prima di considerare questa evidenza consolidata, esegui una REVIEW mirata esclusivamente su:

1. contabilità effettiva dei cicli produttivi;
2. confronto economico `CARROT` vs `MELON`;
3. differenza tra `Yield` utilizzato nella formula ROI e resa reale osservata;
4. conseguenze interpretative di queste verifiche.

Non modificare la strategia e non iniziare E03.

## 1. Verifica contabile dei cicli E02

Ricostruisci direttamente dagli `env.steps` dell'episodio osservato tutti i flussi monetari rilevanti dei cicli `MELON`.

Per ciascun ciclo determina in modo univoco:

* capitale prima dell'acquisto del seme;
* acquisti di semi effettuati;
* eventuale acquisto anticipato del seme buffer;
* capitale dopo ciascun acquisto;
* quantità raccolta;
* prezzo unitario effettivo alla vendita;
* ricavo lordo della vendita;
* capitale immediatamente prima della vendita;
* capitale immediatamente dopo la vendita;
* profitto netto effettivamente attribuibile al ciclo.

Non dedurre il profitto come semplice differenza tra due checkpoint se tra i checkpoint sono intervenuti altri acquisti.

Mostra esplicitamente la riconciliazione:

`Money iniziale + incassi - acquisti = Money finale`

per ciascun ciclo.

## 2. Verifica delle cifre riportate nel documento

Controlla in particolare i valori attualmente presenti in:

`docs/versions/E02_simulation_analysis.md`

relativi a:

* profitto netto Ciclo 1;
* profitto netto Ciclo 2;
* incremento del capitale a Day 15;
* incremento del capitale a Day 25;
* profitto complessivo attribuito ai primi due cicli di `MELON`.

Segnala ogni valore che non sia direttamente riconciliabile con la sequenza monetaria osservata.

Non correggere ancora il documento durante questa fase.

## 3. Ricostruzione del confronto E01 `CARROT`

Nel documento è riportata la stima:

`8 cicli × $70 ricavo lordo - 8 × $20 seme = +$560`

Verifica aritmeticamente e concettualmente questa affermazione.

Ricostruisci il confronto con `CARROT` utilizzando:

* seed cost effettivo;
* quantità effettiva prodotta;
* prezzo di vendita osservato o esplicitamente assunto;
* numero di cicli completabili nel periodo considerato;
* eventuali semi buffer acquistati.

Distingui chiaramente:

* ricavo lordo;
* costo semi;
* profitto netto;
* variazione effettiva del capitale.

Non utilizzare `$560` se non è supportato dai calcoli.

## 4. Verifica della resa reale

Nel codice E02 la formula ROI utilizza:

`Yield_c = 2`

mentre nell'episodio osservato `MELON` produce:

`6 unità`

grazie all'irrigazione regolare.

Verifica direttamente nell'ambiente:

* quale valore rappresenta `2`;
* quale valore rappresenta `6`;
* in quali condizioni si ottiene la resa massima;
* se la resa effettiva differisce tra colture;
* se l'uso di `Yield=2` nella formula ROI costituisce una stima conservativa, una semplificazione oppure un errore di modellazione.

Non assumere che tutte le colture abbiano automaticamente `max_yield = 6` se non verificato.

## 5. Ricalcolo ROI con resa effettiva

Per i punti decisionali già documentati, ricalcola il ROI utilizzando:

### Formula implementata

`Yield = 2`

e, separatamente, la resa effettivamente ottenibile con irrigazione regolare per ciascuna coltura, se disponibile dall'ambiente.

Produci una tabella comparativa:

| Coltura | ROI con Yield implementato | ROI con Yield effettivo | Ranking implementato | Ranking effettivo |
| ------- | -------------------------: | ----------------------: | -------------------: | ----------------: |

Verifica se:

* `MELON` rimane comunque la coltura con ROI maggiore;
* il ranking cambia per alcune colture;
* la scelta di E02 è corretta nonostante il modello semplificato;
* oppure il risultato positivo dipende in parte da una coincidenza favorevole.

## 6. Interpretazione del miglioramento E02

Dopo la verifica, separa:

### Meccanismi effettivamente dimostrati

Ad esempio:

* scelta di una coltura più redditizia;
* maggiore resa effettiva;
* prezzi di vendita favorevoli;
* accumulo di capitale derivante da specifici cicli.

### Meccanismi solo ipotizzati

Non attribuire al “dynamic crop selection” benefici che derivano in realtà da:

* una singola coltura dominante;
* una resa reale non rappresentata correttamente dalla formula;
* condizioni favorevoli di mercato nell'episodio osservato.

Stabilisci se la formulazione:

> “E02 migliora grazie alla selezione dinamica delle colture”

sia pienamente supportata oppure se sia più rigoroso dire:

> “E02 migliora principalmente perché la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.”

## 7. Rivalutazione dei limiti E02

Alla luce dei risultati della REVIEW, rivaluta esclusivamente questi limiti:

* **End-of-season horizon**;
* **Single-tile limitation**;
* **Immediate selling**;
* **Yield model simplification**.

Per ciascuno indica:

1. evidenza osservata;
2. possibile impatto economico;
3. se costituisce una variabile candidata per una successiva iterazione.

Non scegliere ancora E03.

## 8. Nessuna modifica durante questa REVIEW

In questa fase non modificare:

* `ROICropAgent`;
* `CarrotLoopAgent`;
* `GameState`;
* test;
* benchmark runner;
* submission;
* risultati JSON;
* Implementation Plan;
* `PROJECT_STATE.md`;
* `EXPERIMENT_LOG.md`;
* `docs/versions/E02_simulation_analysis.md`.

Non effettuare benchmark aggiuntivi.

Non effettuare submission Kaggle.

Non effettuare commit.

## 9. Rapporto finale

Al termine produci un rapporto strutturato contenente:

1. riconciliazione monetaria del Ciclo 1;
2. riconciliazione monetaria del Ciclo 2;
3. profitto netto corretto per ciascun ciclo;
4. profitto complessivo corretto dei cicli E02 osservati;
5. confronto corretto con `CARROT`;
6. verifica di `Yield=2` vs resa reale;
7. ranking ROI con formula implementata;
8. ranking ROI con resa effettiva;
9. valutazione rigorosa dell'origine del miglioramento E02;
10. limiti E02 rivalutati;
11. elenco preciso delle correzioni che dovranno essere applicate successivamente a `docs/versions/E02_simulation_analysis.md`;
12. `git status`.

Fermati al termine della REVIEW.

Non modificare documentazione o codice finché i risultati non saranno stati sottoposti a revisione umana.
