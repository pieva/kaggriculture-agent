"""Unit test suite for E12-X1.4 Worker Locality & Readiness-Gated Expansion."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.core.state import GameState


def test_wheat_feed_tile_priority_lock():
    """Verify feed tiles (2,3), (2,4), (1,3), (1,4), (3,1), (4,1) NEVER return CARROT or cash crop fallbacks."""
    config = ProductiveMassConfig(productive_core_mode="E12_HYBRID_STAGED_LOCALITY")
    agent = ProductiveMassROIAgent(config=config)

    feed_tile = (2, 3)
    
    # 1. When WHEAT seed is available, must return WHEAT
    v_seeds_with_wheat = {"WHEAT": 5, "CARROT": 10, "MELON": 10}
    crop = agent._select_crop_to_plant(None, day=5, tile=feed_tile, virtual_seeds=v_seeds_with_wheat)
    assert crop == "WHEAT", f"Feed tile must return WHEAT when available, got {crop}"

    # 2. When WHEAT seed is 0, MUST RETURN NONE (CARROT fallback strictly forbidden on feed tiles)
    v_seeds_no_wheat = {"WHEAT": 0, "CARROT": 10, "MELON": 10, "TOMATO": 10}
    crop_no_wheat = agent._select_crop_to_plant(None, day=5, tile=feed_tile, virtual_seeds=v_seeds_no_wheat)
    assert crop_no_wheat is None, f"Feed tile must return None when WHEAT is 0 (CARROT fallback forbidden), got {crop_no_wheat}"


def test_is_expansion_ready_policy():
    """Verify 5-factor readiness policy gates land expansion correctly without hardcoded day limits."""
    config = ProductiveMassConfig(productive_core_mode="E12_HYBRID_STAGED_LOCALITY")
    agent = ProductiveMassROIAgent(config=config)

    # Mock state with low cash ($1000) -> Should fail financial readiness (< $1500)
    class DummyStateLowCash:
        def __init__(self):
            self.day = 5
            self.money = 1000.0
            self.tiles = [[None]*10 for _ in range(10)]
        def get_tile(self, x, y):
            return None

    s_low_cash = DummyStateLowCash()
    assert agent._is_expansion_ready(s_low_cash, target_quadrant=2, cash=1000.0) is False

    # Mock state with sufficient cash ($1600) but low local saturation (only 5 crops < 12) -> Should fail
    class DummyStateLowSat:
        def __init__(self):
            self.day = 2
            self.money = 1600.0
            self.tiles = [[None]*10 for _ in range(10)]
            # 5 planted tiles
            for idx, (x, y) in enumerate([(1,1),(1,2),(2,1),(2,2),(3,1)]):
                self.tiles[y][x] = {"kind": "PLANT", "watered_today": True}
        def get_tile(self, x, y):
            return self.tiles[y][x]

    s_low_sat = DummyStateLowSat()
    assert agent._is_expansion_ready(s_low_sat, target_quadrant=2, cash=1600.0) is False

    # Mock state with high water backlog (> 2 unwatered) -> Should fail
    class DummyStateWaterBacklog:
        def __init__(self):
            self.day = 5
            self.money = 1600.0
            self.tiles = [[None]*10 for _ in range(10)]
            # 15 planted tiles, 5 unwatered
            for i in range(15):
                x, y = i % 5, i // 5
                self.tiles[y][x] = {"kind": "PLANT", "watered_today": (i >= 5)}
        def get_tile(self, x, y):
            return self.tiles[y][x]

    s_backlog = DummyStateWaterBacklog()
    assert agent._is_expansion_ready(s_backlog, target_quadrant=2, cash=1600.0) is False

    # Mock state satisfying all conditions -> Should pass (ready = True)
    class DummyStateReady:
        def __init__(self):
            self.day = 3  # Note: Day 3 (< Day 4), but ready because metrics are healthy!
            self.money = 1600.0
            self.tiles = [[None]*10 for _ in range(10)]
            # 14 planted tiles in Q0, all watered today
            coords = [(x, y) for x in range(1, 5) for y in range(1, 5)][:14]
            for (x, y) in coords:
                self.tiles[y][x] = {"kind": "PLANT", "watered_today": True}
        def get_tile(self, x, y):
            return self.tiles[y][x]

    agent.telemetry.crops_harvested = 6
    s_ready = DummyStateReady()
    assert agent._is_expansion_ready(s_ready, target_quadrant=2, cash=1600.0) is True


def test_e12_x1_4_agent_instantiation():
    """Verify E12-X1.4 agent initialization and config integrity."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_STAGED_LOCALITY",
        target_tiles_per_worker=5.0,
    )
    agent = ProductiveMassROIAgent(config=config)
    assert agent.config.productive_core_mode == "E12_HYBRID_STAGED_LOCALITY"
    assert agent.config.target_tiles_per_worker == 5.0
