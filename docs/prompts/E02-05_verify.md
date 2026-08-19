# E02 — VERIFY indipendente di `ROICropAgent`

La fase BUILD di E02 — **Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)** — è terminata.

Esegui ora una fase **VERIFY indipendente** dell'implementazione e dei risultati prodotti.

Lo scopo non è confermare le conclusioni formulate al termine di BUILD, ma verificare criticamente se esse siano effettivamente supportate dal codice, dall'esecuzione e dalle evidenze quantitative.

Non ottimizzare la strategia e non correggere il codice durante questa fase.

## 1. Riferimenti

Utilizza come riferimento:

`docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`

`docs/versions/E02_build_antigravity.md`

`results/e01_baseline.json`

`results/e02_roi_crop.json`

e il codice E02 effettivamente presente nel repository.

Confronta E02 con la baseline E01 senza modificarla.

## 2. Verifica dell'isolamento sperimentale

Verifica che E02 abbia effettivamente modificato la sola dimensione strategica prevista dal piano:

**selezione dinamica della coltura sulla base del rendimento netto giornaliero e della liquidità disponibile.**

Controlla in particolare:

* `src/agricola/strategy/roi_crop.py`;
* `src/agricola/core/state.py`;
* `src/agricola/agent.py`;
* `scripts/build_submission.py`;
* `submission/submission.py`;
* test aggiunti o modificati.

Confronta il comportamento E02 con `CarrotLoopAgent`.

Verifica che siano rimasti invariati, salvo quanto strettamente necessario all'implementazione:

* utilizzo di una sola casella;
* posizione `(4, 4)`;
* assenza di movimento `MOVE`;
* ciclo fondamentale di acquisto, semina, irrigazione, raccolta e vendita;
* durata dell'episodio;
* infrastruttura di benchmark;
* definizione delle metriche.

### Modifiche a `state.py`

BUILD ha modificato:

`src/agricola/core/state.py`

per aggiornare i parametri `CROPS`.

Verifica esplicitamente:

1. quali valori sono stati modificati;
2. da quale sorgente dell'ambiente `kaggriculture` derivano;
3. se tali valori sono effettivamente disponibili o legittimamente conoscibili dall'agente;
4. se la modifica costituisce soltanto una correzione della rappresentazione dell'ambiente oppure altera sostanzialmente le condizioni sperimentali;
5. se la modifica può influenzare retroattivamente il comportamento della baseline E01 o la comparabilità E01 → E02.

Non correggere eventuali problemi: documentali.

## 3. Verifica della formula ROI

Ricostruisci dal codice la formula effettivamente utilizzata da `ROICropAgent`.

Verifica che corrisponda al piano approvato:

`NetProfitPerDay(c) = ((SellPrice_c × Yield_c) - SeedPrice_c) / Days_c`

Verifica separatamente l'origine effettiva di:

* `SellPrice_c`;
* `Yield_c`;
* `SeedPrice_c`;
* `Days_c`.

Controlla che non venga utilizzata informazione futura, non osservabile o comunque non disponibile legittimamente all'agente al momento della decisione.

Verifica inoltre che la selezione consideri esclusivamente colture acquistabili con la liquidità corrente.

## 4. Verifica comportamentale osservabile

Esegui almeno un episodio completo E02 di 720 turni utilizzando l'ambiente reale `kaggle_environments`.

Ispeziona direttamente `env.steps`.

Produci una traccia sintetica ma sufficientemente dettagliata dei passaggi nei quali:

* viene scelta una coltura;
* viene acquistato un seme;
* viene piantata una coltura;
* viene irrigata;
* viene raccolta;
* viene venduta;
* cambia la coltura selezionata rispetto al ciclo precedente.

Non limitarti a descrivere il codice.

Dimostra attraverso la traccia osservabile che `ROICropAgent` esegue realmente la selezione dinamica prevista.

Indica quali colture vengono effettivamente selezionate durante l'episodio osservato e perché risultano preferibili in quei momenti secondo la formula ROI.

Verifica inoltre che il farmer rimanga sulla casella `(4, 4)` e che non vengano emesse azioni `MOVE`.

## 5. Verifica indipendente del benchmark E02

Non assumere come corretti i valori riepilogati al termine di BUILD.

Leggi direttamente:

`results/e02_roi_crop.json`

e ricostruisci dai dati grezzi le metriche.

Verifica innanzitutto che il benchmark contenga effettivamente:

* 30 episodi;
* 10 episodi contro `pass`;
* 10 episodi contro `random`;
* 10 episodi contro `starter`;
* 720 turni previsti per episodio.

Ricalcola indipendentemente:

