# E11 — DEFINE — 3× Productive Mass Expansion

## Contesto

Stiamo sviluppando l'agente per la competizione Kaggle **Kaggriculture**.

Gli esperimenti precedenti hanno prodotto miglioramenti e verificato diverse ipotesi di ottimizzazione, ma le osservazioni delle simulazioni Kaggle mostrano ancora una differenza strutturale rispetto ai player di vertice.

In particolare, i top player sembrano:

- utilizzare una porzione significativamente maggiore del terreno disponibile;
- sviluppare una workforce più ampia;
- utilizzare una maggiore varietà di crop;
- utilizzare livestock e/o altri prodotti in misura maggiore;
- reinvestire più aggressivamente il capitale;
- raggiungere una massa produttiva ed economica finale molto superiore alla nostra.

Dalle osservazioni preliminari, la differenza di scala sembra essere nell'ordine di circa **3×**.

**Questo valore NON è ancora un target E11 validato.**

Il **3× è un'ipotesi empirica derivata dall'osservazione delle partite e deve essere verificata quantitativamente** prima di definire il target dell'esperimento.

E11 rappresenta inoltre un cambio di impostazione rispetto alle iterazioni precedenti:

> **prima raggiungere una massa produttiva comparabile a quella dei top player; successivamente ottimizzare l'efficienza.**

Non vogliamo quindi realizzare semplicemente una variante più aggressiva di E10 o continuare con correzioni marginali dei parametri esistenti.

---

# Obiettivo di questo task

Eseguire esclusivamente la fase **DEFINE di E11**, iniziando con un benchmark quantitativo della scala raggiunta dai player di vertice.

Non implementare ancora E11.

Non modificare ancora la policy dell'agente.

Non assumere che 3× sia corretto.

Il lavoro deve stabilire:

1. quale sia effettivamente la massa produttiva/economica dei top player osservabili;
2. quale sia il gap rispetto alla nostra configurazione corrente;
3. se l'ipotesi preliminare **3×** sia confermata, corretta o falsificata;
4. quali siano le principali differenze strutturali che sembrano spiegare il gap;
5. quale target quantitativo debba essere utilizzato successivamente per E11.

---

# 1. Ricostruzione dello stato corrente

Prima di effettuare il benchmark:

- leggere `README.md`;
- leggere `PROJECT_STATE.md`;
- leggere `EXPERIMENT_LOG.md`;
- leggere `NEW_SESSION.md`;
- esaminare la documentazione degli esperimenti E07, E08, E09 ed E10 disponibile nel repository;
- identificare con precisione quale configurazione rappresenti attualmente il riferimento;
- recuperare le metriche disponibili della configurazione corrente;
- verificare quali dati siano realmente confrontabili con quelli osservabili nelle simulazioni Kaggle.

Non modificare i valori storici documentati.

Se emergono incongruenze tra documentazione, risultati e codice, segnalarle esplicitamente.

---

# 2. E11-B0 — Top Player Benchmark

Effettuare una ricognizione quantitativa dei player di vertice utilizzando esclusivamente dati effettivamente osservabili o ricavabili dall'ambiente Kaggriculture.

L'obiettivo NON è ancora replicare la loro strategia.

L'obiettivo è misurarne la **scala produttiva**.

Quando possibile, raccogliere per i top player almeno le seguenti dimensioni.

| Dimensione | Misura richiesta |
|---|---|
| Massa economica | money/revenue osservabile e relativo ordine di grandezza |
| Terreno | tile possedute e/o effettivamente utilizzate |
| Utilizzazione terreno | quota indicativa del terreno produttivamente sfruttato |
| Workforce | numerosità e crescita |
| Crop | numero di crop differenti e loro distribuzione |
| Livestock | presenza, quantità e sviluppo |
| Products | varietà di prodotti utilizzati |
| Reinvestimento | evidenza di reinvestimento del capitale |
| Espansione | timing e intensità dell'espansione |
| Production ramp | velocità apparente di crescita della capacità produttiva |
| End-game | comportamento nella fase finale dell'episodio |

Non inventare dati che l'ambiente non consente di osservare.

Per ogni metrica indicare chiaramente se si tratta di:

- **dato direttamente osservato**;
- **dato calcolato**;
- **proxy**;
- **stima visiva**;
- **dato non disponibile**.

---

# 3. Analisi temporale

Se i dati disponibili lo consentono, evitare di confrontare soltanto lo stato finale.

Rilevare alcuni checkpoint della partita, preferibilmente:

- 25% dell'episodio;
- 50%;
- 75%;
- 100%.

Per ogni checkpoint osservare almeno, quando disponibili:

- money/revenue;
- terreno;
- workforce;
- crop attivi;
- livestock;
- prodotti;
- livello complessivo di utilizzazione della capacità produttiva.

Lo scopo è capire **quando** nasce il vantaggio dei top player.

Distinguere, se possibile:

> accumulo iniziale → espansione → aumento workforce → diversificazione → produzione → reinvestimento → ulteriore espansione.

Non assumere a priori che questa sia necessariamente la sequenza effettiva: deve essere verificata dalle osservazioni.

---

# 4. Verifica dell'ipotesi 3×

Formalizzare la seguente ipotesi:

> **H11 — Productive Mass Gap:** le osservazioni preliminari suggeriscono che i player di vertice raggiungano una massa produttiva/economica nell'ordine di circa 3× rispetto alla nostra configurazione corrente.

Calcolare il rapporto effettivo utilizzando le metriche confrontabili disponibili.

Il risultato deve classificare H11 come:

- **confermata**, se il rapporto osservato è ragionevolmente compatibile con 3×;
- **parzialmente confermata**, se esiste un forte gap ma di dimensione significativamente diversa;
- **falsificata**, se il benchmark non mostra un gap di questa natura.

