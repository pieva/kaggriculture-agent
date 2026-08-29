# E09-01 — DEFINE — Livestock Subsystem Ablation

## Contesto

Stiamo proseguendo il ciclo sperimentale del progetto **Kaggriculture**.

L'esperimento precedente, **E08 — Productive Scale Optimization**, è stato chiuso e versionato. La sua ipotesi è stata falsificata. E09 apre quindi una nuova linea sperimentale: invece di modificare ulteriormente lo scaling globale dell'agente, vogliamo isolare e misurare il contributo del sottosistema **livestock**.

Questa fase è esclusivamente **DEFINE**.

**Non implementare ancora E09-01. Non modificare il codice produttivo dell'agente. Non costruire una nuova submission. Non eseguire una submission Kaggle.**

L'obiettivo di questa fase è comprendere con precisione il comportamento corrente di E08, definire l'ablation e predisporre un piano sperimentale verificabile.

---

## Esperimento

**ID:** E09-01  
**Nome:** Livestock Subsystem Ablation  
**Tipo:** controlled ablation  
**Baseline:** E08 — Productive Scale Optimization

### Domanda sperimentale

> Quanto contribuisce il sottosistema livestock alla performance complessiva dell'agente E08?

L'esperimento deve confrontare la strategia E08 invariata con una variante E09-01 nella quale venga eliminato esclusivamente il comportamento riconducibile al livestock.

Lo scopo non è ancora migliorare direttamente la gestione del livestock.

Lo scopo è stabilire se il livestock:

1. produce un contributo netto positivo;
2. è sostanzialmente neutro;
3. oppure sottrae capitale, azioni, spazio o altre risorse alla componente crop/land senza generare un ritorno sufficiente.

---

## Ipotesi

### H0 — ipotesi nulla

La rimozione del sottosistema livestock non produce un miglioramento consistente della performance rispetto a E08.

### H1 — ipotesi sperimentale

La rimozione del sottosistema livestock produce un miglioramento consistente rispetto a E08.

Se H1 fosse supportata, avremmo evidenza che nell'attuale strategia il livestock ha un contributo netto negativo e che capitale, spazio e/o azioni potrebbero essere allocati più produttivamente altrove.

Un eventuale peggioramento di E09-01 sarebbe ugualmente informativo: costituirebbe evidenza che il livestock contribuisce positivamente alla strategia E08.

---

## Principio fondamentale: ablation controllata

E09-01 deve essere una vera ablation.

La futura implementazione dovrà modificare **una sola dimensione sperimentale**:

> livestock attivo in E08 → livestock disattivato in E09-01.

Tutto ciò che non è necessario per realizzare questa rimozione deve rimanere invariato.

In particolare, non introdurre contemporaneamente:

- nuove strategie di crop selection;
- nuove strategie di scaling;
- nuove soglie economiche;
- nuove priorità operative;
- nuove euristiche di movimento;
- nuove logiche di sfruttamento dello spazio;
- nuovi algoritmi di ROI;
- refactoring comportamentali non indispensabili;
- ottimizzazioni opportunistiche emerse durante l'analisi.

Se durante DEFINE emergono possibili miglioramenti ulteriori, documentarli come **esperimenti successivi**, senza incorporarli in E09-01.

---

# Attività richieste

## 1. Ricostruire lo stato corrente

Ispeziona il repository e identifica con precisione:

- commit HEAD;
- tag E08;
- classe/agente produttivo attualmente usato;
- entry point della submission;
- configurazione del benchmark locale;
- risultati E08 disponibili;
- documentazione E08;
- eventuali test specifici introdotti negli esperimenti precedenti.

Verifica che il working tree sia pulito prima di procedere.

Non assumere che la documentazione descriva perfettamente il codice: confronta documentazione, implementazione e test.

---

## 2. Audit completo del livestock in E08

Individua **tutti** i punti in cui E08 interagisce direttamente o indirettamente con il sottosistema livestock.

Non limitarti alla ricerca di un singolo comando o metodo.

Ricostruisci almeno:

- quali entità livestock esistono nell'environment;
- come vengono acquistate/ottenute;
- quali risorse consumano;
- quali prodotti generano;
- quali azioni richiedono;
- quali condizioni attivano tali azioni;
- quali celle/spazi occupano;
- quali vincoli introducono;
- come interagiscono con crop e terreno produttivo;
- come influenzano capitale e cash flow;
- se esistono dipendenze tra livestock e altre parti della strategia;
- se l'agente prende decisioni economiche esplicitamente basate sui prodotti livestock.

