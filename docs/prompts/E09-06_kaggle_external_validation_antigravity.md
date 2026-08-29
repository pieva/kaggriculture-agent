# E09-06 — Kaggle External Validation — Livestock Subsystem Ablation

## Stato approvato

La fase **E09-05 REVIEW**, incluso il correction pass E09-05B, è approvata.

Verdict sperimentale:

> **E09 HYPOTHESIS CONFIRMED**

Nell'architettura e nelle condizioni testate di E08, l'ablazione del sottosistema livestock produce un miglioramento causale molto forte.

### Evidenza locale primaria

**E08 — 40 tile — Livestock ON**
- Mean Final Money paired: **$11,468.53**
- Median: **$9,994.00**
- SD: **$6,643.06**
- Win Rate: **90.0%**

**E09-01 — 40 tile — Livestock OFF**
- Mean Final Money: **$22,899.20**
- Median: **$27,672.00**
- SD: **$7,892.99**
- Win Rate: **100.0%**

**Delta causale E09-01 − E08**
- Mean: **+$11,430.67**
- Relative: **+99.67%**
- Paired wins: **26/30**

### Confronto con E06 shipped baseline

**E06**
- Mean: **$24,731.37**
- Median: **$25,847.00**
- SD: **$1,859.19**

**E09-01**
- Mean: **$22,899.20**
- Median: **$27,672.00**
- SD: **$7,892.99**
- E09-01 batte E06 in **21/30 episodi**.

Il REVIEW ha diagnosticato una coda negativa seed/state-specific legata principalmente al **Q1 Land Expansion Cash Bottleneck del Giorno 12**.

Questa criticità verrà affrontata in un esperimento successivo.

**NON correggerla durante E09-06.**

---

# Decisione del supervisore

La precedente decisione di non inviare E09-01 a Kaggle è superata.

La decisione corrente è:

> **E09-01 SELECTED FOR KAGGLE EXTERNAL VALIDATION**

Motivazione:

1. E09-01 rappresenta una modifica sperimentale isolata e già verificata localmente;
2. l'ablazione livestock ha quasi raddoppiato la performance rispetto a E08;
3. E09-01 presenta un profilo diverso da E06: mediana e ceiling superiori ma maggiore varianza;
4. una validazione esterna prima di E10 consente di separare:
   - il contributo dell'ablazione livestock;
   - il futuro contributo della correzione del cash bottleneck;
5. E10 non deve confondere questi due effetti.

---

# Obiettivo di E09-06

Preparare una **submission Kaggle E09-01 tecnicamente identica alla strategia verificata localmente**, verificarne il package e predisporla per l'upload.

La strategia da validare deve essere:

> **E09-01 — 40 tile — Livestock OFF**

Non introdurre alcuna ottimizzazione.

---

# 1. Verifica iniziale

Prima di modificare qualsiasi file:

1. esegui `git status`;
2. esegui `git log -1 --oneline`;
3. verifica branch;
4. verifica il tag `v0.8-e08-productive-scale`;
5. verifica i file E09 modificati ma non ancora committati;
6. rileggi:
   - `docs/versions/E09_define_livestock_ablation.md`;
   - `docs/versions/E09_build_livestock_ablation.md`;
   - `docs/versions/E09_verify_local_performance.md`;
   - `docs/versions/E09_review_livestock_ablation.md`;
   - `src/agricola/strategy/livestock_ablation_roi.py`;
   - `src/agricola/agent.py`;
   - `scripts/build_submission.py`;
   - i test della submission.

Preserva tutte le modifiche E09 approvate.

Se trovi modifiche produttive estranee a E09-01, fermati.

---

# 2. Congelamento della strategia

Da questo momento E09-01 è **frozen for external validation**.

NON modificare:

- footprint da 40 tile;
- livestock OFF;
- workforce;
- hiring;
- Water-First;
- crop ratios;
- Q1 expansion;
- cash reserve;
- seed policy;
- worker partitioning;
- movement;
- liquidation;
- market policy;
- fallback;
- qualsiasi altra logica produttiva.

In particolare:

> NON implementare ancora il Q1 Expansion Capital Buffer.

La submission deve rappresentare esattamente la variante E09-01 già sottoposta al benchmark locale.

---

# 3. Entrypoint

Verifica quale strategia è attualmente esportata da:

