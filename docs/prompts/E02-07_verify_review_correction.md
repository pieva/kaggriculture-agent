# E02 — Correzione delle formulazioni nella VERIFY REVIEW

La REVIEW delle evidenze VERIFY E02 ha ricostruito correttamente dai dati grezzi di:

`results/e01_baseline.json`

la baseline E01:

`Mean Final Money E01 = $3567.63 ± $205.38`

utilizzando la deviazione standard campionaria (`ddof=1`).

Ha inoltre stabilito correttamente che il miglioramento E01 → E02 è:

`+64.18%`

Prima di salvare il rapporto come evidenza persistente, correggi però **due formulazioni causali che risultano più forti delle evidenze disponibili**.

Non rieseguire il benchmark e non modificare codice o risultati.

## 1. Correzione dell'origine di `$3578.80`

Nel rapporto precedente è stato affermato:

> Il valore `$3578.80` [...] ha origine da una run di test intermedia precedente.

Questa origine non è dimostrata dai dati persistenti attualmente disponibili.

Ciò che è invece verificabile è che `$3578.80` può essere ricostruito dai tre valori aggregati precedentemente riportati:

* `pass = $3594.30`;
* `random = $3610.50`;
* `starter = $3531.60`.

Infatti:

`(3594.30 + 3610.50 + 3531.60) / 3 = 3578.80`

Il valore precedentemente riportato per `random`, `$3610.50`, non coincide però con la media ricostruibile dai 10 episodi attualmente conservati in:

`results/e01_baseline.json`

che è:

`$3577.00`.

Correggi quindi la formulazione indicando che:

* è verificabile **come** sia stato ottenuto `$3578.80` dai valori aggregati precedentemente documentati;
* non è verificabile dai dati persistenti disponibili **perché** il valore `$3610.50` fosse stato precedentemente ottenuto;
* una precedente run differente costituisce una possibile spiegazione, ma non deve essere presentata come fatto accertato.

Non utilizzare formulazioni che attribuiscano con certezza `$3578.80` a una specifica run precedente se non esiste un'evidenza persistente che lo dimostri.

## 2. Correzione dell'origine di `$206.65`

Nel rapporto precedente è stato affermato che `$206.65` è la deviazione standard campionaria calcolata sull'insieme della precedente run intermedia.

Anche questa origine causale non è dimostrata dai dati persistenti disponibili.

Ciò che è verificato è che:

* sui 30 valori attualmente presenti in `results/e01_baseline.json`;
* la deviazione standard della popolazione (`ddof=0`) è `$201.93`;
* la deviazione standard campionaria (`ddof=1`) è `$205.38`.

Di conseguenza `$206.65` **non è la deviazione standard campionaria dei 30 episodi E01 attualmente conservati**.

Correggi la formulazione limitandoti a questa conclusione verificabile.

Puoi indicare che `$206.65` potrebbe derivare da un diverso insieme di osservazioni o da un precedente calcolo, ma non attribuirlo con certezza a una specifica run in assenza dei relativi dati grezzi persistenti.

## 3. Mantieni invariati i risultati verificati

Non modificare le conclusioni quantitative già ricostruite:

* `Mean Final Money E01 = $3567.63`;
* `Median Final Money E01 = $3528.00`;
* Population Std (`ddof=0`) = `$201.93`;
* Sample Std (`ddof=1`) = `$205.38`;
* `Mean Final Money E02 = $5857.17`;
* incremento assoluto E01 → E02 = `+$2289.53`;
* incremento percentuale E01 → E02 = `+64.18%`;
* isolamento sperimentale = `PASSED WITH OBSERVATIONS`;
* ipotesi E02 = `SUPPORTATA nelle condizioni sperimentali testate`.

Non modificare gli altri risultati della REVIEW salvo quanto strettamente necessario per rendere coerenti le due formulazioni corrette.

## 4. Crea l'evidenza persistente

Dopo aver applicato esclusivamente queste due correzioni epistemiche, salva il rapporto completo e definitivo della REVIEW in:

`docs/versions/E02_verify_review_antigravity.md`

Il documento deve conservare:

* ricostruzione dei 30 valori E01;
* medie per avversario;
* calcoli statistici;
* confronto E01 → E02;
* valutazione dell'isolamento;
* valutazione dell'ipotesi;
* indicazione dei documenti che dovranno essere successivamente corretti.

Non trasformare ipotesi sull'origine dei valori errati in fatti.

## 5. Vincoli

Non modificare:

* `results/e01_baseline.json`;
* `results/e02_roi_crop.json`;
* codice sorgente;
* test;
* submission;
* Implementation Plan E01;
* Implementation Plan E02;
* `PROJECT_STATE.md`;
* `EXPERIMENT_LOG.md`.

Non effettuare nuovi benchmark.

Non effettuare submission Kaggle.

Non effettuare commit.

## Al termine

1. mostra le due formulazioni precedenti;

2. mostra le due formulazioni corrette;

3. conferma che i risultati quantitativi verificati siano rimasti invariati;

4. conferma la creazione di:

   `docs/versions/E02_verify_review_antigravity.md`

5. mostra `git diff -- docs/versions/E02_verify_review_antigravity.md`;

6. mostra `git status`;

7. fermati senza effettuare altre modifiche o commit.

Attendi la revisione umana prima di procedere con la correzione degli altri documenti E01/E02.
