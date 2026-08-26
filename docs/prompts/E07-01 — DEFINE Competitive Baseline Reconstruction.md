# E07-01 — DEFINE Competitive Baseline Reconstruction

Stiamo lavorando al progetto **Kaggriculture Agent**.

Questa fase è esclusivamente **DEFINE / reconnaissance**.

**Non modificare il codice dell'agente, non implementare nuove strategie e non costruire una nuova submission.**  
Prima dobbiamo capire come sono strutturate le strategie competitive pubblicamente osservabili e definire una nuova baseline architetturale.

## 1. Contesto sperimentale

La linea E01–E06 ha seguito finora un approccio incrementale e controllato, modificando singole capacità dell'agente e misurandone l'effetto.

La situazione corrente è:

- **E06 resta la baseline locale shipped**;
- la validazione Kaggle di E06 è ancora in assestamento e al momento risulta inferiore a E05;
- il confronto E05/E06 continua tramite il monitoraggio già predisposto;
- **non usare l'attuale differenza E05/E06 per scegliere prematuramente la strategia E07**;
- E07 non deve essere assunto a priori come DIG, espansione del terreno o altra singola capability;
- l'attuale agente utilizza soltanto una porzione limitata dello spazio strategico disponibile.

Il problema da verificare è se E01–E06 abbiano progressivamente ottimizzato una configurazione locale troppo semplice rispetto agli agenti competitivi.

E07 deve quindi individuare una **Competitive Reference Configuration** completa, che possa diventare la baseline della seconda generazione dell'agente.

Successivamente, da E08 in avanti, torneremo agli esperimenti controllati sulle singole variabili.

---

# 2. Domanda DEFINE

Rispondere alla seguente domanda:

> **Qual è una configurazione strategica completa, pubblicamente ricostruibile e rappresentativa degli agenti competitivi Kaggriculture, che possa diventare la nuova baseline architetturale del progetto?**

Non cercare semplicemente "la strategia migliore".

Dobbiamo individuare i **pattern ricorrenti** delle strategie competitive e distinguere:

1. caratteristiche strutturali comuni;
2. varianti strategiche;
3. scelte specifiche di singoli agenti;
4. eventuali trick o ottimizzazioni difficilmente generalizzabili.

---

# 3. Prima attività: ricostruire lo stato del progetto

Prima della ricerca esterna:

1. leggere:
   - `README.md`;
   - `PROJECT_STATE.md`;
   - `NEW_SESSION.md`;
   - `EXPERIMENT_LOG.md`;
   - documentazione E01–E06 rilevante;
   - implementazione corrente dell'agente;
   - benchmark e risultati disponibili;

2. ricostruire sinteticamente l'evoluzione E01–E06;

3. identificare con precisione la configurazione della baseline E06:
   - terreno utilizzato;
   - workforce;
   - crop policy;
   - planting;
   - watering;
   - harvesting;
   - movement;
   - market behavior;
   - livestock;
   - structures;
   - scheduling;
   - eventuali capacità dell'environment non utilizzate.

Non modificare questi file durante questa prima ricognizione.

---

# 4. Ricerca delle strategie competitive pubbliche

Effettuare una ricerca sistematica delle informazioni pubblicamente disponibili su Kaggriculture.

Cercare almeno nelle seguenti categorie di fonti:

- repository GitHub pubblici;
- Kaggle Competition;
- Kaggle Code;
- Kaggle Discussions;
- documentazione ufficiale Kaggriculture/Kaggle Environments;
- agent source code pubblicamente accessibile;
- replay ed episodi pubblicamente accessibili;
- README e documentazione tecnica degli agenti.

Non limitarsi ai README quando è disponibile il codice.

Per ogni informazione importante indicare la fonte esatta e, quando possibile, URL, repository/file e posizione nel codice.

Non assumere che una strategia dichiarata nel README corrisponda necessariamente al comportamento effettivo dell'agente.

---

# 5. Separazione dei livelli di evidenza

Per ogni conclusione distinguere esplicitamente:

### CODE

Comportamento direttamente verificabile nel codice.

### EPISODE

Comportamento osservato in replay o episodi.

### AUTHOR

Comportamento o risultato dichiarato dall'autore nella documentazione.

### INFERENCE

Interpretazione nostra derivata dalle evidenze precedenti.

Non presentare mai una `INFERENCE` come fatto osservato.

Quando più fonti confermano lo stesso pattern, indicarlo.

---

# 6. Dimensioni strategiche da analizzare

