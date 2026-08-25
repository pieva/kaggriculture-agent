# E05-03 — BUILD HIRE / Multi-Worker Scaling

Stiamo proseguendo **E05 — HIRE / Multi-Worker Scaling** del progetto Kaggriculture Agent.

Segui rigorosamente il metodo di progetto:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Sono state completate e approvate:

- **DEFINE:** `docs/experiments/E05-01_HIRE_Capability_Analysis.md`
- **PLAN:** `docs/plans/E05_HIRE_MultiWorker_Scaling.md`

La decisione del PLAN è:

`READY FOR BUILD`

Questo prompt riguarda **esclusivamente la fase BUILD**.

Implementa il piano approvato.

**Non eseguire ancora il benchmark comparativo completo da 30 episodi.**  
**Non effettuare ancora la REVIEW economica di E05.**  
**Non effettuare SHIP.**  
**Non creare tag Git.**

Al termine della BUILD dovremo avere un agente E05 tecnicamente funzionante, testato, integrato nella standalone submission e validato tramite una smoke evaluation limitata.

---

## 1. Obiettivo della BUILD

Implementare:

`HIRENWClusterROIAgent`

per testare successivamente l'ipotesi E05:

> L'aggiunta giornaliera di una farm hand tramite `HIRE` fornisce capacità lavorativa sufficiente a rendere economicamente sostenibile il footprint E04 da 9 tile?

La BUILD deve implementare il trattamento approvato senza anticipare conclusioni sperimentali.

Non assumere che `HIRE`:

- elimini necessariamente la starvation;
- azzeri necessariamente le Weed Conversions;
- migliori necessariamente il Mean Final Money;
- raggiunga necessariamente E03.

Questi sono risultati da misurare nella successiva fase VERIFY.

---

## 2. Disegno sperimentale da preservare

### Controllo E04

`NWClusterROIAgent`

- 1 farmer;
- footprint NW da 9 tile;
- nessun `HIRE`;
- policy `HARVEST > PLANT > WATER`.

### Trattamento E05

`HIRENWClusterROIAgent`

- 1 farmer;
- 1 farm hand assunta giornalmente;
- stesso footprint NW da 9 tile;
- stessa policy `HARVEST > PLANT > WATER`;
- stesso modello ROI E03/E04;
- partizionamento spaziale fisso 4:5.

Variabile sperimentale primaria:

> **Capacità lavorativa aggiuntiva introdotta tramite un singolo `HIRE` giornaliero.**

Non introdurre altri treatment.

---

## 3. Vincoli sperimentali

Durante BUILD non introdurre:

- seconda farm hand;
- `DIG`;
- `BUY_LAND`;
- Water-First scheduling;
- nuove euristiche ROI;
- gestione dell'orizzonte terminale;
- footprint diverso dalle 9 tile E04;
- ribilanciamento dinamico dei worker;
- ottimizzazione del partitioning;
- modifiche non necessarie alla policy economica;
- altre ottimizzazioni prestazionali o strategiche.

Se l'implementazione richiede una modifica che altererebbe materialmente una di queste variabili, **FERMATI** e segnalala invece di introdurla autonomamente.

---

## 4. Partizionamento fisso

Implementa esattamente il partitioning approvato.

### Farmer principale — 4 tile

`{(4,4), (4,3), (3,4), (3,3)}`

### Farm Hand 1 — 5 tile

`{(4,2), (3,2), (2,4), (2,3), (2,2)}`

Il partitioning:

- deve essere deterministico;
- deve restare fisso per l'intero esperimento;
- non deve essere ottimizzato;
- non deve essere ribilanciato dinamicamente.

Ogni worker deve selezionare task esclusivamente all'interno della propria partizione.

---

## 5. Step 1 — Supporto dello stato

Ispeziona prima l'implementazione corrente di:

`src/agricola/core/state.py`

Implementa esclusivamente il supporto minimo necessario per leggere le farm hand attive.

Il requisito previsto è una proprietà equivalente a:

`hands_positions`

che restituisca le coordinate correnti delle farm hand come lista di tuple `(x, y)`.

Preserva l'API esistente.

Non modificare altre astrazioni di `GameState` se non necessario.

### Verifica Step 1

