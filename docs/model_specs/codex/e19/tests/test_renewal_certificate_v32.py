"""Capacity checks must reserve active work and real biological services."""
import unittest
from types import SimpleNamespace
from collections import Counter
from unittest.mock import patch
from docs.model_specs.codex.e19.tools import daily_route_scheduler_770_v32 as v32
from docs.model_specs.codex.e19.tools import daily_route_scheduler_770_v33 as v33

def core(remaining, tile):
    return SimpleNamespace(_day_route_certificate=lambda *a:False, day=20,hour=0,
        positions=[(0,0)],private={'inventories':[{}],'shed':{'WHEAT':1}},remaining=remaining,
        active={},sheds=[(0,0)],metrics=Counter(),_tile=lambda p:tile)

class CertificateTests(unittest.TestCase):
    def test_plant_does_not_consume_time_reserved_for_existing_water(self):
        for remaining,expected in [(4,True),(3,False)]:
            c=core(remaining,{'kind':'PLANT'})
            with patch.object(v32,'previous',lambda c:None):v32.install(c)
            job={'kind':'NEW_CROP','target':(0,0),'steps':[(['PLANT','WHEAT'],(0,0)),(['WATER'],(0,0))]}
            obligations=[((1,0),[['WATER']],3,1,'SERVICE')]
            self.assertEqual(c._day_route_certificate(0,job,obligations),expected)

    def test_care_reservation_needs_its_own_action(self):
        for module,expected in [(v32,True),(v33,False)]:
            c=core(4,{'kind':'PASTURE','animal':'COW'})
            c.private['inventories']=[{'WHEAT':1}]
            with patch.object(module,'previous',lambda c:None):module.install(c)
            job={'kind':'NEW_CROP','target':(0,0),'steps':[(['PLANT','WHEAT'],(0,0)),(['WATER'],(0,0))]}
            obligations=[((1,0),[['FEED'],['CARE']],3,1,'SERVICE')]
            self.assertEqual(c._day_route_certificate(0,job,obligations),expected)

    def test_delivery_does_not_cover_crop_at_shed(self):
        c=core(1,{'kind':'PLANT'})
        with patch.object(v32,'previous',lambda c:None):v32.install(c)
        job={'kind':'DELIVER','target':(0,0),'steps':[(['DROP'],(0,0))]}
        self.assertFalse(c._day_route_certificate(0,job,[((0,0),[['WATER']],3,1,'SERVICE')]))

if __name__=='__main__':unittest.main()
