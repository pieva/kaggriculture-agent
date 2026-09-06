import ast
import json
from copy import deepcopy
from pathlib import Path

import pytest

from docs.model_specs.codex.e18.tools.e18_33_common_policy import (
    Profile, PriceEnvelope, crop_candidates, pasture_candidates, crop_cashflows,
    animal_cashflows, needs_water, biological_deadline,
)

BASE = Path(__file__).resolve().parents[1]
CONFIG = json.loads((BASE / "configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json").read_text())


@pytest.mark.parametrize("target,capacity,expected,mix", [
    (14,7,[7,7,0],{"COW":9,"SHEEP":5}),
    (15,7,[7,7,1],{"COW":10,"SHEEP":5}),
    (16,7,[7,7,2],{"COW":10,"SHEEP":6}),
    (14,6,[6,6,2],{"COW":9,"SHEEP":5}),
])
def test_parametric_contract_without_topology_code(target,capacity,expected,mix):
    c=deepcopy(CONFIG)
    c["pastures"].update(target=target,uniform_capacity_per_quadrant=capacity)
    p=Profile.from_config(c)
    assert list(p.pasture_budgets(["a","b","c"]).values()) == expected
    assert p.species_targets() == mix
    p.validate_board(10)


def test_labels_do_not_select_policy():
    p=Profile.from_config(CONFIG)
    assert list(p.pasture_budgets(["NW","NE","SW"]).values()) == list(p.pasture_budgets(["third","first","second"]).values())


def test_first_pasture_uses_central_tile_not_legacy_list():
    farm=dict(tiles=[[None if x<5 and y<5 else "LOCKED" for x in range(10)] for y in range(10)], unlocked_quadrants=["NW"])
    assert pasture_candidates(farm,Profile.from_config(CONFIG))[0] == (4,4)
    assert len(crop_candidates(farm)) == 25


def test_fifteenth_pasture_is_generated_on_third_land():
    farm=dict(tiles=[[None if x<5 or y<5 else "LOCKED" for x in range(10)] for y in range(10)], unlocked_quadrants=["NW","NE","SW"])
    for x in [0,5]:
        for i in range(7):
            farm["tiles"][i//5][x+i%5] = dict(kind="PASTURE",animal="COW")
    assert not pasture_candidates(farm,Profile.from_config(CONFIG))
    c=deepcopy(CONFIG); c["pastures"]["target"]=15
    candidates=pasture_candidates(farm,Profile.from_config(c))
    assert candidates and all(x<5 and y>=5 for x,y in candidates)
    assert not pasture_candidates(farm,Profile.from_config(c),reserved=[candidates[0]])


def test_harvest_frees_crop_candidate_immediately_in_any_quadrant():
    farm=dict(tiles=[[None if x<5 or y<5 else "LOCKED" for x in range(10)] for y in range(10)],unlocked_quadrants=["NW","NE","SW"])
    for pos in ((0,0),(5,0),(0,5)):
        x,y=pos
        farm["tiles"][y][x]=dict(kind="PLANT",crop="MELON")
        assert pos not in crop_candidates(farm)
        farm["tiles"][y][x]=None
        assert pos in crop_candidates(farm)


@pytest.mark.parametrize("crop,first,last,expected", [
    ("WHEAT",0,4,[(4,4)]), ("WHEAT",0,2,[(2,2)]),
    ("MELON",0,12,[(12,6)]), ("MELON",0,9,[]),
    ("STRAWBERRY",0,29,[(10,1),(12,1),(14,1),(16,1)]),
    ("TOMATO",0,29,[(8,1),(9,1),(10,1),(11,1)]),
])
def test_age_based_crop_cashflow(crop,first,last,expected):
    assert crop_cashflows(crop,first,last)==expected
    assert crop_cashflows(crop,first+3,last+3)==[(d+3,n) for d,n in expected]


def test_species_specific_maturity_and_care():
    assert animal_cashflows("COW",0,10)==[(8,6),(10,3)]
    assert animal_cashflows("SHEEP",0,9)==[(6,6),(9,4)]
    assert animal_cashflows("SHEEP",0,5)==[]


def test_first_water_and_global_terminal_deadline():
    tile=dict(kind="PLANT",crop="WHEAT",planted_day=0,consecutive_unwatered=1,watered_today=False)
    assert needs_water(tile,0)
    assert biological_deadline(tile,0,24,720)==23
    assert biological_deadline(tile,29,24,720)==718
    tile["watered_today"]=True
    assert not needs_water(tile,0)


def test_price_history_has_no_legacy_commission():
    prices=PriceEnvelope(); prices.observe({"WHEAT":25}); prices.observe({"WHEAT":30})
    assert prices.conservative("WHEAT","SELL",[28,24])==49
    assert prices.conservative("WHEAT","BUY",[28,32])==62


def test_no_historical_import_or_profile_fields():
    for name in ("e18_33_common_policy.py","e18_33_common_controller.py"):
        tree=ast.parse((BASE/"tools"/name).read_text())
        imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        assert all(not any(f"e18_{v}_" in (m or "") for v in range(18,33)) for m in imports)
        strings={n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
        assert not strings & {"trajectory","reference_plan","treatment_config","opponent","late_q0_pasture_day"}
        # CROPS[crop]['seed'] is the seed price, not the episode's random seed.
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id in {"observation", "configuration", "config"}:
                assert not isinstance(node.slice, ast.Constant) or node.slice.value != "seed"


@pytest.mark.parametrize("field",["trajectory","late_q0_pasture_day","calendar","Q0"])
def test_runtime_profile_refuses_unknown_fields(field):
    c=deepcopy(CONFIG); c[field]={}
    with pytest.raises(ValueError): Profile.from_config(c)
