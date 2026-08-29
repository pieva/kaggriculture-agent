"""Tests for E12-X1.9 growth-first concurrent architecture."""

from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


def make_initial_state():
    tiles = [[None if x < 5 and y < 5 else "LOCKED" for x in range(10)] for y in range(10)]
    return GameState({
        "player": 0,
        "day": 0,
        "hour": 0,
        "step": 0,
        "farms": [{
            "money": 3000.0,
            "farmer": [4, 4],
            "hands": [],
            "tiles": tiles,
            "unlocked_quadrants": ["NW"],
            "hires_today": 0,
        }],
        "private": {"shed": {}, "seeds": {}, "inventories": [{}]},
        "market": {"prices": {"WHEAT": 25}},
    })


def test_x19_day1_targets_all_q0_external_tiles():
    agent = ProductiveMassROIAgent(ProductiveMassConfig(productive_core_mode="E12_GROWTH_FIRST_X19"))
    q0_external = agent._x19_q0_external_tiles()
    assert len(q0_external) == 21
    assert len(set(q0_external)) == 21
    assert set(q0_external).isdisjoint(agent.livestock_core_tiles)


def test_x19_opens_with_four_hands_and_wheat_seed_mass():
    agent = ProductiveMassROIAgent(ProductiveMassConfig(productive_core_mode="E12_GROWTH_FIRST_X19"))
    action = agent.decide(make_initial_state())
    assert action["market"].count(["HIRE"]) == 4
    assert ["BUY_SEED", "WHEAT", 24] in action["market"]
    assert action["farmer"] == ["WEST"]
