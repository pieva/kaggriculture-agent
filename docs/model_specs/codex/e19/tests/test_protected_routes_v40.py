import unittest
from docs.model_specs.codex.e19.tools.daily_routes_770_v40 import pack_routes, route_cost, protected_order

class ProtectedRoutesTests(unittest.TestCase):
    pack=staticmethod(pack_routes)
    def test_nearby_plant_cannot_precede_animal_visit(self):
        animal=((4,0),[['FEED'],['CARE']],8,1,'SERVICE')
        plant=((1,0),[['PLANT','WHEAT'],['WATER']],7,1,'NEW_ROTATION')
        routes,unassigned=self.pack([(0,0)],[{'WHEAT':1}],[(0,0)],[plant,animal],20)
        self.assertEqual(unassigned,[])
        self.assertEqual(routes[0],[animal,plant])
        self.assertLessEqual(route_cost((0,0),routes[0],[(0,0)],{'WHEAT':1}),20)
    def test_renewal_is_left_out_when_protected_route_fills_budget(self):
        animal=((4,0),[['FEED'],['CARE']],8,1,'SERVICE')
        plant=((1,0),[['PLANT','WHEAT'],['WATER']],7,1,'NEW_ROTATION')
        routes,unassigned=self.pack([(0,0)],[{'WHEAT':1}],[(0,0)],[plant,animal],6)
        self.assertEqual(routes,[[animal]])
        self.assertEqual(unassigned,[plant])
    def test_multiple_workers_obey_order_and_budgets(self):
        offers=[((x,0),[['CARE']],8,1,'SERVICE') for x in (3,7)]
        offers+=[((x,1),[['PLANT','WHEAT'],['WATER']],7,1,'NEW_ROTATION') for x in range(9)]
        routes,_=self.pack([(0,0),(9,0)],[{},{}],[(0,0)],offers,10)
        for start,route in zip([(0,0),(9,0)],routes):
            self.assertTrue(protected_order(route))
            self.assertLessEqual(route_cost(start,route,[(0,0)],{}),10)

from docs.model_specs.codex.e19.tools.daily_routes_770_v41 import pack_routes as pack_v41

class V41ProtectedRoutesTests(ProtectedRoutesTests):
    pack=staticmethod(pack_v41)

if __name__=='__main__':unittest.main()
