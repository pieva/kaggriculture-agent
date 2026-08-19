# E02 — SHIP Review e verifica del risultato Kaggle

La submission reale dell'iterazione **E02 — Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)** è stata completata sulla piattaforma Kaggle.

L'evidenza visiva è stata salvata come:

`docs/screenshots/E02-005_kaggle_submission_successful.png`

La schermata mostra:

- submission E02: `Complete`;
- score E02: `600.0`;
- descrizione riconducibile a `E02 supervised iteration: ROICropAgent...`.

Prima di consolidare definitivamente E02 e creare il tag di versione, esegui una **SHIP REVIEW** rigorosa.

L'obiettivo non è modificare o migliorare l'agente, ma verificare e documentare correttamente il risultato esterno ottenuto.

Non iniziare E03.

## 1. Verifica dell'evidenza Kaggle E02

Considera come evidenza esterna fornita dall'utente:

`docs/screenshots/E02-005_kaggle_submission_successful.png`

Verifica che quanto documentato sia coerente con:

- strategia E02: `ROICropAgent`;
- submission preparata in `submission/submission.py`;
- stato Kaggle: `Complete`;
- score Kaggle: `600.0`.

Distingui esplicitamente:

### Evidenza locale

Da `results/e02_roi_crop.json`:

- Mean Final Money: `$5857.17`;
- Overall Win Rate: `100.00%`;
- Win Rate vs `starter`: `100.00%`;
- incremento locale rispetto alla baseline E01 persistente: `+64.18%`.

### Evidenza esterna

Da Kaggle:

- submission E02 completata;
- score Kaggle E02: `600.0`.

Non assumere che lo score Kaggle rappresenti direttamente il capitale finale, il win rate locale o la stessa metrica del benchmark locale.

## 2. Verifica della discrepanza storica relativa a E01

Nello screenshot:

`docs/screenshots/E02-005_kaggle_submission_successful.png`

è visibile anche una precedente submission E01 identificabile dalla descrizione:

`E01 baseline — CarrotLoopAgent...`

con score:

`328.4`

Tuttavia nella documentazione corrente del repository è stato precedentemente registrato uno score E01 pari a:

`600.0`

Questa discrepanza deve essere investigata prima di consolidare SHIP E02.

Cerca nel repository tutte le evidenze persistenti relative alla submission Kaggle E01, in particolare:

- screenshot E01;
- `docs/PROJECT_STATE.md`;
- `docs/EXPERIMENT_LOG.md`;
- `README.md`;
- `docs/versions/E01_baseline.md`;
- `docs/versions/E01_verify_antigravity.md`;
- prompt E01;
- eventuali walkthrough;
- eventuali altri documenti che riportino score o submission Kaggle.

Ricostruisci una tabella cronologica delle evidenze disponibili indicando almeno:

| Evidenza | Submission/descrizione | Status | Score | Interpretazione possibile |
|---|---|---:|---:|---|

Non modificare ancora alcun documento.

## 3. Regola epistemica per E01

Non cercare di forzare una riconciliazione.

In particolare, non affermare senza evidenza che:

- `600.0` fosse necessariamente lo score E01;
- `328.4` fosse necessariamente lo score E01 definitivo;
- una delle due submission fosse un test;
- Kaggle abbia ricalcolato lo score;
- siano cambiate le regole della competizione;
- gli score appartengano a versioni differenti del codice;
- una submission abbia sostituito l'altra.

Sono tutte spiegazioni possibili soltanto se supportate da evidenza persistente.

Classifica alla fine la discrepanza E01 come una delle seguenti:

- `RESOLVED`;
- `PARTIALLY RESOLVED`;
- `UNRESOLVED`.

Motiva la classificazione esclusivamente sulla base delle evidenze disponibili.

## 4. Verifica del significato dello score Kaggle

Esamina le informazioni sulla competizione disponibili localmente e, se necessario, la configurazione/installazione locale di `kaggriculture` per capire che cosa sia possibile affermare sullo score.

Determina, se verificabile:

- quale metrica viene usata per lo scoring della competition;
- se `600.0` rappresenta un limite, un valore aggregato, un rating o altra metrica;
- se lo score è direttamente confrontabile con `Mean Final Money`;
- se il miglioramento locale `+64.18%` dovrebbe o non dovrebbe produrre necessariamente uno score Kaggle maggiore.

Se il significato preciso dello score non è verificabile dalle evidenze disponibili, dichiaralo esplicitamente.

Non dedurre il significato di `600.0` dal solo valore numerico.

## 5. Interpretazione del risultato E02

Valuta separatamente i due livelli di verifica.

### Benchmark locale

Il benchmark locale supporta, nelle condizioni sperimentali testate, che E02 migliori rispetto a E01:

`Mean Final Money: $3567.63 → $5857.17`

incremento:

`+$2289.53 (+64.18%)`

e:

`Win Rate vs starter: 0% → 100%`

### Kaggle

La submission esterna dimostra almeno che:

- l'agente E02 è accettato dalla piattaforma;
- completa la valutazione Kaggle;
- ottiene score `600.0`.

Non affermare che Kaggle confermi il miglioramento del `+64.18%` a meno che la metrica esterna consenta realmente tale confronto.

Formula quindi separatamente:

1. ciò che è dimostrato dal benchmark locale;
2. ciò che è dimostrato dalla submission Kaggle;
3. ciò che rimane non determinabile.

## 6. Verifica dello stato Git

Esegui:

`git status`

`git log -n 3 --oneline`

`git branch -vv`

Verifica che il repository sia ancora allineato al commit che precede il consolidamento finale di SHIP.

Non effettuare commit.

Non creare tag.

## 7. Nessuna modifica in questa fase

Questa è una fase di REVIEW.

Non modificare:

- `PROJECT_STATE.md`;
- `EXPERIMENT_LOG.md`;
- `README.md`;
- codice;
- test;
- risultati JSON;
- submission;
- Implementation Plan;
- documenti E01;
- documenti E02 esistenti.

Non correggere retroattivamente gli score E01.

Non creare ancora il tag:

`v0.2-e02-roicrop`

## 8. Evidenza persistente della SHIP REVIEW

Al termine crea esclusivamente:

`docs/versions/E02_ship_review_antigravity.md`

Il documento deve contenere:

1. evidenza Kaggle E02;
2. confronto tra evidenza locale ed esterna;
3. ricostruzione delle evidenze Kaggle E01;
4. analisi della discrepanza `600.0` / `328.4`;
5. classificazione della discrepanza E01;
6. ciò che è verificabile sul significato dello score Kaggle;
7. interpretazione metodologica del risultato E02;
8. eventuali questioni ancora aperte prima del consolidamento finale;
9. stato Git.

Non trasformare ipotesi in fatti.

## 9. Al termine

Mostra:

1. **E02 Kaggle result**
   - status;
   - score;
   - evidenza utilizzata.

2. **E01 score reconstruction**
   - tutte le evidenze persistenti trovate;
   - ordine cronologico;
   - classificazione `RESOLVED`, `PARTIALLY RESOLVED` o `UNRESOLVED`.

3. **Local vs Kaggle**
   - cosa dimostra il benchmark locale;
   - cosa dimostra Kaggle;
   - cosa non può essere concluso.

4. **SHIP assessment**
   - `PASSED`;
   - `PASSED WITH OBSERVATIONS`;
   - oppure `FAILED`;
   con motivazione.

5. conferma della creazione di:

   `docs/versions/E02_ship_review_antigravity.md`

6. output di:

   `git status`

7. fermati.

Non effettuare commit, push o tag.

Attendi la revisione umana prima del consolidamento finale di E02.
