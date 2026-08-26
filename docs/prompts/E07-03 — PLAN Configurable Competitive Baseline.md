# E07-03 — PLAN Configurable Competitive Baseline

Stiamo lavorando al progetto **Kaggriculture Agent**.

Le fasi precedenti sono:

- `E07-01 — DEFINE Competitive Baseline Reconstruction`
- `E07-02 — VERIFY Competitive Evidence`

Documenti di riferimento:

- `docs/versions/E07_define_competitive_baseline.md`
- `docs/versions/E07_verify_competitive_evidence.md`

La decisione approvata è:

> **GO FOR PLAN WITH OPEN PARAMETERS**

E07 deve costruire una **baseline competitiva di seconda generazione configurabile**, non implementare rigidamente tutti i valori quantitativi ipotizzati nel DEFINE/VERIFY.

---

# 1. Obiettivo E07

Progettare una nuova architettura dell'agente capace di operare nella stessa **classe strategica** degli agenti competitivi osservati:

- espansione territoriale;
- workforce scaling;
- crop allocation multipla;
- livestock;
- feed loop;
- reinvestimento del capitale;
- gestione del mercato;
- comportamento phase-based;
- end-game policy.

E07 costituisce intenzionalmente un **salto di baseline**.

Non è richiesto che ogni singola capability dimostri separatamente un miglioramento rispetto a E06.

E08+ potranno successivamente effettuare ablation e ottimizzazioni controllate.

---

# 2. Principio architetturale

Separare:

## Strategic architecture

Capacità che E07 deve necessariamente introdurre.

## Tunable parameters

Valori quantitativi che devono essere configurabili e non considerati ancora ottimali.

Evitare di incorporare nel codice come costanti strategiche valori derivati esclusivamente da `INFERENCE`.

---

# 3. Architettura strategica obbligatoria

Il PLAN deve prevedere almeno i seguenti moduli logici.

## Phase Manager

Gestisce le fasi:

```text
OPENING
    ↓
SCALE
    ↓
PRODUCE
    ↓
LIQUIDATE
```

La transizione non deve necessariamente dipendere esclusivamente dal giorno.

Prevedere condizioni basate anche su:

- cash;
- land ownership;
- workforce;
- livestock;
- crop maturity;
- remaining time.

---

## Capital Allocator

Decide come utilizzare la liquidità disponibile.

Deve poter assegnare capitale almeno a:

- seeds;
- feed/security buffer;
- workforce;
- livestock;
- land;
- eventuali structures.

Deve rispettare una `cash_reserve` configurabile.

Evitare una semplice sequenza incontrollata di acquisti.

---

## Land Manager

Responsabile di:

- territorio posseduto;
- territorio produttivo;
- `BUY_LAND`;
- attivazione progressiva delle tile;
- allocazione funzionale.

Distinguere esplicitamente:

```text
owned_tiles
productive_tiles
crop_tiles
livestock_tiles
infrastructure_tiles
reserved_tiles
```

Non assumere:

`owned_tiles == productive_tiles`.

---

## Workforce Manager

Responsabile di:

- farmer;
- farm hands;
- `HIRE`;
- hiring schedule;
- distribuzione dei worker.

Il numero target di worker deve essere configurabile.

Il PLAN deve consentire almeno:

```text
target_workers
hire_days / hire_conditions
minimum_cash_after_hire
```

Non hard-codificare come verità competitiva:

`1 Farmer + 3 Hands`.

Questa resta la configurazione candidata iniziale.

---

## Crop Manager

Deve supportare contemporaneamente almeno:

- Wheat;
- Melon;
- Carrot.

Le tile devono poter avere ruoli differenti:

```text
FEED
CASH
FLEX
```

La configurazione candidata iniziale può essere:

```text
Wheat = 6
Melon = 12
Carrot = 6
```

ma questi valori devono essere parametri.

---

## Livestock Manager