`src/agricola/agent.py`

L'entrypoint precedente potrebbe ancora puntare alla baseline shipped E06.

Per la submission E09-01, modifica l'entrypoint **solo nella misura necessaria** affinché il package Kaggle utilizzi:

`LivestockAblationROIAgent`

o l'esatto identificatore della classe E09-01 già verificata.

Non duplicare la logica della strategia dentro `agent.py`.

L'entrypoint deve limitarsi alla corretta esposizione della strategia E09-01 secondo la convenzione del repository.

---

# 4. Test dopo il cambio entrypoint

Dopo il cambio controllato dell'entrypoint:

1. esegui i test E09-01;
2. esegui l'intera suite `pytest tests/`;
3. verifica i test specifici della submission;
4. verifica che il package non dipenda da:
   - `scratch/`;
   - risultati locali;
   - file non inclusi nella submission;
   - path assoluti;
   - moduli non disponibili nell'ambiente Kaggle.

Tutti i test devono passare.

Se un test fallisce:

> fermati e correggi esclusivamente problemi di packaging/entrypoint, senza modificare il comportamento strategico.

---

# 5. Build della submission

Usa lo script ufficiale del repository:

`python scripts/build_submission.py`

o il comando equivalente già documentato.

Verifica il contenuto prodotto.

La submission deve:

- includere E09-01;
- esportare l'entrypoint corretto;
- non includere accidentalmente strategie sperimentali inutili;
- non dipendere da file locali;
- rispettare i requisiti Kaggriculture;
- essere riproducibile dal repository.

Non alterare `build_submission.py` salvo problema tecnico dimostrato.

---

# 6. Test del package

Esegui tutti i test già previsti dal repository per la submission, incluso, se esistente:

`pytest tests/test_submission.py`

Verifica almeno:

- import corretto;
- entrypoint disponibile;
- assenza di dipendenze mancanti;
- package autocontenuto;
- dimensione/formato accettabili;
- nessuna regressione rispetto ai requisiti Kaggle.

Se esiste una verifica locale dell'agente costruito dalla submission, eseguila.

Non usare tale smoke test come nuova evidenza prestazionale.

---

# 7. Identità della submission

Prima dell'upload, registra chiaramente:

```text
Experiment: E09-01
Variant: Livestock Subsystem Ablation
Footprint: 40 tile
Livestock: OFF
Local Mean: $22,899.20
Local Median: $27,672.00
Primary causal baseline: E08 paired
External validation target: Kaggle
```

Suggerisci una descrizione Kaggle breve e inequivocabile, ad esempio:

`E09-01 Livestock Ablation — 40t Livestock OFF`

Non confondere E09-01 con E10 o con una versione capital-buffer.

---

# 8. Upload Kaggle

## Vincolo operativo

Non tentare automazioni fragili del browser.

Non aprire ripetutamente finestre del browser.

Non tentare login automatici non configurati.

Se l'accesso Kaggle via CLI/API non è già configurato e funzionante nel repository, prepara il file e **fermati chiedendo al supervisore l'upload manuale**.

Se invece esiste già un workflow Kaggle verificato e funzionante, puoi utilizzarlo solo se non richiede modifiche alle credenziali o procedure non documentate.

In ogni caso:

- non inventare score;
- non dichiarare submission riuscita senza evidenza;
- non dichiarare ranking prima che Kaggle lo mostri.

---

# 9. Evidenza da richiedere al supervisore

Dopo l'upload manuale, attendi uno screenshot o un risultato Kaggle che mostri almeno:

- submission E09-01 accettata;
- stato della submission;
- score/ranking quando disponibile.

Non interpretare uno score ancora in assestamento come definitivo.

---

# 10. Confronto esterno

Quando il risultato sarà disponibile, il confronto principale dovrà includere almeno:

- E06 shipped baseline;
- E07;
- E08;
- E09-01.

Non assumere che la metrica Kaggle sia linearmente confrontabile con `Mean Final Money` locale.

La domanda esterna è:

> **L'ablazione livestock che ha prodotto un forte miglioramento locale rispetto a E08 migliora anche il comportamento competitivo osservato su Kaggle?**

---

# 11. Monitoraggio

Dopo una submission Kaggle valida, non dichiarare immediatamente concluso il confronto se il ranking/score è ancora in assestamento.