Per ogni agente competitivo sufficientemente documentato analizzare almeno:

## Land use

- numero di tile utilizzate;
- numero di quadranti utilizzati;
- ordine di espansione;
- timing dell'acquisto;
- condizioni economiche per `BUY_LAND`;
- eventuale terreno lasciato inutilizzato.

## Workforce

- numero di farmer/farm hands;
- hiring schedule;
- condizioni economiche per le assunzioni;
- distribuzione del lavoro;
- eventuale specializzazione dei worker;
- rapporto tra workforce e terreno.

## Crops

- colture utilizzate;
- crop mix;
- superficie dedicata;
- rotazioni;
- funzione economica delle diverse colture;
- eventuale adattamento a prezzi, inventory o opponent.

## Livestock

- presenza o assenza;
- cows;
- sheep;
- numerosità;
- timing dell'introduzione;
- funzione economica;
- rapporto con crops e land allocation.

## Structures

- strutture costruite;
- timing;
- costo;
- funzione;
- condizioni che ne determinano la costruzione.

## Capital allocation

- liquidità mantenuta;
- reinvestimento;
- priorità fra land, workforce, crops, livestock e structures;
- eventuali soglie di capitale;
- comportamento in condizioni di scarsità di cassa.

## Market

- acquisti;
- vendite;
- gestione inventory;
- utilizzo dei prezzi;
- domanda;
- eventuale market timing;
- liquidazione.

## Scheduling

Ricostruire, quando possibile, il comportamento per:

- early game;
- mid game;
- late game;
- end-game.

Verificare se la strategia cambia esplicitamente nelle diverse fasi.

## Opponent awareness

Verificare se e come l'agente:

- osserva l'avversario;
- modifica crop choice;
- modifica mercato;
- modifica espansione;
- modifica altre decisioni.

---

# 7. Performance

Raccogliere soltanto metriche pubblicamente verificabili.

Possibili esempi:

- Kaggle rating;
- leaderboard position;
- win/loss;
- risultati dichiarati;
- risultati di replay;
- benchmark pubblicati.

Per ogni numero indicare chiaramente:

- fonte;
- natura della metrica;
- periodo/versione, quando disponibile;
- grado di verificabilità.

Non confrontare direttamente metriche incompatibili.

Non trasformare rating o risultati storici in stime dell'attuale leaderboard.

---

# 8. Matrice comparativa

Costruire una matrice comparativa degli agenti analizzati.

Usare almeno queste colonne:

| Agent | Performance evidence | Land | Workforce | Crops | Livestock | Structures | Market | Capital policy | Scheduling | Opponent awareness | Evidence quality |
|---|---|---|---|---|---|---|---|---|---|---|---|

Aggiungere colonne se emergono variabili strategiche importanti non previste.

---

# 9. Confronto con E06

Costruire successivamente una seconda matrice:

| Capability | E06 | Competitive pattern | Gap | Evidence | Confidence |
|---|---|---|---|---|---|

Usare almeno:

- land utilization;
- expansion;
- workforce scaling;
- crop diversification;
- livestock;
- structures;
- capital allocation;
- market policy;
- scheduling;
- opponent awareness;
- end-game policy.

La finalità non è ancora stabilire quale singola capability implementare.

Dobbiamo capire **quanto E06 sia distante dalla classe strategica degli agenti competitivi**.

---

# 10. Cercare convergenze, non copiare un singolo agente

Questa è una regola fondamentale del DEFINE.

Non scegliere automaticamente:

- il primo classificato;
- il repository con il rating più alto;
- l'agente con più terreno;
- l'agente con più worker;
- la configurazione più complessa.

Cercare invece i pattern che ricorrono in più strategie competitive indipendenti.

Esempio concettuale:

se diversi agenti forti convergono verso:

- 2–3 quadranti;
- workforce significativamente superiore a E06;
- crop diversification;
- livestock;
- reinvestimento progressivo;
- scheduling early/mid/late;

questo costituisce evidenza molto più interessante della configurazione specifica di un singolo agente.

Cercare anche **controesempi**.

Se un agente documenta che una maggiore espansione o workforce ha peggiorato drasticamente le prestazioni, registrare l'evidenza.

---

# 11. Ricostruire l'economia dello scaling

Non trattare le capability come elementi indipendenti.

Verificare in particolare le dipendenze:

```text
production
    ↓
cash generation
    ↓
reinvestment
    ↓
workforce / land / livestock / structures
    ↓
higher productive capacity
    ↓
market / cash generation
```

