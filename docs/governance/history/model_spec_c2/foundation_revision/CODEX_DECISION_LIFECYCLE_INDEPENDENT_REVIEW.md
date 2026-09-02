# KAGGRICULTURE C2 — Codex Decision Lifecycle Independent Review

```text
DOCUMENT_ID: CODEX_DECISION_LIFECYCLE_INDEPENDENT_REVIEW
REVIEWER: CODEX
DATE: 2026-08-31
REVIEW_TARGET: docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md
TARGET_VERSION: C2-DRAFT-01
REVIEW_MODE: INDEPENDENT / REVIEW ONLY
```

## 1. Executive Verdict

Il Decision Lifecycle Contract ha una base architetturale valida: separa correttamente stato ambientale e stato deliberativo, mantiene le scelte strategiche nei `MODEL_SPEC`, formalizza la quadripartizione dell'evidenza, tratta `REACT` come intake di eventi e `VERIFY` come attività ricorrente, e distingue nominalmente completion, repair, invalidation, cancellation, supersession e terminal closure.

Il draft non è tuttavia congelabile. Esiste un blocker strutturale nella supersession: l'ingresso in `SUPERSEDED` richiede un `successor_decision_id`, ma la sequenza normativa permette di creare la decisione successiva soltanto dopo `SUPERSEDED → REVIEW_READY → DECISION_OPEN → DEFINED`. Senza una regola di preallocazione o una sequenza diversa, il normale caso di sostituzione formale ha una dipendenza circolare.

Sono inoltre aperte ambiguità maggiori sulla copertura terminale di tutti gli stati, sulla precedenza tra completion/invalidation/terminal, sulla distinzione `INFEASIBLE`/`REJECTED`, sul fallimento del repair, sulla governance di cancellation e supersession rispetto all'anti-oscillation, sulla feasibility batch/serializzata, sul record VERIFY, sulla temporalità degli snapshot, sulla provenance e sull'effettiva conclusione della REVIEW prima della riapertura.

Verdetto:

```text
DECISION_LIFECYCLE_REVIEW: FAIL_WITH_BLOCKERS
P0_OPEN: 1
P1_OPEN: 10
P2_OPEN: 2
DECISION_LIFECYCLE_FREEZE_RECOMMENDED: NO
```

Non è stata individuata una regola strategica agricola prescritta dal DLC e non è presente future leakage esplicito. Il problema è l'insufficiente determinismo e auditabilità del protocollo, non la qualità di una particolare strategia.

## 2. Documents Reviewed

### Documenti obbligatori

| Documento | Ruolo | SHA-256 |
|---|---|---|
| `docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md` | Oggetto della review | `c16164d352afb2735234058871765f6fad2fd5fb6be1309d41b532e1fd8919b7` |
| `docs/foundation/ontology/ONTOLOGY_C2.md` | Foundation frozen — vocabolario | `5f345cdf7d533a28bb3f6bd429ae2245aec13a18fd586b9b5645fa73a39a9aa8` |
| `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md` | Foundation frozen — transizioni ambiente | `79e8133d7b0f555f202dad37b3a88160ae5174e5cf72d0693fbc91c5a61b2f4a` |
| `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md` | Foundation frozen — osservabilità e feature | `b0f1cec133d9a9142e6b69e565491373c3b622bbcba48606b8e23fb5df516e59` |
| `docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md` | Frozen Engine Contract | `47dbdf9e0a9100483654951f8cdc61fc80e6225481b776818622ef0c15d1f1d5` |
| `docs/governance/history/model_spec_c2/foundation_revision/CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md` | Frozen Period Ledger / evidence timing baseline | `1c3ffc2dc5039caee0d5c9b5100775278d2b8cb7c062aa9b3952337d6d289c8e` |
| `docs/governance/history/model_spec_c2/foundation_revision/FOUNDATION_CROSS_REVIEW_RECONCILIATION.md` | Canonical correction/reconciliation authority | `ed71ec24070b91834ac81722f135800f9acb30581b78d5c0f0614ed702511fb1` |
| `docs/governance/history/model_spec_c2/foundation_revision/FOUNDATION_FINAL_FREEZE_REVIEW.md` | Foundation freeze authority | `25dd46b3a2af907aa84a559be0c8c52c1f973303364555781a6aadd0df33988a` |
| `README.md` | Architettura di progetto | `cb29639aaeb51b1cbc046fe123d7b784fd643678e1e9cc3fa7ebbb760ca0293b` |

### Indipendenza e non-scope

- Non è stata consultata la review indipendente del DLC prodotta da Antigravity.
- Non sono stati modificati DLC, Engine Contract, Ontology, State Machine, Feature Model, README, `MODEL_SPEC` o codice.
- Non sono stati eseguiti benchmark, tournament o Kaggle.
- La review non propone crop mix, livestock mix, obiettivi economici, soglie o altra policy di gioco.

## 3. Foundation Alignment

Il DLC è correttamente collocato a valle del Feature Model e a monte dei `MODEL_SPEC`. La distinzione

```text
S_t = stato ambiente
D_t = stato deliberativo
```

