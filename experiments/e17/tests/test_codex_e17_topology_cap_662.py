"""Tests for the productive E17.3 6-6-2 topology controller."""

from __future__ import annotations

import json
from copy import deepcopy

from kaggle_environments import make

from agricola.core.benchmark_opponents import inert_pass_policy
from agricola.strategy.codex.codex_e17_topology_cap_662 import (
    TOPOLOGY_662_MODEL_SPEC_VERSION,
    create_codex_e17_topology_cap_662,
    load_topology_662_config,
)


def _observation(
    *,
    position=(3, 2),
    livestock=0,
    inventory=None,
    shed=None,
    seeds=None,
    tiles_at=None,
    day=0,
):
    tiles = [[None for _ in range(10)] for _ in range(10)]
    for index in range(livestock):
        x = index % 5
        y = index // 5
        tiles[y][x] = {"kind": "PASTURE", "animal": "COW"}
    for (x, y), tile in (tiles_at or {}).items():
        tiles[y][x] = deepcopy(tile)
    return {
        "step": day * 24 + 1,
        "day": day,
        "hour": 1,
        "player": 0,
        "farms": [
            {
                "money": 3000,
                "tiles": tiles,
                "farmer": list(position),
                "hands": [],
                "unlocked_quadrants": ["NW", "NE", "SW"],
            }
        ],
        "private": {
            "shed": deepcopy(shed or {"COW": 0, "SHEEP": 0}),
            "inventories": [deepcopy(inventory or {})],
            "seeds": deepcopy(seeds or {}),
        },
        "market": {"prices": {}},
    }


def test_config_is_exact_662_and_q2_is_a_ceiling() -> None:
    config = load_topology_662_config()
    targets = [tuple(value) for value in config["pasture_targets"]]
    assert config["model_spec_version"] == TOPOLOGY_662_MODEL_SPEC_VERSION
    assert len(targets) == 14
    assert sum(x < 5 and y < 5 for x, y in targets) == 6
    assert sum(x >= 5 and y < 5 for x, y in targets) == 6
    assert sum(x < 5 and y >= 5 for x, y in targets) == 2
    assert config["q2_pasture_cap"] == 2
    assert config["allow_q2_zero_future_variant"] is True
    reclaimed = [tuple(value) for value in config["reclaimed_crop_targets"]]
    assert len(reclaimed) == 5
    assert sum(x < 5 and y >= 5 for x, y in reclaimed) == 3
    assert set(reclaimed) == {
        tuple(value) for value in config["blocked_v4d_pasture_targets"]
    }


def test_same_controller_accepts_a_zero_q2_target_variant(tmp_path) -> None:
    config = load_topology_662_config()
    config["pasture_targets"] = [
        value for value in config["pasture_targets"] if value[1] < 5
    ]
    config["pasture_fill_target"] = 12
    config["pre_q2_livestock_resource_cap"] = 12
    config["livestock_resource_cap"] = 13
    path = tmp_path / "topology_660.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    loaded = load_topology_662_config(path)
    assert len(loaded["pasture_targets"]) == 12
    assert all(value[1] < 5 for value in loaded["pasture_targets"])


def test_blocked_v4d_pasture_build_is_reassigned_to_crop() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["BUILD_PASTURE"], "hands": [], "market": []}

    policy = create_codex_e17_topology_cap_662(base_policy=provider)
    policy.codex_e17_topology_662_instance.reclaimed_seed_backfill_requested = True
    action = policy(
        _observation(position=(3, 6), seeds={"STRAWBERRY": 5}, day=11),
        None,
    )
    assert action["farmer"] == ["PLANT", "STRAWBERRY"]
    assert not policy.codex_e17_topology_662_last_error
    telemetry = policy.codex_e17_topology_662_instance.telemetry_snapshot()
    assert telemetry["reassigned_blocked_worker_actions"] == 1


def test_allowed_pasture_build_is_preserved() -> None:
    expected = {"farmer": ["BUILD_PASTURE"], "hands": [], "market": []}

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e17_topology_cap_662(base_policy=provider)
    assert policy(_observation(position=(4, 2)), None) == expected


