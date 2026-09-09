"""Tests for the Claude E18.5 wheat-market-fix controller -- V5.

V5 changes exactly one line versus V4: `_wheat_stock_orders` now emits
`["BUY_PRODUCT", "WHEAT", qty]` instead of the invalid `["BUY_WHEAT", qty]`
the engine's `_parse_order` has always silently discarded (module
docstring of e18_wheat_market_fix_v5.py has the full evidence chain).
Everything else -- worker dispatch, stall handling, crop lifecycle,
livestock ledger, the V4 growth-capacity gate -- is unchanged from V4, so
this file reproduces the load-bearing V4 fixtures (to confirm no
regression on the layers V5 deliberately left untouched) plus new fixtures
for the fixed wheat order verb and a real-engine check that the order is
now actually accepted and executed.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from agricola.core.observation_contract import CodexObservationAdapter
from agricola.strategy.claude.e18_wheat_market_fix_v5 import (
    DEFAULT_CONFIG_PATH,
    POLICY_VERSION,
    ClaudeE18WheatMarketFixV5,
    _Assignment,
    _Features,
    _animal_orders,
    _expansion_guard,
    _extract_features,
    _growth_capacity_available,
    _hire_orders,
    _resolve_assignment,
    _seed_orders,
    _wheat_stock_orders,
    create_claude_e18_wheat_market_fix_v5,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_PATH = REPO_ROOT / "src" / "agricola" / "strategy" / "claude" / "e18_wheat_market_fix_v5.py"
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


def _base_features(**overrides) -> _Features:
    """Directly-constructed `_Features` for unit-testing the market-order
    and admission functions without going through a full observation."""

    defaults = dict(
        board_size=10,
        day=10,
        days_remaining=19,
        current_step=10 * 24,
        turns_per_day=24,
        worker_positions=[(4, 4), (5, 4), (6, 4)],
        worker_inventories=[{}, {}, {}],
        shed={},
        seeds={},
        money=50000.0,
        market_prices={},
        unlocked_quadrants=["NW"],
        hires_today=0,
        opportunities=[],
        plant_tiles_count=5,
        care_due_count=0,
        crop_mix_counts={},
        animal_headcount=0,
        unfed_animal_count=0,
        at_risk_animal_count=0,
        structures_total=1,
        empty_structure_type_counts={"COOP": 0, "PASTURE": 1},
        has_empty_crop_zone_tile=True,
        core_quadrant_fill_ratio=0.5,
        seed_budget={},
        crop_mix_running={},
        in_shutdown=False,
        in_liquidation=False,
        service_pressure=0.0,
        rotation_dig_count=0,
        harvest_deferred_count=0,
        animals_at_risk=False,
        serviceable_crop_capacity=10,
        growth_capacity_available=True,
    )
    defaults.update(overrides)
    return _Features(**defaults)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def test_factory_returns_callable_agent_with_expected_interface() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    assert isinstance(agent, ClaudeE18WheatMarketFixV5)
    assert agent.policy_version == POLICY_VERSION
    assert callable(agent)
    assert agent.technical_errors == 0
    action = agent(_observation(), CONFIGURATION)
    assert isinstance(action, dict)
    assert set(action) == {"farmer", "hands", "market"}


def test_factory_accepts_explicit_run_context_and_config_path() -> None:
    agent = create_claude_e18_wheat_market_fix_v5(
        run_context={"note": "unit-test"}, config_path=DEFAULT_CONFIG_PATH
    )
    assert agent.run_context == {"note": "unit-test"}
    assert agent.config.policy_id == POLICY_VERSION


# ---------------------------------------------------------------------------
# Lifecycle fixtures (unchanged from V3 -- reproduced to confirm V4 did not
# regress the layer it deliberately left untouched).
# ---------------------------------------------------------------------------


def test_late_strawberry_is_marked_for_rotation_dig_not_left_to_expire() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    step = 10 * 24
    obs = _observation(step=step, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _strawberry_tile(
        planted_day=0, current_step=step, lifespan_margin=10, yield_units=0
    )
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["DIG"]


def test_strawberry_with_pending_yield_is_harvested_before_being_dug() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    step = 10 * 24
    obs = _observation(step=step, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _strawberry_tile(
        planted_day=0, current_step=step, lifespan_margin=10, yield_units=2
    )
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["HARVEST"]


def test_wheat_is_not_harvested_at_the_first_available_unit() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    obs = _observation(step=3 * 24, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _wheat_tile(planted_day=0, yield_units=1)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] != ["HARVEST"]


def test_wheat_is_harvested_once_it_reaches_its_yield_target() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    obs = _observation(step=4 * 24, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _wheat_tile(planted_day=0, yield_units=4)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["HARVEST"]


def test_identity_matches_same_worker_after_engine_reorders_hands_list() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    keys_first = agent._track_worker_identities([(4, 4), (1, 1), (5, 5)])
    identity_near_1_1 = keys_first[1]
    identity_near_5_5 = keys_first[2]
    keys_second = agent._track_worker_identities([(4, 4), (5, 5), (1, 1)])
    assert keys_second[0] == "farmer"
    assert keys_second[1] == identity_near_5_5
    assert keys_second[2] == identity_near_1_1
    assert identity_near_1_1 != identity_near_5_5


def test_identity_resets_at_day_rollover() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    obs_day0 = _observation(step=0, farmer=(4, 4), hands=[(2, 2)], money=50000.0)
    agent(obs_day0, CONFIGURATION)
    assert agent._hand_identity_positions

    obs_day1 = _observation(step=24, farmer=(4, 4), hands=[], money=50000.0)
    agent(obs_day1, CONFIGURATION)
    assert agent._hand_identity_positions == {}


def test_stuck_pickup_assignment_times_out_like_a_stuck_pass() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    timeout = agent.config.assignment_stall_timeout
    obs = _observation(step=0, farmer=(4, 4), shed={"WHEAT": 0}, money=50000.0)
    obs["farms"][0]["tiles"][4][6] = {
        "kind": "PASTURE",
        "animal": "SHEEP",
        "fed_today": False,
        "consecutive_unfed": 1,
    }

    commands = []
    stalled_after = []
    for _ in range(timeout + 2):
        action = agent(obs, CONFIGURATION)
        commands.append(tuple(action["farmer"]))
        assignment = agent._assignments.get("farmer")
        stalled_after.append(assignment.stalled_steps if assignment is not None else None)

    assert all(command == ("PICKUP", "WHEAT", 1) for command in commands)
    assert max(s for s in stalled_after if s is not None) >= timeout - 1
    assert None in stalled_after


# ---------------------------------------------------------------------------
# V4: `_growth_capacity_available` as a pure function.
# ---------------------------------------------------------------------------


def test_growth_capacity_available_when_budget_comfortably_exceeds_backlog() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    # 3 workers, start of day (24 steps left each): ample budget for a
    # couple of unwatered tiles.
    opportunities = [{"priority": 1}, {"priority": 1}]
    assert _growth_capacity_available(cfg, 3, 24, current_step=0, opportunities=opportunities)


def test_growth_capacity_denied_when_backlog_exceeds_remaining_budget() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    # Same worker/backlog shape, but only 2 steps left this day: the
    # committed cost of the backlog alone exceeds what is left.
    opportunities = [{"priority": 1}, {"priority": 2}, {"priority": 1}]
    assert not _growth_capacity_available(cfg, 1, 24, current_step=22, opportunities=opportunities)


def test_growth_capacity_denied_purely_by_end_of_day_safety_margin() -> None:
    """Even with an EMPTY backlog, a lone worker one step from EOD cannot
    absorb the safety margin -- growth stays withheld through the last
    stretch of every day by construction, not only when tiles are already
    unwatered."""

    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    assert not _growth_capacity_available(cfg, 1, 24, current_step=23, opportunities=[])


def test_growth_capacity_ignores_non_critical_opportunities() -> None:
    """HARVEST_READY (priority 4) and PLANT_OPPORTUNITY (priority 10) do
    not count as committed cost -- only URGENT_WATER/FEED_NEEDED
    (priority <= CRITICAL_PRIORITY_CEILING) do."""

    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    opportunities = [{"priority": 4}, {"priority": 10}, {"priority": 9}]
    assert _growth_capacity_available(cfg, 2, 24, current_step=20, opportunities=opportunities)


# ---------------------------------------------------------------------------
# V4: the gate wired into `_expansion_guard` and `_animal_orders`.
# ---------------------------------------------------------------------------


def test_expansion_guard_blocked_when_growth_capacity_denied_even_if_everything_else_passes() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = cfg.regime_low
    feat = _base_features(growth_capacity_available=False)
    assert _expansion_guard(cfg, profile, feat, core_harvest_requests=10) is False


def test_expansion_guard_allowed_when_growth_capacity_available_and_everything_else_passes() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = cfg.regime_low
    feat = _base_features(growth_capacity_available=True)
    assert _expansion_guard(cfg, profile, feat, core_harvest_requests=10) is True


def test_animal_orders_blocked_when_growth_capacity_denied() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = cfg.regime_low
    feat = _base_features(
        growth_capacity_available=False,
        structures_total=1,
        empty_structure_type_counts={"COOP": 0, "PASTURE": 1},
        shed={"WHEAT": 10},
    )
    orders, _ = _animal_orders(cfg, profile, feat, feat.money, room_left=10, core_harvest_requests=10)
    assert orders == []


def test_animal_orders_allowed_when_growth_capacity_available() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = cfg.regime_low
    feat = _base_features(
        growth_capacity_available=True,
        structures_total=1,
        empty_structure_type_counts={"COOP": 0, "PASTURE": 1},
        shed={"WHEAT": 10},
    )
    orders, _ = _animal_orders(cfg, profile, feat, feat.money, room_left=10, core_harvest_requests=10)
    assert orders and orders[0][0] == "BUY_ANIMAL"


# ---------------------------------------------------------------------------
# V4: HIRE / BUY_SEED / BUY_WHEAT are deliberately exempt from the gate.
# ---------------------------------------------------------------------------


def test_hire_orders_are_not_gated_by_growth_capacity() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = cfg.regime_low
    feat_denied = _base_features(
        growth_capacity_available=False, worker_positions=[(4, 4)], worker_inventories=[{}]
    )
    orders, _ = _hire_orders(cfg, profile, feat_denied, feat_denied.money)
    assert orders  # floor_headcount (3 per quadrant) > 1 worker -> hires regardless


def test_seed_orders_are_not_gated_by_growth_capacity() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = cfg.regime_low
    feat_denied = _base_features(growth_capacity_available=False, seeds={}, has_empty_crop_zone_tile=True)
    orders, _ = _seed_orders(cfg, profile, feat_denied, feat_denied.money, room_left=10)
    assert orders and orders[0][0] == "BUY_SEED"


def test_wheat_stock_orders_are_not_gated_by_growth_capacity() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    feat_denied = _base_features(
        growth_capacity_available=False, structures_total=1, shed={}, market_prices={}
    )
    orders, _ = _wheat_stock_orders(cfg, feat_denied, feat_denied.money, room_left=10)
    assert orders and orders[0][0] == "BUY_PRODUCT"


def test_wheat_stock_orders_use_the_engine_valid_buy_product_verb() -> None:
    """V5 fix, isolated: the only change from V4 is this order's shape.
    ``kaggle_environments/envs/kaggriculture/kaggriculture.py::_parse_order``
    accepts exactly ``["BUY_PRODUCT", item, n]`` for WHEAT/FERTILIZER; the
    V1-V4 verb ``["BUY_WHEAT", n]`` is not in its recognised set and is
    silently dropped (returns ``None``), never reaching ``_commit_unit``."""

    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    feat = _base_features(structures_total=1, shed={"WHEAT": 0}, market_prices={})
    orders, _ = _wheat_stock_orders(cfg, feat, feat.money, room_left=10)
    assert orders == [["BUY_PRODUCT", "WHEAT", orders[0][2]]]
    assert len(orders[0]) == 3


# ---------------------------------------------------------------------------
# V4: end-to-end wiring inside `_extract_features` (PLANT_OPPORTUNITY
# suppression), and the telemetry counter.
# ---------------------------------------------------------------------------


def test_plant_opportunity_withheld_one_step_from_eod_with_a_lone_worker() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = agent._current_profile()
    obs = _observation(step=23, farmer=(4, 4), money=50000.0, seeds={"WHEAT": 50})
    snap = CodexObservationAdapter.parse(
        obs, CONFIGURATION, fallback_turns_per_day=24, fallback_episode_steps=720
    )
    feat = _extract_features(cfg, profile, snap)
    assert feat.growth_capacity_available is False
    assert not any(o["kind"] == "PLANT_OPPORTUNITY" for o in feat.opportunities)


def test_plant_opportunity_offered_at_start_of_day_with_ample_budget() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = agent._current_profile()
    obs = _observation(step=0, farmer=(4, 4), money=50000.0, seeds={"WHEAT": 50})
    snap = CodexObservationAdapter.parse(
        obs, CONFIGURATION, fallback_turns_per_day=24, fallback_episode_steps=720
    )
    feat = _extract_features(cfg, profile, snap)
    assert feat.growth_capacity_available is True
    assert any(o["kind"] == "PLANT_OPPORTUNITY" for o in feat.opportunities)


def test_growth_capacity_denials_counter_increments_in_telemetry() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    obs = _observation(step=23, farmer=(4, 4), money=50000.0, seeds={"WHEAT": 50})
    agent(obs, CONFIGURATION)
    snapshot = agent.telemetry_snapshot()
    assert snapshot["growth_capacity_denials"] >= 1


# ---------------------------------------------------------------------------
# `_resolve_assignment` sanity check (unchanged from V3): kept as a smoke
# test that the shared dispatch helper still wires correctly in this file.
# ---------------------------------------------------------------------------


def test_resolve_assignment_emits_pickup_when_shed_has_no_wheat() -> None:
    agent = create_claude_e18_wheat_market_fix_v5()
    cfg = agent.config
    profile = agent._current_profile()
    obs = _observation(step=0, farmer=(4, 4), shed={"WHEAT": 0}, money=50000.0)
    snap = CodexObservationAdapter.parse(
        obs, CONFIGURATION, fallback_turns_per_day=24, fallback_episode_steps=720
    )
    feat = _extract_features(cfg, profile, snap)
    assignment = _Assignment(kind="FEED_NEEDED", target=(6, 4))
    command = _resolve_assignment((4, 4), {}, assignment, cfg, profile, feat)
    assert command == ["PICKUP", "WHEAT", 1]


# ---------------------------------------------------------------------------
# Engine-level regression: the worst V2 loss match, replayed under V5.
# ---------------------------------------------------------------------------


def test_v5_does_not_regress_the_worst_traced_v2_match() -> None:
    """Seed 180903002, seat 0 vs Copilot E18.2: V2 lost 4 verified animals
    in this exact match; V3 already brought it to 0, V4 kept it at 0. V5
    changes only the wheat order verb, so this match must not regress."""

    from kaggle_environments import make

    from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
        create_copilot_e18_opponent_reactive_v2,
    )
    from experiments.e18.tools.common import (
        run_e18_dynamic_architecture_tournament_v1 as prior,
    )

    seed = 180903002
    ctx0 = {"run_id": "v5-regression", "episode_id": "v5-regression", "seed": seed, "player_position": 0}
    ctx1 = {"run_id": "v5-regression", "episode_id": "v5-regression", "seed": seed, "player_position": 1}
    policy0 = create_claude_e18_wheat_market_fix_v5(run_context=ctx0)
    policy1 = create_copilot_e18_opponent_reactive_v2(run_context=ctx1)

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])

    assert policy0.technical_errors == 0
    assert prior._verified_livestock_losses(env, 0) == 0


def test_v5_wheat_purchases_are_actually_executed_by_the_real_engine() -> None:
    """The isolated fix's real-world effect: on the same traced match,
    V4 never once got a `BUY_PRODUCT:WHEAT` order accepted (the invalid
    `BUY_WHEAT` verb was silently dropped every call, module docstring of
    e18_wheat_market_fix_v5.py). V5 must show at least one real engine-side
    WHEAT purchase somewhere across the 720 steps: money spent on WHEAT
    without a corresponding drop from crediting a sale, i.e. `market`
    orders this seat actually issued containing `BUY_PRODUCT`/`WHEAT`, that
    the engine's replay confirms were part of the recorded action stream
    (proof the fixed verb was actually sent, not merely constructed)."""

    from kaggle_environments import make

    from agricola.strategy.copilot.e18_opponent_reactive_v2 import (
        create_copilot_e18_opponent_reactive_v2,
    )

    seed = 180903002
    ctx0 = {"run_id": "v5-wheat-check", "episode_id": "v5-wheat-check", "seed": seed, "player_position": 0}
    ctx1 = {"run_id": "v5-wheat-check", "episode_id": "v5-wheat-check", "seed": seed, "player_position": 1}
    policy0 = create_claude_e18_wheat_market_fix_v5(run_context=ctx0)
    policy1 = create_copilot_e18_opponent_reactive_v2(run_context=ctx1)

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run([policy0, policy1])
    replay = env.toJSON()

    wheat_orders = [
        order
        for step in replay["steps"][1:]
        for order in (step[0].get("action") or {}).get("market", [])
        if order[:2] == ["BUY_PRODUCT", "WHEAT"]
    ]
    assert wheat_orders, "expected at least one BUY_PRODUCT WHEAT order across the game"
    assert all(len(order) == 3 and order[2] > 0 for order in wheat_orders)