è esplicita e impedisce di confondere una transizione cognitiva con una mutazione engine. Anche la catena

```text
ACTION_REQUEST
→ SNAPSHOT_ELIGIBILITY
→ EXECUTION_OUTCOME
→ POST_STATE_EVIDENCE
```

è coerente con la Foundation frozen.

L'allineamento non è ancora completo per tre ragioni:

1. il Feasibility Contract non incorpora normativamente la distinzione tra `ACTION_ELIGIBLE_NOW`, fattibilità atomica di batch, effetti della serializzazione e `RESERVED_SERVICEABLE_BEFORE_DEADLINE` come `POLICY_CONTEXT`;
2. il record VERIFY non contiene `snapshot_eligibility_id` e non definisce quando i link a request/outcome siano obbligatori;
3. lo schema deliberativo non ancora associa ogni transizione a un decision boundary e a un `available_at` verificabile, necessario per applicare in replay la separazione temporale Foundation.

Non è necessario né consentito riaprire la Foundation per risolvere questi punti: sono correzioni del DLC.

## 4. State Machine Review

| Stato | Semantica / entry | Exit e copertura | Esito |
|---|---|---|---|
| `DECISION_OPEN` | Punto deliberativo senza nuovo commitment; ingresso iniziale o dopo review. | `DEFINED` e `TERMINAL_CLOSED` sono sufficienti. | **PASS** |
| `DEFINED` | Intent identificato e non committed. | Le uscite principali esistono, ma `INFEASIBLE` e `REJECTED` si sovrappongono per `FEASIBILITY_REJECTION`. | **AMBIGUOUS** |
| `PLAN_FEASIBLE` | Gate agent-specific superato su snapshot dichiarato. | Manca una regola di freshness/revalidation prima di COMMIT; l'uscita verso `REJECTED` non è distinta dall'infeasibility. | **AMBIGUOUS** |
| `INFEASIBLE` | Piano candidato con feasibility `FAIL`. | L'unica uscita è `DECISION_OPEN`; manca terminal edge e la semantica collide con `REJECTED`. | **AMBIGUOUS** |
| `REJECTED` | Abbandono pre-commit. | `FEASIBILITY_REJECTION` duplica `INFEASIBLE`; manca terminal edge. | **AMBIGUOUS** |
| `COMMITTED_EXECUTING` | Commitment attivo con VERIFY ricorrente. | Ampia copertura, ma non esiste precedenza tra completion, invalidation, cancellation, supersession e terminal. | **AMBIGUOUS** |
| `REPAIR_WITHIN_COMMITMENT` | Intent, identity e strategic scope invariati; variazione esecutiva locale. | Un repair fallito è disegnato come invalidation anche senza invalidator; mancano self-loop, completion e record minimo del repair. | **FAIL** |
| `INVALIDATED` | Un invalidator dichiarato è stato provato da evidenza. | L'uscita verso review è corretta; manca gestione terminale interposta. | **AMBIGUOUS** |
| `CANCELLED` | Chiusura volontaria senza impossibilità necessaria. | Il percorso verso review è corretto, ma la policy di cancellazione non è registrata/previncolata e manca terminal edge. | **AMBIGUOUS** |
| `SUPERSEDED` | Il commitment precedente viene sostituito formalmente. | L'entry richiede una decisione successiva che la sequenza vieta di creare prima della review. | **FAIL** |
| `COMPLETED` | Completion condition dichiarata soddisfatta. | Il percorso verso review è corretto; non è definita la precedenza su invalidation/terminal simultanei. | **AMBIGUOUS** |
| `REVIEW_READY` | Ciclo operativamente chiuso, evidenza disponibile. | Il passaggio allo stato non prova che la REVIEW sia stata materializzata prima della riapertura; il testo non impone una guardia, mentre il diagramma etichetta l'arco `REVIEW complete`. | **AMBIGUOUS** |
| `TERMINAL_CLOSED` | Stato deliberativo assorbente. | Il divieto di nuovo intent è chiaro; manca il record di disposizione del commitment/plan ancora aperto al terminale. | **AMBIGUOUS** |

Non vi sono dead-end di uscita ordinari dopo l'ingresso negli stati di closure, ma la supersession presenta un deadlock di ingresso e la raggiungibilità terminale non è totale per tutti gli stati.

## 5. REACT / VERIFY Review

### REACT

La scelta di modellare `REACT` come intake/evaluation e non come stato lineare è corretta. Il flusso ammesso

```text
event → update evidence → evaluate guards → retain / repair / invalidate / complete / close
```

non consente formalmente di saltare `DEFINED → PLAN_FEASIBLE → COMMITTED_EXECUTING`. Le classi evento non attribuiscono importanza o soglie e restano strategy-neutral.

Rimane una difformità minore: l'elenco degli effetti ammessi omette `CANCELLED` e `SUPERSEDED`, benché siano uscite canoniche da `COMMITTED_EXECUTING`. Il contratto deve chiarire se tali transizioni possono essere attivate dall'intake oppure soltanto da un comando deliberativo esplicito.

### VERIFY

