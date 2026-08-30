# ANTIGRAVITY — FINAL REPOSITORY CLOSURE FOR MODEL_SPEC TOURNAMENT C2

## Mandato

Questa è la chiusura finale della fase di build dei tre concorrenti C2.

I tre candidati risultano completati e verificati:

```text
ANTIGRAVITY: TOURNAMENT_READY = YES
CODEX:       TOURNAMENT_READY = YES
COPILOT:     TOURNAMENT_READY = YES
```

Ultima verifica repository disponibile:

```text
pytest -q: 168 passed
git diff --check: PASS
```

Warning non bloccanti noti:

```text
.pytest_cache: WinError 5
LF -> CRLF warning su src/agricola/strategy/antigravity/__init__.py
```

Obiettivo di questo mandato:

```text
verificare integrità 3/3
chiudere le ultime correzioni locali Foundation non bloccanti
pulire i micro-prompt consumati
aggiornare stato progetto
preparare NEW_SESSION per il torneo
eseguire test finali
staging selettivo
commit unico
eventuale push
STOP
```

NON eseguire il torneo.

NON eseguire review post-torneo.

NON eseguire submission Kaggle.

---

# 1. Verifica iniziale obbligatoria

Prima di modificare qualsiasi file:

```powershell
git branch --show-current
git status --short
git diff --check
```

Rileggere lo stato reale del repository.

NON assumere che il working tree corrisponda a una fotografia precedente.

NON revertire modifiche preesistenti intenzionali.

NON usare:

```text
git add .
```

---

# 2. Verifica integrità dei tre candidati

Verificare l'esistenza e la coerenza minima dei tre set.

## Antigravity

Attesi almeno:

```text
docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md
src/agricola/strategy/antigravity/agent_c2.py
src/agricola/strategy/antigravity/c2_policy.py
src/agricola/strategy/antigravity/c2_config.py
tests/test_antigravity_c2.py
results/model_spec_c2/antigravity/BUILD_VERIFICATION.md
```

## Codex

Attesi almeno:

```text
docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md
src/agricola/strategy/codex_c2.py
configs/model_spec_c2/CODEX_C2_CONFIG.json
tests/test_codex_c2_candidate.py
results/model_spec_c2/codex/BUILD_VERIFICATION.md
```

## Copilot

Attesi almeno:

```text
docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md
src/agricola/strategy/copilot/c2_policy.py
src/agricola/strategy/copilot/c2_config.py
src/agricola/strategy/copilot/agent_c2.py
tests/test_copilot_c2.py
results/model_spec_c2/copilot/BUILD_VERIFICATION.md
```

Controllare che ciascun report dichiari o sia aggiornabile coerentemente a:

```text
TOURNAMENT_READY: YES
```

Per Codex, se il report è rimasto formalmente a `NO` per il precedente failure esterno nel namespace Copilot, aggiornare SOLO il report di build per registrare la verifica finale:

```text
repository pytest: PASS (168 passed)
git diff --check: PASS
TOURNAMENT_READY: YES
```

NON modificare MODEL_SPEC o policy Codex.

---

# 3. Correzioni locali Foundation ancora pendenti

La precedente verifica Codex aveva classificato come non bloccanti ma da correggere prima del freeze finale:

```text
State Machine C2 — wording FEED+CARE
Ontology C2 — pending_care_bonus_accumulation wording
```

Applicare SOLO queste correzioni locali se risultano ancora presenti.

Semantica normativa:

```text
CARE:
    cared_today = true

FEED:
    fed_today = true

EOD pending_care_bonus accumulation:
    requires cared_today AND fed_today

production-day consumption:
    distinct from EOD accumulation
```

Non aprire una nuova revisione generale della Foundation.

Non introdurre nuovi concetti.

Non modificare il Feature Model C2 salvo un errore materiale evidente scoperto durante la chiusura.

---

# 4. Stato Foundation

Dopo le correzioni locali, registrare con precisione:

```text
FOUNDATION C2: UPSTREAM_READY_FOR_MODEL_SPEC
FEATURE MODEL C2 BLOCKERS: CLOSED
MODEL_SPEC C2 BUILDS: 3/3 TOURNAMENT_READY
```

NON dichiarare automaticamente:

```text
FOUNDATION C2: FROZEN
```

a meno che esista già nel processo repository una procedura di freeze esplicita, completa e verificata che questo mandato può eseguire senza introdurre lavoro nuovo.

In assenza di tale procedura, mantenere:

```text
FOUNDATION C2: NOT FROZEN
```

ma chiarire che ciò NON blocca il torneo.

---

# 5. Pulizia controllata dei prompt

Pulire la proliferazione dei prompt operativi consumati sotto:

```text
docs/prompts/
```

Obiettivo:

