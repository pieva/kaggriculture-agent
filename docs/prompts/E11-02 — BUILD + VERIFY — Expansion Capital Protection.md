# E11-02 — BUILD + VERIFY — Expansion Capital Protection

## Contesto

La fase **E11-01 — ProductiveMassROIAgent** è stata completata con BUILD e verifica locale.

Il risultato economico è stato:

- **E10-01 paired baseline:** `$23,405.57`
- **E11-01 Mean Final Money:** `$23,837.57`
- **Delta:** `+$432.00`
- **Delta %:** `+1.85%`
- **Ratio vs E10-01:** `1.018×`
- **Paired wins vs E10-01:** `22 / 30`
- **Decision Gate:** `FAIL`, perché `< $50,000`

Tuttavia, E11-01 **non ha effettivamente dispiegato la nuova architettura di massa**.

Stato produttivo massimo osservato:

- **Land:** 50 tile / 2 quadranti
- **Active productive footprint:** 40 tile
- **Peak workforce:** 4 worker
- **Livestock:** 0
- **Q2:** non acquistato
- **Q3:** non acquistato

La diagnosi ha identificato un collo di bottiglia dominante:

> **Expansion Cash Lock**

Il capitale necessario all'acquisto di Q2/Q3 viene assorbito dall'acquisto di sementi e dalla produzione corrente prima che la cassa possa superare la soglia richiesta per `BUY_LAND`.

La sequenza osservata è:

```text
Q1 production
    ↓
cash generation
    ↓
high-value seed purchases
    ↓
cash remains below expansion threshold
    ↓
Q2 not purchased
    ↓
Q3 not purchased
    ↓
workforce remains at 4
    ↓
livestock remains OFF
    ↓
productive mass remains ≈ E10
```

Di conseguenza, il risultato economico di E11-01 **non costituisce ancora un test pieno dell'ipotesi Productive Mass Expansion**.

---

# 1. Obiettivo E11-02

Implementare e verificare:

> **E11-02 — Expansion Capital Protection**

La domanda sperimentale è:

> **Proteggendo prioritariamente il capitale necessario a sbloccare Q2 e Q3, ProductiveMassROIAgent riesce finalmente ad attivare il ciclo 100 tile → workforce scaling → livestock → compounding?**

E11-02 NON è una nuova architettura.

È una correzione mirata del **dominant bottleneck** identificato in E11-01.

Il resto dell'architettura deve rimanere il più possibile invariato.

---

# 2. Principio sperimentale

Non effettuare una generica ottimizzazione del cash.

Non fare tuning simultaneo di:

- crop mix;
- numero di worker;
- livestock count;
- operating reserve;
- locality;
- scheduling;
- end-game;
- altre soglie non direttamente collegate all'espansione.

La modifica E11-02 deve essere sufficientemente isolata da permettere una chiara attribuzione causale.

La nuova logica deve rispondere a questo principio:

> **Il capitale necessario al prossimo sblocco territoriale deve avere priorità sugli investimenti produttivi non indispensabili, fino al completamento dell'espansione prevista.**

---

# 3. Baseline da preservare

E11-02 deve partire da:

`ProductiveMassROIAgent`

implementato in:

`src/agricola/strategy/productive_mass_roi.py`

La configurazione E11-01 deve rimanere riproducibile.

Non sovrascrivere irrimediabilmente i parametri E11-01.

Preferire:

- nuova configurazione;
- variante identificabile;
- flag/config esplicito;

in modo da poter confrontare direttamente:

- E10-01
- E11-01
- E11-02

sugli stessi seed.

---

# 4. Expansion Capital Protection

Implementare un meccanismo esplicito di:

> **Protected Expansion Capital**

Quando il prossimo obiettivo territoriale è Q2 o Q3, una quota di capitale deve essere considerata **riservata** al prossimo `BUY_LAND`.

Il costo reale verificato è:

> `BUY_LAND = $1,000 per quadrante`

La protezione deve considerare anche la liquidità minima necessaria a non bloccare la produzione corrente.

Concettualmente:

```text
cash
  ├─ operating capital
  ├─ protected next-land capital
  └─ discretionary productive capital
```

Non implementare necessariamente questa formula in modo letterale se l'architettura esistente suggerisce una soluzione più semplice.

---

# 5. Priorità tra capitale di espansione e sementi

Il bottleneck E11-01 nasce perché la strategia continua ad acquistare sementi ad alto costo mentre Q2 non è ancora finanziato.

In E11-02, durante la fase di accumulo per il prossimo quadrante:

