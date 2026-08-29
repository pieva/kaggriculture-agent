# E10-01 — DEFINE + PLAN + BUILD + KAGGLE OVERNIGHT VALIDATION
## Q1 Expansion Capital Protection / Productive Utilization

## Decisione del supervisore

E10 deve essere validato **questa notte direttamente su Kaggle**.

NON eseguire un robustness benchmark locale da 150/300 episodi.

La validazione locale deve essere limitata a quanto necessario per garantire:
- correttezza dell'esperimento;
- isolamento della variabile;
- assenza di regressioni tecniche;
- validità della submission.

La vera evidenza competitiva E10 verrà raccolta tramite gli scontri Kaggle durante la notte.

---

# Contesto sperimentale

## E09-01

Baseline causale E10:

> **E09-01 — 40 tile — Livestock OFF**

Risultati locali E09-01:
- Mean Final Money: **$22,899.20**
- Median: **$27,672.00**
- SD: **$7,892.99**
- Win Rate standard: **100%**
- E09 batte E08 in **26/30**
- E09 batte E06 in **21/30**

E09 presenta tuttavia una forte coda negativa.

Il REVIEW ha identificato come failure mode principale:

> **Q1 Land Expansion Cash Bottleneck intorno al Giorno 12**

Nei run peggiori il capitale disponibile non consente l'espansione Q1 tempestiva e/o la successiva attivazione produttiva, con forte perdita di ricavi Melone.

## Evidenza Kaggle corrente

Ultima evidenza fornita dal supervisore, circa 4 ore dopo la submission E09:

- E09-01: **347.0**
- E07: **354.4**
- E06: **375.7**
- E05: **429.5**

Gli scontri osservati mostrano inoltre:
- grandi superfici E09 lasciate improduttive;
- forte variabilità tra gli episodi;
- avversari più forti che sfruttano una superficie maggiore;
- alcuni avversari forti che integrano anche livestock.

Interpretazione corretta:

> E09 dimostra che **il livestock implementato in E08** era un value sink.

NON dimostra che livestock sia intrinsecamente negativo.

E10 NON deve reintrodurre livestock.

---

# Ipotesi E10

> **Proteggere esplicitamente il capitale necessario all'espansione Q1 prima del Giorno 12 aumenta la probabilità di espansione tempestiva e l'attivazione produttiva del footprint da 40 tile, riducendo i collassi economici osservati in E09.**

E10 deve essere un esperimento **single-variable** rispetto a E09.

---

# FASE 1 — DEFINE

Prima di modificare codice:

1. `git status`
2. `git log -1 --oneline`
3. `git tag --list`

Rileggi almeno:
- `docs/versions/E09_define_livestock_ablation.md`
- `docs/versions/E09_build_livestock_ablation.md`
- `docs/versions/E09_verify_local_performance.md`
- `docs/versions/E09_review_livestock_ablation.md`
- `docs/versions/E09_kaggle_external_validation.md`
- `results/e09_livestock_ablation.json`
- `src/agricola/strategy/livestock_ablation_roi.py`
- `src/agricola/agent.py`
- `scripts/build_submission.py`

NON fare commit/push/tag.

## Baseline

Primary causal baseline:

> **E09-01**

E06/E07/E08 sono riferimenti secondari.

## Variabile sperimentale

Individua dal codice:
- costo reale `BUY_LAND Q1`;
- giorno/turno target;
- cash reserve corrente;
- acquisti che possono consumare capitale nei giorni precedenti;
- minima finestra temporale necessaria.

Definisci la più semplice politica di:

> **Q1 Expansion Capital Protection**

La regola deve essere derivata dal comportamento corrente, non da tuning opportunistico.

## Invarianti

Congela:
- 40 tile;
- Livestock OFF;
- 4 worker;
- hiring;
- Water-First;
- spatial partitioning;
- movement logic;
- cross-boundary assist;
- crop allocation;
- liquidation;
- market policy;
- Q1 target timing;
- ogni altra logica non necessaria alla protezione del capitale.

Crea:

`docs/versions/E10_define_q1_capital_protection.md`

---

# FASE 2 — PLAN

Documenta:

1. classe E10;
2. delta esatto E09 -> E10;
3. regola di capital protection;
4. unit test;
5. telemetria;
6. verifica locale minima;
7. packaging;
8. Kaggle validation;
9. criteri di interpretazione mattutini.