Non adattare i dati per confermare 3×.

Se dimensioni differenti producono rapporti differenti — ad esempio 3× revenue ma 2× terreno e 4× workforce — mantenerle separate.

---

# 5. Analisi del gap strutturale

Dopo la misurazione quantitativa, identificare quali differenze sembrano maggiormente associate alla maggiore scala dei top player.

Considerare almeno:

### Terreno

Verificare se i top player utilizzano sistematicamente più spazio produttivo.

### Workforce

Verificare se una workforce maggiore precede o accompagna l'espansione.

### Crop mix

Verificare se la diversificazione delle colture appare strutturale oppure marginale.

### Livestock

Verificare se livestock costituisce una componente significativa della strategia produttiva.

### Products

Verificare se vengono sfruttate più catene/prodotti rispetto alla nostra strategia.

### Reinvestimento

Verificare se il capitale viene reinvestito più rapidamente invece di essere conservato.

### Sequenza di crescita

Cercare di identificare se esiste una sequenza ricorrente di investimento ed espansione.

Separare sempre:

**evidenza osservata → interpretazione → ipotesi da testare.**

---

# 6. Evitare l'ottimizzazione prematura

E11 nasce dall'osservazione che le iterazioni precedenti rischiano di produrre miglioramenti marginali mentre permane un gap molto maggiore nella **massa produttiva complessiva**.

Durante il DEFINE non utilizzare quindi come criterio principale:

- ROI per singola tile;
- minimizzazione della workforce;
- massimizzazione del cash disponibile nel breve periodo;
- scelta del solo crop localmente più redditizio;
- riduzione degli investimenti;
- micro-ottimizzazioni della policy corrente.

Queste metriche rimangono utili come diagnostica, ma non devono impedire di studiare strategie capaci di raggiungere una scala significativamente maggiore.

Il principio da verificare è:

> **Mass first, efficiency second.**

Questo principio è anch'esso un'ipotesi sperimentale, non una conclusione già dimostrata.

---

# 7. Definizione del target E11

Solo dopo il benchmark proporre il target quantitativo dell'esperimento E11.

Il target NON deve essere fissato preventivamente a:

- 3×;
- 50k;
- 60k;
- qualsiasi altro valore derivato esclusivamente dalle osservazioni preliminari.

Deve essere ricavato dai risultati di E11-B0.

Proporre almeno:

### Baseline

Valore della nostra configurazione corrente utilizzato per il confronto.

### Top-player benchmark

Valore o intervallo osservato per i player di vertice.

### Gap

Rapporto:

`top-player benchmark / current baseline`

### E11 primary target

Target quantitativo realistico per la prima iterazione di Productive Mass Expansion.

### Stretch target

Livello che permetterebbe di considerare sostanzialmente colmato il gap di massa critica.

Specificare esattamente quale metrica viene utilizzata.

---

# 8. Output richiesto

Produrre un documento:

`experiments/archive/e11/reports/E11_define_productive_mass_expansion.md`

Il documento deve contenere almeno:

1. **Executive Summary**
2. **Baseline corrente**
3. **Metodo di benchmark**
4. **Top Player Benchmark**
5. **Analisi temporale**
6. **Verifica dell'ipotesi 3×**
7. **Gap analysis**
8. **Terreno**
9. **Workforce**
10. **Crop diversification**
11. **Livestock e products**
12. **Reinvestment dynamics**
13. **Evidenze vs interpretazioni**
14. **Target quantitativo proposto per E11**
15. **Primary target**
16. **Stretch target**
17. **Rischi e dati mancanti**
18. **Decisione DEFINE**
19. **Ipotesi da portare alla fase PLAN**

Inserire tabelle quantitative quando i dati lo consentono.

---

# 9. Aggiornamento della documentazione

Al termine aggiornare, se appropriato:

- `PROJECT_STATE.md`;
- `EXPERIMENT_LOG.md`;
- `NEW_SESSION.md`.

Registrare E11 come:

**E11 — 3× Productive Mass Expansion**

ma specificare esplicitamente che:

> **“3×” nasce da un'osservazione preliminare ed è sottoposto a verifica nel benchmark E11-B0.**

Non presentarlo come risultato acquisito.

---

# 10. Vincoli

In questa fase:

- NON implementare una nuova policy;
- NON modificare `agent.py` per introdurre E11;
- NON costruire una nuova submission;
- NON lanciare una submission Kaggle;
- NON ottimizzare parametri E10;
- NON assumere 3× come target;
- NON inventare informazioni non osservabili;
- NON trasformare proxy o stime visive in dati misurati;
- NON effettuare commit/tag finale di E11 come esperimento completato.

Se il benchmark non può essere effettuato automaticamente con gli strumenti disponibili, documentare esattamente:

1. quali informazioni mancano;
2. quali possono essere ottenute dal replay/visualizzatore;
3. quali osservazioni devono essere raccolte manualmente;
4. quale procedura riproducibile deve seguire l'utente per raccoglierle.

In questo caso predisporre il necessario per rendere la raccolta manuale **minima, strutturata e quantitativamente utilizzabile**.

---

# Deliverable finale

Al termine fermarsi e presentare:

1. risultato sintetico del benchmark;
2. baseline utilizzata;
3. livello osservato dei top player;
4. rapporto effettivo rispetto alla baseline;
5. verdetto sull'ipotesi **3×**;
6. principali driver del gap;
7. target E11 proposto;
8. stretch target;
9. dati mancanti o limiti del benchmark;
10. file creati/modificati;
11. proposta per la successiva fase **PLAN**.

**Non procedere alla PLAN senza approvazione.**