# E11 — BUILD — ProductiveMassROIAgent

## Contesto

La fase **DEFINE** e la fase **PLAN** di:

> **E11 — 3× Productive Mass Expansion**

sono state completate.

Il benchmark E11-B0 ha confermato l'ipotesi preliminare di un gap nell'ordine di circa **3×** tra la baseline corrente E10-01 e i top player osservati.

Baseline ufficiale:

> **E10-01 Mean Final Money = $23,515.87**

Criteri E11 approvati:

- **Minimum Success Threshold:** Mean Final Money **≥ $50,000**
- **Competitive Target:** Mean Final Money **≥ $75,000**

Il principio strategico rimane:

> **Mass first, efficiency second.**

E11 deve quindi produrre un **salto architetturale**, non una serie di micro-ottimizzazioni di E10.

---

# 1. Obiettivo di questo task

Procedere alla fase:

> **E11 BUILD — ProductiveMassROIAgent**

implementando una prima versione completa **E11-01** della nuova architettura Productive Mass Expansion.

E11-01 deve già includere le principali leve strutturali identificate dal benchmark:

1. espansione fino a 4 quadranti / 100 tile;
2. workforce scaling;
3. worker locality;
4. crop portfolio diversificato;
5. livestock e products;
6. capital reinvestment;
7. end-game transition;
8. instrumentation sufficiente per diagnosticare il risultato.

Tuttavia:

> **E11-01 deve implementare l'architettura, non pretendere di avere già trovato i parametri ottimali.**

Le soglie definite nel PLAN devono quindi essere trattate come **ipotesi iniziali configurabili**.

---

# 2. Correzione preliminare del PLAN

Prima di implementare il codice, aggiornare:

`docs/versions/E11_plan_productive_mass_expansion.md`

per chiarire esplicitamente che alcuni valori presenti nel PLAN rappresentano:

> **E11-01 Initial Hypotheses**

e NON risultati già validati sperimentalmente.

In particolare trattare come parametri iniziali configurabili:

- giorni/fasi di espansione;
- soglie di active tiles;
- soglie di cash;
- rapporto worker / active tiles;
- numero massimo/minimo di worker;
- operating reserve;
- reinvestment threshold;
- numero di Wheat tiles;
- numero di Cow;
- numero di Sheep;
- timing di introduzione livestock;
- eventuali soglie di fine reinvestimento.

Non modificare il benchmark E11-B0.

Non modificare:

- `$50k Minimum Success`
- `$75k Competitive Target`

---

# 3. Correzione della gerarchia delle azioni

Il PLAN precedente proponeva:

`HIRE/BUY_LAND > WATER > FEED_ANIMALS > HARVEST_PRODUCTS > HARVEST_CROPS > PLANT > DIG > MOVE > PASS`

Questa gerarchia NON deve essere implementata rigidamente.

`HIRE` e `BUY_LAND` sono decisioni strategiche di investimento.

Non devono sistematicamente interrompere azioni produttive urgenti.

Implementare invece una gerarchia concettuale del tipo:

## Tier 1 — Urgent Productive Actions

Azioni che, se rinviate, producono perdita diretta di output o capacità:

- raccolta di crop maturi quando temporalmente critica;
- raccolta products quando temporalmente critica;
- feeding/care livestock quando necessario;
- watering quando necessario per evitare ritardi/perdite produttive.

## Tier 2 — Productive Continuity

Azioni necessarie a mantenere il ciclo:

- planting;
- replanting;
- altre azioni operative necessarie alla continuità.

## Tier 3 — Strategic Reinvestment

Solo quando le attività urgenti sono sotto controllo:

- `BUY_LAND`
- `HIRE`
- acquisto animali;
- allocazione di capitale a nuova capacità produttiva.

## Tier 4 — Capacity Preparation

- preparazione di tile;
- movement;
- attività necessarie alla futura produzione.

## Tier 5 — PASS

Solo se non esistono azioni economicamente utili.

La gerarchia effettiva deve rispettare le meccaniche reali dell'ambiente.

Non introdurre una priorità teorica incompatibile con l'action model Kaggriculture.

---

# 4. Principio di implementazione: parametrico, non hard-coded