Deve gestire:

- cows;
- sheep;
- feeding;
- produzione;
- eventuale liquidazione.

Configurazione candidata iniziale:

```text
Cows = 4
Sheep = 2
```

ma il numero deve essere configurabile.

Il modulo deve poter funzionare anche con:

```text
Cows = 0
Sheep = 0
```

per future ablation.

---

## Feed Manager

Deve verificare continuamente:

```text
feed inventory
expected consumption
expected production
feed safety buffer
```

La priorità non deve dipendere soltanto dal numero nominale di wheat tile.

Prevedere una condizione del tipo:

```text
expected_feed_supply >= expected_feed_demand + safety_buffer
```

Se il feed diventa insufficiente, l'agente deve poter aumentare temporaneamente la priorità Wheat.

---

## Task Dispatcher

Deve assegnare le attività ai worker evitando conflitti.

Partire dalla priorità candidata:

```text
WATER
FEED_ANIMALS
HARVEST
PLANT
```

ma verificare nel PLAN se l'environment richiede una diversa precedenza operativa.

La distanza Manhattan può continuare a essere utilizzata per scegliere il task all'interno della stessa classe di priorità, se compatibile con l'architettura esistente.

Il dispatcher deve evitare:

- due worker sullo stesso task;
- worker inutilmente idle;
- movement eccessivo;
- starvation degli animali;
- perdita di raccolti maturi.

---

## Market Broker

Deve centralizzare le operazioni di vendita.

Prevedere:

- queue;
- inventory awareness;
- market limits;
- priorità configurabile;
- eventuale buffering;
- end-game liquidation.

Configurazione candidata:

```text
Milk / Wool
Melon
Carrot
surplus Wheat
```

Non assumere prezzi statici.

---

## End-Game Manager

Deve utilizzare:

```text
remaining_steps
remaining_days
crop_growth_time
inventory
livestock
```

per evitare investimenti che non possono rientrare prima della fine dell'episodio.

Deve poter:

- interrompere determinate piantumazioni;
- evitare acquisti tardivi;
- vendere inventory;
- liquidare asset quando economicamente sensato.

Il Giorno 25 e Giorno 29–30 devono essere parametri iniziali, non verità hard-coded.

---

# 4. Configurazione centralizzata

Progettare una configurazione E07 esplicita.

Esempio concettuale:

```python
CompetitiveConfig(
    target_quadrants=2,
    target_workers=4,

    wheat_tiles=6,
    melon_tiles=12,
    carrot_tiles=6,

    target_cows=4,
    target_sheep=2,

    expansion_day=12,
    cash_reserve=300,

    stop_melon_day=25,
    liquidation_day=29,
)
```

Questa struttura è soltanto indicativa.

Adattarla allo stile e all'architettura esistenti.

L'obiettivo è permettere future variazioni sperimentali **senza riscrivere la policy**.

---

# 5. Parametri esplicitamente OPEN

Il PLAN deve marcare come `OPEN / TUNABLE` almeno:

| Parameter | Initial candidate | Status |
|---|---:|---|
| Target quadrants | 2 | OPEN |
| Productive tiles | 24 | OPEN |
| Wheat tiles | 6 | OPEN |
| Melon tiles | 12 | OPEN |
| Carrot tiles | 6 | OPEN |
| Target workers | 4 | OPEN |
| Hiring schedule | D1/D6/D12 | OPEN |
| Cows | 4 | OPEN |
| Sheep | 2 | OPEN |
| Expansion timing | D12 | OPEN |
| Cash reserve | $300 | OPEN |
| Stop melon | D25 | OPEN |
| Liquidation | D29–30 | OPEN |
| Market priority | Premium-first | OPEN |
| Structures | none initially | OPEN |

Questi valori costituiscono la **starting configuration**, non valori ottimali dimostrati.

---

# 6. Nessuna struttura obbligatoria in E07

