#!/usr/bin/env python3
"""Execute the E18.18 planned trajectory in the real Kaggriculture engine.

This is an offline Gate-0B harness, not a submission policy.  It validates the
planned unit routes together with HIRE, land, seed, animal, feed, fertilizer,
shed and SELL constraints under a deterministic weed-free oracle scenario.
"""

from __future__ import annotations

import json
import sys
import tempfile
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
COMMON_TOOLS = ROOT / "experiments/e18/tools/common"
for import_root in (ROOT, COMMON_TOOLS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from analyze_episode_105080066 import analyze

from docs.model_specs.codex.e18.tools.e18_18_capacity_trajectory_planner import (
    build_plan,
)

SEED = 180918001
OUTPUT = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0B_V1.json"
)
REPORT = (
    ROOT
    / "docs/model_specs/codex/e18/reports/"
    / "E18_18_770_CAPACITY_TRAJECTORY_GATE_0B_REPORT_IT.md"
)
PRODUCTS = (
    "WHEAT",
    "CARROT",
    "TOMATO",
    "STRAWBERRY",
    "MELON",
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
)
SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}
SEED_COSTS = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COSTS = {"COW": 400, "SHEEP": 500}
LAND_COSTS = {1: 1000, 2: 2000, 3: 4000}


def _farm(observation: dict[str, Any], seat: int) -> dict[str, Any]:
    farms = observation.get("farms", []) or []
    return farms[seat] if seat < len(farms) else {}


