"""E18.27: early Melon liquidity in D11, preserving the E18.26 late policy."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

from docs.model_specs.codex.e18.tools.e18_18_capacity_trajectory_planner import (
    SHED_ACCESS,
    CapacityTrajectoryPlanner,
)
from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import (
    JesseBoostD10Controller,
)
from docs.model_specs.codex.e18.tools.e18_26_jesse_boost_d10_controller import (
    load_candidate_config as load_parent,
)

BASE = Path(__file__).resolve().parents[1]
CONFIG = BASE / "configs/CODEX_E18_27_770_D10_D15_CASHFLOW_V1.json"
PARENT_PLAN = BASE / "artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json"
PLAN = BASE / "artifacts/derived/E18_27_770_D10_D15_CASHFLOW_PLAN_V1.json"


def load_candidate_config(path=CONFIG):
    treatment = json.loads(path.read_text(encoding="utf-8"))
    assert (
        hashlib.sha256(PARENT_PLAN.read_bytes()).hexdigest()
        == treatment["parent_plan_sha256"]
    )
    parent = load_parent(BASE / "configs" / treatment["parent_config"])
    config = deepcopy(parent)
    for key, value in treatment["overrides"].items():
        if key == "minimum_hands_by_day":
            assert all(
                10 <= int(day) <= 15 and 0 <= n <= 12 for day, n in value.items()
            )
            config[key].update(value)
        elif key == "q2_plant_day":
            assert value == 12
            config[key] = value
        elif key in {"same_batch_melon_sales", "freeze_opening_market_horizon"}:
            assert value is True
            config[key] = value
        else:
            assert key == "melon_harvest_day" and value == 11
            config[key] = value
    config["candidate_id"] = treatment["candidate_id"]
    config["causal_family"] = treatment["causal_family"]
    config["model_spec_version"] = treatment["candidate_id"].replace("_", "-")
    return config


def build_candidate_plan(path=CONFIG):
    config = load_candidate_config(path)
    planner = CapacityTrajectoryPlanner(config)
    if "q2_plant_day" in config:
        # Stage SW after D11 revenue. Keep the inherited retirement rules;
        # this changes activation dates only, not the closing treatment.
        for coord in (*planner.q2_wheat, *planner.q2_strawberry):
            planner.crop_plant_day[coord] = config["q2_plant_day"]
    original = planner._crop_bundles

    def progress(day):
        print(f"Planning D{day:02d}", flush=True)
        return original(day)

    planner._crop_bundles = progress
    plan = planner.build()
    parent = json.loads(PARENT_PLAN.read_text(encoding="utf-8"))
    assert [r for r in plan["trajectory"] if r["day"] <= 9] == [
        r for r in parent["trajectory"] if r["day"] <= 9
    ]
    plan["treatment_config"] = config
    plan["parent_file_sha256"] = hashlib.sha256(PARENT_PLAN.read_bytes()).hexdigest()
    return plan


class D10D15CashflowController(JesseBoostD10Controller):
    """V1 is schedule-only; V2 acknowledges physically carried Melon drops."""

    def __init__(self, plan, seat=0):
        super().__init__(plan, seat=seat)
        self.opening_reference = None
        if plan.get("treatment_config", {}).get("freeze_opening_market_horizon"):
            self.opening_reference = JesseBoostD10Controller(
                json.loads(PARENT_PLAN.read_text()), seat=seat
            )

    def _remaining_horizon(self, day, turn, requirement_kind, *, horizon_days):
        if day <= 9 and self.opening_reference is not None:
            needed = self._pending_requirements(day, requirement_kind)
            for future in range(day + 1, min(30, day + horizon_days) + 1):
                needed.update(
                    self.opening_reference.requirements.get(future, {}).get(
                        requirement_kind, {}
                    )
                )
            return needed
        return super()._remaining_horizon(
            day, turn, requirement_kind, horizon_days=horizon_days
        )

    @staticmethod
    def _merge_melon_sale(orders, quantity):
        if quantity <= 0:
            return orders
        others = [o for o in orders if o[:2] != ["SELL", "MELON"]]
        # Never evict payroll/feed to make an eleventh order.
        if len(others) >= 10:
            return orders
        return [["SELL", "MELON", quantity], *others]

    def _market_orders(self, observation, day, turn):
        orders = super()._market_orders(observation, day, turn)
        if not (
            10 <= day <= 15
            and self.plan.get("treatment_config", {}).get("same_batch_melon_sales")
        ):
            return orders
        farm = observation["farms"][self.seat]
        private = observation["private"]
        incoming = 0
        for worker, position in enumerate([farm["farmer"], *farm["hands"]]):
            row = self.actions.get((day, turn, worker))
            if row and row["opcode"] == "DROP" and tuple(position) in SHED_ACCESS:
                # The retrying executor exposes only DROP actually emitted in
                # this batch. Use real inventory, never the oracle expected yield.
                incoming += private["inventories"][worker].get("MELON", 0)
        if incoming:
            orders = self._merge_melon_sale(
                orders, private["shed"].get("MELON", 0) + incoming
            )
            if (
                self.market_trace
                and self.market_trace[-1]["day"] == day
                and self.market_trace[-1]["turn"] == turn
            ):
                self.market_trace[-1]["orders"] = deepcopy(orders)
        return orders


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("V1", "V2", "V3"), default="V1")
    args = parser.parse_args()
    config_path = CONFIG.with_name(CONFIG.name.replace("V1", args.variant))
    output = PLAN.with_name(PLAN.name.replace("V1", args.variant))
    if args.variant == "V3":
        # V3 fixes online lookahead only; reuse the exact V2 offline plan.
        plan = json.loads(PLAN.with_name(PLAN.name.replace("V1", "V2")).read_text())
        config = load_candidate_config(config_path)
        assert {
            k: v
            for k, v in config.items()
            if k
            not in {
                "candidate_id",
                "model_spec_version",
                "freeze_opening_market_horizon",
            }
        } == {
            k: v
            for k, v in plan["treatment_config"].items()
            if k
            not in {
                "candidate_id",
                "model_spec_version",
                "freeze_opening_market_horizon",
            }
        }
        plan["treatment_config"] = config
        plan["candidate_id"] = config["candidate_id"]
    else:
        plan = build_candidate_plan(config_path)
    output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "path": str(output),
                "checks": plan["gate_0a_checks"],
                "errors": plan["totals"]["route_errors"],
            },
            indent=2,
        )
    )
