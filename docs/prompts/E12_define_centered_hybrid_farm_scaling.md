# E12 — DEFINE — Centered Hybrid Farm Scaling

## Contesto

Stiamo sviluppando l'agente per la competizione Kaggle **Kaggriculture** nel repository `kaggriculture-agent`.

E11 ha confermato che il problema non può essere affrontato semplicemente aumentando la superficie coltivata o allontanandosi progressivamente dall'origine. L'osservazione dei replay dei player più forti suggerisce invece un pattern ricorrente:

- espansione produttiva **compatta e centered**;
- acquisto relativamente precoce di **Q1**;
- sfruttamento intensivo di un'area nell'ordine di circa **5×5**, senza dispersione periferica;
- utilizzo di **colture differenti**;
- presenza di **cow vicino all'origine**;
- nei replay osservati, la componente cow sembra occupare/dedicarsi a un **blocco 2×2 adiacente all'origine**;
- soprattutto, la cow compare già nell'opening: non sembra essere un'aggiunta tardiva a una farm agricola già sviluppata.

L'evidenza più recente suggerisce quindi una strategia **cow-first / hybrid-first**, nella quale l'economia iniziale viene costruita attorno alla componente livestock.

Queste osservazioni sono evidenze empiriche da replay, non ancora assunzioni certe sul funzionamento del motore. Prima di implementare occorre verificare nel codice/environment quali vincoli siano effettivamente imposti dalle azioni, dai requisiti delle cow e dai Quarter.

---

## Obiettivo E12

Definire un nuovo esperimento denominato:

**E12 — Centered Hybrid Farm Scaling**

L'obiettivo non è effettuare micro-ottimizzazioni dell'E11, ma verificare un cambiamento strutturale della strategia:

> costruire fin dall'opening una farm ibrida, compatta e centrata sull'origine, con cow come componente produttiva iniziale e colture differenziate che scalano attorno al livestock core.

E12 deve essere progettato come esperimento falsificabile e confrontabile con E11.

---

## Ipotesi principale

**H12**

Una strategia `cow-first + centered hybrid scaling`, che:

1. accede precocemente a Q1 quando necessario;
2. introduce la cow alla prima opportunità tecnicamente ed economicamente sostenibile;
3. mantiene la componente livestock in un core compatto vicino all'origine;
4. sviluppa le colture attorno a tale core;
5. diversifica la produzione agricola;
6. espande progressivamente la superficie senza allontanarsi inutilmente dall'origine;
7. rimanda Q2 finché la struttura produttiva non è sufficientemente solida da finanziarlo;

produce una massa produttiva e un'economia significativamente superiori a E11.

---

## Geometria target da investigare

L'osservazione dei replay suggerisce la seguente struttura concettuale:

```text
              crop expansion
                   ↑
        ┌─────────────────────┐
        │      crop area      │
        │                     │
        │   ┌────────────┐    │
        │   │ livestock  │    │
        │   │ core ~2×2  │    │
        │   └────────────┘    │
        │      ORIGIN         │
        │                     │
        │      crop area      │
        └─────────────────────┘
                   ↓
              crop expansion
```

Non assumere automaticamente che il 2×2 sia obbligatorio.

Verificare:

- se la cow richiede effettivamente una geometria/spazio specifico;
- quali tile o strutture sono necessarie;
- se il 2×2 osservato deriva da un requisito del gioco o da una scelta strategica;
- quale posizione relativa all'origine minimizza il costo operativo;
- come evitare che livestock e crop planner competano per gli stessi tile.

Se tecnicamente valido, trattare il **2×2 adiacente all'origine come livestock core riservato**.

---

## Opening target

La sequenza strategica da verificare non è più:

`crop → scaling → cow`

ma:

`Q1 / prerequisiti → cow → hybrid core → crop scaling → eventuale Q2`

In termini operativi:

1. preservare il capitale necessario all'opening;
2. acquisire Q1 precocemente se è prerequisito o se il suo ROI strategico lo giustifica;
3. predisporre immediatamente il livestock core vicino all'origine;
4. introdurre la cow alla prima opportunità sostenibile;
5. avviare/continuare contemporaneamente la produzione agricola necessaria a sostenere cash flow e fabbisogni;
6. saturare prima lo spazio produttivo vicino all'origine;
7. espandere successivamente verso una geometria centered più ampia;
8. considerare Q2 solo dopo il raggiungimento di una condizione economica esplicita.

