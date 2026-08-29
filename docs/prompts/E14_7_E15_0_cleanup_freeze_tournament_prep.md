# E14.7 + E15.0 — Cleanup, Freeze Pre-Match e Preparazione del Torneo

## Obiettivo

Chiudere formalmente E14 e preparare E15 senza eseguire ancora alcun match.

Questa fase deve:

1. eliminare gli artefatti ontologici intermedi ormai superati;
2. verificare che l'ontologia canonica e i tre MODEL_SPEC siano coerenti e completi;
3. congelare in modo verificabile lo stato pre-match;
4. verificare le tre submission candidate;
5. ispezionare l'environment per eventuali bias strutturali P0/P1;
6. preparare il runner e la struttura di output dei tre match E15;
7. NON eseguire ancora il torneo;
8. NON modificare i modelli, le strategie o le submission.

---

## 1. Safety e stato repository

Prima di qualsiasi attività esegui:

```powershell
git status --short
git branch --show-current
git log -1 --oneline
```

Il working tree può essere già dirty e rappresenta lo stato autorevole corrente.

### Vietato

NON eseguire:

```text
git reset
git clean
git stash
git revert
```

Inoltre:

- NON fare commit;
- NON fare push;
- NON caricare submission su Kaggle;
- NON eseguire match E15;
- NON modificare strategy;
- NON modificare submission candidate;
- NON modificare ranking, impact, confidence o policy dei MODEL_SPEC;
- NON modificare l'ontologia canonica salvo correzioni puramente documentali già richieste e necessarie per il cleanup;
- NON sovrascrivere risultati E13/E14;
- NON cancellare output storici diversi dagli artefatti E14 esplicitamente indicati.

---

# PARTE A — E14.7 CLEANUP

## 2. Source of truth E14

La sola ontologia operativa deve essere:

```text
docs/model_specs/ONTOLOGY.md
```

La cardinalità canonica è:

```text
64 concept_id
```

I tre MODEL_SPEC attivi sono:

```text
docs/model_specs/antigravity/MODEL_SPEC.md
docs/model_specs/codex/MODEL_SPEC.md
docs/model_specs/copilot/MODEL_SPEC.md
```

Tutti e tre devono coprire esattamente 64/64 concept_id canonici.

---

## 3. Eliminazione artefatti intermedi

Elimina, se presenti, gli artefatti E14 ormai superati:

```text
docs/model_specs/ONTOLOGY_DRAFT.md
```

e, nelle tre directory agente, i file equivalenti a:

```text
ontology_proposal.md
ONTOLOGY_PROPOSAL.md
ONTOLOGY_VERIFICATION.md
```

per:

```text
antigravity
codex
copilot
```

Usa i nomi reali presenti nel repository.

### Non eliminare

NON eliminare:

- `ONTOLOGY.md`;
- i tre `MODEL_SPEC.md`;
- documentazione storica generale E13/E14;
- risultati benchmark;
- replay;
- JSON;
- submission;
- prompt storici, salvo riferimenti esplicitamente obsoleti che creino ambiguità operativa.

---

## 4. Controllo riferimenti orfani

Dopo il cleanup cerca riferimenti a:

```text
ONTOLOGY_DRAFT
ontology_proposal
ONTOLOGY_PROPOSAL
ONTOLOGY_VERIFICATION
```

in:

```text
README.md
docs/
```

Classifica ogni occorrenza come:

- storico legittimo;
- riferimento operativo obsoleto.

Correggi SOLO i riferimenti operativi obsoleti.

Non riscrivere la storia dell'esperimento.

La documentazione può ricordare che proposal e verification sono esistite, ma non deve più indicarle come source of truth o input necessario per E15.

---

# PARTE B — VERIFICA PRE-FREEZE

## 5. Verifica ontologia canonica

Controlla `docs/model_specs/ONTOLOGY.md`.

Deve risultare inequivocabile che:

- il canonical registry contiene esattamente 64 concept_id;
- i termini storici esclusi/fusi non fanno parte del registry;
- i verdict E15 disponibili sono:

```text
SUPPORTED
WEAKENED
NOT_DISCRIMINATED
CONFOUNDED
INCONCLUSIVE
```

- evidence status e observability restano assi distinti;
- `final_money_outcome` è un outcome e non una spiegazione causale.

Non cambiare la sostanza dell'ontologia.

---

## 6. Audit dei tre MODEL_SPEC

Verifica tutti e tre:

```text
docs/model_specs/antigravity/MODEL_SPEC.md
docs/model_specs/codex/MODEL_SPEC.md
docs/model_specs/copilot/MODEL_SPEC.md
```

Per ciascuno controlla:

