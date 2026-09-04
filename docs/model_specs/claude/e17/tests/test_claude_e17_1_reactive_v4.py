"""Tests for the Claude E17.1 3Q reactive independent controller — V4.

Covers everything required of V3 (factory/import, batch schema and limits,
safe fallback, controlled determinism, state reactivity, real config
consumption, absence of prohibited imports/tokens, a full episode smoke run,
ledger-wrapper action parity, persistent target assignment, day-rollover
invalidation, the density-based core-establishment guard, the
workforce-readiness guard on expansion, the dedicated animal-purchase
reserve, and HIRE remaining active during the shutdown window) plus the
V4-specific delta: SW/Q2 livestock structures are now offered once SW is
unlocked, capped at their own smaller `structures_target_third_quadrant`
independently from NW/NE's `structures_target_per_quadrant` (MODEL_SPEC V4).
"""

from __future__ import annotations

import ast
import json
import tempfile
from copy import deepcopy
from pathlib import Path

import kaggle_environments

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.e17_ledger import E17CommandLedger, instrument_policy
from agricola.core.observation_contract import CodexObservationAdapter
from agricola.strategy.claude.e17_reactive_3q_v4 import (
    DEFAULT_CONFIG_PATH,
    POLICY_VERSION,
    SAFE_PASS_ACTION,
    ClaudeE17ReactiveAgentV4,
    ReactiveConfigV4,
    _extract_features,
    claude_policy_fingerprint,
    create_claude_e17_agent_v4,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_PATH = (
    REPO_ROOT / "src" / "agricola" / "strategy" / "claude" / "e17_reactive_3q_v4.py"
)
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
):
    farm = _blank_farm(
        unlocked=unlocked, money=money, farmer=farmer, hands=hands, hires_today=hires_today
    )
    return {
        "step": step,
        "day": step // 24,
        "hour": step % 24,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
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
                    "GOOSE": 300,
                    "COW": 400,
                    "SHEEP": 500,
                }
            ),
        },
    }


def _dense_wheat_tile(planted_day: int = 0) -> dict:
    return {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": planted_day,
        "watered_today": True,
        "consecutive_unwatered": 0,
        "yield_units": 1,
        "max_lifespan_step": 10_000,
        "fertilized_until_day": -1,
    }


def _plant_dense_core(obs: dict, count: int = 9) -> None:
    """Plant `count` mature WHEAT tiles in NW's crop zone (past the
    livestock-zone reservation, the first 4 tiles in row-major scan order,
    and the shed-access tile (4, 4)) so core_quadrant_fill_ratio clears the
    default 0.4 threshold (needs 8/20)."""

    livestock_zone = {(0, 0), (1, 0), (2, 0), (3, 0)}
    shed_tile = (4, 4)
    tiles = obs["farms"][0]["tiles"]
    placed = 0
    for y in range(5):
        for x in range(5):
            if (x, y) in livestock_zone or (x, y) == shed_tile:
                continue
            if placed >= count:
                return
            tiles[y][x] = _dense_wheat_tile()
            placed += 1


# ---------------------------------------------------------------------------
# Factory and import
# ---------------------------------------------------------------------------


def test_factory_returns_callable_agent_with_expected_interface() -> None:
    agent = create_claude_e17_agent_v4()
    assert isinstance(agent, ClaudeE17ReactiveAgentV4)
    assert agent.policy_version == POLICY_VERSION
    assert callable(agent)
    assert agent.technical_errors == 0
    action = agent(_observation(), CONFIGURATION)
    assert isinstance(action, dict)
    assert set(action) == {"farmer", "hands", "market"}


def test_factory_accepts_explicit_run_context_and_config_path() -> None:
    agent = create_claude_e17_agent_v4(
        run_context={"note": "unit-test"}, config_path=DEFAULT_CONFIG_PATH
    )
    assert agent.run_context == {"note": "unit-test"}
    assert agent.config.policy_id == POLICY_VERSION


# ---------------------------------------------------------------------------
# Batch schema and limits
# ---------------------------------------------------------------------------


