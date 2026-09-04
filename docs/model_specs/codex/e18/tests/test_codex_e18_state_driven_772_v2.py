"""Contract tests for the E18.4 V2 locality/task-aging dispatcher."""

from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace

from agricola.strategy.codex.codex_e18_state_driven_772_v2 import (
    E18_STATE_DRIVEN_V2_MODEL_SPEC_VERSION,
    CodexE18StateDriven772V2Agent,
    create_codex_e18_state_driven_772_v2,
    load_e18_state_driven_v2_config,
)


def _provider(observation, configuration=None):
    del observation, configuration
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _observation(
    *,
    day: int,
    hour: int = 0,
    farmer: tuple[int, int] = (4, 4),
    hands: list[tuple[int, int]] | None = None,
    inventories: list[dict] | None = None,
) -> dict:
    farm = {
        "money": 10_000,
        "tiles": [[None for _ in range(10)] for _ in range(10)],
        "farmer": list(farmer),
        "hands": [list(value) for value in (hands or [])],
        "unlocked_quadrants": ["NW", "NE", "SW"],
    }
    return {
        "step": day * 24 + hour,
        "day": day,
        "hour": hour,
        "player": 0,
        "farms": [farm, deepcopy(farm)],
        "private": {
            "shed": {},
            "inventories": inventories or [{} for _ in range(1 + len(hands or []))],
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


def _agent() -> CodexE18StateDriven772V2Agent:
    return CodexE18StateDriven772V2Agent(base_policy=_provider)


def _set_clock(agent: CodexE18StateDriven772V2Agent, step: int) -> None:
    agent._routing_clock = SimpleNamespace(step=step, day=step // 24, hour=step % 24)
    agent._routing_board_size = 10
    agent._routing_farm = {
        "tiles": [[None for _ in range(10)] for _ in range(10)]
    }


def test_config_changes_only_dispatch_metadata_and_keeps_exact_772() -> None:
    config = load_e18_state_driven_v2_config()
    assert config["model_spec_version"] == E18_STATE_DRIVEN_V2_MODEL_SPEC_VERSION
    assert len(config["pasture_targets"]) == 16
    assert config["pasture_livestock_cap"] == 16
    assert config["activation_day"] == 11


def test_bootstrap_is_exact_e18_2_passthrough_through_day_10() -> None:
    expected = {
        "farmer": ["NORTH"],
        "hands": [["PASS"]],
        "market": [["BUY_SEED", "WHEAT", 1]],
    }

    def provider(observation, configuration=None):
        del observation, configuration
        return deepcopy(expected)

    policy = create_codex_e18_state_driven_772_v2(base_policy=provider)
    assert policy(_observation(day=10, hands=[(3, 3)]), _configuration()) == expected


def test_home_cluster_ownership_survives_day_change_and_position_change() -> None:
    agent = _agent()
    private = {"seeds": {}, "shed": {}, "inventories": [{}, {}]}
    tasks = [
        agent._task("WATER", (2, 2), ("WATER",)),
        agent._task("WATER", (7, 2), ("WATER",)),
    ]
    _set_clock(agent, 11 * 24)
    agent._assign(tasks, [(1, 1), (8, 1)], private)
    original = dict(agent.home_clusters)
    _set_clock(agent, 12 * 24)
    agent._assign(tasks, [(8, 1), (1, 1)], private)
    assert agent.home_clusters == original


def test_initial_ownership_reserves_labor_for_both_primary_clusters() -> None:
    agent = _agent()
    private = {
        "seeds": {},
        "shed": {},
        "inventories": [{} for _ in range(13)],
    }
    tasks = [
        *(agent._task("WATER", (x, 2), ("WATER",)) for x in range(2, 5)),
        *(agent._task("WATER", (x, 2), ("WATER",)) for x in range(5, 8)),
    ]
    _set_clock(agent, 11 * 24)
    agent._assign(tasks, [(4, 4) for _ in range(13)], private)
    counts = {
        cluster: list(agent.home_clusters.values()).count(cluster)
        for cluster in set(agent.home_clusters.values())
    }
    assert counts["Q0_NW"] >= 3
    assert counts["Q1_NE"] >= 3
    assert counts["SHED_CORRIDOR"] <= 2


def test_sticky_task_is_not_preempted_by_nearer_ordinary_task() -> None:
    agent = _agent()
    private = {"seeds": {}, "shed": {}, "inventories": [{}]}
    sticky = agent._task("WATER", (4, 2), ("WATER",))
    _set_clock(agent, 11 * 24)
    first = agent._assign([sticky], [(2, 2)], private)
    agent.last_assignments = {0: first[0].identity}
    _set_clock(agent, 11 * 24 + 1)
    nearer = agent._task("WATER", (3, 2), ("WATER",))
    second = agent._assign([sticky, nearer], [(2, 2)], private)
    assert second[0].identity == sticky.identity


def test_aging_breaks_same_class_distance_tie_without_safety_reordering() -> None:
    agent = _agent()
    private = {"seeds": {}, "shed": {}, "inventories": [{}]}
    old = agent._task("WATER", (4, 2), ("WATER",))
    _set_clock(agent, 11 * 24)
    agent._assign([old], [(2, 2)], private)
    agent.last_assignments = {}
    agent.task_states[old.identity].assigned_worker = None
    _set_clock(agent, 11 * 24 + 12)
    new = agent._task("WATER", (3, 2), ("WATER",))
    assignment = agent._assign([old, new], [(2, 2)], private)
    assert assignment[0].identity == old.identity


def test_wheat_carrier_affinity_selects_feed_compatible_worker() -> None:
    agent = _agent()
    private = {
        "seeds": {},
        "shed": {},
        "inventories": [{}, {"WHEAT": 2}],
    }
    task = agent._task(
        "FEED", (3, 3), ("FEED",), allowed_workers=(1,), resource="WHEAT"
    )
    _set_clock(agent, 11 * 24)
    assignment = agent._assign([task], [(2, 3), (2, 3)], private)
    assert assignment == {1: task}


def test_remote_emergency_enables_traced_cross_cluster_transfer() -> None:
    agent = _agent()
    private = {
        "seeds": {},
        "shed": {},
        "inventories": [{"WHEAT": 2}],
    }
    task = agent._task(
        "CRITICAL_FEED",
        (7, 2),
        ("FEED",),
        allowed_workers=(0,),
        resource="WHEAT",
    )
    _set_clock(agent, 11 * 24)
    agent.home_clusters[0] = "Q0_NW"
    assignment = agent._assign([task], [(2, 2)], private)
    assert assignment == {0: task}
    assert agent.cross_cluster_transfers["REMOTE_EMERGENCY_NO_OWNER"] == 1


def test_worker_on_actionable_tile_services_before_moving() -> None:
    observation = _observation(day=11, farmer=(4, 4))
    observation["farms"][0]["tiles"][4][4] = {
        "kind": "PLANT",
        "crop": "WHEAT",
        "planted_day": 10,
        "watered_today": False,
        "consecutive_unwatered": 1,
        "yield_units": 0,
    }
    policy = create_codex_e18_state_driven_772_v2(base_policy=_provider)
    action = policy(observation, _configuration())
    assert action["farmer"] == ["WATER"]
    assert policy.codex_e18_state_driven_v2_instance.pass_on_actionable_violations == []


def test_route_reversal_within_four_steps_is_recorded() -> None:
    agent = _agent()
    agent._routing_clock = SimpleNamespace(step=300, day=12, hour=12)
    agent._routing_farm = {"farmer": [1, 1], "hands": [], "tiles": []}
    agent.home_clusters[0] = "Q0_NW"
    agent._record_emitted_dispatch({"farmer": ["EAST"], "hands": []})
    agent._routing_clock = SimpleNamespace(step=301, day=12, hour=13)
    agent._routing_farm["farmer"] = [2, 1]
    agent._record_emitted_dispatch({"farmer": ["WEST"], "hands": []})
    assert len(agent.route_thrashing_violations) == 1


def test_dispatch_is_deterministic_for_equal_observations() -> None:
    observation = _observation(day=11, farmer=(4, 4), hands=[(3, 4)])
    for farm in observation["farms"]:
        farm["tiles"][4][4] = {
            "kind": "PLANT",
            "crop": "WHEAT",
            "planted_day": 10,
            "watered_today": False,
            "consecutive_unwatered": 0,
            "yield_units": 0,
        }
    left = create_codex_e18_state_driven_772_v2(base_policy=_provider)
    right = create_codex_e18_state_driven_772_v2(base_policy=_provider)
    assert left(deepcopy(observation), _configuration()) == right(
        deepcopy(observation), _configuration()
    )
