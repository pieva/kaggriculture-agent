# E05-02 — Piano di implementazione HIRE / Multi-Worker Scaling

Stiamo proseguendo **E05 — HIRE / Multi-Worker Scaling** del progetto Kaggriculture Agent.

Segui rigorosamente il metodo di progetto:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

La fase **DEFINE** è stata completata nel documento:

`docs/experiments/E05-01_HIRE_Capability_Analysis.md`

La raccomandazione della DEFINE è:

`PROCEED TO PLAN`

Questo prompt riguarda **esclusivamente la fase PLAN**.

**Non implementare ancora E05.**  
**Non modificare il codice di produzione.**  
**Non modificare la submission standalone.**  
**Non eseguire ancora il benchmark E05.**

---

## 1. Domanda sperimentale

E04 ha dimostrato che l'espansione del footprint produttivo E03 da 4 a 9 tile, mantenendo un singolo farmer, provoca una significativa regressione economica.

### E03 — Multi-Tile Scaling

- Agent: `MultiTileROIAgent`
- Footprint: 4 tile
- Mean Final Money: `$14682.47 ± $1164.33`
- Win Rate vs `starter`: `100%`

### E04 — Initial NW Scaling

- Agent: `NWClusterROIAgent`
- Footprint: 9 tile
- Capacità lavorativa: 1 farmer
- Mean Final Money: `$11232.47 ± $661.26`
- Differenza vs E03: `-$3450.00`
- Differenza percentuale vs E03: `-23.49%`
- Total Weed Conversions: `238`
- Mean Unwatered End-of-Day Ratio: `3.33%`
- Completion Rate: `100%`
- Disqualification Rate: `0%`

E04 ha quindi falsificato l'ipotesi secondo cui la policy single-farmer esistente potesse scalare economicamente da 4 a 9 tile.

La domanda sperimentale di E05 è:

> **L'aggiunta giornaliera di una farm hand tramite `HIRE` fornisce capacità lavorativa sufficiente a rendere economicamente sostenibile il footprint E04 da 9 tile?**

---

## 2. Vincoli verificati di HIRE

Utilizza come vincoli di progetto i risultati verificati in E05-01.

In particolare:

- `HIRE` è disponibile tramite l'azione di mercato:
  `action["market"] = [["HIRE"]]`;
- il primo ingaggio di ogni giorno costa `$1`;
- il costo viene addebitato immediatamente;
- la farm hand viene creata durante la fase mercato e può agire dal turno successivo;
- le farm hand hanno posizione indipendente;
- le farm hand sono controllate esplicitamente dall'agente centralizzato;
- le farm hand possono eseguire le stesse azioni agricole rilevanti del farmer principale;
- le farm hand scompaiono alla fine di ogni giornata;
- `hires_today` viene azzerato a fine giornata;
- una farm hand deve quindi essere riassunta ogni giorno;
- farmer e farm hand condividono le risorse economiche della farm, ma dispongono di inventari trasportati individuali;
- richieste aggregate di `PLANT` possono essere annullate atomicamente se la domanda complessiva di semi supera la disponibilità.

Non riaprire l'analisi generale delle capacità di `HIRE`, salvo che durante la preparazione del PLAN emerga una contraddizione concreta.

Se emerge una contraddizione con E05-01, documentala e **FERMATI**, senza modificare silenziosamente il disegno sperimentale.

---

## 3. Disegno sperimentale

L'esperimento deve confrontare:

### Controllo — E04

- 1 farmer;
- footprint NW da 9 tile;
- policy operativa derivata da E03;
- nessun `HIRE`.

### Trattamento — E05

- 1 farmer;
- 1 farm hand assunta ogni giorno;
- stesso footprint NW da 9 tile;
- stessa policy operativa derivata da E03, dove tecnicamente applicabile;
- partizionamento worker-to-tile fisso.

La variabile sperimentale primaria è:

> **Capacità lavorativa aggiuntiva introdotta tramite un singolo `HIRE` giornaliero.**

E05 comprende **un solo trattamento**.

Non testare due farm hand.