1. presenza della sezione `Canonical Ontology Mapping`;
2. copertura 64/64;
3. nessun concept_id canonico mancante;
4. nessun concept_id extra nella tabella;
5. `USED + PARTIAL + NOT_USED = 64`;
6. nessun `CONFLICT` non dichiarato;
7. ranking pre-match presente;
8. impact pre-match presente ove previsto dal modello;
9. confidence pre-match presente ove previsto dal modello;
10. policy e assunzioni strategiche pre-match preservate.

### Controllo specifico Copilot

Verifica la coerenza tra:

- conteggio `NOT_USED`;
- righe con `mapping = ABSENT`;
- eventuali descrizioni testuali che elencano concetti "not used".

Non assumere che `ABSENT` significhi automaticamente `NOT_USED`.

Se i dati sono coerenti, non modificare nulla.

Se c'è solo un errore aritmetico o descrittivo nella nuova sezione di mapping, correggi esclusivamente quello senza cambiare alcun giudizio del modello.

---

# PARTE C — E15.0 FREEZE PRE-MATCH

## 7. Principio di freeze

Dopo questa fase devono essere materialmente identificabili e verificabili:

- ontologia canonica;
- tre MODEL_SPEC pre-match;
- tre submission candidate;
- versioni esatte delle strategie effettivamente incorporate nelle submission;
- ranking / impact / confidence pre-match;
- definizioni delle metriche E15.

Da questo momento fino alla conclusione di M3:

**nessun MODEL_SPEC, strategy o submission candidate può essere modificato.**

---

## 8. Snapshot pre-match

Crea una directory dedicata, ad esempio:

```text
results/e15/freeze/
```

oppure usa una struttura E15 già esistente se coerente.

Crea copie snapshot read-only/logiche dei seguenti file:

```text
docs/model_specs/ONTOLOGY.md
docs/model_specs/antigravity/MODEL_SPEC.md
docs/model_specs/codex/MODEL_SPEC.md
docs/model_specs/copilot/MODEL_SPEC.md
submission/submission_antigravity.py
submission/submission_codex.py
submission/submission_copilot.py
```

Usa nomi inequivocabili, per esempio:

```text
ONTOLOGY_E15_FROZEN.md
MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md
MODEL_SPEC_CODEX_E15_FROZEN.md
MODEL_SPEC_COPILOT_E15_FROZEN.md
submission_antigravity_E15_FROZEN.py
submission_codex_E15_FROZEN.py
submission_copilot_E15_FROZEN.py
```

Non modificare il contenuto durante la copia.

---

## 9. Hash del freeze

Calcola SHA256 per tutti gli artefatti congelati.

Crea:

```text
results/e15/freeze/FREEZE_MANIFEST.md
```

Il manifest deve contenere almeno:

| artifact | source_path | frozen_path | sha256 |
|---|---|---|---|

Aggiungi inoltre:

- branch;
- ultimo commit visibile da `git log -1 --oneline`;
- timestamp locale;
- nota che il working tree era dirty;
- conferma che il freeze rappresenta lo stato autorevole pre-E15.

NON fare commit per ottenere il freeze.

Lo SHA256 è il riferimento di integrità.

---

# PARTE D — VERIFICA TECNICA DELLE SUBMISSION

## 10. Candidate da verificare

Le candidate E15 sono esclusivamente:

```text
submission/submission_antigravity.py
submission/submission_codex.py
submission/submission_copilot.py
```

Verifica per ciascuna:

- importabilità;
- entry point corretto;
- assenza di dipendenze locali non incluse;
- compatibilità con l'environment;
- nessuna dipendenza dal path repository durante l'esecuzione;
- nessuna mutazione o riferimento accidentale alle submission degli altri agenti.

Usa gli script di verifica già presenti quando applicabili.

NON ricostruire le candidate se non necessario.

Se una candidate non è tecnicamente eseguibile, fermati e segnala il problema prima di qualsiasi match.

Non correggere la strategia in questa fase.

---

# PARTE E — AUDIT P0/P1 DELL'ENVIRONMENT

## 11. Obiettivo

Prima del torneo verifica se l'environment introduce differenze strutturali tra player 0 e player 1.

Questo audit deve essere svolto leggendo il codice dell'environment e/o con test locali non competitivi a costo Kaggle nullo.

Verifica almeno:

- ordine di inizializzazione dei player;
- ordine di applicazione delle action;
- ordine di aggiornamento del mercato;
- tie-breaking;
- accesso a inventory/market condivisi;
- RNG;
- eventuali loop sequenziali per player;
- premi o penalità dipendenti dall'indice;
- ordine di risoluzione di BUY/SELL/HIRE;
- limiti di market order;
- eventuale first-mover advantage;
- eventuale last-mover advantage.

---

## 12. Seed e RNG

Documenta:

