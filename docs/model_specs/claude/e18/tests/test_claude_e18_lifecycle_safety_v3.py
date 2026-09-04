"""Tests for the Claude E18.3 lifecycle-safety controller — V3.

V3 changes exactly two mechanisms in the ACTION_ARBITER layer versus V2
(module docstring items 10-11): stable worker identity (replacing a raw,
engine-reorderable list index) and a stall-timeout that also fires on a
repeated, non-progressing ``PICKUP`` (not only a literal ``PASS``). Every
other layer -- opponent snapshot, regime classifier, sticky selector, crop
KEEP/HARVEST/ROTATION_DIG lifecycle, proactive wheat buffer, crop-surface
cap, per-animal ledger and emergency queue -- is unchanged from V2, so the
lifecycle fixtures below are the same fixtures V2 already had to pass
(reproduced here, not re-derived) plus new fixtures for the two V3
mechanisms and an engine-level regression on the worst traced V2 match.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from agricola.strategy.claude.e18_lifecycle_safety_v3 import (
    DEFAULT_CONFIG_PATH,
    POLICY_VERSION,
    ClaudeE18LifecycleSafetyV3,
    _Assignment,
    _resolve_assignment,
    create_claude_e18_lifecycle_safety_v3,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_PATH = REPO_ROOT / "src" / "agricola" / "strategy" / "claude" / "e18_lifecycle_safety_v3.py"
CONFIGURATION = {
    "episodeSteps": 720,
    "turnsPerDay": 24,
    "boardSize": 10,
    "maxMarketOrdersPerTurn": 10,
    "shedCapacity": 100,
}


def _blank_farm(*, unlocked=("NW",), money=3000.0, farmer=(4, 4), hands=(), hires_today=0):
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            quadrant = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
            row.append(None if quadrant in unlocked else "LOCKED")
        tiles.append(row)
    return {
        "money": money,
        "farmer": list(farmer),
        "hands": [list(h) for h in hands],
        "tiles": tiles,
        "unlocked_quadrants": list(unlocked),
        "hires_today": hires_today,
    }


def _observation(
    *,
    step: int = 0,
    unlocked=("NW",),
    money: float = 3000.0,
    farmer=(4, 4),
    hands=(),
    shed=None,
    seeds=None,
    inventories=None,
    market_prices=None,
    hires_today=0,
    player: int = 0,
):
    farm = _blank_farm(
        unlocked=unlocked, money=money, farmer=farmer, hands=hands, hires_today=hires_today
    )
    farms = [farm, deepcopy(farm)]
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": player,
        "farms": farms,
        "private": {
            "shed": dict(shed or {}),
            "seeds": dict(seeds or {}),
            "inventories": inventories if inventories is not None else [{}],
        },
        "market": {
            "inventory": {},
            "prices": dict(
                market_prices
                or {
                    "WHEAT": 25,
                    "CARROT": 35,
                    "MELON": 250,
                    "TOMATO": 60,
                    "STRAWBERRY": 300,
                    "GOOSE": 300,
                    "COW": 400,
                    "SHEEP": 500,
                }
            ),
        },
    }


def _strawberry_tile(*, planted_day: int, current_step: int, lifespan_margin: int, yield_units: int = 0) -> dict:
    return {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "planted_day": planted_day,
        "watered_today": True,
        "consecutive_unwatered": 0,
        "yield_units": yield_units,
        "max_lifespan_step": current_step + lifespan_margin,
        "fertilized_until_day": -1,
    }


def _wheat_tile(*, planted_day: int = 0, watered: bool = True, yield_units: int = 1) -> dict:
    return {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": planted_day,
        "watered_today": watered,
        "consecutive_unwatered": 0,
        "yield_units": yield_units,
        "max_lifespan_step": 10_000,
        "fertilized_until_day": -1,
    }


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def test_factory_returns_callable_agent_with_expected_interface() -> None:
    agent = create_claude_e18_lifecycle_safety_v3()
    assert isinstance(agent, ClaudeE18LifecycleSafetyV3)
    assert agent.policy_version == POLICY_VERSION
    assert callable(agent)
    assert agent.technical_errors == 0
    action = agent(_observation(), CONFIGURATION)
    assert isinstance(action, dict)
    assert set(action) == {"farmer", "hands", "market"}


def test_factory_accepts_explicit_run_context_and_config_path() -> None:
    agent = create_claude_e18_lifecycle_safety_v3(
        run_context={"note": "unit-test"}, config_path=DEFAULT_CONFIG_PATH
    )
    assert agent.run_context == {"note": "unit-test"}
    assert agent.config.policy_id == POLICY_VERSION


# ---------------------------------------------------------------------------
# Lifecycle fixtures (unchanged from V2 -- reproduced to confirm V3 did not
# regress the layer it deliberately left untouched).
# ---------------------------------------------------------------------------


def test_late_strawberry_is_marked_for_rotation_dig_not_left_to_expire() -> None:
    """Required fixture: late Strawberry -> DIG."""

    agent = create_claude_e18_lifecycle_safety_v3()
    step = 10 * 24
    obs = _observation(step=step, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _strawberry_tile(
        planted_day=0, current_step=step, lifespan_margin=10, yield_units=0
    )
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["DIG"]


def test_strawberry_with_pending_yield_is_harvested_before_being_dug() -> None:
    agent = create_claude_e18_lifecycle_safety_v3()
    step = 10 * 24
    obs = _observation(step=step, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _strawberry_tile(
        planted_day=0, current_step=step, lifespan_margin=10, yield_units=2
    )
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["HARVEST"]


def test_wheat_is_not_harvested_at_the_first_available_unit() -> None:
    agent = create_claude_e18_lifecycle_safety_v3()
    obs = _observation(step=3 * 24, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _wheat_tile(planted_day=0, yield_units=1)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] != ["HARVEST"]


def test_wheat_is_harvested_once_it_reaches_its_yield_target() -> None:
    agent = create_claude_e18_lifecycle_safety_v3()
    obs = _observation(step=4 * 24, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _wheat_tile(planted_day=0, yield_units=4)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["HARVEST"]


# ---------------------------------------------------------------------------
# V3 item 10: stable worker identity under engine-reordered `hands`.
# ---------------------------------------------------------------------------


def test_identity_matches_same_worker_after_engine_reorders_hands_list() -> None:
    """Two hands at (1, 1) and (5, 5); next call the *engine* returns them in
    swapped list order (the exact failure mode traced in the V2 audit: a
    newly hired hand can be inserted anywhere, not only appended). The
    tracker must still recognise "the hand near (1, 1)" as the same
    identity both times -- a raw positional key would silently swap which
    key means which physical worker."""

    agent = create_claude_e18_lifecycle_safety_v3()
    keys_first = agent._track_worker_identities([(4, 4), (1, 1), (5, 5)])
    near_1_1_first = keys_first[keys_first.index("farmer") + 1] if False else None
    # positions[1] == (1, 1) -> keys_first[1] is its identity this call.
    identity_near_1_1 = keys_first[1]
    identity_near_5_5 = keys_first[2]

    # Engine reorders: same two hands, same positions, swapped list order.
    keys_second = agent._track_worker_identities([(4, 4), (5, 5), (1, 1)])
    assert keys_second[0] == "farmer"
    # The hand now at index 1 is physically the one that was at (5, 5).
    assert keys_second[1] == identity_near_5_5
    # The hand now at index 2 is physically the one that was at (1, 1).
    assert keys_second[2] == identity_near_1_1
    # Critically: the SAME assignment key must not have jumped onto a
    # different physical worker (the exact bug traced in V2).
    assert identity_near_1_1 != identity_near_5_5


def test_identity_tolerates_a_one_tile_move() -> None:
    agent = create_claude_e18_lifecycle_safety_v3()
    keys_first = agent._track_worker_identities([(4, 4), (2, 2)])
    identity = keys_first[1]
    # The worker moved one tile east -- still the same physical worker.
    keys_second = agent._track_worker_identities([(4, 4), (3, 2)])
    assert keys_second[1] == identity


def test_identity_assigns_fresh_id_to_a_newly_hired_hand() -> None:
    agent = create_claude_e18_lifecycle_safety_v3()
    keys_first = agent._track_worker_identities([(4, 4), (2, 2)])
    existing = keys_first[1]
    # A second hand is hired this call, appearing far from the first.
    keys_second = agent._track_worker_identities([(4, 4), (2, 2), (8, 8)])
    assert keys_second[1] == existing
    assert keys_second[2] not in keys_first


def test_identity_resets_at_day_rollover() -> None:
    """Hands are re-hired fresh each day (V3 audit finding): yesterday's
    identity must never be silently reused for a different physical worker
    hired today at the same tile."""

    agent = create_claude_e18_lifecycle_safety_v3()
    obs_day0 = _observation(step=0, farmer=(4, 4), hands=[(2, 2)], money=50000.0)
    agent(obs_day0, CONFIGURATION)
    assert agent._hand_identity_positions

    obs_day1 = _observation(step=24, farmer=(4, 4), hands=[], money=50000.0)
    agent(obs_day1, CONFIGURATION)
    assert agent._hand_identity_positions == {}


# ---------------------------------------------------------------------------
# V3 item 11: a repeated, non-progressing PICKUP is a stall, exactly like a
# repeated PASS.
# ---------------------------------------------------------------------------


def test_resolve_assignment_emits_pickup_when_shed_has_no_wheat() -> None:
    """`_resolve_assignment` itself is unchanged from V2 -- this documents
    the exact command V3's stall generalisation now catches: a worker at
    the shed, assigned to feed an animal, with nothing to pick up."""

    agent = create_claude_e18_lifecycle_safety_v3()
    cfg = agent.config
    profile = agent._current_profile()
    obs = _observation(step=0, farmer=(4, 4), shed={"WHEAT": 0}, money=50000.0)
    from agricola.core.observation_contract import CodexObservationAdapter

    snap = CodexObservationAdapter.parse(
        obs, CONFIGURATION, fallback_turns_per_day=24, fallback_episode_steps=720
    )
    feat = None
    from agricola.strategy.claude.e18_lifecycle_safety_v3 import _extract_features

    feat = _extract_features(cfg, profile, snap)
    assignment = _Assignment(kind="FEED_NEEDED", target=(6, 4))
    command = _resolve_assignment((4, 4), {}, assignment, cfg, profile, feat)
    assert command == ["PICKUP", "WHEAT", 1]


def test_stuck_pickup_assignment_times_out_like_a_stuck_pass() -> None:
    """End-to-end via `_decide`: a farmer standing at the shed, assigned to
    feed an animal, with the shed permanently out of WHEAT (nothing this
    controller does can conjure feed that was never bought -- the scenario
    V2's own emergency queue could not resolve because the assignment never
    let go). After `assignment_stall_timeout` (3) identical, non-progressing
    calls, V3 must drop the assignment instead of retrying it forever."""

    agent = create_claude_e18_lifecycle_safety_v3()
    timeout = agent.config.assignment_stall_timeout
    obs = _observation(
        step=0,
        farmer=(4, 4),
        shed={"WHEAT": 0},
        money=50000.0,
    )
    obs["farms"][0]["tiles"][4][6] = {"kind": "PASTURE", "animal": "SHEEP", "fed_today": False, "consecutive_unfed": 1}

    commands = []
    stalled_after = []
    for _ in range(timeout + 2):
        action = agent(obs, CONFIGURATION)
        commands.append(tuple(action["farmer"]))
        assignment = agent._assignments.get("farmer")
        stalled_after.append(assignment.stalled_steps if assignment is not None else None)

    # Every call while stuck must be the same non-progressing PICKUP: with
    # no other opportunity in this fixture, FEED_NEEDED (6, 4) is the only
    # candidate, so the worker keeps re-picking it after each timeout --
    # V3's guarantee is not "give up forever" (there is nothing better to
    # do here), it is "the stall counter must actually reach the timeout
    # and reset instead of staying at 0 forever like V1/V2's PASS-only
    # check did for a repeated PICKUP".
    assert all(command == ("PICKUP", "WHEAT", 1) for command in commands)
    assert max(s for s in stalled_after if s is not None) >= timeout - 1
    # The assignment must have been popped at least once (a `None` reading
    # right after a call), proving `assignment_stall_timeout` was actually
    # reached and acted on -- not merely counted up and ignored forever,
    # which is exactly what V1/V2's PASS-only stall check did for a
    # repeated PICKUP (module docstring item 11).
    assert None in stalled_after


# ---------------------------------------------------------------------------
# Engine-level regression: the worst V2 loss match, replayed under V3.
# ---------------------------------------------------------------------------


def test_v3_eliminates_losses_on_the_worst_traced_v2_match() -> None:
    """Seed 180903002, seat 0 vs Copilot E18.2: V2 lost 4 verified animals
    in this exact match (E18_CLAUDE_COPILOT_ANTIGRAVITY_TOURNAMENT_V1.json).
    V3 must not regress it back above zero."""

    from kaggle_environments import make

    from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
        create_copilot_e18_opponent_reactive_v2,
    )
    from experiments.e18.tools.common import (
        run_e18_dynamic_architecture_tournament_v1 as prior,
    )

    seed = 180903002
    ctx0 = {"run_id": "v3-regression", "episode_id": "v3-regression", "seed": seed, "player_position": 0}
    ctx1 = {"run_id": "v3-regression", "episode_id": "v3-regression", "seed": seed, "player_position": 1}
    policy0 = create_claude_e18_lifecycle_safety_v3(run_context=ctx0)
    policy1 = create_copilot_e18_opponent_reactive_v2(run_context=ctx1)

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])

    assert policy0.technical_errors == 0
    assert prior._verified_livestock_losses(env, 0) == 0