La scelta di rendere VERIFY un'attività osservativa ricorrente è corretta e il set di risultati non pianifica autonomamente la strategia. Tuttavia il record minimo non realizza completamente la quadripartizione Foundation:

- manca `snapshot_eligibility_id`;
- `action_request_id` ed `execution_outcome_id` sono opzionali senza una cardinalità condizionale;
- “per ogni transition rilevante” non definisce quali transizioni possano essere omesse;
- non è definita la precedenza quando completion e invalidation risultano simultaneamente vere;
- `REPAIR_REQUIRED` identifica un esito, ma non deve selezionare autonomamente il repair: questa responsabilità deve rimanere nel `MODEL_SPEC` e produrre un record separato.

VERIFY non è un secondo planner per intenzione normativa, ma il contratto non è ancora sufficientemente preciso da provarlo in conformance.

## 6. Commitment & Anti-Oscillation Review

`NO_REPLAN_WITHOUT_LIFECYCLE_CAUSE` è un'invariante condivisa legittima: vieta silent mutation e non prescrive durata, orizzonte o soglia del commitment. Gli invalidator pre-dichiarati rendono possibile reagire a evidenza materiale senza riscrivere a posteriori la motivazione originaria.

Il vincolo è però aggirabile attraverso due uscite:

- `CANCELLED` richiede una causa, ma non una `cancellation_policy_version`, una classe di autorità o una regola dichiarata prima del cambio;
- `SUPERSEDED` può essere invocato esplicitamente, ma non richiede un predicato di supersession versionato e soffre inoltre della dipendenza circolare sul successore.

Un agente potrebbe quindi trasformare “preferisco ora un'altra strategia” in una cancellation/supersession formalmente esplicita ma sostanzialmente equivalente al silent replan. La correzione non deve vietare reazioni necessarie: deve rendere distinguibili un invalidator originario, una cancellazione volontaria governata e una sostituzione formale, conservandone policy/versione/evidenza.

Anche `same strategic scope` e `material change` sono necessari ma non operazionalizzati. Il DLC deve standardizzare come il `MODEL_SPEC` dichiara e confronta questi campi, senza stabilirne il contenuto.

## 7. Feasibility Review

Gli esiti comuni `FEASIBLE` e `INFEASIBLE` sono sufficienti. Restano correttamente agent-specific requisiti, horizon, rischio, criteri economici, buffer, margini di reservation e capacity policy.

Il protocollo è però troppo sottospecificato rispetto alla Foundation:

| Concetto Foundation | Trattamento DLC corrente | Esito |
|---|---|---|
| `ACTION_ELIGIBLE_NOW` | Non richiesto come classe distinta nel feasibility record. | **INCOMPLETE** |
| Batch feasibility | Non viene registrato batch ID, domanda aggregata o risultato atomico. | **INCOMPLETE** |
| Serialization effects | Nessun action order o pre-execution snapshot nel gate. | **INCOMPLETE** |
| Multidimensional capacity | Riconosciuta correttamente nella Reservation Envelope. | **PASS** |
| `RESERVED_SERVICEABLE_BEFORE_DEADLINE` | Implicitamente compatibile, ma non dichiarato esplicitamente `POLICY_CONTEXT` e non-garanzia engine. | **AMBIGUOUS** |
| Freshness del gate | Nessuna scadenza o revalidation tra `PLAN_FEASIBLE` e COMMIT. | **INCOMPLETE** |

Il DLC non deve imporre l'algoritmo, ma deve registrare quali classi di controllo sono state eseguite, su quale snapshot/batch/order, e con quale provenance. Una reservation non deve mai diventare un engine fact.

## 8. Evidence Timing / No-Future-Leakage

L'ordine canonico della Sezione 5 è allineato alla Foundation e la regola anti-retroattiva è esplicita. Non sono stati trovati:

- uso online di reward/final money;
- uso anticipato di `POST_STATE_EVIDENCE`;
- uso retroattivo di `EXECUTION_OUTCOME` per giustificare la request precedente;
- review metric presentate come feature online;
- invalidator inventati dopo un outcome e attribuiti al commitment originario.

Pertanto `NO_FUTURE_LEAKAGE` è **PASS** sul piano normativo.

La verificabilità del timing è invece incompleta. La formula generale della Sezione 4,

```text
D_t + evidence(S_t, S_t+1) → D_t+1
```

è troppo ampia per DEFINE/PLAN/COMMIT, che devono usare soltanto evidenza disponibile al rispettivo decision boundary. Gli snapshot non hanno `captured_at_transition_id`, `available_at_decision_boundary_id`, source/target state ID o una regola di immutabilità. Senza questi campi un replay non può provare, soltanto assumere, che l'evidenza fosse disponibile in tempo.

## 9. Repair / Invalidation / Cancellation / Supersession

### Repair

La definizione concettuale è corretta: stesso intent, stesso commitment, stesso strategic scope, modifica esecutiva locale. Sono mancanti il record del repair, la relazione con `plan_version`, la possibilità di più tentativi governati e la disposizione quando il tentativo fallisce senza attivare un invalidator. “Repair fails → INVALIDATED” contraddice la regola secondo cui invalidation richiede un predicato già dichiarato.

