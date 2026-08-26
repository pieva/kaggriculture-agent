# E08-05 — REVIEW Productive Scale Optimization

## Contesto

Stiamo lavorando al progetto **Kaggriculture**, esperimento **E08 — Productive Scale Optimization**.

Stato:

- **E08-01 DEFINE**: completato e approvato;
- **E08-02 PLAN**: completato e approvato;
- **E08-03 BUILD**: completato e approvato;
- **E08-04 VERIFY**: completato con esito **`VERIFY FAIL — SUPERVISION REQUIRED`**;
- fase corrente: **E08-05 REVIEW**.

La REVIEW deve consolidare le evidenze prodotte da E08, verificare criticamente le interpretazioni formulate durante VERIFY e determinare quale ipotesi sia sufficientemente supportata per il successivo E09.

Questa fase è esclusivamente di analisi e documentazione.

**NON modificare la strategia.**
**NON iniziare E09.**
**NON inviare submission Kaggle.**

---

# Documenti e dati da esaminare

Leggi integralmente almeno:

- `docs/versions/E08_define_productive_scale.md`
- `docs/plans/E08_Productive_Scale_Optimization.md`
- `docs/versions/E08_plan_productive_scale.md`
- `docs/versions/E08_build_productive_scale.md`
- `docs/versions/E08_verify_functional_utilization.md`
- `docs/versions/E08_verify_local_performance.md`
- `docs/versions/E08_verify_competitive_evidence.md`
- `results/e08_productive_scale.json`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Per il confronto storico esamina inoltre i documenti e risultati disponibili di:

- E06;
- E07;

in particolare le evidenze relative a:

- Mean Final Money;
- superficie produttiva;
- workforce;
- movement;
- idle;
- livestock;
- crop mix;
- backlog;
- layout/geometria;
- differenze per opponent.

Non assumere valori non documentati.

---

# Obiettivo della REVIEW

La REVIEW deve rispondere a tre domande separate:

1. **Che cosa E08 ha effettivamente falsificato?**
2. **Quale nuovo collo di bottiglia è dimostrato dai dati e quale è soltanto ipotizzato?**
3. **Qual è la domanda sperimentale corretta per E09?**

È essenziale distinguere:

- evidenza osservata;
- interpretazione plausibile;
- ipotesi non ancora verificata.

Non trasformare correlazioni o osservazioni diagnostiche in causalità senza evidenza.

---

# R1 — Correzione della classificazione Functional Verify

Riesamina la classificazione:

> `FUNCTIONAL VERIFY PASS`

alla luce del requisito E08:

> **40 tile realmente produttive / 80% utilization**

I dati VERIFY riportano:

- 40 tile configurate;
- circa 23 tile attive al picco nell'episodio diagnostico;
- 16.33 tile attive/giorno in media nel diagnostico;
- circa 22.93 tile di picco medio nel benchmark;
- circa 13.84 tile attive/giorno in media nel benchmark;
- backlog `plant_pending` elevato.

Valuta formalmente se il risultato corretto debba essere:

- `FUNCTIONAL VERIFY PASS WITH WARNINGS`
oppure
- `FUNCTIONAL VERIFY FAIL`.

Non modificare retroattivamente i dati.

Se necessario, correggi soltanto la classificazione e l'interpretazione nei documenti.

La REVIEW deve esplicitare la distinzione:

> **40 configured ≠ 40 productive**

---

# R2 — Verifica del risultato economico

Conferma dai dati originali i risultati del benchmark E08.

Valori riportati:

- E08 Mean Final Money: **$11,880.30**
- E07 Mean Final Money nel benchmark paired utilizzato: **$13,320.37**
- delta: **-$1,440.07**
- delta percentuale: **-10.81%**

Verifica i calcoli direttamente dai risultati disponibili.

Controlla anche il riferimento E06.

Nel report VERIFY compare:

- E06 = **$24,987.67**

mentre in documentazione precedente era stato usato:

- E06 = **$25,180.30**

Determina perché esistono due valori.

Possibili spiegazioni da verificare:

- protocolli benchmark differenti;
- seed differenti;
- benchmark storico vs paired benchmark corrente;
- errore documentale.

NON scegliere arbitrariamente uno dei due.

Documenta quale valore è confrontabile con E08 e quale appartiene eventualmente a un protocollo diverso.

Lo stesso controllo va fatto per E07:

- baseline DEFINE/PLAN: **$15,364.57**
- benchmark paired VERIFY: **$13,320.37**

Spiega la differenza sulla base dei file e dei protocolli effettivi.

Questa riconciliazione è obbligatoria prima di definire E09.

---

# R3 — Analisi paired E07 vs E08

Esamina episodio per episodio il confronto paired.

La VERIFY riporta:

- E08 migliore: 4/30;
- uguale: 20/30;
- peggiore: 6/30.

Per opponent:

- `pass`: delta medio 0;
- `starter`: delta medio 0;
- `random`: regressione media E08 di circa $4,320.20 / -27.97%.

