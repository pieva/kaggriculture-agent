"""A service bundle must not suppress feasible deadline-critical actions."""
import json
from collections import Counter
from pathlib import Path

from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

PROFILE = json.loads((Path(__file__).resolve().parents[1]/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V2_BOOTSTRAP.json').read_text())


def controller():
    c = CommonController(PROFILE, None, {})
    c.private = dict(inventories=[{'WHEAT':1}], shed={})
    c.positions = [(8,4)]
    c.sheds = [(4,4)]
    c.remaining = 1
    c._quote = lambda *args: 25
    return c


def test_last_slot_feed_survives_impossible_collection_and_delivery():
    c = controller()
    commands = [['FEED'],['CARE'],['COLLECT_FERTILIZER']]
    assert c._prepare_steps(0,(8,4),commands,requirements=Counter()) is None
    assert c._essential_steps(0,(8,4),commands,3,1000,Counter()) == [(['FEED'],(8,4))]


def test_water_survives_impossible_optional_fertilizer_trip():
    c = controller()
    assert c._essential_steps(0,(8,4),[['FERTILIZE'],['WATER']],3,0,Counter()) == [(['WATER'],(8,4))]


def test_no_time_for_travel_does_not_invent_feasible_feed():
    c = controller()
    assert c._essential_steps(0,(9,4),[['FEED'],['CARE']],3,1000,Counter()) is None