Crea:

`docs/versions/E10_plan_q1_capital_protection.md`

Procedi al BUILD salvo ambiguità bloccante.

---

# FASE 3 — BUILD

Crea una nuova strategia E10 senza modificare E09.

Nome consigliato:

`Q1CapitalProtectedROIAgent`

File:

`src/agricola/strategy/q1_capital_protected_roi.py`

## Test obbligatori

Verifica almeno:

- Livestock OFF;
- footprint 40 tile;
- workforce/hiring invariati;
- Water-First invariato;
- target Q1 invariato;
- protezione capitale attiva solo nella finestra prevista;
- acquisti non prioritari non possono consumare il capitale protetto;
- protezione rilasciata dopo l'espansione;
- nessun'altra policy cambia.

Esegui:
- test E10;
- full `pytest tests/`.

Esegui un singolo smoke test da 720 step.

Lo smoke test serve solo alla validità tecnica.

Crea:

`docs/versions/E10_build_q1_capital_protection.md`

---

# FASE 4 — LOCAL SAFETY VERIFY

NON eseguire 150/300 episodi.

Esegui solo un benchmark paired breve sufficiente a intercettare regressioni macroscopiche.

Preferenza:

> **30 paired episodes con gli stessi seed/opponent E09**

se il tempo di esecuzione resta ragionevole.

Confronta:
- E09-01;
- E10;
- E06 come riferimento secondario.

Metriche minime:
- Mean;
- Median;
- SD;
- Min/Max;
- paired delta E10-E09;
- paired W/D/L;
- episodi < $10k;
- episodi < $20k.

Telemetria diagnostica:
- cash al target Q1;
- giorno/ora BUY_LAND;
- Q1 purchased on time;
- seed spending;
- Melon revenue;
- Q1 planted tiles;
- total planted tiles;
- plant_pending;
- movement share.

## Gate per Kaggle

Procedi alla submission se:

1. tutti i test passano;
2. E10 completa gli episodi senza DQ/errori;
3. la modifica è effettivamente isolata;
4. la protezione capitale produce il comportamento previsto;
5. non emerge una regressione locale catastrofica.

NON richiedere che E10 batta già statisticamente E09 nei 30 episodi per poter andare su Kaggle.

La validazione competitiva è l'obiettivo della notte.

---

# FASE 5 — FREEZE E10

Superato il safety gate:

> **FREEZE E10**

Da questo punto NON modificare più la strategia.

Imposta `src/agricola/agent.py` affinché esponga esclusivamente E10 secondo la convenzione del repository.

Non duplicare logica in `agent.py`.

---

# FASE 6 — BUILD SUBMISSION

Usa lo script ufficiale:

`.venv\Scripts\python.exe scripts/build_submission.py`

Verifica:
- entrypoint E10;
- standalone;
- assenza path locali;
- assenza dipendenze da `scratch/`;
- assenza dipendenze dai risultati;
- package valido.

Esegui:
- `pytest tests/test_submission.py`
- full regression suite dopo il cambio entrypoint.

Se disponibile, esegui un package smoke test nel motore Kaggle.

Non usarlo come benchmark prestazionale.

---

# FASE 7 — IDENTITÀ KAGGLE

Descrizione consigliata:

> **`E10-01 Q1 Capital Protection — 40t Livestock OFF`**

Registra:

```text
Experiment: E10-01
Baseline: E09-01
Variant: Q1 Expansion Capital Protection
Footprint: 40 tile
Livestock: OFF
Single experimental variable: Q1 capital protection
Validation: Kaggle overnight
```

---

# FASE 8 — KAGGLE SUBMISSION

## Regola operativa

Se Kaggle richiede upload manuale:

**FERMATI PRIMA DELL'UPLOAD** e restituisci:
- percorso esatto della submission;
- descrizione esatta;
- test eseguiti;
- risultato safety benchmark.

Il supervisore effettuerà l'upload manuale.

NON tentare browser automation fragile.

Se esiste un workflow Kaggle già configurato, autenticato e verificato nel repository, può essere utilizzato solo se non richiede nuove credenziali o procedure non documentate.

Non inventare score o stato.

---

# FASE 9 — OVERNIGHT KAGGLE MONITORING

Dopo che il supervisore conferma l'upload:

la submission deve essere lasciata invariata per la notte.

