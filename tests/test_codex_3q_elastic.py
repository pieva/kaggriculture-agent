"""Focused structural and economic tests for Codex V8.0 3Q."""

from __future__ import annotations

from types import SimpleNamespace

from agricola.e16.policy import SHED_TILES
from agricola.strategy.codex_3q_elastic import (
    Q2_PASTURE_POSITIONS,
    THREE_Q_MODEL_SPEC_VERSION,
    THREE_Q_ROLE_SEQUENCE,
    CodexThreeQElasticAgent,
    load_3q_config,
)


def test_3q_config_and_geometry_are_bounded():
    config = load_3q_config()
    agent = CodexThreeQElasticAgent(config)

    assert agent.model_spec_version == THREE_Q_MODEL_SPEC_VERSION
    assert len(THREE_Q_ROLE_SEQUENCE) == 13
    assert len(agent.crop_positions) == 36
    assert len(Q2_PASTURE_POSITIONS) == 12
    assert len(set(Q2_PASTURE_POSITIONS)) == 12
    assert all(x < 5 and y >= 5 for x, y in Q2_PASTURE_POSITIONS)
    assert not set(Q2_PASTURE_POSITIONS).intersection(SHED_TILES)
    assert config["q2_incremental_hands"] == 0
    assert config["q2_livestock_targets"] == {"COW": 6, "SHEEP": 6}


def test_q0_q1_roles_are_an_exact_v7_3_prefix():
    from agricola.strategy.codex_dual_q0_q1 import DUAL_ROLE_SEQUENCE

    assert THREE_Q_ROLE_SEQUENCE[: len(DUAL_ROLE_SEQUENCE)] == DUAL_ROLE_SEQUENCE
    assert THREE_Q_ROLE_SEQUENCE == DUAL_ROLE_SEQUENCE


def test_q2_payback_ledger_uses_incremental_fibonacci_cost(monkeypatch):
    agent = CodexThreeQElasticAgent(load_3q_config())
    agent.q1_full_module_day = 11

    snapshot = SimpleNamespace(
        clock=SimpleNamespace(
            day=11,
            step=264,
            episode_steps=720,
            turns_per_day=24,
        ),
        private={"shed": {"MILK": 20}},
        market={
            "prices": {
                "MILK": 300,
                "WOOL": 300,
                "WHEAT": 25,
            }
        },
        farm={"money": 4000},
    )

    monkeypatch.setattr(agent, "animal_escapes", 0)
    monkeypatch.setattr(agent, "_positions", lambda farm: [])
    ledger = agent._q2_admission_ledger(snapshot)  # type: ignore[arg-type]

    assert ledger["available"] == 10000
    assert ledger["projected_incremental_labor_cost"] == 0
    assert ledger["projected_net"] >= 12000
    assert ledger["admitted"] is True
