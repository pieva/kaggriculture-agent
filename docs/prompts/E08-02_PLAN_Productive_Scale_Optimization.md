# E08-02 — PLAN Productive Scale Optimization

## Contesto

Stiamo lavorando al progetto **Kaggriculture**, esperimento **E08 — Productive Scale Optimization**.

La fase precedente **E08-01 DEFINE** è stata completata e approvata con decisione:

> **GO FOR PLAN**

Documento di riferimento principale:

- `docs/versions/E08_define_productive_scale.md`

Esaminare inoltre:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`
- documentazione E07 pertinente, in particolare:
  - `docs/versions/E07_verify_functional_utilization.md`
  - `docs/versions/E07_verify_local_performance.md`
  - `docs/versions/E07_verify_competitive_evidence.md`
  - `docs/plans/E07_Competitive_Baseline_Reconstruction.md`

Questa fase è esclusivamente **PLAN**.

**NON modificare ancora il codice della strategia.**
**NON eseguire benchmark E08.**
**NON generare o inviare submission Kaggle.**

---

# Obiettivo sperimentale E08

E07 ha acquistato 50 tile complessive tra Q0 e Q1, ma il target produttivo era limitato a 24 tile.

E08 deve verificare se un aumento controllato della superficie realmente produttiva può migliorare il rendimento economico mantenendo congelata l'architettura principale E07.

Target sperimentale:

> **40 tile produttive su 50 possedute = 80% land utilization**

Variazione primaria:

- E07: 24 productive tiles;
- E08: 40 productive tiles;
- incremento: +16 tile;
- incremento percentuale: +66.7%.

Configurazione crop target:

- 6 Wheat;
- 22 Melon;
- 12 Carrot.

Componenti da mantenere congelate:

- Strategy Class / architettura E07;
- workforce: 4 worker;
- livestock: 4 Cows + 2 Sheep;
- `BUY_LAND` Q1 al Day 12;
- task priority: `WATER > FEED > HARVEST > PLANT`;
- liquidation policy E07;
- market policy E07.

La PLAN deve progettare esclusivamente le modifiche necessarie a rendere sostenibile e verificabile il passaggio da 24 a 40 tile.

---

# P1 — Analisi preliminare del codice E07

Prima di definire il piano operativo, ispeziona il codice corrente e identifica:

1. dove viene configurato il numero di crop tile;
2. dove sono definite le coordinate del layout;
3. come vengono assegnati i task ai worker;
4. come vengono scelti i target di movimento;
5. come vengono acquistate le sementi;
6. come viene gestito il cash disponibile;
7. come viene acquistato Q1;
8. dove viene implementata la priorità Water-First;
9. come viene gestito il feed loop Wheat;
10. quali telemetrie esistono già.

Identifica i file che dovranno essere modificati nel successivo BUILD.

Non modificarli in questa fase.

---

# P2 — Piano layout a 40 tile

Progetta un layout iniziale per 40 crop tile.

Ipotesi iniziale:

- **20 tile Q0**
- **20 tile Q1**

Crop mix totale:

- 6 Wheat;
- 22 Melon;
- 12 Carrot.

Preserva le 6 Wheat dedicate al feed loop.

Il layout deve evitare:

- collisioni con strutture;
- collisioni con livestock/pascoli;
- coordinate duplicate;
- tile non possedute al momento dell'utilizzo;
- geometrie evidentemente irraggiungibili o inefficienti.

## Vincolo metodologico importante

Il requisito sperimentale è:

> **40 tile realmente produttive / 80% utilization**

La ripartizione:

> **20 Q0 + 20 Q1**

deve essere trattata come **layout iniziale selezionato**, non come requisito architetturale immutabile.

Il PLAN deve quindi separare concettualmente:

- target di scala = 40 tile;
- geometria iniziale = 20+20.

Non progettare test futuri che definiscano il successo generale E08 esclusivamente come presenza esatta di 20 tile in ciascun quadrante.

---

# P3 — Capacità della workforce e Spatial Partitioning

E07 utilizza:

- 1 Farmer;
- 3 Hands;
- totale 4 worker.

Nel DEFINE era stata stimata una capacità di:

- 96 worker-turn/giorno;
- circa 52 azioni produttive/giorno alla scala E08;
- `52 / 96 ≈ 54.2%`.

## Correzione semantica obbligatoria

Il **54.2%** rappresenta una stima del **carico produttivo**, NON il movement share E07.

NON descrivere quindi il piano come una riduzione del movimento:

> `54.2% → <38%`

perché le due metriche sono diverse.

Se viene proposto `<38% movement share`, deve essere definito esclusivamente come:

> **target diagnostico E08**

e non come riduzione rispetto a una falsa baseline E07 del 54.2%.

---

## Spatial Partitioning da progettare

Per limitare gli spostamenti, pianifica un partizionamento spaziale dei worker.

Configurazione iniziale da valutare:

- Worker 0 — Farmer → Q0;
- Worker 1 — Hand 1 → Q0;
- Worker 2 — Hand 2 → Q1;
- Worker 3 — Hand 3 → Q1.

Il dispatcher dovrà preferire task appartenenti al quadrante assegnato.

La località spaziale NON deve alterare la priorità globale:

> `WATER > FEED > HARVEST > PLANT`

---

## Cross-Boundary Water Assist

Prevedi una eccezione controllata:

- se un worker non dispone di task utili nel proprio quadrante;
- e nell'altro quadrante esistono task `needs_water`;
- il worker può attraversare il confine per assistere.

Il PLAN deve specificare che:

- l'assistenza è subordinata alla Water-First priority;
- non deve annullare il beneficio del partizionamento;
- inizialmente non va estesa automaticamente ad HARVEST o PLANT.

---

# P4 — Staggered Seed Purchasing

L'espansione Q1 richiederà più sementi.

Pianifica un meccanismo di acquisto dilazionato per evitare che l'espansione consumi immediatamente la liquidità disponibile.

Finestra iniziale:

> **Day 12–15**

Cash floor:

> **$300**

Il piano deve specificare:

- come distribuire gli acquisti;
- come evitare acquisti duplicati;
- come evitare over-purchasing;
- come mantenere il crop mix target;
- come proteggere il feed loop Wheat;
- cosa fare se il cash floor impedisce temporaneamente l'espansione.

Il cash floor deve essere verificabile nella successiva VERIFY.

Non modificare il timing di `BUY_LAND` Q1 previsto per Day 12.

---

# P5 — Diagnostica necessaria

Il PLAN deve prevedere la telemetria necessaria a distinguere:

> **40 configured** da **40 realmente produttive**

Predisporre nel BUILD almeno le seguenti metriche:

## Land utilization

- configured crop tiles;
- peak productive tiles;
- mean daily productive tiles;
- tile configurate ma mai utilizzate;
- se tecnicamente disponibile:
  - planted tiles;
  - maintained/watered tiles;
  - harvested tiles.

## Workforce utilization

- productive/action turns;
- movement turns;
- idle turns;
- totale turni;
- relative percentuali.

## Backlog

Almeno:

- `needs_water`;
- `harvest_ready`;
- `plant_pending`.

## Cash

- minimum cash balance;
- andamento degli acquisti sementi;
- acquisti impediti dal cash floor.

## Spatial partitioning

Se tecnicamente praticabile:

- task Q0/Q1 per worker;
- cross-boundary assists;
- eventuali worker persistentemente idle o sovraccarichi.

---

# P6 — Piano dei test

Definisci i test da implementare nella successiva fase BUILD.

Devono coprire almeno:

## Configurazione

- target totale 40;
- Wheat = 6;
- Melon = 22;
- Carrot = 12;
- totale crop mix = 40.

## Layout

- coordinate valide;
- coordinate univoche;
- assenza di collisioni note;
- possibilità di utilizzare 40 tile dopo l'espansione.

Ricorda:

> il requisito generale non è rigidamente `20 Q0 + 20 Q1`.

## Spatial partitioning

- worker 0–1 preferiscono Q0;
- worker 2–3 preferiscono Q1;
- Water-First resta prioritaria;
- cross-boundary assist interviene soltanto nelle condizioni previste.

## Seed purchasing

- acquisti dilazionati;
- cash floor;
- assenza duplicazioni;
- progressione verso il target quando la liquidità lo consente.

## Regression

Prevedi l'esecuzione completa:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

Criterio:

> 100% test pass.

---

# P7 — Piano VERIFY

La VERIFY successiva deve essere progettata in due livelli.

## V1 — Functional / Utilization Verification

Prima del benchmark economico verificare:

- 40 tile configurate;
- quante tile diventano realmente produttive;
- picco e media giornaliera;
- progressione Day 12–15;
- minimum cash;
- worker productive/movement/idle;
- backlog WATER/HARVEST/PLANT;
- comportamento dello spatial partitioning.

Il requisito non deve essere chiuso con la sola presenza di 40 coordinate.

La catena da verificare è:

> **configured → planted → maintained → harvested → economic value**

---

## V2 — Local Performance Benchmark

Prevedi benchmark paired da **30 episodi**:

- 10 × `pass`;
- 10 × `random`;
- 10 × `starter`;
- stessi seed e stesso protocollo utilizzato per il confronto E07, quando disponibili.

Baseline primaria iniziale documentata:

> **E07 Mean Final Money = $15,364.57**

Riferimento secondario:

> **E06 Mean Final Money = $25,180.30**

Il piano deve però richiedere che, durante VERIFY/REVIEW, i valori siano confrontati soltanto se derivano da protocolli effettivamente compatibili.

Metriche:

- Mean Final Money;
- Median;
- Standard Deviation (`ddof=1`);
- Completion Rate;
- Disqualification Rate;
- breakdown per opponent;
- delta assoluto E08−E07;
- delta percentuale;
- eventuale gap recuperato verso E06.

---

# Criteri di successo

## Criterio architetturale

E08 deve dimostrare di poter utilizzare realmente la nuova scala produttiva.

Non basta:

> `configured_crop_tiles = 40`

Serve evidenza che una quota prossima al target entri realmente nel ciclo agricolo.

## Criterio economico primario

> **E08 Mean Final Money > E07 Mean Final Money**

con protocollo comparabile.

## Criterio secondario

Misurare il recupero del gap verso E06.

E06 NON è il requisito minimo per dichiarare utile E08.

## Criteri diagnostici

Interpretare il risultato attraverso:

- movement;
- idle;
- backlog;
- cash;
- land utilization.

Il target `<38% movement share`, se mantenuto, è soltanto diagnostico.

---

# Sequenza BUILD proposta

Formalizza una sequenza B1–B6 coerente con:

```text
B1 — Config & Diagnostic Instrumentation
B2 — 40-Tile Spatial Layout
B3 — Spatial Worker Partitioning
B4 — Staggered Seed Purchasing
B5 — Automated Tests
B6 — Preparation for VERIFY
```

B6 deve preparare il benchmark, NON eseguirlo durante PLAN o BUILD se la fase successiva non è stata ancora approvata.

---

# Vincoli

Durante E08 mantenere congelati:

- workforce;
- livestock;
- Day 12 Q1 purchase;
- Water-First priority;
- liquidation policy;
- market policy.

Non introdurre nel PLAN:

- nuovi worker;
- nuove specie livestock;
- rimozione livestock;
- ulteriori quadranti;
- nuove colture;
- nuove euristiche di trading;
- modifiche sostanziali al dispatcher oltre allo spatial partitioning previsto.

Se emerge che una modifica fuori scope è indispensabile, registrarla come rischio/blocker per supervisione.

---

# Deliverable richiesti

Crea:

`docs/plans/E08_Productive_Scale_Optimization.md`

e:

`docs/versions/E08_plan_productive_scale.md`

Il piano deve contenere almeno:

1. obiettivo;
2. baseline;
3. variabile sperimentale;
4. componenti congelate;
5. layout;
6. spatial partitioning;
7. cross-boundary assist;
8. staggered purchasing;
9. diagnostica;
10. test;
11. protocollo VERIFY;
12. criteri di successo;
13. rischi;
14. sequenza B1–B6.

Aggiorna inoltre:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

indicando che E08 PLAN è completato ma BUILD non è ancora iniziato.

---

# Git

Al termine esegui:

```powershell
git status --short
git diff --stat
```

NON eseguire:

- commit;
- push;
- tag.

---

# Output finale richiesto

Restituisci:

## E08-02 — PLAN Productive Scale Optimization

### 1. Configurazione proposta
Tabella E07 → E08.

### 2. Layout e spatial partitioning
Descrizione della soluzione.

### 3. Seed purchasing e liquidità
Meccanismo e cash floor.

### 4. Diagnostica prevista
Metriche.

### 5. Sequenza BUILD B1–B6
Piano operativo.

### 6. Piano VERIFY
Functional + performance benchmark.

### 7. Criteri di successo
Architetturali, economici e diagnostici.

### 8. Rischi e vincoli
Elementi congelati e possibili blocker.

### 9. Deliverable creati/aggiornati
Elenco file.

### 10. Git status e diff
Output dei comandi.

### 11. Decisione PLAN

Usa una sola delle seguenti:

- `GO FOR BUILD`
- `PLAN BLOCKED — SUPERVISION REQUIRED`

---

# STOP OBBLIGATORIO

Al termine:

**FERMATI.**

NON iniziare E08 BUILD.

NON modificare il codice della strategia.

NON eseguire benchmark E08.

NON inviare submission Kaggle.

NON eseguire commit, push o tag.

Attendi esplicita approvazione prima della fase BUILD.