Verifica questi valori dai dati.

Poi analizza:

1. perché 20 episodi producono risultati identici;
2. quali condizioni distinguono i 4 miglioramenti dai 6 peggioramenti;
3. se l'espansione a 40 tile entra realmente in gioco in tutti gli episodi;
4. se la regressione contro `random` è associata a:
   - maggiore movement;
   - maggiore backlog;
   - differente espansione;
   - cash;
   - interferenza dell'opponent;
   - altro comportamento osservabile.

Non inventare causalità se la telemetria non consente di determinarla.

---

# R4 — Productive Scale hypothesis

Valuta formalmente l'ipotesi centrale E08:

> aumentare la superficie produttiva target da 24 a 40 tile, mantenendo invariata la workforce, dovrebbe migliorare il risultato economico sfruttando meglio il terreno acquistato.

Classifica l'ipotesi come:

- `SUPPORTED`
- `PARTIALLY SUPPORTED`
- `FALSIFIED`

La valutazione deve considerare contemporaneamente:

- tile configurate;
- tile realmente produttive;
- backlog;
- worker utilization;
- risultato economico.

Non basta il solo Final Money.

---

# R5 — Workforce sufficiency

Nel DEFINE era stata formulata l'ipotesi che 4 worker fossero sufficienti per 40 tile.

Riesaminala usando i dati reali:

- productive/action share;
- movement share;
- idle share;
- backlog;
- peak/mean productive tiles.

Distingui accuratamente:

> **numero assoluto di worker insufficiente**

da:

> **architettura/geometria/scheduling inefficiente per utilizzare quei worker**

I dati E08 da soli potrebbero non consentire di stabilire quale delle due cause sia dominante.

Se non è possibile distinguerle, dichiaralo esplicitamente.

NON concludere automaticamente che E09 debba aggiungere worker.

---

# R6 — Movement / dispersione geografica

Valuta il nuovo candidato a collo di bottiglia:

> **movement / dispersione geografica**

Evidenze riportate:

- movement share diagnostico circa 63.4%;
- movement share benchmark circa 61.6%;
- target diagnostico `<38%` non raggiunto;
- productive share circa 30%;
- elevato `plant_pending`.

Determina:

1. quanto è robusta questa evidenza;
2. se esiste una baseline E07 comparabile;
3. se è possibile confrontarla con E06;
4. se possiamo affermare causalità oppure soltanto forte associazione.

Classifica il finding come:

- `DEMONSTRATED BOTTLENECK`
- `STRONG CANDIDATE`
- `UNCONFIRMED HYPOTHESIS`

Motiva la classificazione.

---

# R7 — Cash / staggered purchasing

Verifica se liquidità e staggered purchasing sono stati un collo di bottiglia.

Dati riportati:

- minimum cash diagnostico: **$339**
- floor previsto: **$300**
- nessuna violazione attribuita agli acquisti sementi E08.

Valuta se:

- il cash floor ha impedito materialmente l'espansione;
- gli acquisti dilazionati hanno introdotto ritardi rilevanti;
- la liquidità può essere esclusa come causa dominante della regressione.

Classifica:

- `DOMINANT BOTTLENECK`
- `SECONDARY CONSTRAINT`
- `NOT MATERIAL IN E08`

---

# R8 — Livestock: verifica prima di concludere

La VERIFY contiene l'interpretazione:

> l'allevamento consuma circa il 40% dei turni totali per ritorni economici marginali.

Questa affermazione NON deve essere accettata automaticamente.

Verifica nei dati e nel codice diagnostico se esiste una decomposizione sufficientemente robusta dei turni tra:

- crop operations;
- livestock/feed operations;
- movement associato al livestock;
- movement associato alle colture;
- altre attività.

Verifica inoltre, se i dati lo consentono:

- ricavi attribuibili al livestock;
- costi feed;
- numero di azioni FEED;
- movimento generato dal feed loop;
- eventuale interferenza tra livestock e crop scheduling.

Se il valore "~40%" non è direttamente dimostrabile, correggi la documentazione e classifica l'ipotesi:

> **Livestock overhead is a major cause of the E07/E08 gap**

come:

- `SUPPORTED`
- `STRONG CANDIDATE`
- `UNCONFIRMED`

Non proporre la rimozione dell'allevamento come fatto già dimostrato se l'evidenza non è sufficiente.

---

# R9 — Confronto architetturale E06

E06 rimane il riferimento economico più forte.

Confronta E06 con E07/E08 soltanto usando metriche realmente disponibili e comparabili.

Costruisci una tabella concettuale con almeno:

| Dimensione | E06 | E07 | E08 | Evidenza |
|---|---|---|---|---|
| Mean Final Money | | | | |
| Productive scale | | | | |
| Workforce | | | | |
| Livestock | | | | |
| Layout density | | | | |
| Movement | | | | |
| Idle | | | | |
| Backlog | | | | |

Usa `N/A` quando una metrica non è disponibile.

Non colmare valori mancanti con stime.

Obiettivo:

> identificare quali differenze architetturali tra E06 ed E07/E08 meritano una verifica causale successiva.

---

# R10 — Decisione su E08

La REVIEW deve prendere una decisione esplicita su E08.

Valuta separatamente:

## Codice sperimentale

E08 deve essere:

- conservato come evidenza sperimentale;
- non cancellato;
- non sovrascritto.

## Strategia competitiva

Decidi se E08 deve essere:

- candidata a Kaggle;
- non candidata a Kaggle.

Alla luce dei risultati attuali, una candidatura richiede una motivazione eccezionale.

NON inviare comunque alcuna submission in questa fase.

---

# R11 — Direzione E09

Non implementare E09.

Definisci soltanto la **domanda sperimentale raccomandata**.

Evita automaticamente:

> "aggiungiamo worker"

perché E08 non dimostra ancora che il problema sia semplicemente il numero di worker.

Valuta invece se le evidenze supportano un E09 orientato a una **ablazione / semplificazione architetturale**.

Possibili dimensioni da considerare, senza implementarle:

- livestock overhead;
- feed loop;
- densità spaziale;
- superficie target;
- worker travel;
- dispatcher;
- confronto con proprietà architetturali E06.

La REVIEW deve proporre:

### Ipotesi E09 consigliata

Una sola ipotesi primaria, falsificabile.

### Variabile indipendente

Una sola modifica architetturale principale.

### Variabili congelate

Elenco delle componenti che E09 dovrebbe mantenere costanti.

### Baseline

Indicare quale versione usare come baseline primaria e perché.

### Metriche

Indicare le metriche minime necessarie a distinguere causalmente l'ipotesi.

NON creare ancora il piano E09.

---

# Deliverable

Crea:

`docs/versions/E08_review_productive_scale.md`

Struttura minima:

## 1. Executive Review
Esito sintetico E08.

## 2. Reconciliation delle baseline
Spiega le differenze:
- E06 $25,180.30 vs $24,987.67;
- E07 $15,364.57 vs $13,320.37.

## 3. Functional Review
- 40 configured vs productive;
- classificazione V1 corretta.

## 4. Economic Review
- E08 vs E07;
- paired analysis;
- opponent breakdown.

## 5. Bottleneck Analysis
Classifica separatamente:
- scale;
- workforce;
- movement/dispersion;
- backlog;
- cash;
- livestock.

Per ciascuno usa:
- `DEMONSTRATED`
- `STRONG CANDIDATE`
- `UNCONFIRMED`
- `NOT MATERIAL`

## 6. E06 Architectural Comparison
Tabella comparativa con soli dati verificabili.

## 7. Experimental Conclusions
Elenco delle ipotesi:
- confermate;
- falsificate;
- ancora aperte.

## 8. E08 Decision
Esplicita:
- conservazione codice/evidenze;
- candidatura o non candidatura Kaggle.

## 9. Recommended E09 Question
Una sola domanda sperimentale primaria con:
- ipotesi;
- variabile indipendente;
- variabili congelate;
- baseline;
- metriche.

---

# Aggiornamento stato

Aggiorna:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Inserisci:

- esito finale REVIEW E08;
- ipotesi falsificate;
- bottleneck dimostrati/candidati;
- riconciliazione baseline;
- decisione Kaggle;
- domanda raccomandata per E09.

NON dichiarare E09 avviato.

---

# Git

Esegui al termine:

```powershell
git status --short
git diff --stat
```

NON eseguire:

- `git commit`
- `git push`
- `git tag`

La gestione Git definitiva avverrà nella successiva fase SHIP/chiusura sperimentale.

---

# Output finale richiesto

Restituisci:

## E08-05 REVIEW Productive Scale Optimization

### 1. Esito E08
Sintesi.

### 2. Baseline reconciliation
E06 ed E07.

### 3. Functional conclusion
40 configured vs productive.

### 4. Economic conclusion
E08 vs E07.

### 5. Bottleneck classification
Tabella con evidenza e livello di confidenza.

### 6. Livestock finding
Indicare esplicitamente se il presunto overhead è dimostrato oppure no.

### 7. E06 comparison
Differenze architetturali verificabili.

### 8. Decisione E08
Kaggle / conservazione esperimento.

### 9. Raccomandazione E09
Una sola ipotesi sperimentale primaria.

### 10. Deliverable aggiornati
Elenco file.

### 11. Git status e diff
Output dei due comandi.

### 12. Decisione REVIEW

Usa una sola delle seguenti:

- `REVIEW COMPLETE — READY TO CLOSE E08`
- `REVIEW INCONCLUSIVE — SUPERVISION REQUIRED`

---

# STOP OBBLIGATORIO

Al termine:

**FERMATI.**

NON iniziare E09 DEFINE.

NON modificare la strategia.

NON effettuare rollback.

NON inviare E08 a Kaggle.

NON eseguire commit, push o tag.

Attendi esplicita approvazione prima della chiusura/SHIP di E08 e della successiva definizione di E09.
