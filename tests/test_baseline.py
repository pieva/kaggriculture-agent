"""Unit tests for baseline agent logic and short integration smoke test."""

import sys
from pathlib import Path
import pytest
import kaggle_environments

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.state import GameState
from agricola.core.actions import ActionBuilder
from agricola.baseline.carrot_loop import CarrotLoopAgent
from agricola.agent import agent


# --- UNIT TESTS ---

def test_game_state_parsing():
    """Unit Test: Verify GameState correctly parses raw observation dictionary fields."""
    sample_obs = {
        "step": 5,
        "day": 0,
        "hour": 5,
        "player": 0,
        "remainingOverageTime": 59.5,
        "farms": [
            {
                "money": 3000.0,
                "farmer": [4, 4],
                "tiles": [[None]*10 for _ in range(10)],
            },
            {
                "money": 3000.0,
                "farmer": [4, 4],
                "tiles": [[None]*10 for _ in range(10)],
            }
        ],
        "private": {"shed": {"CARROT": 2}, "seeds": {"CARROT": 0}},
        "market": {"prices": {"CARROT": 35}},
    }

    state = GameState(sample_obs)
    assert state.step == 5
    assert state.day == 0
    assert state.hour == 5
    assert state.player_id == 0
    assert state.money == 3000.0
    assert state.farmer_position == (4, 4)
    assert state.get_shed_count("CARROT") == 2
    assert state.get_seed_count("CARROT") == 0
    assert state.get_price("CARROT") == 35.0


def test_action_builder():
    """Unit Test: Verify ActionBuilder constructs valid action structure."""
    builder = ActionBuilder()
    builder.plant("CARROT")
    builder.sell("CARROT", 5)
    builder.buy_seed("CARROT", 1)

    act = builder.build()
    assert act["farmer"] == ["PLANT", "CARROT"]
    assert act["hands"] == []
    assert ["SELL", "CARROT", 5] in act["market"]
    assert ["BUY_SEED", "CARROT", 1] in act["market"]


def test_agent_action_structure():
    """Unit Test: Verify top-level agent() returns expected keys and list types."""
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
        "market": {"prices": {"CARROT": 35}},
    }

    res = agent(sample_obs)
    assert "farmer" in res
    assert "hands" in res
    assert "market" in res
    assert isinstance(res["farmer"], list)
    assert isinstance(res["market"], list)


# --- INTEGRATION SMOKE TESTS ---

def test_short_simulation_smoke():
    """Integration Smoke Test: Verify agent completes a short 48-step episode without crashing."""
    env = kaggle_environments.make("kaggriculture", configuration={"episodeSteps": 48})
    env.run([agent, "starter"])
    assert len(env.steps) == 48
    assert env.steps[-1][0]["status"] == "DONE"
