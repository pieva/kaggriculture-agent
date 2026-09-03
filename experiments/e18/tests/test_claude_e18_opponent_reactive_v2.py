"""Tests for the Claude E18.2 opponent-reactive controller — V2 (remediation).

Covers everything required of V1 (public opponent snapshot, regime
classifier, sticky selector, crop lifecycle KEEP/HARVEST/DIG fixtures,
persistent priority dispatch, batch schema, safe fallback, determinism,
config consumption, independence, episode smoke) plus the V2-specific
remediation fixtures required by
``E18_CLAUDE_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md``: a proactive
wheat feed buffer bought before (not after) the first animal purchase, a
per-call check that reproduces V1's traced escape pattern, an emergency
queue that suppresses non-urgent BUY_LAND/BUY_SEED while any animal is
unfed, and a crop-surface cap tied to currently-hired workforce.
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
from agricola.strategy.claude.e18_opponent_reactive_v2 import (
    DEFAULT_CONFIG_PATH,
    POLICY_VERSION,
    SAFE_PASS_ACTION,
    ClaudeE18OpponentReactiveAgentV2,
    ReactiveConfigE18V2,
    _classify_regime,
    _extract_features,
    _extract_opponent_snapshot,
    claude_policy_fingerprint,
    create_claude_e18_agent_v2,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = REPO_ROOT / "src" / "agricola" / "strategy" / "claude" / "e18_opponent_reactive_v2.py"
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


def _opponent_farm(*, unlocked=("NW",), hands=(), crop_tiles=0, animal_tiles=0):
    tiles = []
    for y in range(10):
        row = []
        for x in range(10):
            quadrant = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
            row.append(None if quadrant in unlocked else "LOCKED")
        tiles.append(row)
    placed_crop = 0
    for y in range(10):
        for x in range(10):
            if placed_crop >= crop_tiles:
                break
            if tiles[y][x] is None:
                tiles[y][x] = {"kind": "PLANT", "crop": "WHEAT", "yield_units": 0}
                placed_crop += 1
    placed_animal = 0
    for y in range(10):
        for x in range(10):
            if placed_animal >= animal_tiles:
                break
            if tiles[y][x] is None:
                tiles[y][x] = {"kind": "PASTURE", "animal": "SHEEP"}
                placed_animal += 1
    return {
        "money": 3000.0,
        "farmer": [4, 4],
        "hands": [list(h) for h in hands],
        "tiles": tiles,
        "unlocked_quadrants": list(unlocked),
        "hires_today": 0,
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
    opponent_farm=None,
):
    farm = _blank_farm(
        unlocked=unlocked, money=money, farmer=farmer, hands=hands, hires_today=hires_today
    )
    farms = [farm, deepcopy(farm)]
    if opponent_farm is not None:
        farms[1 - player] = opponent_farm
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


# ---------------------------------------------------------------------------
# Factory and import
# ---------------------------------------------------------------------------


def test_factory_returns_callable_agent_with_expected_interface() -> None:
    agent = create_claude_e18_agent_v2()
    assert isinstance(agent, ClaudeE18OpponentReactiveAgentV2)
    assert agent.policy_version == POLICY_VERSION
    assert callable(agent)
    assert agent.technical_errors == 0
    action = agent(_observation(), CONFIGURATION)
    assert isinstance(action, dict)
    assert set(action) == {"farmer", "hands", "market"}


def test_factory_accepts_explicit_run_context_and_config_path() -> None:
    agent = create_claude_e18_agent_v2(run_context={"note": "unit-test"}, config_path=DEFAULT_CONFIG_PATH)
    assert agent.run_context == {"note": "unit-test"}
    assert agent.config.policy_id == POLICY_VERSION


# ---------------------------------------------------------------------------
# Batch schema and limits
# ---------------------------------------------------------------------------


def test_action_schema_matches_shared_interface_contract() -> None:
    agent = create_claude_e18_agent_v2()
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
    agent = create_claude_e18_agent_v2()
    tight_configuration = dict(CONFIGURATION, maxMarketOrdersPerTurn=2)
    obs = _observation(money=50000.0, unlocked=("NW", "NE"))
    action = agent(obs, tight_configuration)
    assert len(action["market"]) <= 2


# ---------------------------------------------------------------------------
# Safe fallback
# ---------------------------------------------------------------------------


def test_malformed_observation_falls_back_to_safe_pass() -> None:
    agent = create_claude_e18_agent_v2()
    before = agent.technical_errors
    action = agent({"not": "a valid observation"}, CONFIGURATION)
    assert action == SAFE_PASS_ACTION
    assert agent.technical_errors == before + 1


def test_non_mapping_observation_falls_back_to_safe_pass() -> None:
    agent = create_claude_e18_agent_v2()
    action = agent(None, CONFIGURATION)  # type: ignore[arg-type]
    assert action == SAFE_PASS_ACTION
    assert agent.technical_errors == 1


# ---------------------------------------------------------------------------
# Controlled determinism
# ---------------------------------------------------------------------------


def test_same_observation_produces_identical_action_on_fresh_agents() -> None:
    obs = _observation(hands=[(4, 3)], money=4000.0, unlocked=("NW", "NE"))
    first = create_claude_e18_agent_v2()(deepcopy(obs), CONFIGURATION)
    second = create_claude_e18_agent_v2()(deepcopy(obs), CONFIGURATION)
    assert first == second


def test_same_agent_instance_is_deterministic_when_state_is_unchanged() -> None:
    agent = create_claude_e18_agent_v2()
    obs = _observation(hands=[(3, 4), (5, 5)], money=2500.0, unlocked=("NW", "NE", "SW"))
    first = agent(deepcopy(obs), CONFIGURATION)
    second = agent(deepcopy(obs), CONFIGURATION)
    assert first == second


# ---------------------------------------------------------------------------
# Layer 1: PUBLIC_OPPONENT_SNAPSHOT
# ---------------------------------------------------------------------------


def test_opponent_snapshot_reads_only_public_farm_fields() -> None:
    opp_farm = _opponent_farm(unlocked=("NW", "NE"), hands=[(1, 1)], crop_tiles=5, animal_tiles=2)
    obs = _observation(step=100, player=0, opponent_farm=opp_farm)
    snapshot = _extract_opponent_snapshot(obs, my_seat=0)
    assert snapshot == {
        "unlocked_quadrants": 2,
        "hands": 1,
        "crop_tiles": 5,
        "weed_tiles": 0,
        "animal_count": 2,
        "pasture_count": 2,
    }
    # Never touches `private` -- that key is only ever the observing
    # player's own shed/seeds/inventories, not the opponent's.
    assert "private" not in json.dumps(snapshot)


def test_opponent_snapshot_uses_the_other_seat_when_i_am_seat_one() -> None:
    opp_farm = _opponent_farm(unlocked=("NW",), crop_tiles=3)
    obs = _observation(step=100, player=1, opponent_farm=opp_farm)
    # opponent_farm was injected at index (1 - player) = 0
    snapshot = _extract_opponent_snapshot(obs, my_seat=1)
    assert snapshot["crop_tiles"] == 3


# ---------------------------------------------------------------------------
# Layer 2: REGIME_CLASSIFIER
# ---------------------------------------------------------------------------


def test_classifier_picks_low_pressure_below_threshold() -> None:
    cfg = ReactiveConfigE18V2.load(DEFAULT_CONFIG_PATH)
    snapshot = {
        "unlocked_quadrants": 1,
        "hands": 0,
        "crop_tiles": 0,
        "weed_tiles": 0,
        "animal_count": 0,
        "pasture_count": 0,
    }
    regime, pressure = _classify_regime(cfg, snapshot)
    assert regime == cfg.regime_low.name
    assert pressure < cfg.regime_pressure_threshold


def test_classifier_picks_high_pressure_above_threshold() -> None:
    cfg = ReactiveConfigE18V2.load(DEFAULT_CONFIG_PATH)
    snapshot = {
        "unlocked_quadrants": 3,
        "hands": 10,
        "crop_tiles": 40,
        "weed_tiles": 5,
        "animal_count": 15,
        "pasture_count": 14,
    }
    regime, pressure = _classify_regime(cfg, snapshot)
    assert regime == cfg.regime_high.name
    assert pressure >= cfg.regime_pressure_threshold


# ---------------------------------------------------------------------------
# Layer 3: STICKY_POLICY_SELECTOR
# ---------------------------------------------------------------------------


def test_regime_is_decided_exactly_once_inside_the_window() -> None:
    agent = create_claude_e18_agent_v2()
    assert agent._regime is None
    # Before the window: no decision yet.
    agent(_observation(step=2 * 24, money=50000.0), CONFIGURATION)
    assert agent._regime is None
    assert agent.telemetry_snapshot()["mode_decisions"] == 0
    # Inside the window: exactly one decision, locked.
    agent(_observation(step=5 * 24, money=50000.0), CONFIGURATION)
    assert agent._regime is not None
    assert agent.telemetry_snapshot()["mode_decisions"] == 1
    decided_regime = agent._regime
    # Later calls, even with a very different opponent snapshot, do not
    # re-decide: the choice is sticky for the rest of the episode.
    opp_farm = _opponent_farm(unlocked=("NW", "NE", "SW"), hands=[(0, 0)] * 10, crop_tiles=50, animal_tiles=15)
    agent(_observation(step=20 * 24, money=50000.0, opponent_farm=opp_farm), CONFIGURATION)
    assert agent._regime == decided_regime
    assert agent.telemetry_snapshot()["mode_decisions"] == 1


def test_regime_decision_is_forced_by_the_end_of_the_window_even_with_no_opponent_evidence() -> None:
    agent = create_claude_e18_agent_v2()
    end_day = agent.config.snapshot_window_end_day
    agent(_observation(step=end_day * 24, money=50000.0), CONFIGURATION)
    assert agent._regime is not None
    assert agent.telemetry_snapshot()["mode_decisions"] == 1


# ---------------------------------------------------------------------------
# Layer 4: CAPACITY_AND_LIFECYCLE_CONTROLLER -- crop lifecycle
# ---------------------------------------------------------------------------


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


def test_late_strawberry_is_marked_for_rotation_dig_not_left_to_expire() -> None:
    """Required fixture: late Strawberry -> DIG."""

    agent = create_claude_e18_agent_v2()
    step = 10 * 24
    obs = _observation(step=step, farmer=(1, 1), money=50000.0)
    # Close to its engine-reported expiry, already fully harvested
    # (yield_units == 0): nothing left to lose by digging it now.
    obs["farms"][0]["tiles"][1][1] = _strawberry_tile(
        planted_day=0, current_step=step, lifespan_margin=10, yield_units=0
    )
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["DIG"]


def test_strawberry_with_pending_yield_is_harvested_before_being_dug() -> None:
    """A late Strawberry that still holds unharvested yield must not lose
    that value: HARVEST first, DIG only once yield_units is back to zero."""

    agent = create_claude_e18_agent_v2()
    step = 10 * 24
    obs = _observation(step=step, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _strawberry_tile(
        planted_day=0, current_step=step, lifespan_margin=10, yield_units=2
    )
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["HARVEST"]


def test_wheat_is_not_harvested_at_the_first_available_unit() -> None:
    """Required invariant: Wheat alive and not yet at its yield target is
    KEPT, not harvested prematurely, when waiting increases the yield."""

    agent = create_claude_e18_agent_v2()
    # WHEAT's accumulation window is age 2-4 (max_yield_day=4); age=3 here
    # is still inside it, so a yield of 1 (well under the ratio target of
    # 4) must not be harvested yet -- there are still watering-bonus days
    # left before the window closes at age 4.
    obs = _observation(step=3 * 24, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _wheat_tile(planted_day=0, yield_units=1)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] != ["HARVEST"]


def test_wheat_is_harvested_once_it_reaches_its_yield_target() -> None:
    agent = create_claude_e18_agent_v2()
    # Still inside the accumulation window (age 4 == max_yield_day), but
    # yield_units has already reached the ratio target (4): harvest now
    # rather than waiting for the window to force it.
    obs = _observation(step=4 * 24, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _wheat_tile(planted_day=0, yield_units=4)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["HARVEST"]


def test_wheat_harvest_is_never_deferred_past_the_liquidation_window() -> None:
    """Safety fallback: deferring a harvest must never survive into the
    liquidation window, regardless of the yield ratio reached."""

    agent = create_claude_e18_agent_v2()
    turns_per_day = 24
    liquidation_days = agent.config.liquidation_days_remaining
    step = CONFIGURATION["episodeSteps"] - liquidation_days * turns_per_day - 1
    obs = _observation(step=step, farmer=(1, 1), money=50000.0)
    obs["farms"][0]["tiles"][1][1] = _wheat_tile(planted_day=0, yield_units=1)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["HARVEST"]


def test_urgent_water_still_outranks_a_deferred_harvest() -> None:
    """Required invariant: no serviceable tile is abandoned to weed for
    workforce starvation -- URGENT_WATER always wins the priority race."""

    agent = create_claude_e18_agent_v2()
    obs = _observation(step=5 * 24, farmer=(0, 0), money=50000.0)
    obs["farms"][0]["tiles"][0][0] = _wheat_tile(planted_day=0, watered=False, yield_units=4)
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["WATER"]


def test_livestock_emergency_outranks_non_urgent_land_expansion() -> None:
    """Required fixture: an unfed animal must be serviced before a
    non-urgent BUY_LAND expansion order is even considered by dispatch."""

    agent = create_claude_e18_agent_v2()
    obs = _observation(step=200, farmer=(1, 1), money=50000.0, inventories=[{"WHEAT": 5}])
    obs["farms"][0]["tiles"][1][1] = {
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
    action = agent(obs, CONFIGURATION)
    assert action["farmer"] == ["FEED"]


# ---------------------------------------------------------------------------
# Layer 4: livestock zero-risk ledger
# ---------------------------------------------------------------------------


def test_no_animal_purchase_while_any_animal_is_unfed() -> None:
    agent = create_claude_e18_agent_v2()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    obs = _observation(step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=[(0, 1), (0, 2)])
    livestock_zone = {(0, 0), (1, 0), (2, 0)}
    tiles = obs["farms"][0]["tiles"]
    placed = 0
    for y in range(5):
        for x in range(5):
            if (x, y) in livestock_zone or (x, y) == (4, 4):
                continue
            if placed >= 9:
                break
            tiles[y][x] = _wheat_tile(planted_day=0, yield_units=4)
            placed += 1
    tiles[2][2] = {
        "kind": "PASTURE",
        "animal": "SHEEP",
        "placed_day": 0,
        "yield_units": 0,
        "consecutive_unfed": 0,
        "fed_today": False,
        "cared_today": False,
        "fertilizer_available": False,
        "pending_care_bonus": 0,
    }
    tiles[2][3] = {"kind": "PASTURE"}
    obs["private"]["shed"] = {"SHEEP": 1}
    action = agent(obs, CONFIGURATION)
    assert not any(order[0] == "BUY_ANIMAL" for order in action["market"])


# ---------------------------------------------------------------------------
# Real config consumption
# ---------------------------------------------------------------------------


def test_config_is_actually_read_and_changes_behavior() -> None:
    base_payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        strict_payload = deepcopy(base_payload)
        strict_payload["opponent_snapshot"]["pressure_threshold"] = 100000.0
        strict_path = tmp_path / "strict.json"
        strict_path.write_text(json.dumps(strict_payload), encoding="utf-8")

        permissive_payload = deepcopy(base_payload)
        permissive_payload["opponent_snapshot"]["pressure_threshold"] = -1.0
        permissive_path = tmp_path / "permissive.json"
        permissive_path.write_text(json.dumps(permissive_payload), encoding="utf-8")

        obs = _observation(step=5 * 24, money=50000.0)
        strict_agent = create_claude_e18_agent_v2(config_path=strict_path)
        strict_agent(deepcopy(obs), CONFIGURATION)
        permissive_agent = create_claude_e18_agent_v2(config_path=permissive_path)
        permissive_agent(deepcopy(obs), CONFIGURATION)

    assert strict_agent._regime == strict_agent.config.regime_low.name
    assert permissive_agent._regime == permissive_agent.config.regime_high.name


def test_config_is_frozen_and_holdout_not_consumed() -> None:
    payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    assert payload["provenance"]["holdout_consumed"] is False
    assert payload["provenance"]["final_confirmation_consumed"] is False
    config = ReactiveConfigE18V2.load(DEFAULT_CONFIG_PATH)
    assert config.target_quadrants == 3
    assert config.regime_low.name != config.regime_high.name


# ---------------------------------------------------------------------------
# V2 remediation: proactive wheat buffer (MODEL_SPEC V2, item 1)
# ---------------------------------------------------------------------------


def test_wheat_buffer_is_stocked_before_any_animal_exists() -> None:
    """Reproduces the fix for V1's traced escape (seed 180903001 vs Codex
    E18 seat 1): a SHEEP placed day 11 with zero WHEAT in the shed starved
    within two days. V2 must buy the feed buffer as soon as a livestock
    structure exists, not wait for `animal_headcount > 0`."""

    agent = create_claude_e18_agent_v2()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    obs = _observation(step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=[(0, 1), (0, 2)])
    livestock_zone = {(0, 0), (1, 0), (2, 0)}
    tiles = obs["farms"][0]["tiles"]
    placed = 0
    for y in range(5):
        for x in range(5):
            if (x, y) in livestock_zone or (x, y) == (4, 4):
                continue
            if placed >= 9:
                break
            tiles[y][x] = _wheat_tile(planted_day=0, yield_units=4)
            placed += 1
    tiles[2][2] = {"kind": "PASTURE"}  # empty structure, no animal yet
    action = agent(obs, CONFIGURATION)
    assert any(order[0] == "BUY_WHEAT" for order in action["market"])


def test_animal_purchase_waits_for_the_wheat_buffer() -> None:
    agent = create_claude_e18_agent_v2()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    obs = _observation(step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=[(0, 1), (0, 2)])
    livestock_zone = {(0, 0), (1, 0), (2, 0)}
    tiles = obs["farms"][0]["tiles"]
    placed = 0
    for y in range(5):
        for x in range(5):
            if (x, y) in livestock_zone or (x, y) == (4, 4):
                continue
            if placed >= 9:
                break
            tiles[y][x] = _wheat_tile(planted_day=0, yield_units=4)
            placed += 1
    tiles[2][2] = {"kind": "PASTURE"}
    obs["private"]["shed"] = {"SHEEP": 1, "WHEAT": 0}
    action = agent(obs, CONFIGURATION)
    assert not any(order[0] == "BUY_ANIMAL" for order in action["market"])

    obs["private"]["shed"] = {"SHEEP": 1, "WHEAT": agent.config.feed_security_buffer_per_animal}
    action = agent(obs, CONFIGURATION)
    assert any(order[0] == "BUY_ANIMAL" for order in action["market"])


# ---------------------------------------------------------------------------
# V2 remediation: emergency queue (MODEL_SPEC V2, item 2)
# ---------------------------------------------------------------------------


def test_emergency_queue_suppresses_land_and_seed_orders_while_animal_at_risk() -> None:
    agent = create_claude_e18_agent_v2()
    agent._core_harvest_requests = agent.config.core_min_harvest_requests
    obs = _observation(
        step=200, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=[(0, 1), (0, 2)]
    )
    livestock_zone = {(0, 0), (1, 0), (2, 0)}
    tiles = obs["farms"][0]["tiles"]
    placed = 0
    for y in range(5):
        for x in range(5):
            if (x, y) in livestock_zone or (x, y) == (4, 4):
                continue
            if placed >= 9:
                break
            tiles[y][x] = _wheat_tile(planted_day=0, yield_units=4)
            placed += 1
    tiles[2][2] = {
        "kind": "PASTURE",
        "animal": "SHEEP",
        "placed_day": 0,
        "yield_units": 0,
        "consecutive_unfed": 0,
        "fed_today": False,
        "cared_today": False,
        "fertilizer_available": False,
        "pending_care_bonus": 0,
    }
    action = agent(obs, CONFIGURATION)
    assert ["BUY_LAND"] not in action["market"]
    assert not any(order[0] == "BUY_SEED" for order in action["market"])


# ---------------------------------------------------------------------------
# V2 remediation: crop surface capped to workforce (MODEL_SPEC V2, item 5)
# ---------------------------------------------------------------------------


def test_plant_opportunities_are_capped_to_current_workforce_capacity() -> None:
    cfg = ReactiveConfigE18V2.load(DEFAULT_CONFIG_PATH)
    obs = _observation(step=100, money=50000.0, unlocked=("NW",), farmer=(4, 4), hands=())
    snap = CodexObservationAdapter.parse(
        obs,
        CONFIGURATION,
        fallback_turns_per_day=cfg.fallback_turns_per_day,
        fallback_episode_steps=cfg.fallback_episode_steps,
    )
    feat = _extract_features(cfg, cfg.regime_low, snap)
    plant_opportunities = [o for o in feat.opportunities if o["kind"] == "PLANT_OPPORTUNITY"]
    # A single worker (farmer only, no hands) caps new planting at
    # `max_serviceable_crop_tiles_per_worker` (default 3.0) tiles, far
    # below what the 55% per-quadrant fill ratio alone would offer on an
    # entirely empty NW quadrant.
    assert len(plant_opportunities) <= int(cfg.max_serviceable_crop_tiles_per_worker)


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


def test_source_never_reads_private_opponent_state() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    assert "farms[opponent_seat]" in source or "opp_farm" in source
    # The opponent snapshot function must only ever touch the per-farm
    # `tiles`/`hands`/`unlocked_quadrants`, never a `private` key.
    snapshot_fn_start = source.index("def _extract_opponent_snapshot")
    snapshot_fn_end = source.index("\n\n\n", snapshot_fn_start)
    snapshot_fn_body = source[snapshot_fn_start:snapshot_fn_end]
    # Docstring prose may explain the constraint in words; only the actual
    # access pattern (`.private`, `["private"]`, `.get("private"`) matters.
    assert '"private"' not in snapshot_fn_body
    assert "'private'" not in snapshot_fn_body
    assert ".private" not in snapshot_fn_body


def test_policy_fingerprint_is_a_distinct_sha256() -> None:
    fingerprint = claude_policy_fingerprint()
    assert len(fingerprint) == 64
    assert all(c in "0123456789ABCDEF" for c in fingerprint)

    from agricola.strategy.claude.e17_reactive_3q_v3 import (
        claude_policy_fingerprint as v3_fingerprint,
    )
    from agricola.strategy.claude.e18_opponent_reactive_v1 import (
        claude_policy_fingerprint as v1_fingerprint,
    )

    assert fingerprint != v3_fingerprint()
    assert fingerprint != v1_fingerprint()


# ---------------------------------------------------------------------------
# Episode smoke (real engine)
# ---------------------------------------------------------------------------


def test_short_episode_smoke_completes_without_technical_errors() -> None:
    agent = create_claude_e18_agent_v2()
    env = kaggle_environments.make(
        "kaggriculture", configuration={"episodeSteps": 96, "seed": 180903001}
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
    policy = create_claude_e18_agent_v2()
    reference = create_claude_e18_agent_v2()
    ledger = E17CommandLedger(
        {
            "episode_id": "E18-CLAUDE-V1-UNIT",
            "seed": 180903001,
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
