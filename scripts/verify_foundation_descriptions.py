"""Verify document links, source provenance and retained technical catalogs."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'docs/foundation'
A=ROOT/'docs/governance/history/foundation_documentation_20260908'
records=json.loads((A/'manifest.json').read_text(encoding='utf-8'))
for record in records:
    assert hashlib.sha256((ROOT/record['archive']).read_bytes()).hexdigest()==record['sha256'],record['archive']
active=[F/'README.md',F/'ENGINE_CONTRACT.md',F/'FOUNDATION_C2_1_MANIFEST.md',
 F/'ontology/ONTOLOGY_C2_1.md',F/'state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md',
 F/'feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md',F/'feature_model/FEATURE_CATALOG.md',
 F/'V48_PLANNING_AND_BUILD_IT.md',ROOT/'docs/model_specs/codex/e19/MODEL_SPEC_CODEX_770_V48.md']
for p in active:
    s=p.read_text(encoding='utf-8')
    assert '\ufffd' not in s,p
    for link in re.findall(r'\]\(([^)]+)\)',s):
        if link.startswith(('https:','http:','#')):continue
        target=(p.parent/link.split('#')[0]).resolve()
        assert target.exists(),(str(p),link)
for rel in ['ontology/ONTOLOGY_C2_1.md','feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md']:
    old=(A/rel).read_text(encoding='utf-8')
    new=(F/rel).read_text(encoding='utf-8')
    if rel.startswith('ontology'):
        pattern=r'^### `([^`]+)`'
        assert set(re.findall(pattern,old,re.M))<=set(re.findall(pattern,new,re.M))
    else:
        new+=(F/'feature_model/FEATURE_CATALOG.md').read_text(encoding='utf-8')
        pattern=r'^\| \*\*([^*]+)\*\* \|'
        # The first technical catalog ends at the next horizontal separator.
        old=old[old.index('| feature_id |'):]
        old=old[:old.index('\n---')]
        assert set(re.findall(pattern,old,re.M))<=set(re.findall(pattern,new,re.M))
engine=ROOT/'.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture'
sources=json.loads((F/'ENGINE_SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
for name,h in sources['files'].items():
    assert hashlib.sha256((engine/name).read_bytes()).hexdigest()==h
manifest=(F/'FOUNDATION_C2_1_MANIFEST.md').read_text(encoding='utf-8')
for rel,h in re.findall(r'`([^`]+\.md)` \| `([A-F0-9]{64})`',manifest):
    assert hashlib.sha256((F/rel).read_bytes()).hexdigest().upper()==h
print('Verified:',len(records),'archived originals;',len(active),'documents; retained concept/feature IDs; engine and document hashes.')
