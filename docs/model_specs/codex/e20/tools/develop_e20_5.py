"""Single livestock-mix intervention, frozen E20.2 controls, serial runs."""
import gzip,hashlib,json,sys
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools import run_experiment as runner
BASE=ROOT/'docs/model_specs/codex/e20';STAGE='e20_5_observed_demand'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def replay(p):
    with gzip.open(p.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
    assert hashlib.sha256(raw).hexdigest()==read(p)['replay_sha256'];return json.loads(raw)
def canonical(v):
    if isinstance(v,dict):return {k:canonical(x) for k,x in v.items() if k!='remainingOverageTime'}
    if isinstance(v,list):return [canonical(x) for x in v]
    return v
def main():
    protocol=read(BASE/'E20_5_PROTOCOL.json')
    for p,h in protocol['sources'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
    runner.BUNDLES.update({'E20.2':'submission_codex_e20_772_e20v32_candidate.py','E20.5':'submission_codex_e20_772_e20v36_candidate.py'})
    def policy(name,seat):
        p=ROOT/'submission'/runner.BUNDLES[name];ns={'__name__':'_mix_validation'}
        exec(compile(p.read_text(encoding='utf-8'),str(p),'exec'),ns)
        return ns['create_agent']({'player_position':seat})
    runner.policy=policy
    checks=[]
    for seed in protocol['development_seeds']:
        for seat in [0,1]:
            oldnames=['E20.2','E18'] if seat==0 else ['E18','E20.2']
            old=BASE/'artifacts/e20_2_confirmation'/f'{oldnames[0]}_{oldnames[1]}_{seed}.json'
            before=replay(old)
            # A complete fresh exact control in each seed; both old roles already valid.
            if seat==0:
                print(f'CONTROL {seed}',flush=True)
                control=read(BASE/'artifacts/e20_3_mix_development'/f'{oldnames[0]}_{oldnames[1]}_{seed}.json');assert all(x['calls']==719 for x in control['runtime'])
                p=BASE/'artifacts/e20_3_mix_development'/f'{oldnames[0]}_{oldnames[1]}_{seed}.json'
                assert canonical(replay(p)['steps'])==canonical(before['steps'])
            names=['E20.5','E18'] if seat==0 else ['E18','E20.5']
            print(f'CANDIDATE {seed} {seat}',flush=True)
            m=runner.run((STAGE,*names,seed));assert all(x['calls']==719 for x in m['runtime']) and m['runtime'][seat]['core_errors']==0
            p=BASE/'artifacts'/STAGE/f'{names[0]}_{names[1]}_{seed}.json';after=replay(p)
            assert canonical(after['steps'][:265])==canonical(before['steps'][:265])
            for step in after['steps']:
                counts=[0]*4
                for y,row in enumerate(step[seat]['observation']['farms'][seat]['tiles']):
                    for x,t in enumerate(row):
                        if isinstance(t,dict) and t.get('kind')=='PASTURE':counts[(x>=5)+2*(y>=5)]+=1
                assert all(n<=cap for n,cap in zip(counts,[7,7,2,0]))
            assert counts==[7,7,2,0]
            checks.append(dict(seed=seed,seat=seat,prefix_states=265,cash=m['rewards'][seat],margin=m['rewards'][seat]-m['rewards'][1-seat],delta_cash=m['rewards'][seat]-read(old)['rewards'][seat],baseline=str(old.relative_to(ROOT))))
    from docs.model_specs.codex.e20.tools.audit_results import run as audit
    for p in (BASE/'artifacts'/STAGE).glob('*.json'):
        if not p.name.endswith('.kpi.json'):audit(str(p))
    out=BASE/'reports'/STAGE;out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(dict(variant='E20v36',cases=checks,adopted=False,uploaded=False),indent=2)+'\n',encoding='utf-8')
    print('FINAL '+json.dumps(checks),flush=True)
if __name__=='__main__':main()
