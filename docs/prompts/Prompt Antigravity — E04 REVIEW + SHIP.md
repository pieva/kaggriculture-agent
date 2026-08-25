# E04 — REVIEW + SHIP

E04 (`NWClusterROIAgent`) ha completato BUILD e VERIFY.

Procedere ora con le fasi:

`REVIEW → SHIP`

L'esperimento deve essere consolidato **così come è stato eseguito**, mantenendo il risultato negativo come evidenza sperimentale.

Non modificare la strategia E04 per migliorarne le prestazioni.

---

## 1. Risultati da sottoporre a REVIEW

Baseline di controllo:

**E03 — `MultiTileROIAgent`**

- footprint: 4 tile, cluster 2×2;
- Mean Final Money: `$14682.47`;
- Completion Rate: `100%`;
- Disqualification Rate: `0%`;
- Water Starvation osservata: `0%`.

E04:

**`NWClusterROIAgent`**

- footprint: 9 tile, cluster compatto 3×3;
- singolo farmer;
- nessun `HIRE`;
- nessun `BUY_LAND`;
- formula ROI invariata rispetto a E03;
- horizon logic invariata;
- vendita immediata invariata;
- priorità operative `HARVEST > PLANT > WATER` invariata.

Risultati VERIFY E04:

- Total Episodes: `30`;
- Completion Rate: `100.00%`;
- Disqualification Rate: `0.00%`;
- Overall Win Rate: `100.00%`;
- Mean Final Money: `$11232.47 ± $661.26`;
- Median Final Money: `$11050.00`;
- delta Mean Final Money vs E03: `-$3450.00 (-23.49%)`;
- Total Weed Conversions: `238`;
- media Weed Conversions: `7.93 per episodio`;
- Unwatered End-of-Day Ratio: `3.33%`;
- Agent Mean Turn Latency: `0.0570 ms/turn`.

Target economico previsto dal PLAN:

`Mean Final Money >= $22,000`

Target non raggiunto.

---

# 2. Classificazione dell'esperimento

La REVIEW deve distinguere chiaramente tra:

### Experimental Integrity

Verificare che:

- sia stata modificata una sola variabile strategica;
- E03 costituisca un controllo valido;
- ROI, horizon, selling policy e worker count siano rimasti invariati;
- il benchmark sia stato completato correttamente;
- non siano state introdotte modifiche non previste.

### Operational Correctness

Verificare:

- Completion Rate;
- Disqualification Rate;
- correttezza della submission standalone;
- test suite;
- latenza.

### Economic Hypothesis

Classificare esplicitamente l'ipotesi E04 come:

**FALSIFIED**

se le evidenze confermano i risultati riportati.

Il mancato raggiungimento dell'obiettivo economico non deve essere interpretato come fallimento del processo sperimentale.

---

# 3. Correggere due possibili sovrainterpretazioni

Durante VERIFY sono state formulate alcune conclusioni che devono essere rese più rigorose nella documentazione finale.

## 3.1 Weed conversions

Il valore:

`238 / 30 = 7.93`

deve essere descritto come:

> **7.93 weed conversions per episodio**

Non descriverlo automaticamente come:

> 7.93 piante distinte su 9 morte per episodio

a meno che i dati registrati permettano di dimostrare che le conversioni corrispondano a tile distinte.

Se questa distinzione non è verificabile con i dati disponibili, dichiararlo esplicitamente.

Non eseguire nuovi esperimenti per risolvere questa incertezza.

---

## 3.2 Limite del single farmer

E04 supporta la conclusione:

> **La policy E03, estesa da 4 a 9 tile senza altre modifiche e mantenendo un singolo farmer, non è operativamente sostenibile.**

E04 **non dimostra** invece che:

> qualsiasi strategia single-farmer oltre 4 tile sia impossibile.

Non trasformare quindi il risultato E04 in un limite universale del tipo:

`single farmer capacity = 4 tile`

oppure:

`HIRE è necessariamente richiesto oltre 4 tile`.

Le evidenze permettono di affermare l'esistenza di un **capacity / scheduling bottleneck**, ma non ne identificano ancora univocamente la soluzione.

---

# 4. Interpretazione del capacity bottleneck

Analizzare il risultato senza modificare E04.

Considerare come spiegazioni concorrenti almeno:

### A — Footprint troppo grande

Il salto diretto:

`4 → 9`

potrebbe aver superato il limite gestibile dalla policy corrente, mentre footprint intermedi potrebbero essere sostenibili.

### B — Scheduling / Priority Bottleneck

La policy:

`HARVEST > PLANT > WATER`

potrebbe non essere adeguata quando il footprint aumenta.

Harvest e planting possono sottrarre turni all'irrigazione, causando starvation anche se un semplice conteggio statico di:

`WATER + movement < 24`

sembrava suggerire capacità sufficiente.

### C — Worker Capacity Bottleneck

Un singolo farmer potrebbe effettivamente non disporre di sufficiente capacità operativa per gestire 9 tile.