def test_action_schema_matches_shared_interface_contract() -> None:
    agent = create_claude_e17_agent_v4()
    hands = [(4, 3), (5, 4)]
    obs = _observation(hands=hands, money=5000.0)
    action = agent(obs, CONFIGURATION)
    assert isinstance(action["farmer"], list) and action["farmer"]
    assert isinstance(action["hands"], list)
    assert len(action["hands"]) == len(hands)
    for hand_command in action["hands"]:
        assert isinstance(hand_command, list) and hand_command
    assert isinstance(action["market"], list)
    assert len(action["market"]) <= CONFIGURATION["maxMarketOrdersPerTurn"]


def test_market_batch_never_exceeds_configured_limit() -> None:
    agent = create_claude_e17_agent_v4()
    tight_configuration = dict(CONFIGURATION, maxMarketOrdersPerTurn=2)
    obs = _observation(money=50000.0, unlocked=("NW", "NE"))
    action = agent(obs, tight_configuration)
    assert len(action["market"]) <= 2


# ---------------------------------------------------------------------------
# Safe fallback
# ---------------------------------------------------------------------------


def test_malformed_observation_falls_back_to_safe_pass() -> None:
    agent = create_claude_e17_agent_v4()
    before = agent.technical_errors
    action = agent({"not": "a valid observation"}, CONFIGURATION)
    assert action == SAFE_PASS_ACTION
    assert agent.technical_errors == before + 1


def test_non_mapping_observation_falls_back_to_safe_pass() -> None:
    agent = create_claude_e17_agent_v4()
    action = agent(None, CONFIGURATION)  # type: ignore[arg-type]
    assert action == SAFE_PASS_ACTION
    assert agent.technical_errors == 1


# ---------------------------------------------------------------------------
# Controlled determinism
# ---------------------------------------------------------------------------


def test_same_observation_produces_identical_action_on_fresh_agents() -> None:
    obs = _observation(hands=[(4, 3)], money=4000.0, unlocked=("NW", "NE"))
    first = create_claude_e17_agent_v4()(deepcopy(obs), CONFIGURATION)
    second = create_claude_e17_agent_v4()(deepcopy(obs), CONFIGURATION)
    assert first == second


def test_same_agent_instance_is_deterministic_when_state_is_unchanged() -> None:
    agent = create_claude_e17_agent_v4()
    obs = _observation(hands=[(3, 4), (5, 5)], money=2500.0, unlocked=("NW", "NE", "SW"))
    first = agent(deepcopy(obs), CONFIGURATION)
    second = agent(deepcopy(obs), CONFIGURATION)
    assert first == second


# ---------------------------------------------------------------------------
# State reactivity
# ---------------------------------------------------------------------------


def test_reactivity_to_unwatered_plant_at_same_step() -> None:
    agent = create_claude_e17_agent_v4()

    baseline = _observation(step=100, farmer=(4, 4))
    action_baseline = agent(deepcopy(baseline), CONFIGURATION)

    thirsty = deepcopy(baseline)
    thirsty["farms"][0]["tiles"][4][4] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 3,
        "watered_today": False,
        "consecutive_unwatered": 1,
        "yield_units": 1,
        "max_lifespan_step": 10_000,
        "fertilized_until_day": -1,
    }
    action_thirsty = agent(thirsty, CONFIGURATION)

    assert action_thirsty["farmer"] == ["WATER"]
    assert action_baseline["farmer"] != action_thirsty["farmer"]


def test_reactivity_to_unfed_animal_at_same_step() -> None:
    agent = create_claude_e17_agent_v4()
    obs = _observation(step=200, farmer=(1, 1))
    obs["farms"][0]["tiles"][1][1] = {
        "kind": "PASTURE",
        "animal": "SHEEP",
        "placed_day": 1,
        "yield_units": 0,
        "consecutive_unfed": 1,
        "fed_today": False,
        "cared_today": False,
        "fertilizer_available": False,
        "pending_care_bonus": 0,
    }
    obs["private"]["inventories"] = [{"WHEAT": 2}]
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["FEED"]


# ---------------------------------------------------------------------------
# Persistent target assignment (inherited from V2, re-verified on V3)
# ---------------------------------------------------------------------------


