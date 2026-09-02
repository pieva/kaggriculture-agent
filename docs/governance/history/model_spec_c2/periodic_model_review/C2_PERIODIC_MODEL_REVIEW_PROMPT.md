# C2 â€” Rivalutazione del MODEL_SPEC: da soglie a periodi

## Contesto

Il C2 resta aperto sul piano strategico: il tournament locale ha prodotto un miglioramento reale, ma i replay Kaggle mostrano che esistono policy significativamente piÃ¹ efficienti e con architetture produttive molto diverse.

Sono disponibili quattro replay esterni selezionati appositamente per evitare ulteriore spreco di crediti:

### Q0
- `103484828.json` â€” Antigravity vs **LuCcc** â€” score avversario **56.772**
  - usa un solo quadrante;
  - elemento da analizzare con particolare attenzione: **periodicitÃ  dei cicli produttivi**.

### Q2
- `103473619.json` â€” Antigravity vs **Gordeev** â€” score avversario **88.648**
- `103462357.json` â€” Antigravity vs **Dipin** â€” score avversario **95.496**

### Q3
- `103464592.json` â€” Antigravity vs **ÐŸÐµÑ‚Ð°Ñ€** â€” score avversario **95.475**

Questi replay devono essere trattati come evidenza comparativa, non come configurazioni da copiare meccanicamente.

---

# Obiettivo della review

Rivalutare **indipendentemente il proprio MODEL_SPEC C2** verificando esplicitamente se l'architettura corrente Ã¨ eccessivamente **threshold-centric / reactive** e se una parte significativa della policy dovrebbe evolvere verso un modello **period-centric / plan-driven**.

La review deve partire dall'ipotesi seguente, ma deve poterla anche falsificare:

> **La produzione di base potrebbe essere governata piÃ¹ efficacemente da periodi biologici e calendari di servizio predefiniti, mentre la componente reattiva dovrebbe essere riservata principalmente alle condizioni di mercato e alle deviazioni dal piano.**

Formalizzazione iniziale da valutare:

```text
BASE POLICY = PLAN
MARKET CONDITION = REACT
```

PiÃ¹ precisamente:

```text
PLAN
= biological cycles
+ service schedule
+ workforce allocation
+ production calendar
+ harvest / collect deadlines
+ optional expansion schedule

REACT
= market prices
+ market inventory / demand
+ cash constraints
+ sell timing
+ exceptional deviations from plan
```

Non assumere che questa formulazione sia corretta: verificarla sui replay.

---

# Domande obbligatorie

## 1. Threshold-centric vs period-centric

Per il proprio modello corrente, identificare:

- quali decisioni sono oggi attivate da soglie;
- quali soglie governano produzione, raccolta, feeding, care, replant, selling, workforce, land expansion;
- quali di queste decisioni sembrano invece dipendere da un **periodo biologico o operativo stabile**;
- quali soglie restano realmente necessarie.

Produrre una classificazione esplicita:

```text
KEEP_AS_THRESHOLD
CONVERT_TO_PERIOD
HYBRID_PERIOD_PLUS_THRESHOLD
REMOVE
```

---

## 2. PeriodicitÃ  dei replay

Analizzare i quattro replay e ricostruire, quando osservabile:

### Colture
Per ciascuna specie utilizzata:
- `PLANT`
- frequenza `WATER`
- finestra di maturazione
- timing `HARVEST`
- eventuale `REPLANT`
- intervallo tra cicli
- yield ottenuto
- eventuale sincronizzazione o staggering

Struttura attesa:

```text
crop
plant_step
watering_period
harvest_period_or_window
replant_delay
cycle_length
observed_yield
service_deadline
```

### Animali
Per ciascuna specie:
- acquisto / placement;
- `FEED`;
- `CARE`;
- produzione;
- raccolta del prodotto;
- eventuale fertilizzante;
- intervalli tra eventi.

Struttura attesa:

```text
animal
placement_step
feed_period
care_period
production_period
collection_period
observed_output
service_deadline
```

Non limitarsi a contare le azioni: cercare **regolaritÃ  temporali**.

---

## 3. Caso LuCcc: efficienza senza espansione

Il replay `103484828.json` Ã¨ prioritario perchÃ© LuCcc ottiene **56.772 con un solo quadrante**.

Verificare in particolare:

- quanta parte della performance puÃ² essere spiegata da periodicitÃ ;
- grado di regolaritÃ  di `FEED` e `CARE`;
- periodicitÃ  delle colture;
- eventuale uso di staggered planting;
- numero massimo di tile produttive;
- numero e tipo di animali;
- workforce;
- densitÃ  di servizio per tile;
- tempo perso in routing;
- cash trajectory;
- quantitÃ  vendute e periodicitÃ  delle vendite.

La domanda non Ã¨ â€œperchÃ© non compra terreno?â€, ma:

> **quanto rendimento riesce a estrarre da un singolo Q grazie alla sincronizzazione temporale?**

---

## 4. Espansione non esclusa

Non interpretare il caso LuCcc come prova contro l'espansione.