Determinare se gli agenti competitivi seguono effettivamente un ciclo di questo tipo oppure altri modelli.

Una configurazione con molto terreno ma workforce insufficiente non deve essere considerata automaticamente competitiva.

Analogamente, una workforce numerosa che non genera abbastanza valore per coprire i costi non costituisce automaticamente una strategia migliore.

---

# 12. Competitive Reference Configuration

Alla fine della reconnaissance proporre una:

## E07 Competitive Reference Configuration

La proposta deve specificare, quando l'evidenza lo consente:

- quadranti;
- numero/ordine delle tile;
- workforce target;
- hiring schedule;
- crop mix;
- land allocation;
- livestock;
- structures;
- expansion schedule;
- cash reserve;
- capital allocation;
- market policy;
- opponent awareness;
- early-game policy;
- mid-game policy;
- late-game policy;
- end-game policy.

Per ogni elemento usare una tabella:

| Parameter | Proposed value/policy | Evidence | Sources | Confidence | Notes |
|---|---|---|---|---|---|

Usare per `Confidence`:

- **HIGH**
- **MEDIUM**
- **LOW**

Se l'evidenza non consente di determinare un valore preciso, non inventarlo.

Indicare invece:

- range osservato;
- alternative plausibili;
- informazione mancante.

---

# 13. Criterio per la proposta E07

La Competitive Reference Configuration non deve necessariamente essere:

- ottimale;
- minimalista;
- causalmente interpretabile;
- derivata da una sola strategia.

Deve essere:

1. **competitivamente plausibile**;
2. basata su evidenza pubblica;
3. economicamente coerente;
4. implementabile nel nostro environment;
5. sufficientemente robusta da diventare una nuova baseline;
6. strutturata in modo da poter essere successivamente sottoposta ad ablation e ottimizzazione controllata.

E07 rappresenterà intenzionalmente un'eccezione alla regola "una variabile per esperimento".

Lo scopo è effettuare un **salto di baseline**, non attribuire causalità alle singole modifiche.

---

# 14. Implicazioni per E08+

Identificare le variabili della configurazione proposta che potranno successivamente essere ottimizzate mediante esperimenti controllati.

Produrre una prima lista di candidati, senza ancora pianificare gli esperimenti.

Esempi:

- land utilization;
- expansion timing;
- workforce size;
- hiring schedule;
- crop allocation;
- livestock allocation;
- structures;
- cash reserve;
- market policy;
- scheduling;
- end-game policy.

Non assegnare automaticamente questi numeri agli esperimenti E08, E09, ecc.

---

# 15. Deliverable

Creare:

`docs/versions/E07_define_competitive_baseline.md`

Il documento deve contenere almeno:

1. **Executive Summary**
2. **Current Baseline — E06**
3. **Research Method**
4. **Public Competitive Sources**
5. **Competitive Agents Analysed**
6. **Evidence Classification**
7. **Comparative Strategy Matrix**
8. **Land and Expansion Analysis**
9. **Workforce Analysis**
10. **Crop Strategy Analysis**
11. **Livestock and Structures**
12. **Capital and Market Strategy**
13. **Scheduling and End-game**
14. **Opponent Awareness**
15. **Competitive Patterns**
16. **Counterexamples and Failed Scaling**
17. **E06 Competitive Gap**
18. **Proposed E07 Competitive Reference Configuration**
19. **Confidence and Evidence Gaps**
20. **Candidate Variables for E08+**
21. **DEFINE Decision**

Aggiornare `PROJECT_STATE.md` e `NEW_SESSION.md` **solo per registrare che il DEFINE E07 è stato eseguito e quali evidenze sono state raccolte**.

Non dichiarare E07 implementato, validato o shipped.

---

# 16. Stop condition

Al termine:

1. mostrare sinteticamente le fonti trovate;
2. mostrare i principali pattern competitivi;
3. mostrare la matrice E06 vs competitive pattern;
4. mostrare la proposta di **E07 Competitive Reference Configuration**;
5. evidenziare i parametri con confidence LOW;
6. indicare eventuali informazioni che richiedono ulteriore ricerca.

**FERMARSI QUI.**

Non:

- modificare l'agente;
- creare implementation plan;
- implementare E07;
- eseguire benchmark E07;
- costruire submission;
- inviare submission Kaggle;
- creare tag;
- dichiarare E07 shipped.

Attendere la revisione e l'approvazione del DEFINE prima di passare al PLAN.