# E11 — Correzione DEFINE + PLAN — 3× Productive Mass Expansion

## Contesto

La fase **DEFINE di E11 — 3× Productive Mass Expansion** è stata completata e il benchmark E11-B0 ha confermato l'ipotesi preliminare di un gap economico nell'ordine di circa **3×** tra la configurazione corrente E10-01 e i top player osservati.

Il benchmark ha rilevato:

- **E10-01 Mean Final Money:** `$23,515.87`
- **Top Player Benchmark Mean Final Money:** circa `$70,000–$75,000`
- **Gap economico:** circa `2.98×–3.19×`
- **Land:** 50 tile E10 contro 100 tile top player
- **Active productive footprint:** 40 contro circa 75–90 tile
- **Workforce:** 4 contro circa 8–12 worker
- **Crop:** 3 contro circa 4–5
- **Livestock:** OFF in E10, attivo nei top player
- **Reinvestment:** significativamente più aggressivo nei top player

Il benchmark ha quindi confermato che E11 deve affrontare prima di tutto un problema di **massa produttiva**, non una semplice inefficienza marginale della policy corrente.

---

# IMPORTANTE — Correzione del DEFINE

Prima di iniziare il PLAN, correggere formalmente una conclusione del precedente documento DEFINE.

La precedente formulazione:

- E11 Primary Target = `$45,000`
- E11 Stretch Target = `$60,000`

**non è approvata e deve essere sostituita.**

Il benchmark mostra che il riferimento competitivo è circa `$75,000`.

Non vogliamo progettare E11 per fermarsi volontariamente a metà del gap.

La distinzione corretta è tra:

1. **target competitivo dell'esperimento**;
2. **soglia minima di successo della nuova architettura**.

---

# 1. Target quantitativi E11 approvati

## Competitive Target

> **E11 Competitive Target: Mean Final Money ≥ $75,000**

Questo è il vero obiettivo dell'esperimento.

Rappresenta il raggiungimento della massa economica osservata nei top player.

L'architettura E11 deve quindi essere progettata fin dall'inizio con una capacità produttiva teoricamente compatibile con questo livello.

---

## Minimum Success Threshold

> **E11 Minimum Success Threshold: Mean Final Money ≥ $50,000**

La soglia `$50,000` NON è il target della policy.

È la soglia minima per considerare riuscito il cambio di architettura rispetto a E10-01.

Con baseline:

`$23,515.87`

il raggiungimento di `$50,000` rappresenterebbe già un aumento di circa:

`+112.6%`

ma lascerebbe ancora un gap sostanziale rispetto al benchmark competitivo.

Pertanto:

| Mean Final Money | Valutazione |
|---:|---|
| `< $50k` | **FAIL — massa produttiva insufficiente** |
| `$50k – <$60k` | **Minimum Success raggiunto — forte gap residuo** |
| `$60k – <$70k` | **Architettura competitiva — richiede ottimizzazione** |
| `$70k – <$75k` | **Near Top Benchmark** |
| `≥ $75k` | **E11 TARGET ACHIEVED** |
| `> $75k` | **Top Benchmark exceeded** |

Questa classificazione deve essere riportata nella documentazione E11.

---

# 2. Correggere la documentazione DEFINE

Prima del PLAN aggiornare:

`docs/versions/E11_define_productive_mass_expansion.md`

Sostituendo i precedenti target `$45k/$60k` con:

- **Minimum Success Threshold:** `$50,000 Mean Final Money`
- **Competitive Target:** `$75,000 Mean Final Money`

Aggiornare coerentemente anche:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Non modificare i risultati quantitativi del benchmark E11-B0.

La correzione riguarda esclusivamente **l'interpretazione e i criteri di successo derivati dal benchmark**.

---

# 3. Avviare E11 PLAN

Dopo avere corretto il DEFINE, procedere alla fase:

> **E11 PLAN — 3× Productive Mass Expansion**

Obiettivo del PLAN:

progettare una nuova architettura produttiva capace teoricamente di raggiungere il benchmark competitivo di **$75k Mean Final Money**, utilizzando **$50k esclusivamente come soglia minima di successo sperimentale**.

Non progettare una policy "da $50k".

Non limitare artificialmente terreno, workforce, crop, livestock o reinvestimento per raggiungere soltanto la soglia minima.

---

# 4. Principio architetturale

Il principio guida di E11 è:

> **Mass first, efficiency second.**

E11 deve modificare la scala operativa dell'agente.

