import ast
import unittest
from pathlib import Path
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.portfolio_workforce_v16 import care_value

def services(day,placed=1):
    t=dict(kind='PASTURE',animal='COW',placed_day=placed,fed_today=False,cared_today=False,yield_units=0)
    rule=dict(first_yield_day=8,interval=2,max_held=6,product='MILK')
    core=SimpleNamespace(day=day,final_day=29,active={},farm={'tiles':[[t]]},_quote=lambda *a:100)
    p=Path(__file__).parents[1]/'tools/biological_plan_770_v46.py'
    fn=next(n for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name=='planned_services')
    scope=dict(core=core,observe_plan=lambda:None,services=lambda:['terminal'],care_value=care_value,rules={'ANIMALS':{'COW':rule}})
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(p),'exec'),scope)
    return scope['planned_services']()

class FinalServicesTests(unittest.TestCase):
    def test_care_when_final_production_can_use_it(self):
        self.assertEqual(services(27)[0][1],[['FEED'],['CARE']])
    def test_no_care_when_cycle_has_no_remaining_production(self):
        self.assertEqual(services(27,placed=0)[0][1],[['FEED']])
    def test_d29_feeds_but_no_late_care(self):
        self.assertEqual(services(28)[0][1],[['FEED']])
    def test_d30_uses_terminal_policy(self):
        self.assertEqual(services(29),['terminal'])

if __name__=='__main__':unittest.main()