Gli altri replay mostrano score di circa **88â€“95k** con maggiore scala produttiva.

Valutare quindi una possibile gerarchia:

```text
1. rendere stabile ed efficiente il ciclo produttivo di base;
2. stimare la service capacity necessaria;
3. replicare il ciclo su ulteriore superficie;
4. reagire alle condizioni di mercato;
5. evitare che l'espansione distrugga la periodicitÃ  acquisita.
```

L'espansione deve essere trattata come possibile **replica controllata di capacitÃ  produttiva funzionante**, non come semplice `BUY_LAND`.

Domanda chiave:

> **Se un Q Ã¨ temporalmente ottimizzato, quale quota del suo rendimento puÃ² essere conservata passando a 2Q o piÃ¹?**

Non assumere nÃ© linearitÃ  nÃ© regressione automatica.

---

## 5. PLAN vs REACT

Proporre una separazione esplicita tra:

### PLAN
- calendari biologici;
- cicli giornalieri;
- deadline di servizio;
- assegnazione workforce;
- staggering;
- routing programmato;
- sequenza di espansione;
- finestre di harvest / collect.

### REACT
- prezzo;
- inventory;
- domanda;
- cash insufficiente;
- weed o evento eccezionale;
- mancato servizio;
- deviazione dal calendario;
- opportunitÃ  di monetizzazione.

Valutare se il proprio MODEL_SPEC puÃ² essere riscritto come:

```text
PLANNED_BASELINE
+
REACTIVE_OVERRIDE
```

---

# Vincoli metodologici

1. **Non modificare ancora il codice.**
2. Questa fase Ã¨ **DEFINE / REVIEW del MODEL_SPEC**, non BUILD.
3. Nessun Kaggle run.
4. Nessun nuovo tournament.
5. Nessun tuning sugli score osservati.
6. Non copiare direttamente LuCcc, Gordeev, Dipin o ÐŸÐµÑ‚Ð°Ñ€.
7. Non leggere le nuove revisioni degli altri modeler prima del freeze della propria.
8. Non assumere che livestock sia obbligatorio o dannoso: valutarlo dai periodi e dalla resa.
9. Non assumere che espandere sia sempre meglio: misurare il rapporto tra scala e capacitÃ  di servizio.
10. Distinguere sempre:
   - `OWNED_SURFACE`
   - `ACTIVE_SURFACE`
   - `SERVICEABLE_SURFACE`
   - `PRODUCTIVE_SURFACE`
   - `MONETIZED_OUTPUT`

---

# Output richiesto

Aggiornare il proprio MODEL_SPEC solo se l'evidenza giustifica il cambiamento.

Produrre inoltre un report:

```text
results/model_spec_c2/periodic_model_review/<AGENT>_C2_PERIODIC_MODEL_REVIEW.md
```

Il report deve includere almeno:

## A. Evidenza osservata
Per ciascun replay:
- architettura produttiva;
- periodicitÃ  rilevate;
- anomalie;
- score;
- superficie;
- workforce;
- crop / animal mix;
- pattern di monetizzazione.

## B. Diagnosi del modello corrente
- parti threshold-centric;
- parti giÃ  periodiche;
- collisioni tra soglie e cicli biologici;
- eventuali inefficienze introdotte dal comportamento reattivo.

## C. Proposta architetturale
Classificare ogni meccanismo come:

```text
PLAN
REACT
HYBRID
REMOVE
```

## D. Ipotesi causale

Usare il formato:

```text
HYPOTHESIS_ID:
OBSERVED_PROBLEM:
EVIDENCE:
CAUSAL_MECHANISM:
MODEL_CHANGE:
EXPECTED_INTERMEDIATE_EFFECT:
EXPECTED_ECONOMIC_EFFECT:
FALSIFICATION_CONDITION:
```

## E. Period model

Proporre una struttura esplicita dei cicli, ad esempio:

```text
ENTITY_PERIOD_MODEL
- crop / animal
- phase
- nominal_period
- service_window
- hard_deadline
- expected_output
- required_worker_capacity
- reactive_overrides
```

## F. Espansione

Specificare se e come il modello dovrebbe poter passare:

```text
Q1 productive cycle
-> replicated cycle on Q2
-> eventual Q3/Q4
```

senza compromettere serviceability e periodicitÃ .

---

# Criterio di uscita

La fase termina con uno dei due verdetti:

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
```

oppure

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: NO
```

Se `YES`, il MODEL_SPEC revisionato deve essere pronto per una successiva fase PLAN/BUILD, ma **non implementare ancora**.

Se `NO`, documentare precisamente perchÃ© i replay non supportano una transizione significativa da soglie a periodi.

---

# Principio guida

Non chiedersi soltanto:

> â€œQuando lo stato supera una soglia, cosa faccio?â€

Chiedersi soprattutto:

> â€œQuale evento produttivo deve avvenire, con quale periodicitÃ , entro quale finestra e con quale capacitÃ  di servizio?â€

La componente reattiva deve intervenire dove esiste realmente incertezza economica o deviazione operativa, non sostituire il calendario biologico di base.
