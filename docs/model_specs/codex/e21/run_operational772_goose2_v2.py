from pathlib import Path
import sys,json,runpy,hashlib
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.operational772_goose2_v2_policy import Agent
from docs.model_specs.codex.e20.tools import run_experiment as runner
from docs.model_specs.codex.e20.tools.audit_results import run as audit
if __name__=='__main__':
    runner.BASE=BASE
    runner.policy=lambda name,seat: Agent({'player_position':seat}) if name=='Goose2' else runpy.run_path(str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'))['create_agent']({'player_position':seat})
    out=BASE/'reports/operational772_goose2_v2';out.mkdir(exist_ok=True)
    sources=[Path(__file__),BASE/'operational772_goose2_v2_policy.py',BASE/'operational772_v8_policy.py',BASE/'reports/operational772_v8/PLAN_772.json',BASE/'reports/operational772_v8/PLAN_NATIVE.json',BASE/'reports/common_operational_program/PROGRAM.json',ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py']
    protocol={'seeds':[180911301,180911303],'seat':0,'opponent':'frozen775','change':'Replace COW by GOOSE at (6,3) and (4,5), PASTURE by COOP; same V8 routes, crop calendar, observed resupply and extra specialist. Fixed before both games.','expected_final':{'COW':8,'SHEEP':6,'GOOSE':2},'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    dest=out/'PROTOCOL.json'
    if dest.exists():assert json.loads(dest.read_text(encoding='utf-8'))==protocol
    else:dest.write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    for seed in protocol['seeds']:
        m=runner.run(('operational772_goose2_v2','Goose2','E18',seed))
        audit(BASE/f'artifacts/operational772_goose2_v2/Goose2_E18_{seed}.json')
        print('RESULT',seed,m['rewards'],flush=True)
