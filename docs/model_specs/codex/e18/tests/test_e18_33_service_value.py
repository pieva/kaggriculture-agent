import importlib
import json
from pathlib import Path
from docs.model_specs.codex.e18.artifacts.source.e18_33_common_controller_v8 import CommonController

ENGINE=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
CONFIG=json.loads((Path(__file__).resolve().parents[1]/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V2_BOOTSTRAP.json').read_text())

def controller(day,placed):
    c=CommonController(CONFIG,ENGINE.market_price,ENGINE.MARKET_PARAMS)
    c.farm=ENGINE._new_farm(10,3000); c.private=ENGINE._new_private()
    c.farm['tiles'][4][4]=ENGINE._new_animal('COW',placed)
    c.day=day; c.final_day=29; c._quote=lambda item,op,n:100*n
    return c

def test_care_uses_birth_schedule_and_post_production_timing():
    c=controller(26,1) # production D-index 27, 29: care now contributes at 29.
    assert ['CARE'] in c._services()[0][1]
    c.day=28 # tomorrow is the last production; today's CARE arrives too late.
    assert ['CARE'] not in c._services()[0][1]

def test_future_care_value_is_not_zero_when_no_product_is_ready():
    c=controller(0,0)
    service=c._services()[0]
    assert service[3]>=200 # FEED replacement cost plus a future CARE unit.

def test_stranded_grain_does_not_cancel_an_assigned_pickup_requirement():
    c=controller(10,0)
    c.positions=[(4,4),(0,0)]; c.private['inventories']=[{}, {'WHEAT':3}]
    c.active={0:dict(kind='SERVICE',target=(4,4),steps=[(['PICKUP','WHEAT',1],(4,4)),(['FEED'],(4,4))])}
    assert c._requirements()[0]['WHEAT']==1
    c.sheds=[(4,4)]; c.turns=24; c.remaining=24; c.unfed=1
    assert c._prepare_steps(0,(4,4),[['FEED']],buy=True) is not None
