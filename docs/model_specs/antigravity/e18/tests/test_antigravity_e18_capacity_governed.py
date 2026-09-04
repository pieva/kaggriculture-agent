"""Unit tests and counterfactual fixtures for Antigravity E18.2 Capacity Governor."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from agricola.strategy.antigravity.antigravity_e18_capacity_governed_v2 import (
    AntigravityE18CapacityGovernedPolicy,
    create_antigravity_e18_capacity_governed_agent,
)


def _make_minimal_observation(
    *,
    day: int = 5,
    hour: int = 10,
    farmer_pos: tuple[int, int] = (4, 4),
    hands: list[tuple[int, int]] | None = None,
    tiles: list[list[Any]] | None = None,
) -> dict[str, Any]:
    if hands is None:
        hands = [(2, 2)]
    if tiles is None:
        # 10x10 empty grid
        tiles = [[None for _ in range(10)] for _ in range(10)]

    step = day * 24 + hour
    farm_p0 = {
        "farmer": list(farmer_pos),
        "hands": [list(h) for h in hands],
        "money": 3000.0,
        "tiles": tiles,
        "unlocked_quadrants": ["Q0", "Q1"],
    }
    farm_p1 = {
        "farmer": [4, 4],
        "hands": [],
        "money": 3000.0,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "unlocked_quadrants": ["Q0"],
    }
    return {
        "step": step,
        "day": day,
        "hour": hour,
        "player": 0,
        "farms": [farm_p0, farm_p1],
        "private": {
            "seeds": {"CARROT": 4, "WHEAT": 4},
            "shed": {},
            "inventories": [{}, {}],
        },
        "market": {},
    }


def test_capacity_governor_recovers_on_tile_weed():
    """Verify that an idle worker on a weed cell performs DIG without MOVE."""
    tiles = [[None for _ in range(10)] for _ in range(10)]
    # Place a weed at hand position (2, 2)
    tiles[2][2] = {"kind": "WEED"}

    obs = _make_minimal_observation(day=5, hour=10, hands=[(2, 2)], tiles=tiles)

    policy = AntigravityE18CapacityGovernedPolicy(
        run_context={"seed": 180903001, "player_position": 0}
    )
    action = policy(obs)

    # Base policy might assign farmer something else, but hand at (2, 2)
    # should be given on-tile DIG
    hands_action = action.get("hands", [[]])[0]
    assert hands_action == ["DIG"]
    assert policy.recovery_service_commands >= 1
    assert policy.recovery_breakdown["DIG"] >= 1


def test_capacity_governor_recovers_on_tile_mature_plant():
    """Verify that an idle worker on a mature harvestable crop performs HARVEST."""
    tiles = [[None for _ in range(10)] for _ in range(10)]
    # Place mature carrot at hand position (3, 3) planted day 2 (age 3)
    tiles[3][3] = {
        "kind": "PLANT",
        "crop": "CARROT",
        "planted_day": 2,
        "yield_units": 2,
        "watered_today": True,
    }

    obs = _make_minimal_observation(day=5, hour=10, hands=[(3, 3)], tiles=tiles)

    policy = AntigravityE18CapacityGovernedPolicy(
        run_context={"seed": 180903001, "player_position": 0}
    )
    action = policy(obs)

    hands_action = action.get("hands", [[]])[0]
    assert hands_action == ["HARVEST"]
    assert policy.recovery_service_commands >= 1
    assert policy.recovery_breakdown["HARVEST"] >= 1


def test_capacity_governor_recovers_on_tile_unwatered_plant():
    """Verify that an idle worker on an unwatered growing plant performs WATER."""
    tiles = [[None for _ in range(10)] for _ in range(10)]
    # Place young carrot at hand position (3, 3) planted today (age 0), not watered
    tiles[3][3] = {
        "kind": "PLANT",
        "crop": "CARROT",
        "planted_day": 5,
        "yield_units": 0,
        "watered_today": False,
    }

    obs = _make_minimal_observation(day=5, hour=10, hands=[(3, 3)], tiles=tiles)

    policy = AntigravityE18CapacityGovernedPolicy(
        run_context={"seed": 180903001, "player_position": 0}
    )
    action = policy(obs)

    hands_action = action.get("hands", [[]])[0]
    assert hands_action == ["WATER"]
    assert policy.recovery_service_commands >= 1
    assert policy.recovery_breakdown["WATER"] >= 1


def test_capacity_governor_counterfactual_toggle():
    """Verify that disabling the governor strictly reproduces base V1 action without recoveries."""
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[2][2] = {"kind": "WEED"}
    obs = _make_minimal_observation(day=5, hour=10, hands=[(2, 2)], tiles=tiles)

    # Policy with governor enabled
    policy_enabled = AntigravityE18CapacityGovernedPolicy(
        run_context={"seed": 180903001, "player_position": 0}
    )
    action_enabled = policy_enabled(obs)
    assert policy_enabled.recovery_service_commands >= 1

    # Policy with governor disabled
    cfg_disabled = deepcopy(policy_enabled.config)
    cfg_disabled["capacity_governor_enabled"] = False
    policy_disabled = AntigravityE18CapacityGovernedPolicy(
        config=cfg_disabled,
        run_context={"seed": 180903001, "player_position": 0},
    )
    action_disabled = policy_disabled(obs)
    assert policy_disabled.recovery_service_commands == 0

    # Also compare with base policy directly
    base_action = policy_enabled.base_policy(obs)
    assert action_disabled == base_action


def test_capacity_governor_terminal_passthrough():
    """Verify that on Day 28+ the governor passes through base actions untouched."""
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[2][2] = {"kind": "WEED"}
    obs = _make_minimal_observation(day=28, hour=5, hands=[(2, 2)], tiles=tiles)

    policy = AntigravityE18CapacityGovernedPolicy(
        run_context={"seed": 180903001, "player_position": 0}
    )
    action = policy(obs)
    assert policy.terminal_passthrough_batches >= 1
    base_action = policy.base_policy(obs)
    assert action == base_action


def test_factory_callable():
    """Verify factory callable exports instance and telemetry."""
    agent = create_antigravity_e18_capacity_governed_agent(
        run_context={"seed": 180903001, "player_position": 0}
    )
    assert hasattr(agent, "antigravity_e18_instance")
    assert hasattr(agent, "telemetry_snapshot")
    assert agent.candidate_id == "ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1"
    assert agent.model_spec_version == "ANTIGRAVITY-E18.2-CAPACITY-GOVERNED-V1"

    telemetry = agent.telemetry_snapshot()
    assert telemetry["candidate_id"] == "ANTIGRAVITY_E18_2_CAPACITY_GOVERNED_V1"
    assert telemetry["capacity_governor_enabled"] is True
