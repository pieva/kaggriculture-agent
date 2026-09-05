from copy import deepcopy

from docs.model_specs.codex.e18.tools.e18_29_spawn_matched_anti_pass_controller import (
    SpawnMatchedAntiPassController,
)


def fixture():
    rows = [
        dict(
            day=21,
            turn=t,
            step=t,
            worker=11,
            opcode="WATER",
            position=[4, 4],
            arguments={},
        )
        for t in range(3, 24)
    ]
    rows += [
        dict(
            day=21,
            turn=t,
            step=t,
            worker=12,
            opcode="WATER",
            position=[5, 5],
            arguments={},
        )
        for t in range(3, 11)
    ]
    plan = {
        "trajectory": rows,
        "daily": [],
        "treatment_config": {"progressive_cows": True},
    }
    agent = SpawnMatchedAntiPassController(plan)
    farm = {"farmer": [3, 4], "hands": [[4, 4]] * 10 + [[5, 5], [4, 4]]}
    private = {"inventories": [{} for _ in range(13)]}
    return agent, farm, private, plan


def test_swap_fresh_routes_only_when_it_repairs_deadline():
    agent, farm, private, plan = fixture()
    original = deepcopy(plan)
    agent._assign_fresh_workers(21, 3, farm, private)
    assert agent.routes[(21, 11)][0]["worker"] == 12
    assert agent.routes[(21, 12)][0]["worker"] == 11
    assert agent.reassignments[0]["original_finish"] == [25, 12]
    assert agent.reassignments[0]["swapped_finish"] == [10, 23]
    assert plan == original
    agent._assign_fresh_workers(21, 4, farm, private)
    assert len(agent.reassignments) == 1


def test_no_swap_when_original_routes_fit():
    agent, farm, private, _ = fixture()
    farm["hands"][10:] = [[4, 4], [5, 5]]
    agent._assign_fresh_workers(21, 3, farm, private)
    assert not agent.reassignments


def test_no_swap_started_or_loaded_worker():
    for mode in ("started", "loaded"):
        agent, farm, private, _ = fixture()
        if mode == "started":
            agent.cursors[(21, 11)] = 1
        else:
            private["inventories"][11] = {"WHEAT": 1}
        agent._assign_fresh_workers(21, 3, farm, private)
        assert not agent.reassignments


def test_no_swap_if_it_only_moves_the_overrun_to_the_other_worker():
    agent, farm, private, _ = fixture()
    farm["hands"][11] = [5, 5]
    agent._assign_fresh_workers(21, 3, farm, private)
    assert not agent.reassignments


def test_wait_until_both_late_hires_are_observed():
    agent, farm, private, _ = fixture()
    shorter = dict(farm, hands=farm["hands"][:10])
    agent._assign_fresh_workers(21, 2, shorter, private)
    assert 21 not in agent.assignment_checked
    agent._assign_fresh_workers(21, 3, farm, private)
    assert agent.reassignments