### Invalidation

È la semantica più solida del draft. Richiede invalidator pre-dichiarato, trigger evidence e post-state evidence, e vieta di usare `INVALIDATED` come alias di preferenza. Serve soltanto una regola di priorità quando completion o terminal sono simultanei.

### Cancellation

È correttamente distinta dall'impossibilità: un commitment può essere terminato volontariamente. Per non svuotare l'anti-oscillation, il record deve però identificare la versione della cancellation policy/authority, la decision boundary, la causa e l'evidenza disponibile. La cancellazione non deve essere retro-etichettata come invalidation.

### Supersession

La semantica dichiarata è corretta ma la sequenza non è eseguibile:

```text
SUPERSEDED richiede successor_decision_id
→ REVIEW_READY
→ DECISION_OPEN
→ DEFINED crea decision_B
```

Il successore deve esistere prima per chiudere A, ma non può essere creato prima secondo la macchina a stato singolo. È necessario rimuovere la dipendenza circolare preservando sia il normale feasibility gate del successore sia `REVIEW before reopen`.

## 10. Terminal Semantics

`TERMINAL_CLOSED` è correttamente assorbente rispetto alle decisioni online e consente soltanto final verification, final review materialization e telemetria post-hoc. Questo è compatibile con il terminal boundary frozen e con l'assenza di azioni online successive.

Le lacune sono:

- non tutti gli stati non terminali hanno un arco terminale;
- un commitment attivo può passare direttamente a `TERMINAL_CLOSED`, ma non è definito se la sua closure sia `TERMINAL_PREEMPTION`, completion simultanea o altra disposizione;
- non sono definiti record terminali per decisioni `DEFINED` o `PLAN_FEASIBLE` non committed;
- non esiste priorità normativa tra terminal, completion e invalidation nello stesso transition;
- la review finale può essere materializzata dopo lo stato assorbente, ma deve essere esplicitamente marcata offline/post-hoc e non presentata come nuova transizione online.

Il caso terminale in `REVIEW_READY` è rappresentabile: si entra in `TERMINAL_CLOSED` e si può completare la materializzazione finale offline. Il caso terminale durante esecuzione è invece solo nominalmente coperto e non sufficientemente tracciato.

## 11. REVIEW Semantics

La tripartizione

```text
DIRECT_ACCOUNTING
DESCRIPTIVE_DIAGNOSTICS
CAUSAL_OR_COUNTERFACTUAL_ANALYSIS
```

è corretta. Il controller online non è obbligato a produrre inferenza causale e le disposition `EXPAND / MAINTAIN / REDUCE / REMOVE / INCONCLUSIVE` sono esplicitamente output di review, non policy Foundation. Il payload aperto consente breakdown per categoria o specie.

Due elementi non sono ancora vincolanti:

1. il semplice passaggio attraverso `REVIEW_READY` non prova che una review sia stata completata; l'arco verso `DECISION_OPEN` deve richiedere un `review_id` materializzato o una closure review minimale conforme;
2. classificare un'analisi come causale non basta a impedire di presentare correlazione come causalità. Una claim causale deve registrare metodo, comparatore/counterfactual, evidence window, assunzioni e limiti; in assenza di tali campi deve restare `DESCRIPTIVE_DIAGNOSTICS`.

Le disposition devono rimanere facoltative o estendibili: il DLC può fornire l'envelope, mentre il `MODEL_SPEC` decide se e come consumarle nel ciclo successivo.

## 12. Provenance

La provenance Foundation richiesta dal DLC è corretta: `(run_id, episode_id)`, `engine_fingerprint`, `configuration_hash`, `foundation_version`, `feature_schema_version`, `telemetry_schema_version`, `agent_id` e `model_spec_version` sono presenti.

La ricostruzione end-to-end non è però ancora univoca.

| Oggetto richiesto | Copertura | Lacuna |
|---|---|---|
| run / episode / transition | Parziale | Non è definito lo scope di unicità degli ID DLC e manca un lifecycle transition/event ID. |
| decision / decision version | Presente | Mancano valid-from/created-at e relazione esplicita fra versioni. |
| plan / plan version | Presente | Manca parent plan version / supersedes plan version. |
| commitment | Presente | Il contratto dichiara “versionato” ma non contiene `commitment_version`. |
| action request | Link opzionale in VERIFY | Manca schema/identity comune e cardinalità. |
| snapshot eligibility | Assente da VERIFY | Manca `snapshot_eligibility_id`. |
| execution outcome | Link opzionale in VERIFY | Manca schema/identity e relazione 1:N con request/batch. |
| post-state evidence | Link presente | Manca source state, target state e `available_at`. |
| review | `review_id` presente | Mancano review version, created-at/completed-at e analysis-method provenance. |
| supersession chain | Relazioni nominali | La catena non è costruibile per la dipendenza circolare del successore. |

`DLC-INV-10` non è verificabile finché non viene aggiunto `commitment_version` e non vengono definite le mutazioni che incrementano decision, plan o commitment version.

## 13. DLC ↔ MODEL_SPEC Boundary

