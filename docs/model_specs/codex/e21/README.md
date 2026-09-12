# E21 — historical experiments and external comparisons

The common-calendar development derived from 772 is now maintained under
[E20.8](../e20/E20_8_RELEASE.md). E21 Repair2 and earlier experiments remain
here as immutable provenance. Current E20 reports include the 22 KPIs, sales
and market prices.

Large raw JSON evidence is tracked as deterministic `.json.gz` files.
`COMPRESSED_EVIDENCE.json` records original paths, sizes and SHA256 values.
Run `.venv/Scripts/python.exe docs/model_specs/codex/e21/restore_compressed_evidence.py`
from the repository root to restore the ignored original files before rerunning
historical analysis scripts that read them. Existing files are verified, never
overwritten. Compression preserves the original bytes and source hashes.

Temporary execution logs and the `outputs/` dependency workspace are local;
reports, code, result tables, workbook deliverables and compressed replay
evidence remain versioned.
