# E06-02 — PLAN Water-First Scheduling

Proseguiamo il progetto **Kaggriculture Agent** secondo il metodo sperimentale supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

La fase:

**E06-01 — DEFINE Water-First Scheduling**

è stata completata e approvata con decisione:

`GO`

Documento di riferimento:

`docs/experiments/E06-01_Water_First_Capability_Analysis.md`

---

# Stato di partenza

**E05 — `HIRENWClusterROIAgent` è SHIPPED e costituisce la baseline sperimentale di E06.**

Configurazione E05 da mantenere invariata:

- footprint: 9 tile;
- cluster NW 3×3;
- coordinate `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`;
- 1 farmer principale;
- 1 farm hand giornaliera tramite `HIRE`;
- costo HIRE: `$1/giorno`;
- partitioning spaziale fisso 4:5;
- farmer principale: 4 tile;
- farm hand: 5 tile;
- crop selection e modello economico invariati;
- routing Manhattan invariato;
- durata episodio: 720 turni;
- opponent:
  - `pass`;
  - `random`;
  - `starter`;
- 10 episodi per opponent;
- seed `0–9`;
- 30 episodi complessivi.

Policy E05:

`HARVEST > PLANT > WATER`

Risultati locali consolidati:

- Completion Rate: `100.00%`;
- Disqualification Rate: `0.00%`;
- Win Rate: `100.00%`;
- Mean Final Money: `$21568.93 ± $361.25`;
- Median Final Money: `$21442.00`;
- Total Weed Conversions: `176`;
- Mean Unwatered End-of-Day Ratio: `3.33%`.

La validazione Kaggle E05 è separata dalla valutazione locale e non deve essere utilizzata come metrica primaria dell'esperimento E06.

---

# Ipotesi E06

La sola variabile sperimentale da modificare è l'ordine di priorità operativa dei worker.

Da:

`HARVEST > PLANT > WATER`

a:

`WATER > HARVEST > PLANT`

Nome candidato dell'agente:

`WaterFirstHIRENWClusterROIAgent`

Domanda sperimentale:

> **La priorità tardiva assegnata a WATER in E05 è una causa significativa della starvation residua osservata sul cluster a 9 tile?**

Ipotesi:

> **A parità di footprint, worker, partitioning, crop selection, routing, opponent e seed, assegnare priorità a WATER prima di HARVEST e PLANT ridurrà sostanzialmente le weed conversions e le tile non irrigate a fine giornata, senza produrre una regressione economica materialmente significativa rispetto a E05.**

---

# Obiettivo della fase PLAN

Produci un piano sperimentale completo e implementabile per E06.

**NON modificare ancora il codice sorgente.**

**NON implementare ancora `WaterFirstHIRENWClusterROIAgent`.**

**NON eseguire ancora benchmark E06.**

**NON modificare `submission/submission.py`.**

Il PLAN deve specificare esattamente:

1. cosa verrà modificato;
2. cosa resterà invariato;
3. come verrà implementata la modifica;
4. come verrà verificata l'integrità sperimentale;
5. quali metriche verranno raccolte;
6. come verrà confrontato E06 con E05;
7. come verranno classificati i possibili risultati.

---

# 1. Single-variable experimental design

Conferma che E06 costituisce un esperimento a **variabile singola**.

La sola modifica ammessa deve essere:

`HARVEST > PLANT > WATER`

→

`WATER > HARVEST > PLANT`

Non devono essere introdotte contemporaneamente modifiche a:

- footprint;
- tile ownership;
- worker count;
- HIRE;
- crop selection;
- seed purchasing;
- market logic;
- movement;
- routing;
- Manhattan distance;
- worker partitioning;
- timing degli episodi;
- opponent;
- seed;
- benchmark protocol.

Se durante la pianificazione emerge che una modifica collaterale è tecnicamente necessaria, segnalala esplicitamente come possibile confondente e fermati prima di includerla nel piano.

---

# 2. Strategia di implementazione

Definisci il modo più conservativo per introdurre E06.

Preferire:

- una nuova strategy class;
- riuso dell'implementazione E05;
- minima duplicazione possibile;
- nessuna modifica retroattiva al comportamento E05.

Valuta se implementare:

`WaterFirstHIRENWClusterROIAgent`

tramite:

- inheritance;
- override mirato;
- parametrizzazione della scheduling policy;

oppure altra soluzione coerente con l'architettura esistente.

La soluzione deve mantenere **E05 riproducibile esattamente come prima**.

Indica:

- file da creare;
- file da modificare;
- classi coinvolte;
- metodo/i coinvolti;
- test da aggiungere o aggiornare.

Non implementare ancora nulla.

---

