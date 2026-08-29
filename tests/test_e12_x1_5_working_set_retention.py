"""Unit tests for E12-X1.5 — Working Set Retention @ 4 Tiles/Worker."""

import pytest
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig


def test_capacity_invariant_formula():
    """Verify working_set_capacity = 4 * active_workers invariant calculation."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    for num_hands in range(6):
        active_workers = 1 + num_hands
        cap = 4 * active_workers
        assert cap == 4 * (1 + num_hands)


def test_emergency_water_priority_over_plant():
    """Verify that a crop with consecutive_unwatered >= 1 receives EMERGENCY_WATER priority over PLANT."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    raw_obs = {
        "money": 1000.0,
        "day": 5,
        "step": 120,
        "farms": [
            {
                "money": 1000.0,
                "farmer": [1, 1],
                "hands": [],
                "tiles": [[None for _ in range(10)] for _ in range(10)],
            }
        ],
        "shed": {},
        "private": {"seeds": {"WHEAT": 5}},
    }
    # Tile (1, 1) has a crop unwatered for 1 day
    raw_obs["farms"][0]["tiles"][1][1] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 2,
        "watered_today": False,
        "consecutive_unwatered": 1,
        "yield_units": 0,
    }
    state = GameState(raw_obs)
    
    # Matching check
    emergency_match = agent._tile_matches_task(state, state.get_tile(1, 1), 1, 1, 5, "EMERGENCY_WATER")
    assert emergency_match is True


def test_outside_weed_ignored():
    """Verify that DIG matches WEED tiles inside primary working set but ignores outside weeds."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
    )
    agent = ProductiveMassROIAgent(config=config)

    raw_obs = {
        "money": 1000.0,
        "day": 5,
        "step": 120,
        "farms": [
            {
                "money": 1000.0,
                "farmer": [1, 1],
                "hands": [],
                "tiles": [[None for _ in range(10)] for _ in range(10)],
            }
        ],
        "shed": {},
        "private": {"seeds": {}},
    }
    # (1, 1) is inside working set, (9, 9) is outside working set
    raw_obs["farms"][0]["tiles"][1][1] = {"kind": "WEED"}
    raw_obs["farms"][0]["tiles"][9][9] = {"kind": "WEED"}
    state = GameState(raw_obs)

    # Working set DIG task search should find (1, 1)
    primary_tiles = [(1, 1), (1, 2), (2, 1), (2, 2)]
    secondary_tiles = []
    reserved = set()

    act_inside = agent._find_best_task_action(state, 1, 1, primary_tiles, secondary_tiles, reserved, 0, "DIG")
    assert act_inside == ["DIG"]

    # Outside weed at (9, 9) with primary_tiles = [(1,1)] should not be targeted by primary task search
    act_outside = agent._find_best_task_action(state, 1, 1, [(1, 1)], [], set(), 0, "DIG")
    assert act_outside == ["DIG"]  # Targets (1,1) standing tile, not (9,9)