La nuova strategia deve permettere di modificare i parametri E11 nelle iterazioni successive senza riscrivere l'architettura.

Creare quindi una configurazione E11 centralizzata, coerente con l'architettura esistente del repository.

Per esempio, se compatibile con il codice corrente:

```python
@dataclass
class ProductiveMassConfig:
    ...
```

oppure altra struttura equivalente già utilizzata nel progetto.

Evitare costanti sparse nel codice.

I parametri devono essere raggruppati almeno per:

- land expansion;
- workforce;
- crop portfolio;
- livestock;
- capital reserve;
- reinvestment;
- locality;
- end-game.

Non introdurre astrazioni inutilmente complesse.

Preferire la soluzione minima che consenta E11-02/E11-03 modificando configurazione invece di architettura.

---

# 5. Land Expansion

E11 deve poter raggiungere:

> **4 quadranti / 100 tile**

Questo è un requisito architetturale.

Non significa che debba acquistare sempre e comunque tutto il terreno indipendentemente dalla situazione economica.

Implementare trigger di espansione basati almeno su:

- capitale disponibile;
- operating reserve;
- capacità produttiva corrente;
- workforce;
- utilizzazione del terreno già posseduto;
- tempo residuo nell'episodio.

I valori presenti nel PLAN:

- Q1 Day 4–6;
- Q2 Day 8–10;
- Q3 Day 12–14;

devono essere trattati come **starting hypotheses**, non come trigger temporali obbligatori.

Preferire:

> economic readiness + productive readiness + sufficient remaining horizon

rispetto a:

> `if day == X`

---

# 6. Workforce Scaling

E11 deve supportare una workforce significativamente superiore a E10.

Benchmark osservato:

> **8–12 worker**

Questo è un **range competitivo osservato**, non un numero obbligatorio.

Implementare hiring dinamico basato almeno su:

- active productive tiles;
- backlog operativo;
- terreno posseduto;
- capitale disponibile;
- operating reserve;
- remaining horizon.

Il rapporto iniziale:

> circa 1 worker ogni 8–10 active tiles

può essere utilizzato come ipotesi E11-01.

Deve essere configurabile.

Verificare direttamente dal codice dell'ambiente il costo effettivo di `HIRE`.

Non assumere il valore cumulativo `$54` se non confermato dalle meccaniche reali.

Documentare il risultato della verifica.

---

# 7. Worker Locality dinamica

Implementare il concetto di:

> **preferred locality**

e NON una segregazione rigida dei worker.

Ogni worker può avere:

- quadrante preferenziale;
- regione preferenziale;
- insieme di tile preferite;

ma deve poter essere riallocato se un'altra zona presenta backlog produttivo urgente.

Obiettivo:

- ridurre movement cost;
- ridurre attraversamenti inutili della mappa;
- mantenere capacità di risposta ai picchi di lavoro.

Non implementare rigidamente:

`Q0 → W0,W1`
`Q1 → W2,W3`
`Q2 → W4,W5`
`Q3 → W6,W7`

come vincolo assoluto.

Può essere usato come configurazione preferenziale iniziale.

Prevedere fallback verso attività urgenti fuori zona quando economicamente necessario.

---

# 8. Crop Portfolio

Analizzare direttamente il catalogo `CROPS` dell'ambiente prima di implementare la configurazione.

Verificare:

- seed price;
- market price;
- growth duration;
- eventuali requisiti;
- eventuale relazione con livestock;
- altre proprietà economicamente rilevanti.

Non assumere automaticamente come corretti i valori del PLAN.

La strategia E11-01 deve supportare almeno tre funzioni economiche.

## Liquidity Crops

Crop a ciclo breve destinati a sostenere il cash flow.

## Growth Crops

Crop destinati alla crescita del revenue e della massa economica.

## Strategic / Feed Crops

Crop necessari o utili al livestock oppure ad altre funzioni produttive.

La configurazione iniziale può utilizzare:

- Carrot;
- Tomato;
- Melon;
- Strawberry;
- Wheat;

se l'ispezione dell'ambiente ne conferma l'utilità.

Non diversificare semplicemente per aumentare il numero di crop.

Ogni crop deve avere una funzione economica esplicita.

---

