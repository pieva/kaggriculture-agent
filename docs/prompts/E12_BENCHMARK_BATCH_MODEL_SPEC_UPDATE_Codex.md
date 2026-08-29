# E12 — AGGIORNAMENTO MODEL_SPEC DA BENCHMARK COMPETITIVI PRIMA DI QUALSIASI NUOVO BUILD

## Contesto

È stata creata nel repository una cartella `benchmark` contenente replay JSON di episodi Kaggle competitivi.

Prima di ragionare su Q2 o avviare un nuovo BUILD, occorre usare questi replay per aggiornare il **modello testuale** in `docs/MODEL_SPEC.md`.

Il principio metodologico è:

`OBSERVE → COMPARE → UPDATE MODEL → SOLO DOPO BUILD`

Non partire dal codice.
Non partire da Q2.
Non assumere che una singola traiettoria competitiva definisca la policy corretta.

---

## Obiettivo

Usare i JSON presenti nella cartella `benchmark` come evidenza primaria per:

1. confrontare la X1.12/X1.13 corrente con più competitor;
2. distinguere pattern ricorrenti da scelte specifiche del singolo avversario;
3. aggiornare `docs/MODEL_SPEC.md` prima di qualsiasi nuova modifica al codice;
4. identificare quali trigger/target del modello devono essere:
   - confermati;
   - declassati;
   - riformulati;
   - introdotti come nuove ipotesi;
5. definire il prossimo delta di modello **senza ancora implementarlo**.

Questa attività è solo **MODEL UPDATE / ANALISI**, non BUILD.

---

## Provenance

Lavora nel working tree locale corrente:

`C:\Users\pietr\Projects\kaggriculture-agent`

Prima di iniziare:

1. `git branch --show-current`
2. `git status --short`
3. `git log -1 --oneline`
4. localizza la cartella `benchmark`
5. elenca tutti i file JSON presenti
6. per ogni JSON calcola SHA-256
7. estrai almeno:
   - episode ID
   - seed
   - nomi agenti
   - rewards finali
   - module_version

Non creare worktree.
Non modificare strategy o submission.

---

# FASE 1 — Costruire il Benchmark Registry

Creare:

`results/benchmark/BENCHMARK_REGISTRY.md`

e, se utile:

`results/benchmark/benchmark_registry.json`

Per ogni replay registrare:

- file
- SHA-256
- episode ID
- seed
- competitor
- nostro agente
- reward nostro
- reward competitor
- differenza assoluta
- rapporto competitor / nostro score
- quadranti finali
- livestock finale
- peak Hands
- peak crop tiles
- peak productive tiles
- weeds cumulative o weed tile-days
- principali prodotti venduti
- note sintetiche

Non inventare campi se non ricostruibili dal replay.

---

# FASE 2 — Parser comparativo unico

Riutilizzare, se possibile, il parser già costruito per truebelief.

Se il parser esistente non supporta più replay/competitor, estenderlo senza modificare la strategy.

Obiettivo: produrre per ogni replay una timeline giornaliera canonica con almeno:

- day
- cash
- Hands
- quadranti
- crop tiles
- pasture tiles
- weeds
- livestock per tipo
- principali inventory
- principali SELL/BUY/HIRE/BUY_LAND
- productive actions
- movement actions
- PASS
- principali farmer/hand action categories

Produrre CSV/JSON comparabili tra episodi.

---

# FASE 3 — Analisi cross-competitor

Non limitarsi al replay più recente.

Per ogni competitor/replay identificare:

## A. Pattern condivisi
Cose osservate in più competitor forti.

Esempi possibili da verificare, non assumere:
- 5 Hands iniziali;
- forte deployment iniziale di capitale;
- Q0 pienamente produttivo;
- diversificazione crop;
- livestock precoce;
- workforce intorno a 9-12 Hands nel midgame;
- weeds quasi zero;
- monetizzazione Milk/Wool/Fertilizer;
- Q1 acquistato dopo una fase di compounding;
- endgame liquidation.

## B. Pattern variabili
Scelte che cambiano tra competitor:
- numero animali;
- mix Cow/Sheep/Goose;
- giorno Q1;
- uso o non uso Q2;
- crop mix;
- retail Wheat;
- livello di liquidità;
- peak Hands.

## C. Pattern specifici
Comportamenti presenti in un solo replay e quindi non generalizzabili senza test.

---

# FASE 4 — Rivalutare le assunzioni correnti del MODEL_SPEC

Per ogni regola/target corrente in `docs/MODEL_SPEC.md`, creare una tabella:

| Regola corrente | Evidenza precedente | Nuova evidenza benchmark | Stato aggiornato | Azione |
|---|---|---|---|---|

Usare gli stati:

- `OBSERVED_REFERENCE`
- `INFERRED`
- `IMPLEMENTED`
- `TESTED`
- `ADOPTED`
- `REJECTED`

Possibili azioni:

- `CONFIRM`
- `DOWNGRADE`
- `REFORMULATE`
- `REMOVE`
- `NEW HYPOTHESIS`

Prestare particolare attenzione a:

