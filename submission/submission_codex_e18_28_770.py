"""E18.28 C: fixed 770, full-season Carrot. Daily external diagnostic; not incumbent promotion."""

from __future__ import annotations

import base64
import json
import zlib
from collections import Counter, defaultdict
from copy import deepcopy
from typing import Any

SHED_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))

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

MOVES: dict[str, tuple[int, int]] = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0),
}

class RetryingTrajectoryController(Gate0BController):
    """Execute the E18.18 plan as recoverable, state-aware worker queues."""

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.routes: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
        for row in plan["trajectory"]:
            self.routes[(int(row["day"]), int(row["worker"]))].append(row)
        for rows in self.routes.values():
            rows.sort(key=lambda row: (int(row["turn"]), int(row["step"])))
        self.cursors: dict[tuple[int, int], int] = defaultdict(int)
        self.pickup_remaining: dict[tuple[int, int, int], int] = {}
        self.wait_counts: Counter[tuple[int, int, int, str]] = Counter()
        self.recovery_actions: Counter[str] = Counter()
        self.deferred_critical: Counter[str] = Counter()
        self.skipped_stale: Counter[str] = Counter()
        self.unfinished_by_day: dict[int, int] = {}
        self._last_day = 0

    @staticmethod
    def _inventory(private: dict[str, Any], worker: int) -> Counter[str]:
        inventories = private.get("inventories", []) or []
        if worker >= len(inventories):
            return Counter()
        return Counter(inventories[worker] or {})

    @staticmethod
    def _position(farm: dict[str, Any], worker: int) -> tuple[int, int] | None:
        positions = [farm.get("farmer", [4, 4]), *(farm.get("hands", []) or [])]
        if worker >= len(positions):
            return None
        return tuple(int(value) for value in positions[worker])

    @staticmethod
    def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
        x, y = position
        rows = farm.get("tiles", []) or []
        if not 0 <= y < len(rows) or not 0 <= x < len(rows[y]):
            return "LOCKED"
        return rows[y][x]

    @staticmethod
    def _move_toward(
        position: tuple[int, int], target: tuple[int, int]
    ) -> tuple[list[str], bool]:
        x, y = position
        tx, ty = target
        if x < tx:
            return ["EAST"], x + 1 == tx and y == ty
        if x > tx:
            return ["WEST"], x - 1 == tx and y == ty
        if y < ty:
            return ["SOUTH"], x == tx and y + 1 == ty
        if y > ty:
            return ["NORTH"], x == tx and y - 1 == ty
        return ["PASS"], True

    def _advance(self, key: tuple[int, int]) -> None:
        self.cursors[key] += 1

    def _bounded_defer(
        self,
        key: tuple[int, int],
        opcode: str,
        *,
        max_waits: int = 1,
    ) -> None:
        wait_key = (*key, self.cursors[key], opcode)
        if self.wait_counts[wait_key] < max_waits:
            self.wait_counts[wait_key] += 1
            self.deferred_critical[opcode] += 1
            return
        self.skipped_stale[opcode] += 1
        self._advance(key)

    def _remaining(
        self,
        day: int,
        turn: int,
        requirement_kind: str,
        *,
        include_tomorrow: bool,
    ) -> Counter[str]:
        del turn
        needed = self._pending_requirements(day, requirement_kind)
        if include_tomorrow:
            needed.update(
                self.requirements.get(day + 1, {}).get(requirement_kind, {})
            )
        return needed

    def _remaining_horizon(
        self,
        day: int,
        turn: int,
        requirement_kind: str,
        *,
        horizon_days: int,
    ) -> Counter[str]:
        del turn
        needed = self._pending_requirements(day, requirement_kind)
        for horizon_day in range(day + 1, min(30, day + horizon_days) + 1):
            needed.update(
                self.requirements.get(horizon_day, {}).get(requirement_kind, {})
            )
        return needed

    def _pending_requirements(
        self, day: int, requirement_kind: str
    ) -> Counter[str]:
        opcode = "PICKUP" if requirement_kind == "pickup" else "PLANT"
        argument = "item" if opcode == "PICKUP" else "crop"
        needed: Counter[str] = Counter()
        for key, rows in self.routes.items():
            if key[0] != day:
                continue
            for index, row in enumerate(
                rows[self.cursors[key] :], start=self.cursors[key]
            ):
                if row["opcode"] != opcode:
                    continue
                args = row.get("arguments", {}) or {}
                units = int(args.get("units", 1))
                if opcode == "PICKUP":
                    units = self.pickup_remaining.get((*key, index), units)
                needed[str(args[argument])] += units
        return needed

    def _planned_or_recovery(
        self,
        row: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        worker: int,
        key: tuple[int, int],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        opcode = str(row["opcode"])
        position = self._position(farm, worker)
        if position is None:
            return ["PASS"], None
        target = tuple(int(value) for value in row.get("position", position))

        if opcode in MOVES:
            if position == target:
                self._advance(key)
                return ["PASS"], None
            command, reaches_target = self._move_toward(position, target)
            if reaches_target:
                self._advance(key)
            index = self.cursors[key] - int(reaches_target)
            expected_origin = (
                tuple(self.routes[key][index - 1]["position"])
                if index > 0
                else (4, 4)
            )
            metric = (
                "PLANNED_MOVE"
                if position == expected_origin
                else "POSITION_CORRECTION"
            )
            self.recovery_actions[metric] += 1
            return command, None

        if position != target:
            command, _ = self._move_toward(position, target)
            self.recovery_actions["POSITION_CORRECTION"] += 1
            return command, None

        command = self._unit_command(row)
        args = row.get("arguments", {}) or {}
        inventory = self._inventory(private, worker)
        shed = Counter(private.get("shed", {}) or {})
        tile = self._tile(farm, position)

        if opcode == "PICKUP":
            item = str(args["item"])
            pickup_key = (*key, self.cursors[key])
            units = self.pickup_remaining.get(
                pickup_key, int(args.get("units", 1))
            )
            available = int(shed.get(item, 0))
            if available <= 0 and item == "FERTILIZER":
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
            if available <= 0:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
            picked = min(units, available)
            command = ["PICKUP", item, picked]
            if picked < units and item != "FERTILIZER":
                self.pickup_remaining[pickup_key] = units - picked
                self.recovery_actions["PARTIAL_PICKUP"] += 1
                return command, row
            self.pickup_remaining.pop(pickup_key, None)
        elif opcode == "PLANT":
            crop = str(args["crop"])
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                self.recovery_actions["DIG_BEFORE_PLANT"] += 1
                return ["DIG"], None
            if tile is not None or int(
                (private.get("seeds", {}) or {}).get(crop, 0)
            ) <= 0:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
        elif opcode == "BUILD_PASTURE":
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                self.recovery_actions["DIG_BEFORE_BUILD"] += 1
                return ["DIG"], None
            if tile is not None:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
        elif opcode == "PLACE":
            animal = str(args["animal"])
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                self.recovery_actions["DIG_BEFORE_PLACE"] += 1
                return ["DIG"], None
            if tile is None:
                self.recovery_actions["BUILD_BEFORE_PLACE"] += 1
                return ["BUILD_PASTURE"], None
            valid_pasture = (
                isinstance(tile, dict)
                and tile.get("kind") == "PASTURE"
                and "animal" not in tile
            )
            if not valid_pasture or int(inventory.get(animal, 0)) <= 0:
                self._bounded_defer(key, opcode)
                return ["PASS"], None
        elif opcode == "FEED":
            if not isinstance(tile, dict) or "animal" not in tile:
                self._bounded_defer(key, opcode, max_waits=0)
                return ["PASS"], None
            if bool(tile.get("fed_today")):
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
            if int(inventory.get("WHEAT", 0)) <= 0:
                # Wheat in the shed cannot reach a worker already at pasture
                # without abandoning the route.  Skip this feed instead of
                # deadlocking all later animals in the same daily mission.
                self._bounded_defer(key, opcode, max_waits=0)
                return ["PASS"], None
        elif opcode == "WATER":
            valid = (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and not bool(tile.get("watered_today"))
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "HARVEST":
            if not isinstance(tile, dict) or int(tile.get("yield_units", 0)) <= 0:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "FERTILIZE":
            valid = (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and int(inventory.get("FERTILIZER", 0)) > 0
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "DIG":
            valid = tile is not None and not (
                isinstance(tile, dict) and "animal" in tile
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "CARE":
            valid = (
                isinstance(tile, dict)
                and "animal" in tile
                and not bool(tile.get("cared_today"))
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "COLLECT_FERTILIZER":
            valid = (
                isinstance(tile, dict)
                and "animal" in tile
                and bool(tile.get("fertilizer_available"))
            )
            if not valid:
                self.skipped_stale[opcode] += 1
                self._advance(key)
                return ["PASS"], None
        elif opcode == "DROP" and not any(inventory.values()):
            self.skipped_stale[opcode] += 1
            self._advance(key)
            return ["PASS"], None

        self._advance(key)
        return command, row

    def _worker_command(
        self,
        day: int,
        turn: int,
        worker: int,
        farm: dict[str, Any],
        private: dict[str, Any],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        key = (day, worker)
        rows = self.routes.get(key, [])
        while self.cursors[key] < len(rows):
            row = rows[self.cursors[key]]
            if int(row["turn"]) > turn:
                return ["PASS"], None
            if row["opcode"] == "PASS":
                self._advance(key)
                continue
            command, emitted_row = self._planned_or_recovery(
                row, farm, private, worker, key
            )
            if (
                command[0] == "PASS"
                and self.cursors[key] < len(rows)
                and rows[self.cursors[key]] is not row
            ):
                # A stale optional action advances the cursor and can expose a
                # second already-due task in the same engine turn.  A critical
                # deferred task leaves the cursor unchanged and must wait.
                continue
            return command, emitted_row
        return ["PASS"], None

    def _record_finished_day(self, day: int) -> None:
        if day <= 0 or day in self.unfinished_by_day:
            return
        unfinished = 0
        for key, rows in self.routes.items():
            if key[0] == day:
                unfinished += len(rows) - self.cursors[key]
        self.unfinished_by_day[day] = unfinished

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: Any = None,
    ) -> dict[str, Any]:
        del configuration
        try:
            day = int(observation.get("day", 0)) + 1
            turn = int(observation.get("hour", 0)) + 1
            if day != self._last_day:
                self._record_finished_day(self._last_day)
                self._last_day = day
            farm = _farm(observation, self.seat)
            private = observation.get("private", {}) or {}
            actual_hands = len(farm.get("hands", []) or [])
            selected = [
                self._worker_command(day, turn, worker, farm, private)
                for worker in range(actual_hands + 1)
            ]
            commands = [command for command, _ in selected]
            self.requested_actions.update(command[0] for command in commands)

            # Gate0B's market bridge counts same-batch planned drops.  Expose
            # only drops that this retrying executor actually emits now, then
            # restore the immutable static lookup immediately afterwards.
            marker = object()
            prior: dict[tuple[int, int, int], object] = {}
            for worker, (command, row) in enumerate(selected):
                lookup = (day, turn, worker)
                prior[lookup] = self.actions.get(lookup, marker)
                if command[0] == "DROP" and row is not None:
                    self.actions[lookup] = row
                else:
                    self.actions.pop(lookup, None)
            try:
                market = self._market_orders(observation, day, turn)
            finally:
                for lookup, value in prior.items():
                    if value is marker:
                        self.actions.pop(lookup, None)
                    else:
                        self.actions[lookup] = value  # type: ignore[assignment]

            return {
                "farmer": commands[0] if commands else ["PASS"],
                "hands": commands[1:],
                "market": market,
            }
        except Exception as exc:  # noqa: BLE001 - fail closed and report at Gate-1
            self.error_count += 1
            self.last_error = f"{type(exc).__name__}: {exc}"
            return deepcopy(SAFE_PASS)

    def finalize_metrics(self) -> None:
        self._record_finished_day(self._last_day)

class WheatMarketNettingController(RetryingTrajectoryController):
    """Net simultaneous Wheat sales and purchases before market execution."""

    activation_day = 11
    align_sale_and_buy_horizons = False
    net_same_batch_round_trips = True

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.wheat_market_adjustments: Counter[str] = Counter()

    @staticmethod
    def _net_wheat_orders(
        orders: list[list[Any]],
        extra_reserve: int,
        *,
        net_round_trips: bool = True,
    ) -> tuple[list[list[Any]], dict[str, int]]:
        adjusted = [list(order) for order in orders]
        reserve_left = max(0, int(extra_reserve))
        reserved = 0
        for order in adjusted:
            if order[:2] != ["SELL", "WHEAT"]:
                continue
            reduction = min(reserve_left, int(order[2]))
            order[2] = int(order[2]) - reduction
            reserve_left -= reduction
            reserved += reduction

        sell_total = sum(
            int(order[2])
            for order in adjusted
            if order[:2] == ["SELL", "WHEAT"]
        )
        buy_total = sum(
            int(order[2])
            for order in adjusted
            if order[:2] == ["BUY_PRODUCT", "WHEAT"]
        )
        canceled = min(sell_total, buy_total) if net_round_trips else 0
        sell_remaining = sell_total - canceled
        buy_remaining = buy_total - canceled
        output: list[list[Any]] = []
        for order in adjusted:
            if order[:2] == ["SELL", "WHEAT"]:
                quantity = min(int(order[2]), sell_remaining)
                sell_remaining -= quantity
                if quantity:
                    output.append(["SELL", "WHEAT", quantity])
            elif order[:2] == ["BUY_PRODUCT", "WHEAT"]:
                quantity = min(int(order[2]), buy_remaining)
                buy_remaining -= quantity
                if quantity:
                    output.append(["BUY_PRODUCT", "WHEAT", quantity])
            else:
                output.append(order)
        return output, {
            "reserved_sell_units": reserved,
            "netted_round_trip_units": canceled,
        }

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        orders = super()._market_orders(observation, day, turn)
        if day < self.activation_day:
            return orders

        tomorrow = self._remaining(
            day, turn, "pickup", include_tomorrow=True
        )
        buy_horizon = self._remaining_horizon(
            day, turn, "pickup", horizon_days=2
        )
        extra_reserve = (
            max(
                0,
                int(buy_horizon.get("WHEAT", 0))
                - int(tomorrow.get("WHEAT", 0)),
            )
            if self.align_sale_and_buy_horizons
            else 0
        )
        adjusted, metrics = self._net_wheat_orders(
            orders,
            extra_reserve,
            net_round_trips=self.net_same_batch_round_trips,
        )
        self.wheat_market_adjustments.update(metrics)
        if adjusted != orders:
            self.wheat_market_adjustments["adjusted_turns"] += 1
        return adjusted

class WheatObligationLedgerController(WheatMarketNettingController):
    """Protect in-flight and source-tagged Wheat without changing the route."""

    activation_day = 11
    procurement_horizon_days = 2
    protect_inflight_pickups = True
    protect_procurement_contracts = False

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.inflight_wheat: dict[tuple[int, int], Counter[int]] = defaultdict(
            Counter
        )
        self.wheat_contracts: Counter[tuple[int, int]] = Counter()
        self.wheat_ledger_metrics: Counter[str] = Counter()
        self.wheat_ledger_trace: list[dict[str, Any]] = []

    def _worker_command(
        self,
        day: int,
        turn: int,
        worker: int,
        farm: dict[str, Any],
        private: dict[str, Any],
    ) -> tuple[list[Any], dict[str, Any] | None]:
        command, row = super()._worker_command(
            day, turn, worker, farm, private
        )
        if command[:2] == ["PICKUP", "WHEAT"]:
            self.inflight_wheat[(day, turn)][worker] += int(command[2])
        return command, row

    def _worker_pickup_obligations(
        self,
        day: int,
        turn: int,
        due_day: int,
    ) -> Counter[int]:
        """Return remaining Wheat pickup units keyed by assigned worker."""
        obligations: Counter[int] = Counter()
        for (route_day, worker), rows in self.routes.items():
            if route_day != due_day:
                continue
            start = self.cursors[(route_day, worker)] if due_day == day else 0
            for index, row in enumerate(rows[start:], start=start):
                if row["opcode"] != "PICKUP":
                    continue
                args = row.get("arguments", {}) or {}
                if args.get("item") != "WHEAT":
                    continue
                if due_day == day and int(row["turn"]) < turn:
                    continue
                units = self.pickup_remaining.get(
                    (route_day, worker, index), int(args.get("units", 1))
                )
                obligations[worker] += units
        if due_day == day:
            obligations.update(self.inflight_wheat.get((day, turn), {}))
        return obligations

    def _release_near_contracts(self, day: int) -> int:
        """Release contracts once the parent's D+1 reserve covers them."""
        released = 0
        for key in list(self.wheat_contracts):
            if key[0] <= day + 1:
                released += int(self.wheat_contracts.pop(key))
        return released

    def _cap_contracts_to_shed(self, shed_wheat: int) -> int:
        """Reconcile nominal contracts with Wheat physically in the shed."""
        available = max(0, int(shed_wheat))
        removed = 0
        for key in sorted(self.wheat_contracts):
            units = int(self.wheat_contracts[key])
            kept = min(units, available)
            available -= kept
            removed += units - kept
            if kept:
                self.wheat_contracts[key] = kept
            else:
                del self.wheat_contracts[key]
        return removed

    @staticmethod
    def _reduce_wheat_sales(
        orders: list[list[Any]], reserve: int
    ) -> tuple[list[list[Any]], int]:
        """Remove up to ``reserve`` units from Wheat sales, preserving order."""
        left = max(0, int(reserve))
        protected = 0
        adjusted: list[list[Any]] = []
        for order in orders:
            if order[:2] != ["SELL", "WHEAT"]:
                adjusted.append(list(order))
                continue
            reduction = min(left, int(order[2]))
            quantity = int(order[2]) - reduction
            left -= reduction
            protected += reduction
            if quantity:
                adjusted.append(["SELL", "WHEAT", quantity])
        return adjusted, protected

    @staticmethod
    def _wheat_order_units(orders: list[list[Any]], opcode: str) -> int:
        return sum(
            int(order[2])
            for order in orders
            if order[:2] == [opcode, "WHEAT"]
        )

    def _allocate_contracts(
        self,
        due_day: int,
        obligations: Counter[int],
        units: int,
    ) -> int:
        """Assign newly requested Wheat to concrete worker obligations."""
        left = max(0, int(units))
        allocated = 0
        for worker in sorted(obligations):
            key = (due_day, worker)
            room = max(
                0,
                int(obligations[worker]) - int(self.wheat_contracts[key]),
            )
            quantity = min(left, room)
            if quantity:
                self.wheat_contracts[key] += quantity
                allocated += quantity
                left -= quantity
            if left <= 0:
                break
        return allocated

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        orders = super()._market_orders(observation, day, turn)
        if day < self.activation_day:
            return orders

        private = observation.get("private", {}) or {}
        shed_wheat = int((private.get("shed", {}) or {}).get("WHEAT", 0))
        released = self._release_near_contracts(day)
        reconciled = self._cap_contracts_to_shed(shed_wheat)
        inflight_by_worker = self.inflight_wheat.get((day, turn), Counter())
        inflight = sum(inflight_by_worker.values())
        contracted = sum(self.wheat_contracts.values())
        reserve = (
            inflight if self.protect_inflight_pickups else 0
        ) + (contracted if self.protect_procurement_contracts else 0)
        adjusted, protected = self._reduce_wheat_sales(orders, reserve)

        due_day = min(30, day + self.procurement_horizon_days)
        due_obligations = self._worker_pickup_obligations(
            day, turn, due_day
        )
        pending_near = self._worker_pickup_obligations(day, turn, day)
        pending_near.update(
            self._worker_pickup_obligations(day, turn, min(30, day + 1))
        )
        near_shortage = max(0, sum(pending_near.values()) - shed_wheat)
        bought = self._wheat_order_units(adjusted, "BUY_PRODUCT")
        contractable = max(0, bought - near_shortage)
        allocated = 0
        if self.protect_procurement_contracts and due_day > day + 1:
            allocated = self._allocate_contracts(
                due_day, due_obligations, contractable
            )

        self.wheat_ledger_metrics.update(
            {
                "inflight_pickup_units": inflight,
                "protected_sale_units": protected,
                "contract_allocated_units": allocated,
                "contract_released_units": released,
                "contract_reconciled_units": reconciled,
            }
        )
        if adjusted != orders:
            self.wheat_ledger_metrics["adjusted_turns"] += 1
        if turn in {1, 2, 24} or inflight or protected or allocated:
            self.wheat_ledger_trace.append(
                {
                    "day": day,
                    "turn": turn,
                    "shed_wheat": shed_wheat,
                    "inflight_by_worker": dict(sorted(inflight_by_worker.items())),
                    "pending_near_by_worker": dict(sorted(pending_near.items())),
                    "due_day": due_day,
                    "due_by_worker": dict(sorted(due_obligations.items())),
                    "contracts": {
                        f"D{contract_day}:W{worker}": units
                        for (contract_day, worker), units in sorted(
                            self.wheat_contracts.items()
                        )
                    },
                    "orders_before_ledger": orders,
                    "orders_after_ledger": adjusted,
                }
            )
        return adjusted

class WheatJitD1Controller(WheatObligationLedgerController):
    """Buy Wheat only for worker obligations due no later than tomorrow."""

    activation_day = 11
    procurement_horizon_days = 1

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.wheat_jit_metrics: Counter[str] = Counter()

    @staticmethod
    def _cap_wheat_buys(
        orders: list[list[Any]], cap: int
    ) -> tuple[list[list[Any]], int]:
        """Cap aggregate Wheat buys while preserving all unrelated orders."""
        left = max(0, int(cap))
        removed = 0
        adjusted: list[list[Any]] = []
        for order in orders:
            if order[:2] != ["BUY_PRODUCT", "WHEAT"]:
                adjusted.append(list(order))
                continue
            quantity = min(int(order[2]), left)
            removed += int(order[2]) - quantity
            left -= quantity
            if quantity:
                adjusted.append(["BUY_PRODUCT", "WHEAT", quantity])
        return adjusted, removed

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        orders = super()._market_orders(observation, day, turn)
        if day < self.activation_day:
            return orders

        private = observation.get("private", {}) or {}
        shed_wheat = int((private.get("shed", {}) or {}).get("WHEAT", 0))
        near_by_worker = self._worker_pickup_obligations(day, turn, day)
        if day < 30:
            near_by_worker.update(
                self._worker_pickup_obligations(day, turn, day + 1)
            )
        near_required = sum(near_by_worker.values())
        buy_cap = max(0, near_required - shed_wheat)
        adjusted, removed = self._cap_wheat_buys(orders, buy_cap)
        requested = self._wheat_order_units(orders, "BUY_PRODUCT")
        retained = self._wheat_order_units(adjusted, "BUY_PRODUCT")
        self.wheat_jit_metrics.update(
            {
                "nominal_buy_units": requested,
                "retained_buy_units": retained,
                "removed_d2_buy_units": removed,
            }
        )
        if removed:
            self.wheat_jit_metrics["adjusted_turns"] += 1
        return adjusted

class JesseBoostD10Controller(WheatJitD1Controller):
    """E18.22 execution guards bound to the Jesse-shaped D1-D10 plan."""

    def __init__(self, plan: dict[str, Any], seat: int = 0) -> None:
        super().__init__(plan, seat=seat)
        self.skipped_bounded_by_day: defaultdict[int, Counter[str]] = defaultdict(
            Counter
        )

    def _bounded_defer(
        self,
        key: tuple[int, int],
        opcode: str,
        *,
        max_waits: int = 1,
    ) -> None:
        if key[0] == 13 and opcode == "PICKUP":
            # D13 feed is funded at T2 by the fertilizer bridge. The default
            # one-turn pickup wait expires immediately before that settlement.
            max_waits = max(max_waits, 2)
        skipped_before = int(self.skipped_stale[opcode])
        super()._bounded_defer(key, opcode, max_waits=max_waits)
        if int(self.skipped_stale[opcode]) > skipped_before:
            self.skipped_bounded_by_day[key[0]][opcode] += 1

    def _market_orders(
        self,
        observation: dict[str, Any],
        day: int,
        turn: int,
    ) -> list[list[Any]]:
        """Liquidate the D12 fertilizer bridge before the D13 payroll."""
        orders = super()._market_orders(observation, day, turn)
        private = observation.get("private", {}) or {}
        fertilizer = int((private.get("shed", {}) or {}).get("FERTILIZER", 0))
        bridged = orders
        if day == 12 and fertilizer > 0:
            # Monetize fertilizer already dropped by T21. The final D12 drop is
            # retained to finance the second D13 hire batch.
            remaining = [
                order for order in orders if order[:2] != ["SELL", "FERTILIZER"]
            ]
            bridged = [["SELL", "FERTILIZER", fertilizer], *remaining][:10]
        elif day == 13 and turn == 1:
            # Nine hires consume all but one market slot. Pre-stage the four
            # Wheat units needed by the first D13 pickup; the other nine are
            # bought with the second hire batch.
            hires = [order for order in orders if order[0] == "HIRE"][:9]
            bridged = [*hires, ["BUY_PRODUCT", "WHEAT", 4]][:10]
        elif day == 13 and turn == 2 and fertilizer > 0:
            remaining = [
                order for order in orders if order[:2] != ["SELL", "FERTILIZER"]
            ]
            bridged = [["SELL", "FERTILIZER", fertilizer], *remaining][:10]

        if (
            bridged is not orders
            and self.market_trace
            and self.market_trace[-1]["day"] == day
        ):
            self.market_trace[-1]["orders"] = [list(order) for order in bridged]
        return bridged

class D10D15CashflowController(JesseBoostD10Controller):
    """V1 is schedule-only; V2 acknowledges physically carried Melon drops."""

    def __init__(self, plan, seat=0):
        super().__init__(plan, seat=seat)
        self.opening_reference = None
        if plan.get("treatment_config", {}).get("freeze_opening_market_horizon"):
            self.opening_reference = JesseBoostD10Controller(
                deepcopy(_PARENT_26_PLAN), seat=seat
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
                else deepcopy(_PARENT_27_PLAN),
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

_PLAN = json.loads(zlib.decompress(base64.b85decode('c-qXpU(YW`m8JPze9cA1-^{E#7o2X;xC>;UQFm)pLV!lhQ~{zvGp&}t``Cr;a%P-dJD*&Urmm2%v?5RBFEXAtV(+#7_a}e(^RNH!-~Hw<fBf_R`s5$}$N&E1fBxlnfBNJf(holQ?XUmWzy0rD{`%)XeDV+Z2cP`EfBf_R^SeKP@(;@oKKbLHe)GrQ{_c~1_~d6l`QiWZ%b$JngHL|_=l|=k|N6T>{N;as@(=&}li&a4cmMk3fBfN3fA!^m`RgBk|JDDSzxcr?fBNJ9{QX~k|Hm)o{zv^m{Xf6>!8gO@^Kj+Ca6kX?hYvryIbb;tSRV}ds~>;(^cVj=U{wRw^MLK+1OC%bKmWy#Pvf0+%Xf6!S+{>&_aA@xlh1zi&p-S0=fC*n=O2K6KkKg-6ZP4rKRoMx^6NkR{$GFnFW<fzHO_h-XZ!d#|LMbrADxH!dj6Br-_H8`$Mt{sDVm=BESr{(>;CG)&wn9x%R%=mnUipGU+igwVTq?a>(!n{8di5I?#n%mFf8X(AHLp`@UU#t<8@npkiV-uEZo%n7kn6DSi0%a+WqP)F2@;`Zrc3Udl+F@ylH>@dJn?G^34~^_rs^b@~sEqJS^Xw{O|H%gmH(?bKdT0oMG|i;(wVBBMgf-*T>)H!`l@MlgOv}KC2}5#lK4=NH*W*4kVinvI;wp>~fG*w2_X#>3=%we)5|?|M5@XQkfb>vBu%yKmEmr&%x6x#z^F2a-3_)7|yI5htbHv=H;X;QRDD0`1I#LC&H2}9AOC*j<5s@M_BTNBP=n(5tiKG2uoaWge5K*!WtJGVMz&&u*3pKSki#=@&pZJwr#hYG?3Z0-EPuAMt^qP$AN5YCHXcTWVDgw+ju}{<?i8wH!F9KAn2^zK7+`N@$R2NWD7j*pG0H`9`{ckGUL?y2M*aH)%)iU8M11*%?oTXE#TbY?%e#B51;+?pFWY}NPeJmbN{>{Gm^i5-r!740>=+@McqGkKvR>!IfM5RzJJ<4Kf`yA8wxvaxC<BsUL4##Zz#rvgdz;8n{P4&)lD~<q8KakIEo^Sf_`*IUBwiIQEj@56wa(1htY(==H;X;nW8W-Pq&f6nVQo$k}wMVPNmySQ5Y|#+elHY-7Vb)i~@JJbQ>uO<HdBFD2l~I={8^#$VBNjQWVIG%Wb6a=4QD~7<6uy+e}f&nZ;39Aw_+D)u51~KEG;EL{Xn#H7KB{=y#WHS58pfd=n_B?p=hSy30+3sMbe&xl0rkezTX`3{lx%B+G4tsMb!u+$M?&clzZvL!hZCM`4K&)#AhDHc?c_hs$k-sO;u{xs4Fj`h#M*O%xUWNwM5!h)Q;|qp(H@M_3YsBP@}@5thVY2rFV}M7G@~218a6gCVPk!H`wJV8|+7Fk}@j7_y2M3|WZ>hOVXqM_AH<BP?;i5tcOI2um7pgyr_{2+Q5y5th5ZBP_RjM_BIm&Xyr}dq-IA_KvXJ?Hysc+dIPFERgK9X^=LC+|MJHIeiRyJqy>l4FGvN574G`0Ob9wdr`;z!=HZk*@qwg;-CN1htGfUlh1zg-$N+>?kHtBkFrkbGbrh-yUi`lFZn#cKBY3hl(X(t=LMYi(=c@yCe3L8D8t&l>c4neHeZIddewIU%jV0lRxjHv=-eNM8CL97^98KVFT;|(>b-bc(_V+=dewUYYuf9uUay)h@aN_*%&=;&Ixc?x(_gad;bGlgwOrg$KK#`;EY+)?iywXd)2qGk)6YKp^1uA<|NGPLe)E^#{q~=~`hWlJKYwQyzuX|@V~l(9)utT(X@3wNmh)971{EHb^Hl=|6qb16bYLh5F<LMrgBU#+5<QG242d2_7lwolr$Iu}hS4D*A;alh(3Fwb<wCv970IZP)m)K`Dp}1F$*5q}K#`u8uxf-zMro;Li1fU)RHH*ON<K9^B%|b0<3ch@F*Pov=cSmM7LrjSsR1B8FOk#$kc`qrO#rCr;#6&^2p}8PixL6yTjvnjs9%&2kc|RHNdeiYEtD9LpBEQO3dly$pTvOtyyj0+KsIXeGzR47wRoBWvQZ<aDIh<uk<$>6joLL$0okZs(-e@6nlg<6um@qeO##`c#L*OxpI72&2*^f-jHZD6yh27pKsG8@GzH}6l`9$ovQbeYDWI_Hk9HRV99_i#j;=xgM^_Pmp(_Ev(NzH8=&JqS(UtqZBP_RnM_6wEj<DSQ9bviqJHm4FcZB8MZwTwH-w~EuzauPnen(jD{Eo2P_#I)n@jJqD-*<%NzVB>HYTK{IwSwCA9bL8UJGyGycXZXZZ|KTx-_cduzN4$QeMeVr`;M^O_8nol?K{G9+joTJw(khbZQl`=+rA;Jw|z%gZu^d~-1Z$|x$Qf`a@%)=<+fkny7jMb-TFJi-z<<46eYsj`L>*O%R}9hSy4Lc)~6L-$6L*o&%*7w@WBe9oP{sSm*_oEt7qYhs-+))`uTqyXZh&D@trc7k2`Xo#%|}aw@W`$!~di8^Dz6Qxm(Y|kFB7O_la#AgwxYUJ}D0?H9cLb$6MPzEY+*ZLwX<FhsAnTdKj0F9dF0`uv)LG4e7mmAC~J?x#5&$bsBtF(!vGWaH{IV^1Uid#M3vd*sEH^8#f^b;bFx-c7Hy8`1`P8uPPC5+$tP|$E`I#u82Jt;0+7*s<x0;Wv;`5y(%tzP?h<&pJh~#sd&VwLX<p`oJa=+B+0Q*Qb3Z75(Eh($tXdPK$4!9AV}Cq&npEaT_m)O2whO+avLwGa=ncgPK~4Hi!>ip>um%{(@az~kXX|vfy5|C*0A9e;%dB@{>D#(O9Gkaz^;MBnm$P+Mjf*zlEhG_-X@a7Q0G37q`x<i<XK&t?JlY~Wtb9GoH9&_DtSUXs6>|hyd6{$OP<vZD*45!Qk4LcCv?VXkjc+G<21+QS)FkjYG76D{WFt1p&wL(OMc!Ds!1i!>Ic=>k`bvEa7dCTv_Wfr$<O<sHJjvFeb5?B^7E4iO(xkmdC+K*zps8!4Kn%pJ&OjJ{L%%E;bbi-q`XBT<t+-a%&ZlCIBwPwKdA6>mpF=194v_gT39c)L8BNI*qSt;xAbzGEs9a+uHgcDJ}<YKq8Qx-8Y-X{^Ku&_93Nnf5d~gOrQ7)6_&RHTDC~A6-6jUdrCTFIVTT#%HZeG!>ly+IJ0?lDA;59amlRN6D&wdxm2nvM(~<$|bCU&$0M#&AkO)xc-!|8~lu)MycuHol=1xLGeeO`9nZdF#m(WlRivtY}b^e)qxeXR|TKJg83~Tx%XH=uSKw?HUd^j{_)cN;n_fInFv=}}OCf4*xFsX0Vebl$=KI&_AA9cz#OV<Z4->kp-eVJpf^*rJvbIi4!g(sV1uKhf~9COTdJ?p+<j=65<QRbLquKQVcvN`6qoCla=j=80??knb)TONj)WRAHFYj?Ie<~FR=N#>Z_uvT9&$J~Y$JINe#8<y;BbIfg6u9M6$w_&}$Vve~Ft9F(-=02?3S>~AguvGsp=9v4qC(kj*+=t~n$sBVZmh&WYOo=B(S*nB(!yHpGh+&Q?(Zi@kljvcXV@lX?%rPZx80MG~GMu6^O&LZ}ndS<o@=<ezV~(kL!ZF9xKw+3;YJ_miF*QRN=9n5C9CJ*~4vsmd#s$Y5Q{#eRj;U$EF~`&ZV3=cS0C3DPH31mrn34dTs!WLh`K@yZr|eKdfMbp+DZnwulo()`V@e8e%rPYf80MIo0vvNpjRA%^rltVL98*((VUDRGz%j?v6yTU+Y6@`7F*ODl=9roS9CJ)f0fsrIh5*MLQ&WIpj;SHQF~`&tV3=cS2yo0XB?TDnTM_~sUBv*7u0jAuR}p}ts{p{!RRCb<%KhKbmHWRVEVqA0SZ@E0u-yF}VY&M|!gBL>gyr7v2+OVC5tduOA*^?PM_BIsj<DSL9bvigJHm3`cZB7>?|kOfwr{v^$!*`!RolL!tG0bdS8e-_uG;n;UA65Sx^mlhbmg}12+M8X5tiG&BP_RlM_6wAj<DSJ9bvicJHm3?cZB7(ZwTvc-w~GEz9THReMeYs`}M6`|N7Rge|_oJ-$(+N+rFc#wtYueZTpU{+V&k?we35)YTGw-<+ktW%5C2fmfOA~EVq3}SZ@1{u-x_?VY%%)!gAYpgypvH2+M8X5Z2qiBP_RlM_6wAj<DSJ9bvicJHm3?cZ9!LAZ@NE_P(8U=Xhf8`&qX>_A>siZd#VJ@MBNxW64ok(pkAbSI!6Jd{$ncE2o2UIV*3^m6wBZJuC0eJ)@7x?W~-hyXGF1`=FejdvhP9hxM28V@KYj@~{G*TV0=}hedeRNdPZ1QyNy`bFb^O^so%C+6Qj@<#bdYmf@w7HB}y#;Z@%NRvwn&RjUA29+u%%s{mFWmf=;a09GD%!8}QMScOLU|515Zghu`Uau*5G-S)&E{`6P>-kg{vf+$o-58EO2hzcT%4hIbpMvH@Hi0=yj<1c^m*^mDD%QyauUxv+L^)^eKoMeA^R{rGIfB5~s{`z0Oe(ic3MHcB{|6ILI7>V`I)%$>9IKKvf@$CJchmfG*yx{Xdk~`AFHobbEKN9QHtM~aMJwILz@WWD;_+cqa{IHZIept#9KP+X5AC|Jj4@+6%hovm>!%&v^k>}vR(f&~a2&|ZIcQFGNwzu1ukzudcea^^67n<gaY-EmUqR2*njV6iwZt7S-8+lspSO6d11WM?Dh1&T(Wy~<84k*KLr4A@#nk{v}9QnBwL%<v}?AQbNF#Om9_?TwM9-v4z>=*(Tam=X$7@6o!{iW2`c1igQ17h-P5R+emm@?~3<2J+?-q;di9B*t*F^)O5rkFCpl}gi0d2UOkVW!OTrP5?mo*PpI)KVr`Qw6+Io|{tzxKd`hQw8u+p1bA+%u=j<K|)KJxG#KR9Hf-j4pPc%2Px&XgOu{xK}vb;Af>!^kWyYdNGY!|NO_4t>Pw{^^`+8|YMnhO(r|oLHEFzTORFJdo-M6r5^wqxhScW<LIH+2=E(tmylg%lAj&-V>3~tZ8I+JxpPMiRj8Y93rT{zYyIJW0n$&4w=>e&DGbmA|K95TeP{lAb4^YK0&JIw;aLx`;rCNUjNLKkiyt5_LwCAN85^9<OOA2b*b6C<$)0{$Bg*5HCJ*CE#X82QTKxyv=i)e;v(~?C3r19oYB29bl@EPDrGdw;6Kxyv=ZwCz1rX_C&NMp^QMw<5ACN;p7X85EAfYRpw$pwyEn)NpqIDPSEP%=$>o{SzaO*0DQG}E;20XzcsX~qdq{$?HaiFqJd51G$HmMLvNDVMWw_2UtaBh>Q<?QuN9QMjFj`=oe;<1qa^%=)-@;wZeHg*QJQ;W)x}9$|kRk8l*;&%%>pK~Ce8Wf<q3uz}zXqYNuP%}E<bWmwp$Oi~_JcB+$<hZTL*^n;a$C2jQl9F>PvZ1nsbm4{_)^!yx^hvjSZ{2Y~s^=tI}9F*&@VvU}kqw=`xPFjO?Sc8)yKT;jm;H1nC%^+z`CRqav;&kCi21!m~iDZv7qp(CmNHPjbBzB}}g(VU~l2KS9*(1%UE71^=jJgty9cfx!iN=a##GVCQk!IA}YQRWFy{!g}G_BrN<3=*-Z8dJB8TGcBJCadvtGOdhtGCq@lAL;5jUmaoQ_&ofzOMkZfLhXP)RNw!7Nc`Vvx(EXBiRHdN3`2$0`nc(Z6cv54EIk$vU8y!DI^>B8InS>a~QAb1C^pDa_C_xOWv@QC2m;Ck}@o1Ng0;1<O)k!a)qTVal%rTIAJMEfN+#GKUm5VA1q}F1eUS{0!LW_fzbt{fuJ~~p@5(`q@jSII8DNm2#RwxDT$ysCBTvh4$TWc`OipK0YSNWAN=!QeE#XL{_(@-pZ_;qh^rZ)IF+~>5{glZt0AE{g`}Diicv_aDWN!JkQx(;k>?q3LNNk815hZ>6Fmb^C`P1bKnmq~re{D3?0b^$gTjOlO1=*d#cBQ5^iZCMlLqwQC`)>%*2RIshic@LYJR9jK&b|ZY9y3ufT+(SN;N-JBcoLFLwz1nssW-JA*BH=)aNOs0W4G_rZk|1`aGvJfQ4!Vl?Jp>jil0m7OD|d8qh+0o>dyaLUl}jH7!)b<X6K&bxeLWEmXtgSK~r;Onx;RRKw&~qd|2{el;6Z!){fwfnmU|(ZCW`WMBy^FtCIb7g)lI3oK!U1(vYF0!vs@fupRcz*3e_U@1!|u#_beSjrL!EM-Xqma-%QOIZSer7VHKQkFd6C~F?DlqC*W$`S`GWk~~;@;57Go!GLWi|=bc4>_r2qpoM+`ZVj~RF77-vvTvBL5?Hr=MnnjW{`t$Th7Akq-K!gFzGzZMXmQmGuxm3{Kwz^^*4X{>d5cMA3pr-BmHb$kDt%u?~j{Nj>6?EeAUr`3#M8fq~B@c_)_(6vl_LAwc%@!=A<a4HZ1xyCr2r@Vb!NeNlI;4^_Lkgu!Fn}tNp5-16K_7VZC4VbG*?*-iOb?WzUD#MBaz>p7vQYIIQ^mG=AyygX+VAzv=;@ead~@#-FDz9hHZLd({I%+x+^laIbnmp0~mV?Q4>L(j59}fPS225lKH*vxuahDa|61ew=0zNk8+NMI`;C7wD$~`mu_-HU6Z(2ct-8a<Yju{UnD`B>g0ZQ6&8&r;u0UPkPyxL?cp~=S!l2$(lh;L&@3iCH^F5znApmWJ78CN#DnQuQADK;Lw<4DN9Upl=b&6&pP~R_rHWrr;Gj)W_bJqzJ%F1S<;`m>~uQn58ISv5&eO4l120fZeFs8{@gjqBKmV@g=Xl_m=&6#zhe_aGtw8vS1-Tz)njF=jbI*?F89A~R65`Px>4zL|LaDjm-}BgyT0^1n*7kQ`qHzs{L-P?-hNV+-!^-S&ZEii9h;)FwEW(oDOyj;@^fcT(RnoaQDakdlGb0f`pQL~{@hjPFLC*`t25l!^jEJM_G|j1SEu=}=`Wy>Ul4rls?!*yzjpOy*Gv6Htn*wi^~cbgLHRMPuO0Q**N*z@)KkQJCjt6<+1RcNzKV@)R^Y3MlsED*Y>3k~@&_)J27lmE>2&`KNTmVqH5WNH!hp<vcO$@uevUigJ$s6F!hmdwb^?5;ZfhsJ*WXB&4!&&NiBQy^wm!r2Re$5UVfv~+aebQUtNz|~=ZaT<@4D01r@wc7hU1t1$aTZ<OMm0~G{-Of#p~8#q5Qmc>#$IM-un0ELM+QTR>Leq7Hh1=WrZx(SPiobS*x)+W*M?ZV|6SoWRb?|m_f+84EoIZcE!c&^qcF7i`9sl*Oe11ylYDLab$HGmNj*(?61;vA39d2F<isO3is3HK5eW{)1d~8)o41@d|@d|ys(rdRanZBDlBEm5tg#V2uoQ~grh9EU~@W66c=p9$*bgo&8QQTT(F_<Q3AD_R5{<~g3a;MkzBALBu=0bb8|eRG#6|y$F*v9*yhExYLf6~P?E%ExNK>X*c_KFO%mJ7ajhCQws~=_8a=ET)a<btajlv?HY2W8v&Uw{wQBa*j7~Yt9@~3WN!ygt(drZ=ZH}wBqLkg~2vL->ztw2Fzt(8GJJpa9Q+DfbUxg`DdAW@#yW@!?F=b}}yWFRg-7z212(mLc2A3(jWAmh$V`t2<+-Hv6G1St`v7;~fLMj5OG`J4l9n(;a5IgimOZORKcih}GMC=TF(tU{79p5}n5j$h5bRQyi$DvTe!OomKkILVymu;dyN0ZpFF6SZ3QyYyFA+G7HT>W6r;|TdYLVFzSc@!>Z;XWzX^EgaB53@d>`@<(}ZD-{Pp{mCb`gw%sp{hsW^(;IsRP{K{HjI-VyI&lYhgE##tMRxMXB$@SmB9vW#o2~cdu6cUwc>2U+P$*dh|%EmXT>(G-YdV2#|A#zuyU__H>iWpHmuw$PYut)XB*b<m8Hg=`9Ewa+pvPKEHxh2b8o}qz4F$e_1xRI1?M;NwD(~J&vM$>hZQ{0Y2&+f8Z9_OQ81H?np=r1%=@APWTDFWHmXqNbemO@-}aMk6H9_!Kj}8HBvwbAZi7nldw$Y=cuBD5C*9|j#OlG*eO^g^jdHq=E(z8sr~B-ZSdDVJPb<l<QBL;(CczrzbRS&Uhv-zKtjQ%gmDL(nkfX|}tX;E8aw_IEqo9XAwf|{GNls^>#uD_<r?yUwCCTa-Rixp#Oi0pj@>C^gWT$Xbf<|^)(IjYOqgq8mg_TY!p&}cWjuI-Y3|LJNP6(_9i0o7aX@ba38HdJ&Y?N_mTF6cjg2shx6d`Cd$W8&4MuY5BU}-eSMxvP}gY1-MYcycKE2n}FjRx5%g4b-2+2usJj|P^qL<2`zl0jik>i5aO5>{kj2`ezLgcTQ9!iozlVTA>ju)+dMSW<zdEUCa!mQdg*YbLOiB@<Z65(zA2i3FCiBmzrW0)eG0fxuFhJYXqH9I%un4LHi01}tSs1CFw!fp=V!Bq!7vo$eACs?q2!fuT<8bC>u~zc&j)2^-ZY_?56>2`kvJge7cP$`Up#WeFROvW5*yS;B^;EMdb^mat(dOW3fKC2UyA5;iPl2^*HOgbhns!iJ-)VZ&0Eu;D06*l3PBtYnJjn8QkzXpT3mgo)<+x85&_Xwbg(e*Hsp9Bw5hG{<sQazbMrN6URqXs`tg6gxD>tU;4PW4DE%vY|P)7#bCjwOApQ4VJP*1xs0?f~71`!BUo}U@1#fu#_b#SjrL=9A%9Pma;?zM_HmmXAE-xmckNNpkN6rPOyX(6Ij9u2`phn1eUM@0!vr|fu$^Yz*3et;3#Vxu#_bYSjv(HEM-Xpma?P)OIgx@r7UT{QkFDeDN7o#lqC%~%9;i&Wk~~$vZR6at(t}Pt(t}Pt(t}Pt(t}Pt(t}Pt(t}Pt(t}PwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+Xt(t|+@@G&uuvzW{iU+9j{cD8HG1`?xusJ@v5(%I$>HRB%%`uFUOt2Y-QJM)h$1qAm!DbjnX(-qn!zfJ!n_(EGsbF&qqcj$5j$xGMg3U3E(qOPThEbXfHpehZqrv7FMrk(K48thR2Ag9TrQu*R45Kt0Y>r`+ri0BejM~3hFMD7ZMNJ>~dKNAZg->0Cdpir)hr*}!w!NQ)+e6_~N8Y}kh5J*Nrc;~PzMYlV=gNmK(!QUSx97^={l(>FIV<nam6wBZIxAlpKhYg4FL{to56xE6NqJa+S6)w)4e~N9!SvK2CZCjtHF)LmL@6vU!z#S8b-H0?d{iEm;gzcs#ofFN>+s6W>4q22QF&O0S8h)9&x)Leg?MG)1cMZE8W!S}e-l<7*5Q?H6ILEK!aPZNScX?dO;~wYhF3;SGzvpvL2_yjB^M;8_E3UBa%vAH86>A@PohC`iuNQLBqJtXl7ZvGp~)aUk8KaYz_B|CzyO*m0WffkWdblr&!boaFmNn<0x(GEFZ=z3q>>CAyQF{&pz%<;PX>++RzL>OcqrW`1IOMhKm%wzl<uQ}V_Fxm0ea|mQkHCxoEmls2ieK>m2i-qy9x;h*}1EbaFCt53JC|<DPfmzkc|p<2?yCIVApT}owU+@ILOAaT>uBr@haVigKQj-25<oVlG1%R$i`8000-GP_7C778^`_u96*<+d>;-RE2aPr3@fGp4je0{01lu*P`(cbma=36OIfmkp{&uMu)jLnZ89kAZ^L#Q3<}!5S8$&|mCJ1~pvw6+7!=>@`2HP3fqx6++ptjBALaQzEEM1AIN#@o0{_Iz_W`1?BY=FLAByjEobNM5fq%N^`%F>bfkU~^6cgsC+{X+$N98_e6n4B(?qkM;l~(Sf2VH69K6)TGqO-C@4@+61hovmh!%)`fQQxX$sBcv=ROsPcZlgza+(9LJRQ4C`{ZfYN7ywJmsP6`0YZ9r`a<Bt1apo_ekow#}Ie?IA7$^r6Qs2$N4ydF~%fSv9#hXFNDD}Aob-*L_c@B1fBlUR>c7P-Gc@B1f9@WUf4$z~14>{NYqZsx`0i#&Tl2I(PD8(qv$nKVm(j53vjM5zVQHau<GEPM(%_-wlgwmYI21zJw{$5pY6H2qTs(PPLocRj~r9F?l2neMa(INq%wE0|G?-NS1z_i{c6mJG4p)|%3^**6ABLpWvl<BYiG`hwZ=e3^)l2l{Opr)F}AP>MwdmgD7z)G7!V*Lw)YT8>=(;vEGXKkLLc&8hIU6OY?I+G~?c&PIIGa0IU|2nA8$f1_#)1SvsYpm(BQm6x}>G9|MPk;X7Z~yw6zx>;S{OTj$^R9=N<kQ&~3tSNO2?_840rlq*@B!WQSrPC7+{}Obm6WD*cys{HXu5MMp$Vvad*N5p_;0_|?>hJAU}uz2)SZ(ANkNvfgdj^<LQsG0#HPP?V$<JZoAn{vRBZ*K*k)yiMEBWdwd!^i+pJdIu40?@;VyLl;%Q}@(EWR-)!BpY-!QEVg~655`jGy>)zZrF4_qy+4*!9BrWNgzg&fg5oqupR1Lq%{%~<mfPHI-;Pj-zd>xAT`06f;`(Mth%th2J00t{K_g)dpxOzUgVvc3i_>s!#WIl>A}EMbKvmarldOIU%4C9HVF5>`B72x|hdge8Gk$`U**WeFaZvP2C_S(1jOECIt(mVjX?OQf)rB~m!bnk2T@jxe^@jxe^@jxe^@XkdGd2DZ0oU}w&v_i4ZqRy1G<D;ltb6%AOziUurUMFWPgrU6S>(txEbX~0sJG+-%98nBcl4Oq&O1}tSs1D3L+0ZUoZfTOHwz*3epU@1!)u#_bYSjv(HEM-Xp)^}ezdo50&iFEd|l%=zmr7WGjEM@8JWhqN%FH2ckdl|}swU?!=y}c}H?d@erYjZD4TAO=W(%Rk2lGg5Cmb7;FvZS@UmnE(3y&UPl-pi8K{$7@}_V==+wZWGqtqr~`Y3=Z3Nq@6szEY94;Ii!D=Rf}N;b;F|_7Gf#ZNr%5!I-B~i(t%s7_&a~?L7fpUIyi-Hpcy=oCf9oP<cHm=Rx_x#rPk8`IFCn^v_@Zs($gy;9l}PL>Y#-urvPIXP^G?Ed9x^|M2^N{q?_m`^(Zp)nTX$d*l1}x91_+FvOMPczA((mhPkUQ>Wvz^tiZFo+Lf4;Z!C`k4rVxInrfZt5=@mSbAKnSEl1wdR(nnrsG(8T%}j8<5+rJm5*J=&(h;+d~7>@mL6AQp0pavN4DBYtFer$F;7~JWn7JU(rVP~k?wN9-|DG9-b~U6d89eC(+GK_hqO}+CP}X`33EvA#{xSIB~&`!hmrJ%cg{md2uZhj=c`|{9!R4|dW1XYF*K7Tf;(qv%_Pj-`}_;iQ1bLW7eFW8i!K0Gp1$Y;s0F_00;q+)Xo4+IUo_#DWc>xx5zst+)r4%|t0rWV2qSbvHkPy|8%J7`O`btE=W`rMHu;U#+<<H{J5y=*`6a^~7635$(U+r<)0J%O5RII%<VRnPM$T3;`DiqBq>_#3p@?6ezU2Zy#(T{KYo5Mmf;I3(6OPI3ikskzC9UzrlGgNMNo#1aq&1^h(i%-HX^ke9v_=z4TBC_0t<j`BLX#vnbB!it)&U4WlVSmcWRqfTTarzR5t$b-NqM*-f<u;K?T6r~r99jY$stQ&+aWnyDXi_AoUN1@RvrP26vN9SV30D+%p)L@;@D{fNKz&=vPW!Ep0~0`Y*MB*vj?P7h@;9k=kaGxm8zdW15I(9PXeMT^V(&<{3-nHpC2{O1|(FBj+TIgENM+bj<hDBI>+$?mA=#|t>zMas?ln$$)`?hHP;wq82kqmRA(41XbP%^(SpXFI?ZSyV4rFj*hTPDXIPB{6jTkbkpO<`G_#Qah3X5tV?n1j)i4{37^zOM8;lsK8is=bBh_h^g8?H|!}KqJpK2knh9Ar5KA@O7(TC(VSZVsH@6k_vjeeR@BBB|m8D*;)Z5m5^18CD&NE(2d<_CZQz-cf541i5T`@tz&Op{G>V#@-Up^r^Ya+(uK7eEYs?gS`?K6e7(LZ5p9NJ5``0Z7tVzTE;yq`}C!1)xYnTkUpyl>vRw=S~1W=yPX)AI%BV4Df?KH@Q!0PBdWv63xl^lOWNJDi944{dvZ4022Lq$Z!A>ogqrQ4-(A$eIwM+{RB<`5*_}`!4U~c3t$aE-3WP(IHLPu%;bEe!#HMgK+=uG>If~m6C)j<1%2)W(1Jd90&GE_o3I6a?gg*~TB-dct<i!#_E}q_MTa%b37`di?gY@Hvr^Xt$ik7<WU)F$92zZFr-(zd#cCCCNVuTV={{Yo=*M@KmUKa%dby7h^r@HoC;`p+7l0D%sn6OPC02O!ngBP@=O#xI(A=J!NU+B~X$RP_!b=izB0-;<97(J!?UPW$3iIFyHLzcIMkf;Vxf8$!`rPD1f<AW!*g&6~oJg!jbbSC0n^8cZxnX;rk{e*d=ENv!Y}lSB@CMYdIgy{58aDK0J*ARsYM@UIZZhaolaf^W*yJXIJ~zPz`rHH?=yNZC8|ZVBn~aTRR}*a5VEQt_h7Iip%W03)+(4h3++@(_CWRFAxyelieQweiL!X=6WYFg(B@vsGF0Q%3a(R{9U@1#(aFjJRSjrL`EM-Xzma>EfOIb35rL2*`lGemvNo!!Rq%|*C(i#^W>3|k2X-x~3w1x#sTC;*Btx>^})}&xbYf!MHH78io8WSvOO$pY9t6j@1GgfU+W=U%oGDkWv8?&Uf+n6P--Nr0w?KWmfYnL%gI`9><v;#jeOFJ+Wv$O+4F-toz5_7a8>o7|@une=b1J5u^JMav%v;(g&OFQrev$O+GFiSfy1+%mRS1?OEumyW@gHKLBhu+{F>0pDmr1b`GN$U;XlGYo%C9OAjOFG!#E$v`~x3q%|-qH>>cuPCj;2rH~gSWJU4c^iYHh4=r*x)VgV1u``gALx&4mNm8JJ{gUdyW#GcCf)a+V$JDlbkq}$cFPcW*)}8@P4P&4z&!*7uN6C2%y$Mx;>XZ+?v%kNOw05<UB+lhFBk_ft;1sLHQz&!D}tA+c3^WI78?!@HZ>Cv%5gi!|%iJS9vP5v%M{&baLPSd5m$HUj?gB6Rb9_=Br>8&jhQDi~A~OWzJ9FJpT9vxXNO|4g_ud1YCu&U<ZOWuKlYtmIn?5U(MuKpR0q#llC8I<0s>BhRa!c{7O8|a5+nlUx3FME+^?eegPh5xSXXwvcKm^(&NH^oZ)ho9+&##3>O4EX^x3jBfyiK<_%3e$!Xru#FJ*YR%-G|hH0e+p7eZEY6O2^a18*SDXA#|)Htar0n`{Tpd+%e;#mT;nG$FcP>mC45&(<!4hX#@@)zCd`xd}Unqeg$@JKSO<O3eDzC#7j30npY;YpfkVfBT65DhcQD3S<Z#*)@B<49|m$+H|m+kKc}DHxR;-%x3Ae3NIG9BY`#hR3mnnLN$nSi?+a2Xo~<%;Xs^ngPsY!$mWInLN!!Gk}?lzT&5|(Ew)h3@_OLX0l->8^BDS<|Z4!OlBv2<Rm7~a8nLoCL4Cj0nFrSe#!yN<oAGs9n9qS4rcOu2Q&G-gPHu=!OT0UE1G4j)D_J#Wk%GQW}0F|ooSRQ&R;F{KG+n)(^aEPnUPPanWh-=lmW^V=MVP^z@`}1w*ksLdjl&%8uSWQL^8%JSP|D0W-LWWrm$lfLNXKMLW({T2ymwue_RK+V@Yekaijxev7|M!l=qHb%6rEz<+bA%C-*~xNi}RcG?!GvTSMbWWflPdM_97MLXK9bG`Jd~(&;{WQ0WD*M|JEN0^GO}67sck=zsa}*-!uJBLy5?53i8~rBj^zF#-~)j`v1@BGYH>JiG=JG;1e&tN>7|W4#p+%Jf+~53jid&DzNeE#MLuva$d!sg4_8047vB12VC~VFEO<!eIh7F~ed0_RIb9clU*H@Y0xZB%qk~TA^=yuh6%>SLjQn(|wL<j<2KUnC93zYL02MztIJuPIEq_nsl0DnHpfs^jWJ2b(*tB1gO)TJtE+k_G0;Nd$D}C&DkTolHK-R$!>eEWVgLnvfJLf8EWs{47K-ehT3a4Lr!3e29*BZ{ZF@QekGxFtL9e{N_Py~HKBCJRb3NGcU;vqp}<HVLLV^GhtP)=gb~mO3=AS<(OIY=IYa4A5?cTk-AG~!xS~60X#rPsCoL_&h0fBu62JvZTH}Hv9pHi`t#QGU*0^9vYg}-oH7=}13Y*3S7M{=vE>LNJ3sf550+j~1usY#F8W&b}Ee`HwU<OM9v|weK1h}xyKTt@3D4ZyjfGDgel>jN$`G;2tPzOvzNq{=6WRZY6*7?^m1WZ<TEknR$Wv7V*OjhgaM3c#CU7ct&S*@!R%_i&ja&;0=%=+4)$M#xn$@W@p$@W@pi50G*8OBOL(F|jSlxT*rGD<YWZ1c+v2<X715yClEVn+Zm+x*fN0y<V;NB}xkU`RkQFHBnoq_eS#pbS9AN<RuH=7lAi0qJb4A}9mW*%+S@(Af+Jr+{;|7t2q!7t2q!DGZgXQ+~2LJs=WvcB8pLgU;?`t83EPojh_)I=d4`u1RNSmja-Qc4v12z+h#ER|3RXWoK6c#8_pAR|2H{c!yU4#7kvo2foBY#gf*1Vo7WEu%tD6Skf9jENP7umbAtSM>@a?OIl-vC9SE#lGae+NC)0+x7}(FoqAs*Z!=6!67;NXz`<={=P?a9xG~e(OnP##HfYK@P6>@#4h-8Cc1Q(GPSVlH_3K~Yy}s9ktWMwrC1iHOW@tfx;Y`uOtlJhRE;RCNTb#Vm$hFOyBhnv?=ZKW8riGoYkZM$KrIF%PywXT{Dx0FrJll*Z%FL8)agyL8TQ=kbo0%`0qaE-<a!xfgFC^z!L-Rsnf5sDBNbK);U?OsmzVnAXun}R&3p=q7@uUMjaI_;lu(Sg_u(Sgpu(Sgnu(Sglu(SgJu(X5y-_j2De@i>q@h$CO!*{f!4d2oZws=cB*x@bhV28J~zg;_dVsK8;_ceVOv-m+F$062Xi267u<fyz2%573i$Z?!~7^lxk7h0D=dG&L8jzgqji0yGs&rvxK%KN08p5r)W7{>_8IZD@2Iz7!`I$g7_<8r<V$a!oKypGHFGARc-1h3<=y~@V%EP~f@6+0m~$M-v~+^Z0r$);kb2ieAjewCO*%lfu)fzQgm*~S$<EBj^}7xk>{n{8awv$Aitk8IJCvTwF=DbLEj*~X<jEBi(>%hT+ertQ}xvsl?TnpLJmLuhDmk|8vvSiwD-Q>Fy>Xijm0do-ua3+@RxC9z(e3^*mt2=ohhB^iN!0j8vBfqntBB!=o4U`m>isTtr(GD0;207=tQH3J+;FmRv%9!WDo9|AB*M(9HTCTUveLx3rX{l!!OrX+{f15QcbpGm)@nrxJ2Xm+7#9Q{7KQ0etPvry^nKD1Ej{XVoDf(1VN^q;N@+JF9w&p-XuKYsZ9^Z)jV9!>H~hJB&?eSpcVoM#8fV$aceIE^tG-s|oFUoxx0*#W-TvveL#LrjJR0z06X%qnqq05A3|orVj5Cc{dT9WYFWZpa&8m<iLg0i2=Jv;m&UtR80r1T$gDZGdX%lG^~)pn#i`wC0q;{@?_hQf^NF-;Q<kK$2PtG@)qssiim+C!xieozp-XVG4wbcAr;@Q6sEz#hIP+K$>0(#EAw_r7)amfK;3bI*+8mrNGZx1C&x=D|!W#Qk>@e08@%n=o~OfG3uNHBq>huaeyR+?c?M$rLcNba+*?LyFdo`LBA{+uts4uq8XruBdt+`TGj*Bpwi$>q`DM&9!&yAg)GzW69>!%>h}?&`llrQK6O+GH2pqyzzmBHID`H|SHKw)exfU25BeKj0c})v&AbBGu%tC>Skf9b9O-~GENM*|mb3;9OIm}5C9OfjlGdDINo&loq%~$Z(i$_`-=UtQ&B)c&9MX(jUCkWL=nB%v(Pre`YW8SG-mT`0W^^=Z%xE)0XanA8MhI<y8_n^V3D}}RHyBdr+E}J7DRh1MLnk$^@Rv@`Gn!+@98kv7sUh_uaB4EZ4fqwv05|A5N`N=$I!XXI8tcbQ05}@!$4me?8tlhR_lcuhrw<Y=y7OnF1_~;@-6skvz28TQ?*FX|>OVUCQx_C_baosAYCSqk-P-_GbpNPl1E|sAS<ePgqqEzq4Uk6nOJX)aA03`FZ-6>FyTjT5b#!<`L(Vq3fA>$$J371&A_pFwT?ml_kM7rzkVB9T@1MviNQdP%9Z*R(E?dtdX-J_n)bB$IGKFvC^2Jh?h+-*ALa~%3pg77JMl5B?B9^jb5ldO4h$XGD!;;q2VM%N1u%tC%Skf9WENKlGj&#5mmb7LGOIo9ZC9P4ylGfN@No#7bq%|~H(wY*i%}YXplkcJ-!O3^gkg!=sZ;}$6=on22n`7XoF#$%EfE$s`F=o`9u#unif^I@AY0U|iwB`g$T62OWtvSJx)|_BTYff;a15U7{H78ioniDK(%?XyY<^)SxbAlzUIl+?FoZv`nPH^H;G$%OmD4G*?!$wqN0u87DoUj`Pr5Y1hq|1J~PnMiOGfc{TPJj_61#kkJkPUfn&|e7g+@Q~$04h-J1+W60lLf#6`kAaJX$=cIt0GwdEbK5{dI7Ysvv}zR&;rZ;IYn0oxWJ~Qp&E&u{TWS4BrIvo3zoFz1xGsY_*!1G!?2P{0xPe@Xy6MhykMLKxPUks$m8oOa3O({8o-qV4Qc>)5-=wtp*|05_Rm8FhF&xUq7x@Cm;%v>mDl3eM|9%oMYA9}@$_Q9ri{8jX3P{Ro4_+giX_-is-PkXf1(PioPZNmP@P1AZpEZdA}vnYUu5jH_|<vD76ZP8a}A^BisU$+YOb)PHCI^DnkyXX03<AF%@LNg<_JqVzz9n_;08-Ozy?b@zy?b@Km<!WAOuT000c)nf`Rm&;kc(Aut0jxa@^Anw*B;;>A0sI?E2|F+i_3(+qF}ItQ1=7urGshd8m9UNZ8Y$Tpuc*ss{EvD7U967AFIjy$sS<*(cO3XRm|wMI^$HKmGi_j#F~{bNf4%uV43_bv=3;M!!l;z<=r=2kOH>`>YvU2kEP16zVs$Z=-a2`q*dfaq(UyqfB}8$KlH|uJEhS6n@5b9BEwfR~agF63a5K`RB1I#~b3ZjEg??=g)oA9#?%@Uw!$<;m2j4wplO#IMTT8(>`kw$AzDtMk1w?^tkY^(o<l9Y*{|CY3GO1$6dRmaZO*Pr@)M;lEy`Rm7emzmHcl%q%VJiUl_deG-oACYY9z4FwO#yP;%%^l2CH!O@dHzDpfTIrP*J^^XL+Ul4aLf?}LyxgBpa=^Dj#TLJ4-{5)hh^XA#kkk!KO%&9pp=h;?qPkU#zTkH7uvZ~pQX4E^}Sho609kyQNznuv@<jR=Sm%plBwc4p)TMVw>g21S@NEjK8F9`pnI;ZJ|{k)K!5<7+aasVW7ak(1aGv5}eB^3_a!g&f~aZuxRn{<ea@B8IQwsXOeHXXWa)`|OnAng;NcXGHdDipoZ0ucoLxEwWc5Rrc3&*TYMu$`0U4h{`h(g9Dh#Mr3dRQ+Zlua6ne`e*mYyM+550#^0j>b!8*7I0CIaA+tC_sr)>%I6|pBE3-J_s{8_wo}WNdS9W&w0K4*pUHz-Yc!*E__ig<P{cM`l^7A{T2*MocfWa(jjbQn;OSUrW&<TK3Va-YHJ~tKUlL&aJ%&<z;;8YB&RE<i-Xxh>gRAyMEY8)ztQ))m##c@gvFo<erKt2V!M`l1Z#c;ihu!d?c0Bh)+EC6Q;YfW4L&J?uAZ>Q<j1XExKR|0HOo;!g?Xu_ssM~6TKwmy;ro&q~I6Mze<y#TtPbF$pWi~0~Rf|Cu27uEU0T;fG_Zk{AvRHtr8LPd3qOf*&0`NcheJgQaP1Ng(6K@A}F`9*xh9~DMtkvpvluldMbR%O?G<SwhiYrYKdqdq*e%K$?vJG9FHL#lIVM{cX?^jnyMZn9v66uHT&&IM1vE!8>-(%e$#U+|=x*E$jQ)c4L*>T72z?*!av=$R65qv^*9xY6{}o_~BAVIdai&`6>4)A<M0%y9le`LZ?tq?Q>b8Ij|bDG4tD_818-5%n0apd$uyqGTclnh_-vF^~}@6ETqW4hRD^=Ji7G=IM8ca1Q(sk>eTbOGM6U8uY{=#W+-(P)qYz?YoTDzK~m~W*i#40<MR;VMU_}rW;N)nqaz<Qm>(<8y+{BS-N3yqfw<hzB8Itx?wvL&`Eb}X97IwjulLRC7t{wbCiy-#FEw^Vo7Tbv7|MASkf9lENKlKmb3;AOImY=C9OHblGbG5NC#kHNo%e!qyth|;UC@L&||g!o|mXVrSpAOpwj6+D^Tg>J}j)z=yADE3oAPnSnk8ZigxsVnrcl8D>MU5fEHF(uaf{Qtk1(iBUo5rDMJRdK($Fh><Y^yNFnUX$|Oi3><Y^yNC))_O9DvGG)hO=QBkWUt%<>s*2LgQ2gG1WYhtjZzg;vnFn*EuC*KrZ-zgd?sSab72V+JJM8`4PFlK#f>2hue>w|QAE`9hEr*)9N@QrxfZkV=Vhzt7&+HIKjLHWWN!fQ6n%P`LV*t_VcoCf79KbXgb204#oq=zryEIqF6D_<C|&>)WsIz2aeI!cf0_R8|*j-%{h;pTDSKDT^1d2{4(<vzE3Ictwg_R8|*M?d+`NO@ecS8gu<_{*Ps_M?CPa=ZD(FN0s@X^b*1*DD{FpMCb}56{}4{Q3{S|JPst%eQ-u9&22{*<QfsF~$X)pDy6D^hY-5Nd_-vT(YwaUdp&+CmOsQnwNu$7RfeGO<t<LG?HwSo`(Si1e2ckl>`8jCiImAAd{Z=l?41^SQ?ziku;Nx_LTr&66~fZfM60!Xej_((u69Ih+vXY1rjhznpOo85KMBaKmvkEGpaxWl1WAtNB}ZvS`|pZHOZ&~32-LOr~(NvCK**A0llPYRUiS&B&P}_fSKe}fdn*@=Fv?3LX(B0ncKE2hqw3juWwZ~A_3AIJq*6qzIzhU?gLIX%3K1%$<NDN0<bYA=RA(YoD3s2+I_Og&ntBTurVg*JdUQEY?K5=n3JE^1VwaX%+Gls%{m!Y#5906*{I}+@Wz^;4j3mJB|{P9WLEms0oEAva~ddsoD7T1I)EGIzjG{Li|EFhpa$qB8&!A_-Ovdlbdw!ZWeqHb^+-S@&|(8H2s9r62vT5rEI3>#M&xpU9p!oCazGu$h+Gb^qZpCP5owg?nadGq6eDvvB8_5XE=O=tSiUg1{IUE|0=A$YCJEp~VW(~h&;+$zS^!QIBXc<-2>8uj06;j7F#$gmBbPfu2Ka4V05MQkmjsA`eqGajVyN#FhDesE6YO6DsHo5FUjwM9v+Q33!Z2)J0>G#f{8t0gsL$<J1JJ0m+*c#&FwAfw>M-1JBIu|_j8+64)kuMgr~?|skcty(6hrQ5s8I~LsDVZ?<Z8w-2??0PG6@Nwqt0;l4d|m9&b|SB)M?JX0g6~=Dglbrc~>*VDKu$+heDGXCL{s37$zhEw@fo33Am*_k6a44r8z_-aitmgI03J;8Syv)sx%`WCqR`pEgmNTmu7_11l)q88^V?uwm1>L7``|WzDzU5iCD%k#)(*_!5%nLHrpncVn<NZp1Wd4EMpnIkeXR&_(E!C+xJ!q5`a%5{XnS7q(fZm_lbo{ulGrXN^kd3g-Y-D>4f^a?Dz2m`nv4*@ub5-l>I)QK+BjNPzm*n*#VY7)0iEA2z4^q0f|6InjMe`wWQerfpmBoz5xWG+AE+AIwvc@jt--%H-H`Vxi^3t&|hc+xItIW1_-0G^T7=e2K`QL02+|($Vpm5!^-~529+MGg(H#~R=E52`^>Ofq$8PuKJ|K^8CDCTBs9>c-tI%g%1CDe(6B<(*#I=G@RVl-)Igtm1=K*Fy8~>X&rK>xSH_m4c65c`Y*IVA!VYCZ4fMHJKn*Kn;uS!{3U~GuP{YccxmExTmb8WjOIkC7BdwWXV+Wz&W@Iy*$^vHC45zYy88*YIEMSHW+KHw6%&;-?OZSmsGa_eB18IQRAe$sW5F50HSpY$J6SM%Hpfj`pp4b?^EdVE+2|ACY;bMc}vH-f+7`Q9|E}RL<sIYW{s6h%#H-;LduynIxuSlKg2BC)3nQrW$kJOnu6LcO)gUAMtp^n<$F0tlVpy}$3bLq-9j9Dhxk(GUru9NJ@>M}^T$#!Hl4MX%fc4RdV%Ih0;WVH<ATv#a03EesmUx(o*xuMlIC{K4ot9=|}k{enbm-#zxXmwoMS8iyp#IDux1Mu83?Nl1m#xFo>{%_zo#`p<H{qb+$C_R1y(mLrka2#m-2wWMd-FXLxy`zmQ{K`P>am{=i*ZP%l8ZDY{;}XC0OS7ux+eh~G{O&qDjz4|}W?8JYafwf~So^ma!TkraBIV38lA+QYF?<0-r5P2lnx&Fa0jp6eO{;*_Je8coFbz~`M!lhCsbrKJYD`Mgstp5ZO3smC083M>rvhqntfvA_nrA%~01-50%z%dytoS4xG{s;q03yd=FF>Gq273VyC8z2(;Gi_4>NWtPWK`V-2$ZH(-3F|ajH=s!b<+10!xu1)V<M(WCc{g0Krq?qCea9!orHHyEmS()r<QEp3Z(n&LLJ-EeRzS6Z3*B?w(bNHfEVi7mH@Os&$a}hC0lm_2~Z35BufBWpeI=Z)RL_`fdtrvdRHX?FBz89X22`n3}rwsbcQmZmduKGGoTi4jb(r>bd6=eEt%EM<ohI2jCxy5BE|7w)g)5jy%ac1Db8)0CXr&@rb!Z^(ttgRQ`4f^qc934>`@@~Er2$PQ=$>jMq%f?3!sg{s^k`c7sUvfjPRm7PnnGHq8Krg5l|E(W-<bbLUx0*wB`v*S_6b7t@*){*8E^eYhbXXH7_{Qnit;jRnsIf#aB%eh2yKHfnuJonx>2TLaj)>PaxH(!PWp$jTj`&AJvFK3izYW$UzD?q#8j;0fy9RNk{>dR3{24pc1N0?rJJ@e9Zt$Dsz0zfJ*9&jGur`s*&*%&`F(^@e{C0H8OqzR;f;QO#my^$*u`#rA{alDL;@#Y3wei8pb7>ahem4Q;jkd$74+MjpH$<`KB3uqMB%$VJE6#r8!w309_h95(Mnh*r_{Vm*xar5P)e;U_?MLjU6cyW@*f`p#o%S(9@Na+cqabiPV}jcpFD*OqyeQ8-R;7K?Gx(<E|T!3;bvja%s?mnH;lF?FEoaa~h%o2x;tM2DB3O*GfdX5z?k9qZ|2VnlhlnRJ%_Z)bOa^$BgbIU1_qQPrcqJ3(H+9Knv*7v;vsuFgtDoFkv}B1vKF}Km|0>nbZ0PV4^#IHUU3$b_ccre6SoC1AMS77z1K(JQxFDaGVkYV6dDL17L8R5(8dv+zbO;u-ptaFRZT>a;y%CNM2Z-Bw7s&D{PwU_ld#smeR!FSW9VOSm7T|?LIK9PGW8V468$w8W>h5$Tk3m)xlNG3#*e38UVw}@T>t~Se<C!02o#$aW^1_mEl<jz+f4&1;Ah#vIWGjGOSzyF{}*zRsal^+hsru$lB~It%<>r*1)hiw;b6h=hz;WkYwZjW3$RSC24Fk(wj7KY({vK299l7c9X^r=*<PXZ=tCb>9>V;PzAup=G;IPKq8wHZWo{kbb}(b8=G?nMQ%l?85Fq)*%(fddyvh@6%4RsgIGfBMxK2uGitL%AIproYmKjEM!mKhLo8CqvAyRcvd!zR&5nb}Zd43vblHuHK@BK73!VlA8avB|1_c^BjBf@N8avrqHd2$ZBNE&QitI4qo3IF)kQK4W?$k*J_(8Qv`z+Na9W6Vo?<5^9yOA*;5XX-8?hSRc&|f#{Xo24-($TWR{CZMsK|g?`+JgPMcT{abwMn%FofA@Rv6I7)lXU-f<#flm^<#%2O|nYQ!@#rLTYDL#XSuibI!L$Y(uW^sZ-aDyE`5B-eUM(S%ns2XmFIERVVn!YMr?B4w?X>3CF@anAC#{xS<&pA23nVKp!9Tl&f4QLzA|Q|7U%1@P_L|5ae3fzpmEt=d9GrI^L1ReSDvfX;d~v}?UmK)og1FRH(?zY?v>Xn_Agn-#d>A0ic1gIakXCCtHNWx<3Qu$z4BPaHICc3Uaw46sp<RnkzF@WnV<7O<Kn&YPsN_^+qhn@3{*oZSqPP+iB!@El~`7vno2AaOHC!o$-U83lAPQdO(pcH0f?mM%c~J8Nsj+RfF;TBe+WRtn4XTPBtbI>f+dL^NfHn-=4VAzlAP0)085f_+7eKSF+b;lG@>MU^g<9Nv7;9PCC2>hh)|Mq<`5uCg6BsGPzinR1gIpjvyyb5N*wc2jUCzOOwrVljXFXN9oZ>t)6kKfx;70RId%&<7~_p*AzhCyxx_Q&>-WLLn?VgG(D$+fFv(8iP{1P7-~4%ajVqpEWe4=)O`--CW-5Ft!VQ2WI|aT0vApo|8{io4<u^bz-Xv<Q$wrlQ05X}C^)$dSnU$0@fH9eslr%sw*()je+Yjl>-{2SWAvEte7O9$d3T#K~_koAncJ}+k18qA2@D!u{Me|N^g4H$5Ag{el=*3dj@Zv}Z@M1}8cCn;2msrvoL@a5|A(php5KCH9h$XEF!;;oWVM%MEaHIpGu%tCnSkjs(ENM*?)<;!x!aLTenjq?X<s)@QUyCM*YV@^el0a^#KmYNE4?p|J-#S%4fCP?eG`wius54?yHF#7bH8lW_IxRIdz>qh70p};sv{H@Eq<~hc)1wjKN}bW85pYX2dNcxVsndEi0*ayUfE<)mr=>pNm^%9mD5KMpYNbMv!xU>01NN!!ou<_HPE+c{2Av;#{n7ktYx??_r8}oAZ4N!5GM6?Z_E%F>Gh%-=JT;@sNyAf{5mc%1s2Mqx8jsqHeZT7mknq%u9<czPn&Xxp@KS>{7=(lxtHB^7)L_R8A)yA#E(ifN*3U%<sLjY82;ip~*#iOlys?1KPoN2@F$4Yz=%*RkwgK)mZ*%{8H&0ocvIkt$3{&=ii!5o)MUJ$ln*NY#l5wl#ILB(3ahzi{%s9@m8fLm<^Q9rC&o82B_d%yyMKtX`(0DVbiKfHmiwcN_Y7?UAj;%_7G~Mv_2#BUT_UQr9bjQ^^K$`n2?dQMv{L^3k<A={b|8E~zZdpHrMjq&<n*s9lhex^@Kuu?7x*0%Ccg}P(Kpf}{oB_B{XW#<Jg=!OY>GO_szMP=%te&qZ=JH$z5YWol3UH34EIG$gmYicLOU|*BCFWSl5@9T5$t;$#MixgpAQnqn1B)fCdBu{}ykbdfT(P7ztyt0;LM&+wA(pge4@+9Jha(-(h9#|O!;;ppVM%M&us*615-cy;WYo`Wv(9J0m5}8{tMOv9EMFvFJhi#a_dx^N+~)hBu~~jKk~B8QR3-uL*kDC>0^kAdc@qGS4Z6J~KpxQhHv#g1-oFWu2ei#ifIK!B3q{U9s8cRE0HM!a0DM>uzX5&F=O*_#o0E<i@W*DPV+Q=OIhm&cfNU&n51dl$4>_P3)hGLVCM)~H!WMuUJ1cAfwY$6J5F-iW>AV2cfb){?lLoXk&VVhLNoGfdCHuo_B61zGvvMMG8^eB$r)du$<LT6pYZ*8-<W>f{VH4P}e1iknpx(X-zy|d8O@KA1w=cO^q29jaW(9itX22TM+qVGLpgy(**t#vRIjE$?$-N7l+o<*mtlOw5=nA~s79&+E@NQe+)!qio+o+A~1`ONaFK{D<ZS-fd6U#RGJK2d%+hSy)MmB8=EWOx>Q5&_4-H16G^o-qzIU6-!U5Py#HAP*CB^z`_U5O>z0*@6oV#-FXP&Z=4wy=YRjTo^}gW;VxvC-ekPOR7#c5bnQ{XV@`1mQ{R-9Eim2H{ET%|5+W2;oWVtv<b13SntSJAHbu7{b#IHv05lIfSPjZ1d^8f(TDL*yYoEB@v!>u*s+QiXtrSXp2wpl|^{k!499^D~#~Iv3i5gv(j?O)}P^@o@DQz?m<`)A2=R_72$$6iJBKI4_?g+8UBThfMNQ}FAOT2w_g}zSo0V`1~VWnsO|M2PTCPj|Lb9p8~q5R0XAhL<21sJ{ICv+w7{~-si?U%O|sMs5?Uid$t>5N6i#^B0ijsh0ijsh0ijsh-!8W`h|asQ6&;oPpj;k@c^#G4LAgGT!8$5$gK~SGCUv}$+6U?WJmcvgy)T3GMZVUgPS)e-X&C(?fs1#t9tX<9K>Ms2EQ9n_eBO=o;G=XMrPK59s-yO}c&`HUCOLv1haXq?Rj3|!1V4^6uK4GvdS~r%&0nSJ;WEH|T=c0wf9~&U*JWJwX?^wOABP{8ecEQd{NqUDx=;J8NgNmcRrDULrL4=i@UN2hZghelr9ZN1=ZDheBt5R_tE@dp-*p)m@m18`R6BUUJ61NH1|BOLPZN)oji-^v3b512V+G4;<Vmks3Y;H7a*q>jr$NUFg$p>x%4!Qh=bd+Qeg+LhPF`F9J5JPEKsQzbT0l4Nyp{7aXbMV%u8(gef}q5l*cJddi5ZD4fM^mk5?cV!u*AFLRuK^m)y@EEsCEHNL$wLiB-6O<JDwdqFmID!<J>7|u5ohxG}bt|ewu1vyj!~uHC8s2h8icDO0$X;bEsj(3h4`I1qNz$04o{#f3E;SGOXuZ0foRNvjPgqMonY@A#~BK050IFSpi(oWwQagpzCG>cmdbV2JnKen;qZ<T{k<x3%G7}Ko@Y`>;Nw4y4mmZLU9UeBrjOXk{2vx$qSaU<ON4r<AS9ualulSv|uS~Sg@ouELhT-6)b6u3YN4+1xs3^f+ej<!H|wf!IIXXU`cCEu%tC7Skf93ENM*%mb9h>OIlNcwRuTMsI$sfLEVTIil_OZItE)BAnFW*Elm>DFxb*0fzsA~_|so~<b1g3;U#Xsw7q;EH|h*)=72k@Va*(H$Ncwl9$&)=%)rY4PO9TK9?(f;f9qvHCl#Iu6o4mGo79R_!`CSSlsdosj8unItNx7Cig=T#p{Bl9EK=Vq7OC$Qi<oJ5UwsX~+C1->plb?hj=!n)7}F@!=HOQ&#kEc_okpYvy_i68ZJXgzr5ULiCRG}Ln&VNW`KQgWs0#R}85UIm|InF9fNk1y=hyQ<nsitW-C0|c4ooXdfOL%cIS-_<rx}J`5%#p_hF%f%81r);Nb?QNF-(AH8mnm{wIas+oCnf)(_ryb0({e;MOg-bL!Ud}2bS&ti*7yEz|vo7ch<myVujG9P=}?l^**q4rwmzxN}u5#tBIu>?y(wJx>G|PfJ&cX9~%%$H~eD*VChZ`c)%$A`Nz5;VCk?VoDd62p{$5e`g4c<2vLlwF9=w=VdWn&N{0>Yq@a~P_W~dVMxrhNOK70t0<Z+;tuBB{Xf)<>pGwx(Do)ndDo)ndDo)ndDo)ndDo)ndDo)ndDo)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)ndDo(5{xn`7|Y>p9%WQff%LXixyL04*Uqp~?!<C-F<bh?ibMx5Ju90?U0g!=@j!pSZRsKS_@gf3TTj1)Pma01u@$Y8(B1@+<5Krqr@OM}eF`GoPCS<v|eogi{P;Uw!t++j^n1{C5%_(d23Bjqx{5bL8uE>!482VAH;4VWuN@yFA&Ge9OV?F^8~?o^RTFnOA~Rqq1|4Be{t`2=Qe)%!&9Y+BAkXfi?ba+cO)LKDM?NgCBAWvn!fjFhp$G%`}gO4G<l87oaAD*#4d8d(AOLDR@ci7HJaBSon@`BQvHHK~@g<_$|)^M)m@3B!<%Y{{0_>^r<rxxkl<26}a1Oa`6kIxr@q!EY;YCZoY`E3h1czmgSrj?rJqMqJ0}&txOEWAJyf5j!#ZL)nR;82zQ}#8PZwmeD)06tlDgt1v@5^a``I1G6woJ8%oLv;(^^OFOU&v$O-dFiShI3$wHXyD(?%1RH&NcuJ9s>dTazoRok7671In#|T&(RA3&oNi#4g!90v{qZ=61VB)DEMVMHe+;89?Be~PSPmat*>60US(Zs$v$X?Xa4p_j@4q3p`4p_j_4p_j_4p_j_4p_j_4p_j_4p_j_4p_ihI{^zk4W6rdPt`0iC0!|C0w-K4K!W^&4F<S&ps{e^-eFECSbz;qCRjub`2{BoazBA1+sFmQ<F`YyTIlN`=`0Ca1e0`@L|q}tT?I%qB<|=LU1}uisY%Q^9{#p6y5C^Gt&HwB@a&MnPW<B{rJXFuu%Oyb8j?tgJKc=IZ>%@IYi&N}4IZE9+hw}V&8Vws8I<Q_)YX&*<@z*9?)1S(d5~_;r4KbUsSMJO<EqZmb&!6PR>i)w$46+xBW#az1CPpmP~IQM#~qc|LHR0~?oLhOp)4+Kqjq|(efZ-hjcfKQnvT{x);zA-tK7Ls$!Evm$EAH0M#q!Sjw6jL{VJM{PvW@LucGO0l>8l~$EALiOn1Y~>L@)f;j7fS8++<edR)U-F>^Pz)T8vch_6!S?pz}t7I7XI@m0*+9qq%%Cx2w)&Cj(DyI2_)@m0{=9qq&BTgDYSF=_5VE;l{I0)|P?3nBxCNzZEv1BOXPQC`3>$*9Q-7=}ux`wWvDt0K)NZ-u9&`w){1v!noG*gH8TfCUhfV7(!Mn0MaFhG56Yor^#w!J5Ye&?PyxOaZ#Qm1&m%<G@V21Q-Wq+9kj^Fw-sp#(|l31aYj~xd3sj+_?a8tlYT(alW_Qxd3dk)37TmPXg{S0`CIuF#_)b>@foG0_t%R-U8~O((8Tdp&?l7eVQ@S%p#h}@YtjSn#oQ#VFzeKqoq1PmJHi1SHLV(djrfu=VSxS0%PhnfFe%ZTYw_;eq;kI0zZZuU=jMs+5wEvZ`KZA1ir}~un4@2+5w7WSlz$hr;9R?E*hbWGRt}$a7SThM1VUAG}5m3!J|y*#|;3aJnzR1_@g*yXA(ckgnrzJL(21h+z3O8b@Zpnqrg+N0?4B{=ZXP&6vq)g0}LrfQ*neLC@btNtue%s))-<*YYMTXHHBEx8bT~-%^;3+z#x{iW)MeOBS?L%`lP;AeNx}6KB@0jpH#ybEI<e<z1(Mr>KOfMh?t(Nbsk;wg_Eq6(H)LAhZ;AkVU`@wMm5ZmBieW&RgF}hc&Tcn4#k^9jU@HGLX`SmAxeF(5T(9Yh*DoHM5!+pqSO})QOp#(uPaYdc1lm4rpPsUE2Pn;O)xJD7^giqFAET-`OPL>4=*vO8QCxa2DJ&<FaZv==h-j;4ZZPN3cw+lj938w%*Zc{ILHVvj5uiin>mlKS;<LIj6i5cgkpq1MucKSKySPna&psHRR}q`X%q6CB3^3G^PD1FdgF6OkgB~{_|jf1d}$N9lgi?hy!5Fa_25#fzgF^MrBH#3C>rJjDqy-(wIiviJFfEWK00-$8Bw!ScM6X*7InwpxdBL`(Nqn<QD@ac4Zu-{)j}13Plp976@X8Ng*FWUPj{-E8o(bqK@FfyXB9mSpiOtG`2wV|)@uiVL)U8u@Y31AUI*+#zrr1`ODDHfCuz+j>m0uqR3o#pz)gT7t6}^W5Xd^gqb4Ac^|?h&Kq9MQS{J~_I>ECpfROdMWnBazD<flaHnT!w+zPN`onXro@yGhymM6lG)wsY8=wqE>TM|&nYPgmJ+_AC`eFfNINo(w|q&0O|(wZ|YX^k0<bbuL_w5AM4T2sdMS}n|G_-h3)L8bG3n4r?>K16Izq_(Dr%}LbO6tT^&S}3GmW;2Qw3M!59rceXNW?cUVyn&<}s)b=Q(oikT#%|t7oeO*Hjw)NWSK5?2s({(p{R^pp+2A2R=~Je^Ceo<<&TC;E&D)C|&D)C?JKKvFJKMaD=6Y$`f-ZV?=b|SY<ukkE79(M3cRF4q3&FTDaGpXF#lV5e4vk5`fy(~;oOL6oDpuZFfH_XyT0l886OEL*?97{kl)BI#3~4a3elet`h5lqnEerg~kXjb{lOc5~?7i*?W~eqP=%sVA07!w$XaS6}GmD!AAPSA-TmYi%tjlNt{&36R%SYufGW_hIOC6kd2I@+1P+JFva`d@@w+c=4>%dWtCi($$6&&bC>{V!>-%8Bl=<j4BZgKR7vJo3N7#y|{A2>@p@PV_m10Og`JMee2v;%`TOFM9Qv$O+?H%mM4c(b$vk2gm<@_4hf1CKXHJJ|K7g#{8r+2q_GX#hyp1(F7UG$EfQ0)g~Ao+Sc-#P(Bg_FzQ?h8*BT1%@EtL<NQ*kY-<lojWlDR!GK0*m<Y`9jtkb*ujZh4B^3vTny>qg<k-<n=yX@q+8jX$ACD}iw(<I9Qn$o7h9IGIC7Rv-%HbSz$bZ*0UP6!Y}Hq4K*`otsR89_@FK|Xp}~tFmxl%)f?%G<(Rv6}V6<K)oRX~)qkvPWb0dNfXrqj%gZh#p>VU?i$hn@nhayXQ=y{Ah>8Up^a;2xHzNCd0KRIdQP0-dC5d{6M5G%GsEpiJX2>Rql@o$&VJ~<4q)IoVt7+`6Ga(x^;cU10!^5ZPP^F*(Mbbl^={Pk^v^!i--@GU9(AiX_JOgl-}Wsu%qOr1NAo`%t{f&jTA*Kwpgj+AE2;kbHJew>telpdGwRVpCfq3XDRuOj~@B@P~kA6NNR4j@k)JdQLj`qXDl;<)M`#{!;zR^zIF91D2D!8We?$FYDXL~i4fzKR9BaWH$79@p@+RKWI;9e7qMU>g_lv{b-0F5-!)fH%)IG`=`FfEr(%96*gP$*Anq_>!FRON}qdDb&;WLZtz|&@elIFK=bp5r%<Tb_80IQ)CxFOLB_r0&00H%WeU5lZ-;YfLxMM=og?$ati$dRCz0oa{){Pv-%dmG|A`+3YaE2T|oiVSUG?J)L1!y0n}JIfC1Eee>s2}Z1Q`iXqtPR96-%I*)c2A;NwILYVOI7iJ0b|3{CXweeTIlV1eeI>;x7BJd+(~xD4oqzSRuq23~h$05{ela{w*b@v$lZVXVXKfMMW`O#ujFB}o>*DfE7&08pV9LluyUH9-|%OLkoP0&IczPZdy$wZI6%&;<slq!<=u8av8s*ijrdkknBO7f?+d#qiJ6&{5zQpx=j%;zZzT=qOGCZU7zhu~)zug?&y|fEfj{zy>&@z%R%KIHMTpx&c`fcD1kpuqf<mVFO@M;1T@}SfapM(jBk_{9^9_CEzD}2k=lJ`R@Q8;C`?Jcz_$i4sd~f|MvU1P+u!9sjn56SXqCX7p$y54GdP+pC*Rt)COu|cp;Dv+~9b5eB_?Sn!*4vs!?4TAVz(!xTHE2iUDC%r$8}4j5@z?B?AnpR^dtpRN_sdrjlwDc?M7d6ACkc5|~h!0hGXmLUIpNUo0-EFBX^7{{Y1$ZB9>bBVc2t)oHS!()m8wQ0a7^Y^d~dpKO}rv8l<Xy=02G+{c?{xO@gY!}6#);+X~=L<!KemmEY1`7~BnMyhHXtl%Iev+R|xh-&C_6OL&wRh|&up>s!Wbf`AD(Rr2#xT4D(6x;XnAAk7pvyZ%;s-Hj;Qe$;N<jM!8H4;8DWBdL#lV8!nw2GBJCl?vr8g(bwM$=MvdY3gV^%>bPnwt6x%j*09lC8Sao~_xc&*;w9?9}}*(V~affYpr-?triQj1KOAv*u4<L3J`6TJ@1SnLfk3D1fauR&POtG~Mtx3W%(;&;(LC(~U^+fU`RMlZS9tf0&6)IO~m{R7afE9T?J_)hA>af2r{`6b*+)jLc9dAtJ1G4q-JySSvh!0fe<a3>*gyQLA;DCJF25(*uTDjnA1zsP*9&2h<6(sqYAno<2U|q?LWH2p&EC=@0~3ofFvrfmSC?CO{t;f=YU^SI1f}fEpN>NqVtYC%G)3n$^kO3aAFASuOx(R(9vT07_Y5>DvM@1qBJ7r8RUo(i%FpSBz~nbU3+)nmMdoM9msjE}~`)D;H5S#^zX-X~=jXybx6Pc;SVly2qNrfI>FI^ev!}%_$tx@Ug+#WK!L;IWArSd~EYAiO4<JW?2%ETQP4EHLq+=3691U_PaXOW(K%IwaMYjHY0sI0GExGCz0b7n4n4yOSb<2Wj-&)5^BtGVhJ_oII)D9a-3K~4LMd^TfI*_R{WtR9vIeE@6(JiIp=XS%+LU|3Sfo?w-rD$RGXZoSV4IK&R9Wt0nX6pCWk2~x@|{iDVDTm6Gu8=6H8j7i6yPc#FExPVo7Ttv7|MSIMRVt-7?F9A6(yfA%TI9-C|YWXeYbnVUY&_j<mc`<pDq>S>DUq_ilMur2vrRh3P8@RcNpwL6x-3xKh@Cl|(LiFs-Z-mpn^5aKE#(1N%EmJMh1=v;+S;OFQtjbF?F4J4-uowzISYXFE$faJI9w17|x+J8-shv;)dW6OT|(m97<m7$8V;ddxL>B&*3>Q$=!2)Ibdh3@Sq=bLkz!(DO3{e396ZY9V~#gh)o<kemw3034E0lN5miwA>~Ywa%(oQRQr+KDwlKHbL)jQaqceSvD!3O>fy{lPjJC-IEI;4rni22ysAvVdSOzs+sOYH{JS$anr)0yx1v-Wtgi8B*Q+24iJR8@pgb9(2f^)%+WA8;4ufI0Z)E@5lc{0#ztTw8+L&aOi;JYMrZ=sZ8ky^)GW6XoS?6>6N1RBf}#_E$gs>|B?Lijl~+O#nbG)4z#uakUkMmwcmlr?GJu=UO2~ljJ{utey8Rr*zga+Ey~L@JhHV>^Cq){zeNe7XBm7Q($M$8AZqKC;x7R%l(vQ>4&eD01UY{hyu>*kPBb4D0wx`)y=XX*E>HWF%;g{6gAbk~Vct`uNsrEi<r{^#Hs6DRQt0==sW`M`x$EAH0cgWoUk0Xss{VMzrPvSbR^{Zq<YDvA0YyEkY;aPiJ>}h>93-mbrxX`cS4te42ainqGU!@=NNgNmc<M_k#&uU!vSMi58*y||$k<B_k4sAS2k4yS0{Lnmo`0|0TYfX>OG%o(D(8L>;Fzr6}Sa&eG$yQU5lfkH|$jM;TP~>DVY9>lX4X8$<<djcp)JabDq(+_O6gUQ`lbiy_0CnC95=;PzV31$}xI;rX7XUcPspMV&?a&*G1>nwG7ZwY^A}8%JKprOzF<=}g4KY9*D-AJV94iemfE+6gF`yjl0w<uA@9+LbvyF4dqT$6!4%G0HjX%XSyjUmOnqI7PZH+H^{@-~0KH+5RPrQDgcf1+YyaVrfI>4Rmgf|5kljob}cYr$CGR^M*e5^?fSclzCF6d~-y5kEN=7pC}j&{74PmXrHNz~lq+>-{_lbur|O+DE;HPX<Nol_&tJb6w_^7e&smQ!AFdebCS9H%#pLdCIR(=1eG*sy6PD%1O1&cjP?Do$*JhN3dVh)m<q8<Up-G8J|>nE^5tXbD;XGL;zyeE}EEe>LavH7ymRsxg2im{VH-E5X>q0#K>Uuoez@2u3Rw06@jL)D8fs%y3W%NT|%P$nE+GG%yvz!zBQwV)RM|z*Hu*O77pf?*>hinw#oFZmN1r$xU@er?TcJCr4A`Q=QQ#tnsNDzdTJwmG!yQ`(RX!D^1Nqb%xh>z&zD(+76hf&hTsw*r&dLj1_QEo$x&?`m{SBqiR@)2V`VPYcjH=H5pmb8i*`u4Mdi-<{?X3V~{1S`Nopgd}B##zHy{AuC%{b$xeH%WT(AWveRBG*=evA0vz5@X>fScVDSSuv}rHZK9GZ(#%dqP!3}#UD=OKsG8h9ec`M5>0W^VWc?qCNgNYHOnx{Q4N$RL%hsKwZnw_`eOG$B0d#|{sy;$7SUM%iuFBbQ-7mIt^yyBkj6!&z;qE2&8pMCjUNd-_h?w%_t2(o5Svr#uHuQVEU*a6t?qfwuqJkajbQ@4@_8ek-E3N<8k<Ayz8r2dxaH|h84Mk7YRNRD*CNS3rlBuiRDktMB}$dcBmV@Ye&v7|NWSkfAFENRU-mbAv4{#wV?>Kxxxqf}>|lgZQw%)l^0KrbshG6L|j!awxE-P5xSzm;4<t<Hg$B$U-U@X}1OIxb=XldP<_juhOiPQU`Gx>;e*8mXvRoi@IJJgf=IfJ0U%Z6N@W)oDfyNQ7#WQx|LU$r%it`~{H7%DNdBKqjlxD5uF}b&Mkyz$q&{IbQCA%I1JdF=}I+AV-ZOn_<PHaRlb#fqSM68q9%vCK~7ldc!x?bOc;*HrO#iFl2-6GUWb<K6eHjvawE&49J82{K&Ns{r!=9As8r_0BdZ}8;jfoZH^B&xfa@>pAZ3$%}81fP{Wv?gt%jKBAo;9fFDN!9>)AE2t4TL41mWz>!1QK$L=&6Y3SIkRvbwkR65<q4i*D<mX_GDzj7meegugpFhn!m$CDlQ_mJwA{b3m}!Ib@l{vLudFocw#%ntun$^d29YhO`c((Ysf1T3?^R2@V*n06zcAfO!fS~gUuYem8an6tlBOGiq2cXm8NN_uxz4@OFQccYCVK%RX@iT@AgmB7#_KyX)-7AHg?@aLo2D{$yrU~$6=Jo*;H?>jK*V^dO(#@2yL9}V-|fK4C#1#ZNqkN!+{;?qZeCp$6VgO1-jap0rI+#9jrqb9=}vE73%!yB>PTi_|xO8oSw{q9N}^%iy(uo6o>wt|+^ln17I3p@bWh^yYh4m3C7s<%KRw4K=M(cj8WeD#nG@JTz^?-SgB$bO&T2GqfR50e~$sU1yn1g3U41QA%)vByRxbufT3p{i6YP8yKmgeTN_%w~K+UB&Rh7t}C(3}B7ECkyHr_OyfD-qH>>drLdm>n-hIueY>=t=`fOc6v)Y*y%0pV57IRgMHr74)*!{UgmN@0r}yrj;<sL@PPSWR$}mW&?Xixpg;pZKj;L0{QShmpFThG@uwMS$jF~Q`9g?+KKVkBAv1#;<k6p>UoSUi(x2h|BXa47!LG=CAG(es`+Z~j3v=VANqfkTpJoIiLw@??i4X;S@=TB-KeW}#ge@{*i<9>D?XpUf6BM^RC{IdI+{&O_A19w3mFuAVI6(1KTe-DC+Q?KpO7}tf-AJ|L=<6{0v_!SzK-)0TK5GW|LHa65kygI$%P9RgNb#&aF5Xvz6wkwtD|}Xv;(4TT#Xk>HJZq0@{whfE&Vl>kd$Ny<{&|w(S$kaduO=y;haZ>ytR%(rNaMPHo}_rz9vA-OB*o)i(w1@IKTcB2C+UxD+WB!v<57BC(^pA~(8IGW<08HaM4W23U+?pdlVGTM$4M~MyyGMoYTj`Y3^ndp35FVXtOP^NGRbL3)buhbWUlB((3E2ZGzOTHoSw)4bCT1l7%<FR;g1WTn`E?025^&LEoB05Lo*o@fSb26851BJn8}y`(j>!MFCZG2$(R7qIJt=t(m1(^5z{!ii4oLH%uQT%U8x3}Jhkz+-RB-Buu*f56WFM^#|doI++zhcYVNV(1~vE4r(W-K50%~k&(Im!0MEbx#tq;M&G%aY&Sa;Ra0SdlGw@abE!io744}oDpbZdAc1kS+GNBW+12nNFXa}G|Cuj$x0#g)s04mui7L7m!CN%DVQ!=bx-0!0YjNk%nQ5?5Z4Hw0!oz-+voYGm17lk?80lKi1C0tm_k}WJ{jTVk{Ko*v?CJReigM}rnQNoheBw<Nwkg%jRI#|-094u)K4wke=1w%R_1xs3!f+ej%!IIXXV0~02C)C$!P3mj4CiS&ilj?LgXiBK_3qtCBlBiZeNWBjh-V92zs8%76MhmK)0b9^1$p9`Y`{N`7xTvr{HUYY*@DHB^@S?&T+zj}FY8L<)^_AO|^D}4?Ib<*X<UgZ-odyx-19Toqa|!)z6#yoc)p!&DCNQU!T(wmAXEnKMsq?N{zWhggT~5-SYLfPf>6vDo=9r#o*lCXGnWmlQn4W3cq0-BJlxZ)So-Owwr-9GpSy&=YGrp4Nfi&<mrz<1?9vE*)s!m|OB`G>-jsbMQJ8wk?lB$yijnzoi3DwSki<)CL7x2zo?<E5=f{~6HpirA&a~L5JOe7@bC+)@ZllEfy$@iD+r%9+!%r{0?MBTc_kvK%9*ZVj`WBk_pIMf|iGL1vsF(uQOL!WxT4?6UzcYro9GjRuG(;c(30Bt%#=92|nz&7-`H^4TXo%3!0S-Rt*79dN9$6G5v7W&*PK$gx9zgIva-LZsU0he^c2QK1~{@eyG;*kz(#K`3l)oy@CIxOmG_Yq?y7gLQegrzJI!cvw5VJS<1u#_b~SjrL~EM-X#ma>KiM>>E9OIovoC9ToHlGfy4No#Vjq%}BL(wZAAX^jn*w8jQYT7!Zi9dUvstvSJx)|g;PYf7*_suB{m_pH)1Lpb?&njxJ0JIxSI{+(tBEB{VI#O9PwXo|36(=<j{sc8X6z+@`Y)w{t)15!_7rCyQh5-Y?n;0hW(NUBS$2_jc2bb?4DFP)$TfQA)k7LW!^XIubjI4N}zYQO}=1)zo#J{Yma#)@4Qz#5xlil<@2%AeCXVdc+hp0M)gG*DRibDAie@HY(<?4i%n5-8qDgz5x5U^E-y4j2JOxPwN35$>Sc#1W0gixCgBx8lW!SDF>g7Ep*4%@$C|ZWtW}5VAva8sdDmzhq8B9MX1XPD32hjIg>0R*bN^h*gZRx`<Ww{~*;I$Iu$b_Z{5Az&xmmEYy~VzUjnF&GORKZfeUzmtoMhlPtqtZL9X|@iXbzfeBF=-PGWWHF8&zpqnGPtnnftBkMGp$48oi>CcgL1>@IA`hw}}B#psd3TI?@X2ozuhGz@2FefD*j&^8yW@!hOXO?zgd1h$`mS@hp3>Y9i1dr;#L2?3T0w_o`0%rm`fO&evYc)Lt4`3jl((`t-2nv!D#S=k6nvum5!9jAucp^GTP8d%_2gwQJiRd6XVLTBYBqI$bqJ!kbs6=>>oEVh|50Vq365&Cb5u*}u0t^QwttkiXxSbg}qb94LITLE28K;?G14_s{HOmLs@HD5c>q8Qa4bP%~8ah+R))kY+hNsU@_#s>OSehH2K0k47&+OU>@dI;l>?n2S;pB7_KZE}TmGHyUe?cW2k&V=b2qT{T16Fit0vFhdY(iix+lu@@@RK8+pyJ43olXn#SkKRIRYQ`<>>4Z)bja`?ED>}-0eENaZ&y&B8-UlAJ}A!#z-!AoD9;JNYs)q$PYS?m%RWf==h6qXOv@m>K9@fHJW?8@x96dAN9jCB?~gO*j>=_FzKpYj1$`~mQ9C`I>|@bgOXFI+%Cn;deJzcv@hYrtQe4_`_;JZzCD`$}wBtzQ628i_<C8e9;j275SQXjwxQ4Id>}cg;9@p?yR2{7@%;Orq%BH(<c6pQ@7x7gz-JO>B!y?Y(BEHI|yQ6*h80U{{sQJ0}VGqgUBECwe!}el%T%q&h>9n6%03${^T>vBOFt(pIc1a^tI^V|;DxL1*2$f#$<4Ag`>T|h|E#x%vEG(hLIg30Gq!}i`vfKqQOnPqZ6(I}^Ya|5oRwf$381lo~5VknKtPMd7&8;I812f|Y#lXxsLNPEij!+EEULzD^<<SKcW988W6l3Ml1r#$ekFI{9Ygr}A7_o2x${4Y50m&G#Z~@5B(4cl7WSqpg0A!rRxd2d{#JK=b@+;fq`4Kd{WWyOKU>7GGErOSKrtbU<nsS_Uyog@1<Ej+!3ym}DfLOBQ*c1>;HXNHGWTDSp0khEOt^itKd|U<00wdlkK$gsoxhf!*%#OJTu;llE1)aT=IV~@ZpiF_)5#WxfOejtXpys<n{P5GyKcI(~OjC@imw;)?grb*#ZQ#6=`)E_x`CtLWQjAiL2wBR6N{$F!(4?QGHIbC(H6js^6n0uv0gtdXw4Ht|nn#M!<{a?|${#yRYaFqpHH}!(8b&N>4I`Gch7n6z!-yrVVZ@Qvcu`-gGpVoDnb26Sa-SWjbiNM{PMBB#4^$f5*i^?|M^nS}IKYf9a=bV$a;@Xdq2>!11WE37s^bS00LBYZkmORw%Yr1AI@TlxNK)S`O{wpdrquUJQ|gPQDfPwDl=@<6N`0|3rA{eLN!d9cc_r&EK%3^&!$`Dg#@}?BY}$mX|A25B`CIq=2dM;{=KMV>`KG;8yio6RP_zCb){sNBGr*b#|Ju#~Yu<V-8SqbIT?rZBPlHVf8L$nD_1e(^3w>^Kz%uET7yS$xdm1wpBPTJ9Rp5}5n71PQ$dL_<@FPbyFkX+qQG2oCWnu*0?o_<=*D79Uq!uW7=}s|?<e+X?W(EAyStEJ7&p(#3<R42}VvVJ&sm7AlP-97Jrm>_os#ww*RV-;uDwebc6-PSY6iZs;hb67?!;;qcVM%MMu%tCrSkjs*ENKlDj<m)ED^^Ehf~71e!BUo#U@1#TaFjJ9SjrL-EM*A^ma>KfOIkyMC9NUBlGc!5Noz>3q%|a1(i##R=>QTeX$=XMw1xyrT0?>*ts%jZ){tOHYe=x9H6&P@mxP4Pa3l>VVKXc-15DTqugZWEHp8hh0ENxIBCm3E4HKJjLtcrKi8X^7E;hsIGop*lF#3$};)OR)N=m#}Pby5jNz_QPJvU2@ki?1ZikM`ZT^LhPNs06B3#u@&CNbcc?Y$C{?Zpz4?Zpz4?Zpz4?Zpz4ZBB`a)q=CnYQX^|CQgQ5fJ07(Uw}jV1nbiPi+0w<0_@uM=bowo<Lri`YQQ-A1V7b?b#~UnQUL1gj!93zF;Az4)QG^TAvGc}A(51b?9eDQ1Ay5Lhtr5os5aq|9XQCWh(>mUsa6Ch^t~<sPIkjUC}0zqg17)Qp(%(9K$D%Bzb?RUZGnFnf!i3Cl2gfbj3=!f*DPu6xaLR)j%${*c2cvXwU?SD9k{1i+JSqTr5)I(S=xbrnx!51qFLI3Gn%Cxc%eDkkr$e!9hjk6+JPIIr5)IzS=xaenx!4sp;_929h#*b*r8ebncm>jtdLyLw?eb2K;sGw>?*|keM*j81ObWsjaZ1IhZ9j3L4Xrc7gE5Ch`JC5(7ac4v_OCE<Vayk=2*xD@JC5b7x02j1Pq)kxsVKC5?dl<Kr_q|L4yQSrZZs!D}613gTxxxkymPh&DWXGL1JEtnb1LkCUP0zL4G63Ho}8EA?H5ggv`G8ps^LkHdTZNc|sCz#0hX}2q)y{A-^FeWEky9%)cJadqM7BY~l;D|4P{~*opAq+2my81jZ)ktQ}xNHnON9O2|$cRfGxD+?e#Bvb?f{novFM01_<i01_<ifDtV1fDtV1Z&y#5oIO{TL3vX4TuFoSr0ltp2jyAWbEOQ@v$E$(9i(Sv&y_Yv&&r-FeURQ~hM`qG`Z|n$l~2cQp^hVM<49@N9FD6u<v9U<bzHtzVRbmbuZ|1&Dv54V5Z-b4ag|@i)A1m@<4EJ8zY444lQ^#W$7yw^pH&@K{o}N{)A2<eSN-F(y3>(P9hdY~THTEk(xddahNp$q)sO7Jv%>1yxQM5P)wOXE&kw6hi!RsH_~NA1X?#hBJD0|nWEfm&d`YahrrxI)cFcP+;?eX%rSpAyNsjfBrk8hu(9Vyb5r)njfflO00BCt@?iN5dBt-74tl7p1kvos1F(x?$ZvnU@=8m-hZgKMI0&a2g=>l$X^63I@vGVBxaIx~~0&ubN=>l-E^63I_`Tp|hG`u+ZbQ)fqd^!y;PClK67noPp?!ya>E9>{+g-WmY;f01vt@q*Ot&Fu5z>Ae37r+ahx(&b!eeNAV34QJzV98tWd<Vb+GtG9uEA%R52fzaJ(slqWFfVNfzykBqb^t8&ihKjWLbX=_EL6J#V4>O#0L!cSbnQN{SXptJSgg1;jV#6Kfz`}HrPF<AVfj{PX$dVb!VO#(v4`&Dx(Ftqk*gq<J9lc43{a#v?Uw<H6sP?%KoR=f<o2gHt(^g46sIjRV2t9NE@;Fk&gp_i4EiA<ha%{)D>@V@hNnw_7{#$82@s>Ozq}Vf7{!Qx3IL;6$wiVG>T3li^|b;MD|Aj1gB3cbiNOk;)5K7ndUlNrb#@s@CRE`C!x6~vrcgr$42B~GCiT4nlL}8#GC+*#6x9caQRf%0WI!R+DqhI|O1w$bR8rYdPzF!}qw+F<5*U@20hGX~JaSJ{Uo0@GFBX{8{{RIh?X?1v_F92Sd#%94iZ9djVx^a9dZE&QUM9scCH)8zVH&7p*buTbW2e~=z|eR(LNGAejS$Q`Z+}OJDGe2}kSf_`6|#^jSsFD*s$^lz8>y0oF>j<w7DlX*Dp?q@Mv6_^i^V4G#bT58VzJ4@Xt?YYoAlR;P5NuaCjGTylaAhaI+cV-km>L&4OE+S_Q!a?&oLeTsn_rGNoRlQbpR;zEv^7b=xba7l63YL>I#sAMjoyJH99n&*Z^$M=iUHbz|Y7A=z{)AHh>rKSF!=Tpl^~ChtM~<1HkA`xs2uu8gRM;zUW3NPJkC3x`*!fiD7+c9+G6}jAn_IT_^&USRMY6EU`M#xSAza2dyMZtWGqpW{DNvL)H5%vCgon2%uthy2~|FtZ=uefGJkULJdF#eeMRJVl~RX1EyFZ)Hc8r>_@&FUu6Il^tmg53i{jyPz8PN0;pnTe?=4k6)WSc0-%C^Wyzt%%Hm-QfC@)iGsX5=HOS^ThiY`7(x8BJbL<l}J8X`5qK1d*p=E{Kxp=u%;AX{}K}{K(;XWBq#^(4#29&Wm_K*Q(Y=%2z02!NO4jE9!Hs8mFl!I)Rj}0jY@g`AY$p-0_V9DmVtOZ!IIqaaZWMgL?1WPu<N;;sD?ZtYKIr(s#Qx5Vp9xfZLF}qWOBEg0xa)CNmE9^^y&6KP!4LD97mxh-e_L`LYxIz=53cwZm*yL2?+5244>Bw%BL<QKg!`hV!xMg?htpaYL&s_kNz?827D1`kIcXT*H6T~W@ko_gon+j-UXSFaD(8|tgVJe`Noz=orKr1_|g(0xA{|Bl2@bcvXk2Gp8*MUnKeeMo?(&%%qz$uMB_X@1i=yPwtD~&$)2F%i+%kV}_&=z<~LySby0?+426$pNEQU`*cyc3Hv`sAIsnnB~}PF&3vcz)H1ui3(m%{wtRv$O+eGfO+LHnX$?Ycoqbur_nFBWp8DJFqr$w1dt5Y1Ukm=PdyRq#0o{0S(;nqx{pK|M=U#{^l=Vg;)IaS0BN0ou?NNLvj*l0%EYD-2!5mlI#|c!yE4gd8|6=ZxLNgNq>tdWBv>lbgcvP%FZX*0f|frb&QB4IoU)JlB5~gL=l?2@gpE7D>S{5oUA0%&-1H)?w3nOUkgN>lUT+pIa=|w1I}@@BhIn31I}@@1I~FGn%5o9u~O#(zL}Cb7cfk=I72fG)dsaBFoLU+@{xob7#k`dfpK|_amlkEOk-S<orb=MIiCIt5PM{HF^iBRKfL55w>0n-bcP&H{{;vuvT=YPVa3zm5aI@u?A91JSlR(MINA|6SlR(MSlZt%r#d-Fuhl{Mafr{U!KAf8x;~dao<;RRx;>XZoNl*ukba!1b(Y=+>Ger68M&rCKf*pd!uB{g@u1w7L3w{1oOo1DgYs3J9&VTIdDKpCzmxMbjEnm!Xpgq+_HlKm$IJWF=-J2ReHFBa+iLr`zOPdB=Dn8lGmIaCt9-p1MUqG9@k8)9Uhi}r+Q$W+9;a%awAXQor~U1>a(;&KV{jG3hdtca@ndk6#D_iH*N^Pr`MLICqg}^UewD;$)`M)?!+jk;30JXwH%?C4eF933hr33g<aoGi1WJyFyGEdQg3iv5AW@0roSlUwC^<1_=Yb>+CC3O~^H4I3@B<!t=hdH|L30y%_h)5IL(a=TkEG!!If()R93>-CAYh|+UjO+SG#ioEe^%CL<h=g#NSc(A6GIS?QZhW&0su;e$6CNYR-j+NKUSb$z&}=?Uw||d1O56J#u1Pc=%@L|3G~zW;{^I?`pJ&Rnx>lUc&urz$@AMe`+eBSRySwAk3QB62JDj!o4NpLvg1=1K+W_we;!_wPPTmAJK!E~5;gc_=r7U$&}7HYB|w@NUVa0d<GuU_sK=Vb0DEA*V*}U&GZ-779+<&M4t-z-BRR&&bIkGc7si24G2GfT?-Zx8NCQuC`ieC1l$Xw40U5#AEC5EuXv@&hQ=Fy@jXC9|I|_nBg?(QL4i)x&Av9E+v+w|Q%J-IM8jw&i&cXu_vZOT!S<)JVENP86j&#5@mb6A1OIjn1C9RRhlGaFLNo%AjuiZ>lr@B^?N_7ffHK|mm?p2dYb;@2ffzYR3?js0&>g7IzR3mOwBS>}9Mgz2fp<xR^i^__Z7l0PkNu&+XqOvQ!1;9duS5XU~h03m?7C;NtNkk5Cp)y;Y1>i!3_B0FNh05${7QhP?+S8D$pX$UU1;kLv-g}nT#9&ElVsNB2F|@l)K>z8(=fC*LXFvJx|MoUMeiYb9v9A+2sByvx9Mm-71P*GLumT4)OteFJ|JN_^UXA~G97z_<@!8U7VPz%;XkkrH2B1ObCj-)e*?$>;hA}_qfi!l|aJ&q#qru&(0Pe6Rr~n9|6I1|&w3l4l3ZNC3U|0aHzy!krU<D=^7QiYn!H`s`v=^&XzP}_ujW*pegwycSXWyb$Qp(beOVmm#Tf7;Rz~jU;YToHiOp!*MK0gnj-KU^#<pDInMAj4r804gA1{Bnttfv5jroZ}(E^wT8pV57eH;EdRoSf4Dj=B@w6u?oRUn)m#eY#aEM=pV^NenotzgO7O-z#kC?-jQ6IfX6VDQsD1+57``TG_!5;Gz|J@q?3}b%x1<CZg3jwvt4&&M=<WWW=U^C5Jz&WA`6`&dLt-3g8@;Q+PTo3_xdftoQ@aL78Z0X$>)!w5AqIT0@H^t)az|*39Ba2Rvd)YXGsNHGf#rnm;UQ%^#Mu<_||&Q^oe0Lkvul1D8e{4D&7b*<rK7F(os=C^>LzWQB=oR@hkE3_yj=31$sYVS^1H<Z6gMH@O<xSg!)P8e&tDP|q^`{gI|+7-mO$kztq}X-2kEIs;m8QaS@#pdVIJghIcp3*ZI#X<Yy>(BJj~fB}A77XS?OE4ADwhTW+`Nk$dQKF9075!Bdc_$_MW*r(fIH*%D*TLw9jOZFLtr<zaRm^=V6yWzGPFw8!~Y&Bq+`LlN(U-OO?$Qc07ltj(|eBPKpQYzy_f(CH3Kd+QI52R6vCWK~yN-(7_15|=3efj?{?(CN1HnJ`KDhgf84&)z@*>mN#HPfDO+YZ~OdnQhFRFtTa#4#o6kdoa#4!!%JswheYsP@K(ooQcKlm&7DOdye8W$s)HkW#7Pbgd9mi}xmRbtw&9T}s1xnNlOxAz3PAXl@-??V%}WV7bS2%`9D*bVmwbV76gLwk~6B;MR+^Gw`SD;75y09O~LQg-$O*v8e0VG)yKYbsaPyD#VwL8Xgy7OxMcsxDX3FXn9<SH68TrEySFTx`P+uN7u?9yb$9$XiZ#*a~<`-&BVLTW(=&D*V&wb756%uHLzk|*R}JnL*=`xBOari<s{>ZDgIF56;~trNC6j^5C|r9>ZIE#`~s8Nz>JM8d{V=gD(RCNo><Z!H9V=3{-|M!V;?ifjEr+|nSo5Vuz)v@=38vq3VoQg75K1dYfNF%R+z%1tssR-TOkUQwgMC;ZG|T++6p184Mz+XLhv<0pcPW^mf{>45PXe<SA`V3r2<F>gmsrcIfp_D(1kb>P@q<~kpKepx+T@Dj#_n+a#j|E)}eY<o3_FQCT)caOxg+;n6woxuxM*sVA58&z@)8kfk|880+Y7F1tx8U3ryPgeJ528KOFK*Ijl~@J5??-<+wKOX;OchyP0%aFMUE_+0CT;^@(n$(takrD*JHpUe43AhuPWBgrf1SoTn#>vlEqCEtqD~XJZf_v#QeE&!ye^gvC?sdGB>=yYHmVHqX27xpYHZ!<*+F*sV@4ozyj#c@I99Zis89%e)JpOD(KqHh+5hc{e|oY{<>#PtP>(((8i`r`q#gd@ks4!OG#O^t>0J%P(B8@^vab@5Sfh3l}VWol1XV2==Q3D^I28o!GCAD4l%pF7r-&E{|~ie&2Z}BA^#%@LZGW#ThoQ%Jkw4o@+9^IA)p^m$Qq5PEBz+yRfB(i2;)gChm{$fRd4gM7d3cWni&HxlPX`^NX|CbSeBo?>+&TR=1yk4!i#zV2<tndjLJo;$x=}jbj#R9w3Zk7HJ+342#4Y5W+Z%JAlG4&S34PFpM);yD1D~3LsP%#<dHyNCaej#r;Cl8WxdrEXjv5=U9>tWzJ#wgp<q{8FZ-hupD%#bY2cRRJtq&7!T)M3P2d&DC4I9xPj|e1+WcVVJZM^{Q8Y2(-X=3LRYd1AQ<1MjJW`|fx&kLpp7?F;VNk34Mn&L+IT~SszNs2QlP4kjknaNDrn;^<*5qWcuRGv!Z!X73+s~ECN%M6ld&ckJlSNd2^LQ_nQN$YSk5(}#ztA0Z-Ql?s?0Z`#x_-%bLiDOz&Qct&p5y@^tw9$Fu{_WqYz9m<mM>M5)9ck3bF*~f#(2<1n7b10E+}RGwcA11WUG!0wV#=4t9V>=yi91Mgp7F>Hv%cOS+N*BY_#Hb$~@I(lTAdW(6#<SpiEl6ivzq5e-$1GC@R3O`}W>vHq%hTn-n}w5T4JBZjR7WyFZ=b8G~J5uqs>S^kL@Q$B?-VtteI04OAyOwLKci>VP6D2bMW3Ykfw#YIwql32eWj#RirQ$-wEEwVMDOfj)t#Y=2g@e&(Wyu>;V_uf+SlA4vgq-G^A$zrB10}qu31-q3Z#DaVYA{ix6J}{6Om1KBB4P;&=S)8jB=z-~#q-M9xz0at&m)!h}Dq}2nKco5=Q%0o1Jqb?65biN$e=6Y9>e(WIlq_Km3jHKYn1jMQF!wM5+=01=5#SEYJ&XW%DrOUwca}<;L}qwUZA=e|u3wHkRC-v>JXAU_XC5kDmNO3xNG!`)rf;&`KfMHzdSFH)D3j?ChK9-AmNAEh7iPdYeIr+_3^)e{C}sdUFrP02vZ2v(8IVoi$VDy#0)p{&830fZH(3q<Y-rl!0KleiRIfGw0D{qg0{|cx4M<98`i3PmeZvx(z8+m=O9{<D-eai#cd#TP%LFtSN{eLx8Z4#7BL57QuvnRY27|e;j5UM7+gHY#0WMi3fHed2G)RDIOwux}n51P`F-gm?Vv$x@#Uw2wh)G&T5R<e_ASP)UKuppySD2(_t}sc<Tw#)yvBD%RQ-wuZ=7d~z8xdGLvLqzR6k$n7lqn)xs&GV#$QI)=nIdxiss>OilTAeppjO7#f--ny=q^vlgKGBxJ!qTsfIVQ!S`XMGTOu43_{f%hPy;{_8WlGH7RinFL6K<_7^+ETO<*`BnGDJ8CPQ+&$&lP|G9)*g49WE-L&ny)D~2)cEGo5j76H;Jmiil!bk>Hk0pvl6RzLpj@#F7xfanPs6+?}Y3`Xl(Zy@y3qV)zsMa5J{B~wu`6;jDmM715DBC1U`Dbd(HvP%iZ?vY(eFm|s49K>2=sx5O+sr}JrdU_dwis7@(^h`1l*&0zsBAV;x025Jd51`1Db*Mm5X=os0%sM=d68k~s3=g47nUg#slgU3=LBa`3#4E3}L<}izd0mZ&A;mYZYk&-q?8>G|n8aSMs}XXf_~*4~z`%_5ppiAQ*6W~iPbA)YU5)$)&14VyqDEq#$66<#bt^316U#grW!MwXyjD?$J#p8ArnNn>*Xt~0nVP>|2P+=PtWl#|!{(Q4d5W4DU)OMk$(*NnPgBIaMy8v!$%=#QUL#`<vqeqFB-pJ?PA7K3^!f?Vti66hHuU<zhN#uoPj*JJ^uUNFbL!+bYV1N2C>>!I2ZsPhpamvRI>IatVg>P^aSj3z^7*ZjnW-@e{SC;TZY)l=HLY$QvcZW4#*!UQt6vIauM>+$WLvvU+6qE=%Or+E3f_{`tB`^>y@O>!pxPZE1P@>D9Uuefm)rp`@bKl{5g>qW%pCy&>Jdyl=xD$sS>C|`lVp8|227F#9vm=9mUx_p1v|uu4qrL3qI1yAmsru^XT_1>A9@9oMH}2Z9U1mL3oLeIv^QxhqrE}9@9z6guLLSq%USL_KRair65`l*VWxa0<7q9I_FbHv;!IxKmtXww7+rjtDfer`98W(E^j$xb9_;OMdWvCoioCjAPL=aaxvWm+JXJ0;WkZbOiL~qH(uNqtQ|)=5Jr|?6#N*DNXwUoR`W(fn_PlqV%Ta{!kG-4sO1C-*^>m=_-MnAAeto*&srI~Mp36vt4A8rIhg=_uIMtqa$<?8VlL5)i`{e3S#M3#W-p~7_U)?9C+MgIl{o3fl)0v{)&->)LSj4rnQN5q{&2#aH3*O&;Iby6`k`Sl#6~r(kEh>oNDwMq{h~dbs=m}ytgJr*h7|!6Qub_o9nB6OE;S65)8eG6kP6yz^8LCJ%xNwFlQVlL#?V8Ey>1F;{8bUaBx*xuq`v`V`M{KPq^9arJBRoQ{n*a&S^CLV0^ZW>pI9UElfW#R}R5c)Rh7wf`NGutL8i=?muC;PuszNM=ltG0{=%jgC4km^GLxo4Y!DU1N5=%Cs0wnaR`{h6aC;9v3JmL+TW;Gu1>o?76JVK|*d%z<eezH%1N4&u>MuQDFyPp7D(5EB;xbTK8;Tl{}?E%0AZIc1e1?)KkpbNTsl>uGQr#l0>fKPV@a6zAv0^ou^C1p7@g!QIp3N!=@j)=?<nlVFwriow@gGz%*3@QyKF{m_{#Guk0fQDcwme8mn)Q>$O6CJ@a8{pBrhpiQ5&IoM2oJ?W_Ly3>Z8P#w8^z<@{m~Q^`R5F>^T2UsGz-lBrKqdk1Y9aF;RGZ9uP;D~r5e#WP8k&SE^B(z~T$mvuOkBBA(;JFGVueavg>oWUPl;ruCK^g*70QVfw)-ly1KR}@gP_2yM2bOTh3zyN^PqM~s465HcIs$66D#c0(Le?^4Ji(ZY{`}shr|kj+#1hBwrJ}CtFVl?$*QdaC$U1(x&|q*X##+hND3n-(h8%Pq-8`gNy~&{l9mC*A}w=A`V%TdQnLz?WGb={c_W#MEJWT&rXmZGGpKa895fQF-{_W;MymY*wMP>#$?^fUNAobIMpU3AtvC15SR}CtS2CxPET4T97)gfRyc&d5e`X^p9x*+$5!I5|T2bbeWSN~%fF)JfjjoYPVxQ~C<VtEdxsn=AuB1PIa-}y!*C;Gwi5yg5hF*2Q9A;p=UB8@VdRU7+EN2;-ZZ|Av85k@#EJv9hR@r30DKx<>12BQ<VHt1<eMAZX6Z(u4KqfHttN<{f$z&OT34M)ZKpj1^LdbwJOwuxBn51RKut+OtVUm{7!Xzz|g-Kcl3yZYO3j>>=0Jt!)jR~NhWPtk;z*5U#FcVjBVQAulH;|<mbW1W>iec@RCsRfuR#0iOd4_6}`Hlf5zLWWmq4p>6jOIiJ%O~)R=16R<D5J=L=q#f-5~@vBYN$3@siE2tz(|`n;Pe_~YC*A}lc7VQmVs?Nihx=MHoqAGwG8zFY~n)0c8zvW6d>AilP#VgBJCIw`4rkQB=RY+1M|&5@hnXSi^~}%!;KmMVyHBL7}_8nKuk87QpgZPwF$&zgI||MDAf}oJ47wn0!ST#7+WjK5Ca47NM$Sxz$2Bg*;1-36HIPb2%8%g!sdpBu({z{O>VeWlbdV+Mr$=qlKK=*DHV*)6<{f>dJh0gu~gHDz+#BtQ+TCD1fRk!sKKYoBDNGZVH5$iAn7vsj3+}2OTR0~6ph7{O|@lcK@oM+kM%N;6wCaaLLdcB(U5xAVwwC?5QJVgDI9@MH>n$;Patt2p*^Pq5JIoJ0}xWkjKNe|W)PFKj35?i#SE>hQ|pTALrj@>njczc+5;mSp>+nkc+Co}GuXvzUTB@cE?zT3>kM}Bnj2bIzkZO^yq<OrUO-3|fo$!ld8l>kefL!lwQjvPzG{$01O7<iD{OI(R(0@|lVu$&PS$lyp^B<6T8&Ue)gcXehkCShQzua~$d{lPsTndORU@@-eaMY!q*f=ME<9Q~r6MzkV{1pC>cl236NpJ#1`w09%pWFc89z+YGJTk&6|%5sYb0UPRzSj}t$>6{TLB4^w!#r6Z3QDt+6qOOv=xXjX)6q2(pJ#HqOGBWNn2q8leWSHCT)cYOz&8EfcMQ}U1%H_@mlvLH!*pH_a-|rd5EX>ro?X@`kR7k3)m!%8Lm@tG+$szUsH#9Uwh)ku{i~AnRsz*j=|QD3LAJ!^@73%-cr7xuz|PKFDPu_O}m*DIPeWO%VKfj?}5e9oPqx%iWoGI@ascjRgf@g-*>b@iKL?(;rp3#Se+zxsyxh;<LV%>Q{_BUPV2M2PP;&vN%xgv#6mZd9@a~rymEq@N!N<C3VtSiCe^CaD13VMFgyFXG`bao@ad`I{8X-1BhI_8^Q%+dPNnDlcYQeBRD0fo&xO-fDoi~+{k)r>3$R;Jn0k7udAF~YXBX%FzE+-HocH^4d3H2&F3$V?>NvYeE?k^<>eX>}6ZVSpPJAxT4x?B6#2D<?Yo81|ao&s1#o1x-it}E4F2=5z(TB`0mh3s1U!0*9Qsx(DC?}Np#TlvzWqfh4Y$-0s7uRGz-1HJe%yE`dNf~pfv<D1BwF$I1OAVX?EzVK{r%+4v)Vt~FWw0@&-c3&>LyWBzWomJ(2Dbyy;@H;H4nPacyz2n8ID@sG0xdM(jZljz^G=}_Q|6sQEvC#ng<4#_t-gNoR$mcfED?Az#8`6bWQc*w7HK)ezyPSU9AaqxQ@<QyOrdNtoY1Qtmct3X>H)xsZ-RBxYmgzv6!@h;4Am|GV(5J-fKXc9mjciQ2AUN>E^tk%0CJ(Lzy+WST<$6WUA)1?PC*xMaj{d-g=!A~U8r^s(1mIzfG)nGOUXO&LS$eGEBDnzxtvBsnE=x~z=RBy4$EOC)QC`#sU{c_RAi`uDT`q_(}Ws<J2Kk@L*R~rHZUVH0Ag9!Fw=9$<bqmeDlLNx%(x7ITWG9b06Y>byFwHo2{kr_C}a{0dqNa235LaX1xx~57ma{Sg2B{D0h3^HbyC12kV22Cw9F+YX&Fl_(lThoX5}fdS$Rsd6uHVY5iK>YGDSp7WUh=6(Xtg$=7?B7)fSYnL|dpWDOa(zq0AhSz2ZrEN^Do265;%d2doh-K6MIf#QLQ#9^go{mA-gDC8kzXuq3h>BoDA8vKb@~s3fvk9uKG_vRNLo&=VV$r^JTkDe=!QPf5+nQ&O|?l+>&|B|#e_FbR?@&Q3DEB#Zfyj4#RJy(F_qs_%_XcqQ4q(FwlT8d2t#WH7K&_$65ktQ3Ap^^0Igd2O;4!I1J=Q!6U`l2{Q8DX&ee2!@o`CRPMP%4=c1Bq>x$4GUFL!$OtRuu!E<jvlH^=~=csSkCF&E$8&@mUDVbq`XWpR2odcut2ax2&QL%3jn5vLAiuZdc%uMp%Ho;N!={HkECw4Hw64DG}0UV*%Z>C>3^gKwl`S6DP+;J88=b`+gmn#D`>%T935f{s!irbsCEEwLED?aMbBnW17M3D&dr78%rLAh4(SavF|?zJp@vnwOcjH{Dqe<)!7%?MGsU`Q>B+7f)GSkFku3(p<e7pNLk**Qg)s($)4hTirsPKjF<6M*fT}}a>KG{wS^K01z#8yT4}dk;9qrL7%-W_Q%Q3KN$Z`zKlOxEncGMvA8gSU~fIMLKoCoA#k(R+DTg=gAzQ`7DbeS)*#Ts4aiVR)1-Ey#i5rSZ{BEye#V6vim99kd~8m2U~faW)BZ79PBjCdrgE!ko#uE0mOSokUMkqs7p3VdYv@sgB+<oXUgq&y_s9C!$)m|9WcliaRcB)2OU$?eKTa>H_w+^}3E|M}%2rCGU1X;v;$ET0%<excG}wWYw%qM%-cUNrz1dewkV=v8+BN9bjD07qapA6afGFa(}de^70LBc>!eg-2kb8^IBpj7C_4HTT5eM}Z4d7NP<dmMlaCE<Tq2>g)f7lx4Okw%RYU`a&Od!Wy)T64s#CO&rmv<693r(Wv$ST+yg@2EJ%iy8vf2nr&8qH5#<%Ex_`OxyFWxH-_wa*1`FQOia(9v2Z4)XC2%HH4xV`8p$>g+cRj2JP=PaYB1ar7c(lJh>aPw-c7{FtTPxDX-;O;HZ~D2Gw2(eh?!XjYb|=>W=3ykPwdR-l@G+vjEZMsXhxeQgAw1cx-j4%<{TV2frl8o>_AM!;AKy=mGRyg{MwZ9-oeo)f$`q4iONKVdu9a~CWDVM-qU;8lkwiMIo6&G_s#<1+IUYp=0L`K$FeL2GTd9Vwb9<Bt&H|2ZDp`GX)A-hNn07~P1?#(Z_-vqdXu&?&|9>Xao*Rl^oqy`-LJHPB9`c$`9Kj*bWh@vzx?i>dRTHq#_8Tt@S@;?w^Y0+xUlxNBX4wg-#x*G7B}7#w1AGmq)=kz-3e%kg58~fmM9wBoq!fHVAxqe<(ycYn0>9j_r&&#-g{#E)#Tn2b1<4MNX)^kId}VCcNCEe6g0fCMA2z@W759wleu!tUFv4atMhdxpM8^?NyqilCm$e_pGl|n(kCRD!c2N~;MG(*&ZLJmsbR#rdU^?Ib_scPs^O_}KT|HNQw>j*hne!Zth*)igQwbguI*ailj$|gJNLN|yagqAC(`}Ace~Zyd$QWp&%5`z5WFQba;Mt!{(UatuHJ2#Uc>xFa4!08!K~n^^!!DzI{9w0RNT)yxLX~0In|zbaaUU3mFYFiUk2wg^02RZKYtmV3(3R2>is81aKB#rWS|}9z5HBAp3zr5%f9Nv{FQJnQEveOrR4<VET$MT0y&E*hKxYYVu~Rnkh7R#$Ou$DgKT<sk&;XiWYaT=Fl1{&k%pYXS45#9XE7F0XsG&~pPpU@A=9m&oJs*BQ!6T91fw?{;38+KpjLRN`puu7US=ZG&7Yo1W+YoH%8cX;{$&dKID_qvLO!OTJ%xNsL3;}Mn1c2cm~mA$)XXNV5}Ek1MC-}aV~N(2p~n)fCo_+?6lclI<1M9GGSK+?`xN`-kmGIJ6#M1OV{1YgdSIwx517XkeW(D9uWy##1IY0<v-BP?kEs<E=wWNQlVVZ@dc37jRUw)NcRvBjG2Z<IpvTsVGWB>vwXZ@wFl;da=<$Y<LWOzY5*?Yp@okU?&GZCA#jcDz!LqYRW}X0NUBOycXf){x;0OlB0XBkxYk+%b-WmX%&}eaj08wD?7Xn1VQ1`3wP_RsbE3gy(uy9cYg@R!cTp=Nov<yNfX_<pe(lX<iq-CZtNy|uMl9rLiBrPM2MOr}`leCO9q1lpDTv>8Fh=o8h!o(UC$1=)9L&333GSO1+D-%kr5y&f}N;CxW%BT`8waPN8#2Tf_3W`KSrLuw|(NHI>ph&DyCafSyG*k&IkP$64x(a2)8X?XKZbU<fvw|DZQemv{Myyd_tbj)})E6t@VM&cuz$4bkiB<?C8gil)0*M3@JX%MxNXrD0RuYI8SEOVDu|xvO;E`%rvdaXL43_LNfLQVjW$s8d9NA?6Nd`l9nLm=nT~FbTWU<#%z$01w^%U}8nOl=KQHUb}SFEYB3>?W;o<aB{S&a4-?ttl_ggcVOa7*Eigxt;uZ5Wd-34J7sYnXx`FzJ#|2Wk6)pu-q6Ng#v<O#%w(Ej}nRZ1lBPP$Ma1=`FV>lEM~S6N+HcTPlb|FzGEuGBS|#^_}k1a%kyoPWK5gjI9l2hUqO8UNXY;7Be0NVXEJIk5+F?H{YYx99t{OoYNbM@D$GJEv9q|=k)b!<;a>(Z!4A~Ye2SElwqiESJ%?Ft83}o)wT3>>RNhBT?@>z1C#{g-~a&)?9&n;9v17B$y5xL25Uf6+Al|*!Qy%@^UT1~+R54v%&j9+Ff{m$Y&4?U9pIM%?kws6oWP#m0T>x9AqNVK42F;c1x9GM=>UujY)+vApfNy0f3i(zfFJeAJ|TMDWS`Jr2~bejVz2}#C~z^D0u)4M$jy9TvSB4qW(Jrh23Buq3>IL9%=VXn<(mvk<H52`W|i?^*(O6%bFyrcEs5g_Gh{>JxPlDXk~pp)Lxvk%NTCS5ZV#9NK7bw|1APL?PGkB6lC8xsPLJ#?&M@4e1I$3<B|E?ja6sq)GSEBO0c3#hk`539?UUVdVkj$1LXx2*q^t~!22fF0Ry2T$Qr&Se5%4G`UmKA;*4`FSxe9MfSWX}<ZVRCl7-dNyrL3%TBD7Lip%a0X`gf*Bg(wBi-4LKzdus^Uz+2-1*tEDc9>7mw1|=TA&)S!n2M`3`W*#t5i`N;MTPY1aSV}_=mQuqqI9VK6XoekFx1mvRVBv=5sezRnQ*M}IJjd)xJF?RlYXetZtet_A9F0=T#7nM?qv!M@6w^7F=az}191Sij#6yl66BlA4*UFi=5W6{OO<aiG9Q4;M#7mC4co*Ux*UHDc5Suw@AzX;h9QCTr#A(iE;Hy~8nH+pIuQ{8AuVOY=(Zg3MQ&FJAl9;GKiGvLYrg5+~*j$XYJ-`yGP5f<X5FRnOMJA_-Iowj)<c`n=b^YxKZotk%>Pqn4B!wk3aFkS*;FL;IT7vU6ktHp?a%4ga!%~q6t%JD_WSRs=v66`reC2`Q0lji$MeEo;Us7UX(pJWMOKOoa-kYT5;oc-IkM<^Md9XK0%VWJsS{~|6(#lY8(pE-#leRL@TeP)--lVOJ^CoR&oHuDJ!@Nmb8Rbpd${=sjRt9;Kwlc<>w3Q*=q^*qb7Hw^SH)$&ayh;1M@07~ffkT`rht*+nr^;!j9M^^=O<Ag+NvHMFr&Y$oOuAn$eM0m@o=FeurBADo%1k=1k8wMZ&fQFURbJTLhB|fCb9#C=JN?<<Kv;Q}{ao6u&m=t6o_E-Dd4P4AZF>HBw{~m$^`ts2&-?ZI%)qJkykoD+3|!i5)AP@J|LVNJ=^dH({?&Pb(>^lq{pa!m7p%gZNSAr<KNlCcV2R>Xdfv0or2sCm@;-UhmU-7cmjbv%`(%VDpBRh%dhL^et<1Zv59_s0#^W;Yx95WW*3@AfJKSH&I|Il#gY%dSGR|P$C4-D(JKy4Rj&TOV8yRER?E7@Dl!!4@+Aqf#XW2a_V@&m6wCUMpib3<lla0X&#W=X1*#U~7+JsP?W!I;ID6Tq2WP~w}?barQ;w*c76-24uYy;vLn7c<f2IlS&j-mN=gkwyZehSB!GW`^eF=hHG9OLS6%-E;yJVBydTPhQcud`WaT4^G(j<?ic$gtyUnA6MD;|=EYGWGcC724C&i)7?2<ts87`5NB%G9h_`H@-qYFaa|F`tdb<&J_ys2A^{Ug1p7&T!A28!{=N99dGbCS3swJXP%y4h9Pg58CN*R*YH_afX5qr))nAEcjm{xJ%0TCl1bqRum~peML<O`nJ)q;@)b71j2-0IqGJPECWG3oRfUy6G~4zCfG8Mz*<>CH246NAg95ZZ2OJb?*v-qV6AX6qGU^1wbel{#!7$yX5KgdIGb@M_*xXSBWD_hldkWeFIKLAB+60S-pMo^OG@m9j4Q&$#cm+P)4)98_xREKG65w<)nVF&2-2ntanRHWW89_|aGJ=?-WumZ1%R~{IRlme$)i2TDpeA!eG}xTU*bt$G6<9Qi7UwOQ7h?T{b}(xaS-}9AHHoZXfXtdi_W6lSmavCt5}2nT1=V%{DX2DC4vLn|GYV3~>T5Outr<l_frx?~(Xv@e!H)XP#)@BJ!{V3Nu=pi5EPja%i(g{vMI$svlA4vlB<QRZmLpBFm^R5wlPo^rGSnoCO}Gp-$>I_&Lrtpwdg@8hZ!&n4D^!yVKH>`1(C{`=2}89B)+9@8fPyutHXXCc6d38|0r(_~9k>ED$zlhtP)({|i539(BsQBE0MjH^^%MZoBvu&|0MR5?8AO04HLQY3b$}+^15LJ6!SoQ_`sGAJrHAE2L#6X_qM_1dInmId!LpoaV9;P$4m3Udc%7HS3eDfkfL37sUIw(%!|h-LpcR@*Hvn3JsdNK?m7Yy)4gf@YH~~2T66x6--~d3Rht_u)fCx>m%YZUqdR+#T(L-~Q0x*O2n*ulk_L~AY1NNH&FoX7+vYZ(PgGrf;41*<#S4M`x1Ue!z3?|SKk%2bIupAi%h77}UWEdba^vjW9fXL7TWEdDS^Z*$KhztoJ!(a)rRghsY7#S<bFc^%C6=WFTt1kg$7|3GzR9Z#`leA0>7HI_-Owuwin51Q1FiFd}V3L+`!6Yr?f<;=Ug<PksG?K*>OLU)%5tisanIbIFeKJH?^7UkfFy-sX5RvOwhk%MxOS+$e8K!tYg)>a?ehO#g`swhbDm7b*YGf427FQyLMY6@NQ(=+ncVv2cnO8EaMe=}G^2!}h9)L?`JD@xOm)u|nlm~Q^S!oX`BgqZRNOHq6l3Za6&xa)!=PgAfh0UJ;?kT2?tRnaniw(O>KE>j~E~8Jen6S(2QyLVax#fIR3>NS*`xJ`-yaGSP;{UF|PpLf|CS)83Lko%H3Jdw_QTc3vwNMVgPhr(aWJ3;Xk^zBDfle)iY^pz`1A?By$}tG^Sn>xIo-qaJDL`Wi&{Ke>{K2Ij3Ii1~$AhX!OgVjuJzNJ@6No_^)dp6#SQ~iVVr_smIK2xn3(Z^v(Bi0*t|KOJ(96~l7dUEWi)`Sao2(-?aMVtgPzeroBy%$O%E_b*4OApxf}a&aCOEB;6t7}&VrzoM$x0Cx?}?Key`ep^a_h)=Kh;*O+$`G4fbUi=81=FbiA(}C^^BOsx|Q+S#5UHk_-wGo<4o4SG7q?wk?&w7hqX+PmU7@z)1$SV)r~_Ib!h956&u_-WP8l&)<K{ETL*E1GkjjwIAQG@2k`=Y<&bF#XR|m}aA9rhkbN(-b;y(j3#5bouO@8;8Z6ohH25}ECNea5OPPtx3>FhZ1r@xd&_qTB4{?^Tg0EkHKrq6y`U8X!-jcYaVT8BDZff}8>z5!P#PAkB6ooLLp=2On;VrAF8d<FM97c!%U561_w6KFl_~A`e4hnvFQ<;N;9lmOvLsqOx6;82um1>+~(pEUdr2W2ghOTlRV97J(N_l{#%#`EmAh(Z|hpw9`uZ{yeopBsGH<RwyOZyXPKa(ETOS=>4Fq6*fgY8bG<4n4=&9yr{eVUzqbsS(fk?!ZxZhfxZsrJ0Twv7Xvo`2q}-RfMiZt@(@`?Vzx@I>3qdv@zQz|-^3yT2h1@Kk!<{SA45r_%H8Z^#2Ym7aHhLmuF%^t@|Z@&Hd><8I!!EqQ<^qmTQ<SnU7cT)n}~JNUWaK*$<{oA>W?xq)>t#<C<JV~iyYP{tTT8lZwPhBQEhVk~KZ3dLB`02PX%(tu)|!O&VGl=>lR1!0Uc7;0-6;|zw{8ltplw+>(ojA-lt#TeoMH9#>$=4pUph|JRf#S)pP5sD=;PeT;TdXk1HmdHE}QEElzy^}9OMijTcZd5}QgS3Ju-s1NmGm5wPeaMjF4aQ~)rFes}nSv?HR{?(f>4z`=`Pauk{P2H2F$#G35=5Nw>kZHpnt>~EWjV~WX}0Ml$k5~0n;U67<JX%TX*koS<)+slV~=Mu3<VI4hck>BAWfU5n_h#=K7PH)n8rSEK`;aMY14AkYmgZUu1RKqNOVbZ0Ek4jdw@t(I|1@BuBLtT9E>mBck-3Upahqs(sEE*8~Yc;a$A|8f~DG4CMYT$mJ<|}_R9$>R4CX}2q~;D*HZ{7R9~*2o?gT#m?7x_9l;Pu59lbs4Xgp+QGgp*1HhhOpY8GT`DHc=>kY*<Gzt|8t~K-t>+7vG^r_zsr{|aXD8OCn5pYkauu(t*ps;?UfW|+eM)0ziuRx}xz~%(W^iZfXM>SsTBq-UxvrH|8W>ZVCSrJccR>TvV74gJ&MLe-x5l=Miq*QPyHmI}#I1~-#2?`EHSf@-@zoKFPw#GyC?}$f5JTSG<0UUxUeh%PJT<<WXQBY*a?f?ZvgP)B?II%kW_GpDHvO(Md_=%>)H<^B-Y4J_wnrK>llfkA^^k6n&Ol*cRsm_+EL;%N<pC|*4B|lLi97}$pLO7|yE>?wf()vBD3h1N;A2<Q%B+KNC3_9$N4+wM;oSY$`lNwCU5YT}ckpy&T)*>OD`k|c};SkK<BRB-}_XrIo3ysL2lNy!+rG}+IsbMKlrQE=DH_Z}EB|)iONl<DAJiWoBPR1ITHkX!TO}{>YMWGs+B9@j@O<#Q&nx0-Hp5EZtq##dk@M}_VrbVOmfO%jRSr3qhW|8#(dFnUY^!zgN^l*dL0GOw5ROU1QHezX)leSa1hiWGPKD{9XN+X{Z&s+j{1am7Bpd*<7m;fC0Y!);DHtN|dC@BHzD@_7DI;jToredJJSuxP?Clmt>?TUehcEvzL1rsR+qlWbsQVJmr4JvlRa*7&Eg;XL%QE9S4Y=GefWL9XXKBOcxa|AP8$)per8YPoLEO|Ac9qdDe3?dDHhV>al8voFyA(cLBn<fCpflU(t;|vX|aRQnr8rEA&X(%+9Hq6T`G}Nv131=&P*gp56**^E&tkNf2k_Tky$%fzo1$wd}cR+!iY=|9DXeU>n-VemoC$A4ZP+*4zrm<QdsvQ9AQ0)jnhH583GT9Kdt)Wb=4uI27=Q8flb|dpVRC@rNlN)WK8~_i&B+LO|5R7sh00!koyLQROu-tHCSZ=s6ELU5M`*>C;nr4M^vst0?CsYcRW|cx^y~U7%M`hLLqJcO974orYsw`4cY4E9NdI2IQ6^lWW$Vmm(jzqvorTVx%J-^ISEUh!6ePp!V$Ud^tpyr0`BP-0bi|iv~k%ALLFa@OwG;)dnrRqP*)AP$1RhW?z**{iTg%#O01|v1ewy|Q_v?aq)rD)1w@n$WVr%JneqSCCM=rjZiaFLf;Og2dDV5BuDHga9{H$WsMNtPH<%}J5QT7r6`2F*4-zwEcz!MT1=l>~k_=6XU(lW^W?BDRZ`fLYadv0J%R5{Ut0$JR<BF;_JB%B${*>l()+U}BBq5imLE*Gyo@LBnQ3L#~qZany=h2uC@S6S88_Xwp_J8co`Y^I}7HXlJsAmKg=wIub-NNNe<Al9uViBrU^-Nm}L#leCN#CTWEhOxg-8n6wpEFlj4@VA56)!J@4pf=OE;1CzEw1}1HV3{2Vz8JM({0p6so4DcpxWq>znD+9bqTN&U@qp&={uZ`P`GF8Y!|JqzT66FA6?MRjbHL4_G4wgJYjRI=K32HcCNE1|Xz!K)C^1#~0A<Hndb;vRd%UWEx>=)5W3=7&!XekEX{KTdf{K`E5XpX_NT>xl~!8h0kfF>d;#Z@j`gHZUyTNWV{J~3%4d}7j8_{2BNe&E{w+6!J@jgtTQ`%!vq<JVW)SFgsW;>GsW)A8rh{tAxip0i`|{#X!>ML{zO$9mz|FgsT6kLB61e1ELWj=Aps;Qr+|J?cIjb>dMk9-X((@Zn$-F4!gEH+AzSa{j~7K|GqpqeVLEJMpL!k9zTF5RXRjXcCW#ZRN$b@?u+gv8}=<+iL82Z*F$mH~Y@HxwwAy?DF|x>1X_g%ct8nyUpd(!w~V+<NvdH?DEFv%`kME|M?%^e6#s+9Mr%2cJt-tA8zd8w-+yVFSnatb~m?&p8as=^5^@vz`sA=|HS{>-QMmtPp+?T-)x?`?(<*vKl5@te6_h9U;iKd+~H)OjVJru=g-C;{cL}-&yFYi?90y%C)>Tg9A8E+FE2JX*H?!@=J7usfAih<e}DY#Pn$2l`1Y%>zxv{*{gC=(JD&CR_0{FYZ>PUUI{Y4Axo-2#7k~Zkhs}>aJ^udqi@e_6>>Fd>R-4-wTc7&zC!amrhEj6eUObIYQ`bLz5=u_})8zZI3%k5?+h?UKPoF;X+ZcS@mZz>SDLu_0Zin2Dx)<BGx7(}Dv+c{no9^MqZTQcxfBM___wT>>VZ7|k7k~Zci=V#!?%VyFb8M^4uP??sH2&b&bQix}T<tdF4ZS@sh&>t}m46+->)G3@tIe<DJ-gYwd2w_7_W6s={oCaB=gZf3$1ZkPSGSudza0<${xFR~54%TxJeNEC86WLiAsqhnhd<rn&+hKe?%_BXJltMgUH`gyx_h>}xf!3R+t=G)Uu|x77uVyB9ChE^yxonLHH`oCcDw^`UtL{a{Jc315x4h;UD%92|K{@Q^1sI`d%gW_yqi~>CpVW*pYPs()62_OmoMMGJU+7@UAH^DwEf|=9u9xT!@s1%-}}Sghr>%aAO0-ImT=wi4eH$8SAYEK)A8Nu`@65h-Pe5gwH&{O?%1my9v|p^!*4J4W7+1-ILPgec=P=?UwpfdXWA!jAJ(MDcfxp4?@{b8VHEoNcmH@izJ2$R<%dCXd?AgO@%<0qef1w-{`B?!SU-$I!oxS$<Kuh%eE-A@pADaNhbQ!Q9Cmjf&iJ2)?H-Q~pP(Kcc9lFj!1|-Z!q=n264j%_$J$4SZI_P@j$Drp(EaFOn)c{05I;H;vOGFe%8XCd)&2$WU)|>Je0S?;vwz=w7(MR(;o0SQ8;@6aJaBdS%kK8g{t>v@-Cn=Fx!7$kwy&qhUS9tDp8m=`{f&d|VJUhuzF;nXetms;$B<ujZvW-)W556QcyI2~&BqaKJeY)o`-kA<;K_1VcmK`l@XcwO`4IB`clbRgf8{&<TV^W$!$pO%|Caru_4^)mx8oB(z9~Na`yN`yf5gW3zwF^iJUw#!O(!iHKm1ysXzRP*=95Rx{!IAv&%C<>yUq5O@yqtf`0l#vEw@+KhbPyKqm~;9!Ho>z##TH0J&ccMH$Kecr*t332X+`A?_vLSd{2e(?`iy+#;;}kw=xL-^~e7XKfC|0zxywZPw~eWvKc=P{jz(teRZ+h{~mXP%9Guzix)4qH$OkP*}vz;|Jyydes%TR|9Eg1NH1SKe=t79+l$LLzdab=a<}8RZLc2u?du;NKiG@^vfZEH!JEtR7502TLLMIc{a`Xa@eg+Y9>3?op-Vsb-}`sTgTIb1@a@ghQDu}LU+~9aZX6=VLHN*AU5Z^wX>6b_g*^T}AO5x<h{Ex2F7=0hOMUWX?9~r1U;VPZx!jK9*>>zhx3`<y?aS9!cQ4oR?u^}Wck|0`bF;tJhkxll-%oaZ^iIAQU&y;-Lyf=c$@|wI=+}k2_h^5BZ#NwBX<a^kDTgon2WtPt9l!YFmvH<Nk6+U9OMm=wRPjd@e^l8&V*3~3M_2dc?Kn`p*<aMLR^_yV4dp{eE+4wpv)wpeJ-OOm{CxfP&HJJBUmtqiIQ-8Jj~F_>7RDF!$b}>P`Tg^A{p$JHH=mCK)6M<`wt4+x&l)4ryuEsRd+4J7<?qJa!!Y??YcI5ahR4V7UnjrKv8TLm=1=`bzaJVl92<5xHtZhh_bnSg)w1rcY3~NMa%|dtW85{&?+?TMEs94Wuiv8ns59*Q_uZJjdA-~I`~fT{|Nef)WW3gw+kbCfT#nD(cw{7%`+2=**ZWc7gUaUF&GpO8{l|;h;S<Jr|4H;Hde7)%Cw)8K(nE(DyTH|+pzc9>yfI_P+~4uT;BvLw-h3qX{@{3_mrvi`f7gD{+JA6(`(#AQ@lo3D$Gh9j{;lvHSdRVdeb;@tdwIPFqG#Ky+uc0`j@bKVyB|MqcTew+UB0?_`|`=2J)iFf*vZis*H=&XPvi*cx8rB&4+owde~CT2-@M!&yXy3Ne%?NRKE8Y3zP`HNKHY5JzIkzdGd^=4zTxHWYW%tPkMjNJ%<&06Hr@Sa%klj&c8~3wix->Y&y2s$?w;tL-RyS%z1v*B-tFIxoBg|U?4O5|?b-hLO?PjkJ&!-UgNbPw-S|3wKDO)a_@W$tnO|@3uJhfy{|`UMb@2')))

_PARENT_27_PLAN = json.loads(zlib.decompress(base64.b85decode('c-qXpU(YW`m8JPze9cA1-^{E#7o2X;xC>;UQFm)pLV!lhQ~{zvGp&}t``Cr;a%P-dJD*&Urmm2%v?5RBFEXAtV(+#7_a}e(^RNH!-~Hw<fBf_R`s5$}$N&E1fBxlnfBNJf(holQ?XUmWzy0rD{`%)XeDV+Z2cP`EfBf_R^SeKP@(;@oKKbLHe)GrQ{_c~1_~d6l`QiWZ%b$JngHL|_=l|=k|N6T>{N;as@(=&}li&a4cmMk3fBfN3fA!^m`RgBk|JDDSzxcr?fBNJ9{QX~k|Hm)o{zv^m{Xf6>!8gO@^Kj+Ca6kX?hYvryIbb;tSRV}ds~>;(^cVj=U{wRw^MLK+1OC%bKmWy#Pvf0+%Xf6!S+{>&_aA@xlh1zi&p-S0=fC*n=O2K6KkKg-6ZP4rKRoMx^6NkR{$GFnFW<fzHO_h-XZ!d#|LMbrADxH!dj6Br-_H8`$Mt{sDVm=BESr{(>;CG)&wn9x%R%=mnUipGU+igwVTq?a>(!n{8di5I?#n%mFf8X(AHLp`@UU#t<8@npkiV-uEZo%n7kn6DSi0%a+WqP)F2@;`Zrc3Udl+F@ylH>@dJn?G^34~^_rs^b@~sEqJS^Xw{O|H%gmH(?bKdT0oMG|i;(wVBBMgf-*T>)H!`l@MlgOv}KC2}5#lK4=NH*W*4kVinvI;wp>~fG*w2_X#>3=%we)5|?|M5@XQkfb>vBu%yKmEmr&%x6x#z^F2a-3_)7|yI5htbHv=H;X;QRDD0`1I#LC&H2}9AOC*j<5s@M_BTNBP=n(5tiKG2uoaWge5K*!WtJGVMz&&u*3pKSki#=@&pZJwr#hYG?3Z0-EPuAMt^qP$AN5YCHXcTWVDgw+ju}{<?i8wH!F9KAn2^zK7+`N@$R2NWD7j*pG0H`9`{ckGUL?y2M*aH)%)iU8M11*%?oTXE#TbY?%e#B51;+?pFWY}NPeJmbN{>{Gm^i5-r!740>=+@McqGkKvR>!IfM5RzJJ<4Kf`yA8wxvaxC<BsUL4##Zz#rvgdz;8n{P4&)lD~<q8KakIEo^Sf_`*IUBwiIQEj@56wa(1htY(==H;X;nW8W-Pq&f6nVQo$k}wMVPNmySQ5Y|#+elHY-7Vb)i~@JJbQ>uO<HdBFD2l~I={8^#$VBNjQWVIG%Wb6a=4QD~7<6uy+e}f&nZ;39Aw_+D)u51~KEG;EL{Xn#H7KB{=y#WHS58pfd=n_B?p=hSy30+3sMbe&xl0rkezTX`3{lx%B+G4tsMb!u+$M?&clzZvL!hZCM`4K&)#AhDHc?c_hs$k-sO;u{xs4Fj`h#M*O%xUWNwM5!h)Q;|qp(H@M_3YsBP@}@5thVY2rFV}M7G@~218a6gCVPk!H`wJV8|+7Fk}@j7_y2M3|WZ>hOVXqM_AH<BP?;i5tcOI2um7pgyr_{2+Q5y5th5ZBP_RjM_BIm&Xyr}dq-IA_KvXJ?Hysc+dIPFERgK9X^=LC+|MJHIeiRyJqy>l4FGvN574G`0Ob9wdr`;z!=HZk*@qwg;-CN1htGfUlh1zg-$N+>?kHtBkFrkbGbrh-yUi`lFZn#cKBY3hl(X(t=LMYi(=c@yCe3L8D8t&l>c4neHeZIddewIU%jV0lRxjHv=-eNM8CL97^98KVFT;|(>b-bc(_V+=dewUYYuf9uUay)h@aN_*%&=;&Ixc?x(_gad;bGlgwOrg$KK#`;EY+)?iywXd)2qGk)6YKp^1uA<|NGPLe)E^#{q~=~`hWlJKYwQyzuX|@V~l(9)utT(X@3wNmh)971{EHb^Hl=|6qb16bYLh5F<LMrgBU#+5<QG242d2_7lwolr$Iu}hS4D*A;alh(3Fwb<wCv970IZP)m)K`Dp}1F$*5q}K#`u8uxf-zMro;Li1fU)RHH*ON<K9^B%|b0<3ch@F*Pov=cSmM7LrjSsR1B8FOk#$kc`qrO#rCr;#6&^2p}8PixL6yTjvnjs9%&2kc|RHNdeiYEtD9LpBEQO3dly$pTvOtyyj0+KsIXeGzR47wRoBWvQZ<aDIh<uk<$>6joLL$0okZs(-e@6nlg<6um@qeO##`c#L*OxpI72&2*^f-jHZD6yh27pKsG8@GzH}6l`9$ovQbeYDWI_Hk9HRV99_i#j;=xgM^_Pmp(_Ev(NzH8=&JqS(UtqZBP_RnM_6wEj<DSQ9bviqJHm4FcZB8MZwTwH-w~EuzauPnen(jD{Eo2P_#I)n@jJqD-*<%NzVB>HYTK{IwSwCA9bL8UJGyGycXZXZZ|KTx-_cduzN4$QeMeVr`;M^O_8nol?K{G9+joTJw(khbZQl`=+rA;Jw|z%gZu^d~-1Z$|x$Qf`a@%)=<+fkny7jMb-TFJi-z<<46eYsj`L>*O%R}9hSy4Lc)~6L-$6L*o&%*7w@WBe9oP{sSm*_oEt7qYhs-+))`uTqyXZh&D@trc7k2`Xo#%|}aw@W`$!~di8^Dz6Qxm(Y|kFB7O_la#AgwxYUJ}D0?H9cLb$6MPzEY+*ZLwX<FhsAnTdKj0F9dF0`uv)LG4e7mmAC~J?x#5&$bsBtF(!vGWaH{IV^1Uid#M3vd*sEH^8#f^b;bFx-c7Hy8`1`P8uPPC5+$tP|$E`I#u82Jt;0+7*s<x0;Wv;`5y(%tzP?h<&pJh~#sd&VwLX<p`oJa=+B+0Q*Qb3Z75(Eh($tXdPK$4!9AV}Cq&npEaT_m)O2whO+avLwGa=ncgPK~4Hi!>ip>um%{(@az~kXX|vfy5|C*0A9e;%dB@{>D#(O9Gkaz^;MBnm$P+Mjf*zlEhG_-X@a7Q0G37q`x<i<XK&t?JlY~Wtb9GoH9&_DtSUXs6>|hyd6{$OP<vZD*45!Qk4LcCv?VXkjc+G<21+QS)FkjYG76D{WFt1p&wL(OMc!Ds!1i!>Ic=>k`bvEa7dCTv_Wfr$<O<sHJjvFeb5?B^7E4iO(xkmdC+K*zps8!4Kn%pJ&OjJ{L%%E;bbi-q`XBT<t+-a%&ZlCIBwPwKdA6>mpF=194v_gT39c)L8BNI*qSt;xAbzGEs9a+uHgcDJ}<YKq8Qx-8Y-X{^Ku&_93Nnf5d~gOrQ7)6_&RHTDC~A6-6jUdrCTFIVTT#%HZeG!>ly+IJ0?lDA;59amlRN6D&wdxm2nvM(~<$|bCU&$0M#&AkO)xc-!|8~lu)MycuHol=1xLGeeO`9nZdF#m(WlRivtY}b^e)qxeXR|TKJg83~Tx%XH=uSKw?HUd^j{_)cN;n_fInFv=}}OCf4*xFsX0Vebl$=KI&_AA9cz#OV<Z4->kp-eVJpf^*rJvbIi4!g(sV1uKhf~9COTdJ?p+<j=65<QRbLquKQVcvN`6qoCla=j=80??knb)TONj)WRAHFYj?Ie<~FR=N#>Z_uvT9&$J~Y$JINe#8<y;BbIfg6u9M6$w_&}$Vve~Ft9F(-=02?3S>~AguvGsp=9v4qC(kj*+=t~n$sBVZmh&WYOo=B(S*nB(!yHpGh+&Q?(Zi@kljvcXV@lX?%rPZx80MG~GMu6^O&LZ}ndS<o@=<ezV~(kL!ZF9xKw+3;YJ_miF*QRN=9n5C9CJ*~4vsmd#s$Y5Q{#eRj;U$EF~`&ZV3=cS0C3DPH31mrn34dTs!WLh`K@yZr|eKdfMbp+DZnwulo()`V@e8e%rPYf80MIo0vvNpjRA%^rltVL98*((VUDRGz%j?v6yTU+Y6@`7F*ODl=9roS9CJ)f0fsrIh5*MLQ&WIpj;SHQF~`&tV3=cS2yo0XB?TDnTM_~sUBv*7u0jAuR}p}ts{p{!RRCb<%KhKbmHWRVEVqA0SZ@E0u-yF}VY&M|!gBL>gyr7v2+OVC5tduOA*^?PM_BIsj<DSL9bvigJHm3`cZB7>?|kOfwr{v^$!*`!RolL!tG0bdS8e-_uG;n;UA65Sx^mlhbmg}12+M8X5tiG&BP_RlM_6wAj<DSJ9bvicJHm3?cZB7(ZwTvc-w~GEz9THReMeYs`}M6`|N7Rge|_oJ-$(+N+rFc#wtYueZTpU{+V&k?we35)YTGw-<+ktW%5C2fmfOA~EVq3}SZ@1{u-x_?VY%%)!gAYpgypvH2+M8X5Z2qiBP_RlM_6wAj<DSJ9bvicJHm3?cZ9!LAZ@NE_P(8U=Xhf8`&qX>_A>siZd#VJ@MBNxW64ok(pkAbSI!6Jd{$ncE2o2UIV*3^m6wBZJuC0eJ)@7x?W~-hyXGF1`=FejdvhP9hxM28V@KYj@~{G*TV0=}hedeRNdPZ1QyNy`bFb^O^so%C+6Qj@<#bdYmf@w7HB}y#;Z@%NRvwn&RjUA29+u%%s{mFWmf=;a09GD%!8}QMScOLU|515Zghu`Uau*5G-S)&E{`6P>-kg{vf+$o-58EO2hzcT%4hIbpMvH@Hi0=yj<1c^m*^mDD%QyauUxv+L^)^eKoMeA^R{rGIfB5~s{`z0Oe(ic3MHcB{|6ILI7>V`I)%$>9IKKvf@$CJchmfG*yx{Xdk~`AFHobbEKN9QHtM~aMJwILz@WWD;_+cqa{IHZIept#9KP+X5AC|Jj4@+6%hovm>!%&v^k>}vR(f&~a2&|ZIcQFGNwzu1ukzudcea^^67n<gaY-EmUqR2*njV6iwZt7S-8+lspSO6d11WM?Dh1&T(Wy~<84k*KLr4A@#nk{v}9QnBwL%<v}?AQbNF#Om9_?TwM9-v4z>=*(Tam=X$7@6o!{iW2`c1igQ17h-P5R+emm@?~3<2J+?-q;di9B*t*F^)O5rkFCpl}gi0d2UOkVW!OTrP5?mo*PpI)KVr`Qw6+Io|{tzxKd`hQw8u+p1bA+%u=j<K|)KJxG#KR9Hf-j4pPc%2Px&XgOu{xK}vb;Af>!^kWyYdNGY!|NO_4t>Pw{^^`+8|YMnhO(r|oLHEFzTORFJdo-M6r5^wqxhScW<LIH+2=E(tmylg%lAj&-V>3~tZ8I+JxpPMiRj8Y93rT{zYyIJW0n$&4w=>e&DGbmA|K95TeP{lAb4^YK0&JIw;aLx`;rCNUjNLKkiyt5_LwCAN85^9<OOA2b*b6C<$)0{$Bg*5HCJ*CE#X82QTKxyv=i)e;v(~?C3r19oYB29bl@EPDrGdw;6Kxyv=ZwCz1rX_C&NMp^QMw<5ACN;p7X85EAfYRpw$pwyEn)NpqIDPSEP%=$>o{SzaO*0DQG}E;20XzcsX~qdq{$?HaiFqJd51G$HmMLvNDVMWw_2UtaBh>Q<?QuN9QMjFj`=oe;<1qa^%=)-@;wZeHg*QJQ;W)x}9$|kRk8l*;&%%>pK~Ce8Wf<q3uz}zXqYNuP%}E<bWmwp$Oi~_JcB+$<hZTL*^n;a$C2jQl9F>PvZ1nsbm4{_)^!yx^hvjSZ{2Y~s^=tI}9F*&@VvU}kqw=`xPFjO?Sc8)yKT;jm;H1nC%^+z`CRqav;&kCi21!m~iDZv7qp(CmNHPjbBzB}}g(VU~l2KS9*(1%UE71^=jJgty9cfx!iN=a##GVCQk!IA}YQRWFy{!g}G_BrN<3=*-Z8dJB8TGcBJCadvtGOdhtGCq@lAL;5jUmaoQ_&ofzOMkZfLhXP)RNw!7Nc`Vvx(EXBiRHdN3`2$0`nc(Z6cv54EIk$vU8y!DI^>B8InS>a~QAb1C^pDa_C_xOWv@QC2m;Ck}@o1Ng0;1<O)k!a)qTVal%rTIAJMEfN+#GKUm5VA1q}F1eUS{0!LW_fzbt{fuJ~~p@5(`q@jSII8DNm2#RwxDT$ysCBTvh4$TWc`OipK0YSNWAN=!QeE#XL{_(@-pZ_;qh^rZ)IF+~>5{glZt0AE{g`}Diicv_aDWN!JkQx(;k>?q3LNNk815hZ>6Fmb^C`P1bKnmq~re{D3?0b^$gTjOlO1=*d#cBQ5^iZCMlLqwQC`)>%*2RIshic@LYJR9jK&b|ZY9y3ufT+(SN;N-JBcoLFLwz1nssW-JA*BH=)aNOs0W4G_rZk|1`aGvJfQ4!Vl?Jp>jil0m7OD|d8qh+0o>dyaLUl}jH7!)b<X6K&bxeLWEmXtgSK~r;Onx;RRKw&~qd|2{el;6Z!){fwfnmU|(ZCW`WMBy^FtCIb7g)lI3oK!U1(vYF0!vs@fupRcz*3e_U@1!|u#_beSjrL!EM-Xqma-%QOIZSer7VHKQkFd6C~F?DlqC*W$`S`GWk~~;@;57Go!GLWi|=bc4>_r2qpoM+`ZVj~RF77-vvTvBL5?Hr=MnnjW{`t$Th7Akq-K!gFzGzZMXmQmGuxm3{Kwz^^*4X{>d5cMA3pr-BmHb$kDt%u?~j{Nj>6?EeAUr`3#M8fq~B@c_)_(6vl_LAwc%@!=A<a4HZ1xyCr2r@Vb!NeNlI;4^_Lkgu!Fn}tNp5-16K_7VZC4VbG*?*-iOb?WzUD#MBaz>p7vQYIIQ^mG=AyygX+VAzv=;@ead~@#-FDz9hHZLd({I%+x+^laIbnmp0~mV?Q4>L(j59}fPS225lKH*vxuahDa|61ew=0zNk8+NMI`;C7wD$~`mu_-HU6Z(2ct-8a<Yju{UnD`B>g0ZQ6&8&r;u0UPkPyxL?cp~=S!l2$(lh;L&@3iCH^F5znApmWJ78CN#DnQuQADK;Lw<4DN9Upl=b&6&pP~R_rHWrr;Gj)W_bJqzJ%F1S<;`m>~uQn58ISv5&eO4l120fZeFs8{@gjqBKmV@g=Xl_m=&6#zhe_aGtw8vS1-Tz)njF=jbI*?F89A~R65`Px>4zL|LaDjm-}BgyT0^1n*7kQ`qHzs{L-P?-hNV+-!^-S&ZEii9h;)FwEW(oDOyj;@^fcT(RnoaQDakdlGb0f`pQL~{@hjPFLC*`t25l!^jEJM_G|j1SEu=}=`Wy>Ul4rls?!*yzjpOy*Gv6Htn*wi^~cbgLHRMPuO0Q**N*z@)KkQJCjt6<+1RcNzKV@)R^Y3MlsED*Y>3k~@&_)J27lmE>2&`KNTmVqH5WNH!hp<vcO$@uevUigJ$s6F!hmdwb^?5;ZfhsJ*WXB&4!&&NiBQy^wm!r2Re$5UVfv~+aebQUtNz|~=ZaT<@4D01r@wc7hU1t1$aTZ<OMm0~G{-Of#p~8#q5Qmc>#$IM-un0ELM+QTR>Leq7Hh1=WrZx(SPiobS*x)+W*M?ZV|6SoWRb?|m_f+84EoIZcE!c&^qcF7i`9sl*Oe11ylYDLab$HGmNj*(?61;vA39d2F<isO3is3HK5eW{)1d~8)o41@d|@d|ys(rdRanZBDlBEm5tg#V2uoQ~grh9EU~@W66c=p9$*bgo&8QQTT(F_<Q3AD_R5{<~g3a;MkzBALBu=0bb8|eRG#6|y$F*v9*yhExYLf6~P?E%ExNK>X*c_KFO%mJ7ajhCQws~=_8a=ET)a<btajlv?HY2W8v&Uw{wQBa*j7~Yt9@~3WN!ygt(drZ=ZH}wBqLkg~2vL->ztw2Fzt(8GJJpa9Q+DfbUxg`DdAW@#yW@!?F=b}}yWFRg-7z212(mLc2A3(jWAmh$V`t2<+-Hv6G1St`v7;~fLMj5OG`J4l9n(;a5IgimOZORKcih}GMC=TF(tU{79p5}n5j$h5bRQyi$DvTe!OomKkILVymu;dyN0ZpFF6SZ3QyYyFA+G7HT>W6r;|TdYLVFzSc@!>Z;XWzX^EgaB53@d>`@<(}ZD-{Pp{mCb`gw%sp{hsW^(;IsRP{K{HjI-VyI&lYhgE##tMRxMXB$@SmB9vW#o2~cdu6cUwc>2U+P$*dh|%EmXT>(G-YdV2#|A#zuyU__H>iWpHmuw$PYut)XB*b<m8Hg=`9Ewa+pvPKEHxh2b8o}qz4F$e_1xRI1?M;NwD(~J&vM$>hZQ{0Y2&+f8Z9_OQ81H?np=r1%=@APWTDFWHmXqNbemO@-}aMk6H9_!Kj}8HBvwbAZi7nldw$Y=cuBD5C*9|j#OlG*eO^g^jdHq=E(z8sr~B-ZSdDVJPb<l<QBL;(CczrzbRS&Uhv-zKtjQ%gmDL(nkfX|}tX;E8aw_IEqo9XAwf|{GNls^>#uD_<r?yUwCCTa-Rixp#Oi0pj@>C^gWT$Xbf<|^)(IjYOqgq8mg_TY!p&}cWjuI-Y3|LJNP6(_9i0o7aX@ba38HdJ&Y?N_mTF6cjg2shx6d`Cd$W8&4MuY5BU}-eSMxvP}gY1-MYcycKE2n}FjRx5%g4b-2+2usJj|P^qL<2`zl0jik>i5aO5>{kj2`ezLgcTQ9!iozlVTA>ju)+dMSW<zdEUCa!mQdg*YbLOiB@<Z65(zA2i3FCiBmzrW0)eG0fxuFhJYXqH9I%un4LHi01}tSs1CFw!fp=V!Bq!7vo$eACs?q2!fuT<8bC>u~zc&j)2^-ZY_?56>2`kvJge7cP$`Up#WeFROvW5*yS;B^;EMdb^mat(dOW3fKC2UyA5;iPl2^*HOgbhns!iJ-)VZ&0Eu;D06*l3PBtYnJjn8QkzXpT3mgo)<+x85&_Xwbg(e*Hsp9Bw5hG{<sQazbMrN6URqXs`tg6gxD>tU;4PW4DE%vY|P)7#bCjwOApQ4VJP*1xs0?f~71`!BUo}U@1#fu#_b#SjrL=9A%9Pma;?zM_HmmXAE-xmckNNpkN6rPOyX(6Ij9u2`phn1eUM@0!vr|fu$^Yz*3et;3#Vxu#_bYSjv(HEM-Xpma?P)OIgx@r7UT{QkFDeDN7o#lqC%~%9;i&Wk~~$vZR6at(t}Pt(t}Pt(t}Pt(t}Pt(t}Pt(t}Pt(t}PwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+XwVH+Xt(t|+@@G&uuvzW{iU+9j{cD8HG1`?xusJ@v5(%I$>HRB%%`uFUOt2Y-QJM)h$1qAm!DbjnX(-qn!zfJ!n_(EGsbF&qqcj$5j$xGMg3U3E(qOPThEbXfHpehZqrv7FMrk(K48thR2Ag9TrQu*R45Kt0Y>r`+ri0BejM~3hFMD7ZMNJ>~dKNAZg->0Cdpir)hr*}!w!NQ)+e6_~N8Y}kh5J*Nrc;~PzMYlV=gNmK(!QUSx97^={l(>FIV<nam6wBZIxAlpKhYg4FL{to56xE6NqJa+S6)w)4e~N9!SvK2CZCjtHF)LmL@6vU!z#S8b-H0?d{iEm;gzcs#ofFN>+s6W>4q22QF&O0S8h)9&x)Leg?MG)1cMZE8W!S}e-l<7*5Q?H6ILEK!aPZNScX?dO;~wYhF3;SGzvpvL2_yjB^M;8_E3UBa%vAH86>A@PohC`iuNQLBqJtXl7ZvGp~)aUk8KaYz_B|CzyO*m0WffkWdblr&!boaFmNn<0x(GEFZ=z3q>>CAyQF{&pz%<;PX>++RzL>OcqrW`1IOMhKm%wzl<uQ}V_Fxm0ea|mQkHCxoEmls2ieK>m2i-qy9x;h*}1EbaFCt53JC|<DPfmzkc|p<2?yCIVApT}owU+@ILOAaT>uBr@haVigKQj-25<oVlG1%R$i`8000-GP_7C778^`_u96*<+d>;-RE2aPr3@fGp4je0{01lu*P`(cbma=36OIfmkp{&uMu)jLnZ89kAZ^L#Q3<}!5S8$&|mCJ1~pvw6+7!=>@`2HP3fqx6++ptjBALaQzEEM1AIN#@o0{_Iz_W`1?BY=FLAByjEobNM5fq%N^`%F>bfkU~^6cgsC+{X+$N98_e6n4B(?qkM;l~(Sf2VH69K6)TGqO-C@4@+61hovmh!%)`fQQxX$sBcv=ROsPcZlgza+(9LJRQ4C`{ZfYN7ywJmsP6`0YZ9r`a<Bt1apo_ekow#}Ie?IA7$^r6Qs2$N4ydF~%fSv9#hXFNDD}Aob-*L_c@B1fBlUR>c7P-Gc@B1f9@WUf4$z~14>{NYqZsx`0i#&Tl2I(PD8(qv$nKVm(j53vjM5zVQHau<GEPM(%_-wlgwmYI21zJw{$5pY6H2qTs(PPLocRj~r9F?l2neMa(INq%wE0|G?-NS1z_i{c6mJG4p)|%3^**6ABLpWvl<BYiG`hwZ=e3^)l2l{Opr)F}AP>MwdmgD7z)G7!V*Lw)YT8>=(;vEGXKkLLc&8hIU6OY?I+G~?c&PIIGa0IU|2nA8$f1_#)1SvsYpm(BQm6x}>G9|MPk;X7Z~yw6zx>;S{OTj$^R9=N<kQ&~3tSNO2?_840rlq*@B!WQSrPC7+{}Obm6WD*cys{HXu5MMp$Vvad*N5p_;0_|?>hJAU}uz2)SZ(ANkNvfgdj^<LQsG0#HPP?V$<JZoAn{vRBZ*K*k)yiMEBWdwd!^i+pJdIu40?@;VyLl;%Q}@(EWR-)!BpY-!QEVg~655`jGy>)zZrF4_qy+4*!9BrWNgzg&fg5oqupR1Lq%{%~<mfPHI-;Pj-zd>xAT`06f;`(Mth%th2J00t{K_g)dpxOzUgVvc3i_>s!#WIl>A}EMbKvmarldOIU%4C9HVF5>`B72x|hdge8Gk$`U**WeFaZvP2C_S(1jOECIt(mVjX?OQf)rB~m!bnk2T@jxe^@jxe^@jxe^@XkdGd2DZ0oU}w&v_i4ZqRy1G<D;ltb6%AOziUurUMFWPgrU6S>(txEbX~0sJG+-%98nBcl4Oq&O1}tSs1D3L+0ZUoZfTOHwz*3epU@1!)u#_bYSjv(HEM-Xp)^}ezdo50&iFEd|l%=zmr7WGjEM@8JWhqN%FH2ckdl|}swU?!=y}c}H?d@erYjZD4TAO=W(%Rk2lGg5Cmb7;FvZS@UmnE(3y&UPl-pi8K{$7@}_V==+wZWGqtqr~`Y3=Z3Nq@6szEY94;Ii!D=Rf}N;b;F|_7Gf#ZNr%5!I-B~i(t%s7_&a~?L7fpUIyi-Hpcy=oCf9oP<cHm=Rx_x#rPk8`IFCn^v_@Zs($gy;9l}PL>Y#-urvPIXP^G?Ed9x^|M2^N{q?_m`^(Zp)nTX$d*l1}x91_+FvOMPczA((mhPkUQ>Wvz^tiZFo+Lf4;Z!C`k4rVxInrfZt5=@mSbAKnSEl1wdR(nnrsG(8T%}j8<5+rJm5*J=&(h;+d~7>@mL6AQp0pavN4DBYtFer$F;7~JWn7JU(rVP~k?wN9-|DG9-b~U6d89eC(+GK_hqO}+CP}X`33EvA#{xSIB~&`!hmrJ%cg{md2uZhj=c`|{9!R4|dW1XYF*K7Tf;(qv%_Pj-`}_;iQ1bLW7eFW8i!K0Gp1$Y;s0F_00;q+)Xo4+IUo_#DWc>xx5zst+)r4%|t0rWV2qSbvHkPy|8%J7`O`btE=W`rMHu;U#+<<H{J5y=*`6a^~7635$(U+r<)0J%O5RII%<VRnPM$T3;`DiqBq>_#3p@?6ezU2Zy#(T{KYo5Mmf;I3(6OPI3ikskzC9UzrlGgNMNo#1aq&1^h(i%-HX^ke9v_=z4TBC_0t<j`BLX#vnbB!it)&U4WlVSmcWRqfTTarzR5t$b-NqM*-f<u;K?T6r~r99jY$stQ&+aWnyDXi_AoUN1@RvrP26vN9SV30D+%p)L@;@D{fNKz&=vPW!Ep0~0`Y*MB*vj?P7h@;9k=kaGxm8zdW15I(9PXeMT^V(&<{3-nHpC2{O1|(FBj+TIgENM+bj<hDBI>+$?mA=#|t>zMas?ln$$)`?hHP;wq82kqmRA(41XbP%^(SpXFI?ZSyV4rFj*hTPDXIPB{6jTkbkpO<`G_#Qah3X5tV?n1j)i4{37^zOM8;lsK8is=bBh_h^g8?H|!}KqJpK2knh9Ar5KA@O7(TC(VSZVsH@6k_vjeeR@BBB|m8D*;)Z5m5^18CD&NE(2d<_CZQz-cf541i5T`@tz&Op{G>V#@-Up^r^Ya+(uK7eEYs?gS`?K6e7(LZ5p9NJ5``0Z7tVzTE;yq`}C!1)xYnTkUpyl>vRw=S~1W=yPX)AI%BV4Df?KH@Q!0PBdWv63xl^lOWNJDi944{dvZ4022Lq$Z!A>ogqrQ4-(A$eIwM+{RB<`5*_}`!4U~c3t$aE-3WP(IHLPu%;bEe!#HMgK+=uG>If~m6C)j<1%2)W(1Jd90&GE_o3I6a?gg*~TB-dct<i!#_E}q_MTa%b37`di?gY@Hvr^Xt$ik7<WU)F$92zZFr-(zd#cCCCNVuTV={{Yo=*M@KmUKa%dby7h^r@HoC;`p+7l0D%sn6OPC02O!ngBP@=O#xI(A=J!NU+B~X$RP_!b=izB0-;<97(J!?UPW$3iIFyHLzcIMkf;Vxf8$!`rPD1f<AW!*g&6~oJg!jbbSC0n^8cZxnX;rk{e*d=ENv!Y}lSB@CMYdIgy{58aDK0J*ARsYM@UIZZhaolaf^W*yJXIJ~zPz`rHH?=yNZC8|ZVBn~aTRR}*a5VEQt_h7Iip%W03)+(4h3++@(_CWRFAxyelieQweiL!X=6WYFg(B@vsGF0Q%3a(R{9U@1#(aFjJRSjrL`EM-Xzma>EfOIb35rL2*`lGemvNo!!Rq%|*C(i#^W>3|k2X-x~3w1x#sTC;*Btx>^})}&xbYf!MHH78io8WSvOO$pY9t6j@1GgfU+W=U%oGDkWv8?&Uf+n6P--Nr0w?KWmfYnL%gI`9><v;#jeOFJ+Wv$O+4F-toz5_7a8>o7|@une=b1J5u^JMav%v;(g&OFQrev$O+GFiSfy1+%mRS1?OEumyW@gHKLBhu+{F>0pDmr1b`GN$U;XlGYo%C9OAjOFG!#E$v`~x3q%|-qH>>cuPCj;2rH~gSWJU4c^iYHh4=r*x)VgV1u``gALx&4mNm8JJ{gUdyW#GcCf)a+V$JDlbkq}$cFPcW*)}8@P4P&4z&!*7uN6C2%y$Mx;>XZ+?v%kNOw05<UB+lhFBk_ft;1sLHQz&!D}tA+c3^WI78?!@HZ>Cv%5gi!|%iJS9vP5v%M{&baLPSd5m$HUj?gB6Rb9_=Br>8&jhQDi~A~OWzJ9FJpT9vxXNO|4g_ud1YCu&U<ZOWuKlYtmIn?5U(MuKpR0q#llC8I<0s>BhRa!c{7O8|a5+nlUx3FME+^?eegPh5xSXXwvcKm^(&NH^oZ)ho9+&##3>O4EX^x3jBfyiK<_%3e$!Xru#FJ*YR%-G|hH0e+p7eZEY6O2^a18*SDXA#|)Htar0n`{Tpd+%e;#mT;nG$FcP>mC45&(<!4hX#@@)zCd`xd}Unqeg$@JKSO<O3eDzC#7j30npY;YpfkVfBT65DhcQD3S<Z#*)@B<49|m$+H|m+kKc}DHxR;-%x3Ae3NIG9BY`#hR3mnnLN$nSi?+a2Xo~<%;Xs^ngPsY!$mWInLN!!Gk}?lzT&5|(Ew)h3@_OLX0l->8^BDS<|Z4!OlBv2<Rm7~a8nLoCL4Cj0nFrSe#!yN<oAGs9n9qS4rcOu2Q&G-gPHu=!OT0UE1G4j)D_J#Wk%GQW}0F|ooSRQ&R;F{KG+n)(^aEPnUPPanWh-=lmW^V=MVP^z@`}1w*ksLdjl&%8uSWQL^8%JSP|D0W-LWWrm$lfLNXKMLW({T2ymwue_RK+V@Yekaijxev7|M!l=qHb%6rEz<+bA%C-*~xNi}RcG?!GvTSMbWWflPdM_97MLXK9bG`Jd~(&;{WQ0WD*M|JEN0^GO}67sck=zsa}*-!uJBLy5?53i8~rBj^zF#-~)j`v1@BGYH>JiG=JG;1e&tN>7|W4#p+%Jf+~53jid&DzNeE#MLuva$d!sg4_8047vB12VC~VFEO<!eIh7F~ed0_RIb9clU*H@Y0xZB%qk~TA^=yuh6%>SLjQn(|wL<j<2KUnC93zYL02MztIJuPIEq_nsl0DnHpfs^jWJ2b(*tB1gO)TJtE+k_G0;Nd$D}C&DkTolHK-R$!>eEWVgLnvfJLf8EWs{47K-ehT3a4Lr!3e29*BZ{ZF@QekGxFtL9e{N_Py~HKBCJRb3NGcU;vqp}<HVLLV^GhtP)=gb~mO3=AS<(OIY=IYa4A5?cTk-AG~!xS~60X#rPsCoL_&h0fBu62JvZTH}Hv9pHi`t#QGU*0^9vYg}-oH7=}13Y*3S7M{=vE>LNJ3sf550+j~1usY#F8W&b}Ee`HwU<OM9v|weK1h}xyKTt@3D4ZyjfGDgel>jN$`G;2tPzOvzNq{=6WRZY6*7?^m1WZ<TEknR$Wv7V*OjhgaM3c#CU7ct&S*@!R%_i&ja&;0=%=+4)$M#xn$@W@p$@W@pi50G*8OBOL(F|jSlxT*rGD<YWZ1c+v2<X715yClEVn+Zm+x*fN0y<V;NB}xkU`RkQFHBnoq_eS#pbS9AN<RuH=7lAi0qJb4A}9mW*%+S@(Af+Jr+{;|7t2q!7t2q!DGZgXQ+~2LJs=WvcB8pLgU;?`t83EPojh_)I=d4`u1RNSmja-Qc4v12z+h#ER|3RXWoK6c#8_pAR|2H{c!yU4#7kvo2foBY#gf*1Vo7WEu%tD6Skf9jENP7umbAtSM>@a?OIl-vC9SE#lGae+NC)0+x7}(FoqAs*Z!=6!67;NXz`<={=P?a9xG~e(OnP##HfYK@P6>@#4h-8Cc1Q(GPSVlH_3K~Yy}s9ktWMwrC1iHOW@tfx;Y`uOtlJhRE;RCNTb#Vm$hFOyBhnv?=ZKW8riGoYkZM$KrIF%PywXT{Dx0FrJll*Z%FL8)agyL8TQ=kbo0%`0qaE-<a!xfgFC^z!L-Rsnf5sDBNbK);U?OsmzVnAXun}R&3p=q7@uUMjaI_;lu(Sg_u(Sgpu(Sgnu(Sglu(SgJu(X5y-_j2De@i>q@h$CO!*{f!4d2oZws=cB*x@bhV28J~zg;_dVsK8;_ceVOv-m+F$062Xi267u<fyz2%573i$Z?!~7^lxk7h0D=dG&L8jzgqji0yGs&rvxK%KN08p5r)W7{>_8IZD@2Iz7!`I$g7_<8r<V$a!oKypGHFGARc-1h3<=y~@V%EP~f@6+0m~$M-v~+^Z0r$);kb2ieAjewCO*%lfu)fzQgm*~S$<EBj^}7xk>{n{8awv$Aitk8IJCvTwF=DbLEj*~X<jEBi(>%hT+ertQ}xvsl?TnpLJmLuhDmk|8vvSiwD-Q>Fy>Xijm0do-ua3+@RxC9z(e3^*mt2=ohhB^iN!0j8vBfqntBB!=o4U`m>isTtr(GD0;207=tQH3J+;FmRv%9!WDo9|AB*M(9HTCTUveLx3rX{l!!OrX+{f15QcbpGm)@nrxJ2Xm+7#9Q{7KQ0etPvry^nKD1Ej{XVoDf(1VN^q;N@+JF9w&p-XuKYsZ9^Z)jV9!>H~hJB&?eSpcVoM#8fV$aceIE^tG-s|oFUoxx0*#W-TvveL#LrjJR0z06X%qnqq05A3|orVj5Cc{dT9WYFWZpa&8m<iLg0i2=Jv;m&UtR80r1T$gDZGdX%lG^~)pn#i`wC0q;{@?_hQf^NF-;Q<kK$2PtG@)qssiim+C!xieozp-XVG4wbcAr;@Q6sEz#hIP+K$>0(#EAw_r7)amfK;3bI*+8mrNGZx1C&x=D|!W#Qk>@e08@%n=o~OfG3uNHBq>huaeyR+?c?M$rLcNba+*?LyFdo`LBA{+uts4uq8XruBdt+`TGj*Bpwi$>q`DM&9!&yAg)GzW69>!%>h}?&`llrQK6O+GH2pqyzzmBHID`H|SHKw)exfU25BeKj0c})v&AbBGu%tC>Skf9b9O-~GENM*|mb3;9OIm}5C9OfjlGdDINo&loq%~$Z(i$_`-=UtQ&B)c&9MX(jUCkWL=nB%v(Pre`YW8SG-mT`0W^^=Z%xE)0XanA8MhI<y8_n^V3D}}RHyBdr+E}J7DRh1MLnk$^@Rv@`Gn!+@98kv7sUh_uaB4EZ4fqwv05|A5N`N=$I!XXI8tcbQ05}@!$4me?8tlhR_lcuhrw<Y=y7OnF1_~;@-6skvz28TQ?*FX|>OVUCQx_C_baosAYCSqk-P-_GbpNPl1E|sAS<ePgqqEzq4Uk6nOJX)aA03`FZ-6>FyTjT5b#!<`L(Vq3fA>$$J371&A_pFwT?ml_kM7rzkVB9T@1MviNQdP%9Z*R(E?dtdX-J_n)bB$IGKFvC^2Jh?h+-*ALa~%3pg77JMl5B?B9^jb5ldO4h$XGD!;;q2VM%N1u%tC%Skf9WENKlGj&#5mmb7LGOIo9ZC9P4ylGfN@No#7bq%|~H(wY*i%}YXplkcJ-!O3^gkg!=sZ;}$6=on22n`7XoF#$%EfE$s`F=o`9u#unif^I@AY0U|iwB`g$T62OWtvSJx)|_BTYff;a15U7{H78ioniDK(%?XyY<^)SxbAlzUIl+?FoZv`nPH^H;G$%OmD4G*?!$wqN0u87DoUj`Pr5Y1hq|1J~PnMiOGfc{TPJj_61#kkJkPUfn&|e7g+@Q~$04h-J1+W60lLf#6`kAaJX$=cIt0GwdEbK5{dI7Ysvv}zR&;rZ;IYn0oxWJ~Qp&E&u{TWS4BrIvo3zoFz1xGsY_*!1G!?2P{0xPe@Xy6MhykMLKxPUks$m8oOa3O({8o-qV4Qc>)5-=wtp*|05_Rm8FhF&xUq7x@Cm;%v>mDl3eM|9%oMYA9}@$_Q9ri{8jX3P{Ro4_+giX_-is-PkXf1(PioPZNmP@P1AZpEZdA}vnYUu5jH_|<vD76ZP8a}A^BisU$+YOb)PHCI^DnkyXX03<AF%@LNg<_JqVzz9n_;08-Ozy?b@zy?b@Km<!WAOuT000c)nf`Rm&;kc(Aut0jxa@^Anw*B;;>A0sI?E2|F+i_3(+qF}ItQ1=7urGshd8m9UNZ8Y$Tpuc*ss{EvD7U967AFIjy$sS<*(cO3XRm|wMI^$HKmGi_j#F~{bNf4%uV43_bv=3;M!!l;z<=r=2kOH>`>YvU2kEP16zVs$Z=-a2`q*dfaq(UyqfB}8$KlH|uJEhS6n@5b9BEwfR~agF63a5K`RB1I#~b3ZjEg??=g)oA9#?%@Uw!$<;m2j4wplO#IMTT8(>`kw$AzDtMk1w?^tkY^(o<l9Y*{|CY3GO1$6dRmaZO*Pr@)M;lEy`Rm7emzmHcl%q%VJiUl_deG-oACYY9z4FwO#yP;%%^l2CH!O@dHzDpfTIrP*J^^XL+Ul4aLf?}LyxgBpa=^Dj#TLJ4-{5)hh^XA#kkk!KO%&9pp=h;?qPkU#zTkH7uvZ~pQX4E^}Sho609kyQNznuv@<jR=Sm%plBwc4p)TMVw>g21S@NEjK8F9`pnI;ZJ|{k)K!5<7+aasVW7ak(1aGv5}eB^3_a!g&f~aZuxRn{<ea@B8IQwsXOeHXXWa)`|OnAng;NcXGHdDipoZ0ucoLxEwWc5Rrc3&*TYMu$`0U4h{`h(g9Dh#Mr3dRQ+Zlua6ne`e*mYyM+550#^0j>b!8*7I0CIaA+tC_sr)>%I6|pBE3-J_s{8_wo}WNdS9W&w0K4*pUHz-Yc!*E__ig<P{cM`l^7A{T2*MocfWa(jjbQn;OSUrW&<TK3Va-YHJ~tKUlL&aJ%&<z;;8YB&RE<i-Xxh>gRAyMEY8)ztQ))m##c@gvFo<erKt2V!M`l1Z#c;ihu!d?c0Bh)+EC6Q;YfW4L&J?uAZ>Q<j1XExKR|0HOo;!g?Xu_ssM~6TKwmy;ro&q~I6Mze<y#TtPbF$pWi~0~Rf|Cu27uEU0T;fG_Zk{AvRHtr8LPd3qOf*&0`NcheJgQaP1Ng(6K@A}F`9*xh9~DMtkvpvluldMbR%O?G<SwhiYrYKdqdq*e%K$?vJG9FHL#lIVM{cX?^jnyMZn9v66uHT&&IM1vE!8>-(%e$#U+|=x*E$jQ)c4L*>T72z?*!av=$R65qv^*9xY6{}o_~BAVIdai&`6>4)A<M0%y9le`LZ?tq?Q>b8Ij|bDG4tD_818-5%n0apd$uyqGTclnh_-vF^~}@6ETqW4hRD^=Ji7G=IM8ca1Q(sk>eTbOGM6U8uY{=#W+-(P)qYz?YoTDzK~m~W*i#40<MR;VMU_}rW;N)nqaz<Qm>(<8y+{BS-N3yqfw<hzB8Itx?wvL&`Eb}X97IwjulLRC7t{wbCiy-#FEw^Vo7Tbv7|MASkf9lENKlKmb3;AOImY=C9OHblGbG5NC#kHNo%e!qyth|;UC@L&||g!o|mXVrSpAOpwj6+D^Tg>J}j)z=yADE3oAPnSnk8ZigxsVnrcl8D>MU5fEHF(uaf{Qtk1(iBUo5rDMJRdK($Fh><Y^yNFnUX$|Oi3><Y^yNC))_O9DvGG)hO=QBkWUt%<>s*2LgQ2gG1WYhtjZzg;vnFn*EuC*KrZ-zgd?sSab72V+JJM8`4PFlK#f>2hue>w|QAE`9hEr*)9N@QrxfZkV=Vhzt7&+HIKjLHWWN!fQ6n%P`LV*t_VcoCf79KbXgb204#oq=zryEIqF6D_<C|&>)WsIz2aeI!cf0_R8|*j-%{h;pTDSKDT^1d2{4(<vzE3Ictwg_R8|*M?d+`NO@ecS8gu<_{*Ps_M?CPa=ZD(FN0s@X^b*1*DD{FpMCb}56{}4{Q3{S|JPst%eQ-u9&22{*<QfsF~$X)pDy6D^hY-5Nd_-vT(YwaUdp&+CmOsQnwNu$7RfeGO<t<LG?HwSo`(Si1e2ckl>`8jCiImAAd{Z=l?41^SQ?ziku;Nx_LTr&66~fZfM60!Xej_((u69Ih+vXY1rjhznpOo85KMBaKmvkEGpaxWl1WAtNB}ZvS`|pZHOZ&~32-LOr~(NvCK**A0llPYRUiS&B&P}_fSKe}fdn*@=Fv?3LX(B0ncKE2hqw3juWwZ~A_3AIJq*6qzIzhU?gLIX%3K1%$<NDN0<bYA=RA(YoD3s2+I_Og&ntBTurVg*JdUQEY?K5=n3JE^1VwaX%+Gls%{m!Y#5906*{I}+@Wz^;4j3mJB|{P9WLEms0oEAva~ddsoD7T1I)EGIzjG{Li|EFhpa$qB8&!A_-Ovdlbdw!ZWeqHb^+-S@&|(8H2s9r62vT5rEI3>#M&xpU9p!oCazGu$h+Gb^qZpCP5owg?nadGq6eDvvB8_5XE=O=tSiUg1{IUE|0=A$YCJEp~VW(~h&;+$zS^!QIBXc<-2>8uj06;j7F#$gmBbPfu2Ka4V05MQkmjsA`eqGajVyN#FhDesE6YO6DsHo5FUjwM9v+Q33!Z2)J0>G#f{8t0gsL$<J1JJ0m+*c#&FwAfw>M-1JBIu|_j8+64)kuMgr~?|skcty(6hrQ5s8I~LsDVZ?<Z8w-2??0PG6@Nwqt0;l4d|m9&b|SB)M?JX0g6~=Dglbrc~>*VDKu$+heDGXCL{s37$zhEw@fo33Am*_k6a44r8z_-aitmgI03J;8Syv)sx%`WCqR`pEgmNTmu7_11l)q88^V?uwm1>L7``|WzDzU5iCD%k#)(*_!5%nLHrpncVn<NZp1Wd4EMpnIkeXR&_(E!C+xJ!q5`a%5{XnS7q(fZm_lbo{ulGrXN^kd3g-Y-D>4f^a?Dz2m`nv4*@ub5-l>I)QK+BjNPzm*n*#VY7)0iEA2z4^q0f|6InjMe`wWQerfpmBoz5xWG+AE+AIwvc@jt--%H-H`Vxi^3t&|hc+xItIW1_-0G^T7=e2K`QL02+|($Vpm5!^-~529+MGg(H#~R=E52`^>Ofq$8PuKJ|K^8CDCTBs9>c-tI%g%1CDe(6B<(*#I=G@RVl-)Igtm1=K*Fy8~>X&rK>xSH_m4c65c`Y*IVA!VYCZ4fMHJKn*Kn;uS!{3U~GuP{YccxmExTmb8WjOIkC7BdwWXV+Wz&W@Iy*$^vHC45zYy88*YIEMSHW+KHw6%&;-?OZSmsGa_eB18IQRAe$sW5F50HSpY$J6SM%Hpfj`pp4b?^EdVE+2|ACY;bMc}vH-f+7`Q9|E}RL<sIYW{s6h%#H-;LduynIxuSlKg2BC)3nQrW$kJOnu6LcO)gUAMtp^n<$F0tlVpy}$3bLq-9j9Dhxk(GUru9NJ@>M}^T$#!Hl4MX%fc4RdV%Ih0;WVH<ATv#a03EesmUx(o*xuMlIC{K4ot9=|}k{enbm-#zxXmwoMS8iyp#IDux1Mu83?Nl1m#xFo>{%_zo#`p<H{qb+$C_R1y(mLrka2#m-2wWMd-FXLxy`zmQ{K`P>am{=i*ZP%l8ZDY{;}XC0OS7ux+eh~G{O&qDjz4|}W?8JYafwf~So^ma!TkraBIV38lA+QYF?<0-r5P2lnx&Fa0jp6eO{;*_Je8coFbz~`M!lhCsbrKJYD`Mgstp5ZO3smC083M>rvhqntfvA_nrA%~01-50%z%dytoS4xG{s;q03yd=FF>Gq273VyC8z2(;Gi_4>NWtPWK`V-2$ZH(-3F|ajH=s!b<+10!xu1)V<M(WCc{g0Krq?qCea9!orHHyEmS()r<QEp3Z(n&LLJ-EeRzS6Z3*B?w(bNHfEVi7mH@Os&$a}hC0lm_2~Z35BufBWpeI=Z)RL_`fdtrvdRHX?FBz89X22`n3}rwsbcQmZmduKGGoTi4jb(r>bd6=eEt%EM<ohI2jCxy5BE|7w)g)5jy%ac1Db8)0CXr&@rb!Z^(ttgRQ`4f^qc934>`@@~Er2$PQ=$>jMq%f?3!sg{s^k`c7sUvfjPRm7PnnGHq8Krg5l|E(W-<bbLUx0*wB`v*S_6b7t@*){*8E^eYhbXXH7_{Qnit;jRnsIf#aB%eh2yKHfnuJonx>2TLaj)>PaxH(!PWp$jTj`&AJvFK3izYW$UzD?q#8j;0fy9RNk{>dR3{24pc1N0?rJJ@e9Zt$Dsz0zfJ*9&jGur`s*&*%&`F(^@e{C0H8OqzR;f;QO#my^$*u`#rA{alDL;@#Y3wei8pb7>ahem4Q;jkd$74+MjpH$<`KB3uqMB%$VJE6#r8!w309_h95(Mnh*r_{Vm*xar5P)e;U_?MLjU6cyW@*f`p#o%S(9@Na+cqabiPV}jcpFD*OqyeQ8-R;7K?Gx(<E|T!3;bvja%s?mnH;lF?FEoaa~h%o2x;tM2DB3O*GfdX5z?k9qZ|2VnlhlnRJ%_Z)bOa^$BgbIU1_qQPrcqJ3(H+9Knv*7v;vsuFgtDoFkv}B1vKF}Km|0>nbZ0PV4^#IHUU3$b_ccre6SoC1AMS77z1K(JQxFDaGVkYV6dDL17L8R5(8dv+zbO;u-ptaFRZT>a;y%CNM2Z-Bw7s&D{PwU_ld#smeR!FSW9VOSm7T|?LIK9PGW8V468$w8W>h5$Tk3m)xlNG3#*e38UVw}@T>t~Se<C!02o#$aW^1_mEl<jz+f4&1;Ah#vIWGjGOSzyF{}*zRsal^+hsru$lB~It%<>r*1)hiw;b6h=hz;WkYwZjW3$RSC24Fk(wj7KY({vK299l7c9X^r=*<PXZ=tCb>9>V;PzAup=G;IPKq8wHZWo{kbb}(b8=G?nMQ%l?85Fq)*%(fddyvh@6%4RsgIGfBMxK2uGitL%AIproYmKjEM!mKhLo8CqvAyRcvd!zR&5nb}Zd43vblHuHK@BK73!VlA8avB|1_c^BjBf@N8avrqHd2$ZBNE&QitI4qo3IF)kQK4W?$k*J_(8Qv`z+Na9W6Vo?<5^9yOA*;5XX-8?hSRc&|f#{Xo24-($TWR{CZMsK|g?`+JgPMcT{abwMn%FofA@Rv6I7)lXU-f<#flm^<#%2O|nYQ!@#rLTYDL#XSuibI!L$Y(uW^sZ-aDyE`5B-eUM(S%ns2XmFIERVVn!YMr?B4w?X>3CF@anAC#{xS<&pA23nVKp!9Tl&f4QLzA|Q|7U%1@P_L|5ae3fzpmEt=d9GrI^L1ReSDvfX;d~v}?UmK)og1FRH(?zY?v>Xn_Agn-#d>A0ic1gIakXCCtHNWx<3Qu$z4BPaHICc3Uaw46sp<RnkzF@WnV<7O<Kn&YPsN_^+qhn@3{*oZSqPP+iB!@El~`7vno2AaOHC!o$-U83lAPQdO(pcH0f?mM%c~J8Nsj+RfF;TBe+WRtn4XTPBtbI>f+dL^NfHn-=4VAzlAP0)085f_+7eKSF+b;lG@>MU^g<9Nv7;9PCC2>hh)|Mq<`5uCg6BsGPzinR1gIpjvyyb5N*wc2jUCzOOwrVljXFXN9oZ>t)6kKfx;70RId%&<7~_p*AzhCyxx_Q&>-WLLn?VgG(D$+fFv(8iP{1P7-~4%ajVqpEWe4=)O`--CW-5Ft!VQ2WI|aT0vApo|8{io4<u^bz-Xv<Q$wrlQ05X}C^)$dSnU$0@fH9eslr%sw*()je+Yjl>-{2SWAvEte7O9$d3T#K~_koAncJ}+k18qA2@D!u{Me|N^g4H$5Ag{el=*3dj@Zv}Z@M1}8cCn;2msrvoL@a5|A(php5KCH9h$XEF!;;oWVM%MEaHIpGu%tCnSkjs(ENM*?)<;!x!aLTenjq?X<s)@QUyCM*YV@^el0a^#KmYNE4?p|J-#S%4fCP?eG`wius54?yHF#7bH8lW_IxRIdz>qh70p};sv{H@Eq<~hc)1wjKN}bW85pYX2dNcxVsndEi0*ayUfE<)mr=>pNm^%9mD5KMpYNbMv!xU>01NN!!ou<_HPE+c{2Av;#{n7ktYx??_r8}oAZ4N!5GM6?Z_E%F>Gh%-=JT;@sNyAf{5mc%1s2Mqx8jsqHeZT7mknq%u9<czPn&Xxp@KS>{7=(lxtHB^7)L_R8A)yA#E(ifN*3U%<sLjY82;ip~*#iOlys?1KPoN2@F$4Yz=%*RkwgK)mZ*%{8H&0ocvIkt$3{&=ii!5o)MUJ$ln*NY#l5wl#ILB(3ahzi{%s9@m8fLm<^Q9rC&o82B_d%yyMKtX`(0DVbiKfHmiwcN_Y7?UAj;%_7G~Mv_2#BUT_UQr9bjQ^^K$`n2?dQMv{L^3k<A={b|8E~zZdpHrMjq&<n*s9lhex^@Kuu?7x*0%Ccg}P(Kpf}{oB_B{XW#<Jg=!OY>GO_szMP=%te&qZ=JH$z5YWol3UH34EIG$gmYicLOU|*BCFWSl5@9T5$t;$#MixgpAQnqn1B)fCdBu{}ykbdfT(P7ztyt0;LM&+wA(pge4@+9Jha(-(h9#|O!;;ppVM%M&us*615-cy;WYo`Wv(9J0m5}8{tMOv9EMFvFJhi#a_dx^N+~)hBu~~jKk~B8QR3-uL*kDC>0^kAdc@qGS4Z6J~KpxQhHv#g1-oFWu2ei#ifIK!B3q{U9s8cRE0HM!a0DM>uzX5&F=O*_#o0E<i@W*DPV+Q=OIhm&cfNU&n51dl$4>_P3)hGLVCM)~H!WMuUJ1cAfwY$6J5F-iW>AV2cfb){?lLoXk&VVhLNoGfdCHuo_B61zGvvMMG8^eB$r)du$<LT6pYZ*8-<W>f{VH4P}e1iknpx(X-zy|d8O@KA1w=cO^q29jaW(9itX22TM+qVGLpgy(**t#vRIjE$?$-N7l+o<*mtlOw5=nA~s79&+E@NQe+)!qio+o+A~1`ONaFK{D<ZS-fd6U#RGJK2d%+hSy)MmB8=EWOx>Q5&_4-H16G^o-qzIU6-!U5Py#HAP*CB^z`_U5O>z0*@6oV#-FXP&Z=4wy=YRjTo^}gW;VxvC-ekPOR7#c5bnQ{XV@`1mQ{R-9Eim2H{ET%|5+W2;oWVtv<b13SntSJAHbu7{b#IHv05lIfSPjZ1d^8f(TDL*yYoEB@v!>u*s+QiXtrSXp2wpl|^{k!499^D~#~Iv3i5gv(j?O)}P^@o@DQz?m<`)A2=R_72$$6iJBKI4_?g+8UBThfMNQ}FAOT2w_g}zSo0V`1~VWnsO|M2PTCPj|Lb9p8~q5R0XAhL<21sJ{ICv+w7{~-si?U%O|sMs5?Uid$t>5N6i#^B0ijsh0ijsh0ijsh-!8W`h|asQ6&;oPpj;k@c^#G4LAgGT!8$5$gK~SGCUv}$+6U?WJmcvgy)T3GMZVUgPS)e-X&C(?fs1#t9tX<9K>Ms2EQ9n_eBO=o;G=XMrPK59s-yO}c&`HUCOLv1haXq?Rj3|!1V4^6uK4GvdS~r%&0nSJ;WEH|T=c0wf9~&U*JWJwX?^wOABP{8ecEQd{NqUDx=;J8NgNmcRrDULrL4=i@UN2hZghelr9ZN1=ZDheBt5R_tE@dp-*p)m@m18`R6BUUJ61NH1|BOLPZN)oji-^v3b512V+G4;<Vmks3Y;H7a*q>jr$NUFg$p>x%4!Qh=bd+Qeg+LhPF`F9J5JPEKsQzbT0l4Nyp{7aXbMV%u8(gef}q5l*cJddi5ZD4fM^mk5?cV!u*AFLRuK^m)y@EEsCEHNL$wLiB-6O<JDwdqFmID!<J>7|u5ohxG}bt|ewu1vyj!~uHC8s2h8icDO0$X;bEsj(3h4`I1qNz$04o{#f3E;SGOXuZ0foRNvjPgqMonY@A#~BK050IFSpi(oWwQagpzCG>cmdbV2JnKen;qZ<T{k<x3%G7}Ko@Y`>;Nw4y4mmZLU9UeBrjOXk{2vx$qSaU<ON4r<AS9ualulSv|uS~Sg@ouELhT-6)b6u3YN4+1xs3^f+ej<!H|wf!IIXXU`cCEu%tC7Skf93ENM*%mb9h>OIlNcwRuTMsI$sfLEVTIil_OZItE)BAnFW*Elm>DFxb*0fzsA~_|so~<b1g3;U#Xsw7q;EH|h*)=72k@Va*(H$Ncwl9$&)=%)rY4PO9TK9?(f;f9qvHCl#Iu6o4mGo79R_!`CSSlsdosj8unItNx7Cig=T#p{Bl9EK=Vq7OC$Qi<oJ5UwsX~+C1->plb?hj=!n)7}F@!=HOQ&#kEc_okpYvy_i68ZJXgzr5ULiCRG}Ln&VNW`KQgWs0#R}85UIm|InF9fNk1y=hyQ<nsitW-C0|c4ooXdfOL%cIS-_<rx}J`5%#p_hF%f%81r);Nb?QNF-(AH8mnm{wIas+oCnf)(_ryb0({e;MOg-bL!Ud}2bS&ti*7yEz|vo7ch<myVujG9P=}?l^**q4rwmzxN}u5#tBIu>?y(wJx>G|PfJ&cX9~%%$H~eD*VChZ`c)%$A`Nz5;VCk?VoDd62p{$5e`g4c<2vLlwF9=w=VdWn&N{0>Yq@a~P_W~dVMxrhNOK70t0<Z+;tuBB{Xf)<>pGwx(Do)ndDo)ndDo)ndDo)ndDo)ndDo)ndDo)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)n-Do)ndDo(5{xn`7|Y>p9%WQff%LXixyL04*Uqp~?!<C-F<bh?ibMx5Ju90?U0g!=@j!pSZRsKS_@gf3TTj1)Pma01u@$Y8(B1@+<5Krqr@OM}eF`GoPCS<v|eogi{P;Uw!t++j^n1{C5%_(d23Bjqx{5bL8uE>!482VAH;4VWuN@yFA&Ge9OV?F^8~?o^RTFnOA~Rqq1|4Be{t`2=Qe)%!&9Y+BAkXfi?ba+cO)LKDM?NgCBAWvn!fjFhp$G%`}gO4G<l87oaAD*#4d8d(AOLDR@ci7HJaBSon@`BQvHHK~@g<_$|)^M)m@3B!<%Y{{0_>^r<rxxkl<26}a1Oa`6kIxr@q!EY;YCZoY`E3h1czmgSrj?rJqMqJ0}&txOEWAJyf5j!#ZL)nR;82zQ}#8PZwmeD)06tlDgt1v@5^a``I1G6woJ8%oLv;(^^OFOU&v$O-dFiShI3$wHXyD(?%1RH&NcuJ9s>dTazoRok7671In#|T&(RA3&oNi#4g!90v{qZ=61VB)DEMVMHe+;89?Be~PSPmat*>60US(Zs$v$X?Xa4p_j@4q3p`4p_j_4p_j_4p_j_4p_j_4p_j_4p_j_4p_ihI{^zk4W6rdPt`0iC0!|C0w-K4K!W^&4F<S&ps{e^-eFECSbz;qCRjub`2{BoazBA1+sFmQ<F`YyTIlN`=`0Ca1e0`@L|q}tT?I%qB<|=LU1}uisY%Q^9{#p6y5C^Gt&HwB@a&MnPW<B{rJXFuu%Oyb8j?tgJKc=IZ>%@IYi&N}4IZE9+hw}V&8Vws8I<Q_)YX&*<@z*9?)1S(d5~_;r4KbUsSMJO<EqZmb&!6PR>i)w$46+xBW#az1CPpmP~IQM#~qc|LHR0~?oLhOp)4+Kqjq|(efZ-hjcfKQnvT{x);zA-tK7Ls$!Evm$EAH0M#q!Sjw6jL{VJM{PvW@LucGO0l>8l~$EALiOn1Y~>L@)f;j7fS8++<edR)U-F>^Pz)T8vch_6!S?pz}t7I7XI@m0*+9qq%%Cx2w)&Cj(DyI2_)@m0{=9qq&BTgDYSF=_5VE;l{I0)|P?3nBxCNzZEv1BOXPQC`3>$*9Q-7=}ux`wWvDt0K)NZ-u9&`w){1v!noG*gH8TfCUhfV7(!Mn0MaFhG56Yor^#w!J5Ye&?PyxOaZ#Qm1&m%<G@V21Q-Wq+9kj^Fw-sp#(|l31aYj~xd3sj+_?a8tlYT(alW_Qxd3dk)37TmPXg{S0`CIuF#_)b>@foG0_t%R-U8~O((8Tdp&?l7eVQ@S%p#h}@YtjSn#oQ#VFzeKqoq1PmJHi1SHLV(djrfu=VSxS0%PhnfFe%ZTYw_;eq;kI0zZZuU=jMs+5wEvZ`KZA1ir}~un4@2+5w7WSlz$hr;9R?E*hbWGRt}$a7SThM1VUAG}5m3!J|y*#|;3aJnzR1_@g*yXA(ckgnrzJL(21h+z3O8b@Zpnqrg+N0?4B{=ZXP&6vq)g0}LrfQ*neLC@btNtue%s))-<*YYMTXHHBEx8bT~-%^;3+z#x{iW)MeOBS?L%`lP;AeNx}6KB@0jpH#ybEI<e<z1(Mr>KOfMh?t(Nbsk;wg_Eq6(H)LAhZ;AkVU`@wMm5ZmBieW&RgF}hc&Tcn4#k^9jU@HGLX`SmAxeF(5T(9Yh*DoHM5!+pqSO})QOp#(uPaYdc1lm4rpPsUE2Pn;O)xJD7^giqFAET-`OPL>4=*vO8QCxa2DJ&<FaZv==h-j;4ZZPN3cw+lj938w%*Zc{ILHVvj5uiin>mlKS;<LIj6i5cgkpq1MucKSKySPna&psHRR}q`X%q6CB3^3G^PD1FdgF6OkgB~{_|jf1d}$N9lgi?hy!5Fa_25#fzgF^MrBH#3C>rJjDqy-(wIiviJFfEWK00-$8Bw!ScM6X*7InwpxdBL`(Nqn<QD@ac4Zu-{)j}13Plp976@X8Ng*FWUPj{-E8o(bqK@FfyXB9mSpiOtG`2wV|)@uiVL)U8u@Y31AUI*+#zrr1`ODDHfCuz+j>m0uqR3o#pz)gT7t6}^W5Xd^gqb4Ac^|?h&Kq9MQS{J~_I>ECpfROdMWnBazD<flaHnT!w+zPN`onXro@yGhymM6lG)wsY8=wqE>TM|&nYPgmJ+_AC`eFfNINo(w|q&0O|(wZ|YX^k0<bbuL_w5AM4T2sdMS}n|G_-h3)L8bG3n4r?>K16Izq_(Dr%}LbO6tT^&S}3GmW;2Qw3M!59rceXNW?cUVyn&<}s)b=Q(oikT#%|t7oeO*Hjw)NWSK5?2s({(p{R^pp+2A2R=~Je^Ceo<<&TC;E&D)C|&D)C?JKKvFJKMaD=6Y$`f-ZV?=b|SY<ukkE79(M3cRF4q3&FTDaGpXF#lV5e4vk5`fy(~;oOL6oDpuZFfH_XyT0l886OEL*?97{kl)BI#3~4a3elet`h5lqnEerg~kXjb{lOc5~?7i*?W~eqP=%sVA07!w$XaS6}GmD!AAPSA-TmYi%tjlNt{&36R%SYufGW_hIOC6kd2I@+1P+JFva`d@@w+c=4>%dWtCi($$6&&bC>{V!>-%8Bl=<j4BZgKR7vJo3N7#y|{A2>@p@PV_m10Og`JMee2v;%`TOFM9Qv$O+?H%mM4c(b$vk2gm<@_4hf1CKXHJJ|K7g#{8r+2q_GX#hyp1(F7UG$EfQ0)g~Ao+Sc-#P(Bg_FzQ?h8*BT1%@EtL<NQ*kY-<lojWlDR!GK0*m<Y`9jtkb*ujZh4B^3vTny>qg<k-<n=yX@q+8jX$ACD}iw(<I9Qn$o7h9IGIC7Rv-%HbSz$bZ*0UP6!Y}Hq4K*`otsR89_@FK|Xp}~tFmxl%)f?%G<(Rv6}V6<K)oRX~)qkvPWb0dNfXrqj%gZh#p>VU?i$hn@nhayXQ=y{Ah>8Up^a;2xHzNCd0KRIdQP0-dC5d{6M5G%GsEpiJX2>Rql@o$&VJ~<4q)IoVt7+`6Ga(x^;cU10!^5ZPP^F*(Mbbl^={Pk^v^!i--@GU9(AiX_JOgl-}Wsu%qOr1NAo`%t{f&jTA*Kwpgj+AE2;kbHJew>telpdGwRVpCfq3XDRuOj~@B@P~kA6NNR4j@k)JdQLj`qXDl;<)M`#{!;zR^zIF91D2D!8We?$FYDXL~i4fzKR9BaWH$79@p@+RKWI;9e7qMU>g_lv{b-0F5-!)fH%)IG`=`FfEr(%96*gP$*Anq_>!FRON}qdDb&;WLZtz|&@elIFK=bp5r%<Tb_80IQ)CxFOLB_r0&00H%WeU5lZ-;YfLxMM=og?$ati$dRCz0oa{){Pv-%dmG|A`+3YaE2T|oiVSUG?J)L1!y0n}JIfC1Eee>s2}Z1Q`iXqtPR96-%I*)c2A;NwILYVOI7iJ0b|3{CXweeTIlV1eeI>;x7BJd+(~xD4oqzSRuq23~h$05{ela{w*b@v$lZVXVXKfMMW`O#ujFB}o>*DfE7&08pV9LluyUH9-|%OLkoP0&IczPZdy$wZI6%&;<slq!<=u8av8s*ijrdkknBO7f?+d#qiJ6&{5zQpx=j%;zZzT=qOGCZU7zhu~)zug?&y|fEfj{zy>&@z%R%KIHMTpx&c`fcD1kpuqf<mVFO@M;1T@}SfapM(jBk_{9^9_CEzD}2k=lJ`R@Q8;C`?Jcz_$i4sd~f|MvU1P+u!9sjn56SXqCX7p$y54GdP+pC*Rt)COu|cp;Dv+~9b5eB_?Sn!*4vs!?4TAVz(!xTHE2iUDC%r$8}4j5@z?B?AnpR^dtpRN_sdrjlwDc?M7d6ACkc5|~h!0hGXmLUIpNUo0-EFBX^7{{Y1$ZB9>bBVc2t)oHS!()m8wQ0a7^Y^d~dpKO}rv8l<Xy=02G+{c?{xO@gY!}6#);+X~=L<!KemmEY1`7~BnMyhHXtl%Iev+R|xh-&C_6OL&wRh|&up>s!Wbf`AD(Rr2#xT4D(6x;XnAAk7pvyZ%;s-Hj;Qe$;N<jM!8H4;8DWBdL#lV8!nw2GBJCl?vr8g(bwM$=MvdY3gV^%>bPnwt6x%j*09lC8Sao~_xc&*;w9?9}}*(V~affYpr-?triQj1KOAv*u4<L3J`6TJ@1SnLfk3D1fauR&POtG~Mtx3W%(;&;(LC(~U^+fU`RMlZS9tf0&6)IO~m{R7afE9T?J_)hA>af2r{`6b*+)jLc9dAtJ1G4q-JySSvh!0fe<a3>*gyQLA;DCJF25(*uTDjnA1zsP*9&2h<6(sqYAno<2U|q?LWH2p&EC=@0~3ofFvrfmSC?CO{t;f=YU^SI1f}fEpN>NqVtYC%G)3n$^kO3aAFASuOx(R(9vT07_Y5>DvM@1qBJ7r8RUo(i%FpSBz~nbU3+)nmMdoM9msjE}~`)D;H5S#^zX-X~=jXybx6Pc;SVly2qNrfI>FI^ev!}%_$tx@Ug+#WK!L;IWArSd~EYAiO4<JW?2%ETQP4EHLq+=3691U_PaXOW(K%IwaMYjHY0sI0GExGCz0b7n4n4yOSb<2Wj-&)5^BtGVhJ_oII)D9a-3K~4LMd^TfI*_R{WtR9vIeE@6(JiIp=XS%+LU|3Sfo?w-rD$RGXZoSV4IK&R9Wt0nX6pCWk2~x@|{iDVDTm6Gu8=6H8j7i6yPc#FExPVo7Ttv7|MSIMRVt-7?F9A6(yfA%TI9-C|YWXeYbnVUY&_j<mc`<pDq>S>DUq_ilMur2vrRh3P8@RcNpwL6x-3xKh@Cl|(LiFs-Z-mpn^5aKE#(1N%EmJMh1=v;+S;OFQtjbF?F4J4-uowzISYXFE$faJI9w17|x+J8-shv;)dW6OT|(m97<m7$8V;ddxL>B&*3>Q$=!2)Ibdh3@Sq=bLkz!(DO3{e396ZY9V~#gh)o<kemw3034E0lN5miwA>~Ywa%(oQRQr+KDwlKHbL)jQaqceSvD!3O>fy{lPjJC-IEI;4rni22ysAvVdSOzs+sOYH{JS$anr)0yx1v-Wtgi8B*Q+24iJR8@pgb9(2f^)%+WA8;4ufI0Z)E@5lc{0#ztTw8+L&aOi;JYMrZ=sZ8ky^)GW6XoS?6>6N1RBf}#_E$gs>|B?Lijl~+O#nbG)4z#uakUkMmwcmlr?GJu=UO2~ljJ{utey8Rr*zga+Ey~L@JhHV>^Cq){zeNe7XBm7Q($M$8AZqKC;x7R%l(vQ>4&eD01UY{hyu>*kPBb4D0wx`)y=XX*E>HWF%;g{6gAbk~Vct`uNsrEi<r{^#Hs6DRQt0==sW`M`x$EAH0cgWoUk0Xss{VMzrPvSbR^{Zq<YDvA0YyEkY;aPiJ>}h>93-mbrxX`cS4te42ainqGU!@=NNgNmc<M_k#&uU!vSMi58*y||$k<B_k4sAS2k4yS0{Lnmo`0|0TYfX>OG%o(D(8L>;Fzr6}Sa&eG$yQU5lfkH|$jM;TP~>DVY9>lX4X8$<<djcp)JabDq(+_O6gUQ`lbiy_0CnC95=;PzV31$}xI;rX7XUcPspMV&?a&*G1>nwG7ZwY^A}8%JKprOzF<=}g4KY9*D-AJV94iemfE+6gF`yjl0w<uA@9+LbvyF4dqT$6!4%G0HjX%XSyjUmOnqI7PZH+H^{@-~0KH+5RPrQDgcf1+YyaVrfI>4Rmgf|5kljob}cYr$CGR^M*e5^?fSclzCF6d~-y5kEN=7pC}j&{74PmXrHNz~lq+>-{_lbur|O+DE;HPX<Nol_&tJb6w_^7e&smQ!AFdebCS9H%#pLdCIR(=1eG*sy6PD%1O1&cjP?Do$*JhN3dVh)m<q8<Up-G8J|>nE^5tXbD;XGL;zyeE}EEe>LavH7ymRsxg2im{VH-E5X>q0#K>Uuoez@2u3Rw06@jL)D8fs%y3W%NT|%P$nE+GG%yvz!zBQwV)RM|z*Hu*O77pf?*>hinw#oFZmN1r$xU@er?TcJCr4A`Q=QQ#tnsNDzdTJwmG!yQ`(RX!D^1Nqb%xh>z&zD(+76hf&hTsw*r&dLj1_QEo$x&?`m{SBqiR@)2V`VPYcjH=H5pmb8i*`u4Mdi-<{?X3V~{1S`Nopgd}B##zHy{AuC%{b$xeH%WT(AWveRBG*=evA0vz5@X>fScVDSSuv}rHZK9GZ(#%dqP!3}#UD=OKsG8h9ec`M5>0W^VWc?qCNgNYHOnx{Q4N$RL%hsKwZnw_`eOG$B0d#|{sy;$7SUM%iuFBbQ-7mIt^yyBkj6!&z;qE2&8pMCjUNd-_h?w%_t2(o5Svr#uHuQVEU*a6t?qfwuqJkajbQ@4@_8ek-E3N<8k<Ayz8r2dxaH|h84Mk7YRNRD*CNS3rlBuiRDktMB}$dcBmV@Ye&v7|NWSkfAFENRU-mbAv4{#wV?>Kxxxqf}>|lgZQw%)l^0KrbshG6L|j!awxE-P5xSzm;4<t<Hg$B$U-U@X}1OIxb=XldP<_juhOiPQU`Gx>;e*8mXvRoi@IJJgf=IfJ0U%Z6N@W)oDfyNQ7#WQx|LU$r%it`~{H7%DNdBKqjlxD5uF}b&Mkyz$q&{IbQCA%I1JdF=}I+AV-ZOn_<PHaRlb#fqSM68q9%vCK~7ldc!x?bOc;*HrO#iFl2-6GUWb<K6eHjvawE&49J82{K&Ns{r!=9As8r_0BdZ}8;jfoZH^B&xfa@>pAZ3$%}81fP{Wv?gt%jKBAo;9fFDN!9>)AE2t4TL41mWz>!1QK$L=&6Y3SIkRvbwkR65<q4i*D<mX_GDzj7meegugpFhn!m$CDlQ_mJwA{b3m}!Ib@l{vLudFocw#%ntun$^d29YhO`c((Ysf1T3?^R2@V*n06zcAfO!fS~gUuYem8an6tlBOGiq2cXm8NN_uxz4@OFQccYCVK%RX@iT@AgmB7#_KyX)-7AHg?@aLo2D{$yrU~$6=Jo*;H?>jK*V^dO(#@2yL9}V-|fK4C#1#ZNqkN!+{;?qZeCp$6VgO1-jap0rI+#9jrqb9=}vE73%!yB>PTi_|xO8oSw{q9N}^%iy(uo6o>wt|+^ln17I3p@bWh^yYh4m3C7s<%KRw4K=M(cj8WeD#nG@JTz^?-SgB$bO&T2GqfR50e~$sU1yn1g3U41QA%)vByRxbufT3p{i6YP8yKmgeTN_%w~K+UB&Rh7t}C(3}B7ECkyHr_OyfD-qH>>drLdm>n-hIueY>=t=`fOc6v)Y*y%0pV57IRgMHr74)*!{UgmN@0r}yrj;<sL@PPSWR$}mW&?Xixpg;pZKj;L0{QShmpFThG@uwMS$jF~Q`9g?+KKVkBAv1#;<k6p>UoSUi(x2h|BXa47!LG=CAG(es`+Z~j3v=VANqfkTpJoIiLw@??i4X;S@=TB-KeW}#ge@{*i<9>D?XpUf6BM^RC{IdI+{&O_A19w3mFuAVI6(1KTe-DC+Q?KpO7}tf-AJ|L=<6{0v_!SzK-)0TK5GW|LHa65kygI$%P9RgNb#&aF5Xvz6wkwtD|}Xv;(4TT#Xk>HJZq0@{whfE&Vl>kd$Ny<{&|w(S$kaduO=y;haZ>ytR%(rNaMPHo}_rz9vA-OB*o)i(w1@IKTcB2C+UxD+WB!v<57BC(^pA~(8IGW<08HaM4W23U+?pdlVGTM$4M~MyyGMoYTj`Y3^ndp35FVXtOP^NGRbL3)buhbWUlB((3E2ZGzOTHoSw)4bCT1l7%<FR;g1WTn`E?025^&LEoB05Lo*o@fSb26851BJn8}y`(j>!MFCZG2$(R7qIJt=t(m1(^5z{!ii4oLH%uQT%U8x3}Jhkz+-RB-Buu*f56WFM^#|doI++zhcYVNV(1~vE4r(W-K50%~k&(Im!0MEbx#tq;M&G%aY&Sa;Ra0SdlGw@abE!io744}oDpbZdAc1kS+GNBW+12nNFXa}G|Cuj$x0#g)s04mui7L7m!CN%DVQ!=bx-0!0YjNk%nQ5?5Z4Hw0!oz-+voYGm17lk?80lKi1C0tm_k}WJ{jTVk{Ko*v?CJReigM}rnQNoheBw<Nwkg%jRI#|-094u)K4wke=1w%R_1xs3!f+ej%!IIXXV0~02C)C$!P3mj4CiS&ilj?LgXiBK_3qtCBlBiZeNWBjh-V92zs8%76MhmK)0b9^1$p9`Y`{N`7xTvr{HUYY*@DHB^@S?&T+zj}FY8L<)^_AO|^D}4?Ib<*X<UgZ-odyx-19Toqa|!)z6#yoc)p!&DCNQU!T(wmAXEnKMsq?N{zWhggT~5-SYLfPf>6vDo=9r#o*lCXGnWmlQn4W3cq0-BJlxZ)So-Owwr-9GpSy&=YGrp4Nfi&<mrz<1?9vE*)s!m|OB`G>-jsbMQJ8wk?lB$yijnzoi3DwSki<)CL7x2zo?<E5=f{~6HpirA&a~L5JOe7@bC+)@ZllEfy$@iD+r%9+!%r{0?MBTc_kvK%9*ZVj`WBk_pIMf|iGL1vsF(uQOL!WxT4?6UzcYro9GjRuG(;c(30Bt%#=92|nz&7-`H^4TXo%3!0S-Rt*79dN9$6G5v7W&*PK$gx9zgIva-LZsU0he^c2QK1~{@eyG;*kz(#K`3l)oy@CIxOmG_Yq?y7gLQegrzJI!cvw5VJS<1u#_b~SjrL~EM-X#ma>KiM>>E9OIovoC9ToHlGfy4No#Vjq%}BL(wZAAX^jn*w8jQYT7!Zi9dUvstvSJx)|g;PYf7*_suB{m_pH)1Lpb?&njxJ0JIxSI{+(tBEB{VI#O9PwXo|36(=<j{sc8X6z+@`Y)w{t)15!_7rCyQh5-Y?n;0hW(NUBS$2_jc2bb?4DFP)$TfQA)k7LW!^XIubjI4N}zYQO}=1)zo#J{Yma#)@4Qz#5xlil<@2%AeCXVdc+hp0M)gG*DRibDAie@HY(<?4i%n5-8qDgz5x5U^E-y4j2JOxPwN35$>Sc#1W0gixCgBx8lW!SDF>g7Ep*4%@$C|ZWtW}5VAva8sdDmzhq8B9MX1XPD32hjIg>0R*bN^h*gZRx`<Ww{~*;I$Iu$b_Z{5Az&xmmEYy~VzUjnF&GORKZfeUzmtoMhlPtqtZL9X|@iXbzfeBF=-PGWWHF8&zpqnGPtnnftBkMGp$48oi>CcgL1>@IA`hw}}B#psd3TI?@X2ozuhGz@2FefD*j&^8yW@!hOXO?zgd1h$`mS@hp3>Y9i1dr;#L2?3T0w_o`0%rm`fO&evYc)Lt4`3jl((`t-2nv!D#S=k6nvum5!9jAucp^GTP8d%_2gwQJiRd6XVLTBYBqI$bqJ!kbs6=>>oEVh|50Vq365&Cb5u*}u0t^QwttkiXxSbg}qb94LITLE28K;?G14_s{HOmLs@HD5c>q8Qa4bP%~8ah+R))kY+hNsU@_#s>OSehH2K0k47&+OU>@dI;l>?n2S;pB7_KZE}TmGHyUe?cW2k&V=b2qT{T16Fit0vFhdY(iix+lu@@@RK8+pyJ43olXn#SkKRIRYQ`<>>4Z)bja`?ED>}-0eENaZ&y&B8-UlAJ}A!#z-!AoD9;JNYs)q$PYS?m%RWf==h6qXOv@m>K9@fHJW?8@x96dAN9jCB?~gO*j>=_FzKpYj1$`~mQ9C`I>|@bgOXFI+%Cn;deJzcv@hYrtQe4_`_;JZzCD`$}wBtzQ628i_<C8e9;j275SQXjwxQ4Id>}cg;9@p?yR2{7@%;Orq%BH(<c6pQ@7x7gz-JO>B!y?Y(BEHI|yQ6*h80U{{sQJ0}VGqgUBECwe!}el%T%q&h>9n6%03${^T>vBOFt(pIc1a^tI^V|;DxL1*2$f#$<4Ag`>T|h|E#x%vEG(hLIg30Gq!}i`vfKqQOnPqZ6(I}^Ya|5oRwf$381lo~5VknKtPMd7&8;I812f|Y#lXxsLNPEij!+EEULzD^<<SKcW988W6l3Ml1r#$ekFI{9Ygr}A7_o2x${4Y50m&G#Z~@5B(4cl7WSqpg0A!rRxd2d{#JK=b@+;fq`4Kd{WWyOKU>7GGErOSKrtbU<nsS_Uyog@1<Ej+!3ym}DfLOBQ*c1>;HXNHGWTDSp0khEOt^itKd|U<00wdlkK$gsoxhf!*%#OJTu;llE1)aT=IV~@ZpiF_)5#WxfOejtXpys<n{P5GyKcI(~OjC@imw;)?grb*#ZQ#6=`)E_x`CtLWQjAiL2wBR6N{$F!(4?QGHIbC(H6js^6n0uv0gtdXw4Ht|nn#M!<{a?|${#yRYaFqpHH}!(8b&N>4I`Gch7n6z!-yrVVZ@Qvcu`-gGpVoDnb26Sa-SWjbiNM{PMBB#4^$f5*i^?|M^nS}IKYf9a=bV$a;@Xdq2>!11WE37s^bS00LBYZkmORw%Yr1AI@TlxNK)S`O{wpdrquUJQ|gPQDfPwDl=@<6N`0|3rA{eLN!d9cc_r&EK%3^&!$`Dg#@}?BY}$mX|A25B`CIq=2dM;{=KMV>`KG;8yio6RP_zCb){sNBGr*b#|Ju#~Yu<V-8SqbIT?rZBPlHVf8L$nD_1e(^3w>^Kz%uET7yS$xdm1wpBPTJ9Rp5}5n71PQ$dL_<@FPbyFkX+qQG2oCWnu*0?o_<=*D79Uq!uW7=}s|?<e+X?W(EAyStEJ7&p(#3<R42}VvVJ&sm7AlP-97Jrm>_os#ww*RV-;uDwebc6-PSY6iZs;hb67?!;;qcVM%MMu%tCrSkjs*ENKlDj<m)ED^^Ehf~71e!BUo#U@1#TaFjJ9SjrL-EM*A^ma>KfOIkyMC9NUBlGc!5Noz>3q%|a1(i##R=>QTeX$=XMw1xyrT0?>*ts%jZ){tOHYe=x9H6&P@mxP4Pa3l>VVKXc-15DTqugZWEHp8hh0ENxIBCm3E4HKJjLtcrKi8X^7E;hsIGop*lF#3$};)OR)N=m#}Pby5jNz_QPJvU2@ki?1ZikM`ZT^LhPNs06B3#u@&CNbcc?Y$C{?Zpz4?Zpz4?Zpz4?Zpz4ZBB`a)q=CnYQX^|CQgQ5fJ07(Uw}jV1nbiPi+0w<0_@uM=bowo<Lri`YQQ-A1V7b?b#~UnQUL1gj!93zF;Az4)QG^TAvGc}A(51b?9eDQ1Ay5Lhtr5os5aq|9XQCWh(>mUsa6Ch^t~<sPIkjUC}0zqg17)Qp(%(9K$D%Bzb?RUZGnFnf!i3Cl2gfbj3=!f*DPu6xaLR)j%${*c2cvXwU?SD9k{1i+JSqTr5)I(S=xbrnx!51qFLI3Gn%Cxc%eDkkr$e!9hjk6+JPIIr5)IzS=xaenx!4sp;_929h#*b*r8ebncm>jtdLyLw?eb2K;sGw>?*|keM*j81ObWsjaZ1IhZ9j3L4Xrc7gE5Ch`JC5(7ac4v_OCE<Vayk=2*xD@JC5b7x02j1Pq)kxsVKC5?dl<Kr_q|L4yQSrZZs!D}613gTxxxkymPh&DWXGL1JEtnb1LkCUP0zL4G63Ho}8EA?H5ggv`G8ps^LkHdTZNc|sCz#0hX}2q)y{A-^FeWEky9%)cJadqM7BY~l;D|4P{~*opAq+2my81jZ)ktQ}xNHnON9O2|$cRfGxD+?e#Bvb?f{novFM01_<i01_<ifDtV1fDtV1Z&y#5oIO{TL3vX4TuFoSr0ltp2jyAWbEOQ@v$E$(9i(Sv&y_Yv&&r-FeURQ~hM`qG`Z|n$l~2cQp^hVM<49@N9FD6u<v9U<bzHtzVRbmbuZ|1&Dv54V5Z-b4ag|@i)A1m@<4EJ8zY444lQ^#W$7yw^pH&@K{o}N{)A2<eSN-F(y3>(P9hdY~THTEk(xddahNp$q)sO7Jv%>1yxQM5P)wOXE&kw6hi!RsH_~NA1X?#hBJD0|nWEfm&d`YahrrxI)cFcP+;?eX%rSpAyNsjfBrk8hu(9Vyb5r)njfflO00BCt@?iN5dBt-74tl7p1kvos1F(x?$ZvnU@=8m-hZgKMI0&a2g=>l$X^63I@vGVBxaIx~~0&ubN=>l-E^63I_`Tp|hG`u+ZbQ)fqd^!y;PClK67noPp?!ya>E9>{+g-WmY;f01vt@q*Ot&Fu5z>Ae37r+ahx(&b!eeNAV34QJzV98tWd<Vb+GtG9uEA%R52fzaJ(slqWFfVNfzykBqb^t8&ihKjWLbX=_EL6J#V4>O#0L!cSbnQN{SXptJSgg1;jV#6Kfz`}HrPF<AVfj{PX$dVb!VO#(v4`&Dx(Ftqk*gq<J9lc43{a#v?Uw<H6sP?%KoR=f<o2gHt(^g46sIjRV2t9NE@;Fk&gp_i4EiA<ha%{)D>@V@hNnw_7{#$82@s>Ozq}Vf7{!Qx3IL;6$wiVG>T3li^|b;MD|Aj1gB3cbiNOk;)5K7ndUlNrb#@s@CRE`C!x6~vrcgr$42B~GCiT4nlL}8#GC+*#6x9caQRf%0WI!R+DqhI|O1w$bR8rYdPzF!}qw+F<5*U@20hGX~JaSJ{Uo0@GFBX{8{{RIh?X?1v_F92Sd#%94iZ9djVx^a9dZE&QUM9scCH)8zVH&7p*buTbW2e~=z|eR(LNGAejS$Q`Z+}OJDGe2}kSf_`6|#^jSsFD*s$^lz8>y0oF>j<w7DlX*Dp?q@Mv6_^i^V4G#bT58VzJ4@Xt?YYoAlR;P5NuaCjGTylaAhaI+cV-km>L&4OE+S_Q!a?&oLeTsn_rGNoRlQbpR;zEv^7b=xba7l63YL>I#sAMjoyJH99n&*Z^$M=iUHbz|Y7A=z{)AHh>rKSF!=Tpl^~ChtM~<1HkA`xs2uu8gRM;zUW3NPJkC3x`*!fiD7+c9+G6}jAn_IT_^&USRMY6EU`M#xSAza2dyMZtWGqpW{DNvL)H5%vCgon2%uthy2~|FtZ=uefGJkULJdF#eeMRJVl~RX1EyFZ)Hc8r>_@&FUu6Il^tmg53i{jyPz8PN0;pnTe?=4k6)WSc0-%C^Wyzt%%Hm-QfC@)iGsX5=HOS^ThiY`7(x8BJbL<l}J8X`5qK1d*p=E{Kxp=u%;AX{}K}{K(;XWBq#^(4#29&Wm_K*Q(Y=%2z02!NO4jE9!Hs8mFl!I)Rj}0jY@g`AY$p-0_V9DmVtOZ!IIqaaZWMgL?1WPu<N;;sD?ZtYKIr(s#Qx5Vp9xfZLF}qWOBEg0xa)CNmE9^^y&6KP!4LD97mxh-e_L`LYxIz=53cwZm*yL2?+5244>Bw%BL<QKg!`hV!xMg?htpaYL&s_kNz?827D1`kIcXT*H6T~W@ko_gon+j-UXSFaD(8|tgVJe`Noz=orKr1_|g(0xA{|Bl2@bcvXk2Gp8*MUnKeeMo?(&%%qz$uMB_X@1i=yPwtD~&$)2F%i+%kV}_&=z<~LySby0?+426$pNEQU`*cyc3Hv`sAIsnnB~}PF&3vcz)H1ui3(m%{wtRv$O+eGfO+LHnX$?Ycoqbur_nFBWp8DJFqr$w1dt5Y1Ukm=PdyRq#0o{0S(;nqx{pK|M=U#{^l=Vg;)IaS0BN0ou?NNLvj*l0%EYD-2!5mlI#|c!yE4gd8|6=ZxLNgNq>tdWBv>lbgcvP%FZX*0f|frb&QB4IoU)JlB5~gL=l?2@gpE7D>S{5oUA0%&-1H)?w3nOUkgN>lUT+pIa=|w1I}@@BhIn31I}@@1I~FGn%5o9u~O#(zL}Cb7cfk=I72fG)dsaBFoLU+@{xob7#k`dfpK|_amlkEOk-S<orb=MIiCIt5PM{HF^iBRKfL55w>0n-bcP&H{{;vuvT=YPVa3zm5aI@u?A91JSlR(MINA|6SlR(MSlZt%r#d-Fuhl{Mafr{U!KAf8x;~dao<;RRx;>XZoNl*ukba!1b(Y=+>Ger68M&rCKf*pd!uB{g@u1w7L3w{1oOo1DgYs3J9&VTIdDKpCzmxMbjEnm!Xpgq+_HlKm$IJWF=-J2ReHFBa+iLr`zOPdB=Dn8lGmIaCt9-p1MUqG9@k8)9Uhi}r+Q$W+9;a%awAXQor~U1>a(;&KV{jG3hdtca@ndk6#D_iH*N^Pr`MLICqg}^UewD;$)`M)?!+jk;30JXwH%?C4eF933hr33g<aoGi1WJyFyGEdQg3iv5AW@0roSlUwC^<1_=Yb>+CC3O~^H4I3@B<!t=hdH|L30y%_h)5IL(a=TkEG!!If()R93>-CAYh|+UjO+SG#ioEe^%CL<h=g#NSc(A6GIS?QZhW&0su;e$6CNYR-j+NKUSb$z&}=?Uw||d1O56J#u1Pc=%@L|3G~zW;{^I?`pJ&Rnx>lUc&urz$@AMe`+eBSRySwAk3QB62JDj!o4NpLvg1=1K+W_we;!_wPPTmAJK!E~5;gc_=r7U$&}7HYB|w@NUVa0d<GuU_sK=Vb0DEA*V*}U&GZ-779+<&M4t-z-BRR&&bIkGc7si24G2GfT?-Zx8NCQuC`ieC1l$Xw40U5#AEC5EuXv@&hQ=Fy@jXC9|I|_nBg?(QL4i)x&Av9E+v+w|Q%J-IM8jw&i&cXu_vZOT!S<)JVENP86j&#5@mb6A1OIjn1C9RRhlGaFLNo%AjuiZ>lr@B^?N_7ffHK|mm?p2dYb;@2ffzYR3?js0&>g7IzR3mOwBS>}9Mgz2fp<xR^i^__Z7l0PkNu&+XqOvQ!1;9duS5XU~h03m?7C;NtNkk5Cp)y;Y1>i!3_B0FNh05${7QhP?+S8D$pX$UU1;kLv-g}nT#9&ElVsNB2F|@l)K>z8(=fC*LXFvJx|MoUMeiYb9v9A+2sByvx9Mm-71P*GLumT4)OteFJ|JN_^UXA~G97z_<@!8U7VPz%;XkkrH2B1ObCj-)e*?$>;hA}_qfi!l|aJ&q#qru&(0Pe6Rr~n9|6I1|&w3l4l3ZNC3U|0aHzy!krU<D=^7QiYn!H`s`v=^&XzP}_ujW*pegwycSXWyb$Qp(beOVmm#Tf7;Rz~jU;YToHiOp!*MK0gnj-KU^#<pDInMAj4r804gA1{Bnttfv5jroZ}(E^wT8pV57eH;EdRoSf4Dj=B@w6u?oRUn)m#eY#aEM=pV^NenotzgO7O-z#kC?-jQ6IfX6VDQsD1+57``TG_!5;Gz|J@q?3}b%x1<CZg3jwvt4&&M=<WWW=U^C5Jz&WA`6`&dLt-3g8@;Q+PTo3_xdftoQ@aL78Z0X$>)!w5AqIT0@H^t)az|*39Ba2Rvd)YXGsNHGf#rnm;UQ%^#Mu<_||&Q^oe0Lkvul1D8e{4D&7b*<rK7F(os=C^>LzWQB=oR@hkE3_yj=31$sYVS^1H<Z6gMH@O<xSg!)P8e&tDP|q^`{gI|+7-mO$kztq}X-2kEIs;m8QaS@#pdVIJghIcp3*ZI#X<Yy>(BJj~fB}A77XS?OE4ADwhTW+`Nk$dQKF9075!Bdc_$_MW*r(fIH*%D*TLw9jOZFLtr<zaRm^=V6yWzGPFw8!~Y&Bq+`LlN(U-OO?$Qc07ltj(|eBPKpQYzy_f(CH3Kd+QI52R6vCWK~yN-(7_15|=3efj@y?rfXmxUDSwS5*2;ryB1-_LF026K^H4%g#Dml}b&G$dSY~DQfxR#7X(TFM5We)D6wObNZmO`@y2DCQpOtM)xzo#W?^el^#yl3Nfwm+(cYm%8IToWyN}#(j(R(FqJZBZXK}NgQlDT%ROdT&C&&v9+1KpFxzlIwl2fkfLkxDodJKk0sLr@5r?{UoI>Y~P%P>OY#JsbCUpa7KvWQ4I@IvEAjWiSIUX0p!Va`NE{HW9=-XQmb2`)=ydZvbYx#p0#JCQ$CN79`9qNIb5$`(A7+5i{<D7vN_d3oRSh24g*7L7}%6At>JbF3HNyZf_{!rl+(<Ayw0T(bK5SY~IlWwQ*3z*CX%-C?@lN!EsNuSj4gh_wY@T5!nqlPI4`<Q{u$QT1IGa%C~SiqZw=36*zg+3^41wI&UjVUN?g()a)1t}<Pg(xU(1t=(Og(nzog%Fm8BRYl<Y>yCVg%m7PoFfB*?UC@Rkb-3@fMh^e*8JHy6jA_Ph&=)dsMW1U00H#6MXFg1YSoF9vtmJL160q-X)9bnX)9bnX)9bnX)9d7Xlq<RX)9bnX)9bnX)9bnX)9bnX)9bnX+Mpf&^i1t<wn^pPQ#ljmqytyO?#TvpXQ;F4$Gw{1eQ%B9hWD%O{Hxky(s(e<h`8Jv%BW(M?%r?t(?;n`Q}8WR}Y3p`e+Q|ORTCi$5z@bPgtC4x1-lA9lo<V+uRP{W9f!)4R3A-uvwg5I;(3g?Fc@WZV1;*mv#srOD*hVHa|UmJIs$I8{%g3(=)Y0dU?>{T)Q2`$AS(|SUH?Zx1;!2e&Go#UsLIJ6d#K(JYnH$D*c&Puw5KjIhAe)v0WTdI{V;V+Ch9Qk8t^Z-!>Bwpcg}UuF3Rbh|Q}qy%@rCO@<ePnP&OZ*~NfPP5yLt!Im0k223)Tn16)_l#DD$l-pcb1{NmDZGI-1Ukqc@rSJ=S^$~zs>+&O@gI#|MU=DZvEdV`+@v&2g#$Xm{7C;z-S)^HjV6aHM1R;!J+yNAZF@&|7!Z3!gc2gLJ3LsP%#;g};5fG5E9rp{(Ygk0iVUiDJ&S8=dWzNC!31^uvGU%Yv>2%ORrSs{agG!gv0mg!JE(JgsyHdta0pJE)zbXLRfGbP|KpVS!<H`I)GQXfJSp^^%yHXi*0oVo%zAFIQSfUD7K^sdH;VNiji3(MPY%Eits*sIk>Qfc8u}pcY!ZwzvPF2{({>#F;WVT_#24#40jGe1YFOJ|MnO+>jMIyX7#_3Xq7f0+&lG()(8<S*oaZF&Uf-VkQkPQHlP|`AyP|`AyP|`AkFwzQwP|`A4P|`A4P|`A4P|`A4P|`A4P|`A3P|`A2P|`A1P|`A0Fw!z7_|-~L{A#5ro+y8mF~Jk{i83a5raDo^1mAys+@FpTo?0IFr;`QOgECoo>=UU6$ijp6X2?R0XYBP9w($M!${oNTp0X=PN>`{(RCvTQr4cfZc*YM>0TSQ8v<<0M@l<UavhKrmq6{&9z1kJOUhRrsv3AAx@v65>@k&^&cqOb>yb>5&bQyS1X`uABQy7?&n;?==015#TQhghUCsabJZv*2&r9cmuLy1)1u5;}(RHcht{0!B&FjqfAl`K@+qryD_j21w+hf48Oz-O&{3jw6S#4;%K6PQ>Ag?GRNLl58%m|*Au+yN5|J%BqMQwGZ~OifHcW_X|~m-v5G<q}t`a*5FJbF*3$5r|OfbUF~B()o1IL8JD7GMBiLg;PEqg21r93@{LwC6@sPLSxV}z&3Fu$FmGjP{ig+Gk`r2Oi4%p_C%(NCjkr;!THJrFi>2niYEaK6tOwe1RxNY@|OSt0#p7HKtN#1A5skySFDDKD^|nAf0<RA%s@*M3X_;nDC188?dyRFq140sU*@31nD5IRlzN!&%RGd(9+>(`Jv^{w-bq;P7Bc6Pdf31z;FAa!IE8ys4-+_rYZ8d*$f_2q?E$b!J$#cCrb*Z<&I3r3dbn08$O47cd1%&#l9rK$l9rK$l9rK$l9q{ul9qvmk(Lo8uVMu!BS>bvVr2x$J*;A71j$Ge#P`2@`SM$RA=)FLk_oF?nNM;Lr&^g)*62Nl?7{}q;E-+D8Qgk>)a&FP{(TC@WTt>krkBjv_bK#}`<DbEfRm|`AOv%$PE<H2gE0$8Au*~Q0l-1~Bm#s3MrlTXaKI?d2oO%jU>KQ`$t%vuWO7bs|Ed^O9_w+aZAwd%6RkXZB2rOdN`OQtTAJ(z%*&J&Uh5GlWG+ORlMF@6dM_cx%4_sqLW-CRRmvq(QK4$NWGX_n4M0Pv_5k1zn&CG9I0R<+4FKwZ8GZx6Hdv3$wPm&`y#aB4dKrHT0f_T6$uPuqq6|Z5NT2~|2-UU#4pG603J;YP-Dt|nJOmZ%P#KDfx!%B3%_#PIXo?t6k+WKe7~oKYW{5?=iVt;*On?{P0PfXKfXUuEmu21t#g7jhE(vkq1HH5p;=qTxDksE(Z&=CVCm|ku15;?BxbO{3rG?_VhYrV#81JFth(8TH*b#@C)kZtwWy7T{YBqhtif%Ss+M;IFH>@~Y)H7`{|3Xv~bHRrSzEIJ73cjG)2EY;n4tWD`3EJ)f;1aam1HdI<2;qR>h5<2mKzIWT9~=<gK*I--ITozp2AX358*ZRk7Odd|G|d7we1PUzi~*w@48jp;%MHR22CEu22p*vK3NmwoHQdg$6*@pir$OkzU?6S~I6$9=26*4wb(V%?5U|ABkir3&>tI9*RThR0Mx<l~Za+{{ySV*8Q7znlgMa~M**X_jzyNJIL<VTfAu_PoVj)BZ7TdlKfq@10_Zox@EV#kfAY@>%I1&g9ESO0Efq?}>DUc-<xa9*v1{RA`7!Wc*@09@|11R8duC0&(p&f^(0Tla&C&s}x%6-BU<KP<QPT`4h@Qrk*@WeQTMmjE+HWTUCNT=n})B7Ve(s_Ac;Z!;|(q+}i$LZNib9N#waUyMoR+@-QoNBk@^;leDr?S!M>DxhV+~TyxsdPK4k0mOipYfw<hxM^U#ZIn{)6=&@|5)ha37^xa((TYc7N~f_C+VqlJM@nwD4y_HcPiZu{lx)_ekR?H>tg|mr>qK1p0l<c*vAqSPtl&d9_(jc#CEy%<gI4gQQIp+G1_+6_RmmMeCQO4Awm=tiZR4IgMu-Jm;z8R#t@&*6^t>&XLAK(4Drca!5Bk)E>|$d^nSHO2xH9hNdXOG3{mc>VNCa4OAyAG<<lJ+#u(y5riL-ydo4p4V~B|yjbl)43xJFv%=t8uF@$-YhBE8Kf6m&VAdgvYa;FiGS#ENt0gqX3a;Nc5$Gk;*b`*aCf<ILBqL<1@6gncJ7Zo@nq8Al5vdeRT6f`0t?dInZImv?43*mH5vdg246ilM>{sI6*mdH%fhzQKu3jh#VVz;SAJJgLC0rs)PwpNXOz*{o{TtnTP5r7=@-i!d`Sg?vE0g!`gX8>~0KFI*Qfa5g-@Pdxl0?-ROj0%7+&{EP&TBZ=Uu*Aejwr~o75W$QJfH<&V)1OWtj;Os=5X5ybl2Pd6(^Gu)<##Wk#*6UbkkJ}u$|8I?!og1C4OH6zyy3u|kp=(`aOfC-H^Agk0}zHIYUDJ+0Ao!JKo}16*s%aqpqZ)2%n2BpY5}Hj;0x3NOyP(WDvc??v{wf(g#$4QnGtbB;G4!2V4xx}v*G(Ng-4crJoS1Op~4e8V-%?H#Ksr}Dm<|-MuCa$*=X~#i@@QDO*sm2cw$eEMjR`28nP_pmv0Hun8Xu1f;1@U-fIq87V^vYBWc{?LAXG`#jgl1sI~*Z#S^B68oBrmriL29c;r)-g;sQY58Eauw?O6`Fw7Cb9KYOCS)&}^#oEN3^(lD?y=GegG73zYjR;18Dzg#6C{SfKA{d1Z8*LOo3dnO{t}Mb2n6PP2XP-dWn`!KWMmQp~EntKrGT9QS>INBXm{>!NTChu*q3M=D?A+0?B`n{#qftvB_U&lY5{PX(8npys*N#Rj*zH}Qnp;#Gskue9k(yhyza4-gP`=?zTE+@0-_R1JByqJ;5+b9_A%!JqY#>ls5}9fkkuQkOu}EP_1ShG1$`UYy45=kyqA@kvV6rha+(2)|1mH$oZsexX2ACh20N6nDBNG4{M8KW~8xfqw$N+4hLox%f0gg$eUIYvVM9M`XIBAR2i-7O943Gx;BtgnW&?gB{FOqs$k^q#ER;w3D;JpKYMFMwk#nZt8ZFM}IEE3_Pr@%y_YI8)G=n<TzQANTkXgmNFiP+AsFh!3<JdG`&o|#L_Y>@~%0);IS_>v9)TcFxVHEIF@0I5cWqTlAyGFwp6GFvdx3R_UpGFnj5GFnj5GFdRvGFYq<4yb@dW_(mcu)xxb9I`ahBREe1jEp_efjU$$Fbb$c%~X|+h!?p-Vz7o68N&+;;6+{@My%mQ?hr<-;RSdzA`2y8KBEQjA~VK83SMNwD^tS@FqaWoC&`32sfHIBtM4=bUSz@xR^y8d){Y{}Bxt)WKo}X@qGJKVK<^TJI$|tM+KWW>#j-@VfUrhE9*_aq^HP}75s@%@!~`m+QLrKme>!Rq`F{#&^vM6yNCWDZ1WjZx(S90glvQjM=53Hs1dO|L0E(0j_Qe{LfFr^INCKwyIe<u(K0%SfQ}7XrSdA2B7n_16OS{Gbhyr#ELMTjJo<=B4T%Lv~rK6dM>>y&FMqTP`18ZZW+{p&krbfA!4Xn+LbT1oNTN>$JHn47Jq|<V*)~U2<r1Pp?t<$sH=Imv$RqIsQHOfa_V9`&K&bQiTRjbzN>DwV~>|(3dsdPK0kGjC3A7ouSs*l;gcCu=np1vLV$DCr}&(W?O`p0Zw;m^^&9s9?8U^{i&^z`lXVX;^2?4!1C2mfNP*x9q#x1;}<SL_L8DpTop@E@~^Jz;u!D*c&vbuXt_-;V5VPO-in*(*53MtR$e3_6TctPDDa_$V)f4ro^CPv;y1miN2UIR}-tr*n>BHYLcMW0*Y&GQ_Ol-HCvXA$CM4oMV_B5emd~@3jJfj$t-rD4=7Q4H*i>tk7)(06J!Qh>ONKpdaY~FbwENIsgm<`jHL*!x(US!T=D1Y9kb5m?;~DVhl57qfm@l$L}7Ru3>yvWr|^ZS7nM}d{<?Pp{z4yilGcGWr|_^EM<tHTqb3Rp-d(fLP49I07S8?EcwjaAfpUrqN#8Ss$Bq1L9a^zIAyKtQUF*1O+pI*D;Ar&C;+TjZ0e!_uwt>Pivqxk1xxEP04u0=0$>HzjsUD!W}}1xE4JVIlK(|)hzu-Cy<xq$*GEPfhfVbWDC0m&5nx8f^{8f%nZ^;-EHctK#>GWu8rP$!L1r6A)HEn);}{Pb1#Mgp6B-3w9N|Kvkc%U1XcTa9pjV6qzy-7FoYe*?K!Ud00Yu`kxnu_r$*0mUzWyzwECY#SGIkUqao~)v2Z+QG**OZ3xE|$w3Ya*eyieg0$T2n{QzO35u40cY{dlH&MkEc-Z2pl+1C<79Tzrqc95QNnVk?JC8jwBWSKs_uH%FYGUZfE8vLI_fo-t2XFk}ULRb-vW6W;9#p?IeHNG22y&Rimd;+fqK3ZeM^l}$*ki)SiAWQd_WX%&p2JZTk->EcPN;0)tQtKbad2&+&G;|Qxz4Cx3vzC1qhgUw7`OIWS0C9GE05|}+6GTflj0NhaSrZUt}=B6^$Fy5vzuu#^f3b0VtrV6lt7NN*=31us(&<JHKso)4|KZ@W8+HM3#sQy-11J(8bY@mJO0oVwutgICXN&;2}gs@0hZ)znFvBV0C1R|DLVUh6vWG4}2ARFW*CXrJj<B}$W3M!pW2NhI0pAIUhbU7VV2-n#8c|>YK4H?Vn*aG@77JynJIE9k|YN5=GGr%yY@gq{L0$Rvs0AV7yy)FR=LwO}9fM-x=)&%ej<FTvYOay1MGJrFYiLlN9v!F)7NQDY$6r2HQL5+e7KrPgLUjT+d@B4B(mZXlp_D~fH<2Wl*3FSB|Q%Pd#i$y3&jH9{?C5d@80_C*{d@};&wF#T6i~y7*hG7*bNem7mCA8=*p8zO<{3z$rGL%r#GLul!GKDbG3WQM7GK5glGJ{akGIdbWGIUVVGIUVVGILPUGG#E*GGr_@o()9pN$z1-E`vrU{K{p{$lYr#JW>hEnD)vnl6#n?%NUXguXLG0@(L9&9zYe!@mN8XE|$j%r7)hy3ZyWm#|oq@eULbSR=_6-QZ!4MHY>Q&#kE=C7RI$%;g&U?vWUw{ru<4|y2+GZiHtY7LwQG$i#ikv${4C3>qU&TOhJX2YLVS*WfUrXeE$Q&MqNyKWk_O7d1d}V4JF;_0Mx~5QwAW$X;TIu%4k!8n=VG13gj?Gn+n^YU4s<b7HD=SK$W(j|1{zlhc$byEmI9>hHC(*L9Zm@q*9ho2nNVk1-)euW0iuuA?MOEwNTPBv{2GAjZo4ujWE)R;oHy=N1%cfGcc<tvLoEUWDP5xa06ojBYVOPObW1K3O5k`GKwi2Y7!d&S2)ZM*gz906LEOe+#?onXcu|J18zW`4s&hA;EmE&4BjYh#o&$7R@~bdZOy)o(pLQ2C~d{SjnY;e+$e3u!Hv>Z9NZ{v#lelzRvg?IZRMSBx|Y8pCb5Ruge((*VLbe0A~1}Jzd{6tsapajB8&mC2AGO~I|!MJ;Ccv|k$}4hnUlcoPXpPL7y}kHB1<kz{~KuG1?+zVExlm<KS0}Wm@XP1`x3B=259RqcpD8EKTv%H(FEE@5Kf?d6cC<3TaLJ_P2c(&P|UTT23J;sc}`j1nn;JCktVGEC)I|*G}3;#^rXfn*hV@mm!1?+2iHh1j^~(5`$l?EItQ{FZ{CE^G$AjJc$zB5M!77FG;*`6of_%o`8;#&+-jS(FUq_P?eJb4(lguX5!>Ny+~U-vsdPKMk7e|n@WP);x5L{kj^3J?7sqydo48zi@-U6<05@rQw$D_%9l54!`c{-r-wyA^0X(zW&)5#{#Q{9C`QX@&?!^H-vl;UEnRl{Xob5A_PVJyQmcPRqwmvzFMA^DEwS)awY|jamA^_Z&KJ~J*ng^MBOpk&MnSKmWupz^b>0Ze-KfMS@hN%~k0m<~J7m)$T5cMK50IhLZ8~{mRsFed4$@K8uRT#(+#=8mw^}jOn^UI)Q7~@}sluQrfUxk<qVf?EA(;An?0#F4;@>l?vOph8bg`5mg<E4<(8jmvz;1!h&r0^A$45WaP=}<3hf^5Db0~M1CBx4hk3nbGLlM5u%5}2?PP6r`0ZY7=$LR7+z3_w%>jZ8pjMob3iX042v3}6tL5t9M>LDQ=WfInz_RRPduoy#(BgN#5-zK%jZOumjnJ{FwQECAKmmF6@HfIm!rkU~9FevpDaRDO_xG*o_&f;3cqkb*QF^MjO0C>d-V;i4jgjbmI?WU_I+U9vqwKaOERk$xOgd@R$C>pjywKf4G>j)7c}j~r9@tng9yKAWFjMkB}YyNpJTsk>ItsC%!?PcPGxV-`MSC~}|`7_x$f-p3KZBDV^<%-bO2lf$Sl0#xJ(ZzqL{(05n_sK~8Uxex(*aungn^yJo9aI=<LadWG!xGhabN@8WQOjy2$Lyb&Yo^Ys<DawPlo;w|*d=JA78K*qqw;`jFXY4j)R`NaEHWX&^gxiL~Ltq$~1$d}Su9m_@Ot6;1JRbCZbO7}D9=<*b{CL9GM`0hdYdpX-zK0i;0ymy8qf+3;6Pr&Iw&@a@q_7JUnxvqMM=-%cOIeJxOdz38J|k4~6R5fskvsxp6(XZYV5~M|^aza8hKwAc_oUbS>>`!~!sbJ!lEAopC^XW&&*rC>i3LpfG61nqiB<}!bnmtK>1CP;U;;E!+7p=MYK39~lU%J}462P_Oz4q#tYAza5|0&(VN!(@j0p=1!4QlISRojKF-$0uf-z($(&KE7u}n=)T&*T2u2z#1SF6cEGeY9&P=h9S07W^m|6)Nr9cm(0#}rS8nh2KdL;z}H|4l0qfSQO^>_h-+(0dr!w1wWp$gZupQpFCky$g)MNdVZO5jYtD8#I|F17H(ZTKCET_(W{oD+AyYv2`z`VkfRxu@hIU*oiAv?8G(Jvy5emcM|rY93Y^CeR2f|D1j-@z>-p8Vy|Tc`c(SG*T02?MF2`zd^E6-l)(6Ce>&YDy)hS-*(PDx(H`Iyq|tL_8Cw#V?u_iSN=z!Xf-Q+jrB-kxF{#uFk0dPp7}-0Om|S!PN1%9|4DE}eq-DyWq-DyWq-Drpq!q@Xq-Dflq-9cI0(oRo$iyn5ObQvBD*-?uGoGq4C}eC(!JkeFnQ@4cQ6Xa==>by6pb0OsIXg4XYYHr6!gx)gh0M62DYO7yNCXx#Hot(Bm}JJ~QDKG5xI8MbkQwVm1r{<kZ-Br87<Glf0wj&?ozBdny+R9_No-JXAu~Y=3NK{B+&?{yo1(bmop2$iOGmy@b_<o~>s_Hy_6wC~6ALLe%3-1M>;rE~jdEP5Jo{9da-*D<T5`=kIHuA_=cSHZGwD1u(xs;%mzU3OnzJ7>#e+W)XWMF<<-Io5Zb$1ev%5~+Ha&eiq!%0F%|5r}c1#~N#6v%j=XO*dbHwY?YxC2$L;sj*p4w}(Qk2||{pFr{bM1EU_w~&4;^|BKfH>xvcS5<xRJtAg$2{{;<C@YA{$rkbu=7g!%&Xci*PgsYN;|SUy5@aY<%n{fM`@n{i+%FuFd||O<+~<xj$!IoWzaDU3d^KpC=wP?$50?FvX1Fp5ivizh(oCJkvScQP-zRW4rK<VunuJgrLd0a@<>viNDA;6;)$dH4<#-04kazK3?(hI3?(h23?r>z3MDOL3MDOL3MDO53MDN=3MDP0hgl6hEE5tSqlX1ny63_ocvvQVKn9Oa_DW7}f(R&Bx24nZ#4^bWGJ9Zc&Zm<H+U5d~$6D9A0EB{dTmkq5w2CYMb|8(OE6dbj!K8@{V8=R_d)@|_Pq3cL0G?PTqeI~ntkns?6SUP4;FGnkcLYEN>$wPUj3wM=6po?%<`j_W=r^a;tjgTO7|zMq!}zkv+{4(H$=Kt-<!NAP$uR+tGSE0?QC$Wa$E>N#NV9^S8#3R5x`!e2Esm+6P<UpAZgT+hpxuVdwV>JopdQLBPN5kGyxr!?GR>f^Mrg*Z!UY!M9<1jQKs}(rT>@YRG`LFu%{XQ=j)F68MV#qqF6U0(j3a}MCrWH(uwjgPWU%qf15hR#&piKRvhmDAN+ui6Y;}~$#zT)DV5$afGcr}<S9)e6Q#Dw}AyYLTt1w5VYLG@7XsX78CDq7O%{rIcKvOkX&mmJaXwM;VgS8q#7Ef&KR+z=F$1Hw5X7MXBi(iph{J+fdUj~(c&A<Sl5*P#$K_xH<Byvh1b{WZ-5|~{^GNy$7wkiH}k_pVF9+_nVv!_R4nH4$>nWG8BmLi2?0<)z^0h!R>ZN>q#6ToOKq#h<PJL(jQS)tpIqM1PK=u=21U_62p%>;}`kfND@@d#2h)5i<V`d{Qm$WRn8XM3c)hLV<%h>?~dhcSnfA%`)ClOcyOhm#>E5`m2}<U}U0QHGqz1UAY96IV(;OsA7h1U@j%g=Nl(Od6#EF<7fJz%Xd5k;#~~E;ll5gY{eiFa|W_D*(krA_h_+lt{!tDufb=m_&t8A`_FSAPQx=rZ5U+x~8B9WxA%YM^DqWUzo|8NF)czq>>i;_BU?s0K+iGaWca&#&I&kP{wgG#H1b$*fPu{!T?)lnMC+s%ZP&Yc!VZnP;F$Vby{fKjqJEim~A(*n;J9ji_mn+(ynm;kAPj{03JcR2AMKRJ<Q$}GD(ElyFw<AcUXkxPAF-aODJg>ODJiXN+@ZWGZ<-^Gx9>th{S?WW^80c&d7^KYd}_pGBQ{L!W)^|b}n+p(tZK#U%-9=R(~?HXI=r0r5%HS2iP+RZ)9xI7U7NDBNkHOj!eWtD!7sL$({GNHy01*_v5+0`SU3|$q*Zt4DOV30F&e%Nu~;uWFpE`VG^`!5Gct#!fzEi$wd0CLMLn7wFtswZenF@(Pyeq5Yox3t^Jf<Gb#Y-6sD*~B%Q(()rf#odgPbNq*I9aQW<ng_W|UPS(gHCpadwW^hn%QXs8g0y9xxMJ%dnC>5<c{;7}oQniUFK<DNxOsbEXj2n7{tcbiN>h1vop(@*J<RIFf7A(Dy}3WDya?|=95<+rC)=Oc_%n3^4#kqT3@BjZo$fj?)DJz6`E0inXw*L)b2Zcto&2@sl}GdJgSeVl_!X_S2z=ioF9jdJMX9GnKzC?E0oT)MK92HTwCh}S2$vXlnbC}U2a`oqP_4e(6^mV13pl|!Sv-063^N|A=xYMbTScB0*m=wnX5OV_s2(2n3^cD~@+RvOwNe9X?b4*|{2Z`y%=%<>mqTT7-L>L&7+W_pfxtedp>(oCh>!EW-pmu7nYcB~&W_C?qBl4(c#F=yYUYkSGGqyCu1FSxds%x7NXcHIZ@yanwe!MerP$W!U|k#Nl2mq#(LI1P)uWES#Lkk2XdlIgLKC4-Y$zL2GWlj;7<2nby<_RR`anGWk{3SODz>u3r$t#Mf#09TCnwFXzF!#bV@S!Ve<p2k*dTp9$x%<^?ajjc?FbwrJ^%<^?a4Xq5Zj;FDe>9CHc@snA;j;G<1S%E+1Es){L5G#oqU6~F5Ql0?B{vx+U<}9;(E=c1nv)VM1?SoD8f@~3+P_IM)mu!cXWrdsU@`YsuiR|*#LWPKIht)!bi0ty!LWPJdv0SIoj_t5sr%{hxzFw!nj$Ps5K5v1{M3z`F)Og2sSTWSV$1Yzn)Og1(U$N78#}X@c8t+(Q#ZKcK+hN5{10K74#ZDs`yL`P&0~xz~y-ed0);{<&Hj)9x!T|HvQSb7qD*ol42jzMp-d}Csy{nCTyM1?YfRM*ywmIgXjyd6&7c_%#EDFa`bF4fa%gwR;bgVST%<yz@e2mSHnvX|~c+`qV+x|%(4|<`&CJ4W&X}ieSk4KYuG>b=zbkq*wQ6nC;;!!6a_2SVW9*sgr+9X{)E8S7H2)eHAC_9e2``g|2ejJ#a^P6|CFW>BUSl8p17u);Y=JH}cxAEfTe{Eixys>GM(y)19#{a_Rt1rL*-M|0-n?G-UaCL;=oxj~(Z#O^fZtwO3`}xk~UyToezyE6dq5t09-R(B7Zf@@GHy393)la7W%ym6{wYjSgp-+Bpf4(p3`M$8}i~6Hq)brK<!WSRT_r?BvyZ4v%X>@&gzPY`*+CS}H{_yhm-+cRrmw)_IZQ37SeEs6fKaKB$SKE5x_cvFU=RZ$>oAC78{Qk?|eDmGr`#-(>cJss7uJ_y9u}j7d+uXg~+7RnczJ9%RrDVT7zwj4fh!?M1$st|@8_Uk^^3H5um!Vu-ytZ5KtlyRk6H5pe+4*hCvFe_0AMUnSo7dax{j=`*ho1aHZTKHQ_GfMU=KGi5{qXfyWBY4wZT|MQUZ(nUwe!w@KEK*+>P5Xf_+gx-v+~!&cfEeNy4w7$Ubx%M{oC7{hc|CGPmhzkA1~iO9y{M%UEOV7{d_q1&*z~EJs-|&J(t=4>CeVaaQi>){!g?2b9nr7cwS!y&$m}sH-Fn)>|XC~Z|hxk_kR1gcbnVY`Axl)Rrmh(VON`#>OVcy3-Ivn>gN2%&EXYs_jK5}P5t@%%d5+O)Rw*9{#-BS)#lah<;9!bhi|&Re0O>MaDBLMKWVqwKeg@tx$gFV`u)Fz{omvM?`i)O&ig;hp(o66c!V1B_|+c9*z?0JI(Fpte0(`=?(17?cX(}n`};5dIEImp9<+M{qB_XyNj_lsuU&nZ{NbA)Ue?FySYxz*>(wVrmH+m;Z(jW8SAY6?JQh=Z#y`KmsdwYeoACyyH~1IB{)W4&uhHGdGyY|dpJ)4-v9mp;pY11N&h`*<w&#tr{k!vQKd*SUUtT@iPye3n*YnQyGxTTs<)gFxYJR;-uEtUQKf~tne2+}j{QKtP>)`PpUSHPBa%kP*z}4kXySw}GlHTs_ZXRyWcboI=`}wi!%fEkS=4G5t7;PLj^^tM@<NKS-M>csenDNVgG#p-JkCr?26;%%g;ox{tCkH>>P(HpT9=|#4zd1D4!ujbt>^N)t!VdbkG%EIEqg)xk#f>T>N^R>MTnGN=f8TxY*iYuAo_^W=5kEb0_)TX$>OcNkpXuwz-{!MNj{c1M{LlRINNStyPxZ_8Recscj+VQtoBf?@>Wj$KSH7uGU}~@J|L*GTSwHyO`svyFdc&rAd#CYheeSsW_fWrv`nA-5D@ph-9{$_^?D$`N{4dnI_|t}L>PO+9cJH?D&UfSQ@%WB-wR?B|_Ii8!<FniGxmEvf_w44~)zAO-Z2xk+eD~&Ay^FW!m-jzEt52=F`fb~*XTSUUyO+;K@t?Ni37*|w)<@Et@twE7@yB;Vz2l$l{$9W5*?ver`;YNi^6WSDfxNxFs47*yKClmOt@_fdZ`OTR4Z#l~gxWzvaJl|H@BcQwSKQ%mCdB=}g&1t9qx$*fyPvkVm)rV!+SW02celCQUcbM3d|1}2Q-|a3_NU$Ec5LhOUk|?;r=dQ1#-7&)?C#J}^;exdPwgIOjeC49#yw4&v|sr(`S7Lezl=B3_{AK)*uxih_~H*=!r@Cid^xDtgNi+<jJMeMK>Vb2uO8}y|9))L!RKW<z{X1N4+FV;99FM)_5JheYJ2|U&BOhNSL0tlj=K6bZw^<ktdE8IfUcldY0i%K&&|6xb!@(=FPhu&0k(Pnc0`8?DGyf<cl#mwKlbq*x_|9`&>Drtd$`_)f1Ug`hmrE3n?Ls({d3>3?$EL6(6J+<k3H)@*R$raYwe+H%b{z>&UoyYe?E6lm&hN4tbU2&K_`vl`|%yUdB5BK_>o^{|Nh~_du{9W_V1gwm-W7@M=E(dO}o9m8Q%&YRW`40Z>~2_pBI|L6J{A1dXzedK0$XKq!0Cy?gvyI0#_puef<92Z5^2772m&Hu6ElGKUqFGSQ~nI@$mFr<4bG&B=GR65@NlTw&VNmZZkd=J^;vJoP8L&*SqVR5pZ5_ukLnFOjkknemlND?{*hY$1dNUKU}{WQS#0Bf}I_GdvkR$-jS8O@9Kx+j|W~Keu)vtZ?Ct9p*sJbAGdGb)MxL*`>UJn#b*0(|Mup#-g6(n;d*yff9}Jr{Pe-G-ob~id-||gpC5I2Z12zCZVo?Ff1TYEp}oG{?f$Xb+`Qk7Psh#p?5yK+f3lI*_Ya+4{uk=Qht&')))

_PARENT_26_PLAN = json.loads(zlib.decompress(base64.b85decode('c-qXpU+*qQm8JPzeC>;je;Ju|=YrD>8h3#VH0o}RN(j)1nJPdOXr@)-yN?aV<u~KJYv+?I!qgQKmR976HzVWuMeM!Szkl+_Km6kV{`D{a_`5&+?@#{WfBpL>|MtgU|NfJINS}W4t6%)@zx?kX|MZ97e)13b(@*~2-~HkL`Sl+@`G@V(Pk#6NU;ge_zy9POKKbzvzxRLq?8l#c`pGZ;@PGa3Uw{4EKmOY%|M2gh{N|6p{?{-6<M)2_^DqC)pMLwBum0cs=TATR{qO$mH-G%i@4l4#U-i@afByN?zYUkK!<7fa{p1H9KK%IRfaN-1eK6q9fAHb6pZ>>yRSj6L1GbM3_)kCj;-^2jjCa*7-_mVY-TmXb|M;^Xe*XP`{_$r&`RUKT_yF|xtA2koQJ;VIy{qmgzxeHM{`D9C^36}9#_88_j*pM?Up{>J{&kqI=RYa^<EnptT>pEYq3JoVvT6Ic?$1B`<fl@%yy$)<a}iGN4|^G5SmG(q`e`pC4XZm9_s6}AFf8X(AO5@-;bGaP$LqFyn!l|)EZnsFKk&;4!_rNU*6vqdaXHSgbkpJgye}gRi#MH*f8H12Vfp4a%lE@)!Sbyy!g*M}Ir-n^ml4JtI?wraFXIf0Hy8iQ{4&C@cyoRHZGQQ61;ZrrX}-@YiGA_!5($#cx48q!rWaX-9Y}V2kyW&jUf=0|y6S%N%Rl_?_uo*N8bz_j%fo;6(+^*Or&o-T$j9V$t|enQv+_EOMh-SF7iEbWFaLtie)1C{EXl$VmO$YMOQ3LsB~LiQ5+fX8$qkOM#05uK;({TpalsLml;8+UEO3M+4LCoZpn=S`?RJv}GTXM>O&ZAP&yM>zkd3V*-=>3%Hj;cB59qAiJ$&$H<?ay#ot4{X5ScOF{WFMcfye!mhz!Bw{>ejToO=JjAzP$+|NJ3CRxP)Afi0#DoIBi|oB#IV^B?`wCvqIg4|HzspEqPi^7qdhoT*9R_<^pd`^OGwYBD%y@IJ!#PaEiG`0jB-VaE-30i(c+gS+Pq#ki1Agh6%lO{So_=_XSYV@1A>q6nj)m+n<pF-2iio9-foGb^vdXu@Fga#5B{Q5cw~+eqO|&1D=(7zKW((ru<Fj2F{wq$t+zmTm(^fxBC}jTD9PV!BNf#bTm#8!!rFqI4T63gpG@Hd1(Vv)v{PIyc*GrYPjh;#F87MSXtNppc?IziLoKQJ-HmD4?k5y-T+%C#Y_|2^3WKE<#Y<?IuE0>!ZEhC5j5a+1qV~sO&G2?KVPGYp36C6GeqP{dSun(A1PyVTlmc;=}DWQB=r>+iixZ?B;*FjS$uPgJQc)6czqSvE62fN_MkXVT}-uup|gaSR#WXEQ!GoR>aVVY`aYihO8n6Lsk)kA*+DFkX5{3$SPbgWECwKvJwvrT}=m$u%rV=SmJ;qENQ?ImNei9%kAG0mb<?rEO&oLSZ?=@u-xsPEko}1j<DSA9bviKJHm3ecZC18K(f=OLE0GdejTyQ>0`+KDqQC_0OaF3K%3G5kk6~`n>z0A{pj=0KYZ_}|NLJ*eDTvCe*VM%8AAEDM=9HNls=`;protrF}F0o<m&+El*;^4uDb6!FW|gihN;6aX-)$`8P@K*{)?w&^JQ48@A@ua*?bw+>f3e;I`=Qb3@i3s^98KVFT;|3*L(4_ro9f!^<D1;tZA>qdVSYyfj>7d!wjqTUB|^we)KbTJv^-2cP$rplwbbp8<y(3o{R5)@uPQp;b)(J{^fu9_5b(#U;pxtzy8%ffA#<V<v)LG7Qfse<ztL{^1Dqr{?q<Ncv#NwIx(p5u$<pDU_fDsCr$^3f)JwxLo$fbgCWtwXu^=_VRT_g*l-#oByAWS5)v|;&IL^wiCr$#+gy>18d=R1$*7XmJdunFRt*&Cc?qjVh-8$OYKBP9OG`C6B%|b0vqLgUJ~b{RqZCu)LV8|`sc9h@C6XEd((@8Y4FJg~UDO1Cnl3KYmWlwfQN1V;Ag?-y$VUC5gn(=mFiHx@Ms1<Qfc(6;P*OlPivA=9<mWYingX&>i>EOlKd;5p6p)P?IZXlid5xTgfNa#RX$r_j?V6^5Y}Ax#41hfd+ieQSMkS7>fc(4?M?*k1Dr7VT<mVMK8UnIWxuPi`Kd)TT5Ri?E5=jAtU4OK@5a8%425@v00yw&g01RCT0FJH#07qBt|BkNQ{~cku{X4>P`*(!p?(Yc8-QN+Go4+G0_kKfIZ~cz2-1;41x$`^1a_4u1<;L#_%Z=X=mixXVEcbn9TT<J8HLexZw(sbwZQs#V+rFc#wtYiaZu^d|+V&k?we35)a@%)=<+kq#%WdBgmfOA~EVq3}SZ@1{u-x_yVZH4;!gAYpgypvH2+M8X5tiG&BP_T5y6V=yuDbPig#WfcN>G#tZ|B=~)h!QoFJ?vQs#~8{c)i|gwtN+C&xK#C5Xx2fP5BbN2Ws^y{HAK@2cLcM-^W>gb>a9{8O_HXxi4e4>)6LzKU2g1qwUvW&Pj9EufmV5pkMD3+c5~Ir;mJ59#(34x>R3pZTDfRzN<W>_rd$HSl^W%#^qzLx8wV;THjS0(tG!PSg!BN4W}%t%izP37B0|+Q`J5!-*<(Hc>0DF`>q!8#!bkJ@UUVZyFb5v`1fJOzN<vMajWnmJZ`P|aYgKl0p74+-_;h<s?0tt*muQ+52`Z%`dUT>nTkh@Dn!X6$%%AOK$08_B?TnOC_#`wl8h1r2_)%x34(-;^t@6)(nUhch|mR9F1PW5D%ab1;nX;4zDV;ywcbXMG|fa+1Bo?#5=e}KWDOfmA+E-Y>A(18a7iHZ9N0CGSkoto#HeG|M3NZl)Z0Xo80y>ylJxfml02(xv)x4%rwmh~ic^LuQ6*1k2bIW@pSOcbV#%}GK_$O9RjLwT@`TPf4Kn$8XPoAkJgYNKLk+Boy?<tsC-j4AaLLd6K{cu5S^c0ITQVZm0uD*?gf?i+FZp>Nv}Th$s}EYENq&Cvpvfc~Cl4A;@^{q_szD|{zh}`PlNVj!7*5ubLdq%%DXS>NGP73n;ka2#{Gh_yUE(N4aj+x~XkoqG2907=U~AHV-qPD`wkSrOyM_zs`Mlj`iehvVXsCc*%-d~@aD0F@Mih8Cm2TsM<Lj*Xp|IPPbek9)mu`&=g&k(3+r;2_u4@P=?3g6oh5*MwUs6C_RK`&km2nvM(~<$|bCU&$0M#&AkO)xc-!|8~lu)MycuHol=1xLGeeO`9nZdF#m(WlRivtY}b^e)qxeXR|TKJg83~Tx%XH=uSKw?HUd^j{_)cN;n_fInFv=}}OCf4*xFsZBRKI*EvkGibxqfWVI+4aH8-_~FKuFNrey^c7^9J9Bp@MLq$zF!BJV~*MTRd<CsW<Rc@%rVF8=T&#IIp(ol2bg1yd8DiE5_8NW55r6{$2^9$JKG%d7}n|}bIfB{t4qu=k7315GRHiIB|F<3^B9)vBy-GTSg%XWG0$Pu&N9b5hjly49P=EO>fgm2^Bni&Ip&z>u$(8EW1houo@9<G@x&-gl@MZ>V@d`w%rPZ;7`12;Jq&Y92^)?%rlbwS98*GuQ&grY!ze1#T;WtcYOZk1F*Q#(=9n5N40BA45RN&fW(dO^Q=@}pj;YzfF~`)n;Fx1-TrkWrH7z*im>K{Kb4(2Yjya|#0K*(p5`a^cDG?yAI)`w|4kZLQ=9rQK9CJ*G0fsrIqyWbpQ(}N&j;SfYF~`&xV3=cS3UJIZH3b;vm>L2cb4*PEjya~L0LL6tV}N0fsVTrQ$J7*Hm}6=PaLh3^1sLX-8Uh@1OiclXIi`jH#~f2qfZ@I+A;8g94B+T01aNc}0XVt}032Nf0EVvI{~cYq|2x8R`*(!p_U{PG-QN+GyT2nWH-AT1?){Fi-1;41x%C^udgph9<<9R2%Z=X=mK(n#Ecbm!Snm7IXI^dlhWnP>_8ncd?K`?^+jn%;w(sbwZQs#V+rFVIw|z%fZu^d~-1Z$|x$Qf`a@%)=<+kq#%WdBgmfOA~EVq3}SZ@1<u-^6^VY%%)!gAYpgypthSKa#8Rk!|i(XGFc1TMFIM^|n8j;`AF9bL8UJGyGycXZXZZ|KTx-_e!Zz9THReMeYs`;M^O_8nol?K{G9+joTJw(khbZQl`=+rA;Jw|z%gZu^d~-1Z$|x$Qf`a@%)=<+kq#|80S^xt`ePan+sUiG7||-TK(e_}jW^+pfZoJ+WU)j?$K{%KLNW{Gyz%%Kf==dQmP{<>R^X_M%*`%I9;>=vU=-RZh=cb6=JBK{-A5=6;nP)?dnx9eH1shZXqT>iQ}@EW&r41n@F5rC}95_qx7H56kdf`@oIAoL-fOW%$;~nko;=@Lk^kRvwn&yH)|LJS@X^tpZqiScdOf1+enC3+746!zwh&|6i4dMQGIjZ+DR(-EB|&-j9C%AI*tbB8WnT^spULkEkHR=y1>wVYE1ChWNJdKmP28pMU?Kzx>62`m?Y(tlnmci<9j4uF9YM;<vx~*I)e0*FU=+N0CK(*gscq6GmeFbM-!87|yQ&U_ASMuR}=CaDL$HK$1Js!#2HopFa}o)2sLSBRxM}4e-NKmiS>QOZ>2uC4N}S5<e_ui654-#1BhZ;)kUy@xxG-_>t$}z^nbE1Q1v;-|k`tENpMLF(boXvHP5njV?6J7um=h(?pSt{u)gZd2Q-gKpS~l?pOdH-ULeMfQ8!mK4r`>r4A^=aHS3?W11~>z#RFx6+^%rGwj#{_%Qs~1NfL`$R40bHtZMz7IDm}0~nd;PW`3S*LF$y&j!TgWe}4WK}?x-rg0l$3~y`+F^)I3rWnT@TT@J#;7X-wraZT$(lAqI`BG`JDbJ0m0%|D}tf>NCDbLNR0$eGx+^GV1DbHQ=0%j@Jz96BcOxzd#Y#gMNWd|u`*+EKKc92q*9i)_H2PtLQK}uP6kW!X0NLj=nbx~<YT~yjpt+NM38ji23CXL0mv>HO@+0tqz@up8<NPTV~6kv#Bo*dxEV)N+$QRcZ%2aMv)poEnA+=MA$lxnyz1=vy7W~B#cQm2Kb2c+W7phT7WJT5&z6~oXxKo!F{J3tk~IXgg=YW)o$S>?O%&X!Qqo|kS&sA&c)DX3}BVM#Mha|&S<(zNIHlp0r>;ZLanrL7GX(G1h3C5r?|<ISH$n)ck`Gr*N*czgzc($)rV2Mp7uC2t2vW6hvOn)ci#HNcf-_@oAa(&qok1&&*q^*0wdeeq^cGEIA)j2<veGYaH1)3omZJOcJ<#tBgV+dAAQ=7D5AWWEkrrnLQ}T&}{^k4JbNp<YL5kK++uh1*qlpA?VqI?R3@ra$hTcoptf;lqzdcpc%mj&MGXM|c%JufmgJK`!HzZ5U@w*g$ZHQHB+t=A;dzGA!&=CMgdqJJm_b!-{^_^n;a$C2jQlyebc?*y#CrRUVeH(ev}FJS<<M=jT;<SieTk&x>*$R;<zU^Qt`Vx|7ym9oFEa$d6QqH8?5rLo-O4lS$S9gE(C{l0lMFSR&aY%_uC95R#0-5{VsYT49NVkYp5=NcKoG>Pj?(B%`iGV@H}+SE8{Z8L?*pSEL#Bwi+;!QE#gOBTcKf)wq$2dRvVfX-2)R=8k04+iLDe)9P(Cg(RomR%1wV?o>2~r0*&KEufaPj9StvYB4%@G@CfBJCaRcazwk0CNSTj-6j&6!f^j2Bs&)xl0vd^pCKtEJBRU_K2RxoB8MK9vg8d*S>lGJEGffMmXu*BORlh#C0AI=5+^KWi4&Hx1PDi2^Mj=<@xfA-Kwv3LAaIl=5ExxB8VHI*8VU%CLmCPQiqj-4iJ&-FladIEQvxiB;H7!thyNAnDj+B~?}LBx(=R^z`9FU6;*0;G3vo3g6sHnbLqai1aWy0qr;t=rLNN+SH6;|M3{qo4G4ebEPAEp8X8;Q2d7@_k3dM-@3`n6o&-4sPfqhT%eNdS2LCN>wp*XGonjXsYaMFMt9A!xl)w(!P_)v{}Qq2$52q@J6QH_LB4G{HtM5*S7YGjmZeyGnwN;N=KBcwE-h59_DG=PO_#FPfKP@m_N2Cz_#pwfUAs*zM0&_Xq$N&{M`&$CJcSg4N4ucn1+nEYy3sE*06riE&l{AygNj>)fPgKC)kYBZ>h$**REYS^txHZTm>H5ypLiVQ4a1qPO|;sQ%pae*bQu)q>lSYQcDDsYrF6<Ep=3M^#_1(vd80!vvUfu$^oz*3e(U@1!=u#_bbSjv(I9A(V|ma@bFOIhN8r7UT{QvTaY=@VNvbn$)NuR~61*{J<0T%TrrT<X#4aaC@9Gsx=*=XHeraWlw^aNDlJeNr>X>oDm$%$r*8H_dFn|HJQo^`~F{@v9@hAAI=m<B#;S?Rxxt9shjXjPfd6uEOs+I&i^MtAq5KCXO#v|2nHtYgik;25C-;QfkAZPjhmVQX5u%nv|r}hE@MI!v%Jbw_&xvYv;ffL;JAa-}Q5>=po;S&%oQB53h-QAJ%(1XU*WS;`7t^rOOMo4-5WX4+!m3-p6hHdHT|;^008<^?=YezkOJ^?|ML<x55VPYm$D_9QtX1ew=0zNk3Mzh@_t>%_5S1oMsV8Kl7SJB>kiX^iu)-SVi3$f70KBQ6x1v*+iOtlEWyHev-o|l75m?$gA-uE%qhRh?M5}l4xMEW>C{ma`t<PKgrqeCH*+rP?~<ycd_4VOmZ4HG$vWf5|bQd{k_Yx4u9JHFQL=vqQ8V09{+$ZVRlZI^k*(RosRm$HYHg^f8d;C5&eOimn@<`cTTd1{@hui8TvD3g=XmQ*u>C`^k?I%mzRC@SlMbLm`A0{{jVF9&iB7=R65=Nx>4!v{@2Z}FTIW?KXk0V^eQdCbf~s>zbMOZn>|I>(d74zP0>|ae(%r}^^3Cn+}Trf9Zi1J*c4r)^;fMfxyaL>yXyQUF28nlhWncS>Q%#jO@H+2H2*dI1vK&tg0Ee58l&{rt}b@H)L+Cp&-GG&480kYAH%xrsJ|{d>aSBz5$~M@=<j7?yDs=DHnv%TuOd=D$j7iDPCLjSxKtYaflH;+{VyPu2E5l?<TwZeGW*?w03UiCPr`fl6rF?t*%X}w_)y)}NqBExkuDv4*>)#FQGeR@8J@5D8@C&#ulf_WPcwbh-@Dzp;?>`~-RbMo-@AQ=<Cp%(?S|u*{>JUo9KZAzZ?_H$<>zg;4h!YyZU4?(h-Dc^H_S3*u|_v8D`c@oH_S3*twwjuGGvWLcPuSrkw$mSAY@$zedc_-;-WkK=DOmd8&UJRa-ze#rgR@iy3??%siU*MO4EJl=uTs}hK&yQ)9pTObf@W114cKR4mDp`$`UUuWl0s5vZM-2S#pG>EHT1TmK5PAOD;H^P7}oihjH>Mx!^GB#3UCS=zEkv?Iu;ux4GbO{B$H290-XMsKh)Rk0{Lr$KtqF%?`)BxK>RP-V92TI1HC9O%jLWvZYDlSRB`?VdIz=*Q(LOnnBGThY{DR+2b(cS~YtdMqI0AkHhGc)9i7qt4cbil#W)XAn9;i#TBKTPDhBMlyg<1?YXSc_H?QtC8nI#-@Xb{sPc9jQ%=VdM`Fs!0Cu}iDW_vTq!Hv~a11U}PRHg+Gsnr8W4q5Br(>w4nd3xX@{LpkQfY7<d^)C~8X->Ti<a&)#Ob)XX^1!(_@w&~aXP+vnj%idROvoMoQ^}GhJ%widA=(DZM_^5{W+S%hQ3{gEKhATE`-?ARk`}Xp06Y1>j>>}u;;6AxeD)-ay?&%sn=op^SOWdg!Oh+o)D_~I>LS(;d!X)t8l*xPYYFj9p@OvNsrwxUX_Pc{LWY7aVyR-tlD=58?+VY7*_2&gAK10=NQ)RJG+e-4K9CH9K-5;=eP0Lz~>lN?mOQN>fmz>EBBqJhG*e(4D0uurN*84f7w!wVFkal)OcLaeGH5Dowo+9=RU?QIIqalK8F=N%W2~rR`5ipjc?a!wBQUy!Avr0ZY8oX?~5HE3sugyQH3g}+pLoOwx4vHSQ6~|Nw<k5u{!E>8&s0t^ONqwOM*Q=={~O{Ru7);^Gfn-l+%55Nw7va-Dj7?YLwG`T1kG5a=H&N3Dzj5`{2SpM3*9EO)kl)tk$rC991r5?V44RQ!%d@1wHho{ZBJWaykn&mY|2ev~_AMNmj?GA`Qo7LXw7)rz$}sJB6DPG_uo*CP5<`)hZGytaMTd71^+Klu%)1z-oeULSQvOWTz@f6GV2(I5aL~ql`n-LUxJ}G%jSL2tlJkb_%dG8f2#eOQS(H63sLjWT!M+qXF|>xfFb8G{{a7yk>*UE+@);G_aH<8aT?53<`5nzfT61up$FXSb>2hthm4uR$O2SD=e^t6&6^+k_s$kNd=a&gaSudGl8WnnZQz(NMI>TB(Rhv5m?F+2rOj@1eUVo0ZUopfTb*Hz){vTU@1!)aFitttZ_|}oKR<Ux=UcFMx(m~hB~d!UE)Li&MXKeY*eG*SHgxRtYE_umat(dOW3fKC2Tm#8a6Ct2^*HOgbhns!iJ?RVZ&0Euwf}n*szo(Y*@+?HY{Zc8;-Ju4NF<VhNCQDqdD%dk|~;F4l7xrIo_}mCYtZxdcP#1LHpMG^$*Q)xRsdD9LrhB35|6eZTC5$!4@!3?9d#u22Bc$-4=q%hUVB}XjDMfVue&TSjrL=EM<ubma;?zOIf0Vr7TgwQkJM-DN9svlr<_?$`TbEWr+$qW03o|6qc|81xr|Qf+eh&z!FwSU<oTCu!I#5Si%wrEM>_9ma@bFM_J>5r7UT{QkFDeDN7o#lqC&V%8~{wWk~~;vZMh^S<--|ENQ?|)-+%#OB!&LB@OgdH4A-J%|c&Qv(Q)7Ec8`13w>41LSI$0(3jOL^kp>*eOb*yUskiwm(?uvWi<<ZS<OOUR<qET)hzU7H4A-N%|c&Rv(T5-Ec9hH3w>G5LSI$0a9I8f3I`6$eL(R5Rla|Xa5zT0k_ZmRXICNt^d-H2WpFr#QIZJ`!!SxS!QmK2X(%`h!zc{}hhrF}so*dSqcjy9j$xF>g2OS4(p+#jhEW;}4#zM`lfmH_MrkxS9K$Hh28Ur7rP<(c45Kt09EM?(hJ(W~jM8*)7=}^j-`2|+7)DXk$Fp9A%R}Ky7vb5i!u6r>rM>Okufpx2@TDW~>{sFasY}zPP3%0b%Kf?W%NOZ9ugb@B<!`@ndE2ha=X2%lMLAuS-x)vA9V>5nkWLTHR?<azSb*=mo+umSZCHZosY6V@C=YA!oyQZUu)Gbc@SUyG4J+eU<zX4Vb9JJ)o3~*dzH@WB;l=Z+JgmcaZcg;iikyap_|Cuy1}Wq;EW~&IO;~wYhwp5gu=2PO=1I!KGJI#$gq4S7_|B+_Mqx-SNKWmc<bveX9!fAsPVJ#2gX9$LNi;}K(Vj$uWW>ZvGH_ftG#RAlvF!mEICdui7(i1c00xe+OaKPyc@%2^29AYK00s&DWq)3fRFZ*XmlTizG#*O#$-uF}3djH&52gEL;Mki5XaJ3e(tR{=OzQ$RKo8w6%90I|Q^PLdAUnCf5)QI+S0UjbJ9iZl4zhDsA>kl9CF~LovQfb<;UF6Y>>3WBlUBM92iZ8b3*Z1cUZwkRkc|V<01lvEQo0WZ**J<0;2;~v{sA0h<Jdod1L*RU@56y(#T3ASVZ{`{fn&uKzyUM}%J<>GQkHCBDN8mmlr<U@_E%@SO$LSiZP;#uK|$Mh2lok7x!eW=s+@0wLGitg@82;L__sj54GV?+QJ(L^Lh+rB^L>6O@K3yaA0P@l0?7CIq4-Y6`94z=_@{fm&lCk7IF$QLF=39%eaxV9RPJ*|VaFTgK4wf<Y2`k8(3Mv1qX%*$x++Wbu#_cwSjrMT3}uZTbyX!pT~*0Yp@(z1jULr;2bJhi*<ZBxOBt$T04y=1t_{N0BvPm4U<Y90%wIqu^|^s^03p>dP!1@huFb&?sH9HI!44S3n?cDa^|=Lgz$5i}4t9Ve^?43<fFt#J4t9VZ)yTmP(4&3_IoJWC81_g3qgcw4Q7p44#VF0l?v{+w9QaX;(j53vh|-)gPDLoqDdSXx(wxW!NhodpUR7@sO0%}AdY@37`3nf8J&(Ky2&Ea(A_1Ya`CMA>6H2qdwB9EaZw4iyG{zD2KA|)t1Sde0=|B5rbd532&wd?9QjIl(nra$@JOC^0d8B3lD{Tsi?SD3?rmdoy{h=#%*5(<CcXlJNOY+W+&SVMz9;$r*Ool4ozYf}G<WNiW*`LQyYpmI4rBDY{v&WzF-~ZuvzxvZJ|M-^&`T0k_=er(WlF!b*Sm1(apO63_5YYZS0zROdeO3f~05|i0{Ypwxc6f9E&S-Y$R6-Nb?(KzNP2*qQ)NecY=U``)P_#QI36g>=WeGu+vV@?0*@?}*?8IhY#WwvR+f;1@qS&UhL!$d^)2+H)#Wvll+f{7SAMQf;FP=Kvgzn!vb!QK{f5X%n3WF=9{*eB_)lz5p2d<X7!++qOsiS?ekRzI>^A8SZ;QWKL8EgK*NliEYWY?I|CnPTg;L)E)F9qPyXJs!17}Dp3FIm@2eHpa$Wzf=BLCfI?D>Si$6`EMWicBnF1tylT;t@+&@rWU;3B(eX1Y#*m@UWC6cv#93H7sRG8kVvI3`<!8hNUc#!cvw<;V5g8IF=n@9LtU{j%7y}$1)l?meIhmiUv;REP9^?EMY|hmaw7$OIXo>C9G(`5>_-|2x}U!ge47F%8~{wWk~~;vZMh^S<--|ENQ?}mNZ}~OB%40B@H;rng%RoNduO$qybA=(txEbX~0sJG+=%ArL))O1e!=^FH2cEds)iT*~?Ov&R&+XboR28rL~u#99Vl<%G%q@lGff{mb5navZS@SmnE&;y)0?%?qx}9cP~p?yL(yE+TP2N4(z=wY3=W2No#*EOIjOzS<>3z%aYa(UzYUWmdsZw(iU8nJ^bVcA3pr}Kgu40%dle@vpg8{Qfd*5c@AUNhrYcRfXmyU{M5#HzbL0cd4H(fFUomPe&b^Nk3ak2=imS5FW;)4{w%ncybe)@A>P;-|M>IIzIT=W<QKpF&A<NQU%q*>^iXve>W#he{rlVN5N#OZo#S|TfqRwSN9m_d$5-ibai=^<dR)V)Op+d#YN~Uj%eYqGd5&Z0ak0KL9mmq+YJF!qj-|&{`p$J6OOLDavFrF%dR&c<ZO5<D<7&*4R%7|dRy%1mmT@)aNvpApt1(Ynjha2uT@LtbJ@v<%Ng5%KG>3K?A&>Nsc8b9yX&I9+hxGlmz)nL6mCpBJBt7Dt>ktw`(rw=P>TT8oX%tD1aOXOPW|Bm3=PIq4gt>cP-yjVoPk-kE=*0V>3xJiUKXd`q0)OZNsD=K}1Y4f|(1c%-^%u;Jfad8>O~?lR)P!sjVT2u#jU}zg#*x-!lV_04^&Cf%O<vKO8<0(AXDaPJzhs!h0stmI`f@aKx{{3@qLDL}{OGIE$k|FJAB~2NRI(906!FW`U%3E~@qT84HBWzMf;I4mCLEL56*s{bOIqWLC9UbjlGe~-Noz*2q&1pY(i%-HX^ke9v_=z0TBAvMgeFOD<{C}PtOF2$CdC2>$tK0xwj`SrBQh^wlJamv1cxle+7H1|OL@2*l0%llwnK8ZQdrwJIa?_+tULl3DTbFvz#wIsnMXh*#j(=}kfcm#WRKXSJa1)>*rZHrW)DcE5J#22oyT82RjPgh4K&4ZJ_(4X%xjnZ@>TfjKR;@m4M?aM9W4O~S<;$>9BEBLb&lf)Dt)O_TFoW;RHM~glTV%2YOXQJF!&EBsLn82&=gb+qXmsUb(+yaz&_P5u#4cQ&afH@D5x4<BLV!>X=Wn<3e^R>V?n1j)i4{37^zOM8;lsK8is=bBh_h^g8?H|!}KqJpK2knh9Ar5KA@O7(TC(VSZVsH>*%L0qn~D!h-k)XM%k)Ho5s@K0NOMbk_KR=`2k=6a2gB%17Oq8esIYa(`3_}*s=g-=wp+UoaRK*1rS4@I{}KJ&z%6c(C6L&lF;Yg0FpG8Z?^#wX)tnb11QqaR(rhulmUIv=S~1W=yPX)AI%BV4Df?KH@Q!0PBdWv63xl^lOVAhRUjH9_U9SH0Z8o6Lxuy8*cqa<`yj#0-w#3!yPv=bKw^ilIXEIgX#uPOXg5NhBaYbpFlKT-vcouLazL^hiPaHW>`shyfEM(*6F>|4+zGG+eQv@Q^tm^{7HFmJ7io<a?6I%f8ZCBM)0_ZW(C1D7Ep}GwngCfi(wZ!~Q^cXsqB}(#nk~9j#3A8=N~imD(b3Cym6mitpL)BG67;FJ`zQg;`8R+P?5VHX8YMbBdQE^E=yQ`J321IlP9)f4U$g^k=<t$+oJi2;CPxyTrF{}==r9kCPy>6rGdhu=&z%4^(B~#667;z<zy|u<<V2zy(e(j197X|w=7!^WN^XD+hZCcyvEg{0z#CA*;Y5CFYB<oB^^!`isewK<xXGYTO-fSfW0RW<`rHH?=yMZnpwGPlZlKRiZZZy*T}`mzfa%Kw8xFJ|Y?nP!a|3;Da+5)yn-o&e=O#B9^tnl641I2LlR=-Gltdg(y13>B%jH#agQYCF!BN)OU@1#%u#_b=SjrL_EM>_Ima;|$OIj0yC9Q$MlGeOnNo!niqyt*8q%|#A(i#>lY0V0jv_=I>T9bk$twF(()|_BTYfP}DH6>UZu68Z6%viNOnI)}V$Q<dwY|N6@Zey0Tb{n&#wcD5_tzE_}>A+Xa(hmH@EbYKh%+d}F#VqZ>NX*fWtivqrz%tCz4m`sw?Z7k4(hj`BEbYJ>%+d}#!7S~-6wJ~NT)`~uz!q%b2A`aM4!yxU(!mCAN$U;XlGYo%C9OAjOImO6mUOVeTiU?}Z)pb`yrms%@RoM4!8_W~25)Hx8@#0*Z19$Lu)$l}!3J+>2OGSl9c=KHcCf*xb&e9AcCf)a+Vz{Ylbkpe?R9k>GY@0F@qUl*KrfxVwG7hrx%A83R;`0{b3;3>L$qOt{b6RuRe2wj-vlyvMn$y`<Ge{{2wedFYS?!504RF+V;KHTg2RnEnpfp>P=1%E^4I~OZQ~f};qQNy9+&yMU=_~+pp9$$UChdyH{d${_yI^ybCWJFR~tV7sXdNldX*j*e%c>rGQCQVEB{><%VYQbHm>@2p)AyWzl|&UT__8Dajyf73;bO~OZe@${JQ(NuHQwp#MK3t;{E+2`*(h>{jyK*<63?f((=H%;;YsD)%Nyn3ybn+{Xpa5ejM%62nVG(-dc@tP;z=YGzTT8r$cj4nqg+CIVc%kmYRdo^RG!G9F&ajxkel-jU-^4Dft}%<2d;p0plcRt0;hRte}v9U#0|W1R&!CYXl%;{RS0aO)^Y-0-8xP;u!<1Nk%+l05Zl;a2Y7Tn#5XSE1;UhV2nUbn&`)6!Ax2PGnxGv-0mYwMqj@2>3$zsvg;{u9Zgb9hP`V0eR|2P<z~N6FZL8&N0SVbVS~?pA7W4t&vo)O!_YUh19qA4igv&=^d0R0Vc<*J0l`doOFMuW`kHn?GnqA_b-*w7EM14wOp{@6PzNlNS#MAWEMw2oWw?N7GHli80BJI8F*yL!OqiwvkPDrr<375;tO<ZF<>nmy^?*kYBtfP?*MWAQT8aa95?Y+uxeg>5roc_D-3OKey$$MpU@4Bnct9-0@vRPsg=!~&C&jUn2=JshRuTc96vIj)V3FcjNdzoX7>jIxMT*ln9DoPQEV(pO2jEehM(uz+=yQ|%pyD*f2bfV9jAcL>#c3Q4kOHNqT%<KoJWWkWMukgVSK(6ERk%>;bRRFO<HV$aq8dg_nkTB`!=!nlvOOpPoT!d1P=FKFu>}fnqB_<+0ZvrMx+lPi%FeP1zzLY9Q2<R?i5CG*Ov#K2u)+zA3aDaUYE*z26O%!b&I1W}#0l*PaKw_<IATd_8mY_bZQDZ{X-1t%n~}P%siYaH>l#X$Q?XI+6H2p+aU`L%8ENPmRhkiou1Uq3e{u}c*vTKMIcYNzP6K>tM#5=8FKt@FX@D|~p)^66HX}waV47yc=mkjArp4$5T+`t7B>|f@BTO=2nr5U)29(mK#YqOt(inCVW@+<~ul?B}oVJW`cKDaYejjA)*ojICQg(P|0jf{v9QFGgGhvSUeYBx-)bAtB4o{;%`3aS70Ar|j1st<G$BF^J?9RDj05H3Auoy54)h5?DyW@KwzzR&EBG);)6EYC+35>Yf0G?P;B>|RLQ6&MFz-+DrNQ6yEN4GgvI8i_sC}O3P+njDhtZBIDM#P#1iEc!!X^!YD1s2qUbeM`+?=wSpB40H#be4$;3P3sxvm+-T-HA~QkfF1HIYJEGNlpuhp*!hj0WowZfh-_~?j(=}!~j1dgc!OL${G+ucS2bMWPsm4LJVw5PE`NVofzf-8M+h093Vq?qLKq-=uT9!W`^VLoy*H<(#J1eP#K65>!OjuiFMIPal9N7emx)eP6{)*Z?WQIG+;RKF`6%o$w`DZteBdBHmsbQfHti8A?#r#;sopgqfW>Li!nbNx^A(uG6D{<vN8e?u_lPrk657`0hO>7cAb2UB~+VW3DqVi8CF<MfF<;~36@ylMEf@jDNnRstNPw&AI2<?4YFR9`=I>TdF^s3x*vmd^R2gDhd75J_Q%d!FUoxzl=~#(t=DnVFwXJV_v%$S56b5xPrY6SY2Q`tIz}DGNON5E`nZB8xvE_U8kcP<bByi!xNhGWrad;c>*E4`=bT23?fSTI-#Mpw#&*ZJj^FvHQDeDdT)OF)V=Q-!YxkXf+GDq-V_d}VoYSaX(=o2ycg|^^U(@lCy*N*@XgkKm`_4uUTeKbH>V4;kw%E-?!VEOL0?6VR{b*!K>_D~NCzb@yJnMZ@N$kk8-Y1m=Pxk<vBzU+7=p?Z#p90_{!8;!UCG-s;RFc@858;sH+{*+YlHlD*0ssQ7suBPYHYJymh=4f~EL+$BbinWG2B0GuH&p>^&~>u`*npqb4d6wBw@C@$1^u`tfEUQ4?0T6bfgw9(qM8`8Q(dW%fl43unSn~5_n9I4HKFHyj>xcT?!3<t(Ae(0j}a5By-t7@)Y|I=XaTLgPCynDti4V^8`RqC1hfIIy-old6Rf>X03g)b>jVG-t-Vgb9}_&QPQWD8v+4v;lHmo!0ieY4+6t%y*)XPyw1$!iYv2H!Lf61?A5_XLXZUuXV2V-YssX0JzgEDZN15SVtwE+3#?=~HigC)MnWfBdlh*K33^VBfR0{lqzW`7v@DKh1NTskp_zR$tGQ%Z5pp#;_<Og&@zX0Sirp(Bi36P{1Su+8W6e9vAz>fm$1rorI0{eXuz>mUA$`hauOIp*1C9O%rk=CG5=U9WFdXOnrJ(@TirydO)^Ne~lbyTBhMpH+f(UGt5qZ$qQnmX#Ve*Azzs?m=hAc$qu7a&NT;W`qqNHttX0tBhkTt@;RsjT{;03N9`oOc2qsfP7Vz$4Wv9MC{gXP80-U{VcNsDMi*dZz`EbOFUwBgG}47)x4Hj3ccn2HH3QR%y#>SDVpIqY<S!T`rnRn$hK=siZmGCz?hYJ5L5Q(wu_+06-e-cxZq?nqj<u9ZB;DouLLeq`?#L3P7Ye?GyofG^bA{fRDyb*9mhpr~N5_jt2X~$SFv3jL!quK+~O36)OFTlfu)+?1MAlhvtMo1OU+-Z){BvyAg7t31WA$M>In03?bTmgxJ|W-|iE{4kHfs`v|ccyV`Xi2^2g0qU`sHVrQ(f1EAQgO@9Y?vBM2+2SBm24Q>ZKL0`=dcw%>=&;p*=*(THhPVCSh{{TF(`*l4BK#U#krw2fco$aRwAdKCw5hIl!bhjdvA3HlzC6yl&3@AzE2leO!l^@;6qSGMKt>RY+BHeK<)g;mxnC<sTq&uOlnnb!2qN>@W8yTt^J($r>M(oj@Sl@s)=yQ|fi*7JeMu!=6h8lp6ZqR(d9^GQ@22i9!f@%OoIysrXN^9(}q&0O|(waIfX-ycGv<3`IS_6h9tzp8E)+}*27tI<b4#%HC!^GhjH*1(UoJ2TH6Nh67t!d(L9HBK$K(n~*K201>m})>1hY_Y4z{KH%sRl4{7-6abJseJ$YCsRrnrs8~U>O|+yg(hp65s`@P3l1pC-5{N2Fq+KKnBZfD`19$9r}@i(8G!I4WQv*2Xo{q<ZuEvk8f5^2`s{B$-}t~%1;f2E_DfK8kFlp<xBCvnFr<e)QIYG>v@(z`i+YazEC~uApOQS=m(#D@!!WOdHuueTjfe$*I?~>^frwC##)H~QTRI0J`8lun!!FuzjFzrj-2N)N~fofebpWp?>l#}DZl*d@MRlU_&d)qe#!JY(zxQ^S%}d|EZex|-&u!Ix6!hVi$3kopZisNT=l6h{qbLiAD4YPX8riDBaQ1mowFu!T=?&t#csgHtMs_=-#Lrj0D@QPk8Ilcq4evnUDCLw-&u*lQuva_MLf|-?5{7<m+zpCrPI8VX7$<v5=t`)p*0dEqYhdlQJR*HtNADyRlORI(u@uy%|OZMK+@2Yrgb0%1eD_4<oAF0-LL-i%Rm0*Nq!!0C)e>cCMD+&5lu;HLJw4gLg{%ERKz}MRu@zRLi1mNf?z2bTTj4B$v7O3KqyV<!io?mJ@3Mb2q?|!!isnZy<R{0!G{k&{>Tef^%H1pO0Xz`a8vT&=BwrOmygzqU+Sk{&%@xH%D^ibQM?+bvQbH^p(z{Xu9}rHEFl1}M5V#`5p}8p=SR?}3Y-mPr_x`85tUAWg{bxhI43)oHv#D6+b075?Zf9k`lmYwfg50;{QT}HVxVl?9YxqPeb%nSYwCd(SsS39%uXOS06m$VKx}|@GQ+?Punu*=OaO1Fb_U==wF>~3Y(bF*kL*FwU)S50pE&2l=c&6|mhNgAUL1Ed4KJ3vnueDt?rIuh9CtO%Fpj&LW|%4NYMNynceMazEO)g4Wr`Ee8=y=vvcn@zDTc*-1S-Xd{*6GT7}38Gg_P%p>Jfz$Bl<VOkYYstMjTR}NB>3~QjF-|h(n4I{Tp#eF`|DX4k<?TZ^R+RiT>4i@zhf-xNeYm;n;;~yr@pmj--p~6zxc;sE(P4riwbhvIdYxwJK`>e|R&f0i;?bRT@C5b-bhjq#8yN5rEYB=QJ5GN`3BQ5g|%_?lln+N}Z4*7@<mio+22LN}ZJ=7-38GZ}EyAU$aepo?;lGO?8ez0<@_M?}qAxyP@)WHT31Ie0@6d<=gOeWz23}64hmwMD6cTbJL(3a=Fh)ZHDEehNWgWK5AHMPB{;_Q)=u44BRQT8RqDkhnnGy9^jBM|2tx%=9sVtY(%vaV50^D>B!*>bJ^Pw`Lqef^brEJ=f?CA`B?8I;h^^10Y4(2HX(^PqMP<Si8!L0HY<rZLY-zL5l5)g3`60FP}+BvM67vcUsm+8FDrW4*A>0&>xy2ebiNNLR65-!6e_*lCzIXjSPsx+pM5HkQDMw(G)xD)vO9$-8dr9s@i@Yj-Dt9naAlug^pXI{?9Y3ABa+#l_u)qD0-fK;WfQbZBbQCPRhXigWnXwAvoAc6*}sdzl!#~cWhX9<ubd{7?y!#}6zb5n-zOC6(6-+vl+M=eejiY}lQFFUg*y24`+(9})Jg|@(%F$x2kg;V^-u@w(OF?d2kgPT@Q#<4FJcd>-2i(~ZPG(TwF@AN4vS4l6H#ZyCZu<$!(tQCKHXtq1?itgR%s{dpLV1JvaqBzFBsARFC24fWKj{zv8;&YSXRVxIAJ>)B#zmoCYcnv9G3MdsA=(LP@>22+!P@~j|1jhkc*n*VO<09i8)wZ1Mz@4oVo^L0dp*9A1%lz=3uN}0Jb;|n-R7g5BrnJt<J&vlgX{l;q)hytDR$d;S4)VIToI!91G7<j``Is`9B(;Csnr`%g$O($GAii(z%R~&SivjE-UjrjbJ|wKc^G_rg4W#g9hl+u?`J*=bV2#kO2~%>~?^ZuAD~Oc!WZy;Vv4{&pE$jm|Pc~&ZUY*pVKfmjnL<uf2B$8i_UfTMd!NvqI2PW(YcUu&V`I~&bco-EQUFkF-+Rv-yg*NZgYYO0^7UINhS!4?=~lzATYbzoNR)??rxj?(W|8RC2i~mC;>0L4Hk8i>KFKvG*sJ?HugsXDQ>~<5-D$4@iGzLm$W_4tO)JyHY2qn^s<{iaRoJ9rwv}G6RyECN62Qy%n|%an}b$?1>UyMBnFF<x?U`f{OPtSc$KwFUc@Q4t$|-oAK%@Cfy$Tk>LB^G_}ydL29PGft)c;>Nls;uCK_XYt^;XyNltus058d@?GD%_IeCH+yCfq}Fk+X)4)q#Amjn;U8sU<}j;Kg^OiD&-ddMZoh%*nNBe7$moiIm&>C~Mt2VFp&00mq?od5+~K%MXeT|k}i1oEW4Y6m!BX@9eRY7mzs8R2gi(0ANkN~*({<-wSj;+&$#Y{QuKX%NyCCHFzPJ(qq#;M51{H)$)6Z@SYl4Dlv(g<f>0b5MShr{djn=WQ70e4P08s+<PpcPUDbEjn@@$4C!<fUESlw%?^Gc@`acT+r!xG}^25xNhGCCEeL2Ulwj27w+?*q)Vbr9#`)3protzxMbf2C4K*g{}m~ZOZHs`(m(#}ho67{pTFF0e)_ZEt-Op;#^w4h{piP^fA+oM51(KB_Ba3fi+}lM&(ULz3pm>g_&Ub8fb-J@e3kyl<~%7Dsf<f@RxDB(m+Zt?q?fvx;C@N6&5~%OfNc`%=>P<io*Tjj0Fx#d!UiCdo*Tjj{9>eiT*r|#lMLV40ALcdK`nq_(4SNLMOuSPn&4X#5lnh+ToW-%nq^!Q5lk|SYa)V4GfY|nl1YY1O8_!ynn_E*HOVk(32-LOFlh-eCK)Cz0llPYCM^NWB*&yBfSKf&v;;JhzAKZKfM&9Do72=qNPsj(BvODhMkG>zH2L`j%XJ*dHQBhQ2*4&kzoiIJ#+aPTIGSr{GEf6tlbtJt0Bo%J*#X^T=jtNB8<<_R1E4YH=Q@z48yb?d1FFfeki7w{u_mYitjW%eV8AsQ8UgKqXQ*}uKtr_;z%X>a55O?=xlh0_^tsRbSYjjt1>6A>Z~%9}Y!JX5#c_hrs6mrKz!?e*1_7rgGy?;in$QRga%xh@=6Rq~6Z(db`yTp=kSiWEB^_PySn)*xLePkz1Q4RIv$X^Wf~KNv02&H3B;Eitz;E^jn868j3Xp-Wn++fX{I+g@7-;BH0>nVSuIWB8)HUTFk|pZHLJDv{Q&}MexSy#`Aq5}|BZVmdj0$V_!C^)<DqI7?sL&*(0>XG2{!#&I!0?v}NW%($sQ^2waZMdyM|DcV0_=GDy(s`c;0LDw{II?_1+a(}QWLO9op*3wbQwZGE=CYdL@t)J1{X_OgNr4txy6yz*wX$E)g(^?AON<&{0D$7R{R6NmiFAQCcu{F0Fk7YX85lK)Y2x{uSN9I4EwbJTG}-GwE$t7VSW}sOJg15q?lwzR#yZsMp#$GEYs4uB7!mEx*}$wp-Y5W+JwmZ2uIrU%=!pNtk5L_Copu0z{z(O$`heXBPfGPNoWwkexF!&!{j|66)Jt)N0lA65g+&Igg*6oA5Z90pZEC$CPJO}@nnbRH7CFlm^O6+ETK6?Cm<0R6m$X-*<ppr2~cE*&T|Jq5USk)gU~tY06TVAmUIB_pwE2(?tmFX2fz)wat^>7Fu#bDdeH9_DfQUlUw<7?1AT7LD{O@D1k}(C8;^h*y2Uz@8t7B+_o)G<67Bb)p|d@5zt0REF7*9AG<3E@?tmG(QzxmJp<5+}ni;4zxpV2TT8vz}bY?SB0W);S4CLIR!@ZXrRdlxZlB0@l#EnMCK$kn|cR|508TGqZ(i#~oX-y24v<3!8TJyrejzPh_$N_yb%Y9y;()m6wQ0a7^7Y^w4neGF_!Kg3Y2L>mj=Q5DShr=+Zjrf5EoooOgyb0O>P8^QqYJd}m;dmO*gfl_cku+Q!j<sq47ckyy18m{NV3DfQ!wB+@P~&)>q#colGeHRznH~@!Ns;Mc<bem|;Y`qVBn=`5{Ila#`<o@!9G5dxa$1gI%rePwtek^%o#Z%Hw?Vp1b{wl|7-FB}I9BtZ+*de`)iR9p#wBS<uvV?Z@RJPBY8#ZN8=lpD9AlE<Ssj=88pE?XuI+b*XLH_w>-ggb;GHYljpCIT={9}<-kGA^_^a(zdR+MLJkf3xWxPs{EB~D(+G8V>Hm>@2=4jLirHw24ohO=Sgwn<Z{>~7M8lkjtUBB}|!v-JiBl~xLuKlu4w{b1Mb3%I>_qTs4>xHimG%oIU{%N%ELvzp?M>Ner$vLah9F&~18qGmdTzxbLIi^0EgXVeqXbwuo_go`Rf;DypFwPX;vVd_M-?D&l=J}QdjFX%?$ADkbj5@~vWRg+m7=TQgR_7RCjbr*4(99Iq#{g>_+s6Q8=J`GbSOXmtE1;TWRIvt7^WC|Y1u&DA!HnZerjf<*CDX*>n0jeo$wu&q<`l~aNP~)H@TA$qvKZ2ElARcd08TQikLZ9&vQwKFKuLCL69W#(Mr~q%A=#)O4Co^}^@9O^WOn*<0N}_@xq3hx*{N3#NFy5s>j7zGqpCb$i|kaD2XK*%s`3CX;9heAT(F$VG%u8iad?g3L^0}SHBJ-*fizAO=-9E}=ZONpjDRN!`!E8WC{ACK#)$$yiv%a&3qo+Bu+L%#G*O)JvVbOvkzE$hM1cjUJHUzJSj7f7L7%$;o+yq7aKIDvxyi{zaXf&@IR>2|a&%D`Ig_J{0xOFPz>DITcNYK~^gC1T!$$o(RGc{eU79ndxK(N3aLlSSZ_M+m((q9i)CAP~gi_glT<-%)oe`oHfJ!w&v;t5ue*f!08e6K7))i1ob^KxiY^gI0V*-4shG9%VFLjz>On@@f#E@LZSO$p!%2*DG0lnP#=DpO1j-R|;53d2ITJ_%z@Qyc$ns=bbVFQFyC)Bo-OKr=iUr*<kKb=0hkbu;TpgfI1&A2nw7}S^rF`%DjIIwH_Y0$_Q08e8s>40S#G)XV_VWvT^XHr?xm`6G(C~43mom9;>=#fqeWt-#e9)Jtg-T<)BIoSZQG{ea}U=-#}cDzn^z$kR(B)}-}`<DQsH0Y8}N?z&5H3Q;kFghav;-K0aKn^-5pp9prc!N{P4bJYAnn<MBjZzbh6uVPuB9UTuN=+nD>`tDQMvC1r%+N@&J8@s+kYsm^IRe1g4P%agFLuY6Bj5|FO`2?Wt2dPN+)!&T(sTo@y-3r|?i|#U&YRuw8VS&2hc_97J$9@8Isp=)Gn4>{K$kTFBD-~flK_@bU$k@|OB`P`%^iIicl2f4(Va+K4IZ7nhyXmgaRjHiqr+Zpz#ZM`Fb`0pTP@}qHK=w1tkE5-mw+|kY9vP)9p3Mdqm1rYmjrMD*9|$!=&TQU131y4Thaz_qO)`D4bVh~4OxUAIt&FQ{D2(BcEk^sv<3!8TJyp&^%w)(j2z1fL=LC;K;i`S{sA{5hxKQv#EHYH9xM0Z;&5y!HC#YTA;K1ib6!F&O{k*~X~R9>c@nua@jREv5eJ<ia;R~z6D4w{L6>d<+(ESocvv1_0eBp+y^EY<crIy#L+A_<4uPLE!Xe&@C0IgNEZ~y!@8Aw{&Pce^Y;qb2cbZMkX$g0lR8Gf2MU%=oBTr02%4x)jX+}AxrHKW^a<UUX!YJpAq}YH}P9rHcK$UY^Qfxpfr;`*LkjgnD9Xvpm(})KTh~=D?4<6vlxxn|3H098DfK;-cP6SB+HRtRq*@|jcPs>J{RI+-LsKMu)U&>nVma^{OtnJ-#m;KmzPLm5_&%?m8EN1sINYApE-RmITo=d+F?A`|H{kinZ-&gxSNWV3hM28mFar!XM8<R=w#J(Sc^mE_XSLJh1e(xKLX6G_c-^PK`)9JZtkIVR-do1-~@8d#!=NF4BC0+*_m+d=aSZu@I$94P88J60x_i^36bB4u-7kyl~@2p|*kwPCA>pM$Wd|1@S)%wm879S$N4m2*_x1O-{RO%Sl>pN3e>P&xpWY^78=I1)lxOm?g#A0LmV_dI~y<RWUno80{DrtmDEW=k#C6?i<rjq1@^JpqbPB@RI68h8tMAGx+)d-a&=Q2LPl4M-Q2Owfh&yJ`h!JB!4CD2}!fQT_a9Z^YgI&}gpNk*qmKqbcfTnEyKl3?2oL6pSWb_kRh^K&9XNlw2?fG7#}9wk5}^tltD5@gzXk=9h=n6_%{a7<e@bvUN28ak*Y=YAhLvSS#fp(D>e&b*E;xg=Y6(ffTc@n%qiNj6f412C~XbpsZe{>xv7*SM0cTlO8$i#LfHSh5of9RN#q8t4LIS@7dGz%kyB-vHHklc=!<`a3rOGSDZv0glN=<3)fm+336oC?<P1MqghIrNg-!D$M>K@Q$S{dB;+gykjX#+_97;?O4i^WGrQgE|#(;7e_iE7fV`$izTh0#FEw&Vo7TVv7|MFSkf9nENP7wmbB&xOIqWEBOTy`C9QG7lGZq3No$<2KB^KD)|ka=e5mVcN9v4{Mhz0xsA$w6fm~dF@`Dc_e*BR?bgF&;$s5qcx7_EADMp_fJRG0T06gaTd<Gb@;tjYyfu<E`<y!!)Fr(2+r(S?7Q+$F0ZgG5q18$k;6C6+s{S64lRL6ZG;F#%VuNkpUwaioq`dE_~uuolglv39nrPO(Gf?xg{{`%4UYHONNe%t2I6RL4(GuoCkMKz;sNyC$4y{qA=&4_i?c+`wkSB*z)#=gJn2axdO7#9cdM6FT@FHx&hLPF3gm5>m%N+l#jtx^dAL6c!ZKy5}OZ~#Behy)JUXT<`(K7l5rW@H5i^wW&2-~e};x4D14o2RUEf&(sUMow_RMV7SYB1c+N&Hj*Tk|rrhHIB`#h8f4^R>O>AbE{!yccRNQ#O(7cXu!Rb=W7bCp}ZN?M6)~LZvoL*hP46F?2ctmfHctRwE&`_E~yz1jpgndAkF=i_LHA}@!8M+@xvEi{Ev?;x2&H*BM<aX%>a4!hex^@K+Vq1bTfdO-8s|E0C9G9G?D?h?64`l0CL$K(}MtA_IXD-Urx}sR?k-y^Y&Z^5Kv!MI@6bx&h%xaGksa<OkY+y)0dUb^kt<peO>8HUspQQ*Okunb)_?XUFl3;S31+zmCp2ar89k9=}cc&I@8yc&h&MqGksm@OkY<z)7O>G^kt<pmX~fa>SvBw=QH3+=&)*bBwier-;3mn<6${az7HA)D+kK=LF2H@Y9whKj-yNh+;KRb_yKqvh9`ai9*2|I5s(M;t4@GCpkZ|a<lz{Y2IRrqV>fjEVVMjE>_MNq0Qj)%qXYV&&rR-g4ksoo;E%(I2@CjxTK|&6j)MS5BBvB<Omj7Roa-D`rue~X)NuS@HEEodJ&Yubr}F|(1I|mnPZ}pH_{o4RPMAqT3QNw1)kNev=49nW<Ti%AjhAT;Ami!OkZTz@HRM+2WR*??HclsSI)IH6RyrjB8z-xDN`N&^Sm{JAR!&&yL~d42<}Q-~Yn;%Sr2y7Ap)pGVo^IPR`;<hTHNmY&V)l;ZVx^&d+o*O2#%**?I&f~=*p*}l&TSjKHavh^8}+9>h+P|ey$|BoM&FZ@c(l<M<s>F;(3kckE^QmE>o|xr8#SXnh&3B@qdkZ>8?|-q#E*^It#)F_2K`n$ab(-znZ-d|*r>_sL2TGIc4~1D8#ZcPd=eiv`mUT{!%uLR*ujRM;4VQn{KPg1;F-pxGx1D=Gm?oTT0(YxnRuXi(!p-;Xh*xfr5$YcmUgh$TiU^1Z)pcxy`>%O^p<w8(_7lXMsH~c`@E$c?DLLxw9Q-E!7guU2fMtb9c=Q}H&*ZQ`QhzE)?Fle^UqG?eX#lG8BtvU1!N<tE1-aEBrpdMkRO(Ug9cSLGX-_1zP_r_Dk!L*!_y9Ez|szAz|szAz|szAz|szAz|szAz|szAz|szAz|szAz|oFqz|szAz|szAz|szAz|#I^?erk0j&453J}8&R$yu+;eNe8CGpAmak3qRTk8XOs0y+oj{du6$i}bk-(r?17CUuU!j-H0m-^5+<&e7L_@-WajYX-|8{VuES#u4eObRDJB^Q5R(?Q!wGOQ)M;zx_J=xWeBh*m3*q*OA5*|2)F(sy(jxcM*2D?Cu;FecGQt_qVm{Hm>^Am;U&#!;i~89kYJ?*OA6`pUzp6I4=BmId`yjv2NqSe;0Fiqx1Sz`Xifmekffo(&L(b7i@Rq3i?%gT*U8k?WTIK1KzQM=rr(HL3EmUtROm#JXTtqMjk80O(RcQ(!zgz1j#*4j+_P^CxI>C94i<t0G&0z$@LjD5INy&0qi)rW&zz;abp49toc>0&!8y?U7^1IDiH)F=6tpRz)8%wYXd}+m~qzzfQH@Rzit%~(NOISkcMg(z%*2wKut1@(!S-9u?J>p5^S6hJ<T;vh@Qq8Cqz$E4a`z&_o2oLg3?gq<Unawu`&fUtXPS70j<FFsvW>ehJM=}KuCsVJsnU8TrwR{NH)p@0|=purUSTutEL0Epv&d}bV1k60q_E@n*-nlT{kDd3%YJjfERGxoPaLix;X({&~<a(=LIViNAiNDEP26Fmb_poOI~o4H7;1n5*I9GNeh;;h6PJn!-6HPS;3Ols9;HJRIsEqDp=B*6b$Kz6f9{C3YN6y1WQ_Tf+ejn!IIXLU`cCAu%tC5SeuuGggUEK6x5AaA#|D_s$*!S0iw<@w9+I|4MQtU5-8p5dq4X5N6v?f9$w-GOt;JTaih+#LJqj28dk^wcg+7?uH$Psfthm|z)5xdy#qR_>~Fmc=%m6EfdcS^YLi-#YWOHcfKum|pONa2YSo{SS`lv&HPqB~#UgcGu}EE4EMlh1ef2f`YV*8jI<6_GIewzr(@UdJn}c7C6xTXIa2k;s^gaT`wQYtglxC!6m_lj%X^tn9=ASmh5-Q-IW>`W6{6l9Z0k&z+omQ^{Y0_c2Z&z(iIxrnD0n#z%=Q@zao@N+mMcC7x8)!w;W6aNWAk8;4H!uOBX{@G+)QTAMa~(+IO@qZ#3GhvWmS7nG4t?%?A6Rw=Sah4O29|wEYq16v6yt*~g?3mPTkiwQ?vx>GP}yg=wQ6G74YyVeEW1-f9e~O{!>%<Tmfi4c4S;2LYQO_V*`I%`8v>RcmV^^xL8*@wG0Ohj(LO>HW9kb6mff(<j~Io$n*|lL(&yd)q`(N$4PXfkFx&u^z<kpUPzjBq-0o9JUsiF_msOnfWfdoVS;a|TR&mmoRh;x?6(@aN#YtaRanjdSob+`SCw*PTNnclS($`g-^mP>{eO<*#UsrL`*HxVKbrmOlUByXXS8>wURh;x?6(?49TQkZ|4#x;ZGQ{B+p-6@}piwipQ8}D!Z%q+YI^D+zBR=gqj)aN>!hHf%;bescRAEd{LYFHvwuzioIDuyYWUx1LLw&e3fQ$6k(%>+1K4H8w8#<q$6GYA@oFu!5JFE%HfI^(eya+>Jgj)s}VtsVTg$n)XfD4tUfo{bp{&<=$2FL`aivcn@ohlLuCQnnY>U}_gAy@T2pTLZ(dY?$1P0Mu%O(tkwuF{%JXhIh;Nu%1NjFqN;kup}8{zb}IY5Er_W2Na|1;7YQ|0)1KX!;i^QKji$q$u?ye~O=|Ce@PGykSXe-ms)KVHnbpE!p<>D%p4$8ApzTs}!6P1};;q47|X^Y;!JX!R3k<wikGnSz&vDTN!<B;s8Pu@rVToj>ID#Aoy)3CLr{6CoUlPRXK<m8GTm{;xY!`m4n!f(Rbw}Mq~6{If>QSMmDXhcHlK;X$M|omUiGZW@!grW0rQ{HD+i>7?9><)>m@=@G|J*<dy&pl9AjJpg~&DHw(@wXzCp}sCf9x6mn$2ewl)fDi-`S1s!Ol1WV$`iN@n!hnTz5pNH7F(@;fX=Z;eq$>By?W2c(YDF{sI%&439;k%X5fe3rIGCB~!vqLID@XJMNK~iF!x}+F{X;)MYlG2=B-EVuL=07`U8c!qcoXZrJ<Hi^!Tb?KyVxFewftD1So(Eb{@YI0rS*%UUJW_^#^pQdj{N%`Eojy5oS<mcG9AvX@X$RC{X$R0@XooCeX$L4_X$J&hX$J&hX$JsdX$SmZX$SmZX$SmZX@9eJj=Ax6HEo0PoOrvM(x6<QhR|L9bVzxSZqKD(%5PE`q#q|;U8U<F{V3>){mu3I2yJ+T<8kERtMWc5pO2I0UX}Zx{4Uh)PC4UCMO`{Z?etvxWzD8>&Av;uqotBHkE`}wWZk6DwAbOsrTs3)j)$hbjx?_Hcd2%K633<fF4gWvwcxAtxYXZ;+THNMdX*lR@Vmge8-HEDN{?&!T|(WBKdxV;$3^@upzhAa)5{{x<05{SP<KcB<>Qk-vhn8U+Aq6U85i-pjJiA8FPm=}SLno$x|cJIoAzS?!=&f6lmWw}=jDh2!z81gFJPEtl=B4)L#5MwhDnagk!F)sxohb@#3aLKDS#OEn_R-f0*FblRFOc;nqTEWuwz8lMIe)4xnu(9k{m~;09{ta;U&O0Fb*#P#({Bo2`~<f!%Kj1U>qJn94oReKpZQwE<hYBvMxZJ?<}$|0GsU8yvkD4fP0LrynuU*th@kwjI6wXdYo{$fO@EOzfV0hKdaxT86yZSqL~bjO?E&t*=a=F0ou@1svRIphMk%nFbmZ_0JG3JIRLZ3gu4Tvh?5i-pa@NKI{=HokKqAWgnqJ403-C9bpjZHzvKy6B(sCF6QD?j_2B1yx+oLrq7k|%vs~K&cNBI;1h}I>5AJ#&Jj#St-T*+#^H$z~KZ<j9Ch?<8XyuJKq&#osjWDEGM}L|;3Oq$CfINzGt{9L<am>^+z>s3}BS#p5V#co08bd5;jUkq_rVvY7Q-~$4A;gl_4B|)!3}Q)Z263b{g4AWzCv{o%NnKZcQrA_VRKrs&KnN<m-DimEcm!*Rm>$Y?9bNN<6Uvp*9ga7L8aJxpvmDSyHGGyM+E@_CMk-IdKsHi`;!UDPlDe)CrLHSPsp|?+>cT>ly08$XE-XZ;3ky-q0KBg&Pf~VDPo4(QHF+zf(WXuCJqsA8J@-8e5U2TVr@J0rVo)<;WdaOp6Jlio9BR*FWda&n@v{_wLoiga0REW~eHd|&k$o6((EMNKI=*HlCwwsip&99m5ds<MixB~>_-V+=O=DFd<m9GJh=PiEsXdQ^ig0Pg=Zqj#TUhwg78bs=34O|Cb4p(JiBZC+<Yix0^0FJYWdTj?PBo1LrQI=#Z}+KbckBW*E$vQ0kff#Eacph?i)h$X16;JTBAy0tXop2S74Xmw>qshKogLP{G{8E$Q+(6_@X!frfOvLRXwv}9>`swgKr_~Q-2u|j^|}M5+1Yv94seBjgm-`|JGnf%N^4qiq&0=~IbLt5DyB1c6aXL{dR>6yoIb&yE+CQq+@3CAk8YU81nki#c*X<}(w|$#MA*?83zO5B4$V_5z>Yq_k}txK{@ju;qK|G|SqJdZXIPd6+|dokvH&|e`_NZ_9hS7F4og~dh9#{r!;;pR;YbIRVM%MsaHKV59LuU-4#QhBfC(y{@52O@PWK_=aPqe`MI282wx)<<cAY{Y6*7lWrch8Zj5mcEI1b~&Ki~}{-B9%ln~{d9Uk-NHMk-s_WACVz<yg{~yrY_zgWb50nwJ9}>yyr8`Zkf)<TXDF>tQ|?_Anm{uX2usS2@SL9_ISirUhN?oD&m#P{GXU_`^sTI-MRD$wDyO44kLX_%U#xazZN-aG-KNKf*o8sfrcO7GRDO&K6J(4NxP+Ehls1AjK{8g&{3P)*C~rSm-N5s#oAEL#kKkD?=(%*zbBGn4#LFgqP0A1|S74qYW_1$xLlFfG9M-a|4KSvc4kVYHLO5MV@ffTyF=iaP+x%U<(JWes^FCM<dZX@P(s^Xuu+c2BHCr6#SMP#PW^4CI|6+gBe-}@qBZ%BQG~gJ1}#zv;#9YOFJ-gv$O+~HcLBjX|uEgn>I^3@M*KO1EV%eJ1}Z<v?HT7OFJ-Xv%Xb&n@@8haw>9#P0p2&-u{zyC#3iP8F6b72N-E<5eC5MCvcnqXT2i(dMr-->tT@BRXpH;H2Y@j+D;j;LNe~Qu0sXrV9jI14#|iy3gICcF-9RhEO-ORb&L51kd|X}9s}Y?3%ic7I5LM#3;T|-II@RL-%00jz$bZ*iyGsTY?VxEK*`otsR89_h93ywp&5Q4Tqi+4UXZTyaApbvmCV>J6Hdui)lk4G)P4~`2=qcm)IrTf5p_U!QDi?)EkKd4JTxvw#`4tQ7Fo+vXI|2Wi=Uiy;wI?LiwJ_gE5uJNQJ>pF2!cNOtN1rd=$xGBSL&cVDbcUALAgFok9$?#2j$0se%FcagY^Df`t|KQ2I>A>`sG_v&O!Qk8hdt;uG=7eE{u-5j-H0m-=+C+TdmiT@;FkOHHYKsP5E)$;j8qxeBVX;;T@`u3;11b-=x^U*Wt%i{w~aq#|FNRG%otI&zi(>)j!VmyS`TAs(+mAcfr9nuKLH>eiuY;<C1=t?RVo~_EmaZ!_%Vu+DCTaS<!xNT*T9&{o1&QCr10-JlD|p;)MBWd~w43G`=LGSX1Lmaw;k{z9gsiPU8!e2KYh~=>Wd03Zx?p0|V&@v?Ql)E`XNg)XfFdvMP{n19X#&+P#2Wl2N-Cph|LT_X1Q|m8rP_rh$Qb8(^AbH2MTglblAM0BWo-zW{2iFuwq5tT4X-YQDQLKMghu!~8V&<XMF*?LHA@r~XzWQJ#Ns-0o9TwyuraeTMR8P%@O0?x+zeJ63lA8s+)T&<)^Iwz{DkfGKYhHB342n*k$b7z0rOB;^_YB>^pEC)XpOrR=yV7Jx+b+OGg6%1e;%`V1PLVA5Uz?39fnzyO`Hb!MZ{DbK^3{OR2zoB+8ptI7os^)x!LNMkn5PX&6$gM*{u*wJfDDl_cpH47EPv|Ynbnc>;4A*eXM=9+@a3|sSnhG4p42BbrC{>beXjo%~JTZNs%lH0A~9Ls66DQIuFwBZIwQ=Asx0BMTT;u}y5eQt7Fg~IGkbX#RfYdEo_HJn(|noTTejTnx!MvS_wex@#~pRqCtHAh&Pgqk0$OhOG1)hU0};IJS#5L{Auxq;*=%9_FeF{)8O8W2WZS3gsoBFum=s#Aj*AV!^En?oq1TD3WZNxVtaOj3<H)&NOhl41r(0+SRoKoXdwNUoad!upxIuzsfgC#avX67Dp=Q0aUhV5oGu4=_}EyALqUap}|m(-zq(Zudc_89t#JVpxRLj<BUc3sQnDZIJ~j;hV+|ehA;NpQR(dY4G5O@J(A(i$Wl$vBM`qHSA|O(0x&J><$C0X^ZOV$bC^`)m7xasIlrJa$f|49SQ!lg_SmK-c{7$RN6REewu)sygdy-PFS7hA1CKc;}4BX+wbEK4KdsAV-0=kexGaTQ+L2MFnX;6tfA3s2f!7Yh;{&8fr)4bz?Gf--FyIAp>d!Gppc#YO@06h+2P;KC!mlW*1Da5Lf~d_0=R&?!3p4kCi0ztF5p&k0=j^E%?aRwep}D`yx=77X<q0KiAY|cIcocTVCe7zwcjTO7;y%Gp~Jf*P%hh@h++*4-JrgJ7rGN28~{T%kTT$f?xfcSywHvG+JG0jlU^GDLw7=D17PSzsB8cXY)bNlST!)vCD{QmbcTK%07EzIrUPK;5TQB%hR(`4I{*etS_6Y4t$E>CRv}{L_Gw_Sa{DweSh;-~7!JpOOB2I_a6M2(;)Uyhf)Q&51I9QE1G4}zj&&6x2i&VOK#aq2qzV}0m~XE`Zdne?UWeSJc$289<S=S20w_70S_{o2hf`~zndGo)Ei{xIR;`7GlH)t6wFvO#FdAI~d^wi&&{#QqMc>Ovx;f`K)}js@C;LxR&-t*+qu!^VGydZL{tv(V)t`R($FCOH4?cYO@kc)TRX>1aBq!fc^Ut%{y9}YpXT|JYA3*cb2|H;D03;*c?mCdhC7J+M04~9l%K~WWgjExy9odQ&Bt6MiR%bv$Fj}wz5;ErJGEl%pG_S7$FoJn~6>t&E>myinvZ@pUJ1473A+U3rl_P)oczZ=7uTesdpFX%BVgYoGTo9$rYFpN>blbz`V!%H5`9XUz*3Q77?&;is24npE$bxQj(&8f%x{cknl5-uLib!f>X?iB<E`~p6Vg7P7KNC63K}&GtFb7S+k#ih%a7Ny7D3mTS^EgX8Fpsme1M@gbJ1~#4v;*@vM?2X2lXDK!^Z}4Y11DuLAcN%eIBOtCR+F;^f@F0$YamFD`4gdn1aHNO-w69*6EYluVO<FwUpUjB&|wCg|AdY+*!*u7?En#sDY}jn@Ir#+J;Y=UzD655((vYpoN3@WB8M6*>NKHK4R589Lk_&s$T7$3z8r7)$cxs|4shbB&Fk)v#M4|of)tsY<A3i*KmW)ne$nG=?yxcs1MYY_f57OB&EL&?kjoPUU}7aZMqn}}+A$)O74Kjs6yqd7M%*$b0y5&4`7>Bh`3lT)D~xOMi~#hAZ&obig4%`gBqH#6I*AB?R=kIZlAzBl;v&-w_N#yHUqs$qsIcOgl-E_qc-ntk%wN42Q}YwsF(^;UPi*I)T%YCzUXDigZIEuyrC+|udm5x4N2y(<^B~=y#L+RY>eojo!y_C|gSxK2Ngbrm=h824(%uH?cPWZ@v|p|y_kGk(&wub&?Qzw<%T1hQ%lA6`xU}D8D{^1H*OA7h{w`?|Phua}`nwoK+K<-9wf;Oe@v1#8_SBaKkG>8+F7$WVio7!Vb)<3Kzl&PrlQ=H?$61Tl*J@n%@3IzeR7Sr_e`K@HPiN$+J+A3@QHwW7?NxeQ#1oSiZ@c!l``nWz<`Xr7MNZ<Q#v&*2QB#qV_^6>M8D)8ziD&>|xz9ROI^SoV<oJvStdks{@ql$!#TF*OL@>560p6hzpBo^Y<doNL0C#AZ=mvOaRhsAqxX8(t44B8sUJM||$zBW?$I4y|AjisH3@FFSUJNM5%3cgGXJYnZ)y2J<ZJfkA4KGfhnueEb{4J*8B|BynnqIQwRiW`E&;KKDzfU;X`WtV*&pX}>YTn7LhGYl0lO4mp0Auoe|N0%EPPY8(cK|-tBnGU*?qD}`wv!#xo`7K%{P^T-$NTZg*^W1fntQV0d=y|$c8-lS^<?MRNJCFvceIn|G^QWUS<cg##3mb#GznQTi5i8hm_*G&Q(_V|6P4*V&e!23Hx;MXNkdVY(dwjeXvO4ZfJ`vsG6Q5PFa@CiWSSD78F113pXNHgrln%IqzAB6SeIG>tW?;aq6MH*nNfrk@K9lY?-l?+#ktiE0I19e5D!SG%qY*=^%H1dDh!w^0H$J8Ed{_-CKN55-_$Jae>Q4=>O*d-dQ8bpbw&xb<|il8QsYydQL?A;sTyydCZo!l@9TXqs>YS3=Ak;nbtqt-Y8X8P%u{C=2L$X>7a(H=TvR7~&x$_n4#=pI;>hcXz9u6}T9c6_t;xue)<9%QYap_uH4j<R8iOop%{P{`<{L{|^Nk~|ai#seN_N_^lAX4!WT!1F*=evA0vz5@X>fQ$qu;=x&8p-#a&QBa-^jsDgSLL8WQXP?lA4`WIf)6N2~5pP08QA>vZHFA_Piu%M<qKnzLeDLtcous#XW6ZaZg)V+|w2o_q2t@J#Are&&0UL-6`(bC;Ayza^vOXOlk_+opdLSK~%cm=b-)hNAfz3gd&=t*Y86Sot@)86jA9Dzz&^}6VQ&6au>kP4tom^06R26?*I@36Z8%MF>FdMIiCT<?2bQ62M|L;KRbXJE37nt6RLdzI-zrN0y=SG7XvuiVcFOL;AD3!l@35EG&}OR4<Fruk7|_L^oLhfNslS9q_blmP?Fr)u}`}XB^~~;4(^Zoj0^+KBi%W)k~q?>Lo1CV9Ud(efFqst$C09$?%39o%9#%P&PY{EcUtiRII$)u15%+AlmVP{r=c)_6RJ&4POQl%=O}dYH$W<#btG<pRJzmbra`4USt}a=l@3pTxBH-SOg$w5cSTNGrpA%O@YB&a0@DY<UC{ymz5{nfhhsmhG2}4JXElZ#jv;J-AqV{1h1>zr=gxpb4%V%a0eR5Zk6i80_mAA|z}UtFSmS_)P~<k}aIC+{)y@G=y9jt3Mh-)O8i#WtMY!W|@*V>4fFDN!9*1*6LcoK5&H#9vvkoc%bDU1YkcN)aYNwIZaXP6!8aqxW(??^+x#U*)`UnzFV8~~>k0&SW(IFKoPXj~=rko3UbO_4808xT6G?y|1lwm)6N4-T>o@T%@=b{Q9(uL$?dIpqZWqJmbV?}KSm~$?wha+XVPUd6)Ku+dl06<RWWPm*9j57UC=asSC51{<m2~9TYSkeY_+IL{Vw>?MLO6pp0`X6w$q2YhP)rKbM0m~X^>NBydNz{^-c-GJuKw?@0gBKGrB*x;T#|Q@)lJ+4s<s0fBf)Bo-4kDJ;x1kmyPdhNvv$O*@Jxe>V)3dY#J3UJ~u+y`&13NuSJFwGpv;zi6Q|W`4^rnXgMEX)HpoQdwIt8?lW`sHg*pQq^rGOjKj6|gX8R+vPTi@gaK}XC$pL`?CK%aag%#c{WJF@IGJbN4S>`m|}6PflVX8eN8cwy=;a^p=-={+*%O-`J6#1jeD$RmGV`s9fa1%2{NkRr_pXp7haMN?k11GdNu&ljk62arIu4*&@ne(4VY2QVD#0Bm4MYb3Cw10t}r10b-p10Jxn101ll0~~O)BLJ|pgZ<yq4)%XbJJ|m%?O?~Zw1W-b(hl}}OFP)^E$v{px3q&z-qAk3SvzTRY~qmz<w>!LM;Vms<G8a|<vJ)oPEEYjVjgXfHiFb%rT0O4ZI0UO=zSP{T8!H3K*uo9Ico;bLHb>MBCV7?w^90Wdg4`kT)a!u6R*RMD|}XZ;&r5P#XnC^ylRhY{#|-v{O7{uc=j9@{qy+5tM<6+m&PYvhaZ>ytoX$1NaMPH9-nyC9vA-O_{7(}q;2EEe;l8fFVY{`wDaR+##iZaO&jTnuhQcpo|vBa-eSMr=N%`tQ1gzHTBv!)NiEd8<D?d9+_6#%HSSocg_>oO)4-_dWm2$Q(T|`h#|mW(Fef=ZlmX@>r?oL)m{oy~8=#wHv{wdjlVI&-0&qif7!!b-RXL0a5Dv^?OaN(;;inf64a{LofM}eo#0Y7eti*_EoUFtMY9?kSc3p?6!6r|1G`W<aYVL7D8a4MgA&r`QGR&;l?}HDO?)SlmN+0*ZCp$H#$9)RQj=fhvH*|VVKsWTcPe3;?G4up*li_*h0iY#2O`r!r7#gj40EEeoby$Ef)&!k^Q?lbx7Jy1NJjw!4$xfH-39yAmG@bxkvSG9qVGGsn09)vs^!p@Im~lQp4NF;~hNUb~!%~){VJS<{u#_cdSjv(tEM*NAj&#5kmbAtSOIl-vC9SE#lGYqyNo$O-q%}oY(wZAAX^jn*w8jQQIsyetT62OWtueup)|6m<R3#+TWpyWYS=~upR(DdJwm?k@b$)S3y-yO=Dh{dl!NQwCNfy;A3espnwKHG~IwcvvMP+x}8Nfw_#$E}~MTN&W3E)MA$4?pX1=TJ9FzS+<mg_TU5_!p9{NaB^|2hpK&Ijl^lI9ZnZWRC~mDPI`046Y}m0Y`2*oQ%`UFy7RmoNVjUze8bPGw13Vwk2`r#Xgc8g`mvn5Jo`IfiMPcBu4rA7$Di!?f)_<TUV^yb4RiX~tLbI*<mQ=CpwZzysqgNd*ebw<HB9%`uM-cxP2~AgMrU(3Fi-piu1$xTrZsbph|J`du<0BN*wJ0SdJV7KsrO!9+q*iqaOAqO^sjDBoSOpC+N*=^NI-vpa3W8hCct+1u{}&+arNYv9?Peq;?i^r_GLAVZ(}ypJ+4-SGtMV#W0Z?7{-OE(wMKywK-90KLGNK~i8sV+K2b5*jnu0hGX)!48;&#tiO&NodmD4p;*w-R*!iXwn_I5268d<U(j?o?zrc$dcBGVMqti(3e$>^kr2eeOc8=Usg5JmsO4QWmO}6S=C5iS2fbtRgLs@RU>^})kt4gHPY8rjr4U@BYj=fNMBbq($`gu^mSDueO=W^UspBK*Hw-5byXvMS=Gp~&h1n)gp-D+8Nx}!(+uIH;c14j((p7y98N)mrU)xUO=E<Wp%!oi%&8(hy9ac>AQd831{SFou_FBfuAotbq+Z0DAaY4UCy2D^(h1rCXjtK90cpUj#to2$lUWy`2Fz330BSf<gb`~TtbAnytZ_KLwi-69G&+qFRvMk=2`i0G1BI1Fr-{Oeg40039{MURfnrTQ)K0(y2DK6HfPr9yJ7^#n;SQ=z{LX0D7;!jT6*fkk(5#@gfI_UGwtzxT!^S9pkP}+Z5MQ%%k@XDmKRcQA4DmlRqU$19F{0}tRxzUMB33#7lhkM2kF2|ts%FC`1P8r=dl(w@1}<XYV;6E21Ea<YX}r0l$lVVg06jO!viQ|*Y0n=2I!0iJw!yXvaz}&H^~fzvf(DS}ng-6wB{nf~I-|>JCthb8%fi@+*O{dqc%50=frpu;9hjI|+JTFip&i<oS=xb(nWY`rm|5C^jhXXX20Q=Lq`0OpY%~%)O+zE@sa6_Yzy?#&=mJK7(N@3|{&DsZ@PlW;XchJ4dO>{=8ca#*ix9zz>Wdh`it39P!HVjO7{Q9_iy*<tii;q@3R#ON!3tT6Fu@90i#TCM$XW;tiT$C2d`}bVea?gzlGXg22|gtF*G>lfkRS5HuFps`KjcU6RYUxcts5rI4^N+;@I$t)u{1zDeSTuep4qJvvRY@(k~@l&c{n*c%9g?Zf=U45>A#>7kjO?PL&Oo!{sA4`nZO0sk?#kLvh2vv13x+GT*czZKAlbrGEmRYFI7X3$m|v@5t7L88Y~fZK<Rc@?Qd34o||shwtY~ZlWy0xJ}A#gw`<!mC{IeaYuh<U@6V-Q*fMQ{bbl`W@_M8+NFUD=<zA)pAbma#lzUY!gYw&~I#|!wQXRF^)5(6Vxoc@$i|@kfXgyy`<7#}DL^ml5?REHZ$-axH<5_60BaKV=U05BT#BmM33#)@gku8sF_+3^VEnLjw8h)2UM~e&dxQ5>a&)qm+e3c#-@w?o)JI(bki#U&q_+9Ya9qpHoasJ4LnxAXG>>+tv#P6c#uwPgnSLpogIc*RYz=#n&7r+QRFx@X3yQC2+o$uoal}`6@gi3GsaU?A&`rPhg3pp{o3QK5l&I_*tX@*I#Dt7}6lb(BZMF<0v7zx3w3OpkiLtd-{VT<!-9SCA*C>@~~7zjrw1_r_rih+S}gkos08le~~Y%ZV}D{L;H7%OZppqPnabM?=<lvSdPk@*&&jFI^kkPM93YWG2ghDh!AL552A`yfM8qxyY7$xHUK>mx{%p%ZricyU6*B6wLfbtj-4Bl9bw94js>pcfixbpU=@^Rrx^L6c2p$1?{2o6L@94gfZJk-hu@2q?27q5}|6W=BK^0H6%ZpgI5`s=WgMqS_4rP@V@s$DiecXaFkY6IlrW6{AfiAfVz<n<SuOG|2=6RE%zffPjk8ix3b{VV{NlKG+n)0XG7hVp!ltV1uHhuF{%UENRUvmbAtdOIp*4C9NUEkq#illGYGnNo%&Sq%~Vu(wZ$SX^j?^v?dEnT7!intx=&at3j#DYEWnfSGkW0R65^B1t&QyKm{rdZgZ+*yrWrRdiGyNmpoqf7P<2A=1|iGOnoGGKGm^`3h-h<?jyPI@q!=8g^x9f0g}{pWh-@E*-Bkkwo(_Ct<;5OD|KPnN?lmCQm2%yr0mqKv}JWG?RkBE05FYR)Po}0w&<R|-sc<^a`$Qh6>v^79IgV+p--Lfa}Is#3?OFJ@0|hOG*;Q40o^oM*q;I3u&k@|@-k_>q0e0ayG;7Yi+%=8HI4al6#zAjRk0KRHLG&%3ZNgDYgYjMz|6S<;K#~^3*cvBF5IcBMgmf5%ov`4k|VA0$4Rpb_=m=z?e_s_U$PRfk0412Cb5C47#KPRu7qeV7`PJJ7hQydyCaxPwgXIZ(!(PBG19{#{Gkb7JHVeEy6cn6Bl_Ir_Go8yCgk>LXXh#8_Q*-}i?C*AXEo&dh-NdA`=d2qoPsWzc6Js;E}Hg*H7xtW8kT*X4J@i*=?`sHip~a-#M7Z;2srZT6AW7dqWSg^-}~%~59r|~(R9NJCP11#!3ZWm8#piJKCyIm_E-S1bi>{xB9=bE-6TR6H0f7qO)e<F>ng3m#gf+CVo7Umaijxov7|M&Skf9>ENM+Gmb8WuOIpK-C9PS+lGZ5VNNcz_3~SVYAr8ZuGhm3r@XQR@;V>LC19&*>tNtoS*L-mpH~p2kwOBK#G2<{CM<dQS48zfgGZy^vq%_9+=}D!GH;Ecaj_0PW5t2CRWD%1bvkQC*Dvfb|`+_QEtVs+w=2%xMb1W>CITn`691BZjj)kQ%$DC4`>XgcyvyN0i5zXn8=SUhlo$?$BL+1qZ%m9i`^5^kISp$y~KBWogbbNd?;hYm3V<XZz*@;8}pmRDlL;=M-of=XK1E(efe1WSp1AIB56>0|favC145t~qLLL(>e$mxhhPJ^gALKFJCZU9YA!y+jl6BzTj0WhI4j~f7!liAyDz)@~VkY8jrx4}P_0dYKxeXE2$Ud9N&#g#Bea{Pt^+qoHeevz*nnwhJ#c9wJek|QrUC&n){lXGJHLOZ$5@Fa@-<fyrEBSvv3E$pftSjAb|fjOL`9ht*f+JQTqr5)JAS=xa=oTVN3!&%yaKb)l<_`_M+fj^w19c=r_>0{Qreu6o;pxqd2gMMSI4Q^GeM6PI`hjCWmA_eC_5#xIpB$iQ+jg?>(ZuE(5^yFv(&PqaUHgHxF>a&6CC!zBN{N$PJ^@)`vXR_BPSlgS)W}jeDGHH*&;-q#1PYbEuz)y}geEQ^Q$4_L(-_VXfDR+;Z0A#ChM6*Dikf|FnL1w25ppX+!O$JDiCq&XlYyhW*bm_A2tH#J+MigO42$|K;B0|W_t&rS4BxnUqt{)ywd|{lB*`XK0gbd9KNw4kW*&)rebaoIfK(BAoP77x~Gg^2y^BGlrvYF4!Mjj>ZUA4biPi1oAUfBlaNr`(U4a$=e_evg=XC>~HGDy!#+$(jEo|U*)+8{kEaj)!y^f@yEuIkbIF#5YxK5lsRI?^$YlxEH0xO!8b6I)ov<@+w8562ePaRI-}-<uTw_d5Kz%HM_Z@%X>jk;X;;E~1Z5;<)M`XY^fOt2(aw#~FQ>L%}+(`o|f4mt)d8F6nm}eK(3jU!})2JT0QHeq;xp717tmMLaE{uZ@d%enel|bOEQv7bl}n<4ZD%DK)+%!|P1rOJW5#^*+6@li!PVlBO3bo$u32a?G+cy{w6UyFP+O7&>zVTB!C0pk>wEZGdh_blz22vyBs-cO6M%Omd3g0&q#p&ujzS;-vBg+~TD21>EAK@&(*trSb*fVx{s0;9{ln1>j<(@&(}X-KFwrcyUtsG`u*ed>UTpIo*DrUZ`}xk1wl2t@?e;fpLcYKIK@^d75%)=HLP7WmR(C0VoG1=N$lYGQ6Qa0ld)Uyc6Kds^q*AfQ^+p7=R7c?tpAo&0Plwlnpny0D-dM1{WYuHXPdm0?LM?SpYy*DqjFVRw`crK;K;|p9UZ&l}`hZ6P>34s5odP`KLIY3z~n5(YK(nrZ`;-nrjN%oZEe@DNcb`fHei~FBRZQaZ2g}UMXzfr~p^!J5m9z6jnfA0fku78bT~-%^;SvMhi<?qlG1{(ZZ6}Xkkffv~Z*YvaqBzSUA!e73#7&mAb4>#Y*MVtYD?`X;!dO`7|t4r`bfqLY-Yrl1VL#mz+n+R=g?Hcmb31NS#VuSEo|pK}!a7QJvO~059tN8kh_aq*^sF84!s#i5f{Nqt*<N1ZD|lfFv+WFasokS%T!cr!K5hsSE2=>VJYdmA0%-r7f#dY0K(VtUx?XFIH-urWYy==w(t4SJICl5vGBHhyx)@Gj^H-0SwI*Bm@I9{RqLV`Snj!k=sx`3@Ns4Ry_<Uwxt<^q}Ueb`;lT>nD0l5ZDF<^DYk{#dZcEhEv#8-3u{)|!kU$dnSj};S)mbl;Lc{BZ;lP_b#}`e8(i~vGbrI_cW%8T`_R}caLqIQXD{R`Xt!*!$;FU2g&KTz*tfa^@L82gwgW<fsbo6<9~u|h0s2sFQpZ9+BL{#Tnx;nTQ&t6?l0p_Mi7wzGD~T=uqlrm$U%mieA8Z5_905=5<i_V(rJ`}llGZfkNNYZN8q(KgNS_8LE2K|T(Ug!r%|lj{p5~z`QF<DT=+lGlr9Q*PMAJ_<j79?7=}t6LfIHnu77B2uGh-TZ&chzNq4OIUyhsjkXz(Jrh3YfB`~#Yy&tCw|^cgV?0j+d)!e0QabZ9JJ0IaZS@2EPa&&VSQ@S_{CApw3&i5t}%axANtIUMs>O&f>f{i-SBaI9Z7WgL$4tEP)%{@Dn)mGUCPz}=HKgPKDQ!#g*?ki)UJ4KU<z+-(C6ISg~#07DMP#5LfMW4>V!L6yTY3?jhdO`-;t!!aKYK;>|}hXYbMSTzm-m4j8|6u>Dku8>?d9SbXF=0x)yPQlD+oeD^RIjuk0CBRVWbRS@-^mZR$PWX4}b{}A1*x_~`PEPn&9l#MbA3MSknEpm^1SWZrLlHLF2ci+GT>y@pupp=a9HGxm`h)0mlLn#FFo_D_f~K;O4xw|AX%J~8I$04AX(c*Y5fC{naq>?C2sv315Mhw>KS{w0&4>f{HZ)`nRI^w~Wr4}u2LFWEfz2HCO5K6a9P~=vfzKSZ`P_lg9JKk|iGdvS`P_+t+-BMN1P*dk{2<nFG(zwo?r_lm^dNq48$3rN^(G0rtCD(?L~Tk>;t99G+rpE$!ol6)B(`w$=RAoo9Nc?O;tNL?&`FHp;LdguV>r6~oM5w0b1FkBvYJgZ@_7RuxMAn{`#=2dSAY8DAHPaQ_|eZlLght|ubCk^2}A)iq!|fB0X!rpCMbZ1G$SS`qKFkQKqjb>j7*z|G}4Srn}|5(&tO5<HZV`Epo5afQ&<R|BqN+A!V?-bNh(NiNG3Tnc{ueMor<Kykd_>aJbrh`0m+i(M~+e046?hNWV+pc_0RqCi>U8%0`$pF_p=6^?6f~?u3-**ofM{GZP2EiGA!yMhWhlm!L18^ZgTB{AABSHL7yC%<!8s!Jm8M(n3@Mj0YeOt@jZ0TM#lFU{?(1F@1Zd_^1g=-)5!du8bKrbd+5Tv5q_XH%!zPAcC3dYCdf|ma|8v{LHbqvn-x?iCknPYC{IchY;91kPh*lUH!*D=q}$U3u&Z<*r1ymhde_m9Ve~#HMD04zISh16n!$Y=q|e7mlCR2XP=1#$h>dagJZh(<(TT6aj|====pe6zd>v_A@Xs>{uiE31PxWzh;;Zzy<WqZ|`uD0muKBcb(O-uj7k%opq7z?78drTfCQV`=m;K`q!pm#b$94ZWgz)mQ>f^G17eaXBoaI&eBYSp!9G&<oJ+9$*5rl^QTGnmKeO&DCvI=o8vBVuGfl%X)lR&6($4Ma6wBsZYYS^(72sO#j9JO+vT~<ZimHUii<tqk|V+AY*kYlAA1_YBFr?7xolHn8<AWJfw!UAMj^P*m#L8A@HWV|YCYH>0duOn${NzNf=KrP8|a|@^?8E$R?wO9#+0k&8PgaNl$34{TTe0K?i8ea0<nw0<Y;ftUC@be%3&%eCS?}`T6eYSC;4>j93(TAFCvT<0T*(N&`wVG|HbidCwR_>r?7Ak!LX30*CSHLW*G7V3_Ht;n41ZZRB@&#;@UoQH;{@UET?Y|DBNrxVNAAn$11ppp^bzlJC0pJD(03LvCvQZWtuuV1!mjkxRj!|B~HdeS`z&2L6V8Awc9owLTnc}cbk#=mFZJbm?%{ES|p=KK=)ljodaRQ??+mz>9#&sMCIy9JZzYjWPQ84umfT%c)Isp(_KT!wNLw}<Vu%{T|v;p-P^K%_YQ%`|aEgeu#S>zDh0reCk<u{<7;<)$**i#%A-++6{BBxyfNM#`)m4$#*76MY42S~dENOdA0RdTWAWI1X;s<4d#5K?vQ+chFp$Gu%6Qg!whfJk(903ubx`#m6^>Uh5g<YUZyMdVZA7DC9UI-l48eXI%E0s7Dh+5!61MSJWH(5E_kRlq)VoeM`r6+6`^;0QR$lGgZRNo)GCq&56l(wcqhvO1jhu)R9#>oW;5%`vIdB-0#|I!!XoF{#re)0TV=ua6*!hXmPOg(c!RId+$UH1IUXCO#mZX4u3Bz_aGJ-%(u;`SEvD)#Lp7J1X*Nj{9JMLd~)A4^XJhu<{R3r%i9vy^gPOs5wyr0pYY6Q33(#teC$7cnF3@7QjPR_+kJ=Z9)t6mn#L7?F1Or2u7ibpxrqX%0@-dzN{i>Use&cFRKXJ*Hr}V>neiw=YP^)#?ged!xEkj2x(tb!b8rEc2>eePK$P@%!V8t?Xb*-+?wsM4vCx=?T(dWfJpoN-Ys%av|GJfJK!X15(7@!4L{5Pk9NZjGa#Rx-68LQe4KF90DSg^*I*OFEb}*EmR7}3pI8lzDu!Tq8(<%p9R}E^vmP?QJ}f!#+MXuar#rstntkX~gAT6lxY!4{(^*SV0Tk06kD~x%`g4rA4x}-rJ7!7&#=s?%0maZ)h8*<3SB9MLz|1{zbi>}p9W`cA?F}$VhsS{%fD*VnYye8SV~G_|30yZDfD*cHw)=E(Ec3-Vmigkqq&Uzh&hi*9Sz($VtQa!Q4+s0h95jj_jv<rAhXek#Od7!HW0MB(gZ-gL@PWR4<fe$ee&lWlrr?pQA((<k`ns)n&wv<cuImPn;c%P)17tW1Bfx+dXmltchQsg}42a=yECvH&I1GoufEef(5D>%pu%x9LB`xQpTgXPB;+%d7*$8=9$&#8po=zShkQI{$Fy&;uZGckF8A%HPt(;EMLO?52o0PSju!5D~3VrSk;0k^24e$zzF}zq82fSkCp$5Ei!ZHQoJ#$)4E1FlHe%dksmlfZ(4B+Op++;M}oD0iS&I#oyr&W(~E~`he;uiydJtuxKFxYd9WdnyjD}FKX*t6mn1CzZ4rnR6!DS4)~pkK+G#K>^ZNo<S^_pHRm$Z^j~Y>X`Tti;C1bZ=YKqfbn0tk}rNcJKc$?%Z`Y$*n8;LK774WM~Kt%aH{ua9}79;J^lifpekX-7~thRK@<zsl`ps#D(6)=J&H|)#2gZ7d(GBi1VHlV(6LeU58Gd58}!Py>kb#<+~uAle5`aoE*-^;-oDFi<7>TaBVcOdEJ;|lges#WU)_a+YA%f7Zz~|mQ0gvgb9mn^q`9*NY2bQrmPMBaSsPjf)Z@y0SYxhB^@OJI-n*3C_y-z;PFXN%4QCpNb#W_c5KNH_4q@H@AU9vOMIt?AuxNA)Ln4)Bq_My>`8LgM@!B0@B(H|BIDmJd8Hm@1X412XgjnJ7il3Wv=DbBO*_~Sl@=Ns8{&?fQ3o5M(x+o%L)?+`>R>|@nt?oOpr*W;Py=+t&4e1Ln`|c75Xm#*sqJ8cr0r0Hr0u|hr0u|hr0p<*qU|w)r0pPrr0o!br0oELr0oELr0sBlr2TE}l+D46txw9Ef*ISGlt1J)`5!kAhV0iQUDl;<VBNzcUDp!}@6vISZbvg8?{`nr-TSW0$NP=)bfd9r2FoP<F`4lT>nrVbmJaKAg?H_F^@g~dS9q76m+yMa;!}HGz+pLB_0iZo<`t~uEZ()}C44w%@qYVxneWS4yx(bF(n`+aU3*@|LeAn{dS1ms&f;BqUd2Mr;$8YXui*8Z#k=&ph(F~lzA>}By@kiTh(E<Au4g#*ujUwRdQr9vY<f|u`8K^MIg2*DC^?HZyU=L7{GMH;2uB-CHpSNkdk7}7ko3BzunjCqdfoF*Hor(om=3>4Ig}2-ocj3*=&;{E0?g5V{|KN*%JX!H2IgW$fG|Ngk?ar*+aYNPVWh26hhdbRQioxbjZ%kUq|8N!VZu2p<3d2@VCJIDIZEcD%{fZuqRlx`Ne{9?Co0{JHt0m9*U<(YDm~r<OoTO;0T3o0>Y*F}Zs7ja0BoaVE;?u<<suHiFLWns0D?J{i#Pz=z+A)u&<5rr4uCc=7jXczi9+A1LpD)qTXo1r%3O5NM#@}t*hb1+blB#X%UrbCMu|SO;e`fe0eVqV6>WM+N@kEvFG^se4KFlFue^tsB%F$}*(I?TZ~^F&;CrzEBuQ+uw*VxOq-`XTq-_XMq#Xv4q;0g2q;0g2q;0g2q;0g2q;0g2q;0a0q;0T}q;0N{q;0HFq-{{h$9hrnv0juc^gr61kc9?C8xyk9o@jGI-oHVf-=jp9_Q&&kve0JGMvKfoNi!getoZ9WXpt3zJ%=sw{!`)!@JE(TiId(HX%ZbC$x3g8%_CVk)ZqY0-rw6snpLvY+(tHjv`MrfCZB6w$>*9^^1<enyrp?1M5TMB9P3^w$GTUFa!k|)o}yTT+r+aehA!DdFv*Cd&^6M2tAx-s(tcYM*K-GYir{+gK+l;7!j9T>$&cSrlZ*1}cht&K6!&<Cdst3eN8D4CpachePW^2WK%#S(0sRyu8pGk8!uoSEz@5VSTr$8N7*?18?v#D|HSMd?6r%(Q+Qd_Ttu~i>tj(n!YjdgR+Fa_nHkW#+siVCoBACF~-XoBb!RHWAJ=6`+04l*0wFU@?226IqKvKeF2M9zXCObf&QxTILpc0I_>wuK1U{&V;P=y=n9RN^0<R#YuD8VQ{(l%2Mw$0RoZ8P;?+swuY!mhN<v_->~W@ZlBnAD&RJ}4Zu9T@^PFg3-*-v*|(!^GbPCpvmiB5FH)x@|IQtjUYihT0ChF^7Db;5O!vPupQO<`7VWX02rRi)v>8J#B}<k^?o3y*@L5nzqB<%AuP^KE^Yu?nu%$vq;i5vq;i5vPjZ4u}IQ3uqe_tg7hPvaW;Z<h<52cg7h6}GB$#Al2-Bi-+uY>JAcDE6HtMHl7LV84g*A+Q%=lYBFD9102?{4-C@a%^!4-|Mt=^*D5;+gy>!Lr&!LyTzjcTJPM2DT2<AwW=x|Pl#XHh)+?C`K2XML)y5SH`7cw^-!hxxq6%bBmFidJP{a{U|i#3_QyefWHd1t(DQ_*SyW3;O$CKU~(Rmg;*vBMhQhN5xcwO&cX^AOshY$zH#ocV1iIx%~VG&>Ke<;$j`A@zLOR7AA{pdqS#0UR2z&*}m=G+1ZE1yE<O&WH=Jjg-CUu+7*Fh|k;G_%j4ReBQ~1A#D<E7?J`k9U77XEFBz@!W|tR8V7A_#$g^pO+8W?qvOIyQ^+dt;X9QRR)J&RCGfao*+;D(L66U&smr9v2mk*%aP6bo#PtS--(_THbL^KP#y46(o#*N&1=M+VeNsT3=h!C&)OjX-8w2X9{dMeF`dw^4f)tB1ZO7D4(soS!ByGpkPttZ={UmM2)=$!QZ2c5%2T8)Y4Js|R%|Q*S9RO<t_(}_aHR!l6zz}rY7hnh&V0RIO2(abxA_xJ4>n=hDH2#g$P1wK#s++)p2UIy>1HVw|1P=T{wG$W>cs;)Rop(JQc_1(Qz*^k{dD+vy6;cgh1CI}F=WS0{XCSY87|s~T>z+Oj19;!ZGuu5j2t;AO$Ke2GIao>a$ztMQC2c5p{Gd;EdHkSJ7LPv=FkpVIPjLqf=*STn(2*lDh-?E8kwIif*AW;*c(ykXGKlbSZy;n4Sr!Qbg9rl&5Ew+5NI|wq@W?Mh29aecT!akh-^xYE0Hqr~wH-1LwCnY40oA?9iS>$;@}A_xdZkHuQ*vUx@+7?}Ik8@4lCJC0;U--t>9#I?|NCf@bYD*^yi4~<dK}Gryx)CHcNek}Z_?qKrG>1-yY{?ZKV>CuY6ZRDeqPieEk`xprRP=sDNd1o<JT}R>rZitn;aeQx1X2(r^Lk<-|2VhdFg*jQ+)9yeV3k>{-^lF7vH*f>3Qidrzhrz^t`S=r6<1G^}Ic2<Gipx#V5YezP%pecV5JCUHkS{i}R}86`)w-ylnReC^{Z=4#fxwiVnpDq0Zo7Ob|){4#ouG>)gSZAbguU7!!mqa|dIB@Lld;OxXQusR(1jdQrf`m>{%pdKj~P)*8Z?uwL%)FeV5enI6V$pS6xKCJ2Qbk7KBI1RxUxV?K{$f?!<dp-ebr%$EW3gmr^Ek9fkm!JP*@Vcp=)<DH#hi$8qCpF;3Qh(C1jCkmab4*pQ-_8xyC+(>Kh@h2W?w{7n+2}V-3_mmXZE$19aim)Qm00G5Ao?{K5Qe3yx^GGSe?t~67hz28ez(J>i5j)@|7>w8f3&nMpIS+**Eax_WLR7l~6rw4s6`;_ml+_AQD6XGq_E0FUpP=wiNC{{3SSbEdE^`h53E_+m04d>&4ge*E+D!gY!WkX@NfHp6Tti1)--AsOmX{4SNjRV6feroJBfye`BO)HL&~aBlEa}k6pbE$)DNj^~SklI?OZ$oH@J(7jd*JbnByHo3ByH1;ByGcuBJD7XByBT`ByBT`ByA&$B5gxRUTm=q_QscqCs{bg<KRgaPVqQ=l7&M&4xeP<43EPn+cVsrcQ+9x3kQfChRMSDA&+4WOd8q3%In9MJj%(!=_QYHw$EBZTUdGh?3Bkh85#%%fGkuy0%oDw2|!C0Ocgz9$s0@+J$(7+d;I2K{^JW7zJo7$hiz1{M_^M944ovKRC(Rg*`u7i#abo(u%|tz>>;B<$fzhSK_(a#sU^q+qaw8gnP5~l913y(sgUQuQ`v+cm;@T%vriH1)jam0QIi3H4UC!$0BnlXiD83{62ItC3;QXbb7Esl5l$I-*izOH8F|!Fgfm7SwG`oqkw+~>IAP?`3j6aOs6Uu$lm1|;P5OiBd?$b+D2MSOZDWO$!<dClp{nfMm~0{BFgj=f;{?H$kQ7{3-s1($tt;>O0wyAs_k1Bt&htJtY*g6FQ2=bfM8yJNqYB399&AW|m}En!3J&cadB8u-3cy49+pGXX=-*}q7*b(-R09}7$K3#i2q~o=g(xYd9)(ct0VsqnqX8(S5(;@p+Z59F#0wPyAWi9aF#)8(ZHD}wK$^5yWg<x1kcs5bM<d0Jr?LqjZ9VMBfseK!?8xH|G%pWn2RmTqT>{wAl+8^CJ9Z>Jdc*<$8Y2J>Aw<#xj>f)j$o@=&y{F{(P-CA?5fDa$ue=Bdqp=R<2neGoUKS2vG{L^jBaF80-sS;D6U^Hj!stq!L+LK*dradp*<I<1A&to&EZQj%{-DxeQ>AYR-gN+^vsXCSU4cPe5pV~RE{_MN%^iJ1(6k32XwD1bj}9Za1K^InUNR_X!==NV7qa2f+1C@<aDh)RvflzzJp-T+n2H$ygml40)}xTlN@D~<y5QRDK}d%cs|YBBjyt}mkk!DzA~bP~#V0Y~jlmwofH#KHfnwsuj<iDuI|l3J$nR-Gh%t0%V@HgkhaG5M9?}kWC<%ogZj2+xW}aiPxdf*6C4ePkgJZKtBydF}03<MUFaaQ0eS(tyRrm-c?kY<BoQEdk+)=B7np_9jn<%JzRg$(bMv}HEMv-=m;;yZ=6tHEZ<O_O6a@Vo0k()I9;ESY*Bv7MS&^Q8v@FF=`jJ1Jj3Z4^kxEK$-6X!TO@=mPdpf4#gM4?fZ#1I8XCK9I;`gkE$Cpf=!5Z|{87S0DTenSarPi@EeP11IZ-xO`n&`r{I9Ni>s$I?yGc0An_ZRfoob|vo+A_z)@h)o1R>JYIZAS`a3gTlt`9xt}eL1lx6<$==1;>;ve+h9|ZP;rCi@nr%8FfuO_Ab_cMnE(OJhRXy9U^ZMPK){{>0aYw;@Ej>s+@HpNA0Tpqm9!loP_#WDkhC2jkhC2jkhC2jkhH(8p0+u0C)P=MQ{ql+lk%>_o!BSoU5Pt!Owzj&chWUUxAj<@yL6bO`_WjO``zPo_pzLcb5~B2^2fj(x)q%AtR0S~;@odPFX<4MQ*rLn^P2t`xI=fM)4ZxbCGKoW#kt>pUiqIwdGJPfnwS2k#2vg5p69jyDRO7iwB2t%KOdH3c^)mJd0za>u{@7wah_NIr&yjBMZ3H7y!bz*^3X1`{GE68u27yluk3B1Jb7N(2SRzO?fPMZjuOgagH8}y2yD=SxghyH=LG0Zklu3+m5%Q@Cn%l@Hs=JzQo)9p12HKCbb?^$;BZb*3>_SZ**<Fnflg5TBplEQil2l-F$bpY0-zJt^Kw1TfzdA)U>F$vash^c(JvQZm;k#`0)QB*O(=$H6N(8+hmJ!r;Y_q(Arzxz>(~?%g{}>oVxrRTU}H>F+8u0+ITi8H-s6rEfMe56RL<nvv_rFXIzX9I**YCC56sr-0C{M(&Hy|^vvmgGnN!(118@(^6?y(HHq=n<2B_xL+%<qdQ852-@CW7+HGn@b|E2-@f%!KLz)w_?E*$ugvUMEz`Q@^8Yye6dJ7x>vqqNI47Lbz?BxHk=lJ;YBQxZ7R#-XJ2<k~!x1Uot#hmv9w=ipEheBvC+Ns51)gE>j?Z*wRoDgJE^<s`*c&7qeBJ6H;!7pk2By(GocE(1iNlb->jB*rKiFiP6tckjST68!ERSV8GDPidP~BxxH}6lohi@(~9Tn>(`7pkvZSRvbudyvRGOzHH9Og437H8CkJUu{ncEgI%VqIQ}@GaUcMOY%^te;3EPU$vX^f94g6zqm2V4D3Rnh|NftT9?A3mHn?QLL(SoqEcl!`*pd~WGlx|2{@yRrGn3Et%;a-DGx=Q4Og`8%lMnXHh?zM*ul0XQ%;`$&Oxbm22w;yAm}6s)6qsXUj}(|=<Ia}A9GiQTz#JQUl)xODdSLKO1kfXe!#G3(LskgT(C`cbGE(S=Lo!n6heIiJ+!<gB9XBbjlp~u%165uM>*yhcm%=)FNa3aIFkf<@r3mIr4zv{3kVFbEg*7A*WGTO#g^kH8QW8(JcU4SisgMWjdupN5?LD<n>HeNtsPuSGD;3&TjQ6+#1C_>mT&b}BLz-iR{FH<`U@ELMkro)3IMo5XRM;y<I$)~eOGMgSD%=AdfMhDGn-2golC;eylC;eylC;eylC+H_lC+H_lC+H_lC+H_inI+H?TDF*%@_^(X@km0+u?6(vqlsAZEe(mAw>B-X-G*yHfd~03bK(yNeXg^qcPL_1Q>(<m6HldQyl3X$Y_dDyaO4Hl|;$e=f(<j0Z>Il*wxTJ4%JS8D;kW;P5>+#c_TfgZLpA}ZLpA}ZLpA}ZLpA}ZLm<JZLsKj-0e}LN#EgiW&=hS%+74C=-c<fGl35!Cdh`5zQbwFhLA4!tl8|*4|FGF04Ol<Cj&s~5)|5i(v>(s2T=NsI6wzfx)2BGfXaz=PMT7boF@lnw&XlHP^08LIZV@~Q@u9S^c}GQ4&8JiHo&2qE*(m?@uqKR6B%EXU7xNv@0%1feuci1ajfrTOH7VUK}t-H4LCz-nz0FIOInIeI7(QGO*k+<h*VbwYi%Lb6_#W2*wlC6Wx%$X4B%xbu0;;C-11lc?O&0y%`AhpIV6B1G^B~}$bbb9!Xb3r0e}b{cK{#)L!*e}3LExQ+XfJr=oA2d3|LIP09g!JOuc{`98JFfJ2YXtBV#6qhNWm9$2E?oV}NtR`)4hY!^JpNqylfb>qsBpa}2f#9kiva#9{7Inv*<_xigdZ9E4*=cPX|Fp4Hr?_%?W6bJxD6ylfmND8!=<<(p)5+F8=}9Oxu%$AV7Mc0A}LZO4R8(soSfByGopPSSQv=p=2&gig_RxFslkvqjh!lA>xHWKoh{9AXJd4uOLsLFp(2r4g8K5=n6cPY^ktqs<UGtb?bBG^5b8AhOpJ0<=RR^%7<N1FD~B5j-9*z(l1)ctMz=3pK0Y>?YE!0{@IIbWlf|BXV3v%eV4yg3b}*2`XL*P|#_)i+@{P-3b?Z^IdqGlyXhdLR`UZ)Fn*Pd0qPUAz9)iUDl;<=Nn3zq?aQ`p3-@eUP>5YU*Pv4lxYZkIi~8aTqotR8q4(Xkt}VJUe6eMYWG<?oc>XsW0;rsa?sGj-LuZiJEZ00r@QpLyg%g(y?Eo_rRU}SDMRSZv-GY#ukWy&ANF`o*Li_|$`E>^eS1*XdF6fz2*Or^bzZxl5`xxh#?`+4yuO!HgdVPabza`fDMAmg%le&{a$L?nx=FWr)qV;QdQoJ)OV6uzV}{W8>zLK9W7>2R_B81}+EZ-o2|JGH*!UBKBRV$ygze3H&)b`X6yR26dQV7UM}wM8KtbqFvkB<L&yoNo!DOxkASvwVEpi|z2+c(f1nvK2p7*y&DJXtM4l0EmhDHuD1;NqCA*K^QO$1a0bA=*+s<5LG*&(MOG$K3XbmDOq0bWV*Mh;&|@kS0{g$<p=p*XF?CQvEiMm9Dn;YKzsMZr1VrllyjyW1cXm2#pDLR7lF2Oug9YCtp`rvth<74Xsl2El-r4(Nv_NezHMG)ig!v^f<eH2?y^aGU|i2ZrMeKt2%`H3y)Yc&Mm30RF)6p8=?c2K01*Jyg2^q>)049Hfy#iyWlc7+NG%ij*858*G#u9~*3x93LBOq#PfcY|`#}@bm5_{3t0xHv32^LN@zspR(uOZ9Gaso!g<Fq~wk|*prmtQ3reI`XGB>33g;vfHQR574S?tl*URn$r59#3b-dhrmBEvlF<0?@Jxa|2Nm#4I@EMf0rw<{O>FK-C-$?ZaB0R%N$FcQ31~GrshM5HHXG#~hBh`NWx>$KhNP_ci`bBqcbLxEB$NfyIh%yC;*DaHP~KsU;^0metWg}?fk9yr(9V{SB!_yGkR%6sXns@z(6c4!%z+;z>davpIyD(UP2OQ$<-koAysI3z$-==Ahi&qXSV)ImvJeaDpi344799dnq-_E@6Jlf&NRc{DO!6p-L8^@&Me#?q(W5B#s5Wwx-F1xT-Aybhf;X#8B}MUtaA>6LK63xOy-h4daGiCCr6?vK4ykOPwdd_^nkkB*u0u0L@qBS8rYL5;4#rSzf-zg7gdB`fqJ$ibQKEz#j43-D%^Zv=f~A>*F-j7WgE3+f(%-8&S?Q*!$GU0iv2L1rted97K85-oYAW2E0qrz(|K?164>gr_Al3I!Q<XD^4%F2BXF@7~n#y`@$fgth8z!4h^pBWqI@LqHHsoYhW&4ceU=|IQ>HutL-ctu)QxEN_bpSq<?WuJDK9%izkzSj6u-B#@?6s)}du{5kv7coVP&?Lk)6ShfZ|6>*H@IEf-ZK!40&4FO2&UeEhGH0c)86AvgZ8EbZ>Toun4#JkzzfwT=cF3&?rrD<R1-{?9U^Ip3A2MF4Vf8d03?kimy<#Z8T3Hq752CH$QE}nqba%N4rkDDlVeIv$%%J3qp{5J2r#2Td-3=l7nBem8yC8;m1xsKX9W|`fYRXyAvlQLSzRH&hlQ?KJlV9+*>`<@PYW#WC!n*{U9nDcXrT+vX$~xO#m>xu1^7b}TIj6EKxm;WHjNG~bj7C8;f1bvCpy5;S@D3JfriOp<mj^!A?5HwS9b0lUg(O^zrzb%G5U9a0mc*ErN6D4;ketq_#yB6M|o0Swb6NQdX-5zFDgGi@LHXe%cAn*o1?W!xh^U{J`7r)l$UL<9_-%6B)#l<^^oq@B)!%2D%*Dt)7?Lr+To9q9%t>aK5KXFd9{8rtJ^ef_uJ1)dfCwK@!itrHT}`hj(!vMc~yUMwA(Uk&)d&S|C8z6i|nMk^t|>zdEUKfjJQkBYd@^IRX$$vV_y589PhBZ$e365Cp$arE;8no{mIWx=!l4RN5uHf3;V+(fJPOLd3k?wzQfY<^8Vy}N2P6oS#_|>0^5XRY!i;LP1w-_W<yR8I>2nm2}<GJhMb_p&)JX@luks4V8Z?eP69bWdGXkcv&B@+0U5<q%>fx^Z}sr9b3kT`6`(^aiWQ(kD|Biyz?HD0kJI6nAoOuM*b;<3PKR2;7HY{7w1jie63#(OI0h|o5n7Vn-C{yZWTl?+9$F$Ss{v|>JG_EzYKekZuuUydIXY!iOWa}BYtu^<%z7PoiORt*hfLxQ=T8SwqTu}LkV$0E96~0Nv<)Vbw9O-uw9O-uw2dQ*v_m11v`rzBv`rzBv<(-Mv<(-Mv<(-Ev<(+&4_p)i7fC_@lP;3<7B%T2DeobhDw48|X=6o_b}>z?NXjOrjT32i!Qy#$8#$nT;RT2z!EWaONP}t<)JQwLVjSj3f>(^g9BI2pdPZPEe;QILNjvO~97IWizmbC|bZSVYB<*m-a$qG1mRJs~ocOCH<&w0)A;13csVbCFeFa*zf%-~TLK|(;$;z=An{+a09)Aj(oRgLFI5y|7F}L@Wla-iBn{wEg`+LTrV;%rt@*ywD0Z4~U+yI;djo${q95U#qvJE#G#%^{%H=BO$WRJln95!<u@J&_%OC7FZqiz6e=%_2e8aC<*U?vORxem-^<t(lPDtX^o++rWVbtokZhO#!LlwE}y(7ICCcQB~a6yfNRjW1<~38RfMMety>Ii_p}{^#vY)+z9r1vZGv4%<+NdWv8h>c9-08L~lCc9_jNTvG(ISqE%R{LPZmPGM&aN!6w(XL%f|Df^Q<$evSy9xkM!Q<S4y4*DFJwgmX7uoGAb@KIstl>i<Usl;XzPuW@{`i}nzsN~c|MhZfSM{%9A8A)-Svl*$v^N)ay>JF!88<MJG^lb7^C9ksI|Mtt5-}x`I#{g_fqRv_c&{0*=fgC)l;Dhw3Y{OAia)%r!Vxw+=iJ;3@1GocSz8b(C$%)Is9m$EyVHwql>n{uWr*&(8_}k1=g%5uRc_e8YXC!GGXC!GGXC!HxX6mu}jpEH_6G%HoAnh1|H05Pv6G&6u7&dt{#rV=jkA~hwV4I1KnQSw)Bl`{!Z8NcnBil@kSq+hGCNk)NwwW6A)*;(W?U1c4*=AxhN4A;h%#m#-HfplX)C8MfhdY`8u?}}M0b(8QXbQwS;L)TlESo&qFSdncbBbaLXLE{T3TJbQVhU$-iew6Bb4uTDbq|Utk_VfOGLi+G4KoMkjBGF|25=6>NCt2Y$n^aI0SUlPM+ExtD0FZ~@;`KN=fJdOKst*5qJuinwvQaGh8A_?L^ZUiBYnbs%dzL^b-3D4)P)XL2Z|(Vn~5Z88;Sa{mfxW?wwRDJ6nruvXDIk&Le5a|$z+@%7~k6bGT=+4yyq7xUElKym2Ln|2KdH&D%)&AN8JINuu*q_9dy*B$})~rLY`x=@r2FX0OT<kc?>`vgOSGo<S`g|3_u=(k;ee!F<?od1E3g6YL7z{<6xO(94xbpePtFWs%QLtk)_M=(iNQOo<P;7d!{}9y<<$ud5eE<yRJ#OZ1L}HSD2JPIBl+a+_fuCxA@?=2|e!Gl_uqmTuS{;m1qwjPXidsW}<iHGAXb7?cQC*+Er)mu&y0%+VhJ3<hQ%(Mc1x*1%EQtg<f>+nwRh=Q{6p%ypQ{bd7*zY-lbl6EzC<jRQ;#9-(z0up)LP3cj<Ythko{_x!-?Y>+2r8kJTRL)&9wYch!rpg?ZI~^5TVFd@X$EH6G7Ch@T^v9|<undoSOm=SRXPBVM7m_iqhWo-3fqORLVk#lEM>OJRqfoDEK4-A~Q|r?CB*Q3zcH!HCD9s<6S%&cUm&ZfECk(}|xY0k{f+i;)LcVS}5V2U%g=P0wSi6F&_Bu)vDagss8`_a2Y2!n%8phgLyw&+*tQY;e!<_$jQr=Xm%O4)Diw1U6g+;c$^hS78HyjBfy9pDpq@E3EHEd7KrLJv0-W;vQ^zmbOf6im-eKa4Bx^b8@&TuG={|NEFw%1|1@b8_v8tL=@N0ygNh`g+u2a?ZgeI&OPdh>!;2=*og-o?#~g}OcaH4?;h{O4d>oH@QLf^-aX!l>*vlr-igBDY>#)Sb_SdiHyr--fG4h>{`5#DuJ<l^AQRVnmpm?sTTZ`uY-9sW!~pY$pY{ItPd_RC*Ps8Y{L>Hde}DSpk3ar2xc~X%kN^Ew2>IK!I9<!%t|jAIHZ+TIts2+bbZvaQ)~9Rz+qE%W3)i=cKR?EvSHnN9217SQ>tZr>v-MAl@gEKI42AfQtIfRH&8x$@8ZYx|Ft0}QYBH~8^J+1#R_iy2&Ae*;Ma5zKLTR3<`1KE8{~tAlM}`')))

MODEL_VERSION = "E18.28-C-770-FULL-SEASON-V1"

SOURCE_HASHES = {'docs/model_specs/codex/e18/tools/run_e18_18_770_capacity_trajectory_gate_0b.py': 'b984f82d07b67b6267168479b54e80f8b404d80798afaa406940b3f53a57c2ba', 'docs/model_specs/codex/e18/tools/e18_19_retrying_trajectory_controller.py': '30b68cf47c8a3f9662b6aab2f480531420cdcc3d1ce4abc96659974d9294befe', 'docs/model_specs/codex/e18/tools/e18_20_wheat_market_netting_controller.py': 'e51b5eacede6a20c5dd288762764188b11f754f32a2aee310d017595fba16e71', 'docs/model_specs/codex/e18/tools/e18_21_wheat_obligation_ledger_controller.py': '9c6c1e903b15f75d40b645d4ca19a477f890db97cdbef3ae2b9778227ff01553', 'docs/model_specs/codex/e18/tools/e18_22_wheat_jit_d1_controller.py': 'bc2353e84aa7d529622667711a3e526fac1482a0065951406c52906e4d626762', 'docs/model_specs/codex/e18/tools/e18_26_jesse_boost_d10_controller.py': 'b1f1e4ba123cacd77a3faf8d7796b957f5f4fe532ce4fa305d958211ec4c0ab2', 'docs/model_specs/codex/e18/tools/e18_27_d10_d15_cashflow_controller.py': 'f3d6f85a7309611463ecba986c9807c3a18e89f73f1e00a3026f2224f1b38cbb', 'docs/model_specs/codex/e18/tools/e18_28_full_season_controller.py': '2fa5c185c9823ee41b639878ccf20c70c34890e9164195981c9fbe199685128f', 'docs/model_specs/codex/e18/artifacts/derived/E18_28_FULL_SEASON_C_PLAN_V1.json': '643970c6a8b4b6636f8352d4479c5550c6c985861104b9cc1e126f4723cdf9b8', 'docs/model_specs/codex/e18/artifacts/derived/E18_27_770_D10_D15_CASHFLOW_PLAN_V3.json': 'a82be752fc04b3c8d0409076b62778c2d92cc8248d3366fa81cf197c48c064cf', 'docs/model_specs/codex/e18/artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json': '4b6bfb018e69ec0f7b2aa8d816f1aecf946ebbee77e02ea3e74e6169a3a15616'}

def create_agent(run_context=None):
    context = run_context or {}
    return FullSeasonController(deepcopy(_PLAN), int(context.get('player_position', 0)), reference_plan=_PARENT_27_PLAN)

_ACTIVE = {}

def agent(observation, configuration=None):
    seat = int(observation.get('player', 0))
    step = int(observation.get('step', 0))
    entry = _ACTIVE.get(seat)
    if entry is None or step <= entry[0]:
        policy = create_agent({'player_position': seat})
    else:
        policy = entry[1]
    _ACTIVE[seat] = (step, policy)
    return policy(observation, configuration)
