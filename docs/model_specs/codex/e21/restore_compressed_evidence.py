"""Restore ignored large JSON evidence from verified tracked gzip archives."""
from pathlib import Path
import json,gzip,hashlib
ROOT=Path(__file__).resolve().parents[4]
for row in json.loads(Path(__file__).with_name('COMPRESSED_EVIDENCE.json').read_text(encoding='utf-8')):
    target=(ROOT/row['path']).resolve();archive=(ROOT/row['archive']).resolve()
    assert target.is_relative_to(ROOT) and archive.is_relative_to(ROOT)
    raw=gzip.decompress(archive.read_bytes())
    assert hashlib.sha256(raw).hexdigest()==row['sha256']
    if target.exists():assert target.read_bytes()==raw
    else:target.write_bytes(raw)
print('Evidence restored and hashes verified.')
