# E11-X1.1A — AUDIT — HIRE Constraint Verification + E06 Productivity Reconciliation

## Obiettivo

Prima di procedere a **E11-X1.2 — 2-Worker Revenue Throughput Optimization**, verificare rigorosamente due questioni che al momento non possono essere considerate dimostrate:

1. **Perché E11-X1.1 non riesce ad assumere più di 2 worker?**
2. **Perché E06, con footprint molto più piccolo, riusciva a ottenere prestazioni economiche molto superiori?**

Non accettare come fatto il precedente verdetto:

> `2 Quadrants => max 2 workers`

finché non viene dimostrato direttamente dalle regole dell'environment o da micro-test controllati.

Il confronto con **E06** è obbligatorio e deve essere ricostruito da evidenza macchina/storica disponibile nel repository, non da valori narrativi non verificati.

---

# 1. Stato quantitativo verificato

Baseline autorevole:

> **E11-VB1**

- Mean Final Money: **$429.00**
- 3Q unlock: **0 / 30**
- Peak land: **50 tile / 2Q**
- Active tiles: circa **17**
- Workforce: **2**
- Provenance: **PASS**

E11-X1:

- 3Q unlock: **0 / 5**
- Mean Final Money: **$429**
- Workforce: **2**
- Active tiles: **~17**

E11-X1.1:

- Stage B: **5 episodi**
- Mean Final Money: **$429**
- Peak workforce: **2**
- Peak active tiles: **17**
- 3Q unlock: **0 / 5**
- Provenance: **PASS**

Il precedente report ha interpretato il mancato hiring come:

> `ENVIRONMENT WORKFORCE HARD-CAP`

Questa interpretazione è ora da considerare:

> **HYPOTHESIS TO VERIFY — NOT YET ESTABLISHED FACT**

---

# 2. Contraddizione da risolvere: E06

Il progetto contiene un riferimento storico molto importante:

> **E06 — 9t Water-First / multi-worker strategy**

che nei benchmark storici raggiungeva circa:

> **$24k–$25k Mean Final Money**

con una superficie produttiva molto inferiore a E11-VB1.

Questo crea una contraddizione diagnostica fondamentale:

```text
E06:
small footprint
+ multi-worker / effective execution
→ ~$25k

E11-VB1:
50 tiles owned
+ 2 workers
→ $429
```

Non possiamo attribuire automaticamente il divario al solo terreno o al presunto hard-cap workforce.

Dobbiamo capire **che cosa E06 faceva concretamente meglio**.

---

# 3. Scopo dell'audit

Procedere con:

> **E11-X1.1A — HIRE Constraint Verification + E06 Productivity Reconciliation**

Questo NON è un nuovo trattamento economico.

È un audit diagnostico.

NON modificare ancora la strategia per migliorare il risultato.

---

# 4. Parte A — verificare la regola HIRE nell'environment

Individuare nel codice dell'environment / action validation la logica esatta che determina se:

> `HIRE`

è valido o rifiutato.

Ricostruire tutte le precondizioni.

Verificare almeno:

- cash requirement;
- hiring cost;
- numero corrente di worker;
- eventuale worker cap;
- eventuale relazione worker/land;
- eventuale relazione worker/quadrant;
- cooldown;
- hour/day restriction;
- location requirement;
- prerequisite;
- action priority/conflict;
- ownership requirement;
- limite globale;
- limite per player;
- eventuali condizioni non evidenti.

Riportare:

> **la condizione esatta nel codice**

con file e linee.

---

# 5. Non inferire il cap dal solo comportamento

Il fatto che:

> `HIRE` venga rifiutato

NON dimostra automaticamente:

> `2Q => 2 workers maximum`

Serve identificare il motivo di rifiuto.

Se l'environment espone reason/error/status:

registrarlo.

Se non lo espone:

strumentare un micro-test diagnostico senza modificare le regole.

---

# 6. Micro-test HIRE

Creare uno script diagnostico, ad esempio:

`scratch/audit_hire_constraints.py`

Non serve un benchmark 720-step.

Costruire stati controllati e testare HIRE variando una dimensione per volta.

Test minimi:

### A. Land / workforce

