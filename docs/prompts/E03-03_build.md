# E03 — Multi-Tile Scaling — BUILD

Il piano E03 è approvato.

Piano di riferimento:

`docs/plans/E03_Multi_Tile_Scaling.md`

La soluzione autorizzata è:

**Compact 2×2 Multi-Tile Cluster**

Tile gestite:

`{(4,4), (4,3), (3,4), (3,3)}`

Metodo sperimentale:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

DEFINE e PLAN sono completati e approvati.

Procedi ora esclusivamente con la fase:

# BUILD

## Vincolo sperimentale

L'unica modifica strategica principale rispetto a E02 deve restare:

`single-tile production → multi-tile production`

Mantieni invariati:

- `select_best_crop`;
- formula ROI E02 con `Yield = 2`;
- vendita immediata;
- nessun market timing;
- nessun end-of-season cutoff;
- nessun `BUY_LAND`;
- configurazione benchmark;
- durata episodi;
- avversari.

Le modifiche necessarie per navigazione, target selection, gestione delle quattro tile e acquisto semi multi-tile sono considerate meccanismi operativi abilitanti.

Non introdurre ottimizzazioni ulteriori.

## Implementazione autorizzata

Implementa quanto definito nel piano approvato.

In particolare:

### 1. Movement Action Fix

Correggi `ActionBuilder.move()` affinché produca il formato effettivamente accettato dall'ambiente:

- `["NORTH"]`
- `["SOUTH"]`
- `["EAST"]`
- `["WEST"]`

Documenta questa modifica come:

**bug fix infrastrutturale necessario ad abilitare il multi-tile**

e non come nuova strategia sperimentale.

### 2. MultiTileROIAgent

Implementa il nuovo agente multi-tile mantenendo la logica economica di E02.

Cluster:

`{(4,4), (4,3), (3,4), (3,3)}`

Priorità globale:

`HARVEST > PLANT > WATER`

Per ogni classe:

1. costruisci il relativo insieme di tile candidate;
2. scegli la tile a minima distanza Manhattan;
3. usa tie-breaking deterministico `(y, x)`;
4. se il farmer si trova sulla tile target, esegui l'azione;
5. altrimenti muoviti di un solo passo verso il target.

Se nessuna azione è necessaria:

`PASS`

### 3. Market Orders

Mantieni:

- vendita immediata dello shed;
- selezione della coltura tramite la funzione ROI E02;
- acquisto di semi coerente con il numero di tile vuote gestite e con la liquidità disponibile.

Gli ordini di mercato possono essere emessi nello stesso turno dell'azione del farmer.

### 4. Test

Implementa i test previsti dal piano, inclusi almeno:

- formato corretto delle azioni di movimento;
- gestione delle quattro tile;
- priorità `HARVEST > PLANT > WATER`;
- selezione della tile più vicina;
- tie-breaking deterministico;
- acquisto semi multi-tile;
- movimento di un solo passo per turno;
- `PASS` quando nessuna azione è disponibile.

Esegui la suite di test necessaria a verificare la BUILD.

## Documentazione BUILD

Crea una nuova evidenza nella directory:

`docs/versions/`

con nome coerente con le convenzioni E01/E02, ad esempio:

`E03_build_antigravity.md`

Documenta:

- file creati;
- file modificati;
- comportamento implementato;
- bug fix del movimento;
- test eseguiti;
- risultati dei test;
- eventuali deviazioni dal piano.

## Git

Al termine mostra:

- `git status --short`;
- elenco dei file creati/modificati.

Non eseguire ancora commit salvo richiesta esplicita.

# STOP

NON eseguire ancora il benchmark completo E03 da 30 episodi.

NON eseguire VERIFY osservabile.

NON modificare il piano sperimentale.

NON creare o caricare la submission Kaggle.

NON eseguire SHIP.

Al termine mostra esclusivamente:

1. sintesi della BUILD;
2. file modificati/creati;
3. test eseguiti e risultati;
4. eventuali problemi riscontrati;
5. stato Git.

Attendi l'approvazione esplicita prima della fase VERIFY.