Se una farm hand risultasse insufficiente, l'eventuale aumento del numero di worker dovrà costituire un esperimento successivo separato.

---

## 4. Meccanismo di coordinamento fisso

L'implementazione multi-worker richiede un meccanismo deterministico per impedire ai due worker di competere sulle stesse tile.

Per E05 utilizza un **partizionamento spaziale fisso 4:5**.

### Farmer principale — 4 tile

`{(4,4), (4,3), (3,4), (3,3)}`

### Farm Hand 1 — 5 tile

`{(4,2), (3,2), (2,4), (2,3), (2,2)}`

Vincolo metodologico fondamentale:

> Il partizionamento 4:5 è un meccanismo di coordinamento fisso necessario per rendere operativo il trattamento `HIRE`. **Non costituisce una seconda variabile sperimentale da ottimizzare.**

Non cercare un partizionamento migliore.

Non confrontare partizionamenti alternativi.

Non effettuare ribilanciamento dinamico delle tile durante E05.

L'eventuale ottimizzazione dell'allocazione dei worker appartiene a esperimenti successivi.

---

## 5. Variabili da mantenere costanti

Mantieni invariati rispetto a E04:

- footprint NW da 9 tile:
  `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`;
- logica ROI delle colture ereditata da E03;
- `yield = 2.0`, dove attualmente utilizzato;
- priorità operativa:
  `HARVEST > PLANT > WATER`;
- vendita immediata dei prodotti;
- assenza di gestione dell'orizzonte di fine stagione;
- nessun `DIG`;
- nessun `BUY_LAND`;
- nessuna strategia Water-First;
- nessuna nuova euristica di selezione delle colture;
- nessun ridimensionamento dinamico del footprint;
- nessuna ottimizzazione dinamica del numero di worker;
- nessun partizionamento alternativo;
- stessi opponent;
- stesso numero di episodi;
- stessi criteri di riproducibilità utilizzati in E03/E04;
- stessi vincoli di timeout.

Non introdurre ottimizzazioni non necessarie.

---

## 6. Modifiche architetturali minime

Progetta il più piccolo insieme di modifiche architetturali necessario per supportare E05.

Prima di definire esattamente i file da modificare, verifica il codice corrente.

### `GameState`

Valuta la necessità di:

- esporre le posizioni correnti delle farm hand;
- esporre il numero di farm hand attive, se non già direttamente disponibile.

Evita modifiche alle astrazioni di stato non necessarie a E05.

### `ActionBuilder`

Valuta le modifiche minime necessarie per:

- supportare gli ordini di mercato `HIRE`;
- supportare le action list delle farm hand;
- preservare, dove possibile, l'API esistente per le azioni del farmer.

L'action object finale deve rispettare esattamente lo schema dell'ambiente.

### Strategia E05

Pianifica un nuovo modulo di strategia senza modificare la strategia E04 già shipped.

Nome concettuale atteso:

`HIRENWClusterROIAgent`

oppure un equivalente coerente con le convenzioni effettive del repository.

La strategia E04 deve restare disponibile e invariata come riferimento di controllo.

### Standalone submission

Pianifica le modifiche minime necessarie affinché:

`scripts/build_submission.py`

possa generare:

`submission/submission.py`

contenente l'agente E05 e tutte le astrazioni necessarie.

Non implementare queste modifiche durante PLAN.

---

## 7. Ciclo giornaliero di HIRE

Il PLAN deve definire esplicitamente il lifecycle giornaliero della farm hand.

Specifica almeno:

1. rilevazione dell'inizio di una nuova giornata;
2. emissione di esattamente un ordine `HIRE`;
3. comportamento durante il turno in cui la farm hand non è ancora disponibile;
4. rilevazione della nuova farm hand dal turno successivo;
5. assegnazione alla farm hand della partizione fissa da 5 tile;
6. funzionamento ordinario durante la giornata;
7. rimozione automatica attesa della farm hand a fine giornata;
8. ripetizione del processo il giorno successivo.

L'implementazione deve rilevare l'esistenza della farm hand dallo stato reale dell'ambiente.

Non assumere che un precedente `HIRE` sia necessariamente riuscito.

