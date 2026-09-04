# Prompt operativo — Claude E17.1 3Q reattivo indipendente

Esegui questo prompt dalla root:

`C:\Users\pietr\Projects\kaggriculture-agent`

## Mandato

Progetta, implementa e valida una policy Claude 3Q nativa, state-reactive e
strategicamente indipendente, destinata al torneo definito in
`experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`.

Non modificare la policy Codex. Non costruire un wrapper della V9. Non usare o
ricostruire la sua action table.

## Lettura obbligatoria

Leggi integralmente:

1. `docs/repository/REPOSITORY_ARCHITECTURE.md`;
2. `README.md`;
3. `docs/NEW_SESSION.md`;
4. `docs/PROJECT_STATE.md`;
5. `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`;
6. i tre documenti C2.1 di ontology, state machine e feature model;
7. `src/agricola/core/observation_contract.py`;
8. `src/agricola/core/e17_ledger.py`;
9. `experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`;
10. `experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md`;
11. il report di onboarding Claude aggiornato, se disponibile fuori repo.

Puoi leggere il MODEL_SPEC Codex e la guida V9 soltanto per comprendere
interfaccia, baseline del torneo e differenza tra open-loop e reattivo. Non
leggere la tabella generata `codex_v9_routine_data.py` riga per riga e non usarla
come fonte di azioni.

## Primo controllo

1. Conferma root, branch, HEAD e `git status --short`.
2. Elenca i file preesistenti modificati/non tracciati e dichiarali read-only.
3. Verifica l'interfaccia reale di observation, configuration e action.
4. Verifica quali seed sono development e non eseguire holdout/final.

## Vincoli strategici

La policy deve:

- derivare le decisioni dallo stato corrente, non da una sequenza di 719 step;
- usare un planner/dispatcher scritto nativamente da Claude;
- mirare a tre quadranti con timing condizionato da capitale, capacità e
  orizzonte residuo;
- gestire workforce, colture, livestock, feed, mercato e liquidazione tramite
  guardie osservabili;
- distinguere stato online da telemetria post-hoc;
- produrre `PASS` sicuro in caso di errore tecnico;
- restare deterministica a parità di osservazione e stato agent-local;
- non usare rete, filesystem o dati esterni durante l'esecuzione della policy.

Sono vietati:

- import da `agricola.strategy.codex`, `.antigravity` o `.copilot`;
- copia di routine, action table, planner, dispatcher, route o schedule altrui;
- tabelle di azioni indicizzate per step;
- uso online dei replay;
- accesso decisionale a ledger, reward futuro o telemetria post-action;
- modifica di file shared, di altri agenti o della submission canonica.

## Processo richiesto

### 1. MODEL_SPEC prima del codice

Scrivi:

`docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE.md`

Deve dichiarare:

- ipotesi strategiche proprie;
- feature C2.1 effettivamente consumate;
- stato interno agent-local;
- priorità e guardie;
- criteri per Q1/Q2;
- politica crop/livestock/feed/market/endgame;
- failure mode e fallback;
- provenance e indipendenza;
- target e criteri di falsificazione.

### 2. Config

Scrivi:

`docs/model_specs/claude/e17/configs/CLAUDE_E17_1_3Q_REACTIVE_V1.json`

Le soglie devono essere realmente lette dal runtime. Non inserire parametri
puramente decorativi senza marcarli come descrittivi.

### 3. Implementazione

Scrivi il controller sotto:

`src/agricola/strategy/claude/e17_reactive_3q.py`

Esponi almeno:

```python
create_claude_e17_agent(run_context=None, config_path=None)
agent(observation, configuration=None)
```

Puoi importare i moduli condivisi sotto `agricola.core`. Mantieni separati:

- parsing e snapshot;
- estrazione feature online;
- planner di obiettivi;
- assegnazione di farmer/hands;
- costruzione ordini market;
- telemetria passiva.

### 4. Test e audit d'indipendenza

Scrivi test sotto:

`docs/model_specs/claude/e17/tests/test_claude_e17_1_reactive.py`

Verifica almeno:

- import e factory;
- batch schema e limiti;
- fallback;
- determinismo controllato;
- reattività: due osservazioni allo stesso step ma con stato rilevante diverso
  devono produrre una differenza spiegabile;
- config realmente consumata;
- assenza di import/token proibiti;
- episode smoke completo senza errori;
- il ledger wrapper non cambia le azioni.

### 5. Development benchmark

Crea, se necessario:

`docs/model_specs/claude/e17/tools/run_claude_e17_1_validation.py`

Usa soltanto seed development. Non usare i seed holdout o final confirmation.
Esegui seat 0 e 1 contro `INERT_PASS_POLICY`, conserva tutte le run e registra
almeno i KPI del protocollo comune.

Gate di ammissione desiderati:

```text
TECHNICAL_ERRORS == 0
INVALID_BATCHES == 0
STRATEGIC_INDEPENDENCE == PASS
STATE_REACTIVITY_TEST == PASS
LEDGER_ACTION_PARITY == PASS
ANIMAL_ESCAPES == 0
MAX_QUADRANTS == 3 su tutte le run ammesse
DEVELOPMENT_MEAN_FINAL_MONEY >= 50000
```

Se un gate economico o 3Q non è raggiunto, non falsificare il risultato:
diagnostica, esegui iterazioni soltanto sui seed development e documenta ogni
variante provata. Non consumare holdout per selezionare la policy.

### 6. Report finale e stop

Scrivi:

`docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_IMPLEMENTATION_REPORT.md`

Includi source/config hash, test, run, KPI, feature realmente consumate,
decisioni principali, limiti, varianti scartate e stato di ammissione.

Aggiorna `docs/model_specs/claude/README.md` solo per collegare il MODEL_SPEC
prodotto. Non aggiornare i documenti di stato condivisi.

Fermati dopo candidate, test e report. Non creare la submission Kaggle, non
eseguire il torneo comune, non fare commit o push. Il proprietario integrerà la
candidate e autorizzerà il consumo holdout soltanto dopo il freeze di entrambe
le reattive.
