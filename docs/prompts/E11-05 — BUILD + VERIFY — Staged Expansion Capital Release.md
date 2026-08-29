# E11-05 — BUILD + VERIFY — Staged Expansion Capital Release

## Contesto

Le iterazioni E11-01 → E11-04 hanno isolato progressivamente il problema principale che impedisce a `ProductiveMassROIAgent` di trasformare l'espansione territoriale in massa economica competitiva.

I riferimenti quantitativi rimangono:

- **E10 baseline:** circa `$23k Mean Final Money`
- **Minimum Success Threshold E11:** `$50,000`
- **Competitive Target E11:** `$75,000`

Il principio generale rimane:

> **Mass first, efficiency second.**

---

# 1. Evidenze consolidate

## E11-01 — Expansion Cash Lock

La policy non riusciva a finanziare Q2/Q3 perché la produzione corrente assorbiva il capitale disponibile.

Esito architetturale:

- 2 quadranti
- 50 tile
- 4 worker
- livestock OFF

---

## E11-02 — Expansion Capital Protection

È stata introdotta una protezione rigida del capitale destinato al successivo `BUY_LAND`.

La cassa riusciva a raggiungere il livello richiesto, ma il gate:

`active_tiles >= 15`

impediva Q2.

---

## E11-03 — Expansion Gate Unlock

È stato introdotto:

`expansion_gate_mode = "MIN_OPERATIONAL"`

Risultati principali:

- **Q2 Unlock Rate:** `83.3%`
- **Q3 Unlock Rate:** `60.0%`
- **Q2 Mean Timing:** Day `5.4`
- **Q3 Mean Timing:** Day `11.2`
- **Peak land:** `4 quadranti / 100 tile`
- **Peak active tiles:** `54`
- **Peak workforce:** `6`
- **Livestock:** `0% activation`
- **Mean Final Money:** circa `$7.1k`

Conclusione:

> **Il Land Expansion Bottleneck è stato risolto.**

Ma la protezione rigida del capitale produceva starvation colturale.

---

## E11-04 — Seed–Expansion Synchronization

È stata tentata una protezione più permissiva:

- semi costosi consentiti sotto `$900`;
- protezione ripristinata vicino alla soglia del terreno.

Risultato:

- Q2 crollato da `83.3%` a `6.7%`
- Q3 crollato da `60.0%` a `0%`
- Mean Final Money: circa `$1.3k`

Conclusione:

> **Consentire investimenti colturali discrezionali prima di Q2 ricrea l'Expansion Cash Lock.**

Questa strada è da considerare falsificata.

---

# 2. Conclusione causale acquisita

La serie E11 ha ora mostrato due estremi:

### Protezione troppo rigida

```text
capital fully protected
    ↓
Q2/Q3 unlocked
    ↓
crop engine starved
    ↓
land under-monetized
```

### Protezione troppo permissiva

```text
high-value crop spending
    ↓
cash consumed
    ↓
Q2/Q3 blocked
    ↓
mass architecture never deployed
```

E11-05 deve testare un terzo modello:

> **rilascio progressivo e staged del capitale in funzione degli eventi territoriali.**

---

# 3. Obiettivo E11-05

Procedere con:

> **E11-05 — Staged Expansion Capital Release**

Domanda sperimentale:

> **Possiamo mantenere l'elevato tasso di sblocco territoriale di E11-03 e contemporaneamente introdurre una finestra produttiva controllata tra Q2 e Q3, così da iniziare a monetizzare la nuova capacità prima del completamento dell'espansione?**

E11-05 deve cercare per la prima volta di ottenere contemporaneamente:

> **land expansion + high-value productive activation**

senza modificare gli altri sottosistemi.

---

# 4. Ipotesi E11-05

Formalizzare:

> **H11-05 — Staged Capital Release Hypothesis:** la protezione del capitale deve essere differenziata per fase territoriale. Una protezione rigida fino a Q2, seguita da una finestra produttiva controllata e da una successiva nuova fase di accumulo per Q3, dovrebbe preservare l'espansione territoriale e consentire ai crop ad alto rendimento di maturare abbastanza presto da finanziare il compounding.

---

# 5. Esperimento controllato

E11-05 deve modificare esclusivamente:

> **capital/seed policy durante il percorso Q1 → Q2 → Q3**

Mantenere invariati rispetto a E11-03:

- `expansion_gate_mode = MIN_OPERATIONAL`
- readiness Q1/Q2/Q3
- land cost
- operating reserve
- workforce scaling
- max workers
- worker locality
- crop catalog
- livestock logic
- target Cow/Sheep
- feed logic
- action hierarchy
- end-game logic
- benchmark protocol

