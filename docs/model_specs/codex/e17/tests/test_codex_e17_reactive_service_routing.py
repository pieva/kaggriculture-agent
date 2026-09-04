from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_reactive_service_routing import (
    SERVICE_ROUTING_MODEL_SPEC_VERSION,
    create_codex_e17_reactive_service_routing_agent,
    load_service_routing_config,
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


def _clear_farm(observation: dict) -> tuple[dict, dict, tuple[int, int]]:
    farm = observation["farms"][observation["player"]]
    private = observation["private"]
    for row in farm["tiles"]:
        for index, tile in enumerate(row):
            if tile != "LOCKED":
                row[index] = None
    positions = [farm["farmer"], *farm.get("hands", [])]
    private["inventories"] = [{} for _ in positions]
    farmer_position = tuple(farm["farmer"])
    return farm, private, farmer_position


def _adjacent(position: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    if x < 9:
        return x + 1, y
    return x - 1, y


def test_config_limits_change_to_service_and_routing() -> None:
    config = load_service_routing_config()
    assert config["model_spec_version"] == SERVICE_ROUTING_MODEL_SPEC_VERSION
    assert config["causal_family"] == "REACTIVE_SERVICE_AND_ROUTING"
    assert config["base_policy"] == "CODEX-E17.1-TRUE-REACTIVE-V2"


def test_critical_water_routes_then_services_from_observed_state() -> None:
    observation, configuration = _observation(21)
    farm, _private, source = _clear_farm(observation)
    target = _adjacent(source)
    farm["tiles"][target[1]][target[0]] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 0,
        "yield_units": 0,
        "watered_today": False,
        "consecutive_unwatered": 1,
        "fertilized_until_day": -1,
    }
    candidate = create_codex_e17_reactive_service_routing_agent()
    first = candidate(deepcopy(observation), configuration)
    assert first["farmer"][0] in {"EAST", "WEST"}

    following = deepcopy(observation)
    following["step"] = 22
    following["day"] = 0
    following["hour"] = 22
    following["farms"][following["player"]]["farmer"] = list(target)
    second = candidate(following, configuration)
    assert second["farmer"] == ["WATER"]
    telemetry = candidate.codex_e17_service_routing_instance.telemetry_snapshot()
    assert telemetry["routing_overrides"] >= 1
    assert telemetry["service_overrides"] >= 1


def test_critical_feed_stages_wheat_at_shed() -> None:
    observation, configuration = _observation(23)
    farm, private, _source = _clear_farm(observation)
    farm["farmer"] = [4, 4]
    farm["tiles"][0][0] = {
        "kind": "PASTURE",
        "animal": "COW",
        "placed_day": 0,
        "yield_units": 0,
        "fed_today": False,
        "cared_today": False,
        "consecutive_unfed": 1,
        "fertilizer_available": False,
    }
    private["inventories"][0] = {}
    private.setdefault("shed", {})["WHEAT"] = 6
    candidate = create_codex_e17_reactive_service_routing_agent()
    action = candidate(observation, configuration)
    assert action["farmer"] == ["PICKUP", "WHEAT", 6]


def test_feasible_structural_provider_action_is_preserved() -> None:
    observation, configuration = _observation(4)
    farm = observation["farms"][observation["player"]]
    private = observation["private"]
    position = tuple(farm["farmer"])
    farm["tiles"][position[1]][position[0]] = None
    private.setdefault("seeds", {})["MELON"] = 10
    provider = create_codex_e17_true_reactive_agent()(
        deepcopy(observation), configuration
    )
    assert provider["farmer"] == ["PLANT", "MELON"]
    candidate = create_codex_e17_reactive_service_routing_agent()
    emitted = candidate(observation, configuration)
    assert emitted["farmer"] == provider["farmer"]
    assert candidate.codex_e17_service_routing_instance.feasible_structural_mutations == 0


def test_market_block_is_always_provider_owned() -> None:
    observation, configuration = _observation(215)
    provider = create_codex_e17_true_reactive_agent()(
        deepcopy(observation), configuration
    )
    candidate = create_codex_e17_reactive_service_routing_agent()
    emitted = candidate(deepcopy(observation), configuration)
    assert emitted["market"] == provider["market"]
    assert candidate.codex_e17_service_routing_instance.market_mutations == 0


def test_same_initial_state_is_deterministic() -> None:
    observation, configuration = _observation(215)
    first = create_codex_e17_reactive_service_routing_agent()(
        deepcopy(observation), configuration
    )
    second = create_codex_e17_reactive_service_routing_agent()(
        deepcopy(observation), configuration
    )
    assert first == second


def test_short_smoke_has_no_policy_or_contract_errors() -> None:
    candidate = create_codex_e17_reactive_service_routing_agent()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 96, "seed": 26090101, "turnsPerDay": 24},
        debug=True,
    )
    env.run([candidate, inert_pass_policy])
    instance = candidate.codex_e17_service_routing_instance
    telemetry = instance.telemetry_snapshot()
    assert instance.error_count == 0
    assert instance.fallback_count == 0
    assert telemetry["market_mutations"] == 0
    assert telemetry["feasible_structural_mutations"] == 0
    assert sum(telemetry["execution_outcomes"].values()) == telemetry["override_commands"]
