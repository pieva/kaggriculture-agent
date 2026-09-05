from copy import deepcopy

from docs.model_specs.codex.e18.tools.e18_29_anti_pass_controller import (
    AntiPassController,
)
from docs.model_specs.codex.e18.tools.e18_29_fertilizer_audit import fertilizer_audit


def fixture(variant="B"):
    agent = AntiPassController(
        {"trajectory": [], "daily": [], "treatment_config": {"progressive_cows": True}},
        variant=variant,
    )
    farm = {
        "farmer": [4, 4],
        "hands": [[4, 4]],
        "tiles": [[None] * 10 for _ in range(10)],
    }
    farm["tiles"][3][4] = {
        "kind": "PASTURE",
        "animal": "COW",
        "fertilizer_available": True,
    }
    private = {"shed": {}, "inventories": [{}, {}]}
    return agent, farm, private


def row(opcode, turn=20):
    return {
        "opcode": opcode,
        "position": [4, 3],
        "turn": turn,
        "step": 0,
        "arguments": {},
    }


def test_off_and_inactive_window():
    for variant, day in [("OFF", 10), ("B", 6), ("A", 13)]:
        agent, farm, private = fixture(variant)
        assert agent._worker_command(day, 10, 0, farm, private)[0] == ["PASS"]
        assert not agent.missions


def test_future_productive_task_is_not_borrowed():
    agent, farm, private = fixture()
    agent.routes[(8, 0)] = [row("WATER")]
    assert agent._worker_command(8, 10, 0, farm, private)[0] == ["PASS"]
    assert not agent.missions


def test_pending_collection_other_worker_is_not_stolen():
    agent, farm, private = fixture()
    agent.routes[(8, 1)] = [row("COLLECT_FERTILIZER")]
    assert agent._worker_command(8, 10, 0, farm, private)[0] == ["PASS"]


def test_same_batch_planned_collection_not_duplicated():
    agent, farm, private = fixture()
    farm["farmer"] = [4, 3]
    agent.routes[(8, 0)] = [row("COLLECT_FERTILIZER", 10)]
    assert agent._worker_command(8, 10, 0, farm, private)[0] == ["COLLECT_FERTILIZER"]
    assert agent._worker_command(8, 10, 1, farm, private)[0] == ["PASS"]


def test_reservation_prevents_duplicate_extra_missions():
    agent, farm, private = fixture()
    assert agent._worker_command(8, 10, 0, farm, private)[0] == ["NORTH"]
    assert agent._worker_command(8, 10, 1, farm, private)[0] == ["PASS"]


def test_complete_budget_includes_return_and_drop():
    agent, farm, private = fixture()
    # NORTH, COLLECT, SOUTH, DROP = four slots. Start H21 is too late.
    assert agent._worker_command(30, 21, 0, farm, private)[0] == ["PASS"]
    assert agent._worker_command(30, 20, 0, farm, private)[0] == ["NORTH"]
    assert agent.missions[(30, 0)]["reserved_actions"] == 4


def test_no_start_with_inventory_or_full_shed():
    for shed, inventory in [({}, {"WHEAT": 1}), ({"WHEAT": 90}, {})]:
        agent, farm, private = fixture()
        private.update(shed=shed, inventories=[inventory, {}])
        assert agent._worker_command(8, 10, 0, farm, private)[0] == ["PASS"]


def test_collect_deliver_ack_and_terminal():
    agent, farm, private = fixture()
    assert agent._worker_command(30, 20, 0, farm, private)[0] == ["NORTH"]
    farm["farmer"] = [4, 3]
    assert agent._worker_command(30, 21, 0, farm, private)[0] == ["COLLECT_FERTILIZER"]
    farm["tiles"][3][4]["fertilizer_available"] = False
    private["inventories"][0] = {"FERTILIZER": 1}
    assert agent._worker_command(30, 22, 0, farm, private)[0] == ["SOUTH"]
    farm["farmer"] = [4, 4]
    command, emitted = agent._worker_command(30, 23, 0, farm, private)
    assert command == ["DROP"] and emitted["arguments"]["expected_items"] == {
        "FERTILIZER": 1
    }
    private["inventories"][0] = {}
    private["shed"]["FERTILIZER"] = 1
    agent.acknowledge_terminal({"farms": [farm, farm], "private": private})
    assert not agent.missions
    assert agent.anti_daily[30]["collection_ack_units"] == 1
    assert agent.anti_daily[30]["missions_completed"] == 1


def test_target_disappeared_returns_to_origin():
    agent, farm, private = fixture()
    agent._worker_command(8, 10, 0, farm, private)
    farm["farmer"] = [4, 3]
    farm["tiles"][3][4]["fertilizer_available"] = False
    assert agent._worker_command(8, 11, 0, farm, private)[0] == ["SOUTH"]
    farm["farmer"] = [4, 4]
    agent._worker_command(8, 12, 0, farm, private)
    assert not agent.missions
    assert agent.anti_daily[8]["target_cancelled"] == 1


def test_unacknowledged_collection_is_not_counted():
    agent, farm, private = fixture()
    farm["farmer"] = [4, 3]
    agent._worker_command(8, 10, 0, farm, private)
    agent._worker_command(8, 11, 0, farm, private)
    assert agent.anti_daily[8]["collection_failed"] == 1
    assert agent.anti_daily[8]["collection_ack_units"] == 0


def test_parent_plan_not_mutated():
    plan = {
        "trajectory": [],
        "daily": [],
        "treatment_config": {"progressive_cows": True},
    }
    original = deepcopy(plan)
    AntiPassController(plan)
    assert plan == original


def test_delivery_reserves_room_for_other_workers_same_batch():
    agent, farm, private = fixture()
    agent.missions[(8, 0)] = {"phase": "DELIVER", "shed": (4, 4), "origin": (4, 4)}
    private["shed"] = {"WHEAT": 90}
    private["inventories"] = [{"FERTILIZER": 1}, {"MILK": 10}]
    assert agent._worker_command(8, 20, 0, farm, private)[0] == ["PASS"]
    assert agent.missions[(8, 0)]["phase"] == "DELIVER"


def test_audit_distinguishes_destroyed_inventory_from_delivery():
    _, farm, private = fixture()
    private.update(shed={"WHEAT": 100}, inventories=[{"FERTILIZER": 1}, {}], seeds={})
    replay = {
        "configuration": {},
        "steps": [
            [{"observation": {"day": 7, "farms": [farm], "private": private}}],
            [{"action": {"farmer": ["DROP"], "hands": [["PASS"]]}}],
        ],
    }
    stats = fertilizer_audit(replay, 0)[7]
    assert stats["delivered"] == 0 and stats["drop_destroyed"] == 1


def test_audit_records_real_collection():
    _, farm, private = fixture()
    farm["farmer"] = [4, 3]
    private["seeds"] = {}
    replay = {
        "configuration": {},
        "steps": [
            [{"observation": {"day": 7, "farms": [farm], "private": private}}],
            [{"action": {"farmer": ["COLLECT_FERTILIZER"], "hands": [["PASS"]]}}],
        ],
    }
    assert fertilizer_audit(replay, 0)[7]["collected"] == 1