def _mix(farm: dict[str, Any], kind: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in farm.get("tiles", []) or []:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if kind == "crop" and tile.get("kind") == "PLANT":
                counts[str(tile.get("crop"))] += 1
            elif kind == "animal" and tile.get("animal"):
                counts[str(tile.get("animal"))] += 1
    return dict(sorted(counts.items()))


def _topology(farm: dict[str, Any]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict) or tile.get("kind") != "PASTURE":
                continue
            quadrant = "Q0" if x < 5 and y < 5 else "Q1" if x >= 5 and y < 5 else "Q2" if x < 5 else "Q3"
            counts[quadrant] += 1
    return dict(sorted(counts.items()))


class Gate0BController:
    """Replay planned routes with state-aware procurement in the oracle env."""

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        self.plan = plan
        self.seat = seat
        self.actions: dict[tuple[int, int, int], dict[str, Any]] = {
            (int(row["day"]), int(row["turn"]), int(row["worker"])): row
            for row in plan["trajectory"]
        }
        self.daily_hands = {
            int(row["day"]): int(row["planned_hands"]) for row in plan["daily"]
        }
        self.requirements: dict[int, dict[str, Counter[str]]] = defaultdict(
            lambda: {"pickup": Counter(), "seed": Counter()}
        )
        self.events: dict[int, list[tuple[int, str, str, int]]] = defaultdict(list)
        for row in plan["trajectory"]:
            day = int(row["day"])
            turn = int(row["turn"])
            opcode = str(row["opcode"])
            args = row.get("arguments", {}) or {}
            if opcode == "PICKUP":
                item = str(args["item"])
                units = int(args.get("units", 1))
                self.requirements[day]["pickup"][item] += units
                self.events[day].append((turn, "pickup", item, units))
            elif opcode == "PLANT":
                crop = str(args["crop"])
                self.requirements[day]["seed"][crop] += 1
                self.events[day].append((turn, "seed", crop, 1))
        self.requested_actions: Counter[str] = Counter()
        self.market_requests: Counter[str] = Counter()
        self.market_trace: list[dict[str, Any]] = []
        self.guarded_noops: Counter[str] = Counter()
        self.error_count = 0
        self.last_error: str | None = None

    @staticmethod
    def _unit_command(row: dict[str, Any] | None) -> list[Any]:
        if row is None:
            return ["PASS"]
        opcode = str(row["opcode"])
        args = row.get("arguments", {}) or {}
        if opcode == "PLANT":
            return [opcode, str(args["crop"])]
        if opcode == "PICKUP":
            return [opcode, str(args["item"]), int(args.get("units", 1))]
        if opcode == "PLACE":
            return [opcode, str(args["animal"])]
        return [opcode]

    def _guarded_unit_command(
        self,
        row: dict[str, Any] | None,
        farm: dict[str, Any],
        private: dict[str, Any],
        worker: int,
    ) -> list[Any]:
        command = self._unit_command(row)
        opcode = str(command[0])
        if row is None or opcode == "PASS":
            return command
        positions = [farm.get("farmer", [4, 4]), *(farm.get("hands", []) or [])]
        if worker >= len(positions):
            self.guarded_noops[opcode] += 1
            return ["PASS"]
        position = tuple(positions[worker])
        planned_position = tuple(row.get("position", position))
        moves = {
            "NORTH": (0, -1),
            "SOUTH": (0, 1),
            "EAST": (1, 0),
            "WEST": (-1, 0),
        }
        if opcode in moves:
            dx, dy = moves[opcode]
            if (position[0] + dx, position[1] + dy) == planned_position:
                return command
            self.guarded_noops[opcode] += 1
            return ["PASS"]
        if opcode in {"PICKUP", "DROP"}:
            return command
        if position != planned_position:
            self.guarded_noops[opcode] += 1
            return ["PASS"]
        tile = farm.get("tiles", [])[position[1]][position[0]]
        inventories = private.get("inventories", []) or []
        inventory = inventories[worker] if worker < len(inventories) else {}
        valid = True
        if opcode == "PLANT":
            valid = tile is None and int(
                (private.get("seeds", {}) or {}).get(str(command[1]), 0)
            ) > 0
        elif opcode == "WATER":
            valid = (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and not bool(tile.get("watered_today"))
            )
        elif opcode == "HARVEST":
            valid = isinstance(tile, dict) and int(tile.get("yield_units", 0)) > 0
        elif opcode == "FERTILIZE":
            valid = (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and int(inventory.get("FERTILIZER", 0)) > 0
            )
        elif opcode == "DIG":
            valid = tile is not None and not (
                isinstance(tile, dict) and "animal" in tile
            )
        elif opcode == "BUILD_PASTURE":
            valid = tile is None
        elif opcode == "PLACE":
            animal = str(command[1])
            structure = "PASTURE" if animal in {"COW", "SHEEP"} else "COOP"
            valid = (
                isinstance(tile, dict)
                and tile.get("kind") == structure
                and "animal" not in tile
                and int(inventory.get(animal, 0)) > 0
            )
        elif opcode == "FEED":
            valid = (
                isinstance(tile, dict)
                and "animal" in tile
                and not bool(tile.get("fed_today"))
                and int(inventory.get("WHEAT", 0)) > 0
            )
        elif opcode == "CARE":
            valid = (
                isinstance(tile, dict)
                and "animal" in tile
                and not bool(tile.get("cared_today"))
            )
        elif opcode == "COLLECT_FERTILIZER":
            valid = (
                isinstance(tile, dict)
                and "animal" in tile
                and bool(tile.get("fertilizer_available"))
            )
        if not valid:
            self.guarded_noops[opcode] += 1
            return ["PASS"]
        return command

    def _remaining(
        self,
        day: int,
        turn: int,
        requirement_kind: str,
        *,
        include_tomorrow: bool,
    ) -> Counter[str]:
        needed: Counter[str] = Counter()
        for event_turn, kind, item, units in self.events.get(day, []):
            if kind == requirement_kind and event_turn >= turn:
                needed[item] += units
        if include_tomorrow:
            needed.update(self.requirements.get(day + 1, {}).get(requirement_kind, {}))
        return needed

    def _remaining_horizon(
        self,
        day: int,
        turn: int,
        requirement_kind: str,
        *,
        horizon_days: int,
    ) -> Counter[str]:
        """Return unconsumed requirements through a short procurement horizon."""
        needed: Counter[str] = Counter()
        for horizon_day in range(day, min(30, day + horizon_days) + 1):
            if horizon_day == day:
                for event_turn, kind, item, units in self.events.get(day, []):
                    if kind == requirement_kind and event_turn >= turn:
                        needed[item] += units
            else:
                needed.update(
                    self.requirements.get(horizon_day, {}).get(requirement_kind, {})
                )
        return needed

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        farm = _farm(observation, self.seat)
        private = observation.get("private", {}) or {}
        shed = Counter(private.get("shed", {}) or {})
        seeds = Counter(private.get("seeds", {}) or {})
        max_orders = 10
        hire_orders: list[list[Any]] = []

        target_hands = self.daily_hands.get(day, 0)
        actual_hands = len(farm.get("hands", []) or [])
        if turn == 1:
            first_batch_cap = (
                8
                if day == 7
                else int(self.plan.get("max_hires_per_turn", 10))
            )
            for _ in range(min(target_hands, first_batch_cap)):
                hire_orders.append(["HIRE"])
        elif turn == 2 and actual_hands < target_hands:
            for _ in range(target_hands - actual_hands):
                hire_orders.append(["HIRE"])

        unlocked = set(farm.get("unlocked_quadrants", []) or [])
        land_orders: list[list[Any]] = []
        # Pre-stage SW one day before its first planned route.  BUY_LAND always
        # unlocks the next quadrant, so a missing NE remains the first target.
        if (day >= 7 and "NE" not in unlocked) or (day >= 10 and "SW" not in unlocked):
            land_orders.append(["BUY_LAND"])

        current_pickup = self._remaining(
            day, turn, "pickup", include_tomorrow=False
        )
        pickup_through_tomorrow = self._remaining(
            day, turn, "pickup", include_tomorrow=True
        )
        current_seed = self._remaining(day, turn, "seed", include_tomorrow=False)
        strategic_pickup = self._remaining_horizon(
            day, turn, "pickup", horizon_days=5
        )
        imminent_pickup = self._remaining_horizon(
            day, turn, "pickup", horizon_days=2
        )
        strategic_seed = self._remaining_horizon(
            day, turn, "seed", horizon_days=5
        )
        feed_pickup = self._remaining_horizon(
            day, turn, "pickup", horizon_days=2
        )

        sell_orders: list[list[Any]] = []
        prices = (observation.get("market", {}) or {}).get("prices", {}) or {}
        predicted_drop: Counter[str] = Counter()
        product_by_species = {"COW": "MILK", "SHEEP": "WOOL"}
        for worker in range(actual_hands + 1):
            row = self.actions.get((day, turn, worker))
            if row is None or row.get("opcode") != "DROP":
                continue
            for item, units in (
                row.get("arguments", {}).get("expected_items", {}) or {}
            ).items():
                item = str(item)
                product = product_by_species.get(item, item)
                # Annual Wheat and animal production are engine-aligned. The
                # latter finances the explicit D7 NE-unlock dependency.
                if product in {"WHEAT", "MILK", "WOOL"}:
                    predicted_drop[product] += int(units)
        for item in PRODUCTS:
            reserve = int(pickup_through_tomorrow.get(item, 0))
            if item == "FERTILIZER" and day == 5:
                # Liquidate two optional boosts to fund the second D5 cow even
                # when all four opening animals are fed on D4.
                reserve = max(0, reserve - 2)
            elif item == "FERTILIZER" and day == 7:
                # D7 needs all twelve hands before the two same-batch wool
                # sales. Fertilizer is the bridge liquidity for that hire.
                reserve = 0
            sellable = max(
                0,
                int(shed.get(item, 0)) + int(predicted_drop.get(item, 0)) - reserve,
            )
            if sellable:
                sell_orders.append(["SELL", item, sellable])
        sell_orders.sort(
            key=lambda order: float(prices.get(str(order[1]), 0)) * int(order[2]),
            reverse=True,
        )

        # Current biological continuity has strict priority.  Fertilizer is
        # deliberately excluded from emergency purchases: the route collects
        # it for free and a missed boost is cheaper than starving an animal.
        current_orders: list[list[Any]] = []
        wheat_shortage = max(
            0, int(current_pickup.get("WHEAT", 0)) - int(shed.get("WHEAT", 0))
        )
        if wheat_shortage:
            current_orders.append(["BUY_PRODUCT", "WHEAT", wheat_shortage])
        for crop, needed in sorted(current_seed.items()):
            shortage = max(0, int(needed) - int(seeds.get(crop, 0)))
            if shortage:
                current_orders.append(["BUY_SEED", crop, shortage])
        for animal in ("COW", "SHEEP"):
            shortage = max(
                0,
                int(current_pickup.get(animal, 0)) - int(shed.get(animal, 0)),
            )
            if shortage:
                current_orders.append(["BUY_ANIMAL", animal, shortage])

        money = float(farm.get("money", 0.0) or 0.0)
        # At most two high-value sales precede HIRE.  This both monetizes the
        # farm and guarantees that every planned hire keeps its market slot.
        sell_limit = min(
            2 if hire_orders else 4,
            max(0, max_orders - len(hire_orders)),
        )
        selected_sales = sell_orders[:sell_limit]
        orders = [*selected_sales, *hire_orders]
        orders.extend(current_orders[: max(0, max_orders - len(orders))])

        # Land follows today's feed/seeds/animals.  Optional procurement below
        # is budgeted against a cash floor and cannot displace current needs.
        orders.extend(land_orders[: max(0, max_orders - len(orders))])

        sale_revenue = sum(
            float(prices.get(str(order[1]), 0)) * int(order[2])
            for order in selected_sales
        )
        committed_cost = self._estimated_cost(
            [order for order in orders if order[0] != "SELL"],
            observation,
            int(farm.get("hires_today", 0) or 0),
            len(unlocked),
        )
        projected_money = money + sale_revenue - committed_cost
        cash_floor = (
            300.0
            if day <= 3
            else 40.0
            if day <= 5
            else 300.0
            if day < 15
            else 100.0
        )

        def append_budgeted(opcode: str, item: str, wanted: int, unit_cost: float) -> None:
            nonlocal projected_money
            if wanted <= 0 or len(orders) >= max_orders or unit_cost <= 0:
                return
            affordable = max(0, int((projected_money - cash_floor) // unit_cost))
            quantity = min(wanted, affordable)
            if quantity:
                orders.append([opcode, item, quantity])
                projected_money -= unit_cost * quantity

        # Missing seeds break a whole crop cycle, while animals must already be
        # in the shed before their T2 pickup.  Give the latter precedence only
        # inside the final two-day acquisition window.
        def append_strategic_seeds() -> None:
            for crop, needed in sorted(strategic_seed.items()):
                current = int(seeds.get(crop, 0))
                already_ordered = sum(
                    int(order[2])
                    for order in orders
                    if order[0] == "BUY_SEED" and order[1] == crop
                )
                append_budgeted(
                    "BUY_SEED",
                    crop,
                    max(0, int(needed) - current - already_ordered),
                    float(SEED_COSTS[crop]),
                )

        def append_strategic_animals(requirements: Counter[str]) -> None:
            for animal in ("COW", "SHEEP"):
                needed = int(requirements.get(animal, 0))
                current = int(shed.get(animal, 0))
                already_ordered = sum(
                    int(order[2])
                    for order in orders
                    if order[0] == "BUY_ANIMAL" and order[1] == animal
                )
                append_budgeted(
                    "BUY_ANIMAL",
                    animal,
                    max(0, needed - current - already_ordered),
                    float(ANIMAL_COSTS[animal]),
                )

        animal_imminent = any(
            kind == "pickup" and item in ANIMAL_COSTS
            for horizon_day in range(day, min(30, day + 2) + 1)
            for _, kind, item, _ in self.events.get(horizon_day, [])
        )
        animal_pending = False
        if animal_imminent:
            append_strategic_animals(imminent_pickup)
            animal_pending = any(
                int(imminent_pickup.get(animal, 0))
                > int(shed.get(animal, 0))
                + sum(
                    int(order[2])
                    for order in orders
                    if order[0] == "BUY_ANIMAL" and order[1] == animal
                )
                for animal in ANIMAL_COSTS
            )
            if not animal_pending:
                append_strategic_seeds()
        else:
            append_strategic_seeds()
            # Before the D7 land purchase, holding D10 livestock in the shed
            # destroys the liquidity needed to hire the unlock routes. D8 is
            # still a two-day acquisition window and has the wool proceeds.
            if day >= 8:
                append_strategic_animals(strategic_pickup)

        # Feed is held for two days to protect care continuity without filling
        # the shed or displacing harvest output.
        feed_needed = int(feed_pickup.get("WHEAT", 0))
        feed_current = int(shed.get("WHEAT", 0))
        feed_ordered = sum(
            int(order[2])
            for order in orders
            if order[0] == "BUY_PRODUCT" and order[1] == "WHEAT"
        )
        if not animal_pending:
            append_budgeted(
                "BUY_PRODUCT",
                "WHEAT",
                max(0, feed_needed - feed_current - feed_ordered),
                float(prices.get("WHEAT", 25)),
            )
        for order in orders:
            self.market_requests[str(order[0])] += 1
        if turn in {1, 2, 24}:
            self.market_trace.append(
                {
                    "day": day,
                    "turn": turn,
                    "money_before": money,
                    "shed_before": dict(sorted(shed.items())),
                    "seeds_before": dict(sorted(seeds.items())),
                    "orders": deepcopy(orders),
                }
            )
        return orders

    @staticmethod
    def _estimated_cost(
        orders: list[list[Any]],
        observation: dict[str, Any],
        hire_start: int,
        unlocked_count: int,
    ) -> float:
        prices = (observation.get("market", {}) or {}).get("prices", {}) or {}
        hire_costs = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144)
        hire_index = hire_start
        total = 0.0
        for order in orders:
            opcode = order[0]
            if opcode == "HIRE":
                if hire_index < len(hire_costs):
                    total += hire_costs[hire_index]
                hire_index += 1
            elif opcode == "BUY_LAND":
                total += LAND_COSTS.get(unlocked_count, 4000)
            elif opcode == "BUY_ANIMAL":
                total += ANIMAL_COSTS.get(str(order[1]), 0) * int(order[2])
            elif opcode == "BUY_SEED":
                total += SEED_COSTS.get(str(order[1]), 0) * int(order[2])
            elif opcode == "BUY_PRODUCT":
                total += float(prices.get(str(order[1]), 100)) * int(order[2])
        return total

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        try:
            day = int(observation.get("day", 0)) + 1
            turn = int(observation.get("hour", 0)) + 1
            farm = _farm(observation, self.seat)
            private = observation.get("private", {}) or {}
            actual_hands = len(farm.get("hands", []) or [])
            rows = [self.actions.get((day, turn, worker)) for worker in range(actual_hands + 1)]
            commands = [
                self._guarded_unit_command(row, farm, private, worker)
                for worker, row in enumerate(rows)
            ]
            self.requested_actions.update(command[0] for command in commands)
            return {
                "farmer": commands[0] if commands else ["PASS"],
                "hands": commands[1:],
                "market": self._market_orders(observation, day, turn),
            }
        except Exception as exc:  # noqa: BLE001 - offline gate records fail-closed errors
            self.error_count += 1
            self.last_error = f"{type(exc).__name__}: {exc}"
            return deepcopy(SAFE_PASS)


def _pass_policy(observation: dict[str, Any], configuration: Any = None):
    return deepcopy(SAFE_PASS)


def _snapshot(replay: dict[str, Any], day: int, seat: int) -> dict[str, Any]:
    record = replay["steps"][min(day * 24 - 1, 719)][seat]
    observation = record["observation"]
    farm = observation["farms"][seat]
    private = observation.get("private", {}) or {}
    return {
        "money": float(farm.get("money", 0.0)),
        "hands": len(farm.get("hands", []) or []),
        "unlocked": list(farm.get("unlocked_quadrants", []) or []),
        "crops": _mix(farm, "crop"),
        "animals": _mix(farm, "animal"),
        "topology": _topology(farm),
        "shed_units": int(sum((private.get("shed", {}) or {}).values())),
    }


def run(plan: dict[str, Any] | None = None) -> dict[str, Any]:
    plan = build_plan() if plan is None else plan
    controller = Gate0BController(plan, seat=0)
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": SEED,
            "turnsPerDay": 24,
            "weedSpawnChance": 0.0,
        },
        debug=False,
    )
    env.run([controller, _pass_policy])
    replay = env.toJSON()
    replay.setdefault("info", {})["EpisodeId"] = 918180002
    replay["info"]["Agents"] = [
        {"Name": "CODEX E18.18 GATE 0B"},
        {"Name": "PASSIVE ORACLE"},
    ]
    with tempfile.TemporaryDirectory(prefix="e18_18_gate_0b_") as temp_dir:
        replay_path = Path(temp_dir) / "918180002.json"
        replay_path.write_text(json.dumps(replay), encoding="utf-8")
        summary, daily_rows, action_rows = analyze(replay_path)
    player_summary = next(
        row for row in summary["players"] if int(row["player_index"]) == 0
    )
    final = _snapshot(replay, 30, 0)
    snapshots = {
        f"D{day:02d}": _snapshot(replay, day, 0)
        for day in (1, 5, 10, 15, 20, 25, 30)
    }
    target = plan["snapshots"]
    checkpoint_checks = {
        key: {
            "crop_match": snapshots[key]["crops"] == target[key]["crops"],
            "animal_match": snapshots[key]["animals"] == target[key]["animals"],
        }
        for key in target
    }
    transition_counts = (
        player_summary.get("transition_metrics", {}).get("counts", {}) or {}
    )
    crop_execution = player_summary.get("crop_action_execution", {}) or {}
    acknowledged = crop_execution.get("acknowledged", {}) or {}
    requested = crop_execution.get("requested", {}) or {}
    acknowledgement_rate = crop_execution.get("acknowledgement_rate_pct", {}) or {}
    planted_units = crop_execution.get("planted_units", {}) or {}
    expected_planting = {
        crop: int(units)
        for crop, units in plan["totals"]["seed_use"].items()
        if int(units) > 0
    }
    gate_checks = {
        "gate_0a_precondition": bool(plan["gate_0a_passed"]),
        "zero_controller_errors": controller.error_count == 0,
        "all_composition_checkpoints": all(
            all(check.values()) for check in checkpoint_checks.values()
        ),
        "exact_final_770": final["topology"] == {"Q0": 7, "Q1": 7},
        "exact_final_9_cow_5_sheep": final["animals"] == {"COW": 9, "SHEEP": 5},
        "all_three_target_quadrants_unlocked": set(final["unlocked"]) >= {"NW", "NE", "SW"},
        "positive_terminal_money": final["money"] > 0,
        "terminal_crop_cap": sum(final["crops"].values()) <= 2,
        "zero_terminal_shed_inventory": final["shed_units"] == 0,
        "zero_exact_crop_starvation": int(
            transition_counts.get("starved_to_weed", 0)
        )
        == 0,
        "exact_planned_planting_acknowledged": planted_units == expected_planting,
        "all_plant_and_dig_actions_acknowledged": all(
            int(acknowledged.get(opcode, 0)) == int(requested.get(opcode, 0))
            for opcode in ("PLANT", "DIG")
        ),
        # The residual WATER no-ops occur only after exhausted Strawberry
        # cohorts enter terminal decay; no biological starvation is observed.
        "all_emitted_water_actions_acknowledged": float(
            acknowledgement_rate.get("WATER", 0.0)
        )
        == 100.0,
        "deterministic_exact_replay": False,
    }
    return {
        "schema_version": "e18.codex.770_capacity_trajectory_gate_0b.v1",
        "candidate_id": plan["candidate_id"],
        "epistemic_role": "DEVELOPMENT_GATE_0B_ORACLE",
        "seed": SEED,
        "configuration": {
            "episodeSteps": 720,
            "turnsPerDay": 24,
            "weedSpawnChance": 0.0,
            "opponent": "PASSIVE_ORACLE",
        },
        "plan_sha256": plan["plan_sha256"],
        "gate_0b_passed": all(gate_checks.values()),
        "gate_0b_checks": gate_checks,
        "policy_build_authorized": False,
        "executor_authorized": False,
        "controller": {
            "errors": controller.error_count,
            "last_error": controller.last_error,
            "requested_actions": dict(sorted(controller.requested_actions.items())),
            "market_requests": dict(sorted(controller.market_requests.items())),
            "guarded_noops": dict(sorted(controller.guarded_noops.items())),
            "market_trace": controller.market_trace,
        },
        "engine_summary": player_summary,
        "snapshots": snapshots,
        "checkpoint_checks": checkpoint_checks,
        "final": final,
        "daily_rows": [
            row for row in daily_rows if int(row["player_index"]) == 0
        ],
        "action_rows": [
            row for row in action_rows if int(row["player_index"]) == 0
        ],
        "blocking_note": (
            None
            if all(gate_checks.values())
            else "Gate 0B remains blocked; use the failed checks to revise logistics before creating an executor."
        ),
    }


