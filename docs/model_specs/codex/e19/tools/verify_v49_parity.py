"""Action-by-action source/bundle parity on immutable candidate trajectories."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))


def verify(path):
    metadata=json.loads(path.read_text())
    variant=metadata['variant']
    import importlib
    module=importlib.import_module('docs.model_specs.codex.e19.tools.policy_770_'+variant)
    install=module.install
    raw=ROOT/metadata['details']
    replay=json.load(gzip.open(raw,'rt',encoding='utf-8'))['replay']
    seat=metadata['seat']
    source=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'))['create_agent']({'player_position':seat})
    install(source.core)
    if hasattr(module,'adapt'):source=module.adapt(source)
    standalone=runpy.run_path(str(ROOT/f'submission/submission_codex_e19_770_{variant}_candidate.py'))
    times=[]
    for i in range(1,len(replay['steps'])):
        obs=deepcopy(replay['steps'][i-1][seat]['observation'])
        obs.update(player=seat,step=i-1)
        start=time.perf_counter()
        actual=standalone['agent'](deepcopy(obs),replay['configuration'])
        times.append(time.perf_counter()-start)
        expected=source(obs,replay['configuration'])
        assert actual==expected==replay['steps'][i][seat]['action'],(path.name,i)
    manifest_name={'v49':'candidate_manifest.json','v49b':'candidate_b_manifest.json','v49c':'candidate_c_manifest.json','v49d':'candidate_d_manifest.json','v49f':'candidate_f_manifest.json'}[variant]
    manifest=json.loads((path.parent/manifest_name).read_text())
    frozen=json.loads((ROOT/'docs/model_specs/codex/e19/artifacts/derived/v48_external_manifest.json').read_text())
    for entry in [manifest,frozen]:
        for p,sha in entry['sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
        assert hashlib.sha256((ROOT/entry['output']).read_bytes()).hexdigest()==entry['sha256']
    result=dict(input=path.name,seat=seat,seed=metadata['seed'],actions=719,mismatches=0,
        bundle_sha256=manifest['sha256'],frozen_v48_intact=True,
        runtime_note='Offline, no instrumentation; may overlap other processes. First call includes loading policy.',
        max_seconds=max(times),overage=sum(max(0,t-1) for t in times))
    (path.parent/f'parity_{variant}_{metadata["seed"]}_{seat}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)


if __name__=='__main__':verify(Path(sys.argv[1]))
