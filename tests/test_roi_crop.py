"""Unit tests for ROICropAgent logic."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.state import GameState
from agricola.strategy.roi_crop import ROICropAgent


def test_roi_crop_selection():
    """Unit Test: Verify ROICropAgent selects the highest ROI crop based on capital and prices."""
    sample_obs = {
        "step": 0,
        "day": 0,
        "hour": 0,
        "player": 0,
        "remainingOverageTime": 60.0,
        "farms": [
            {"money": 3000.0, "farmer": [4, 4], "tiles": [[None]*10 for _ in range(10)]},
            {"money": 3000.0, "farmer": [4, 4], "tiles": [[None]*10 for _ in range(10)]},
        ],
        "private": {"shed": {}, "seeds": {}},
        "market": {
            "prices": {
                "WHEAT": 15.0,
                "CARROT": 35.0,
                "TOMATO": 90.0,
                "STRAWBERRY": 180.0,
                "MELON": 250.0,
            }
        },
    }

    state = GameState(sample_obs)
    agent_inst = ROICropAgent()

    # Calculate ROI for each crop given these prices
    # WHEAT: (15 * 2 - 10) / 4 = 20 / 4 = 5.0 / day
    # CARROT: (35 * 2 - 20) / 3 = 50 / 3 = 16.67 / day
    # TOMATO: (90 * 2 - 50) / 8 = 130 / 8 = 16.25 / day
    # STRAWBERRY: (180 * 2 - 100) / 10 = 260 / 10 = 26.0 / day
    # MELON: (250 * 2 - 80) / 12 = 420 / 12 = 35.0 / day

    best_crop = agent_inst.select_best_crop(state)
    # At money = 3000.0, MELON is affordable (seed = 80 <= 3000) and has highest profit per day (35.0/day)
    assert best_crop == "MELON"


def test_roi_crop_low_capital_fallback():
    """Unit Test: Verify ROICropAgent falls back to low-cost crops if capital is low."""
    sample_obs = {
        "step": 0,
        "day": 0,
        "hour": 0,
        "player": 0,
        "remainingOverageTime": 60.0,
        "farms": [
            {"money": 15.0, "farmer": [4, 4], "tiles": [[None]*10 for _ in range(10)]},
            {"money": 15.0, "farmer": [4, 4], "tiles": [[None]*10 for _ in range(10)]},
        ],
        "private": {"shed": {}, "seeds": {}},
        "market": {"prices": {"WHEAT": 15.0, "CARROT": 35.0, "MELON": 250.0}},
    }

    state = GameState(sample_obs)
    agent_inst = ROICropAgent()

    # At money = 15.0, only WHEAT (seed = 10) is affordable (CARROT=20, MELON=80)
    best_crop = agent_inst.select_best_crop(state)
    assert best_crop == "WHEAT"
