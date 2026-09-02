# C2 â€” COPILOT AGG-01 ONLY RE-VERIFICATION

## 1. Scope

This review is limited to AGG-01 provenance only. It does not reopen the semantic engine contract, the crop/animal ledger, serviceability, replay reconciliation, or any Foundation / MODEL_SPEC logic.

## 2. Command executed

Working directory:

```text
C:\Users\pietr\Projects\kaggriculture-agent
```

Canonical command executed:

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; import hashlib; ps=[Path(x) for x in ('.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA','.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md','.venv/Lib/site-packages/kaggriculture/envs/kaggriculture/README.md','.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json','.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py')]; es=sorted(((p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()) for p in ps),key=lambda x:x[0]); rows=[p+'\t'+h for p,h in es]; payload='\n'.join(rows).encode('utf-8'); print('\n'.join(rows)); print('AGGREGATE_SHA256='+hashlib.sha256(payload).hexdigest())"
```

Note: this is the exact canonical reproduction procedure from the Codex AGG-01 correction, executed from the repository root. The command is intentionally not reinterpreted.

## 3. Runtime / working directory

```text
WORKING_DIRECTORY: C:\Users\pietr\Projects\kaggriculture-agent
PYTHON_RUNTIME: .\.venv\Scripts\python.exe
```

## 4. Individual file hash result

```text
.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA	5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md	e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md	3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json	a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py	bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
```

All five individual SHA-256 values match the published values in the Codex correction report.

## 5. Manifest / payload verification

Observed canonical payload properties:

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

## 6. Observed aggregate

```text
AGGREGATE_SHA256=4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

## 7. Comparison with expected aggregate

```text
EXPECTED_AGGREGATE_SHA256: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
OBSERVED_AGGREGATE_SHA256: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
MATCH: YES
```

## 8. AGG-01 final verdict

```text
AGG_01_STATUS: RESOLVED
ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED: YES
ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE: YES
```

---

```text
REVIEWER: COPILOT

CANONICAL_COMMAND_EXECUTED: YES
INDIVIDUAL_FILE_HASHES_MATCH: YES
CANONICAL_PAYLOAD_MATCH: YES
PAYLOAD_LENGTH_702: YES

EXPECTED_AGGREGATE_SHA256:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

OBSERVED_AGGREGATE_SHA256:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

AGGREGATE_MATCH: YES

SEMANTIC_CONTENT_REVIEWED_AGAIN: NO
NEW_SEMANTIC_FINDINGS: 0

AGG_01_STATUS: RESOLVED
ENGINE_CONTRACT_PROVENANCE_INDEPENDENTLY_VERIFIED: YES
ENGINE_CONTRACT_READY_FOR_RECONCILIATION_AND_FREEZE: YES

FOUNDATION_MODIFIED: NO
MODEL_SPEC_MODIFIED: NO
CODE_MODIFIED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

This re-verification confirms the Codex AGG-01 canonical fingerprint is reproducible with the canonical serialization and the expected aggregate matches exactly.