Cerca riferimenti nel codice, nei test, nei risultati e, se disponibile localmente, nell'API/environment Kaggriculture.

Produci una mappa sintetica del flusso:

`decisione → azione livestock → risorsa consumata → output → effetto economico/strategico`

---

## 3. Determinare il perimetro esatto dell'ablation

Definisci cosa significherà tecnicamente **"livestock disabled"**.

La definizione deve essere operativa e non ambigua.

Verifica quali comportamenti devono essere eliminati affinché E09-01 non investa deliberatamente nel livestock.

Ad esempio, determina se l'ablation richiede di impedire:

- acquisto/creazione di animali;
- alimentazione;
- raccolta di prodotti animali;
- vendita specifica di prodotti livestock;
- allocazione di spazio dedicato;
- altre azioni direttamente dipendenti dal livestock.

Non assumere che tutte queste operazioni esistano: ricavale dal codice e dall'environment.

Distingui inoltre tra:

### comportamento attivo

Azioni deliberate dell'agente che investono nel livestock.

### effetti passivi

Eventuali animali, prodotti o stati livestock già presenti nell'environment o generati indipendentemente dalle decisioni dell'agente.

E09-01 deve eliminare il **comportamento strategico attivo** verso il livestock senza alterare arbitrariamente lo stato dell'environment.

---

## 4. Identificare possibili confondenti

Analizza quali effetti secondari potrebbe produrre la rimozione del livestock.

In particolare verifica se può cambiare:

- capitale disponibile per semi/crop;
- numero di azioni disponibili;
- utilizzo delle celle;
- espansione territoriale;
- timing delle operazioni;
- inventory;
- vendita dei prodotti;
- priorità delle action class;
- movimento dell'agente;
- condizioni di fallback.

Questi effetti non sono necessariamente errori: possono essere proprio il meccanismo attraverso cui l'ablation produce il risultato.

Devono però essere documentati in modo da distinguere:

**effetto causale atteso della rimozione del livestock**

da

**modifica accidentale di un'altra strategia**.

---

## 5. Baseline quantitativa E08

Recupera dai risultati già presenti nel repository la baseline E08 da usare nel confronto.

Non inventare valori e non usare numeri provenienti da esperimenti precedenti se non corrispondono esattamente a E08.

Riporta almeno, se disponibili:

- numero di episodi;
- Mean Final Money;
- sample standard deviation (`ddof=1`);
- median;
- completion rate;
- disqualification rate;
- win/draw/loss;
- breakdown per opponent.

Se qualche metrica non è disponibile, dichiararlo esplicitamente.

Non rieseguire E08 soltanto per riempire dati mancanti durante DEFINE, salvo che sia strettamente necessario per comprendere la configurazione sperimentale. In tal caso fermati e segnalalo prima di trasformare DEFINE in un nuovo benchmark.

---

## 6. Disegnare il benchmark E09-01

Proponi un benchmark locale comparabile direttamente con E08.

La configurazione deve mantenere invariati, per quanto possibile:

- numero di episodi;
- opponent;
- distribuzione degli opponent;
- seed/reproducibility;
- numero massimo di step;
- timeout;
- metodo di aggregazione delle metriche.

L'obiettivo è rendere interpretabile:

`Δ = E09-01 − E08`

Calcolare nella futura fase VERIFY almeno:

- delta assoluto Mean Final Money;
- delta percentuale Mean Final Money;
- sample standard deviation;
- mediana;
- completion;
- disqualification;
- win/draw/loss;
- breakdown per opponent.

Valuta inoltre se sia possibile e utile usare **paired seeds / paired episodes** tra E08 ed E09-01. Se tecnicamente fattibile, preferire il confronto paired perché riduce il rumore sperimentale.

Non implementarlo ancora: descrivi la soluzione nel piano.

---

## 7. Criterio decisionale

Non definire il successo come:

> E09-01 Mean Final Money > E08 Mean Final Money

in modo puramente nominale.

Proponi un criterio che tenga conto almeno di:

- dimensione del delta;
- variabilità;
- consistenza tra opponent;
- eventuali outlier;
- regressioni di completion/disqualification;
- stabilità dell'effetto nei singoli episodi, soprattutto se è possibile un confronto paired.

Il DEFINE deve consentire, dopo VERIFY, una delle seguenti conclusioni:

### A — livestock negativo

