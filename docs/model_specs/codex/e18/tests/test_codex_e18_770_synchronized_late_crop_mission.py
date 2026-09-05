"""Contract tests for the E18.17 synchronized late crop controller."""

from agricola.strategy.codex.codex_e18_770_synchronized_late_crop_mission import (
    E18_770_SYNCHRONIZED_LATE_CROP_MISSION_MODEL_SPEC_VERSION,
    CodexE18770SynchronizedLateCropMissionAgent,
    load_e18_770_synchronized_late_crop_mission_config,
)


def _observation(*, day=20, step=480, positions=None, tiles=None, inventories=None):
    positions = positions or [(0, 0), (1, 1)]
    board = [[None for _ in range(10)] for _ in range(10)]
    for position, tile in (tiles or {}).items():
        board[position[1]][position[0]] = tile
    return {
        "day": day,
        "hour": step % 24,
        "step": step,
        "player": 0,
        "farms": [
            {
                "farmer": list(positions[0]),
                "hands": [list(value) for value in positions[1:]],
                "tiles": board,
                "unlocked_quadrants": [0, 1, 2, 3],
                "money": 10000,
            },
            {},
        ],
        "private": {
            "inventories": inventories or [{} for _ in positions],
            "seeds": {"WHEAT": 20},
            "shed": {},
        },
    }


def _agent() -> CodexE18770SynchronizedLateCropMissionAgent:
    return CodexE18770SynchronizedLateCropMissionAgent()


def test_config_freezes_770_cap_and_livestock_policy() -> None:
    config = load_e18_770_synchronized_late_crop_mission_config()
    assert config["model_spec_version"] == (
        E18_770_SYNCHRONIZED_LATE_CROP_MISSION_MODEL_SPEC_VERSION
    )
    assert config["pasture_topology"] == {"Q0": 7, "Q1": 7, "Q2": 0}
    assert config["livestock_resource_cap"] == 14
    assert config["preserve_livestock_policy"] is True
    assert config["max_persistent_harvest_missions"] == 1
    assert config["mission_workers"] == "ANY_UNIT_ON_TARGET_PROVIDER_PASS"
    assert config["mission_provider_override_opcodes"] == ["PASS"]


def test_local_priority_harvests_ready_crop_before_stale_water() -> None:
    agent = _agent()
    observation = _observation(
        positions=[(0, 0), (2, 2)],
        tiles={
            (2, 2): {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 18,
                "watered_today": False,
                "consecutive_unwatered": 1,
                "yield_units": 6,
            }
        },
    )
    action = {"farmer": ["PASS"], "hands": [["PASS"]], "market": []}
    agent._apply_local_priorities(action, observation)
    assert action["hands"] == [["HARVEST"]]
    assert agent.local_harvest_overrides == 1


def test_plant_admission_blocks_only_extreme_pressure_in_v1() -> None:
    agent = _agent()
    observation = _observation(day=26)
    action = {
        "farmer": ["PLANT", "WHEAT"],
        "hands": [["PASS"]],
        "market": [],
    }
    agent._apply_plant_admission(
        action,
        observation,
        {"harvest_ready": 999, "water_at_risk": 999, "weeds": 0},
    )
    assert action["farmer"] == ["PASS"]
    assert agent.plant_commands_blocked == 1
    assert agent.plant_blocks_by_reason["NO_PAYBACK_WINDOW"] == 0
    assert agent.plant_blocks_by_reason["HARVEST_BACKLOG"] == 1


def test_persistent_mission_reserves_nearby_ready_crop_for_empty_hand() -> None:
    agent = _agent()
    observation = _observation(
        positions=[(0, 0), (1, 1)],
        tiles={
            (1, 1): {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 18,
                "watered_today": True,
                "consecutive_unwatered": 0,
                "yield_units": 6,
            }
        },
    )
    action = {"farmer": ["PASS"], "hands": [["PASS"]], "market": []}
    agent._start_harvest_mission(action, observation)
    agent._advance_harvest_mission(action, observation)
    assert agent.active_harvest_mission == {
        "worker": 1,
        "target": [1, 1],
        "crop": "WHEAT",
        "created_step": 480,
    }
    assert action["hands"] == [["HARVEST"]]
    assert agent.harvest_missions_started == 1
    assert agent.harvest_mission_route_commands == 0
    assert agent.harvest_mission_service_commands == 1


def test_existing_provider_harvest_is_adopted_for_ack_without_override() -> None:
    agent = _agent()
    observation = _observation(
        positions=[(2, 2), (1, 1)],
        tiles={
            (2, 2): {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 18,
                "watered_today": True,
                "yield_units": 6,
            }
        },
    )
    action = {"farmer": ["HARVEST"], "hands": [["PASS"]], "market": []}
    agent._start_harvest_mission(action, observation)
    assert action["farmer"] == ["HARVEST"]
    assert agent.provider_harvest_missions_adopted == 1
    assert agent.pending_harvest_ack == {
        "step": 480,
        "target": [2, 2],
        "before_yield": 6,
    }


def test_mission_does_not_override_non_pass_logistics() -> None:
    agent = _agent()
    observation = _observation(
        positions=[(0, 0), (3, 3)],
        tiles={
            (4, 4): {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 18,
                "watered_today": True,
                "yield_units": 6,
            }
        },
        inventories=[{}, {}],
    )
    action = {"farmer": ["PASS"], "hands": [["DROP", "WHEAT", 1]], "market": []}
    agent._start_harvest_mission(action, observation)
    assert agent.active_harvest_mission is None
    assert action["hands"] == [["DROP", "WHEAT", 1]]


def test_local_priority_never_overrides_shared_shed_access() -> None:
    agent = _agent()
    observation = _observation(
        positions=[(0, 0), (4, 4)],
        tiles={
            (4, 4): {
                "kind": "PLANT",
                "crop": "WHEAT",
                "planted_day": 18,
                "watered_today": False,
                "consecutive_unwatered": 1,
                "yield_units": 0,
            }
        },
    )
    action = {"farmer": ["PASS"], "hands": [["PASS"]], "market": []}
    agent._apply_local_priorities(action, observation)
    assert action["hands"] == [["PASS"]]
    assert agent.local_water_overrides == 0