Aggiungi o aggiorna test che dimostrino:

- nessuna hand → lista vuota;
- una hand → posizione corretta;
- più hand, se rappresentabili nello stato → ordine e posizioni corretti;
- nessuna regressione sulle proprietà esistenti.

Esegui i test pertinenti prima di procedere.

---

## 6. Step 2 — Supporto delle azioni HIRE e Hand

Ispeziona:

`src/agricola/core/actions.py`

Aggiungi il supporto minimo per:

### HIRE

Generare correttamente:

`action["market"] = [["HIRE"]]`

tramite un helper coerente con l'architettura corrente, ad esempio:

`hire()`

### Azioni farm hand

Supportare:

`action["hands"]`

nel formato richiesto dall'ambiente.

Utilizza un helper coerente con l'API esistente, ad esempio:

`add_hand_action(...)`

senza modificare inutilmente l'interfaccia delle azioni farmer già esistente.

### Verifica Step 2

Testa almeno:

- serializzazione di `HIRE`;
- action object senza hand;
- action object con una hand;
- assenza di regressioni sul farmer;
- formato finale conforme allo schema Kaggriculture.

Esegui i test pertinenti prima di procedere.

---

## 7. Step 3 — Implementazione HIRENWClusterROIAgent

Crea:

`src/agricola/strategy/hire_nw_cluster_roi.py`

Implementa:

`HIRENWClusterROIAgent`

riutilizzando la logica E04 dove possibile, evitando duplicazione non necessaria.

Non modificare il comportamento di:

`NWClusterROIAgent`

che deve restare disponibile come controllo shipped E04.

---

## 8. Lifecycle giornaliero HIRE

Implementa il lifecycle verificato durante DEFINE.

### Inizio giornata

A `hour == 0`:

- controlla lo stato reale;
- verifica che non esistano farm hand attive;
- verifica che non sia già stato effettuato un `HIRE` nella giornata;
- emetti esattamente un `HIRE`.

Non assumere che la hand esista nello stesso turno.

Il farmer continua a operare normalmente sulla propria partizione.

### Turno successivo

Dal turno successivo:

- rileva la farm hand dallo stato;
- se presente, genera la sua azione;
- assegnale esclusivamente la partizione da 5 tile.

### Fine giornata

Non implementare persistenza artificiale della hand.

Lascia che l'ambiente:

- rimuova la hand;
- depositi gli inventari secondo le proprie regole;
- resetti `hires_today`.

### Nuovo giorno

Ripeti il processo sulla base dello stato osservato.

### Guard obbligatorio

L'agente non deve mai emettere accidentalmente più `HIRE` nella stessa giornata.

---

## 9. Scheduling locale dei worker

Mantieni la policy:

`HARVEST > PLANT > WATER`

per entrambi i worker.

Ogni worker deve:

1. considerare solo le tile della propria partizione;
2. individuare la classe di task attiva a priorità più alta;
3. selezionare il target all'interno di tale classe;
4. applicare il routing/distanza coerente con E04;
5. muoversi verso il target oppure eseguire l'azione richiesta.

Non introdurre priorità diverse per farmer e hand.

Non introdurre Water-First.

Non introdurre cooperazione dinamica fra le due partizioni.

---

## 10. Protezione condivisa dei semi

Implementa il minimo coordinamento necessario per evitare la cancellazione atomica delle azioni `PLANT`.

La protezione deve essere:

- centralizzata all'interno della singola chiamata `act()`;
- deterministica;
- basata esclusivamente sullo stato osservato e sulle azioni pianificate nel turno corrente;
- priva di nuove euristiche economiche.

Il farmer può essere valutato per primo.

Se il farmer pianifica un `PLANT`, considera il relativo seme come **riservato virtualmente** per il turno corrente.

Quando viene valutata la farm hand, utilizza:

`semi osservati - semi già riservati`

come disponibilità effettiva per l'eventuale `PLANT` della hand.

Questa prenotazione:

- esiste soltanto durante la costruzione dell'action object corrente;
- non modifica lo stato dell'ambiente;
- non deve persistere tra turni;
- non deve modificare la scelta ROI della coltura.

Aggiungi test specifici per questo comportamento.

---