# 9. Dynamic Crop Allocation

Evitare una distribuzione completamente statica delle tile.

La composizione dovrebbe poter cambiare almeno tra:

### Early game

priorità alla liquidità.

### Mid game

priorità all'espansione della capacità e al revenue.

### Mature mass phase

massimizzazione dell'output della capacità disponibile.

### End game

selezione di crop compatibili con il tempo residuo.

Una coltura non deve essere piantata se non può realisticamente maturare e produrre valore entro la fine dell'episodio.

---

# 10. Livestock & Products

E11-01 deve includere il livestock.

Questa è una differenza architetturale fondamentale rispetto a E10.

Prima dell'implementazione verificare direttamente nell'ambiente:

- animali disponibili;
- purchase price;
- feed requirements;
- production interval;
- products;
- product price;
- workload;
- movement requirements;
- tile requirements;
- eventuali altre condizioni.

I valori del PLAN:

- 6 Cow;
- 4 Sheep;
- Milk `$160`;
- Wool `$200`;

devono essere verificati.

Le quantità **6 Cow + 4 Sheep** devono essere trattate come ipotesi E11-01, non come configurazione ottimale dimostrata.

L'introduzione del livestock deve dipendere almeno da:

- capitale disponibile;
- terreno disponibile;
- feed capacity;
- workforce capacity;
- remaining horizon.

Evitare **premature livestock entry**.

---

# 11. Capital Reinvestment Model

Implementare una distinzione esplicita tra:

## Operating Reserve

Capitale necessario per non compromettere la produzione esistente.

## Productive Reinvestment Pool

Capitale disponibile per:

- land;
- workforce;
- seeds;
- livestock;
- altri asset produttivi.

## Idle Capital

Cash non necessario alla continuità produttiva che rimane inutilizzato pur essendoci investimenti con orizzonte sufficiente per produrre ritorno.

Il valore:

> `$300 operating reserve`

è un'ipotesi E11-01.

Il valore:

> `$1,500 reinvestment threshold`

è un'ipotesi E11-01.

Devono essere configurabili.

Non implementare:

> spend everything above reserve immediately

senza verificare la sostenibilità del ciclo successivo.

---

# 12. Growth Feedback Loop

L'architettura deve rendere esplicito il ciclo:

```text
PRODUCTION
    ↓
REVENUE
    ↓
AVAILABLE CAPITAL
    ↓
LAND / WORKFORCE / SEEDS / LIVESTOCK
    ↓
MORE PRODUCTIVE CAPACITY
    ↓
MORE PRODUCTION
```

La fase centrale dell'episodio deve cercare di mantenere questo loop attivo.

L'instrumentation deve permettere di capire se il loop:

- accelera;
- rimane lineare;
- si blocca;
- produce overexpansion;
- produce liquidity collapse.

---

# 13. Economic Phases

È possibile mantenere il modello a cinque fasi:

1. Bootstrap
2. First Expansion
3. Mass Scaling
4. Full Mass Engine
5. End-Game Flush

ma i giorni:

- 1–5;
- 6–10;
- 11–18;
- 19–26;
- 27–30;

devono essere trattati come **starting boundaries**.

Quando possibile, combinare:

> temporal progress + economic state

per determinare la fase.

Per esempio:

- land ownership;
- active tiles;
- workforce;
- liquidity;
- livestock activation;
- remaining horizon.

---

# 14. End-Game Strategy

E11 deve avere una modalità esplicita di end-game.

Quando il tempo residuo non permette più a un investimento di produrre ritorno:

- ridurre o fermare `BUY_LAND`;
- ridurre o fermare `HIRE`;
- evitare nuovi animali non ammortizzabili;
- evitare crop che non maturano;
- privilegiare harvest;
- privilegiare product collection;
- privilegiare vendite;
- convertire capacità produttiva in final money.

L'end-game non deve essere semplicemente una data fissa.

Utilizzare, quando possibile:

> **remaining productive horizon**

---

# 15. Instrumentation obbligatoria

E11-01 deve essere molto più osservabile di E10.

Registrare, senza compromettere `actTimeout`, almeno:

### Economy

- current money;
- cumulative revenue, se ricostruibile;
- operating reserve;
- available reinvestment capital.

