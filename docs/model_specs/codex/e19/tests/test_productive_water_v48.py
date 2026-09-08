import unittest
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import yield_water_units,due_visit
from docs.model_specs.codex.e19.tools.daily_route_dispatch_770_v48 import v48_essential_allowed

RULES={'CARROT':dict(ongoing=False,max_yield_day=3,max_yield=4),'STRAWBERRY':dict(ongoing=True,max_yield_day=10,max_yield=4)}
def tile(**changes):
    return dict(dict(kind='PLANT',crop='CARROT',planted_day=25,yield_units=2,watered_today=False,fertilized_until_day=-1,max_lifespan_step=696),**changes)

class ProductiveWaterTests(unittest.TestCase):
    def test_water_gain_is_bounded_and_observed(self):
        self.assertEqual(yield_water_units(tile(),28,RULES),1)
        self.assertEqual(yield_water_units(tile(fertilized_until_day=28),28,RULES),2)
        self.assertEqual(yield_water_units(tile(fertilized_until_day=28,yield_units=3),28,RULES),1)
        for t in [tile(watered_today=True),tile(yield_units=4),tile(crop='STRAWBERRY')]:
            self.assertEqual(yield_water_units(t,28,RULES),0)
        self.assertEqual(yield_water_units(tile(),26,RULES),0)
    def test_full_visit_and_short_fallback_remain_available(self):
        offer=((0,0),[['WATER'],['HARVEST']],4,20,'SERVICE')
        full,bare=due_visit(offer,tile(),28,24,RULES,lambda c,s,n:10*n)
        self.assertEqual(full,((0,0),[['WATER'],['HARVEST']],6,30,'SERVICE'))
        self.assertEqual(bare,((0,0),[['HARVEST']],5,20,'SERVICE'))
    def test_pre_d28_due_harvest_keeps_baseline(self):
        t=tile(planted_day=23,max_lifespan_step=648)
        full,bare=due_visit(((0,0),[['WATER'],['HARVEST']],4,20,'SERVICE'),t,26,24,RULES,lambda *a:0)
        self.assertEqual(full[1],[['HARVEST']]);self.assertIsNone(bare)
    def test_no_water_only_fallback_for_due_productive_visit(self):
        for priority in (6,8):
            self.assertFalse(v48_essential_allowed(28,'SERVICE',[['WATER'],['HARVEST']],priority))
        self.assertTrue(v48_essential_allowed(26,'SERVICE',[['WATER'],['HARVEST']],6))
        self.assertTrue(v48_essential_allowed(28,'SERVICE',[['FEED']],8))

if __name__=='__main__':unittest.main()
