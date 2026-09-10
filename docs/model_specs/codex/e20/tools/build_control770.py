"""Freeze an explicit topology ablation with the identical E20.1 scheduler."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'

def build():
    parent=ROOT/'submission/submission_codex_e20_772_e20v28_candidate.py'
    protocol=json.loads((BASE/'E20_1_PROTOCOL.json').read_text())
    assert hashlib.sha256(parent.read_bytes()).hexdigest()==protocol['frozen_for_role_swap']['sha256']
    out=ROOT/'submission/submission_codex_e20_1_control_770.py'
    assert not out.exists()
    source='import sys\nimport types\nfrom dataclasses import replace\n_PARENT_SOURCE='+repr(parent.read_text(encoding='utf-8'))+'''
MODEL_VERSION='CODEX-E20.1-CONTROL-770'
def create_agent(run_context=None):
    module=types.ModuleType('_e20_control770')
    module.__file__='/bundle/docs/model_specs/codex/e20/control770.py'
    sys.modules[module.__name__]=module
    exec(compile(_PARENT_SOURCE,module.__file__,'exec'),module.__dict__)
    cfg=module.VARIANTS[module.SELECTED_VARIANT]
    cfg['positions']=()
    cfg['species']=()
    policy=module.create_agent(run_context)
    policy.core.profile=replace(policy.core.profile,target=14)
    return policy
_ACTIVE={}
def agent(observation,configuration=None):
    configuration=configuration or {}
    seat=int(observation.get('player',0))
    step=observation['day']*configuration.get('turnsPerDay',24)+observation['hour']
    previous=_ACTIVE.get(seat)
    policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
'''
    compile(source,str(out),'exec');out.write_text(source,encoding='utf-8')
    manifest=dict(status='RESEARCH_TOPOLOGY_CONTROL_NOT_PROMOTED',topology=[7,7,0],
        parent_sha256=hashlib.sha256(parent.read_bytes()).hexdigest(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        changes='No Q2 reservations or animals, target 14, mix 9 cows / 5 sheep; same remote-first routes and zero-gain CARE filter',uploaded=False)
    out.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(out)

if __name__=='__main__':build()