Non modificare altri sottosistemi.

---

# 6. Nuova macchina a stati economici

Implementare una policy esplicita basata su stati economici.

La struttura concettuale deve essere:

```text
ACCUMULATE_Q2
      ↓
BUY_Q2
      ↓
PRODUCTIVE_WINDOW
      ↓
ACCUMULATE_Q3
      ↓
BUY_Q3
      ↓
MASS_ACTIVATION
```

Non utilizzare semplicemente giorni fissi come regola primaria.

Le transizioni devono dipendere soprattutto dagli eventi realmente osservati.

---

# 7. Stato A — ACCUMULATE_Q2

Prima dell'acquisto di Q2:

> **mantenere la protezione rigida validata in E11-03.**

Obiettivo prioritario:

`BUY_LAND Q2`

Durante questo stato:

- mantenere operating reserve;
- consentire solo spesa colturale essenziale;
- bloccare seed discrezionali ad alto costo;
- evitare hiring opzionale che consumi il capitale protetto;
- evitare livestock;
- mantenere operativa la farm.

Questa fase non deve adottare la policy permissiva di E11-04.

---

# 8. Transizione A → B

La transizione deve avvenire sull'evento:

> **Q2 PURCHASED**

Non su un giorno fisso.

Registrare:

- day/turn;
- cash prima;
- cash dopo;
- active tiles;
- workforce.

---

# 9. Stato B — PRODUCTIVE_WINDOW

Subito dopo Q2, introdurre una finestra produttiva controllata.

Obiettivo:

> investire parte del capitale in crop capaci di maturare e generare revenue abbastanza presto da contribuire alla successiva crescita.

Questa fase deve essere temporaneamente meno restrittiva della protezione Q2.

Ma:

> **non deve rilasciare completamente ogni protezione territoriale.**

---

# 10. Productive Budget

Durante `PRODUCTIVE_WINDOW`, introdurre un budget esplicito destinato ai crop.

Questo budget deve essere:

- limitato;
- configurabile;
- distinto dall'operating reserve;
- distinto dal capitale destinato successivamente a Q3.

Non usare semplicemente:

`reserve = 300`

e consentire tutta la spesa residua.

Serve un concetto del tipo:

```text
productive_window_budget
```

oppure equivalente.

---

# 11. Productive Window Budget — criterio

Il budget non deve essere un magic number arbitrario se può essere derivato da una logica semplice.

Preferire una delle seguenti impostazioni:

### Opzione A — quota della liquidità post-Q2

```text
budget = fraction × disposable_cash
```

### Opzione B — cap massimo

```text
budget = min(configured_cap, disposable_cash)
```

### Opzione C — combinazione semplice

solo se realmente necessaria.

Evitare una logica troppo sofisticata.

Lo scopo è testare se **un rilascio limitato** è sufficiente.

---

# 12. Crop ammessi nella Productive Window

Riutilizzare il crop portfolio esistente.

Non effettuare crop optimization.

Consentire prioritariamente crop che:

- possono maturare entro il remaining horizon;
- hanno funzione di crescita/revenue;
- non richiedono spesa incompatibile con il successivo accumulo Q3.

In particolare verificare l'uso effettivo di:

- Tomato
- Strawberry
- Melon

insieme ai crop di liquidità già presenti.

Non forzare tutti i crop contemporaneamente.

---

# 13. Horizon-aware buying

Ogni seed acquistato nella Productive Window deve essere compatibile con il tempo residuo.

Verificare:

```text
current_day
+
growth_duration
+
harvest/market margin
<= episode_end
```

o criterio equivalente coerente con il modello temporale reale.

Non acquistare crop che finiranno inevitabilmente incompleti.

---

# 14. Trigger di uscita dalla Productive Window

La finestra produttiva non deve continuare indefinitamente.

Deve terminare quando diventa prioritario finanziare Q3.

La transizione può essere basata su:

- capitale disponibile;
- Q3 funding gap;
- tempo trascorso dall'acquisto Q2;
- remaining horizon;
- combinazione semplice di questi fattori.

Non usare principalmente:

> Day 12

senza tener conto dello stato economico.

---

# 15. Stato C — ACCUMULATE_Q3

Quando termina la Productive Window:

> **ripristinare una protezione rigida del capitale per Q3.**

In questo stato:

- bloccare nuovamente seed discrezionali;
- proteggere il capitale territoriale;
- mantenere solo spesa produttiva essenziale;
- evitare livestock;
- limitare hiring opzionale se interferisce con Q3.

