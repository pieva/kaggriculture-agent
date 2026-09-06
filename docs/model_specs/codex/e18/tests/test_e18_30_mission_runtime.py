"""Engine-backed acknowledgement and clock/identity/admission contracts."""

import importlib
from copy import deepcopy

import pytest

from docs.model_specs.codex.e18.tools.e18_30_mission_runtime import (
    MissionRuntimeController,
    route,
)

ENGINE = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")


def planned(op, day=11, turn=3, worker=9, position=(4, 3)):
    return {
        "day": day,
        "turn": turn,
        "worker": worker,
        "step": (day - 1) * 24 + turn,
        "position": list(position),
        "opcode": op,
        "arguments": {},
    }


def fixture(variant="RESCUE", rows=None, day=11, turn=3):
    agent = MissionRuntimeController(
        {
            "trajectory": rows or [],
            "daily": [],
            "treatment_config": {"progressive_cows": True},
        },
        variant=variant,
    )
    farm = {"farmer": [4, 4], "hands": [], "tiles": [[None] * 10 for _ in range(10)]}
    farm["tiles"][3][4] = ENGINE._new_plant("WHEAT", day - 2, 24)
    private = {"shed": {}, "inventories": [{}], "seeds": {}}
    obs = {
        "farms": [farm, deepcopy(farm)],
        "private": private,
        "day": day - 1,
        "hour": turn - 1,
    }
    return agent, obs


def step(agent, obs):
    agent._prepare(obs, {})
    selected = deepcopy(agent.selected)
    for worker, (command, _) in enumerate(selected):
        ENGINE._apply_unit_action(
            obs["farms"][0], obs["private"], worker, command, 10, obs["day"], 24
        )
    obs["hour"] += 1
    return selected


def test_actual_orphan_water_moves_services_then_acknowledges():
    agent, obs = fixture(rows=[planned("WATER")])
    original_plan = deepcopy(agent.plan)
    assert step(agent, obs)[0][0] == ["NORTH"]
    assert len(agent.active) == 1 and agent.runtime_daily[11]["ack_WATER"] == 0
    assert step(agent, obs)[0][0] == ["WATER"]
    assert agent.runtime_daily[11]["ack_WATER"] == 0  # emitted, not yet observed
    step(agent, obs)
    assert not agent.active and agent.runtime_daily[11]["ack_WATER"] == 1
    assert agent.plan == original_plan


def test_partial_hiring_never_produces_commands_for_unobserved_workers():
    agent, obs = fixture(rows=[planned("WATER")])
    agent._prepare(obs, {})
    assert len(agent.selected) == 1  # farmer, zero actual hands
    assert all(j["worker"] == 0 for j in agent.active.values())


def test_no_borrowing_an_immediately_blocked_baseline_worker():
    rows = [planned("WATER"), planned("PICKUP", worker=0, position=(4, 4))]
    rows[-1]["arguments"] = {"item": "WHEAT", "units": 1}
    agent, obs = fixture(rows=rows)
    step(agent, obs)
    assert not agent.active


def test_no_early_transfer_of_future_water():
    agent, obs = fixture(rows=[planned("WATER", turn=18)])
    step(agent, obs)
    assert not agent.active


def test_complete_mission_must_fit_before_next_baseline_action():
    rows = [planned("WATER"), planned("NORTH", turn=5, worker=0, position=(4, 3))]
    agent, obs = fixture(rows=rows)
    # North + WATER + return = three batches; H3-H4 gap only has two.
    step(agent, obs)
    assert not agent.active


def test_temporary_gap_returns_to_origin_without_delaying_baseline():
    rows = [planned("WATER"), planned("NORTH", turn=7, worker=0, position=(4, 3))]
    agent, obs = fixture(rows=rows)
    assert step(agent, obs)[0][0] == ["NORTH"]
    assert step(agent, obs)[0][0] == ["WATER"]
    assert step(agent, obs)[0][0] == ["SOUTH"]
    step(agent, obs)
    assert not agent.active and obs["farms"][0]["farmer"] == [4, 4]
    assert step(agent, obs)[0][0] == ["NORTH"]


def test_failed_emission_not_acknowledged_or_lost():
    agent, obs = fixture(rows=[planned("WATER")])
    step(agent, obs)
    agent._prepare(obs, {})  # WATER deliberately not applied to engine
    obs["hour"] += 1
    agent._prepare(obs, {})
    assert agent.runtime_daily[11]["ack_WATER"] == 0
    assert agent.selected[0][0] == ["WATER"]


def test_pool_fertilizer_closes_collect_drop_with_verified_inventory():
    agent, obs = fixture("POOL", day=30, turn=20)
    obs["farms"][0]["tiles"][3][4] = ENGINE._new_animal("COW", 0)
    obs["farms"][0]["tiles"][3][4]["fertilizer_available"] = True
    assert step(agent, obs)[0][0] == ["NORTH"]
    assert step(agent, obs)[0][0] == ["COLLECT_FERTILIZER"]
    assert step(agent, obs)[0][0] == ["SOUTH"]
    assert step(agent, obs)[0][0] == ["DROP"]
    agent.acknowledge_terminal(obs)
    assert not agent.active
    assert obs["private"]["shed"] == {"FERTILIZER": 1}
    assert agent.runtime_daily[30]["drop_ack_units"] == 1


