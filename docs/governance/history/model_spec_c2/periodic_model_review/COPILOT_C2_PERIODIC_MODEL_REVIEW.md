# COPILOT C2 â€” PERIODIC MODEL REVIEW
## Da soglie reattive a piano biologico e scala di servizio

```text
AGENT_ID: COPILOT
REVIEW_PHASE: C2 PERIODIC MODEL REVIEW
STATUS: COMPLETE â€” PERIODIC EVOLUTION RECOMMENDED
EVIDENCE_BASE: 4 Kaggle Benchmark Replays (103484828, 103473619, 103462357, 103464592)
MODEL_SPEC_STATUS: FROZEN FOR REVIEW ONLY â€” NO BUILD, NO TOURNAMENT, NO CODE CHANGE
```

---

## 1. Executive Summary & Verdetto

L'evidenza comparativa sui replay benchmark indica che il modello corrente di Copilot, anche nella sua performance iteration, resta troppo vicino a una logica `threshold-centric / reactive` e non sufficientemente `period-centric / plan-driven`.

Il punto non Ã¨ semplicemente â€œpiÃ¹ soglieâ€ o â€œpiÃ¹ acquaâ€ ma la struttura del controllo: i top performer non costruiscono un agente che decide solo quando il valore supera una soglia, ma un agente che opera su una pianificazione biologica e di servizio stabile, con reazione limitata a prezzi, inventario, cash e deviazioni eccezionali.

Le evidenze raccolte confermano che:

