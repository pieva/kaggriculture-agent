from __future__ import annotations

import json
from copy import deepcopy
from unittest.mock import patch

from docs.model_specs.codex.e18.tools.e18_27_d10_d15_cashflow_controller import (
    PARENT_PLAN,
    PLAN,
    D10D15CashflowController,
    load_candidate_config,
)


def plans():
    return json.loads(PLAN.read_text()), json.loads(PARENT_PLAN.read_text())


def test_only_declared_config_family_changes():
    config = load_candidate_config()
    assert config["melon_harvest_day"] == 11
    assert config["minimum_hands_by_day"]["11"] == 11
    assert config["topology"] == "7-7-0"
    assert config["livestock_resource_cap"] == 14
    assert config["workers_peak_hands"] == 12
    assert config["annual_replant_last_day"] == 25
    assert config["terminal_crop_clear_day"] == 29


def test_plan_changes_only_d11_d13_not_opening_or_closure():
    candidate, parent = plans()
    for day in range(1, 31):
        a = [r for r in candidate["trajectory"] if r["day"] == day]
        b = [r for r in parent["trajectory"] if r["day"] == day]
        assert (a != b) == (day in (11, 12, 13))


def test_safe_plan_exposes_failed_legacy_peak_instead_of_masking_it():
    plan, _ = plans()
    assert plan["totals"]["illegal_actions"] == []
    assert plan["totals"]["route_errors"] == []
    assert plan["totals"]["animal_losses"] == plan["totals"]["crop_losses"] == 0
    assert plan["gate_0a_checks"]["peak_62_crops_by_d13"] is False
    assert plan["gate_0a_passed"] is False
    assert plan["snapshots"]["D15"]["crops"] == {"STRAWBERRY": 38, "WHEAT": 23}


def test_controller_binds_new_capacity_without_mutating_parent():
    plan, parent = plans()
    candidate = D10D15CashflowController(plan, seat=1)
    assert candidate.daily_hands[11] == 11
    assert candidate.daily_hands[12] == 7
    assert candidate.daily_hands[13] == 8
    assert parent["daily"][10]["planned_hands"] == 8


def test_all_planned_melon_harvests_are_in_d11():
    plan, _ = plans()
    melon = [
        r
        for r in plan["trajectory"]
        if r["opcode"] == "HARVEST" and r["arguments"].get("crop") == "MELON"
    ]
    assert len(melon) == 12
    assert {r["day"] for r in melon} == {11}


def test_melon_sale_never_evicts_payroll_or_feed():
    full = [["HIRE"] for _ in range(9)] + [["BUY_PRODUCT", "WHEAT", 13]]
    assert D10D15CashflowController._merge_melon_sale(full, 71) == full
    assert D10D15CashflowController._merge_melon_sale(full, 0) == full


def test_same_batch_sale_uses_real_inventory_and_preserves_other_orders():
    plan, _ = plans()
    plan["treatment_config"]["same_batch_melon_sales"] = True
    controller = D10D15CashflowController(plan)
    controller.actions[(11, 20, 0)] = {
        "opcode": "DROP",
        "arguments": {"expected_items": {"MELON": 72}},
    }
    obs = {
        "farms": [{"farmer": [4, 4], "hands": []}],
        "private": {"shed": {"MELON": 3}, "inventories": [{"MELON": 5}]},
    }
    original = deepcopy(obs)
    base = [["SELL", "MELON", 3], ["BUY_PRODUCT", "WHEAT", 13]]
    with patch(
        "docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller.JesseBoostD10Controller._market_orders",
        return_value=base,
    ):
        assert controller._market_orders(obs, 11, 20) == [
            ["SELL", "MELON", 8],
            ["BUY_PRODUCT", "WHEAT", 13],
        ]
        assert controller._market_orders(obs, 16, 20) == base
        obs["farms"][0]["farmer"] = [0, 0]
        assert controller._market_orders(obs, 11, 20) == base
    obs["farms"][0]["farmer"] = [4, 4]
    assert obs == original


def test_v1_does_not_activate_v2_market_bridge():
    plan, _ = plans()
    controller = D10D15CashflowController(plan)
    base = [["BUY_PRODUCT", "WHEAT", 13]]
    with patch(
        "docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller.JesseBoostD10Controller._market_orders",
        return_value=base,
    ):
        assert controller._market_orders({}, 11, 20) == base


def test_v3_freezes_opening_lookahead_and_preserves_v2_offline_routes():
    candidate = json.loads(PLAN.with_name(PLAN.name.replace("V1", "V3")).read_text())
    prior = json.loads(PLAN.with_name(PLAN.name.replace("V1", "V2")).read_text())
    parent = json.loads(PARENT_PLAN.read_text())
    assert candidate["trajectory"] == prior["trajectory"]
    assert (
        candidate["calendar"]["strawberry_retire_day"]
        == parent["calendar"]["strawberry_retire_day"]
    )
    executor = D10D15CashflowController(candidate)
    reference = executor.opening_reference
    assert reference is not None
    for day in range(1, 10):
        for kind in ("pickup", "seed"):
            assert executor._remaining_horizon(
                day, 1, kind, horizon_days=5
            ) == reference._remaining_horizon(day, 1, kind, horizon_days=5)
    assert executor._remaining_horizon(
        10, 1, "seed", horizon_days=1
    ) != reference._remaining_horizon(10, 1, "seed", horizon_days=1)
