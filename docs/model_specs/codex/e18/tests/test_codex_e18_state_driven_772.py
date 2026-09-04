"""Contract tests for the E18.4 state-driven 7-7-2 candidate."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_state_driven_772 import (
    E18_STATE_DRIVEN_MODEL_SPEC_VERSION,
    create_codex_e18_state_driven_772,
    load_e18_state_driven_config,
)


def _observation(*, day: int, shed: dict | None = None) -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": [4, 4],
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
            "shed": shed or {},
            "inventories": [{}],
            "seeds": {},
        },
        "market": {"prices": {"MILK": 160, "WHEAT": 25}},
    }


def _configuration() -> dict:
    return {
        "boardSize": 10,
        "turnsPerDay": 24,
        "episodeSteps": 720,
        "shedCapacity": 100,
        "maxMarketOrdersPerTurn": 10,
    }


def test_config_is_exact_772_and_causally_bounded() -> None:
    config = load_e18_state_driven_config()
    assert config["model_spec_version"] == E18_STATE_DRIVEN_MODEL_SPEC_VERSION
    assert len(config["pasture_targets"]) == 16
    assert config["activation_day"] == 11
    assert config["holdout_consumed"] is False
    assert config["final_confirmation_consumed"] is False


def test_bootstrap_is_exact_provider_passthrough() -> None:
    expected = {
        "farmer": ["NORTH"],
        "hands": [],
        "market": [["BUY_SEED", "WHEAT", 1]],
    }

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_state_driven_772(base_policy=provider)
    assert policy(_observation(day=10), _configuration()) == expected


def test_active_market_sells_observed_shed_before_provider_buys() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {
            "farmer": ["PASS"],
            "hands": [],
            "market": [["BUY_SEED", "WHEAT", 1]],
        }

    policy = create_codex_e18_state_driven_772(base_policy=provider)
    action = policy(
        _observation(day=11, shed={"MILK": 3, "WHEAT": 4}),
        _configuration(),
    )
    assert action["market"][0] == ["SELL", "MILK", 3]
    assert ["BUY_SEED", "WHEAT", 1] in action["market"]
    assert not any(order[:2] == ["SELL", "WHEAT"] for order in action["market"])


def test_active_scheduler_replaces_provider_unit_command() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["WEST"], "hands": [], "market": []}

    observation = _observation(day=11)
    observation["farms"][0]["tiles"][4][4] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 10,
        "watered_today": False,
        "consecutive_unwatered": 1,
        "yield_units": 0,
    }
    policy = create_codex_e18_state_driven_772(base_policy=provider)
    action = policy(observation, _configuration())
    assert action["farmer"] == ["WATER"]

