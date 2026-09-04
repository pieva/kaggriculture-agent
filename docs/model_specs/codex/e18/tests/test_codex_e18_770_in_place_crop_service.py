"""Contract tests for E18.7 exact-7-7-0 in-place crop service."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_770_in_place_crop_service import (
    E18_770_IN_PLACE_SERVICE_MODEL_SPEC_VERSION,
    create_codex_e18_770_in_place_crop_service,
    load_e18_770_in_place_service_config,
)


def _observation(
    *,
    positions: list[tuple[int, int]],
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
            "seeds": {"STRAWBERRY": 5, "WHEAT": 5},
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


def test_config_freezes_every_non_service_dimension() -> None:
    config = load_e18_770_in_place_service_config()
    assert config["model_spec_version"] == (
        E18_770_IN_PLACE_SERVICE_MODEL_SPEC_VERSION
    )
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["max_service_distance"] == 0
    assert config["local_service_opcodes"] == ["HARVEST", "WATER"]
    assert config["allow_plant"] is False
    assert config["allow_dig"] is False
    assert config["allow_cross_quadrant_routing"] is False
    assert config["market_mutation"] is False
    assert config["calendar_mutation"] is False
    assert config["worker_count_mutation"] is False
    assert config["livestock_cap_mutation"] is False


def test_pass_on_ready_crop_becomes_in_place_harvest() -> None:
    observation = _observation(positions=[(1, 1)])
    _plant(
        observation,
        (1, 1),
        planted_day=1,
        yield_units=3,
        watered=False,
    )
    policy = create_codex_e18_770_in_place_crop_service(
        base_policy=_provider([["PASS"]])
    )
    action = policy(observation, {"maxMarketOrdersPerTurn": 10})
    assert action["farmer"] == ["HARVEST"]


def test_pass_on_immature_unwatered_crop_becomes_in_place_water() -> None:
    observation = _observation(positions=[(1, 1)], day=3)
    _plant(
        observation,
        (1, 1),
        planted_day=2,
        yield_units=0,
        watered=False,
    )
    policy = create_codex_e18_770_in_place_crop_service(
        base_policy=_provider([["PASS"]])
    )
    action = policy(observation, {"maxMarketOrdersPerTurn": 10})
    assert action["farmer"] == ["WATER"]


def test_non_pass_provider_command_is_authoritative() -> None:
    observation = _observation(positions=[(1, 1)])
    _plant(
        observation,
        (1, 1),
        planted_day=1,
        yield_units=3,
        watered=False,
    )
    policy = create_codex_e18_770_in_place_crop_service(
        base_policy=_provider([["NORTH"]])
    )
    action = policy(observation, {"maxMarketOrdersPerTurn": 10})
    assert action["farmer"] == ["NORTH"]
    telemetry = policy.codex_e18_770_in_place_service_instance.telemetry_snapshot()
    assert telemetry["non_pass_overrides"] == 0
    assert telemetry["cross_quadrant_routes"] == 0
    assert telemetry["max_observed_service_distance"] == 0


def test_only_one_pass_is_replaced_per_quadrant_and_turn() -> None:
    observation = _observation(positions=[(1, 1), (2, 1)])
    for position in ((1, 1), (2, 1)):
        _plant(
            observation,
            position,
            planted_day=10,
            yield_units=0,
            watered=False,
        )
    policy = create_codex_e18_770_in_place_crop_service(
        base_policy=_provider([["PASS"], ["PASS"]])
    )
    action = policy(observation, {"maxMarketOrdersPerTurn": 10})
    assert [action["farmer"], *action["hands"]].count(["WATER"]) == 1
    assert [action["farmer"], *action["hands"]].count(["PASS"]) == 1


def test_inventory_blocks_harvest_and_empty_or_weed_tiles_stay_pass() -> None:
    observation = _observation(
        positions=[(1, 1), (2, 1), (3, 1)],
        inventories=[{"WHEAT": 1}, {}, {}],
    )
    _plant(
        observation,
        (1, 1),
        planted_day=1,
        yield_units=3,
        watered=False,
    )
    observation["farms"][0]["tiles"][1][2] = {"kind": "WEED"}
    policy = create_codex_e18_770_in_place_crop_service(
        base_policy=_provider([["PASS"], ["PASS"], ["PASS"]])
    )
    action = policy(observation, {"maxMarketOrdersPerTurn": 10})
    assert action["farmer"] == ["PASS"]
    assert action["hands"] == [["PASS"], ["PASS"]]
    telemetry = policy.codex_e18_770_in_place_service_instance.telemetry_snapshot()
    assert telemetry["in_place_inventory_blocks"] == 1