1. Una parte dominante della performance viene dal ciclo periodico: `PLAN = biological cycles + service schedule + workforce cadence + harvest deadlines + expansion cadence`.
2. Il modello reattivo sembra sopravvivere solo come override del piano, non come sostituto del piano.
3. La performance di LuCcc su un solo quadrante mostra che una scala produttiva correttamente sincronizzata puÃ² offrire rendimento forte senza bisogno di espansione aggressiva.
4. I replay a 3Q/4Q mostrano che l'espansione funziona quando replica un modulo produttivo giÃ  stabile, non quando si usa `BUY_LAND` come risposta immediata a una soglia.

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
```

---

## A. Evidenza osservata

### A.1 Quadro comparativo generale

| Replay | Score | Quadranti | Workforce | Architettura dominante | Evidenza periodica principale |
|---|---:|---:|---:|---|---|
| `103484828` LuCcc | $56.772 | 1 | 6 fisse | 6 pasture + 18 crop tile, alta densitÃ  | Feeds/care giornalieri fissi, onde di semina e raccolta sincronizzate |
| `103473619` Gordeev | $88.648 | 3 | 12 | 11 pasture + crop mix + espansione controllata | Wheat continuo e breeding schedule, scaling a 3Q |
| `103462357` Dipin | $95.496 | 3 | 12 | 12 pasture + crop mix + milk/wool/fertilizer | 243 SELL distribuiti, semina + servizio molto regolari |
| `103464592` Petar | $95.475 | 4 | 12â€“18 | 22 pasture + wheat + wool/fertilizer | Sheep + wheat a calendario stabile, forte cash flow giornaliero |
| Copilot C2 corrente | non benchmarkato in questa fase | 1-2Q tipico | limitato / capacitÃ  frame | ancora sovente threshold-driven | assenza di un calendario biologico esplicito |

### A.2 LuCcc (`103484828`) â€” score $56.772, 1 quadrante

- Architettura produttiva:
  - 1 quadrante compattato (NW), nessuna espansione.
  - Layout densissimo: 6 pasture adiacenti e 18 crop tile.
  - Pasture: 3 Cow + 3 Sheep stabilizzati a partire da Day 7.
- PeriodicitÃ  osservata:
  - `FEED` e `CARE`: 6 ciascuno ogni giorno.
  - `WATER`: circa 19 al giorno in piatti stabili.
  - `PLANT`: 45 total, ma distribuiti su onde di semina (`Day 7`, `9`, `19`, `24`), mai come burst unico.
  - `HARVEST`: regolare e ad alta maturitÃ , senza cursor disordinati.
  - `SELL`: profilo di vendita distribuito, non solo a fine partita.
- Monitora il cluster andato oltre una soglia? No. La performance deriva da un servizio continuativo e da una densitÃ  produttiva molto buona mantenuta su un singolo quadrante.
- Anomalie:
  - Nessun `BUY_LAND`.
  - Non Ã¨ un modello â€œanti-espansioneâ€; Ã¨ un modello â€œservizio ottimizzato dentro un modulo chiusoâ€.
- Interpretazione:
  - Il rendimento di LuCcc non va spiegato con una formula â€œpiÃ¹ terra = piÃ¹ soldiâ€, ma con `serviceability + synchrony + biological window`.

### A.3 Gordeev (`103473619`) â€” score $88.648, 3 quadranti

- Architettura produttiva:
  - 3 quadranti espansi in modo progressivo (`Day 0-10`), ma con piano chiaro.
  - Workforce: 12 hires costanti dalle prime giornate.
  - Pasture: 11 tile, principalmente Cow + Sheep.
- PeriodicitÃ  osservata:
  - WHEAT in onda continua, ristretto in piccoli lotti (3-10 / giorno) per dare feed e manutenzione senza picchi disarticolati.
  - `WATER` e `CARE` sono regolari, con valori giornalieri coerenti.
  - `HARVEST` e `SELL` effettuati in modo distribuito, non solo in gruppi a fine giorno.
- Anomalie:
  - Espansione non casuale: il modulo produttivo viene replicato una volta pronto.
- Interpretazione:
  - L'espansione Ã¨ globata come `replica controllata di capacitÃ `, non come semplice `BUY_LAND` ad hoc.

### A.4 Dipin (`103462357`) â€” score $95.496, 3 quadranti

- Architettura produttiva:
  - 3 quadranti, 12 pasture, 164 `PLANT` totali, 337 hires, 243 `SELL`.
  - Livestock: 96 Sheep, 192 Cow in stabilizzazione finale.
- PeriodicitÃ  osservata:
  - `WATER`: tra 37 e 53 al giorno a regime.
  - `FEED`: 11-12 al giorno, `CARE`: 11-12 al giorno.
  - `HARVEST`: 20-26 al giorno in regimi costanti, con fertilizzazione costante e daily monetization.
  - Vendite distribuite nel tempo â€” non un lauto blocco finale.
- Anomalie:
  - Nessun segno di â€œproduttivitÃ  si spacca alla fineâ€; il sistema resta coerente fino alla chiusura.
- Interpretazione:
  - La performance arriva da un calibro metrico: ogni famiglia di azioni Ã¨ in un tempo nominale, con servizio e raccolta periodici.

### A.5 Petar (`103464592`) â€” score $95.475, 4 quadranti

- Architettura produttiva:
  - 4 quadranti, 22 pasture, prevalenza di Sheep (528 a fine partita).
  - Crop base: WHEAT continuativo, con una piccola quantitÃ  di MELON e STRAWBERRY.
- PeriodicitÃ  osservata:
  - `FEED`: quasi costante, insieme a `CARE` e `WATER` di servizio.
  - `SELL`: molte vendite di `WOOL`, `FERTILIZER` e `WHEAT`, messe in forma di cadenza giornaliera/programmata.
- Anomalie:
  - Non c'Ã¨ un â€œprimo burst miracolosoâ€: la liquiditÃ  Ã¨ costruita per via di un ciclo di bestiame + colture altamente coordinato.
- Interpretazione:
  - L'hardware di servizio e la periodicitÃ  sono piÃ¹ importanti della singola commodity.

### A.6 Pattern comune alle top policy benchmark

Tutti i replay ad alto score condividono un pattern ricorrente:

```text
stable service cadence
+ crop wave staggering
+ fixed workforce in periodic blocks
+ planned harvest windows
+ sale inventory on cadence
+ expansion as replication of a working module
```

Questo contrasta con un agente che si basa su:

```text
empty-slot reaction
+ opportunistic harvest
+ cash threshold spikes
+ ad hoc replant on need
+ expansion when some quota crosses a threshold
```

---

## B. Diagnosi del modello corrente

### B.1 Cosa oggi Ã¨ threshold-centric

Nel modello corrente di Copilot le decisioni ancora sono fortemente attivate da soglie e condizioni locali:

- `if empty tile and seed available -> PLANT`
- `if money >= X -> buy seed`
- `if harvest_ready -> HARVEST`
- `if unwatered -> WATER`
- `if no capacity -> PASS`
- `if land target not yet reached -> expand / route`
- `if cash reserve below threshold -> sell`

Queste regole sono corrette in sÃ©, ma rimangono decise in modo `event-driven`, non `calendar-driven`.

### B.2 Cosa appare giÃ  periodico

Non tutto Ã¨ threshold-only. Nel modello C2 esistono giÃ  elementi plausibili di plan:

- il `harvest_ready` Ã¨ una gate semantica; questo Ã¨ un passo necessario verso il calendario biologico;
- `WATER` su plant non irrigate Ã¨ una manutenzione periodica;
- `replant`/`recovery` Ã¨ stato definito come importante;
- il working set e la workforce target sono una base di schedulazione.

### B.3 Collisione tra soglie e cicli biologici

Il problema principale non Ã¨ che una soglia Ã¨ errata; Ã¨ che la soglia sostituisce il calendario biologico. La collisione piÃ¹ evidente Ã¨:

```text
threshold = action trigger
calendar = biological requirement
```

Quando il calendario biologico si sposta, la soglia reagisce tardivamente. Esempi:

- un tile maturo non viene servito nella finestra corretta perchÃ© la policy Ã¨ in fase di â€œcheck di statoâ€ locale;
- la semina avviene su slot vuoti senza sobrietÃ  temporale; invece di un onda di plant stabilizzata;
- il bestiame/colture non sono collegati a un programma di servizio e di riciclo;
- la workforce Ã¨ considerata come capienza di cluster, non come risorsa per disciplina temporale.

### B.4 Inefficienze introdotte dal comportamento reattivo

Il comportamento reattivo si manifesta soprattutto in questi punti:

- `PLANT` su prioritÃ  locale invece di sequenza di calendario;
- `HARVEST` di sola validitÃ , senza finestra di raccolta stabile;
- `WATER` non necessariamente sincronizzato con il ciclo di crescita;
- `SELL` come uscita di cash senza piano di monetizzazione continua;
- `expansion` come risposta a carenza, non come replica del modulo raggiunto.

In altre parole: il modello corretta il ciclo, ma non ancora lo `progetta`.

---

## C. Proposta architetturale

### C.1 Classificazione dei meccanismi

```text
KEEP_AS_THRESHOLD
- cash floor emergency;
- hard-priority harvest gate;
- water emergency when near loss threshold;
- prices/demand override when a market opportunity is clearly superior.