### Land

- quadrants owned;
- total tiles owned;
- active productive tiles;
- idle owned tiles.

### Workforce

- total workers;
- worker activity;
- idle workers, se ricostruibile;
- movement burden/proxy, se disponibile.

### Crop

- tiles per crop;
- mature crops;
- unplanted productive tiles;
- crop harvest/sales.

### Livestock

- animals by type;
- feed state;
- products generated;
- products collected;
- products sold.

### Investment Events

- BUY_LAND;
- HIRE;
- animal purchase;
- major seed allocation.

### Timing

Checkpoint almeno:

- 25%;
- 50%;
- 75%;
- 100%.

Non introdurre logging per-turn eccessivo se rischia di compromettere performance o leggibilità.

---

# 16. Diagnostic Metrics

Oltre a Mean Final Money, predisporre metriche che permettano di capire il failure mode.

Almeno:

- peak owned tiles;
- peak active tiles;
- peak workforce;
- final crop mix;
- livestock count;
- total land purchases;
- total hires;
- estimated/known investment by category;
- idle land ratio;
- idle capital proxy;
- expansion timing;
- livestock activation timing.

Se alcune metriche non sono ricostruibili dall'ambiente, documentarlo.

---

# 17. Failure Modes

Implementare safeguards semplici e osservabili per:

1. Overexpansion
2. Overhiring
3. Liquidity Collapse
4. Premature Livestock
5. Travel Dilution
6. Idle Land
7. Idle Capital
8. End-Game Overinvestment

Non creare un sistema eccessivamente complesso di regole preventive.

Il primo obiettivo è rendere il failure mode **misurabile**.

Successivamente E11-02 potrà correggerlo.

---

# 18. E11-01 deve essere un salto architetturale

Questo punto è fondamentale.

Non costruire E11-01 introducendo una leva alla volta:

- prima land;
- poi workforce;
- poi crop;
- poi livestock.

E11-01 deve già integrare:

> **Land + Workforce + Crop Portfolio + Livestock + Reinvestment + Locality**

perché l'ipotesi E11 riguarda il **sistema produttivo complessivo**.

Le successive iterazioni serviranno a identificare e correggere il collo di bottiglia dominante.

---

# 19. Evitare l'ottimizzazione prematura

Durante BUILD:

- non effettuare grid search;
- non effettuare parameter sweep;
- non cercare il miglior numero di Cow;
- non cercare il miglior operating reserve;
- non cercare il giorno perfetto per Q2;
- non ottimizzare il crop mix.

Utilizzare configurazioni iniziali ragionevoli e documentate.

Lo scopo di E11-01 è rispondere prima alla domanda:

> **Questa architettura riesce effettivamente a produrre un salto di massa?**

---

# 20. Implementazione

Implementare:

`src/agricola/strategy/productive_mass_roi.py`

con classe:

`ProductiveMassROIAgent`

oppure adattare naming/path solo se l'architettura effettiva del repository richiede una convenzione diversa.

Aggiornare il necessario affinché l'agente sia utilizzabile dal benchmark esistente.

Non rompere le strategie precedenti.

E10 deve rimanere riproducibile.

---

# 21. Test

Creare:

`tests/test_e11_productive_mass.py`

o equivalente coerente con la struttura esistente.

Testare almeno:

- configurazione caricabile;
- strategia istanziabile;
- action legality;
- expansion trigger;
- operating reserve;
- hiring safeguard;
- worker locality fallback;
- crop selection;
- livestock activation;
- end-game investment stop;
- assenza di regressioni evidenti sulle strategie precedenti.

Eseguire l'intera suite:

```powershell
.venv\Scripts\pytest.exe tests/
```

oppure il comando equivalente corretto per l'ambiente.

---

# 22. Benchmark locale E11-01

Dopo che BUILD e test sono completati, eseguire il benchmark locale standard utilizzato dal progetto.

Utilizzare condizioni confrontabili con E10-01.

Registrare almeno:

- Mean Final Money;
- Median;
- sample standard deviation (`ddof=1`);
- Min;
- Max;
- Completion Rate;
- Disqualification Rate;
- breakdown per opponent;
- delta assoluto vs E10-01;
- delta percentuale;
- ratio vs E10-01.

