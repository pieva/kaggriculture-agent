"""Focused comparison with installed engine semantics, not economic promotion."""
import importlib
import json
from collections import Counter
from pathlib import Path

import pytest

from docs.model_specs.codex.e18.tools.e18_33_common_policy import CROPS, ANIMALS, crop_cashflows, animal_cashflows
from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

ENGINE = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")
BASE = Path(__file__).resolve().parents[1]
CONFIG = json.loads((BASE / "configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json").read_text())


def test_rule_tables_match_installed_engine():
    for species, rule in ANIMALS.items():
        assert all(ENGINE.ANIMALS[species][k] == v for k,v in rule.items())
    for species, rule in ENGINE.CROPS.items():
        assert all(CROPS[species][k] == v for k,v in rule.items())


@pytest.mark.parametrize("crop", list(CROPS))
def test_crop_cashflow_matches_engine_refresh(crop):
    farm=ENGINE._new_farm(10,3000)
    private=ENGINE._new_private()
    farm["tiles"][4][4]=ENGINE._new_plant(crop,0,24)
    expected=crop_cashflows(crop,0,29)
    actual=[]
    harvest_days={d for d,_ in expected}
    for day in range(30):
        ENGINE._apply_unit_action(farm,private,0,["WATER"],10,day,24)
        if day in harvest_days:
            before=private["inventories"][0].get(crop,0)
            ENGINE._apply_unit_action(farm,private,0,["HARVEST"],10,day,24)
            actual.append((day,private["inventories"][0].get(crop,0)-before))
        ENGINE._daily_refresh_plants(farm,day,24)
    assert actual==expected


@pytest.mark.parametrize("species", list(ANIMALS))
def test_animal_cashflow_matches_engine_refresh(species):
    farm=ENGINE._new_farm(10,3000)
    private=ENGINE._new_private()
    private["inventories"][0]["WHEAT"]=30
    farm["tiles"][4][4]=ENGINE._new_animal(species,0)
    actual=[]
    for day in range(30):
        tile=farm["tiles"][4][4]
        if tile["yield_units"]:
            actual.append((day,tile["yield_units"]))
            ENGINE._apply_unit_action(farm,private,0,["HARVEST"],10,day,24)
        ENGINE._apply_unit_action(farm,private,0,["FEED"],10,day,24)
        ENGINE._apply_unit_action(farm,private,0,["CARE"],10,day,24)
        ENGINE._daily_refresh_animals(farm,day)
    assert actual==animal_cashflows(species,0,29)


def test_paid_feed_does_not_block_current_workers_again():
    c=CommonController(CONFIG,ENGINE.market_price,ENGINE.MARKET_PARAMS)
    c.farm=dict(money=5,hands=[],unlocked_quadrants=["NW","NE","SW"],
                tiles=[[dict(kind="PLANT") for _ in range(10)] for _ in range(10)])
    c.private=dict(shed={"WHEAT":14},seeds={},inventories=[{}])
    c._services=lambda:[((0,0),[["FEED"],["CARE"],["COLLECT_FERTILIZER"]],3,1,"SERVICE")]*14
    c._quote=lambda item,op,n:25*n
    c.active={}; c.unfed=14; c.feed_reserve=350; c.maintenance_floor=400
    c.day=1; c.final_day=29; c.remaining=24; c.hire_mult=1; c.positions=[(4,4)]
    c.crop_values={"WHEAT":{"gain":100}}
    orders=c._market_orders()
    assert orders==[["HIRE"],["HIRE"],["HIRE"]]


def test_observed_feed_is_net_of_next_day_reserve():
    c=CommonController(CONFIG,ENGINE.market_price,ENGINE.MARKET_PARAMS)
    c.farm=dict(tiles=[[dict(kind="PASTURE",animal="SHEEP") for _ in range(5)]])
    c.private=dict(shed={"WHEAT":10},inventories=[{}])
    c.turns=24; c.hire_mult=1; c._quote=lambda item,op,n:25*n
    # Five animals: estimated two units including farmer, salary 1; feed funded.
    assert c._maintenance_floor()==1
    c.private["shed"]["WHEAT"]=0
    assert c._maintenance_floor()==251


def test_farmer_does_not_hoard_feed_before_hires_are_observed():
    c=CommonController(CONFIG,ENGINE.market_price,ENGINE.MARKET_PARAMS)
    c.farm=ENGINE._new_farm(10,3000)
    for n in range(12):
        c.farm["tiles"][n//5][n%5]=dict(kind="PASTURE",animal="COW")
    c.private=ENGINE._new_private(); c.private["shed"]["WHEAT"]=12
    c.positions=[(4,4)]; c.sheds=ENGINE._shed_access_tiles(10)
    c.turns=24; c.remaining=24; c.unfed=12
    steps=c._prepare_steps(0,(4,4),[["FEED"]])
    pickups=[cmd[2] for cmd,_ in steps if cmd[:2]==["PICKUP","WHEAT"]]
    assert pickups==[3]
    assert len(c.positions)==1  # Future capacity was not turned into real workers.
