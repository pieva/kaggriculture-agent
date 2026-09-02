"""Single shared policy implementation for every frozen E16 cell.

This module intentionally depends only on the standard library so the exact file
can be frozen as the treatment build. Cell differences enter only through the
four manipulated values validated by :mod:`agricola.e16.config`.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from copy import deepcopy
from typing import Any

MANIPULATED_FIELDS = {
    "watering_dispatch_priority",
    "crop_working_set_target",
    "livestock_headcount_target",
    "pasture_allocation_target",
}
WATER_DISPATCH_RANKS = {
    0.20: 6,
    0.45: 3,
    0.70: 0,
}
CROP_MIX = ("WHEAT", "STRAWBERRY", "MELON")
SEED_COSTS = {"WHEAT": 10, "STRAWBERRY": 100, "MELON": 80}
SHED_TILES = ((4, 4), (5, 4), (4, 5), (5, 5))
CROP_POSITIONS = tuple((x, y) for y in range(3) for x in range(10))
PASTURE_POSITIONS = tuple(
    (x, y) for y in (3, 4) for x in range(10) if (x, y) not in {(4, 4), (5, 4)}
)
PRODUCTS = {
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


def _fib(index: int) -> int:
    a, b = 1, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def _distance(left: tuple[int, int], right: tuple[int, int]) -> int:
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def _move_towards(position: tuple[int, int], target: tuple[int, int]) -> list[str]:
    x, y = position
    tx, ty = target
    if x < tx:
        return ["EAST"]
    if x > tx:
        return ["WEST"]
    if y < ty:
        return ["SOUTH"]
    if y > ty:
        return ["NORTH"]
    return ["PASS"]


def _quota_counts(target: int) -> dict[str, int]:
    raw = {"WHEAT": target * 0.4, "STRAWBERRY": target * 0.4, "MELON": target * 0.2}
    counts = {crop: math.floor(value) for crop, value in raw.items()}
    remaining = target - sum(counts.values())
    order = sorted(
        CROP_MIX, key=lambda crop: (-(raw[crop] - counts[crop]), CROP_MIX.index(crop))
    )
    for crop in order[:remaining]:
        counts[crop] += 1
    return counts


def _crop_plan(target: int) -> dict[tuple[int, int], str]:
    quotas = _quota_counts(target)
    cycle: list[str] = []
    while len(cycle) < target:
        for crop in CROP_MIX:
            if quotas[crop] > 0:
                cycle.append(crop)
                quotas[crop] -= 1
    return {position: crop for position, crop in zip(CROP_POSITIONS[:target], cycle)}


def _inventory_total(inventory: dict[str, int]) -> int:
    return sum(int(value) for value in inventory.values())


def _water_dispatch_rank(priority: float) -> int:
    for level, rank in WATER_DISPATCH_RANKS.items():
        if math.isclose(priority, level, rel_tol=0.0, abs_tol=1e-12):
            return rank
    raise ValueError(f"unsupported watering dispatch priority: {priority}")


class E16TrainingAgent:
    """Deterministic treatment policy with a verified T0 treatment boundary."""

    def __init__(self, cell_config: dict[str, Any]):
        required = MANIPULATED_FIELDS | {
            "quadrants_owned",
            "workforce_headcount",
            "livestock_species",
            "operating_cash_floor",
            "endgame_shutdown_steps",
        }
        missing = required - set(cell_config)
        if missing:
            raise ValueError(f"missing E16 cell fields: {sorted(missing)}")
        if int(cell_config["quadrants_owned"]) != 2:
            raise ValueError("E16 hard cap requires quadrants_owned=2")
        if cell_config["livestock_species"] != "COW":
            raise ValueError("E16 livestock species must be COW")
        _water_dispatch_rank(float(cell_config["watering_dispatch_priority"]))

        self.config = deepcopy(cell_config)
        self.t0_step: int | None = None
        self.current_day: int | None = None
        self.watering_needs: set[tuple[int, int, int]] = set()
        self.watering_successes: set[tuple[int, int, int]] = set()
        self.last_observed_quadrants = 1

    @staticmethod
    def _farm(observation: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        player = int(observation.get("player", 0))
        farms = observation.get("farms", [])
        farm = farms[player] if player < len(farms) else {}
        private = observation.get("private", {}) or {}
        return farm, private

    @staticmethod
    def _owned_quadrants(farm: dict[str, Any]) -> int:
        raw = farm.get("unlocked_quadrants", ["NW"])
        if isinstance(raw, list):
            return len(raw)
        return int(raw)

    @staticmethod
    def _tile(farm: dict[str, Any], position: tuple[int, int]) -> Any:
        x, y = position
        tiles = farm.get("tiles", [])
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return "LOCKED"

    @staticmethod
    def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
        positions = [tuple(farm.get("farmer", [4, 4]))]
        positions.extend(tuple(position) for position in farm.get("hands", []))
        return positions

    def _active_values(self, quadrants: int) -> tuple[int, int, int, float]:
        if quadrants < 2 or self.t0_step is None:
            return 10, 0, 0, 0.45
        return (
            int(self.config["crop_working_set_target"]),
            int(self.config["pasture_allocation_target"]),
            int(self.config["livestock_headcount_target"]),
            float(self.config["watering_dispatch_priority"]),
        )

    def _sync_t0_and_water(
        self, observation: dict[str, Any], farm: dict[str, Any], quadrants: int
    ) -> None:
        step = int(observation.get("step", 0))
        day = int(observation.get("day", 0))
        if self.t0_step is None and self.last_observed_quadrants < 2 <= quadrants:
            self.t0_step = step
        self.last_observed_quadrants = quadrants

        if self.current_day != day:
            self.current_day = day
            self.watering_needs.clear()
            self.watering_successes.clear()
        for position in CROP_POSITIONS:
            tile = self._tile(farm, position)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                key = (day, position[0], position[1])
                self.watering_needs.add(key)
                if tile.get("watered_today", False):
                    self.watering_successes.add(key)

    def _target_action(
        self,
        position: tuple[int, int],
        targets: list[tuple[tuple[int, int], list[str]]],
        reserved: set[tuple[int, int]],
    ) -> list[str] | None:
        available = [
            (target, action) for target, action in targets if target not in reserved
        ]
        if not available:
            return None
        target, action = min(
            available,
            key=lambda pair: (_distance(position, pair[0]), pair[0][1], pair[0][0]),
        )
        reserved.add(target)
        return action if target == position else _move_towards(position, target)

    def _unit_actions(
        self,
        observation: dict[str, Any],
        farm: dict[str, Any],
        private: dict[str, Any],
        crop_target: int,
        pasture_target: int,
        herd_target: int,
        watering_priority: float,
        shutdown: bool,
    ) -> list[list[str]]:
        positions = self._positions(farm)
        inventories = list(private.get("inventories", []))
        while len(inventories) < len(positions):
            inventories.append({})
        shed = private.get("shed", {}) or {}
        crop_plan = _crop_plan(crop_target)
        pasture_positions = PASTURE_POSITIONS[:pasture_target]
        reserved: set[tuple[int, int]] = set()
        reserved_cow_pickups = 0
        reserved_wheat_pickups = 0

        water_targets: list[tuple[tuple[int, int], list[str]]] = []
        crop_harvest: list[tuple[tuple[int, int], list[str]]] = []
        crop_plant: list[tuple[tuple[int, int], list[str]]] = []
        pasture_build: list[tuple[tuple[int, int], list[str]]] = []
        empty_pasture: list[tuple[tuple[int, int], list[str]]] = []
        feed_targets: list[tuple[tuple[int, int], list[str]]] = []
        care_targets: list[tuple[tuple[int, int], list[str]]] = []
        fertilizer_targets: list[tuple[tuple[int, int], list[str]]] = []
        animal_harvest: list[tuple[tuple[int, int], list[str]]] = []

        available_seeds = {
            crop: int(private.get("seeds", {}).get(crop, 0)) for crop in CROP_MIX
        }
        for target, crop in crop_plan.items():
            tile = self._tile(farm, target)
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if not tile.get("watered_today", False):
                    water_targets.append((target, ["WATER"]))
                if int(tile.get("yield_units", 0)) > 0:
                    crop_harvest.append((target, ["HARVEST"]))
            elif tile is None and not shutdown and available_seeds[crop] > 0:
                crop_plant.append((target, ["PLANT", crop]))
                available_seeds[crop] -= 1

        for target in pasture_positions:
            tile = self._tile(farm, target)
            if tile is None and not shutdown:
                pasture_build.append((target, ["BUILD_PASTURE"]))
            elif (
                isinstance(tile, dict)
                and tile.get("kind") == "PASTURE"
                and not tile.get("animal")
            ):
                empty_pasture.append((target, ["PASS"]))
            elif isinstance(tile, dict) and tile.get("animal") == "COW":
                if not tile.get("fed_today", False):
                    feed_targets.append((target, ["FEED"]))
                if not tile.get("cared_today", False):
                    care_targets.append((target, ["CARE"]))
                if tile.get("fertilizer_available", False):
                    fertilizer_targets.append((target, ["COLLECT_FERTILIZER"]))
                if int(tile.get("yield_units", 0)) > 0:
                    animal_harvest.append((target, ["HARVEST"]))

        water_unmet = bool(water_targets)
        actions: list[list[str]] = []
        for worker_id, position in enumerate(positions):
            inventory = (
                inventories[worker_id]
                if isinstance(inventories[worker_id], dict)
                else {}
            )
            total_inventory = _inventory_total(inventory)
            carried_cow = int(inventory.get("COW", 0)) > 0
            carried_wheat = int(inventory.get("WHEAT", 0)) > 0
            carried_non_feed = any(
                item != "WHEAT" and item != "COW" and amount > 0
                for item, amount in inventory.items()
            )

            if carried_cow:
                choices = [(target, ["PLACE", "COW"]) for target, _ in empty_pasture]
                action = self._target_action(position, choices, reserved)
                actions.append(
                    action
                    or (
                        ["DROP"]
                        if position in SHED_TILES
                        else _move_towards(position, (4, 4))
                    )
                )
                continue

            if carried_wheat and feed_targets:
                action = self._target_action(position, feed_targets, reserved)
                if action is not None:
                    actions.append(action)
                    continue

            if (
                carried_non_feed
                or (carried_wheat and not feed_targets)
                or total_inventory >= 5
            ):
                actions.append(
                    ["DROP"]
                    if position in SHED_TILES
                    else _move_towards(position, (4, 4))
                )
                continue

            if position in SHED_TILES and total_inventory == 0:
                available_cows = max(0, int(shed.get("COW", 0)) - reserved_cow_pickups)
                if len(empty_pasture) > reserved_cow_pickups and available_cows > 0:
                    reserved_cow_pickups += 1
                    actions.append(["PICKUP", "COW", 1])
                    continue
                available_wheat = max(
                    0, int(shed.get("WHEAT", 0)) - reserved_wheat_pickups
                )
                remaining_feed = max(0, len(feed_targets) - reserved_wheat_pickups)
                if available_wheat > 0 and remaining_feed > 0:
                    quantity = min(5, available_wheat, remaining_feed)
                    reserved_wheat_pickups += quantity
                    actions.append(["PICKUP", "WHEAT", quantity])
                    continue

            priority_groups = [
                fertilizer_targets,
                animal_harvest,
                care_targets,
                pasture_build,
                crop_harvest,
                crop_plant,
            ]
            if water_unmet:
                priority_groups.insert(
                    _water_dispatch_rank(watering_priority), water_targets
                )
            action = None
            for group in priority_groups:
                action = self._target_action(position, group, reserved)
                if action is not None:
                    break
            actions.append(action or ["PASS"])

        return actions

    def _market_orders(
        self,
        farm: dict[str, Any],
        private: dict[str, Any],
        market: dict[str, Any],
        quadrants: int,
        crop_target: int,
        pasture_target: int,
        herd_target: int,
        shutdown: bool,
    ) -> list[list[Any]]:
        orders: list[list[Any]] = []
        cash = float(farm.get("money", 0.0))
        floor = float(self.config["operating_cash_floor"])

        def add(order: list[Any], estimated_cost: float = 0.0) -> bool:
            nonlocal cash
            if len(orders) >= 10 or cash - estimated_cost < floor:
                return False
            orders.append(order)
            cash -= estimated_cost
            return True

        # This is the sole land order. Once two quadrants are observed, no code
        # path can emit another BUY_LAND.
        if quadrants < 2:
            add(["BUY_LAND"], 1000.0)

        shed = private.get("shed", {}) or {}
        inventories = private.get("inventories", []) or []
        active_by_crop = {crop: 0 for crop in CROP_MIX}
        for position in CROP_POSITIONS[:crop_target]:
            tile = self._tile(farm, position)
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") in active_by_crop
            ):
                active_by_crop[tile["crop"]] += 1
        quotas = _quota_counts(crop_target)
        if not shutdown:
            for crop in CROP_MIX:
                deficit = max(
                    0,
                    quotas[crop]
                    - active_by_crop[crop]
                    - int(private.get("seeds", {}).get(crop, 0)),
                )
                if deficit:
                    add(["BUY_SEED", crop, deficit], deficit * SEED_COSTS[crop])

        hands = len(farm.get("hands", []))
        target_hands = int(self.config["workforce_headcount"])
        hires_today = int(farm.get("hires_today", 0))
        for offset in range(max(0, target_hands - hands)):
            if not add(["HIRE"], float(_fib(hires_today + offset))):
                break

        if quadrants >= 2 and self.t0_step is not None:
            pasture_count = sum(
                1
                for position in PASTURE_POSITIONS[:pasture_target]
                if isinstance(self._tile(farm, position), dict)
                and self._tile(farm, position).get("kind") == "PASTURE"
            )
            cows_on_tiles = sum(
                1
                for position in PASTURE_POSITIONS[:pasture_target]
                if isinstance(self._tile(farm, position), dict)
                and self._tile(farm, position).get("animal") == "COW"
            )
            cows_in_transit = int(shed.get("COW", 0)) + sum(
                int(inv.get("COW", 0)) for inv in inventories if isinstance(inv, dict)
            )
            cow_deficit = max(
                0, min(herd_target, pasture_count) - cows_on_tiles - cows_in_transit
            )
            if cow_deficit and not shutdown:
                affordable = max(0, int((cash - floor) // 400))
                quantity = min(cow_deficit, affordable, 10)
                if quantity:
                    add(["BUY_ANIMAL", "COW", quantity], quantity * 400.0)

            feed_demand = cows_on_tiles * 3 + (2 if cows_on_tiles else 0)
            wheat_carried = sum(
                int(inv.get("WHEAT", 0)) for inv in inventories if isinstance(inv, dict)
            )
            wheat_deficit = max(
                0, feed_demand - int(shed.get("WHEAT", 0)) - wheat_carried
            )
            wheat_price = float((market.get("prices", {}) or {}).get("WHEAT", 10.0))
            if wheat_deficit and wheat_price > 0:
                quantity = min(
                    wheat_deficit, max(0, int((cash - floor) // wheat_price)), 10
                )
                if quantity:
                    add(["BUY_PRODUCT", "WHEAT", quantity], quantity * wheat_price)

        # Sales are common and last in the queue. Wheat needed for feed is held.
        reserve = herd_target * 3 + (2 if herd_target else 0)
        for product in ("MILK", "STRAWBERRY", "MELON", "WHEAT", "FERTILIZER"):
            quantity = int(shed.get(product, 0))
            if product == "WHEAT":
                quantity = max(0, quantity - reserve)
            if quantity > 0 and len(orders) < 10:
                orders.append(["SELL", product, quantity])
        return orders[:10]

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        farm, private = self._farm(observation)
        quadrants = self._owned_quadrants(farm)
        if quadrants > 2:
            raise RuntimeError(
                "E16 hard cap violated: observed more than two quadrants"
            )
        self._sync_t0_and_water(observation, farm, quadrants)
        crop_target, pasture_target, herd_target, watering_priority = (
            self._active_values(quadrants)
        )
        if isinstance(configuration, dict):
            episode_steps = int(configuration.get("episodeSteps", 720))
        else:
            episode_steps = int(getattr(configuration, "episodeSteps", 720))
        shutdown = episode_steps - int(observation.get("step", 0)) <= int(
            self.config["endgame_shutdown_steps"]
        )
        actions = self._unit_actions(
            observation,
            farm,
            private,
            crop_target,
            pasture_target,
            herd_target,
            watering_priority,
            shutdown,
        )
        market_orders = self._market_orders(
            farm,
            private,
            observation.get("market", {}) or {},
            quadrants,
            crop_target,
            pasture_target,
            herd_target,
            shutdown,
        )
        return {
            "farmer": actions[0] if actions else ["PASS"],
            "hands": actions[1:],
            "market": market_orders,
        }


def create_agent(
    cell_config: dict[str, Any],
) -> Callable[[dict[str, Any], Any], dict[str, Any]]:
    """Create an isolated stateful agent for exactly one episode."""

    instance = E16TrainingAgent(cell_config)

    def treatment_agent(
        observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        return instance(observation, configuration)

    treatment_agent.e16_instance = instance  # type: ignore[attr-defined]
    return treatment_agent
