# E17.1 — Sviluppo reattivo e torneo a tre

- **Data:** 2026-09-02
- **Stato:** AUTHORIZED FOR IMPLEMENTATION
- **Autorizzazione:** `experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md`
- **Submission Kaggle:** NOT AUTHORIZED

## 1. Obiettivo

Mantenere la Codex V9 come controllo permanente e confrontarla con due policy
reattive:

| ID logico | Natura | Relazione con V9 |
|---|---|---|
| `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY` | controllo open-loop congelato | baseline |
| `CODEX-E17.1-3Q-REACTIVE-GUARDED-V1` | evoluzione reattiva Codex | derivativa dichiarata |
| `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V1` | planner reattivo Claude | strategicamente indipendente |

Il torneo deve misurare sia la robustezza della routine precompilata sia il
valore e il costo della reattività. Non assume che la reattività sia sempre
superiore.

## 2. Ipotesi

- `H-CODEX-R`: una guardia locale reattiva può ridurre divergenze da mercato o
  stato mantenendo il nucleo economico della V9.
- `H-CLAUDE-R`: una policy nativa che usa stato corrente e planning agent-local
  può raggiungere una traiettoria 3Q robusta senza copiare schedule altrui.
- `H-OPEN`: la V9 può mantenere un vantaggio quando il costo decisionale o gli
  errori del planner superano il beneficio dell'adattamento.

## 3. Confini di indipendenza

La candidate Codex reattiva può chiamare la V9 come provider dell'azione di
default, perché è una sua evoluzione dichiarata. Deve comunque registrare ogni
override e la feature che lo ha attivato.

La candidate Claude può condividere soltanto:

- Foundation C2.1 e fatti engine;
- `agricola.core.observation_contract`;
- schema del ledger E17;
- protocolli, metriche e replay pubblici come evidenza di discovery;
- action schema pubblico dell'ambiente.

Non può importare o copiare codice sotto gli altri namespace strategy, routine
da replay, tabelle indicizzate per step o schedule ricostruiti da un altro
agente. Il suo comportamento deve derivare da osservazione corrente, stato
agent-local e regole proprie.

## 4. Interfaccia comune

Ogni candidata deve esporre una factory che restituisce una callable:

```python
policy = create_agent(run_context=None, config_path=None)
action = policy(observation, configuration)
```

L'azione deve avere sempre la forma:

```python
{"farmer": ["PASS"], "hands": [], "market": []}
```

con un comando farmer, al massimo un comando per hand e non più del limite di
ordini market dichiarato dalla configurazione.

## 5. Fasi

### A. Development

- usare esclusivamente i seed `development` del manifest E17.0;
- consentire smoke test, unit test e benchmark contro opponent inert;
- non usare holdout o final confirmation;
- non modificare la baseline V9.

### B. Admission e freeze

Ogni reattiva deve produrre:

- MODEL_SPEC as-built;
- config;
- source agent-local;
- test tecnici e di indipendenza;
- report di sviluppo;
- hash di source e config;
- zero errori tecnici su un episode completo;
- prova di attivazione 3Q oppure spiegazione verificata del mancato gate.

Claude deve inoltre superare una scansione che escluda import/copie dagli altri
namespace strategici. Codex deve dichiarare esplicitamente la dipendenza dalla
V9 e contare gli override.

### C. Tournament

Solo dopo il freeze di entrambe le candidate:

1. eseguire benchmark passivo di tutte e tre contro lo stesso opponent;
2. consumare una volta i sei seed holdout già preregistrati;
3. eseguire round-robin sui tre pair, scambiando i seat per ogni seed;
4. non rimuovere run e non ritoccare le policy dopo aver visto l'holdout;
5. conservare ledger, summary, hash e primo punto di divergenza.

La matrice round-robin contiene:

```text
3 coppie × 6 seed × 2 orientamenti di seat = 36 match
```

I quattro seed `final_confirmation` restano non consumati.

## 6. Metriche

Metriche tecniche:

- errori e fallback;
- validità dei batch;
- lunghezza episodio;
- hash delle sequenze;
- copertura del ledger;
- primo step e causa di divergenza.

Metriche operative:

- giorno/step di attivazione Q1 e Q2;
- massimo e profilo temporale degli hands;
- tile coltivate, pascoli e tile finali non produttive per quadrante;
- mix di colture e animali;
- stock WHEAT, feed richiesti, fughe derivate;
- azioni MOVE, produttive e PASS;
- ordini market requested/executed/unknown;
- inventario terminale e final money.

Metriche competitive:

- vittorie, sconfitte e pareggi;
- reward per seed e seat;
- media, mediana, minimo, deviazione standard;
- sensibilità al seat;
- confronto matched-pair con la baseline V9.

## 7. Interpretazione

- V9 vs Codex reattivo: confronto diretto con baseline derivativa; attribuzione
  causale valida soltanto se la candidate cambia una famiglia di guardie.
- V9 vs Claude reattivo: confronto tra architetture, non ablation.
- Codex reattivo vs Claude reattivo: confronto tra adattamento incrementale e
  planning reattivo indipendente.
- Il testa-a-testa è influenzato dalla contesa. Il benchmark passivo matched
  contro lo stesso opponent resta necessario per separare capacità economica e
  interazione competitiva.

## 8. Stop boundary

```text
EDIT_CANONICAL_SUBMISSION: FORBIDDEN
KAGGLE_UPLOAD: FORBIDDEN
ANTIGRAVITY_OR_COPILOT_MUTATION: FORBIDDEN
HOLDOUT_BEFORE_BOTH_FREEZES: FORBIDDEN
POST_HOC_SEED_REMOVAL: FORBIDDEN
COMMIT_OR_PUSH: NOT_AUTHORIZED_BY_THIS_DESIGN
```
