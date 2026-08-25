# E06-03 — BUILD Water-First Scheduling

Proseguiamo il progetto **Kaggriculture Agent** secondo il metodo sperimentale supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Le fasi seguenti sono concluse e approvate:

- `E06-01 — DEFINE Water-First Scheduling` → `GO`
- `E06-02 — PLAN Water-First Scheduling` → `GO FOR BUILD`

Documenti di riferimento:

- `docs/experiments/E06-01_Water_First_Capability_Analysis.md`
- `docs/plans/E06_Water_First_Scheduling.md`

Procedi ora esclusivamente con la fase:

# E06-03 — BUILD

---

# 1. Obiettivo sperimentale

Implementare una nuova strategia:

`WaterFirstHIRENWClusterROIAgent`

derivata dalla baseline E05:

`HIRENWClusterROIAgent`

La **sola variabile sperimentale comportamentale** deve essere la priorità operativa dei worker.

E05:

`HARVEST > PLANT > WATER`

E06:

`WATER > HARVEST > PLANT`

Tutto il resto deve rimanere invariato rispetto a E05.

---

# 2. Baseline E05 da preservare

E05 è `SHIPPED` e non deve essere alterato.

Configurazione congelata:

- footprint: 9 tile;
- cluster NW 3×3;
- coordinate `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`;
- 1 farmer principale;
- 1 farm hand giornaliera;
- `HIRE` a `$1/giorno`;
- partitioning spaziale fisso 4:5;
- farmer: 4 tile;
- hand: 5 tile;
- crop selection invariata;
- modello ROI invariato;
- seed purchasing invariato;
- vendita/liquidazione invariata;
- routing Manhattan invariato;
- worker allocation invariata;
- durata episodio: 720 turni;
- opponent: `pass`, `random`, `starter`;
- 10 episodi per opponent;
- seed 0–9;
- 30 episodi complessivi.

Baseline economico-operativa E05:

- Mean Final Money: `$21568.93 ± $361.25`;
- Median Final Money: `$21442.00`;
- Total Weed Conversions: `176`;
- Mean Unwatered End-of-Day Ratio: `3.33%`;
- Completion Rate: `100%`;
- Disqualification Rate: `0%`;
- Win Rate: `100%`.

---

# 3. Regola fondamentale del BUILD

**Non ottimizzare E06 oltre la modifica pianificata.**

L'esperimento deve misurare l'effetto puro della priorità Water-First.

Se emergono:

- routing inefficiente;
- movimenti aggiuntivi;
- ping-pong tra tile;
- raccolti ritardati;
- semine ritardate;
- perdita di cicli produttivi;
- regressione economica;
- altre inefficienze;

**NON correggerle durante E06.**

Devono essere osservate come conseguenze della variabile sperimentale.

Qualsiasi intervento ulteriore introdurrebbe un confondente e dovrà eventualmente essere valutato in una futura iterazione.

---

# 4. Implementazione richiesta

Seguire il piano E06 approvato.

Soluzione prevista:

creare:

`src/agricola/strategy/water_first_hire_nw_cluster_roi.py`

con classe:

`WaterFirstHIRENWClusterROIAgent`

Preferire:

- subclassing di `HIRENWClusterROIAgent`;
- massimo riuso dell'implementazione E05;
- override minimo necessario;
- nessuna modifica al comportamento della classe E05.

La logica E06 deve selezionare le categorie di attività nell'ordine:

1. `WATER`
2. `HARVEST`
3. `PLANT`

all'interno delle stesse regole di targeting e routing di E05.

Non cambiare il criterio Manhattan utilizzato per scegliere il target all'interno della categoria prioritaria.

---

# 5. Verifica dell'integrità della variabile singola

Prima di eseguire il benchmark, confronta E05 ed E06 e verifica esplicitamente che non siano state introdotte altre differenze comportamentali.

Controllare almeno:

- footprint;
- tile assignments;
- HIRE;
- worker count;
- partitioning;
- crop selection;
- market behavior;
- seed purchasing;
- shed behavior;
- routing;
- movement;
- target distance;
- opponent;
- seeds;
- episode length.

Documentare qualsiasi differenza tecnica necessaria all'implementazione.

