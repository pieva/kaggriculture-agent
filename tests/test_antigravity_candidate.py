"""Unit and integration tests for Antigravity Independent Strategy Agent (E14)."""

import pytest
from kaggle_environments import make

from agricola.core.state import GameState
from agricola.strategy.antigravity import AntigravityConfig, AntigravityROIAgent


def test_antigravity_initialization():
    config = AntigravityConfig()
    agent = AntigravityROIAgent(config=config)
    assert agent.config.target_quadrants == 3
    assert agent.config.max_hands == 12
    assert agent.config.target_cows == 14
    assert agent.config.target_sheep == 4


def test_antigravity_step_0_opening():
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 0})
    steps = env.reset()
    state = GameState(steps[0].observation)
    
    agent = AntigravityROIAgent()
    action = agent.act(state)
    
    assert "farmer" in action
    assert "hands" in action
    assert "market" in action
    assert len(action["market"]) <= 10
    
    # Check that day 1 opening buys animals and seeds
    market_orders = action["market"]
    order_types = [o[0] for o in market_orders]
    assert "BUY_ANIMAL" in order_types
    assert "BUY_PRODUCT" in order_types
    assert "BUY_SEED" in order_types


def test_antigravity_short_run_progression():
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 0})
    steps = env.reset()
    agent = AntigravityROIAgent()
    
    for step_idx in range(48):  # Run first 2 full days
        state = GameState(steps[0].observation)
        action = agent.act(state)
        steps = env.step([action, {}])
        assert steps[0].status == "ACTIVE"
    
    final_state = GameState(steps[0].observation)
    assert final_state.day == 2
    assert final_state.money > 0


def test_canonical_submission_standalone():
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent
    sub_dir = str(project_root / "submission")
    if sub_dir not in sys.path:
        sys.path.insert(0, sub_dir)
    import submission_antigravity
    
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 0})
    steps = env.reset()
    obs = steps[0].observation
    action = submission_antigravity.agent(obs)
    
    assert "farmer" in action
    assert "hands" in action
    assert "market" in action

