# E15.0e — Close pre-tournament state, cleanup, documentation, commit & push — ANTIGRAVITY

## Obiettivo

Chiudere formalmente la fase **E15.0 pre-torneo** dopo la certificazione finale di Codex:

```text
ACCEPT_E15_FREEZE
```

con:

- blocking issue E15.0b = `RESOLVED`;
- freeze integrity = `7/7 MATCH`;
- frozen execution = `PASS`;
- SHA256 enforcement = `PASS`;
- fail-closed prima dell'environment = `PASS`;
- seed/match map = confermati;
- metadata provenance = `PASS`;
- output isolation = `PASS`;
- nessun nuovo blocking issue;
- nessun match E15 ancora eseguito.

Questa fase serve a:

1. fare cleanup degli artefatti temporanei non necessari;
2. aggiornare lo stato documentale del progetto;
3. registrare con precisione freeze, governance e piano torneo;
4. eseguire le verifiche finali;
5. creare commit e push del checkpoint pre-torneo;
6. lasciare `NEW_SESSION.md` pronto per una nuova chat che inizi da **M1**.

NON eseguire M1/M2/M3 in questa fase.

---

# 1. Safety iniziale

Esegui:

```powershell
git status --short
git branch --show-current
git log -1 --oneline
```

Il working tree dirty è lo stato autorevole.

NON usare:

```text
git reset
git clean
git stash
git revert
```

NON eseguire:

- match E15;
- Kaggle upload;
- rebuild delle submission;
- modifica delle strategie;
- modifica degli artefatti frozen;
- modifica di seed;
- rigenerazione del freeze.

---

# 2. Stato certificato da preservare

La review finale Codex E15.0d ha certificato:

```text
ACCEPT_E15_FREEZE
```

## Frozen execution

```text
M1:
P0 experiments/archive/e15/artifacts/freeze/submission_antigravity_E15_FROZEN.py
P1 experiments/archive/e15/artifacts/freeze/submission_codex_E15_FROZEN.py

M2:
P0 experiments/archive/e15/artifacts/freeze/submission_codex_E15_FROZEN.py
P1 experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py

M3:
P0 experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py
P1 experiments/archive/e15/artifacts/freeze/submission_antigravity_E15_FROZEN.py
```

## Seed

```text
M1 = 1113294977
M2 = 3033283457
M3 = 3122977751
```

## Frozen hashes

```text
ONTOLOGY
5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa

MODEL_SPEC Antigravity
f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46

MODEL_SPEC Codex
9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7

MODEL_SPEC Copilot
d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686

Submission Antigravity
629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d

Submission Codex
fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3

Submission Copilot
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

NON modificare questi valori.

---

# 3. Cleanup controllato

Effettua un cleanup conservativo degli artefatti chiaramente temporanei creati durante E15.0a/E15.0b/E15.0c/E15.0d.

## Candidato certo alla rimozione

Se presente:

```text
verify_copilot_freeze.py
```

può essere eliminato, perché Codex lo ha classificato `AUDIT_TRAIL_ONLY` e non è necessario al torneo.

## Report ownership Copilot

Per:

```text
docs/model_specs/copilot/E15_0a_OWNERSHIP_VERIFICATION_REPORT.md
```

preferisci **CONSERVARLO** come audit trail dell'accettazione proprietaria della candidate Copilot, salvo evidenza che sia ridondante o errato.

## Non eliminare

NON eliminare:

- `results/e15/freeze/`;
- `FREEZE_MANIFEST.md`;
- `P0_P1_ENVIRONMENT_AUDIT.md`;
- `TOURNAMENT_PLAN.md`;
- MODEL_SPEC;
- ONTOLOGY;
- submission frozen;
- runner E15;
- documentazione storica utile;
- risultati E13/E14.

Se trovi altri file chiaramente temporanei, elencali prima di eliminarli e applica criterio conservativo.

---

# 4. Verifica struttura MODEL_SPEC / ontology

Non rivalutare i modelli.

Registra soltanto lo stato certificato:

```text
Canonical ontology: 64 concept_id

Antigravity:
64/64
USED 59
PARTIAL 4
NOT_USED 1
CONFLICT 0

Codex:
64/64
USED 37
PARTIAL 20
NOT_USED 7
CONFLICT 0