CONVERT_TO_PERIOD
- crop planting cadence;
- harvest windows per crop;
- feed/care schedule for livestock;
- workforce allocation by planned service blocks;
- staggered replanting;
- water maintenance schedule.

HYBRID_PERIOD_PLUS_THRESHOLD
- expansion trigger;
- seed purchase order;
- fertilizer use / production windows;
- sell batching with cadence + price gate.

REMOVE
- ad hoc empty-slot planting without temporal grouping;
- one-off harvest attempts whenever some yield > 0;
- â€œbuy land when cash is highâ€ without serviceability proof.
```

### C.2 Separazione obbligatoria

```text
PLAN
= biological cycles
+ service schedule
+ workforce allocation
+ production calendar
+ harvest / collect deadlines
+ expansion schedule as replication of a stable module

REACT
= market prices
+ inventory / demand
+ cash constraints
+ exceptional deviations from plan
+ opportunistic monetization windows
```

Il design corretto per Copilot Ã¨ quindi:

```text
PLANNED_BASELINE + REACTIVE_OVERRIDE
```

non `soglia immediata` come default decision engine.

---

## D. Ipotesi causale

```text
HYPOTHESIS_ID: COPILOT_C2_H1
OBSERVED_PROBLEM: il modello C2 Ã¨ in gran parte guidato da condizioni locali e non da un calendario di servizio stabile.
EVIDENCE: LuCcc, Gordeev, Dipin e Petar mostrano routine giornaliere automatiche di FEED / CARE / WATER / HARVEST; il modello Copilot Ã¨ ancora troppo reattivo alle condizioni correnti.
CAUSAL_MECHANISM: senza un periodo nominale, la policy perde sincronizzazione tra crescita, service, vendita e espansione. Il risultato Ã¨ un throughput medio piÃ¹ basso e una capacitÃ  produttiva meno scalabile.
MODEL_CHANGE: introdurre `PLANNED_BASELINE` con periodi nominali per colture e animale, con scheduling di servizio giornaliero e ripiano di workforce.
EXPECTED_INTERMEDIATE_EFFECT: la policy impiega periodi regolari di irrigazione, feed, care, harvest e replant, con minore dispersione operativa.
EXPECTED_ECONOMIC_EFFECT: migliori hit rate di raccolta e maggiore stabilitÃ  del cash flow, con supporto al reinvestimento.
FALSIFICATION_CONDITION: se la policy continua a generare azioni soltanto in risposta a slot vuoti o cash trigger, senza un calendario osservabile di servizio, questa ipotesi Ã¨ falsa.
```

```text
HYPOTHESIS_ID: COPILOT_C2_H2
OBSERVED_PROBLEM: semina / replant non organizzata in onde biologiche.
EVIDENCE: i replay top performer usano staggered planting e scheduling per evitare picchi di servicio e di raccolta; l'architettura Copilot Ã¨ piÃ¹ diffusa in burst e in resequencing localmente attivato.
CAUSAL_MECHANISM: burst planting concentra l'onere di irrigazione, feeding, harvest e collection in un piccolo frame temporale; la capacity del worker diventa il collo di bottiglia e il servizio non scalabile.
MODEL_CHANGE: definire un plant wave per crop specifica, con replant separato dal ciclo di maturazione e dal servizio.
EXPECTED_INTERMEDIATE_EFFECT: ritmi di water, harvest e sell piÃ¹ regolari in piccole raffiche controllate.
EXPECTED_ECONOMIC_EFFECT: minore perdita di raccolto e maggior resa utile per tile / unitÃ  di lavoro.
FALSIFICATION_CONDITION: se la policy produce ancora semina in picchi non scaglionati senza una prova di serviceability, H2 Ã¨ falsa.
```

```text
HYPOTHESIS_ID: COPILOT_C2_H3
OBSERVED_PROBLEM: mancanza di un modulo periodico di bestiame + colture come motore di cash flow.
EVIDENCE: LuCcc e Dipin ottengono liquiditÃ  giornaliera stabile da Milk/Wool/Fertilizer; i replay ad alto score non costruiscono redditivitÃ  solo da crop.
CAUSAL_MECHANISM: il bestiame crea un flusso di cassa continuo, finanziando lavoro, semi e manutenzione. Senza questo, la policy dipende da vendite sporadiche o da un bootstrap poco robusto.
MODEL_CHANGE: includere un modulo animale periodico con feed/care/cycle calendar, senza imporre il bestiame come requisito inevitabile ma come opzione validata dal calendario.
EXPECTED_INTERMEDIATE_EFFECT: aumento della frequenza di MONETIZED_OUTPUT e minore dipendenza da eventi di mercato isolati.
EXPECTED_ECONOMIC_EFFECT: riduzione del rischio di cash crunch e maggiore capacitÃ  di crescita sostenuta.
FALSIFICATION_CONDITION: se la policy non ha una misurazione del ciclo di servizio del bestiame e del suo contributo monetario, H3 Ã¨ falsa.
```

```text
HYPOTHESIS_ID: COPILOT_C2_H4
OBSERVED_PROBLEM: espansione non rigorosamente asservita al modulo produttivo esistente.
EVIDENCE: i replay migliori espandono solo dopo aver costruito un modulo stabile; role e dimensione del servizio sono antecedenti all'espansione.
CAUSAL_MECHANISM: se l'espansione precede la capacitÃ  di servizio, si crea un sistema che spende terra e soldi senza sostenerne la manutenzione; il modello perde rendimento per tile, non guadagna.
MODEL_CHANGE: usare espansione come replica controllata di un modulo giÃ  stabile, con workforce e service margin vincolati.
EXPECTED_INTERMEDIATE_EFFECT: Q2/Q3 aggiuntivi restano produttivi e non drenano il ciclo esistente.
EXPECTED_ECONOMIC_EFFECT: miglior scaling del rendimento per quadrante e minore regressione di serviceability.
FALSIFICATION_CONDITION: se le nuove tile non aggiungono `ACTIVE_SURFACE` e `MONETIZED_OUTPUT` sostenuti, H4 Ã¨ falsa.
```

---

## E. Period model

### E.1 Crop period model

```text
ENTITY_PERIOD_MODEL
- crop: WHEAT
  - phase: seed -> growth -> water -> harvest -> replant
  - nominal_period: short cycle, with tight watering discipline
  - service_window: daily maintenance during active growth
  - hard_deadline: harvest immediately when maturity reached
  - expected_output: feed / cash / seed recapture
  - required_worker_capacity: low/moderate per tile, but high aggregate if many tiles are active
  - reactive_overrides: market sell timing, emergency seed refill

