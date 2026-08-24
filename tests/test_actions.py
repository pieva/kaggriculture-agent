"""Unit tests for ActionBuilder functionality, focusing on movement action formatting."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.actions import ActionBuilder


def test_action_builder_movement_formatting():
    """Verify ActionBuilder.move outputs direct directional action lists expected by Kaggriculture."""
    ab = ActionBuilder()
    
    # Test short and full direction names
    assert ab.move("N").build()["farmer"] == ["NORTH"]
    assert ab.move("NORTH").build()["farmer"] == ["NORTH"]
    
    assert ab.move("S").build()["farmer"] == ["SOUTH"]
    assert ab.move("SOUTH").build()["farmer"] == ["SOUTH"]
    
    assert ab.move("E").build()["farmer"] == ["EAST"]
    assert ab.move("EAST").build()["farmer"] == ["EAST"]
    
    assert ab.move("W").build()["farmer"] == ["WEST"]
    assert ab.move("WEST").build()["farmer"] == ["WEST"]


def test_action_builder_basic_actions():
    """Verify basic farmer and market actions."""
    ab = ActionBuilder()
    assert ab.pass_turn().build()["farmer"] == ["PASS"]
    assert ab.plant("CARROT").build()["farmer"] == ["PLANT", "CARROT"]
    assert ab.water().build()["farmer"] == ["WATER"]
    assert ab.harvest().build()["farmer"] == ["HARVEST"]
    
    ab = ActionBuilder()
    ab.buy_seed("MELON", 4).sell("CARROT", 2)
    built = ab.build()
    assert built["market"] == [["BUY_SEED", "MELON", 4], ["SELL", "CARROT", 2]]
