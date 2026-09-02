# Proposta di architettura del repository

- **Stato:** proposta, nessuna migrazione ancora eseguita
- **Data:** 2026-09-02
- **Obiettivo:** rendere immediatamente distinguibili artefatti canonici,
  esperimenti attivi, output generati e materiale storico

## 1. Diagnosi dell'albero corrente

La struttura attuale organizza prevalentemente per tipo di artefatto:

```text
docs/experiment_designs/e17/
docs/prompts/
docs/versions/
configs/
scripts/e17/
results/e17/
```

Questo obbliga a ricostruire un esperimento attraversando cinque o sei rami.
Inoltre:

- `docs/versions/` contiene 77 file eterogenei e replica la cronologia già
  mantenuta da Git;
- `docs/prompts/` contiene prompt di molti round, documenti operativi e perfino
  asset non-prompt;
- `results/` mescola run grezzi, report durevoli, review della Foundation e
  freeze di submission;
- `results/model_spec_c2/` contiene sia evidenza generata sia documentazione
  normativa o di governance;
- i replay JSON sono sotto `docs/benchmark/`, pur essendo dati di input;
- gli script storici sono prevalentemente piatti, mentre solo E17 ha iniziato
  una separazione per round e agente.

## 2. Principio architetturale

Adottare una struttura **verticale per esperimento**:

> Tutto ciò che esiste soltanto perché esiste E17 deve stare sotto
> `experiments/e17/`.

Restano top-level soltanto gli elementi trasversali e stabili:

- Foundation e documentazione globale;
- codice runtime riutilizzabile;
- test comuni;
- dati esterni condivisi;
- submission canonica corrente.

## 3. Albero obiettivo

```text
kaggriculture-agent/
├── README.md
├── pyproject.toml
│
├── docs/                         # solo documentazione stabile e trasversale
│   ├── NEW_SESSION.md            # entry point operativo
│   ├── PROJECT_STATE.md          # stato canonico
│   ├── EXPERIMENT_LOG.md         # indice cronologico sintetico
│   ├── foundation/               # contract, ontology, state machine, features
│   ├── model_specs/
│   │   ├── antigravity/
│   │   ├── codex/
│   │   └── copilot/
│   ├── governance/               # review/reconciliation cross-experiment
│   └── repository/               # convenzioni e migration manifest
│
├── experiments/                  # vertical slice per round
│   ├── README.md                 # indice esperimenti e stato
│   ├── e17/
│   │   ├── README.md             # unico START_HERE del round
│   │   ├── manifest/             # freeze, hash, seed, opponent, provenance
│   │   ├── design/               # strategia e preregistrazioni
│   │   ├── prompts/              # prompt comuni o per agente
│   │   │   ├── common/
│   │   │   ├── antigravity/
│   │   │   ├── codex/
│   │   │   └── copilot/
│   │   ├── configs/              # config specifiche del round
│   │   ├── tools/                # runner/estrattori specifici del round
│   │   ├── reviews/              # feedback e reconciliation E17
│   │   ├── reports/              # report umani finali/intermedi promossi
│   │   │   ├── common/
│   │   │   ├── antigravity/
│   │   │   ├── codex/
│   │   │   └── copilot/
│   │   ├── artifacts/            # output macchina
│   │   │   ├── discovery/
│   │   │   ├── runs/
│   │   │   ├── derived/
│   │   │   └── freeze/
│   │   └── tests/                # test specifici E17
│   └── archive/                  # round chiusi E01–E16
│       ├── e01/
│       └── ...
│
├── data/                         # input esterni, mai documentazione
│   ├── replays/
│   │   ├── reference/
│   │   └── e17-discovery/
│   └── screenshots/
│
├── src/agricola/                 # runtime e policy mantenute
│   ├── core/
│   └── strategy/
│       ├── antigravity/
│       ├── codex/
│       └── copilot/
│
├── scripts/                      # soltanto tooling riutilizzabile cross-round
├── tests/                        # test runtime e integrazione trasversali
└── submission/
    └── submission_codex.py       # sola submission canonica richiesta
```

## 4. Regole di classificazione

### `docs/`

Un file appartiene a `docs/` solo se resta valido oltre il singolo round:

- stato progetto;
- Foundation;
- MODEL_SPEC attivi;
- governance condivisa;
- convenzioni del repository.

Un prompt E17, un report E17 o una config E17 non appartengono a `docs/`.

### `experiments/<round>/`

È l'unità primaria di lavoro. Deve contenere tutto il ciclo:

```text
DEFINE -> FREEZE -> IMPLEMENT -> RUN -> ANALYZE -> REVIEW -> DECIDE
```

Il `README.md` del round indica sempre:

- stato e fase;
- baseline e hash;
- documento di design corrente;
- run promossi;
- decisione e prossimo passo;
- link ai tre agenti.

### `artifacts/`

Contiene output macchina, non documentazione normativa:

- JSON/CSV di telemetria;
- replay derivati;
- log e run directories;
- freeze standalone;
- hash manifest.

Un report Markdown entra in `reports/` solo se è stato promosso come evidenza
umana leggibile. I dump Markdown generati automaticamente restano artifacts.

### `data/`

Contiene input esterni immutabili. Ogni dataset ha un manifest con origine,
data, hash, ruolo epistemico (`DISCOVERY`, `TRAINING`, `HOLDOUT`, `TEST`) e
divieto di utilizzo online.

### `scripts/`

