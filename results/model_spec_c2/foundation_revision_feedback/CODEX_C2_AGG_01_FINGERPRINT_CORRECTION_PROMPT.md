# C2 â€” CODEX AGG-01 FINGERPRINT PROVENANCE CORRECTION

```text
AGENT: CODEX
PHASE: REVIEW / RECONCILIATION FIX
TASK_ID: C2-ENGINE-CONTRACT-AGG-01-FINGERPRINT-FIX
SCOPE: PROVENANCE CORRECTION ONLY
SEMANTIC_REAUDIT_AUTHORIZED: NO
FOUNDATION_MODIFICATION_AUTHORIZED: NO
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
CODE_MODIFICATION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Obiettivo

Risolvere esclusivamente il rilievo `AGG-01` emerso dalla review indipendente di Copilot sul documento:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

Copilot ha confermato la sostanza semantica dell'Engine Contract, ma non Ã¨ riuscito a riprodurre il fingerprint SHA-256 aggregato dichiarato.

Questa attivitÃ  NON deve riaprire l'audit biologico o semantico.

---

# 2. Rilievo da risolvere

L'audit Codex dichiara:

```text
EXPECTED / REPORTED AGGREGATE SHA256:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

con formula dichiarata:

```text
sha256(UTF8(join("\n", sort(relative_path + "\t" + file_sha256))))
```

e manifest pubblicato nel report.

Copilot, applicando la formula dichiarata al manifest dichiarato, ha ottenuto:

```text
COPILOT REPRODUCED SHA256:
1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d
```

Copilot classifica:

```text
DISCREPANCY_ID: AGG-01
SEVERITY: P3
TYPE: PROVENANCE / REPRODUCIBILITY
SEMANTIC_ENGINE_CONTRADICTION: NO
```

Antigravity aveva invece dichiarato di aver riprodotto il fingerprint Codex originale.

La discrepanza deve quindi essere risolta in modo meccanico e riproducibile.

---

# 3. Input canonici

Usare:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

e i file engine locali effettivamente indicati nel manifest.

Non assumere che il vecchio hash Codex o quello Copilot sia corretto.

Ricalcolare da zero.

---

# 4. Verifica obbligatoria dei singoli file

Ricalcolare SHA-256 byte-for-byte per:

```text
.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA

.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md

.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md

.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json

.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py
```

Confrontare ciascun risultato con il manifest pubblicato.

Produrre tabella:

```text
PATH
AUDIT_REPORTED_SHA256
RECOMPUTED_SHA256
MATCH
```

Se un singolo file non coincide, fermarsi e classificare la causa prima di ricalcolare l'aggregate.

---

# 5. Ricostruzione esatta del manifest

Costruire esplicitamente le righe che entrano nell'aggregate.

Per ogni riga mostrare esattamente:

```text
<relative_path>\t<sha256>
```

Specificare:

```text
PATH_ROOT:
PATH_SEPARATOR:
PATH_CASE:
SORT_ORDER:
TEXT_ENCODING:
LINE_SEPARATOR_BETWEEN_RECORDS:
TRAILING_NEWLINE: YES/NO
BOM: YES/NO
HASH_HEX_CASE: lower/upper
```

Non lasciare nessuno di questi aspetti implicito.

---

# 6. Riproduzione delle due hash discordanti

Tentare di riprodurre separatamente:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

e:

```text
1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d
```

Determinare quale differenza produce ciascun valore, per esempio:

- trailing newline;
- CRLF vs LF;
- path assoluto vs relativo;
- root differente;
- backslash vs slash;
- ordinamento differente;
- manifest con file differente;
- encoding;
- hash di file letto in text mode invece che binary;
- concatenazione differente;
- errore di trascrizione;
- altro.

Non limitarsi a scegliere una delle due hash: identificare la root cause.

---

# 7. Canonicalizzazione

Definire una sola procedura canonica, cross-platform e non ambigua.

Preferenza:

```text
1. SHA-256 di ogni file sui raw bytes.
2. Path relativi a una root esplicitamente dichiarata.
3. Path separator normalizzato a "/".
4. Record ordinati lessicograficamente per path normalizzato.
5. Ogni record:
   normalized_relative_path + "\t" + lowercase_file_sha256
6. Record concatenati con "\n".
7. Dichiarare esplicitamente se esiste o no trailing "\n".
8. UTF-8 senza BOM.
9. SHA-256 sui bytes UTF-8 risultanti.
```

Se questa procedura differisce da quella usata originariamente, dichiararlo.

---

# 8. Comando indipendente di riproduzione

Produrre almeno un comando/script minimale che un reviewer possa eseguire senza interpretazione manuale.

Deve:

- leggere i file in binary mode;
- calcolare i singoli hash;
- costruire il manifest canonico;
- stampare il manifest esatto;
- stampare l'aggregate SHA-256.

Il comando deve essere compatibile con l'ambiente del repository.

Non modificare file engine.

---

# 9. Correzione del report Codex

Dopo aver identificato la root cause, correggere esclusivamente le sezioni del report necessarie alla provenance:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

Sono consentite soltanto modifiche a:

- fingerprint aggregato;
- formula di aggregazione;
- manifest/path normalization;
- istruzioni di riproduzione;
- eventuali riferimenti interni al fingerprint;
- final verdict relativo alla riproducibilitÃ , se necessario.

NON modificare:

- clock semantics;
- species inventory;
- crop ledger;
- animal ledger;
- FEED/CARE semantics;
- fertilizer semantics;
- inventory semantics;
- serviceability;
- discrepancy semantic findings;
- replay reconciliation;
- policy/engine distinction.

Se per risolvere AGG-01 emergesse inaspettatamente una modifica semantica necessaria:

```text
SEMANTIC_CONTENT_CHANGED: YES
```

e NON procedere al freeze.

---

# 10. Report di correzione

Creare:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md
```

con almeno:

1. Issue statement.
2. Old reported aggregate.
3. Copilot reproduced aggregate.
4. Individual-file hash verification.
5. Exact old aggregation reconstruction.
6. Exact Copilot aggregation reconstruction, se riproducibile.
7. Root cause.
8. Canonical aggregation specification.
9. Canonical manifest.
10. New canonical aggregate.
11. Independent reproduction command.
12. Exact changes made to the Codex audit.
13. Confirmation that semantic content was or was not changed.
14. Final AGG-01 verdict.

---

# 11. Output finale obbligatorio

Chiudere con:

```text
AGG_01_REPRODUCED: YES/NO
OLD_CODEX_HASH_REPRODUCED: YES/NO
COPILOT_HASH_REPRODUCED: YES/NO

ROOT_CAUSE:
<precise cause>

OLD_REPORTED_HASH:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

COPILOT_REPORTED_HASH:
1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d

NEW_CANONICAL_HASH:
<sha256>

CANONICAL_REPRODUCTION_COMMAND:
<command or script>

AUDIT_DOCUMENT_CORRECTED: YES/NO
SEMANTIC_CONTENT_CHANGED: NO/YES

AGG_01_STATUS: RESOLVED/UNRESOLVED
ENGINE_CONTRACT_PROVENANCE_READY_FOR_REVIEW: YES/NO

FOUNDATION_MODIFIED: NO
MODEL_SPEC_MODIFIED: NO
CODE_MODIFIED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Se:

```text
SEMANTIC_CONTENT_CHANGED: YES
```

oppure:

```text
AGG_01_STATUS: UNRESOLVED
```

allora:

```text
ENGINE_CONTRACT_PROVENANCE_READY_FOR_REVIEW: NO
```

---

# 12. Gate successivo

Se e solo se:

```text
AGG_01_STATUS: RESOLVED
SEMANTIC_CONTENT_CHANGED: NO
ENGINE_CONTRACT_PROVENANCE_READY_FOR_REVIEW: YES
```

il passo successivo sarÃ  una review **mirata esclusivamente ad AGG-01 da parte di Copilot**.

Non richiedere una nuova review completa dell'Engine Contract.

```text
NEXT_ACTION_IF_PASS:
COPILOT AGG-01 ONLY RE-VERIFICATION
```
