"""Contract tests for the E18.5 fixed 6-6-2 topology ablation."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_state_driven_662_ablation import (
    E18_STATE_DRIVEN_662_ABLATION_MODEL_SPEC_VERSION,
    create_codex_e18_state_driven_662_ablation,
    load_e18_state_driven_662_ablation_config,
)
from agricola.strategy.codex.codex_e18_state_driven_772_v2 import (
    load_e18_state_driven_v2_config,
)


def _observation(*, day: int) -> dict:
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
        "private": {"shed": {}, "inventories": [{}], "seeds": {}},
        "market": {"prices": {"WHEAT": 25}},
    }


def _configuration() -> dict:
    return {
        "boardSize": 10,
        "turnsPerDay": 24,
        "episodeSteps": 720,
        "shedCapacity": 100,
        "maxMarketOrdersPerTurn": 10,
    }


def test_config_is_exact_662_and_removes_only_two_canonical_targets() -> None:
    config = load_e18_state_driven_662_ablation_config()
    control = load_e18_state_driven_v2_config()
    targets = {tuple(value) for value in config["pasture_targets"]}
    control_targets = {tuple(value) for value in control["pasture_targets"]}
    assert config["model_spec_version"] == (
        E18_STATE_DRIVEN_662_ABLATION_MODEL_SPEC_VERSION
    )
    assert control_targets - targets == {(3, 2), (6, 2)}
    assert len(targets) == 14
    assert config["pasture_livestock_cap"] == 14


def test_every_non_topology_policy_field_matches_772_v2() -> None:
    config = load_e18_state_driven_662_ablation_config()
    control = load_e18_state_driven_v2_config()
    allowed = {
        "candidate_id",
        "schema_version",
        "model_spec_version",
        "base_policy",
        "causal_family",
        "pasture_targets",
        "pasture_livestock_cap",
    }
    assert {
        key: value for key, value in config.items() if key not in allowed
    } == {key: value for key, value in control.items() if key not in allowed}


def test_bootstrap_remains_exact_provider_passthrough() -> None:
    expected = {
        "farmer": ["NORTH"],
        "hands": [],
        "market": [["BUY_SEED", "WHEAT", 1]],
    }

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_state_driven_662_ablation(base_policy=provider)
    assert policy(_observation(day=10), _configuration()) == expected


def test_bootstrap_vetoes_only_removed_target_pasture_build() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["BUILD_PASTURE"], "hands": [], "market": []}

    policy = create_codex_e18_state_driven_662_ablation(base_policy=provider)
    blocked = _observation(day=5)
    blocked["farms"][0]["farmer"] = [3, 2]
    allowed = _observation(day=5)
    allowed["farms"][0]["farmer"] = [4, 2]
    assert policy(blocked, _configuration())["farmer"] == ["PASS"]
    assert policy(allowed, _configuration())["farmer"] == ["BUILD_PASTURE"]
    assert policy.codex_e18_state_driven_662_instance.bootstrap_topology_vetoes == 1


def test_telemetry_declares_topology_only_ablation() -> None:
    policy = create_codex_e18_state_driven_662_ablation()
    instance = policy.codex_e18_state_driven_662_instance
    assert instance.model_spec_version == (
        E18_STATE_DRIVEN_662_ABLATION_MODEL_SPEC_VERSION
    )
    assert instance.config["dispatcher"] == load_e18_state_driven_v2_config()[
        "dispatcher"
    ]
