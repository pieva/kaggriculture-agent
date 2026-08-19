# E02 — Review dell'Implementation Plan

Prima di approvare l'Implementation Plan di E02 e procedere con l'implementazione, esegui una revisione puntuale del piano appena prodotto.

Non iniziare ancora BUILD.

## 1. Verifica della baseline quantitativa E01

Nel piano E02 viene utilizzato come riferimento:

`Mean Final Money E01 = 3578.80`

Durante il successivo VERIFY osservabile di E01 è stato invece registrato:

`Final Money = 3564.0`

Verifica nei risultati e nella documentazione E01 l'origine esatta di entrambi i valori.

Distingui esplicitamente:

* il valore medio ottenuto dal benchmark E01 sui 30 episodi;
* il valore finale del singolo episodio eseguito durante il VERIFY tramite Antigravity.

Se `3578.80` è effettivamente la media del benchmark E01, mantienilo come baseline quantitativa per il confronto E01 → E02 e chiarisci nel piano che si tratta di **Mean Final Money sui 30 episodi**.

Non sostituirlo con `3564.0`, se quest'ultimo rappresenta soltanto il singolo episodio VERIFY.

## 2. Verifica dell'ipotesi sperimentale

Controlla che l'ipotesi di E02 sia formulata come ipotesi da verificare e non come risultato già acquisito.

In particolare, affermazioni come:

* superamento netto dello `starter` agent;
* aumento significativo del capitale finale;
* target `Mean Final Money > 4500`;
* `Win Rate > 90%`;

devono essere chiaramente presentate come **obiettivi o risultati attesi**, non come risultati già dimostrati.

## 3. Verifica del calcolo ROI

Verifica che la formula proposta per la selezione dinamica della coltura utilizzi esclusivamente informazioni realmente disponibili nell'ambiente e già accessibili all'agente.

Controlla in particolare l'origine di:

* prezzo del seme;
* prezzo di vendita;
* resa della coltura;
* giorni di crescita.

Distingui eventuali valori statici di configurazione dai prezzi dinamici osservabili durante l'episodio.

Non introdurre informazioni che l'agente non può conoscere legittimamente al momento della decisione.

## 4. Verifica dell'isolamento sperimentale

Conferma che E02 modifichi una sola dimensione strategica principale rispetto a E01:

**scelta dinamica della coltura in funzione del rendimento economico**

e che rimangano invariati, per quanto possibile:

* utilizzo di una singola tile;
* posizione iniziale;
* ciclo fondamentale `BUY_SEED → PLANT → WATER → HARVEST → SELL`;
* infrastruttura di esecuzione;
* criteri di benchmark;
* durata degli episodi;
* confronto con lo `starter` agent.

Lo scopo è rendere attribuibile l'eventuale variazione delle metriche alla nuova strategia economica.

## 5. Verifica della comparabilità E01 → E02

Controlla che il Verification Plan consenta un confronto quantitativo diretto con E01 utilizzando le stesse metriche consolidate:

* Completion Rate;
* Disqualification Rate;
* Win Rate;
* Mean Final Money;
* Agent Mean Turn Latency.

Segnala eventuali differenze metodologiche che renderebbero non direttamente confrontabili i risultati.

## 6. Aggiornamento dell'Implementation Plan

Se dalla revisione emergono correzioni o precisazioni necessarie, aggiorna esclusivamente l'Implementation Plan E02.

Non modificare ancora:

* codice sorgente;
* test;
* submission;
* risultati E01;
* documentazione consolidata E01.

Al termine mostra chiaramente:

1. origine e significato di `3578.80` e `3564.0`;
2. eventuali problemi individuati nel piano;
3. correzioni apportate;
4. ipotesi sperimentale definitiva di E02;
5. metriche e target definitivi;
6. conferma che E02 rimanga un'evoluzione incrementale controllata rispetto a E01.

Fermati al termine della REVIEW.

Non procedere con l'implementazione finché non viene fornita esplicita approvazione umana tramite `Proceed`.
