"""The alternating calendar must not suppress a required service or closure."""
import ast
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.biological_plan_770_v38 import biological_calendar

def services(day, watered=False, required=False):
    tile=dict(kind='PLANT',crop='STRAWBERRY',planted_day=day,watered_today=watered,
              yield_units=0,consecutive_unwatered=0,fertilized_until_day=-1)
    core=SimpleNamespace(day=day,final_day=29,farm={'tiles':[[tile]]},active={},
        private={'shed':{}},_requirements=lambda:(Counter(),Counter()),_quote=lambda *args:0)
    rule=dict(first_yield_day=4,max_yield=6,interval=2,ongoing=True)
    scope=dict(core=core,observe_plan=lambda:None,services=lambda:['closure'],
        biological_calendar=biological_calendar,rules={'CROPS':{'STRAWBERRY':rule},'ANIMALS':{},'needs_water':lambda t,d:required})
    path=Path(__file__).parents[1]/'tools/biological_plan_770_v38.py'
    tree=ast.parse(path.read_text(encoding='utf-8'))
    fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='planned_services')
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),scope)
    return scope['planned_services']()

class CalendarTests(unittest.TestCase):
    def test_alternating_slots(self):
        self.assertEqual(services(12)[0][1],[['WATER']])
        self.assertEqual(services(13),[])
    def test_required_water_overrides_off_day(self):
        self.assertEqual(services(13,required=True)[0][1],[['WATER']])
        self.assertEqual(services(12,watered=True,required=True),[])
    def test_closure_uses_original_services(self):
        self.assertEqual(services(25),['closure'])

if __name__=='__main__':unittest.main()