E09-01 migliora in modo consistente → il livestock corrente distrugge valore.

### B — livestock positivo

E09-01 peggiora in modo consistente → il livestock corrente contribuisce positivamente.

### C — effetto non conclusivo / marginale

Differenze piccole o instabili → il contributo del livestock non può essere considerato determinante con l'evidenza disponibile.

Non forzare una soglia statistica arbitraria se la dimensione del campione o il disegno sperimentale non la giustificano.

---

## 8. Validazione Kaggle

La validazione Kaggle **non appartiene alla fase DEFINE**.

Nel piano indica soltanto che:

1. E09-01 dovrà superare BUILD e VERIFY locali;
2. solo successivamente verrà costruita la submission;
3. il confronto esterno sarà E09-01 vs E08;
4. il risultato Kaggle verrà interpretato come validazione esterna del comportamento osservato localmente.

Non tentare ora di accedere a Kaggle.

Non aprire browser.

Non inviare submission.

---

# Deliverable DEFINE

Crea un documento:

`docs/experiments/E09-01_Livestock_Subsystem_Ablation.md`

oppure utilizza la convenzione equivalente già adottata dal repository se la struttura corrente è diversa.

Il documento deve contenere almeno:

1. **Experiment ID e titolo**
2. **Contesto**
3. **Domanda sperimentale**
4. **H0 / H1**
5. **Baseline E08**
6. **Audit del comportamento livestock corrente**
7. **Definizione operativa dell'ablation**
8. **Variabile indipendente**
9. **Variabili controllate**
10. **Possibili confondenti**
11. **Metriche**
12. **Disegno del benchmark**
13. **Criterio decisionale**
14. **Rischi**
15. **Piano BUILD proposto**
16. **Piano VERIFY proposto**
17. **Condizioni per passare alla submission Kaggle**
18. **Questioni ancora aperte**

Aggiorna inoltre gli eventuali documenti di stato del progetto (`PROJECT_STATE.md`, `EXPERIMENT_LOG.md`, `NEW_SESSION.md` o equivalenti) **solo se la convenzione corrente prevede che il DEFINE venga registrato immediatamente**.

Non dichiarare E09-01 implementato o validato.

---

# Vincoli della fase

Durante E09-01 DEFINE:

- non modificare il comportamento produttivo;
- non implementare l'ablation;
- non cambiare `agent.py` della submission;
- non costruire una nuova submission;
- non eseguire benchmark completi E09-01;
- non accedere a Kaggle;
- non aprire browser;
- non fare commit/tag/push salvo istruzione successiva;
- non introdurre refactoring estranei;
- non correggere opportunisticamente altre strategie.

Sono consentiti:

- lettura del codice;
- lettura dei test;
- lettura dei risultati;
- lettura della documentazione;
- piccoli comandi diagnostici read-only;
- ispezione locale dell'environment/API, purché non alteri il codice produttivo;
- aggiornamento della documentazione DEFINE.

---

# Output finale richiesto ad Antigravity

Al termine, rispondi con un report sintetico ma completo contenente:

### 1. Stato iniziale
- branch;
- commit;
- tag E08 rilevato;
- working tree.

### 2. Audit livestock
- comportamento effettivamente trovato;
- file/classi/metodi coinvolti;
- risorse e azioni interessate;
- dipendenze con crop/land/economia.

### 3. Ablation proposta
Descrizione esatta di ciò che E09-01 disabiliterà e di ciò che rimarrà invariato.

### 4. Baseline E08
Metriche recuperate dal repository, con indicazione dei file sorgente.

### 5. Disegno sperimentale
Benchmark e metodo di confronto proposti.

### 6. Criterio decisionale
Come interpreteremo E09-01 rispetto a E08.

### 7. File modificati
Elenco dei soli file documentali eventualmente creati/modificati.

### 8. Questioni aperte
Qualsiasi elemento che debba essere deciso prima di BUILD.

### 9. Raccomandazione
Concludi esplicitamente con una delle due formule:

**READY FOR E09-01 BUILD**

oppure

**NOT READY FOR E09-01 BUILD**

motivando l'eventuale blocco.

---

## Principio metodologico finale

E09-01 non deve dimostrare che una nuova strategia è migliore.

Deve rispondere a una domanda più semplice e più importante:

> **Se togliamo il livestock da E08 e non cambiamo nient'altro, cosa succede?**

La qualità dell'esperimento dipende dalla capacità di mantenere invariato tutto il resto.
