import json

from docs.model_specs.codex.e18.tools.e18_27_d10_d15_cashflow_controller import (
    D10D15CashflowController,
)
from docs.model_specs.codex.e18.tools.e18_28_full_season_controller import (
    DERIVED,
    FullSeasonController,
    FullSeasonPlanner,
    candidate_config,
)


def controller():
    return FullSeasonController(
        {"trajectory": [], "daily": [], "treatment_config": {"progressive_cows": True}},
        0,
    )


def observation(shed=None, inventory=None):
    farm = {"farmer": [4, 4], "hands": [], "tiles": [[None] * 10 for _ in range(10)]}
    return {
        "farms": [farm, farm],
        "private": {"shed": shed or {}, "inventories": [inventory or {}]},
        "market": {"prices": {"WHEAT": 30, "CARROT": 50, "MILK": 100}},
    }


def test_same_batch_sale_uses_actual_inventory(monkeypatch):
    monkeypatch.setattr(
        D10D15CashflowController, "_market_orders", lambda *a: [["SELL", "CARROT", 999]]
    )
    agent = controller()
    agent.actions[(30, 23, 0)] = {"opcode": "DROP"}
    orders = agent._market_orders(observation({"CARROT": 2}, {"CARROT": 3}), 30, 23)
    assert orders == [["SELL", "CARROT", 5]]


def test_feed_inflight_not_sold_and_round_trip_netted(monkeypatch):
    monkeypatch.setattr(
        D10D15CashflowController,
        "_market_orders",
        lambda *a: [["BUY_PRODUCT", "WHEAT", 2]],
    )
    agent = controller()
    agent.inflight_wheat[(28, 4)][0] = 3
    orders = agent._market_orders(observation({"WHEAT": 8}), 28, 4)
    assert orders == [["SELL", "WHEAT", 3]]


def test_animal_cap_covers_carried_and_shed(monkeypatch):
    monkeypatch.setattr(
        D10D15CashflowController,
        "_market_orders",
        lambda *a: [["BUY_ANIMAL", "COW", 20], ["BUY_ANIMAL", "SHEEP", 20]],
    )
    orders = controller()._market_orders(
        observation({"COW": 8, "SHEEP": 4}, {"COW": 1}), 8, 1
    )
    assert orders == [["BUY_ANIMAL", "SHEEP", 1]]


def test_progressive_calendar():
    planner = FullSeasonPlanner(candidate_config("D_CARROT"))
    count = [
        sum(
            day <= d and species == "COW"
            for day, species in planner.animal_plan.values()
        )
        for d in range(1, 11)
    ]
    assert count == [2, 2, 3, 3, 4, 4, 4, 6, 8, 9]


def test_late_plans_safe_and_species_ablation_matched():
    plans = [
        json.loads((DERIVED / f"E18_28_FULL_SEASON_{v}_PLAN_V1.json").read_text())
        for v in ("B", "C")
    ]
    for plan in plans:
        assert plan["gate_0a_checks"]["all_daily_routes_feasible"]
        assert plan["totals"]["crop_losses"] == plan["totals"]["animal_losses"] == 0
        assert all(r["planned_hands"] == 12 for r in plan["daily"][24:])
        assert all(r["day"] <= 28 for r in plan["trajectory"] if r["opcode"] == "PLANT")
        assert all(
            r["turn"] <= 23
            for r in plan["trajectory"]
            if r["day"] == 30 and r["opcode"] != "PASS"
        )
        assert not any(
            r["day"] == 30 and r["opcode"] == "DIG" for r in plan["trajectory"]
        )

    def schedule(plan):
        return [
            (r["day"], r["turn"], r["worker"], r["opcode"], r["position"])
            for r in plan["trajectory"]
        ]

    assert schedule(plans[0]) == schedule(plans[1])
