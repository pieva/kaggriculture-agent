# E07-05 — BUILD Configurable Competitive Baseline

Stiamo lavorando al progetto **Kaggriculture Agent**.

Le fasi precedenti sono:

- `E07-01 — DEFINE Competitive Baseline Reconstruction`
- `E07-02 — VERIFY Competitive Evidence`
- `E07-03 — PLAN Configurable Competitive Baseline`
- `E07-04 — VERIFY Final Reward and Asset Liquidation`

La decisione approvata è:

> **GO FOR BUILD WITH END-GAME CORRECTIONS**

E07 deve ora implementare una **baseline competitiva configurabile di seconda generazione**, con capacità di scaling, produzione multi-componente e conversione degli asset in cash entro l'orizzonte finito dell'episodio.

Non assumere che i parametri quantitativi iniziali siano ottimali.

---

# 1. Obiettivo BUILD

Implementare un nuovo agente separato da E06, preservando integralmente la baseline precedente.

L'agente E07 deve supportare:

- phase-based strategy;
- capital allocation;
- land expansion;
- workforce scaling;
- multi-crop allocation;
- livestock;
- feed management;
- multi-worker task dispatching;
- market brokerage;
- end-game cutoffs;
- inventory liquidation;
- instrumentation diagnostica.

L'obiettivo del BUILD non è ancora dimostrare che E07 batta E06.

L'obiettivo è ottenere un agente:

1. integrato;
2. eseguibile;
3. configurabile;
4. osservabile;
5. capace di completare 720 step;
6. privo di errori strutturali evidenti.

---

# 2. Principio economico da preservare

Il reward finale verificato è:

```python
reward = float(farm["money"])
```

Quindi:

```text
productive capacity != final reward
```

La logica strategica deve rispettare il principio:

```text
cash
  ↓
productive investment
  ↓
production
  ↓
sellable products
  ↓
cash before episode end
```

Asset non liquidabili:

- cows;
- sheep;
- land;
- structures;
- crops non raccolte.

Questi asset devono quindi essere acquistati soltanto se hanno tempo sufficiente per ripagare il capitale investito.

---

# 3. Cutoff: capacità sì, valori rigidi no

Implementare il supporto a cutoff temporali per:

- livestock purchase;
- land expansion;
- crop planting;
- workforce hiring;
- structures;
- final inventory flush.

I valori iniziali possono derivare dal PLAN corretto, ma devono essere `OPEN / TUNABLE`.

Non trattare come verità economiche definitive:

- Cow cutoff = D20;
- Sheep cutoff = D18;
- Melon cutoff = D18;
- Stop all planting = D26;
- liquidation start = D27/D29.

Devono essere parametri configurabili.

---

# 4. Nuovo agente

Creare una nuova classe E07 separata.

Nome candidato:

```text
HybridLivestockClusterROIAgent
```

Se la struttura del repository suggerisce un nome più coerente, usarlo mantenendo chiaro il collegamento a E07.

Non modificare il comportamento delle classi E01–E06 salvo refactoring strettamente necessario e privo di regressioni.

---

# 5. Configurazione centralizzata

Implementare una configurazione esplicita.

Esempio orientativo:

```python
@dataclass(frozen=True)
class CompetitiveConfig:
    target_quadrants: int = 2
    target_workers: int = 4

    wheat_tiles: int = 6
    melon_tiles: int = 12
    carrot_tiles: int = 6

    target_cows: int = 4
    target_sheep: int = 2

    hire_days: tuple[int, ...] = (1, 6, 12)
    expansion_day: int = 12

    cash_reserve: float = 300.0
    feed_safety_buffer: int = 3

    cow_purchase_cutoff_day: int = 20
    sheep_purchase_cutoff_day: int = 18
    melon_plant_cutoff_day: int = 18
    all_plant_cutoff_day: int = 26
    inventory_flush_start_day: int = 27
```

Adattare tipi e nomi all'architettura reale.

Tutti questi valori devono essere modificabili senza riscrivere la policy.

---

# 6. Implementazione incrementale

Procedere per blocchi testabili.

## B1 — Config + telemetry foundation

Implementare:

- `CompetitiveConfig`;
- strutture telemetry;
- contatori episodio;
- event log sintetico.

Testare subito.

---

## B2 — Phase Manager

Implementare almeno:

```text
OPENING
SCALE
PRODUCE
LIQUIDATE
```

Registrare ogni cambio fase:

```text
step
day
hour
phase_from
phase_to
cash
```

Le transizioni devono poter usare:

- giorno;
- cash;
- land ownership;
- workforce;
- remaining steps.

