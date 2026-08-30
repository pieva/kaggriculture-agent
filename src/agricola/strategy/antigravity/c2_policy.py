"""Antigravity C2 Policy Implementation.

Implements the C2 Model Foundation specification for Antigravity:
- Strict harvest readiness gate (CRP-10) preventing premature harvest no-ops.
- Tile lifecycle classification (CRP-09) supporting 6 discrete states.
- Preventive and recovery DIG actions for working-set maintenance.
- Day-0 and urgent EOD water prioritization.
- Full multi-occupancy routing and clean inventory management.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Set, Tuple

from agricola.strategy.antigravity.c2_config import AntigravityC2Config

CROPS: Dict[str, Dict[str, Any]] = {
    "WHEAT": {"first_yield_day": 3, "interval": 0, "ongoing": False, "max_yield": 10},
    "STRAWBERRY": {"first_yield_day": 5, "interval": 3, "ongoing": True, "max_yield": 12},
    "MELON": {"first_yield_day": 8, "interval": 0, "ongoing": False, "max_yield": 14},
    "CARROT": {"first_yield_day": 3, "interval": 0, "ongoing": False, "max_yield": 9},
    "TOMATO": {"first_yield_day": 4, "interval": 2, "ongoing": True, "max_yield": 10},
}

SEED_COSTS: Dict[str, float] = {
    "WHEAT": 10.0,
    "STRAWBERRY": 100.0,
    "MELON": 80.0,
    "CARROT": 10.0,
    "TOMATO": 50.0,
}

SHED_TILES: Set[Tuple[int, int]] = {(4, 4), (5, 4), (4, 5), (5, 5)}
CROP_POSITIONS: Tuple[Tuple[int, int], ...] = tuple((x, y) for y in range(3) for x in range(10))
PASTURE_POSITIONS: Tuple[Tuple[int, int], ...] = tuple(
    (x, y) for y in (3, 4) for x in range(10) if (x, y) not in {(4, 4), (5, 4)}
)


def _fib(index: int) -> int:
    a, b = 1, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def _distance(left: Tuple[int, int], right: Tuple[int, int]) -> int:
    return abs(left[0] - right[0]) + abs(left[1] - right[1])


def _move_towards(position: Tuple[int, int], target: Tuple[int, int]) -> List[str]:
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


def _quota_counts(target: int, weights: Dict[str, float]) -> Dict[str, int]:
    raw = {crop: target * weight for crop, weight in weights.items()}
    counts = {crop: math.floor(value) for crop, value in raw.items()}
    remaining = target - sum(counts.values())
    order = sorted(
        weights.keys(),
        key=lambda c: (-(raw[c] - counts[c]), list(weights.keys()).index(c)),
    )
    for crop in order[:remaining]:
        counts[crop] += 1
    return counts


def _crop_plan(target: int, weights: Dict[str, float]) -> Dict[Tuple[int, int], str]:
    quotas = _quota_counts(target, weights)
    cycle: List[str] = []
    crops_list = list(weights.keys())
    while len(cycle) < target:
        for crop in crops_list:
            if quotas[crop] > 0:
                cycle.append(crop)
                quotas[crop] -= 1
    return {position: crop for position, crop in zip(CROP_POSITIONS[:target], cycle)}


def _inventory_total(inventory: Dict[str, int]) -> int:
    return sum(int(v) for v in inventory.values())


class AntigravityC2Policy:
    """Antigravity C2 Decision Policy."""

    def __init__(self, config: Optional[AntigravityC2Config] = None):
        self.config = config or AntigravityC2Config()
        self.crop_plan = _crop_plan(
            self.config.crop_working_set_target, self.config.crop_mix_weights
        )

    def is_harvest_ready(self, tile: Any, current_day: int) -> bool:
        """Evaluate canonical CRP-10 harvest_ready predicate."""
        if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
            return False
        yield_units = int(tile.get("yield_units", 0))
        if yield_units <= 0:
            return False
        crop = tile.get("crop", "WHEAT")
        planted_day = int(tile.get("planted_day", 0))
        first_yield_day = CROPS.get(crop, {}).get("first_yield_day", 3)
        return (current_day - planted_day) >= first_yield_day

    def classify_tile_lifecycle(
        self,
        position: Tuple[int, int],
        tile: Any,
        current_day: int,
        engine_step: int,
    ) -> str:
        """Classify tile into one of the 6 canonical lifecycle states (CRP-09)."""
        if position not in self.crop_plan:
            return "OUT_OF_SCOPE"
        if tile is None:
            return "EMPTY_ASSIGNED"
        if isinstance(tile, dict):
            kind = tile.get("kind")
            if kind == "WEED":
                return "LOST_WEED"
            if kind == "PLANT":
                crop = tile.get("crop", "WHEAT")
                rule = CROPS.get(crop, {})
                is_ongoing = rule.get("ongoing", False)
                yield_units = int(tile.get("yield_units", 0))
                max_lifespan_step = tile.get("max_lifespan_step")

                # Check if retired ongoing crop
                if is_ongoing and yield_units == 0 and max_lifespan_step is not None:
                    if engine_step >= int(max_lifespan_step):
                        return "RETIREMENT_DUE"

                # Check harvest readiness
                if self.is_harvest_ready(tile, current_day):
                    return "HARVEST_READY"

                return "GROWING"
        return "OUT_OF_SCOPE"

    def _tile(self, farm: Dict[str, Any], position: Tuple[int, int]) -> Any:
        x, y = position
        tiles = farm.get("tiles", [])
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
            return tiles[y][x]
        return "LOCKED"

    def _target_action(
        self,
        worker_pos: Tuple[int, int],
        candidates: List[Tuple[Tuple[int, int], List[str]]],
        reserved: Set[Tuple[int, int]],
    ) -> Optional[List[str]]:
        """Assign best target minimizing Manhattan distance with target reservation."""
        available = [item for item in candidates if item[0] not in reserved]
        if not available:
            return None
        target_pos, action_cmd = min(
            available, key=lambda item: _distance(worker_pos, item[0])
        )
        reserved.add(target_pos)
        if worker_pos == target_pos:
            return action_cmd
        return _move_towards(worker_pos, target_pos)

    def decide_actions(
        self,
        observation: Dict[str, Any],
        player_index: int = 0,
    ) -> List[List[str]]:
        """Generate unit actions for main farmer and all farm hands."""
        farms = observation.get("farms", [])
        if player_index >= len(farms):
            return [["PASS"]]
        farm = farms[player_index]
        privates = observation.get("private", [])
        private = privates[player_index] if player_index < len(privates) else {}

        current_step = int(observation.get("step", 0))
        current_day = int(observation.get("day", 0))
        turns_per_day = int(observation.get("turnsPerDay", 24))
        max_steps = int(observation.get("max_steps", 720))
        shutdown = (max_steps - current_step) <= self.config.endgame_shutdown_steps

        farmer_pos = tuple(farm.get("farmer", [4, 4]))
        hands_raw = farm.get("hands", [])
        hands_positions = [tuple(h) for h in hands_raw]
        all_positions: List[Tuple[int, int]] = [farmer_pos] + hands_positions

        inventories_raw = private.get("inventories", []) or []
        inventories: List[Dict[str, int]] = []
        for idx in range(len(all_positions)):
            if idx < len(inventories_raw) and isinstance(inventories_raw[idx], dict):
                inventories.append(inventories_raw[idx])
            else:
                inventories.append({})

        shed = private.get("shed", {}) or {}
        seeds = private.get("seeds", {}) or {}
        available_seeds = {k: int(v) for k, v in seeds.items()}

        # Task buckets
        critical_water_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        normal_water_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        harvest_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        preventive_dig_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        recovery_dig_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        plant_targets: List[Tuple[Tuple[int, int], List[str]]] = []

        pasture_build_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        empty_pasture_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        feed_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        care_targets: List[Tuple[Tuple[int, int], List[str]]] = []
        animal_harvest_targets: List[Tuple[Tuple[int, int], List[str]]] = []

        # Scan working set crop positions
        for pos, crop in self.crop_plan.items():
            tile = self._tile(farm, pos)
            state = self.classify_tile_lifecycle(pos, tile, current_day, current_step)

            if state == "LOST_WEED":
                if self.config.enable_recovery_dig:
                    recovery_dig_targets.append((pos, ["DIG"]))
            elif state == "RETIREMENT_DUE":
                if self.config.enable_preventive_dig:
                    preventive_dig_targets.append((pos, ["DIG"]))
            elif state == "HARVEST_READY":
                harvest_targets.append((pos, ["HARVEST"]))
            elif state == "GROWING":
                if isinstance(tile, dict) and not tile.get("watered_today", False):
                    consecutive_unwatered = int(tile.get("consecutive_unwatered", 0))
                    # Critical day-0 or 2nd day unwatered
                    if consecutive_unwatered + 1 >= 2 or consecutive_unwatered == 1:
                        critical_water_targets.append((pos, ["WATER"]))
                    else:
                        normal_water_targets.append((pos, ["WATER"]))
            elif state == "EMPTY_ASSIGNED":
                if not shutdown and available_seeds.get(crop, 0) > 0:
                    plant_targets.append((pos, ["PLANT", crop]))
                    available_seeds[crop] -= 1

        # Scan pasture positions
        for pos in PASTURE_POSITIONS[: self.config.pasture_allocation_target]:
            tile = self._tile(farm, pos)
            if tile is None and not shutdown:
                pasture_build_targets.append((pos, ["BUILD_PASTURE"]))
            elif isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                animal = tile.get("animal")
                if not animal:
                    empty_pasture_targets.append((pos, ["PASS"]))
                elif animal == "COW":
                    if not tile.get("fed_today", False):
                        feed_targets.append((pos, ["FEED"]))
                    if not tile.get("cared_today", False):
                        care_targets.append((pos, ["CARE"]))
                    if int(tile.get("yield_units", 0)) > 0:
                        animal_harvest_targets.append((pos, ["HARVEST"]))

        # Dispatch actions per worker
        reserved: Set[Tuple[int, int]] = set()
        actions: List[List[str]] = []
        reserved_wheat_pickups = 0

        for worker_id, pos in enumerate(all_positions):
            inv = inventories[worker_id]
            total_inv = _inventory_total(inv)
            carried_wheat = int(inv.get("WHEAT", 0)) > 0
            carried_non_feed = any(
                item != "WHEAT" and item != "COW" and amt > 0 for item, amt in inv.items()
            )

            # 1. Handle carried items requiring drop
            if carried_non_feed or (carried_wheat and not feed_targets) or total_inv >= 5:
                if pos in SHED_TILES:
                    actions.append(["DROP"])
                else:
                    actions.append(_move_towards(pos, (4, 4)))
                continue

            # 2. Feed animal if carrying wheat
            if carried_wheat and feed_targets:
                act = self._target_action(pos, feed_targets, reserved)
                if act is not None:
                    actions.append(act)
                    continue

            # 3. Pickup feed at shed if needed
            if pos in SHED_TILES and total_inv == 0:
                available_wheat = max(0, int(shed.get("WHEAT", 0)) - reserved_wheat_pickups)
                remaining_feed = max(0, len(feed_targets) - reserved_wheat_pickups)
                if available_wheat > 0 and remaining_feed > 0:
                    qty = min(5, available_wheat, remaining_feed)
                    reserved_wheat_pickups += qty
                    actions.append(["PICKUP", "WHEAT", qty])
                    continue

            # 4. Action Priority Cascade
            priority_groups = [
                critical_water_targets,      # P0: Prevent Day-0 / EOD death
                harvest_targets,             # P1: Realize mature output
                preventive_dig_targets + recovery_dig_targets,  # P2: Clear retired crops & recover weed tiles
                normal_water_targets,        # P3: Standard hydration
                plant_targets,               # P4: Replant / extend surface
                animal_harvest_targets,      # P5: Livestock product collection
                care_targets,                # P6: Care bonus accumulation
                pasture_build_targets,       # P7: Pasture expansion
            ]

            action: Optional[List[str]] = None
            for group in priority_groups:
                action = self._target_action(pos, group, reserved)
                if action is not None:
                    break

            actions.append(action or ["PASS"])

        return actions

    def decide_market_orders(
        self,
        observation: Dict[str, Any],
        player_index: int = 0,
    ) -> List[List[Any]]:
        """Generate market transactions (BUY_LAND, BUY_SEED, HIRE, SELL)."""
        farms = observation.get("farms", [])
        if player_index >= len(farms):
            return []
        farm = farms[player_index]
        privates = observation.get("private", [])
        private = privates[player_index] if player_index < len(privates) else {}

        current_step = int(observation.get("step", 0))
        max_steps = int(observation.get("max_steps", 720))
        shutdown = (max_steps - current_step) <= self.config.endgame_shutdown_steps

        cash = float(farm.get("money", 0.0))
        floor = self.config.operating_cash_floor
        orders: List[List[Any]] = []

        def add_order(order: List[Any], cost: float = 0.0) -> bool:
            nonlocal cash
            if len(orders) >= 10 or (cash - cost) < floor:
                return False
            orders.append(order)
            cash -= cost
            return True

        # 1. Land expansion to 2 quadrants
        unlocked = farm.get("unlocked_quadrants", ["NW"])
        quad_count = len(unlocked) if isinstance(unlocked, list) else int(unlocked)
        if quad_count < self.config.quadrants_owned:
            add_order(["BUY_LAND"], 1000.0)

        # 2. Seed purchasing for working set deficit
        if not shutdown:
            active_by_crop: Dict[str, int] = {k: 0 for k in self.config.crop_mix_weights}
            for pos in list(self.crop_plan.keys())[: self.config.crop_working_set_target]:
                tile = self._tile(farm, pos)
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    c = tile.get("crop", "WHEAT")
                    if c in active_by_crop:
                        active_by_crop[c] += 1

            quotas = _quota_counts(
                self.config.crop_working_set_target, self.config.crop_mix_weights
            )
            seeds = private.get("seeds", {}) or {}
            for crop, quota in quotas.items():
                in_seed = int(seeds.get(crop, 0))
                active = active_by_crop.get(crop, 0)
                deficit = max(0, quota - active - in_seed)
                if deficit > 0:
                    cost_per_unit = SEED_COSTS.get(crop, 10.0)
                    add_order(["BUY_SEED", crop, deficit], deficit * cost_per_unit)

        # 3. Workforce hiring up to target headcount
        current_hands = len(farm.get("hands", []))
        hires_today = int(farm.get("hires_today", 0))
        needed_hires = max(0, self.config.workforce_headcount - (1 + current_hands))
        for offset in range(needed_hires):
            cost = float(_fib(hires_today + offset))
            if not add_order(["HIRE"], cost):
                break

        # 4. Livestock purchase if pasture available
        shed = private.get("shed", {}) or {}
        if quad_count >= 2 and not shutdown:
            pastures_count = sum(
                1
                for pos in PASTURE_POSITIONS[: self.config.pasture_allocation_target]
                if isinstance(self._tile(farm, pos), dict)
                and self._tile(farm, pos).get("kind") == "PASTURE"
            )
            cows_on_tiles = sum(
                1
                for pos in PASTURE_POSITIONS[: self.config.pasture_allocation_target]
                if isinstance(self._tile(farm, pos), dict)
                and self._tile(farm, pos).get("animal") == "COW"
            )
            cows_in_shed = int(shed.get("COW", 0))
            cow_deficit = max(
                0,
                min(self.config.livestock_headcount_target, pastures_count)
                - cows_on_tiles
                - cows_in_shed,
            )
            if cow_deficit > 0:
                affordable = max(0, int((cash - floor) // 400.0))
                qty = min(cow_deficit, affordable, 10)
                if qty > 0:
                    add_order(["BUY_ANIMAL", "COW", qty], qty * 400.0)

            # Feed procurement for cows
            feed_demand = cows_on_tiles * 3 + (2 if cows_on_tiles else 0)
            wheat_in_shed = int(shed.get("WHEAT", 0))
            wheat_deficit = max(0, feed_demand - wheat_in_shed)
            if wheat_deficit > 0:
                add_order(["BUY_PRODUCT", "WHEAT", wheat_deficit], wheat_deficit * 10.0)

        # 5. Sell inventory from shed to avoid overflow and realize revenue
        for item in ["MILK", "WOOL", "EGG", "MELON", "STRAWBERRY"]:
            qty = int(shed.get(item, 0))
            if qty > 0:
                add_order(["SELL", item, qty], 0.0)

        if shutdown:
            # Liquidate remaining wheat in endgame
            wheat_qty = int(shed.get("WHEAT", 0))
            if wheat_qty > 0:
                add_order(["SELL", "WHEAT", wheat_qty], 0.0)

        return orders