- crop: STRAWBERRY
  - phase: plant -> water -> maturity -> harvest -> replant
  - nominal_period: mid-cycle, high-value but service-heavy
  - service_window: periodic water and harvesting at maturity
  - hard_deadline: after maturity, no postponement; queue harvest
  - expected_output: midrange monetization
  - required_worker_capacity: moderate
  - reactive_overrides: price spikes, inventory sell opportunism

- crop: MELON
  - phase: plant -> water -> maturity -> harvest -> replant
  - nominal_period: high-value burst crop
  - service_window: concentrated but still scheduled
  - hard_deadline: harvest window at maturity; avoid overrun
  - expected_output: strong payout, often used as cash burst
  - required_worker_capacity: high if blocks are large
  - reactive_overrides: late market sell windows only after serviceability is assured
```

### E.2 Animal period model

```text
ENTITY_PERIOD_MODEL
- animal: SHEEP
  - phase: placement -> feed -> care -> product generation -> collect -> market
  - nominal_period: daily feed/care cadence; output on recurring intervals
  - service_window: fixed daily service block
  - hard_deadline: feed/care before product loss or service degradation
  - expected_output: wool + cash flow
  - required_worker_capacity: moderate and predictable
  - reactive_overrides: price opportunism / inventory flush

- animal: COW
  - phase: placement -> feed -> care -> milk generation -> collect -> sell
  - nominal_period: daily, with room for stable service and milk collection
  - service_window: daily fixed block
  - hard_deadline: feed/care on schedule; milk collected before backlog accumulates
  - expected_output: milk + cash flow + fertility/resilience
  - required_worker_capacity: moderate-to-high
  - reactive_overrides: market timing and sell batching
