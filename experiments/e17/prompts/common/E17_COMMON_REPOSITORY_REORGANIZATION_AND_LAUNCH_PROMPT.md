# Prompt comune — Riordino repository e avvio sequenziale di E17

## Mandato

Agisci come uno dei tre agenti del progetto Kaggriculture:

```text
AGENT_ID: antigravity | codex | copilot
REPOSITORY_ROOT: C:\Users\pietr\Projects\kaggriculture-agent
LANGUAGE: italiano
```

Il lavoro ha due fronti rigorosamente sequenziali:

```text
FRONTE_A: RIORDINO_COMPLETO_DEL_REPOSITORY
          ↓ solo dopo gate PASS e riconciliazione
FRONTE_B: AVVIO_E17_LIMITATO_A_E17.0
```

È vietato iniziare E17, modificare policy o generare nuove candidate mentre il
riordino non è formalmente chiuso.

## Documenti obbligatori

Leggi integralmente prima di agire:

1. `README.md`;
2. `docs/NEW_SESSION.md`;
3. `docs/PROJECT_STATE.md`;
4. `docs/repository/REPOSITORY_ARCHITECTURE.md`;
5. `experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md`;
6. `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`;
7. `experiments/e17/reviews/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md`;
8. `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`;
9. il MODEL_SPEC corrente del proprio agente.

Esegui inoltre `git status`, inventario dei file e verifica degli hash prima
di qualsiasi move. Le modifiche già presenti appartengono al proprietario e
devono essere preservate.

## Principi comuni

1. Il repository viene organizzato verticalmente per esperimento.
2. `docs/` conserva soltanto documentazione stabile e cross-round.
3. `experiments/<round>/` contiene l'intero ciclo del round.
4. `data/` contiene input esterni, non documentazione.
5. `src/` contiene codice runtime mantenuto.
6. `submission/` contiene la sola submission canonica richiesta.
7. Git mantiene la cronologia: `docs/versions/` non è una categoria futura.
8. Nessun file viene cancellato senza classificazione, hash e destinazione.
9. Riordino strutturale e modifica semantica non possono stare nello stesso
   passaggio.
10. Nessun agente può importare o copiare routine, planner, dispatcher,
    schedule o action table di un altro.

# FRONTE A — Riordino del repository

## A0 — Preflight e inventario indipendente

Ogni agente deve produrre senza spostare file:

```text
docs/repository/migration/MIGRATION_INVENTORY_<AGENT_ID>.csv
docs/repository/migration/MIGRATION_REVIEW_<AGENT_ID>.md
```

Il CSV deve contenere almeno:

```text
source_path
sha256
tracked_status
artifact_role
experiment_id
ownership: common | antigravity | codex | copilot
epistemic_role: normative | design | prompt | input | raw | derived | report | freeze | transient
proposed_destination
action: move | keep | archive | candidate_delete
references_found
notes
```

Regole:

- `candidate_delete` è solo una proposta; non autorizza la cancellazione;
- file byte-identici vanno segnalati, non rimossi automaticamente;
- directory vuote e cache possono essere segnalate separatamente;
- ogni riferimento Markdown/Python/config alla source deve essere inventariato;
- ogni agente è responsabile in particolare dei propri artefatti, ma deve
  segnalare anche problemi nei percorsi comuni.

## A1 — Reconciliation e manifest di migrazione

`codex` opera come integration owner del riordino comune. Dopo la disponibilità
dei tre inventari deve produrre:

```text
docs/repository/migration/REPOSITORY_MIGRATION_PLAN_FROZEN.md
docs/repository/migration/REPOSITORY_MIGRATION_MANIFEST.csv
```

Il manifest riconciliato deve avere una sola destinazione per source, nessuna
collisione e un owner esecutivo per ciascun move.

Se i tre inventari non sono disponibili, non inventare il loro contenuto e
non dichiarare reconciliation completa. È ammesso avanzare soltanto sui path
non controversi di propria proprietà.

## A2 — Albero target

Applicare l'architettura approvata:

```text
docs/
  NEW_SESSION.md
  PROJECT_STATE.md
  EXPERIMENT_LOG.md
  foundation/
  model_specs/{antigravity,codex,copilot}/
  governance/
  repository/

experiments/
  README.md
  e17/
    README.md
    manifest/
    design/
    prompts/{common,antigravity,codex,copilot}/
    configs/
    tools/
    tests/
    reviews/{common,antigravity,codex,copilot}/
    reports/{common,antigravity,codex,copilot}/
    artifacts/{discovery,runs,derived,freeze}/
  archive/e01/ ... archive/e16/

data/
  replays/{reference,e17-discovery}/
  screenshots/

src/agricola/{core,strategy/antigravity,strategy/codex,strategy/copilot}/
scripts/
tests/
submission/submission_codex.py
```

## A3 — Ownership dei move

### Codex

- crea lo skeleton comune;
- migra entry point, governance comune, Foundation e materiale non
  attribuibile a un singolo agente;