- mantenere la produzione corrente;
- evitare che il sistema si fermi;
- limitare gli acquisti non essenziali;
- proteggere la quota di capitale necessaria a `BUY_LAND`.

In particolare:

> **gli acquisti di sementi non urgenti non devono impedire il raggiungimento della soglia per il prossimo quadrante.**

Questo NON significa interrompere completamente planting e replanting.

Significa distinguere tra:

### Essential productive spending

Spesa necessaria per evitare che la produzione corrente collassi.

### Expansion-blocking discretionary spending

Spesa che può essere rinviata senza perdita produttiva immediata e che impedirebbe il raggiungimento del capitale di espansione.

---

# 6. Crop spending durante l'accumulo

E11-01 ha mostrato che gli acquisti di crop relativamente costosi possono ritardare Q2.

Durante la fase di protezione capitale:

- privilegiare, se economicamente sensato, crop compatibili con liquidità più rapida o minore assorbimento di capitale;
- non saturare automaticamente tutte le tile con seed costosi;
- evitare di lasciare però una porzione significativa del terreno improduttiva.

Non cambiare completamente il crop portfolio.

La modifica deve essere una **spending policy**, non un nuovo esperimento crop.

Se necessario, introdurre un concetto configurabile di:

> `expansion_mode_crop_budget`

oppure equivalente.

---

# 7. Trigger di BUY_LAND

Una volta disponibile il capitale sufficiente, `BUY_LAND` deve essere eseguito senza ritardi non necessari.

Per Q2 e Q3:

- verificare che l'acquisto sia legalmente possibile;
- verificare che resti sufficiente capitale operativo;
- acquistare il quadrante quando la condizione economica è soddisfatta.

Evitare che altre azioni strategiche rinviino continuamente `BUY_LAND`.

Tuttavia:

> le azioni produttive realmente urgenti continuano ad avere priorità.

La gerarchia 5-tier introdotta in E11-01 rimane valida.

---

# 8. Q2 e Q3 sono obiettivi E11-02

E11-02 deve essere progettato per tentare esplicitamente:

1. acquisto Q2;
2. utilizzo Q2;
3. accumulo capitale;
4. acquisto Q3;
5. utilizzo Q3.

Il risultato dell'esperimento deve registrare chiaramente:

- se Q2 è stato acquistato;
- giorno/turno di Q2;
- se Q3 è stato acquistato;
- giorno/turno di Q3;
- cash immediatamente prima e dopo;
- productive footprint prima e dopo.

---

# 9. Workforce scaling deve rimanere downstream

Non forzare l'assunzione di 8–10 worker prima dell'espansione.

La workforce deve continuare a scalare in risposta a:

- active tiles;
- backlog;
- land ownership;
- available capital.

La nuova protezione del capitale deve però evitare che l'hiring consumi prematuramente il capitale destinato al prossimo quadrante, se questo rappresenta ancora il bottleneck prioritario.

Quindi durante l'accumulo per Q2/Q3:

> **BUY_LAND capital protection ha precedenza su hiring discrezionale, salvo carenza di workforce che renda impossibile mantenere produttiva la superficie già attiva.**

---

# 10. Livestock deve rimanere downstream

Non anticipare artificialmente livestock in E11-02.

Il suo comportamento deve rimanere coerente con E11-01.

La domanda è verificare se:

```text
Q2/Q3 unlocked
    ↓
more productive tiles
    ↓
workforce scaling
    ↓
feed capacity
    ↓
livestock activation
```

si attiva naturalmente.

Il livestock non deve consumare capitale protetto per Q2/Q3.

Una volta completata l'espansione territoriale prevista, il capitale protetto può essere rilasciato e destinato a livestock e altra capacità.

---

# 11. Nuova configurazione E11-02

Creare una configurazione esplicita, per esempio:

```python
E11_02_CONFIG
```

oppure struttura equivalente coerente con il repository.

I parametri nuovi devono essere pochi e strettamente collegati al bottleneck.

Per esempio:

```text
protect_expansion_capital = True
next_land_cost = 1000
expansion_operating_buffer = ...
expansion_crop_budget = ...
prefer_land_before_optional_hire = True
prefer_land_before_livestock = True
```

Questi nomi sono indicativi.

Non introdurre configurazioni inutilmente complesse.

---

# 12. Invarianti rispetto a E11-01

Salvo modifica necessaria per correggere l'Expansion Cash Lock, mantenere invariati:

- architecture;
- worker locality;
- crop catalog;
- livestock subsystem;
- target livestock count;
- reinvestment framework;
- 5-tier action hierarchy;
- end-game logic;
- telemetry;
- benchmark protocol.

Documentare qualsiasi deviazione necessaria.

---

# 13. Instrumentation specifica E11-02

Aggiungere telemetria sufficiente a osservare la protezione capitale.

Registrare almeno:

### Expansion Capital

- current cash;
- protected expansion capital target;
- amount currently protected;
- discretionary cash;
- operating reserve;
- next quadrant target.

### Spending During Protection

- seed spending;
- hiring spending;
- livestock spending;
- other discretionary spending.

### Expansion Events

- Q1 purchase;
- Q2 purchase;
- Q3 purchase;
- day/turn;
- cash before;
- cash after.

### Blocked Expansion

Se un quadrante non viene acquistato, registrare la causa:

- insufficient cash;
- operating reserve;
- insufficient productive readiness;
- insufficient workforce;
- remaining horizon;
- other.

Questo è essenziale.

---

# 14. Test specifici E11-02

Estendere:

`tests/test_e11_productive_mass.py`

oppure creare test dedicati se più appropriato.

Testare almeno:

1. capitale Q2 protetto da acquisto seed discrezionale;
2. capitale Q3 protetto;
3. essential planting ancora possibile;
4. BUY_LAND eseguito quando la soglia è raggiunta;
5. operating reserve rispettata;
6. hiring discrezionale non consuma capitale protetto;
7. livestock non consuma capitale protetto;
8. protezione capitale rilasciata dopo l'espansione;
9. E11-01 rimane riproducibile;
10. action legality.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

Tutti i test esistenti devono rimanere verdi.

---

# 15. Benchmark locale E11-02

Eseguire un nuovo benchmark paired da **30 episodi** sugli stessi seed utilizzati per E11-01.

Confrontare almeno:

- E10-01
- E11-01
- E11-02

Se lo script esistente consente di mantenere anche le versioni precedenti, conservarle.

Metriche obbligatorie:

- Mean Final Money;
- Median;
- sample Std Dev (`ddof=1`);
- Min;
- Max;
- Completion Rate;
- Disqualification Rate;
- breakdown per opponent;
- paired wins vs E10-01;
- paired wins vs E11-01;
- delta assoluto;
- delta percentuale;
- ratio.

---

# 16. Metriche architetturali obbligatorie

E11-02 deve essere valutato non soltanto sul money.

Registrare almeno:

- max quadrants owned;
- Q2 unlock rate;
- Q3 unlock rate;
- mean Q2 unlock day;
- mean Q3 unlock day;
- peak owned tiles;
- peak active productive tiles;
- peak workforce;
- livestock activation rate;
- Cow count;
- Sheep count;
- crop distribution;
- idle owned land;
- idle cash.

Queste metriche sono fondamentali per stabilire se abbiamo realmente testato Productive Mass Expansion.

---

# 17. Success Gate intermedio architetturale

Prima del gate economico, classificare il dispiegamento architetturale.

## ARCHITECTURE NOT DEPLOYED

Se E11-02 rimane prevalentemente:

- 2 quadranti;
- circa 40 active tiles;
- circa 4 worker;
- livestock OFF;

allora il bottleneck non è stato risolto.

Non interpretare il final money come test completo dell'ipotesi E11.

---

## PARTIAL MASS DEPLOYMENT

Se:

- Q2 viene acquistato stabilmente;
- active footprint aumenta;
- workforce inizia a scalare;

ma Q3/livestock non vengono raggiunti stabilmente.

Interpretare il risultato come avanzamento parziale.

---

## FULL MASS DEPLOYMENT

Considerare la nuova architettura effettivamente dispiegata quando la maggioranza delle run raggiunge indicativamente:

- **4 quadranti / 100 tile owned**;
- **significativo aumento active footprint**;
- **≥8 worker**, salvo evidenza che meno worker siano sufficienti;
- **livestock attivato**.

Solo a questo punto il risultato economico costituisce un vero test dell'ipotesi E11.

---

# 18. Decision Gate economico

La classificazione E11 rimane invariata:

| Mean Final Money | Verdict |
|---:|---|
| `< $50,000` | `FAIL` |
| `$50,000 – <$60,000` | `MINIMUM SUCCESS` |
| `$60,000 – <$70,000` | `COMPETITIVE` |
| `$70,000 – <$75,000` | `NEAR TOP BENCHMARK` |
| `≥ $75,000` | `TARGET ACHIEVED` |
| `> $75,000` | `BENCHMARK EXCEEDED` |

