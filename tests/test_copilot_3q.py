"""Structural and short-engine tests for Copilot's 3Q candidate."""

from __future__ import annotations

from kaggle_environments import make

from agricola.strategy.copilot.three_quadrant import (
    COPILOT_3Q_ROLE_SEQUENCE,
    COPILOT_3Q_SPEC_VERSION,
    CopilotThreeQAgent,
    CopilotThreeQPolicy,
    load_copilot_3q_config,
)


def test_copilot_3q_high_density_contract_is_disclosed() -> None:
    config = load_copilot_3q_config()
    assert config["model_spec_version"] == COPILOT_3Q_SPEC_VERSION
    assert config["quadrants_owned"] == 3
    assert config["workforce_total"] == 13
    assert config["feed_correction_step"] == 195
    assert len(COPILOT_3Q_ROLE_SEQUENCE) == 13
    assert CopilotThreeQPolicy.__bases__ == (object,)


def test_copilot_3q_applies_the_d8_feed_correction() -> None:
    agent = CopilotThreeQAgent()
    action = agent.policy({"step": 195})
    wheat_orders = [
        order
        for order in action["market"]
        if order[:2] == ["BUY_PRODUCT", "WHEAT"]
    ]
    assert wheat_orders == [["BUY_PRODUCT", "WHEAT", 4]]
    assert not any(order[:2] == ["BUY_ANIMAL", "COW"] for order in action["market"])


def test_copilot_3q_runs_a_real_engine_prefix() -> None:
    agent = CopilotThreeQAgent()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 72, "seed": 26090101, "turnsPerDay": 24},
    )
    steps = env.reset()
    passive = {"farmer": ["PASS"], "hands": [], "market": []}
    for _ in range(72):
        if steps[0].status != "ACTIVE":
            break
        steps = env.step([agent(steps[0].observation), passive])
        assert steps[0].status in {"ACTIVE", "DONE"}

    assert agent.policy.model_spec_version == COPILOT_3Q_SPEC_VERSION
    assert agent.policy.error_count == 0