- migra replay/cataloghi in `data/`;
- migra il materiale E17 comune;
- riconcilia manifest, link e indici;
- non modifica semanticamente i documenti agent-local.

### Antigravity

- migra MODEL_SPEC, prompt, review, report, config, freeze e tooling di propria
  proprietà;
- classifica e archivia il materiale storico Antigravity;
- non modifica file strategici Codex o Copilot.

### Copilot

- migra MODEL_SPEC, prompt, review, report, config, freeze e tooling di propria
  proprietà;
- classifica e archivia il materiale storico Copilot;
- non modifica file strategici Codex o Antigravity.

### Path condivisi

Per un file con ownership `common`, un solo agente esegue il move secondo il
manifest. Gli altri effettuano review read-only. Non eseguire move concorrenti
sullo stesso path.

## A4 — Regole di migrazione

- preferire move tracciabili che preservino i contenuti;
- verificare ogni destinazione prima di move ricorsivi;
- aggiornare riferimenti solo dopo il move corrispondente;
- non cambiare contemporaneamente testo, codice o config, salvo la correzione
  strettamente necessaria dei path;
- conservare SHA-256 degli artefatti immutabili;
- i replay mantengono EpisodeId e hash;
- i risultati storici E01–E16 vanno archiviati per round, non eliminati;
- `docs/prompts/` e `docs/versions/` si rimuovono soltanto quando vuoti e dopo
  verifica del manifest;
- `results/` si rimuove soltanto quando ogni file è migrato e referenziato;
- `scripts/` mantiene solo strumenti cross-round; gli strumenti E17 vanno in
  `experiments/e17/tools/`;
- non alterare `submission/submission_codex.py` durante il riordino.

## A5 — README e indici obbligatori

Creare o aggiornare:

```text
experiments/README.md
experiments/e17/README.md
data/replays/MANIFEST.md
docs/repository/README.md
docs/NEW_SESSION.md
docs/PROJECT_STATE.md
README.md
```

`experiments/e17/README.md` è l'unico START_HERE del round e deve indicare:

- fase e stato;
- protocollo comune;
- responsabilità dei tre agenti;
- baseline/hash;
- design corrente;
- seed e opponent;
- report/review;
- gate e prossimo passo.

## A6 — Verifica indipendente

Dopo i move, ogni agente produce:

```text
docs/repository/migration/POST_MIGRATION_REVIEW_<AGENT_ID>.md
```

Controllare almeno:

```text
NO_LOST_TRACKED_FILES
SOURCE_DESTINATION_COVERAGE
SHA256_PRESERVATION
MARKDOWN_LINKS
PYTHON_IMPORTS
TEST_SUITE
CONFIG_PATHS
REPLAY_MANIFEST
SUBMISSION_HASH
GIT_STATUS
AGENT_OWNERSHIP
```

Ogni rilievo deve essere classificato `BLOCKER`, `MAJOR`, `MINOR` o
`ACCEPTED_DEBT`.

## A7 — Gate di chiusura riordino

Codex riconcilia le tre review in:

```text
docs/repository/migration/POST_MIGRATION_RECONCILIATION.md
```

E17 può iniziare soltanto con:

```text
REPOSITORY_TREE_MATCHES_ARCHITECTURE: PASS
NO_LOST_TRACKED_FILES: PASS
MIGRATION_MANIFEST_COVERAGE: 100%
IMMUTABLE_HASHES_PRESERVED: PASS
MARKDOWN_LINK_CHECK: PASS
PYTHON_IMPORT_CHECK: PASS
TEST_SUITE: PASS
SUBMISSION_CODEX_SHA256: AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421
UNRESOLVED_BLOCKERS: 0
POST_MIGRATION_REVIEWS: 3/3
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
```

Se un gate fallisce, fermarsi sul Fronte A. Non compensare un errore di
migrazione con modifiche E17.

Commit e push non sono autorizzati da questo documento: richiedono istruzione
esplicita del proprietario dopo la review del diff.

# BARRIERA A→B

Prima del Fronte B devono esistere il manifest e la reconciliation con tutti i
gate `PASS`. Aggiornare `PROJECT_STATE` e `NEW_SESSION` a:

```text
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
E17_PHASE: DEFINE / E17.0
E17_POLICY_MUTATION: NOT_STARTED
```

Solo allora procedere.

# FRONTE B — Avvio di E17

## B0 — Principio comune

E17 è la guida comune per i modelli 3Q di Antigravity, Codex e Copilot. Non
preseleziona un archetipo vincente. `tetsuya`, `OceanMix` e `Crop Dusta` sono
combinazioni osservate di fattori, non routine da copiare.

Le dimensioni devono essere valutate causalmente:

- timing Q2 D11/D10/D8;
- topologia livestock distribuita/compatta/mista;
- diversificazione crop 3/4/5 specie;
- diversificazione animale 2/3 specie;
- reinvestimento aggressivo/riserva liquida;
- densità, servicing e chiusura terminale.

Prima si misurano effetti principali; poi interazioni preregistrate; solo alla
fine è ammessa una candidata composita.

## B1 — Review indipendente della strategia

