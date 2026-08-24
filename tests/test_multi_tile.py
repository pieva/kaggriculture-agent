"""Unit tests for MultiTileROIAgent strategy and behavior."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.state import GameState
from agricola.strategy.multi_tile_roi import MultiTileROIAgent


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


def test_multi_tile_seed_purchasing():
    """Test seed buying scales up to number of empty managed tiles (4 tiles)."""
    agent = MultiTileROIAgent()
    # All 4 managed tiles (4,4), (4,3), (3,4), (3,3) are None (empty)
    # Owned MELON seeds = 0, money = 3000.0 (MELON seed cost = 80) -> should buy 4 MELON seeds
    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, seeds={"MELON": 0})
    state = GameState(obs)
    actions = agent.act(state)

    assert ["BUY_SEED", "MELON", 4] in actions["market"]


def test_multi_tile_priority_harvest_over_plant_and_water():
    """Test priority HARVEST > PLANT > WATER."""
    agent = MultiTileROIAgent()
    grid = [[None] * 10 for _ in range(10)]
    
    # Tile (3,3): Needs WATER (planted_day=0, age=0, watered_today=False)
    grid[3][3] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": False}
    # Tile (4,3): Ready to HARVEST (planted_day=0, age=5 >= max_yield_day 3)
    grid[3][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": True}

    # Farmer is at (4,4), day is 5
    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, tiles_grid=grid, seeds={"CARROT": 2})
    obs["day"] = 5
    state = GameState(obs)
    actions = agent.act(state)

    # Candidate HARVEST tile is (4,3). Farmer at (4,4) must move NORTH to reach (4,3).
    assert actions["farmer"] == ["NORTH"]


def test_multi_tile_nearest_tile_selection_and_tie_breaking():
    """Test nearest tile selection via Manhattan distance and deterministic tie-breaking (y, x)."""
    agent = MultiTileROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Populate managed tiles (4,4) and (3,4) with watered crops so PLANT_SET is empty
    grid[4][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": True}
    grid[4][3] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": True}

    # Two tiles need water: (4,3) at dist 1 from (4,4), and (3,3) at dist 2 from (4,4)
    grid[3][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": False}  # pos (4, 3)
    grid[3][3] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": False}  # pos (3, 3)

    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, tiles_grid=grid, seeds={"CARROT": 0})
    obs["day"] = 1
    state = GameState(obs)
    actions = agent.act(state)

    # Nearest water tile is (4,3) at dist 1. Farmer at (4,4) moves NORTH.
    assert actions["farmer"] == ["NORTH"]


def test_multi_tile_action_execution_on_current_tile():
    """Test executing HARVEST / PLANT / WATER when farmer is directly on the target tile."""
    agent = MultiTileROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # All managed tiles are planted; (4,4) needs water, others are already watered today
    grid[4][4] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": False}
    grid[3][4] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}
    grid[4][3] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}
    grid[3][3] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}

    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, tiles_grid=grid, seeds={"MELON": 0})
    obs["day"] = 1
    state = GameState(obs)
    actions = agent.act(state)

    assert actions["farmer"] == ["WATER"]


def test_multi_tile_pass_when_no_action_needed():
    """Test farmer outputs PASS when all managed tiles are fully watered and no planting/harvesting needed."""
    agent = MultiTileROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # All 4 managed tiles are watered and growing
    for x, y in [(4, 4), (4, 3), (3, 4), (3, 3)]:
        grid[y][x] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}

    obs = create_mock_observation(farmer_pos=[4, 4], money=3000.0, tiles_grid=grid, seeds={"MELON": 0})
    obs["day"] = 1
    state = GameState(obs)
    actions = agent.act(state)

    assert actions["farmer"] == ["PASS"]