In questo caso `HIRE` diventerebbe una candidata naturale per una successiva iterazione.

Non scegliere ancora tra queste spiegazioni se E04 non fornisce evidenza sufficiente.

---

# 5. Rivalutazione della stima teorica 17–19 turni/giorno

Il PLAN ipotizzava:

- 9 azioni `WATER`;
- circa 8–10 movimenti;
- totale teorico 17–19 turni/giorno;
- budget disponibile: 24 turni/giorno.

Il VERIFY dimostra che questa stima non era sufficiente a prevedere la sostenibilità operativa.

Documentare esplicitamente il motivo metodologico:

> Il semplice conteggio WATER + movement non rappresenta l'intero carico operativo della policy.

Il farmer deve infatti gestire anche:

- `HARVEST`;
- `PLANT`;
- routing fra task differenti;
- distribuzione temporale dei task;
- eventuali conflitti fra priorità operative.

Questo costituisce una nuova evidenza acquisita attraverso E04.

---

# 6. Decisione REVIEW

Produrre una decisione sintetica utilizzando almeno la seguente struttura:

| Dimensione | Decisione |
|---|---|
| Experimental Integrity | PASS / FAIL |
| Test Suite | PASS / FAIL |
| Standalone Submission | PASS / FAIL |
| Completion | PASS / FAIL |
| Disqualification | PASS / FAIL |
| Economic Success Criterion | PASS / FAIL |
| Water Starvation Criterion | PASS / FAIL |
| Economic Hypothesis | SUPPORTED / FALSIFIED |
| Scaling 4→9 con policy E03 | SUSTAINABLE / NOT SUSTAINABLE |
| Universal single-worker limit | SUPPORTED / NOT ESTABLISHED |
| E04 Experimental Value | VALID / INVALID |

La conclusione attesa, se confermata dalle evidenze, deve distinguere:

> **Hypothesis Falsified**

da:

> **Experiment Failed**

Un esperimento metodologicamente valido che falsifica l'ipotesi costituisce un risultato sperimentale utile e deve essere preservato.

---

# 7. Implicazioni per esperimenti successivi

Registrare esclusivamente come **candidate future**, senza definire E05:

1. **Capacity Boundary**
   - footprint intermedio, ad esempio `4 → 6`;
   - stessa policy e singolo farmer.

2. **Water-first / Scheduling Strategy**
   - footprint 9 tile;
   - modifica della priorità operativa;
   - singolo farmer.

3. **HIRE / Multi-worker**
   - footprint 9 tile;
   - introduzione di farm hands.

4. **DIG / Weed Recovery**
   - considerare separatamente;
   - classificare principalmente come meccanismo di recovery rispetto alla starvation, non automaticamente come soluzione della sua causa.

Non selezionare E05.

Non creare un piano E05.

---

# 8. Documentazione finale E04

Aggiornare la documentazione necessaria per consolidare E04, includendo almeno:

- `docs/versions/E04_verify_antigravity.md`;
- `docs/EXPERIMENT_LOG.md`;
- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`;
- eventuale README se contiene lo stato delle iterazioni sperimentali.

Creare inoltre, se coerente con la struttura utilizzata per E01–E03:

`docs/versions/E04_ship_antigravity.md`

Il documento SHIP deve registrare chiaramente:

- ipotesi;
- variabile sperimentale;
- baseline;
- risultati;
- falsificazione dell'ipotesi;
- evidenza di water starvation;
- interpretazione rigorosa del capacity bottleneck;
- valore sperimentale del risultato negativo;
- candidate future senza selezione di E05.

---

# 9. Git e SHIP

Prima del commit:

1. eseguire l'intera test suite;
2. rigenerare la submission standalone;
3. verificare `git diff`;
4. verificare `git status`;
5. verificare che non siano presenti artefatti temporanei o file non intenzionali.

Se tutto è coerente:

Commit suggerito:

`Finalize E04 initial NW scaling experiment`

Push su:

`origin/main`

Creare tag annotato:

`v0.4-e04-nw-scaling`

Messaggio tag:

`E04 Initial NW Scaling validated — hypothesis falsified`

Push del tag.

---

# 10. Stato finale richiesto

Al termine mostrare:

- REVIEW decision;
- risultati E04 consolidati;
- file aggiornati/creati;
- commit hash;
- tag creato;
- stato Git finale;
- conferma `working tree clean`.

Lo stato della prossima sessione deve indicare esplicitamente:

> **E04 è concluso e shipped. L'ipotesi 4→9 single-farmer è stata falsificata. Non iniziare automaticamente E05.**

La prossima sessione dovrà partire dalla scelta tra le candidate emerse dalla REVIEW.

---

## Stop Condition

Dopo SHIP:

**FERMARSI.**

Non iniziare E05.

Non modificare ulteriormente la strategia.

Non implementare `HIRE`.

Non modificare le priorità operative.

Non provare footprint intermedi.

Attendere la REVIEW umana prima di definire la successiva iterazione.