"""Protect future and held harvests while admitting an exhausted plot."""
import ast
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.biological_plan_770_v39 import biological_calendar, exhausted_perennial

ROOT=Path(__file__).resolve().parents[5]
RULES=runpy.run_path(str(ROOT/'submission/submission_codex_e19_control_770_v2.py'))['CROPS']

def growth(day, units, planted=5):
    tile=dict(kind='PLANT',crop='STRAWBERRY',planted_day=planted,yield_units=units)
    core=SimpleNamespace(day=day,final_day=29,active={},_tile=lambda p:tile,
        _quote=lambda crop,side,n:35*n,portfolio_proposed_ends={})
    path=ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v39.py'
    fn=next(n for n in ast.walk(ast.parse(path.read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name=='planned_growth')
    scope=dict(core=core,observe_plan=lambda:None,growth=lambda cash:[],intentions={(0,0):'STRAWBERRY'},
        rules={'CROPS':RULES},biological_calendar=biological_calendar,exhausted_perennial=exhausted_perennial)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),scope)
    return scope['planned_growth'](1000)

class RenewalTests(unittest.TestCase):
    def test_future_production_survives(self):
        self.assertEqual(growth(20,0),[])
    def test_empty_final_crop_needs_no_harvest(self):
        offer=growth(21,0)[0]
        self.assertEqual(offer[1][0],['DIG'])
        self.assertFalse(any(c[0]=='HARVEST' for c in offer[1]))
        self.assertEqual(offer[1][-1],['WATER'])
        self.assertEqual(offer[4],'NEW_ROTATION')
    def test_held_final_yield_is_collected_before_dig(self):
        self.assertEqual(growth(21,2)[0][1][:2],[['HARVEST'],['DIG']])
    def test_horizon_does_not_define_biological_exhaustion(self):
        self.assertEqual(growth(24,0,planted=12),[])

if __name__=='__main__':unittest.main()