- livestock target;
- crop maintenance;
- HIRE;
- liquidità;
- crop mix;
- commodity Wheat;
- worker assignment;
- shed logistics;
- selling cadence;
- land expansion.

---

# FASE 5 — Q2: NON DECIDERE ANCORA

Q2 deve essere analizzato soltanto dopo il confronto cross-competitor.

Non assumere:
- Q2 necessario;
- Q2 vietato;
- Q2 target.

Creare una sezione specifica:

## Evidence on Q2

Per ogni replay indicare:

- Q2 acquistato? sì/no
- giorno
- stato economico prima dell'acquisto
- superficie Q0+Q1 prima dell'acquisto
- backlog/weeds
- Hands
- payback osservabile
- impatto sul final money

Poi concludere soltanto con una delle categorie:

- `NO EVIDENCE`
- `MIXED EVIDENCE`
- `CONSISTENT SUPPORT`
- `CONSISTENT REJECTION`

Se i replay forti arrivano a score elevati senza Q2, non proporre Q2 come priorità.

Se alcuni lo usano e altri no, classificare Q2 come **conditional expansion option**.

---

# FASE 6 — Focus su workforce throughput

Il replay Dr. Mikholae Hutchinson ha mostrato una divergenza importante da verificare sistematicamente:

- nostro score: `38.815`
- competitor: `90.137`
- stesso seed: `1056561958`

Ipotesi corrente da testare:

> Il collo principale non è il livestock in sé, ma la capacità di mantenere simultaneamente crop engine, livestock engine e logistics senza accumulare backlog.

Verificare quindi cross-competitor:

- weeds per giorno;
- crop tiles attive;
- Hands;
- productive/movement ratio;
- backlog implicito;
- cash deployment;
- crop surface vs livestock count;
- eventuali worker role specialization.

Non trasformare subito questa ipotesi in codice.

---

# FASE 7 — Capital deployment

Verificare il pattern osservato:

- noi possiamo avere cash disponibile mentre crop surface degrada;
- alcuni competitor spendono aggressivamente in workforce/capacità;
- altri mantengono liquidità ma senza backlog.

Definire nel MODEL_SPEC un concetto di:

`Deployable Capital`

distinto da semplice `cash`.

Possibile definizione:

> capitale che può essere convertito in produttività aggiuntiva entro un payback compatibile con l'orizzonte residuo.

Questo deve rimanere concetto `INFERRED` finché non implementato.

---

# FASE 8 — Aggiornare MODEL_SPEC

Dopo l'analisi, aggiornare:

`docs/MODEL_SPEC.md`

con almeno:

## 1. Benchmark evidence base
Elenco dei replay competitivi usati come training evidence.

## 2. Cross-competitor invariants
Pattern ricorrenti supportati da più replay.

## 3. Conditional behaviors
Comportamenti dipendenti da seed/mercato/stato.

## 4. Rejected hard targets
Valori osservati che non devono essere hardcoded.

## 5. Current model hypotheses
Nuove ipotesi da testare.

## 6. Training interpretation
Ribadire:

> Il modello viene aggiornato tramite evidenza competitiva osservabile e modifiche esplicite a trigger/target/regole. Non vengono aggiornati pesi di reti neurali.

## 7. Model Change Log
Aggiungere una voce:

`Competitive Benchmark Batch #1`

con:

- replay analizzati;
- pattern confermati;
- pattern falsificati;
- regole riformulate;
- ipotesi nuove;
- nessun Code Delta ancora applicato.

---

# FASE 9 — Proporre il prossimo Model Delta

Solo dopo avere aggiornato `MODEL_SPEC.md`, proporre:

`results/benchmark/NEXT_MODEL_DELTA.md`

Non implementare.

Il documento deve contenere:

1. massimo 3 divergenze strutturali ad alto impatto;
2. evidenza multi-replay che le supporta;
3. trigger/target da modificare;
4. effetto atteso;
5. metriche di VERIFY;
6. counterfactual da eseguire;
7. rischi di overfitting.

Il delta deve essere formulato in modo parametrico.

Esempio corretto:

`HIRE capacity target = funzione di workload e backlog previsto`

Esempio scorretto:

`usa 10 Hands perché Hutchinson ne usa 10`

---

# Output finale richiesto

Riportare:

1. replay trovati nella cartella benchmark;
2. registry creato;
3. SHA-256 per ogni replay;
4. tabella comparativa competitor;
5. pattern condivisi;
6. pattern variabili;
7. pattern specifici;
8. principali assunzioni del MODEL_SPEC confermate/falsificate;
9. stato evidenza Q2;
10. stato evidenza livestock;
11. stato evidenza workforce;
12. stato evidenza capital deployment;
13. modifiche apportate a `MODEL_SPEC.md`;
14. contenuto sintetico di `NEXT_MODEL_DELTA.md`;
15. file creati/modificati;
16. `git diff --stat`;
17. `git status --short`.

Vincoli finali:

- non modificare strategy;
- non modificare submission;
- non fare BUILD;
- non fare upload Kaggle;
- non fare commit;
- non iniziare una nuova versione codice.

Dichiarazione finale:

`BENCHMARK BATCH ANALYZED`
`MODEL_SPEC UPDATED`
`CODE DELTA: NOT STARTED`