Impedisci ingaggi duplicati nella stessa giornata.

---

## 8. Scheduling dei worker

Entrambi i worker devono mantenere la priorità operativa E03/E04:

`HARVEST > PLANT > WATER`

applicandola esclusivamente alla propria partizione.

Progetta uno scheduling deterministico locale per ciascun worker.

Per ogni worker:

1. considera esclusivamente le tile assegnate;
2. individua la classe di task attiva con priorità più elevata;
3. all'interno di quella classe utilizza la regola di routing/distanza esistente, dove applicabile;
4. esegui movimento o azione sulla tile;
5. evita di selezionare tile assegnate all'altro worker.

Non introdurre comportamento Water-First.

Lo scopo di E05 è verificare la capacità lavorativa aggiuntiva mantenendo la policy esistente, non correggere contemporaneamente la policy.

---

## 9. Coordinamento delle risorse condivise

Il PLAN deve affrontare esplicitamente le risorse condivise.

### Semi

Poiché una domanda aggregata di `PLANT` può essere annullata atomicamente quando i semi disponibili non sono sufficienti, definisci il meccanismo deterministico minimo con cui E05 eviterà ordini di semina simultanei non validi.

Non ridisegnare inutilmente la policy economica.

### Denaro

Considera il costo reale di `$1/giorno` per `HIRE`.

Non compensare artificialmente tale costo nei risultati.

`Final Money` deve includere la spesa effettiva per gli ingaggi.

### Prodotti e shed

Mantieni il comportamento esistente di gestione e vendita dei prodotti, salvo modifiche minime necessarie per compatibilità con `HIRE`.

### Inventari

Considera che gli inventari trasportati sono individuali per worker mentre l'economia della farm è condivisa.

Non introdurre ottimizzazioni dell'inventario se non necessarie alla correttezza.

---

## 10. Instrumentation

E05 deve produrre evidenze sufficienti per distinguere:

- successo dello scaling di capacità;
- sottoutilizzo della farm hand;
- persistenza della starvation operativa;
- fallimento economico nonostante un miglioramento operativo.

Mantieni tutte le metriche E04 ancora applicabili.

### Metriche principali

Registra almeno:

- Total Episodes;
- Completion Rate;
- Disqualification Rate;
- Overall Win Rate;
- wins / losses / draws;
- Mean Final Money;
- sample standard deviation (`ddof=1`);
- Median Final Money;
- breakdown per opponent.

### Metriche comparative

Calcola:

- differenza assoluta di Mean Final Money vs E04;
- differenza percentuale vs E04;
- differenza assoluta di Mean Final Money vs E03;
- differenza percentuale vs E03.

### Diagnostica agricola

Mantieni o estendi:

- Weed Conversions;
- Mean Unwatered End-of-Day Ratio.

Per Weed Conversions confronta E05 con E04 indicando:

- variazione assoluta;
- variazione percentuale.

### Diagnostica HIRE

Dove misurabile in modo affidabile, registra:

- total `HIRE` actions;
- successful hires;
- hires per episode;
- costo totale atteso/effettivo degli ingaggi;
- worker-active turns;
- utilizzo della farm hand;
- azioni eseguite dal farmer;
- azioni eseguite dalla farm hand;
- distribuzione delle principali azioni per worker.

Non introdurre metriche che non possano essere misurate in modo affidabile dallo stato o dalle azioni disponibili.

### Performance

Registra:

- Agent Mean Turn Latency;
- Maximum Turn Latency, se supportata dall'infrastruttura di benchmark;
- eventuali timeout o disqualification.

---

## 11. Interpretazione di successo e fallimento

Non introdurre soglie arbitrarie come `$13000`, `<30 weeds` o `>100 weeds`.

Utilizza confronti sperimentali diretti.

### Successo economico minimo

Il criterio primario è:

`Mean Final Money E05 > Mean Final Money E04`

con riferimento:

`E04 = $11232.47 ± $661.26`

Riporta:

- miglioramento assoluto;
- miglioramento percentuale.

Questo determina se la capacità lavorativa aggiuntiva migliora la configurazione da 9 tile risultata inefficiente in E04.

