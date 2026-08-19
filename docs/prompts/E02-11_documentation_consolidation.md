# E02 — Consolidamento documentale

La fase E02 è stata completata fino a:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW`

e le evidenze sono state consolidate nel repository.

Aggiorna ora esclusivamente:

`docs/PROJECT_STATE.md`

e:

`docs/EXPERIMENT_LOG.md`

in modo che rappresentino correttamente lo stato verificato del progetto dopo E02 e prima della fase SHIP.

Non modificare codice, risultati, submission o altri documenti.

## 1. Valori quantitativi definitivi da utilizzare

Utilizza esclusivamente i valori verificati dai dati grezzi persistenti.

### Baseline E01 definitiva

Da:

`results/e01_baseline.json`

utilizza:

* Mean Final Money E01: `$3567.63`;
* Median Final Money E01: `$3528.00`;
* Population Std Dev (`ddof=0`): `$201.93`;
* Sample Std Dev (`ddof=1`): `$205.38`;
* Overall Win Rate E01: `66.67%`;
* Win Rate vs `starter`: `0.00%`;
* Draw Rate vs `starter`: `100.00%`.

Per il confronto E01 → E02 utilizza:

`Mean Final Money E01 = $3567.63 ± $205.38`

dove `$205.38` è la deviazione standard campionaria.

Non utilizzare più:

* `$3578.80`;
* `$206.65`;
* `+63.66%`.

Se uno di questi valori compare nei due documenti da aggiornare, correggilo.

### Risultati E02 definitivi

Da:

`results/e02_roi_crop.json`

utilizza:

* Total Episodes: `30`;
* Completion Rate: `100.00%`;
* Disqualification Rate: `0.00%`;
* Overall Win Rate: `100.00%`;
* Win Rate vs `pass`: `100.00%`;
* Win Rate vs `random`: `100.00%`;
* Win Rate vs `starter`: `100.00%`;
* Mean Final Money: `$5857.17`;
* Median Final Money: `$5837.00`;
* Agent Mean Turn Latency: `0.0267 ms/turno`;
* Simulation Mean Step Duration: `3.45 ms/step`.

Per la dispersione E02 distingui:

* Population Std Dev (`ddof=0`): `$130.14`;
* Sample Std Dev (`ddof=1`): `$132.37`.

Per confronti statistici con E01, utilizza preferibilmente la deviazione standard campionaria.

### Miglioramento E01 → E02

Utilizza:

* incremento assoluto: `+$2289.53`;
* incremento percentuale: `+64.18%`;
* Win Rate vs `starter`: `0% → 100%`.

## 2. Interpretazione verificata di E02

Registra come interpretazione principale:

> E02 migliora principalmente perché la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.

Non descrivere il miglioramento come prova generale della superiorità della "dynamic crop selection".

Distingui chiaramente:

### Evidenza osservata

* `ROICropAgent` seleziona inizialmente `MELON`;
* `MELON` è Rank 1 sia usando il modello implementato `Yield=2` sia usando `max_yield`;
* i primi due raccolti completati nell'episodio osservato sono `MELON`;
* successivamente, nella parte finale della stagione, l'agente seleziona `STRAWBERRY`;
* il benchmark E02 raggiunge 100% di vittorie contro tutti gli avversari testati.

### Interpretazione

Il principale salto economico rispetto a E01 deriva dal passaggio dalla monocultura `CARROT` a una coltura molto più redditizia nelle condizioni osservate.

## 3. Limiti E02 da registrare

Inserisci sinteticamente i limiti emersi dall'analisi osservabile:

1. **End-of-Season Horizon**

   * l'agente può avviare una coltura che non maturerà prima della fine della stagione;

2. **Single-Tile Limitation**

   * viene utilizzata una sola casella `(4, 4)`;

3. **Immediate Selling**

   * il raccolto viene venduto immediatamente senza market timing;

4. **Yield Model Simplification**

   * la formula ROI utilizza `Yield=2`, mentre l'ambiente dispone di `max_yield` specifici per coltura.

Non scegliere quale di questi elementi diventerà E03.

## 4. Valutazione metodologica

Registra:

* Implementazione E02: `PASSED`;
* Isolamento sperimentale: `PASSED WITH OBSERVATIONS`;
* Benchmark E02: `PASSED`;
* Ipotesi E02: `SUPPORTATA nelle condizioni sperimentali testate`.

Per `PASSED WITH OBSERVATIONS`, documenta sinteticamente che durante BUILD è stato corretto `src/agricola/core/state.py` per allineare i parametri `CROPS` ai valori reali dell'ambiente.

Non descrivere questa modifica come invalidante per E01, poiché il comportamento effettivo di `CarrotLoopAgent` è rimasto invariato.

## 5. Aggiornamento di `docs/PROJECT_STATE.md`

Aggiorna il documento affinché rappresenti lo stato corrente.

La sezione `Current phase` deve indicare che:

* E01 è consolidata e costituisce la baseline;
* E02 è implementata, verificata e revisionata;
* SHIP E02 non è ancora stato eseguito.

Aggiorna la sezione relativa alle metriche includendo un confronto sintetico E01 → E02.

Inserisci un riferimento alle evidenze:

* `docs/versions/E02_build_antigravity.md`;
* `docs/versions/E02_verify_review_antigravity.md`;
* `docs/versions/E02_simulation_analysis.md`.

La sezione `Next step` deve indicare:

`E02 — SHIP: submission Kaggle reale, verifica del risultato esterno e successivo tag di versione.`

Non anticipare il risultato della submission Kaggle E02.

## 6. Aggiornamento di `docs/EXPERIMENT_LOG.md`

Mantieni integralmente la sezione E01 già consolidata.

Aggiungi una nuova sezione:

`## E02 — Dynamic Crop Selection & ROI Scaling`

