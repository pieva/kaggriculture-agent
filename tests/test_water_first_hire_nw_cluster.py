"""Unit tests for WaterFirstHIRENWClusterROIAgent strategy, verifying WATER > HARVEST > PLANT priority and E05 non-regression."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.state import GameState
from agricola.strategy.hire_nw_cluster_roi import HIRENWClusterROIAgent, FARMER_4_TILES, HAND1_5_TILES, ALL_9_TILES
from agricola.strategy.water_first_hire_nw_cluster_roi import WaterFirstHIRENWClusterROIAgent
from tests.test_hire_nw_cluster import create_mock_observation


def test_water_first_priority_over_harvest_and_plant():
    """Test WaterFirstHIRENWClusterROIAgent prioritizes WATER over HARVEST and PLANT when all candidates exist."""
    agent = WaterFirstHIRENWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Farmer at (4,4)
    # (4,4): Mature CARROT (HARVEST candidate) - age 3 >= max_yield_day 3
    grid[4][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": True}
    # (4,3): Growing CARROT unwatered (WATER candidate) - age 1 < max_yield_day 3
    grid[3][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 2, "watered_today": False}
    # (3,3): Empty tile (PLANT candidate)
    grid[3][3] = None

    obs = create_mock_observation(
        farmer_pos=[4, 4],
        hands=[],
        hires_today=0,
        money=3000.0,
        tiles_grid=grid,
        hour=1,
        day=3,
        seeds={"CARROT": 5},
    )
    state = GameState(obs)
    actions = agent.act(state)

    # Under Water-First, farmer at (4,4) targets (4,3) for WATER rather than harvesting (4,4) or planting (3,3)
    # Movement towards (4,3) [x=4, y=3] from (4,4) [x=4, y=4] is NORTH
    assert actions["farmer"] == ["NORTH"]


def test_harvest_second_priority_when_no_water_candidates():
    """Test WaterFirstHIRENWClusterROIAgent prioritizes HARVEST over PLANT when no WATER candidates exist."""
    agent = WaterFirstHIRENWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Farmer at (4,4)
    # (4,4): Mature CARROT (HARVEST candidate)
    grid[4][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": True}
    # (3,3): Empty tile (PLANT candidate)
    grid[3][3] = None

    obs = create_mock_observation(
        farmer_pos=[4, 4],
        hands=[],
        hires_today=0,
        money=3000.0,
        tiles_grid=grid,
        hour=1,
        day=3,
        seeds={"CARROT": 5},
    )
    state = GameState(obs)
    actions = agent.act(state)

    # Farmer at (4,4) executes HARVEST
    assert actions["farmer"] == ["HARVEST"]


def test_plant_third_priority_when_no_water_or_harvest_candidates():
    """Test WaterFirstHIRENWClusterROIAgent chooses PLANT when no WATER or HARVEST candidates exist."""
    agent = WaterFirstHIRENWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Farmer at (4,4) [Empty]
    grid[4][4] = None

    obs = create_mock_observation(
        farmer_pos=[4, 4],
        hands=[],
        hires_today=0,
        money=3000.0,
        tiles_grid=grid,
        hour=1,
        day=1,
        seeds={"CARROT": 5},
    )
    state = GameState(obs)
    actions = agent.act(state)

    # Farmer executes PLANT on best crop (MELON given 3000.0 money and market prices)
    assert actions["farmer"][0] == "PLANT"


def test_e05_priority_unmodified_retains_harvest_first():
    """Verify E05 HIRENWClusterROIAgent retains HARVEST > PLANT > WATER under identical conditions."""
    agent_e05 = HIRENWClusterROIAgent()
    grid = [[None] * 10 for _ in range(10)]

    # Farmer at (4,4)
    # (4,4): Mature CARROT (HARVEST candidate)
    grid[4][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0, "watered_today": True}
    # (4,3): Growing CARROT unwatered (WATER candidate)
    grid[3][4] = {"kind": "PLANT", "crop": "CARROT", "planted_day": 2, "watered_today": False}

    obs = create_mock_observation(
        farmer_pos=[4, 4],
        hands=[],
        hires_today=0,
        money=3000.0,
        tiles_grid=grid,
        hour=1,
        day=3,
        seeds={"CARROT": 5},
    )
    state = GameState(obs)
    actions = agent_e05.act(state)

    # E05 prioritizes HARVEST first over WATER
    assert actions["farmer"] == ["HARVEST"]


def test_water_first_invariants_and_partitioning():
    """Verify WaterFirstHIRENWClusterROIAgent preserves 4:5 spatial partitioning and HIRE behavior."""
    agent = WaterFirstHIRENWClusterROIAgent()

    # Check partition tile setup matches E05 exactly
    assert set(agent.farmer_tiles) == set(FARMER_4_TILES)
    assert set(agent.hand1_tiles) == set(HAND1_5_TILES)
    assert set(agent.all_managed_tiles) == set(ALL_9_TILES)

    grid = [[None] * 10 for _ in range(10)]
    # Populate all tiles except (3,3) in farmer partition (needs water) and (2,2) in hand partition (needs water)
    for pos in ALL_9_TILES:
        grid[pos[1]][pos[0]] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": True}

    grid[3][3] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0, "watered_today": False}
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

    # Farmer moves towards (3,3) in farmer_tiles
    assert actions["farmer"] == ["NORTH"]
    # Hand 1 waters (2,2) in hand1_tiles
    assert len(actions["hands"]) == 1
    assert actions["hands"][0] == ["WATER"]
