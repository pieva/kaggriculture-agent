from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.core.observation_contract import stable_payload_hash
from agricola.strategy.codex.codex_e17_reactive_guarded import (
    create_codex_e17_reactive_agent,
)
from agricola.strategy.codex.codex_e17_true_reactive import (
    TRUE_REACTIVE_MODEL_SPEC_VERSION,
    create_codex_e17_true_reactive_agent,
    load_true_reactive_config,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
REPLAY = REPO_ROOT / "data/replays/json/104498819.json"
REFERENCE_PRICES = {
    "WHEAT": 25,
    "CARROT": 35,
    "TOMATO": 60,
    "STRAWBERRY": 120,
    "MELON": 250,
    "EGG": 50,
    "MILK": 160,
    "WOOL": 200,
    "FERTILIZER": 100,
}


def _observation(step: int) -> tuple[dict, dict]:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    observation = deepcopy(replay["steps"][step][0]["observation"])
    configuration = deepcopy(replay["configuration"])
    return observation, configuration


def _neutralize(observation: dict) -> None:
    observation["market"]["prices"] = deepcopy(REFERENCE_PRICES)
    player = observation["player"]
    observation["farms"][player]["money"] = 100_000
    private = observation["private"]
    private["shed"]["WHEAT"] = 0
    inventories = private.get("inventories", []) or []
    for inventory in inventories:
        if isinstance(inventory, dict):
            inventory["WHEAT"] = 0
    if inventories:
        inventories[0]["WHEAT"] = 100


def _sell_quantity(action: dict, item: str) -> int:
    return sum(
        int(order[2])
        for order in action.get("market", [])
        if isinstance(order, list) and len(order) >= 3 and order[:2] == ["SELL", item]
    )


def _has_order(action: dict, opcode: str) -> bool:
    return any(
        isinstance(order, list) and order and order[0] == opcode
        for order in action.get("market", [])
    )


def test_config_declares_one_market_causal_family() -> None:
    config = load_true_reactive_config()
    assert config["model_spec_version"] == TRUE_REACTIVE_MODEL_SPEC_VERSION
    assert config["causal_family"] == "MARKET_REGIME_ADAPTATION"
    assert config["base_policy"] == "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1"


def test_neutral_state_preserves_guarded_provider_action() -> None:
    observation, configuration = _observation(195)
    _neutralize(observation)
    provider = create_codex_e17_reactive_agent()(deepcopy(observation), configuration)
    candidate = create_codex_e17_true_reactive_agent()
    emitted = candidate(deepcopy(observation), configuration)
    assert emitted == provider
    assert candidate.codex_e17_true_reactive_instance.override_count == 0


def test_low_price_defers_a_scheduled_sale() -> None:
    observation, configuration = _observation(195)
    _neutralize(observation)
    observation["market"]["prices"]["MILK"] = 50
    provider = create_codex_e17_reactive_agent()(deepcopy(observation), configuration)
    assert _sell_quantity(provider, "MILK") > 0
    candidate = create_codex_e17_true_reactive_agent()
    emitted = candidate(deepcopy(observation), configuration)
    assert _sell_quantity(emitted, "MILK") == 0
    telemetry = candidate.codex_e17_true_reactive_instance.telemetry_snapshot()
    assert telemetry["true_reactive_override_reasons"]["LOW_PRICE_SALE_DEFERRED"] == 1


def test_deferred_sale_is_released_at_the_bounded_deadline() -> None:
    first, configuration = _observation(195)
    _neutralize(first)
    first["market"]["prices"]["MILK"] = 50
    candidate = create_codex_e17_true_reactive_agent()
    candidate(deepcopy(first), configuration)

    release, _ = _observation(201)
    _neutralize(release)
    release["private"]["shed"]["MILK"] = 12
    release["market"]["prices"]["MILK"] = 50
    emitted = candidate(release, configuration)
    assert _sell_quantity(emitted, "MILK") == 12
    telemetry = candidate.codex_e17_true_reactive_instance.telemetry_snapshot()
    assert telemetry["true_reactive_override_reasons"]["DEFERRED_SALE_RELEASED"] == 1


def test_high_price_sells_observed_shed_inventory_opportunistically() -> None:
    observation, configuration = _observation(194)
    _neutralize(observation)
    observation["private"]["shed"]["WOOL"] = 5
    observation["market"]["prices"]["WOOL"] = 400
    provider = create_codex_e17_reactive_agent()(deepcopy(observation), configuration)
    assert _sell_quantity(provider, "WOOL") == 0
    candidate = create_codex_e17_true_reactive_agent()
    emitted = candidate(deepcopy(observation), configuration)
    assert _sell_quantity(emitted, "WOOL") == 5


def test_wheat_scarcity_does_not_break_the_structural_purchase_plan() -> None:
    observation, configuration = _observation(195)
    _neutralize(observation)
    observation["private"]["shed"]["WHEAT"] = 0
    for inventory in observation["private"].get("inventories", []) or []:
        if isinstance(inventory, dict):
            inventory["WHEAT"] = 0
    observation["market"]["prices"]["WHEAT"] = 40
    provider = create_codex_e17_reactive_agent()(deepcopy(observation), configuration)
    assert _has_order(provider, "BUY_ANIMAL")
    candidate = create_codex_e17_true_reactive_agent()
    emitted = candidate(deepcopy(observation), configuration)
    assert _has_order(emitted, "BUY_ANIMAL")
    telemetry = candidate.codex_e17_true_reactive_instance.telemetry_snapshot()
    assert telemetry["market_regime_counts"]["INPUT_SCARCITY"] == 1


def test_paired_market_states_are_deterministic_and_discriminated() -> None:
    observation, configuration = _observation(195)
    _neutralize(observation)
    low = deepcopy(observation)
    low["market"]["prices"]["MILK"] = 50
    high = deepcopy(observation)
    high["market"]["prices"]["MILK"] = 240
    low_a = create_codex_e17_true_reactive_agent()(low, configuration)
    low_b = create_codex_e17_true_reactive_agent()(deepcopy(low), configuration)
    high_action = create_codex_e17_true_reactive_agent()(high, configuration)
    assert low_a == low_b
    assert stable_payload_hash(low_a) != stable_payload_hash(high_action)


def test_standard_development_episode_has_natural_overrides_and_no_errors() -> None:
    candidate = create_codex_e17_true_reactive_agent()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 240, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    env.run([candidate, inert_pass_policy])
    instance = candidate.codex_e17_true_reactive_instance
    assert env.steps[-1][0]["status"] == "DONE"
    assert instance.error_count == 0
    assert instance.fallback_count == 0
    assert instance.override_count > 0
