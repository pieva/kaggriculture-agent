# E04-01 — Competitive Gap Analysis

## Obiettivo

Il progetto ha completato e consolidato E03 (`MultiTileROIAgent`).

Prima di definire la strategia di E04, eseguire una **Competitive Gap Analysis** dell'agente corrente e dell'ambiente Kaggriculture.

Il progetto segue il metodo sperimentale supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Le iterazioni completate sono:

- **E01** — baseline operativa;
- **E02** — selezione dinamica della coltura basata sul ROI/giorno;
- **E03** — scaling produttivo multi-tile mediante cluster compatto 2×2.

E03 ha prodotto un miglioramento molto rilevante nel benchmark locale controllato:

- E02 Mean Final Money: `$5857.17`;
- E03 Mean Final Money: `$14682.47`;
- miglioramento: `+150.68%`;
- Completion Rate: `100%`;
- Disqualification Rate: `0%`;
- Overall Win Rate locale: `100%`.

Le evidenze Kaggle attualmente osservate mostrano però un miglioramento competitivo molto più contenuto:

- E02 Kaggle score attualmente osservato: circa `282.3`;
- E03 Kaggle score attualmente osservato: circa `294.4`;
- posizione E03 attualmente osservata nel leaderboard: circa `#5642`.

La domanda principale non è quindi più:

> Come possiamo aumentare ulteriormente il reddito della farm nel benchmark locale?

La domanda diventa:

> Quali meccaniche competitive rilevanti di Kaggriculture sono attualmente ignorate, semplificate o sfruttate in modo insufficiente da `MultiTileROIAgent`?

---

## Vincolo fondamentale

Questa attività costituisce esclusivamente una fase di **DEFINE / investigazione**.

Non modificare l'agente.

Non implementare E04.

Non creare ancora un Implementation Plan per E04.

Non assumere che le candidate già individuate siano necessariamente le strategie corrette per la prossima iterazione.

Lo scopo è identificare il principale **competitive gap** tra la strategia E03 e le capacità effettivamente offerte dall'ambiente Kaggriculture.

---

## 1. Ricognizione dello stato corrente del progetto

Esaminare la documentazione e il codice rilevanti presenti nel repository, includendo almeno:

- `README.md`;
- `PROJECT_STATE.md`, nella posizione effettivamente presente nel repository;
- `NEW_SESSION.md`, nella posizione effettivamente presente nel repository;
- documentazione sperimentale relativa a E01, E02 ed E03;
- implementazione corrente di E03;
- script di valutazione;
- test;
- eventuali script disponibili per l'ispezione o la diagnostica dell'ambiente;
- risultati registrati.

Prima di formulare conclusioni, ricostruire e confermare il comportamento effettivo di E03.

Non assumere che la documentazione sia sufficiente: confrontarla con l'implementazione corrente quando necessario.

---

## 2. Audit dell'ambiente Kaggriculture

Esaminare l'ambiente/API effettivamente disponibile nel repository e determinare l'insieme completo delle meccaniche strategicamente rilevanti esposte all'agente.

### 2.1 Observation space

Identificare quali informazioni l'agente può osservare relativamente almeno a:

- propria farm;
- denaro e liquidità;
- inventario;
- colture disponibili;
- stato delle colture;
- maturazione;
- prezzi di mercato;
- tempo;
- turno corrente;
- orizzonte residuo;
- proprietà dei terreni;
- altri player;
- farm degli altri player;
- azioni degli altri player, se osservabili;
- stato del mercato;
- eventuale stato globale condiviso;
- qualsiasi altra informazione strategicamente rilevante.

Per ogni elemento distinguere esplicitamente tra:

1. **informazione disponibile all'agente**;
2. **informazione attualmente utilizzata da E03**;
3. **informazione disponibile ma ignorata da E03**.

Non dedurre l'esistenza di informazioni non verificate nell'ambiente.

---

### 2.2 Action space

Identificare tutte le azioni disponibili all'agente e classificarle come:

- utilizzate da E03;
- utilizzate solo parzialmente;
- mai utilizzate.

