"""E18.28 isolated full-season treatments on the fixed 770 trajectory."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

from agricola.core.state import CROPS
from docs.model_specs.codex.e18.tools.e18_18_capacity_trajectory_planner import (
    SHED_ACCESS,
    Bundle,
    CapacityTrajectoryPlanner,
)
from docs.model_specs.codex.e18.tools.e18_27_d10_d15_cashflow_controller import (
    D10D15CashflowController,
    load_candidate_config,
)

BASE = Path(__file__).resolve().parents[1]
DERIVED = BASE / "artifacts/derived"
PARENT = DERIVED / "E18_27_770_D10_D15_CASHFLOW_PLAN_V3.json"
VARIANTS = ("A", "B", "C", "D_WHEAT", "D_CARROT", "E_WHEAT", "E_CARROT")


def candidate_config(variant):
    assert variant in VARIANTS
    config = load_candidate_config(
        BASE / "configs/CODEX_E18_27_770_D10_D15_CASHFLOW_V3.json"
    )
    config.update(
        candidate_id=f"CODEX_E18_28_770_FULL_SEASON_{variant}_V1",
        model_spec_version=f"CODEX-E18.28-770-FULL-SEASON-{variant}-V1",
        causal_family="FULL_SEASON_WITH_SEPARATE_ABLATIONS",
        variant=variant,
        late_crop="CARROT" if variant in ("C", "D_CARROT", "E_CARROT") else "WHEAT",
        progressive_cows=variant.startswith(("D_", "E_")),
        force_peak_hands_through_day=30,
        terminal_crop_clear_day=30,
        annual_replant_last_day=28 if variant != "A" else 25,
    )
    config["minimum_hands_by_day"].update({str(d): 12 for d in range(25, 31)})
    if config["progressive_cows"]:
        config["freeze_opening_market_horizon"] = False
    return config


class FullSeasonPlanner(CapacityTrajectoryPlanner):
    def __init__(self, config):
        super().__init__(config)
        self.current_day = 0
        for coord in (*self.q2_wheat, *self.q2_strawberry):
            self.crop_plant_day[coord] = 12
        if config["variant"] != "A":
            for coord, day in self.strawberry_retire_day.items():
                if day >= 29:
                    self.strawberry_retire_day[coord] = 30
        if config["progressive_cows"]:
            q0_cows = sorted(
                c for c, (d, s) in self.animal_plan.items() if d == 5 and s == "COW"
            )
            placement_days = (4, 5) if config["variant"].startswith("E_") else (3, 5)
            for coord, day in zip(q0_cows, placement_days, strict=True):
                self.animal_plan[coord] = (day, "COW")
            q1_cows = sorted(
                c for c, (d, s) in self.animal_plan.items() if d == 10 and s == "COW"
            )
            # NE is unlocked through the D7 wool missions. Placement begins D8;
            # no animal route is allowed to race that intra-day dependency.
            for coord, day in zip(q1_cows, (8, 8, 9, 9, 10), strict=True):
                self.animal_plan[coord] = (day, "COW")

    def _worker_capacities(self, hands):
        specs = super()._worker_capacities(hands)
        if self.current_day == 30:
            # The terminal H24 is an observation, not an executable batch.
            specs = [(w, cap - 1, start, pos) for w, cap, start, pos in specs]
        return specs

    def _route(self, day, bundles, raw_capacities, **kwargs):
        if day < 25:
            return super()._route(day, bundles, raw_capacities, **kwargs)
        # The two delayed hires can spawn at any shed access (max distance 2).
        # Reserve that distance explicitly instead of chasing a cyclic nominal
        # spawn/route fixed point. The online executor corrects actual position.
        reserved = [
            (w, cap - (2 if w >= 11 else 0), start, pos)
            for w, cap, start, pos in raw_capacities
        ]
        routes = super()._route(day, bundles, reserved, **kwargs)
        for route in routes:
            if route.worker >= 11:
                route.capacity += 2
                assert route.used + 2 <= route.capacity
        return routes

    def _reconcile_deferred_hire_spawns(self, routes, worker_specs):
        if self.current_day >= 25:
            return worker_specs
        return super()._reconcile_deferred_hire_spawns(routes, worker_specs)

    def _crop_bundles(self, day):
        self.current_day = day
        print(f"{self.config['variant']} planning D{day:02d}", flush=True)
        if day <= 25 or self.config["variant"] == "A":
            return super()._crop_bundles(day)
        bundles = []
        for coord in sorted(self.final_crop_targets):
            state = self.crops.get(coord)
            bundle = Bundle(coord, "CROP")
            if state is not None:
                crop = CROPS[state.crop]
                age = day - state.planted_day
                ongoing = crop["ongoing"]
                retire = ongoing and day >= self.strawberry_retire_day[coord]
                due = (
                    (state.yield_units >= 2 and (day + coord[0] + coord[1]) % 2 == 0)
                    or retire
                    or day == 30
                )
                if ongoing and day == 29:
                    due = False
                annual_age = 3 if state.planted_day >= 26 else 4
                harvest = age >= crop["first_yield_day"] and (
                    (ongoing and due)
                    or (not ongoing and (age >= annual_age or day == 30))
                )
                if (
                    not state.watered_today
                    and not retire
                    and self._should_water(coord, state, day)
                ):
                    self._water(coord, day, bundle)
                if harvest and state.yield_units > 0:
                    self._harvest_crop(coord, day, bundle)
                # Clearing a harvested ongoing plant at the terminal has no
                # resale value and steals an action from HARVEST/DROP/SELL.
                if retire and day < 30 and coord in self.crops:
                    self._dig_crop(coord, day, bundle)
            if coord not in self.crops and day <= 28:
                self._plant(coord, self.config["late_crop"], day, bundle)
            if bundle.actions:
                bundles.append(bundle)
        return bundles

    def _end_day(self, day):
        if day < 30:
            super()._end_day(day)


class FullSeasonController(D10D15CashflowController):
    """Same executor; late sales use acknowledged carried quantities only."""

    def __init__(self, plan, seat=0, reference_plan=None):
        super().__init__(plan, seat)
        if plan["treatment_config"].get("variant", "").startswith("E_"):
            self.activation_day = 1
        self.prefix_reference = None
        if not plan["treatment_config"]["progressive_cows"]:
            self.prefix_reference = D10D15CashflowController(
                deepcopy(reference_plan)
                if reference_plan is not None
                else json.loads(PARENT.read_text()),
                seat,
            )

    def _remaining_horizon(self, day, turn, requirement_kind, *, horizon_days):
        if day <= 24 and self.prefix_reference is not None:
            needed = self._pending_requirements(day, requirement_kind)
            for future in range(day + 1, min(30, day + horizon_days) + 1):
                reference = self.prefix_reference
                if day <= 9 and reference.opening_reference is not None:
                    reference = reference.opening_reference
                needed.update(
                    reference.requirements.get(future, {}).get(requirement_kind, {})
                )
            return needed
        return super()._remaining_horizon(
            day, turn, requirement_kind, horizon_days=horizon_days
        )

    def _remaining(self, day, turn, requirement_kind, *, include_tomorrow):
        if day == 24 and include_tomorrow and self.prefix_reference is not None:
            needed = self._pending_requirements(day, requirement_kind)
            needed.update(
                self.prefix_reference.requirements.get(25, {}).get(requirement_kind, {})
            )
            return needed
        return super()._remaining(
            day, turn, requirement_kind, include_tomorrow=include_tomorrow
        )

    def _market_orders(self, observation, day, turn):
        orders = super()._market_orders(observation, day, turn)
        farm, private = observation["farms"][self.seat], observation["private"]
        owned = Counter(private["shed"])
        for inventory in private["inventories"]:
            owned.update(inventory)
        owned.update(
            t["animal"]
            for row in farm["tiles"]
            for t in row
            if isinstance(t, dict) and t.get("animal")
        )
        limited = []
        for order in orders:
            if order[0] == "BUY_ANIMAL":
                species = order[1]
                quantity = min(
                    order[2],
                    max(0, {"COW": 9, "SHEEP": 5}.get(species, 0) - owned[species]),
                )
                if quantity:
                    limited.append(["BUY_ANIMAL", species, quantity])
                    owned[species] += quantity
            else:
                limited.append(order)
        orders = limited
        if day < 25:
            return orders
        private = observation["private"]
        farm = observation["farms"][self.seat]
        available = Counter(private["shed"])
        for worker, pos in enumerate([farm["farmer"], *farm["hands"]]):
            row = self.actions.get((day, turn, worker))
            if row and row["opcode"] == "DROP" and tuple(pos) in SHED_ACCESS:
                available.update(private["inventories"][worker])
        # Keep inherited feed obligations. Terminal has no next-day purchases.
        reserve = self._remaining(day, turn, "pickup", include_tomorrow=day < 30)
        reserve["WHEAT"] += sum(self.inflight_wheat.get((day, turn), {}).values())
        sales = []
        products = {
            "WHEAT",
            "CARROT",
            "TOMATO",
            "STRAWBERRY",
            "MELON",
            "MILK",
            "WOOL",
            "EGG",
            "FERTILIZER",
        }
        for item in products:
            quantity = max(0, available[item] - reserve[item])
            if quantity:
                sales.append(["SELL", item, quantity])
        prices = observation["market"]["prices"]
        sales.sort(key=lambda o: (-o[2] * prices.get(o[1], 0), o[1]))
        other = [o for o in orders if o[0] != "SELL"]
        merged = [*sales[: max(0, 10 - len(other))], *other][:10]
        return self._net_wheat_orders(merged, 0)[0]


def build(variant):
    config = candidate_config(variant)
    plan = FullSeasonPlanner(config).build()
    plan["treatment_config"] = config
    if not config["progressive_cows"]:
        parent = json.loads(PARENT.read_text())
        assert [r for r in plan["trajectory"] if r["day"] <= 24] == [
            r for r in parent["trajectory"] if r["day"] <= 24
        ]
    output = DERIVED / f"E18_28_FULL_SEASON_{variant}_PLAN_V1.json"
    output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output),
                "checks": plan["gate_0a_checks"],
                "errors": plan["totals"]["route_errors"],
                "illegal": plan["totals"]["illegal_actions"],
            }
        ),
        flush=True,
    )
    return plan


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=VARIANTS, required=True)
    build(parser.parse_args().variant)
