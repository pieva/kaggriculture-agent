"""Tests for the E18 public-opponent-reactive 6-6-2 / 7-7-0 overlay."""

from __future__ import annotations

from copy import deepcopy

from agricola.strategy.codex.codex_e18_opponent_reactive_topology import (
    E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION,
    create_codex_e18_opponent_reactive_topology,
    load_e18_opponent_reactive_config,
)


def _farm(
    *,
    position=(4, 4),
    quadrants=3,
    crops=0,
    pastures=0,
    weeds=0,
    animals=0,
    hands=0,
):
    tiles = [[None for _ in range(10)] for _ in range(10)]
    cursor = 0
    for kind, count in (
        ("PLANT", crops),
        ("PASTURE", pastures),
        ("WEED", weeds),
    ):
        for _ in range(count):
            x, y = cursor % 10, cursor // 10
            tile = {"kind": kind}
            if kind == "PLANT":
                tile.update(
                    {
                        "crop": "WHEAT",
                        "planted_day": 0,
                        "yield_units": 0,
                        "watered_today": True,
                    }
                )
            tiles[y][x] = tile
            cursor += 1
    for _ in range(animals):
        x, y = cursor % 10, cursor // 10
        tiles[y][x] = {"kind": "PASTURE", "animal": "SHEEP"}
        cursor += 1
    return {
        "money": 3000,
        "tiles": tiles,
        "farmer": list(position),
        "hands": [[4, 4] for _ in range(hands)],
        "unlocked_quadrants": ["NW", "NE", "SW"][:quadrants],
    }


def _observation(*, opponent, day=6, position=(4, 4), inventory=None):
    return {
        "step": day * 24 + 1,
        "day": day,
        "hour": 1,
        "player": 0,
        "farms": [_farm(position=position), deepcopy(opponent)],
        "private": {
            "shed": {},
            "inventories": [deepcopy(inventory or {})],
            "seeds": {},
        },
        "market": {"prices": {}},
    }


def _pass_provider(observation, configuration=None):
    del configuration
    hands = observation["farms"][0].get("hands", [])
    return {
        "farmer": ["PASS"],
        "hands": [["PASS"] for _ in hands],
        "market": [],
    }


def test_config_defines_two_fourteen_pasture_topologies() -> None:
    config = load_e18_opponent_reactive_config()
    assert config["model_spec_version"] == E18_OPPONENT_REACTIVE_MODEL_SPEC_VERSION
    assert set(config["topologies"]) == {"6-6-2", "7-7-0"}
    for mode, payload in config["topologies"].items():
        assert len(payload["pasture_targets"]) == 14, mode
        assert len(payload["reclaimed_crop_targets"]) == 5, mode


def test_conservative_public_opponent_freezes_662() -> None:
    policy = create_codex_e18_opponent_reactive_topology(
        base_policy=_pass_provider
    )
    policy(_observation(opponent=_farm(quadrants=1, pastures=2)), None)
    telemetry = policy.codex_e18_opponent_reactive_instance.telemetry_snapshot()
    assert telemetry["topology_mode"] == "6-6-2"
    assert telemetry["target_pastures_by_quadrant"] == {
        "Q0": 6,
        "Q1": 6,
        "Q2": 2,
    }
    assert telemetry["mode_decisions"] == 1
    assert telemetry["mode_decision_features"]["quadrants"] == 1
    assert telemetry["public_features_only"] is True


def test_expanding_crop_opponent_freezes_770_and_is_sticky() -> None:
    policy = create_codex_e18_opponent_reactive_topology(
        base_policy=_pass_provider
    )
    policy(_observation(opponent=_farm(quadrants=3, crops=33)), None)
    policy(
        _observation(
            opponent=_farm(quadrants=1),
            day=7,
        ),
        None,
    )
    telemetry = policy.codex_e18_opponent_reactive_instance.telemetry_snapshot()
    assert telemetry["topology_mode"] == "7-7-0"
    assert telemetry["target_pastures_by_quadrant"] == {
        "Q0": 7,
        "Q1": 7,
        "Q2": 0,
    }
    assert telemetry["mode_decisions"] == 1
    assert telemetry["unique_regimes"] == 2
    assert len(telemetry["regime_transitions"]) == 2


def test_selected_dynamic_cell_is_built_and_alternative_is_blocked() -> None:
    high = create_codex_e18_opponent_reactive_topology(
        base_policy=_pass_provider
    )
    high_action = high(
        _observation(
            opponent=_farm(quadrants=3, crops=33),
            position=(3, 2),
        ),
        None,
    )
    assert high_action["farmer"] == ["BUILD_PASTURE"]

    low = create_codex_e18_opponent_reactive_topology(
        base_policy=_pass_provider
    )
    low_action = low(
        _observation(
            opponent=_farm(quadrants=1, pastures=2),
            position=(3, 5),
        ),
        None,
    )
    assert low_action["farmer"] == ["BUILD_PASTURE"]


def test_no_topology_decision_before_preregistered_checkpoint() -> None:
    policy = create_codex_e18_opponent_reactive_topology(
        base_policy=_pass_provider
    )
    policy(
        _observation(
            opponent=_farm(quadrants=3, crops=33),
            day=5,
        ),
        None,
    )
    telemetry = policy.codex_e18_opponent_reactive_instance.telemetry_snapshot()
    assert telemetry["topology_mode"] is None
    assert telemetry["mode_decisions"] == 0
    assert telemetry["target_pastures_by_quadrant"] == {
        "Q0": 6,
        "Q1": 6,
        "Q2": 0,
    }


def test_service_risk_pasture_is_delayed_until_high_pressure_release() -> None:
    def place_provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["PLACE", "COW", 1], "hands": [], "market": []}

    policy = create_codex_e18_opponent_reactive_topology(
        base_policy=place_provider
    )
    observation = _observation(
        opponent=_farm(quadrants=3, crops=33),
        day=18,
        position=(2, 4),
    )
    observation["farms"][0]["tiles"][4][2] = {
        "kind": "PASTURE",
    }
    assert policy(observation, None)["farmer"] != ["PLACE", "COW", 1]
    observation["day"] = 28
    observation["step"] = 28 * 24 + 1
    assert policy(observation, None)["farmer"] == ["PLACE", "COW", 1]
    telemetry = policy.codex_e18_opponent_reactive_instance.telemetry_snapshot()
    assert telemetry["delayed_livestock_placements"] == 1
    assert telemetry["livestock_resource_cap"] == 14