Non includere `WELL`, `BARN` o altre structures come requisito della prima implementazione salvo che l'environment le renda tecnicamente necessarie per livestock o altre capability.

Le structures non supportate da ROI verificato devono rimanere fuori dal core E07.

Potranno essere oggetto di esperimenti successivi.

---

# 7. Compatibilità con E06

E07 non deve distruggere o sostituire E06.

Preservare:

- classe/agente E06;
- benchmark E06;
- test E06;
- risultati E06;
- submission E06;
- documentazione E06.

La nuova baseline deve essere implementata separatamente.

E06 rimane la baseline shipped precedente e il riferimento per misurare il salto architetturale.

---

# 8. Instrumentation obbligatoria

Questa è una parte essenziale di E07.

Il nuovo agente deve consentire di osservare cosa accade realmente durante gli episodi.

Prevedere metriche aggregate almeno per:

## Economy

- starting money;
- final money;
- minimum cash;
- land spending;
- workforce spending;
- livestock spending;
- seed spending;
- structure spending;
- revenue per product/categoria, se ricostruibile.

## Land

- owned tiles;
- productive tiles;
- utilization ratio;
- expansion step/day.

## Workforce

- worker count nel tempo;
- hires;
- worker idle time;
- movement steps;
- productive actions.

## Crops

- planted;
- watered;
- harvested;
- lost/unharvested crops;
- produzione per crop.

## Livestock

- animals acquired;
- feed consumed;
- missed feeds/starvation events;
- milk produced;
- wool produced.

## Market

- sell orders;
- quantities sold;
- realized revenue;
- inventory remaining.

## End-game

- crops ancora immature;
- inventory residuo;
- livestock residuo;
- liquidazioni eseguite.

Se alcune metriche richiedono modifiche invasive, indicarlo nel PLAN e proporre il livello minimo di instrumentation necessario.

---

# 9. Test strategy

Il PLAN deve progettare test prima del BUILD.

Prevedere almeno:

### Unit tests

- phase transitions;
- config parsing/defaults;
- capital reserve;
- land allocation;
- workforce targets;
- crop allocation;
- feed balance logic;
- livestock target;
- market queue;
- end-game cutoff.

### Behavioral tests

Scenari sintetici:

- cash insufficiente;
- feed insufficiente;
- crop maturo;
- animale da alimentare;
- possibilità di espansione;
- fine episodio vicina;
- inventory elevato;
- worker idle.

### Regression tests

Tutti i test E01–E06 devono continuare a passare.

---

# 10. Benchmark locale E07

Il PLAN deve prevedere esplicitamente che il BUILD/VERIFY successivo esegua il benchmark standard del progetto.

Usare la stessa metodologia comparabile già adottata per E01–E06, salvo modifiche motivate.

Registrare almeno:

- Completion Rate;
- Disqualification Rate;
- Win/Draw/Loss;
- Mean Final Money;
- Standard Deviation (`ddof=1`);
- Median Final Money;
- breakdown per opponent.

Ma per E07 aggiungere le metriche diagnostiche definite sopra.

---

# 11. Nessuna accettazione basata sul modello teorico

Non utilizzare:

`$35k–$45k`

come criterio di successo.

Questo intervallo deriva da un modello economico preliminare e **non è un risultato sperimentale E07**.

Non utilizzare neppure il presunto:

`+42% / +82%`

come miglioramento osservato.

I risultati reali devono provenire dall'esecuzione dell'agente.

---

# 12. Criteri di successo E07

E07 ha due livelli distinti di successo.

## A. Architectural success — obbligatorio

La nuova baseline deve:

- funzionare per 720 step;
- non essere disqualificata;
- utilizzare realmente le nuove capability;
- espandersi quando previsto;
- scalare workforce;
- utilizzare più crop;
- utilizzare livestock;
- gestire feed;
- utilizzare il mercato;
- cambiare comportamento nelle fasi;
- eseguire una policy end-game;
- produrre instrumentation verificabile.

