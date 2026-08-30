# C2 â€” Codex AGG-01 Fingerprint Provenance Correction

```text
AGENT: CODEX
PHASE: REVIEW / RECONCILIATION FIX
TASK_ID: C2-ENGINE-CONTRACT-AGG-01-FINGERPRINT-FIX
SCOPE: PROVENANCE CORRECTION ONLY
CORRECTION_DATE: 2026-08-31
```

## 1. Issue statement

La review Copilot ha contestato la riproducibilitÃ  del fingerprint aggregato dichiarato in `CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`. Il report Codex riportava `4378b60fâ€¦`; Copilot ha riportato `1c58e32fâ€¦` applicando, secondo la review, la formula pubblicata allo stesso manifest.

Il rilievo Ã¨ `AGG-01`, severitÃ  `P3`, limitato a provenance/riproducibilitÃ . Questa correzione non riapre clock, biologia, inventory, serviceability, replay o policy distinction.

## 2. Old reported aggregate

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

La formula originariamente pubblicata era:

```text
sha256(UTF8(join("\n", sort(relative_path + "\t" + file_sha256))))
```

La formula indicava gli elementi essenziali, ma lasciava impliciti root, path normalization, collation/case sensitivity del sort, BOM e trailing newline.

## 3. Copilot reproduced aggregate

```text
1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d
```

Questo valore Ã¨ trattato come digest esterno riportato dalla review. Non Ã¨ stato assunto corretto nÃ© usato per scegliere la canonicalizzazione.

## 4. Individual-file hash verification

Tutti gli hash sono stati ricalcolati sui raw bytes con SHA-256.

| PATH | AUDIT_REPORTED_SHA256 | RECOMPUTED_SHA256 | MATCH |
|---|---|---|---:|
| `.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA` | `5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add` | `5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add` | YES |
| `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md` | `e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22` | `e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22` | YES |
| `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md` | `3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00` | `3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00` | YES |
| `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json` | `a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867` | `a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867` | YES |
| `.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py` | `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e` | `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e` | YES |

PoichÃ© tutti i singoli file coincidono, la divergenza riguarda esclusivamente la serializzazione/aggregazione del manifest, non il contenuto engine.

## 5. Exact old aggregation reconstruction

Usando path esattamente come pubblicati, slash `/`, hash lowercase, ordinamento lessicografico Unicode case-sensitive, tab tra path e digest, LF tra record, UTF-8 senza BOM e nessun LF finale, il payload Ã¨ lungo esattamente 702 byte.

Il suo SHA-256 Ã¨:

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

Quindi il vecchio digest Codex Ã¨ riprodotto. Non deriva da un file diverso nÃ© da text-mode hashing dei file engine.

Varianti di controllo:

| Serialization variant | Aggregate SHA-256 |
|---|---|
| case-sensitive, LF, no trailing newline | `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d` |
| case-sensitive, LF, trailing LF | `163a10e34c0263048bee7fccebda1103adef89cd78de25c73d78ddb9d114e4ac` |
| case-sensitive, CRLF, no trailing newline | `66638dfcc953c031b6805951298dfd12a043affab040901ec480392d674d5c3e` |
| case-sensitive, CRLF, trailing CRLF | `3545c04aa37b8201e9a0fadd0c201d0f7e87cba7a9595576844149de3ce61bd0` |
| case-insensitive path sort, LF, no trailing newline | `a4bc52b053a3f21c2f022ef8d5161051abbe514604555f3b32f746525824f354` |
| case-insensitive path sort, LF, trailing LF | `39510982f9464459ae7c1ff0f7e0eec5f18de8548edd3c7c2539623f8683d985` |

La differenza fra case-sensitive e case-insensitive Ã¨ concreta: con case-sensitive `README.md` precede `kaggriculture.*`; con case-insensitive segue quei file.

## 6. Exact Copilot aggregation reconstruction

Il digest Copilot non Ã¨ riproducibile dagli input canonici disponibili.

