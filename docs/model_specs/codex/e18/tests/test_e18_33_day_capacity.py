"""Current-day certificate, independent of scenario dates and quadrant names."""
import json
from pathlib import Path
from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

CONFIG=json.loads((Path(__file__).resolve().parents[1]/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json').read_text())

def controller(remaining):
    c=CommonController(CONFIG,None,{})
    c.positions=[(4,4)]; c.private=dict(inventories=[{}],shed={})
    c.sheds=[(4,4)]; c.remaining=remaining
    c._services=lambda:[((3,4),[['WATER']],1,1,'SERVICE')]
    return c

def test_investment_must_leave_a_route_to_existing_service():
    c=controller(2)
    job=dict(target=(4,4),steps=[(['PLANT','WHEAT'],(4,4)),(['WATER'],(4,4))],kind='NEW_CROP')
    assert not c._day_route_certificate(0,job)
    c.remaining=4
    assert c._day_route_certificate(0,job)

def test_does_not_count_hires_that_are_not_observed():
    c=controller(2)
    job=dict(target=(4,4),steps=[(['PLANT','WHEAT'],(4,4)),(['WATER'],(4,4))],kind='NEW_CROP')
    assert not c._day_route_certificate(0,job)
    c.positions.append((3,4)); c.private['inventories'].append({})
    assert c._day_route_certificate(0,job)