- 1Q + 1 worker → HIRE?
- 1Q + 2 worker → HIRE?
- 2Q + 2 worker → HIRE?
- 2Q + 3 worker → HIRE?
- 3Q + 2 worker → HIRE?
- 3Q + 3 worker → HIRE?
- 4Q + N worker → HIRE?

### B. Cash

Ripetere con:

- cash insufficiente;
- cash appena sufficiente;
- cash abbondante.

### C. Timing

Provare:

- Day 0;
- Day 1;
- Day 4;
- differenti ore se rilevanti.

### D. Position / state

Se HIRE richiede posizione o altro requisito, testarlo esplicitamente.

---

# 7. Output Parte A

Produrre una matrice:

| Land | Current Workers | Cash | Day/Hour | HIRE Requested | Accepted | Reason |
|---|---:|---:|---|---|---|---|

Concludere con UNO dei seguenti verdict:

- `LAND-DEPENDENT WORKFORCE CAP CONFIRMED`
- `GLOBAL WORKFORCE CAP CONFIRMED`
- `HIRE CASH CONSTRAINT`
- `HIRE TIMING CONSTRAINT`
- `HIRE LOCATION/STATE CONSTRAINT`
- `AGENT HIRE ACTION BUG`
- `OTHER VERIFIED CONSTRAINT`

Non usare formule vaghe.

---

# 8. Parte B — ricostruzione E06

Questa parte è obbligatoria.

Individuare nel repository:

- strategy class E06;
- config E06;
- report E06;
- benchmark/result JSON originale se disponibile;
- test;
- eventuali telemetry/log;
- EXPERIMENT_LOG;
- README/version docs;
- eventuale submission implementation.

Identificare la strategia **esatta** usata da E06.

---

# 9. Provenance E06

Prima di usare qualsiasi numero storico, classificarlo:

- `PRIMARY MACHINE EVIDENCE`
- `DERIVED FROM PRIMARY DATA`
- `HISTORICAL DOCUMENTED RESULT`
- `NARRATIVE ONLY`
- `UNVERIFIED`

Dopo l'incidente E11-R2 non assumere che un numero documentato sia automaticamente machine-verifiable.

---

# 10. Non rieseguire subito E06

Prima:

1. cercare il dataset originale;
2. verificare config/code provenance;
3. verificare che il risultato storico sia ricostruibile.

Se esiste evidenza primaria sufficiente:

> NON rieseguire E06.

Se manca evidenza primaria ma la strategy/config storica è ricostruibile in modo affidabile:

> è consentito UN SOLO smoke episode E06 per confronto diagnostico.

NON fare 30 episodi.

NON fare 10 episodi.

---

# 11. Metriche E06 da ricostruire

Ricostruire, se supportato dall'evidenza:

- owned land;
- productive footprint;
- peak active tiles;
- workforce;
- hire timing;
- crop portfolio;
- seed spending;
- watering cadence;
- harvesting cadence;
- movement;
- revenue;
- final money;
- inventory liquidation;
- land purchases;
- livestock;
- action priority.

---

# 12. Confronto strutturale E06 vs E11-VB1

Produrre obbligatoriamente:

| Dimension | E06 | E11-VB1 | Difference |
|---|---:|---:|---|
| Owned land | | 50 | |
| Active tiles | | ~17 | |
| Workforce | | 2 | |
| Active tiles / worker | | ~8.5 | |
| First hire timing | | | |
| Peak workforce | | 2 | |
| Crop mix | | | |
| Watering policy | | | |
| Harvest policy | | | |
| Seed spending | | | |
| Expansion spending | | | |
| Mean Final Money | | $429 | |
| Revenue before Day 5 | | | |
| Idle cash | | | |
| Movement burden | | | |

---

# 13. Domanda fondamentale E06

Rispondere:

> **Come può E06 produrre circa $25k su un footprint piccolo mentre E11-VB1 produce $429 possedendo 50 tile?**

Non accettare una spiegazione generica.

Identificare il/i meccanismo/i concreto/i.

Possibili categorie da verificare, NON da assumere:

- workforce;
- watering;
- crop choice;
- seed affordability;
- harvest timing;
- selling;
- movement locality;
- excessive land spending;
- capital reserve;
- starvation;
- action ordering;
- active footprint;
- crop death;
- inventory not sold;
- regression introdotta nella nuova architecture.

