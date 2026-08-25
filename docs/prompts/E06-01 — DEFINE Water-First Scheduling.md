# E06-01 — DEFINE Water-First Scheduling

Stiamo proseguendo il progetto **Kaggriculture Agent** con il metodo sperimentale supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

## Contesto

Le iterazioni E01–E05 sono concluse.

**E05 — `HIRENWClusterROIAgent` è SHIPPED e non deve essere modificato.**

E05 ha introdotto:

- footprint produttivo di 9 tile nel cluster NW 3×3;
- 1 farmer principale;
- 1 farm hand giornaliera tramite `HIRE`;
- partitioning spaziale fisso 4:5 tra i due worker;
- policy operativa `HARVEST > PLANT > WATER`.

Risultati locali consolidati E05:

- 30 episodi;
- Completion Rate: 100%;
- Disqualification Rate: 0%;
- Win Rate: 100%;
- Mean Final Money: `$21568.93 ± $361.25`;
- Median Final Money: `$21442.00`;
- Weed Conversions: `176`;
- Mean Unwatered End-of-Day Ratio: `3.33%`.

La REVIEW E05 ha classificato:

- Economic Hypothesis: `SUPPORTED`;
- Worker Capacity Bottleneck: `STRONGLY SUPPORTED`;
- Starvation Operational Status: `STARVATION REDUCED BUT UNRESOLVED`.

La validazione Kaggle E05 si è nel frattempo assestata a uno Skill Rating osservato di **439.7**, superiore agli score attualmente mostrati per E01, E02 ed E03.

Questo dato deve essere registrato come evidenza esterna aggiornata, ma **non deve essere utilizzato per modificare retroattivamente i risultati locali o la valutazione sperimentale di E05**.

---

# Obiettivo E06

Vogliamo valutare come candidata E06 una modifica della sola priorità operativa:

`HARVEST > PLANT > WATER`

→

`WATER > HARVEST > PLANT`

mantenendo per quanto possibile invariati tutti gli altri elementi di E05.

La domanda sperimentale preliminare è:

> **Il problema operativo residuo osservato in E05 dipende, almeno in parte, dal fatto che WATER viene eseguito dopo HARVEST e PLANT?**

L'ipotesi da analizzare è che una policy **Water-First** possa ridurre starvation, tile non irrigate a fine giornata e conseguenti weed conversions, senza introdurre una regressione economica tale da rendere la strategia complessivamente peggiore di E05.

Questa formulazione è ancora preliminare: deve essere verificata rispetto al comportamento effettivo dell'ambiente e all'implementazione corrente.

---

# Attività richiesta — solo DEFINE

**NON modificare ancora il codice dell'agente.**

**NON implementare E06.**

**NON eseguire ancora il benchmark E06.**

Prima di qualsiasi BUILD:

1. ispeziona il codice e la documentazione corrente di E05;
2. identifica esattamente dove e come è implementata la policy `HARVEST > PLANT > WATER`;
3. verifica il significato operativo delle metriche:
   - Weed Conversions;
   - Mean Unwatered End-of-Day Ratio;
   - eventuali altre metriche già disponibili utili a misurare starvation e capacità operativa;
4. verifica, sulla base dell'ambiente e del codice esistente, la relazione effettiva tra:
   - irrigazione tardiva;
   - stato non irrigato delle tile;
   - weed conversion;
   - raccolta;
   - semina;
   - risultato economico;
5. determina se la sostituzione con `WATER > HARVEST > PLANT` costituisce realmente una modifica isolabile e controllata rispetto a E05;
6. individua eventuali confondenti che renderebbero il confronto E05/E06 non valido;
7. valuta se mantenere invariati:
   - footprint 3×3 / 9 tile;
   - posizione del cluster NW;
   - 1 farmer + 1 farm hand;
   - costo e modalità di `HIRE`;
   - partitioning fisso 4:5;
   - crop selection;
   - movement/pathfinding;
   - durata degli episodi;
   - opponent set;
   - seed e protocollo di benchmark;
8. proponi le metriche primarie e secondarie appropriate per E06;
9. proponi criteri di successo e falsificazione metodologicamente giustificati.

## Importante sulle soglie

I valori E05:

- `176` Weed Conversions;
- `3.33%` Mean Unwatered End-of-Day Ratio;
- `$21568.93` Mean Final Money;

devono essere trattati inizialmente come **baseline di confronto**, non come soglie di successo imposte a priori.

Non assumere automaticamente che:

- Weed Conversions `< 176`;
- Mean Unwatered EOD Ratio `< 3.33%`;

siano da soli criteri sufficienti per dichiarare E06 riuscito.

Valuta quali variazioni siano sperimentalmente ed economicamente significative e proponi criteri motivati.

---

# Controllo dell'ipotesi

Verifica in particolare un possibile trade-off.

Dare priorità a `WATER` potrebbe migliorare la gestione idrica ma ritardare `HARVEST` o `PLANT`, riducendo il numero di cicli produttivi o il risultato economico.

L'esperimento non deve quindi ottimizzare una metrica operativa ignorando il risultato economico complessivo.

Distingui esplicitamente:

- miglioramento operativo;
- neutralità/regressione economica;
- miglioramento economico;
- eventuale trade-off tra questi risultati.

---

# Output richiesto

Produci un documento:

`docs/experiments/E06-01_Water_First_Capability_Analysis.md`

Il documento deve contenere almeno:

1. **Experimental Question**
2. **E05 Baseline**
3. **Current Scheduling Logic**
4. **Environment Mechanics Relevant to WATER**
5. **Relationship Between Watering, Starvation and Weeds**
6. **Candidate E06 Intervention**
7. **Controlled Variables**
8. **Potential Confounders**
9. **Primary Metrics**
10. **Secondary / Diagnostic Metrics**
11. **Economic Trade-off**
12. **Proposed Success / Falsification Criteria**
13. **Risks**
14. **Recommendation: GO / REVISE / NO-GO**

Se l'analisi conclude `GO`, proponi alla fine una formulazione precisa e falsificabile dell'ipotesi E06 da utilizzare nella successiva fase PLAN.

Se conclude `REVISE` o `NO-GO`, spiega quale assunzione della candidata Water-First non è supportata.

---

# Aggiornamento documentale E05

Aggiorna inoltre **solo la documentazione relativa alla validazione esterna E05**, senza modificare codice o risultati locali E05, per registrare lo Skill Rating Kaggle osservato e stabilizzato a:

`439.7`

Mantieni distinta:

- **local validation**;
- **Kaggle external validation**.

Non reinterpretare retroattivamente E01–E05 sulla sola base degli Skill Rating Kaggle.

---

# Vincoli

- Non modificare l'implementazione E05.
- Non creare ancora l'agente E06.
- Non modificare `submission/submission.py`.
- Non eseguire una nuova submission Kaggle.
- Non effettuare BUILD.
- Non effettuare VERIFY.
- Non effettuare SHIP.
- Non creare tag Git.
- Non effettuare commit o push in questa fase, salvo istruzione successiva.
- Mantieni la compatibilità con il protocollo sperimentale e con la struttura documentale esistente del repository.

Al termine fermati e mostrami:

1. sintesi dell'analisi;
2. definizione proposta dell'esperimento E06;
3. metriche e criteri proposti;
4. eventuali criticità;
5. raccomandazione `GO / REVISE / NO-GO`;
6. file creati o modificati;
7. `git diff --stat`;
8. `git status --short`.

**Attendi la mia approvazione prima di procedere alla fase PLAN.**