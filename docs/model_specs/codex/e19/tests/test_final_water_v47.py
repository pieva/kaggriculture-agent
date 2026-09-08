import unittest
from docs.model_specs.codex.e19.tools.daily_routes_770_v47 import final_water_deadline,pack_routes

class FinalWaterTests(unittest.TestCase):
    def test_only_transition_days(self):
        tile=dict(kind='PLANT',consecutive_unwatered=1,watered_today=False)
        self.assertEqual([final_water_deadline(d,tile,[['WATER']]) for d in [26,27,28,29]],[False,True,True,False])
    def test_observed_water_and_new_plant_are_excluded(self):
        tile=dict(kind='PLANT',consecutive_unwatered=1,watered_today=True)
        self.assertFalse(final_water_deadline(27,tile,[['WATER']]))
        tile['watered_today']=False
        self.assertFalse(final_water_deadline(27,tile,[['DIG'],['PLANT','CARROT'],['WATER']]))
    def test_water_deadline_precedes_discretionary_harvest(self):
        water=((3,0),[['WATER']],8,1,'SERVICE')
        harvest=((1,0),[['HARVEST']],4,50,'SERVICE')
        routes,left=pack_routes([(0,0)],[{}],[(0,0)],[harvest,water],4)
        self.assertEqual(routes,[[water]])
        self.assertEqual(left,[harvest])

if __name__=='__main__':unittest.main()