```

### E.3 Service periodicity that should be explicit in Copilot

```text
SERVICE_BLOCKS
- morning: seed/worker check + capacity review
- active day: water and care reminders, by crop/animal priorities
- harvest gate: mature tiles queue only; no opportunistic harvest before maturity
- market cycle: sell inventory on planned windows, not only on empty cash condition
- expansion gate: only after serviceability of current module is verified
```

---

## F. Espansione

L'espansione deve essere trattata come:

```text
Q1 productive cycle
-> replicated cycle on Q2
-> eventual Q3 / Q4 replication with service margin
```

non come semplice reddito da `BUY_LAND`.

### F.1 Principio di scala

Un modulo Q1 Ã¨ considerato valido quando:

- la zona produce un ciclo chiuso senza slot congestion;
- la workforce Ã¨ stabile e non costretta in overload;
- WATER / FEED / CARE sono dentro la capacitÃ  disponibile;
- `HARVEST` e `SELL` sono in una finestra di service non conflittuale.

Lo step successivo Ã¨ replicare il modulo con un fattore di sicurezza, non aumentare indefinitamente la superficie senza servizio.

### F.2 Analisi contro-intuitiva di LuCcc

LuCcc non dimostra che â€œpiÃ¹ grande Ã¨ peggioâ€ o che l'espansione sia inutile. Dimostra che:

- un modulo compattato molto ben servito Ã¨ giÃ  fortemente redditizio;
- l'espansione ha senso solo quando si replica un ciclo giÃ  stabilizzato;
- la scala va gestita con service capacity, non con `BUY_LAND` ad hoc.

---

## Verdetto di uscita

```text
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
```

La review non richiede ancora una build: richiede un cambiamento di architettura del MODEL_SPEC in direzione `PLAN + REACT`, con un calendario biologico e di servizio esplicito, e con l'espansione come replica controllata di capacitÃ  giÃ  validata. La fase successiva deve arrivare a un `MODEL_SPEC_REVISION` o a una `PLAN/BUILD` formale, ma non a una run o a una modifica di codice.

---

## Stato finale

```text
MODEL_SPEC_REVIEW_COMPLETE
NO_CODE_CHANGE
NO_TOURNAMENT_RUN
PERIODIC_MODEL_EVOLUTION_RECOMMENDED: YES
```