Se una differenza modifica il comportamento oltre alla scheduling priority, **fermarsi e segnalarla prima del benchmark**.

---

# 6. Test automatici

Creare:

`tests/test_water_first_hire_nw_cluster.py`

o equivalente coerente con la struttura attuale.

I test devono verificare almeno:

## 6.1 Priorità E06

In presenza contemporanea di:

- almeno una tile da irrigare;
- almeno una tile raccoglibile;
- almeno una tile seminabile;

E06 deve selezionare:

`WATER`

prima delle altre categorie.

## 6.2 HARVEST dopo WATER

Se non esistono tile da irrigare ma esistono:

- tile raccoglibili;
- tile seminabili;

E06 deve scegliere:

`HARVEST`

prima di `PLANT`.

## 6.3 PLANT

Se non esistono task WATER o HARVEST ma esiste una tile seminabile:

E06 deve scegliere:

`PLANT`.

## 6.4 Regressione E05

Verificare che:

`HIRENWClusterROIAgent`

mantenga:

`HARVEST > PLANT > WATER`.

La nuova implementazione non deve modificare semanticamente E05.

## 6.5 Invarianti

Aggiungere, dove sensato, test che confermino:

- partitioning 4:5;
- worker count;
- footprint;
- comportamento HIRE;

senza duplicare inutilmente test già coperti dalla suite E05.

---

# 7. Suite completa

Eseguire:

`pytest tests/`

La suite deve completarsi senza regressioni.

Registrare:

- numero di test;
- passed;
- failed;
- eventuali warning.

Non ignorare test falliti.

---

# 8. Standalone build

Verificare che la nuova strategia sia compatibile con il processo di standalone build esistente.

Non modificare ancora:

`submission/submission.py`

Non preparare una submission Kaggle definitiva.

Se per testare la build standalone è necessario estendere tooling interno non destinato alla submission ufficiale, farlo soltanto se non altera il comportamento dell'esperimento e documentare la modifica.

---

# 9. Benchmark locale E06

Dopo il completamento dei test, eseguire il benchmark pianificato.

Configurazione:

- agent: `WaterFirstHIRENWClusterROIAgent`;
- 30 episodi;
- 720 turni per episodio;
- opponent:
  - `pass` × 10;
  - `random` × 10;
  - `starter` × 10;
- stessi seed e stesso protocollo E05.

Salvare i risultati in:

`results/e06_water_first.json`

Non sovrascrivere:

`results/e05_hire_multiworker.json`

---

# 10. Metriche da registrare

Calcolare almeno:

## Affidabilità

- Total Episodes
- Completion Rate
- Disqualification Rate
- Win / Loss / Draw
- Overall Win Rate

## Economiche

- Mean Final Money
- Sample Standard Deviation (`ddof=1`)
- Median Final Money
- Min Final Money
- Max Final Money

## Operative

- Total Weed Conversions
- Mean Weed Conversions per Episode
- Mean Unwatered End-of-Day Ratio

## Performance

- Agent Mean Turn Latency

## Breakdown

Per ciascun opponent:

- Mean Final Money
- standard deviation
- median
- wins/losses/draws
- weed conversions
- unwatered EOD, se disponibile

---

# 11. Confronto E06 vs E05

Produrre esplicitamente:

## Money

`Δ Mean Final Money = E06 − E05`

e:

`Δ% = (E06 − E05) / E05 × 100`

Baseline:

`$21568.93`

## Weed Conversions

`Δ Weeds = E06 − 176`

e riduzione percentuale.

## Mean Unwatered EOD Ratio

Confrontare con:

`3.33%`

---

# 12. Paired seed-by-seed comparison

Il PLAN ha verificato che:

`results/e05_hire_multiworker.json`

contiene risultati episode-level utilizzabili per il pairing.

Eseguire, se la struttura dei dati lo conferma effettivamente, il confronto paired E05/E06 usando:

- stesso opponent;
- stesso seed;
- stessa configurazione dell'episodio.

Per ogni episodio calcolare almeno:

`delta_money_i = money_E06_i - money_E05_i`

e, se disponibile allo stesso livello:

`delta_weeds_i = weeds_E06_i - weeds_E05_i`

Riportare:

- numero di coppie valide;
- mean paired money delta;
- median paired money delta;
- min delta;
- max delta;
- numero di episodi E06 migliori;
- numero di episodi E06 peggiori;
- numero di episodi invariati.

Se tecnicamente utile e già supportato dalle dipendenze correnti, può essere aggiunto un intervallo di confidenza o altro descrittore statistico.

**Non introdurre nuove dipendenze statistiche esclusivamente per questo scopo.**

Non chiamare “significativo” un risultato se non viene effettuato un test appropriato.

---

# 13. Classificazione operativa

Usare la matrice PLAN:

| Classe | Total Weed Conversions |
|---|---:|
| `STRONG SUCCESS` | `< 50` |
| `PARTIAL SUPPORT` | `50–119` |
| `FALSIFIED` | `≥ 120` |

Per Mean Unwatered End-of-Day Ratio:

`< 1.0%`

è un **target forte**, non una soglia binaria assoluta.

Descrivere separatamente:

- forte riduzione;
- riduzione parziale;
- invariato;
- peggiorato.

---

# 14. Guardrail economico

Baseline E05:

`$21568.93 ± $361.25`

Guardrail pratico:

`Mean Final Money ≥ $21200`

Classificazione:

- `ECONOMIC IMPROVEMENT`: `> $21568.93`
- `SUBSTANTIAL NEUTRALITY`: `$21200.00 – $21568.93`
- `MODERATE REGRESSION`: `$20500.00 – $21199.99`
- `SEVERE REGRESSION`: `< $20500.00`

Il valore `$21200` è un **guardrail operativo**, non un test statistico.

---

# 15. Non effettuare ancora REVIEW

Questa fase deve produrre i risultati necessari alla successiva valutazione.

Non dichiarare ancora:

- `SUPPORTED`;
- `FALSIFIED`;
- `SHIP`;
- `NO SHIP`;

come decisione sperimentale conclusiva.

È ammessa soltanto una classificazione **meccanica/preliminare** dei risultati rispetto alle soglie definite dal PLAN.

La decisione sperimentale definitiva sarà presa nella fase:

`E06-04 — VERIFY / REVIEW`

dopo la nostra approvazione.

---

# 16. Documentazione BUILD

Creare:

`docs/versions/E06_build_antigravity.md`

Il documento deve registrare almeno:

1. obiettivo BUILD;
2. baseline preservata;
3. file creati/modificati;
4. strategia di implementazione;
5. differenza E05/E06;
6. verifica single-variable;
7. test aggiunti;
8. risultati suite;
9. protocollo benchmark;
10. risultati benchmark grezzi/aggregati;
11. paired comparison;
12. eventuali anomalie;
13. eventuali trade-off osservati;
14. stato BUILD.

Aggiornare inoltre, se coerente:

- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`;
- `docs/EXPERIMENT_LOG.md`.

Registrare E06 esclusivamente come:

`BUILD COMPLETED — AWAITING VERIFY`

se tutte le attività tecniche sono concluse.

Non dichiararlo shipped.

---

# 17. Vincoli Git

In questa fase:

- NON creare tag;
- NON effettuare commit;
- NON effettuare push.

Mantieni tutte le modifiche disponibili per la nostra revisione.

---

# 18. Vincoli Kaggle

- NON modificare `submission/submission.py`;
- NON effettuare submission;
- NON utilizzare lo Skill Rating Kaggle per valutare E06.

La validazione Kaggle verrà eventualmente effettuata solo dopo REVIEW e SHIP.

---

# Output finale richiesto

Al termine mostra:

1. implementazione realizzata;
2. conferma della preservazione E05;
3. test creati;
4. risultati completi di `pytest`;
5. risultato standalone/build check;
6. risultati benchmark E06;
7. tabella E05 vs E06;
8. breakdown per opponent;
9. paired seed-by-seed comparison;
10. classificazione operativa preliminare;
11. classificazione economica preliminare;
12. eventuali trade-off o anomalie;
13. file creati/modificati;
14. `git diff --stat`;
15. `git status --short`.

**Fermati dopo BUILD e benchmark. Non procedere autonomamente a REVIEW, SHIP, commit, push, tag o Kaggle submission.**