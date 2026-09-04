# Prompt operativo — Codex
## Chiusura E15, aggiornamento stato e commit repository

Stai lavorando sul repository locale:

```text
C:\Users\pietr\Projects\kaggriculture-agent
```

Obiettivo: **chiudere formalmente E15 a livello documentale e Git**, senza alterare alcun artefatto frozen, MODEL_SPEC strategico o submission.

I rename dei MODEL_SPEC sorgente con agent prefix sono **già stati eseguiti dall'utente**. Non devi rifarli.

---

## 1. Stato canonico da registrare

E15 è concluso con il seguente stato:

```text
E15 — PAIRWISE TOURNAMENT
STATUS: EPISTEMICALLY CLOSED

Competitive result:
- Copilot: 2–0
- Codex: 1–1
- Antigravity: 0–2

Competitive winner: Copilot
Tie-break: not required
Frozen artifacts: unchanged
```

### M1
Antigravity vs Codex:
- Antigravity: $8,672
- Codex: $20,461
- Winner: Codex
- Consensus chiuso con doppio ACK

### M2
Codex vs Copilot:
- Codex: $27,510
- Copilot: $37,752
- Winner: Copilot
- Consensus chiuso con doppio ACK

### M3
Copilot vs Antigravity:
- Copilot: $26,629
- Antigravity: $9,371
- Winner: Copilot
- Consensus chiuso con:

```text
ACK_M3_CONSENSUS_ANTIGRAVITY
ACK_M3_CONSENSUS_COPILOT
```

---

## 2. Artefatto finale E15

Assicurati che esista nel repository:

```text
experiments/archive/e15/artifacts/E15_FINAL_TOURNAMENT_SYNTHESIS.md
```

Se il file è già presente, leggilo e preservane il contenuto sostanziale.

La sintesi finale deve rappresentare almeno:
- risultati M1/M2/M3;
- classifica finale;
- policy fingerprints replicati;
- modello empirico a due regimi;
- cosa E15 ha stabilito;
- cosa E15 non ha stabilito;
- verdict finali sui tre agenti;
- osservabilità mancanti;
- priorità post-E15;
- prossimo gate: **Model Capability Check**.

Non introdurre nuove interpretazioni strategiche non già approvate nei consensus.

---

## 3. File di stato da aggiornare

Esamina e aggiorna, se necessario:

```text
PROJECT_STATE.md
NEW_SESSION.md
EXPERIMENT_LOG.md
README.md
```

Aggiorna `README.md` **solo se contiene effettivamente lo stato corrente dell'esperimento**.

### PROJECT_STATE.md

Deve riportare chiaramente:
- E15 `EPISTEMICALLY CLOSED`;
- classifica finale;
- winner competitivo Copilot;
- M3 double ACK completato;
- frozen artifacts unchanged;
- risultato epistemico principale:
  - Antigravity replica in M1/M3 un failure mode sistematico;
  - Copilot replica in M2/M3 un policy footprint stabile;
  - state-capacity alignment / activated-maintained-monetized capacity emergono come discriminanti principali;
- modello empirico a due regimi:
  1. sotto-soglia operativa: irrigation/dispatch/maintenance dominano;
  2. sopra-soglia: monetization, alignment, capital timing, sell-through dominano;
- prossimo passo obbligatorio: **Model Capability Check prima di qualunque revisione MODEL_SPEC**.

### NEW_SESSION.md

Riscrivilo come handoff pulito per la prossima sessione.

La prossima sessione deve iniziare da:

```text
POST-E15 — MODEL CAPABILITY CHECK
```

Ordine operativo obbligatorio:
1. verificare i modelli disponibili per Antigravity, Codex e Copilot;
2. confrontarli sullo stesso task di reasoning basato sulla baseline E15;
3. scegliere e registrare il runtime/model per ciascun agente;
4. creare/aggiornare `AGENT_RUNTIME_MANIFEST.md`;
5. solo dopo autorizzare revisione indipendente dei MODEL_SPEC;
6. cross-review;
7. nuova freeze;
8. solo infine nuova generazione submission.

