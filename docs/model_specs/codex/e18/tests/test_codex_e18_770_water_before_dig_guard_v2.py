"""Contract tests for the safe PASS-only E18.10 V2 guard."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_770_live_crop_rotation_guard import (
    create_codex_e18_770_live_crop_rotation_guard,
)
from agricola.strategy.codex.codex_e18_770_water_before_dig_guard_v2 import (
    E18_770_WATER_BEFORE_DIG_GUARD_V2_MODEL_SPEC_VERSION,
    create_codex_e18_770_water_before_dig_guard_v2,
    load_e18_770_water_before_dig_guard_v2_config,
)


def _observation(
    *,
    watered: bool = False,
    day: int = 21,
    position: tuple[int, int] = (3, 5),
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
        "planted_day": 11,
        "yield_units": 0,
        "watered_today": watered,
    }
    return {
        "step": day * 24,
        "day": day,
        "hour": 0,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {"shed": {}, "inventories": [{}], "seeds": {"WHEAT": 5}},
        "market": {"prices": {}},
    }


def _provider(command: list[str]):
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": deepcopy(command), "hands": [], "market": []}

    return provider


def test_config_requires_pass_only_and_freezes_routes() -> None:
    config = load_e18_770_water_before_dig_guard_v2_config()
    assert config["model_spec_version"] == (
        E18_770_WATER_BEFORE_DIG_GUARD_V2_MODEL_SPEC_VERSION
    )
    assert config["allowed_override"] == "PASS_TO_WATER_ONLY"
    assert config["provider_non_pass_authoritative"] is True
    assert config["allow_worker_rerouting"] is False
    assert config["excluded_shared_logistics_targets"] == [[4, 5]]
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}


def test_provider_pass_on_unwatered_protected_crop_becomes_water() -> None:
    policy = create_codex_e18_770_water_before_dig_guard_v2(
        base_policy=_provider(["PASS"])
    )
    assert policy(_observation(), {})["farmer"] == ["WATER"]
    telemetry = (
        policy.codex_e18_770_water_before_dig_guard_v2_instance.telemetry_snapshot()
    )
    assert telemetry["provider_pass_to_water_overrides"] == 1
    assert telemetry["provider_non_pass_overrides"] == 0


def test_provider_non_pass_is_never_overridden() -> None:
    for command in (["PICKUP", "SHEEP", 1], ["DROP"], ["PLACE", "SHEEP", 1]):
        policy = create_codex_e18_770_water_before_dig_guard_v2(
            base_policy=_provider(command)
        )
        control = create_codex_e18_770_live_crop_rotation_guard(
            base_policy=_provider(command)
        )
        assert policy(_observation(position=(4, 5)), {})["farmer"] == control(
            _observation(position=(4, 5)), {}
        )["farmer"]
        telemetry = (
            policy.codex_e18_770_water_before_dig_guard_v2_instance.telemetry_snapshot()
        )
        assert telemetry["provider_non_pass_overrides"] == 0


def test_watered_crop_and_outside_window_remain_pass() -> None:
    policy = create_codex_e18_770_water_before_dig_guard_v2(
        base_policy=_provider(["PASS"])
    )
    assert policy(_observation(watered=True), {})["farmer"] == ["PASS"]
    control = create_codex_e18_770_live_crop_rotation_guard(
        base_policy=_provider(["PASS"])
    )
    assert policy(_observation(day=19), {})["farmer"] == control(
        _observation(day=19), {}
    )["farmer"]


def test_no_move_or_market_mutation_is_introduced() -> None:
    observation = _observation()
    observation["farms"][0]["farmer"] = [2, 5]

    def provider(obs, configuration=None):
        del obs, configuration
        return {
            "farmer": ["PASS"],
            "hands": [],
            "market": [["BUY_SEED", "WHEAT", 5]],
        }

    policy = create_codex_e18_770_water_before_dig_guard_v2(base_policy=provider)
    action = policy(observation, {})
    assert action["farmer"] == ["PASS"]
    assert ["BUY_SEED", "WHEAT", 5] in action["market"]