* Completion Rate;
* Disqualification Rate;
* Overall Win Rate;
* Win Rate vs `pass`;
* Win Rate vs `random`;
* Win Rate vs `starter`;
* Mean Final Money;
* Median Final Money;
* dispersione di Final Money;
* Agent Mean Turn Latency;
* Simulation Mean Step Duration.

Per la dispersione utilizza la stessa definizione statistica adottata nel confronto consolidato con E01 e dichiarala esplicitamente.

Confronta i valori ricalcolati con quelli dichiarati al termine di BUILD:

* Completion Rate: `100.00%`;
* Disqualification Rate: `0.00%`;
* Overall Win Rate: `100.00%`;
* Win Rate vs `starter`: `100.00%`;
* Mean Final Money: `$5857.17 ± $130.14`;
* Median Final Money: `$5837.00`;
* Agent Mean Turn Latency: `0.0267 ms/turno`;
* Simulation Mean Step Duration: `3.45 ms/step`.

Segnala qualsiasi differenza, anche piccola.

## 6. Verifica del confronto E01 → E02

Utilizzando direttamente:

`results/e01_baseline.json`

e:

`results/e02_roi_crop.json`

ricostruisci il confronto quantitativo tra E01 ed E02.

Verifica in particolare il calcolo dichiarato:

`Mean Final Money: 3578.80 → 5857.17`

e ricalcola:

* incremento assoluto;
* incremento percentuale.

Verifica quindi se il valore dichiarato di **+63.66%** sia corretto.

Controlla inoltre il passaggio:

`Win Rate vs starter: 0% → 100%`

e verifica che in E01 i 10 episodi contro `starter` fossero effettivamente pareggi e che in E02 siano effettivamente vittorie.

Distingui chiaramente:

* risultati osservati;
* target sperimentali;
* interpretazioni.

## 7. Verifica della submission

Verifica che:

`submission/submission.py`

sia stato realmente rigenerato dal codice E02 e che implementi la stessa strategia presente nel repository.

Controlla che il bundling non introduca differenze comportamentali rispetto a:

`src/agricola/agent.py`

e:

`src/agricola/strategy/roi_crop.py`.

Esegui lo smoke test della submission.

Non effettuare ancora una nuova submission sulla piattaforma Kaggle.

## 8. Verifica dei test

Esegui l'intera suite:

`pytest tests/`

Verifica:

* numero dei test raccolti;
* numero dei test superati;
* ruolo dei nuovi test E02;
* copertura concettuale dei test rispetto alla selezione ROI.

Non aggiungere nuovi test durante VERIFY.

Se individui una lacuna nella copertura, documentala senza correggerla.

## 9. Valutazione finale

Al termine classifica separatamente:

### Implementazione

`PASSED`, `PASSED WITH OBSERVATIONS` oppure `FAILED`.

### Isolamento sperimentale

`PASSED`, `PASSED WITH OBSERVATIONS` oppure `FAILED`.

### Benchmark

`PASSED`, `PASSED WITH OBSERVATIONS` oppure `FAILED`.

### Ipotesi E02

Indica esclusivamente sulla base delle evidenze se risulta:

* supportata;
* parzialmente supportata;
* non supportata.

Non utilizzare il termine "confermata" come sinonimo di "dimostrata": il benchmark costituisce evidenza sperimentale nelle condizioni testate, non una dimostrazione generale della superiorità della strategia.

## 10. Vincoli

Durante VERIFY:

* non modificare `ROICropAgent`;
* non modificare `CarrotLoopAgent`;
* non modificare `GameState`;
* non modificare test;
* non modificare benchmark runner;
* non modificare submission;
* non modificare risultati JSON;
* non ottimizzare la strategia;
* non effettuare submission Kaggle;
* non aggiornare ancora `PROJECT_STATE.md`;
* non aggiornare ancora `EXPERIMENT_LOG.md`;
* non effettuare commit.

Se emerge un problema, documentalo e fermati prima di correggerlo.

## Al termine

Produci un rapporto strutturato contenente:

1. verifica dell'isolamento sperimentale;
2. verifica della formula ROI;
3. traccia comportamentale osservabile;
4. colture effettivamente selezionate;
5. benchmark E02 ricalcolato;
6. confronto E01 → E02 ricalcolato;
7. verifica della submission;
8. esito dei test;
9. eventuali anomalie o discrepanze;
10. valutazione finale di implementazione, isolamento, benchmark e ipotesi E02;
11. `git status`.

Non modificare documentazione per registrare il rapporto durante questa esecuzione.

Fermati senza commit e attendi la REVIEW umana.
