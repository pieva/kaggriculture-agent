# E11-04 — BUILD + VERIFY — Seed–Expansion Synchronization

## Contesto

Le prime tre iterazioni di **E11 — 3× Productive Mass Expansion** hanno progressivamente isolato i colli di bottiglia che impedivano il passaggio dalla scala E10 alla massa produttiva osservata nei top player.

Il riferimento strategico rimane:

- **E10 baseline:** circa `$23k Mean Final Money`
- **Minimum Success Threshold E11:** `$50,000`
- **Competitive Target E11:** `$75,000`

Il principio generale rimane:

> **Mass first, efficiency second.**

---

# 1. Evidenze acquisite da E11-01 → E11-03

## E11-01 — Productive Mass Baseline

L'architettura E11 non riusciva a espandersi oltre:

- 2 quadranti;
- 50 tile;
- 4 worker;
- livestock OFF.

Diagnosi:

> **Expansion Cash Lock**

Il capitale destinabile all'espansione veniva assorbito dalla produzione corrente prima di poter finanziare Q2/Q3.

---

## E11-02 — Expansion Capital Protection

È stata introdotta una protezione esplicita del capitale destinato al prossimo `BUY_LAND`.

Risultato:

- Q2 Unlock Rate: `0%`
- Q3 Unlock Rate: `0%`
- Mean Final Money: `$15,682.50`

La disponibilità finanziaria per l'espansione veniva raggiunta, ma il gate:

`active_tiles >= 15`

impediva comunque Q2.

Diagnosi:

> **Active Tile Gate Lock / Seed Starvation Deadlock**

---

## E11-03 — Expansion Gate Unlock

È stata modificata esclusivamente la readiness territoriale introducendo:

> `expansion_gate_mode = "MIN_OPERATIONAL"`

con Minimum Operational Readiness:

- Q1: `active_tiles >= 6`
- Q2: `active_tiles >= 8`
- Q3: `active_tiles >= 12`

mantenendo invariata la Expansion Capital Protection.

### Risultati E11-03

- **Mean Final Money:** `$7,193.77`
- **Q2 Unlock Rate:** `83.3%`
- **Q2 Mean Unlock:** Day `5.4`
- **Q3 Unlock Rate:** `60.0%`
- **Q3 Mean Unlock:** Day `11.2`
- **Peak owned:** 4 quadranti / 100 tile
- **Mean peak quadrants:** `3.43`
- **Peak active productive tiles:** `54`
- **Peak workforce:** `6`
- **Livestock Activation Rate:** `0%`

### Conclusione acquisita

> **Il Land Expansion Bottleneck è stato risolto.**

E11-03 dimostra che ProductiveMassROIAgent può effettivamente trasformare il capitale protetto in espansione territoriale.

Non tornare quindi alla precedente logica di saturazione.

---

# 2. Nuovo bottleneck dominante

E11-03 ha però evidenziato un nuovo collo di bottiglia:

> **Seed–Expansion Misalignment / Productive Starvation**

La protezione del capitale è troppo binaria.

Durante l'accumulo per Q2/Q3:

- gli acquisti di Melon/Strawberry e altri investimenti colturali costosi vengono bloccati;
- l'agente riesce ad acquistare terreno;
- ma non costruisce abbastanza produzione ad alto rendimento prima dell'espansione;
- dopo Q2/Q3 rimane poco tempo per completare i cicli colturali più lunghi;
- la nuova capacità territoriale non genera abbastanza revenue entro la fine dell'episodio.

La sequenza osservata è:

```text
Expansion Capital Protection
        ↓
High-yield crop spending blocked
        ↓
Q2/Q3 successfully purchased
        ↓
Large productive capacity becomes available
        ↓
Insufficient mature high-value production
        ↓
Land investment does not pay back in time
        ↓
Final Money collapses
```

E11-04 deve intervenire esclusivamente su questo problema.

---

# 3. Obiettivo E11-04

Procedere con:

> **E11-04 — Seed–Expansion Synchronization**

Domanda sperimentale:

> **Possiamo mantenere il land expansion ottenuto in E11-03 permettendo contemporaneamente investimenti colturali economicamente compatibili con il prossimo expansion unlock e con il remaining productive horizon?**

E11-04 deve verificare se:

> **protected expansion capital + productive crop investment**

possono convivere senza ricreare l'Expansion Cash Lock di E11-01.

---

# 4. Ipotesi E11-04

Formalizzare:

> **H11-04 — Seed–Expansion Synchronization Hypothesis:** la protezione binaria degli investimenti colturali durante l'accumulo per Q2/Q3 produce starvation produttiva. Una protezione dinamica, che consenta investimenti colturali quando questi non compromettono materialmente il prossimo land unlock e possono maturare entro l'orizzonte disponibile, dovrebbe mantenere l'espansione territoriale e aumentare significativamente la capacità di revenue.

L'obiettivo NON è semplicemente:

> comprare più Melon/Strawberry.

L'obiettivo è:

> **sincronizzare ciclo di investimento territoriale e ciclo di investimento colturale.**

---

# 5. Esperimento controllato

E11-04 deve modificare una sola componente rispetto a E11-03:

> **crop spending policy durante Expansion Capital Protection**

Mantenere invariati:

- Expansion Gate `MIN_OPERATIONAL`;
- Q1/Q2/Q3 readiness;
- land cost;
- operating reserve;
- workforce scaling;
- worker locality;
- livestock logic;
- target livestock;
- action hierarchy;
- end-game logic;
- benchmark protocol.

Non effettuare tuning simultaneo degli altri sottosistemi.

---

# 6. Non utilizzare una soglia arbitraria `$600`

NON implementare semplicemente:

```text
if cash >= 600:
    allow_high_value_seeds
```

La soglia `$600` non deriva dalle meccaniche economiche e rischierebbe di ricreare E11-01:

```text
cash
 ↓
high-value seeds
 ↓
cash below land threshold
 ↓
Q2/Q3 blocked again
```

La decisione deve invece essere collegata allo stato economico reale.

---

# 7. Dynamic Expansion Capital Protection

Trasformare la protezione binaria E11-02/E11-03 in una protezione dinamica.

Concettualmente distinguere:

```text
CURRENT CASH
    │
    ├── Operating Reserve
    │
    ├── Expansion Requirement
    │
    └── Productive Investment Capacity
```

La policy deve valutare quanto capitale può essere investito in crop **senza compromettere materialmente il prossimo land unlock**.

---

# 8. Expansion Funding Gap

Introdurre, se utile, un concetto esplicito di:

```text
expansion_funding_gap
```

concettualmente:

```text
expansion_funding_gap =
    max(
        0,
        next_land_required_capital
        - capital_effectively_available_for_expansion
    )
```

La definizione concreta deve rispettare l'architettura reale.

Non duplicare operating reserve o altri buffer.

L'obiettivo è sapere:

> **quanto manca realmente al prossimo BUY_LAND?**

---

# 9. Productive Investment Capacity

Calcolare una capacità indicativa di investimento produttivo:

```text
productive_investment_capacity
```

che rappresenti il capitale spendibile in crop senza compromettere:

1. operating reserve;
2. next land purchase;
3. produzione minima corrente.

Non è obbligatorio utilizzare esattamente questa formula o questo nome.

Preferire la soluzione più semplice compatibile con il codice.

---

# 10. Horizon-Aware Crop Investment

Ogni acquisto di seed deve considerare il tempo residuo.

Per ogni crop verificare almeno:

- seed cost;
- growth duration;
- expected harvest timing;
- expected revenue;
- remaining horizon.

Non acquistare crop che non possono realisticamente:

> essere piantati → maturare → essere raccolti → essere monetizzati

entro la fine dell'episodio.

Riutilizzare le meccaniche reali dell'ambiente già verificate.

---

# 11. Expansion-Aware Crop Investment

Durante l'accumulo per il prossimo quadrante, un crop ad alto valore può essere acquistato solo se l'investimento non rende irrealistico il prossimo land unlock.

La decisione concettuale deve valutare:

```text
IF
    crop_can_mature_within_horizon
AND crop_investment_is_affordable
AND operating_reserve_remains_safe
AND next_land_unlock_remains_financially_plausible
THEN
    allow_crop_investment
```

Non richiedere necessariamente che tutti i `$1,000` del prossimo quadrante siano già fisicamente presenti prima di acquistare qualsiasi seed.

Questo era precisamente il problema di E11-03.

---

# 12. Considerare il ritorno produttivo

Quando possibile, distinguere gli investimenti colturali in base al loro ruolo economico.

## Liquidity crop

Producono ritorno rapidamente e possono aiutare a finanziare il prossimo quadrante.

## Growth crop

Assorbono più capitale ma producono maggiore revenue futura.

## Late-cycle crop

Possono essere convenienti soltanto se piantati abbastanza presto.

La policy deve poter riconoscere che:

> **un investimento produttivo può contribuire all'espansione invece di essere necessariamente in conflitto con essa.**

---

# 13. Evitare un ROI engine complesso

E11-04 NON deve trasformarsi in un nuovo esperimento di ottimizzazione matematica del crop portfolio.

Non implementare:

- solver;
- grid search;
- predictive optimization;
- parameter sweep;
- crop allocation optimizer complesso.

Serve una regola economica semplice, interpretabile e testabile.

---

# 14. Preservare il risultato territoriale E11-03

Questo è un criterio fondamentale.

E11-04 non deve ottenere più revenue tornando semplicemente alla scala E11-01.

La nuova policy deve cercare di preservare:

- Q2 Unlock Rate vicino o superiore a E11-03;
- Q3 Unlock Rate vicino o superiore a E11-03;
- crescita active tiles;
- workforce scaling.

Baseline architetturale E11-03:

- Q2 Unlock Rate: `83.3%`
- Q3 Unlock Rate: `60.0%`
- Peak active tiles: `54`
- Peak workforce: `6`
- Peak land: `100 tile`

---

# 15. Regression Gate territoriale

Definire esplicitamente un controllo di regressione.

## LAND REGRESSION

Se E11-04 produce un miglioramento economico ma:

- Q2 Unlock Rate crolla significativamente;
- Q3 torna quasi sempre bloccato;
- peak land torna prevalentemente a 50 tile;

allora:

> **la sincronizzazione è fallita perché ha ricreato l'Expansion Cash Lock.**

Non considerare sufficiente un aumento di Final Money ottenuto tornando alla vecchia scala.

---

# 16. Crop Maturity Telemetry

Aggiungere instrumentation specifica per capire se i nuovi investimenti produttivi stanno effettivamente maturando.

Registrare almeno per crop:

- seed purchases;
- seed spending;
- tiles planted;
- planting timing;
- harvest count;
- harvested units;
- revenue generated;
- crops planted but not matured by episode end, se ricostruibile.

In particolare tracciare:

- Carrot;
- Wheat;
- Tomato;
- Strawberry;
- Melon.

---

# 17. Expansion vs Crop Spending

Registrare almeno per checkpoint:

- cash;
- protected/required expansion capital;
- seed spending cumulative;
- land spending cumulative;
- next quadrant;
- expansion funding gap;
- active tiles.

Questo deve permettere di rispondere:

> **quanto capitale è stato investito in produzione mentre si accumulava per il prossimo quadrante?**

e:

> **questo investimento ha ritardato Q2/Q3 oppure ne ha accelerato indirettamente il finanziamento?**

---

# 18. Configurazione E11-04

Creare una configurazione distinta e riproducibile, per esempio:

`E11_04_CONFIG`

oppure equivalente coerente con il repository.

La configurazione deve ereditare E11-03 e modificare esclusivamente la modalità di crop spending durante expansion protection.

Possibili parametri, solo se necessari:

```text
expansion_crop_policy = "SYNCHRONIZED"
horizon_aware_seed_buying = True
expansion_funding_gap_enabled = True
```

Non introdurre una proliferazione di soglie.

---

# 19. Invarianti obbligatorie

Documentare esplicitamente che restano invariati rispetto a E11-03:

### Land

- `expansion_gate_mode = MIN_OPERATIONAL`
- readiness Q1/Q2/Q3
- land cost
- expansion operating buffer

### Workforce

- hiring model
- worker ratio
- max workers
- locality

### Livestock

- activation rules
- target Cow
- target Sheep
- feed logic

### Scheduling

- 5-tier hierarchy

### End-game

- existing horizon/cutoff logic

Qualsiasi deviazione tecnica necessaria deve essere documentata.

---

# 20. Test specifici E11-04

Estendere la suite.

Testare almeno:

1. E11-03 rimane riproducibile.
2. Expansion Gate `MIN_OPERATIONAL` invariato.
3. seed high-value può essere acquistato quando economicamente compatibile.
4. seed high-value rimane bloccato quando comprometterebbe il prossimo land unlock.
5. operating reserve sempre rispettata.
6. crop non acquistato se non può maturare entro l'orizzonte.
7. liquidity crop ancora utilizzabile durante expansion.
8. Expansion Capital Protection non completamente disabilitata.
9. Q2 può ancora essere acquistato.
10. Q3 può ancora essere acquistato.
11. workforce logic invariata.
12. livestock logic invariata.
13. action legality.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

Tutti i test devono passare.

---