# 3. Metriche primarie

## 3.1 Total Weed Conversions

Baseline E05:

`176`

Misurare sul benchmark completo di 30 episodi.

Questa è la principale metrica operativa.

## 3.2 Mean Final Money

Baseline E05:

`$21568.93 ± $361.25`

È la principale metrica economica.

Registrare almeno:

- media;
- deviazione standard campionaria (`ddof=1`);
- mediana;
- delta assoluto E06 vs E05;
- delta percentuale E06 vs E05.

---

# 4. Metriche secondarie e diagnostiche

Registrare almeno:

- Mean Unwatered End-of-Day Ratio;
- Completion Rate;
- Disqualification Rate;
- Win Rate;
- Harvest Yield Count o metrica equivalente disponibile;
- cicli produttivi completati, se tecnicamente misurabili senza alterare l'esperimento;
- breakdown per opponent;
- Agent Mean Turn Latency;
- eventuali indicatori diagnostici già disponibili nel runner.

Baseline E05 per Mean Unwatered EOD Ratio:

`3.33%`

---

# 5. Classificazione dei risultati operativi

Non utilizzare un criterio puramente binario.

Per **Total Weed Conversions** utilizzare questa classificazione preliminare:

| Classe | Total Weed Conversions | Interpretazione |
|---|---:|---|
| `STRONG SUCCESS` | `< 50` | Water-First elimina gran parte della starvation |
| `PARTIAL SUPPORT` | `50–119` | Water-First migliora il problema, ma non lo risolve completamente |
| `FALSIFIED` | `≥ 120` | La priorità di scheduling non spiega sufficientemente la starvation residua |

Verifica nel PLAN che queste soglie siano coerenti con il DEFINE e con i dati disponibili.

Se proponi variazioni, motivale esplicitamente.

---

# 6. Mean Unwatered End-of-Day Ratio

Baseline:

`3.33%`

Usa:

`< 1.0%`

come **target forte**, non come unico criterio binario di successo.

Il PLAN deve distinguere tra:

- forte riduzione;
- riduzione parziale;
- nessun miglioramento;
- peggioramento.

Non dichiarare E06 falsificato automaticamente solo perché il valore finale è leggermente superiore all'1%, se le altre metriche mostrano un miglioramento operativo sostanziale.

---

# 7. Guardrail economico

Utilizzare:

`Mean Final Money ≥ $21200`

come **guardrail pratico di non-regressione**, non come test statistico formale.

Non descrivere `$21200` come soglia di «significatività statistica».

La baseline E05 è:

`$21568.93 ± $361.25`

Il valore `$21200` rappresenta una tolleranza operativa approssimativamente pari a una deviazione standard sotto la media E05.

La classificazione economica deve distinguere almeno:

- miglioramento;
- sostanziale neutralità;
- regressione moderata;
- regressione incompatibile con il guardrail.

---

# 8. Confronto paired E05/E06

Poiché E05 ed E06 utilizzeranno:

- gli stessi opponent;
- gli stessi seed;
- lo stesso numero di episodi;
- la stessa configurazione ambientale;

pianifica, se tecnicamente possibile con i risultati esistenti, anche un confronto **paired seed-by-seed**.

Per ciascuna coppia corrispondente E05/E06, considera almeno:

`delta_money = final_money_E06 - final_money_E05`

Se i dati E05 episode-level sono già disponibili nei risultati salvati, riutilizzali.

Non rieseguire E05 se non strettamente necessario.

Nel PLAN specifica:

- dove sono memorizzati i risultati episode-level E05;
- se il pairing è effettivamente possibile;
- quali statistiche paired possono essere calcolate senza introdurre dipendenze non necessarie.

Il paired comparison deve essere considerato **analisi diagnostica aggiuntiva**, non deve sostituire Mean Final Money, deviazione standard, mediana e breakdown tradizionali.

---

# 9. Trade-off operativo/economico

Il PLAN deve esplicitamente verificare il rischio individuato nel DEFINE:

> anticipare WATER può salvare le colture ma ritardare HARVEST e PLANT.

Valuta come diagnosticare:

- raccolti ritardati;
- semine ritardate;
- eventuale perdita di un ciclo produttivo;
- incremento delle distanze percorse;
- routing ping-pong;
- capitale immobilizzato in seed non ancora utilizzati.

Non modificare il routing per correggere questi effetti durante E06.

Se emergono, devono essere osservati come conseguenze della policy Water-First e non corretti all'interno dello stesso esperimento.

---

# 10. Matrice decisionale finale

Il PLAN deve proporre una matrice di interpretazione che combini almeno:

- risultato operativo;
- risultato economico;
- affidabilità esecutiva.

