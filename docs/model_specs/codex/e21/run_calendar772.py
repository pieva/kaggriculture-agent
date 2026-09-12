"""Serial technical gate followed by paired exposed-seed diagnostics."""
import json,hashlib,sys,gzip
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.calendar772_policy import create_agent
from docs.model_specs.codex.e20.tools import run_experiment as runner
from docs.model_specs.codex.e20.tools.audit_results import run as audit

def main():
    import runpy
    runner.BASE=BASE
    def factory(name,seat):
        if name=='Calendar772':return create_agent({'player_position':seat})
        if name=='Base772':return runpy.run_path(str(ROOT/'submission/submission_codex_e20_772_e20v28_loaderfix.py'))['create_agent']({'player_position':seat})
        return runpy.run_path(str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'))['create_agent']({'player_position':seat})
    runner.policy=factory
    stage='calendar772_c1';out=BASE/'reports'/stage;out.mkdir(parents=True,exist_ok=True)
    sources=[BASE/'calendar772_policy.py',Path(__file__),ROOT/'submission/submission_codex_e20_772_e20v28_loaderfix.py',ROOT/'submission/submission_codex_e18_770_v48_external.py',ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v48.py']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    protocol=dict(identity='CALENDAR772-C1',status='FROZEN_DEVELOPMENT',scope='Published E20.1 loaderfix 772; retain opening, dispatcher and 10C6S. Change biological calendar intentions to 33 strawberries, wheat succession and final carrots.',seeds=[180911301,180911303],roles=[0,1],opponent='E18 frozen775',baseline='Base772 freshly run matching seed and role',economic_gate='Positive own-cash delta averaged roles on each seed; biological losses no worse each case',sources=hashes,stop='Stop on first technical failure of topology, animal mix, opening parity, calls or core errors. No economic tuning after first result.',reserved_seeds='180912401-407 remain unused')
    p=out/'PROTOCOL.json'
    if p.exists():
        original=json.loads(p.read_text())
        for source,digest in original['sources'].items():
            if source.endswith('run_calendar772.py'):continue
            assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==digest
    else:p.write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    outcomes=[]
    for seed in protocol['seeds']:
        for left,right in [('Calendar772','E18'),('E18','Calendar772')]:
            seat=0 if left=='Calendar772' else 1
            bleft,bright=('Base772','E18') if seat==0 else ('E18','Base772')
            baseline_meta=runner.run((stage,bleft,bright,seed))
            audit(BASE/f'artifacts/{stage}/{bleft}_{bright}_{seed}.json')
            meta=runner.run((stage,left,right,seed));path=BASE/f'artifacts/{stage}/{left}_{right}_{seed}.json'
            audit(path)
            kpi=json.loads(path.with_suffix('.kpi.json').read_text())['sides'][seat]
            with gzip.open(path.with_suffix('.replay.json.gz'),'rt',encoding='utf-8') as f:r=json.load(f)
            bpath=BASE/f'artifacts/{stage}/{bleft}_{bright}_{seed}.replay.json.gz'
            with gzip.open(bpath,'rt',encoding='utf-8') as f:b=json.load(f)
            prefix=all(r['steps'][i][seat]['action']==b['steps'][i][seat]['action'] for i in range(1,265))
            last=kpi['kpi'][-1];mix={k:last[k] for k in ['COW','SHEEP','GOOSE']}
            def geometry(replay):
                tiles=replay['steps'][-1][seat]['observation']['farms'][seat]['tiles']
                return {(x,y):(t.get('kind'),t.get('animal')) for y,row in enumerate(tiles) for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind') in ('PASTURE','COOP')}
            same_geometry=geometry(r)==geometry(b)
            passed=same_geometry and all(x['calls']==719 for x in baseline_meta['runtime']) and baseline_meta['runtime'][seat]['core_errors']==0 and prefix and meta['opening'][seat]['topology']==[7,7,2] and mix=={'COW':10,'SHEEP':6,'GOOSE':0} and meta['runtime'][seat]['calls']==719 and meta['runtime'][seat]['core_errors']==0
            row=dict(seed=seed,seat=seat,technical_pass=passed,geometry_equal=same_geometry,prefix_equal=prefix,mix=mix,topology=meta['opening'][seat]['topology'],cash=meta['rewards'][seat],baseline_cash=b['rewards'][seat],cash_delta=meta['rewards'][seat]-b['rewards'][seat],runtime=meta['runtime'][seat]);outcomes.append(row)
            (out/'RESULTS.json').write_text(json.dumps(outcomes,indent=2),encoding='utf-8');print('GATE',json.dumps(row),flush=True)
            if not passed:return
if __name__=='__main__':main()
