# E02 — Preparazione SHIP

L'iterazione **E02 — Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)** è stata implementata, verificata, revisionata e consolidata documentalmente.

Prima della submission reale su Kaggle, prepara gli artefatti finali di SHIP senza effettuare ancora l'invio.

## 1. Verifica finale della suite di test

Esegui:

`pytest tests/`

Conferma:

* numero di test raccolti;
* numero di test superati;
* assenza di regressioni;
* esito dei test specifici di `ROICropAgent`;
* esito degli smoke/integration test;
* esito del test della submission.

Se un test fallisce, fermati e non procedere oltre.

Non modificare il codice per correggere eventuali problemi senza prima segnalarli.

## 2. Rigenerazione della submission standalone

Esegui:

`scripts/build_submission.py`

Rigenera:

`submission/submission.py`

Verifica che il file generato contenga effettivamente la strategia E02:

`ROICropAgent`

e che sia coerente con:

* `src/agricola/agent.py`;
* `src/agricola/strategy/roi_crop.py`;
* `src/agricola/core/state.py`.

Controlla che il bundling non introduca differenze comportamentali rispetto al codice sorgente corrente.

## 3. Smoke test della submission

Esegui il test dedicato alla submission:

`pytest tests/test_submission.py`

Verifica che:

* `submission/submission.py` venga importato correttamente;
* l'entrypoint Kaggle sia valido;
* l'agente completi correttamente la simulazione prevista dal test;
* non vengano emesse eccezioni o azioni invalide.

Se il test fallisce, fermati.

## 4. Verifica della versione da spedire

Conferma che la versione corrente da inviare corrisponda esattamente a E02 e non contenga modifiche successive o non approvate.

La strategia deve essere:

**Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)**

Non introdurre:

* modifiche al ROI;
* gestione dell'orizzonte di fine stagione;
* multi-tile;
* market timing;
* modifiche al modello Yield;
* altre evoluzioni candidate per E03.

La submission E02 deve corrispondere alla versione già benchmarkata e verificata.

## 5. Verifica Git

Controlla:

* branch corrente;
* commit HEAD;
* relazione con `origin/main`;
* working tree;
* file staged;
* file unstaged;
* file untracked.

Il riferimento atteso prima di SHIP è il repository consolidato dopo il commit documentale E02.

Se il working tree non è pulito esclusivamente a causa della rigenerazione deterministica di `submission/submission.py`, mostra il diff e verifica che non rappresenti una modifica sostanziale rispetto alla versione già committata.

Non effettuare commit in questa fase.

## 6. Preparazione del pacchetto Kaggle

Prepara il file/pacchetto esatto da utilizzare per la submission Kaggle E02 secondo i requisiti già verificati in E01.

Utilizza esclusivamente la submission standalone corrente.

Se è necessario creare un archivio ZIP:

* includi soltanto i file richiesti da Kaggle;
* non includere `.venv`, sorgenti modulari, test, risultati o documentazione;
* non includere file temporanei o cache.

Indica chiaramente:

* percorso del file da caricare;
* nome del file;
* contenuto dell'eventuale archivio;
* dimensione finale.

Non effettuare l'upload su Kaggle.

## 7. Confronto con E01 prima della submission

Riporta come riferimento esterno già verificato:

* E01 Kaggle score: `600.0`;
* tag E01: `v0.1-e01-baseline`.

Riporta inoltre i risultati locali E02 già consolidati:

* Mean Final Money E02: `$5857.17`;
* Overall Win Rate: `100.00%`;
* Win Rate vs `starter`: `100.00%`;
* incremento locale rispetto alla baseline E01: `+64.18%`.

Non formulare previsioni certe sullo score Kaggle E02.

La submission reale deve essere trattata come verifica esterna indipendente.

## 8. Evidenza da conservare

Non modificare ancora `PROJECT_STATE.md` o `EXPERIMENT_LOG.md`.

Dopo la submission reale conserveremo separatamente:

* screenshot della submission pronta;
* screenshot della submission completata;
* score Kaggle ottenuto;
* eventuali messaggi di errore;
* confronto con E01.

Non creare ancora questi artefatti se l'upload non è stato effettuato.

## 9. Vincoli

Non:

* modificare la strategia;
* iniziare E03;
* eseguire nuovi benchmark comparativi;
* modificare risultati JSON;
* effettuare commit;
* creare tag Git;
* effettuare push;
* effettuare upload su Kaggle.

Lo scopo è esclusivamente preparare e verificare la versione da spedire.

## Al termine

Mostra:

1. esito completo dei test;
2. esito della rigenerazione di `submission/submission.py`;
3. esito dello smoke test della submission;
4. conferma che la strategia contenuta sia `ROICropAgent`;
5. percorso esatto del file/pacchetto da caricare su Kaggle;
6. contenuto dell'eventuale archivio;
7. dimensione del file/pacchetto;
8. HEAD Git corrente;
9. stato rispetto a `origin/main`;
10. `git status`;
11. conferma che nessun upload Kaggle, commit, push o tag sia stato effettuato.

Fermati e attendi l'approvazione umana prima della submission reale.
