# E02 — Final Check dell'Implementation Plan

Prima di approvare definitivamente l'Implementation Plan E02 ed iniziare BUILD, esegui un ultimo controllo quantitativo esclusivamente sul file:

`docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`

Non iniziare BUILD.

## 1. Verifica della baseline quantitativa E01

Nel documento compare correttamente:

`Mean Final Money E01 = 3578.80`

ma sono riportati due diversi valori di dispersione:

* `±206.65`;
* `±194.05`.

Verifica direttamente `results/e01_baseline.json` e determina quale valore sia effettivamente supportato dai risultati del benchmark E01 sui 30 episodi.

Mantieni:

`Mean Final Money E01 = 3578.80`

e utilizza in tutto l'Implementation Plan un solo valore di dispersione, quello effettivamente verificato dai risultati E01.

Non modificare altri risultati numerici E01 se non emerge una loro effettiva incoerenza con il report.

## 2. Verifica di `MELON max_yield_day`

Nella sezione relativa ai giorni di crescita compare:

`MELON=7/12`

Questo valore è ambiguo e viene utilizzato direttamente nella formula di selezione ROI.

Verifica direttamente nella configurazione dell'ambiente `kaggriculture` il valore effettivo di:

`CROPS["MELON"]["max_yield_day"]`

Sostituisci `7/12` con l'unico valore effettivamente definito dall'ambiente.

Non dedurre o stimare il valore: utilizza quello presente nella configurazione effettiva dell'ambiente installato.

## 3. Verifica finale di coerenza

Dopo le due correzioni, verifica che il piano utilizzi in modo coerente:

* `Mean Final Money E01 = 3578.80` con la dispersione corretta;
* il valore verificato di `MELON max_yield_day`;
* `SellPrice` come prezzo dinamico osservato dal mercato;
* `SeedPrice` come costo del seme definito dalla configurazione della coltura;
* la stessa formula `NetProfitPerDay` in tutto il documento.

Non modificare:

* ipotesi sperimentale E02;
* strategia proposta;
* target sperimentali;
* isolamento sperimentale;
* Verification Plan, salvo le correzioni quantitative strettamente necessarie;
* codice sorgente;
* test;
* submission;
* risultati E01;
* `PROJECT_STATE.md`;
* `EXPERIMENT_LOG.md`;
* altri documenti.

Non creare altri Implementation Plan e non rinominare:

`docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`

## Al termine

Indica:

1. valore verificato di `Mean Final Money E01` e relativa dispersione;

2. origine del valore verificato;

3. valore effettivo di `CROPS["MELON"]["max_yield_day"]`;

4. correzioni applicate all'Implementation Plan;

5. risultato della verifica finale di coerenza;

6. diff del solo file:

   `docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`

7. `git status`.

Fermati senza commit.

Non iniziare BUILD e attendi l'esplicita approvazione umana prima di procedere.