```text
conservare i mandati metodologici principali
rimuovere micro-fix / micro-review / blocker-check ormai assorbiti negli artefatti finali
```

## Conservare sicuramente

Conservare:

```text
MASTER_MODEL_SPEC_C2_TOURNAMENT_BUILD_R2.md
```

e i prompt che rappresentano:

```text
major forensic analysis
Foundation reconciliation / major review mandate
major experimental mandate ancora utile alla tracciabilità
```

## Candidati forti alla rimozione

Valutare e rimuovere se ormai completamente assorbiti:

```text
COPILOT_FEATURE_MODEL_C2_REMEDIATION_R2.md
COPILOT_FEATURE_MODEL_C2_MICRO_FIX_R2_1.md
COPILOT_FEATURE_MODEL_C2_MICRO_FIX_R2_2.md
CODEX_FEATURE_MODEL_C2_BLOCKER_VERIFICATION_R2_1.md
CODEX_FEATURE_MODEL_C2_BLOCKER_REVERIFICATION_R2_2.md
```

Valutare analogamente altri prompt chiaramente superseded o one-shot.

NON eliminare i report finali sotto:

```text
docs/model/reviews/
```

La tracciabilità deve restare negli artefatti di review/evidence, non in decine di micro-prompt.

---

# 6. Aggiornamento PROJECT_STATE

Aggiornare `PROJECT_STATE.md` sul filesystem corrente.

Deve risultare almeno:

```text
Current phase:
MODEL_SPEC TOURNAMENT C2 — READY TO RUN

Foundation:
C2 upstream-ready
Feature Model blockers closed
Foundation C2 not frozen unless explicit freeze executed

Candidates:
Antigravity C2 — TOURNAMENT_READY
Codex C2 — TOURNAMENT_READY
Copilot C2 — TOURNAMENT_READY

Repository validation:
168 passed
git diff --check PASS

Tournament:
NOT RUN

Post-tournament reviews:
PENDING

Kaggle validation:
NOT RUN
```

Non includere un vincitore.

Non confrontare ancora qualitativamente i tre MODEL_SPEC.

---

# 7. Aggiornamento EXPERIMENT_LOG

Aggiungere una sola entry sintetica che chiuda la fase corrente.

Registrare:

```text
Foundation C2 blocker closure
3 independent MODEL_SPEC C2 builds
3 independent executables
all 3 TOURNAMENT_READY
168 tests PASS
no tournament yet
next experiment = MODEL_SPEC TOURNAMENT C2
```

Non trasformare il log in una nuova review.

---

# 8. README

Aggiornare `README.md` solo se necessario per riflettere correttamente la struttura corrente o i nuovi entrypoint C2.

Non aggiungere una lunga sezione metodologica se già presente altrove.

Se il README è già coerente, lasciare invariato.

---

# 9. NEW_SESSION — preparazione nuova chat

Aggiornare `NEW_SESSION.md` come handoff operativo per la nuova chat/esperimento.

Titolo/fase:

```text
MODEL_SPEC TOURNAMENT C2
```

La nuova sessione deve partire direttamente dall'esperimento, non da altra documentazione.

Includere:

```text
FOUNDATION C2:
- upstream-ready
- Feature Model blockers closed
- not frozen unless explicitly frozen in this closure
```

Tre candidati:

```text
ANTIGRAVITY C2
CODEX C2
COPILOT C2
```

con path a:

```text
MODEL_SPEC
candidate executable
BUILD_VERIFICATION
```

Stato:

```text
3/3 TOURNAMENT_READY
168 tests PASS
git diff --check PASS
TOURNAMENT NOT RUN
KAGGLE NOT RUN
```

---

# 10. Obiettivo della prossima chat

Scrivere chiaramente in `NEW_SESSION.md`:

```text
Obiettivo:
verificare se il lavoro sulla Foundation C2 e sui tre MODEL_SPEC
si traduce in migliore policy realization e performance.
```

Il torneo deve rispondere alla domanda:

> Quale dei tre MODEL_SPEC corregge meglio i meccanismi che hanno performato peggio, e quali modifiche decisionali producono un miglioramento verificabile?

---

# 11. Protocollo iniziale della prossima chat

Non eseguire il protocollo ora, ma inserirlo nell'handoff:

```text
1. verificare integrità dei tre candidati
2. definire/congelare un solo protocollo comune di torneo
3. stesso opponent/seed/configuration rules
4. stessa telemetry
5. stesso budget sperimentale
6. eseguire i tre candidati
7. confrontare outcome economici e meccanismi
8. produrre tre POST-TOURNAMENT REVIEW indipendenti
9. confrontare le tre review
10. selezionare il candidato più promettente
11. Kaggle external validation
```

---

# 12. Metriche da preservare nell'handoff

