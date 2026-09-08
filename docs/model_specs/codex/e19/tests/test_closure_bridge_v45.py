import ast
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.biological_plan_770_v45 import biological_calendar,exhausted_perennial

ROOT=Path(__file__).resolve().parents[5]
RULES=runpy.run_path(str(ROOT/'submission/submission_codex_e19_control_770_v2.py'))['CROPS']

def growth(day):
    core=SimpleNamespace(day=day,final_day=29,active={},_tile=lambda p:None,
        _quote=lambda crop,side,n:35*n,portfolio_proposed_ends={})
    path=ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v45.py'
    fn=next(n for n in ast.walk(ast.parse(path.read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name=='planned_growth')
    scope=dict(core=core,observe_plan=lambda:None,growth=lambda cash:['closure'],intentions={(0,0):'WHEAT'},rules={'CROPS':RULES},biological_calendar=biological_calendar,exhausted_perennial=exhausted_perennial)
    # Prior growth normally supplies tuples; the closure sentinel is only
    # used on days when planned_growth must directly delegate.
    if day<27:scope['growth']=lambda cash:[]
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),scope)
    return scope['planned_growth'](1000)

class ClosureTests(unittest.TestCase):
    def test_d26_uses_full_carrot_cycle_with_delivery_day(self):
        self.assertEqual(growth(25)[0][1],[['PLANT','CARROT'],['WATER']])
    def test_d27_rejects_late_new_cycles(self):
        self.assertEqual(growth(26),[])
    def test_d28_delegates_original_closure(self):
        self.assertEqual(growth(27),['closure'])

if __name__=='__main__':unittest.main()
