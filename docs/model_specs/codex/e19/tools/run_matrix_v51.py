"""Open the next partition only after the preceding economic/biological gates."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import hashlib,json,sys
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.run_pass_reduction_v51 import run,OUT
from docs.model_specs.codex.e19.tools.analyze_pass_reduction_v51 import analyze

def one(case):
    v,s,seat,split=case
    if (OUT/f'{split}_{v}_{s}_{seat}.json').exists():return
    run(v,s,seat,split,False)

if __name__=='__main__':
    stage=sys.argv[1];assert stage in {'development','validation'}
    report=analyze('v51c');dev=report['partitions']['development']
    assert all(dev['gates'].values()),dev['gates']
    if stage=='development':
        assert dev['n']>=3
        cases=[('v51c',s,1,'development') for s in [180903001,180903002,180903003]]
    else:
        assert dev['n']==6
        manifest=json.loads((OUT/'candidate_manifest.json').read_text())
        assert hashlib.sha256((ROOT/manifest['output']).read_bytes()).hexdigest()==manifest['sha256']
        for p,h in manifest['sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
        parity=json.loads((OUT/'parity_v51c_180903003_0.json').read_text())
        assert parity['mismatches']==0 and parity['bundle_sha256']==manifest['sha256']
        opened=OUT/'validation_opened.json'
        if not opened.exists():opened.write_text(json.dumps(dict(opened_at=datetime.now(timezone.utc).isoformat(),seeds=[260909201,260909202],seats=[0,1],bundle_sha256=manifest['sha256'],development_gate_passed=True),indent=2))
        cases=[(v,s,seat,'validation') for s in [260909201,260909202] for seat in [0,1] for v in ['v49f','v51c']]
    with ProcessPoolExecutor(max_workers=2) as pool:list(pool.map(one,cases))
