import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
def main():
    base=ROOT/'submission/submission_codex_e19_770_v51_candidate.py'
    s=base.read_text(encoding='utf-8').split("MODEL_VERSION='CODEX-E19-770-V51-CANDIDATE'")[0]
    overlay=(HERE/'workforce_v52c.py').read_text(encoding='utf-8')
    s+='\n_V52={}\nexec('+repr(overlay)+',_V52)\n'
    s+='''
MODEL_VERSION='CODEX-E19.2-770-V52C-OBSERVED-WORKFORCE'
def create_agent(run_context=None):
    policy=_base.create_agent(run_context)
    _sys.modules['_v51pkg.policy_770_v51'].install(policy.core)
    _V52['install'](policy.core)
    return _sys.modules['_v51pkg.policy_770_v51'].adapt(policy)
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
    p=ROOT/'submission/archive/e19_rejected/submission_codex_e19_2_770_v52c.py';compile(s,str(p),'exec');p.write_text(s,encoding='utf-8')
    (HERE/'MANIFEST_V52C.json').write_text(json.dumps(dict(file=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),parent_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),status='experimental, not submitted',change='D12-D29 nominal maximum 11 instead of12; restore12 on observed animal/crop stress. Existing adaptive hiring may use fewer; D30 unchanged.'),indent=2),encoding='utf-8')
if __name__=='__main__':main()