# 21. Benchmark locale

Eseguire il benchmark paired standard da **30 episodi** sugli stessi seed.

Confrontare almeno:

- E10-01
- E11-01
- E11-02
- E11-03
- E11-04

Non cambiare protocollo.

Registrare:

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
- paired wins vs E11-03;
- delta assoluto;
- delta percentuale;
- ratio.

---

# 22. Metriche architetturali

Registrare:

## Land

- Q2 Unlock Rate
- Q2 Mean Unlock Timing
- Q3 Unlock Rate
- Q3 Mean Unlock Timing
- mean/peak quadrants
- peak owned tiles

## Productive Footprint

- active tiles ai checkpoint
- peak active tiles
- idle owned tiles
- utilization ratio

## Workforce

- workers ai checkpoint
- peak workforce
- first post-expansion hire timing

## Livestock

- activation rate
- Cow count
- Sheep count
- first activation timing

---

# 23. Metriche colturali

Per E11-04 sono obbligatorie almeno:

- seed spending per crop;
- planted tiles per crop;
- harvest count per crop;
- revenue per crop;
- high-value crops matured;
- high-value crops unfinished at episode end;
- first Melon planting;
- first Melon harvest;
- first Strawberry planting;
- first Strawberry harvest;
- Tomato utilization, se presente.

Non limitarsi a dichiarare che il crop è stato utilizzato.

Misurare se ha realmente generato revenue.

---

# 24. Trajectory Analysis

Confrontare:

- E10-01
- E11-01
- E11-03
- E11-04

ai checkpoint:

- 25%
- 50%
- 75%
- 100%.

Registrare almeno:

| Metric | 25% | 50% | 75% | 100% |
|---|---:|---:|---:|---:|
| Money | | | | |
| Quadrants | | | | |
| Active tiles | | | | |
| Workforce | | | | |
| Livestock | | | | |
| Cumulative seed spending | | | | |
| Cumulative crop revenue | | | | |

La domanda principale è:

> **E11-04 mostra finalmente una curva di revenue che accelera dopo l'espansione?**

---

# 25. Compounding Test

Valutare esplicitamente:

> **LAND → PRODUCTION → REVENUE → REINVESTMENT**

Non considerare sufficiente:

> LAND → MORE LAND.

Cercare evidenza che:

1. Q2/Q3 vengono acquistati;
2. le nuove tile vengono attivate;
3. i crop maturano;
4. la revenue cresce;
5. la revenue finanzia ulteriore workforce/livestock/produzione.

Classificare il compounding come:

- `NOT OBSERVED`
- `WEAK`
- `PARTIAL`
- `STRONG`

motivando quantitativamente il verdetto.

---

# 26. Architecture Deployment Verdict

Utilizzare la scala già definita.

## ARCHITECTURE NOT DEPLOYED

Q2 non viene raggiunto stabilmente.

## PARTIAL LAND DEPLOYMENT

Q2 sì, Q3 no.

## FULL LAND DEPLOYMENT

4 quadranti raggiunti ma downstream produttivo ancora debole.

## PARTIAL MASS DEPLOYMENT

4 quadranti + crescita significativa di active tiles/workforce, ma livestock o altri sottosistemi rimangono bloccati.

## FULL MASS DEPLOYMENT

Maggioranza delle run con indicativamente:

- 4 quadranti / 100 tile;
- forte active footprint;
- workforce circa ≥8, salvo evidenza che meno sia sufficiente;
- livestock attivato.

---

# 27. Economic Decision Gate

Rimane invariato:

| Mean Final Money | Verdict |
|---:|---|
| `< $50,000` | `FAIL` |
| `$50,000 – <$60,000` | `MINIMUM SUCCESS` |
| `$60,000 – <$70,000` | `COMPETITIVE` |
| `$70,000 – <$75,000` | `NEAR TOP BENCHMARK` |
| `≥ $75,000` | `TARGET ACHIEVED` |
| `> $75,000` | `BENCHMARK EXCEEDED` |

Riportare sempre:

> **Architecture Verdict + Economic Verdict + Compounding Verdict**

Esempio:

`PARTIAL MASS DEPLOYMENT + FAIL + PARTIAL COMPOUNDING`

---

# 28. Interpretazione dei possibili risultati

## Caso A — Land regression

E11-04 aumenta revenue ma Q2/Q3 tornano bloccati.

Diagnosi:

> crop spending troppo aggressivo; Expansion Cash Lock reintrodotto.

---

## Caso B — Land preserved, revenue still low