def test_farmer_keeps_moving_toward_the_same_persistent_target() -> None:
    agent = create_claude_e17_agent_v4()
    obs = _observation(step=0, farmer=(0, 0))
    obs["farms"][0]["tiles"][4][4] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "watered_today": False,
        "consecutive_unwatered": 0,
        "yield_units": 1,
        "max_lifespan_step": 10_000,
        "fertilized_until_day": -1,
    }

    first_action = agent(deepcopy(obs), CONFIGURATION)
    assert first_action["farmer"] in (["EAST"], ["SOUTH"])
    assignment = agent._assignments["farmer"]
    assert assignment.kind == "URGENT_WATER"
    assert assignment.target == (4, 4)

    move = first_action["farmer"][0]
    new_pos = {"EAST": (1, 0), "SOUTH": (0, 1)}[move]
    obs["farms"][0]["farmer"] = list(new_pos)
    second_action = agent(deepcopy(obs), CONFIGURATION)
    assert agent._assignments["farmer"].target == (4, 4)
    assert second_action["farmer"][0] in ("EAST", "SOUTH", "WATER")


def test_hand_assignments_are_cleared_on_day_rollover_but_farmer_is_not() -> None:
    from agricola.strategy.claude.e17_reactive_3q_v4 import _Assignment

    agent = create_claude_e17_agent_v4()
    agent._assignments["hand:0"] = _Assignment(kind="URGENT_WATER", target=(9, 9))
    agent._assignments["farmer"] = _Assignment(kind="RECOVERY_DIG", target=(2, 2))
    agent._last_seen_day = 0

    obs_day1 = _observation(step=30, farmer=(4, 4), hands=[(5, 5)])
    obs_day1["day"] = 1
    obs_day1["hour"] = 6
    obs_day1["farms"][0]["tiles"][2][2] = {"kind": "WEED"}
    agent(obs_day1, CONFIGURATION)

    assert agent._last_seen_day == 1
    assert agent._assignments.get("hand:0") is None or agent._assignments["hand:0"].target != (
        9,
        9,
    )
    assert agent._assignments["farmer"].target == (2, 2)


# ---------------------------------------------------------------------------
# V3: density-based core-establishment guard
# ---------------------------------------------------------------------------


def test_no_land_expansion_before_core_established() -> None:
    agent = create_claude_e17_agent_v4()
    obs = _observation(step=0, money=50000.0, unlocked=("NW",))
    action = agent(obs, CONFIGURATION)
    assert ["BUY_LAND"] not in action["market"]


def test_no_land_expansion_with_harvests_but_low_density() -> None:
    """Regression test for the V2 loophole this version closes: satisfying
    the harvest-request counter alone (via a fast WHEAT cycle) must not be
    enough without real crop-zone density."""

    agent = create_claude_e17_agent_v4()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    obs = _observation(step=200, money=50000.0, unlocked=("NW",), hands=[(0, 1), (0, 2)])
    # A single planted tile: far below core_min_fill_ratio (0.4 -> 8/20).
    obs["farms"][0]["tiles"][1][1] = _dense_wheat_tile()
    action = agent(obs, CONFIGURATION)
    assert ["BUY_LAND"] not in action["market"]


def test_land_expansion_allowed_once_core_established_and_workforce_ready() -> None:
    agent = create_claude_e17_agent_v4()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    # min_workers_per_quadrant defaults to 3: farmer + 2 hands.
    obs = _observation(
        step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=[(0, 1), (0, 2)]
    )
    _plant_dense_core(obs, count=9)
    action = agent(obs, CONFIGURATION)
    assert ["BUY_LAND"] in action["market"]


def test_no_land_expansion_when_workforce_below_quadrant_floor() -> None:
    """Regression test for the collapse found during V3 development: a dense
    but understaffed Q0 must not expand (workforce-readiness guard)."""

    agent = create_claude_e17_agent_v4()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    obs = _observation(step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=())
    _plant_dense_core(obs, count=9)
    action = agent(obs, CONFIGURATION)
    assert ["BUY_LAND"] not in action["market"]


