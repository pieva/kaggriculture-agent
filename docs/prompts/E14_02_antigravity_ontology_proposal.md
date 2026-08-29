# E14.2 --- Cross-Model Ontology Proposal

## Ruolo

Sei **Antigravity**. Devi contribuire alla costruzione di un'ontologia
comune dei meccanismi economici e operativi di Kaggriculture,
confrontando in modo indipendente i tre modelli Antigravity, Codex e
Copilot.

## Obiettivo

Costruire una proposta di **vocabolario ontologico comune** che permetta
ai tre MODEL_SPEC di usare gli stessi nomi canonici (`concept_id`)
quando descrivono lo stesso fenomeno, senza uniformare valutazioni,
ranking, confidence, causalità o policy.

L'ontologia deve standardizzare **che cosa stiamo osservando**, non
**quanto è importante** né **come debba essere sfruttato**.

Dopo questa fase ChatGPT consoliderà le tre proposte in una bozza unica;
la bozza sarà successivamente verificata dai tre agenti prima
dell'adozione.

## Vincoli di sicurezza

Prima di lavorare esegui: - `git status --short` -
`git branch --show-current` - `git log -1 --oneline`

Non eseguire `git reset`, `git clean`, `git stash`, `git revert`. Non
fare commit o push. Non caricare submission su Kaggle. Non modificare
strategie, submission, builder, test o risultati preesistenti. Non
modificare nessuno dei tre `MODEL_SPEC.md`.

## Fonti da esaminare

Leggi: - `docs/model_specs/antigravity/MODEL_SPEC.md` -
`docs/model_specs/codex/MODEL_SPEC.md` -
`docs/model_specs/copilot/MODEL_SPEC.md`

Puoi usare come verifica le evidenze empiriche accumulate nel
repository: benchmark, JSON/replay, ledger, risultati E13 e precedenti,
test report e altri artefatti fattuali pertinenti.

Non trattare un MODEL_SPEC come evidenza empirica: è una
rappresentazione/ipotesi del modello.

## Principio fondamentale

Preferisci nomi canonici **neutrali e descrittivi del fenomeno**, non
nomi che incorporano già una policy o una soluzione.

Esempio concettuale: - preferire `feed_market_dependency` a un nome che
prescriva già l'autarchia alimentare; - distinguere proprietà del
terreno, terreno attivato, superficie mantenuta e superficie monetizzata
se i dati indicano fenomeni diversi.

Non forzare equivalenze. Due termini possono essere: - equivalenti; -
parzialmente sovrapposti; - uno più generale dell'altro; - distinti; -
in conflitto semantico.

## Tassonomia aperta

Non sei vincolato ai parametri esistenti. Puoi proporre: - nuovi
concetti; - decomposizioni; - fusioni; - gerarchie padre/figlio; -
relazioni tra concetti; - deprecazioni terminologiche.

L'ontologia deve distinguere almeno, quando appropriato: `STATE`,
`FLOW`, `CAPACITY`, `COST`, `REVENUE`, `EFFICIENCY`, `CONSTRAINT`,
`TIMING`, `INTERACTION`, `DERIVED_METRIC`, `OUTCOME`.

Le **POLICY** non appartengono all'ontologia: restano nei singoli
modelli.

## Mapping obbligatorio

Per ogni fattore significativo presente in almeno uno dei tre MODEL_SPEC
proponi: - `concept_id` canonico; - tipo ontologico; - definizione
neutrale; - termine Antigravity corrispondente; - termine Codex
corrispondente; - termine Copilot corrispondente; - mapping per ciascun
modello: `FULL`, `PARTIAL`, `ABSENT`, `BROADER`, `NARROWER`,
`CONFLICT`; - evidenze empiriche pertinenti e loro path; - ambiguità
ancora aperte.

Non usare il consenso fra modelli come prova.

## Relazioni

Proponi separatamente relazioni ontologiche motivate, per esempio:
`enables`, `constrains`, `converts_to`, `consumes`, `produces`,
`measures`, `interacts_with`.

Distingui esplicitamente: - direct effect; - enabling effect; -
constraining effect; - interaction effect.

Non trasformare una correlazione osservata in causalità certa.

## Indipendenza delle valutazioni

L'obiettivo futuro è che i tre modelli possano usare lo stesso
`concept_id` ma attribuirgli importanza diversa. Non mediare ranking,
impact o confidence.

Se un concetto è valido per l'ontologia ma un modello non lo usa, deve
essere possibile rappresentarlo come `ABSENT` / futuro `NOT_USED`.

## Output

Crea **un solo file**:
`results/e14/ontology_proposals/antigravity_ontology_proposal.md`

Il documento deve contenere: 1. Executive summary. 2. Principi di
normalizzazione adottati. 3. Tabella completa dei concept_id proposti e
mapping dei tre modelli. 4. Relazioni ontologiche proposte. 5.
Equivalenze forti. 6. Sovrapposizioni parziali e conflitti di
granularità. 7. Concetti presenti in un solo modello. 8. Concetti
mancanti emersi dalle evidenze. 9. Termini/policy che non devono entrare
nell'ontologia. 10. Questioni che ChatGPT dovrà risolvere nella sintesi.

Non modificare i MODEL_SPEC e non proporre ancora una nuova strategia
operativa.

Al termine esegui `git status --short` e conferma che l'unico nuovo
output intenzionale di questa attività sia il file sopra indicato, senza
alterare il dirty state preesistente.
