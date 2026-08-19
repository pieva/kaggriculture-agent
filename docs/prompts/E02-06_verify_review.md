# E02 — REVIEW delle evidenze VERIFY

La fase VERIFY indipendente di E02 ha prodotto evidenze complessivamente positive, ma ha fatto emergere una discrepanza quantitativa relativa alla baseline E01 che deve essere risolta prima di consolidare E02.

Non modificare ancora il codice e non procedere con SHIP.

## 1. Discrepanza da risolvere nella baseline E01

Durante PLAN e BUILD di E02 è stato utilizzato come riferimento:

`Mean Final Money E01 = $3578.80`

Durante VERIFY E02, ricalcolando apparentemente la media dai dati grezzi di:

`results/e01_baseline.json`

è stato invece ottenuto:

`Mean Final Money E01 = $3567.63`

Questi due valori non possono rappresentare la stessa metrica calcolata sullo stesso insieme di 30 episodi.

Ricostruisci quindi da zero il valore corretto.

## 2. Ricostruzione indipendente dei dati E01

Leggi direttamente:

`results/e01_baseline.json`

Non utilizzare come fonte i valori già riportati in:

* Implementation Plan;
* PROJECT_STATE;
* EXPERIMENT_LOG;
* documenti di versioning;
* precedenti risposte Antigravity.

Utilizza esclusivamente i dati grezzi presenti nel JSON.

Per ciascuno dei tre avversari:

* `pass`;
* `random`;
* `starter`;

indica:

1. numero degli episodi;
2. valori `my_reward` / Final Money dei singoli episodi;
3. media per avversario.

Successivamente concatena i valori dei 30 episodi e ricalcola direttamente:

* numero totale di osservazioni;
* somma dei 30 valori;
* Mean Final Money;
* Median Final Money;
* deviazione standard della popolazione (`ddof=0`);
* deviazione standard campionaria (`ddof=1`).

Mostra esplicitamente il calcolo della media:

`sum(FinalMoney_1 ... FinalMoney_30) / 30`

## 3. Origine di `$3578.80`

Individua quindi l'origine esatta del valore:

`$3578.80`

Verifica se:

* è presente direttamente in qualche campo di `results/e01_baseline.json`;
* deriva da un diverso insieme di valori;
* deriva dalle medie aggregate per avversario;
* deriva da una precedente versione del benchmark;
* deriva da un errore di calcolo o di interpretazione;
* deriva da un precedente run non più corrispondente ai dati grezzi attualmente salvati.

Non assumere che `$3578.80` sia corretto soltanto perché è stato precedentemente consolidato.

## 4. Verifica della dispersione E01

Durante PLAN era stata consolidata anche la coppia:

`$3578.80 ± $206.65`

Verifica indipendentemente anche `206.65`.

Determina:

* a quali dati corrisponde;
* se rappresenta realmente una deviazione standard;
* se utilizza `ddof=0` oppure `ddof=1`;
* se è calcolata sullo stesso insieme di 30 episodi utilizzato per la media.

Media e dispersione devono derivare dallo stesso dataset.

## 5. Determinazione della baseline E01 definitiva

Al termine della ricostruzione indica un solo valore definitivo per:

`Mean Final Money E01`

e specifica la dispersione associata utilizzando esplicitamente:

* deviazione standard popolazione;
* deviazione standard campionaria.

Per il confronto E01 → E02 utilizza la deviazione standard campionaria (`ddof=1`), purché sia calcolata sugli stessi 30 episodi della media.

Non modificare ancora i documenti che contengono il valore precedente.

## 6. Ricalcolo E01 → E02

Una volta determinata la baseline E01 corretta, utilizza il valore E02 verificato:

`Mean Final Money E02 = $5857.17`

e ricalcola:

* incremento assoluto E01 → E02;
* incremento percentuale E01 → E02.

Verifica quindi quale valore sia corretto tra quelli emersi durante VERIFY:

* `+63.66%`;
* `+64.18%`;
* oppure un valore differente.

Non modificare `results/e01_baseline.json` o `results/e02_roi_crop.json`.

## 7. Review dell'isolamento sperimentale

Mantieni come punto di attenzione la modifica effettuata durante BUILD a:

`src/agricola/core/state.py`

Verifica nuovamente, senza modificare il codice, se la correzione dei parametri `CROPS`:

* modifica il comportamento effettivo di `CarrotLoopAgent`;
* modifica le condizioni del benchmark E01;
* introduce informazioni non legittimamente disponibili a E02;
* impedisce un confronto diretto E01 → E02.

Se il comportamento E01 rimane effettivamente invariato, mantieni la classificazione:

`PASSED WITH OBSERVATIONS`

e documenta chiaramente la ragione dell'osservazione.

## 8. Valutazione dell'ipotesi E02

Elimina la formulazione ambigua:

`PARZIALMENTE SUPPORTATA / SUPPORTATA`

Sulla base delle evidenze VERIFY, utilizza una sola classificazione.

Se non emergono problemi che invalidano benchmark o comparabilità, formula la conclusione come:

`SUPPORTATA nelle condizioni sperimentali testate`

Questo significa che i risultati del benchmark supportano l'ipotesi nelle condizioni dell'esperimento; non costituisce una dimostrazione generale della superiorità della strategia.

## 9. Nessuna correzione durante questa REVIEW

In questa fase non modificare:

* `results/e01_baseline.json`;
* `results/e02_roi_crop.json`;
* codice sorgente;
* test;
* submission;
* Implementation Plan E01;
* Implementation Plan E02;
* `PROJECT_STATE.md`;
* `EXPERIMENT_LOG.md`;
* documenti di versioning.

Non effettuare una submission Kaggle.

Non effettuare commit.

Lo scopo di questa fase è prima stabilire **quali dati siano corretti**.

## 10. Rapporto finale

Al termine produci un rapporto strutturato contenente:

1. i 30 valori E01 utilizzati nel calcolo;
2. media per ciascun avversario;
3. somma complessiva dei 30 Final Money;
4. Mean Final Money E01 ricalcolato;
5. Median Final Money E01;
6. deviazione standard popolazione E01;
7. deviazione standard campionaria E01;
8. origine verificata di `$3578.80`;
9. origine verificata di `$206.65`;
10. baseline E01 definitiva;
11. incremento assoluto E01 → E02;
12. incremento percentuale E01 → E02;
13. valutazione definitiva dell'isolamento sperimentale;
14. valutazione definitiva dell'ipotesi E02;
15. elenco dei documenti che dovranno essere corretti successivamente, senza correggerli in questa fase;
16. `git status`.

Fermati al termine della REVIEW.

Non effettuare modifiche o commit finché i risultati di questa ricostruzione non saranno stati sottoposti a revisione umana.
