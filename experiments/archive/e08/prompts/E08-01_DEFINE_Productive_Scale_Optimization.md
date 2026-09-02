# E08-01 — DEFINE Productive Scale Optimization

## Contesto

E07 ha completato una architettura competitiva più ampia. La validazione locale E07-08 l'ha classificata **ARCHITECTURALLY VALID, ECONOMICALLY WEAK**.

Dopo circa 5 ore dalla submission Kaggle:
- E05: **429.5**
- E06: **375.7**
- E07: **339.5**

Il valore iniziale 600.0 non è significativo. E07 è quindi circa -9.6% rispetto a E06 e -21.0% rispetto a E05.

I replay Kaggle mostrano inoltre che diversi agenti competitivi trasformano una quota sensibilmente maggiore del terreno disponibile in superficie produttiva. E07 compra Q1 ma mantiene un target di sole **24 productive tiles**, lasciando inutilizzata una quota consistente del terreno posseduto.

Questa fase deve definire una prima ottimizzazione controllata E08, da implementare e validare in tempo per una nuova submission questa sera.

## 1. Domanda sperimentale

> Il principale limite di E07 è il sottoutilizzo della superficie acquistata, e possiamo aumentare la scala produttiva senza distruggere l'efficienza operativa?

Usare come evidenza:
1. diagnostica locale E07;
2. replay Kaggle E07;
3. replay degli avversari forti già osservati;
4. meccaniche effettive dell'environment.

## 2. Principio sperimentale

E08 NON deve essere una nuova modifica multi-variabile.

Variabile strategica primaria:

> **PRODUCTIVE SCALE**

La workforce può cambiare soltanto se l'analisi dimostra che è una variabile dipendente strettamente necessaria per rendere eseguibile la nuova scala.

Congelare, salvo necessità tecnica dimostrata:
- livestock target;
- market policy;
- BUY_LAND timing;
- liquidation;
- feed policy;
- Water-First scheduling.

## 3. Misurare l'utilizzo reale E07

Produrre:

| Metric | E07 |
|---|---:|
| owned tiles after expansion | |
| target productive tiles | 24 |
| actually worked unique tiles | |
| planted unique tiles | |
| harvested unique tiles | |
| productive utilization / owned land | |
| Q0 utilization | |
| Q1 utilization | |
| worker productive % | |
| worker movement % | |
| worker idle % | |
| worker-days | |

Distinguere terreno posseduto, target, realmente lavorato e monetizzato.

## 4. Evidenza dai replay Kaggle

Usare le evidenze già raccolte. Non inventare conteggi esatti dalle immagini.

Classificare gli agenti osservati in:
- LOW productive utilization;
- MEDIUM productive utilization;
- HIGH productive utilization.

Quando osservabile registrare:
- final money;
- quadranti attivi;
- superficie produttiva approssimativa;
- livestock;
- workforce;
- strutture;
- terreno inattivo.

L'obiettivo è individuare un ordine di grandezza competitivo, non copiare un avversario.

## 5. Workforce bottleneck

Determinare se il limite delle 24 tile deriva da:
A. configurazione conservativa;
B. workforce insufficiente;
C. pathing inefficiente;
D. task priority;
E. combinazione.

Calcolare quando possibile:
- productive actions / worker-day;
- movement actions / worker-day;
- productive tiles / worker;
- harvests / worker.

## 6. Scenari candidati

Valutare SENZA implementarli:

### S0 — Control
24 productive tiles; workforce E07.

### S1 — Moderate
circa 32 productive tiles; workforce invariata se sostenibile.

### S2 — High
circa 40 productive tiles; workforce invariata o minimo incremento necessario.

### S3 — Near-full Q0+Q1
circa 48–50 productive tiles; workforce dimensionata solo se indispensabile.

Adattare i numeri alla geometria reale.

Per ogni scenario valutare qualitativamente:
- planting load;
- watering load;
- harvesting load;
- movement burden;
- capitale;
- rischio di colture incompiute.

Niente proiezioni monetarie arbitrarie.

## 7. Crop mix

E08 deve isolare la scala.

Mantenere per quanto possibile la logica crop E07. Per le tile aggiuntive estendere in modo esplicito e conservativo il mix cash-crop esistente.

NON aumentare automaticamente Wheat/feed.

La feed optimization resta un esperimento successivo.

## 8. Livestock

Mantenere target cows, sheep e feed logic E07.

Non aumentare livestock sulla base delle sole immagini degli avversari.

## 9. Land expansion

Mantenere il BUY_LAND timing E07 salvo evidenza che impedisca materialmente l'utilizzo della superficie.

Distinguere:
> comprare terreno

da:
> rendere produttivo terreno già comprato.

La seconda è la variabile E08.

## 10. Scelta E08

Scegliere UNA configurazione.

Preferire il maggiore incremento di productive scale ancora operativamente plausibile sulla base dei dati E07.

Se 40 tile sono gestibili con la workforce E07, 40 è più informativo di 32. Se E07 è già saturo a 24, non aumentare arbitrariamente senza affrontare workforce/pathing.

## 11. Success criteria

Confronto primario locale: **E08 vs E07**, stessi seed quando possibile.

Misurare:
- Mean Final Money;
- SD;
- Median;
- paired better/equal/worse;
- productive tiles;
- land utilization;
- worker productive %;
- worker movement %;
- terminal unused assets.

Successo architetturale:
> aumento sostanziale della superficie realmente produttiva senza regressioni di completion/disqualification.

Successo economico:
> Mean Final Money E08 > E07.

Target secondario:
> recuperare parte del gap verso E06/E05.

## 12. External validation successiva

Se E08 supera VERIFY, preparare successivamente una submission Kaggle E08 questa sera.

Il confronto sarà letto domani mattina dopo almeno circa 4 ore di assestamento. Non è necessario attendere 6 ore.

## 13. Deliverable

Creare:
`experiments/archive/e08/reports/E08_define_productive_scale.md`

Contenuti:
1. Evidence from E07
2. Kaggle E07 status
3. Competitive replay evidence
4. Productive-land gap
5. Workforce bottleneck analysis
6. Candidate scale scenarios
7. Selected E08 configuration
8. Variables frozen from E07
9. Variable changed in E08
10. Success criteria
11. Risks
12. PLAN recommendation

Decisione:
- `GO FOR PLAN`
- `REVISE E08 HYPOTHESIS`
- `INSUFFICIENT EVIDENCE`

Aggiornare:
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

NON modificare codice.
NON fare tuning.
NON costruire submission.
NON fare commit/push/tag.

Mostrare:
- configurazione E08 proposta;
- differenze esatte E07 → E08;
- motivazione quantitativa;
- `git status --short`;
- `git diff --stat`.

FERMARSI e attendere approvazione per PLAN.
