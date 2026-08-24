# E03 — Implementation Plan Review

Il piano E03 è approvato nella sua impostazione generale.

La soluzione sperimentale selezionata è:

**Compact 2×2 Cluster**

con le quattro tile:

`{(4,4), (4,3), (3,4), (3,3)}`

La scelta è coerente con l'obiettivo di isolare il **Multi-Tile Production Scaling** rispetto a E02.

Prima di autorizzare BUILD, aggiorna però l'Implementation Plan nei seguenti punti.

## 1. Correggere la logica delle priorità

Il piano dichiara:

`HARVEST > PLANT > WATER`

ma stabilisce anche che qualsiasi azione disponibile sulla tile corrente venga eseguita immediatamente.

Queste due regole possono entrare in conflitto.

Adotta invece una gerarchia non ambigua:

1. costruisci `HARVEST_SET`;
2. se non vuoto, seleziona al suo interno la tile a minima distanza Manhattan;
3. altrimenti usa `PLANT_SET` con lo stesso criterio;
4. altrimenti usa `WATER_SET`;
5. se il target coincide con la posizione corrente, esegui l'azione;
6. altrimenti muoviti di un passo verso il target.

La distanza deve quindi essere utilizzata **all'interno della classe di priorità più alta disponibile**, non per superare la priorità dell'azione.

Mantieni un tie-breaking deterministico.

## 2. Correggere il criterio Mean Final Money

Non utilizzare:

`Mean Final Money > $10,000`

come soglia obbligatoria di successo, perché non abbiamo ancora evidenza empirica sufficiente per stabilire tale valore.

Definisci invece:

### criterio primario

`Mean Final Money E03 > Mean Final Money E02 ($5857.17)`

Registrare inoltre:

- differenza assoluta;
- differenza percentuale;
- deviazione standard;
- mediana.

`$10,000` può eventualmente essere mantenuto esclusivamente come **target esplorativo**, non come requisito di validazione.

## 3. Precisare il comportamento degli ordini di mercato

Non descrivere gli ordini di mercato come genericamente `Turn-free`.

Utilizza una formulazione coerente con l'evidenza empirica:

> Gli ordini di mercato possono essere emessi nello stesso turno dell'azione del farmer e non richiedono quindi di rinunciare all'azione del farmer in quel turno.

## 4. Correggere l'ipotesi sperimentale

Evitare il termine `significantly` se non viene definito un test di significatività statistica.

Utilizzare una formulazione del tipo:

> Holding E02's economic strategy constant, expanding cultivation from one tile to a compact four-tile 2×2 cluster using spatial task prioritization will increase productive throughput and produce a measurable improvement in Mean Final Money without introducing operational instability or unacceptable decision latency.

## 5. Distinguere variabile strategica e modifiche abilitanti

Esplicitare che E03 mantiene il principio:

**una modifica strategica principale per esperimento**

La modifica strategica è:

`single-tile production → multi-tile production`

Le seguenti modifiche sono invece considerate **meccanismi operativi necessari per rendere possibile la variabile sperimentale**:

- correzione del formato delle azioni di movimento;
- navigazione Manhattan;
- selezione del target;
- gestione dello stato di quattro tile;
- acquisto di semi coerente con il numero di tile vuote.

Non devono essere considerate nuove strategie economiche indipendenti.

## 6. Conservare gli altri vincoli E02

Restano invariati:

- `select_best_crop`;
- formula ROI E02 con `Yield = 2`;
- vendita immediata;
- nessun market timing;
- nessun end-of-season cutoff;
- nessun `BUY_LAND`;
- configurazione benchmark E01/E02;
- 30 episodi;
- 720 step;
- avversari `pass`, `random`, `starter`.

Non introdurre altre ottimizzazioni.

## Output

Aggiorna:

`docs/plans/E03_Multi_Tile_Scaling.md`

Mostra poi soltanto:

1. modifiche apportate al piano;
2. ipotesi definitiva;
3. strategia definitiva di target selection;
4. criteri di successo definitivi;
5. stato Git.

## STOP

Non implementare codice.

Non eseguire BUILD.

Attendi l'approvazione esplicita prima di procedere.