from copy import deepcopy

from docs.model_specs.codex.e18.tests.test_e18_29_anti_pass import fixture, row
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import (
    crop_service_audit,
)
from docs.model_specs.codex.e18.tools.e18_29_service_safe_anti_pass_controller import (
    ServiceSafeAntiPassController,
)


def setup():
    _, farm, private = fixture()
    agent = ServiceSafeAntiPassController(
        {"trajectory": [], "daily": [], "treatment_config": {"progressive_cows": True}}
    )
    farm["farmer"] = [4, 3]
    farm["tiles"][3][4] = {"kind": "PLANT", "crop": "WHEAT", "watered_today": False}
    private["inventories"][0] = {"FERTILIZER": 1}
    return agent, farm, private


def test_optional_boost_preempted_when_last_water_would_overrun():
    agent, farm, private = setup()
    agent.current_turn = 24
    agent.routes[(21, 0)] = [row("FERTILIZE", 22), row("WATER", 23)]
    assert agent._planned_or_recovery(
        agent.routes[(21, 0)][0], farm, private, 0, (21, 0)
    )[0] == ["PASS"]
    assert agent.cursors[(21, 0)] == 1
    assert agent.anti_daily[21]["optional_fertilize_preempted"] == 1


def test_boost_kept_when_service_fits():
    agent, farm, private = setup()
    agent.current_turn = 23
    agent.routes[(21, 0)] = [row("FERTILIZE", 22), row("WATER", 23)]
    assert agent._planned_or_recovery(
        agent.routes[(21, 0)][0], farm, private, 0, (21, 0)
    )[0] == ["FERTILIZE"]
    assert agent.anti_daily[21]["optional_fertilize_preempted"] == 0


def test_forecast_accounts_for_actual_position_and_future_calendar():
    agent, _, _ = setup()
    agent.current_turn = 10
    agent.routes[(21, 0)] = [row("FERTILIZE", 11), row("WATER", 23)]
    assert agent._earliest_route_finish((21, 0), (4, 5)) == 23
    agent.current_turn = 22
    assert agent._earliest_route_finish((21, 0), (4, 5)) == 25


def test_d30_deadline_is_h23():
    agent, farm, private = setup()
    agent.current_turn = 23
    agent.routes[(30, 0)] = [row("FERTILIZE", 22), row("WATER", 23)]
    assert agent._planned_or_recovery(
        agent.routes[(30, 0)][0], farm, private, 0, (30, 0)
    )[0] == ["PASS"]


def test_crop_audit_detects_new_unwatered_plant_in_last_batch():
    _, farm, private = fixture()
    farm["tiles"][4][4] = None
    private.update(seeds={"WHEAT": 1})
    after = deepcopy(farm)
    after["tiles"][4][4] = {"kind": "WEED"}
    replay = {
        "configuration": {},
        "steps": [
            [{"observation": {"day": 20, "farms": [farm], "private": private}}],
            [
                {
                    "action": {"farmer": ["PLANT", "WHEAT"], "hands": [["PASS"]]},
                    "observation": {"day": 21, "farms": [after]},
                }
            ],
        ],
    }
    assert crop_service_audit(replay, 0) == [
        {"service_day": 21, "position": [4, 4], "crop": "WHEAT"}
    ]


def test_crop_audit_does_not_call_spontaneous_weed_a_water_death():
    _, farm, private = fixture()
    private.update(seeds={})
    after = deepcopy(farm)
    after["tiles"][4][4] = {"kind": "WEED"}
    replay = {
        "configuration": {},
        "steps": [
            [{"observation": {"day": 20, "farms": [farm], "private": private}}],
            [
                {
                    "action": {"farmer": ["PASS"]},
                    "observation": {"day": 21, "farms": [after]},
                }
            ],
        ],
    }
    assert crop_service_audit(replay, 0) == []
