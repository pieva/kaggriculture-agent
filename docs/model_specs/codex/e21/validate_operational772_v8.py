from pathlib import Path
import sys,json,runpy,hashlib
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.operational772_v8_policy import Agent
from docs.model_specs.codex.e20.tools import run_experiment as runner
from docs.model_specs.codex.e20.tools.audit_results import run as audit
if __name__=='__main__':
 runner.BASE=BASE
 runner.policy=lambda name,seat: Agent({'player_position':seat}) if name=='Op772' else runpy.run_path(str(ROOT/'submission'/('submission_codex_e20_772_e20v28_loaderfix.py' if name=='Base772' else 'submission_codex_e18_2_capacity_governed_v4d.py')))['create_agent']({'player_position':seat})
 out=BASE/'reports/operational772_validation';out.mkdir(exist_ok=True)
 sources=[BASE/'operational772_v8_policy.py',BASE/'reports/operational772_v8/PLAN_772.json',BASE/'reports/operational772_v8/PLAN_NATIVE.json',BASE/'reports/common_operational_program/PROGRAM.json',ROOT/'submission/submission_codex_e20_772_e20v28_loaderfix.py',ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py',Path(__file__)]
 protocol={'seed':180911303,'seat':0,'opponent':'frozen775','scope':'One additional exposed seed, frozen V8 and published772; no tuning and no publication. This is not reserved holdout validation.','sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
 (out/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8')
 for name in ['Base772','Op772']:
  meta=runner.run(('operational772_validation',name,'E18',180911303))
  audit(BASE/f'artifacts/operational772_validation/{name}_E18_180911303.json')
  print('RESULT',name,meta['rewards'],flush=True)