Mantiene soltanto tooling usabile da più round. Un estrattore o runner scritto
solo per E17 deve stare in `experiments/e17/tools/`.

### `docs/versions/`

Va eliminata come categoria attiva. Git è la cronologia. I documenti storici
utili vanno collocati nel round che li ha prodotti; bozze e transitori senza
valore di provenance possono essere rimossi dopo verifica.

## 5. Separazione common / agent-local

Ogni round deve rendere evidente la proprietà:

```text
common/       schema, benchmark, Foundation, seed, gate condivisi
antigravity/  design, prompt, report e freeze proprietari
codex/        design, prompt, report e freeze proprietari
copilot/      design, prompt, report e freeze proprietari
```

La collocazione comune non autorizza il riuso di routine. Il manifest deve
dichiarare separatamente:

```text
SHARED_PROTOCOL_HASH
AGENT_POLICY_HASH
AGENT_CONFIG_HASH
AGENT_FREEZE_HASH
STRATEGIC_INDEPENDENCE_GATE
```

## 6. Politica di versionamento

Evitare nomi come `final_final_v3_revised`. Usare:

```text
Documento mutable in DEFINE:
E17_STRATEGY_DRAFT.md

Freeze immutabile:
E17_STRATEGY_FROZEN_V1.md

Run:
run-20260902T221530Z-seed207899150-seat0

Candidata:
CODEX_E17_RQ1_WHEAT_FILL_GUARD_V1
```

Una volta congelato, un file non viene sovrascritto: una revisione produce V2.
La storia minuta resta in Git, non nel nome del file.

## 7. Politica di retention

### Conservare in Git

- manifest e hash;
- design/preregistrazione congelati;
- codice e config delle candidate valutate;
- report finali e tabelle sintetiche;
- freeze standalone promosse;
- replay esterni necessari alla riproducibilità, se dimensione e licenza lo consentono.

### Non conservare o ignorare

- `__pycache__`, cache test e ambienti virtuali;
- run interrotti senza informazione;
- duplicati byte-identici non richiesti dalla provenance;
- log temporanei e dump esplorativi non promossi;
- directory di run vuote.

### Conservare fuori dal percorso attivo

- risultati storici completi E01–E16;
- prompt ormai eseguiti;
- screenshot storici;
- review sostituite ma ancora utili alla provenance.

Questi elementi vanno sotto `experiments/archive/<round>/`, non mescolati con
E17.

## 8. Migrazione raccomandata

### Fase 0 — Freeze e inventario

1. congelare lo stato Git corrente;
2. generare inventario path → hash → ruolo → destinazione;
3. identificare riferimenti nei Markdown, script e test;
4. non cancellare ancora nulla.

### Fase 1 — E17 come vertical slice

Creare `experiments/e17/` e migrare soltanto il round corrente:

| Origine | Destinazione |
|---|---|
| `docs/experiment_designs/e17/` | `experiments/e17/design/` |
| `docs/prompts/E17_*` | `experiments/e17/prompts/common/` o agente |
| `results/e17/*` | `experiments/e17/reports/` e `artifacts/` secondo tipo |
| `scripts/e17/*` | `experiments/e17/tools/` |
| future config E17 | `experiments/e17/configs/` |
| future test E17 | `experiments/e17/tests/` |

Aggiornare tutti i riferimenti e aggiungere `experiments/e17/README.md`.

### Fase 2 — Dati esterni

Migrare `docs/benchmark/*.json` in `data/replays/`, separando reference e
discovery E17. Spostare il catalogo in `data/replays/MANIFEST.md`.

### Fase 3 — Archivio storico

Migrare un round per volta, iniziando da E16 e scendendo. Per ogni round:

1. riunire design, prompt, version docs e risultati;
2. mantenere un solo README/index;
3. conservare solo run informativi o citati;
4. verificare link e hash;
5. rimuovere le vecchie directory soltanto dopo il controllo.

### Fase 4 — Normalizzazione trasversale

- spostare le review Foundation da `results/model_spec_c2/` a
  `docs/governance/` o all'archivio relativo;
- lasciare in `docs/model_specs/` soltanto le specifiche attive;
- eliminare `docs/versions/` e `docs/prompts/` dopo svuotamento verificato;
- ridurre `scripts/` al tooling comune;
- aggiornare README, PROJECT_STATE e NEW_SESSION.

## 9. Gate della migrazione

```text
NO_LOST_TRACKED_FILES: true
ALL_MOVES_HAVE_SOURCE_AND_DESTINATION: true
SHA256_PRESERVED_FOR_IMMUTABLE_ARTIFACTS: true
MARKDOWN_LINK_CHECK: PASS
PYTHON_IMPORT_AND_TEST_CHECK: PASS
SUBMISSION_HASH_UNCHANGED: true
GIT_STATUS_REVIEWED: true
```

La migrazione deve essere un cambiamento strutturale separato dallo sviluppo
E17.0: nessuna modifica di policy, telemetria o risultato va mescolata con i
move del repository.

## 10. Raccomandazione

Adottare la struttura verticale e partire soltanto da E17. È il round attivo,
ha ancora pochi artefatti e permette di validare la convenzione con rischio
contenuto. Dopo un commit esclusivamente strutturale e il controllo dei link,
archiviare E16→E01 in lotti separati.

Non eseguire una grande riscrittura atomica dell'intero repository: renderebbe
difficile distinguere move, cancellazioni, correzioni di link e modifiche
semantiche.