Q2/Q3 rimangono sbloccati, high-value crop maturano, ma Final Money resta basso.

Diagnosi:

> il nuovo bottleneck è downstream; identificare workforce, utilization, crop economics o altro.

---

## Caso C — Land + crop engine funzionano, workforce ≤6

Diagnosi:

> Workforce Scaling Bottleneck.

---

## Caso D — Land + crop + workforce funzionano, livestock OFF

Diagnosi:

> Livestock Activation Bottleneck.

---

## Caso E — Full Mass Deployment, `<$50k`

L'ipotesi Productive Mass è finalmente testata integralmente ma non produce ancora output sufficiente.

Identificare il principale problema di efficienza/output.

---

## Caso F — `≥$50k`

> **E11 architecture direction validated.**

Procedere successivamente verso `$75k`.

---

## Caso G — `≥$75k`

> **Competitive Target achieved.**

La fase successiva può passare da mass expansion a efficiency optimization.

---

# 29. Dominant Bottleneck

Al termine identificare un solo:

> **dominant bottleneck**

oppure dichiarare che non è distinguibile.

Possibili nuovi bottleneck:

- crop spending still too restrictive;
- expansion regression;
- active-tile activation;
- workforce scaling;
- worker travel;
- livestock activation;
- feed supply;
- crop scheduling;
- harvest capacity;
- market throughput;
- idle capital;
- end-game conversion.

Non correggerlo nello stesso task.

---

# 30. Deliverable documentale

Creare:

`docs/versions/E11_04_seed_expansion_synchronization.md`

Struttura minima:

1. Executive Summary
2. E11-03 Findings
3. H11-04 Hypothesis
4. Controlled Change
5. Invariants Preserved
6. Dynamic Expansion Capital Protection
7. Expansion Funding Gap
8. Horizon-Aware Crop Investment
9. Expansion-Aware Crop Investment
10. Configuration Delta
11. Tests
12. Benchmark Protocol
13. Economic Results
14. Land Regression Check
15. Q2/Q3 Analysis
16. Productive Footprint
17. Crop Spending Analysis
18. Crop Maturity & Revenue
19. Workforce Scaling
20. Livestock Activation
21. Trajectory Analysis
22. Compounding Test
23. Architecture Deployment Verdict
24. Economic Decision Gate
25. Dominant Bottleneck
26. Recommendation for E11-05

---

# 31. Aggiornamento stato progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Registrare:

> **E11-04 BUILD + LOCAL VERIFY COMPLETED — awaiting supervisor review**

Non dichiarare E11 completato.

---

# 32. Git

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
- Kaggle submission.

---

# Deliverable finale

Al termine fermarsi e riportare:

1. **E11-04 BUILD status**
2. **controlled change**
3. **dynamic seed/expansion logic implementata**
4. **invarianti E11-03 preservate**
5. **test result**
6. **Mean Final Money**
7. **Median / Std / Min / Max**
8. **delta vs E10-01**
9. **delta vs E11-01**
10. **delta vs E11-03**
11. **paired wins**
12. **Q2 unlock rate/timing**
13. **Q3 unlock rate/timing**
14. **land regression verdict**
15. **peak active tiles**
16. **peak workforce**
17. **crop portfolio effettivo**
18. **seed spending per crop**
19. **revenue per crop**
20. **Melon/Strawberry maturity**
21. **livestock activation**
22. **trajectory 25/50/75/100**
23. **Compounding Verdict**
24. **Architecture Deployment Verdict**
25. **Economic Decision Gate**
26. **dominant bottleneck**
27. **file creati/modificati**
28. **proposta E11-05**

## Regola finale

Se E11-04 migliora economicamente ma perde Q2/Q3:

> **considerare fallita la sincronizzazione e non accettare il miglioramento come progresso E11.**

Se preserva il land deployment ma non aumenta la produzione:

> **identificare il successivo collo di bottiglia downstream.**

Se land, crop engine e active footprint crescono ma workforce rimane insufficiente:

> **E11-05 dovrà concentrarsi sulla workforce.**

Se land + crop + workforce funzionano ma livestock resta OFF:

> **E11-05 dovrà concentrarsi sull'attivazione del livestock.**

Se viene raggiunto **FULL MASS DEPLOYMENT**, valutare finalmente E11 come architettura completa rispetto a `$50k/$75k`.

**Non modificare workforce, livestock, locality o end-game in E11-04. Fermarsi dopo BUILD + LOCAL VERIFY e attendere approvazione.**