# E17 — Review indipendente della strategia (Copilot)

- **Reviewer:** Copilot
- **Oggetto:** `experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md`
- **Data:** 2026-09-02
- **Decisione:** `ACCEPT_WITH_CHANGES`
- **Freeze-ready:** `NO`
- **Policy o E17.0 implementati:** `NO`

## 1. Sintesi del verdetto

Il draft adotta correttamente ledger-before-policy, separazione fra evidenza osservata/derivata, seed preregistrati, entrambi i seat, ablation monofattoriali ed esclusione delle baseline derivative dal torneo indipendente. È quindi una base valida per il freeze, ma non è ancora un protocollo eseguibile senza decisioni post-hoc.

Prima del freeze sono indispensabili definizioni normative su identità e denominatore dei record, attribuzione degli outcome di mercato, consumo di holdout/final, artefatti opponent, regole di promozione e separazione fra parità Codex e costruzione della baseline Copilot nativa. L'accettazione è condizionata all'inclusione di queste correzioni nel documento frozen e nel manifest comune.

## 2. Completezza del ledger

**Valutazione: parzialmente completa.** I campi minimi coprono contesto episodico, pre/post state, valori economici, outcome e provenance. Mancano però contratti necessari per ottenere una copertura confrontabile e auditabile:

1. un `command_id` deterministico e un `command_index` nell'action batch, oltre a un hash del batch richiesto, per distinguere comandi omonimi nello stesso step;
2. il denominatore normativo di `LEDGER_RECORD_COVERAGE`: tutti gli step, tutti i comandi emessi, `PASS`, unità senza comando, market orders e fallback devono essere classificati senza doppio conteggio;
3. tipi e serializzazione canonica di fingerprint, inventory e tile/asset state, inclusi ordinamento, valori assenti e versione dello schema;
4. semantica dispositiva degli outcome: `EXECUTED` se esiste un effetto attribuibile, `NOT_EXECUTED` solo con prova sufficiente, `UNKNOWN` negli altri casi; per fill parziali occorrono quantità requested/executed e regola esplicita di classificazione;
5. `outcome_evidence_code`, fonte osservativa e confidence/limite di attribuzione, non soltanto testo libero;
6. separazione tra `MARKET_RECORD_COVERAGE` e `MARKET_CLASSIFIED_OUTCOME_COVERAGE`. Il secondo non può essere portato artificialmente al 100% convertendo `UNKNOWN`;
7. definizione della parità finale Codex: action batch hash per 719/719 step, reward, stato terminale, errori e fallback, confrontati con un run baseline non strumentato sullo stesso seed/seat/opponent.

La telemetria condivisa è ammissibile solo come infrastruttura neutrale, append-only e fuori dal decision path. Il freeze deve includere un test esplicito di non-interferenza.

## 3. Seed, holdout, opponent e gate

### Seed e holdout

Le liste holdout e final corrispondono alla derivazione SHA-256 dichiarata usando gli indici `i=0..5` e `i=0..3`; development, holdout e final sono disgiunti. I development seed sono correttamente classificati come già osservati.

Il draft deve però congelare una policy di consumo: chi può sbloccare i risultati, quando un set si considera consumato, dove viene registrato il primo accesso e cosa accade dopo un fallimento. Una candidata modificata dopo avere visto il holdout non può riusare lo stesso holdout come validazione indipendente. Il final confirmation deve essere one-shot per la candidata già promossa, senza tuning successivo presentato come conferma.

### Opponent e schedule

I livelli A–E sono appropriati, ma i nomi degli opponent non bastano. Il manifest deve fissare per ogni livello:

- policy ID, source/config/freeze SHA-256 e ruolo dell'opponent;
- matrice seed × seat × opponent, numero di episodi e regola di pairing;
- ordine dei match o regola deterministica di generazione;
- trattamento di crash, timeout, opening failure e run ripetuti;
- denominatore invariabile: nessun episodio fallito viene escluso o sostituito.

`INERT_PASS_POLICY`, Codex V9 e ogni freeze usata in mirror devono essere artefatti esatti, non etichette logiche. Il Livello D resta chiuso finché almeno due policy non superano un audit di indipendenza.

### Gate

Gli assoluti tecnici sono corretti, ma la promozione non è ancora completamente preregistrata. Il freeze deve specificare aggregazione per seed/seat/opponent, confronto paired contro la baseline, non-inferiorità del floor, gestione di parità e varianza e precedenza fra gate assoluti e target economici. I target numerici Codex non possono fungere automaticamente da gate Copilot: servono criteri comuni di eligibility e target agent-local dichiarati prima dei run.

`ANIMAL_ESCAPES == 0` va definito come conteggio `DERIVED_EOD_ESCAPE_COUNT == 0` tramite estrattore/versione congelati. `SOURCE_CONFIG_FREEZE` deve elencare manifest, hash e autorità di freeze. Un esperimento che fallisce può restare `INFORMATIVE_ONLY`; rollback significa non promozione, non cancellazione dell'evidenza.

