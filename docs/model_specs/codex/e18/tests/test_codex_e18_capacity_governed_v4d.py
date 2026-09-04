"""Contract tests for the E18.2 capacity-governed V4D candidate."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_capacity_governed_v4d import (
    E18_CAPACITY_GOVERNED_MODEL_SPEC_VERSION,
    create_codex_e18_capacity_governed_v4d,
    load_e18_capacity_governed_config,
)


def _farm(*, hands=5, crops=0, pastures=0, weeds=0, position=(4, 7)):
    tiles = [[None for _ in range(10)] for _ in range(10)]
    cursor = 0
    for kind, count in (("PLANT", crops), ("PASTURE", pastures), ("WEED", weeds)):
        for _ in range(count):
            x, y = cursor % 10, cursor // 10
            tile = {"kind": kind}
            if kind == "PLANT":
                tile.update(
                    crop="WHEAT",
                    planted_day=0,
                    yield_units=0,
                    watered_today=True,
                    consecutive_unwatered=0,
                )
            tiles[y][x] = tile
            cursor += 1
    return {
        "money": 10000,
        "tiles": tiles,
        "farmer": list(position),
        "hands": [[4, 4] for _ in range(hands)],
        "unlocked_quadrants": ["NW", "NE", "SW"],
    }


def _observation(*, day=6, own=None, opponent=None, seeds=None):
    return {
        "step": day * 24,
        "day": day,
        "hour": 0,
        "player": 0,
        "farms": [own or _farm(), opponent or _farm(crops=20, pastures=10)],
        "private": {
            "shed": {},
            "inventories": [{} for _ in range(6)],
            "seeds": seeds or {},
        },
        "market": {"prices": {}},
    }


def _pass_provider(observation, configuration=None):
    del configuration
    return {
        "farmer": ["PASS"],
        "hands": [["PASS"] for _ in observation["farms"][0]["hands"]],
        "market": [],
    }


def test_config_keeps_v4d_and_only_one_reclaim_cell() -> None:
    config = load_e18_capacity_governed_config()
    assert config["model_spec_version"] == E18_CAPACITY_GOVERNED_MODEL_SPEC_VERSION
    assert len(config["dense_pasture_targets"]) == 19
    assert config["reclaim_targets_in_order"] == [[4, 7]]
    assert config["topology_reclaim_enabled"] is False
    assert config["holdout_consumed"] is False
    assert config["final_confirmation_consumed"] is False


def test_disabled_governor_is_exact_provider_parity() -> None:
    expected = {"farmer": ["NORTH"], "hands": [["PASS"]] * 5, "market": []}

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_capacity_governed_v4d(base_policy=provider)
    policy.codex_e18_capacity_governed_instance.governor_enabled = False
    assert policy(_observation(), None) == expected
    telemetry = policy.codex_e18_capacity_governed_instance.telemetry_snapshot()
    assert telemetry["mode"] == "DENSE_V4D"
    assert telemetry["override_batches"] == 0


def test_public_pressure_cannot_override_insufficient_own_capacity() -> None:
    policy = create_codex_e18_capacity_governed_v4d(base_policy=_pass_provider)
    own = _farm(hands=1, weeds=2)
    policy(_observation(own=own, opponent=_farm(crops=40, pastures=19)), None)
    telemetry = policy.codex_e18_capacity_governed_instance.telemetry_snapshot()
    assert telemetry["mode"] == "RECOVERY"
    assert telemetry["committed_reclaims"] == []


def test_healthy_capacity_reclaims_one_q2_cell_and_uses_released_work() -> None:
    def build_provider(observation, configuration=None):
        del configuration
        return {
            "farmer": ["BUILD_PASTURE"],
            "hands": [["PASS"] for _ in observation["farms"][0]["hands"]],
            "market": [],
        }

    policy = create_codex_e18_capacity_governed_v4d(base_policy=build_provider)
    policy.codex_e18_capacity_governed_instance.e18_config[
        "topology_reclaim_enabled"
    ] = True
    action = policy(_observation(seeds={"WHEAT": 1}), None)
    telemetry = policy.codex_e18_capacity_governed_instance.telemetry_snapshot()
    assert action["farmer"] == ["PLANT", "WHEAT"]
    assert telemetry["mode"] == "RECLAIM_CROP"
    assert telemetry["committed_reclaims"] == [[4, 7]]
    assert telemetry["target_pastures_by_quadrant"] == {"Q0": 7, "Q1": 7, "Q2": 4}
    assert telemetry["no_freed_work_violations"] == 0


def test_unfunded_reclaim_reverts_to_provider_instead_of_pass() -> None:
    def build_provider(observation, configuration=None):
        del configuration
        return {
            "farmer": ["BUILD_PASTURE"],
            "hands": [["NORTH"] for _ in observation["farms"][0]["hands"]],
            "market": [],
        }

    policy = create_codex_e18_capacity_governed_v4d(base_policy=build_provider)
    policy.codex_e18_capacity_governed_instance.e18_config[
        "topology_reclaim_enabled"
    ] = True
    action = policy(_observation(seeds={}), None)
    telemetry = policy.codex_e18_capacity_governed_instance.telemetry_snapshot()
    assert action["farmer"] == ["BUILD_PASTURE"]
    assert telemetry["mode"] == "DENSE_V4D"
    assert telemetry["aborted_reclaim_batches"] == 1
    assert telemetry["no_freed_work_violations"] == 1


def test_terminal_days_are_exact_v4d_passthrough() -> None:
    expected = {"farmer": ["DROP", "WHEAT", 2], "hands": [["PASS"]] * 5, "market": []}

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_capacity_governed_v4d(base_policy=provider)
    assert policy(_observation(day=28), None) == expected
    telemetry = policy.codex_e18_capacity_governed_instance.telemetry_snapshot()
    assert telemetry["terminal_passthrough_batches"] == 1


def test_public_opponent_modulates_mild_recovery_action() -> None:
    own = _farm(hands=5, weeds=1, position=(0, 0))
    own["tiles"][0][0]["consecutive_unwatered"] = 0
    high = create_codex_e18_capacity_governed_v4d(base_policy=_pass_provider)
    low = create_codex_e18_capacity_governed_v4d(base_policy=_pass_provider)
    high_action = high(
        _observation(own=deepcopy(own), opponent=_farm(crops=20, pastures=10)),
        None,
    )
    low_action = low(
        _observation(own=deepcopy(own), opponent=_farm(hands=0)),
        None,
    )
    assert high_action["farmer"] == ["DIG"]
    assert low_action["farmer"] == ["PASS"]
    high_telemetry = high.codex_e18_capacity_governed_instance.telemetry_snapshot()
    assert high_telemetry["opponent_conditioned_recovery_batches"] == 1
