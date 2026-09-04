"""Contract tests for the E18.6 concentrated 7-7-0 candidate."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_concentrated_770_throughput import (
    E18_CONCENTRATED_770_MODEL_SPEC_VERSION,
    create_codex_e18_concentrated_770_throughput,
    load_e18_concentrated_770_config,
)


def _observation(*, position: tuple[int, int] = (3, 5), day: int = 11) -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": list(position),
        "hands": [],
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
            "inventories": [{}],
            "seeds": {"STRAWBERRY": 5, "WHEAT": 5},
        },
        "market": {"prices": {}},
    }


def test_config_is_exact_concentrated_770_partition() -> None:
    config = load_e18_concentrated_770_config()
    assert config["model_spec_version"] == E18_CONCENTRATED_770_MODEL_SPEC_VERSION
    targets = {tuple(value) for value in config["pasture_targets"]}
    reclaimed = {tuple(value) for value in config["reclaimed_q2_crop_targets"]}
    assert len(targets) == 14
    assert len(reclaimed) == 5
    assert all(y < 5 for _x, y in targets)
    assert all(x < 5 and y >= 5 for x, y in reclaimed)
    assert config["global_rerouting_enabled"] is False
    assert config["holdout_consumed"] is False
    assert config["final_confirmation_consumed"] is False
    assert config["kaggle_upload_authorized"] is False


def test_removed_q2_build_is_translated_in_place_to_crop() -> None:
    expected = {"farmer": ["BUILD_PASTURE"], "hands": [], "market": []}

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_concentrated_770_throughput(
        base_policy=provider
    )
    action = policy(_observation(), {"maxMarketOrdersPerTurn": 10})
    assert action["farmer"] == ["PLANT", "STRAWBERRY"]
    telemetry = policy.codex_e18_concentrated_770_instance.telemetry_snapshot()
    assert telemetry["target_pastures_by_quadrant"] == {
        "Q0": 7,
        "Q1": 7,
        "Q2": 0,
    }
    assert telemetry["global_rerouting_enabled"] is False


def test_provider_movement_is_not_globally_replanned() -> None:
    expected = {"farmer": ["NORTH"], "hands": [], "market": []}

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_concentrated_770_throughput(
        base_policy=provider
    )
    action = policy(_observation(), {"maxMarketOrdersPerTurn": 10})
    assert action["farmer"] == ["NORTH"]


def test_non_q2_provider_action_remains_authoritative() -> None:
    expected = {"farmer": ["WATER"], "hands": [], "market": []}

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_concentrated_770_throughput(
        base_policy=provider
    )
    action = policy(
        _observation(position=(1, 1)), {"maxMarketOrdersPerTurn": 10}
    )
    assert action["farmer"] == ["WATER"]
