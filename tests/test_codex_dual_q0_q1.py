"""Focused tests for the isolated Codex V7.2 Q0+Q1 candidate."""

from __future__ import annotations

from kaggle_environments import make

from agricola.strategy.codex_dual_q0_q1 import (
    DUAL_MODEL_SPEC_VERSION,
    DUAL_ROLE_SEQUENCE,
    Q1_CROP_POSITIONS,
    Q1_PASTURE_POSITIONS,
    CodexDualQAgent,
    create_dual_agent,
    load_dual_config,
)

SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}


def test_dual_config_and_geometry_are_complete_and_disjoint():
    agent = CodexDualQAgent(load_dual_config())

    assert agent.model_spec_version == DUAL_MODEL_SPEC_VERSION
    assert len(agent.crop_positions) == 36
    assert len(agent.pasture_positions) == 12
    assert len(set(agent.crop_positions)) == 36
    assert len(set(agent.pasture_positions)) == 12
    assert not set(agent.crop_positions) & set(agent.pasture_positions)
    assert (4, 4) not in agent.crop_positions
    assert (5, 4) not in agent.crop_positions
    assert all(x >= 5 for x, _ in Q1_CROP_POSITIONS)
    assert all(x >= 5 for x, _ in Q1_PASTURE_POSITIONS)


def test_dual_role_sequence_has_independent_module_owners():
    assert len(DUAL_ROLE_SEQUENCE) == 13
    assert DUAL_ROLE_SEQUENCE[4:7] == (
        "LIVESTOCK_COW_Q0",
        "LIVESTOCK_SHEEP_Q0",
        "FERTILIZER_LOGISTICS_Q0",
    )
    assert DUAL_ROLE_SEQUENCE[10:13] == (
        "LIVESTOCK_COW_Q1",
        "LIVESTOCK_SHEEP_Q1",
        "FERTILIZER_LOGISTICS_Q1",
    )


def test_dual_real_engine_prefix_is_legal_and_fail_closed():
    agent = create_dual_agent(
        run_context={
            "run_id": "dual-q-test",
            "episode_id": "dual-q-prefix",
            "seed": 26090101,
            "opponent_id": "INERT_PASS_POLICY",
            "player_position": 0,
        }
    )
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    observations = env.reset()
    for _ in range(192):
        action = agent(observations[0].observation)
        observations = env.step([action, SAFE_PASS])
        if observations[0].status in {"DONE", "INVALID", "ERROR"}:
            break

    instance = agent.codex_dual_instance
    assert observations[0].status not in {"INVALID", "ERROR"}
    assert instance.error_count == 0
    assert instance.fallback_count == 0