Sono state testate meccanicamente:

- tutte le 120 permutazioni dei cinque record con LF, CRLF, blank-line separator, concatenazione senza separatore e trailing separator sÃ¬/no;
- 1.587.600 combinazioni comuni di order, root/path form, slash/backslash, path case, hash hex case, field separator, record separator, prefix/suffix, BOM, UTF-8/UTF-16 e trailing newline;
- concatenazione dei raw file bytes, dei soli hash, dei soli path e serializzazioni JSON/repr comuni.

Nessuna produce:

```text
1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d
```

Un SHA-256 Ã¨ one-way: dal solo digest non Ã¨ possibile ricostruire quale byte sequence aggiuntiva o differente sia stata usata. Il valore Copilot richiede quindi almeno un input, ordine o framing non riportato, oppure un errore di trascrizione/calcolo. Ãˆ classificato `UNVERIFIED_EXTERNAL_DIGEST`, non come seconda interpretazione valida del manifest pubblicato.

## 7. Root cause

La root cause normativa di `AGG-01` Ã¨ l'underspecification della serializzazione nel report originale: `sort(...)` non dichiarava collation/case sensitivity e mancavano dichiarazioni esplicite su path root, separator normalization, trailing newline e BOM. CiÃ² rendeva possibile a reviewer differenti costruire payload diversi pur ritenendo di seguire la stessa descrizione.

La root cause osservabile del valore `1c58â€¦` Ã¨ piÃ¹ stretta: esso Ã¨ stato calcolato su bytes diversi dal manifest dichiarato/canonico, ma la trasformazione esatta non Ã¨ presente negli input autorizzati e non Ã¨ inferibile dal digest. Nessuna delle differenze candidate elencate nel prompt lo riproduce.

La risoluzione consiste nel congelare una serializzazione unica, pubblicare il payload esatto e fornire un comando eseguibile. Non Ã¨ necessario cambiare il digest `4378â€¦`.

## 8. Canonical aggregation specification

```text
PATH_ROOT: C:/Users/pietr/Projects/kaggriculture-agent
PATH_ROOT_SEMANTICS: repository worktree root; command executed from this root
PATH_SEPARATOR: /
PATH_CASE: preserved exactly as listed
SORT_ORDER: ascending by normalized relative path,
            Unicode code-point order, case-sensitive
FILE_READ_MODE: binary / raw bytes
FILE_HASH_ALGORITHM: SHA-256
HASH_HEX_CASE: lower
RECORD: normalized_relative_path + HTAB (0x09) + lowercase_file_sha256
TEXT_ENCODING: UTF-8
BOM: NO
LINE_SEPARATOR_BETWEEN_RECORDS: LF (0x0A)
TRAILING_NEWLINE: NO
PAYLOAD_LENGTH: 702 bytes
AGGREGATE_ALGORITHM: SHA-256 over the 702 serialized payload bytes
```

Questa procedura differisce dall'originale soltanto per grado di esplicitazione. Il payload e il digest risultante coincidono con quelli effettivamente usati dal vecchio valore Codex.

## 9. Canonical manifest

Le cinque righe seguenti sono l'intero payload testuale. I separatori visivi tra path e hash sono tab reali. La fence e il newline dopo l'ultima riga non appartengono al payload.

```text
.venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA	5621f9e36c001c9d1a5fa7832cb46551cb480ad00a2005b2e4539554a7ba8add
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md	e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md	3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json	a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867
.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py	bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
```

## 10. New canonical aggregate

