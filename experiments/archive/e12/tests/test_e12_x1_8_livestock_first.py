"""Tests for E12-X1.8 verifiable livestock-first architecture."""

from agricola.core.state import CROPS, GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


def make_state(day=0, money=3000.0, farmer=(4, 4), hands=None, tiles=None, shed=None, seeds=None):
    if hands is None:
        hands = []
    if tiles is None:
        tiles = [[None for _ in range(10)] for _ in range(10)]
    if shed is None:
        shed = {}
    if seeds is None:
        seeds = {}
    return GameState({
        "player": 0,
        "day": day,
        "hour": 0,
        "step": day * 24,
        "farms": [{
            "money": money,
            "farmer": list(farmer),
            "hands": [list(h) for h in hands],
            "tiles": tiles,
            "unlocked_quadrants": ["NW"],
            "hires_today": 0,
        }],
        "private": {"shed": shed, "seeds": seeds, "inventories": [{} for _ in range(1 + len(hands))]},
        "market": {"prices": {"WHEAT": 25, "MILK": 160, "MELON": 250, "CARROT": 35}},
    })


def test_crop_maturity_uses_first_yield_day_not_growth_fallback():
    agent = ProductiveMassROIAgent(ProductiveMassConfig(productive_core_mode="E12_LIVESTOCK_FIRST_X18"))
    wheat = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0, "watered_today": True, "yield_units": 1}
    assert CROPS["WHEAT"]["first_yield_day"] == 2
    assert agent._tile_matches_task(make_state(day=1), wheat, 1, 1, 1, "HARVEST") is False
    assert agent._tile_matches_task(make_state(day=2), wheat, 1, 1, 2, "HARVEST") is True


def test_next_land_cost_matches_engine_progression():
    agent = ProductiveMassROIAgent(ProductiveMassConfig(productive_core_mode="E12_LIVESTOCK_FIRST_X18"))
    state = make_state()
    state.my_farm["unlocked_quadrants"] = ["NW"]
    assert agent._next_land_cost(state) == 1000.0
    state.my_farm["unlocked_quadrants"] = ["NW", "NE"]
    assert agent._next_land_cost(state) == 2000.0
    state.my_farm["unlocked_quadrants"] = ["NW", "NE", "SW"]
    assert agent._next_land_cost(state) == 4000.0


def test_core_requires_four_physical_pastures():
    agent = ProductiveMassROIAgent(ProductiveMassConfig(productive_core_mode="E12_LIVESTOCK_FIRST_X18"))
    tiles = [[None for _ in range(10)] for _ in range(10)]
    for x, y in [(3, 3), (3, 4), (4, 3)]:
        tiles[y][x] = {"kind": "PASTURE"}
    state = make_state(tiles=tiles)
    assert agent._x18_phase(state) == "CORE_BUILDING"
    tiles[4][4] = {"kind": "PASTURE"}
    state = make_state(tiles=tiles)
    assert agent._x18_phase(state) == "FIRST_COW_BOOTSTRAP"


def test_crop_capacity_excludes_livestock_primary_worker():
    agent = ProductiveMassROIAgent(ProductiveMassConfig(productive_core_mode="E12_LIVESTOCK_FIRST_X18"))
    assert agent._x18_crop_workers_target("CORE_BUILDING", 0, 0, make_state()) == 0
    assert agent._x18_crop_workers_target("FEED_STABILIZATION", 0, 1, make_state()) == 1
    assert agent._x18_crop_workers_target("CROP_EXPANSION", 12, 4, make_state()) == 3


def test_x18_core_tiles_are_never_crop_candidates():
    agent = ProductiveMassROIAgent(ProductiveMassConfig(productive_core_mode="E12_LIVESTOCK_FIRST_X18"))
    core = set(agent.livestock_core_tiles)
    assert core.isdisjoint(agent._x18_feed_tiles())
    assert core.isdisjoint(agent._x18_ring_tiles())
