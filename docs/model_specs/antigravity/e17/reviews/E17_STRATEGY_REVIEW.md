# E17 Strategy Review — Antigravity

Data: 2026-09-02
Reviewer: Antigravity
Oggetto: `experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md`
Verdetto: `ACCEPT_WITH_CHANGES`

## Sintesi

Il draft è metodologicamente solido e, nel complesso, compatibile con il
prompt comune E17. La separazione fra benchmark osservazionale, ablation
monofattoriali, interazioni preregistrate e freeze prima di E17.0 è corretta.
Sono inoltre condivisi i punti più importanti per Antigravity:

- nessun archetipo Top 3 viene promosso a candidato da copiare;
- il ledger requested/executed precede ogni mutazione di policy;
- `Crop Dusta` resta una frontiera da testare, non una prova causale;
- le baseline derivative non possono essere presentate come strategie
  indipendenti.

Il documento è quindi accettabile come base di freeze, ma richiede alcune
correzioni prima della promozione a `E17_STRATEGY_FROZEN_V1.md`.

## 1. Completezza del ledger

Valutazione: `ADEGUATA CON CHIARIMENTO RICHIESTO`

Punti positivi:

- il ledger minimo richiesto dal prompt comune è integralmente recepito;
- la distinzione `EXECUTED | NOT_EXECUTED | UNKNOWN` è corretta;
- il draft aggiunge opportunamente quantità richiesta, quantità attribuita,
  prezzo/cash delta e motivo dell'eventuale `UNKNOWN` per il mercato;
- è esplicitato che la telemetria deve restare fuori dal decision path.

Chiarimento indispensabile:

- il testo usa sia `MARKET_OUTCOME_COVERAGE: 100% prima di E17.1` sia la
  formulazione del prompt comune secondo cui le ambiguità non vanno convertite
  forzatamente. Prima del freeze va esplicitato che:
  `LEDGER_RECORD_COVERAGE == 100%` è obbligatorio in E17.0, mentre
  `EXECUTED_MARKET_LEDGER_COVERAGE == 100%` è un target/gate successivo solo
  se la classificazione completa è realmente dimostrabile senza falsi positivi.

In assenza di questo chiarimento il draft rischia di confondere:

- copertura del record;
- copertura della classificazione esecutiva;
- quota di eventi che devono restare `UNKNOWN`.

## 2. Seed, holdout, opponent e gate

Valutazione: `FORTE`

Punti positivi:

- la separazione fra development, holdout e final confirmation è chiara;
- la generazione deterministica dei seed holdout/final è buona e auditabile;
- entrambi i seat sono richiesti esplicitamente;
- i livelli A–E distinguono bene contract, economia passiva, mirror, torneo
  indipendente e Kaggle;
- i gate assoluti (`TECHNICAL_ERRORS == 0`, `ANIMAL_ESCAPES == 0`,
  `LEDGER_RECORD_COVERAGE == 100%`, `SOURCE_CONFIG_FREEZE == true`) sono
  appropriati.

Osservazione:

- i target finali numerici restano fortemente centrati su Codex, il che è
  legittimo per il primo ramo E17 ma va tenuto semanticamente separato dal
  protocollo comune. Non è un blocker, purché il frozen distingua bene:
  protocollo comune condiviso vs target prestazionali del ramo Codex.

## 3. Rischio di confondimento fra fattori

Valutazione: `BASSO`

Punti positivi:

- l'ordine `RQ0 -> RQ6` è sensato;
- la regola “una sola famiglia causale per candidata” è corretta;
- le interazioni sono posticipate fino a dopo gli effetti principali;
- il contrasto `D11 / D10 / D8` è separato dalla topologia;
- la diversificazione è giustamente spezzata in modifiche singole, non in
  ricombinazione integrale del mix dei vincitori.

Questa è la parte migliore del draft: evita esplicitamente il cherry-picking
post-hoc e tiene separati timing, topologia, diversificazione, capitale e
chiusura.

## 4. Indipendenza strategica

Valutazione: `CORRETTA MA DA IRROBUSTIRE NEL TIMING`

Punti positivi:

- il draft riconosce senza ambiguità che Antigravity V4 e Copilot V2 sono
  baseline derivative;
- il divieto di import/copia di routine, planner, dispatcher o action table è
  coerente con il prompt comune e con il MODEL_SPEC Antigravity corrente.

Correzione indispensabile prima del freeze:

- il prompt comune B3 colloca per Antigravity e Copilot il lavoro di baseline
  nativa già dentro E17.0, non genericamente “prima del torneo E17”.
- il draft deve quindi allineare la formulazione temporale e dire in modo
  esplicito che:
  1. E17.0 per Antigravity include la costruzione di una baseline 3Q nativa;
  2. la provenance della baseline nativa va documentata già negli output E17.0;
  3. nessun report comparativo a tre agenti può essere interpretato come
     confronto indipendente finché `STRATEGIC_INDEPENDENCE_GATE` non passa.

Senza questa precisazione il documento resta corretto nel principio ma troppo
debole sul punto operativo più importante per Antigravity.

## 5. Correzioni indispensabili prima del freeze

1. Allineare il paragrafo sull'indipendenza strategica al prompt comune:
   per Antigravity e Copilot la baseline nativa e la relativa provenance devono
   entrare esplicitamente nel perimetro di `E17.0`, non essere rinviate a una
   soglia temporale successiva e generica.

2. Chiarire il gate del market ledger:
   `LEDGER_RECORD_COVERAGE == 100%` in E17.0 è obbligatorio;
   la quota di ordini classificati `EXECUTED` non deve essere gonfiata
   artificialmente, e gli `UNKNOWN` devono restare ammessi finché non esiste
   evidenza osservativa sufficiente.

3. Distinguere nel frozen, anche a livello lessicale, fra:
   - protocollo comune E17;
   - target prestazionali specifici del ramo Codex.
   Questo evita che un documento comune sembri prescrivere una roadmap Codex
   come se fosse già la roadmap implementativa degli altri agenti.

## 6. Decisione finale

```text
REVIEW_DECISION: ACCEPT_WITH_CHANGES
LEDGER_COMPLETENESS: ACCEPT_WITH_CHANGES
SEED_HOLDOUT_OPPONENT_GATE_VALIDITY: ACCEPT
CONFOUNDING_RISK: ACCEPT
STRATEGIC_INDEPENDENCE: ACCEPT_WITH_CHANGES
FREEZE_READY: NO
REQUIRED_FIXES_BEFORE_FREEZE: 3
POLICY_IMPLEMENTATION_STARTED: NO
E17_0_IMPLEMENTATION_STARTED: NO
```

## 7. Conclusione

Il draft è abbastanza forte da non richiedere un rigetto. La struttura
causale, il protocollo seed/seat e la disciplina epistemologica sono corretti.
Le modifiche richieste sono mirate e servono soprattutto a evitare un freeze
troppo permissivo sul punto di maggiore sensibilità per Antigravity:
indipendenza strategica reale già in E17.0, con ledger di mercato rigoroso ma
senza forzare classificazioni non osservabili.