---

## B3 — Capital Allocator

Implementare controlli per:

- cash reserve;
- seed budget;
- feed buffer;
- hiring;
- livestock;
- land.

Ogni investimento deve essere negato se:

```text
cash_after_action < cash_reserve
```

salvo eccezioni esplicitamente motivate.

Registrare ogni investimento con:

```text
step
category
amount
cash_before
cash_after
```

---

## B4 — Land Manager

Implementare:

- tile owned;
- tile productive;
- tile reserved;
- quadrants owned;
- `BUY_LAND`.

Non assumere che tutte le 50 tile diventino immediatamente produttive.

La prima espansione deve essere configurabile.

Registrare:

```text
BUY_LAND event
day
cash before
cash after
new owned tile count
productive tile count
```

---

## B5 — Workforce Manager

Implementare:

- target workers;
- hiring schedule;
- affordability;
- cutoff tardivo;
- eventi `HIRE`.

Il burst-hiring a `hour == 0` può essere usato come policy iniziale se compatibile con l'environment.

Registrare:

```text
hire day
worker count
cash cost
```

---

## B6 — Multi-Crop Manager

Supportare almeno:

- `WHEAT`;
- `MELON`;
- `CARROT`.

Separare ruoli:

```text
FEED
CASH
FLEX
```

Implementare allocazione deterministica e riproducibile.

Il numero di tile per crop deve dipendere dalla config.

Applicare crop cutoff configurabili.

---

## B7 — Livestock + Feed

Implementare:

- cows;
- sheep;
- purchase policy;
- pasture requirement;
- feeding;
- milk/wool production workflow;
- feed safety guard.

Prima di comprare un animale verificare almeno:

```text
cash
remaining time
feed availability
worker capacity
```

Non acquistare livestock oltre il cutoff configurato.

Registrare:

```text
animal purchased
animal fed
feed missed
milk/wool collected
```

---

## B8 — Task Dispatcher

Integrare i task di:

- WATER;
- FEED;
- HARVEST;
- PLANT;
- livestock collection;
- movement.

Partire dalla priorità candidata:

```text
WATER
FEED_ANIMALS
HARVEST
PLANT
```

ma correggerla se i test mostrano conflitti con le reali meccaniche dell'environment.

All'interno della stessa classe di priorità, riutilizzare Manhattan distance se compatibile.

Evitare:

- doppia assegnazione;
- collisioni;
- worker idle evitabile;
- task già completati.

---

## B9 — Market Broker

Centralizzare gli ordini `SELL`.

Gestire:

- inventory;
- max order limit;
- priorità prodotto;
- late-game flush.

Non assumere prezzi statici.

Qualsiasi soglia intermedia tipo:

```text
inventory > 70
```

deve essere configurabile e marcata come euristica, non come regola dell'environment.

---

## B10 — End-Game Manager

Implementare:

- stop investimenti tardivi;
- crop cutoff;
- livestock cutoff;
- inventory flush;
- riduzione del reinvestimento;
- priorità al cash realizzato.

Non tentare:

- `SELL_ANIMAL`;
- `SELL_LAND`;
- `SELL_STRUCTURE`.

Queste azioni non esistono.

---

# 7. Telemetria obbligatoria

La telemetria deve permettere di capire il comportamento di **un singolo episodio** prima del benchmark.

Registrare almeno:

## Event timeline

Eventi principali:

```text
PHASE_CHANGE
HIRE
BUY_LAND
BUY_ANIMAL
PLANT
HARVEST
SELL
FEED_MISS
INVENTORY_FLUSH
```

Per gli eventi strategici registrare:

```text
step
day
hour
cash
phase
```

---

## Economy

- starting money;
- minimum cash;
- final money;
- spending:
  - seeds;
  - workforce;
  - land;
  - livestock;
  - structures;
- realized revenue per product, quando ricostruibile.

---

## Land

- owned tiles;
- productive tiles;
- utilization ratio;
- expansion timing.

---

## Workforce

- peak workers;
- hires;
- idle steps;
- movement steps;
- productive actions.

---

## Crops

- planted;
- harvested;
- unharvested mature;
- immature at end;
- counts by crop.

---

## Livestock

- animals acquired;
- feed consumed;
- missed feed events;
- milk/wool collected.

---

## Inventory

- peak inventory;
- final inventory;
- sold quantities;
- unsold items at end.

---

# 8. Test richiesti durante BUILD

## Unit tests

Creare almeno test per:

- config defaults;
- phase transitions;
- cash reserve;
- land purchase guard;
- workforce hiring guard;
- crop allocation;
- crop cutoff;
- livestock cutoff;
- feed safety;
- market order limit;
- inventory flush.

---

## Behavioral tests

Creare scenari controllati per almeno:

1. cash insufficiente;
2. feed insufficiente;
3. fine episodio vicina;
4. inventory da liquidare;
5. tentativo di acquisto animale troppo tardi;
6. tentativo di piantare Melon oltre cutoff.

---

## Regression

Eseguire:

```powershell
.venv\Scripts\pytest tests/
```

Tutti i test precedenti E01–E06 devono restare verdi.

---

# 9. Smoke episode obbligatorio

Dopo l'integrazione, eseguire **un singolo episodio completo da 720 step**.

Usare un opponent già presente nel benchmark standard, preferibilmente `pass` per il primo controllo strutturale.

Non eseguire ancora il benchmark completo da 30 episodi.

Registrare:

- completion;
- disqualification;
- final money;
- fase raggiunta;
- quadranti acquistati;
- productive tiles;
- peak workers;
- cows/sheep acquistate;
- feed misses;
- inventory finale;
- crops immature finali;
- principali eventi economici.

---

# 10. Diagnosi dello smoke episode

Non limitarsi a riportare Final Money.

Produrre una timeline sintetica simile a:

```text
D1  OPENING   cash=...
    HIRE ...
    BUY_ANIMAL ...

D6  SCALE     cash=...
    HIRE ...

D12 SCALE     cash=...
    BUY_LAND ...

D16 PRODUCE   cash=...

D27 LIQUIDATE cash=...

D30 END       final_money=...
```

I giorni effettivi devono provenire dall'episodio reale.

---

# 11. Smoke acceptance criteria

Lo smoke episode è accettabile se:

- completa 720 step;
- nessuna disqualification;
- nessuna eccezione;
- le fasi vengono attivate;
- almeno alcune nuove capability E07 vengono realmente esercitate;
- telemetria completa;
- nessun comportamento palesemente incoerente.

Non richiedere ancora:

```text
E07 > E06
```

come condizione di BUILD.

---

# 12. Failure conditions

Fermarsi e diagnosticare se:

- cash negativo o blocco economico;
- espansione non avviene pur essendo prevista;
- compra land ma non la utilizza;
- livestock acquistato ma non alimentato;
- starvation significativa;
- worker largamente idle;
- market queue bloccata;
- inventory non liquidabile per bug;
- fase LIQUIDATE non attivata;
- episodio non completa;
- disqualification.

Correggere i bug strutturali prima dello smoke finale.

Non fare tuning prestazionale estensivo durante BUILD.

---

# 13. Deliverable

Creare:

`docs/versions/E07_build_competitive_baseline.md`

Il documento deve includere:

1. Implemented Architecture
2. Files Added / Modified
3. Configuration
4. Modules Implemented
5. Test Results
6. Regression Results
7. Smoke Episode
8. Smoke Timeline
9. Telemetry Summary
10. Structural Issues Found
11. Corrections Applied
12. Remaining Open Parameters
13. BUILD Decision

---

# 14. Aggiornamenti documentali

Aggiornare:

- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`.

Non dichiarare ancora:

- E07 validated;
- E07 shipped.

---

# 15. Git discipline

Al termine mostrare:

```powershell
git status --short
git diff --stat
```

Non creare tag.

Non inviare submission Kaggle.

Non fare `git push` salvo istruzione già prevista esplicitamente dal workflow corrente del progetto.

---

# 16. Decisione BUILD

Terminare con:

### GO FOR VERIFY

se:

- test verdi;
- regressioni verdi;
- smoke episode completo;
- telemetria sufficiente;
- nessun blocker strutturale.

### CONTINUE BUILD

se restano bug implementativi risolvibili.

### RETURN TO PLAN

se emerge un problema architetturale sostanziale.

---

# 17. STOP CONDITION

Al termine mostrare:

1. codice/moduli implementati;
2. test nuovi;
3. risultato completo `pytest`;
4. smoke episode 720 step;
5. Final Money dello smoke;
6. timeline strategica reale;
7. metriche diagnostiche principali;
8. problemi rilevati;
9. parametri ancora OPEN;
10. decisione BUILD.

**FERMARSI QUI.**

Non:

- eseguire benchmark 30 episodi;
- confrontare statisticamente E07 vs E06;
- creare submission;
- inviare a Kaggle;
- creare tag;
- dichiarare E07 validated;
- dichiarare E07 shipped.

Attendere la revisione prima della fase VERIFY.