Baseline:

> `$23,515.87`

---

# 23. Decision Gate E11-01

Classificare il risultato secondo lo schema ufficiale:

| Mean Final Money | Verdict |
|---:|---|
| `< $50,000` | `FAIL` |
| `$50,000 – <$60,000` | `MINIMUM SUCCESS` |
| `$60,000 – <$70,000` | `COMPETITIVE` |
| `$70,000 – <$75,000` | `NEAR TOP BENCHMARK` |
| `≥ $75,000` | `TARGET ACHIEVED` |
| `> $75,000` | `BENCHMARK EXCEEDED` |

Ma NON fermarsi al solo valore finale.

Se `< $50k`, identificare il **dominant bottleneck** utilizzando l'instrumentation.

Per esempio:

- insufficient land expansion;
- insufficient active tile utilization;
- workforce bottleneck;
- travel bottleneck;
- crop-cycle bottleneck;
- liquidity collapse;
- livestock drag;
- idle capital;
- end-game failure.

---

# 24. Confronto della traiettoria

Confrontare E11-01 con E10-01 non soltanto al termine.

Utilizzare checkpoint:

- 25%;
- 50%;
- 75%;
- 100%.

La domanda principale è:

> **E11 sta generando compounding oppure semplicemente spendendo più capitale?**

Verificare quindi se:

- productive footprint cresce;
- workforce cresce;
- revenue acceleration aumenta;
- reinvestment produce nuova capacità;
- nuova capacità produce ulteriore revenue.

---

# 25. Documentazione BUILD

Creare:

`docs/versions/E11_build_productive_mass_expansion.md`

Documentare:

1. modifiche apportate al PLAN;
2. architettura implementata;
3. configurazione E11-01;
4. parametri considerati ipotesi;
5. meccaniche dell'ambiente verificate;
6. land expansion;
7. workforce scaling;
8. worker locality;
9. crop portfolio;
10. livestock;
11. capital reinvestment;
12. scheduling;
13. end-game;
14. instrumentation;
15. test;
16. benchmark locale;
17. confronto E10-01 vs E11-01;
18. trajectory analysis;
19. failure-mode diagnosis;
20. decision gate.

---

# 26. Aggiornamento documentazione di progetto

Aggiornare coerentemente:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Non dichiarare E11 concluso.

Lo stato finale deve riflettere il risultato reale, per esempio:

> `E11-01 BUILD + LOCAL VERIFY COMPLETED — awaiting review`

---

# 27. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

Non effettuare ancora:

- commit finale E11;
- tag E11;
- push del tag;
- submission Kaggle;

salvo istruzioni successive.

---

# Deliverable finale

Al termine fermarsi e presentare:

1. **BUILD status**
2. **meccaniche dell'ambiente verificate**
3. **architettura implementata**
4. **configurazione E11-01 effettiva**
5. **parametri ancora considerati ipotesi**
6. **test result**
7. **Mean Final Money E11-01**
8. **Median / Std / Min / Max**
9. **delta e ratio vs E10-01**
10. **decision gate verdict**
11. **land raggiunto**
12. **active productive footprint**
13. **peak workforce**
14. **crop portfolio effettivamente utilizzato**
15. **livestock effettivamente attivato**
16. **reinvestment behavior**
17. **trajectory 25% / 50% / 75% / 100%**
18. **dominant bottleneck**
19. **file creati/modificati**
20. **proposta per E11-02**

## Regola finale

Se E11-01 non raggiunge `$50k`:

> **NON tornare automaticamente alle micro-ottimizzazioni.**

Prima identificare quale componente impedisce alla nuova architettura di generare il compounding atteso.

Se E11-01 raggiunge `$50k` ma non `$75k`:

> **considerare validata la direzione architetturale e ottimizzare il bottleneck dominante verso il Competitive Target.**

Se E11-01 raggiunge `$75k`:

> **considerare raggiunta la parità di massa economica con il benchmark top-player e preparare la successiva fase di efficiency optimization.**

**Fermarsi dopo BUILD + benchmark locale e attendere approvazione prima di procedere con ulteriori iterazioni o submission Kaggle.**