"""Contract tests for E18.8 exact-7-7-0 adjacent crop queue."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_770_adjacent_crop_queue import (
    E18_770_ADJACENT_CROP_QUEUE_MODEL_SPEC_VERSION,
    create_codex_e18_770_adjacent_crop_queue,
    load_e18_770_adjacent_crop_queue_config,
)


def _observation(
    positions: list[tuple[int, int]],
    *,
    day: int = 11,
    inventories: list[dict] | None = None,
) -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": list(positions[0]),
        "hands": [list(value) for value in positions[1:]],
        "unlocked_quadrants": ["NW", "NE", "SW"],
    }
    return {
        "step": day * 24,
        "day": day,
        "hour": 0,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {
            "shed": {},
            "inventories": inventories or [{} for _ in positions],
            "seeds": {},
        },
        "market": {"prices": {}},
    }


def _provider(commands: list[list[str]]):
    def provider(observation, configuration=None):
        del observation, configuration
        return {
            "farmer": deepcopy(commands[0]),
            "hands": deepcopy(commands[1:]),
            "market": [],
        }

    return provider


def _plant(
    observation: dict,
    position: tuple[int, int],
    *,
    planted_day: int,
    yield_units: int,
    watered: bool,
) -> None:
    x, y = position
    observation["farms"][0]["tiles"][y][x] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": planted_day,
        "yield_units": yield_units,
        "watered_today": watered,
    }


def test_config_freezes_non_queue_dimensions() -> None:
    config = load_e18_770_adjacent_crop_queue_config()
    assert config["model_spec_version"] == (
        E18_770_ADJACENT_CROP_QUEUE_MODEL_SPEC_VERSION
    )
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["max_assignment_distance"] == 1
    assert config["provider_non_pass_authoritative"] is True
    assert config["allow_cross_quadrant_routing"] is False
    assert config["allow_plant"] is False
    assert config["allow_dig"] is False
    assert config["market_mutation"] is False
    assert config["calendar_mutation"] is False
    assert config["worker_count_mutation"] is False
    assert config["livestock_cap_mutation"] is False


def test_adjacent_pass_moves_then_waters() -> None:
    first = _observation([(1, 1)], day=3)
    _plant(first, (2, 1), planted_day=2, yield_units=0, watered=False)
    policy = create_codex_e18_770_adjacent_crop_queue(
        base_policy=_provider([["PASS"]])
    )
    action = policy(first, {})
    assert action["farmer"] == ["EAST"]

    second = deepcopy(first)
    second["farms"][0]["farmer"] = [2, 1]
    second["step"] += 1
    action = policy(second, {})
    assert action["farmer"] == ["WATER"]
    telemetry = policy.codex_e18_770_adjacent_crop_queue_instance.telemetry_snapshot()
    assert telemetry["adjacent_queue_assignments"] == 1
    assert telemetry["adjacent_queue_completions"] == 1


def test_in_place_harvest_is_still_available() -> None:
    observation = _observation([(1, 1)])
    _plant(observation, (1, 1), planted_day=1, yield_units=3, watered=False)
    policy = create_codex_e18_770_adjacent_crop_queue(
        base_policy=_provider([["PASS"]])
    )
    assert policy(observation, {})["farmer"] == ["HARVEST"]


def test_provider_non_pass_cancels_mission_without_override() -> None:
    observation = _observation([(1, 1)], day=3)
    _plant(observation, (2, 1), planted_day=2, yield_units=0, watered=False)
    commands = [["PASS"]]

    def provider(obs, configuration=None):
        del obs, configuration
        return {"farmer": deepcopy(commands[0]), "hands": [], "market": []}

    policy = create_codex_e18_770_adjacent_crop_queue(base_policy=provider)
    assert policy(observation, {})["farmer"] == ["EAST"]
    commands[0] = ["NORTH"]
    observation["farms"][0]["farmer"] = [2, 1]
    assert policy(observation, {})["farmer"] == ["NORTH"]
    telemetry = policy.codex_e18_770_adjacent_crop_queue_instance.telemetry_snapshot()
    assert telemetry["adjacent_queue_cancellations"] == 1
    assert telemetry["non_pass_overrides"] == 0


def test_cross_quadrant_adjacent_task_is_not_routed() -> None:
    observation = _observation([(4, 1)], day=3)
    _plant(observation, (5, 1), planted_day=2, yield_units=0, watered=False)
    policy = create_codex_e18_770_adjacent_crop_queue(
        base_policy=_provider([["PASS"]])
    )
    assert policy(observation, {})["farmer"] == ["PASS"]
    telemetry = policy.codex_e18_770_adjacent_crop_queue_instance.telemetry_snapshot()
    assert telemetry["cross_quadrant_routes"] == 0


def test_distance_two_and_inventory_block_remain_pass() -> None:
    observation = _observation([(1, 1), (3, 1)], inventories=[{}, {"WHEAT": 1}])
    _plant(observation, (3, 1), planted_day=1, yield_units=3, watered=False)
    policy = create_codex_e18_770_adjacent_crop_queue(
        base_policy=_provider([["PASS"], ["PASS"]])
    )
    action = policy(observation, {})
    assert action["farmer"] == ["PASS"]
    assert action["hands"] == [["PASS"]]