def test_no_animal_purchase_before_core_established() -> None:
    agent = create_claude_e17_agent_v4()
    obs = _observation(step=0, money=50000.0, unlocked=("NW",))
    obs["farms"][0]["tiles"][0][0] = {"kind": "PASTURE"}
    action = agent(obs, CONFIGURATION)
    assert not any(order[0] == "BUY_ANIMAL" for order in action["market"])


# ---------------------------------------------------------------------------
# V3: dedicated animal-purchase reserve
# ---------------------------------------------------------------------------


def test_no_animal_purchase_below_dedicated_reserve() -> None:
    agent = create_claude_e17_agent_v4()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    reserve = agent.config.animal_purchase_reserve
    obs = _observation(
        step=200,
        money=reserve + 10.0,  # below reserve + cheapest animal cost (GOOSE $300)
        unlocked=("NW",),
        farmer=(4, 4),
        hands=[(0, 1), (0, 2)],
    )
    _plant_dense_core(obs, count=9)
    obs["farms"][0]["tiles"][0][0] = {"kind": "COOP"}
    action = agent(obs, CONFIGURATION)
    assert not any(order[0] == "BUY_ANIMAL" for order in action["market"])


def test_no_new_animal_purchase_while_an_existing_one_is_at_risk() -> None:
    agent = create_claude_e17_agent_v4()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    obs = _observation(
        step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=[(0, 1), (0, 2)]
    )
    _plant_dense_core(obs, count=9)
    obs["farms"][0]["tiles"][2][2] = {
        "kind": "PASTURE",
        "animal": "SHEEP",
        "placed_day": 0,
        "yield_units": 0,
        "consecutive_unfed": 1,
        "fed_today": False,
        "cared_today": False,
        "fertilizer_available": False,
        "pending_care_bonus": 0,
    }
    obs["farms"][0]["tiles"][2][3] = {"kind": "PASTURE"}
    obs["private"]["shed"] = {"SHEEP": 1}
    action = agent(obs, CONFIGURATION)
    assert not any(order[0] == "BUY_ANIMAL" for order in action["market"])


# ---------------------------------------------------------------------------
# V3: HIRE remains active during the shutdown window
# ---------------------------------------------------------------------------


def test_hire_is_not_blocked_during_shutdown_but_new_investment_is() -> None:
    """Regression test for the endgame collapse found during V3 development:
    HIRE must keep firing when days_remaining is inside the shutdown window
    (episode_steps - step small enough), while BUY_LAND/BUY_SEED do not."""

    agent = create_claude_e17_agent_v4()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    shutdown_days = agent.config.shutdown_days_remaining
    turns_per_day = 24
    # 2 days remaining: inside the shutdown window.
    remaining_days = max(1, shutdown_days - 1)
    step = CONFIGURATION["episodeSteps"] - remaining_days * turns_per_day - 1
    obs = _observation(step=step, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=())
    _plant_dense_core(obs, count=9)
    action = agent(obs, CONFIGURATION)
    assert any(order[0] == "HIRE" for order in action["market"])
    assert ["BUY_LAND"] not in action["market"]
    assert not any(order[0] == "BUY_SEED" for order in action["market"])


# ---------------------------------------------------------------------------
# Real config consumption
# ---------------------------------------------------------------------------


def test_config_is_actually_read_and_changes_behavior() -> None:
    base_payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        strict_payload = deepcopy(base_payload)
        strict_payload["workforce"]["hire_batch_limit_per_turn"] = 0
        strict_path = tmp_path / "strict.json"
        strict_path.write_text(json.dumps(strict_payload), encoding="utf-8")

        permissive_payload = deepcopy(base_payload)
        permissive_payload["workforce"]["hire_batch_limit_per_turn"] = 5
        permissive_payload["workforce"]["max_hands"] = 20
        permissive_path = tmp_path / "permissive.json"
        permissive_path.write_text(json.dumps(permissive_payload), encoding="utf-8")

        obs = _observation(money=50000.0)
        strict_action = create_claude_e17_agent_v4(config_path=strict_path)(
            deepcopy(obs), CONFIGURATION
        )
        permissive_action = create_claude_e17_agent_v4(config_path=permissive_path)(
            deepcopy(obs), CONFIGURATION
        )

    strict_hires = sum(1 for order in strict_action["market"] if order[0] == "HIRE")
    permissive_hires = sum(1 for order in permissive_action["market"] if order[0] == "HIRE")
    assert strict_hires == 0
    assert permissive_hires > strict_hires