### Successo economico forte

Il criterio di successo forte è:

`Mean Final Money E05 >= Mean Final Money E03`

con riferimento:

`E03 = $14682.47 ± $1164.33`

Questo determina se la configurazione multi-worker da 9 tile raggiunge o supera il benchmark economico precedente da 4 tile.

### Successo operativo

Valuta la diagnostica agricola in termini comparativi.

Confronta in particolare E05 con:

`E04 Total Weed Conversions = 238`

riportando:

- totale E05;
- variazione assoluta;
- variazione percentuale.

`0` Weed Conversions costituisce un risultato operativo forte, perché rappresenta l'eliminazione completa del failure mode osservato.

Confronta inoltre il Mean Unwatered End-of-Day Ratio con il valore E04:

`3.33%`

### Fallimento

E05 falsifica l'ipotesi economica primaria se:

`Mean Final Money E05 <= Mean Final Money E04`

a condizione che siano state verificate integrità del benchmark e correttezza dell'implementazione.

Durante REVIEW distingui almeno:

1. **fallimento economico di HIRE** — la capacità operativa migliora, ma il risultato economico netto non migliora;
2. **capacità insufficiente** — una farm hand aggiuntiva non riesce comunque a servire il footprint;
3. **fallimento di coordinamento** — lo scheduling multi-worker impedisce di testare correttamente la capacità aggiuntiva;
4. **fallimento di implementazione** — `HIRE` o le azioni delle farm hand non funzionano secondo la semantica verificata.

Non confondere questi esiti.

---

## 12. Interpretazione economica

Il costo diretto deterministico previsto per una farm hand è:

`$1/giorno`

Se l'episodio comprende effettivamente 30 giorni, il costo complessivo atteso è:

`$30/episodio`

Verifica la struttura effettiva giorno/episodio nel repository e nell'ambiente prima di assumere `$30` come valore definitivo.

Il benchmark deve misurare il `Final Money` effettivo dopo i costi di ingaggio.

Non formulare previsioni non osservate sul miglioramento economico E05.

Non utilizzare intervalli speculativi di profitto come:

`+$3,000 ... +$10,000+`

come evidenza o risultato atteso.

L'effetto economico deve essere determinato empiricamente dal benchmark E05.

---

## 13. Piano dei test

Definisci i test unitari e di integrazione necessari prima del benchmark.

Considera almeno:

1. serializzazione corretta di `HIRE`;
2. esattamente un `HIRE` giornaliero;
3. assenza di `HIRE` duplicati nella stessa giornata;
4. parsing corretto dello stato delle farm hand;
5. generazione invariata delle azioni farmer quando non esiste una hand;
6. serializzazione corretta delle azioni della hand;
7. rispetto del partizionamento fisso 4:5;
8. assenza di targeting intenzionale delle tile dell'altro worker;
9. sicurezza nell'utilizzo condiviso dei semi;
10. generazione deterministica delle azioni;
11. scomparsa della hand a fine giornata;
12. nuovo ingaggio il giorno successivo;
13. generazione della standalone submission;
14. import/esecuzione dell'agente standalone;
15. regressione dell'intera test suite esistente.

Non legare inutilmente i test a dettagli implementativi.

---

## 14. Protocollo di benchmark

Salvo evidenze contrarie nel repository, mantieni il protocollo consolidato utilizzato per E03/E04:

- `30` episodi totali;
- stesso insieme di opponent;
- stessa distribuzione degli episodi per opponent;
- stessa configurazione dell'ambiente;
- stesso approccio di seeding/riproducibilità;
- stessi timeout.

Prima della BUILD identifica nel repository il comando e la configurazione esatti attualmente utilizzati per il benchmark.

Non modificare silenziosamente il protocollo.

I risultati E05 devono restare direttamente confrontabili con E04 ed E03.

---

## 15. Artifact previsti

Il PLAN deve identificare esattamente i file che saranno creati o modificati durante BUILD.

### Da creare

Includi almeno:

`docs/plans/E05_HIRE_MultiWorker_Scaling.md`

e il nuovo modulo della strategia E05.