## B. Performance success — da misurare

Confrontare E07 con E06 e con il miglior riferimento locale precedente.

Non fissare nel PLAN un valore finale inventato.

Registrare:

```text
Δ Mean Final Money
Δ %
Δ Median
Δ Win Rate
```

La valutazione dovrà stabilire se il salto architetturale ha effettivamente prodotto una baseline più competitiva.

---

# 13. Failure criteria

E07 deve essere considerato problematico se, durante VERIFY:

- non completa gli episodi;
- genera disqualification;
- non riesce a finanziare la strategia;
- compra land senza utilizzarla;
- workforce rimane largamente idle;
- livestock soffre starvation;
- feed loop non è sostenibile;
- movement domina il tempo operativo;
- market queue accumula inventory;
- end-game lascia capitale facilmente liquidabile;
- le nuove capability peggiorano drasticamente il risultato.

Questi casi devono produrre diagnosi, non essere nascosti dietro il risultato medio.

---

# 14. Deliverable PLAN

Creare:

`docs/versions/E07_plan_competitive_baseline.md`

Il documento deve contenere almeno:

1. Objective
2. Inputs from DEFINE/VERIFY
3. Architectural Principles
4. Proposed Agent Architecture
5. Configuration Model
6. Phase Manager
7. Capital Allocator
8. Land Manager
9. Workforce Manager
10. Crop Manager
11. Livestock / Feed Manager
12. Task Dispatcher
13. Market Broker
14. End-Game Manager
15. Instrumentation
16. Test Strategy
17. Local Benchmark Strategy
18. Success Criteria
19. Failure Criteria
20. Open Parameters
21. Implementation Sequence
22. Risks
23. PLAN Decision

---

# 15. Implementation sequence

Il PLAN deve proporre una sequenza BUILD incrementale.

Preferire una struttura simile:

```text
B1 Configuration + Phase Manager
        ↓
B2 Land + Workforce
        ↓
B3 Multi-Crop Allocation
        ↓
B4 Livestock + Feed
        ↓
B5 Task Dispatcher
        ↓
B6 Market Broker
        ↓
B7 End-Game
        ↓
B8 Instrumentation
        ↓
B9 Integration
        ↓
B10 Local Benchmark
```

Adattare la sequenza se l'architettura esistente suggerisce dipendenze differenti.

Ogni passaggio deve essere testabile.

---

# 16. PLAN decision

Al termine utilizzare:

### GO FOR BUILD

se l'architettura è implementabile senza questioni bloccanti.

### GO FOR BUILD WITH OPEN PARAMETERS

se l'architettura è definita ma rimangono parametri quantitativi sperimentali.

### RETURN TO VERIFY

se emergono problemi nelle meccaniche dell'environment.

### RETURN TO DEFINE

se emerge che l'architettura competitiva stessa non è sufficientemente definita.

La decisione attesa, se non emergono nuovi blocker, è:

> **GO FOR BUILD WITH OPEN PARAMETERS**

ma deve derivare dall'analisi, non essere forzata.

---

# 17. Aggiornamento documentazione

Aggiornare:

- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`;

per registrare il PLAN.

Non dichiarare E07:

- implemented;
- validated;
- shipped.

Non modificare ancora il codice dell'agente.

---

# 18. STOP CONDITION

Al termine mostrare:

1. architettura proposta;
2. moduli e responsabilità;
3. modello di configurazione;
4. parametri OPEN;
5. instrumentation prevista;
6. test strategy;
7. implementation sequence;
8. rischi principali;
9. decisione PLAN.

**FERMARSI.**

Non:

- implementare codice;
- creare E07 agent;
- eseguire benchmark E07;
- costruire submission;
- inviare submission Kaggle;
- creare tag;
- dichiarare E07 shipped.

Attendere l'approvazione prima del BUILD.