def test_config_core_min_fill_ratio_is_consumed() -> None:
    base_payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp_dir:
        zero_threshold_payload = deepcopy(base_payload)
        zero_threshold_payload["expansion"]["core_min_fill_ratio"] = 0.0
        zero_threshold_payload["expansion"]["core_min_harvest_requests"] = 0
        zero_threshold_path = Path(tmp_dir) / "zero_threshold.json"
        zero_threshold_path.write_text(json.dumps(zero_threshold_payload), encoding="utf-8")

        agent = create_claude_e17_agent_v4(config_path=zero_threshold_path)
        obs = _observation(
            step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=[(0, 1), (0, 2)]
        )
        obs["farms"][0]["tiles"][1][1] = _dense_wheat_tile()
        action = agent(obs, CONFIGURATION)
    assert ["BUY_LAND"] in action["market"]


def test_config_is_frozen_and_holdout_not_consumed() -> None:
    payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    assert payload["provenance"]["holdout_consumed"] is False
    assert payload["provenance"]["final_confirmation_consumed"] is False
    config = ReactiveConfigV4.load(DEFAULT_CONFIG_PATH)
    assert config.target_quadrants == 3


# ---------------------------------------------------------------------------
# V4: SW/Q2 livestock topology (MODEL_SPEC V4, single new lever)
# ---------------------------------------------------------------------------


def _feat_for(cfg: ReactiveConfigV4, obs: dict, configuration=CONFIGURATION):
    snap = CodexObservationAdapter.parse(
        obs,
        configuration,
        fallback_turns_per_day=cfg.fallback_turns_per_day,
        fallback_episode_steps=cfg.fallback_episode_steps,
    )
    return _extract_features(cfg, snap)


def _build_opportunity_count(feat, quadrant: str) -> int:
    return sum(
        1
        for o in feat.opportunities
        if o["kind"] == "BUILD_OPPORTUNITY" and o["quadrant"] == quadrant
    )


def test_default_config_opens_sw_with_its_own_smaller_target() -> None:
    cfg = ReactiveConfigV4.load(DEFAULT_CONFIG_PATH)
    assert cfg.max_quadrants_for_livestock == 3
    assert (
        cfg.livestock_structures_target_third_quadrant
        < cfg.livestock_structures_target_per_quadrant
    )

    obs = _observation(step=200, unlocked=("NW", "NE", "SW"), money=50000.0)
    feat = _feat_for(cfg, obs)

    assert _build_opportunity_count(feat, "NW") == cfg.livestock_structures_target_per_quadrant
    assert _build_opportunity_count(feat, "NE") == cfg.livestock_structures_target_per_quadrant
    assert (
        _build_opportunity_count(feat, "SW")
        == cfg.livestock_structures_target_third_quadrant
    )


def test_sw_livestock_opportunities_absent_when_sw_locked() -> None:
    cfg = ReactiveConfigV4.load(DEFAULT_CONFIG_PATH)
    obs = _observation(step=200, unlocked=("NW", "NE"), money=50000.0)
    feat = _feat_for(cfg, obs)
    assert _build_opportunity_count(feat, "SW") == 0


def test_v3_equivalent_config_keeps_sw_at_zero() -> None:
    """Regression guard: a V3-equivalent config (`max_quadrants_for_livestock:
    2`) must reproduce V3's SW=0 behavior exactly, so the new lever is a pure
    addition, not a change to V3's own default topology."""

    base_payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    payload = deepcopy(base_payload)
    payload["livestock"]["max_quadrants_for_livestock"] = 2
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "v3_equivalent.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        cfg = ReactiveConfigV4.load(path)

    obs = _observation(step=200, unlocked=("NW", "NE", "SW"), money=50000.0)
    feat = _feat_for(cfg, obs)
    assert _build_opportunity_count(feat, "SW") == 0
    assert _build_opportunity_count(feat, "NW") == cfg.livestock_structures_target_per_quadrant


