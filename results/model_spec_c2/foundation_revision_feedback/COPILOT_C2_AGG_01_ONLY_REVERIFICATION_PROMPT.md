# C2 â€” COPILOT AGG-01 ONLY RE-VERIFICATION

```text
AGENT: COPILOT
PHASE: REVIEW / FINAL PROVENANCE CHECK
TASK_ID: C2-ENGINE-CONTRACT-AGG-01-REVERIFY
SCOPE: AGG-01 ONLY
FULL_ENGINE_REVIEW_AUTHORIZED: NO
FOUNDATION_MODIFICATION_AUTHORIZED: NO
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
CODE_MODIFICATION_AUTHORIZED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## 1. Obiettivo unico

Verificare indipendentemente la correzione `AGG-01` prodotta da Codex.

Leggere:

```text
results/model_spec_c2/foundation_revision/
CODEX_C2_AGG_01_FINGERPRINT_CORRECTION.md

results/model_spec_c2/foundation_revision/
CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md
```

Non riaprire clock, biologia, specie, FEED/CARE, fertilizer, inventory, serviceability, replay o MODEL_SPEC.

L'unica domanda Ã¨:

```text
La procedura canonica pubblicata da Codex riproduce realmente
il fingerprint aggregato dichiarato?
```

---

# 2. Fingerprint atteso

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

---

# 3. Procedura obbligatoria

Dalla root:

```text
C:\Users\pietr\Projects\kaggriculture-agent
```

eseguire **esattamente** il comando canonico pubblicato da Codex nel report di correzione.

Non reinterpretare la formula.

Non riscrivere il manifest prima del primo tentativo.

Registrare:

```text
COMMAND_EXECUTED:
WORKING_DIRECTORY:
STDOUT:
EXIT_CODE:
OBSERVED_AGGREGATE_SHA256:
EXPECTED_AGGREGATE_SHA256:
MATCH:
```

---

# 4. Controllo payload

Se `MATCH: YES`, verificare inoltre:

```text
PAYLOAD_LENGTH: 702
FILE_COUNT: 5
TEXT_ENCODING: UTF-8
BOM: NO
RECORD_SEPARATOR: LF
TRAILING_NEWLINE: NO
PATH_SEPARATOR: /
SORT: case-sensitive ascending normalized relative path
HASH_HEX: lowercase
```

e verificare che i cinque singoli SHA-256 coincidano con quelli pubblicati.

---

# 5. In caso di mismatch

Se il comando canonico NON restituisce l'hash atteso:

1. non limitarsi a dichiarare un nuovo digest;
2. salvare/stampare il manifest effettivo;
3. riportare la lunghezza esatta del payload;
4. riportare `repr(payload)` o equivalente non ambiguo;
5. riportare i cinque hash individuali;
6. identificare la prima differenza rispetto al payload canonico Codex;
7. distinguere:
   - file content mismatch;
   - working-directory mismatch;
   - path mismatch;
   - sort mismatch;
   - separator/newline mismatch;
   - encoding/BOM mismatch;
   - altro.

Non riaprire l'Engine Contract semantico.

---

# 6. Output

Creare:

```text
results/model_spec_c2/foundation_revision/
COPILOT_C2_AGG_01_REVERIFICATION.md
```

Contenuto minimo:

1. Scope.
2. Command executed.
3. Runtime/working directory.
4. Individual file hash result.
5. Manifest/payload verification.
6. Observed aggregate.
7. Comparison with expected aggregate.
8. AGG-01 final verdict.

---

# 7. Chiusura obbligatoria

```text
REVIEWER: COPILOT

CANONICAL_COMMAND_EXECUTED: YES/NO
INDIVIDUAL_FILE_HASHES_MATCH: YES/NO
CANONICAL_PAYLOAD_MATCH: YES/NO
PAYLOAD_LENGTH_702: YES/NO

EXPECTED_AGGREGATE_SHA256:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

OBSERVED_AGGREGATE_SHA256:
<sha256>

AGGREGATE_MATCH: YES/NO

SEMANTIC_CONTENT_REVIEWED_AGAIN: NO
NEW_SEMANTIC_FINDINGS: 0

AGG_01_STATUS: RESOLVED/UNRESOLVED
ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED: YES/NO
ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE: YES/NO

FOUNDATION_MODIFIED: NO
MODEL_SPEC_MODIFIED: NO
CODE_MODIFIED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

Regola:

```text
if AGGREGATE_MATCH == YES:
    AGG_01_STATUS = RESOLVED
    ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED = YES
    ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE = YES
else:
    AGG_01_STATUS = UNRESOLVED
    ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED = NO
    ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE = NO
```

```text
NEXT_ACTION_IF_PASS:
FINAL ENGINE CONTRACT RECONCILIATION + FREEZE
```