Ma il deliverable deve combinare:

> **Architecture Deployment Verdict + Economic Verdict**

Per esempio:

```text
FULL MASS DEPLOYMENT + FAIL
```

significherebbe:

> la massa è stata effettivamente dispiegata, ma l'architettura non genera ancora abbastanza valore.

Questo sarebbe molto diverso da E11-01.

---

# 19. Trajectory Analysis

Confrontare E10-01, E11-01 ed E11-02 ai checkpoint:

- 25%;
- 50%;
- 75%;
- 100%.

Registrare almeno:

- cash;
- quadrants;
- active tiles;
- workforce;
- livestock;
- cumulative/estimated revenue.

La domanda chiave è:

> **Dopo Q2/Q3, la curva economica di E11-02 cambia pendenza?**

Cerchiamo evidenza di:

> **compounding**

e non soltanto di maggiore spesa.

---

# 20. Dominant Bottleneck Diagnosis

Dopo il benchmark identificare un solo:

> **dominant bottleneck**

oppure dichiarare esplicitamente che il bottleneck dominante non è distinguibile.

Possibili esiti:

- expansion capital lock ancora presente;
- insufficient active-tile ramp after land purchase;
- workforce scaling bottleneck;
- worker travel dilution;
- seed capital bottleneck;
- livestock activation bottleneck;
- feed bottleneck;
- crop-cycle bottleneck;
- end-game conversion bottleneck;
- idle capital after expansion.

Non fare tuning ulteriore nello stesso task.

---

# 21. Deliverable E11-02

Creare:

`docs/versions/E11_02_expansion_capital_protection.md`

Il documento deve contenere almeno:

1. Executive Summary
2. E11-01 Failure Diagnosis
3. E11-02 Hypothesis
4. Controlled Change
5. Expansion Capital Protection Logic
6. Spending Policy During Protection
7. Q2/Q3 Trigger Logic
8. Configuration Delta E11-01 → E11-02
9. Tests
10. Benchmark Protocol
11. Benchmark Results
12. E10-01 vs E11-01 vs E11-02
13. Q2/Q3 Unlock Analysis
14. Workforce Scaling
15. Active Footprint Scaling
16. Livestock Activation
17. Trajectory 25/50/75/100
18. Architecture Deployment Verdict
19. Economic Decision Gate
20. Dominant Bottleneck
21. Recommendation for E11-03

---

# 22. Aggiornamento documentazione

Aggiornare coerentemente:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato finale:

> **E11-02 BUILD + LOCAL VERIFY COMPLETED — awaiting supervisor review**

Non dichiarare E11 completato.

---

# 23. Git

Al termine eseguire:

```powershell
git status
git diff --stat
git diff --check
```

Non effettuare:

- commit finale;
- tag;
- push;
- submission Kaggle;

senza istruzioni successive.

---

# Deliverable finale

Al termine fermarsi e presentare:

1. **E11-02 BUILD status**
2. **modifica controllata introdotta**
3. **test result**
4. **Mean Final Money**
5. **Median / Std / Min / Max**
6. **delta vs E10-01**
7. **delta vs E11-01**
8. **paired wins**
9. **Q2 unlock rate**
10. **Q2 mean unlock timing**
11. **Q3 unlock rate**
12. **Q3 mean unlock timing**
13. **peak land**
14. **peak active tiles**
15. **peak workforce**
16. **livestock activation rate**
17. **crop portfolio**
18. **trajectory 25/50/75/100**
19. **Architecture Deployment Verdict**
20. **Economic Decision Gate Verdict**
21. **dominant bottleneck**
22. **file creati/modificati**
23. **proposta E11-03**

## Regola finale

Se E11-02 **non sblocca Q2/Q3**, correggere successivamente ancora il meccanismo di espansione: non passare a tuning di efficienza.

Se E11-02 **sblocca la massa ma resta sotto $50k**, considerare finalmente l'ipotesi Productive Mass realmente testata e identificare il nuovo collo di bottiglia.

Se E11-02 raggiunge **≥$50k**, la direzione E11 è validata e le iterazioni successive devono puntare direttamente verso **$75k**.

Se E11-02 raggiunge **≥$75k**, il benchmark competitivo è raggiunto e il focus può passare dall'espansione della massa all'efficienza.

**Fermarsi dopo BUILD + LOCAL VERIFY. Non procedere automaticamente a E11-03 o Kaggle.**