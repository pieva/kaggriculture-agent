"""Frozen F: finish development, check scope, then open preregistered seeds."""
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.run_v49_matrix import one
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909'


def run_cases(cases):
    with ProcessPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,cases))
    assert all(x is not False for x in results),'Incomplete matrix'


if __name__=='__main__':
    run_cases([('v49f',s,t,'development') for s in range(180903001,180903004) for t in (0,1) if (s,t)!=(180903003,0)])
    for seed in range(180903001,180903004):
        for seat in (0,1):
            a=json.loads((OUT/f'development_v48_{seed}_{seat}.json').read_text())
            b=json.loads((OUT/f'development_v49f_{seed}_{seat}.json').read_text())
            assert b['reward']>=a['reward'],(seed,seat,'cash')
            assert sum(d['pass_count'] for d in b['daily'])<sum(d['pass_count'] for d in a['daily'])
            assert sum(d['move'] for d in b['daily'])<=sum(d['move'] for d in a['daily'])
    manifest=json.loads((OUT/'candidate_f_manifest.json').read_text())
    for p,sha in manifest['sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha
    (OUT/'validation_opened.json').write_text(json.dumps(dict(
        utc=datetime.now(timezone.utc).isoformat(),candidate_sha256=manifest['sha256'],
        seeds=[260909101,260909102],seats=[0,1],opponent='V4D exposed internal control',
        policy_frozen=True,no_validation_based_edits=True),indent=2))
    print('OPENING PREREGISTERED VALIDATION',flush=True)
    run_cases([(v,s,t,'validation') for s in [260909101,260909102] for t in (0,1) for v in ['v48','v49f']])
