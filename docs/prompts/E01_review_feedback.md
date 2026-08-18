La prima implementazione E01 è sostanzialmente approvata: la baseline funziona, il benchmark è stato eseguito e l'infrastruttura prevista dal piano è stata in gran parte realizzata.

Prima di considerare E01 conclusa, però, la revisione indipendente del repository ha individuato alcuni aspetti da correggere.

Non modificare la strategia `CarrotLoopAgent` e non introdurre ancora ottimizzazioni competitive. Questa attività serve esclusivamente a consolidare E01 e a rendere verificabili e corrette le evidenze prodotte.

## 1. README mancante

Il walkthrough dichiara la presenza di `README.md`, ma il file non esiste nel repository.

Inoltre `pyproject.toml` contiene:

```toml
readme = "README.md"
```

Crea quindi il `README.md` previsto, limitandolo alla documentazione effettiva dello stato E01 del progetto.

## 2. Igiene del repository

Nel repository sono stati generati file e directory che non devono essere versionati, tra cui:

- `.venv/`
- `.pytest_cache/`
- `__pycache__/`
- `*.pyc`

Aggiungi un `.gitignore` appropriato e rimuovi dagli artefatti da versionare eventuali cache Python generate durante test ed esecuzioni.

Non eliminare i risultati E01 che costituiscono evidenza dell'esperimento.

## 3. Invalid Action Rate

La documentazione dichiara:

> Invalid Action Rate (%): percentuale di turni in cui l'azione restituita è stata rifiutata o non valida.

La revisione del runner mostra però che il contatore viene aggiornato quando un episodio termina con stato `INVALID` per l'agente.

Questa implementazione non misura quindi direttamente la percentuale di singoli turni contenenti azioni invalide.

Verifica il comportamento effettivo del runner e scegli una delle due soluzioni:

- implementare realmente una metrica per-turno, se l'ambiente consente di rilevarla in modo affidabile;
- oppure rinominare la metrica affinché descriva esattamente ciò che viene misurato.

Non presentare come misurato un dato che l'infrastruttura non permette di osservare direttamente.

## 4. Mean Latency per Turn

La documentazione dichiara che `Mean Latency` rappresenta il tempo medio impiegato dall'agente per turno.

La revisione mostra invece che il runner misura il tempo complessivo di `env.run(...)` e lo divide per il numero di step. Questo valore comprende quindi anche l'esecuzione dell'ambiente, dell'avversario e altro overhead della simulazione.

Anche in questo caso scegli una soluzione tecnicamente corretta:

- misura direttamente il tempo di esecuzione del nostro agente, se può essere fatto senza alterare significativamente la simulazione;
- oppure rinomina la metrica affinché rappresenti correttamente il tempo medio della simulazione per step.

Non attribuire all'agente una latenza che non è stata direttamente misurata.

## 5. Test e livello di verifica

I test esistenti sono stati eseguiti con successo, ma la revisione ha rilevato che alcuni test di integrazione utilizzano episodi abbreviati invece di una stagione completa di 720 turni.

Non è necessario rendere tutti i test lunghi o costosi.

Verifica però che la documentazione distingua chiaramente tra:

- unit test;
- smoke/integration test;
- benchmark completo E01 su 720 turni.

Le affermazioni nel walkthrough devono corrispondere esattamente al livello di verifica realmente effettuato.

## 6. Aggiornamento delle evidenze

Dopo le correzioni:

1. esegui nuovamente la suite di test;
2. esegui nuovamente il benchmark E01 se le modifiche apportate possono influenzarne le metriche;
3. verifica che `submission/submission.py` continui a essere valida;
4. aggiorna `docs/EXPERIMENT_LOG.md`;
5. aggiorna `docs/PROJECT_STATE.md`;
6. aggiorna il walkthrough E01 affinché descriva esclusivamente ciò che è effettivamente presente e verificato nel repository.

Mantieni separati:

- risultati osservati;
- metriche effettivamente misurate;
- interpretazioni dei risultati.

Al termine presenta le modifiche effettuate, i test eseguiti e gli eventuali nuovi risultati.

Non iniziare E02 e non introdurre strategie competitive aggiuntive.