con almeno:

* data;
* fase raggiunta;
* tool e modello;
* obiettivo;
* baseline E01 utilizzata;
* prompt E02 utilizzati;
* Implementation Plan;
* Human intervention;
* modifiche implementate;
* test;
* benchmark;
* VERIFY;
* REVIEW;
* analisi osservabile della simulazione;
* anomalie/discrepanze rilevate e corrette;
* valutazione metodologica;
* risultato sperimentale.

### Prompt da referenziare

Utilizza i riferimenti:

* `docs/prompts/E02-01_start.md`;
* `docs/prompts/E02-02_plan_review.md`;
* `docs/prompts/E02-03_plan_final_check.md`;
* `docs/prompts/E02-04_build_approval.md`;
* `docs/prompts/E02-05_verify.md`;
* `docs/prompts/E02-06_verify_review.md`;
* `docs/prompts/E02-07_verify_review_correction.md`;
* `docs/prompts/E02-08_simulation_analysis.md`;
* `docs/prompts/E02-09_simulation_analysis_review.md`;
* `docs/prompts/E02-10_simulation_analysis_correction.md`.

### Evidenze da referenziare

* `results/e02_roi_crop.json`;
* `docs/versions/E02_build_antigravity.md`;
* `docs/versions/E02_verify_review_antigravity.md`;
* `docs/versions/E02_simulation_analysis.md`.

### Human intervention

Documenta almeno:

* scelta e approvazione dell'evoluzione E02;
* review dell'Implementation Plan;
* approvazione esplicita di BUILD;
* review indipendente dei risultati;
* rilevazione della baseline E01 incoerente;
* ricostruzione dai dati grezzi;
* review dell'analisi della simulazione;
* correzione della ricostruzione economica.

## 7. Correzioni storiche

Non riscrivere retroattivamente la storia dell'esperimento per far sembrare che la baseline corretta fosse già nota durante PLAN.

Quando necessario, specifica che:

* PLAN E02 utilizzava inizialmente `$3578.80`;
* VERIFY ha rilevato che tale valore non era riproducibile da `results/e01_baseline.json`;
* REVIEW ha ricostruito la baseline persistente corretta pari a `$3567.63 ± $205.38`.

Questo passaggio è parte dell'evidenza metodologica dell'esperimento e deve rimanere visibile.

## 8. Vincoli

Modifica esclusivamente:

`docs/PROJECT_STATE.md`

`docs/EXPERIMENT_LOG.md`

Non modificare:

* codice sorgente;
* test;
* risultati JSON;
* submission;
* Implementation Plan;
* README;
* documenti in `docs/versions/`;
* prompt;
* screenshot.

Non eseguire benchmark.

Non effettuare submission Kaggle.

Non iniziare E03.

Non effettuare commit.

## 9. Al termine

Mostra:

1. sintesi delle modifiche a `PROJECT_STATE.md`;
2. sintesi della nuova sezione E02 in `EXPERIMENT_LOG.md`;
3. conferma che `$3578.80`, `$206.65` e `+63.66%` non siano più utilizzati come valori definitivi;
4. conferma dei valori:

   * E01 `$3567.63 ± $205.38`;
   * E02 `$5857.17`;
   * incremento `+64.18%`;
5. `git diff -- docs/PROJECT_STATE.md`;
6. `git diff -- docs/EXPERIMENT_LOG.md`;
7. `git status`;
8. fermati senza commit.

Attendi la revisione umana prima di procedere con SHIP E02.