### `FOUNDATION_REQUIRED`

Devono restare nel DLC:

- stati e transizioni deliberative comuni;
- identità e versionamento di decision, plan, commitment, repair, closure e review;
- evidence timing e link alle quattro classi Foundation;
- esiti generici `FEASIBLE`/`INFEASIBLE` e classi di reason code;
- envelope di commitment, reservation e invalidator;
- semantica comune di completion, repair, invalidation, cancellation, supersession e terminal closure;
- provenance, replay contract e conformance invariants;
- priorità delle guardie concorrenti e requisiti minimi per riapertura.

### `MODEL_SPEC_REQUIRED`

Devono rimanere downstream:

- objective, utility/scoring e ranking;
- intent type/payload semantici dell'agente;
- planning method e horizon;
- resource requirements e reservation values/margins;
- risk model e criterio economico;
- completion conditions, invariants e invalidator predicates/thresholds;
- commitment duration e policy;
- repair, cancellation e supersession policy;
- action selection/prioritisation;
- crop/livestock mix, workforce, routing, market, expansion, buffer, exploration, retirement, liquidation e opponent response;
- consumo delle disposition di review e policy-update logic.

### `AMBIGUOUS_BOUNDARY`

Richiedono una definizione protocollare più neutrale:

- `strategic scope` e “material change”: il contenuto è agent-specific, ma forma, versione e confronto devono essere comuni;
- “transition rilevante” per VERIFY: la copertura minima è Foundation-required e non può essere scelta opportunisticamente dal controller;
- cause di cancellation e supersession: criteri e soglie sono agent-specific, mentre dichiarazione, versione, evidence timing e audit sono comuni;
- `EXPAND / MAINTAIN / REDUCE / REMOVE / INCONCLUSIVE`: possono essere label comuni opzionali, non un output obbligatorio né un comando esecutivo.

Il boundary generale è corretto; le ambiguità riguardano la verificabilità della separazione, non il trasferimento di una strategia agricola nella Foundation.

## 14. Conformance Invariants

| Invariant | Esito | Motivazione |
|---|---|---|
| `DLC-INV-01 No future leakage` | **PASS** | Regola esplicita e anti-retroattività coerente; servono metadati temporali per provarla in replay, ma il contratto non autorizza leakage. |
| `DLC-INV-02 Explicit commitment` | **PASS** | Ogni esecuzione committed richiede `commitment_id`. |
| `DLC-INV-03 No silent replan` | **FAIL** | Cancellation/supersession non hanno governance/versione sufficiente e possono fungere da replan arbitrario esplicito solo nominalmente. |
| `DLC-INV-04 Evidence-driven invalidation` | **PASS** | Invalidator pre-dichiarato e trigger evidence sono obbligatori. |
| `DLC-INV-05 Repair preserves commitment` | **AMBIGUOUS** | “Strategic scope” e “materiale” non sono rappresentati né confrontabili; manca il repair record. |
| `DLC-INV-06 Explicit execution evidence` | **AMBIGUOUS** | Request e outcome sono distinti, ma i link sono opzionali e `SNAPSHOT_ELIGIBILITY` manca dal record VERIFY. |
| `DLC-INV-07 Review before reopen` | **AMBIGUOUS** | È obbligatorio passare da `REVIEW_READY`, non è obbligatorio dimostrare `REVIEW complete` prima di `DECISION_OPEN`. |
| `DLC-INV-08 Terminal closure` | **AMBIGUOUS** | Lo stato è assorbente, ma la raggiungibilità terminale e la disposizione degli oggetti attivi non sono complete. |
| `DLC-INV-09 Strategy neutrality` | **PASS** | Nessuna preferenza o soglia agricola è imposta dalla conformità. |
| `DLC-INV-10 Version integrity` | **FAIL** | `commitment_version` è assente e le relazioni fra versioni non sono definite. |

Sintesi: 4 `PASS`, 2 `FAIL`, 4 `AMBIGUOUS`.

## 15. Failure-Mode Challenge

