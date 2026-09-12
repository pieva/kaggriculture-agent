"""Serial native/adapted operational execution, same engine seed and opponent."""
from pathlib import Path
import sys,json,hashlib,runpy
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.operational772_v3_policy import Agent
from docs.model_specs.codex.e20.tools import run_experiment as runner
from docs.model_specs.codex.e20.tools.audit_results import run as audit
STAGE='operational772_v3'
def main():
    runner.BASE=BASE;created=[]
    def factory(name,seat):
        a=Agent({'player_position':seat},name=='Op772') if name in ['OpNative','Op772'] else runpy.run_path(str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'))['create_agent']({'player_position':seat})
        created.append(a);return a
    runner.policy=factory
    out=BASE/'reports'/STAGE
    sources=[BASE/'adapt_operational772_v2.py',BASE/'operational772_v3_policy.py',Path(__file__),out/'PLAN_772.json',out/'PLAN_NATIVE.json',ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py']
    protocol=dict(scope='Compiled worker visits from D1, fixed daily ordering, observed resource resupply; native control and 772 adaptation. V3 preserves compiled V2 routes and repairs fertilizer reservation, ripe-crop prerequisites and final delivery. One technical case each before extension.',seed=180911301,seat=0,opponent='frozen775',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},gate='719 calls, zero errors, native14pastures/8C6S3G; adapted772/10C6S0G; D1 12M7W, strawberries D6/D9/D12=4/20/33. No promotion if technical timing fails.',reserved='180912401-407 unused')
    if (out/'PROTOCOL.json').exists():assert json.loads((out/'PROTOCOL.json').read_text(encoding='utf-8'))==protocol
    else:(out/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    rows=[]
    for name in ['OpNative','Op772']:
        created.clear();meta=runner.run((STAGE,name,'E18',180911301));path=BASE/f'artifacts/{STAGE}/{name}_E18_180911301.json';audit(path)
        profile=json.loads(path.with_suffix('.kpi.json').read_text(encoding='utf-8'))['sides'][0]
        if created:
            (out/f'{name}_UNFINISHED.json').write_text(json.dumps(created[0].log,indent=2),encoding='utf-8')
        final=profile['kpi'][-1]
        checkpoints={str(d):{k:profile['kpi'][d-1][k] for k in ['MELON','WHEAT','STRAWBERRY','COW','SHEEP','GOOSE','people','money']} for d in [1,6,9,12,15,30]}
        row=dict(name=name,rewards=meta['rewards'],runtime=meta['runtime'][0],topology=meta['opening'][0]['topology'],checkpoints=checkpoints,crop_losses=len(profile['crop_starvation']),animal_losses=sum(k['verified_animal_losses'] for k in profile['kpi']),terminal=profile['terminal'])
        rows.append(row);(out/'RESULTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print('RESULT',json.dumps(row),flush=True)
if __name__=='__main__':main()
