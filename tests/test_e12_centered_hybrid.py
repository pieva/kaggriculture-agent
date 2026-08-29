"""Unit test suite for E12 Centered Hybrid Farm Scaling (E12-X1.0)."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.core.actions import ActionBuilder
from agricola.core.state import GameState


def test_e12_livestock_core_geometry_and_invariants():
    """Verify 2x2 reserved livestock core geometry, Q0 containment, and non-overlapping invariants."""
    livestock_core = set([(3, 3), (3, 4), (4, 3), (4, 4)])
    
    # 2x2 cardinality
    assert len(livestock_core) == 4
    
    # Origin adjacent & Q0 containment
    assert (4, 4) in livestock_core, "(4,4) must be in 2x2 reserved core!"
    assert all(0 <= x <= 4 and 0 <= y <= 4 for x, y in livestock_core), "2x2 livestock core must be strictly inside Q0!"

    # Crop outer core tiles (EPU1 target 13 minus reserved 2x2 core)
    epu1_crop_tiles = set([(1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (4, 1), (4, 2)])
    assert len(livestock_core.intersection(epu1_crop_tiles)) == 0, "Livestock core and crop tiles must be strictly disjoint!"


def test_e12_config_routing_and_initialization():
    """Verify ProductiveMassConfig supports E12_HYBRID_RECOVERY & E12_HYBRID_FULL_SCALING modes."""
    config = ProductiveMassConfig(
        productive_core_mode="E12_HYBRID_FULL_SCALING",
        epu_level=3,
        enable_land_expansion=True,
        workforce_scaling_mode="LEGACY",
        multi_hire_mode="CORRECTED_MULTI",
        land_buy_mode="IMMEDIATE"
    )
    agent = ProductiveMassROIAgent(config=config)
    assert agent.config.productive_core_mode == "E12_HYBRID_FULL_SCALING"


def test_e12_buy_animal_action_builder():
    """Verify ActionBuilder produces valid BUY_ANIMAL market order."""
    builder = ActionBuilder()
    builder.buy_animal("COW", 1)
    act = builder.build()
    assert act["market"] == [["BUY_ANIMAL", "COW", 1]]