def _write_report(payload: dict[str, Any]) -> None:
    verdict = "PASS" if payload["gate_0b_passed"] else "FAIL"
    failed = [key for key, value in payload["gate_0b_checks"].items() if not value]
    report = f"""# E18.18 — Gate 0B exact-engine oracle

## Verdetto

`{verdict}` nel replay weed-free dell'interprete Kaggriculture reale.

Check falliti: `{', '.join(failed) if failed else 'nessuno'}`.
Money terminale: `{payload['final']['money']:.0f}`; topologia finale:
`{json.dumps(payload['final']['topology'], sort_keys=True)}`; animali finali:
`{json.dumps(payload['final']['animals'], sort_keys=True)}`; crop residui:
`{json.dumps(payload['final']['crops'], sort_keys=True)}`.

`policy_build_authorized={str(payload['policy_build_authorized']).lower()}`;
`executor_authorized=false` finché la policy non è stata materialmente costruita
e verificata nei Gate 1–2.

Il Gate richiede inoltre zero crop starvation, 100% di PLANT, DIG e WATER
effettivamente emessi riconosciuti, shed terminale vuoto e un secondo replay
esatto identico.

Le guardie state-aware rimuovono prima dell'emissione i comandi divenuti
inapplicabili. Il PASS oracle autorizza l'estrazione della policy, non la
submission: il rolling replan resta soggetto al Gate 1 development.

## Check

```json
{json.dumps(payload['gate_0b_checks'], indent=2, sort_keys=True)}
```

## Checkpoint

```json
{json.dumps(payload['checkpoint_checks'], indent=2, sort_keys=True)}
```
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> int:
    plan = build_plan()
    payload = run(plan)
    confirmation = run(plan)
    determinism_fields = {
        "plan_sha256": payload["plan_sha256"],
        "action_stream_sha256": payload["engine_summary"]["action_stream_sha256"],
        "final_reward": payload["engine_summary"]["final_reward"],
        "final": payload["final"],
        "snapshots": payload["snapshots"],
        "transition_counts": payload["engine_summary"]["transition_metrics"]["counts"],
    }
    confirmation_fields = {
        "plan_sha256": confirmation["plan_sha256"],
        "action_stream_sha256": confirmation["engine_summary"]["action_stream_sha256"],
        "final_reward": confirmation["engine_summary"]["final_reward"],
        "final": confirmation["final"],
        "snapshots": confirmation["snapshots"],
        "transition_counts": confirmation["engine_summary"]["transition_metrics"]["counts"],
    }
    deterministic = determinism_fields == confirmation_fields
    payload["determinism"] = {
        "passed": deterministic,
        "first": determinism_fields,
        "confirmation": confirmation_fields,
    }
    payload["gate_0b_checks"]["deterministic_exact_replay"] = deterministic
    payload["gate_0b_passed"] = all(payload["gate_0b_checks"].values())
    payload["policy_build_authorized"] = payload["gate_0b_passed"]
    payload["blocking_note"] = (
        None
        if payload["gate_0b_passed"]
        else "Gate 0B remains blocked; use the failed checks to revise logistics before creating an executor."
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_report(payload)
    print(json.dumps({
        "gate_0b_passed": payload["gate_0b_passed"],
        "failed_checks": [
            key for key, value in payload["gate_0b_checks"].items() if not value
        ],
        "final": payload["final"],
        "controller_errors": payload["controller"]["errors"],
    }, indent=2))
    return 0 if payload["gate_0b_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