La cow NON deve essere implementata come semplice acquisto opportunistico tardivo.

---

## Scaling centered

L'espansione agricola deve privilegiare la **densità produttiva locale**, non la distanza massima raggiungibile.

Valutare una progressione geometrica equivalente a:

- fase iniziale: core compatto / raggio circa 2;
- fase intermedia: raggio circa 3;
- fase matura: raggio circa 4 o area comparabile a ~5×5 effettivamente produttiva.

I numeri sono ipotesi operative, non parametri da hardcodare senza verifica.

Il planner deve preferire tile:

1. utilizzabili;
2. compatibili con il livestock core;
3. vicini all'origine/core;
4. che aumentino la massa produttiva senza generare costi di movimento sproporzionati.

Evitare espansioni periferiche solo perché esiste capitale disponibile.

---

## Crop diversification

E12 deve superare esplicitamente una logica di monocultura.

Analizzare `CROPS`, prezzi, seed price, tempi/cicli, requisiti e meccaniche disponibili nell'environment per determinare:

- quali colture sono accessibili nelle diverse fasi;
- quali combinazioni possono sostenere meglio il cash flow;
- se esistono sinergie o fabbisogni collegati agli animali;
- come distribuire colture diverse nella superficie centered;
- se il mix deve cambiare nel corso dell'episodio.

Non introdurre complessità arbitraria: la diversificazione deve avere una motivazione economica o funzionale verificabile.

---

## Cow economics

Prima dell'implementazione ricostruire esattamente la catena economica della cow.

Documentare almeno:

- prerequisiti;
- costo iniziale;
- spazio necessario;
- eventuali strutture necessarie;
- alimentazione/fabbisogni;
- azioni richieste;
- output/prodotti generati;
- prezzi/ricavi;
- frequenza delle interazioni;
- eventuali costi ricorrenti;
- dipendenza da Q1/Q2 o altre tecnologie;
- rischi di immobilizzare troppo capitale nell'opening.

Determinare quindi una condizione esplicita per l'acquisto/attivazione della prima cow.

L'obiettivo strategico è **cow early**, non **cow at any cost**.

---

## Q1 e Q2

### Q1

Trattare Q1 come abilitatore potenzialmente precoce.

Verificare:

- costo;
- prerequisiti;
- cosa sblocca;
- relazione con cow e scaling;
- momento minimo e momento economicamente sensato per acquistarlo.

Se i vincoli del gioco lo consentono, E12 deve essere predisposto per acquistare Q1 molto prima delle strategie conservative precedenti.

### Q2

Q2 è un obiettivo dell'esperimento, ma **non deve essere forzato nell'opening**.

Definire una soglia/condizione economica per Q2 basata almeno su:

- liquidità disponibile;
- mantenimento di una reserve;
- stabilità del livestock core;
- superficie agricola attiva;
- capacità di continuare i cicli produttivi dopo l'acquisto.

Q2 deve essere conseguenza dello scaling riuscito, non causa di starvation finanziaria iniziale.

---

## Vincoli architetturali

Prima di modificare codice:

1. ispeziona l'implementazione E11 corrente;
2. identifica planner, policy ROI, gestione Quarter, tile selection, crop selection e qualsiasi supporto già presente per `PRODUCTS`/animali;
3. riusa quanto possibile;
4. evita una riscrittura non necessaria dell'agente;
5. mantieni separabili le nuove decisioni E12:
   - geometry;
   - livestock;
   - crop mix;
   - Q1;
   - Q2.

Questo è importante perché, se E12 fallisce, dobbiamo poter capire **quale componente dell'ipotesi è stata falsificata**.

---

## Instrumentation richiesta

E12 deve produrre evidenze sufficienti per capire la dinamica dell'episodio, non soltanto il final money.

Aggiungere o estendere il logging per poter ricostruire almeno:

- step di acquisto Q1;
- step di predisposizione/acquisto prima cow;
- posizione della cow/livestock core;
- numero di cow nel tempo;
- composizione delle colture nel tempo;
- numero di tile produttivi;
- distanza/raggio massimo dei tile produttivi dall'origine;
- money ai principali milestone;
- step di eventuale acquisto Q2;
- quantità/valore dei prodotti livestock;
- eventuali periodi di cash starvation;
- eventuali azioni fallite o impossibili;
- final money.

Se possibile, creare milestone sintetiche almeno a:

`step 24, 48, 72, 120, 240, 480, 720`

o a punti equivalenti coerenti con il motore.