Copilot:
64/64
USED 50
PARTIAL 7
NOT_USED 7
CONFLICT 0
```

La governance resta:

- ontology = union/OR dei fenomeni rilevanti;
- presenza nel canonical registry != consenso;
- ogni modello mantiene indipendentemente USED/PARTIAL/NOT_USED;
- evidence status separato dalla presenza;
- policy e ranking restano model-owned.

---

# 5. Aggiornare PROJECT_STATE.md

Aggiorna:

```text
docs/PROJECT_STATE.md
```

per rappresentare con precisione lo stato corrente.

Deve risultare chiaramente che:

## E14 chiuso

- ontology canonicalizzata;
- 64 concept_id;
- tre MODEL_SPEC riallineati alla canonical ontology;
- freeze pre-match completato.

## E15.0 chiuso

- ownership Copilot verificata e accettata;
- freeze 7/7 verificato;
- P0/P1 audit completato;
- runner inizialmente rifiutato da Codex perché usava file live;
- E15.0c ha corretto il runner;
- E15.0d Codex ha emesso:

```text
ACCEPT_E15_FREEZE
```

## Stato attuale

```text
PRE-TOURNAMENT CHECKPOINT COMPLETE
NO E15 MATCH EXECUTED
NEXT ACTION = M1
```

Non dichiarare risultati di match che non esistono.

---

# 6. Aggiornare EXPERIMENT_LOG.md

Aggiorna:

```text
docs/EXPERIMENT_LOG.md
```

con una sezione E15.0 sintetica ma verificabile.

Includi almeno:

### E15.0 — Pre-Tournament Freeze & Governance

- freeze dei 7 artefatti;
- hash SHA256;
- cardinalità MODEL_SPEC;
- ownership review Copilot;
- review neutrale Codex E15.0b;
- blocking issue del runner;
- fix E15.0c;
- certificazione Codex E15.0d;
- verdict finale:

```text
ACCEPT_E15_FREEZE
```

- nessun match eseguito.

Registra anche:

```text
M1 Antigravity P0 vs Codex P1 — seed 1113294977
M2 Codex P0 vs Copilot P1 — seed 3033283457
M3 Copilot P0 vs Antigravity P1 — seed 3122977751
```

e il tie-break pre-dichiarato:

```text
primary: head-to-head wins

if all 1–1:
aggregate signed final-money differential

