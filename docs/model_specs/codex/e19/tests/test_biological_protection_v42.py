import unittest
from docs.model_specs.codex.e19.tools.daily_routes_770_v42 import urgent_biological_visit,pack_routes,route_cost

class ProtectionTests(unittest.TestCase):
    def test_observed_water_deadline(self):
        t=dict(kind='PLANT',consecutive_unwatered=1,watered_today=False)
        self.assertTrue(urgent_biological_visit(t,[['WATER'],['HARVEST']]))
        self.assertFalse(urgent_biological_visit(dict(t,watered_today=True),[['WATER']]))
        self.assertFalse(urgent_biological_visit(dict(t,consecutive_unwatered=0),[['WATER']]))
    def test_renewal_is_not_an_existing_water_obligation(self):
        t=dict(kind='PLANT',consecutive_unwatered=1)
        self.assertFalse(urgent_biological_visit(t,[['DIG'],['PLANT','WHEAT'],['WATER']]))
        self.assertFalse(urgent_biological_visit(None,[['PLANT','WHEAT'],['WATER']]))
    def test_animal_protection_retained(self):
        t=dict(animal='COW',consecutive_unfed=1,fed_today=False)
        self.assertTrue(urgent_biological_visit(t,[['FEED'],['CARE']]))
        self.assertFalse(urgent_biological_visit(dict(t,fed_today=True),[['CARE']]))
    def test_joint_deadlines_fit_before_renewal(self):
        a=((1,0),[['FEED'],['CARE']],8,1,'SERVICE')
        w=((2,0),[['WATER']],8,1,'SERVICE')
        p=((0,0),[['PLANT','WHEAT'],['WATER']],7,1,'NEW_CROP')
        routes,unassigned=pack_routes([(0,0)],[{'WHEAT':1}],[(0,0)],[p,w,a],5)
        self.assertEqual(routes,[[a,w]])
        self.assertEqual(unassigned,[p])
        self.assertEqual(route_cost((0,0),routes[0],[(0,0)],{'WHEAT':1}),5)

if __name__=='__main__':unittest.main()