### Da modificare

Limita le modifiche ai file realmente necessari per:

- supporto dello stato;
- supporto delle azioni;
- test;
- instrumentation;
- standalone build;
- documentazione nelle fasi successive.

Durante PLAN **non modificare questi file**.

---

## 16. Sequenza di implementazione

Produci una sequenza BUILD concreta e supervisionabile.

Preferisci passi piccoli e verificabili, ad esempio:

1. supporto lettura stato delle farm hand;
2. supporto `HIRE` e serializzazione delle azioni;
3. test delle primitive `HIRE`;
4. implementazione del partizionamento fisso;
5. implementazione del lifecycle giornaliero `HIRE`;
6. implementazione dello scheduling locale dei worker;
7. protezione delle risorse condivise;
8. aggiunta della diagnostica E05;
9. esecuzione dei test mirati;
10. esecuzione dell'intera regression suite;
11. generazione della standalone submission;
12. smoke evaluation;
13. solo dopo il superamento dei controlli, benchmark completo da 30 episodi.

Adatta questa sequenza all'architettura effettiva del repository.

Per ogni passo BUILD principale specifica una condizione esplicita di verifica.

---

## 17. Rischi e condizioni di STOP

Identifica i rischi concreti prima della BUILD.

Considera almeno:

- emissione accidentale di più `HIRE`;
- indicizzazione errata delle farm hand;
- errore nel timing dello spawn;
- emissione di azioni hand prima della sua esistenza;
- conflitti nelle azioni `PLANT`;
- worker che selezionano la stessa tile;
- inefficienza di movimento;
- sottoutilizzo della farm hand;
- errata assunzione di persistenza tra giornate;
- instrumentation che modifica il comportamento dell'agente;
- errore nel bundling standalone;
- perdita di confrontabilità del benchmark.

Definisci condizioni di STOP esplicite qualora:

- l'implementazione contraddica la semantica verificata in E05-01;
- `HIRE` non possa essere introdotto senza modificare sostanzialmente altre variabili sperimentali;
- il partizionamento fisso risulti tecnicamente incompatibile con il modello dell'ambiente;
- non sia possibile preservare la confrontabilità con E04.

---

## 18. Documento PLAN richiesto

Crea:

`docs/plans/E05_HIRE_MultiWorker_Scaling.md`

Il documento deve contenere almeno:

1. **Obiettivo**
2. **Domanda sperimentale**
3. **Ipotesi**
4. **Controllo e trattamento**
5. **Variabile sperimentale**
6. **Variabili mantenute costanti**
7. **Vincoli HIRE verificati**
8. **Impatto sull'architettura**
9. **Partizionamento fisso dei worker**
10. **Lifecycle giornaliero HIRE**
11. **Scheduling dei worker**
12. **Coordinamento delle risorse condivise**
13. **Instrumentation**
14. **Interpretazione di successo/fallimento**
15. **Piano dei test**
16. **Protocollo di benchmark**
17. **Sequenza di implementazione**
18. **Rischi**
19. **Condizioni di STOP**
20. **File previsti**
21. **Decisione di readiness per BUILD**

Concludi con esattamente una delle seguenti raccomandazioni:

- `READY FOR BUILD`
- `PLAN REVISION REQUIRED`
- `EXPERIMENT NOT VIABLE`

motivandola.

---

## 19. Condizione di arresto

Dopo aver creato il PLAN:

1. riassumi il disegno sperimentale finale;
2. riassumi le modifiche architetturali necessarie;
3. mostra il partizionamento fisso dei worker;
4. riassumi il lifecycle `HIRE`;
5. mostra la instrumentation prevista;
6. mostra i criteri di interpretazione di successo/fallimento;
7. elenca la sequenza BUILD;
8. elenca rischi e condizioni di STOP;
9. indica il percorso del documento creato;
10. mostra `git status --short`.

Poi **FERMATI**.

Non implementare E05.

Non modificare il codice di produzione.

Non generare la standalone submission.

Non eseguire il benchmark E05.

Attendi approvazione esplicita prima di passare da **PLAN** a **BUILD**.