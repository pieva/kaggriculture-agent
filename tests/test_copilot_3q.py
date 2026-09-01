"""Structural and short-engine tests for Copilot's 3Q candidate."""

from __future__ import annotations

from kaggle_environments import make

from agricola.e16.policy import SHED_TILES
from agricola.strategy.copilot.three_quadrant import (
    COPILOT_3Q_ROLE_SEQUENCE,
    COPILOT_3Q_SPEC_VERSION,
    Q0_CENTRAL_PASTURES,
    Q1_CENTRAL_PASTURES,
    Q2_CENTRAL_PASTURES,
    Q2_CONCENTRIC_CROPS,
    CopilotThreeQAgent,
)


def test_copilot_3q_central_geometry_and_wage_envelope():
    assert len(COPILOT_3Q_ROLE_SEQUENCE) == 13
    pastures = (*Q0_CENTRAL_PASTURES, *Q1_CENTRAL_PASTURES, *Q2_CENTRAL_PASTURES)
    assert len(pastures) == 19
    assert len(set(pastures)) == 19
    assert not set(pastures) & set(SHED_TILES)
    assert not set(pastures) & set(Q2_CONCENTRIC_CROPS)
    assert all(x < 5 and y >= 5 for x, y in Q2_CENTRAL_PASTURES)


def test_copilot_3q_runs_a_real_engine_prefix():
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