D_i = Σ(final_money_i - final_money_opponent)
```

Nessun quarto match automatico.

---

# 7. Aggiornare NEW_SESSION.md

Aggiorna:

```text
docs/NEW_SESSION.md
```

perché sia il documento operativo di apertura della prossima chat.

Deve iniziare con lo stato attuale, non con cronologia prolissa.

La nuova sessione deve poter partire direttamente da:

```text
E15 — TOURNAMENT
NEXT ACTION: RUN M1 ONLY
```

## Inserire chiaramente

### Freeze

```text
ACCEPT_E15_FREEZE
7/7 SHA256 MATCH
runner fail-closed
frozen artifacts executed directly
```

### M1

```text
Antigravity P0 vs Codex P1
seed 1113294977
```

### Runner

Comando effettivo da usare, ricavato dal CLI reale, ad esempio:

```powershell
python experiments/archive/e01/tools/run_e15_tournament.py --match M1
```

Usa il comando esatto supportato dal runner.

### Vincolo

```text
DO NOT RUN M2 OR M3 UNTIL M1 HAS BEEN ANALYZED
```

### Pipeline post-M1

Dopo M1:

1. preservare raw replay + telemetry + metadata;
2. ChatGPT fa analisi indipendente usando:
   - frozen ontology;
   - frozen MODEL_SPEC Antigravity;
   - frozen MODEL_SPEC Codex;
   - JSON/replay;
3. classificare i concept discriminati con:
   - SUPPORTED
   - WEAKENED
   - NOT_DISCRIMINATED
   - CONFOUNDED
   - INCONCLUSIVE
4. soltanto dopo raccogliere feedback/challenge di Antigravity e Codex;
5. sintesi ChatGPT;
6. aggiornamento model-owned post-match;
7. poi autorizzazione M2.

Sottolinea:

```text
victory != model validity
```

e:

```text
non inferire metriche non osservabili dal final score
```

---

# 8. README

Aggiorna `README.md` soltanto se serve davvero a riflettere il nuovo stato o la struttura definitiva.

Evita modifiche cosmetiche.

---

# 9. Verifica runner prima del commit

Esegui:

```powershell
.\.venv\Scripts\python.exe experiments/archive/e01/tools/run_e15_tournament.py --validate
```

oppure il comando Python corretto per l'ambiente corrente.

Deve risultare:

```text
FREEZE INTEGRITY: PASS
M1: READY
M2: READY
M3: READY
NO MATCH EXECUTED
```

NON eseguire `--match`.

---

# 10. Test suite

Esegui la test suite pertinente.

Preferenza:

```powershell
.\.venv\Scripts\pytest.exe tests/
```

Se la suite completa ha failure preesistenti/non pertinenti, documentale con precisione e non nasconderle.

Non modificare strategie per far passare test non pertinenti.

---

# 11. Diff review finale

Prima del commit:

```powershell
git diff --check
git status --short
git diff --stat
```

Esamina il diff.

Verifica espressamente che:

- nessuna frozen submission sia cambiata;
- nessun frozen MODEL_SPEC sia cambiato;
- ONTOLOGY frozen non sia cambiata;
- seed siano invariati;
- runner sia quello certificato;
- nessun risultato M1/M2/M3 esista accidentalmente.

Se trovi un match E15 eseguito accidentalmente:

FERMATI.
NON COMMITTARE.
SEGNALA.

---

# 12. Git staging

Questa chiusura deve creare un checkpoint repository coerente.

Aggiungi i file pertinenti dell'intero lavoro E09–E15 presenti nel working tree e destinati al progetto, evitando cache/artefatti puramente temporanei.

Prima di `git add`, verifica `.gitignore`.

Non usare staging cieco se rischia di includere file indesiderati.

Dopo staging:

```powershell
git status --short
git diff --cached --stat
git diff --check --cached
```

Controlla che il commit includa:

- strategie/versioni necessarie;
- test;
- submission candidate;
- model specs;
- canonical ontology;
- freeze;
- E15 runner;
- audit e tournament plan;
- PROJECT_STATE;
- EXPERIMENT_LOG;
- NEW_SESSION;
- documentazione necessaria.

Non includere file temporanei chiaramente inutili.

---

# 13. Commit

Se tutte le verifiche sono positive, crea un singolo commit coerente.

Messaggio consigliato:

```text
Freeze E15 tournament candidates and finalize pre-match governance
```

oppure equivalente, ma chiaro.

Poi:

```powershell
git status
git log -1 --oneline
```

---

# 14. Push

Se il commit è riuscito e il working tree è pulito:

```powershell
git push origin main
```

Poi:

```powershell
git status
git log -1 --oneline
```

Non creare tag salvo istruzione esplicita.

---

# 15. Condizione finale obbligatoria

Il risultato desiderato è:

```text
branch: main
working tree: clean
freeze: ACCEPT_E15_FREEZE
E15 matches executed: 0
next action: M1
```

La nuova chat deve poter iniziare senza ricostruire E14/E15.0.

---

# 16. Risposta finale richiesta

Riporta:

## A. Cleanup
- file rimossi;
- file audit conservati.

## B. Documentazione
Conferma aggiornamento di:
- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`
- eventuale `README.md`

## C. E15 validation

```text
FREEZE INTEGRITY
M1 READY
M2 READY
M3 READY
NO MATCH EXECUTED
```

## D. Test

Riporta esito test suite.

## E. Freeze protection

Conferma:

```text
FROZEN ONTOLOGY UNCHANGED
FROZEN MODEL_SPEC UNCHANGED
FROZEN SUBMISSIONS UNCHANGED
SEEDS UNCHANGED
```

## F. Commit

Riporta:

```text
commit hash
commit subject
```

## G. Push

Conferma esito push.

## H. Final repository state

Riporta:

```text
git status
git log -1 --oneline
```

## I. Next session

Conferma:

```text
NEXT ACTION: M1 ONLY
Antigravity P0 vs Codex P1
seed 1113294977
```

e:

```text
M2/M3 NOT EXECUTED
```

Non eseguire M1.

Fermati dopo il push.