Utilizza il normale criterio operativo del progetto per osservare la stabilizzazione del divario tra submission.

Non modificare E09-01 durante il monitoraggio.

Non iniziare E10 mentre stai ancora raccogliendo l'evidenza necessaria a interpretare E09, salvo decisione esplicita del supervisore.

---

# 12. Documentazione

Crea:

`docs/versions/E09_kaggle_external_validation.md`

Documenta almeno:

1. stato locale E09-01;
2. motivazione della validazione esterna;
3. commit/working state corrente;
4. entrypoint selezionato;
5. test eseguiti;
6. build della submission;
7. identificazione del package;
8. modalità di upload;
9. eventuale submission ID/nome;
10. score Kaggle quando disponibile;
11. confronto con E06/E07/E08;
12. stato di stabilizzazione;
13. conclusione, solo quando supportata.

Aggiorna:

- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`;

senza dichiarare E09 SHIPPED finché la validazione esterna non è stata interpretata e approvata.

---

# 13. Git

Prima dell'upload puoi:

- eseguire `git status`;
- eseguire `git diff`;
- eseguire test;
- costruire la submission.

NON fare ancora:

- commit;
- push;
- tag.

La chiusura Git appartiene alla successiva fase SHIP.

---

# 14. Stato intermedio corretto

Dopo build e test, ma prima del risultato Kaggle, lo stato deve essere:

> **E09-06 EXTERNAL VALIDATION — SUBMISSION READY**

oppure, dopo upload confermato:

> **E09-06 EXTERNAL VALIDATION — KAGGLE SUBMITTED / MONITORING**

Non usare:

> E09 SHIPPED

finché non viene autorizzato.

---

# STOP OBBLIGATORIO — PRIMA DELL'UPLOAD MANUALE

Se la submission è pronta ma Kaggle richiede intervento manuale:

**FERMATI.**

Restituisci il percorso esatto del file da caricare e la descrizione da usare.

Attendi che il supervisore effettui l'upload e fornisca evidenza del risultato.

---

# STOP OBBLIGATORIO — DOPO L'UPLOAD

Se l'upload è stato effettuato:

**FERMATI DOPO AVER REGISTRATO L'EVIDENZA DISPONIBILE.**

NON:

- modificare E09-01;
- implementare E10;
- modificare capital reserve;
- modificare seed policy;
- modificare footprint;
- fare commit/push/tag;
- dichiarare E09 chiuso senza approvazione.

---

# Output finale richiesto ad Antigravity

## 1. Stato iniziale
- branch;
- HEAD;
- working tree;
- tag E08.

## 2. Frozen candidate
Conferma che il candidato è:

> **E09-01 — 40 tile — Livestock OFF**

e che nessuna logica sperimentale è stata modificata.

## 3. Entrypoint
Indica esattamente cosa esporta `src/agricola/agent.py` dopo la preparazione.

## 4. Test
Riporta:

- test E09;
- full regression suite;
- submission tests;
- eventuale package smoke test.

## 5. Submission build
Riporta:

- comando usato;
- file prodotto;
- dimensione;
- contenuto/entrypoint verificato.

## 6. Kaggle status
Una sola delle seguenti:

**SUBMISSION READY — MANUAL UPLOAD REQUIRED**

oppure

**KAGGLE SUBMITTED — MONITORING REQUIRED**

oppure

**EXTERNAL VALIDATION BLOCKED**

con motivazione.

## 7. Descrizione Kaggle
Riporta la descrizione esatta consigliata:

> `E09-01 Livestock Ablation — 40t Livestock OFF`

## 8. File modificati
Elenco completo.

## 9. Next action
Indica esattamente cosa deve fare il supervisore.

---

# Principio metodologico finale

E09-06 non serve a migliorare E09-01.

Serve a misurare esternamente **la variante già verificata**.

La separazione sperimentale deve restare:

```text
E08
40 tile + Livestock ON
        |
        | E09: Livestock Ablation
        v
E09-01
40 tile + Livestock OFF
        |
        | Kaggle external validation
        v
External evidence
        |
        | solo successivamente
        v
Future experiment:
Q1 expansion capital protection
```

Qualsiasi modifica al cash buffer prima della submission renderebbe impossibile attribuire il risultato Kaggle alla sola ablazione livestock.