| ID | Scenario | Esito DLC | Analisi | Finding |
|---|---|---|---|---|
| `FM-01` | Piano feasible; prima request produce `NO_OP`. | **AMBIGUOUS** | VERIFY vede l'outcome, ma non esiste una regola di copertura/precedenza che scelga in modo auditabile tra continue, repair e invalidation sulla base dei predicati dichiarati. | `DLC-REV-P1-07` |
| `FM-02` | Commitment eseguibile; forte variazione di mercato. | **DETERMINISTIC** | In assenza di una condizione dichiarata attivata, il solo cambiamento di mercato non autorizza replan: il commitment resta attivo. | — |
| `FM-03` | Reservation diventa insufficiente. | **AMBIGUOUS** | Non è stabilito se reservation insufficiente sia invariant, invalidator, repair trigger o semplice forecast update; `RESERVED_SERVICEABLE` non è formalmente tipizzato come policy context nel DLC. | `DLC-REV-P1-06` |
| `FM-04` | Repair locale fallisce. | **AMBIGUOUS** | Il diagramma impone invalidation, ma questa è legale solo se scatta un invalidator dichiarato; non esistono self-loop/retry o una closure generica del repair. | `DLC-REV-P1-04` |
| `FM-05` | Terminal durante `COMMITTED_EXECUTING`. | **AMBIGUOUS** | Esiste l'arco terminale, ma non la disposizione terminale del commitment né la priorità su completion/invalidation simultanee. | `DLC-REV-P1-01`, `DLC-REV-P1-02` |
| `FM-06` | Terminal in `REVIEW_READY`. | **DETERMINISTIC** | Transizione a `TERMINAL_CLOSED`; la materializzazione finale può continuare soltanto come attività post-hoc. | — |
| `FM-07` | Nello stesso transition risultano completion e invalidation. | **AMBIGUOUS** | Nessuna precedence rule o record multi-outcome definisce il closure type canonico. | `DLC-REV-P1-02` |
| `FM-08` | Nuovo piano preferibile, nessun invalidator attivo. | **AMBIGUOUS** | La stabilità vieterebbe il replan, ma cancellation/supersession possono essere invocate senza un predicato/versione pre-dichiarati sufficienti. | `DLC-REV-P1-05` |
| `FM-09` | Commitment cancellato volontariamente. | **DETERMINISTIC** | `COMMITTED_EXECUTING → CANCELLED → REVIEW_READY`; la causa va registrata, pur restando incompleta la governance. | `DLC-REV-P1-05` |
| `FM-10` | Supersession richiede una nuova decisione non ancora esistente. | **IMPOSSIBLE** | `successor_decision_id` è richiesto prima che la sequenza autorizzi la creazione del successore. | `DLC-REV-P0-01` |

Copertura: 3 `DETERMINISTIC`, 6 `AMBIGUOUS`, 1 `IMPOSSIBLE`.

## 16. Findings Register

### `DLC-REV-P0-01` — Circular dependency in supersession

- **severity:** P0
- **section:** 6.10, 15, 17; `FM-10`
- **claim:** `SUPERSEDED` richiede `successor_decision_id`, mentre la sequenza canonica crea la decisione successiva soltanto dopo review e reopen.
- **evidence:** `commitment_A → SUPERSEDED → REVIEW_READY → DECISION_OPEN → DEFINED(decision_B)` e campo obbligatorio `successor_decision_id` all'ingresso in `SUPERSEDED`.
- **impact:** la sostituzione formale di un normale commitment è impossibile senza violare la macchina o inventare un ID/oggetto non ancora ammesso; la supersession chain non è ricostruibile.
- **required_correction:** definire una sequenza non circolare per identificare/proporre il successore, preservando feasibility/commit gate e review-before-reopen; aggiornare stato, record, invarianti e diagramma in modo coerente.

### `DLC-REV-P1-01` — Terminal reachability and active-object closure are incomplete

- **severity:** P1
- **section:** 6, 7, 10; `FM-05`
- **claim:** non tutti gli stati hanno una transizione terminale e `TERMINAL_CLOSED` non dispone esplicitamente decision, plan o commitment ancora aperti.
- **evidence:** mancano archi terminali da `INFEASIBLE`, `REJECTED`, `INVALIDATED`, `CANCELLED`, `SUPERSEDED` e `COMPLETED`; il record terminale minimo non è definito.
- **impact:** al boundary dell'episodio alcuni stati possono riaprire impropriamente o lasciare oggetti attivi/orfani nella provenance.
- **required_correction:** rendere terminal globalmente raggiungibile con priorità esplicita e introdurre un terminal-closure record che conservi stato precedente, oggetti aperti, closure type ed evidenza finale.

### `DLC-REV-P1-02` — Concurrent guard precedence is undefined

- **severity:** P1
- **section:** 6.6, 6.8, 6.11, 10; `FM-05`, `FM-07`
- **claim:** completion, invalidation e terminal possono risultare veri sulla stessa evidenza, ma il DLC non assegna una precedenza né consente un outcome primario con evidenze secondarie.
- **evidence:** gli archi sono paralleli e privi di priority/decision table.
- **impact:** due implementazioni conformi possono produrre closure type, review e supersession history differenti sullo stesso trace.
- **required_correction:** definire una precedence table policy-neutral e conservare tutti i predicate result anche quando un solo closure type guida la transizione.

### `DLC-REV-P1-03` — `INFEASIBLE` and `REJECTED` overlap

- **severity:** P1
- **section:** 6.4, 6.5
- **claim:** `INFEASIBLE` rappresenta il fallimento del feasibility gate, ma `REJECTED` ammette `FEASIBILITY_REJECTION` dalla stessa fase.
- **evidence:** entrambe sono uscite da `DEFINED`; non esiste una guardia che scelga l'una o l'altra.
- **impact:** reason code, conteggi di failure e replay del pre-commit non sono comparabili.
- **required_correction:** rendere disgiunte entry conditions e cause, oppure fondere gli stati mantenendo un unico esito con reason code distinto.

### `DLC-REV-P1-04` — Repair failure and repair identity are underspecified

