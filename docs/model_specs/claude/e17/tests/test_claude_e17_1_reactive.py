"""Tests for the Claude E17.1 3Q reactive independent controller.

Covers: factory/import, batch schema and limits, safe fallback, controlled
determinism, state reactivity, real config consumption, absence of
prohibited imports/tokens, a full episode smoke run, and ledger-wrapper
action parity.
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
from agricola.strategy.claude.e17_reactive_3q import (
    DEFAULT_CONFIG_PATH,
    POLICY_VERSION,
    SAFE_PASS_ACTION,
    ClaudeE17ReactiveAgent,
    ReactiveConfig,
    claude_policy_fingerprint,
    create_claude_e17_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
SOURCE_PATH = (
    REPO_ROOT / "src" / "agricola" / "strategy" / "claude" / "e17_reactive_3q.py"
)
CONFIGURATION = {
    "episodeSteps": 720,
    "turnsPerDay": 24,
    "boardSize": 10,
    "maxMarketOrdersPerTurn": 10,
    "shedCapacity": 100,
}


def _blank_farm(*, unlocked=("NW",), money=3000.0, farmer=(4, 4), hands=()):
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
):
    farm = _blank_farm(unlocked=unlocked, money=money, farmer=farmer, hands=hands)
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


# ---------------------------------------------------------------------------
# Factory and import
# ---------------------------------------------------------------------------


def test_factory_returns_callable_agent_with_expected_interface() -> None:
    agent = create_claude_e17_agent()
    assert isinstance(agent, ClaudeE17ReactiveAgent)
    assert agent.policy_version == POLICY_VERSION
    assert callable(agent)
    assert agent.technical_errors == 0
    action = agent(_observation(), CONFIGURATION)
    assert isinstance(action, dict)
    assert set(action) == {"farmer", "hands", "market"}


def test_factory_accepts_explicit_run_context_and_config_path() -> None:
    agent = create_claude_e17_agent(run_context={"note": "unit-test"}, config_path=DEFAULT_CONFIG_PATH)
    assert agent.run_context == {"note": "unit-test"}
    assert agent.config.policy_id == POLICY_VERSION


# ---------------------------------------------------------------------------
# Batch schema and limits
# ---------------------------------------------------------------------------


def test_action_schema_matches_shared_interface_contract() -> None:
    agent = create_claude_e17_agent()
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
    agent = create_claude_e17_agent()
    tight_configuration = dict(CONFIGURATION, maxMarketOrdersPerTurn=2)
    obs = _observation(money=50000.0, unlocked=("NW", "NE"))
    action = agent(obs, tight_configuration)
    assert len(action["market"]) <= 2


# ---------------------------------------------------------------------------
# Safe fallback
# ---------------------------------------------------------------------------


def test_malformed_observation_falls_back_to_safe_pass() -> None:
    agent = create_claude_e17_agent()
    before = agent.technical_errors
    action = agent({"not": "a valid observation"}, CONFIGURATION)
    assert action == SAFE_PASS_ACTION
    assert agent.technical_errors == before + 1


def test_non_mapping_observation_falls_back_to_safe_pass() -> None:
    agent = create_claude_e17_agent()
    action = agent(None, CONFIGURATION)  # type: ignore[arg-type]
    assert action == SAFE_PASS_ACTION
    assert agent.technical_errors == 1


# ---------------------------------------------------------------------------
# Controlled determinism
# ---------------------------------------------------------------------------


def test_same_observation_produces_identical_action() -> None:
    obs = _observation(hands=[(4, 3)], money=4000.0, unlocked=("NW", "NE"))
    first = create_claude_e17_agent()(deepcopy(obs), CONFIGURATION)
    second = create_claude_e17_agent()(deepcopy(obs), CONFIGURATION)
    assert first == second


def test_same_agent_instance_is_deterministic_across_repeated_calls() -> None:
    agent = create_claude_e17_agent()
    obs = _observation(hands=[(3, 4), (5, 5)], money=2500.0, unlocked=("NW", "NE", "SW"))
    first = agent(deepcopy(obs), CONFIGURATION)
    second = agent(deepcopy(obs), CONFIGURATION)
    assert first == second


# ---------------------------------------------------------------------------
# State reactivity
# ---------------------------------------------------------------------------


def test_reactivity_to_unwatered_plant_at_same_step() -> None:
    """Two observations at the same step but different farm state must
    produce an explainably different farmer command, without relying on a
    precompiled step index."""

    agent = create_claude_e17_agent()

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
    agent = create_claude_e17_agent()
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
        permissive_payload["workforce"]["max_hands"] = 12
        permissive_path = tmp_path / "permissive.json"
        permissive_path.write_text(json.dumps(permissive_payload), encoding="utf-8")

        obs = _observation(money=50000.0)
        strict_action = create_claude_e17_agent(config_path=strict_path)(
            deepcopy(obs), CONFIGURATION
        )
        permissive_action = create_claude_e17_agent(config_path=permissive_path)(
            deepcopy(obs), CONFIGURATION
        )

    strict_hires = sum(1 for order in strict_action["market"] if order[0] == "HIRE")
    permissive_hires = sum(1 for order in permissive_action["market"] if order[0] == "HIRE")
    assert strict_hires == 0
    assert permissive_hires > strict_hires


def test_config_target_fill_ratio_gates_plant_opportunities() -> None:
    base_payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as tmp_dir:
        zero_fill_payload = deepcopy(base_payload)
        zero_fill_payload["crop"]["target_fill_ratio"] = 0.0
        zero_fill_path = Path(tmp_dir) / "zero_fill.json"
        zero_fill_path.write_text(json.dumps(zero_fill_payload), encoding="utf-8")

        obs = _observation(money=5000.0, seeds={"WHEAT": 5})
        action = create_claude_e17_agent(config_path=zero_fill_path)(obs, CONFIGURATION)

    assert action["farmer"][0] != "PLANT"


def test_config_is_frozen_and_holdout_not_consumed() -> None:
    payload = json.loads(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    assert payload["provenance"]["holdout_consumed"] is False
    assert payload["provenance"]["final_confirmation_consumed"] is False
    config = ReactiveConfig.load(DEFAULT_CONFIG_PATH)
    assert config.target_quadrants == 3


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


def test_policy_fingerprint_is_a_distinct_sha256() -> None:
    fingerprint = claude_policy_fingerprint()
    assert len(fingerprint) == 64
    assert all(c in "0123456789ABCDEF" for c in fingerprint)
    codex_v9_routine_sha256 = (
        "C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4"
    )
    assert fingerprint != codex_v9_routine_sha256


# ---------------------------------------------------------------------------
# Episode smoke (real engine)
# ---------------------------------------------------------------------------


def test_short_episode_smoke_completes_without_technical_errors() -> None:
    agent = create_claude_e17_agent()
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
    policy = create_claude_e17_agent()
    reference = create_claude_e17_agent()
    ledger = E17CommandLedger(
        {
            "episode_id": "E17-1-CLAUDE-UNIT",
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
    expected_commands = (
        1 + len(wrapped_action["hands"]) + len(wrapped_action["market"])
    )
    assert len(ledger.records) == expected_commands
    assert ledger.metrics()["ledger_record_coverage"] == 1.0
    assert wrapped.e17_inner_policy is policy
    assert policy.technical_errors == 0


def test_ledger_errors_do_not_affect_returned_action(monkeypatch) -> None:
    policy = create_claude_e17_agent()
    ledger = E17CommandLedger({"episode_id": "E17-1-CLAUDE-FAULT", "seed": 1, "seat": 0})

    def _broken_record(*args, **kwargs):
        raise RuntimeError("simulated ledger failure")

    monkeypatch.setattr(ledger, "record", _broken_record)
    wrapped = instrument_policy(policy, ledger)

    obs = _observation()
    action = wrapped(deepcopy(obs), CONFIGURATION)
    assert action == policy(deepcopy(obs), CONFIGURATION)
    assert ledger.errors
