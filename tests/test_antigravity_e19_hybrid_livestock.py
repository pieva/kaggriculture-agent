"""Unit, behavioral, and simulation tests for Antigravity E19.1 Hybrid Livestock V1."""

from __future__ import annotations

from typing import Any
import pytest
from kaggle_environments import make

from agricola.strategy.antigravity.antigravity_e19_hybrid_livestock_v1 import (
    AntigravityE19HybridLivestockPolicy,
    create_antigravity_e19_agent,
    POLICY_VERSION,
    CANDIDATE_ID,
)


def _mock_obs(
    *,
    day: int = 5,
    hour: int = 10,
    farmer_pos: tuple[int, int] = (4, 4),
    hands: list[tuple[int, int]] | None = None,
    tiles: list[list[Any]] | None = None,
    money: float = 3000.0,
    shed: dict[str, int] | None = None,
    seeds: dict[str, int] | None = None,
    inventories: list[dict[str, int]] | None = None,
    unlocked_quadrants: list[str] | None = None,
) -> dict[str, Any]:
    if hands is None:
        hands = [(2, 2)]
    if tiles is None:
        tiles = [[None for _ in range(10)] for _ in range(10)]
    if shed is None:
        shed = {}
    if seeds is None:
        seeds = {"WHEAT": 8, "CARROT": 6, "MELON": 4}
    if inventories is None:
        inventories = [{} for _ in range(1 + len(hands))]
    if unlocked_quadrants is None:
        unlocked_quadrants = ["Q0", "Q1"]

    step = day * 24 + hour
    farm_p0 = {
        "farmer": list(farmer_pos),
        "hands": [list(h) for h in hands],
        "money": money,
        "tiles": tiles,
        "unlocked_quadrants": unlocked_quadrants,
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
            "seeds": seeds,
            "shed": shed,
            "inventories": inventories,
        },
        "market": {},
    }


def test_antigravity_e19_policy_initialization():
    policy = AntigravityE19HybridLivestockPolicy()
    assert policy.candidate_id == CANDIDATE_ID
    assert policy.model_spec_version == POLICY_VERSION
    assert policy.target_cows == 4
    assert policy.target_sheep == 2
    assert policy.cash_reserve == 300.0
    assert (3, 3) in policy.pasture_cluster_q0
    assert (5, 4) in policy.pasture_cluster_q1


def test_farmer_pasture_building_and_placement():
    policy = AntigravityE19HybridLivestockPolicy()
    tiles = [[None for _ in range(10)] for _ in range(10)]

    # 1. Farmer at (3, 3) should execute BUILD_PASTURE because (3, 3) is in pasture cluster
    obs = _mock_obs(day=2, hour=1, farmer_pos=(3, 3), hands=[], tiles=tiles)
    action = policy(obs)
    assert action["farmer"] == ["BUILD_PASTURE"]

    # 2. When pasture is built and Farmer carries a COW, Farmer standing on (3, 3) executes PLACE COW
    tiles[3][3] = {"kind": "PASTURE"}
    obs2 = _mock_obs(
        day=6,
        hour=2,
        farmer_pos=(3, 3),
        hands=[],
        tiles=tiles,
        inventories=[{"COW": 1}],
    )
    action2 = policy(obs2)
    assert action2["farmer"] == ["PLACE", "COW"]


def test_zero_escape_feeding_protocol():
    policy = AntigravityE19HybridLivestockPolicy()
    tiles = [[None for _ in range(10)] for _ in range(10)]
    # Unfed cow at (3, 3)
    tiles[3][3] = {
        "kind": "PASTURE",
        "animal": "COW",
        "fed_today": False,
        "yield_units": 0,
    }

    # Worker 1 (hand 0) at (3, 3) with WHEAT in inventory should FEED
    obs = _mock_obs(
        day=6,
        hour=5,
        farmer_pos=(4, 4),
        hands=[(3, 3)],
        tiles=tiles,
        inventories=[{}, {"WHEAT": 2}],
    )
    action = policy(obs)
    assert action["hands"][0] == ["FEED"]


def test_on_tile_capacity_governor_hybrid():
    policy = AntigravityE19HybridLivestockPolicy()
    tiles = [[None for _ in range(10)] for _ in range(10)]
    # Unwatered plant on hand's current tile (2, 2)
    tiles[2][2] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 5,
        "yield_units": 0,
        "watered_today": False,
    }
    farm = {"tiles": tiles}
    private = {"inventories": [{}, {}]}

    # Hand at (2, 2) was given "NORTH" (in MOVE_OPCODES) by dispatcher,
    # but on-tile governor intercepts and performs WATER locally!
    f_act, h_acts = policy._apply_capacity_governor(
        farmer_action=["PASS"],
        hands_actions=[["NORTH"]],
        farmer_pos=(4, 4),
        hand_positions=[(2, 2)],
        farm=farm,
        private=private,
        day=6,
    )
    assert h_acts[0] == ["WATER"]
    assert policy.recovery_service_commands == 1
    assert policy.recovery_breakdown["WATER"] == 1


def test_market_orders_capital_reserve_protection():
    policy = AntigravityE19HybridLivestockPolicy()
    # Money is $250, below the $300 cash reserve floor
    obs = _mock_obs(day=5, hour=0, money=250.0)
    action = policy(obs)

    market_orders = action.get("market", [])
    # No HIRE or BUY_LAND when below reserve
    assert not any(o[0] == "HIRE" for o in market_orders)
    assert not any(o[0] == "BUY_LAND" for o in market_orders)
    assert not any(o[0] == "BUY_ANIMAL" for o in market_orders)


def test_antigravity_e19_simulation_smoke():
    agent = create_antigravity_e19_agent(
        run_context={"run_id": "test-e19", "episode_id": "smoke", "seed": 42}
    )
    env = make("kaggriculture", configuration={"episodeSteps": 48, "seed": 42})
    observations = env.reset()

    for _ in range(47):
        action = agent(observations[0].observation)
        assert set(action) == {"farmer", "hands", "market"}
        observations = env.step(
            [action, {"farmer": ["PASS"], "hands": [], "market": []}]
        )
        if observations[0].status != "ACTIVE":
            break

    policy_instance = agent.policy_instance
    assert policy_instance.error_count == 0
    assert policy_instance.fallback_count == 0