Prestare particolare attenzione alle meccaniche relative a:

- produzione agricola;
- acquisto;
- vendita;
- movimento;
- irrigazione;
- inventario;
- acquisizione di nuovi terreni;
- mercato;
- interazione o competizione con altri player;
- timing delle decisioni;
- qualsiasi azione disponibile ma non rappresentata nella strategia E03.

Non dedurre la semantica delle azioni esclusivamente dal loro nome.

Quando possibile, verificarne il comportamento effettivo attraverso codice, configurazione o documentazione dell'ambiente.

---

## 3. Ricostruzione dell'obiettivo competitivo

Determinare, sulla base dell'ambiente e delle evidenze disponibili nel progetto, quali elementi determinano effettivamente il successo in Kaggriculture.

Distinguere chiaramente tra:

- Final Money;
- performance relativa rispetto agli avversari;
- condizioni di vittoria e sconfitta;
- reward dell'ambiente;
- valutazione Kaggle;
- Skill Rating o altro score Kaggle osservabile.

Individuare esplicitamente eventuali assunzioni del benchmark locale che potrebbero non rappresentare adeguatamente la valutazione competitiva Kaggle.

Non formulare ipotesi come fatti relativamente a meccanismi interni di Kaggle non documentati o non osservabili.

Tutto ciò che non può essere stabilito attraverso le evidenze disponibili deve essere classificato come:

**UNKNOWN**

---

## 4. Audit strategico di E03

Ricostruire `MultiTileROIAgent` come una vera e propria **decision policy**.

Per ciascuna decisione significativa determinare:

- quali informazioni vengono osservate;
- quale regola decisionale viene applicata;
- quali informazioni disponibili vengono ignorate;
- se la regola è statica oppure adattiva;
- se reagisce agli avversari;
- se reagisce all'evoluzione del mercato;
- se considera l'orizzonte temporale residuo;
- se modifica la strategia in funzione dello stato competitivo.

Identificare inoltre:

- assunzioni hard-coded;
- soglie fisse;
- semplificazioni;
- comportamenti deterministici;
- informazioni disponibili ma non utilizzate.

L'obiettivo non è soltanto descrivere **che cosa fa E03**, ma stabilire **che tipo di strategia rappresenta E03**.

---

## 5. Analisi della divergenza locale/Kaggle

Analizzare la seguente evidenza:

> E03 migliora il Mean Final Money del `+150.68%` rispetto a E02 nel benchmark locale, mentre il miglioramento dello score Kaggle attualmente osservato è molto più contenuto.

Individuare le possibili spiegazioni supportate dalle meccaniche dell'ambiente o dalle evidenze presenti nel progetto.

Per ogni spiegazione utilizzare una delle seguenti classificazioni:

### SUPPORTED

La spiegazione è direttamente supportata da codice, ambiente, risultati o altre evidenze verificabili.

### PLAUSIBLE

La spiegazione è coerente con le evidenze disponibili, ma non è ancora stata dimostrata.

### UNSUPPORTED / UNKNOWN

Le evidenze attuali non consentono di stabilirla.

Non forzare una spiegazione unica se i dati disponibili non la supportano.

---

## 6. Competitive Gap Matrix

Produrre come deliverable principale una matrice con la seguente struttura:

| Meccanica / capacità | Disponibile nell'ambiente | Utilizzata da E03 | Rilevanza strategica | Evidenza | Gap potenziale |
|---|---|---|---|---|---|

La matrice deve includere **tutte le meccaniche strategicamente rilevanti individuate durante l'audit**, non soltanto quelle già considerate nelle precedenti iterazioni.

La matrice deve permettere di distinguere chiaramente:

- capacità già sfruttate;
- capacità parzialmente sfruttate;
- capacità completamente ignorate;
- capacità la cui rilevanza non è ancora verificabile.

---

## 7. Rivalutazione delle candidate già individuate

Il progetto aveva precedentemente individuato come possibili direzioni:

