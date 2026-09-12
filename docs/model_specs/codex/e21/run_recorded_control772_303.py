"""Exact recorded-order control to separate route reconstruction from market changes."""
from pathlib import Path
import sys,json,runpy,hashlib
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e21.operational_program import OperationalProgram
from docs.model_specs.codex.e20.tools import run_experiment as runner
from docs.model_specs.codex.e20.tools.audit_results import run as audit
runner.BASE=BASE
program=json.loads((BASE/'reports/common_operational_program/PROGRAM.json').read_text(encoding='utf-8'))
def factory(name,seat):
    if name=='OpRecorded':return OperationalProgram(program,seat,strict=False)
    return runpy.run_path(str(ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'))['create_agent']({'player_position':seat})
runner.policy=factory
out=BASE/'reports/operational772_recorded_control_303';out.mkdir(parents=True,exist_ok=True)
(out/'PROTOCOL.json').write_text(json.dumps(dict(seed=180911303,seat=0,opponent='frozen775',scope='Unmodified source order stream; no reconstruction or adaptation. Observe first position divergence in new market.',program_sha256=hashlib.sha256((BASE/'reports/common_operational_program/PROGRAM.json').read_bytes()).hexdigest()),indent=2),encoding='utf-8')
meta=runner.run(('operational772_recorded_control','OpRecorded','E18',180911303))
audit(BASE/'artifacts/operational772_recorded_control/OpRecorded_E18_180911303.json')
