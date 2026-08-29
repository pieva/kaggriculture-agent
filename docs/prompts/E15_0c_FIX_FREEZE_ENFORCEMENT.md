# E15.0c — Correzione runner per enforcement del freeze

## Obiettivo

Correggere **esclusivamente** il blocking issue individuato dalla review neutrale E15.0b di Codex:

> Il runner E15 esegue attualmente le submission live da `submission/` e non rifiuta automaticamente l'esecuzione se gli hash differiscono dagli artefatti congelati.

La correzione deve rendere il freeze **enforced by code**, senza modificare:

- ONTOLOGY;
- MODEL_SPEC;
- strategie;
- submission candidate;
- seed;
- piano del torneo;
- artefatti frozen;
- risultati E13/E14.

NON eseguire alcun match.

---

## 1. Safety

Prima di qualsiasi modifica esegui:

```powershell
git status --short
git branch --show-current
git log -1 --oneline
```

Il working tree dirty è lo stato autorevole.

NON eseguire:

```text
git reset
git clean
git stash
git revert
```

NON fare:

- commit;
- push;
- Kaggle upload;
- rebuild delle submission;
- modifica di MODEL_SPEC;
- modifica delle strategie;
- modifica delle submission;
- rigenerazione del freeze;
- M1;
- M2;
- M3.

---

## 2. Source of truth del freeze

Il freeze E15 già verificato da Codex è valido e NON deve essere rigenerato.

Manifest:

```text
results/e15/freeze/FREEZE_MANIFEST.md
```

Hash frozen verificati 7/7 MATCH:

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

Codex ha inoltre verificato:

```text
source ↔ frozen = IDENTICAL per tutti e 7
Copilot ownership = CONFIRMED
P0/P1 = NO_MATERIAL_POSITION_BIAS_FOUND
post-freeze contamination = HARMLESS_POST_FREEZE_CHANGE
```

Il solo blocking issue è il runner.

---

# 3. File modificabile

Puoi modificare esclusivamente:

```text
scripts/run_e15_tournament.py
```

Se assolutamente necessario per testare il runner, puoi creare/modificare un test dedicato E15, ma NON modificare altri file operativi.

Preferisci evitare nuovi artefatti se non necessari.

---

# 4. Comportamento richiesto

La soluzione preferita è:

## Eseguire direttamente le frozen submission

Il runner deve usare:

```text
results/e15/freeze/submission_antigravity_E15_FROZEN.py
results/e15/freeze/submission_codex_E15_FROZEN.py
results/e15/freeze/submission_copilot_E15_FROZEN.py
```

e NON:

```text
submission/submission_antigravity.py
submission/submission_codex.py
submission/submission_copilot.py
```

come input competitivo.

Questo elimina la dipendenza dallo stato live del repository.

---

# 5. Verifica obbligatoria degli hash

Prima di qualsiasi match, il runner deve:

1. calcolare SHA256 degli artefatti frozen necessari;
2. confrontarli con gli hash attesi del freeze;
3. abortire con errore chiaro se anche un solo hash non corrisponde.

Almeno devono essere verificati:

- ONTOLOGY frozen;
- MODEL_SPEC frozen dei due partecipanti;
- submission frozen dei due partecipanti.

Preferibilmente verifica tutti i 7 artefatti a ogni invocation, dato il costo trascurabile.

Il controllo deve avvenire **prima** della creazione/esecuzione dell'environment competitivo.

---

# 6. Manifest come riferimento

Preferisci leggere gli hash da:

```text
results/e15/freeze/FREEZE_MANIFEST.md
```

se puoi farlo in modo semplice e robusto.

In alternativa puoi mantenere una struttura hash dichiarata nel runner, purché:

- corrisponda esattamente al manifest;
- sia verificata da test/validate;
- non possa essere sovrascritta via CLI.

Non introdurre complessità inutile.

---

# 7. Seed immutabili

NON modificare i seed:

```text
M1 = 1113294977
M2 = 3033283457
M3 = 3122977751
```

Mappatura:

```text
M1: Antigravity P0 vs Codex P1
M2: Codex P0 vs Copilot P1
M3: Copilot P0 vs Antigravity P1
```

Il runner deve continuare a impedire reroll automatici.

---

# 8. Metadata

`match_metadata.json` deve registrare gli hash degli **artefatti frozen realmente eseguiti**.

In particolare:

```text
submission_0_sha256
submission_1_sha256
ontology_sha256
model_spec_0_sha256
model_spec_1_sha256
```

Gli hash registrati devono provenire dai file frozen verificati, non dai file live.

Aggiungi, se utile:

```text
freeze_manifest_path
frozen_submission_0_path
frozen_submission_1_path
```

per rendere evidente la provenienza.

---

# 9. Modalità --validate

La modalità:

```text
python scripts/run_e15_tournament.py --validate
```

deve:

- verificare presenza dei file;
- verificare gli hash;
- verificare match map;
- verificare seed;
- verificare directory output;
- NON creare un episodio competitivo;
- NON eseguire un match.

Output atteso concettualmente:

```text
FREEZE INTEGRITY: PASS
M1: READY
M2: READY
M3: READY
NO MATCH EXECUTED
```

Non è necessario usare esattamente queste stringhe.

---

# 10. Fail closed

Il runner deve essere **fail-closed**.

Se:

- manca un frozen artifact;
- un SHA256 non corrisponde;
- un match_id non è valido;
- un seed non corrisponde alla configurazione pre-dichiarata;
- una frozen submission non è quella prevista;

allora:

```text
ABORT
```

prima dell'esecuzione dell'environment.

NON fare fallback sulle submission live.

NON rigenerare file automaticamente.

NON ricostruire submission automaticamente.

---

# 11. Protezione artefatti frozen

Il runner NON deve scrivere in:

```text
results/e15/freeze/
```

Gli output devono restare nelle directory match separate:

```text
results/e15/M1_antigravity_vs_codex/
results/e15/M2_codex_vs_copilot/
results/e15/M3_copilot_vs_antigravity/
```

Non modificare il freeze manifest.

---

# 12. Test consentiti

Puoi eseguire esclusivamente test che NON avviano un match competitivo reale.

Sono consentiti:

```text
--validate
import del modulo
hash verification
path verification
CLI argument validation
mock/unit test
```

È utile verificare anche il fail-closed con un test non distruttivo, ad esempio confrontando in memoria un hash errato o usando una funzione testabile.

NON alterare temporaneamente i file frozen per provocare il mismatch.

---

# 13. Extra artifacts E15.0a

Codex ha individuato:

```text
docs/model_specs/copilot/E15_0a_OWNERSHIP_VERIFICATION_REPORT.md
verify_copilot_freeze.py
```

e li ha classificati:

```text
AUDIT_TRAIL_ONLY
```

NON toccarli in questa fase.

Non sono blocking.

---

# 14. Verifica finale

Al termine esegui:

```powershell
python scripts/run_e15_tournament.py --validate
git diff --check -- scripts/run_e15_tournament.py
git diff -- scripts/run_e15_tournament.py
git status --short
```

NON eseguire match.

---

# 15. Risposta finale richiesta

Riporta:

1. modifica effettuata in `run_e15_tournament.py`;
2. conferma che ora vengono eseguite direttamente le frozen submission;
3. path frozen usati per M1/M2/M3;
4. modalità di verifica SHA256;
5. comportamento fail-closed;
6. conferma seed invariati;
7. conferma che i metadata useranno hash frozen;
8. risultato di `--validate`;
9. risultato `git diff --check -- scripts/run_e15_tournament.py`;
10. `git status --short`;
11. conferma esplicita:

```text
ONTOLOGY NON MODIFICATA
MODEL_SPEC NON MODIFICATI
STRATEGIE NON MODIFICATE
SUBMISSION NON MODIFICATE
FREEZE NON RIGENERATO
SEED NON MODIFICATI
NESSUN MATCH E15 ESEGUITO
NESSUN COMMIT
NESSUN PUSH
```

Fermati e attendi approvazione.

NON avviare M1.
