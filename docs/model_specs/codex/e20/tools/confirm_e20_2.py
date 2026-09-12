"""Frozen, serial three-model holdout; no tuning or submission."""
import gzip, hashlib, itertools, json, sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools import run_experiment as runner
BASE=ROOT/'docs/model_specs/codex/e20';STAGE='e20_2_confirmation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    protocol=read(BASE/'E20_2_CONFIRMATION_PROTOCOL.json')
    for p,h in protocol['sources'].items():assert sha(ROOT/p)==h,p
    runner.BUNDLES['E20.2']='submission_codex_e20_772_e20v32_candidate.py'
    def frozen_policy(name,seat):
        p=ROOT/'submission'/runner.BUNDLES[name]
        ns={'__name__':'_frozen_confirmation'}
        exec(compile(p.read_text(encoding='utf-8'),str(p),'exec'),ns)
        return ns['create_agent']({'player_position':seat})
    runner.policy=frozen_policy
    records=[]
    for seed in protocol['seeds']:
        for left,right in itertools.permutations(protocol['models'],2):
            print(f'START {seed} {left} {right}',flush=True)
            m=runner.run((STAGE,left,right,seed))
            assert all(r['calls']==719 for r in m['runtime'])
            for i,name in enumerate(m['agents']):
                if name!='E18':assert m['runtime'][i]['core_errors']==0
            p=BASE/'artifacts'/STAGE/f'{left}_{right}_{seed}.json'
            with gzip.open(p.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
            assert hashlib.sha256(raw).hexdigest()==m['replay_sha256']
            r=json.loads(raw);assert len(r['steps'])==720 and all(x['status']=='DONE' for x in r['steps'][-1])
            for i,name in enumerate(m['agents']):
                if name=='E20.2':
                    for step in r['steps']:
                        counts=[0]*4
                        for y,row in enumerate(step[i]['observation']['farms'][i]['tiles']):
                            for x,t in enumerate(row):
                                if isinstance(t,dict) and t.get('kind')=='PASTURE':counts[(x>=5)+2*(y>=5)]+=1
                        assert all(n<=cap for n,cap in zip(counts,[7,7,2,0]))
            records.append(m)
    assert len(records)==42
    from docs.model_specs.codex.e20.tools.audit_results import run as audit
    for m in records:
        p=BASE/'artifacts'/STAGE/f"{m['agents'][0]}_{m['agents'][1]}_{m['seed']}.json"
        audit(str(p));assert read(p.with_suffix('.kpi.json'))['replay_sha256']==m['replay_sha256']
    from docs.model_specs.codex.e20.tools.build_report import build
    build(STAGE)
    cases=[read(BASE/'artifacts'/STAGE/f"{m['agents'][0]}_{m['agents'][1]}_{m['seed']}.kpi.json") for m in records]
    comparisons={}
    for ref in ['E18','E19']:
        matches=[c for c in cases if {s['name'] for s in c['sides']}=={ref,'E20.2'}]
        deltas=[]
        for seed in protocol['seeds']:
            games=[c for c in matches if c['seed']==seed]
            deltas.append(mean(next(s['reward'] for s in c['sides'] if s['name']=='E20.2')-next(s['reward'] for s in c['sides'] if s['name']==ref) for c in games))
        bio={name:dict(stress=mean(len(s['crop_starvation']) for c in matches for s in c['sides'] if s['name']==name),losses=mean(len(s['ledger']['animal_escapes']) for c in matches for s in c['sides'] if s['name']==name)) for name in [ref,'E20.2']}
        passed=mean(deltas)>0 and sum(d>0 for d in deltas)>=5 and all(bio['E20.2'][k]<=bio[ref][k] for k in ['stress','losses'])
        comparisons[ref]=dict(seed_deltas=deltas,mean_margin=mean(deltas),positive_seeds=sum(d>0 for d in deltas),biology=bio,passed=passed)
    result=dict(candidate='E20.2',decision='ELIGIBLE_FOR_EXTERNAL_CHECK' if all(v['passed'] for v in comparisons.values()) else 'DO_NOT_SUBMIT_E20_2',comparisons=comparisons,uploaded=False,protocol_sha256=sha(BASE/'E20_2_CONFIRMATION_PROTOCOL.json'),matches=42)
    out=BASE/'reports'/STAGE
    (out/'DECISION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('FINAL '+json.dumps(result),flush=True)
if __name__=='__main__':main()
