"""Decision policy and tactical dispatch for Antigravity C2 Livestock Diagnostic Variant (LS1)."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Set, Tuple

from agricola.strategy.antigravity_livestock.c2_livestock_config import AntigravityC2LivestockConfig

CROPS: Dict[str, Dict[str, Any]] = {
    "WHEAT": {"first_yield_day": 2, "max_yield_day": 4, "interval": 0, "ongoing": False, "max_yield": 6, "seed": 10},
    "CARROT": {"first_yield_day": 2, "max_yield_day": 3, "interval": 0, "ongoing": False, "max_yield": 4, "seed": 20},
    "TOMATO": {"first_yield_day": 8, "max_yield_day": 8, "interval": 1, "ongoing": True, "max_yield": 4, "seed": 50},
    "STRAWBERRY": {"first_yield_day": 10, "max_yield_day": 10, "interval": 2, "ongoing": True, "max_yield": 4, "seed": 100},
    "MELON": {"first_yield_day": 10, "max_yield_day": 12, "interval": 0, "ongoing": False, "max_yield": 6, "seed": 80},
}

ANIMALS: Dict[str, Dict[str, Any]] = {
    "GOOSE": {"cost": 300, "structure": "COOP", "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW": {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}

SEED_COSTS: Dict[str, float] = {
    "WHEAT": 10.0,
    "STRAWBERRY": 100.0,
    "MELON": 80.0,
    "CARROT": 10.0,
    "TOMATO": 50.0,
}

SHED_ACCESS_TILES: Set[Tuple[int, int]] = {(4, 4), (5, 4)}
# Centered Pasture Tiles: directly adjacent (1 step) to central shed access tiles
PASTURE_TILES: Set[Tuple[int, int]] = {(3, 4), (6, 4)}

# 44 sorted farmable crop positions in Quadrants 0 (NW) and 1 (NE) excluding shed and centered pastures
CROP_POSITIONS_44: Tuple[Tuple[int, int], ...] = (
    # Distance 1
    (4, 3), (5, 3),
    # Distance 2
    (2, 4), (3, 3), (4, 2), (5, 2), (6, 3), (7, 4),
    # Distance 3
    (1, 4), (2, 3), (3, 2), (4, 1), (5, 1), (6, 2), (7, 3), (8, 4),
    # Distance 4
    (0, 4), (1, 3), (2, 2), (3, 1), (4, 0), (5, 0), (6, 1), (7, 2), (8, 3), (9, 4),
    # Distance 5
    (0, 3), (1, 2), (2, 1), (3, 0), (6, 0), (7, 1), (8, 2), (9, 3),
    # Distance 6
    (0, 2), (1, 1), (2, 0), (7, 0), (8, 1), (9, 2),
    # Distance 7
    (0, 1), (1, 0), (8, 0), (9, 1),
    # Distance 8
    (0, 0), (9, 0),
)


def _get_private(observation: Dict[str, Any], player_index: int = 0) -> Dict[str, Any]:
    """Extract private dictionary robustly."""
    raw_private = observation.get("private", {})
    if isinstance(raw_private, dict):
        return raw_private
    if isinstance(raw_private, list):
        if 0 <= player_index < len(raw_private) and isinstance(raw_private[player_index], dict):
            return raw_private[player_index]
        return {}
    return {}


def _fib(index: int) -> int:
    """Calculate Fibonacci number for wage determination."""
    a, b = 1, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def _shortest_path_step(
    start: Tuple[int, int],
    target: Tuple[int, int],
) -> Optional[str]:
    """Determine immediate orthogonal cardinal direction step towards target."""
    sx, sy = start
    tx, ty = target
    if sx == tx and sy == ty:
        return None
    dx = tx - sx
    dy = ty - sy
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


class AntigravityC2LivestockPolicy:
    """Deliberative and tactical policy for Antigravity C2 Livestock Diagnostic Variant."""

    def __init__(self, config: Optional[AntigravityC2LivestockConfig] = None) -> None:
        self.config = config or AntigravityC2LivestockConfig()
        self.crop_positions = CROP_POSITIONS_44
        self.pasture_positions = tuple(PASTURE_TILES)

    def decide_market_orders(
        self,
        observation: Dict[str, Any],
        player_index: int = 0,
    ) -> List[List[Any]]:
        """Compute atomic market orders following DLC precedence."""
        orders: List[List[Any]] = []
        current_step = int(observation.get("step", 0))
        current_day = int(observation.get("day", 0))
        farms = observation.get("farms", [])
        if player_index >= len(farms):
            return orders
        farm = farms[player_index]
        tiles = farm.get("tiles", [])
        cash = float(farm.get("money", 0.0))
        unlocked = farm.get("unlocked_quadrants", ["NW"])
        hires_today = int(farm.get("hires_today", 0))
        private = _get_private(observation, player_index)
        shed = private.get("shed", {}) or {}
        seeds = private.get("seeds", {}) or {}

        # 1. SELL ALL PRODUCTS IN SHED
        for product in ["MELON", "STRAWBERRY", "WHEAT", "CARROT", "TOMATO", "EGG", "MILK", "WOOL", "FERTILIZER"]:
            qty = int(shed.get(product, 0))
            if qty > 0 and len(orders) < 10:
                if product == "WHEAT" and current_day >= self.config.livestock_activation_day and qty > 4:
                    orders.append(["SELL", product, qty - 4])
                elif product != "WHEAT":
                    orders.append(["SELL", product, qty])
                elif product == "WHEAT" and current_day < self.config.livestock_activation_day:
                    orders.append(["SELL", product, qty])

        # 2. LAND EXPANSION ON DAY 0
        if "NE" not in unlocked and cash >= 1000.0 and len(orders) < 10:
            orders.append(["BUY_LAND"])
            cash -= 1000.0

        # 3. WORKFORCE HIRING
        target_hands = max(0, self.config.workforce_headcount - 1)
        needed_hires = max(0, target_hands - hires_today)
        if needed_hires > 0 and len(orders) < 10:
            total_wage_cost = sum(_fib(hires_today + i) for i in range(needed_hires))
            if cash >= total_wage_cost + self.config.operating_cash_floor:
                for _ in range(needed_hires):
                    if len(orders) < 10:
                        orders.append(["HIRE"])
                cash -= total_wage_cost

        # 4. LIVESTOCK ORDER (Day >= activation day)
        if current_day >= self.config.livestock_activation_day and len(orders) < 10:
            active_animals = 0
            for r in tiles:
                for t in r:
                    if isinstance(t, dict) and t.get("animal") == self.config.livestock_species:
                        active_animals += 1
            animals_in_shed = int(shed.get(self.config.livestock_species, 0))
            needed_animals = max(0, self.config.livestock_headcount_target - (active_animals + animals_in_shed))
            animal_cost = ANIMALS[self.config.livestock_species]["cost"]
            if needed_animals > 0 and cash >= (needed_animals * animal_cost) + 500.0:
                orders.append(["BUY_ANIMAL", self.config.livestock_species, needed_animals])
                cash -= needed_animals * animal_cost

        # 5. SEED ORDERS
        if current_step < (720 - self.config.endgame_shutdown_steps) and len(orders) < 10:
            active_crops: Dict[str, int] = {"WHEAT": 0, "STRAWBERRY": 0, "MELON": 0}
            for pos in self.crop_positions[: self.config.crop_working_set_target]:
                x, y = pos
                if y < len(tiles) and x < len(tiles[y]):
                    t = tiles[y][x]
                    if isinstance(t, dict) and t.get("kind") == "PLANT":
                        c = t.get("crop")
                        if c in active_crops:
                            active_crops[c] += 1

            total_slots = min(len(self.crop_positions), self.config.crop_working_set_target)
            weights = self.config.crop_mix_weights

            if current_day >= 18:
                weights = {"WHEAT": 1.0, "STRAWBERRY": 0.0, "MELON": 0.0}
            elif current_day >= 12:
                weights = {"WHEAT": 0.30, "STRAWBERRY": 0.30, "MELON": 0.40}

            target_crops = {c: int(round(total_slots * w)) for c, w in weights.items()}
            deficit = {
                c: max(0, target_crops[c] - (active_crops[c] + int(seeds.get(c, 0))))
                for c in ["MELON", "STRAWBERRY", "WHEAT"]
            }

            labor_reserve = 880.0 if current_day <= 10 else 200.0
            order_priority = ["MELON", "STRAWBERRY", "WHEAT"]
            for crop in order_priority:
                needed = deficit.get(crop, 0)
                if needed > 0 and len(orders) < 10:
                    cost_per_seed = SEED_COSTS.get(crop, 10.0)
                    avail_cash = max(0.0, cash - self.config.operating_cash_floor - labor_reserve)
                    buy_qty = min(needed, int(avail_cash // cost_per_seed))
                    if buy_qty > 0:
                        orders.append(["BUY_SEED", crop, buy_qty])
                        cash -= buy_qty * cost_per_seed

        return orders

    def decide_actions(
        self,
        observation: Dict[str, Any],
        player_index: int = 0,
    ) -> List[List[str]]:
        """Compute coordinated unit actions for farmer and farm hands."""
        current_step = int(observation.get("step", 0))
        current_day = int(observation.get("day", 0))
        farms = observation.get("farms", [])
        if player_index >= len(farms):
            return [["PASS"]]
        farm = farms[player_index]
        tiles = farm.get("tiles", [])
        farmer_pos = tuple(farm.get("farmer", [4, 4]))
        hands = farm.get("hands", [])
        private = _get_private(observation, player_index)
        shed = private.get("shed", {}) or {}
        seeds = private.get("seeds", {}) or {}
        inventories = private.get("inventories", [{}])

        units: List[Tuple[int, Tuple[int, int], Dict[str, int]]] = []
        units.append((0, (farmer_pos[0], farmer_pos[1]), inventories[0] if inventories else {}))
        for i, h in enumerate(hands):
            inv = inventories[i + 1] if i + 1 < len(inventories) else {}
            units.append((i + 1, (h[0], h[1]), inv))

        actions: List[List[str]] = [["PASS"] for _ in range(len(units))]

        # Scan farm tiles
        weed_tiles: List[Tuple[int, int]] = []
        water_needed: List[Tuple[int, int]] = []
        harvest_ready: List[Tuple[int, int]] = []
        empty_crop_tiles: List[Tuple[int, int]] = []
        pasture_build_needed: List[Tuple[int, int]] = []
        animal_place_needed: List[Tuple[int, int]] = []
        animal_feed_needed: List[Tuple[int, int]] = []
        animal_harvest_needed: List[Tuple[int, int]] = []

        # Livestock tiles inspection
        if current_day >= self.config.livestock_activation_day:
            for ppos in self.pasture_positions:
                px, py = ppos
                if py < len(tiles) and px < len(tiles[py]):
                    t = tiles[py][px]
                    if t is None:
                        pasture_build_needed.append(ppos)
                    elif isinstance(t, dict):
                        if t.get("kind") == "PASTURE" and "animal" not in t:
                            animal_place_needed.append(ppos)
                        elif "animal" in t:
                            if not t.get("fed_today", False):
                                animal_feed_needed.append(ppos)
                            if t.get("yield_units", 0) > 0:
                                animal_harvest_needed.append(ppos)
                        elif t.get("kind") in ("PLANT", "WEED"):
                            weed_tiles.append(ppos)

        # Crop tiles inspection
        for pos in self.crop_positions[: self.config.crop_working_set_target]:
            x, y = pos
            if y < len(tiles) and x < len(tiles[y]):
                tile = tiles[y][x]
                if tile is None:
                    empty_crop_tiles.append(pos)
                elif isinstance(tile, dict):
                    kind = tile.get("kind")
                    if kind == "WEED":
                        weed_tiles.append(pos)
                    elif kind == "PLANT":
                        crop_name = tile.get("crop")
                        crop_data = CROPS.get(crop_name, {})
                        age = current_day - tile.get("planted_day", current_day)
                        yield_units = tile.get("yield_units", 0)
                        watered = tile.get("watered_today", False)

                        is_ready = False
                        if crop_data.get("ongoing", False):
                            if age >= crop_data.get("first_yield_day", 10) and yield_units > 0:
                                is_ready = True
                        else:
                            if age >= crop_data.get("max_yield_day", 4) and yield_units > 0:
                                is_ready = True
                            elif age >= crop_data.get("first_yield_day", 2) and yield_units >= crop_data.get("max_yield", 6):
                                is_ready = True

                        if is_ready:
                            harvest_ready.append(pos)
                        elif not watered:
                            water_needed.append(pos)

        seed_inventory: List[str] = []
        for sname in ["MELON", "STRAWBERRY", "WHEAT"]:
            cnt = int(seeds.get(sname, 0))
            seed_inventory.extend([sname] * cnt)

        claimed_tasks: Set[Tuple[int, int]] = set()

        for u_idx, pos, inv in units:
            ux, uy = pos

            # 0. INVENTORY OFFLOAD (Produce drops)
            has_harvest_drops = any(inv.get(p, 0) > 0 for p in ["MELON", "STRAWBERRY", "MILK", "EGG", "WOOL", "CARROT", "TOMATO"])
            has_excess_wheat = inv.get("WHEAT", 0) > 1 or (inv.get("WHEAT", 0) > 0 and not animal_feed_needed)

            if has_harvest_drops or has_excess_wheat:
                if (ux, uy) in SHED_ACCESS_TILES:
                    actions[u_idx] = ["DROP"]
                    continue
                else:
                    nearest_shed = min(SHED_ACCESS_TILES, key=lambda s: abs(ux-s[0]) + abs(uy-s[1]))
                    step_dir = _shortest_path_step((ux, uy), nearest_shed)
                    if step_dir:
                        actions[u_idx] = [step_dir]
                        continue

            # 1. ANIMAL FEEDING (Priority handler)
            if animal_feed_needed and u_idx in (0, 1):
                unclaimed_feed = [p for p in animal_feed_needed if p not in claimed_tasks]
                if unclaimed_feed:
                    target_cow = min(unclaimed_feed, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                    if inv.get("WHEAT", 0) > 0:
                        if (ux, uy) == target_cow:
                            actions[u_idx] = ["FEED"]
                            claimed_tasks.add(target_cow)
                            animal_feed_needed.remove(target_cow)
                            continue
                        else:
                            step_dir = _shortest_path_step((ux, uy), target_cow)
                            if step_dir:
                                actions[u_idx] = [step_dir]
                                claimed_tasks.add(target_cow)
                                continue
                    elif (ux, uy) in SHED_ACCESS_TILES and shed.get("WHEAT", 0) > 0:
                        actions[u_idx] = ["PICKUP", "WHEAT", 1]
                        claimed_tasks.add(target_cow)
                        continue
                    elif shed.get("WHEAT", 0) > 0:
                        nearest_shed = min(SHED_ACCESS_TILES, key=lambda s: abs(ux-s[0]) + abs(uy-s[1]))
                        step_dir = _shortest_path_step((ux, uy), nearest_shed)
                        if step_dir:
                            actions[u_idx] = [step_dir]
                            claimed_tasks.add(target_cow)
                            continue

            # 2. ANIMAL HARVEST (Milk)
            if animal_harvest_needed:
                unclaimed_harv = [p for p in animal_harvest_needed if p not in claimed_tasks]
                if unclaimed_harv:
                    target_cow = min(unclaimed_harv, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                    if (ux, uy) == target_cow:
                        actions[u_idx] = ["HARVEST"]
                        claimed_tasks.add(target_cow)
                        animal_harvest_needed.remove(target_cow)
                        continue
                    else:
                        step_dir = _shortest_path_step((ux, uy), target_cow)
                        if step_dir:
                            actions[u_idx] = [step_dir]
                            claimed_tasks.add(target_cow)
                            continue

            # 3. ANIMAL PLACEMENT
            if animal_place_needed:
                unclaimed_place = [p for p in animal_place_needed if p not in claimed_tasks]
                if unclaimed_place:
                    target_pasture = min(unclaimed_place, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                    if inv.get("COW", 0) > 0:
                        if (ux, uy) == target_pasture:
                            actions[u_idx] = ["PLACE", "COW"]
                            claimed_tasks.add(target_pasture)
                            animal_place_needed.remove(target_pasture)
                            continue
                        else:
                            step_dir = _shortest_path_step((ux, uy), target_pasture)
                            if step_dir:
                                actions[u_idx] = [step_dir]
                                claimed_tasks.add(target_pasture)
                                continue
                    elif (ux, uy) in SHED_ACCESS_TILES and shed.get("COW", 0) > 0:
                        actions[u_idx] = ["PICKUP", "COW", 1]
                        claimed_tasks.add(target_pasture)
                        continue
                    elif shed.get("COW", 0) > 0:
                        nearest_shed = min(SHED_ACCESS_TILES, key=lambda s: abs(ux-s[0]) + abs(uy-s[1]))
                        step_dir = _shortest_path_step((ux, uy), nearest_shed)
                        if step_dir:
                            actions[u_idx] = [step_dir]
                            claimed_tasks.add(target_pasture)
                            continue

            # 4. PASTURE BUILDING
            if pasture_build_needed:
                unclaimed_build = [p for p in pasture_build_needed if p not in claimed_tasks]
                if unclaimed_build:
                    target_p = min(unclaimed_build, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                    if (ux, uy) == target_p:
                        actions[u_idx] = ["BUILD_PASTURE"]
                        claimed_tasks.add(target_p)
                        pasture_build_needed.remove(target_p)
                        continue
                    else:
                        step_dir = _shortest_path_step((ux, uy), target_p)
                        if step_dir:
                            actions[u_idx] = [step_dir]
                            claimed_tasks.add(target_p)
                            continue

            # 5. WEED DIG / RECOVERY
            if weed_tiles:
                unclaimed_weed = [p for p in weed_tiles if p not in claimed_tasks]
                if unclaimed_weed:
                    target_w = min(unclaimed_weed, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                    if (ux, uy) == target_w:
                        actions[u_idx] = ["DIG"]
                        claimed_tasks.add(target_w)
                        weed_tiles.remove(target_w)
                        continue
                    else:
                        step_dir = _shortest_path_step((ux, uy), target_w)
                        if step_dir:
                            actions[u_idx] = [step_dir]
                            claimed_tasks.add(target_w)
                            continue

            # 6. CROP HARVEST
            unclaimed_harvest = [p for p in harvest_ready if p not in claimed_tasks]
            if unclaimed_harvest:
                target_h = min(unclaimed_harvest, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                if (ux, uy) == target_h:
                    actions[u_idx] = ["HARVEST"]
                    claimed_tasks.add(target_h)
                    harvest_ready.remove(target_h)
                    continue
                else:
                    step_dir = _shortest_path_step((ux, uy), target_h)
                    if step_dir:
                        actions[u_idx] = [step_dir]
                        claimed_tasks.add(target_h)
                        continue

            # 7. CROP WATERING
            unclaimed_water = [p for p in water_needed if p not in claimed_tasks]
            if unclaimed_water:
                target_wat = min(unclaimed_water, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                if (ux, uy) == target_wat:
                    actions[u_idx] = ["WATER"]
                    claimed_tasks.add(target_wat)
                    water_needed.remove(target_wat)
                    continue
                else:
                    step_dir = _shortest_path_step((ux, uy), target_wat)
                    if step_dir:
                        actions[u_idx] = [step_dir]
                        claimed_tasks.add(target_wat)
                        continue

            # 8. CROP PLANTING
            unclaimed_empty = [p for p in empty_crop_tiles if p not in claimed_tasks]
            if unclaimed_empty and seed_inventory and current_step < (720 - self.config.endgame_shutdown_steps):
                target_e = min(unclaimed_empty, key=lambda p: abs(ux-p[0]) + abs(uy-p[1]))
                if (ux, uy) == target_e:
                    s_to_plant = seed_inventory.pop(0)
                    actions[u_idx] = ["PLANT", s_to_plant]
                    claimed_tasks.add(target_e)
                    empty_crop_tiles.remove(target_e)
                    continue
                else:
                    step_dir = _shortest_path_step((ux, uy), target_e)
                    if step_dir:
                        actions[u_idx] = [step_dir]
                        claimed_tasks.add(target_e)
                        continue

            actions[u_idx] = ["PASS"]

        return actions
