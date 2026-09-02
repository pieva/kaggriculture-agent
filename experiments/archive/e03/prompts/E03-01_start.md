# E03 — Multi-Tile Scaling — DEFINE & PLAN

Stiamo continuando il progetto sperimentale **Kaggriculture Agent** seguendo il metodo supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Branch:

`main`

Prima di iniziare:

1. verifica lo stato Git;
2. verifica che il working tree sia pulito;
3. esamina la documentazione consolidata di E01 ed E02;
4. considera `docs/NEW_SESSION.md` come punto di ripartenza del progetto;
5. esamina il codice corrente di `ROICropAgent`, i benchmark E01/E02 e le evidenze di simulazione disponibili.

## Stato sperimentale

Sono state completate due iterazioni.

### E01 — CarrotLoopAgent

Baseline operativa:

- coltura fissa `CARROT`;
- singola tile `(4, 4)`;
- nessun movimento;
- ciclo fondamentale:

`BUY_SEED → PLANT → WATER → HARVEST → SELL`

### E02 — ROICropAgent

E02 modifica una sola variabile strategica rispetto a E01:

**selezione dinamica della coltura sulla base del ROI/giorno e della liquidità disponibile.**

La strategia mantiene:

- singola tile `(4, 4)`;
- nessun movimento;
- vendita immediata;
- infrastruttura di benchmark invariata.

Il benchmark locale E02 ha prodotto:

- Mean Final Money: `$5857.17`;
- Overall Win Rate: `100%`;
- Win Rate vs `starter`: `100%`.

Rispetto alla baseline E01:

- Mean Final Money: `$3567.63 → $5857.17`;
- incremento: `+64.18%`.

Le analisi hanno mostrato che `MELON` è la coltura economicamente dominante nelle condizioni osservate.

## Evidenza competitiva aggiornata

Il Kaggle Skill Rating è dinamico e deve essere tenuto distinto dalle metriche del benchmark locale.

Dopo una fase iniziale in cui E02 era scesa sotto E01, l'osservazione più recente mostra una situazione stabilizzata con:

- E01 `CarrotLoopAgent`: **255.2**
- E02 `ROICropAgent`: **290.8**

Questa evidenza non dimostra che il miglioramento competitivo sia proporzionale al miglioramento del benchmark locale.

Mostra però che, nell'osservazione più recente, E02 presenta anche un vantaggio competitivo rispetto a E01.

Non confrontare numericamente:

- Mean Final Money locale;
- Kaggle Skill Rating.

Sono metriche differenti.

## E03 — ipotesi sperimentale proposta

Il principale limite strutturale che vogliamo analizzare in E03 è il seguente:

**E02 utilizza una sola tile `(4, 4)`, lasciando inutilizzata gran parte della griglia disponibile.**

La variabile sperimentale candidata per E03 è quindi:

# Multi-Tile Scaling

Ipotesi:

> Mantenendo invariata la strategia economica di E02, l'utilizzo coordinato di più tile può aumentare la capacità produttiva e migliorare la performance rispetto al ROICropAgent single-tile.

La progressione sperimentale deve rimanere leggibile:

`E01 operational baseline → E02 economic crop selection → E03 production scaling`

## Vincolo fondamentale

E03 deve modificare **una sola dimensione strategica principale** rispetto a E02.

La variabile da modificare è:

**utilizzo di più tile invece della singola tile `(4, 4)`.**

Non introdurre contemporaneamente:

- market timing;
- ottimizzazione end-of-season;
- modifiche alla formula ROI;
- utilizzo di `max_yield` al posto del modello corrente;
- nuove strategie competitive non necessarie al multi-tile;
- altre ottimizzazioni economiche.

La logica di selezione della coltura introdotta in E02 deve rimanere sostanzialmente invariata.

## Attività richiesta

NON implementare ancora E03.

Esegui esclusivamente **DEFINE e PLAN**.

### 1. Analizza l'ambiente

Determina, attraverso il codice e le API effettivamente disponibili nel repository e nell'ambiente Kaggriculture:

- dimensioni e struttura della griglia utilizzabile;
- posizione iniziale del farmer;
- modalità di movimento;
- azioni necessarie per spostarsi tra tile;
- costo temporale degli spostamenti;
- eventuali costi economici;
- modalità con cui lo stato delle diverse tile viene rappresentato nell'osservazione;
- possibilità di conoscere coltura, stato di crescita, irrigazione e maturità delle singole tile;
- eventuali limiti al numero di tile coltivabili;
- eventuali vincoli che rendano il multi-tile più complesso di una semplice estensione del ciclo single-tile.

