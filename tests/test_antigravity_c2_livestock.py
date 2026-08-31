"""Unit and integration test suite for Antigravity C2 Livestock Strategy Variant (LS1)."""

from typing import Any, Dict
from kaggle_environments import make

from agricola.strategy.antigravity_livestock import (
    AntigravityC2LivestockAgent,
    AntigravityC2LivestockConfig,
    AntigravityC2LivestockPolicy,
)


def test_antigravity_c2_livestock_config_defaults() -> None:
    """Verify default parameters of the livestock diagnostic config."""
    cfg = AntigravityC2LivestockConfig()
    assert cfg.quadrants_owned == 2
    assert cfg.crop_working_set_target == 38
    assert cfg.pasture_allocation_target == 2
    assert cfg.livestock_headcount_target == 2
    assert cfg.livestock_species == "COW"
    assert cfg.livestock_activation_day == 11
    assert cfg.workforce_headcount == 10


def test_antigravity_c2_livestock_activation_gate() -> None:
    """Verify that BUY_ANIMAL is gated until Day >= 11 with sufficient cash."""
    policy = AntigravityC2LivestockPolicy()
    
    # Day 5 with high cash: no animal orders
    obs_day5 = {
        "step": 120,
        "day": 5,
        "farms": [{"money": 15000.0, "unlocked_quadrants": ["NW", "NE"], "hires_today": 9, "tiles": [[None]*10 for _ in range(10)]}],
        "private": {"shed": {}, "seeds": {}},
    }
    orders_day5 = policy.decide_market_orders(obs_day5)
    assert not any(o[0] == "BUY_ANIMAL" for o in orders_day5)

    # Day 11 with high cash: BUY_ANIMAL COW 2 emitted
    obs_day11 = {
        "step": 264,
        "day": 11,
        "farms": [{"money": 15000.0, "unlocked_quadrants": ["NW", "NE"], "hires_today": 9, "tiles": [[None]*10 for _ in range(10)]}],
        "private": {"shed": {}, "seeds": {}},
    }
    orders_day11 = policy.decide_market_orders(obs_day11)
    animal_orders = [o for o in orders_day11 if o[0] == "BUY_ANIMAL"]
    assert len(animal_orders) == 1
    assert animal_orders[0] == ["BUY_ANIMAL", "COW", 2]


def test_antigravity_c2_livestock_agent_callable_interface() -> None:
    """Verify that AntigravityC2LivestockAgent produces compliant action dicts."""
    agent = AntigravityC2LivestockAgent()
    obs = {
        "step": 0,
        "day": 0,
        "farms": [{
            "money": 3000.0,
            "unlocked_quadrants": ["NW"],
            "hires_today": 0,
            "farmer": [4, 4],
            "hands": [],
            "tiles": [[None]*10 for _ in range(10)],
        }],
        "private": {"shed": {}, "seeds": {}},
    }
    action = agent(obs)
    assert isinstance(action, dict)
    assert "farmer" in action
    assert "hands" in action
    assert "market" in action
    assert isinstance(action["farmer"], list)
    assert isinstance(action["hands"], list)
    assert isinstance(action["market"], list)


def test_antigravity_c2_livestock_player1_support() -> None:
    """Verify that the livestock agent handles Player 1 observations correctly."""
    policy = AntigravityC2LivestockPolicy()
    obs = {
        "step": 0,
        "day": 0,
        "player": 1,
        "farms": [
            {"money": 3000.0, "unlocked_quadrants": ["NW"], "hires_today": 0, "farmer": [4, 4], "hands": [], "tiles": [[None]*10 for _ in range(10)]},
            {"money": 3000.0, "unlocked_quadrants": ["NW"], "hires_today": 0, "farmer": [4, 4], "hands": [], "tiles": [[None]*10 for _ in range(10)]},
        ],
        "private": [
            {"shed": {}, "seeds": {}},
            {"shed": {}, "seeds": {}},
        ],
    }
    orders = policy.decide_market_orders(obs, player_index=1)
    actions = policy.decide_actions(obs, player_index=1)
    assert isinstance(orders, list)
    assert isinstance(actions, list)


def test_antigravity_c2_livestock_real_engine_smoke_48_steps() -> None:
    """Verify 48 steps in real Kaggle environment with zero crashes or errors."""
    env = make("kaggriculture", configuration={"seed": 1838889274, "episodeSteps": 48})
    agent = AntigravityC2LivestockAgent()
    env.run([agent, "pass"])
    assert len(env.steps) >= 48
    final_state = env.state[0]
    assert final_state.status in ("ACTIVE", "DONE")
    assert final_state.observation.farms[0]["money"] > 0.0
