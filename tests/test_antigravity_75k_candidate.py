"""Technical unit tests for the Antigravity C2 75K Dual-Quadrant Q0+Q1 candidate."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity import (
    AntigravityC2_75K_Agent,
    AntigravityC2_75K_Config,
    AntigravityDualQPolicy,
    DUAL_ROLE_SEQUENCE,
    Q1_CROP_POSITIONS,
    Q1_CROP_ZONES,
    Q1_PASTURE_POSITIONS,
    create_dual_agent,
)
from agricola.strategy.antigravity.antigravity_compact_q0 import (
    ANTIGRAVITY_CROP_POSITIONS,
    ANTIGRAVITY_CROP_ZONES,
    ANTIGRAVITY_PASTURE_POSITIONS,
)
from agricola.strategy.codex_lifecycle import CodexObservationAdapter


def _observation(
    *,
    day: int = 0,
    hour: int = 0,
    money: float = 3000.0,
    player: int = 0,
    hands: int = 0,
    positions: list[tuple[int, int]] | None = None,
    unlocked_quadrants: list[str] | None = None,
    seeds: dict[str, int] | None = None,
    shed: dict[str, int] | None = None,
    inventories: list[dict[str, int]] | None = None,
    tiles: list[list[Any]] | None = None,
) -> dict:
    step = day * 24 + hour
    quads = unlocked_quadrants or ["NW"]
    if tiles is None:
        base_tiles = []
        for y in range(10):
            row = []
            for x in range(10):
                is_nw = x < 5 and y < 5
                is_ne = x >= 5 and y < 5
                if is_nw and "NW" in quads:
                    row.append(None)
                elif is_ne and "NE" in quads:
                    row.append(None)
                else:
                    row.append("LOCKED")
            base_tiles.append(row)
    else:
        base_tiles = tiles
    unit_positions = positions or [(4, 4)] * (hands + 1)
    farm = {
        "money": money,
        "tiles": deepcopy(base_tiles),
        "farmer": list(unit_positions[0]),
        "hands": [list(position) for position in unit_positions[1:]],
        "unlocked_quadrants": quads,
        "hires_today": 0,
    }
    other_farm = deepcopy(farm)
    base_shed = {
        "WHEAT": 0,
        "CARROT": 0,
        "TOMATO": 0,
        "STRAWBERRY": 0,
        "MELON": 0,
        "EGG": 0,
        "MILK": 0,
        "WOOL": 0,
        "FERTILIZER": 0,
        "GOOSE": 0,
        "COW": 0,
        "SHEEP": 0,
    }
    base_shed.update(shed or {})
    private = {
        "shed": base_shed,
        "seeds": {"WHEAT": 0, "CARROT": 0, "TOMATO": 0, "STRAWBERRY": 0, "MELON": 0},
        "inventories": inventories or [{} for _ in range(hands + 1)],
    }
    private["seeds"].update(seeds or {})
    return {
        "step": step,
        "day": day,
        "hour": hour,
        "player": player,
        "farms": [farm, other_farm],
        "private": private,
        "market": {
            "prices": {
                "WHEAT": 25.0,
                "CARROT": 20.0,
                "TOMATO": 40.0,
                "STRAWBERRY": 180.0,
                "MELON": 450.0,
                "EGG": 20.0,
                "MILK": 200.0,
                "WOOL": 200.0,
                "FERTILIZER": 10.0,
            }
        },
    }


def _snapshot(observation: dict, *, steps: int = 720):
    return CodexObservationAdapter.parse(
        observation,
        {"episodeSteps": steps, "turnsPerDay": 24},
        fallback_turns_per_day=24,
        fallback_episode_steps=steps,
    )


def test_dual_config_and_geometry_are_complete_and_disjoint():
    """Verify geometry, crop positions, and pasture counts for Q0+Q1."""
    config = AntigravityC2_75K_Config.load()
    policy = AntigravityDualQPolicy(config)

    assert policy.model_spec_version == "ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0"
    assert len(policy.crop_positions) == 36
    assert len(policy.pasture_positions) == 12
    assert len(set(policy.crop_positions)) == 36
    assert len(set(policy.pasture_positions)) == 12
    assert not set(policy.crop_positions) & set(policy.pasture_positions)
    assert (4, 4) not in policy.crop_positions
    assert (5, 4) not in policy.crop_positions
    assert all(x < 5 and y < 5 for x, y in ANTIGRAVITY_CROP_POSITIONS)
    assert all(x >= 5 and y < 5 for x, y in Q1_CROP_POSITIONS)
    assert all(x >= 5 and y < 5 for x, y in Q1_PASTURE_POSITIONS)


def test_dual_role_sequence_has_independent_module_owners():
    """Verify that role sequence has 13 distinct roles with dedicated specialists."""
    assert len(DUAL_ROLE_SEQUENCE) == 13
    assert DUAL_ROLE_SEQUENCE[0] == "RELIEF_LOGISTICS"
    assert DUAL_ROLE_SEQUENCE[1:4] == ("CROP_ZONE_0", "CROP_ZONE_1", "CROP_ZONE_2")
    assert DUAL_ROLE_SEQUENCE[4:7] == (
        "LIVESTOCK_COW_Q0",
        "LIVESTOCK_SHEEP_Q0",
        "FERTILIZER_LOGISTICS_Q0",
    )
    assert DUAL_ROLE_SEQUENCE[7:10] == ("CROP_ZONE_3", "CROP_ZONE_4", "CROP_ZONE_5")
    assert DUAL_ROLE_SEQUENCE[10:13] == (
        "LIVESTOCK_COW_Q1",
        "LIVESTOCK_SHEEP_Q1",
        "FERTILIZER_LOGISTICS_Q1",
    )


def test_q1_admission_cashflow_gating():
    """Verify that BUY_LAND for Q1 is emitted only when within day window and cash threshold is met."""
    policy = AntigravityDualQPolicy()

    # Case 1: Day 4 (too early) -> No BUY_LAND
    obs_early = _observation(day=4, hour=0, money=4000.0, unlocked_quadrants=["NW"])
    snap_early = _snapshot(obs_early)
    orders_early = policy.decide_market_orders(snap_early)
    assert not any(o[0] == "BUY_LAND" for o in orders_early)

    # Case 2: Day 8 with low cash ($500) -> No BUY_LAND
    obs_low = _observation(day=8, hour=0, money=500.0, unlocked_quadrants=["NW"])
    snap_low = _snapshot(obs_low)
    orders_low = policy.decide_market_orders(snap_low)
    assert not any(o[0] == "BUY_LAND" for o in orders_low)

    # Case 3: Day 8 with sufficient cash ($3500) -> Emits BUY_LAND
    obs_admit = _observation(day=8, hour=0, money=3500.0, unlocked_quadrants=["NW"])
    snap_admit = _snapshot(obs_admit)
    orders_admit = policy.decide_market_orders(snap_admit)
    assert any(o[0] == "BUY_LAND" for o in orders_admit)


def test_dual_feed_owner_binding():
    """Verify feed owner bindings for Q0 and Q1 livestock specialists."""
    policy = AntigravityDualQPolicy()
    obs = _observation(day=12, hour=0, hands=12, unlocked_quadrants=["NW", "NE"])
    snap = _snapshot(obs)

    # W4 -> COW Q0
    assert policy._feed_assignments(snap, 4, "LIVESTOCK_COW_Q0") == [("Q0", "COW")]
    # W5 -> SHEEP Q0
    assert policy._feed_assignments(snap, 5, "LIVESTOCK_SHEEP_Q0") == [("Q0", "SHEEP")]
    # W10 -> COW Q1
    assert policy._feed_assignments(snap, 10, "LIVESTOCK_COW_Q1") == [("Q1", "COW")]
    # W11 -> SHEEP Q1
    assert policy._feed_assignments(snap, 11, "LIVESTOCK_SHEEP_Q1") == [("Q1", "SHEEP")]


def test_dual_real_engine_prefix_is_legal_and_fail_closed():
    """Run short match with real kaggle_environments to ensure zero runtime exceptions."""
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
        configuration={"episodeSteps": 48, "seed": 26090101, "turnsPerDay": 24},
    )
    steps = env.reset()

    for _ in range(48):
        if steps[0].status in ("DONE", "INVALID", "ERROR"):
            break
        action = agent(steps[0].observation)
        steps = env.step([action, {"farmer": ["PASS"], "hands": [], "market": []}])
        assert steps[0].status in ("ACTIVE", "DONE")
        assert agent.error_count == 0