---

# 14. Confronto delle action priority

Confrontare la gerarchia azioni E06 con E11-VB1.

Produrre:

| Priority | E06 | E11-VB1 |
|---|---|---|

Verificare se E11 ha introdotto una regressione nel dispatcher.

---

# 15. Confronto crop lifecycle

Confrontare almeno:

- crop selected;
- growth duration;
- seed cost;
- market value;
- watering requirement;
- expected cycles per episode;
- gross revenue potential.

Non fare assunzioni teoriche se i valori sono disponibili nell'environment.

Leggerli direttamente.

---

# 16. Confronto workload

Stimare dal comportamento reale:

> workload richiesto / worker capacity

per E06 e VB1.

Verificare se E11 possiede 50 tile ma ne attiva 17 perché:

- mancano worker;
- oppure il dispatcher non genera abbastanza DIG/PLANT/WATER;
- oppure le colture muoiono;
- oppure il capitale impedisce il planting.

---

# 17. Worker efficiency

Calcolare quando possibile:

- productive actions / worker / day;
- MOVE actions / worker / day;
- PASS / idle;
- active tiles / worker;
- harvested value / worker.

Questo è particolarmente importante perché:

> **più worker non servono se il dispatcher non li usa produttivamente.**

---

# 18. Competitor benchmark come terzo riferimento

Aggiungere alla matrice anche il benchmark top verificato:

### Around 3Q

- Day 4.20
- 4–6 workers
- 35–45 active tiles

### Around 4Q

- Day 8.53
- 8–10 workers
- 75–85 active tiles

La comparazione deve quindi essere:

> **E06 ↔ E11-VB1 ↔ TOP**

Non solo E11-VB1 ↔ TOP.

---

# 19. Matrice finale

Produrre:

| Metric | E06 | E11-VB1 | TOP |
|---|---:|---:|---:|
| Early workforce | | 2 | |
| Active footprint | | ~17 | 35–45 @3Q |
| 3Q timing | | never | 4.20 |
| 4Q timing | | never | 8.53 |
| Final Money | ~25k historical | $429 | ~70–75k+ |
| Crop strategy | | | |
| Workforce utilization | | | |
| Revenue engine | | | |

---

# 20. Verificare la semantica dei “9 tile”

Chiarire esattamente che cosa significava:

> **E06 9t**

Potrebbe significare:

- 9 active crop tiles;
- 9 target tiles;
- 9 owned tiles;
- 9 managed tiles;
- altra definizione.

Non usare “9x9” o “9 tile” in modo ambiguo.

Riportare la definizione dal codice/documentazione.

---

# 21. Verificare la workforce E06

Determinare con evidenza:

> quanti worker E06 aveva realmente.

Non assumere “multi-worker” = 4, 6 o altro.

Riportare:

- initial workers;
- hires;
- peak workers;
- timing;
- eventuale cap.

Questo può risolvere direttamente la contraddizione X1.1.

---

# 22. Verificare il costo HIRE

Leggere il costo direttamente dalle regole environment.

Verificare se la precedente affermazione:

> `cumulative hiring capital is very small`

è corretta.

Produrre la curva reale almeno per i primi worker rilevanti.

---

# 23. Possibile regressione E11

Verificare esplicitamente se la nuova `ProductiveMassROIAgent` ha perso una capacità presente in E06.

Confrontare:

- agent loop;
- action generation;
- worker selection;
- target assignment;
- movement;
- market handling;
- watering;
- harvest;
- planting.

Se emerge:

> **E11 architecture regression**

dichiararlo chiaramente.

---

# 24. Nessuna ottimizzazione durante l'audit

NON correggere il codice strategico mentre si analizza.

L'audit deve prima produrre una spiegazione causale.

Sono consentiti:

- script scratch;
- instrumentation;
- test diagnostici.

Non sono consentite modifiche strategiche per migliorare score.

---

# 25. Test suite

Se vengono aggiunti test diagnostici permanenti:

`.venv\Scripts\pytest.exe tests/`

Tutti devono passare.

---

# 26. Deliverable

Creare:

`docs/versions/E11_X1_1A_hire_constraint_e06_reconciliation.md`

---

# 27. Sezione obbligatoria — Facts vs Hypotheses

Nel report separare:

## VERIFIED FACTS

Solo dati supportati.

## HISTORICAL BUT NOT MACHINE-VERIFIED

Dati documentati ma senza raw evidence.

## HYPOTHESES

Interpretazioni ancora da testare.

---

# 28. Verdict HIRE

Rispondere esplicitamente:

> **Esiste davvero un hard-cap workforce dipendente dal numero di quadranti?**

YES / NO.

Se YES:

riportare la formula/regola.

Se NO:

spiegare perché X1.1 non assumeva.

---

# 29. Verdict E06

Rispondere:

> **Qual è il principale motivo verificabile per cui E06 produceva molto più di E11-VB1?**

Se non è possibile determinarlo:

> `INSUFFICIENT PRIMARY EVIDENCE`

Non inventare.

---

# 30. Decisione per X1.2

Solo dopo l'audit scegliere tra:

### A — se workforce cap confermato

`E11-X1.2 — 2-Worker Revenue Throughput Optimization`

### B — se workforce cap falso / HIRE bug

`E11-X1.2 — Corrected Pre-3Q Workforce Scaling`

### C — se emerge regressione E11 rispetto a E06

`E11-X1.2 — E06 Productive Mechanism Restoration`

### D — se emerge altro bottleneck

Definire trattamento specifico basato sull'evidenza.

---

# 31. Protocollo simulazioni

Questo audit deve essere economico.

Consentito:

- code inspection;
- dataset inspection;
- micro-test;
- massimo 1 smoke E06 se indispensabile.

NON eseguire:

- 5 episode benchmark;
- 10 episode benchmark;
- 30 episode benchmark;
- tutte le versioni storiche.

---

# 32. Aggiornamento documentazione

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato:

> **E11-X1.1A HIRE CONSTRAINT + E06 RECONCILIATION AUDIT COMPLETED — awaiting supervisor review**

---

# 33. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

NON:

- commit;
- tag;
- push;
- Kaggle submission.

---

# Deliverable finale obbligatorio

Riportare almeno:

1. Audit status
2. HIRE environment source file
3. Exact HIRE validation rule
4. Land/workforce relationship
5. HIRE cost curve
6. HIRE micro-test matrix
7. Workforce hard-cap verdict YES/NO
8. Exact reason X1.1 hires were rejected
9. E06 strategy identity
10. Meaning of E06 `9t`
11. E06 evidence provenance
12. E06 actual workforce
13. E06 hire timing
14. E06 active footprint
15. E06 crop portfolio
16. E06 action hierarchy
17. E06 watering behavior
18. E06 movement behavior
19. E06 economic result and evidence class
20. E11-VB1 corresponding metrics
21. E06 vs VB1 structural comparison
22. E06 vs VB1 worker-efficiency comparison
23. E06 vs VB1 early-revenue comparison
24. E06 vs VB1 crop lifecycle comparison
25. E06 vs VB1 capital allocation comparison
26. TOP competitor comparison
27. E06 ↔ VB1 ↔ TOP matrix
28. Verified reason for E06 performance advantage
29. Whether E11 introduced an architectural regression
30. Facts vs hypotheses separation
31. Recommended X1.2 branch
32. Simulations executed
33. Files created/modified
34. Test suite result
35. Next-step recommendation

---

# Regola metodologica finale

D'ora in avanti sfruttare sistematicamente i benchmark già disponibili come vincoli empirici.

Non limitarsi a confrontare:

> **current treatment vs current baseline**

quando esistono versioni storiche che hanno già dimostrato capacità produttive superiori.

In particolare, E06 deve funzionare come:

> **sanity benchmark interno**

mentre i top competitor costituiscono:

> **competitive benchmark esterno**

La strategia E11 deve spiegare contemporaneamente:

1. perché non riesce ancora a replicare la produttività interna già ottenuta in E06;
2. quale gap rimane successivamente rispetto ai top.

Prima recuperiamo la capacità produttiva già dimostrata internamente.

Solo dopo ottimizziamo verso i **$75k+** dei top.
