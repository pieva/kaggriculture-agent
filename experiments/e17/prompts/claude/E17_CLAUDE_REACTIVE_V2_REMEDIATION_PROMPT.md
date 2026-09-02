# Prompt Claude — remediation E17.1 Reactive V2

Lavora come owner esclusivo della policy Claude. Leggi integralmente:

1. `docs/NEW_SESSION.md`;
2. `experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V1_FAILED_GATE_REPORT.md`;
3. `experiments/e17/reviews/common/E17_REACTIVE_TOURNAMENT_CANDIDATE_AMENDMENT_1.md`;
4. `experiments/e17/artifacts/derived/claude/E17_1_METRICS.json`;
5. i summary e ledger V1 sotto
   `experiments/e17/artifacts/runs/claude/e17_1/`;
6. la Foundation C2.1 e il tuo MODEL_SPEC V1.

## Obiettivo

Costruisci una nuova policy
`CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2` che superi su tutti i sette seed
development e su entrambi i seat:

```text
TECHNICAL_ERRORS == 0
INVALID_BATCHES == 0
STRATEGIC_INDEPENDENCE == PASS
STATE_REACTIVITY == PASS
LEDGER_RECORD_COVERAGE == 100%
DERIVED_EOD_ESCAPES == 0
MAX_QUADRANTS == 3 IN ALL RUNS
MEAN_FINAL_MONEY >= 50000
```

Non usare seed holdout o final confirmation. Non eseguire il torneo.

## Diagnosi da verificare, non da assumere

La V1 ottiene media `9201.7143`, range `5415..13625`, e otto fughe. Nel primo
run richiede circa 3.369 MOVE contro 621 azioni produttive e 156 `HIRE`.
Verifica nel ledger requested/executed quali richieste falliscono e perché.
Tratta come ipotesi:

- oscillazione da dispatcher stateless;
- target non persistenti e percorsi lunghi;
- `HIRE` ripetuti senza cash o senza necessità;
- espansione Q1/Q2 prematura rispetto al motore Q0;
- densità/resa insufficiente per tile;
- guardie feed incapaci di garantire zero fughe.

Correggi le cause confermate. È ammesso stato agent-local persistente per
ruolo/target/coda breve, purché derivi da osservazioni correnti, si invalidi
quando il target cambia e non diventi una tabella indicizzata per step.

## Indipendenza obbligatoria

Non importare, leggere per copiare o trascrivere:

- `agricola.strategy.codex`;
- `agricola.strategy.antigravity`;
- `agricola.strategy.copilot`;
- `ROUTINE_ACTIONS`, routine replay-derived, schedule o planner altrui;
- `submission/submission_codex.py`.

Puoi usare Foundation C2.1, observation contract, ledger, fatti engine e la
tua evidenza V1. Il target 50k non autorizza a derivare la V2 dalla routine
Codex.

## Orientamento tecnico

Mantieni la decisione reattiva, ma valuta queste correzioni sulla tua
architettura:

1. avvia un nucleo Q0 compatto e redditizio prima di acquistare Q1/Q2;
2. espandi soltanto con capitale e capacità di servizio osservati;
3. assegna target persistenti ai worker per evitare oscillazioni;
4. misura requested/executed di `HIRE` e limita i retry;
5. porta gradualmente la forza lavoro al livello richiesto dalla superficie,
   senza assumere che sei hands siano sufficienti;
6. non introdurre animali finché feed e servicing non garantiscono zero fughe;
7. usa liquidazione terminale reattiva e riduci spostamenti non produttivi;
8. esegui ablation development documentate, senza rimuovere seed sfavorevoli.

Sono direzioni di ricerca, non una routine da copiare. Decidi tu regole,
topologia, colture, animali, timing e priorità.

## Output obbligatori V2

- `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V2.md`;
- `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V2.json`;
- `src/agricola/strategy/claude/e17_reactive_3q_v2.py`;
- `experiments/e17/tests/test_claude_e17_1_reactive_v2.py`;
- `experiments/e17/tools/claude/run_claude_e17_1_v2_validation.py`;
- `experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V2_IMPLEMENTATION_REPORT.md`;
- metrics e freeze V2 in directory separate dalla V1.

Il runner V2 deve impedire programmaticamente seed holdout/final, produrre
metriche per tutte le run e scrivere `FROZEN_FOR_REACTIVE_TOURNAMENT` soltanto
se ogni gate è superato. Se fallisce, usa `FROZEN_WITH_FAILED_GATES` e fermati
senza consumare holdout.

## Stop boundary

Fermati dopo report e freeze V2. Non modificare file Codex, submission
canonica, Antigravity o Copilot. Non fare commit, push, upload Kaggle o torneo.
