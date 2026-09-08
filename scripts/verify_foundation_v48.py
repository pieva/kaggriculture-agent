"""Verify current checkpoint without running simulations or changing evidence."""
import hashlib
import json
import re
from pathlib import Path

root=Path(__file__).resolve().parents[1]
b=root/'docs/model_specs/codex/e19'
m=json.loads((b/'artifacts/derived/v48_external_manifest.json').read_text(encoding='utf-8'))
assert hashlib.sha256((root/m['output']).read_bytes()).hexdigest()==m['sha256']
assert len(m['sources'])==18 and m['validation']['frozen_sides_equal']
for p,h in m['sources'].items():
    assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h,p
foundation=root/'docs/foundation'
s=(foundation/'FOUNDATION_C2_1_MANIFEST.md').read_text(encoding='utf-8')
for p,h in re.findall(r'`([^`]+\.md)` \| `([A-F0-9]{64})`',s):
    assert hashlib.sha256((foundation/p).read_bytes()).hexdigest().upper()==h,p
local=json.loads((foundation/'evidence/LOCAL_ARTIFACTS_20260908.json').read_text(encoding='utf-8'))
for row in local:
    p=root/row['path']
    assert p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],p
for p in [foundation/'V48_PLANNING_AND_BUILD_IT.md',foundation/'FOUNDATION_C2_1_MANIFEST.md']:
    assert '\ufffd' not in p.read_text(encoding='utf-8')
print('Verified: 18 bundle sources, publication hash, foundation hashes,',len(local),'local artifacts.')
