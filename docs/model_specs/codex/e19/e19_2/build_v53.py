import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
def main():
    base=ROOT/'submission/submission_codex_e19_770_v51_candidate.py'
    assert hashlib.sha256(base.read_bytes()).hexdigest()=='43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda'
    s=base.read_text(encoding='utf-8').split("MODEL_VERSION='CODEX-E19-770-V51-CANDIDATE'")[0]
    s+='\n_FIX={}\nexec('+repr((HERE/'fixes_v53.py').read_text(encoding='utf-8'))+',_FIX)\n'
    s+='''
MODEL_VERSION='CODEX-E19.3-770-V53-FIXES'
def create_agent(run_context=None):
    policy=_base.create_agent(run_context)
    _sys.modules['_v51pkg.policy_770_v51'].install(policy.core)
    _FIX['install'](policy.core)
    return _FIX['FixedPolicy'](_sys.modules['_v51pkg.policy_770_v51'].adapt(policy))
_ACTIVE={}
def agent(observation,configuration=None):
    configuration=configuration or {}
    seat=int(observation.get('player',0));step=observation['day']*configuration.get('turnsPerDay',24)+observation['hour']
    previous=_ACTIVE.get(seat)
    policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
'''
    out=ROOT/'submission/archive/e19_rejected/submission_codex_e19_3_770_v53_fixes.py';compile(s,str(out),'exec');out.write_text(s,encoding='utf-8')
    (HERE/'MANIFEST_V53.json').write_text(json.dumps(dict(file=str(out.relative_to(ROOT)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),parent_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),status='internal validation, not submitted',fixes=['net same-batch grain round trips','urgent feeding separate from optional services','reserve accessible grain and delay growth for threatened animals','sell observed terminal stock']),indent=2),encoding='utf-8')
if __name__=='__main__':main()
