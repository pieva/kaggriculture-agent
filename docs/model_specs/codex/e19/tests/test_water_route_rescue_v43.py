import ast
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.daily_routes_770_v43 import route_cost,inputs,harvest_due

def prepare_elsewhere(target,remaining=10,stress=1):
    tile=dict(kind='PLANT',crop='STRAWBERRY',consecutive_unwatered=stress,watered_today=False)
    core=SimpleNamespace(day=20,turns=24,remaining=remaining,_tile=lambda t:tile,
        active={},positions=[(0,0),(9,0)],sheds=[(0,0)],
        private={'inventories':[{},{}],'shed':{}},_requirements=lambda:(Counter(),Counter()))
    queues={0:[target],1:[]};contracts={target:(target,[['WATER']],3,1,'SERVICE')}
    path=Path(__file__).parents[1]/'tools/daily_routes_770_v43.py'
    fn=next(n for n in ast.walk(ast.parse(path.read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name=='route_prepare')
    scope=dict(core=core,queues=queues,contracts=contracts,Counter=Counter,route_cost=route_cost,inputs=inputs,harvest_due=harvest_due,
        prepare=lambda worker,target,commands,**kw:[(c,target) for c in commands])
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),scope)
    return scope['route_prepare'](1,target,[['WATER']])

class RescueTests(unittest.TestCase):
    def test_feasible_owner_route_is_respected(self):
        self.assertIsNone(prepare_elsewhere((4,0)))
    def test_late_owner_allows_nearby_worker(self):
        self.assertEqual(prepare_elsewhere((10,0)),[(['WATER'],(10,0))])
    def test_nonurgent_crop_does_not_trigger_rescue(self):
        self.assertIsNone(prepare_elsewhere((10,0),stress=0))

if __name__=='__main__':unittest.main()