---

## Benchmark e criterio di successo

Usare **E11 come baseline primaria**.

Recuperare dai risultati/versioni esistenti i valori E11 effettivamente validati e NON inventare numeri.

Il confronto deve includere almeno:

- Mean Final Money;
- differenza assoluta vs E11;
- differenza percentuale vs E11;
- deviazione standard (`ddof=1`);
- mediana;
- completion rate;
- disqualification rate;
- breakdown per opponent;
- eventuali outlier.

### Successo primario

E12 è promettente se produce un miglioramento **materiale e ripetibile** rispetto a E11, non una variazione marginale compatibile con rumore.

### Successo strutturale

Indipendentemente dal final money, verificare inoltre se E12 riesce effettivamente a ottenere:

- cow nell'opening;
- livestock vicino all'origine;
- superficie produttiva centered;
- maggiore utilizzo del terreno vicino al core;
- crop diversification;
- accesso sostenibile a Q2, se economicamente raggiungibile.

Un aumento del final money senza questi comportamenti NON valida automaticamente H12: potrebbe derivare da altri cambiamenti.

---

## Analisi di falsificazione

Il piano deve esplicitare in anticipo almeno questi possibili esiti:

### A — H12 confermata
Cow-first + centered hybrid scaling produce un salto economico significativo.

### B — Cow utile, scaling insufficiente
La componente livestock migliora l'economia ma la geometria/crop policy limita ancora la massa produttiva.

### C — Cow troppo costosa nell'opening
L'investimento iniziale rallenta troppo il cash flow. In questo caso occorrerà testare un ingresso cow leggermente ritardato, non abbandonare automaticamente il livestock.

### D — Geometria errata
Il 2×2 osservato non è appropriato o non deriva dai vincoli ipotizzati.

### E — Q1/Q2 timing errato
La struttura ibrida funziona ma gli upgrade assorbono capitale nel momento sbagliato.

### F — Crop mix errato
La diversificazione introdotta non aumenta il rendimento o non sostiene correttamente la componente animale.

---

## Cosa devi fare ora — solo DEFINE + PLAN

In questa fase **NON implementare ancora E12**.

Procedi con:

1. ispezione del repository e dello stato E11;
2. recupero delle metriche baseline E11;
3. analisi delle API/meccaniche relative a cow, prodotti, crop, Quarter e tile;
4. verifica tecnica dell'ipotesi del livestock core 2×2;
5. ricostruzione della catena economica necessaria per ottenere e mantenere una cow;
6. analisi del timing possibile di Q1 e Q2;
7. proposta della geometria centered;
8. proposta della crop diversification policy;
9. definizione delle condizioni di ingresso cow e Q2;
10. definizione dell'instrumentation;
11. definizione del protocollo di benchmark;
12. stesura del piano di implementazione E12.

---

## Output richiesto

Al termine restituisci un report strutturato con:

### 1. Stato E11
- agent corrente;
- comportamento;
- metriche validate;
- limiti rilevanti per E12.

### 2. Meccaniche verificate
- cow;
- livestock geometry;
- crop;
- products;
- Q1;
- Q2;
- costi e prerequisiti.

Distingui chiaramente:
- **fatto verificato nel codice/environment**;
- **evidenza osservata nei replay**;
- **ipotesi strategica**.

### 3. Strategia E12 proposta
Descrivi opening, livestock core, crop mix, scaling centered e upgrade timing.

### 4. State machine / decision policy
Proponi una policy sufficientemente precisa da poter essere implementata senza ambiguità.

### 5. Modifiche al codice
Elenca file/classi/funzioni da creare o modificare e responsabilità di ciascun cambiamento.

### 6. Instrumentation
Definisci metriche e milestone.

### 7. Benchmark
Definisci protocollo locale e confronto E11/E12.

### 8. Rischi e falsificazione
Indica cosa potrebbe smentire H12 e come distingueremo le cause.

### 9. Implementation plan
Fornisci una sequenza concreta di BUILD → VERIFY, ma **fermati prima di modificare il codice**.

---

## Regola finale

Non ottimizzare E12 per assomigliare visivamente ai replay.

I replay sono una fonte di **ipotesi strategiche**.

Prima verifica le meccaniche nell'environment, poi implementa la versione più semplice e misurabile della strategia che permetta di testare:

> **cow-first + livestock centered + diversified crop scaling + delayed sustainable Q2**

Fermati al termine del PLAN e attendi approvazione prima del BUILD.