## 11. Instrumentation E05

Implementa o estendi l'instrumentation necessaria alla futura VERIFY senza modificare il comportamento strategico.

Mantieni le metriche E04 compatibili e prepara almeno:

### Core

- Completion Rate;
- Disqualification Rate;
- Win Rate;
- Final Money;
- Mean Final Money;
- sample standard deviation (`ddof=1`);
- Median Final Money;
- opponent breakdown.

### Diagnostica agricola

- Weed Conversions;
- Mean Unwatered End-of-Day Ratio.

### Diagnostica HIRE

Dove tecnicamente affidabile:

- numero di `HIRE` emessi;
- numero di hire riusciti;
- costo HIRE;
- turni con hand attiva;
- action count farmer;
- action count hand;
- breakdown almeno per:
  - `HARVEST`;
  - `PLANT`;
  - `WATER`;
  - movimento;
  - `PASS`.

### Performance

Mantieni:

- Agent Mean Turn Latency;

e aggiungi Maximum Turn Latency solo se l'infrastruttura corrente lo consente senza alterazioni invasive.

Non introdurre instrumentation che possa cambiare la strategia o compromettere la confrontabilità con E04.

---

## 12. Test della strategia E05

Crea:

`tests/test_hire_nw_cluster.py`

o utilizza un nome diverso soltanto se le convenzioni reali del repository lo richiedono.

Copri almeno:

1. parsing delle posizioni hand;
2. serializzazione `HIRE`;
3. un solo `HIRE` a inizio giornata;
4. nessun duplicate `HIRE`;
5. nessuna azione hand prima dello spawn;
6. azione hand dopo lo spawn;
7. partitioning farmer = 4 tile;
8. partitioning hand = 5 tile;
9. nessun targeting intenzionale cross-partition;
10. priorità `HARVEST > PLANT > WATER` per farmer;
11. stessa priorità per hand;
12. prenotazione deterministica dei semi;
13. prevenzione di `PLANT` aggregati incompatibili con i semi disponibili;
14. comportamento deterministico;
15. rehire il giorno successivo;
16. nessuna assunzione di persistenza notturna.

I test devono verificare il comportamento osservabile, evitando dipendenza eccessiva da dettagli implementativi.

---

## 13. Regression suite

Dopo il superamento dei test mirati, esegui l'intera suite esistente:

`.venv\Scripts\python.exe -m pytest tests/`

Tutti i test precedenti devono continuare a passare.

Se un test E01–E04 fallisce a causa delle modifiche E05:

**FERMATI e correggi la regressione prima di procedere.**

Non modificare i vecchi test soltanto per farli passare, salvo che sia dimostrabile che il test precedente contenga un'assunzione incompatibile con lo schema reale dell'ambiente.

In tal caso documenta esplicitamente la situazione.

---

## 14. Entrypoint e standalone submission

Solo dopo il superamento della test suite:

### Aggiorna

`src/agricola/agent.py`

per utilizzare:

`HIRENWClusterROIAgent`

come agente corrente E05.

### Aggiorna

`scripts/build_submission.py`

per includere tutte le dipendenze necessarie.

Genera quindi:

`submission/submission.py`

con il comando già consolidato nel repository.

Verifica che:

- il file venga generato;
- sia self-contained secondo i requisiti del progetto;
- sia importabile;
- possa produrre un'action object valido;
- includa il comportamento `HIRE`;
- non dipenda da import locali non disponibili su Kaggle.

Esegui gli eventuali test standalone già presenti.

---

## 15. Smoke evaluation

Dopo test e standalone build, esegui una **smoke evaluation limitata**.

Lo scopo non è valutare economicamente E05, ma verificare che:

- l'ambiente accetti `HIRE`;
- la hand venga effettivamente creata;
- la hand riceva azioni;
- il lifecycle giornaliero funzioni;
- non si verifichino crash;
- non si verifichino disqualification;
- il standalone agent completi almeno un episodio;
- la latenza resti ampiamente sotto il timeout.

Utilizza il numero minimo di episodi necessario per questa verifica tecnica, preferibilmente **1 episodio** con la configurazione consolidata del progetto.

Il risultato economico dello smoke test **non costituisce evidenza sperimentale E05**.