Obiettivo prioritario:

> **BUY_LAND Q3**

---

# 16. Transizione C → D

La transizione avviene all'evento:

> **Q3 PURCHASED**

Registrare:

- timing;
- cash pre/post;
- active tiles;
- workers;
- crop state.

---

# 17. Stato D — MASS_ACTIVATION

Dopo Q3:

> **rilasciare la protezione territoriale.**

A questo punto tutti i 4 quadranti sono posseduti e non esiste un ulteriore `BUY_LAND`.

La priorità passa da:

> land acquisition

a:

> productive activation.

Consentire quindi al sistema esistente di utilizzare capitale per:

- seeds;
- workforce;
- livestock;
- altre attività previste da E11.

Non modificare però workforce/livestock logic in questa iterazione.

Il loro comportamento deve emergere naturalmente.

---

# 18. Nessuna nuova ottimizzazione dei crop

E11-05 NON deve introdurre:

- nuove percentuali ottimali per crop;
- nuovo crop scoring;
- nuovo ROI optimizer;
- grid search;
- parameter sweep;
- nuove soglie di irrigazione;
- nuove priorità harvest.

Utilizzare la logica crop esistente.

L'unico cambiamento riguarda:

> **quando il capitale viene reso disponibile alla produzione.**

---

# 19. Configurazione E11-05

Creare configurazione distinta e riproducibile:

`E11_05_CONFIG`

oppure equivalente.

Possibili nuovi parametri:

```text
capital_release_mode = "STAGED"
productive_window_enabled = True
productive_window_budget_fraction = ...
productive_window_budget_cap = ...
q3_reprotection_trigger = ...
```

Introdurre solo i parametri effettivamente necessari.

---

# 20. Telemetria della macchina a stati

Registrare per ogni episodio:

- stato economico corrente;
- timing ingresso `ACCUMULATE_Q2`;
- Q2 purchase;
- timing ingresso `PRODUCTIVE_WINDOW`;
- seed spending durante Productive Window;
- timing uscita Productive Window;
- timing ingresso `ACCUMULATE_Q3`;
- Q3 purchase;
- timing ingresso `MASS_ACTIVATION`.

Questo è obbligatorio.

---

# 21. Capital Flow Telemetry

Registrare almeno:

### ACCUMULATE_Q2

- cash
- operating reserve
- protected Q2 capital
- seed spending

### PRODUCTIVE_WINDOW

- initial cash
- allocated productive budget
- actual seed spending
- remaining budget
- revenue generata dai crop acquistati nella finestra, se ricostruibile

### ACCUMULATE_Q3

- Q3 funding gap
- cash
- protected capital
- blocked discretionary spending

### MASS_ACTIVATION

- cash available
- seed spending
- workforce spending
- livestock spending

---

# 22. Crop telemetry

Per almeno:

- Carrot
- Wheat
- Tomato
- Strawberry
- Melon

registrare:

- seed purchases
- seed spending
- first planting
- planted tiles
- harvest count
- harvested units
- revenue
- unfinished crop at episode end, se disponibile

Particolare attenzione a:

> crop acquistati durante la Productive Window.

---

# 23. Test specifici E11-05

Estendere la suite.

Testare almeno:

1. E11-03 rimane riproducibile.
2. E11-04 rimane riproducibile.
3. E11-05 parte in `ACCUMULATE_Q2`.
4. seed discrezionali bloccati prima di Q2.
5. evento Q2 attiva `PRODUCTIVE_WINDOW`.
6. Productive Window consente seed entro il budget.
7. Productive Window non supera il budget.
8. operating reserve rispettata.
9. crop fuori horizon non acquistati.
10. trigger di reprotection attiva `ACCUMULATE_Q3`.
11. seed discrezionali nuovamente bloccati durante Q3 accumulation.
12. Q3 può essere acquistato.
13. dopo Q3 entra `MASS_ACTIVATION`.
14. dopo Q3 la protezione territoriale viene rilasciata.
15. workforce logic invariata.
16. livestock logic invariata.
17. action legality.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

Tutti i test devono passare.

---

# 24. Benchmark locale

Eseguire benchmark paired da **30 episodi** sugli stessi seed.

Confrontare almeno:

- E10-01
- E11-01
- E11-03
- E11-04
- E11-05

Mantenere E11-02 se lo script lo consente senza complicazioni.

Metriche economiche:

- Mean Final Money
- Median
- Sample Std Dev (`ddof=1`)
- Min
- Max
- Completion Rate
- Disqualification Rate
- breakdown per opponent
- paired wins vs E10-01
- paired wins vs E11-03
- paired wins vs E11-04
- delta
- ratio

---

# 25. Gate architetturale principale

E11-05 deve almeno preservare sostanzialmente il risultato territoriale E11-03.

Baseline:

- Q2 Unlock = `83.3%`
- Q3 Unlock = `60.0%`

Utilizzare come riferimento operativo:

### Q2 preservation

> circa `≥80%`

### Q3 preservation

> circa `≥60%`

Non trattare questi valori come soglie matematiche assolute su un campione piccolo, ma usarli come segnale di regressione/non regressione.

---

# 26. Land Regression Verdict

Classificare:

## NO LAND REGRESSION

Q2/Q3 rimangono sostanzialmente ai livelli E11-03 o migliorano.

## MODERATE LAND REGRESSION

Una riduzione limitata accompagnata da forte miglioramento downstream, da analizzare.

## LAND REGRESSION

Q2/Q3 tornano sostanzialmente bloccati.

In caso di LAND REGRESSION:

> E11-05 è fallita indipendentemente dal miglioramento economico.

---

# 27. Productive Activation Gate

Per dimostrare progresso rispetto a E11-03 cercare:

- **Peak active tiles > 54**
- high-value crop realmente piantati;
- high-value crop realmente maturati;
- crop revenue significativamente superiore a E11-03;
- crescita della capacità utilizzata dopo Q2/Q3.

Non basta possedere 100 tile.

---

# 28. Workforce Observation

Non modificare workforce logic.

Ma registrare:

- peak workforce;
- workforce ai checkpoint;
- backlog;
- active tiles / worker;
- eventuale travel burden.

Se la Productive Window riesce e la superficie cresce, ci aspettiamo che il sistema possa superare i 6 worker.

Se non accade:

> workforce scaling può diventare il nuovo dominant bottleneck.

---

# 29. Livestock Observation

Non modificare livestock.

Registrare:

- activation rate;
- first activation;
- Cow count;
- Sheep count;
- Wheat availability;
- capitale disponibile al momento dell'attivazione.

Se land + crop + workforce funzionano ma livestock resta OFF:

> livestock activation diventa candidato per E11-06.

---

# 30. Trajectory Analysis

Confrontare almeno E11-03 ed E11-05 ai checkpoint:

- 25%
- 50%
- 75%
- 100%.

Registrare:

| Metric | 25% | 50% | 75% | 100% |
|---|---:|---:|---:|---:|
| Money | | | | |
| Economic State | | | | |
| Quadrants | | | | |
| Active tiles | | | | |
| Workforce | | | | |
| Crop revenue | | | | |
| Seed spending | | | | |
| Livestock | | | | |

La domanda è:

> **La finestra produttiva crea un aumento di revenue senza distruggere Q3?**

---

# 31. Compounding Test

Valutare il ciclo:

```text
Q2
 ↓
productive investment
 ↓
crop maturation
 ↓
revenue
 ↓
Q3
 ↓
mass activation
 ↓
more production
```

Classificare:

- `NOT OBSERVED`
- `WEAK`
- `PARTIAL`
- `STRONG`

Il verdetto deve essere motivato quantitativamente.

---

# 32. Architecture Deployment Verdict

Utilizzare:

### ARCHITECTURE NOT DEPLOYED

Q2 non stabile.

### PARTIAL LAND DEPLOYMENT

Q2 sì, Q3 sostanzialmente no.

### FULL LAND DEPLOYMENT

4 quadranti ottenuti con downstream ancora insufficiente.

### PARTIAL MASS DEPLOYMENT

4 quadranti + crescita significativa active tiles/workforce, ma massa ancora incompleta.

### FULL MASS DEPLOYMENT

Maggioranza delle run con indicativamente:

- 4 quadranti;
- forte active footprint;
- workforce circa ≥8 salvo diversa evidenza;
- livestock attivato.

---

# 33. Economic Decision Gate

Rimane:

| Mean Final Money | Verdict |
|---:|---|
| `< $50,000` | `FAIL` |
| `$50,000 – <$60,000` | `MINIMUM SUCCESS` |
| `$60,000 – <$70,000` | `COMPETITIVE` |
| `$70,000 – <$75,000` | `NEAR TOP BENCHMARK` |
| `≥ $75,000` | `TARGET ACHIEVED` |
| `> $75,000` | `BENCHMARK EXCEEDED` |

Riportare:

> **Land Regression Verdict + Architecture Verdict + Compounding Verdict + Economic Verdict**

