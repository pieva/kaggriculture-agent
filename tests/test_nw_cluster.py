"""Unit tests for NWClusterROIAgent strategy and behavior."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.state import GameState
from agricola.strategy.nw_cluster_roi import NWClusterROIAgent, DEFAULT_NW_9_TILES


def create_mock_observation(
    farmer_pos=[4, 4],
    money=3000.0,
    tiles_grid=None,
    shed=None,
    seeds=None,
    prices=None,
):
    """Helper to build custom test GameState observation dictionaries."""
    if tiles_grid is None:
        tiles_grid = [[None] * 10 for _ in range(10)]
    if shed is None:
        shed = {}
    if seeds is None:
        seeds = {}
    if prices is None:
        prices = {"WHEAT": 25.0, "CARROT": 35.0, "TOMATO": 60.0, "STRAWBERRY": 120.0, "MELON": 250.0}

    return {
        "step": 0,
        "day": 0,
        "hour": 0,
        "player": 0,
        "remainingOverageTime": 60.0,
        "farms": [
            {"money": money, "farmer": farmer_pos, "tiles": tiles_grid},
            {"money": money, "farmer": [4, 4], "tiles": [[None] * 10 for _ in range(10)]},
        ],
        "private": {"shed": shed, "seeds": seeds},
        "market": {"prices": prices, "inventory": {}},
    }


def test_nw_cluster_tile_count():
    """Test NWClusterROIAgent manages exactly 9 tiles."""
    agent = NWClusterROIAgent()
    assert len(agent.managed_tiles) == 9
    assert set(agent.managed_tiles) == set(DEFAULT_NW_9_TILES)


def test_nw_cluster_seed_purchasing():
    """Test seed buying scales up to number of empty managed tiles (9 tiles)."""
    agent = NWClusterROIAgent()
    # All 9 managed tiles are None (empty)
    # Owned MELON seeds = 0, money = 3000.0 (MELON seed cost = 80) -> should buy 9 MELON seeds
    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, seeds={"MELON": 0})
    state = GameState(obs)
    actions = agent.act(state)

    assert ["BUY_SEED", "MELON", 9] in actions["market"]


def test_nw_cluster_priority_harvest_over_plant_and_water():
    """Test priority HARVEST > PLANT > WATER on 9-tile cluster."""
    agent = NWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Tile (2,2): Needs WATER (planted_day=0, age=0, watered_today=False)
    grid[2][2] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": False}
    # Tile (2,4): Ready to HARVEST (planted_day=0, age=5 >= max_yield_day 3)
    grid[4][2] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": True}

    # Farmer is at (4,4), day is 5
    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, tiles_grid=grid, seeds={"CARROT": 2})
    obs["day"] = 5
    state = GameState(obs)
    actions = agent.act(state)

    # Candidate HARVEST tile is (2,4) [grid[4][2]]. Farmer at (4,4) moves WEST towards (2,4).
    assert actions["farmer"] == ["WEST"]


def test_nw_cluster_action_execution_on_current_tile():
    """Test executing WATER when farmer is on current target tile."""
    agent = NWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # All 9 managed tiles planted; (4,4) needs water, others watered
    for pos in DEFAULT_NW_9_TILES:
        grid[pos[1]][pos[0]] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}
    grid[4][4] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": False}

    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, tiles_grid=grid, seeds={"MELON": 0})
    obs["day"] = 1
    state = GameState(obs)
    actions = agent.act(state)

    assert actions["farmer"] == ["WATER"]


def test_nw_cluster_pass_when_all_watered():
    """Test farmer outputs PASS when all 9 managed tiles are fully watered."""
    agent = NWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    for pos in DEFAULT_NW_9_TILES:
        grid[pos[1]][pos[0]] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}

    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, tiles_grid=grid, seeds={"MELON": 0})
    obs["day"] = 1
    state = GameState(obs)
    actions = agent.act(state)

    assert actions["farmer"] == ["PASS"]