Non confrontarlo formalmente con E03/E04.

---

## 16. Controlli specifici durante lo smoke test

Durante lo smoke test verifica concretamente:

1. `HIRE` emesso a inizio giornata;
2. hand assente nel turno di emissione;
3. hand presente dal turno successivo;
4. massimo una hand attiva;
5. nuovo `HIRE` nelle giornate successive;
6. nessun duplicate hire;
7. farmer limitato alla partizione da 4 tile;
8. hand limitata alla partizione da 5 tile;
9. azioni hand accettate dall'ambiente;
10. assenza di errori di serializzazione;
11. nessuna disqualification;
12. completamento dell'episodio.

Se possibile, registra il numero totale di `HIRE` nello smoke episode per verificare la coerenza con il numero effettivo di giornate.

---

## 17. Correzioni consentite durante BUILD

Durante test e smoke evaluation puoi correggere:

- bug;
- errori di schema;
- errori di indexing;
- errori nel lifecycle `HIRE`;
- errori di routing;
- errori nel partitioning;
- errori nella prenotazione dei semi;
- problemi di bundling;
- problemi di instrumentation;
- regressioni introdotte dalla BUILD.

Non utilizzare lo smoke test per ottimizzare:

- ROI;
- crop selection;
- worker allocation;
- numero di hand;
- task priority;
- footprint;
- scheduling policy.

Se il risultato economico dello smoke test appare basso, **non modificare la strategia per migliorarlo**.

La performance economica deve essere misurata senza tuning nella VERIFY.

---

## 18. Condizioni di STOP

Interrompi la BUILD e segnala il problema se si verifica una delle seguenti condizioni:

- `HIRE` non funziona secondo la semantica verificata in DEFINE;
- la farm hand non è controllabile nel modo previsto;
- il lifecycle giornaliero non può essere implementato senza modificare il disegno sperimentale;
- il partitioning fisso 4:5 non è tecnicamente applicabile;
- è necessaria una modifica sostanziale della policy E03/E04;
- la protezione dei semi richiede una nuova euristica economica;
- la regression suite non può essere ripristinata;
- la standalone submission non può supportare correttamente E05;
- il benchmark non sarebbe più confrontabile con E04.

In questi casi non procedere autonomamente con un nuovo disegno.

---

## 19. Deliverable BUILD

Crea:

`docs/versions/E05_build_antigravity.md`

Il documento deve descrivere almeno:

1. **Obiettivo BUILD**
2. **File creati**
3. **File modificati**
4. **Supporto GameState**
5. **Supporto ActionBuilder**
6. **Implementazione HIRENWClusterROIAgent**
7. **Partitioning 4:5**
8. **Lifecycle HIRE**
9. **Scheduling dei worker**
10. **Protezione dei semi**
11. **Instrumentation**
12. **Test aggiunti**
13. **Risultato test mirati**
14. **Risultato regression suite**
15. **Standalone build**
16. **Smoke evaluation**
17. **Problemi rilevati e correzioni**
18. **Eventuali deviazioni dal PLAN**
19. **Rischi residui**
20. **Decisione di readiness per VERIFY**

Concludi con esattamente una delle seguenti decisioni:

- `READY FOR VERIFY`
- `BUILD REVISION REQUIRED`
- `EXPERIMENT BLOCKED`

motivandola.

---

## 20. Condizione finale di arresto

Al termine:

1. mostra i file creati e modificati;
2. riassumi l'implementazione;
3. mostra il risultato dei test E05;
4. mostra il risultato completo di `pytest`;
5. mostra il risultato della standalone build;
6. mostra il risultato dello smoke episode;
7. conferma il numero di `HIRE` osservati;
8. segnala eventuali deviazioni dal PLAN;
9. indica il percorso di:
   `docs/versions/E05_build_antigravity.md`;
10. mostra:
   `git diff --stat`;
11. mostra:
   `git status --short`.

Poi **FERMATI**.

### Non eseguire:

- benchmark completo da 30 episodi;
- confronto statistico E05 vs E04/E03;
- REVIEW;
- commit finale E05;
- push;
- tag Git;
- SHIP.

Attendi approvazione esplicita prima di passare da **BUILD** a **VERIFY**.