- **severity:** P1
- **section:** 6.7, 7, 14; `FM-04`
- **claim:** il repair non ha record/versione minima e il diagramma trasforma ogni fallimento in invalidation anche senza invalidator dichiarato.
- **evidence:** l'unico arco diagrammato per `repair fails` è `INVALIDATED`; la definizione di invalidation richiede invece un predicate pre-dichiarato.
- **impact:** repair legittimi non sono replayable e un semplice tentativo fallito può falsificare la causa di chiusura.
- **required_correction:** definire `repair_id`, evidence, plan version relation, attempt/result e uscite per retry/continue, invalidation solo su trigger valido, cancellation e terminal; formalizzare il confronto di intent/scope.

### `DLC-REV-P1-05` — Cancellation and supersession can bypass anti-oscillation

- **severity:** P1
- **section:** 6.6, 6.9, 6.10, 15, 18, 20; `FM-08`, `FM-09`
- **claim:** un reason code esplicito è sufficiente a cancellare/supersedere, ma policy/authority/versione/evidence timing non sono richiesti.
- **evidence:** `cancellation_policy` non compare fra le dichiarazioni minime del `MODEL_SPEC`; supersession e cancellation non hanno un vincolo anti-retroattivo equivalente agli invalidator.
- **impact:** `NO_REPLAN_WITHOUT_LIFECYCLE_CAUSE` può ridursi a un cambio arbitrario rinominato come cancel/supersede.
- **required_correction:** richiedere policy/authority versionata, decision boundary, reason/evidence e distinzione dall'invalidation, senza imporre criteri o soglie comuni.

### `DLC-REV-P1-06` — Feasibility is not aligned with Foundation execution classes

- **severity:** P1
- **section:** 6.3, 10, 12; `FM-03`
- **claim:** il feasibility record non distingue snapshot eligibility, atomic batch feasibility, serialization feasibility e reserved future serviceability.
- **evidence:** non esistono batch/order/freshness fields e `RESERVED_SERVICEABLE_BEFORE_DEADLINE` non è esplicitamente qualificato come previsione `POLICY_CONTEXT`.
- **impact:** un `FEASIBLE` può essere interpretato come engine fact o restare valido dopo che lo snapshot di supporto è divenuto stale.
- **required_correction:** registrare le classi di check, snapshot/batch/order/versione e freshness/revalidation; ribadire che reservation/serviceability futura non è una garanzia engine.

### `DLC-REV-P1-07` — VERIFY does not provide a complete execution-evidence ledger

- **severity:** P1
- **section:** 5, 9; `FM-01`
- **claim:** VERIFY omette `snapshot_eligibility_id`, rende request/outcome opzionali senza regola e limita il logging a transition “rilevanti” non definite.
- **evidence:** il record minimo elenca `action_request_id?`, `execution_outcome_id?`, `post_state_evidence_id`, ma non l'eligibility record.
- **impact:** no-op, batch rejection e azioni serializzate possono essere omessi o ricostruiti in modo non uniforme; `DLC-INV-06` non è testabile.
- **required_correction:** definire copertura minima e cardinalità condizionali per tutte e quattro le classi, inclusi no-request e no-op, con guard evaluation e precedence result.

### `DLC-REV-P1-08` — Evidence snapshots lack enforceable decision-boundary timing

- **severity:** P1
- **section:** 4, 5, 6.2, 6.3, 13
- **claim:** la regola no-leakage è corretta, ma gli snapshot non identificano capture time, availability boundary, source/target state o immutabilità.
- **evidence:** `evidence_snapshot_id` è usato senza schema temporale; la formula generale include simultaneamente `S_t` e `S_t+1` per ogni transizione deliberativa.
- **impact:** un replay non può provare che DEFINE/PLAN/COMMIT non abbiano consumato evidenza posteriore.
- **required_correction:** introdurre campi `captured_at`, `available_at`, state/transition references e regola append-only/versioned; specificare le evidence classes consentite per ogni transizione deliberativa.

### `DLC-REV-P1-09` — Provenance and version integrity are insufficient

- **severity:** P1
- **section:** 9, 11, 17, 18
- **claim:** mancano `commitment_version`, lifecycle event identity e relazioni/versioni sufficienti per action, evidence, repair e review.
- **evidence:** Section 11 dichiara il commitment versionato, ma Section 17 elenca solo `commitment_id`; non definisce identity/cardinality delle quattro evidenze.
- **impact:** mutazioni materiali e catene decisionali non sono ricostruibili senza ambiguità; `DLC-INV-10` fallisce.
- **required_correction:** completare ID, scope di unicità, version lineage, timestamps/transition IDs e foreign-key cardinalities per tutti gli oggetti DLC.

### `DLC-REV-P1-10` — REVIEW completion and causal-claim governance are not enforceable

- **severity:** P1
- **section:** 6.12, 16, 18
- **claim:** passare da `REVIEW_READY` non prova review completion e la sola etichetta causale non impedisce causalità non supportata.
- **evidence:** il testo ammette direttamente `REVIEW_READY → DECISION_OPEN`; soltanto il diagramma scrive `REVIEW complete`. Il review record non richiede method/comparator/assumptions per causal claims.
- **impact:** reopen senza audit e correlazioni presentate come causalità possono risultare formalmente conformi.
- **required_correction:** rendere `review_id` materializzato guardia della riapertura e definire metadata minimi per causal/counterfactual analysis, con fallback obbligatorio a descriptive diagnostics.

