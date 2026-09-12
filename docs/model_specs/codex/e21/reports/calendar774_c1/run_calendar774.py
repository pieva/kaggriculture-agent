"""Serial technical gate followed by paired exposed-seed diagnostics."""
import json,hashlib,sys,gzip
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.calendar774_policy import create_agent
from docs.model_specs.codex.e20.tools import run_experiment as runner
from docs.model_specs.codex.e20.tools.audit_results import run as audit

def main():
    import runpy
    runner.BASE=BASE
    def factory(name,seat):
        if name=='Calendar774':return create_agent({'player_position':seat})
        return runpy.run_path(str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'))['create_agent']({'player_position':seat})
    runner.policy=factory
    stage='calendar774_c1';out=BASE/'reports'/stage;out.mkdir(parents=True,exist_ok=True)
    sources=[BASE/'calendar774_policy.py',Path(__file__),ROOT/'submission/submission_codex_e21_774_repair2.py',ROOT/'submission/submission_codex_e18_770_v48_external.py',ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v48.py']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    protocol=dict(identity='E21-CALENDAR774-C1',status='FROZEN_DEVELOPMENT',scope='Maintain Repair2 774 geometry and 8C9S1G; transfer calendar AND existing V48 dispatcher from D12. Not pure calendar causality.',seeds=[180911301,180911303],roles=[0,1],opponent='E18 frozen775',baseline='repair774_v2 matching seed and role',sources=hashes,stop='Stop on first technical failure of topology, animal mix, opening parity, calls or core errors. No economic tuning after first result.',reserved_seeds='180912401-407 remain unused')
    p=out/'PROTOCOL.json'
    if p.exists():assert json.loads(p.read_text())==protocol
    else:p.write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    outcomes=[]
    for seed in protocol['seeds']:
        for left,right in [('Calendar774','E18'),('E18','Calendar774')]:
            seat=0 if left=='Calendar774' else 1
            meta=runner.run((stage,left,right,seed));path=BASE/f'artifacts/{stage}/{left}_{right}_{seed}.json'
            audit(path)
            kpi=json.loads(path.with_suffix('.kpi.json').read_text())['sides'][seat]
            with gzip.open(path.with_suffix('.replay.json.gz'),'rt',encoding='utf-8') as f:r=json.load(f)
            bleft,bright=('Repair774','E18') if seat==0 else ('E18','Repair774')
            bpath=BASE/f'artifacts/repair774_v2/{bleft}_{bright}_{seed}.replay.json.gz'
            with gzip.open(bpath,'rt',encoding='utf-8') as f:b=json.load(f)
            prefix=all(r['steps'][i][seat]['action']==b['steps'][i][seat]['action'] for i in range(1,265))
            last=kpi['kpi'][-1];mix={k:last[k] for k in ['COW','SHEEP','GOOSE']}
            passed=prefix and meta['opening'][seat]['topology']==[7,7,4] and mix=={'COW':8,'SHEEP':9,'GOOSE':1} and meta['runtime'][seat]['calls']==719 and meta['runtime'][seat]['core_errors']==0
            row=dict(seed=seed,seat=seat,technical_pass=passed,prefix_equal=prefix,mix=mix,topology=meta['opening'][seat]['topology'],cash=meta['rewards'][seat],baseline_cash=b['rewards'][seat],cash_delta=meta['rewards'][seat]-b['rewards'][seat],runtime=meta['runtime'][seat]);outcomes.append(row)
            (out/'RESULTS.json').write_text(json.dumps(outcomes,indent=2),encoding='utf-8');print('GATE',json.dumps(row),flush=True)
            if not passed:return
if __name__=='__main__':main()
