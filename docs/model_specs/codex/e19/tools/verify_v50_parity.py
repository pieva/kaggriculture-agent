"""Source, standalone and recorded-action equality on a complete replay."""
from copy import deepcopy
import gzip,hashlib,json,runpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.policy_770_v50 import install,adapt
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v50'


def main():
    path=Path(sys.argv[1]);metadata=json.loads(path.read_text());seat=metadata['seat']
    replay=json.load(gzip.open(ROOT/metadata['details'],'rt'))['replay']
    source=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'))['create_agent']({'player_position':seat})
    install(source.core);source=adapt(source)
    bundle=runpy.run_path(str(ROOT/'submission/submission_codex_e19_770_v50_candidate.py'))['agent']
    for i in range(1,720):
        obs=deepcopy(replay['steps'][i-1][seat]['observation']);obs.update(player=seat,step=i-1)
        assert bundle(deepcopy(obs),replay['configuration'])==source(obs,replay['configuration'])==replay['steps'][i][seat]['action'],i
    manifests=[OUT/'candidate_manifest.json',ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909/candidate_f_manifest.json',ROOT/'docs/model_specs/codex/e19/artifacts/derived/v48_external_manifest.json']
    for path in manifests:
        m=json.loads(path.read_text())
        assert hashlib.sha256((ROOT/m['output']).read_bytes()).hexdigest()==m['sha256']
        for p,sha in m['sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
    old=ROOT/f"scratch/v49/development_v49f_{metadata['seed']}_{seat}.json.gz"
    scope=None
    if metadata['split']=='development':
        baseline=json.load(gzip.open(old,'rt'))['replay']
        scope=all(replay['steps'][i][seat]['action']==baseline['steps'][i][seat]['action'] for i in range(1,673))
        assert scope
    result=dict(seed=metadata['seed'],seat=seat,actions=719,mismatches=0,
        bundle_sha256=json.loads((OUT/'candidate_manifest.json').read_text())['sha256'],
        d1_d28_parity=scope,frozen_v48_v49f_intact=True)
    (OUT/f'parity_v50j_{metadata["seed"]}_{seat}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