- **End-of-Season Horizon**;
- **Market Timing**;
- modello economico con `max_yield` specifico per coltura;
- scaling geografico oltre le quattro tile tramite `BUY_LAND`.

Rivalutare ciascuna candidata alla luce della Competitive Gap Analysis.

Classificarla principalmente come:

- **ottimizzazione economica incrementale**;
- **miglioramento di scalabilità**;
- **miglioramento competitivo/adattivo**;
- **non classificabile con le evidenze disponibili**.

Non selezionare una candidata soltanto perché era già stata individuata.

Se l'audit dell'ambiente rivela meccaniche inutilizzate potenzialmente più importanti, aggiungere nuove candidate.

---

## 8. Individuazione dei principali strategic gap

Al termine dell'audit individuare i **3–5 gap strategici più rilevanti**.

Per ciascuno indicare:

1. meccanica ignorata o sottoutilizzata;
2. evidenza della sua esistenza;
3. comportamento corrente di E03;
4. ragione per cui potrebbe influire sulla performance competitiva;
5. cosa dovrebbe essere misurato per verificare l'ipotesi;
6. rischio sperimentale previsto;
7. possibilità di isolarla come **singola variabile sperimentale**.

Non implementare nessuna delle candidate.

---

## 9. Raccomandazione sulla direzione di E04

Soltanto dopo aver completato l'intero audit, indicare quale strategic gap appare più adatto a diventare oggetto di E04.

La raccomandazione deve essere motivata sulla base di:

- evidenze disponibili;
- rilevanza competitiva attesa;
- isolabilità sperimentale;
- misurabilità;
- compatibilità con il metodo sperimentale supervisionato del progetto.

La raccomandazione **non costituisce ancora autorizzazione a implementare E04**.

Se le evidenze disponibili non sono sufficienti per scegliere E04, dichiararlo esplicitamente e indicare il **minimo esperimento diagnostico aggiuntivo** necessario per risolvere l'incertezza.

---

## 10. Deliverable richiesti

Produrre l'analisi strutturandola nelle seguenti sezioni:

1. **Environment Capability Inventory**
2. **E03 Decision Policy Reconstruction**
3. **Competitive Objective Analysis**
4. **Local vs Kaggle Divergence Analysis**
5. **Competitive Gap Matrix**
6. **Reassessment of Existing E04 Candidates**
7. **Top Strategic Gaps**
8. **Recommended E04 Direction**
9. **Open Questions / Unknowns**

Salvare l'intera analisi nel file:

`docs/experiments/E04-01_Competitive_Gap_Analysis.md`

Se la struttura effettiva del repository utilizza una directory diversa per la documentazione degli esperimenti E01–E03, utilizzare **la stessa directory già adottata dal progetto**, mantenendo comunque il nome:

`E04-01_Competitive_Gap_Analysis.md`

---

## 11. Vincoli operativi

Questa è esclusivamente una fase di **DEFINE / investigation**.

Non:

- modificare il source code dell'agente;
- modificare i test;
- modificare gli script di valutazione;
- creare file di implementazione E04;
- implementare una nuova strategia;
- creare un Implementation Plan E04;
- eseguire commit;
- eseguire push;
- creare tag Git.

È consentito:

- leggere file;
- cercare nel repository;
- ispezionare codice e configurazioni;
- eseguire comandi diagnostici read-only;
- utilizzare diagnostica già esistente quando non modifica lo stato sperimentale.

Se un'esecuzione diagnostica aggiuntiva comporta la creazione o modifica di risultati, log o altri file versionati, **fermarsi prima dell'esecuzione**, spiegare:

1. quale diagnostica si propone;
2. perché è necessaria;
3. quale evidenza dovrebbe produrre;

e richiedere approvazione.

---

## Principio sperimentale da preservare

La successiva iterazione deve continuare a rispettare:

> **Una modifica strategica principale per esperimento.**

L'obiettivo di questa analisi non è trovare un altro modo per rendere E03 semplicemente più produttivo.

L'obiettivo è determinare:

> **Che cosa il nostro agente attuale non ha ancora capito del gioco?**