Ogni agente legge il draft migrato e produce:

```text
experiments/e17/reviews/<agent>/E17_STRATEGY_REVIEW.md
```

La review deve esprimere:

- `ACCEPT`, `ACCEPT_WITH_CHANGES` o `REJECT`;
- completezza del ledger;
- validità di seed, holdout, opponent e gate;
- rischio di confondimento fra fattori;
- indipendenza strategica;
- correzioni indispensabili prima del freeze.

Codex riconcilia soltanto dopo 3/3 review in:

```text
experiments/e17/reviews/common/E17_STRATEGY_RECONCILIATION.md
experiments/e17/design/E17_STRATEGY_FROZEN_V1.md
experiments/e17/manifest/E17_COMMON_MANIFEST_V1.json
```

Se manca una review, il draft non diventa frozen.

## B2 — E17.0 comune: measurement parity

E17.0 implementa osservabilità prima di qualsiasi ottimizzazione.

Ledger minimo per ogni comando:

```text
episode_id, seed, seat, player_id
step, day, hour, unit_id
requested_command, requested_parameters
pre_state_fingerprint, post_state_fingerprint
cash_before, cash_after
inventory_before, inventory_after
tile_or_asset_before, tile_or_asset_after
outcome: EXECUTED | NOT_EXECUTED | UNKNOWN
outcome_evidence
quadrant_slot
policy_version, source_hash, config_hash, routine_hash
```

La telemetria non deve entrare nel percorso decisionale durante E17.0.

## B3 — Responsabilità E17.0

### Codex

- mantiene V9 byte/behavioralmente congelata;
- implementa ledger esterno al decision path;
- dimostra parità 719/719, stesso action hash e stesso outcome per
  seed/seat/opponent;
- non introduce ancora la guardia WHEAT.

### Antigravity

- elimina la dipendenza da `codex_v9_routine_data`;
- costruisce una baseline 3Q nativa e documenta la provenance;
- implementa lo stesso schema ledger senza copiare policy altrui;
- non può dichiarare confronto indipendente finché il gate non passa.

### Copilot

- elimina import e copia della routine Codex;
- costruisce una baseline 3Q nativa e documenta la provenance;
- implementa lo stesso schema ledger senza copiare policy altrui;
- non può dichiarare confronto indipendente finché il gate non passa.

## B4 — Seed e livelli di benchmark

Usare esclusivamente seed e protocollo congelati dal documento E17 frozen:

- development già osservato;
- holdout non eseguito prima del freeze;
- final confirmation una sola volta;
- entrambi i seat;
- livelli contract, passive, mirror, independent tournament, Kaggle.

I replay Top 3 sono dati offline di discovery e non possono essere feature
online o validation indipendente.

## B5 — Gate E17.0

```text
ACTION_PARITY: PASS per baseline che richiedono parità
LEDGER_RECORD_COVERAGE: 100%
MARKET_OUTCOME_COVERAGE: dichiarata senza convertire UNKNOWN
TECHNICAL_ERRORS: 0
FALLBACK_DELTA: 0
ANIMAL_ESCAPE_LEDGER: AUDITABLE
SOURCE_CONFIG_FREEZE: PASS
STRATEGIC_INDEPENDENCE_GATE: PASS prima del torneo a tre
```

Ogni agente produce:

```text
experiments/e17/reports/<agent>/E17_0_IMPLEMENTATION_AND_PARITY_REPORT.md
experiments/e17/artifacts/derived/<agent>/E17_0_METRICS.json
experiments/e17/artifacts/freeze/<agent>/
```

## B6 — Stop obbligatorio

Questo prompt non autorizza E17.1 o fasi successive.

Al completamento di E17.0:

1. raccogliere le tre review e i tre report;
2. produrre un riepilogo di gate e blocker;
3. aggiornare `PROJECT_STATE` e `NEW_SESSION`;
4. fermarsi in attesa della riconciliazione E17.0 e dell'autorizzazione del
   proprietario.

Non eseguire:

- guardia fill-aware WHEAT;
- timing D10/D8;
- nuova topologia;
- diversificazione;
- torneo a tre se un gate d'indipendenza fallisce;
- submission Kaggle;
- commit o push non esplicitamente autorizzati.

# Formato della risposta finale di ciascun agente

```text
AGENT_ID:
FRONTE_A_STATUS:
FILES_INVENTORIED:
FILES_MOVED:
FILES_ARCHIVED:
FILES_DELETED:
MIGRATION_GATE:
POST_MIGRATION_BLOCKERS:

FRONTE_B_STARTED: YES | NO
E17_STRATEGY_REVIEW:
E17_0_IMPLEMENTATION_STATUS:
LEDGER_COVERAGE:
ACTION_PARITY:
STRATEGIC_INDEPENDENCE_GATE:
E17_0_BLOCKERS:

POLICY_MUTATION_BEYOND_E17_0: NO
KAGGLE_SUBMISSION: NO
COMMIT: NO unless separately authorized
PUSH: NO unless separately authorized
NEXT_RECOMMENDED_ACTION:
```