### `DLC-REV-P2-01` — Mermaid diagram is not semantically complete

- **severity:** P2
- **section:** 7
- **claim:** il diagramma è sintatticamente renderizzabile ma non contiene tutte le uscite testuali.
- **evidence:** omette `REPAIR_WITHIN_COMMITMENT → CANCELLED` e `REPAIR_WITHIN_COMMITMENT → TERMINAL_CLOSED`, oltre alle terminal transitions mancanti negli stati intermedi.
- **impact:** lettori e implementazioni diagram-driven possono produrre una macchina diversa dal testo.
- **required_correction:** aggiornare il Mermaid dopo la correzione della transition table e verificarne la parità semantica.

### `DLC-REV-P2-02` — REACT allowed effects omit canonical closure paths

- **severity:** P2
- **section:** 8
- **claim:** l'elenco `retain / repair / invalidate / complete / close` non chiarisce cancellation e supersession.
- **evidence:** entrambe sono uscite canoniche da `COMMITTED_EXECUTING` ma non compaiono nell'effect contract di REACT.
- **impact:** non è chiaro se un evento possa soltanto aggiornare evidenza o anche abilitare una scelta esplicita di cancel/supersede.
- **required_correction:** dichiarare esplicitamente l'interazione fra event intake e comando deliberativo di cancellation/supersession, senza introdurre soglie comuni.

## 17. Required Corrections

Prima del freeze sono necessarie, nell'ordine:

1. eliminare la dipendenza circolare di supersession (`DLC-REV-P0-01`);
2. rendere terminal closure globalmente raggiungibile e definire la disposizione degli oggetti aperti (`P1-01`);
3. stabilire precedence policy-neutral fra terminal, completion e invalidation (`P1-02`);
4. separare normativamente `INFEASIBLE` e `REJECTED` (`P1-03`);
5. introdurre un repair record e uscite coerenti con invalidation evidence-driven (`P1-04`);
6. vincolare cancellation/supersession a policy/authority/versione/evidenza senza prescriverne i criteri (`P1-05`);
7. allineare feasibility a snapshot, batch, serializzazione, capacità multidimensionale e serviceability tripartita (`P1-06`);
8. completare il ledger VERIFY sulle quattro classi Foundation e su tutte le transizioni coperte (`P1-07`);
9. rendere evidence timing provabile mediante decision-boundary metadata (`P1-08`);
10. completare provenance e version lineage, incluso `commitment_version` (`P1-09`);
11. imporre REVIEW completion prima di reopen e provenance delle claim causali (`P1-10`);
12. riallineare Mermaid e REACT wording alla macchina corretta (`P2-01`, `P2-02`).

Queste correzioni riguardano esclusivamente il DLC. Non richiedono modifiche retroattive alla Foundation frozen e non autorizzano la progettazione di un `MODEL_SPEC`.

## 18. Final Gate

```text
FOUNDATION_ALIGNMENT: CORRECTIONS_REQUIRED
DLC_STATE_COMPLETENESS: CORRECTIONS_REQUIRED
DLC_TRANSITION_COMPLETENESS: FAIL_WITH_BLOCKERS
REACT_SEMANTICS: PASS_WITH_P2
VERIFY_SEMANTICS: CORRECTIONS_REQUIRED
COMMITMENT_ANTI_OSCILLATION: CORRECTIONS_REQUIRED
FEASIBILITY_BOUNDARY: CORRECTIONS_REQUIRED
EVIDENCE_TIMING_ALIGNMENT: CORRECTIONS_REQUIRED
NO_FUTURE_LEAKAGE: PASS
REPAIR_VS_REPLAN: CORRECTIONS_REQUIRED
INVALIDATION_SEMANTICS: CORRECTIONS_REQUIRED
CANCELLATION_SEMANTICS: CORRECTIONS_REQUIRED
SUPERSESSION_SEMANTICS: FAIL_WITH_BLOCKERS
TERMINAL_SEMANTICS: CORRECTIONS_REQUIRED
REVIEW_SEMANTICS: CORRECTIONS_REQUIRED
PROVENANCE_SUFFICIENCY: CORRECTIONS_REQUIRED
MODEL_SPEC_BOUNDARY: CORRECTIONS_REQUIRED
STRATEGY_NEUTRALITY: PASS
CONFORMANCE_INVARIANTS: CORRECTIONS_REQUIRED
FAILURE_MODE_COVERAGE: FAIL_WITH_BLOCKERS
MERMAID_RENDERABILITY: PASS

P0_OPEN: 1
P1_OPEN: 10
P2_OPEN: 2

DECISION_LIFECYCLE_REVIEW: FAIL_WITH_BLOCKERS
DECISION_LIFECYCLE_FREEZE_RECOMMENDED: NO
```

La review termina qui. Nessuna correzione è stata applicata al Decision Lifecycle Contract o agli artefatti upstream/downstream.
