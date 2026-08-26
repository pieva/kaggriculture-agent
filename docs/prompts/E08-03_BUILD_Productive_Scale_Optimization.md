# E08-03 — BUILD Productive Scale Optimization

## Contesto

Stiamo lavorando al progetto **Kaggriculture**, esperimento **E08 — Productive Scale Optimization**.

Le fasi precedenti sono state completate:

- **E08-01 DEFINE**: approvato;
- **E08-02 PLAN**: approvato con due correzioni da recepire prima/durante il BUILD;
- fase corrente: **E08-03 BUILD**.

Documenti di riferimento prioritari:

- `docs/versions/E08_define_productive_scale.md`
- `docs/plans/E08_Productive_Scale_Optimization.md`
- `docs/versions/E08_plan_productive_scale.md`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`
- documentazione E07 rilevante, in particolare:
  - `docs/versions/E07_verify_functional_utilization.md`
  - `docs/versions/E07_verify_local_performance.md`
  - `docs/versions/E07_verify_competitive_evidence.md`
  - `docs/plans/E07_Competitive_Baseline_Reconstruction.md`

La baseline primaria E08 è **E07 = $15,364.57 Mean Final Money**.

Il valore **E06 = $25,180.30** è esclusivamente un riferimento secondario per valutare quanto del gap competitivo venga recuperato: **non è il criterio minimo di successo di E08**.

---

# Obiettivo del BUILD

Implementare la strategia E08 aumentando la scala produttiva da **24 a 40 tile**, mantenendo congelate le altre principali componenti architetturali E07.

L'esperimento deve isolare, per quanto possibile, l'effetto dell'aumento della superficie produttiva e delle sole modifiche strettamente necessarie a renderlo operativo.

Configurazione target:

- **40 productive crop tiles**
- **80% land utilization** sulle 50 tile possedute
- **6 Wheat**
- **22 Melon**
- **12 Carrot**
- **4 workers** invariati
- **4 Cows + 2 Sheep** invariati
- acquisto Q1 al **Day 12** invariato
- priorità operativa **WATER > FEED > HARVEST > PLANT** invariata
- liquidation/market policy E07 invariata salvo modifiche strettamente necessarie alla compatibilità tecnica.

Non introdurre nuove ottimizzazioni economiche non previste dal PLAN.

---

# Correzioni obbligatorie al PLAN

Prima di considerare completato il BUILD, recepisci esplicitamente queste due correzioni nella documentazione E08.

## 1. Correzione della metrica `54.2%`

Nel PLAN compare un riferimento al passaggio del rapporto di movimento dal **54.2% a <38%**.

Questa formulazione è errata.

Nel DEFINE, **54.2%** indicava la stima del **carico produttivo**:

- circa 52 azioni produttive/giorno;
- 96 worker-turn/giorno disponibili;
- `52 / 96 ≈ 54.2%`.

Non rappresentava il movement share E07.

Pertanto:

- NON usare `54.2%` come baseline del movimento;
- correggi la documentazione che contiene questa interpretazione;
- se viene mantenuto `<38%`, trattalo esclusivamente come **target diagnostico E08 del movement share**, non come riduzione misurata da una baseline del 54.2%;
- non inventare una baseline E07 del movement share se non è già disponibile da evidenze misurate.

## 2. 40 tile è il requisito; 20 Q0 + 20 Q1 è il layout iniziale

Il requisito sperimentale E08 è:

> **40 tile realmente produttive / 80% di utilizzo delle 50 tile possedute.**

La distribuzione:

> **20 Q0 + 20 Q1**

è il layout iniziale scelto nel PLAN, NON un requisito architetturale immutabile.

Puoi implementarlo come configurazione iniziale, ma:

- non codificare test che definiscano il successo E08 esclusivamente come `20 Q0 + 20 Q1`;
- separa, dove ragionevole, il target di scala dalla geometria concreta;
- se durante il BUILD emergono impedimenti tecnici evidenti, documenta il problema;
- NON effettuare però autonomamente una nuova ottimizzazione del layout fuori dallo scope E08.

L'eventuale modifica sostanziale del layout dovrà essere motivata e sottoposta a supervisione.

---

# BUILD — attività richieste

## B1 — Configurazione E08 e diagnostica

Aggiorna la configurazione della strategia E07/E08 per supportare:

- `target_productive_tiles = 40`
- `wheat_tiles = 6`
- `melon_tiles = 22`
- `carrot_tiles = 12`

Mantieni invariati:

- workforce;
- livestock;
- Day 12 Q1 purchase;
- task priority;
- liquidation policy.

Evita magic numbers sparsi nel codice se esiste già una configurazione centralizzata adatta.

Aggiungi o prepara la diagnostica necessaria per misurare almeno:

1. numero di tile produttive;
2. picco delle tile produttive;
3. media giornaliera delle tile produttive;
4. worker productive turns;
5. worker movement turns;
6. worker idle turns;
7. task backlog;
8. minimum cash balance.

Per il backlog, se tecnicamente disponibile senza modificare in modo invasivo l'architettura, distinguere almeno:

- `needs_water`;
- harvest-ready non ancora raccolte;
- plant pending / tile previste ma non ancora seminate.

Una tile non deve essere considerata realmente produttiva soltanto perché appartiene alla griglia configurata.

La diagnostica deve permettere di distinguere, per quanto possibile:

- tile configurata;
- tile seminata;
- tile mantenuta correttamente;
- tile raccolta/produttiva.

---

## B2 — Layout produttivo a 40 tile

Implementa il layout iniziale:

- 20 tile Q0;
- 20 tile Q1.

Allocazione complessiva:

- 6 Wheat;
- 22 Melon;
- 12 Carrot.

Preserva il feed loop dedicato alle 6 Wheat.

Verifica che le coordinate:

- siano valide;
- appartengano a terreno effettivamente posseduto quando utilizzate;
- non confliggano con strutture, livestock o altre entità;
- siano raggiungibili dai worker;
- non generino duplicazioni.

Non modificare la logica di acquisto Q1 al Day 12.

Prima del Day 12 la strategia deve continuare a funzionare correttamente utilizzando solo il terreno disponibile.

---

## B3 — Spatial Worker Partitioning

Implementa il partizionamento previsto:

- Worker 0 — Farmer → Q0;
- Worker 1 — Hand 1 → Q0;
- Worker 2 — Hand 2 → Q1;
- Worker 3 — Hand 3 → Q1.

Obiettivo: ridurre gli spostamenti inutili causati dall'aumento della superficie produttiva.

Il dispatcher deve preferire task appartenenti al quadrante assegnato al worker.

Mantieni la priorità globale:

`WATER > FEED > HARVEST > PLANT`

Il partizionamento spaziale NON deve invertire questa gerarchia.

### Cross-Boundary Water Assist

Implementa l'override previsto:

- se un worker non dispone di task utili nel proprio quadrante;
- e sono presenti task `needs_water` prioritari nell'altro quadrante;
- il worker può attraversare il confine per assistere.

L'assistenza cross-boundary deve rimanere una **eccezione**, non trasformare nuovamente il dispatcher in un sistema completamente globale.

Non estendere autonomamente il cross-boundary assist ad altre classi di task durante questo BUILD.

---

## B4 — Staggered Seed Purchasing

Implementa l'acquisto dilazionato delle sementi necessarie all'espansione Q1.

Periodo previsto:

- Day 12–15.

Vincolo:

> mantenere, per quanto consentito dalla logica operativa, un **cash floor di $300**.

La strategia non deve acquistare sementi se l'acquisto porterebbe il cash disponibile sotto il floor previsto.

La logica deve:

- essere deterministica;
- evitare acquisti duplicati;
- evitare over-purchasing;
- rispettare il crop mix target;
- non compromettere il feed loop Wheat.

Registra nella diagnostica il **minimum cash balance** osservato.

Se il floor di $300 impedisce materialmente il raggiungimento delle 40 tile, NON abbassarlo arbitrariamente: documenta l'evidenza per la successiva VERIFY/REVIEW.

---

## B5 — Test automatici

Aggiorna `tests/test_hybrid_livestock_cluster.py` e/o crea test E08 dedicati se ciò mantiene meglio la separazione degli esperimenti.

I test devono coprire almeno:

### Configurazione

- target totale = 40;
- crop mix totale = 40;
- Wheat = 6;
- Melon = 22;
- Carrot = 12.

### Layout

- coordinate univoche;
- coordinate valide;
- assenza di collisioni note;
- capacità di raggiungere 40 tile dopo l'espansione.

NON definire il successo generale E08 esclusivamente come `20 Q0 + 20 Q1`.

### Spatial partitioning

Verificare:

- worker 0–1 preferiscono Q0;
- worker 2–3 preferiscono Q1;
- la task priority resta Water-First;
- il cross-boundary water assist scatta solo nelle condizioni previste.

### Seed purchasing

Verificare:

- acquisti staggered;
- rispetto del cash floor;
- assenza di acquisti duplicati;
- raggiungimento progressivo del target quando la liquidità lo consente.

### Regressioni

Esegui l'intera suite:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

Tutti i test devono passare.

---

# Confine BUILD / VERIFY

Questa fase è **BUILD**, non VERIFY.

Puoi eseguire:

- test unitari;
- test funzionali strettamente necessari a verificare che il codice costruito funzioni;
- smoke test tecnici brevi se indispensabili per individuare errori di implementazione.

NON eseguire ancora il benchmark comparativo ufficiale da 30 episodi E08 vs E07.

NON produrre ancora una decisione economica GO/NO-GO sulla strategia.

Il benchmark paired da 30 episodi appartiene alla successiva fase **E08 VERIFY**.

---

# Metriche da predisporre per VERIFY

Il BUILD deve lasciare il sistema pronto a misurare nella fase successiva:

## Prestazione economica

- Mean Final Money;
- Median Final Money;
- Standard Deviation (`ddof=1`);
- breakdown per opponent;
- differenza assoluta E08 − E07;
- differenza percentuale E08 vs E07.

Baseline primaria:

> **E07 = $15,364.57**

Riferimento secondario:

> **E06 = $25,180.30**

## Utilizzo terreno

- configured crop tiles;
- peak productive tiles;
- mean daily productive tiles;
- eventuali tile configurate ma non realmente utilizzate.

## Workforce

- productive turns;
- movement turns;
- idle turns;
- percentuali corrispondenti.

Se viene utilizzato `<38% movement share`, registrarlo come **target diagnostico E08**, non come criterio primario di successo e non come confronto con una falsa baseline E07 del 54.2%.

## Backlog

Almeno:

- watering backlog;
- harvest backlog;
- planting backlog.

## Liquidità

- minimum cash balance;
- andamento degli acquisti Day 12–15;
- eventuali giorni nei quali il cash floor impedisce l'espansione.

---

# Vincoli sperimentali

Durante il BUILD NON introdurre modifiche non previste a:

- numero worker;
- livestock;
- timing `BUY_LAND`;
- task priority;
- livestock feed policy;
- liquidation policy;
- prezzi/assunzioni economiche;
- altre euristiche di trading;
- nuove colture;
- ulteriori acquisti di terreno.

Se scopri che una di queste modifiche è indispensabile per rendere tecnicamente funzionante E08:

1. fermati;
2. documenta il blocker;
3. non modificare autonomamente il perimetro dell'esperimento.

---

# Submission parity

Preserva la parità tra:

- implementazione sorgente;
- `submission/submission.py`;
- `scripts/build_submission.py`.

Non lasciare una versione E08 funzionante localmente ma non riproducibile nella submission Kaggle.

Se il normale processo del repository prevede la rigenerazione della submission durante BUILD, eseguilo e verifica che completi senza errori.

NON inviare nulla a Kaggle in questa fase.

NON aprire browser o tentare autenticazioni Kaggle.

---

# Documentazione

Al termine del BUILD:

1. crea:

`docs/versions/E08_build_productive_scale.md`

2. aggiorna:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Registra almeno:

- file modificati;
- configurazione implementata;
- layout implementato;
- spatial partitioning;
- cross-boundary assist;
- staggered purchasing;
- diagnostica aggiunta;
- test aggiunti/modificati;
- risultato completo di `pytest`;
- eventuali deviazioni dal PLAN;
- eventuali blocker o anomalie;
- stato della submission parity.

Non dichiarare E08 validato: la validazione appartiene a VERIFY.

---

# Controlli Git finali

Al termine esegui:

```powershell
git status --short
git diff --stat
```

NON eseguire commit.

NON eseguire push.

NON creare tag.

La decisione di SHIP verrà presa solo dopo VERIFY e REVIEW.

---

# Output finale richiesto

Restituisci un report sintetico ma verificabile con questa struttura:

## E08-03 BUILD Productive Scale Optimization

### 1. Implementazione completata
Elenco delle modifiche effettivamente realizzate.

### 2. Correzioni PLAN recepite
Conferma esplicita:
- correzione semantica del 54.2%;
- distinzione fra requisito 40 tile e layout iniziale 20 Q0 + 20 Q1.

### 3. Diagnostica disponibile
Elenco delle metriche effettivamente implementate.

### 4. Test
Riporta:
- numero test;
- pass/fail;
- eventuali test E08 aggiunti.

### 5. Submission parity
Stato della generazione/allineamento di `submission/submission.py`.

### 6. Deviazioni o problemi
Qualunque differenza rispetto al PLAN deve essere esplicitata.

### 7. Git status e diff
Riporta l'output di:
- `git status --short`
- `git diff --stat`

### 8. Decisione BUILD
Usa esclusivamente una delle seguenti:

- `BUILD COMPLETE — READY FOR VERIFY`
- `BUILD BLOCKED — SUPERVISION REQUIRED`

---

# STOP OBBLIGATORIO

Al termine del BUILD:

**FERMATI.**

NON iniziare E08 VERIFY.

NON eseguire il benchmark ufficiale da 30 episodi.

NON modificare ulteriormente la strategia sulla base di risultati economici preliminari.

NON inviare submission Kaggle.

Attendi esplicita approvazione prima di procedere alla fase successiva.