Esempi di possibili esiti:

### A — Strong Success
- Weed Conversions `< 50`;
- forte riduzione Unwatered EOD;
- Mean Final Money `≥ $21200`;
- Completion `100%`;
- Disqualification `0%`.

Interpretazione:

`E06 SUPPORTED / SHIP CANDIDATE`

### B — Operational Success with Economic Trade-off
- forte riduzione starvation;
- Mean Final Money `< $21200`.

Interpretazione:

Water-First funziona operativamente ma il trade-off economico è eccessivo.

Non classificare automaticamente come successo complessivo.

### C — Partial Support
- Weed Conversions `50–119`;
- miglioramento Unwatered EOD;
- economia sostanzialmente preservata.

Interpretazione:

la priorità WATER contribuisce alla starvation ma non ne è l'unica causa.

### D — Falsified
- Weed Conversions `≥ 120`;
- miglioramento operativo marginale o assente.

Interpretazione:

la deferizione di WATER non è la causa principale del problema residuo.

### E — Reliability Failure
- Completion `< 100%`;
- Disqualification `> 0%`;
- regressioni esecutive.

Interpretazione:

E06 non è accettabile indipendentemente dai risultati economici.

Raffina questa matrice nel piano se necessario, mantenendo però distinta la dimensione operativa da quella economica.

---

# 11. VERIFY previsto

Definisci già nel PLAN il protocollo VERIFY che verrà utilizzato dopo BUILD.

Deve includere almeno:

### Test automatici
- suite esistente;
- nuovi test sulla priority policy;
- verifica che E05 mantenga la vecchia policy;
- verifica che E06 utilizzi esclusivamente Water-First;
- controllo standalone build.

### Benchmark locale
- 30 episodi;
- 10 `pass`;
- 10 `random`;
- 10 `starter`;
- seed `0–9`;
- 720 turni;
- stesso protocollo E05.

### Analisi
- aggregati;
- breakdown per opponent;
- confronto E06 vs E05;
- eventuale paired seed comparison;
- controllo episodi anomali;
- weeds;
- unwatered EOD;
- money;
- reliability.

---

# 12. Nessuna Kaggle submission in questa fase

E06 deve essere prima:

`PLAN → BUILD → VERIFY → REVIEW`

Solo se REVIEW autorizzerà SHIP potrà essere valutata una nuova submission Kaggle.

Non preparare e non inviare submission Kaggle durante PLAN.

---

# Output richiesto

Crea:

`docs/plans/E06_Water_First_Scheduling.md`

Il documento deve contenere almeno:

1. **Experiment ID and Objective**
2. **Baseline E05**
3. **Experimental Hypothesis**
4. **Independent Variable**
5. **Controlled Variables**
6. **Implementation Strategy**
7. **Files and Classes Impacted**
8. **Primary Metrics**
9. **Secondary Metrics**
10. **Operational Success Classification**
11. **Economic Guardrail**
12. **Paired E05/E06 Comparison**
13. **Trade-off Analysis**
14. **Confounder Controls**
15. **Test Plan**
16. **Benchmark Protocol**
17. **Decision Matrix**
18. **Rollback / Preservation of E05**
19. **Expected Artifacts**
20. **GO / REVISE / NO-GO for BUILD**

Aggiorna inoltre, se coerente con la struttura corrente:

- `docs/NEW_SESSION.md`;
- `docs/PROJECT_STATE.md`;
- eventuale indice dei piani o log sperimentale;

ma **solo per registrare che E06 è nella fase PLAN**.

Non dichiarare E06 implementato, verificato o concluso.

---

# Vincoli

- Non modificare ancora codice sorgente.
- Non creare ancora la classe E06.
- Non modificare il comportamento E05.
- Non modificare `submission/submission.py`.
- Non eseguire benchmark E06.
- Non eseguire submission Kaggle.
- Non creare tag Git.
- Non effettuare commit.
- Non effettuare push.
- Non iniziare BUILD.

---

# Output finale della sessione Antigravity

Al termine mostrami:

1. sintesi del PLAN;
2. ipotesi sperimentale definitiva;
3. variabile indipendente e variabili controllate;
4. strategia di implementazione prevista;
5. metriche;
6. classificazione `STRONG SUCCESS / PARTIAL SUPPORT / FALSIFIED`;
7. guardrail economico;
8. fattibilità del paired comparison E05/E06;
9. protocollo VERIFY previsto;
10. criticità residue;
11. raccomandazione `GO / REVISE / NO-GO` per BUILD;
12. file creati o modificati;
13. `git diff --stat`;
14. `git status --short`.

**Fermati al termine del PLAN e attendi la mia approvazione prima di qualsiasi BUILD.**