NON:
- modificare E10;
- creare E10-02;
- fare tuning;
- reintrodurre livestock;
- ridurre footprint;
- creare E11;
- fare una seconda submission;
- commit/push/tag.

L'obiettivo è raccogliere **evidenza competitiva pulita**.

Il confronto primario sarà:

> **E10 vs E09**

Secondari:
- E06;
- E07;
- E05.

Non interpretare il rating iniziale come definitivo.

---

# FASE 10 — GAME FORENSICS

Domattina l'analisi NON dovrà limitarsi al rating.

Gli scontri Kaggle sono parte essenziale del VERIFY.

Per un campione di:
- vittorie E10;
- sconfitte moderate;
- peggiori sconfitte/collassi;

ricostruire, quando osservabile:

1. uso Q0;
2. timing espansione Q1;
3. uso Q1;
4. superficie coltivata;
5. superficie improduttiva;
6. worker distribution;
7. cicli produttivi;
8. final money;
9. comportamento dell'avversario;
10. eventuale livestock dell'avversario.

Prestare particolare attenzione alla domanda:

> **E10 compra Q1 puntualmente ma continua comunque a lasciarlo vuoto?**

Se sì, il cash bottleneck è stato corretto ma il problema dominante è downstream:

> **productive throughput / planting-water-harvest scheduling / movement**

---

# Criteri di interpretazione E10

## SUCCESS

E10:
- migliora il rating stabilizzato rispetto a E09;
- riduce i collassi competitivi;
- mostra maggiore utilizzo Q1;
- conserva i run forti.

## PARTIAL SUCCESS

E10 migliora timing/robustezza locale e/o riduce alcuni collassi, ma resta dietro competitivamente e lascia terreno inutilizzato.

Interpretazione:

> Q1 cash bottleneck reale ma non sufficiente.

## FAILURE

E10 non migliora E09 oppure Q1 viene acquistato correttamente ma il terreno resta improduttivo.

Interpretazione:

> passare nel prossimo esperimento al productive throughput.

---

# Documentazione

Crea:

`docs/versions/E10_kaggle_overnight_validation.md`

Prima dell'upload documenta:
- DEFINE;
- PLAN;
- BUILD;
- safety VERIFY;
- freeze;
- package;
- submission readiness.

Dopo evidenza Kaggle aggiungere:
- timestamp upload;
- rating iniziali;
- rating successivi;
- confronto E09/E10;
- game forensics;
- verdict.

Aggiorna:
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

NON dichiarare E10 SHIPPED.

---

# Git

Durante questa fase:

NON:
- commit;
- push;
- tag.

La chiusura Git avverrà solo dopo REVIEW e decisione del supervisore.

---

# STOP 1 — UPLOAD MANUALE

Se serve upload manuale:

> **E10-01 KAGGLE SUBMISSION READY — MANUAL UPLOAD REQUIRED**

FERMATI e attendi il supervisore.

---

# STOP 2 — DOPO UPLOAD

Dopo conferma dell'upload:

> **E10-01 KAGGLE OVERNIGHT VALIDATION RUNNING**

Non modificare nulla.

---

# STOP 3 — DOMATTINA

Dopo aver raccolto l'evidenza disponibile:

> **E10 KAGGLE OVERNIGHT VALIDATION — READY FOR SUPERVISOR REVIEW**

NON:
- fare REVIEW autonomamente;
- SHIP;
- commit/push/tag;
- iniziare E11.

---

# Principio metodologico

```text
E09
40 tile
Livestock OFF
        |
        | unica modifica
        v
E10
Q1 capital protected
        |
        | safety verify locale
        v
Frozen E10
        |
        | Kaggle overnight
        v
Competitive evidence
        |
        +--> Q1 timing corretto?
        |
        +--> Q1 realmente coltivato?
        |
        +--> collassi ridotti?
        |
        +--> rating migliore di E09?
```

E10 non deve dimostrare genericamente che “più terreno è meglio”.

Deve stabilire se **la protezione del capitale consente alla strategia di trasformare più affidabilmente il footprint da 40 tile in capacità produttiva effettiva**.

Solo dopo questa evidenza sarà corretto decidere se il prossimo collo di bottiglia è:
- capitale;
- seed allocation;
- worker throughput;
- movement;
- scheduling;
- oppure, più avanti, una reintroduzione economicamente disciplinata del livestock.
