"""Contract tests for the E18.3 Codex-only topology ablation."""

from __future__ import annotations

from copy import deepcopy

import pytest

from agricola.strategy.codex.codex_e18_labor_conserving_topology_ablation import (
    E18_LABOR_CONSERVING_MODEL_SPEC_VERSION,
    TOPOLOGY_MODES,
    create_codex_e18_labor_conserving_topology,
    load_e18_labor_conserving_config,
)


def _observation() -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": [4, 4],
        "hands": [[4, 4] for _ in range(5)],
        "unlocked_quadrants": ["NW", "NE", "SW"],
    }
    return {
        "step": 144,
        "day": 6,
        "hour": 0,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {
            "shed": {},
            "inventories": [{} for _ in range(6)],
            "seeds": {},
        },
        "market": {"prices": {}},
    }


def test_config_contains_five_nested_fixed_topologies() -> None:
    config = load_e18_labor_conserving_config()
    assert config["model_spec_version"] == E18_LABOR_CONSERVING_MODEL_SPEC_VERSION
    assert tuple(config["topologies"]) == TOPOLOGY_MODES
    dense = {tuple(value) for value in config["dense_pasture_targets"]}
    assert len(dense) == 19
    for mode in TOPOLOGY_MODES:
        targets = {
            tuple(value)
            for value in config["topologies"][mode]["pasture_targets"]
        }
        assert targets <= dense
        assert len(targets) == sum(map(int, mode.split("-")))
    assert config["holdout_consumed"] is False
    assert config["final_confirmation_consumed"] is False


def test_775_is_exact_provider_passthrough() -> None:
    expected = {
        "farmer": ["NORTH"],
        "hands": [["PASS"] for _ in range(5)],
        "market": [["BUY_SEED", "WHEAT", 1]],
    }

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_labor_conserving_topology(
        topology_mode="7-7-5", base_policy=provider
    )
    assert policy(_observation(), None) == expected
    telemetry = policy.codex_e18_labor_conserving_instance.telemetry_snapshot()
    assert telemetry["target_pastures_by_quadrant"] == {"Q0": 7, "Q1": 7, "Q2": 5}
    assert telemetry["override_batches"] == 0


@pytest.mark.parametrize("mode", TOPOLOGY_MODES)
def test_mode_identity_matches_target_counts(mode: str) -> None:
    policy = create_codex_e18_labor_conserving_topology(
        topology_mode=mode,
        base_policy=lambda observation, configuration=None: {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in observation["farms"][0]["hands"]],
            "market": [],
        },
    )
    telemetry = policy.codex_e18_labor_conserving_instance.telemetry_snapshot()
    expected = dict(zip(("Q0", "Q1", "Q2"), map(int, mode.split("-")), strict=True))
    assert telemetry["target_pastures_by_quadrant"] == expected
    assert telemetry["pasture_target_count"] == sum(expected.values())


def test_unknown_topology_fails_closed_at_construction() -> None:
    with pytest.raises(ValueError, match="unknown topology_mode"):
        create_codex_e18_labor_conserving_topology(topology_mode="6-6-3")