## 4. Rischio di confondimento fra fattori

L'ordine effetti principali → interazioni → composita è corretto, ma alcune RQ richiedono una definizione più stretta dei trattamenti:

- **RQ1 WHEAT:** congelare trigger, singolo comando sostituito, quantità massima e azioni non modificabili; altrimenti recovery, capitale e timing cambiano insieme.
- **RQ2 topologia:** congelare conteggi asset, specie, budget, timing di build e schedule di servizio; coordinate e routing sono il trattamento, mentre i loro effetti sul MOVE sono mediatori ammessi.
- **RQ3/RQ6 timing Q2:** distinguere acquisto del quadrante, attivazione e popolamento. Anticipare più di uno di questi eventi introduce trattamenti multipli; capitale e ciclo produttivo conseguenti devono essere dichiarati mediatori, non fattori “congelati”.
- **RQ4 chiusura:** delimitare la mutazione ai comandi di vendita D26–D29 e dichiarare invarianti servicing animale e produzione precedente.
- **RQ5 diversificazione:** scegliere `aggiunta` oppure `sostituzione` per singola candidata; specie, quantità, costo e superficie non possono cambiare simultaneamente senza un contrasto separato.
- **Densità, servicing e capitale:** il draft li cita come dimensioni, ma non assegna livelli operativi completi o una RQ autonoma. Devono essere congelati come covariate oppure introdotti come fattori con livelli e gate propri prima di preregistrare interazioni.

Per ogni RQ il frozen design deve contenere un diff contrattuale: fattore manipolato, invarianti hashabili, mediatori ammessi, outcome primario, falsificazione e stop rule.

## 5. Indipendenza strategica Copilot

La Copilot V2 corrente è dichiaratamente derivativa e fallisce il gate: importa la routine Codex, non possiede working set/planner/schedule nativi e non può entrare nel Livello D.

E17.0 deve distinguere due deliverable senza confonderli:

1. **measurement parity:** validazione del ledger su una baseline congelata, senza attribuire indipendenza alla V2;
2. **baseline Copilot nativa:** nuovo policy ID, source, config, design, freeze e provenance agent-local, senza importazione, copia o trascrizione di routine/action table/planner/dispatcher/schedule altrui.

La baseline nativa Copilot non deve dimostrare parità 719/719 con Codex: deve dimostrare conformità al protocollo, copertura del ledger, assenza di errori e indipendenza. La parità comportamentale esatta resta un requisito della sola strumentazione Codex V9. Sono condivisibili Foundation, observation contract, schema ledger e harness neutrale; non lo è la deliberazione.

Prima del torneo servono un audit indipendente di import/dipendenze, provenance del design, hash distinti e una review che verifichi l'assenza di riuso semantico oltre al semplice `NO_IDENTICAL_ROUTINE_SHA`.

## 6. Correzioni indispensabili prima del freeze

1. rendere normativo lo schema ledger con tipi, identità record, denominatori e regole per partial fill/`UNKNOWN`;
2. congelare nel manifest opponent, hash, schedule, pairing e gestione degli errori;
3. aggiungere il registro one-shot di consumo holdout/final e il divieto di riuso dopo osservazione;
4. definire regole statistiche di promozione/non-inferiorità e separare target comuni da target agent-local;
5. aggiungere per ogni RQ trattamento, invarianti, mediatori ammessi e diff hashabile;
6. separare formalmente parità Codex e baseline nativa Copilot/Antigravity;
7. congelare checklist e reviewer del `STRATEGIC_INDEPENDENCE_GATE` prima del Livello D;
8. sostituire l'ambiguo market coverage 100% con record coverage 100% più classification coverage dichiarata senza falsificare `UNKNOWN`.

## 7. Decisione finale

```text
E17_STRATEGY_REVIEW: ACCEPT_WITH_CHANGES
FREEZE_READY: NO
REQUIRED_CHANGES_BEFORE_FREEZE: 8
LEDGER_COMPLETENESS: PARTIAL
SEED_DERIVATION: PASS
HOLDOUT_GOVERNANCE: CHANGE_REQUIRED
OPPONENT_FREEZE: CHANGE_REQUIRED
CAUSAL_ISOLATION: CHANGE_REQUIRED
STRATEGIC_INDEPENDENCE_GATE_COPILOT_CURRENT: FAIL_DERIVATIVE_BASELINE
E17_0_IMPLEMENTATION_STATUS: NOT_STARTED
POLICY_MUTATION: NO
KAGGLE_SUBMISSION: NO
```

Dopo il recepimento delle otto correzioni, il draft può essere riconciliato e congelato. Nessuna implementazione E17.0 è autorizzata da questa review.