Non deve essere semplicemente:

- E10 con più tile;
- E10 con più worker;
- E10 con soglie di capitale inferiori;
- E10 con qualche crop aggiuntivo;
- una combinazione di piccoli tuning dei parametri precedenti.

Serve una policy esplicitamente progettata per:

> **expand → staff → diversify → produce → reinvest → expand again**

La sequenza è un modello concettuale da verificare e adattare alle regole effettive dell'ambiente, non una macchina a stati da implementare ciecamente.

---

# 5. Architettura produttiva da progettare

Il PLAN deve affrontare congiuntamente almeno cinque sottosistemi.

## 5.1 Land Expansion

Progettare una strategia capace di arrivare a:

> **4 quadranti / 100 tile**

Il benchmark mostra che la piena espansione territoriale è una caratteristica strutturale dei top player.

Definire:

- condizioni per acquistare Q1;
- condizioni per acquistare Q2;
- condizioni per acquistare Q3;
- capitale minimo necessario;
- rapporto tra acquisto terreno e capacità di sfruttarlo;
- eventuali condizioni dinamiche invece di giorni hard-coded.

Evitare, se possibile, una strategia basata esclusivamente su:

`if day == X: BUY_LAND`

Preferire trigger economici e produttivi verificabili.

---

# 5.2 Workforce Scaling

Progettare una workforce capace di sostenere 100 tile.

Benchmark top:

> circa **8–12 worker**

Il PLAN deve determinare:

- quando assumere;
- quanti worker mantenere nelle diverse fasi;
- rapporto worker / active tiles;
- eventuale assegnazione territoriale;
- prevenzione del travel-time bottleneck;
- costo effettivo della workforce;
- condizioni per ulteriori assunzioni.

Non assumere automaticamente che 10 o 12 worker siano ottimali solo perché osservati nei top player.

Il benchmark indica la **scala**, non necessariamente la configurazione ottimale.

---

# 5.3 Crop Portfolio

E10 utilizza principalmente:

- Melon
- Carrot
- Wheat

Il benchmark top mostra una maggiore diversificazione.

Analizzare l'intero catalogo `CROPS` dell'ambiente e progettare un portafoglio capace di combinare:

### Liquidity crops

Cicli brevi che generano cash rapidamente.

### Growth crops

Crop con rendimento elevato utilizzabili per aumentare la massa economica.

### Strategic crops

Crop eventualmente necessari per sostenere livestock, prodotti o specifiche fasi della strategia.

Il PLAN deve evitare sia:

- monocultura rigida;
- diversificazione indiscriminata.

La scelta deve essere legata alla fase economica dell'agente.

---

# 5.4 Livestock & Products

Questa è una differenza strutturale fondamentale rispetto a E10.

E10:

> **Livestock OFF**

Top players:

> **Livestock ON**

Analizzare direttamente dall'ambiente:

- tipi di animali;
- costi;
- requisiti;
- tempi;
- prodotti generati;
- prezzi;
- eventuali input necessari;
- workload;
- frequenza delle azioni;
- vincoli territoriali.

Non assumere automaticamente che le quantità osservate nei replay siano ottimali.

Progettare una strategia di introduzione del livestock che non distrugga la liquidità necessaria alla fase di espansione.

Determinare quando il livestock diventa economicamente sostenibile.

---

# 5.5 Capital Reinvestment

E11 deve passare da una logica prevalentemente di **capital protection** a una logica di **productive reinvestment**.

Questo NON significa spendere tutto il cash disponibile.

Significa distinguere almeno:

### Operating reserve

Capitale necessario per mantenere operativa la produzione corrente.

### Expansion capital

Capitale destinato a:

- BUY_LAND
- HIRE
- seeds
- animals
- eventuali altri asset produttivi.

### Idle capital

Cash disponibile che non è necessario nel breve periodo e che potrebbe essere reinvestito produttivamente.

Progettare una regola esplicita che riduca l'accumulo improduttivo di cash durante la fase di crescita.

---

# 6. Strategia per fasi

Valutare una policy organizzata in **fasi economiche**, non semplicemente in giorni fissi.

Per esempio:

### Phase A — Bootstrap

Obiettivo:

- garantire liquidità;
- attivare la prima produzione;
- evitare insolvency.

### Phase B — First Expansion

Obiettivo:

- aumentare terreno;
- aumentare workforce;
- mantenere la produzione esistente.

### Phase C — Scaling

Obiettivo:

- accelerare l'utilizzo delle nuove tile;
- diversificare crop;
- continuare l'espansione.

### Phase D — Productive Mass

Obiettivo:

- arrivare a 4 quadranti;
- aumentare active tiles;
- introdurre/scalare livestock;
- aumentare workforce.

### Phase E — Exploitation / End Game

Obiettivo:

- ridurre investimenti che non possono più ripagarsi entro la fine dell'episodio;
- massimizzare harvest/sales/products;
- convertire capacità produttiva in final money.

Queste fasi sono indicative.

Il PLAN deve derivare le condizioni effettive dalle meccaniche dell'ambiente.

Preferire trigger basati sullo **stato economico e produttivo** rispetto a semplici soglie temporali quando possibile.

---

# 7. Worker Locality

Il DEFINE ha identificato come rischio il travel time su quattro quadranti.

Analizzare se sia conveniente introdurre una forma di:

> **worker locality / territorial assignment**

Per esempio assegnando gruppi di worker a specifici quadranti o regioni.

Non assumere automaticamente la configurazione:

`Q0 → W0,W1`
`Q1 → W2,W3`
`Q2 → W4,W5`
`Q3 → W6,W7`

Questa è un'ipotesi.

Il PLAN deve verificare:

- geometria della mappa;
- movement cost;
- distribuzione delle attività;
- possibilità di idle worker;
- necessità di redistribuzione dinamica.

Proporre l'architettura più semplice compatibile con una forte riduzione del travel overhead.

---

# 8. Scheduling delle azioni

Con 70–90 tile attive e 8–12 worker, il problema di scheduling cambia scala.

La policy deve gestire contemporaneamente:

- harvest;
- planting;
- watering;
- movement;
- livestock;
- product collection;
- expansion;
- hiring.

Definire una gerarchia delle azioni che impedisca:

- crop maturi non raccolti;
- tile vuote inutilizzate;
- watering sistematicamente in ritardo;
- livestock trascurato;
- worker che attraversano inutilmente tutta la mappa;
- expansion actions che interrompono attività produttive urgenti.

Non ereditare automaticamente la priorità E10 se non è adatta alla nuova scala.

---

# 9. Growth Feedback Loop

Il cuore di E11 deve essere un ciclo di crescita esplicito:

`PRODUCTION`
↓
`REVENUE`
↓
`AVAILABLE CAPITAL`
↓
`LAND / WORKFORCE / SEEDS / LIVESTOCK`
↓
`MORE PRODUCTIVE CAPACITY`
↓
`MORE PRODUCTION`

Il PLAN deve identificare:

- trigger;
- condizioni;
- limiti;
- riserve;
- priorità di investimento;

necessari affinché questo ciclo produca **compounding** durante la parte centrale dell'episodio.

---

# 10. Failure Modes

Identificare preventivamente almeno questi rischi:

### Overexpansion

Acquistare terreno senza workforce/capitale sufficiente per utilizzarlo.

### Overhiring

Aumentare workforce senza attività produttive sufficienti.

### Liquidity collapse

Investire troppo rapidamente e non avere capitale per semi/input.

### Livestock premature entry

Attivare livestock prima che il sistema possa sostenerne capitale e workload.

### Travel dilution

Aumentare workforce senza ottenere un aumento proporzionale delle azioni produttive.

### Idle land

Possedere 100 tile ma utilizzarne soltanto una piccola parte.

### Idle capital

Accumulo eccessivo di cash durante una fase in cui ulteriori investimenti avrebbero ancora tempo di ripagarsi.

### End-game overinvestment

Investimenti troppo tardivi che non recuperano il capitale entro la fine dell'episodio.

Per ogni failure mode proporre una misura osservabile.

---

# 11. Instrumentation

E11 introduce un salto di complessità.

Il PLAN deve quindi specificare instrumentation sufficiente a capire **perché** una run raggiunge o non raggiunge $50k/$75k.

Registrare almeno:

- money per day/checkpoint;
- cumulative revenue;
- quadranti posseduti;
- active productive tiles;
- crop distribution;
- workforce;
- worker utilization, se misurabile;
- livestock;
- products collected/sold;
- capital invested in land;
- capital invested in workforce;
- capital invested in seeds;
- capital invested in livestock;
- idle cash;
- timing degli expansion events.

Checkpoint preferiti:

- 25%
- 50%
- 75%
- 100%

dell'episodio.

---

# 12. Piano sperimentale

Non tentare di ottimizzare contemporaneamente decine di parametri.