# ---------------------------------------------------------------------------
# Independence: no prohibited imports or tokens
# ---------------------------------------------------------------------------


def test_source_has_no_other_agent_strategy_dependency() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    prohibited_prefixes = (
        "agricola.strategy.codex",
        "agricola.strategy.antigravity",
        "agricola.strategy.copilot",
    )
    prohibited = [name for name in imported if name.startswith(prohibited_prefixes)]
    assert not prohibited
    assert "ROUTINE_ACTIONS" not in source
    assert "codex_v9_routine_data" not in source
    assert "submission_codex" not in source


def test_policy_fingerprint_is_a_distinct_sha256() -> None:
    fingerprint = claude_policy_fingerprint()
    assert len(fingerprint) == 64
    assert all(c in "0123456789ABCDEF" for c in fingerprint)
    codex_v9_routine_sha256 = (
        "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"
    )
    assert fingerprint != codex_v9_routine_sha256

    from agricola.strategy.claude.e17_reactive_3q import (
        claude_policy_fingerprint as v1_fingerprint,
    )
    from agricola.strategy.claude.e17_reactive_3q_v2 import (
        claude_policy_fingerprint as v2_fingerprint,
    )
    from agricola.strategy.claude.e17_reactive_3q_v3 import (
        claude_policy_fingerprint as v3_fingerprint,
    )

    assert fingerprint != v1_fingerprint()
    assert fingerprint != v3_fingerprint()
    assert fingerprint != v2_fingerprint()


# ---------------------------------------------------------------------------
# Episode smoke (real engine)
# ---------------------------------------------------------------------------


def test_short_episode_smoke_completes_without_technical_errors() -> None:
    agent = create_claude_e17_agent_v4()
    env = kaggle_environments.make(
        "kaggriculture", configuration={"episodeSteps": 96, "seed": 26090101}
    )
    env.run([agent, inert_pass_policy])
    terminal = env.steps[-1]
    assert terminal[0]["status"] == "DONE"
    assert agent.technical_errors == 0
    for state in env.steps:
        action = state[0].get("action")
        if action is None:
            continue
        assert isinstance(action["farmer"], list) and action["farmer"]
        assert len(action["market"]) <= CONFIGURATION["maxMarketOrdersPerTurn"]


# ---------------------------------------------------------------------------
# Ledger wrapper parity
# ---------------------------------------------------------------------------


def test_ledger_wrapper_does_not_change_actions() -> None:
    policy = create_claude_e17_agent_v4()
    reference = create_claude_e17_agent_v4()
    ledger = E17CommandLedger(
        {
            "episode_id": "E17-1-CLAUDE-V4-UNIT",
            "seed": 26090101,
            "seat": 0,
            "policy_version": POLICY_VERSION,
            "source_hash": "SOURCE",
            "config_hash": "CONFIG",
            "routine_hash": claude_policy_fingerprint(),
        }
    )
    wrapped = instrument_policy(policy, ledger)

    obs = _observation(hands=[(4, 3)], money=4000.0, unlocked=("NW", "NE"))
    wrapped_action = wrapped(deepcopy(obs), CONFIGURATION)
    reference_action = reference(deepcopy(obs), CONFIGURATION)

    assert wrapped_action == reference_action
    expected_commands = 1 + len(wrapped_action["hands"]) + len(wrapped_action["market"])
    assert len(ledger.records) == expected_commands
    assert ledger.metrics()["ledger_record_coverage"] == 1.0
    assert wrapped.e17_inner_policy is policy
    assert policy.technical_errors == 0


def test_ledger_errors_do_not_affect_returned_action(monkeypatch) -> None:
    policy = create_claude_e17_agent_v4()
    ledger = E17CommandLedger({"episode_id": "E17-1-CLAUDE-V4-FAULT", "seed": 1, "seat": 0})

    def _broken_record(*args, **kwargs):
        raise RuntimeError("simulated ledger failure")

    monkeypatch.setattr(ledger, "record", _broken_record)
    wrapped = instrument_policy(policy, ledger)

    obs = _observation()
    action = wrapped(deepcopy(obs), CONFIGURATION)
    assert action == policy(deepcopy(obs), CONFIGURATION)
    assert ledger.errors
