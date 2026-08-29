# E15.0d — Final Freeze Certification — CODEX

## Obiettivo

Verificare in modalità **strettamente READ-ONLY** che la correzione E15.0c abbia eliminato l'unico blocking issue rilevato nella review E15.0b.

NON ripetere l'intero audit E15.0b.

Il precedente verdict era:

```text
REJECT_E15_FREEZE
```

per un solo motivo:

> `scripts/run_e15_tournament.py` eseguiva le submission live e non imponeva la corrispondenza con gli SHA256 frozen.

Antigravity ha ora modificato esclusivamente il runner per:

- eseguire direttamente le frozen submission;
- verificare 7/7 SHA256 prima di qualsiasi match;
- abortire fail-closed in caso di mismatch;
- usare gli hash frozen nei metadata;
- mantenere invariati match e seed.

Devi stabilire se il blocking issue è realmente risolto.

---

## 1. Safety

Esegui:

```powershell
git status --short
git branch --show-current
git log -1 --oneline
```

Questa review è READ-ONLY.

NON modificare alcun file.
NON creare report nel repository.
NON creare script.
NON creare memory file.
NON fare commit.
NON fare push.
NON eseguire M1/M2/M3.
NON rigenerare il freeze.

---

## 2. File da verificare

Leggi:

```text
scripts/run_e15_tournament.py
results/e15/freeze/FREEZE_MANIFEST.md
results/e15/TOURNAMENT_PLAN.md
```

e, solo per verificare path/hash, i sette artefatti in:

```text
results/e15/freeze/
```

Non è necessario rivalutare i MODEL_SPEC o l'ontologia: E15.0b li ha già verificati 64/64 e 7/7 MATCH.

---

## 3. Verifica artefatti realmente eseguiti

Conferma dal codice che M1/M2/M3 utilizzino direttamente:

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

Se esiste fallback automatico ai file live:

```text
REJECT_E15_FREEZE
```

---

## 4. Verifica SHA256 enforcement

Conferma che prima di creare/eseguire l'environment competitivo il runner:

1. legga gli hash attesi dal freeze;
2. calcoli gli SHA256 reali;
3. confronti expected vs observed;
4. abortisca se un file manca;
5. abortisca se anche un solo hash differisce.

Verifica che il controllo copra tutti e 7 gli artefatti frozen oppure, come minimo, tutti gli artefatti necessari al match.

La soluzione dichiarata da Antigravity è 7/7.

---

## 5. Verifica fail-closed

Controlla staticamente il control flow.

Un mismatch deve impedire di raggiungere:

```python
make("kaggriculture")
```

o equivalente creazione/esecuzione del match.

NON alterare i frozen file per testarlo.

Puoi usare test in-memory/read-only se strettamente necessario, senza creare file.

---

## 6. Verifica --validate

Puoi eseguire:

```powershell
python scripts/run_e15_tournament.py --validate
```

solo dopo aver verificato dal codice che non avvii alcun episodio.

Deve confermare:

```text
FREEZE INTEGRITY: PASS
M1 READY
M2 READY
M3 READY
NO MATCH EXECUTED
```

o equivalente.

---

## 7. Seed e match map

Conferma che siano rimasti:

```text
M1: Antigravity P0 vs Codex P1
seed = 1113294977

M2: Codex P0 vs Copilot P1
seed = 3033283457

M3: Copilot P0 vs Antigravity P1
seed = 3122977751
```

Nessun reroll.
Nessun override ambiguo.
Nessun match speculare automatico.

---

## 8. Metadata provenance

Conferma che `match_metadata.json` registri gli hash degli artefatti frozen realmente usati:

```text
submission_0_sha256
submission_1_sha256
ontology_sha256
model_spec_0_sha256
model_spec_1_sha256
```

e preferibilmente i relativi frozen path / manifest path.

---

## 9. Output isolation

Conferma che gli output siano separati:

```text
results/e15/M1_antigravity_vs_codex/
results/e15/M2_codex_vs_copilot/
results/e15/M3_copilot_vs_antigravity/
```

e che il runner non scriva in:

```text
results/e15/freeze/
```

---

## 10. Hash frozen

Ricalcola rapidamente i sette SHA256.

Devono restare:

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

Se uno differisce:

```text
REJECT_E15_FREEZE
```

---

# 11. Verdict

Usa ESATTAMENTE uno:

```text
ACCEPT_E15_FREEZE
REJECT_E15_FREEZE
INCONCLUSIVE
```

`ACCEPT_E15_FREEZE` significa che l'unico blocking issue di E15.0b è stato eliminato e non esistono nuovi blocking issue introdotti dal fix.

---

# 12. Risposta finale richiesta

Riporta:

### A. Verdict

```text
ACCEPT_E15_FREEZE
REJECT_E15_FREEZE
INCONCLUSIVE
```

### B. Blocking issue E15.0b

```text
RESOLVED
NOT_RESOLVED
INCONCLUSIVE
```

### C. Frozen execution

Indica i path realmente usati da M1/M2/M3.

### D. SHA256 enforcement

Indica:

```text
PASS
FAIL
```

e se è fail-closed prima dell'environment.

### E. Frozen integrity

```text
7/7 MATCH
```

oppure dettaglio mismatch.

### F. Seed / match map

Conferma o segnala differenze.

### G. Metadata provenance

```text
PASS
FAIL
```

### H. Output isolation

```text
PASS
FAIL
```

### I. --validate

Riporta l'esito senza eseguire match.

### J. Nuovi blocking issue

Se nessuno:

```text
NONE
```

### K. Conferme

```text
NESSUN FILE MODIFICATO
NESSUN MATCH E15 ESEGUITO
NESSUN COMMIT
NESSUN PUSH
```

Riporta infine:

```text
git status --short
```

Fermati.

NON avviare M1.