Elencare soltanto metriche realmente supportate/computabili, tra:

```text
final_money
completion
crop_target_attainment
active_crop_surface
maintained_productive_surface
watering_execution
watering_continuity
premature_harvest_count
failed_action_count
no_op_action_count
WEED/lost_tile_count
lost_tile_persistence
replant_latency
movement_share
productive_action_share
workforce_utilization
inventory state
market activity
livestock contribution, se rilevante
```

Non inventare valori.

---

# 13. Review post-torneo già contrattualizzate

In `NEW_SESSION.md` ricordare che, dopo il torneo, ciascun agente dovrà analizzare tutti e tre i concorrenti.

Struttura:

```text
RISULTATO
    ↓
MECCANISMO OSSERVATO
    ↓
DECISIONE MODEL_SPEC
    ↓
SPIEGAZIONE CAUSALE
    ↓
MODIFICA PROPOSTA
    ↓
PREVISIONE VERIFICABILE
```

La review post-torneo non è parte di questo mandato.

---

# 14. Verifica finale repository

Dopo tutte le modifiche:

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\pytest.exe -q
git --no-pager diff --check
git status --short
```

Target:

```text
pytest: 168 passed
git diff --check: PASS
```

Se il numero dei test aumenta per una modifica strettamente necessaria, è accettabile purché tutti passino.

Il warning `.pytest_cache` `WinError 5` è non bloccante.

Il warning LF→CRLF è non bloccante se `git diff --check` passa.

---

# 15. Audit prima dello staging

Prima di fare staging:

```powershell
git status --short
git diff --stat
git diff --check
```

Classificare ogni file modificato/untracked come:

```text
A. candidato C2
B. Foundation C2 / review necessaria
C. state/handoff
D. prompt cleanup
E. modifica preesistente intenzionale rilevante
F. estraneo al mandato
```

NON includere automaticamente i file di classe F.

NON revertire le modifiche intenzionali già presenti.

---

# 16. Staging selettivo

Usare esclusivamente:

```powershell
git add <path espliciti>
```

NON usare:

```text
git add .
git add -A
```

Dopo staging:

```powershell
git status --short
git diff --cached --stat
git diff --cached --check
```

Verificare che il commit rappresenti realmente la chiusura C2.

---

# 17. Commit unico

Se:

```text
3/3 candidati presenti
3/3 TOURNAMENT_READY
suite completa PASS
git diff --check PASS
NEW_SESSION aggiornato
state aggiornato
micro-prompt cleanup completata
```

creare un solo commit.

Messaggio consigliato:

```text
Build C2 model-spec tournament candidates
```

Poi:

```powershell
git status --short
git log -1 --oneline
```

---

# 18. Push

Se il branch corrente è il branch operativo previsto e `origin` è già configurato:

```powershell
git push origin <current-branch>
```

Non fare force push.

Se il push non è appropriato o fallisce per ragioni esterne, non alterare la storia locale.

Registrare semplicemente:

```text
PUSH: NOT PERFORMED | FAILED_EXTERNAL | COMPLETED
```

---

# 19. Nessun torneo in questa sessione

Dopo commit/push:

```text
STOP
```

NON:

```text
eseguire tournament runner
confrontare i tre risultati
produrre ranking
fare review post-tournament
preparare Kaggle submission
inviare Kaggle submission
```

La prossima chat deve partire pulita da:

```text
MODEL_SPEC TOURNAMENT C2
```

---

# 20. Output finale richiesto

Riportare:

```text
C2 CANDIDATES:
ANTIGRAVITY: TOURNAMENT_READY YES
CODEX: TOURNAMENT_READY YES
COPILOT: TOURNAMENT_READY YES

FOUNDATION C2:
UPSTREAM_READY: YES
FROZEN: YES | NO

LOCAL FOUNDATION CORRECTIONS:
<summary>

MICRO_PROMPT CLEANUP:
REMOVED:
- ...
PRESERVED:
- ...

PROJECT_STATE: UPDATED
EXPERIMENT_LOG: UPDATED
README: UPDATED | UNCHANGED
NEW_SESSION: UPDATED

FINAL TESTS:
pytest: PASS (<N> passed)
git diff --check: PASS

COMMIT:
<hash> <message>

PUSH:
COMPLETED | NOT_PERFORMED | FAILED_EXTERNAL

NEXT SESSION:
MODEL_SPEC TOURNAMENT C2
```

Chiudere con:

```text
MODEL_SPEC C2 BUILD PHASE: CLOSED
3/3 CANDIDATES: TOURNAMENT_READY
THREE_WAY_TOURNAMENT: NOT RUN
POST_TOURNAMENT_REVIEWS: PENDING
KAGGLE_VALIDATION: NOT RUN
NEW_SESSION: READY
```

STOP.