def test_d30_terminal_observation_not_executable_capacity():
    agent, obs = fixture("POOL", day=30, turn=21)
    obs["farms"][0]["tiles"][3][4] = ENGINE._new_animal("COW", 0)
    obs["farms"][0]["tiles"][3][4]["fertilizer_available"] = True
    step(agent, obs)
    assert not agent.active


def test_day_identity_reset_and_unfinished_not_silently_erased():
    agent, obs = fixture(rows=[planned("WATER")])
    step(agent, obs)
    assert agent.worker_id(11, 1) != agent.worker_id(12, 1)
    agent._new_day(12)
    assert agent.incomplete_missions == 1
    assert agent.runtime_daily[11]["unfinished_at_day_refresh"] == 1


def test_route_matches_engine_even_across_locked_tiles():
    _agent, obs = fixture()
    farm = obs["farms"][0]
    farm["tiles"] = [["LOCKED"] * 10 for _ in range(10)]
    for command in route((4, 4), (9, 9)):
        ENGINE._apply_unit_action(farm, obs["private"], 0, command, 10, 0, 24)
    assert farm["farmer"] == [9, 9]
    with pytest.raises(ValueError):
        route((4, 4), (10, 9))


def crop_fixture(turn=3, seeds=1, weed=False):
    rows = [planned("PLANT", turn=23), planned("WATER", turn=24)]
    rows[0]["arguments"] = {"crop": "STRAWBERRY"}
    agent, obs = fixture("CROP_POOL", rows, turn=turn)
    obs["farms"][0]["tiles"][3][4] = {"kind": "WEED"} if weed else None
    obs["private"]["seeds"] = {"STRAWBERRY": seeds}
    return agent, obs


def test_compound_plant_water_acknowledges_both_services():
    agent, obs = crop_fixture()
    assert step(agent, obs)[0][0] == ["NORTH"]
    assert step(agent, obs)[0][0] == ["PLANT", "STRAWBERRY"]
    assert not agent.plant_confirmed
    assert agent._pending_requirements(11, "seed")["STRAWBERRY"] == 1
    assert step(agent, obs)[0][0] == ["WATER"]
    assert (11, (4, 3)) in agent.plant_confirmed
    assert agent._pending_requirements(11, "seed")["STRAWBERRY"] == 0
    assert agent.runtime_daily[11]["ack_PLANT_WATER"] == 0
    step(agent, obs)
    assert not agent.active
    assert agent.runtime_daily[11]["ack_PLANT_WATER"] == 1
    assert obs["farms"][0]["tiles"][3][4]["watered_today"]


def test_compound_includes_weed_clearance():
    agent, obs = crop_fixture(weed=True)
    assert [step(agent, obs)[0][0] for _ in range(4)] == [
        ["NORTH"],
        ["DIG"],
        ["PLANT", "STRAWBERRY"],
        ["WATER"],
    ]
    step(agent, obs)
    assert not agent.active


@pytest.mark.parametrize("turn,seeds", [(3, 0), (22, 1)])
def test_compound_requires_seed_and_full_water_budget(turn, seeds):
    agent, obs = crop_fixture(turn=turn, seeds=seeds)
    step(agent, obs)
    assert not agent.active  # H22: MOVE+PLANT fit, WATER does not


def test_failed_plant_does_not_acknowledge_or_emit_water():
    agent, obs = crop_fixture()
    step(agent, obs)
    agent._prepare(obs, {})  # deliberately do not apply PLANT
    obs["hour"] += 1
    agent._prepare(obs, {})
    assert agent.selected[0][0] == ["PLANT", "STRAWBERRY"]
    assert not agent.plant_confirmed
    assert agent.runtime_daily[11]["plant_unacknowledged"] == 1


def test_donor_crop_obligation_retained_until_observed_ack():
    agent, obs = crop_fixture()
    step(agent, obs)
    row = agent.routes[(11, 9)][0]
    farm, private = obs["farms"][0], obs["private"]
    assert agent._planned_or_recovery(row, farm, private, 9, (11, 9))[0] == ["PASS"]
    assert agent.cursors[(11, 9)] == 0
    step(agent, obs)
    step(agent, obs)
    agent._planned_or_recovery(row, farm, private, 9, (11, 9))
    assert agent.cursors[(11, 9)] == 1


def test_baseline_plants_reserve_current_batch_seeds():
    agent, obs = crop_fixture()
    farm = obs["farms"][0]
    farm["hands"] = [[5, 4]]
    obs["private"]["inventories"].append({})
    row = planned("PLANT", turn=3, worker=1, position=(5, 4))
    row["arguments"] = {"crop": "STRAWBERRY"}
    agent.routes[(11, 1)] = [row]
    agent._prepare(obs, {})
    assert agent.selected[1][0] == ["PLANT", "STRAWBERRY"]
    assert not agent.active


def test_post_baseline_eta_does_not_double_count_selected_movement():
    agent, obs = crop_fixture(turn=22)
    farm = obs["farms"][0]
    farm["hands"] = [[4, 4]] * 9
    baseline = [(["PASS"], None)] * 9 + [(["NORTH"], None)]
    assert agent._water_eta(11, 22, 9, (4, 3), farm, baseline) == 24
    farm["hands"][8] = [4, 5]
    assert agent._water_eta(11, 22, 9, (4, 3), farm, baseline) == 25
