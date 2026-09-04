"""Contract tests for E18.11 invalid-command WATER recovery."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_770_invalid_command_water_recovery import (
    E18_770_INVALID_COMMAND_WATER_RECOVERY_MODEL_SPEC_VERSION,
    create_codex_e18_770_invalid_command_water_recovery,
    load_e18_770_invalid_command_water_recovery_config,
)


def _observation(
    *,
    day: int = 16,
    position: tuple[int, int] = (2, 2),
    watered: bool = False,
    yield_units: int = 0,
    fertilizer: int = 0,
) -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": list(position),
        "hands": [],
        "unlocked_quadrants": ["NW", "NE", "SW"],
    }
    x, y = position
    farm["tiles"][y][x] = {
        "kind": "PLANT",
        "crop": "STRAWBERRY",
        "planted_day": 9,
        "yield_units": yield_units,
        "watered_today": watered,
    }
    return {
        "step": day * 24,
        "day": day,
        "hour": 0,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {
            "shed": {},
            "inventories": [{"FERTILIZER": fertilizer}],
            "seeds": {"STRAWBERRY": 5},
        },
        "market": {"prices": {}},
    }


def _provider(command: list):
    def provider(observation, configuration=None):
        del observation, configuration
        return {
            "farmer": deepcopy(command),
            "hands": [],
            "market": [["SELL", "STRAWBERRY", 1]],
        }

    return provider


def test_config_freezes_topology_routes_and_provider_scope() -> None:
    config = load_e18_770_invalid_command_water_recovery_config()
    assert config["model_spec_version"] == (
        E18_770_INVALID_COMMAND_WATER_RECOVERY_MODEL_SPEC_VERSION
    )
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["allow_worker_rerouting"] is False
    assert config["replaceable_infeasible_opcodes"] == [
        "FERTILIZE",
        "HARVEST",
        "PLACE",
        "PLANT",
    ]


def test_known_infeasible_local_commands_become_water() -> None:
    for command in (
        ["FERTILIZE"],
        ["HARVEST"],
        ["PLACE", "SHEEP", 1],
        ["PLANT", "STRAWBERRY"],
    ):
        policy = create_codex_e18_770_invalid_command_water_recovery(
            base_policy=_provider(command)
        )
        action = {
            "farmer": deepcopy(command),
            "hands": [],
            "market": [["SELL", "STRAWBERRY", 1]],
        }
        (
            policy.codex_e18_770_invalid_command_water_recovery_instance
            ._apply_invalid_command_water_recovery(action, _observation())
        )
        assert action["farmer"] == ["WATER"]
        assert ["SELL", "STRAWBERRY", 1] in action["market"]


def test_feasible_fertilize_and_harvest_remain_authoritative() -> None:
    fertilize = create_codex_e18_770_invalid_command_water_recovery(
        base_policy=_provider(["FERTILIZE"])
    )
    assert fertilize(_observation(fertilizer=1), {})["farmer"] == [
        "FERTILIZE"
    ]
    harvest = create_codex_e18_770_invalid_command_water_recovery(
        base_policy=_provider(["HARVEST"])
    )
    assert harvest(_observation(yield_units=3), {})["farmer"] == ["HARVEST"]


def test_move_pass_watered_terminal_and_shed_access_are_immutable() -> None:
    cases = (
        (["NORTH"], _observation()),
        (["PASS"], _observation()),
        (["HARVEST"], _observation(watered=True)),
        (["HARVEST"], _observation(day=29)),
        (["PLACE", "SHEEP", 1], _observation(position=(4, 4))),
    )
    for command, observation in cases:
        policy = create_codex_e18_770_invalid_command_water_recovery(
            base_policy=_provider(command)
        )
        assert policy(observation, {})["farmer"] == command


def test_telemetry_attributes_only_infeasible_overrides() -> None:
    policy = create_codex_e18_770_invalid_command_water_recovery(
        base_policy=_provider(["FERTILIZE"])
    )
    policy(_observation(), {})
    telemetry = (
        policy.codex_e18_770_invalid_command_water_recovery_instance
        .telemetry_snapshot()
    )
    assert telemetry["infeasible_local_to_water"] == {"FERTILIZE": 1}
    assert telemetry["feasible_provider_overrides"] == 0
    assert telemetry["worker_route_mutations"] == 0