def test_livestock_orders_keep_one_transition_resource_above_fill_target() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {
            "farmer": ["PASS"],
            "hands": [],
            "market": [
                ["BUY_ANIMAL", "SHEEP", 4],
                ["BUY_ANIMAL", "GOOSE", 1],
            ],
        }

    policy = create_codex_e17_topology_cap_662(base_policy=provider)
    action = policy(_observation(livestock=12), None)
    assert action["market"] == [
        ["BUY_ANIMAL", "SHEEP", 3],
        ["BUY_ANIMAL", "GOOSE", 1],
    ]
    telemetry = policy.codex_e17_topology_662_instance.telemetry_snapshot()
    assert telemetry["clamped_animal_units"] == {"SHEEP": 1}


def test_q2_animal_placement_outside_cap_is_blocked() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["PLACE", "SHEEP"], "hands": [], "market": []}

    policy = create_codex_e17_topology_cap_662(base_policy=provider)
    action = policy(_observation(position=(4, 6)), None)
    assert action["farmer"] == ["PASS"]


def test_fill_mission_places_carrier_on_empty_allowed_q1_pasture() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["PASS"], "hands": [], "market": []}

    policy = create_codex_e17_topology_cap_662(base_policy=provider)
    policy.codex_e17_topology_662_instance.reclaimed_seed_backfill_requested = True
    policy.codex_e17_topology_662_instance.fill_mission_workers.add(0)
    policy.codex_e17_topology_662_instance.fill_mission_started = True
    observation = _observation(
        position=(6, 3),
        inventory={"SHEEP": 1},
        tiles_at={(6, 3): {"kind": "PASTURE"}},
        day=12,
    )
    assert policy(observation, None)["farmer"] == ["PLACE", "SHEEP", 1]


def test_empty_built_pasture_backfills_missing_livestock_resource() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["PASS"], "hands": [], "market": []}

    policy = create_codex_e17_topology_cap_662(base_policy=provider)
    policy.codex_e17_topology_662_instance.reclaimed_seed_backfill_requested = True
    observation = _observation(
        position=(4, 4),
        tiles_at={(6, 3): {"kind": "PASTURE"}},
        day=12,
    )
    assert policy(observation, None)["market"] == [
        ["BUY_ANIMAL", "SHEEP", 1]
    ]


def test_reclaimed_crop_is_watered_and_harvested_from_state() -> None:
    def provider(observation, configuration=None):
        del observation, configuration
        return {"farmer": ["PASS"], "hands": [], "market": []}

    policy = create_codex_e17_topology_cap_662(base_policy=provider)
    policy.codex_e17_topology_662_instance.reclaimed_seed_backfill_requested = True
    growing = {
        "kind": "PLANT",
        "crop": "MELON",
        "planted_day": 10,
        "yield_units": 0,
        "watered_today": False,
    }
    assert policy(
        _observation(position=(3, 6), tiles_at={(3, 6): growing}, day=11),
        None,
    )["farmer"] == ["WATER"]

    mature = {**growing, "yield_units": 6}
    assert policy(
        _observation(position=(3, 6), tiles_at={(3, 6): mature}, day=20),
        None,
    )["farmer"] == ["HARVEST"]


def test_full_episode_fills_662_and_activates_all_reclaimed_crops() -> None:
    policy = create_codex_e17_topology_cap_662(
        run_context={"seed": 26090101, "player_position": 0}
    )
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": 26090101,
            "turnsPerDay": 24,
        },
        debug=False,
    )
    env.run([policy, inert_pass_policy])
    instance = policy.codex_e17_topology_662_instance
    telemetry = instance.telemetry_snapshot()
    assert instance.error_count == 0
    assert instance.fallback_count == 0
    assert telemetry["latest_target_pastures_built"] == 14
    assert telemetry["latest_target_pastures_filled"] == 14
    assert telemetry["latest_empty_target_pastures"] == 0
    assert telemetry["max_active_reclaimed_crops"] == 5
    assert telemetry["max_observed_q2_pastures"] == 2
    assert telemetry["topology_cap_breaches"] == 0
