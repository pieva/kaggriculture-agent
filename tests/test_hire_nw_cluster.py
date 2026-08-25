"""Unit tests for HIRENWClusterROIAgent strategy, state hand support, and actions."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.state import GameState
from agricola.core.actions import ActionBuilder
from agricola.strategy.hire_nw_cluster_roi import (
    HIRENWClusterROIAgent,
    FARMER_4_TILES,
    HAND1_5_TILES,
    ALL_9_TILES,
)


def create_mock_observation(
    farmer_pos=[4, 4],
    hands=None,
    hires_today=0,
    money=3000.0,
    tiles_grid=None,
    shed=None,
    seeds=None,
    prices=None,
    hour=0,
    day=0,
):
    """Helper to build custom test GameState observation dictionaries with hand support."""
    if hands is None:
        hands = []
    if tiles_grid is None:
        tiles_grid = [[None] * 10 for _ in range(10)]
    if shed is None:
        shed = {}
    if seeds is None:
        seeds = {}
    if prices is None:
        prices = {"WHEAT": 25.0, "CARROT": 35.0, "TOMATO": 60.0, "STRAWBERRY": 120.0, "MELON": 250.0}

    return {
        "step": day * 24 + hour,
        "day": day,
        "hour": hour,
        "player": 0,
        "remainingOverageTime": 60.0,
        "farms": [
            {
                "money": money,
                "farmer": farmer_pos,
                "hands": hands,
                "hires_today": hires_today,
                "tiles": tiles_grid,
            },
            {
                "money": money,
                "farmer": [4, 4],
                "hands": [],
                "hires_today": 0,
                "tiles": [[None] * 10 for _ in range(10)],
            },
        ],
        "private": {"shed": shed, "seeds": seeds},
        "market": {"prices": prices, "inventory": {}},
    }


def test_game_state_hands_properties():
    """Test hands_positions and hires_today in GameState."""
    obs = create_mock_observation(hands=[[4, 4], [5, 4]], hires_today=2)
    state = GameState(obs)
    assert state.hands_positions == [(4, 4), (5, 4)]
    assert state.hires_today == 2


def test_action_builder_hire_and_hands():
    """Test ActionBuilder hire and add_hand_action methods."""
    builder = ActionBuilder()
    builder.hire()
    builder.add_hand_action(["WATER"])
    built = builder.build()

    assert built["market"] == [["HIRE"]]
    assert built["hands"] == [["WATER"]]


def test_hire_agent_emits_hire_on_hour_zero():
    """Test HIRENWClusterROIAgent emits HIRE on hour == 0 if no hands active today."""
    agent = HIRENWClusterROIAgent()
    obs = create_mock_observation(hour=0, hands=[], hires_today=0)
    state = GameState(obs)
    actions = agent.act(state)

    assert ["HIRE"] in actions["market"]


def test_hire_agent_no_duplicate_hire_if_already_hired():
    """Test HIRENWClusterROIAgent does not emit HIRE if hires_today > 0."""
    agent = HIRENWClusterROIAgent()
    obs = create_mock_observation(hour=0, hands=[[4, 4]], hires_today=1)
    state = GameState(obs)
    actions = agent.act(state)

    assert ["HIRE"] not in actions["market"]


def test_hire_agent_spatial_partitioning_farmer_and_hand():
    """Test Farmer operates on farmer_tiles and Hand 1 operates on hand1_tiles."""
    agent = HIRENWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Populate all tiles in cluster except (3,3) and (2,2) with watered crops so empty_tiles is []
    for pos in ALL_9_TILES:
        grid[pos[1]][pos[0]] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}

    # Farmer tile (3,3) in farmer_tiles needs WATER
    grid[3][3] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": False}
    # Hand tile (2,2) in hand1_tiles needs WATER
    grid[2][2] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": False}

    obs = create_mock_observation(
        farmer_pos=[4, 4],
        hands=[[2, 2]],
        hires_today=1,
        tiles_grid=grid,
        hour=1,
        day=1,
        seeds={"MELON": 0},
    )
    state = GameState(obs)
    actions = agent.act(state)

    # Farmer is at (4,4), nearest water in farmer_tiles is (3,3). Farmer moves NORTH towards (3,3).
    assert actions["farmer"] == ["NORTH"]
    # Hand 1 is at (2,2), direct match for water in hand1_tiles -> Hand 1 executes WATER
    assert len(actions["hands"]) == 1
    assert actions["hands"][0] == ["WATER"]


def test_hire_agent_seed_protection_prevents_unbacked_plant():
    """Test shared seed reservation prevents workers from issuing double PLANT when seeds = 1 and money = 0."""
    agent = HIRENWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Farmer at (4,4) [empty, in farmer_tiles]
    # Hand 1 at (2,2) [empty, in hand1_tiles]
    # Only 1 CARROT seed available in stock, 0 money to buy more seeds (select_best_crop defaults to CARROT)
    obs = create_mock_observation(
        farmer_pos=[4, 4],
        hands=[[2, 2]],
        hires_today=1,
        money=0.0,
        tiles_grid=grid,
        hour=1,
        day=1,
        seeds={"CARROT": 1},
    )
    state = GameState(obs)
    actions = agent.act(state)

    # Farmer gets the 1 seed and plants CARROT
    assert actions["farmer"] == ["PLANT", "CARROT"]
    # Hand 1 has 0 seeds remaining, so Hand 1 cannot plant CARROT and PASSes
    assert len(actions["hands"]) == 1
    assert actions["hands"][0] == ["PASS"]
