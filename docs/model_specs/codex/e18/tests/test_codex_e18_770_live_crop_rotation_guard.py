"""Contract tests for E18.9 exact-7-7-0 live-crop rotation guard."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_770_live_crop_rotation_guard import (
    E18_770_LIVE_CROP_ROTATION_GUARD_MODEL_SPEC_VERSION,
    create_codex_e18_770_live_crop_rotation_guard,
    load_e18_770_live_crop_rotation_guard_config,
)
from agricola.strategy.codex.codex_e18_concentrated_770_throughput import (
    create_codex_e18_concentrated_770_throughput,
)


def _observation(tile: dict | None, *, day: int = 21) -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": [3, 5],
        "hands": [],
        "unlocked_quadrants": ["NW", "NE", "SW"],
    }
    farm["tiles"][5][3] = deepcopy(tile)
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


def test_config_freezes_every_non_rotation_dimension() -> None:
    config = load_e18_770_live_crop_rotation_guard_config()
    assert config["model_spec_version"] == (
        E18_770_LIVE_CROP_ROTATION_GUARD_MODEL_SPEC_VERSION
    )
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["allow_worker_rerouting"] is False
    assert config["provider_trajectory_mutation"] is False
    assert config["market_mutation"] is False
    assert config["worker_count_mutation"] is False
    assert config["livestock_cap_mutation"] is False


def test_live_strawberry_rotation_dig_is_suppressed() -> None:
    observation = _observation(
        {
            "kind": "PLANT",
            "crop": "STRAWBERRY",
            "planted_day": 11,
            "yield_units": 0,
            "watered_today": True,
        }
    )
    policy = create_codex_e18_770_live_crop_rotation_guard(
        base_policy=_provider(["PASS"])
    )
    action = policy(observation, {})
    assert action["farmer"] == ["PASS"]
    telemetry = (
        policy.codex_e18_770_live_crop_rotation_guard_instance.telemetry_snapshot()
    )
    assert telemetry["live_crop_dig_tasks_suppressed"] > 0
    assert telemetry["worker_route_mutations"] == 0


def test_weed_dig_is_preserved() -> None:
    observation = _observation({"kind": "WEED"})
    policy = create_codex_e18_770_live_crop_rotation_guard(
        base_policy=_provider(["PASS"])
    )
    assert policy(observation, {})["farmer"] == ["DIG"]


def test_harvest_and_water_are_preserved() -> None:
    ready = _observation(
        {
            "kind": "PLANT",
            "crop": "STRAWBERRY",
            "planted_day": 11,
            "yield_units": 3,
            "watered_today": False,
        }
    )
    policy = create_codex_e18_770_live_crop_rotation_guard(
        base_policy=_provider(["PASS"])
    )
    assert policy(ready, {})["farmer"] == ["HARVEST"]

    unwatered = _observation(
        {
            "kind": "PLANT",
            "crop": "STRAWBERRY",
            "planted_day": 19,
            "yield_units": 0,
            "watered_today": False,
        },
        day=19,
    )
    policy = create_codex_e18_770_live_crop_rotation_guard(
        base_policy=_provider(["PASS"])
    )
    assert policy(unwatered, {})["farmer"] == ["WATER"]


def test_market_and_provider_trajectory_are_unchanged() -> None:
    observation = _observation(None)

    def provider(obs, configuration=None):
        del obs, configuration
        return {
            "farmer": ["EAST"],
            "hands": [],
            "market": [["BUY_SEED", "WHEAT", 5]],
        }

    policy = create_codex_e18_770_live_crop_rotation_guard(base_policy=provider)
    action = policy(observation, {})
    control = create_codex_e18_concentrated_770_throughput(base_policy=provider)
    control_action = control(observation, {})
    assert action["farmer"] == control_action["farmer"] == ["EAST"]
    assert action["market"] == control_action["market"]