- dove viene inizializzato il seed;
- quali componenti consumano RNG;
- se i due agenti possono consumare la sequenza RNG in modo differente;
- se usare lo stesso seed in match diversi garantirebbe o NON garantirebbe condizioni direttamente comparabili.

Non assumere equivalenza tra stesso seed e stessa traiettoria casuale.

---

## 13. Esito audit P0/P1

Crea:

```text
results/e15/P0_P1_ENVIRONMENT_AUDIT.md
```

Con una conclusione tra:

```text
NO_MATERIAL_POSITION_BIAS_FOUND
POTENTIAL_POSITION_BIAS
MATERIAL_POSITION_BIAS_FOUND
INCONCLUSIVE
```

Ogni conclusione deve citare file/funzioni/righe o test che la supportano.

Se emerge `MATERIAL_POSITION_BIAS_FOUND`, NON preparare il torneo come 3 match non speculari senza segnalarlo esplicitamente.

Fermati prima dell'esecuzione.

---

# PARTE F — DISEGNO DEL TORNEO E15

## 14. Round robin

Preparare esattamente questi tre match:

```text
M1: Antigravity vs Codex
M2: Codex vs Copilot
M3: Copilot vs Antigravity
```

Assegnazione posizione:

| Match | P0 | P1 |
|---|---|---|
| M1 | Antigravity | Codex |
| M2 | Codex | Copilot |
| M3 | Copilot | Antigravity |

In questo modo ogni agente gioca:

- una volta come P0;
- una volta come P1.

NON creare automaticamente match speculari.

---

## 15. Seed del torneo

Pre-dichiara ora i tre seed E15.

Requisiti:

- tre seed distinti;
- generati e registrati prima di vedere qualsiasi risultato;
- nessun reroll successivo;
- nessuna scelta basata sulla performance dei modelli;
- nessun riuso del seed decisivo E13.

Registra i seed in:

```text
results/e15/TOURNAMENT_PLAN.md
```

Se il repository dispone già di una convenzione deterministica per generare seed, usala.

Altrimenti genera i tre valori una sola volta con un metodo documentato e riproducibile.

NON eseguire i match.

---

## 16. Criterio classifica pre-dichiarato

Inserisci nel piano:

### Primary
Numero di vittorie head-to-head.

### Tie
Se tutti terminano 1–1:

```text
aggregate signed final-money differential
```

Per agente `i`:

```text
D_i = Σ (final_money_i - final_money_opponent)
```

calcolato sui due match disputati.

NON introdurre altri tie-break dopo aver visto i risultati.

NON prevedere automaticamente un quarto match.

---

# PARTE G — TELEMETRIA E OUTPUT DEI MATCH

## 17. Telemetria minima E15

Il runner deve preservare, quando osservabili o derivabili:

### Outcome / economy

- final money;
- money trajectory;
- realized revenue;
- market costs;
- transaction value e price provenance;
- revenue by category;
- terminal inventory quantity;
- unsold inventory valuation method quando disponibile.

### Land

- total land surface;
- activated land surface;
- crop surface maintained;
- pasture surface maintained;
- maintained productive surface.

### Workforce

- workforce headcount;
- worker capacity;
- total worker actions;
- actions by category;
- movement actions;
- productive action share;
- dispatch failures;
- worker_action_monetization_rate macro;
- worker_action_monetization_rate net quando definibile;
- necessary_transit_fraction solo se la regola di attribuzione è definibile.

### Crop

- PLANT;
- WATER;
- HARVEST;
- DIG;
- counts per day quando possibile;
- watering_execution_rate;
- watering_continuity;
- crop output;
- crop revenue;
- crop_care_completion_rate solo se il denominatore è definibile.

### Feed / livestock

- species;
- livestock headcount;
- feed availability;
- feed purchases;
- feed expenditure;
- Milk produced/sold;
- Wool produced/sold;
- Fertilizer produced/sold;
- pasture utilization quando osservabile.

### Capital / market

- cash trajectory;
- purchase timing;
- produced vs sold;
- sellthrough lag;
- reinvestment cash flow;
- observed/reconstructed prices;
- market order limit;
- action/order slot pressure quando misurabile.

### Diagnostics

- operational divergence onset;
- economic lock-in onset;
- local/Kaggle fidelity scope.

Se una metrica non è osservabile:

NON inventarla.

Classificala successivamente come `INCONCLUSIVE` quando necessaria alla verifica di un concept_id.

---

## 18. Output per singolo match

Prepara una struttura del tipo:

```text
results/e15/
├── freeze/
├── M1_antigravity_vs_codex/
├── M2_codex_vs_copilot/
└── M3_copilot_vs_antigravity/
```

Per ogni match il runner dovrà produrre almeno:

```text
match_metadata.json
raw_replay.json
telemetry.json
summary.json
```

Se l'environment genera già un replay in altro formato, preservalo senza conversione distruttiva.

### `match_metadata.json`

Deve includere almeno:

```text
match_id
seed
player_0
player_1
submission_0_sha256
submission_1_sha256
ontology_sha256
model_spec_0_sha256
model_spec_1_sha256
environment/version info
start timestamp
end timestamp
```

---

# PARTE H — PREPARAZIONE DEL RUNNER

## 19. Runner E15

Crea o adatta uno script dedicato, preferibilmente:

```text
scripts/run_e15_tournament.py
```

Deve supportare:

```text
--match M1
--match M2
--match M3
```

oppure un'interfaccia equivalente chiara.

### Requisito critico

Lo script NON deve eseguire automaticamente tutti i match quando viene creato o importato.

Ogni match deve richiedere un comando esplicito.

NON eseguire nessun match in E15.0.

---

## 20. Dry validation

È consentito:

- importare il runner;
- validare gli argomenti;
- verificare path;
- verificare SHA256;
- verificare che le submission siano individuate correttamente;
- eseguire test unitari o mock che NON avviino un episodio competitivo reale.

Non è consentito:

- avviare M1;
- avviare M2;
- avviare M3;
- generare risultati competitivi anticipati.

---

# PARTE I — PROTOCOLLO DI VERIFICA POST-MATCH

## 21. Non implementare ancora l'analisi post-match

Prepara nel `TOURNAMENT_PLAN.md` il protocollo, ma NON produrre verdict prima dei match.

Per ogni match la sequenza sarà:

```text
MATCH
→ JSON / replay
→ analisi neutrale ChatGPT
→ feedback indipendente dei due partecipanti
→ sintesi ChatGPT
→ verdict per concept_id discriminato
```

Verdict ammessi:

```text
SUPPORTED
WEAKENED
NOT_DISCRIMINATED
CONFOUNDED
INCONCLUSIVE
```

### Regola fondamentale

Vittoria del match ≠ validità automatica del modello.

Sconfitta del match ≠ falsificazione automatica del modello.

---

# PARTE J — FILE DA CREARE / MODIFICARE

## 22. Output consentiti

Puoi:

### eliminare
gli artefatti intermedi E14 indicati nella Parte A.

### creare
```text
results/e15/freeze/FREEZE_MANIFEST.md
results/e15/P0_P1_ENVIRONMENT_AUDIT.md
results/e15/TOURNAMENT_PLAN.md
scripts/run_e15_tournament.py
```

e le copie frozen elencate in precedenza.

### modificare
solo documentazione necessaria a rimuovere riferimenti operativi orfani a proposal/verification/draft.

NON modificare:

```text
docs/model_specs/ONTOLOGY.md
```

se non per una correzione puramente formale già necessaria a rendere inequivocabile il registry 64/64.

NON modificare sostanzialmente nessun:

```text
MODEL_SPEC.md
```

salvo eventuale correzione puramente aritmetica/descrittiva della sezione Copilot già indicata, se effettivamente necessaria.

---

# PARTE K — VERIFICA FINALE

## 23. Controlli

Esegui almeno:

```powershell
git diff --check
git status --short
```

Verifica inoltre:

- ONTOLOGY canonica = 64 concept_id;
- Antigravity = 64/64;
- Codex = 64/64;
- Copilot = 64/64;
- tre frozen MODEL_SPEC presenti;
- tre frozen submission presenti;
- SHA256 presenti;
- runner presente;
- runner non ha eseguito match;
- seed M1/M2/M3 già fissati;
- P0/P1 audit completato;
- nessuna strategy modificata;
- nessuna submission modificata;
- nessun MODEL_SPEC sostanzialmente modificato;
- nessun commit;
- nessun push.

---

# 24. Risposta finale richiesta

Riporta:

1. file eliminati durante E14.7;
2. eventuali riferimenti orfani corretti;
3. risultato audit 64/64 dei tre MODEL_SPEC;
4. eventuale correzione Copilot effettuata o conferma che non era necessaria;
5. path del `FREEZE_MANIFEST.md`;
6. hash SHA256 di:
   - ONTOLOGY;
   - 3 MODEL_SPEC;
   - 3 submission;
7. esito verifica tecnica delle tre submission;
8. esito P0/P1 audit;
9. seed fissati per M1/M2/M3;
10. path del `TOURNAMENT_PLAN.md`;
11. path del runner E15;
12. conferma esplicita:

```text
NESSUN MATCH E15 ESEGUITO
```

13. risultato `git diff --check`;
14. `git status --short`.

NON fare commit.
NON fare push.
NON avviare M1.

Fermati e attendi approvazione.