Non assumere caratteristiche dell'ambiente che non siano verificabili.

Indica esplicitamente eventuali informazioni che non possono essere determinate dal repository o dalle evidenze disponibili.

### 2. Analizza ROICropAgent

Identifica:

- quali parti dell'agente assumono implicitamente l'esistenza di una sola tile;
- quali stati interni dovrebbero diventare tile-aware;
- quali transizioni del ciclo operativo dovrebbero essere modificate;
- quali componenti della strategia E02 possono invece essere riutilizzate senza modifiche.

Distingui chiaramente:

**logica economica da preservare**

da

**logica operativa da modificare per il multi-tile**.

### 3. Definisci il minimo esperimento multi-tile

Non assumere che utilizzare tutta la griglia sia necessariamente la scelta migliore per E03.

Valuta quale sia la **minima estensione multi-tile** capace di testare l'ipotesi mantenendo l'esperimento interpretabile.

Confronta almeno:

- 2 tile;
- un piccolo insieme fisso di tile adiacenti;
- utilizzo progressivo delle tile in funzione della liquidità;
- utilizzo dell'intera griglia.

Per ciascuna alternativa valuta:

- complessità;
- costo di movimento;
- utilizzo del capitale;
- rischio di introdurre variabili confondenti;
- capacità di attribuire l'eventuale miglioramento al production scaling.

Proponi una scelta motivata.

### 4. Definisci la strategia operativa

Per la soluzione raccomandata descrivi:

- come vengono selezionate le tile;
- in quale ordine vengono visitate;
- come viene mantenuto lo stato delle colture;
- come vengono gestiti acquisto, semina, irrigazione, raccolta e vendita;
- come viene riutilizzata la selezione ROI di E02;
- come viene evitata, per quanto possibile, l'introduzione di nuove strategie non necessarie all'esperimento.

### 5. Definisci VERIFY

Progetta prima dell'implementazione le verifiche necessarie.

Devono permettere di osservare almeno:

- utilizzo effettivo di più tile;
- movimento corretto;
- assenza di loop o deadlock;
- corretta gestione indipendente dello stato delle tile;
- completamento dei cicli produttivi;
- comportamento economico;
- assenza di disqualification;
- latenza;
- Mean Final Money;
- Win Rate complessivo;
- Win Rate vs `starter`.

Prevedi inoltre una verifica osservabile in Antigravity che consenta di seguire almeno un episodio e dimostrare concretamente il comportamento multi-tile.

### 6. Mantieni confrontabile il benchmark

Il benchmark E03 deve essere confrontabile con E01 ed E02.

Salvo modifiche strettamente necessarie per supportare il nuovo agente, mantieni invariati:

- numero di episodi;
- durata degli episodi;
- avversari;
- metriche;
- struttura dei risultati;
- modalità di esecuzione.

Qualsiasi modifica infrastrutturale necessaria deve essere esplicitamente documentata.

## Output richiesto

Produci un **Implementation Plan E03** sufficientemente dettagliato da poter essere revisionato prima dell'implementazione.

Il piano deve contenere almeno:

1. stato iniziale verificato;
2. evidenze ricavate dall'ambiente;
3. analisi delle assunzioni single-tile di E02;
4. alternative multi-tile considerate;
5. soluzione raccomandata;
6. ipotesi sperimentale definitiva;
7. variabile indipendente;
8. variabili mantenute costanti;
9. modifiche previste al codice;
10. test previsti;
11. piano VERIFY;
12. metriche di confronto E02 → E03;
13. rischi e possibili confondenti;
14. criteri di successo;
15. file che prevedi di creare o modificare.

Salva il piano nella directory:

`docs/plans/`

utilizzando un nome coerente con la convenzione adottata per gli esperimenti precedenti.

## STOP

**Non modificare il codice dell'agente.**

**Non implementare E03.**

**Non eseguire BUILD.**

Al termine mostra:

- sintesi dell'analisi;
- soluzione multi-tile raccomandata;
- percorso del file del piano creato;
- eventuali dubbi o elementi dell'ambiente che richiedono supervisione.

Attendi la mia approvazione esplicita prima di procedere alla fase BUILD.