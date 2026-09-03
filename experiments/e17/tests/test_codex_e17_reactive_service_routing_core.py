from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_reactive_service_routing_core import (
    CORE_MODEL_SPEC_VERSION,
    create_codex_e17_reactive_service_routing_core,
    load_core_config,
)
from agricola.strategy.codex.codex_e17_true_reactive import (
    create_codex_e17_true_reactive_agent,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
REPLAY = REPO_ROOT / "data/replays/json/104498819.json"


def _observation(step: int) -> tuple[dict, dict]:
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    return (
        deepcopy(replay["steps"][step][0]["observation"]),
        deepcopy(replay["configuration"]),
    )


def _clear_owned_tiles(observation: dict) -> tuple[dict, dict]:
    farm = observation["farms"][observation["player"]]
    for row in farm["tiles"]:
        for index, tile in enumerate(row):
            if tile != "LOCKED":
                row[index] = None
    return farm, observation["private"]


def test_core_config_freezes_progressive_activation() -> None:
    config = load_core_config()
    assert config["model_spec_version"] == CORE_MODEL_SPEC_VERSION
    assert config["causal_family"] == "REACTIVE_SERVICE_AND_ROUTING_CORE"
    assert config["base_policy"] == "CODEX-E17.1-TRUE-REACTIVE-V2"
    assert config["activation_day"] == 29


def test_pre_activation_action_is_exact_provider_action() -> None:
    observation, configuration = _observation(215)
    provider = create_codex_e17_true_reactive_agent()(
        deepcopy(observation), configuration
    )
    candidate = create_codex_e17_reactive_service_routing_core()
    emitted = candidate(deepcopy(observation), configuration)
    assert emitted == provider


def test_terminal_ready_crop_is_harvested_from_observed_state() -> None:
    observation, configuration = _observation(696)
    farm, private = _clear_owned_tiles(observation)
    farmer = tuple(farm["farmer"])
    farm["tiles"][farmer[1]][farmer[0]] = {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "planted_day": 0,
        "yield_units": 3,
        "watered_today": False,
        "consecutive_unwatered": 0,
        "fertilized_until_day": -1,
    }
    private["inventories"] = [
        {} for _ in [farm["farmer"], *farm.get("hands", [])]
    ]
    candidate = create_codex_e17_reactive_service_routing_core()
    action = candidate(observation, configuration)
    assert action["farmer"] == ["HARVEST"]


def test_terminal_inventory_is_routed_to_shed_and_dropped() -> None:
    observation, configuration = _observation(696)
    farm, private = _clear_owned_tiles(observation)
    farm["farmer"] = [4, 4]
    private["inventories"] = [
        {"STRAWBERRY": 3},
        *({} for _ in farm.get("hands", [])),
    ]
    candidate = create_codex_e17_reactive_service_routing_core()
    action = candidate(observation, configuration)
    assert action["farmer"] == ["DROP"]


def test_market_remains_byte_equivalent_to_provider() -> None:
    observation, configuration = _observation(696)
    provider = create_codex_e17_true_reactive_agent()(
        deepcopy(observation), configuration
    )
    candidate = create_codex_e17_reactive_service_routing_core()
    emitted = candidate(deepcopy(observation), configuration)
    assert emitted["market"] == provider["market"]
    assert candidate.codex_e17_service_routing_core_instance.market_mutations == 0


def test_same_initial_state_is_deterministic() -> None:
    observation, configuration = _observation(696)
    first = create_codex_e17_reactive_service_routing_core()(
        deepcopy(observation), configuration
    )
    second = create_codex_e17_reactive_service_routing_core()(
        deepcopy(observation), configuration
    )
    assert first == second


def test_full_episode_has_complete_classified_core_ledger() -> None:
    candidate = create_codex_e17_reactive_service_routing_core()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    env.run([candidate, inert_pass_policy])
    instance = candidate.codex_e17_service_routing_core_instance
    telemetry = instance.telemetry_snapshot()
    assert instance.error_count == 0
    assert instance.fallback_count == 0
    assert telemetry["market_mutations"] == 0
    assert telemetry["routing_commands"] > 0
    assert telemetry["service_commands"] > 0
    assert sum(telemetry["execution_outcomes"].values()) == telemetry[
        "ledger_record_count"
    ]
