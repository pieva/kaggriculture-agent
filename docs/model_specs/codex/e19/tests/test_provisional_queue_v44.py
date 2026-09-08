import ast
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from docs.model_specs.codex.e19.tools.daily_routes_770_v44 import inputs,harvest_due

def prepare_after(head_kind,command):
    target=(2,0);head=(1,0)
    tile=dict(kind='PLANT',crop='WHEAT',yield_units=0,consecutive_unwatered=0)
    core=SimpleNamespace(day=20,turns=24,remaining=16,_tile=lambda t:tile,
        private={'inventories':[{}],'shed':{}},_requirements=lambda:(Counter(),Counter()))
    queues={0:[head,target]}
    contracts={head:(head,[['PLANT','WHEAT'],['WATER']],7,1,head_kind),target:(target,[command],3,1,'SERVICE')}
    path=Path(__file__).parents[1]/'tools/daily_routes_770_v44.py'
    fn=next(n for n in ast.walk(ast.parse(path.read_text(encoding='utf-8'))) if isinstance(n,ast.FunctionDef) and n.name=='route_prepare')
    scope=dict(core=core,queues=queues,contracts=contracts,Counter=Counter,inputs=inputs,harvest_due=harvest_due,
        prepare=lambda worker,target,commands,**kw:[(c,target) for c in commands])
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),scope)
    return scope['route_prepare'](0,target,[command])

class QueueTests(unittest.TestCase):
    def test_water_can_pass_a_provisional_renewal(self):
        self.assertEqual(prepare_after('NEW_ROTATION',['WATER']),[(['WATER'],(2,0))])
    def test_water_can_pass_a_provisional_plant(self):
        self.assertEqual(prepare_after('NEW_CROP',['WATER']),[(['WATER'],(2,0))])
    def test_existing_service_order_is_preserved(self):
        self.assertIsNone(prepare_after('SERVICE',['WATER']))
    def test_new_plant_does_not_bypass_queue(self):
        self.assertIsNone(prepare_after('NEW_ROTATION',['PLANT','WHEAT']))

if __name__=='__main__':unittest.main()