```text
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

Il new canonical aggregate coincide con l'old reported aggregate. La correzione riguarda la riproducibilitÃ  della procedura, non il risultato o i file sorgente.

## 11. Independent reproduction command

Eseguire dalla repository root in PowerShell. Il comando legge ogni file in binary mode tramite `Path.read_bytes()`, stampa il manifest esatto e poi l'aggregate.

```powershell
.\.venv\Scripts\python.exe -c 'from pathlib import Path; import hashlib; ps=[Path(x) for x in (".venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py")]; es=sorted(((p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()) for p in ps),key=lambda x:x[0]); rows=[p+"\t"+h for p,h in es]; payload="\n".join(rows).encode("utf-8"); print("\n".join(rows)); print("AGGREGATE_SHA256="+hashlib.sha256(payload).hexdigest())'
```

Output finale atteso:

```text
AGGREGATE_SHA256=4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

## 12. Exact changes made to the Codex audit

Ãˆ stata modificata esclusivamente la sezione 2 di `CODEX_C2_ENGINE_CONTRACT_PERIOD_LEDGER_AUDIT.md`:

1. sostituito il pseudocodice ambiguo con la specifica completa di root, slash, path case, sort, raw-byte file hashing, record format, encoding, BOM, separator e trailing newline;
2. dichiarata la lunghezza del payload, 702 byte;
3. chiarito che fence e newline di rendering non fanno parte del payload;
4. aggiunto il comando PowerShell di riproduzione indipendente;
5. registrato l'esito `AGG-01` e il riferimento a questo report.

Non Ã¨ stato cambiato il fingerprint aggregato, perchÃ© la procedura canonica riproduce quello giÃ  pubblicato.

## 13. Semantic content confirmation

```text
SEMANTIC_CONTENT_CHANGED: NO
```

Non sono stati modificati:

- clock o action-transition semantics;
- species inventory;
- crop o animal ledger;
- FEED/CARE o fertilizer semantics;
- inventory semantics;
- serviceability/capacity;
- discrepancy semantiche;
- replay reconciliation;
- policy/engine distinction;
- final authorization dei downstream stage.

Foundation, MODEL_SPEC, codice, configurazioni e file engine non sono stati modificati.

## 14. Final AGG-01 verdict

`AGG_01_REPRODUCED: YES` indica che il rilievo di riproducibilitÃ  Ã¨ stato rieseguito e diagnosticato; i due campi successivi distinguono chiaramente quale digest sia stato riprodotto.

```text
AGG_01_REPRODUCED: YES
OLD_CODEX_HASH_REPRODUCED: YES
COPILOT_HASH_REPRODUCED: NO

ROOT_CAUSE:
The old audit underspecified manifest serialization (root, path normalization,
case-sensitive sort, BOM and trailing newline). The Copilot digest was computed
over an additional or different byte sequence not disclosed in the authorized
inputs and is not reproducible from the declared manifest; the exact hidden
transformation cannot be recovered from a one-way digest.

OLD_REPORTED_HASH:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

COPILOT_REPORTED_HASH:
1c58e32f8e156f9049c7a14aefe54d8fb244c4bc5441d95b491432f21886a13d

NEW_CANONICAL_HASH:
4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d

CANONICAL_REPRODUCTION_COMMAND:
.\.venv\Scripts\python.exe -c 'from pathlib import Path; import hashlib; ps=[Path(x) for x in (".venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info/METADATA",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/AGENTS.md",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/README.md",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.json",".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py")]; es=sorted(((p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()) for p in ps),key=lambda x:x[0]); rows=[p+"\t"+h for p,h in es]; payload="\n".join(rows).encode("utf-8"); print("\n".join(rows)); print("AGGREGATE_SHA256="+hashlib.sha256(payload).hexdigest())'

AUDIT_DOCUMENT_CORRECTED: YES
SEMANTIC_CONTENT_CHANGED: NO

AGG_01_STATUS: RESOLVED
ENGINE_CONTRACT_PROVENANCE_READY_FOR_REVIEW: YES

FOUNDATION_MODIFIED: NO
MODEL_SPEC_MODIFIED: NO
CODE_MODIFIED: NO
BUILD_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

```text
NEXT_ACTION_IF_PASS:
COPILOT AGG-01 ONLY RE-VERIFICATION
```