Specificare esplicitamente:

```text
DO NOT MODIFY E15 FROZEN ARTIFACTS.
DO NOT REVISE MODEL_SPEC BEFORE CAPABILITY CHECK.
DO NOT GENERATE NEW SUBMISSIONS YET.
```

### EXPERIMENT_LOG.md

Aggiungi una voce conclusiva E15 che riporti:
- esito M3;
- double ACK M3;
- chiusura epistemica E15;
- classifica;
- principali finding cross-match;
- baseline finale congelata;
- passaggio formale alla fase post-E15.

Non riscrivere la storia precedente dell'experiment log.

---

## 4. Convenzione nomi MODEL_SPEC

I rename sono già stati eseguiti.

Verifica soltanto che i working source correnti seguano la convenzione:

```text
docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY.md
docs/model_specs/codex/MODEL_SPEC_CODEX.md
docs/model_specs/copilot/MODEL_SPEC_COPILOT.md
```

Aggiorna eventuali riferimenti documentali rimasti ai vecchi nomi **solo se necessario**.

### Vincolo assoluto

Non rinominare e non modificare i frozen:

```text
docs/model_specs/antigravity/archive/e15/artifacts/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md
docs/model_specs/codex/archive/e15/artifacts/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md
docs/model_specs/copilot/archive/e15/artifacts/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md
```

e nessun altro file sotto `results/e15/freeze/`.

---

## 5. Frozen integrity check

Prima del commit verifica che gli hash SHA-256 E15 frozen siano invariati.

Hash attesi:

```text
ONTOLOGY_E15_FROZEN.md
5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa

MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md
f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46

MODEL_SPEC_CODEX_E15_FROZEN.md
9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7

MODEL_SPEC_COPILOT_E15_FROZEN.md
d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686

submission_antigravity_E15_FROZEN.py
629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d

submission_codex_E15_FROZEN.py
fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3

submission_copilot_E15_FROZEN.py
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Se anche **un solo hash non coincide**, fermati e segnala il problema. Non committare.

---

## 6. Validazioni

Esegui:

```powershell
git branch --show-current
git status --short

.\.venv\Scripts\python.exe experiments/archive/e01/tools/run_e15_tournament.py --validate
.\.venv\Scripts\pytest.exe tests/

git diff --check
git status --short
git diff --stat
```

Se esiste un validator specifico per frozen/hash già presente nel repository, usalo preferibilmente invece di creare script temporanei.

Non lasciare file diagnostici temporanei nel working tree.

---

## 7. Review pre-commit

Prima del commit controlla esplicitamente che:
- nessun file sotto `results/e15/freeze/` sia modificato;
- nessuna submission frozen sia modificata;
- nessun MODEL_SPEC strategico sia stato revisionato nel contenuto;
- il commit contenga solo:
  - chiusura E15;
  - aggiornamento stato/handoff/log;
  - eventuali fix di riferimenti ai rename già effettuati;
  - sintesi finale E15.

Mostra:

```powershell
git status --short
git diff --stat
git diff --check
```

Se il perimetro è corretto, procedi.

---

## 8. Commit e push

Esegui:

```powershell
git add .
git commit -m "Close E15 pairwise tournament"
git push origin main
```

Non creare tag in questa attività.

Dopo il push esegui:

```powershell
git status
git log -1 --oneline
```

Il working tree finale deve essere pulito.

---

## 9. Output finale richiesto

Restituisci un report sintetico con:

1. file aggiornati;
2. eventuali riferimenti corretti dopo i rename;
3. esito validator E15;
4. esito test;
5. esito frozen hash check;
6. commit hash + subject;
7. esito push;
8. `git status` finale;
9. conferma esplicita:

```text
E15 = EPISTEMICALLY CLOSED
FROZEN ARTIFACTS = UNCHANGED
POST-E15 NEXT GATE = MODEL CAPABILITY CHECK
```

Se trovi una discrepanza sostanziale, **non correggerla silenziosamente**: fermati e riportala.