---

# 34. Matrice diagnostica

Interpretare i risultati secondo questa matrice:

| Stato | Diagnosi |
|---|---|
| Q2 < E11-03 in modo forte | pre-Q2 protection rotta |
| Q2 preservato, Q3 crolla | Productive Window troppo aggressiva |
| Q2/Q3 preservati, active tiles ≤54 | Productive Activation Bottleneck |
| Land + active tiles crescono, workers ≤6 | Workforce Scaling Bottleneck |
| Land + crop + workers crescono, livestock OFF | Livestock Activation Bottleneck |
| Full Mass ma `<$50k` | Efficiency/Monetization Bottleneck |
| `≥$50k` | E11 architecture direction validated |
| `≥$75k` | Competitive target achieved |

---

# 35. Dominant Bottleneck

Identificare al termine un solo:

> **dominant bottleneck**

Possibili esiti:

- Q2 protection regression;
- Productive Window overspending;
- Q3 accumulation delay;
- high-value crop maturation;
- active tile activation;
- workforce;
- travel;
- livestock;
- feed;
- harvest capacity;
- market throughput;
- end-game conversion.

Non correggerlo nello stesso task.

---

# 36. Deliverable documentale

Creare:

`docs/versions/E11_05_staged_expansion_capital_release.md`

Struttura minima:

1. Executive Summary
2. E11-04 Failure
3. H11-05 Hypothesis
4. Controlled Change
5. Invariants Preserved
6. Economic State Machine
7. ACCUMULATE_Q2
8. PRODUCTIVE_WINDOW
9. ACCUMULATE_Q3
10. MASS_ACTIVATION
11. Productive Budget
12. Horizon-Aware Crop Spending
13. Configuration Delta
14. Tests
15. Benchmark Protocol
16. Economic Results
17. Land Regression Analysis
18. Q2 Analysis
19. Productive Window Analysis
20. Q3 Analysis
21. Productive Footprint
22. Crop Maturity & Revenue
23. Workforce Scaling
24. Livestock Activation
25. Trajectory
26. Compounding Test
27. Architecture Verdict
28. Economic Verdict
29. Dominant Bottleneck
30. Recommendation for E11-06

---

# 37. Aggiornamento documentazione

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato finale:

> **E11-05 BUILD + LOCAL VERIFY COMPLETED — awaiting supervisor review**

Non dichiarare E11 completato.

---

# 38. Git

Al termine:

```powershell
git status
git diff --stat
git diff --check
```

Non effettuare:

- commit finale;
- tag;
- push;
- submission Kaggle.

---

# Deliverable finale

Al termine fermarsi e riportare:

1. **E11-05 BUILD status**
2. **state machine implementata**
3. **parametri Productive Window**
4. **invarianti preservate**
5. **test result**
6. **Mean Final Money**
7. **Median / Std / Min / Max**
8. **delta vs E10-01**
9. **delta vs E11-03**
10. **delta vs E11-04**
11. **paired wins**
12. **Q2 unlock rate/timing**
13. **Q3 unlock rate/timing**
14. **Land Regression Verdict**
15. **mean/peak quadrants**
16. **peak active tiles**
17. **peak workforce**
18. **Productive Window seed spending**
19. **high-value crop planting**
20. **high-value crop maturity**
21. **crop revenue**
22. **livestock activation**
23. **trajectory 25/50/75/100**
24. **Compounding Verdict**
25. **Architecture Deployment Verdict**
26. **Economic Decision Gate**
27. **dominant bottleneck**
28. **file creati/modificati**
29. **proposta E11-06**

## Regola finale

Se Q2 regredisce:

> **ripristinare successivamente la protezione pre-Q2 senza modificare altri sottosistemi.**

Se Q2 è preservato ma Q3 regredisce:

> **ridurre o riprogettare esclusivamente la Productive Window.**

Se Q2/Q3 sono preservati ma active tiles non superano E11-03:

> **il nuovo bottleneck è Productive Activation.**

Se land + crop engine funzionano ma workforce rimane ≤6:

> **la successiva iterazione deve concentrarsi sulla workforce.**

Se land + crop + workforce funzionano ma livestock resta OFF:

> **la successiva iterazione deve concentrarsi sul livestock.**

Se viene raggiunto **FULL MASS DEPLOYMENT**, valutare finalmente in modo pieno il risultato economico rispetto a `$50k/$75k`.

**Non modificare workforce, livestock, locality o end-game in E11-05. Fermarsi dopo BUILD + LOCAL VERIFY e attendere approvazione.**