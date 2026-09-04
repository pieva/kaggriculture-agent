from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_reactive_service_routing_v3 import (
    V3_MODEL_SPEC_VERSION,
    create_codex_e17_reactive_service_routing_v3,
    load_v3_config,
)
from agricola.strategy.codex.codex_e17_true_reactive import (
    create_codex_e17_true_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
REPLAY = REPO_ROOT / "data/replays/json/104498819.json"


def _observation(step: int) -> tuple[dict, dict]:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    return (
        deepcopy(replay["steps"][step][0]["observation"]),
        deepcopy(replay["configuration"]),
    )


def _clear_farm(observation: dict, *, hands: bool = True) -> tuple[dict, dict]:
    farm = observation["farms"][observation["player"]]
    for row in farm["tiles"]:
        for index, tile in enumerate(row):
            if tile != "LOCKED":
                row[index] = None
    if not hands:
        farm["hands"] = []
    private = observation["private"]
    private["inventories"] = [
        {} for _ in [farm["farmer"], *farm.get("hands", [])]
    ]
    return farm, private


def test_v3_config_freezes_d28_handoff_and_d29_liquidation() -> None:
    config = load_v3_config()
    assert config["model_spec_version"] == V3_MODEL_SPEC_VERSION
    assert config["activation_day"] == 28
    assert config["liquidation_day"] == 29
    assert config["causal_family"] == (
        "REACTIVE_SERVICE_ROUTING_AND_TERMINAL_LIQUIDATION"
    )


def test_pre_activation_action_is_exact_provider_action() -> None:
    observation, configuration = _observation(215)
    provider = create_codex_e17_true_reactive_agent()(
        deepcopy(observation), configuration
    )
    candidate = create_codex_e17_reactive_service_routing_v3()
    assert candidate(deepcopy(observation), configuration) == provider


def test_d28_stages_wheat_for_normal_unfed_animal() -> None:
    observation, configuration = _observation(672)
    farm, private = _clear_farm(observation, hands=False)
    farm["farmer"] = [4, 4]
    farm["tiles"][0][0] = {
        "kind": "PASTURE",
        "animal": "COW",
        "placed_day": 0,
        "yield_units": 0,
        "fed_today": False,
        "cared_today": False,
        "consecutive_unfed": 0,
        "fertilizer_available": False,
    }
    private["inventories"] = [{}]
    private.setdefault("shed", {})["WHEAT"] = 6
    candidate = create_codex_e17_reactive_service_routing_v3()
    assert candidate(observation, configuration)["farmer"] == [
        "PICKUP",
        "WHEAT",
        6,
    ]


def test_d28_routes_non_feed_output_to_shed() -> None:
    observation, configuration = _observation(672)
    farm, private = _clear_farm(observation, hands=False)
    farm["farmer"] = [4, 4]
    private["inventories"] = [{"MILK": 3}]
    candidate = create_codex_e17_reactive_service_routing_v3()
    assert candidate(observation, configuration)["farmer"] == ["DROP"]


def test_d29_same_batch_drop_is_added_to_market_sale() -> None:
    observation, configuration = _observation(697)
    farm, private = _clear_farm(observation, hands=False)
    farm["farmer"] = [4, 4]
    private["inventories"] = [{"TOMATO": 3}]
    private.setdefault("shed", {})["TOMATO"] = 0
    candidate = create_codex_e17_reactive_service_routing_v3()
    action = candidate(observation, configuration)
    assert action["farmer"] == ["DROP"]
    assert ["SELL", "TOMATO", 3] in action["market"]


def test_non_sell_provider_orders_are_preserved() -> None:
    observation, configuration = _observation(697)
    farm, private = _clear_farm(observation, hands=False)
    farm["farmer"] = [4, 4]
    private["inventories"] = [{"TOMATO": 3}]
    provider = create_codex_e17_true_reactive_agent()(
        deepcopy(observation), configuration
    )
    candidate = create_codex_e17_reactive_service_routing_v3()
    emitted = candidate(observation, configuration)
    before = [order for order in provider["market"] if order[0] != "SELL"]
    after = [order for order in emitted["market"] if order[0] != "SELL"]
    assert after == before


def test_unreachable_terminal_harvest_is_not_started() -> None:
    observation, configuration = _observation(718)
    farm, private = _clear_farm(observation, hands=False)
    farm["farmer"] = [9, 9]
    farm["tiles"][0][0] = {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "planted_day": 0,
        "yield_units": 4,
        "watered_today": False,
        "consecutive_unwatered": 0,
        "fertilized_until_day": -1,
    }
    private["inventories"] = [{}]
    candidate = create_codex_e17_reactive_service_routing_v3()
    assert candidate(observation, configuration)["farmer"] == ["PASS"]


def test_same_initial_state_is_deterministic() -> None:
    observation, configuration = _observation(672)
    first = create_codex_e17_reactive_service_routing_v3()(
        deepcopy(observation), configuration
    )
    second = create_codex_e17_reactive_service_routing_v3()(
        deepcopy(observation), configuration
    )
    assert first == second


def test_full_episode_has_complete_ledgers_and_natural_actions() -> None:
    candidate = create_codex_e17_reactive_service_routing_v3()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    env.run([candidate, inert_pass_policy])
    instance = candidate.codex_e17_service_routing_v3_instance
    telemetry = instance.telemetry_snapshot()
    assert instance.error_count == 0
    assert instance.fallback_count == 0
    assert telemetry["action_counts"]["FEED"] > 0
    assert telemetry["action_counts"]["WATER"] > 0
    assert telemetry["action_counts"]["DROP"] > 0
    assert telemetry["coordinated_sell_orders"] > 0
    assert telemetry["non_sell_preservation_failures"] == 0
    assert sum(telemetry["execution_outcomes"].values()) == telemetry[
        "ledger_record_count"
    ]
    assert telemetry["execution_outcomes"].get("NOT_EXECUTED", 0) == 0
    assert sum(telemetry["market_execution_outcomes"].values()) == telemetry[
        "market_ledger_record_count"
    ]
    terminal_private = env.steps[-1][0]["observation"]["private"]
    sellable = set(load_v3_config()["sellable_products"])
    assert not any(
        int(quantity or 0) > 0 and item in sellable
        for item, quantity in terminal_private["shed"].items()
    )
    assert not any(
        int(quantity or 0) > 0 and item in sellable
        for inventory in terminal_private["inventories"]
        for item, quantity in inventory.items()
    )