Progettare una sequenza di implementazione e verifica che permetta di capire quale componente produce il salto di scala.

Tuttavia, evitare anche di ricadere nelle micro-iterazioni precedenti.

Il PLAN deve trovare un equilibrio tra:

> **architectural leap**

e

> **experimental attribution**

Proporre quindi una prima configurazione E11 sufficientemente completa da testare realmente la Productive Mass Expansion.

---

# 13. Criteri quantitativi

La baseline ufficiale rimane:

> **E10-01 Mean Final Money = $23,515.87**

### Minimum Success

`Mean Final Money ≥ $50,000`

### Competitive Target

`Mean Final Money ≥ $75,000`

Calcolare sempre anche:

- delta assoluto vs E10;
- delta percentuale vs E10;
- ratio vs E10;
- sample standard deviation (`ddof=1`);
- median;
- min/max;
- breakdown per opponent, quando applicabile;
- completion rate;
- disqualification rate.

Il valore medio rimane la metrica primaria, ma non accettare una configurazione estremamente instabile soltanto perché pochi episodi eccezionali alzano la media.

---

# 14. Decision Gate

Alla fine della futura fase BUILD/VERIFY:

## FAIL

`Mean Final Money < $50k`

La nuova architettura non produce ancora sufficiente massa produttiva.

Analizzare il collo di bottiglia prima di procedere con tuning marginale.

## PASS — OPTIMIZE

`$50k ≤ Mean Final Money < $75k`

L'architettura Productive Mass Expansion è validata.

Procedere con ottimizzazioni mirate verso il benchmark competitivo.

## TARGET ACHIEVED

`Mean Final Money ≥ $75k`

E11 ha raggiunto la massa economica del benchmark top-player.

A questo punto il focus può spostarsi progressivamente da:

> **mass expansion**

a:

> **efficiency optimization**

---

# 15. Deliverable PLAN

Creare:

`docs/versions/E11_plan_productive_mass_expansion.md`

Il documento deve contenere almeno:

1. Executive Summary
2. Corrected E11 Success Criteria
3. Architectural Objective
4. Environment Mechanics Relevant to Scaling
5. Land Expansion Strategy
6. Workforce Scaling Strategy
7. Worker Locality Strategy
8. Crop Portfolio Strategy
9. Livestock & Product Strategy
10. Capital Reinvestment Model
11. Economic Phase Model
12. Action Scheduling & Priorities
13. Growth Feedback Loop
14. End-Game Strategy
15. Failure Modes & Safeguards
16. Instrumentation
17. Experimental Design
18. E11 Initial Configuration
19. Expected Growth Trajectory
20. Minimum Success Gate — $50k
21. Competitive Target — $75k
22. BUILD Acceptance Criteria
23. Open Questions / Risks

Il PLAN deve indicare chiaramente quali componenti:

- riutilizzano codice esistente;
- richiedono modifica;
- richiedono nuovi moduli/classi;
- devono essere testate separatamente.

---

# 16. Aggiornamento stato progetto

Dopo il PLAN aggiornare coerentemente:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Registrare lo stato come:

> **E11 — PLAN COMPLETED / awaiting BUILD approval**

Non dichiarare E11 validato.

Non dichiarare raggiunto il target $75k.

---

# 17. Vincoli operativi

In questo task:

- correggere il DEFINE;
- produrre il PLAN;
- NON implementare ancora E11;
- NON modificare la policy produttiva;
- NON generare la submission;
- NON effettuare run Kaggle;
- NON effettuare tuning;
- NON trasformare osservazioni dei top player in regole rigide senza giustificazione;
- NON ottimizzare per $50k;
- NON ridurre il target competitivo da $75k.

In particolare:

> **$50k è il pavimento sperimentale, non il soffitto progettuale.**

E:

> **$75k è il target competitivo che deve guidare l'architettura E11.**

---

# Deliverable finale

Al termine fermarsi e presentare:

1. conferma della correzione del DEFINE;
2. target competitivo registrato;
3. minimum success threshold registrata;
4. sintesi dell'architettura proposta;
5. strategia land;
6. strategia workforce;
7. strategia crop;
8. strategia livestock/products;
9. modello di reinvestimento;
10. strategia di scheduling;
11. instrumentation prevista;
12. configurazione E11 iniziale proposta;
13. principali rischi;
14. file creati/modificati;
15. decisione richiesta per procedere al **BUILD**.

**Non procedere al BUILD senza approvazione.**